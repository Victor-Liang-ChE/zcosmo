"""P44 arithmetic only. Profile attribution is not a liquid-state accuracy gate."""
from __future__ import annotations
import numpy as np

CONTROLS = ('water', 'methanol', 'methoxyethanol', 'tetrahydrofuran')
TAILS = ('raw_abs_tail_A2', 'averaged_segment_abs_tail_A2', 'final_binned_tail_A2')
FLOOR_TAIL_A2 = 0.5
FLOOR_SHAPE_L1 = 0.01


def finite(x):
    a = np.asarray(x, dtype=float)
    if not np.isfinite(a).all():
        raise ValueError('Nonfinite arithmetic input')
    return a


def norm(x):
    return float(np.sum(np.abs(finite(x))))


def profiles(x):
    a = finite(x)
    if a.shape != (3, 51) or (a < 0).any() or a.sum() <= 0:
        raise ValueError('Expected a nonnegative 153-bin area profile')
    return a


def split(ud, archived, repeat, cross):
    """Both paths telescope exactly. Repeat drift is retained, never hidden."""
    u, a, r, c = map(finite, (ud, archived, repeat, cross))
    if not (u.shape == a.shape == r.shape == c.shape):
        raise ValueError('Mismatched profile/descriptor shapes')
    out = {'historical_total': u-a, 'historical_geometry': c-a,
           'method': u-c, 'repeat_drift': r-a,
           'current_total': u-r, 'current_geometry': c-r}
    residuals = (out['historical_total']-out['historical_geometry']-out['method'],
                 out['current_total']-out['current_geometry']-out['method'],
                 out['historical_geometry']-out['current_geometry']-out['repeat_drift'])
    if max(norm(x) for x in residuals) > 1e-10 * max(1., norm(u), norm(a)):
        raise ValueError('Telescoping identity failed')
    return {k: v.tolist() for k, v in out.items()}


def scalar_verdict(d, g, m, eta):
    d, g, m, eta = map(float, finite([d, g, m, eta]))
    if eta <= 0 or abs(d-g-m) > 1e-9 * max(1., abs(d), abs(g), abs(m)):
        raise ValueError('Invalid scalar decomposition')
    if g*m < 0 and min(abs(g), abs(m)) > eta:
        return 'inconclusive_cancellation'
    if abs(d) <= 2*eta:
        return 'inconclusive_small_contrast'
    remainder = max(eta, 0.25*abs(d))
    if g*d > 0 and abs(g) > eta and abs(m) <= remainder:
        return 'mainly_geometry'
    if m*d > 0 and abs(m) > eta and abs(g) <= remainder:
        return 'mainly_method'
    if g*d > 0 and m*d > 0 and min(abs(g), abs(m)) > eta:
        return 'both'
    return 'inconclusive_borderline'


def vector_verdict(d, g, m, eta):
    d, g, m = map(finite, (d, g, m)); eta = float(eta)
    if eta <= 0 or not (d.shape == g.shape == m.shape) or norm(d-g-m) > 1e-9:
        raise ValueError('Invalid vector decomposition')
    D, G, M = map(norm, (d, g, m))
    cancellation = max(0., G+M-D)
    if cancellation > max(2*eta, 0.25*D):
        label = 'inconclusive_cancellation'
    elif D <= 2*eta:
        label = 'inconclusive_small_contrast'
    elif M <= max(eta, 0.25*D) and G > eta:
        label = 'mainly_geometry'
    elif G <= max(eta, 0.25*D) and M > eta:
        label = 'mainly_method'
    elif min(G, M) > eta:
        label = 'both'
    else:
        label = 'inconclusive_borderline'
    return dict(label=label, total_L1=D, geometry_L1=G, method_L1=M,
                cancellation_excess_L1=cancellation, background_scale=eta)


def outliers(q, area):
    """Area-weighted diagnostics on retained tesserae. No clipping or neutralizing."""
    q, area = map(finite, (q, area))
    if q.ndim != 1 or area.shape != q.shape or not len(q) or (area <= 0).any():
        raise ValueError('Invalid raw tesserae')
    s = q/area
    order = np.argsort(s, kind='stable')
    cdf = np.cumsum(area[order])/area.sum()
    quantiles = [float(s[order[min(np.searchsorted(cdf, p, side='left'), len(q)-1)]])
                 for p in (.01, .05, .5, .95, .99)]
    ans = dict(segments=len(q), net_charge_e=float(q.sum()),
               area_A2=float(area.sum()), sigma_min=float(s.min()), sigma_max=float(s.max()),
               area_weighted_quantiles=dict(zip(('p01','p05','p50','p95','p99'), quantiles)),
               convention='Discrete area CDF; strict +/-0.025 e/A2 outlier cuts')
    for name, mask in (('negative', s < -.025), ('positive', s > .025)):
        ans[name] = dict(count=int(mask.sum()), area_A2=float(area[mask].sum()),
            area_fraction=float(area[mask].sum()/area.sum()), signed_charge_e=float(q[mask].sum()),
            absolute_charge_e=float(abs(q[mask]).sum()),
            minimum_area_A2=float(area[mask].min()) if mask.any() else None)
    return ans


def describe(parser, output):
    """Use the unchanged R10 stage definitions and add bounded scalar outlier data."""
    from r10_replay import stages
    desc, arrays = stages(parser, output)
    raw, area, _avg, _p = arrays
    desc['outliers'] = outliers(raw*area, area)
    return desc


def native_parity(archived, repeat, old_energy, new_energy):
    a = profiles(archived['post_HB_bins_A2']); r = profiles(repeat['post_HB_bins_A2'])
    checks = dict(max_raw_bin_A2=float(abs(a-r).max()),
        normalized_L1=norm(a/a.sum()-r/r.sum()),
        energy_Eh=abs(float(new_energy)-float(old_energy)),
        net_charge_e=abs(repeat['raw_q_sum_e']-archived['raw_q_sum_e']),
        area_A2=abs(repeat['area_sum_A2']-archived['area_sum_A2']),
        volume_A3=abs(repeat['volume_A3']-archived['volume_A3']))
    limits = dict(max_raw_bin_A2=1e-4, normalized_L1=1e-5, energy_Eh=1e-7,
                  net_charge_e=1e-5, area_A2=1e-4, volume_A3=1e-4)
    passed = all(np.isfinite(v) and v < limits[k] for k, v in checks.items())
    return dict(passed=bool(passed), checks=checks, strict_limits=limits,
                scope='Same RO input; no E-equivalence of different geometries, no affinity gate')


def member_math(ud, archived, repeat, cross):
    ds = (ud, archived, repeat, cross)
    pp = [profiles(d['post_HB_bins_A2']) for d in ds]
    ans = dict(area_profile=split(*pp), normalized_profile=split(*(p/p.sum() for p in pp)),
               tails={k:split(*(d[k] for d in ds)) for k in TAILS},
               net_charge_e=split(*(d['raw_q_sum_e'] for d in ds)))
    return ans


def classify_panel(rows):
    """rows: all 12 members with parity and math. No label from an incomplete panel."""
    from r10_sources import DATA
    names = [r['name'] for r in rows]
    if len(names) != 12 or set(names) != {r[0] for r in DATA}:
        raise ValueError('Incomplete, extra, or duplicate member')
    if any(r.get('status') != 'paired_complete' or not r.get('parity', {}).get('passed') for r in rows):
        return dict(complete=False, reason='native_or_parity_failure', rows=[])
    by = {r['name']:r for r in rows}
    scales = {}
    for key in TAILS:
        d = [by[n]['math']['tails'][key] for n in CONTROLS]
        drift = max(abs(r['math']['tails'][key]['repeat_drift']) for r in rows)
        scales[key] = max(FLOOR_TAIL_A2,
            max(abs(x['current_total']) for x in d),
            max(abs(x['current_geometry']) for x in d), 4*drift)
    d = [by[n]['math']['normalized_profile'] for n in CONTROLS]
    shape_scale = max(FLOOR_SHAPE_L1,
        max(norm(x['current_total']) for x in d),
        max(norm(x['current_geometry']) for x in d),
        4*max(norm(r['math']['normalized_profile']['repeat_drift']) for r in rows))
    result = []
    for r in rows:
        tails = {}
        for key in TAILS:
            s = r['math']['tails'][key]; eta = scales[key]
            label = scalar_verdict(s['current_total'], s['current_geometry'], s['method'], eta)
            old = scalar_verdict(s['historical_total'], s['historical_geometry'], s['method'], eta)
            if label != old: label = 'inconclusive_repeat_boundary'
            tails[key] = dict(s, label=label, background_scale_A2=eta)
        v = r['math']['normalized_profile']
        shape = vector_verdict(v['current_total'], v['current_geometry'], v['method'], shape_scale)
        old = vector_verdict(v['historical_total'], v['historical_geometry'], v['method'], shape_scale)
        if shape['label'] != old['label']: shape['label'] = 'inconclusive_repeat_boundary'
        headline = tails['final_binned_tail_A2']['label']
        if r['name'] in CONTROLS:
            headline = 'background_control_descriptive_only'
        elif headline not in ('mainly_geometry','mainly_method','both') or headline != shape['label']:
            headline = 'metric_dependent_or_inconclusive'
        result.append(dict(name=r['name'], key=r['key'], tails=tails, shape=shape,
                           profile_gap_label=headline))
    return dict(complete=True, rows=result, tail_scales_A2=scales, shape_scale_L1=shape_scale,
        scale_interpretation='Predeclared background envelope, not random noise, a confidence interval, or a convergence proof',
        authorizes_profiles=False, authorizes_conformer_selection=False)
