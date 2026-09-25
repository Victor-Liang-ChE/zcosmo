"""Fit the single global scale s of Z1 on the TRAIN split IDAC only."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from zcosmo.cosmosac import Mixture
from zcosmo.models import load_z_params
from zcosmo.zmodel import scaled, write

ROOT = Path(__file__).resolve().parents[2]


def train_mae(prm, df):
    errs = []
    cache = {}
    for r in df.itertuples():
        k = (r.solute, r.solvent)
        if k not in cache:
            cache[k] = Mixture([r.solute, r.solvent], prm)
        v = cache[k].lngamma_inf(r.T, 0)
        if np.isfinite(v):
            errs.append(abs(v - r.ln_gamma_inf))
    return float(np.mean(errs)), len(errs)


def main():
    df = pd.read_csv(ROOT / "data/benchmark/idac.csv")
    df = df[(df.split == "train") & df.has_sigma]
    z0 = load_z_params("Z0")
    grid = np.round(np.arange(0.30, 1.51, 0.05), 3)
    res = []
    for s in grid:
        mae, n = train_mae(scaled(z0, s), df)
        res.append((float(s), mae, n))
        print(f"s={s:.2f} train MAE={mae:.4f} n={n}", flush=True)
    # refine around the best grid point
    s0 = min(res, key=lambda r: r[1])[0]
    for s in np.arange(s0 - 0.04, s0 + 0.041, 0.01):
        mae, n = train_mae(scaled(z0, s), df)
        res.append((float(round(s, 3)), mae, n))
    best = min(res, key=lambda r: r[1])
    write("Z1", scaled(z0, best[0]), f"Z0 with one global scale s={best[0]:.3f} fitted on train IDAC",
          {"s": best[0], "train_MAE": best[1], "scan": res})
    print("best", best)


if __name__ == "__main__":
    main()
