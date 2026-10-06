"""Conditional A protocol: sampled lowest conductor-energy conformer, not an ensemble.

Two independent deterministic proposal pools. MMFF only generates starts.
No conformer is selected by a profile match, an experimental value, or an H-bond filter.
No production directory is written. A capped or failed member blocks acceptance.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import time
import numpy as np
from r3_common import digest,write_json,read_sigma
from r4_common import geometry,contacts
from r5_common import fresh,align,rmsd,require_registration

SEEDS=(20261005,20261006)


def molecular_indices(m):
    heavy=[a.GetIdx() for a in m.GetAtoms() if a.GetAtomicNum()>1]
    donorH=[a.GetIdx() for a in m.GetAtoms() if a.GetAtomicNum()==1 and any(n.GetAtomicNum() in (7,8) for n in a.GetNeighbors())]
    return heavy,heavy+donorH


def proposal_pool(smiles,reference,seed):
    from rdkit import Chem
    from rdkit.Chem import AllChem
    m=Chem.AddHs(Chem.MolFromSmiles(smiles));heavy,metric=molecular_indices(m)
    if len(m.GetAtoms())!=len(reference): raise ValueError('atom-order/size mismatch')
    params=AllChem.ETKDGv3();params.randomSeed=seed;params.numThreads=1
    params.maxIterations=1000;params.pruneRmsThresh=-1.;params.enforceChirality=True
    ids=list(AllChem.EmbedMultipleConfs(m,numConfs=32,params=params))
    if len(ids)!=32: raise RuntimeError('32 requested conformers did not embed; do not replace the seed')
    props=AllChem.MMFFGetMoleculeProperties(m,mmffVariant='MMFF94s')
    if props is None: raise RuntimeError('MMFF94s parameters unavailable')
    candidates=[];failures=[]
    for cid in ids:
        ff=AllChem.MMFFGetMoleculeForceField(m,props,confId=cid)
        if ff is None: raise RuntimeError('missing MMFF force field')
        status=ff.Minimize(maxIts=500)
        if status!=0: failures.append(int(cid));continue
        x=align(m.GetConformer(cid).GetPositions(),reference,heavy)
        candidates.append(dict(cid=int(cid),MMFF_energy_kcal=float(ff.CalcEnergy()),x=x))
    if failures: raise RuntimeError(f'MMFF failed for proposal ids {failures}; pool is incomplete')
    first=min(range(len(candidates)),key=lambda i:(candidates[i]['MMFF_energy_kcal'],candidates[i]['cid']))
    chosen=[first]
    for _ in range(3):
        remaining=[i for i in range(len(candidates)) if i not in chosen]
        distances={i:min(rmsd(candidates[i]['x'],candidates[j]['x'],metric) for j in chosen) for i in remaining}
        pick=max(remaining,key=lambda i:(distances[i],-candidates[i]['cid']))
        chosen.append(pick)
    return m,[candidates[i] for i in chosen]


def generate(a):
    from rdkit import Chem,rdBase
    m=json.loads(Path(a.manifest).read_text());registration=require_registration(a.registration)
    if rdBase.rdkitVersion!=m['rdkit']: raise RuntimeError('RDKit differs from the frozen planner environment')
    records=m[a.panel];r=next((q for q in records if q['key']==a.key),None)
    if r is None: raise ValueError('key not in selected frozen panel')
    ref=Path(r['geometry']);ref=ref if ref.is_absolute() else Path(a.manifest).resolve().parent/ref
    if digest(ref)!=r['geometry_sha256']: raise ValueError('frozen geometry changed')
    sym,x=geometry(ref);out=fresh(a.out);cases=[]
    (out/'reference.json').write_bytes(ref.read_bytes())
    # Rigid controls get the saved geometry only, never a fictional conformer gain.
    rigid=r['name'] in ('water','methanol')
    if rigid:
        write_json(out/'proposals.json',dict(key=a.key,rigid=True,cases=[],registration=registration));return
    for seed in SEEDS:
        mol,pool=proposal_pool(r['smiles'],x,seed)
        if sym!=[at.GetSymbol() for at in mol.GetAtoms()]: raise ValueError('proposal atom order differs')
        for rank,p in enumerate(pool):
            path=out/f's{seed}-c{rank}.json'
            record=dict(key=a.key,smiles=r['smiles'],sym=sym,x=p['x'].tolist(),seed=seed,rank=rank,
                MMFF_proposal_id=p['cid'],MMFF_energy_kcal=p['MMFF_energy_kcal'],
                reference='reference.json',reference_sha256=r['geometry_sha256'],spin=r['spin'],
                registration=registration,rdkit=rdBase.rdkitVersion)
            write_json(path,record)
            cases.append(dict(path=path.name,sha256=digest(path),seed=seed,rank=rank,probe=rank<2))
    write_json(out/'proposals.json',dict(key=a.key,smiles=r['smiles'],cases=cases,rigid=False,registration=registration,
        reference_sha256=r['geometry_sha256'],
        selection='lowest MMFF start plus three farthest starts; metric includes donor hydrogens',
        note='Probe runs ranks 0,1 per pool. Conditional full protocol runs all four, never a new seed.'))


def optimize(a):
    from importlib.metadata import version
    if version('pyscf')!='2.14.0' or version('pyberny')!='0.7.0': raise RuntimeError('requires pinned PySCF/pyberny')
    from pyscf.geomopt.berny_solver import kernel
    from r3_precision import factory
    from zcosmo.pyscf_cosmo import cosmo_segments,to_profiles,write_sigma
    g=json.loads(Path(a.input).read_text());registration=require_registration(a.registration)
    ref=Path(g['reference']);ref=ref if ref.is_absolute() else Path(a.input).resolve().parent/ref
    if digest(ref)!=g['reference_sha256']: raise ValueError('reference changed')
    sym,x=list(g['sym']),np.asarray(g['x'],float);out=fresh(a.out);records=[];t=time.perf_counter()
    from rdkit import Chem,rdBase
    if rdBase.rdkitVersion!=g['rdkit']:raise RuntimeError('RDKit differs from the frozen proposal environment')
    mol=Chem.AddHs(Chem.MolFromSmiles(g['smiles']));heavy,_=molecular_indices(mol)
    if sym!=[q.GetSymbol() for q in mol.GetAtoms()]: raise ValueError('atom order changed')
    mf=factory(sym,x,g['spin'],False,a.memory)  # unchanged registered SVP/PCM/DF/grid settings
    def callback(env):
        if not env['g_scanner'].converged or not np.isfinite(env['energy']) or not np.isfinite(env['gradients']).all(): raise RuntimeError('SCF gradient did not converge')
        state=env['optimizer']._state
        records.append(dict(cycle=int(env['cycle']),energy=float(env['energy']),trust=float(state.trust)))
        write_json(out/'trace.json',records)
        write_json(out/'latest.json',dict(sym=sym,x=env['mol'].atom_coords(unit='Angstrom').tolist()))
    write_json(out/'result.json',dict(status='running',input_sha256=digest(a.input),registration=registration))
    try:
        converged,m2=kernel(mf,maxsteps=80,callback=callback,assert_convergence=True)
        if not converged:
            write_json(out/'result.json',dict(status='censored',evaluations=len(records),budget=80,
                input_sha256=digest(a.input),wall_s=time.perf_counter()-t,registration=registration));return 2
        x=m2.atom_coords(unit='Angstrom')
        # Keep the evaluated Berny coordinates; do not rotate the converged geometry.
        os.environ['ZC_R3_COOH_FLAG']='1'
        seg,e=cosmo_segments(sym,x,spin=g['spin']);p,meta=to_profiles(sym,x,seg)
        # Connectivity must agree exactly with the declared RDKit structure.
        con=contacts(sym,x);expected=[sorted(n.GetIdx() for n in at.GetNeighbors()) for at in mol.GetAtoms()]
        actual=[sorted(row['bonds']) for row in con['atoms']]
        if expected!=actual: raise ValueError('covalent connectivity changed')
        meta.update(geometry_converged=True,source='R5 conformer trial, not adopted',
             geometry_protocol='A-R5-two-pool-lowest-conductor-energy',registration=registration,E_scf_Eh=float(e))
        write_sigma(out/(g['key']+'.sigma'),p,meta,g['key'])
        write_json(out/(g['key']+'.xyz.json'),dict(sym=sym,x=x.tolist()))
        np.savez_compressed(out/(g['key']+'.segments.npz'),sym=np.array(sym),x=x,**seg)
        write_json(out/'result.json',dict(status='stationary_sample',key=g['key'],seed=g['seed'],rank=g['rank'],
            E_TZVP_Eh=float(e),evaluations=len(records),wall_s=time.perf_counter()-t,
            profile=str(out/(g['key']+'.sigma')),geometry=str(out/(g['key']+'.xyz.json')),
            input_sha256=digest(a.input),registration=registration,contacts=con,
            caveat='Berny convergence is not a Hessian certificate or proof of a global conformer minimum.'))
        return 0
    except Exception as e:
        write_json(out/'result.json',dict(status='failed',error=repr(e),evaluations=len(records),
             wall_s=time.perf_counter()-t,input_sha256=digest(a.input),registration=registration));raise


def select(a):
    require_registration(a.registration)
    proposals=json.loads(Path(a.proposals).read_text())
    reference=json.loads(Path(a.reference_native).read_text())
    if reference['key']!=proposals['key'] or reference['method']!='tz_swig' or not reference['SCF_converged']:
        raise ValueError('reference must be the registered frozen-geometry TZVP/SWIG single point')
    if reference['geometry_sha256']!=proposals['reference_sha256']:raise ValueError('reference geometry hash mismatch')
    if proposals.get('rigid'): raise ValueError('rigid controls have no conformer selection')
    expected=[c for c in proposals['cases'] if a.stage=='full' or c['probe']]
    if len(expected)!=(8 if a.stage=='full' else 4): raise ValueError('wrong frozen proposal count')
    root=Path(a.results);runs=[]
    for c in expected:
        hits=[]
        for p in sorted(root.rglob('result.json')):
            d=json.loads(p.read_text())
            if d.get('input_sha256')==c['sha256']:hits.append((p,d))
        if len(hits)!=1: raise ValueError('require exactly one recorded run per frozen proposal; no cherry-picked reruns')
        path,d=hits[0]
        if d['status']!='stationary_sample': raise ValueError(f'incomplete pool: {path}')
        for field,suffix in [('profile','.sigma'),('geometry','.xyz.json')]:
            local=path.parent/(proposals['key']+suffix)
            if not local.is_file(): raise FileNotFoundError(local)
            d[field]=str(local.resolve())
        runs.append(d)
    best=[]
    for seed in SEEDS:
        group=[r for r in runs if r['seed']==seed]
        floor=min(r['E_TZVP_Eh'] for r in group)
        # Within 1e-7 Eh use the frozen proposal rank, not a profile/benchmark value.
        best.append(min([r for r in group if r['E_TZVP_Eh']<=floor+1e-7],key=lambda r:r['rank']))
    (sym,x),(_,y)=[geometry(r['geometry']) for r in best]
    from rdkit import Chem
    mol=Chem.AddHs(Chem.MolFromSmiles(proposals['smiles']));_,metric=molecular_indices(mol)
    dE=abs(best[0]['E_TZVP_Eh']-best[1]['E_TZVP_Eh']);geo=rmsd(x,y,metric)
    s,p,_=read_sigma(best[0]['profile']);_,q,_=read_sigma(best[1]['profile'])
    distance=float(abs(p/p.sum()-q/q.sum()).sum())
    winner=min(best,key=lambda r:(r['E_TZVP_Eh'],r['seed'],r['rank']))
    nearby=[]
    floor=min(r['E_TZVP_Eh'] for r in runs)
    for i,a0 in enumerate(runs):
        for b0 in runs[i+1:]:
            if max(a0['E_TZVP_Eh'],b0['E_TZVP_Eh'])>floor+3/627.509474: continue
            _,xa=geometry(a0['geometry']);_,xb=geometry(b0['geometry'])
            _,pa,_=read_sigma(a0['profile']);_,pb,_=read_sigma(b0['profile'])
            rr=rmsd(xa,xb,metric);lp=float(abs(pa/pa.sum()-pb/pb.sum()).sum())
            if rr>=.2 and lp>=.02: nearby.append(dict(profiles=[a0['profile'],b0['profile']],RMSD_A=rr,L1=lp))
    lower=winner['E_TZVP_Eh']<=reference['energy_Eh']+1e-4
    write_json(a.out,dict(key=proposals['key'],stage=a.stage,best_by_pool=best,candidate=winner,
        energy_disagreement_Eh=dE,heavy_plus_donorH_RMSD_A=geo,normalized_L1=distance,
        reference_energy_Eh=reference['energy_Eh'],not_higher_than_reference=bool(lower),
        internal_gate=bool(dE<=1e-4 and geo<=.15 and distance<=.02 and lower),
        low_energy_shape_sensitive_pairs=nearby,
        selected_by='TZVP conductor electronic energy only; no Boltzmann or embedding-frequency weights',
        registration=a.registration,total_evaluations=sum(r['evaluations'] for r in runs),
        total_wall_s=sum(r['wall_s'] for r in runs),not_adopted=True))



def gate(a):
    """Separate validation panel only; computational probes have no experimental responses."""
    import subprocess,sys
    from r3_common import STALL_KEYS
    from r5_common import check_fingerprint
    manifest=json.loads(Path(a.manifest).read_text());require_registration(a.registration)
    out=fresh(a.out);chosen={};summaries=[]
    for rec in manifest['validation']:
        candidates=[]
        for p in Path(a.selections).rglob('*.json'):
            d=json.loads(p.read_text())
            if d.get('key')==rec['key'] and d.get('stage')=='full' and 'best_by_pool' in d: candidates.append(d)
        if len(candidates)!=1: raise ValueError('exactly one full selection record per validation molecule required')
        d=candidates[0]
        if not d['internal_gate']: raise ValueError('seed agreement or reference-energy gate failed')
        chosen[rec['key']]=d['best_by_pool'];summaries.append(d)
    if len(chosen)!=8: raise ValueError('expected all eight separate validation molecules')
    names={'water','methanol','nonane','dimethoxyethane'}
    probes=[r['key'] for r in manifest['panel'] if r['name'] in names]
    if len(probes)!=4: raise ValueError('fixed probe panel incomplete')
    rows=[]
    for k in sorted(chosen):
        for other in probes:
            for T in (250.,298.15,400.):
                for i,j in ((k,other),(other,k)):
                    rows.append(dict(r5_row_id=f'{i}|{j}|{T}',solute=i,solvent=j,T=T))
    import pandas as pd
    queries=out/'queries.csv';pd.DataFrame(rows).to_csv(queries,index=False)
    background=Path(a.background).resolve();needed=set(chosen)|set(probes);variants={}
    for name,ix in [('reference',0),('pool2',1)]:
        folder=out/name;folder.mkdir()
        for k in needed:
            path=Path(chosen[k][ix]['profile']) if k in chosen else background/(k+'.sigma')
            if not path.is_file(): raise FileNotFoundError(path)
            (folder/(k+'.sigma')).symlink_to(path.resolve())
        variants[name]={'directory':str(folder)}
    cfg=out/'config.json';write_json(cfg,dict(variants=variants,rows=str(queries),
        compounds=manifest['compounds'],registration=a.registration))
    subprocess.run([sys.executable,str(Path(__file__).with_name('r5_terms.py')),'run','--config',str(cfg),
                    '--out',str(out/'probe-results')],check=True)
    frames=[pd.read_csv(out/'probe-results'/(name+'.csv')).set_index('r5_row_id') for name in variants]
    r,c=frames;c=c.loc[r.index]
    errors={}
    for col in ('total','dsp_total'):
        if not np.isfinite(r[col]).all() or not np.isfinite(c[col]).all(): raise ValueError('all 192 theoretical probes must be finite')
        errors[col]=float(abs(r[col]-c[col]).max())
    timing=sum(q['total_wall_s'] for q in summaries)
    accepted=max(errors.values())<.02 and timing<=64*3600
    write_json(out/'gate.json',dict(accepted=accepted,probe_rows=len(rows),seed_disagreement=errors,
         aggregate_validation_worker_hours=timing/3600,validation_budget_worker_hours=64,
         registration=a.registration,scope='eligible for one separately authorized exploratory score; no primary replacement',
         note='No experimental response or UD profile enters this numerical reproducibility gate.'))
    if not accepted:return 2
    return 0


def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
    q=s.add_parser('generate');q.add_argument('--manifest',required=True);q.add_argument('--key',required=True)
    q.add_argument('--panel',choices=['panel','validation'],default='panel');q.add_argument('--out',required=True);q.add_argument('--registration',required=True)
    q=s.add_parser('optimize');q.add_argument('--input',required=True);q.add_argument('--out',required=True)
    q.add_argument('--memory',type=int,default=4000);q.add_argument('--registration',required=True)
    q=s.add_parser('select');q.add_argument('--proposals',required=True);q.add_argument('--results',required=True)
    q.add_argument('--reference-native',required=True);q.add_argument('--stage',choices=['probe','full'],required=True);q.add_argument('--out',required=True);q.add_argument('--registration',required=True)
    q=s.add_parser('gate');q.add_argument('--manifest',required=True);q.add_argument('--selections',required=True)
    q.add_argument('--background',required=True);q.add_argument('--out',required=True);q.add_argument('--registration',required=True)
    a=p.parse_args();answer=globals()[a.cmd](a)
    if isinstance(answer,int): raise SystemExit(answer)
if __name__=='__main__':main()
