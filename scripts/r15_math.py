"""R15 finite-game accounting and endpoint-preserving diagnostic model factory.

No chemistry data is read until make_corner is called. All fitted substitutions
are explanatory interventions, never candidates for production selection.
"""
from __future__ import annotations
import itertools
import math
import numpy as np

FACTORS = ('electrostatic_closure', 'HB_constants', 'London_to_none',
           'aeff_shared', 'profile_convention_shared')
CORNERS = tuple(f'{i:03b}' for i in range(8))
ANCHORS = ('000', '111')
INTERMEDIATE = tuple(c for c in CORNERS if c not in ANCHORS)
TOL_PP = 1e-8


def require(ok, message):
    if not ok:
        raise ValueError(message)


def shared_audit(z0, target):
    """A drift is a failed design, not permission to invent another factor."""
    shared = ('aeff', 'q0', 'r0', 'z', 'london_table', 'disp_override')
    require(all(getattr(z0, n) == getattr(target, n) for n in shared),
            'Non-registered endpoint difference in shared ingredients')
    require(z0.aeff == target.aeff == 7.25 and z0.B_ES == 0.0,
            'Expected common aeff and historical Z0 ES definition')
    require(z0.disp_mode == 'london' and z0.w_dsp == 1.0 and z0.use_dsp,
            'Expected Z0 London endpoint')
    require(target.disp_mode == 'dsp' and not target.use_dsp,
            '2010 target must have no explicit dispersion, not fitted 2014 dsp')
    return dict(shared={n: getattr(z0, n) for n in shared},
        HB_cutoff='same stored NHB/OH/OT split and delta_w opposite-sign mask',
        profile='identical frozen P52 UD bytes for both components in every corner')


def make_corner(keys, corner):
    """Use existing production kernels, including dc/dx only on the Z0x side."""
    require(corner in CORNERS, 'Unknown three-bit corner')
    from zcosmo.cosmosac import Params, Mixture
    from zcosmo.models import load_z_params
    from zcosmo.z0x import Z0xBinary
    z0, target = load_z_params('Z0'), Params(use_dsp=False)
    shared_audit(z0, target)
    e, h, disp = map(int, corner)
    kw = {}
    if h:
        kw.update({n: getattr(target, n) for n in ('c_OH_OH', 'c_OT_OT', 'c_OH_OT')})
    if disp:
        kw.update(use_dsp=False, disp_mode=target.disp_mode, w_dsp=target.w_dsp)
    if e:
        kw.update(A_ES=target.A_ES, B_ES=target.B_ES)
    p = z0.with_(**kw)
    if corner == '111':
        require(p == target, 'All-swapped corner does not exhaust target differences')
    if e:
        # c(T)=A+B/T^2 is independent of composition: dc/dx = 0.
        return Mixture(keys, p)
    model = Z0xBinary(keys)
    model.z0 = p
    model._mix.clear()
    return model


def shapley(values):
    """Exact finite-game Shapley values, first string character is player zero."""
    n = len(next(iter(values)))
    names = tuple(f'{i:0{n}b}' for i in range(2**n))
    require(set(values) == set(names), 'Incomplete cube')
    arrays = {s: np.asarray(values[s], float) for s in names}
    shape = arrays[names[0]].shape
    require(all(a.shape == shape and np.isfinite(a).all() for a in arrays.values()),
            'Nonfinite or misaligned cube')
    ans = np.zeros((n,) + shape)
    for j in range(n):
        for s in names:
            if s[j] == '1':
                continue
            k = s.count('1')
            t = s[:j] + '1' + s[j+1:]
            weight = math.factorial(k) * math.factorial(n-k-1) / math.factorial(n)
            ans[j] += weight * (arrays[t] - arrays[s])
    return ans


def lift_five(values):
    require(set(values) == set(CORNERS), 'Incomplete active cube')
    return {f'{i:05b}': values[f'{i:05b}'[:3]] for i in range(32)}


def dividends(values):
    """Baseline-anchored inclusion/exclusion interactions, not extra experiments."""
    out = {}
    for s in CORNERS[1:]:
        active = [j for j, b in enumerate(s) if b == '1']
        v = np.zeros_like(np.asarray(values['000'], float))
        for bits in itertools.product('01', repeat=len(active)):
            t = ['0'] * 3
            for j, bit in zip(active, bits):
                t[j] = bit
            v += (-1)**(len(active)-bits.count('1')) * np.asarray(values[''.join(t)], float)
        out[s] = v
    return out


def summary(rows, predictions, anchors_passed):
    """Fixed denominator; a single failed corner withholds complete attribution."""
    a = np.asarray(predictions, float)
    require(len(rows) > 0 and a.shape == (len(rows), 8), 'Wrong factorial dimensions')
    ids = [str(r['row_id']) for r in rows]
    require(len(set(ids)) == len(ids), 'Duplicate observation identity')
    truth = np.array([r['P'] for r in rows], float)
    require(np.isfinite(truth).all() and (truth > 0).all(), 'Invalid frozen pressure')
    finite = np.isfinite(a) & (a > 0)
    status = dict(requested_rows=len(rows), requested_corners=8,
        requested_values=8*len(rows), finite_by_corner=dict(zip(CORNERS, finite.sum(0).tolist())),
        complete=bool(finite.all() and anchors_passed), anchors_passed=bool(anchors_passed),
        adopted=False, retrospective=True, fitted_substitutions=True)
    if not status['complete']:
        return dict(status=status, public_errors=None, private_rows=None)
    with np.errstate(over='ignore', invalid='ignore', divide='ignore'):
        signed = 100*(a/truth[:, None]-1)
    if not np.isfinite(signed).all():
        status.update(complete=False, derived_error_nonfinite=int((~np.isfinite(signed)).sum()))
        return dict(status=status, public_errors=None, private_rows=None)
    errors = np.abs(signed)
    value = {c: -errors[:, j] for j, c in enumerate(CORNERS)}
    bias_value = {c: signed[:, j] for j, c in enumerate(CORNERS)}
    phi = shapley(lift_five(value))
    bias_phi = shapley(lift_five(bias_value))
    three = shapley(value)
    efficiency = float(np.max(np.abs(phi.sum(0) - (errors[:, 0]-errors[:, 7]))))
    require(efficiency < TOL_PP, 'Error Shapley efficiency failed')
    require(np.max(np.abs(bias_phi.sum(0)-(signed[:, 7]-signed[:, 0]))) < TOL_PP,
            'Signed-pressure Shapley efficiency failed')
    require(np.max(np.abs(phi[:3]-three)) < TOL_PP and np.array_equal(phi[3:], np.zeros_like(phi[3:])),
            'Shared-factor dummy-player identity failed')
    dd = dividends(value)
    require(np.max(np.abs(sum(dd.values())-(errors[:, 0]-errors[:, 7]))) < TOL_PP,
            'Interaction efficiency failed')
    systems = sorted({r['system'] for r in rows})
    group = [np.array([r['system'] == s for r in rows]) for s in systems]
    avg = lambda x: float(np.mean(x))
    macro = lambda x: float(np.mean([np.mean(x[g]) for g in group]))
    public = dict(rows=len(rows), systems=len(systems), corners={}, factors={}, interactions={},
        max_efficiency_error_pp=efficiency, no_generalization_CI=True,
        profile_source='P52 UD for both endpoints; no profile-source claim',
        direction='stored-epsilon Z0x to COSMO-SAC 2010, not experimental-epsilon Z0x')
    for j, c in enumerate(CORNERS):
        public['corners'][c] = dict(AAD_percent=avg(errors[:, j]), bias_percent=avg(signed[:, j]),
            equal_system_AAD_percent=macro(errors[:, j]),
            improved_vs_000=int((errors[:, j] < errors[:, 0]).sum()),
            worsened_vs_000=int((errors[:, j] > errors[:, 0]).sum()))
    gap = avg(errors[:, 0]-errors[:, 7])
    public['endpoint_gap_pp'] = gap
    for j, name in enumerate(FACTORS):
        public['factors'][name] = dict(error_reduction_pp=avg(phi[j]),
            equal_system_error_reduction_pp=macro(phi[j]),
            signed_bias_change_pp=avg(bias_phi[j]),
            gap_share=None if gap <= 1e-6 else avg(phi[j])/gap,
            one_at_a_time_error_reduction_pp=avg(errors[:, 0]-errors[:, int(''.join('1' if i==j else '0' for i in range(3)),2)])
                if j < 3 else 0.0)
    public['interactions'] = {s: dict(error_reduction_pp=avg(v),
        equal_system_error_reduction_pp=macro(v)) for s, v in dd.items()}
    private = [dict(row_id=ids[i], pressure_kPa=a[i].tolist(),
        absolute_percent_error=errors[i].tolist(), error_ShAP_pp=phi[:, i].tolist(),
        signed_bias_ShAP_pp=bias_phi[:, i].tolist()) for i in range(len(rows))]
    return dict(status=status, public_errors=public, private_rows=private)
