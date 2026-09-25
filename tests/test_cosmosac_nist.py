"""Our COSMO-SAC-dsp must reproduce the NIST benchmark implementation."""
from pathlib import Path

import numpy as np
import pandas as pd

from zcosmo.cosmosac import Mixture, Params

ROOT = Path(__file__).resolve().parents[1]


def test_matches_nist_validation_data():
    d = pd.read_csv(ROOT / "data/raw/nist/val/validation_data.csv").dropna(subset=["lngamma0"])
    s = d.sample(300, random_state=0)
    worst = 0.0
    for r in s.itertuples():
        m = Mixture([r.InChIKey0, r.InChIKey1], Params())
        lg = m.lngamma(r.T_K, np.array([r.z0_molar, r.z1_molar]))
        worst = max(worst, abs(lg[0] - r.lngamma0), abs(lg[1] - r.lngamma1))
    assert worst < 1e-6, worst


def test_gibbs_duhem_binary():
    m = Mixture(["LFQSCWFLJHTTHZ-UHFFFAOYSA-N", "XLYOFNOQVPJJNP-UHFFFAOYSA-N"], Params())
    h = 1e-5
    for x in (0.1, 0.3, 0.5, 0.7, 0.9):
        a = m.lngamma(320.0, np.array([x + h, 1 - x - h]))
        b = m.lngamma(320.0, np.array([x - h, 1 - x + h]))
        d = (a - b) / (2 * h)
        assert abs(x * d[0] + (1 - x) * d[1]) < 1e-6
