"""Prospective A finite-basin extension of Z0x, for computational probes only.

Conductor energies plus nuclear free energies define intrinsic basin offsets.
Pure-conformer contact and London terms supply explicit hypothetical pure-liquid
standards. Equilibrate conformers before subtracting the pure chemical standard.
No measured property is an input. A finite multistart solve is not a global certificate.
"""
from __future__ import annotations
import argparse
import itertools
import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from scipy.special import softmax,logsumexp
from r6_common import sha,write,registration


class PhaseModel:
    def __init__(self,states,T,prm,c0):
        from zcosmo.cosmosac import R_KCAL,HARTREE_KCAL,BOHR_A,solve_gamma,delta_w
        if not 250<=T<=400:raise ValueError('R6 probe temperatures are restricted to 250..400 K')
        self.T=float(round(T,6));self.RT=R_KCAL*self.T;self.prm=prm;self.c0=float(c0)
        self.states=states;self.labels=list(dict.fromkeys(s['molecule'] for s in states))
        if len(self.labels)>2 or not self.labels:raise ValueError('one or two chemical species per R6 probe')
        self.groups=[np.array([j for j,s in enumerate(states) if s['molecule']==name],int) for name in self.labels]
        if any(len(g)>4 for g in self.groups):raise ValueError('at most four audited basins per species in this pilot')
        self.fl=[s['fluid'] for s in states];self.pa=np.array([f.psigA.ravel() for f in self.fl]);self.A=self.pa.sum(1);self.V=np.array([f.V for f in self.fl])
        self.eps=np.array([s['eps'] for s in states],float)
        C=np.array([s['C6_au'] for s in states]);alpha=np.array([s['alpha_au'] for s in states])
        if np.any(C<=0) or np.any(alpha<=0) or np.any(self.eps<1) or np.any(self.V<=0):raise ValueError('invalid pure input table')
        for g in self.groups:
            if not np.all(self.eps[g]==self.eps[g[0]]):raise ValueError('conformers retain the same frozen chemical permittivity')
            if not np.all(C[g]==C[g[0]]) or not np.all(alpha[g]==alpha[g[0]]):raise ValueError('conformers retain the same frozen chemical D4 data')
        d=2*(3*self.V/(4*np.pi))**(1/3)/BOHR_A
        cij=2*C[:,None]*C[None,:]/((alpha[None,:]/alpha[:,None])*C[:,None]+(alpha[:,None]/alpha[None,:])*C[None,:])
        self.e=-cij/((d[:,None]+d[None,:])/2)**6*HARTREE_KCAL
        self.w=2*self.e-np.diag(self.e)[:,None]-np.diag(self.e)[None,:]
        self.L=prm.w_dsp*prm.z/(2*self.RT)
        energy=np.array([s['E_conductor_kcal']+s['F_nuclear_kcal'] for s in states],float)
        deg=np.array([s['degeneracy'] for s in states],float)
        if not np.isfinite(energy).all() or np.any(deg<=0) or not np.isfinite(deg).all():raise ValueError('invalid basin free energies or multiplicity')
        # Separate energy gauges per chemical species cancel from every activity coefficient.
        for g in self.groups:energy[g]-=energy[g].min()
        self.g0=energy/self.RT-np.log(deg)
        for a,f in enumerate(self.fl):
            c=self.c0*(self.eps[a]-1)/(self.eps[a]+.5)
            E=np.exp(-delta_w(self.T,prm.with_(A_ES=c))/self.RT)
            y=np.log(solve_gamma(E,self.pa[a]/self.A[a]))
            self.g0[a]+=self.pa[a]@y/prm.aeff+self.L*self.e[a,a]

    def excess(self,x):
        from zcosmo.cosmosac import Mixture,solve_gamma,_pure_lnG,SIG
        x=np.asarray(x,float)
        if x.shape!=(len(self.fl),) or np.any(x<0) or abs(x.sum()-1)>1e-10:raise ValueError('invalid microstate fractions')
        V=x@self.V;eps=(x*self.V)@self.eps/V;c=self.c0*(eps-1)/(eps+.5)
        prm=self.prm.with_(A_ES=c,disp_mode='none');mix=Mixture(None,prm,fluids=self.fl)
        p=(x@self.pa)/(x@self.A);E=mix._E(self.T);ym=np.log(solve_gamma(E,p))
        yp=np.array([_pure_lnG(f.key,self.T,prm,self.pa[j].tobytes()) for j,f in enumerate(self.fl)])
        res=np.sum(self.pa*(ym-yp),axis=1)/prm.aeff
        sig=np.tile(SIG,3);ED=E*(sig[:,None]+sig[None,:])**2
        z=p*np.exp(ym);zp=self.pa/self.A[:,None]*np.exp(yp)
        gc=((x@self.A)*(z@ED@z)-(x*self.A)@np.einsum('ki,ij,kj->k',zp,ED,zp))/(2*self.RT*prm.aeff)
        dc=self.c0*1.5*self.V*(self.eps-eps)/(V*(eps+.5)**2)
        gdisp=.5*self.L*(x@self.w@x);mudisp=self.L*(self.w@x)-gdisp
        mu=mix.lngamma_comb(x)+res+gc*dc+mudisp
        return mu,float(x@mu)

    def free(self,x):
        mu,ge=self.excess(x);positive=x>0
        return float(x@self.g0+np.sum(x[positive]*np.log(x[positive]))+ge)

    def equilibrium(self,chemical_x,budget=2000):
        X=np.asarray(chemical_x,float)
        if X.shape!=(len(self.groups),) or (X<0).any() or abs(X.sum()-1)>1e-12:raise ValueError('invalid chemical composition')
        active=[(g,v) for g,v in zip(self.groups,X) if v>0]
        size=sum(len(g)-1 for g,v in active);calls=0
        def unpack(t):
            x=np.zeros(len(self.fl));pos=0
            for g,v in active:
                w=softmax(np.r_[t[pos:pos+len(g)-1],0.]);pos+=len(g)-1;x[g]=v*w
            return x
        if size==0:
            x=unpack(np.empty(0));return dict(x=x,free_energy_RT=self.free(x),model_calls=1,stationary=True,globally_certified=False)
        starts=[np.zeros(size)]
        for chosen in itertools.product(*(range(len(g)) for g,v in active)):
            t=[]
            for (g,v),j in zip(active,chosen):
                a=np.zeros(len(g));a[j]=4.;t.extend((a-a[-1])[:-1])
            starts.append(np.asarray(t))
        records=[]
        def objective(t):
            nonlocal calls
            calls+=1
            if calls>budget:raise RuntimeError('fixed equilibrium model-call budget exhausted')
            x=unpack(t);ex,ge=self.excess(x);positive=x>0
            f=float(x@self.g0+np.sum(x[positive]*np.log(x[positive]))+ge)
            grad=[]
            for g,v in active:
                w=x[g]/v;mu=self.g0[g]+np.log(x[g])+ex[g]
                grad.extend((v*w*(mu-w@mu))[:-1])
            return f,np.asarray(grad)
        for t in starts:
            ans=minimize(objective,t,jac=True,method='L-BFGS-B',bounds=[(-80.,80.)]*size,
                         options={'ftol':1e-13,'gtol':1e-10,'maxiter':150,'maxls':30})
            x=unpack(ans.x);ex,_=self.excess(x);error=0.
            for g,v in active:error=max(error,float(abs(x[g]/v-softmax(-self.g0[g]-ex[g])).max()))
            records.append(dict(x=x,F=self.free(x),fixed_point_error=error,optimizer_success=bool(ans.success)))
        good=[r for r in records if r['fixed_point_error']<1e-8]
        if len(good)!=len(records):raise RuntimeError('one or more fixed multistarts failed the stationarity check')
        best=min(good,key=lambda r:r['F'])
        return dict(x=best['x'],free_energy_RT=best['F'],model_calls=calls,stationary=True,
                    stationary_free_energy_spread=max(r['F'] for r in good)-best['F'],globally_certified=False)

    def idac(self,solute,solvent):
        if solute==solvent or len(self.groups)!=2:raise ValueError('two distinct chemical species required')
        i=self.labels.index(solute);j=self.labels.index(solvent)
        xi=np.eye(2)[i];xj=np.eye(2)[j]
        ri=self.equilibrium(xi);rj=self.equilibrium(xj)
        ex,_=self.excess(rj['x']);group=self.groups[i]
        insertion=self.g0[group]+ex[group]
        value=-logsumexp(-insertion)-ri['free_energy_RT']
        return dict(ln_gamma_inf=float(value),solute_trace_populations=softmax(-insertion).tolist(),
            solute_pure_populations=ri['x'][group].tolist(),solvent_populations=rj['x'][self.groups[j]].tolist(),
            pure_solute_model_calls=ri['model_calls'],pure_solvent_model_calls=rj['model_calls'],
            globally_certified=False,adopted=False)


def main():
    p=argparse.ArgumentParser();p.add_argument('--catalog',required=True);p.add_argument('--solute',required=True);p.add_argument('--solvent',required=True);p.add_argument('--out',required=True)
    a=p.parse_args()
    from zcosmo.cosmosac import Fluid
    from zcosmo.models import load_z_params
    from zcosmo.zmodel import c_es_theory
    from r3_common import read_sigma
    d=json.loads(Path(a.catalog).read_text());registration(d['registration'])
    if float(d['T']) not in (250.,298.15,400.):raise ValueError('R6 catalog temperature outside the fixed panel')
    if not d.get('thermal_protocol') or not d.get('basin_and_symmetry_audit'):raise ValueError('thermal/reference and basin/symmetry provenance required')
    import pandas as pd
    eps_table=pd.read_csv('results/qc/dielectric.csv').set_index('inchikey')
    d4_table=pd.read_csv('results/qc/dispersion.csv').set_index('inchikey')
    states=[];inputs={p:sha(p) for p in ('results/qc/dielectric.csv','results/qc/dispersion.csv','results/z_params/Z0.json')}
    for s in d['states']:
        for k in ('id','molecule','E_conductor_kcal','F_nuclear_kcal','degeneracy','eps','C6_au','alpha_au','profile','profile_sha256'):
            if k not in s:raise ValueError('missing basin input: '+k)
        key=s['molecule']
        if s['eps']!=float(eps_table.loc[key,'eps']) or s['C6_au']!=float(d4_table.loc[key,'C6_au']) or s['alpha_au']!=float(d4_table.loc[key,'alpha_au']):
            raise ValueError('Frozen dielectric/D4 input changed')
        if sha(s['profile'])!=s['profile_sha256']:raise ValueError('basin profile changed')
        _,ps,m=read_sigma(s['profile']);r=dict(s);r['fluid']=Fluid(s['molecule']+':'+s['id'],ps,float(ps.sum()),m['volume [A^3]'],m.get('disp. flag','NHB'),None,m)
        states.append(r);inputs[s['profile']]=s['profile_sha256']
    if len({(s['molecule'],s['id']) for s in states})!=len(states):raise ValueError('duplicate basin ID')
    model=PhaseModel(states,float(d['T']),load_z_params('Z0'),c_es_theory(fpol=1.))
    answer=model.idac(a.solute,a.solvent);answer.update(T=d['T'],registration=d['registration'],catalog_sha256=sha(a.catalog),profile_inputs=inputs,
        scope='New A finite-basin Z0x extension with explicit pure-conformer standards; theoretical probe only, not a registered score.')
    from r6_common import check_inputs
    check_inputs(inputs)
    write(a.out,answer);print(json.dumps(answer,indent=2))
if __name__=='__main__':main()
