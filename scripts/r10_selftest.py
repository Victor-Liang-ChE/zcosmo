"""Portable tests of R10 bookkeeping/geometry math, not a UD or quantum calculation."""
from __future__ import annotations
import argparse
from contextlib import ExitStack
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch
import numpy as np
import pandas as pd
import r10_sources as src
import r10_replay as replay


def sigma_file(path,p,meta=None):
    m=meta or {'volume [A^3]':10.}
    text='# meta: '+json.dumps(m)+'\n'
    grid=np.round(np.linspace(-.025,.025,51),3)
    text+=''.join(f'{s:.3f} {a:.16e}\n' for s,a in zip(np.tile(grid,3),np.asarray(p).ravel()))
    Path(path).write_text(text)


def binning(values,grid):
    p=np.zeros(51)
    for sigma,area in np.asarray(values).reshape(-1,2):
        if not grid[0]<sigma<grid[-1]:raise ValueError('synthetic test sigma outside interior grid')
        left=min(int((sigma-grid[0])/(grid[1]-grid[0])),49)
        f=(sigma-grid[left])/(grid[left+1]-grid[left])
        p[left]+=area*(1-f);p[left+1]+=area*f
    return p


class TestSources(unittest.TestCase):
    def test_verified_catalog(self):
        c=src.catalog();self.assertEqual(len(c),14)
        self.assertEqual(len({r['relative_path'] for r in c}),14)
        self.assertEqual(len(src.DATA),12)
        for r in c:self.assertEqual(len(r['expected_git_blob']),40)
        aliases=[r for r in c if 'source_key' in r and r['source_key']!=r['key']]
        self.assertEqual(len(aliases),1)
        self.assertEqual(aliases[0]['source_key'],'DNIAPMSPPWPWGF-VKHMYHEASA-N')

    def test_exact_download_bytes(self):
        b=b'not real COSMO data\r\n'
        src.verify_download(b,src.blob(b))
        with self.assertRaises(ValueError):src.verify_download(b.replace(b'\r\n',b'\n'),src.blob(b))

    def test_frozen_input_mutation(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'file';p.write_bytes(b'original');r=src.record(p)
            self.assertEqual(src.verify_record(r),p.resolve())
            p.write_bytes(b'mutated')
            with self.assertRaises(ValueError):src.verify_record(r)

    def test_output_root_is_private_and_fresh(self):
        with self.assertRaises(ValueError):src.private_output(src.ROOT/'production')
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(FileExistsError):src.private_output(t)
            self.assertEqual(src.private_output(Path(t)/'new'),(Path(t)/'new').resolve())

    def test_json_rejects_nonfinite(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(ValueError):src.write(Path(t)/'bad.json',{'value':np.nan})

    def test_lookup_is_explicit_and_unique(self):
        key='DNIAPMSPPWPWGF-UHFFFAOYSA-N'
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);source=root/'DNIAPMSPPWPWGF-VKHMYHEASA-N.sigma';source.write_text('fixture')
            self.assertEqual(replay.historical_ud_path(root,key),source)
            (root/'DNIAPMSPPWPWGF-SYNTHETICA-N.sigma').write_text('another')
            with self.assertRaises(ValueError):replay.historical_ud_path(root,key)
            exact=root/(key+'.sigma');exact.write_text('exact fixture')
            self.assertEqual(replay.historical_ud_path(root,key),exact)


class TestArrays(unittest.TestCase):
    def test_sigma_roundtrip_and_wrong_order(self):
        rng=np.random.default_rng(20261007);p=rng.random((3,51))
        with tempfile.TemporaryDirectory() as t:
            f=Path(t)/'a.sigma';sigma_file(f,p)
            axis,q,_=replay.read_profile(f);self.assertLess(abs(p-q).max(),1e-15)
            lines=f.read_text().splitlines();lines[1]='0.024 1.0';f.write_text('\n'.join(lines))
            with self.assertRaises(ValueError):replay.read_profile(f)

    def test_sigma_nonfinite_and_negative(self):
        with tempfile.TemporaryDirectory() as t:
            f=Path(t)/'a.sigma';p=np.ones((3,51));p[0,0]=np.nan;sigma_file(f,p)
            with self.assertRaises(ValueError):replay.read_profile(f)
            p[0,0]=-1.;sigma_file(f,p)
            with self.assertRaises(ValueError):replay.read_profile(f)

    def test_npz_shapes_and_owner(self):
        with tempfile.TemporaryDirectory() as t:
            f=Path(t)/'s.npz'
            kw=dict(sym=np.array(['O','H','H']),x=np.eye(3),xyz=np.eye(3),q=np.zeros(3),area=np.ones(3),atom=np.arange(3))
            np.savez(f,**kw);self.assertEqual(replay.load_npz(f)[0],['O','H','H'])
            kw['atom']=np.array([0,1,3]);np.savez(f,**kw)
            with self.assertRaises(ValueError):replay.load_npz(f)
            kw['atom']=np.array([0.,1.,1.5]);np.savez(f,**kw)
            with self.assertRaises(ValueError):replay.load_npz(f)

    def test_stages_separate_raw_and_binned_tail(self):
        grid=np.arange(-.025,.025+.0001,.001)
        area=np.array([2.,3.]);q=np.array([.024,-.024]);av=np.array([.004,-.006])
        parser=types.SimpleNamespace(df=pd.DataFrame({'area / A^2':area,'charge / e':q,'atom':[1,2]}),
            df_atom=pd.DataFrame({'atom':['O','H'],'hb_class':['OH','OH']}),
            sigma_averaged=av,sigma_nhb=np.c_[av,area],sigma_OH=np.empty((0,2)),sigma_OT=np.empty((0,2)),
            area_A2=5.,volume_A3=10.)
        total=binning(np.c_[av,area],grid)
        result=types.SimpleNamespace(sigmas=grid,psigmaA_nhb=total.copy(),psigmaA_OH=np.zeros(51),psigmaA_OT=np.zeros(51))
        with patch.object(replay,'parser_module',return_value=types.SimpleNamespace(weightbin_sigmas=binning)):
            desc,_=replay.stages(parser,result)
            self.assertEqual(desc['raw_abs_tail_A2'],2.)
            self.assertEqual(desc['final_binned_tail_A2'],0.)
            result.psigmaA_nhb[25]+=1e-4
            with self.assertRaises(ValueError):replay.stages(parser,result)

    def test_printed_charge_audit_not_neutralization(self):
        text='''Sum of polarization charges = -0.01000
Sum of polarization charges(corr.) = 0.00000
1 1 0.00000 0.00000 0.00000 -0.00500 1.00000 -0.00500 0.0
2 1 1.00000 0.00000 0.00000 -0.00500 1.00000 -0.00500 0.0
'''
        r=replay.printed_charge_audit(text,-.01000)
        self.assertEqual(r['printed_segment_count'],2)
        self.assertAlmostEqual(r['charge_column_half_last_decimal_sum_e'],1e-5)
        self.assertTrue(r['header_candidates']['original']['rounding_consistent'])
        self.assertFalse(r['header_candidates']['corrected']['rounding_consistent'])

    def test_cavity_setting_is_not_actual_segment_count(self):
        text=''' Dielectric Constant = infinity
 Number of Segments = 92
 Molecular car file :
552.car
 COSMO-RS Atomic data
 1 O1 1.72 0.1 16.0 0.01
 2 H1 1.30 -0.1 8.0 -0.01
 Segment information:
 total number of segments: 406
'''
        d=replay.cavity_header(text)
        self.assertEqual(d['Number of Segments'],'92')
        self.assertEqual(d['actual_segment_record_count'],406)
        self.assertEqual(d['embedded_car_name'],'552.car')
        self.assertEqual(len(d['atomic_radii']),2)
        self.assertFalse(d['electronic_input_deck_verified'])


class TestGeometry(unittest.TestCase):
    def test_graph_permutation_and_symmetry(self):
        # Synthetic O-C-C-O graph with hydrogens. No geometry optimization.
        sym=['O','C','C','O','H','H','H','H','H','H']
        adj=[[1,4],[0,2,5,6],[1,3,7,8],[2,9],[0],[1],[1],[2],[2],[3]]
        perm=[3,2,1,0,9,8,7,6,5,4];inv={v:i for i,v in enumerate(perm)}
        sb=[sym[i] for i in perm];ab=[[inv[j] for j in adj[i]] for i in perm]
        maps=replay.graph_maps(sym,adj,sb,ab);self.assertEqual(len(maps),2)
        with self.assertRaises(ValueError):replay.graph_maps(sym,adj,sb,ab,limit=1)

    def test_graph_wrong_formula_or_connectivity(self):
        a=['C','O','H'];g=[[1],[0,2],[1]]
        with self.assertRaises(ValueError):replay.graph_maps(a,g,['C','N','H'],g)
        with self.assertRaises(ValueError):replay.graph_maps(a,g,a,[[1],[0],[]])

    def test_proper_rotation_rejects_reflection(self):
        rng=np.random.default_rng(4);x=rng.normal(size=(8,3))
        q,_=np.linalg.qr(rng.normal(size=(3,3)));q[:,0]*=np.linalg.det(q)
        self.assertLess(replay.proper_rmsd(x,x@q+[4,2,1]),2e-15)
        y=x.copy();y[:,0]*=-1
        self.assertGreater(replay.proper_rmsd(x,y),.1)

    def test_dihedral_periodicity_and_singularity(self):
        a=np.array([[1.,0,0],[0,0,0],[0,1,0],[0,1,1]])
        self.assertAlmostEqual(abs(replay.dihedral(a,(0,1,2,3))),90.)
        self.assertEqual(replay.delta_angle(179.,-179.),2.)
        self.assertIsNone(replay.dihedral(np.zeros((4,3)),(0,1,2,3)))


class TestResults(unittest.TestCase):
    def test_failure_does_not_drop_later_members(self):
        manifest={'rows':[dict(key=r[1],source_key=r[2]) for r in src.DATA],
                  'registration':{'commit':'a'*40},'packages':{}}
        bad=src.DATA[2][1]
        def member(r,ts):
            if r['key']==bad:raise ValueError('synthetic parity failure')
            return dict(key=r['key'],status='replay_passed',adopted=False)
        with tempfile.TemporaryDirectory() as t,ExitStack() as stack:
            p=Path(t)/'manifest.json';src.write(p,manifest)
            stack.enter_context(patch.object(replay,'mac'))
            stack.enter_context(patch.object(replay,'verify_manifest',return_value=manifest))
            stack.enter_context(patch.object(replay,'parser_module',return_value=None))
            stack.enter_context(patch.object(replay,'run_member',side_effect=member))
            rc=replay.compare(argparse.Namespace(manifest=str(p),plan_commit='b'*40,out=str(Path(t)/'out')))
            d=src.read(Path(t)/'out/summary.json')
            self.assertEqual(rc,2);self.assertEqual(d['processed'],12)
            self.assertEqual(sum(r['status']=='blocked' for r in d['rows']),1)
            self.assertFalse(d['all_lineage_gates_passed'])
            with self.assertRaises(ValueError):replay.check(argparse.Namespace(summary=Path(t)/'out/summary.json'))

    def test_checker_rejects_missing_or_duplicated_member(self):
        d=dict(schema=replay.SCHEMA,complete=True,all_lineage_gates_passed=True,
               rows=[dict(key=r[1],status='replay_passed') for r in src.DATA],SCF_calls=0,model_calls=0,adopted=False)
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'summary.json';src.write(p,d)
            self.assertEqual(replay.check(argparse.Namespace(summary=p)),0)
            d['rows'][-1]=d['rows'][0];src.write(p,d)
            with self.assertRaises(ValueError):replay.check(argparse.Namespace(summary=p))


    def test_member_adapter_and_lineage_gate(self):
        # Exercise run_member, not just the component routines. Synthetic water,
        # mocked legacy adapters; this is deliberately NOT an actual UD replay.
        sym=['O','H','H'];x=np.array([[0.,0,0],[.96,0,0],[-.24,.93,0]])
        area=np.array([2.,1.,1.]);charge=np.array([.01,-.005,-.005])
        avg=np.array([.004,-.003,-.003]);grid=np.arange(-.025,.025+.0001,.001)
        meta={'area [A^2]':4.,'volume [A^3]':10.,'r_av [A]':1.5,'f_decay':3.57,
              'disp. flag':'H2O','disp. e/kB [K]':70.,'averaging':'Hsieh','sigma_hb [e/A^2]':.0084}
        total=binning(np.c_[avg,area],grid)
        output=types.SimpleNamespace(sigmas=grid,psigmaA_nhb=total,
            psigmaA_OH=np.zeros(51),psigmaA_OT=np.zeros(51),meta=meta)
        def parser():
            return types.SimpleNamespace(
                df=pd.DataFrame({'area / A^2':area,'charge / e':charge,'atom':[1,2,3]}),
                df_atom=pd.DataFrame({'atom':sym,'hb_class':['OH']*3,
                                     'x / A':x[:,0],'y / A':x[:,1],'z / A':x[:,2]}),
                area_A2=4.,volume_A3=10.,sigma_averaged=avg,
                sigma_nhb=np.c_[avg,area],sigma_OH=np.empty((0,2)),sigma_OT=np.empty((0,2)),
                get_outputs=lambda:output)
        ts=types.SimpleNamespace(BOHR_TO_ANGSTROM=.52917721067,
             Dmol3COSMOParser=lambda *a,**k:parser(),weightbin_sigmas=binning)
        rc=types.ModuleType('r4_common')
        rc.parser_trace=lambda *a:(parser(),output,{})
        rc.contacts=lambda *a:{'atoms':[{'bonds':[1,2]},{'bonds':[0]},{'bonds':[0]}],'contacts':[]}
        z=types.ModuleType('zcosmo');z.__path__=[]
        pc=types.ModuleType('zcosmo.pyscf_cosmo');pc.BOHR=ts.BOHR_TO_ANGSTROM;pc.RADII={'H':1.3,'O':1.72}
        z.pyscf_cosmo=pc
        with tempfile.TemporaryDirectory() as t,ExitStack() as stack:
            root=Path(t);raw=root/'synthetic.cosmo'
            raw.write_text('''Dielectric Constant = infinity
COSMO-RS Atomic data
 1 O1 1.72 0.01 2.0 0.005
 2 H1 1.30 -0.005 1.0 -0.005
 3 H2 1.30 -0.005 1.0 -0.005
Segment information:
total number of segments: 3
Sum of polarization charges = 0.00000
1 1 0.0 0.0 0.0 0.01000 2.0 0.005 0.0
2 2 1.0 0.0 0.0 -0.00500 1.0 -0.005 0.0
3 3 0.0 1.0 0.0 -0.00500 1.0 -0.005 0.0
''')
            npz=root/'a.npz';np.savez(npz,sym=sym,x=x,xyz=x,area=area,q=charge,atom=np.arange(3))
            a=replay.output_array(output)
            for f in ('ud.sigma','old.sigma','primary.sigma'):sigma_file(root/f,a,meta)
            r=dict(key=src.DATA[0][1],source_key=src.DATA[0][2],stereo_alias=False,
                source_smiles='O',open_smiles='O',raw=src.record(raw),segments=src.record(npz),
                UD_profile=src.record(root/'ud.sigma'),archived_open_profile=src.record(root/'old.sigma'),
                primary_profile=src.record(root/'primary.sigma'))
            stack.enter_context(patch.dict('sys.modules',{'r4_common':rc,'zcosmo':z,'zcosmo.pyscf_cosmo':pc}))
            stack.enter_context(patch.object(replay,'parser_module',return_value=ts))
            d=replay.run_member(r,ts)
            self.assertEqual(d['status'],'replay_passed')
            self.assertEqual(d['geometry']['count'],1)
            self.assertFalse(d['mechanism_resolved'])
            self.assertLess(d['lineage_checks']['UD_max_raw_bin_A2'],1e-14)
            a[0,25]+=1e-5;sigma_file(root/'ud.sigma',a,meta)
            with self.assertRaises(ValueError):replay.run_member(r,ts)

    def test_mac_requirement_is_not_a_native_install_requirement(self):
        with patch.object(src.sys,'platform','linux'):
            with self.assertRaises(RuntimeError):src.mac()
        with patch.object(src.sys,'platform','darwin'):src.mac()


def main():
    p=argparse.ArgumentParser();p.add_argument('--out');a=p.parse_args()
    suite=unittest.defaultTestLoader.loadTestsFromModule(__import__(__name__))
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    summary=dict(tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),
                 passed=result.wasSuccessful(),scope='Portable synthetic checks only',SCF_calls=0,UD_comparisons=0)
    if a.out:src.write(a.out,summary)
    return 0 if result.wasSuccessful() else 1

if __name__=='__main__':raise SystemExit(main())
