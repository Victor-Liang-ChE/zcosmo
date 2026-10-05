"""Raw PCM charge and parser diagnostics, with explicitly unadopted A projections.

The neutral Gaussian sphere is an analytic reference, not a molecule benchmark.
No charge is silently renormalized. Native calculations require pinned PySCF.
"""
from __future__ import annotations
import argparse
from importlib.metadata import version
import json
from pathlib import Path
import time
import numpy as np
from scipy.linalg import lu_factor,lu_solve
from scipy.special import erf,erfc
from scipy.spatial.distance import cdist
from r3_common import digest,write_json,profile_descriptors
from r4_common import geometry,parser_trace,contacts


def gaussian_sphere(t,Z=1.,f=1.):
    """Neutral point nucleus + normalized Gaussian electrons; zero boundary potential."""
    return dict(t=float(t),total_solute_charge=0.,
        screening_charge_e=float(-f*Z*erfc(t)),
        electrons_outside=float(Z*(erfc(t)+2*t/np.sqrt(np.pi)*np.exp(-t*t))))


def project(q,area,K):
    """Two different A sensitivities. Neither is an outlying-charge correction."""
    q=np.asarray(q,float);area=np.asarray(area,float);K=np.asarray(K,float)
    if q.shape!=area.shape or K.shape!=(len(q),len(q)) or np.any(area<=0): raise ValueError('bad projection inputs')
    c=np.linalg.solve(K,np.ones(len(q))); den=float(c.sum())
    if not np.isfinite(den) or den<=0: raise ValueError('invalid capacitance direction')
    qa=q-q.sum()*area/area.sum(); qc=q-q.sum()*c/den
    for x in (qa,qc):
        if abs(x.sum())>1e-10: raise AssertionError('charge constraint failed')
    return qa,qc,c


def pcm_settings(s,order,radius_scale=1.):
    from pyscf.data import elements
    from zcosmo.pyscf_cosmo import RADII,BOHR
    s.method='C-PCM';s.eps=1e9;s.lebedev_order=order;s.vdw_scale=1.
    table=np.zeros(120)
    for el,r in RADII.items(): table[elements.charge(el)]=radius_scale*r/BOHR
    s.radii_table=table


def factory(sym,x,spin,basis,memory):
    import pyscf
    if pyscf.__version__!='2.14.0': raise RuntimeError('requires pyscf==2.14.0')
    from pyscf import gto,dft
    from zcosmo.pcm_lu import cache_pcm3c
    mol=gto.M(atom=list(zip(sym,x.tolist())),basis=basis,unit='Angstrom',spin=spin,verbose=0,max_memory=memory)
    mf=(dft.UKS(mol) if spin else dft.RKS(mol)).density_fit().PCM()
    mf=cache_pcm3c(mf);mf.xc='b88,p86';mf.grids.level=3;mf.conv_tol=1e-9
    pcm_settings(mf.with_solvent,29)
    return mf


def segments(s,q=None):
    from zcosmo.pyscf_cosmo import BOHR
    surf=s.surface; area=np.asarray(surf['area']);keep=area>1e-8
    owners=np.concatenate([np.full(int(b-a),i) for i,(a,b) in enumerate(surf['gslice_by_atom'])])
    q=np.asarray(s._intermediates['q'] if q is None else q)
    return dict(xyz=np.asarray(surf['grid_coords'])[keep],q=q[keep],area=area[keep]*BOHR**2,atom=owners[keep]),keep


def potential(coords,s,c):
    """Potential of the discrete capacitary Gaussian layer, in atomic units."""
    d=cdist(coords,np.asarray(s.surface['grid_coords']))
    xi=np.asarray(s.surface['charge_exp'])[None,:]
    value=np.empty_like(d); nz=d>1e-14
    np.divide(erf(xi*d),d,out=value,where=nz)
    value[~nz]=np.broadcast_to(2*xi/np.sqrt(np.pi),d.shape)[~nz]
    return value@c


def density_partition(mf,dm,s,level):
    """A volume-quadrature check of q=-f integral rho*u, partitioned about the sphere union.

    The sphere union is a declared diagnostic boundary. SWIG is smooth, so its
    inside/outside split is not claimed to be a unique physical cavity partition.
    """
    from pyscf import dft
    from pyscf.data import elements
    from zcosmo.pyscf_cosmo import RADII,BOHR
    mol=mf.mol;K=np.asarray(s._intermediates['K']);c=np.linalg.solve(K.T,np.ones(len(K)))
    grids=dft.gen_grid.Grids(mol);grids.level=level;grids.build()
    xyz=mol.atom_coords();rad=np.array([RADII[el]/BOHR for el in mol.elements])
    N=Nu=Nout=Din=Dout=0.
    for lo in range(0,len(grids.coords),256):
        p=grids.coords[lo:lo+256];w=grids.weights[lo:lo+256]
        ao=dft.numint.eval_ao(mol,p,deriv=0)
        rho=dft.numint.eval_rho(mol,ao,dm,xctype='LDA')
        u=potential(p,s,c);outside=(cdist(p,xyz)>=rad[None,:]).all(1)
        wr=w*rho;N+=float(wr.sum());Nu+=float(wr@u);Nout+=float(wr[outside].sum())
        z=wr*(1-u);Din+=float(z[~outside].sum());Dout+=float(z[outside].sum())
    un=potential(xyz,s,c);Z=mol.atom_charges();Dn=float(Z@(1-un));f=float(s._intermediates['f_epsilon'])
    q=float(np.asarray(s._intermediates['q']).sum());qhat=-f*(float(Z@un)-Nu)
    parts=-f*(float(Z.sum())-N)+f*Dn-f*Din-f*Dout
    if abs(parts-qhat)>1e-9: raise AssertionError('partition algebra failed')
    return dict(level=level,points=len(grids.coords),electron_count=N,electron_count_error=N-mol.nelectron,
        electrons_outside_union=Nout,nuclear_defect_e=Dn,electron_inside_defect_e=Din,
        electron_outside_defect_e=Dout,screening_charge_e=q,quadrature_charge_e=qhat,
        quadrature_charge_error_e=qhat-q,
        nuclear_contribution_e=f*Dn,inside_contribution_e=-f*Din,outside_contribution_e=-f*Dout,
        note='Interpret outlying charge only after both levels agree and total electron/charge quadrature converges.')


def molecule(a):
    sym,x=geometry(a.geometry);out=Path(a.out)
    if out.exists() and any(out.iterdir()): raise FileExistsError(out)
    out.mkdir(parents=True,exist_ok=True);t=time.perf_counter()
    mf=factory(sym,x,a.spin,a.basis,a.memory);e=mf.kernel()
    if not mf.converged or not np.isfinite(e): raise RuntimeError('SCF failed')
    s=mf.with_solvent;it=s._intermediates;K=np.asarray(it['K']);q=np.asarray(it['q']);v=np.asarray(it['v_grids'])
    R=np.asarray(it['R']);seg,keep=segments(s)
    from zcosmo.pyscf_cosmo import to_profiles,write_sigma
    native,meta=to_profiles(sym,x,seg);p,traceout,trace=parser_trace(sym,x,seg)
    arr=lambda o:np.stack([o.psigmaA_nhb,o.psigmaA_OH,o.psigmaA_OT])
    if np.max(abs(arr(native)-arr(traceout)))>1e-10: raise AssertionError('parser instrumentation changed bins')
    meta.update(source='R4 charge diagnostic, not adopted',r4_registration=a.registration,
        geometry_converged='R4-frozen',E_scf_Eh=float(e),input_geometry_sha256=digest(a.geometry))
    write_sigma(out/f'{a.key}.sigma',native,meta,a.key)
    np.savez_compressed(out/f'{a.key}.segments.npz',sym=np.asarray(sym),x=x,**seg)
    dm=np.asarray(it['dm']);dm=dm.sum(axis=0) if dm.ndim==3 else dm
    ne=float(np.einsum('ij,ji->',dm,mf.get_ovlp()))
    rhs=R@v
    report=dict(key=a.key,basis=a.basis,grid_level=3,lebedev_order=29,eps=1e9,
        spin=a.spin,SCF_converged=True,electron_count_overlap=ne,declared_electrons=mf.mol.nelectron,
        surface_points=len(q),kept_points=int(keep.sum()),raw_full_q_e=float(q.sum()),raw_kept_q_e=float(q[keep].sum()),
        omitted_q_e=float(q[~keep].sum()),q_sym_sum_e=float(np.asarray(it['q_sym']).sum()),
        q_vs_qsym_max_e=float(np.max(abs(q-np.asarray(it['q_sym'])))),
        linear_residual_relative=float(np.max(abs(K@q-rhs))/max(1.,np.max(abs(rhs)))),
        K_symmetry_relative=float(np.max(abs(K-K.T))/max(1.,np.max(abs(K)))),
        parser=trace,geometry_contacts=contacts(sym,x),profile=profile_descriptors(out/f'{a.key}.sigma'),
        native_pyscf=version('pyscf'),input_geometry_sha256=digest(a.geometry),registration=a.registration)
    if abs(ne-mf.mol.nelectron)>1e-7 or report['linear_residual_relative']>1e-10:
        raise AssertionError('electron count or PCM linear solve failed')
    if a.projections:
        qa,qc,c=project(q,np.asarray(s.surface['area']),K)
        report['projections']={}
        for name,newq in [('area_zero',qa),('capacitary_zero',qc)]:
            sub=out/name;sub.mkdir();qs,_=segments(s,newq);z,mm=to_profiles(sym,x,qs)
            mm.update(meta);mm.update(source='R4 A charge-constraint sensitivity, not OCC, not adopted',r4_projection=name)
            write_sigma(sub/f'{a.key}.sigma',z,mm,a.key)
            report['projections'][name]=dict(sum_q_e=float(newq.sum()),
                boundary_residual_variation=float(np.ptp(K@(newq-q))),
                descriptors=profile_descriptors(sub/f'{a.key}.sigma'))
    if a.sweep:
        from pyscf.solvent.pcm import PCM
        from zcosmo.pcm_lu import CachedPCM
        sweep=[]
        for order,scale in [(29,1.),(41,1.),(59,1.),(29,1.10)]:
            sp=CachedPCM(mf.mol);sp.max_memory=a.memory;pcm_settings(sp,order,scale)
            sp._get_vind(dm)
            sweep.append(dict(order=order,radius_scale=scale,frozen_density=True,
                points=len(sp._intermediates['q']),sum_q_e=float(np.sum(sp._intermediates['q']))))
        report['fixed_density_sweep']=sweep
    if a.quadrature:
        report['density_partitions']=[density_partition(mf,dm,s,level) for level in (4,5)]
        a4,a5=report['density_partitions']
        report['quadrature_gate']=bool(abs(a5['electron_count_error'])<1e-5 and
            abs(a5['quadrature_charge_error_e'])<1e-5 and
            abs(a5['electron_outside_defect_e']-a4['electron_outside_defect_e'])<1e-4 and
            abs(a5['electron_inside_defect_e']-a4['electron_inside_defect_e'])<1e-4)
    report['wall_s']=time.perf_counter()-t;write_json(out/'charge.json',report)
    print(json.dumps(report,indent=2))
    if a.quadrature and not report['quadrature_gate']: return 2
    return 0


def sphere_native(a):
    import pyscf
    if pyscf.__version__!='2.14.0': raise RuntimeError('requires pyscf==2.14.0')
    from pyscf import gto
    from pyscf.solvent.pcm import PCM
    mol=gto.M(atom='He 0 0 0',basis='def2-svp',verbose=0)
    records=[]; radius=4.
    for order in (29,41,59):
        s=PCM(mol);s.method='C-PCM';s.eps=1e9;s.lebedev_order=order
        tab=np.full(120,radius);s.radii_table=tab;s.build()
        K=s._intermediates['K'];xi=np.asarray(s.surface['charge_exp']);f=s._intermediates['f_epsilon']
        lu=lu_factor(K)
        for t in (6.,1.5):
            alpha=(t/radius)**2;effective=xi*np.sqrt(alpha)/np.sqrt(xi*xi+alpha)
            # Convolve the analytic source with the SAME Gaussian test functions as the PCM surface.
            v=(erf(xi*radius)-erf(effective*radius))/radius
            q=lu_solve(lu,-f*v)
            exact=gaussian_sphere(t,f=f)
            records.append(dict(order=order,points=len(q),**exact,discrete_screening_charge_e=float(q.sum()),
                error_to_continuum_e=float(q.sum()-exact['screening_charge_e']),
                residual=float(np.max(abs(K@q+f*v)))))
    write_json(a.out,dict(records=records,note='Synthetic analytic source, not a molecular density. No SCF or experimental data.'))


def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
    q=s.add_parser('analytic');q.add_argument('--out',required=True)
    q=s.add_parser('sphere-native');q.add_argument('--out',required=True)
    q=s.add_parser('molecule');q.add_argument('--geometry',required=True);q.add_argument('--key',required=True)
    q.add_argument('--out',required=True);q.add_argument('--registration',required=True)
    q.add_argument('--basis',choices=['def2-svp','def2-tzvp'],default='def2-tzvp')
    q.add_argument('--spin',type=int,default=0);q.add_argument('--memory',type=int,default=6000)
    q.add_argument('--quadrature',action='store_true');q.add_argument('--sweep',action='store_true')
    q.add_argument('--projections',action='store_true')
    a=p.parse_args()
    if a.cmd=='analytic': write_json(a.out,dict(spheres=[gaussian_sphere(t) for t in (6.,1.5)]))
    elif a.cmd=='sphere-native': sphere_native(a)
    else: raise SystemExit(molecule(a))
if __name__=='__main__':main()
