Z-COSMO round 12: explain prediction changes without selecting a new profile version

Reference: `Victor-Liang-ChE/zcosmo`, `main = a93a1c9abbec32e0af7ff259a8db6fa550bb34a9`. This report follows the round-12 prompt, the complete round-11 report and the recorded R10/R11 outcomes. The branch was rechecked before delivery and still points to this commit. The patches are prospective. A favorable explanatory result does not adopt a profile. The numerical-gradient campaign stays closed and the 630 primary plus six S1/S2 files remain frozen. [S1–S5]

| Rank | ID | Target and class | Mechanism and expected cost | Expected saving / speed-up | Effort |
|---:|---|---|---|---|---|
| 1 | P46 | `r12_review.py`: `freeze`, `one_model_job`, `run_factorial`, `check`; A explanatory input substitution with E integrity checks | Reuse the frozen C profiles. Evaluate the P21 area/volume/shape cube on the four glycol-solvent subsets with unchanged open solutes. Core: 1,269 P28 requests. Historical-anchor gate: 282 requests. Zero new QC. | No solver acceleration claimed. Avoid repeating R11's 24 single points, already completed in 594 s, or extending to unrelated model/phase tables. | Moderate |
| 2 | P47 | `r12_analysis.py`: `regional_panel`, `vector_regions`; E read-only analysis | Partition all twelve members' archived profile differences by fixed sigma regions and existing HB channel. Zero QC and zero model calls. | Reuse existing 153-bin arrays; no new surface calculation, fitting or parameter sweep. | Low |
| 3 | P48 | README and dated P35 annotation; E reporting | State the EG/DEG/TEG tail finding and tetraEG exception, preserving the unresolved whole-profile/liquid claims. | No computational speed-up. Prevents spending another native campaign to answer a question the archive already settles within its scope. | Low |
| Shared | H12, REG12 | Arithmetic/tests and proposed registration | Fixed input identities, private-output rules and exact accounting. | No additional physical experiment. | Low |

The brief's ranking criterion is decision value per effort here, not an invented probability of improving experimental accuracy. P46 addresses the missing prediction-level observation directly. P47 is less expensive but cannot substitute a histogram norm for a nonlinear activity calculation. Their savings overlap and must not be added. P46's actual model time is `sum_j(worker_time_j)` plus orchestration, bounded at 7,200 seconds on the existing Mac. That is an allocation, not a forecast. R11's 594 seconds is an archived measurement, not a measurement from this review. [S2, S4]

The new scientific calculation is worth running. It can answer whether the coordinate-input intervention that moved the tails also changes the measured glycol-solvent IDAC errors. The profiles already exist, so another SCF, optimization or conformer search adds nothing necessary to this question. A negative result would be useful: large tail changes need not account for the prediction deficit. There is no requirement that the errors decrease.

P46 is scoring against ThermoML. It uses experimental ln gamma values to compute bias and absolute error, so calling it “only a diagnostic” does not exempt it from preregistration. The supplied registration explicitly records a retrospective explanatory evaluation, motivated by results already inspected in R4–R11. It is not a fresh test set, a fitted improvement, or evidence accepting a new production geometry. The C input is frozen before these scores, with no selection among conformers or favorable subsets after evaluation. [S1, S4]

Use exactly the original P21 observations for the four fixed R11 glycol keys. Their expected denominators are below. Preparation checks the original 332-row, fourteen-solvent archive and all of its per-pair input receipts, then extracts these keys without rebuilding rows from a newer benchmark export. The other 191 observations remain in the archive audit; they receive no new C predictions. This is not a new 332-row C score. [S6]

| Solvent | Fixed key | Original P21 rows |
|---|---|---:|
| Ethylene glycol | `LYCAIKOWRPUZTN-UHFFFAOYSA-N` | 9 |
| Diethylene glycol | `MTHSVFCYNBDYFN-UHFFFAOYSA-N` | 108 |
| Triethylene glycol | `ZIBGPFATKBEMQZ-UHFFFAOYSA-N` | 17 |
| Tetraethylene glycol | `UWHCKJMYHZGTIT-UHFFFAOYSA-N` | 7 |
| Total | Exact keys, unchanged solutes and observations | 141 |

TetraEG is retained despite its different R11 attribution. Names are not join keys: the separate one-row “1,2-dihydroxyethane” entry in P21 is not silently merged into the nine-row EG entry. A different identity/count in the original files stops preparation. The patch does not invent the missing archive's row identifiers.

For each row, let O be the original P21 open solvent profile, C the archived R11 `RU` profile, and U the original UD solvent profile. The solute remains the exact original P21 open solute in every calculation. U therefore means an UD-solvent substitution, not an all-UD mixture. O is deliberately the historical P21 input, not whichever open profile is easiest to find today. Its byte hash must match the original receipts. The current production files are protected independently using the R11 plan. [S5, S6]

The bit order remains area, cavity volume, normalized shape. With `s_O=O/sum(O)` and `s_C=C/sum(C)`, corner `(a,v,s)` uses

\[
 A_a=(1-a)A_O+aA_C,\qquad
 V_v=(1-v)V_O+vV_C,\qquad
 p_{avs}=A_a[(1-s)s_O+s\,s_C].
\]

Original open metadata is retained in this cube, while its area and volume fields are updated. The chemical dielectric and London tables remain unchanged. For Z0x these eight corners exhaust the chosen A/V/shape substitution. The `111` corner has C's area, volume and profile; no separate ninth C replay adds another independent factor. The extra anchor is the actual U solvent file. These are counterfactual inputs, not deployable mixed recipes. [S6, S8]

The primary evaluation uses the accepted P28 endpoint for every O, C-cube and U calculation, explicitly setting `ZC_R6_ENDPOINT=1`. This is important because historical P21 used the older endpoint. Subtracting an old O error from a new exact-endpoint C error would mix two interventions. Each primary O-to-C error comparison is endpoint-consistent. The report also carries the old-to-P28 O and U MAE changes on the same rows as a separate bridge. It never overwrites P21. [S6, S8]

There are eight corners and one U anchor per row: `9 × 141 = 1,269` requests. The preliminary gate reruns only historical O and U anchors on those rows with `ZC_R6_ENDPOINT=0`: `2 × 141 = 282`. Every original P21 intermediate corner is checked against its own archived per-pair output and input hashes, without another model run. This keeps the scientific cube complete while avoiding unnecessary recalculation of all nine historical corners on all 332 observations. The maximum is therefore `1,269 + 282 = 1,551` requested `lngamma_inf` evaluations, not 1,551 SCF calls or segment iterations.

The historical-anchor gate requires all 282 values finite and matched by observation identity, with maximum absolute replay error below `1e-8`. The stored P21 `111` and full-U columns must agree below `1e-10`. A failure blocks all C-scoring jobs. It does not authorize changing the solver, weakening a tolerance or falling back to another profile snapshot. The uncomputed historical intermediate corners are not described as newly reproduced.

One fresh subprocess handles one ordered pair and one corner, retaining the original row order within that pair. Both requested profile overrides must resolve explicitly, including the unchanged open solute. This prevents a missing solute from silently falling back to UD, or a process-global profile cache from retaining the previous corner. Experimental response values do not enter model construction or its query arguments. The model receives only its frozen chemical inputs and temperature.

The job count is `11 × N_target_pairs`, determined from the actual archive. The synthetic test has four target pairs and therefore 44 jobs; that is not the real Mac job count. A worker has a 120-second process-group deadline, within a 7,200-second serial model-run allocation. An additional five seconds is only a kill/accounting allowance. Closing integrity and aggregation time is recorded separately. No retry, alternative output run, cloud job or paid resource is introduced. A permanent claim binds each private plan to one execution.

Requested identities and failed outcomes are preserved. A nonfinite new corner blocks the complete-panel aggregate rather than shrinking to a favorable finite intersection. Completed values and terminal receipts remain private. The checker independently reconstructs the saved summary and verifies hashes without calling the activity model again. These are accounting/acceptance conditions for a completed explanatory experiment, not accuracy gates for adopting C. The original E 25-molecule/2,302-row gate is neither performed nor claimed satisfied.

For experimental value `y_i`, write the three consistent-endpoint predictions as `y_O,i`, `y_C,i` and `y_U,i`. The direct answer is

\[
 \Delta_{O\to C}^{\rm MAE}
 =\frac{1}{n}\sum_i\left(|y_{O,i}-y_i|-|y_{C,i}-y_i|\right).
\]

A positive value is the absolute error removed by this frozen intervention on these inspected rows; a negative value is deterioration. Report the residual comparator gap `MAE_C−MAE_U` and check

\[
 (\mathrm{MAE}_O-\mathrm{MAE}_C)+(\mathrm{MAE}_C-\mathrm{MAE}_U)
 =\mathrm{MAE}_O-\mathrm{MAE}_U.
\]

The signed recovery ratio is shown only when the denominator `MAE_O−MAE_U` exceeds `1e-6`. It is not clipped to zero or one. Overshoot and degradation remain visible; a nearly zero comparator gap makes the fraction unavailable. A tail fraction such as R11's 79–87% is never inserted into this equation.

Apply the existing P21 `shapley_three` twice. The first cube contains predictions. The second contains negative absolute errors at the same corners. If \(f_i(b)\) is a corner prediction, then

\[
 \sum_j\phi_{j,i}^{\rm pred}=f_i(111)-f_i(000),\qquad
 \sum_j\phi_{j,i}^{\rm gain}=|f_i(000)-y_i|-|f_i(111)-y_i|.
\]

Both identities are checked for each row and in the aggregate. Taking the absolute value of a prediction Shapley contribution does not yield its contribution to MAE reduction. For example, moving a prediction from `−1` to `+1` with an observed value zero changes the prediction by two and removes no absolute error. Interaction effects are distributed by the stated Shapley convention; they do not become independent physical mechanisms merely because the algebra sums exactly.

The public error summary contains per-solvent and pooled MAE/bias, error reductions and the A/V/shape contributions to absolute-error reduction. Prediction-cube details and prediction Shapley values stay private. Equal-solvent mean MAE is a declared secondary summary because DEG supplies `108/141`, about 77%, of the pooled observations. The code does not select whichever weighting looks better. No post-selection confidence interval or generalization claim is attached to this retrospective panel.

| Possible outcome | Permitted conclusion |
|---|---|
| C reduces glycol errors and the error-reduction Shapley term is mainly shape | The frozen coordinate-derived profile substitution explains that part of the inspected IDAC deficit through the stated model. It does not validate C for production or establish the liquid conformation. |
| C moves the tails but leaves errors similar or worse | Tail attribution did not translate into the expected prediction benefit on these rows. Retain the unfavorable result. |
| A/V contributions or cancellations matter for errors | Report them. P21's O-to-U shape dominance does not require O-to-C to have the same decomposition. |
| Archive, coverage or execution gate fails | No complete P46 result. Preserve the original requested denominator and the failure record. P47 can still run independently. |

Only `public-errors.json`, after operator review, is eligible for publication. It is an explicit allowlist, not a recursive export of the private summary. No dense profiles, row predictions, coordinates, private paths, per-member regional distributions or logs enter it. The code uploads nothing. The actual ThermoML explanatory results remain unavailable until the private Mac run is executed.

The R11 result should not be recast as “there is no shape difference.” Its normalized contrasts were below a deliberately conservative background threshold. The observed scale `eta=0.359` came from the registered maximum over control total/coordinate norms, the repeat-drift term and the floor. It was not defined simply as the maximum method norm. After the cross, U−C is a genuine same-coordinate comparison of the two method bundles, and that norm reaches about 0.37 in the controls. These facts are consistent: a large, reproducible method difference can make the background large without being numerical noise. [S2, S5]

The whole-profile labels remain unchanged. It would be inappropriate to remove water, lower eta, subtract a control vector or use a favorable tail-only classification to turn those old results into whole-profile passes. Equally, a large background does not make a `0.2` shape difference physically irrelevant. L1 gives all bins equal weight; activity coefficients depend nonlinearly on the location and channel of the redistributed area.

P47 uses all twelve private R11 members, with U, archived A, fresh R and crossed C. It calculates `D=U−R`, `G=C−R`, `M=U−C` and repeat drift `R−A`, first for unnormalized area profiles, then after normalizing each input by its own area. Every array entry goes into exactly one of these fixed regions, crossed with the existing NHB, OH and OT channels:

| Region | Sigma condition, e/Å² | Number of bins per channel |
|---|---|---:|
| Negative tail | `sigma <= −0.010` | 16 |
| Negative shoulder | `−0.010 < sigma <= −0.005` | 5 |
| Centre | `abs(sigma) < 0.005` | 9 |
| Positive shoulder | `0.005 <= sigma < 0.010` | 5 |
| Positive tail | `sigma >= 0.010` | 16 |

Boundaries use integer millithresholds on the fixed output grid, avoiding a floating-point ambiguity at `±0.010`. Each of the fifteen region/channel cells reports signed mass change, L1 contribution, its share of total L1 and its signed first moment. The signed totals and L1 contributions must sum to the full-vector quantities within the implemented `1e-12` scaled bound. A zero norm yields null shares, not division by zero. These are exhaustive descriptive partitions, not fifteen new hypothesis tests.

The parser convention places donor-side OH/OT contributions at negative sigma and acceptor-side contributions at positive sigma. A signed NHB entry is still NHB. The low-sigma centre is not an identification of “nonpolar molecules.” The post-HB channel split and charge convention are unchanged. In particular, P47 does not reconstruct raw net charge or extreme tesserae from a normalized, averaged profile. [S7]

There is another useful exact comparison. For a difference \(d_{cb}\), where c indexes channel and b sigma bin,

\[
 L_{153}=\sum_{cb}|d_{cb}|,\qquad
 L_{51}=\sum_b\left|\sum_c d_{cb}\right|,\qquad
 L_{153}-L_{51}\ge0.
\]

A large last quantity identifies channel cancellation hidden when plotting only the total sigma profile. If all channels at a bin change with the same sign, there is no cancellation there. This does not assign an HB energy or an ln gamma error to that bin. P47 also checks `D=G+M`; the norms themselves need not telescope because opposing changes cancel.

A method difference concentrated in the centre would explain why normalized L1 can be large while the tail-area difference is small. A donor/acceptor asymmetry would locate which side carries the discrepancy. A large channel-cancellation term would show that a total-profile plot hides HB-class redistribution. All are conditional readings of the proposed output. None has been measured here. The regional tables remain private on the Mac; no new classification or public per-bin dataset is created.

The broad wording “the glycol gap is mainly the stored conformation” is too broad. It omits tetraEG, conflates tail area with the complete profile and suggests a liquid-state explanation. The proposed dated wording is:

“Under the registered ordered open-method cross, the raw, averaged and final polar-tail gaps for ethylene, diethylene and triethylene glycol are mainly due to their stored coordinate inputs. Tetraethylene glycol is an exception: its raw-tail gap is mainly method, while its other tail contrasts are small under the registered scale. No whole-profile attribution label passed. The liquid conformer distribution and the physical explanation of the prediction discrepancy remain unresolved. These results do not identify the UD conformation as correct, adopt crossed profiles, or reopen the numerical-gradient campaign.”

Here coordinate input includes hydrogen positions and laboratory orientation as well as conformation. R11 did not isolate a torsion or prove an intramolecular hydrogen-bond mechanism. The R10 contact-angle rule was not met, and it remains unchanged. The public provenance notice describes empirical conformation revision at database level, without identifying which individual glycol members were revised. No stronger member-specific claim is needed. [S2, S3, S5]

Run the bounded P46 explanation and P47 accounting, then archive the outcome whether favorable or unfavorable. No new native experiment is recommended in this round. The profile-tail question has a useful, restricted answer already. P46 can connect that answer to inspected prediction errors, but cannot turn it into a phase-equilibrium conformer rule.

A phase-dependent free-energy rule is physically defensible in principle, as discussed in R11. Its cheap part is minimizing a finite-state functional once audited basin free energies and transfer conventions are supplied. Those inputs are the difficulty here. The current conductor single points do not contain complete basin entropy, low-barrier torsional partitions, independently converged basin populations or a controlled common reference across phases. R11's 24 single points taking 594 s is not a cost estimate for obtaining those missing quantities. [S3, S4]

A small calculation choosing the lowest current conductor-energy conformer would be affordable but would answer a different question. It would not establish the neat-liquid and infinite-dilution populations, nor validate replacing a phase-dependent ensemble with one profile. Published COSMO conformer treatments show that phase-dependent approaches exist; they do not validate an inexpensive fit-free Z0x implementation on this panel. [U1]

There is consequently no validated, costed full-class free-energy protocol in the present record that should be accepted under this round's free-compute constraints. This is not a claim that such a calculation is impossible. It is a recommendation against allocating another native campaign on the strength of an explanatory tail result. A future proposal would need a separately preregistered, bounded route to the missing physical validation, applied beyond just the glycols with unfavorable benchmark errors. R12 assigns zero native or ensemble budget.

The P21 code already supplies the required factorial and exact Shapley operation; duplicating an activity solver is unnecessary. Its process isolation and input receipts are valuable and are retained. The new code adds the distinct absolute-error cube instead of interpreting a signed prediction shift as an error improvement. It explicitly isolates P28 from the historical endpoint and refuses profile fallback. These are safeguards, not evidence that P21's recorded values were wrong. [S6]

The R11 results correctly distinguish tail labels from whole-profile labels and explicitly say the activity model was not run. No numerical table needs rewriting. The README still stops at the descriptive R10 comparison, so P48 appends the actual R11 cross result and the tetraEG exception. The earlier P30/P32 failures and R8/R9 closure remain. The P35 file receives a dated annotation rather than deletion of its historical unresolved state. [S2, S9]

Executed in this review: Git-blob verification of the reconstructed relevant source subset, the current README/P35 files and the complete mounted R11 report; independent and combined application of all four patches; Python compilation and command-help checks; 26 new portable tests, the 22 R11 tests and the 20 R10 tests, including runs on the combined applied tree. The new suite tests all eight hybrid corners, both Shapley identities, exact band boundaries, channel cancellation, preserved labels, private-output allowlisting, altered inputs, missing values, an actual process-group timeout and a synthetic end-to-end runner/checker. A failed historical anchor blocks every C job. A single nonfinite exact corner retains 1,269 requested predictions and blocks the complete score. The synthetic successful runner accounts for all 1,551 planned requests. Those are mock model calls, not actual Z0x evaluations.

Not executed: the real P21 archive audit, Mac preparation/registration ancestry against the user's checkout, P46 ThermoML scoring, the real R11 regional tables, any new quantum calculation, or a repository/production write. The runtime has no PySCF; installation was not attempted because no native work is proposed and actual UD-backed analysis is Mac-only. The local source is a verified relevant-file reconstruction, not a full clone. The tests do not establish that the private Mac assets are available or that any actual prediction improves. The exact commands below are the remaining acceptance path.

The commands below apply the four patches, run software checks, and commit the prospective registration before either private plan is generated. They use the existing Mac environment from R11, without installing or upgrading dependencies. `REPORT` is the saved Markdown report. `R11_PLAN` and `R11_RUN` default to the locations prescribed in R11, not to newly invented copies. The code verifies that the actual old plan and completed run exist and pass their original checks.

```bash
# Run in a clean Mac checkout at the reviewed main.
set -euo pipefail
umask 077
export BASE=a93a1c9abbec32e0af7ff259a8db6fa550bb34a9
: "${REPORT:?Set REPORT to the saved ZCOSMO_ROUND12_REPORT.md}"
export REPORT
export PATCHDIR="${PATCHDIR:-${TMPDIR:-/tmp}/zc-r12-patches}"
export PYTHONPATH=src:scripts
export MPLBACKEND=Agg

test "$(git rev-parse HEAD)" = "$BASE"
git diff --quiet
git diff --cached --quiet
python - <<'PY'
import os,re
from pathlib import Path
text=Path(os.environ['REPORT']).read_text()
out=Path(os.environ['PATCHDIR']);out.mkdir(parents=True,exist_ok=False)
for name in ('H12','P46P47','P48','REG12'):
    pattern=r'<!-- BEGIN PATCH '+name+r' -->\s*```diff\n(.*?)\n```\s*<!-- END PATCH '+name+r' -->'
    found=re.findall(pattern,text,re.S)
    if len(found)!=1:raise ValueError('Missing or duplicate patch: '+name)
    (out/(name+'.patch')).write_text(found[0]+'\n')
PY
for name in H12 P46P47 P48 REG12; do
  git apply --check "$PATCHDIR/$name.patch"
  git apply "$PATCHDIR/$name.patch"
done
python scripts/r12_selftest.py
python scripts/r11_selftest.py
python scripts/r10_selftest.py
python -m py_compile scripts/r12_analysis.py scripts/r12_review.py scripts/r12_selftest.py

python - <<'PY'
from pathlib import Path
from datetime import datetime,timezone
p=Path('PREREGISTRATION.md')
marker='R12-P46-P47-P48: private explanatory scoring and regional accounting'
old=p.read_text()
if marker in old:raise ValueError('R12 already appears registered; do not duplicate it')
text=Path('docs/astra/round12/REGISTRATION_PROPOSED.md').read_text()
stamp=datetime.now(timezone.utc).isoformat()
p.write_text(old.rstrip()+'\n\nRound 12 prospective registration recorded '+stamp+
             '. The following design is adopted before new plans or outputs.\n\n'+text)
PY
git add scripts/r12_analysis.py scripts/r12_review.py scripts/r12_selftest.py \
  docs/astra/round12/REGISTRATION_PROPOSED.md README.md \
  docs/astra/round7/GLYCOL_STATUS.md PREREGISTRATION.md
git commit -m "Register R12 private explanatory scoring and regional accounting"
export R12_REG="$(git rev-parse HEAD)"
export R11_PLAN_COMMIT="$(git rev-parse '1ecca25^{commit}')"
export R11_PLAN="${R11_PLAN:-$HOME/zc-r11-cross-20261007/plan/plan.json}"
export R11_RUN="${R11_RUN:-$HOME/zc-r11-cross-20261007/native}"
export R12_PRIVATE="${R12_PRIVATE:-$HOME/zc-r12-explanations-20261007}"
test -f "$R11_PLAN"
test -f "$R11_RUN/summary.json"
mkdir -p "$R12_PRIVATE"
chmod 700 "$R12_PRIVATE"
```

P47 can be executed independently, including when the original P21 scoring archive is unavailable. This block commits only a plan digest. Both the regional output and its timing log remain private. Re-running the `check` command is allowed because it reads saved data and performs no model evaluations; re-running a claimed analysis into another output location is refused.

```bash
set -euo pipefail
umask 077
: "${R12_REG:?Run the registration block first}"
python scripts/r12_review.py freeze --task regions \
  --registration "$R12_REG" \
  --r11-plan "$R11_PLAN" --r11-plan-commit "$R11_PLAN_COMMIT" \
  --r11-run "$R11_RUN" --out "$R12_PRIVATE/regions-plan" \
  > "$R12_PRIVATE/regions-freeze.log" 2>&1
cp "$R12_PRIVATE/regions-plan/PLAN_SHA256.txt" \
  docs/astra/round12/REGIONS_PLAN_SHA256.txt
git add docs/astra/round12/REGIONS_PLAN_SHA256.txt
git commit -m "Freeze R12 private regional-analysis plan digest"
export R12_REGIONS_COMMIT="$(git rev-parse HEAD)"
/usr/bin/time -p python scripts/r12_review.py regions \
  --plan "$R12_PRIVATE/regions-plan/plan.json" \
  --plan-commit "$R12_REGIONS_COMMIT" --out "$R12_PRIVATE/regions" \
  > "$R12_PRIVATE/regions-run.log" 2>&1
python scripts/r12_review.py check \
  --plan "$R12_PRIVATE/regions-plan/plan.json" \
  --plan-commit "$R12_REGIONS_COMMIT" --run "$R12_PRIVATE/regions" \
  > "$R12_PRIVATE/regions-check.log" 2>&1
# Inspect regions-private.json locally. Do not commit or upload it.
```

For P46, `P21_RUN` must point to the original P21 factorial directory containing `factorial_rows.csv`, `summary.json` and the `pair-*` folders. `P21_OPEN` must be the original open-profile snapshot used by that run. These paths are not available in the public checkout, so the commands require the real asset locations rather than guessing them. A current profile with different metadata bytes is not silently substituted. The R11 plan supplies the private UD directory and the C profiles.

```bash
set -euo pipefail
umask 077
: "${R12_REG:?Run the registration block first}"
: "${P21_RUN:?Set P21_RUN to the original P21 factorial output directory}"
: "${P21_OPEN:?Set P21_OPEN to its original open-profile snapshot}"
python scripts/r12_review.py freeze --task factorial \
  --registration "$R12_REG" \
  --r11-plan "$R11_PLAN" --r11-plan-commit "$R11_PLAN_COMMIT" \
  --r11-run "$R11_RUN" --p21-run "$P21_RUN" \
  --p21-open-profiles "$P21_OPEN" --out "$R12_PRIVATE/factorial-plan" \
  > "$R12_PRIVATE/factorial-freeze.log" 2>&1
cp "$R12_PRIVATE/factorial-plan/PLAN_SHA256.txt" \
  docs/astra/round12/FACTORIAL_PLAN_SHA256.txt
git add docs/astra/round12/FACTORIAL_PLAN_SHA256.txt
git commit -m "Freeze R12 private P21 explanatory-scoring plan digest"
export R12_FACTORIAL_COMMIT="$(git rev-parse HEAD)"

# Exactly one claimed execution. A nonzero status must not trigger a retry.
set +e
/usr/bin/time -p python scripts/r12_review.py run \
  --plan "$R12_PRIVATE/factorial-plan/plan.json" \
  --plan-commit "$R12_FACTORIAL_COMMIT" --out "$R12_PRIVATE/factorial" \
  > "$R12_PRIVATE/factorial-run.log" 2>&1
rc=$?
set -e
if [ "$rc" -ne 0 ]; then
  printf 'P46 ended with status %s. Retain the private failure receipts; do not rerun.\n' "$rc"
  exit "$rc"
fi
python scripts/r12_review.py check \
  --plan "$R12_PRIVATE/factorial-plan/plan.json" \
  --plan-commit "$R12_FACTORIAL_COMMIT" --run "$R12_PRIVATE/factorial" \
  > "$R12_PRIVATE/factorial-check.log" 2>&1
python - <<'PY'
import json,os
from pathlib import Path
root=Path(os.environ['R12_PRIVATE'])/'factorial'
s=json.loads((root/'summary.json').read_text())
print(json.dumps({k:s[k] for k in ('attempted_model_calls','model_run_wall_s',
    'closing_check_wall_s','driver_wall_s')},indent=2))
p=json.loads((root/'public-errors.json').read_text())
if not p['complete'] or p['adopted']:raise ValueError('Not a complete explanatory-only result')
print(json.dumps(p,indent=2))
PY
# Review public-errors.json before any separate publication step.
# No private plan, log, dense profile, row prediction or regional table enters Git.
```

The four following diffs are independent against the pinned main. H12 and P46P47 share imports, so apply both before testing. The combined P46P47 patch supplies separate scoring and regional commands, not an obligation to run scoring before the regional audit. REG12 is proposed text; the preceding explicit commit is what registers the design.

<!-- BEGIN PATCH H12 -->
```diff
diff --git a/scripts/r12_analysis.py b/scripts/r12_analysis.py
new file mode 100644
--- /dev/null
+++ b/scripts/r12_analysis.py
@@ -0,0 +1,206 @@
+"""R12 arithmetic. Retrospective explanations do not authorize profile adoption."""
+from __future__ import annotations
+import numpy as np
+from r4_glycols import shapley_three
+from r10_sources import DATA
+
+CORNERS = tuple(f'{i:03b}' for i in range(8))
+GLYCOLS = {
+    'LYCAIKOWRPUZTN-UHFFFAOYSA-N': ('ethylene_glycol', 9),
+    'MTHSVFCYNBDYFN-UHFFFAOYSA-N': ('diethylene_glycol', 108),
+    'ZIBGPFATKBEMQZ-UHFFFAOYSA-N': ('triethylene_glycol', 17),
+    'UWHCKJMYHZGTIT-UHFFFAOYSA-N': ('tetraethylene_glycol', 7),
+}
+CHANNELS = ('NHB', 'OH', 'OT')
+BANDS = ('negative_tail', 'negative_shoulder', 'centre',
+         'positive_shoulder', 'positive_tail')
+SIG = np.arange(-25, 26, dtype=float)/1000
+PARITY_TOL = 1e-8
+IDENTITY_TOL = 1e-10
+
+
+def require(ok, message):
+    if not ok:
+        raise ValueError(message)
+
+
+def finite(x):
+    a = np.asarray(x, dtype=float)
+    require(np.isfinite(a).all(), 'Nonfinite arithmetic input')
+    return a
+
+
+def profile(x):
+    a = finite(x)
+    require(a.shape == (3, 51) and (a >= 0).all() and a.sum() > 0,
+            'Expected a positive-total, nonnegative 153-bin area profile')
+    return a
+
+
+def hybrid(open_bins, open_meta, other_bins, other_meta, corner):
+    """Same P21 bit order: area, volume, separately normalized 153-bin shape."""
+    require(corner in CORNERS, 'Unknown factorial corner')
+    o, c = map(profile, (open_bins, other_bins))
+    for m in (open_meta, other_meta):
+        require(np.isfinite(m['volume [A^3]']) and m['volume [A^3]'] > 0,
+                'Invalid cavity volume')
+    ia, iv, ip = map(int, corner)
+    area = float(c.sum() if ia else o.sum())
+    shape = c/c.sum() if ip else o/o.sum()
+    meta = dict(open_meta)
+    meta.update({'area [A^2]': area,
+                 'volume [A^3]': other_meta['volume [A^3]'] if iv else open_meta['volume [A^3]'],
+                 'source': 'R12 explanatory counterfactual; never adopted'})
+    return area*shape, meta
+
+
+def band_masks():
+    # Integer millithresholds avoid arange/linspace ambiguity at +/-0.005, 0.010.
+    k = np.arange(-25, 26)
+    masks = (k <= -10, (k > -10) & (k <= -5), abs(k) < 5,
+             (k >= 5) & (k < 10), k >= 10)
+    require(np.array_equal(np.sum(masks, axis=0), np.ones(51, dtype=int)),
+            'Bands must partition the entire output grid exactly once')
+    return dict(zip(BANDS, masks))
+
+
+def vector_regions(d):
+    """Additive L1 accounting, not an interaction-energy decomposition."""
+    d = finite(d)
+    require(d.shape == (3, 51), 'Wrong difference shape')
+    norm = float(abs(d).sum())
+    cells = []
+    for band, mask in band_masks().items():
+        for j, channel in enumerate(CHANNELS):
+            v = d[j, mask]
+            mass = float(v.sum()); local = float(abs(v).sum())
+            cells.append(dict(band=band, channel=channel, signed_mass=mass,
+                L1=local, share_of_L1=local/norm if norm > 0 else None,
+                signed_first_moment=float(v @ SIG[mask])))
+    collapsed = d.sum(axis=0)
+    collapsed_L1 = float(abs(collapsed).sum())
+    require(abs(sum(c['L1'] for c in cells)-norm) < 1e-12*max(1., norm),
+            'Regional L1 accounting failed')
+    require(abs(sum(c['signed_mass'] for c in cells)-d.sum()) < 1e-12*max(1., norm),
+            'Regional signed accounting failed')
+    require(abs(sum(c['signed_first_moment'] for c in cells)-(d*SIG).sum()) < 1e-12*max(1., norm),
+            'Regional moment accounting failed')
+    require(collapsed_L1 <= norm+1e-12*max(1., norm), 'Triangle inequality failed')
+    return dict(L1_153=norm, signed_total=float(d.sum()),
+                first_moment=float((d*SIG).sum()), L1_collapsed_51=collapsed_L1,
+                channel_cancellation_L1=max(0., norm-collapsed_L1), cells=cells)
+
+
+def regional_panel(summary):
+    expected = {r[1]:r[0] for r in DATA}
+    rows = summary['rows']
+    require(summary.get('paired_integrity_passed') is True and len(rows) == 12 and
+            {r['key'] for r in rows} == set(expected), 'Need the complete accepted R11 input panel')
+    result = []
+    for r in rows:
+        require(expected[r['key']] == r['name'] and r['status'] == 'paired_complete', 'Changed R11 identity')
+        ds = r['descriptors']
+        p = {k:profile(ds[k]['post_HB_bins_A2']) for k in ('UD', 'P25', 'RO', 'RU')}
+        metrics = {}
+        for units in ('area_profile', 'normalized_profile'):
+            v = p if units == 'area_profile' else {k:a/a.sum() for k,a in p.items()}
+            d = dict(total=v['UD']-v['RO'], coordinate=v['RU']-v['RO'],
+                     method=v['UD']-v['RU'], repeat=v['RO']-v['P25'])
+            require(abs(d['total']-d['coordinate']-d['method']).max() < 1e-10,
+                    'Ordered profile identity failed')
+            metrics[units] = {k:vector_regions(a) for k,a in d.items()}
+        result.append(dict(key=r['key'], name=r['name'], regions=metrics))
+    return dict(rows=result, R11_classification=summary['classification'],
+        new_labels=False, SCF_calls=0, model_calls=0, adopted=False,
+        band_units='sigma in e/A^2; area-profile mass A^2, normalized mass dimensionless',
+        meaning='Disjoint descriptive partitions. Channel cancellation is not an HB energy or error contribution.')
+
+
+def error_summary(y0, yc, yu, truth, phi_y, phi_gain):
+    y0, yc, yu, truth, phi_y, phi_gain = map(finite, (y0, yc, yu, truth, phi_y, phi_gain))
+    n = len(truth)
+    require(n > 0 and all(a.shape == (n,) for a in (y0,yc,yu)) and
+            phi_y.shape == phi_gain.shape == (3,n), 'Error-summary shape mismatch')
+    out = dict(rows=n)
+    for name, y in (('O',y0), ('C',yc), ('U',yu)):
+        err = y-truth
+        out[name] = dict(MAE=float(abs(err).mean()), bias=float(err.mean()))
+    removed = out['O']['MAE']-out['C']['MAE']
+    remaining = out['C']['MAE']-out['U']['MAE']
+    available = out['O']['MAE']-out['U']['MAE']
+    out.update(MAE_removed_O_to_C=removed, MAE_remaining_C_to_U=remaining,
+        MAE_gap_O_to_U=available,
+        signed_recovery_fraction=removed/available if available > 1e-6 else None,
+        mean_prediction_shift=float((yc-y0).mean()),
+        improved_rows=int((abs(yc-truth)<abs(y0-truth)).sum()),
+        worsened_rows=int((abs(yc-truth)>abs(y0-truth)).sum()),
+        prediction_ShAP={k:float(v.mean()) for k,v in zip(('area','volume','shape'),phi_y)},
+        absolute_error_reduction_ShAP={k:float(v.mean()) for k,v in zip(('area','volume','shape'),phi_gain)})
+    require(abs(removed+remaining-available) < IDENTITY_TOL, 'Error telescope failed')
+    require(abs(sum(out['prediction_ShAP'].values())-out['mean_prediction_shift']) < IDENTITY_TOL,
+            'Prediction Shapley identity failed')
+    require(abs(sum(out['absolute_error_reduction_ShAP'].values())-removed) < IDENTITY_TOL,
+            'Absolute-error Shapley identity failed')
+    return out
+
+
+def explanatory_scores(rows, legacy, exact):
+    """Audit all 332 archived rows; replay and score only the fixed 141 glycol rows.
+
+    legacy has 2 columns (original P21 000 and UD anchors) on the 141-row target.
+    exact has 9 columns (eight O->C corners and full U) on the 141-row target.
+    A missing/nonfinite value blocks the complete-panel result, never drops a row.
+    """
+    require(len(rows) == 332, 'P21 332-row universe changed')
+    ids = [str(r['r3_row_id']) for r in rows]
+    require(len(set(ids)) == 332 and len({r['solvent'] for r in rows}) == 14, 'P21 identity universe changed')
+    idx = np.array([i for i,r in enumerate(rows) if r['solvent'] in GLYCOLS], dtype=int)
+    require(len(idx) == 141, 'Expected 141 fixed linear-glycol rows')
+    for key, (_name,n) in GLYCOLS.items():
+        require(sum(r['solvent'] == key for r in rows) == n, 'Glycol denominator changed')
+    l = np.asarray(legacy,float); x = np.asarray(exact,float)
+    require(l.shape == (141,2) and x.shape == (141,9), 'Missing factorial dimensions')
+    target = [rows[i] for i in idx]
+    old = finite([[r[c] for c in (*CORNERS,'UD')] for r in rows])
+    require(abs(old[:,7]-old[:,8]).max() < IDENTITY_TOL, 'Archived P21 111 is not full UD')
+    anchors=old[idx][:,[0,8]]
+    finite_l = np.isfinite(l); finite_x = np.isfinite(x)
+    parity = bool(finite_l.all() and abs(l-anchors).max() < PARITY_TOL)
+    status = dict(legacy_requested=282, legacy_finite=int(finite_l.sum()),
+        exact_requested=1269, exact_finite=int(finite_x.sum()),
+        legacy_parity_passed=parity,
+        legacy_max_error=float(abs(l-anchors).max()) if finite_l.all() else None,
+        complete=bool(parity and finite_x.all()), model='Z0x',
+        endpoint='P28 exact, ZC_R6_ENDPOINT=1', adopted=False)
+    if not status['complete']:
+        return dict(status=status, aggregate_errors=None, private_rows=[])
+    truth = finite([r['ln_gamma_inf'] for r in target])
+    values = {c:x[:,j] for j,c in enumerate(CORNERS)}
+    phi_y = shapley_three(values)
+    losses = {c:abs(values[c]-truth) for c in CORNERS}
+    phi_gain = -shapley_three(losses)
+    require(abs(phi_y.sum(axis=0)-(x[:,7]-x[:,0])).max() < IDENTITY_TOL,
+            'Per-row prediction Shapley identity failed')
+    require(abs(phi_gain.sum(axis=0)-(losses['000']-losses['111'])).max() < IDENTITY_TOL,
+            'Per-row absolute-error Shapley identity failed')
+    pooled = error_summary(x[:,0],x[:,7],x[:,8],truth,phi_y,phi_gain)
+    solvents = []
+    for key,(name,n) in GLYCOLS.items():
+        use = np.array([r['solvent'] == key for r in target])
+        q = error_summary(x[use,0],x[use,7],x[use,8],truth[use],phi_y[:,use],phi_gain[:,use])
+        # Endpoint bridge never subtracts a legacy O score from an exact C score.
+        oo = old[idx[use]]
+        q['legacy_P21'] = dict(O_MAE=float(abs(oo[:,0]-truth[use]).mean()),
+                               U_MAE=float(abs(oo[:,8]-truth[use]).mean()))
+        q['endpoint_bridge'] = dict(O_MAE_change=q['O']['MAE']-q['legacy_P21']['O_MAE'],
+                                     U_MAE_change=q['U']['MAE']-q['legacy_P21']['U_MAE'])
+        solvents.append(dict(name=name,key=key,**q))
+    macro = {f'{a}_MAE':float(np.mean([s[a]['MAE'] for s in solvents])) for a in ('O','C','U')}
+    macro['MAE_removed_O_to_C'] = macro['O_MAE']-macro['C_MAE']
+    private_rows = []
+    for j,r in enumerate(target):
+        private_rows.append(dict(r3_row_id=str(r['r3_row_id']),
+            predictions={c:float(x[j,k]) for k,c in enumerate((*CORNERS,'UD'))},
+            prediction_ShAP=phi_y[:,j].tolist(), absolute_error_reduction_ShAP=phi_gain[:,j].tolist()))
+    return dict(status=status, aggregate_errors=dict(solvents=solvents, pooled=pooled,
+        equal_solvent_mean=macro, requested_P21_rows=332, audit_only_other_rows=191), private_rows=private_rows)
diff --git a/scripts/r12_selftest.py b/scripts/r12_selftest.py
new file mode 100644
--- /dev/null
+++ b/scripts/r12_selftest.py
@@ -0,0 +1,327 @@
+"""Synthetic software tests only. No UD data, quantum chemistry or real Z0x scores."""
+from __future__ import annotations
+import argparse
+from contextlib import ExitStack
+import copy
+import json
+import os
+from pathlib import Path
+import sys
+import tempfile
+import types
+import unittest
+from unittest.mock import patch
+import numpy as np
+import pandas as pd
+import r12_analysis as a
+import r12_review as r
+from r11_selftest import panel
+from r3_common import write_sigma
+
+
+def data():
+    counts=list(a.GLYCOLS.items())+[(f'OTHER{k}',(f'other{k}',20 if k<9 else 11)) for k in range(10)]
+    rows=[];exact=[];cases=[]
+    for solvent,(_name,n) in counts:
+        part=[]
+        for k in range(n):
+            truth=float(k%7)/10
+            vals={c:truth+2-.1*int(c[0])-.2*int(c[1])-1.3*int(c[2])+.03*int(c[0])*int(c[2]) for c in a.CORNERS}
+            row=dict(r3_row_id=f'id-{len(rows):04d}',solute='SOLUTE',solvent=solvent,T=298.15+k,
+                     ln_gamma_inf=truth,**vals,UD=vals['111'])
+            rows.append(row);part.append({k:row[k] for k in ('r3_row_id','T')})
+            if solvent in a.GLYCOLS:
+                values=[truth+2-.15*int(c[0])-.05*int(c[1])-1.1*int(c[2])+.02*int(c[0])*int(c[1]) for c in a.CORNERS]
+                exact.append(values+[truth+.45])
+        cases.append(dict(solute='SOLUTE',solvent=solvent,rows=part))
+    old=np.array([[z[c] for c in ('000','UD')] for z in rows if z['solvent'] in a.GLYCOLS])
+    return rows,old,np.array(exact),cases
+
+
+class Arithmetic(unittest.TestCase):
+    def test_hybrid_all_eight_corners(self):
+        o=np.zeros((3,51));o[0,25]=90;o[1,40]=10
+        c=np.zeros((3,51));c[0,25]=100;c[2,10]=100
+        for corner in a.CORNERS:
+            v,m=a.hybrid(o,{'volume [A^3]':70,'keep':'old'},c,{'volume [A^3]':100},corner)
+            self.assertAlmostEqual(v.sum(),200 if corner[0]=='1' else 100)
+            np.testing.assert_allclose(v/v.sum(),c/c.sum() if corner[2]=='1' else o/o.sum())
+            self.assertEqual(m['volume [A^3]'],100 if corner[1]=='1' else 70)
+            self.assertEqual(m['keep'],'old')
+
+    def test_nonfinite_and_invalid_profiles(self):
+        for p in (np.zeros((3,51)),np.ones((2,51)),np.full((3,51),np.nan),-np.ones((3,51))):
+            with self.assertRaises(ValueError):a.profile(p)
+        with self.assertRaises(ValueError):a.hybrid(np.ones((3,51)),{'volume [A^3]':0},np.ones((3,51)),{'volume [A^3]':1},'000')
+
+    def test_sigma_boundary_partition(self):
+        masks=a.band_masks()
+        self.assertEqual([int(v.sum()) for v in masks.values()],[16,5,9,5,16])
+        self.assertTrue(masks['negative_tail'][15])  # -0.010
+        self.assertTrue(masks['negative_shoulder'][20])  # -0.005
+        self.assertTrue(masks['centre'][25])
+        self.assertTrue(masks['positive_shoulder'][30])
+        self.assertTrue(masks['positive_tail'][35])
+
+    def test_channel_cancellation_is_not_shape_erasure(self):
+        x=np.zeros((3,51));x[0,25]=.1;x[1,25]=-.1
+        q=a.vector_regions(x)
+        self.assertAlmostEqual(q['L1_153'],.2)
+        self.assertEqual(q['L1_collapsed_51'],0.)
+        self.assertAlmostEqual(q['channel_cancellation_L1'],.2)
+        self.assertEqual(q['signed_total'],0.)
+
+    def test_area_normalization_and_zero_denominator(self):
+        q=a.vector_regions(np.zeros((3,51)))
+        self.assertTrue(all(c['share_of_L1'] is None for c in q['cells']))
+        rows=panel();row=rows[0]
+        base=np.asarray(row['descriptors']['RO']['post_HB_bins_A2'])
+        row['descriptors']['UD']['post_HB_bins_A2']=(2*base).tolist()
+        s=dict(rows=rows,paired_integrity_passed=True,classification={'unchanged':True})
+        z=a.regional_panel(s)['rows'][0]['regions']
+        self.assertAlmostEqual(z['normalized_profile']['total']['L1_153'],0.)
+        self.assertGreater(z['area_profile']['total']['L1_153'],0.)
+
+    def test_preserve_R11_labels_and_all_members(self):
+        s=dict(rows=panel(),paired_integrity_passed=True,classification={'labels':['inconclusive']})
+        original=copy.deepcopy(s);q=a.regional_panel(s)
+        self.assertEqual(s,original);self.assertEqual(q['R11_classification'],s['classification'])
+        self.assertFalse(q['new_labels']);self.assertEqual(q['model_calls'],0)
+        s['rows'].pop()
+        with self.assertRaises(ValueError):a.regional_panel(s)
+
+    def test_shapley_of_loss_not_absolute_shapley(self):
+        values={c:np.array([-1.+2*int(c[2])]) for c in a.CORNERS}
+        pred=a.shapley_three(values)
+        gain=-a.shapley_three({k:abs(v) for k,v in values.items()})
+        self.assertAlmostEqual(pred.sum(),2.);self.assertAlmostEqual(gain.sum(),0.)
+        q=a.error_summary([-1],[1],[0],[0],pred,gain)
+        self.assertEqual(q['MAE_removed_O_to_C'],0.)
+
+    def test_full_synthetic_scorecard(self):
+        rows,l,x,_=data();d=a.explanatory_scores(rows,l,x)
+        self.assertTrue(d['status']['complete'])
+        self.assertEqual(len(d['private_rows']),141)
+        self.assertEqual(d['aggregate_errors']['pooled']['rows'],141)
+        self.assertEqual(d['aggregate_errors']['audit_only_other_rows'],191)
+        for z in d['aggregate_errors']['solvents']:
+            self.assertAlmostEqual(sum(z['absolute_error_reduction_ShAP'].values()),z['MAE_removed_O_to_C'])
+
+    def test_nonfinite_preserves_denominator(self):
+        rows,l,x,_=data();x[0,1]=np.nan;d=a.explanatory_scores(rows,l,x)
+        self.assertFalse(d['status']['complete']);self.assertEqual(d['status']['exact_requested'],1269)
+        self.assertEqual(d['status']['exact_finite'],1268);self.assertIsNone(d['aggregate_errors'])
+
+    def test_legacy_gate_and_unknown_identity(self):
+        rows,l,x,_=data();l[0,0]+=.01
+        self.assertFalse(a.explanatory_scores(rows,l,x)['status']['legacy_parity_passed'])
+        rows[0]['r3_row_id']=rows[1]['r3_row_id']
+        with self.assertRaises(ValueError):a.explanatory_scores(rows,l,x)
+
+    def test_macro_is_not_row_weighted_pool(self):
+        rows,l,x,_=data();use=[j for j,z in enumerate([v for v in rows if v['solvent'] in a.GLYCOLS]) if z['solvent'].startswith('MTH')]
+        x[use,7]+=1
+        q=a.explanatory_scores(rows,l,x)['aggregate_errors']
+        self.assertNotAlmostEqual(q['pooled']['C']['MAE'],q['equal_solvent_mean']['C_MAE'])
+
+    def test_negative_and_greater_than_one_recovery_not_clipped(self):
+        for c in (-2.,.0):
+            vals={k:np.array([1.+(c-1)*int(k[2])]) for k in a.CORNERS}
+            phi=a.shapley_three(vals);gain=-a.shapley_three({k:abs(v) for k,v in vals.items()})
+            z=a.error_summary([1],[c],[.5],[0],phi,gain)
+            self.assertAlmostEqual(z['signed_recovery_fraction'],-2. if c==-2 else 2.)
+        z=a.error_summary([1],[1],[1],[0],np.zeros((3,1)),np.zeros((3,1)))
+        self.assertIsNone(z['signed_recovery_fraction'])
+
+    def test_public_allowlist_discards_private_fields(self):
+        rows,l,x,_=data();d=a.explanatory_scores(rows,l,x)
+        d['coordinates']=[[1,2,3]];d['aggregate_errors']['solvents'][0]['private_path']='/secret'
+        d['aggregate_errors']['pooled']['dense_profile']=[1]*153
+        z=r.public_scores(d);text=json.dumps(z)
+        self.assertNotIn('/secret',text);self.assertNotIn('dense_profile',text)
+        self.assertNotIn('coordinates',text);self.assertNotIn('private_rows',text)
+        self.assertNotIn('prediction_ShAP',text);self.assertNotIn('mean_prediction_shift',text)
+        d['aggregate_errors']['pooled']['O']['MAE']=[1,2]
+        with self.assertRaises(ValueError):r.public_scores(d)
+
+
+class Execution(unittest.TestCase):
+    def test_mac_guard(self):
+        with patch.object(sys,'platform','linux'):
+            with self.assertRaises(RuntimeError):r.cross.mac_only()
+
+    def test_identity_alignment_not_row_position(self):
+        rows,_,_,_=data();d=pd.DataFrame(rows)
+        r.same_rows(d,d.iloc[::-1])
+        b=d.copy();b.loc[0,'T']+=1
+        with self.assertRaises(ValueError):r.same_rows(d,b)
+        b=d.copy();b.loc[0,'solvent']='wrong'
+        with self.assertRaises(ValueError):r.same_rows(d,b)
+
+    def test_job_budget(self):
+        _,_,_,cases=data();jobs=r.jobs_for(cases)
+        self.assertEqual(len(jobs),44)
+        self.assertEqual(sum(len(j['case']['rows']) for j in jobs if j['phase']=='legacy'),282)
+        self.assertEqual(sum(len(j['case']['rows']) for j in jobs if j['phase']=='exact'),1269)
+        with self.assertRaises(ValueError):r.jobs_for(cases[1:])
+
+    def test_private_alias_and_fresh(self):
+        with tempfile.TemporaryDirectory() as t:
+            p=Path(t);(p/'real').mkdir();(p/'alias').symlink_to(p/'real')
+            self.assertEqual(r.private(p/'alias/new'),(p/'real/new').resolve())
+            with self.assertRaises(FileExistsError):r.private(p/'real',fresh=True)
+            (p/'real/.git').mkdir()
+            with self.assertRaises(ValueError):r.private(p/'alias/new')
+
+    def test_process_timeout(self):
+        with tempfile.TemporaryDirectory() as t:
+            q=r.cross.launch([sys.executable,'-c','import time;time.sleep(10)'],Path(t)/'log',.05,os.environ.copy())
+            self.assertEqual(q['execution_state'],'timeout');self.assertNotEqual(q['returncode'],0)
+
+    def fixture_job(self,p,corner='111',phase='exact'):
+        p=Path(p);o=np.zeros((3,51));o[0,25]=90;o[1,40]=10
+        u=o.copy();u[0,25]=80;u[1,40]=30
+        key=next(iter(a.GLYCOLS));meta={'volume [A^3]':80,'standard_INCHIKEY':key}
+        for name,ps in [('O',o),('U',u),('S',o)]:write_sigma(p/(name+'.sigma'),a.SIG,ps,meta)
+        case=dict(solute='SOLUTE',solvent=key,rows=[dict(r3_row_id='a',T=300.),dict(r3_row_id='b',T=320.)],
+            open_solvent=r.src.record(p/'O.sigma'),UD_solvent=r.src.record(p/'U.sigma'),open_solute=r.src.record(p/'S.sigma'))
+        cross_profile=u*2
+        (p/'run').mkdir();r.write(p/'run/summary.json',dict(rows=[dict(key=key,
+            descriptors={'RU':{'post_HB_bins_A2':cross_profile.tolist(),'volume_A3':100.}})]))
+        job=dict(case=case,phase=phase,corner=corner)
+        m=dict(r11_run=str(p/'run'),smiles={'SOLUTE':'C',key:'OCCO'})
+        return job,m
+
+    def test_worker_uses_frozen_solute_and_only_requested_endpoint(self):
+        with tempfile.TemporaryDirectory() as t,patch.dict(os.environ,{},clear=False):
+            p=Path(t);job,m=self.fixture_job(p);out=p/'out';out.mkdir();seen=[]
+            cos=types.ModuleType('zcosmo.cosmosac');mod=types.ModuleType('zcosmo.models');pkg=types.ModuleType('zcosmo');pkg.__path__=[]
+            cos.sigma_path=lambda k:Path(os.environ['ZC_SIGMA_OVERRIDE_DIR'])/(k+'.sigma')
+            class Toy:
+                def lngamma_inf(self,T,i):
+                    _,ps,mm=r.replay.read_profile(cos.sigma_path(job['case']['solvent']))
+                    _,ss,_=r.replay.read_profile(cos.sigma_path('SOLUTE'))
+                    seen.append((T,i,ps.sum(),ss.sum(),mm['volume [A^3]'],os.environ['ZC_R6_ENDPOINT']))
+                    return float(ps.sum()+mm['volume [A^3]']/T)
+            mod.make_model=lambda *args:Toy()
+            with patch.dict(sys.modules,{'zcosmo':pkg,'zcosmo.cosmosac':cos,'zcosmo.models':mod}):
+                q=r.one_model_job(job,m,out)
+            self.assertTrue(q['completed']);self.assertEqual(q['attempted_model_calls'],2)
+            self.assertEqual(seen[0][2:],(220.,100.,100.,'1'))
+            self.assertEqual(q['values'][0]['r3_row_id'],'a')
+            self.assertEqual(r.sha(p/'S.sigma'),job['case']['open_solute']['sha256'])
+
+    def test_original_P21_archive_preparation_and_receipts(self):
+        with tempfile.TemporaryDirectory() as t:
+            root=Path(t);archive=root/'AVP';archive.mkdir();op=root/'open';up=root/'UD';op.mkdir();up.mkdir()
+            rows,old,_x,cases=data();df=pd.DataFrame(rows)
+            df.to_csv(archive/'factorial_rows.csv',index=False)
+            r.write(archive/'summary.json',dict(rows=332,finite_all=332))
+            ps=np.zeros((3,51));ps[0,25]=100
+            for k in {'SOLUTE',*(c['solvent'] for c in cases)}:
+                for folder in (op,up):write_sigma(folder/(k+'.sigma'),a.SIG,ps,{'volume [A^3]':80})
+            for name in r.TABLES.values():
+                z=root/name;z.parent.mkdir(parents=True,exist_ok=True);z.write_text('fixed-table')
+            for j,c in enumerate(cases):
+                part=archive/f'pair-{j:04d}';part.mkdir();d=df[df.solvent==c['solvent']]
+                d.to_csv(part/'rows.csv',index=False)
+                rec=dict(open_solvent=r.sha(op/(c['solvent']+'.sigma')),open_solute=r.sha(op/'SOLUTE.sigma'),
+                    UD_solvent=r.sha(up/(c['solvent']+'.sigma')),
+                    **{k:r.sha(root/v) for k,v in r.TABLES.items()})
+                for corner in (*a.CORNERS,'UD'):
+                    pd.DataFrame({'r3_row_id':d.r3_row_id,'value':d[corner],'error':''}).to_csv(part/(corner+'.csv'),index=False)
+                    r.write(part/(corner+'.csv.inputs.json'),rec)
+            with patch.object(r,'ROOT',root):
+                rr,cc,files=r.p21_inputs(archive,op,up)
+                self.assertEqual(len(rr),332);self.assertEqual(len(cc),14);self.assertGreater(len(files),100)
+                # A changed parameter is refused before any model is called.
+                (root/next(iter(r.TABLES.values()))).write_text('changed')
+                with self.assertRaises(ValueError):r.p21_inputs(archive,op,up)
+
+    def test_parameter_receipt_rejects_changed_original(self):
+        # The immutable file-record primitive is used before every evaluation.
+        with tempfile.TemporaryDirectory() as t:
+            p=Path(t)/'x';p.write_text('before');rec=r.src.record(p);p.write_text('after')
+            with self.assertRaises(ValueError):r.src.verify_record(rec)
+
+    def run_driver(self,base,bad_legacy=False,bad_exact=False):
+        base=Path(base);rows,l,x,cases=data();jobs=r.jobs_for(cases)
+        plan_dir=base/'plan';plan_dir.mkdir();p=plan_dir/'plan.json'
+        m=dict(schema=r.SCHEMA,task='factorial',design=r.canonical(r.DESIGN),rows=rows,jobs=jobs,cases=cases)
+        r.write(p,m);out=base/'results';idmap={z['r3_row_id']:i for i,z in enumerate(rows)}
+        tx={z['r3_row_id']:i for i,z in enumerate(v for v in rows if v['solvent'] in a.GLYCOLS)}
+        used=[]
+        def launch(command,log,seconds,env):
+            job=next(j for j in jobs if j['id']==command[command.index('--job')+1]);used.append(job['phase'])
+            folder=Path(command[command.index('--out')+1]);folder.mkdir()
+            j=(('000','UD') if job['phase']=='legacy' else (*a.CORNERS,'UD')).index(job['corner']);vals=[]
+            for z in job['case']['rows']:
+                value=l[tx[z['r3_row_id']],j] if job['phase']=='legacy' else x[tx[z['r3_row_id']],j]
+                if bad_legacy and job['id']=='job-00000':value+=.1
+                value=float(value)
+                if bad_exact and job['phase']=='exact' and job['id']=='job-00008' and not vals:value=None
+                vals.append(dict(r3_row_id=z['r3_row_id'],value=value,error='' if value is not None else 'nonfinite'))
+            r.write(folder/'result.json',dict(job=job['id'],plan_sha256=r.sha(p),completed=all(v['value'] is not None for v in vals),
+                attempted_model_calls=len(vals),values=vals))
+            r.write(folder/'progress.json',dict(attempted_model_calls=len(vals)))
+            Path(log).write_text('synthetic model stand-in, not Z0x\n')
+            return dict(execution_state='returned',returncode=0 if all(v['value'] is not None for v in vals) else 2,wall_s=.001)
+        with patch.object(r.cross,'mac_only'),patch.object(r,'load_plan',return_value=(p,m)),patch.object(r.cross,'launch',side_effect=launch):
+            rc=r.run_factorial(argparse.Namespace(plan=str(p),plan_commit='a'*40,out=str(out)))
+            if not bad_legacy and not bad_exact:
+                self.assertEqual(r.check(argparse.Namespace(plan=str(p),plan_commit='a'*40,run=str(out))),0)
+                with self.assertRaises(FileExistsError):
+                    r.run_factorial(argparse.Namespace(plan=str(p),plan_commit='a'*40,out=str(base/'retry')))
+            d=r.read(out/'summary.json')
+        return rc,d,used,p,m,out
+
+    def test_complete_orchestration_and_independent_check(self):
+        with tempfile.TemporaryDirectory() as t:
+            rc,d,used,p,m,out=self.run_driver(t)
+            self.assertEqual(rc,0);self.assertEqual(d['attempted_model_calls'],1551)
+            self.assertEqual(len(d['receipts']),44);self.assertTrue(d['status']['complete'])
+            bad=r.read(out/'job-00000/result.json');bad['values'][0]['value']+=.1;r.write(out/'job-00000/result.json',bad)
+            with patch.object(r,'load_plan',return_value=(p,m)):
+                with self.assertRaises(ValueError):r.check(argparse.Namespace(plan=str(p),plan_commit='a'*40,run=str(out)))
+
+    def test_failed_legacy_blocks_every_C_request(self):
+        with tempfile.TemporaryDirectory() as t:
+            rc,d,used,*_=self.run_driver(t,bad_legacy=True)
+            self.assertEqual(rc,2);self.assertNotIn('exact',used)
+            self.assertEqual(d['attempted_model_calls'],282)
+            self.assertEqual(sum(z['state']=='blocked_legacy_gate' for z in d['receipts']),36)
+            self.assertIsNone(d['aggregate_errors'])
+
+    def test_failed_exact_row_retains_other_finite_rows_and_requests(self):
+        with tempfile.TemporaryDirectory() as t:
+            rc,d,used,*_=self.run_driver(t,bad_exact=True)
+            self.assertEqual(rc,2);self.assertEqual(d['attempted_model_calls'],1551)
+            self.assertEqual(d['status']['exact_finite'],1268)
+            self.assertEqual(d['status']['exact_requested'],1269)
+            self.assertIsNone(d['aggregate_errors'])
+
+    def test_private_region_run_and_replay(self):
+        with tempfile.TemporaryDirectory() as t:
+            root=Path(t);pd=root/'plan';pd.mkdir();p=pd/'plan.json'
+            old=root/'old';old.mkdir();s=dict(rows=panel(),paired_integrity_passed=True,
+                classification={'old_labels':['inconclusive'], 'eta':.359})
+            r.write(old/'summary.json',s)
+            m=dict(task='regions',r11_run=str(old));r.write(p,m)
+            out=root/'regions'
+            with patch.object(r.cross,'mac_only'),patch.object(r,'load_plan',return_value=(p,m)):
+                self.assertEqual(r.regions(argparse.Namespace(plan=str(p),plan_commit='a'*40,out=str(out))),0)
+                self.assertEqual(r.check(argparse.Namespace(plan=str(p),plan_commit='a'*40,run=str(out))),0)
+                self.assertFalse((out/'public-errors.json').exists())
+                self.assertEqual(r.read(out/'regions-private.json')['R11_classification'],s['classification'])
+                with self.assertRaises(FileExistsError):
+                    r.regions(argparse.Namespace(plan=str(p),plan_commit='a'*40,out=str(root/'retry')))
+                z=r.read(out/'regions-private.json');z['new_labels']=True;r.write(out/'regions-private.json',z)
+                with self.assertRaises(ValueError):r.check(argparse.Namespace(plan=str(p),plan_commit='a'*40,run=str(out)))
+
+    def test_successful_process_does_not_make_nan_a_success(self):
+        rows,l,x,_=data();l[10,1]=np.nan
+        d=a.explanatory_scores(rows,l,x)
+        self.assertFalse(d['status']['complete']);self.assertEqual(d['status']['legacy_requested'],282)
+
+
+if __name__=='__main__':unittest.main(verbosity=2)
```
<!-- END PATCH H12 -->

<!-- BEGIN PATCH P46P47 -->
```diff
diff --git a/scripts/r12_review.py b/scripts/r12_review.py
new file mode 100644
--- /dev/null
+++ b/scripts/r12_review.py
@@ -0,0 +1,481 @@
+"""P46/P47: one private Mac-only scoring replay or sigma-region audit, zero QC.
+
+Do not publish plans, dense profiles, row predictions or logs. Only
+public-errors.json from P46 is eligible for a separate human publication review.
+"""
+from __future__ import annotations
+import argparse
+from contextlib import redirect_stdout, redirect_stderr
+import hashlib
+import json
+import os
+from pathlib import Path
+import re
+import subprocess
+import sys
+import time
+import traceback
+import numpy as np
+import pandas as pd
+import r10_sources as src
+import r10_replay as replay
+import r11_cross as cross
+import r12_analysis as ana
+
+ROOT = Path(__file__).resolve().parents[1]
+BASE = 'a93a1c9abbec32e0af7ff259a8db6fa550bb34a9'
+MARKER = 'R12-P46-P47-P48: private explanatory scoring and regional accounting'
+SCHEMA = 'R12-explanation-v1'
+RECORDS = {k:f'docs/astra/round12/{k.upper()}_PLAN_SHA256.txt' for k in ('factorial','regions')}
+MODEL_FILES = ['src/zcosmo/cosmosac.py','src/zcosmo/z0x.py','src/zcosmo/models.py',
+               'src/zcosmo/zmodel.py','src/zcosmo/baselines.py']
+FILES = ['scripts/r12_review.py','scripts/r12_analysis.py','scripts/r4_glycols.py',
+         *cross.FILES, *MODEL_FILES]
+FILES = list(dict.fromkeys(FILES))
+TABLES = {'dielectric':'results/qc/dielectric.csv',
+          'dispersion':'results/qc/dispersion.csv','Z0':'results/z_params/Z0.json'}
+DESIGN = dict(P21_rows=332,P21_solvents=14,scored_glycol_rows=141,
+    targets=ana.GLYCOLS,legacy_requests=282,exact_requests=1269,
+    maximum_requests=1551,seconds_per_worker=120,total_model_seconds=7200,
+    workers_in_parallel=1,legacy_tolerance=ana.PARITY_TOL,identity_tolerance=ana.IDENTITY_TOL,
+    primary_endpoint='P28_exact',SCF_calls=0,gradients=0,no_retries=True,
+    band_millithresholds=[-10,-5,5,10],R11_labels_unchanged=True)
+sha, read, write = src.sha, src.read, src.write
+
+
+def canonical(x):
+    return json.loads(json.dumps(x,sort_keys=True,allow_nan=False))
+
+
+def private(path,fresh=False):
+    return cross.private_path(path,fresh=fresh)
+
+
+def reg_check(commit):
+    if not re.fullmatch('[0-9a-f]{40}',commit):raise ValueError('Full registration commit required')
+    src.git('merge-base','--is-ancestor',BASE,'HEAD')
+    src.git('merge-base','--is-ancestor',commit,'HEAD')
+    b = src.git('show',commit+':PREREGISTRATION.md')
+    if MARKER.encode() not in b:raise ValueError('R12 registration marker missing')
+    return dict(commit=commit,preregistration_sha256=hashlib.sha256(b).hexdigest())
+
+
+def r11_evidence(plan,commit,run):
+    # The original checker performs no new SCF or activity-model call.
+    with redirect_stdout(sys.stderr):
+        cross.check(argparse.Namespace(plan=str(plan),plan_commit=commit,run=str(run)))
+        _p,m,by,_s = cross.load_plan(plan,commit)
+    d = read(Path(run)/'summary.json')
+    return m,by,d
+
+
+def frame(path):
+    d = pd.read_csv(path,dtype={'r3_row_id':str},float_precision='round_trip')
+    if 'r3_row_id' not in d or d.r3_row_id.isna().any() or d.r3_row_id.duplicated().any():
+        raise ValueError('Missing/duplicate P21 observation IDs')
+    return d
+
+
+def same_rows(a,b):
+    if set(a.r3_row_id)!=set(b.r3_row_id):raise ValueError('P21 row identities differ')
+    aa=a.set_index('r3_row_id');bb=b.set_index('r3_row_id').loc[aa.index]
+    for f in ('solute','solvent'):
+        if not np.array_equal(aa[f].to_numpy(),bb[f].to_numpy()):raise ValueError('P21 ordered-pair drift')
+    for f in ('T','ln_gamma_inf'):
+        if not np.array_equal(aa[f].to_numpy(float),bb[f].to_numpy(float)):
+            raise ValueError('P21 temperature/observation drift')
+
+
+def p21_inputs(folder,open_dir,ud_dir):
+    """Use the original P21 archive, including its per-pair input receipts."""
+    folder=Path(folder).resolve();open_dir=Path(open_dir).resolve();ud_dir=Path(ud_dir).resolve()
+    d=frame(folder/'factorial_rows.csv');s=read(folder/'summary.json')
+    if len(d)!=332 or d.solvent.nunique()!=14 or s['rows']!=332 or s['finite_all']!=332:
+        raise ValueError('P21 universe or recorded completeness changed')
+    if not np.isfinite(d[['T','ln_gamma_inf',*ana.CORNERS,'UD']].to_numpy(float)).all():
+        raise ValueError('The recorded P21 comparison is not fully finite')
+    if (d['T']<=0).any() or (d.solute==d.solvent).any():raise ValueError('Invalid P21 states')
+    if abs(d['111'].to_numpy(float)-d['UD'].to_numpy(float)).max()>=ana.IDENTITY_TOL:
+        raise ValueError('Archived P21 111/full-UD identity failed')
+    for key,(_name,n) in ana.GLYCOLS.items():
+        if int((d.solvent==key).sum())!=n:raise ValueError('P21 glycol membership differs')
+    protected=[src.record(folder/'factorial_rows.csv'),src.record(folder/'summary.json')]
+    cases=[];parts=[]
+    for part in sorted(folder.glob('pair-*')):
+        q=frame(part/'rows.csv');same_rows(q,d[d.r3_row_id.isin(q.r3_row_id)])
+        if len(q[['solute','solvent']].drop_duplicates())!=1:raise ValueError('Not one P21 pair')
+        solute,solvent=q[['solute','solvent']].iloc[0].tolist()
+        op=open_dir/(solvent+'.sigma');sp=open_dir/(solute+'.sigma')
+        up=replay.historical_ud_path(ud_dir,solvent)
+        protected.append(src.record(part/'rows.csv'))
+        for corner in (*ana.CORNERS,'UD'):
+            pred=frame(part/(corner+'.csv')).set_index('r3_row_id')
+            wanted=d.set_index('r3_row_id').loc[q.r3_row_id,corner].to_numpy(float)
+            if set(pred.index)!=set(q.r3_row_id) or not np.isfinite(pred.value.to_numpy(float)).all():
+                raise ValueError('P21 per-corner identity/finite mismatch')
+            if abs(pred.loc[q.r3_row_id,'value'].to_numpy(float)-wanted).max()>1e-12:
+                raise ValueError('P21 aggregate differs from its per-pair output')
+            receipt=part/(corner+'.csv.inputs.json');r=read(receipt)
+            expected=dict(open_solvent=sha(op),open_solute=sha(sp),UD_solvent=sha(up),
+                          **{k:sha(ROOT/v) for k,v in TABLES.items()})
+            if r!=expected:raise ValueError('P21 profile/parameter hashes differ; recover originals, no fallback')
+            protected.extend([src.record(part/(corner+'.csv')),src.record(receipt)])
+        cases.append(dict(solute=solute,solvent=solvent,
+            rows=q[['r3_row_id','T']].to_dict('records'),
+            open_solvent=src.record(op),open_solute=src.record(sp),UD_solvent=src.record(up)))
+        parts.append(q)
+    if not parts:raise ValueError('Original P21 per-pair archive unavailable')
+    allparts=pd.concat(parts,ignore_index=True)
+    if allparts.r3_row_id.duplicated().any():raise ValueError('Duplicate P21 pair observation')
+    same_rows(d,allparts)
+    if len({(r['solute'],r['solvent']) for r in cases})!=len(cases):raise ValueError('Duplicate P21 pair')
+    protected.extend(src.record(ROOT/v) for v in TABLES.values())
+    for r in cases:protected.extend(r[k] for k in ('open_solvent','open_solute','UD_solvent'))
+    unique={r['path']:r for r in protected}
+    # No outcome selects a member. This is a retrospective source-identity freeze.
+    return d.to_dict('records'),cases,list(unique.values())
+
+
+def jobs_for(cases):
+    jobs=[]
+    for phase in ('legacy','exact'):
+        for case in cases:
+            if case['solvent'] not in ana.GLYCOLS:continue
+            for corner in (('000','UD') if phase=='legacy' else (*ana.CORNERS,'UD')):
+                jobs.append(dict(id=f'job-{len(jobs):05d}',phase=phase,corner=corner,case=case))
+    if sum(len(j['case']['rows']) for j in jobs)!=1551:
+        raise ValueError('Fixed model request budget changed')
+    return jobs
+
+
+def freeze(a):
+    cross.mac_only();os.umask(0o077)
+    reg=reg_check(a.registration)
+    oldplan=private(a.r11_plan);oldrun=private(a.r11_run)
+    m,by,d=r11_evidence(oldplan,a.r11_plan_commit,oldrun)
+    sources=src.committed_sources(FILES)
+    inputs=[src.record(oldplan),src.record(oldrun/'summary.json'),src.record(oldrun/'public-summary.json')]
+    for key in by:
+        for arm in ('RO','RU'):
+            inputs.append(src.record(oldrun/key/(arm+'.terminal.json')))
+            inputs.extend(src.record(oldrun/key/arm/n) for n in ('result.json','segments.npz'))
+    inputs += m['protected_population']
+    plan=dict(schema=SCHEMA,base=BASE,registration=reg,task=a.task,design=canonical(DESIGN),
+        r11_plan=src.record(oldplan),r11_run=str(oldrun),r11_plan_commit=a.r11_plan_commit,
+        sources=sources,packages=cross.packages(),inputs=inputs,
+        observed_R11_classification=d['classification'],adopted=False)
+    if a.task=='factorial':
+        if not a.p21_run or not a.p21_open_profiles:raise ValueError('Need the original P21 archive and original open profiles')
+        uds={str(Path(r['UD_profile']['path']).parent.resolve()) for r in by.values()}
+        if len(uds)!=1:raise ValueError('Ambiguous original UD directory')
+        rows,cases,files=p21_inputs(a.p21_run,a.p21_open_profiles,next(iter(uds)))
+        # UD files for the scored targets must be the same lineage checked in R11.
+        for c in cases:
+            if c['solvent'] in ana.GLYCOLS and c['UD_solvent']['sha256']!=by[c['solvent']]['UD_profile']['sha256']:
+                raise ValueError('P21/R11 UD lineage differs')
+        plan.update(rows=rows,cases=cases,jobs=jobs_for(cases));plan['inputs']+=files
+        compounds=ROOT/'data/benchmark/compounds.csv';plan['inputs'].append(src.record(compounds))
+        cd=pd.read_csv(compounds)
+        if cd.inchikey.duplicated().any():raise ValueError('Duplicate compound identity')
+        lookup=dict(zip(cd.inchikey,cd.smiles))
+        keys={k for c in cases for k in (c['solute'],c['solvent'])}
+        if not keys<=set(lookup):raise ValueError('P21 molecule missing from fixed compound table')
+        plan['smiles']={k:lookup[k] for k in sorted(keys)}
+    plan['inputs']=list({z['path']:z for z in plan['inputs']}.values())
+    out=private(a.out,fresh=True);out.mkdir(parents=True,mode=0o700)
+    write(out/'plan.json',plan);(out/'PLAN_SHA256.txt').write_text(sha(out/'plan.json')+'\n')
+    print('Private',a.task,'plan digest:',sha(out/'plan.json'))
+    return 0
+
+
+def load_plan(path,commit,full=True):
+    cross.mac_only();p=private(path);m=read(p)
+    if m.get('schema')!=SCHEMA or m.get('base')!=BASE or m.get('design')!=canonical(DESIGN) or m.get('task') not in RECORDS:
+        raise ValueError('Changed R12 design')
+    if not re.fullmatch('[0-9a-f]{40}',commit):raise ValueError('Full plan-record commit required')
+    src.git('merge-base','--is-ancestor',commit,'HEAD')
+    src.git('merge-base','--is-ancestor',m['registration']['commit'],commit)
+    if src.git('show',commit+':'+RECORDS[m['task']]).decode().strip()!=sha(p):raise ValueError('Plan was not committed before output')
+    if reg_check(m['registration']['commit'])!=m['registration'] or cross.packages()!=m['packages']:
+        raise ValueError('Registration/package drift')
+    src.verify_sources(m['sources'])
+    if m['task']=='factorial' and m['jobs']!=jobs_for(m['cases']):
+        raise ValueError('Changed factorial job schedule')
+    for r in m['inputs']:src.verify_record(r)
+    if full:
+        _old,_by,s=r11_evidence(m['r11_plan']['path'],m['r11_plan_commit'],m['r11_run'])
+        if s['classification']!=m['observed_R11_classification']:raise ValueError('R11 labels changed')
+    return p,m
+
+
+def one_model_job(job,m,out):
+    """One fresh worker, one ordered pair and one corner. No fitting input enters the model."""
+    c=job['case'];out=Path(out);overlay=out/'overlay';overlay.mkdir(mode=0o700)
+    for k in ('open_solvent','open_solute','UD_solvent'):src.verify_record(c[k])
+    solute,solvent=c['solute'],c['solvent']
+    (_s,o,om)=replay.read_profile(c['open_solvent']['path'])
+    if job['phase']=='exact' and job['corner']!='UD':
+        summary=read(Path(m['r11_run'])/'summary.json')
+        r=next(v for v in summary['rows'] if v['key']==solvent)
+        desc=r['descriptors']['RU'];other=ana.profile(desc['post_HB_bins_A2'])
+        meta={'volume [A^3]':desc['volume_A3']}
+    else:
+        _s,other,meta=replay.read_profile(c['UD_solvent']['path'])
+    (overlay/(solute+'.sigma')).symlink_to(Path(c['open_solute']['path']).resolve())
+    if job['corner']=='UD':
+        (overlay/(solvent+'.sigma')).symlink_to(Path(c['UD_solvent']['path']).resolve())
+    else:
+        bins,metadata=ana.hybrid(o,om,other,meta,job['corner'])
+        metadata['standard_INCHIKEY']=solvent
+        from r3_common import write_sigma
+        write_sigma(overlay/(solvent+'.sigma'),ana.SIG,bins,metadata)
+    # Never inherit another experiment's profile override or endpoint setting.
+    for key in list(os.environ):
+        if key.startswith('ZC_'):os.environ.pop(key)
+    os.environ.update(ZC_SIGMA_OVERRIDE_DIR=str(overlay),
+        ZC_R6_ENDPOINT='1' if job['phase']=='exact' else '0')
+    from zcosmo.cosmosac import sigma_path
+    for key in (solute,solvent):
+        if Path(sigma_path(key)).resolve()!=(overlay/(key+'.sigma')).resolve():
+            raise ValueError('A requested override fell back to another profile')
+    from zcosmo.models import make_model
+    model=make_model('Z0x',[solute,solvent],[m['smiles'][solute],m['smiles'][solvent]])
+    values=[];attempted=0
+    for row in c['rows']:
+        attempted+=1
+        write(out/'progress.json',dict(attempted_model_calls=attempted,requested=len(c['rows'])))
+        try:
+            y=float(model.lngamma_inf(float(row['T']),0))
+            error='' if np.isfinite(y) else 'nonfinite_prediction'
+        except Exception as e:
+            y=float('nan');error=type(e).__name__
+        values.append(dict(r3_row_id=str(row['r3_row_id']),value=y if np.isfinite(y) else None,error=error))
+    return dict(values=values,attempted_model_calls=attempted,
+                completed=all(v['value'] is not None for v in values))
+
+
+def worker(a):
+    cross.mac_only();os.umask(0o077)
+    p=private(a.plan);m=read(p);claim=read(p.parent/'execution_claim.json')
+    out=private(a.out,fresh=True)
+    if (m.get('schema')!=SCHEMA or m['task']!='factorial' or m['design']!=canonical(DESIGN) or
+        claim['plan_sha256']!=sha(p) or claim['nonce']!=os.environ.get('ZC_R12_NONCE') or
+        claim['pid']!=os.getppid() or out!=Path(claim['output'])/a.job):
+        raise ValueError('Only the single claimed parent run may invoke this worker')
+    src.verify_sources(m['sources'])
+    if cross.packages()!=m['packages']:raise ValueError('Worker package drift')
+    for name in TABLES.values():
+        matches=[z for z in m['inputs'] if Path(z['path']).resolve()==(ROOT/name).resolve()]
+        if len(matches)!=1:raise ValueError('Missing or duplicate model-table fingerprint')
+        src.verify_record(matches[0])
+    for r in (m['r11_plan'],next(r for r in m['inputs'] if r['path']==str(Path(m['r11_run'])/'summary.json'))):
+        src.verify_record(r)
+    js=[j for j in m['jobs'] if j['id']==a.job]
+    if len(js)!=1:raise ValueError('Unknown or repeated worker identity')
+    out.mkdir(parents=True,mode=0o700)
+    result=dict(job=a.job,plan_sha256=sha(p),completed=False,attempted_model_calls=0,values=[])
+    try:
+        result.update(one_model_job(js[0],m,out))
+    except Exception:
+        result['failure']='worker_exception';traceback.print_exc()
+    write(out/'result.json',result)
+    return 0 if result['completed'] else 2
+
+
+def archived_arrays(m,run):
+    rows=m['rows'];ids=[str(r['r3_row_id']) for r in rows];index={k:i for i,k in enumerate(ids)}
+    target=[i for i,r in enumerate(rows) if r['solvent'] in ana.GLYCOLS]
+    ti={ids[i]:j for j,i in enumerate(target)}
+    arrays={'legacy':np.full((141,2),np.nan),'exact':np.full((141,9),np.nan)}
+    receipt=[];used=set();run=Path(run)
+    for job in m['jobs']:
+        term=run/(job['id']+'.terminal.json');folder=run/job['id'];dest=folder/'result.json'
+        state='missing';attempts=0;hashes={}
+        if term.is_file():
+            t=read(term);hashes['terminal']=sha(term)
+            if t.get('job')!=job['id'] or t.get('plan_sha256')!=sha(m['_plan_path']):raise ValueError('Terminal identity changed')
+            state=t['execution_state']
+            if (not isinstance(t.get('wall_s'),(float,int)) or not np.isfinite(t['wall_s']) or
+                t['wall_s']<0 or t['wall_s']>125.):
+                raise ValueError('Invalid or over-budget worker receipt')
+            if dest.is_file():
+                q=read(dest);hashes['result']=sha(dest)
+                if q.get('job')!=job['id'] or q.get('plan_sha256')!=t['plan_sha256']:
+                    raise ValueError('Result identity changed')
+                attempts=q['attempted_model_calls']
+                if type(attempts) is not int or not 0<=attempts<=len(job['case']['rows']):
+                    raise ValueError('Invalid per-worker model-call count')
+                if q.get('values'):
+                    wanted=[str(r['r3_row_id']) for r in job['case']['rows']]
+                    got=[r['r3_row_id'] for r in q['values']]
+                    if got!=wanted or attempts!=len(wanted):
+                        raise ValueError('Completed worker lost identities or exceeded calls')
+                    j=(('000','UD') if job['phase']=='legacy' else (*ana.CORNERS,'UD')).index(job['corner'])
+                    for v in q['values']:
+                        ident=(job['phase'],v['r3_row_id'],j)
+                        if ident in used:raise ValueError('Duplicate factorial output')
+                        used.add(ident)
+                        i=ti[v['r3_row_id']]
+                        arrays[job['phase']][i,j]=float(v['value']) if v['value'] is not None else np.nan
+                    if q.get('completed') is True and t.get('returncode')==0:
+                        if any(v['value'] is None or not np.isfinite(v['value']) for v in q['values']):
+                            raise ValueError('Completed worker contains nonfinite predictions')
+                        state='completed'
+                    else:
+                        state='failed'
+            progress=folder/'progress.json'
+            if progress.is_file():
+                a=read(progress)['attempted_model_calls']
+                if a<attempts or a>len(job['case']['rows']):raise ValueError('Invalid model-call receipt')
+                attempts=a;hashes['progress']=sha(progress)
+        receipt.append(dict(job=job['id'],state=state,attempted_model_calls=attempts,hashes=hashes))
+    if sum(r['attempted_model_calls'] for r in receipt)>1551:raise ValueError('Model budget exceeded')
+    return arrays,receipt
+
+
+def public_scores(d):
+    """Only aggregate errors and accounting. No paths, predictions, bins or R11 descriptors."""
+    s=d['status']
+    out={k:s[k] for k in ('complete','legacy_requested','legacy_finite','exact_requested','exact_finite',
+        'legacy_parity_passed','legacy_max_error','model','endpoint','adopted')}
+    out['interpretation']='Retrospective ThermoML explanatory scoring; no held-out claim, fitted improvement, or adoption'
+    out['SCF_calls']=0
+    def scalar(value):
+        if value is None:return None
+        if not isinstance(value,(int,float,bool)) or not np.isfinite(value):
+            raise ValueError('Non-scalar data in public error summary')
+        return value
+    def metrics(q):
+        names=('rows','MAE_removed_O_to_C','MAE_remaining_C_to_U','MAE_gap_O_to_U',
+               'signed_recovery_fraction','improved_rows','worsened_rows')
+        z={k:scalar(q[k]) for k in names}
+        for name in ('O','C','U'):z[name]={k:scalar(q[name][k]) for k in ('MAE','bias')}
+        for name in ('absolute_error_reduction_ShAP',):
+            z[name]={k:scalar(q[name][k]) for k in ('area','volume','shape')}
+        return z
+    q=d['aggregate_errors']
+    if q is None:
+        out['aggregate_errors']=None
+    else:
+        solvents=[]
+        if len(q['solvents'])!=4 or {r['key'] for r in q['solvents']}!=set(ana.GLYCOLS):
+            raise ValueError('Changed public solvent universe')
+        for r in q['solvents']:
+            name,n=ana.GLYCOLS[r['key']]
+            if r['name']!=name or r['rows']!=n:raise ValueError('Changed public solvent identity')
+            v=dict(key=r['key'],name=name,**metrics(r))
+            v['legacy_P21']={k:scalar(r['legacy_P21'][k]) for k in ('O_MAE','U_MAE')}
+            v['endpoint_bridge']={k:scalar(r['endpoint_bridge'][k]) for k in ('O_MAE_change','U_MAE_change')}
+            solvents.append(v)
+        out['aggregate_errors']=dict(solvents=solvents,pooled=metrics(q['pooled']),
+            equal_solvent_mean={k:scalar(q['equal_solvent_mean'][k]) for k in
+                ('O_MAE','C_MAE','U_MAE','MAE_removed_O_to_C')},
+            requested_P21_rows=332,audit_only_other_rows=191)
+    return out
+
+
+def collect(p,m,run):
+    mm=dict(m,_plan_path=str(p));arrays,receipts=archived_arrays(mm,run)
+    d=ana.explanatory_scores(m['rows'],arrays['legacy'],arrays['exact'])
+    if any(r['state']!='completed' for r in receipts):
+        d['status']['complete']=False;d['aggregate_errors']=None;d['private_rows']=[]
+    d.update(plan_sha256=sha(p),receipts=receipts,attempted_model_calls=sum(r['attempted_model_calls'] for r in receipts))
+    return d
+
+
+def run_factorial(a):
+    cross.mac_only();os.umask(0o077);p,m=load_plan(a.plan,a.plan_commit)
+    if m['task']!='factorial':raise ValueError('Wrong family')
+    out=private(a.out,fresh=True)
+    if out.is_relative_to(p.parent) or p.parent.is_relative_to(out):raise ValueError('Separate plan and output directories')
+    import secrets
+    nonce=secrets.token_hex(24)
+    claim=dict(plan_sha256=sha(p),plan_commit=a.plan_commit,output=str(out),pid=os.getpid(),nonce=nonce)
+    with (p.parent/'execution_claim.json').open('x') as f:json.dump(claim,f)
+    out.mkdir(parents=True,mode=0o700);start=time.monotonic();receipts=[]
+    env={k:v for k,v in os.environ.items() if not k.startswith('ZC_')}
+    env.update(OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',BLIS_NUM_THREADS='1',
+        VECLIB_MAXIMUM_THREADS='1',NUMEXPR_NUM_THREADS='1',MPLBACKEND='Agg',ZC_R12_NONCE=nonce,
+        PYTHONPATH=str(ROOT/'src')+os.pathsep+str(ROOT/'scripts'))
+    legacy_ok=None
+    for job in m['jobs']:
+        if job['phase']=='exact' and legacy_ok is None:
+            arrays,prior=archived_arrays(dict(m,_plan_path=str(p)),out)
+            old=np.asarray([[r[c] for c in ('000','UD')] for r in m['rows'] if r['solvent'] in ana.GLYCOLS],float)
+            legacy_ids={j['id'] for j in m['jobs'] if j['phase']=='legacy'}
+            legacy_ok=bool(np.isfinite(arrays['legacy']).all() and abs(arrays['legacy']-old).max()<ana.PARITY_TOL and
+                           all(r['state']=='completed' for r in prior if r['job'] in legacy_ids))
+        remaining=7200-(time.monotonic()-start)
+        t=dict(job=job['id'],plan_sha256=sha(p),execution_state='not_run_budget',returncode=None,wall_s=0.)
+        if job['phase']=='exact' and legacy_ok is not True:
+            t['execution_state']='blocked_legacy_gate'
+        elif remaining>2:
+            command=[sys.executable,str(ROOT/'scripts/r12_review.py'),'_worker',
+                     '--plan',str(p),'--job',job['id'],'--out',str(out/job['id'])]
+            try:t.update(cross.launch(command,out/(job['id']+'.log'),min(120.,remaining),env))
+            except Exception:t.update(execution_state='launch_failed')
+        write(out/(job['id']+'.terminal.json'),t);receipts.append(t)
+    # End-of-run integrity is mandatory even for a scientific failure.
+    model_run_wall=time.monotonic()-start;closing_start=time.monotonic()
+    load_plan(p,a.plan_commit)
+    d=collect(p,m,out)
+    d.update(model_run_wall_s=model_run_wall,closing_check_wall_s=time.monotonic()-closing_start,
+             driver_wall_s=time.monotonic()-start)
+    write(out/'summary.json',d);write(out/'public-errors.json',public_scores(d))
+    print('Private explanatory scoring completed:',d['status']['complete'],
+          '; model requests attempted:',d['attempted_model_calls'])
+    return 0 if d['status']['complete'] else 2
+
+
+def regions(a):
+    cross.mac_only();os.umask(0o077);p,m=load_plan(a.plan,a.plan_commit)
+    if m['task']!='regions':raise ValueError('Wrong family')
+    out=private(a.out,fresh=True)
+    with (p.parent/'execution_claim.json').open('x') as f:json.dump(dict(plan_sha256=sha(p),output=str(out)),f)
+    out.mkdir(parents=True,mode=0o700);start=time.monotonic()
+    d=ana.regional_panel(read(Path(m['r11_run'])/'summary.json'));d['plan_sha256']=sha(p)
+    load_plan(p,a.plan_commit)
+    write(out/'regions-private.json',d)
+    write(out/'receipt.json',dict(plan_sha256=sha(p),result_sha256=sha(out/'regions-private.json'),
+          SCF_calls=0,model_calls=0,wall_s=time.monotonic()-start,requested_members=12))
+    print('Private regional accounting completed for 12 members; R11 labels unchanged.')
+    return 0
+
+
+def check(a):
+    p,m=load_plan(a.plan,a.plan_commit);run=private(a.run)
+    claim=read(p.parent/'execution_claim.json')
+    if Path(claim['output']).resolve()!=run or claim['plan_sha256']!=sha(p):raise ValueError('Different claimed run')
+    if m['task']=='regions':
+        d=ana.regional_panel(read(Path(m['r11_run'])/'summary.json'));d['plan_sha256']=sha(p)
+        if d!=read(run/'regions-private.json') or sha(run/'regions-private.json')!=read(run/'receipt.json')['result_sha256']:
+            raise ValueError('Regional results were not reproduced')
+    else:
+        d=collect(p,m,run);old=read(run/'summary.json')
+        for field in ('model_run_wall_s','closing_check_wall_s','driver_wall_s'):
+            value=old.pop(field,None)
+            if not isinstance(value,(int,float)) or not np.isfinite(value) or value<0:
+                raise ValueError('Missing or invalid timing receipt')
+        if d!=old or public_scores(d)!=read(run/'public-errors.json'):
+            raise ValueError('Scoring summary or receipts changed')
+        if not d['status']['complete']:raise ValueError('Incomplete panel; no complete-score claim')
+    print('Saved outputs independently checked without new model calls.')
+    return 0
+
+
+def main():
+    if Path.cwd().resolve()!=ROOT:raise ValueError('Run from this checkout root')
+    p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='cmd',required=True)
+    q=s.add_parser('freeze');q.add_argument('--task',choices=RECORDS,required=True)
+    q.add_argument('--registration',required=True);q.add_argument('--r11-plan',required=True)
+    q.add_argument('--r11-plan-commit',required=True);q.add_argument('--r11-run',required=True)
+    q.add_argument('--p21-run');q.add_argument('--p21-open-profiles');q.add_argument('--out',required=True);q.set_defaults(fn=freeze)
+    for name,fn in (('run',run_factorial),('regions',regions),('check',check)):
+        q=s.add_parser(name);q.add_argument('--plan',required=True);q.add_argument('--plan-commit',required=True)
+        q.add_argument('--run' if name=='check' else '--out',required=True);q.set_defaults(fn=fn)
+    q=s.add_parser('_worker');q.add_argument('--plan',required=True);q.add_argument('--job',required=True)
+    q.add_argument('--out',required=True);q.set_defaults(fn=worker)
+    return p.parse_args()
+
+if __name__=='__main__':
+    a=main();raise SystemExit(a.fn(a))
```
<!-- END PATCH P46P47 -->

<!-- BEGIN PATCH P48 -->
```diff
diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -42,7 +42,8 @@
 response and incomplete finite-difference checks limit stationarity claims.
 The corrected-gradient calibration failed its preregistered compatibility gate;
 no corrected-gradient rollout or chain rescue is accepted. Displacement sensitivity
-does not measure geometry error, and the glycol discrepancy remains unresolved.
+does not measure geometry error, and the liquid-state explanation of the glycol
+discrepancy remains unresolved.
 Z0x was not fitted to ThermoML. Its exact infinite-dilution endpoint passed an
 independent numerical gate and is enabled with `ZC_R6_ENDPOINT=1`. Archived matched benchmark
 comparisons favor UD over open profiles for IDAC and excess enthalpy; the VLE
@@ -58,3 +59,9 @@
 stored conformations, but that observation alone does not separate geometry
 from electronic/cavity effects or identify the liquid-state distribution.
 The glycol mechanism remains unresolved; the numerical-gradient campaign stays closed.
+
+The [round-11 fixed-coordinate cross](docs/astra/round11/RESULTS.md) attributes
+polar-tail gaps mainly to stored coordinate inputs for ethylene, diethylene and
+triethylene glycol. Tetraethylene glycol's raw-tail gap is mainly method; no
+whole-profile attribution label passed. The liquid-conformer distribution and
+the consequences for IDAC error remain unresolved. No crossed profile or conformer-selection rule is adopted.
diff --git a/docs/astra/round7/GLYCOL_STATUS.md b/docs/astra/round7/GLYCOL_STATUS.md
--- a/docs/astra/round7/GLYCOL_STATUS.md
+++ b/docs/astra/round7/GLYCOL_STATUS.md
@@ -39,3 +39,25 @@
 No new quantum calculation, conformer selection or production replacement is
 authorized by this source discovery. The 630 primary and six S1/S2 files stay
 frozen, and the numerical-gradient campaign remains closed.
+
+Update, round 12, based on the completed [round-11 cross](../round11/RESULTS.md).
+For ethylene, diethylene and triethylene glycol, the archived polar-tail gaps
+are mainly due to the stored coordinate inputs under the registered ordered
+open-method comparison. This includes the actual coordinate representation;
+it is not an isolated torsion or hydrogen-bond intervention. Tetraethylene
+glycol is an explicit exception: its raw-tail gap was mainly method, while its
+other tail contrasts were small under the registered rule. No whole-profile
+attribution label passed. The liquid-state conformer mechanism remains unresolved.
+
+This replaces neither a historical result nor a numerical gate. In particular,
+R11's control-derived normalized-shape threshold and its inconclusive headline
+labels stand. A tail fraction is not a fraction of IDAC error explained. The
+proposed R12 scoring and regional analyses consume existing private inputs only;
+no prediction benefit is claimed before they execute. Any score is retrospective
+explanatory ThermoML scoring, not a new fit-free production profile selection.
+
+The native glycol/conformer campaign has no further budget under R12. Archive
+the bounded explanatory findings without adopting a UD structure or fitting
+conformer populations. A future liquid free-energy protocol would require a
+separate prospective design and independent validation. The 630 primary and
+six S1/S2 profiles remain frozen, and the numerical-gradient campaign stays closed.
```
<!-- END PATCH P48 -->

<!-- BEGIN PATCH REG12 -->
```diff
diff --git a/docs/astra/round12/REGISTRATION_PROPOSED.md b/docs/astra/round12/REGISTRATION_PROPOSED.md
new file mode 100644
--- /dev/null
+++ b/docs/astra/round12/REGISTRATION_PROPOSED.md
@@ -0,0 +1,179 @@
+R12-P46-P47-P48: private explanatory scoring and regional accounting
+
+Proposed registration. Adopt and commit this complete text in PREREGISTRATION.md
+before either new plan is frozen or any new R12 output is interpreted. Reference
+main: a93a1c9abbec32e0af7ff259a8db6fa550bb34a9. The design is motivated by already
+inspected R4-R11 outcomes, not by a new held-out experiment. Previous P30/P32
+failures and P33/P37 decisions are not reopened. The numerical-gradient campaign
+stays closed. The 630 primary and six S1/S2 production profiles remain unchanged.
+
+P46 is A explanatory input substitution, with E replay/accounting checks. It
+IS scoring against ThermoML under the optimization brief: experimental ln gamma
+values are used to compute errors. No C profile, geometry, mixture parameter or
+conformer weight may be selected from the result. C is the already frozen R11
+open-method profile at that member's historical UD coordinate input. All such
+data stay on the private asset-bearing Mac. No new quantum calculation,
+optimization, molecular gradient, conformer search or fitted parameter is allowed.
+
+Require the completed R11 private plan, its original committed digest and its
+successful 12-member/24-slot integrity record. Run the original R11 checker,
+retain its package/source/lineage requirements and protect its frozen 630+6
+population. R10/R11 scientific helpers remain unchanged. Freeze hashes of the
+new helpers and every reused input; retain the installed environment. Only
+plan digests enter Git. No coordinates, dense profiles, per-row predictions,
+logs or private paths may be committed or uploaded. Synthetic software tests
+may execute outside the Mac and before registration.
+
+P46 uses the ORIGINAL P21 factorial_rows.csv, summary.json and complete per-pair
+rows, corner predictions and *.csv.inputs.json receipts. The archive must contain
+332 unique r3_row_id observations and 14 solvent identities. Verify every pair's
+solute, solvent, temperature and experimental value against the top-level table.
+Verify per-pair predictions against the original nine output columns. The four
+pre-stated scored identities and row counts are EG LYCAIKOWRPUZTN-UHFFFAOYSA-N (9),
+DEG MTHSVFCYNBDYFN-UHFFFAOYSA-N (108), TEG ZIBGPFATKBEMQZ-UHFFFAOYSA-N (17), and
+tetraEG UWHCKJMYHZGTIT-UHFFFAOYSA-N (7), totaling 141. Selection is by these exact
+keys, not by a solvent-name synonym, error sign or R11 label. TetraEG remains
+included despite its different R11 attribution. The other 191 P21 observations
+remain in the read-only archive identity/hash audit, explicitly outside the new C scoring
+subset. Do not change the 141-row scientific denominator or claim a new 332-row
+C score. The original query rows are not rebuilt from a newer benchmark export.
+
+Use the exact original P21 open solute and open solvent profile bytes. The
+original per-corner receipts must match their SHA256 values, the UD solvent
+bytes and the dielectric.csv, dispersion.csv and Z0.json tables. Recover the
+original snapshot if necessary; do not silently replace it with current files
+whose metadata hashes differ. P21/R11 UD profiles for the four targets must
+match the already verified lineage. Missing, ambiguous or altered archives stop
+preparation. No new SCF is authorized to recreate an absent private artifact.
+
+Before C scoring, replay the original P21 open-solvent (000) and full-UD-solvent
+anchors on the same 141 target observations using the HISTORICAL endpoint
+(ZC_R6_ENDPOINT=0). This is 2*141=282 requested lngamma_inf evaluations. Audit
+all 332 original archive identities and all nine per-corner stored outputs and
+input receipts without new model calls. Check the archived 111/full-UD identity
+to 1e-10. The 282 fresh anchor identities and finite coverage must match;
+maximum absolute replay difference must be strictly below 1e-8 in ln gamma.
+This is a same-input anchor gate, not a claim that every historical intermediate
+corner was recalculated, or a relaxation of E/P32/scientific accuracy gates.
+If anchor replay fails, record the failure and block every C-scoring job.
+Do not change a solver or endpoint to make the old comparison pass.
+
+The primary new evaluation uses the accepted P28 EXACT endpoint consistently
+for O, all C-factorial corners and the full U solvent (ZC_R6_ENDPOINT=1).
+For every one of the 141 rows, evaluate the eight O-to-C corners and U: 1269
+requested calls. Keep the solute's original open profile in every corner.
+Bit order is area, cavity volume, normalized 153-bin shape, exactly as P21.
+For bit vector (a,v,s), use A=A_C if a else A_O; V=V_C if v else V_O;
+and the shape C/A_C if s else O/A_O. Multiply the chosen normalized shape by
+the chosen area. Retain original open metadata in the factorial. Z0x's physical
+constants, chemical dielectric data, London data and chemical identities are
+unchanged. The full-U anchor uses the original UD solvent file. This is not
+an all-UD mixture and no solute is replaced merely because it is another glycol.
+
+One worker handles one ordered pair and one corner in a fresh process. Its
+temporary overlay must resolve BOTH requested profiles explicitly; a missing
+open solute cannot fall back to UD. Clear inherited ZC_* experiment switches
+and set the declared endpoint and private overlay before model construction.
+Do not reuse a process-global profile cache across corners. No new data loader,
+segment solver, endpoint approximation or physical model is introduced.
+
+The maximum is 1551 requested model API calls, zero SCFs and zero gradients.
+The job count is 11 times the number of target ordered pairs, computed from
+the frozen inputs, not guessed here. The two replay anchors precede the nine
+new endpoint-consistent evaluations for each target observation. Calls denote lngamma_inf
+requests, not individual internal segment iterations. Run serially on the Mac,
+with at most four OpenMP threads and one BLAS thread. Each worker has 120 seconds;
+the model-run allocation is 7200 seconds including orchestration. A process-group
+kill/accounting allowance of five seconds is not extra scientific computation.
+Record closing zero-model integrity/aggregation time separately if it extends
+the allocation. No parallel cloud workflow, paid resource, retry, resumption,
+stale-claim deletion or second run of a claimed plan is authorized. Every
+planned job retains a terminal state, even when it is blocked or never starts.
+
+Failure handling is part of the design. Preserve requested row identities and
+finite/nonfinite counts for every arm. Do not form a smaller favorable intersection.
+A failed historical replay blocks the new stage. A missing, failed or nonfinite
+new result blocks complete-panel error summaries; retain its diagnostic receipt
+and the remaining completed values privately. A green process or workflow state
+is not numerical acceptance. Independent jobs continue within the fixed budget.
+The original input hashes and the protected production population are rechecked
+after execution. Checks of saved output may be repeated without new model calls.
+
+Report errors on the 141 fixed rows per solvent, pooled with original row weights,
+and with equal solvent weighting as a declared secondary summary. DEG contributes
+108 of 141 rows to the pooled score. For y_O,y_C,y_U and experimental y, report
+MAE and bias. The removed absolute error is mean(|y_O-y|-|y_C-y|); the remaining
+UD-comparator gap is mean(|y_C-y|-|y_U-y|). Their sum must equal the O-to-U MAE
+gap. A recovery fraction is reported only for a positive denominator above
+1e-6, is signed and is never clipped to [0,1]. Negative values and values above
+one remain visible. No confidence interval, success threshold or production
+acceptance is inferred from this retrospective fraction.
+
+Apply the unchanged P21 shapley_three function twice to the complete eight-corner
+cube: once to predictions and once to negative absolute errors. The second
+calculation gives additive area/volume/shape contributions to absolute-error
+reduction. Taking absolute values of prediction Shapley terms is not equivalent.
+Require both efficiency identities to 1e-10. Positive/negative contributions and
+interactions remain visible. A C-minus-O prediction change is not automatically
+an error reduction. Report the legacy-versus-P28 O and U endpoint bridge on the
+same target rows; never subtract a legacy O score from an exact C score. No
+post-P28 value overwrites P21 or a historical scorecard.
+
+The original P21 profile is the primary baseline, even if its bytes differ from
+the R11 repeat. Hence P46 is explicitly a FROZEN-INPUT C-substitution explanation.
+It is not a new pure torsional or hydrogen-bond causal estimate, and it does not
+relabel the R11 profile decomposition. Dense per-row values and counterfactual
+profiles stay private. Prediction Shapley values remain private; only aggregate bias and MAE statistics
+and absolute-error-reduction Shapley values enter the public allowlist.
+Only that aggregate error summary is eligible for separate human review before publication. The software never
+uploads or copies it into Git. Publish improvements and deteriorations under
+the same predetermined headings, clearly labelled retrospective explanatory
+ThermoML scoring, not a fitted improvement or a new validated profile version.
+
+P47 is an independent E read-only analysis with zero QC and zero model calls.
+Freeze its own plan digest, so it can proceed even if the P21 archive is absent.
+Use all twelve verified R11 members and all four archived profile families:
+U (UD), A (P25 archive), R (fresh open-geometry repeat), C (crossed UD geometry).
+Normalize each family by its OWN area before taking a normalized difference.
+Use D=U-R, G=C-R, M=U-C and repeat drift R-A. Preserve the R11 classification
+object unchanged, including the 0.359 realized scale and all inconclusive labels.
+Do not substitute a new eta, exclude water, subtract a background vector, or
+reinterpret the regions as independent hypothesis tests.
+
+Partition the fixed 51-point sigma grid by integer millithresholds into five
+bands: sigma<=-0.010; -0.010<sigma<=-0.005; |sigma|<0.005;
+0.005<=sigma<0.010; sigma>=0.010 e/A2. Cross these bands with the existing NHB,
+OH and OT channels. Each of the 153 entries belongs to exactly one of 15 cells.
+Report each cell's signed mass change, L1 contribution and first moment, for
+unnormalized and normalized profiles separately. Regional L1 shares sum to one
+when the total is nonzero; use null for zero-total shares. Require conservation
+of signed mass, L1 and moments to the implemented 1e-12 scaled arithmetic bound.
+Also collapse the HB channels at each sigma and report L1_153-L1_51, the amount
+of channel cancellation hidden by a total-profile projection. This is a
+representation diagnostic, not an attribution to an HB energy term.
+
+The positive and negative OH/OT regions use the existing acceptor-side and
+donor-side parser convention. NHB entries remain NHB irrespective of sign.
+The centre is a low-|sigma| region, not a proof of nonpolar chemistry. Raw
+outlier tesserae and net surface charge are not reconstructed from a normalized,
+smoothed histogram. P47 cannot infer a nonlinear ln gamma contribution from a
+regional profile norm. All region tables remain private; no regional or dense
+profile data are included in P46's public error summary.
+
+P48 records the scope of the established result. The polar-tail gaps for EG,
+DEG and TEG are mainly due to stored coordinate inputs under the registered
+ordered open-method cross. TetraEG is an explicit exception, with a mainly-method
+raw-tail gap and small other tail contrasts. No whole-profile attribution label
+passed. No conformation is thereby established as the liquid distribution, no
+UD structure is adopted, and no IDAC improvement is claimed before P46 executes.
+The numerical-gradient campaign remains closed.
+
+After these bounded read-only/explanatory tasks, archive the findings whether
+favorable, unfavorable, operationally incomplete or inconclusive. The liquid-
+state mechanism and a production conformer rule remain unresolved. R12 provides
+no native or ensemble budget and no automatic continuation. A phase-dependent
+free-energy protocol would require separately validated basin populations,
+thermal contributions and common reference conventions on the full eligible
+class and controls; the existing finite samples and R11 single points do not
+supply them. A cheap calculation on incomplete inputs is not acceptance of such
+a protocol. Historical profiles and scientific decisions remain unchanged.
```
<!-- END PATCH REG12 -->

Source references are pinned to the reviewed main; they identify evidence, not newly executed experiments. The original UD data are not bundled.

| Reference | Scope | Location |
|---|---|---|
| S1 | Round-12 task and unchanged optimization rules | [ROUND12_PROMPT.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/a93a1c9abbec32e0af7ff259a8db6fa550bb34a9/docs/astra/ROUND12_PROMPT.md), [OPTIMIZATION_BRIEF.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/a93a1c9abbec32e0af7ff259a8db6fa550bb34a9/docs/OPTIMIZATION_BRIEF.md) |
| S2 | Measured R11 calls, parity, tail and whole-profile labels | [R11 RESULTS](https://github.com/Victor-Liang-ChE/zcosmo/blob/a93a1c9abbec32e0af7ff259a8db6fa550bb34a9/docs/astra/round11/RESULTS.md) |
| S3 | The complete R11 design, interpretation and free-energy discussion | [R11 report](https://github.com/Victor-Liang-ChE/zcosmo/blob/a93a1c9abbec32e0af7ff259a8db6fa550bb34a9/docs/astra/round11/ZCOSMO_ROUND11_REPORT.md), [R10 results](https://github.com/Victor-Liang-ChE/zcosmo/blob/a93a1c9abbec32e0af7ff259a8db6fa550bb34a9/docs/astra/round10/RESULTS.md) |
| S4 | R10/R11 registrations, usage restrictions and outcomes | [PREREGISTRATION.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/a93a1c9abbec32e0af7ff259a8db6fa550bb34a9/PREREGISTRATION.md) |
| S5 | Actual R11 input schema, checker and classifications | [r11_cross.py](https://github.com/Victor-Liang-ChE/zcosmo/blob/a93a1c9abbec32e0af7ff259a8db6fa550bb34a9/scripts/r11_cross.py), [r11_analysis.py](https://github.com/Victor-Liang-ChE/zcosmo/blob/a93a1c9abbec32e0af7ff259a8db6fa550bb34a9/scripts/r11_analysis.py), [r10_replay.py](https://github.com/Victor-Liang-ChE/zcosmo/blob/a93a1c9abbec32e0af7ff259a8db6fa550bb34a9/scripts/r10_replay.py), [r10_sources.py](https://github.com/Victor-Liang-ChE/zcosmo/blob/a93a1c9abbec32e0af7ff259a8db6fa550bb34a9/scripts/r10_sources.py) |
| S6 | P21 factorial mechanism and original denominators | [r4_glycols.py](https://github.com/Victor-Liang-ChE/zcosmo/blob/a93a1c9abbec32e0af7ff259a8db6fa550bb34a9/scripts/r4_glycols.py), [R4 RESULTS](https://github.com/Victor-Liang-ChE/zcosmo/blob/a93a1c9abbec32e0af7ff259a8db6fa550bb34a9/docs/astra/round4/RESULTS.md) |
| S7 | Unchanged sigma parser and archived open-table adapter | [to_sigma.py](https://github.com/Victor-Liang-ChE/zcosmo/blob/a93a1c9abbec32e0af7ff259a8db6fa550bb34a9/data/raw/nist/to_sigma.py), [r4_common.py](https://github.com/Victor-Liang-ChE/zcosmo/blob/a93a1c9abbec32e0af7ff259a8db6fa550bb34a9/scripts/r4_common.py), [r5_shape.py](https://github.com/Victor-Liang-ChE/zcosmo/blob/a93a1c9abbec32e0af7ff259a8db6fa550bb34a9/scripts/r5_shape.py) |
| S8 | Current Z0x/loader behavior and accepted endpoint scope | [z0x.py](https://github.com/Victor-Liang-ChE/zcosmo/blob/a93a1c9abbec32e0af7ff259a8db6fa550bb34a9/src/zcosmo/z0x.py), [cosmosac.py](https://github.com/Victor-Liang-ChE/zcosmo/blob/a93a1c9abbec32e0af7ff259a8db6fa550bb34a9/src/zcosmo/cosmosac.py), [models.py](https://github.com/Victor-Liang-ChE/zcosmo/blob/a93a1c9abbec32e0af7ff259a8db6fa550bb34a9/src/zcosmo/models.py), [P28 acceptance](https://github.com/Victor-Liang-ChE/zcosmo/blob/a93a1c9abbec32e0af7ff259a8db6fa550bb34a9/docs/astra/round6/RESULTS.md) |
| S9 | Current wording and scope of P35 | [README](https://github.com/Victor-Liang-ChE/zcosmo/blob/a93a1c9abbec32e0af7ff259a8db6fa550bb34a9/README.md), [GLYCOL_STATUS.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/a93a1c9abbec32e0af7ff259a8db6fa550bb34a9/docs/astra/round7/GLYCOL_STATUS.md) |
| U1 | Primary evidence that solution-phase conformer treatments exist, not validation of Z0x or a cost estimate | Pung and Leito, [Predicting Relative Stability of Conformers in Solution with COSMO-RS](https://pubs.acs.org/doi/10.1021/acs.jpca.7b05197), J. Phys. Chem. A 121 (2017), 6823–6829. |

The local verification record is separate from scientific acceptance.

| Check | Executed outcome |
|---|---|
| Baseline verification | Eleven reused/touched source files and the complete R11 report matched their connector-reported Git blobs. Relevant-file reconstruction only. |
| Patches | All four apply independently and together. Applied files match the candidate bytes. |
| Software suites | 26 R12, 22 R11 and 20 R10 tests pass on the combined applied tree. Synthetic chemistry/model fixtures only. |
| Commands | CLI help and Python compilation passed; shell blocks and embedded Python were syntax checked. Patch extraction from this report was checked. |
| Native/private acceptance | Not executed. No PySCF installation, real activity-model evaluation, Mac registration, private asset analysis, Actions dispatch or production change. |

| Extractable patch | SHA256 of the extracted UTF-8 patch, including final newline |
|---|---|
| H12 | `e9dc3d64018d99a447ef6d3276f74cee89361b5ab65013ded6f6835ce098aaf3` |
| P46P47 | `3901ce8d3bd6d1c93396151ab2e6cb6be1dec1626a047ee99327e921b30aef99` |
| P48 | `94b23d014d5ae5e78d2aeff24035085d14016f13ccf1e6290ffb3adce7fd81f5` |
| REG12 | `647e672b7510d977072a89ef81e9b69a035762180c697047a7a3f7411389c995` |

P35 can be archived with a coordinate-input explanation for the EG/DEG/TEG polar-tail contrasts, the tetraEG exception and unchanged whole-profile labels. Liquid-state mechanism and production conformer selection remain unresolved. A later P46 outcome may describe an inspected prediction-error change, but it cannot accept a profile or reopen a native campaign.
