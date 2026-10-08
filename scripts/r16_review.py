"""Private R16 audit and one fixed LV1 screen. No QC, MD or production writes.

P54's VLE rows and frozen saturation pressures are retained. Other properties
use all input-covered original test rows. No runtime finite-subset selection.
Only unchanged Z0x is queried; LV1 uses an exact additive correction to its gE.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time
import numpy as np
import r14_dielectric as d
import r14_oracle as r14
import r15_factorial as r15
import r16_london as law
import r16_stats as stats

ROOT = d.ROOT
BASE = 'ca5c7e94627fcdebbf787afb688f8cab10e42a03'
MARKER = 'R16-P57-P58-P59: London audit, one LV1 screen, and P54 reporting'
FILES = ('scripts/r16_london.py','scripts/r16_stats.py',
         'scripts/r16_review.py','scripts/r16_selftest.py')
DESIGN = dict(recipe=law.RECIPE,vle_rows=963,vle_systems=100,
    source='completed original P54 and original benchmark test collections',
    native_QC=0,MD_steps=0,max_baseline_requests=180000,driver_seconds=21600,
    worker_seconds=180,OMP_threads=4,BLAS_threads=1,no_retries=True,
    exact_endpoint=True,he_dT_K=.5,grid_sizes=list(stats.GRID_SIZES),gap_tolerance=stats.GAP_TOL,
    baseline_relative_pressure_tolerance=1e-8,bootstrap_replicates=stats.BOOTSTRAPS,
    bootstrap_seed=stats.SEED,adopted=False,exposed=True,
    failure='withhold complete tradeoff/acceptance; never drop a failed row',
    fallback='no candidate for unavailable input; explicitly counted before queries')


def registration(commit):
    r15.ancestor(commit);r15.ancestor(BASE,commit)
    text=r15.git_bytes(commit,'PREREGISTRATION.md').decode()
    d.require(MARKER in text and law.RECIPE in text,'R16 registration absent')
    for rel in FILES:
        d.require((ROOT/rel).read_bytes()==r15.git_bytes(commit,rel),'Unregistered R16 source: '+rel)
    # No change to the participating baseline or to the P55 repair is allowed.
    for p in (ROOT/'src/zcosmo').glob('*.py'):
        rel=str(p.relative_to(ROOT))
        d.require(p.read_bytes()==r15.git_bytes(BASE,rel),'Production source drift: '+rel)
    for rel in ('results/qc/dispersion.csv','results/qc/dielectric.csv','results/z_params/Z0.json'):
        d.require((ROOT/rel).read_bytes()==r15.git_bytes(BASE,rel),'Model table changed: '+rel)
    return commit


def read_profile(path):
    lines=Path(path).read_text().splitlines()
    d.require(lines and lines[0].startswith('# meta: '),'Profile metadata absent')
    meta=json.loads(lines[0][8:]);a=np.loadtxt(path)
    grid=np.tile(np.round(np.linspace(-.025,.025,51),3),3)
    d.require(a.shape==(153,2) and np.isfinite(a).all() and
        np.max(abs(a[:,0]-grid))<1e-12 and (a[:,1]>=0).all() and a[:,1].sum()>0,
        'Invalid frozen sigma profile')
    V=float(meta['volume [A^3]'])
    d.require(math.isfinite(V) and V>0,'Invalid cavity volume')
    return V


def table_inputs():
    rows=d.records(ROOT/'results/qc/dispersion.csv');tab={};bad=[]
    for r in rows:
        k=r['inchikey'];d.require(k and k not in tab,'Duplicate/missing dispersion identity')
        v=[d.number(r.get(c)) for c in ('C6_au','alpha_au')]
        tab[k]=v
        if any(q is None or q<=0 for q in v):bad.append(k)
    ers=d.records(ROOT/'results/qc/dielectric.csv');eps={}
    for r in ers:
        d.require(r['inchikey'] not in eps,'Duplicate dielectric identity')
        eps[r['inchikey']]=d.number(r['eps'])
    return tab,eps,dict(dispersion_rows=len(rows),invalid_descriptor_keys=bad)


def flag(v):
    if v in (True,'True','true','1',1):return True
    if v in (False,'False','false','0',0):return False
    raise ValueError('Ambiguous boolean metadata')


def guard_rows(path,kind,available):
    """Input-only eligibility, with every exclusion reason retained privately."""
    original=d.records(path);selected=[];exclusions=[]
    if kind=='negative':d.require(len(original)==336,'Not the original 336-state negative archive')
    for i,r in enumerate(original):
        if r.get('split') not in ('train','test_one','test_both'):
            raise ValueError('Unknown original split label')
        reason=None
        if r['split']=='train':reason='original_train'
        elif 'has_sigma' in r and not flag(r['has_sigma']):reason='original_no_sigma'
        cols=('solute','solvent') if kind=='idac' else ('c1','c2')
        keys=[r[c] for c in cols]
        T=d.number(r.get('T'))
        if reason is None and (T is None or not 250<=T<=450):reason='outside_temperature_scope'
        if reason is None and keys[0]==keys[1]:reason='self_pair'
        if reason is None:
            failures=[available(k) for k in keys]
            if any(q is not None for q in failures):reason='input_unavailable:'+','.join(q or 'ok' for q in failures)
        if reason:
            exclusions.append(dict(row_id=f'{kind}:{i}',reason=reason));continue
        out=dict(row_id=f'{kind}:{i}',keys=keys,T=T,system='|'.join(sorted(keys)))
        if kind=='idac':
            out.update(x1=0.,truth=d.number(r.get('ln_gamma_inf')))
        elif kind=='he':
            out.update(x1=d.number(r.get('x1')),truth=d.number(r.get('HE_J')))
            d.require(out['x1'] is not None and 0<out['x1']<1,'Invalid HE composition')
        elif kind=='positive':
            x=d.number(r.get('x1'));d.require(x is not None and 0<=x<=1,'Invalid LLE observation')
            out.update(T=float(round(T/2)*2),observed_T=T,observed_x1=x)
        if kind in ('idac','he'):d.require(out['truth'] is not None,'Invalid original response')
        selected.append(out)
    d.require(selected,'Empty fixed '+kind+' guard collection')
    if kind=='negative':d.require(len({r['system'] for r in selected})==len(selected),'Duplicate negative systems')
    return selected,dict(original_rows=len(original),eligible_rows=len(selected),exclusions=exclusions)


def queries(task):
    k=task['kind'];out=[]
    if k in ('vle','idac','he'):
        for r in task['members']:
            offsets=(-DESIGN['he_dT_K'],DESIGN['he_dT_K']) if k=='he' else (0.,)
            for j,dt in enumerate(offsets):
                out.append(dict(query_id=r['row_id']+':'+str(j),T=r['T']+dt,x1=r['x1']))
    else:
        out=[dict(query_id=f'grid:{i}',T=task['T'],x1=float(x)) for i,x in enumerate(stats.grid_union())]
    return out


def tasks_for(vle,guards):
    tasks=[]
    for kind,rows in [('vle',vle),*((k,guards[k]) for k in ('idac','he','positive','negative'))]:
        groups={}
        for r in rows:
            key=tuple(r['keys'])+((r['T'],) if kind in ('positive','negative') else ())
            groups.setdefault(key,[]).append(r)
        for key,members in sorted(groups.items()):
            t=dict(id=f'job-{len(tasks):05d}',kind=kind,keys=list(key[:2]),members=members)
            if kind in ('positive','negative'):t['T']=float(key[2])
            t['queries']=queries(t);tasks.append(t)
    return tasks


def freeze(a):
    d.mac();reg=registration(a.registration)
    prior=argparse.Namespace(plan=a.r15_plan,plan_commit=a.r15_plan_commit,run=a.r15_run)
    d.require(r15.check(prior)==0,'P54 saved check failed')
    oldp,oldm=r15.load(a.r15_plan,a.r15_plan_commit)
    vals,n,hashes=r15.arrays(oldm,a.r15_run,d.sha(oldp))
    d.require(n==7704 and len(oldm['rows'])==963 and r15.anchor(oldm,vals)['passed'],
              'Not the complete original P54 experiment')
    tab,eps,census=table_inputs();profiles=dict(oldm['profiles']);volumes={};rejected={}
    def available(k):
        if k in rejected:return rejected[k]
        if k not in tab or any(v is None or v<=0 for v in tab[k]):reason='dispersion'
        elif k not in eps or eps[k] is None or eps[k]<1:reason='dielectric'
        else:
            try:
                p=Path(profiles[k]) if k in profiles else r14.profile_path(k,a.ud_profiles)
                volumes[k]=read_profile(p);profiles[k]=str(p.resolve());return None
            except (OSError,ValueError,KeyError):reason='profile'
        rejected[k]=reason;return reason
    vle=[]
    for i,r in enumerate(oldm['rows']):
        keys=[r['c1'],r['c2']]
        d.require(all(available(k) is None for k in keys),'P54 input missing; no row removal')
        vle.append(dict(r,keys=keys,truth=r['P'],expected_P=float(vals[i,0]),reference_P=float(vals[i,7])))
    d.require(len({r['row_id'] for r in vle})==963 and len({r['system'] for r in vle})==100,'P54 identity changed')
    guards={};coverage={}
    input_paths={k:Path(getattr(a,k)).expanduser().resolve() for k in ('idac','he','positive','negative')}
    # Copies are permitted, a changed benchmark or newly selected split is not.
    for kind,rel in (('idac','data/benchmark/idac.csv'),('he','data/benchmark/he.csv'),
                     ('positive','data/benchmark/lle.csv')):
        d.require(input_paths[kind].read_bytes()==r15.git_bytes(BASE,rel),
                  'Guard is not the frozen original benchmark: '+kind)
    for kind,p in input_paths.items():guards[kind],coverage[kind]=guard_rows(p,kind,available)
    d.require(any(abs(r['truth'])>20 for r in guards['he']), 'HE sign guard has no eligible rows')
    tasks=tasks_for(vle,guards);request_count=sum(len(t['queries']) for t in tasks)
    d.require(request_count<=DESIGN['max_baseline_requests'],'Full fixed screen exceeds budget; no automatic downsampling')
    pairs={};old_terms=[]
    for keys in sorted({tuple(t['keys']) for t in tasks}):
        q=law.LondonPair(tuple(tab[k][0] for k in keys),tuple(tab[k][1] for k in keys),tuple(volumes[k] for k in keys))
        pairs['|'.join(keys)]=dict(c6=list(q.c6),alpha=list(q.alpha),volumes=list(q.volumes))
        if any(tuple(r['keys'])==keys for r in vle):old_terms.append(dict(keys=list(keys),**q.old_audit()))
    # P57 is an old-formula audit only. Candidate coefficients are first consumed
    # by post-run analysis under the committed LV1 plan; no score is made here.
    sources=[*(ROOT/r for r in FILES),*list((ROOT/'src/zcosmo').glob('*.py'))]
    sources += [ROOT/'results/qc/dispersion.csv',ROOT/'results/qc/dielectric.csv',ROOT/'results/z_params/Z0.json']
    sources += [ROOT/'scripts/r14_dielectric.py',ROOT/'scripts/r14_oracle.py',
                ROOT/'scripts/r15_factorial.py',ROOT/'scripts/r15_math.py']
    worker_inputs=d.fingerprint(sources)
    inputs=dict(oldm['inputs']);inputs.update(hashes);inputs.update(worker_inputs)
    inputs.update(d.fingerprint([oldp,oldp.parent/'execution_claim.json',Path(a.r15_run)/'summary.json',
        Path(a.r15_run)/'public-errors.json',*input_paths.values(),*profiles.values()]))
    out=d.private(a.out,True)
    d.write(out/'audit-private.json',dict(descriptor_census=census,pairs=old_terms,
        activity_calls=0,QCs=0,energy_terms_are_not_error_attributions=True))
    inputs.update(d.fingerprint([out/'audit-private.json']))
    m=dict(schema='r16-lv1-v1',base=BASE,registration=reg,design=DESIGN,environment=d.environment(),
        inputs=inputs,worker_inputs=worker_inputs,profiles=profiles,pairs=pairs,tasks=tasks,
        source_P54=dict(plan=str(oldp),commit=a.r15_plan_commit,run=str(Path(a.r15_run).resolve())),
        protected_counts=oldm['protected_counts'],coverage=coverage,baseline_requests=request_count,
        exposure=dict(old_compound_split='already exposed',temporal='not rescored; already exposed',
          P54='963 exposed VLE rows; unchanged',custodian_holdout=None,recipe_fixed=law.RECIPE,
          may_claim_unexposed=False,may_adopt=False))
    d.check_inputs(inputs);d.write(out/'plan.json',m)
    (out/'PLAN_SHA256.txt').write_text(d.sha(out/'plan.json')+'\n')
    print('R16 private plan frozen; baseline request budget:',request_count)


def load(plan,commit,full=True):
    d.mac();p=d.private(plan);m=d.read(p);registration(m['registration'])
    r15.ancestor(commit);r15.ancestor(m['registration'],commit)
    d.require(r15.git_bytes(commit,'docs/astra/round16/PLAN_SHA256.txt').decode().strip()==d.sha(p),
              'Plan digest not committed or changed')
    d.require(m['schema']=='r16-lv1-v1' and m['base']==BASE and m['design']==DESIGN,'Design drift')
    d.require(m['environment']==d.environment(),'Environment drift')
    d.require(m['protected_counts']=={'profiles_v2':630,'s1_stalled':1,'s2_stalled':5},'Frozen population drift')
    d.require(m['baseline_requests']==sum(len(t['queries']) for t in m['tasks'])<=DESIGN['max_baseline_requests'],
              'Budget drift')
    for t in m['tasks']:d.require(t['queries']==queries(t),'Query identity drift')
    d.check_inputs(m['inputs'] if full else m['worker_inputs'])
    return p,m


def native_baseline(keys,profiles):
    from zcosmo.z0x import Z0xBinary
    from zcosmo.cosmosac import load_fluid,sigma_path
    for k in keys:
        d.require(sigma_path(k).resolve()==Path(profiles[k]).resolve(),'Silent profile fallback')
        d.require(load_fluid(k).V==read_profile(profiles[k]),'Profile volume mismatch')
    base=Z0xBinary(keys);pr=base.z0
    d.require(pr.z==10. and pr.w_dsp==1. and pr.disp_mode=='london' and base.H==1e-4,
              'Unexpected baseline London/derivative prescription')
    return base


def worker(a):
    p,m=load(a.plan,a.plan_commit,False);task=next(t for t in m['tasks'] if t['id']==a.job)
    claim=d.read(p.parent/'execution_claim.json');out=d.private(a.out)
    d.require(claim==dict(plan_sha256=d.sha(p),output=str(out.parent)),'Worker outside claimed run')
    d.require(out.name==task['id'],'Wrong worker directory')
    checks={m['profiles'][k]:m['inputs'][str(Path(m['profiles'][k]).resolve())] for k in task['keys']}
    d.check_inputs(checks);out=d.private(out,True);overlay=out/'overlay';overlay.mkdir(mode=0o700)
    for key in list(os.environ):
        if key.startswith('ZC_'):os.environ.pop(key)
    os.environ['ZC_SIGMA_OVERRIDE_DIR']=str(overlay);os.environ['ZC_R6_ENDPOINT']='1'
    for k in task['keys']:(overlay/(k+'.sigma')).symlink_to(m['profiles'][k])
    base=native_baseline(task['keys'],m['profiles'])
    values=[]
    for j,q in enumerate(task['queries']):
        d.write(out/f'attempt-{j:05d}.json',dict(query_id=q['query_id'],attempted=True))
        value=None;error=None
        try:
            lg=np.asarray(base.lngamma(q['T'],np.array([q['x1'],1-q['x1']])),float)
            d.require(lg.shape==(2,) and np.isfinite(lg).all(),'Nonfinite baseline')
            value=lg.tolist()
        except Exception as ex:error=type(ex).__name__
        values.append(dict(query_id=q['query_id'],lngamma=value,error=error))
    d.check_inputs(checks);d.check_inputs(m['worker_inputs'])
    d.write(out/'result.json',dict(job=task['id'],plan_sha256=d.sha(p),values=values))


def arrays(m,run,ph):
    run=Path(run);raw={};hashes={};n=0
    states={'not_started','not_run_budget','blocked_anchor','returned','timeout','launch_failed'}
    for t in m['tasks']:
        tp=run/(t['id']+'.terminal.json');term=d.read(tp);hashes.update(d.fingerprint([tp]))
        d.require(term['job']==t['id'] and term['plan_sha256']==ph and term['state'] in states,'Terminal identity drift')
        folder=run/t['id'];attempts=sorted(folder.glob('attempt-*.json'))
        d.require(len(attempts)<=len(t['queries']),'Request budget exceeded')
        for j,f in enumerate(attempts):
            d.require(f.name==f'attempt-{j:05d}.json' and d.read(f)==dict(query_id=t['queries'][j]['query_id'],attempted=True),
                      'Attempt receipt drift')
        n+=len(attempts);hashes.update(d.fingerprint(attempts))
        a=np.full((len(t['queries']),2),np.nan);dest=folder/'result.json'
        if term['state']=='returned' and term['returncode']==0 and dest.is_file():
            z=d.read(dest);hashes.update(d.fingerprint([dest]))
            d.require(z['job']==t['id'] and z['plan_sha256']==ph and len(attempts)==len(t['queries'])
                and [v['query_id'] for v in z['values']]==[q['query_id'] for q in t['queries']], 'Result identity drift')
            for j,v in enumerate(z['values']):
                if v['lngamma'] is not None:
                    g=np.asarray(v['lngamma'],float);d.require(g.shape==(2,), 'Wrong component dimension');a[j]=g
        raw[t['id']]=a
    d.require(n<=m['baseline_requests'],'Actual request budget exceeded')
    return raw,n,hashes


def anchor(m,raw):
    err=[];finite=0;requested=0
    for t in m['tasks']:
        if t['kind']!='vle':continue
        for r,lg in zip(t['members'],raw[t['id']]):
            requested+=1
            if not np.isfinite(lg).all():continue
            try:p=r14.pressure(lg,r['x1'],r['psat'])
            except (ValueError,FloatingPointError):continue
            e=abs(p/r['expected_P']-1)
            if math.isfinite(e):err.append(e);finite+=1
    value=max(err) if finite==requested and requested else None
    return dict(requested=requested,finite=finite,max_relative_error=value,
        passed=value is not None and value<DESIGN['baseline_relative_pressure_tolerance'])


def analyze(m,raw):
    ar=anchor(m,raw)
    counts={k:dict(requested=0,finite=0) for k in ('vle','idac','he','positive','negative')}
    for t in m['tasks']:
        counts[t['kind']]['requested']+=len(t['queries'])
        counts[t['kind']]['finite']+=int(np.isfinite(raw[t['id']]).all(1).sum())
    status=dict(anchor=ar,query_coverage=counts,complete=False,adopted=False,
                exposed=True,recipe=law.RECIPE,QC_calls=0)
    if not ar['passed'] or any(v['requested']!=v['finite'] for v in counts.values()):
        return dict(status=status,scores=None,acceptance=None,private_predictions=None)
    records={k:[] for k in counts};uncertain=[]
    try:
        for t in m['tasks']:
            ch=law.DispersionChange(law.LondonPair(**m['pairs']['|'.join(t['keys'])]))
            b=raw[t['id']]
            c=np.array([lg+ch.delta(q['T'],[q['x1'],1-q['x1']],exact_endpoint=True)
                        for q,lg in zip(t['queries'],b)])
            d.require(np.isfinite(c).all(),'Candidate arithmetic overflow')
            if t['kind'] in ('positive','negative'):
                ds=[stats.detection(z) for z in (b,c)]
                if any(z['detected'] is None for z in ds):uncertain.append(t['id'])
                for r in t['members']:
                    records[t['kind']].append(dict(row_id=r['row_id'],system=r['system'],
                        values=[z['detected'] for z in ds],diagnostics=ds))
            else:
                for j,r in enumerate(t['members']):
                    if t['kind']=='vle':
                        pred=[r14.pressure(z[j],r['x1'],r['psat']) for z in (b,c)]
                    elif t['kind']=='idac':pred=[float(z[j,0]) for z in (b,c)]
                    else:
                        x=np.array([r['x1'],1-r['x1']]);dt=DESIGN['he_dT_K']
                        pred=[float(-8.314462618*r['T']**2*(x@(z[2*j+1]-z[2*j]))/(2*dt)) for z in (b,c)]
                    d.require(np.isfinite(pred).all(),'Nonfinite derived property')
                    z=dict(row_id=r['row_id'],system=r['system'],truth=r['truth'],values=pred)
                    if t['kind']=='vle':z['reference_P']=r['reference_P']
                    records[t['kind']].append(z)
    except (ValueError,FloatingPointError,OverflowError) as ex:
        status['analysis_error']=type(ex).__name__
        return dict(status=status,scores=None,acceptance=None,private_predictions=records)
    status['unresolved_grid_jobs']=uncertain
    if uncertain:return dict(status=status,scores=None,acceptance=None,private_predictions=records)
    try:
        scores={}
        for kind in ('vle','idac','he'):
            r=records[kind]
            scores[kind]=stats.paired_summary([v['truth'] for v in r],[v['values'] for v in r],
                          [v['system'] for v in r],kind,percent=kind=='vle')
        vr=records['vle']
        scores['vle_vs_2010']=stats.paired_summary([v['truth'] for v in vr],
            [[v['reference_P'],v['values'][1]] for v in vr],[v['system'] for v in vr], 'vle_vs_2010',True)
        scores['lle']=stats.lle_summary([(r['system'],*r['values']) for r in records['positive']],
                                       [(r['system'],*r['values']) for r in records['negative']])
        # HE sign is retained as an additional no-worsening point-estimate guard.
        hr=[r for r in records['he'] if abs(r['truth'])>20.]
        d.require(hr,'No HE sign-control rows')
        sign=[float(np.mean([np.sign(r['values'][j])==np.sign(r['truth']) for r in hr])) for j in (0,1)]
        scores['he']['sign_correct']=sign;scores['he']['sign_rows']=len(hr)
        result=stats.gates(scores)
        result['checks']['he_sign_does_not_worsen']=sign[1]>=sign[0]
        result['passed']=all(result['checks'].values())
        ref=scores['vle_vs_2010']
        result['gap_closed_on_exposed_panel']=ref['change']<=0 and ref['delta_one_sided_upper95']<=0
        status['complete']=True
        return dict(status=status,scores=scores,acceptance=result,private_predictions=records)

    except (ValueError,FloatingPointError,OverflowError) as ex:
        status['analysis_error']=type(ex).__name__
        return dict(status=status,scores=None,acceptance=None,private_predictions=records)


def public(q):
    return dict(status=q['status'],scores=q['scores'],acceptance=q['acceptance'],
                statement='exposed one-recipe screen; no automatic production adoption')


def collect(a):
    p,m=load(a.plan,a.plan_commit);run=d.private(a.run)
    d.require(d.read(p.parent/'execution_claim.json')==dict(plan_sha256=d.sha(p),output=str(run)),'Claim drift')
    raw,n,h=arrays(m,run,d.sha(p));q=analyze(m,raw);d.check_inputs(m['inputs'])
    d.write(run/'private-predictions.json',q['private_predictions'])
    d.write(run/'summary.json',dict(plan_sha256=d.sha(p),baseline_requests=n,output_hashes=h,**public(q)))
    d.write(run/'public-errors.json',public(q))
    print('R16 complete:',q['status']['complete'],'screen passed:',q['acceptance'] and q['acceptance']['passed'])
    return 0 if q['status']['complete'] else 2


def run(a):
    p,m=load(a.plan,a.plan_commit);out=d.private(a.out)
    d.require(not out.exists(),'Output already exists')
    d.write(p.parent/'execution_claim.json',dict(plan_sha256=d.sha(p),output=str(out)))
    out=d.private(out,True);start=time.monotonic();env=dict(os.environ)
    env.update(OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1')
    for t in m['tasks']:
        d.write(out/(t['id']+'.terminal.json'),dict(job=t['id'],plan_sha256=d.sha(p),state='not_started',returncode=None))
    ar=None
    for t in m['tasks']:
        if t['kind']!='vle' and ar is None:ar=anchor(m,arrays(m,out,d.sha(p))[0])
        remain=DESIGN['driver_seconds']-(time.monotonic()-start)
        term=dict(job=t['id'],plan_sha256=d.sha(p),state='not_run_budget',returncode=None)
        if t['kind']!='vle' and not ar['passed']:term['state']='blocked_anchor'
        elif remain>1:
            cmd=[sys.executable,str(Path(__file__).resolve()),'_worker','--plan',str(p),
                 '--plan-commit',a.plan_commit,'--job',t['id'],'--out',str(out/t['id'])]
            try:term.update(r14.launch(cmd,out/(t['id']+'.log'),min(remain,DESIGN['worker_seconds']),env))
            except Exception:term['state']='launch_failed'
        tmp=out/(t['id']+'.terminal.tmp');d.write(tmp,term);os.replace(tmp,out/(t['id']+'.terminal.json'))
    native_seconds=time.monotonic()-start;closing=time.monotonic()
    rc=collect(argparse.Namespace(plan=str(p),plan_commit=a.plan_commit,run=str(out)))
    d.write(out/'timing.json',dict(baseline_model_wall_s=native_seconds,
        closing_readonly_wall_s=time.monotonic()-closing,total_driver_wall_s=time.monotonic()-start))
    return rc


def check(a):
    p,m=load(a.plan,a.plan_commit);run=d.private(a.run);z=d.read(run/'summary.json')
    d.require(d.read(p.parent/'execution_claim.json')==dict(plan_sha256=d.sha(p),output=str(run)),'Claim drift')
    raw,n,h=arrays(m,run,d.sha(p));q=analyze(m,raw)
    d.require(z==dict(plan_sha256=d.sha(p),baseline_requests=n,output_hashes=h,**public(q)), 'Saved summary drift')
    d.require(d.read(run/'private-predictions.json')==q['private_predictions'] and
              d.read(run/'public-errors.json')==public(q), 'Derived outputs drift')
    print('R16 checked without new model queries. Complete:',q['status']['complete'])
    return 0 if q['status']['complete'] else 2


def main():
    ap=argparse.ArgumentParser(description=__doc__);sp=ap.add_subparsers(dest='cmd',required=True)
    q=sp.add_parser('freeze');q.add_argument('--registration',required=True)
    for arg in ('r15-plan','r15-plan-commit','r15-run','idac','he','positive','negative','ud-profiles','out'):
        q.add_argument('--'+arg,required=True)
    q.set_defaults(fn=freeze)
    for name,fn in (('run',run),('collect',collect),('check',check),('_worker',worker)):
        q=sp.add_parser(name);q.add_argument('--plan',required=True);q.add_argument('--plan-commit',required=True)
        q.add_argument('--run' if name in ('collect','check') else '--out',required=True)
        if name=='_worker':q.add_argument('--job',required=True)
        q.set_defaults(fn=fn)
    a=ap.parse_args();return a.fn(a)

if __name__=='__main__':raise SystemExit(main())
