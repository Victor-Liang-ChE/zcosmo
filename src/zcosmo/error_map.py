"""Error map: IDAC and VLE error by chemical family pair, per model."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from rdkit import Chem

ROOT = Path(__file__).resolve().parents[2]

FAMILIES = [  # first match wins, most specific first
    ("water", "[OX2H2]"),
    ("acid", "C(=O)[OX2H1]"),
    ("amide", "C(=O)[NX3]"),
    ("alcohol", "[CX4,c][OX2H1]"),
    ("amine", "[NX3;!$(N-C=O);!$(N=*);!$(N#*);!$([N+])]"),
    ("nitrile", "C#N"),
    ("nitro", "[N+](=O)[O-]"),
    ("ester", "C(=O)O[#6]"),
    ("ketone/aldehyde", "[CX3]=O"),
    ("ether", "[OX2]([#6])[#6]"),
    ("sulfur", "[#16]"),
    ("halogenated", "[F,Cl,Br]"),
    ("aromatic HC", "c"),
    ("alkene/alkyne", "[C]=,#[C]"),
    ("alkane", "[CX4]"),
]
_PATS = [(n, Chem.MolFromSmarts(s)) for n, s in FAMILIES]


def family(smiles: str) -> str:
    m = Chem.MolFromSmiles(smiles) if isinstance(smiles, str) else None
    if m is None:
        return "other"
    for n, p in _PATS:
        if m.HasSubstructMatch(p):
            return n
    return "other"


def main(models, split="test"):
    comp = pd.read_csv(ROOT / "data/benchmark/compounds.csv")
    fam = {k: family(s) for k, s in zip(comp.inchikey, comp.smiles)}
    rows = []
    frames = {m: pd.read_csv(ROOT / f"results/predictions/{m}__idac__all.csv") for m in models}
    ok = np.ones(len(next(iter(frames.values()))), bool)
    for f in frames.values():
        ok &= f.pred_ln_gamma_inf.notna().to_numpy()
    for m, f in frames.items():
        d = f[ok].copy()
        if split == "test":
            d = d[d.split != "train"]
        d["fam_solute"] = d.solute.map(fam)
        d["fam_solvent"] = d.solvent.map(fam)
        d["ae"] = (d.pred_ln_gamma_inf - d.ln_gamma_inf).abs()
        d["err"] = d.pred_ln_gamma_inf - d.ln_gamma_inf
        g = d.groupby(["fam_solute", "fam_solvent"]).agg(n=("ae", "size"), MAE=("ae", "mean"), bias=("err", "mean"))
        g["model"] = m
        rows.append(g.reset_index())
    out = pd.concat(rows)
    wide = out.pivot_table(index=["fam_solute", "fam_solvent"], columns="model", values="MAE")
    wide["n"] = out.groupby(["fam_solute", "fam_solvent"]).n.first()
    wide = wide.sort_values("n", ascending=False)
    wide.to_csv(ROOT / f"results/error_map_idac_{split}.csv")
    out.to_csv(ROOT / f"results/error_map_idac_{split}_long.csv", index=False)
    print(wide.head(30).round(3).to_string())


if __name__ == "__main__":
    main(sys.argv[1:] or ["unifac_do", "cosmosac2010", "Z0", "Z1"], "all")
