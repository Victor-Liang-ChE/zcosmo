import modal, pathlib
here = pathlib.Path(__file__).parent
app = modal.App("zc-bench12")
image = (modal.Image.debian_slim(python_version="3.11")
         .pip_install("torch", "mace-torch[cueq]", "cuequivariance-ops-torch-cu13", "nvidia-cuda-nvrtc", "matscipy", "ase", "numpy")
         .add_local_file(str(here / "bench12_core.py"), "/root/bench12_core.py")
         .add_local_file(str(here / "bench6_core.py"), "/root/bench6_core.py")
         .add_local_file(str(here / "multi_mace.py"), "/root/multi_mace.py"))
vol = modal.Volume.from_name("zc-liquids", create_if_missing=True)

@app.function(gpu="L4", image=image, timeout=4 * 3600, volumes={"/vol": vol})
def bench():
    import subprocess, sys, shutil
    with open("/vol/bench12.log", "w") as f:     # streamed to the Volume as it runs (survives a broken log stream)
        p = subprocess.Popen([sys.executable, "-u", "/root/bench12_core.py"], cwd="/root", stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, text=True)
        keep = []
        for line in p.stdout:
            if line[:3] in ("A2 ", "D2 ") or "failed" in line or "Error" in line:
                keep.append(line.rstrip()); f.write(line); f.flush(); vol.commit()
        p.wait()
    try: shutil.copy("/tmp/d2.npz", "/vol/bench12_d2.npz"); vol.commit()
    except Exception: pass
    return "\n".join(keep)

@app.local_entrypoint()
def main():
    print(bench.remote())
