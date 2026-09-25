"""Apply v1 scope, data-quality filters and frozen molecule-level splits.

Every rejected row is logged with a reason in data/processed/rejections.csv.
Outputs data/benchmark/{idac,vle,lle,he}.csv, compounds.csv, splits.json (+ sha256).
"""
from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit import RDLogger

RDLogger.DisableLog("rdApp.*")

ROOT = Path(__file__).resolve().parents[2]
import os
PROC = Path(os.environ.get("ZC_PROC", ROOT / "data" / "processed"))
BENCH = Path(os.environ.get("ZC_BENCH", ROOT / "data" / "benchmark"))
ALLOWED = {"C", "H", "N", "O", "F", "Cl", "Br", "S"}
TMIN, TMAX, PMAX = 250.0, 450.0, 500.0
MAX_HEAVY = 25
SEED = 20260924
WATER = "XLYOFNOQVPJJNP-UHFFFAOYSA-N"


def compound_table():
    ud = pd.read_csv(PROC / "ud_complist.csv", dtype=str)
    ident = pd.read_csv(PROC / "tml_identity.csv", dtype=str).dropna(subset=["inchikey"])
    rows = {}
    for r in ident.itertuples():
        rows.setdefault(r.inchikey, dict(inchikey=r.inchikey, name=r.name, smiles=r.smiles))
    for r in ud.itertuples():
        rows[r.inchikey] = dict(inchikey=r.inchikey, name=r.name.lower(), smiles=r.smiles, cas=r.cas)
    df = pd.DataFrame(rows.values())
    from zcosmo.cosmosac import sigma_path
    df["has_sigma_ud"] = [sigma_path(k) is not None for k in df.inchikey]
    heavy, elems, ok = [], [], []
    for s in df.smiles:
        m = Chem.MolFromSmiles(s) if isinstance(s, str) else None
        if m is None:
            heavy.append(np.nan); elems.append(""); ok.append(False); continue
        e = {a.GetSymbol() for a in Chem.AddHs(m).GetAtoms()}
        charged = any(a.GetFormalCharge() != 0 for a in m.GetAtoms())
        heavy.append(m.GetNumHeavyAtoms()); elems.append(",".join(sorted(e)))
        ok.append(e <= ALLOWED and not charged and "." not in s)
    df["heavy_atoms"] = heavy
    df["elements"] = elems
    df["in_scope_chem"] = np.array(ok) & (df.heavy_atoms <= MAX_HEAVY)
    return df


@lru_cache(maxsize=None)
def psat_model(inchikey: str):
    from chemicals.identifiers import search_chemical
    from thermo import VaporPressure
    try:
        c = search_chemical("InChIKey=" + inchikey)
        vp = VaporPressure(CASRN=c.CASs)
        if vp.method is None:
            return None
        return vp
    except Exception:
        return None


def psat(inchikey: str, T: float) -> float:
    vp = psat_model(inchikey)
    if vp is None:
        return np.nan
    try:
        v = vp(T)
        return v / 1000.0 if v else np.nan  # kPa
    except Exception:
        return np.nan


def clean_idac(t, rej):
    t = t.dropna(subset=["solute", "solvent"]).copy()
    t["Tbin"] = (t["T"] / 2.0).round() * 2.0
    keep = []
    for (a, b, T), g in t.groupby(["solute", "solvent", "Tbin"]):
        if len(g) == 1:
            keep.append(g.index[0]); continue
        med = g.ln_gamma_inf.median()
        good = g[(g.ln_gamma_inf - med).abs() <= 0.2]
        if len(good) >= 0.5 * len(g):
            keep += list(good.index)
            for i in g.index.difference(good.index):
                rej.append(("idac", i, "repeat disagreement >0.2 in ln gamma"))
        else:
            for i in g.index:
                rej.append(("idac", i, "repeat measurements disagree, group dropped"))
    return t.loc[keep].drop(columns="Tbin")


def herington(g, c1, c2):
    """Herington area test on one VLE dataset. Returns (D, passed) or (nan, None) if untestable."""
    g = g.dropna(subset=["y1"]).sort_values("x1")
    g = g[(g.x1 > 0) & (g.x1 < 1) & (g.y1 > 0) & (g.y1 < 1)]
    if len(g) < 5 or g.x1.min() > 0.15 or g.x1.max() < 0.85:
        return np.nan, None
    p1 = np.array([psat(c1, T) for T in g["T"]])
    p2 = np.array([psat(c2, T) for T in g["T"]])
    if np.isnan(p1).any() or np.isnan(p2).any():
        return np.nan, None
    g1 = g.y1 * g.P / (g.x1 * p1)
    g2 = (1 - g.y1) * g.P / ((1 - g.x1) * p2)
    f = np.log(g1 / g2).to_numpy()
    x = g.x1.to_numpy()
    xs = np.concatenate([[0], x, [1]])
    fs = np.concatenate([[f[0]], f, [f[-1]]])
    pos = np.trapezoid(np.clip(fs, 0, None), xs)
    neg = -np.trapezoid(np.clip(fs, None, 0), xs)
    if pos + neg == 0:
        return 0.0, True
    D = 100 * abs(pos - neg) / (pos + neg)
    # Near-ideal systems make D ill-conditioned: a 2% Psat error flips the sign
    # of the whole area. Accept when the absolute area imbalance is < 0.03.
    if abs(pos - neg) < 0.03:
        return D, True
    if g.iso.iloc[0] == "P":
        J = 150 * (g["T"].max() - g["T"].min()) / g["T"].min()
        return D, (D - J) < 10
    return D, D < 10


@lru_cache(maxsize=None)
def tc(inchikey: str) -> float:
    from chemicals.identifiers import search_chemical
    from chemicals.critical import Tc
    try:
        v = Tc(search_chemical("InChIKey=" + inchikey).CASs)
        return float(v) if v else np.nan
    except Exception:
        return np.nan


def assign_series(t):
    """Split each dataset into isothermal or isobaric series."""
    t = t.copy()
    t["Tk"] = t["T"].round(1)
    t["Pk"] = np.round(np.log(t["P"].clip(lower=1e-6)) / 0.005)
    nT = t.groupby(["file", "dataset", "Tk"])["x1"].transform("size")
    nP = t.groupby(["file", "dataset", "Pk"])["x1"].transform("size")
    t["iso"] = np.where(nT >= 3, "T", np.where(nP >= 3, "P", "single"))
    t["series"] = (t.file + "#" + t.dataset.astype(str) + "#" + t.iso + "#" +
                   np.where(t.iso == "T", t.Tk.astype(str), t.Pk.astype(str)))
    return t.drop(columns=["Tk", "Pk"])


def clean_vle(t, rej):
    t = t.dropna(subset=["c1", "c2"]).copy()
    t = t[(t.x1 >= 0) & (t.x1 <= 1)]
    t = assign_series(t)
    # subcritical check: both components must be below their critical temperature
    tc1 = t.c1.map(tc)
    tc2 = t.c2.map(tc)
    sub = ~((t["T"] >= 0.98 * tc1) | (t["T"] >= 0.98 * tc2))  # unknown Tc is not a rejection
    for i in t.index[~sub]:
        rej.append(("vle", i, "a component is near or above its critical temperature (gas solubility)"))
    t = t[sub]
    keep = []
    status = {}
    for s, g in t.groupby("series"):
        D, ok = herington(g, g.c1.iloc[0], g.c2.iloc[0])
        status[s] = "untested" if ok is None else ("pass" if bool(ok) else "fail")
        if ok is not None and not bool(ok):
            for i in g.index:
                rej.append(("vle", i, f"Herington area test failed (D={D:.1f})"))
        else:
            keep += list(g.index)
    out = t.loc[keep].copy()
    out["consistency"] = out.series.map(status)
    return out


def clean_lle(t, rej):
    """Keep binary LLE systems whose data really describe a two-liquid region.

    Single isolated 'Liquid mixture' compositions are often binary sub-data of
    ternary or multiphase studies. Require: composition-type systems with both
    coexisting branches at one temperature (points below and above x1 = 0.5 within
    2 K), cloud-point systems with at least 5 points.
    """
    t = t.copy()
    t["sysk"] = _pairkey(t.c1, t.c2)
    t["Tb"] = (t["T"] / 2).round()
    keep = set()
    for s, g in t.groupby("sysk"):
        comp = g[g.kind == "composition"]
        ok_comp = any((h.x1 < 0.5).any() and (h.x1 > 0.5).any() for _, h in comp.groupby("Tb"))
        ok_cloud = (g.kind == "cloud_point").sum() >= 5
        if ok_comp or ok_cloud:
            keep.add(s)
    m = t.sysk.isin(keep)
    for i in t.index[~m]:
        rej.append(("lle", i, "no evidence of two coexisting liquid branches (isolated compositions)"))
    return t[m].drop(columns=["sysk", "Tb"])


def _pairkey(a, b):
    a = a.astype(str).to_numpy()
    b = b.astype(str).to_numpy()
    return np.where(a < b, np.char.add(np.char.add(a, "|"), b), np.char.add(np.char.add(b, "|"), a))


def apply_scope(t, cols, comp, rej, name):
    ok_chem = set(comp.inchikey[comp.in_scope_chem])
    has_sig = set(comp.inchikey[comp.has_sigma_ud])
    m_chem = t[cols[0]].isin(ok_chem) & t[cols[1]].isin(ok_chem)
    for i in t.index[~m_chem]:
        rej.append((name, i, "compound outside v1 chemistry scope"))
    t = t[m_chem]
    m_T = t["T"].between(TMIN, TMAX)
    for i in t.index[~m_T]:
        rej.append((name, i, "temperature outside 250-450 K"))
    t = t[m_T]
    if "P" in t:
        m_P = t["P"] <= PMAX
        for i in t.index[~m_P]:
            rej.append((name, i, "pressure above 500 kPa"))
        t = t[m_P]
    t = t.copy()
    t["has_sigma"] = t[cols[0]].isin(has_sig) & t[cols[1]].isin(has_sig)
    return t


def make_splits(all_compounds, rng_seed=SEED, frac=0.2):
    comps = sorted(c for c in all_compounds if c != WATER)
    rng = np.random.default_rng(rng_seed)
    held = set(rng.choice(comps, size=int(round(frac * len(comps))), replace=False))
    return held


def tag_split(t, cols, held):
    a = t[cols[0]].isin(held)
    b = t[cols[1]].isin(held)
    t = t.copy()
    t["split"] = np.where(a & b, "test_both", np.where(a | b, "test_one", "train"))
    return t


def main():
    BENCH.mkdir(parents=True, exist_ok=True)
    comp = compound_table()
    rej = []
    idac = clean_idac(pd.read_csv(PROC / "idac_raw.csv"), rej)
    vle = clean_vle(pd.read_csv(PROC / "vle_raw.csv"), rej)
    lle = pd.read_csv(PROC / "lle_raw.csv").dropna(subset=["c1", "c2"])
    he = pd.read_csv(PROC / "he_raw.csv").dropna(subset=["c1", "c2"])
    lle = lle[(lle.x1 > 0) & (lle.x1 < 1)]
    lle = clean_lle(lle, rej)
    tables = {"idac": (idac, ("solute", "solvent")), "vle": (vle, ("c1", "c2")),
              "lle": (lle, ("c1", "c2")), "he": (he, ("c1", "c2"))}
    scoped = {k: apply_scope(t, c, comp, rej, k) for k, (t, c) in tables.items()}
    allc = set()
    for k, t in scoped.items():
        c = tables[k][1]
        allc |= set(t[c[0]]) | set(t[c[1]])
    # held-out compounds are drawn from every in-scope compound, independent of
    # which tables survive filtering, so later data-cleaning changes cannot move the split
    held = make_splits(set(comp.inchikey[comp.in_scope_chem]))
    if os.environ.get("ZC_EXTENDED"):
        # extended benchmark: keep the frozen v1 held-out list, hash-assign compounds new to it
        import hashlib as _h
        v1 = json.loads((ROOT / "data/benchmark/splits.json").read_text())
        v1_held = set(v1["held_out_compounds"])
        v1_all = set(pd.read_csv(ROOT / "data/benchmark/compounds.csv").inchikey)
        known = v1_held | v1_all
        held = set(v1_held) | {k for k in comp.inchikey[comp.in_scope_chem]
                               if k not in known and k != WATER and int(_h.sha256(k.encode()).hexdigest(), 16) % 5 == 0}
    for k, t in scoped.items():
        t = tag_split(t, tables[k][1], held)
        t.to_csv(BENCH / f"{k}.csv", index=False)
        print(k, len(t), t.split.value_counts().to_dict(), "with sigma:", int(t.has_sigma.sum()))
    comp[comp.inchikey.isin(allc)].assign(held_out=lambda d: d.inchikey.isin(held)).to_csv(
        BENCH / "compounds.csv", index=False)
    pd.DataFrame(rej, columns=["table", "row", "reason"]).to_csv(PROC / "rejections.csv", index=False)
    splits = {"seed": SEED, "held_out_compounds": sorted(held), "water_always_train": True}
    s = json.dumps(splits, indent=1, sort_keys=True)
    (BENCH / "splits.json").write_text(s)
    (BENCH / "splits.sha256").write_text(hashlib.sha256(s.encode()).hexdigest() + "\n")
    print("compounds", len(allc), "held out", len(held))
    print(pd.DataFrame(rej, columns=["table", "row", "reason"]).groupby(["table", "reason"]).size())


if __name__ == "__main__":
    main()
