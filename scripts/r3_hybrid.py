"""Diagnostic four-corner substitution: UD/open solute x UD/open solvent.

One fresh worker per ordered pair and corner. No altered profile, fitted parameter,
or production output. Prediction and absolute-error Shapley attributions both sum exactly.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import numpy as np
import pandas as pd
from r3_common import keyed, digest, write_json

def worker(a):
    os.environ.pop('ZC_SIGMA_OVERRIDE_DIR',None)
    from zcosmo.cosmosac import sigma_path
    rows=pd.read_csv(a.rows); pairs=rows[['solute','solvent']].drop_duplicates()
    if len(pairs)!=1: raise ValueError('worker must have exactly one ordered pair')
    solute,solvent=pairs.iloc[0].tolist()
    if solute==solvent: raise ValueError('a self-pair does not define two independent profile substitutions')
    used={}
    with tempfile.TemporaryDirectory(prefix='r3-hybrid-') as td:
        for key,kind in zip((solute,solvent),a.corner):
            p=Path(a.open_profiles)/f'{key}.sigma' if kind=='o' else sigma_path(key)
            if p is None or not Path(p).is_file(): raise FileNotFoundError(str(p))
            p=Path(p).resolve(); (Path(td)/f'{key}.sigma').symlink_to(p)
            used[key]=dict(source=kind,path=str(p),sha256=digest(p))
        os.environ['ZC_SIGMA_OVERRIDE_DIR']=td
        from zcosmo.models import make_model
        compounds=pd.read_csv(a.compounds); smi=dict(zip(compounds.inchikey,compounds.smiles))
        m=make_model(a.model,[solute,solvent],[smi[solute],smi[solvent]])
        records=[]
        for r in rows.itertuples():
            try: value=float(m.lngamma_inf(r.T,0)); error=''
            except Exception as ex: value=np.nan; error=type(ex).__name__+': '+str(ex)[:200]
            records.append(dict(r3_row_id=r.r3_row_id,value=value,error=error))
        pd.DataFrame(records).to_csv(a.out,index=False); write_json(str(a.out)+'.inputs.json',used)

def run(a):
    d=pd.read_csv(a.paired_rows)
    if 'r3_row_id' not in d or d.r3_row_id.duplicated().any(): raise ValueError('use audit/paired_rows.csv with unique row IDs')
    out=Path(a.out); out.mkdir(parents=True,exist_ok=True); joined=[]
    for j,(_,g) in enumerate(d.groupby(['solute','solvent'],sort=True)):
        part=out/f'pair-{j:04d}'; part.mkdir(exist_ok=True)
        rows=part/'rows.csv'; g.to_csv(rows,index=False); frame=g.set_index('r3_row_id').copy()
        for corner in ('uu','ou','uo','oo'):
            target=part/f'{corner}.csv'
            subprocess.run([sys.executable,str(Path(__file__).resolve()),'worker','--rows',str(rows),
                '--open-profiles',a.open_profiles,'--corner',corner,'--model',a.model,
                '--compounds',a.compounds,'--out',str(target)],check=True)
            value=pd.read_csv(target).set_index('r3_row_id')
            frame[corner]=value.loc[frame.index,'value']
        joined.append(frame)
    d=pd.concat(joined); valid=np.isfinite(d[['uu','ou','uo','oo']].to_numpy()).all(1)
    d['all_corners_finite']=valid
    for tag,transform in [('prediction',lambda x:x),('absolute_error',lambda x:(x-d.ln_gamma_inf).abs())]:
        uu,ou,uo,oo=[transform(d[k]) for k in ('uu','ou','uo','oo')]
        d[tag+'_solute']=.5*((ou-uu)+(oo-uo))
        d[tag+'_solvent']=.5*((uo-uu)+(oo-ou))
        residual=d[tag+'_solute']+d[tag+'_solvent']-(oo-uu)
        if valid.any() and abs(residual[valid]).max()>1e-10: raise AssertionError('attribution identity failed')
    d.reset_index().to_csv(out/'hybrid_rows.csv',index=False)
    report=dict(model=a.model,rows=len(d),all_corners_finite=int(valid.sum()),
        unavailable_rows=d.index[~valid].tolist(),paired_rows_sha256=digest(a.paired_rows))
    if valid.any():
        report['mean_solute_delta_MAE']=float(d.loc[valid,'absolute_error_solute'].mean())
        report['mean_solvent_delta_MAE']=float(d.loc[valid,'absolute_error_solvent'].mean())
        report['mean_total_delta_MAE']=float(((d.loc[valid,'oo']-d.loc[valid,'ln_gamma_inf']).abs()-(d.loc[valid,'uu']-d.loc[valid,'ln_gamma_inf']).abs()).mean())
        report['fresh_UD_vs_stored_ref_max']=float(abs(d.loc[valid,'uu']-d.loc[valid,'ref']).max())
        report['fresh_open_vs_stored_candidate_max']=float(abs(d.loc[valid,'oo']-d.loc[valid,'candidate']).max())
    write_json(out/'hybrid.json',report)
    if not valid.all(): raise SystemExit('nonfinite corner(s): partial attribution recorded, not a decomposition of the full cited score')

def main():
    p=argparse.ArgumentParser(); s=p.add_subparsers(dest='cmd',required=True)
    for name in ('run','worker'):
        q=s.add_parser(name); q.add_argument('--open-profiles',required=True); q.add_argument('--out',required=True)
        q.add_argument('--model',choices=['Z0x','cosmosac_dsp'],default='Z0x'); q.add_argument('--compounds',default='data/benchmark/compounds.csv')
        if name=='run': q.add_argument('--paired-rows',required=True)
        else: q.add_argument('--rows',required=True); q.add_argument('--corner',choices=['uu','ou','uo','oo'],required=True)
    a=p.parse_args(); globals()[a.cmd](a)
if __name__=='__main__': main()
