"""Molecular London dispersion descriptors from first principles (D4 model).

For each compound with a sigma profile: RDKit 3D geometry (ETKDG + MMFF), then
the D4 model gives atom-pairwise C6 coefficients and static atomic
polarizabilities (both derived from TD-DFT reference polarizabilities via the
Casimir-Polder integral, not from any mixture data). We store
  C6_mol  = sum_ab C6_ab            (Hartree bohr^6)
  alpha   = sum_a alpha_a           (bohr^3)
Writes results/qc/dispersion.csv
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem

ROOT = Path(__file__).resolve().parents[2]
BOHR = 0.52917721067


def descriptors(smiles):
    from dftd4.interface import DispersionModel
    m = Chem.AddHs(Chem.MolFromSmiles(smiles))
    if AllChem.EmbedMolecule(m, randomSeed=7) != 0:
        AllChem.EmbedMolecule(m, randomSeed=7, useRandomCoords=True)
    try:
        AllChem.MMFFOptimizeMolecule(m)
    except Exception:
        pass
    x = m.GetConformer().GetPositions() / BOHR
    z = np.array([a.GetAtomicNum() for a in m.GetAtoms()])
    p = DispersionModel(z, x).get_properties()
    c6 = np.asarray(p["c6 coefficients"])
    al = np.asarray(p["polarizabilities"])
    return float(c6.sum()), float(al.sum())


def main():
    comp = pd.read_csv(Path(__import__("os").environ.get("ZC_BENCH", ROOT / "data/benchmark")) / "compounds.csv")
    comp = comp[comp.has_sigma_ud]
    rows = []
    for r in comp.itertuples():
        try:
            c6, al = descriptors(r.smiles)
        except Exception as e:
            c6, al = np.nan, np.nan
        rows.append(dict(inchikey=r.inchikey, name=r.name, C6_au=c6, alpha_au=al))
    out = ROOT / "results/qc"
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out / "dispersion.csv", index=False)
    print(len(rows), "compounds")


if __name__ == "__main__":
    main()
