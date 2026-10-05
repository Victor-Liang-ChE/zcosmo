"""Round-3 audit utilities. No model parameters and no production writes."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

BASE = 'c515e38e1a7fd91a02e1ff1f1209a81b67a7d49d'
STALL_KEYS = (
 'BTFJIXJJCSYFAL-UHFFFAOYSA-N', 'FLIACVVOZYBSBS-UHFFFAOYSA-N',
 'HPEUJPJOZXNMSJ-UHFFFAOYSA-N', 'MVLVMROFTAUDAG-UHFFFAOYSA-N',
 'OYHQOLUKZRVURQ-HZJYTTRNSA-N', 'PYGXAGIECVVIOZ-UHFFFAOYSA-N')
WATER = 'XLYOFNOQVPJJNP-UHFFFAOYSA-N'

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def write_json(path, obj):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_text(json.dumps(obj, indent=2, allow_nan=False) + '\n')
    tmp.replace(path)

def scalar(x):
    if pd.isna(x): return None
    if isinstance(x, (float, np.floating)): return format(float(x), '.12g')
    if isinstance(x, (int, np.integer)): return str(int(x))
    return str(x)

def row_ids(df, prediction='pred_ln_gamma_inf'):
    """Observation identity, not (solute, solvent, T) alone. Refuse ambiguous duplicates."""
    required = ['file', 'dataset', 'solute', 'solvent', 'T', 'method', 'ln_gamma_inf', 'split']
    missing = set(required) - set(df)
    if missing: raise ValueError(f'missing observation identity fields: {sorted(missing)}')
    payload = [json.dumps([scalar(v) for v in row], separators=(',', ':'))
               for row in df[required].itertuples(index=False, name=None)]
    base = pd.Series([hashlib.sha256(p.encode()).hexdigest() for p in payload], index=df.index)
    if prediction in df:
        for _, idx in base.groupby(base).groups.items():
            vals = df.loc[idx, prediction].to_numpy(float)
            if len(vals) > 1 and not np.all((vals == vals[0]) | (np.isnan(vals) & np.isnan(vals[0]))):
                raise ValueError('indistinguishable duplicate observations have different predictions; attach original row IDs')
    occ = base.groupby(base).cumcount().astype(str)
    return (base + ':' + occ).to_numpy(str)

def keyed(df):
    df = df.reset_index(drop=True).copy()
    df['r3_row_id'] = row_ids(df)
    return df.set_index('r3_row_id', drop=False)

def select_split(df, split):
    if df['split'].isna().any(): raise ValueError('missing split labels are not a test set')
    if not df['split'].isin(['train', 'test_one', 'test_both']).all():
        raise ValueError('unexpected split labels; use a separately declared manifest')
    if split == 'all': return df
    if split == 'test': return df[df['split'] != 'train']
    if split in ('train', 'test_one', 'test_both'): return df[df['split'] == split]
    raise ValueError(split)

def system_ids(df):
    a, b = df.solute.to_numpy(str), df.solvent.to_numpy(str)
    return np.where(a < b, a + '|' + b, b + '|' + a)

def cluster_ci(values, systems, seed=7, repeats=1000):
    """Mean of row values; pairs, rather than rows, are resampled."""
    values = np.asarray(values, float)
    if not len(values): return None
    u, inv = np.unique(np.asarray(systems, str), return_inverse=True)
    groups = [np.flatnonzero(inv == j) for j in range(len(u))]
    rng = np.random.default_rng(seed)
    means = [float(values[np.concatenate([groups[j] for j in rng.integers(len(u), size=len(u))])].mean())
             for _ in range(repeats)]
    return np.quantile(means, [.025, .975]).tolist()

def read_sigma(path):
    path = Path(path)
    lines = path.read_text().splitlines()
    if not lines or not lines[0].startswith('# meta: '): raise ValueError(f'invalid profile header: {path}')
    meta = json.loads(lines[0][8:]); a = np.loadtxt(path)
    if a.shape != (153, 2) or not np.isfinite(a).all(): raise ValueError(f'invalid profile: {path}')
    grid, p = a[:, 0].reshape(3,51), a[:,1].reshape(3,51)
    if not np.allclose(grid, np.linspace(-.025,.025,51)[None,:], atol=1e-12, rtol=0):
        raise ValueError('sigma grid changed')
    if (p < 0).any() or p.sum() <= 0 or not np.isfinite(meta['volume [A^3]']) or meta['volume [A^3]'] <= 0:
        raise ValueError('nonphysical profile')
    return grid[0], p, meta

def profile_descriptors(path):
    s, p, m = read_sigma(path); A = float(p.sum()); normalized = p / A
    out = dict(area_A2=A, volume_A3=float(m['volume [A^3]']),
               normalization=1., net_sigma_moment=float((p*s).sum()),
               sigma_second_moment=float((normalized*s*s).sum()),
               tail_area_A2=float(p[:,abs(s)>=.01].sum()),
               flag=m.get('disp. flag'), averaging=m.get('averaging'),
               r_av_A=m.get('r_av [A]'), f_decay=m.get('f_decay'),
               source_sha256=digest(path))
    for j, block in enumerate(('NHB','OH','OT')):
        out[block+'_area_A2'] = float(p[j].sum())
    return out

def write_sigma(path, sigma, p, meta):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w') as f:
        f.write('# meta: ' + json.dumps(meta, allow_nan=False) + '\n')
        f.write('# sigma [e/A^2] psigmaA [A^2]; NHB, OH, OT\n')
        for block in p:
            for s, a in zip(sigma, block): f.write(f'{s:.3f} {a:.14e}\n')

def rotations():
    from scipy.spatial.transform import Rotation
    # First eight reproduce S2 exactly; r8..r15 are a predeclared extension, not a redraw.
    ans = {'id': np.eye(3), 'repeat': np.eye(3)}
    ans.update({f'r{i}': q for i,q in enumerate(Rotation.random(16, random_state=20261004).as_matrix())})
    axis=np.array([1.,2.,3.]); axis/=np.linalg.norm(axis)
    for label, angle in [('a001',.001),('a01',.01),('a1',.1),('a5',.5),('a10',1.)]:
        ans[label]=Rotation.from_rotvec(angle*axis).as_matrix()
    ans['cube90']=Rotation.from_euler('x',90,degrees=True).as_matrix()
    return ans

def canonical_xyz(x, weights=None):
    """Proper, fixed-atom-order body frame; degenerate inertia uses molecular anchors.

    This does NOT claim chemical atom-permutation canonicalization. Centering and
    reorientation change the finite quadrature and are an A protocol.
    """
    x=np.asarray(x,float)
    if x.ndim!=2 or x.shape[1]!=3 or not np.isfinite(x).all(): raise ValueError('invalid coordinates')
    w=np.ones(len(x)) if weights is None else np.asarray(weights,float)
    if w.shape!=(len(x),) or (w<=0).any(): raise ValueError('invalid weights')
    y=x-np.average(x,axis=0,weights=w)
    I=np.eye(3)*np.sum(w[:,None]*y*y)-(y*w[:,None]).T@y
    vals, vecs=np.linalg.eigh(I)
    def choose(scores):
        # Atom-index tie breaking is invariant to rotation within this relative tolerance.
        mx=float(np.max(scores)); tol=1e-10*max(mx,1.)
        return int(np.flatnonzero(scores>=mx-tol)[0])
    if np.max(np.linalg.norm(y,axis=1)) < 1e-12: return np.zeros_like(y)
    separated=np.min(np.diff(vals))>1e-8*max(float(np.max(abs(vals))),1.)
    if separated:
        e1,e2=vecs[:,0].copy(),vecs[:,1].copy()
        for e in (e1,e2):
            pr=y@e; j=choose(abs(pr))
            if pr[j]<0: e*=-1
    else:
        e1=y[choose(np.sum(y*y,axis=1))].copy(); e1/=np.linalg.norm(e1)
        ort=y-np.outer(y@e1,e1); j=choose(np.sum(ort*ort,axis=1))
        if np.linalg.norm(ort[j])<1e-10:
            return np.c_[y@e1,np.zeros((len(y),2))]  # Linear molecules, no arbitrary transverse axis.
        e2=ort[j]/np.linalg.norm(ort[j])
    e3=np.cross(e1,e2); e3/=np.linalg.norm(e3); e2=np.cross(e3,e1)
    return y@np.column_stack([e1,e2,e3])
