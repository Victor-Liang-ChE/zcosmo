Z-COSMO round 13: close P35 with a coordinate-input explanation, not a new conformer rule

Reference: `Victor-Liang-ChE/zcosmo`, `main = e2b36c8c5c2273f47ee6df21975b295b93689ca8`. This review incorporates the R12 report and its measured outcome, including the P46a amendment. The attached report matches the repository blob; the relevant source reconstruction was checked against the current repository's file blobs. The proposed patches leave every production calculation unchanged. [S1-S4]

| Rank | ID | Target / pipeline | Class | Mechanism and expected saving | Effort |
|---:|---|---|:---:|---|---|
| 1 | P49 | README and dated P35 record | E reporting | Replace stale pre-scoring language with the completed R10-R12 finding and close the present explanatory campaign. Zero native or model evaluations. No solver speed-up claimed. | Low |
| 2 | P50 | `scripts/r13_closeout.py`, `scripts/r13_selftest.py` | E public-aggregate audit | Check P46a counts, printed-precision arithmetic and explicit 630-member cost scenarios. No private inputs or scientific rerun. | Low |
| Record | REG13 | Proposed closeout text | Policy, not a model | Zero new scientific budget; preserve all earlier acceptances and failures. | Very low |
| Not proposed for execution | A new production geometry/ensemble rule | Profile generation and phase thermodynamics | A if introduced | Physically motivated options exist, but no candidate has both an established acceptance path and a validated whole-portfolio cost here. Do not run another search solely to approach the observed UD result. | Substantial and not yet bounded by evidence |

The brief's saving-per-effort criterion does not produce a meaningful solver-acceleration ranking for documentation. Both implemented items have deterministic reporting checks rather than a speculative probability of improving accuracy. They avoid recomputing observations already obtained, including the 427-second R12 scoring run and the 594-second R11 single-point campaign. Those times are overlapping examples of unnecessary repetition, not additive speed-ups or promises of future runtime. P49 ranks first because the public conclusion is now stale; P50 checks its arithmetic at negligible cost. [S2, S5]

My recommendation is to close the current P35 explanatory campaign. There are defensible future conformer models, especially a declared finite-search conductor reference and a phase-equilibrated basin model. Neither is currently validated as a replacement for the frozen 630 profiles. This is not a claim that conformer calculations are inherently unaffordable, that every possible rule is invalid, or that the liquid-state question has been solved. It is a decision against adopting or launching a new geometry campaign from this retrospective success alone.

The completed evidence is substantial. R10 recovered inputs that reproduce the historical UD profiles. R11 evaluated the previously missing open-method cross at those coordinates. For EG, DEG and TEG, the registered raw, averaged and final polar-tail labels were mainly geometry. R12 then tested the consequence in the activity model, on the original inspected observations, rather than assuming that a tail-area fraction was an error fraction. That chain explains an important part of the stored-input discrepancy. It does not identify a thermodynamically correct liquid conformation. [S2, S5-S7]

P46a matters to the final statement. The accepted target contains 142 observations, including ten under EG's exact InChIKey. The additional EG observation was named “1,2-dihydroxyethane”; it was not a new molecule. The original archive has 13 solvent keys under 14 names. The amendment corrected conflicting counts before any P46 model call. The earlier 141-row report is superseded for these denominators, not for its other experimental rules. The measured run completed 1,562 finite requests, with no retry, and reproduced the historical anchors. [S2, S3]

Using the printed pooled values, the relevant calculation is

\[
 \frac{\mathrm{MAE}_{O}-\mathrm{MAE}_{C}}
      {\mathrm{MAE}_{O}-\mathrm{MAE}_{U}}
 =\frac{1.813-0.702}{1.813-0.419}
 =0.796987\ldots.
\]

Thus “about 80%” refers to the open-to-UD-solvent comparator gap. The fraction of the original open absolute error removed is instead `1.111 / 1.813 = 0.6128`, approximately 61%. The residual comparator difference is `0.702 - 0.419 = 0.283`. It is a difference of MAEs on these observations, not `mean(abs(pred_C - pred_U))`, not a bound on an electronic method, and not the entire remaining C error of 0.702. The original open solute profile is fixed in every arm, so U must not be described as an all-UD mixture. [S2; arithmetic reproduced here]

The pooled outcome is heavily weighted toward DEG: `108/142 = 76.1%` of the observations. The declared equal-solvent summary also improves, from 1.903 to 0.829, versus 0.539 for the U comparator. Both weightings belong in the record. The pooled result is not evidence for 142 independent solvent-level replications or an attribution across all 630 profiles. Three observations worsened and 139 improved. No confidence interval or out-of-sample claim is created by the new arithmetic audit. [S2]

The proposed geometry rules have different physical meanings.

| Rule | Defensible interpretation | Limitation and decision now |
|---|---|---|
| Maximize extension, minimize intramolecular O-H proximity, or maximize donor exposure | A declared geometric heuristic can be evaluated as an empirical model hypothesis. | Extension is not a free-energy criterion. Selecting this rule because it reproduces the inspected beneficial pattern is an adaptive model choice, even if its implementation never reads ThermoML. Applying it to every flexible molecule does not make it independently theory-derived. Do not adopt it as a fit-free liquid geometry rule. |
| Lowest gas-phase electronic energy after a fixed conformer search | A finite-search, zero-temperature gas-reference approximation. | It omits the solvent environment and basin entropy. Its winner need not be the conductor or liquid winner. It also differs from the v2 conductor-optimization protocol. |
| Lowest conductor electronic energy after a fixed, complete search | A physically interpretable single-basin conductor-reference approximation. It can be defined without UD or experimental response values. | It is not a liquid free-energy population. P26 already explored this idea and remained unaccepted because its required pools were incomplete. Reimplementing it under a new name would not resolve those deficiencies. |
| Lowest condensed-phase potential energy | A minimum of one specified approximate environment-dependent potential. | “Condensed phase” must name the environment and state. A minimum energy is not a finite-temperature basin free energy. Choosing a pure-liquid winner does not establish the same winner at infinite dilution in another solvent. |
| Boltzmann weights from conductor electronic energies, followed by a weighted sigma histogram | A fixed-reference ensemble approximation, provided every input and missing-state policy is explicit. | Electronic energies alone omit basin entropy and multiplicity. A histogram average is generally not a phase-equilibrated chemical potential. The legacy helper is not adequate validation of this rule. |
| Basin free energies with phase-dependent populations and a consistent excess-Gibbs functional | The strongest physical route in principle: conformers equilibrate in the actual environment, using one reference convention. | Requires complete enough sampling, thermal/reference information and numerical validation. These inputs are missing from the current accepted pipeline. No native or ensemble budget is proposed here. |

A conductor-reference rule is therefore not ruled out on scientific grounds. A concrete version would generate two fixed proposal pools for every structurally eligible flexible molecule, optimize every selected start with one predeclared protocol, and choose the lowest final conductor energy only after all required starts and integrity checks complete. The winner would be the lowest among that finite sample, not a demonstrated global minimum. Rank ties would use a fixed deterministic rule. R5 already supplies this architecture: two pools, four selected starts per pool, with a smaller two-start-per-pool probe. Its inclusion of donor hydrogens in the structural metric is more appropriate than treating near-degenerate heavy-atom structures as necessarily identical. [S8]

That architecture cannot currently be advertised as the missing glycol fix. P26's pilot ran 39 of 40 optimizations, with 36 reaching its original stationary-sample status, three capped, and one never run. Its complete-pool energy selection moved some glycol tails farther from UD, but that unfavorable proximity is not the reason to reject or change an energy rule. The formal problem was incomplete required evidence, and the later gradient campaign did not validate a replacement optimizer protocol. A conductor minimum could still be a reproducible A reference convention even when it worsens inspected IDAC scores. It cannot be sold as an independent liquid-state explanation merely because it has an energy objective. [S5, S8, S9]

The phase-dependent alternative can be stated without reference histograms. Let `n_ik` denote the amount of basin k of chemical species i, with `sum_k n_ik = n_i`. One possible thermodynamic architecture is

\[
 G(T,P,\{n_{ik}\})=
 \sum_{ik}n_{ik}a_{ik}(T,P)
 +RT\sum_{ik}n_{ik}\ln\!\frac{n_{ik}}{n}
 +G^{\rm ex}(T,P,\{n_{ik}\}).
\]

The basin standard `a_ik` must contain the intrinsic and nuclear free-energy contributions in one consistent convention. A degeneracy can enter as `-RT ln g_ik`, once. Minimize this G subject to the chemical-species constraints. For populated basins, the necessary stationarity equation gives

\[
 w_{ik}=\frac{\exp[-(a_{ik}+\mu^{\rm ex}_{ik})/(RT)]}
 {\sum_l\exp[-(a_{il}+\mu^{\rm ex}_{il})/(RT)]},
 \qquad w_{ik}=n_{ik}/n_i.
\]

Because the excess chemical potentials depend on the environment and its populations, pure-liquid and solution weights need not be equal. Solve the pure reference using the same functional. With consistent full chemical potentials, `ln gamma_i = (mu_i^mix - mu_i^pure - RT ln x_i)/(RT)`. This is a derivation of what a future model would need, not a claim that the required basin standards or a global minimization have been obtained. Equilibrium self-consistency is not statistical circularity; using measured IDAC values to choose basin energies or weights would be. [S10 for the existing finite-basin prototype; thermodynamic derivation here]

The conductor reference also creates a double-counting risk. Adding a gas electronic energy, a full conductor electronic energy and a solvation chemical potential without deriving their common energy cycle can count screening contributions twice. The R6 prototype attempted an explicit convention, but its missing thermal/basin audit was never supplied. Its existence is not permission to run it with zero thermal corrections or renormalize an incomplete catalog. A pure-liquid-minimum proxy can only replace a full population model after an independently checked dominance/error argument; the four known glycol conformers do not supply one. [S10]

Low-cost sampling methods are real tools, not a resolution of that reference problem. The CREST paper describes semiempirical conformer exploration and subsequent refinement, including implicit-solvent searches. Its entropy documentation separates a reference DFT thermal contribution from lower-cost ensemble corrections and recommends repeated sampling for stability. Those capabilities can reduce cost, but they do not certify the particular liquid populations needed by Z0x. Official COSMO-RS multispecies examples also explicitly allow conformer distributions to vary with solvent or composition. These references support the physical architecture, not a recommendation to use paid software or an acceptance of any particular implementation here. [U1-U3]

Validation without circularity is possible in principle, but the existing `test` label is insufficient now. The original split withheld 20% of compounds and kept water in train. Its test scorecards have since been reported and inspected, including across properties. Removing just the 142 glycol rows after seeing these results does not restore an untouched confirmatory set. A second property is not automatically independent: the project has already examined VLE and excess enthalpy, and an upstream database may itself have used property data in selecting inputs. No per-glycol empirical revision history has been verified. [S3, S5-S7]

For a future project, the first inexpensive prerequisite would be a metadata-only exposure and provenance audit performed before any new candidate score. It must distinguish response values actually inspected, aggregate scores already used during development, duplicated measurements, and the inputs used to train or calibrate any proposed potential. A genuinely unused external property set or new measurements can then be frozen by a custodian. Splits must respect shared chemical identities and experimental systems rather than treating temperatures from one binary as independent holdouts. The already-inspected glycol observations and their duplicates cannot enter acceptance. A more conservative design would reserve new compounds or publication groups, while keeping the known glycol examples solely as explanatory diagnostics.

Water and branched polyols must remain required controls, with a role fixed before results. They are useful guards against a universal donor-exposure story, but their known outcomes are development evidence, not fresh validation samples. Water has no backbone-conformer search to perform; a rule must not manufacture a water “conformer improvement” from a new optimization or grid. Glycerol and propylene glycol retain their contrary behavior and actual uncertainty. Computational acceptance would separately require complete requested inputs, reproducible population or winner choices across independent searches, preserved connectivity and defined reference conventions. It cannot discard expensive or unfavorable molecules and then report the surviving panel as the full eligible class. [S5-S8]

Only after freezing one candidate rule and its numerical gates should an untouched outcome set be read once. A possible confirmatory accuracy criterion would use an unchanged-coverage, paired system-level IDAC error difference with its upper confidence bound below zero, together with predeclared control/noninferiority criteria. The actual margins and sample-size requirements would have to be set before unblinding, not borrowed from the favorable 80% figure. Phase-matched spectroscopy could independently test a population hypothesis, while gas-phase conformer energies would test only the gas reference. Neither alone establishes solution activity accuracy. No such unexposed, sufficiently informative acceptance set has been established in this review, so no current replacement is described as ready for validation or deployment.

Free compute means an owned machine or available free quota, not zero computational work. The following sizing uses the existing protocol's structure and explicitly separates measured calibration from assumed costs. Let F be the number of eligible molecules, K the required starts per molecule and g_i the average number of SVP energy/gradient evaluations per start for molecule i. The finite-search effort is

\[
 N_{\rm SVP}=K\sum_{i=1}^{F}g_i,\qquad
 N_{\rm TZVP}=KF,\qquad
 W=\sum_{ik}\bigl(t_{\rm proposal,ik}+g_{ik}t_{\rm SVP,ik}+t_{\rm TZVP,ik}\bigr).
\]

One SVP evaluation is an energy-plus-gradient calculation containing an SCF solve, not one electronic iteration. To select a winner by the final TZVP conductor energy, every competing start needs its final single point; multiplying the final-profile cost by only 630 misses that work. The winning profile can be reused rather than calculated once more. Molecules outside the structural scope retain their old profiles unless a separate design explicitly requests repeats. The exact flexible subset count is not measured here, and ordinary rotatable-bond counts alone can miss ring or hydroxyl flexibility. [S8, S11]

| Sizing scenario, all 630 treated as eligible | Required final TZVP single points | SVP energy/gradient evaluations at an illustrative g=8 | Evaluation ceiling at 80 per start |
|---|---:|---:|---:|
| Four starts each, the P26 probe-sized search | 2,520 | 20,160 | 201,600 |
| Eight starts each, the two-pool full search | 5,040 | 40,320 | 403,200 |

The value eight is R5's small-panel median, used only to make the arithmetic concrete. A median is not a whole-portfolio mean, and the upper end contains the difficult molecules that motivated these reviews. The 80-step counts are ceilings for an illustrative extension of that cap, not proof that a converged catalog would be obtained. They are not authorized allocations. Restricting to a verified F instead of all 630 scales these counts by `F/630`; it does not remove the need to account for all excluded or unchanged molecules. [S8, S9]

For the eight-start scenario, assumed four-core SVP evaluation costs of 10, 60 and 300 seconds give `40,320*t/3,600 = 112, 672 and 3,360` worker-hours for optimization alone. The four-start values are 56, 336 and 1,680 worker-hours. These are sensitivity scenarios, not measured timings. At an illustrative one-worker-hour cap per start, an eight-start portfolio would reserve 5,040 four-core worker-hours. Dividing by 20 gives 252 ideal hours of concurrent capacity, excluding setup and availability. This is neither a promised completion time nor evidence of sufficient free Actions quota. Four-core worker-hours are not core-hours; multiplying by four gives the latter.

The R11 Mac calibration is quite different: `594/24 = 24.75` seconds per completed single-point slot, averaged over its known panel and orchestration. Naively transferring that mean would give 4.33 Mac hours for one single point on each of 630 molecules, 17.33 hours for four per molecule, and 34.65 hours for eight. Those figures omit every geometry optimization and do not estimate a validated 630-molecule ensemble. The largest molecules can have very different integral/cache costs. R11 gives evidence that a small frozen-geometry pilot is cheap; it does not show that a whole-portfolio search is cheap. [S5]

The existing legacy search would add `50*630 = 31,500` GFN2-xTB relaxations before any high-level selection if applied indiscriminately to the portfolio. A better sampling engine could reduce that count, but its actual coverage and timing would have to be measured. A full basin free-energy model costs more than energy ranking. For example, a central Cartesian finite-difference Hessian requires `6*N_atom` gradient evaluations per basin in a straightforward implementation. For an explicitly hypothetical 24-atom average and eight basins on 630 molecules, that is `144*5,040 = 725,760` extra gradients. Analytical Hessians or approximate thermal corrections can reduce this particular cost; the count is not a fundamental lower bound. Such approximations would be A choices requiring their own validation. [S11; sizing derivation here]

An explicit-solvent population route has no defensible converged cost estimate from the archived single points. Its work scales with independent replicas, trajectory duration, force-call cost and slow basin interchange. Duration has to be justified by statistical convergence, rather than selected because the free GPU allowance ends there. The earlier MACE free-energy timings do not establish polyol basin populations or a valid reference Hamiltonian. A small semiempirical or MLIP pilot is possible on free hardware, but it would answer the behavior of its chosen approximate Hamiltonian until independently validated. It is not a cheap automatic replacement for the missing liquid evidence. [S4, S10]

These numbers support a qualified conclusion: a conductor-reference search is computationally possible as a bounded A research project, and parts may be inexpensive. The obstacle to adoption is the combination of incomplete computational validation, absent population/reference information for a liquid rule, and no certified untouched acceptance set. A $0 invoice does not remove those requirements. I would not run a new 630-member campaign merely because R12 revealed an exposed-donor profile that performs better on the already-inspected glycol rows.

The source audit also identifies concrete risks in reusing existing helpers. `pyscf_cosmo_v2.run_one` starts from one seed-7 xTB path, or its saved checkpoint, and performs one conductor optimization. It does not claim a global conformer search. Its original Berny convergence is the registered predicate, and the closed response-gradient findings still limit full-energy stationarity claims. Running it on the frozen output directory is not a harmless audit: the cache check can reject historical files and proceed to regeneration. No command in this report invokes that path. [S11]

The older `zcosmo.conformers` helper is particularly unsuitable as an unattended prospective ensemble rule. Its `select` function chooses only the fifty most flexible eligible UD-covered compounds, with benchmark row counts as a tiebreaker, rather than all structurally eligible members of the 630. Its duplicate test can discard a geometrically distinct conformer solely because the energy differs by less than 0.1 kcal/mol. Near-degenerate energy does not imply duplicate geometry or an identical sigma profile. It also does not require the xTB BFGS convergence return before retaining a result. [S11]

In `combine`, missing conformer profile files are silently skipped and the remaining weights are normalized. That can make an incomplete catalog look like an ordinary smaller ensemble. The weights use electronic conductor energies at one temperature, and area/profile averaging supplies no independent phase-population validation. R5's newer helper explicitly blocks incomplete required pools and is materially better on this point. Do not treat a legacy implementation risk as evidence that the R12 explanatory result is invalid, or silently patch these rules and call the change E. Changing deduplication, failure acceptance, weighting or geometry selection can change scientific output and needs its own prospective A design. [S8, S11]

I found no reason to rewrite P46 or P47. Their important arithmetic distinction is correct: P46 applies the Shapley identity to negative absolute errors separately from prediction shifts; P47 partitions profile differences without claiming binwise prediction errors. P46a has corrected the exact-key count conflict. The new audit verifies only the public rounded aggregates. It does not replace the existing private identity, profile-hash or model checks. [S2, S3, S12]

The exact P35 wording is in P49's dated append below. It closes the explanatory campaign while preserving the unresolved liquid mechanism, the tetraEG exception and the conditional method-bundle residual. It records that the C-to-U comparison retains all remaining electronic/cavity and surface-representation differences, not merely the choice of density functional. The phrase “coordinates alone” is shorthand for the prescribed coordinate-input substitution at otherwise frozen settings, including its full representation; it is not an isolated torsion intervention. P47's donor/acceptor regional findings locate differences without proving hydrogen-bond energetics. [S2, S5]

The README patch removes the obsolete claim that IDAC consequences remain unmeasured. It does not label the extended geometry correct or announce a new accepted pipeline. The original R12 RESULTS and all prior registrations remain byte-for-byte unchanged. The proposed registration records closure separately, so the historical R12 statement that P35 was still open remains a valid record of that stage.

P50 reads only the already-public R12 RESULTS file and checks its exact Git blob before arithmetic. It treats three-decimal MAEs as independently rounded values. This matters for TEG: the printed `2.088-0.934` is 1.154, while the independently printed removed error is 1.153. Their rounding intervals overlap; it would be wrong to report this as a failed scientific identity. The reconstructed 79.7% ratio has a printed-rounding range of approximately 0.79627 to 0.79770, not a confidence interval. No private values were reconstructed or accessed.

The smallest remaining task is therefore reporting, not a new physical experiment. The present patches contain no conformer generator, revised electronic settings or activity evaluation. A future project can start with an unexposed-data and resource audit if that information actually becomes available, but this report does not create an automatic continuation. P35's current explanation is complete within its measured scope; the liquid-state and production-rule questions remain open without receiving a new budget.

Executed here: the public R12 RESULTS bytes, the current README/P35 bases and the reused R10-R12 helper files needed by the tests were verified against repository Git blobs. P50 ran on the actual public R12 archive, with the correct P46a counts. Its computation took about 0.001 seconds in this runtime, excluding Python startup, and produced no model requests. The new 15-test suite passed. The unchanged P46a-adjusted R12 suite passed 26 tests, R11 passed 22, and R10 passed 20, for 83 portable tests in total. Their native/model adapters are mocks and their data are fixtures. No real SCF or activity calculation was executed by those tests.

Independent and combined patch-application checks passed against the verified relevant-file reconstruction. The combined patch was applied to a fresh copy, its resulting files matched the reviewed bytes, and the new audit/documentation check passed there. Python syntax and the command blocks were checked. The delivered report's patch-extraction route was also verified before delivery.

Not executed: a private R12 replay, any UD-derived profile analysis, any real quantum or activity-model evaluation, a new conformer search, an Actions dispatch or a modification to the remote repository. PySCF and pyberny are absent here; no installation was attempted because the proposed work has zero native budget. This runtime holds a verified relevant-file reconstruction rather than a full repository clone. The clean-HEAD guard and adoption commit below are commands for the maintainer, not operations claimed to have been run against the user's actual checkout. The observed R10-R12 scientific results remain the maintainer's archived measurements, and no new experimental acceptance is claimed.

The following commands are the complete application and checking path. They create no native workflow and perform no private-Mac scoring. Use an existing checkout at the reviewed commit. The standard-library P50 checks work without PySCF; the optional regression checks use the existing environment already used for R10-R12. Do not install a new quantum-chemistry environment for this closeout.

```bash
set -euo pipefail
export BASE=e2b36c8c5c2273f47ee6df21975b295b93689ca8
: "${REPORT:?Set REPORT to the saved ZCOSMO_ROUND13_REPORT.md}"
export REPORT
export PYTHONPATH=src:scripts
export MPLBACKEND=Agg

test "$(git rev-parse HEAD)" = "$BASE"
git diff --quiet
git diff --cached --quiet
export PATCHDIR="$(mktemp -d "${TMPDIR:-/tmp}/zc-r13-patches.XXXXXXXX")"
python - <<'PY'
import os,re
from pathlib import Path
text=Path(os.environ['REPORT']).read_text()
out=Path(os.environ['PATCHDIR'])
for name in ('P49','P50','REG13'):
    pattern=r'<!-- BEGIN PATCH '+name+r' -->\s*```diff\n(.*?)\n```\s*<!-- END PATCH '+name+r' -->'
    matches=re.findall(pattern,text,re.S)
    if len(matches)!=1:raise ValueError('Missing or duplicate patch: '+name)
    with (out/(name+'.patch')).open('x') as handle:handle.write(matches[0]+'\n')
PY
for name in P49 P50 REG13; do
    git apply --check "$PATCHDIR/$name.patch"
done
cat "$PATCHDIR/P49.patch" "$PATCHDIR/P50.patch" "$PATCHDIR/REG13.patch" > "$PATCHDIR/all.patch"
git apply --check "$PATCHDIR/all.patch"
git apply "$PATCHDIR/all.patch"
python scripts/r13_selftest.py
python -m py_compile scripts/r13_closeout.py scripts/r13_selftest.py
```

Adopt the reporting record before the new archive-audit output is used. The code's proposed registration is not itself a claim that the maintainer accepted it. This command records the actual adoption timestamp and commits only the named reporting changes. It does not alter a prior result or create an executable scientific budget.

```bash
set -euo pipefail
python - <<'PY'
from datetime import datetime,timezone
from pathlib import Path
p=Path('PREREGISTRATION.md')
old=p.read_text()
marker='R13-P49-P50: P35 explanatory closeout, no production geometry rule'
if marker in old:raise ValueError('R13 reporting record already exists; do not duplicate it')
text=Path('docs/astra/round13/REGISTRATION_PROPOSED.md').read_text()
assert text.startswith(marker)
stamp=datetime.now(timezone.utc).isoformat()
p.write_text(old.rstrip()+'\n\nRound 13 reporting closeout adopted '+stamp+
    '. Zero new native or model budget.\n\n'+text)
PY
git add README.md docs/astra/round7/GLYCOL_STATUS.md \
    scripts/r13_closeout.py scripts/r13_selftest.py \
    docs/astra/round13/REGISTRATION_PROPOSED.md PREREGISTRATION.md
git commit -m "Record R13 P35 explanatory closeout without a new geometry rule"
```

The benchmark is the read-only audit itself. It reports its measured wall time and verifies the documentation qualifications. The output contains only previously public aggregate arithmetic and declared sizing scenarios. It is not a new scorecard or an adoption record. A fresh output name is required; repeated checks never overwrite a prior result.

```bash
set -euo pipefail
export CHECKDIR="$(mktemp -d "${TMPDIR:-/tmp}/zc-r13-check.XXXXXXXX")"
/usr/bin/time -p python scripts/r13_closeout.py --repo . \
    --check-docs --out "$CHECKDIR/public-closeout-audit.json"
python - <<'PY'
import json,os
from pathlib import Path
p=Path(os.environ['CHECKDIR'])/'public-closeout-audit.json'
d=json.loads(p.read_text())
assert d['SCF_calls']==d['activity_model_calls']==0
assert d['adoption_authorized'] is False and d['new_scientific_gate_passed'] is False
assert d['public_aggregate_arithmetic']['rows']==142
print(json.dumps(d,indent=2))
PY
```

The unchanged R10-R12 portable suites can also be run in their existing environment. Their printed “model requests” and “SCF slots” are mock orchestration fixtures, not new chemistry. The P50 task does not depend on running these suites on the Mac or on locating any UD input.

```bash
set -euo pipefail
export PYTHONPATH=src:scripts
export MPLBACKEND=Agg
python scripts/r12_selftest.py
python scripts/r11_selftest.py
python scripts/r10_selftest.py
```

The independent unified diffs follow. Supplying REG13 is not itself adoption of its proposed stopping decision.

<!-- BEGIN PATCH P49 -->
```diff
diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -54,14 +54,24 @@
 See [round-7 evidence](docs/astra/round7/RESULTS.md) and
 [endpoint acceptance](docs/astra/round6/RESULTS.md).
 
-The [round-10 replay](docs/astra/round10/RESULTS.md) matched all twelve recovered
-UD raw files to their historical profiles. The linear glycols have different
-stored conformations, but that observation alone does not separate geometry
-from electronic/cavity effects or identify the liquid-state distribution.
-The glycol mechanism remains unresolved; the numerical-gradient campaign stays closed.
+The [round-10 replay](docs/astra/round10/RESULTS.md) linked all twelve recovered
+UD raw files to their historical profiles. The [round-11 ordered cross](docs/astra/round11/RESULTS.md)
+attributed the polar-tail gaps for ethylene, diethylene and triethylene glycol
+mainly to stored coordinate inputs, without a whole-profile attribution label.
+Tetraethylene glycol differed: its raw-tail gap was mainly method.
 
-The [round-11 fixed-coordinate cross](docs/astra/round11/RESULTS.md) attributes
-polar-tail gaps mainly to stored coordinate inputs for ethylene, diethylene and
-triethylene glycol. Tetraethylene glycol's raw-tail gap is mainly method; no
-whole-profile attribution label passed. The liquid-conformer distribution and
-the consequences for IDAC error remain unresolved. No crossed profile or conformer-selection rule is adopted.
+In [round-12 retrospective scoring](docs/astra/round12/RESULTS.md), on 142
+already-inspected glycol-solvent observations, using our open method at the UD
+solvent coordinates reduced MAE in ln gamma from 1.813 to 0.702, versus 0.419
+for the UD-solvent comparator. Original open solute profiles and Z0x were held
+fixed. This removes about 80% of the open-to-UD comparator error gap, mainly
+through shape; tetraethylene glycol recovers only 13%. The remaining 0.283
+pooled MAE difference is conditional on the same-coordinate method-bundle
+comparison. It is not the total remaining experimental error or a universal
+method-error bound.
+
+These inspected-row results do not establish the liquid conformer distribution
+or a held-out accuracy improvement. No crossed profile or conformer-selection
+rule is adopted. The 630 primary plus six flagged profiles remain frozen.
+P35's present explanatory campaign is closed with these findings; its liquid-state
+mechanism remains unresolved. The separate numerical-gradient campaign stays closed.
diff --git a/docs/astra/round7/GLYCOL_STATUS.md b/docs/astra/round7/GLYCOL_STATUS.md
--- a/docs/astra/round7/GLYCOL_STATUS.md
+++ b/docs/astra/round7/GLYCOL_STATUS.md
@@ -61,3 +61,50 @@
 conformer populations. A future liquid free-energy protocol would require a
 separate prospective design and independent validation. The 630 primary and
 six S1/S2 profiles remain frozen, and the numerical-gradient campaign stays closed.
+
+Update, round 13: close the present P35 explanatory campaign with the R10-R12 finding.
+
+R10 established the lineage of all twelve recovered UD raw files. R11's ordered
+open-method cross attributes the raw, averaged and final polar-tail gaps for
+ethylene, diethylene and triethylene glycol mainly to their stored coordinate
+inputs. This includes the full coordinate representation and does not isolate
+an intramolecular hydrogen-bond energy. R11's whole-profile labels remain
+metric-dependent or inconclusive under the unchanged control scale.
+
+R12, including the prospectively recorded count amendment P46a, performed
+retrospective ThermoML scoring on 142 already-inspected glycol-solvent rows:
+EG 10, DEG 108, TEG 17 and tetraEG 7. With the original open solutes and Z0x
+fixed, replacing the open solvent input O by C, the open method at the UD
+coordinates, reduced pooled MAE from 1.813 to 0.702. The UD-solvent comparator
+U had MAE 0.419. The reduction of 1.111 removes about 80% of the O-to-U comparator
+gap, not 80% of O's absolute error. A total of 139 rows improved and three
+worsened. The error-reduction Shapley contribution was +1.103 from shape,
++0.009 from area and -0.001 from volume. All comparisons use the same P28 endpoint.
+
+Tetraethylene glycol is an explicit exception: only about 13% of its IDAC gap
+was recovered by coordinates, and its R11 raw-tail gap was mainly method.
+The remaining pooled C-to-U comparator gap is approximately 0.283 in ln gamma.
+It is a difference of MAEs for these fixed solutes and observations, not a
+mean absolute prediction difference, a universal electronic-method error, or
+an attribution of C's entire 0.702 experimental error. The method bundle
+includes the remaining electronic/cavity, charge and surface representation.
+R12's private regional analysis locates a donor-side coordinate redistribution
+for EG/DEG/TEG and an acceptor-side residual method redistribution; it does not
+assign a prediction error or hydrogen-bond energy to a sigma bin.
+
+The stored UD structures are not validated equilibrium liquid conformations.
+The database notice reports some empirical conformation revisions without
+identifying which glycol members were revised. A rule chosen to enforce the
+observed extended geometry would encode this inspected result even without
+reading an experimental-value column during execution. No adoption follows.
+The result neither accepts an incomplete conformer pool nor establishes a new
+independent holdout. A prospective conductor-reference rule or phase-equilibrated
+basin model would require a separate physical definition and validation design.
+
+The present P35 explanatory campaign is closed. The liquid-state distribution
+and a production conformer-selection rule remain unresolved. No further QC,
+conformer search, population calculation or experimental scoring is authorized
+by this closeout. The 630 primary and six S1/S2 profiles remain frozen. All
+prior gates and the separate R8/R9 numerical-gradient closure remain unchanged.
+The historical records above are retained; completed outcomes are in
+[round 11](../round11/RESULTS.md) and [round 12](../round12/RESULTS.md).
```
<!-- END PATCH P49 -->

<!-- BEGIN PATCH P50 -->
```diff
diff --git a/scripts/r13_closeout.py b/scripts/r13_closeout.py
new file mode 100644
--- /dev/null
+++ b/scripts/r13_closeout.py
@@ -0,0 +1,190 @@
+"""E reporting audit of public, rounded R12 aggregates. No chemistry imports.
+
+This does not rerun P46, access private inputs, or accept a conformer rule.
+Cost outputs are explicit sizing scenarios, not measured portfolio forecasts.
+"""
+from __future__ import annotations
+import argparse
+from decimal import Decimal as D
+import hashlib
+import itertools
+import json
+from pathlib import Path
+import time
+
+BASE = 'e2b36c8c5c2273f47ee6df21975b295b93689ca8'
+SOURCE = 'docs/astra/round12/RESULTS.md'
+SOURCE_BLOB = 'c036e8e24aa45a03aed0485664b3a26cd842c17f'
+COUNTS = {'ethylene glycol': 10, 'diethylene glycol': 108,
+          'triethylene glycol': 17, 'tetraethylene glycol': 7}
+HEADER = ('solvent', 'rows', 'MAE O', 'MAE C', 'MAE U', 'removed O→C',
+          'signed recovery', 'rows improved / worsened')
+
+
+def require(ok: bool, message: str) -> None:
+    if not ok:
+        raise ValueError(message)
+
+
+def blob(data: bytes) -> str:
+    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
+
+
+def decimal(text: str) -> D:
+    value = D(text)
+    require(value.is_finite(), 'Nonfinite public number')
+    return value
+
+
+def rounding_interval(value: D, places: int = 3) -> tuple[D, D]:
+    half = D(5).scaleb(-places - 1)
+    return value - half, value + half
+
+
+def difference_interval(a: D, b: D) -> tuple[D, D]:
+    al, ah = rounding_interval(a)
+    bl, bh = rounding_interval(b)
+    return al - bh, ah - bl
+
+
+def overlaps(left: tuple[D, D], right: tuple[D, D]) -> bool:
+    return max(left[0], right[0]) <= min(left[1], right[1])
+
+
+def recovery_interval(o: D, c: D, u: D) -> tuple[D, D]:
+    require(rounding_interval(o)[0] > rounding_interval(u)[1],
+            'Rounded comparator denominator can reach zero')
+    corners = itertools.product(*(rounding_interval(v) for v in (o, c, u)))
+    values = [(a - b) / (a - z) for a, b, z in corners]
+    return min(values), max(values)
+
+
+def table(text: str) -> dict:
+    rows = {}
+    active = False
+    for line in text.splitlines():
+        if not line.startswith('|'):
+            if active:
+                break
+            continue
+        cells = tuple(c.strip().replace('**', '') for c in line.strip('|').split('|'))
+        if cells == HEADER:
+            require(not active, 'Duplicated result header')
+            active = True
+            continue
+        if not active or all(set(c) <= set('-: ') for c in cells):
+            continue
+        require(len(cells) == len(HEADER), 'Malformed public result row')
+        name, count, o, c, u, removed, recovery, changes = cells
+        require(name not in rows, 'Duplicate solvent or pooled row')
+        require(name in COUNTS or name == 'pooled', 'Unexpected solvent identity')
+        imp, bad = map(int, changes.split('/'))
+        require(imp >= 0 and bad >= 0, 'Negative outcome count')
+        values = list(map(decimal, (o, c, u, removed, recovery)))
+        require(all(v >= 0 for v in values[:3]), 'Negative MAE')
+        rows[name] = dict(rows=int(count), O=values[0], C=values[1], U=values[2],
+                          removed=values[3], recovery=values[4], improved=imp, worsened=bad)
+    require(set(rows) == set(COUNTS) | {'pooled'}, 'Missing public solvent or pooled row')
+    require({k: rows[k]['rows'] for k in COUNTS} == COUNTS, 'P46a denominators changed')
+    pool = rows['pooled']
+    require(pool['rows'] == sum(COUNTS.values()) == 142, 'Wrong pooled denominator')
+    for name, row in rows.items():
+        require(row['improved'] + row['worsened'] == row['rows'], 'Outcome count mismatch')
+        require(overlaps(difference_interval(row['O'], row['C']),
+                         rounding_interval(row['removed'])), 'Inconsistent rounded MAE reduction')
+        require(overlaps(recovery_interval(row['O'], row['C'], row['U']),
+                         rounding_interval(row['recovery'], 2)), 'Inconsistent rounded recovery')
+    for field in ('improved', 'worsened'):
+        require(sum(rows[k][field] for k in COUNTS) == pool[field], 'Pooled outcomes do not add')
+    for field in ('O', 'C', 'U'):
+        # Weighted solvent means and the published pooled mean were rounded independently.
+        lo = sum(COUNTS[k] * rounding_interval(rows[k][field])[0] for k in COUNTS) / 142
+        hi = sum(COUNTS[k] * rounding_interval(rows[k][field])[1] for k in COUNTS) / 142
+        require(overlaps((lo, hi), rounding_interval(pool[field])), 'Pooled rounding ranges conflict')
+    return rows
+
+
+def sizing(n: int = 630) -> dict:
+    require(type(n) is int and n > 0, 'Positive integer portfolio size required')
+    cases = []
+    for starts in (4, 8):
+        evaluations = n * starts * 8
+        cases.append(dict(molecules=n, starts_each=starts, assumed_SVP_evaluations_each=8,
+            TZVP_single_points=n * starts, SVP_energy_gradient_evaluations=evaluations,
+            SVP_evaluation_ceiling_at_80_per_start=n * starts * 80,
+            four_core_SVP_hours_at_assumed_seconds={str(t): evaluations * t / 3600 for t in (10, 60, 300)},
+            Mac_SP_hours_if_R11_small_panel_mean_transferred=n * starts * (594 / 24) / 3600,
+            one_hour_per_start_allocation_worker_hours=n * starts,
+            ideal_20_runner_hours_for_that_allocation=n * starts / 20))
+    return dict(cases=cases, all_molecules_treated_as_search_eligible_for_sizing=True,
+        exact_flexible_population_count_not_measured=True,
+        legacy_50_embedding_xTB_relaxations=n * 50,
+        notes='Sizing only. No QC execution or account-quota claim. Eight steps is a sample-median '
+              'scenario, not a portfolio mean. SVP times omit proposal work and TZVP. Mac '
+              'SP extrapolation omits optimization, thermal calculations and validation.')
+
+
+def arithmetic(rows: dict) -> dict:
+    p = rows['pooled']
+    o, c, u = (p[k] for k in ('O', 'C', 'U'))
+    low, high = recovery_interval(o, c, u)
+    return dict(rows=p['rows'], improved=p['improved'], worsened=p['worsened'],
+        removed_from_rounded_MAEs=float(o-c), residual_comparator_MAE_gap=float(c-u),
+        comparator_gap_recovery=float((o-c)/(o-u)),
+        comparator_recovery_rounding_range=[float(low), float(high)],
+        original_absolute_error_fraction_removed=float((o-c)/o),
+        DEG_row_weight=float(D(COUNTS['diethylene glycol']) / p['rows']),
+        interpretation='80 percent refers to the O-to-U comparator gap, not original absolute error. '
+                       'The residual is a difference of MAEs, not mean absolute C-minus-U predictions. '
+                       'Intervals propagate printed rounding only, not sampling uncertainty.')
+
+
+def audit(repo: Path) -> dict:
+    path = repo / SOURCE
+    raw = path.read_bytes()
+    require(blob(raw) == SOURCE_BLOB, 'Public R12 source changed; do not infer a new archive')
+    rows = table(raw.decode('utf-8'))
+    answer = dict(base=BASE, source=SOURCE, source_blob=SOURCE_BLOB,
+        source_sha256=hashlib.sha256(raw).hexdigest(), public_aggregate_arithmetic=arithmetic(rows),
+        hypothetical_portfolio_sizing=sizing(), SCF_calls=0, activity_model_calls=0,
+        private_assets_read=False, adoption_authorized=False, new_scientific_gate_passed=False)
+    require(path.read_bytes() == raw, 'Public source changed during audit')
+    return answer
+
+
+def check_docs(repo: Path) -> None:
+    readme = (repo / 'README.md').read_text()
+    status = (repo / 'docs/astra/round7/GLYCOL_STATUS.md').read_text()
+    for phrase in ('142', '1.813', '0.702', '0.419', '80%', '13%', 'retrospective',
+                   'No crossed profile', 'closed'):
+        require(phrase in readme, 'README closeout qualification missing: ' + phrase)
+    for phrase in ('P46a', '0.283', 'difference of MAEs', 'whole-profile', '139',
+                   'liquid', 'No adoption', 'closed'):
+        require(phrase in status, 'P35 closeout qualification missing: ' + phrase)
+    for phrase in ('ZC_R6_ENDPOINT=1', 'compatibility gate', 'six separately flagged S1/S2'):
+        require(phrase in readme, 'Earlier README qualification removed: ' + phrase)
+    require('the consequences for IDAC error remain unresolved' not in readme,
+            'Stale pre-P46 README wording remains')
+
+
+def main() -> int:
+    parser = argparse.ArgumentParser(description=__doc__)
+    parser.add_argument('--repo', type=Path, default=Path('.'))
+    parser.add_argument('--out', type=Path, required=True)
+    parser.add_argument('--check-docs', action='store_true')
+    args = parser.parse_args()
+    start = time.perf_counter()
+    result = audit(args.repo.resolve())
+    if args.check_docs:
+        check_docs(args.repo.resolve())
+    result['audit_wall_s'] = time.perf_counter() - start
+    # Fresh output only. The fixed input is never overwritten.
+    with args.out.open('x', encoding='utf-8') as handle:
+        json.dump(result, handle, indent=2, allow_nan=False)
+        handle.write('\n')
+    print('Public rounding/count audit passed. Zero chemistry evaluations; no adoption.')
+    return 0
+
+
+if __name__ == '__main__':
+    raise SystemExit(main())
diff --git a/scripts/r13_selftest.py b/scripts/r13_selftest.py
new file mode 100644
--- /dev/null
+++ b/scripts/r13_selftest.py
@@ -0,0 +1,99 @@
+"""Portable R13 software tests. Fixtures contain public aggregate numbers only."""
+from decimal import Decimal as D
+import tempfile
+from pathlib import Path
+import unittest
+from unittest.mock import patch
+import r13_closeout as r
+
+FIXTURE = '''| solvent | rows | MAE O | MAE C | MAE U | removed O→C | signed recovery | rows improved / worsened |
+|---|---:|---:|---:|---:|---:|---:|---|
+| ethylene glycol | 10 | 2.541 | 0.559 | 0.498 | 1.982 | 0.97 | 10 / 0 |
+| diethylene glycol | 108 | 1.740 | 0.648 | 0.371 | 1.092 | 0.80 | 105 / 3 |
+| triethylene glycol | 17 | 2.088 | 0.934 | 0.556 | 1.153 | 0.75 | 17 / 0 |
+| tetraethylene glycol | 7 | 1.242 | 1.175 | 0.731 | 0.067 | 0.13 | 7 / 0 |
+| **pooled** | **142** | **1.813** | **0.702** | **0.419** | **1.111** | **0.80** | **139 / 3** |
+'''
+
+
+class CloseoutTests(unittest.TestCase):
+    def test_P46a_counts(self):
+        self.assertEqual(r.table(FIXTURE)['ethylene glycol']['rows'], 10)
+        self.assertEqual(r.table(FIXTURE)['pooled']['rows'], 142)
+
+    def test_wrong_old_count_rejected(self):
+        with self.assertRaises(ValueError): r.table(FIXTURE.replace('glycol | 10 |', 'glycol | 9 |'))
+
+    def test_missing_solvent_rejected(self):
+        with self.assertRaises(ValueError): r.table('\n'.join(FIXTURE.splitlines()[:-2]))
+
+    def test_duplicate_row_rejected(self):
+        with self.assertRaises(ValueError): r.table(FIXTURE + FIXTURE.splitlines()[2] + '\n')
+
+    def test_nonfinite_rejected(self):
+        with self.assertRaises(ValueError): r.table(FIXTURE.replace('2.541', 'NaN'))
+
+    def test_wrong_outcomes_rejected(self):
+        with self.assertRaises(ValueError): r.table(FIXTURE.replace('105 / 3', '105 / 2'))
+
+    def test_rounding_is_not_false_exactness(self):
+        rows = r.table(FIXTURE)
+        z = rows['triethylene glycol']
+        self.assertNotEqual(z['O'] - z['C'], z['removed'])
+        self.assertTrue(r.overlaps(r.difference_interval(z['O'], z['C']), r.rounding_interval(z['removed'])))
+
+    def test_false_recovery_rejected(self):
+        with self.assertRaises(ValueError): r.table(FIXTURE.replace('0.97', '0.85'))
+
+    def test_recovery_denominator(self):
+        q = r.arithmetic(r.table(FIXTURE))
+        self.assertAlmostEqual(q['comparator_gap_recovery'], .7969870875, places=9)
+        self.assertAlmostEqual(q['original_absolute_error_fraction_removed'], .6127964699, places=9)
+        self.assertGreater(q['comparator_gap_recovery'], q['original_absolute_error_fraction_removed'])
+
+    def test_zero_denominator_rejected(self):
+        with self.assertRaises(ValueError): r.recovery_interval(D('1'), D('.5'), D('1'))
+
+    def test_cost_units(self):
+        q = r.sizing()['cases'][1]
+        self.assertEqual(q['TZVP_single_points'], 5040)
+        self.assertEqual(q['SVP_energy_gradient_evaluations'], 40320)
+        self.assertEqual(q['four_core_SVP_hours_at_assumed_seconds']['60'], 672)
+        self.assertAlmostEqual(q['Mac_SP_hours_if_R11_small_panel_mean_transferred'], 34.65)
+
+    def test_invalid_portfolio(self):
+        for n in (0, -1, 2.5, True):
+            with self.assertRaises(ValueError): r.sizing(n)
+
+    def test_blob_verification_and_source_unchanged(self):
+        with tempfile.TemporaryDirectory() as directory:
+            root = Path(directory); path = root / r.SOURCE; path.parent.mkdir(parents=True)
+            path.write_text(FIXTURE)
+            raw = path.read_bytes()
+            with self.assertRaises(ValueError): r.audit(root)
+            with patch.object(r, 'SOURCE_BLOB', r.blob(raw)):
+                q = r.audit(root)
+            self.assertFalse(q['adoption_authorized'])
+            self.assertFalse(q['new_scientific_gate_passed'])
+            self.assertEqual(q['SCF_calls'], 0)
+            self.assertEqual(path.read_bytes(), raw)
+
+    def test_fresh_output_only(self):
+        with tempfile.TemporaryDirectory() as directory:
+            out = Path(directory) / 'existing.json'; out.write_text('keep')
+            with patch('sys.argv', ['r13', '--out', str(out)]), patch.object(r, 'audit', return_value={}):
+                with self.assertRaises(FileExistsError): r.main()
+            self.assertEqual(out.read_text(), 'keep')
+
+    def test_no_chemistry_imports(self):
+        import ast
+        tree = ast.parse(Path(r.__file__).read_text())
+        imports = set()
+        for node in ast.walk(tree):
+            if isinstance(node, ast.Import): imports.update(x.name.split('.')[0] for x in node.names)
+            if isinstance(node, ast.ImportFrom): imports.add((node.module or '').split('.')[0])
+        self.assertFalse(imports & {'pyscf', 'rdkit', 'zcosmo', 'r12_review', 'numpy', 'pandas'})
+
+
+if __name__ == '__main__':
+    unittest.main(verbosity=2)
```
<!-- END PATCH P50 -->

<!-- BEGIN PATCH REG13 -->
```diff
diff --git a/docs/astra/round13/REGISTRATION_PROPOSED.md b/docs/astra/round13/REGISTRATION_PROPOSED.md
new file mode 100644
--- /dev/null
+++ b/docs/astra/round13/REGISTRATION_PROPOSED.md
@@ -0,0 +1,59 @@
+R13-P49-P50: P35 explanatory closeout, no production geometry rule
+
+Proposed record, not a claim of adoption. Append the adopted text to
+PREREGISTRATION.md with the actual timestamp and commit before running the new
+reporting command. Base: e2b36c8c5c2273f47ee6df21975b295b93689ca8.
+The review has already inspected the public R10-R12 outcomes and performed
+retrospective arithmetic on their rounded summaries. No new holdout or
+prospectively discovered scientific effect is claimed.
+
+P49 is E reporting. Replace the stale README statements about unmeasured IDAC
+consequences and append a dated P35 closeout. Preserve the R10 lineage result,
+R11's tail-specific ordered attribution, its inconclusive whole-profile labels,
+and the tetraethylene-glycol exception. Record the P46a denominator of 142,
+including ten EG observations, rather than the superseded name-based count.
+The approximately 80 percent recovery refers to the O-to-U comparator MAE gap
+on inspected rows with original open solutes and the same P28 endpoint. The
+remaining C-to-U MAE difference is a conditional method-bundle contrast, not
+C's entire experimental error or a universal method-error estimate. Preserve
+all unfavorable rows and the retrospective scope.
+
+Close the present P35 explanatory campaign. This is a stopping decision, not
+acceptance of a liquid-conformer explanation. No most-extended, minimum-energy
+or ensemble recipe is adopted. The frozen 630 primary plus six S1/S2 profiles
+and all existing model defaults remain unchanged. P30/P32 failures, R11 labels,
+P46a and R8/R9's numerical-gradient closure are not rewritten.
+
+P50 is an E standard-library reporting check of public aggregates only. Require
+the exact Git blob c036e8e24aa45a03aed0485664b3a26cd842c17f for the archived
+R12 RESULTS.md. Check the published counts and independent rounding ranges,
+then reproduce explicitly labelled hypothetical portfolio-sizing arithmetic.
+Rounding ranges are not confidence intervals. This does not rerun the private
+P46 checker, score ThermoML, certify its row-level inputs, or create a new
+scientific gate. Read no private plan, geometry, surface file or profile.
+Do not fetch an alternative result when a hash mismatches. Write a fresh
+reporting output only; never overwrite a historical file. Repeating this
+zero-model integrity check is allowed and is not another scientific run.
+
+The cost scenarios allocate four or eight starts to each of 630 molecules for
+sizing. They do not claim that all 630 require that many starts or that the
+small-panel median is their mean runtime. A nominal single-point extrapolation
+excludes geometry search, thermal quantities and independent validation. A
+four-core worker-hour is wall time on four allocated cores, not a core-hour.
+Twenty-way division is an ideal capacity calculation, not a promised schedule
+or a claim of available free account quota. No scenario is an execution budget.
+
+The authorized new native/model budget is zero: no SCF, gradient, conformer
+proposal, optimization, molecular dynamics or activity-model request. There
+is no Actions dispatch or private-Mac scoring task. UD-derived data stays
+private on the Mac and is not copied by these helpers. The public summary
+check can run on any local machine because it reads only already published
+aggregate text. Code-only tests can run before the reporting record is adopted.
+
+A future geometry project would first need one fully specified physical rule,
+complete computational acceptance criteria and a genuinely unexposed validation
+source with an exposure/overlap audit. Water and branched polyols remain required
+controls; their already-inspected results do not become independent holdouts.
+No current test split is certified fresh by this record. Such a project needs
+its own prospective registration and budget. This closeout creates no automatic
+continuation or permission to select conformers from the R12 accuracy result.
```
<!-- END PATCH REG13 -->

Evidence and verification pointers

Repository references below are paths at `e2b36c8c5c2273f47ee6df21975b295b93689ca8`, unless explicitly historical. They can be resolved from the pinned base `https://github.com/Victor-Liang-ChE/zcosmo/blob/e2b36c8c5c2273f47ee6df21975b295b93689ca8/`. None requires a private coordinate file for this review.

[S1] `docs/astra/ROUND13_PROMPT.md`; `docs/astra/round12/ZCOSMO_ROUND12_REPORT.md`. The latter's Git blob is `6bcf6010beff2a83ce4c7328f06ce8864dd998e6`, matching the mounted report used to reconstruct its source patches.

[S2] `docs/astra/round12/RESULTS.md`, Git blob `c036e8e24aa45a03aed0485664b3a26cd842c17f`. This is the full public source read by P50, not a recreated table assembled from memory. Its 5,877 bytes were reconstructed from the connector content and verified against that blob before audit.

[S3] `PREREGISTRATION.md`, Git blob `5fcc3115389b85f0f8cab0b5156c09a6d89f1a92`, including the original split, R10-R12 records and P46a. The P46a amendment is commit `d6b7e25805f468e76fdc56c4185134f3e3bf5b7d`.

[S4] `docs/OPTIMIZATION_BRIEF.md`, Git blob `9042052e2c0884226db6f795d14f8ec8c0157bd4`. Its unchanged classification rules and resource description remain the review contract; its earliest progress counts are historical, not the present 630+6 status.

[S5] `docs/astra/round11/RESULTS.md`; `docs/astra/round11/ZCOSMO_ROUND11_REPORT.md`. The first supplies the 24-slot, 594-second measured run, the ordered attribution and its unchanged operational labels.

[S6] `docs/astra/round10/RESULTS.md`; `docs/astra/round10/PROVENANCE_STATUS.md`. These distinguish recovered raw-input lineage from verified electronic decks and from database-level empirical conformation revisions.

[S7] `docs/astra/round7/GLYCOL_STATUS.md`, current base blob `88b56ebefa5e2a414ed06e64266769a4a66d585b`; `README.md`, current base blob `8c934966e68104551659c91021128f0029901967`. P49 changes only the README closeout paragraphs and appends the dated P35 outcome.

[S8] `scripts/r5_conformers.py`, blob `e1989d5800f9f1c79f9c7573725313afe0b739b7`; `scripts/r5_common.py`, blob `f5d21bb018b69a7d6125380f1218b0991dd5bc50`; `scripts/r5_shape.py`, blob `1d539ee44b1e925d2e6cd4e821111b56ac173401`.

[S9] `docs/astra/round5/RESULTS.md`, blob `88d669c4c8abc6269e55f3609d7ff390e7f6fc5c`. It reports the incomplete P26 probe and explicitly records the decision not to continue the full protocol.

[S10] `scripts/r6_phase.py`; `scripts/r6_ensemble.py`; `docs/astra/round6/RESULTS.md`. The finite-basin implementation is a prospective model probe requiring missing thermal and basin information, not an accepted ensemble for the 630 profiles.

[S11] `src/zcosmo/conformers.py`, blob `dd0007c5d0048d58561f8b9d7ffaebec5dc424ae`; `src/zcosmo/pyscf_cosmo.py`, blob `0f72e5383898d9c2cff21f2692ec6330c22d7a7a`; `src/zcosmo/pyscf_cosmo_v2.py`, blob `80abbf28d915057e27dc1513a9b194e4e2d9f31f`.

[S12] `scripts/r12_analysis.py`, blob `4072a6c0850bb0d08ccc0d8208996c41b0a04119`; `scripts/r12_review.py`, blob `4419c0ccf71d0e4a345232120d0fdb7fcad6836a`; `scripts/r12_selftest.py`, blob `a1320bf60c03887c9337508c1092ac3b9d9e5b18`. These are the P46a-adjusted files, not the superseded report constants.

[U1] Pracht, Bohle and Grimme, “Automated exploration of the low-energy chemical space with fast quantum chemical methods,” PCCP 2020, DOI `10.1039/C9CP06869D`. Publisher abstract and article metadata verified at `https://pubs.rsc.org/en/content/articlelanding/2020/cp/c9cp06869d/unauth`. No run or accuracy number for this project is inferred from that paper.

[U2] CREST authors' conformational entropy documentation, `https://crest-lab.github.io/crest-docs/page/examples/entropy.html`, read during this review. Its thermal/reference and sampling requirements are cited as methodology, not as a tested Z-COSMO implementation.

[U3] SCM official multispecies COSMO-RS tutorial, `https://www.scm.com/doc/Tutorials/COSMO-RS/COSMO-RS_multispecies.html`, and species-distribution example, `https://www.scm.com/doc/COSMO-RS/Examples/Multispecies_distribution.html`. Their solvent/composition-dependent examples illustrate the distinction between a fixed histogram and equilibrated conformers. They are not part of the proposed free-compute stack.
