"""Turn flattened ThermoML points into clean binary benchmark tables.

Produces data/processed/{idac,vle,lle,he}_raw.csv with columns keyed by
InChIKey. Scope filters are applied later (scope.py) so rejections are logged.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

import os
P = Path(os.environ.get("ZC_PROC", Path(__file__).resolve().parents[2] / "data" / "processed"))


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return np.nan


def load():
    d = pd.read_pickle(P / "tml_points.pkl")
    d = d[d.ncomp == 2].copy()
    comps = pd.read_csv(P / "tml_compounds.csv", dtype=str)
    ident = pd.read_csv(P / "tml_identity.csv", dtype=str)
    comps = comps.rename(columns={"inchikey": "xml_inchikey", "smiles": "xml_smiles"})
    comps = comps.merge(ident[["name", "formula", "inchikey", "smiles"]].drop_duplicates(["name", "formula"]),
                        on=["name", "formula"], how="left")
    # newer ThermoML files carry standard InChIKeys; they take precedence over name resolution
    comps["inchikey"] = comps.xml_inchikey.fillna(comps.inchikey)
    key = {(r.file, str(r.orgnum)): (r.inchikey, r.name) for r in comps.itertuples()}
    return d, key


def build_idac(d, key):
    a = d[d.prop == "Activity coefficient"].copy()
    rows = []
    for r in a.itertuples():
        cons = json.loads(r.constraints)
        vars_ = json.loads(r.variables)
        phases = [p["phase"] for p in json.loads(r.phases)]
        if any(p and ("Liquid mixture" in p or p == "Crystal" or p == "Glass") for p in phases):
            continue
        solute = r.prop_org
        zero = [c for c in cons if c["name"] == "Mole fraction" and c["org"] == solute and _f(c["value"]) == 0]
        if not zero:
            continue
        if any(v["name"] and ("Mole fraction" in v["name"] or "Molality" in v["name"]) for v in vars_):
            continue
        T = next((_f(v["value"]) for v in vars_ if v["name"] == "Temperature, K"), np.nan)
        if np.isnan(T):
            T = next((_f(c["value"]) for c in cons if c["name"] == "Temperature, K"), np.nan)
        comps = r.components.split("|")
        solvent = [c for c in comps if c != solute]
        if len(solvent) != 1:
            continue
        ks, ns = key.get((r.file, solute), (None, None))
        kv, nv = key.get((r.file, solvent[0]), (None, None))
        g = _f(r.value)
        if not (g > 0) or np.isnan(T):
            continue
        rows.append(dict(file=r.file, year=r.year, dataset=r.dataset, solute=ks, solvent=kv,
                         solute_name=ns, solvent_name=nv, T=T, gamma_inf=g, ln_gamma_inf=np.log(g),
                         method=r.method))
    return pd.DataFrame(rows)


def _pivot_points(sub):
    """Group rows by (file, dataset, point) and collect T, P and compositions."""
    pts = defaultdict(dict)
    for r in sub.itertuples():
        k = (r.file, r.dataset, r.point)
        p = pts[k]
        if "meta" not in p:
            p["meta"] = r
            for c in json.loads(r.constraints):
                p.setdefault("cons", []).append(c)
            for v in json.loads(r.variables):
                p.setdefault("vars", []).append(v)
        p.setdefault("props", []).append((r.prop, r.prop_org, r.prop_phase, _f(r.value)))
    return pts


def build_vle(d, key):
    vle_props = {"Vapor or sublimation pressure, kPa", "Boiling temperature at pressure P, K", "Mole fraction"}
    sets = d[d.prop.isin(vle_props)]
    # keep datasets whose phases are exactly liquid + gas
    ph = sets.phases.map(lambda s: sorted(p["phase"] for p in json.loads(s)))
    sets = sets[ph.map(lambda x: x == ["Gas", "Liquid"])]
    pts = _pivot_points(sets)
    rows = []
    for (f, ds, ip), p in pts.items():
        m = p["meta"]
        comps = m.components.split("|")
        c1, c2 = comps
        T = P_ = x1 = y1 = np.nan
        for v in p.get("vars", []) + p.get("cons", []):
            n, val = v["name"], _f(v["value"])
            if n == "Temperature, K":
                T = val
            elif n == "Pressure, kPa":
                P_ = val
            elif n == "Mole fraction" and v.get("phase") == "Liquid":
                x1 = val if v["org"] == c1 else 1 - val
            elif n == "Mole fraction" and v.get("phase") == "Gas":
                y1 = val if v["org"] == c1 else 1 - val
        for prop, org, phase, val in p["props"]:
            if prop == "Vapor or sublimation pressure, kPa":
                P_ = val
            elif prop == "Boiling temperature at pressure P, K":
                T = val
            elif prop == "Mole fraction" and phase == "Gas":
                y1 = val if org == c1 else 1 - val
            elif prop == "Mole fraction" and phase == "Liquid":
                x1 = val if org == c1 else 1 - val
        if np.isnan(T) or np.isnan(P_) or np.isnan(x1):
            continue
        k1, n1 = key.get((f, c1), (None, None))
        k2, n2 = key.get((f, c2), (None, None))
        rows.append(dict(file=f, year=m.year, dataset=ds, point=ip, c1=k1, c2=k2, name1=n1, name2=n2,
                         org1=c1, org2=c2, T=T, P=P_, x1=x1, y1=y1))
    vle = pd.DataFrame(rows)
    # Vapor compositions often sit in a separate dataset of the same file that
    # shares (T or P, x1). Join them back on rounded conditions.
    ys = []
    for (f, ds, ip), p in pts.items():
        m = p["meta"]
        c1, c2 = m.components.split("|")
        yv = [(org, val) for prop, org, phase, val in p["props"] if prop == "Mole fraction" and phase == "Gas"]
        if not yv:
            continue
        T = P_ = x1 = np.nan
        for v in p.get("vars", []) + p.get("cons", []):
            n, val = v["name"], _f(v["value"])
            if n == "Temperature, K":
                T = val
            elif n == "Pressure, kPa":
                P_ = val
            elif n == "Mole fraction" and v.get("phase") == "Liquid":
                x1 = val if v["org"] == c1 else 1 - val
        org, val = yv[0]
        ys.append(dict(file=f, org1=c1, org2=c2, T=T, P=P_, x1=x1, y1_j=val if org == c1 else 1 - val))
    ys = pd.DataFrame(ys).dropna(subset=["x1"])
    vle["xk"] = vle.x1.round(4)
    ys["xk"] = ys.x1.round(4)
    vle["Tk"] = vle["T"].round(1)
    ys["Tk"] = ys["T"].round(1)
    yT = ys.dropna(subset=["T"]).drop_duplicates(["file", "org1", "org2", "xk", "Tk"])
    vle = vle.merge(yT[["file", "org1", "org2", "xk", "Tk", "y1_j"]], on=["file", "org1", "org2", "xk", "Tk"],
                    how="left")
    vle["y1"] = vle.y1.fillna(vle.y1_j)
    vle = vle.drop(columns=["y1_j", "xk", "Tk"]).drop_duplicates(["file", "org1", "org2", "T", "P", "x1"])
    # classify each dataset as isothermal or isobaric from the data itself
    g = vle.groupby(["file", "dataset"])
    Tsp = g["T"].transform(lambda s: s.max() - s.min())
    Psp = g["P"].transform(lambda s: (s.max() - s.min()) / max(s.mean(), 1e-9))
    vle["iso"] = np.where(Tsp < 0.05, "T", np.where(Psp < 0.005, "P", "?"))
    return vle


def build_lle(d, key):
    """Binodal points (T, x1) on the liquid-liquid coexistence curve.

    ThermoML stores LLE either as the composition of one liquid phase at a set
    temperature, or as the LLE temperature at a set composition (cloud points).
    Both give points on the binodal; the branch is not always identifiable, so
    scoring uses the distance to the nearest predicted branch.
    """
    rows = []
    two_liq = d.phases.map(lambda s: sorted(p["phase"] for p in json.loads(s))).map(
        lambda x: x == ["Liquid mixture 1", "Liquid mixture 2"])
    a = d[(d.prop == "Mole fraction") & two_liq]
    b = d[d.prop == "Liquid-liquid equilibrium temperature, K"]
    for r in pd.concat([a, b]).itertuples():
        c1, c2 = r.components.split("|")
        T = x1 = np.nan
        for v in json.loads(r.variables) + json.loads(r.constraints):
            if v["name"] == "Temperature, K":
                T = _f(v["value"])
            elif v["name"] == "Mole fraction":
                x1 = _f(v["value"]) if v["org"] == c1 else 1 - _f(v["value"])
            elif v["name"] == "Mass fraction":
                x1 = np.nan  # needs molar masses; handled in scope step
        if r.prop == "Mole fraction":
            x1 = _f(r.value) if r.prop_org == c1 else 1 - _f(r.value)
        else:
            T = _f(r.value)
        if np.isnan(T) or np.isnan(x1):
            continue
        k1, n1 = key.get((r.file, c1), (None, None))
        k2, n2 = key.get((r.file, c2), (None, None))
        rows.append(dict(file=r.file, year=r.year, dataset=r.dataset, c1=k1, c2=k2, name1=n1, name2=n2,
                         T=T, x1=x1, kind="composition" if r.prop == "Mole fraction" else "cloud_point"))
    return pd.DataFrame(rows)


def build_he(d, key):
    sub = d[d.prop == "Excess molar enthalpy (molar enthalpy of mixing), kJ/mol"]
    rows = []
    for r in sub.itertuples():
        c1, c2 = r.components.split("|")
        T = x1 = np.nan
        for v in json.loads(r.variables) + json.loads(r.constraints):
            if v["name"] == "Temperature, K":
                T = _f(v["value"])
            elif v["name"] == "Mole fraction":
                x1 = _f(v["value"]) if v["org"] == c1 else 1 - _f(v["value"])
        if np.isnan(T) or np.isnan(x1):
            continue
        k1, n1 = key.get((r.file, c1), (None, None))
        k2, n2 = key.get((r.file, c2), (None, None))
        rows.append(dict(file=r.file, year=r.year, dataset=r.dataset, c1=k1, c2=k2, name1=n1, name2=n2,
                         T=T, x1=x1, HE_J=1000 * _f(r.value)))
    return pd.DataFrame(rows)


def main():
    d, key = load()
    for name, fn in [("idac", build_idac), ("vle", build_vle), ("lle", build_lle), ("he", build_he)]:
        t = fn(d, key)
        t.to_csv(P / f"{name}_raw.csv", index=False)
        both = t.dropna(subset=[c for c in t.columns if c in ("solute", "solvent", "c1", "c2")])
        print(f"{name}: rows={len(t)} resolved_both={len(both)}")


if __name__ == "__main__":
    main()
