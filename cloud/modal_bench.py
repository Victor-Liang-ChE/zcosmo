import modal, pathlib
app = modal.App("zc-mace-bench")
image = (modal.Image.debian_slim(python_version="3.11")
         .pip_install("torch", "mace-torch", "ase", "numpy")
         .add_local_file(str(pathlib.Path(__file__).with_name("bench_core.py")), "/root/bench_core.py"))

@app.function(gpu="T4", image=image, timeout=1200)
def bench():
    import sys; sys.path.insert(0, "/root")
    import bench_core
    return bench_core.run("cuda")

@app.local_entrypoint()
def main():
    print(bench.remote())
