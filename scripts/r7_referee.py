"""P33: prospective finite-resolution derivative checks, not a retrospective P30 pass."""
from __future__ import annotations
from r7_common import source_fingerprint
import argparse
import json
import sys
import time
from pathlib import Path
import numpy as np
from r7_common import (BASE,sha,write,fresh,geometry,versions,registration,clean_environment,
                       factory,gradient,load_plan,bounded,verdict)

from r7_common import fd_assess as assess, FD_TAU as TAU, FD_STEPS as STEPS

def plan(a):
    registration(a.registration);p,m=load_plan(a.pilot_plan);out=fresh(a.out);cases=[]
    if m['family']!='pilot':raise ValueError('Use the fixed three-case P26 pilot plan')
    for r in m['cases']:
        dest=out/(r['key']+'.json');dest.write_bytes((p.parent/r['geometry']).read_bytes())
        cases.append(dict(r,geometry=dest.name,geometry_sha256=sha(dest)))
    original=Path('cloud/r5/shape-plan');old=json.loads((original/'manifest.json').read_text())
    for name in ('methanol','ethylene_glycol'):
        r=next(x for x in old['panel'] if x['name']==name);source=original/r['geometry']
        if sha(source)!=r['geometry_sha256']:raise ValueError('Saved R5 control geometry changed')
        dest=out/(r['key']+'.json');dest.write_bytes(source.read_bytes())
        cases.append(dict(key=r['key'],smiles=r['smiles'],spin=r['spin'],geometry=dest.name,geometry_sha256=sha(dest)))
    write(out/'plan.json',dict(sources=source_fingerprint('referee'),base=BASE,registration=a.registration,family='referee',cases=cases,
        seconds_per_case=7200,maximum_SCF_per_case=82,maximum_gradients_per_case=3,
        tolerance=TAU,steps_Bohr=STEPS.tolist()))


def native(a):
    p,m=load_plan(a.plan);v=versions(native=True)
    # R7 amendment P33a: pip/importlib report the pinned RDKit 2026.03.6 as the PEP 440-normalized '2026.3.6'; compare normalized versions.
    from packaging.version import Version
    if m['family']!='referee' or v['rdkit'] is None or Version(v['rdkit'])!=Version('2026.03.6'):raise ValueError('Fixed R7 referee and RDKit 2026.03.6 required')
    r=next((x for x in m['cases'] if x['key']==a.key),None)
    if r is None:raise ValueError('Unknown referee case')
    from r6_referee import probe_directions
    from zcosmo.pyscf_cosmo import BOHR
    clean_environment();sym,x=geometry(p.parent/r['geometry']);out=fresh(a.out);start=time.monotonic();calls=[]
    def scf(pos,precision):
        if time.monotonic()-start>6800:raise TimeoutError('Referee internal deadline')
        mf=factory(sym,pos,r['spin'],precision);e=float(mf.kernel())
        if not mf.converged or not np.isfinite(e):raise RuntimeError('SCF failed')
        calls.append(dict(precision=precision,E_Eh=e,grid_points=len(mf.grids.coords),
                          small_rho_cutoff=float(mf.small_rho_cutoff)))
        write(out/'calls.json',calls)
        return e,mf
    write(out/'result.json',dict(status='running',key=a.key,input_geometry_sha256=r['geometry_sha256']))
    try:
        _,mt=scf(x,'tight');gt=np.asarray(gradient(mt,True).kernel())
        _,ms=scf(x,'strict');gf=np.asarray(gradient(ms,True).kernel());go=np.asarray(gradient(ms,False).kernel())
        if not np.isfinite([gt,gf,go]).all():raise ValueError('Nonfinite center gradient')
        records=[]
        for label,direction in probe_directions(r['smiles'],sym,x):
            direction=direction/np.linalg.norm(direction)
            tables={};counts=[]
            for precision in ('tight','strict'):
                vals=[]
                for h in STEPS:
                    pair=[]
                    for sign in (1.,-1.):
                        e,mf=scf(x+sign*h*BOHR*direction,precision)
                        pair.append(e);counts.append(len(mf.grids.coords))
                    vals.append(pair)
                tables[precision]=vals
            result=assess(tables['tight'],tables['strict'],float(np.sum(gt*direction)),
                          float(np.sum(gf*direction)),float(np.sum(go*direction)),
                          topology_stable=len(set(counts+[len(mt.grids.coords),len(ms.grids.coords)]))==1)
            result.update(direction=label,unit_L2_direction=direction.tolist(),energies=tables,
                          sampled_grid_counts=counts)
            records.append(result);write(out/'directions.json',records)
        if len(calls)>82:raise AssertionError('SCF budget exceeded')
        np.savez_compressed(out/'gradients.npz',x_A=x,full_tight=gt,full_strict=gf,off_strict=go)
        result=dict(base=BASE,registration=m['registration'],key=a.key,status='diagnostic_complete',
            input_geometry_sha256=r['geometry_sha256'],plan_sha256=sha(p),records=records,
            full_response_consistent=all(z['full_verdict']=='consistent' for z in records),
            SCF_evaluations=len(calls),gradient_evaluations=3,wall_s=time.monotonic()-start,
            center_full_gmax=float(abs(gf).max()),center_full_grms=float(np.sqrt(np.mean(gf*gf))),
            adopted=False,authorizes_optimizer=False,authorizes_R6_stage2=False)
        write(out/'result.json',result)
        # Completed diagnostics return zero even when their scientific verdict is negative.
    except Exception as e:
        write(out/'result.json',dict(status='censored_deadline' if isinstance(e,TimeoutError) else 'failed',
            error=repr(e),SCF_evaluations=len(calls),key=a.key,plan_sha256=sha(p),adopted=False))
        raise


def run_case(a):
    p,m=load_plan(a.plan)
    if m['family']!='referee':raise ValueError('Wrong family')
    bounded([sys.executable,str(Path(__file__).resolve()),'native','--plan',str(p),
             '--key',a.key,'--out',str(Path(a.out).resolve())],a.out,7200)


def check(a):
    p,m=load_plan(a.plan);results=[]
    for r in m['cases']:
        hits=[]
        for f in Path(a.results).rglob('result.json'):
            d=json.loads(f.read_text())
            if d.get('key')==r['key'] and d.get('plan_sha256')==sha(p):hits.append((f,d))
        if len(hits)!=1:raise ValueError('Missing or duplicate referee result')
        f,d=hits[0]
        if d.get('status')!='diagnostic_complete':raise ValueError('Incomplete referee')
        if d['input_geometry_sha256']!=r['geometry_sha256']:raise ValueError('Geometry identity mismatch')
        results.append(dict(key=r['key'],result_sha256=sha(f),passed=d['full_response_consistent']))
    write(a.out,dict(passed=all(r['passed'] for r in results),cases=results,
        registration=m['registration'],historical_P30_remains_failed=True,
        scope='New R7 directional gate only; no Hessian or basin integration authorized'))
    if not all(r['passed'] for r in results):raise SystemExit(2)


def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='command',required=True)
    q=s.add_parser('plan');q.add_argument('--pilot-plan',required=True);q.add_argument('--registration',required=True);q.add_argument('--out',required=True)
    for name in ('native','run_case'):
        q=s.add_parser(name);q.add_argument('--plan',required=True);q.add_argument('--key',required=True);q.add_argument('--out',required=True)
    q=s.add_parser('check');q.add_argument('--plan',required=True);q.add_argument('--results',required=True);q.add_argument('--out',required=True)
    a=p.parse_args();globals()[a.command](a)
if __name__=='__main__':main()
