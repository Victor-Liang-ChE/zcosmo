"""Portable R6 tests. Synthetic inputs, not a Mac/UD or native PySCF acceptance run."""
from __future__ import annotations
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import types
import numpy as np
from r6_common import boltzmann,profile_envelope


def endpoint():
    # Execute the actual current source with a synthetic, explicit input catalog.
    import zcosmo.cosmosac as cs
    prm=cs.Params(A_ES=11000.,B_ES=0.,c_OH_OH=5000.,c_OT_OT=4500.,c_OH_OT=4800.,disp_mode='london',w_dsp=1.)
    profiles={}
    sig=cs.SIG
    for i,(A,V) in enumerate(((100.,80.),(180.,160.),(65.,40.))):
        ps=np.zeros((3,51));ps[0]=np.exp(-((sig-.001*i)/.004)**2)
        ps[1]=.15*np.exp(-((abs(sig)-.011)/.002)**2)
        ps[2]=.1*np.exp(-((sig-.009)/.0025)**2)
        ps[:,abs(sig)>.020]=0.
        ps*=A/ps.sum();key=f'fake{i}'
        profiles[key]=cs.Fluid(key,ps,A,V,'H2O' if i==2 else 'NHB',50.,{'synthetic':True})
    original=cs.load_fluid;old_london=cs._london_table
    cs.load_fluid=lambda k,*a:profiles[k]
    cs._london_table=lambda p:{f'fake{i}':(200.+50*i,20.+3*i) for i in range(3)}
    models=types.ModuleType('zcosmo.models');models.ROOT=Path.cwd();models.load_z_params=lambda n:prm
    theory=types.ModuleType('zcosmo.zmodel');theory.c_es_theory=lambda fpol=1.:12226.235339788673*fpol
    previous={name:sys.modules.get(name) for name in ('zcosmo.models','zcosmo.zmodel')}
    sys.modules['zcosmo.models']=models;sys.modules['zcosmo.zmodel']=theory
    previous_env=os.environ.get('ZC_R6_ENDPOINT')
    try:
        spec=importlib.util.spec_from_file_location('r6_test_model',Path('src/zcosmo/z0x.py'))
        z=importlib.util.module_from_spec(spec);spec.loader.exec_module(z)
        z._eps=lambda:{'fake0':5.,'fake1':30.,'fake2':70.}
        from r6_endpoint import reference_value,fresh_stencils
        errors=[];fd=[];rev=[];off=[]
        for T in (250.,298.15,400.):
            for a,b in (('fake0','fake1'),('fake1','fake2'),('fake2','fake0')):
                m=z.Z0xBinary([a,b]);os.environ['ZC_R6_ENDPOINT']='0'
                y=m.lngamma(T,np.array([.3,.7]));legacy=m.lngamma_inf(T,0)
                os.environ['ZC_R6_ENDPOINT']='1';n=z.Z0xBinary([a,b]);new=n.lngamma_inf(T,0)
                yr=n.lngamma(T,np.array([.3,.7]));off.append(float(abs(y-yr).max()))
                ref,_=reference_value(n,T,0.);errors.append(abs(new-ref[0]))
                reverse=z.Z0xBinary([b,a]).lngamma_inf(T,1);rev.append(abs(reverse-new))
                if abs(n.lngamma(T,np.array([0.,1.]))[1])>1e-9:raise AssertionError('pure solvent does not vanish')
                fd.append(min(abs(v-new) for v in fresh_stencils(n,T).values()))
                os.environ['ZC_R6_ENDPOINT']='0'
                if abs(n.lngamma_inf(T,0)-legacy)>1e-12:raise AssertionError('opt-out changed legacy endpoint')
        assert max(errors)<1e-8 and max(rev)<1e-8 and max(off)==0. and max(fd)<1e-5
        from r6_phase import PhaseModel
        c0=12226.235339788673
        states=[]
        for i,key in enumerate(('fake0','fake1')):
            states.append(dict(id=key,molecule=key,fluid=profiles[key],eps=[5.,30.][i],
                C6_au=200.+50*i,alpha_au=20.+3*i,E_conductor_kcal=10.+i,F_nuclear_kcal=2.,degeneracy=1.))
        pm=PhaseModel(states,298.15,prm,c0)
        os.environ['ZC_R6_ENDPOINT']='1'
        refz=z.Z0xBinary(['fake0','fake1'])
        singleton_error=abs(pm.idac('fake0','fake1')['ln_gamma_inf']-refz.lngamma_inf(298.15,0))
        assert singleton_error<1e-8,singleton_error
        for u in (.01,.3,.8):
            yy=np.array([u,1-u]);phase,_=pm.excess(yy)
            assert abs(phase-refz.lngamma(298.15,yy)).max()<1e-8
        from dataclasses import replace
        other=replace(profiles['fake0'],key='fake0:basin2',psigA=profiles['fake0'].psigA.copy())
        other.psigA=np.roll(other.psigA,1,axis=1)
        alt=dict(states[0],id='second',fluid=other,E_conductor_kcal=10.4)
        pm2=PhaseModel([states[0],alt,states[1]],298.15,prm,c0)
        yy=np.array([.2,.3,.5]);ex,_=pm2.excess(yy);mu=pm2.g0+np.log(yy)+ex
        direction=np.array([1.,-1.,0.]);h=1e-5
        derivative=(pm2.free(yy+h*direction)-pm2.free(yy-h*direction))/(2*h)
        gradient_error=abs(derivative-mu@direction);assert gradient_error<1e-6,gradient_error
        pop=pm2.idac('fake0','fake1');assert abs(sum(pop['solute_trace_populations'])-1)<1e-12
        return dict(phase_singleton_error=singleton_error,phase_derivative_error=gradient_error,endpoint_reference_max=max(errors),reverse_max=max(rev),interior_change=max(off),finite_difference_best_max=max(fd))
    finally:
        cs.load_fluid=original;cs._london_table=old_london
        for name,value in previous.items():
            if value is None:sys.modules.pop(name,None)
            else:sys.modules[name]=value
        if previous_env is None:os.environ.pop('ZC_R6_ENDPOINT',None)
        else:os.environ['ZC_R6_ENDPOINT']=previous_env


def ensemble():
    w,f=boltzmann([0.,1.],298.15,[1.,2.]);v,g=boltzmann([20.,21.],298.15,[1.,2.])
    assert np.max(abs(w-v))<1e-13 and abs((g-f)-20)<1e-13
    # A twofold degeneracy is exactly two equal-energy, distinct microstates.
    z,h=boltzmann([0.,1.,1.],298.15)
    assert abs(w[0]-z[0])<1e-13 and abs(w[1]-z[1:].sum())<1e-13 and abs(f-h)<1e-13
    ps=np.zeros((2,3,51));ps[0,0,25]=100.;ps[1,1,40]=50.
    d=profile_envelope(ps)
    rng=np.random.default_rng(8)
    for _ in range(20):
        q=rng.dirichlet([1.,1.]);mix=np.einsum('k,kij->ij',q,ps)
        tail=mix[:,abs(np.linspace(-.025,.025,51))>=.01].sum()
        assert d['raw_tail_min_A2']<=tail<=d['raw_tail_max_A2']
    return dict(weight_sum=float(w.sum()),common_free_energy_shift=float(g-f))


def modes():
    from r6_referee import projected_modes,thermo_harmonic,probe_directions
    x=np.array([[0.,0.,0.],[0.,0.,2.]])
    masses=np.array([1.,1.]);v=np.array([0.,0.,-1.,0.,0.,1.])/np.sqrt(2)
    H=.1*np.outer(v,v);vals,vecs,freq=projected_modes(H,x,masses)
    assert len(vals)==1 and abs(vals[0]-.1)<1e-12 and freq[0]>1000
    try:thermo_harmonic([-10.,100.],298.15)
    except ValueError:pass
    else:raise AssertionError('imaginary mode was hidden')
    from rdkit import Chem
    from rdkit.Chem import AllChem
    m=Chem.AddHs(Chem.MolFromSmiles('OCCO'));assert AllChem.EmbedMolecule(m,randomSeed=7)==0
    x=m.GetConformer().GetPositions();sym=[a.GetSymbol() for a in m.GetAtoms()]
    d=probe_directions('OCCO',sym,x)
    assert len(d)==4
    for _,v in d:
        assert abs(np.linalg.norm(v,axis=1).max()-1)<1e-12 and np.linalg.norm(v.sum(0))<1e-10
    return dict(diatomic_frequency_cm1=float(freq[0]),directions=len(d))


def jobs():
    from r6_jobs import execute
    with tempfile.TemporaryDirectory() as td:
        p=Path(td);code=[2,0,1]
        queue=[dict(id=f'j{i}',argv=[sys.executable,'-c',f'raise SystemExit({c})'],timeout_s=5,
                    lock=str(p/f'j{i}.lock')) for i,c in enumerate(code)]
        rc=execute(queue,p/'out',str(p),'portable-test')
        d=json.loads((p/'out/jobs.json').read_text())
        assert rc==2 and [r['status'] for r in d]==['censored','completed','failed']
        assert not list(p.glob('*.lock'))
        return dict(statuses=[r['status'] for r in d])


def headline():
    from r6_headline import render
    d={'tables':{}}
    for table in ('idac','vle','he'):
        d['tables'][table]={'pairwise':[dict(model='Z0x',arm='open630',common_rows=2,
            reference={'rows':2,'MAE':1.},candidate={'rows':2,'MAE':2.},delta_MAE_CI95=[.5,1.5])]}
    lle=dict(rows=2,systems=1,row_gap_found_bounds=[.5,1.],system_gap_found_bounds=[0.,1.],
             unresolved_rows=1,endpoint_rows=0,composition_MAE=None)
    d['tables']['lle']={'pairwise':[dict(model='Z0x',arm='open630',common_rows=2,reference=lle,candidate=lle)]}
    text=render(d);assert 'endpoint MAE None on 0' in text and 'false-positive rate' in text
    d['tables']['idac']['pairwise'][0]['candidate']['rows']=1
    try:render(d)
    except ValueError:pass
    else:raise AssertionError('different denominators accepted')
    return dict(mismatched_denominator_rejected=True)


def main():
    result={}
    for f in (endpoint,ensemble,modes,jobs,headline):result[f.__name__]=f()
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
