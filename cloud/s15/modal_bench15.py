import modal, pathlib
here = pathlib.Path(__file__).parent
app = modal.App("zc-bench15")
image = (modal.Image.debian_slim(python_version="3.11")
         .pip_install("torch", "mace-torch[cueq]", "cuequivariance-ops-torch-cu13", "nvidia-cuda-nvrtc", "matscipy", "ase", "numpy")
         .add_local_file(str(here / "bench15_core.py"), "/root/bench15_core.py")
         .add_local_file(str(here / "bench6_core.py"), "/root/bench6_core.py")
         .add_local_file(str(here / "multi_mace.py"), "/root/multi_mace.py"))
vol = modal.Volume.from_name("zc-liquids", create_if_missing=True)
L2 = "0,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.65,0.7,0.75,0.8,0.85,0.9,1"
M1 = "0,0.025,0.05,0.075,0.1,0.15,0.2,0.35,0.5,0.65,0.8,0.9,1"

@app.function(gpu="L4", image=image, timeout=8 * 3600, volumes={"/vol": vol})
def run(solute, solvent, seed):
    import subprocess, sys, os, glob, shutil
    tag = f"{solute}_in_{solvent}_s{seed}"
    env = dict(os.environ, ZC_SOLUTE=solute, ZC_SOLVENT=solvent, ZC_SEED=str(seed), ZC_PROD_STEPS="60000", ZC_LAM2=L2, ZC_MU1=M1)
    keep = []
    with open(f"/vol/pilot_{tag}.log", "w") as f:
        p = subprocess.Popen([sys.executable, "-u", "/root/bench15_core.py"], env=env, cwd="/root",
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in p.stdout:
            if line[:3] == "D2 " or "failed" in line or "Error" in line:
                keep.append(line.rstrip()); f.write(line); f.flush(); vol.commit()
        p.wait()
    for fn in glob.glob("/tmp/d2_*.npz"): shutil.copy(fn, "/vol/pilot_" + os.path.basename(fn))
    vol.commit()
    return tag + "\n" + "\n".join(keep)

@app.local_entrypoint()
def main(which: str = "all", seed: int = 1):
    jobs = [("methanol", "water"), ("methanol", "methanol"), ("water", "water"), ("water", "methanol")]
    for r in run.starmap([(a, b, seed) for a, b in jobs]):
        print(r)
