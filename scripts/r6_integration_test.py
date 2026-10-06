"""Synthetic four-arm process/coverage regression. No quantum chemistry or experimental data."""
import json, tempfile, shutil, subprocess, os, sys, hashlib
from pathlib import Path
import numpy as np,pandas as pd
source=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as temp:
 root=Path(temp)
 for rel in ('scripts/r6_common.py','scripts/r6_endpoint.py','scripts/r3_common.py','src/zcosmo/z0x.py','src/zcosmo/cosmosac.py'):
  p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source/rel,p)
 (root/'src/zcosmo/models.py').write_text("from pathlib import Path\nfrom zcosmo.cosmosac import Params\nROOT=Path(__file__).resolve().parents[2]\ndef load_z_params(n):return Params(A_ES=12000.,B_ES=0.,disp_mode='london')\n")
 (root/'src/zcosmo/zmodel.py').write_text('def c_es_theory(fpol=1.):return 12226.235339788673*fpol\n')
 keys=['fake-a','fake-b','BTFJIXJJCSYFAL-UHFFFAOYSA-N','missing-dielectric']
 for folder in ('data/raw/nist/UD/sigma3','open630','open636','water_stress'):
  p=root/folder;p.mkdir(parents=True)
  for j,key in enumerate(keys):
   if folder=='open630' and j==2:continue
   g=np.linspace(-.025,.025,51);ps=np.zeros((3,51));ps[0]=np.exp(-((g-.001*j)/.004)**2)
   ps[1]=.1*np.exp(-((abs(g)-.010)/.002)**2);ps[:,abs(g)>.019]=0;ps*=100/ps.sum()
   with (p/(key+'.sigma')).open('w') as f:
    f.write('# meta: '+json.dumps({'volume [A^3]':80.+j*5,'disp. flag':'NHB','disp. e/kB [K]':50.})+'\n')
    np.savetxt(f,np.column_stack([np.tile(g,3),ps.ravel()]))
 (root/'results/qc').mkdir(parents=True)
 pd.DataFrame(dict(inchikey=keys[:3],eps=[5.,30.,8.])).to_csv(root/'results/qc/dielectric.csv',index=False)
 pd.DataFrame(dict(inchikey=keys,C6_au=[200.,250.,180.,190.],alpha_au=[20.,25.,17.,18.])).to_csv(root/'results/qc/dispersion.csv',index=False)
 rows=pd.DataFrame([['r0',keys[0],keys[1],298.15,'train'],['r1',keys[1],keys[0],298.15,'test_one'],['r2',keys[2],keys[1],298.15,'test_both'],['r3',keys[3],keys[1],298.15,'test_one']],columns=['r5_row_id','solute','solvent','T','split'])
 experiment=root/'experiment';experiment.mkdir();rows.to_csv(experiment/'queries.csv',index=False)
 digest=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
 inputs={str(p):digest(p) for p in root.rglob('*.sigma')};inputs[str(experiment/'queries.csv')]=digest(experiment/'queries.csv')
 cfg={'registration':'synthetic-acceptance-test','rows':str(experiment/'queries.csv'),'variants':{'UD':None,**{name:str(root/name) for name in ('open630','open636','water_stress')}},'inputs':inputs}
 config=experiment/'config.json';config.write_text(json.dumps(cfg))
 env=dict(os.environ,PYTHONPATH='src:scripts',OPENBLAS_NUM_THREADS='1')
 def run(*argv):return subprocess.run([sys.executable,'scripts/r6_endpoint.py',*argv],cwd=root,env=env,capture_output=True,text=True)
 p=run('run','--config',str(config),'--out',str(root/'audit'))
 if p.returncode:raise RuntimeError(p.stdout+p.stderr)
 gate=json.loads((root/'audit/gate.json').read_text());assert gate['numerical_gate']
 for arm in cfg['variants']:
  records=pd.read_csv(root/'audit'/f'{arm}.csv')
  assert records.status.eq('baseline_nonfinite').sum()==1,arm
 good=pd.read_csv(root/'audit/UD.csv');good.iloc[:-1].to_csv(root/'audit/UD.csv',index=False)
 q=run('summarize','--config',str(config),'--out',str(root/'audit'));assert q.returncode!=0 and 'observation identity' in q.stderr
 good.to_csv(root/'audit/UD.csv',index=False)
 q=run('summarize','--config',str(config),'--out',str(root/'audit'));assert q.returncode==0,q.stderr
 print(json.dumps({'four_arm_gate_passed':True,'missing_row_rejected':True,'rows_per_arm':4,'open630_excluded':1,'matched_nonfinite_retained_per_arm':1}))
