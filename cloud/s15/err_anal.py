import numpy as np, sys
from bench12_core import mbar, KT, EV2KCAL
d = np.load(sys.argv[1]); lam2, mu1 = d["lam2"], d["mu1"]; r2, r1, r1d = d["rec2"], d["rec1"], d["rec1d"]
S = r2.shape[0]; bet = 1 / KT
def tau(x):  # integrated autocorrelation time (samples)
    x = x - x.mean(); n = len(x); c = np.correlate(x, x, "full")[n-1:] / (x.var() * np.arange(n, 0, -1))
    t = 1.0
    for k in range(1, n // 4):
        if c[k] < 0.05: break
        t += 2 * c[k]
    return t
print("tau stage2 (samples of 10 fs):", [round(tau(r2[:, k]), 0) for k in range(len(lam2))])
print("tau stage1:", [round(tau(r1d[:, k]), 0) for k in range(len(mu1))])
def w(x):
    w = np.zeros(len(x)); dx = np.diff(x); w[:-1] += dx / 2; w[1:] += dx / 2; return w
se2 = np.array([r2[:, k].std() * np.sqrt(tau(r2[:, k]) / S) for k in range(len(lam2))])
se1 = np.array([r1d[:, k].std() * np.sqrt(tau(r1d[:, k]) / S) for k in range(len(mu1))])
c2 = (w(lam2) * se2) ** 2; c1 = (w(mu1) * se1) ** 2
print("TI SE via autocorrelation: stage1 %.3f stage2 %.3f total %.3f kcal/mol" % (np.sqrt(c1.sum()) * EV2KCAL, np.sqrt(c2.sum()) * EV2KCAL, np.sqrt(c1.sum() + c2.sum()) * EV2KCAL))
print("variance share by window, stage1:", np.round(c1 / (c1.sum() + c2.sum()), 2), "stage2:", np.round(c2 / (c1.sum() + c2.sum()), 2))
rng = np.random.default_rng(0); B = 20; nb = 20; bl = S // nb; G = []
for b in range(B):
    pick = np.concatenate([np.arange(i * bl, (i + 1) * bl) for i in rng.integers(0, nb, nb)])
    a2 = r2[pick]; a1 = r1[pick]
    f2, _ = mbar(bet * np.outer(lam2, a2.T.reshape(-1)), np.full(len(lam2), len(pick), float), iters=2000)
    f1, _ = mbar(bet * a1.transpose(2, 1, 0).reshape(len(mu1), -1), np.full(len(mu1), len(pick), float), iters=2000)
    G.append((f1[-1] + f2[-1]) * KT * EV2KCAL)
print("MBAR block-bootstrap: %.3f +- %.3f kcal/mol" % (np.mean(G), np.std(G, ddof=1)))
