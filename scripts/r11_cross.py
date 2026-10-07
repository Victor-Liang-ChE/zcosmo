"""P44: private Mac-only crossed single points. No optimization or scoring.

Use the already accepted R10 manifest and summary. Only a plan digest enters
Git. This module never uploads data or writes a production sigma file.
"""
from __future__ import annotations
import argparse
from contextlib import redirect_stdout, redirect_stderr
import hashlib
from importlib import import_module
from importlib.metadata import version
import json
import os
from pathlib import Path
import platform
import re
import signal
import subprocess
import sys
import time
import traceback
import numpy as np
from packaging.version import Version
import r10_sources as src
import r10_replay as replay
import r11_analysis as ana

BASE = '463ec1be5c0edfad1e8effd334a17fc44cd27405'
MARKER = 'R11-P44-P45: private fixed-geometry crossed profiles'
PLAN_RECORD = 'docs/astra/round11/PLAN_SHA256.txt'
SCHEMA = 'R11-cross-v1'
ROOT = Path(__file__).resolve().parents[1]
ARMS = ('RO', 'RU')
DESIGN = dict(SCF_limit=24, seconds_per_slot=900, total_run_seconds=22500,
    max_parallel=1, OMP_threads=4, BLAS_threads=1, memory_MB=4000, PCM_cache_MB=2000,
    gradients=0, optimizations=0, model_calls=0, no_retries=True,
    tail_floor_A2=ana.FLOOR_TAIL_A2, shape_floor_L1=ana.FLOOR_SHAPE_L1,
    dominance_remainder_fraction=.25, background_signal_factor=2.,
    control_names=list(ana.CONTROLS))
FILES = ['scripts/r11_analysis.py', 'scripts/r11_cross.py',
    'scripts/r10_sources.py', 'scripts/r10_replay.py', 'scripts/r4_charge.py',
    'scripts/r4_common.py', 'scripts/r3_common.py', 'scripts/r5_shape.py',
    'src/zcosmo/pyscf_cosmo.py', 'src/zcosmo/pcm_lu.py', 'data/raw/nist/to_sigma.py']
sha, read, write = src.sha, src.read, src.write


def mac_only():
    if sys.platform != 'darwin' or os.environ.get('GITHUB_ACTIONS') == 'true' or os.environ.get('CI') == 'true':
        raise RuntimeError('Private asset-bearing Mac only, never a CI worker')


def private_path(path, fresh=False):
    p = Path(path).expanduser().resolve()
    if p.is_relative_to(ROOT) or ROOT.is_relative_to(p):
        raise ValueError('Use private storage outside the repository')
    for a in (p, *p.parents):
        if (a/'.git').exists():
            raise ValueError('Private calculation data cannot be stored in another Git checkout')
    if fresh and p.exists():
        raise FileExistsError(p)
    return p


def no_custom_config():
    # PySCF also searches CWD/HOME when PYSCF_CONFIG_FILE is unset.
    candidates=(Path.cwd()/'.pyscf_conf.py', Path.home()/'.pyscf_conf.py')
    if os.environ.get('PYSCF_CONFIG_FILE') or any(p.is_file() for p in candidates):
        raise RuntimeError('Custom PySCF configuration is outside this registration')


def packages():
    d = {p:str(Version(version(p))) for p in
         ('numpy','scipy','pandas','rdkit','packaging','matplotlib','pyscf')}
    if d['pyscf'] != '2.14.0':
        raise RuntimeError('PySCF 2.14.0 is required; no dependency upgrade is authorized')
    d.update(python=platform.python_version(), machine=platform.machine())
    return d


def registration(commit):
    if not re.fullmatch('[0-9a-f]{40}', commit):
        raise ValueError('Full actual registration commit required')
    src.git('merge-base','--is-ancestor',BASE,'HEAD')
    src.git('merge-base','--is-ancestor',commit,'HEAD')
    text = src.git('show',commit+':PREREGISTRATION.md')
    if MARKER.encode() not in text:
        raise ValueError('Commit lacks the R11 registration marker')
    return dict(commit=commit, preregistration_sha256=hashlib.sha256(text).hexdigest())


def old_evidence(manifest, plan_commit, summary):
    with redirect_stdout(sys.stderr):
        m = replay.verify_manifest(manifest, plan_commit)
        replay.check(argparse.Namespace(summary=summary))
    s = read(summary)
    if (s['manifest_sha256'] != sha(manifest) or s['plan_commit'] != plan_commit or
        s['registration'] != m['registration'] or s['packages'] != m['packages']):
        raise ValueError('R10 lineage summary does not belong to these exact frozen inputs')
    return m, s


def freeze(a):
    mac_only(); no_custom_config(); os.umask(0o077)
    reg = registration(a.registration)
    old = private_path(a.r10_manifest); summary = private_path(a.r10_summary)
    m, s = old_evidence(old, a.r10_plan_commit, summary)
    native_packages = packages()
    sources = src.committed_sources(FILES)
    out = private_path(a.out, fresh=True)
    # No coordinate extraction, profile arithmetic or native work in this step.
    cases = []
    for r in m['rows']:
        order = list(ARMS)
        if int(hashlib.sha256(r['key'].encode()).hexdigest(), 16) % 2:
            order.reverse()
        cases.append(dict(name=r['name'], key=r['key'], order=order))
    if len(cases) != 12 or {r['key'] for r in cases} != {d[1] for d in src.DATA}:
        raise ValueError('Frozen twelve-member panel changed')
    out.mkdir(parents=True, mode=0o700)
    plan = dict(schema=SCHEMA, base=BASE, registration=reg, design=DESIGN,
        sources=sources, packages=native_packages, cases=cases,
        r10_manifest=src.record(old), r10_summary=src.record(summary),
        r10_plan_commit=a.r10_plan_commit,
        protected_population=m['protected_population'],
        coordinate_policy='Exact stored coordinates and atom order; no rotation, reflection, or centering',
        purpose='Ordered open-method coordinate contrast and remaining method bundle; no adoption')
    write(out/'plan.json', plan)
    (out/'PLAN_SHA256.txt').write_text(sha(out/'plan.json')+'\n')
    print('Private plan frozen; only its SHA256 may be committed:', sha(out/'plan.json'))
    return 0


def load_plan(path, plan_commit):
    no_custom_config()
    p = private_path(path); m = read(p)
    if (m['schema'] != SCHEMA or m['base'] != BASE or m['design'] != DESIGN or
        len(m['cases']) != 12 or {r['key'] for r in m['cases']} != {r[1] for r in src.DATA}):
        raise ValueError('Changed design or panel')
    if not re.fullmatch('[0-9a-f]{40}', plan_commit):
        raise ValueError('Full plan-record commit required')
    src.git('merge-base','--is-ancestor',plan_commit,'HEAD')
    src.git('merge-base','--is-ancestor',m['registration']['commit'],plan_commit)
    if src.git('show',plan_commit+':'+PLAN_RECORD).decode().strip() != sha(p):
        raise ValueError('Plan digest was not committed before native work')
    if registration(m['registration']['commit']) != m['registration'] or packages() != m['packages']:
        raise ValueError('Registration or environment drift')
    src.verify_sources(m['sources'])
    for r in [m['r10_manifest'], m['r10_summary'], *m['protected_population']]:
        src.verify_record(r)
    old, summary = old_evidence(m['r10_manifest']['path'], m['r10_plan_commit'], m['r10_summary']['path'])
    by = {r['key']:r for r in old['rows']}
    names = {r[1]:r[0] for r in src.DATA}
    for r in m['cases']:
        order = list(ARMS)
        if int(hashlib.sha256(r['key'].encode()).hexdigest(),16) % 2: order.reverse()
        if r['name'] != names[r['key']] or r['order'] != order or r['name'] != by[r['key']]['name']:
            raise ValueError('Changed member identity/order')
    return p, m, by, summary


def source_geometry(row, arm):
    if arm == 'RO':
        sym, xyz, _ = replay.load_npz(row['segments']['path'])
    elif arm == 'RU':
        df = replay.parser_module().get_atom_DataFrame(Path(row['raw']['path']).read_text())
        sym = list(df.atom)
        xyz = df[['x / A','y / A','z / A']].to_numpy(float)
    else:
        raise ValueError('Unknown arm')
    return replay.validate_geometry(sym, xyz)


def single_point(sym, xyz, progress):
    """Call the unchanged P25 factory once. Extra observations do not change SCF."""
    from pyscf import lib
    from r4_charge import factory, segments
    from zcosmo.pyscf_cosmo import RADII, BOHR
    lib.num_threads(4)
    mf = factory(sym, xyz, 0, 'def2-tzvp', 4000)
    s = mf.with_solvent
    from pyscf.data import elements
    want = np.zeros(120)
    for element, radius in RADII.items(): want[elements.charge(element)] = radius/BOHR
    if (mf.xc != 'b88,p86' or mf.grids.level != 3 or mf.conv_tol != 1e-9 or
        s.method != 'C-PCM' or s.eps != 1e9 or s.lebedev_order != 29 or
        s.surface_discretization_method.upper() != 'SWIG' or
        s.vdw_scale != 1. or not np.array_equal(s.radii_table, want) or
        getattr(mf.mol, 'spin', None) != 0):
        raise RuntimeError('P25 single-point settings changed')
    settings = dict(basis=str(mf.mol.basis), xc=mf.xc, grid_level=mf.grids.level,
        conv_tol=mf.conv_tol, conv_tol_grad=mf.conv_tol_grad,
        max_cycle=mf.max_cycle, small_rho_cutoff=float(mf.small_rho_cutoff),
        prune=getattr(mf.grids.prune,'__name__',str(mf.grids.prune)),
        surface_discretization=s.surface_discretization_method, eps=s.eps,
        method=s.method, lebedev_order=s.lebedev_order, vdw_scale=s.vdw_scale,
        radius_table_sha256=hashlib.sha256(s.radii_table.tobytes()).hexdigest())
    progress()
    energy = float(mf.kernel())
    if not mf.converged or not np.isfinite(energy):
        raise RuntimeError('SCF failed; no retry, alternate guess, or solver')
    dm = mf.make_rdm1(); overlap = mf.mol.intor_symmetric('int1e_ovlp')
    electron_error = float(np.einsum('ij,ji->',dm,overlap)-mf.mol.nelectron)
    it = s._intermediates; rhs = it['R']@it['v_grids']
    solve_error = float(np.max(abs(it['K']@it['q']-rhs))/max(1.,np.max(abs(rhs))))
    if abs(electron_error) > 1e-7 or solve_error > 1e-10:
        raise RuntimeError('Electron-count or PCM linear-system integrity failed')
    seg, keep = segments(s)
    allq = np.asarray(it['q']).ravel(); allarea = np.asarray(s.surface['area'])*BOHR**2
    drop = ~keep
    if (abs(float(allq.sum()-seg['q'].sum()-allq[drop].sum())) > 1e-12 or
        abs(float(allarea.sum()-seg['area'].sum()-allarea[drop].sum())) > 1e-9):
        raise RuntimeError('Retained/discarded surface accounting failed')
    audit = dict(surface_nodes=len(allq), retained_nodes=int(keep.sum()),
        discarded_nodes=int(drop.sum()), net_all_e=float(allq.sum()),
        net_kept_e=float(seg['q'].sum()), net_discarded_e=float(allq[drop].sum()),
        discarded_abs_charge_e=float(abs(allq[drop]).sum()), discarded_area_A2=float(allarea[drop].sum()),
        electron_error_e=electron_error, PCM_solve_relative_residual=solve_error,
        filter='surface area > 1e-8 bohr^2, unchanged P25 filter',
        raw_outliers=ana.outliers(seg['q'],seg['area']),
        all_surface_sigma_min=float((allq/allarea).min()),
        all_surface_sigma_max=float((allq/allarea).max()))
    aux = getattr(mf.with_df, 'auxmol', None)
    settings['auxiliary_basis'] = str(getattr(aux,'basis',getattr(mf.with_df,'auxbasis',None)))
    return seg, energy, dict(settings=settings, audit=audit, SCF_cycles=int(getattr(mf,'cycles',-1)))


def worker(a):
    mac_only(); os.umask(0o077)
    p, m, by, _ = load_plan(a.plan, a.plan_commit)
    if a.key not in by or a.arm not in ARMS:
        raise ValueError('Unrequested native identity')
    claim = read(p.parent/'execution_claim.json'); out = private_path(a.out, fresh=True)
    expected = Path(claim['output']).resolve()/a.key/a.arm
    if (claim['plan_sha256'] != sha(p) or out != expected or
        claim['nonce'] != os.environ.get('ZC_R11_NONCE') or claim['pid'] != os.getppid()):
        raise ValueError('Only the single claimed parent run may launch native slots')
    out.mkdir(parents=True, mode=0o700)
    status = dict(key=a.key, arm=a.arm, plan_sha256=sha(p), status='preparing',
                  SCF_attempted=0, SCF_converged=False, adopted=False)
    write(out/'result.json',status); start=time.monotonic()
    try:
        sym, xyz = source_geometry(by[a.key], a.arm)
        original = xyz.copy()
        def progress():
            status.update(status='SCF_running', SCF_attempted=1)
            write(out/'result.json',status)
        seg, energy, native = single_point(sym,xyz,progress)
        if not np.array_equal(xyz, original):
            raise RuntimeError('Native helper changed the input coordinates')
        upstream = {name:sha(import_module(name).__file__) for name in
            ('pyscf.dft.rks','pyscf.dft.gen_grid','pyscf.solvent.pcm','pyscf.df.df')}
        # Retain the private raw result even if subsequent profile binning fails.
        np.savez_compressed(out/'segments.npz',sym=np.array(sym),x=xyz,**seg)
        status.update(status='SCF_complete',SCF_converged=True,energy_Eh=energy,
            native=native,packages=m['packages'],upstream_sha256=upstream,
            geometry_input_sha256=by[a.key]['raw' if a.arm=='RU' else 'segments']['sha256'],
            segments_sha256=sha(out/'segments.npz'),wall_s=time.monotonic()-start)
        write(out/'result.json',status)
        from r4_common import parser_trace
        pp, output, _ = parser_trace(sym,xyz,seg)
        desc = ana.describe(pp,output)
        status.update(status='completed',descriptor=desc,wall_s=time.monotonic()-start)
        write(out/'result.json',status)
        return 0
    except Exception:
        status.update(failure_phase=status['status'],status='failed',wall_s=time.monotonic()-start)
        write(out/'result.json',status)
        traceback.print_exc()  # Parent redirects all output into private storage.
        return 2


def launch(command, log, seconds, env):
    """Kill the whole process group at the fixed ceiling; never retry a slot."""
    start=time.monotonic()
    with Path(log).open('xb') as f:
        proc=subprocess.Popen(command,stdout=f,stderr=subprocess.STDOUT,
                              start_new_session=True,env=env)
        try:
            rc=proc.wait(timeout=seconds); state='returned'
        except subprocess.TimeoutExpired:
            state='timeout'
            try:os.killpg(proc.pid,signal.SIGKILL)
            except ProcessLookupError:pass
            rc=proc.wait()
        except BaseException:
            try:os.killpg(proc.pid,signal.SIGKILL)
            except ProcessLookupError:pass
            proc.wait();raise
    return dict(execution_state=state,returncode=rc,wall_s=time.monotonic()-start)


def runner(a):
    mac_only(); os.umask(0o077)
    p, m, _by, _ = load_plan(a.plan, a.plan_commit)
    out=private_path(a.out,fresh=True)
    if out.is_relative_to(p.parent) or p.parent.is_relative_to(out):
        raise ValueError('Plan and native output must be separate private directories')
    no_custom_config()
    import secrets
    nonce=secrets.token_hex(24)
    claim=dict(plan_sha256=sha(p),output=str(out),pid=os.getpid(),nonce=nonce)
    # Permanent claim is the no-retry barrier. Interrupted plans are not resumed.
    with (p.parent/'execution_claim.json').open('x') as f:json.dump(claim,f)
    out.mkdir(parents=True,mode=0o700); start=time.monotonic(); terminals=[]
    env=os.environ.copy()
    env.update(OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',BLIS_NUM_THREADS='1',
        VECLIB_MAXIMUM_THREADS='1',NUMEXPR_NUM_THREADS='1',QC_MEM_MB='4000',
        ZC_PCM3C='1',ZC_PCM3C_MB='2000',ZC_R3_COOH_FLAG='1',MPLBACKEND='Agg',
        ZC_R11_NONCE=nonce,PYTHONPATH=str(ROOT/'src')+os.pathsep+str(ROOT/'scripts'))
    for case in m['cases']:
        for arm in case['order']:
            remaining=DESIGN['total_run_seconds']-(time.monotonic()-start)
            terminal=dict(key=case['key'],arm=arm,plan_sha256=sha(p),execution_state='not_run_budget',
                          returncode=None,wall_s=0.)
            folder=out/case['key']; folder.mkdir(exist_ok=True,mode=0o700)
            if remaining > 2:
                command=[sys.executable,str(ROOT/'scripts/r11_cross.py'),'_worker',
                    '--plan',str(p),'--plan-commit',a.plan_commit,'--key',case['key'],
                    '--arm',arm,'--out',str(folder/arm)]
                try:terminal.update(launch(command,folder/(arm+'.log'),min(900.,remaining),env))
                except Exception:
                    terminal.update(execution_state='launch_failed',returncode=None)
            terminal['slot_consumed']=terminal['execution_state']!='not_run_budget'
            write(folder/(arm+'.terminal.json'),terminal);terminals.append(terminal)
            write(out/'run.json',dict(plan_sha256=sha(p),plan_commit=a.plan_commit,
                requested=24,recorded=len(terminals),terminals=terminals,complete=False,
                wall_s=time.monotonic()-start))
    write(out/'run.json',dict(plan_sha256=sha(p),plan_commit=a.plan_commit,requested=24,
        recorded=24,terminals=terminals,complete=True,wall_s=time.monotonic()-start))
    return collect(argparse.Namespace(plan=str(p),plan_commit=a.plan_commit,run=str(out)))


def read_slot(run, key, arm, plan_hash, expected_packages, expected_input_hash):
    terminal=run/key/(arm+'.terminal.json'); result=run/key/arm/'result.json'
    if not terminal.is_file(): return None, 'missing_terminal'
    t=read(terminal)
    if (t.get('key'),t.get('arm'),t.get('plan_sha256')) != (key,arm,plan_hash):
        raise ValueError('Terminal identity mismatch')
    if t['execution_state']!='returned' or t['returncode']!=0 or not result.is_file():
        return None,t['execution_state'] if t['execution_state']!='returned' else 'failed'
    if not np.isfinite(t['wall_s']) or t['wall_s'] < 0 or t['wall_s'] > 905:
        raise ValueError('Native execution receipt exceeded its 900-second slot plus 5-second kill/accounting allowance')
    d=read(result)
    if ((d.get('key'),d.get('arm'),d.get('plan_sha256')) != (key,arm,plan_hash) or
        d.get('status')!='completed' or d.get('SCF_attempted')!=1 or
        d.get('SCF_converged') is not True or d.get('packages')!=expected_packages or
        d.get('geometry_input_sha256') != expected_input_hash or
        sha(result.parent/'segments.npz')!=d['segments_sha256']):
        raise ValueError('Native result identity, completion, or content mismatch')
    return d,'completed'


def public_summary(summary):
    """Allowlist only. No paths, logs, coordinates, raw rows, dense bins or energies."""
    def numbers(d, names):
        out={}
        for key in names:
            value=d.get(key)
            if value is not None and (not isinstance(value,(int,float,bool)) or not np.isfinite(value)):
                raise ValueError('Non-scalar field in public allowlist')
            out[key]=value
        return out
    def outlier_summary(d):
        ans=numbers(d,('segments','net_charge_e','area_A2','sigma_min','sigma_max'))
        ans['area_weighted_quantiles']=numbers(d['area_weighted_quantiles'],('p01','p05','p50','p95','p99'))
        for name in ('negative','positive'):
            ans[name]=numbers(d[name],('count','area_A2','area_fraction','signed_charge_e',
                                       'absolute_charge_e','minimum_area_A2'))
        return ans
    verdicts={r['key']:r for r in summary['classification'].get('rows',[])}
    expected={r[1]:r[0] for r in src.DATA};rows=[]
    for r in summary['rows']:
        if expected.get(r['key'])!=r['name']:raise ValueError('Unknown public member identity')
        z={k:r[k] for k in ('name','key','status')}
        if 'parity' in r:
            fields=('max_raw_bin_A2','normalized_L1','energy_Eh','net_charge_e','area_A2','volume_A3')
            z['parity']=dict(passed=r['parity']['passed'],checks=numbers(r['parity']['checks'],fields),
                             strict_limits=numbers(r['parity']['strict_limits'],fields))
        if r['key'] in verdicts:
            v=verdicts[r['key']]
            z['attribution']=dict(profile_gap_label=v['profile_gap_label'],
                shape=dict(numbers(v['shape'],('total_L1','geometry_L1','method_L1',
                     'cancellation_excess_L1','background_scale')),label=v['shape']['label']),tails={})
            for key in ana.TAILS:
                t=v['tails'][key]
                z['attribution']['tails'][key]=dict(numbers(t,('historical_total','historical_geometry',
                    'method','repeat_drift','current_total','current_geometry','background_scale_A2')),label=t['label'])
        if 'descriptors' in r:
            z['surface_audit']={}
            for arm in ('UD','P25','RO','RU'):
                desc=r['descriptors'][arm]
                z['surface_audit'][arm]=numbers(desc,(*ana.TAILS,'raw_q_sum_e','area_sum_A2','volume_A3'))
                z['surface_audit'][arm]['outliers']=outlier_summary(desc['outliers'])
        if 'native_audits' in r:
            z['native_integrity']={arm:numbers(r['native_audits'][arm],('surface_nodes','retained_nodes',
                'discarded_nodes','net_all_e','net_kept_e','net_discarded_e','discarded_abs_charge_e',
                'discarded_area_A2','electron_error_e','PCM_solve_relative_residual')) for arm in ARMS}
        rows.append(z)
    return dict(base=BASE,plan_sha256=summary['plan_sha256'],
        paired_integrity_passed=summary['paired_integrity_passed'],rows=rows,
        tail_scales_A2=summary['classification'].get('tail_scales_A2'),
        shape_scale_L1=summary['classification'].get('shape_scale_L1'),
        model_calls=0,optimizations=0,gradients=0,adopted=False,
        note='Ordered coordinate-input/method-bundle attribution only. Not a liquid-conformer rule or an accuracy score.')


def collect(a):
    mac_only(); collection_start=time.monotonic()
    p,m,by,old_summary=load_plan(a.plan,a.plan_commit)
    run=private_path(a.run);claim=read(p.parent/'execution_claim.json')
    if Path(claim['output']).resolve()!=run or claim['plan_sha256']!=sha(p):
        raise ValueError('Run differs from the single claimed output')
    if (run/'summary.json').exists() or (run/'public-summary.json').exists():
        raise FileExistsError('Collection already exists; no overwrite or selective replacement')
    ts=replay.parser_module();rows=[]
    old_by={r['key']:r for r in old_summary['rows']}
    for case in m['cases']:
        key=case['key'];r=by[key];row=dict(name=case['name'],key=key,status='incomplete')
        try:
            outcomes={};native={}
            for arm in ARMS:
                native[arm],outcomes[arm]=read_slot(run,key,arm,sha(p),m['packages'],r['raw' if arm=='RU' else 'segments']['sha256'])
            row['outcomes']=outcomes
            if any(native[a] is None for a in ARMS):
                rows.append(row);continue
            # Recheck exact lineage now, using unchanged files, before attribution.
            checked=replay.run_member(r,ts)
            if checked['status']!='replay_passed' or old_by[key]['status']!='replay_passed':
                raise ValueError('R10 lineage not reproduced')
            up=ts.Dmol3COSMOParser(r['raw']['path'],num_profiles=3,averaging='Hsieh')
            ud=ana.describe(up,up.get_outputs())
            osym,ox,seg=replay.load_npz(r['segments']['path'])
            from r4_common import parser_trace
            op,oo,_=parser_trace(osym,ox,seg);arch=ana.describe(op,oo)
            repeat=native['RO']['descriptor'];cross=native['RU']['descriptor']
            parity=ana.native_parity(arch,repeat,read(r['native']['path'])['energy_Eh'],native['RO']['energy_Eh'])
            row.update(status='paired_complete' if parity['passed'] else 'parity_failed',parity=parity,
                descriptors=dict(UD=ud,P25=arch,RO=repeat,RU=cross),
                math=ana.member_math(ud,arch,repeat,cross),
                native_audits={arm:native[arm]['native']['audit'] for arm in ARMS},
                native_hashes={arm:sha(run/key/arm/'result.json') for arm in ARMS})
        except Exception as e:
            row.update(status='integrity_failed',error=type(e).__name__+': '+str(e))
        rows.append(row)
    # Detect any package, code, historical-data, or protected-profile mutation.
    load_plan(a.plan,a.plan_commit)
    classification=ana.classify_panel(rows)
    d=dict(schema=SCHEMA,base=BASE,plan_sha256=sha(p),plan_commit=a.plan_commit,
        requested_members=12,requested_native_slots=24,rows=rows,
        paired_integrity_passed=all(r['status']=='paired_complete' for r in rows),
        classification=classification,protected_population_unchanged=True,
        adopted=False,model_calls=0,gradients=0,optimizations=0,
        zero_QC_collection_wall_s=time.monotonic()-collection_start)
    write(run/'summary.json',d)
    write(run/'public-summary.json',public_summary(d))
    print('Collected private crossed-profile run. Paired integrity passed:',d['paired_integrity_passed'])
    return 0 if d['paired_integrity_passed'] else 2


def check(a):
    mac_only();p,m,by,_=load_plan(a.plan,a.plan_commit);run=private_path(a.run)
    d=read(run/'summary.json')
    if d.get('schema')!=SCHEMA or d.get('plan_sha256')!=sha(p):raise ValueError('Different summary')
    if len(d['rows'])!=12 or {r['key'] for r in d['rows']}!=set(by):raise ValueError('Lost member')
    if not d.get('paired_integrity_passed') or not d.get('protected_population_unchanged'):
        raise ValueError('Panel incomplete or parity/protection gate failed')
    if any(d.get(k)!=0 for k in ('model_calls','gradients','optimizations')) or d.get('adopted') is not False:
        raise ValueError('Unregistered computation or adoption')
    for row in d['rows']:
        for arm in ARMS:
            native,state=read_slot(run,row['key'],arm,sha(p),m['packages'],
                by[row['key']]['raw' if arm=='RU' else 'segments']['sha256'])
            if state!='completed' or sha(run/row['key']/arm/'result.json')!=row['native_hashes'][arm]:
                raise ValueError('Native result changed after collection')
            if (row['descriptors'][arm]!=native['descriptor'] or
                row['native_audits'][arm]!=native['native']['audit']):
                raise ValueError('Summary no longer matches the native descriptor or audit')
        ds=row['descriptors']
        parity=ana.native_parity(ds['P25'],ds['RO'],read(by[row['key']]['native']['path'])['energy_Eh'],
            read(run/row['key']/'RO/result.json')['energy_Eh'])
        if parity!=row['parity'] or not parity['passed']:raise ValueError('Parity was not reproduced')
        if ana.member_math(ds['UD'],ds['P25'],ds['RO'],ds['RU'])!=row['math']:
            raise ValueError('Decomposition changed')
    if ana.classify_panel(d['rows'])!=d['classification']:
        raise ValueError('Classification was not reproduced')
    if public_summary(d)!=read(run/'public-summary.json'):
        raise ValueError('Public allowlist summary changed')
    print('24 one-SCF slots and 12 parity checks verified. No production adoption authorized.')
    return 0


def main():
    if Path.cwd().resolve()!=ROOT:raise ValueError('Run from this checkout root')
    ap=argparse.ArgumentParser(description=__doc__);sp=ap.add_subparsers(dest='cmd',required=True)
    q=sp.add_parser('freeze');q.add_argument('--registration',required=True)
    q.add_argument('--r10-manifest',required=True);q.add_argument('--r10-summary',required=True)
    q.add_argument('--r10-plan-commit',required=True);q.add_argument('--out',required=True);q.set_defaults(fn=freeze)
    for name,fn in (('run',runner),('collect',collect),('check',check),('_worker',worker)):
        q=sp.add_parser(name);q.add_argument('--plan',required=True);q.add_argument('--plan-commit',required=True)
        if name in ('collect','check'):q.add_argument('--run',required=True)
        else:q.add_argument('--out',required=True)
        if name=='_worker':q.add_argument('--key',required=True);q.add_argument('--arm',choices=ARMS,required=True)
        q.set_defaults(fn=fn)
    a=ap.parse_args();return a.fn(a)

if __name__=='__main__':raise SystemExit(main())
