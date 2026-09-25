"""Model registry: name -> binary model with lngamma(T, x) and lngamma_inf(T, i)."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import numpy as np

from zcosmo.cosmosac import Mixture, Params
from zcosmo.baselines import UnifacBinary

ROOT = Path(__file__).resolve().parents[2]
ZPARAMS = ROOT / "results" / "z_params"


class _Nan:
    ok = False

    def lngamma(self, T, x):
        return np.full(2, np.nan)

    def lngamma_inf(self, T, i=0):
        return np.nan


@lru_cache(maxsize=None)
def load_z_params(name: str) -> Params:
    d = json.loads((ZPARAMS / f"{name}.json").read_text())
    p = d["params"]
    if "disp_override" in p:
        p["disp_override"] = tuple(tuple(x) for x in p["disp_override"])
    return Params(**p)


BASE = {
    "cosmosac2010": Params(use_dsp=False),
    "cosmosac_dsp": Params(),
}


@lru_cache(maxsize=None)
def _eps_table():
    import pandas as pd
    d = pd.read_csv(ROOT / "results/qc/dielectric.csv")
    return dict(zip(d.inchikey, d.eps))


def z0e_params(keys):
    """Z0 with the COSMO dielectric factor from first-principles pure-liquid permittivities."""
    from zcosmo.zmodel import c_es_theory
    e = _eps_table()
    eps = 0.5 * (e[keys[0]] + e[keys[1]])
    fpol = (eps - 1) / (eps + 0.5)
    return load_z_params("Z0").with_(A_ES=c_es_theory(fpol=fpol))


def z0s_params(keys):
    """Z0s: optical permittivity (Clausius-Mossotti n^2), harmonic mean; chosen on the train split."""
    from zcosmo.z0s_select import params
    return params(keys[0], keys[1], "optical", "harm")


def make_model(name, keys, smiles=None):
    if name == "Z0w2":
        from zcosmo.z0w import Z0w2Binary
        try:
            return Z0w2Binary(keys, smiles)
        except (FileNotFoundError, KeyError):
            return _Nan()
    if name == "Z0w":
        from zcosmo.z0w import Z0wBinary
        try:
            return Z0wBinary(keys, smiles)
        except (FileNotFoundError, KeyError):
            return _Nan()
    if name == "Z0x":
        from zcosmo.z0x import Z0xBinary
        try:
            return Z0xBinary(keys)
        except (FileNotFoundError, KeyError):
            return _Nan()
    if name == "Z0s":
        try:
            return Mixture(keys, z0s_params(keys))
        except (FileNotFoundError, KeyError):
            return _Nan()
    if name == "Z0e":
        try:
            return Mixture(keys, z0e_params(keys))
        except (FileNotFoundError, KeyError):
            return _Nan()
    if name == "unifac_do":
        return UnifacBinary(*smiles)
    if name == "hanna":
        from zcosmo.hanna_model import HannaBinary
        return HannaBinary(*smiles)
    try:
        if name in BASE:
            return Mixture(keys, BASE[name])
        return Mixture(keys, load_z_params(name))
    except FileNotFoundError:
        return _Nan()
