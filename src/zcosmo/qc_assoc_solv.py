"""Z0w2 ingredient: electrostatic continuum desolvation of each H-bond dimer.

For every dimer in results/qc/hbond_dimers_b3lyp_def2-tzvp.csv (B3LYP geometry; monomers frozen at their
dimer geometry, deformation is already in the gas-phase term), compute BP86/def2-TZVP C-PCM energies at
a fixed grid of permittivities, with the same radii as the sigma profiles, and
  ddG_solv(eps) = [E(AB,eps)-E(AB,gas)] - [E(A,eps)-E(A,gas)] - [E(B,eps)-E(B,gas)]   (kcal/mol).
Writes results/qc/assoc_solv.csv (one row per dimer x eps). No experimental input.
Usage: python -m zcosmo.qc_assoc_solv [--nproc N]
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
from rdkit import Chem

ROOT = Path(__file__).resolve().parents[2]
HARTREE_KCAL = 627.509474
BOHR = 0.52917721067
EPS_GRID = [2.0, 4.0, 8.0, 16.0, 32.0, 64.0, 1e9]


def energies(sym, x):
    from pyscf import gto, dft
    from pyscf.data import elements
    from zcosmo.pyscf_cosmo import RADII
    mol = gto.M(atom=[(s, tuple(p)) for s, p in zip(sym, x)], basis="def2-tzvp", unit="Angstrom", verbose=0,
                max_memory=int(os.environ.get("QC_MEM_MB", "3000")))
    out = {}
    mf = dft.RKS(mol).density_fit()
    mf.xc = "b88,p86"; mf.grids.level = 3; mf.conv_tol = 1e-9
    out[1.0] = mf.kernel()
    dm = mf.make_rdm1()
    table = np.zeros(120)
    for el, r in RADII.items():
        table[elements.charge(el)] = r / BOHR
    for eps in EPS_GRID:
        m2 = dft.RKS(mol).density_fit().PCM()
        m2.xc = "b88,p86"; m2.grids.level = 3; m2.conv_tol = 1e-9
        s = m2.with_solvent
        s.method = "C-PCM"; s.eps = eps; s.lebedev_order = 29; s.vdw_scale = 1.0; s.radii_table = table
        out[eps] = m2.kernel(dm0=dm)
        if not m2.converged:
            raise RuntimeError(f"SCF not converged at eps={eps}")
    return out


def one(row):
    from zcosmo.qc_hbond import DIMERS
    nd = {d[0]: Chem.AddHs(Chem.MolFromSmiles(d[1])).GetNumAtoms() for d in DIMERS}
    g = json.loads(row["xyz"])
    sym, x = g["sym"], np.array(g["x"])
    k = nd[row["label"]]
    eab, ea, eb = energies(sym, x), energies(sym[:k], x[:k]), energies(sym[k:], x[k:])
    rows = []
    for eps in EPS_GRID:
        dd = ((eab[eps] - eab[1.0]) - (ea[eps] - ea[1.0]) - (eb[eps] - eb[1.0])) * HARTREE_KCAL
        rows.append(dict(label=row["label"], eps=eps, ddG_solv_kcal=dd,
                         dGsolv_AB=(eab[eps] - eab[1.0]) * HARTREE_KCAL,
                         dGsolv_A=(ea[eps] - ea[1.0]) * HARTREE_KCAL, dGsolv_B=(eb[eps] - eb[1.0]) * HARTREE_KCAL))
    print(row["label"], [round(r["ddG_solv_kcal"], 2) for r in rows], flush=True)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nproc", type=int, default=1)
    a = ap.parse_args()
    d = pd.read_csv(ROOT / "results/qc/hbond_dimers_b3lyp_def2-tzvp.csv").to_dict("records")
    if a.nproc > 1:
        import multiprocessing as mp
        with mp.get_context("spawn").Pool(a.nproc) as p:
            res = p.map(one, d)
    else:
        res = [one(r) for r in d]
    pd.DataFrame([r for rr in res for r in rr]).to_csv(ROOT / "results/qc/assoc_solv.csv", index=False)


if __name__ == "__main__":
    main()
