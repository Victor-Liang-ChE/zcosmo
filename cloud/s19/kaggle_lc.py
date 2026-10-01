# Kaggle CPU kernel: finish ONE open v2 long-chain profile with the registered code, resuming from the committed Berny checkpoint
# (cloud/s19/seeds, refreshed 2026-09-30 from the 4070). ZC_BERNY_STATE=1 keeps the pyberny optimiser state across passes (registered A-class, accepted 2026-09-30). Repeats 100-step passes until the profile is written or ~10 h have passed.
import glob, os, shutil, subprocess, sys, time
KEY = "__KEY__"
T0 = time.time()
sh = lambda c: subprocess.run(c, shell=True, check=False)
sh(f"{sys.executable} -m pip install -q pyscf==2.14.0 pyberny rdkit tblite ase pandas scipy matplotlib")
sh("git clone -q --depth 1 https://github.com/Victor-Liang-ChE/zcosmo /kaggle/working/zcosmo")
OUT = "/kaggle/working/out"; os.makedirs(OUT, exist_ok=True)
for f in glob.glob(f"/kaggle/working/zcosmo/cloud/s19/seeds/{KEY}.partial.json*"): shutil.copy(f, OUT)
print("seeded:", os.listdir(OUT), "cpus", os.cpu_count(), flush=True)
env = dict(os.environ, PYTHONPATH="src", ZC_BERNY_STATE="1", ZC_MAXSTEPS="300", OMP_NUM_THREADS=str(os.cpu_count()), QC_MEM_MB="20000", MPLBACKEND="Agg")
n = 0
while time.time() - T0 < 10 * 3600 and not os.path.exists(f"{OUT}/{KEY}.sigma"):
    n += 1; t = time.time()
    subprocess.run([sys.executable, "-m", "zcosmo.pyscf_cosmo_v2", OUT, "data/benchmark/compounds.csv", "--keys", KEY],
                   cwd="/kaggle/working/zcosmo", env=env)
    print(f"pass {n} took {(time.time()-t)/3600:.2f} h, sigma exists: {os.path.exists(f'{OUT}/{KEY}.sigma')}", flush=True)
sh("rm -rf /kaggle/working/zcosmo")
print("done", os.listdir(OUT), flush=True)
