"""Mac-side R7 gates. Fresh processes per target/profile set; historical occurrences retained."""
from __future__ import annotations
import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
import numpy as np
import pandas as pd
from r7_common import (BASE,PILOT,PROBES,sha,write,fresh,load_plan,find_result,
                       clean_environment,chain_decision,registration)

MODELS=('cosmosac_dsp','Z0x')


def worker(a):
    spec=json.loads(Path(a.spec).read_text());clean_environment()
    q=pd.read_csv(spec['queries']);q=q[q.target==spec['target']].copy()
    if q.empty or q.occurrence.duplicated().any():raise ValueError('Invalid target query identities')
    smi=pd.read_csv('data/benchmark/compounds.csv').set_index('inchikey').smiles.to_dict()
    target=spec.get('profile');background=spec.get('background');used={}
    with tempfile.TemporaryDirectory(prefix='r7-query-') as temp:
        d=Path(temp)
        if background:
            for k in set(q[['solute','solvent']].to_numpy().ravel()):
                src=Path(background)/(k+'.sigma')
                if not src.is_file():raise FileNotFoundError(f'No authorized open profile for {k}')
                (d/src.name).symlink_to(src.resolve())
        if target:
            dst=d/(spec['target']+'.sigma')
            if dst.is_symlink():dst.unlink()
            dst.symlink_to(Path(target).resolve())
        if target or background:os.environ['ZC_SIGMA_OVERRIDE_DIR']=temp
        from zcosmo.cosmosac import sigma_path,SIGMA_DIR
        if not background and not SIGMA_DIR.is_dir():raise FileNotFoundError('UD-backed gate must run on the Mac with UD assets')
        from zcosmo.models import make_model
        records=[];cache={}
        for r in q.itertuples():
            keys=(r.solute,r.solvent)
            for k in keys:
                p=sigma_path(k)
                if p is None:raise FileNotFoundError(k)
                if background and p.resolve()!=(d/(k+'.sigma')).resolve():raise ValueError('Unauthorized UD fallback')
                used[str(p.resolve())]=sha(p)
            for name in MODELS:
                try:
                    ck=(name,keys)
                    if ck not in cache:cache[ck]=make_model(name,list(keys),[smi[k] for k in keys])
                    y=float(cache[ck].lngamma_inf(float(r.T),0))
                    if not np.isfinite(y):raise ValueError('nonfinite model output')
                    error=''
                except Exception as e:y=None;error=type(e).__name__+': '+str(e)[:300]
                records.append(dict(occurrence=int(r.occurrence),target=r.target,solute=r.solute,
                    solvent=r.solvent,T=float(r.T),model=name,value=y,error=error))
        if any(sha(p)!=h for p,h in used.items()):raise ValueError('Profile changed during evaluation')
        write(a.out,dict(records=records,inputs=used,spec_sha256=sha(a.spec)))


def evaluate(qpath,target,p,out,background=None):
    spec=dict(queries=str(Path(qpath).resolve()),target=target,
              profile=str(Path(p).resolve()) if p else None,
              background=str(Path(background).resolve()) if background else None)
    sp=Path(out).with_suffix('.spec.json');write(sp,spec)
    subprocess.run([sys.executable,str(Path(__file__).resolve()),'worker','--spec',str(sp),
                    '--out',str(out)],check=True)
    return pd.DataFrame(json.loads(Path(out).read_text())['records'])


def aligned_values(frame,q,model):
    f=frame[frame.model==model].set_index('occurrence')
    if not f.index.is_unique or set(f.index)!=set(q.occurrence):raise ValueError('Missing, extra, or duplicate result occurrence')
    f=f.loc[q.occurrence]
    for c in ('target','solute','solvent'):
        if not np.array_equal(f[c].to_numpy(str),q[c].to_numpy(str)):raise ValueError('Query identity changed')
    if not np.array_equal(f['T'].to_numpy(float),q['T'].to_numpy(float)):raise ValueError('Query temperature changed')
    return pd.to_numeric(f.value,errors='raise').to_numpy(float)


def compare_arrays(reference,candidate):
    fr=np.isfinite(reference);fc=np.isfinite(candidate)
    same=np.array_equal(fr,fc)
    good=fr&fc
    return dict(coverage_identical=bool(same),requested=len(fr),finite_reference=int(fr.sum()),
        finite_candidate=int(fc.sum()),max_abs_change=float(np.max(abs(reference[good]-candidate[good]))) if good.any() else None,
        median_abs_change=float(np.median(abs(reference[good]-candidate[good]))) if good.any() else None)


def calibration(a):
    plan,m=load_plan(a.plan)
    if m['family']!='calibration' or len(m['cases'])!=25:raise ValueError('Expected complete historical 25 plan')
    qpath=plan.parent/m['queries']
    if sha(qpath)!=m['queries_sha256']:raise ValueError('Historical occurrences changed')
    q=pd.read_csv(qpath)
    if len(q)!=2302 or q.target.nunique()!=25:raise ValueError('Wrong historical universe')
    out=fresh(a.out);frames={x:[] for x in ('off','full','UD')};runs=[];bins=[];t=time.monotonic()
    for case in m['cases']:
        key=case['key'];pfiles={};native={};runtime={}
        for arm in ('off','full'):
            p,r=find_result(a.results,key,arm,sha(plan));native[arm]=r
            if r['status']!='berny_converged' or r.get('berny_converged') is not True:
                raise ValueError(f'{key}/{arm} did not pass the original Berny predicate')
            if r.get('grid_response')!=(arm=='full') or not 1<=r['evaluations']<=100:
                raise ValueError('Wrong gradient setting or evaluation budget')
            profile=p.parent/(key+'.sigma')
            if sha(profile)!=r['profile']['sha256']:raise ValueError('Trial profile changed')
            pfiles[arm]=profile
            rr=p.parent.with_name(p.parent.name+'.run.json')
            z=json.loads(rr.read_text())
            if z['execution_status']!='completed' or z['returncode']!=0:raise ValueError('Worker did not complete successfully')
            runtime[arm]=float(z['wall_s'])
            frames[arm].append(evaluate(qpath,key,profile,out/(key+'-'+arm+'.json')))
        if native['off']['input_geometry_sha256']!=native['full']['input_geometry_sha256'] or native['off']['packages']!=native['full']['packages']:
            raise ValueError('Paired inputs/environments differ')
        frames['UD'].append(evaluate(qpath,key,None,out/(key+'-UD.json')))
        from r3_common import read_sigma
        ps=[read_sigma(pfiles[k])[1] for k in ('off','full')]
        bins.append(dict(key=key,max_raw_bin=float(abs(ps[0]-ps[1]).max()),
            max_normalized_bin=float(abs(ps[0]/ps[0].sum()-ps[1]/ps[1].sum()).max()),
            normalized_L1=float(abs(ps[0]/ps[0].sum()-ps[1]/ps[1].sum()).sum())))
        runs.append(dict(key=key,wall_s=runtime,evaluations={k:native[k]['evaluations'] for k in native}))
    frames={k:pd.concat(v,ignore_index=True) for k,v in frames.items()};checks={}
    for model in MODELS:
        values={k:aligned_values(v,q,model) for k,v in frames.items()}
        checks[model]=dict(candidate_vs_control=compare_arrays(values['off'],values['full']),
                           candidate_vs_UD=compare_arrays(values['UD'],values['full']))
    off=sum(r['wall_s']['off'] for r in runs);full=sum(r['wall_s']['full'] for r in runs)
    dsp=checks['cosmosac_dsp'];z0=checks['Z0x']
    finite_ok=all(c['coverage_identical'] for x in checks.values() for c in x.values())
    expected=(dsp['candidate_vs_control']['finite_reference']==2271 and z0['candidate_vs_control']['finite_reference']==2302)
    passed=bool(finite_ok and expected and dsp['candidate_vs_control']['max_abs_change']<.01
                and dsp['candidate_vs_UD']['median_abs_change']<.15)
    report=dict(base=BASE,registration=m['registration'],passed=passed,plan_sha256=sha(plan),
        rows=2302,targets=25,checks=checks,bins=bins,runs=runs,
        gate_kind='P32_numerical_compatibility',
        routine_throughput_indicator=bool(full/off<=1.50),routine_throughput_limit=1.50,
        paired_worker_seconds=dict(off=off,full=full),wall_ratio=full/off,
        shared_xtb_seconds=sum(r['shared_xtb_seconds'] for r in m['cases']),
        timing_scope='Worker optimizer plus TZVP profile; one shared xTB preparation excluded from both arms',
        gate_elapsed_s=time.monotonic()-t,adopted=False)
    write(out/'gate.json',report)
    if not passed:raise SystemExit(2)


def decide(a):
    cal=json.loads(Path(a.calibration).read_text());plan,m=load_plan(a.pilot_plan)
    cp,cm=load_plan(a.chains_plan)
    if m['family']!='pilot' or cm['family']!='chains':raise ValueError('Wrong plan families')
    if cal['registration']!=m['registration'] or cm['registration']!=m['registration']:
        raise ValueError('Registrations differ')
    pilots={}
    for k in PILOT:
        pilots[k]={}
        for arm in ('off','full'):
            p,d=find_result(a.pilot_results,k,arm,sha(plan))
            status=d.get('status','missing')
            if d.get('evaluations',0)<1:status='operational_failure'
            if status=='censored_evaluations' and d.get('evaluations')!=80:status='operational_failure'
            if status=='berny_converged':
                if d.get('grid_response')!=(arm=='full') or d.get('berny_converged') is not True:
                    raise ValueError('Invalid pilot convergence record')
                if sha(p.parent/(k+'.sigma'))!=d['profile']['sha256']:raise ValueError('Pilot profile changed')
            pilots[k][arm]=status
    d=chain_decision(cal,pilots)
    d.update(base=BASE,registration=m['registration'],calibration_gate_sha256=sha(a.calibration),
        pilot_plan_sha256=sha(plan),chains_plan_sha256=sha(cp),
        not_a_conclusion_about='Untested chains, all 630 geometries, or the historical P30 gate')
    write(a.out,d)
    if not d['eligible_for_chain_trial']:raise SystemExit(2)


def affinities(a):
    """Compare one profile to its own reference, using fixed computational probes.

    Optional IDAC queries supply identities and temperatures only. No measured
    response is sent to workers. Background must be a complete open overlay.
    """
    registration(a.registration);out=fresh(a.out);rows=[]
    if a.idac:
        d=pd.read_csv(a.idac);d=d[(d.solute==a.key)|(d.solvent==a.key)]
        rows.extend(dict(target=a.key,solute=r.solute,solvent=r.solvent,T=float(r.T)) for r in d.itertuples())
    for k in PROBES:
        if k==a.key:continue
        for T in (250.,298.15,400.):
            for i,j in ((a.key,k),(k,a.key)):
                rows.append(dict(target=a.key,solute=i,solvent=j,T=T))
    q=pd.DataFrame(rows);q['occurrence']=np.arange(len(q));qp=out/'queries.csv';q.to_csv(qp,index=False)
    ref=evaluate(qp,a.key,a.reference,out/'reference.json',a.background);summaries=[]
    for i,p in enumerate(a.candidate):
        frame=evaluate(qp,a.key,p,out/f'candidate-{i}.json',a.background);check={}
        for model in MODELS:
            r=aligned_values(ref,q,model);c=aligned_values(frame,q,model);check[model]=compare_arrays(r,c)
        summaries.append(dict(profile=str(Path(p).resolve()),sha256=sha(p),models=check,
            passed=all(v['coverage_identical'] and v['max_abs_change'] is not None and v['max_abs_change']<a.limit for v in check.values())))
    report=dict(key=a.key,registration=a.registration,reference_sha256=sha(a.reference),
        limit=a.limit,rows=len(q),candidates=summaries,passed=all(x['passed'] for x in summaries),
        scope='Finite fixed query set; not a bound on all compositions, temperatures, or geometries')
    write(out/'gate.json',report)
    if not report['passed']:raise SystemExit(2)



def replacements(a):
    from argparse import Namespace
    from r7_common import STALL
    plan,m=load_plan(a.plan);registration(a.authorization)
    permit=json.loads(Path(a.permit).read_text())
    if m['family']!='chains' or permit.get('eligible_for_chain_trial') is not True:
        raise ValueError('No approved bounded chain trial')
    if permit.get('chains_plan_sha256')!=sha(plan):raise ValueError('Chain inputs differ from approval')
    evidence={(k,arm):find_result(a.results,k,arm,sha(plan)) for k in STALL for arm in ('off','full')}
    out=fresh(a.out);records=[]
    for k in STALL:
        p,d=evidence[k,'full'];_,old=evidence[k,'off']
        row=dict(key=k,off_status=old['status'],full_status=d['status'],replacement_eligible=False,
                 full_result_sha256=sha(p),off_original_success=old['status']=='berny_converged')
        if d['status']!='berny_converged':records.append(row);continue
        target=p.parent/(k+'.sigma');reference=Path(a.background)/(k+'.sigma')
        if sha(target)!=d['profile']['sha256']:raise ValueError('Chain candidate changed')
        if d.get('authorization_commit')!=a.authorization or d.get('permit_sha256')!=sha(a.permit):
            raise ValueError('Chain execution did not use the declared authorization')
        meta=json.loads(reference.read_text().splitlines()[0][8:])
        expected='S1' if k=='MVLVMROFTAUDAG-UHFFFAOYSA-N' else 'S2'
        if meta.get('geometry_converged')!=expected:raise ValueError('Reference is not the selected flagged profile')
        try:
            affinities(Namespace(key=k,reference=str(reference),candidate=[str(target)],
                background=a.background,out=str(out/k),registration=m['registration'],
                idac='data/benchmark/idac.csv',limit=.05))
        except SystemExit as e:
            if e.code!=2:raise
        g=out/k/'gate.json';check=json.loads(g.read_text())
        row.update(replacement_eligible=bool(check['passed']),local_gate_sha256=sha(g),
                   reference_sha256=sha(reference),candidate_sha256=sha(target))
        records.append(row)
    write(out/'promotions.json',dict(base=BASE,registration=m['registration'],
        authorization=a.authorization,permit_sha256=sha(a.permit),records=records,
        production_files_written=0,
        note='Eligibility only. An adoption commit must update protocol-aware selection/cache provenance; do not copy a new A profile into an old cache fingerprint.'))


def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='command',required=True)
    q=s.add_parser('worker');q.add_argument('--spec',required=True);q.add_argument('--out',required=True)
    q=s.add_parser('calibration');q.add_argument('--plan',required=True);q.add_argument('--results',required=True);q.add_argument('--out',required=True)
    q=s.add_parser('decide')
    for name in ('calibration','pilot-plan','pilot-results','chains-plan','out'):q.add_argument('--'+name,required=True)
    q=s.add_parser('affinities')
    for name in ('key','reference','background','out','registration'):q.add_argument('--'+name,required=True)
    q.add_argument('--candidate',action='append',required=True);q.add_argument('--limit',type=float,choices=[.01,.05],required=True);q.add_argument('--idac')
    q=s.add_parser('replacements')
    for name in ('plan','results','permit','authorization','background','out'):q.add_argument('--'+name,required=True)
    a=p.parse_args();globals()[a.command](a)
if __name__=='__main__':main()
