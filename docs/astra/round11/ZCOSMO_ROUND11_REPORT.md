Z-COSMO round 11: the missing fixed-geometry cross, without a conformer-selection claim

Reference: `Victor-Liang-ChE/zcosmo`, `main = 463ec1be5c0edfad1e8effd334a17fc44cd27405`. The round-11 prompt and the completed R10 lineage comparison govern this design. The four extractable patches below target that snapshot. R8/R9's numerical-gradient campaign remains closed, and the 630 primary profiles plus six flagged S1/S2 files remain unchanged. This report proposes an experiment; it does not record its adoption or execution. [S1–S4]

| Rank | ID | Target | Class | Mechanism, expected cost and saving | Effort |
|---:|---|---|---|---|---|
| 1 | P44 | `scripts/r11_cross.py`: `freeze`, `single_point`, `runner`, `collect`, `check` | A coordinate-input diagnostic; E same-input integrity controls | Twelve missing crossed single points and twelve fresh open-geometry controls. The SCF algorithm is unchanged, so no per-call acceleration is claimed. Reuse both archived input families instead of regenerating them or restarting optimizations. At most 24 SCF attempts, six hours of serial native slots. | Moderate |
| 2 | P45 | README and `docs/astra/round10/RESULTS.md` | E reporting | Record the completed lineage result and correct the scope of the control/provenance language. Zero native or activity-model calls. | Low |
| Shared | H11 | `r11_analysis.py`, `r11_selftest.py`, two R10 test assertions | E arithmetic/test infrastructure | Exact telescoping accounting, fixed effect-size decisions and privacy/failure tests. Does not change a physical model. | Moderate |
| Record | REG11 | `docs/astra/round11/REGISTRATION_PROPOSED.md` | Prospective policy | Fix inputs, thresholds and budgets before any new output. No automatic profile promotion. | Low |

P44 has direct decision value because it measures the quantity missing from R10. There is no evidence-based numerical probability of finding geometry dominance, and no invented expected accuracy gain. Its wall cost is `sum_i(t_RO,i + t_RU,i)`, not an extrapolation from R10's 2.9-second parser replay. The saving is avoiding an additional geometry search or method sweep: neither is needed to measure this ordered contrast. The 24-call design is the smallest one with a fresh native same-input control for every one of the twelve requested crosses. A twelve-call cross-only design could reuse old tables, but would not test current native reproducibility for each member. [S2, S5]

The experiment that should be registered

Run the existing P25 BP86/def2-TZVP, density-fitted, grid-level-3, SWIG C-PCM single point at each recovered UD geometry, with epsilon `1e9`, Lebedev order 29, project radii and `conv_tol=1e-9`. Use the existing `r4_charge.factory` and `segments`, which P25's `tz_swig` branch already uses. The default orbital-gradient tolerance and maximum SCF iterations stay unchanged. Preserve the `area > 1e-8 bohr^2` extraction filter and the actual `q` field. Do not substitute `q_sym`, neutralize charge, change the cavity or choose another initial-guess recipe. All members are the same neutral, closed-shell panel. The implementation checks the declared settings and records the auxiliary basis and loaded upstream source hashes. [S5, S6]

A fresh calculation at the exact P25 open geometry accompanies each cross. Both origins keep their own stored atom order and laboratory orientation. Alignment is useful for describing structures, but rotating the UD input before this calculation would define a different finite-grid experiment. “Geometry” therefore means the complete coordinate-input change, including hydrogen coordinates and any orientation dependence. It does not isolate a torsion, an OH approach, or intramolecular hydrogen bonding. Propylene glycol retains the explicit stereospecific-UD/unspecified-benchmark alias from R10; no atom mapping is used to make those declarations identical. [S3, S5]

There is no optimization and no nuclear-gradient evaluation. An SCF result at a frozen geometry is meaningful without claiming that geometry is stationary. This is not a continuation of P30, P32 or P37. A successful result measures a profile contrast within the specified finite-basis, finite-grid method; it does not establish basis/grid/response convergence or the physical accuracy of the UD reference. [S1, S4]

Let the unnormalized 153-bin area profiles be

\[
 U=p_U(R_U),\quad A=p_O^{\rm P25}(R_O),\quad
 R=p_O^{\rm R11}(R_O),\quad C=p_O^{\rm R11}(R_U).
\]

The report must retain the requested historical decomposition and the fresh paired decomposition:

\[
\begin{aligned}
 U-A&=\underbrace{C-A}_{\text{historical geometry term}}+
       \underbrace{U-C}_{\text{method term}},\\
 U-R&=\underbrace{C-R}_{\text{current coordinate term}}+
       \underbrace{U-C}_{\text{same-geometry method term}},\\
 C-A&=(C-R)+(R-A).
\end{aligned}
\]

The last term, `R-A`, is native repeat drift. Hiding it in the coordinate term would confound the new result with a platform or implementation difference. H11 checks these identities directly, stores the full differences privately, and reports scalar summaries. It repeats the calculation after separately normalizing each profile by its own total area. Normalizing a difference is not equivalent.

The same algebra applies separately to the raw tessera tail, the continuously averaged tessera tail and the final binned tail. All use the existing inclusive `|sigma| >= 0.01 e/A^2` convention, with the output-grid coordinates rounded to three decimals for the final-bin test. Tesserae from different surfaces are never paired by ordinal. The method term includes the remaining electronic/cavity and surface-representation bundle, including whatever charge convention is present in the archived UD table. It is not a pure functional or basis-set effect. [S5]

This is an ordered decomposition. The uncomputed reverse corner `p_U(R_O)` would be needed to assess the corresponding two-method interaction and reverse ordering. No unique, method-independent causal percentage is identified. Also, a decomposition of profiles or their tail areas is not a decomposition of IDAC MAE: the activity model is nonlinear. R11 performs zero activity-model calls and makes no claim about the percentage of the experimental error explained.

The same-input acceptance checks

The old R10 manifest and successful summary must pass their original hash, identity, package and lineage checks. The private plan is not reconstructed from whichever files happen to be newest. For each fresh RO single point, the following strict limits are applied against its own P25 archive, before any full-panel attribution label is permitted.

| Repeat quantity | Required absolute difference |
|---|---:|
| Maximum unnormalized profile bin | `< 1e-4 A^2` |
| Separately normalized 153-bin L1 distance | `< 1e-5` |
| Total SCF energy | `< 1e-7 Eh` |
| Retained net surface charge | `< 1e-5 e` |
| Total retained area | `< 1e-4 A^2` |
| Cavity volume | `< 1e-4 A^3` |

These are prospective same-input reproducibility limits, not a relaxation of P32 or a requirement to match UD. They combine a bin-scale integrity limit with independent energy and charge checks. No different-geometry result is described as E-equivalent. The original 25/2,302 affinity gate is not executed or claimed satisfied by R11. A large, well-controlled crossed difference is a valid scientific outcome rather than a failed accuracy gate. A native failure, parser failure or repeat-parity failure blocks complete-panel labels and remains visible in the denominator. [S1, S4]

Decision rules fixed before any cross is computed

The four background controls are water, methanol, methoxyethanol and THF. They are near-matching heavy-atom controls, not exact coordinate nulls. Their observed discrepancies include real method and geometry differences. Calling them a random-noise estimate would be incorrect. Methoxyethanol is flexible; water's one-heavy-atom aligned RMSD says nothing about its O-H bond geometry. [S2, S3]

For each tail observable independently, define the background scale

\[
 \eta=\max\left(0.5\ {\rm A^2},\;
       \max_{i\in\mathcal C}|U_i-R_i|,\;
       \max_{i\in\mathcal C}|C_i-R_i|,\;
       4\max_{i\in\mathcal P}|R_i-A_i|\right),
\]

Here the control set contains the four named members and the full panel contains all twelve; the capital C used for a crossed result is distinct from the control-set symbol. For normalized-profile comparisons, use the same formula with L1 norms and a `0.01` floor. The formula, control membership and floors are fixed now; the realized scales are printed with the results. This is a conservative engineering background envelope, not a confidence interval or a convergence certificate. Including the measured control coordinate terms prevents treating a near-match as an exact null. No control may be dropped because it enlarges the envelope.

For any signed tail contrast set `D=U-R`, `G=C-R`, `M=U-C`. Use the following rules in the stated order.

| Decision | Pre-stated condition and meaning |
|---|---|
| Inconclusive cancellation | `G*M < 0` and `min(abs(G),abs(M)) > eta`. Material terms oppose one another; do not report a simple dominance percentage. |
| Inconclusive small contrast | `abs(D) <= 2*eta`. The net gap is not separated from the control/background scale. |
| Mainly geometry | `G*D > 0`, `abs(G) > eta`, and `abs(M) <= max(eta,abs(D)/4)`. The residual method term is small relative to the declared effect scale. |
| Mainly method | The previous rule with G and M exchanged. |
| Both | Neither dominance rule holds, both terms have D's sign, and each magnitude exceeds eta. |
| Inconclusive borderline | Everything else. |

For the normalized 153-bin vectors, calculate `Dn=||D||1`, `Gn=||G||1`, `Mn=||M||1` and cancellation excess `Gn+Mn-Dn`. Excess greater than `max(2*eta,Dn/4)` is inconclusive cancellation. Otherwise apply the small-contrast rule and the corresponding remainder tests to the norms. The code reports all norms, not just a label. These operational labels describe the specified observable, not which method or conformation is physically correct.

Every metric is classified again using the archived RO result A. A label that changes solely from using A rather than the validated fresh repeat R becomes `inconclusive_repeat_boundary`. For a non-control member, a broad profile-gap label is issued only when its final-tail and normalized-shape labels agree on geometry, method or both. Otherwise it remains metric-dependent or inconclusive. Raw and averaged tails retain their separate labels even when the final bins tell a different story. Charge diagnostics cannot break a tie.

The following schedule fixes the treatment of every member. “G/M/B rules” means the decision table plus the normalized-shape concurrence requirement, not a prediction of the outcome.

| Member | Pre-stated treatment |
|---|---|
| Ethylene glycol | Apply G/M/B rules independently; a result does not generalize automatically to its homologues. |
| Diethylene glycol | Apply the same rules, with no special weighting for its larger experimental-row count. |
| Triethylene glycol | Apply the same rules at its recovered geometry; no restart of the gradient referee. |
| Tetraethylene glycol | Apply the same rules. A near-zero averaged-tail gap and a nonzero final-bin gap remain distinct outcomes. |
| Glycerol | Apply the signed rules unchanged. A negative UD-minus-open tail gap is not relabelled an error or excluded. |
| Propylene glycol | Apply the signed rules unchanged, retaining the R10 stereochemical-alias qualification. |
| Methoxyethanol | Background control; report G, M and all distributions descriptively. Do not call it a rigid exact-geometry null. |
| Dimethoxyethane | Apply the same rules. Similar final tails can make the scalar result inconclusive while shape information remains descriptive. |
| Water | Background control; report the cross despite its zero aligned heavy-atom RMSD. |
| Methanol | Background control, with the actual hydrogen geometry retained. |
| Tetrahydrofuran | Background control, with its actual ring geometry retained. |
| n-Nonane | Apply the same rules; an essentially zero polar tail is not evidence of profile equivalence. No invented polar-tail fraction. |

Because every control contributes its own `abs(D)` to eta, its tail contrast cannot itself pass the panel's `abs(D)>2*eta` signal criterion. That is intentional: controls establish the descriptive background and are not independently declared geometry- or method-dominant using a scale they helped define. All twelve still have their requested signed terms calculated. Missing any native/parity result makes the panel incomplete; the implementation does not manufacture a background scale from whichever controls succeeded.

Net charge and extreme tesserae

Record the complete native PCM charge sum, the retained sum and the discarded sum under the unchanged filter. Check charge/area conservation across that filter, the electron-count error `|Tr(PS)-N| <= 1e-7 e`, and the PCM linear-system relative residual `<= 1e-10`. The presence of a nonzero screening charge is not a failure in this experiment. For UD, retain the actual parsed column and the already audited printed-summary distinction; do not pick a correction convention by proximity to zero. [S5, S6]

For retained segments, report minimum/maximum charge density and discrete area-weighted quantiles. At the fixed cuts `sigma < -0.025` and `sigma > +0.025 e/A^2`, report segment counts and area fractions, together with signed and absolute charge contributions. Pre-filter extrema and discarded charge/area are stored separately. This distinguishes a very negative density on a tiny patch from a substantial portion of the molecular surface. No outlier is clipped, neutralized or silently omitted. A profile-domain failure preserves the completed raw single point privately but blocks that slot's profile acceptance.

The net-charge decomposition is reported alongside the profile terms. Geometry dominance in the polar-tail metric can coexist with a method-dependent net charge. Neither a close net-charge sum nor a small tail residual establishes that two full electrostatic calculations are equivalent.

Execution and privacy budget

All actual input preparation, SCFs and UD-backed collection run on the private Mac. The code refuses Linux and CI execution. It reuses the established R10 manifest, package versions and frozen population; it never downloads a replacement raw table or re-embeds a missing geometry. New plan and output locations must be outside every Git checkout, including symlink-resolved paths. Only the plan digest is committed. Dense profiles, raw surface tables and coordinates remain private. The public aggregate JSON is an explicit field allowlist and requires operator review before publication. [S1–S4]

There are 24 fresh subprocess slots, run serially with four OpenMP threads, one BLAS thread, 4000 MB nominal PySCF memory and a 2000 MB PCM integral cache. The fixed SHA256-key parity determines which origin runs first within each member. Each slot has a 900-second process-group deadline, including postprocessing. Thus `24*900=21600 s`, six hours, is the reserved native-slot ceiling. The driver allocation is 22500 seconds, six hours fifteen minutes including orchestration; remaining slots are not started when it is spent. A five-second process-kill/accounting allowance is not a scientific extension. Final zero-QC verification is timed separately. These are prospective budget ceilings, not measured runtimes or a promise that every member will finish.

A permanent exclusive claim binds one plan to one execution. A timeout or interruption does not permit a new output directory to restart it. Independent slots continue after a failed member, all requested identities remain, and the collector distinguishes incomplete execution from a complete scientific outcome. Partial results receive no complete-panel attribution label. A parser failure does not authorize changing a threshold or running another SCF.

PySCF also searches working-directory and home `.pyscf_conf.py` files, even when `PYSCF_CONFIG_FILE` is unset. The helper rejects all these configuration routes before native import; checking only the environment variable would be insufficient. It records the runtime SCF settings instead of relying on docstring defaults. No automatic package upgrade is included. [U1]

What a geometry answer would justify

A dominant coordinate term would establish that changing the stored coordinate input, while holding this open single-point recipe fixed, accounts for most of the measured profile contrast under the declared effect-size rules. It would not establish that an extended chain is the equilibrium liquid conformation, that the folded state is wrong, or that an OH approach failing the registered angle criterion should now be called a hydrogen bond. It would also not justify selecting geometries by their agreement with UD or ThermoML. The UD notice describes empirical conformation revision at database level, without identifying which members of this glycol panel were revised. That qualification applies even when the particular raw input lineage is established. [S2–S4]

There is a defensible class of prospective conformer rules: determine phase-dependent basin populations from one declared free-energy functional. It is not a defensible production change merely to choose the lowest of R11's conductor single-point energies. Those coordinates need not be minima, the calculations contain no basin partition functions, and a conductor electronic energy is not a liquid free energy.

For example, a future model could define basin amounts `n_ik=n_i*w_ik` and minimize

\[
 \mathcal G^\alpha=
 \sum_{ik}n_{ik}a^0_{ik}(T)
 +RT\sum_{ik}n_{ik}\ln\!\left(\frac{w_{ik}}{g_{ik}}\right)
 +G_{\rm inter}^\alpha(T,P,\{n_{ik}\}),
 \qquad \sum_k w_{ik}=1.
\]

Here `a0` contains the electronic and nuclear basin contributions on one consistent reference, `g` is an audited multiplicity, and `G_inter` uses transfer and interaction terms compatible with that reference. Stationarity gives the self-consistent relation

\[
 w_{ik}\ \propto\ g_{ik}\exp\!\left[-\frac{a^0_{ik}+\partial G_{\rm inter}^\alpha/\partial n_{ik}}{RT}\right].
\]

A conductor reference would require compatible transfer/self-contact standards so its polarization is not counted twice. The equation defines a class of closures, not a unique physical model inferable from a sigma histogram. It also shows why the neat-liquid population and infinite-dilution population generally require separate calculations. Phase-dependent multi-species treatment is documented in other COSMO models, but that does not validate a Z0x closure or confer fit-free status on another implementation's parameters. [U2]

Such a future rule would have to be declared for the full eligible polyol class, with water and the branched controls retained, rather than only for the glycols with unfavorable scores. Candidate basins and symmetry correspondence would be determined independently of experimental error. The nuclear partition and low-barrier torsions need controlled treatment, not absolute-valued imaginary modes or a fitted frequency floor. Independent discovery pools would have to agree on chemical free energies and relevant predictions under fixed acceptance criteria. Existing incomplete conformer pools and agreement of electronic minima alone do not meet those requirements. [S4]

Even a validated population average does not imply `ln gamma(average profile) = average ln gamma`, nor does it automatically reduce to one universal structure. Choosing one representative would be an additional compression approximation requiring its own prospective error test. R11 therefore remains explanatory only for production purposes. It supplies no conformer-selection implementation, new ensemble budget or permission to replace a profile. A new, independently validated phase-free-energy protocol could be defensible later; the outcome of P44 alone cannot accept it.

Wording corrections and current-code findings

The README's main numerical/accuracy qualifications are sound. Its last paragraph is stale because R10's lineage comparison has now completed. P45 replaces only that paragraph, records all twelve matches, and keeps the unresolved mechanism and closed gradient campaign explicit. [S7]

R10 RESULTS needs narrower control language. Heavy-atom RMSD below 0.02 A is not exact all-atom equality; in water, the one heavy atom makes that statistic especially uninformative about O-H geometry. Methoxyethanol is not rigid. The observed small control differences remain useful, but should not be named a pure matched-geometry method effect before the cross exists. The sentence implying particular extended glycol structures were empirically revised is also too specific: the provenance record supplies no per-glycol revision label. [S2, S3]

There is a separate sign correction. P21 reports glycerol's mean normalized-shape Shapley contribution as small and positive, `+0.037` in ln gamma, whereas propylene glycol's is negative, `-0.861`. R10's statement that both had the opposite sign conflates the profile-tail direction and the prediction attribution. P45 preserves the measured descriptors and clarifies the comparison. It also replaces “nothing was computed” with the accurate statement that no new quantum-chemistry or activity-model evaluation was performed. These are reporting changes, not revisions to a numerical gate. [S8]

The two failing R10 tests compare resolved private paths with unresolved expected paths. H11 changes only the expected values to `.resolve()`, including the macOS `/var` alias case. It does not weaken the underlying private-path or input-mutation checks. The unchanged R10 scientific helper fingerprints continue to validate the existing manifest. [S2, S5]

The source itself provides a usable minimal route: P25 already separates the factory, retained surface extraction and same-parser adaptation. Copying a new SCF implementation or adding another smoothing routine would create avoidable validation work. P44 instead imports those helpers, and H11 retains the R10 stage definitions. No defect in the native electrostatics is declared from this software-only review.

Executed and not executed

Executed here: Git-blob verification of the relevant baseline files and the full mounted R10 report; all four independent patch checks and a combined application; Python compilation and CLI-help checks; shell syntax and embedded-Python syntax checks for the commands; 22 new portable tests and the 20 existing R10 tests after the two assertion fixes. The applied-tree suites also passed. The new tests include a synthetic twelve-member collection and independent checker, altered-native/altered-summary rejection, cancellation and boundary decisions, alias-safe private paths, a real subprocess timeout, a mocked one-kernel/no-gradient native interface, and preservation of raw output after a synthetic parser failure.

The local baseline is a verified reconstruction of the relevant subset, not a full repository clone. Native tests use synthetic arrays and mock factories, not real PySCF integrals. Registration ancestry and the actual Mac asset-backed freeze/run/check remain unexecuted here. No UD coordinates or raw tables were retrieved or numerically replayed in this review. PySCF is absent from the runtime, and installation was not attempted because the actual calculation is explicitly Mac-only. No new SCF, optimization, quantum gradient, activity-model evaluation, Actions dispatch or repository write was performed. No production file changed. The verification record at the end distinguishes these software checks from future scientific acceptance.

Commands for the maintainer

The commands use the already installed Mac environment from R10, with PySCF 2.14.0 and unchanged parser dependencies. `R10` defaults to the private location prescribed in the R10 report; it is not an assertion that a file exists in a newly created worktree. Set that variable to the actual completed R10 run when necessary. Preparation verifies its original committed plan digest and all existing data hashes. There is no fallback to a different profile root or newly computed asset. `REPORT` identifies this saved Markdown file. All four patches must be applied before the portable tests, because H11 and P44 share imports.

The first block applies and registers the proposed work locally, then freezes the private plan. The single native run and its checks are explicit. A nonzero result stops the command sequence without a retry. Only aggregate timing is printed afterward; detailed outputs remain private. These commands were syntax-checked, not executed against the Mac or the real repository.

```bash
# Run from the current Mac checkout. REPORT points to the saved report.
set -euo pipefail
export BASE=463ec1be5c0edfad1e8effd334a17fc44cd27405
: "${REPORT:?Set REPORT to the saved ZCOSMO_ROUND11_REPORT.md}"
export PATCHDIR="${PATCHDIR:-${TMPDIR:-/tmp}/zc-r11-patches}"
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
for name in ('H11','P44','P45','REG11'):
    pattern=r'<!-- BEGIN PATCH '+name+r' -->\s*```diff\n(.*?)\n```\s*<!-- END PATCH '+name+r' -->'
    found=re.findall(pattern,text,re.S)
    if len(found)!=1:raise ValueError('Missing or duplicate patch '+name)
    (out/(name+'.patch')).write_text(found[0]+'\n')
print('Extracted four patches, without executing them.')
PY

git switch -c astra-r11-cross "$BASE"
git apply --check "$PATCHDIR/H11.patch" "$PATCHDIR/P44.patch" "$PATCHDIR/P45.patch" "$PATCHDIR/REG11.patch"
git apply "$PATCHDIR/H11.patch" "$PATCHDIR/P44.patch" "$PATCHDIR/P45.patch" "$PATCHDIR/REG11.patch"
python -m py_compile scripts/r11_*.py scripts/r10_selftest.py
python scripts/r11_selftest.py
python scripts/r10_selftest.py

# Register the complete prospective design before any new native output.
if grep -Fq 'R11-P44-P45: private fixed-geometry crossed profiles' PREREGISTRATION.md; then
  echo 'An R11 registration already exists. Do not append or rerun automatically.' >&2
  exit 2
fi
printf '\nRound 11 prospective registration recorded %s. The following design is adopted before plan generation or native output.\n\n' \
  "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" >> PREREGISTRATION.md
cat docs/astra/round11/REGISTRATION_PROPOSED.md >> PREREGISTRATION.md
git add PREREGISTRATION.md README.md docs/astra/round10/RESULTS.md \
  docs/astra/round11/REGISTRATION_PROPOSED.md scripts/r11_analysis.py \
  scripts/r11_cross.py scripts/r11_selftest.py scripts/r10_selftest.py
git commit -m 'Register R11 P44 private crossed single points and P45 wording'
export R11_REG="$(git rev-parse HEAD)"

# The R10 default is its prior report's prescribed location, not a new search.
# Override R10 only to identify that already-completed run's actual private location.
export R10="${R10:-$HOME/zc-r10-provenance-20261007}"
export R11="${R11:-$HOME/zc-r11-cross-20261007}"
export R10_PLAN_COMMIT="$(git rev-parse ba033e4^{commit})"
test -f "$R10/frozen/manifest.json"
test -f "$R10/comparison/summary.json"
test ! -e "$R11"
umask 077

# Use the existing Mac interpreter/environment from R10, with PySCF 2.14.0.
# Do not upgrade the old parser's NumPy/SciPy/pandas/RDKit dependencies.
python - <<'PY'
import sys
from importlib.metadata import version
from packaging.version import Version
if sys.platform!='darwin':raise SystemExit('Asset-bearing Mac only')
if Version(version('pyscf'))!=Version('2.14.0'):raise SystemExit('Pinned PySCF unavailable')
print('Mac interpreter and PySCF version available. Input/package compatibility is checked by freeze.')
PY
python scripts/r11_cross.py freeze --registration "$R11_REG" \
  --r10-manifest "$R10/frozen/manifest.json" --r10-summary "$R10/comparison/summary.json" \
  --r10-plan-commit "$R10_PLAN_COMMIT" --out "$R11/plan"
cp "$R11/plan/PLAN_SHA256.txt" docs/astra/round11/PLAN_SHA256.txt
git add docs/astra/round11/PLAN_SHA256.txt
git commit -m 'Freeze R11 private plan digest before its 24-slot run'
export R11_PLAN_COMMIT="$(git rev-parse HEAD)"

# Exactly one run. Do not retry after a native failure or timeout.
# Logs, coordinates, dense profiles and raw segments remain outside Git.
set +e
python scripts/r11_cross.py run --plan "$R11/plan/plan.json" \
  --plan-commit "$R11_PLAN_COMMIT" --out "$R11/native" \
  > "$R11/driver.log" 2>&1
R11_RUN_RC=$?
set -e
printf 'R11 driver return code: %s\n' "$R11_RUN_RC"
if [ "$R11_RUN_RC" -ne 0 ]; then
  echo 'No complete-panel acceptance. Preserve private logs and every failed or missing slot.'
  exit "$R11_RUN_RC"
fi
python scripts/r11_cross.py check --plan "$R11/plan/plan.json" \
  --plan-commit "$R11_PLAN_COMMIT" --run "$R11/native" \
  > "$R11/check.log" 2>&1
python - <<'PY'
import json,os
from pathlib import Path
root=Path(os.environ['R11'])/'native'
r=json.loads((root/'run.json').read_text());s=json.loads((root/'summary.json').read_text())
print(json.dumps({'requested_slots':r['requested'],'recorded_slots':r['recorded'],
    'driver_wall_s':r['wall_s'],
    'sum_slot_wall_s':sum(t['wall_s'] for t in r['terminals']),
    'zero_QC_collection_wall_s':s['zero_QC_collection_wall_s'],
    'paired_integrity_passed':s['paired_integrity_passed'],
    'authorizes_production_change':False},indent=2))
PY
# Review $R11/native/public-summary.json for permitted aggregate publication.
# Do not git-add the private run or use any outcome to select a conformer.
```

Unified diffs

Each patch applies against the pinned reference. Their application is independently checkable; execution of the shared tests requires H11 and P44 together. The registration patch adds proposed text, while the command block explicitly appends and commits its adoption. Nothing has been appended to the connected repository here.

<!-- BEGIN PATCH H11 -->
```diff
diff --git a/scripts/r10_selftest.py b/scripts/r10_selftest.py
index a4571af86a19875ce7e21f30fe840b4aa532cefa..40f8167a8081294fe2d939332d8d91e57d875c84 100644
--- a/scripts/r10_selftest.py
+++ b/scripts/r10_selftest.py
@@ -50,7 +50,7 @@ class TestSources(unittest.TestCase):
     def test_frozen_input_mutation(self):
         with tempfile.TemporaryDirectory() as t:
             p=Path(t)/'file';p.write_bytes(b'original');r=src.record(p)
-            self.assertEqual(src.verify_record(r),p)
+            self.assertEqual(src.verify_record(r),p.resolve())
             p.write_bytes(b'mutated')
             with self.assertRaises(ValueError):src.verify_record(r)
 
@@ -58,7 +58,7 @@ class TestSources(unittest.TestCase):
         with self.assertRaises(ValueError):src.private_output(src.ROOT/'production')
         with tempfile.TemporaryDirectory() as t:
             with self.assertRaises(FileExistsError):src.private_output(t)
-            self.assertEqual(src.private_output(Path(t)/'new'),Path(t)/'new')
+            self.assertEqual(src.private_output(Path(t)/'new'),(Path(t)/'new').resolve())
 
     def test_json_rejects_nonfinite(self):
         with tempfile.TemporaryDirectory() as t:
diff --git a/scripts/r11_analysis.py b/scripts/r11_analysis.py
new file mode 100644
index 0000000000000000000000000000000000000000..72c6f006edead248f6e349d20711accff137467c
--- /dev/null
+++ b/scripts/r11_analysis.py
@@ -0,0 +1,183 @@
+"""P44 arithmetic only. Profile attribution is not a liquid-state accuracy gate."""
+from __future__ import annotations
+import numpy as np
+
+CONTROLS = ('water', 'methanol', 'methoxyethanol', 'tetrahydrofuran')
+TAILS = ('raw_abs_tail_A2', 'averaged_segment_abs_tail_A2', 'final_binned_tail_A2')
+FLOOR_TAIL_A2 = 0.5
+FLOOR_SHAPE_L1 = 0.01
+
+
+def finite(x):
+    a = np.asarray(x, dtype=float)
+    if not np.isfinite(a).all():
+        raise ValueError('Nonfinite arithmetic input')
+    return a
+
+
+def norm(x):
+    return float(np.sum(np.abs(finite(x))))
+
+
+def profiles(x):
+    a = finite(x)
+    if a.shape != (3, 51) or (a < 0).any() or a.sum() <= 0:
+        raise ValueError('Expected a nonnegative 153-bin area profile')
+    return a
+
+
+def split(ud, archived, repeat, cross):
+    """Both paths telescope exactly. Repeat drift is retained, never hidden."""
+    u, a, r, c = map(finite, (ud, archived, repeat, cross))
+    if not (u.shape == a.shape == r.shape == c.shape):
+        raise ValueError('Mismatched profile/descriptor shapes')
+    out = {'historical_total': u-a, 'historical_geometry': c-a,
+           'method': u-c, 'repeat_drift': r-a,
+           'current_total': u-r, 'current_geometry': c-r}
+    residuals = (out['historical_total']-out['historical_geometry']-out['method'],
+                 out['current_total']-out['current_geometry']-out['method'],
+                 out['historical_geometry']-out['current_geometry']-out['repeat_drift'])
+    if max(norm(x) for x in residuals) > 1e-10 * max(1., norm(u), norm(a)):
+        raise ValueError('Telescoping identity failed')
+    return {k: v.tolist() for k, v in out.items()}
+
+
+def scalar_verdict(d, g, m, eta):
+    d, g, m, eta = map(float, finite([d, g, m, eta]))
+    if eta <= 0 or abs(d-g-m) > 1e-9 * max(1., abs(d), abs(g), abs(m)):
+        raise ValueError('Invalid scalar decomposition')
+    if g*m < 0 and min(abs(g), abs(m)) > eta:
+        return 'inconclusive_cancellation'
+    if abs(d) <= 2*eta:
+        return 'inconclusive_small_contrast'
+    remainder = max(eta, 0.25*abs(d))
+    if g*d > 0 and abs(g) > eta and abs(m) <= remainder:
+        return 'mainly_geometry'
+    if m*d > 0 and abs(m) > eta and abs(g) <= remainder:
+        return 'mainly_method'
+    if g*d > 0 and m*d > 0 and min(abs(g), abs(m)) > eta:
+        return 'both'
+    return 'inconclusive_borderline'
+
+
+def vector_verdict(d, g, m, eta):
+    d, g, m = map(finite, (d, g, m)); eta = float(eta)
+    if eta <= 0 or not (d.shape == g.shape == m.shape) or norm(d-g-m) > 1e-9:
+        raise ValueError('Invalid vector decomposition')
+    D, G, M = map(norm, (d, g, m))
+    cancellation = max(0., G+M-D)
+    if cancellation > max(2*eta, 0.25*D):
+        label = 'inconclusive_cancellation'
+    elif D <= 2*eta:
+        label = 'inconclusive_small_contrast'
+    elif M <= max(eta, 0.25*D) and G > eta:
+        label = 'mainly_geometry'
+    elif G <= max(eta, 0.25*D) and M > eta:
+        label = 'mainly_method'
+    elif min(G, M) > eta:
+        label = 'both'
+    else:
+        label = 'inconclusive_borderline'
+    return dict(label=label, total_L1=D, geometry_L1=G, method_L1=M,
+                cancellation_excess_L1=cancellation, background_scale=eta)
+
+
+def outliers(q, area):
+    """Area-weighted diagnostics on retained tesserae. No clipping or neutralizing."""
+    q, area = map(finite, (q, area))
+    if q.ndim != 1 or area.shape != q.shape or not len(q) or (area <= 0).any():
+        raise ValueError('Invalid raw tesserae')
+    s = q/area
+    order = np.argsort(s, kind='stable')
+    cdf = np.cumsum(area[order])/area.sum()
+    quantiles = [float(s[order[min(np.searchsorted(cdf, p, side='left'), len(q)-1)]])
+                 for p in (.01, .05, .5, .95, .99)]
+    ans = dict(segments=len(q), net_charge_e=float(q.sum()),
+               area_A2=float(area.sum()), sigma_min=float(s.min()), sigma_max=float(s.max()),
+               area_weighted_quantiles=dict(zip(('p01','p05','p50','p95','p99'), quantiles)),
+               convention='Discrete area CDF; strict +/-0.025 e/A2 outlier cuts')
+    for name, mask in (('negative', s < -.025), ('positive', s > .025)):
+        ans[name] = dict(count=int(mask.sum()), area_A2=float(area[mask].sum()),
+            area_fraction=float(area[mask].sum()/area.sum()), signed_charge_e=float(q[mask].sum()),
+            absolute_charge_e=float(abs(q[mask]).sum()),
+            minimum_area_A2=float(area[mask].min()) if mask.any() else None)
+    return ans
+
+
+def describe(parser, output):
+    """Use the unchanged R10 stage definitions and add bounded scalar outlier data."""
+    from r10_replay import stages
+    desc, arrays = stages(parser, output)
+    raw, area, _avg, _p = arrays
+    desc['outliers'] = outliers(raw*area, area)
+    return desc
+
+
+def native_parity(archived, repeat, old_energy, new_energy):
+    a = profiles(archived['post_HB_bins_A2']); r = profiles(repeat['post_HB_bins_A2'])
+    checks = dict(max_raw_bin_A2=float(abs(a-r).max()),
+        normalized_L1=norm(a/a.sum()-r/r.sum()),
+        energy_Eh=abs(float(new_energy)-float(old_energy)),
+        net_charge_e=abs(repeat['raw_q_sum_e']-archived['raw_q_sum_e']),
+        area_A2=abs(repeat['area_sum_A2']-archived['area_sum_A2']),
+        volume_A3=abs(repeat['volume_A3']-archived['volume_A3']))
+    limits = dict(max_raw_bin_A2=1e-4, normalized_L1=1e-5, energy_Eh=1e-7,
+                  net_charge_e=1e-5, area_A2=1e-4, volume_A3=1e-4)
+    passed = all(np.isfinite(v) and v < limits[k] for k, v in checks.items())
+    return dict(passed=bool(passed), checks=checks, strict_limits=limits,
+                scope='Same RO input; no E-equivalence of different geometries, no affinity gate')
+
+
+def member_math(ud, archived, repeat, cross):
+    ds = (ud, archived, repeat, cross)
+    pp = [profiles(d['post_HB_bins_A2']) for d in ds]
+    ans = dict(area_profile=split(*pp), normalized_profile=split(*(p/p.sum() for p in pp)),
+               tails={k:split(*(d[k] for d in ds)) for k in TAILS},
+               net_charge_e=split(*(d['raw_q_sum_e'] for d in ds)))
+    return ans
+
+
+def classify_panel(rows):
+    """rows: all 12 members with parity and math. No label from an incomplete panel."""
+    from r10_sources import DATA
+    names = [r['name'] for r in rows]
+    if len(names) != 12 or set(names) != {r[0] for r in DATA}:
+        raise ValueError('Incomplete, extra, or duplicate member')
+    if any(r.get('status') != 'paired_complete' or not r.get('parity', {}).get('passed') for r in rows):
+        return dict(complete=False, reason='native_or_parity_failure', rows=[])
+    by = {r['name']:r for r in rows}
+    scales = {}
+    for key in TAILS:
+        d = [by[n]['math']['tails'][key] for n in CONTROLS]
+        drift = max(abs(r['math']['tails'][key]['repeat_drift']) for r in rows)
+        scales[key] = max(FLOOR_TAIL_A2,
+            max(abs(x['current_total']) for x in d),
+            max(abs(x['current_geometry']) for x in d), 4*drift)
+    d = [by[n]['math']['normalized_profile'] for n in CONTROLS]
+    shape_scale = max(FLOOR_SHAPE_L1,
+        max(norm(x['current_total']) for x in d),
+        max(norm(x['current_geometry']) for x in d),
+        4*max(norm(r['math']['normalized_profile']['repeat_drift']) for r in rows))
+    result = []
+    for r in rows:
+        tails = {}
+        for key in TAILS:
+            s = r['math']['tails'][key]; eta = scales[key]
+            label = scalar_verdict(s['current_total'], s['current_geometry'], s['method'], eta)
+            old = scalar_verdict(s['historical_total'], s['historical_geometry'], s['method'], eta)
+            if label != old: label = 'inconclusive_repeat_boundary'
+            tails[key] = dict(s, label=label, background_scale_A2=eta)
+        v = r['math']['normalized_profile']
+        shape = vector_verdict(v['current_total'], v['current_geometry'], v['method'], shape_scale)
+        old = vector_verdict(v['historical_total'], v['historical_geometry'], v['method'], shape_scale)
+        if shape['label'] != old['label']: shape['label'] = 'inconclusive_repeat_boundary'
+        headline = tails['final_binned_tail_A2']['label']
+        if r['name'] in CONTROLS:
+            headline = 'background_control_descriptive_only'
+        elif headline not in ('mainly_geometry','mainly_method','both') or headline != shape['label']:
+            headline = 'metric_dependent_or_inconclusive'
+        result.append(dict(name=r['name'], key=r['key'], tails=tails, shape=shape,
+                           profile_gap_label=headline))
+    return dict(complete=True, rows=result, tail_scales_A2=scales, shape_scale_L1=shape_scale,
+        scale_interpretation='Predeclared background envelope, not random noise, a confidence interval, or a convergence proof',
+        authorizes_profiles=False, authorizes_conformer_selection=False)
diff --git a/scripts/r11_selftest.py b/scripts/r11_selftest.py
new file mode 100644
index 0000000000000000000000000000000000000000..6d8ec6a5acc47f866a34a986ecea9865cdfc09aa
--- /dev/null
+++ b/scripts/r11_selftest.py
@@ -0,0 +1,311 @@
+"""Portable synthetic tests. No UD data and no PySCF calculation are used."""
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
+import r11_analysis as a
+import r11_cross as x
+import r10_sources as src
+
+
+def desc(tail=5., area=100.):
+    p=np.zeros((3,51));p[0,25]=area-tail;p[1,40]=tail
+    d=dict(post_HB_bins_A2=p.tolist(),raw_abs_tail_A2=tail,
+        averaged_segment_abs_tail_A2=tail,final_binned_tail_A2=tail,
+        raw_q_sum_e=-.02,area_sum_A2=area,volume_A3=80.)
+    d['outliers']=a.outliers(np.array([-.02,.0]),np.array([1.,area-1]))
+    return d
+
+
+def panel():
+    rows=[]
+    for name,key,*_ in src.DATA:
+        arch=desc();repeat=desc();cross=desc(5.05);ud=desc(5.1)
+        if name not in a.CONTROLS:
+            cross=desc(13.);ud=desc(15.)
+        rows.append(dict(name=name,key=key,status='paired_complete',
+            parity=a.native_parity(arch,repeat,-3.,-3.),
+            math=a.member_math(ud,arch,repeat,cross),
+            descriptors=dict(UD=ud,P25=arch,RO=repeat,RU=cross)))
+    return rows
+
+
+class Arithmetic(unittest.TestCase):
+    def test_telescoping_and_repeat_drift(self):
+        z=a.split(np.array([4.,2.]),np.array([1.,1.]),np.array([1.01,.99]),np.array([3.,1.5]))
+        np.testing.assert_allclose(np.array(z['current_geometry'])+z['method'],z['current_total'])
+        np.testing.assert_allclose(np.array(z['current_geometry'])+z['repeat_drift'],z['historical_geometry'])
+
+    def test_scalar_negative_and_positive_gap(self):
+        for sign in (-1.,1.):
+            self.assertEqual(a.scalar_verdict(sign*10,sign*9,sign, .5),'mainly_geometry')
+            self.assertEqual(a.scalar_verdict(sign*10,sign,sign*9,.5),'mainly_method')
+            self.assertEqual(a.scalar_verdict(sign*10,sign*5,sign*5,.5),'both')
+
+    def test_cancellation_is_not_dominance(self):
+        self.assertEqual(a.scalar_verdict(10,20,-10,.5),'inconclusive_cancellation')
+        d=np.array([1.,-1.]);g=np.array([10.,0.]);m=d-g
+        self.assertEqual(a.vector_verdict(d,g,m,.01)['label'],'inconclusive_cancellation')
+
+    def test_small_and_exact_boundary(self):
+        self.assertEqual(a.scalar_verdict(1,.9,.1,.5),'inconclusive_small_contrast')
+        self.assertEqual(a.scalar_verdict(10,7.5,2.5,.5),'mainly_geometry')
+        self.assertEqual(a.scalar_verdict(10,7.499,2.501,.5),'both')
+
+    def test_nonfinite_and_broken_identity_rejected(self):
+        with self.assertRaises(ValueError):a.scalar_verdict(1,np.nan,0,.5)
+        with self.assertRaises(ValueError):a.vector_verdict([1],[0],[0],.1)
+        with self.assertRaises(ValueError):a.split([1],[1,2],[1],[1])
+
+    def test_normalize_each_profile_before_subtraction(self):
+        z=a.member_math(desc(10,200),desc(5,100),desc(5,100),desc(10,200))
+        self.assertAlmostEqual(a.norm(z['normalized_profile']['historical_total']),0.)
+        self.assertGreater(a.norm(z['area_profile']['historical_total']),0.)
+
+    def test_native_parity_and_strict_limit(self):
+        self.assertTrue(a.native_parity(desc(),desc(),-3.,-3.)['passed'])
+        d=desc();d['post_HB_bins_A2'][0][25]+=1.1e-4
+        self.assertFalse(a.native_parity(desc(),d,-3.,-3.)['passed'])
+        self.assertFalse(a.native_parity(desc(),desc(),-3.,-2.999)['passed'])
+
+    def test_outliers_are_area_weighted(self):
+        d=a.outliers(np.array([-.1e-6,.01,.0]),np.array([1e-6,1.,99.]))
+        self.assertEqual(d['negative']['count'],1)
+        self.assertLess(d['negative']['area_fraction'],1.1e-8)
+        self.assertEqual(d['area_weighted_quantiles']['p50'],0.)
+        self.assertAlmostEqual(d['net_charge_e'],.01-.1e-6)
+
+    def test_profile_validation(self):
+        with self.assertRaises(ValueError):a.profiles(np.zeros((3,51)))
+        with self.assertRaises(ValueError):a.outliers([1.],[0.])
+
+    def test_panel_controls_and_signed_targets(self):
+        d=a.classify_panel(panel());self.assertTrue(d['complete'])
+        for r in d['rows']:
+            expected='background_control_descriptive_only' if r['name'] in a.CONTROLS else 'mainly_geometry'
+            self.assertEqual(r['profile_gap_label'],expected)
+        self.assertEqual(d['tail_scales_A2']['final_binned_tail_A2'],.5)
+
+    def test_panel_failure_blocks_all_labels(self):
+        r=panel();r[0]['status']='failed'
+        self.assertFalse(a.classify_panel(r)['complete'])
+        r=panel();r[0]['parity']['passed']=False
+        self.assertFalse(a.classify_panel(r)['complete'])
+        with self.assertRaises(ValueError):a.classify_panel(r[:-1])
+        r[-1]=r[0]
+        with self.assertRaises(ValueError):a.classify_panel(r)
+
+    def test_background_not_selected_for_agreement(self):
+        r=panel();c=next(z for z in r if z['name']=='water')
+        c['math']=a.member_math(desc(20),desc(),desc(),desc(5.1))
+        d=a.classify_panel(r)
+        self.assertEqual(d['tail_scales_A2']['raw_abs_tail_A2'],15.)
+        self.assertTrue(all(z['tails']['raw_abs_tail_A2']['label']=='inconclusive_small_contrast' for z in d['rows']))
+
+
+class Execution(unittest.TestCase):
+    def test_mac_and_ci_guards(self):
+        with patch.object(sys,'platform','linux'):
+            with self.assertRaises(RuntimeError):x.mac_only()
+        with patch.object(sys,'platform','darwin'),patch.dict(os.environ,{'GITHUB_ACTIONS':'true'}):
+            with self.assertRaises(RuntimeError):x.mac_only()
+
+    def test_custom_configs_block_before_native_import(self):
+        with tempfile.TemporaryDirectory() as t, ExitStack() as stack:
+            home=Path(t); cwd=home/'working';cwd.mkdir()
+            stack.enter_context(patch.object(Path,'home',return_value=home))
+            stack.enter_context(patch.object(Path,'cwd',return_value=cwd))
+            stack.enter_context(patch.dict(os.environ,{'PYSCF_CONFIG_FILE':''}))
+            x.no_custom_config()
+            (home/'.pyscf_conf.py').write_text('# fixture')
+            with self.assertRaises(RuntimeError):x.no_custom_config()
+            (home/'.pyscf_conf.py').unlink()
+            (cwd/'.pyscf_conf.py').write_text('# fixture')
+            with self.assertRaises(RuntimeError):x.no_custom_config()
+            (cwd/'.pyscf_conf.py').unlink()
+            with patch.dict(os.environ,{'PYSCF_CONFIG_FILE':'some-config'}):
+                with self.assertRaises(RuntimeError):x.no_custom_config()
+
+    def test_private_paths_resolve_aliases(self):
+        with tempfile.TemporaryDirectory() as t:
+            p=Path(t);(p/'real').mkdir();(p/'alias').symlink_to(p/'real',target_is_directory=True)
+            self.assertEqual(x.private_path(p/'alias/new'),(p/'real/new').resolve())
+            (p/'real/.git').mkdir()
+            with self.assertRaises(ValueError):x.private_path(p/'alias/new')
+        with self.assertRaises(ValueError):x.private_path(x.ROOT/'private')
+
+    def test_process_group_deadline(self):
+        with tempfile.TemporaryDirectory() as t:
+            d=x.launch([sys.executable,'-c','import time; time.sleep(10)'],Path(t)/'log',.05,os.environ.copy())
+            self.assertEqual(d['execution_state'],'timeout');self.assertNotEqual(d['returncode'],0)
+            self.assertLess(d['wall_s'],3.)
+
+    def test_single_point_has_one_kernel_and_no_gradients(self):
+        from types import SimpleNamespace as N
+        bohr=.52917721067;radii={'H':1.3,'C':2.,'O':1.72};nums={'H':1,'C':6,'O':8}
+        rt=np.zeros(120)
+        for k,v in radii.items():rt[nums[k]]=v/bohr
+        allq=np.array([.01,-.01,1e-14]);ab=np.array([1.,1.,1e-10])
+        solvent=N(method='C-PCM',eps=1e9,lebedev_order=29,vdw_scale=1.,radii_table=rt,
+                  surface_discretization_method='SWIG',surface={'area':ab},
+                  _intermediates={'K':np.eye(3),'R':np.eye(3),'q':allq,'v_grids':allq})
+        counts={'kernel':0,'progress':0}
+        def kernel():counts['kernel']+=1;return -3.
+        mol=N(basis='def2-tzvp',spin=0,nelectron=1,intor_symmetric=lambda name:np.eye(1))
+        mf=N(xc='b88,p86',grids=N(level=3,prune=None),conv_tol=1e-9,conv_tol_grad=None,
+             max_cycle=50,small_rho_cutoff=0.,mol=mol,with_solvent=solvent,converged=True,
+             kernel=kernel,make_rdm1=lambda:np.eye(1),with_df=N(auxmol=None,auxbasis='fixture'),cycles=2)
+        seg=dict(xyz=np.zeros((2,3)),q=allq[:2],area=ab[:2]*bohr**2,atom=np.array([0,1]))
+        fakepc=types.ModuleType('zcosmo.pyscf_cosmo');fakepc.RADII=radii;fakepc.BOHR=bohr
+        fakez=types.ModuleType('zcosmo');fakez.__path__=[]
+        fakepyscf=types.ModuleType('pyscf');fakepyscf.lib=N(num_threads=lambda n:None)
+        fakedata=types.ModuleType('pyscf.data');fakedata.elements=N(charge=lambda x:nums[x])
+        fakecharge=types.ModuleType('r4_charge')
+        fakecharge.factory=lambda sym,xyz,spin,basis,memory:mf
+        fakecharge.segments=lambda s:(seg,ab>1e-8)
+        def progress():counts['progress']+=1
+        with patch.dict(sys.modules,{'pyscf':fakepyscf,'pyscf.data':fakedata,
+            'zcosmo':fakez,'zcosmo.pyscf_cosmo':fakepc,'r4_charge':fakecharge}):
+            out,e,d=x.single_point(['O','H'],np.zeros((2,3)),progress)
+        self.assertEqual(counts,{'kernel':1,'progress':1})
+        self.assertEqual(d['audit']['discarded_nodes'],1)
+        self.assertEqual(e,-3.)
+
+    def test_parser_failure_preserves_the_completed_raw_single_point(self):
+        with tempfile.TemporaryDirectory() as t, ExitStack() as stack:
+            root=Path(t);p=root/'plan/plan.json';src.write(p,{'fixture':True})
+            key=src.DATA[0][1];run=root/'run';run.mkdir();out=run/key/'RU'
+            src.write(p.parent/'execution_claim.json',dict(output=str(run),plan_sha256=src.sha(p),
+                                                         nonce='fixture',pid=os.getppid()))
+            row=dict(raw={'sha256':'a'*64})
+            stack.enter_context(patch.object(x,'mac_only'))
+            stack.enter_context(patch.object(x,'load_plan',return_value=(p,{'packages':{}},{key:row},{})))
+            stack.enter_context(patch.dict(os.environ,{'ZC_R11_NONCE':'fixture'}))
+            stack.enter_context(patch.object(x,'source_geometry',return_value=(['O'],np.zeros((1,3)))))
+            seg=dict(xyz=np.zeros((1,3)),q=np.array([-.01]),area=np.array([1.]),atom=np.array([0]))
+            def native(sym,xyz,progress):
+                progress();return seg,-3.,{'audit':{'net_kept_e':-.01}}
+            stack.enter_context(patch.object(x,'single_point',side_effect=native))
+            stack.enter_context(patch.object(x,'import_module',return_value=types.SimpleNamespace(__file__=str(p))))
+            fake=types.ModuleType('r4_common')
+            def bad_parser(*args):raise ValueError('Synthetic bin-domain failure')
+            fake.parser_trace=bad_parser
+            stack.enter_context(patch.dict(sys.modules,{'r4_common':fake}))
+            stack.enter_context(patch.object(x.traceback,'print_exc'))
+            rc=x.worker(argparse.Namespace(plan=str(p),plan_commit='b'*40,key=key,arm='RU',out=str(out)))
+            record=read_json(out/'result.json')
+            self.assertEqual(rc,2);self.assertEqual(record['SCF_attempted'],1)
+            self.assertTrue(record['SCF_converged']);self.assertEqual(record['failure_phase'],'SCF_complete')
+            self.assertTrue((out/'segments.npz').is_file())
+            self.assertEqual(record['native']['audit']['net_kept_e'],-.01)
+
+    def test_runner_preserves_failed_slots_and_no_retry(self):
+        with tempfile.TemporaryDirectory() as t,ExitStack() as stack:
+            root=Path(t);p=root/'plan/plan.json';src.write(p,{'fixture':True})
+            cases=[dict(name=n,key=k,order=['RO','RU']) for n,k,*_ in src.DATA]
+            m=dict(cases=cases,packages={})
+            stack.enter_context(patch.object(x,'mac_only'))
+            stack.enter_context(patch.object(x,'load_plan',return_value=(p,m,{},{})))
+            stack.enter_context(patch.object(x,'collect',return_value=2))
+            count=[]
+            def launch(cmd,log,secs,env):
+                count.append(cmd);return dict(execution_state='returned',returncode=2 if len(count)==1 else 0,wall_s=.001)
+            stack.enter_context(patch.object(x,'launch',side_effect=launch))
+            args=argparse.Namespace(plan=str(p),plan_commit='a'*40,out=str(root/'run'))
+            self.assertEqual(x.runner(args),2);self.assertEqual(len(count),24)
+            run=read_json(root/'run/run.json')
+            self.assertEqual(run['recorded'],24);self.assertTrue(run['complete'])
+            args.out=str(root/'another')
+            with self.assertRaises(FileExistsError):x.runner(args)
+
+    def test_aggregate_has_no_dense_or_coordinate_fields(self):
+        rows=panel();d=dict(rows=rows,classification=a.classify_panel(rows),plan_sha256='a'*64,paired_integrity_passed=True)
+        for r in rows:
+            r['path']='/private/secret';r['coordinates']=[[1,2,3]]
+            r['descriptors']['UD']['xyz']=[[1,2,3]]
+        text=json.dumps(x.public_summary(d))
+        for forbidden in ('coordinates','post_HB_bins','pre_HB_bins','/private','xyz'):
+            self.assertNotIn(forbidden,text)
+
+
+def read_json(p):return json.loads(Path(p).read_text())
+
+
+class Integration(unittest.TestCase):
+    def fixture(self, root):
+        p=root/'plan/plan.json';src.write(p,{'synthetic':True});run=root/'run';run.mkdir()
+        src.write(p.parent/'execution_claim.json',dict(output=str(run),plan_sha256=src.sha(p)))
+        m=dict(packages={'fixture':'1'},cases=[dict(name=n,key=k) for n,k,*_ in src.DATA])
+        by={};old=dict(rows=[]);descmap={}
+        for r in panel():
+            key=r['key'];local=root/'inputs'/key;local.mkdir(parents=True)
+            src.write(local/'native.json',{'energy_Eh':-3.})
+            raw=local/'synthetic.cosmo';raw.write_text('SYNTHETIC NO UD DATA')
+            by[key]=dict(key=key,raw={'path':str(raw),'sha256':'u'*64},segments={'path':str(local/'old.npz'),'sha256':'o'*64},
+                         native={'path':str(local/'native.json')})
+            descmap[str(raw)]=r['descriptors']['UD'];descmap[str(local/'old.npz')]=r['descriptors']['P25']
+            old['rows'].append(dict(key=key,status='replay_passed'))
+            for arm in ('RO','RU'):
+                d=run/key/arm;d.mkdir(parents=True)
+                (d/'segments.npz').write_bytes(b'synthetic NPZ stand-in')
+                native=dict(key=key,arm=arm,plan_sha256=src.sha(p),status='completed',SCF_attempted=1,
+                    SCF_converged=True,packages=m['packages'],energy_Eh=-3.,descriptor=r['descriptors'][arm],
+                    native={'audit':{'synthetic':True}},geometry_input_sha256=('u' if arm=='RU' else 'o')*64,segments_sha256=src.sha(d/'segments.npz'))
+                src.write(d/'result.json',native)
+                src.write(run/key/(arm+'.terminal.json'),dict(key=key,arm=arm,plan_sha256=src.sha(p),
+                    execution_state='returned',returncode=0,wall_s=.01))
+        return p,run,m,by,old,descmap
+
+    def execute(self, root, broken=False):
+        p,run,m,by,old,descmap=self.fixture(root)
+        fakecommon=types.ModuleType('r4_common')
+        fakecommon.parser_trace=lambda sym,xyz,seg:(None,types.SimpleNamespace(desc=seg['fixture']),None)
+        fakeparser=types.SimpleNamespace(Dmol3COSMOParser=lambda path,**kw:
+            types.SimpleNamespace(get_outputs=lambda:types.SimpleNamespace(desc=descmap[path])))
+        if broken:(run/src.DATA[0][1]/'RU/segments.npz').write_bytes(b'mutated')
+        with ExitStack() as s:
+            s.enter_context(patch.object(x,'mac_only'))
+            s.enter_context(patch.object(x,'load_plan',return_value=(p,m,by,old)))
+            s.enter_context(patch.object(x.replay,'parser_module',return_value=fakeparser))
+            s.enter_context(patch.object(x.replay,'run_member',return_value={'status':'replay_passed'}))
+            s.enter_context(patch.object(x.replay,'load_npz',side_effect=lambda path:(['O'],np.zeros((1,3)),{'fixture':descmap[path]})))
+            s.enter_context(patch.object(a,'describe',side_effect=lambda pp,output:output.desc))
+            s.enter_context(patch.dict(sys.modules,{'r4_common':fakecommon}))
+            args=argparse.Namespace(plan=str(p),plan_commit='b'*40,run=str(run))
+            rc=x.collect(args);d=read_json(run/'summary.json')
+            if not broken:
+                self.assertEqual(x.check(args),0)
+                altered=copy.deepcopy(d)
+                altered['rows'][1]['descriptors']['RU']['raw_q_sum_e']+=.1
+                ds=altered['rows'][1]['descriptors']
+                altered['rows'][1]['math']=a.member_math(ds['UD'],ds['P25'],ds['RO'],ds['RU'])
+                src.write(run/'summary.json',altered)
+                with self.assertRaises(ValueError):x.check(args)
+                src.write(run/'summary.json',d)
+                native=run/src.DATA[1][1]/'RU/result.json';q=read_json(native);q['energy_Eh']=999.;src.write(native,q)
+                with self.assertRaises(ValueError):x.check(args)
+            return rc,d
+
+    def test_all_twelve_and_independent_check(self):
+        with tempfile.TemporaryDirectory() as t:
+            rc,d=self.execute(Path(t));self.assertEqual(rc,0)
+            self.assertEqual(len(d['rows']),12);self.assertTrue(d['paired_integrity_passed'])
+
+    def test_mutated_slot_retained_and_blocks_classification(self):
+        with tempfile.TemporaryDirectory() as t:
+            rc,d=self.execute(Path(t),True);self.assertEqual(rc,2)
+            self.assertEqual(len(d['rows']),12);self.assertFalse(d['classification']['complete'])
+            self.assertEqual(d['rows'][0]['status'],'integrity_failed')
+            self.assertEqual(d['rows'][-1]['status'],'paired_complete')
+
+
+if __name__=='__main__':unittest.main()
```
<!-- END PATCH H11 -->

<!-- BEGIN PATCH P44 -->
```diff
diff --git a/scripts/r11_cross.py b/scripts/r11_cross.py
new file mode 100644
index 0000000000000000000000000000000000000000..d251a6d17388c8d84f319e873ae2f81c27b560b0
--- /dev/null
+++ b/scripts/r11_cross.py
@@ -0,0 +1,506 @@
+"""P44: private Mac-only crossed single points. No optimization or scoring.
+
+Use the already accepted R10 manifest and summary. Only a plan digest enters
+Git. This module never uploads data or writes a production sigma file.
+"""
+from __future__ import annotations
+import argparse
+from contextlib import redirect_stdout, redirect_stderr
+import hashlib
+from importlib import import_module
+from importlib.metadata import version
+import json
+import os
+from pathlib import Path
+import platform
+import re
+import signal
+import subprocess
+import sys
+import time
+import traceback
+import numpy as np
+from packaging.version import Version
+import r10_sources as src
+import r10_replay as replay
+import r11_analysis as ana
+
+BASE = '463ec1be5c0edfad1e8effd334a17fc44cd27405'
+MARKER = 'R11-P44-P45: private fixed-geometry crossed profiles'
+PLAN_RECORD = 'docs/astra/round11/PLAN_SHA256.txt'
+SCHEMA = 'R11-cross-v1'
+ROOT = Path(__file__).resolve().parents[1]
+ARMS = ('RO', 'RU')
+DESIGN = dict(SCF_limit=24, seconds_per_slot=900, total_run_seconds=22500,
+    max_parallel=1, OMP_threads=4, BLAS_threads=1, memory_MB=4000, PCM_cache_MB=2000,
+    gradients=0, optimizations=0, model_calls=0, no_retries=True,
+    tail_floor_A2=ana.FLOOR_TAIL_A2, shape_floor_L1=ana.FLOOR_SHAPE_L1,
+    dominance_remainder_fraction=.25, background_signal_factor=2.,
+    control_names=list(ana.CONTROLS))
+FILES = ['scripts/r11_analysis.py', 'scripts/r11_cross.py',
+    'scripts/r10_sources.py', 'scripts/r10_replay.py', 'scripts/r4_charge.py',
+    'scripts/r4_common.py', 'scripts/r3_common.py', 'scripts/r5_shape.py',
+    'src/zcosmo/pyscf_cosmo.py', 'src/zcosmo/pcm_lu.py', 'data/raw/nist/to_sigma.py']
+sha, read, write = src.sha, src.read, src.write
+
+
+def mac_only():
+    if sys.platform != 'darwin' or os.environ.get('GITHUB_ACTIONS') == 'true' or os.environ.get('CI') == 'true':
+        raise RuntimeError('Private asset-bearing Mac only, never a CI worker')
+
+
+def private_path(path, fresh=False):
+    p = Path(path).expanduser().resolve()
+    if p.is_relative_to(ROOT) or ROOT.is_relative_to(p):
+        raise ValueError('Use private storage outside the repository')
+    for a in (p, *p.parents):
+        if (a/'.git').exists():
+            raise ValueError('Private calculation data cannot be stored in another Git checkout')
+    if fresh and p.exists():
+        raise FileExistsError(p)
+    return p
+
+
+def no_custom_config():
+    # PySCF also searches CWD/HOME when PYSCF_CONFIG_FILE is unset.
+    candidates=(Path.cwd()/'.pyscf_conf.py', Path.home()/'.pyscf_conf.py')
+    if os.environ.get('PYSCF_CONFIG_FILE') or any(p.is_file() for p in candidates):
+        raise RuntimeError('Custom PySCF configuration is outside this registration')
+
+
+def packages():
+    d = {p:str(Version(version(p))) for p in
+         ('numpy','scipy','pandas','rdkit','packaging','matplotlib','pyscf')}
+    if d['pyscf'] != '2.14.0':
+        raise RuntimeError('PySCF 2.14.0 is required; no dependency upgrade is authorized')
+    d.update(python=platform.python_version(), machine=platform.machine())
+    return d
+
+
+def registration(commit):
+    if not re.fullmatch('[0-9a-f]{40}', commit):
+        raise ValueError('Full actual registration commit required')
+    src.git('merge-base','--is-ancestor',BASE,'HEAD')
+    src.git('merge-base','--is-ancestor',commit,'HEAD')
+    text = src.git('show',commit+':PREREGISTRATION.md')
+    if MARKER.encode() not in text:
+        raise ValueError('Commit lacks the R11 registration marker')
+    return dict(commit=commit, preregistration_sha256=hashlib.sha256(text).hexdigest())
+
+
+def old_evidence(manifest, plan_commit, summary):
+    with redirect_stdout(sys.stderr):
+        m = replay.verify_manifest(manifest, plan_commit)
+        replay.check(argparse.Namespace(summary=summary))
+    s = read(summary)
+    if (s['manifest_sha256'] != sha(manifest) or s['plan_commit'] != plan_commit or
+        s['registration'] != m['registration'] or s['packages'] != m['packages']):
+        raise ValueError('R10 lineage summary does not belong to these exact frozen inputs')
+    return m, s
+
+
+def freeze(a):
+    mac_only(); no_custom_config(); os.umask(0o077)
+    reg = registration(a.registration)
+    old = private_path(a.r10_manifest); summary = private_path(a.r10_summary)
+    m, s = old_evidence(old, a.r10_plan_commit, summary)
+    native_packages = packages()
+    sources = src.committed_sources(FILES)
+    out = private_path(a.out, fresh=True)
+    # No coordinate extraction, profile arithmetic or native work in this step.
+    cases = []
+    for r in m['rows']:
+        order = list(ARMS)
+        if int(hashlib.sha256(r['key'].encode()).hexdigest(), 16) % 2:
+            order.reverse()
+        cases.append(dict(name=r['name'], key=r['key'], order=order))
+    if len(cases) != 12 or {r['key'] for r in cases} != {d[1] for d in src.DATA}:
+        raise ValueError('Frozen twelve-member panel changed')
+    out.mkdir(parents=True, mode=0o700)
+    plan = dict(schema=SCHEMA, base=BASE, registration=reg, design=DESIGN,
+        sources=sources, packages=native_packages, cases=cases,
+        r10_manifest=src.record(old), r10_summary=src.record(summary),
+        r10_plan_commit=a.r10_plan_commit,
+        protected_population=m['protected_population'],
+        coordinate_policy='Exact stored coordinates and atom order; no rotation, reflection, or centering',
+        purpose='Ordered open-method coordinate contrast and remaining method bundle; no adoption')
+    write(out/'plan.json', plan)
+    (out/'PLAN_SHA256.txt').write_text(sha(out/'plan.json')+'\n')
+    print('Private plan frozen; only its SHA256 may be committed:', sha(out/'plan.json'))
+    return 0
+
+
+def load_plan(path, plan_commit):
+    no_custom_config()
+    p = private_path(path); m = read(p)
+    if (m['schema'] != SCHEMA or m['base'] != BASE or m['design'] != DESIGN or
+        len(m['cases']) != 12 or {r['key'] for r in m['cases']} != {r[1] for r in src.DATA}):
+        raise ValueError('Changed design or panel')
+    if not re.fullmatch('[0-9a-f]{40}', plan_commit):
+        raise ValueError('Full plan-record commit required')
+    src.git('merge-base','--is-ancestor',plan_commit,'HEAD')
+    src.git('merge-base','--is-ancestor',m['registration']['commit'],plan_commit)
+    if src.git('show',plan_commit+':'+PLAN_RECORD).decode().strip() != sha(p):
+        raise ValueError('Plan digest was not committed before native work')
+    if registration(m['registration']['commit']) != m['registration'] or packages() != m['packages']:
+        raise ValueError('Registration or environment drift')
+    src.verify_sources(m['sources'])
+    for r in [m['r10_manifest'], m['r10_summary'], *m['protected_population']]:
+        src.verify_record(r)
+    old, summary = old_evidence(m['r10_manifest']['path'], m['r10_plan_commit'], m['r10_summary']['path'])
+    by = {r['key']:r for r in old['rows']}
+    names = {r[1]:r[0] for r in src.DATA}
+    for r in m['cases']:
+        order = list(ARMS)
+        if int(hashlib.sha256(r['key'].encode()).hexdigest(),16) % 2: order.reverse()
+        if r['name'] != names[r['key']] or r['order'] != order or r['name'] != by[r['key']]['name']:
+            raise ValueError('Changed member identity/order')
+    return p, m, by, summary
+
+
+def source_geometry(row, arm):
+    if arm == 'RO':
+        sym, xyz, _ = replay.load_npz(row['segments']['path'])
+    elif arm == 'RU':
+        df = replay.parser_module().get_atom_DataFrame(Path(row['raw']['path']).read_text())
+        sym = list(df.atom)
+        xyz = df[['x / A','y / A','z / A']].to_numpy(float)
+    else:
+        raise ValueError('Unknown arm')
+    return replay.validate_geometry(sym, xyz)
+
+
+def single_point(sym, xyz, progress):
+    """Call the unchanged P25 factory once. Extra observations do not change SCF."""
+    from pyscf import lib
+    from r4_charge import factory, segments
+    from zcosmo.pyscf_cosmo import RADII, BOHR
+    lib.num_threads(4)
+    mf = factory(sym, xyz, 0, 'def2-tzvp', 4000)
+    s = mf.with_solvent
+    from pyscf.data import elements
+    want = np.zeros(120)
+    for element, radius in RADII.items(): want[elements.charge(element)] = radius/BOHR
+    if (mf.xc != 'b88,p86' or mf.grids.level != 3 or mf.conv_tol != 1e-9 or
+        s.method != 'C-PCM' or s.eps != 1e9 or s.lebedev_order != 29 or
+        s.surface_discretization_method.upper() != 'SWIG' or
+        s.vdw_scale != 1. or not np.array_equal(s.radii_table, want) or
+        getattr(mf.mol, 'spin', None) != 0):
+        raise RuntimeError('P25 single-point settings changed')
+    settings = dict(basis=str(mf.mol.basis), xc=mf.xc, grid_level=mf.grids.level,
+        conv_tol=mf.conv_tol, conv_tol_grad=mf.conv_tol_grad,
+        max_cycle=mf.max_cycle, small_rho_cutoff=float(mf.small_rho_cutoff),
+        prune=getattr(mf.grids.prune,'__name__',str(mf.grids.prune)),
+        surface_discretization=s.surface_discretization_method, eps=s.eps,
+        method=s.method, lebedev_order=s.lebedev_order, vdw_scale=s.vdw_scale,
+        radius_table_sha256=hashlib.sha256(s.radii_table.tobytes()).hexdigest())
+    progress()
+    energy = float(mf.kernel())
+    if not mf.converged or not np.isfinite(energy):
+        raise RuntimeError('SCF failed; no retry, alternate guess, or solver')
+    dm = mf.make_rdm1(); overlap = mf.mol.intor_symmetric('int1e_ovlp')
+    electron_error = float(np.einsum('ij,ji->',dm,overlap)-mf.mol.nelectron)
+    it = s._intermediates; rhs = it['R']@it['v_grids']
+    solve_error = float(np.max(abs(it['K']@it['q']-rhs))/max(1.,np.max(abs(rhs))))
+    if abs(electron_error) > 1e-7 or solve_error > 1e-10:
+        raise RuntimeError('Electron-count or PCM linear-system integrity failed')
+    seg, keep = segments(s)
+    allq = np.asarray(it['q']).ravel(); allarea = np.asarray(s.surface['area'])*BOHR**2
+    drop = ~keep
+    if (abs(float(allq.sum()-seg['q'].sum()-allq[drop].sum())) > 1e-12 or
+        abs(float(allarea.sum()-seg['area'].sum()-allarea[drop].sum())) > 1e-9):
+        raise RuntimeError('Retained/discarded surface accounting failed')
+    audit = dict(surface_nodes=len(allq), retained_nodes=int(keep.sum()),
+        discarded_nodes=int(drop.sum()), net_all_e=float(allq.sum()),
+        net_kept_e=float(seg['q'].sum()), net_discarded_e=float(allq[drop].sum()),
+        discarded_abs_charge_e=float(abs(allq[drop]).sum()), discarded_area_A2=float(allarea[drop].sum()),
+        electron_error_e=electron_error, PCM_solve_relative_residual=solve_error,
+        filter='surface area > 1e-8 bohr^2, unchanged P25 filter',
+        raw_outliers=ana.outliers(seg['q'],seg['area']),
+        all_surface_sigma_min=float((allq/allarea).min()),
+        all_surface_sigma_max=float((allq/allarea).max()))
+    aux = getattr(mf.with_df, 'auxmol', None)
+    settings['auxiliary_basis'] = str(getattr(aux,'basis',getattr(mf.with_df,'auxbasis',None)))
+    return seg, energy, dict(settings=settings, audit=audit, SCF_cycles=int(getattr(mf,'cycles',-1)))
+
+
+def worker(a):
+    mac_only(); os.umask(0o077)
+    p, m, by, _ = load_plan(a.plan, a.plan_commit)
+    if a.key not in by or a.arm not in ARMS:
+        raise ValueError('Unrequested native identity')
+    claim = read(p.parent/'execution_claim.json'); out = private_path(a.out, fresh=True)
+    expected = Path(claim['output']).resolve()/a.key/a.arm
+    if (claim['plan_sha256'] != sha(p) or out != expected or
+        claim['nonce'] != os.environ.get('ZC_R11_NONCE') or claim['pid'] != os.getppid()):
+        raise ValueError('Only the single claimed parent run may launch native slots')
+    out.mkdir(parents=True, mode=0o700)
+    status = dict(key=a.key, arm=a.arm, plan_sha256=sha(p), status='preparing',
+                  SCF_attempted=0, SCF_converged=False, adopted=False)
+    write(out/'result.json',status); start=time.monotonic()
+    try:
+        sym, xyz = source_geometry(by[a.key], a.arm)
+        original = xyz.copy()
+        def progress():
+            status.update(status='SCF_running', SCF_attempted=1)
+            write(out/'result.json',status)
+        seg, energy, native = single_point(sym,xyz,progress)
+        if not np.array_equal(xyz, original):
+            raise RuntimeError('Native helper changed the input coordinates')
+        upstream = {name:sha(import_module(name).__file__) for name in
+            ('pyscf.dft.rks','pyscf.dft.gen_grid','pyscf.solvent.pcm','pyscf.df.df')}
+        # Retain the private raw result even if subsequent profile binning fails.
+        np.savez_compressed(out/'segments.npz',sym=np.array(sym),x=xyz,**seg)
+        status.update(status='SCF_complete',SCF_converged=True,energy_Eh=energy,
+            native=native,packages=m['packages'],upstream_sha256=upstream,
+            geometry_input_sha256=by[a.key]['raw' if a.arm=='RU' else 'segments']['sha256'],
+            segments_sha256=sha(out/'segments.npz'),wall_s=time.monotonic()-start)
+        write(out/'result.json',status)
+        from r4_common import parser_trace
+        pp, output, _ = parser_trace(sym,xyz,seg)
+        desc = ana.describe(pp,output)
+        status.update(status='completed',descriptor=desc,wall_s=time.monotonic()-start)
+        write(out/'result.json',status)
+        return 0
+    except Exception:
+        status.update(failure_phase=status['status'],status='failed',wall_s=time.monotonic()-start)
+        write(out/'result.json',status)
+        traceback.print_exc()  # Parent redirects all output into private storage.
+        return 2
+
+
+def launch(command, log, seconds, env):
+    """Kill the whole process group at the fixed ceiling; never retry a slot."""
+    start=time.monotonic()
+    with Path(log).open('xb') as f:
+        proc=subprocess.Popen(command,stdout=f,stderr=subprocess.STDOUT,
+                              start_new_session=True,env=env)
+        try:
+            rc=proc.wait(timeout=seconds); state='returned'
+        except subprocess.TimeoutExpired:
+            state='timeout'
+            try:os.killpg(proc.pid,signal.SIGKILL)
+            except ProcessLookupError:pass
+            rc=proc.wait()
+        except BaseException:
+            try:os.killpg(proc.pid,signal.SIGKILL)
+            except ProcessLookupError:pass
+            proc.wait();raise
+    return dict(execution_state=state,returncode=rc,wall_s=time.monotonic()-start)
+
+
+def runner(a):
+    mac_only(); os.umask(0o077)
+    p, m, _by, _ = load_plan(a.plan, a.plan_commit)
+    out=private_path(a.out,fresh=True)
+    if out.is_relative_to(p.parent) or p.parent.is_relative_to(out):
+        raise ValueError('Plan and native output must be separate private directories')
+    no_custom_config()
+    import secrets
+    nonce=secrets.token_hex(24)
+    claim=dict(plan_sha256=sha(p),output=str(out),pid=os.getpid(),nonce=nonce)
+    # Permanent claim is the no-retry barrier. Interrupted plans are not resumed.
+    with (p.parent/'execution_claim.json').open('x') as f:json.dump(claim,f)
+    out.mkdir(parents=True,mode=0o700); start=time.monotonic(); terminals=[]
+    env=os.environ.copy()
+    env.update(OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',BLIS_NUM_THREADS='1',
+        VECLIB_MAXIMUM_THREADS='1',NUMEXPR_NUM_THREADS='1',QC_MEM_MB='4000',
+        ZC_PCM3C='1',ZC_PCM3C_MB='2000',ZC_R3_COOH_FLAG='1',MPLBACKEND='Agg',
+        ZC_R11_NONCE=nonce,PYTHONPATH=str(ROOT/'src')+os.pathsep+str(ROOT/'scripts'))
+    for case in m['cases']:
+        for arm in case['order']:
+            remaining=DESIGN['total_run_seconds']-(time.monotonic()-start)
+            terminal=dict(key=case['key'],arm=arm,plan_sha256=sha(p),execution_state='not_run_budget',
+                          returncode=None,wall_s=0.)
+            folder=out/case['key']; folder.mkdir(exist_ok=True,mode=0o700)
+            if remaining > 2:
+                command=[sys.executable,str(ROOT/'scripts/r11_cross.py'),'_worker',
+                    '--plan',str(p),'--plan-commit',a.plan_commit,'--key',case['key'],
+                    '--arm',arm,'--out',str(folder/arm)]
+                try:terminal.update(launch(command,folder/(arm+'.log'),min(900.,remaining),env))
+                except Exception:
+                    terminal.update(execution_state='launch_failed',returncode=None)
+            terminal['slot_consumed']=terminal['execution_state']!='not_run_budget'
+            write(folder/(arm+'.terminal.json'),terminal);terminals.append(terminal)
+            write(out/'run.json',dict(plan_sha256=sha(p),plan_commit=a.plan_commit,
+                requested=24,recorded=len(terminals),terminals=terminals,complete=False,
+                wall_s=time.monotonic()-start))
+    write(out/'run.json',dict(plan_sha256=sha(p),plan_commit=a.plan_commit,requested=24,
+        recorded=24,terminals=terminals,complete=True,wall_s=time.monotonic()-start))
+    return collect(argparse.Namespace(plan=str(p),plan_commit=a.plan_commit,run=str(out)))
+
+
+def read_slot(run, key, arm, plan_hash, expected_packages, expected_input_hash):
+    terminal=run/key/(arm+'.terminal.json'); result=run/key/arm/'result.json'
+    if not terminal.is_file(): return None, 'missing_terminal'
+    t=read(terminal)
+    if (t.get('key'),t.get('arm'),t.get('plan_sha256')) != (key,arm,plan_hash):
+        raise ValueError('Terminal identity mismatch')
+    if t['execution_state']!='returned' or t['returncode']!=0 or not result.is_file():
+        return None,t['execution_state'] if t['execution_state']!='returned' else 'failed'
+    if not np.isfinite(t['wall_s']) or t['wall_s'] < 0 or t['wall_s'] > 905:
+        raise ValueError('Native execution receipt exceeded its 900-second slot plus 5-second kill/accounting allowance')
+    d=read(result)
+    if ((d.get('key'),d.get('arm'),d.get('plan_sha256')) != (key,arm,plan_hash) or
+        d.get('status')!='completed' or d.get('SCF_attempted')!=1 or
+        d.get('SCF_converged') is not True or d.get('packages')!=expected_packages or
+        d.get('geometry_input_sha256') != expected_input_hash or
+        sha(result.parent/'segments.npz')!=d['segments_sha256']):
+        raise ValueError('Native result identity, completion, or content mismatch')
+    return d,'completed'
+
+
+def public_summary(summary):
+    """Allowlist only. No paths, logs, coordinates, raw rows, dense bins or energies."""
+    def numbers(d, names):
+        out={}
+        for key in names:
+            value=d.get(key)
+            if value is not None and (not isinstance(value,(int,float,bool)) or not np.isfinite(value)):
+                raise ValueError('Non-scalar field in public allowlist')
+            out[key]=value
+        return out
+    def outlier_summary(d):
+        ans=numbers(d,('segments','net_charge_e','area_A2','sigma_min','sigma_max'))
+        ans['area_weighted_quantiles']=numbers(d['area_weighted_quantiles'],('p01','p05','p50','p95','p99'))
+        for name in ('negative','positive'):
+            ans[name]=numbers(d[name],('count','area_A2','area_fraction','signed_charge_e',
+                                       'absolute_charge_e','minimum_area_A2'))
+        return ans
+    verdicts={r['key']:r for r in summary['classification'].get('rows',[])}
+    expected={r[1]:r[0] for r in src.DATA};rows=[]
+    for r in summary['rows']:
+        if expected.get(r['key'])!=r['name']:raise ValueError('Unknown public member identity')
+        z={k:r[k] for k in ('name','key','status')}
+        if 'parity' in r:
+            fields=('max_raw_bin_A2','normalized_L1','energy_Eh','net_charge_e','area_A2','volume_A3')
+            z['parity']=dict(passed=r['parity']['passed'],checks=numbers(r['parity']['checks'],fields),
+                             strict_limits=numbers(r['parity']['strict_limits'],fields))
+        if r['key'] in verdicts:
+            v=verdicts[r['key']]
+            z['attribution']=dict(profile_gap_label=v['profile_gap_label'],
+                shape=dict(numbers(v['shape'],('total_L1','geometry_L1','method_L1',
+                     'cancellation_excess_L1','background_scale')),label=v['shape']['label']),tails={})
+            for key in ana.TAILS:
+                t=v['tails'][key]
+                z['attribution']['tails'][key]=dict(numbers(t,('historical_total','historical_geometry',
+                    'method','repeat_drift','current_total','current_geometry','background_scale_A2')),label=t['label'])
+        if 'descriptors' in r:
+            z['surface_audit']={}
+            for arm in ('UD','P25','RO','RU'):
+                desc=r['descriptors'][arm]
+                z['surface_audit'][arm]=numbers(desc,(*ana.TAILS,'raw_q_sum_e','area_sum_A2','volume_A3'))
+                z['surface_audit'][arm]['outliers']=outlier_summary(desc['outliers'])
+        if 'native_audits' in r:
+            z['native_integrity']={arm:numbers(r['native_audits'][arm],('surface_nodes','retained_nodes',
+                'discarded_nodes','net_all_e','net_kept_e','net_discarded_e','discarded_abs_charge_e',
+                'discarded_area_A2','electron_error_e','PCM_solve_relative_residual')) for arm in ARMS}
+        rows.append(z)
+    return dict(base=BASE,plan_sha256=summary['plan_sha256'],
+        paired_integrity_passed=summary['paired_integrity_passed'],rows=rows,
+        tail_scales_A2=summary['classification'].get('tail_scales_A2'),
+        shape_scale_L1=summary['classification'].get('shape_scale_L1'),
+        model_calls=0,optimizations=0,gradients=0,adopted=False,
+        note='Ordered coordinate-input/method-bundle attribution only. Not a liquid-conformer rule or an accuracy score.')
+
+
+def collect(a):
+    mac_only(); collection_start=time.monotonic()
+    p,m,by,old_summary=load_plan(a.plan,a.plan_commit)
+    run=private_path(a.run);claim=read(p.parent/'execution_claim.json')
+    if Path(claim['output']).resolve()!=run or claim['plan_sha256']!=sha(p):
+        raise ValueError('Run differs from the single claimed output')
+    if (run/'summary.json').exists() or (run/'public-summary.json').exists():
+        raise FileExistsError('Collection already exists; no overwrite or selective replacement')
+    ts=replay.parser_module();rows=[]
+    old_by={r['key']:r for r in old_summary['rows']}
+    for case in m['cases']:
+        key=case['key'];r=by[key];row=dict(name=case['name'],key=key,status='incomplete')
+        try:
+            outcomes={};native={}
+            for arm in ARMS:
+                native[arm],outcomes[arm]=read_slot(run,key,arm,sha(p),m['packages'],r['raw' if arm=='RU' else 'segments']['sha256'])
+            row['outcomes']=outcomes
+            if any(native[a] is None for a in ARMS):
+                rows.append(row);continue
+            # Recheck exact lineage now, using unchanged files, before attribution.
+            checked=replay.run_member(r,ts)
+            if checked['status']!='replay_passed' or old_by[key]['status']!='replay_passed':
+                raise ValueError('R10 lineage not reproduced')
+            up=ts.Dmol3COSMOParser(r['raw']['path'],num_profiles=3,averaging='Hsieh')
+            ud=ana.describe(up,up.get_outputs())
+            osym,ox,seg=replay.load_npz(r['segments']['path'])
+            from r4_common import parser_trace
+            op,oo,_=parser_trace(osym,ox,seg);arch=ana.describe(op,oo)
+            repeat=native['RO']['descriptor'];cross=native['RU']['descriptor']
+            parity=ana.native_parity(arch,repeat,read(r['native']['path'])['energy_Eh'],native['RO']['energy_Eh'])
+            row.update(status='paired_complete' if parity['passed'] else 'parity_failed',parity=parity,
+                descriptors=dict(UD=ud,P25=arch,RO=repeat,RU=cross),
+                math=ana.member_math(ud,arch,repeat,cross),
+                native_audits={arm:native[arm]['native']['audit'] for arm in ARMS},
+                native_hashes={arm:sha(run/key/arm/'result.json') for arm in ARMS})
+        except Exception as e:
+            row.update(status='integrity_failed',error=type(e).__name__+': '+str(e))
+        rows.append(row)
+    # Detect any package, code, historical-data, or protected-profile mutation.
+    load_plan(a.plan,a.plan_commit)
+    classification=ana.classify_panel(rows)
+    d=dict(schema=SCHEMA,base=BASE,plan_sha256=sha(p),plan_commit=a.plan_commit,
+        requested_members=12,requested_native_slots=24,rows=rows,
+        paired_integrity_passed=all(r['status']=='paired_complete' for r in rows),
+        classification=classification,protected_population_unchanged=True,
+        adopted=False,model_calls=0,gradients=0,optimizations=0,
+        zero_QC_collection_wall_s=time.monotonic()-collection_start)
+    write(run/'summary.json',d)
+    write(run/'public-summary.json',public_summary(d))
+    print('Collected private crossed-profile run. Paired integrity passed:',d['paired_integrity_passed'])
+    return 0 if d['paired_integrity_passed'] else 2
+
+
+def check(a):
+    mac_only();p,m,by,_=load_plan(a.plan,a.plan_commit);run=private_path(a.run)
+    d=read(run/'summary.json')
+    if d.get('schema')!=SCHEMA or d.get('plan_sha256')!=sha(p):raise ValueError('Different summary')
+    if len(d['rows'])!=12 or {r['key'] for r in d['rows']}!=set(by):raise ValueError('Lost member')
+    if not d.get('paired_integrity_passed') or not d.get('protected_population_unchanged'):
+        raise ValueError('Panel incomplete or parity/protection gate failed')
+    if any(d.get(k)!=0 for k in ('model_calls','gradients','optimizations')) or d.get('adopted') is not False:
+        raise ValueError('Unregistered computation or adoption')
+    for row in d['rows']:
+        for arm in ARMS:
+            native,state=read_slot(run,row['key'],arm,sha(p),m['packages'],
+                by[row['key']]['raw' if arm=='RU' else 'segments']['sha256'])
+            if state!='completed' or sha(run/row['key']/arm/'result.json')!=row['native_hashes'][arm]:
+                raise ValueError('Native result changed after collection')
+            if (row['descriptors'][arm]!=native['descriptor'] or
+                row['native_audits'][arm]!=native['native']['audit']):
+                raise ValueError('Summary no longer matches the native descriptor or audit')
+        ds=row['descriptors']
+        parity=ana.native_parity(ds['P25'],ds['RO'],read(by[row['key']]['native']['path'])['energy_Eh'],
+            read(run/row['key']/'RO/result.json')['energy_Eh'])
+        if parity!=row['parity'] or not parity['passed']:raise ValueError('Parity was not reproduced')
+        if ana.member_math(ds['UD'],ds['P25'],ds['RO'],ds['RU'])!=row['math']:
+            raise ValueError('Decomposition changed')
+    if ana.classify_panel(d['rows'])!=d['classification']:
+        raise ValueError('Classification was not reproduced')
+    if public_summary(d)!=read(run/'public-summary.json'):
+        raise ValueError('Public allowlist summary changed')
+    print('24 one-SCF slots and 12 parity checks verified. No production adoption authorized.')
+    return 0
+
+
+def main():
+    if Path.cwd().resolve()!=ROOT:raise ValueError('Run from this checkout root')
+    ap=argparse.ArgumentParser(description=__doc__);sp=ap.add_subparsers(dest='cmd',required=True)
+    q=sp.add_parser('freeze');q.add_argument('--registration',required=True)
+    q.add_argument('--r10-manifest',required=True);q.add_argument('--r10-summary',required=True)
+    q.add_argument('--r10-plan-commit',required=True);q.add_argument('--out',required=True);q.set_defaults(fn=freeze)
+    for name,fn in (('run',runner),('collect',collect),('check',check),('_worker',worker)):
+        q=sp.add_parser(name);q.add_argument('--plan',required=True);q.add_argument('--plan-commit',required=True)
+        if name in ('collect','check'):q.add_argument('--run',required=True)
+        else:q.add_argument('--out',required=True)
+        if name=='_worker':q.add_argument('--key',required=True);q.add_argument('--arm',choices=ARMS,required=True)
+        q.set_defaults(fn=fn)
+    a=ap.parse_args();return a.fn(a)
+
+if __name__=='__main__':raise SystemExit(main())
```
<!-- END PATCH P44 -->

<!-- BEGIN PATCH P45 -->
```diff
diff --git a/README.md b/README.md
index 4576ae724b165a069bdccd012839178141fc8dd9..cbf40c26b31a639b33a9041adb30c4e4bffede81 100644
--- a/README.md
+++ b/README.md
@@ -53,7 +53,8 @@ energy-gradient mismatch unresolved; its numerical diagnostic budget is closed.
 See [round-7 evidence](docs/astra/round7/RESULTS.md) and
 [endpoint acceptance](docs/astra/round6/RESULTS.md).
 
-A [round-10 provenance review](docs/astra/round10/PROVENANCE_STATUS.md) located
-public UD geometry and raw-surface files. Matching those files to the Mac's
-historical profiles remains a separate zero-QC replay; the glycol mechanism
-and the closed numerical-gradient campaign are unchanged.
+The [round-10 replay](docs/astra/round10/RESULTS.md) matched all twelve recovered
+UD raw files to their historical profiles. The linear glycols have different
+stored conformations, but that observation alone does not separate geometry
+from electronic/cavity effects or identify the liquid-state distribution.
+The glycol mechanism remains unresolved; the numerical-gradient campaign stays closed.
diff --git a/docs/astra/round10/RESULTS.md b/docs/astra/round10/RESULTS.md
index 4140c6ef05c3f235eff72878269838f7c99affc0..0656f37159bbeb6f7a18477f91b513e46f3c3e0c 100644
--- a/docs/astra/round10/RESULTS.md
+++ b/docs/astra/round10/RESULTS.md
@@ -1,6 +1,6 @@
 # Round 10: measured results
 
-Reference: round 10 registered 2026-10-07 in 39cd85d (P41, P42, P43 and REG10 applied unchanged to 4dc8985). The comparison manifest was frozen in ba033e4 (SHA256 `4acf76db…fca0f`, in `PLAN_SHA256.txt`). Everything ran on the Mac in queue jobs 392 to 394. Nothing was computed: 0 SCF calls and 0 model calls. Acquisition took 5.9 s of wall time and the comparison 2.9 s.
+Reference: round 10 registered 2026-10-07 in 39cd85d (P41, P42, P43 and REG10 applied unchanged to 4dc8985). The comparison manifest was frozen in ba033e4 (SHA256 `4acf76db…fca0f`, in `PLAN_SHA256.txt`). Everything ran on the Mac in queue jobs 392 to 394. No new quantum-chemistry or activity-model evaluation was performed: 0 SCF calls and 0 model calls. Acquisition took 5.9 s of wall time and the comparison 2.9 s.
 
 Use terms: Victor confirmed the project is academic and non-profit before acquisition, as the NIST UD notice requires. The twelve raw `.cosmo` files and the detailed per-member comparison JSON stay in a private folder on the Mac, outside the repository. This file reports aggregate descriptors only.
 
@@ -45,10 +45,12 @@ Other descriptors:
 
 What this establishes, and what it does not:
 
-- **Geometry differs systematically.** The four UD linear glycols are fully extended, all-anti chains with no OH group near another oxygen. The open geometries all fold, with gauche O–C–C–O units and a terminal OH about 2.2 to 2.4 Å from an oxygen. For glycerol and propylene glycol the direction reverses: the UD geometry has the short OH···O approach, or both do. Those are exactly the two polyols where the P21 shape effect had the opposite sign. In the four linear glycols and propylene glycol, the geometry with the short OH···O approach has the smaller polar tail. Glycerol does not fit this simple picture: both geometries have a short approach, and the open tail is the larger one.
-- **Method difference at matched geometry is small.** Where the geometries match (water, methanol, THF, methoxyethanol, RMSD ≤ 0.02 Å), the raw tails differ by 0.4 to 2.9 Å². The linear glycols differ by 6.5 to 8.1 Å² raw and 8.6 to 10.8 Å² after averaging (tetraethylene glycol excepted).
-- **This is still descriptive.** It is not a causal partition. Under the registered decomposition, the crossed quantity p_O(R_U), the open method evaluated at the UD geometry, was not computed. The method difference at matched geometry is measured only on small rigid molecules, not on glycols. Nothing here shows which conformation is right for the liquid. UD's extended chains were partly revised to fit vapor pressures, so they are not an independent gas- or liquid-phase reference. Nothing is adopted: P35 stays unresolved, and the 630 + 6 profiles are unchanged.
+- **Geometry differs systematically.** The four UD linear glycols are fully extended, all-anti chains with no OH group near another oxygen. The open geometries all fold, with gauche O–C–C–O units and a terminal OH about 2.2 to 2.4 Å from an oxygen. For glycerol and propylene glycol the direction reverses: the UD geometry has the short OH···O approach, or both do. P21's mean normalized-shape Shapley contribution to ln γ∞ was small and positive for glycerol (+0.037), and opposite in sign for propylene glycol (−0.861). In the four linear glycols and propylene glycol, the geometry with the short OH···O approach has the smaller polar tail. Glycerol does not fit this simple picture: both geometries have a short approach, and the open tail is the larger one.
+- **Differences in near-matching heavy-atom controls are smaller.** For water, methanol, THF and methoxyethanol (reported heavy-atom RMSD ≤ 0.02 Å), the raw tails differ by 0.4 to 2.9 Å². The linear glycols differ by 6.5 to 8.1 Å² raw and 8.6 to 10.8 Å² after averaging (tetraethylene glycol excepted).
+- **This is still descriptive.** It is not a causal partition. Under the registered decomposition, the crossed quantity p_O(R_U), the open method evaluated at the UD geometry, was not computed. These controls do not establish a pure method effect: the coordinates are not identical, heavy-atom RMSD omits hydrogen positions, and methoxyethanol is flexible. In water, alignment of its single heavy atom gives zero heavy-atom RMSD irrespective of O-H bond geometry. Nothing here shows which conformation is right for the liquid. The UD notice reports empirical conformation revisions in the database but does not identify which glycol members were revised. The stored UD geometries are not an independently validated gas- or liquid-phase reference. Nothing is adopted: P35 stays unresolved, and the 630 + 6 profiles are unchanged.
 
 ## P43, reporting: applied
 
 In the registration commit, the README, `GLYCOL_STATUS.md` and `PROVENANCE_STATUS.md` were updated as supplied. A dated outcome line is appended to `PROVENANCE_STATUS.md` with this record, so its "not yet executed" sentence is no longer the current status.
+
+Wording clarification, round 11: the changes above qualify control matching and database-level provenance. They do not change a measured descriptor, replay gate, or the zero-QC scope of round 10.
```
<!-- END PATCH P45 -->

<!-- BEGIN PATCH REG11 -->
```diff
diff --git a/docs/astra/round11/REGISTRATION_PROPOSED.md b/docs/astra/round11/REGISTRATION_PROPOSED.md
new file mode 100644
index 0000000000000000000000000000000000000000..b839c03adec8e7c20f7b712db55e915bb4b2d23f
--- /dev/null
+++ b/docs/astra/round11/REGISTRATION_PROPOSED.md
@@ -0,0 +1,162 @@
+R11-P44-P45: private fixed-geometry crossed profiles
+
+Proposed registration, not an acceptance record. Append this text to
+PREREGISTRATION.md and commit it with the reviewed helpers before freezing a
+new plan. Base: 463ec1be5c0edfad1e8effd334a17fc44cd27405. This experiment is
+motivated by the observed R10 input-lineage and geometry results; those results
+are not a fresh holdout. R8/R9's numerical-gradient campaign remains closed.
+The 630 primary profiles and six flagged S1/S2 files remain frozen. P30/P32 and
+other prior scientific decisions are not reopened or overwritten.
+
+P44 is an A coordinate-input diagnostic with E same-input integrity controls.
+It does not change the open electronic method, introduce a conformer rule, or
+claim independent basis/grid/response convergence. Use exactly the twelve
+members and explicit source keys in r10_sources.DATA. Require the completed
+R10 private manifest and summary, their recorded plan commit, all twelve
+successful lineage gates, and all original input and protected-profile hashes.
+A missing private asset cannot be substituted, downloaded anew as a different
+version, re-embedded, or generated by another SCF.
+
+Real preparation, native execution and collection occur only on the private
+asset-bearing Mac, never on GitHub Actions, another CI system, or this review's
+container. Native and dense derived data stay in private directories outside
+all Git checkouts, with restrictive local permissions. Use the twelve already
+acquired raw UD files. Do not commit their coordinates, raw tesserae, dense
+profiles or private paths. The helper's public-summary.json is an allowlist of
+aggregate scalar descriptors and decisions, and still requires operator review
+before publication. No helper uploads an artifact or alters a production file.
+
+Freeze the R10 manifest and summary hashes, exact helper source hashes and
+normalized installed package versions in a private R11 plan. Pin PySCF 2.14.0;
+retain the R10 NumPy/SciPy/pandas/RDKit/parser environment. Record Python version
+and machine architecture. Commit only the new plan's SHA256 to
+ docs/astra/round11/PLAN_SHA256.txt
+before any SCF. Require the actual registration and plan commits to be ancestors
+of the executing HEAD. Package, source, input or protected-file drift blocks
+execution. Only the R10 test assertions for path aliases change; the R10
+scientific helpers and numerical gates remain unchanged.
+
+For every member run one new open-method calculation at its exact P25 stored
+geometry RO and one at the exact atomic coordinates extracted from the recovered
+UD raw file RU. Retain each file's own atom order, coordinate origin and
+orientation. No Kabsch alignment, canonical rotation, reflection, optimization,
+H-bond selection or modified bond geometry is applied to a calculation. The
+RO/RU order is the fixed SHA256(key)-parity order stored in the plan. All pairs
+run sequentially, each slot in a fresh subprocess. Geometry attribution means
+this full coordinate-input change; it is not an isolated torsional or H-bond
+intervention and may include finite-grid orientation dependence. The explicit
+PG stereochemical alias is retained without claiming identical stereochemistry.
+
+Use the unchanged r4_charge.factory and segments functions used by P25's
+TZVP/SWIG arm. They use BP86 (b88,p86), def2-TZVP, existing density fitting,
+XC grid level 3 with unchanged pruning, conv_tol 1e-9 and default orbital-gradient
+tolerance/SCF cycle limit, C-PCM epsilon 1e9, SWIG, Lebedev order 29 and the
+project's radii. Keep CachedPCM3c, its 2000 MB cache budget and nominal 4000 MB
+PySCF memory. Use four OpenMP threads and one BLAS thread. Verify SWIG and the
+method settings rather than accepting a changed default. No custom PySCF config (environment, working-directory or home file),
+new SCF solver, extra grid, charge correction, alternative guess, or gradient
+calculation is introduced. Save loaded upstream source hashes and runtime
+settings. One kernel call is one SCF attempt, not one SCF iteration.
+
+The budget is 24 SCF attempts, zero molecular gradients, zero optimizations and
+zero activity-model evaluations. Each subprocess has a 900-second wall ceiling,
+including its profile postprocessing. Thus reserved native slots total at most
+21600 seconds (six serial Mac hours); the driver has a 22500-second allocation
+including orchestration. A five-second process-kill/accounting allowance per
+slot is not extra scientific compute. Remaining slots are not started once the
+driver allocation is spent. Final zero-QC verification is reported separately,
+not hidden as another SCF budget. The plan has a permanent exclusive execution
+claim. No retry, resume, stale-claim removal, alternative output run, or budget
+extension is authorized. Independent slots continue after an earlier failure;
+missing, failed and timed-out identities remain in the requested denominator.
+No finished output can be replaced by a later favorable attempt.
+
+Require finite SCF energy and native convergence, electron-count error at most
+1e-7 e, and relative PCM linear-system residual at most 1e-10. Preserve the
+existing retained-surface filter, area > 1e-8 bohr^2. Record all/retained/discarded
+net charges and areas, with conservation checks at 1e-12 e and 1e-9 A2. The
+nonzero total screening charge is not itself a failure. Retained raw sigma
+outliers outside +/-0.025 e/A2 are not clipped or deleted. Report counts, area
+fractions, signed and absolute charge contributions, minimum patch areas and
+area-weighted sigma quantiles at 1, 5, 50, 95 and 99 percent. Report pre-filter
+extrema separately. Do not infer importance from a minimum sigma or node count
+alone. No neutralization or per-atom charge reassignment is allowed.
+
+Process every table through the identical pinned to_sigma.py Hsieh/NHB/OH/OT
+implementation and r4_common.parser_trace. Keep raw tessera tails, continuously
+averaged tessera tails and final binned tails distinct. Each tail uses
+absolute sigma >=0.01 e/A2, with the final grid rounded to three decimal places
+before the inclusive comparison. Keep unnormalized area profiles and separately
+normalized profiles. Do not normalize a difference or equate different-surface
+rows by tessera ordinal. Parser/domain failures are failed outputs; their completed native raw records
+remain private and available for accounting, without permission to change the parser.
+
+Reproduce the old R10 lineage/replay checks before attribution. For each new RO
+repeat versus its own P25 archive require strict differences below: 1e-4 A2
+maximum profile bin, 1e-5 normalized-profile L1, 1e-7 Eh total energy, 1e-5 e
+retained net charge, 1e-4 A2 total area and 1e-4 A3 cavity volume. These are
+same-input reproducibility tests, not an open-versus-UD agreement gate. This
+experiment performs no 25/2302 affinity test and makes no new global E claim
+for a changed production model. A larger cross-method or cross-geometry effect
+does not fail scientific acceptance. Failure of any native/lineage/parity
+control blocks the complete-panel attribution labels; partial results remain.
+
+For each observable save U, A, R, C, where U is the replayed UD result, A the
+archived P25 open result, R the new RO repeat and C the new RU crossed result.
+The requested historical decomposition is U-A=(C-A)+(U-C). The simultaneous
+current-run decomposition is U-R=(C-R)+(U-C). Report R-A explicitly and check
+both telescoping identities; do not hide reproducibility drift in a geometry
+term. Save the full 153-bin area and normalized-profile differences privately.
+Report signed scalar terms for every tail and net charge. No tail percentage
+is used as a percentage of ln gamma, MAE, or experimental error explained.
+
+The fixed background controls are water, methanol, methoxyethanol and THF.
+They are near-matching heavy-atom controls, not exact-geometry nulls or estimates
+of random SCF noise. For each scalar tail define the prospective background
+scale eta as the maximum of 0.5 A2, the largest control |U-R|, the largest
+control |C-R|, and four times the largest |R-A| across all twelve members.
+For normalized-profile L1 use the same rule with norms and a 0.01 floor.
+These formulas and control identities are fixed before crossed results. Their
+realized values are reported; no control is dropped, no threshold is tuned and
+no unresolved control is treated as zero. No statistical confidence level or
+basis/grid convergence is implied by eta.
+
+For each signed tail let D=U-R, G=C-R, M=U-C. Significant opposite signs,
+G*M<0 with min(|G|,|M|)>eta, give inconclusive_cancellation. Otherwise |D|<=2 eta
+is inconclusive_small_contrast. A geometry-dominant label requires G to have
+D's sign, |G|>eta and |M|<=max(eta,|D|/4). Interchange G and M for method-dominant.
+If both have D's sign and each magnitude exceeds eta, after the dominance
+checks, label both. Remaining cases are inconclusive_borderline. This is an
+operational effect-size convention, not a physical correctness test.
+
+For the normalized 153-bin differences use L1 norms Dn,Gn,Mn. Define cancellation
+excess Gn+Mn-Dn. If it exceeds max(2 eta,Dn/4), label inconclusive_cancellation;
+otherwise Dn<=2 eta is a small contrast. Geometry dominance requires
+Mn<=max(eta,Dn/4) and Gn>eta; method dominance is the reverse. Otherwise label
+both if Gn and Mn exceed eta, and inconclusive if they do not. Report the norms
+and cancellation excess. Repeating each classification with the archived
+instead of fresh RO result must leave the label unchanged, or that metric is
+inconclusive_repeat_boundary. Controls themselves remain descriptive. For every
+other member a broad profile-gap label is issued only when final binned-tail
+and normalized-shape labels agree on mainly_geometry, mainly_method or both.
+All other outcomes are metric-dependent or inconclusive. Net-charge and outlier
+changes are supporting diagnostics, not tie-breakers or selection criteria.
+
+An ordered decomposition does not identify the uncomputed reverse-method
+interaction or establish a unique, method-independent causal percentage.
+Even geometry dominance would not justify choosing the UD structure, rejecting
+folded states, changing the contact-angle rule, or weighting conformers to
+match the UD histogram. A future condensed-phase basin rule would require a
+common free-energy convention and independent sampling/thermal validation,
+including all eligible polyols and the water/branched controls. It receives
+zero budget and no adoption authorization in R11. A profile average is not
+assumed to equal a phase-equilibrated chemical potential. The existing incomplete
+P26/P29 pools are not accepted as an ensemble.
+
+P45 is E reporting. Update the README to acknowledge the completed R10 lineage
+replay. Qualify the R10 controls as near-matching heavy-atom geometries, avoid
+calling methoxyethanol rigid, and state that no per-glycol empirical-revision
+label has been verified. Distinguish glycerol's small positive P21 shape shift
+from propylene glycol's negative one. Preserve every measured number and prior failure.
+Do not claim the crossed calculation has run merely because this protocol
+and its code are committed. Record actual outcomes separately afterward.
```
<!-- END PATCH REG11 -->

Sources and verification

Repository paths below refer to `Victor-Liang-ChE/zcosmo` at `463ec1be5c0edfad1e8effd334a17fc44cd27405` unless a different reference is explicitly stated. The public-source URLs identify documentation only; no UD source data are bundled.

| Reference | Reviewed source and scope |
|---|---|
| S1 | `docs/astra/ROUND11_PROMPT.md`, blob `f5a78aa826576b7ddbe6e60aeebb0dc4da9f30f7`; `docs/OPTIMIZATION_BRIEF.md`, blob `9042052e2c0884226db6f795d14f8ec8c0157bd4`. Requested cross, private Mac venue and unchanged E/A rules. |
| S2 | `docs/astra/round10/RESULTS.md`, baseline blob `4140c6ef05c3f235eff72878269838f7c99affc0`. Actual lineage results, aggregate geometry/tail descriptors and Mac test deviations. |
| S3 | `docs/astra/round10/PROVENANCE_STATUS.md`, blob `0f8f1922275db5c1aef23e898d61d0b8473ed014`. Source identity, explicit PG alias, use restrictions and absence of individual electronic input decks/revision labels. |
| S4 | `PREREGISTRATION.md`, blob `7b16911e49a8632e1372a6d8cc643cf2365a09f5`, especially R10 registration/results; `docs/astra/round7/GLYCOL_STATUS.md`, blob `2674ec836839594d56a1d1d31a719666cd5a9d13`. Frozen profile version, scope of provenance reopening and unresolved physical mechanism. |
| S5 | `scripts/r10_sources.py`, `scripts/r10_replay.py`, `scripts/r10_selftest.py`, `scripts/r5_shape.py` and `scripts/r4_common.py`. Complete local copies were recovered from the archived reports and checked against their current Git blobs, recorded below. |
| S6 | `src/zcosmo/pyscf_cosmo.py`, blob `0f72e5383898d9c2cff21f2692ec6330c22d7a7a`; `scripts/r4_charge.py`, blob `5fb839d20dec4175a1a1b6473ea7041d3fc192e5`. P25 single-point settings, charge field, retained-area filter and unchanged parser adapter. |
| S7 | `README.md`, baseline blob `4576ae724b165a069bdccd012839178141fc8dd9`. Current-evidence language before P45. |
| S8 | `docs/astra/round4/RESULTS.md`, blob `428e5b4e0ce8801a5f55ac16d5a1a9a9217d400a`, P21 solvent table. Glycerol and propylene-glycol Shapley signs. |
| S9 | `docs/astra/round10/ZCOSMO_ROUND10_REPORT.md`, blob `9dd4e18c8c0fded6d744e5f356338ed916288bb1`. Complete preceding report and its actual source helpers; private command-path convention. |
| U1 | Pinned PySCF source: `https://raw.githubusercontent.com/pyscf/pyscf/v2.14.0/pyscf/__config__.py`. Environment, working-directory and home configuration-file search. |
| U2 | SCM primary documentation, “COSMO-RS with multi-species components”: `https://www.scm.com/doc/Tutorials/COSMO-RS/COSMO-RS_multispecies.html`, especially the phase-partition conformer example. Context for phase-dependent populations, not validation of Z0x or a software dependency. |

The following record is local software verification, not acceptance of a physical result. Its source hashes and patch hashes make the limited reconstructed-worktree scope explicit.

```json
{
  "base": "463ec1be5c0edfad1e8effd334a17fc44cd27405",
  "base_scope": "Git-blob-verified relevant subset; not a full clone",
  "verified_base_blobs": {
    "README.md": "4576ae724b165a069bdccd012839178141fc8dd9",
    "docs/astra/round10/RESULTS.md": "4140c6ef05c3f235eff72878269838f7c99affc0",
    "scripts/r10_sources.py": "cd90c5f96c91d95e58f912c7cd7659b562b08826",
    "scripts/r10_replay.py": "7d2bdded3403eaef8a1b13589f833b37caaa5f94",
    "scripts/r10_selftest.py": "a4571af86a19875ce7e21f30fe840b4aa532cefa",
    "scripts/r4_common.py": "d96484bbd0aed5aafeb47d038f6485055f425ecb",
    "scripts/r4_charge.py": "5fb839d20dec4175a1a1b6473ea7041d3fc192e5",
    "scripts/r5_shape.py": "1d539ee44b1e925d2e6cd4e821111b56ac173401",
    "scripts/r3_common.py": "bdddba8b5d5587891d945db585413c63371fa050",
    "scripts/r5_common.py": "f5d21bb018b69a7d6125380f1218b0991dd5bc50"
  },
  "prior_report_blob": "9dd4e18c8c0fded6d744e5f356338ed916288bb1",
  "patches": [
    {
      "id": "H11",
      "paths": [
        "scripts/r11_analysis.py",
        "scripts/r11_selftest.py",
        "scripts/r10_selftest.py"
      ],
      "sha256": "b72acbc96a1ea329414ac36d6313c8ac1776d0a2844107e9ea2f3a52e3214ba8",
      "independent_apply_check": true
    },
    {
      "id": "P44",
      "paths": [
        "scripts/r11_cross.py"
      ],
      "sha256": "178ae4b6413988a24cbd4a4cd0d1fe2423f10d9b5306ac35e4750d41e3458cf6",
      "independent_apply_check": true
    },
    {
      "id": "P45",
      "paths": [
        "README.md",
        "docs/astra/round10/RESULTS.md"
      ],
      "sha256": "4da34a2009c78615c7c27297b644746e599da012c949413e4d8db5f19b91427a",
      "independent_apply_check": true
    },
    {
      "id": "REG11",
      "paths": [
        "docs/astra/round11/REGISTRATION_PROPOSED.md"
      ],
      "sha256": "8c042da4ed45f6ee119cf61cebd7a08ed1bd852c7a550203c8d0e2d7ab1a4f06",
      "independent_apply_check": true
    }
  ],
  "combined_apply_check": true,
  "applied_bytes_match": true,
  "SCF_calls": 0,
  "real_UD_comparisons": 0,
  "remote_writes": 0,
  "production_changes": 0,
  "python_syntax": true,
  "CLI_help": true,
  "shell_syntax": true,
  "report_patch_extraction_checked": true,
  "main_rechecked": "463ec1be5c0edfad1e8effd334a17fc44cd27405",
  "R10_descriptor_table_preserved": true,
  "embedded_Python_blocks_parsed": 3,
  "portable_tests": {
    "R11": 22,
    "R10_after_path_assertion_fixes": 20,
    "passed": true,
    "scope": "Synthetic software tests and mock native interfaces; no actual UD or PySCF calculations"
  },
  "actual_Mac_freeze": false,
  "actual_Mac_run": false,
  "actual_Mac_check": false,
  "pyscf_status": "Absent; installation not attempted because native work is Mac-only"
}
```

Closing decision

Register the private twelve-member cross with fresh same-input controls. Interpret a completed run as an ordered explanation of the frozen profile difference, with the predeclared background and cancellation qualifications. Keep conformer selection and production replacement outside this experiment, regardless of which term dominates.
