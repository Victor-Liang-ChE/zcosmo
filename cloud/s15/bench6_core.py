"""MLIP kernel study v6: fix cuEquivariance loading (preload libnvrtc from the pip CUDA wheels), then measure
speed AND accuracy of: e3nn baseline, cuEq fused kernels (ASE), torch-sim with e3nn and with the cuEq-converted
model, single and batched. Accuracy gate: max |dF| vs e3nn float32 reference on identical coordinates."""
import ctypes, glob, os, site, time, traceback
for sp in site.getsitepackages():
    for lib in sorted(glob.glob(os.path.join(sp, "nvidia", "**", "libnvrtc*.so*"), recursive=True)):
        try: ctypes.CDLL(lib, mode=ctypes.RTLD_GLOBAL)
        except OSError: pass
import numpy as np, torch
from ase.build import molecule
from ase import Atoms

def water_box(n, seed=0):
    rng = np.random.default_rng(seed)
    L = (n**3 * 18.015 / 0.997 / 0.6022) ** (1/3)
    w = molecule("H2O"); pos = []; sym = []
    for i in range(n):
        for j in range(n):
            for k in range(n):
                c = (np.array([i, j, k]) + 0.5) * L / n + 0.1 * rng.standard_normal(3)
                pos += list(w.get_positions() + c); sym += list(w.get_chemical_symbols())
    return Atoms(sym, positions=pos, cell=[L]*3, pbc=True)

def nsday(ms, dt_fs=0.5): return 86400 / (ms / 1000) * dt_fs * 1e-6

def timed(f, n=20):
    f(); torch.cuda.synchronize(); t = time.time()
    for _ in range(n): f()
    torch.cuda.synchronize(); return (time.time() - t) / n * 1000

def run(dev="cuda"):
    out = [f"torch {torch.__version__} gpu {torch.cuda.get_device_name(0)}"]
    try:
        import cuequivariance_ops_torch; out.append("cuEq ops: loaded")
    except Exception as e: out.append(f"cuEq ops: FAILED {e!r}"[:200])
    from mace.calculators import mace_off
    ref = {}
    calcs = {}
    for cueq in (False, True):
        try:
            calcs[cueq] = mace_off(model="small", device=dev, default_dtype="float32", enable_cueq=cueq)
        except Exception:
            out.append(f"load cueq={cueq} failed: " + traceback.format_exc().splitlines()[-1][:200]); continue
        for n in (4, 6, 8):
            box = water_box(n); box.calc = calcs[cueq]
            F = box.get_forces(); E = box.get_potential_energy(); ref[(cueq, n)] = (F, E)
            ms = timed(lambda: (box.positions.__iadd__(0.0), box.calc.reset(), box.get_forces()))
            out.append(f"ASE cueq={cueq} {len(box)} atoms: {ms:.1f} ms/step ({nsday(ms):.2f} ns/day @0.5 fs)")
    for n in (4, 6, 8):
        if (True, n) in ref and (False, n) in ref:
            dF = np.abs(ref[(True, n)][0] - ref[(False, n)][0]).max(); dE = abs(ref[(True, n)][1] - ref[(False, n)][1]) / (3 * n**3)
            out.append(f"ACCURACY {3*n**3} atoms cueq vs e3nn: max|dF| {dF:.2e} eV/A, |dE| {dE:.2e} eV/atom")
    try:
        import torch_sim as ts
        from torch_sim.models.mace import MaceModel
        for cueq, calc in calcs.items():
            model = MaceModel(model=calc.models[0], device=torch.device(dev), dtype=torch.float32, compute_forces=True,
                              compute_stress=False)
            for n, B in ((6, 1), (4, 20), (6, 8)):
                sys_ = [water_box(n, seed=s) for s in range(B)]
                ts.integrate(system=sys_, model=model, integrator=ts.nvt_langevin, n_steps=5, temperature=298.15, timestep=0.0005)
                torch.cuda.synchronize(); t = time.time()
                ts.integrate(system=sys_, model=model, integrator=ts.nvt_langevin, n_steps=50, temperature=298.15, timestep=0.0005)
                torch.cuda.synchronize(); ms = (time.time() - t) / 50 * 1000
                out.append(f"torch-sim cueq={cueq} {B}x{3*n**3} atoms: {ms:.1f} ms/step, aggregate {B*nsday(ms):.2f} ns/day, {ms*1000/(B*3*n**3):.1f} us/atom-step")
    except Exception:
        out.append("torch-sim failed: " + traceback.format_exc()[-400:])
    return "\n".join(out)
