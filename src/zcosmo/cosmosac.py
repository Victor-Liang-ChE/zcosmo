"""COSMO-SAC 2010 / COSMO-SAC-dsp in NumPy, plus a hook for replacing constants.

Follows Hsieh, Sandler & Lin (2010) and Hsieh, Lin & Vrabec (2014) as
implemented in the NIST benchmark code (Bell et al., JCTC 2020). Every
constant lives in a `Params` object so the Z0 model can swap each one for a
computed value and the ablation can switch them one at a time.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, replace
from functools import lru_cache
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SIGMA_DIR = ROOT / "data" / "raw" / "nist" / "UD" / "sigma3"
SIG = np.linspace(-0.025, 0.025, 51)
N_A = 6.022140758e23
K_B = 1.38064903e-23
R_KCAL = K_B * N_A / 4184.0


@dataclass(frozen=True)
class Params:
    aeff: float = 7.25            # A^2, effective segment area
    c_OH_OH: float = 4013.78      # kcal A^4 / (mol e^2)
    c_OT_OT: float = 932.31
    c_OH_OT: float = 3016.43
    A_ES: float = 6525.69         # kcal A^4 / (mol e^2)
    B_ES: float = 1.4859e8        # kcal A^4 K^2 / (mol e^2)
    q0: float = 79.53
    r0: float = 66.69
    z: float = 10.0
    use_dsp: bool = True
    w_dsp: float = 0.27027
    # "dsp" = Hsieh 2014 fitted form; "london" = first-principles D4/London term; "none"
    disp_mode: str = "dsp"
    london_table: str = "results/qc/dispersion.csv"
    # optional per-compound dispersion energies (e/kB, K) overriding the file values
    disp_override: tuple = field(default=(), compare=False)

    def with_(self, **kw):
        return replace(self, **kw)


@dataclass
class Fluid:
    key: str
    psigA: np.ndarray        # (3, 51): NHB, OH, OT, in A^2
    A: float
    V: float
    disp_flag: str
    ekB: float | None
    meta: dict


@lru_cache(maxsize=None)
def _skeleton_index(sigma_dir: str) -> dict:
    idx = {}
    for p in Path(sigma_dir).glob("*.sigma"):
        idx.setdefault(p.stem[:14], []).append(p)
    return idx


def sigma_path(inchikey: str, sigma_dir: str = str(SIGMA_DIR)) -> Path | None:
    """Exact InChIKey match, else a unique match on the connectivity block (stereo-free).

    If ZC_SIGMA_OVERRIDE_DIR is set and holds <inchikey>.sigma, that file wins (used for the
    conformer and open-profile experiments; never set for the main scorecard)."""
    import os
    ov = os.environ.get("ZC_SIGMA_OVERRIDE_DIR")
    if ov and sigma_dir == str(SIGMA_DIR) and (Path(ov) / f"{inchikey}.sigma").exists():
        return Path(ov) / f"{inchikey}.sigma"
    p = Path(sigma_dir) / f"{inchikey}.sigma"
    if p.exists():
        return p
    c = _skeleton_index(sigma_dir).get(inchikey[:14], [])
    return c[0] if len(c) == 1 else None


@lru_cache(maxsize=None)
def load_fluid(inchikey: str, sigma_dir: str = str(SIGMA_DIR)) -> Fluid:
    p = sigma_path(inchikey, sigma_dir)
    if p is None:
        raise FileNotFoundError(inchikey)
    lines = p.read_text().splitlines()
    meta = json.loads(lines[0][len("# meta: "):])
    vals = np.array([[float(x) for x in ln.split()] for ln in lines if ln and not ln.startswith("#")])
    ps = vals[:, 1].reshape(3, 51)
    ekB = meta.get("disp. e/kB [K]")
    return Fluid(key=inchikey, psigA=ps, A=float(ps.sum()), V=float(meta["volume [A^3]"]),
                 disp_flag=meta.get("disp. flag", "NHB"), ekB=None if ekB is None else float(ekB), meta=meta)


def delta_w(T: float, prm: Params) -> np.ndarray:
    """153 x 153 interaction energy matrix (kcal/mol) in NHB|OH|OT block order."""
    sm = SIG[:, None]
    sn = SIG[None, :]
    c_es = prm.A_ES + prm.B_ES / T ** 2
    base = c_es * (sm + sn) ** 2
    opp = (sm * sn) < 0
    diff2 = (sm - sn) ** 2
    chb = np.array([[0, 0, 0], [0, prm.c_OH_OH, prm.c_OH_OT], [0, prm.c_OH_OT, prm.c_OT_OT]])
    W = np.empty((153, 153))
    for i in range(3):
        for j in range(3):
            W[51 * i:51 * i + 51, 51 * j:51 * j + 51] = base - np.where(opp, chb[i, j], 0.0) * diff2
    return W


def solve_gamma(E: np.ndarray, ps: np.ndarray, tol=1e-10, max_iter=5000) -> np.ndarray:
    """Segment activity coefficients for profile ps (length 153, sums to 1).

    E = exp(-DeltaW/RT). Only segments with nonzero probability matter for the
    sums; others still get a value from the same fixed-point expression.
    """
    AA = E * ps[None, :]
    G = np.ones(153)
    for _ in range(max_iter):
        Gn = 1.0 / (AA @ G)
        Gm = 0.5 * (G + Gn)
        if np.max(np.abs((Gm - Gn) / Gm)) < tol:
            G = Gm
            break
        G = Gm
    return G


@lru_cache(maxsize=4096)
def _E_cached(T: float, prm: Params) -> np.ndarray:
    return np.exp(-delta_w(T, prm) / (R_KCAL * T))


@lru_cache(maxsize=200000)
def _pure_lnG(key: str, T: float, prm: Params, psA_bytes: bytes) -> np.ndarray:
    psA = np.frombuffer(psA_bytes)
    return np.log(solve_gamma(_E_cached(T, prm), psA / psA.sum()))


BOHR_A = 0.52917721067
HARTREE_KCAL = 627.509474


@lru_cache(maxsize=None)
def _london_table(path: str) -> dict:
    import pandas as pd
    d = pd.read_csv(ROOT / path)
    return {r.inchikey: (r.C6_au, r.alpha_au) for r in d.itertuples()}


def london_pair_w(f0: Fluid, f1: Fluid, path: str) -> float:
    """Contact exchange energy w = 2 e_ij - e_ii - e_jj (kcal/mol), London theory.

    e_ij = -C6_ij / d_ij^6 with molecular C6 and polarizabilities from D4,
    C6_ij from the London/Slater-Kirkwood combining rule and contact distance
    d_i = diameter of a sphere with the COSMO cavity volume.
    """
    tab = _london_table(path)
    (c0, a0), (c1, a1) = tab[f0.key], tab[f1.key]
    d0 = 2 * (3 * f0.V / (4 * np.pi)) ** (1 / 3) / BOHR_A
    d1 = 2 * (3 * f1.V / (4 * np.pi)) ** (1 / 3) / BOHR_A
    c01 = 2 * c0 * c1 / ((a1 / a0) * c0 + (a0 / a1) * c1)
    e00 = -c0 / d0 ** 6
    e11 = -c1 / d1 ** 6
    e01 = -c01 / ((d0 + d1) / 2) ** 6
    return (2 * e01 - e00 - e11) * HARTREE_KCAL


def london_lngamma(f0: Fluid, f1: Fluid, x, T, prm: "Params"):
    try:
        w = london_pair_w(f0, f1, prm.london_table)
    except KeyError:
        return np.full(2, np.nan)
    A = prm.w_dsp * (prm.z / 2) * w / (R_KCAL * T)
    return np.array([A * x[1] ** 2, A * x[0] ** 2])


def _disp_w(f0: Fluid, f1: Fluid, prm: Params) -> float:
    pair = {f0.disp_flag, f1.disp_flag}
    neg = [{"H2O", "HB-ACCEPTOR"}, {"H2O", "COOH"}, {"COOH", "NHB"}, {"COOH", "HB-DONOR-ACCEPTOR"}]
    return -prm.w_dsp if pair in neg else prm.w_dsp


class Mixture:
    """Binary (or N-component) COSMO-SAC mixture at fixed temperature set per call."""

    def __init__(self, keys, prm: Params = Params(), fluids=None):
        self.fl = fluids if fluids is not None else [load_fluid(k) for k in keys]
        self.prm = prm
        self.A = np.array([f.A for f in self.fl])
        self.V = np.array([f.V for f in self.fl])
        self._pure_cache = {}

    def _E(self, T):
        return _E_cached(round(float(T), 6), self.prm)

    def lngamma_comb(self, x):
        prm = self.prm
        q = self.A / prm.q0
        r = self.V / prm.r0
        l = prm.z / 2 * (r - q) - (r - 1)
        phi_x = r / (x @ r)
        th_phi = (q / (x @ q)) / (r / (x @ r))
        return np.log(phi_x) + prm.z / 2 * q * np.log(th_phi) + l - phi_x * (x @ l)

    def lngamma_resid(self, T, x, E=None):
        E = self._E(T) if E is None else E
        psA = np.array([f.psigA.ravel() for f in self.fl])  # (n, 153)
        mix = (x @ psA) / (x @ self.A)
        lnGm = np.log(solve_gamma(E, mix))
        out = np.empty(len(self.fl))
        for i, f in enumerate(self.fl):
            lnGi = _pure_lnG(f.key, round(float(T), 6), self.prm, psA[i].tobytes())
            out[i] = self.A[i] / self.prm.aeff * np.sum(psA[i] / self.A[i] * (lnGm - lnGi))
        return out

    def lngamma_disp(self, x, T=None):
        if self.prm.disp_mode == "london" and len(self.fl) == 2:
            return london_lngamma(self.fl[0], self.fl[1], x, T, self.prm)
        if self.prm.disp_mode == "none" or not self.prm.use_dsp or len(self.fl) != 2:
            return np.zeros(len(self.fl))
        f0, f1 = self.fl
        ov = dict(self.prm.disp_override)
        e0 = ov.get(f0.key, f0.ekB)
        e1 = ov.get(f1.key, f1.ekB)
        if e0 is None or e1 is None or np.isnan(e0) or np.isnan(e1):
            return np.full(2, np.nan)
        A = _disp_w(f0, f1, self.prm) * (0.5 * (e0 + e1) - np.sqrt(e0 * e1))
        return np.array([A * x[1] ** 2, A * x[0] ** 2])

    def lngamma(self, T, x):
        x = np.asarray(x, float)
        return self.lngamma_comb(x) + self.lngamma_resid(T, x) + self.lngamma_disp(x, T)

    def lngamma_inf(self, T, solute_index=0):
        x = np.zeros(len(self.fl))
        x[1 - solute_index] = 1.0
        # the combinatorial expressions stay finite at x_i = 0 in this form
        return self.lngamma(T, x)[solute_index]
