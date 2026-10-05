"""Frozen-geometry orientation experiment. Native items need PySCF; scoring needs local UD assets.

All generated profiles stay in a separate experiment directory. A rotated/reoriented,
rotation-averaged, or finer-surface profile is NOT an accepted production profile.
"""
from __future__ import annotations
import argparse
from collections import Counter
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import numpy as np
import pandas as pd
from r3_common import (BASE, digest, write_json, rotations, canonical_xyz,
                       read_sigma, write_sigma, profile_descriptors)

PHYSICS=['src/zcosmo/pyscf_cosmo.py','src/zcosmo/pcm_lu.py',
         'data/raw/nist/to_sigma.py','src/zcosmo/cosmosac.py','src/zcosmo/z0x.py',
         'src/zcosmo/models.py','results/z_params/Z0.json',
         'results/qc/dielectric.csv','results/qc/dispersion.csv']

def manifest(work): return json.loads((Path(work)/'manifest.json').read_text())

def freeze(a):
    work=Path(a.work).resolve()
    if work.exists() and any(work.iterdir()): raise ValueError('freeze into a new directory')
    work.mkdir(parents=True,exist_ok=True)
    old=pd.read_csv('results/pyscf_profile_validation.csv',usecols=['key','T'])
    if len(old)!=2302 or old.key.nunique()!=25: raise ValueError('historical fixture changed')
    val=pd.read_csv('data/pyscf_sigma/validation_set.csv')
    val=val[val.inchikey.isin(old.key.unique())]
    if len(val)!=25 or val.inchikey.duplicated().any(): raise ValueError('validation keys changed')
    d=pd.read_csv('data/benchmark/idac.csv',usecols=['file','dataset','solute','solvent','T','method','has_sigma'])
    if d.has_sigma.dtype!=bool: raise ValueError('has_sigma is not Boolean')
    d=d[d.has_sigma]; records=[]; geoms={}
    for k,smi in zip(val.inchikey,val.smiles):
        p=Path(a.geometry_dir)/f'{k}.xyz.json'
        g=json.loads(p.read_text()); x=np.asarray(g['x'],float)
        if x.shape!=(len(g['sym']),3) or not np.isfinite(x).all(): raise ValueError(f'bad geometry {p}')
        q=work/'geometries'/p.name; q.parent.mkdir(exist_ok=True); shutil.copy2(p,q)
        geoms[k]=dict(file=str(q.relative_to(work)),sha256=digest(q),smiles=smi,
                      note='Frozen stored coordinates. run_one rounds xyz.json to 5 decimals; identity is recomputed.')
        for i,r in d[(d.solute==k)|(d.solvent==k)].iterrows():
            records.append(dict(query=f'{k}:{i}',key=k,solute=r.solute,solvent=r.solvent,T=float(r['T']),
                                role='solute' if r.solute==k else 'solvent',benchmark_row=int(i)))
    rows=pd.DataFrame(records)
    if len(rows)!=2302 or Counter(zip(rows.key,rows['T']))!=Counter(zip(old.key,old['T'])):
        raise ValueError('historical 25/2302 occurrence manifest mismatch')
    rows.to_csv(work/'queries.csv',index=False)
    package_versions={}
    from importlib.metadata import version, PackageNotFoundError
    for name in ['numpy','scipy','pandas','pyscf','pyberny','rdkit']:
        try: package_versions[name]=version(name)
        except PackageNotFoundError: package_versions[name]='not installed on manifest host'
    files=sorted(set(PHYSICS) | {str(p) for p in Path('src/zcosmo').rglob('*.py')}
                 | {str(p) for p in Path('scripts').glob('r3_*.py')})
    hashes={p:digest(p) for p in files}
    write_json(work/'manifest.json',dict(reference=BASE,geometries=geoms,physics_sha256=hashes,
        queries_sha256=digest(work/'queries.csv'),rotations={k:v.tolist() for k,v in rotations().items()},
        packages_on_manifest_host=package_versions,registration=a.registration,
        cooh_flag=os.environ.get('ZC_R3_COOH_FLAG','0')))
    (work/'keys.txt').write_text('\n'.join(geoms)+'\n')
    print(f'Frozen {len(geoms)} geometries / {len(rows)} query occurrences at {work}')

def check_inputs(work):
    m=manifest(work)
    if os.environ.get('ZC_R3_COOH_FLAG','0')!=m['cooh_flag']: raise ValueError('COOH protocol changed; freeze a new experiment')
    if digest(Path(work)/'queries.csv')!=m['queries_sha256']: raise ValueError('query manifest changed')
    for p,h in m['physics_sha256'].items():
        if digest(p)!=h: raise ValueError(f'physics/input file changed: {p}; freeze a separate arm')
    return m

def item(a):
    m=check_inputs(a.work)
    import pyscf
    if pyscf.__version__!='2.14.0': raise RuntimeError('native gate requires pyscf==2.14.0')
    from zcosmo.pyscf_cosmo import cosmo_segments, to_profiles, write_sigma as native_write, BOHR, cavity_volume
    from zcosmo.pyscf_cosmo_v2 import OPEN_SHELL
    from rdkit import Chem
    gref=m['geometries'][a.key]; path=Path(a.work)/gref['file']
    if digest(path)!=gref['sha256']: raise ValueError('geometry changed')
    g=json.loads(path.read_text()); sym=g['sym']; x=np.asarray(g['x'],float)
    R=np.asarray(m['rotations'][a.rotation]); centroid=x.mean(0)
    x=(x-centroid)@R.T+centroid
    if a.method=='canonical':
        table=Chem.GetPeriodicTable(); masses=[table.GetAtomicWeight(s) for s in sym]
        x=canonical_xyz(x,masses)
    target=Path(a.work)/a.method/a.rotation; target.mkdir(parents=True,exist_ok=True)
    dest=target/f'{a.key}.sigma'
    if dest.exists(): raise FileExistsError(f'{dest}; use a fresh arm, do not silently reuse an output')
    order=41 if a.method=='lebedev41' else 29
    t=time.perf_counter(); seg,e=cosmo_segments(sym,x,lebedev=order,spin=OPEN_SHELL.get(gref['smiles'],0))
    out,meta=to_profiles(sym,x,seg)
    meta.update(source='R3 experiment, not adopted',geometry_converged='R3-frozen-geometry',
        r3_method=a.method,r3_rotation=a.rotation,registration=m['registration'],
        input_geometry_sha256=gref['sha256'],E_scf_Eh=float(e),lebedev_order=order)
    native_write(dest,out,meta,a.key)
    np.savez_compressed(target/f'{a.key}.segments.npz',x=x,sym=np.asarray(sym),**seg)
    # Co-rotating existing segments tests the parser, NOT new electronic/surface quadrature.
    Q=rotations()['r3']; segq=dict(seg); segq['xyz']=seg['xyz']@Q.T
    oq,mq=to_profiles(sym,x@Q.T,segq)
    p=np.stack([out.psigmaA_nhb,out.psigmaA_OH,out.psigmaA_OT])
    pq=np.stack([oq.psigmaA_nhb,oq.psigmaA_OH,oq.psigmaA_OT])
    parser_error=float(abs(p-pq).max())
    normals=seg['xyz']*BOHR-x[np.asarray(seg['atom'],int)]
    normals/=np.linalg.norm(normals,axis=1)[:,None]
    flux=(normals*seg['area'][:,None]).sum(0)
    # A finite surface can violate area-normal closure and make the volume origin-dependent.
    shift=np.array([1.,2.,3.]); shifted=dict(seg); shifted['xyz']=seg['xyz']+shift/BOHR
    v0=cavity_volume(seg,x/BOHR); vt=cavity_volume(shifted,(x+shift)/BOHR)
    report=dict(key=a.key,method=a.method,rotation=a.rotation,segments=len(seg['q']),
        sum_q_e=float(np.sum(seg['q'])),parser_corotation_max_dpsigmaA=parser_error,
        parser_corotation_dvolume_A3=float(abs(meta['volume [A^3]']-mq['volume [A^3]'])),
        surface_normal_closure_A2=flux.tolist(),translation_volume_observed_A3=float(vt-v0),
        translation_volume_predicted_A3=float(shift@flux/3),
        profile_sha256=digest(dest),wall_s=time.perf_counter()-t,descriptors=profile_descriptors(dest))
    write_json(target/f'{a.key}.diagnostic.json',report)
    if parser_error>=1e-7: raise AssertionError('co-rotated parser control failed; investigate before attributing variation to SCF')
    if abs((vt-v0)-shift@flux/3)>1e-8: raise AssertionError('translation-volume identity failed')
    print(json.dumps(report))

def average(a):
    m=check_inputs(a.work); n=16 if a.method=='mean16' else 8; offset=8 if a.method=='mean8b' else 0
    target=Path(a.work)/a.method/'id'; target.mkdir(parents=True,exist_ok=True)
    keys=[a.key] if a.key else list(m['geometries'])
    for k in keys:
        files=[Path(a.work)/'raw'/f'r{i}'/f'{k}.sigma' for i in range(offset,offset+n)]
        loaded=[read_sigma(p) for p in files]
        flags=[v[2].get('disp. flag') for v in loaded]
        if len(set(flags))!=1: raise ValueError('orientation changed the discrete dispersion flag')
        sigma=loaded[0][0]; p=np.mean([v[1] for v in loaded],axis=0); meta=dict(loaded[0][2])
        meta.update({'area [A^2]':float(p.sum()),'volume [A^3]':float(np.mean([v[2]['volume [A^3]'] for v in loaded])),
                     'r3_method':a.method,'r3_rotation':'id','source':'R3 equal-weight profile-quadrature average, not a conformer ensemble',
                     'members_sha256':[digest(f) for f in files], 'E_scf_Eh':float(np.mean([v[2]['E_scf_Eh'] for v in loaded]))})
        dest=target/f'{k}.sigma'
        if dest.exists(): raise FileExistsError(dest)
        write_sigma(dest,sigma,p,meta)

def worker(a):
    # A new process for EACH target/profile set, including UD. Never switch loader environments in process.
    work=Path(a.work); m=check_inputs(work)
    rows=pd.read_csv(work/'queries.csv'); rows=rows[rows.key==a.key]
    os.environ.pop('ZC_SIGMA_OVERRIDE_DIR',None)
    from zcosmo.cosmosac import SIGMA_DIR
    if not SIGMA_DIR.is_dir(): raise FileNotFoundError('UD profiles absent: run score on the asset-bearing Mac, not a bare Actions runner')
    with tempfile.TemporaryDirectory(prefix='r3-profile-set-') as td:
        if a.background and a.profile_set=='UD':
            raise ValueError('UD baseline requires the UD background; open-background reference must be an explicit identity profile set')
        if a.background:
            bg=Path(a.background).resolve()
            for k in set(rows.solute)|set(rows.solvent):
                f=bg/f'{k}.sigma'
                if not f.is_file(): raise FileNotFoundError(f'missing exact open-background profile {f}')
                (Path(td)/f.name).symlink_to(f)
        if a.profile_set!='UD':
            f=Path(a.profile_set).resolve()/f'{a.key}.sigma'
            if not f.is_file(): raise FileNotFoundError(f)
            target=Path(td)/f.name
            if target.is_symlink() or target.exists(): target.unlink()
            target.symlink_to(f)
        os.environ['ZC_SIGMA_OVERRIDE_DIR']=td
        from zcosmo.models import make_model
        from zcosmo.cosmosac import sigma_path
        compounds=pd.read_csv('data/benchmark/compounds.csv'); smi=dict(zip(compounds.inchikey,compounds.smiles))
        used={}
        for k in set(rows.solute)|set(rows.solvent):
            p=sigma_path(k)
            if p is None: raise FileNotFoundError(k)
            used[k]=dict(path=str(p.resolve()),sha256=digest(p))
        cache={}; records=[]
        for r in rows.itertuples():
            result=dict(query=r.query,key=r.key,solute=r.solute,solvent=r.solvent,T=r.T,role=r.role)
            for name in ('cosmosac_dsp','Z0x'):
                mk=(name,r.solute,r.solvent)
                try:
                    if mk not in cache: cache[mk]=make_model(name,[r.solute,r.solvent],[smi[r.solute],smi[r.solvent]])
                    result[name]=float(cache[mk].lngamma_inf(r.T,0)); result[name+'_error']=''
                except Exception as ex:
                    result[name]=np.nan; result[name+'_error']=type(ex).__name__+': '+str(ex)[:200]
            records.append(result)
        pd.DataFrame(records).to_csv(a.out,index=False)
        write_json(str(a.out)+'.inputs.json',used)

def score(a):
    work=Path(a.work); m=check_inputs(work); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    chunks=[]; t=time.perf_counter()
    for k in m['geometries']:
        p=out/f'{k}.csv'
        cmd=[sys.executable,str(Path(__file__).resolve()),'worker','--work',str(work),'--key',k,
             '--profile-set',a.profile_set,'--out',str(p)]
        if a.background: cmd += ['--background',a.background]
        subprocess.run(cmd,check=True); chunks.append(pd.read_csv(p))
    d=pd.concat(chunks,ignore_index=True)
    if len(d)!=2302 or d['query'].duplicated().any(): raise ValueError('missing/duplicate query occurrences')
    d.to_csv(out/'values.csv',index=False)
    write_json(out/'timing.json',dict(wall_s=time.perf_counter()-t,rows=len(d),profile_set=a.profile_set,background=a.background))

def compare(a):
    base=pd.read_csv(a.reference).set_index('query'); changes=[]; failed=False
    summaries=[]
    for spec in a.candidate:
        label,path=spec.split('=',1); d=pd.read_csv(path).set_index('query')
        if set(d.index)!=set(base.index): raise ValueError('query identity mismatch')
        d=d.loc[base.index]
        for model in ('cosmosac_dsp','Z0x'):
            x=base[model].to_numpy(float); y=d[model].to_numpy(float)
            mask=np.isfinite(x); same=np.array_equal(mask,np.isfinite(y))
            if not same or not mask.any(): failed=True
            valid=mask&np.isfinite(y); delta=y[valid]-x[valid]
            summaries.append(dict(label=label,model=model,rows=len(x),finite_reference=int(mask.sum()),
                same_finite_mask=bool(same),max_abs=float(abs(delta).max()) if len(delta) else None,
                median_abs=float(np.median(abs(delta))) if len(delta) else None,
                mean_abs=float(abs(delta).mean()) if len(delta) else None))
            for role in ('solute','solvent'):
                sub=valid&(base.role.to_numpy()==role)
                if sub.any(): summaries.append(dict(label=label,model=model,role=role,rows=int(sub.sum()),max_abs=float(abs(y[sub]-x[sub]).max()),mean_abs=float(abs(y[sub]-x[sub]).mean())))
            q=base.loc[valid,['key','solute','solvent','T','role']].copy(); q['query']=q.index
            q['label']=label; q['model']=model; q['delta']=delta; changes.append(q)
    out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    pd.concat(changes).to_csv(out/'row_deltas.csv',index=False)
    write_json(out/'comparison.json',dict(summaries=summaries,coverage_pass=not failed))
    print(json.dumps(summaries,indent=2))
    if failed: raise SystemExit('coverage mismatch or empty finite comparison; not accepted')

def main():
    p=argparse.ArgumentParser(); s=p.add_subparsers(dest='cmd',required=True)
    q=s.add_parser('freeze'); q.add_argument('--work',required=True); q.add_argument('--geometry-dir',required=True); q.add_argument('--registration',required=True)
    q=s.add_parser('item'); q.add_argument('--work',required=True); q.add_argument('--key',required=True)
    q.add_argument('--method',choices=['raw','canonical','lebedev41'],default='raw'); q.add_argument('--rotation',choices=list(rotations()),default='id')
    q=s.add_parser('average'); q.add_argument('--work',required=True); q.add_argument('--method',choices=['mean8','mean8b','mean16'],required=True); q.add_argument('--key')
    for name in ('score','worker'):
        q=s.add_parser(name); q.add_argument('--work',required=True); q.add_argument('--profile-set',required=True); q.add_argument('--out',required=True); q.add_argument('--background')
        if name=='worker': q.add_argument('--key',required=True)
    q=s.add_parser('compare'); q.add_argument('--reference',required=True); q.add_argument('--candidate',action='append',required=True); q.add_argument('--out',required=True)
    a=p.parse_args(); globals()[a.cmd](a)
if __name__=='__main__': main()
