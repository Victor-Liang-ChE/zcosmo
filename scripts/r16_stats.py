"""R16 fixed-design accounting. No model evaluation and no data acquisition."""
from __future__ import annotations
import hashlib
import numpy as np
from r16_london import require

BOOTSTRAPS = 1000
SEED = 'R16-LV1-fixed-look-20261008'
GRID_SIZES = (81, 161)
GAP_TOL = 1e-7  # dimensionless g/RT, numerical indicator, not a certificate


def grids():
    return tuple(np.unique(np.r_[np.logspace(-6, -2, 10),
        np.linspace(.02, .98, n), 1-np.logspace(-2, -6, 10)]) for n in GRID_SIZES)


def grid_union():
    return np.unique(np.concatenate(grids()))


def hull_gap(x, g):
    x, g = np.asarray(x, float), np.asarray(g, float)
    require(x.ndim == g.ndim == 1 and len(x) >= 3 and x.shape == g.shape and
            np.isfinite(x).all() and np.isfinite(g).all() and
            (np.diff(x) > 0).all(), 'Invalid convexity grid')
    hull = []
    for k in range(len(x)):
        while len(hull) >= 2:
            a, b = hull[-2:]
            if (x[b]-x[a])*(g[k]-g[a])-(g[b]-g[a])*(x[k]-x[a]) > 0:
                break
            hull.pop()
        hull.append(k)
    line = np.interp(x, x[hull], g[hull])
    gap = float(np.max(g-line))
    return gap > GAP_TOL, gap


def detection(lngamma):
    """Same baseline/candidate grids. A disagreement is not called miscibility."""
    union = grid_union(); a = np.asarray(lngamma, float)
    require(a.shape == (len(union), 2) and np.isfinite(a).all(), 'Incomplete LLE grid')
    indicators, gaps = [], []
    for x in grids():
        idx = np.searchsorted(union, x)
        require(np.array_equal(union[idx], x), 'LLE grid identity drift')
        g = x*np.log(x)+(1-x)*np.log1p(-x)+x*a[idx,0]+(1-x)*a[idx,1]
        found, gap = hull_gap(x, g)
        indicators.append(found); gaps.append(gap)
    return dict(detected=indicators[0] if indicators[0] == indicators[1] else None,
                grid_agreement=indicators[0] == indicators[1], gaps=gaps,
                numerical_indicator_not_global_stability=True)


def rng_for(label):
    seed = int.from_bytes(hashlib.sha256((SEED+'|'+label).encode()).digest()[:8], 'big')
    return np.random.default_rng(seed)


def paired_summary(truth, values, systems, label, percent=False):
    """Equal observation weight, with a paired system bootstrap.

    Intervals describe this exposed collection; they are not fresh holdout
    inference. One-sided 95% bounds use the 5th and 95th percentiles.
    """
    truth, values = np.asarray(truth, float), np.asarray(values, float)
    require(truth.ndim == 1 and len(truth) > 0 and values.shape == (len(truth),2)
            and len(systems) == len(truth) and np.isfinite(truth).all()
            and np.isfinite(values).all(), 'Incomplete paired metric')
    signed = values-truth[:,None]
    if percent:
        require((truth > 0).all(), 'Pressure must be positive')
        signed *= 100/truth[:,None]
    require(np.isfinite(signed).all(), 'Derived metric overflow')
    losses = np.abs(signed)
    unique = sorted(set(systems))
    groups = [np.flatnonzero(np.array(systems) == s) for s in unique]
    counts = np.array([len(i) for i in groups])
    sums = np.array([losses[i].sum(0) for i in groups])
    rng = rng_for(label); delta = []
    for _ in range(BOOTSTRAPS):
        sample = rng.integers(0, len(groups), len(groups))
        means = sums[sample].sum(0)/counts[sample].sum()
        delta.append(means[1]-means[0])
    return dict(rows=len(truth), systems=len(groups), baseline=float(losses[:,0].mean()),
        candidate=float(losses[:,1].mean()), change=float(np.diff(losses.mean(0))[0]),
        bias=signed.mean(0).tolist(), equal_system=np.mean(sums/counts[:,None],axis=0).tolist(),
        delta_CI95=np.quantile(delta,[.025,.975]).tolist(),
        delta_one_sided_upper95=float(np.quantile(delta,.95)),
        improved=int((losses[:,1] < losses[:,0]).sum()),
        worsened=int((losses[:,1] > losses[:,0]).sum()),
        scope='exposed fixed-design comparison; no restored holdout guarantee')


def lle_summary(positive, negative):
    """Rows: (system, baseline detection, candidate detection).

    Positive systems use the original >half-of-observations rule. Negatives
    must have exactly one saved state per unordered binary. No uncertain
    state is permitted to enter this function as False.
    """
    require(positive and negative, 'Both LLE classes required')
    def group(rows, is_negative=False):
        result = []
        systems = sorted({r[0] for r in rows})
        for s in systems:
            part = [(r[1],r[2]) for r in rows if r[0] == s]
            require(all(type(v) is bool for p in part for v in p), 'Unresolved LLE detection')
            if is_negative:
                require(len(part) == 1, 'Duplicate negative binary')
            result.append(np.array(part).mean(0) > .5)
        return np.array(result, float), systems
    p, ps = group(positive); n, ns = group(negative,True)
    recall, fp = p.mean(0), n.mean(0)
    ba = .5*(recall+1-fp)
    rng = rng_for('lle'); changes = []
    for _ in range(BOOTSTRAPS):
        rp = p[rng.integers(0,len(p),len(p))].mean(0)
        fn = n[rng.integers(0,len(n),len(n))].mean(0)
        changes.append([rp[1]-rp[0],fn[1]-fn[0],.5*((rp[1]-rp[0])-(fn[1]-fn[0]))])
    changes = np.array(changes)
    return dict(positive_rows=len(positive),positive_systems=len(ps),negative_systems=len(ns),
        recall=recall.tolist(),false_positive_rate=fp.tolist(),balanced_accuracy=ba.tolist(),
        recall_change_lower95=float(np.quantile(changes[:,0],.05)),
        false_positive_change_upper95=float(np.quantile(changes[:,1],.95)),
        balanced_accuracy_change_lower95=float(np.quantile(changes[:,2],.05)),
        numerical_indicator_not_global_stability=True)


def gates(scores):
    """No positive noninferiority margin; failure is recorded without tuning."""
    v, i, h, l = (scores[k] for k in ('vle','idac','he','lle'))
    flags = dict(vle_improves=v['change'] < 0 and v['delta_one_sided_upper95'] < 0,
        idac_does_not_worsen=i['change'] <= 0 and i['delta_one_sided_upper95'] <= 0,
        he_does_not_worsen=h['change'] <= 0 and h['delta_one_sided_upper95'] <= 0,
        lle_recall_does_not_worsen=l['recall'][1] >= l['recall'][0] and l['recall_change_lower95'] >= 0,
        lle_false_positives_do_not_worsen=l['false_positive_rate'][1] <= l['false_positive_rate'][0]
            and l['false_positive_change_upper95'] <= 0,
        lle_balanced_accuracy_does_not_worsen=l['balanced_accuracy'][1] >= l['balanced_accuracy'][0]
            and l['balanced_accuracy_change_lower95'] >= 0)
    return dict(checks=flags,passed=all(flags.values()),adopted=False,
                scope='One exposed development screen, not universal or untouched validation')
