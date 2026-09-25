"""First-principles hydrogen-bond reference energies for the Z0 model.

For each reference dimer (donor X-H ... acceptor Y):
  1. build 3D monomers with RDKit, place the donor H 1.95 A from the acceptor
     atom along its lone-pair direction;
  2. relax monomers and dimer with GFN2-xTB (tblite + ASE);
  3. counterpoise-corrected B3LYP-D4/def2-TZVP binding energy with PySCF
     (density fitting), D4 from dftd4.
No experimental numbers enter anywhere.

Usage: python -m zcosmo.qc_hbond [--method b3lyp] [--basis def2-tzvp]
Writes results/qc/hbond_dimers.csv
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "qc"
HARTREE_KCAL = 627.509474
BOHR = 0.52917721067

# (label, donor SMILES with :1 on donor heavy atom, donor InChIKey,
#  acceptor SMILES with :1 on acceptor atom, acceptor InChIKey,
#  donor profile, acceptor profile)
DIMERS = [
    ("water->water", "[OH2:1]", "XLYOFNOQVPJJNP-UHFFFAOYSA-N", "[OH2:1]", "XLYOFNOQVPJJNP-UHFFFAOYSA-N", "OH", "OH"),
    ("methanol->methanol", "C[OH:1]", "OKKJLVBELUTLKV-UHFFFAOYSA-N", "C[OH:1]", "OKKJLVBELUTLKV-UHFFFAOYSA-N", "OH", "OH"),
    ("water->methanol", "[OH2:1]", "XLYOFNOQVPJJNP-UHFFFAOYSA-N", "C[OH:1]", "OKKJLVBELUTLKV-UHFFFAOYSA-N", "OH", "OH"),
    ("methanol->water", "C[OH:1]", "OKKJLVBELUTLKV-UHFFFAOYSA-N", "[OH2:1]", "XLYOFNOQVPJJNP-UHFFFAOYSA-N", "OH", "OH"),
    ("ethanol->ethanol", "CC[OH:1]", "LFQSCWFLJHTTHZ-UHFFFAOYSA-N", "CC[OH:1]", "LFQSCWFLJHTTHZ-UHFFFAOYSA-N", "OH", "OH"),
    ("water->acetone", "[OH2:1]", "XLYOFNOQVPJJNP-UHFFFAOYSA-N", "CC(=[O:1])C", "CSCPPACGZOOCGX-UHFFFAOYSA-N", "OH", "OT"),
    ("water->dimethyl ether", "[OH2:1]", "XLYOFNOQVPJJNP-UHFFFAOYSA-N", "C[O:1]C", "LCGLNKUTAGEVQW-UHFFFAOYSA-N", "OH", "OT"),
    ("water->acetonitrile", "[OH2:1]", "XLYOFNOQVPJJNP-UHFFFAOYSA-N", "CC#[N:1]", "WEVYAHXRMPXWCK-UHFFFAOYSA-N", "OH", "OT"),
    ("water->trimethylamine", "[OH2:1]", "XLYOFNOQVPJJNP-UHFFFAOYSA-N", "C[N:1](C)C", "GETQZCLCWQTVFV-UHFFFAOYSA-N", "OH", "OT"),
    ("methanol->pyridine", "C[OH:1]", "OKKJLVBELUTLKV-UHFFFAOYSA-N", "c1cc[n:1]cc1", "JUJWROOIHBZHMG-UHFFFAOYSA-N", "OH", "OT"),
    ("water->THF", "[OH2:1]", "XLYOFNOQVPJJNP-UHFFFAOYSA-N", "C1CC[O:1]C1", "WYURNTSHIVDZCO-UHFFFAOYSA-N", "OH", "OT"),
    ("methylamine->water", "C[NH2:1]", "BAVYZALUXZFZLV-UHFFFAOYSA-N", "[OH2:1]", "XLYOFNOQVPJJNP-UHFFFAOYSA-N", "OT", "OH"),
    ("methylamine->methylamine", "C[NH2:1]", "BAVYZALUXZFZLV-UHFFFAOYSA-N", "C[NH2:1]", "BAVYZALUXZFZLV-UHFFFAOYSA-N", "OT", "OT"),
    ("dimethylamine->dimethylamine", "C[NH:1]C", "ROSDSFDQCJNGOL-UHFFFAOYSA-N", "C[NH:1]C", "ROSDSFDQCJNGOL-UHFFFAOYSA-N", "OT", "OT"),
    ("NMA->NMA", "CC(=O)[NH:1]C", "OHLUUHNLEMFGTQ-UHFFFAOYSA-N", "CC(=[O:1])NC", "OHLUUHNLEMFGTQ-UHFFFAOYSA-N", "OT", "OT"),
    ("formamide->acetone", "O=C[NH2:1]", "ZHNUHDYFZUAESO-UHFFFAOYSA-N", "CC(=[O:1])C", "CSCPPACGZOOCGX-UHFFFAOYSA-N", "OT", "OT"),
    ("methylamine->acetonitrile", "C[NH2:1]", "BAVYZALUXZFZLV-UHFFFAOYSA-N", "CC#[N:1]", "WEVYAHXRMPXWCK-UHFFFAOYSA-N", "OT", "OT"),
]


def _mol3d(smiles):
    m = Chem.AddHs(Chem.MolFromSmiles(smiles))
    AllChem.EmbedMolecule(m, randomSeed=42)
    AllChem.MMFFOptimizeMolecule(m)
    return m


def _mapped(m):
    return next(a.GetIdx() for a in m.GetAtoms() if a.GetAtomMapNum() == 1)


def _rot(a, b):
    """Rotation matrix taking unit vector a to unit vector b."""
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)
    v = np.cross(a, b)
    c = float(a @ b)
    if np.linalg.norm(v) < 1e-8:
        return np.eye(3) if c > 0 else -np.eye(3) + 2 * np.outer(np.cross(a, [1, 0, 0]) if abs(a[0]) < .9 else np.cross(a, [0, 1, 0]), np.cross(a, [1, 0, 0]) if abs(a[0]) < .9 else np.cross(a, [0, 1, 0])) / np.linalg.norm(np.cross(a, [1, 0, 0]) if abs(a[0]) < .9 else np.cross(a, [0, 1, 0]))**2
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + vx + vx @ vx * (1 / (1 + c))


def build_dimer(dsmi, asmi):
    D, A = _mol3d(dsmi), _mol3d(asmi)
    xd = D.GetConformer().GetPositions()
    xa = A.GetConformer().GetPositions()
    ia = _mapped(A)
    idh = _mapped(D)
    h = next(n.GetIdx() for n in D.GetAtomWithIdx(idh).GetNeighbors() if n.GetSymbol() == "H")
    # acceptor lone-pair direction: away from the mean of its neighbours
    nb = [n.GetIdx() for n in A.GetAtomWithIdx(ia).GetNeighbors()]
    lp = xa[ia] - xa[nb].mean(axis=0) if nb else np.array([1.0, 0, 0])
    lp /= np.linalg.norm(lp)
    # align donor X-H bond with lp, H pointing back at acceptor
    xh = xd[h] - xd[idh]
    Rm = _rot(xh, -lp)
    xd2 = (xd - xd[h]) @ Rm.T
    xd2 = xd2 + xa[ia] + 1.95 * lp
    sym = [a.GetSymbol() for a in D.GetAtoms()] + [a.GetSymbol() for a in A.GetAtoms()]
    return sym, np.vstack([xd2, xa]), D.GetNumAtoms(), (h, D.GetNumAtoms() + ia)


def xtb_relax(sym, x, fmax=0.02, steps=400):
    from ase import Atoms
    from ase.optimize import BFGS
    from tblite.ase import TBLite
    at = Atoms(sym, positions=x)
    at.calc = TBLite(method="GFN2-xTB", verbosity=0)
    BFGS(at, logfile=None).run(fmax=fmax, steps=steps)
    return at.get_positions(), at.get_potential_energy() / 27.211386245988


def dft_energy(sym, x, ghost=(), method="b3lyp", basis="def2-tzvp"):
    from pyscf import gto, dft
    atoms = []
    for i, (s, p) in enumerate(zip(sym, x)):
        atoms.append((("ghost-" + s) if i in ghost else s, tuple(p)))
    mol = gto.M(atom=atoms, basis=basis, unit="Angstrom", verbose=0)
    mf = dft.RKS(mol).density_fit()
    mf.xc = method
    mf.conv_tol = 1e-9
    mf.grids.level = 3
    e = mf.kernel()
    return e


def d4_energy(sym, x, method="b3lyp"):
    from dftd4.interface import DampingParam, DispersionModel
    nums = np.array([Chem.GetPeriodicTable().GetAtomicNumber(s) for s in sym])
    model = DispersionModel(nums, np.asarray(x) / BOHR)
    return model.get_dispersion(DampingParam(method=method), grad=False)["energy"]


def run_one(label, dsmi, asmi, method, basis):
    sym, x0, nd, (ih, ia) = build_dimer(dsmi, asmi)
    x, _ = xtb_relax(sym, x0)
    dHA = float(np.linalg.norm(x[ih] - x[ia]))
    n = len(sym)
    idx_d = list(range(nd))
    idx_a = list(range(nd, n))
    # relaxed monomers (deformation energy included)
    xd, _ = xtb_relax(sym[:nd], x[:nd])
    xa, _ = xtb_relax(sym[nd:], x[nd:])
    e_ab = dft_energy(sym, x, method=method, basis=basis)
    e_a_cp = dft_energy(sym, x, ghost=set(idx_a), method=method, basis=basis)   # donor in dimer basis
    e_b_cp = dft_energy(sym, x, ghost=set(idx_d), method=method, basis=basis)   # acceptor in dimer basis
    e_a_d = dft_energy(sym[:nd], x[:nd], method=method, basis=basis)
    e_b_d = dft_energy(sym[nd:], x[nd:], method=method, basis=basis)
    e_a_r = dft_energy(sym[:nd], xd, method=method, basis=basis)
    e_b_r = dft_energy(sym[nd:], xa, method=method, basis=basis)
    disp = d4_energy(sym, x, method) - d4_energy(sym[:nd], xd, method) - d4_energy(sym[nd:], xa, method)
    e_int_cp = (e_ab - e_a_cp - e_b_cp)
    e_def = (e_a_d - e_a_r) + (e_b_d - e_b_r)
    e_bind = (e_int_cp + e_def) * HARTREE_KCAL + disp * HARTREE_KCAL
    return dict(label=label, dHA_A=dHA, E_int_cp_kcal=e_int_cp * HARTREE_KCAL, E_def_kcal=e_def * HARTREE_KCAL,
                E_disp_kcal=disp * HARTREE_KCAL, E_bind_kcal=e_bind, n_atoms=n,
                xyz=json.dumps({"sym": sym, "x": np.round(x, 4).tolist()}))


def main():
    import pandas as pd
    ap = argparse.ArgumentParser()
    ap.add_argument("--method", default="b3lyp")
    ap.add_argument("--basis", default="def2-tzvp")
    ap.add_argument("--only", default=None)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    f = OUT / f"hbond_dimers_{a.method}_{a.basis}.csv"
    done = set(pd.read_csv(f).label) if f.exists() else set()
    for row in DIMERS:
        label = row[0]
        if label in done or (a.only and a.only != label):
            continue
        t = time.time()
        r = run_one(label, row[1], row[3], a.method, a.basis)
        r.update(donor_key=row[2], acceptor_key=row[4], donor_prof=row[5], acceptor_prof=row[6],
                 method=a.method, basis=a.basis, seconds=round(time.time() - t))
        pd.DataFrame([r]).to_csv(f, mode="a", header=not f.exists(), index=False)
        print(f"{label}: E_bind={r['E_bind_kcal']:.2f} kcal/mol, H..A={r['dHA_A']:.2f} A, {r['seconds']}s", flush=True)


if __name__ == "__main__":
    main()
