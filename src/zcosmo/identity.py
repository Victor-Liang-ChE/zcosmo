"""Resolve ThermoML compound names to InChIKeys offline.

Sources, in order: the NIST COSMO-SAC UD compound list (name/CAS/InChIKey),
then the `chemicals` package database. A hit is accepted only when its molecular
formula matches the formula written in the ThermoML file.
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
from rdkit import Chem
from rdkit.Chem.rdMolDescriptors import CalcMolFormula
from rdkit import RDLogger

RDLogger.DisableLog("rdApp.*")


def norm_formula(f: str | None) -> str | None:
    if not f or not isinstance(f, str):
        return None
    toks = re.findall(r"([A-Z][a-z]?)(\d*)", f.replace(" ", ""))
    counts: dict[str, int] = {}
    for el, n in toks:
        counts[el] = counts.get(el, 0) + (int(n) if n else 1)
    # Hill order
    keys = sorted(counts)
    if "C" in counts:
        keys = ["C"] + (["H"] if "H" in counts else []) + sorted(k for k in counts if k not in ("C", "H"))
    return "".join(f"{k}{counts[k] if counts[k] != 1 else ''}" for k in keys)


def norm_name(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower()) if isinstance(s, str) else ""


def load_ud(complist: Path) -> pd.DataFrame:
    rows = []
    for line in Path(complist).read_text(errors="ignore").splitlines()[1:]:
        parts = line.split()
        if len(parts) < 7:
            continue
        idx, formula, cas = parts[0], parts[1], parts[2]
        inchikey, inchi, smiles = parts[-1], parts[-2], parts[-3]
        name = " ".join(parts[3:-3])
        rows.append(dict(ud_id=idx, formula=formula, cas=cas, name=name, smiles=smiles,
                         inchi=inchi, inchikey=inchikey))
    return pd.DataFrame(rows)


def resolve(names_formulas: pd.DataFrame, ud: pd.DataFrame) -> pd.DataFrame:
    from chemicals.identifiers import search_chemical

    ud_by_name = {norm_name(n): r for n, r in zip(ud.name, ud.itertuples())}
    out = []
    for name, formula in names_formulas[["name", "formula"]].itertuples(index=False):
        f = norm_formula(formula)
        hit = None
        src = None
        r = ud_by_name.get(norm_name(name))
        if r is not None and norm_formula(r.formula) == f:
            hit = (r.inchikey, r.smiles)
            src = "UD"
        if hit is None:
            try:
                c = search_chemical(name)
                smi = c.smiles
                fm = None
                if smi:
                    m = Chem.MolFromSmiles(smi)
                    fm = CalcMolFormula(m) if m is not None else None
                if norm_formula(fm or c.formula) == f and c.InChI_key:
                    hit = (c.InChI_key, smi)
                    src = "chemicals"
                elif c.InChI_key:
                    src = f"formula_mismatch:{c.formula}"
            except Exception:
                src = "not_found"
        out.append(dict(name=name, formula=formula, inchikey=hit[0] if hit else None,
                        smiles=hit[1] if hit else None, source=src))
    return pd.DataFrame(out)
