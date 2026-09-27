"""Try every remaining exact speed-up on an L4, each with its accuracy/exactness check.
A: neighbour list on GPU, half-edge symmetry, static padding (+ torch.compile reduce-overhead = CUDA graphs)
C: distil a small student from MACE-OFF on the fly, then surrogate-driven HMC that samples the TEACHER exactly
D: end-state-interpolation TI probe (water decoupled from water) -> <dU/dlambda> profile and optimal window spacing"""
import ctypes, glob, os, site, time, traceback, subprocess, sys, math, json
for sp in site.getsitepackages():
    for lib in sorted(glob.glob(os.path.join(sp, "nvidia", "**", "libnvrtc*.so*"), recursive=True)):
        try: ctypes.CDLL(lib, mode=ctypes.RTLD_GLOBAL)
        except OSError: pass
import numpy as np, torch
from bench6_core import water_box
from fast_md import FastMACE, patch_half
CONV = 9.648533212e-3; KT = 8.617333e-5 * 298.15
out = []
def log(s): print(s, flush=True); out.append(s)

def teacher(cueq=True, half=False):
    from mace.calculators import mace_off
    c = mace_off(model="small", device="cuda", default_dtype="float32", enable_cueq=cueq)
    if half: log(f"   half-edge wrapped: {patch_half(c.models[0])}")
    return c

def tstep(eng, x, n=30):
    eng.forces(x); torch.cuda.synchronize(); t = time.time()
    for k in range(n): eng.forces(x + 1e-5 * k)
    torch.cuda.synchronize(); return (time.time() - t) / n * 1000

def stage_A():
    for nbox in (6, 12):
        at = water_box(nbox); c0 = teacher(); at.calc = c0; Fref = at.get_forces()
        x = torch.tensor(at.positions, dtype=torch.float32, device="cuda")
        base = FastMACE(c0, at, skin=1.0, gpu_nl=False); ms0 = tstep(base, x)
        g = FastMACE(c0, at, skin=1.0, gpu_nl=True); msg = tstep(g, x)
        t0 = time.time(); g._build(x); torch.cuda.synchronize(); tb = (time.time() - t0) * 1000
        t0 = time.time(); base._build(x); tbm = (time.time() - t0) * 1000
        _, F = g.forces(x)
        log(f"A {len(at)} atoms: matscipy-list {ms0:.1f} ms/step (rebuild {tbm:.1f} ms) | GPU-list {msg:.1f} ms (rebuild {tb:.1f} ms), max|dF| {np.abs(F.cpu().numpy()-Fref).max():.1e}")
        ch = teacher(half=True); h = FastMACE(ch, at, skin=1.0, gpu_nl=True); msh = tstep(h, x); _, Fh = h.forces(x)
        log(f"A {len(at)} atoms: + half-edge {msh:.1f} ms/step, max|dF| {np.abs(Fh.cpu().numpy()-Fref).max():.1e}")
        try:
            K = int(h.bd['edge_index'].shape[1] // 2 * 1.1)
            cp = teacher(half=True); p = FastMACE(cp, at, skin=1.0, gpu_nl=True, pad_to=K)
            cp.models[0] = torch.compile(cp.models[0], mode="reduce-overhead", dynamic=False); p.model = cp.models[0]
            for _ in range(3): p.forces(x)
            msp = tstep(p, x); _, Fp = p.forces(x)
            log(f"A {len(at)} atoms: + padding + CUDA graphs (torch.compile) {msp:.1f} ms/step, max|dF| {np.abs(Fp.cpu().numpy()-Fref).max():.1e}")
        except Exception:
            log("A compile/CUDA-graph failed: " + traceback.format_exc().splitlines()[-1][:200])

def langevin(eng, x, m, nsteps, dt=0.5, gamma=0.01, every=0, g=None):
    v = torch.randn(x.shape, device="cuda", generator=g) * torch.sqrt(KT / m * CONV)
    c1 = math.exp(-gamma * dt); E, F = eng.forces(x); frames = []
    for s in range(nsteps):
        v = v + 0.5 * dt * F / m * CONV; x = x + 0.5 * dt * v
        v = c1 * v + math.sqrt(1 - c1 * c1) * torch.sqrt(KT / m * CONV) * torch.randn(x.shape, device="cuda", generator=g)
        x = x + 0.5 * dt * v; E, F = eng.forces(x); v = v + 0.5 * dt * F / m * CONV
        if every and s % every == 0: frames.append(x.clone())
    return x, frames

def oo_peak(frames, at):
    O = torch.tensor([i for i, s in enumerate(at.get_chemical_symbols()) if s == "O"], device="cuda"); L = float(at.cell[0, 0])
    h = torch.zeros(80, device="cuda")
    for x in frames:
        d = x[O][None] - x[O][:, None]; d -= L * torch.round(d / L); r = d.norm(dim=-1)
        h += torch.histc(r[r > 0.1], bins=80, min=2.0, max=4.0)
    c = (torch.arange(80, device="cuda") + 0.5) * 0.025 + 2.0
    return float(c[h.argmax()]), float((h / h.sum()).max())

def int_energy(eng, x):
    bd = dict(eng.bd); eng.forces(x)
    b2 = dict(eng.bd); b2["positions"] = x.detach()
    o = eng.model(b2, compute_force=False, training=False)
    return float(o.get("interaction_energy", o["energy"]).double().sum())

def stage_C():
    from ase import Atoms
    from ase.io import write
    at = water_box(4); cT = teacher(); at.calc = cT
    T = FastMACE(cT, at, skin=1.0, gpu_nl=True)
    m = torch.tensor(at.get_masses(), dtype=torch.float32, device="cuda")[:, None]
    g = torch.Generator(device="cuda").manual_seed(3)
    x = torch.tensor(at.positions, dtype=torch.float32, device="cuda")
    t0 = time.time(); x, fr = langevin(T, x, m, 24000, every=50, g=g)   # 12 ps, frame every 25 fs
    log(f"C teacher MD 12 ps: {time.time()-t0:.0f} s, {len(fr)} frames")
    ref_frames = fr[len(fr)//3:]
    confs = []
    for f in fr[40:]:
        a = Atoms(at.get_chemical_symbols(), positions=f.cpu().numpy(), cell=at.cell, pbc=True); a.calc = cT
        a.info["REF_energy"] = float(a.get_potential_energy()); a.arrays["REF_forces"] = a.get_forces(); confs.append(a)
    write("/tmp/train.xyz", confs)
    cmd = ["mace_run_train", "--name", "student", "--train_file", "/tmp/train.xyz", "--valid_fraction", "0.1",
           "--E0s", "average", "--model", "MACE", "--num_channels", "16", "--max_L", "0", "--r_max", "4.5",
           "--num_interactions", "2", "--correlation", "2", "--batch_size", "4", "--max_num_epochs", "60",
           "--device", "cuda", "--default_dtype", "float32", "--energy_key", "REF_energy", "--forces_key", "REF_forces",
           "--forces_weight", "100", "--energy_weight", "1", "--work_dir", "/tmp/stu", "--seed", "1"]
    t0 = time.time(); r = subprocess.run(cmd, capture_output=True, text=True)
    mp = sorted(glob.glob("/tmp/stu/*student*.model"))
    log(f"C student training {time.time()-t0:.0f} s, files {[os.path.basename(p) for p in mp]}, rc {r.returncode}")
    if not mp: log("C train stderr: " + r.stderr[-600:]); return
    from mace.calculators import MACECalculator
    cS = MACECalculator(model_paths=[p for p in mp if "compiled" not in p][0], device="cuda", default_dtype="float32")
    S = FastMACE(cS, at, skin=1.0, gpu_nl=True)
    Fs = np.concatenate([S.forces(torch.tensor(a.positions, dtype=torch.float32, device="cuda"))[1].cpu().numpy() - a.arrays["REF_forces"] for a in confs[-40:]])
    log(f"C student force MAE vs teacher (last 40 frames, seen in training/valid mix): {np.abs(Fs).mean()*1000:.1f} meV/A")
    xs = torch.tensor(at.positions, dtype=torch.float32, device="cuda"); msT = tstep(T, xs); msS = tstep(S, xs)
    log(f"C cost per force call: teacher {msT:.1f} ms, student {msS:.1f} ms ({msT/msS:.1f}x)")
    for nstep, dt in ((10, 0.5), (20, 0.5), (20, 1.0)):
        x = fr[-1].clone(); acc = 0; ntraj = 150; samples = []; t0 = time.time()
        U = int_energy(T, x)
        for k in range(ntraj):
            v = torch.randn(x.shape, device="cuda", generator=g) * torch.sqrt(KT / m * CONV)
            ke = lambda vv: float((m.double() * vv.double() ** 2).sum()) * 0.5 / CONV
            H0 = U + ke(v)
            y, q = x.clone(), v.clone(); _, F = S.forces(y)
            for _ in range(nstep):
                q = q + 0.5 * dt * F / m * CONV; y = y + dt * q; _, F = S.forces(y); q = q + 0.5 * dt * F / m * CONV
            U1 = int_energy(T, y); H1 = U1 + ke(q)
            if math.log(max(torch.rand(1, generator=g, device="cuda").item(), 1e-300)) < -(H1 - H0) / KT:
                x, U, acc = y, U1, acc + 1
            samples.append(x.clone())
        wall = time.time() - t0; ps = ntraj * nstep * dt / 1000
        pk = oo_peak(samples[30:], at); rk = oo_peak(ref_frames, at)
        log(f"C surrogate-HMC n={nstep} dt={dt} fs: acceptance {acc/ntraj:.2f}, {2*ntraj} teacher calls for {ps:.1f} ps "
            f"(plain MD needs {int(ps*1000/0.5)}), wall {wall:.0f} s; O-O peak {pk[0]:.3f} A (teacher MD {rk[0]:.3f} A)")

def stage_D():
    at = water_box(4); c = teacher(); at.calc = c
    sym = at.get_chemical_symbols(); n = len(at)
    solute = [0, 1, 2]; solv = list(range(3, n))
    Afull = FastMACE(c, at, skin=1.0, gpu_nl=True)
    Asol = FastMACE(c, at[solv], skin=1.0, gpu_nl=True)
    Aone = FastMACE(c, at[solute], skin=1.0, gpu_nl=True)
    m = torch.tensor(at.get_masses(), dtype=torch.float32, device="cuda")[:, None]
    g = torch.Generator(device="cuda").manual_seed(5)
    x0 = torch.tensor(at.positions, dtype=torch.float32, device="cuda"); x0, _ = langevin(Afull, x0, m, 2000, g=g)
    res = []
    for lam in (0.0, 0.02, 0.05, 0.1, 0.2, 0.35, 0.5, 0.65, 0.8, 0.9, 1.0):
        class Mix:
            def forces(self, x):
                Ef, Ff = Afull.forces(x); Es, Fs = Asol.forces(x[solv]); Eo, Fo = Aone.forces(x[solute])
                Fsep = torch.cat([Fo, Fs]) if solute == [0, 1, 2] else None
                self.du = float(Ef.double() - Es.double() - Eo.double())
                return None, lam * Ff + (1 - lam) * Fsep
        mix = Mix(); x = x0.clone(); dus = []; ok = True; t0 = time.time()
        v = torch.randn(x.shape, device="cuda", generator=g) * torch.sqrt(KT / m * CONV); c1 = math.exp(-0.005)
        _, F = mix.forces(x)
        for s in range(3000):
            v = v + 0.25 * F / m * CONV; x = x + 0.25 * v
            v = c1 * v + math.sqrt(1 - c1 * c1) * torch.sqrt(KT / m * CONV) * torch.randn(x.shape, device="cuda", generator=g)
            x = x + 0.25 * v; _, F = mix.forces(x); v = v + 0.25 * F / m * CONV
            if not torch.isfinite(F).all(): ok = False; break
            if s >= 1000 and s % 10 == 0: dus.append(mix.du)
        dus = np.array(dus)
        res.append((lam, float(dus.mean()) if len(dus) else float("nan"), float(dus.std()) if len(dus) else float("nan"), ok))
        log(f"D lambda {lam:.2f}: <dU/dl> {res[-1][1]:.3f} eV, sd {res[-1][2]:.3f} eV, {'ok' if ok else 'BLEW UP'}, {time.time()-t0:.0f} s")
    lam = np.array([r[0] for r in res]); mu = np.array([r[1] for r in res]); sd = np.array([r[2] for r in res])
    if np.isfinite(mu).all():
        dG = np.trapz(mu, lam) * 23.0605
        # thermodynamic length: optimal windows are equally spaced in cumulative integral of sd(lambda)
        cum = np.concatenate([[0], np.cumsum(0.5 * (sd[1:] + sd[:-1]) * np.diff(lam))]); cum /= cum[-1]
        opt = np.interp(np.linspace(0, 1, 11), cum, lam)
        var_uniform = np.trapz(sd, lam) ** 2
        log(f"D TI estimate of decoupling (1 ps/window, not converged, feasibility only): {dG:.1f} kcal/mol; "
            f"optimal 11-window spacing {np.round(opt, 3).tolist()}")

if __name__ == "__main__":
    for st in (stage_A, stage_C, stage_D):
        try: st()
        except Exception: log(f"{st.__name__} failed: " + traceback.format_exc()[-700:])
    json.dump(out, open("/tmp/bench11.json", "w"))
