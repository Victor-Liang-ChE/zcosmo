"""R12 arithmetic. Retrospective explanations do not authorize profile adoption."""
from __future__ import annotations
import numpy as np
from r4_glycols import shapley_three
from r10_sources import DATA

CORNERS = tuple(f'{i:03b}' for i in range(8))
GLYCOLS = {
    'LYCAIKOWRPUZTN-UHFFFAOYSA-N': ('ethylene_glycol', 9),
    'MTHSVFCYNBDYFN-UHFFFAOYSA-N': ('diethylene_glycol', 108),
    'ZIBGPFATKBEMQZ-UHFFFAOYSA-N': ('triethylene_glycol', 17),
    'UWHCKJMYHZGTIT-UHFFFAOYSA-N': ('tetraethylene_glycol', 7),
}
CHANNELS = ('NHB', 'OH', 'OT')
BANDS = ('negative_tail', 'negative_shoulder', 'centre',
         'positive_shoulder', 'positive_tail')
SIG = np.arange(-25, 26, dtype=float)/1000
PARITY_TOL = 1e-8
IDENTITY_TOL = 1e-10


def require(ok, message):
    if not ok:
        raise ValueError(message)


def finite(x):
    a = np.asarray(x, dtype=float)
    require(np.isfinite(a).all(), 'Nonfinite arithmetic input')
    return a


def profile(x):
    a = finite(x)
    require(a.shape == (3, 51) and (a >= 0).all() and a.sum() > 0,
            'Expected a positive-total, nonnegative 153-bin area profile')
    return a


def hybrid(open_bins, open_meta, other_bins, other_meta, corner):
    """Same P21 bit order: area, volume, separately normalized 153-bin shape."""
    require(corner in CORNERS, 'Unknown factorial corner')
    o, c = map(profile, (open_bins, other_bins))
    for m in (open_meta, other_meta):
        require(np.isfinite(m['volume [A^3]']) and m['volume [A^3]'] > 0,
                'Invalid cavity volume')
    ia, iv, ip = map(int, corner)
    area = float(c.sum() if ia else o.sum())
    shape = c/c.sum() if ip else o/o.sum()
    meta = dict(open_meta)
    meta.update({'area [A^2]': area,
                 'volume [A^3]': other_meta['volume [A^3]'] if iv else open_meta['volume [A^3]'],
                 'source': 'R12 explanatory counterfactual; never adopted'})
    return area*shape, meta


def band_masks():
    # Integer millithresholds avoid arange/linspace ambiguity at +/-0.005, 0.010.
    k = np.arange(-25, 26)
    masks = (k <= -10, (k > -10) & (k <= -5), abs(k) < 5,
             (k >= 5) & (k < 10), k >= 10)
    require(np.array_equal(np.sum(masks, axis=0), np.ones(51, dtype=int)),
            'Bands must partition the entire output grid exactly once')
    return dict(zip(BANDS, masks))


def vector_regions(d):
    """Additive L1 accounting, not an interaction-energy decomposition."""
    d = finite(d)
    require(d.shape == (3, 51), 'Wrong difference shape')
    norm = float(abs(d).sum())
    cells = []
    for band, mask in band_masks().items():
        for j, channel in enumerate(CHANNELS):
            v = d[j, mask]
            mass = float(v.sum()); local = float(abs(v).sum())
            cells.append(dict(band=band, channel=channel, signed_mass=mass,
                L1=local, share_of_L1=local/norm if norm > 0 else None,
                signed_first_moment=float(v @ SIG[mask])))
    collapsed = d.sum(axis=0)
    collapsed_L1 = float(abs(collapsed).sum())
    require(abs(sum(c['L1'] for c in cells)-norm) < 1e-12*max(1., norm),
            'Regional L1 accounting failed')
    require(abs(sum(c['signed_mass'] for c in cells)-d.sum()) < 1e-12*max(1., norm),
            'Regional signed accounting failed')
    require(abs(sum(c['signed_first_moment'] for c in cells)-(d*SIG).sum()) < 1e-12*max(1., norm),
            'Regional moment accounting failed')
    require(collapsed_L1 <= norm+1e-12*max(1., norm), 'Triangle inequality failed')
    return dict(L1_153=norm, signed_total=float(d.sum()),
                first_moment=float((d*SIG).sum()), L1_collapsed_51=collapsed_L1,
                channel_cancellation_L1=max(0., norm-collapsed_L1), cells=cells)


def regional_panel(summary):
    expected = {r[1]:r[0] for r in DATA}
    rows = summary['rows']
    require(summary.get('paired_integrity_passed') is True and len(rows) == 12 and
            {r['key'] for r in rows} == set(expected), 'Need the complete accepted R11 input panel')
    result = []
    for r in rows:
        require(expected[r['key']] == r['name'] and r['status'] == 'paired_complete', 'Changed R11 identity')
        ds = r['descriptors']
        p = {k:profile(ds[k]['post_HB_bins_A2']) for k in ('UD', 'P25', 'RO', 'RU')}
        metrics = {}
        for units in ('area_profile', 'normalized_profile'):
            v = p if units == 'area_profile' else {k:a/a.sum() for k,a in p.items()}
            d = dict(total=v['UD']-v['RO'], coordinate=v['RU']-v['RO'],
                     method=v['UD']-v['RU'], repeat=v['RO']-v['P25'])
            require(abs(d['total']-d['coordinate']-d['method']).max() < 1e-10,
                    'Ordered profile identity failed')
            metrics[units] = {k:vector_regions(a) for k,a in d.items()}
        result.append(dict(key=r['key'], name=r['name'], regions=metrics))
    return dict(rows=result, R11_classification=summary['classification'],
        new_labels=False, SCF_calls=0, model_calls=0, adopted=False,
        band_units='sigma in e/A^2; area-profile mass A^2, normalized mass dimensionless',
        meaning='Disjoint descriptive partitions. Channel cancellation is not an HB energy or error contribution.')


def error_summary(y0, yc, yu, truth, phi_y, phi_gain):
    y0, yc, yu, truth, phi_y, phi_gain = map(finite, (y0, yc, yu, truth, phi_y, phi_gain))
    n = len(truth)
    require(n > 0 and all(a.shape == (n,) for a in (y0,yc,yu)) and
            phi_y.shape == phi_gain.shape == (3,n), 'Error-summary shape mismatch')
    out = dict(rows=n)
    for name, y in (('O',y0), ('C',yc), ('U',yu)):
        err = y-truth
        out[name] = dict(MAE=float(abs(err).mean()), bias=float(err.mean()))
    removed = out['O']['MAE']-out['C']['MAE']
    remaining = out['C']['MAE']-out['U']['MAE']
    available = out['O']['MAE']-out['U']['MAE']
    out.update(MAE_removed_O_to_C=removed, MAE_remaining_C_to_U=remaining,
        MAE_gap_O_to_U=available,
        signed_recovery_fraction=removed/available if available > 1e-6 else None,
        mean_prediction_shift=float((yc-y0).mean()),
        improved_rows=int((abs(yc-truth)<abs(y0-truth)).sum()),
        worsened_rows=int((abs(yc-truth)>abs(y0-truth)).sum()),
        prediction_ShAP={k:float(v.mean()) for k,v in zip(('area','volume','shape'),phi_y)},
        absolute_error_reduction_ShAP={k:float(v.mean()) for k,v in zip(('area','volume','shape'),phi_gain)})
    require(abs(removed+remaining-available) < IDENTITY_TOL, 'Error telescope failed')
    require(abs(sum(out['prediction_ShAP'].values())-out['mean_prediction_shift']) < IDENTITY_TOL,
            'Prediction Shapley identity failed')
    require(abs(sum(out['absolute_error_reduction_ShAP'].values())-removed) < IDENTITY_TOL,
            'Absolute-error Shapley identity failed')
    return out


def explanatory_scores(rows, legacy, exact):
    """Audit all 332 archived rows; replay and score only the fixed 141 glycol rows.

    legacy has 2 columns (original P21 000 and UD anchors) on the 141-row target.
    exact has 9 columns (eight O->C corners and full U) on the 141-row target.
    A missing/nonfinite value blocks the complete-panel result, never drops a row.
    """
    require(len(rows) == 332, 'P21 332-row universe changed')
    ids = [str(r['r3_row_id']) for r in rows]
    require(len(set(ids)) == 332 and len({r['solvent'] for r in rows}) == 14, 'P21 identity universe changed')
    idx = np.array([i for i,r in enumerate(rows) if r['solvent'] in GLYCOLS], dtype=int)
    require(len(idx) == 141, 'Expected 141 fixed linear-glycol rows')
    for key, (_name,n) in GLYCOLS.items():
        require(sum(r['solvent'] == key for r in rows) == n, 'Glycol denominator changed')
    l = np.asarray(legacy,float); x = np.asarray(exact,float)
    require(l.shape == (141,2) and x.shape == (141,9), 'Missing factorial dimensions')
    target = [rows[i] for i in idx]
    old = finite([[r[c] for c in (*CORNERS,'UD')] for r in rows])
    require(abs(old[:,7]-old[:,8]).max() < IDENTITY_TOL, 'Archived P21 111 is not full UD')
    anchors=old[idx][:,[0,8]]
    finite_l = np.isfinite(l); finite_x = np.isfinite(x)
    parity = bool(finite_l.all() and abs(l-anchors).max() < PARITY_TOL)
    status = dict(legacy_requested=282, legacy_finite=int(finite_l.sum()),
        exact_requested=1269, exact_finite=int(finite_x.sum()),
        legacy_parity_passed=parity,
        legacy_max_error=float(abs(l-anchors).max()) if finite_l.all() else None,
        complete=bool(parity and finite_x.all()), model='Z0x',
        endpoint='P28 exact, ZC_R6_ENDPOINT=1', adopted=False)
    if not status['complete']:
        return dict(status=status, aggregate_errors=None, private_rows=[])
    truth = finite([r['ln_gamma_inf'] for r in target])
    values = {c:x[:,j] for j,c in enumerate(CORNERS)}
    phi_y = shapley_three(values)
    losses = {c:abs(values[c]-truth) for c in CORNERS}
    phi_gain = -shapley_three(losses)
    require(abs(phi_y.sum(axis=0)-(x[:,7]-x[:,0])).max() < IDENTITY_TOL,
            'Per-row prediction Shapley identity failed')
    require(abs(phi_gain.sum(axis=0)-(losses['000']-losses['111'])).max() < IDENTITY_TOL,
            'Per-row absolute-error Shapley identity failed')
    pooled = error_summary(x[:,0],x[:,7],x[:,8],truth,phi_y,phi_gain)
    solvents = []
    for key,(name,n) in GLYCOLS.items():
        use = np.array([r['solvent'] == key for r in target])
        q = error_summary(x[use,0],x[use,7],x[use,8],truth[use],phi_y[:,use],phi_gain[:,use])
        # Endpoint bridge never subtracts a legacy O score from an exact C score.
        oo = old[idx[use]]
        q['legacy_P21'] = dict(O_MAE=float(abs(oo[:,0]-truth[use]).mean()),
                               U_MAE=float(abs(oo[:,8]-truth[use]).mean()))
        q['endpoint_bridge'] = dict(O_MAE_change=q['O']['MAE']-q['legacy_P21']['O_MAE'],
                                     U_MAE_change=q['U']['MAE']-q['legacy_P21']['U_MAE'])
        solvents.append(dict(name=name,key=key,**q))
    macro = {f'{a}_MAE':float(np.mean([s[a]['MAE'] for s in solvents])) for a in ('O','C','U')}
    macro['MAE_removed_O_to_C'] = macro['O_MAE']-macro['C_MAE']
    private_rows = []
    for j,r in enumerate(target):
        private_rows.append(dict(r3_row_id=str(r['r3_row_id']),
            predictions={c:float(x[j,k]) for k,c in enumerate((*CORNERS,'UD'))},
            prediction_ShAP=phi_y[:,j].tolist(), absolute_error_reduction_ShAP=phi_gain[:,j].tolist()))
    return dict(status=status, aggregate_errors=dict(solvents=solvents, pooled=pooled,
        equal_solvent_mean=macro, requested_P21_rows=332, audit_only_other_rows=191), private_rows=private_rows)
