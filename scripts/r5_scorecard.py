"""Regenerate nine score arms in separate processes, with P23 LLE status accounting.

Requires the already tested P14 audit hook (included in this patch). Uses the
unchanged evaluate prediction routines. Historical files and profiles are read-only.
"""
from __future__ import annotations
import argparse
import hashlib
import inspect
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import numpy as np
import pandas as pd
from r3_common import digest,write_json,cluster_ci
from r4_common import selected_profiles
from r4_lle import quality,strict_binodal,bounds
from r5_common import (BASE,fresh,observation_ids,pairs,systems,subset,
                        require_registration,fingerprint,check_fingerprint,STALL_KEYS)

TABLES=('idac','vle','he','lle')
MODELS=('Z0x','cosmosac2010','cosmosac_dsp')


def freeze(a):
    require_registration(a.registration);out=fresh(a.out)
    compounds=pd.read_csv('data/benchmark/compounds.csv')
    sources=selected_profiles(a.profile_root,compounds)
    open_inputs={};inventory=[]
    for arm in ('open630','open636'):
        p=out/'overlays'/arm;p.mkdir(parents=True)
        for key,folder,source in sources:
            if arm=='open630' and folder!='profiles_v2': continue
            meta=json.loads(source.read_text().splitlines()[0][8:])
            if 'p18_rule' not in meta: raise ValueError(f'P20 deployment provenance missing: {source}')
            (p/(key+'.sigma')).symlink_to(source.resolve());open_inputs[str(source.resolve())]=digest(source)
            inventory.append(dict(arm=arm,key=key,status=folder,path=str(source.resolve()),sha256=digest(source)))
    os.environ.pop('ZC_SIGMA_OVERRIDE_DIR',None)
    from zcosmo.cosmosac import sigma_path,SIGMA_DIR
    if not SIGMA_DIR.is_dir(): raise FileNotFoundError('UD-backed regeneration must run on the asset-bearing Mac')
    ud_inputs={}
    for table in TABLES:
        d=pd.read_csv('data/benchmark/'+table+'.csv')
        if 'has_sigma' in d:
            if not d.has_sigma.isin([True,False]).all(): raise ValueError('invalid has_sigma labels')
            d=d[d.has_sigma].copy()
        d=d.reset_index(drop=True);d['r5_row_id']=observation_ids(d,table)
        subset(d,'all')  # validate split labels before any evaluation
        if d.r5_row_id.duplicated().any(): raise ValueError('row IDs are not unique')
        for k in set(d[list(pairs(d,table))].to_numpy().ravel()):
            p=sigma_path(k)
            if p is None: raise FileNotFoundError(f'UD missing for declared has_sigma row: {k}')
            ud_inputs[str(p.resolve())]=digest(p)
        dest=out/'universe'/(table+'.csv');dest.parent.mkdir(exist_ok=True);d.to_csv(dest,index=False)
    modelpaths=['src/zcosmo/'+n for n in ('cosmosac.py','z0x.py','models.py','evaluate.py','metrics.py','scope.py','zmodel.py','baselines.py')]
    modelpaths+=['results/qc/dielectric.csv','results/qc/dispersion.csv','results/z_params/Z0.json']
    modelpaths+=['scripts/r4_lle.py','scripts/r5_scorecard.py','scripts/r5_common.py']
    inputs=fingerprint(modelpaths+['data/benchmark/'+t+'.csv' for t in TABLES]+['data/benchmark/compounds.csv'])
    from importlib.metadata import version,PackageNotFoundError
    packages={}
    for name in ('numpy','scipy','pandas','thermo','chemicals','rdkit','pyscf','pyberny'):
        try:packages[name]=version(name)
        except PackageNotFoundError:packages[name]=None
    config=dict(packages=packages,base=BASE,registration=a.registration,profile_root=str(Path(a.profile_root).resolve()),
        inputs=inputs,open_inputs=open_inputs,UD_inputs=ud_inputs,
        universe={t:dict(path=str((out/'universe'/(t+'.csv')).resolve()),sha256=digest(out/'universe'/(t+'.csv'))) for t in TABLES},
        overlays={k:str((out/'overlays'/k).resolve()) for k in ('open630','open636')},
        note='Fixed historical has_sigma universe. Expanded non-UD coverage requires a different labelled table.')
    write_json(out/'config.json',config);pd.DataFrame(inventory).to_csv(out/'profile_inventory.csv',index=False)


def worker(a):
    root=Path(a.run).resolve();cfg=json.loads((root/'config.json').read_text())
    check_fingerprint(cfg['inputs']);check_fingerprint(cfg['UD_inputs']);check_fingerprint(cfg['open_inputs'])
    for name in ('ZC_SIGMA_OVERRIDE_DIR','ZC_ONLY_KEYS','ZC_LLE_AUDIT_DIR','ZC_BENCH','ZC_PRED'):os.environ.pop(name,None)
    if a.arm!='UD': os.environ['ZC_SIGMA_OVERRIDE_DIR']=cfg['overlays'][a.arm]
    from zcosmo import evaluate as ev
    from zcosmo.models import make_model
    from zcosmo.cosmosac import sigma_path
    if 'audit' not in inspect.signature(ev.binodal).parameters: raise RuntimeError('apply the P14 hook included with P27')
    smi=ev._smiles();out=fresh(root/'predictions'/a.model/a.arm);t0=time.perf_counter()
    for table in TABLES:
        u=cfg['universe'][table]
        if digest(u['path'])!=u['sha256']: raise ValueError('frozen universe changed')
        d=pd.read_csv(u['path']);ca,cb=pairs(d,table)
        eligible=~(d[ca].isin(STALL_KEYS)|d[cb].isin(STALL_KEYS)) if a.arm=='open630' else pd.Series(True,index=d.index)
        d['profile_eligible']=eligible;d['r5_eval_status']=np.where(eligible,'pending','excluded_S1_S2_by_design')
        sub=d[eligible].copy().reset_index(drop=True)
        if a.arm!='UD':
            for k in set(sub[[ca,cb]].to_numpy().ravel()):
                p=Path(cfg['overlays'][a.arm])/(k+'.sigma')
                if not p.is_file() or sigma_path(k).resolve()!=p.resolve(): raise ValueError('unintended fallback to UD')
        if table=='idac':
            columns=['pred_ln_gamma_inf'];values=[ev.predict_idac(a.model,sub,smi)]
        elif table=='vle':
            columns=['pred_P','pred_y1'];values=list(ev.predict_vle(a.model,sub,smi))
        elif table=='he':
            columns=['pred_HE_J'];values=[ev.predict_he(a.model,sub,smi)]
        else:
            columns=['pred_split','pred_x1_I','pred_x1_II','r5_detection','r5_x1_I','r5_x1_II']
            values=[np.full(len(sub),np.nan) for _ in columns];status=[];models={};calls={}
            # Extend the accepted repair only after the same first-20-good control gate per arm.
            controls=[]
            unique=sorted({(r.c1,r.c2,float(round(float(r.T)/2)*2)) for r in sub.itertuples()})
            for c1,c2,T in unique:
                model=make_model(a.model,[c1,c2],[smi[c1],smi[c2]])
                oldaudit={};old=ev.binodal(model,T,audit=oldaudit);oldaudit['returned']=old
                if quality(oldaudit)[0]!=1.:continue
                answer=strict_binodal(make_model(a.model,[c1,c2],[smi[c1],smi[c2]]),T,budget=4000)
                same=(answer['status']=='root_passes_refined_sampled_checks' and
                      any(np.max(abs(np.asarray(q['x'])-old))<1e-4 for q in answer.get('roots',[])))
                controls.append(dict(c1=c1,c2=c2,T=T,passed=bool(same),answer=answer))
                if not same:raise ValueError('P23 extension control failed; this score arm is not accepted')
                if len(controls)==20:break
            write_json(out/'lle_controls.json',dict(controls=controls,passed=len(controls)==20))
            if len(controls)!=20:raise ValueError('fewer than 20 good controls; report inconclusive, do not weaken the gate')
            with (out/'lle_calls.jsonl').open('w') as handle:
                for i,r in enumerate(sub.itertuples()):
                    pair=(r.c1,r.c2);T=float(round(float(r.T)/2)*2);key=(pair,T)
                    if pair not in models: models[pair]=make_model(a.model,list(pair),[smi[k] for k in pair])
                    if key not in calls:
                        audit={};b=ev.binodal(models[pair],T,audit=audit)
                        audit.update(model=a.model,c1=pair[0],c2=pair[1],binodal_T=T,returned=b)
                        decision,label=quality(audit);xy=b;repair=None
                        if not np.isfinite(decision):
                            # The same accepted P23 finite-grid repair, no new thresholds.
                            fresh_model=make_model(a.model,list(pair),[smi[k] for k in pair])
                            repair=strict_binodal(fresh_model,T,budget=4000);label=repair['status'];xy=None
                            if label=='root_passes_refined_sampled_checks':
                                decision=1.;xy=max(repair['roots'],key=lambda z:z['x'][1]-z['x'][0])['x']
                            elif label=='gap_witness_only':decision=1.
                            elif label=='no_gap_on_refined_grid':decision=0.
                            else:decision=np.nan
                        calls[key]=(b,decision,label,xy)
                        handle.write(json.dumps(dict(legacy=audit,repair=repair,registration=cfg['registration']),allow_nan=False)+'\n');handle.flush()
                    b,decision,label,xy=calls[key]
                    values[0][i]=float(b is not None)
                    if b is not None:values[1][i],values[2][i]=b
                    values[3][i]=decision
                    if decision==1. and xy is not None: values[4][i],values[5][i]=xy
                    status.append(label)
            d['r5_lle_status']='not_eligible';d.loc[eligible,'r5_lle_status']=status
        for c,v in zip(columns,values):d[c]=np.nan;d.loc[eligible,c]=v
        finite=np.isfinite(np.stack(values,axis=1)).all(1) if table!='lle' else np.isfinite(values[3])
        d.loc[eligible,'r5_eval_status']=np.where(finite,'evaluated','nonfinite_or_unresolved')
        d.to_csv(out/(table+'.csv'),index=False)
    check_fingerprint(cfg['inputs']);check_fingerprint(cfg['UD_inputs']);check_fingerprint(cfg['open_inputs'])
    write_json(out/'timing.json',dict(model=a.model,arm=a.arm,wall_s=time.perf_counter()-t0,registration=cfg['registration']))


def scalar_metrics(d,table):
    sid=systems(d,table)
    if table=='idac':
        pred=d.pred_ln_gamma_inf.to_numpy(float);target=d.ln_gamma_inf.to_numpy(float);e=pred-target
        from zcosmo.metrics import selectivity_spearman
        rho,n=selectivity_spearman(d,'pred_ln_gamma_inf')
        extra=dict(bias=float(e.mean()),solvent_rank_rho=float(rho) if np.isfinite(rho) else None,ranking_solutes=n)
    elif table=='vle':
        e=100*(d.pred_P-d.P).to_numpy(float)/d.P.to_numpy(float)
        from zcosmo.metrics import three_phase_mask
        homogeneous=~three_phase_mask(d)
        ym=np.isfinite(d[['pred_y1','y1']].to_numpy()).all(1) if 'y1' in d else np.zeros(len(d),bool)
        extra=dict(homogeneous_rows=int(homogeneous.sum()),three_phase_rows=int((~homogeneous).sum()),
            homogeneous_AAD_pct=float(abs(e[homogeneous]).mean()) if homogeneous.any() else None,
            vapor_y_rows=int(ym.sum()),vapor_y_AAD=float(abs(d.loc[ym,'pred_y1']-d.loc[ym,'y1']).mean()) if ym.any() else None)
    else:
        e=(d.pred_HE_J-d.HE_J).to_numpy(float);large=abs(d.HE_J.to_numpy(float))>20
        extra=dict(sign_rows=int(large.sum()),sign_correct=float((np.sign(d.pred_HE_J.to_numpy()[large])==np.sign(d.HE_J.to_numpy()[large])).mean()) if large.any() else None)
    return dict(rows=len(d),systems=len(np.unique(sid)),MAE=float(abs(e).mean()),
                MAE_CI95=cluster_ci(abs(e),sid),**extra),e


def eligibility(d,table):
    if table=='idac':cols=['pred_ln_gamma_inf','ln_gamma_inf']
    elif table=='vle':cols=['pred_P','P']
    elif table=='he':cols=['pred_HE_J','HE_J']
    else:return d.profile_eligible.to_numpy(bool)
    finite=np.isfinite(d[cols].to_numpy(float)).all(1)&d.profile_eligible.to_numpy(bool)
    if table=='vle':finite&=d.P.to_numpy(float)>0
    return finite


def lle_metrics(d):
    result=bounds(d.r5_detection.to_numpy(float),systems(d,'lle'))
    valid=(d.r5_detection==1.)&np.isfinite(d[['r5_x1_I','r5_x1_II','x1']].to_numpy(float)).all(1)
    result['endpoint_rows']=int(valid.sum())
    result['composition_MAE']=float(np.minimum(abs(d.loc[valid,'x1']-d.loc[valid,'r5_x1_I']),
                  abs(d.loc[valid,'x1']-d.loc[valid,'r5_x1_II'])).mean()) if valid.any() else None
    result['statuses']=d.r5_lle_status.value_counts().to_dict()
    result['legacy_gap_found_rows']=float(d.pred_split.mean())
    result['meaning']='Operational finite-grid detection, not a certificate of miscibility or global stability. Witnesses have no endpoint MAE.'
    return result


def summarize(a):
    root=Path(a.run).resolve();cfg=json.loads((root/'config.json').read_text())
    report={'base':BASE,'registration':cfg['registration'],'tables':{},'scope':'Z0x-UD remains reference; open630 secondary; open636 includes exploratory S1/S2'}
    lines=['Z-COSMO regenerated scorecard, '+a.split,'',report['scope'],'']
    for table in TABLES:
        frames={}
        for model in MODELS:
            for arm in ('UD','open630','open636'):
                p=root/'predictions'/model/arm/(table+'.csv');d=pd.read_csv(p)
                if d.r5_row_id.duplicated().any():raise ValueError('duplicate prediction identities')
                frames[(model,arm)]=subset(d,a.split).set_index('r5_row_id',drop=False)
        first=next(iter(frames.values()))
        if any(set(d.index)!=set(first.index) for d in frames.values()): raise ValueError('denominator identity mismatch')
        standalone={};paired=[]
        for (model,arm),d in frames.items():
            eligible=d[d.profile_eligible]
            if table=='lle':ans=lle_metrics(eligible)
            else:
                valid=eligibility(d,table)
                ans,_=scalar_metrics(d.loc[valid],table) if valid.any() else ({'rows':0},None)
                ans.update(requested_rows=len(d),profile_eligible_rows=len(eligible),unavailable_rows=int((~valid).sum()))
            standalone[model+'/'+arm]=ans
        # Fixed pairwise intersections, never a hidden intersection over all nine arms.
        for model in MODELS:
            r=frames[(model,'UD')]
            for arm in ('open630','open636'):
                c=frames[(model,arm)].loc[r.index]
                common=eligibility(r,table)&eligibility(c,table)
                rr,cc=r.loc[common],c.loc[common]
                if table=='lle':
                    pair=dict(reference=lle_metrics(rr),candidate=lle_metrics(cc))
                elif len(rr):
                    rm,er=scalar_metrics(rr,table);cm,ec=scalar_metrics(cc,table)
                    pair=dict(reference=rm,candidate=cm,delta_MAE_CI95=cluster_ci(abs(ec)-abs(er),systems(rr,table)))
                else:pair=dict(reference={'rows':0},candidate={'rows':0})
                pair.update(model=model,arm=arm,common_rows=len(rr),row_ids_sha256=hashlib.sha256('\n'.join(rr.index).encode()).hexdigest())
                paired.append(pair)
        report['tables'][table]=dict(standalone=standalone,pairwise=paired)
        lines+=['Table: '+table,'','| Model / profiles | Rows | Systems | Error or detection | Status |','|---|---:|---:|---|---|']
        for name,r in standalone.items():
            if table=='lle':value=str(r['row_gap_found_bounds']);status=f"{r['endpoint_rows']} checked endpoint rows; {r['unresolved_rows']} unresolved"
            else:value=str(r.get('MAE'));status=f"{r.get('unavailable_rows',0)} unavailable of {r.get('requested_rows',0)}"
            lines.append(f"| {name} | {r['rows']} | {r.get('systems','')} | {value} | {status} |")
        lines+=['','Pairwise comparison denominators and CIs are in scorecard.json; each open arm is compared with UD on identical row identities.','']
    write_json(root/('scorecard_'+a.split+'.json'),report)
    (root/('scorecard_'+a.split+'.md')).write_text('\n'.join(lines)+'\n')


def run(a):
    freeze(a)
    for model in MODELS:
        for arm in ('UD','open630','open636'):
            subprocess.run([sys.executable,str(Path(__file__).resolve()),'worker','--run',str(Path(a.out).resolve()),
                            '--model',model,'--arm',arm],check=True)
    for split in ('all','test'):
        summarize(argparse.Namespace(run=a.out,split=split))


def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
    for name in ('run','freeze'):
        q=s.add_parser(name);q.add_argument('--profile-root',default='data/pyscf_sigma');q.add_argument('--out',required=True);q.add_argument('--registration',required=True)
    q=s.add_parser('worker');q.add_argument('--run',required=True);q.add_argument('--model',choices=MODELS,required=True);q.add_argument('--arm',choices=['UD','open630','open636'],required=True)
    q=s.add_parser('summarize');q.add_argument('--run',required=True);q.add_argument('--split',choices=['all','test','train'],default='test')
    a=p.parse_args();globals()[a.cmd](a)
if __name__=='__main__':main()
