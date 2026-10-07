# Z-COSMO round 8: freeze the profile version and isolate the remaining derivative mismatch

Reference: `Victor-Liang-ChE/zcosmo`, `main = 58cc629df42156c0b7862710057318db0a495dbb`. The five extractable patches below target this snapshot. P32 remains failed, its pilot and chain stages remain unrun, and no production calculation is changed by these patches. [S1–S4]

| Rank | ID | Pipeline / target | Class | Expected speed-up or compute arithmetic | Effort |
|---:|---|---|:---:|---|---|
| 1 | P36 | Read-only R7 evidence and denominator audit, `scripts/r8_evidence.py` | E | Zero quantum or model evaluations. Reuse the completed calibration instead of repeating its `2635.74 + 2986.17 = 5621.91 s` of worker time. This is avoided repetition, not a faster solver. | Low |
| 2 | P38 | Append the closing evidence statement to `README.md` | E reporting | Zero model evaluations. Keep accepted numerical corrections separate from unaccepted geometry protocols. | Low |
| 3 | P37 | One final derivative-stage experiment, `scripts/r8_diagnostic.py` and `r8_review.yml` | A diagnostic; E cache/stock parity control | Eight one-hour four-core native jobs. At most 176 SCFs and 24 molecular gradients, plus 44 explicit PCM energies and four PCM gradients. The SCF ceiling is 57.1% below a repeat of the five-case, 410-SCF P33 design, although the experiments have different scope and unpruned calls can cost more. No wall-time speed-up is claimed. | Moderate |
| Shared | H8 | Common checks and portable tests | E instrumentation | No native work. Required by P36/P37. | Low |
| Shared | REG8 | Proposed prospective registration | Policy, not a model | No computation or adoption by itself. | Low |
| Not authorized | Six chains / 630-profile re-polish | Existing primary and S1/S2 collections | No new protocol | Zero optimization budget in this round. | None |

The rank follows avoided work and confidence that the result is useful per implementation effort. Bookkeeping and an accurate public status have known value and no new quantum cost. P37 has uncertain diagnostic yield, so it comes last and has a hard stopping rule. There is no measured probability from which to construct a credible numerical saving-times-probability score. The call-count comparison is a budget comparison, not a prediction of hardware throughput.

## Decisions and the limits of the evidence

**Keep the six chains flagged. Do not launch a corrected-gradient re-polish of all 630 profiles yet. Run at most the fixed P37 diagnostic, if its new registration is adopted.** Its purpose is to locate a remaining numerical inconsistency, not to obtain permission for a previously rejected rollout.

P32's actual maximum COSMO-SAC-dsp change was `0.012074145054630225`, exceeding the original `0.01` gate by `0.002074145054630225`. Its median change was `0.00016563140277092714`; the median difference from UD was `0.13639218459184735`. Both arms converged all 25 calibration targets. Their masks matched, with 2,271 finite dsp and 2,302 finite Z0x occurrences, and the measured worker-time ratio was `1.1329537736908066`. Those are useful positive findings, but they do not change the failed maximum criterion. [S2, S4]

A change of 0.01207 in ln gamma is small in ordinary physical terms. Backward compatibility and correctness of a derivative are nevertheless different questions. P32 did not establish that full-response gradients are scientifically inferior. It established that this particular replacement did not satisfy its predeclared equivalence requirement. Removing the offending observation or changing the maximum test into a median test would not preserve that requirement. The archived gate contains extrema rather than per-query values; P36 therefore does not manufacture an independently verified count or identity of over-limit queries from that JSON. [S1, S4]

The amendments P34a and P33a do not provide a precedent for changing P32's scientific gate after observing it. P34a accepted documented legacy provenance where a newer Boolean field did not yet exist, before the screen ran. P33a normalized equivalent representations of the pinned RDKit version before any referee SCF ran. Their exact source changes are retained. Neither amendment excused an observed failure of a numerical acceptance criterion. [S3]

The defensible future route for a chain is a genuinely new, versioned geometry protocol whose numerical target has independently been validated. It could ask whether that protocol converges under a fixed budget and supplies scientifically interpretable geometries, rather than whether it reproduces an old approximate-gradient input within 0.01. That would require a separate scientific rationale and registration. It would not retroactively accept P32. At present, one sampled full-response direction remains inconsistent and most directions remain unresolved. There is no justification here for bypassing those facts to run the six chains. [S2, S3]

P33 supports a narrower conclusion than “the cause of every stall is solved.” Under its finite-resolution rule, adding grid response corrected three sampled directional discrepancies. The controlled optimization intervention was never run on the P26-censored pilot after the calibration failed. Thus the evidence separates a demonstrated missing derivative contribution from an untested claim that restoring it will cure every historical Berny stall. P37 does not perform that unrun optimization. [S2, S3, S6]

## Why P34 does not authorize 630 re-optimizations

P34 recorded 39 completed native cases from 40 selected cases. All 39 had an off/full Cartesian force difference above `1e-5 Eh/Bohr`. Of the affinity assessments, 35 were screen-positive and four had changed finite coverage. One native case did not reach a final result. There are no negative screens, but there is also no complete probability-sample result from which this report would infer a population bound. The fixed sentinels remain descriptive evidence. [S2, S5]

That is sufficient to withdraw an unqualified claim of stationarity for the discretized full-response energy. It does not demonstrate that every saved geometry is displaced by 0.01 Å from a corrected minimum, or that every saved prediction has the measured stress error.

Write the prediction as `L(R)` and the full-response energy as `E(R)`. P34 measured changes of the form

\[
L(R+s v)-L(R),\qquad \max_a\lVert s v_a\rVert=0.01\ \mathrm{\AA}.
\]

The quantity needed for a geometry-error claim is `L(R*) - L(R)`, where `R*` is a relevant corrected stationary geometry. No stress experiment located `R*`. Moreover, P34's maximum-atom displacement convention is different from P33's unit-L2 directional convention; their scalar thresholds cannot be interchanged.

A displacement bound would require additional information. For example, after removing rigid motions, a positive lower curvature bound `H >= m I` on a suitable region can give `||R-R*|| <= ||grad E(R)||/m`. No such lower bound was established. Soft torsions make precisely this inference difficult. Even the elementary family `E(q)=k(q-a)^2/2` illustrates the problem: a force at `q=0` fixes the product `ka`, not the displacement `a`. A steep profile response to an imposed displacement adds no missing curvature information.

The existing files should therefore be described as **630 geometries satisfying the original Berny predicate with the declared original gradient approximation**, with full-energy stationarity unverified. Preserve their actual provenance, including the legacy strings accepted by P34a. Do not erase a historical convergence result, and do not relabel it as convergence under a different derivative. Their benchmark performance remains empirical evidence about that frozen input version. [S2, S3]

A full re-polish now would spend substantial compute on a derivative whose remaining mismatch is not yet isolated. It would also mix two questions: whether the geometry protocol is numerically consistent and how much a different input version changes predictions. No 630-molecule campaign or new compatibility limit is registered here. A later source-level correction, with independent directional verification and a separately versioned protocol, could justify such a campaign. P37's outcome alone is not that authorization.

## P37: one final stage-isolation diagnostic

Targets: `plan`, `native`, `pcm_layer_check` and `collect` in `scripts/r8_diagnostic.py`. The existing production functions are called but not patched.

The unresolved P33 result is worth one targeted diagnostic because it admits useful stage controls at fixed coordinates. It does not justify another optimizer comparison or a broad grid sweep. Freeze the exact archived TEG `bond-3-4` unit-L2 direction that was resolved inconsistent and the EG `bond-2-3` direction that was consistent. The planner takes their existing vectors and geometry hashes from the committed P33 files. These cases are deliberately chosen mechanism controls, not a probability sample or an experimental holdout. [S2, S6, S7]

A source-level distinction matters before blaming pruning. In pinned PySCF 2.14.0, the executable `small_rho_cutoff` default is **zero**, although its docstring still describes `1e-7`. Density-based point removal occurs only when the actual cutoff enables it. Angular pruning is a different setting, `mf.grids.prune`. The full-response path regenerates quadrature through `grids_response_cc`, using the selected atomic-grid construction. A nonzero runtime density cutoff would require investigation; it must not be assumed from the stale docstring. P37 requires the runtime value to be zero and records it. [U1, U2, U3]

Ordinary angular pruning chooses the angular rule on atomic radial shells. Removing it is a resolution intervention, not evidence that geometry-dependent point deletion caused the original discrepancy. The experiment holds grid level 2 fixed and compares the following arms at each archived geometry:

| Arm | Solvent calculation | Angular pruning | Density-based point removal |
|---|---|---|---|
| `pcm_pruned` | Existing C-PCM conductor, project radii, Lebedev 17 | Existing default | Runtime cutoff must be zero |
| `pcm_unpruned` | Same C-PCM definition | `None` | Same requirement |
| `vacuum_pruned` | PCM detached; same nuclear geometry | Existing default | Same requirement |
| `vacuum_unpruned` | PCM detached; same nuclear geometry | `None` | Same requirement |

All arms retain BP86/def2-SVP and density fitting. The two centers use the existing P33 tight and strict SCF settings, `(1e-11, 1e-7)` and `(1e-12, 1e-8)` for energy/orbital-gradient tolerances. At the centers compute tight/full, strict/full and strict/off gradients. Auxiliary-basis response is required. PCM response is retained in the PCM arms. No optimizer, profile generator or ThermoML evaluator is called.

Each arm computes the complete `±0.016, ±0.008, ±0.004, ±0.002, ±0.001 Bohr` energy ladder at both precisions. The reference remains the finest Richardson estimate. P33's `tau=1e-5 Eh/Bohr`, stabilization requirement and `tau/4` indicator ceiling remain unchanged. A noisier estimate cannot pass through a wider tolerance. Scientific outcomes are consistent, inconsistent or inconclusive, distinct from failed execution. The assessment remains empirical, not an interval certificate. [S3, S8]

The new bookkeeping replaces a point-count-only warning with retained-node identities: generating atom plus atomic-template ordinal for XC, and generating atom plus Lebedev ordinal for PCM. Reordering identical nodes does not count as a topology change. At the centers the SCF and full-response quadratures must also have matching membership and weights. A discrepancy or a membership change makes the derivative assessment inconclusive. These checks do not claim to inspect every AO/integral screening decision. [U2, U3]

### The explicit PCM partial derivative

The two `pcm_pruned` jobs also test a different mathematical object from the total SCF derivative. Let `P0` be the converged center AO density coefficient matrix. Keep its numerical entries fixed while moving the atom-centered basis and rebuilding the surface. Solve surface charges anew. Then compare

\[
\frac{d}{dt}E_{\mathrm{PCM}}(R+t v,P_0)
\quad\text{with}\quad
v\mathbin{:}\operatorname{PCM.grad}(P_0).
\]

This is a derivative at fixed **AO coefficients**, not at fixed real-space electron density. The off-center value of `Tr(P0 S(R))` can change and is recorded without renormalization. It is also different from differentiating the PCM energy component along a relaxed SCF solution `P(R)`, which would introduce a density-response term. A naive split of relaxed SCF energies into components would confound that term with an explicit PCM derivative error. The pinned API includes nuclear, charge-potential and surface-solver derivatives in `PCM.grad(dm)`. [U4, U5]

For C-PCM at fixed dielectric factor `f`, with symmetric surface matrix `K`,

\[
q=-f K^{-1}v_s,\qquad
E_{\mathrm{PCM}}=-\frac f2 v_s^T K^{-1}v_s.
\]

Consequently, writing `z=K^{-1}v_s`, the explicit directional derivative is

\[
E'_{\mathrm{PCM}}=-f(v_s')^Tz+\frac f2 z^TK'z.
\]

Both the moving AO functions in `v_s'` and the surface change in `K'` belong to this test. The portable matrix test below verifies this algebra; it does not validate native molecular integrals.

Use stock `PCM` and the current `CachedPCM3c` independently at the center and ten displaced geometries. This tests the cache as well as the layer derivative without changing the production cache. Record the linear residual and retained surface identity. Cache/stock parity requires energy differences below `1e-9 Eh` and gradient-component differences below `1e-8 Eh/Bohr`. Both implementations are float64 and share upstream derivative code; their agreement is not an independent high-precision proof. The layer FD assessment explicitly retains that limitation. [S9, U4, U5]

### Interpretation and stopping rule

Before calling an intervention a removal of the old discrepancy, the pruned PCM baseline must reproduce the TEG inconsistency and EG consistency under the unchanged criterion. Failure to reproduce changes the conclusion to a reproducibility problem, not a successful fix.

If changing angular pruning removes a resolved mismatch, that establishes a dependence on that quadrature choice at the tested coordinates. It does not show that a whole new profile version is more accurate. A PCM/vacuum contrast alone cannot isolate an additive solvent error because the converged electron density also changes.

A resolved failure of the explicit PCM partial derivative, with stock/cache parity and stable membership, localizes a problem to that partial calculation. It still does not identify a particular SWIG term without further evidence. Conversely, a passing layer and failing total derivative leaves other derivative terms, SCF response or screening among the possibilities. Equal counts alone would not have made these distinctions. PCM's switching and retained-support tests are plausible places to inspect, not established causes of the remaining mismatch. [U4, U5]

There is no automatic escalation. Missing jobs remain missing. Inconclusive ladders remain inconclusive. After these eight jobs, archive the resolved contrasts or close the mismatch as unresolved. Do not select another step, grid or molecule until a separately justified registration exists. Neither an encouraging diagnostic nor an all-consistent result grants a chain retry or a 630-profile re-polish.

The native ceiling is `2 cases × 4 arms × 3600 s = 8 four-core worker-hours`, or 32 allocated core-hours. The internal per-job deadline is 3,400 s to leave time for failure recording. Counts are `8 × 22 = 176` SCFs and `8 × 3 = 24` molecular gradients, plus `2 × 22 = 44` explicit PCM energies and four PCM gradients. The layer work is inside the same wall cap. Installation and artifact transfer are outside this native count. Free-account quota and actual memory fit are not guaranteed. No paid fallback or automatic retry is requested.

## Bugs, wasted work and reporting corrections

The existing `r7_screen.run_case` discards the execution record returned by `bounded`. A child failure can therefore leave the wrapper returning successfully. The R8 runner checks the child record and native terminal status and returns nonzero for operational failure. This is fixed for the new experiment only; the frozen R7 helpers are not edited. A scientifically negative diagnostic may still complete successfully, so a green job never substitutes for reading its assessment. [S8]

A point count is weaker than point identity. P33 already warned about that limitation; P37 records owner/template membership and checks the actual response quadrature. The stale PySCF docstring is another reason to record runtime settings rather than infer active density pruning from documentation. [S3, U1–U3]

The P34 missing native member and four affinity coverage changes are not permission to remove those cases from a population claim. P36 preserves their requested denominator. Likewise, P32's aggregate extrema do not provide a row-level count of compatibility failures. [S4, S5]

P28 is accepted numerically, but current `z0x.py` still defaults `ZC_R6_ENDPOINT` to zero. The README patch explicitly tells users how the accepted endpoint is enabled. Historical finite-difference-endpoint scorecards must remain labelled; this report neither flips the default nor silently re-scores them. [S10]

## Execution record

Executed here: Git-blob checks of the complete archived R7 report, the amended `r7_referee.py` and `r7_screen.py`, the reused `r7_common.py`, the R7 workflow and the README patch base; independent and combined patch-application checks; Python syntax and workflow-shell checks; and the delivered portable suite. The suite contains ten passing tests. Its polynomial FD error is `8.99e-12`; its toy PCM matrix-derivative error is `4.14e-13`. Mock execution checks exercised all 22 SCF calls, the 22-energy/two-gradient layer budget, operational failures, deadline claims, missing-result retention and duplicate rejection.

Not executed: native PySCF, the real P37 experiment, a full local run of P36 against the complete real R7 archive, any Mac-only UD calculation, any optimizer or a production profile change. The source archive and relevant data were read through GitHub; this runtime did not obtain a full repository checkout. Local runtime source reconstruction is not being represented as a clone.

The attempted pinned PySCF installation failed at package resolution with “No matching distribution found for pyscf==2.14.0”; PySCF and pyberny are absent from this Python 3.13 runtime. This does not establish that the registered releases are unavailable in the working Python 3.11 environments. Native claims remain source-checked hypotheses until the supplied commands run. Mock SCF and matrix tests are not molecular validation.

## Apply and check

The five blocks below are independent unified diffs against the reference. Apply all five before running the shared test suite; H8's tests import P36/P37. No old R7 scientific helper or production equation is changed.

```bash
set -euo pipefail
BASE=58cc629df42156c0b7862710057318db0a495dbb
test "$(git rev-parse HEAD)" = "$BASE"
test -z "$(git status --porcelain)"
export REPORT="${REPORT:-$HOME/Downloads/ZCOSMO_ROUND8_REPORT.md}"
export PATCH_DIR="$(mktemp -d)"
python - <<'PY'
import os,re
from pathlib import Path
text=Path(os.environ['REPORT']).read_text()
blocks=re.findall(r'<!-- BEGIN PATCH (\w+) -->\n```diff\n(.*?)```\n<!-- END PATCH \1 -->',text,re.S)
assert [name for name,_ in blocks]==['H8','P36','P37','P38','REG8']
for name,body in blocks:
    (Path(os.environ['PATCH_DIR'])/(name+'.patch')).write_text(body)
PY
for id in H8 P36 P37 P38 REG8; do
    git apply --check "$PATCH_DIR/$id.patch"
    git apply "$PATCH_DIR/$id.patch"
done
git diff --check
export PYTHONPATH="$PWD/src:$PWD/scripts"
python -m py_compile scripts/r8_*.py
python scripts/r8_selftest.py --out /tmp/zcosmo-r8-selftest.json
```

P36's benchmark and check require only the committed evidence, not PySCF or UD. Use a new output path; existing reports are not overwritten.

```bash
python scripts/r8_evidence.py --data docs/astra/round7/data \
  --out results/r8/evidence.json
python - <<'PY'
import json
r=json.load(open('results/r8/evidence.json'))
assert r['P32']['recorded_passed'] is False
assert abs(r['P32']['max_dsp_change']-.012074145054630225)<1e-14
assert abs(r['P32']['full_over_off']-1.1329537736908066)<1e-12
assert r['P33']['completed']==4
assert r['P33']['resolved_omitted_response_directions']==3
assert r['P33']['full_inconsistent_directions']==1
assert [r['P34'][k] for k in ('requested','positive','negative','affinity_unresolved','native_missing_or_failed')]==[40,35,0,4,1]
assert r['P34']['sampling_bound'] is None
print('Archived R7 outcomes retained; no new scientific gate has passed.')
PY
```

P38 is reporting-only. Its check is that the README diff adds the supplied evidence statement and changes no existing text:

```bash
git diff --check -- README.md
git diff -- README.md
```

The following is the prospective native command set, **not a record of actions performed here**. Adopt and commit the registration before freezing native plans. The maintainer may edit the proposed policy before adoption, but any changed numerical design must be reflected in the implementation and its new registration, rather than introduced after results.

```bash
# In the patched checkout, after adopting REG8:
cat docs/astra/round8/REGISTRATION_PROPOSED.md >> PREREGISTRATION.md
git add scripts/r8_*.py .github/workflows/r8_review.yml \
  docs/astra/round8/REGISTRATION_PROPOSED.md README.md PREREGISTRATION.md
git commit -m "Register R8 final derivative-stage diagnostic; keep profile versions frozen"
REG=$(git rev-parse HEAD)
python scripts/r8_diagnostic.py plan --registration "$REG" \
  --out cloud/r8/diagnostic
git add cloud/r8/diagnostic
git commit -m "Freeze the two R8 directions and eight bounded native arms"
```

Run the committed matrix once using the maintainer's normal push/merge process. The workflow must be available on the branch used for dispatch. This command assumes the registered plan has reached `main`, as in the earlier rounds; it does not push anything:

```bash
gh workflow run r8_review.yml --ref main \
  -f plan=cloud/r8/diagnostic/plan.json
```

Use that dispatch's explicit run ID when retrieving outputs. Set `R8_RUN_ID` to the ID returned/listed for the exact plan commit, rather than selecting the newest unrelated workflow. No failed member is automatically rerun.

```bash
: "${R8_RUN_ID:?Set the explicit ID of the single R8 dispatch}"
gh run watch "$R8_RUN_ID" --exit-status || true
# Failure does not prevent collecting the recorded failed and completed jobs.
gh run download "$R8_RUN_ID" -R Victor-Liang-ChE/zcosmo \
  --dir results/r8/native
python scripts/r8_diagnostic.py collect --plan cloud/r8/diagnostic/plan.json \
  --results results/r8/native --out results/r8/diagnostic.json
```

The collector returns nonzero for incomplete execution and writes the missing/failed identities. Successful collection means the eight diagnostics completed, not that all derivatives passed. Inspect the actual verdicts and cache checks:

```bash
python - <<'PY'
import json
r=json.load(open('results/r8/diagnostic.json'))
print('Complete:',r['complete'],'P33 baseline pattern:',r['baseline_P33_pattern_reproduced'])
for q in r['rows']:
    a=q['assessment']
    print(q['case'],q['arm'],'full:',a['full_verdict'],'off:',a['off_verdict'],
          'error:',a['full_error'],'indicator:',a['combined_indicator'],'wall_s:',q['wall_s'])
    if 'layer' in q:
        print('  PCM partial:',q['layer']['assessment']['full_verdict'],
              'cache parity:',q['layer']['parity'])
print('Missing/failed:',r['missing_or_failed'])
assert not r['authorizes_optimizer']
assert not r['authorizes_630_repolish']
assert not r['authorizes_chain_retry']
PY
```

For a recorded local venue instead of Actions, use the identical `run` subcommand once per fixed case/arm with `OMP_NUM_THREADS=4`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `BLIS_NUM_THREADS=1` and `ZC_PCM3C_MB=2000`. Do not run both venues for the same registered identity. The wrapper's deadlines and per-job timing are the benchmark; do not add timing repetitions to the scientific budget.

## Sources and provenance

Repository paths below refer to the pinned `main` unless a historical source is explicitly named. The full source identifiers make the report usable independently of chat citations.

| ID | Inspected source |
|---|---|
| S1 | `docs/astra/ROUND8_PROMPT.md`; `docs/OPTIMIZATION_BRIEF.md` (blob `9042052e2c0884226db6f795d14f8ec8c0157bd4`) |
| S2 | `docs/astra/round7/RESULTS.md` and archived round-7 report; report blob `1b2771b11cce157f570f113a979cbfab41520267` |
| S3 | `PREREGISTRATION.md`, R7 registration, P34a/P33a amendments and result entry; blob `d1db92d9997daa65d3e0edd2d2523201fda4ab38`; amendment commits `ef2fa5831a7be1d63db9b10b13c5d2c4be72abe1` and `29e9bf26cf0c2128956e1591c6a046244abbf0ba` |
| S4 | `docs/astra/round7/data/p32_calibration_gate.json`, blob `ad7f40f0c27d62eec3be85461f75aa5da67da525` |
| S5 | `docs/astra/round7/data/p34_primary_screen.json`, blob `4d73213e0245f7ee48484bd1353225efd522ecc2` |
| S6 | `docs/astra/round7/data/referee/`; TEG result blob `5e3046d8990fef3f55284d242802363a6079787c`; the five-case archive and its published outcome summary |
| S7 | `cloud/r7/referee/plan.json`, blob `c3518784628d6d6c8b56c7770a01e0183565aa01`; associated frozen geometry identities |
| S8 | R7 plan/optimizer/gate/screen/referee helpers and workflow. Reused common blob `990f4beff67165b5ed58d906926bd668b5fc834a`; amended referee `f4a26b35b915ccbdb5abb1b5f2ab3863ef91de4f`; amended screen `ec5ee0e423fd155daaed8f5dc21ea558e2b3cdc1`; workflow `0fe1507ab0bbed068506846f7918361756b3bbab` |
| S9 | `src/zcosmo/pcm_lu.py`, blob `f31533d998ed35a90349bfbe1e6553407fae5ee8`; `scripts/r3_precision.py` factory |
| S10 | `src/zcosmo/z0x.py`, blob `c558d4e95db9b78f3b57d6a103a293e21feeb9af`; `docs/astra/round6/RESULTS.md`; pre-P28 matched headline and numerical endpoint acceptance |
| U1 | `pyscf/pyscf@v2.14.0:pyscf/dft/rks.py`, executable `small_rho_cutoff`, `initialize_grids` and the contrasting docstring |
| U2 | `pyscf/pyscf@v2.14.0:pyscf/dft/gen_grid.py`, atomic-grid generation, `atm_idx`, padding, pruning and partition assembly |
| U3 | `pyscf/pyscf@v2.14.0:pyscf/grad/rks.py`, `get_vxc_full_response`, `grids_response_cc` and atomic quadrature regeneration |
| U4 | `pyscf/pyscf@v2.14.0:pyscf/solvent/pcm.py`, surface construction, C-PCM matrix equations, `_get_vind`, `grad` |
| U5 | `pyscf/pyscf@v2.14.0:pyscf/solvent/grad/pcm.py`, `grad_qv`, `grad_nuc`, `grad_solver`; `pyscf/df/grad/rks.py` for auxiliary-basis response |

## Unified diffs

### Patch H8

Files: `scripts/r8_common.py`, `scripts/r8_selftest.py`.

<!-- BEGIN PATCH H8 -->
```diff
diff --git a/scripts/r8_common.py b/scripts/r8_common.py
new file mode 100644
--- /dev/null
+++ b/scripts/r8_common.py
@@ -0,0 +1,117 @@
+"""R8 bookkeeping and finite-resolution diagnostics. No production changes."""
+from __future__ import annotations
+import hashlib
+import json
+import os
+from pathlib import Path
+import numpy as np
+
+BASE = '58cc629df42156c0b7862710057318db0a495dbb'
+STEPS = np.array([.016, .008, .004, .002, .001])  # Bohr, unchanged P33 ladder
+TAU = 1e-5
+CASES = {
+    'TEG': ('ZIBGPFATKBEMQZ-UHFFFAOYSA-N', 'bond-3-4'),
+    'EG': ('LYCAIKOWRPUZTN-UHFFFAOYSA-N', 'bond-2-3'),
+}
+ARMS = ('pcm_pruned', 'pcm_unpruned', 'vacuum_pruned', 'vacuum_unpruned')
+
+
+def sha(path):
+    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
+
+
+def write(path, obj):
+    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
+    tmp = p.with_name(p.name + '.tmp')
+    tmp.write_text(json.dumps(obj, indent=2, allow_nan=False) + '\n')
+    os.replace(tmp, p)
+
+
+def read(path):
+    return json.loads(Path(path).read_text())
+
+
+def validate_direction(v, n):
+    v = np.asarray(v, float)
+    if v.shape != (n, 3) or not np.isfinite(v).all():
+        raise ValueError('Malformed archived direction')
+    if abs(np.linalg.norm(v) - 1.) > 1e-10:
+        raise ValueError('Use the archived P33 unit-L2 Cartesian direction')
+    return v
+
+
+def richardson(energies):
+    e = np.asarray(energies, float)
+    if e.shape != (5, 2) or not np.isfinite(e).all():
+        raise ValueError('Need all five finite +/- energy pairs, no selected h')
+    d = (e[:, 0] - e[:, 1]) / (2 * STEPS)
+    return (4 * d[1:] - d[:-1]) / 3
+
+
+def fd_check(tight, strict, g_tight, g_full, g_off, topology_stable=True):
+    """Same P33 empirical accuracy allocation; not a certified error bound."""
+    from r7_common import fd_assess
+    ans = fd_assess(tight, strict, g_tight, g_full, g_off,
+                    topology_stable=topology_stable)
+    if ans['tolerance'] != TAU or ans['steps_Bohr'] != STEPS.tolist():
+        raise ValueError('P33 resolution changed')
+    return ans
+
+
+def canonical_membership(owners, ordinals):
+    """Count is insufficient: hash an order-independent multiset of node IDs."""
+    a = np.asarray(owners, dtype=np.int64)
+    b = np.asarray(ordinals, dtype=np.int64)
+    if a.ndim != 1 or a.shape != b.shape or np.any(a < 0) or np.any(b < 0):
+        raise ValueError('Invalid node identities')
+    ids = np.c_[a, b]
+    order = np.lexsort((ids[:, 1], ids[:, 0])); ids = ids[order]
+    if len(ids) > 1 and np.any(np.all(ids[1:] == ids[:-1], axis=1)):
+        raise ValueError('Duplicate quadrature node identity')
+    return hashlib.sha256(ids.astype('<i8').tobytes()).hexdigest(), order
+
+
+def match_local_nodes(local, template):
+    """Identify nodes by the generating atomic template, not rounded world positions."""
+    from scipy.spatial import cKDTree
+    local = np.asarray(local, float); template = np.asarray(template, float)
+    if local.ndim != 2 or local.shape[1] != 3 or not len(template):
+        raise ValueError('Invalid quadrature coordinates')
+    dist, index = cKDTree(template).query(local)
+    scale = np.maximum(1., np.linalg.norm(local, axis=1))
+    if np.any(dist > 1e-9 * scale):
+        raise ValueError('Cannot identify a quadrature node in its atomic template')
+    return index.astype(np.int64)
+
+
+def screening_counts(rows):
+    """Keep missing cases and coverage failures separate. Do not estimate prevalence."""
+    keys = [r['key'] for r in rows]
+    if len(keys) != len(set(keys)):
+        raise ValueError('Duplicate screen key')
+    complete = [r for r in rows if r.get('status') == 'complete']
+    for r in complete:
+        if type(r.get('screen_positive')) is not bool:
+            raise ValueError('Complete screen lacks a Boolean decision')
+    result = dict(requested=len(rows),
+        positive=sum(r['screen_positive'] for r in complete),
+        negative=sum(not r['screen_positive'] for r in complete),
+        affinity_unresolved=sum(r.get('status') == 'affinity_unresolved' for r in rows),
+        native_missing_or_failed=sum(r.get('status') not in ('complete', 'affinity_unresolved') for r in rows),
+        force_observed=sum('response_change_max' in r for r in rows),
+        force_over_1e_5=sum(float(r.get('response_change_max', 0.)) > 1e-5 for r in rows),
+        sampling_bound=None,
+        scope='Fixed-displacement sensitivity only; no inferred geometry error or population bound')
+    if result['positive'] + result['negative'] + result['affinity_unresolved'] + result['native_missing_or_failed'] != len(rows):
+        raise AssertionError('Lost denominator')
+    return result
+
+
+def file_sources(paths):
+    return {str(p): sha(p) for p in paths}
+
+
+def check_sources(sources):
+    for path, digest in sources.items():
+        if sha(path) != digest:
+            raise ValueError('Frozen source changed: ' + path)
diff --git a/scripts/r8_selftest.py b/scripts/r8_selftest.py
new file mode 100644
--- /dev/null
+++ b/scripts/r8_selftest.py
@@ -0,0 +1,286 @@
+"""Portable tests only. The mock SCF is an analytic polynomial, not PySCF."""
+from __future__ import annotations
+import argparse
+import contextlib
+import io
+import json
+import os
+from pathlib import Path
+import sys
+import tempfile
+import types
+import unittest
+from unittest.mock import patch
+import numpy as np
+from r8_common import (BASE, STEPS, CASES, ARMS, sha, read, write, fd_check,
+    canonical_membership, match_local_nodes, validate_direction, screening_counts)
+import r8_diagnostic as native
+from r8_evidence import audit
+
+METRICS={}
+
+@contextlib.contextmanager
+def cwd(path):
+    old=Path.cwd(); os.chdir(path)
+    try: yield
+    finally: os.chdir(old)
+
+
+def polynomial_pairs():
+    f=lambda x:-100.+.3*x+.2*x*x+.7*x**3+.1*x**5
+    return np.array([[f(h),f(-h)] for h in STEPS])
+
+
+class PortableTests(unittest.TestCase):
+    def test_fd_and_inconclusive(self):
+        e=polynomial_pairs(); a=fd_check(e,e,.3,.3,.30003)
+        self.assertEqual(a['full_verdict'],'consistent')
+        self.assertEqual(a['off_verdict'],'inconsistent')
+        self.assertTrue(a['missing_response_material'])
+        METRICS['polynomial_FD_error']=a['full_error']
+        noisy=e.copy();noisy[-1,0]+=1e-7
+        a=fd_check(noisy,noisy,.3,.3,.30003)
+        self.assertEqual(a['full_verdict'],'inconclusive')
+        self.assertEqual(fd_check(e,e,.3,.3,.3,False)['full_verdict'],'inconclusive')
+        with self.assertRaises(ValueError):fd_check(e[:-1],e,.3,.3,.3)
+
+    def test_node_identities(self):
+        a,_=canonical_membership([0,0,1],[0,1,0])
+        b,_=canonical_membership([1,0,0],[0,1,0]);self.assertEqual(a,b)
+        c,_=canonical_membership([0,0,1],[0,2,0]);self.assertNotEqual(a,c)
+        with self.assertRaises(ValueError):canonical_membership([0,0],[1,1])
+        template=np.array([[1.,0,0],[0,1,0],[-1,0,0]])
+        np.testing.assert_array_equal(match_local_nodes(template[[2,0]],template),[2,0])
+        with self.assertRaises(ValueError):match_local_nodes(np.array([[2.,0,0]]),template)
+        with self.assertRaises(ValueError):validate_direction(np.ones((2,3)),2)
+
+    def test_screen_denominators(self):
+        r=[dict(key=str(i),status='complete',screen_positive=True,
+                response_change_max=2e-5) for i in range(35)]
+        r += [dict(key=str(i),status='affinity_unresolved',screen_positive=None,
+                   response_change_max=2e-5) for i in range(35,39)]
+        r += [dict(key='39',status='running',screen_positive=None)]
+        d=screening_counts(r)
+        self.assertEqual([d[k] for k in ('requested','positive','negative','affinity_unresolved',
+                                        'native_missing_or_failed','force_observed')],[40,35,0,4,1,39])
+        self.assertIsNone(d['sampling_bound'])
+        with self.assertRaises(ValueError):screening_counts(r+[r[0]])
+
+    def test_explicit_pcm_math(self):
+        # Toy C-PCM algebra E=-f*v^T*K^-1*v/2, not molecular quantum chemistry.
+        K=np.array([[2.,.1],[.1,1.4]]);dK=np.array([[.2,.03],[.03,-.1]])
+        v=np.array([.3,-.2]);dv=np.array([.07,.03]);f=.999999999
+        z=np.linalg.solve(K,v)
+        exact=-f*dv@z+.5*f*z@dK@z
+        def energy(t):
+            u=v+t*dv
+            return -.5*f*u@np.linalg.solve(K+t*dK,u)
+        h=1e-5;fd=(energy(h)-energy(-h))/(2*h)
+        self.assertLess(abs(fd-exact),1e-10)
+        METRICS['explicit_PCM_matrix_derivative_error']=abs(fd-exact)
+
+    def test_pcm_layer_orchestration_with_mock(self):
+        # Check fixed P0, units and the exact 22+2 partial-layer call budget.
+        import copy,time
+        K0=np.array([[2.,.1],[.1,1.4]]);dK=np.array([[.2,.03],[.03,-.1]])
+        v0=np.array([.3,-.2]);dv=np.array([.07,.03]);f=.999999999
+        class Mol:
+            nao=2
+            def __init__(self,x):self.x=np.asarray(x).copy()
+            def copy(self):return copy.deepcopy(self)
+            def set_geom_(self,x,unit):
+                if unit!='Angstrom':raise ValueError(unit)
+                self.x=np.asarray(x).copy();return self
+            def intor_symmetric(self,name):return np.eye(2)*(1.+.01*self.x[0,0])
+        calls=[0,0]
+        class PCM:
+            def __init__(self,mol):self.mol=mol
+            def _get_vind(self,P):
+                np.testing.assert_array_equal(P,np.eye(2));calls[0]+=1
+                t=self.mol.x[0,0];K=K0+t*dK;v=v0+t*dv;R=-f*np.eye(2)
+                q=np.linalg.solve(K,R@v)
+                self._intermediates={'K':K,'R':R,'q':q,'v_grids':v}
+                return .5*q@v,np.zeros((2,2))
+            def grad(self,P):
+                np.testing.assert_array_equal(P,np.eye(2));calls[1]+=1
+                z=np.linalg.solve(K0,v0);g=np.zeros((2,3))
+                g[0,0]=-f*dv@z+.5*f*z@dK@z;return g
+        settings=dict(method='C-PCM',eps=1e9,lebedev_order=17,radii_table=np.ones(10),
+                      vdw_scale=1.2,r_probe=0.,surface_discretization_method='SWIG')
+        xyz=np.zeros((2,3));v=np.zeros((2,3));v[0,0]=1.
+        template=types.SimpleNamespace(mol=Mol(xyz),with_solvent=types.SimpleNamespace(**settings),make_rdm1=lambda:np.eye(2))
+        modules={}
+        for name in ('pyscf','pyscf.solvent','zcosmo'):
+            modules[name]=types.ModuleType(name);modules[name].__path__=[]
+        for name,attrs in [('pyscf.solvent.pcm',{'PCM':PCM}),('zcosmo.pcm_lu',{'CachedPCM3c':PCM}),
+                           ('zcosmo.pyscf_cosmo',{'BOHR':1.})]:
+            modules[name]=types.ModuleType(name);modules[name].__dict__.update(attrs)
+        with tempfile.TemporaryDirectory() as td,patch.dict(sys.modules,modules), \
+             patch.object(native,'pcm_nodes',return_value={'signature':'same','count':2}):
+            native.pcm_layer_check(template,xyz,v,time.monotonic()+10,Path(td))
+            d=read(Path(td)/'layer.json');self.assertEqual(calls,[22,2])
+            self.assertTrue(d['parity']['passed'])
+            self.assertEqual(d['assessment']['full_verdict'],'consistent')
+            counts=[r['overlap_electrons'] for r in read(Path(td)/'layer_calls.json')]
+            self.assertGreater(max(counts)-min(counts),0.)
+            METRICS['mock_PCM_layer_calls']={'energy':22,'gradient':2}
+
+    def test_plan_roundtrip_and_tamper(self):
+        with tempfile.TemporaryDirectory() as td,cwd(td):
+            oldpath=Path('cloud/r7/referee/plan.json');cases=[]
+            for label,(key,direction) in CASES.items():
+                geom=oldpath.parent/(key+'.json')
+                write(geom,dict(sym=['H','H'],x=[[0.,0,0],[1.,0,0]]))
+                cases.append(dict(key=key,geometry=geom.name,geometry_sha256=sha(geom),spin=0))
+            write(oldpath,dict(family='referee',cases=cases))
+            for r in cases:
+                key=r['key']; direction=next(v[1] for v in CASES.values() if v[0]==key)
+                write(Path('docs/astra/round7/data/referee')/(key+'.result.json'),dict(
+                    status='diagnostic_complete',plan_sha256=sha(oldpath),
+                    input_geometry_sha256=r['geometry_sha256'],records=[dict(direction=direction,
+                    unit_L2_direction=[[1.,0,0],[0.,0,0]])]))
+            for source in native.SOURCES:
+                p=Path(source);p.parent.mkdir(parents=True,exist_ok=True);p.write_text('synthetic source\n')
+            native.plan(types.SimpleNamespace(registration='a'*40,out='new'))
+            _,m=native.load_plan('new/plan.json')
+            self.assertEqual(m['budgets']['SCF_calls'],176)
+            Path(native.SOURCES[0]).write_text('changed\n')
+            with self.assertRaises(ValueError):native.load_plan('new/plan.json')
+            Path(native.SOURCES[0]).write_text('synthetic source\n')
+            bad=Path('docs/astra/round7/data/referee')/(cases[0]['key']+'.result.json')
+            d=read(bad);d['records']=[];write(bad,d)
+            with self.assertRaises(ValueError):native.plan(types.SimpleNamespace(registration='a'*40,out='bad'))
+            self.assertFalse(Path('bad').exists())
+
+    def test_native_orchestration_with_mock_SCF(self):
+        # Exercise all 22 energy evaluations and failure recording, without native imports.
+        with tempfile.TemporaryDirectory() as td:
+            out=Path(td)/'run';geometry=Path(td)/'TEG.json'
+            x=np.zeros((2,3));direction=np.zeros((2,3));direction[0,0]=1.
+            write(geometry,dict(sym=['H','H'],x=x.tolist()))
+            planfile=Path(td)/'plan.json';write(planfile,{})
+            key=CASES['TEG'][0]
+            m=dict(registration='a'*40,cases=[dict(label='TEG',key=key,
+                geometry=geometry.name,geometry_sha256=sha(geometry),direction=direction.tolist(),
+                direction_name=CASES['TEG'][1])])
+            count=[0];fail=[None]
+            class MF:
+                def __init__(self,pos):self.pos=pos;self.converged=True;self.cycles=1;self.small_rho_cutoff=0.;self.grids=types.SimpleNamespace(prune=None)
+                def kernel(self):
+                    count[0]+=1
+                    if count[0]==fail[0]:raise RuntimeError('mock SCF failure')
+                    t=float(self.pos[0,0]);return -100.+.3*t+.2*t*t+.7*t**3+.1*t**5
+                def make_rdm1(self):return np.eye(2)
+            def g(mf,response):return direction*(.3 if response else .30003)
+            z=types.ModuleType('zcosmo');z.__path__=[]
+            pc=types.ModuleType('zcosmo.pyscf_cosmo');pc.BOHR=1.
+            import importlib
+            original=importlib.import_module
+            def modules(name,*args,**kw):
+                if name.startswith('pyscf.'):
+                    return types.SimpleNamespace(__name__=name,__file__=__file__)
+                return original(name,*args,**kw)
+            with patch.dict(sys.modules,{'zcosmo':z,'zcosmo.pyscf_cosmo':pc}), \
+                 patch('importlib.metadata.version',side_effect=lambda n:{'pyscf':'2.14.0','pyberny':'0.7.0','numpy':'2','scipy':'1'}[n]), \
+                 patch('importlib.import_module',side_effect=modules), \
+                 patch.object(native,'load_plan',return_value=(planfile,m)), \
+                 patch.object(native,'make_mf',side_effect=lambda s,p,precision,arm:MF(p)), \
+                 patch.object(native,'full_gradient',side_effect=g), \
+                 patch.object(native,'xc_nodes',return_value=({'signature':'same','count':3},None,None)), \
+                 patch.object(native,'response_grid_check',return_value={'membership_identical':True,'weights_match':True}), \
+                 patch('r7_common.clean_environment'):
+                a=types.SimpleNamespace(plan=str(planfile),case='TEG',arm='vacuum_pruned',out=str(out))
+                native.native(a)
+                d=read(out/'result.json')
+                self.assertEqual(count[0],22);self.assertEqual(d['gradient_evaluations'],3)
+                self.assertEqual(d['assessment']['full_verdict'],'consistent')
+                self.assertEqual(d['assessment']['off_verdict'],'inconsistent')
+                count[0]=0;fail[0]=3;a.out=str(Path(td)/'failed')
+                with self.assertRaises(RuntimeError):native.native(a)
+                d=read(Path(a.out)/'result.json');self.assertEqual(d['status'],'failed')
+                self.assertEqual(d['SCF_evaluations'],3)
+            METRICS['mock_SCF_count']=22
+
+    def test_collect_missing_and_duplicates(self):
+        with tempfile.TemporaryDirectory() as td:
+            p=Path(td)/'plan.json';write(p,{})
+            cases=[dict(label=label,key=key,geometry_sha256='b'*64) for label,(key,_) in CASES.items()]
+            m=dict(registration='a'*40,cases=cases)
+            root=Path(td)/'results';root.mkdir()
+            for case in cases:
+                for arm in ARMS:
+                    dest=root/case['label']/arm
+                    write(dest/'result.json',dict(plan_sha256=sha(p),label=case['label'],arm=arm,
+                        status='diagnostic_complete',key=case['key'],geometry_sha256='b'*64,
+                        SCF_evaluations=22,gradient_evaluations=3,assessment={'full_verdict':'inconclusive'},
+                        response_grid_check={},wall_s=1.,packages={},upstream_sha256={}))
+                    write(dest.with_name(arm+'.terminal.json'),dict(plan_sha256=sha(p),case=case['label'],arm=arm,status='completed',execution={'returncode':0}))
+                    if arm=='pcm_pruned':write(dest/'layer.json',dict(explicit_energy_evaluations=22,gradient_evaluations=2))
+            with patch.object(native,'load_plan',return_value=(p,m)):
+                a=types.SimpleNamespace(plan=str(p),results=str(root),out=str(Path(td)/'all.json'))
+                native.collect(a);self.assertTrue(read(a.out)['complete'])
+                missing=root/'TEG'/'vacuum_pruned'/'result.json';missing.unlink()
+                a.out=str(Path(td)/'missing.json')
+                with self.assertRaises(SystemExit):native.collect(a)
+                self.assertEqual(read(a.out)['completed_jobs'],7)
+                src=root/'EG'/'pcm_pruned'/'result.json'
+                write(root/'duplicate'/'result.json',read(src));a.out=str(Path(td)/'dupe.json')
+                with self.assertRaises(ValueError):native.collect(a)
+
+    def test_bound_failure_deadline_and_claim(self):
+        from r7_common import bounded
+        with tempfile.TemporaryDirectory() as td:
+            p=Path(td)/'one'
+            r=bounded([sys.executable,'-c','raise SystemExit(2)'],p,2)
+            self.assertEqual(r['execution_status'],'child_failed')
+            with self.assertRaises(FileExistsError):bounded([sys.executable,'-c','pass'],p,2)
+            r=bounded([sys.executable,'-c','import time;time.sleep(5)'],Path(td)/'two',.1)
+            self.assertEqual(r['execution_status'],'deadline')
+            # R7 bounded can label diagnostic_complete as completed despite rc!=0.
+            # The R8 wrapper must still reject that operational failure.
+            planfile=Path(td)/'plan.json';write(planfile,{})
+            out=Path(td)/'late-failure'
+            write(out/'result.json',dict(status='diagnostic_complete',assessment={'full_verdict':'consistent'}))
+            a=types.SimpleNamespace(plan=str(planfile),case='TEG',arm='pcm_pruned',out=str(out))
+            with patch.object(native,'load_plan',return_value=(planfile,{})), \
+                 patch('r7_common.bounded',return_value={'execution_status':'completed','returncode':1}):
+                with self.assertRaises(SystemExit):native.run(a)
+            self.assertEqual(read(out.with_name(out.name+'.terminal.json'))['status'],'failed')
+
+    def test_evidence_schema_and_retention(self):
+        with tempfile.TemporaryDirectory() as td:
+            root=Path(td)
+            checks={model:{name:dict(requested=2302,finite_reference=n,finite_candidate=n,
+                   coverage_identical=True,max_abs_change=.0121,median_abs_change=.00017)
+                   for name in ('candidate_vs_control','candidate_vs_UD')}
+                   for model,n in (('cosmosac_dsp',2271),('Z0x',2302))}
+            runs=[dict(key=str(i),wall_s={'off':1.,'full':1.13}) for i in range(25)]
+            write(root/'p32_calibration_gate.json',dict(rows=2302,targets=25,runs=runs,checks=checks,passed=False))
+            rows=[dict(key=str(i),status='complete',screen_positive=True) for i in range(35)]
+            rows += [dict(key=str(i),status='affinity_unresolved') for i in range(35,39)]+[dict(key='39',status='running')]
+            write(root/'p34_primary_screen.json',dict(rows=rows))
+            keys=['BKIMMITUMNQMOS','ZIBGPFATKBEMQZ','XTHFKEDIFFGKHM','LYCAIKOWRPUZTN','OKKJLVBELUTLKV']
+            for i,k in enumerate(keys):
+                key=k+'-UHFFFAOYSA-N'
+                records=[dict(direction=str(j),full_verdict='inconclusive',off_verdict='inconclusive',
+                    combined_indicator=1.,full_error=0.,off_error=0.,missing_response_material=None) for j in range(4)]
+                write(root/'referee'/(key+'.result.json'),dict(key=key,status='diagnostic_complete' if i<4 else 'failed',records=records))
+            with contextlib.redirect_stdout(io.StringIO()):a=audit(root,root/'out.json')
+            self.assertEqual(a['P33']['completed'],4)
+            self.assertFalse(a['P32']['chains_authorized']);self.assertIsNone(a['P32']['count_of_over_limit_queries'])
+            (root/'referee'/(keys[0]+'-UHFFFAOYSA-N.result.json')).unlink()
+            with self.assertRaises(ValueError):audit(root,root/'bad.json')
+
+
+def main():
+    p=argparse.ArgumentParser();p.add_argument('--out');a=p.parse_args()
+    suite=unittest.defaultTestLoader.loadTestsFromTestCase(PortableTests)
+    r=unittest.TextTestRunner(verbosity=2).run(suite)
+    summary=dict(tests=r.testsRun,failures=len(r.failures),errors=len(r.errors),passed=r.wasSuccessful(),
+        metrics=METRICS,scope='Portable and mocked orchestration only; no native PySCF or actual Mac-backed data')
+    if a.out:write(a.out,summary)
+    print(json.dumps(summary,indent=2))
+    raise SystemExit(0 if r.wasSuccessful() else 1)
+
+
+if __name__=='__main__':main()
```
<!-- END PATCH H8 -->

### Patch P36

Files: `scripts/r8_evidence.py`.

<!-- BEGIN PATCH P36 -->
```diff
diff --git a/scripts/r8_evidence.py b/scripts/r8_evidence.py
new file mode 100644
--- /dev/null
+++ b/scripts/r8_evidence.py
@@ -0,0 +1,90 @@
+"""Read R7 decisions without re-gating them or running a model."""
+from __future__ import annotations
+import argparse
+import json
+from pathlib import Path
+import numpy as np
+from r8_common import BASE, read, write, sha, screening_counts
+
+
+def audit(root, out):
+    root = Path(root)
+    p32 = root / 'p32_calibration_gate.json'
+    p34 = root / 'p34_primary_screen.json'
+    cal, screen = read(p32), read(p34)
+    if cal['rows'] != 2302 or cal['targets'] != 25 or len(cal['runs']) != 25:
+        raise ValueError('Historical calibration denominator changed')
+    if len({r['key'] for r in cal['runs']}) != 25:
+        raise ValueError('Duplicate calibration member')
+    dsp = cal['checks']['cosmosac_dsp']['candidate_vs_control']
+    ud = cal['checks']['cosmosac_dsp']['candidate_vs_UD']
+    for model, n in (('cosmosac_dsp', 2271), ('Z0x', 2302)):
+        for kind in ('candidate_vs_control', 'candidate_vs_UD'):
+            q = cal['checks'][model][kind]
+            if q['requested'] != 2302 or q['finite_reference'] != n or q['finite_candidate'] != n or not q['coverage_identical']:
+                raise ValueError('Historical calibration coverage changed')
+    if cal['passed'] is not False:
+        raise ValueError('This report expects the recorded failed P32 gate')
+    time_by_arm = {arm: sum(float(r['wall_s'][arm]) for r in cal['runs'])
+                   for arm in ('off', 'full')}
+    if not all(np.isfinite(t) and t > 0 for t in time_by_arm.values()):
+        raise ValueError('Invalid timing data')
+    histories = []
+    expected = {
+        'BKIMMITUMNQMOS-UHFFFAOYSA-N', 'ZIBGPFATKBEMQZ-UHFFFAOYSA-N',
+        'XTHFKEDIFFGKHM-UHFFFAOYSA-N', 'LYCAIKOWRPUZTN-UHFFFAOYSA-N',
+        'OKKJLVBELUTLKV-UHFFFAOYSA-N'}
+    source = {str(p32): sha(p32), str(p34): sha(p34)}
+    paths = sorted((root / 'referee').glob('*.result.json'))
+    if {p.name.removesuffix('.result.json') for p in paths} != expected:
+        raise ValueError('Missing or extra archived referee case')
+    for p in paths:
+        d = read(p); key = p.name.removesuffix('.result.json')
+        if d['key'] != key:
+            raise ValueError('Referee identity mismatch')
+        source[str(p)] = sha(p)
+        row = dict(key=key, status=d['status'], directions=[])
+        if d['status'] == 'diagnostic_complete':
+            if len(d['records']) != 4:
+                raise ValueError('Incomplete directional record')
+            for r in d['records']:
+                for v in ('full_verdict', 'off_verdict'):
+                    if r[v] not in ('consistent', 'inconsistent', 'inconclusive'):
+                        raise ValueError('Invalid tri-state verdict')
+                row['directions'].append({k: r[k] for k in (
+                    'direction', 'full_verdict', 'off_verdict', 'combined_indicator',
+                    'full_error', 'off_error', 'missing_response_material')})
+        histories.append(row)
+    counts = screening_counts(screen['rows'])
+    all_directions = [r for h in histories for r in h['directions']]
+    ans = dict(base=BASE, source_sha256=source,
+        P32=dict(recorded_passed=cal['passed'], rows=2302, targets=25,
+            max_dsp_change=dsp['max_abs_change'], median_dsp_change=dsp['median_abs_change'],
+            excess_over_original_limit=dsp['max_abs_change'] - .01,
+            median_dsp_vs_UD=ud['median_abs_change'],
+            worker_seconds=time_by_arm, full_over_off=time_by_arm['full']/time_by_arm['off'],
+            count_of_over_limit_queries=None,
+            reason_count_unavailable='Archived gate stores extrema, not per-query values',
+            pilot_authorized=False, chains_authorized=False),
+        P33=dict(cases=histories, completed=sum(h['status']=='diagnostic_complete' for h in histories),
+            resolved_omitted_response_directions=sum(r['missing_response_material'] is True for r in all_directions),
+            full_inconsistent_directions=sum(r['full_verdict']=='inconsistent' for r in all_directions),
+            unknowns_are_not_passes=True),
+        P34=counts, primary_repolish_authorized=False)
+    write(out, ans)
+    print(json.dumps({k: ans[k] for k in ('P32', 'P34')}, indent=2))
+    return ans
+
+
+def main():
+    p=argparse.ArgumentParser()
+    p.add_argument('--data', default='docs/astra/round7/data')
+    p.add_argument('--out', required=True)
+    a=p.parse_args()
+    if Path(a.out).exists():
+        raise FileExistsError(a.out)
+    audit(a.data, a.out)
+
+
+if __name__ == '__main__':
+    main()
```
<!-- END PATCH P36 -->

### Patch P37

Files: `scripts/r8_diagnostic.py`, `.github/workflows/r8_review.yml`.

<!-- BEGIN PATCH P37 -->
```diff
diff --git a/scripts/r8_diagnostic.py b/scripts/r8_diagnostic.py
new file mode 100644
--- /dev/null
+++ b/scripts/r8_diagnostic.py
@@ -0,0 +1,405 @@
+"""P37: one fixed stage-isolation experiment, not an optimizer or rollout.
+
+Two archived directions, four SCF arms per direction. On the PCM/pruned arm,
+a fixed-AO-density layer check separates explicit PCM derivatives from the
+self-consistent total-energy derivative. No profiles or experimental scores.
+"""
+from __future__ import annotations
+import argparse
+import json
+import os
+from pathlib import Path
+import shutil
+import sys
+import time
+import numpy as np
+from r8_common import (BASE, CASES, ARMS, STEPS, TAU, sha, read, write,
+    validate_direction, canonical_membership, match_local_nodes, fd_check,
+    file_sources, check_sources)
+
+SOURCES = ['scripts/r8_common.py', 'scripts/r8_diagnostic.py',
+           'scripts/r7_common.py', 'scripts/r3_precision.py',
+           'src/zcosmo/pyscf_cosmo.py', 'src/zcosmo/pcm_lu.py']
+
+
+def plan(a):
+    from r7_common import registration, geometry
+    registration(a.registration)
+    oldpath = Path('cloud/r7/referee/plan.json')
+    old = read(oldpath); oldhash = sha(oldpath)
+    if old['family'] != 'referee':
+        raise ValueError('Expected the archived R7 referee plan')
+    data = Path('docs/astra/round7/data/referee')
+    out = Path(a.out)
+    if out.exists():
+        raise FileExistsError(out)
+    planned = []; inputs = [oldpath]
+    for label, (key, direction) in CASES.items():
+        matches = [r for r in old['cases'] if r['key'] == key]
+        if len(matches) != 1:
+            raise ValueError('Missing or duplicate frozen R7 geometry')
+        r = matches[0]; src = oldpath.parent / r['geometry']
+        sym, xyz = geometry(src)
+        if sha(src) != r['geometry_sha256'] or r['spin'] != 0:
+            raise ValueError('Geometry or closed-shell scope mismatch')
+        resultpath = data / (key + '.result.json'); d = read(resultpath)
+        if d['status'] != 'diagnostic_complete' or d['plan_sha256'] != oldhash:
+            raise ValueError('Need the exact completed P33 record for this input')
+        if d['input_geometry_sha256'] != sha(src):
+            raise ValueError('P33 result geometry mismatch')
+        rows = [v for v in d['records'] if v['direction'] == direction]
+        if len(rows) != 1:
+            raise ValueError('Archived direction missing or duplicated')
+        v = validate_direction(rows[0]['unit_L2_direction'], len(sym))
+        planned.append(dict(label=label, key=key, geometry=label+'.json',
+            geometry_sha256=sha(src), sym=sym, direction_name=direction,
+            direction=v.tolist(), source_geometry=str(src),
+            source_result_sha256=sha(resultpath)))
+        inputs.extend([src, resultpath])
+    # Finish every validation before creating a plan. No native computation here.
+    sources = file_sources(SOURCES); input_hashes = file_sources(inputs)
+    out.mkdir(parents=True)
+    for r in planned:
+        shutil.copyfile(r['source_geometry'], out/r['geometry'])
+    write(out/'plan.json', dict(base=BASE, registration=a.registration, cases=planned,
+        arms=list(ARMS), sources=sources, inputs=input_hashes,
+        seconds_per_job=3600, SCF_calls_per_job=22, steps_Bohr=STEPS.tolist(), tau=TAU,
+        budgets=dict(jobs=8, four_core_worker_hours=8, SCF_calls=176,
+                     total_gradients=24, explicit_PCM_energy_calls=44, PCM_gradients=4),
+        authorizes_optimization=False, authorizes_profiles=False,
+        reason='Isolate one unresolved P33 regression against one already-consistent direction'))
+
+
+def load_plan(path):
+    p=Path(path).resolve(); m=read(p)
+    if m['base'] != BASE or m['arms'] != list(ARMS) or m['steps_Bohr'] != STEPS.tolist() or m['tau'] != TAU:
+        raise ValueError('Unregistered diagnostic definition')
+    if m['seconds_per_job'] != 3600 or m['SCF_calls_per_job'] != 22:
+        raise ValueError('Diagnostic budget changed')
+    if {r['label'] for r in m['cases']} != set(CASES) or len(m['cases']) != 2:
+        raise ValueError('Fixed cases changed')
+    from r7_common import registration
+    registration(m['registration']); check_sources(m['sources']); check_sources(m['inputs'])
+    for r in m['cases']:
+        if (r['key'], r['direction_name']) != CASES[r['label']]:
+            raise ValueError('Fixed direction changed')
+        if sha(p.parent/r['geometry']) != r['geometry_sha256']:
+            raise ValueError('Frozen geometry changed')
+        from r7_common import geometry
+        sym, _ = geometry(p.parent/r['geometry'])
+        if sym != r['sym']:
+            raise ValueError('Frozen atom identity mismatch')
+        validate_direction(r['direction'], len(r['sym']))
+    return p,m
+
+
+def xc_nodes(mf):
+    """Map retained SCF nodes to (owner, atomic-template ordinal), ignoring padding."""
+    grids=mf.grids; mol=mf.mol
+    tab=grids.gen_atomic_grids(mol, grids.atom_grid, grids.radi_method,
+                              grids.level, grids.prune)
+    owner=np.asarray(grids.atm_idx, dtype=int)
+    valid=owner >= 0; owners=owner[valid]
+    coords=np.asarray(grids.coords)[valid]; weights=np.asarray(grids.weights)[valid]
+    atoms=mol.atom_coords(); ordinals=np.empty(len(owners), dtype=np.int64)
+    for i in range(mol.natm):
+        use=owners==i
+        ordinals[use]=match_local_nodes(coords[use]-atoms[i], tab[mol.atom_symbol(i)][0])
+    signature, order=canonical_membership(owners, ordinals)
+    return dict(signature=signature, count=len(owners)), (owners,ordinals,weights,order), tab
+
+
+def response_grid_check(mf, actual, tab):
+    """Compare the quadrature used in full-response integration with SCF quadrature.
+
+    This costs no SCF and does not replace the actual gradient implementation.
+    """
+    from pyscf.grad.rks import grids_response_cc
+    owners=[]; ordinals=[]; weights=[]; atoms=mf.mol.atom_coords()
+    for i,(coords,w,_dw) in enumerate(grids_response_cc(mf.grids)):
+        owners.extend([i]*len(w))
+        ordinals.extend(match_local_nodes(coords-atoms[i], tab[mf.mol.atom_symbol(i)][0]))
+        weights.extend(w)
+    digest,order=canonical_membership(owners,ordinals)
+    ao,an,aw,aorder=actual
+    actual_digest,_=canonical_membership(ao,an)
+    same=digest==actual_digest
+    equal=False; difference=None
+    if same:
+        a=np.asarray(aw)[aorder]; b=np.asarray(weights)[order]
+        difference=float(np.max(abs(a-b))) if len(a) else 0.
+        equal=bool(np.allclose(a,b,rtol=1e-10,atol=1e-12))
+    return dict(membership_identical=same, weights_match=equal,
+        max_weight_difference=difference, relative_tolerance=1e-10, absolute_tolerance=1e-12)
+
+
+def pcm_nodes(s):
+    from pyscf.dft.gen_grid import MakeAngularGrid
+    surf=s.surface; nodes=MakeAngularGrid(int(surf['ng']))[:,:3]
+    owners=[]; ordinals=[]
+    for i,(lo,hi) in enumerate(surf['gslice_by_atom']):
+        owners.extend([i]*(hi-lo))
+        ordinals.extend(match_local_nodes(surf['norm_vec'][lo:hi], nodes))
+    digest,_=canonical_membership(owners,ordinals)
+    return dict(signature=digest, count=len(owners),
+        minimum_switch=float(np.min(surf['switch_fun'])),
+        note='Retained surface-node identity; continuous switching weights are not fixed')
+
+
+def make_mf(sym, xyz, precision, arm):
+    from r7_common import factory
+    mf=factory(sym,xyz,0,precision)
+    # Runtime code, not a docstring, decides the actual density-pruning default.
+    if float(mf.small_rho_cutoff) != 0.:
+        raise RuntimeError('Unexpected density pruning: baseline differs; no silent override')
+    if arm.endswith('_unpruned'):
+        mf.grids.prune=None
+    if arm.startswith('vacuum_'):
+        mf=mf.undo_solvent()
+        if getattr(mf,'with_solvent',None) is not None:
+            raise RuntimeError('Vacuum control still has PCM attached')
+    return mf
+
+
+def full_gradient(mf, response):
+    g=mf.nuc_grad_method(); g.grid_response=bool(response)
+    if not bool(getattr(g,'auxbasis_response',False)):
+        raise RuntimeError('Density-fitting derivative was detached')
+    out=np.asarray(g.kernel(),float)
+    if not np.isfinite(out).all():
+        raise RuntimeError('Nonfinite gradient')
+    return out
+
+
+def pcm_layer_check(template, xyz, direction, deadline, out):
+    """Derivative of E_PCM(R,P0) at FIXED AO coefficient matrix P0.
+
+    The basis functions move with the atoms and the surface charges are solved
+    anew. This is NOT a fixed physical electron density, a total BO derivative,
+    or the derivative of the PCM component along an SCF solution curve.
+    """
+    from pyscf.solvent.pcm import PCM
+    from zcosmo.pcm_lu import CachedPCM3c
+    from zcosmo.pyscf_cosmo import BOHR
+    P=np.asarray(template.make_rdm1()).copy()
+    if P.ndim!=2:
+        raise ValueError('This fixed two-case pilot is restricted to closed-shell RKS')
+    old=template.with_solvent; records=[]; all_energies={}; center_energies={}; grad={}
+    settings=('method','eps','lebedev_order','radii_table','vdw_scale','r_probe','surface_discretization_method')
+    for engine,cls in (('stock',PCM),('cached',CachedPCM3c)):
+        energies=[]
+        for index,(h,sign) in enumerate([(0.,0.)]+[(float(h),s) for h in STEPS for s in (1.,-1.)]):
+            if time.monotonic()>deadline:
+                raise TimeoutError('Native fixed deadline')
+            mol=template.mol.copy(); mol.set_geom_(xyz+sign*h*BOHR*direction,unit='Angstrom')
+            if mol.nao!=P.shape[0]:
+                raise ValueError('AO basis changed')
+            s=cls(mol); s.max_memory=4000
+            for name in settings:
+                val=getattr(old,name)
+                setattr(s,name,val.copy() if isinstance(val,np.ndarray) else val)
+            e=float(s._get_vind(P)[0]); it=s._intermediates
+            residual=float(np.max(abs(it['K']@it['q']-it['R']@it['v_grids']))/
+                           max(1.,np.max(abs(it['R']@it['v_grids']))))
+            if not np.isfinite(e) or residual>1e-10:
+                raise RuntimeError('PCM energy/linear solve failed')
+            if index==0:
+                center_energies[engine]=e
+                grad[engine]=np.asarray(s.grad(P))
+                if not np.isfinite(grad[engine]).all():
+                    raise RuntimeError('Nonfinite PCM derivative')
+            else:
+                energies.append(e)
+            records.append(dict(engine=engine,h_Bohr=h,sign=sign,energy_Eh=e,
+                solve_residual=residual,PCM=pcm_nodes(s),
+                overlap_electrons=float(np.einsum('ij,ji->',P,mol.intor_symmetric('int1e_ovlp')))))
+            write(out/'layer_calls.json',records)
+        all_energies[engine]=np.asarray(energies).reshape(5,2)
+    stock=all_energies['stock']; cached=all_energies['cached']
+    gs=float(np.sum(grad['stock']*direction)); gc=float(np.sum(grad['cached']*direction))
+    assessment=fd_check(stock,cached,gs,gc,gs,
+        topology_stable=len({r['PCM']['signature'] for r in records})==1)
+    assessment['precision_interpretation']='Two float64 implementations at identical fixed P0, not a high-precision oracle'
+    parity=dict(max_energy_difference_Eh=max(float(np.max(abs(stock-cached))),
+                abs(center_energies['stock']-center_energies['cached'])),
+                max_gradient_difference_Eh_Bohr=float(np.max(abs(grad['stock']-grad['cached']))))
+    parity['passed']=bool(parity['max_energy_difference_Eh']<1e-9 and parity['max_gradient_difference_Eh_Bohr']<1e-8)
+    write(out/'layer.json',dict(assessment=assessment,parity=parity,center_energy_Eh=center_energies,
+        energies={k:v.tolist() for k,v in all_energies.items()},
+        projected_gradient={'stock':gs,'cached':gc},
+        fixed_AO_density_sha256=__import__('hashlib').sha256(P.tobytes()).hexdigest(),
+        explicit_energy_evaluations=len(records), gradient_evaluations=2,
+        scope='Explicit PCM partial derivative only; overlap electron count can change off center'))
+
+
+def native(a):
+    from importlib.metadata import version
+    from packaging.version import Version
+    from r7_common import geometry,clean_environment
+    for package,expected in (('pyscf','2.14.0'),('pyberny','0.7.0')):
+        if Version(version(package))!=Version(expected):
+            raise RuntimeError('Requires the registered pinned native environment')
+    p,m=load_plan(a.plan)
+    r=next(x for x in m['cases'] if x['label']==a.case)
+    if a.arm not in ARMS:
+        raise ValueError('Unknown arm')
+    out=Path(a.out); out.mkdir(parents=True,exist_ok=False)
+    clean_environment();sym,xyz=geometry(p.parent/r['geometry'])
+    v=validate_direction(r['direction'],len(sym))
+    from zcosmo.pyscf_cosmo import BOHR
+    start=time.monotonic();deadline=start+3400;calls=[];center=None;tables={};gradients={};checks={}
+    import importlib
+    upstream = [importlib.import_module(name) for name in (
+        'pyscf.dft.rks', 'pyscf.dft.gen_grid', 'pyscf.grad.rks',
+        'pyscf.df.grad.rks', 'pyscf.solvent.pcm', 'pyscf.solvent.grad.pcm')]
+    provenance=dict(packages={name:version(name) for name in ('pyscf','pyberny','numpy','scipy')},
+        upstream_sha256={mod.__name__:sha(mod.__file__) for mod in upstream},
+        base=BASE,registration=m['registration'],plan_sha256=sha(p),
+        label=a.case,key=r['key'],arm=a.arm,geometry_sha256=r['geometry_sha256'],
+        direction=r['direction_name'],adopted=False,optimization_authorized=False)
+    write(out/'result.json',dict(provenance,status='running'))
+    def evaluate(pos,precision):
+        if len(calls)>=22 or time.monotonic()>deadline:
+            raise TimeoutError('Fixed SCF/evaluation budget exhausted')
+        mf=make_mf(sym,pos,precision,a.arm)
+        record=dict(index=len(calls),precision=precision,status='started')
+        calls.append(record);write(out/'calls.json',calls)
+        e=float(mf.kernel())
+        if not mf.converged or not np.isfinite(e):
+            raise RuntimeError('SCF failed; no alternate solver or retry')
+        signature,node_data,tab=xc_nodes(mf)
+        record.update(status='completed',energy_Eh=e,XC=signature,
+            small_rho_cutoff=float(mf.small_rho_cutoff),
+            prune=repr(mf.grids.prune),SCF_cycles=int(getattr(mf,'cycles',-1)),
+            PCM=pcm_nodes(mf.with_solvent) if a.arm.startswith('pcm_') else None)
+        write(out/'calls.json',calls)
+        return e,mf,node_data,tab
+    try:
+        for precision in ('tight','strict'):
+            _,mf,nodes,tab=evaluate(xyz,precision)
+            if precision == 'strict':
+                center=mf
+            gradients[precision]=full_gradient(mf,True)
+            checks[precision]=response_grid_check(mf,nodes,tab)
+        off=full_gradient(center,False)
+        for precision in ('tight','strict'):
+            e=[]
+            for h in STEPS:
+                pair=[]
+                for sign in (1.,-1.):
+                    value,tmp_mf,tmp_nodes,tmp_tab=evaluate(xyz+sign*h*BOHR*v,precision)
+                    pair.append(value)
+                    del tmp_mf,tmp_nodes,tmp_tab
+                    __import__('gc').collect()
+                e.append(pair)
+            tables[precision]=e
+        stable=len({r['XC']['signature'] for r in calls})==1
+        if a.arm.startswith('pcm_'):
+            stable=stable and len({r['PCM']['signature'] for r in calls})==1
+        same_quadrature=all(q['membership_identical'] and q['weights_match'] for q in checks.values())
+        assessment=fd_check(tables['tight'],tables['strict'],
+            float(np.sum(gradients['tight']*v)),float(np.sum(gradients['strict']*v)),
+            float(np.sum(off*v)),topology_stable=stable and same_quadrature)
+        np.savez_compressed(out/'center.npz',xyz_A=xyz,dm_strict=center.make_rdm1(),
+                            full_tight=gradients['tight'],full_strict=gradients['strict'],off_strict=off)
+        if a.arm=='pcm_pruned':
+            pcm_layer_check(center,xyz,v,deadline,out)
+        write(out/'result.json',dict(provenance,status='diagnostic_complete',
+            assessment=assessment,energies=tables,response_grid_check=checks,
+            membership_stable=stable,SCF_evaluations=len(calls),gradient_evaluations=3,
+            wall_s=time.monotonic()-start,precision={'tight':[1e-11,1e-7],'strict':[1e-12,1e-8]},
+            scope='Two directions only; a changed vacuum density prevents additive solvent attribution'))
+    except Exception as exc:
+        write(out/'result.json',dict(provenance,status='censored_deadline' if isinstance(exc,TimeoutError) else 'failed',
+            error=repr(exc),SCF_evaluations=len(calls),wall_s=time.monotonic()-start))
+        raise
+
+
+def run(a):
+    from r7_common import bounded
+    p,m=load_plan(a.plan)
+    record=bounded([sys.executable,str(Path(__file__).resolve()),'native','--plan',str(p),
+                   '--case',a.case,'--arm',a.arm,'--out',str(Path(a.out).resolve())],a.out,3600)
+    dest=Path(a.out); result=dest/'result.json'
+    d=read(result) if result.exists() else {}
+    if record['execution_status']!='completed' or record['returncode']!=0 or d.get('status')!='diagnostic_complete':
+        # Keep the child's partial result; provide a terminal execution envelope.
+        write(dest.with_name(dest.name+'.terminal.json'),dict(status='deadline' if record['execution_status']=='deadline' else 'failed',
+            execution=record,partial_status=d.get('status'),plan_sha256=sha(p),case=a.case,arm=a.arm))
+        raise SystemExit(2)
+    write(dest.with_name(dest.name+'.terminal.json'),dict(status='completed',execution=record,
+        scientific_verdict=d['assessment']['full_verdict'],plan_sha256=sha(p),case=a.case,arm=a.arm))
+
+
+def collect(a):
+    if Path(a.out).exists():
+        raise FileExistsError(a.out)
+    p,m=load_plan(a.plan); ph=sha(p); rows=[]; missing=[]
+    parsed=[(f,read(f)) for f in Path(a.results).rglob('result.json')]
+    terminals=[(f,read(f)) for f in Path(a.results).rglob('*.terminal.json')]
+    for f,d in parsed:
+        if d.get('plan_sha256')==ph and (d.get('label') not in CASES or d.get('arm') not in ARMS):
+            raise ValueError('Unexpected job identity in this experiment')
+    for case in CASES:
+        for arm in ARMS:
+            hits=[(f,d) for f,d in parsed if d.get('plan_sha256')==ph and
+                  d.get('label')==case and d.get('arm')==arm]
+            terminal=[(f,d) for f,d in terminals if d.get('plan_sha256')==ph and
+                      d.get('case')==case and d.get('arm')==arm]
+            if len(hits)>1 or len(terminal)>1:
+                raise ValueError('Duplicate result; do not select a favorable repeat')
+            if not hits or hits[0][1].get('status')!='diagnostic_complete':
+                missing.append(dict(case=case,arm=arm,
+                    status=hits[0][1].get('status') if hits else 'missing',
+                    execution=terminal[0][1] if terminal else None))
+                continue
+            if (len(terminal)!=1 or terminal[0][1].get('status')!='completed' or
+                    terminal[0][1].get('execution',{}).get('returncode')!=0):
+                raise ValueError('Native completion lacks a successful bounded execution record')
+            f,d=hits[0]
+            expected=next(r for r in m['cases'] if r['label']==case)
+            if d['key']!=expected['key'] or d['geometry_sha256']!=expected['geometry_sha256']:
+                raise ValueError('Result input identity mismatch')
+            if d['SCF_evaluations']!=22 or d['gradient_evaluations']!=3:
+                raise ValueError('Incomplete native evaluation count')
+            row=dict(case=case,arm=arm,sha256=sha(f),assessment=d['assessment'],
+                response_grid_check=d['response_grid_check'],wall_s=d['wall_s'],
+                packages=d['packages'],upstream_sha256=d['upstream_sha256'],
+                terminal_sha256=sha(terminal[0][0]))
+            if arm=='pcm_pruned':
+                layer=f.parent/'layer.json'
+                if not layer.exists():
+                    raise ValueError('Completed pruned PCM arm lacks layer diagnostic')
+                row['layer']=read(layer);row['layer_sha256']=sha(layer)
+                if row['layer']['explicit_energy_evaluations']!=22 or row['layer']['gradient_evaluations']!=2:
+                    raise ValueError('Incomplete explicit PCM diagnostic')
+            rows.append(row)
+    environments={json.dumps([r['packages'],r['upstream_sha256']],sort_keys=True) for r in rows}
+    if len(environments)>1:
+        raise ValueError('Native arms used different package versions or upstream sources')
+    by={(r['case'],r['arm']):r for r in rows}
+    baseline_reproduced=None
+    if ('TEG','pcm_pruned') in by and ('EG','pcm_pruned') in by:
+        baseline_reproduced=(by['TEG','pcm_pruned']['assessment']['full_verdict']=='inconsistent'
+            and by['EG','pcm_pruned']['assessment']['full_verdict']=='consistent')
+    write(a.out,dict(base=BASE,registration=m['registration'],plan_sha256=ph,complete=not missing,
+        baseline_P33_pattern_reproduced=baseline_reproduced,
+        requested_jobs=8,completed_jobs=len(rows),missing_or_failed=missing,rows=rows,
+        authorizes_optimizer=False,authorizes_630_repolish=False,authorizes_chain_retry=False,
+        scope='Attribute only resolved contrasts. Inconclusive or failed arms remain visible.'))
+    if missing:
+        raise SystemExit(2)
+
+
+def main():
+    p=argparse.ArgumentParser(); s=p.add_subparsers(dest='command',required=True)
+    q=s.add_parser('plan');q.add_argument('--registration',required=True);q.add_argument('--out',required=True)
+    for name in ('run','native'):
+        q=s.add_parser(name);q.add_argument('--plan',required=True);q.add_argument('--case',choices=CASES,required=True)
+        q.add_argument('--arm',choices=ARMS,required=True);q.add_argument('--out',required=True)
+    q=s.add_parser('collect');q.add_argument('--plan',required=True);q.add_argument('--results',required=True);q.add_argument('--out',required=True)
+    a=p.parse_args();globals()[a.command](a)
+
+
+if __name__=='__main__':
+    main()
diff --git a/.github/workflows/r8_review.yml b/.github/workflows/r8_review.yml
new file mode 100644
--- /dev/null
+++ b/.github/workflows/r8_review.yml
@@ -0,0 +1,65 @@
+name: r8-stage-isolation
+run-name: r8/${{ inputs.plan }}
+on:
+  workflow_dispatch:
+    inputs:
+      plan:
+        description: 'Committed cloud/r8/diagnostic/plan.json'
+        required: true
+        default: 'cloud/r8/diagnostic/plan.json'
+        type: string
+permissions:
+  contents: read
+env:
+  OMP_NUM_THREADS: '4'
+  OPENBLAS_NUM_THREADS: '1'
+  MKL_NUM_THREADS: '1'
+  BLIS_NUM_THREADS: '1'
+  ZC_PCM3C: '1'
+  ZC_PCM3C_MB: '2000'
+  PYTHONPATH: 'src:scripts'
+  MPLBACKEND: Agg
+jobs:
+  diagnostic:
+    runs-on: ubuntu-latest
+    timeout-minutes: 80
+    strategy:
+      fail-fast: false
+      max-parallel: 8
+      matrix:
+        case: [TEG, EG]
+        arm: [pcm_pruned, pcm_unpruned, vacuum_pruned, vacuum_unpruned]
+    steps:
+      - uses: actions/checkout@v4
+        timeout-minutes: 3
+      - uses: actions/setup-python@v5
+        timeout-minutes: 5
+        with:
+          python-version: '3.11'
+      - name: Pinned native dependencies
+        timeout-minutes: 10
+        run: python -m pip install --retries 1 --timeout 30 pyscf==2.14.0 pyberny==0.7.0 rdkit==2026.03.6 numpy scipy pandas packaging matplotlib
+      - name: One bounded diagnostic
+        env:
+          PLAN_PATH: ${{ inputs.plan }}
+          R8_CASE: ${{ matrix.case }}
+          R8_ARM: ${{ matrix.arm }}
+        run: |
+          python - <<'PY'
+          import os,subprocess,sys
+          from pathlib import Path
+          p=Path(os.environ['PLAN_PATH']).resolve()
+          if not p.is_relative_to(Path.cwd()/'cloud'/'r8'):
+              raise ValueError('Plan must be committed under cloud/r8')
+          command=[sys.executable,'scripts/r8_diagnostic.py','run','--plan',str(p),
+                   '--case',os.environ['R8_CASE'],'--arm',os.environ['R8_ARM'],
+                   '--out','out/'+os.environ['R8_CASE']+'/'+os.environ['R8_ARM']]
+          raise SystemExit(subprocess.run(command).returncode)
+          PY
+      - uses: actions/upload-artifact@v4
+        timeout-minutes: 5
+        if: always()
+        with:
+          name: r8-${{ matrix.case }}-${{ matrix.arm }}
+          path: out
+          retention-days: 60
```
<!-- END PATCH P37 -->

### Patch P38

Files: `README.md`.

<!-- BEGIN PATCH P38 -->
```diff
diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -34,3 +34,19 @@
 python -c "from zcosmo.identity import *"   # see scripts/run_all.sh for the full chain
 bash scripts/run_all.sh
 ```
+
+## Current evidence
+
+The open workflow produced 630 profiles that passed the original Berny predicate,
+plus six separately flagged S1/S2 profiles. Resolved errors from omitted XC-grid
+response and incomplete finite-difference checks limit stationarity claims.
+The corrected-gradient calibration failed its preregistered compatibility gate;
+no corrected-gradient rollout or chain rescue is accepted. Displacement sensitivity
+does not measure geometry error, and the glycol discrepancy remains unresolved.
+Z0x was not fitted to ThermoML. Its exact infinite-dilution endpoint passed an
+independent numerical gate and is enabled with `ZC_R6_ENDPOINT=1`. Archived matched benchmark
+comparisons favor UD over open profiles for IDAC and excess enthalpy; the VLE
+interval includes zero. LLE detection and checked endpoint compositions have
+separate denominators and are not global phase-equilibrium certificates.
+See [round-7 evidence](docs/astra/round7/RESULTS.md) and
+[endpoint acceptance](docs/astra/round6/RESULTS.md).
```
<!-- END PATCH P38 -->

### Patch REG8

Files: `docs/astra/round8/REGISTRATION_PROPOSED.md`.

<!-- BEGIN PATCH REG8 -->
```diff
diff --git a/docs/astra/round8/REGISTRATION_PROPOSED.md b/docs/astra/round8/REGISTRATION_PROPOSED.md
new file mode 100644
--- /dev/null
+++ b/docs/astra/round8/REGISTRATION_PROPOSED.md
@@ -0,0 +1,126 @@
+Round-8 proposed registration. This text is not a claim that it has been adopted.
+Append the accepted text with the actual commit timestamp before new candidate
+computation. The source baseline is 58cc629df42156c0b7862710057318db0a495dbb plus
+these archived R8 helpers. The hypotheses are motivated by known R7 outcomes;
+this is neither a new ThermoML holdout nor selection by experimental error.
+
+P32 remains rejected under its actual maximum-dsp compatibility limit of 0.01.
+Neither its 0.012074 result nor the small median changes authorize its pilot or
+chain stages. The six stopped chains retain S1/S2 labels and receive no native
+budget in R8. The 630 primary profiles remain a frozen original-gradient data
+version. R8 authorizes no re-polish, new profile, profile promotion, re-scoring,
+conformer weighting, or change to a production default. P35 stays unresolved.
+P20 and P28 retain their accepted, explicitly scoped status. P28 remains opt-in
+in the current code; this registration does not change its deployment switch.
+
+P36 is E read-only bookkeeping. Reproduce the archived R7 denominators and
+recorded decisions, preserving native failures and inconclusive directions.
+Report P32 timing from its paired runs. Do not infer a count or identity of
+above-limit queries from an extrema-only JSON. Keep P34's 35 positive screens,
+four affinity-coverage failures and one unfinished native case separate. Do
+not estimate population prevalence or turn fixed-displacement sensitivity into
+an error estimate at the corrected minimum. Historical files remain unchanged.
+
+P37 is one final A stage-isolation diagnostic, not a relaxed referee or an
+optimizer trial. Freeze exactly the archived P33 TEG bond-3-4 direction that
+was resolved inconsistent with full response and the EG bond-2-3 consistent
+control. They are targeted diagnostic identities, not a random sample. Use
+their existing full-precision unit-L2 Cartesian vectors and exact generating
+geometry hashes from cloud/r7/referee and docs/astra/round7/data/referee.
+No new conformer, reorientation, random direction or step-size selection is
+allowed. Freeze the plan and code hashes before native output.
+
+Cross PCM on/off with the existing angular pruning/None, yielding four arms
+per case and eight jobs in total. Use BP86/def2-SVP, the existing DF auxiliary
+basis, XC grid level 2, and, when attached, C-PCM epsilon 1e9, Lebedev 17 and
+project radii. The no-PCM arms are genuine vacuum controls at the same nuclear
+coordinates, not claims that their electron density matches the PCM density.
+Check the actual runtime small_rho_cutoff is zero. An unexpected nonzero value
+is an environment mismatch and stops the job; do not silently force it to zero.
+Angular pruning and density-based point removal are different settings.
+
+Pin PySCF 2.14.0 and pyberny 0.7.0 using normalized package versions. Record
+NumPy/SciPy versions and the loaded upstream source hashes. Native jobs use
+four OpenMP threads, one BLAS thread, 4000 MB nominal PySCF memory and a 2000 MB
+PCM integral cache. No tighter integral threshold, denser radial grid, alternative
+SCF solver, modified PCM switching, or other functional/basis is substituted.
+
+Per arm compute tight and strict center SCFs, with (conv_tol,conv_tol_grad)
+equal to (1e-11,1e-7) and (1e-12,1e-8), respectively. Compute tight/full-response,
+strict/full-response and strict/off center gradients, retaining DF auxiliary
+and, where present, PCM derivatives. Compute both signs of the fixed Bohr
+ladder 0.016,0.008,0.004,0.002,0.001 at each precision. All five energy pairs
+are required; the finest Richardson estimate is the reference, not a selected
+best-agreement step. This is exactly 22 SCF calls and three full molecular
+gradient calls per completed arm.
+
+Retain P33's tau=1e-5 Eh/Bohr and its unchanged finite-resolution decision rule.
+The uncertainty indicator is the difference of the finest strict Richardson
+estimates plus tight/strict, center-gradient and roundoff indicators. Require
+its value at most tau/4 and stabilization. Consistency requires discrepancy
+plus indicator at most tau; inconsistency requires discrepancy minus indicator
+greater than tau; other outcomes are inconclusive. This is not a rigorous
+interval enclosure. No outcome is promoted by increasing uncertainty or changing
+a threshold. The old P33 and P30 decisions are never overwritten or re-gated.
+
+Track retained XC points by generating atom and atomic-template ordinal,
+ignoring zero-weight padding, and PCM points by generating atom and Lebedev
+ordinal. Equal point counts alone do not establish identical membership. A
+membership change along a ladder makes its assessment inconclusive. Compare
+the SCF quadrature with the full-response quadrature at both centers, requiring
+identical node membership and matching weights (absolute 1e-12, relative 1e-10).
+A discrepancy is recorded and also makes the derivative verdict inconclusive.
+These are quadrature representation checks, not universal AO-screening proofs.
+
+In each PCM/pruned arm additionally test the explicit PCM partial derivative
+at the strict center. Freeze the AO density coefficient matrix P0, retain the
+same AO labels and basis, move the atom-centered basis and PCM surface with
+the geometry, and solve the surface charges anew. Do not set frozen=True.
+Compare the derivative of E_PCM(R,P0) with PCM.grad(P0). The off-center overlap
+electron count can change because the basis moves; report it, never renormalize
+P0. This derivative is not the PCM energy derivative along a relaxed SCF curve
+and is not a fixed physical real-space density derivative.
+
+Use stock PCM and the existing CachedPCM3c independently at the center and the
+ten displacements: 22 explicit PCM energy calls and two PCM gradient calls per
+case. Require linear-solve relative residual at most 1e-10. Cache/stock parity
+is an E diagnostic, maximum center/displaced energy difference below 1e-9 Eh and
+maximum center gradient difference below 1e-8 Eh/Bohr. Apply the unchanged
+finite-resolution ladder calculation to the layer, retaining its interpretation
+as two float64 implementations, not an independent high-precision oracle.
+No cache implementation is changed or newly accepted by this test.
+
+The budget is eight one-hour four-core native jobs, with a 3400-second internal
+deadline and a 3600-second process-group deadline. Maximum totals are 176 SCF
+calls, 24 molecular gradients, 44 explicit PCM energy calls and four PCM gradients.
+Installation, planning and artifact transfer are outside the native-time count;
+no paid resource or guarantee of available account quota is implied. No retry,
+continuation, new optimizer history or budget extension is authorized. Reuse
+no prior native result as an unlabelled new observation. Preserve every failed
+or missing job. Scientific negatives can complete; execution failures must
+propagate a nonzero status and receive a terminal execution record. Collection
+requires one result and bounded execution record per requested identity.
+
+First require the PCM/pruned baseline to reproduce the TEG inconsistency and
+the EG consistency before interpreting another arm as removing that discrepancy.
+Failure to reproduce is informative but does not demonstrate a fix.
+Interpret only resolved contrasts. An unpruned-arm improvement is evidence
+of dependence on angular quadrature, not proof that all pruning is a bug or
+that the new energy is physically more accurate. A vacuum/PCM contrast alone
+cannot isolate an additive solvent error because the SCF density changes.
+A resolved explicit-layer failure localizes an issue to the PCM partial
+calculation at this density and surface; it does not by itself identify a
+particular switching term. A passing layer and failing total derivative leaves
+SCF, other derivative terms or integral/quadrature screening as possibilities.
+A cache/stock discrepancy is reported before making a physical attribution.
+
+Neither a pass nor a favorable contrast authorizes corrected-gradient defaults,
+a 630-profile re-polish, six-chain jobs, an ensemble or experimental scoring.
+If the fixed contrasts remain inconclusive or fail operationally, archive the
+unresolved mismatch and close this diagnostic budget. Reopening would require
+new independent evidence, auditable inputs or a source-level correction, then
+a separate registration. There is no automatic next parameter sweep.
+
+P38 is E reporting only. Append the supplied short README status, linking the
+archived evidence. Preserve distinctions between original-predicate convergence,
+full-energy stationarity, numerical acceptance and experimental accuracy.
```
<!-- END PATCH REG8 -->

## README-ready closing status

The open workflow produced 630 profiles that passed the original Berny predicate,
plus six separately flagged S1/S2 profiles. Resolved errors from omitted XC-grid
response and incomplete finite-difference checks limit stationarity claims.
The corrected-gradient calibration failed its preregistered compatibility gate;
no corrected-gradient rollout or chain rescue is accepted. Displacement sensitivity
does not measure geometry error, and the glycol discrepancy remains unresolved.
Z0x was not fitted to ThermoML. Its exact infinite-dilution endpoint passed an
independent numerical gate and is enabled with `ZC_R6_ENDPOINT=1`. Archived matched benchmark
comparisons favor UD over open profiles for IDAC and excess enthalpy; the VLE
interval includes zero. LLE detection and checked endpoint compositions have
separate denominators and are not global phase-equilibrium certificates.
See [round-7 evidence](docs/astra/round7/RESULTS.md) and
[endpoint acceptance](docs/astra/round6/RESULTS.md).

