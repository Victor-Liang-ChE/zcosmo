"""Identity table for the extended (NIST 2020) archive: InChIKey and SMILES straight from the XML InChI.

Falls back to offline name resolution (identity.resolve) for compounds without an InChI.
Writes $ZC_PROC/tml_identity.csv and $ZC_PROC/ud_complist.csv.
"""
import os
from pathlib import Path

import pandas as pd
from rdkit import Chem, RDLogger

from zcosmo.identity import load_ud, resolve

RDLogger.DisableLog("rdApp.*")
ROOT = Path(__file__).resolve().parents[2]
P = Path(os.environ["ZC_PROC"])

c = pd.read_csv(P / "tml_compounds.csv", dtype=str)
ud = load_ud(ROOT / "data/raw/nist/UD/complist.txt")
ud.to_csv(P / "ud_complist.csv", index=False)
rows = []
for (name, formula), g in c.groupby(["name", "formula"], dropna=False):
    inchi = g.inchi.dropna()
    key = g.inchikey.dropna()
    smi = None
    if len(inchi):
        m = Chem.MolFromInchi(inchi.iloc[0])
        smi = Chem.MolToSmiles(m) if m is not None else None
    rows.append(dict(name=name, formula=formula, inchikey=key.iloc[0] if len(key) else None, smiles=smi,
                     source="xml_inchi" if len(key) else None))
t = pd.DataFrame(rows)
miss = t[t.inchikey.isna()]
if len(miss):
    r = resolve(miss[["name", "formula"]], ud)
    t = pd.concat([t[t.inchikey.notna()], r])
t.to_csv(P / "tml_identity.csv", index=False)
print(t.source.fillna("none").str.split(":").str[0].value_counts())
