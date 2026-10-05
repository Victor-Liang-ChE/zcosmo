"""Explicit numeric gates; no experimental response values are loaded here."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from r3_common import read_sigma,write_json

def paired(reference,candidate,model):
    r=pd.read_csv(reference).set_index('query'); c=pd.read_csv(candidate).set_index('query')
    if not r.index.is_unique or not c.index.is_unique or set(r.index)!=set(c.index): raise ValueError('query mismatch')
    if len(r)!=2302: raise ValueError('expected historical 2302 occurrences')
    c=c.loc[r.index]; x=r[model].to_numpy(float); y=c[model].to_numpy(float); ok=np.isfinite(x)
    if not np.array_equal(ok,np.isfinite(y)) or not ok.any(): raise ValueError('changed or empty finite coverage')
    return r,c,ok,abs(y[ok]-x[ok])

def profiles(a):
    r,c,ok,dc=paired(a.reference,a.candidate,'cosmosac_dsp')
    _,_,_,dz=paired(a.reference,a.candidate,'Z0x')
    ud=pd.read_csv(a.ud).set_index('query')
    if set(ud.index)!=set(r.index): raise ValueError('UD query mismatch')
    u=ud.loc[r.index,'cosmosac_dsp'].to_numpy(float); y=c.cosmosac_dsp.to_numpy(float)
    uu=ok&np.isfinite(u)
    if not uu.any(): raise ValueError('UD comparison empty')
    max_raw=0.;max_norm=0.;max_area=0.;max_vol=0.
    keys=sorted(r.key.unique())
    if len(keys)!=25: raise ValueError('expected 25 keys')
    for k in keys:
        _,p,pm=read_sigma(Path(a.reference_dir)/f'{k}.sigma')
        _,q,qm=read_sigma(Path(a.candidate_dir)/f'{k}.sigma')
        max_raw=max(max_raw,float(abs(p-q).max()));max_norm=max(max_norm,float(abs(p/p.sum()-q/q.sum()).max()))
        max_area=max(max_area,float(abs(p.sum()-q.sum())));max_vol=max(max_vol,abs(pm['volume [A^3]']-qm['volume [A^3]']))
    med=float(np.median(abs(y[uu]-u[uu])))
    passed=bool(max_raw<1e-4 and max_norm<1e-4 and dc.max()<1e-3 and dz.max()<1e-3) if a.mode=='E' else bool(dc.max()<a.max_change and med<.15)
    report=dict(mode=a.mode,keys=25,rows=2302,finite_cosmosac=int(ok.sum()),UD_comparisons=int(uu.sum()),
        max_delta_lngamma_cosmosac=float(dc.max()),max_delta_lngamma_Z0x=float(dz.max()),median_cosmosac_vs_UD=med,
        max_raw_bin_A2=max_raw,max_normalized_bin=max_norm,max_area_A2=max_area,max_volume_A3=max_vol,passed=passed)
    write_json(a.out,report)
    if not passed: raise SystemExit('profile numeric gate failed; nothing is adopted')

def stability(a):
    _,_,_,b=paired(a.reference,a.reference_other,a.model)
    _,_,_,c=paired(a.candidate,a.candidate_other,a.model)
    bm=float(b.max());cm=float(c.max())
    passed=cm<a.bound and (a.ratio is None or cm<=a.ratio*bm)
    write_json(a.out,dict(model=a.model,reference_max=bm,candidate_max=cm,bound=a.bound,ratio=a.ratio,passed=bool(passed)))
    if not passed: raise SystemExit('stability gate failed')

def panel(a):
    b=json.loads(Path(a.reference).read_text()); c=json.loads(Path(a.candidate).read_text())
    if not b['coverage_pass'] or not c['coverage_pass']: raise ValueError('coverage failed')
    result=[]
    for model in ('cosmosac_dsp','Z0x'):
        maxima=[]
        for doc in (b,c):
            rows=[r for r in doc['summaries'] if r['model']==model and 'role' not in r and r['label'] in [f'r{i}' for i in range(8)]]
            if len(rows)!=8 or len({r['label'] for r in rows})!=8 or any(r['max_abs'] is None for r in rows): raise ValueError('requires all eight fixed rotations')
            maxima.append(max(r['max_abs'] for r in rows))
        bm,cm=maxima
        result.append(dict(model=model,reference_max=bm,candidate_max=cm,passed=bool(cm<a.bound and (a.ratio is None or cm<=a.ratio*bm))))
    write_json(a.out,dict(bound=a.bound,ratio=a.ratio,results=result))
    if not all(r['passed'] for r in result): raise SystemExit('orientation panel gate failed')

def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
    q=s.add_parser('profiles')
    for name in ('reference','candidate','ud','reference-dir','candidate-dir','out'): q.add_argument('--'+name,required=True)
    q.add_argument('--mode',choices=['E','A'],required=True);q.add_argument('--max-change',type=float,default=.05)
    q=s.add_parser('stability')
    for name in ('reference','reference-other','candidate','candidate-other','out'):q.add_argument('--'+name,required=True)
    q.add_argument('--bound',type=float,required=True);q.add_argument('--ratio',type=float)
    q.add_argument('--model',choices=['cosmosac_dsp','Z0x'],default='cosmosac_dsp')
    q=s.add_parser('panel')
    for name in ('reference','candidate','out'):q.add_argument('--'+name,required=True)
    q.add_argument('--bound',type=float,required=True);q.add_argument('--ratio',type=float)
    a=p.parse_args();globals()[a.cmd](a)
if __name__=='__main__':main()
