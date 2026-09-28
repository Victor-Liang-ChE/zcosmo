"""CPU (registered pyscf 2.14 path) gradient audit of saved open-profile geometries. Diagnostic only.
Same mean-field settings as zcosmo.pyscf_cosmo_v2.dft_geometry. Reports max/rms Cartesian gradient vs pyberny's default
gradient thresholds (max 4.5e-4, rms 1.5e-4 Eh/Bohr). Usage: cpu_grad_audit.py GEOMDIR OUT.csv CHUNK NCHUNKS"""
import glob, json, os, sys, time, numpy as np
from pyscf import gto, dft
from pyscf.data import elements
from zcosmo.pyscf_cosmo import RADII, BOHR
d, out, chunk, n = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
files = sorted(glob.glob(os.path.join(d, "**", "*.xyz.json"), recursive=True), key=os.path.getsize)[chunk::n]
with open(out, "w") as f:
    f.write("set,key,natoms,gmax,grms,converged_grad,wall_s\n")
    for p in files:
        k, s = os.path.basename(p)[:-9], os.path.basename(os.path.dirname(p))
        g = json.load(open(p)); sym, x = g["sym"], np.array(g["x"])
        ne = sum(elements.charge(a) for a in sym); spin = 2 if sym == ["O", "O"] else ne % 2
        t = time.time()
        try:
            mol = gto.M(atom=[(a, tuple(v)) for a, v in zip(sym, x)], basis="def2-svp", unit="Angstrom", spin=spin,
                        verbose=0, max_memory=int(os.environ.get("QC_MEM_MB", "10000")))
            mf = (dft.UKS(mol) if spin else dft.RKS(mol)).density_fit().PCM()
            mf.xc = "b88,p86"; mf.grids.level = 2; mf.conv_tol = 1e-8
            so = mf.with_solvent; so.method = "C-PCM"; so.eps = 1e9; so.lebedev_order = 17
            tb = np.zeros(120)
            for el, r in RADII.items(): tb[elements.charge(el)] = r / BOHR
            so.radii_table = tb
            mf.kernel(); gr = mf.nuc_grad_method().kernel()
            gmax, grms = float(abs(gr).max()), float(np.sqrt((gr ** 2).mean()))
            f.write(f"{s},{k},{len(sym)},{gmax:.3e},{grms:.3e},{int(gmax < 4.5e-4 and grms < 1.5e-4)},{time.time()-t:.1f}\n")
        except Exception as ex:
            print(k, repr(ex)[:200], flush=True)
            f.write(f"{s},{k},{len(sym)},nan,nan,-1,{time.time()-t:.1f}\n")
        f.flush()
