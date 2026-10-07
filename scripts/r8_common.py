"""R8 bookkeeping and finite-resolution diagnostics. No production changes."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import numpy as np

BASE = '58cc629df42156c0b7862710057318db0a495dbb'
STEPS = np.array([.016, .008, .004, .002, .001])  # Bohr, unchanged P33 ladder
TAU = 1e-5
CASES = {
    'TEG': ('ZIBGPFATKBEMQZ-UHFFFAOYSA-N', 'bond-3-4'),
    'EG': ('LYCAIKOWRPUZTN-UHFFFAOYSA-N', 'bond-2-3'),
}
ARMS = ('pcm_pruned', 'pcm_unpruned', 'vacuum_pruned', 'vacuum_unpruned')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, obj):
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + '.tmp')
    tmp.write_text(json.dumps(obj, indent=2, allow_nan=False) + '\n')
    os.replace(tmp, p)


def read(path):
    return json.loads(Path(path).read_text())


def validate_direction(v, n):
    v = np.asarray(v, float)
    if v.shape != (n, 3) or not np.isfinite(v).all():
        raise ValueError('Malformed archived direction')
    if abs(np.linalg.norm(v) - 1.) > 1e-10:
        raise ValueError('Use the archived P33 unit-L2 Cartesian direction')
    return v


def richardson(energies):
    e = np.asarray(energies, float)
    if e.shape != (5, 2) or not np.isfinite(e).all():
        raise ValueError('Need all five finite +/- energy pairs, no selected h')
    d = (e[:, 0] - e[:, 1]) / (2 * STEPS)
    return (4 * d[1:] - d[:-1]) / 3


def fd_check(tight, strict, g_tight, g_full, g_off, topology_stable=True):
    """Same P33 empirical accuracy allocation; not a certified error bound."""
    from r7_common import fd_assess
    ans = fd_assess(tight, strict, g_tight, g_full, g_off,
                    topology_stable=topology_stable)
    if ans['tolerance'] != TAU or ans['steps_Bohr'] != STEPS.tolist():
        raise ValueError('P33 resolution changed')
    return ans


def canonical_membership(owners, ordinals):
    """Count is insufficient: hash an order-independent multiset of node IDs."""
    a = np.asarray(owners, dtype=np.int64)
    b = np.asarray(ordinals, dtype=np.int64)
    if a.ndim != 1 or a.shape != b.shape or np.any(a < 0) or np.any(b < 0):
        raise ValueError('Invalid node identities')
    ids = np.c_[a, b]
    order = np.lexsort((ids[:, 1], ids[:, 0])); ids = ids[order]
    if len(ids) > 1 and np.any(np.all(ids[1:] == ids[:-1], axis=1)):
        raise ValueError('Duplicate quadrature node identity')
    return hashlib.sha256(ids.astype('<i8').tobytes()).hexdigest(), order


def match_local_nodes(local, template):
    """Identify nodes by the generating atomic template, not rounded world positions."""
    from scipy.spatial import cKDTree
    local = np.asarray(local, float); template = np.asarray(template, float)
    if local.ndim != 2 or local.shape[1] != 3 or not len(template):
        raise ValueError('Invalid quadrature coordinates')
    dist, index = cKDTree(template).query(local)
    scale = np.maximum(1., np.linalg.norm(local, axis=1))
    if np.any(dist > 1e-9 * scale):
        raise ValueError('Cannot identify a quadrature node in its atomic template')
    return index.astype(np.int64)


def screening_counts(rows):
    """Keep missing cases and coverage failures separate. Do not estimate prevalence."""
    keys = [r['key'] for r in rows]
    if len(keys) != len(set(keys)):
        raise ValueError('Duplicate screen key')
    complete = [r for r in rows if r.get('status') == 'complete']
    for r in complete:
        if type(r.get('screen_positive')) is not bool:
            raise ValueError('Complete screen lacks a Boolean decision')
    result = dict(requested=len(rows),
        positive=sum(r['screen_positive'] for r in complete),
        negative=sum(not r['screen_positive'] for r in complete),
        affinity_unresolved=sum(r.get('status') == 'affinity_unresolved' for r in rows),
        native_missing_or_failed=sum(r.get('status') not in ('complete', 'affinity_unresolved') for r in rows),
        force_observed=sum('response_change_max' in r for r in rows),
        force_over_1e_5=sum(float(r.get('response_change_max', 0.)) > 1e-5 for r in rows),
        sampling_bound=None,
        scope='Fixed-displacement sensitivity only; no inferred geometry error or population bound')
    if result['positive'] + result['negative'] + result['affinity_unresolved'] + result['native_missing_or_failed'] != len(rows):
        raise AssertionError('Lost denominator')
    return result


def file_sources(paths):
    return {str(p): sha(p) for p in paths}


def check_sources(sources):
    for path, digest in sources.items():
        if sha(path) != digest:
            raise ValueError('Frozen source changed: ' + path)
