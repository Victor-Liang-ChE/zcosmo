"""Portable R15 tests. Synthetic profiles, fake table loaders, no UD or ThermoML.

Numerical tests use the actual NumPy segment solver and actual Z0x/Z0w classes.
Process tests mock scientific workers; one harmless subprocess checks timeout.
"""
from __future__ import annotations
import argparse
from contextlib import contextmanager
import importlib.util
import itertools
import json
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
import numpy as np
import r15_math as a
import r15_factorial as r


@contextmanager
def engines():
    root=Path(__file__).resolve().parents[1]
    package=types.ModuleType('zcosmo');package.__path__=[str(root/'src/zcosmo')]
    def module(name,path):
        spec=importlib.util.spec_from_file_location(name,path)
        mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod)
        return mod
    with patch.dict(sys.modules,{'zcosmo':package}):
        c=module('zcosmo.cosmosac',root/'src/zcosmo/cosmosac.py')
        models=types.ModuleType('zcosmo.models');zm=types.ModuleType('zcosmo.zmodel')
        qc=types.ModuleType('zcosmo.qc_hbond');qc.DIMERS=()
        z0=c.Params(A_ES=12226.235339788673,B_ES=0.0,c_OH_OH=5712.229463082564,
                    c_OT_OT=5611.4027535161395,c_OH_OT=5987.642651646004,
                    disp_mode='london',w_dsp=1.0)
        models.ROOT=root;models.load_z_params=lambda name:z0
        zm.c_es_theory=lambda aeff=7.25,fpol=1.:fpol*.3*aeff**1.5/2.395e-4/2
        sys.modules.update({'zcosmo.models':models,'zcosmo.zmodel':zm,'zcosmo.qc_hbond':qc})
        fluids={}
        for i,key in enumerate(('A','B')):
            p=np.zeros((3,51));p[0,[15,22,25,30,38]]=[2,8,9,5,1]
            p[1,[8,12,39,42]]=[1+2*i,2+i,4-i,1]
            p[2,[10,20,36,41]]=[1,2,3+i,1]
            p *= (90+30*i)/p.sum()
            fluids[key]=c.Fluid(key,p,float(p.sum()),80.+30*i,'NHB',None,{})
        c.load_fluid=lambda k:fluids[k]
        c._london_table=lambda path:{'A':(1000.,10.),'B':(1600.,14.)}
        x=module('zcosmo.z0x',root/'src/zcosmo/z0x.py');x._eps=lambda:{'A':3.,'B':35.}
        w=module('zcosmo.z0w',root/'src/zcosmo/z0w.py')
        yield c,x,w,z0


def fixture(n=6):
    rows=[dict(row_id=str(i),c1='A'+str(i%2),c2='B',T=298.15,x1=.3,P=100.,
               psat=[50.,80.],system='A'+str(i%2)+'|B') for i in range(n)]
    def val(row,c):
        e,h,d=map(int,c)
        return 112.+int(row['row_id'])/10-6*e+2*h-3*d+e*h
    preds=np.array([[val(row,c) for c in a.CORNERS] for row in rows])
    m=dict(rows=rows,jobs=r.jobs_for(rows),prior_anchors=preds[:,[0,7]].tolist())
    return m,preds,val


class Arithmetic(unittest.TestCase):
    def test_dummy_factor_exactness(self):
        rng=np.random.default_rng(7);v={c:rng.normal(size=11) for c in a.CORNERS}
        full=a.shapley(a.lift_five(v));small=a.shapley(v)
        np.testing.assert_allclose(full[:3],small,atol=1e-12,rtol=0)
        np.testing.assert_array_equal(full[3:],np.zeros_like(full[3:]))

    def test_interaction_allocates_to_its_members(self):
        v={c:np.array([6*int(c[0])*int(c[1])]) for c in a.CORNERS}
        np.testing.assert_allclose(a.shapley(v).ravel(),[3,3,0],atol=1e-14)
        dd=a.dividends(v);self.assertEqual(dd['110'][0],6.)
        self.assertEqual(sum(v[0] for v in dd.values()),6.)

    def test_full_five_way_efficiency(self):
        m,p,_=fixture();z=a.summary(m['rows'],p,True)
        self.assertTrue(z['status']['complete'])
        q=z['public_errors'];self.assertAlmostEqual(sum(v['error_reduction_pp'] for v in q['factors'].values()),q['endpoint_gap_pp'])
        self.assertEqual(q['factors']['profile_convention_shared']['error_reduction_pp'],0.)

    def test_error_not_absolute_pressure_change(self):
        rows=[dict(row_id='r',P=100.,system='x|y')]
        p=np.array([[90. if c[0]=='0' else 110. for c in a.CORNERS]])
        z=a.summary(rows,p,True)['public_errors']
        self.assertAlmostEqual(z['factors']['electrostatic_closure']['error_reduction_pp'],0.)
        self.assertAlmostEqual(z['factors']['electrostatic_closure']['signed_bias_change_pp'],20.)

    def test_nonfinite_preserves_universe(self):
        m,p,_=fixture();p[0,2]=np.nan;z=a.summary(m['rows'],p,True)
        self.assertFalse(z['status']['complete']);self.assertIsNone(z['public_errors'])
        self.assertEqual(z['status']['requested_rows'],6)
        self.assertEqual(z['status']['finite_by_corner']['010'],5)

    def test_derived_error_overflow_is_not_a_complete_score(self):
        m,p,_=fixture();m['rows'][0]['P']=1e-300;p[0,2]=1e300
        q=a.summary(m['rows'],p,True)
        self.assertFalse(q['status']['complete']);self.assertIsNone(q['public_errors'])
        self.assertEqual(q['status']['derived_error_nonfinite'],1)

    def test_failed_anchors_withhold_complete_result(self):
        m,p,_=fixture();self.assertIsNone(a.summary(m['rows'],p,False)['public_errors'])

    def test_duplicate_ids_fail(self):
        m,p,_=fixture();m['rows'][1]['row_id']='0'
        with self.assertRaises(ValueError):a.summary(m['rows'],p,True)

    def test_negative_contribution_and_unclipped_share(self):
        m,p,_=fixture();q=a.summary(m['rows'],p,True)['public_errors']
        self.assertLess(q['factors']['HB_constants']['error_reduction_pp'],0)
        self.assertGreater(q['factors']['electrostatic_closure']['gap_share'],0)

    def test_incomplete_cube_fails(self):
        with self.assertRaises(ValueError):a.shapley({'000':np.ones(2)})

    def test_budget_arithmetic(self):
        rows=[]
        for j in range(100):
            for k in range(10 if j<63 else 9):
                rows.append(dict(c1=str(j),c2='b'))
        self.assertEqual(len(rows),963);jobs=r.jobs_for(rows)
        self.assertEqual(len(jobs),800)
        self.assertEqual(sum(len(j['indices']) for j in jobs if j['corner'] in a.ANCHORS),1926)
        self.assertEqual(sum(len(j['indices']) for j in jobs),7704)


class ModelTests(unittest.TestCase):
    def test_endpoint_models_unchanged(self):
        with engines() as (c,x,w,z0):
            for T,xx in itertools.product((298.15,360.),(.2,.63)):
                comp=np.array([xx,1-xx])
                np.testing.assert_array_equal(a.make_corner(['A','B'],'000').lngamma(T,comp),x.Z0xBinary(['A','B']).lngamma(T,comp))
                np.testing.assert_array_equal(a.make_corner(['A','B'],'111').lngamma(T,comp),c.Mixture(['A','B'],c.Params(use_dsp=False)).lngamma(T,comp))

    def test_shared_drift_fails(self):
        with engines() as (c,x,w,z0):
            for n,v in (('aeff',8.),('q0',80.),('r0',70.),('z',8.)):
                with self.assertRaises(ValueError):a.shared_audit(z0.with_(**{n:v}),c.Params(use_dsp=False))

    def test_London_really_switches_off(self):
        with engines() as (c,x,w,z0):
            p=a.make_corner(['A','B'],'001').z0
            self.assertNotEqual(p.disp_mode,'london');self.assertFalse(p.use_dsp)
            np.testing.assert_array_equal(c.Mixture(['A','B'],p).lngamma_disp([.4,.6],298.15),[0.,0.])
            self.assertGreater(abs(c.Mixture(['A','B'],z0).lngamma_disp([.4,.6],298.15)).max(),0.)

    def test_constant_ES_never_uses_variable_dc_dx(self):
        with engines() as (c,x,w,z0):
            with patch.object(x.Z0xBinary,'_analytic',side_effect=AssertionError('wrong branch')):
                self.assertTrue(np.isfinite(a.make_corner(['A','B'],'100').lngamma(298.15,[.3,.7])).all())

    def test_hybrid_derivatives_from_excess_g(self):
        with engines() as (c,x,w,z0):
            for bits in a.CORNERS:
                model=a.make_corner(['A','B'],bits);T=330.;xx=.37;h=2e-4
                def g(t):
                    if bits[0]=='0':
                        mx=c.Mixture(['A','B'],model.z0.with_(A_ES=model._c(t)))
                    else:mx=model
                    return float(np.array([t,1-t])@mx.lngamma(T,[t,1-t]))
                derivative=(g(xx-2*h)-8*g(xx-h)+8*g(xx+h)-g(xx+2*h))/(12*h)
                expected=np.array([g(xx)+(1-xx)*derivative,g(xx)-xx*derivative])
                np.testing.assert_allclose(model.lngamma(T,[xx,1-xx]),expected,atol=2e-6,rtol=0)

    def test_contact_energy_gauge_cancels_in_pure_referenced_residual(self):
        with engines() as (c,x,w,z0):
            T=310.;weights=np.array([.37,.63]);fl=[c.load_fluid(k) for k in ('A','B')]
            ps=np.array([f.psigA.ravel() for f in fl]);areas=ps.sum(1)
            pm=weights@ps/(weights@areas)
            W=c.delta_w(T,z0);u=np.linspace(-.15,.12,153)
            def residual(W):
                E=np.exp(-W/(c.R_KCAL*T));gm=np.log(c.solve_gamma(E,pm))
                gp=np.array([np.log(c.solve_gamma(E,v/v.sum())) for v in ps])
                return np.sum(ps*(gm-gp),axis=1)/z0.aeff
            np.testing.assert_allclose(residual(W),residual(W+u[:,None]+u[None,:]),atol=2e-8,rtol=0)

    def test_HB_mask_shared(self):
        with engines() as (c,x,w,z0):
            other=z0.with_(c_OH_OH=c.Params().c_OH_OH,c_OT_OT=c.Params().c_OT_OT,c_OH_OT=c.Params().c_OH_OT)
            diff=c.delta_w(298.15,z0)-c.delta_w(298.15,other)
            sig=np.tile(c.SIG,3);same=sig[:,None]*sig[None,:]>=0
            np.testing.assert_array_equal(diff[same],np.zeros_like(diff[same]))
            np.testing.assert_array_equal(diff[:51],np.zeros_like(diff[:51]))

    def test_association_all_branches_restore_full_g(self):
        with engines() as (c,x,w,z0):
            class Descendant(w.Z0w2Binary):
                def _ga(self,T,t):return .7*t*(1-t)*(1+.2*t)*298.15/T
            for cls in (w.Z0wBinary,w.Z0w2Binary,Descendant):
                obj=cls.__new__(cls)
                if cls is not Descendant:obj._ga=types.MethodType(lambda self,T,t:.7*t*(1-t)*298.15/T,obj)
                # Keep the real association _g and override only the residual data source.
                with patch.object(x.Z0xBinary,'_g',lambda self,T,t:.2*t*(1-t)),\
                     patch.object(obj,'_analytic',side_effect=AssertionError('association bypassed')),\
                     patch.object(obj,'_endpoint',side_effect=AssertionError('P28 bypassed')):
                    for flag,T,t in itertools.product(('0','1'),(278.15,350.),(0.,.00005,.0001,.3,.9999,.99995,1.)):
                        with patch.dict(os.environ,{'ZC_R6_ENDPOINT':flag}):
                            lo=max(0,t-obj.H);hi=min(1,t+obj.H)
                            gp=(obj._g(T,hi)-obj._g(T,lo))/(hi-lo);g0=obj._g(T,t)
                            expected=np.array([g0+(1-t)*gp,g0-t*gp])
                            np.testing.assert_allclose(obj.lngamma(T,[t,1-t]),expected,rtol=0,atol=1e-12)
                            self.assertAlmostEqual(float(np.array([t,1-t])@obj.lngamma(T,[t,1-t])),g0,places=12)
                    self.assertAlmostEqual(obj.lngamma_inf(298.15,0),obj.lngamma(298.15,[0.,1.])[0],places=12)

    def test_actual_site_mass_action_with_synthetic_strengths(self):
        with engines() as (c,x,w,z0):
            strengths={(dd,aa):18.+3*j for j,(dd,aa) in enumerate(itertools.product(w.DONORS,w.ACCEPTORS))}
            with patch.object(w,'delta',return_value=strengths),\
                 patch.object(w,'delta_liq',side_effect=lambda T,e:{k:v*(1+.002*e) for k,v in strengths.items()}):
                for cls in (w.Z0wBinary,w.Z0w2Binary):
                    obj=cls(['A','B'],['O','CO'])
                    T=298.15;t=.31
                    part=obj._ga(T,t)
                    self.assertGreater(abs(part),1e-8)
                    full=obj.lngamma(T,[t,1-t])
                    original=obj._ga
                    obj._ga=lambda T,x:0.
                    without=obj.lngamma(T,[t,1-t])
                    obj._ga=original
                    dg=(original(T,t+obj.H)-original(T,t-obj.H))/(2*obj.H)
                    np.testing.assert_allclose(full-without,[part+(1-t)*dg,part-t*dg],atol=2e-11,rtol=0)
                    self.assertAlmostEqual(original(T,0.),0.,places=12)
                    self.assertAlmostEqual(original(T,1.),0.,places=12)

    def test_endpoint_error_is_historical_not_claimed_exact(self):
        with engines() as (c,x,w,z0):
            obj=w.Z0wBinary.__new__(w.Z0wBinary);obj._g=lambda T,t:2*t*(1-t)
            for t,j in ((0.,0),(1.,1)):
                self.assertAlmostEqual(obj.lngamma(300.,[t,1-t])[j],2*(1-obj.H),places=11)

    def test_direct_g_override_descendant(self):
        with engines() as (c,x,w,z0):
            class Other(w.Z0wBinary):
                def _g(self,T,t):return 1.5*t*(1-t)
            obj=Other.__new__(Other)
            np.testing.assert_allclose(obj.lngamma(300.,[.3,.7]),[1.5*.7**2,1.5*.3**2],atol=1e-11,rtol=0)


class RunnerTests(unittest.TestCase):
    def driver(self,tmp,bad_anchor=False,missing=False):
        m,preds,value=fixture();root=Path(tmp);plan=root/'plan.json';r.d.write(plan,m)
        out=root/'run';used=[]
        def launch(cmd,log,seconds,env):
            jid=cmd[cmd.index('--job')+1];job=next(j for j in m['jobs'] if j['id']==jid)
            folder=Path(cmd[cmd.index('--out')+1]);folder.mkdir();used.append(job['corner'])
            vals=[]
            for n,i in enumerate(job['indices']):
                row=m['rows'][i];r.d.write(folder/f'attempt-{n:04d}.json',dict(row_id=row['row_id'],attempted=True))
                v=value(row,job['corner'])+(.01 if bad_anchor and job['corner']=='000' else 0)
                if missing and job['corner']=='010' and n==0:v=None
                vals.append(dict(row_id=row['row_id'],value=v,error=None))
            r.d.write(folder/'result.json',dict(job=jid,corner=job['corner'],plan_sha256=r.d.sha(plan),
                requested=len(vals),attempted=len(vals),values=vals,wall_s=.1))
            return dict(state='returned',returncode=0)
        m['inputs']={str(plan):r.d.sha(plan)}
        args=argparse.Namespace(plan=str(plan),plan_commit='f'*40,out=str(out))
        with patch.object(r,'load',return_value=(plan,m)),patch.object(r.old,'launch',side_effect=launch):
            rc=r.run(args)
            self.assertEqual(r.check(argparse.Namespace(plan=str(plan),plan_commit='f'*40,run=str(out))),rc)
        return rc,m,plan,out,used

    def test_complete_run_and_saved_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            rc,m,p,out,used=self.driver(tmp)
            self.assertEqual(rc,0);self.assertEqual(r.d.read(out/'summary.json')['attempted_model_calls'],48)
            self.assertTrue(r.d.read(out/'public-errors.json')['status']['complete'])
            self.assertEqual(len(used),16)

    def test_anchor_blocks_all_six_intermediates(self):
        with tempfile.TemporaryDirectory() as tmp:
            rc,m,p,out,used=self.driver(tmp,bad_anchor=True)
            self.assertEqual(rc,2);self.assertEqual(set(used),set(a.ANCHORS))
            self.assertEqual(r.d.read(out/'summary.json')['attempted_model_calls'],12)
            self.assertIsNone(r.d.read(out/'public-errors.json')['aggregate_errors'])

    def test_nonfinite_row_not_removed(self):
        with tempfile.TemporaryDirectory() as tmp:
            rc,m,p,out,used=self.driver(tmp,missing=True);self.assertEqual(rc,2)
            z=r.d.read(out/'public-errors.json');self.assertEqual(z['status']['requested_rows'],6)
            self.assertIsNone(z['aggregate_errors'])

    def test_changed_prediction_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            rc,m,p,out,used=self.driver(tmp);rp=out/'job-0000/result.json';z=r.d.read(rp);z['values'][0]['value']+=1
            rp.write_text(json.dumps(z))
            with patch.object(r,'load',return_value=(p,m)):
                with self.assertRaises(ValueError):r.check(argparse.Namespace(plan=str(p),plan_commit='f'*40,run=str(out)))

    def test_claim_prevents_repeat(self):
        with tempfile.TemporaryDirectory() as tmp:
            rc,m,p,out,used=self.driver(tmp)
            with patch.object(r,'load',return_value=(p,m)):
                with self.assertRaises(FileExistsError):r.run(argparse.Namespace(plan=str(p),plan_commit='f'*40,out=str(out)+'2'))

    def test_row_order_mutation_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            rc,m,p,out,used=self.driver(tmp);rp=out/'job-0000/result.json';z=r.d.read(rp);z['values'].reverse();rp.write_text(json.dumps(z))
            with self.assertRaises(ValueError):r.arrays(m,out,r.d.sha(p))

    def test_worker_with_real_numerical_kernels_and_synthetic_profiles(self):
        with tempfile.TemporaryDirectory() as tmp, engines() as (c,x,w,z0), patch.dict(os.environ):
            root=Path(tmp);profiles={}
            for key in ('A','B'):
                fl=c.load_fluid(key);path=root/(key+'.sigma')
                with path.open('w') as stream:
                    stream.write('# synthetic test only\n')
                    np.savetxt(stream,np.c_[np.tile(c.SIG,3),fl.psigA.ravel()],fmt='%.18e')
                profiles[key]=str(path)
            rows=[dict(row_id=str(i),c1='A',c2='B',system='A|B',T=310.,x1=t,P=100.,psat=[110.,70.])
                  for i,t in enumerate((.2,.65))]
            m=dict(rows=rows,jobs=r.jobs_for(rows),profiles=profiles,
                   inputs=r.d.fingerprint(profiles.values()),worker_inputs={})
            plan=root/'plan.json';r.d.write(plan,m);run=root/'run';run.mkdir()
            r.d.write(root/'execution_claim.json',dict(plan_sha256=r.d.sha(plan),output=str(run)))
            before=r.d.fingerprint(profiles.values())
            for job in m['jobs']:
                args=argparse.Namespace(plan=str(plan),plan_commit='f'*40,job=job['id'],out=str(run/job['id']))
                with patch.object(r,'load',return_value=(plan,m)):
                    r.worker(args)
                result=r.d.read(run/job['id']/'result.json')
                self.assertEqual(result['attempted'],2)
                model=a.make_corner(['A','B'],job['corner'])
                for row,v in zip(rows,result['values']):
                    expected=r.old.pressure(model.lngamma(row['T'],[row['x1'],1-row['x1']]),row['x1'],row['psat'])
                    self.assertAlmostEqual(v['value'],expected,places=11)
            self.assertEqual(before,r.d.fingerprint(profiles.values()))

    def test_actual_R14_archive_receipt_adapter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);run=root/'run';run.mkdir();plan=root/'plan.json'
            rows=[]
            for j in range(100):
                for k in range(10 if j<63 else 9):
                    rows.append(dict(row_id=str(len(rows)),c1=f'A{j:03}',c2='B',system=f'A{j:03}|B',
                        T=298.15,x1=.4,P=100.,archived_pred_P=112.,psat=[80.,110.]))
            jobs=[]
            for arm in r.old.ARMS:
                for j in range(100):
                    idx=[i for i,row in enumerate(rows) if row['c1']==f'A{j:03}']
                    jobs.append(dict(id=f'job-{len(jobs):04d}',arm=arm,keys=[f'A{j:03}','B'],indices=idx))
            m=dict(registration='a'*40,schema='r14-oracle-v1',design=r.old.DESIGN,environment=r.d.environment(),
                inputs={},ingredient_manifest={'inputs':{}},exposure={'may_claim_unexposed':False},
                protected_counts={'profiles_v2':630,'s1_stalled':1,'s2_stalled':5},rows=rows,jobs=jobs,census={})
            r.d.write(plan,m);ph=r.d.sha(plan)
            r.d.write(root/'execution_claim.json',dict(plan_sha256=ph,output=str(run)))
            for job in jobs:
                folder=run/job['id'];folder.mkdir();vals=[]
                for j,i in enumerate(job['indices']):
                    row=rows[i];r.d.write(folder/f'attempt-{j:04d}.json',dict(row_id=row['row_id'],attempted=True))
                    vals.append(dict(row_id=row['row_id'],value=112.-r.old.ARMS.index(job['arm']),error=None))
                r.d.write(folder/'result.json',dict(job=job['id'],arm=job['arm'],plan_sha256=ph,
                    requested=len(vals),attempted=len(vals),values=vals))
                r.d.write(run/(job['id']+'.terminal.json'),dict(job=job['id'],plan_sha256=ph,state='returned',returncode=0))
            v,n,h=r.old.arrays(m,run,ph);ar=r.old.anchor_pass(rows,v[:,0]);q=r.old.error_summary(rows,v)
            r.d.write(run/'summary.json',dict(plan_sha256=ph,anchor=ar,output_hashes=h,
                attempted_model_calls=n,**q))
            r.d.write(run/'public-errors.json',dict(status=q['status'],anchor=ar,aggregate_errors=q['aggregate_errors'],
                census=m['census'],interpretation=r.old.DESIGN['result'],adopted=False,SCF_calls=0))
            with patch.object(r.d,'registration'),patch.object(r,'ancestor'),patch.object(r,'git_bytes',return_value=(ph+'\n').encode()):
                out,got,receipts,bridges=r.archive(str(plan),'b'*40,str(run),'c'*40)
                self.assertEqual(got.shape,(963,3));self.assertEqual(len(out['rows']),963)
                self.assertGreater(len(receipts),3000);self.assertEqual(bridges,[])
                bad=run/'job-0000'/'attempt-0000.json';bad.write_text('{}')
                with self.assertRaises(ValueError):r.archive(str(plan),'b'*40,str(run),'c'*40)

    def test_only_explicit_source_bridge(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);src=root/r.ASSOC;src.parent.mkdir(parents=True);src.write_bytes(b'new')
            expected=__import__('hashlib').sha256(b'old').hexdigest()
            with patch.object(r,'ROOT',root),patch.object(r,'git_bytes',side_effect=lambda commit,rel:b'old' if commit==r.BASE else b'new'):
                self.assertEqual(len(r.check_old_inputs({str(src):expected},'c'*40)),1)
                other=root/'other.dat';other.write_bytes(b'new')
                with self.assertRaises(ValueError):r.check_old_inputs({str(other):expected},'c'*40)

    def test_private_output_cannot_enter_git(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'.git').mkdir()
            with self.assertRaises(ValueError):r.d.private(root/'out',True)

    def test_public_allowlist_has_no_rows(self):
        m,p,_=fixture();q=a.summary(m['rows'],p,True);pub=r.public(q,{'passed':True})
        self.assertNotIn('private_rows',pub);self.assertNotIn('profiles',pub)
        self.assertNotIn('row_id',json.dumps(pub))

    def test_timeout_is_terminal(self):
        with tempfile.TemporaryDirectory() as tmp:
            z=r.old.launch([sys.executable,'-c','import time; time.sleep(2)'],Path(tmp)/'log',.03,dict(os.environ))
            self.assertEqual(z['state'],'timeout')

if __name__=='__main__':unittest.main()
