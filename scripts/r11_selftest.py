"""Portable synthetic tests. No UD data and no PySCF calculation are used."""
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
import r11_analysis as a
import r11_cross as x
import r10_sources as src


def desc(tail=5., area=100.):
    p=np.zeros((3,51));p[0,25]=area-tail;p[1,40]=tail
    d=dict(post_HB_bins_A2=p.tolist(),raw_abs_tail_A2=tail,
        averaged_segment_abs_tail_A2=tail,final_binned_tail_A2=tail,
        raw_q_sum_e=-.02,area_sum_A2=area,volume_A3=80.)
    d['outliers']=a.outliers(np.array([-.02,.0]),np.array([1.,area-1]))
    return d


def panel():
    rows=[]
    for name,key,*_ in src.DATA:
        arch=desc();repeat=desc();cross=desc(5.05);ud=desc(5.1)
        if name not in a.CONTROLS:
            cross=desc(13.);ud=desc(15.)
        rows.append(dict(name=name,key=key,status='paired_complete',
            parity=a.native_parity(arch,repeat,-3.,-3.),
            math=a.member_math(ud,arch,repeat,cross),
            descriptors=dict(UD=ud,P25=arch,RO=repeat,RU=cross)))
    return rows


class Arithmetic(unittest.TestCase):
    def test_telescoping_and_repeat_drift(self):
        z=a.split(np.array([4.,2.]),np.array([1.,1.]),np.array([1.01,.99]),np.array([3.,1.5]))
        np.testing.assert_allclose(np.array(z['current_geometry'])+z['method'],z['current_total'])
        np.testing.assert_allclose(np.array(z['current_geometry'])+z['repeat_drift'],z['historical_geometry'])

    def test_scalar_negative_and_positive_gap(self):
        for sign in (-1.,1.):
            self.assertEqual(a.scalar_verdict(sign*10,sign*9,sign, .5),'mainly_geometry')
            self.assertEqual(a.scalar_verdict(sign*10,sign,sign*9,.5),'mainly_method')
            self.assertEqual(a.scalar_verdict(sign*10,sign*5,sign*5,.5),'both')

    def test_cancellation_is_not_dominance(self):
        self.assertEqual(a.scalar_verdict(10,20,-10,.5),'inconclusive_cancellation')
        d=np.array([1.,-1.]);g=np.array([10.,0.]);m=d-g
        self.assertEqual(a.vector_verdict(d,g,m,.01)['label'],'inconclusive_cancellation')

    def test_small_and_exact_boundary(self):
        self.assertEqual(a.scalar_verdict(1,.9,.1,.5),'inconclusive_small_contrast')
        self.assertEqual(a.scalar_verdict(10,7.5,2.5,.5),'mainly_geometry')
        self.assertEqual(a.scalar_verdict(10,7.499,2.501,.5),'both')

    def test_nonfinite_and_broken_identity_rejected(self):
        with self.assertRaises(ValueError):a.scalar_verdict(1,np.nan,0,.5)
        with self.assertRaises(ValueError):a.vector_verdict([1],[0],[0],.1)
        with self.assertRaises(ValueError):a.split([1],[1,2],[1],[1])

    def test_normalize_each_profile_before_subtraction(self):
        z=a.member_math(desc(10,200),desc(5,100),desc(5,100),desc(10,200))
        self.assertAlmostEqual(a.norm(z['normalized_profile']['historical_total']),0.)
        self.assertGreater(a.norm(z['area_profile']['historical_total']),0.)

    def test_native_parity_and_strict_limit(self):
        self.assertTrue(a.native_parity(desc(),desc(),-3.,-3.)['passed'])
        d=desc();d['post_HB_bins_A2'][0][25]+=1.1e-4
        self.assertFalse(a.native_parity(desc(),d,-3.,-3.)['passed'])
        self.assertFalse(a.native_parity(desc(),desc(),-3.,-2.999)['passed'])

    def test_outliers_are_area_weighted(self):
        d=a.outliers(np.array([-.1e-6,.01,.0]),np.array([1e-6,1.,99.]))
        self.assertEqual(d['negative']['count'],1)
        self.assertLess(d['negative']['area_fraction'],1.1e-8)
        self.assertEqual(d['area_weighted_quantiles']['p50'],0.)
        self.assertAlmostEqual(d['net_charge_e'],.01-.1e-6)

    def test_profile_validation(self):
        with self.assertRaises(ValueError):a.profiles(np.zeros((3,51)))
        with self.assertRaises(ValueError):a.outliers([1.],[0.])

    def test_panel_controls_and_signed_targets(self):
        d=a.classify_panel(panel());self.assertTrue(d['complete'])
        for r in d['rows']:
            expected='background_control_descriptive_only' if r['name'] in a.CONTROLS else 'mainly_geometry'
            self.assertEqual(r['profile_gap_label'],expected)
        self.assertEqual(d['tail_scales_A2']['final_binned_tail_A2'],.5)

    def test_panel_failure_blocks_all_labels(self):
        r=panel();r[0]['status']='failed'
        self.assertFalse(a.classify_panel(r)['complete'])
        r=panel();r[0]['parity']['passed']=False
        self.assertFalse(a.classify_panel(r)['complete'])
        with self.assertRaises(ValueError):a.classify_panel(r[:-1])
        r[-1]=r[0]
        with self.assertRaises(ValueError):a.classify_panel(r)

    def test_background_not_selected_for_agreement(self):
        r=panel();c=next(z for z in r if z['name']=='water')
        c['math']=a.member_math(desc(20),desc(),desc(),desc(5.1))
        d=a.classify_panel(r)
        self.assertEqual(d['tail_scales_A2']['raw_abs_tail_A2'],15.)
        self.assertTrue(all(z['tails']['raw_abs_tail_A2']['label']=='inconclusive_small_contrast' for z in d['rows']))


class Execution(unittest.TestCase):
    def test_mac_and_ci_guards(self):
        with patch.object(sys,'platform','linux'):
            with self.assertRaises(RuntimeError):x.mac_only()
        with patch.object(sys,'platform','darwin'),patch.dict(os.environ,{'GITHUB_ACTIONS':'true'}):
            with self.assertRaises(RuntimeError):x.mac_only()

    def test_custom_configs_block_before_native_import(self):
        with tempfile.TemporaryDirectory() as t, ExitStack() as stack:
            home=Path(t); cwd=home/'working';cwd.mkdir()
            stack.enter_context(patch.object(Path,'home',return_value=home))
            stack.enter_context(patch.object(Path,'cwd',return_value=cwd))
            stack.enter_context(patch.dict(os.environ,{'PYSCF_CONFIG_FILE':''}))
            x.no_custom_config()
            (home/'.pyscf_conf.py').write_text('# fixture')
            with self.assertRaises(RuntimeError):x.no_custom_config()
            (home/'.pyscf_conf.py').unlink()
            (cwd/'.pyscf_conf.py').write_text('# fixture')
            with self.assertRaises(RuntimeError):x.no_custom_config()
            (cwd/'.pyscf_conf.py').unlink()
            with patch.dict(os.environ,{'PYSCF_CONFIG_FILE':'some-config'}):
                with self.assertRaises(RuntimeError):x.no_custom_config()

    def test_private_paths_resolve_aliases(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);(p/'real').mkdir();(p/'alias').symlink_to(p/'real',target_is_directory=True)
            self.assertEqual(x.private_path(p/'alias/new'),(p/'real/new').resolve())
            (p/'real/.git').mkdir()
            with self.assertRaises(ValueError):x.private_path(p/'alias/new')
        with self.assertRaises(ValueError):x.private_path(x.ROOT/'private')

    def test_process_group_deadline(self):
        with tempfile.TemporaryDirectory() as t:
            d=x.launch([sys.executable,'-c','import time; time.sleep(10)'],Path(t)/'log',.05,os.environ.copy())
            self.assertEqual(d['execution_state'],'timeout');self.assertNotEqual(d['returncode'],0)
            self.assertLess(d['wall_s'],3.)

    def test_single_point_has_one_kernel_and_no_gradients(self):
        from types import SimpleNamespace as N
        bohr=.52917721067;radii={'H':1.3,'C':2.,'O':1.72};nums={'H':1,'C':6,'O':8}
        rt=np.zeros(120)
        for k,v in radii.items():rt[nums[k]]=v/bohr
        allq=np.array([.01,-.01,1e-14]);ab=np.array([1.,1.,1e-10])
        solvent=N(method='C-PCM',eps=1e9,lebedev_order=29,vdw_scale=1.,radii_table=rt,
                  surface_discretization_method='SWIG',surface={'area':ab},
                  _intermediates={'K':np.eye(3),'R':np.eye(3),'q':allq,'v_grids':allq})
        counts={'kernel':0,'progress':0}
        def kernel():counts['kernel']+=1;return -3.
        mol=N(basis='def2-tzvp',spin=0,nelectron=1,intor_symmetric=lambda name:np.eye(1))
        mf=N(xc='b88,p86',grids=N(level=3,prune=None),conv_tol=1e-9,conv_tol_grad=None,
             max_cycle=50,small_rho_cutoff=0.,mol=mol,with_solvent=solvent,converged=True,
             kernel=kernel,make_rdm1=lambda:np.eye(1),with_df=N(auxmol=None,auxbasis='fixture'),cycles=2)
        seg=dict(xyz=np.zeros((2,3)),q=allq[:2],area=ab[:2]*bohr**2,atom=np.array([0,1]))
        fakepc=types.ModuleType('zcosmo.pyscf_cosmo');fakepc.RADII=radii;fakepc.BOHR=bohr
        fakez=types.ModuleType('zcosmo');fakez.__path__=[]
        fakepyscf=types.ModuleType('pyscf');fakepyscf.lib=N(num_threads=lambda n:None)
        fakedata=types.ModuleType('pyscf.data');fakedata.elements=N(charge=lambda x:nums[x])
        fakecharge=types.ModuleType('r4_charge')
        fakecharge.factory=lambda sym,xyz,spin,basis,memory:mf
        fakecharge.segments=lambda s:(seg,ab>1e-8)
        def progress():counts['progress']+=1
        with patch.dict(sys.modules,{'pyscf':fakepyscf,'pyscf.data':fakedata,
            'zcosmo':fakez,'zcosmo.pyscf_cosmo':fakepc,'r4_charge':fakecharge}):
            out,e,d=x.single_point(['O','H'],np.zeros((2,3)),progress)
        self.assertEqual(counts,{'kernel':1,'progress':1})
        self.assertEqual(d['audit']['discarded_nodes'],1)
        self.assertEqual(e,-3.)

    def test_parser_failure_preserves_the_completed_raw_single_point(self):
        with tempfile.TemporaryDirectory() as t, ExitStack() as stack:
            root=Path(t);p=root/'plan/plan.json';src.write(p,{'fixture':True})
            key=src.DATA[0][1];run=root/'run';run.mkdir();out=run/key/'RU'
            src.write(p.parent/'execution_claim.json',dict(output=str(run),plan_sha256=src.sha(p),
                                                         nonce='fixture',pid=os.getppid()))
            row=dict(raw={'sha256':'a'*64})
            stack.enter_context(patch.object(x,'mac_only'))
            stack.enter_context(patch.object(x,'load_plan',return_value=(p,{'packages':{}},{key:row},{})))
            stack.enter_context(patch.dict(os.environ,{'ZC_R11_NONCE':'fixture'}))
            stack.enter_context(patch.object(x,'source_geometry',return_value=(['O'],np.zeros((1,3)))))
            seg=dict(xyz=np.zeros((1,3)),q=np.array([-.01]),area=np.array([1.]),atom=np.array([0]))
            def native(sym,xyz,progress):
                progress();return seg,-3.,{'audit':{'net_kept_e':-.01}}
            stack.enter_context(patch.object(x,'single_point',side_effect=native))
            stack.enter_context(patch.object(x,'import_module',return_value=types.SimpleNamespace(__file__=str(p))))
            fake=types.ModuleType('r4_common')
            def bad_parser(*args):raise ValueError('Synthetic bin-domain failure')
            fake.parser_trace=bad_parser
            stack.enter_context(patch.dict(sys.modules,{'r4_common':fake}))
            stack.enter_context(patch.object(x.traceback,'print_exc'))
            rc=x.worker(argparse.Namespace(plan=str(p),plan_commit='b'*40,key=key,arm='RU',out=str(out)))
            record=read_json(out/'result.json')
            self.assertEqual(rc,2);self.assertEqual(record['SCF_attempted'],1)
            self.assertTrue(record['SCF_converged']);self.assertEqual(record['failure_phase'],'SCF_complete')
            self.assertTrue((out/'segments.npz').is_file())
            self.assertEqual(record['native']['audit']['net_kept_e'],-.01)

    def test_runner_preserves_failed_slots_and_no_retry(self):
        with tempfile.TemporaryDirectory() as t,ExitStack() as stack:
            root=Path(t);p=root/'plan/plan.json';src.write(p,{'fixture':True})
            cases=[dict(name=n,key=k,order=['RO','RU']) for n,k,*_ in src.DATA]
            m=dict(cases=cases,packages={})
            stack.enter_context(patch.object(x,'mac_only'))
            stack.enter_context(patch.object(x,'load_plan',return_value=(p,m,{},{})))
            stack.enter_context(patch.object(x,'collect',return_value=2))
            count=[]
            def launch(cmd,log,secs,env):
                count.append(cmd);return dict(execution_state='returned',returncode=2 if len(count)==1 else 0,wall_s=.001)
            stack.enter_context(patch.object(x,'launch',side_effect=launch))
            args=argparse.Namespace(plan=str(p),plan_commit='a'*40,out=str(root/'run'))
            self.assertEqual(x.runner(args),2);self.assertEqual(len(count),24)
            run=read_json(root/'run/run.json')
            self.assertEqual(run['recorded'],24);self.assertTrue(run['complete'])
            args.out=str(root/'another')
            with self.assertRaises(FileExistsError):x.runner(args)

    def test_aggregate_has_no_dense_or_coordinate_fields(self):
        rows=panel();d=dict(rows=rows,classification=a.classify_panel(rows),plan_sha256='a'*64,paired_integrity_passed=True)
        for r in rows:
            r['path']='/private/secret';r['coordinates']=[[1,2,3]]
            r['descriptors']['UD']['xyz']=[[1,2,3]]
        text=json.dumps(x.public_summary(d))
        for forbidden in ('coordinates','post_HB_bins','pre_HB_bins','/private','xyz'):
            self.assertNotIn(forbidden,text)


def read_json(p):return json.loads(Path(p).read_text())


class Integration(unittest.TestCase):
    def fixture(self, root):
        p=root/'plan/plan.json';src.write(p,{'synthetic':True});run=root/'run';run.mkdir()
        src.write(p.parent/'execution_claim.json',dict(output=str(run),plan_sha256=src.sha(p)))
        m=dict(packages={'fixture':'1'},cases=[dict(name=n,key=k) for n,k,*_ in src.DATA])
        by={};old=dict(rows=[]);descmap={}
        for r in panel():
            key=r['key'];local=root/'inputs'/key;local.mkdir(parents=True)
            src.write(local/'native.json',{'energy_Eh':-3.})
            raw=local/'synthetic.cosmo';raw.write_text('SYNTHETIC NO UD DATA')
            by[key]=dict(key=key,raw={'path':str(raw),'sha256':'u'*64},segments={'path':str(local/'old.npz'),'sha256':'o'*64},
                         native={'path':str(local/'native.json')})
            descmap[str(raw)]=r['descriptors']['UD'];descmap[str(local/'old.npz')]=r['descriptors']['P25']
            old['rows'].append(dict(key=key,status='replay_passed'))
            for arm in ('RO','RU'):
                d=run/key/arm;d.mkdir(parents=True)
                (d/'segments.npz').write_bytes(b'synthetic NPZ stand-in')
                native=dict(key=key,arm=arm,plan_sha256=src.sha(p),status='completed',SCF_attempted=1,
                    SCF_converged=True,packages=m['packages'],energy_Eh=-3.,descriptor=r['descriptors'][arm],
                    native={'audit':{'synthetic':True}},geometry_input_sha256=('u' if arm=='RU' else 'o')*64,segments_sha256=src.sha(d/'segments.npz'))
                src.write(d/'result.json',native)
                src.write(run/key/(arm+'.terminal.json'),dict(key=key,arm=arm,plan_sha256=src.sha(p),
                    execution_state='returned',returncode=0,wall_s=.01))
        return p,run,m,by,old,descmap

    def execute(self, root, broken=False):
        p,run,m,by,old,descmap=self.fixture(root)
        fakecommon=types.ModuleType('r4_common')
        fakecommon.parser_trace=lambda sym,xyz,seg:(None,types.SimpleNamespace(desc=seg['fixture']),None)
        fakeparser=types.SimpleNamespace(Dmol3COSMOParser=lambda path,**kw:
            types.SimpleNamespace(get_outputs=lambda:types.SimpleNamespace(desc=descmap[path])))
        if broken:(run/src.DATA[0][1]/'RU/segments.npz').write_bytes(b'mutated')
        with ExitStack() as s:
            s.enter_context(patch.object(x,'mac_only'))
            s.enter_context(patch.object(x,'load_plan',return_value=(p,m,by,old)))
            s.enter_context(patch.object(x.replay,'parser_module',return_value=fakeparser))
            s.enter_context(patch.object(x.replay,'run_member',return_value={'status':'replay_passed'}))
            s.enter_context(patch.object(x.replay,'load_npz',side_effect=lambda path:(['O'],np.zeros((1,3)),{'fixture':descmap[path]})))
            s.enter_context(patch.object(a,'describe',side_effect=lambda pp,output:output.desc))
            s.enter_context(patch.dict(sys.modules,{'r4_common':fakecommon}))
            args=argparse.Namespace(plan=str(p),plan_commit='b'*40,run=str(run))
            rc=x.collect(args);d=read_json(run/'summary.json')
            if not broken:
                self.assertEqual(x.check(args),0)
                altered=copy.deepcopy(d)
                altered['rows'][1]['descriptors']['RU']['raw_q_sum_e']+=.1
                ds=altered['rows'][1]['descriptors']
                altered['rows'][1]['math']=a.member_math(ds['UD'],ds['P25'],ds['RO'],ds['RU'])
                src.write(run/'summary.json',altered)
                with self.assertRaises(ValueError):x.check(args)
                src.write(run/'summary.json',d)
                native=run/src.DATA[1][1]/'RU/result.json';q=read_json(native);q['energy_Eh']=999.;src.write(native,q)
                with self.assertRaises(ValueError):x.check(args)
            return rc,d

    def test_all_twelve_and_independent_check(self):
        with tempfile.TemporaryDirectory() as t:
            rc,d=self.execute(Path(t));self.assertEqual(rc,0)
            self.assertEqual(len(d['rows']),12);self.assertTrue(d['paired_integrity_passed'])

    def test_mutated_slot_retained_and_blocks_classification(self):
        with tempfile.TemporaryDirectory() as t:
            rc,d=self.execute(Path(t),True);self.assertEqual(rc,2)
            self.assertEqual(len(d['rows']),12);self.assertFalse(d['classification']['complete'])
            self.assertEqual(d['rows'][0]['status'],'integrity_failed')
            self.assertEqual(d['rows'][-1]['status'],'paired_complete')


if __name__=='__main__':unittest.main()
