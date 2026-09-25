"""Select the dielectric-combination variant of Z0e on the TRAIN split only."""
import itertools
import sys
from functools import lru_cache

import numpy as np
import pandas as pd

from zcosmo.cosmosac import Mixture
from zcosmo.models import load_z_params, ROOT
from zcosmo.zmodel import c_es_theory
from zcosmo.scope import psat

D = pd.read_csv(ROOT / "results/qc/dielectric.csv").set_index("inchikey")


def eps_pair(k1, k2, kind, rule):
    e1, e2 = (D.loc[k1, "eps"], D.loc[k2, "eps"]) if kind == "static" else (D.loc[k1, "n2"], D.loc[k2, "n2"])
    if rule == "arith":
        return 0.5 * (e1 + e2)
    if rule == "geom":
        return np.sqrt(e1 * e2)
    return 2 / (1 / e1 + 1 / e2)


def params(k1, k2, kind, rule):
    e = eps_pair(k1, k2, kind, rule)
    return load_z_params("Z0").with_(A_ES=c_es_theory(fpol=(e - 1) / (e + 0.5)))


def score(kind, rule, split="train"):
    idac = pd.read_csv(ROOT / "data/benchmark/idac.csv")
    idac = idac[(idac.split == "train") == (split == "train")]
    idac = idac[idac.has_sigma]
    errs = []
    for r in idac.itertuples():
        try:
            m = Mixture([r.solute, r.solvent], params(r.solute, r.solvent, kind, rule))
            errs.append(abs(m.lngamma_inf(r.T, 0) - r.ln_gamma_inf))
        except (KeyError, FileNotFoundError):
            pass
    vle = pd.read_csv(ROOT / "data/benchmark/vle.csv")
    vle = vle[((vle.split == "train") == (split == "train")) & vle.has_sigma]
    vle = vle.sample(min(4000, len(vle)), random_state=0)
    ve = []
    for r in vle.itertuples():
        p1, p2 = psat(r.c1, r.T), psat(r.c2, r.T)
        if np.isnan(p1) or np.isnan(p2):
            continue
        try:
            m = Mixture([r.c1, r.c2], params(r.c1, r.c2, kind, rule))
        except (KeyError, FileNotFoundError):
            continue
        x = np.array([r.x1, 1 - r.x1])
        g = np.exp(m.lngamma(r.T, np.clip(x, 1e-12, 1)))
        ve.append(abs(100 * (x[0] * g[0] * p1 + x[1] * g[1] * p2 - r.P) / r.P))
    return np.nanmean(errs), np.nanmedian(ve), np.nanmean(np.clip(ve, None, 200)), len(errs), len(ve)


if __name__ == "__main__":
    rows = []
    for kind, rule in itertools.product(["static", "optical"], ["arith", "geom", "harm"]):
        r = score(kind, rule)
        rows.append((kind, rule) + r)
        print(kind, rule, r, flush=True)
    t = pd.DataFrame(rows, columns=["kind", "rule", "idac_mae", "vle_median", "vle_mean_clip200", "n_idac", "n_vle"])
    t["rank"] = t.idac_mae.rank() + t.vle_median.rank()
    t.to_csv(ROOT / "results/z0s_selection_train.csv", index=False)
    print(t.sort_values("rank"))
