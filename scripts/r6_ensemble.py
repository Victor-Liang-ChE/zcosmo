"""Conformer evidence audit and finite-state thermodynamic kernel.

Electronic energies alone never define populations here. A liquid-population
calculation requires nuclear and conductor-to-environment free energies; missing
terms are errors, never silently zero. No profile or score is deployed.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
from r3_common import read_sigma
from r6_common import BASE,sha,write,fresh,registration,boltzmann,profile_envelope


def inventory(a):
    out=fresh(a.out);registration(a.registration)
    manifests=sorted(Path(a.proposals).rglob('proposals.json'))
    if not manifests:raise ValueError('no frozen proposals')
    found={}
    for p in sorted(Path(a.artifacts).rglob('result.json')):
        r=json.loads(p.read_text());key=r.get('input_sha256')
        if key:found.setdefault(key,[]).append((p,r))
    rows=[]
    for p in manifests:
        m=json.loads(p.read_text())
        cases=[c for c in m.get('cases',[]) if c['probe']]
        if not cases:continue
        states=[];profiles=[];energies=[];sources=[]
        for c in cases:
            proposal=p.parent/c['path']
            if sha(proposal)!=c['sha256']:raise ValueError('frozen proposal changed')
            hits=found.get(c['sha256'],[])
            if len(hits)>1:raise ValueError('duplicate run for one frozen input: '+c['path'])
            if not hits:
                states.append(dict(proposal=c['path'],status='never_run'));continue
            f,r=hits[0];states.append(dict(proposal=c['path'],status=r['status'],result_sha256=sha(f)))
            if r['status']!='stationary_sample':continue
            profile=f.parent/(m['key']+'.sigma')
            if not profile.is_file():raise FileNotFoundError(profile)
            _,v,_=read_sigma(profile);profiles.append(v);energies.append(r['E_TZVP_Eh']*627.509474)
            sources.append(dict(profile=str(profile.resolve()),sha256=sha(profile),proposal=c['path']))
        row=dict(key=m['key'],manifest_sha256=sha(p),expected=len(cases),states=states,
                 complete=len(profiles)==len(cases),available_profiles=sources)
        if profiles:
            row['sampled_envelope']=profile_envelope(profiles)
            row['electronic_energy_range_kcal']=[float(min(energies)),float(max(energies))]
            row['population_status']='not computed: duplicate basins, degeneracy, nuclear entropy and environment transfer require an audit'
        rows.append(row)
    write(out/'inventory.json',dict(base=BASE,registration=a.registration,molecules=rows,
          adoption=False,reference='Conductor electronic energies of the available P26 samples only'))


def populations(a):
    d=json.loads(Path(a.input).read_text());registration(d['registration'])
    required=('basin','E_conductor_kcal','F_nuclear_kcal','mu_from_conductor_kcal','degeneracy')
    states=d['states']
    if not states or any(any(k not in s for k in required) for s in states):
        raise ValueError('All basin free-energy terms must be supplied explicitly')
    if len({s['basin'] for s in states})!=len(states):raise ValueError('duplicate basin, not degeneracy')
    if d.get('environment') not in ('conductor','fixed_environment'):
        raise ValueError('This kernel does not solve a self-consistent liquid environment')
    if not d.get('common_standard_state') or not d.get('thermal_protocol'):
        raise ValueError('Common energy reference and nuclear partition protocol are mandatory')
    g=np.array([s['E_conductor_kcal']+s['F_nuclear_kcal']+s['mu_from_conductor_kcal'] for s in states])
    if d['environment']=='conductor' and any(s['mu_from_conductor_kcal']!=0 for s in states):
        raise ValueError('Conductor reference must not include its solvation energy twice')
    w,f=boltzmann(g,float(d['T']),[s['degeneracy'] for s in states])
    report=dict(T=d['T'],environment=d['environment'],states=[s['basin'] for s in states],
                weights=w.tolist(),free_energy_kcal=f,adopted=False,input_sha256=sha(a.input),
                note='For a liquid, environment potentials must be derivatives of a single specified free-energy functional.')
    if all('profile' in s for s in states):
        ps=[read_sigma(s['profile'])[1] for s in states]
        report['sampled_envelope']=profile_envelope(ps)
        report['average_psigmaA']=np.einsum('k,kij->ij',w,np.asarray(ps)).tolist()
        report['warning']='Average profile is a moment approximation; its gamma is not the log partition-function chemical potential.'
    write(a.out,report)



def rotor_free_energy(x_A,masses,T,symmetry_number):
    """Classical rigid-rotor contribution for the specified isolated isotropic reference.

    Translational standard-state terms cancel within one molecular formula.
    Symmetry is an input audited from molecular symmetry, never embedding count.
    """
    from scipy.constants import h,k,pi,physical_constants
    x=np.asarray(x_A,float);m=np.asarray(masses,float)
    if int(symmetry_number)!=symmetry_number or symmetry_number<1:raise ValueError('positive integer rotational symmetry number required')
    x=x-np.average(x,axis=0,weights=m)
    I=sum(w*(np.dot(r,r)*np.eye(3)-np.outer(r,r)) for w,r in zip(m,x))
    vals=np.linalg.eigvalsh(I)*physical_constants['atomic mass constant'][0]*1e-20
    factor=8*pi*pi*k*T/(h*h)
    if vals[-1]<=0:raise ValueError('atomic species has no molecular rotor partition')
    if vals[0]<1e-10*vals[-1]:q=factor*np.sqrt(vals[1]*vals[2])/symmetry_number
    else:q=np.sqrt(pi)*factor**1.5*np.sqrt(np.prod(vals))/symmetry_number
    return float(-.00198720425864083*T*np.log(q))


def conductor(a):
    """Build a reference-only thermal ensemble from a complete, audited basin catalog.

    Does not turn reference weights into liquid weights or publish an activity coefficient.
    """
    from r6_referee import thermo_harmonic
    catalog=json.loads(Path(a.catalog).read_text());registration(catalog['registration'])
    entries=catalog['basins'];out=fresh(a.out)
    if not entries or len({r['id'] for r in entries})!=len(entries):raise ValueError('distinct audited basins required')
    if not catalog.get('basin_and_symmetry_audit'):raise ValueError('explicit basin/symmetry audit identifier required')
    states=[];key=None;formula=None
    for r in entries:
        folder=Path(r['referee']);report=json.loads((folder/'status.json').read_text())
        if sha(folder/'status.json')!=r['status_sha256']:raise ValueError('referee result changed')
        if report['status']!='diagnostic_complete' or not report['force_gate'] or not report['thermal_gate']:
            raise ValueError('all basin stationarity/thermal checks must pass')
        if key is None:key=report['key']
        if report['key']!=key:raise ValueError('one molecular species per conformer catalog')
        if sha(folder/'local.npz')!=report['local_data_sha256'] or sha(folder/'center.sigma')!=report['center_profile_sha256']:
            raise ValueError('native mode or profile data changed')
        data=np.load(folder/'local.npz',allow_pickle=False)
        atoms=tuple(sorted(data['sym'].tolist()))
        if formula is None:formula=atoms
        if atoms!=formula:raise ValueError('conformer stoichiometry changed')
        states.append((r,report,data,read_sigma(folder/'center.sigma')))
    import pandas as pd
    eps=pd.read_csv('results/qc/dielectric.csv').set_index('inchikey').loc[key,'eps']
    quantum=pd.read_csv('results/qc/dispersion.csv').set_index('inchikey').loc[key]
    results=[]
    for T in (250.,298.15,400.):
        G=[];d=[];ps=[];vol=[];microstates=[]
        for r,rep,dat,(_,p,meta) in states:
            freq=rep['frequencies_cm1'][0]
            internal=thermo_harmonic(freq,T)+rotor_free_energy(dat['x'],dat['masses'],T,r['rotational_symmetry_number'])
            electronic=rep['center_E_TZVP_Eh']*627.509474
            G.append(electronic+internal);d.append(r['degeneracy']);ps.append(p);vol.append(meta['volume [A^3]'])
            profile=Path(r['referee'])/'center.sigma'
            microstates.append(dict(id=r['id'],molecule=key,E_conductor_kcal=electronic,F_nuclear_kcal=internal,
                degeneracy=r['degeneracy'],eps=float(eps),C6_au=float(quantum.C6_au),alpha_au=float(quantum.alpha_au),
                profile=str(profile.resolve()),profile_sha256=sha(profile)))
        w,f=boltzmann(G,T,d);mean=np.einsum('k,kij->ij',w,np.array(ps))
        write(out/f'catalog_{T:g}.json',dict(T=T,states=microstates,registration=catalog['registration'],
            thermal_protocol='R6 conductor harmonic plus classical rigid rotor',basin_and_symmetry_audit=catalog['basin_and_symmetry_audit'],
            dielectric_sha256=sha('results/qc/dielectric.csv'),dispersion_sha256=sha('results/qc/dispersion.csv')))
        results.append(dict(T=T,weights=w.tolist(),free_energy_kcal=f,mean_psigmaA=mean.tolist(),mean_volume_A3=float(w@vol),
            delta_G_kcal=(np.array(G)-min(G)).tolist()))
    write(out/'reference_ensemble.json',dict(key=key,basins=[r['id'] for r in entries],results=results,
        catalog_sha256=sha(a.catalog),adopted=False,
        scope='Finite listed-basin conductor reference, harmonic plus classical rigid rotor. No liquid transfer, no completeness certificate.'))

def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
    q=s.add_parser('inventory');q.add_argument('--proposals',default='cloud/r5/proposals');q.add_argument('--artifacts',required=True)
    q.add_argument('--out',required=True);q.add_argument('--registration',required=True)
    q=s.add_parser('populations');q.add_argument('--input',required=True);q.add_argument('--out',required=True)
    q=s.add_parser('conductor');q.add_argument('--catalog',required=True);q.add_argument('--out',required=True)
    a=p.parse_args();globals()[a.cmd](a)
if __name__=='__main__':main()
