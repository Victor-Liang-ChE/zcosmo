"""Round-5 read-only experiment utilities. No production model is patched."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from r3_common import digest, read_sigma, write_json, STALL_KEYS

BASE = '69b49116c2ae7574d7ae471f0a4ed7ba33d0db8b'
PANEL = (
 ('water','O'), ('methanol','CO'), ('ethylene_glycol','OCCO'),
 ('diethylene_glycol','OCCOCCO'), ('triethylene_glycol','OCCOCCOCCO'),
 ('tetraethylene_glycol','OCCOCCOCCOCCO'), ('glycerol','OCC(O)CO'),
 ('propylene_glycol','CC(O)CO'), ('methoxyethanol','COCCO'),
 ('dimethoxyethane','COCCOC'), ('tetrahydrofuran','C1CCOC1'),
 ('nonane','CCCCCCCCC'))


def fresh(path):
    p=Path(path).resolve()
    if p.exists(): raise FileExistsError(f'use a new output path: {p}')
    p.mkdir(parents=True)
    return p


def require_registration(value):
    if not str(value).strip(): raise ValueError('record the prospective registration identifier')
    return str(value)


def fingerprint(paths):
    return {str(Path(p).resolve()):digest(p) for p in paths}


def check_fingerprint(record):
    for p,h in record.items():
        if digest(p)!=h: raise ValueError(f'input changed: {p}')


def canonical_smiles(s):
    from rdkit import Chem
    m=Chem.MolFromSmiles(s)
    if m is None: raise ValueError(s)
    return Chem.MolToSmiles(m,isomericSmiles=True)


def align(x, reference, indices=None):
    """Proper Kabsch alignment in the fixed atom order; not atom permutation."""
    x=np.asarray(x,float); y=np.asarray(reference,float)
    if x.shape!=y.shape or x.ndim!=2 or x.shape[1]!=3: raise ValueError('coordinate mismatch')
    if not np.isfinite(x).all() or not np.isfinite(y).all(): raise ValueError('nonfinite coordinates')
    ii=np.arange(len(x)) if indices is None else np.asarray(indices,int)
    a=x[ii].mean(0);b=y[ii].mean(0)
    u,_,vt=np.linalg.svd((x[ii]-a).T@(y[ii]-b))
    d=np.ones(3);d[-1]=1. if np.linalg.det(u@vt)>=0 else -1.
    return (x-a)@(u@np.diag(d)@vt)+b


def rmsd(x,y,indices=None):
    ii=np.arange(len(x)) if indices is None else np.asarray(indices,int)
    return float(np.sqrt(np.mean(np.sum((align(x,y,ii)[ii]-np.asarray(y)[ii])**2,axis=1))))


def charge_average(xyz_A, area_A2, sigma, subdivision=1., block=128):
    """Hsieh formula; infinity is an A point-patch-limit sensitivity, not a new default.

    subdivision m is algebraically the result of replacing each patch by m
    coincident patches with A/m and q/m. It is not a physical surface remesh.
    """
    x=np.asarray(xyz_A,float);a=np.asarray(area_A2,float);s=np.asarray(sigma,float)
    if x.shape!=(len(a),3) or s.shape!=a.shape or np.any(a<=0): raise ValueError('invalid segments')
    if not (np.isfinite(x).all() and np.isfinite(a).all() and np.isfinite(s).all()): raise ValueError('nonfinite segments')
    if subdivision not in (1.,4.,np.inf): raise ValueError('fixed diagnostic subdivisions are 1, 4, infinity')
    rav2=7.25/np.pi; rn2=np.zeros_like(a) if np.isinf(subdivision) else a/(np.pi*subdivision)
    # Constants independent of j cancel between numerator and denominator.
    pref=a/(rn2+rav2);out=np.empty_like(s)
    for lo in range(0,len(a),block):
        w=np.exp(-3.57*cdist(x[lo:lo+block],x,'sqeuclidean')/(rn2+rav2))*pref
        out[lo:lo+block]=(w@s)/w.sum(1)
    return out


def bin_linear(sigma, area, grid):
    """Independent mass/first-moment preserving interpolation; no clipping."""
    s=np.asarray(sigma,float);a=np.asarray(area,float);g=np.asarray(grid,float)
    if s.shape!=a.shape or np.any(a<0) or not np.isfinite(s).all(): raise ValueError('invalid bin inputs')
    if np.any(s<g[0]-1e-12) or np.any(s>g[-1]+1e-12): raise ValueError('out-of-range sigma, do not clip')
    # Tiny endpoint roundoff only. A genuinely out-of-range value already failed.
    s=np.minimum(np.maximum(s,g[0]),g[-1]);j=np.searchsorted(g,s,side='right')-1
    j=np.minimum(j,len(g)-2);t=(s-g[j])/(g[j+1]-g[j]);p=np.zeros_like(g)
    np.add.at(p,j,a*(1-t));np.add.at(p,j+1,a*t)
    return p


def observation_ids(df, table):
    """Identity from source observations only, independent of predictions and row order."""
    required={'idac':['file','dataset','solute','solvent','T','ln_gamma_inf','split'],
              'vle':['file','dataset','c1','c2','T','x1','P','split'],
              'he':['file','dataset','c1','c2','T','x1','HE_J','split'],
              'lle':['file','dataset','c1','c2','T','x1','split']}[table]
    if set(required)-set(df): raise ValueError(f'{table}: missing identity fields {set(required)-set(df)}')
    cols=required+[c for c in ('year','method','gamma_inf','y1','P','temporal') if c in df and c not in required]
    def value(v):
        if pd.isna(v): return None
        if isinstance(v,(float,np.floating)): return format(float(v),'.15g')
        return str(v)
    keys=pd.Series([hashlib.sha256(json.dumps([value(v) for v in row],separators=(',',':')).encode()).hexdigest()
                    for row in df[cols].itertuples(index=False,name=None)],index=df.index)
    return (keys+':'+keys.groupby(keys).cumcount().astype(str)).to_numpy()


def pairs(df,table):
    return ('solute','solvent') if table=='idac' else ('c1','c2')


def systems(df,table):
    a,b=pairs(df,table);x=df[a].to_numpy(str);y=df[b].to_numpy(str)
    return np.where(x<y,x+'|'+y,y+'|'+x)


def subset(df, split):
    if df['split'].isna().any() or not df['split'].isin(['train','test_one','test_both']).all():
        raise ValueError('invalid split labels')
    return df if split=='all' else df[df['split']!='train'] if split=='test' else df[df['split']==split]
