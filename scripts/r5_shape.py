"""Fixed structural panel, crossed quantum settings, and stage-resolved sigma profiles.

No UD geometry is invented. No profile recipe is selected by experimental error.
The point-patch limit is an A diagnostic of Hsieh averaging, never a default.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import os
import time
import numpy as np
import pandas as pd
from r3_common import digest, read_sigma, write_sigma, write_json, profile_descriptors
from r4_common import geometry, structure, contacts, parser_trace, selected_profiles
from r5_common import (BASE,PANEL,fresh,canonical_smiles,charge_average,bin_linear,
                       require_registration,check_fingerprint)


def plan(a):
    from rdkit import Chem, rdBase
    compounds=pd.read_csv(a.compounds)
    if compounds.inchikey.duplicated().any(): raise ValueError('duplicate compound keys')
    by={}
    for r in compounds.itertuples(): by.setdefault(canonical_smiles(r.smiles),[]).append(r)
    panel=[]
    for name,s in PANEL:
        match=by.get(canonical_smiles(s),[])
        if len(match)>1:
            expected=Chem.MolToInchiKey(Chem.MolFromSmiles(s))
            match=[r for r in match if r.inchikey==expected]
        if len(match)!=1: raise ValueError(f'{name}: expected one exact stereo-aware SMILES match, got {len(match)}')
        r=match[0];panel.append(dict(name=name,key=r.inchikey,smiles=r.smiles,**structure(r.smiles)))
    historical=set(pd.read_csv('results/pyscf_profile_validation.csv',usecols=['key']).key)
    excluded=historical|{r['key'] for r in panel};eligible=[]
    import hashlib
    for r in compounds.itertuples():
        st=structure(r.smiles);m=Chem.MolFromSmiles(r.smiles)
        if r.inchikey in excluded or st['heavy_atoms']>13 or st['rotatable_bonds']<2: continue
        if (len(Chem.GetMolFrags(m))!=1 or any(x.GetAtomicNum() not in (1,6,8) or
             x.GetFormalCharge()!=0 or x.GetNumRadicalElectrons()!=0 for x in m.GetAtoms())): continue
        if st['OH_count']<2 and st['ether_count']<1: continue
        eligible.append(dict(name=r.inchikey,key=r.inchikey,smiles=r.smiles,**st,
            order=hashlib.sha256(('R5-validation-v1|'+r.inchikey).encode()).hexdigest()))
    eligible.sort(key=lambda r:r['order'])
    if len(eligible)<8: raise ValueError('fewer than eight separate validation members; no substitution rule is authorized')
    validation=eligible[:8];gm=json.loads(Path(a.geometry_map).read_text()) if a.geometry_map else {}
    out=fresh(a.out)
    for r in panel+validation:
        k=r['key'];p=Path(gm[k]) if k in gm else Path(a.geometry_dir)/(k+'.xyz.json')
        if not p.is_file():
            alt=Path('cloud/r4/native')/(k+'.open.json')
            if alt.is_file(): p=alt
            else: raise FileNotFoundError(f'{k}: provide the saved generating geometry; no re-embedding fallback')
        sym,x=geometry(p);m=Chem.AddHs(Chem.MolFromSmiles(r['smiles']))
        if sym!=[at.GetSymbol() for at in m.GetAtoms()]: raise ValueError(f'{k}: atom order differs')
        dest=out/'geometries'/(k+'.json')
        write_json(dest,dict(sym=sym,x=x.tolist()))
        r.update(geometry=str(dest.relative_to(out)),geometry_sha256=digest(dest),source_geometry=str(p.resolve()),
                 source_sha256=digest(p),spin=0)
    manifest=dict(base=BASE,registration=require_registration(a.registration),panel=panel,validation=validation,
        selection='fixed homologues/branched/rigid controls; validation first 8 SHA-ordered eligible structures, excluding panel and historical 25',
        compounds=str(Path(a.compounds)),compounds_sha256=digest(a.compounds),rdkit=rdBase.rdkitVersion)
    write_json(out/'manifest.json',manifest)
    print(json.dumps({'panel_keys':[r['key'] for r in panel],'validation_keys':[r['key'] for r in validation]},indent=2))


def process(sym,x,seg,out,key,registration):
    from zcosmo.pyscf_cosmo import BOHR
    p,reference,trace=parser_trace(sym,x,seg)
    arr=lambda o:np.stack([o.psigmaA_nhb,o.psigmaA_OH,o.psigmaA_OT])
    original=arr(reference);grid=reference.sigmas;area=seg['area'];raw=seg['q']/area
    independent=charge_average(seg['xyz']*BOHR,area,raw,1.)
    discrepancy=float(abs(independent-p.sigma_averaged).max())
    if discrepancy>1e-10: raise AssertionError('independent Hsieh formula failed parity')
    base_total=bin_linear(p.sigma_averaged,area,grid)
    if abs(original.sum(0)-base_total).max()>1e-8: raise AssertionError('HB split changed total bin distribution')
    report={'key':key,'registration':registration,'native_trace':trace,'geometry_contacts':contacts(sym,x),
            'Hsieh_parity_e_A2':discrepancy,'raw_abs_tail_A2':float(area[abs(raw)>=.01].sum()),
            'raw_second_moment':float(area@(raw*raw)/area.sum()),'variants':{}}
    for label,m in [('hsieh',1.),('coincident4',4.),('point_limit',np.inf)]:
        avg=charge_average(seg['xyz']*BOHR,area,raw,m)
        p.sigma_averaged=avg
        p.sigma_nhb,p.sigma_OH,p.sigma_OT=p.split_profiles(avg,3)
        z=p.get_outputs();ps=arr(z);total=bin_linear(avg,area,z.sigmas)
        if abs(ps.sum(0)-total).max()>1e-8: raise AssertionError('binwise conservation failure')
        meta=dict(z.meta);meta.update(source='R5 stage diagnostic, not adopted',r5_recipe=label,
            r5_registration=registration,geometry_converged='R5-frozen')
        ek=meta.get('disp. e/kB [K]')
        if ek is not None and not np.isfinite(ek): meta['disp. e/kB [K]']=None
        path=out/label/(key+'.sigma');write_sigma(path,z.sigmas,ps,meta)
        pre=np.array([bin_linear(v[:,0],v[:,1],grid) for v in (p.sigma_nhb,p.sigma_OH,p.sigma_OT)])
        np.savez_compressed(out/(label+'.stages.npz'),sigma=grid,total=total,pre_HB=pre,post_HB=ps,
             averaged_sigma=avg,area=area,raw_sigma=raw,owner=seg['atom'])
        report['variants'][label]=dict(**profile_descriptors(path),
             averaging_moment_e=float(area@avg),pre_HB_A2=pre.sum(1).tolist())
    write_json(out/'stages.json',report)
    return report


def post(a):
    with np.load(a.segments,allow_pickle=False) as d:
        sym=d['sym'].tolist();x=d['x'];seg={k:d[k] for k in ('xyz','q','area','atom')}
    out=fresh(a.out);process(sym,x,seg,out,a.key,require_registration(a.registration))
    write_json(out/'inputs.json',dict(segments=str(Path(a.segments).resolve()),sha256=digest(a.segments)))


def native(a):
    from importlib.metadata import version
    if version('pyscf')!='2.14.0': raise RuntimeError('requires pinned pyscf==2.14.0')
    from r4_charge import factory,segments
    sym,x=geometry(a.geometry);out=fresh(a.out);t=time.perf_counter()
    basis='def2-svp' if a.method=='svp_swig' else 'def2-tzvp'
    mf=factory(sym,x,a.spin,basis,a.memory)
    method='ISWIG' if a.method=='tz_iswig' else 'SWIG'
    if not hasattr(mf.with_solvent,'surface_discretization_method'): raise RuntimeError('required PCM API unavailable')
    mf.with_solvent.surface_discretization_method=method
    e=mf.kernel()
    if not mf.converged or not np.isfinite(e): raise RuntimeError('unconverged native SCF')
    seg,_=segments(mf.with_solvent)
    np.savez_compressed(out/(a.key+'.segments.npz'),sym=np.array(sym),x=x,**seg)
    process(sym,x,seg,out,a.key,require_registration(a.registration))
    aux=getattr(mf.with_df,'auxmol',None)
    write_json(out/'native.json',dict(key=a.key,method=a.method,geometry=str(Path(a.geometry).resolve()),
        geometry_sha256=digest(a.geometry),energy_Eh=float(e),SCF_converged=True,
        basis=basis,XC='b88,p86',grid_level=3,lebedev_order=29,eps=1e9,surface_discretization=method,
        auxiliary_basis=str(getattr(aux,'basis',getattr(mf.with_df,'auxbasis',None))),
        wall_s=time.perf_counter()-t,registration=a.registration,pyscf=version('pyscf')))


def descriptors(a):
    m=json.loads(Path(a.manifest).read_text());os.environ.pop('ZC_SIGMA_OVERRIDE_DIR',None)
    from zcosmo.cosmosac import sigma_path
    rows=[]
    for r in m['panel']+m['validation']:
        for source,path in [('open',Path(a.open_profiles)/(r['key']+'.sigma')),('UD',sigma_path(r['key']))]:
            if path is None or not Path(path).is_file(): raise FileNotFoundError(f"{source}: {r['key']}")
            s,p,meta=read_sigma(path);tot=p.sum(0);occ=tot>0
            rows.append(dict(key=r['key'],name=r['name'],source=source,**profile_descriptors(path),
                normalized_total= (tot/tot.sum()).tolist(),OH_fraction=np.divide(p[1],tot,out=np.zeros_like(tot),where=occ).tolist(),
                OT_fraction=np.divide(p[2],tot,out=np.zeros_like(tot),where=occ).tolist(),occupied_bins=occ.tolist()))
    write_json(a.out,dict(manifest_sha256=digest(a.manifest),profiles=rows,
        note='Conditional HB fractions at unoccupied bins are undefined, encoded as zero plus an explicit occupancy mask.'))



def collect(a):
    """Compare stage outputs with stored UD bins, never experimental response values."""
    os.environ.pop('ZC_SIGMA_OVERRIDE_DIR',None)
    from zcosmo.cosmosac import sigma_path,SIGMA_DIR
    if not SIGMA_DIR.is_dir(): raise FileNotFoundError('UD-backed collection runs on the Mac')
    records=[]
    for path in sorted(Path(a.results).rglob('stages.json')):
        d=json.loads(path.read_text());key=d['key'];ud=sigma_path(key)
        if ud is None: raise FileNotFoundError(key)
        _,u,_=read_sigma(ud);un=u/u.sum()
        for label in ('hsieh','coincident4','point_limit'):
            pth=path.parent/label/(key+'.sigma');sig,p,meta=read_sigma(pth);pn=p/p.sum()
            desc=profile_descriptors(pth)
            records.append(dict(key=key,case=str(path.parent),recipe=label,UD_sha256=digest(ud),
                 normalized_153_L1=float(abs(pn-un).sum()),
                 normalized_total_L1=float(abs(pn.sum(0)-un.sum(0)).sum()),
                 raw_second_moment=d['raw_second_moment'],raw_abs_tail_A2=d['raw_abs_tail_A2'],
                 **{k:v for k,v in desc.items() if not isinstance(v,(dict,list))}))
    if not records:raise ValueError('no completed stage diagnostics')
    pd.DataFrame(records).to_csv(a.out,index=False)


def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
    q=s.add_parser('plan');q.add_argument('--compounds',default='data/benchmark/compounds.csv')
    q.add_argument('--geometry-dir',default='data/pyscf_sigma/profiles_v2');q.add_argument('--geometry-map')
    q.add_argument('--out',required=True);q.add_argument('--registration',required=True)
    q=s.add_parser('post');q.add_argument('--segments',required=True);q.add_argument('--key',required=True)
    q.add_argument('--out',required=True);q.add_argument('--registration',required=True)
    q=s.add_parser('native');q.add_argument('--geometry',required=True);q.add_argument('--key',required=True)
    q.add_argument('--method',choices=['tz_swig','svp_swig','tz_iswig'],required=True)
    q.add_argument('--spin',type=int,default=0);q.add_argument('--memory',type=int,default=4000)
    q.add_argument('--out',required=True);q.add_argument('--registration',required=True)
    q=s.add_parser('descriptors');q.add_argument('--manifest',required=True);q.add_argument('--open-profiles',required=True);q.add_argument('--out',required=True)
    q=s.add_parser('collect');q.add_argument('--results',required=True);q.add_argument('--out',required=True)
    a=p.parse_args();globals()[a.cmd](a)
if __name__=='__main__':main()
