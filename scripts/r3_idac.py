"""Stored-prediction provenance, common-subset, and descriptive class/role audits.

Never edits predictions or model constants. Run where the stored CSVs exist.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import time
import numpy as np
import pandas as pd
from r3_common import (digest, keyed, select_split, system_ids, cluster_ci,
                       write_json, STALL_KEYS, WATER)

PRED='pred_ln_gamma_inf'

def chemical_class(smiles):
    from rdkit import Chem
    m=Chem.MolFromSmiles(smiles)
    if m is None: raise ValueError(f'invalid SMILES: {smiles}')
    atoms=[a.GetAtomicNum() for a in m.GetAtoms() if a.GetAtomicNum()!=1]
    if atoms==[8]: return 'water'
    tests=[('carboxylic_acid','[CX3](=O)[OX2H1]'),
           ('amide','[CX3](=O)[NX3]'),('ester','[CX3](=O)[OX2][#6]'),
           ('alcohol','[CX4][OX2H1]'),('phenol','[c][OX2H1]'),
           ('ether','[#6;!$(C=O)][OX2][#6;!$(C=O)]'),
           ('carbonyl','[CX3;!$(C(=O)[O,N])]=O'),
           ('amine','[NX3;!$(N-C=O)]'),('aromatic_N','[n]'),('nitrile','[C]#[N]')]
    tags=[name for name,smarts in tests if m.HasSubstructMatch(Chem.MolFromSmarts(smarts))]
    if len(tags)>1: return 'multifunctional'
    if tags: return tags[0]
    if set(atoms)<={6}: return 'aromatic_hydrocarbon' if any(a.GetIsAromatic() for a in m.GetAtoms()) else 'aliphatic_hydrocarbon'
    if any(z in (9,17,35) for z in atoms): return 'halogenated_other'
    if 16 in atoms: return 'sulfur_other'
    return 'other'

def summarize(df, total=None, bootstrap=True):
    if df.empty: return {'n_rows':0,'n_systems':0}
    er=df.ref.to_numpy(float)-df.ln_gamma_inf.to_numpy(float)
    ec=df.candidate.to_numpy(float)-df.ln_gamma_inf.to_numpy(float)
    dae=abs(ec)-abs(er); s=system_ids(df)
    n=len(df); total=n if total is None else total
    out=dict(n_rows=n,n_systems=int(len(np.unique(s))),
        mae_ref=float(abs(er).mean()),mae_candidate=float(abs(ec).mean()),
        bias_ref=float(er.mean()),bias_candidate=float(ec.mean()),
        delta_mae=float(dae.mean()),delta_prediction_mean=float((ec-er).mean()),
        contribution_to_total_delta_mae=float(dae.sum()/total))
    if bootstrap: out['delta_mae_CI95']=cluster_ci(dae,s)
    return out

def audit(a):
    start=time.perf_counter(); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    r0=pd.read_csv(a.reference); c0=pd.read_csv(a.candidate)
    r=keyed(r0); c=keyed(c0)
    pos_identity=(len(r)==len(c) and np.array_equal(r.index,c.index))
    r=select_split(r,a.split); c=select_split(c,a.split)
    ids=r.index.intersection(c.index,sort=False)
    aligned=r.loc[ids].copy(); aligned['ref']=r.loc[ids,PRED]; aligned['candidate']=c.loc[ids,PRED]
    finite=np.isfinite(aligned[['ref','candidate','ln_gamma_inf']].to_numpy(float)).all(1)
    common=aligned.loc[finite].copy()
    if common.empty: raise ValueError('no finite common observations')
    excluded=[]
    for key in r.index.difference(c.index): excluded.append((key,'missing_in_candidate'))
    for key in c.index.difference(r.index): excluded.append((key,'missing_in_reference'))
    for key in aligned.index[~finite]: excluded.append((key,'nonfinite_prediction_or_response'))
    pd.DataFrame(excluded,columns=['r3_row_id','reason']).to_csv(out/'excluded.csv',index=False)
    smi=pd.read_csv(a.compounds,usecols=['inchikey','smiles'])
    if smi.inchikey.duplicated().any(): raise ValueError('duplicate compound keys')
    classes={k:chemical_class(s) for k,s in zip(smi.inchikey,smi.smiles)}
    for role in ('solute','solvent'):
        common[role+'_class']=common[role].map(classes)
        if common[role+'_class'].isna().any(): raise ValueError(f'missing {role} class')
    common['water_role']=np.where(common.solute==WATER,'water_solute',
                         np.where(common.solvent==WATER,'water_solvent','no_water'))
    common['flagged']=common.solute.isin(STALL_KEYS)|common.solvent.isin(STALL_KEYS)
    common['delta_prediction']=common.candidate-common.ref
    common['delta_absolute_error']=(common.candidate-common.ln_gamma_inf).abs()-(common.ref-common.ln_gamma_inf).abs()
    common.to_csv(out/'paired_rows.csv',index=False)
    for group in ['solute_class','solvent_class','water_role','solute','solvent']:
        rows=[]
        for label,g in common.groupby(group,sort=True):
            row={group:label}; row.update(summarize(g,len(common),bootstrap=group.endswith('class') or group=='water_role')); rows.append(row)
        pd.DataFrame(rows).to_csv(out/f'by_{group}.csv',index=False)
    cross=[]
    for (s,v),g in common.groupby(['solute_class','solvent_class'],sort=True):
        x=dict(solute_class=s,solvent_class=v); x.update(summarize(g,len(common),False)); cross.append(x)
    pd.DataFrame(cross).to_csv(out/'class_by_role.csv',index=False)
    # Model masks are evaluated on the SAME reference observations, with identity joins.
    mask_rows=[]
    def masked(label,keep):
        if not keep.any(): mask_rows.append(dict(mask=label,n_rows=0)); return
        d=r.loc[keep]; e=d[PRED].to_numpy(float)-d.ln_gamma_inf.to_numpy(float)
        mask_rows.append(dict(mask=label,n_rows=len(d),n_systems=len(np.unique(system_ids(d))),
            reference_mae=float(abs(e).mean()),reference_bias=float(e.mean())))
    rf=np.isfinite(r[[PRED,'ln_gamma_inf']].to_numpy(float)).all(1)
    masked('reference_alone_finite',rf)
    jointly=rf.copy()
    for spec in a.mask:
        label,path=spec.split('=',1); f=select_split(keyed(pd.read_csv(path)),a.split)
        v=f[PRED].reindex(r.index).to_numpy(float)
        valid=rf & np.isfinite(v)
        masked('reference_and_'+label,valid); jointly &= np.isfinite(v)
    if a.mask: masked('reference_and_all_supplied_masks',jointly)
    in_common=r.index.isin(common.index)
    masked('reference_and_candidate_finite',rf&in_common)
    mask_no_stall=rf&in_common&~(r.solute.isin(STALL_KEYS)|r.solvent.isin(STALL_KEYS)).to_numpy()
    masked('common_without_flagged_chains',mask_no_stall)
    pd.DataFrame(mask_rows).to_csv(out/'denominators.csv',index=False)
    result=dict(reference_sha256=digest(a.reference),candidate_sha256=digest(a.candidate),
        mask_inputs=[dict(label=q.split('=',1)[0],path=str(Path(q.split('=',1)[1]).resolve()),sha256=digest(q.split('=',1)[1])) for q in a.mask],
        same_row_identity_and_order=bool(pos_identity),split=a.split,
        reference_split_rows=len(r),candidate_split_rows=len(c),identity_intersection=len(ids),
        rows_excluded=len(excluded),infinite_ref=int(np.isinf(r[PRED]).sum()),infinite_candidate=int(np.isinf(c[PRED]).sum()),
        common=summarize(common),without_flagged=summarize(common.loc[~common.flagged]),
        flagged=summarize(common.loc[common.flagged]),
        common_row_ids_sha256=__import__('hashlib').sha256('\n'.join(common.index).encode()).hexdigest(),
        wall_s=time.perf_counter()-start)
    write_json(out/'audit.json',result)
    if a.expect_points is not None and len(common)!=a.expect_points: raise AssertionError('common row count does not reproduce the cited scorecard')
    print(json.dumps(result,indent=2))

def inventory(a):
    rows=[]
    for p in sorted(Path(a.root).rglob('*__idac__*.csv')):
        d=pd.read_csv(p)
        if PRED not in d: continue
        rows.append(dict(path=str(p.resolve()),sha256=digest(p),rows=len(d),
            test_rows=int((d['split']!='train').sum()) if 'split' in d else None))
    cards=[]
    for p in sorted(Path(a.root).rglob('*scorecard*.json')):
        try:
            c=json.loads(p.read_text()); table=c.get('tables',{}).get('idac',{})
            if 'Z0x' in table: cards.append(dict(path=str(p.resolve()),sha256=digest(p),models=c.get('models'),split=c.get('split'),n_points=table.get('n_points'),Z0x=table['Z0x']))
        except (ValueError,TypeError): continue
    print(json.dumps(dict(predictions=rows,Z0x_scorecards=cards),indent=2))

def compare_fresh(a):
    r=keyed(pd.read_csv(a.reference)); c=keyed(pd.read_csv(a.candidate))
    if set(r.index)!=set(c.index): raise ValueError('fresh/stored identity coverage changed; audit inputs before a numerical comparison')
    x=r[PRED].to_numpy(float); y=c.loc[r.index,PRED].to_numpy(float)
    mask=np.isfinite(x)
    if not np.array_equal(mask,np.isfinite(y)): raise ValueError('fresh/stored finite coverage changed')
    if not mask.any(): raise ValueError('no finite comparisons')
    err=float(abs(x[mask]-y[mask]).max())
    result=dict(rows=len(x),finite=int(mask.sum()),max_delta_lngamma=err,
                reference_sha256=digest(a.reference),candidate_sha256=digest(a.candidate))
    write_json(a.out,result)
    if err>=a.tol: raise AssertionError(f'fresh/stored mismatch {err} >= {a.tol}')

def main():
    p=argparse.ArgumentParser(); s=p.add_subparsers(dest='cmd',required=True)
    q=s.add_parser('inventory'); q.add_argument('--root',default='results')
    q=s.add_parser('audit'); q.add_argument('--reference',required=True); q.add_argument('--candidate',required=True)
    q.add_argument('--compounds',default='data/benchmark/compounds.csv'); q.add_argument('--split',default='test',choices=['test','train','test_one','test_both','all'])
    q.add_argument('--mask',action='append',default=[],help='LABEL=prediction.csv; reproduce the historical model list')
    q.add_argument('--expect-points',type=int); q.add_argument('--out',required=True)
    q=s.add_parser('compare-fresh'); q.add_argument('--reference',required=True); q.add_argument('--candidate',required=True)
    q.add_argument('--out',required=True); q.add_argument('--tol',type=float,default=1e-3)
    a=p.parse_args(); globals()[a.cmd.replace('-','_')](a)
if __name__=='__main__': main()
