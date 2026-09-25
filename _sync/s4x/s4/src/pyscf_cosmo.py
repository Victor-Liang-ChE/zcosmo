"""Open-source COSMO sigma profiles: PySCF BP86/def2-TZVP C-PCM (conductor limit) on GFN2-xTB geometries,
averaged and split into NHB/OH/OT exactly as NIST to_sigma.py (Hsieh averaging) does for the UD set.

Usage: python -m zcosmo.pyscf_cosmo OUTDIR SMILES_CSV [--basis def2-tzvp] [--nproc N]
SMILES_CSV needs columns inchikey, smiles (optional: conf_id, xyz for pre-made conformer geometries).
Writes OUTDIR/<inchikey>[__<conf_id>].sigma in the UD sigma3 format plus a .json with energies.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.spatial

ROOT = Path(__file__).resolve().parents[2]
BOHR = 0.52917721067
# COSMO radii (A) used for the DMol3/VT-UD profiles (Klamt-optimized set)
RADII = {"H": 1.30, "C": 2.00, "N": 1.83, "O": 1.72, "F": 1.72, "S": 2.16, "Cl": 2.05, "Br": 2.16}


def xtb_geometry(smiles, seed=7):
    from rdkit import Chem
    from rdkit.Chem import AllChem
    from ase import Atoms
    from ase.optimize import BFGS
    from tblite.ase import TBLite
    m = Chem.AddHs(Chem.MolFromSmiles(smiles))
    if AllChem.EmbedMolecule(m, randomSeed=seed) != 0:
        AllChem.EmbedMolecule(m, randomSeed=seed, useRandomCoords=True)
    try:
        AllChem.MMFFOptimizeMolecule(m)
    except Exception:
        pass
    sym = [a.GetSymbol() for a in m.GetAtoms()]
    at = Atoms(sym, positions=m.GetConformer().GetPositions())
    at.calc = TBLite(method="GFN2-xTB", verbosity=0)
    BFGS(at, logfile=None).run(fmax=0.01, steps=500)
    return sym, at.get_positions()


def cosmo_segments(sym, xyz_A, basis="def2-tzvp", lebedev=29):
    """Return segment table (x,y,z in bohr, charge, area A^2, atom index) and SCF energy."""
    from pyscf import gto, dft
    mol = gto.M(atom=[(s, tuple(p)) for s, p in zip(sym, xyz_A)], basis=basis, unit="Angstrom", verbose=0,
                max_memory=int(os.environ.get("QC_MEM_MB", "4000")))
    mf = dft.RKS(mol).density_fit().PCM()
    mf.xc = "b88,p86"
    mf.grids.level = 3
    mf.conv_tol = 1e-9
    s = mf.with_solvent
    s.method = "C-PCM"
    s.eps = 1e9  # conductor limit
    s.lebedev_order = lebedev
    s.vdw_scale = 1.0
    table = np.zeros(120)
    from pyscf.data import elements
    for el, r in RADII.items():
        table[elements.charge(el)] = r / BOHR
    s.radii_table = table
    e = mf.kernel()
    if not mf.converged:
        raise RuntimeError("SCF not converged")
    surf = s.surface
    q = np.asarray(s._intermediates["q"]).ravel()
    xyz = np.asarray(surf["grid_coords"])
    area_b2 = np.asarray(surf["area"])
    atom = np.concatenate([np.full(n, i) for i, n in enumerate(np.diff(surf["gslice_by_atom"], axis=1).ravel())]) \
        if "gslice_by_atom" in surf else np.asarray(surf["atom_idx"])
    keep = area_b2 > 1e-8
    return dict(xyz=xyz[keep], q=q[keep], area=area_b2[keep] * BOHR ** 2, atom=atom[keep]), e


def cavity_volume(seg, atoms_b):
    """Volume (A^3) by the divergence theorem with outward normals from the owning atom centre."""
    r = seg["xyz"] * BOHR
    c = atoms_b[seg["atom"]] * BOHR
    n = r - c
    n /= np.linalg.norm(n, axis=1)[:, None]
    return float(np.sum(np.einsum("ij,ij->i", r, n) * seg["area"]) / 3.0)


def to_profiles(sym, xyz_A, seg):
    """Reuse the NIST parser logic on in-memory data (Hsieh averaging, 3 profiles)."""
    sys.path.insert(0, str(ROOT / "data/raw/nist"))
    import to_sigma as ts
    p = ts.Dmol3COSMOParser.__new__(ts.Dmol3COSMOParser)
    n = len(seg["q"])
    p.df = pd.DataFrame({"n": np.arange(1, n + 1), "atom": seg["atom"] + 1,
                         "x / a.u.": seg["xyz"][:, 0], "y / a.u.": seg["xyz"][:, 1], "z / a.u.": seg["xyz"][:, 2],
                         "charge / e": seg["q"], "area / A^2": seg["area"]})
    p.df_atom = pd.DataFrame({"atom": sym, "x / A": xyz_A[:, 0], "y / A": xyz_A[:, 1], "z / A": xyz_A[:, 2]})
    p.area_A2 = float(seg["area"].sum())
    p.volume_A3 = cavity_volume(seg, xyz_A / BOHR)
    p.num_profiles = 3
    p.averaging = "Hsieh"
    for f in "xyz":
        p.df[f + " / A"] = p.df[f + " / a.u."] * BOHR
    p.df["rn / A"] = (p.df["area / A^2"] / np.pi) ** 0.5
    p.df["rn^2 / A^2"] = p.df["rn / A"] ** 2
    p.sigma = np.array(p.df["charge / e"] / p.df["area / A^2"])
    p.rn2 = np.array(p.df["rn^2 / A^2"])
    XA = np.c_[p.df["x / A"], p.df["y / A"], p.df["z / A"]]
    p.dist_mat_squared = scipy.spatial.distance.cdist(XA, XA) ** 2
    XA = np.c_[p.df_atom["x / A"], p.df_atom["y / A"], p.df_atom["z / A"]]
    p.dist_mat_atom = scipy.spatial.distance.cdist(XA, XA)
    p.is_water = sym.count("H") == 2 and sym.count("O") == 1 and len(sym) == 3
    p.disp = p.get_dispersive_values()
    p.df_atom["hb_class"] = p.get_HB_classes_per_atom()
    p.df_atom["Nbonds"] = p.disp.Nbonds
    p.sigma_averaged = p.average_sigmas(p.sigma)
    p.sigma_nhb, p.sigma_OH, p.sigma_OT = p.split_profiles(p.sigma_averaged, 3)
    out = p.get_outputs()
    meta = p.get_meta()
    meta["disp. flag"] = "H2O" if p.is_water else p.disp.dispersion_flag
    meta["disp. e/kB [K]"] = None if p.disp.dispersive_molecule is None or np.isnan(p.disp.dispersive_molecule) \
        else float(p.disp.dispersive_molecule)
    return out, meta


def write_sigma(path, out, meta, key):
    meta = dict(meta)
    meta["standard_INCHIKEY"] = key
    meta["source"] = "pyscf_cosmo BP86/def2-TZVP C-PCM conductor, GFN2-xTB geometry"
    with open(path, "w") as f:
        f.write("# meta: " + json.dumps(meta) + "\n")
        f.write("# Rows are given as: sigma [e/A^2] followed by a space, then psigmaA [A^2]\n")
        f.write("# In the case of three sigma profiles, the order is NHB, OH, then OT\n")
        for arr in (out.psigmaA_nhb, out.psigmaA_OH, out.psigmaA_OT):
            for s, pA in zip(out.sigmas, arr):
                f.write(f"{s:0.3f} {pA:0.14e}\n")


def run_one(row, outdir, basis):
    key = row["inchikey"]
    tag = key + (f"__{row['conf_id']}" if "conf_id" in row and pd.notna(row.get("conf_id")) else "")
    dest = Path(outdir) / f"{tag}.sigma"
    if dest.exists():
        return tag, "exists"
    try:
        if "xyz" in row and isinstance(row.get("xyz"), str):
            g = json.loads(row["xyz"])
            sym, xyz = g["sym"], np.array(g["x"])
        else:
            sym, xyz = xtb_geometry(row["smiles"])
        seg, e = cosmo_segments(sym, np.asarray(xyz), basis=basis)
        out, meta = to_profiles(sym, np.asarray(xyz), seg)
        meta["E_scf_Eh"] = e
        write_sigma(dest, out, meta, key)
        return tag, "ok"
    except Exception as ex:  # keep going
        return tag, f"fail: {ex!r}"[:300]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("outdir")
    ap.add_argument("csv")
    ap.add_argument("--basis", default="def2-tzvp")
    ap.add_argument("--nproc", type=int, default=1)
    a = ap.parse_args()
    Path(a.outdir).mkdir(parents=True, exist_ok=True)
    rows = pd.read_csv(a.csv).to_dict("records")
    if a.nproc > 1:
        import multiprocessing as mp
        with mp.get_context("spawn").Pool(a.nproc) as p:
            for tag, st in p.starmap(run_one, [(r, a.outdir, a.basis) for r in rows]):
                print(tag, st, flush=True)
    else:
        for r in rows:
            print(*run_one(r, a.outdir, a.basis), flush=True)


if __name__ == "__main__":
    main()
