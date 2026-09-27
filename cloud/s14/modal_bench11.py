import modal, pathlib
here = pathlib.Path(__file__).parent
app = modal.App("zc-bench11")
image = (modal.Image.debian_slim(python_version="3.11")
         .pip_install("torch", "mace-torch[cueq]", "cuequivariance-ops-torch-cu13", "nvidia-cuda-nvrtc", "matscipy", "ase", "numpy")
         .add_local_file(str(here / "bench11_core.py"), "/root/bench11_core.py")
         .add_local_file(str(here / "bench6_core.py"), "/root/bench6_core.py")
         .add_local_file(str(here / "fast_md.py"), "/root/fast_md.py")
         .add_local_file(str(here / "zc_md.py"), "/root/zc_md.py"))

@app.function(gpu="L4", image=image, timeout=4 * 3600)
def bench():
    import subprocess, sys
    r = subprocess.run([sys.executable, "/root/bench11_core.py"], cwd="/root", capture_output=True, text=True)
    return "\n".join(l for l in r.stdout.splitlines() if l[:2] in ("A ", "C ", "D ") or "failed" in l) + "\n" + r.stderr[-800:]

@app.local_entrypoint()
def main():
    print(bench.remote())
