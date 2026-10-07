Z-COSMO round 9: close the numerical campaign, clarify the archived node evidence

Reference: `main` at `83cf52163d806ef0c92ba2002094832824122d59`, rechecked before delivery. This review uses the round-9 prompt, the complete round-8 report, the registered R8 design and measured archive, and the current README. The supplied patches change reporting only. They do not reopen a native-computation budget. [S1–S5]

| Rank | ID | Pipeline / target | Class | Mechanism, cost and saving | Effort |
|---:|---|:---|:---:|---|---|
| 1 | P40 | README, Current evidence | E reporting | Add the R8 unresolved result and closed-budget status. Zero quantum or model calls; no solver speed-up claimed. | Very low |
| 2 | P39 | `scripts/r9_membership_audit.py` | E read-only audit | Replay the exact 22-record TEG call log. Distinguish equal counts from equal membership and locate the reported minimum. Zero new SCFs; avoids rerunning an experiment to answer an existing-data question. | Low |
| Record | REG9 | Proposed closeout note | Policy | Zero new native budget. Preserve every prior acceptance and failure. | Very low |
| Closed | Native diagnostics, chain rescue, 630-profile re-polish | No new protocol | No change | Do not repeat P37's 176 SCFs and 24 molecular gradients, or its 44 explicit PCM energies and four PCM gradients. Those counts describe avoided repetition, not a measured acceleration. | None |

These reporting tasks have deterministic, directly checkable outcomes and negligible compute cost. There is no speculative A optimization to rank. The old run used about 4,151 native worker-seconds; another run would spend compute without a demonstrated correction to test. No numerical probability of discovering a cause is invented. [S3]

Close the present numerical campaign. P37 adds information about why its test is inconclusive, but does not supply the independent causal evidence or demonstrated source correction needed to reopen native work. Its registration explicitly anticipated changing surface membership and prescribed an inconclusive verdict followed by closure. Treating that anticipated outcome as an automatic exception would remove the stopping rule. This recommendation leaves the mathematical source of the residual total-energy discrepancy unresolved. It does not declare the derivative correct. [S2, S3]

The source and the call log support a narrower account than “one node of weight 5.5e-13 caused the derivative collapse.” In pinned PySCF 2.14.0, SWIG uses the smoothstep polynomial H(t)=t³(10−15t+6t²), clipped outside [0,1]. It also sets t<1e-8 to zero before evaluating H. The total switching factor F is the product over neighboring atoms. A surface point is retained when wF>1e-16, where w is the angular weight. Thus F alone is neither the retention threshold nor an energy-error estimate. `get_D_S` sets the diagonal to ξ sqrt(2/π)/F; C-PCM uses this S as its linear-system matrix. Small F suppresses the associated charge rather than deleting an ordinary, fully weighted quadrature point. [U1]

The archive also contains a useful reporting correction. `pcm_nodes()` stores a membership hash and the minimum F over the retained set. It does not store the identity of the node attaining that minimum or an identity list for removed points. From that field alone, one cannot attach the minimum to the point that disappeared. [S4]

The zero-QC replay of the exact TEG PCM/pruned log gives the following strict-precision records. A, B and C denote different full membership hashes, not molecule labels. The two center SCFs and the corresponding tight-precision records have the same geometry-only node records. [S6]

| Displacement in Bohr | Positive-side nodes / membership | Negative-side nodes / membership | Minimum retained F, positive side | Strict central derivative, Eh/Bohr |
|---:|---|---|---:|---:|
| Center | 1340 / A | Same center | 1.1970e-12 | Not applicable |
| 0.016 | 1340 / B | 1340 / A | 5.5136e-13 | 2.3319931e-5 |
| 0.008 | 1339 / C | 1340 / A | 3.7335e-10 | 2.1535548e-5 |
| 0.004 | 1339 / C | 1340 / A | 5.2788e-10 | 2.0022441e-5 |
| 0.002 | 1339 / C | 1340 / A | 5.8142e-10 | 4.2518593e-6 |
| 0.001 | 1339 / C | 1340 / A | 6.0956e-10 | −2.9444891e-8 |

At +0.016 the count equals the center's, but the membership differs. Since the recorded membership is a set of unique owner/template identities, equal cardinality and unequal hashes imply exchanged identities, not unchanged support. At the smaller positive displacements, the same C membership recurs. The drop in the central derivative between h=0.004 and h=0.002 therefore does not coincide with a new sampled membership change between those positive-side evaluations. The negative-side membership remains A. This does not prove that support changes or continuous switching are harmless; it prevents attributing the collapse to the mere observation of one changed count. The minimum 5.5136e-13 occurs at +0.016, not at the smaller positive points with 1,339 retained nodes. [S6]

The registered result remains inconclusive. Its finest Richardson value is −1.4565463e-6 Eh/Bohr, its full-response discrepancy is 2.1633410e-5, and its uncertainty indicator is 4.5460247e-7. The membership condition fails despite the small indicator. Reclassifying it by ignoring that condition would be a new decision rule applied after seeing the outcome. P39 does not do that. [S7]

There is a theoretical reason to avoid either blaming or dismissing a tiny switching factor without additional information. At one fixed geometry and fixed AO density, write the C-PCM system as

\[
 S=\begin{pmatrix}B&b\\b^T&d\end{pmatrix},\qquad
 v=\binom{v_R}{v_j},\qquad d=a/F_j,
 \qquad a=\xi_j\sqrt{2/\pi}.
\]

The source energy is \(E=-\kappa v^TS^{-1}v/2\), with \(\kappa=(\epsilon-1)/\epsilon\). Assuming the indicated inverses exist, block elimination gives the exact difference between retaining this point and deleting it at that same geometry and density:

\[
 E_{\rm retain}-E_{\rm delete}
 =-\frac{\kappa}{2}
 \frac{(v_j-b^TB^{-1}v_R)^2}{a/F_j-b^TB^{-1}b}.
\]

For bounded couplings and a nonsingular retained block, this tends to zero proportionally to F_j. That is a limiting argument, not a numerical bound for TEG. A finite-cutoff error depends on the potential and the Schur complement, and a derivative also involves their geometry dependence. A count and a minimum switching factor do not supply those quantities. Nor does this fixed-geometry deletion formula equal the energy difference between opposite displaced molecular geometries. The algebra follows directly from the source's C-PCM quadratic energy; no new molecular result is asserted. [U1]

The explicit PCM partial provides another important constraint. With the same moving basis and fixed AO density coefficients, the TEG layer's directional error is 3.1151e-14 Eh/Bohr, while its formal verdict is still inconclusive because membership changes. Stock and cached energies agree within 6.87e-16 Eh. Thus the archived support change coexists with excellent agreement for the explicit PCM partial on that density. This weakens the claim that the observed support event, by itself, demonstrates a faulty PCM derivative. It does not validate the complete self-consistent energy gradient or establish an error bound after density relaxation. The EG layer has a consistent verdict and an error of 2.7446e-13. [S8, S9]

I found no demonstrated source-level correction in these records. Lowering the retention cutoff, forcing a common point set, changing angular pruning or choosing a different finite-difference step would each be a new intervention without an identified, validated fix. Equal XC membership does not certify every integral-screening or SCF detail either. P37's other arms remain under their original inconclusive assessments, and their apparently smaller errors cannot be selected as evidence of a remedy. [S2–S4]

The README's Current evidence section is accurate in its substantive claims. It distinguishes original Berny convergence from full-energy stationarity, records P32's failed compatibility gate, and keeps displacement sensitivity separate from geometry error. Its Z0x and benchmark statements remain appropriately scoped, including the explicit P28 enable flag and separate LLE denominators. The omission is chronological: it links through R7 without recording the completed R8 closure. P40 adds two lines and leaves the existing claims intact. It does not say that P37 proved a PCM bug or made the earlier P33 result disappear. [S3, S5]

Nothing further native is warranted within this campaign, even under a one-job ceiling. There is no proposed re-polish or six-chain attempt. P39 answers the remaining bookkeeping question from bytes already in the archive; it is not a new experiment about the accuracy of the 630 profiles. A future reopening would need distinct evidence that isolates a specific error, such as an independently checked source correction with a reproducer, rather than another reading of these same inconclusive ladders. The existing profile-version and glycol qualifications remain. [S2]

P39's exactness argument is simple: it never imports chemistry code, evaluates a model or modifies an input. It checks the frozen Git blob before computing differences from the archived energies. The assertions concern faithful transcription and membership accounting, not new physical acceptance criteria. It preserves all 22 identities and refuses missing, duplicated or nonfinite records. P40 edits documentation only. Both are E reporting changes; the original E profile/affinity tolerances are neither relaxed nor reinterpreted.

Executed in this review: the actual 22-record TEG log was reconstructed from the connector's contents and verified byte-for-byte against Git blob `1273d62de16736fd7138d8f80b9ee47393ac8e6d` before replay. Its central differences and Richardson values reproduce the archived result. The README base and complete attached R8 report also match their repository Git blobs. The R8 diagnostic/common helpers and reused factories match the plan's SHA256 source fingerprints. Six new standard-library tests pass; the ten archived portable R8 tests also pass. These include mock orchestration and do not constitute native validation. Independent and combined patch-application checks passed against the verified reconstruction. The exact archive-replay and README-check commands passed. Additional checks rejected a modified input and refused to overwrite an existing output. The initial real-main checkout guard and repository commit command are supplied for the maintainer, not represented as executed against a full clone here.

Not executed: PySCF or pyberny, any new SCF, any model score, a Mac-only UD gate, an Actions dispatch or a production modification. PySCF and pyberny are absent from this runtime; no installation was attempted because this review authorizes zero native work. The local files used for replay and patch checks are a verified reconstruction of the relevant subset, not a full repository clone. The aggregate eight-job outcomes above are the maintainer's archived results, not eight calculations rerun here.

The following are independent unified diffs against the pinned main. The registration block is proposed text, not an assertion that it has been committed. No change is made to the archived R8 result or its decision.

<!-- BEGIN PATCH P39 -->
```diff
diff --git a/scripts/r9_membership_audit.py b/scripts/r9_membership_audit.py
new file mode 100644
--- /dev/null
+++ b/scripts/r9_membership_audit.py
@@ -0,0 +1,153 @@
+"""Read the frozen P37 TEG call log. No chemistry imports, new gate, or native work."""
+from __future__ import annotations
+import argparse
+import copy
+import hashlib
+import json
+import math
+from pathlib import Path
+import time
+import unittest
+
+BASE = '83cf52163d806ef0c92ba2002094832824122d59'
+CALLS = 'docs/astra/round8/data/native/TEG-pcm_pruned.calls.json'
+CALLS_BLOB = '1273d62de16736fd7138d8f80b9ee47393ac8e6d'
+STEPS = (.016, .008, .004, .002, .001)
+
+
+def require(condition: bool, message: str) -> None:
+    if not condition:
+        raise ValueError(message)
+
+
+def number(value) -> float:
+    require(type(value) in (int, float) and math.isfinite(value), 'Invalid number')
+    return float(value)
+
+
+def summarize(calls: list[dict]) -> dict:
+    """Preserve call identities; the archived evaluator fixes the call order."""
+    require(len(calls) == 22, 'Need both centers and all twenty displaced SCFs')
+    for i, r in enumerate(calls):
+        expected = 'strict' if i == 1 or i >= 12 else 'tight'
+        require(type(r['index']) is int and r['index'] == i, 'Missing/reordered call')
+        require(r['precision'] == expected and r['status'] == 'completed', 'Incomplete call')
+        number(r['energy_Eh'])
+        require(number(r['small_rho_cutoff']) == 0., 'Unexpected density pruning')
+        for kind in ('XC', 'PCM'):
+            node = r[kind]
+            require(type(node['count']) is int and node['count'] > 0, 'Invalid node count')
+            require(isinstance(node['signature'], str) and len(node['signature']) == 64,
+                    'Missing membership signature')
+        require(0 < number(r['PCM']['minimum_switch']) <= 1., 'Invalid switching minimum')
+    # Geometry-only membership must match at the two electronic precisions.
+    for i, j in [(0, 1)] + [(k, k + 10) for k in range(2, 12)]:
+        for kind in ('XC', 'PCM'):
+            require(calls[i][kind] == calls[j][kind], 'Precision changed node record')
+    labels = {}
+    rows = []
+    for h, sign, index in [(0., 0, 1)] + [
+            (h, sign, 12 + 2*k + (sign == -1))
+            for k, h in enumerate(STEPS) for sign in (1, -1)]:
+        r = calls[index]; n = r['PCM']; sig = n['signature']
+        if sig not in labels:
+            labels[sig] = chr(ord('A') + len(labels))
+        rows.append(dict(index=index, h_Bohr=h, sign=sign, PCM_count=n['count'],
+                         membership=labels[sig], minimum_retained_switch=n['minimum_switch'],
+                         energy_Eh=r['energy_Eh']))
+    central = [(calls[12+2*k]['energy_Eh'] - calls[13+2*k]['energy_Eh'])/(2*h)
+               for k, h in enumerate(STEPS)]
+    richardson = [(4*central[k+1]-central[k])/3 for k in range(4)]
+    equal_count_different_ids = [r['index'] for r in rows[1:]
+        if r['PCM_count'] == rows[0]['PCM_count'] and r['membership'] != rows[0]['membership']]
+    minimum = min(r['minimum_retained_switch'] for r in rows)
+    return dict(base=BASE, requested_SCF_records=22, strict_rows=rows,
+        signature_labels={value: key for key, value in labels.items()},
+        XC_memberships=len({r['XC']['signature'] for r in calls}),
+        PCM_memberships=len(labels),
+        equal_count_different_membership_indices=equal_count_different_ids,
+        minimum_retained_switch=minimum,
+        minimum_locations=[dict(h_Bohr=r['h_Bohr'], sign=r['sign'], index=r['index'])
+                           for r in rows if r['minimum_retained_switch'] == minimum],
+        central_strict=central, Richardson_strict=richardson,
+        strict_positive_small_h_signature_constant=len({calls[i]['PCM']['signature']
+                                                        for i in (14,16,18,20)}) == 1,
+        changed_node_identity=None,
+        interpretation='A minimum over retained nodes does not identify a removed node. '
+                       'Hashes establish set changes, not a causal energy error.',
+        scientific_verdict='P37 inconclusive, retained without re-gating',
+        new_QC_evaluations=0, new_model_evaluations=0, native_budget_authorized=0)
+
+
+def audit(path: Path) -> dict:
+    raw = path.read_bytes()
+    blob = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
+    require(blob == CALLS_BLOB, 'Input differs from the pinned archive; no automatic re-baselining')
+    result = summarize(json.loads(raw))
+    require(result['XC_memberships'] == 1 and result['PCM_memberships'] == 3,
+            'Archived membership pattern changed')
+    require(result['equal_count_different_membership_indices'] == [12],
+            'Equal-count support change not reproduced')
+    require(result['minimum_locations'] == [dict(h_Bohr=.016, sign=1, index=12)],
+            'Minimum-switch location not reproduced')
+    require(result['strict_positive_small_h_signature_constant'], 'Small-h support pattern changed')
+    result.update(source_git_blob=blob, source_sha256=hashlib.sha256(raw).hexdigest())
+    return result
+
+
+def self_test() -> None:
+    # Synthetic record-shape tests only. They do not simulate a molecule.
+    fixture=[]
+    for i in range(22):
+        signature = 'a'*64 if i < 2 or i % 2 else ('b'*64 if i in (2,12) else 'c'*64)
+        fixture.append(dict(index=i, precision='strict' if i==1 or i>=12 else 'tight',
+            status='completed', energy_Eh=-1.+i*1e-6, small_rho_cutoff=0.,
+            XC=dict(signature='x'*64,count=200),
+            PCM=dict(signature=signature,count=99 if signature=='c'*64 else 100,
+                     minimum_switch=1e-12)))
+    class Tests(unittest.TestCase):
+        def test_equal_count_is_not_equal_support(self):
+            r=summarize(fixture)
+            self.assertEqual(r['equal_count_different_membership_indices'], [12])
+            self.assertIsNone(r['changed_node_identity'])
+            self.assertEqual(r['new_QC_evaluations'], 0)
+        def test_missing(self):
+            with self.assertRaises(ValueError): summarize(fixture[:-1])
+        def test_duplicate(self):
+            q=copy.deepcopy(fixture); q[4]=q[3]
+            with self.assertRaises(ValueError): summarize(q)
+        def test_nonfinite(self):
+            q=copy.deepcopy(fixture); q[4]['energy_Eh']=float('nan')
+            with self.assertRaises(ValueError): summarize(q)
+        def test_failed_call(self):
+            q=copy.deepcopy(fixture); q[4]['status']='failed'
+            with self.assertRaises(ValueError): summarize(q)
+        def test_changed_precision_membership(self):
+            q=copy.deepcopy(fixture); q[12]['PCM']['signature']='z'*64
+            with self.assertRaises(ValueError): summarize(q)
+    runner=unittest.TextTestRunner(verbosity=2)
+    if not runner.run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests)).wasSuccessful():
+        raise SystemExit(1)
+
+
+def main() -> None:
+    p=argparse.ArgumentParser(description=__doc__)
+    p.add_argument('--calls', type=Path, default=Path(CALLS))
+    p.add_argument('--out', type=Path)
+    p.add_argument('--self-test', action='store_true')
+    a=p.parse_args()
+    if a.self_test:
+        self_test(); return
+    if a.out is None:
+        p.error('--out is required unless --self-test is used')
+    start=time.perf_counter(); result=audit(a.calls)
+    result['audit_wall_s']=time.perf_counter()-start
+    a.out.parent.mkdir(parents=True,exist_ok=True)
+    # Exclusive creation prevents an audit from overwriting a historical result.
+    with a.out.open('x') as f:
+        json.dump(result,f,indent=2,allow_nan=False); f.write('\n')
+    print(json.dumps(result,indent=2))
+
+
+if __name__ == '__main__':
+    main()
```
<!-- END PATCH P39 -->

<!-- BEGIN PATCH P40 -->
```diff
diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -48,5 +48,7 @@
 comparisons favor UD over open profiles for IDAC and excess enthalpy; the VLE
 interval includes zero. LLE detection and checked endpoint compositions have
 separate denominators and are not global phase-equilibrium certificates.
+The [round-8 stage-isolation test](docs/astra/round8/RESULTS.md) left the TEG
+energy-gradient mismatch unresolved; its numerical diagnostic budget is closed.
 See [round-7 evidence](docs/astra/round7/RESULTS.md) and
 [endpoint acceptance](docs/astra/round6/RESULTS.md).
```
<!-- END PATCH P40 -->

<!-- BEGIN PATCH REG9 -->
```diff
diff --git a/docs/astra/round9/REGISTRATION_PROPOSED.md b/docs/astra/round9/REGISTRATION_PROPOSED.md
new file mode 100644
--- /dev/null
+++ b/docs/astra/round9/REGISTRATION_PROPOSED.md
@@ -0,0 +1,23 @@
+Round-9 proposed closeout record. Record adoption with the actual commit ID.
+Reference main: 83cf52163d806ef0c92ba2002094832824122d59.
+
+P39 is an E, zero-QC replay of the existing P37 TEG PCM/pruned call log.
+It checks the exact archived Git blob and preserves all 22 call identities.
+It reports node counts separately from membership hashes and identifies the
+location of the minimum over retained switching weights. It does not identify
+a removed node from a minimum, change a referee verdict, recompute a model,
+or create a new scientific acceptance gate. Prior read-only analysis of this
+archive is explicitly retrospective, not a preregistered discovery.
+
+P40 appends the R8 unresolved-mismatch and closed-budget status to the README.
+No historical registration, result, source profile, or model default is edited.
+P32 remains failed. P30/P33/P37 outcomes keep their original qualifications.
+P20/P28 keep their existing scoped acceptance. The 630 original-gradient
+profiles and six S1/S2 profiles remain unchanged. P35 stays unresolved.
+
+The R9 native budget is zero: no Actions dispatch, new SCF, geometry re-polish,
+chain retry, profile generation, or experimental scoring. P37's observed
+membership changes are not, on their own, independent validation of a source
+correction. Further native work requires distinct evidence that isolates a
+specific error and a separate prospective authorization. This note creates
+no automatic continuation and does not reopen the R8 budget.
```
<!-- END PATCH REG9 -->

Apply and check the reporting-only changes from a clean checkout at the pinned commit:

```bash
set -euo pipefail
BASE=83cf52163d806ef0c92ba2002094832824122d59
test "$(git rev-parse HEAD)" = "$BASE"
test -z "$(git status --porcelain)"
export REPORT="${REPORT:-$HOME/Downloads/ZCOSMO_ROUND9_REPORT.md}"
export PATCH_DIR="$(mktemp -d)"
python - <<'PYEXTRACT'
import os,re
from pathlib import Path
text=Path(os.environ['REPORT']).read_text()
blocks=re.findall(r'<!-- BEGIN PATCH (\w+) -->\n```diff\n(.*?)```\n<!-- END PATCH \1 -->',text,re.S)
assert [name for name,_ in blocks]==['P39','P40','REG9']
for name,body in blocks:
    (Path(os.environ['PATCH_DIR'])/(name+'.patch')).write_text(body)
PYEXTRACT
for id in P39 P40 REG9; do
    git apply --check "$PATCH_DIR/$id.patch"
    git apply "$PATCH_DIR/$id.patch"
done
python -m py_compile scripts/r9_membership_audit.py
python scripts/r9_membership_audit.py --self-test
# Record adoption before using the new reporting output; no native job is registered.
printf '\n\n' >> PREREGISTRATION.md
cat docs/astra/round9/REGISTRATION_PROPOSED.md >> PREREGISTRATION.md
git add scripts/r9_membership_audit.py README.md PREREGISTRATION.md \
  docs/astra/round9/REGISTRATION_PROPOSED.md
git diff --cached --check
git commit -m "Record R9 zero-QC archive clarification and R8 closure"
```

P39's benchmark and check run on any ordinary Python installation, including the Mac or a local checkout. They use no UD assets. Use a new output path; an existing file is deliberately not overwritten.

```bash
python scripts/r9_membership_audit.py \
  --calls docs/astra/round8/data/native/TEG-pcm_pruned.calls.json \
  --out results/r9/membership-audit.json
python - <<'PYCHECK'
import json
r=json.load(open('results/r9/membership-audit.json'))
assert r['source_git_blob']=='1273d62de16736fd7138d8f80b9ee47393ac8e6d'
assert r['requested_SCF_records']==22
assert r['XC_memberships']==1 and r['PCM_memberships']==3
assert r['equal_count_different_membership_indices']==[12]
assert r['minimum_locations']==[{'h_Bohr':.016,'sign':1,'index':12}]
assert r['strict_positive_small_h_signature_constant']
assert r['changed_node_identity'] is None
assert r['native_budget_authorized']==0
assert abs(r['Richardson_strict'][-1]-(-1.456546290986201e-6))<1e-18
print('Archived node bookkeeping reproduced; P37 remains inconclusive.')
print('Read/parse/arithmetic seconds:',r['audit_wall_s'])
PYCHECK
```

P40's check is textual and does not require regenerating the scorecard:

```bash
python - <<'PYREADME'
from pathlib import Path
r=Path('README.md').read_text()
assert 'The [round-8 stage-isolation test](docs/astra/round8/RESULTS.md) left the TEG\n' in r
assert 'energy-gradient mismatch unresolved; its numerical diagnostic budget is closed.' in r
assert 'ZC_R6_ENDPOINT=1' in r
assert 'The corrected-gradient calibration failed its preregistered compatibility gate;' in r
print('README retains previous qualifications and records R8 closure.')
PYREADME
```

Do not dispatch `r8_review.yml` again as part of these commands. The 630 primary profiles and six flagged profiles receive no writes.

Source key, with repository paths resolved at the pinned commit unless stated otherwise:

| Key | Source |
|---|---|
| S1 | `docs/astra/ROUND9_PROMPT.md`; `docs/OPTIMIZATION_BRIEF.md` |
| S2 | `PREREGISTRATION.md`, R8 registration and results entry; original decisions are retained |
| S3 | `docs/astra/round8/RESULTS.md`; `docs/astra/round8/data/p37_diagnostic.json` |
| S4 | `scripts/r8_diagnostic.py`, especially `pcm_nodes`, `native`, `pcm_layer_check`, `collect`; `scripts/r8_common.py`; `cloud/r8/diagnostic/plan.json`; `.github/workflows/r8_review.yml` |
| S5 | `README.md`, Current evidence; original blob `0169e5da6bb52bc8d09b4dc753955e9122603003`; `src/zcosmo/z0x.py`, `_endpoint` and `lngamma` |
| S6 | `docs/astra/round8/data/native/TEG-pcm_pruned.calls.json`, all 22 records; exact blob verified locally |
| S7 | `docs/astra/round8/data/native/TEG-pcm_pruned.result.json` |
| S8 | `docs/astra/round8/data/native/TEG-pcm_pruned.layer.json` |
| S9 | `docs/astra/round8/data/p37_diagnostic.json`, EG PCM/pruned layer record |
| S10 | `docs/astra/round8/ZCOSMO_ROUND8_REPORT.md`, complete report blob `2381bbe01dacc512f2d78b1441607b116d038aa0`; `scripts/r8_evidence.py` and `scripts/r8_selftest.py` |
| U1 | PySCF `v2.14.0`, `pyscf/solvent/pcm.py`, `switch_h`, `gen_surface`, `get_D_S`, `PCM.build`, `PCM._get_vind`; primary source: `https://raw.githubusercontent.com/pyscf/pyscf/v2.14.0/pyscf/solvent/pcm.py` |

The campaign closes with the total-energy derivative mismatch unresolved. The original decisions and profile versions remain unchanged.
