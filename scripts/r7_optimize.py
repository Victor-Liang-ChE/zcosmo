"""P32: one gradient-response intervention, fresh Berny histories, bounded paired runs."""
from __future__ import annotations
import argparse
import json
import os
import sys
import time
from pathlib import Path
import numpy as np
from r7_common import (BASE,BERNY,sha,write,fresh,geometry,versions,clean_environment,
    factory,gradient,profile,assert_connectivity,load_plan,bounded,registration)


def validate_permit(a,m):
    if m['family']!='chains':return
    if not a.permit or not a.authorization:
        raise ValueError('Six-chain jobs require a recorded positive decision and authorization commit')
    registration(a.authorization);d=json.loads(Path(a.permit).read_text())
    if d.get('eligible_for_chain_trial') is not True or d.get('registration')!=m['registration']:
        raise ValueError('The supplied decision does not authorize this experiment')
    if d.get('chains_plan_sha256')!=sha(a.plan):
        raise ValueError('Chain inputs were not sealed in the approved decision')


def native(a):
    plan,m=load_plan(a.plan);validate_permit(a,m);packages=versions(native=True)
    if m.get('packages',{}).get('rdkit') not in (None,packages['rdkit']):
        raise RuntimeError('RDKit differs from the frozen starting-geometry environment')
    if m['family'] not in ('calibration','pilot','chains'):raise ValueError('Not an optimizer plan')
    expected={'calibration':(100,1800),'pilot':(80,3600),'chains':(100,19800)}[m['family']]
    if (m['budget'],m['seconds_per_arm'])!=expected:raise ValueError('Budget differs from registration')
    rec=next((r for r in m['cases'] if r['key']==a.key),None)
    if rec is None:raise ValueError('Case not in frozen plan')
    clean_environment();sym,x=geometry(plan.parent/rec['geometry']);out=fresh(a.out)
    start=time.monotonic();trace=[];response=a.arm=='full'
    common=dict(base=BASE,registration=m['registration'],plan_sha256=sha(plan),key=a.key,
        family=m['family'],arm=a.arm,grid_response=response,packages=packages,
        input_geometry_sha256=rec['geometry_sha256'],budget=m['budget'],
        authorization_commit=a.authorization,permit_sha256=sha(a.permit) if a.permit else None,
        berny_parameters=BERNY,adopted=False)
    write(out/'result.json',dict(common,status='running'))
    from pyscf.geomopt.berny_solver import kernel
    mf=factory(sym,x,rec['spin'],'production');g=gradient(mf,response)
    def cb(env):
        scanner=env['g_scanner'];gg=np.asarray(env['gradients'])
        if bool(scanner.grid_response)!=response:raise RuntimeError('Scanner lost grid-response setting')
        if not bool(scanner.auxbasis_response):raise RuntimeError('Scanner lost DF response')
        if scanner.base.with_solvent.method.upper()!='C-PCM':raise RuntimeError('Solvent method changed')
        if not scanner.converged or not np.isfinite(env['energy']) or not np.isfinite(gg).all():
            raise RuntimeError('Unconverged SCF/gradient is not a geometry evaluation')
        state=env['optimizer']._state
        trace.append(dict(cycle=int(env['cycle']),energy_Eh=float(env['energy']),
            trust_pre_send=float(state.trust),cartesian_gmax=float(abs(gg).max()),
            cartesian_grms=float(np.sqrt(np.mean(gg*gg))),
            scf_cycles=int(getattr(scanner.base,'cycles',-1)),grid_response=bool(scanner.grid_response)))
        if len(trace)>m['budget']:raise RuntimeError('Gradient-evaluation budget exceeded')
        write(out/'trace.json',trace)
        write(out/'latest.json',dict(sym=sym,x=env['mol'].atom_coords(unit='Angstrom').tolist(),
                                    evaluations=len(trace),input_geometry_sha256=rec['geometry_sha256']))
    try:
        # grid_response is configured on Gradients, NOT passed as a Berny keyword.
        converged,mol=kernel(g,maxsteps=m['budget'],callback=cb,assert_convergence=True,**BERNY)
        result=dict(common,evaluations=len(trace),berny_converged=bool(converged),
            wall_s=time.monotonic()-start,auxbasis=repr(mf.with_df.auxbasis),
            resolved_auxiliary_basis=repr(getattr(getattr(mf.with_df,'auxmol',None),'basis',None)))
        if not converged:
            write(out/'result.json',dict(result,status='censored_evaluations'));return
        x=mol.atom_coords(unit='Angstrom');assert_connectivity(rec['smiles'],sym,x)
        geom=out/(a.key+'.xyz.json');write(geom,dict(sym=sym,x=x.tolist()))
        desc=profile(sym,x,a.key,out/(a.key+'.sigma'),rec['spin'],
            dict(geometry_converged=True,geometry_protocol='A-R7-grid-response' if response else 'R7-original-gradient-control',
                 source='R7 isolated trial; not adopted',r7_registration=m['registration'],
                 r7_plan_sha256=sha(plan),r7_input_geometry_sha256=rec['geometry_sha256']))
        result.update(status='berny_converged',profile=desc,geometry_sha256=sha(geom),
                      wall_s=time.monotonic()-start)
        write(out/'result.json',result)
    except Exception as e:
        write(out/'result.json',dict(common,status='failed',error=repr(e),
            evaluations=len(trace),wall_s=time.monotonic()-start))
        raise


def run_case(a):
    plan,m=load_plan(a.plan);validate_permit(a,m)
    r=next((r for r in m['cases'] if r['key']==a.key),None)
    if r is None:raise ValueError('Unknown case')
    if m['family']=='chains' and a.arm=='pair':
        raise ValueError('One chain arm per worker: two 5.5-hour arms exceed the runner cap')
    out=fresh(a.out)
    arms=['off','full'] if a.arm=='pair' else [a.arm]
    if len(arms)==2 and int(__import__('hashlib').sha256(a.key.encode()).hexdigest(),16)%2:
        arms.reverse()
    records=[]
    for arm in arms:
        dest=out/arm
        cmd=[sys.executable,str(Path(__file__).resolve()),'native','--plan',str(plan),
             '--key',a.key,'--arm',arm,'--out',str(dest)]
        if a.permit:cmd+=['--permit',str(Path(a.permit).resolve()),'--authorization',a.authorization]
        run=bounded(cmd,dest,int(m['seconds_per_arm']));records.append(run)
        if run['execution_status']=='deadline':
            old=json.loads((dest/'result.json').read_text()) if (dest/'result.json').exists() else {}
            trace=json.loads((dest/'trace.json').read_text()) if (dest/'trace.json').is_file() else []
            old.update(base=BASE,registration=m['registration'],plan_sha256=sha(plan),key=a.key,
                       evaluations=len(trace),
                       arm=arm,status='censored_deadline',deadline_s=m['seconds_per_arm'],
                       wall_s=run['wall_s'],adopted=False)
            write(dest/'result.json',old)
        # Continue the other arm even after a scientific or operational failure.
    write(out/'pair.json',dict(key=a.key,plan_sha256=sha(plan),order=arms,runs=records))
    if any(r['execution_status']=='child_failed' for r in records):raise SystemExit(1)


def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='command',required=True)
    for name in ('native','run_case'):
        q=s.add_parser(name);q.add_argument('--plan',required=True);q.add_argument('--key',required=True)
        q.add_argument('--arm',choices=['off','full'] if name=='native' else ['off','full','pair'],required=True)
        q.add_argument('--out',required=True);q.add_argument('--permit');q.add_argument('--authorization')
    a=p.parse_args();globals()[a.command](a)
if __name__=='__main__':main()
