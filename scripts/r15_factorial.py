"""Mac-only R15 fitted-ingredient attribution on the exact archived P52 rows.

No QC, sampling, profile generation, parameter fitting, or production writes.
The archived R14 controls are audited separately from the new factorial.
"""
from __future__ import annotations
import argparse
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import numpy as np
import r14_dielectric as d
import r14_oracle as old
import r15_math as a

ROOT = d.ROOT
BASE = '3cd0a22888b40699d5f4994f5ba2e5cd274703df'
MARKER = 'R15-P54-P55-P56: contact attribution, association dispatch, and manuscript scope'
FILES = ('scripts/r15_math.py', 'scripts/r15_factorial.py', 'scripts/r15_selftest.py')
ASSOC = 'src/zcosmo/z0w.py'
DESIGN = dict(rows=963, systems=100, factors=list(a.FACTORS), active_corners=list(a.CORNERS),
    order=list(a.ANCHORS+a.INTERMEDIATE), shared_aeff=7.25,
    source='original private P52 plan and completed run',
    baseline='stored-epsilon Z0x', target='COSMO-SAC 2010 without explicit dispersion',
    requests=7704, anchors=1926, remaining=5778, seconds_per_worker=120,
    driver_seconds=7200, workers_in_parallel=1, anchor_relative_tolerance=1e-8,
    adopted=False, QC_calls=0, scoring='exposed retrospective ThermoML diagnostic',
    no_new_subset=True, no_tuning=True, no_retries=True)


def git_bytes(commit, rel):
    return subprocess.check_output(['git', 'show', commit+':'+rel], cwd=ROOT)


def ancestor(commit, child='HEAD'):
    d.require(re.fullmatch(r'[0-9a-f]{40}', commit) is not None, 'Use full commit identity')
    subprocess.run(['git','merge-base','--is-ancestor',commit,child], cwd=ROOT,
                   check=True, capture_output=True)


def registration(commit):
    ancestor(commit); ancestor(BASE, commit)
    d.require(MARKER in git_bytes(commit, 'PREREGISTRATION.md').decode(), 'R15 registration absent')
    for rel in (*FILES, ASSOC):
        d.require((ROOT/rel).read_bytes() == git_bytes(commit, rel), 'Unregistered source drift: '+rel)
    for rel in ('src/zcosmo/cosmosac.py','src/zcosmo/z0x.py',
                'src/zcosmo/zmodel.py','src/zcosmo/models.py',
                'results/z_params/Z0.json','results/qc/dielectric.csv',
                'results/qc/dispersion.csv'):
        d.require((ROOT/rel).read_bytes() == git_bytes(BASE,rel),
                  'Participating model source differs from reviewed main: '+rel)
    return commit


def check_old_inputs(saved, reg):
    """One explicit nonparticipant-source bridge, not a weakened R14 checker.

    P55 changes z0w.py. P52 did not call it. All old data and all participating
    model sources must still match. The old R14 check remains unmodified.
    """
    bridges=[]
    for name, expected in saved.items():
        p=Path(name).resolve()
        if d.sha(p) == expected:
            continue
        d.require(p == (ROOT/ASSOC).resolve(), 'Historical input mutation: '+p.name)
        original=git_bytes(BASE,ASSOC)
        d.require(hashlib.sha256(original).hexdigest() == expected,
                  'Historical association file was not the reviewed baseline')
        d.require(p.read_bytes() == git_bytes(reg,ASSOC), 'Association repair differs from registration')
        bridges.append(dict(relative_path=ASSOC, old_sha256=expected, new_sha256=d.sha(p),
                            scope='not invoked by P52 or P54'))
    return bridges


def archive(plan, plan_commit, run, reg):
    """Replay only archived hashes/arithmetic. Never call an activity model."""
    p=d.private(plan); rp=d.private(run); m=d.read(p)
    d.registration(m['registration']); ancestor(plan_commit)
    ancestor(m['registration'], plan_commit)
    d.require(git_bytes(plan_commit,'docs/astra/round14/ORACLE_PLAN_SHA256.txt').decode().strip()==d.sha(p),
              'Wrong R14 plan digest')
    d.require(m['schema']=='r14-oracle-v1' and m['design']==old.DESIGN,
              'Unexpected R14 design')
    d.require(m['environment']==d.environment(), 'R14 environment changed')
    bridges=check_old_inputs(m['inputs'],reg)
    bridges+=check_old_inputs(m['ingredient_manifest']['inputs'],reg)
    d.require(m['exposure']['may_claim_unexposed'] is False and
              m['protected_counts']=={'profiles_v2':630,'s1_stalled':1,'s2_stalled':5},
              'Historical exposure or protected selection changed')
    d.require(d.read(p.parent/'execution_claim.json')==dict(plan_sha256=d.sha(p),output=str(rp)),
              'Different R14 claimed run')
    v,n,h=old.arrays(m,rp,d.sha(p)); z=d.read(rp/'summary.json')
    ar=old.anchor_pass(m['rows'],v[:,0]); fresh=old.error_summary(m['rows'],v)
    d.require(ar['passed'] and fresh['status']['complete'] and n==2889,
              'R14 is not the completed 2889-request result')
    d.require(z['plan_sha256']==d.sha(p) and z['anchor']==ar and z['output_hashes']==h and
              z['attempted_model_calls']==n and z['status']==fresh['status'] and
              z['aggregate_errors']==fresh['aggregate_errors'], 'R14 summary changed')
    expected=dict(status=fresh['status'],anchor=ar,aggregate_errors=fresh['aggregate_errors'],
                  census=m['census'],interpretation=old.DESIGN['result'],adopted=False,SCF_calls=0)
    d.require(d.read(rp/'public-errors.json')==expected, 'R14 public receipt changed')
    # Identity counts come from a completed private plan, not rounded public tables.
    rows=m['rows']; ids=[r['row_id'] for r in rows]
    d.require(len(rows)==963 and len(set(ids))==963 and len({r['system'] for r in rows})==100,
              'Not the requested 963-row/100-system universe')
    for r in rows:
        d.require(250<=r['T']<=450 and 0<r['P']<=500 and 1e-4<r['x1']<1-1e-4,
                  'P52 query outside its stated scope; no silent removal')
        d.require(r['system']=='|'.join(sorted((r['c1'],r['c2']))) and r['c1']!=r['c2'],
                  'Historical pair identity changed')
        d.require(np.isfinite(r['psat']).all() and min(r['psat'])>0, 'Invalid saved psat')
    receipts=dict(h)
    receipts.update(d.fingerprint([p,p.parent/'execution_claim.json',rp/'summary.json',rp/'public-errors.json']))
    receipts.update({name:d.sha(name) for name in m['inputs']})
    receipts.update({name:d.sha(name) for name in m['ingredient_manifest']['inputs']})
    return m,v,receipts,bridges


def jobs_for(rows):
    pairs=sorted({(r['c1'],r['c2']) for r in rows}); jobs=[]
    for corner in a.ANCHORS+a.INTERMEDIATE:
        for pair in pairs:
            idx=[i for i,r in enumerate(rows) if (r['c1'],r['c2'])==pair]
            jobs.append(dict(id=f'job-{len(jobs):04d}',corner=corner,keys=list(pair),indices=idx))
    d.require(sum(len(j['indices']) for j in jobs)==8*len(rows), 'Request count mismatch')
    return jobs


def freeze(args):
    d.mac();reg=registration(args.registration)
    previous,values,inputs,bridges=archive(args.r14_plan,args.r14_plan_commit,args.r14_run,reg)
    from zcosmo.cosmosac import Params
    params=d.read(ROOT/'results/z_params/Z0.json')['params']
    params['disp_override']=tuple(tuple(v) for v in params.get('disp_override',()))
    audit=a.shared_audit(Params(**params),Params(use_dsp=False))
    sources=[*list((ROOT/'src/zcosmo').glob('*.py')),
             *(ROOT/rel for rel in FILES),ROOT/'scripts/r14_dielectric.py',
             ROOT/'scripts/r14_oracle.py',ROOT/'scripts/r14_selftest.py']
    sources+= [ROOT/'results/z_params/Z0.json',ROOT/'results/qc/dispersion.csv',ROOT/'results/qc/dielectric.csv']
    worker_inputs=d.fingerprint(sources);inputs.update(worker_inputs)
    rows=previous['rows'];jobs=jobs_for(rows)
    d.require(sum(len(j['indices']) for j in jobs)==DESIGN['requests'], 'Fixed budget changed')
    out=d.private(args.out,True)
    m=dict(schema='r15-factorial-v1',base=BASE,registration=reg,design=DESIGN,
        environment=d.environment(),inputs=inputs,worker_inputs=worker_inputs,
        archive=dict(plan=str(d.private(args.r14_plan)),plan_commit=args.r14_plan_commit,
                     run=str(d.private(args.r14_run))),
        source_bridge=bridges,rows=rows,jobs=jobs,profiles=previous['profiles'],
        prior_anchors=values[:,[0,2]].tolist(),shared_audit=audit,
        protected_counts=previous['protected_counts'],exposure=previous['exposure'])
    d.check_inputs(inputs);d.write(out/'plan.json',m)
    (out/'PLAN_SHA256.txt').write_text(d.sha(out/'plan.json')+'\n')
    print('R15 private plan frozen: 963 rows; 7704 requests; no new model calls.')


def load(plan,commit,full=True):
    d.mac();p=d.private(plan);m=d.read(p);registration(m['registration'])
    ancestor(commit);ancestor(m['registration'],commit)
    d.require(git_bytes(commit,'docs/astra/round15/PLAN_SHA256.txt').decode().strip()==d.sha(p),
              'Uncommitted or altered R15 plan')
    d.require(m['schema']=='r15-factorial-v1' and m['base']==BASE and m['design']==DESIGN,
              'R15 design changed')
    d.require(m['environment']==d.environment(), 'Package environment drift')
    d.require(m['jobs']==jobs_for(m['rows']) and len(m['rows'])==DESIGN['rows'], 'Job identity drift')
    d.check_inputs(m['inputs'] if full else m['worker_inputs'])
    return p,m


def worker(args):
    p,m=load(args.plan,args.plan_commit,False)
    job=next(j for j in m['jobs'] if j['id']==args.job)
    claim=d.read(p.parent/'execution_claim.json');out=d.private(args.out)
    d.require(claim['plan_sha256']==d.sha(p) and out==Path(claim['output'])/job['id'],
              'Worker outside the single claimed run')
    for k in job['keys']:
        d.require(d.sha(m['profiles'][k])==m['inputs'][str(Path(m['profiles'][k]).resolve())],
                  'Frozen profile changed')
    out=d.private(out,True)
    for k in list(os.environ):
        if k.startswith('ZC_'):os.environ.pop(k)
    ov=out/'overlay';ov.mkdir(mode=0o700)
    for key in job['keys']:(ov/(key+'.sigma')).symlink_to(Path(m['profiles'][key]))
    os.environ['ZC_SIGMA_OVERRIDE_DIR']=str(ov);os.environ['ZC_R6_ENDPOINT']='1'
    from zcosmo.cosmosac import load_fluid,sigma_path,SIG
    for key in job['keys']:
        d.require(sigma_path(key).resolve()==Path(m['profiles'][key]).resolve(), 'Unexpected fallback profile')
        fl=load_fluid(key);raw=np.loadtxt(m['profiles'][key])
        d.require(raw.shape==(153,2) and np.allclose(raw[:,0],np.tile(SIG,3),rtol=0,atol=1e-12)
                  and np.isfinite(raw).all() and (raw[:,1]>=0).all()
                  and np.array_equal(fl.psigA.ravel(),raw[:,1]) and fl.A>0 and fl.V>0,
                  'Invalid or mismatched stored sigma grid')
    model=a.make_corner(job['keys'],job['corner']);vals=[];start=time.monotonic()
    for i in job['indices']:
        r=m['rows'][i];value=None;error=None
        d.write(out/f'attempt-{len(vals):04d}.json',dict(row_id=r['row_id'],attempted=True))
        try:value=old.pressure(model.lngamma(r['T'],np.array([r['x1'],1-r['x1']])),r['x1'],r['psat'])
        except Exception as ex:error=type(ex).__name__
        vals.append(dict(row_id=r['row_id'],value=value,error=error))
    d.check_inputs(m['worker_inputs'])
    d.check_inputs({str(Path(m['profiles'][k]).resolve()):m['inputs'][str(Path(m['profiles'][k]).resolve())]
                    for k in job['keys']})
    d.write(out/'result.json',dict(job=job['id'],corner=job['corner'],plan_sha256=d.sha(p),
        requested=len(job['indices']),attempted=len(vals),values=vals,wall_s=time.monotonic()-start))


def arrays(m,run,plan_hash):
    run=Path(run);values=np.full((len(m['rows']),8),np.nan);hashes={};attempts=0
    for job in m['jobs']:
        tp=run/(job['id']+'.terminal.json');term=d.read(tp);hashes.update(d.fingerprint([tp]))
        d.require(term['job']==job['id'] and term['plan_sha256']==plan_hash, 'Terminal identity changed')
        folder=run/job['id'];started=sorted(folder.glob('attempt-*.json'))
        expected=[m['rows'][i]['row_id'] for i in job['indices']]
        d.require(len(started)<=len(expected), 'Query ceiling exceeded')
        for j,sp in enumerate(started):
            d.require(sp.name==f'attempt-{j:04d}.json' and
                d.read(sp)==dict(row_id=expected[j],attempted=True), 'Attempt receipt changed')
        attempts+=len(started);hashes.update(d.fingerprint(started));rp=folder/'result.json'
        if term['state']!='returned' or term['returncode']!=0 or not rp.is_file():continue
        z=d.read(rp);hashes.update(d.fingerprint([rp]))
        d.require(z['job']==job['id'] and z['corner']==job['corner'] and z['plan_sha256']==plan_hash
                  and z['attempted']==z['requested']==len(expected)==len(started)
                  and [v['row_id'] for v in z['values']]==expected, 'Worker result identity changed')
        for i,v in zip(job['indices'],z['values']):
            if v['value'] is not None:values[i,a.CORNERS.index(job['corner'])]=float(v['value'])
    d.require(attempts<=DESIGN['requests'], 'R15 request ceiling exceeded')
    return values,attempts,hashes


def anchor(m,values):
    now=np.asarray(values)[:,[0,7]];prior=np.asarray(m['prior_anchors'],float)
    d.require(now.shape==prior.shape and np.isfinite(prior).all() and (prior>0).all(), 'Invalid archived anchors')
    finite=np.isfinite(now)&(now>0)
    with np.errstate(over='ignore', invalid='ignore'):
        relative=abs(now/prior-1)
    err=float(np.max(relative)) if finite.all() and np.isfinite(relative).all() else None
    return dict(passed=bool(err is not None and err<DESIGN['anchor_relative_tolerance']),
        requested=int(now.size),finite=int(finite.sum()),max_relative_pressure_error=err)


def public(result,ar):
    return dict(status=result['status'],anchors=ar,aggregate_errors=result['public_errors'],
        adopted=False,QC_calls=0,interpretation='retrospective fitted-ingredient diagnostic; not a selected model')


def collect(args):
    start=time.monotonic();p,m=load(args.plan,args.plan_commit);run=d.private(args.run)
    d.require(d.read(p.parent/'execution_claim.json')==dict(plan_sha256=d.sha(p),output=str(run)), 'Run claim changed')
    v,n,h=arrays(m,run,d.sha(p));ar=anchor(m,v);q=a.summary(m['rows'],v,ar['passed'])
    d.check_inputs(m['inputs'])
    z=dict(plan_sha256=d.sha(p),attempted_model_calls=n,anchors=ar,
           status=q['status'],public_errors=q['public_errors'],output_hashes=h,
           collection_wall_s=time.monotonic()-start,QC_calls=0,source_profiles_unchanged=True)
    d.write(run/'private-rows.json',q['private_rows']);d.write(run/'summary.json',z)
    d.write(run/'public-errors.json',public(q,ar))
    print('R15 saved result complete:',q['status']['complete'])
    return 0 if q['status']['complete'] else 2


def run(args):
    p,m=load(args.plan,args.plan_commit);out=d.private(args.out)
    d.write(p.parent/'execution_claim.json',dict(plan_sha256=d.sha(p),output=str(out)))
    out=d.private(out,True);start=time.monotonic();env=dict(os.environ)
    env.update(OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1')
    for j in m['jobs']:
        d.write(out/(j['id']+'.terminal.json'),dict(job=j['id'],plan_sha256=d.sha(p),state='not_started',returncode=None))
    ar=None
    for j in m['jobs']:
        if j['corner'] not in a.ANCHORS and ar is None:
            v,_,_=arrays(m,out,d.sha(p));ar=anchor(m,v)
        remain=DESIGN['driver_seconds']-(time.monotonic()-start)
        term=dict(job=j['id'],plan_sha256=d.sha(p),state='not_run_budget',returncode=None)
        if j['corner'] not in a.ANCHORS and not ar['passed']:term['state']='blocked_anchors'
        elif remain>1:
            cmd=[sys.executable,str(Path(__file__).resolve()),'_worker','--plan',str(p),
                 '--plan-commit',args.plan_commit,'--job',j['id'],'--out',str(out/j['id'])]
            try:term.update(old.launch(cmd,out/(j['id']+'.log'),min(remain,DESIGN['seconds_per_worker']),env))
            except Exception:term.update(state='launch_failed')
        tmp=out/(j['id']+'.terminal.tmp');d.write(tmp,term);os.replace(tmp,out/(j['id']+'.terminal.json'))
    d.write(out/'timing.json',dict(model_run_wall_s=time.monotonic()-start))
    return collect(argparse.Namespace(plan=args.plan,plan_commit=args.plan_commit,run=str(out)))


def check(args):
    p,m=load(args.plan,args.plan_commit);run=d.private(args.run);z=d.read(run/'summary.json')
    d.require(d.read(p.parent/'execution_claim.json')==dict(plan_sha256=d.sha(p),output=str(run)), 'Run claim changed')
    v,n,h=arrays(m,run,d.sha(p));ar=anchor(m,v);q=a.summary(m['rows'],v,ar['passed'])
    d.require(z['plan_sha256']==d.sha(p) and z['attempted_model_calls']==n and z['anchors']==ar
        and z['status']==q['status'] and z['public_errors']==q['public_errors'] and z['output_hashes']==h,
        'Saved R15 result changed')
    d.require(d.read(run/'private-rows.json')==q['private_rows'] and
              d.read(run/'public-errors.json')==public(q,ar), 'Derived output changed')
    print('R15 checked without new activity calls. Complete:',q['status']['complete'])
    return 0 if q['status']['complete'] else 2


def main():
    p=argparse.ArgumentParser(description=__doc__);sp=p.add_subparsers(dest='cmd',required=True)
    q=sp.add_parser('freeze');q.add_argument('--registration',required=True)
    q.add_argument('--r14-plan',required=True);q.add_argument('--r14-plan-commit',required=True)
    q.add_argument('--r14-run',required=True);q.add_argument('--out',required=True);q.set_defaults(fn=freeze)
    for name,fn in (('run',run),('collect',collect),('check',check),('_worker',worker)):
        q=sp.add_parser(name);q.add_argument('--plan',required=True);q.add_argument('--plan-commit',required=True)
        q.add_argument('--run' if name in ('collect','check') else '--out',required=True)
        if name=='_worker':q.add_argument('--job',required=True)
        q.set_defaults(fn=fn)
    args=p.parse_args();return args.fn(args)

if __name__=='__main__':raise SystemExit(main())
