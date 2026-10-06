"""Round-6 utilities. Output is separate from all registered profiles and scores."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import numpy as np

BASE = '43213a5e61f591a19b4d3352a95315a62ee2aeb8'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, obj):
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + '.tmp')
    tmp.write_text(json.dumps(obj, indent=2, allow_nan=False) + '\n')
    tmp.replace(p)


def fresh(path):
    p = Path(path).resolve()
    if p.exists():
        raise FileExistsError(p)
    p.mkdir(parents=True)
    return p


def registration(text):
    if not text or text.lower() in ('todo', 'pending', 'proposed', 'none'):
        raise ValueError('Supply the actual prospective registration commit, not a placeholder')
    return text


def check_inputs(inputs):
    for p, expected in inputs.items():
        if sha(p) != expected:
            raise ValueError('Frozen input changed: ' + p)


def boltzmann(g_kcal, T, degeneracy=None):
    """Finite-state partition function. Values must share one reference state."""
    from scipy.special import logsumexp
    g = np.asarray(g_kcal, float)
    d = np.ones_like(g) if degeneracy is None else np.asarray(degeneracy, float)
    if g.ndim != 1 or not len(g) or d.shape != g.shape or not np.isfinite(T) or T <= 0:
        raise ValueError('invalid finite-state problem')
    if not np.isfinite(g).all() or not np.isfinite(d).all() or (d <= 0).any():
        raise ValueError('nonfinite energies or nonpositive degeneracy')
    R = 0.00198720425864083
    logw = np.log(d) - (g - g.min()) / (R*T)
    logz = logsumexp(logw)
    return np.exp(logw-logz), float(g.min()-R*T*logz)


def profile_envelope(psigmaA):
    """Convex-envelope statements about supplied samples, not unseen geometries."""
    p = np.asarray(psigmaA, float)
    if p.ndim != 3 or not len(p) or p.shape[1:] != (3, 51) or not np.isfinite(p).all() or (p < 0).any():
        raise ValueError('expected nonnegative (conformers,3,51) profiles')
    A = p.sum((1,2))
    if (A <= 0).any(): raise ValueError('empty profile')
    norm = p / A[:,None,None]
    sig = np.linspace(-.025,.025,51)
    tails = p[:,:,abs(sig)>=.01].sum((1,2))
    fraction = tails/A
    diameter = max(float(abs(a-b).sum()) for a in norm for b in norm)
    return dict(raw_tail_min_A2=float(tails.min()),raw_tail_max_A2=float(tails.max()),
                normalized_tail_min=float(fraction.min()),normalized_tail_max=float(fraction.max()),
                normalized_L1_diameter=diameter,
                meaning='Bounds cover convex averages of these samples only; no unsampled-basin bound.')
