"""P34: a frozen primary-profile sample, fixed-coordinate gradients, and local stresses.

No optimization, Hessian certificate, profile replacement, or claim about every
geometry in a ball. Primary-set screen flags are not experimental errors.
"""
from __future__ import annotations
from r7_common import source_fingerprint
import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
import numpy as np
import pandas as pd
from r7_common import (BASE,SENTINELS,sha,write,fresh,registration,geometry,versions,
    factory,gradient,profile,load_plan,bounded,clean_environment,internal_projection)


def plan(a):
    from r4_common import selected_profiles
    from zcosmo.pyscf_cosmo_v2 import OPEN_SHELL
    registration(a.registration);out=fresh(a.out)
    compounds=pd.read_csv('data/benchmark/compounds.csv');smi=compounds.set_index('inchikey').smiles.to_dict()
    primary={k:p for k,folder,p in selected_profiles(a.profile_root,compounds) if folder=='profiles_v2'}
    if len(primary)!=630:raise ValueError('The registered 630-member primary universe changed')
    ordering=sorted(primary,key=lambda k:hashlib.sha256(('R7-primary-screen-v1|'+k).encode()).hexdigest())
    sample=set(ordering[:32])
    if not set(SENTINELS)<=set(primary):raise ValueError('A frozen sentinel is absent from primary')
    chosen=sample|set(SENTINELS);cases=[];population={k:sha(p) for k,p in primary.items()}
    for key in sorted(chosen):
        source=primary[key];meta=json.loads(source.read_text().splitlines()[0][8:])
        if meta.get('geometry_converged') is not True:raise ValueError('Primary convergence metadata absent')
        original=source.with_suffix('.xyz.json');sym,x=geometry(original)
        dest=out/'geometries'/(key+'.json');dest.parent.mkdir(exist_ok=True);dest.write_bytes(original.read_bytes())
        ref=out/'references'/(key+'.sigma');ref.parent.mkdir(exist_ok=True);ref.write_bytes(source.read_bytes())
        cases.append(dict(key=key,smiles=smi[key],spin=OPEN_SHELL.get(smi[key],0),
            geometry=str(dest.relative_to(out)),geometry_sha256=sha(dest),
            reference_profile=str(ref.relative_to(out)),reference_sha256=sha(ref),
            probability_sample=key in sample,sentinel=key in SENTINELS))
    write(out/'plan.json',dict(sources=source_fingerprint('screen'),base=BASE,registration=a.registration,family='screen',cases=cases,
        population_profile_hashes=population,universe=630,probability_sample_size=32,
        selection='SHA256 R7-primary-screen-v1|key, plus eight named structural sentinels',
        stress_max_atom_displacement_A=.01,seconds_per_case=3600,packages=versions()))


def native(a):
    from r3_common import read_sigma
    p,m=load_plan(a.plan);versions(native=True)
    if m['family']!='screen':raise ValueError('Not the fixed primary screen')
    r=next((q for q in m['cases'] if q['key']==a.key),None)
    if r is None:raise ValueError('Key not selected in advance')
    clean_environment();out=fresh(a.out);sym,x=geometry(p.parent/r['geometry']);t=time.monotonic()
    common=dict(base=BASE,registration=m['registration'],key=a.key,plan_sha256=sha(p),
                geometry_sha256=r['geometry_sha256'],adopted=False)
    write(out/'result.json',dict(common,status='running'))
    try:
        mf=factory(sym,x,r['spin'],'production');e=float(mf.kernel())
        if not mf.converged or not np.isfinite(e):raise RuntimeError('SCF failed')
        off=np.asarray(gradient(mf,False).kernel());full=np.asarray(gradient(mf,True).kernel())
        if not np.isfinite([off,full]).all():raise ValueError('Gradient failed')
        v=-internal_projection(x,full);length=float(np.max(np.linalg.norm(v,axis=1)))
        label='projected negative full-response gradient'
        if length<1e-12:
            from r6_referee import probe_directions
            name,v=probe_directions(r['smiles'],sym,x)[0]
            length=float(np.max(np.linalg.norm(v,axis=1)));label='fixed fallback '+name
        v=v/length
        np.savez_compressed(out/'gradients.npz',x_A=x,g_off=off,g_full=full,stress_direction=v)
        outputs={}
        for name,sign in (('center',0.),('minus',-1.),('plus',1.)):
            if time.monotonic()-t>3400:raise TimeoutError('Fixed screen deadline')
            outputs[name]=profile(sym,x+sign*.01*v,a.key,out/(name+'.sigma'),r['spin'],
                dict(geometry_converged='R7-fixed-stress',source='R7 screen, not optimized or adopted',
                     r7_registration=m['registration'],r7_plan_sha256=sha(p)))
        _,center,_=read_sigma(out/'center.sigma');_,stored,_=read_sigma(p.parent/r['reference_profile'])
        bin_changes={}
        for name in ('minus','plus'):
            _,z,_=read_sigma(out/(name+'.sigma'))
            bin_changes[name]=dict(raw_max=float(abs(z-center).max()),
                normalized_L1=float(abs(z/z.sum()-center/center.sum()).sum()))
        write(out/'result.json',dict(common,status='diagnostic_complete',profiles=outputs,
            SVP_energy_Eh=e,SVP_SCF=1,SVP_gradients=2,TZVP_single_points=3,
            g_off_max=float(abs(off).max()),g_full_max=float(abs(full).max()),
            response_change_max=float(abs(full-off).max()),response_force_flag=bool(abs(full-off).max()>1e-5),
            direction=label,stress_A=.01,bin_changes=bin_changes,
            stored_vs_recomputed_raw_max=float(abs(stored-center).max()),
            wall_s=time.monotonic()-t,
            scope='Finite directional stresses at saved coordinates; no minimum-displacement or basin-wide bound'))
    except Exception as e:
        write(out/'result.json',dict(common,status='censored_deadline' if isinstance(e,TimeoutError) else 'failed',
                                    error=repr(e),wall_s=time.monotonic()-t))
        raise


def run_case(a):
    p,m=load_plan(a.plan)
    if m['family']!='screen':raise ValueError('Wrong plan')
    bounded([sys.executable,str(Path(__file__).resolve()),'native','--plan',str(p),
             '--key',a.key,'--out',str(Path(a.out).resolve())],a.out,3600)


def report(a):
    from scipy.stats import hypergeom
    p,m=load_plan(a.plan);rows=[]
    for case in m['cases']:
        matches=[]
        for f in Path(a.results).rglob('result.json'):
            d=json.loads(f.read_text())
            if d.get('key')==case['key'] and d.get('plan_sha256')==sha(p):matches.append((f,d))
        row=dict(key=case['key'],probability_sample=case['probability_sample'],sentinel=case['sentinel'],screen_positive=None)
        if len(matches)!=1:
            row['status']='missing_or_duplicate_native';rows.append(row);continue
        f,d=matches[0];row['native_sha256']=sha(f)
        if d.get('status')!='diagnostic_complete':
            row['status']=d.get('status','unknown');rows.append(row);continue
        ag=Path(a.affinities)/case['key']/'gate.json'
        if not ag.is_file():row['status']='missing_affinity';rows.append(row);continue
        q=json.loads(ag.read_text())
        if q.get('key')!=case['key'] or q.get('registration')!=m['registration'] or q.get('limit')!=.01:
            raise ValueError('Wrong affinity evidence')
        if q['reference_sha256']!=d['profiles']['center']['sha256']:
            raise ValueError('Affinity center differs')
        if {z['sha256'] for z in q['candidates']}!={d['profiles'][k]['sha256'] for k in ('minus','plus')}:
            raise ValueError('Wrong stress candidates')
        checks=[z for c in q['candidates'] for z in c['models'].values()]
        complete=all(z['coverage_identical'] and z['max_abs_change'] is not None for z in checks)
        row.update(status='complete' if complete else 'affinity_unresolved',
            response_force_flag=d['response_force_flag'],response_change_max=d['response_change_max'],
            max_affinity_change=max(z['max_abs_change'] or 0. for z in checks),affinity_sha256=sha(ag))
        if complete:row['screen_positive']=row['max_affinity_change']>=.01
        rows.append(row)
    random=[r for r in rows if r['probability_sample']];N=630;n=len(random)
    complete=all(r['screen_positive'] is not None for r in random)
    upper=None
    if complete:
        k=sum(r['screen_positive'] for r in random)
        accepted=[K for K in range(k,N-n+k+1) if hypergeom.cdf(k,N,K,n)>=.05]
        upper=max(accepted)/N
    write(a.out,dict(base=BASE,registration=m['registration'],rows=rows,
        random_sample_complete=complete,one_sided_95_upper_fraction=upper,
        interpretation='Sampling-model bound on this finite-stress screen ONLY, conditional on SHA ordering behaving as a uniform sample. Not an accuracy or stationarity bound.',
        primary_profiles_changed=0))


def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='command',required=True)
    q=s.add_parser('plan');q.add_argument('--profile-root',required=True);q.add_argument('--registration',required=True);q.add_argument('--out',required=True)
    for name in ('native','run_case'):
        q=s.add_parser(name);q.add_argument('--plan',required=True);q.add_argument('--key',required=True);q.add_argument('--out',required=True)
    q=s.add_parser('report')
    for name in ('plan','results','affinities','out'):q.add_argument('--'+name,required=True)
    a=p.parse_args();globals()[a.command](a)
if __name__=='__main__':main()
