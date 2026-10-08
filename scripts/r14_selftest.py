"""Portable R14 tests: synthetic arrays/files and mocked model orchestration only."""
from __future__ import annotations
import ast
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
import numpy as np
import r14_dielectric as d
import r14_oracle as o


def query(i, c1='a', c2='b'):
    return dict(c1=c1,c2=c2,T='298.15',x1=str(.02+.9*(i%19)/19),P='100000',
                pred_P='110000',split='test_one',system_id='irrelevant-name')


def reference(cas='7732-18-5',**kw):
    r=dict(CAS=cas,Chemical='fixture',T='298.15',Permittivity='10',A='',B='',C='',D='',Tmin='',Tmax='')
    r.update(kw);return r


def load_base():
    path=d.ROOT/'src/zcosmo/z0x.py'
    if not path.is_file():raise unittest.SkipTest('verified current z0x source not available')
    require_blob='c558d4e95db9b78f3b57d6a103a293e21feeb9af'
    if d.blob(path.read_bytes())!=require_blob:raise AssertionError('test requires the reviewed z0x Git blob')
    cosmos=types.ModuleType('zcosmo.cosmosac');models=types.ModuleType('zcosmo.models');zm=types.ModuleType('zcosmo.zmodel')
    class P:
        aeff=7.25
        def __init__(self,c=1.):self.A_ES=c
        def with_(self,**kw):return P(kw['A_ES'])
    class Mix:
        def __init__(self,keys,prm):
            self.prm=prm;self.A=np.array([1.,2.]);self.fl=[]
            for i in range(2):
                p=np.zeros((3,51));p[0,5+30*i]=self.A[i]
                self.fl.append(types.SimpleNamespace(key=keys[i],psigA=p))
        def _E(self,T):return np.ones((153,153))
        def lngamma_comb(self,x):return np.zeros(2)
        def lngamma_disp(self,x,T):return np.zeros(2)
        def lngamma(self,T,x):return np.array([self.prm.A_ES,-self.prm.A_ES])
    cosmos.Mixture=Mix;cosmos.load_fluid=lambda k:types.SimpleNamespace(V=1.)
    cosmos.solve_gamma=lambda e,p:np.ones(153);cosmos._pure_lnG=lambda *a:np.zeros(153)
    cosmos.SIG=np.linspace(-.025,.025,51);cosmos.R_KCAL=.001987
    models.load_z_params=lambda n:P();models.ROOT=d.ROOT
    zm.c_es_theory=lambda fpol=1.:12000*fpol
    spec=importlib.util.spec_from_file_location('r14_test_z0x',path);mod=importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules,{'zcosmo.cosmosac':cosmos,'zcosmo.models':models,'zcosmo.zmodel':zm}):
        spec.loader.exec_module(mod)
    return mod


class Physics(unittest.TestCase):
    def test_f_monotonic_and_saturation(self):
        f=d.screening([1,2,10,100,1e12]);self.assertTrue(np.all(np.diff(f)>0));self.assertAlmostEqual(f[0],0)
        self.assertLess(f[-1],1)
    def test_f_derivative(self):
        x=24.447;h=1e-3;fd=(d.screening(x+h)-d.screening(x-h))/(2*h)
        self.assertAlmostEqual(fd,1.5/(x+.5)**2,places=10)
    def test_water_coefficient_not_epsilon_fraction(self):
        s=d.sensitivity(52.93798366132173,78.)
        self.assertGreater(s['delta_f'],0);self.assertLess(s['relative_coefficient_change'],.01)
    def test_bad_epsilon(self):
        for e in (np.nan,np.inf,0.5):
            with self.assertRaises(ValueError):d.screening(e)
    def test_kf_zero_dipole(self):self.assertAlmostEqual(d.kf_epsilon(0,50,2.4,3),2.4)
    def test_kf_g_monotonic(self):
        self.assertLess(d.kf_epsilon(2,50,2,1),d.kf_epsilon(2,50,2,2))
    def test_kf_temperature(self):
        self.assertGreater(d.kf_epsilon(2,50,2,1,280),d.kf_epsilon(2,50,2,1,330))
    def test_kf_input_rejected(self):
        with self.assertRaises(ValueError):d.kf_epsilon(2,-1,2,1)
    def test_pressure_units(self):self.assertAlmostEqual(o.pressure([0,0],.25,[1e5,2e5]),175000)
    def test_pressure_nonfinite(self):
        with self.assertRaises(ValueError):o.pressure([np.nan,0],.5,[1,1])


class Ingredient(unittest.TestCase):
    def test_CAS_checksum(self):
        self.assertTrue(d.cas_valid('7732-18-5'));self.assertTrue(d.cas_valid('67-56-1'))
        self.assertFalse(d.cas_valid('7732-18-4'));self.assertFalse(d.cas_valid('water'))
    def test_polynomial_range(self):
        r=reference(A='20',B='-0.01',Tmin='290',Tmax='310')
        self.assertAlmostEqual(d.reference_at(r)[0],17.0185)
    def test_no_extrapolation(self):
        r=reference(A='20',B='-.01',Tmin='280',Tmax='290',T='293.15')
        self.assertIsNone(d.reference_at(r)[0])
    def test_exact_temperature_point(self):
        self.assertEqual(d.reference_at(reference())[0],10.)
        self.assertIsNone(d.reference_at(reference(T='293.15'))[0])
    def test_invalid_polynomial(self):
        with self.assertRaises(ValueError):d.reference_at(reference(A='-1',B='0',Tmin='290',Tmax='310'))
    def test_exact_join(self):
        rr=d.ingredient_rows([dict(inchikey='K',eps='8')],[dict(inchikey='K',cas='7732-18-5')],[reference()])
        self.assertEqual(rr[0]['status'],'matched')
    def test_stereo_ambiguity(self):
        rr=d.ingredient_rows([dict(inchikey='K',eps='8')],
           [dict(inchikey='K',cas='7732-18-5'),dict(inchikey='K2',cas='7732-18-5')],[reference()])
        self.assertEqual(rr[0]['status'],'invalid_or_stereochemically_ambiguous_CAS')
    def test_duplicates_refused(self):
        with self.assertRaises(ValueError):d.ingredient_rows([dict(inchikey='K',eps='8')]*2,[],[])
        with self.assertRaises(ValueError):d.ingredient_rows([],[],[reference(),reference()])
    def test_nonfinite_explicit(self):
        rr=d.ingredient_rows([dict(inchikey='K',eps='nan')],[dict(inchikey='K',cas='7732-18-5')],[reference()])
        self.assertEqual(rr[0]['status'],'invalid_stored_epsilon')
        with self.assertRaises(ValueError):d.metrics([1,np.nan],[1,2])
    def test_metrics(self):
        m=d.metrics([2,4],[2,4]);self.assertEqual(m['mean_abs_f_error'],0);self.assertEqual(m['mean_abs_log_epsilon'],0)
    def test_future_pilot_gate(self):
        rows=[dict(key=k,status='matched',stored_epsilon=10.,reference_epsilon=20.) for k in d.PILOT]
        c=[dict(key=k,eps=20.,sampling_gate_passed=True,dipole_gate_passed=True) for k in d.PILOT]
        self.assertTrue(d.candidate_gate(rows,c)['passed'])
        c[0]['dipole_gate_passed']=False
        with self.assertRaises(ValueError):d.candidate_gate(rows,c)
    def test_missing_pilot_member(self):
        with self.assertRaises(ValueError):d.candidate_gate([],[])


class Oracle(unittest.TestCase):
    def test_selection_counts_and_budget(self):
        rows=[query(i,f'K{i//20}','b') for i in range(2200)]
        ref={r['c1']:10 for r in rows};ref['b']=2
        got,c=o.select(rows,ref)
        self.assertEqual(len(got),1000);self.assertEqual(c['selected_systems'],100)
        self.assertEqual(3*len(got),o.DESIGN['max_model_calls'])
    def test_selection_ignores_observed_error(self):
        rows=[query(i) for i in range(20)]
        a,_=o.select(rows,{'a':10,'b':2})
        rows[0]['P']='9e20';rows[0]['pred_P']='1e-3'
        b,_=o.select(rows,{'a':10,'b':2})
        self.assertEqual([r['row_id'] for r in a],[r['row_id'] for r in b])
    def test_unknown_refs_are_exclusions(self):
        rows=[query(0),query(1,'missing','b')];r,c=o.select(rows,{'a':10,'b':2})
        self.assertEqual(len(r),1);self.assertEqual(c['excluded']['missing_exact_reference_identity'],1)
    def test_pure_endpoints_excluded(self):
        r=query(0);r['x1']='0';rows=[r,query(1)]
        g,c=o.select(rows,{'a':10,'b':2});self.assertEqual(len(g),1)
    def test_preserve_nonfinite(self):
        rows,_=o.select([query(0)],{'a':10,'b':2})
        s=o.error_summary(rows,[[1e5,np.nan,1e5]])
        self.assertFalse(s['status']['complete']);self.assertIsNone(s['aggregate_errors'])
        self.assertEqual(s['status']['requested_rows'],1)
    def test_gain_and_residual(self):
        rows,_=o.select([query(0)],{'a':10,'b':2})
        s=o.error_summary(rows,[[120000,110000,100000]])['aggregate_errors']
        self.assertAlmostEqual(s['signed_gap_recovery'],.5)
        self.assertAlmostEqual(s['oracle_minus_baseline_pp']+s['baseline_minus_cosmosac2010_pp'],s['oracle_minus_cosmosac2010_pp'])
    def test_recovery_not_clipped(self):
        rows,_=o.select([query(0)],{'a':10,'b':2})
        q=o.error_summary(rows,[[120000,140000,100000]])['aggregate_errors']
        self.assertAlmostEqual(q['signed_gap_recovery'],-1)
    def test_zero_gap_ratio_unavailable(self):
        rows,_=o.select([query(0)],{'a':10,'b':2})
        q=o.error_summary(rows,[[120000,100000,120000]])['aggregate_errors']
        self.assertIsNone(q['signed_gap_recovery'])
    def test_anchor_gate(self):
        rows,_=o.select([query(0)],{'a':10,'b':2})
        self.assertTrue(o.anchor_pass(rows,[110000])['passed'])
        self.assertFalse(o.anchor_pass(rows,[110001])['passed'])
    def test_source_mutation(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'source';p.write_text('one');fp=d.fingerprint([p]);d.check_inputs(fp)
            p.write_text('two')
            with self.assertRaises(ValueError):d.check_inputs(fp)
    def test_exclusive_output(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'out.json';d.write(p,dict(ok=True))
            with self.assertRaises(FileExistsError):d.write(p,dict(ok=False))
    def test_private_git_path(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);(root/'.git').mkdir()
            with self.assertRaises(ValueError):d.private(root/'out')
    def test_exposure_never_claims_new_holdout(self):
        e=d.exposure_receipt('fixture');self.assertFalse(e['may_claim_unexposed']);self.assertFalse(e['may_adopt'])


class ActualSourceDispatch(unittest.TestCase):
    def test_override_updates_composition_screening(self):
        m=load_base();b=m.Z0xBinary.__new__(m.Z0xBinary);b.V=np.array([1.,2.]);b.eps=np.array([10.,2.])
        c=b._c(.4);der=(b._c(.40001)-b._c(.39999))/.00002
        b.eps=np.array([20.,3.]);self.assertNotEqual(c,b._c(.4))
        self.assertNotEqual(der,(b._c(.40001)-b._c(.39999))/.00002)
    def test_analytic_branch_reads_replaced_epsilon(self):
        m=load_base();b=m.Z0xBinary.__new__(m.Z0xBinary)
        b.V=np.array([1.,2.]);b.keys=['a','b'];b.z0=m.load_z_params('Z0');b.eps=np.array([10.,2.])
        old=b._analytic(298.15,.4);b.eps=np.array([20.,3.]);new=b._analytic(298.15,.4)
        self.assertGreater(np.max(abs(old-new)),0)
    def test_observed_subclass_dispatch_limitation(self):
        m=load_base()
        class Extension(m.Z0xBinary):
            def _g(self,T,x):return x*(1-x)
        b=Extension.__new__(Extension);b._analytic=lambda T,x:np.zeros(2);b._endpoint=lambda T,x:np.zeros(2)
        self.assertTrue(np.array_equal(b.lngamma(298.15,[.4,.6]),[0,0]))
        with patch.dict(os.environ,{'ZC_R6_ENDPOINT':'1'}):self.assertEqual(b.lngamma_inf(298.15),0.)
        with patch.dict(os.environ,{'ZC_R6_ENDPOINT':'0'}):self.assertGreater(b.lngamma_inf(298.15),.99)
        # This documents a base-class extension hazard, not correct association physics.



class Orchestration(unittest.TestCase):
    """Exercise the real driver and archive checker with mocked model workers."""
    def fixture(self, folder):
        root=Path(folder);plan=root/'plan.json';run=root/'run'
        d.write(plan,{'private_fixture':True})
        rows=[dict(row_id='row-0',c1='A',c2='B',system='A|B',T=298.15,x1=.4,
                   P=100.,archived_pred_P=120.,psat=[120.,80.])]
        jobs=[dict(id=f'job-{i:04d}',arm=arm,keys=['A','B'],indices=[0]) for i,arm in enumerate(o.ARMS)]
        manifest=dict(rows=rows,jobs=jobs,exposure=d.exposure_receipt('a'*40),
                      census={'eligible_rows':1,'selected_rows':1})
        return plan,run,manifest

    def execute(self, folder, bad_anchor=False, missing=False):
        p,out,m=self.fixture(folder);seen=[]
        def fake_launch(command, log, seconds, env):
            jid=command[command.index('--job')+1];job=next(j for j in m['jobs'] if j['id']==jid)
            dest=Path(command[command.index('--out')+1]);dest.mkdir();seen.append(job['arm'])
            d.write(dest/'attempt-0000.json',{'row_id':'row-0','attempted':True})
            value={'baseline':121. if bad_anchor else 120.,'experimental_epsilon_298':105.,'cosmosac2010':110.}[job['arm']]
            if not (missing and job['arm']=='experimental_epsilon_298'):
                d.write(dest/'result.json',dict(job=jid,plan_sha256=d.sha(p),arm=job['arm'],requested=1,
                    attempted=1,values=[dict(row_id='row-0',value=value,error=None)]))
            return dict(state='returned',returncode=0,wall_s=.001)
        args=argparse.Namespace(plan=str(p),plan_commit='synthetic',out=str(out))
        with patch.object(o,'load',return_value=(p,m)),patch.object(d,'private',side_effect=lambda v,fresh=False: self.private(v,fresh)),patch.object(o,'launch',side_effect=fake_launch):
            rc=o.run(args)
        return rc,p,out,m,seen

    @staticmethod
    def private(v,fresh=False):
        p=Path(v).resolve()
        if fresh:p.mkdir()
        return p

    def test_complete_run_and_repeated_readonly_check(self):
        with tempfile.TemporaryDirectory() as t:
            rc,p,out,m,seen=self.execute(t)
            self.assertEqual(rc,0);self.assertEqual(seen,list(o.ARMS))
            q=d.read(out/'summary.json');self.assertEqual(q['attempted_model_calls'],3)
            self.assertTrue(q['status']['complete'])
            with patch.object(o,'load',return_value=(p,m)),patch.object(d,'private',side_effect=self.private):
                for _ in range(2):o.check(argparse.Namespace(plan=str(p),plan_commit='synthetic',run=str(out)))
            public=d.read(out/'public-errors.json')
            self.assertNotIn('receipts',public);self.assertNotIn('rows',public)

    def test_failed_anchor_blocks_all_new_arms(self):
        with tempfile.TemporaryDirectory() as t:
            rc,p,out,m,seen=self.execute(t,bad_anchor=True)
            self.assertEqual(rc,2);self.assertEqual(seen,['baseline'])
            q=d.read(out/'summary.json');self.assertFalse(q['status']['complete']);self.assertEqual(q['attempted_model_calls'],1)
            self.assertEqual(d.read(out/'job-0001.terminal.json')['state'],'blocked_anchor')

    def test_missing_result_keeps_requested_denominator(self):
        with tempfile.TemporaryDirectory() as t:
            rc,p,out,m,seen=self.execute(t,missing=True)
            self.assertEqual(rc,2);q=d.read(out/'summary.json')
            self.assertEqual(q['status']['requested_rows'],1);self.assertEqual(q['attempted_model_calls'],3)
            self.assertIsNone(q['aggregate_errors'])

    def test_permanent_claim_blocks_second_run(self):
        with tempfile.TemporaryDirectory() as t:
            _,p,out,m,_=self.execute(t)
            with patch.object(o,'load',return_value=(p,m)),patch.object(d,'private',side_effect=self.private):
                with self.assertRaises(FileExistsError):
                    o.run(argparse.Namespace(plan=str(p),plan_commit='synthetic',out=str(out.parent/'other')))

    def test_changed_worker_result_is_detected(self):
        with tempfile.TemporaryDirectory() as t:
            _,p,out,m,_=self.execute(t)
            result=out/'job-0001/result.json';q=d.read(result);q['values'][0]['value']=104.
            result.write_text(__import__('json').dumps(q))
            with patch.object(o,'load',return_value=(p,m)),patch.object(d,'private',side_effect=self.private):
                with self.assertRaises(ValueError):o.check(argparse.Namespace(plan=str(p),plan_commit='synthetic',run=str(out)))

    def test_real_process_timeout_without_chemistry(self):
        with tempfile.TemporaryDirectory() as t:
            got=o.launch([sys.executable,'-c','import time;time.sleep(10)'],Path(t)/'log',.05,dict(os.environ))
            self.assertEqual(got['state'],'timeout');self.assertNotEqual(got['returncode'],0)

    def test_existing_pressure_api_is_key_based_and_kpa(self):
        self.assertEqual(o.DESIGN['pressure_unit'],'kPa')
        self.assertAlmostEqual(o.pressure([0.,0.],.4,[120.,80.]),96.)
        source=Path(o.__file__).read_text()
        self.assertIn('from zcosmo.scope import psat',source)
        self.assertIn("float(psat(k,r['T']))",source)
        self.assertNotIn('vapor_pressure(',source)

if __name__=='__main__':unittest.main(verbosity=2)
