"""Run a frozen local job manifest with per-job locks, deadlines and explicit outcomes.

A censored member cannot prevent independent later members from running.
No retries, shell evaluation, workflow dispatch or stale-lock deletion are performed.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from r6_common import sha,write,fresh,registration,check_inputs


def execute(jobs,out,cwd,reg):
    out=fresh(out);summary=[]
    ids=[j['id'] for j in jobs]
    if len(set(ids))!=len(ids) or not ids:raise ValueError('nonempty unique job ids required')
    for j in jobs:
        if not j['id'].replace('-','').replace('_','').isalnum():raise ValueError('unsafe job id')
        command=j['argv'];limit=float(j['timeout_s'])
        if not isinstance(command,list) or not command or not all(isinstance(v,str) for v in command):
            raise ValueError('argv must be a nonempty string array, not a shell command')
        if not 0<limit<=7200:raise ValueError('per-job timeout must be in (0,7200] seconds')
        check_inputs(j.get('inputs',{}))
        lock=Path(j['lock']).resolve();lock.parent.mkdir(parents=True,exist_ok=True)
        # The manifest must assign the SAME lock to every writer of one output/checkpoint.
        try:fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
        except FileExistsError:
            summary.append(dict(id=j['id'],status='locked_not_run'));write(out/'jobs.json',summary);continue
        os.write(fd,json.dumps(dict(pid=os.getpid(),job=j['id'],registration=reg)).encode());os.close(fd)
        started=time.perf_counter();p=None
        try:
            env=dict(os.environ);env.update(j.get('env',{}))
            with (out/(j['id']+'.log')).open('wb') as f:
                p=subprocess.Popen(command,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
                timedout=False
                try:rc=p.wait(timeout=limit)
                except subprocess.TimeoutExpired:
                    timedout=True
                    os.killpg(p.pid,signal.SIGTERM)
                    try:rc=p.wait(timeout=10)
                    except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);rc=p.wait()
            status='deadline' if timedout else ('completed' if rc==0 else 'censored' if rc==2 else 'failed')
            summary.append(dict(id=j['id'],status=status,returncode=rc,wall_s=time.perf_counter()-started,
                                command=command,registration=reg))
        except Exception as ex:
            summary.append(dict(id=j['id'],status='failed',error=repr(ex),wall_s=time.perf_counter()-started))
        finally:
            if p is not None and p.poll() is None:
                os.killpg(p.pid,signal.SIGKILL);p.wait()
            # Deliberately retained after an outer SIGKILL, which requires human review.
            lock.unlink(missing_ok=True)
        write(out/'jobs.json',summary)
    return 0 if all(r['status']=='completed' for r in summary) else 2



def plan_referee(a):
    reg=registration(a.registration);out=fresh(a.out);cases=[]
    root=Path(a.artifacts);inputs={}
    plan=Path('cloud/r5/shape-plan/manifest.json');manifest=json.loads(plan.read_text());inputs[str(plan.resolve())]=sha(plan)
    # Structural calibration controls, chosen before any new numerical result.
    for name in ('methanol','ethylene_glycol'):
        r=next(q for q in manifest['panel'] if q['name']==name)
        gp=plan.parent/r['geometry']
        if sha(gp)!=r['geometry_sha256']:raise ValueError('control geometry differs from frozen R5 bytes')
        cases.append(dict(id=name,key=r['key'],smiles=r['smiles'],source=gp,spin=r['spin']))
    targets=[('BKIMMITUMNQMOS-UHFFFAOYSA-N',20261006,1),
             ('ZIBGPFATKBEMQZ-UHFFFAOYSA-N',20261006,1),
             ('XTHFKEDIFFGKHM-UHFFFAOYSA-N',20261005,1)]
    for key,seed,rank in targets:
        pp=Path('cloud/r5/proposals')/key/f's{seed}-c{rank}.json'
        if not pp.is_file():raise FileNotFoundError(pp)
        proposal=json.loads(pp.read_text());identity=sha(pp);hits=[]
        for path in root.rglob('result.json'):
            r=json.loads(path.read_text())
            if r.get('input_sha256')==identity:hits.append((path,r))
        if len(hits)!=1:raise ValueError('exactly one archived result required for each frozen censored member')
        path,r=hits[0]
        if r['status']!='censored' or r['evaluations']!=80:raise ValueError('the frozen censoring result changed')
        gp=path.parent/'latest.json'
        cases.append(dict(id=key[:14],key=key,smiles=proposal['smiles'],source=gp,spin=proposal['spin']))
        inputs[str(path.resolve())]=sha(path);inputs[str(pp.resolve())]=identity
    env=dict(OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',ZC_PCM3C_MB='2000',ZC_PCM3C='1',PYTHONPATH='src:scripts')
    jobs=[];records=[]
    for r in cases:
        gp=out/'geometries'/(r['id']+'.json');gp.parent.mkdir(exist_ok=True)
        gp.write_bytes(Path(r['source']).read_bytes());inputs[str(gp)]=sha(gp)
        dest=out/'consistency'/r['id']
        jobs.append(dict(id=r['id'],argv=[sys.executable,str(Path('scripts/r6_referee.py').resolve()),'consistency',
            '--geometry',str(gp),'--key',r['key'],'--smiles',r['smiles'],'--spin',str(r['spin']),
            '--registration',reg,'--out',str(dest)],lock=str(out/'locks'/(r['id']+'.lock')),timeout_s=3600,env=env))
        records.append(dict(id=r['id'],key=r['key'],smiles=r['smiles'],spin=r['spin'],geometry=str(gp),geometry_sha256=sha(gp),consistency=str(dest)))
    for f in ('scripts/r6_referee.py','scripts/r6_jobs.py','scripts/r3_precision.py','src/zcosmo/pcm_lu.py','src/zcosmo/pyscf_cosmo.py'):
        inputs[str(Path(f).resolve())]=sha(f)
    write(out/'jobs.json',dict(registration=reg,cwd=os.getcwd(),inputs=inputs,jobs=jobs,cases=records))


def plan_modes(a):
    source=json.loads(Path(a.manifest).read_text());check_inputs(source['inputs']);out=fresh(a.out);jobs=[];inputs=dict(source['inputs'])
    for r in source['cases']:
        path=Path(r['consistency'])/'status.json';d=json.loads(path.read_text())
        if d['status']!='diagnostic_complete' or not d['full_response_consistent'] or d['input_sha256']!=r['geometry_sha256']:
            raise ValueError('all five fixed consistency cases must pass before optional Hessians')
        inputs[str(path.resolve())]=sha(path)
        env=source['jobs'][0]['env']
        jobs.append(dict(id=r['id'],argv=[sys.executable,str(Path('scripts/r6_referee.py').resolve()),'modes',
            '--geometry',r['geometry'],'--key',r['key'],'--spin',str(r['spin']),'--consistency',str(path),
            '--registration',source['registration'],'--out',str(out/r['id'])],
            lock=str(out/'locks'/(r['id']+'.lock')),timeout_s=7200,env=env))
    write(out/'jobs.json',dict(registration=source['registration'],cwd=os.getcwd(),inputs=inputs,jobs=jobs))


def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
    q=s.add_parser('run');q.add_argument('--manifest',required=True);q.add_argument('--out',required=True)
    q=s.add_parser('plan_referee');q.add_argument('--artifacts',required=True);q.add_argument('--registration',required=True);q.add_argument('--out',required=True)
    q=s.add_parser('plan_modes');q.add_argument('--manifest',required=True);q.add_argument('--out',required=True)
    a=p.parse_args()
    if a.cmd!='run':globals()[a.cmd](a);return
    m=json.loads(Path(a.manifest).read_text());reg=registration(m['registration']);check_inputs(m.get('inputs',{}))
    rc=execute(m['jobs'],a.out,m.get('cwd',os.getcwd()),reg)
    write(Path(a.out)/'manifest.json',dict(input_sha256=sha(a.manifest),registration=reg))
    raise SystemExit(rc)
if __name__=='__main__':main()
