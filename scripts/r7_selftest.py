"""Portable R7 software/math tests. This suite makes no PySCF acceptance claim."""
from __future__ import annotations
import argparse
import json
import sys
import tempfile
import time
from pathlib import Path
import numpy as np
import pandas as pd
from r7_common import PILOT,BERNY,verdict,chain_decision,internal_projection,bounded,gradient,write
from r7_common import fd_assess as assess, FD_STEPS as STEPS, FD_TAU as TAU
from r7_common import historical_queries
from r7_gate import aligned_values,compare_arrays


def run():
    checks={}
    def energy(x):return -100.+1.7e-4*x+.3*x*x+.7*x**3+.2*x**4+.05*x**5
    table=np.array([[energy(h),energy(-h)] for h in STEPS])
    ok=assess(table,table,1.7e-4,1.7e-4,1.7e-4)
    assert ok['full_verdict']=='consistent'
    bad=assess(table,table,1.7e-4+4*TAU,1.7e-4+4*TAU,1.7e-4)
    assert bad['full_verdict']=='inconsistent'
    noisy=table.copy();noisy[:,0]+=STEPS*1e-4;noisy[:,1]-=STEPS*1e-4
    assert assess(noisy,table,1.7e-4,1.7e-4,1.7e-4)['full_verdict']=='inconclusive'
    assert assess(table,table,1.7e-4,1.7e-4,1.7e-4,False)['full_verdict']=='inconclusive'
    assert verdict(0,0,TAU/2)=='inconclusive'
    checks['FD_reference_error']=abs(ok['reference']-1.7e-4)
    checks['FD_indicator']=ok['combined_indicator']
    checks['tri_state_gate']='pass'
    keys=list(PILOT)
    pilot={k:dict(off='censored_evaluations',full='berny_converged') for k in keys}
    assert chain_decision({'passed':True},pilot)['eligible_for_chain_trial']
    mixed={k:dict(v) for k,v in pilot.items()};mixed[keys[2]]=dict(off='berny_converged',full='censored_evaluations')
    assert not chain_decision({'passed':True},mixed)['eligible_for_chain_trial']
    mixed={k:dict(v) for k,v in pilot.items()};mixed[keys[2]]['off']='failed'
    assert not chain_decision({'passed':True},mixed)['eligible_for_chain_trial']
    assert not chain_decision({'passed':False},pilot)['eligible_for_chain_trial']
    try:chain_decision({'passed':True},{keys[0]:pilot[keys[0]]})
    except ValueError:pass
    else:raise AssertionError('Missing pilot was accepted')
    checks['chain_escalation_negative_controls']='pass'
    x=np.array([[0.,0.,0.],[1.,0.,0.],[0.,1.,0.],[.2,.3,1.]])
    v=internal_projection(x,np.random.default_rng(17).normal(size=x.shape))
    trans=np.max(abs(v.sum(0)));torque=np.max(abs(np.cross(x-x.mean(0),v).sum(0)))
    assert max(trans,torque)<1e-12
    checks['rigid_projection_residual']=float(max(trans,torque))
    class MF:
        with_solvent=object()
        def nuc_grad_method(self):
            class G:auxbasis_response=True
            g=G();g.base=self;return g
    assert gradient(MF(),True).grid_response is True
    checks['configured_gradient_interface_mock']='pass, mock only'
    fakekeys=['A'*13+chr(65+i)+'-'+'B'*10+'-C' for i in range(25)]
    q=pd.DataFrame(dict(target=[fakekeys[i%25] for i in range(2302)],
        solute=[fakekeys[i%25] for i in range(2302)],solvent=['Z'*14+'-'+'B'*10+'-C']*2302,
        T=[298.15]*2302,occurrence=np.arange(2302)))
    with tempfile.TemporaryDirectory(prefix='r7-test-') as td:
        root=Path(td);q.to_csv(root/'queries.csv',index=False)
        _,_,found=historical_queries(root)
        assert len(found)==2302 and found.target.nunique()==25
        f=q.copy();f['model']='Z0x';f['value']=np.arange(2302,dtype=float);f.loc[0,'value']=np.nan
        shuffled=f.sample(frac=1,random_state=2)
        a=aligned_values(shuffled,q,'Z0x');b=aligned_values(f,q,'Z0x')
        assert np.array_equal(a,b,equal_nan=True)
        c=compare_arrays(a,b);assert c['coverage_identical'] and c['finite_reference']==2301
        try:aligned_values(f.iloc[1:],q,'Z0x')
        except ValueError:pass
        else:raise AssertionError('Missing query accepted')
        changed=b.copy();changed[0]=0
        assert not compare_arrays(a,changed)['coverage_identical']
        checks['historical_occurrences_and_finite_masks']='pass'
        dest=root/'diagnostic'
        code="from pathlib import Path;import json,sys;p=Path(sys.argv[1]);p.mkdir();(p/'result.json').write_text(json.dumps({'status':'diagnostic_complete','passed':False}));sys.exit(2)"
        r=bounded([sys.executable,'-c',code,str(dest)],dest,5)
        assert r['execution_status']=='completed' and r['native_status']=='diagnostic_complete'
        try:bounded([sys.executable,'-c','pass'],dest,5)
        except FileExistsError:pass
        else:raise AssertionError('Duplicate output claim accepted')
        deadline=root/'deadline'
        r=bounded([sys.executable,'-c','import time;time.sleep(20)'],deadline,.1)
        assert r['execution_status']=='deadline'
        checks['worker_status_lock_and_deadline']='pass'
    checks['berny_constants']=BERNY
    checks['native_PySCF_test']=False
    return checks


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args()
    t=time.monotonic();d=run();write(a.out,dict(passed=True,tests=d,wall_s=time.monotonic()-t))
    print(json.dumps(d,indent=2))
if __name__=='__main__':main()
