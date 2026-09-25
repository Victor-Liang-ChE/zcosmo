"""Predict every benchmark table with a given model and write predictions.

Usage: python -m zcosmo.evaluate MODEL [--tables idac,vle,lle,he] [--split all|train|test]
Models are defined in zcosmo.models.
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import fsolve

from zcosmo.models import make_model
from zcosmo.scope import psat

ROOT = Path(__file__).resolve().parents[2]
import os
BENCH = Path(os.environ.get("ZC_BENCH", ROOT / "data" / "benchmark"))
PRED = Path(os.environ.get("ZC_PRED", ROOT / "results" / "predictions"))
R_J = 8.314462618


def _smiles():
    c = pd.read_csv(BENCH / "compounds.csv")
    return dict(zip(c.inchikey, c.smiles))


def predict_idac(model_name, df, smi):
    out = np.full(len(df), np.nan)
    cache = {}
    for i, r in enumerate(df.itertuples()):
        k = (r.solute, r.solvent)
        if k not in cache:
            cache[k] = make_model(model_name, [r.solute, r.solvent], [smi[r.solute], smi[r.solvent]])
        m = cache[k]
        try:
            out[i] = m.lngamma_inf(r.T, 0)
        except Exception:
            pass
    return out


def predict_vle(model_name, df, smi):
    Pc = np.full(len(df), np.nan)
    yc = np.full(len(df), np.nan)
    cache = {}
    for i, r in enumerate(df.itertuples()):
        k = (r.c1, r.c2)
        if k not in cache:
            cache[k] = make_model(model_name, [r.c1, r.c2], [smi[r.c1], smi[r.c2]])
        m = cache[k]
        p1, p2 = psat(r.c1, r.T), psat(r.c2, r.T)
        if np.isnan(p1) or np.isnan(p2):
            continue
        x = np.array([r.x1, 1 - r.x1])
        try:
            g = np.exp(m.lngamma(r.T, np.clip(x, 1e-12, 1)))
        except Exception:
            continue
        P = x[0] * g[0] * p1 + x[1] * g[1] * p2
        Pc[i] = P
        yc[i] = x[0] * g[0] * p1 / P
    return Pc, yc


def predict_he(model_name, df, smi, dT=0.5):
    out = np.full(len(df), np.nan)
    cache = {}
    for i, r in enumerate(df.itertuples()):
        k = (r.c1, r.c2)
        if k not in cache:
            cache[k] = make_model(model_name, [r.c1, r.c2], [smi[r.c1], smi[r.c2]])
        m = cache[k]
        x = np.array([r.x1, 1 - r.x1])
        if not (0 < r.x1 < 1):
            continue
        try:
            dlg = (m.lngamma(r.T + dT, x) - m.lngamma(r.T - dT, x)) / (2 * dT)
        except Exception:
            continue
        out[i] = -R_J * r.T ** 2 * float(x @ dlg)
    return out


def binodal(m, T, n=81):
    """Return (x1_I, x1_II) of the liquid-liquid split at T, or None if miscible."""
    xs = np.concatenate([np.logspace(-6, -2, 10), np.linspace(0.02, 0.98, n), 1 - np.logspace(-2, -6, 10)])
    try:
        lg = np.array([m.lngamma(T, np.array([x, 1 - x])) for x in xs])
    except Exception:
        return None
    if not np.all(np.isfinite(lg)):
        return None
    g = xs * np.log(xs) + (1 - xs) * np.log(1 - xs) + xs * lg[:, 0] + (1 - xs) * lg[:, 1]
    # lower convex hull
    pts = list(zip(xs, g))
    hull = []
    for p in pts:
        while len(hull) >= 2:
            (x1, y1), (x2, y2) = hull[-2], hull[-1]
            if (x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1) <= 0:
                hull.pop()
            else:
                break
        hull.append(p)
    hx = [h[0] for h in hull]
    idx = {x: i for i, x in enumerate(xs)}
    best = None
    for a, b in zip(hx[:-1], hx[1:]):
        if idx[b] - idx[a] > 1 and (best is None or b - a > best[1] - best[0]):
            best = (a, b)
    if best is None:
        return None

    def eqs(v):
        xa, xb = v
        xa = min(max(xa, 1e-9), 1 - 1e-9)
        xb = min(max(xb, 1e-9), 1 - 1e-9)
        la = m.lngamma(T, np.array([xa, 1 - xa]))
        lb = m.lngamma(T, np.array([xb, 1 - xb]))
        return [np.log(xa) + la[0] - np.log(xb) - lb[0], np.log(1 - xa) + la[1] - np.log(1 - xb) - lb[1]]

    try:
        sol, info, ier, _ = fsolve(eqs, best, full_output=True)
        if ier == 1 and 0 < sol[0] < sol[1] < 1 and sol[1] - sol[0] > 1e-4:
            return float(sol[0]), float(sol[1])
    except Exception:
        pass
    return best


def predict_lle(model_name, df, smi):
    xI = np.full(len(df), np.nan)
    xII = np.full(len(df), np.nan)
    split = np.zeros(len(df), bool)
    cache, bcache = {}, {}
    for i, r in enumerate(df.itertuples()):
        k = (r.c1, r.c2)
        if k not in cache:
            cache[k] = make_model(model_name, [r.c1, r.c2], [smi[r.c1], smi[r.c2]])
        Tk = round(r.T / 2) * 2
        bk = (k, Tk)
        if bk not in bcache:
            bcache[bk] = binodal(cache[k], float(Tk))
        b = bcache[bk]
        if b is not None:
            split[i] = True
            xI[i], xII[i] = b
    return split, xI, xII


def run(model_name, tables, split="all"):
    PRED.mkdir(parents=True, exist_ok=True)
    smi = _smiles()
    for t in tables:
        df = pd.read_csv(BENCH / f"{t}.csv")
        if os.environ.get("ZC_ONLY_KEYS"):
            keys = set(open(os.environ["ZC_ONLY_KEYS"]).read().split())
            cols = ["solute", "solvent"] if t == "idac" else ["c1", "c2"]
            df = df[df[cols[0]].isin(keys) | df[cols[1]].isin(keys)]
            if os.environ.get("ZC_SIGMA_OVERRIDE_DIR"):
                from zcosmo.cosmosac import sigma_path
                df = df[[sigma_path(a) is not None and sigma_path(b) is not None
                         for a, b in zip(df[cols[0]], df[cols[1]])]]
            df = df.reset_index(drop=True)
        else:
            df = df[df.has_sigma].reset_index(drop=True) if "has_sigma" in df else df
        if split == "train":
            df = df[df.split == "train"].reset_index(drop=True)
        elif split == "test":
            df = df[df.split != "train"].reset_index(drop=True)
        elif split == "temporal":
            df = df[df.temporal].reset_index(drop=True)
        t0 = time.time()
        if t == "idac":
            df["pred_ln_gamma_inf"] = predict_idac(model_name, df, smi)
        elif t == "vle":
            df["pred_P"], df["pred_y1"] = predict_vle(model_name, df, smi)
        elif t == "he":
            df["pred_HE_J"] = predict_he(model_name, df, smi)
        elif t == "lle":
            df["pred_split"], df["pred_x1_I"], df["pred_x1_II"] = predict_lle(model_name, df, smi)
        df.to_csv(PRED / f"{model_name}__{t}__{split}.csv", index=False)
        print(f"{model_name} {t} {split}: {len(df)} rows in {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("model")
    ap.add_argument("--tables", default="idac,vle,he,lle")
    ap.add_argument("--split", default="all")
    a = ap.parse_args()
    run(a.model, a.tables.split(","), a.split)
