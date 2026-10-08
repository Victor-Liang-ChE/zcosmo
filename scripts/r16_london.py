"""One R16 candidate: D4-based volume regular-solution dispersion (LV1).

A physical approximation, never an E-equivalent replacement for London.
No production registry/default is modified. No data is read at import time.
The original residual is evaluated once and shared by the two comparison arms.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
import os
import numpy as np

BOHR_A = 0.52917721067
HARTREE_KCAL = 627.509474
R_KCAL = 1.38064903e-23 * 6.022140758e23 / 4184.0  # Match current evaluator.
RECIPE = 'R16-LV1-cohesive-density-SK-volume-regular-solution'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def positive_pair(values, name):
    a = np.array(values, dtype=float, copy=True)
    require(a.shape == (2,) and np.isfinite(a).all() and (a > 0).all(),
            'Expected two finite positive ' + name)
    return a


def state(T, x):
    T = float(T)
    a = np.asarray(x, dtype=float)
    require(math.isfinite(T) and T > 0 and a.shape == (2,) and
            np.isfinite(a).all() and (a >= 0).all() and (a <= 1).all() and
            abs(float(a.sum()) - 1.0) <= 1e-14, 'Invalid binary state')
    return T, a


def sech_parts(t):
    """sech(t), 1-sech(t), with a stable nonnegative small-difference term."""
    t = abs(float(t))
    a = math.exp(-t)
    den = 1.0 + a*a
    return 2.0*a/den, math.expm1(-t)**2/den


@dataclass(frozen=True)
class LondonPair:
    c6: tuple
    alpha: tuple
    volumes: tuple

    def __post_init__(self):
        for name in ('c6', 'alpha', 'volumes'):
            object.__setattr__(self, name, tuple(positive_pair(getattr(self, name), name)))
        require(all(math.isfinite(v) and v > 0 for v in self.self_energies()),
                'Descriptor/volume range gives invalid self-contact energy')

    def diameters(self):
        return 2.0 * (3.0*np.array(self.volumes)/(4.0*np.pi))**(1.0/3.0) / BOHR_A

    def self_energies(self):
        """Positive magnitudes u_i=C6_ii/d_i^6, kcal/mol of contacts."""
        with np.errstate(over='raise', under='ignore', divide='raise', invalid='raise'):
            return np.array(self.c6) / self.diameters()**6 * HARTREE_KCAL

    def spectral(self):
        c0, c1 = self.c6
        a0, a1 = self.alpha
        t = 0.5*(math.log(c0)-math.log(c1)) - math.log(a0) + math.log(a1)
        return sech_parts(t)

    def old_audit(self):
        """Exact algebraic decomposition, not attribution of experimental error."""
        u = self.self_energies()
        di = self.diameters()
        kappa, one_minus_kappa = self.spectral()
        geom, _ = sech_parts(0.5*math.log(float(di[0]/di[1])))
        q = geom**6
        root = math.sqrt(float(u[0]*u[1]))
        parts = ((math.sqrt(u[0])-math.sqrt(u[1]))**2,
                 2*root*one_minus_kappa,
                 2*root*kappa*(1-q))
        # Direct reference expression follows current london_pair_w arithmetic.
        c0, c1 = self.c6
        a0, a1 = self.alpha
        cross = 2*c0*c1 / ((a1/a0)*c0 + (a0/a1)*c1)
        old_w = float((c0/di[0]**6 + c1/di[1]**6 -
                       2*cross/((di[0]+di[1])/2)**6)*HARTREE_KCAL)
        require(math.isfinite(old_w) and abs(old_w-sum(parts)) <=
                1e-10*max(1.0, float(u.max())), 'London decomposition failed')
        return dict(kappa=kappa, geometry_factor=q, self_energies_kcal=u.tolist(),
                    w_kcal=old_w, components_kcal=dict(cohesive_mismatch=parts[0],
                    spectral_mismatch=parts[1], arithmetic_contact_size=parts[2]))

    def coefficients(self):
        """Original Margules numerator L and new energy-density K.

        L=(z/2)w, kcal/mol. K=(z/2)[u1/V1+u2/V2-
        2*kappa*sqrt(u1*u2/(V1*V2))], kcal/mol/A^3. z=10 and weight=1
        are inherited, explicitly unmodified conventions, not newly fitted.
        """
        old = 5.0*self.old_audit()['w_kcal']
        u = self.self_energies()/np.array(self.volumes)
        _, omk = self.spectral()
        K = 5.0*((math.sqrt(u[0])-math.sqrt(u[1]))**2 +
                 2*math.sqrt(float(u[0]*u[1]))*omk)
        require(math.isfinite(K) and K >= 0, 'Invalid cohesive-density coefficient')
        return old, K


class DispersionChange:
    """Only the difference between the two excess-Gibbs terms, at fixed inputs."""
    def __init__(self, pair: LondonPair):
        self.pair = pair
        self.volumes = np.array(pair.volumes)
        self.L, self.K = pair.coefficients()

    def energies(self, x):
        """Old and LV1 molar excess energies in kcal/mol (T independent)."""
        _, x = state(1.0, x)
        V = float(x @ self.volumes)
        phi = x*self.volumes/V
        return float(self.L*x[0]*x[1]), float(V*phi[0]*phi[1]*self.K)

    def terms(self, T, x):
        T, x = state(T, x)
        phi = x*self.volumes/float(x @ self.volumes)
        old = self.L * x[::-1]**2/(R_KCAL*T)
        new = self.K * self.volumes * phi[::-1]**2/(R_KCAL*T)
        return old, new

    def delta(self, T, x, h=1e-4, exact_endpoint=True):
        """Match the current base dispatch, including its near-endpoint stencil.

        This avoids silently converting the adjacent numerical strip to a new
        derivative prescription. P28 endpoints are exact only when enabled.
        """
        T, x = state(T, x)
        t = float(x[0])
        require(math.isfinite(h) and 0 < h < 0.5, 'Invalid stencil')
        if h < t < 1-h or (t in (0., 1.) and exact_endpoint):
            old, new = self.terms(T, x)
            return new-old
        def dg(v):
            old, new = self.energies([v, 1-v])
            return (new-old)/(R_KCAL*T)
        lo, hi = max(t-h, 0.), min(t+h, 1.)
        slope = (dg(hi)-dg(lo))/(hi-lo)
        g = dg(t)
        return np.array([g+(1-t)*slope, g-t*slope])


class PairedLondon:
    """Adapter for the unchanged Z0x baseline and exactly one LV1 candidate."""
    ok = True

    def __init__(self, baseline, pair: LondonPair):
        p = baseline.z0
        require(p.disp_mode == 'london' and p.w_dsp == 1.0 and p.z == 10.0,
                'LV1 requires the original registered London convention')
        require(np.array_equal(np.asarray(baseline.V), np.array(pair.volumes)),
                'Density and COSMO-volume conventions differ')
        self.baseline = baseline
        self.change = DispersionChange(pair)

    def paired(self, T, x):
        T, x = state(T, x)
        old = np.asarray(self.baseline.lngamma(T, x), dtype=float)
        delta = self.change.delta(T, x, self.baseline.H,
                os.environ.get('ZC_R6_ENDPOINT', '0') == '1')
        require(old.shape == (2,) and np.isfinite(old).all(), 'Invalid baseline result')
        new = old+delta
        require(np.isfinite(new).all(), 'Invalid LV1 result')
        return old, new

    def lngamma(self, T, x):
        return self.paired(T, x)[1]

    def lngamma_inf(self, T, solute_index=0):
        require(solute_index in (0, 1), 'Invalid solute index')
        x = np.zeros(2); x[1-solute_index] = 1.0
        return float(self.lngamma(T, x)[solute_index])


def make_pair(keys):
    """Real source imports are lazy; caller must freeze inputs before calling."""
    from zcosmo.z0x import Z0xBinary
    from zcosmo.cosmosac import _london_table, load_fluid
    base = Z0xBinary(keys)
    desc = _london_table(base.z0.london_table)
    pair = LondonPair(tuple(desc[k][0] for k in keys),
                      tuple(desc[k][1] for k in keys),
                      tuple(load_fluid(k).V for k in keys))
    return PairedLondon(base, pair)
