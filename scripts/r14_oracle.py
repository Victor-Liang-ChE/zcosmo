"""Private, retrospective R14 epsilon-298 oracle. No native calculations or adoption.

The same frozen sigma profiles, parameters and pure vapor pressures are used in
all arms. The experiment is deliberately not a new held-out scorecard.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import numpy as np
import r14_dielectric as d

ROOT=d.ROOT
ARMS=('baseline','experimental_epsilon_298','cosmosac2010')
DESIGN=dict(max_systems=100,max_rows_per_system=10,max_rows=1000,
    selection_seed='R14-oracle-v1',split='already_exposed_test_one_and_test_both',
    interior_strip=1e-4,baseline_relative_pressure_tolerance=1e-7,
    max_model_calls=3000,worker_seconds=120,driver_seconds=7200,
    epsilon_temperature_K=298.15,temperature_dependence_changed=False,
    profile_source='frozen_UD',fallback='exclude missing reference from paired oracle, enumerate exclusions',
    result='retrospective sensitivity, not an attainable upper bound or production model',
    SCF_calls=0,adopted=False,pressure_unit='kPa')


def stable_order(text):
    return hashlib.sha256((DESIGN['selection_seed']+'|'+text).encode()).hexdigest()


def select(rows, refs):
    """Stable identities are input-file ordinals bound to the complete file hash."""
    groups={}; counts={}
    for i,r in enumerate(rows):
        why=None
        k1,k2=r['c1'],r['c2']
        x,t,p,old=(d.number(r.get(k)) for k in ('x1','T','P','pred_P'))
        if r.get('split') not in ('test_one','test_both'):why='other_historical_split'
        elif k1==k2:why='self_pair'
        elif k1 not in refs or k2 not in refs:why='missing_exact_reference_identity'
        elif None in (x,t,p,old) or t<=0 or p<=0 or old<=0:why='invalid_archived_query_or_prediction'
        elif not DESIGN['interior_strip']<x<1-DESIGN['interior_strip']:why='endpoint_or_numerical_strip'
        if why:
            counts[why]=counts.get(why,0)+1; continue
        system='|'.join(sorted((k1,k2)))
        z=dict(row_id=str(i),c1=k1,c2=k2,T=t,x1=x,P=p,archived_pred_P=old,system=system)
        groups.setdefault(system,[]).append(z)
    selected=[]
    eligible_rows=sum(map(len,groups.values()))
    chosen=sorted(groups,key=stable_order)[:DESIGN['max_systems']]
    for system in chosen:
        chosen_rows=sorted(groups[system],key=lambda r:stable_order(system+'|'+r['row_id']))[:DESIGN['max_rows_per_system']]
        selected.extend(chosen_rows)
    d.require(selected,'no eligible oracle rows; no substitute selection authorized')
    return selected,dict(input_rows=len(rows),eligible_rows=eligible_rows,eligible_systems=len(groups),
        selected_rows=len(selected),selected_systems=len(chosen),
        eligible_not_sampled=eligible_rows-len(selected),excluded=counts)


def protected_profiles(root):
    root=Path(root).resolve(); files=[]; counts={}
    for folder,expected in (('profiles_v2',630),('s1_stalled',1),('s2_stalled',5)):
        ps=sorted((root/folder).glob('*.sigma'))
        d.require(len(ps)==expected,'protected profile count differs in '+folder)
        counts[folder]=len(ps); files.extend(ps)
    d.require(len({p.stem for p in files})==636,'duplicate protected identities')
    return d.fingerprint(files),counts


def profile_path(key, folder):
    folder=Path(folder).resolve(); exact=folder/(key+'.sigma')
    if exact.is_file():return exact
    matches=sorted(folder.glob(key[:14]+'-*.sigma'))
    d.require(len(matches)==1,'missing or ambiguous historical UD profile: '+key)
    return matches[0]


def pressure(lg,x,psat):
    """All pressures are kPa, as in zcosmo.scope.psat and the archive."""
    lg=np.asarray(lg,float); psat=np.asarray(psat,float)
    d.require(lg.shape==(2,) and psat.shape==(2,) and np.isfinite(lg).all() and
              np.isfinite(psat).all() and (psat>0).all(),'invalid pressure ingredients')
    with np.errstate(over='raise',invalid='raise'):
        p=float(np.sum(np.array([x,1-x])*np.exp(lg)*psat))
    d.require(math.isfinite(p) and p>0,'invalid predicted pressure')
    return p


def error_summary(rows, values):
    a=np.asarray(values,float); n=len(rows)
    d.require(n>0 and a.shape==(n,3),'oracle dimensions changed')
    finite=np.isfinite(a)&(a>0)
    receipt=dict(requested_rows=n,finite_counts=finite.sum(0).tolist(),complete=bool(finite.all()),
        adopted=False,confirmatory=False,experimental_epsilon_is_fit_free=False)
    if not finite.all():return dict(status=receipt,aggregate_errors=None)
    truth=np.array([r['P'] for r in rows]); d.require(np.isfinite(truth).all() and (truth>0).all(),'invalid observed pressure')
    err=100*np.abs(a/truth[:,None]-1)
    signed=100*(a/truth[:,None]-1)
    means=err.mean(0); gap=float(means[0]-means[2]);gain=float(means[0]-means[1])
    groups=sorted({r['system'] for r in rows})
    grouped=np.array([err[[r['system']==g for r in rows]].mean(0) for g in groups])
    return dict(status=receipt,aggregate_errors=dict(arms=list(ARMS),rows=n,systems=len(groups),
        AAD_percent=means.tolist(),bias_percent=signed.mean(0).tolist(),
        equal_system_AAD_percent=grouped.mean(0).tolist(),
        oracle_minus_baseline_pp=-gain,baseline_minus_cosmosac2010_pp=gap,
        oracle_minus_cosmosac2010_pp=float(means[1]-means[2]),
        signed_gap_recovery=None if gap<=1e-6 else gain/gap,
        improved_rows=int((err[:,1]<err[:,0]).sum()),worsened_rows=int((err[:,1]>err[:,0]).sum()),
        no_generalization_CI=True))


def code_paths():
    return list((ROOT/'src/zcosmo').glob('*.py'))+[ROOT/'scripts/r14_dielectric.py',
        ROOT/'scripts/r14_oracle.py',ROOT/'scripts/r14_selftest.py']


def freeze(a):
    d.mac();reg=d.registration(a.registration);out=d.private(a.out,True)
    ingredient=d.private(a.ingredients)
    d.check(argparse.Namespace(out=str(ingredient)))
    im=d.read(ingredient/'manifest.json'); ir=d.read(ingredient/'ingredients.json')
    d.require(im['registration']==reg and im['exposure']['may_score_frozen_retrospective_oracle'] is True
              and im['exposure']['may_claim_unexposed'] is False,'exposure or registration mismatch')
    refs={r['key']:r['reference_epsilon'] for r in ir['rows'] if r['status']=='matched'}
    rows,census=select(d.records(a.archive),refs)
    ps,counts=protected_profiles(a.profile_root)
    tables=[ROOT/'results/qc/dielectric.csv',ROOT/'results/qc/dispersion.csv',ROOT/'results/z_params/Z0.json']
    files=code_paths()+tables+[ROOT/'data/benchmark/compounds.csv',Path(a.archive),ingredient/'manifest.json',ingredient/'ingredients.json']
    filehash=d.fingerprint(files);filehash.update(ps)
    profiles={k:str(profile_path(k,a.ud_profiles)) for k in {v for r in rows for v in (r['c1'],r['c2'])}}
    filehash.update(d.fingerprint(profiles.values()))
    # This is the existing vapor-pressure provider, used once to freeze common inputs.
    # No activity coefficient is queried here and experimental mixture P is not used.
    for key in list(os.environ):
        if key.startswith('ZC_'):os.environ.pop(key)
    from zcosmo.scope import psat
    for r in rows:
        r['psat']=[float(psat(k,r['T'])) for k in (r['c1'],r['c2'])]
        d.require(all(math.isfinite(v) and v>0 for v in r['psat']),'invalid pure vapor pressure; preparation stops')
    jobs=[]
    pairs=sorted({(r['c1'],r['c2']) for r in rows})
    for arm in ARMS:
        for pair in pairs:
            idx=[i for i,r in enumerate(rows) if (r['c1'],r['c2'])==pair]
            jobs.append(dict(id=f'job-{len(jobs):04d}',arm=arm,keys=list(pair),indices=idx))
    d.require(sum(len(j['indices']) for j in jobs)==3*len(rows)<=DESIGN['max_model_calls'],'request budget mismatch')
    d.check_inputs(filehash)
    m=dict(schema='r14-oracle-v1',base=d.BASE,registration=reg,design=DESIGN,environment=d.environment(),
        inputs=filehash,ingredient_manifest=im,exposure=im['exposure'],rows=rows,census=census,
        reference_epsilon={k:refs[k] for k in profiles},profiles=profiles,protected_counts=counts,jobs=jobs)
    d.write(out/'plan.json',m)
    with (out/'PLAN_SHA256.txt').open('x') as f:f.write(d.sha(out/'plan.json')+'\n')
    print('Private oracle plan frozen. Commit only its digest before the one run.')


def load(plan, plan_commit):
    d.mac();p=d.private(plan);m=d.read(p);d.registration(m['registration'])
    d.require(m['design']==DESIGN and m['schema']=='r14-oracle-v1','design changed')
    d.require(m['environment']==d.environment(),'environment changed')
    d.check_inputs(m['inputs']);d.check_inputs(m['ingredient_manifest']['inputs'])
    d.require(m['exposure']['may_claim_unexposed'] is False,'oracle cannot be relabeled held out')
    subprocess.run(['git','merge-base','--is-ancestor',plan_commit,'HEAD'],cwd=ROOT,check=True,capture_output=True)
    text=subprocess.check_output(['git','show',plan_commit+':docs/astra/round14/ORACLE_PLAN_SHA256.txt'],cwd=ROOT,text=True).strip()
    d.require(text==d.sha(p),'uncommitted or different oracle plan')
    return p,m


def worker(a):
    p,m=load(a.plan,a.plan_commit); job=next(j for j in m['jobs'] if j['id']==a.job)
    claim=d.read(p.parent/'execution_claim.json')
    expected=Path(claim['output']).resolve()/job['id']
    d.require(claim['plan_sha256']==d.sha(p) and d.private(a.out)==expected,'worker outside the one claimed run')
    out=d.private(a.out,True)
    for key in list(os.environ):
        if key.startswith('ZC_'):os.environ.pop(key)
    os.environ['ZC_R6_ENDPOINT']='1';os.environ['ZC_SIGMA_OVERRIDE_DIR']=str(out/'overlay')
    ov=out/'overlay';ov.mkdir(mode=0o700)
    for key in job['keys']:(ov/(key+'.sigma')).symlink_to(Path(m['profiles'][key]))
    from zcosmo.z0x import Z0xBinary
    from zcosmo.cosmosac import Mixture,Params,load_fluid
    # Explicit overlay verification prevents silent fallback or cached profiles.
    for key in job['keys']:
        fl=load_fluid(key)
        d.require(fl.psigA.shape==(3,51) and np.isfinite(fl.psigA).all(),'invalid frozen profile')
    if job['arm']=='cosmosac2010':model=Mixture(job['keys'],Params(use_dsp=False))
    else:
        model=Z0xBinary(job['keys'])
        if job['arm']=='experimental_epsilon_298':
            model.eps=np.array([m['reference_epsilon'][k] for k in job['keys']],float)
            model._mix.clear()
    values=[]; start=time.monotonic()
    for i in job['indices']:
        r=m['rows'][i]; value=None; error=None
        d.write(out/f'attempt-{len(values):04d}.json',dict(row_id=r['row_id'],attempted=True))
        try:value=pressure(model.lngamma(r['T'],np.array([r['x1'],1-r['x1']])),r['x1'],r['psat'])
        except Exception as e:error=type(e).__name__
        values.append(dict(row_id=r['row_id'],value=value,error=error))
    d.check_inputs(m['inputs'])
    d.write(out/'result.json',dict(job=job['id'],arm=job['arm'],plan_sha256=d.sha(p),
        requested=len(job['indices']),attempted=len(values),values=values,wall_s=time.monotonic()-start))


def launch(cmd, log, seconds, env):
    with Path(log).open('xb') as f:
        proc=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT,env=env,start_new_session=True)
        try:return dict(state='returned',returncode=proc.wait(timeout=seconds))
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid,signal.SIGKILL);proc.wait(timeout=5)
            return dict(state='timeout',returncode=proc.returncode)


def arrays(m, run, plan_hash):
    a=np.full((len(m['rows']),3),np.nan);hashes={};attempts=0
    for job in m['jobs']:
        tpath=run/(job['id']+'.terminal.json'); term=d.read(tpath);hashes[str(tpath)]=d.sha(tpath)
        d.require(term['job']==job['id'] and term['plan_sha256']==plan_hash,'terminal identity changed')
        folder=run/job['id'];started=sorted(folder.glob('attempt-*.json')) if folder.exists() else []
        for j,ap in enumerate(started):
            expected_row=m['rows'][job['indices'][j]]['row_id'] if j<len(job['indices']) else None
            d.require(ap.name==f'attempt-{j:04d}.json' and d.read(ap)==dict(row_id=expected_row,attempted=True),'attempt receipt changed')
        attempts+=len(started)
        d.require(len(started)<=len(job['indices']),'per-job request ceiling exceeded')
        hashes.update(d.fingerprint(started))
        rp=folder/'result.json'
        if term['state']!='returned' or term['returncode']!=0 or not rp.is_file():continue
        z=d.read(rp);hashes[str(rp)]=d.sha(rp)
        expected=[m['rows'][i]['row_id'] for i in job['indices']]
        d.require(z['job']==job['id'] and z['arm']==job['arm'] and z['plan_sha256']==plan_hash
            and z['requested']==len(expected) and z['attempted']==len(started)==len(expected)
            and [v['row_id'] for v in z['values']]==expected,'result identities or counts changed')
        for i,v in zip(job['indices'],z['values']):
            if v['value'] is not None:a[i,ARMS.index(job['arm'])]=float(v['value'])
    d.require(attempts<=3*len(m['rows'])<=DESIGN['max_model_calls'],'total request ceiling exceeded')
    return a,attempts,hashes


def anchor_pass(rows, baseline):
    old=np.array([r['archived_pred_P'] for r in rows]); b=np.asarray(baseline,float)
    finite=np.isfinite(b)&(b>0)
    error=float(np.max(np.abs(b/old-1))) if finite.all() else None
    return dict(passed=bool(finite.all() and error<DESIGN['baseline_relative_pressure_tolerance']),
        max_relative_pressure_error=error,requested=len(rows),finite=int(finite.sum()))


def run(a):
    p,m=load(a.plan,a.plan_commit);out=d.private(a.out)
    d.write(p.parent/'execution_claim.json',dict(plan_sha256=d.sha(p),output=str(out)))
    out=d.private(out,True);start=time.monotonic(); env=dict(os.environ)
    env.update(OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1')
    anchor=None
    # All terminals exist first, so a killed driver cannot erase requested identities.
    for job in m['jobs']:
        d.write(out/(job['id']+'.terminal.json'),dict(job=job['id'],plan_sha256=d.sha(p),state='not_started',returncode=None))
    for job in m['jobs']:
        if job['arm']!='baseline' and anchor is None:
            v,_,_=arrays(m,out,d.sha(p));anchor=anchor_pass(m['rows'],v[:,0])
        rem=DESIGN['driver_seconds']-(time.monotonic()-start)
        term=dict(job=job['id'],plan_sha256=d.sha(p),state='not_run_budget',returncode=None)
        if job['arm']!='baseline' and not anchor['passed']:term['state']='blocked_anchor'
        elif rem>1:
            cmd=[sys.executable,str(Path(__file__).resolve()),'_worker','--plan',str(p),
                '--plan-commit',a.plan_commit,'--job',job['id'],'--out',str(out/job['id'])]
            try:term.update(launch(cmd,out/(job['id']+'.log'),min(rem,DESIGN['worker_seconds']),env))
            except Exception:term.update(state='launch_failed')
        # Only terminal receipts are updated, never a native/model result or input.
        tp=out/(job['id']+'.terminal.json'); tmp=out/(job['id']+'.terminal.tmp')
        d.write(tmp,term);os.replace(tmp,tp)
    v,attempts,hashes=arrays(m,out,d.sha(p));anchor=anchor_pass(m['rows'],v[:,0])
    load(a.plan,a.plan_commit)
    result=error_summary(m['rows'],v)
    if not anchor['passed']:result['aggregate_errors']=None;result['status']['complete']=False
    summary=dict(plan_sha256=d.sha(p),anchor=anchor,**result,
        attempted_model_calls=attempts,wall_s=time.monotonic()-start,output_hashes=hashes,
        SCF_calls=0,source_profiles_unchanged=True)
    d.write(out/'summary.json',summary)
    d.write(out/'public-errors.json',dict(status=result['status'],anchor=anchor,
        aggregate_errors=result['aggregate_errors'],census=m['census'],
        interpretation=DESIGN['result'],adopted=False,SCF_calls=0))
    print('Private oracle finished. Complete:',result['status']['complete'])
    return 0 if result['status']['complete'] else 2


def check(a):
    p,m=load(a.plan,a.plan_commit);runpath=d.private(a.run);z=d.read(runpath/'summary.json')
    claim=d.read(p.parent/'execution_claim.json')
    d.require(claim==dict(plan_sha256=d.sha(p),output=str(runpath)),'run claim changed')
    v,n,h=arrays(m,runpath,d.sha(p));fresh=error_summary(m['rows'],v);anchor=anchor_pass(m['rows'],v[:,0])
    if not anchor['passed']:fresh['aggregate_errors']=None;fresh['status']['complete']=False
    d.require(z['plan_sha256']==d.sha(p) and z['anchor']==anchor and
        z['attempted_model_calls']==n and z['output_hashes']==h and
        z['status']==fresh['status'] and z['aggregate_errors']==fresh['aggregate_errors'],'saved summary changed')
    public=dict(status=fresh['status'],anchor=anchor,aggregate_errors=fresh['aggregate_errors'],
        census=m['census'],interpretation=DESIGN['result'],adopted=False,SCF_calls=0)
    d.require(public==d.read(runpath/'public-errors.json'),'public summary changed')
    print('Saved oracle checked without model calls. Complete:',fresh['status']['complete'])
    return 0 if fresh['status']['complete'] else 2


def main():
    p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='cmd',required=True)
    q=s.add_parser('freeze');q.add_argument('--registration',required=True);q.add_argument('--ingredients',required=True)
    q.add_argument('--archive',required=True);q.add_argument('--profile-root',required=True);q.add_argument('--ud-profiles',required=True)
    q.add_argument('--out',required=True);q.set_defaults(fn=freeze)
    for name,fn in (('run',run),('check',check),('_worker',worker)):
        q=s.add_parser(name);q.add_argument('--plan',required=True);q.add_argument('--plan-commit',required=True)
        if name=='check':q.add_argument('--run',required=True)
        else:q.add_argument('--out',required=True)
        if name=='_worker':q.add_argument('--job',required=True)
        q.set_defaults(fn=fn)
    a=p.parse_args();return a.fn(a)

if __name__=='__main__':raise SystemExit(main())
