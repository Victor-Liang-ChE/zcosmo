"""P9 fixed-geometry E check (same tolerances as P1): dE < 1e-8 Eh, max dG < 1e-6 Eh/Bohr, max dq < 1e-8 e,
P1 path (CachedPCM) vs P9 (CachedPCM3c), SVP (grid 2, Lebedev 17, conv 1e-8) and TZVP (grid 3, Lebedev 29, conv 1e-9),
water, O2 (UKS triplet), 1-octanol (xTB geometry). Also exercises the partial-cache path (ZC_PCM3C_MB tiny)."""
import os, json, time, sys, numpy as np
from pyscf import gto, dft
from pyscf.data import elements
from zcosmo.pyscf_cosmo import RADII, BOHR, xtb_geometry
from zcosmo.pcm_lu import cache_pcm, cache_pcm3c
oct_sym, oct_x = xtb_geometry("CCCCCCCCO")
mols = [("water", "O 0 0 0; H 0 .76 .59; H 0 -.76 .59", 0), ("oxygen", "O 0 0 0; O 0 0 1.21", 2),
        ("1-octanol", [(s, tuple(p)) for s, p in zip(oct_sym, oct_x)], 0)]
rows = []
for label, atoms, spin in mols:
    for basis, level, leb, tol in (("def2-svp", 2, 17, 1e-8), ("def2-tzvp", 3, 29, 1e-9)):
        if label == "1-octanol" and basis == "def2-tzvp" and os.environ.get("P9_SKIP_OCT_TZVP"): continue
        outs = []
        for arm in ("P1", "P9", "P9-partial"):
            if arm == "P9-partial": os.environ["ZC_PCM3C_MB"] = "20"
            mol = gto.M(atom=atoms, unit="Angstrom", basis=basis, spin=spin, verbose=0, max_memory=int(os.environ.get("QC_MEM_MB", "8000")))
            mf = (dft.UKS(mol) if spin else dft.RKS(mol)).density_fit().PCM()
            mf.xc = "b88,p86"; mf.grids.level = level; mf.conv_tol = tol
            s = mf.with_solvent; s.method = "C-PCM"; s.eps = 1e9; s.lebedev_order = leb
            tb = np.zeros(120)
            for el, r in RADII.items(): tb[elements.charge(el)] = r / BOHR
            s.radii_table = tb
            mf = cache_pcm(mf) if arm == "P1" else cache_pcm3c(mf)
            t = time.perf_counter(); e = mf.kernel(); assert mf.converged
            g = mf.nuc_grad_method().kernel(); dt = time.perf_counter() - t
            outs.append((e, np.asarray(g), np.asarray(mf.with_solvent._intermediates["q"]), dt))
            os.environ.pop("ZC_PCM3C_MB", None)
        for i, arm in ((1, "P9"), (2, "P9-partial")):
            de = abs(outs[i][0] - outs[0][0]); dg = float(abs(outs[i][1] - outs[0][1]).max()); dq = float(abs(outs[i][2] - outs[0][2]).max())
            ok = de < 1e-8 and dg < 1e-6 and dq < 1e-8
            rows.append(dict(molecule=label, basis=basis, arm=arm, dE=de, dG=dg, dq=dq, P1_s=outs[0][3], cand_s=outs[i][3], ok=ok))
            print(json.dumps(rows[-1]), flush=True)
json.dump(rows, open(sys.argv[1] if len(sys.argv) > 1 else "p9_fixed.json", "w"), indent=1)
print("ALL PASS" if all(r["ok"] for r in rows) else "FAIL")
