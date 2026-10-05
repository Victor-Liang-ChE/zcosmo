"""Portable round-4 regression tests. Native PySCF and real profiles are separate gates."""
from __future__ import annotations
import argparse
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
from unittest.mock import patch
import numpy as np
import pandas as pd
from scipy.integrate import quad
from scipy.optimize import brentq
from r3_common import STALL_KEYS,write_json,write_sigma,digest
import r4_charge as ch
import r4_common as cm
import r4_glycols as gl
import r4_lle as lle
import r4_metadata as md


def algebra():
    t=1.5
    sphere=ch.gaussian_sphere(t)
    density=lambda r:4/np.sqrt(np.pi)*r*r*np.exp(-r*r)
    inside=quad(density,0,t,epsabs=1e-13)[0]
    weighted_out=quad(lambda r:density(r)*t/r,t,np.inf,epsabs=1e-13)[0]
    q=-(1-inside-weighted_out)
    assert abs(q-sphere['screening_charge_e'])<1e-13
    assert abs(quad(density,t,np.inf)[0]-sphere['electrons_outside'])<1e-13
    rng=np.random.default_rng(4);a=rng.normal(size=(19,19));K=a@a.T+np.eye(19)
    q=rng.normal(size=19);area=rng.uniform(.1,2,19)
    qa,qc,c=ch.project(q,area,K)
    assert max(abs(qa.sum()),abs(qc.sum()))<1e-12
    assert np.ptp((qa-q)/area)<1e-12
    assert np.ptp(K@(qc-q))<1e-11
    vals={format(i,'03b'):rng.normal(size=100) for i in range(8)}
    error=float(abs(gl.shapley_three(vals).sum(0)-(vals['111']-vals['000'])).max())
    assert error<1e-12
    # Row normalization preserves constants, not the area-weighted sigma moment.
    M=np.array([[1.,2.],[3.,1.] ]);B=M/M.sum(1)[:,None]
    weights=np.array([1.,2.]);sig=np.array([.01,-.005])
    assert abs(weights@sig)<1e-15 and abs(weights@(B@sig))>1e-3
    expected={'OCCO':('polyol_without_ether',2,0),
              'OCCOCCO':('polyol_with_ether',2,1),
              'OCCOCCOCCO':('polyol_with_ether',2,2),
              'COCCOC':('polyether_no_OH',0,2)}
    for smiles,(group,oh,ether) in expected.items():
        s=cm.structure(smiles);assert (s['group'],s['OH_count'],s['ether_count'])==(group,oh,ether)
    return dict(gaussian_sphere=sphere,quadrature_charge_e=q if np.ndim(q)==0 else -(1-inside-weighted_out),
                shapley_max_error=error,projection_max_sum=float(max(abs(qa.sum()),abs(qc.sum()))))


class Regular:
    def __init__(self,chi):self.chi=chi
    def lngamma(self,T,x):return self.chi*np.array([x[1]**2,x[0]**2])


def lle_tests(tmp):
    ideal=lle.strict_binodal(Regular(0),298.15)
    assert ideal['status']=='no_gap_on_refined_grid' and not ideal['globally_certified']
    reg=lle.strict_binodal(Regular(3),298.15)
    assert reg['status']=='root_passes_refined_sampled_checks'
    root=brentq(lambda x:np.log(x/(1-x))+3*(1-2*x),.001,.49,xtol=1e-14)
    assert np.max(abs(np.array(reg['roots'][0]['x'])-[root,1-root]))<1e-10
    def bad(fun,x0,**kw):return SimpleNamespace(x=np.asarray(x0),success=False)
    with patch.object(lle,'least_squares',bad):
        witness=lle.strict_binodal(Regular(3),298.15)
    assert witness['status']=='gap_witness_only' and witness['nonconvex_witness']['depth']>0
    exhausted=lle.strict_binodal(Regular(3),298.15,budget=1)
    assert exhausted['status']=='unresolved' and exhausted['model_calls']==1
    b=lle.bounds([1,np.nan,0],['a','a','b'])
    assert b['rows']==3 and b['unresolved_rows']==1 and b['system_gap_found_bounds']==[0.,.5]
    sidecars=[];rows=[]
    for j,(status,ends,res,margin) in enumerate([
          ('refined_root',[.1,.9],1e-10,0.),('refined_root',[.1,.9],.005,-.001),('no_gap_on_grid',None,None,None)]):
        sidecars.append(dict(model='Z0x',c1=f'A{j}',c2='B',binodal_T=298.,status=status,
                             returned=ends,residual_max=res,sampled_tangent_margin=margin))
        rows.append(dict(c1=f'A{j}',c2='B',T=298.15,split='test_one',x1=.12,
                         pred_split=ends is not None,pred_x1_I=ends[0] if ends else np.nan,
                         pred_x1_II=ends[1] if ends else np.nan))
    sp=tmp/'sidecar.jsonl';sp.write_text(''.join(json.dumps(r)+'\n' for r in sidecars))
    pp=tmp/'pred.csv';pd.DataFrame(rows).to_csv(pp,index=False);original=digest(pp)
    lle.audit(SimpleNamespace(sidecars=str(sp),predictions=str(pp),repairs=None,split='test',model='Z0x',out=str(tmp/'audit')))
    got=pd.read_csv(tmp/'audit/quality_rows.csv');assert got.r4_split.isna().sum()==1 and len(got)==3
    assert digest(pp)==original
    return dict(regular_roots=reg['roots'],regular_model_calls=reg['model_calls'],
                ideal_model_calls=ideal['model_calls'],bad_refinement_status=witness['status'],
                exhausted_status=exhausted['status'],audit_rows=len(got),unknown_rows=1)


def metadata_tests(tmp):
    root=tmp/'assets';keys=[f'SYNTH{i:04d}' for i in range(630)]+list(STALL_KEYS)
    compounds=pd.DataFrame(dict(inchikey=keys,smiles=['CC(=O)O']*636));cp=tmp/'compounds.csv';compounds.to_csv(cp,index=False)
    source_hashes={}
    for k in keys:
        folder='s1_stalled' if k==cm.S1_KEY else ('s2_stalled' if k in STALL_KEYS else 'profiles_v2')
        dest=root/folder/f'{k}.sigma';dest.parent.mkdir(parents=True,exist_ok=True)
        p=np.zeros((3,51));p[0,25]=10
        meta={'volume [A^3]':12.,'disp. flag':'HB-DONOR-ACCEPTOR','geometry_converged':True if folder=='profiles_v2' else ('S1' if folder=='s1_stalled' else 'S2'),
              'standard_INCHIKEY':k}
        write_sigma(dest,np.linspace(-.025,.025,51),p,meta)
        write_json(dest.with_suffix('.xyz.json'),dict(sym=['O','H'],x=[[0.,0.,0.],[0.,0.,1.]]))
        source_hashes[str(dest)]=digest(dest)
    # Only the native geometry classifier is stubbed. Exercise real 636-file I/O,
    # byte identity, manifest verification, backup, explicit apply and rollback.
    parser=tmp/'parser.py';parser.write_text('portable classifier fixture\n')
    real_digest=md.digest
    def mapped_digest(p):return real_digest(parser if str(p)=='data/raw/nist/to_sigma.py' else p)
    with patch.object(md,'flag_for_geometry',return_value='COOH'),patch.object(md,'digest',mapped_digest),redirect_stdout(io.StringIO()):
        bundle=tmp/'bundle';backup=tmp/'backup'
        md.prepare(SimpleNamespace(root=str(root),compounds=str(cp),geometry_map=None,out=str(bundle)))
        manifest=md.verify_bundle(bundle,require_original=True)
        for r in manifest['profiles']:
            src=Path(r['source']);cand=bundle/r['relative']
            assert src.read_bytes().partition(b'\n')[2]==cand.read_bytes().partition(b'\n')[2]
            before=json.loads(src.read_text().splitlines()[0][8:]);after=json.loads(cand.read_text().splitlines()[0][8:])
            assert before['geometry_converged']==after['geometry_converged']
        md.apply(SimpleNamespace(bundle=str(bundle),backup=str(backup)))
        assert all(digest(r['source'])==r['candidate_sha256'] for r in manifest['profiles'])
        md.rollback(SimpleNamespace(backup=str(backup)))
        assert all(digest(p)==h for p,h in source_hashes.items())
        suspect=bundle/manifest['profiles'][0]['relative'];suspect.write_bytes(suspect.read_bytes()+b'\n')
        try:md.verify_bundle(bundle,require_original=True)
        except ValueError:pass
        else:raise AssertionError('tampered candidate accepted')
    return dict(profiles=636,round_trip='byte-identical originals',raw_rows='byte-identical',
                S1_S2_flags='preserved',tamper='rejected',classifier='stub, not a native parser gate')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args()
    with tempfile.TemporaryDirectory(prefix='r4-selftest-') as td:
        tmp=Path(td);result=dict(algebra=algebra(),lle=lle_tests(tmp),metadata=metadata_tests(tmp))
    result['native_pyscf_tested']=False
    write_json(a.out,result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
