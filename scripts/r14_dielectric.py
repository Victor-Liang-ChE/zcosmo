"""R14 ingredient audit and exposure receipt. No quantum or activity-model calls.

Real data work is private and Mac-only. Unit tests use synthetic records.
Experimental permittivities are references, never a production replacement.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import importlib.metadata
import io
import json
import math
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import time
import urllib.request
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
BASE = '864aaac1e85eda31a43f24e856770c7f56ccb760'
MARKER = 'R14-P51-P52-P53: exposure, dielectric ingredient, and oracle diagnostic'
SOURCE_COMMIT = 'e79047588b30cfabc564c79fb26d760c746877d7'
SOURCE_BLOB = 'bf12ffba51b478a021acc6ed58778c04deb9b988'
SOURCE_URL = ('https://raw.githubusercontent.com/CalebBell/chemicals/' + SOURCE_COMMIT +
    '/chemicals/Electrolytes/Permittivity%20%28Dielectric%20Constant%29%20of%20Liquids.tsv')
TREF = 298.15
DESIGN = dict(T_K=TREF, point_temperature_tolerance_K=0.10,
    coefficient_policy='A and B required; absent C/D mean zero in documented polynomial',
    no_extrapolation=True, identity='exact unique key to unique checksum-valid CAS',
    baseline_gate='descriptive only; no baseline error threshold authorizes a model',
    candidate_mean_abs_log_ratio_max=0.8, candidate_mean_abs_f_max=0.02,
    candidate_max_relative_error=0.25, candidate_per_member_log_worsening_max=0.05,
    candidate_scope='four predeclared pilot liquids only; not a 740-compound acceptance',
    native_budget=0, activity_model_budget=0, adoption=False)
PILOT = ('XLYOFNOQVPJJNP-UHFFFAOYSA-N','OKKJLVBELUTLKV-UHFFFAOYSA-N',
         'WEVYAHXRMPXWCK-UHFFFAOYSA-N','UHOVQNZJYSORNB-UHFFFAOYSA-N')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def write(path, obj):
    p=Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('x') as f:
        json.dump(obj, f, indent=2, sort_keys=True, allow_nan=False)
        f.write('\n')
    p.chmod(0o600)


def records(path, delimiter=','):
    with Path(path).open(newline='') as f:
        return list(csv.DictReader(f, delimiter=delimiter))


def number(value):
    try:
        x=float(value)
        return x if math.isfinite(x) else None
    except (ValueError, TypeError):
        return None


def screening(eps):
    x=np.asarray(eps, float)
    require(np.isfinite(x).all() and (x>=1).all(), 'epsilon must be finite and >= 1')
    return 1.0-1.5/(x+0.5)


def sensitivity(old, new):
    a=float(screening(old)); b=float(screening(new))
    return dict(old_f=a,new_f=b,delta_f=b-a,
        relative_coefficient_change=None if a==0 else (b-a)/a,
        residual_to_conductor=1-a, d_f_d_epsilon=1.5/(old+0.5)**2)


def kf_epsilon(mu_D, volume_A3, eps_inf, g, T=TREF):
    """KF closure only. The input g must have the proper bulk/boundary convention."""
    vals=np.asarray([mu_D,volume_A3,eps_inf,g,T],float)
    require(np.isfinite(vals).all() and mu_D>=0 and volume_A3>0 and
            eps_inf>=1 and g>=0 and T>0, 'invalid KF arguments')
    y=1e30/volume_A3*(mu_D*3.33564e-30)**2/(9*8.8541878128e-12*1.380649e-23*T)
    b=eps_inf+(eps_inf+2)**2*y*g
    return float((b+math.sqrt(b*b+8*eps_inf*eps_inf))/4)


def cas_valid(cas):
    if not isinstance(cas,str) or not re.fullmatch(r'\d{2,7}-\d{2}-\d',cas):
        return False
    left, last=cas.rsplit('-',1)
    digits=left.replace('-','')
    return sum((i+1)*int(v) for i,v in enumerate(reversed(digits)))%10==int(last)


def reference_at(row, T=TREF):
    """Use the declared polynomial only inside its range, else a near-exact point."""
    a,b,c,d=(number(row.get(k)) for k in ('A','B','C','D'))
    lo,hi=number(row.get('Tmin')),number(row.get('Tmax'))
    if a is not None and b is not None and lo is not None and hi is not None and lo<=T<=hi:
        v=a+T*(b+T*((c or 0.)+T*(d or 0.)))
        require(math.isfinite(v) and v>=1, 'invalid interpolated reference')
        return v, 'CRC_polynomial_in_range'
    t,v=number(row.get('T')),number(row.get('Permittivity'))
    if t is not None and v is not None and abs(t-T)<=DESIGN['point_temperature_tolerance_K']:
        require(v>=1, 'invalid reference point')
        return v, 'CRC_point_within_0.10_K'
    return None, 'no_reference_at_declared_temperature'


def metrics(pred, ref):
    p=np.asarray(pred,float); r=np.asarray(ref,float)
    require(p.ndim==1 and p.shape==r.shape and len(p)>0, 'empty or misaligned ingredient comparison')
    require(np.isfinite(p).all() and np.isfinite(r).all() and (p>=1).all() and (r>=1).all(),
            'nonfinite ingredient value; do not shrink to a favorable intersection')
    z=np.log(p/r); relative=np.abs(p-r)/r
    return dict(n=len(p),mean_abs_log_epsilon=float(abs(z).mean()),
        median_abs_log_epsilon=float(np.median(abs(z))),mean_log_bias=float(z.mean()),
        mean_abs_relative_error=float(relative.mean()),max_relative_error=float(relative.max()),
        mean_abs_f_error=float(abs(screening(p)-screening(r)).mean()))


def ingredient_rows(stored, identities, reference):
    keys=[r['inchikey'] for r in stored]
    require(len(keys)==len(set(keys)), 'duplicate dielectric keys')
    bykey={}; bycas={}; ref={}
    for r in identities:
        k,c=r['inchikey'],r['cas'].strip()
        bykey.setdefault(k,set()).add(c); bycas.setdefault(c,set()).add(k)
    for r in reference:
        c=r['CAS'].strip()
        require(cas_valid(c), 'invalid CAS in source')
        require(c not in ref, 'duplicate CAS in dielectric reference')
        ref[c]=r
    out=[]
    for r in stored:
        k=r['inchikey']; z=dict(key=k,status='unmatched',stored_epsilon=number(r['eps']))
        cs=bykey.get(k,set())
        if len(cs)!=1:
            z['status']='missing_or_ambiguous_key_to_CAS'
        else:
            c=next(iter(cs)); z['CAS']=c
            if not cas_valid(c) or len(bycas.get(c,set()))!=1:
                z['status']='invalid_or_stereochemically_ambiguous_CAS'
            elif c not in ref:
                z['status']='CAS_absent_from_reference'
            else:
                v,how=reference_at(ref[c]); z['reference_method']=how
                if v is None:
                    z['status']=how
                else:
                    z['reference_epsilon']=v
                    z['status']='matched' if z['stored_epsilon'] is not None and z['stored_epsilon']>=1 else 'invalid_stored_epsilon'
        out.append(z)
    return out


def candidate_gate(rows, candidates):
    """Future physical-pilot gate. R14 provides no candidate-generating authorization."""
    by={r['key']:r for r in rows}; cs={r['key']:r for r in candidates}
    require(len(cs)==len(candidates) and set(cs)==set(PILOT), 'candidate must contain exactly the frozen four-liquid panel')
    require(all(k in by and by[k]['status']=='matched' for k in PILOT), 'pilot reference coverage incomplete')
    require(all(cs[k].get('sampling_gate_passed') is True and cs[k].get('dipole_gate_passed') is True
                for k in PILOT), 'physical validation missing')
    p=[cs[k]['eps'] for k in PILOT]; b=[by[k]['stored_epsilon'] for k in PILOT]
    r=[by[k]['reference_epsilon'] for k in PILOT]
    m0,m1=metrics(b,r),metrics(p,r)
    worse=float(np.max(np.abs(np.log(np.array(p)/r))-np.abs(np.log(np.array(b)/r))))
    checks=dict(log_improvement=m1['mean_abs_log_epsilon']<=0.8*m0['mean_abs_log_epsilon'],
        f_accuracy=m1['mean_abs_f_error']<=0.02,individual_relative=m1['max_relative_error']<=0.25,
        no_large_member_regression=worse<=0.05)
    return dict(passed=all(checks.values()),checks=checks,baseline=m0,candidate=m1,
                adopted=False,scope='ingredient pilot only, not phase-equilibrium acceptance')


def environment():
    ans={'python':platform.python_version(),'machine':platform.machine()}
    for name in ('numpy','scipy','pandas','rdkit','thermo','chemicals'):
        try: ans[name]=importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError: ans[name]=None
    return ans


def mac():
    require(sys.platform=='darwin' and not os.environ.get('CI') and not os.environ.get('GITHUB_ACTIONS'),
            'Real R14 data work is restricted to the private Mac, outside CI')


def private(path, fresh=False):
    p=Path(path).expanduser().resolve()
    require(not p.is_relative_to(ROOT.resolve()), 'private output must be outside this checkout')
    require(not any((v/'.git').exists() for v in (p,*p.parents)), 'private output cannot be inside a Git checkout')
    if fresh:
        p.mkdir(parents=True,exist_ok=False,mode=0o700)
    return p


def registration(commit):
    require(re.fullmatch(r'[0-9a-f]{40}',commit) is not None,'use a full registration commit')
    subprocess.run(['git','merge-base','--is-ancestor',commit,'HEAD'],cwd=ROOT,check=True,capture_output=True)
    text=subprocess.check_output(['git','show',commit+':PREREGISTRATION.md'],cwd=ROOT,text=True)
    require(MARKER in text,'registration marker missing')
    subprocess.run(['git','merge-base','--is-ancestor',BASE,commit],cwd=ROOT,check=True,capture_output=True)
    for rel in ('scripts/r14_dielectric.py','scripts/r14_oracle.py','scripts/r14_selftest.py'):
        registered=subprocess.check_output(['git','show',commit+':'+rel],cwd=ROOT)
        require(registered==(ROOT/rel).read_bytes(),'helper differs from registered bytes: '+rel)
    return commit


def fingerprint(paths):
    return {str(Path(p).resolve()):sha(p) for p in paths}


def check_inputs(saved):
    for p,h in saved.items():
        require(sha(p)==h,'input mutation: '+Path(p).name)


def exposure_receipt(reg):
    """An exposure declaration, not proof of what every collaborator has seen."""
    return dict(registration=reg,base=BASE,
        test_20pct='repeatedly inspected; historical partition retained, not a new holdout',
        temporal_2017_2019='repeatedly inspected; no reset of holdout status',
        glycol_R4_R12='inspected; P35 stays closed',
        dielectric_reference='source schema and some values exposed during design; new property benchmark, not wholly blinded',
        phase_oracle='retrospective explanatory scoring; experimental epsilon is not fit-free input',
        new_post2019_source='not certified unexposed; custodian/document/duplicate audit required',
        may_score_frozen_retrospective_oracle=True,may_claim_unexposed=False,
        may_adopt=False,native_budget=0)


def acquire(a):
    mac(); reg=registration(a.registration); out=private(a.out,True)
    exp=exposure_receipt(reg)
    exp['reviewed_public_record_hashes']=fingerprint([ROOT/p for p in (
        'PREREGISTRATION.md','PROGRESS.md','results/scorecard_test_main7.md',
        'results/scorecard_temporal_ext.md','results/scorecard_temporal_test_ext.md',
        'docs/astra/round12/RESULTS.md','docs/astra/round13/RESULTS.md','manuscript/draft.md')])
    exp['private_queue_and_collaborator_exposure_complete']=False
    write(out/'exposure.json',exp)
    start=time.monotonic()
    try:
        with urllib.request.urlopen(SOURCE_URL,timeout=30) as response:
            data=response.read(2_000_001)
        require(len(data)<=2_000_000 and blob(data)==SOURCE_BLOB,'source size or pinned Git blob mismatch')
        with (out/'reference.tsv').open('xb') as f: f.write(data)
        (out/'reference.tsv').chmod(0o600)
        write(out/'acquisition.json',dict(status='complete',url=SOURCE_URL,git_blob=SOURCE_BLOB,
              sha256=sha(out/'reference.tsv'),registration=reg,wall_s=time.monotonic()-start))
    except Exception as e:
        write(out/'acquisition.json',dict(status='failed',error_type=type(e).__name__,
              registration=reg,wall_s=time.monotonic()-start))
        raise


def ingredients(a):
    mac(); reg=registration(a.registration); source=private(a.source); out=private(a.out,True)
    exp=read(source/'exposure.json'); require(exp['registration']==reg,'exposure registration differs')
    acq=read(source/'acquisition.json'); require(acq['status']=='complete','acquisition incomplete')
    require(blob((source/'reference.tsv').read_bytes())==SOURCE_BLOB,'source blob changed')
    paths=[source/'reference.tsv',source/'exposure.json',ROOT/'results/qc/dielectric.csv',
           ROOT/'data/processed_ext/ud_complist.csv',Path(__file__)]
    fp=fingerprint(paths); env=environment(); start=time.monotonic()
    manifest=dict(design=DESIGN,registration=reg,exposure=exp,inputs=fp,environment=env)
    write(out/'manifest.json',manifest)
    rows=ingredient_rows(records(paths[2]),records(paths[3]),records(paths[0],'\t'))
    matched=[r for r in rows if r['status']=='matched']
    invalid=[r for r in rows if r['status']=='invalid_stored_epsilon']
    status={k:sum(r['status']==k for r in rows) for k in sorted({r['status'] for r in rows})}
    aggregate=metrics([r['stored_epsilon'] for r in matched],[r['reference_epsilon'] for r in matched]) if matched and not invalid else None
    check_inputs(fp)
    write(out/'ingredients.json',dict(manifest_sha256=sha(out/'manifest.json'),rows=rows,
        population=len(rows),status_counts=status,baseline_metrics=aggregate,
        reference_comparison_complete=bool(matched and not invalid),
        invalid_stored_values_block_complete_comparison=bool(invalid),
        missing_reference_is_not_zero_error=True,experimental_input_not_adopted=True,
        source_independence='different measured property; common laboratories/compilations and unknown per-row lineage remain possible',
        wall_s=time.monotonic()-start,activity_model_calls=0,SCF_calls=0))
    print('Private ingredient audit complete. No activity model or quantum calculation ran.')


def check(a):
    mac(); out=private(a.out); m=read(out/'manifest.json'); registration(m['registration'])
    check_inputs(m['inputs']); require(environment()==m['environment'],'package environment changed')
    require(m['design']==DESIGN,'ingredient design changed')
    d=read(out/'ingredients.json'); require(d['manifest_sha256']==sha(out/'manifest.json'),'manifest changed')
    rows=ingredient_rows(records(ROOT/'results/qc/dielectric.csv'),
        records(ROOT/'data/processed_ext/ud_complist.csv'),
        records(next(p for p in m['inputs'] if Path(p).name=='reference.tsv'),'\t'))
    require(rows==d['rows'],'ingredient rows do not reproduce')
    matched=[r for r in rows if r['status']=='matched']
    invalid=any(r['status']=='invalid_stored_epsilon' for r in rows)
    aggregate=metrics([r['stored_epsilon'] for r in matched],[r['reference_epsilon'] for r in matched]) if matched and not invalid else None
    require(aggregate==d['baseline_metrics'],'ingredient metrics do not reproduce')
    print('Ingredient inputs and numerical summary verified; this is not production acceptance.')


def main():
    p=argparse.ArgumentParser(description=__doc__); s=p.add_subparsers(dest='command',required=True)
    q=s.add_parser('catalog'); q.set_defaults(fn=lambda a:print(json.dumps(dict(url=SOURCE_URL,commit=SOURCE_COMMIT,blob=SOURCE_BLOB,design=DESIGN),indent=2)))
    q=s.add_parser('screening'); q.set_defaults(fn=lambda a:print(json.dumps(dict(
        water=sensitivity(52.93798366132173,78.),methanol=sensitivity(24.447223573823276,33.)),indent=2)))
    q=s.add_parser('acquire');q.add_argument('--registration',required=True);q.add_argument('--out',required=True);q.set_defaults(fn=acquire)
    q=s.add_parser('ingredients');q.add_argument('--registration',required=True);q.add_argument('--source',required=True);q.add_argument('--out',required=True);q.set_defaults(fn=ingredients)
    q=s.add_parser('check');q.add_argument('--out',required=True);q.set_defaults(fn=check)
    a=p.parse_args();a.fn(a)

if __name__=='__main__':main()
