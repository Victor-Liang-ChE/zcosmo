"""E reporting audit of public, rounded R12 aggregates. No chemistry imports.

This does not rerun P46, access private inputs, or accept a conformer rule.
Cost outputs are explicit sizing scenarios, not measured portfolio forecasts.
"""
from __future__ import annotations
import argparse
from decimal import Decimal as D
import hashlib
import itertools
import json
from pathlib import Path
import time

BASE = 'e2b36c8c5c2273f47ee6df21975b295b93689ca8'
SOURCE = 'docs/astra/round12/RESULTS.md'
SOURCE_BLOB = 'c036e8e24aa45a03aed0485664b3a26cd842c17f'
COUNTS = {'ethylene glycol': 10, 'diethylene glycol': 108,
          'triethylene glycol': 17, 'tetraethylene glycol': 7}
HEADER = ('solvent', 'rows', 'MAE O', 'MAE C', 'MAE U', 'removed O→C',
          'signed recovery', 'rows improved / worsened')


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def decimal(text: str) -> D:
    value = D(text)
    require(value.is_finite(), 'Nonfinite public number')
    return value


def rounding_interval(value: D, places: int = 3) -> tuple[D, D]:
    half = D(5).scaleb(-places - 1)
    return value - half, value + half


def difference_interval(a: D, b: D) -> tuple[D, D]:
    al, ah = rounding_interval(a)
    bl, bh = rounding_interval(b)
    return al - bh, ah - bl


def overlaps(left: tuple[D, D], right: tuple[D, D]) -> bool:
    return max(left[0], right[0]) <= min(left[1], right[1])


def recovery_interval(o: D, c: D, u: D) -> tuple[D, D]:
    require(rounding_interval(o)[0] > rounding_interval(u)[1],
            'Rounded comparator denominator can reach zero')
    corners = itertools.product(*(rounding_interval(v) for v in (o, c, u)))
    values = [(a - b) / (a - z) for a, b, z in corners]
    return min(values), max(values)


def table(text: str) -> dict:
    rows = {}
    active = False
    for line in text.splitlines():
        if not line.startswith('|'):
            if active:
                break
            continue
        cells = tuple(c.strip().replace('**', '') for c in line.strip('|').split('|'))
        if cells == HEADER:
            require(not active, 'Duplicated result header')
            active = True
            continue
        if not active or all(set(c) <= set('-: ') for c in cells):
            continue
        require(len(cells) == len(HEADER), 'Malformed public result row')
        name, count, o, c, u, removed, recovery, changes = cells
        require(name not in rows, 'Duplicate solvent or pooled row')
        require(name in COUNTS or name == 'pooled', 'Unexpected solvent identity')
        imp, bad = map(int, changes.split('/'))
        require(imp >= 0 and bad >= 0, 'Negative outcome count')
        values = list(map(decimal, (o, c, u, removed, recovery)))
        require(all(v >= 0 for v in values[:3]), 'Negative MAE')
        rows[name] = dict(rows=int(count), O=values[0], C=values[1], U=values[2],
                          removed=values[3], recovery=values[4], improved=imp, worsened=bad)
    require(set(rows) == set(COUNTS) | {'pooled'}, 'Missing public solvent or pooled row')
    require({k: rows[k]['rows'] for k in COUNTS} == COUNTS, 'P46a denominators changed')
    pool = rows['pooled']
    require(pool['rows'] == sum(COUNTS.values()) == 142, 'Wrong pooled denominator')
    for name, row in rows.items():
        require(row['improved'] + row['worsened'] == row['rows'], 'Outcome count mismatch')
        require(overlaps(difference_interval(row['O'], row['C']),
                         rounding_interval(row['removed'])), 'Inconsistent rounded MAE reduction')
        require(overlaps(recovery_interval(row['O'], row['C'], row['U']),
                         rounding_interval(row['recovery'], 2)), 'Inconsistent rounded recovery')
    for field in ('improved', 'worsened'):
        require(sum(rows[k][field] for k in COUNTS) == pool[field], 'Pooled outcomes do not add')
    for field in ('O', 'C', 'U'):
        # Weighted solvent means and the published pooled mean were rounded independently.
        lo = sum(COUNTS[k] * rounding_interval(rows[k][field])[0] for k in COUNTS) / 142
        hi = sum(COUNTS[k] * rounding_interval(rows[k][field])[1] for k in COUNTS) / 142
        require(overlaps((lo, hi), rounding_interval(pool[field])), 'Pooled rounding ranges conflict')
    return rows


def sizing(n: int = 630) -> dict:
    require(type(n) is int and n > 0, 'Positive integer portfolio size required')
    cases = []
    for starts in (4, 8):
        evaluations = n * starts * 8
        cases.append(dict(molecules=n, starts_each=starts, assumed_SVP_evaluations_each=8,
            TZVP_single_points=n * starts, SVP_energy_gradient_evaluations=evaluations,
            SVP_evaluation_ceiling_at_80_per_start=n * starts * 80,
            four_core_SVP_hours_at_assumed_seconds={str(t): evaluations * t / 3600 for t in (10, 60, 300)},
            Mac_SP_hours_if_R11_small_panel_mean_transferred=n * starts * (594 / 24) / 3600,
            one_hour_per_start_allocation_worker_hours=n * starts,
            ideal_20_runner_hours_for_that_allocation=n * starts / 20))
    return dict(cases=cases, all_molecules_treated_as_search_eligible_for_sizing=True,
        exact_flexible_population_count_not_measured=True,
        legacy_50_embedding_xTB_relaxations=n * 50,
        notes='Sizing only. No QC execution or account-quota claim. Eight steps is a sample-median '
              'scenario, not a portfolio mean. SVP times omit proposal work and TZVP. Mac '
              'SP extrapolation omits optimization, thermal calculations and validation.')


def arithmetic(rows: dict) -> dict:
    p = rows['pooled']
    o, c, u = (p[k] for k in ('O', 'C', 'U'))
    low, high = recovery_interval(o, c, u)
    return dict(rows=p['rows'], improved=p['improved'], worsened=p['worsened'],
        removed_from_rounded_MAEs=float(o-c), residual_comparator_MAE_gap=float(c-u),
        comparator_gap_recovery=float((o-c)/(o-u)),
        comparator_recovery_rounding_range=[float(low), float(high)],
        original_absolute_error_fraction_removed=float((o-c)/o),
        DEG_row_weight=float(D(COUNTS['diethylene glycol']) / p['rows']),
        interpretation='80 percent refers to the O-to-U comparator gap, not original absolute error. '
                       'The residual is a difference of MAEs, not mean absolute C-minus-U predictions. '
                       'Intervals propagate printed rounding only, not sampling uncertainty.')


def audit(repo: Path) -> dict:
    path = repo / SOURCE
    raw = path.read_bytes()
    require(blob(raw) == SOURCE_BLOB, 'Public R12 source changed; do not infer a new archive')
    rows = table(raw.decode('utf-8'))
    answer = dict(base=BASE, source=SOURCE, source_blob=SOURCE_BLOB,
        source_sha256=hashlib.sha256(raw).hexdigest(), public_aggregate_arithmetic=arithmetic(rows),
        hypothetical_portfolio_sizing=sizing(), SCF_calls=0, activity_model_calls=0,
        private_assets_read=False, adoption_authorized=False, new_scientific_gate_passed=False)
    require(path.read_bytes() == raw, 'Public source changed during audit')
    return answer


def check_docs(repo: Path) -> None:
    readme = (repo / 'README.md').read_text()
    status = (repo / 'docs/astra/round7/GLYCOL_STATUS.md').read_text()
    for phrase in ('142', '1.813', '0.702', '0.419', '80%', '13%', 'retrospective',
                   'No crossed profile', 'closed'):
        require(phrase in readme, 'README closeout qualification missing: ' + phrase)
    for phrase in ('P46a', '0.283', 'difference of MAEs', 'whole-profile', '139',
                   'liquid', 'No adoption', 'closed'):
        require(phrase in status, 'P35 closeout qualification missing: ' + phrase)
    for phrase in ('ZC_R6_ENDPOINT=1', 'compatibility gate', 'six separately flagged S1/S2'):
        require(phrase in readme, 'Earlier README qualification removed: ' + phrase)
    require('the consequences for IDAC error remain unresolved' not in readme,
            'Stale pre-P46 README wording remains')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path('.'))
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--check-docs', action='store_true')
    args = parser.parse_args()
    start = time.perf_counter()
    result = audit(args.repo.resolve())
    if args.check_docs:
        check_docs(args.repo.resolve())
    result['audit_wall_s'] = time.perf_counter() - start
    # Fresh output only. The fixed input is never overwritten.
    with args.out.open('x', encoding='utf-8') as handle:
        json.dump(result, handle, indent=2, allow_nan=False)
        handle.write('\n')
    print('Public rounding/count audit passed. Zero chemistry evaluations; no adoption.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
