"""Z0x: composition-dependent dielectric screening, thermodynamically consistent by construction."""
from __future__ import annotations

from functools import lru_cache

import numpy as np
import pandas as pd

from zcosmo.cosmosac import Mixture, load_fluid
from zcosmo.models import load_z_params, ROOT
from zcosmo.zmodel import c_es_theory


@lru_cache(maxsize=1)
def _eps():
    d = pd.read_csv(ROOT / "results/qc/dielectric.csv")
    return dict(zip(d.inchikey, d.eps))


class Z0xBinary:
    ok = True
    H = 1e-4

    def __init__(self, keys):
        e = _eps()
        self.keys = keys
        self.eps = np.array([e[keys[0]], e[keys[1]]])
        self.V = np.array([load_fluid(k).V for k in keys])
        self.z0 = load_z_params("Z0")
        self._mix = {}

    def _c(self, x1):
        phi = np.array([x1, 1 - x1]) * self.V
        phi /= phi.sum()
        eps = float(phi @ self.eps)
        return c_es_theory(fpol=(eps - 1) / (eps + 0.5))

    def _frozen(self, T, x1, c):
        key = round(c, 6)
        if key not in self._mix:
            self._mix[key] = Mixture(self.keys, self.z0.with_(A_ES=c))
        return self._mix[key].lngamma(T, np.array([x1, 1 - x1]))

    def _g(self, T, x1):
        x1 = min(max(x1, 0.0), 1.0)
        lg = self._frozen(T, x1, self._c(x1))
        return x1 * lg[0] + (1 - x1) * lg[1]

    def lngamma(self, T, x):
        x1 = float(x[0])
        h = self.H
        a, b = max(x1 - h, 0.0), min(x1 + h, 1.0)
        dg = (self._g(T, b) - self._g(T, a)) / (b - a)
        g = self._g(T, x1)
        return np.array([g + (1 - x1) * dg, g - x1 * dg])

    def lngamma_inf(self, T, solute_index=0):
        x = np.array([0.0, 1.0]) if solute_index == 0 else np.array([1.0, 0.0])
        return float(self.lngamma(T, x)[solute_index])
