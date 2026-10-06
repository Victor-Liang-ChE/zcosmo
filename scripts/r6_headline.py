"""Reformat archived P27 comparisons, preserving pairwise denominators and LLE scope.

No prediction regeneration, input change, experimental selection or new bootstrap.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from r6_common import BASE,sha,write


def extract(d):
    tables=d['tables'];out={}
    for table in ('idac','vle','he','lle'):
        pairs=tables[table]['pairwise']
        matches=[p for p in pairs if p['model']=='Z0x' and p['arm']=='open630']
        if len(matches)!=1:raise ValueError('one matched Z0x/open630 comparison required per table')
        p=matches[0];r,c=p['reference'],p['candidate']
        if r['rows']!=c['rows'] or r['rows']!=p['common_rows']:raise ValueError('matched denominator changed')
        out[table]=p
    return out


def render(d):
    q=extract(d)
    lines=['Z0x-UD versus primary open profiles, archived P27 matched comparisons','',
        'Historical finite-difference endpoint implementation. No R6 endpoint correction is included.','',
        '| Quantity | Common rows | UD | Open630 | Open minus UD 95% CI |',
        '|---|---:|---:|---:|---|']
    for table,label in [('idac','IDAC MAE, ln units'),('vle','VLE pressure AAD, %'),('he','HE MAE, J/mol')]:
        p=q[table];r,c=p['reference'],p['candidate'];ci=p.get('delta_MAE_CI95')
        if ci is None:raise ValueError('paired uncertainty missing')
        lines.append(f"| {label} | {p['common_rows']} | {r['MAE']:.6g} | {c['MAE']:.6g} | [{ci[0]:.6g}, {ci[1]:.6g}] |")
    p=q['lle'];r,c=p['reference'],p['candidate']
    lines.extend(['','LLE detection uses finite-grid quality accounting, not a certificate of global equilibrium.'])
    for name,z in [('UD',r),('open630',c)]:
        lines.append(f"{name}: {z['rows']} common rows and {z['systems']} systems; row detection {z['row_gap_found_bounds']}; "
                     f"system detection {z['system_gap_found_bounds']}; unresolved {z['unresolved_rows']}; "
                     f"endpoint MAE {z.get('composition_MAE')} on {z['endpoint_rows']} checked endpoint rows.")
    lines.extend(['','Witnesses count as detections only. The positive LLE table supplies no false-positive rate or balanced accuracy.',
        'Open630 excludes six S1/S2 compounds by design. Open636 is a separate exploratory arm, not 636 Berny-converged profiles.',
        'The earlier 0.839 standalone UD IDAC result has 828 rows; it must not be compared as though it shared the 816-row open630 denominator.'])
    return '\n'.join(lines)+'\n'


def main():
    p=argparse.ArgumentParser();p.add_argument('--input',default='docs/astra/round5/data/scorecard_test.json');p.add_argument('--out',required=True)
    a=p.parse_args();d=json.loads(Path(a.input).read_text());text=render(d)
    target=Path(a.out)
    if target.exists():raise FileExistsError(target)
    target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
    write(str(target)+'.json',dict(source_sha256=sha(a.input),report_base=BASE,source_base=d.get('base'),comparisons=extract(d)))
    print(text)
if __name__=='__main__':main()
