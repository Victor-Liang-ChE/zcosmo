"""Run LLE predictions for one model in parallel over systems. Usage: python scripts/lle_parallel.py MODEL NPROC"""
import sys
import multiprocessing as mp

import numpy as np
import pandas as pd

from zcosmo.evaluate import predict_lle, _smiles, BENCH, PRED

MODEL = sys.argv[1]
NPROC = int(sys.argv[2]) if len(sys.argv) > 2 else 8


def run(d):
    d = d.copy()
    d["pred_split"], d["pred_x1_I"], d["pred_x1_II"] = predict_lle(MODEL, d, _smiles())
    return d


if __name__ == "__main__":
    df = pd.read_csv(BENCH / "lle.csv")
    df = df[df.has_sigma].reset_index(drop=True)
    sysk = (df.c1 + "|" + df.c2).to_numpy()
    u = np.unique(sysk)
    parts = [df[np.isin(sysk, u[i::NPROC])] for i in range(NPROC)]
    with mp.get_context("spawn").Pool(NPROC) as p:
        out = p.map(run, parts)
    res = pd.concat(out).sort_index()
    res.to_csv(PRED / f"{MODEL}__lle__all.csv", index=False)
    print("done", MODEL, len(res))
