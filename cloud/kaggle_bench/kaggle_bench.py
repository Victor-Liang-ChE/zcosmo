import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "mace-torch"], check=True)
import time, sys, numpy as np, torch
from ase.build import molecule
from ase import Atoms
from mace.calculators import mace_off

def water_box(n):
    L = (n**3 * 18.015 / 0.997 / 0.6022) ** (1/3)
    w = molecule("H2O"); pos = []; sym = []
    for i in range(n):
        for j in range(n):
            for k in range(n):
                c = (np.array([i, j, k]) + 0.5) * L / n
                pos += list(w.get_positions() + c); sym += list(w.get_chemical_symbols())
    return Atoms(sym, positions=pos, cell=[L]*3, pbc=True)

def run(dev):
    out = [f"torch {torch.__version__} cuda {torch.cuda.is_available()} "
           f"{torch.cuda.get_device_name(0) if torch.cuda.is_available() else ''}"]
    rng = np.random.default_rng(0)
    for size in ("small", "medium"):
        calc = mace_off(model=size, device=dev, default_dtype="float32")
        for n in (4, 6, 8):
            box = water_box(n); box.calc = calc
            box.get_forces()
            t = time.time()
            for _ in range(20):
                box.positions += 1e-4 * rng.standard_normal(box.positions.shape)
                box.get_forces()
            dt = (time.time() - t) / 20
            out.append(f"{dev} MACE-OFF {size} {len(box)} atoms: {dt*1000:.1f} ms/step -> {86400/dt*1e-6:.2f} ns/day at 1 fs")
    return "\n".join(out)

if True:
    print(run(sys.argv[1] if len(sys.argv) > 1 else "cuda"))
