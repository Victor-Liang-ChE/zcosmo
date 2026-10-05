"""Glycol/polyol/ether inventory and diagnostic A,V,profile-shape factorial.

The eight corners are sensitivity probes, not deployable or selected models.
Every model evaluation uses a fresh worker and fixed dielectric/C6 input tables.
"""
from __future__ import annotations
import argparse
import itertools
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import numpy as np
import pandas as pd
from r3_common import digest,read_sigma,write_sigma,write_json,profile_descriptors,WATER
from r4_common import structure,geometry,contacts

CONTROL_SMILES={'O','CO','CCCCO','CCCCCCCCC'}


def inventory(a):
    os.environ.pop('ZC_SIGMA_OVERRIDE_DIR',None)
    from zcosmo.cosmosac import sigma_path,SIGMA_DIR
    if not SIGMA_DIR.is_dir(): raise FileNotFoundError('Run UD-backed inventory on the asset-bearing Mac')
    compounds=pd.read_csv(a.compounds)
    idac=pd.read_csv(a.idac)
    paired=pd.read_csv(a.paired_rows) if a.paired_rows else None
    gm=json.loads(Path(a.geometry_map).read_text()) if a.geometry_map else {}
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True);rows=[];geo=[]
    for r in compounds.itertuples():
        d=structure(r.smiles)
        selected=d['OH_count']>=2 or d['ether_count']>0 or r.smiles in CONTROL_SMILES
        if not selected: continue
        k=r.inchikey; op=Path(a.open_profiles)/f'{k}.sigma'; up=sigma_path(k)
        record=dict(key=k,smiles=r.smiles,**d,
            solute_rows=int((idac.solute==k).sum()),solvent_rows=int((idac.solvent==k).sum()))
        for tag,p in [('open',op),('UD',up)]:
            if p is None or not Path(p).is_file():
                record[tag+'_available']=False;continue
            record[tag+'_available']=True
            record.update({tag+'_'+f:v for f,v in profile_descriptors(p).items()})
        if paired is not None:
            for role in ('solute','solvent'):
                sub=paired[paired[role]==k]
                record[role+'_scored_rows']=len(sub)
                if len(sub):
                    er=sub['ref']-sub.ln_gamma_inf; ec=sub.candidate-sub.ln_gamma_inf
                    record[role+'_signed_delta_prediction']=float((ec-er).mean())
                    record[role+'_delta_MAE_contribution']=float((abs(ec)-abs(er)).sum()/len(paired))
        rows.append(record)
        gp=Path(gm[k]) if k in gm else Path(a.geometry_dir)/f'{k}.xyz.json'
        # Missing geometries are visible. They do not silently cause profile/score rows to disappear.
        for tag,p in [('open',gp),('UD',Path(a.ud_cosmo)/(up.stem+'.cosmo') if up else None)]:
            item=dict(key=k,source=tag,path=str(p) if p else None,available=p is not None and p.is_file())
            if item['available']:
                sym,x=geometry(p);item.update(sha256=digest(p),**contacts(sym,x))
                write_json(out/'geometries'/f'{k}.{tag}.json',dict(sym=sym,x=x.tolist(),
                    source=str(p.resolve()),source_sha256=digest(p)))
            geo.append(item)
    if not rows: raise ValueError('empty structural panel')
    d=pd.DataFrame(rows);d.to_csv(out/'inventory.csv',index=False)
    (out/'keys.txt').write_text('\n'.join(d.key)+'\n')
    write_json(out/'geometries.json',geo)
    write_json(out/'inputs.json',dict(compounds=digest(a.compounds),idac=digest(a.idac),
        paired_rows=digest(a.paired_rows) if a.paired_rows else None,
        open_profiles=str(Path(a.open_profiles).resolve()),selected=len(d),
        note='All structural strata selected before prediction inspection; missing assets are explicit.'))


def shapley_three(values):
    """Exact three-factor Shapley identity for arrays at all eight corners."""
    out=[]
    for j in range(3):
        total=np.zeros_like(np.asarray(values['000'],float))
        others=[i for i in range(3) if i!=j]
        for subset in itertools.chain.from_iterable(itertools.combinations(others,n) for n in range(3)):
            bits=['0']*3
            for i in subset: bits[i]='1'
            before=''.join(bits);bits[j]='1';after=''.join(bits)
            w=math.factorial(len(subset))*math.factorial(2-len(subset))/6
            total+=w*(values[after]-values[before])
        out.append(total)
    return np.asarray(out)


def worker(a):
    os.environ.pop('ZC_SIGMA_OVERRIDE_DIR',None)
    from zcosmo.cosmosac import sigma_path,SIGMA_DIR
    if not SIGMA_DIR.is_dir(): raise FileNotFoundError('UD profiles unavailable')
    rows=pd.read_csv(a.rows); pair=rows[['solute','solvent']].drop_duplicates()
    if len(pair)!=1: raise ValueError('one ordered pair per worker')
    solute,solvent=pair.iloc[0].tolist()
    if solute==solvent: raise ValueError('self pair is not a solvent substitution')
    op=Path(a.open_profiles)/f'{solvent}.sigma'; up=sigma_path(solvent)
    if up is None: raise FileNotFoundError(solvent)
    s,po,mo=read_sigma(op); _,pu,mu=read_sigma(up)
    Ao,Au=float(po.sum()),float(pu.sum())
    with tempfile.TemporaryDirectory(prefix='r4-factorial-') as td:
        b=Path(td); solutep=Path(a.open_profiles)/f'{solute}.sigma'
        if not solutep.is_file(): raise FileNotFoundError(solutep)
        (b/solutep.name).symlink_to(solutep.resolve())
        if a.corner=='UD': (b/f'{solvent}.sigma').symlink_to(Path(up).resolve())
        else:
            # Bit order is A, V, normalized 153-bin shape. Never change fitted constants.
            iA,iV,iP=map(int,a.corner)
            area=Au if iA else Ao; p=(pu/Au if iP else po/Ao)*area; meta=dict(mo)
            meta.update({'area [A^2]':area,'volume [A^3]':mu['volume [A^3]'] if iV else mo['volume [A^3]'],
                'r4_diagnostic':'AVP '+a.corner,'source':'counterfactual only, never adopted'})
            write_sigma(b/f'{solvent}.sigma',s,p,meta)
        os.environ['ZC_SIGMA_OVERRIDE_DIR']=td
        from zcosmo.models import make_model
        compounds=pd.read_csv(a.compounds);smi=dict(zip(compounds.inchikey,compounds.smiles))
        model=make_model('Z0x',[solute,solvent],[smi[solute],smi[solvent]])
        vals=[]
        for r in rows.itertuples():
            try: y=float(model.lngamma_inf(r.T,0));err=''
            except Exception as e: y=np.nan;err=repr(e)
            vals.append(dict(r3_row_id=r.r3_row_id,value=y,error=err))
        pd.DataFrame(vals).to_csv(a.out,index=False)
        write_json(str(a.out)+'.inputs.json',dict(open_solvent=digest(op),UD_solvent=digest(up),
            open_solute=digest(solutep),dielectric=digest('results/qc/dielectric.csv'),
            dispersion=digest('results/qc/dispersion.csv'),Z0=digest('results/z_params/Z0.json')))


def factorial(a):
    d=pd.read_csv(a.paired_rows)
    if 'r3_row_id' not in d or d.r3_row_id.duplicated().any(): raise ValueError('use unique paired_rows from P16')
    panel=set(Path(a.keys).read_text().split());d=d[d.solvent.isin(panel)].copy()
    if d.empty: raise ValueError('selected solvents have no rows in the frozen scored set')
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True);joined=[]
    corners=[''.join(c) for c in itertools.product('01',repeat=3)]
    for j,(_,g) in enumerate(d.groupby(['solute','solvent'],sort=True)):
        part=out/f'pair-{j:04d}';part.mkdir(exist_ok=True);rp=part/'rows.csv';g.to_csv(rp,index=False)
        f=g.set_index('r3_row_id').copy()
        for corner in corners+['UD']:
            dest=part/f'{corner}.csv'
            subprocess.run([sys.executable,str(Path(__file__).resolve()),'worker','--rows',str(rp),
                '--corner',corner,'--open-profiles',a.open_profiles,'--compounds',a.compounds,
                '--out',str(dest)],check=True)
            q=pd.read_csv(dest).set_index('r3_row_id')
            if not q.index.is_unique or set(q.index)!=set(f.index): raise ValueError('worker identity mismatch')
            f[corner]=q.loc[f.index,'value']
        valid=np.isfinite(f[corners+['UD']].to_numpy()).all(1);f['all_corners_finite']=valid
        if valid.any() and abs(f.loc[valid,'111']-f.loc[valid,'UD']).max()>1e-10:
            raise AssertionError('A,V,shape do not exhaust this Z0x solvent substitution')
        vals={c:f[c].to_numpy(float) for c in corners}
        phi=shapley_three(vals)
        for k,v in zip(('A','V','shape'),phi): f['delta_lngamma_'+k]=v
        if valid.any() and abs(phi.sum(0)[valid]-(vals['111']-vals['000'])[valid]).max()>1e-10:
            raise AssertionError('Shapley identity failed')
        joined.append(f)
    result=pd.concat(joined);result.to_csv(out/'factorial_rows.csv')
    write_json(out/'summary.json',dict(rows=len(result),finite_all=int(result.all_corners_finite.sum()),
        unavailable=result.index[~result.all_corners_finite].tolist(),
        direction='open solvent to UD A,V,shape; solute remains open; dielectric and C6 tables frozen',
        registration=a.registration,paired_rows_sha256=digest(a.paired_rows)))
    if not result.all_corners_finite.all(): raise SystemExit(2)


def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
    q=s.add_parser('inventory');q.add_argument('--paired-rows');q.add_argument('--idac',default='data/benchmark/idac.csv')
    q.add_argument('--geometry-dir',default='data/pyscf_sigma/profiles_v2');q.add_argument('--geometry-map')
    q.add_argument('--ud-cosmo',default='data/raw/nist/UD/cosmo')
    q=s.add_parser('factorial');q.add_argument('--paired-rows',required=True);q.add_argument('--keys',required=True)
    q.add_argument('--registration',required=True)
    q=s.add_parser('worker');q.add_argument('--rows',required=True)
    q.add_argument('--corner',required=True,choices=[''.join(c) for c in itertools.product('01',repeat=3)]+['UD'])
    for q in s.choices.values():
        q.add_argument('--open-profiles',required=True);q.add_argument('--out',required=True)
        q.add_argument('--compounds',default='data/benchmark/compounds.csv')
    a=p.parse_args();globals()[a.cmd](a)
if __name__=='__main__':main()
