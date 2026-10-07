"""P37: one fixed stage-isolation experiment, not an optimizer or rollout.

Two archived directions, four SCF arms per direction. On the PCM/pruned arm,
a fixed-AO-density layer check separates explicit PCM derivatives from the
self-consistent total-energy derivative. No profiles or experimental scores.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import time
import numpy as np
from r8_common import (BASE, CASES, ARMS, STEPS, TAU, sha, read, write,
    validate_direction, canonical_membership, match_local_nodes, fd_check,
    file_sources, check_sources)

SOURCES = ['scripts/r8_common.py', 'scripts/r8_diagnostic.py',
           'scripts/r7_common.py', 'scripts/r3_precision.py',
           'src/zcosmo/pyscf_cosmo.py', 'src/zcosmo/pcm_lu.py']


def plan(a):
    from r7_common import registration, geometry
    registration(a.registration)
    oldpath = Path('cloud/r7/referee/plan.json')
    old = read(oldpath); oldhash = sha(oldpath)
    if old['family'] != 'referee':
        raise ValueError('Expected the archived R7 referee plan')
    data = Path('docs/astra/round7/data/referee')
    out = Path(a.out)
    if out.exists():
        raise FileExistsError(out)
    planned = []; inputs = [oldpath]
    for label, (key, direction) in CASES.items():
        matches = [r for r in old['cases'] if r['key'] == key]
        if len(matches) != 1:
            raise ValueError('Missing or duplicate frozen R7 geometry')
        r = matches[0]; src = oldpath.parent / r['geometry']
        sym, xyz = geometry(src)
        if sha(src) != r['geometry_sha256'] or r['spin'] != 0:
            raise ValueError('Geometry or closed-shell scope mismatch')
        resultpath = data / (key + '.result.json'); d = read(resultpath)
        if d['status'] != 'diagnostic_complete' or d['plan_sha256'] != oldhash:
            raise ValueError('Need the exact completed P33 record for this input')
        if d['input_geometry_sha256'] != sha(src):
            raise ValueError('P33 result geometry mismatch')
        rows = [v for v in d['records'] if v['direction'] == direction]
        if len(rows) != 1:
            raise ValueError('Archived direction missing or duplicated')
        v = validate_direction(rows[0]['unit_L2_direction'], len(sym))
        planned.append(dict(label=label, key=key, geometry=label+'.json',
            geometry_sha256=sha(src), sym=sym, direction_name=direction,
            direction=v.tolist(), source_geometry=str(src),
            source_result_sha256=sha(resultpath)))
        inputs.extend([src, resultpath])
    # Finish every validation before creating a plan. No native computation here.
    sources = file_sources(SOURCES); input_hashes = file_sources(inputs)
    out.mkdir(parents=True)
    for r in planned:
        shutil.copyfile(r['source_geometry'], out/r['geometry'])
    write(out/'plan.json', dict(base=BASE, registration=a.registration, cases=planned,
        arms=list(ARMS), sources=sources, inputs=input_hashes,
        seconds_per_job=3600, SCF_calls_per_job=22, steps_Bohr=STEPS.tolist(), tau=TAU,
        budgets=dict(jobs=8, four_core_worker_hours=8, SCF_calls=176,
                     total_gradients=24, explicit_PCM_energy_calls=44, PCM_gradients=4),
        authorizes_optimization=False, authorizes_profiles=False,
        reason='Isolate one unresolved P33 regression against one already-consistent direction'))


def load_plan(path):
    p=Path(path).resolve(); m=read(p)
    if m['base'] != BASE or m['arms'] != list(ARMS) or m['steps_Bohr'] != STEPS.tolist() or m['tau'] != TAU:
        raise ValueError('Unregistered diagnostic definition')
    if m['seconds_per_job'] != 3600 or m['SCF_calls_per_job'] != 22:
        raise ValueError('Diagnostic budget changed')
    if {r['label'] for r in m['cases']} != set(CASES) or len(m['cases']) != 2:
        raise ValueError('Fixed cases changed')
    from r7_common import registration
    registration(m['registration']); check_sources(m['sources']); check_sources(m['inputs'])
    for r in m['cases']:
        if (r['key'], r['direction_name']) != CASES[r['label']]:
            raise ValueError('Fixed direction changed')
        if sha(p.parent/r['geometry']) != r['geometry_sha256']:
            raise ValueError('Frozen geometry changed')
        from r7_common import geometry
        sym, _ = geometry(p.parent/r['geometry'])
        if sym != r['sym']:
            raise ValueError('Frozen atom identity mismatch')
        validate_direction(r['direction'], len(r['sym']))
    return p,m


def xc_nodes(mf):
    """Map retained SCF nodes to (owner, atomic-template ordinal), ignoring padding."""
    grids=mf.grids; mol=mf.mol
    tab=grids.gen_atomic_grids(mol, grids.atom_grid, grids.radi_method,
                              grids.level, grids.prune)
    owner=np.asarray(grids.atm_idx, dtype=int)
    valid=owner >= 0; owners=owner[valid]
    coords=np.asarray(grids.coords)[valid]; weights=np.asarray(grids.weights)[valid]
    atoms=mol.atom_coords(); ordinals=np.empty(len(owners), dtype=np.int64)
    for i in range(mol.natm):
        use=owners==i
        ordinals[use]=match_local_nodes(coords[use]-atoms[i], tab[mol.atom_symbol(i)][0])
    signature, order=canonical_membership(owners, ordinals)
    return dict(signature=signature, count=len(owners)), (owners,ordinals,weights,order), tab


def response_grid_check(mf, actual, tab):
    """Compare the quadrature used in full-response integration with SCF quadrature.

    This costs no SCF and does not replace the actual gradient implementation.
    """
    from pyscf.grad.rks import grids_response_cc
    owners=[]; ordinals=[]; weights=[]; atoms=mf.mol.atom_coords()
    for i,(coords,w,_dw) in enumerate(grids_response_cc(mf.grids)):
        owners.extend([i]*len(w))
        ordinals.extend(match_local_nodes(coords-atoms[i], tab[mf.mol.atom_symbol(i)][0]))
        weights.extend(w)
    digest,order=canonical_membership(owners,ordinals)
    ao,an,aw,aorder=actual
    actual_digest,_=canonical_membership(ao,an)
    same=digest==actual_digest
    equal=False; difference=None
    if same:
        a=np.asarray(aw)[aorder]; b=np.asarray(weights)[order]
        difference=float(np.max(abs(a-b))) if len(a) else 0.
        equal=bool(np.allclose(a,b,rtol=1e-10,atol=1e-12))
    return dict(membership_identical=same, weights_match=equal,
        max_weight_difference=difference, relative_tolerance=1e-10, absolute_tolerance=1e-12)


def pcm_nodes(s):
    from pyscf.dft.gen_grid import MakeAngularGrid
    surf=s.surface; nodes=MakeAngularGrid(int(surf['ng']))[:,:3]
    owners=[]; ordinals=[]
    for i,(lo,hi) in enumerate(surf['gslice_by_atom']):
        owners.extend([i]*(hi-lo))
        ordinals.extend(match_local_nodes(surf['norm_vec'][lo:hi], nodes))
    digest,_=canonical_membership(owners,ordinals)
    return dict(signature=digest, count=len(owners),
        minimum_switch=float(np.min(surf['switch_fun'])),
        note='Retained surface-node identity; continuous switching weights are not fixed')


def make_mf(sym, xyz, precision, arm):
    from r7_common import factory
    mf=factory(sym,xyz,0,precision)
    # Runtime code, not a docstring, decides the actual density-pruning default.
    if float(mf.small_rho_cutoff) != 0.:
        raise RuntimeError('Unexpected density pruning: baseline differs; no silent override')
    if arm.endswith('_unpruned'):
        mf.grids.prune=None
    if arm.startswith('vacuum_'):
        mf=mf.undo_solvent()
        if getattr(mf,'with_solvent',None) is not None:
            raise RuntimeError('Vacuum control still has PCM attached')
    return mf


def full_gradient(mf, response):
    g=mf.nuc_grad_method(); g.grid_response=bool(response)
    if not bool(getattr(g,'auxbasis_response',False)):
        raise RuntimeError('Density-fitting derivative was detached')
    out=np.asarray(g.kernel(),float)
    if not np.isfinite(out).all():
        raise RuntimeError('Nonfinite gradient')
    return out


def pcm_layer_check(template, xyz, direction, deadline, out):
    """Derivative of E_PCM(R,P0) at FIXED AO coefficient matrix P0.

    The basis functions move with the atoms and the surface charges are solved
    anew. This is NOT a fixed physical electron density, a total BO derivative,
    or the derivative of the PCM component along an SCF solution curve.
    """
    from pyscf.solvent.pcm import PCM
    from zcosmo.pcm_lu import CachedPCM3c
    from zcosmo.pyscf_cosmo import BOHR
    P=np.asarray(template.make_rdm1()).copy()
    if P.ndim!=2:
        raise ValueError('This fixed two-case pilot is restricted to closed-shell RKS')
    old=template.with_solvent; records=[]; all_energies={}; center_energies={}; grad={}
    settings=('method','eps','lebedev_order','radii_table','vdw_scale','r_probe','surface_discretization_method')
    for engine,cls in (('stock',PCM),('cached',CachedPCM3c)):
        energies=[]
        for index,(h,sign) in enumerate([(0.,0.)]+[(float(h),s) for h in STEPS for s in (1.,-1.)]):
            if time.monotonic()>deadline:
                raise TimeoutError('Native fixed deadline')
            mol=template.mol.copy(); mol.set_geom_(xyz+sign*h*BOHR*direction,unit='Angstrom')
            if mol.nao!=P.shape[0]:
                raise ValueError('AO basis changed')
            s=cls(mol); s.max_memory=4000
            for name in settings:
                val=getattr(old,name)
                setattr(s,name,val.copy() if isinstance(val,np.ndarray) else val)
            e=float(s._get_vind(P)[0]); it=s._intermediates
            residual=float(np.max(abs(it['K']@it['q']-it['R']@it['v_grids']))/
                           max(1.,np.max(abs(it['R']@it['v_grids']))))
            if not np.isfinite(e) or residual>1e-10:
                raise RuntimeError('PCM energy/linear solve failed')
            if index==0:
                center_energies[engine]=e
                grad[engine]=np.asarray(s.grad(P))
                if not np.isfinite(grad[engine]).all():
                    raise RuntimeError('Nonfinite PCM derivative')
            else:
                energies.append(e)
            records.append(dict(engine=engine,h_Bohr=h,sign=sign,energy_Eh=e,
                solve_residual=residual,PCM=pcm_nodes(s),
                overlap_electrons=float(np.einsum('ij,ji->',P,mol.intor_symmetric('int1e_ovlp')))))
            write(out/'layer_calls.json',records)
        all_energies[engine]=np.asarray(energies).reshape(5,2)
    stock=all_energies['stock']; cached=all_energies['cached']
    gs=float(np.sum(grad['stock']*direction)); gc=float(np.sum(grad['cached']*direction))
    assessment=fd_check(stock,cached,gs,gc,gs,
        topology_stable=len({r['PCM']['signature'] for r in records})==1)
    assessment['precision_interpretation']='Two float64 implementations at identical fixed P0, not a high-precision oracle'
    parity=dict(max_energy_difference_Eh=max(float(np.max(abs(stock-cached))),
                abs(center_energies['stock']-center_energies['cached'])),
                max_gradient_difference_Eh_Bohr=float(np.max(abs(grad['stock']-grad['cached']))))
    parity['passed']=bool(parity['max_energy_difference_Eh']<1e-9 and parity['max_gradient_difference_Eh_Bohr']<1e-8)
    write(out/'layer.json',dict(assessment=assessment,parity=parity,center_energy_Eh=center_energies,
        energies={k:v.tolist() for k,v in all_energies.items()},
        projected_gradient={'stock':gs,'cached':gc},
        fixed_AO_density_sha256=__import__('hashlib').sha256(P.tobytes()).hexdigest(),
        explicit_energy_evaluations=len(records), gradient_evaluations=2,
        scope='Explicit PCM partial derivative only; overlap electron count can change off center'))


def native(a):
    from importlib.metadata import version
    from packaging.version import Version
    from r7_common import geometry,clean_environment
    for package,expected in (('pyscf','2.14.0'),('pyberny','0.7.0')):
        if Version(version(package))!=Version(expected):
            raise RuntimeError('Requires the registered pinned native environment')
    p,m=load_plan(a.plan)
    r=next(x for x in m['cases'] if x['label']==a.case)
    if a.arm not in ARMS:
        raise ValueError('Unknown arm')
    out=Path(a.out); out.mkdir(parents=True,exist_ok=False)
    clean_environment();sym,xyz=geometry(p.parent/r['geometry'])
    v=validate_direction(r['direction'],len(sym))
    from zcosmo.pyscf_cosmo import BOHR
    start=time.monotonic();deadline=start+3400;calls=[];center=None;tables={};gradients={};checks={}
    import importlib
    upstream = [importlib.import_module(name) for name in (
        'pyscf.dft.rks', 'pyscf.dft.gen_grid', 'pyscf.grad.rks',
        'pyscf.df.grad.rks', 'pyscf.solvent.pcm', 'pyscf.solvent.grad.pcm')]
    provenance=dict(packages={name:version(name) for name in ('pyscf','pyberny','numpy','scipy')},
        upstream_sha256={mod.__name__:sha(mod.__file__) for mod in upstream},
        base=BASE,registration=m['registration'],plan_sha256=sha(p),
        label=a.case,key=r['key'],arm=a.arm,geometry_sha256=r['geometry_sha256'],
        direction=r['direction_name'],adopted=False,optimization_authorized=False)
    write(out/'result.json',dict(provenance,status='running'))
    def evaluate(pos,precision):
        if len(calls)>=22 or time.monotonic()>deadline:
            raise TimeoutError('Fixed SCF/evaluation budget exhausted')
        mf=make_mf(sym,pos,precision,a.arm)
        record=dict(index=len(calls),precision=precision,status='started')
        calls.append(record);write(out/'calls.json',calls)
        e=float(mf.kernel())
        if not mf.converged or not np.isfinite(e):
            raise RuntimeError('SCF failed; no alternate solver or retry')
        signature,node_data,tab=xc_nodes(mf)
        record.update(status='completed',energy_Eh=e,XC=signature,
            small_rho_cutoff=float(mf.small_rho_cutoff),
            prune=repr(mf.grids.prune),SCF_cycles=int(getattr(mf,'cycles',-1)),
            PCM=pcm_nodes(mf.with_solvent) if a.arm.startswith('pcm_') else None)
        write(out/'calls.json',calls)
        return e,mf,node_data,tab
    try:
        for precision in ('tight','strict'):
            _,mf,nodes,tab=evaluate(xyz,precision)
            if precision == 'strict':
                center=mf
            gradients[precision]=full_gradient(mf,True)
            checks[precision]=response_grid_check(mf,nodes,tab)
        off=full_gradient(center,False)
        for precision in ('tight','strict'):
            e=[]
            for h in STEPS:
                pair=[]
                for sign in (1.,-1.):
                    value,tmp_mf,tmp_nodes,tmp_tab=evaluate(xyz+sign*h*BOHR*v,precision)
                    pair.append(value)
                    del tmp_mf,tmp_nodes,tmp_tab
                    __import__('gc').collect()
                e.append(pair)
            tables[precision]=e
        stable=len({r['XC']['signature'] for r in calls})==1
        if a.arm.startswith('pcm_'):
            stable=stable and len({r['PCM']['signature'] for r in calls})==1
        same_quadrature=all(q['membership_identical'] and q['weights_match'] for q in checks.values())
        assessment=fd_check(tables['tight'],tables['strict'],
            float(np.sum(gradients['tight']*v)),float(np.sum(gradients['strict']*v)),
            float(np.sum(off*v)),topology_stable=stable and same_quadrature)
        np.savez_compressed(out/'center.npz',xyz_A=xyz,dm_strict=center.make_rdm1(),
                            full_tight=gradients['tight'],full_strict=gradients['strict'],off_strict=off)
        if a.arm=='pcm_pruned':
            pcm_layer_check(center,xyz,v,deadline,out)
        write(out/'result.json',dict(provenance,status='diagnostic_complete',
            assessment=assessment,energies=tables,response_grid_check=checks,
            membership_stable=stable,SCF_evaluations=len(calls),gradient_evaluations=3,
            wall_s=time.monotonic()-start,precision={'tight':[1e-11,1e-7],'strict':[1e-12,1e-8]},
            scope='Two directions only; a changed vacuum density prevents additive solvent attribution'))
    except Exception as exc:
        write(out/'result.json',dict(provenance,status='censored_deadline' if isinstance(exc,TimeoutError) else 'failed',
            error=repr(exc),SCF_evaluations=len(calls),wall_s=time.monotonic()-start))
        raise


def run(a):
    from r7_common import bounded
    p,m=load_plan(a.plan)
    record=bounded([sys.executable,str(Path(__file__).resolve()),'native','--plan',str(p),
                   '--case',a.case,'--arm',a.arm,'--out',str(Path(a.out).resolve())],a.out,3600)
    dest=Path(a.out); result=dest/'result.json'
    d=read(result) if result.exists() else {}
    if record['execution_status']!='completed' or record['returncode']!=0 or d.get('status')!='diagnostic_complete':
        # Keep the child's partial result; provide a terminal execution envelope.
        write(dest.with_name(dest.name+'.terminal.json'),dict(status='deadline' if record['execution_status']=='deadline' else 'failed',
            execution=record,partial_status=d.get('status'),plan_sha256=sha(p),case=a.case,arm=a.arm))
        raise SystemExit(2)
    write(dest.with_name(dest.name+'.terminal.json'),dict(status='completed',execution=record,
        scientific_verdict=d['assessment']['full_verdict'],plan_sha256=sha(p),case=a.case,arm=a.arm))


def collect(a):
    if Path(a.out).exists():
        raise FileExistsError(a.out)
    p,m=load_plan(a.plan); ph=sha(p); rows=[]; missing=[]
    parsed=[(f,read(f)) for f in Path(a.results).rglob('result.json')]
    terminals=[(f,read(f)) for f in Path(a.results).rglob('*.terminal.json')]
    for f,d in parsed:
        if d.get('plan_sha256')==ph and (d.get('label') not in CASES or d.get('arm') not in ARMS):
            raise ValueError('Unexpected job identity in this experiment')
    for case in CASES:
        for arm in ARMS:
            hits=[(f,d) for f,d in parsed if d.get('plan_sha256')==ph and
                  d.get('label')==case and d.get('arm')==arm]
            terminal=[(f,d) for f,d in terminals if d.get('plan_sha256')==ph and
                      d.get('case')==case and d.get('arm')==arm]
            if len(hits)>1 or len(terminal)>1:
                raise ValueError('Duplicate result; do not select a favorable repeat')
            if not hits or hits[0][1].get('status')!='diagnostic_complete':
                missing.append(dict(case=case,arm=arm,
                    status=hits[0][1].get('status') if hits else 'missing',
                    execution=terminal[0][1] if terminal else None))
                continue
            if (len(terminal)!=1 or terminal[0][1].get('status')!='completed' or
                    terminal[0][1].get('execution',{}).get('returncode')!=0):
                raise ValueError('Native completion lacks a successful bounded execution record')
            f,d=hits[0]
            expected=next(r for r in m['cases'] if r['label']==case)
            if d['key']!=expected['key'] or d['geometry_sha256']!=expected['geometry_sha256']:
                raise ValueError('Result input identity mismatch')
            if d['SCF_evaluations']!=22 or d['gradient_evaluations']!=3:
                raise ValueError('Incomplete native evaluation count')
            row=dict(case=case,arm=arm,sha256=sha(f),assessment=d['assessment'],
                response_grid_check=d['response_grid_check'],wall_s=d['wall_s'],
                packages=d['packages'],upstream_sha256=d['upstream_sha256'],
                terminal_sha256=sha(terminal[0][0]))
            if arm=='pcm_pruned':
                layer=f.parent/'layer.json'
                if not layer.exists():
                    raise ValueError('Completed pruned PCM arm lacks layer diagnostic')
                row['layer']=read(layer);row['layer_sha256']=sha(layer)
                if row['layer']['explicit_energy_evaluations']!=22 or row['layer']['gradient_evaluations']!=2:
                    raise ValueError('Incomplete explicit PCM diagnostic')
            rows.append(row)
    environments={json.dumps([r['packages'],r['upstream_sha256']],sort_keys=True) for r in rows}
    if len(environments)>1:
        raise ValueError('Native arms used different package versions or upstream sources')
    by={(r['case'],r['arm']):r for r in rows}
    baseline_reproduced=None
    if ('TEG','pcm_pruned') in by and ('EG','pcm_pruned') in by:
        baseline_reproduced=(by['TEG','pcm_pruned']['assessment']['full_verdict']=='inconsistent'
            and by['EG','pcm_pruned']['assessment']['full_verdict']=='consistent')
    write(a.out,dict(base=BASE,registration=m['registration'],plan_sha256=ph,complete=not missing,
        baseline_P33_pattern_reproduced=baseline_reproduced,
        requested_jobs=8,completed_jobs=len(rows),missing_or_failed=missing,rows=rows,
        authorizes_optimizer=False,authorizes_630_repolish=False,authorizes_chain_retry=False,
        scope='Attribute only resolved contrasts. Inconclusive or failed arms remain visible.'))
    if missing:
        raise SystemExit(2)


def main():
    p=argparse.ArgumentParser(); s=p.add_subparsers(dest='command',required=True)
    q=s.add_parser('plan');q.add_argument('--registration',required=True);q.add_argument('--out',required=True)
    for name in ('run','native'):
        q=s.add_parser(name);q.add_argument('--plan',required=True);q.add_argument('--case',choices=CASES,required=True)
        q.add_argument('--arm',choices=ARMS,required=True);q.add_argument('--out',required=True)
    q=s.add_parser('collect');q.add_argument('--plan',required=True);q.add_argument('--results',required=True);q.add_argument('--out',required=True)
    a=p.parse_args();globals()[a.command](a)


if __name__=='__main__':
    main()
