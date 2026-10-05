"""Portable regression tests. No native PySCF or UD data is exercised by these tests."""
from __future__ import annotations
import argparse
import ast
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from scipy.spatial.transform import Rotation
from r3_common import canonical_xyz,rotations,keyed,write_sigma,read_sigma,write_json
from r3_idac import chemical_class

def run(a):
    result={};rng=np.random.default_rng(19)
    cases=[np.array([[0,0,0],[0,.76,.59],[0,-.76,.59]]),np.array([[0,0,0],[0,0,1.21]]),
           np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]]),rng.normal(size=(10,3))]
    error=0.
    for x in cases:
        for R in Rotation.random(100,random_state=7).as_matrix():
            error=max(error,float(abs(canonical_xyz(x@R.T+[5,-2,3])-canonical_xyz(x)).max()))
    if error>=1e-10: raise AssertionError('body frame is not rotation covariant')
    result['canonical_max_coordinate_difference_A']=error
    result['canonical_test_geometries']=len(cases);result['rotations_per_geometry']=100
    if not np.array_equal(np.array([rotations()[f'r{i}'] for i in range(8)]),Rotation.random(8,random_state=20261004).as_matrix()):
        raise AssertionError('S2 rotations not reproduced')
    # Formula-level test of Hsieh averaging on a co-rotated FIXED segment set.
    x=rng.normal(size=(40,3));areas=rng.uniform(.01,1,40);sig=rng.normal(0,.003,40);rn2=areas/np.pi;rav=7.25/np.pi
    def avg(y):
        M=np.exp(-3.57*cdist(y,y)**2/(rn2+rav))*rn2*rav/(rn2+rav)
        return (M*sig).sum(1)/M.sum(1)
    er=float(abs(avg(x)-avg(x@rotations()['r0'].T)).max())
    if er>1e-12: raise AssertionError('Hsieh formula co-rotation test failed')
    result['Hsieh_formula_max_difference_e_A2']=er
    # Four-corner Shapley identity, including the nonlinear absolute-error transformation.
    uu,ou,uo,oo,obs=rng.normal(size=(5,50));s=.5*((ou-uu)+(oo-uo));v=.5*((uo-uu)+(oo-ou))
    if abs(s+v-(oo-uu)).max()>1e-12: raise AssertionError('prediction attribution')
    e=[abs(t-obs) for t in (uu,ou,uo,oo)];es=.5*((e[1]-e[0])+(e[3]-e[2]));ev=.5*((e[2]-e[0])+(e[3]-e[1]))
    if abs(es+ev-(e[3]-e[0])).max()>1e-12: raise AssertionError('error attribution')
    result['Shapley_identity_pass']=True
    if chemical_class('CC(=O)O')!='carboxylic_acid' or chemical_class('O')!='water' or chemical_class('CC(=O)OC')!='ester': raise AssertionError('fixed structural classes')
    with tempfile.TemporaryDirectory(prefix='r3-test-') as td:
        t=Path(td); rows=[]
        for i in range(30):
            rows.append(dict(file=f'{i}.xml',dataset=i,solute=['k1','k2','k3'][i%3],solvent=['k3','k1','k2'][i%3],
                T=298.15,method='synthetic',ln_gamma_inf=i/30,split='train' if i<6 else 'test_one',pred_ln_gamma_inf=i/30+.2))
        r=pd.DataFrame(rows);c=r.copy();c.pred_ln_gamma_inf+=.1
        c=c.sample(frac=1,random_state=8).reset_index(drop=True)
        r.to_csv(t/'ref.csv',index=False);c.to_csv(t/'candidate.csv',index=False)
        pd.DataFrame(dict(inchikey=['k1','k2','k3'],smiles=['O','CO','CCCC'])).to_csv(t/'compounds.csv',index=False)
        scripts=Path(__file__).resolve().parent
        subprocess.run([sys.executable,str(scripts/'r3_idac.py'),'audit','--reference',str(t/'ref.csv'),
            '--candidate',str(t/'candidate.csv'),'--compounds',str(t/'compounds.csv'),'--out',str(t/'audit'),
            '--expect-points','24'],check=True,stdout=subprocess.DEVNULL)
        report=json.loads((t/'audit/audit.json').read_text())
        if report['same_row_identity_and_order'] or abs(report['common']['delta_mae']-.1)>1e-12: raise AssertionError('identity alignment failed')
        for group in ('solute_class','solvent_class','water_role'):
            table=pd.read_csv(t/f'audit/by_{group}.csv')
            if abs(table.contribution_to_total_delta_mae.sum()-.1)>1e-12: raise AssertionError('nonadditive class contributions')
        result['reordered_IDAC_rows_joined']=24
        duplicate=pd.concat([r.iloc[[0]],r.iloc[[0]]],ignore_index=True);duplicate.loc[1,'pred_ln_gamma_inf']+=1
        try:keyed(duplicate)
        except ValueError:pass
        else:raise AssertionError('ambiguous duplicate was accepted')
        bad=c.copy();bad.loc[0,'pred_ln_gamma_inf']=np.inf;bad.to_csv(t/'bad.csv',index=False)
        f=subprocess.run([sys.executable,str(scripts/'r3_idac.py'),'compare-fresh','--reference',str(t/'ref.csv'),
            '--candidate',str(t/'bad.csv'),'--out',str(t/'no.json')],capture_output=True)
        if f.returncode==0:raise AssertionError('nonfinite mismatch accepted')
        result['duplicate_and_nonfinite_guards_pass']=True
        grid=np.linspace(-.025,.025,51);p=rng.uniform(size=(3,51))
        meta={'volume [A^3]':100.,'area [A^2]':float(p.sum()),'disp. flag':'NHB'}
        write_sigma(t/'a.sigma',grid,p,meta);_,q,_=read_sigma(t/'a.sigma')
        if abs(p-q).max()>1e-13:raise AssertionError('profile round trip')
        result['sigma_round_trip_max_A2']=float(abs(p-q).max())
    # Version-sensitive calls are source-shape checks, NOT native API executions.
    tree=ast.parse((Path(__file__).parent/'r3_precision.py').read_text())
    kernels=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='kernel']
    if len(kernels)!=1 or {k.arg for k in kernels[0].keywords}!={'maxsteps','callback','assert_convergence'}:raise AssertionError('unexpected Berny interface')
    result['precision_budget']=dict(pre=80,original_confirmation=20)
    # Exercise the actual repository volume routine when an explicit source copy is supplied.
    if a.volume_source:
        spec=importlib.util.spec_from_file_location('r3_volume_source',a.volume_source);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        xyz=np.array([[0.,0.,0.]]);r=rng.normal(size=(20,3));r/=np.linalg.norm(r,axis=1)[:,None];r*=2
        area=rng.uniform(size=20);seg=dict(xyz=r/m.BOHR,area=area,atom=np.zeros(20,dtype=int))
        shift=np.array([1.,2.,3.]);s2=dict(seg,xyz=(r+shift)/m.BOHR)
        obs=m.cavity_volume(s2,(xyz+shift)/m.BOHR)-m.cavity_volume(seg,xyz/m.BOHR)
        pred=shift@((r/2)*area[:,None]).sum(0)/3
        if abs(obs-pred)>1e-12:raise AssertionError('finite-surface volume translation identity')
        result['actual_volume_function_translation_identity_error_A3']=float(abs(obs-pred))
    write_json(a.out,result);print(json.dumps(result,indent=2))

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--volume-source');run(p.parse_args())
if __name__=='__main__':main()
