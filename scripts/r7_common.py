"""Round-7 read-only experiments. A successful diagnostic is not adoption."""
from __future__ import annotations
import hashlib
import json
import os
import re
import signal
import subprocess
import sys
import time
from pathlib import Path
import numpy as np

BASE = 'ddf22b19f9e1750308bd11572786b44d407a80f9'
BERNY = dict(gradientmax=4.5e-4, gradientrms=1.5e-4,
             stepmax=1.8e-3, steprms=1.2e-3)
STALL = ('BTFJIXJJCSYFAL-UHFFFAOYSA-N','FLIACVVOZYBSBS-UHFFFAOYSA-N',
         'HPEUJPJOZXNMSJ-UHFFFAOYSA-N','MVLVMROFTAUDAG-UHFFFAOYSA-N',
         'OYHQOLUKZRVURQ-HZJYTTRNSA-N','PYGXAGIECVVIOZ-UHFFFAOYSA-N')
PILOT = {
 'BKIMMITUMNQMOS-UHFFFAOYSA-N': ('s20261006-c1.json','7b9f8443a8f40cfb329a35b828777a03cedd91226863a15446995f5603b1659d'),
 'ZIBGPFATKBEMQZ-UHFFFAOYSA-N': ('s20261006-c1.json','538bb17a59324e1f1597934a044cdaa6843ea174f655e33669539fb538b39d5d'),
 'XTHFKEDIFFGKHM-UHFFFAOYSA-N': ('s20261005-c1.json','eb305508f6c6dcf68f610d0927af1977339dedc9da04238443c9acc20008df34')}
PROBES = ('XLYOFNOQVPJJNP-UHFFFAOYSA-N','OKKJLVBELUTLKV-UHFFFAOYSA-N',
          'BKIMMITUMNQMOS-UHFFFAOYSA-N','XTHFKEDIFFGKHM-UHFFFAOYSA-N')
SENTINELS = PROBES[:3] + ('LYCAIKOWRPUZTN-UHFFFAOYSA-N',
 'MTHSVFCYNBDYFN-UHFFFAOYSA-N','ZIBGPFATKBEMQZ-UHFFFAOYSA-N',
 'PEDCQBHIVMGVHV-UHFFFAOYSA-N','DNIAPMSPPWPWGF-UHFFFAOYSA-N')

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def write(path, value):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+'.tmp')
    tmp.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
    os.replace(tmp,path)

def fresh(path):
    p=Path(path).resolve(); p.mkdir(parents=True,exist_ok=False); return p

def registration(value):
    if not re.fullmatch(r'[0-9a-f]{40}',value):
        raise ValueError('Use the actual full registration commit SHA, not a placeholder')
    return value

def geometry(path):
    d=json.loads(Path(path).read_text()); sym=list(d['sym']); x=np.asarray(d['x'],float)
    if x.shape!=(len(sym),3) or not len(sym) or not np.isfinite(x).all():
        raise ValueError('Invalid saved geometry')
    return sym,x

def versions(native=False):
    from importlib.metadata import version,PackageNotFoundError
    result={}
    for k in ('pyscf','pyberny','rdkit','numpy','scipy','pandas','tblite','ase'):
        try: result[k]=version(k)
        except PackageNotFoundError: result[k]=None
    if native and (result['pyscf']!='2.14.0' or result['pyberny']!='0.7.0'):
        raise RuntimeError('Requires pyscf 2.14.0 and pyberny 0.7.0')
    return result

def clean_environment():
    for k in ('ZC_BERNY_NOISE_EH','ZC_MAXSTEPS','ZC_TRIC_PREOPT','ZC_BERNY_STATE',
              'ZC_BERNY_REPLAY','ZC_SIGMA_OVERRIDE_DIR','ZC_ONLY_KEYS'):
        os.environ.pop(k,None)
    os.environ.update(ZC_PCM3C='1',ZC_R3_COOH_FLAG='1',ZC_R6_ENDPOINT='1')

def factory(sym,x,spin=0,precision='production'):
    """Use the inspected, unchanged R3 factory. Only precision diagnostics override SCF."""
    from r3_precision import factory as original
    mf=original(sym,np.asarray(x,float),spin,precision!='production',4000)
    if precision=='strict':
        mf.conv_tol=1e-12; mf.conv_tol_grad=1e-8
    elif precision not in ('production','tight'):
        raise ValueError(precision)
    return mf

def gradient(mf,response):
    g=mf.nuc_grad_method(); g.grid_response=bool(response)
    if not bool(getattr(g,'auxbasis_response',False)):
        raise RuntimeError('Density-fitting auxiliary-basis response is missing')
    if getattr(g.base,'with_solvent',None) is None:
        raise RuntimeError('PCM response was detached')
    return g

def profile(sym,x,key,dest,spin,meta):
    from zcosmo.pyscf_cosmo import cosmo_segments,to_profiles,write_sigma
    seg,e=cosmo_segments(sym,x,spin=spin)
    out,m=to_profiles(sym,x,seg); m.update(meta)
    m.update(E_scf_Eh=float(e),standard_INCHIKEY=key)
    write_sigma(dest,out,m,key)
    return dict(path=str(Path(dest).resolve()),sha256=sha(dest),energy_Eh=float(e))

def assert_connectivity(smiles,sym,x):
    from rdkit import Chem
    from r4_common import contacts
    mol=Chem.AddHs(Chem.MolFromSmiles(smiles))
    if sym!=[a.GetSymbol() for a in mol.GetAtoms()]:
        raise ValueError('Saved geometry and declared atom order disagree')
    expected=[sorted(n.GetIdx() for n in a.GetNeighbors()) for a in mol.GetAtoms()]
    found=[sorted(a['bonds']) for a in contacts(sym,x)['atoms']]
    if expected!=found: raise ValueError('Covalent connectivity changed')

def load_plan(path):
    p=Path(path).resolve(); m=json.loads(p.read_text())
    if m['base']!=BASE: raise ValueError('Unexpected source baseline')
    registration(m['registration'])
    for source,digest in m.get('sources',{}).items():
        if sha(source)!=digest:raise ValueError('Frozen experiment source changed: '+source)
    if len({r['key'] for r in m['cases']})!=len(m['cases']):
        raise ValueError('Duplicate plan case')
    for r in m['cases']:
        q=p.parent/r['geometry']
        if sha(q)!=r['geometry_sha256']: raise ValueError('Frozen geometry changed')
    return p,m

def find_result(root,key,arm,plan_hash):
    hits=[]
    for p in Path(root).rglob('result.json'):
        d=json.loads(p.read_text())
        if d.get('key')==key and d.get('arm')==arm and d.get('plan_sha256')==plan_hash:
            hits.append((p,d))
    if len(hits)!=1: raise ValueError(f'Expected exactly one result for {key}/{arm}, found {len(hits)}')
    return hits[0]

def bounded(argv,out,seconds):
    """One POSIX process group and one persistent claim per output. Never retry."""
    out=Path(out).resolve(); out.parent.mkdir(parents=True,exist_ok=True)
    lock=out.with_name(out.name+'.claim')
    fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    with os.fdopen(fd,'w') as f: f.write(json.dumps(dict(pid=os.getpid(),argv=argv)))
    if out.exists(): raise FileExistsError(out)
    logpath=out.with_name(out.name+'.log'); start=time.monotonic(); timed=False
    with logpath.open('wb') as log:
        p=subprocess.Popen(argv,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
        try: rc=p.wait(timeout=seconds)
        except subprocess.TimeoutExpired:
            timed=True
            try: os.killpg(p.pid,signal.SIGTERM)
            except ProcessLookupError: pass
            try: rc=p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                try: os.killpg(p.pid,signal.SIGKILL)
                except ProcessLookupError: pass
                rc=p.wait()
    native={}
    if (out/'result.json').is_file(): native=json.loads((out/'result.json').read_text())
    status='deadline' if timed else ('completed' if rc==0 else 'child_failed')
    # Scientific negative decisions can complete normally; do not call them censoring.
    if not timed and native.get('status') in ('censored_evaluations','diagnostic_complete'):
        status='completed'
    record=dict(argv=argv,wall_s=time.monotonic()-start,deadline_s=seconds,
                returncode=rc,execution_status=status,native_status=native.get('status'),
                output=str(out),log_sha256=sha(logpath))
    write(out.with_name(out.name+'.run.json'),record)
    return record

def internal_projection(x,v):
    from scipy.linalg import null_space
    y=np.asarray(x)-np.mean(x,axis=0); rigid=[]
    for axis in np.eye(3):
        rigid.extend([np.broadcast_to(axis,y.shape).ravel(),
                      np.cross(np.broadcast_to(axis,y.shape),y).ravel()])
    Q=null_space(np.asarray(rigid),rcond=1e-10)
    return (Q@(Q.T@np.asarray(v).ravel())).reshape(y.shape)

def verdict(reference,analytic,u,tau=1e-5):
    """Finite-resolution equivalence assessment, not a certified error interval."""
    if not np.isfinite([reference,analytic,u]).all() or u<0:
        return 'inconclusive'
    if u>tau/4: return 'inconclusive'
    error=abs(reference-analytic)
    if error+u<=tau: return 'consistent'
    if error-u>tau: return 'inconsistent'
    return 'inconclusive'

def chain_decision(cal,pilots):
    keys=set(PILOT)
    if set(pilots)!=keys: raise ValueError('All three fixed pilot cases are required')
    only_full=[]; only_off=[]; invalid=[]
    allowed={'berny_converged','censored_evaluations','censored_deadline'}
    for k,r in pilots.items():
        if set(r)!= {'off','full'} or any(v not in allowed for v in r.values()):
            invalid.append(k); continue
        if r['full']=='berny_converged' and r['off']!='berny_converged':only_full.append(k)
        if r['off']=='berny_converged' and r['full']!='berny_converged':only_off.append(k)
    ok=bool(cal.get('passed') is True and len(only_full)>=2 and not only_off and not invalid)
    return dict(eligible_for_chain_trial=ok,full_only=only_full,off_only=only_off,
                invalid=invalid,pilots=pilots,rule='calibration numerical compatibility pass; >=2 full-only; zero off-only; no missing/failed pilot; targeted rescue has its own wall cap')


def source_fingerprint(family):
    shared=['scripts/r7_common.py','scripts/r7_gate.py','scripts/r3_precision.py',
            'scripts/r4_common.py','data/raw/nist/to_sigma.py']
    specific={'optimizer':['scripts/r7_plan.py','scripts/r7_optimize.py'],
              'referee':['scripts/r7_referee.py','scripts/r6_referee.py'],
              'screen':['scripts/r7_screen.py','scripts/r6_referee.py']}[family]
    shared += ['src/zcosmo/'+n for n in ('pyscf_cosmo.py','pyscf_cosmo_v2.py','pcm_lu.py',
                                        'cosmosac.py','z0x.py','models.py')]
    return {p:sha(p) for p in shared+specific}


FD_TAU=5e-5/5
FD_STEPS=np.array([.016,.008,.004,.002,.001])

def fd_assess(tight,strict,gtight,gfull,goff,topology_stable=True):
    tight=np.asarray(tight,float);strict=np.asarray(strict,float)
    if tight.shape!=(5,2) or strict.shape!=(5,2):raise ValueError('Five fixed +/- energy pairs are required')
    if not np.isfinite([tight,strict]).all():raise ValueError('Nonfinite energy table')
    d0=(tight[:,0]-tight[:,1])/(2*FD_STEPS)
    d1=(strict[:,0]-strict[:,1])/(2*FD_STEPS)
    r0=(4*d0[1:]-d0[:-1])/3;r1=(4*d1[1:]-d1[:-1])/3
    trunc=abs(r1[-1]-r1[-2])  # Full difference, deliberately not an asserted /15 bound.
    previous=abs(r1[-2]-r1[-3])
    precision=max(abs(r1[-1]-r0[-1]),abs(r1[-2]-r0[-2]))
    gradient_precision=abs(gfull-gtight)
    h=FD_STEPS[-1];hl=FD_STEPS[-2]
    rounding=8*np.finfo(float).eps*((4/3)*abs(strict[-1]).sum()/(2*h)
                                     +(1/3)*abs(strict[-2]).sum()/(2*hl))
    uncertainty=float(trunc+precision+gradient_precision+rounding)
    stabilizing=bool(trunc<=previous or trunc<=FD_TAU/16)
    f=verdict(float(r1[-1]),float(gfull),uncertainty,FD_TAU)
    o=verdict(float(r1[-1]),float(goff),uncertainty,FD_TAU)
    if not topology_stable or not stabilizing:f=o='inconclusive'
    material=True if f=='consistent' and o=='inconsistent' else (False if f==o=='consistent' else None)
    return dict(steps_Bohr=FD_STEPS.tolist(),central_tight=d0.tolist(),central_strict=d1.tolist(),
        Richardson_tight=r0.tolist(),Richardson_strict=r1.tolist(),reference=float(r1[-1]),
        truncation_indicator=float(trunc),precision_indicator=float(precision),
        gradient_precision_indicator=float(gradient_precision),roundoff_indicator=float(rounding),
        combined_indicator=uncertainty,indicator_ceiling=FD_TAU/4,tolerance=FD_TAU,
        stabilizing=stabilizing,grid_count_stable=bool(topology_stable),
        full_error=float(abs(gfull-r1[-1])),off_error=float(abs(goff-r1[-1])),
        full_verdict=f,off_verdict=o,missing_response_material=material,
        scope='Empirical finite-resolution assessment; no rigorous interval enclosure or global stationarity certificate')




HIST_KEY_RE=re.compile(r'^[A-Z]{14}-[A-Z]{10}-[A-Z]$')

def historical_queries(path):
    """Read an explicit query file, or find the single archived 2302-occurrence table.

    Field names may differ across archived harnesses. A target field is accepted
    only if every entry is a full molecular key occurring in that row's pair.
    No query is dropped, deduplicated, or reconstructed from an arbitrary 25.
    """
    import pandas as pd
    path=Path(path); sources=[path] if path.is_file() else sorted(path.rglob('*.csv'))
    candidates=[]
    for p in sources:
        try:d=pd.read_csv(p)
        except (ValueError,UnicodeError):continue
        if len(d)!=2302 or not {'solute','solvent','T'}<=set(d):continue
        for c in d.columns:
            if c in ('solute','solvent','T'):continue
            v=d[c].astype(str)
            if v.nunique()!=25 or not v.map(lambda x:bool(HIST_KEY_RE.fullmatch(x))).all():continue
            if not ((v==d.solute)|(v==d.solvent)).all():continue
            q=pd.DataFrame(dict(target=v,solute=d.solute,solvent=d.solvent,T=d['T'],
                                occurrence=np.arange(len(d))))
            if not np.isfinite(q['T']).all() or (q['T']<=0).any():raise ValueError('Invalid historical temperatures')
            candidates.append((p,c,q))
    if not candidates:
        raise ValueError('No archived 25-target/2302-occurrence query table. Supply its exact CSV with --historical; do not use validation_set.csv alone.')
    unique={q.to_csv(index=False): (p,c,q) for p,c,q in candidates}
    if len(unique)!=1:raise ValueError('Conflicting historical query tables; supply the explicit registered CSV')
    return next(iter(unique.values()))

