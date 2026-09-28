"""Measured-first profile of the registered QC path (Astra round-2 question 1). For one molecule: GFN2-xTB start,
then 3 Berny cycles of BP86/def2-SVP C-PCM (registered settings, pcm_lu cache as in main) under cProfile, with pyscf's
own timers (verbose 4). Reports the split of wall time into SCF (J/K build, XC), gradient terms, PCM and Berny.
Usage: qc_cycle_profile.py SMILES OUTPREFIX"""
import cProfile, pstats, io, sys, time, os
import numpy as np
from zcosmo.pyscf_cosmo import xtb_geometry
from zcosmo import pyscf_cosmo_v2 as v2
smi, pre = sys.argv[1], sys.argv[2]
sym, x0 = xtb_geometry(smi)
pr = cProfile.Profile(); t = time.time(); pr.enable()
try:
    v2.dft_geometry(sym, np.asarray(x0), maxsteps=3)
except RuntimeError as e:
    print("expected stop:", e)
pr.disable(); wall = time.time() - t
s = io.StringIO(); st = pstats.Stats(pr, stream=s); st.sort_stats("cumulative").print_stats(60)
open(pre + "_cumulative.txt", "w").write(s.getvalue())
s = io.StringIO(); st = pstats.Stats(pr, stream=s); st.sort_stats("tottime").print_stats(40)
open(pre + "_tottime.txt", "w").write(s.getvalue())
st.dump_stats(pre + ".prof")
# bucket the cumulative time of well-known pyscf entry points
buckets = {"get_jk (DF J/K)": "get_jk", "nr_rks / nr_vxc (XC)": "nr_rks", "XC gradient": "get_vxc",
           "DF gradient (get_jk grad)": "df_rhf_grad", "PCM (energy)": "pcm", "Berny": "berny"}
rows = []
for (fn, line, name), (cc, nc, tt, ct, callers) in st.stats.items():
    rows.append((ct, tt, f"{os.path.basename(fn)}:{name}"))
rows.sort(reverse=True)
with open(pre + "_summary.txt", "w") as f:
    f.write(f"molecule {smi} natoms {len(sym)} threads {os.environ.get('OMP_NUM_THREADS')} wall {wall:.1f}s (3 Berny cycles)\n")
    for ct, tt, n in rows[:45]:
        f.write(f"{ct:9.1f} cum {tt:9.1f} self  {n}\n")
print(open(pre + "_summary.txt").read())
