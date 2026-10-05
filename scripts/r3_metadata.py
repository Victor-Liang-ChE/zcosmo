"""A-class COOH metadata repair using the existing NIST geometry-based classifier.

No SCF. The raw sigma rows are copied byte-for-byte. No input file is modified.
Register before generating candidate profiles; changing this flag changes COSMO-SAC-dsp.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from r3_common import digest,write_json,read_sigma

def run(a):
    sys.path.insert(0,str(Path('data/raw/nist').resolve()))
    import to_sigma as ts
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True); report=[]
    keys=Path(a.keys).read_text().split()
    if len(keys)!=len(set(keys)) or not keys: raise ValueError('invalid key manifest')
    for k in keys:
        src=Path(a.profile_dir)/f'{k}.sigma'; xyz=Path(a.geometry_dir)/f'{k}.xyz.json'
        g=json.loads(xyz.read_text()); sym=g['sym']; x=np.asarray(g['x'],float)
        if x.shape!=(len(sym),3) or not np.isfinite(x).all(): raise ValueError('invalid geometry')
        p=ts.Dmol3COSMOParser.__new__(ts.Dmol3COSMOParser)
        p.df_atom=pd.DataFrame(dict(atom=sym));p.dist_mat_atom=cdist(x,x)
        p.is_water=sym.count('H')==2 and sym.count('O')==1 and len(sym)==3
        disp=p.get_dispersive_values()
        flag='H2O' if p.is_water else ('COOH' if disp.has_COOH else disp.dispersion_flag)
        _,_,meta=read_sigma(src);old=meta.get('disp. flag')
        meta.update({'disp. flag':flag,'r3_protocol':'COOH metadata correction, not adopted',
                     'r3_registration':a.registration,'r3_parent_sha256':digest(src)})
        lines=src.read_text().splitlines(keepends=True);target=out/src.name
        if target.exists(): raise FileExistsError(target)
        target.write_text('# meta: '+json.dumps(meta,allow_nan=False)+'\n'+''.join(lines[1:]))
        if not np.array_equal(np.loadtxt(src),np.loadtxt(target)): raise AssertionError('sigma rows changed')
        report.append(dict(key=k,old_flag=old,new_flag=flag,has_COOH=bool(disp.has_COOH),
                           geometry_sha256=digest(xyz),source_sha256=digest(src),candidate_sha256=digest(target)))
    write_json(out/'metadata_audit.json',dict(registration=a.registration,
        parser_sha256=digest('data/raw/nist/to_sigma.py'),profiles=report))

def main():
    p=argparse.ArgumentParser()
    for name in ('profile-dir','geometry-dir','keys','out','registration'):p.add_argument('--'+name,required=True)
    run(p.parse_args())
if __name__=='__main__':main()
