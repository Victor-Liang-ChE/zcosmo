"""False-positive test for liquid-liquid splitting.

Negatives: isothermal VLE series whose liquid compositions cover the whole range
(x1 < 0.1 and > 0.9, and at least one point in each of 0.2-0.4, 0.4-0.6, 0.6-0.8),
so the liquid was observed homogeneous across the composition range at that T.
A model that predicts a miscibility gap at that T is a false positive.
Usage: python -m zcosmo.lle_negatives MODEL...
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from zcosmo.evaluate import binodal, _smiles
from zcosmo.models import make_model

ROOT = Path(__file__).resolve().parents[2]


def negative_series():
    v = pd.read_csv(ROOT / "data/benchmark/vle.csv")
    v = v[(v.iso == "T") & v.has_sigma]
    keep = []
    for s, g in v.groupby("series"):
        x = g.x1
        if len(g) < 8 or x.min() > 0.1 or x.max() < 0.9:
            continue
        if all(((x > a) & (x < b)).any() for a, b in [(0.2, 0.4), (0.4, 0.6), (0.6, 0.8)]):
            keep.append(dict(series=s, c1=g.c1.iloc[0], c2=g.c2.iloc[0], T=float(g["T"].median()),
                             split=g.split.iloc[0], name1=g.name1.iloc[0], name2=g.name2.iloc[0]))
    d = pd.DataFrame(keep)
    # one temperature per system: the lowest (hardest for a false split)
    return d.sort_values("T").drop_duplicates(["c1", "c2"]).reset_index(drop=True)


def main(models):
    out = ROOT / "results/predictions/lle_negatives.csv"
    neg = pd.read_csv(out) if out.exists() else negative_series()
    smi = _smiles()
    for m in models:
        fp = []
        for r in neg.itertuples():
            mod = make_model(m, [r.c1, r.c2], [smi[r.c1], smi[r.c2]])
            b = binodal(mod, r.T)
            ok = getattr(mod, "ok", True)
            fp.append(np.nan if not ok else float(b is not None))
        neg[f"fp_{m}"] = fp
        print(m, "false-positive rate", np.nanmean(fp), "n", np.sum(~np.isnan(fp)), flush=True)
    neg.to_csv(out, index=False)


if __name__ == "__main__":
    main(sys.argv[1:])
