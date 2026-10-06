"""Finite local profile-stability probe. Fresh process per immutable profile replacement.

This tests the saved stress points only. It never certifies all geometries in a
ball, supplies a ThermoML score, or marks a geometry Berny-converged.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import numpy as np
from r6_common import sha,write,fresh,check_inputs

PROBES=('XLYOFNOQVPJJNP-UHFFFAOYSA-N','OKKJLVBELUTLKV-UHFFFAOYSA-N',
        'BKIMMITUMNQMOS-UHFFFAOYSA-N','XTHFKEDIFFGKHM-UHFFFAOYSA-N')


def worker(a):
    key=a.key;background=Path(a.background).resolve();required=set(PROBES)|{key}
    inputs={}
    with tempfile.TemporaryDirectory(prefix='r6-stress-') as td:
        for k in required:
            p=Path(a.profile).resolve() if k==key else background/(k+'.sigma')
            if not p.is_file():raise FileNotFoundError('no UD fallback: '+str(p))
            inputs[str(p)]=sha(p)
            (Path(td)/(k+'.sigma')).symlink_to(p)
        os.environ['ZC_SIGMA_OVERRIDE_DIR']=td;os.environ['ZC_R6_ENDPOINT']='1'
        from zcosmo.z0x import Z0xBinary
        rows=[]
        for other in PROBES:
            if other==key:continue
            for T in (250.,298.15,400.):
                for pair in ((key,other),(other,key)):
                    try:value=float(Z0xBinary(list(pair)).lngamma_inf(T,0));error=''
                    except Exception as e:value=None;error=repr(e)
                    if value is not None and not np.isfinite(value):value=None;error='nonfinite'
                    rows.append(dict(pair=pair,T=T,value=value,error=error))
        check_inputs(inputs)
        write(a.out,dict(profile_sha256=sha(a.profile),inputs=inputs,rows=rows))


def run(a):
    plan=json.loads(Path(a.manifest).read_text());check_inputs(plan['inputs']);out=fresh(a.out)
    reports=[];eligible=True
    for j in plan['jobs']:
        folder=Path(j['argv'][j['argv'].index('--out')+1]);status=json.loads((folder/'status.json').read_text())
        if status['status']!='diagnostic_complete' or not status.get('force_gate'):
            reports.append(dict(case=j['id'],status='local_stationarity_not_established'));eligible=False;continue
        key=status['key'];profiles=[folder/'center.sigma']+sorted(p for p in folder.glob('*.sigma') if p.name!='center.sigma')
        if len(profiles)!=status['profiles']:raise ValueError('stress panel changed')
        records=[]
        for i,p in enumerate(profiles):
            target=out/(j['id']+f'-{i}.json')
            subprocess.run([sys.executable,str(Path(__file__).resolve()),'worker','--key',key,
                '--background',a.background,'--profile',str(p),'--out',str(target)],check=True)
            records.append(json.loads(target.read_text()))
        ref=records[0]['rows'];largest=0.;valid=True
        expected_n=6*sum(k!=key for k in PROBES)
        if len(ref)!=expected_n:raise ValueError('incomplete reference probe panel')
        for r in records[1:]:
            if len(r['rows'])!=len(ref):raise ValueError('incomplete candidate probe panel')
            check_inputs(r['inputs'])
            for x,y in zip(ref,r['rows']):
                if x['pair']!=y['pair'] or x['T']!=y['T']:raise ValueError('probe identity changed')
                if (x['value'] is None)!=(y['value'] is None):valid=False
                if x['value'] is not None and y['value'] is not None:largest=max(largest,abs(x['value']-y['value']))
        check_inputs(records[0]['inputs'])
        finite=sum(r['value'] is not None for r in ref)
        ok=bool(valid and finite>0 and largest<.01)
        reports.append(dict(case=j['id'],finite_reference_queries=finite,max_sampled_delta_lngamma=largest,
                            profile_stability_gate=ok,stress_profiles=len(profiles),globally_certified=False))
        eligible &= ok
    check_inputs(plan['inputs'])
    write(out/'summary.json',dict(registration=plan['registration'],cases=reports,all_fixed_cases_pass=eligible,
        scope='A declared finite diagnostic, not an accepted force-only production convergence rule.',adopted=False))
    if not eligible:raise SystemExit(2)


def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
    q=s.add_parser('run');q.add_argument('--manifest',required=True);q.add_argument('--background',required=True);q.add_argument('--out',required=True)
    q=s.add_parser('worker')
    for name in ('key','background','profile','out'):q.add_argument('--'+name,required=True)
    a=p.parse_args();globals()[a.cmd](a)
if __name__=='__main__':main()
