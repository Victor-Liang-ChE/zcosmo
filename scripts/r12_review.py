"""P46/P47: one private Mac-only scoring replay or sigma-region audit, zero QC.

Do not publish plans, dense profiles, row predictions or logs. Only
public-errors.json from P46 is eligible for a separate human publication review.
"""
from __future__ import annotations
import argparse
from contextlib import redirect_stdout, redirect_stderr
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import traceback
import numpy as np
import pandas as pd
import r10_sources as src
import r10_replay as replay
import r11_cross as cross
import r12_analysis as ana

ROOT = Path(__file__).resolve().parents[1]
BASE = 'a93a1c9abbec32e0af7ff259a8db6fa550bb34a9'
MARKER = 'R12-P46-P47-P48: private explanatory scoring and regional accounting'
SCHEMA = 'R12-explanation-v1'
RECORDS = {k:f'docs/astra/round12/{k.upper()}_PLAN_SHA256.txt' for k in ('factorial','regions')}
MODEL_FILES = ['src/zcosmo/cosmosac.py','src/zcosmo/z0x.py','src/zcosmo/models.py',
               'src/zcosmo/zmodel.py','src/zcosmo/baselines.py']
FILES = ['scripts/r12_review.py','scripts/r12_analysis.py','scripts/r4_glycols.py',
         *cross.FILES, *MODEL_FILES]
FILES = list(dict.fromkeys(FILES))
TABLES = {'dielectric':'results/qc/dielectric.csv',
          'dispersion':'results/qc/dispersion.csv','Z0':'results/z_params/Z0.json'}
DESIGN = dict(P21_rows=332,P21_solvents=13,scored_glycol_rows=142,
    targets=ana.GLYCOLS,legacy_requests=284,exact_requests=1278,
    maximum_requests=1562,seconds_per_worker=120,total_model_seconds=7200,
    workers_in_parallel=1,legacy_tolerance=ana.PARITY_TOL,identity_tolerance=ana.IDENTITY_TOL,
    primary_endpoint='P28_exact',SCF_calls=0,gradients=0,no_retries=True,
    band_millithresholds=[-10,-5,5,10],R11_labels_unchanged=True)
sha, read, write = src.sha, src.read, src.write


def canonical(x):
    return json.loads(json.dumps(x,sort_keys=True,allow_nan=False))


def private(path,fresh=False):
    return cross.private_path(path,fresh=fresh)


def reg_check(commit):
    if not re.fullmatch('[0-9a-f]{40}',commit):raise ValueError('Full registration commit required')
    src.git('merge-base','--is-ancestor',BASE,'HEAD')
    src.git('merge-base','--is-ancestor',commit,'HEAD')
    b = src.git('show',commit+':PREREGISTRATION.md')
    if MARKER.encode() not in b:raise ValueError('R12 registration marker missing')
    return dict(commit=commit,preregistration_sha256=hashlib.sha256(b).hexdigest())


def r11_evidence(plan,commit,run):
    # The original checker performs no new SCF or activity-model call.
    with redirect_stdout(sys.stderr):
        cross.check(argparse.Namespace(plan=str(plan),plan_commit=commit,run=str(run)))
        _p,m,by,_s = cross.load_plan(plan,commit)
    d = read(Path(run)/'summary.json')
    return m,by,d


def frame(path):
    d = pd.read_csv(path,dtype={'r3_row_id':str},float_precision='round_trip')
    if 'r3_row_id' not in d or d.r3_row_id.isna().any() or d.r3_row_id.duplicated().any():
        raise ValueError('Missing/duplicate P21 observation IDs')
    return d


def same_rows(a,b):
    if set(a.r3_row_id)!=set(b.r3_row_id):raise ValueError('P21 row identities differ')
    aa=a.set_index('r3_row_id');bb=b.set_index('r3_row_id').loc[aa.index]
    for f in ('solute','solvent'):
        if not np.array_equal(aa[f].to_numpy(),bb[f].to_numpy()):raise ValueError('P21 ordered-pair drift')
    for f in ('T','ln_gamma_inf'):
        if not np.array_equal(aa[f].to_numpy(float),bb[f].to_numpy(float)):
            raise ValueError('P21 temperature/observation drift')


def p21_inputs(folder,open_dir,ud_dir):
    """Use the original P21 archive, including its per-pair input receipts."""
    folder=Path(folder).resolve();open_dir=Path(open_dir).resolve();ud_dir=Path(ud_dir).resolve()
    d=frame(folder/'factorial_rows.csv');s=read(folder/'summary.json')
    if len(d)!=332 or d.solvent.nunique()!=13 or s['rows']!=332 or s['finite_all']!=332:
        raise ValueError('P21 universe or recorded completeness changed')
    if not np.isfinite(d[['T','ln_gamma_inf',*ana.CORNERS,'UD']].to_numpy(float)).all():
        raise ValueError('The recorded P21 comparison is not fully finite')
    if (d['T']<=0).any() or (d.solute==d.solvent).any():raise ValueError('Invalid P21 states')
    if abs(d['111'].to_numpy(float)-d['UD'].to_numpy(float)).max()>=ana.IDENTITY_TOL:
        raise ValueError('Archived P21 111/full-UD identity failed')
    for key,(_name,n) in ana.GLYCOLS.items():
        if int((d.solvent==key).sum())!=n:raise ValueError('P21 glycol membership differs')
    protected=[src.record(folder/'factorial_rows.csv'),src.record(folder/'summary.json')]
    cases=[];parts=[]
    for part in sorted(folder.glob('pair-*')):
        q=frame(part/'rows.csv');same_rows(q,d[d.r3_row_id.isin(q.r3_row_id)])
        if len(q[['solute','solvent']].drop_duplicates())!=1:raise ValueError('Not one P21 pair')
        solute,solvent=q[['solute','solvent']].iloc[0].tolist()
        op=open_dir/(solvent+'.sigma');sp=open_dir/(solute+'.sigma')
        up=replay.historical_ud_path(ud_dir,solvent)
        protected.append(src.record(part/'rows.csv'))
        for corner in (*ana.CORNERS,'UD'):
            pred=frame(part/(corner+'.csv')).set_index('r3_row_id')
            wanted=d.set_index('r3_row_id').loc[q.r3_row_id,corner].to_numpy(float)
            if set(pred.index)!=set(q.r3_row_id) or not np.isfinite(pred.value.to_numpy(float)).all():
                raise ValueError('P21 per-corner identity/finite mismatch')
            if abs(pred.loc[q.r3_row_id,'value'].to_numpy(float)-wanted).max()>1e-12:
                raise ValueError('P21 aggregate differs from its per-pair output')
            receipt=part/(corner+'.csv.inputs.json');r=read(receipt)
            expected=dict(open_solvent=sha(op),open_solute=sha(sp),UD_solvent=sha(up),
                          **{k:sha(ROOT/v) for k,v in TABLES.items()})
            if r!=expected:raise ValueError('P21 profile/parameter hashes differ; recover originals, no fallback')
            protected.extend([src.record(part/(corner+'.csv')),src.record(receipt)])
        cases.append(dict(solute=solute,solvent=solvent,
            rows=q[['r3_row_id','T']].to_dict('records'),
            open_solvent=src.record(op),open_solute=src.record(sp),UD_solvent=src.record(up)))
        parts.append(q)
    if not parts:raise ValueError('Original P21 per-pair archive unavailable')
    allparts=pd.concat(parts,ignore_index=True)
    if allparts.r3_row_id.duplicated().any():raise ValueError('Duplicate P21 pair observation')
    same_rows(d,allparts)
    if len({(r['solute'],r['solvent']) for r in cases})!=len(cases):raise ValueError('Duplicate P21 pair')
    protected.extend(src.record(ROOT/v) for v in TABLES.values())
    for r in cases:protected.extend(r[k] for k in ('open_solvent','open_solute','UD_solvent'))
    unique={r['path']:r for r in protected}
    # No outcome selects a member. This is a retrospective source-identity freeze.
    return d.to_dict('records'),cases,list(unique.values())


def jobs_for(cases):
    jobs=[]
    for phase in ('legacy','exact'):
        for case in cases:
            if case['solvent'] not in ana.GLYCOLS:continue
            for corner in (('000','UD') if phase=='legacy' else (*ana.CORNERS,'UD')):
                jobs.append(dict(id=f'job-{len(jobs):05d}',phase=phase,corner=corner,case=case))
    if sum(len(j['case']['rows']) for j in jobs)!=1562:
        raise ValueError('Fixed model request budget changed')
    return jobs


def freeze(a):
    cross.mac_only();os.umask(0o077)
    reg=reg_check(a.registration)
    oldplan=private(a.r11_plan);oldrun=private(a.r11_run)
    m,by,d=r11_evidence(oldplan,a.r11_plan_commit,oldrun)
    sources=src.committed_sources(FILES)
    inputs=[src.record(oldplan),src.record(oldrun/'summary.json'),src.record(oldrun/'public-summary.json')]
    for key in by:
        for arm in ('RO','RU'):
            inputs.append(src.record(oldrun/key/(arm+'.terminal.json')))
            inputs.extend(src.record(oldrun/key/arm/n) for n in ('result.json','segments.npz'))
    inputs += m['protected_population']
    plan=dict(schema=SCHEMA,base=BASE,registration=reg,task=a.task,design=canonical(DESIGN),
        r11_plan=src.record(oldplan),r11_run=str(oldrun),r11_plan_commit=a.r11_plan_commit,
        sources=sources,packages=cross.packages(),inputs=inputs,
        observed_R11_classification=d['classification'],adopted=False)
    if a.task=='factorial':
        if not a.p21_run or not a.p21_open_profiles:raise ValueError('Need the original P21 archive and original open profiles')
        uds={str(Path(r['UD_profile']['path']).parent.resolve()) for r in by.values()}
        if len(uds)!=1:raise ValueError('Ambiguous original UD directory')
        rows,cases,files=p21_inputs(a.p21_run,a.p21_open_profiles,next(iter(uds)))
        # UD files for the scored targets must be the same lineage checked in R11.
        for c in cases:
            if c['solvent'] in ana.GLYCOLS and c['UD_solvent']['sha256']!=by[c['solvent']]['UD_profile']['sha256']:
                raise ValueError('P21/R11 UD lineage differs')
        plan.update(rows=rows,cases=cases,jobs=jobs_for(cases));plan['inputs']+=files
        compounds=ROOT/'data/benchmark/compounds.csv';plan['inputs'].append(src.record(compounds))
        cd=pd.read_csv(compounds)
        if cd.inchikey.duplicated().any():raise ValueError('Duplicate compound identity')
        lookup=dict(zip(cd.inchikey,cd.smiles))
        keys={k for c in cases for k in (c['solute'],c['solvent'])}
        if not keys<=set(lookup):raise ValueError('P21 molecule missing from fixed compound table')
        plan['smiles']={k:lookup[k] for k in sorted(keys)}
    plan['inputs']=list({z['path']:z for z in plan['inputs']}.values())
    out=private(a.out,fresh=True);out.mkdir(parents=True,mode=0o700)
    write(out/'plan.json',plan);(out/'PLAN_SHA256.txt').write_text(sha(out/'plan.json')+'\n')
    print('Private',a.task,'plan digest:',sha(out/'plan.json'))
    return 0


def load_plan(path,commit,full=True):
    cross.mac_only();p=private(path);m=read(p)
    if m.get('schema')!=SCHEMA or m.get('base')!=BASE or m.get('design')!=canonical(DESIGN) or m.get('task') not in RECORDS:
        raise ValueError('Changed R12 design')
    if not re.fullmatch('[0-9a-f]{40}',commit):raise ValueError('Full plan-record commit required')
    src.git('merge-base','--is-ancestor',commit,'HEAD')
    src.git('merge-base','--is-ancestor',m['registration']['commit'],commit)
    if src.git('show',commit+':'+RECORDS[m['task']]).decode().strip()!=sha(p):raise ValueError('Plan was not committed before output')
    if reg_check(m['registration']['commit'])!=m['registration'] or cross.packages()!=m['packages']:
        raise ValueError('Registration/package drift')
    src.verify_sources(m['sources'])
    if m['task']=='factorial' and m['jobs']!=jobs_for(m['cases']):
        raise ValueError('Changed factorial job schedule')
    for r in m['inputs']:src.verify_record(r)
    if full:
        _old,_by,s=r11_evidence(m['r11_plan']['path'],m['r11_plan_commit'],m['r11_run'])
        if s['classification']!=m['observed_R11_classification']:raise ValueError('R11 labels changed')
    return p,m


def one_model_job(job,m,out):
    """One fresh worker, one ordered pair and one corner. No fitting input enters the model."""
    c=job['case'];out=Path(out);overlay=out/'overlay';overlay.mkdir(mode=0o700)
    for k in ('open_solvent','open_solute','UD_solvent'):src.verify_record(c[k])
    solute,solvent=c['solute'],c['solvent']
    (_s,o,om)=replay.read_profile(c['open_solvent']['path'])
    if job['phase']=='exact' and job['corner']!='UD':
        summary=read(Path(m['r11_run'])/'summary.json')
        r=next(v for v in summary['rows'] if v['key']==solvent)
        desc=r['descriptors']['RU'];other=ana.profile(desc['post_HB_bins_A2'])
        meta={'volume [A^3]':desc['volume_A3']}
    else:
        _s,other,meta=replay.read_profile(c['UD_solvent']['path'])
    (overlay/(solute+'.sigma')).symlink_to(Path(c['open_solute']['path']).resolve())
    if job['corner']=='UD':
        (overlay/(solvent+'.sigma')).symlink_to(Path(c['UD_solvent']['path']).resolve())
    else:
        bins,metadata=ana.hybrid(o,om,other,meta,job['corner'])
        metadata['standard_INCHIKEY']=solvent
        from r3_common import write_sigma
        write_sigma(overlay/(solvent+'.sigma'),ana.SIG,bins,metadata)
    # Never inherit another experiment's profile override or endpoint setting.
    for key in list(os.environ):
        if key.startswith('ZC_'):os.environ.pop(key)
    os.environ.update(ZC_SIGMA_OVERRIDE_DIR=str(overlay),
        ZC_R6_ENDPOINT='1' if job['phase']=='exact' else '0')
    from zcosmo.cosmosac import sigma_path
    for key in (solute,solvent):
        if Path(sigma_path(key)).resolve()!=(overlay/(key+'.sigma')).resolve():
            raise ValueError('A requested override fell back to another profile')
    from zcosmo.models import make_model
    model=make_model('Z0x',[solute,solvent],[m['smiles'][solute],m['smiles'][solvent]])
    values=[];attempted=0
    for row in c['rows']:
        attempted+=1
        write(out/'progress.json',dict(attempted_model_calls=attempted,requested=len(c['rows'])))
        try:
            y=float(model.lngamma_inf(float(row['T']),0))
            error='' if np.isfinite(y) else 'nonfinite_prediction'
        except Exception as e:
            y=float('nan');error=type(e).__name__
        values.append(dict(r3_row_id=str(row['r3_row_id']),value=y if np.isfinite(y) else None,error=error))
    return dict(values=values,attempted_model_calls=attempted,
                completed=all(v['value'] is not None for v in values))


def worker(a):
    cross.mac_only();os.umask(0o077)
    p=private(a.plan);m=read(p);claim=read(p.parent/'execution_claim.json')
    out=private(a.out,fresh=True)
    if (m.get('schema')!=SCHEMA or m['task']!='factorial' or m['design']!=canonical(DESIGN) or
        claim['plan_sha256']!=sha(p) or claim['nonce']!=os.environ.get('ZC_R12_NONCE') or
        claim['pid']!=os.getppid() or out!=Path(claim['output'])/a.job):
        raise ValueError('Only the single claimed parent run may invoke this worker')
    src.verify_sources(m['sources'])
    if cross.packages()!=m['packages']:raise ValueError('Worker package drift')
    for name in TABLES.values():
        matches=[z for z in m['inputs'] if Path(z['path']).resolve()==(ROOT/name).resolve()]
        if len(matches)!=1:raise ValueError('Missing or duplicate model-table fingerprint')
        src.verify_record(matches[0])
    for r in (m['r11_plan'],next(r for r in m['inputs'] if r['path']==str(Path(m['r11_run'])/'summary.json'))):
        src.verify_record(r)
    js=[j for j in m['jobs'] if j['id']==a.job]
    if len(js)!=1:raise ValueError('Unknown or repeated worker identity')
    out.mkdir(parents=True,mode=0o700)
    result=dict(job=a.job,plan_sha256=sha(p),completed=False,attempted_model_calls=0,values=[])
    try:
        result.update(one_model_job(js[0],m,out))
    except Exception:
        result['failure']='worker_exception';traceback.print_exc()
    write(out/'result.json',result)
    return 0 if result['completed'] else 2


def archived_arrays(m,run):
    rows=m['rows'];ids=[str(r['r3_row_id']) for r in rows];index={k:i for i,k in enumerate(ids)}
    target=[i for i,r in enumerate(rows) if r['solvent'] in ana.GLYCOLS]
    ti={ids[i]:j for j,i in enumerate(target)}
    arrays={'legacy':np.full((142,2),np.nan),'exact':np.full((142,9),np.nan)}
    receipt=[];used=set();run=Path(run)
    for job in m['jobs']:
        term=run/(job['id']+'.terminal.json');folder=run/job['id'];dest=folder/'result.json'
        state='missing';attempts=0;hashes={}
        if term.is_file():
            t=read(term);hashes['terminal']=sha(term)
            if t.get('job')!=job['id'] or t.get('plan_sha256')!=sha(m['_plan_path']):raise ValueError('Terminal identity changed')
            state=t['execution_state']
            if (not isinstance(t.get('wall_s'),(float,int)) or not np.isfinite(t['wall_s']) or
                t['wall_s']<0 or t['wall_s']>125.):
                raise ValueError('Invalid or over-budget worker receipt')
            if dest.is_file():
                q=read(dest);hashes['result']=sha(dest)
                if q.get('job')!=job['id'] or q.get('plan_sha256')!=t['plan_sha256']:
                    raise ValueError('Result identity changed')
                attempts=q['attempted_model_calls']
                if type(attempts) is not int or not 0<=attempts<=len(job['case']['rows']):
                    raise ValueError('Invalid per-worker model-call count')
                if q.get('values'):
                    wanted=[str(r['r3_row_id']) for r in job['case']['rows']]
                    got=[r['r3_row_id'] for r in q['values']]
                    if got!=wanted or attempts!=len(wanted):
                        raise ValueError('Completed worker lost identities or exceeded calls')
                    j=(('000','UD') if job['phase']=='legacy' else (*ana.CORNERS,'UD')).index(job['corner'])
                    for v in q['values']:
                        ident=(job['phase'],v['r3_row_id'],j)
                        if ident in used:raise ValueError('Duplicate factorial output')
                        used.add(ident)
                        i=ti[v['r3_row_id']]
                        arrays[job['phase']][i,j]=float(v['value']) if v['value'] is not None else np.nan
                    if q.get('completed') is True and t.get('returncode')==0:
                        if any(v['value'] is None or not np.isfinite(v['value']) for v in q['values']):
                            raise ValueError('Completed worker contains nonfinite predictions')
                        state='completed'
                    else:
                        state='failed'
            progress=folder/'progress.json'
            if progress.is_file():
                a=read(progress)['attempted_model_calls']
                if a<attempts or a>len(job['case']['rows']):raise ValueError('Invalid model-call receipt')
                attempts=a;hashes['progress']=sha(progress)
        receipt.append(dict(job=job['id'],state=state,attempted_model_calls=attempts,hashes=hashes))
    if sum(r['attempted_model_calls'] for r in receipt)>1562:raise ValueError('Model budget exceeded')
    return arrays,receipt


def public_scores(d):
    """Only aggregate errors and accounting. No paths, predictions, bins or R11 descriptors."""
    s=d['status']
    out={k:s[k] for k in ('complete','legacy_requested','legacy_finite','exact_requested','exact_finite',
        'legacy_parity_passed','legacy_max_error','model','endpoint','adopted')}
    out['interpretation']='Retrospective ThermoML explanatory scoring; no held-out claim, fitted improvement, or adoption'
    out['SCF_calls']=0
    def scalar(value):
        if value is None:return None
        if not isinstance(value,(int,float,bool)) or not np.isfinite(value):
            raise ValueError('Non-scalar data in public error summary')
        return value
    def metrics(q):
        names=('rows','MAE_removed_O_to_C','MAE_remaining_C_to_U','MAE_gap_O_to_U',
               'signed_recovery_fraction','improved_rows','worsened_rows')
        z={k:scalar(q[k]) for k in names}
        for name in ('O','C','U'):z[name]={k:scalar(q[name][k]) for k in ('MAE','bias')}
        for name in ('absolute_error_reduction_ShAP',):
            z[name]={k:scalar(q[name][k]) for k in ('area','volume','shape')}
        return z
    q=d['aggregate_errors']
    if q is None:
        out['aggregate_errors']=None
    else:
        solvents=[]
        if len(q['solvents'])!=4 or {r['key'] for r in q['solvents']}!=set(ana.GLYCOLS):
            raise ValueError('Changed public solvent universe')
        for r in q['solvents']:
            name,n=ana.GLYCOLS[r['key']]
            if r['name']!=name or r['rows']!=n:raise ValueError('Changed public solvent identity')
            v=dict(key=r['key'],name=name,**metrics(r))
            v['legacy_P21']={k:scalar(r['legacy_P21'][k]) for k in ('O_MAE','U_MAE')}
            v['endpoint_bridge']={k:scalar(r['endpoint_bridge'][k]) for k in ('O_MAE_change','U_MAE_change')}
            solvents.append(v)
        out['aggregate_errors']=dict(solvents=solvents,pooled=metrics(q['pooled']),
            equal_solvent_mean={k:scalar(q['equal_solvent_mean'][k]) for k in
                ('O_MAE','C_MAE','U_MAE','MAE_removed_O_to_C')},
            requested_P21_rows=332,audit_only_other_rows=190)
    return out


def collect(p,m,run):
    mm=dict(m,_plan_path=str(p));arrays,receipts=archived_arrays(mm,run)
    d=ana.explanatory_scores(m['rows'],arrays['legacy'],arrays['exact'])
    if any(r['state']!='completed' for r in receipts):
        d['status']['complete']=False;d['aggregate_errors']=None;d['private_rows']=[]
    d.update(plan_sha256=sha(p),receipts=receipts,attempted_model_calls=sum(r['attempted_model_calls'] for r in receipts))
    return d


def run_factorial(a):
    cross.mac_only();os.umask(0o077);p,m=load_plan(a.plan,a.plan_commit)
    if m['task']!='factorial':raise ValueError('Wrong family')
    out=private(a.out,fresh=True)
    if out.is_relative_to(p.parent) or p.parent.is_relative_to(out):raise ValueError('Separate plan and output directories')
    import secrets
    nonce=secrets.token_hex(24)
    claim=dict(plan_sha256=sha(p),plan_commit=a.plan_commit,output=str(out),pid=os.getpid(),nonce=nonce)
    with (p.parent/'execution_claim.json').open('x') as f:json.dump(claim,f)
    out.mkdir(parents=True,mode=0o700);start=time.monotonic();receipts=[]
    env={k:v for k,v in os.environ.items() if not k.startswith('ZC_')}
    env.update(OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',BLIS_NUM_THREADS='1',
        VECLIB_MAXIMUM_THREADS='1',NUMEXPR_NUM_THREADS='1',MPLBACKEND='Agg',ZC_R12_NONCE=nonce,
        PYTHONPATH=str(ROOT/'src')+os.pathsep+str(ROOT/'scripts'))
    legacy_ok=None
    for job in m['jobs']:
        if job['phase']=='exact' and legacy_ok is None:
            arrays,prior=archived_arrays(dict(m,_plan_path=str(p)),out)
            old=np.asarray([[r[c] for c in ('000','UD')] for r in m['rows'] if r['solvent'] in ana.GLYCOLS],float)
            legacy_ids={j['id'] for j in m['jobs'] if j['phase']=='legacy'}
            legacy_ok=bool(np.isfinite(arrays['legacy']).all() and abs(arrays['legacy']-old).max()<ana.PARITY_TOL and
                           all(r['state']=='completed' for r in prior if r['job'] in legacy_ids))
        remaining=7200-(time.monotonic()-start)
        t=dict(job=job['id'],plan_sha256=sha(p),execution_state='not_run_budget',returncode=None,wall_s=0.)
        if job['phase']=='exact' and legacy_ok is not True:
            t['execution_state']='blocked_legacy_gate'
        elif remaining>2:
            command=[sys.executable,str(ROOT/'scripts/r12_review.py'),'_worker',
                     '--plan',str(p),'--job',job['id'],'--out',str(out/job['id'])]
            try:t.update(cross.launch(command,out/(job['id']+'.log'),min(120.,remaining),env))
            except Exception:t.update(execution_state='launch_failed')
        write(out/(job['id']+'.terminal.json'),t);receipts.append(t)
    # End-of-run integrity is mandatory even for a scientific failure.
    model_run_wall=time.monotonic()-start;closing_start=time.monotonic()
    load_plan(p,a.plan_commit)
    d=collect(p,m,out)
    d.update(model_run_wall_s=model_run_wall,closing_check_wall_s=time.monotonic()-closing_start,
             driver_wall_s=time.monotonic()-start)
    write(out/'summary.json',d);write(out/'public-errors.json',public_scores(d))
    print('Private explanatory scoring completed:',d['status']['complete'],
          '; model requests attempted:',d['attempted_model_calls'])
    return 0 if d['status']['complete'] else 2


def regions(a):
    cross.mac_only();os.umask(0o077);p,m=load_plan(a.plan,a.plan_commit)
    if m['task']!='regions':raise ValueError('Wrong family')
    out=private(a.out,fresh=True)
    with (p.parent/'execution_claim.json').open('x') as f:json.dump(dict(plan_sha256=sha(p),output=str(out)),f)
    out.mkdir(parents=True,mode=0o700);start=time.monotonic()
    d=ana.regional_panel(read(Path(m['r11_run'])/'summary.json'));d['plan_sha256']=sha(p)
    load_plan(p,a.plan_commit)
    write(out/'regions-private.json',d)
    write(out/'receipt.json',dict(plan_sha256=sha(p),result_sha256=sha(out/'regions-private.json'),
          SCF_calls=0,model_calls=0,wall_s=time.monotonic()-start,requested_members=12))
    print('Private regional accounting completed for 12 members; R11 labels unchanged.')
    return 0


def check(a):
    p,m=load_plan(a.plan,a.plan_commit);run=private(a.run)
    claim=read(p.parent/'execution_claim.json')
    if Path(claim['output']).resolve()!=run or claim['plan_sha256']!=sha(p):raise ValueError('Different claimed run')
    if m['task']=='regions':
        d=ana.regional_panel(read(Path(m['r11_run'])/'summary.json'));d['plan_sha256']=sha(p)
        if d!=read(run/'regions-private.json') or sha(run/'regions-private.json')!=read(run/'receipt.json')['result_sha256']:
            raise ValueError('Regional results were not reproduced')
    else:
        d=collect(p,m,run);old=read(run/'summary.json')
        for field in ('model_run_wall_s','closing_check_wall_s','driver_wall_s'):
            value=old.pop(field,None)
            if not isinstance(value,(int,float)) or not np.isfinite(value) or value<0:
                raise ValueError('Missing or invalid timing receipt')
        if d!=old or public_scores(d)!=read(run/'public-errors.json'):
            raise ValueError('Scoring summary or receipts changed')
        if not d['status']['complete']:raise ValueError('Incomplete panel; no complete-score claim')
    print('Saved outputs independently checked without new model calls.')
    return 0


def main():
    if Path.cwd().resolve()!=ROOT:raise ValueError('Run from this checkout root')
    p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='cmd',required=True)
    q=s.add_parser('freeze');q.add_argument('--task',choices=RECORDS,required=True)
    q.add_argument('--registration',required=True);q.add_argument('--r11-plan',required=True)
    q.add_argument('--r11-plan-commit',required=True);q.add_argument('--r11-run',required=True)
    q.add_argument('--p21-run');q.add_argument('--p21-open-profiles');q.add_argument('--out',required=True);q.set_defaults(fn=freeze)
    for name,fn in (('run',run_factorial),('regions',regions),('check',check)):
        q=s.add_parser(name);q.add_argument('--plan',required=True);q.add_argument('--plan-commit',required=True)
        q.add_argument('--run' if name=='check' else '--out',required=True);q.set_defaults(fn=fn)
    q=s.add_parser('_worker');q.add_argument('--plan',required=True);q.add_argument('--job',required=True)
    q.add_argument('--out',required=True);q.set_defaults(fn=worker)
    return p.parse_args()

if __name__=='__main__':
    a=main();raise SystemExit(a.fn(a))
