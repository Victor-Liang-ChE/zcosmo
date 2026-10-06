"""E accounting of actual Z0x IDAC; A ES/HB interventions used only diagnostically.

Run a separate worker per frozen profile set. No fitting, no table writes.
A component decomposition is additive; ES and HB Shapley attributions are not
claimed to be separately measurable physical free energies.
"""
from __future__ import annotations
import argparse
from dataclasses import replace
import json
import os
from pathlib import Path
import subprocess
import sys
import shutil
import numpy as np
import pandas as pd
from r3_common import digest, write_json
from r5_common import fresh, observation_ids, fingerprint, check_fingerprint, require_registration


def stencil(parts0, partsh, h):
    return np.asarray(parts0)+(np.asarray(partsh)-np.asarray(parts0))/h


def account(model,T,es=True,hb=True,h=None,flags=False):
    from zcosmo.cosmosac import Mixture
    h=model.H if h is None else h
    pieces=[];limits=[]
    for x0 in (0.,h):
        x=np.array([x0,1-x0]);c=model._c(x0)
        # Preserve the actual rounded-c cache convention when establishing parity.
        model._frozen(T,x0,c); original=model._mix[round(c,6)]
        prm=original.prm.with_(A_ES=original.prm.A_ES if es else 0.,
             B_ES=original.prm.B_ES if es else 0.,
             c_OH_OH=original.prm.c_OH_OH if hb else 0.,
             c_OT_OT=original.prm.c_OT_OT if hb else 0.,
             c_OH_OT=original.prm.c_OH_OT if hb else 0.)
        fl=original.fl if not flags else [replace(f,disp_flag='NHB') for f in original.fl]
        mix=Mixture(None,prm,fluids=fl)
        terms=np.array([mix.lngamma_comb(x),mix.lngamma_resid(T,x),mix.lngamma_disp(x,T)])
        pieces.append(terms@x)
        if x0==0.: limits=terms[:,0]
    out=stencil(pieces[0],pieces[1],h)
    return out,np.asarray(limits)


def worker(a):
    config=json.loads(Path(a.config).read_text()); spec=config['variants'][a.variant]
    for name in ('ZC_SIGMA_OVERRIDE_DIR','ZC_ONLY_KEYS'): os.environ.pop(name,None)
    if spec.get('directory'): os.environ['ZC_SIGMA_OVERRIDE_DIR']=str(Path(spec['directory']).resolve())
    from zcosmo.cosmosac import sigma_path
    from zcosmo.models import make_model
    rows=pd.read_csv(config['rows'])
    if 'r5_row_id' not in rows: rows['r5_row_id']=observation_ids(rows,'idac')
    if rows.r5_row_id.duplicated().any(): raise ValueError('duplicate row ids')
    compounds=pd.read_csv(config.get('compounds','data/benchmark/compounds.csv'))
    smi=dict(zip(compounds.inchikey,compounds.smiles));cache={};records=[];inputs={};max_parity=0.;max_flag=0.
    for r in rows.itertuples():
        key=(r.solute,r.solvent)
        for k in key:
            p=sigma_path(k)
            if p is None: raise FileNotFoundError(k)
            # Open overlays must be complete for the supplied queries, not mixed with UD by accident.
            if spec.get('directory') and p.resolve()!=(Path(spec['directory'])/f'{k}.sigma').resolve():
                raise ValueError(f'profile fallback in {a.variant}: {k}')
            inputs[str(p.resolve())]=digest(p)
        rec=dict(r5_row_id=r.r5_row_id,solute=r.solute,solvent=r.solvent,T=float(r.T),error='')
        try:
            if key not in cache: cache[key]=make_model('Z0x',list(key),[smi[k] for k in key])
            m=cache[key]
            actual=float(m.lngamma_inf(r.T,0));base,lim=account(m,r.T)
            discrepancy=abs(base.sum()-actual)
            if not np.isfinite(actual) or not np.isfinite(base).all(): raise ValueError('nonfinite Z0x query')
            if discrepancy>1e-9: raise AssertionError(f'component parity failure: {discrepancy}')
            max_parity=max(max_parity,discrepancy)
            flag,_=account(m,r.T,flags=True);max_flag=max(max_flag,float(abs(flag-base).max()))
            if np.max(abs(flag-base))>1e-10: raise AssertionError('H2O/COOH flags reached London Z0x')
            try:
                dsp=make_model('cosmosac_dsp',list(key),[smi[k] for k in key]).lngamma_inf(r.T,0)
            except Exception: dsp=np.nan
            rec.update(dsp_total=float(dsp),total=actual,comb=float(base[0]),residual=float(base[1]),london=float(base[2]),
                       exact_limit=float(lim.sum()),endpoint_stencil_error=float(actual-lim.sum()),
                       solvent_c_ES=float(m._c(0.)),flag_change=float(flag.sum()-actual))
            for es,hb in ((False,False),(True,False),(False,True),(True,True)):
                q,_=account(m,r.T,es,hb)
                rec[f'kernel_{int(es)}{int(hb)}']=float(q[1])
            for h in (1e-5,1e-6):
                q,_=account(m,r.T,h=h);rec[f'stencil_{h:g}']=float(q.sum())
        except AssertionError: raise
        except Exception as e:
            rec['error']=type(e).__name__+': '+str(e)
        records.append(rec)
    out=Path(a.out);pd.DataFrame(records).to_csv(out,index=False)
    check_fingerprint(inputs)
    write_json(str(out)+'.json',dict(variant=a.variant,profile_inputs=inputs,rows=len(rows),
        max_parity=max_parity,max_flag=max_flag,registration=config['registration']))


def compare(reference,candidate):
    r=reference.set_index('r5_row_id');c=candidate.set_index('r5_row_id')
    if not r.index.is_unique or set(r.index)!=set(c.index): raise ValueError('query identity mismatch')
    c=c.loc[r.index];required=['total','comb','residual','london','kernel_00','kernel_10','kernel_01','kernel_11']
    if any(k not in r or k not in c for k in required): raise ValueError('no evaluable component rows')
    finite=np.isfinite(r[required].to_numpy(float)).all(1)
    if not np.array_equal(finite,np.isfinite(c[required].to_numpy(float)).all(1)):
        raise ValueError('finite coverage differs; do not interpret a partial effect as the original panel')
    out=c[['solute','solvent','T']].copy();out['finite_all']=finite
    for k in required+['endpoint_stencil_error']:
        out['delta_'+k]=c[k]-r[k]
    d={k:out['delta_kernel_'+k] for k in ('00','10','01','11')}
    out['ES_shapley']=.5*((d['10']-d['00'])+(d['11']-d['01']))
    out['HB_shapley']=.5*((d['01']-d['00'])+(d['11']-d['10']))
    if finite.any():
        err=out.ES_shapley+out.HB_shapley-(d['11']-d['00'])
        if abs(err[finite]).max()>1e-10: raise AssertionError('ES/HB identity failed')
        additive=out.delta_comb+out.delta_residual+out.delta_london-out.delta_total
        if abs(additive[finite]).max()>2e-9: raise AssertionError('component identity failed')
    return out


def run(a):
    cfg=json.loads(Path(a.config).read_text());require_registration(cfg['registration'])
    if 'inputs' in cfg: check_fingerprint(cfg['inputs'])
    if 'reference' not in cfg['variants']: raise ValueError('name the reference variant explicitly')
    out=fresh(a.out);frames={}
    for v in cfg['variants']:
        p=out/(v+'.csv')
        subprocess.run([sys.executable,str(Path(__file__).resolve()),'worker','--config',str(Path(a.config).resolve()),
                        '--variant',v,'--out',str(p)],check=True)
        frames[v]=pd.read_csv(p)
    summaries=[]
    for v in frames:
        if v=='reference': continue
        d=compare(frames['reference'],frames[v]);d.to_csv(out/(v+'-delta.csv'))
        for solvent,g in [('ALL',d)]+list(d.groupby('solvent',sort=True)):
            good=g[g.finite_all]
            s=dict(variant=v,solvent=solvent,rows=len(g),finite=len(good))
            for k in ('delta_total','delta_comb','delta_residual','delta_london','ES_shapley','HB_shapley','delta_endpoint_stencil_error'):
                s[k+'_mean']=float(good[k].mean()) if len(good) else None
                s[k+'_mean_abs']=float(good[k].abs().mean()) if len(good) else None
                s[k+'_max_abs']=float(good[k].abs().max()) if len(good) else None
            summaries.append(s)
    write_json(out/'summary.json',dict(config_sha256=digest(a.config),registration=cfg['registration'],
        summaries=summaries,note='No experimental response is used; four kernels are diagnostic interventions.'))



def prepare(a):
    """Freeze the P22 projection panel plus six one-profile UD-shape probes on the Mac."""
    from r3_common import read_sigma,write_sigma
    require_registration(a.registration);out=fresh(a.out)
    root=Path(a.artifacts).resolve();background=Path(a.background).resolve()
    keys=('LYCAIKOWRPUZTN-UHFFFAOYSA-N','MTHSVFCYNBDYFN-UHFFFAOYSA-N',
          'ZIBGPFATKBEMQZ-UHFFFAOYSA-N','OKKJLVBELUTLKV-UHFFFAOYSA-N',
          'XLYOFNOQVPJJNP-UHFFFAOYSA-N','BKIMMITUMNQMOS-UHFFFAOYSA-N')
    d=pd.read_csv(a.idac);d=d[d.solute.isin(keys)|d.solvent.isin(keys)].copy()
    d['r5_row_id']=observation_ids(d,'idac')
    if len(d)!=859: raise ValueError('P22 frozen panel is not 859 rows; resolve the input version')
    # Experimental responses are deliberately not passed to the term workers.
    rows=out/'queries.csv';d[['r5_row_id','solute','solvent','T']].to_csv(rows,index=False)
    inputs=fingerprint([a.idac,a.compounds]);paths={}
    for key in keys:
        for variant in ('native','area_zero','capacitary_zero'):
            hits=[p for p in root.rglob(key+'.sigma') if
                  (p.parent.name==variant if variant!='native' else p.parent.name not in ('area_zero','capacitary_zero'))]
            # A repeated identical artifact is acceptable; conflicting native outputs are not.
            hashes={digest(p) for p in hits}
            if len(hashes)!=1: raise ValueError(f'{key}/{variant}: missing or conflicting artifacts')
            paths[key,variant]=sorted(hits)[0].resolve();inputs[str(paths[key,variant])]=next(iter(hashes))
    source={p.stem:p.resolve() for p in background.glob('*.sigma')}
    needed=set(d[['solute','solvent']].to_numpy().ravel())
    if needed-set(source): raise ValueError('background is incomplete; no UD fallback is authorized')
    variants={}
    for name,kind in [('reference','native'),('area_zero','area_zero'),('capacitary_zero','capacitary_zero')]:
        folder=out/name;folder.mkdir()
        for key in needed:
            p=paths[key,kind] if key in keys else source[key]
            (folder/(key+'.sigma')).symlink_to(p);inputs[str(p)]=digest(p)
        variants[name]={'directory':str(folder)}
    os.environ.pop('ZC_SIGMA_OVERRIDE_DIR',None)
    from zcosmo.cosmosac import sigma_path,SIGMA_DIR
    if not SIGMA_DIR.is_dir(): raise FileNotFoundError('UD-shape diagnostics require Mac-only UD assets')
    for key in keys:
        folder=out/('UDshape_'+key[:14]);folder.mkdir()
        for other in needed:
            if other!=key: (folder/(other+'.sigma')).symlink_to(out/'reference'/(other+'.sigma'))
        sig,po,meta=read_sigma(out/'reference'/(key+'.sigma'));ud=sigma_path(key)
        if ud is None: raise FileNotFoundError(key)
        _,pu,_=read_sigma(ud);inputs[str(Path(ud).resolve())]=digest(ud)
        meta.update(source='R5 shape-only diagnostic; original area/volume/metadata retained')
        write_sigma(folder/(key+'.sigma'),sig,pu/pu.sum()*po.sum(),meta)
        variants[folder.name]={'directory':str(folder)}
    inputs.update(fingerprint(['results/qc/dielectric.csv','results/qc/dispersion.csv','results/z_params/Z0.json',
          'src/zcosmo/cosmosac.py','src/zcosmo/z0x.py',str(rows)]))
    write_json(out/'config.json',dict(variants=variants,rows=str(rows),compounds=str(Path(a.compounds).resolve()),
         registration=a.registration,inputs=inputs,keys=keys,
         note='P22 panel; one fresh worker per immutable profile overlay; no experimental response in queries.'))


def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
    for name in ('run','worker'):
        q=s.add_parser(name);q.add_argument('--config',required=True);q.add_argument('--out',required=True)
        if name=='worker': q.add_argument('--variant',required=True)
    q=s.add_parser('prepare');q.add_argument('--background',required=True);q.add_argument('--artifacts',required=True)
    q.add_argument('--out',required=True);q.add_argument('--registration',required=True)
    q.add_argument('--idac',default='data/benchmark/idac.csv');q.add_argument('--compounds',default='data/benchmark/compounds.csv')
    a=p.parse_args();globals()[a.cmd](a)
if __name__=='__main__':main()
