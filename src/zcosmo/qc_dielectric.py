"""Pure-liquid static permittivity from first principles (Onsager equation).

mu    : GFN2-xTB dipole moment of the MMFF conformer (tblite)
alpha : D4 static polarizability (results/qc/dispersion.csv)
N     : 1 / V_COSMO (molecules per A^3)
n^2   : Clausius-Mossotti, (n^2 - 1)/(n^2 + 2) = 4 pi N alpha / 3
eps   : Onsager, 2 eps^2 - eps (n^2 + (n^2 + 2)^2 y) - n^4 = 0,  y = N mu^2 / (9 eps0 k T)
Writes results/qc/dielectric.csv
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem

from zcosmo.cosmosac import load_fluid

ROOT = Path(__file__).resolve().parents[2]
BOHR = 0.52917721067
E = 1.602176634e-19
EPS0 = 8.8541878128e-12
KB = 1.380649e-23


def xtb_dipole_debye(smiles):
    from tblite.interface import Calculator
    m = Chem.AddHs(Chem.MolFromSmiles(smiles))
    AllChem.EmbedMolecule(m, randomSeed=7)
    try:
        AllChem.MMFFOptimizeMolecule(m)
    except Exception:
        pass
    x = m.GetConformer().GetPositions() / BOHR
    z = np.array([a.GetAtomicNum() for a in m.GetAtoms()])
    calc = Calculator("GFN2-xTB", z, x)
    calc.set("verbosity", 0)
    res = calc.singlepoint()
    d = np.linalg.norm(res.get("dipole"))  # e*bohr
    return d * 2.541746


def onsager_eps(mu_D, alpha_A3, V_A3, T=298.15):
    N = 1.0 / V_A3                                   # A^-3
    cm = 4 * np.pi * N * alpha_A3 / 3
    cm = min(cm, 0.95)
    n2 = (1 + 2 * cm) / (1 - cm)
    mu = mu_D * 3.33564e-30                          # C m
    y = (N * 1e30) * mu ** 2 / (9 * EPS0 * KB * T)
    b = n2 + (n2 + 2) ** 2 * y
    return (b + np.sqrt(b * b + 8 * n2 * n2)) / 4, n2


def main():
    disp = pd.read_csv(ROOT / "results/qc/dispersion.csv")
    comp = pd.read_csv(Path(__import__("os").environ.get("ZC_BENCH", ROOT / "data/benchmark")) / "compounds.csv").set_index("inchikey")
    rows = []
    for r in disp.itertuples():
        try:
            mu = xtb_dipole_debye(comp.loc[r.inchikey, "smiles"])
            V = load_fluid(r.inchikey).V
            eps, n2 = onsager_eps(mu, r.alpha_au * BOHR ** 3, V)
        except Exception:
            mu = eps = n2 = np.nan
        rows.append(dict(inchikey=r.inchikey, name=r.name, dipole_D=mu, n2=n2, eps=eps))
    pd.DataFrame(rows).to_csv(ROOT / "results/qc/dielectric.csv", index=False)
    print(pd.DataFrame(rows).describe())


if __name__ == "__main__":
    main()
