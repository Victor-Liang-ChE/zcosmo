"""Freeze R7 inputs before trials. Never guess the historical 25 from the 26-row CSV."""
from __future__ import annotations
from r7_common import source_fingerprint, historical_queries
import argparse
import json
import re
import shutil
import time
from pathlib import Path
import numpy as np
import pandas as pd
from r7_common import BASE,STALL,PILOT,sha,write,fresh,registration,geometry,versions

KEY_RE=re.compile(r'^[A-Z]{14}-[A-Z]{10}-[A-Z]$')

def record_geometry(out,key,source,sym=None,x=None):
    dest=out/'geometries'/(key+'.json');dest.parent.mkdir(exist_ok=True)
    if source is not None:
        geometry(source);dest.write_bytes(Path(source).read_bytes())
        provenance=dict(path=str(Path(source).resolve()),sha256=sha(source))
    else:
        write(dest,dict(sym=list(sym),x=np.asarray(x,float).tolist()));provenance=None
    return str(dest.relative_to(out)),sha(dest),provenance

def calibration(a):
    reg=registration(a.registration);src,col,q=historical_queries(a.historical)
    val=pd.read_csv('data/pyscf_sigma/validation_set.csv')
    keys=sorted(q.target.unique());missing=set(keys)-set(val.inchikey)
    if missing:raise ValueError('Historical target not in the validation source')
    if val.inchikey.duplicated().any():raise ValueError('Ambiguous validation key')
    smi=val.set_index('inchikey').smiles.to_dict();out=fresh(a.out);cases=[]
    from zcosmo.pyscf_cosmo import xtb_geometry
    for key in keys:
        t=time.monotonic();sym,x=xtb_geometry(smi[key],seed=7)
        elapsed=time.monotonic()-t;rel,digest,_=record_geometry(out,key,None,sym,x)
        cases.append(dict(key=key,smiles=smi[key],spin=0,geometry=rel,
                          geometry_sha256=digest,shared_xtb_seconds=elapsed))
    q.to_csv(out/'queries.csv',index=False)
    write(out/'plan.json',dict(sources=source_fingerprint('optimizer'),base=BASE,registration=reg,family='calibration',
        cases=cases,queries='queries.csv',queries_sha256=sha(out/'queries.csv'),
        historical_source=str(src.resolve()),historical_sha256=sha(src),target_column=col,
        packages=versions(),budget=100,seconds_per_arm=1800,
        start_protocol='One frozen seed-7 GFN2-xTB start shared by both arms; no saved DFT geometry is substituted'))

def pilot(a):
    reg=registration(a.registration);out=fresh(a.out);cases=[]
    compounds=pd.read_csv('data/benchmark/compounds.csv').set_index('inchikey')
    for key,(proposal,expected_geometry_sha) in PILOT.items():
        pp=Path('cloud/r5/proposals')/key/'proposals.json';m=json.loads(pp.read_text())
        selected=[c for c in m['cases'] if c['path']==proposal]
        if len(selected)!=1:raise ValueError('Frozen P26 proposal missing')
        input_hash=selected[0]['sha256'];hits=[]
        for p in Path(a.artifacts).rglob('result.json'):
            d=json.loads(p.read_text())
            if d.get('input_sha256')==input_hash:hits.append((p,d))
        if len(hits)!=1:raise ValueError(f'Require exactly one archived P26 result for {key}')
        p,d=hits[0]
        if d.get('status')!='censored' or d.get('evaluations')!=80:
            raise ValueError('Not the registered censored P26 member')
        source=p.parent/'latest.json'
        if sha(source)!=expected_geometry_sha:raise ValueError('P30 geometry hash mismatch; no replacement checkpoint')
        rel,h,prov=record_geometry(out,key,source)
        cases.append(dict(key=key,smiles=str(compounds.loc[key,'smiles']),spin=0,
            geometry=rel,geometry_sha256=h,source=prov,proposal_sha256=input_hash,
            source_result_sha256=sha(p)))
    write(out/'plan.json',dict(sources=source_fingerprint('optimizer'),base=BASE,registration=reg,family='pilot',cases=cases,
        budget=80,seconds_per_arm=3600,packages=versions()))

def chains(a):
    reg=registration(a.registration);out=fresh(a.out);cases=[]
    compounds=pd.read_csv('data/benchmark/compounds.csv').set_index('inchikey')
    # Use the deliberately supplied final-checkpoint directory. Never choose the
    # newest among conflicting files or read optimizer pickles from the old force field.
    for key in STALL:
        hits=list(Path(a.checkpoints).rglob(key+'.partial.json'))
        if len(hits)!=1:raise ValueError(f'Exactly one designated checkpoint required for {key}')
        rel,h,prov=record_geometry(out,key,hits[0])
        cases.append(dict(key=key,smiles=str(compounds.loc[key,'smiles']),spin=0,
                          geometry=rel,geometry_sha256=h,source=prov))
    write(out/'plan.json',dict(sources=source_fingerprint('optimizer'),base=BASE,registration=reg,family='chains',cases=cases,
        budget=100,seconds_per_arm=19800,packages=versions(),
        execution_requires='A matching positive calibration-plus-pilot decision and a separate authorization commit'))

def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='command',required=True)
    q=s.add_parser('calibration');q.add_argument('--historical',required=True)
    q=s.add_parser('pilot');q.add_argument('--artifacts',required=True)
    q=s.add_parser('chains');q.add_argument('--checkpoints',required=True)
    for q in s.choices.values():
        q.add_argument('--out',required=True);q.add_argument('--registration',required=True)
    a=p.parse_args();globals()[a.command](a)
if __name__=='__main__':main()
