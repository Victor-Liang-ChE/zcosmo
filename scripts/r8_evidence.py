"""Read R7 decisions without re-gating them or running a model."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
from r8_common import BASE, read, write, sha, screening_counts


def audit(root, out):
    root = Path(root)
    p32 = root / 'p32_calibration_gate.json'
    p34 = root / 'p34_primary_screen.json'
    cal, screen = read(p32), read(p34)
    if cal['rows'] != 2302 or cal['targets'] != 25 or len(cal['runs']) != 25:
        raise ValueError('Historical calibration denominator changed')
    if len({r['key'] for r in cal['runs']}) != 25:
        raise ValueError('Duplicate calibration member')
    dsp = cal['checks']['cosmosac_dsp']['candidate_vs_control']
    ud = cal['checks']['cosmosac_dsp']['candidate_vs_UD']
    for model, n in (('cosmosac_dsp', 2271), ('Z0x', 2302)):
        for kind in ('candidate_vs_control', 'candidate_vs_UD'):
            q = cal['checks'][model][kind]
            if q['requested'] != 2302 or q['finite_reference'] != n or q['finite_candidate'] != n or not q['coverage_identical']:
                raise ValueError('Historical calibration coverage changed')
    if cal['passed'] is not False:
        raise ValueError('This report expects the recorded failed P32 gate')
    time_by_arm = {arm: sum(float(r['wall_s'][arm]) for r in cal['runs'])
                   for arm in ('off', 'full')}
    if not all(np.isfinite(t) and t > 0 for t in time_by_arm.values()):
        raise ValueError('Invalid timing data')
    histories = []
    expected = {
        'BKIMMITUMNQMOS-UHFFFAOYSA-N', 'ZIBGPFATKBEMQZ-UHFFFAOYSA-N',
        'XTHFKEDIFFGKHM-UHFFFAOYSA-N', 'LYCAIKOWRPUZTN-UHFFFAOYSA-N',
        'OKKJLVBELUTLKV-UHFFFAOYSA-N'}
    source = {str(p32): sha(p32), str(p34): sha(p34)}
    paths = sorted((root / 'referee').glob('*.result.json'))
    if {p.name.removesuffix('.result.json') for p in paths} != expected:
        raise ValueError('Missing or extra archived referee case')
    for p in paths:
        d = read(p); key = p.name.removesuffix('.result.json')
        if d['key'] != key:
            raise ValueError('Referee identity mismatch')
        source[str(p)] = sha(p)
        row = dict(key=key, status=d['status'], directions=[])
        if d['status'] == 'diagnostic_complete':
            if len(d['records']) != 4:
                raise ValueError('Incomplete directional record')
            for r in d['records']:
                for v in ('full_verdict', 'off_verdict'):
                    if r[v] not in ('consistent', 'inconsistent', 'inconclusive'):
                        raise ValueError('Invalid tri-state verdict')
                row['directions'].append({k: r[k] for k in (
                    'direction', 'full_verdict', 'off_verdict', 'combined_indicator',
                    'full_error', 'off_error', 'missing_response_material')})
        histories.append(row)
    counts = screening_counts(screen['rows'])
    all_directions = [r for h in histories for r in h['directions']]
    ans = dict(base=BASE, source_sha256=source,
        P32=dict(recorded_passed=cal['passed'], rows=2302, targets=25,
            max_dsp_change=dsp['max_abs_change'], median_dsp_change=dsp['median_abs_change'],
            excess_over_original_limit=dsp['max_abs_change'] - .01,
            median_dsp_vs_UD=ud['median_abs_change'],
            worker_seconds=time_by_arm, full_over_off=time_by_arm['full']/time_by_arm['off'],
            count_of_over_limit_queries=None,
            reason_count_unavailable='Archived gate stores extrema, not per-query values',
            pilot_authorized=False, chains_authorized=False),
        P33=dict(cases=histories, completed=sum(h['status']=='diagnostic_complete' for h in histories),
            resolved_omitted_response_directions=sum(r['missing_response_material'] is True for r in all_directions),
            full_inconsistent_directions=sum(r['full_verdict']=='inconsistent' for r in all_directions),
            unknowns_are_not_passes=True),
        P34=counts, primary_repolish_authorized=False)
    write(out, ans)
    print(json.dumps({k: ans[k] for k in ('P32', 'P34')}, indent=2))
    return ans


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--data', default='docs/astra/round7/data')
    p.add_argument('--out', required=True)
    a=p.parse_args()
    if Path(a.out).exists():
        raise FileExistsError(a.out)
    audit(a.data, a.out)


if __name__ == '__main__':
    main()
