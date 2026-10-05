"""Round-4 diagnostic helpers. No production defaults are changed."""
from __future__ import annotations
import importlib
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from r3_common import digest, read_sigma, write_json, STALL_KEYS

BASE = '33ebac0146ae2df4dd73fcf8a431cb6d7033554b'
S1_KEY = 'MVLVMROFTAUDAG-UHFFFAOYSA-N'


def parser_module():
    sys.path.insert(0, str(Path('data/raw/nist').resolve()))
    return importlib.import_module('to_sigma')


def geometry(path):
    """Read actual saved coordinates. Never substitute a new conformer for missing bytes."""
    path = Path(path)
    if path.suffix == '.cosmo':
        d = parser_module().get_atom_DataFrame(path.read_text())
        sym = list(d['atom'])
        x = d[['x / A', 'y / A', 'z / A']].to_numpy(float)
    else:
        d = json.loads(path.read_text()); sym = list(d['sym']); x = np.asarray(d['x'], float)
    if x.shape != (len(sym), 3) or not len(sym) or not np.isfinite(x).all():
        raise ValueError(f'invalid geometry: {path}')
    return sym, x


def geometry_parser(sym, x):
    ts = parser_module()
    p = ts.Dmol3COSMOParser.__new__(ts.Dmol3COSMOParser)
    p.df_atom = pd.DataFrame({'atom': sym})
    p.dist_mat_atom = cdist(x, x)
    p.is_water = sym.count('H') == 2 and sym.count('O') == 1 and len(sym) == 3
    p.disp = p.get_dispersive_values()
    return p


def flag_for_geometry(sym, x):
    p = geometry_parser(sym, x)
    return 'H2O' if p.is_water else ('COOH' if p.disp.has_COOH else p.disp.dispersion_flag)


def structure(smiles):
    from rdkit import Chem
    from rdkit.Chem import rdMolDescriptors
    m = Chem.MolFromSmiles(smiles)
    if m is None: raise ValueError(f'invalid SMILES {smiles}')
    oh = len(m.GetSubstructMatches(Chem.MolFromSmarts('[OX2H1]')))
    ether = len(m.GetSubstructMatches(Chem.MolFromSmarts('[#6;!$(C=O)][OX2][#6;!$(C=O)]')))
    acid = m.HasSubstructMatch(Chem.MolFromSmarts('[CX3](=O)[OX2H1]'))
    # Structural strata, not labels chosen after looking at errors.
    if oh >= 2 and ether: group = 'polyol_with_ether'
    elif oh >= 2: group = 'polyol_without_ether'
    elif oh == 1 and ether: group = 'hydroxyether'
    elif not oh and ether >= 2: group = 'polyether_no_OH'
    elif not oh and ether: group = 'monoether_no_OH'
    elif oh == 1: group = 'single_OH'
    else: group = 'other'
    return dict(group=group, OH_count=oh, ether_count=ether, has_COOH=bool(acid),
                rotatable_bonds=int(rdMolDescriptors.CalcNumRotatableBonds(m)),
                rings=int(rdMolDescriptors.CalcNumRings(m)), heavy_atoms=m.GetNumHeavyAtoms())


def contacts(sym, x):
    """Geometric contacts only; these are not an H-bond energy or a basin assignment."""
    p = geometry_parser(sym, x)
    classes = p.get_HB_classes_per_atom()
    bonds = [p.get_bonds(i) for i in range(len(sym))]
    rows = []
    for donor, element in enumerate(sym):
        if element not in ('O', 'N'): continue
        for h, hsym in bonds[donor]:
            if hsym != 'H': continue
            for acc, asym in enumerate(sym):
                if asym not in ('O', 'N') or acc == donor: continue
                if acc in [j for j, _ in bonds[h]]: continue
                a, b = x[donor] - x[h], x[acc] - x[h]
                denom = np.linalg.norm(a) * np.linalg.norm(b)
                if denom == 0: raise ValueError('coincident atoms')
                angle = np.degrees(np.arccos(np.clip(a @ b / denom, -1., 1.)))
                da, ha = np.linalg.norm(x[donor]-x[acc]), np.linalg.norm(b)
                rows.append(dict(donor=donor, H=h, acceptor=acc, acceptor_class=classes[acc],
                    DA_A=float(da), HA_A=float(ha), DHA_deg=float(angle),
                    contact=bool(da <= 3.2 and ha <= 2.5 and angle >= 120.)))
    return dict(atoms=[dict(i=i,element=sym[i],hb_class=classes[i],
                            bonds=[j for j,_ in bonds[i]]) for i in range(len(sym))],
                contacts=rows)


def parser_trace(sym, x, seg):
    """Reconstruct the exact registered parser inputs, retaining intermediate arrays."""
    from zcosmo.pyscf_cosmo import BOHR, cavity_volume
    p = geometry_parser(sym, x)
    n = len(seg['q'])
    p.df = pd.DataFrame({'n': np.arange(1,n+1), 'atom': seg['atom']+1,
        'x / a.u.':seg['xyz'][:,0], 'y / a.u.':seg['xyz'][:,1], 'z / a.u.':seg['xyz'][:,2],
        'charge / e':seg['q'], 'area / A^2':seg['area']})
    for j, f in enumerate('xyz'):
        p.df[f+' / A'] = seg['xyz'][:,j]*BOHR
        p.df_atom[f+' / A'] = x[:,j]
    p.area_A2 = float(seg['area'].sum()); p.volume_A3 = cavity_volume(seg,x/BOHR)
    p.num_profiles=3; p.averaging='Hsieh'
    p.df['rn / A'] = np.sqrt(seg['area']/np.pi)
    p.df['rn^2 / A^2'] = p.df['rn / A']**2
    p.sigma=seg['q']/seg['area']; p.rn2=p.df['rn^2 / A^2'].to_numpy()
    p.dist_mat_squared=cdist(seg['xyz']*BOHR,seg['xyz']*BOHR)**2
    p.df_atom['hb_class']=p.get_HB_classes_per_atom(); p.df_atom['Nbonds']=p.disp.Nbonds
    p.sigma_averaged=p.average_sigmas(p.sigma)
    p.sigma_nhb,p.sigma_OH,p.sigma_OT=p.split_profiles(p.sigma_averaged,3)
    out=p.get_outputs()
    atom=[]
    for i, element in enumerate(sym):
        use=seg['atom']==i; area=seg['area'][use]; raw=p.sigma[use]; av=p.sigma_averaged[use]
        atom.append(dict(i=i,element=element,hb_class=str(p.df_atom.hb_class.iloc[i]),
            area_A2=float(area.sum()),raw_q_e=float(seg['q'][use].sum()),
            averaged_moment_e=float((area*av).sum()),
            positive_tail_A2=float(area[av>=.01].sum()),negative_tail_A2=float(area[av<=-.01].sum())))
    bins=np.stack([out.psigmaA_nhb,out.psigmaA_OH,out.psigmaA_OT])
    return p, out, dict(raw_kept_q_e=float(seg['q'].sum()),
        averaged_moment_e=float((seg['area']*p.sigma_averaged).sum()),
        binned_moment_e=float((bins*out.sigmas).sum()),atom=atom,
        pre_HB_area_A2={k:float(v[:,1].sum()) for k,v in
                       [('NHB',p.sigma_nhb),('OH',p.sigma_OH),('OT',p.sigma_OT)]},
        post_HB_area_A2=dict(zip(('NHB','OH','OT'),map(float,bins.sum(1)))))


def selected_profiles(root, compounds):
    """Select exactly the registered 630+5+1 collection, not all files in a directory."""
    root=Path(root).resolve(); rows=[]
    keys=list(compounds.inchikey)
    if len(keys)!=636 or len(set(keys))!=636: raise ValueError('expected frozen 636 benchmark compounds')
    for key in keys:
        folder='s1_stalled' if key==S1_KEY else ('s2_stalled' if key in STALL_KEYS else 'profiles_v2')
        src=root/folder/f'{key}.sigma'
        if not src.is_file(): raise FileNotFoundError(src)
        _,_,meta=read_sigma(src)
        if meta.get('standard_INCHIKEY', key) != key: raise ValueError(f'profile key mismatch: {src}')
        if folder!='profiles_v2' and meta.get('geometry_converged')!=('S1' if folder=='s1_stalled' else 'S2'):
            raise ValueError(f'flagged status mismatch: {src}')
        rows.append((key,folder,src))
    return rows
