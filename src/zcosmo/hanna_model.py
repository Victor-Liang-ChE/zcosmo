"""HANNA (Hoffmann/Specht et al., Nat. Commun. 2026) wrapped in the benchmark's model interface.

HANNA was trained on ~824k Dortmund Data Bank points, so it has very likely seen many of our test
systems; it is a reference point for what data-driven models reach, not a clean held-out comparison.
"""
from __future__ import annotations

import os
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
HANNA_DIR = ROOT / "third_party" / "HANNA"


@lru_cache(maxsize=1)
def _predictor():
    import torch
    torch.set_num_threads(int(os.environ.get("HANNA_THREADS", "4")))
    sys.path.insert(0, str(HANNA_DIR))
    cwd = os.getcwd()
    os.chdir(HANNA_DIR)
    try:
        from utils.HANNA_predictor import HANNA_Predictor
        p = HANNA_Predictor()
    finally:
        os.chdir(cwd)
    return p


@lru_cache(maxsize=None)
def _emb(smiles: str):
    p = _predictor()
    return p._get_scaled_embeddings_from_smiles([smiles])[0]


class HannaBinary:
    ok = True

    def __init__(self, smiles1: str, smiles2: str):
        self.s = (smiles1, smiles2)
        try:
            self.e = [_emb(smiles1), _emb(smiles2)]
        except Exception:
            self.ok = False

    def lngamma_batch(self, T, x1):
        import torch
        p = _predictor()
        x1 = np.atleast_1d(np.asarray(x1, float))
        n = len(x1)
        tT = p._get_scaled_temperature(float(T)).repeat(n, 1)
        tx = torch.FloatTensor(x1.reshape(-1, 1))
        te = torch.stack(self.e).repeat(n, 1, 1)
        lg, _ = p.model(tT, tx, te)
        return lg.detach().cpu().numpy()

    def lngamma(self, T, x):
        if not self.ok:
            return np.full(2, np.nan)
        return self.lngamma_batch(T, [float(x[0])])[0]

    def lngamma_inf(self, T, solute_index=0):
        if not self.ok:
            return np.nan
        x1 = 0.0 if solute_index == 0 else 1.0
        return float(self.lngamma_batch(T, [x1])[0][solute_index])
