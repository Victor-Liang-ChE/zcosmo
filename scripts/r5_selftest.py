"""Portable R5 tests. Synthetic data and RDKit proposals, never native QC acceptance."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import tempfile
import time
import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation
from r3_common import write_json
from r5_common import align,rmsd,charge_average,bin_linear,observation_ids
from r5_terms import stencil,compare
from r4_lle import strict_binodal,bounds


def coefficients(E,p):
    G=np.ones(len(p))
    for _ in range(10000):
        Gn=1/(E@(p*G));nextG=.5*(G+Gn)
        if np.max(abs(np.log(nextG/G)))<1e-13:return nextG
        G=nextG
    raise AssertionError('test segment solver did not converge')


def gauge_test():
    # Shift the labels, not an interpolated/binned approximation to their distributions.
    rng=np.random.default_rng(12);s=np.linspace(-.02,.02,17);c=8000.;RT=.593;shift=.0004
    p=rng.random(17);p/=p.sum();q=rng.random(17);q/=q.sum();mix=.3*p+.7*q
    E=np.exp(-c*(s[:,None]+s[None,:])**2/RT)
    Et=np.exp(-c*(s[:,None]+s[None,:]+2*shift)**2/RT)
    a=4*c*shift*s+2*c*shift**2;factor=np.exp(-a/RT)
    err=float(abs(Et-E*factor[:,None]*factor[None,:]).max())
    gm,gp=coefficients(E,mix),coefficients(E,p)
    hm,hp=coefficients(Et,mix),coefficients(Et,p)
    residual=float(abs(p@(np.log(gm)-np.log(gp))-p@(np.log(hm)-np.log(hp))))
    if err>1e-12 or residual>1e-10:raise AssertionError('common-shift gauge identity failed')
    return dict(kernel_error=err,residual_error=residual)


def tests():
    rng=np.random.default_rng(7);x=rng.normal(size=(11,3));R=Rotation.random(random_state=13).as_matrix()
    y=x@R+np.array([4.,-2.,1.]);alignment=float(abs(align(y,x)-x).max())
    if alignment>1e-12:raise AssertionError('Kabsch rotation failure')
    area=rng.uniform(.05,2.,11);sig=rng.uniform(-.02,.02,11)
    v=charge_average(x,area,sig,4.)
    # Literal four-way duplication is an independent check of the algebraic compressed formula.
    xx=np.repeat(x,4,axis=0);aa=np.repeat(area/4,4);ss=np.repeat(sig,4)
    literal=charge_average(xx,aa,ss,1.)[::4]
    subdivision=float(abs(v-literal).max())
    if subdivision>1e-12:raise AssertionError('patch-subdivision identity failed')
    grid=np.linspace(-.025,.025,51);p=bin_linear(sig,area,grid)
    mass=float(abs(p.sum()-area.sum()));moment=float(abs(p@grid-area@sig))
    if max(mass,moment)>1e-12:raise AssertionError('bin mass/moment failure')
    hb=rng.uniform(0,.5,(2,51));pre=rng.uniform(0,1,(3,51));ph=1-np.exp(-grid**2/(2*.007**2))
    post=pre.copy();post[1:]*=ph;post[0]+=(pre[1]+pre[2])*(1-ph)
    split=float(abs(post.sum(0)-pre.sum(0)).max())
    if split>1e-12:raise AssertionError('HB conservation identity failure')
    p0=np.array([0.,0.,0.]);phs=np.array([2.,3.,5.])*1e-4
    if not np.allclose(stencil(p0,phs,1e-4),[2,3,5]):raise AssertionError('endpoint component algebra')
    base=pd.DataFrame(dict(file=['a','b'],dataset=[1,2],solute=['x','y'],solvent=['z','z'],T=[298.,300.],
           ln_gamma_inf=[1.,2.],split=['train','test_one']))
    ids=observation_ids(base,'idac');reverse=observation_ids(base.iloc[::-1].reset_index(drop=True),'idac')
    if list(ids)!=list(reverse[::-1]):raise AssertionError('observation ids depend on row order')
    r=pd.DataFrame(dict(r5_row_id=['a','b'],solute=['x','y'],solvent=['z','z'],T=[298.,300.],
        total=[3.,4.],comb=[1.,1.],residual=[1.,2.],london=[1.,1.],kernel_00=[0.,0.],
        kernel_10=[.4,.5],kernel_01=[.4,.5],kernel_11=[1.,2.],endpoint_stencil_error=[.01,.01]))
    c=r.copy();c['total']+=.1;c['residual']+=.1;c['kernel_11']+=.1
    d=compare(r,c.iloc[::-1]);assert abs(d.ES_shapley+d.HB_shapley-.1).max()<1e-12
    bad=c.copy();bad.loc[0,'total']=np.nan
    try:compare(r,bad)
    except ValueError:pass
    else:raise AssertionError('finite coverage guard failed')
    class Ideal:
        def lngamma(self,T,x):return np.zeros(2)
    class Regular:
        def lngamma(self,T,x):return np.array([3*x[1]**2,3*x[0]**2])
    ideal=strict_binodal(Ideal(),298.15);regular=strict_binodal(Regular(),298.15)
    if ideal['status']!='no_gap_on_refined_grid' or regular['status']!='root_passes_refined_sampled_checks':
        raise AssertionError('real SciPy synthetic LLE check failed')
    b=bounds([1.,np.nan,0.,1.],['a','a','b','b'])
    if b['row_gap_found_bounds']!=[.5,.75] or b['unresolved_rows']!=1:raise AssertionError('denominator bounds failed')
    # Exercise the actual report's endpoint denominator with a witness and an unknown.
    from r5_scorecard import lle_metrics
    q=pd.DataFrame(dict(c1=['a']*4,c2=['b']*4,r5_detection=[1.,1.,0.,np.nan],x1=[.1,.2,.3,.4],
        r5_x1_I=[.1,np.nan,np.nan,np.nan],r5_x1_II=[.9,np.nan,np.nan,np.nan],
        r5_lle_status=['root_passes_sampled_checks','gap_witness_only','no_gap_on_81_grid','unresolved'],pred_split=[1.,1.,0.,1.]))
    lm=lle_metrics(q)
    if lm['endpoint_rows']!=1 or lm['rows']!=4 or lm['unresolved_rows']!=1:raise AssertionError('witness leaked into endpoint MAE')
    return dict(alignment_error_A=alignment,subdivision_error=subdivision,bin_mass_error=mass,
        bin_moment_error=moment,HB_total_bin_error=split,gauge=gauge_test(),
        ideal_status=ideal['status'],regular_status=regular['status'],denominator_checks='passed',
        scope='Portable synthetic checks, not native quantum chemistry or production score acceptance.')


def rdkit_test():
    from rdkit import Chem,rdBase
    from rdkit.Chem import AllChem
    from r5_conformers import proposal_pool
    m=Chem.AddHs(Chem.MolFromSmiles('OCCO'));p=AllChem.ETKDGv3();p.randomSeed=7
    if AllChem.EmbedMolecule(m,p)!=0:raise AssertionError('test reference failed to embed')
    x=m.GetConformer().GetPositions();t=time.perf_counter()
    _,a=proposal_pool('OCCO',x,20261005);_,b=proposal_pool('OCCO',x,20261005)
    error=max(float(abs(u['x']-v['x']).max()) for u,v in zip(a,b))
    if error!=0. or [u['cid'] for u in a]!=[u['cid'] for u in b]:raise AssertionError('proposal reproducibility failed')
    return dict(rdkit=rdBase.rdkitVersion,molecule='synthetic EG start',pools=2,selected_per_pool=len(a),
         max_coordinate_difference_A=error,wall_s=time.perf_counter()-t,scope='proposal generation only, no DFT')


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--rdkit',action='store_true');a=p.parse_args()
    d=tests()
    if a.rdkit:d['RDKit']=rdkit_test()
    write_json(a.out,d);print(json.dumps(d,indent=2))
if __name__=='__main__':main()
