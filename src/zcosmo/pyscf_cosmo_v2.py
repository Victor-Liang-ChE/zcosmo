"""Open sigma profiles v2: geometry optimised at BP86/def2-SVP inside the conductor (C-PCM, eps -> inf),
starting from the GFN2-xTB geometry, then the v1 BP86/def2-TZVP C-PCM single point, Hsieh averaging and
NHB/OH/OT split. This mirrors the COSMO convention (DFT geometry in the conductor) that the DMol3/UD
profiles follow. No experimental input.

Usage: python -m zcosmo.pyscf_cosmo_v2 OUTDIR CSV [--chunk i --nchunks n]
"""
from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

import numpy as np
import pandas as pd

from zcosmo.pyscf_cosmo import BOHR, RADII, cosmo_segments, to_profiles, write_sigma, xtb_geometry


def dft_geometry(sym, xyz_A, basis="def2-svp", maxsteps=100):
    from pyscf import gto, dft
    from pyscf.data import elements
    from pyscf.geomopt.berny_solver import optimize
    mol = gto.M(atom=[(s, tuple(p)) for s, p in zip(sym, xyz_A)], basis=basis, unit="Angstrom", verbose=0,
                max_memory=int(os.environ.get("QC_MEM_MB", "3000")))
    mf = dft.RKS(mol).density_fit().PCM()
    mf.xc = "b88,p86"
    mf.grids.level = 2
    mf.conv_tol = 1e-8
    s = mf.with_solvent
    s.method = "C-PCM"
    s.eps = 1e9
    s.lebedev_order = 17
    table = np.zeros(120)
    for el, r in RADII.items():
        table[elements.charge(el)] = r / BOHR
    s.radii_table = table
    m2 = optimize(mf, maxsteps=maxsteps)
    return np.asarray(m2.atom_coords(unit="Angstrom"))


def run_one(row, outdir):
    key = row["inchikey"]
    dest = Path(outdir) / f"{key}.sigma"
    if dest.exists():
        return key, "exists", 0.0
    t = time.time()
    try:
        sym, x0 = xtb_geometry(row["smiles"])
        x = dft_geometry(sym, np.asarray(x0))
        seg, e = cosmo_segments(sym, x)
        out, meta = to_profiles(sym, x, seg)
        meta["E_scf_Eh"] = e
        meta["geometry"] = "BP86/def2-SVP C-PCM conductor (pyberny)"
        write_sigma(dest, out, meta, key)
        with open(Path(outdir) / f"{key}.xyz.json", "w") as f:
            json.dump({"sym": sym, "x": np.round(x, 5).tolist()}, f)
        return key, "ok", time.time() - t
    except Exception as ex:
        return key, f"fail: {ex!r}"[:300], time.time() - t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("outdir")
    ap.add_argument("csv")
    ap.add_argument("--chunk", type=int, default=0)
    ap.add_argument("--nchunks", type=int, default=1)
    ap.add_argument("--keys", default="")
    a = ap.parse_args()
    Path(a.outdir).mkdir(parents=True, exist_ok=True)
    d = pd.read_csv(a.csv)
    if a.keys:
        d = d[d.inchikey.isin(a.keys.split(","))]
    d = d.sort_values(["heavy_atoms", "inchikey"]).reset_index(drop=True)
    d = d.iloc[a.chunk::a.nchunks]  # round-robin so chunks are balanced by size
    for r in d.to_dict("records"):
        k, st, dt = run_one(r, a.outdir)
        print(k, st, f"{dt:.0f}s", flush=True)


if __name__ == "__main__":
    main()
