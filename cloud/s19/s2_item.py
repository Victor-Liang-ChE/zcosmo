"""Registered rule S2 (PREREGISTRATION.md, entry of 2026-10-04): one computation per call, so the 13 items of a chain run as parallel jobs.
Usage: s2_item.py KEY ITEM NEW_PARTIAL OLD_PARTIAL OUTDIR
ITEM: grad (BP86/def2-SVP C-PCM Cartesian gradient at NEW, registered settings) | new | old | xtb | pert | r0..r7 (registered TZVP profile at that geometry).
Rotations: scipy Rotation.random(8, random_state=20261004), applied about the centroid of the NEW geometry.
pert: NEW geometry + isotropic Gaussian displacement (numpy default_rng(20261004)) scaled to a maximum atomic displacement of exactly 0.02 Angstrom (report only).
xtb: the runner's own xTB start geometry for this SMILES (RDKit seed 7, GFN2-xTB), the same construction the optimisation started from."""
import csv, json, os, sys, time
import numpy as np
key, item, newp, oldp, outdir = sys.argv[1:6]
os.makedirs(outdir, exist_ok=True)
new, old = json.load(open(newp)), json.load(open(oldp))
sym, xn, xo = new["sym"], np.asarray(new["x"], float), np.asarray(old["x"], float)
assert old["sym"] == sym and xn.shape == xo.shape
t0 = time.time()
rep = dict(key=key, item=item, atoms=len(sym))
if item == "grad":
    from pyscf import gto, dft
    from pyscf.data import elements
    from zcosmo.pyscf_cosmo_v2 import RADII
    BOHR = 0.529177210903
    mol = gto.M(atom=[(s, tuple(q)) for s, q in zip(sym, xn)], basis="def2-svp", unit="Angstrom", verbose=0, max_memory=int(os.environ.get("QC_MEM_MB", "6000")))
    mf = dft.RKS(mol).density_fit().PCM(); mf.xc = "b88,p86"; mf.grids.level = 2; mf.conv_tol = 1e-8
    s = mf.with_solvent; s.method = "C-PCM"; s.eps = 1e9; s.lebedev_order = 17
    tab = np.zeros(120)
    for el, r in RADII.items(): tab[elements.charge(el)] = r / BOHR
    s.radii_table = tab
    e = mf.kernel(); g = mf.nuc_grad_method().kernel()
    rep.update(E_SVP=float(e), grad_max=float(np.abs(g).max()), grad_rms=float(np.sqrt((g ** 2).mean())),
               displacement_new_vs_old_A=float(np.abs(xn - xo).max()))
else:
    from zcosmo.pyscf_cosmo import cosmo_segments, to_profiles, write_sigma, xtb_geometry
    if item == "new": x = xn
    elif item == "old": x = xo
    elif item == "xtb":
        smi = {r["inchikey"]: r["smiles"] for r in csv.DictReader(open("data/benchmark/compounds.csv"))}[key]
        sx, x = xtb_geometry(smi); x = np.asarray(x, float)
        assert list(sx) == list(sym), "atom order of the xTB geometry differs from the checkpoint"
        rep["displacement_xtb_vs_new_A"] = float(np.abs(x - xn).max())
    elif item == "pert":
        d = np.random.default_rng(20261004).normal(size=xn.shape); d *= 0.02 / np.abs(d).max(); x = xn + d
    elif item.startswith("r") and item[1:].isdigit() and 0 <= int(item[1:]) < 8:
        from scipy.spatial.transform import Rotation
        R = Rotation.random(8, random_state=20261004)[int(item[1:])]
        c = xn.mean(0); x = R.apply(xn - c) + c
        rep["rotation_angle_rad"] = float(R.magnitude())
    else:
        raise SystemExit("unknown item " + item)
    seg, e2 = cosmo_segments(sym, x); out, meta = to_profiles(sym, x, seg)
    meta.update(E_scf_Eh=e2, geometry_converged="S2-candidate", source=f"rule S2 item {item}",
                geometry=f"BP86/def2-SVP C-PCM conductor (pyberny) [stalled checkpoint, rule S2, {item}]")
    write_sigma(f"{outdir}/{key}.{item}.sigma", out, meta, key)
rep["seconds"] = round(time.time() - t0)
json.dump(rep, open(f"{outdir}/{key}.{item}.json", "w")); print("RESULT", json.dumps(rep), flush=True)
