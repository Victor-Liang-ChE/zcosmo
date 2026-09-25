"""Conformer ensembles for flexible molecules and ensemble-averaged sigma profiles.

1. select the 50 most flexible benchmark molecules with UD profiles (rotatable bonds, then IDAC+VLE rows);
2. RDKit ETKDG x50 + GFN2-xTB relaxation, dedupe (heavy-atom RMSD < 0.5 A or dE < 0.1 kcal/mol),
   keep <= 5 within 3 kcal/mol;
3. pyscf_cosmo profile per conformer (separate step, python -m zcosmo.pyscf_cosmo with the xyz csv);
4. build lowest-energy and Boltzmann-ensemble profiles from the conductor energies.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolDescriptors
from rdkit.Chem import rdMolAlign

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/pyscf_sigma"
HARTREE_KCAL = 627.509474
R_KCAL = 1.987204e-3


def select(n=50):
    comp = pd.read_csv(ROOT / "data/benchmark/compounds.csv")
    comp = comp[comp.has_sigma_ud & comp.in_scope_chem]
    rows = []
    for t, a, b in [("idac", "solute", "solvent"), ("vle", "c1", "c2")]:
        d = pd.read_csv(ROOT / f"data/benchmark/{t}.csv")
        rows.append(pd.concat([d[a], d[b]]))
    cnt = pd.concat(rows).value_counts()
    comp["n_rows"] = comp.inchikey.map(cnt).fillna(0)
    comp["rotb"] = [rdMolDescriptors.CalcNumRotatableBonds(Chem.MolFromSmiles(s)) for s in comp.smiles]
    comp = comp[(comp.rotb >= 3) & (comp.n_rows > 0)]
    return comp.sort_values(["rotb", "n_rows"], ascending=False).head(n)


def conformers(smiles, n_embed=50, keep=5, window=3.0):
    from ase import Atoms
    from ase.optimize import BFGS
    from tblite.ase import TBLite
    m = Chem.AddHs(Chem.MolFromSmiles(smiles))
    cids = AllChem.EmbedMultipleConfs(m, numConfs=n_embed, randomSeed=7)
    AllChem.MMFFOptimizeMoleculeConfs(m)
    sym = [a.GetSymbol() for a in m.GetAtoms()]
    res = []
    for cid in cids:
        at = Atoms(sym, positions=m.GetConformer(cid).GetPositions())
        at.calc = TBLite(method="GFN2-xTB", verbosity=0)
        BFGS(at, logfile=None).run(fmax=0.01, steps=400)
        e = at.get_potential_energy() / 27.211386245988 * HARTREE_KCAL
        m.GetConformer(cid).SetPositions(at.get_positions()) if hasattr(m.GetConformer(cid), "SetPositions") else None
        conf = m.GetConformer(cid)
        for i, p in enumerate(at.get_positions()):
            conf.SetAtomPosition(i, p.tolist())
        res.append((e, cid, at.get_positions()))
    res.sort(key=lambda r: r[0])
    heavy = [a.GetIdx() for a in m.GetAtoms() if a.GetSymbol() != "H"]
    kept = []
    for e, cid, x in res:
        if e - res[0][0] > window:
            break
        dup = False
        for e2, cid2, _ in kept:
            if abs(e - e2) < 0.1:
                dup = True
                break
            rms = rdMolAlign.GetBestRMS(Chem.RemoveHs(m), Chem.RemoveHs(m), cid2, cid) if False else \
                AllChem.GetConformerRMS(m, cid2, cid, atomIds=heavy)
            if rms < 0.5:
                dup = True
                break
        if not dup:
            kept.append((e, cid, x))
        if len(kept) >= keep:
            break
    return sym, [(e - kept[0][0], x) for e, _, x in kept]


def build_conformer_csv(n=50):
    sel = select(n)
    rows = []
    for r in sel.itertuples():
        try:
            sym, confs = conformers(r.smiles)
        except Exception as ex:
            print("fail", r.name, ex)
            continue
        for k, (de, x) in enumerate(confs):
            rows.append(dict(inchikey=r.inchikey, smiles=r.smiles, conf_id=k, dE_xtb_kcal=de,
                             xyz=json.dumps({"sym": sym, "x": np.round(x, 5).tolist()})))
        print(r.name, r.rotb, len(confs), flush=True)
    pd.DataFrame(rows).to_csv(OUT / "conformers.csv", index=False)


def read_sigma(p):
    lines = Path(p).read_text().splitlines()
    meta = json.loads(lines[0][len("# meta: "):])
    v = np.array([[float(t) for t in ln.split()] for ln in lines if ln and not ln.startswith("#")])
    return meta, v


def combine(T=298.15):
    """Write lowest-conformer and Boltzmann-ensemble profiles into two directories."""
    confs = pd.read_csv(OUT / "conformers.csv")
    d_low = OUT / "conf_lowest"
    d_ens = OUT / "conf_ensemble"
    d_low.mkdir(exist_ok=True)
    d_ens.mkdir(exist_ok=True)
    from zcosmo.pyscf_cosmo import write_sigma  # noqa: F401  (format reference)
    summary = []
    for key, g in confs.groupby("inchikey"):
        items = []
        for c in g.conf_id:
            p = OUT / "conf_profiles" / f"{key}__{c}.sigma"
            if p.exists():
                items.append(read_sigma(p))
        if not items:
            continue
        E = np.array([m["E_scf_Eh"] for m, _ in items]) * HARTREE_KCAL
        w = np.exp(-(E - E.min()) / (R_KCAL * T))
        w /= w.sum()
        low = int(np.argmin(E))
        for dest, wts in [(d_low, np.eye(len(items))[low]), (d_ens, w)]:
            meta = dict(items[low][0])
            prof = sum(wi * v[:, 1] for wi, (_, v) in zip(wts, items))
            meta["area [A^2]"] = float(sum(wi * m["area [A^2]"] for wi, (m, _) in zip(wts, items)))
            meta["volume [A^3]"] = float(sum(wi * m["volume [A^3]"] for wi, (m, _) in zip(wts, items)))
            meta["n_conformers"] = len(items)
            with open(dest / f"{key}.sigma", "w") as f:
                f.write("# meta: " + json.dumps(meta) + "\n# Rows: sigma psigmaA; NHB, OH, OT\n# ensemble\n")
                for s, pa in zip(items[low][1][:, 0], prof):
                    f.write(f"{s:0.3f} {pa:0.14e}\n")
        summary.append(dict(inchikey=key, n=len(items), w_lowest=float(w[low]), w_max=float(w.max())))
    pd.DataFrame(summary).to_csv(OUT / "conformer_summary.csv", index=False)
    print(pd.DataFrame(summary).describe())


if __name__ == "__main__":
    {"build": build_conformer_csv, "combine": combine}[sys.argv[1]]()
