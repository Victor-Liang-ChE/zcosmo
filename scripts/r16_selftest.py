"""Portable R16 tests. Synthetic inputs only; no module-cache clearing.

The real current segment solver and the unchanged Z0x class AST are used for
numerical tests, with synthetic profile/table providers. Mac/file/Git checks
in driver tests are mocked explicitly. No scientific acceptance is implied.
"""
from __future__ import annotations
import argparse
import ast
from contextlib import contextmanager
from dataclasses import replace
import hashlib
import itertools
import math
import json
import os
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch
import numpy as np
from scipy import linalg  # Import once, not through a restored module dictionary.
import r16_london as law
import r16_stats as st
import r16_review as run
from zcosmo import cosmosac as cs

ROOT=Path(__file__).resolve().parents[1]


def pair(volumes=(45.,130.),c6=(400.,3600.),alpha=(30.,100.)):
    return law.LondonPair(c6,alpha,volumes)


def profile(path,V=45.):
    p=np.zeros((3,51));p[0,10]=30.;p[0,35]=40.;p[1,12]=15.;p[2,40]=15.
    text='# meta: '+json.dumps({'volume [A^3]':V})+'\n'
    text+=''.join(f'{s:.3f} {v:.15e}\n' for s,v in zip(np.tile(cs.SIG,3),p.ravel()))
    Path(path).write_text(text)


@contextmanager
def actual_model(volumes=(45.,130.)):
    p=cs.Params(A_ES=12226.235339788673,B_ES=0.,c_OH_OH=5712.229463082564,
                c_OT_OT=5611.4027535161395,c_OH_OT=5987.642651646004,
                disp_mode='london',w_dsp=1.)
    a=np.zeros((3,51));a[0,14]=20;a[0,29]=20;a[1,12]=5;a[2,41]=5
    b=np.zeros((3,51));b[0,18]=35;b[0,36]=45;b[1,11]=10;b[2,39]=10
    fluids={k:cs.Fluid(k,v,float(v.sum()),V,'NHB',1.,{}) for k,v,V in zip(('A','B'),(a,b),volumes)}
    tab={'A':(400.,30.),'B':(3600.,100.)}
    path=ROOT/'src/zcosmo/z0x.py';tree=ast.parse(path.read_text())
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Z0xBinary')
    ns=dict(np=np,os=os,Mixture=lambda keys,prm:cs.Mixture(keys,prm,fluids=[fluids[k] for k in keys]),
            solve_gamma=cs.solve_gamma,_pure_lnG=cs._pure_lnG,SIG=cs.SIG,R_KCAL=cs.R_KCAL,
            load_fluid=lambda k:fluids[k],load_z_params=lambda name:p,
            _eps=lambda:{'A':2.5,'B':31.},c_es_theory=lambda fpol:12226.235339788673*fpol)
    exec(compile(ast.Module(body=[cls],type_ignores=[]),str(path),'exec'),ns)
    with patch.object(cs,'_london_table',return_value=tab),patch.dict(os.environ,{'ZC_R6_ENDPOINT':'1'}):
        yield ns['Z0xBinary'](['A','B']),fluids,p


class Algebra(unittest.TestCase):
    def test_source_blobs(self):
        for rel,expected in [('src/zcosmo/cosmosac.py','c226a668b7b9dba9e7400cda180fafd8faa700f3'),
                             ('src/zcosmo/z0x.py','c558d4e95db9b78f3b57d6a103a293e21feeb9af')]:
            b=(ROOT/rel).read_bytes()
            self.assertEqual(hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest(),expected)

    def test_decomposition_random(self):
        rng=np.random.default_rng(16)
        for _ in range(100):
            p=pair(tuple(rng.uniform(20,400,2)),tuple(np.exp(rng.uniform(3,10,2))),tuple(rng.uniform(10,200,2)))
            d=p.old_audit()
            self.assertGreaterEqual(min(d['components_kcal'].values()),0.)
            self.assertAlmostEqual(d['w_kcal'],sum(d['components_kcal'].values()),places=10)
            self.assertGreaterEqual(d['w_kcal'],-1e-12)

    def test_current_formula_reference(self):
        p=pair();f=[types.SimpleNamespace(key=k,V=v) for k,v in zip(('A','B'),p.volumes)]
        tab={k:v for k,v in zip(('A','B'),zip(p.c6,p.alpha))}
        with patch.object(cs,'_london_table',return_value=tab):
            self.assertAlmostEqual(p.old_audit()['w_kcal'],cs.london_pair_w(*f,'synthetic'),places=13)

    def test_identical_species(self):
        p=pair((90.,90.),(1600.,1600.),(60.,60.))
        for v in p.old_audit()['components_kcal'].values():self.assertAlmostEqual(v,0.,places=13)
        a,b=law.DispersionChange(p).terms(300.,[.23,.77])
        np.testing.assert_allclose(a,0.,atol=1e-12);np.testing.assert_allclose(b,0.,atol=1e-12)

    def test_equal_volumes_recover_original(self):
        c=law.DispersionChange(pair((80.,80.)))
        for x in (0.,.05,.5,.99,1.):
            for T in (250.,298.15,450.):np.testing.assert_allclose(*c.terms(T,[x,1-x]),rtol=1e-12,atol=1e-12)

    def test_exchange_symmetry(self):
        p=pair();q=law.LondonPair(p.c6[::-1],p.alpha[::-1],p.volumes[::-1])
        c,d=law.DispersionChange(p),law.DispersionChange(q)
        for x in (0.,.17,.6,1.):
            np.testing.assert_allclose(c.terms(333.,[x,1-x])[1],d.terms(333.,[1-x,x])[1][::-1],atol=1e-13)

    def test_derivative_of_total_excess_energy(self):
        c=law.DispersionChange(pair());T=317.;x=.36;h=1e-5
        def g(t):return c.energies([t,1-t])[1]/(law.R_KCAL*T)
        slope=(g(x+h)-g(x-h))/(2*h)
        np.testing.assert_allclose(c.terms(T,[x,1-x])[1],[g(x)+(1-x)*slope,g(x)-x*slope],atol=2e-8,rtol=0)

    def test_gibbs_duhem(self):
        c=law.DispersionChange(pair());x=.42;h=1e-6
        d=(c.terms(310.,[x+h,1-x-h])[1]-c.terms(310.,[x-h,1-x+h])[1])/(2*h)
        self.assertLess(abs(np.dot([x,1-x],d)),1e-7)

    def test_infinite_dilution_asymmetry(self):
        c=law.DispersionChange(pair());T=300.
        self.assertAlmostEqual(c.terms(T,[0.,1.])[1][0]/c.terms(T,[1.,0.])[1][1],45./130.,places=12)
        self.assertEqual(c.terms(T,[0.,1.])[1][1],0.)

    def test_temperature_and_enthalpy(self):
        c=law.DispersionChange(pair());x=np.array([.3,.7]);T=333.;h=.5
        exact=c.energies(x)[1]*8.314462618/law.R_KCAL
        v=-(8.314462618*T*T)*x@(c.terms(T+h,x)[1]-c.terms(T-h,x)[1])/(2*h)
        self.assertAlmostEqual(v/exact,T*T/(T*T-h*h),places=10)

    def test_not_a_uniform_downweight(self):
        c=law.DispersionChange(pair((40.,320.),(100.,6400.),(20.,160.)))
        a,b=c.terms(300.,[.5,.5]);self.assertGreater(b[0],a[0]);self.assertLess(b[1],a[1])
        self.assertGreater(c.energies([.5,.5])[1],c.energies([.5,.5])[0])

    def test_old_pressure_monotone(self):
        c=law.DispersionChange(pair());old,_=c.terms(300.,[.4,.6]);lg=np.array([-.3,.5])
        self.assertGreater(run.r14.pressure(lg+old,.4,[80.,120.]),run.r14.pressure(lg,.4,[80.,120.]))

    def test_stencil_strip(self):
        c=law.DispersionChange(pair());T=300.;h=1e-4
        for x in (0.,.00002,.0001,.9999,.99998,1.):
            lo=max(0.,x-h);hi=min(1.,x+h)
            def f(v):a,b=c.energies([v,1-v]);return (b-a)/(law.R_KCAL*T)
            slope=(f(hi)-f(lo))/(hi-lo);v=f(x)
            np.testing.assert_allclose(c.delta(T,[x,1-x],h,False),[v+(1-x)*slope,v-x*slope],atol=1e-12)

    def test_invalid_inputs_fail(self):
        for vals in ((0.,10.),(-1.,10.),(np.nan,10.),(np.inf,10.),(1.,)):
            with self.assertRaises(ValueError):pair(c6=vals)
        c=law.DispersionChange(pair())
        for T,x in ((0,[.5,.5]),(np.nan,[.5,.5]),(300,[-.1,1.1]),(300,[.3,.6])):
            with self.assertRaises(ValueError):c.terms(T,x)

    def test_no_factor_two_error_in_c6_sum(self):
        atomic=np.array([[1.,2.],[2.,4.]])
        mol=atomic.sum();two_copies=sum(atomic[i,j] for i in range(2) for j in range(2))
        self.assertEqual(mol,two_copies);self.assertNotEqual(mol,np.triu(atomic,1).sum())

    def test_actual_model_equal_size(self):
        with actual_model((80.,80.)) as (base,fl,p):
            m=law.PairedLondon(base,pair((80.,80.)))
            for x in (0.,.00002,.4,.99998,1.):
                old,new=m.paired(330.,[x,1-x]);np.testing.assert_allclose(old,new,atol=2e-11,rtol=0)

    def test_actual_model_preserves_residual_and_derivative(self):
        with actual_model() as (base,fl,p):
            m=law.PairedLondon(base,pair());T=325.;x=.37;h=2e-4
            def g(t):
                mix=cs.Mixture(['A','B'],p.with_(A_ES=base._c(t),disp_mode='none',use_dsp=False),fluids=list(fl.values()))
                return float(np.dot([t,1-t],mix.lngamma(T,[t,1-t])))+m.change.energies([t,1-t])[1]/(law.R_KCAL*T)
            gp=(g(x-2*h)-8*g(x-h)+8*g(x+h)-g(x+2*h))/(12*h)
            np.testing.assert_allclose(m.lngamma(T,[x,1-x]),[g(x)+(1-x)*gp,g(x)-x*gp],atol=3e-6,rtol=0)

    def test_actual_endpoints_and_strip(self):
        with actual_model() as (base,fl,p):
            m=law.PairedLondon(base,pair());T=310.
            for flag,x in itertools.product(('0','1'),(0.,.00003,.99997,1.)):
                with patch.dict(os.environ,{'ZC_R6_ENDPOINT':flag}):
                    if x in (0.,1.) and flag=='1':
                        pure=cs.Mixture(['A','B'],p.with_(A_ES=base._c(x),disp_mode='none'),fluids=list(fl.values()))
                        expected=pure.lngamma(T,[x,1-x])+m.change.terms(T,[x,1-x])[1]
                    else:
                        def g(t):
                            mix=cs.Mixture(['A','B'],p.with_(A_ES=base._c(t),disp_mode='none'),fluids=list(fl.values()))
                            return np.dot([t,1-t],mix.lngamma(T,[t,1-t]))+m.change.energies([t,1-t])[1]/(law.R_KCAL*T)
                        lo=max(x-base.H,0);hi=min(x+base.H,1);dg=(g(hi)-g(lo))/(hi-lo)
                        expected=[g(x)+(1-x)*dg,g(x)-x*dg]
                    np.testing.assert_allclose(m.lngamma(T,[x,1-x]),expected,atol=2e-8,rtol=0)

    def test_one_baseline_call_for_two_arms(self):
        with actual_model() as (base,fl,p):
            m=law.PairedLondon(base,pair())
            with patch.object(base,'lngamma',wraps=base.lngamma) as call:m.paired(300.,[.4,.6]);self.assertEqual(call.call_count,1)


class Accounting(unittest.TestCase):
    def test_grid_union_is_exact(self):
        union=st.grid_union()
        for g in st.grids():np.testing.assert_array_equal(union[np.searchsorted(union,g)],g)
        self.assertLess(len(union),sum(map(len,st.grids())))

    def test_convex_and_nonconvex(self):
        x=st.grid_union();ideal=np.zeros((len(x),2))
        self.assertFalse(st.detection(ideal)['detected'])
        regular=np.c_[4*(1-x)**2,4*x*x]
        self.assertTrue(st.detection(regular)['detected'])

    def test_disagreement_is_inconclusive(self):
        x=st.grid_union()
        with patch.object(st,'hull_gap',side_effect=[(False,0.),(True,1e-5)]):
            self.assertIsNone(st.detection(np.zeros((len(x),2)))['detected'])

    def test_error_sign_and_system_weighting(self):
        a=st.paired_summary([100.,100.,100.],[[90.,110.],[80.,90.],[120.,110.]],['a','a','b'],'s',True)
        self.assertAlmostEqual(a['baseline'],50/3);self.assertAlmostEqual(a['candidate'],10.)
        self.assertEqual(a['improved'],2);self.assertEqual(a['worsened'],0)
        self.assertAlmostEqual(a['equal_system'][0],17.5)

    def test_bootstrap_repeats_without_new_rng_state(self):
        args=([0.,1.],[[2.,1.],[3.,2.]],['a','b'],'idac')
        self.assertEqual(st.paired_summary(*args),st.paired_summary(*args))

    def test_lle_guard_counts(self):
        p=[('p',True,True),('p',False,True),('q',False,False)]
        n=[('n',True,False),('m',False,False)]
        a=st.lle_summary(p,n);self.assertEqual(a['recall'],[0.,.5]);self.assertEqual(a['false_positive_rate'],[.5,0.])

    def test_uncertain_is_not_false(self):
        with self.assertRaises(ValueError):st.lle_summary([('p',True,None)],[('n',False,False)])

    def test_no_finite_subset(self):
        with self.assertRaises(ValueError):st.paired_summary([1.],[[1.,np.nan]],['a'],'idac')

    def test_no_worsening_gates(self):
        a={'change':-1.,'delta_one_sided_upper95':-.5}
        s=dict(vle=a,idac=dict(a),he=dict(a),lle=dict(recall=[.8,.8],false_positive_rate=[.1,.1],
            balanced_accuracy=[.85,.85],recall_change_lower95=0.,false_positive_change_upper95=0.,
            balanced_accuracy_change_lower95=0.))
        self.assertTrue(st.gates(s)['passed']);s['he']['change']=.01;self.assertFalse(st.gates(s)['passed'])

    def test_round15_bias_contrast_is_not_shapley(self):
        self.assertAlmostEqual(-2.79-1.44,-4.23)
        self.assertGreater(abs((-2.79-1.44)-(-4.47)),.02)


class InputTests(unittest.TestCase):
    def test_profile_units_and_validation(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'f.sigma';profile(p,83.);self.assertEqual(run.read_profile(p),83.)
            text=p.read_text().replace('83.0','-83.0');p.write_text(text)
            with self.assertRaises(ValueError):run.read_profile(p)

    def test_csv_scope_is_input_only(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'idac.csv';p.write_text('solute,solvent,T,ln_gamma_inf,split,has_sigma\nA,B,300,1,test_one,True\nC,B,300,2,test_both,True\nA,B,300,3,train,True\n')
            rows,c=run.guard_rows(p,'idac',lambda k:'descriptor' if k=='C' else None)
            self.assertEqual(len(rows),1);self.assertEqual(c['original_rows'],3);self.assertEqual(len(c['exclusions']),2)

    def test_bad_original_response_is_not_dropped(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'idac.csv';p.write_text('solute,solvent,T,ln_gamma_inf,split\nA,B,300,nan,test_one\n')
            with self.assertRaises(ValueError):run.guard_rows(p,'idac',lambda k:None)

    def test_negative_identity_count(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'n.csv';p.write_text('c1,c2,T,split\nA,B,300,test_one\n')
            with self.assertRaises(ValueError):run.guard_rows(p,'negative',lambda k:None)

    def test_duplicate_descriptor_identity(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);p=root/'results/qc';p.mkdir(parents=True)
            (p/'dispersion.csv').write_text('inchikey,C6_au,alpha_au\nA,100,20\nA,200,30\n')
            with patch.object(run,'ROOT',root):
                with self.assertRaises(ValueError):run.table_inputs()

    def test_queries_have_declared_derivative_cost(self):
        t=dict(kind='he',members=[dict(row_id='he:0',T=300.,x1=.3)])
        q=run.queries(t);self.assertEqual([v['T'] for v in q],[299.5,300.5])

    def test_private_output_rejects_checkout(self):
        with self.assertRaises(ValueError):run.d.private(ROOT/'data/private')


def fixture():
    keys=['A','B'];p=pair();change=law.DispersionChange(p)
    vle=[dict(row_id='42',keys=keys,T=300.,x1=.4,truth=100.,P=100.,psat=[100.,100.],system='A|B',reference_P=95.,expected_P=0.)]
    # A deterministic physically separable fake source, not a molecular model.
    def model(T,x):return change.terms(T,x)[0]+np.array([.1*x[1]**2,.1*x[0]**2])
    vle[0]['expected_P']=run.r14.pressure(model(300.,np.array([.4,.6])),.4,[100.,100.])
    guards={
      'idac':[dict(row_id='idac:0',keys=keys,T=300.,x1=0.,truth=.5,system='A|B')],
      'he':[dict(row_id='he:0',keys=keys,T=300.,x1=.4,truth=100.,system='A|B')],
      'positive':[dict(row_id='positive:0',keys=keys,T=300.,system='A|B')],
      'negative':[dict(row_id='negative:0',keys=keys,T=320.,system='A|B')]}
    tasks=run.tasks_for(vle,guards)
    m=dict(tasks=tasks,pairs={'A|B':dict(c6=list(p.c6),alpha=list(p.alpha),volumes=list(p.volumes))},
           inputs={},worker_inputs={},profiles={},baseline_requests=sum(len(t['queries']) for t in tasks))
    raw={t['id']:np.array([model(q['T'],np.array([q['x1'],1-q['x1']])) for q in t['queries']]) for t in tasks}
    return m,raw


class DriverTests(unittest.TestCase):
    def driver(self,td,bad_anchor=False,missing=False,timeout=False):
        m,raw=fixture();root=Path(td);p=root/'plan.json';run.d.write(p,m);out=root/'output';used=[]
        def launch(cmd,log,seconds,env):
            jid=cmd[cmd.index('--job')+1];t=next(t for t in m['tasks'] if t['id']==jid)
            folder=Path(cmd[cmd.index('--out')+1]);folder.mkdir();used.append(t['kind']);values=[]
            for j,q in enumerate(t['queries']):
                run.d.write(folder/f'attempt-{j:05d}.json',dict(query_id=q['query_id'],attempted=True))
                value=(raw[jid][j]+(.1 if bad_anchor and t['kind']=='vle' else 0)).tolist()
                if missing and t['kind']=='he' and j==0:value=None
                values.append(dict(query_id=q['query_id'],lngamma=value,error=None))
                if timeout and t['kind']=='he':return dict(state='timeout',returncode=-9)
            run.d.write(folder/'result.json',dict(job=jid,plan_sha256=run.d.sha(p),values=values))
            return dict(state='returned',returncode=0)
        a=argparse.Namespace(plan=str(p),plan_commit='f'*40,out=str(out))
        with patch.object(run,'load',return_value=(p,m)),patch.object(run.r14,'launch',side_effect=launch):
            rc=run.run(a)
            self.assertEqual(run.check(argparse.Namespace(plan=str(p),plan_commit='f'*40,run=str(out))),rc)
        return rc,p,m,out,used

    def test_complete_mocked_run_and_check(self):
        with tempfile.TemporaryDirectory() as td:
            rc,p,m,out,used=self.driver(td);self.assertEqual(rc,0);self.assertTrue(run.d.read(out/'summary.json')['status']['complete'])
            self.assertEqual(run.d.read(out/'summary.json')['baseline_requests'],m['baseline_requests'])

    def test_anchor_failure_blocks_guard_calls(self):
        with tempfile.TemporaryDirectory() as td:
            rc,p,m,out,used=self.driver(td,bad_anchor=True);self.assertEqual(rc,2);self.assertEqual(used,['vle'])
            self.assertIsNone(run.d.read(out/'public-errors.json')['scores'])

    def test_one_failed_value_blocks_acceptance(self):
        with tempfile.TemporaryDirectory() as td:
            rc,p,m,out,used=self.driver(td,missing=True);self.assertEqual(rc,2)
            self.assertEqual(len(used),5);self.assertIsNone(run.d.read(out/'public-errors.json')['acceptance'])

    def test_timeout_keeps_attempt_receipts(self):
        with tempfile.TemporaryDirectory() as td:
            rc,p,m,out,used=self.driver(td,timeout=True);self.assertEqual(rc,2)
            self.assertEqual(run.d.read(out/'summary.json')['status']['query_coverage']['he']['finite'],0)

    def test_tampered_output_refused(self):
        with tempfile.TemporaryDirectory() as td:
            rc,p,m,out,used=self.driver(td);t=m['tasks'][0];f=out/t['id']/'result.json';v=run.d.read(f)
            v['values'][0]['lngamma'][0]+=.1;f.write_text(json.dumps(v))
            with patch.object(run,'load',return_value=(p,m)):
                with self.assertRaises(ValueError):run.check(argparse.Namespace(plan=str(p),plan_commit='f'*40,run=str(out)))

    def test_second_claim_refused(self):
        with tempfile.TemporaryDirectory() as td:
            rc,p,m,out,used=self.driver(td)
            with patch.object(run,'load',return_value=(p,m)):
                with self.assertRaises(FileExistsError):run.run(argparse.Namespace(plan=str(p),plan_commit='f'*40,out=str(Path(td)/'another')))

    def test_partial_finite_result_is_not_scored(self):
        m,raw=fixture();first=next(t for t in m['tasks'] if t['kind']=='idac');raw[first['id']][0,0]=np.nan
        q=run.analyze(m,raw);self.assertFalse(q['status']['complete']);self.assertIsNone(q['scores'])

    def test_grid_disagreement_blocks_complete_tradeoff(self):
        m,raw=fixture()
        with patch.object(run.stats,'detection',return_value=dict(detected=None,grid_agreement=False,gaps=[0.,1.])):
            q=run.analyze(m,raw);self.assertFalse(q['status']['complete']);self.assertTrue(q['status']['unresolved_grid_jobs'])

    def test_declared_budget_no_second_candidate_query(self):
        m,raw=fixture();self.assertEqual(m['baseline_requests'],1+1+2+2*len(st.grid_union()))
        self.assertEqual(len(st.grids()),2)



class ReproductionTests(unittest.TestCase):
    def test_registration_binds_baseline_and_helpers(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);frozen={};reg='e'*40
            files=list(run.FILES)+['src/zcosmo/example.py','results/qc/dispersion.csv',
                'results/qc/dielectric.csv','results/z_params/Z0.json']
            for rel in files:
                p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(rel+'\n')
                frozen[rel]=p.read_bytes()
            def git(c,rel):
                if rel=='PREREGISTRATION.md':return (run.MARKER+' '+law.RECIPE).encode()
                return frozen[rel]
            with patch.object(run,'ROOT',root),patch.object(run.r15,'ancestor'),patch.object(run.r15,'git_bytes',side_effect=git):
                self.assertEqual(run.registration(reg),reg)
                (root/files[0]).write_text('changed helper')
                with self.assertRaises(ValueError):run.registration(reg)
                (root/files[0]).write_bytes(frozen[files[0]])
                (root/'src/zcosmo/example.py').write_text('changed baseline')
                with self.assertRaises(ValueError):run.registration(reg)

    def test_source_recipe_cannot_have_weight_changed(self):
        with actual_model() as (b,f,p):
            b.z0=p.with_(w_dsp=.5)
            with self.assertRaises(ValueError):law.PairedLondon(b,pair())

    def test_changed_volume_is_not_silent(self):
        with actual_model() as (b,f,p):
            with self.assertRaises(ValueError):law.PairedLondon(b,pair((44.,130.)))

    def test_statistical_overflow_withholds_acceptance(self):
        m,raw=fixture()
        with patch.object(run.stats,'paired_summary',side_effect=FloatingPointError):
            q=run.analyze(m,raw)
        self.assertFalse(q['status']['complete']);self.assertIsNone(q['acceptance'])
        self.assertEqual(q['status']['analysis_error'],'FloatingPointError')

    def test_missing_he_sign_class_withholds_acceptance(self):
        m,raw=fixture()
        for t in m['tasks']:
            if t['kind']=='he':t['members'][0]['truth']=0.
        q=run.analyze(m,raw);self.assertFalse(q['status']['complete']);self.assertIsNone(q['scores'])

    def test_scope_and_input_coverage_do_not_hide_failure(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'idac.csv'
            p.write_text('solute,solvent,T,ln_gamma_inf,split,has_sigma\nA,B,300,2,test_one,True\nA,C,300,3,test_one,True\nA,B,299,2,test_one,False\nA,B,460,2,test_one,True\n')
            rows,c=run.guard_rows(p,'idac',lambda k:'missing' if k=='C' else None)
            self.assertEqual(len(rows),1);self.assertEqual(c['original_rows'],4)
            self.assertEqual(len(c['exclusions']),3)

    def test_unknown_split_refused(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'idac.csv';p.write_text('solute,solvent,T,ln_gamma_inf,split\nA,B,300,2,new_holdout\n')
            with self.assertRaises(ValueError):run.guard_rows(p,'idac',lambda k:None)

    def test_p54_bias_quantities_are_distinct(self):
        # Public rounded numbers, not a candidate or experimental scoring run.
        bias=np.array([1.44,-2.79,6.56,1.53,-.35,-4.34,4.66,-.02])
        oat=bias[1]-bias[0]
        shap=sum((math.factorial(len(S))*math.factorial(2-len(S))/6)*
            (bias[sum(S)+1]-bias[sum(S)]) for S in ((),(2,),(4,),(2,4)))
        self.assertAlmostEqual(oat,-4.23);self.assertAlmostEqual(shap,-4.473333333333333)
        self.assertGreater(abs(oat-shap),.2)

    def test_worker_calls_only_unchanged_baseline(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);out=root/'run/job-00000';prof=root/'p.sigma';profile(prof)
            q=dict(query_id='idac:0:0',T=300.,x1=0.)
            task=dict(id='job-00000',keys=['A','B'],queries=[q])
            m=dict(tasks=[task],profiles={'A':str(prof),'B':str(prof)},
                   inputs=run.d.fingerprint([prof]),worker_inputs={})
            p=root/'plan.json';run.d.write(p,m)
            run.d.write(root/'execution_claim.json',dict(plan_sha256=run.d.sha(p),output=str(out.parent)))
            calls=[]
            def lg(T,x):
                calls.append((T,x.tolist(),os.environ.get('ZC_R6_ENDPOINT')))
                self.assertTrue((out/'attempt-00000.json').is_file())
                self.assertNotIn('ZC_UNREGISTERED',os.environ)
                return np.array([.3,0.])
            model=types.SimpleNamespace(lngamma=lg)
            a=argparse.Namespace(plan=str(p),plan_commit='e'*40,job=task['id'],out=str(out))
            with patch.object(run,'load',return_value=(p,m)),patch.object(run,'native_baseline',return_value=model),\
                 patch.dict(os.environ,{'ZC_UNREGISTERED':'1'}):
                run.worker(a)
            self.assertEqual(len(calls),1);self.assertEqual(calls[0][2],'1')
            self.assertEqual(run.d.read(out/'result.json')['values'][0]['lngamma'],[.3,0.])
            self.assertTrue((out/'overlay/A.sigma').is_symlink())
            with patch.object(run,'load',return_value=(p,m)),patch.object(run,'native_baseline',return_value=model):
                with self.assertRaises(FileExistsError):run.worker(a)

    def test_worker_nonfinite_retains_requested_identity(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);out=root/'run/job-00000';prof=root/'p.sigma';profile(prof)
            task=dict(id='job-00000',keys=['A','B'],queries=[dict(query_id='x',T=300.,x1=.4)])
            m=dict(tasks=[task],profiles={'A':str(prof),'B':str(prof)},inputs=run.d.fingerprint([prof]),worker_inputs={})
            p=root/'plan.json';run.d.write(p,m);run.d.write(root/'execution_claim.json',dict(plan_sha256=run.d.sha(p),output=str(out.parent)))
            with patch.object(run,'load',return_value=(p,m)),patch.object(run,'native_baseline',
                return_value=types.SimpleNamespace(lngamma=lambda T,x:np.array([np.nan,0.]))),patch.dict(os.environ,{}):
                run.worker(argparse.Namespace(plan=str(p),plan_commit='e'*40,job=task['id'],out=str(out)))
            z=run.d.read(out/'result.json')['values'][0]
            self.assertEqual(z['query_id'],'x');self.assertIsNone(z['lngamma']);self.assertIsNotNone(z['error'])

    def freeze_fixture(self,td,budget=180000,changed_guard=False):
        root=Path(td)/'checkout';root.mkdir();outside=Path(td)/'private';outside.mkdir()
        for rel in (*run.FILES,'src/zcosmo/dummy.py','scripts/r14_dielectric.py','scripts/r14_oracle.py',
                    'scripts/r15_factorial.py','scripts/r15_math.py'):
            p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('# synthetic\n')
        qc=root/'results/qc';qc.mkdir(parents=True)
        (qc/'dispersion.csv').write_text('inchikey,C6_au,alpha_au\nA,400,30\nB,3600,100\n')
        (qc/'dielectric.csv').write_text('inchikey,eps\nA,10\nB,20\n')
        (root/'results/z_params').mkdir();(root/'results/z_params/Z0.json').write_text('{}')
        ud=outside/'ud';ud.mkdir();profile(ud/'A.sigma',45.);profile(ud/'B.sigma',130.)
        inp=outside/'inputs';inp.mkdir()
        (inp/'idac.csv').write_text('solute,solvent,T,ln_gamma_inf,split\nA,B,300,1,test_one\n')
        (inp/'he.csv').write_text('c1,c2,T,x1,HE_J,split\nA,B,300,.3,100,test_one\n')
        (inp/'positive.csv').write_text('c1,c2,T,x1,split\nA,B,300,.1,test_one\n')
        (inp/'negative.csv').write_text('c1,c2,T,split\nA,B,300,test_one\n'+'A,B,300,train\n'*335)
        orig={'data/benchmark/'+n:(inp/(n if n!='lle.csv' else 'positive.csv')).read_bytes() for n in ('idac.csv','he.csv','lle.csv')}
        if changed_guard:(inp/'idac.csv').write_text((inp/'idac.csv').read_text().replace(',1,test_one',',2,test_one'))
        oldp=outside/'prior/plan.json';run.d.write(oldp,{'mock':True})
        run.d.write(oldp.parent/'execution_claim.json',{'mock':True})
        prev=outside/'prior-run';prev.mkdir();run.d.write(prev/'summary.json',{});run.d.write(prev/'public-errors.json',{})
        # Only the source checker is mocked. The new 963-row freeze, hashes,
        # job allocation and audit output execute through their real functions.
        rows=[dict(row_id=str(i),c1='A',c2='B',T=300.,x1=.4,P=100.,psat=[100.,100.],system='mock-system-'+str(i%100)) for i in range(963)]
        oldm=dict(rows=rows,profiles={'A':str(ud/'A.sigma'),'B':str(ud/'B.sigma')},inputs={},
                  protected_counts={'profiles_v2':630,'s1_stalled':1,'s2_stalled':5})
        a=argparse.Namespace(registration='e'*40,r15_plan=str(oldp),r15_plan_commit='f'*40,
            r15_run=str(prev),out=str(outside/'plan'),ud_profiles=str(ud),**{k:str(inp/(k+'.csv')) for k in ('idac','he','positive','negative')})
        with patch.object(run,'ROOT',root),patch.object(run.d,'mac'),patch.object(run,'registration',return_value='e'*40),\
             patch.object(run.r15,'check',return_value=0),patch.object(run.r15,'load',return_value=(oldp,oldm)),\
             patch.object(run.r15,'arrays',return_value=(np.full((963,8),100.),7704,{})),\
             patch.object(run.r15,'anchor',return_value={'passed':True}),patch.object(run.r15,'git_bytes',side_effect=lambda c,p:orig[p]),\
             patch.dict(run.DESIGN,{'max_baseline_requests':budget}):
            run.freeze(a)
        return Path(a.out)

    def test_real_freeze_logic_with_mock_P54_archive(self):
        with tempfile.TemporaryDirectory() as td:
            p=self.freeze_fixture(td);m=run.d.read(p/'plan.json')
            self.assertEqual(m['baseline_requests'],963+1+2+2*len(st.grid_union()))
            self.assertEqual(len(m['tasks'][0]['members']),963)
            self.assertFalse(m['exposure']['may_claim_unexposed'])
            self.assertEqual(run.d.read(p/'audit-private.json')['activity_calls'],0)
            self.assertEqual((p/'PLAN_SHA256.txt').read_text().strip(),run.d.sha(p/'plan.json'))
            run.d.check_inputs(m['inputs'])

    def test_full_guard_budget_never_downsamples(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):self.freeze_fixture(td,budget=964)
            self.assertFalse((Path(td)/'private/plan').exists())

    def test_changed_benchmark_refused_before_new_plan(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):self.freeze_fixture(td,changed_guard=True)
            self.assertFalse((Path(td)/'private/plan').exists())


if __name__=='__main__':unittest.main(verbosity=2)
