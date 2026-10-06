"""Z0x: composition-dependent dielectric screening, thermodynamically consistent by construction."""
from __future__ import annotations

from functools import lru_cache
import os

import numpy as np
import pandas as pd

from zcosmo.cosmosac import Mixture, load_fluid, solve_gamma, _pure_lnG, SIG, R_KCAL
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

    def _analytic(self, T, x1):
        x = np.array([x1, 1 - x1])
        mix = Mixture(self.keys, self.z0.with_(A_ES=self._c(x1)))
        A, aeff = mix.A, mix.prm.aeff
        psA = np.array([f.psigA.ravel() for f in mix.fl])
        p = (x @ psA) / (x @ A)
        E = mix._E(T)
        ym = np.log(solve_gamma(E, p))
        yi = np.array([_pure_lnG(f.key, round(float(T), 6), mix.prm, psA[i].tobytes())
                       for i, f in enumerate(mix.fl)])
        lg = (mix.lngamma_comb(x) + np.sum(psA * (ym - yi), axis=1) / aeff
              + mix.lngamma_disp(x, T))
        sig = np.tile(SIG, 3)
        ED = E * (sig[:, None] + sig[None, :]) ** 2
        z = p * np.exp(ym)
        zpure = (psA / A[:, None]) * np.exp(yi)
        moment = z @ ED @ z
        pure_moments = np.einsum("ki,ij,kj->k", zpure, ED, zpure)
        gc = ((x @ A) * moment - (x * A) @ pure_moments) / (2 * R_KCAL * round(float(T), 6) * aeff)
        volume = x @ self.V
        eps = (x * self.V) @ self.eps / volume
        deps = self.V.prod() * (self.eps[0] - self.eps[1]) / volume ** 2
        dc = c_es_theory(fpol=1.0) * 1.5 * deps / (eps + 0.5) ** 2
        return lg + np.array([1 - x1, -x1]) * gc * dc

    def _endpoint(self, T, x1):
        """Exact pure endpoint of the same excess-Gibbs model, not a stencil.

        g_c is zero at a pure endpoint because g(pure,c)=0 for every c.
        Use a new Mixture to avoid the rounded-c, first-insertion cache.
        """
        if x1 not in (0.0, 1.0):
            raise ValueError("_endpoint requires an exactly pure composition")
        mix = Mixture(self.keys, self.z0.with_(A_ES=self._c(x1)))
        return mix.lngamma(T, np.array([x1, 1.0 - x1]))

    def lngamma(self, T, x):
        x1 = float(x[0])
        # Prospective A numerical correction. Defaults remain historical.
        if x1 in (0.0, 1.0) and os.environ.get("ZC_R6_ENDPOINT", "0") == "1":
            return self._endpoint(T, x1)
        h = self.H
        if h < x1 < 1 - h:
            return self._analytic(T, x1)
        a, b = max(x1 - h, 0.0), min(x1 + h, 1.0)
        dg = (self._g(T, b) - self._g(T, a)) / (b - a)
        g = self._g(T, x1)
        return np.array([g + (1 - x1) * dg, g - x1 * dg])

    def lngamma_inf(self, T, solute_index=0):
        x = np.array([0.0, 1.0]) if solute_index == 0 else np.array([1.0, 0.0])
        return float(self.lngamma(T, x)[solute_index])
