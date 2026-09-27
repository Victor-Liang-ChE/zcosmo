"""bench12 (L4): (A2) exact multi-system batching throughput; (D2) two-stage cavity TI for decoupling one water
from 63 waters with MACE-OFF23 small, all lambda windows batched into ONE MACE graph per step.

D2 path (registered before running, PREREGISTRATION.md 2026-09-26):
  stage 1 (decoupled solute): grow a purely repulsive soft-core WCA cavity between solute and solvent atoms,
      U1(mu) = U_MACE(solvent) + U_MACE(solute) + U_scWCA(mu)
  stage 2: U2(l) = l U_MACE(full) + (1 - l) [U_MACE(solvent) + U_MACE(solute) + U_WCA]
  dG(couple) = dG1 + dG2; both ends exact (stage-2 l = 1 is plain MACE), the cavity only keeps solvent atoms off
  the solute where the full-system MACE energy is undefined (bench11 D: <dU/dl> ~ 1e10 eV at l = 0).
  WCA: eps = 1 kcal/mol; sigma 2.4 A heavy-heavy, 1.4 A pairs with H (cutoffs 2.69 / 1.57 A, below H-bond
  distances); Beutler soft-core alpha = 0.5. Path parameters do not change dG, only its variance."""
import ctypes, glob, os, site, time, traceback, math, json
for sp in site.getsitepackages():
    for lib in sorted(glob.glob(os.path.join(sp, "nvidia", "**", "libnvrtc*.so*"), recursive=True)):
        try: ctypes.CDLL(lib, mode=ctypes.RTLD_GLOBAL)
        except OSError: pass
import numpy as np, torch
from bench6_core import water_box
from multi_mace import MultiMACE

CONV = 9.648533212e-3; KB = 8.617333e-5; T = 298.15; KT = KB * T; EV2KCAL = 23.0605
EPS = 1.0 / EV2KCAL; ALPHA = 0.5
PROD = int(os.environ.get("ZC_PROD_STEPS", "16000")); EQ = int(os.environ.get("ZC_EQ_STEPS", "2000"))
out = []
DEV = "cuda" if torch.cuda.is_available() else "cpu"
PRE = int(os.environ.get("ZC_PRE_STEPS", "2000"))
def log(s): print(s, flush=True); out.append(s)

def teacher(cueq=None):
    cueq = (DEV == "cuda") if cueq is None else cueq
    from mace.calculators import mace_off
    return mace_off(model="small", device=DEV, default_dtype="float32", enable_cueq=cueq)


def stage_A2():
    c = teacher()
    for nbox, reps in ((4, (1, 2, 4, 8, 16, 32)), (6, (1, 4, 8))):
        base = water_box(nbox); n = len(base); ms1 = None
        for B in reps:
            systems = [water_box(nbox, seed=s) for s in range(B)]
            mm = MultiMACE(c, systems, skin=1.0)
            x = torch.cat([torch.tensor(a.positions, dtype=torch.float32, device=DEV) for a in systems])
            mm.forces(x); (torch.cuda.synchronize() if DEV == "cuda" else None); t = time.time()
            for k in range(20): mm.forces(x + 1e-5 * k)
            (torch.cuda.synchronize() if DEV == "cuda" else None); ms = (time.time() - t) / 20 * 1000; ms1 = ms1 or ms
            a0 = systems[-1].copy(); a0.calc = c; F0 = a0.get_forces()
            _, F = mm.forces(x); dF = np.abs(F[-n:].cpu().numpy() - F0).max()
            log(f"A2 {B:2d} x {n} atoms: {ms:6.1f} ms/call -> {ms/B:5.1f} ms per replica ({ms1*B/ms:4.1f}x throughput), max|dF| last replica {dF:.1e}")


def wca(xsolu, xsolv, L, sig, mu, alpha=ALPHA):
    """Beutler soft-core WCA between solute (W,a,3) and solvent (W,b,3); mu (W,) or (W,K). Returns (W,) or (W,K)."""
    d = xsolv[:, None, :, :] - xsolu[:, :, None, :]
    d = d - L * torch.round(d / L)
    r6 = (d.norm(dim=-1) / sig) ** 6                                       # (W,a,b)
    if mu.dim() == 1: mu = mu[:, None]
    s = alpha * (1 - mu)[:, :, None, None] + r6[:, None]                   # (W,K,a,b)
    u = mu[:, :, None, None] * EPS * (4 * (1 / s ** 2 - 1 / s) + 1)
    return torch.where(s < 2.0, u, torch.zeros_like(u)).sum((-1, -2)).squeeze(1) if mu.shape[1] == 1 else \
        torch.where(s < 2.0, u, torch.zeros_like(u)).sum((-1, -2))


def mbar(u_kn, N_k, iters=5000):
    K = len(N_k); f = np.zeros(K); lN = np.log(N_k)
    for _ in range(iters):
        a = -u_kn + (f + lN)[:, None]; mx = a.max(0); den = mx + np.log(np.exp(a - mx).sum(0))
        b = -u_kn - den[None]; mb = b.max(1); fn = -(mb + np.log(np.exp(b - mb[:, None]).sum(1)))
        fn -= fn[0]
        if np.abs(fn - f).max() < 1e-9: f = fn; break
        f = fn
    a = -u_kn + (f + lN)[:, None]; mx = a.max(0); den = mx + np.log(np.exp(a - mx).sum(0))
    W = np.exp(-u_kn + f[:, None] - den[None]).T                          # (N, K), columns sum to 1
    O = (W.T @ W) * N_k[None, :]
    return f, O


def block_se(x, nb=5):
    b = np.array_split(np.asarray(x), nb); m = np.array([bb.mean() for bb in b]); return m.std(ddof=1) / math.sqrt(nb)


def solute_box(c, name):
    """64-water box with water 0 replaced by the solute (same centre, random orientation) and the one other water
    whose O is nearest the solute removed; then FIRE-relaxed with MACE so no start overlaps remain."""
    from ase.build import molecule
    from ase.optimize import FIRE
    at = water_box(4)
    if name == "water":
        return at, 3
    mol = molecule({"methanol": "CH3OH"}[name]); mol.rotate(np.random.default_rng(3).uniform(0, 360), "z")
    L = float(at.cell[0, 0]); ctr = at.positions[0]
    mol.translate(ctr - mol.get_center_of_mass())
    rest = at[3:]; dO = [np.linalg.norm(((rest.positions[i] - ctr + L / 2) % L) - L / 2) for i in range(0, len(rest), 3)]
    k = int(np.argmin(dO)); keep = [i for i in range(len(rest)) if i // 3 != k]
    box = mol + rest[keep]; box.set_cell(at.cell); box.set_pbc(True); box.calc = c
    FIRE(box, logfile=None).run(fmax=0.3, steps=300)
    return box, len(mol)


def stage_D2():
    c = teacher(); name = os.environ.get("ZC_SOLUTE", "water")
    at, ns = solute_box(c, name); n = len(at); L = float(at.cell[0, 0])
    log(f"D2 solute {name}: {ns} atoms + {(n-ns)//3} waters, L = {L:.3f} A")
    sym = at.get_chemical_symbols(); solu = list(range(ns)); solv = list(range(ns, n))
    heavy = torch.tensor([s != "H" for s in sym], device=DEV)
    sig = torch.where(heavy[solu][:, None] & heavy[solv][None, :], 2.4, 1.4).float()
    lam2 = [0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    mu1 = [0.0, 0.05, 0.1, 0.2, 0.35, 0.5, 0.65, 0.8, 0.9, 1.0]
    if os.environ.get("ZC_TEST"): lam2, mu1 = [0.0, 0.5, 1.0], [0.0, 1.0]
    W2, W1 = len(lam2), len(mu1); W = W2 + W1
    # equilibrate one coupled box, then start every window from it
    one = MultiMACE(c, [at]); m1 = torch.tensor(at.get_masses(), dtype=torch.float32, device=DEV)[:, None]
    g = torch.Generator(device=DEV).manual_seed(7)
    x = torch.tensor(at.positions, dtype=torch.float32, device=DEV); v = torch.randn(x.shape, device=DEV, generator=g) * torch.sqrt(KT / m1 * CONV)
    c1 = math.exp(-0.01 * 0.5); _, F = one.forces(x)
    for s in range(PRE):
        v += 0.25 * F / m1 * CONV; x += 0.25 * v
        v = c1 * v + math.sqrt(1 - c1 * c1) * torch.sqrt(KT / m1 * CONV) * torch.randn(x.shape, device=DEV, generator=g)
        x += 0.25 * v; _, F = one.forces(x); v += 0.25 * F / m1 * CONV
    # graphs: per stage-2 window [full, solvent, solute]; per stage-1 window [solvent, solute]
    systems, idx, wnode = [], [], []
    for w in range(W):
        base = w * n
        if w < W2:
            systems.append(at); idx.append(base + np.arange(n)); wnode.append(np.full(n, lam2[w]))
            lsep = 1 - lam2[w]
        else:
            lsep = 1.0
        systems += [at[solv], at[solu]]
        idx += [base + np.array(solv), base + np.array(solu)]; wnode += [np.full(len(solv), lsep), np.full(ns, lsep)]
    idx = torch.tensor(np.concatenate(idx), device=DEV); wnode = torch.tensor(np.concatenate(wnode), dtype=torch.float32, device=DEV)[:, None]
    mm = MultiMACE(c, systems, skin=1.0)
    log(f"D2 batched graph: {mm.G} systems, {mm.M} nodes for {W} windows")
    lamt = torch.tensor(lam2, device=DEV); mut = torch.tensor(mu1, device=DEV); mu_all = mut[None].repeat(W1, 1)
    X = x.repeat(W, 1).clone(); m = m1.repeat(W, 1); V = torch.randn(X.shape, device=DEV, generator=g) * torch.sqrt(KT / m * CONV)
    solu_i = torch.tensor([w * n + i for w in range(W) for i in solu], device=DEV).view(W, ns)
    solv_i = torch.tensor([w * n + i for w in range(W) for i in solv], device=DEV).view(W, len(solv))

    def force():
        E, Fm = mm.forces(X[idx])
        Fp = torch.zeros_like(X).index_add_(0, idx, wnode * Fm)
        Xg = X.detach().requires_grad_(True)
        xs, xv = Xg[solu_i], Xg[solv_i]
        strength = torch.cat([1 - lamt, torch.ones(W1, device=DEV)])
        mu_eff = torch.cat([torch.ones(W2, device=DEV), mut])
        Uw = wca(xs, xv, L, sig, mu_eff)                                  # (W,)
        Fw, = torch.autograd.grad((strength * Uw).sum(), Xg)
        Fp -= Fw
        e2 = E[: 3 * W2].view(W2, 3)
        du2 = (e2[:, 0] - e2[:, 1] - e2[:, 2] - Uw[:W2]).detach()            # dU/dl, stage 2
        return Fp, du2, xs.detach(), xv.detach()

    t0 = time.time(); F, du2, xs, xv = force(); rec2, rec1, rec1d = [], [], []
    for s in range(EQ + PROD):
        V += 0.25 * F / m * CONV; X += 0.25 * V
        V = c1 * V + math.sqrt(1 - c1 * c1) * torch.sqrt(KT / m * CONV) * torch.randn(X.shape, device=DEV, generator=g)
        X += 0.25 * V; F, du2, xs, xv = force(); V += 0.25 * F / m * CONV
        if not torch.isfinite(F).all():
            log(f"D2 non-finite forces at step {s}"); return
        if s >= EQ and s % 20 == 0:
            rec2.append(du2.cpu().numpy())
            with torch.no_grad():
                u_all = wca(xs[W2:], xv[W2:], L, sig, mu_all)             # (W1, K1) U_wca of each stage-1 sample at every mu
                mu_g = mut.clone().requires_grad_(True)
            with torch.enable_grad():
                d1, = torch.autograd.grad(wca(xs[W2:], xv[W2:], L, sig, mu_g).sum(), mu_g)
            rec1.append(u_all.cpu().numpy()); rec1d.append(d1.detach().cpu().numpy())
        if s == min(EQ + 999, EQ + PROD - 1):
            log(f"D2 speed: {(time.time()-t0)/(s+1)*1000:.1f} ms/step for all {W} windows (rebuilds {mm.n_rebuild})")
    wall = time.time() - t0
    rec2, rec1, rec1d = np.array(rec2), np.array(rec1), np.array(rec1d)      # (S,W2), (S,W1,K1), (S,W1)
    np.savez(f"/tmp/d2_{name}.npz", lam2=lam2, mu1=mu1, rec2=rec2, rec1=rec1, rec1d=rec1d)
    json.dump({"lam2": lam2, "mu1": mu1}, open("/tmp/d2.json", "w"))
    bet = 1 / KT; S = rec2.shape[0]
    # TI
    m2 = rec2.mean(0); se2 = np.array([block_se(rec2[:, k]) for k in range(W2)])
    m1d = rec1d.mean(0); se1 = np.array([block_se(rec1d[:, k]) for k in range(W1)])
    def trap(xk, yk, sk):
        w = np.zeros(len(xk)); dx = np.diff(xk); w[:-1] += dx / 2; w[1:] += dx / 2
        return float(w @ yk), float(np.sqrt((w ** 2) @ sk ** 2))
    g2, e2 = trap(lam2, m2, se2); g1, e1 = trap(mu1, m1d, se1)
    for k in range(W2): log(f"D2 stage2 l={lam2[k]:.2f}: <dU/dl> {m2[k]:+.4f} eV (se {se2[k]:.4f}, sd {rec2[:, k].std():.4f})")
    for k in range(W1): log(f"D2 stage1 mu={mu1[k]:.2f}: <dU/dmu> {m1d[k]:+.4f} eV (se {se1[k]:.4f})")
    # MBAR (reduced potentials differ only by the lambda- or mu-dependent parts)
    u2 = bet * np.outer(lam2, rec2.T.reshape(-1))
    f2, O2 = mbar(u2, np.full(W2, S, dtype=float))
    u1 = bet * rec1.transpose(2, 1, 0).reshape(W1, -1)                    # u1[k, (window, sample)]
    f1, O1 = mbar(u1, np.full(W1, S, dtype=float))
    ov2 = min(O2[i, i + 1] for i in range(W2 - 1)); ov1 = min(O1[i, i + 1] for i in range(W1 - 1))
    G2m, G1m = f2[-1] * KT * EV2KCAL, f1[-1] * KT * EV2KCAL
    log(f"D2 stage1 (cavity growth, decoupled): TI {g1*EV2KCAL:+.3f} +- {e1*EV2KCAL:.3f}, MBAR {G1m:+.3f} kcal/mol; min neighbour overlap {ov1:.3f}")
    log(f"D2 stage2 (cavity -> full MACE):      TI {g2*EV2KCAL:+.3f} +- {e2*EV2KCAL:.3f}, MBAR {G2m:+.3f} kcal/mol; min neighbour overlap {ov2:.3f}")
    log(f"D2 coupling free energy of {name} in MACE-OFF23-small water (298 K, {S} samples/window x 10 fs, "
        f"{(EQ+PROD)*0.5/1000:.1f} ps/window, wall {wall/60:.0f} min): TI {(g1+g2)*EV2KCAL:+.3f} +- {math.hypot(e1,e2)*EV2KCAL:.3f}, "
        f"MBAR {G1m+G2m:+.3f} kcal/mol  [feasibility only]")


if __name__ == "__main__":
    for st in (stage_D2,):
        try: st()
        except Exception: log(f"{st.__name__} failed: " + traceback.format_exc()[-1500:])
