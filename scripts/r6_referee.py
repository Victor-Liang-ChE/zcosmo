"""Bounded local stationarity and profile-sensitivity diagnostic, NOT a new optimizer.

No stopped long chain may enter this pilot. This produces no Berny convergence
claim, Hessian positivity certificate, liquid ensemble, or production profile.
The observed finite-stress envelope is not a bound over a geometry ball.
"""
from __future__ import annotations
import argparse
from importlib.metadata import version
import json
import os
import time
from pathlib import Path
import numpy as np
from scipy.linalg import null_space
from scipy.constants import physical_constants, c, pi
from r3_common import STALL_KEYS
from r4_common import geometry
from r6_common import BASE,sha,write,fresh,registration,profile_envelope


def projected_modes(H, xyz_bohr, masses):
    """Cartesian Hessian Eh/Bohr^2, masses in amu. Remove rigid-body subspace."""
    x=np.asarray(xyz_bohr,float);m=np.asarray(masses,float)
    n=len(m);r=x-np.average(x,axis=0,weights=m);sm=np.sqrt(m)
    rigid=[]
    for e in np.eye(3):
        rigid.append((sm[:,None]*np.broadcast_to(e,(n,3))).ravel())
        rigid.append((sm[:,None]*np.cross(np.broadcast_to(e,(n,3)),r)).ravel())
    rigid=np.column_stack(rigid)
    Q=null_space(rigid.T,rcond=1e-10)
    mass=np.repeat(sm,3);K=np.asarray(H)/mass[:,None]/mass[None,:]
    D=Q.T@((K+K.T)/2)@Q;vals,U=np.linalg.eigh(D)
    vectors=(Q@U)/mass[:,None]
    Eh=physical_constants['Hartree energy'][0]
    bohr=physical_constants['Bohr radius'][0]
    amu=physical_constants['atomic mass constant'][0]
    scale=np.sqrt(Eh/(bohr*bohr*amu))/(2*pi*c*100)
    freq=np.sign(vals)*np.sqrt(abs(vals))*scale
    return vals,vectors,freq


def thermo_harmonic(freq_cm,T):
    """Diagnostic quantum harmonic internal free energy, no absolute-value/floor rescue."""
    from scipy.constants import h,k,N_A
    nu=np.asarray(freq_cm,float)
    if (nu<=0).any() or not np.isfinite(nu).all():raise ValueError('nonpositive vibrational mode: harmonic partition invalid')
    z=h*c*100*nu/(k*T)
    return float(np.sum(.5*h*c*100*nu*N_A/4184 + .00198720425864083*T*np.log(-np.expm1(-z))))


def modes(a):
    reg=registration(a.registration)
    if a.key in STALL_KEYS:raise ValueError('Stopped-chain campaign remains closed; this pilot excludes those six keys')
    if version('pyscf')!='2.14.0' or version('pyberny')!='0.7.0':raise RuntimeError('Pinned PySCF/pyberny required')
    from r3_precision import factory
    from zcosmo.pyscf_cosmo import BOHR,cosmo_segments,to_profiles,write_sigma
    sym,x=geometry(a.geometry)
    evidence=json.loads(Path(a.consistency).read_text())
    if evidence['input_sha256']!=sha(a.geometry) or not evidence['full_response_consistent']:
        raise ValueError('Matched full-response consistency evidence required before Hessians')
    os.environ['ZC_R3_COOH_FLAG']='1'
    # Two central-difference Hessians plus two center checks; fixed ceiling.
    expected=12*len(sym)+2
    if expected>360:raise ValueError(f'{expected} gradients exceed the 360-call pilot cap')
    out=fresh(a.out);start=time.perf_counter();records=[]
    write(out/'status.json',dict(status='running',base=BASE,registration=reg,input_sha256=sha(a.geometry),expected_gradients=expected))
    def check_deadline():
        if time.perf_counter()-start>7000:raise TimeoutError('7000-second internal deadline; no extension')
    def eg(pos,tight):
        check_deadline()
        mf=factory(sym,np.asarray(pos),a.spin,tight,4000)
        e=mf.kernel()
        if not mf.converged or not np.isfinite(e):raise RuntimeError('SCF failed')
        grad=mf.nuc_grad_method();grad.grid_response=bool(tight)
        g=np.asarray(grad.kernel())
        if not np.isfinite(g).all():raise RuntimeError('nonfinite gradient')
        records.append(dict(energy_Eh=float(e),gmax=float(abs(g).max()),tight=tight))
        write(out/'calls.json',records)
        return float(e),g,mf
    try:
        e0,g0,_=eg(x,False);e1,g1,mf=eg(x,True)
        Hs=[]
        for step in (.003,.006):  # Bohr, not Angstrom
            H=np.zeros((3*len(sym),3*len(sym)))
            for j in range(3*len(sym)):
                delta=np.zeros_like(x);delta.ravel()[j]=step*BOHR
                _,gp,_=eg(x+delta,True);_,gm,_=eg(x-delta,True)
                H[:,j]=((gp-gm)/(2*step)).ravel()
            Hs.append(H)
        masses=mf.mol.atom_mass_list(isotope_avg=True)
        modes=[projected_modes(H,x/BOHR,masses) for H in Hs]
        freqs=[q[2] for q in modes];negative=any((nu < -20).any() for nu in freqs)
        force_gate=bool(abs(g1).max()<5e-5 and np.sqrt(np.mean(g1*g1))<1.5e-5)
        # Hessians are finite-difference diagnostics. Frequencies near zero are not clipped.
        report=dict(base=BASE,registration=reg,key=a.key,input_sha256=sha(a.geometry),
            original_energy_Eh=e0,tight_energy_Eh=e1,original_gmax=float(abs(g0).max()),
            tight_gmax=float(abs(g1).max()),tight_grms=float(np.sqrt(np.mean(g1*g1))),
            delta_gradient_max=float(abs(g1-g0).max()),force_gate=force_gate,
            significant_negative_sampled_mode=negative,frequencies_cm1=[nu.tolist() for nu in freqs],
            Hessian_step_difference_max=float(abs(Hs[0]-Hs[1]).max()),
            Hessian_asymmetry_max=[float(abs(H-H.T).max()) for H in Hs],
            gradients=len(records),Berny_converged=False,adopted=False)
        np.savez_compressed(out/'local.npz',x=x,sym=np.array(sym),g_original=g0,g_tight=g1,H_small=Hs[0],H_large=Hs[1],masses=masses)
        if negative or not force_gate:
            report.update(status='stationarity_failed',wall_s=time.perf_counter()-start)
            write(out/'status.json',report);return 2
        # All candidate thermo numbers remain diagnostics; no floor for soft/imaginary modes.
        if all((nu>0).all() for nu in freqs):
            report['harmonic_F_kcal']={str(T):[thermo_harmonic(nu,T) for nu in freqs] for T in (250.,298.15,400.)}
            report['thermal_gate']=max(abs(v[0]-v[1]) for v in report['harmonic_F_kcal'].values())<.05
        else:report['thermal_gate']=False
        ps=[];frames=[('center',x)];profile_energies=[]
        # Fixed six softest vibrational directions, two amplitudes, both signs.
        # 25 profiles maximum; counted separately from quantum gradients.
        for j in range(min(6,modes[0][1].shape[1])):
            v=modes[0][1][:,j].reshape(-1,3)
            v=v/np.max(np.linalg.norm(v,axis=1))
            for amp in (.005,.010):
                for sign in (-1,1):frames.append((f'm{j}-a{amp}-s{sign}',x+sign*amp*v))
        for name,pos in frames:
            check_deadline();seg,e=cosmo_segments(sym,pos,spin=a.spin);p,meta=to_profiles(sym,pos,seg)
            meta.update(source='R6 local stress diagnostic, not adopted',geometry_converged='R6-diagnostic',r6_registration=reg)
            write_sigma(out/(name+'.sigma'),p,meta,a.key)
            ps.append(np.array([p.psigmaA_nhb,p.psigmaA_OH,p.psigmaA_OT]));profile_energies.append(float(e))
        report['center_E_TZVP_Eh']=profile_energies[0]
        report['center_profile_sha256']=sha(out/'center.sigma')
        report['local_data_sha256']=sha(out/'local.npz')
        report['profiles']=len(ps);report['sampled_profile_envelope']=profile_envelope(ps)
        report['scope']='Finite local stress sample; neither a basin-wide stability bound nor a local-minimum certificate.'
        report['wall_s']=time.perf_counter()-start;report['status']='diagnostic_complete'
        write(out/'status.json',report)
    except Exception as ex:
        write(out/'status.json',dict(status='censored' if isinstance(ex,TimeoutError) else 'failed',error=repr(ex),
              gradients=len(records),wall_s=time.perf_counter()-start,registration=reg,input_sha256=sha(a.geometry),adopted=False))
        raise



def probe_directions(smiles,sym,x):
    """First covalent heavy-atom single-bond rotations, then fixed internal directions.

    Directions are derivatives at this geometry, not minimized conformers or an
    H-bond filter. Units are dimensionless and max atomic displacement is one.
    """
    from rdkit import Chem
    mol=Chem.AddHs(Chem.MolFromSmiles(smiles))
    if sym!=[at.GetSymbol() for at in mol.GetAtoms()]:raise ValueError('declared atom order does not match geometry')
    adj={a.GetIdx():[n.GetIdx() for n in a.GetNeighbors()] for a in mol.GetAtoms()}
    candidates=[]
    for b in mol.GetBonds():
        i,j=b.GetBeginAtomIdx(),b.GetEndAtomIdx()
        if b.IsInRing() or b.GetBondType()!=Chem.BondType.SINGLE or min(mol.GetAtomWithIdx(i).GetAtomicNum(),mol.GetAtomWithIdx(j).GetAtomicNum())<=1:continue
        side={j};stack=[j]
        while stack:
            u=stack.pop()
            for v in adj[u]:
                if {u,v}=={i,j} or v in side:continue
                side.add(v);stack.append(v)
        axis=x[j]-x[i];axis=axis/np.linalg.norm(axis);v=np.zeros_like(x)
        for k in side:v[k]=np.cross(axis,x[k]-x[j])
        candidates.append((f'bond-{i}-{j}',v))
    rng=np.random.default_rng(20261006)
    candidates.extend((f'internal-{j}',rng.normal(size=x.shape)) for j in range(8))
    centered=x-x.mean(0);rigid=[]
    for e in np.eye(3):
        rigid.extend([np.broadcast_to(e,x.shape).ravel(),np.cross(np.broadcast_to(e,x.shape),centered).ravel()])
    Q=null_space(np.asarray(rigid),rcond=1e-10);ans=[]
    for label,v in candidates:
        v=(Q@(Q.T@v.ravel())).reshape(x.shape)
        length=np.max(np.linalg.norm(v,axis=1))
        if length<1e-10:continue
        v=v/length
        if ans:
            matrix=np.column_stack([w.ravel() for _,w in ans]+[v.ravel()])
            if np.linalg.matrix_rank(matrix,tol=1e-9)<=len(ans):continue
        ans.append((label,v))
        if len(ans)==4:break
    if len(ans)<min(4,Q.shape[1]):raise ValueError('insufficient independent direction probes')
    return ans


def consistency(a):
    reg=registration(a.registration)
    if a.key in STALL_KEYS:raise ValueError('The six stopped chains are outside the R6 pilot')
    if version('pyscf')!='2.14.0' or version('pyberny')!='0.7.0':raise RuntimeError('Pinned native environment required')
    from r3_precision import factory
    from zcosmo.pyscf_cosmo import BOHR
    from rdkit import rdBase
    if rdBase.rdkitVersion!='2026.03.6':raise RuntimeError('Match the frozen R5 RDKit 2026.03.6 direction convention')
    sym,x=geometry(a.geometry);directions=probe_directions(a.smiles,sym,x)
    out=fresh(a.out);start=time.perf_counter();energies=[]
    def scf(pos,tight):
        if time.perf_counter()-start>3400:raise TimeoutError('3400-second diagnostic deadline')
        mf=factory(sym,pos,a.spin,tight,4000);e=mf.kernel()
        if not mf.converged or not np.isfinite(e):raise RuntimeError('SCF did not converge')
        energies.append(float(e));write(out/'energies.json',energies)
        return float(e),mf
    write(out/'status.json',dict(status='running',input_sha256=sha(a.geometry),registration=reg))
    try:
        _,normal=scf(x,False);go=normal.nuc_grad_method()
        if go.grid_response:raise ValueError('Baseline grid_response differs from the registered default')
        g0=np.asarray(go.kernel());_,tight=scf(x,True)
        gt=tight.nuc_grad_method();gt.grid_response=False;g1=np.asarray(gt.kernel())
        gf=tight.nuc_grad_method();gf.grid_response=True;g2=np.asarray(gf.kernel())
        if not np.isfinite([g0,g1,g2]).all():raise ValueError('nonfinite gradient')
        records=[]
        for name,v in directions:
            slopes=[]
            for h in (.003,.006):
                ep,_=scf(x+h*BOHR*v,True);em,_=scf(x-h*BOHR*v,True)
                slopes.append((ep-em)/(2*h))
            reference=(4*slopes[0]-slopes[1])/3
            projected=[float(np.sum(g*v)) for g in (g0,g1,g2)]
            records.append(dict(direction=name,fd=slopes,Richardson=reference,
                fd_uncertainty_indicator=abs(slopes[0]-slopes[1])/3,
                grad_original=projected[0],grad_tight_no_response=projected[1],grad_tight_full_response=projected[2],
                original_error=abs(projected[0]-reference),tight_error=abs(projected[1]-reference),
                full_error=abs(projected[2]-reference)))
        stable=all(r['fd_uncertainty_indicator']<1e-7 for r in records)
        full=max(r['full_error'] for r in records);old=max(r['tight_error'] for r in records)
        passed=bool(stable and full<2e-7)
        write(out/'status.json',dict(base=BASE,registration=reg,key=a.key,status='diagnostic_complete',
            input_sha256=sha(a.geometry),records=records,SCF_evaluations=len(energies),gradient_evaluations=3,
            response_gradient_change_max=float(abs(g2-g1).max()),original_vs_tight_change_max=float(abs(g1-g0).max()),
            full_response_consistent=passed,missing_response_material=bool(passed and old>5*max(full,1e-10) and old>1e-6),
            original_gmax=float(abs(g0).max()),full_gmax=float(abs(g2).max()),
            wall_s=time.perf_counter()-start,adopted=False,
            scope='Four sampled directional tests; not a proof of gradient consistency everywhere or Berny convergence.'))
        if not passed:return 2
        return 0
    except Exception as e:
        write(out/'status.json',dict(status='censored' if isinstance(e,TimeoutError) else 'failed',error=repr(e),
            input_sha256=sha(a.geometry),registration=reg,SCF_evaluations=len(energies),adopted=False))
        raise


def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
    for name in ('consistency','modes'):
        q=s.add_parser(name);q.add_argument('--geometry',required=True);q.add_argument('--key',required=True)
        q.add_argument('--out',required=True);q.add_argument('--registration',required=True);q.add_argument('--spin',type=int,default=0)
        if name=='consistency':q.add_argument('--smiles',required=True)
        else:q.add_argument('--consistency',required=True)
    a=p.parse_args();rc=globals()[a.cmd](a)
    if rc:raise SystemExit(rc)
if __name__=='__main__':main()
