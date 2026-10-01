"""Registered rule S1 (PREREGISTRATION.md, entry of 2026-10-01): accept a long-chain checkpoint whose Berny test is perpetually blocked by 'minimization on sphere'
although its gradient criteria are met.  Usage: stall_accept.py KEY NEW_PARTIAL OLD_PARTIAL OUTDIR
Computes (a) the Cartesian gradient at the NEW checkpoint with the registered settings, (b) displacement and cycle count between OLD and NEW checkpoints,
and, only if (a) and (b) hold, (c) the registered TZVP profile at both checkpoints (NEW -> OUTDIR/KEY.sigma, OLD -> OUTDIR_old/KEY.sigma) and max |d p(sigma)|."""
import json, os, sys, time
import numpy as np
from pyscf import gto, dft
from pyscf.data import elements
from zcosmo.pyscf_cosmo_v2 import RADII
from zcosmo.pyscf_cosmo import cosmo_segments, to_profiles, write_sigma
BOHR = 0.529177210903
key, newp, oldp, outdir = sys.argv[1:5]
new, old = json.load(open(newp)), json.load(open(oldp))
sym, xn, xo = new["sym"], np.asarray(new["x"], dtype=float), np.asarray(old["x"], dtype=float)
disp = float(np.abs(xn - xo).max()); cyc = int(new.get("cycle", -1))
t0 = time.time()
mol = gto.M(atom=[(s, tuple(q)) for s, q in zip(sym, xn)], basis="def2-svp", unit="Angstrom", verbose=0, max_memory=int(os.environ.get("QC_MEM_MB", "6000")))
mf = dft.RKS(mol).density_fit().PCM(); mf.xc = "b88,p86"; mf.grids.level = 2; mf.conv_tol = 1e-8
s = mf.with_solvent; s.method = "C-PCM"; s.eps = 1e9; s.lebedev_order = 17
tab = np.zeros(120)
for el, r in RADII.items(): tab[elements.charge(el)] = r / BOHR
s.radii_table = tab
e = mf.kernel(); g = mf.nuc_grad_method().kernel()
gmax, grms = float(np.abs(g).max()), float(np.sqrt((g ** 2).mean()))
a = gmax < 4.5e-4 and grms < 1.5e-4
b = cyc >= 90 and disp <= 0.005
rep = dict(key=key, atoms=len(sym), cycle_since_resume=cyc, displacement_A=disp, E_SVP=float(e), grad_max=gmax, grad_rms=grms, cond_a_gradient=bool(a), cond_b_stationary=bool(b), seconds_grad=round(time.time() - t0))
print(json.dumps(rep), flush=True)
if a and b:
    for tag, x, d in (("new", xn, outdir), ("old", xo, outdir + "_old")):
        t1 = time.time(); seg, e2 = cosmo_segments(sym, x); out, meta = to_profiles(sym, x, seg)
        meta.update(E_scf_Eh=e2, geometry_converged="S1", source="stalled checkpoint accepted by registered rule S1 (%s checkpoint)" % tag,
                    geometry="BP86/def2-SVP C-PCM conductor (pyberny) [stalled checkpoint, registered rule S1, %s]" % tag)
        os.makedirs(d, exist_ok=True); write_sigma(f"{d}/{key}.sigma", out, meta, key)
        if tag == "new": pn = out
        else: po = out
        print(key, tag, "profile written", round(time.time() - t1), "s", flush=True)
    dp = max(float(np.abs(np.asarray(getattr(pn, k)) - np.asarray(getattr(po, k))).max()) for k in ("psigmaA_nhb", "psigmaA_OH", "psigmaA_OT"))
    rep["max_dp_sigma_new_vs_old"] = dp; rep["peak_psigmaA"] = float(max(np.asarray(getattr(pn, k)).max() for k in ("psigmaA_nhb", "psigmaA_OH", "psigmaA_OT")))
    rep["cond_c_dp_below_1e-3"] = bool(dp < 1e-3)
    print("RESULT", json.dumps(rep), flush=True)
else:
    print("RESULT", json.dumps(rep), "-> S1 conditions (a) and (b) NOT met, no profile computed", flush=True)
