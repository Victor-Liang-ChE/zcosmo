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


def profile_revision():
    import hashlib
    from importlib.metadata import version
    here = Path(__file__).resolve().parent
    code = b"".join((here / name).read_bytes() for name in
                    ("pyscf_cosmo.py", "pyscf_cosmo_v2.py", "pcm_lu.py") if (here / name).exists())
    packages = [(name, version(name)) for name in ("pyscf", "pyberny", "rdkit", "tblite", "ase", "numpy", "scipy")]
    return hashlib.sha256(code + json.dumps(packages).encode()
                          + os.environ.get("ZC_TRIC_PREOPT", "0").encode()
                          + os.environ.get("ZC_BERNY_NOISE_EH", "").encode()
                          + os.environ.get("ZC_R3_COOH_FLAG", "0").encode()).hexdigest()


def dft_geometry(sym, xyz_A, basis="def2-svp", maxsteps=100, partial=None, spin=0):
    """partial: optional JSON path; the current geometry is written there after every Berny cycle so a job
    killed by a wall-clock cap can resume from its last geometry (same functional, basis, solvent and
    convergence criteria; only the Berny Hessian guess restarts)."""
    from pyscf import gto, dft
    from pyscf.data import elements
    from pyscf.geomopt.berny_solver import kernel
    mol = gto.M(atom=[(s, tuple(p)) for s, p in zip(sym, xyz_A)], basis=basis, unit="Angstrom", verbose=0,
                spin=spin, max_memory=int(os.environ.get("QC_MEM_MB", "3000")))
    mf = (dft.UKS(mol) if spin else dft.RKS(mol)).density_fit().PCM()
    from zcosmo.pcm_lu import cache_pcm, cache_pcm3c
    # P9 (E, 2026-09-28): cached surface 3-centre integrals; accepted as E; ZC_PCM3C=0 restores the P1 path
    mf = cache_pcm3c(mf) if os.environ.get("ZC_PCM3C", "1") == "1" else cache_pcm(mf)
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
    # E-class restart (registered 2026-09-30, off unless ZC_BERNY_STATE=1): the pyberny optimiser state (Hessian, trust
    # radius, history) is pickled next to the geometry checkpoint and restored on resume, so a resumed run continues
    # exactly the optimisation an uninterrupted run would have done. ZC_MAXSTEPS only overrides the per-pass step cap.
    keep_state = os.environ.get("ZC_BERNY_STATE", "0") == "1" and partial is not None
    maxsteps = int(os.environ.get("ZC_MAXSTEPS", maxsteps))
    state_path = str(partial) + ".bstate" if keep_state else None
    kw = {}
    if keep_state and os.path.exists(state_path):
        try:
            import pickle
            with open(state_path, "rb") as f:
                st = pickle.load(f)
            g = np.asarray(st["geom"].coords, dtype=float)
            if g.shape == (len(sym), 3) and np.abs(g - np.asarray(xyz_A, dtype=float)).max() < 1e-4:
                kw["restart"] = st
        except Exception:
            kw = {}
    noise = os.environ.get("ZC_BERNY_NOISE_EH")
    if noise:
        from importlib.metadata import version
        from dataclasses import replace
        if version("pyberny") != "0.7.0" or float(noise) != 2e-7:
            raise ValueError("R2 A-trial is fixed at pyberny 0.7.0, energy_noise=2e-7 Eh")
        kw["energy_noise"] = 2e-7
        if "restart" in kw:
            # Berny ignores keyword parameters when restart is supplied.
            kw["restart"]["params"] = replace(kw["restart"]["params"], energy_noise=2e-7)
    def cb(env):
        if partial is not None and env.get("mol") is not None:
            tmp = str(partial) + ".tmp"
            with open(tmp, "w") as f:
                json.dump({"sym": list(sym), "x": env["mol"].atom_coords(unit="Angstrom").tolist(),
                           "cycle": int(env.get("cycle", -1))}, f)
            os.replace(tmp, partial)
        if keep_state and env.get("optimizer") is not None:
            import pickle
            from dataclasses import fields
            s_ = env["optimizer"]._state
            tmp = state_path + ".tmp"
            with open(tmp, "wb") as f:
                pickle.dump({fl.name: getattr(s_, fl.name) for fl in fields(s_)}, f)
            os.replace(tmp, state_path)
    converged, m2 = kernel(mf, maxsteps=maxsteps, callback=cb, **kw)
    if not converged:
        raise RuntimeError(f"Berny did not converge in {maxsteps} steps; checkpoint retained")
    return np.asarray(m2.atom_coords(unit="Angstrom"))


# Ground states that are not closed-shell singlets (2S): treated spin-unrestricted. O2 is a triplet.
OPEN_SHELL = {"O=O": 2}


def complete_profile(path):
    """Legacy files without a convergence declaration are not certified cache hits."""
    try:
        meta = json.loads(path.read_text().splitlines()[0][len("# meta: "):])
        a = np.loadtxt(path)
        return (meta.get("geometry_converged") is True
                and meta.get("profile_revision") == profile_revision() and a.shape == (153, 2)
                and np.isfinite(a).all() and (a[:, 1] >= 0).all() and a[:, 1].sum() > 0)
    except (OSError, ValueError, IndexError):
        return False


def run_one(row, outdir):
    key = row["inchikey"]
    dest = Path(outdir) / f"{key}.sigma"
    if complete_profile(dest):
        return key, "exists", 0.0
    t = time.time()
    try:
        partial = Path(outdir) / f"{key}.partial.json"
        # Atom order comes from the same RDKit construction, without an xTB optimization.
        from rdkit import Chem
        mol = Chem.AddHs(Chem.MolFromSmiles(row["smiles"]))
        sym = [a.GetSymbol() for a in mol.GetAtoms()]
        resumed = False
        if partial.exists():
            p = json.loads(partial.read_text())
            trial = np.asarray(p["x"], dtype=float)
            if p["sym"] == sym and trial.shape == (len(sym), 3) and np.isfinite(trial).all():
                x0, resumed = trial, True
        if not resumed:
            sym, x0 = xtb_geometry(row["smiles"])
        spin = OPEN_SHELL.get(row["smiles"], 0)
        x = dft_geometry(sym, np.asarray(x0), partial=partial, spin=spin)
        seg, e = cosmo_segments(sym, x, spin=spin)
        out, meta = to_profiles(sym, x, seg)
        meta["E_scf_Eh"] = e
        meta["geometry_converged"] = True
        if os.environ.get("ZC_BERNY_NOISE_EH"):
            meta["geometry_protocol"] = "A-R2-noise-aware-trust-2e-7-Eh"
        meta["profile_revision"] = profile_revision()
        meta["source"] = "pyscf_cosmo_v2 BP86/def2-SVP conductor geometry; BP86/def2-TZVP conductor profile"
        meta["geometry"] = "BP86/def2-SVP C-PCM conductor (pyberny)" + (" [resumed from checkpoint]" if resumed else "")
        tmp = dest.with_suffix(".sigma.tmp")
        write_sigma(tmp, out, meta, key)
        os.replace(tmp, dest)
        with open(Path(outdir) / f"{key}.xyz.json", "w") as f:
            json.dump({"sym": sym, "x": np.round(x, 5).tolist()}, f)
        partial.unlink(missing_ok=True)
        Path(str(partial) + ".bstate").unlink(missing_ok=True)
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
    if not (1 <= a.nchunks <= 20 and 0 <= a.chunk < a.nchunks):
        ap.error("require 1 <= nchunks <= 20 and 0 <= chunk < nchunks")
    Path(a.outdir).mkdir(parents=True, exist_ok=True)
    d = pd.read_csv(a.csv)
    if a.keys:
        d = d[d.inchikey.isin(a.keys.split(","))]
    d = d.sort_values(["heavy_atoms", "inchikey"], ascending=[False, True]).reset_index(drop=True)
    d = d.iloc[a.chunk::a.nchunks]  # round-robin so chunks are balanced by size
    failed = False
    for r in d.to_dict("records"):
        k, st, dt = run_one(r, a.outdir)
        print(k, st, f"{dt:.0f}s", flush=True)
        failed |= st.startswith("fail:")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
