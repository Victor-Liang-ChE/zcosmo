"""Synthetic software tests only. No UD data, quantum chemistry or real Z0x scores."""
from __future__ import annotations
import argparse
from contextlib import ExitStack
import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
import numpy as np
import pandas as pd
import r12_analysis as a
import r12_review as r
from r11_selftest import panel
from r3_common import write_sigma


def data():
    counts=list(a.GLYCOLS.items())+[(f'OTHER{k}',(f'other{k}',20 if k<8 else 30)) for k in range(9)]
    rows=[];exact=[];cases=[]
    for solvent,(_name,n) in counts:
        part=[]
        for k in range(n):
            truth=float(k%7)/10
            vals={c:truth+2-.1*int(c[0])-.2*int(c[1])-1.3*int(c[2])+.03*int(c[0])*int(c[2]) for c in a.CORNERS}
            row=dict(r3_row_id=f'id-{len(rows):04d}',solute='SOLUTE',solvent=solvent,T=298.15+k,
                     ln_gamma_inf=truth,**vals,UD=vals['111'])
            rows.append(row);part.append({k:row[k] for k in ('r3_row_id','T')})
            if solvent in a.GLYCOLS:
                values=[truth+2-.15*int(c[0])-.05*int(c[1])-1.1*int(c[2])+.02*int(c[0])*int(c[1]) for c in a.CORNERS]
                exact.append(values+[truth+.45])
        cases.append(dict(solute='SOLUTE',solvent=solvent,rows=part))
    old=np.array([[z[c] for c in ('000','UD')] for z in rows if z['solvent'] in a.GLYCOLS])
    return rows,old,np.array(exact),cases


class Arithmetic(unittest.TestCase):
    def test_hybrid_all_eight_corners(self):
        o=np.zeros((3,51));o[0,25]=90;o[1,40]=10
        c=np.zeros((3,51));c[0,25]=100;c[2,10]=100
        for corner in a.CORNERS:
            v,m=a.hybrid(o,{'volume [A^3]':70,'keep':'old'},c,{'volume [A^3]':100},corner)
            self.assertAlmostEqual(v.sum(),200 if corner[0]=='1' else 100)
            np.testing.assert_allclose(v/v.sum(),c/c.sum() if corner[2]=='1' else o/o.sum())
            self.assertEqual(m['volume [A^3]'],100 if corner[1]=='1' else 70)
            self.assertEqual(m['keep'],'old')

    def test_nonfinite_and_invalid_profiles(self):
        for p in (np.zeros((3,51)),np.ones((2,51)),np.full((3,51),np.nan),-np.ones((3,51))):
            with self.assertRaises(ValueError):a.profile(p)
        with self.assertRaises(ValueError):a.hybrid(np.ones((3,51)),{'volume [A^3]':0},np.ones((3,51)),{'volume [A^3]':1},'000')

    def test_sigma_boundary_partition(self):
        masks=a.band_masks()
        self.assertEqual([int(v.sum()) for v in masks.values()],[16,5,9,5,16])
        self.assertTrue(masks['negative_tail'][15])  # -0.010
        self.assertTrue(masks['negative_shoulder'][20])  # -0.005
        self.assertTrue(masks['centre'][25])
        self.assertTrue(masks['positive_shoulder'][30])
        self.assertTrue(masks['positive_tail'][35])

    def test_channel_cancellation_is_not_shape_erasure(self):
        x=np.zeros((3,51));x[0,25]=.1;x[1,25]=-.1
        q=a.vector_regions(x)
        self.assertAlmostEqual(q['L1_153'],.2)
        self.assertEqual(q['L1_collapsed_51'],0.)
        self.assertAlmostEqual(q['channel_cancellation_L1'],.2)
        self.assertEqual(q['signed_total'],0.)

    def test_area_normalization_and_zero_denominator(self):
        q=a.vector_regions(np.zeros((3,51)))
        self.assertTrue(all(c['share_of_L1'] is None for c in q['cells']))
        rows=panel();row=rows[0]
        base=np.asarray(row['descriptors']['RO']['post_HB_bins_A2'])
        row['descriptors']['UD']['post_HB_bins_A2']=(2*base).tolist()
        s=dict(rows=rows,paired_integrity_passed=True,classification={'unchanged':True})
        z=a.regional_panel(s)['rows'][0]['regions']
        self.assertAlmostEqual(z['normalized_profile']['total']['L1_153'],0.)
        self.assertGreater(z['area_profile']['total']['L1_153'],0.)

    def test_preserve_R11_labels_and_all_members(self):
        s=dict(rows=panel(),paired_integrity_passed=True,classification={'labels':['inconclusive']})
        original=copy.deepcopy(s);q=a.regional_panel(s)
        self.assertEqual(s,original);self.assertEqual(q['R11_classification'],s['classification'])
        self.assertFalse(q['new_labels']);self.assertEqual(q['model_calls'],0)
        s['rows'].pop()
        with self.assertRaises(ValueError):a.regional_panel(s)

    def test_shapley_of_loss_not_absolute_shapley(self):
        values={c:np.array([-1.+2*int(c[2])]) for c in a.CORNERS}
        pred=a.shapley_three(values)
        gain=-a.shapley_three({k:abs(v) for k,v in values.items()})
        self.assertAlmostEqual(pred.sum(),2.);self.assertAlmostEqual(gain.sum(),0.)
        q=a.error_summary([-1],[1],[0],[0],pred,gain)
        self.assertEqual(q['MAE_removed_O_to_C'],0.)

    def test_full_synthetic_scorecard(self):
        rows,l,x,_=data();d=a.explanatory_scores(rows,l,x)
        self.assertTrue(d['status']['complete'])
        self.assertEqual(len(d['private_rows']),142)
        self.assertEqual(d['aggregate_errors']['pooled']['rows'],142)
        self.assertEqual(d['aggregate_errors']['audit_only_other_rows'],190)
        for z in d['aggregate_errors']['solvents']:
            self.assertAlmostEqual(sum(z['absolute_error_reduction_ShAP'].values()),z['MAE_removed_O_to_C'])

    def test_nonfinite_preserves_denominator(self):
        rows,l,x,_=data();x[0,1]=np.nan;d=a.explanatory_scores(rows,l,x)
        self.assertFalse(d['status']['complete']);self.assertEqual(d['status']['exact_requested'],1278)
        self.assertEqual(d['status']['exact_finite'],1277);self.assertIsNone(d['aggregate_errors'])

    def test_legacy_gate_and_unknown_identity(self):
        rows,l,x,_=data();l[0,0]+=.01
        self.assertFalse(a.explanatory_scores(rows,l,x)['status']['legacy_parity_passed'])
        rows[0]['r3_row_id']=rows[1]['r3_row_id']
        with self.assertRaises(ValueError):a.explanatory_scores(rows,l,x)

    def test_macro_is_not_row_weighted_pool(self):
        rows,l,x,_=data();use=[j for j,z in enumerate([v for v in rows if v['solvent'] in a.GLYCOLS]) if z['solvent'].startswith('MTH')]
        x[use,7]+=1
        q=a.explanatory_scores(rows,l,x)['aggregate_errors']
        self.assertNotAlmostEqual(q['pooled']['C']['MAE'],q['equal_solvent_mean']['C_MAE'])

    def test_negative_and_greater_than_one_recovery_not_clipped(self):
        for c in (-2.,.0):
            vals={k:np.array([1.+(c-1)*int(k[2])]) for k in a.CORNERS}
            phi=a.shapley_three(vals);gain=-a.shapley_three({k:abs(v) for k,v in vals.items()})
            z=a.error_summary([1],[c],[.5],[0],phi,gain)
            self.assertAlmostEqual(z['signed_recovery_fraction'],-2. if c==-2 else 2.)
        z=a.error_summary([1],[1],[1],[0],np.zeros((3,1)),np.zeros((3,1)))
        self.assertIsNone(z['signed_recovery_fraction'])

    def test_public_allowlist_discards_private_fields(self):
        rows,l,x,_=data();d=a.explanatory_scores(rows,l,x)
        d['coordinates']=[[1,2,3]];d['aggregate_errors']['solvents'][0]['private_path']='/secret'
        d['aggregate_errors']['pooled']['dense_profile']=[1]*153
        z=r.public_scores(d);text=json.dumps(z)
        self.assertNotIn('/secret',text);self.assertNotIn('dense_profile',text)
        self.assertNotIn('coordinates',text);self.assertNotIn('private_rows',text)
        self.assertNotIn('prediction_ShAP',text);self.assertNotIn('mean_prediction_shift',text)
        d['aggregate_errors']['pooled']['O']['MAE']=[1,2]
        with self.assertRaises(ValueError):r.public_scores(d)


class Execution(unittest.TestCase):
    def test_mac_guard(self):
        with patch.object(sys,'platform','linux'):
            with self.assertRaises(RuntimeError):r.cross.mac_only()

    def test_identity_alignment_not_row_position(self):
        rows,_,_,_=data();d=pd.DataFrame(rows)
        r.same_rows(d,d.iloc[::-1])
        b=d.copy();b.loc[0,'T']+=1
        with self.assertRaises(ValueError):r.same_rows(d,b)
        b=d.copy();b.loc[0,'solvent']='wrong'
        with self.assertRaises(ValueError):r.same_rows(d,b)

    def test_job_budget(self):
        _,_,_,cases=data();jobs=r.jobs_for(cases)
        self.assertEqual(len(jobs),44)
        self.assertEqual(sum(len(j['case']['rows']) for j in jobs if j['phase']=='legacy'),284)
        self.assertEqual(sum(len(j['case']['rows']) for j in jobs if j['phase']=='exact'),1278)
        with self.assertRaises(ValueError):r.jobs_for(cases[1:])

    def test_private_alias_and_fresh(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);(p/'real').mkdir();(p/'alias').symlink_to(p/'real')
            self.assertEqual(r.private(p/'alias/new'),(p/'real/new').resolve())
            with self.assertRaises(FileExistsError):r.private(p/'real',fresh=True)
            (p/'real/.git').mkdir()
            with self.assertRaises(ValueError):r.private(p/'alias/new')

    def test_process_timeout(self):
        with tempfile.TemporaryDirectory() as t:
            q=r.cross.launch([sys.executable,'-c','import time;time.sleep(10)'],Path(t)/'log',.05,os.environ.copy())
            self.assertEqual(q['execution_state'],'timeout');self.assertNotEqual(q['returncode'],0)

    def fixture_job(self,p,corner='111',phase='exact'):
        p=Path(p);o=np.zeros((3,51));o[0,25]=90;o[1,40]=10
        u=o.copy();u[0,25]=80;u[1,40]=30
        key=next(iter(a.GLYCOLS));meta={'volume [A^3]':80,'standard_INCHIKEY':key}
        for name,ps in [('O',o),('U',u),('S',o)]:write_sigma(p/(name+'.sigma'),a.SIG,ps,meta)
        case=dict(solute='SOLUTE',solvent=key,rows=[dict(r3_row_id='a',T=300.),dict(r3_row_id='b',T=320.)],
            open_solvent=r.src.record(p/'O.sigma'),UD_solvent=r.src.record(p/'U.sigma'),open_solute=r.src.record(p/'S.sigma'))
        cross_profile=u*2
        (p/'run').mkdir();r.write(p/'run/summary.json',dict(rows=[dict(key=key,
            descriptors={'RU':{'post_HB_bins_A2':cross_profile.tolist(),'volume_A3':100.}})]))
        job=dict(case=case,phase=phase,corner=corner)
        m=dict(r11_run=str(p/'run'),smiles={'SOLUTE':'C',key:'OCCO'})
        return job,m

    def test_worker_uses_frozen_solute_and_only_requested_endpoint(self):
        with tempfile.TemporaryDirectory() as t,patch.dict(os.environ,{},clear=False):
            p=Path(t);job,m=self.fixture_job(p);out=p/'out';out.mkdir();seen=[]
            cos=types.ModuleType('zcosmo.cosmosac');mod=types.ModuleType('zcosmo.models');pkg=types.ModuleType('zcosmo');pkg.__path__=[]
            cos.sigma_path=lambda k:Path(os.environ['ZC_SIGMA_OVERRIDE_DIR'])/(k+'.sigma')
            class Toy:
                def lngamma_inf(self,T,i):
                    _,ps,mm=r.replay.read_profile(cos.sigma_path(job['case']['solvent']))
                    _,ss,_=r.replay.read_profile(cos.sigma_path('SOLUTE'))
                    seen.append((T,i,ps.sum(),ss.sum(),mm['volume [A^3]'],os.environ['ZC_R6_ENDPOINT']))
                    return float(ps.sum()+mm['volume [A^3]']/T)
            mod.make_model=lambda *args:Toy()
            with patch.dict(sys.modules,{'zcosmo':pkg,'zcosmo.cosmosac':cos,'zcosmo.models':mod}):
                q=r.one_model_job(job,m,out)
            self.assertTrue(q['completed']);self.assertEqual(q['attempted_model_calls'],2)
            self.assertEqual(seen[0][2:],(220.,100.,100.,'1'))
            self.assertEqual(q['values'][0]['r3_row_id'],'a')
            self.assertEqual(r.sha(p/'S.sigma'),job['case']['open_solute']['sha256'])

    def test_original_P21_archive_preparation_and_receipts(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);archive=root/'AVP';archive.mkdir();op=root/'open';up=root/'UD';op.mkdir();up.mkdir()
            rows,old,_x,cases=data();df=pd.DataFrame(rows)
            df.to_csv(archive/'factorial_rows.csv',index=False)
            r.write(archive/'summary.json',dict(rows=332,finite_all=332))
            ps=np.zeros((3,51));ps[0,25]=100
            for k in {'SOLUTE',*(c['solvent'] for c in cases)}:
                for folder in (op,up):write_sigma(folder/(k+'.sigma'),a.SIG,ps,{'volume [A^3]':80})
            for name in r.TABLES.values():
                z=root/name;z.parent.mkdir(parents=True,exist_ok=True);z.write_text('fixed-table')
            for j,c in enumerate(cases):
                part=archive/f'pair-{j:04d}';part.mkdir();d=df[df.solvent==c['solvent']]
                d.to_csv(part/'rows.csv',index=False)
                rec=dict(open_solvent=r.sha(op/(c['solvent']+'.sigma')),open_solute=r.sha(op/'SOLUTE.sigma'),
                    UD_solvent=r.sha(up/(c['solvent']+'.sigma')),
                    **{k:r.sha(root/v) for k,v in r.TABLES.items()})
                for corner in (*a.CORNERS,'UD'):
                    pd.DataFrame({'r3_row_id':d.r3_row_id,'value':d[corner],'error':''}).to_csv(part/(corner+'.csv'),index=False)
                    r.write(part/(corner+'.csv.inputs.json'),rec)
            with patch.object(r,'ROOT',root):
                rr,cc,files=r.p21_inputs(archive,op,up)
                self.assertEqual(len(rr),332);self.assertEqual(len(cc),13);self.assertGreater(len(files),100)
                # A changed parameter is refused before any model is called.
                (root/next(iter(r.TABLES.values()))).write_text('changed')
                with self.assertRaises(ValueError):r.p21_inputs(archive,op,up)

    def test_parameter_receipt_rejects_changed_original(self):
        # The immutable file-record primitive is used before every evaluation.
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'x';p.write_text('before');rec=r.src.record(p);p.write_text('after')
            with self.assertRaises(ValueError):r.src.verify_record(rec)

    def run_driver(self,base,bad_legacy=False,bad_exact=False):
        base=Path(base);rows,l,x,cases=data();jobs=r.jobs_for(cases)
        plan_dir=base/'plan';plan_dir.mkdir();p=plan_dir/'plan.json'
        m=dict(schema=r.SCHEMA,task='factorial',design=r.canonical(r.DESIGN),rows=rows,jobs=jobs,cases=cases)
        r.write(p,m);out=base/'results';idmap={z['r3_row_id']:i for i,z in enumerate(rows)}
        tx={z['r3_row_id']:i for i,z in enumerate(v for v in rows if v['solvent'] in a.GLYCOLS)}
        used=[]
        def launch(command,log,seconds,env):
            job=next(j for j in jobs if j['id']==command[command.index('--job')+1]);used.append(job['phase'])
            folder=Path(command[command.index('--out')+1]);folder.mkdir()
            j=(('000','UD') if job['phase']=='legacy' else (*a.CORNERS,'UD')).index(job['corner']);vals=[]
            for z in job['case']['rows']:
                value=l[tx[z['r3_row_id']],j] if job['phase']=='legacy' else x[tx[z['r3_row_id']],j]
                if bad_legacy and job['id']=='job-00000':value+=.1
                value=float(value)
                if bad_exact and job['phase']=='exact' and job['id']=='job-00008' and not vals:value=None
                vals.append(dict(r3_row_id=z['r3_row_id'],value=value,error='' if value is not None else 'nonfinite'))
            r.write(folder/'result.json',dict(job=job['id'],plan_sha256=r.sha(p),completed=all(v['value'] is not None for v in vals),
                attempted_model_calls=len(vals),values=vals))
            r.write(folder/'progress.json',dict(attempted_model_calls=len(vals)))
            Path(log).write_text('synthetic model stand-in, not Z0x\n')
            return dict(execution_state='returned',returncode=0 if all(v['value'] is not None for v in vals) else 2,wall_s=.001)
        with patch.object(r.cross,'mac_only'),patch.object(r,'load_plan',return_value=(p,m)),patch.object(r.cross,'launch',side_effect=launch):
            rc=r.run_factorial(argparse.Namespace(plan=str(p),plan_commit='a'*40,out=str(out)))
            if not bad_legacy and not bad_exact:
                self.assertEqual(r.check(argparse.Namespace(plan=str(p),plan_commit='a'*40,run=str(out))),0)
                with self.assertRaises(FileExistsError):
                    r.run_factorial(argparse.Namespace(plan=str(p),plan_commit='a'*40,out=str(base/'retry')))
            d=r.read(out/'summary.json')
        return rc,d,used,p,m,out

    def test_complete_orchestration_and_independent_check(self):
        with tempfile.TemporaryDirectory() as t:
            rc,d,used,p,m,out=self.run_driver(t)
            self.assertEqual(rc,0);self.assertEqual(d['attempted_model_calls'],1562)
            self.assertEqual(len(d['receipts']),44);self.assertTrue(d['status']['complete'])
            bad=r.read(out/'job-00000/result.json');bad['values'][0]['value']+=.1;r.write(out/'job-00000/result.json',bad)
            with patch.object(r,'load_plan',return_value=(p,m)):
                with self.assertRaises(ValueError):r.check(argparse.Namespace(plan=str(p),plan_commit='a'*40,run=str(out)))

    def test_failed_legacy_blocks_every_C_request(self):
        with tempfile.TemporaryDirectory() as t:
            rc,d,used,*_=self.run_driver(t,bad_legacy=True)
            self.assertEqual(rc,2);self.assertNotIn('exact',used)
            self.assertEqual(d['attempted_model_calls'],284)
            self.assertEqual(sum(z['state']=='blocked_legacy_gate' for z in d['receipts']),36)
            self.assertIsNone(d['aggregate_errors'])

    def test_failed_exact_row_retains_other_finite_rows_and_requests(self):
        with tempfile.TemporaryDirectory() as t:
            rc,d,used,*_=self.run_driver(t,bad_exact=True)
            self.assertEqual(rc,2);self.assertEqual(d['attempted_model_calls'],1562)
            self.assertEqual(d['status']['exact_finite'],1277)
            self.assertEqual(d['status']['exact_requested'],1278)
            self.assertIsNone(d['aggregate_errors'])

    def test_private_region_run_and_replay(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);pd=root/'plan';pd.mkdir();p=pd/'plan.json'
            old=root/'old';old.mkdir();s=dict(rows=panel(),paired_integrity_passed=True,
                classification={'old_labels':['inconclusive'], 'eta':.359})
            r.write(old/'summary.json',s)
            m=dict(task='regions',r11_run=str(old));r.write(p,m)
            out=root/'regions'
            with patch.object(r.cross,'mac_only'),patch.object(r,'load_plan',return_value=(p,m)):
                self.assertEqual(r.regions(argparse.Namespace(plan=str(p),plan_commit='a'*40,out=str(out))),0)
                self.assertEqual(r.check(argparse.Namespace(plan=str(p),plan_commit='a'*40,run=str(out))),0)
                self.assertFalse((out/'public-errors.json').exists())
                self.assertEqual(r.read(out/'regions-private.json')['R11_classification'],s['classification'])
                with self.assertRaises(FileExistsError):
                    r.regions(argparse.Namespace(plan=str(p),plan_commit='a'*40,out=str(root/'retry')))
                z=r.read(out/'regions-private.json');z['new_labels']=True;r.write(out/'regions-private.json',z)
                with self.assertRaises(ValueError):r.check(argparse.Namespace(plan=str(p),plan_commit='a'*40,run=str(out)))

    def test_successful_process_does_not_make_nan_a_success(self):
        rows,l,x,_=data();l[10,1]=np.nan
        d=a.explanatory_scores(rows,l,x)
        self.assertFalse(d['status']['complete']);self.assertEqual(d['status']['legacy_requested'],284)


if __name__=='__main__':unittest.main(verbosity=2)
