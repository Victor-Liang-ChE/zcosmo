"""Z0w: Z0x electrostatics/dispersion without the COSMO H-bond term, plus Wertheim TPT1 association
with site-pair strengths from first-principles dimerization free energies (see PREREGISTRATION.md)."""
from __future__ import annotations

from functools import lru_cache

import numpy as np
import pandas as pd
from rdkit import Chem

from zcosmo.cosmosac import load_fluid
from zcosmo.models import ROOT
from zcosmo.z0x import Z0xBinary
from zcosmo.qc_hbond import DIMERS

KB = 1.380649e-23
P0 = 101325.0
R_KCAL = 1.987204e-3
DONORS = ("OH", "NH")
ACCEPTORS = ("Ohyd", "Oother", "N")


def sites(smiles: str) -> dict:
    """Site counts {type: n} from structure, fixed a priori."""
    m = Chem.AddHs(Chem.MolFromSmiles(smiles))
    s = {}
    for a in m.GetAtoms():
        el = a.GetSymbol()
        if el == "H":
            nb = a.GetNeighbors()[0].GetSymbol()
            if nb == "O":
                s["OH"] = s.get("OH", 0) + 1
            elif nb == "N":
                s["NH"] = s.get("NH", 0) + 1
        elif el == "O":
            t = "Ohyd" if any(n.GetSymbol() == "H" for n in a.GetNeighbors()) else "Oother"
            s[t] = s.get(t, 0) + 2
        elif el == "N":
            s["N"] = s.get("N", 0) + 1
    return s


def _dimer_classes():
    out = {}
    for label, dsmi, _, asmi, _, _, _ in DIMERS:
        dm = Chem.MolFromSmiles(dsmi)
        da = next(a for a in dm.GetAtoms() if a.GetAtomMapNum() == 1)
        dcls = "OH" if da.GetSymbol() == "O" else "NH"
        am = Chem.MolFromSmiles(asmi)
        aa = next(a for a in am.GetAtoms() if a.GetAtomMapNum() == 1)
        if aa.GetSymbol() == "N":
            acls = "N"
        else:
            acls = "Ohyd" if aa.GetTotalNumHs() > 0 else "Oother"
        out[label] = (dcls, acls)
    return out


@lru_cache(maxsize=1)
def class_thermo():
    """Mean dH (kcal/mol) and dS (kcal/mol/K) per (donor, acceptor) class pair."""
    t = pd.read_csv(ROOT / "results/qc/assoc_thermo.csv")
    cls = _dimer_classes()
    t["pair"] = t.label.map(cls)
    t["dS_kcal"] = t.dS_J_molK / 4184.0
    g = {p: (float(h.dH_kcal.mean()), float(h.dS_kcal.mean())) for p, h in t.groupby(t.pair.map(str))}
    allmean = (float(t.dH_kcal.mean()), float(t.dS_kcal.mean()))
    return {p: g.get(str(p), allmean) for p in [(d, a) for d in DONORS for a in ACCEPTORS]}


def delta(T: float) -> dict:
    """Site-pair association strength in A^3 per molecule pair."""
    kT_P = KB * T / P0 * 1e30  # A^3
    out = {}
    for (d, a), (dH, dS) in class_thermo().items():
        dG = dH - T * dS
        out[(d, a)] = kT_P * np.exp(-dG / (R_KCAL * T))
    return out


def _solve_X(c, S, D, tol=1e-13, it=2000):
    """c: concentrations (n_comp,), S: list of site dicts, D: {(donor, acceptor): Delta}. Returns X list."""
    X = [{k: 0.5 for k in s} for s in S]
    for _ in range(it):
        err = 0.0
        newX = []
        for i, s in enumerate(S):
            xi = {}
            for A in s:
                tot = 0.0
                for j, sj in enumerate(S):
                    if c[j] == 0:
                        continue
                    for B, nB in sj.items():
                        if A in DONORS and B in ACCEPTORS:
                            dl = D[(A, B)]
                        elif A in ACCEPTORS and B in DONORS:
                            dl = D[(B, A)]
                        else:
                            continue
                        tot += c[j] * nB * X[j][B] * dl
                v = 1.0 / (1.0 + tot)
                xi[A] = 0.5 * X[i][A] + 0.5 * v
                err = max(err, abs(v - X[i][A]))
            newX.append(xi)
        X = newX
        if err < tol:
            break
    return X


def g_assoc(x, V, S, D):
    x = np.asarray(x, float)
    vmix = float(x @ V)
    c = x / vmix
    X = _solve_X(c, S, D)
    return sum(x[i] * sum(n * (np.log(X[i][A]) - X[i][A] / 2 + 0.5) for A, n in S[i].items())
               for i in range(len(S)))


class Z0wBinary(Z0xBinary):
    def __init__(self, keys, smiles):
        super().__init__(keys)
        self.z0 = self.z0.with_(c_OH_OH=0.0, c_OT_OT=0.0, c_OH_OT=0.0)
        self.S = [sites(s) for s in smiles]
        self.Vm = np.array([load_fluid(k).V for k in keys])
        self._pure = {}

    def _ga(self, T, x1):
        D = delta(T)
        key = round(T, 6)
        if key not in self._pure:
            self._pure[key] = [g_assoc([1, 0], self.Vm, self.S, D), g_assoc([0, 1], self.Vm, self.S, D)]
        p = self._pure[key]
        return g_assoc([x1, 1 - x1], self.Vm, self.S, D) - x1 * p[0] - (1 - x1) * p[1]

    def _g(self, T, x1):
        x1 = min(max(x1, 0.0), 1.0)
        return super()._g(T, x1) + self._ga(T, x1)


# ---------------------------------------------------------------- Z0w2: condensed-phase association
def _f(eps):
    return (eps - 1.0) / eps


@lru_cache(maxsize=1)
def class_desolv():
    """{(donor, acceptor): (f_grid, ddG_grid)} class-mean electrostatic desolvation vs f=(eps-1)/eps."""
    s = pd.read_csv(ROOT / "results/qc/assoc_solv.csv")
    cls = _dimer_classes()
    s["pair"] = s.label.map(cls).map(str)
    g = s.groupby(["pair", "eps"]).ddG_solv_kcal.mean().reset_index()
    allm = s.groupby("eps").ddG_solv_kcal.mean()
    out = {}
    for p in [(d, a) for d in DONORS for a in ACCEPTORS]:
        h = g[g.pair == str(p)].set_index("eps").ddG_solv_kcal
        h = h if len(h) else allm
        e = np.array(sorted(h.index))
        out[p] = (np.r_[0.0, _f(e)], np.r_[0.0, h.loc[e].to_numpy()])
    return out


def delta_liq(T: float, eps: float) -> dict:
    kT_P = KB * T / P0 * 1e30
    f = _f(max(eps, 1.0))
    out = {}
    ds = class_desolv()
    for p, (dH, dS) in class_thermo().items():
        fg, dg = ds[p]
        out[p] = kT_P * np.exp(-(dH - T * dS + float(np.interp(f, fg, dg))) / (R_KCAL * T))
    return out


class Z0w2Binary(Z0wBinary):
    """Z0w with site-pair strengths evaluated in the mixture's own (fit-free) dielectric continuum."""

    def _eps_mix(self, x1):
        phi = np.array([x1, 1 - x1]) * self.V
        phi /= phi.sum()
        return float(phi @ self.eps)

    def _ga(self, T, x1):
        key = round(T, 6)
        if key not in self._pure:
            self._pure[key] = [g_assoc([1, 0], self.Vm, self.S, delta_liq(T, self.eps[0])),
                               g_assoc([0, 1], self.Vm, self.S, delta_liq(T, self.eps[1]))]
        p = self._pure[key]
        D = delta_liq(T, self._eps_mix(x1))
        return g_assoc([x1, 1 - x1], self.Vm, self.S, D) - x1 * p[0] - (1 - x1) * p[1]
