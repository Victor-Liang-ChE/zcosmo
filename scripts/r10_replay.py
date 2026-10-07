"""P42: Mac-only, zero-QC replay of recovered UD and archived P25 raw tables.

No optimizer, SCF, activity-coefficient evaluation, histogram fitting, or profile
installation is reachable from this CLI. Outputs stay outside the repository.
"""
from __future__ import annotations
import argparse
from collections import Counter
from decimal import Decimal
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import re
import sys
import time
import numpy as np
import pandas as pd
from packaging.version import Version
from scipy.stats import wasserstein_distance
from r10_sources import (BASE,UPSTREAM,PARSER_BLOB,DATA,PLAN_RECORD,ROOT,sha,blob,
    read,write,record,verify_record,registration,committed_sources,verify_sources,
    private_output,mac,check as check_acquisition)

SCHEMA='R10-replay-v1'
BIN_TOL=1e-8  # A^2, replay of the SAME published table, not an open/UD physics gate
MAX_SEGMENTS=10000
SOURCE_FILES=['scripts/r10_sources.py','scripts/r10_replay.py',
    'data/raw/nist/to_sigma.py','scripts/r4_common.py','scripts/r3_common.py',
    'src/zcosmo/pyscf_cosmo.py','src/zcosmo/cosmosac.py','src/zcosmo/z0x.py']
R5_PLAN='cloud/r5/shape-plan/manifest.json'
R5_STAGES='docs/astra/round5/data/p25_stage_comparison.csv'


def packages() -> dict:
    return {p:str(Version(version(p))) for p in ('numpy','scipy','pandas','rdkit','packaging','matplotlib')}


def parser_module():
    folder=ROOT/'data/raw/nist'
    if blob((folder/'to_sigma.py').read_bytes())!=PARSER_BLOB:
        raise ValueError('The reviewed parser changed; re-register before a new replay')
    sys.path.insert(0,str(folder))
    import to_sigma
    if Path(to_sigma.__file__).resolve()!=folder/'to_sigma.py':
        raise ValueError('Another to_sigma module is already imported')
    return to_sigma


def read_profile(path):
    lines=Path(path).read_text().splitlines()
    if not lines or not lines[0].startswith('# meta: '):
        raise ValueError('Missing sigma metadata')
    meta=json.loads(lines[0][8:])
    values=np.array([[float(v) for v in line.split()] for line in lines
                     if line.strip() and not line.lstrip().startswith('#')])
    axis=np.round(np.linspace(-.025,.025,51),3)
    if values.shape!=(153,2) or not np.isfinite(values).all():
        raise ValueError('Need all 153 finite profile rows')
    if not np.allclose(values[:,0],np.tile(axis,3),rtol=0,atol=1e-12):
        raise ValueError('Unexpected sigma grid or block order')
    p=values[:,1].reshape(3,51)
    if (p<0).any() or p.sum()<=0: raise ValueError('Invalid profile area')
    return axis,p,meta


def historical_ud_path(folder: Path,key: str) -> Path:
    exact=folder/(key+'.sigma')
    if exact.is_file(): return exact
    hits=sorted(folder.glob(key[:14]+'*.sigma'))
    if len(hits)!=1: raise ValueError('Missing or ambiguous historical UD lookup: '+key)
    return hits[0]


def validate_geometry(sym,x):
    sym=list(sym);x=np.asarray(x,dtype=float)
    if not sym or x.shape!=(len(sym),3) or not np.isfinite(x).all():
        raise ValueError('Invalid molecular coordinates')
    if any(s not in ('H','C','O') for s in sym):
        raise ValueError('R10 is restricted to the frozen CHO panel')
    return sym,x


def load_npz(path):
    with np.load(path,allow_pickle=False) as d:
        if not {'sym','x','xyz','q','area','atom'}<=set(d.files):
            raise ValueError('Incomplete P25 segment archive')
        sym,x=validate_geometry(d['sym'].tolist(),d['x'])
        seg={k:np.array(d[k],copy=True) for k in ('xyz','q','area','atom')}
    validate_segments(seg,len(sym))
    return sym,x,seg


def validate_segments(s,natoms):
    area=np.asarray(s['area']);n=len(area);owner=np.asarray(s['atom'])
    if not 0<n<=MAX_SEGMENTS or s['xyz'].shape!=(n,3) or s['q'].shape!=(n,) or owner.shape!=(n,):
        raise ValueError('Invalid surface shape or fixed memory ceiling exceeded')
    if any(not np.isfinite(v).all() for v in s.values()) or (area<=0).any():
        raise ValueError('Nonfinite or nonpositive surface inputs')
    if not np.array_equal(owner,owner.astype(int)) or (owner<0).any() or (owner>=natoms).any():
        raise ValueError('Owner indices must be zero-based integers within this geometry')


def freeze(a) -> int:
    mac();reg=registration(a.registration);ts=parser_module()
    sources=committed_sources(SOURCE_FILES)
    acquired=Path(a.source_root).resolve()
    check_acquisition(argparse.Namespace(source_root=str(acquired)))
    if read(acquired/'acquisition.json')['registration']!=reg:
        raise ValueError('Acquisition belongs to a different registration')
    shape_path=ROOT/R5_PLAN;shape=read(shape_path)
    panel={r['key']:r for r in shape['panel']}
    if len(shape['panel'])!=12 or set(panel)!={r[1] for r in DATA}:
        raise ValueError('The fixed R5 panel changed')
    stages_path=ROOT/R5_STAGES
    if blob(stages_path.read_bytes())!='28f751319c697907454acb098f9f9e01499c2042':
        raise ValueError('Historical P25 output table changed')
    # Only identities and provenance hashes are used to select the archived files.
    stages=pd.read_csv(stages_path,usecols=['key','case','recipe','UD_sha256','source_sha256'])
    stages=stages[(stages.recipe=='hsieh') & stages['case'].str.rstrip('/').str.endswith('/tz_swig')]
    if len(stages)!=12 or set(stages.key)!=set(panel) or stages.key.duplicated().any():
        raise ValueError('Expected exactly the twelve P25 TZVP/SWIG/Hsieh records')
    stage_by={r.key:r for r in stages.itertuples()}
    comp_path=ROOT/'data/processed_ext/ud_complist.csv';comp=pd.read_csv(comp_path)
    from r4_common import selected_profiles
    compounds_path=ROOT/'data/benchmark/compounds.csv'
    population=selected_profiles(a.profile_root,pd.read_csv(compounds_path))
    by_key={k:p for k,_folder,p in population}
    protected=[record(p) for _k,_folder,p in population]
    if len(protected)!=636:raise ValueError('The original 630+6 population changed')
    ud_dir=Path(a.ud_dir).resolve()
    artifact_root=Path(a.open_artifacts).resolve()
    candidates=list(artifact_root.rglob('native.json'));rows=[]
    official=(acquired/'profiles/UD/complist.txt').read_text()
    from rdkit import Chem
    for name,key,source,git_blob in DATA:
        r=panel[key];s=stage_by[key]
        idx=comp[comp.inchikey==source]
        if len(idx)!=1:raise ValueError('Source index identity is missing or ambiguous: '+source)
        idx=idx.iloc[0]
        if Chem.MolToInchiKey(Chem.MolFromSmiles(str(idx.smiles)))!=source:
            raise ValueError('Published SMILES and source key disagree')
        if sum(bool(line.split()) and line.split()[-1]==source for line in official.splitlines())!=1:
            raise ValueError('Published source key is not unique in the downloaded index')
        raw=acquired/'profiles/UD/cosmo'/(source+'.cosmo')
        if blob(raw.read_bytes())!=git_blob:raise ValueError('Raw source changed')
        ud=historical_ud_path(ud_dir,key)
        if sha(ud)!=s.UD_sha256:raise ValueError('Mac UD bytes differ from the P25 comparison: '+key)
        _axis,_ps,meta=read_profile(ud)
        if meta.get('standard_INCHIKEY') not in (key,source):
            raise ValueError('UD metadata identity conflicts with the declared mapping')
        hits=[]
        for p in candidates:
            d=read(p)
            if d.get('key')==key and d.get('method')=='tz_swig':hits.append((p,d))
        if len(hits)!=1:raise ValueError('Require one original P25 TZVP/SWIG artifact per key: '+key)
        npth,native=hits[0];folder=npth.parent
        expected=dict(SCF_converged=True,basis='def2-tzvp',XC='b88,p86',grid_level=3,
                      lebedev_order=29,eps=1e9,surface_discretization='SWIG')
        if any(native.get(k)!=v for k,v in expected.items()):raise ValueError('P25 method/provenance mismatch')
        if native.get('geometry_sha256')!=r['geometry_sha256']:
            raise ValueError('P25 result has a different generating geometry')
        geom=shape_path.parent/r['geometry'];gd=read(geom)
        if sha(geom)!=r['geometry_sha256']:raise ValueError('R5 generating geometry changed')
        seg=folder/(key+'.segments.npz');sym,x,_=load_npz(seg)
        if sym!=gd['sym'] or not np.array_equal(x,np.asarray(gd['x'])):
            raise ValueError('Segments do not belong to the frozen R5 geometry')
        old=folder/'hsieh'/(key+'.sigma')
        if sha(old)!=s.source_sha256:raise ValueError('P25 raw replay reference does not match the archive')
        primary=by_key[key];pg=primary.with_suffix('.xyz.json');gprim=read(pg)
        if gprim['sym']!=sym or not np.array_equal(np.asarray(gprim['x']),x):
            raise ValueError('Saved primary geometry differs from P25; no substitute is authorized')
        protected.append(record(pg))
        rows.append(dict(name=name,key=key,source_key=source,source_git_blob=git_blob,
            stereo_alias=source!=key,open_smiles=r['smiles'],source_smiles=str(idx.smiles),
            published_index_id=int(idx.ud_id),published_name=str(idx['name']),CAS=str(idx.cas),
            raw=record(raw),UD_profile=record(ud),segments=record(seg),native=record(npth),
            archived_open_profile=record(old),primary_profile=record(primary),geometry=record(geom)))
    inputs=[record(shape_path),record(stages_path),record(comp_path),record(compounds_path),
            record(acquired/'acquisition.json'),record(acquired/'profiles/UD/complist.txt'),
            record(acquired/'profiles/UD/Readme.txt')]
    out=private_output(a.out);out.mkdir(parents=True,exist_ok=False)
    manifest=dict(schema=SCHEMA,base=BASE,upstream=UPSTREAM,registration=reg,sources=sources,
        packages=packages(),rows=rows,inputs=inputs,protected_population=protected,
        bin_tolerance_A2=BIN_TOL,SCF_budget=0,model_evaluation_budget=0,
        notes='Freeze paths and hashes only. The P25 source table links the exact historical UD and open bytes.')
    write(out/'manifest.json',manifest)
    (out/'PLAN_SHA256.txt').write_text(sha(out/'manifest.json')+'\n')
    print('Plan ready; commit PLAN_SHA256.txt before compare:',sha(out/'manifest.json'))
    return 0


def verify_manifest(path,plan_commit):
    from r10_sources import git
    if not re.fullmatch('[0-9a-f]{40}',plan_commit):raise ValueError('Full plan-record commit required')
    git('merge-base','--is-ancestor',plan_commit,'HEAD')
    wanted=git('show',plan_commit+':'+PLAN_RECORD).decode().strip()
    if wanted!=sha(path):raise ValueError('Plan digest was not committed before use')
    m=read(path)
    if m['schema']!=SCHEMA or m['base']!=BASE or m['upstream']!=UPSTREAM:
        raise ValueError('Different replay definition')
    if registration(m['registration']['commit'])!=m['registration']:
        raise ValueError('Registration identity changed')
    if packages()!=m['packages']:raise ValueError('Package versions changed after freezing')
    if m.get('SCF_budget')!=0 or m.get('model_evaluation_budget')!=0 or m['bin_tolerance_A2']!=BIN_TOL:
        raise ValueError('Budget or tolerance changed')
    if len(m['rows'])!=12 or {r['key'] for r in m['rows']}!={r[1] for r in DATA}:
        raise ValueError('Panel incomplete or duplicated')
    verify_sources(m['sources'])
    for r in m['inputs']+m['protected_population']:verify_record(r)
    for r in m['rows']:
        for field in ('raw','UD_profile','segments','native','archived_open_profile','primary_profile','geometry'):
            verify_record(r[field])
    return m


def heavy_graph(sym,adj):
    """Saturated CHO connectivity and attached-H counts, no stereochemical claim."""
    n=len(sym)
    if len(adj)!=n:raise ValueError('Bad adjacency')
    for i,neighbors in enumerate(adj):
        if len(set(neighbors))!=len(neighbors) or any(j<0 or j>=n or j==i or i not in adj[j] for j in neighbors):
            raise ValueError('Invalid covalent graph')
        if sym[i]=='H' and (len(neighbors)!=1 or sym[neighbors[0]]=='H'):
            raise ValueError('Unsupported hydrogen connectivity')
    nodes=[i for i,s in enumerate(sym) if s!='H']
    graph={i:set(j for j in adj[i] if sym[j]!='H') for i in nodes}
    labels={i:(sym[i],sum(sym[j]=='H' for j in adj[i]),len(graph[i])) for i in nodes}
    return nodes,graph,labels


def graph_maps(sym_a,adj_a,sym_b,adj_b,limit=256):
    na,ga,la=heavy_graph(sym_a,adj_a);nb,gb,lb=heavy_graph(sym_b,adj_b)
    if Counter(sym_a)!=Counter(sym_b) or len(na)!=len(nb):raise ValueError('Molecular formulas differ')
    options={i:[j for j in nb if la[i]==lb[j]] for i in na}
    order=sorted(na,key=lambda i:(len(options[i]),-len(ga[i]),i));out=[]
    def visit(k,m,used):
        if k==len(order):
            out.append(dict(m))
            if len(out)>limit:raise ValueError('More than 256 symmetry correspondences; no truncation')
            return
        i=order[k]
        for j in options[i]:
            if j in used:continue
            if all((u in ga[i])==(v in gb[j]) for u,v in m.items()):
                m[i]=j;used.add(j);visit(k+1,m,used);used.remove(j);del m[i]
    visit(0,{},set())
    if not out:raise ValueError('Geometry connectivity differs from the declared structure')
    return sorted(out,key=lambda m:tuple(m[i] for i in sorted(m)))


def proper_rmsd(x,y):
    x=np.asarray(x,float);y=np.asarray(y,float)
    x=x-x.mean(0);y=y-y.mean(0)
    u,_,vh=np.linalg.svd(x.T@y);d=np.eye(3);d[-1,-1]=np.sign(np.linalg.det(u@vh))
    return float(np.sqrt(np.mean(np.sum((x@u@d@vh-y)**2,axis=1))))


def dihedral(x,quad):
    a,b,c,d=np.asarray(x)[list(quad)];axis=c-b;norm=np.linalg.norm(axis)
    if norm<1e-12:return None
    axis=axis/norm;u=a-b;v=d-c
    u=u-(u@axis)*axis;v=v-(v@axis)*axis
    if min(np.linalg.norm(u),np.linalg.norm(v))<1e-10:return None
    return float(np.degrees(np.arctan2(np.cross(axis,u)@v,u@v)))


def delta_angle(a,b):
    return None if a is None or b is None else float((b-a+180)%360-180)


def geometry_comparison(osym,ox,usym,ux,oc,uc):
    oa=[r['bonds'] for r in oc['atoms']];ua=[r['bonds'] for r in uc['atoms']]
    maps=graph_maps(osym,oa,usym,ua);nodes,graph,_=heavy_graph(osym,oa)
    paths=set()
    for j in nodes:
        for k in graph[j]:
            for i in graph[j]-{k}:
                for l in graph[k]-{j}:
                    q=(i,j,k,l)
                    if len(set(q))==4:paths.add(min(q,q[::-1]))
    result=[]
    for m in maps:
        torsions=[]
        for q in sorted(paths):
            target=tuple(m[i] for i in q);a=dihedral(ox,q);b=dihedral(ux,target)
            torsions.append(dict(kind='heavy',open_atoms=[i+1 for i in q],UD_atoms=[i+1 for i in target],
                                 open_deg=a,UD_deg=b,delta_deg=delta_angle(a,b)))
        for o in nodes:
            hs=[h for h in oa[o] if osym[h]=='H']
            uhs=[h for h in ua[m[o]] if usym[h]=='H']
            if osym[o]!='O' or len(hs)!=1 or len(uhs)!=1:continue
            for carbon in graph[o]:
                if osym[carbon]!='C':continue
                for end in graph[carbon]-{o}:
                    q=(hs[0],o,carbon,end);target=(uhs[0],m[o],m[carbon],m[end])
                    a=dihedral(ox,q);b=dihedral(ux,target)
                    torsions.append(dict(kind='OH',open_atoms=[i+1 for i in q],UD_atoms=[i+1 for i in target],
                                         open_deg=a,UD_deg=b,delta_deg=delta_angle(a,b)))
        result.append(dict(heavy_mapping_1based=[[i+1,m[i]+1] for i in sorted(m)],
            heavy_RMSD_A=proper_rmsd(ox[sorted(m)],ux[[m[i] for i in sorted(m)]]),dihedrals=torsions))
    return dict(correspondences=result,count=len(result),contacts_open=oc['contacts'],contacts_UD=uc['contacts'],
        contacts_indexing='contacts retain zero-based indices from r4_common; dihedrals/maps above are one-based',
        scope='All connectivity correspondences retained; proper rotations only for RMSD; no geometry is rotated for averaging')


def output_array(output):
    return np.stack([output.psigmaA_nhb,output.psigmaA_OH,output.psigmaA_OT])


def stages(parser,output):
    df=parser.df;area=df['area / A^2'].to_numpy(float)
    q=df['charge / e'].to_numpy(float)
    if not 0<len(area)<=MAX_SEGMENTS or not np.isfinite(area).all() or (area<=0).any() or not np.isfinite(q).all():
        raise ValueError('Invalid or oversized retained raw table')
    raw=q/area
    avg=np.asarray(parser.sigma_averaged,float);p=output_array(output)
    axis=np.round(np.asarray(output.sigmas),3)
    pre=np.stack([parser_module().weightbin_sigmas(v,output.sigmas)
                  for v in (parser.sigma_nhb,parser.sigma_OH,parser.sigma_OT)])
    total=parser_module().weightbin_sigmas(np.c_[avg,area],output.sigmas)
    if not np.isfinite(p).all() or (p<0).any() or p.sum()<=0:raise ValueError('Invalid replay profile')
    conservation=float(np.max(abs(p.sum(0)-total)))
    if conservation>BIN_TOL or abs(p.sum()-area.sum())>BIN_TOL:
        raise ValueError('HB/bin conservation failed')
    owner=df.atom.to_numpy(int)-1
    if (owner<0).any() or (owner>=len(parser.df_atom)).any():
        raise ValueError('Invalid raw-table atom owner')
    atomrows=[]
    for i in range(len(parser.df_atom)):
        use=owner==i
        atomrows.append(dict(atom_1based=i+1,element=str(parser.df_atom.atom.iloc[i]),
            hb_class=str(parser.df_atom.hb_class.iloc[i]),area_A2=float(area[use].sum()),
            raw_q_e=float(q[use].sum()),raw_abs_tail_A2=float(area[use & (abs(raw)>=.01)].sum()),
            averaged_abs_tail_A2=float(area[use & (abs(avg)>=.01)].sum())))
    desc=dict(segments=len(area),area_sum_A2=float(area.sum()),header_area_A2=float(parser.area_A2),
        volume_A3=float(parser.volume_A3),raw_q_sum_e=float(q.sum()),
        raw_sigma_min=float(raw.min()),raw_sigma_max=float(raw.max()),
        printed_sigma_max_difference=(float(np.max(abs(raw-df['charge/area / e/A^2'].to_numpy(float))))
            if 'charge/area / e/A^2' in df else None),
        raw_abs_tail_A2=float(area[abs(raw)>=.01].sum()),
        averaged_segment_abs_tail_A2=float(area[abs(avg)>=.01].sum()),
        final_binned_tail_A2=float(p[:,abs(axis)>=.01].sum()),
        averaged_moment_e=float(area@avg),binned_moment_e=float((p*axis).sum()),
        binwise_HB_conservation_max_A2=conservation,pre_HB_area_A2=pre.sum(1).tolist(),
        post_HB_area_A2=p.sum(1).tolist(),atoms=atomrows,
        post_HB_bins_A2=p.tolist(),pre_HB_bins_A2=pre.tolist())
    return desc,(raw,area,avg,p)


def printed_charge_audit(text,actual_sum):
    fields={}
    for name,pattern in (
        ('original',r'Sum of polarization charges\s*=\s*([-+\d.Ee]+)'),
        ('corrected',r'Sum of polarization charges\(corr\.\)\s*=\s*([-+\d.Ee]+)')):
        m=re.search(pattern,text)
        if m:fields[name]=m.group(1)
    tokens=[]
    for line in text.splitlines():
        parts=line.split()
        if len(parts)==9 and all(re.fullmatch(r'\d+',v) for v in parts[:2]):
            try:[Decimal(v) for v in parts[2:]]
            except Exception:continue
            tokens.append(parts[5])
    if not tokens:raise ValueError('No printed DMol segment charge tokens')
    budget=sum(.5*10.**Decimal(v).as_tuple().exponent for v in tokens)
    candidates={}
    for name,token in fields.items():
        h=float(token);u=.5*10.**Decimal(token).as_tuple().exponent
        candidates[name]=dict(value_e=h,difference_e=float(actual_sum-h),
            rounding_consistent=bool(abs(actual_sum-h)<=budget+u+1e-12))
    return dict(printed_segment_count=len(tokens),charge_column_sum_e=float(actual_sum),
        charge_column_half_last_decimal_sum_e=float(budget),header_candidates=candidates,
        meaning='Rounding-only consistency screen, not a correction recipe or a proof of which charge convention was used')


def cavity_header(text):
    labels=('Dielectric Constant','Basic Grid Size','Number of Segments','Solvent Radius',
            'A - Matrix Cutoff','Radius Increment')
    out={}
    for label in labels:
        m=re.search(r'^\s*'+re.escape(label)+r'\s*=\s*(.*?)\s*$',text,re.M)
        out[label]=m.group(1) if m else None
    m=re.search(r'total number of segments\s*:\s*(\d+)',text,re.I)
    out['actual_segment_record_count']=int(m.group(1)) if m else None
    m=re.search(r'Molecular car file\s*:\s*([^\r\n]+)',text)
    out['embedded_car_name']=m.group(1).strip() if m else None
    block=text.split('COSMO-RS Atomic data',1)
    radii=[]
    if len(block)==2:
        for line in block[1].split('Segment information:',1)[0].splitlines():
            m=re.fullmatch(r'\s*(\d+)\s+([A-Za-z]+\d*)\s+([-+\d.Ee]+)\s+([-+\d.Ee]+)\s+([-+\d.Ee]+)\s+([-+\d.Ee]+)\s*',line)
            if m:radii.append(dict(atom_1based=int(m.group(1)),label=m.group(2),radius_A=float(m.group(3))))
    out['atomic_radii']=radii
    out['electronic_input_deck_verified']=False
    out['electronic_protocol_source']='Bell et al. 2020 and VT tutorial; nominal VWN-BP/DNP, not per-file input proof'
    return out


def run_member(r,ts):
    from r4_common import parser_trace,contacts
    from zcosmo.pyscf_cosmo import BOHR,RADII
    if ts.BOHR_TO_ANGSTROM!=BOHR:raise ValueError('Different Bohr conversions in the two raw-table adapters')
    from rdkit import Chem
    raw=Path(r['raw']['path']);up=ts.Dmol3COSMOParser(str(raw),num_profiles=3,averaging='Hsieh')
    uo=up.get_outputs();usym=list(up.df_atom.atom)
    ux=up.df_atom[['x / A','y / A','z / A']].to_numpy(float)
    validate_geometry(usym,ux)
    osym,ox,seg=load_npz(r['segments']['path'])
    op,oo,_=parser_trace(osym,ox,seg)
    ud_axis,ud_p,ud_meta=read_profile(r['UD_profile']['path'])
    _axis,old_p,old_meta=read_profile(r['archived_open_profile']['path'])
    _axis,primary_p,_=read_profile(r['primary_profile']['path'])
    ud_diff=float(np.max(abs(output_array(uo)-ud_p)))
    open_diff=float(np.max(abs(output_array(oo)-old_p)))
    meta_checks={k:bool(np.isclose(float(uo.meta[k]),float(ud_meta[k]),rtol=0,atol=1e-8))
                 for k in ('area [A^2]','volume [A^3]','r_av [A]','f_decay','sigma_hb [e/A^2]')}
    meta_checks['averaging']=uo.meta.get('averaging')==ud_meta.get('averaging')=='Hsieh'
    meta_checks['disp_flag']=uo.meta['disp. flag']==ud_meta.get('disp. flag')
    meta_checks['dispersion_value']=bool(np.isclose(float(uo.meta['disp. e/kB [K]']),
        float(ud_meta['disp. e/kB [K]']),rtol=0,atol=1e-8))
    if ud_diff>=BIN_TOL or open_diff>=BIN_TOL or not all(meta_checks.values()):
        raise ValueError(json.dumps(dict(lineage_replay_failed=True,UD_max=ud_diff,
                                        open_max=open_diff,metadata=meta_checks)))
    uc=contacts(usym,ux);oc=contacts(osym,ox)
    # Independently declared structural identities must fit both observed graphs.
    for smiles,sym,c in ((r['source_smiles'],usym,uc),(r['open_smiles'],osym,oc)):
        mol=Chem.AddHs(Chem.MolFromSmiles(smiles))
        es=[a.GetSymbol() for a in mol.GetAtoms()]
        ea=[[a.GetIdx() for a in atom.GetNeighbors()] for atom in mol.GetAtoms()]
        graph_maps(es,ea,sym,[a['bonds'] for a in c['atoms']])
    ud,uv=stages(up,uo);od,ov=stages(op,oo)
    geom=geometry_comparison(osym,ox,usym,ux,oc,uc)
    text=raw.read_text();headers=cavity_header(text)
    if headers['actual_segment_record_count']!=len(up.df):raise ValueError('Printed segment count differs from parsed table')
    if len(headers['atomic_radii'])!=len(usym):raise ValueError('Atomic-radius block missing or incomplete')
    qa=printed_charge_audit(text,ud['raw_q_sum_e'])
    if qa['printed_segment_count']!=len(up.df):raise ValueError('Charge-token count differs from parser')
    un=uv[3]/uv[3].sum();on=ov[3]/ov[3].sum()
    comparison=dict(normalized_153_L1=float(abs(un-on).sum()),
        normalized_total_L1=float(abs(un.sum(0)-on.sum(0)).sum()),
        raw_area_weighted_W1_e_A2=float(wasserstein_distance(uv[0],ov[0],uv[1],ov[1])),
        averaged_area_weighted_W1_e_A2=float(wasserstein_distance(uv[2],ov[2],uv[1],ov[1])),
        delta_final_tail_UD_minus_open_A2=ud['final_binned_tail_A2']-od['final_binned_tail_A2'],
        note='Distributions on different surfaces; no pointwise tessera correspondence or method/conformer causal separation',
        open_surface_scope='The archived retained P25 table, without reconstructing discarded tesserae')
    return dict(key=r['key'],source_key=r['source_key'],stereo_alias=r['stereo_alias'],
        status='replay_passed',lineage_checks=dict(UD_max_raw_bin_A2=ud_diff,
        open_max_raw_bin_A2=open_diff,metadata=meta_checks,
        primary_vs_P25_max_raw_bin_A2=float(abs(primary_p-old_p).max())),
        cavity_input_fields=headers,open_atomic_radii_A={s:RADII[s] for s in set(osym)},
        BOHR_TO_ANGSTROM=float(ts.BOHR_TO_ANGSTROM),printed_charge_audit=qa,
        geometry=geom,UD=ud,open=od,comparison=comparison,
        stereo_scope='PG source is stereospecific; its benchmark alias is unspecified. Graph matching alone does not certify stereochemistry.',
        mechanism_resolved=False,adopted=False)


def compare(a) -> int:
    mac();m=verify_manifest(a.manifest,a.plan_commit);ts=parser_module()
    os.environ['ZC_R3_COOH_FLAG']='1'  # accepted metadata convention, no COOH in this fixed panel
    out=private_output(a.out);out.mkdir(parents=True,exist_ok=False)
    start=time.perf_counter();results=[]
    for r in m['rows']:
        try:d=run_member(r,ts)
        except Exception as exc:
            d=dict(key=r['key'],source_key=r['source_key'],status='blocked',
                   error=type(exc).__name__+': '+str(exc),adopted=False)
        results.append(d);write(out/(r['key']+'.json'),d)
        write(out/'summary.json',dict(complete=False,requested=12,processed=len(results),rows=results,
            SCF_calls=0,model_calls=0,adopted=False,mechanism_resolved=False))
    verify_manifest(a.manifest,a.plan_commit)
    if any(name=='pyscf' or name.startswith('pyscf.') for name in sys.modules):
        raise RuntimeError('Unexpected native PySCF import during a zero-QC replay')
    passed=all(r['status']=='replay_passed' for r in results)
    write(out/'summary.json',dict(schema=SCHEMA,complete=True,all_lineage_gates_passed=passed,
        requested=12,processed=12,rows=results,base=BASE,registration=m['registration'],
        manifest_sha256=sha(a.manifest),plan_commit=a.plan_commit,packages=m['packages'],
        wall_s=time.perf_counter()-start,SCF_calls=0,model_calls=0,adopted=False,
        mechanism_resolved=False,native_calculations_authorized=False,
        summary_scope='Same-parser input comparison. A successful replay links stored bytes; it is not a liquid-state or method-accuracy validation.'))
    return 0 if passed else 2


def check(a) -> int:
    d=read(a.summary)
    if d.get('schema')!=SCHEMA or d.get('complete') is not True or d.get('all_lineage_gates_passed') is not True:
        raise ValueError('Lineage/replay incomplete or failed; do not interpret a partial panel as complete')
    if len(d['rows'])!=12 or {r['key'] for r in d['rows']}!={r[1] for r in DATA}:
        raise ValueError('Missing, extra, or duplicate member')
    if any(r.get('status')!='replay_passed' for r in d['rows']):raise ValueError('Blocked member')
    if d.get('SCF_calls')!=0 or d.get('model_calls')!=0 or d.get('adopted') is not False:
        raise ValueError('This is not the registered zero-QC, non-adopting replay')
    print('All 12 lineage/replay gates passed; mechanism and production adoption remain unresolved')
    return 0


def main() -> int:
    if Path.cwd().resolve()!=ROOT:raise ValueError('Run this command from the repository root')
    p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='cmd',required=True)
    q=s.add_parser('freeze');q.add_argument('--source-root',required=True);q.add_argument('--open-artifacts',required=True)
    q.add_argument('--profile-root',default='data/pyscf_sigma');q.add_argument('--ud-dir',default='data/raw/nist/UD/sigma3')
    q.add_argument('--registration',required=True);q.add_argument('--out',required=True);q.set_defaults(fn=freeze)
    q=s.add_parser('compare');q.add_argument('--manifest',required=True);q.add_argument('--plan-commit',required=True)
    q.add_argument('--out',required=True);q.set_defaults(fn=compare)
    q=s.add_parser('check');q.add_argument('--summary',required=True);q.set_defaults(fn=check)
    a=p.parse_args();return a.fn(a)

if __name__=='__main__':raise SystemExit(main())
