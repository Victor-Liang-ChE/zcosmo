"""Deploy the accepted P18 correction with an auditable, metadata-only transaction.

prepare never changes source files. apply is explicit and backs up all originals.
A killed process can leave a partial application; rollback restores the complete bundle.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import numpy as np
import pandas as pd
from r3_common import digest, read_sigma, write_json
from r4_common import BASE, geometry, flag_for_geometry, selected_profiles

RULE='P18: registration 9d32e9e; acceptance recorded in 613dd8f, 2026-10-05'
PROVENANCE={'p18_rule','p18_parent_sha256','p18_geometry_sha256'}


def relabel_bytes(raw, flag, geometry_hash):
    head, sep, body=raw.partition(b'\n')
    if not sep or not head.startswith(b'# meta: '): raise ValueError('invalid sigma header')
    old=json.loads(head[8:]); new=dict(old)
    new.update({'disp. flag':flag,'p18_rule':RULE,
        'p18_parent_sha256':hashlib.sha256(raw).hexdigest(),'p18_geometry_sha256':geometry_hash})
    result=b'# meta: '+json.dumps(new,allow_nan=False).encode()+b'\n'+body
    if result.partition(b'\n')[2]!=body: raise AssertionError('raw rows or comments changed')
    for k in set(old)|set(new):
        if k not in PROVENANCE|{'disp. flag'} and old.get(k)!=new.get(k):
            raise AssertionError(f'unrelated metadata changed: {k}')
    return result


def prepare(a):
    out=Path(a.out).resolve()
    if out.exists(): raise FileExistsError(out)
    root=Path(a.root).resolve(); compounds=pd.read_csv(a.compounds)
    sources=selected_profiles(root,compounds)
    gm=json.loads(Path(a.geometry_map).read_text()) if a.geometry_map else {}
    unknown=set(gm)-set(compounds.inchikey)
    if unknown: raise ValueError(f'geometry map has unknown keys: {sorted(unknown)}')
    staged=[]; missing=[]
    for key,folder,src in sources:
        gp=Path(gm[key]).resolve() if key in gm else src.with_suffix('.xyz.json')
        if not gp.is_file(): missing.append(dict(key=key,profile=str(src),needed_geometry=str(gp))); continue
        sym,x=geometry(gp); flag=flag_for_geometry(sym,x)
        raw=src.read_bytes(); new=relabel_bytes(raw,flag,digest(gp))
        old=json.loads(raw.partition(b'\n')[0][8:])
        if old.get('disp. flag') != flag and not (old.get('disp. flag') == 'HB-DONOR-ACCEPTOR' and flag == 'COOH'):
            raise ValueError(f'unexpected non-P18 relabel for {key}; investigate geometry/provenance before deployment')
        staged.append((dict(key=key,folder=folder,source=str(src),geometry=str(gp),
            source_sha256=digest(src),geometry_sha256=digest(gp),old_flag=old.get('disp. flag'),new_flag=flag,
            candidate_sha256=hashlib.sha256(new).hexdigest(),
            raw_body_sha256=hashlib.sha256(raw.partition(b'\n')[2]).hexdigest(),
            relative=f'{folder}/{key}.sigma'),new))
    if missing:
        print(json.dumps({'missing_geometry':missing,'action':'Supply actual profile-generating coordinates in --geometry-map. No substitution of an old checkpoint.'},indent=2))
        raise SystemExit(2)
    if len(staged)!=636: raise ValueError('incomplete plan')
    out.parent.mkdir(parents=True,exist_ok=True)
    tmp=Path(tempfile.mkdtemp(prefix='p18-stage-',dir=out.parent))
    try:
        for r,new in staged:
            p=tmp/r['relative'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(new)
        write_json(tmp/'manifest.json',dict(base=BASE,rule=RULE,root=str(root),
            compounds_sha256=digest(a.compounds),parser_sha256=digest('data/raw/nist/to_sigma.py'),
            profiles=[r for r,_ in staged]))
        tmp.rename(out)
    except BaseException:
        shutil.rmtree(tmp,ignore_errors=True);raise
    verify_bundle(out,require_original=True)
    print(json.dumps({'profiles':636,'changed_flags':[r for r,_ in staged if r['old_flag']!=r['new_flag']],
                      'bundle':str(out)},indent=2))


def verify_bundle(bundle,require_original=False):
    bundle=Path(bundle).resolve(); m=json.loads((bundle/'manifest.json').read_text())
    if len(m['profiles'])!=636 or len({r['key'] for r in m['profiles']})!=636:
        raise ValueError('incomplete manifest')
    if digest('data/raw/nist/to_sigma.py')!=m['parser_sha256']: raise ValueError('parser changed')
    for r in m['profiles']:
        cp=bundle/r['relative']; raw=cp.read_bytes()
        if digest(cp)!=r['candidate_sha256']: raise ValueError(f'candidate changed: {cp}')
        if hashlib.sha256(raw.partition(b'\n')[2]).hexdigest()!=r['raw_body_sha256']:
            raise ValueError('raw sigma rows changed')
        if digest(r['geometry'])!=r['geometry_sha256']: raise ValueError('geometry changed')
        sym,x=geometry(r['geometry'])
        if flag_for_geometry(sym,x)!=r['new_flag']: raise ValueError('parser flag mismatch')
        if require_original and digest(r['source'])!=r['source_sha256']:
            raise ValueError(f'source changed: {r["source"]}')
        read_sigma(cp)
    return m


def atomic_bytes(path,raw):
    path=Path(path)
    fd,name=tempfile.mkstemp(prefix=path.name+'.p18-',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as f:
            f.write(raw);f.flush();os.fsync(f.fileno())
        os.replace(name,path)
    finally:
        if os.path.exists(name): os.unlink(name)


def apply(a):
    bundle=Path(a.bundle).resolve(); m=verify_bundle(bundle,require_original=True)
    backup=Path(a.backup).resolve()
    if backup.exists(): raise FileExistsError(backup)
    backup.mkdir(parents=True)
    for r in m['profiles']:
        p=backup/r['relative'];p.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(r['source'],p)
        if digest(p)!=r['source_sha256']: raise ValueError('backup hash failed')
    write_json(backup/'transaction.json',dict(bundle=str(bundle),manifest=m,status='backed_up',applied=[]))
    done=[]
    try:
        for r in m['profiles']:
            if digest(r['source'])!=r['source_sha256']: raise ValueError('concurrent modification')
            atomic_bytes(r['source'],(bundle/r['relative']).read_bytes());done.append(r['key'])
            write_json(backup/'transaction.json',dict(bundle=str(bundle),manifest=m,status='applying',applied=done))
        for r in m['profiles']:
            if digest(r['source'])!=r['candidate_sha256']: raise ValueError('deployed hash failed')
        write_json(backup/'transaction.json',dict(bundle=str(bundle),manifest=m,status='applied',applied=done))
    except BaseException:
        for r in m['profiles']:
            if digest(r['source']) in (r['source_sha256'],r['candidate_sha256']):
                atomic_bytes(r['source'],(backup/r['relative']).read_bytes())
        write_json(backup/'transaction.json',dict(bundle=str(bundle),manifest=m,status='failed_check_rollback',applied=done))
        raise
    print('Applied metadata-only P18 to 636 profiles; append the transaction hashes to PREREGISTRATION.md.')


def rollback(a):
    backup=Path(a.backup).resolve(); t=json.loads((backup/'transaction.json').read_text());m=t['manifest']
    for r in m['profiles']:
        if digest(backup/r['relative'])!=r['source_sha256']: raise ValueError('backup changed')
        if digest(r['source']) not in (r['source_sha256'],r['candidate_sha256']):
            raise ValueError(f'concurrent modification, refuse rollback: {r["source"]}')
    for r in m['profiles']: atomic_bytes(r['source'],(backup/r['relative']).read_bytes())
    t['status']='rolled_back';write_json(backup/'transaction.json',t)


def overlay(a):
    """Read-only unified view for scoring. Keeps the primary/flagged distinction in the bundle."""
    b=Path(a.bundle).resolve();m=verify_bundle(b)
    out=Path(a.out).resolve()
    if out.exists(): raise FileExistsError(out)
    out.mkdir(parents=True)
    for r in m['profiles']:
        if a.exclude_flagged and r['folder']!='profiles_v2': continue
        (out/f'{r["key"]}.sigma').symlink_to(b/r['relative'])
    write_json(out/'provenance.json',dict(bundle=str(b),exclude_flagged=a.exclude_flagged,
        manifest_sha256=digest(b/'manifest.json')))


def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
    q=s.add_parser('prepare');q.add_argument('--root',default='data/pyscf_sigma')
    q.add_argument('--compounds',default='data/benchmark/compounds.csv');q.add_argument('--geometry-map')
    q.add_argument('--out',required=True)
    q=s.add_parser('verify');q.add_argument('--bundle',required=True)
    q=s.add_parser('apply');q.add_argument('--bundle',required=True);q.add_argument('--backup',required=True)
    q=s.add_parser('rollback');q.add_argument('--backup',required=True)
    q=s.add_parser('overlay');q.add_argument('--bundle',required=True);q.add_argument('--out',required=True)
    q.add_argument('--exclude-flagged',action='store_true')
    a=p.parse_args()
    if a.cmd=='verify': verify_bundle(a.bundle,require_original=True);print('P18 bundle verified')
    else: globals()[a.cmd](a)
if __name__=='__main__':main()
