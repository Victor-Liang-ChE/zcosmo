"""All-row endpoint audit. No experimental response is passed to a worker.

Four source arms: UD, open630, open636, and the declared water-shape stress arm.
Missing and excluded rows remain explicit. Nothing is scored or adopted here.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import numpy as np
import pandas as pd
from scipy.special import logsumexp
from scipy.optimize import root
from r6_common import BASE, sha, write, fresh, registration, check_inputs

HS=(1e-4,1e-5,1e-6,1e-7,1e-8)


def log_reference(E, p):
    """Independent residual/Jacobian polish of the strictly convex log-state problem.

    Structural zeros are kept. Positive bins are never thresholded.
    """
    from zcosmo.cosmosac import solve_gamma
    E=np.asarray(E,float);p=np.asarray(p,float)
    if not np.isfinite(E).all() or (E<=0).any() or not np.isfinite(p).all() or (p<0).any():
        raise ValueError('nonpositive/invalid kernel or profile')
    ix=np.flatnonzero(p>0)
    if not len(ix):raise ValueError('empty profile')
    le=np.log(E[:,ix])+np.log(p[ix])[None,:]
    start=np.log(solve_gamma(E,p))[ix]
    def fun(y):return y+logsumexp(le[ix]+y[None,:],axis=1)
    def jac(y):
        z=le[ix]+y[None,:];return np.eye(len(ix))+np.exp(z-logsumexp(z,axis=1)[:,None])
    sol=root(fun,start,jac=jac,method='hybr',options={'xtol':1e-11})
    y=sol.x
    residual=float(abs(fun(y)).max())
    # The equation residual decides numerical convergence, not only MINPACK's flag.
    if residual>5e-12:raise RuntimeError(f'independent segment residual {residual}')
    full=-logsumexp(le+y[None,:],axis=1)
    return full,residual


def reference_value(model,T,x1,parts=False):
    from zcosmo.cosmosac import Mixture
    mix=Mixture(model.keys,model.z0.with_(A_ES=model._c(x1)))
    x=np.array([x1,1-x1]);pa=np.array([f.psigA.ravel() for f in mix.fl])
    E=mix._E(T);ym,rm=log_reference(E,(x@pa)/(x@mix.A))
    yi=[];res=[rm]
    for p in pa:
        y,r=log_reference(E,p/p.sum());yi.append(y);res.append(r)
    resid=np.sum(pa*(ym-np.asarray(yi)),axis=1)/mix.prm.aeff
    components=np.array([mix.lngamma_comb(x),resid,mix.lngamma_disp(x,T)])
    if not np.isfinite(components).all():raise ValueError('nonfinite independent endpoint')
    return (components if parts else components.sum(0)), max(res)


def fresh_stencils(model,T):
    """Three-point one-sided derivative of g, with c rebuilt exactly at every x.

    Richardson columns are diagnostics; round-off amplification is reported.
    """
    cache={0.:0.};values={}
    for h in HS:
        for x in (h,2*h):
            if x not in cache:
                v,_=reference_value(model,T,x)
                cache[x]=float(np.array([x,1-x])@v)
        values[f'fd2_{h:g}']=(4*cache[h]-cache[2*h])/(2*h)
    return values


def prepare(a):
    from r5_scorecard import freeze
    from r3_common import WATER,read_sigma,write_sigma
    out=fresh(a.out);reg=registration(a.registration)
    freeze(argparse.Namespace(out=str(out/'assets'),profile_root=a.profile_root,registration=reg))
    cfg=json.loads((out/'assets/config.json').read_text())
    d=pd.read_csv(cfg['universe']['idac']['path'])
    # Remove responses before handing any data to numerical acceptance workers.
    q=d[['r5_row_id','solute','solvent','T','split']].copy()
    q.to_csv(out/'queries.csv',index=False)
    from zcosmo.cosmosac import sigma_path
    os.environ.pop('ZC_SIGMA_OVERRIDE_DIR',None)
    water=sigma_path(WATER)
    if water is None:raise FileNotFoundError(WATER)
    p=out/'water_stress';p.mkdir()
    background=Path(cfg['overlays']['open636'])
    for f in background.glob('*.sigma'):
        if f.stem!=WATER:(p/f.name).symlink_to(f.resolve())
    s,po,meta=read_sigma(background/(WATER+'.sigma'));_,pu,_=read_sigma(water)
    meta.update(source='R6 diagnostic UD water shape at fixed open area and volume, not adopted')
    write_sigma(p/(WATER+'.sigma'),s,pu/pu.sum()*po.sum(),meta)
    inputs=dict(cfg['inputs']);inputs.update(cfg['open_inputs']);inputs.update(cfg['UD_inputs'])
    for source in ('scripts/r6_endpoint.py','scripts/r6_common.py'):
        inputs[str(Path(source).resolve())]=sha(source)
    inputs[str((out/'queries.csv').resolve())]=sha(out/'queries.csv')
    inputs[str((p/(WATER+'.sigma')).resolve())]=sha(p/(WATER+'.sigma'))
    write(out/'config.json',dict(base=BASE,registration=reg,rows=str(out/'queries.csv'),
          variants={'UD':None,'open630':cfg['overlays']['open630'],'open636':cfg['overlays']['open636'],
                    'water_stress':str(p)},inputs=inputs))


def worker(a):
    cfg=json.loads(Path(a.config).read_text());check_inputs(cfg['inputs'])
    reg=registration(cfg['registration']);directory=cfg['variants'][a.arm]
    os.environ.pop('ZC_SIGMA_OVERRIDE_DIR',None);os.environ.pop('ZC_ONLY_KEYS',None)
    if directory:os.environ['ZC_SIGMA_OVERRIDE_DIR']=directory
    os.environ['ZC_R6_ENDPOINT']='0'
    from zcosmo.z0x import Z0xBinary
    from r3_common import STALL_KEYS
    d=pd.read_csv(cfg['rows']);rows=[];cache={};t0=time.perf_counter()
    for r in d.itertuples():
        q=dict(r5_row_id=r.r5_row_id,solute=r.solute,solvent=r.solvent,T=float(r.T),split=r.split,status='',error='')
        if a.arm=='open630' and (r.solute in STALL_KEYS or r.solvent in STALL_KEYS):
            q['status']='excluded_by_design';rows.append(q);continue
        if directory:
            for k in (r.solute,r.solvent):
                if not (Path(directory)/(k+'.sigma')).is_file():raise FileNotFoundError('No UD fallback: '+k)
        key=(r.solute,r.solvent,float(r.T))
        if key in cache:q.update(cache[key]);rows.append(q);continue
        values={'legacy':np.nan,'candidate':np.nan};errors=[]
        os.environ['ZC_R6_ENDPOINT']='0'
        t=time.perf_counter()
        try:
            m=Z0xBinary([r.solute,r.solvent]);values['legacy']=float(m.lngamma_inf(r.T,0))
        except Exception as ex:errors.append('legacy: '+repr(ex))
        values['legacy_s']=time.perf_counter()-t
        os.environ['ZC_R6_ENDPOINT']='1';t=time.perf_counter();new=None
        try:
            new=Z0xBinary([r.solute,r.solvent]);values['candidate']=float(new.lngamma_inf(r.T,0))
        except Exception as ex:errors.append('candidate: '+repr(ex))
        values['candidate_s']=time.perf_counter()-t
        finite=np.isfinite([values['legacy'],values['candidate']])
        if not finite.any():
            values.update(status='baseline_nonfinite',error='; '.join(errors))
        elif not finite.all():
            values.update(status='coverage_changed',error='; '.join(errors))
        else:
            try:
                ref,res=reference_value(new,r.T,0.);values['reference']=float(ref[0]);values['pure_solvent']=float(ref[1])
                values['reference_residual']=res
                rev=Z0xBinary([r.solvent,r.solute]);values['reverse_error']=abs(float(rev.lngamma_inf(r.T,1))-values['candidate'])
                values['api_error']=abs(float(new.lngamma(r.T,np.array([0.,1.]))[0])-values['candidate'])
                values['change']=values['candidate']-values['legacy']
                values['reference_error']=abs(values['candidate']-values['reference'])
                values.update(fresh_stencils(new,r.T))
                err=np.array([abs(values[f'fd2_{h:g}']-values['reference']) for h in HS])
                values['best_fd2_error']=float(err.min())
                valid=(values['reference_error']<1e-8 and values['reverse_error']<1e-8 and
                       values['api_error']<1e-10 and abs(ref[1])<1e-9)
                values['status']='checked' if valid else 'check_failed'
            except Exception as ex:values.update(status='check_failed',error=repr(ex))
        cache[key]=values;q.update(values);rows.append(q)
    output=pd.DataFrame(rows);output.to_csv(a.out,index=False)
    check_inputs(cfg['inputs'])
    write(str(a.out)+'.json',dict(base=BASE,registration=reg,arm=a.arm,rows=len(output),
          unique_queries=len(cache),wall_s=time.perf_counter()-t0,statuses=output.status.value_counts().to_dict()))


def summarize(a):
    cfg=json.loads(Path(a.config).read_text());check_inputs(cfg['inputs']);result={};passed=True;artifacts={}
    expected=pd.read_csv(cfg['rows']).set_index('r5_row_id')
    from r3_common import STALL_KEYS
    for arm in cfg['variants']:
        d=pd.read_csv(Path(a.out)/(arm+'.csv'))
        if d.r5_row_id.duplicated().any() or set(d.r5_row_id)!=set(expected.index):raise ValueError('missing, extra, or duplicate observation identity')
        d=d.set_index('r5_row_id').loc[expected.index].reset_index()
        for col in ('solute','solvent','split'):
            if list(d[col])!=list(expected[col]):raise ValueError('query labels changed')
        if not np.allclose(d['T'],expected['T'],atol=1e-12,rtol=0):raise ValueError('query temperatures changed')
        excluded=(expected.solute.isin(STALL_KEYS)|expected.solvent.isin(STALL_KEYS)).to_numpy() if arm=='open630' else np.zeros(len(d),bool)
        if not np.array_equal(d.status=='excluded_by_design',excluded):raise ValueError('exclusion policy changed')
        artifacts[str((Path(a.out)/(arm+'.csv')).resolve())]=sha(Path(a.out)/(arm+'.csv'))
        good=d.status=='checked';eligible=d.status!='excluded_by_design'
        # Recheck numerical flags, so a malformed CSV cannot turn a failed result into a pass.
        if good.any():
            g=d.loc[good]
            required=['legacy','candidate','reference','reference_error','reverse_error','api_error','pure_solvent']
            if not np.isfinite(g[required].to_numpy(float)).all():raise ValueError('nonfinite checked result')
            if not ((g.reference_error<1e-8)&(g.reverse_error<1e-8)&(g.api_error<1e-10)&(abs(g.pure_solvent)<1e-9)).all():
                raise ValueError('checked status disagrees with numerical limits')
        nf=d.status=='baseline_nonfinite'
        if nf.any() and np.isfinite(d.loc[nf,['legacy','candidate']].to_numpy(float)).any():
            raise ValueError('nonfinite status disagrees with values')
        # Candidate is evaluated even when legacy failed. Preserve identical nonfinite coverage.
        passed &= bool(d.loc[eligible,'status'].isin(['checked','baseline_nonfinite']).all() and good.any())
        records=[]
        for split in ('all','test'):
            sub=d if split=='all' else d[d['split']!='train'];g=sub[sub.status=='checked']
            rec=dict(split=split,requested=len(sub),checked=len(g),statuses=sub.status.value_counts().to_dict())
            if len(g):
                e=abs(g.change)
                rec.update(mean_abs_change=float(e.mean()),max_abs_change=float(e.max()),
                    counts_above={str(t):int((e>t).sum()) for t in (1e-3,1e-2,.05,.1)},
                    max_reference_error=float(g.reference_error.max()),
                    fd2_inconclusive_rows=int((g.best_fd2_error>=1e-5).sum()))
            records.append(rec)
        result[arm]=records
        for role in ('solute','solvent'):
            d[d.status=='checked'].groupby(role)['change'].agg(['count','mean','min','max']).to_csv(Path(a.out)/(arm+'-'+role+'s.csv'))
    write(Path(a.out)/'gate.json',dict(base=BASE,registration=cfg['registration'],
          numerical_gate=passed,arms=result,experimental_response_used=False,
          config_sha256=sha(a.config),audit_csv_inputs=artifacts,
          meaning='A numerical correction of the same endpoint model; historical scores stay unchanged.'))
    if not passed:raise SystemExit(2)


def run(a):
    out=fresh(a.out);cfg=json.loads(Path(a.config).read_text())
    for arm in cfg['variants']:
        subprocess.run([sys.executable,str(Path(__file__).resolve()),'worker','--config',str(Path(a.config).resolve()),
                        '--arm',arm,'--out',str(out/(arm+'.csv'))],check=True)
    summarize(a)



def timing_worker(a):
    cfg=json.loads(Path(a.config).read_text());check_inputs(cfg['inputs'])
    directory=cfg['variants'][a.arm]
    os.environ.pop('ZC_SIGMA_OVERRIDE_DIR',None);os.environ.pop('ZC_ONLY_KEYS',None)
    if directory:os.environ['ZC_SIGMA_OVERRIDE_DIR']=directory
    os.environ['ZC_R6_ENDPOINT']=str(a.flag)
    from zcosmo.z0x import Z0xBinary
    from r3_common import STALL_KEYS
    rows=pd.read_csv(cfg['rows']);cache={};values=[]
    t=time.perf_counter()
    for r in rows.itertuples():
        if a.arm=='open630' and (r.solute in STALL_KEYS or r.solvent in STALL_KEYS):continue
        key=(r.solute,r.solvent)
        try:
            if key not in cache:cache[key]=Z0xBinary(list(key))
            v=float(cache[key].lngamma_inf(r.T,0))
        except Exception:v=np.nan
        values.append(v)
    write(a.out,dict(flag=a.flag,arm=a.arm,rows=len(values),finite_rows=int(np.isfinite(values).sum()),wall_s=time.perf_counter()-t))
    check_inputs(cfg['inputs'])


def timing(a):
    cfg=json.loads(Path(a.config).read_text());out=fresh(a.out);answer={}
    for arm in cfg['variants']:
        times={0:[],1:[]}
        for rep in range(3):
            for flag in ((0,1) if rep%2==0 else (1,0)):
                p=out/f'{arm}-{rep}-{flag}.json'
                subprocess.run([sys.executable,str(Path(__file__).resolve()),'timing_worker',
                    '--config',str(Path(a.config).resolve()),'--arm',arm,'--flag',str(flag),'--out',str(p)],check=True)
                times[flag].append(json.loads(p.read_text())['wall_s'])
        answer[arm]=dict(legacy_s=times[0],candidate_s=times[1],
                        median_speedup=float(np.median(times[0])/np.median(times[1])))
    write(out/'summary.json',dict(timings=answer,scope='Fresh-process matched query sequence; no profiler or reference solve in the timed section.'))


def score(a):
    # This intentionally separate command reads responses only after numerical acceptance.
    cfg=json.loads(Path(a.config).read_text());check_inputs(cfg['inputs'])
    run=Path(a.run);gate=run/'gate.json';g=json.loads(gate.read_text())
    check_inputs(g['audit_csv_inputs'])
    if g['config_sha256']!=sha(a.config):raise ValueError('gate configuration changed')
    decision=json.loads(Path(a.acceptance_record).read_text())
    if not g['numerical_gate'] or decision.get('decision')!='accepted' or decision.get('numerical_gate_sha256')!=sha(gate):
        raise ValueError('A recorded acceptance of this exact numerical gate is required')
    from r3_common import cluster_ci
    asset=json.loads((Path(a.config).parent/'assets/config.json').read_text())
    record=asset['universe']['idac']
    if sha(record['path'])!=record['sha256']:raise ValueError('frozen scoring universe changed')
    u=pd.read_csv(record['path']).set_index('r5_row_id')
    out=fresh(a.out);records=[]
    for arm in cfg['variants']:
        d=pd.read_csv(run/(arm+'.csv')).set_index('r5_row_id')
        if set(d.index)!=set(u.index) or not d.index.is_unique:raise ValueError('score universe changed')
        d['response']=u.loc[d.index,'ln_gamma_inf']
        for split in ('all','test'):
            q=d if split=='all' else d[d['split']!='train']
            f=q[q.status=='checked'];er=f.legacy-f.response;ec=f.candidate-f.response
            sid=np.where(f.solute<f.solvent,f.solute+'|'+f.solvent,f.solvent+'|'+f.solute)
            records.append(dict(arm=arm,split=split,requested_rows=len(q),finite_paired_rows=len(f),
                legacy_MAE=float(abs(er).mean()),candidate_MAE=float(abs(ec).mean()),
                delta_MAE_CI95=cluster_ci(abs(ec)-abs(er),sid),
                source='R6 numerical endpoint correction; historical P27 files not overwritten'))
        d.to_csv(out/(arm+'.csv'))
    write(out/'scores.json',dict(acceptance_sha256=sha(a.acceptance_record),tables=records))

def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
    q=s.add_parser('prepare');q.add_argument('--profile-root',default='data/pyscf_sigma');q.add_argument('--registration',required=True);q.add_argument('--out',required=True)
    for name in ('run','worker','summarize','timing','timing_worker'):
        q=s.add_parser(name);q.add_argument('--config',required=True);q.add_argument('--out',required=True)
        if name in ('worker','timing_worker'):q.add_argument('--arm',required=True)
        if name=='timing_worker':q.add_argument('--flag',type=int,choices=[0,1],required=True)
    q=s.add_parser('score');q.add_argument('--config',required=True);q.add_argument('--run',required=True)
    q.add_argument('--acceptance-record',required=True);q.add_argument('--out',required=True)
    a=p.parse_args();globals()[a.cmd](a)
if __name__=='__main__':main()
