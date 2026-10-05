"""LLE quality accounting and an opt-in A numerical repair, separate from production.

No unresolved call is converted to 'miscible'. Grid tests are never certificates
of global stability or absence of narrower gaps. Original predictions are retained.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import time
import numpy as np
import pandas as pd
from scipy.optimize import least_squares
from r3_common import digest,write_json

RESIDUAL=1e-7
MARGIN=1e-7


def call_key(r):
    return (str(r['model']),str(r['c1']),str(r['c2']),float(r.get('binodal_T',r.get('T'))))


def load_records(path):
    path=Path(path);files=sorted(path.rglob('*.jsonl')) if path.is_dir() else [path]
    if not files: raise FileNotFoundError(path)
    out={};duplicates=0
    for p in files:
        for line in p.read_text().splitlines():
            if not line.strip(): continue
            r=json.loads(line);k=call_key(r)
            if k in out:
                if out[k]!=r: raise ValueError(f'conflicting repeated audit record: {k}')
                duplicates+=1
            out[k]=r
    if not out: raise ValueError('empty sidecar')
    return out,dict(files=[dict(path=str(p.resolve()),sha256=digest(p)) for p in files],identical_duplicates=duplicates)


def quality(r):
    if r['status']=='no_gap_on_grid': return 0.,'no_gap_on_81_grid'
    if r['status']!='refined_root': return np.nan,r['status']
    residual=r.get('residual_max');margin=r.get('sampled_tangent_margin');b=r.get('returned')
    if not isinstance(b,(list,tuple)) or len(b)!=2 or not 0<b[0]<b[1]<1 or b[1]-b[0]<=1e-4:
        return np.nan,'invalid_endpoints'
    if residual is None or not np.isfinite(residual) or residual>=RESIDUAL: return np.nan,'residual_failed'
    if margin is None or not np.isfinite(margin): return np.nan,'tangent_unchecked'
    if margin < -MARGIN: return np.nan,'negative_tangent_margin'
    return 1.,'root_passes_sampled_checks'


def bounds(decisions,systems):
    """Keep every row and the original >1/2 per-system aggregation."""
    d=np.asarray(decisions,float);systems=np.asarray(systems,str)
    if len(d)!=len(systems) or not len(d): raise ValueError('empty or inconsistent denominator')
    if not np.isin(d[np.isfinite(d)],[0.,1.]).all(): raise ValueError('invalid nullable decision')
    low=np.nan_to_num(d,nan=0.);high=np.nan_to_num(d,nan=1.)
    u=np.unique(systems)
    return dict(rows=len(d),systems=len(u),unresolved_rows=int(np.isnan(d).sum()),
        row_gap_found_bounds=[float(low.mean()),float(high.mean())],
        system_gap_found_bounds=[float(np.mean([low[systems==s].mean()>.5 for s in u])),
                                 float(np.mean([high[systems==s].mean()>.5 for s in u]))],
        interpretation='Bounds for this finite-grid quality screen, not certified thermodynamic bounds.')


def lower_gaps(xs,g):
    hull=[]
    for i in range(len(xs)):
        while len(hull)>=2:
            j,k=hull[-2:]
            if (xs[k]-xs[j])*(g[i]-g[j])-(g[k]-g[j])*(xs[i]-xs[j])<=0: hull.pop()
            else: break
        hull.append(i)
    return [(xs[i],xs[j]) for i,j in zip(hull[:-1],hull[1:]) if j-i>1]


class BudgetExceeded(RuntimeError): pass


def strict_binodal(model,T,budget=4000):
    """Bounded numerical repair. No clipping inside equations; reject trivial roots."""
    cache={};calls=0;history=[];witness=None
    def unresolved(reason):
        return dict(status='gap_witness_only' if witness else 'unresolved',reason=reason,
                    history=history,model_calls=calls,nonconvex_witness=witness,globally_certified=False)
    def lg(x):
        nonlocal calls
        x=float(x)
        if not 0<x<1: raise ValueError('composition outside open interval')
        if x not in cache:
            if calls>=budget: raise BudgetExceeded('model-call budget exhausted')
            calls+=1;y=np.asarray(model.lngamma(T,np.array([x,1-x])),float)
            if y.shape!=(2,) or not np.isfinite(y).all(): raise ValueError('nonfinite model')
            cache[x]=y
        return cache[x]
    def mu(x): return np.log([x,1-x])+lg(x)
    try:
        for n in (81,161,321):
            xs=np.unique(np.r_[np.logspace(-8,-2,14),np.linspace(.02,.98,n),1-np.logspace(-2,-8,14)])
            m=np.array([mu(x) for x in xs]);g=np.sum(np.c_[xs,1-xs]*m,axis=1)
            gaps=lower_gaps(xs,g)
            for a,b in gaps:
                ia,ib=np.searchsorted(xs,[a,b]);inside=np.arange(ia+1,ib)
                if not len(inside): continue
                chord=g[ia]+(g[ib]-g[ia])*(xs[inside]-a)/(b-a)
                j=int(inside[np.argmax(g[inside]-chord)])
                depth=float(g[j]-(g[ia]+(g[ib]-g[ia])*(xs[j]-a)/(b-a)))
                if depth>1e-7 and (witness is None or depth>witness['depth']):
                    witness=dict(x=[float(a),float(xs[j]),float(b)],g=[float(g[ia]),float(g[j]),float(g[ib])],depth=depth)
            if len(gaps)>4: return unresolved('more than four sampled gaps')
            roots=[];failures=[]
            for initial in gaps:
                mid=sum(initial)/2;sep=min(1e-8,(initial[1]-initial[0])/8)
                lb=[1e-10,mid+sep];ub=[mid-sep,1-1e-10]
                def eq(v): return mu(v[0])-mu(v[1])
                opt=least_squares(eq,np.asarray(initial),bounds=(lb,ub),
                    xtol=1e-12,ftol=1e-12,gtol=1e-12,max_nfev=120,diff_step=1e-6)
                a,b=map(float,opt.x);ma,mb=mu(a),mu(b);res=float(abs(ma-mb).max())
                plane=(ma+mb)/2;margin=float(np.min(g-(np.c_[xs,1-xs]@plane)))
                valid=bool(res<RESIDUAL and margin>=-MARGIN and b-a>1e-4)
                r=dict(x=[a,b],residual=res,sampled_tangent_margin=margin,
                       solver_success=bool(opt.success),accepted=valid)
                (roots if valid else failures).append(r)
            roots.sort(key=lambda r:r['x'][0])
            history.append(dict(n=n,sampled_points=len(xs),sampled_gaps=len(gaps),roots=roots,failures=failures))
        previous,last=history[-2:]
        if previous['failures'] or last['failures']:
            return unresolved('refinement/stability check failed')
        p,q=previous['roots'],last['roots']
        stable=len(p)==len(q) and all(np.max(abs(np.asarray(a['x'])-b['x']))<5e-5 for a,b in zip(p,q))
        if not stable: return unresolved('grid refinement changed roots')
        if not q and witness: return unresolved('positive nonconvexity witness without checked endpoints')
        if not q:
            return dict(status='no_gap_on_refined_grid',roots=[],history=history,model_calls=calls,
                        globally_certified=False)
        return dict(status='root_passes_refined_sampled_checks',roots=q,history=history,model_calls=calls,
                    globally_certified=False,nonconvex_witness=witness)
    except (BudgetExceeded,ValueError,RuntimeError,FloatingPointError) as e:
        return unresolved(repr(e))


def audit(a):
    calls,provenance=load_records(a.sidecars)
    repairs,rprov=load_records(a.repairs) if a.repairs else ({},None)
    d=pd.read_csv(a.predictions).reset_index(drop=True)
    if d['split'].isna().any(): raise ValueError('missing split labels')
    if a.split=='test': d=d[d['split']!='train'].copy()
    elif a.split=='train':d=d[d['split']=='train'].copy()
    if not len(d): raise ValueError('empty requested split')
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True);rows=[];used=set();unknown={}
    for index,r in d.iterrows():
        key=(a.model,str(r.c1),str(r.c2),float(round(float(r['T'])/2)*2))
        if key not in calls: raise ValueError(f'missing audit call for prediction row: {key}')
        c=calls[key];used.add(key);b=c.get('returned')
        pv=r.pred_split
        if not isinstance(pv,(bool,np.bool_)): raise ValueError('pred_split must be Boolean, not strings or NaN')
        if bool(pv)!=(b is not None): raise ValueError('sidecar and prediction disagree')
        if b is not None and not np.allclose([r.pred_x1_I,r.pred_x1_II],b,rtol=0,atol=1e-12):
            raise ValueError('sidecar endpoint mismatch')
        decision,status=quality(c);xy=b
        if key in repairs:
            repair=repairs[key]
            if repair.get('reference_call_sha256')!=hashlib.sha256(json.dumps(c,sort_keys=True).encode()).hexdigest():
                raise ValueError('repair belongs to a different reference call')
            status=repair['status']
            if status=='root_passes_refined_sampled_checks':
                decision=1.;xy=max(repair['roots'],key=lambda q:q['x'][1]-q['x'][0])['x']
            elif status=='gap_witness_only': decision=1.;xy=None
            elif status=='no_gap_on_refined_grid': decision=0.;xy=None
            else: decision=np.nan;xy=None
        if not np.isfinite(decision):
            unknown[key]=dict(model=key[0],c1=key[1],c2=key[2],binodal_T=key[3],status=status)
        rows.append(dict(original_row_index=int(index),r4_split=decision,r4_status=status,
            r4_x1_I=xy[0] if decision==1. and xy is not None else np.nan,r4_x1_II=xy[1] if decision==1. and xy is not None else np.nan,
            call_key=json.dumps(key)))
    q=pd.DataFrame(rows,index=d.index);result=pd.concat([d,q],axis=1)
    result.to_csv(out/'quality_rows.csv',index=False)
    pd.DataFrame(list(unknown.values()),columns=['model','c1','c2','binodal_T','status']).to_csv(out/'unresolved_calls.csv',index=False)
    systems=np.where(d.c1.to_numpy(str)<d.c2.to_numpy(str),d.c1+'|'+d.c2,d.c2+'|'+d.c1)
    summary=bounds(q.r4_split,systems)
    relevant=[calls[k] for k in used]
    summary.update(model=a.model,split=a.split,unique_calls=len(used),legacy_gap_found_rows=float(d.pred_split.mean()),
        statuses=q.r4_status.value_counts().to_dict(),source_sha256=digest(a.predictions),sidecar_inputs=provenance,
        repairs=rprov,negative_margin_calls_raw=sum(c.get('sampled_tangent_margin',0) is not None and c.get('sampled_tangent_margin',0)<0 for c in relevant),
        note='Primary prediction columns are unchanged. Do not pass nullable r4_split to metrics.lle_rows or astype(bool).')
    good=(q.r4_split==1.) & np.isfinite(q[['r4_x1_I','r4_x1_II']].to_numpy()).all(1)
    if good.any():
        err=np.minimum(abs(d.loc[good,'x1']-q.loc[good,'r4_x1_I']),abs(d.loc[good,'x1']-q.loc[good,'r4_x1_II']))
        summary['composition_MAE_on_checked_detections']=float(err.mean());summary['composition_MAE_denominator']=int(good.sum())
    write_json(out/'summary.json',summary)


def repair(a):
    if not a.registration: raise ValueError('prospective registration identifier required')
    calls,prov=load_records(a.sidecars);todo=pd.read_csv(a.calls)
    if todo.empty: raise ValueError('no unresolved calls selected')
    if a.background: os.environ['ZC_SIGMA_OVERRIDE_DIR']=str(Path(a.background).resolve())
    else: os.environ.pop('ZC_SIGMA_OVERRIDE_DIR',None)
    from zcosmo.models import make_model
    from zcosmo.evaluate import binodal
    from zcosmo.cosmosac import sigma_path
    compounds=pd.read_csv(a.compounds);smi=dict(zip(compounds.inchikey,compounds.smiles))
    path=Path(a.out)
    if path.exists(): raise FileExistsError(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w') as f:
        for r in todo.itertuples():
            key=(r.model,r.c1,r.c2,float(r.binodal_T));reference=calls[key]
            model=make_model(r.model,[r.c1,r.c2],[smi[r.c1],smi[r.c2]])
            used={}
            for k in (r.c1,r.c2):
                pp=sigma_path(k)
                if pp is None: raise FileNotFoundError(k)
                used[k]=dict(path=str(pp.resolve()),sha256=digest(pp))
            replay=binodal(model,float(r.binodal_T));old=reference['returned']
            if (replay is None)!=(old is None) or (old is not None and not np.allclose(replay,old,rtol=0,atol=1e-8)):
                raise ValueError('legacy replay disagrees: freeze the correct profile/data/model source first')
            model=make_model(r.model,[r.c1,r.c2],[smi[r.c1],smi[r.c2]])
            t=time.perf_counter();answer=strict_binodal(model,float(r.binodal_T),budget=4000)
            answer['profile_inputs']=used
            answer.update(model=r.model,c1=r.c1,c2=r.c2,binodal_T=float(r.binodal_T),
                registration=a.registration,wall_s=time.perf_counter()-t,
                reference_call_sha256=hashlib.sha256(json.dumps(reference,sort_keys=True).encode()).hexdigest())
            f.write(json.dumps(answer,allow_nan=False)+'\n');f.flush()
    write_json(str(path)+'.inputs.json',dict(sidecars=prov,calls_sha256=digest(a.calls),
        registration=a.registration,global_certification=False,
        model_inputs={p:digest(p) for p in ('src/zcosmo/evaluate.py','src/zcosmo/z0x.py',
            'src/zcosmo/cosmosac.py','results/z_params/Z0.json',
            'results/qc/dielectric.csv','results/qc/dispersion.csv')}))


def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
    q=s.add_parser('audit');q.add_argument('--sidecars',required=True);q.add_argument('--predictions',required=True)
    q.add_argument('--model',default='Z0x');q.add_argument('--split',choices=['all','test','train'],default='test')
    q.add_argument('--repairs');q.add_argument('--out',required=True)
    q=s.add_parser('repair');q.add_argument('--sidecars',required=True);q.add_argument('--calls',required=True)
    q.add_argument('--compounds',default='data/benchmark/compounds.csv');q.add_argument('--background');q.add_argument('--registration',required=True);q.add_argument('--out',required=True)
    a=p.parse_args();globals()[a.cmd](a)
if __name__=='__main__':main()
