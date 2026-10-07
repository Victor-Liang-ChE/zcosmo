"""Read the frozen P37 TEG call log. No chemistry imports, new gate, or native work."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import time
import unittest

BASE = '83cf52163d806ef0c92ba2002094832824122d59'
CALLS = 'docs/astra/round8/data/native/TEG-pcm_pruned.calls.json'
CALLS_BLOB = '1273d62de16736fd7138d8f80b9ee47393ac8e6d'
STEPS = (.016, .008, .004, .002, .001)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def number(value) -> float:
    require(type(value) in (int, float) and math.isfinite(value), 'Invalid number')
    return float(value)


def summarize(calls: list[dict]) -> dict:
    """Preserve call identities; the archived evaluator fixes the call order."""
    require(len(calls) == 22, 'Need both centers and all twenty displaced SCFs')
    for i, r in enumerate(calls):
        expected = 'strict' if i == 1 or i >= 12 else 'tight'
        require(type(r['index']) is int and r['index'] == i, 'Missing/reordered call')
        require(r['precision'] == expected and r['status'] == 'completed', 'Incomplete call')
        number(r['energy_Eh'])
        require(number(r['small_rho_cutoff']) == 0., 'Unexpected density pruning')
        for kind in ('XC', 'PCM'):
            node = r[kind]
            require(type(node['count']) is int and node['count'] > 0, 'Invalid node count')
            require(isinstance(node['signature'], str) and len(node['signature']) == 64,
                    'Missing membership signature')
        require(0 < number(r['PCM']['minimum_switch']) <= 1., 'Invalid switching minimum')
    # Geometry-only membership must match at the two electronic precisions.
    for i, j in [(0, 1)] + [(k, k + 10) for k in range(2, 12)]:
        for kind in ('XC', 'PCM'):
            require(calls[i][kind] == calls[j][kind], 'Precision changed node record')
    labels = {}
    rows = []
    for h, sign, index in [(0., 0, 1)] + [
            (h, sign, 12 + 2*k + (sign == -1))
            for k, h in enumerate(STEPS) for sign in (1, -1)]:
        r = calls[index]; n = r['PCM']; sig = n['signature']
        if sig not in labels:
            labels[sig] = chr(ord('A') + len(labels))
        rows.append(dict(index=index, h_Bohr=h, sign=sign, PCM_count=n['count'],
                         membership=labels[sig], minimum_retained_switch=n['minimum_switch'],
                         energy_Eh=r['energy_Eh']))
    central = [(calls[12+2*k]['energy_Eh'] - calls[13+2*k]['energy_Eh'])/(2*h)
               for k, h in enumerate(STEPS)]
    richardson = [(4*central[k+1]-central[k])/3 for k in range(4)]
    equal_count_different_ids = [r['index'] for r in rows[1:]
        if r['PCM_count'] == rows[0]['PCM_count'] and r['membership'] != rows[0]['membership']]
    minimum = min(r['minimum_retained_switch'] for r in rows)
    return dict(base=BASE, requested_SCF_records=22, strict_rows=rows,
        signature_labels={value: key for key, value in labels.items()},
        XC_memberships=len({r['XC']['signature'] for r in calls}),
        PCM_memberships=len(labels),
        equal_count_different_membership_indices=equal_count_different_ids,
        minimum_retained_switch=minimum,
        minimum_locations=[dict(h_Bohr=r['h_Bohr'], sign=r['sign'], index=r['index'])
                           for r in rows if r['minimum_retained_switch'] == minimum],
        central_strict=central, Richardson_strict=richardson,
        strict_positive_small_h_signature_constant=len({calls[i]['PCM']['signature']
                                                        for i in (14,16,18,20)}) == 1,
        changed_node_identity=None,
        interpretation='A minimum over retained nodes does not identify a removed node. '
                       'Hashes establish set changes, not a causal energy error.',
        scientific_verdict='P37 inconclusive, retained without re-gating',
        new_QC_evaluations=0, new_model_evaluations=0, native_budget_authorized=0)


def audit(path: Path) -> dict:
    raw = path.read_bytes()
    blob = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    require(blob == CALLS_BLOB, 'Input differs from the pinned archive; no automatic re-baselining')
    result = summarize(json.loads(raw))
    require(result['XC_memberships'] == 1 and result['PCM_memberships'] == 3,
            'Archived membership pattern changed')
    require(result['equal_count_different_membership_indices'] == [12],
            'Equal-count support change not reproduced')
    require(result['minimum_locations'] == [dict(h_Bohr=.016, sign=1, index=12)],
            'Minimum-switch location not reproduced')
    require(result['strict_positive_small_h_signature_constant'], 'Small-h support pattern changed')
    result.update(source_git_blob=blob, source_sha256=hashlib.sha256(raw).hexdigest())
    return result


def self_test() -> None:
    # Synthetic record-shape tests only. They do not simulate a molecule.
    fixture=[]
    for i in range(22):
        signature = 'a'*64 if i < 2 or i % 2 else ('b'*64 if i in (2,12) else 'c'*64)
        fixture.append(dict(index=i, precision='strict' if i==1 or i>=12 else 'tight',
            status='completed', energy_Eh=-1.+i*1e-6, small_rho_cutoff=0.,
            XC=dict(signature='x'*64,count=200),
            PCM=dict(signature=signature,count=99 if signature=='c'*64 else 100,
                     minimum_switch=1e-12)))
    class Tests(unittest.TestCase):
        def test_equal_count_is_not_equal_support(self):
            r=summarize(fixture)
            self.assertEqual(r['equal_count_different_membership_indices'], [12])
            self.assertIsNone(r['changed_node_identity'])
            self.assertEqual(r['new_QC_evaluations'], 0)
        def test_missing(self):
            with self.assertRaises(ValueError): summarize(fixture[:-1])
        def test_duplicate(self):
            q=copy.deepcopy(fixture); q[4]=q[3]
            with self.assertRaises(ValueError): summarize(q)
        def test_nonfinite(self):
            q=copy.deepcopy(fixture); q[4]['energy_Eh']=float('nan')
            with self.assertRaises(ValueError): summarize(q)
        def test_failed_call(self):
            q=copy.deepcopy(fixture); q[4]['status']='failed'
            with self.assertRaises(ValueError): summarize(q)
        def test_changed_precision_membership(self):
            q=copy.deepcopy(fixture); q[12]['PCM']['signature']='z'*64
            with self.assertRaises(ValueError): summarize(q)
    runner=unittest.TextTestRunner(verbosity=2)
    if not runner.run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests)).wasSuccessful():
        raise SystemExit(1)


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--calls', type=Path, default=Path(CALLS))
    p.add_argument('--out', type=Path)
    p.add_argument('--self-test', action='store_true')
    a=p.parse_args()
    if a.self_test:
        self_test(); return
    if a.out is None:
        p.error('--out is required unless --self-test is used')
    start=time.perf_counter(); result=audit(a.calls)
    result['audit_wall_s']=time.perf_counter()-start
    a.out.parent.mkdir(parents=True,exist_ok=True)
    # Exclusive creation prevents an audit from overwriting a historical result.
    with a.out.open('x') as f:
        json.dump(result,f,indent=2,allow_nan=False); f.write('\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
