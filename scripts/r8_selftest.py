"""Portable tests only. The mock SCF is an analytic polynomial, not PySCF."""
from __future__ import annotations
import argparse
import contextlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
import numpy as np
from r8_common import (BASE, STEPS, CASES, ARMS, sha, read, write, fd_check,
    canonical_membership, match_local_nodes, validate_direction, screening_counts)
import r8_diagnostic as native
from r8_evidence import audit

METRICS={}

@contextlib.contextmanager
def cwd(path):
    old=Path.cwd(); os.chdir(path)
    try: yield
    finally: os.chdir(old)


def polynomial_pairs():
    f=lambda x:-100.+.3*x+.2*x*x+.7*x**3+.1*x**5
    return np.array([[f(h),f(-h)] for h in STEPS])


class PortableTests(unittest.TestCase):
    def test_fd_and_inconclusive(self):
        e=polynomial_pairs(); a=fd_check(e,e,.3,.3,.30003)
        self.assertEqual(a['full_verdict'],'consistent')
        self.assertEqual(a['off_verdict'],'inconsistent')
        self.assertTrue(a['missing_response_material'])
        METRICS['polynomial_FD_error']=a['full_error']
        noisy=e.copy();noisy[-1,0]+=1e-7
        a=fd_check(noisy,noisy,.3,.3,.30003)
        self.assertEqual(a['full_verdict'],'inconclusive')
        self.assertEqual(fd_check(e,e,.3,.3,.3,False)['full_verdict'],'inconclusive')
        with self.assertRaises(ValueError):fd_check(e[:-1],e,.3,.3,.3)

    def test_node_identities(self):
        a,_=canonical_membership([0,0,1],[0,1,0])
        b,_=canonical_membership([1,0,0],[0,1,0]);self.assertEqual(a,b)
        c,_=canonical_membership([0,0,1],[0,2,0]);self.assertNotEqual(a,c)
        with self.assertRaises(ValueError):canonical_membership([0,0],[1,1])
        template=np.array([[1.,0,0],[0,1,0],[-1,0,0]])
        np.testing.assert_array_equal(match_local_nodes(template[[2,0]],template),[2,0])
        with self.assertRaises(ValueError):match_local_nodes(np.array([[2.,0,0]]),template)
        with self.assertRaises(ValueError):validate_direction(np.ones((2,3)),2)

    def test_screen_denominators(self):
        r=[dict(key=str(i),status='complete',screen_positive=True,
                response_change_max=2e-5) for i in range(35)]
        r += [dict(key=str(i),status='affinity_unresolved',screen_positive=None,
                   response_change_max=2e-5) for i in range(35,39)]
        r += [dict(key='39',status='running',screen_positive=None)]
        d=screening_counts(r)
        self.assertEqual([d[k] for k in ('requested','positive','negative','affinity_unresolved',
                                        'native_missing_or_failed','force_observed')],[40,35,0,4,1,39])
        self.assertIsNone(d['sampling_bound'])
        with self.assertRaises(ValueError):screening_counts(r+[r[0]])

    def test_explicit_pcm_math(self):
        # Toy C-PCM algebra E=-f*v^T*K^-1*v/2, not molecular quantum chemistry.
        K=np.array([[2.,.1],[.1,1.4]]);dK=np.array([[.2,.03],[.03,-.1]])
        v=np.array([.3,-.2]);dv=np.array([.07,.03]);f=.999999999
        z=np.linalg.solve(K,v)
        exact=-f*dv@z+.5*f*z@dK@z
        def energy(t):
            u=v+t*dv
            return -.5*f*u@np.linalg.solve(K+t*dK,u)
        h=1e-5;fd=(energy(h)-energy(-h))/(2*h)
        self.assertLess(abs(fd-exact),1e-10)
        METRICS['explicit_PCM_matrix_derivative_error']=abs(fd-exact)

    def test_pcm_layer_orchestration_with_mock(self):
        # Check fixed P0, units and the exact 22+2 partial-layer call budget.
        import copy,time
        K0=np.array([[2.,.1],[.1,1.4]]);dK=np.array([[.2,.03],[.03,-.1]])
        v0=np.array([.3,-.2]);dv=np.array([.07,.03]);f=.999999999
        class Mol:
            nao=2
            def __init__(self,x):self.x=np.asarray(x).copy()
            def copy(self):return copy.deepcopy(self)
            def set_geom_(self,x,unit):
                if unit!='Angstrom':raise ValueError(unit)
                self.x=np.asarray(x).copy();return self
            def intor_symmetric(self,name):return np.eye(2)*(1.+.01*self.x[0,0])
        calls=[0,0]
        class PCM:
            def __init__(self,mol):self.mol=mol
            def _get_vind(self,P):
                np.testing.assert_array_equal(P,np.eye(2));calls[0]+=1
                t=self.mol.x[0,0];K=K0+t*dK;v=v0+t*dv;R=-f*np.eye(2)
                q=np.linalg.solve(K,R@v)
                self._intermediates={'K':K,'R':R,'q':q,'v_grids':v}
                return .5*q@v,np.zeros((2,2))
            def grad(self,P):
                np.testing.assert_array_equal(P,np.eye(2));calls[1]+=1
                z=np.linalg.solve(K0,v0);g=np.zeros((2,3))
                g[0,0]=-f*dv@z+.5*f*z@dK@z;return g
        settings=dict(method='C-PCM',eps=1e9,lebedev_order=17,radii_table=np.ones(10),
                      vdw_scale=1.2,r_probe=0.,surface_discretization_method='SWIG')
        xyz=np.zeros((2,3));v=np.zeros((2,3));v[0,0]=1.
        template=types.SimpleNamespace(mol=Mol(xyz),with_solvent=types.SimpleNamespace(**settings),make_rdm1=lambda:np.eye(2))
        modules={}
        for name in ('pyscf','pyscf.solvent','zcosmo'):
            modules[name]=types.ModuleType(name);modules[name].__path__=[]
        for name,attrs in [('pyscf.solvent.pcm',{'PCM':PCM}),('zcosmo.pcm_lu',{'CachedPCM3c':PCM}),
                           ('zcosmo.pyscf_cosmo',{'BOHR':1.})]:
            modules[name]=types.ModuleType(name);modules[name].__dict__.update(attrs)
        with tempfile.TemporaryDirectory() as td,patch.dict(sys.modules,modules), \
             patch.object(native,'pcm_nodes',return_value={'signature':'same','count':2}):
            native.pcm_layer_check(template,xyz,v,time.monotonic()+10,Path(td))
            d=read(Path(td)/'layer.json');self.assertEqual(calls,[22,2])
            self.assertTrue(d['parity']['passed'])
            self.assertEqual(d['assessment']['full_verdict'],'consistent')
            counts=[r['overlap_electrons'] for r in read(Path(td)/'layer_calls.json')]
            self.assertGreater(max(counts)-min(counts),0.)
            METRICS['mock_PCM_layer_calls']={'energy':22,'gradient':2}

    def test_plan_roundtrip_and_tamper(self):
        with tempfile.TemporaryDirectory() as td,cwd(td):
            oldpath=Path('cloud/r7/referee/plan.json');cases=[]
            for label,(key,direction) in CASES.items():
                geom=oldpath.parent/(key+'.json')
                write(geom,dict(sym=['H','H'],x=[[0.,0,0],[1.,0,0]]))
                cases.append(dict(key=key,geometry=geom.name,geometry_sha256=sha(geom),spin=0))
            write(oldpath,dict(family='referee',cases=cases))
            for r in cases:
                key=r['key']; direction=next(v[1] for v in CASES.values() if v[0]==key)
                write(Path('docs/astra/round7/data/referee')/(key+'.result.json'),dict(
                    status='diagnostic_complete',plan_sha256=sha(oldpath),
                    input_geometry_sha256=r['geometry_sha256'],records=[dict(direction=direction,
                    unit_L2_direction=[[1.,0,0],[0.,0,0]])]))
            for source in native.SOURCES:
                p=Path(source);p.parent.mkdir(parents=True,exist_ok=True);p.write_text('synthetic source\n')
            native.plan(types.SimpleNamespace(registration='a'*40,out='new'))
            _,m=native.load_plan('new/plan.json')
            self.assertEqual(m['budgets']['SCF_calls'],176)
            Path(native.SOURCES[0]).write_text('changed\n')
            with self.assertRaises(ValueError):native.load_plan('new/plan.json')
            Path(native.SOURCES[0]).write_text('synthetic source\n')
            bad=Path('docs/astra/round7/data/referee')/(cases[0]['key']+'.result.json')
            d=read(bad);d['records']=[];write(bad,d)
            with self.assertRaises(ValueError):native.plan(types.SimpleNamespace(registration='a'*40,out='bad'))
            self.assertFalse(Path('bad').exists())

    def test_native_orchestration_with_mock_SCF(self):
        # Exercise all 22 energy evaluations and failure recording, without native imports.
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'run';geometry=Path(td)/'TEG.json'
            x=np.zeros((2,3));direction=np.zeros((2,3));direction[0,0]=1.
            write(geometry,dict(sym=['H','H'],x=x.tolist()))
            planfile=Path(td)/'plan.json';write(planfile,{})
            key=CASES['TEG'][0]
            m=dict(registration='a'*40,cases=[dict(label='TEG',key=key,
                geometry=geometry.name,geometry_sha256=sha(geometry),direction=direction.tolist(),
                direction_name=CASES['TEG'][1])])
            count=[0];fail=[None]
            class MF:
                def __init__(self,pos):self.pos=pos;self.converged=True;self.cycles=1;self.small_rho_cutoff=0.;self.grids=types.SimpleNamespace(prune=None)
                def kernel(self):
                    count[0]+=1
                    if count[0]==fail[0]:raise RuntimeError('mock SCF failure')
                    t=float(self.pos[0,0]);return -100.+.3*t+.2*t*t+.7*t**3+.1*t**5
                def make_rdm1(self):return np.eye(2)
            def g(mf,response):return direction*(.3 if response else .30003)
            z=types.ModuleType('zcosmo');z.__path__=[]
            pc=types.ModuleType('zcosmo.pyscf_cosmo');pc.BOHR=1.
            import importlib
            original=importlib.import_module
            def modules(name,*args,**kw):
                if name.startswith('pyscf.'):
                    return types.SimpleNamespace(__name__=name,__file__=__file__)
                return original(name,*args,**kw)
            with patch.dict(sys.modules,{'zcosmo':z,'zcosmo.pyscf_cosmo':pc}), \
                 patch('importlib.metadata.version',side_effect=lambda n:{'pyscf':'2.14.0','pyberny':'0.7.0','numpy':'2','scipy':'1'}[n]), \
                 patch('importlib.import_module',side_effect=modules), \
                 patch.object(native,'load_plan',return_value=(planfile,m)), \
                 patch.object(native,'make_mf',side_effect=lambda s,p,precision,arm:MF(p)), \
                 patch.object(native,'full_gradient',side_effect=g), \
                 patch.object(native,'xc_nodes',return_value=({'signature':'same','count':3},None,None)), \
                 patch.object(native,'response_grid_check',return_value={'membership_identical':True,'weights_match':True}), \
                 patch('r7_common.clean_environment'):
                a=types.SimpleNamespace(plan=str(planfile),case='TEG',arm='vacuum_pruned',out=str(out))
                native.native(a)
                d=read(out/'result.json')
                self.assertEqual(count[0],22);self.assertEqual(d['gradient_evaluations'],3)
                self.assertEqual(d['assessment']['full_verdict'],'consistent')
                self.assertEqual(d['assessment']['off_verdict'],'inconsistent')
                count[0]=0;fail[0]=3;a.out=str(Path(td)/'failed')
                with self.assertRaises(RuntimeError):native.native(a)
                d=read(Path(a.out)/'result.json');self.assertEqual(d['status'],'failed')
                self.assertEqual(d['SCF_evaluations'],3)
            METRICS['mock_SCF_count']=22

    def test_collect_missing_and_duplicates(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'plan.json';write(p,{})
            cases=[dict(label=label,key=key,geometry_sha256='b'*64) for label,(key,_) in CASES.items()]
            m=dict(registration='a'*40,cases=cases)
            root=Path(td)/'results';root.mkdir()
            for case in cases:
                for arm in ARMS:
                    dest=root/case['label']/arm
                    write(dest/'result.json',dict(plan_sha256=sha(p),label=case['label'],arm=arm,
                        status='diagnostic_complete',key=case['key'],geometry_sha256='b'*64,
                        SCF_evaluations=22,gradient_evaluations=3,assessment={'full_verdict':'inconclusive'},
                        response_grid_check={},wall_s=1.,packages={},upstream_sha256={}))
                    write(dest.with_name(arm+'.terminal.json'),dict(plan_sha256=sha(p),case=case['label'],arm=arm,status='completed',execution={'returncode':0}))
                    if arm=='pcm_pruned':write(dest/'layer.json',dict(explicit_energy_evaluations=22,gradient_evaluations=2))
            with patch.object(native,'load_plan',return_value=(p,m)):
                a=types.SimpleNamespace(plan=str(p),results=str(root),out=str(Path(td)/'all.json'))
                native.collect(a);self.assertTrue(read(a.out)['complete'])
                missing=root/'TEG'/'vacuum_pruned'/'result.json';missing.unlink()
                a.out=str(Path(td)/'missing.json')
                with self.assertRaises(SystemExit):native.collect(a)
                self.assertEqual(read(a.out)['completed_jobs'],7)
                src=root/'EG'/'pcm_pruned'/'result.json'
                write(root/'duplicate'/'result.json',read(src));a.out=str(Path(td)/'dupe.json')
                with self.assertRaises(ValueError):native.collect(a)

    def test_bound_failure_deadline_and_claim(self):
        from r7_common import bounded
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'one'
            r=bounded([sys.executable,'-c','raise SystemExit(2)'],p,2)
            self.assertEqual(r['execution_status'],'child_failed')
            with self.assertRaises(FileExistsError):bounded([sys.executable,'-c','pass'],p,2)
            r=bounded([sys.executable,'-c','import time;time.sleep(5)'],Path(td)/'two',.1)
            self.assertEqual(r['execution_status'],'deadline')
            # R7 bounded can label diagnostic_complete as completed despite rc!=0.
            # The R8 wrapper must still reject that operational failure.
            planfile=Path(td)/'plan.json';write(planfile,{})
            out=Path(td)/'late-failure'
            write(out/'result.json',dict(status='diagnostic_complete',assessment={'full_verdict':'consistent'}))
            a=types.SimpleNamespace(plan=str(planfile),case='TEG',arm='pcm_pruned',out=str(out))
            with patch.object(native,'load_plan',return_value=(planfile,{})), \
                 patch('r7_common.bounded',return_value={'execution_status':'completed','returncode':1}):
                with self.assertRaises(SystemExit):native.run(a)
            self.assertEqual(read(out.with_name(out.name+'.terminal.json'))['status'],'failed')

    def test_evidence_schema_and_retention(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            checks={model:{name:dict(requested=2302,finite_reference=n,finite_candidate=n,
                   coverage_identical=True,max_abs_change=.0121,median_abs_change=.00017)
                   for name in ('candidate_vs_control','candidate_vs_UD')}
                   for model,n in (('cosmosac_dsp',2271),('Z0x',2302))}
            runs=[dict(key=str(i),wall_s={'off':1.,'full':1.13}) for i in range(25)]
            write(root/'p32_calibration_gate.json',dict(rows=2302,targets=25,runs=runs,checks=checks,passed=False))
            rows=[dict(key=str(i),status='complete',screen_positive=True) for i in range(35)]
            rows += [dict(key=str(i),status='affinity_unresolved') for i in range(35,39)]+[dict(key='39',status='running')]
            write(root/'p34_primary_screen.json',dict(rows=rows))
            keys=['BKIMMITUMNQMOS','ZIBGPFATKBEMQZ','XTHFKEDIFFGKHM','LYCAIKOWRPUZTN','OKKJLVBELUTLKV']
            for i,k in enumerate(keys):
                key=k+'-UHFFFAOYSA-N'
                records=[dict(direction=str(j),full_verdict='inconclusive',off_verdict='inconclusive',
                    combined_indicator=1.,full_error=0.,off_error=0.,missing_response_material=None) for j in range(4)]
                write(root/'referee'/(key+'.result.json'),dict(key=key,status='diagnostic_complete' if i<4 else 'failed',records=records))
            with contextlib.redirect_stdout(io.StringIO()):a=audit(root,root/'out.json')
            self.assertEqual(a['P33']['completed'],4)
            self.assertFalse(a['P32']['chains_authorized']);self.assertIsNone(a['P32']['count_of_over_limit_queries'])
            (root/'referee'/(keys[0]+'-UHFFFAOYSA-N.result.json')).unlink()
            with self.assertRaises(ValueError):audit(root,root/'bad.json')


def main():
    p=argparse.ArgumentParser();p.add_argument('--out');a=p.parse_args()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(PortableTests)
    r=unittest.TextTestRunner(verbosity=2).run(suite)
    summary=dict(tests=r.testsRun,failures=len(r.failures),errors=len(r.errors),passed=r.wasSuccessful(),
        metrics=METRICS,scope='Portable and mocked orchestration only; no native PySCF or actual Mac-backed data')
    if a.out:write(a.out,summary)
    print(json.dumps(summary,indent=2))
    raise SystemExit(0 if r.wasSuccessful() else 1)


if __name__=='__main__':main()
