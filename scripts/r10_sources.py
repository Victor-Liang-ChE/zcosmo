"""P41: acquire the fixed public UD inputs. No quantum or model evaluation.

Run the real acquisition on the asset-bearing Mac after registration. The data
notice is separate from the code license. This helper does not grant use rights.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time
import urllib.request

BASE = '4dc898521f6c49355e442be78f1e2570d3686aee'
UPSTREAM = '1b82456be38026719b16cad4076109bef3fcb309'
PARSER_BLOB = '9f2e0d6f3bb4da4880f9bd6ad702847f9308ed1d'
MARKER = 'R10-P41-P42-P43: UD provenance, zero-QC replay'
PLAN_RECORD = 'docs/astra/round10/PLAN_SHA256.txt'
ROOT = Path(__file__).resolve().parents[1]
# name, benchmark key, published source key, verified upstream Git blob
DATA = (
 ('water','XLYOFNOQVPJJNP-UHFFFAOYSA-N','XLYOFNOQVPJJNP-UHFFFAOYSA-N','3d23436d2b3025016350174f12f6acdd8d032867'),
 ('methanol','OKKJLVBELUTLKV-UHFFFAOYSA-N','OKKJLVBELUTLKV-UHFFFAOYSA-N','3c69191c1aa5f04e7e9ee15e1fb83d4fd84e677b'),
 ('ethylene_glycol','LYCAIKOWRPUZTN-UHFFFAOYSA-N','LYCAIKOWRPUZTN-UHFFFAOYSA-N','b0cc75c9c38912e5a73f2b7d2c375c063169f4da'),
 ('diethylene_glycol','MTHSVFCYNBDYFN-UHFFFAOYSA-N','MTHSVFCYNBDYFN-UHFFFAOYSA-N','46c92287b77d7854f8e141e7df2745e99a12f09a'),
 ('triethylene_glycol','ZIBGPFATKBEMQZ-UHFFFAOYSA-N','ZIBGPFATKBEMQZ-UHFFFAOYSA-N','0668b927572f4ef4fdb17e5492001bd5698a04e5'),
 ('tetraethylene_glycol','UWHCKJMYHZGTIT-UHFFFAOYSA-N','UWHCKJMYHZGTIT-UHFFFAOYSA-N','5f79ef7c81b9eb669b0ca5f1ff943c9cac30ba0d'),
 ('glycerol','PEDCQBHIVMGVHV-UHFFFAOYSA-N','PEDCQBHIVMGVHV-UHFFFAOYSA-N','39e1c2167fb3ca26308ef97f75bf2eab8a289f3a'),
 ('propylene_glycol','DNIAPMSPPWPWGF-UHFFFAOYSA-N','DNIAPMSPPWPWGF-VKHMYHEASA-N','68f1bbda2363037e5246e69b1145a239908d0b8b'),
 ('methoxyethanol','XNWFRZJHXBZDAG-UHFFFAOYSA-N','XNWFRZJHXBZDAG-UHFFFAOYSA-N','f29e58fcc3f30f49122367613221fe46314f0c98'),
 ('dimethoxyethane','XTHFKEDIFFGKHM-UHFFFAOYSA-N','XTHFKEDIFFGKHM-UHFFFAOYSA-N','eea387e357e7bcb6be3441ffac3224d9de77708a'),
 ('tetrahydrofuran','WYURNTSHIVDZCO-UHFFFAOYSA-N','WYURNTSHIVDZCO-UHFFFAOYSA-N','360b38b378ab42a9098df97b84708fd5b4bc2bce'),
 ('nonane','BKIMMITUMNQMOS-UHFFFAOYSA-N','BKIMMITUMNQMOS-UHFFFAOYSA-N','3122e6a49334515b0f56edf3a8586fe54e7d7efd'),
)


def sha(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def read(path: str | Path):
    return json.loads(Path(path).read_text())


def write(path: str | Path, value) -> None:
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    text=json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n'
    tmp=p.with_name(p.name+'.tmp'); tmp.write_text(text); tmp.replace(p)


def git(*args: str) -> bytes:
    return subprocess.check_output(['git','-C',str(ROOT),*args],stderr=subprocess.PIPE)


def registration(commit: str) -> dict:
    if not re.fullmatch('[0-9a-f]{40}',commit):
        raise ValueError('Use the actual full registration commit SHA')
    git('merge-base','--is-ancestor',BASE,'HEAD')
    git('merge-base','--is-ancestor',commit,'HEAD')
    text=git('show',commit+':PREREGISTRATION.md')
    if MARKER.encode() not in text:
        raise ValueError('The commit does not contain the R10 registration marker')
    return dict(commit=commit,preregistration_sha256=hashlib.sha256(text).hexdigest())


def committed_sources(paths: list[str]) -> dict:
    result={}
    for name in paths:
        data=(ROOT/name).read_bytes()
        if data!=git('show','HEAD:'+name):
            raise ValueError('Commit the reviewed source before use: '+name)
        result[name]=hashlib.sha256(data).hexdigest()
    return result


def verify_sources(sources: dict) -> None:
    for name,expected in sources.items():
        if sha(ROOT/name)!=expected:
            raise ValueError('Source changed: '+name)


def record(path: str | Path) -> dict:
    p=Path(path).resolve(strict=True)
    if not p.is_file(): raise ValueError('Not a file: '+str(p))
    return dict(path=str(p),sha256=sha(p))


def verify_record(r: dict) -> Path:
    p=Path(r['path'])
    if not p.is_file() or sha(p)!=r['sha256']:
        raise ValueError('Frozen input missing or changed: '+str(p))
    return p


def private_output(path: str | Path) -> Path:
    p=Path(path).expanduser().resolve()
    if p.is_relative_to(ROOT) or ROOT.is_relative_to(p):
        raise ValueError('Keep recovered raw inputs and reports outside the repository')
    if p.exists(): raise FileExistsError(p)
    return p


def mac() -> None:
    if sys.platform!='darwin':
        raise RuntimeError('UD-backed acquisition/replay is registered on the Mac only')


def catalog() -> list[dict]:
    items=[]
    for name,key,source,expected in DATA:
        path='profiles/UD/cosmo/'+source+'.cosmo'
        items.append(dict(name=name,key=key,source_key=source,relative_path=path,
            expected_git_blob=expected,
            url=f'https://raw.githubusercontent.com/usnistgov/COSMOSAC/{UPSTREAM}/{path}'))
    for path,expected in (
        ('profiles/UD/Readme.txt','a536b2b8b76ba687b5f134d402baad73efb92150'),
        ('profiles/UD/complist.txt','565a7be9a604b7e0670e724b141fdc349c59459d')):
        items.append(dict(relative_path=path,expected_git_blob=expected,
            url=f'https://raw.githubusercontent.com/usnistgov/COSMOSAC/{UPSTREAM}/{path}'))
    return items


def verify_download(data: bytes, expected: str) -> None:
    if blob(data)!=expected:
        raise ValueError('Downloaded bytes do not match the verified upstream Git blob')


def acquire(a) -> int:
    mac(); reg=registration(a.registration)
    if not a.acknowledge_ud_terms:
        raise ValueError('Read the UD data notice and explicitly acknowledge applicable rights')
    source=committed_sources(['scripts/r10_sources.py'])
    out=private_output(a.out); out.mkdir(parents=True,exist_ok=False)
    start=time.perf_counter(); records=[]
    for item in catalog():
        r=dict(item,status='pending'); records.append(r)
        try:
            req=urllib.request.Request(item['url'],headers={'User-Agent':'zcosmo-R10-provenance'})
            with urllib.request.urlopen(req,timeout=30) as response:
                data=response.read(8_000_001)
                if response.status!=200 or len(data)>8_000_000:
                    raise ValueError('Unexpected status or file larger than the fixed 8 MB ceiling')
            verify_download(data,item['expected_git_blob'])
            dest=out/item['relative_path']; dest.parent.mkdir(parents=True,exist_ok=True)
            with dest.open('xb') as f: f.write(data)
            r.update(status='verified',sha256=sha(dest),bytes=len(data))
        except Exception as exc:
            r.update(status='unavailable',error=type(exc).__name__+': '+str(exc))
        write(out/'acquisition.json',dict(base=BASE,upstream=UPSTREAM,registration=reg,
            records=records,sources=source,SCF_calls=0,model_calls=0,complete=False))
    complete=all(r['status']=='verified' for r in records)
    verify_sources(source)
    write(out/'acquisition.json',dict(base=BASE,upstream=UPSTREAM,registration=reg,
        records=records,sources=source,SCF_calls=0,model_calls=0,complete=complete,
        wall_s=time.perf_counter()-start,
        rights='UD notice applies; no redistribution or commercial-use permission is granted here'))
    return 0 if complete else 2


def check(a) -> int:
    root=Path(a.source_root).resolve(); d=read(root/'acquisition.json')
    if d.get('upstream')!=UPSTREAM or d.get('complete') is not True:
        raise ValueError('Incomplete or different acquisition')
    expected=catalog()
    if len(d['records'])!=len(expected): raise ValueError('Wrong acquisition count')
    by={r['relative_path']:r for r in d['records']}
    if len(by)!=len(expected): raise ValueError('Duplicate acquisition record')
    for e in expected:
        r=by[e['relative_path']]; p=root/e['relative_path']
        verify_download(p.read_bytes(),e['expected_git_blob'])
        if r.get('status')!='verified' or sha(p)!=r['sha256']:
            raise ValueError('Acquisition record mismatch')
    print('Verified 12 COSMO files and 2 provenance documents; no SCF or model evaluation')
    return 0


def main() -> int:
    p=argparse.ArgumentParser(description=__doc__); s=p.add_subparsers(dest='cmd',required=True)
    q=s.add_parser('catalog'); q.set_defaults(fn=lambda a:print(json.dumps(catalog(),indent=2)))
    q=s.add_parser('acquire'); q.add_argument('--out',required=True)
    q.add_argument('--registration',required=True); q.add_argument('--acknowledge-ud-terms',action='store_true')
    q.set_defaults(fn=acquire)
    q=s.add_parser('check'); q.add_argument('--source-root',required=True); q.set_defaults(fn=check)
    a=p.parse_args(); return a.fn(a) or 0

if __name__=='__main__': raise SystemExit(main())
