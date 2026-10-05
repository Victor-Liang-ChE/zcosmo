"""One prospective A trial: 80 tighter-SCF Berny evaluations, then <=20 original evaluations.

The control has the identical 80+20 structure with original SCF tolerances throughout.
Both stages start fresh optimizer histories. No .bstate file is read. All output is experimental.
"""
from __future__ import annotations
import argparse
from importlib.metadata import version
import json
from pathlib import Path
import time
import numpy as np
from r3_common import digest, write_json

def factory(sym, xyz, spin, tight, memory):
    from pyscf import gto, dft
    from pyscf.data import elements
    from zcosmo.pyscf_cosmo import BOHR, RADII
    from zcosmo.pcm_lu import cache_pcm3c
    mol=gto.M(atom=list(zip(sym,xyz.tolist())),unit='Angstrom',basis='def2-svp',
              spin=spin,verbose=0,max_memory=memory)
    mf=(dft.UKS(mol) if spin else dft.RKS(mol)).density_fit().PCM()
    mf=cache_pcm3c(mf); mf.xc='b88,p86'; mf.grids.level=2
    mf.conv_tol=1e-11 if tight else 1e-8
    mf.conv_tol_grad=1e-7 if tight else None
    s=mf.with_solvent; s.method='C-PCM'; s.eps=1e9; s.lebedev_order=17
    table=np.zeros(120)
    for element,r in RADII.items(): table[elements.charge(element)]=r/BOHR
    s.radii_table=table
    return mf

def run(a):
    if version('pyscf')!='2.14.0' or version('pyberny')!='0.7.0':
        raise RuntimeError('requires pyscf 2.14.0 and pyberny 0.7.0')
    from pyscf.geomopt.berny_solver import kernel
    from zcosmo.pyscf_cosmo import cosmo_segments, to_profiles, write_sigma
    out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    if any(out.iterdir()): raise FileExistsError('use a fresh arm directory')
    g=json.loads(Path(a.input).read_text()); sym=g['sym']; x=np.asarray(g['x'],float)
    if x.shape!=(len(sym),3) or not np.isfinite(x).all(): raise ValueError('bad input geometry')
    records=[]; t=time.perf_counter(); stages=[]
    for name,cap,tight in [('pre',80,a.arm=='tight'),('confirm',20,False)]:
        mf=factory(sym,x,a.spin,tight,a.memory)
        stage_records=[]
        def callback(env):
            scanner=env['g_scanner']; gradient=np.asarray(env['gradients'],float)
            if not scanner.converged or not np.isfinite(gradient).all():
                raise RuntimeError('unconverged SCF or nonfinite gradient is not an optimizer step')
            state=env['optimizer']._state
            r=dict(stage=name,cycle=int(env['cycle']),energy_Eh=float(env['energy']),
                gradient_max_Eh_Bohr=float(abs(gradient).max()),
                scf_cycles=int(getattr(scanner.base,'cycles',-1)),
                trust_pre_send=float(state.trust))
            stage_records.append(r); records.append(r)
            write_json(out/'trace.json',records)
            write_json(out/'latest.json',dict(sym=sym,x=env['mol'].atom_coords(unit='Angstrom').tolist(),
                stage=name,evaluations=len(records),registration=a.registration))
        st=time.perf_counter()
        converged,mol=kernel(mf,maxsteps=cap,callback=callback,assert_convergence=True)
        x=mol.atom_coords(unit='Angstrom')
        stages.append(dict(stage=name,budget=cap,evaluations=len(stage_records),converged=bool(converged),
                           tight_scf=tight,wall_s=time.perf_counter()-st))
    original_pass=bool(stages[-1]['converged'])
    report=dict(arm=a.arm,key=a.key,registration=a.registration,input_sha256=digest(a.input),
        pyscf=version('pyscf'),pyberny=version('pyberny'),stages=stages,
        evaluations=len(records),original_berny_pass=original_pass,wall_s=time.perf_counter()-t)
    write_json(out/'result.json',report)
    if not original_pass:
        print(json.dumps(report)); return 2  # Budget exhausted, not successful convergence.
    seg,e=cosmo_segments(sym,np.asarray(x),spin=a.spin)
    p,meta=to_profiles(sym,np.asarray(x),seg)
    meta.update(geometry_converged=True,geometry_protocol='R3-A-tight-SCF-80-plus-original-20' if a.arm=='tight' else 'R3-control-original-80-plus-20',
                source='R3 trial, not adopted',E_scf_Eh=float(e),registration=a.registration)
    write_sigma(out/f'{a.key}.sigma',p,meta,a.key)
    write_json(out/f'{a.key}.xyz.json',dict(sym=sym,x=x.tolist()))
    report.update(profile_energy_Eh=float(e),profile_sha256=digest(out/f'{a.key}.sigma'),
                  wall_s=time.perf_counter()-t)
    write_json(out/'result.json',report); print(json.dumps(report)); return 0

def main():
    p=argparse.ArgumentParser(); p.add_argument('--input',required=True); p.add_argument('--key',required=True)
    p.add_argument('--arm',choices=['control','tight'],required=True); p.add_argument('--out',required=True)
    p.add_argument('--spin',type=int,default=0); p.add_argument('--memory',type=int,default=6000)
    p.add_argument('--registration',required=True); raise SystemExit(run(p.parse_args()))
if __name__=='__main__': main()
