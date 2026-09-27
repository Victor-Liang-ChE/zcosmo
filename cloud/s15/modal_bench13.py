import modal, pathlib
here = pathlib.Path(__file__).parent
app = modal.App("zc-bench13")
image = (modal.Image.debian_slim(python_version="3.11")
         .pip_install("torch", "mace-torch[cueq]", "cuequivariance-ops-torch-cu13", "nvidia-cuda-nvrtc", "matscipy", "ase", "numpy")
         .add_local_file(str(here / "bench13_core.py"), "/root/bench13_core.py")
         .add_local_file(str(here / "bench6_core.py"), "/root/bench6_core.py")
         .add_local_file(str(here / "multi_mace.py"), "/root/multi_mace.py"))
vol = modal.Volume.from_name("zc-liquids", create_if_missing=True)

@app.function(gpu="L4", image=image, timeout=4 * 3600, volumes={"/vol": vol})
def bench():
    import subprocess, sys, shutil
    with open("/vol/bench13.log", "w") as f:     # streamed to the Volume as it runs (survives a broken log stream)
        p = subprocess.Popen([sys.executable, "-u", "/root/bench13_core.py"], env=dict(__import__("os").environ, ZC_SOLUTE="methanol", ZC_PROD_STEPS="40000"), cwd="/root", stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, text=True)
        keep = []
        for line in p.stdout:
            if line[:3] in ("A2 ", "D2 ") or "failed" in line or "Error" in line:
                keep.append(line.rstrip()); f.write(line); f.flush(); vol.commit()
        p.wait()
    try: shutil.copy("/tmp/d2_methanol.npz", "/vol/bench13_d2_methanol.npz"); vol.commit()
    except Exception: pass
    return "\n".join(keep)

@app.local_entrypoint()
def main():
    print(bench.remote())
