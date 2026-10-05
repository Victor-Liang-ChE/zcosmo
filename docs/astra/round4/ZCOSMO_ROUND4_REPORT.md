# Z-COSMO round 4: glycol solvents, screening-charge diagnostics, P18 deployment, and LLE quality

Reference: `Victor-Liang-ChE/zcosmo`, `main = 33ebac0146ae2df4dd73fcf8a431cb6d7033554b`, committed October 5, 2026, 12:47:34 UTC. This report follows `ROUND4_PROMPT.md`, the complete archived round-3 report, its measured results, and the October 5 registrations. The implementation patches add experimental helpers; they do not modify the production equations or automatically deploy a profile. [S1–S4]

The immediate action is the already accepted P18 metadata correction. The scientific priority is to distinguish a glycol conformer/exposure difference from a general screening-charge effect. **Do not neutralize every profile merely because its raw surface charge is negative.** That can remove a genuine feature of an uncorrected conductor calculation with electron density outside the cavity. The pinned PySCF COSMO exporter explicitly says that outlying-charge correction is not implemented. Separately, the LLE audit has established that some reported endpoint compositions lack the necessary numerical checks; their contribution must be made visible before another LLE score is presented. [S2, S3, S9, U1]

There is no new native molecular result in this report. Installation of `pyscf==2.14.0 pyberny==0.7.0` was attempted in the Python 3.13 runtime and failed at its package resolver. This does not establish that those releases are unavailable on the working Python 3.11 machines. I executed the portable tests, syntax and CLI checks, and new-file patch application checks against a reconstructed checkout containing the blob-verified round-3 helpers. I did not clone the full repository, run PySCF, inspect the Mac-only UD files, relabel the actual 636 profiles, repair the actual 2,255 LLE calls, or spend cloud credits. Native API use remains source-checked and conditional on the supplied execution gates.

## Ranked work and cost

| Priority | ID | Work | Class | Cost and expected saving | Effort |
|---:|---|---|:---:|---|---|
| 1 | P20 | Deploy and verify the accepted P18 correction | A, already accepted rule | Zero quantum calculations. Relabeling saves `N × t_SP` compared with regenerating N profiles; verification is evaluator time only. | Low |
| 2 | P23-account | Map the existing LLE sidecar back to rows and systems | E, observation only | Zero additional model evaluations. No prediction or denominator is changed. | Low |
| 3 | P21 | Inventory polyols/ethers; isolate solvent area, volume and profile shape | E inventory; A diagnostic substitutions | Zero quantum calculations. Nine evaluator corners per selected ordered pair, with temperature reuse inside each worker. | Moderate |
| 4 | P22 | Test raw charge and the glycol geometry/exposure mechanism | E diagnostics; A sensitivity arms | At most nine initial single points; extra fixed-density layer solves and volume quadratures on three molecules. No global profile rerun. | Moderate |
| 5 | P23-repair | Repair the frozen set of questionable LLE calls | A numerical correction | At most 4,000 new model calls per selected pair-temperature, plus one legacy replay. No quantum chemistry. | Moderate |
| Closed for this round | Chains | Continue trying to turn the six flagged geometries into Berny-converged profiles | No new protocol | Zero new optimization budget. Keep 630 primary profiles plus six explicitly flagged exploratory profiles. | None |
| Shared | H4 | Common helpers and portable tests | E instrumentation | Diagnostic overhead only. | Shared |

The brief's saving × probability / effort rule remains useful for throughput changes. Here the first two rows are accepted-correction and reporting prerequisites, rather than speculative speed-ups. For the discretionary work, no measured probability of finding the cause exists, so I do not manufacture numerical ROI scores. The order minimizes new quantum work: audit existing assets, run inexpensive counterfactuals, then spend the fixed nine-single-point budget. If those diagnostics falsify a proposed explanation, stop that line before launching a conformer or 636-profile campaign. Savings in this table overlap and should not be added.

## What the glycol result establishes

The denominator discrepancy is resolved: 0.839 belongs to 828 test observations; 0.800 belongs to the 762-observation common subset that also required the other named models. Fresh Z0x predictions reproduced stored predictions to `2.9e-10`. Neither number should now be replaced by the other without its denominator. [S2, S3]

For diethylene glycol (DEG), the rounded reported numbers alone give

\[
\frac{108}{828}(1.74-0.69)=0.13696.
\]

Thus DEG's solvent rows account for a contribution numerically equal to the overall +0.137 deficit. That does not mean every other contribution is zero: triethylene glycol (TEG) and ethylene glycol (EG) worsen the result, while other rows improve. The four-corner calculation likewise gives +0.236 from the solvent role and −0.099 from the solute role. Water as solvent improves. Another water-centered or global orientation campaign would therefore target the wrong dominant error. [S2]

| Derived from the rounded profile table | DEG | TEG | EG |
|---|---:|---:|---:|
| Loss of tail area, relative to UD | 27.1% | 34.0% | 30.3% |
| Loss of total OH + OT area | 22.3% | 27.9% | 24.2% |
| Decrease in cavity volume | 4.39% | 4.55% | 4.17% |
| Increase in area | 1.91% | 1.86% | 0.10% |

These quantities are calculated from `RESULTS.md`, not newly measured profiles. The polar deficit is considerably larger than the total-area difference. [S2]

A hydrocarbon solute has mostly near-zero-sigma surface. A solvent with a strongly polar and associating surface has favorable solvent–solvent contacts that must be displaced when such a solute is inserted. Weakening that solvent representation can lower the calculated insertion penalty. This is a plausible explanation for an underprediction of hydrocarbon ln gamma in glycols. **It is not a monotonic theorem about this implementation:** residual terms, pure-component reference terms, combinatorial terms and London dispersion all enter. The reported MAEs do not by themselves give the sign of every individual prediction change. P21 records signed changes as well as absolute-error contributions.

Volume is not a harmless cosmetic field. It affects the combinatorial contribution and the composition-weighted dielectric calculation. In the current London term, a spherical contact distance is proportional to `V^(1/3)`, so a pure self-contact energy magnitude scales as `V^-2`. The reported glycol volume reductions correspond to roughly 9–10% changes in that magnitude if C6 is held fixed. Cross-contact and pure-reference terms can cancel, so this is not a 9–10% prediction-error estimate. The stored dielectric and D4/C6 tables are kept fixed in the diagnostic, exactly as in the existing Z0x profile substitution. [S10]

The competing explanations make different observable predictions:

**Conformer/exposure.** An intramolecular O–H···O contact can reduce exposed donor or acceptor surface and change sigma amplitudes. Compare actual saved open and UD coordinates, O···O/H···O distances and D–H···A angles, then recompute the *same* open electronic method at both geometries. If atom-owned exposure and tails follow the geometry, conformer choice is implicated. A short contact is a geometric observation, not an H-bond free energy or proof that the isolated lowest-energy conformer describes the liquid.

**Classification/splitting.** Ordinary hydrogen bonding should not turn an ether oxygen into an OH oxygen in the existing classifier. It uses inferred covalent connectivity, with a 1.15 covalent-radius distance rule. An O–H covalent cutoff is about 1.12 Å, much shorter than a normal H-bond contact. Nevertheless, distorted coordinates or erroneous ownership could produce wrong tags, so P22 records every bond/tag. Final OH/OT area can also fall with completely unchanged tags: the split uses the sign of the *averaged* sigma, and the final `1-exp[-sigma²/(2·0.007²)]` factor transfers weakly polar area back to NHB. Report pre-redistribution and post-redistribution areas separately. [S7]

**Surface and radii.** With the same atom tags and geometry, different ownership/exposure near ether oxygens points toward the cavity construction, switching or electronic charge distribution. Recompute at the UD geometry before changing radii. A radius sweep is a sensitivity diagnostic, not permission to select the radius that gives a preferred IDAC value. The existing custom radii already bypass the default radius scale; changing `vdw_scale` alone is not a controlled radius experiment when `radii_table` is explicitly supplied. [S6, U2]

**General charge bias.** n-Nonane also has a substantial negative moment, so the charge observation is not specific to glycols. A global charge defect could interact particularly strongly with polar solvents, but that needs an actual calculation of its prediction effect. The two fixed projections in P22 provide that sensitivity without pretending to identify a physical correction.

The previous conformer experiment does not settle this question. Its committed summary assigns TEG's lowest member a weight of 0.9932558 among five members. DEG and EG are not listed in that 50-molecule summary. The earlier registration used a limited xTB-derived ensemble and SVP conformer profiles. It does not establish that conductor-relaxed TZVP glycol conformers have negligible profile variation. Reuse those assets as evidence; do not rerun the same broad ensemble and expect a different answer. [S11]

## P21: an experiment that separates those explanations

`scripts/r4_glycols.py inventory` selects all benchmark molecules with at least two structural OH groups or a non-carbonyl ether oxygen, plus the declared controls. It records class, flexibility, row counts in each role, UD/open descriptors and coordinate availability. Its `has_COOH` field allows carboxylic OH groups to be distinguished from alcohol-only polyols. This is a structural panel, not a list chosen from the largest errors. Missing coordinates do not silently remove profile or score rows.

The inventory reports every selected solvent, so the DEG/TEG/EG pattern can be compared with hydroxyethers, polyethers without OH, rigid monoethers and other polyols. Use the complete inventory, including compounds without scored IDAC rows. An unrepresented compound cannot supply a benchmark acceptance claim.

For the scored panel, the eight-factorial corners replace only solvent **A**, **V**, and normalized **153-bin shape**, keeping the solute open. A ninth control uses the full UD solvent. The eight corners use the same frozen Z0x constants and property tables. Each ordered pair/corner runs in a fresh process, avoiding the environment-dependent profile cache. The full descriptor-substitution corner must reproduce the full-UD-solvent control to `1e-10`; the Shapley contributions must sum to the complete prediction difference to `1e-10`. All finite masks must agree. These are attribution identities, not fitted coefficients or candidate production models. This factorial conditions on an open solute, so its total is not expected to equal the earlier +0.236 solvent Shapley attribution, which averaged over both solute-profile backgrounds. [S5, S10]

The native panel is deliberately small: the open and UD geometries of EG, DEG and TEG, plus open water, methanol and n-nonane. That is nine single points. Neither geometry optimization nor a new orientation is allowed in this first comparison. The two saved geometries can have different orientations, so their native difference includes the already measured quadrature sensitivity. A difference on the order of the orientation uncertainty is inconclusive evidence for a conformer mechanism; atom connectivity and contact distances provide orientation-independent checks. For each geometry, record atom-owned surface area and raw charge, then the averaged moment and tail area, then the HB redistribution. These stages localize where the polar area disappears.

No glycol profile fix is adopted by this report. A subsequent conformer correction must use a frozen, theory-only construction, a fixed conformer budget and independent validation molecules. Require every final geometry to meet the declared original confirmation test, identical finite coverage, and the preregistered compatibility check before one separately labelled experimental score is read. The historical 25/2,302 check can measure compatibility but cannot become a clean held-out discovery after these repeated analyses. A radius, averaging or charge change needs the same explicit separation. Selecting any of them by the DEG error would violate the project's rule.

## P22: why a neutral molecule can have negative raw screening charge

There are four different numbers to retain:

\[
Q_{\rm full}=\sum_{\text{all PCM points}}q_j,\quad
Q_{\rm kept}=\sum_{A_j>10^{-8}\,a_0^2}q_j,\quad
Q_{\rm avg}=\sum_j A_j\bar\sigma_j,\quad
M_{\rm bins}=\sum_{b,k}pA_{bk}\sigma_k.
\]

The last quantity has units of elementary charge for the stored area-bin convention. It is not automatically the physical net molecular charge or the raw PCM charge. Hsieh averaging is row-normalized, not constrained to preserve the area-weighted first moment. Linear binning and the final HB redistribution should preserve the *averaged* first moment, up to roundoff, while that moment can differ from `Q_kept`. The discarded tiny-area points may also contribute a difference between full and kept charge. P22 measures each difference rather than assigning them all to outlying charge. [S6, S7]

For C-PCM at fixed density,

\[
Kq=Rv,\qquad K=S,\qquad R=-f_\epsilon I,
\qquad f_\epsilon=(\epsilon-1)/\epsilon.
\]

At epsilon = 1e9, replacing `f` by 1 changes it by only `1e-9`; this cannot explain a roughly `0.03 e` effect. The residual of the linear solve, the overlap electron count `Tr(DS)`, and `q` versus `q_sym` should be checked first. P9 equivalence demonstrates equivalence of two implementations of these equations; it does not validate a missing outlying-charge correction. [U2, S3]

The usual statement that a neutral conductor calculation must have zero total induced surface charge assumes the solute charge is entirely inside the cavity. Gaussian orbital density is not compactly supported. In a continuum single-layer conductor problem, let `u(r)` be the capacitary potential: one on and inside the cavity, harmonic outside, tending to zero at infinity. Reciprocity gives

\[
Q_{\rm scr}=-f_\epsilon\int\rho(\mathbf r)u(\mathbf r)\,d\mathbf r.
\]

For a neutral source with all positive nuclei inside, this becomes

\[
Q_{\rm scr}=-f_\epsilon\int_{\rm outside}n(\mathbf r)[1-u(\mathbf r)]\,d\mathbf r.
\]

Thus a negative raw total can occur with exact arithmetic and an exactly neutral electronic system. It is a weighted electron-penetration quantity, **not simply minus the number of electrons outside**. This derivation concerns the uncorrected conductor boundary problem; it does not establish that the entire observed molecular value is physical rather than a finite-surface defect.

A useful exact counterexample is a point nucleus +Z and a normalized spherical Gaussian electron density, enclosed by a spherical cavity of radius a. With `t=sqrt(alpha)*a`,

\[
Q_{\rm scr}=-f_\epsilon Z\,\operatorname{erfc}(t),\qquad
N_{\rm outside}=Z\left[\operatorname{erfc}(t)+\frac{2t}{\sqrt\pi}e^{-t^2}\right].
\]

For the illustrative dimensionless choice `Z=f=1, t=1.5`, these are `−0.0338948535 e` and `0.2122902874 electrons`, respectively. I checked the first formula by independent one-dimensional quadrature to about `5e-17 e`. This is an analytic test source, not a fitted explanation of any molecule. A blanket zero-sum rule would fail this valid uncorrected-conductor example.

PySCF 2.14.0's COSMO export code explicitly returns zero outlying-charge correction and exports the same corrected and uncorrected charges. Q-Chem's documentation distinguishes the C-PCM matrix equation from the additional treatment of electronic density outside the cavity. Neither supports identifying an arbitrary zero-sum shift with a complete physical outlying-charge correction. [U1, U3]

### The discriminating test

The native sphere test uses PySCF's actual SWIG Gaussian surface at Lebedev orders 29, 41 and 59. Its analytic source is convolved with the same Gaussian test functions as the molecular potential integrals. It has a compact-density case (`t=6`) and a penetrating case (`t=1.5`). The first should approach zero, the second the nonzero analytic limit. Report all deviations rather than calling either finite mesh exact. A failure to approach the correct limits implicates the numerical surface/test setup, even though the source density is known exactly.

For real molecules, P22 then freezes the converged density and changes only the PCM layer. It measures orders 29/41/59 and one 1.10 radius scale. This distinguishes SCF-density changes from surface changes. A larger cavity reducing the negative charge is consistent with penetration, but is not sufficient evidence by itself because it also changes switching and surface discretization. Changing the orbital basis can change the density tail; the optional SVP calculation is a basis-only diagnostic with the profile grid and surface settings held fixed, not a second production protocol.

The stronger check uses the discrete capacitary layer. Set `c=K^(-T)1`, and evaluate its Gaussian Coulomb potential `u_h(r)`. Independent density quadrature reconstructs

\[
Q_{\rm scr}=-f_\epsilon\{\sum_A Z_Au_h(R_A)-\int n(r)u_h(r)dr\}.
\]

For a declared partition into the union of project-radius spheres and its outside, the same quantity decomposes as

\[
-f_\epsilon Q_{\rm mol}
+f_\epsilon\sum_A Z_A[1-u_h(R_A)]
-f_\epsilon\int_{\rm inside}n(1-u_h)
-f_\epsilon\int_{\rm outside}n(1-u_h).
\]

The nuclear and inside terms expose departures from the ideal constant interior potential. The outside term measures weighted penetration for that discrete layer. Since SWIG is smooth, the sharp sphere union is a diagnostic partition, not a unique definition of its boundary. The code reports it explicitly.

Use volume-grid levels 4 and 5. Do not interpret the partition unless the level-5 electron count and reconstructed total charge are within `1e-5 e`, and the inside/outside contributions agree between levels to `1e-4 e`. Failure is an inconclusive quadrature calculation, not permission to claim a numerical defect or penetration. A source-level C-PCM residual alone cannot substitute for this independent volume check.

### What a zero-sum correction would change

Multiplying all charges by a common factor cannot turn a nonzero sum into zero without multiplying them all by zero. That destroys the polar profile. Reject that proposal.

Two additive choices illustrate the nonuniqueness:

\[
q'_j=q_j-Q\frac{A_j}{A},\qquad
q'=q-Q\frac{K^{-1}1}{1^TK^{-1}1}.
\]

The first is a uniform sigma-density shift, not a uniform point-charge shift. The second is the stationary solution of a charge-constrained quadratic electrostatic problem when K is positive definite; it changes the boundary potential by a constant. It is a different boundary-value problem. Neither is automatically the outlying-charge correction required for compatible COSMO thermodynamics.

For `Q=−0.03 e`, the uniform shifts are approximately `+1.94e-4`, `+1.44e-4`, and `+3.03e-4 e/Å²` for DEG, TEG and EG. They strengthen some positive tails and weaken negative tails. They can change sign-based HB assignment and its final weighting, so the original averaging/splitting must be rerun from segments. Merely translating the already split bins is not equivalent. Whether those shifts recover 10–14 Å² of glycol tail area depends on where the segment distribution lies near the thresholds; the reported moments do not answer it.

There is also an exact diagnostic identity. Because the averaging rows sum to one, a uniform sigma shift passes unchanged through Hsieh averaging. Consequently, shifting raw charges to zero gives `Q_avg' = Q_avg − Q_raw` for the same retained segments, not necessarily zero. Simultaneously forcing both totals to zero would introduce another modification.

P22 therefore writes both projections only as explicitly unadopted A sensitivities. Their raw sums must be below `1e-10 e`. Record how they alter OH/OT area and ln gamma for glycols *and controls*. No projection is adopted because it improves IDAC. A physical correction would require a fixed theoretical construction, validation against appropriate corrected-charge calculations, and consistency of charges and electrostatic energy before experimental scoring. The smaller UD binned moments do not by themselves identify which correction, cavity convention or geometry produced them. Inspect the original UD COSMO files rather than infer their raw charges from a binned moment.

## P20: exact deployment of accepted P18

The helper prepares all 636 selected files into a separate bundle, verifies them, then applies them only through an explicit `apply` command. The original locations remain `profiles_v2`, `s2_stalled` and `s1_stalled`. It keeps MVLVMROFTA's S1 file and the other five S2 files. An S2 file is never copied into the primary set.

For each file, the entire byte sequence after its first newline must be identical. All metadata except `disp. flag` and three explicit P18 provenance fields is retained. This includes area, volume, dispersion energy, geometry status and existing revision fields. The existing geometry-based NIST classifier decides the flag. An unexpected change other than `HB-DONOR-ACCEPTOR → COOH` stops the deployment for investigation. It is not broadened into an unregistered general metadata cleanup.

Every generating geometry is hashed. The default is the profile's adjacent `.xyz.json`; a map is required where that is unavailable. Do not substitute a convenient old checkpoint for an S1/S2 profile's actual generating coordinates. The script prints missing geometry requirements and writes no bundle until all are resolved. It also checks profile/header identities and the exact 636-key manifest. [S5, S6]

`apply` first backs up every original, verifies the backups, and writes each replacement atomically. It records progress. A process kill can still interrupt a multi-file transaction; the independent `rollback` command restores all originals after verifying that no unrelated concurrent edit would be overwritten. Run it when no other job is writing profiles or scoring from the changing source directories. Actual deployment did not occur here.

**Scores affected.** Recompute open-profile COSMO-SAC-dsp IDAC, VLE and LLE predictions that involve a changed acid, plus derived solvent rankings and their scorecards. Preserve the old outputs. The profile-versus-UD acceptance statistic must be recorded under the corrected metadata, as already validated at 0.1362 on the calibration. Other model variants need inspection of `disp_mode` and `use_dsp`; do not assume all names beginning with Z use the same dispersion implementation.

**Scores invariant.** Z0x's London calculation never reads this flag; its IDAC, VLE, HE and LLE predictions are invariant when all other inputs and code are fixed. COSMO-SAC 2010 with dispersion disabled is likewise invariant. Stored predictions that use untouched UD profiles are unchanged. UNIFAC and HANNA do not acquire a new numerical result from relabeling open COSMO metadata. The fitted COSMO-SAC-dsp flag term itself has no temperature dependence, so its direct contribution to excess enthalpy is zero; a finite-difference HE implementation can show roundoff-level subtraction differences, not a physical HE correction. Verify these claims numerically where the corresponding files are used. [S10]

After deployment, use `ZC_R3_COOH_FLAG=1` for future explicitly requested profile generation. Do not invoke the full profile-generation job simply to refresh headers: changing that environment switch affects the code's revision fingerprint, and stale fingerprints can trigger unwanted quantum reruns. This metadata deployment deliberately retains historical provenance and bypasses `run_one`.

## The six chains: close this optimization campaign, preserve the flags

I would allocate **no new chain optimization in round 4**. P19 established that the tighter calculation can confirm already-converged calibration geometries at greater cost. It did not establish convergence of a stalled chain. Its registered cost gate failed, so treating it as accepted with a larger wall-time threshold after seeing the result would be incorrect. [S2, S3]

The earlier long-chain runs already cost roughly 1 h 45 min to 3 h 28 min per 50-evaluation pass on four-core runners. A 100-evaluation budget is therefore roughly 3.5–6.9 runner-hours before further setup and final profiling. Multiplying by the *calibration* ratio of 2.28 gives an illustrative 8–15.8 hours, not a measured prediction for these chains. Even the original 100-step budget was difficult to fit into a six-hour job. A tighter-SCF campaign with the same unsuccessful starting logic is poor use of this round's free compute. [S3]

This closes a bounded compute campaign, not the mathematical question of whether an optimizer could eventually converge. Keep the current 630 Berny-converged profiles as primary and the six S1/S2 profiles as a labelled exploratory extension. Their small checkpoint-to-checkpoint ln gamma changes do not certify a minimum or justify replacing the primary denominator. Do not change the Berny on-sphere rule, reclassify a Cartesian-gradient check as that rule, or promote the flags.

A future reopening needs a specific mechanism and a new prospective budget. Examples of qualifying evidence would be a reproducible energy/gradient inconsistency at one frozen stalled geometry, or a native test showing that a newly identified numerical defect is fixed. Neither has been established here. There is no additional chain patch or automatic optimization job in this report.

## P23: what the LLE failures mean, and a bounded treatment

The 223 failures are about **12.1% of 1,842 refined calls**, not 223 test observations and not necessarily 223 binaries. The 158 negative margins can overlap those calls, and some negative values may be smaller than a meaningful numerical tolerance. The five fallbacks are another call category. The sidecar must be joined back to the 6,581 original rows and the requested split before any change to reported test statistics is calculated. The old per-system rule is a majority of row-level detections, so even one failed pair-temperature can affect several rows and a system vote. [S2, S9]

A chemical-potential residual of 0.005 is roughly 12.4 J/mol at 298 K in one component. It says the reported compositions have not solved the coexistence equations at the intended precision. It does not by itself prove that the binary is miscible or that its detection indicator must flip. Near a critical point, a small residual can coexist with a large endpoint error.

A negative tangent margin beyond tolerance means that the proposed common plane lies above the evaluated free energy at at least one sampled composition. This invalidates that sampled global-stability check. It can indicate a metastable solution, a poorly refined root, or a numerical inconsistency in the quantities used. A margin of `−1e-14` is not treated like `−1e-3`. Z0x also retains one-sided finite differences near pure ends; the reporting should not silently assume that all near-endpoint numerical quantities have exact thermodynamic derivatives. [S9, S10]

A coarse lower-hull chord can witness nonconvexity even when the nonlinear endpoint solver fails. Conversely, absence of a gap on an 81-point grid is not a proof of miscibility. Keep separate labels for a checked endpoint pair, a nonconvexity witness with unknown endpoints, an operational no-gap result on a stated grid, and an unresolved evaluation.

P23-account reads the existing P14 records. It checks their ordered pair, rounded temperature and returned endpoints against each prediction row. It requires residual `<1e-7` and a present sampled margin `≥−1e-7` for the legacy root-quality pass. Failures, unchecked margins and hull fallbacks become **nullable diagnostic outcomes**, while the old prediction columns remain untouched. The old 2 K temperature rounding remains, so this audit does not also introduce a temperature-model change.

The summary retains every row and system. It reports the result of assigning unresolved votes zero and one under the original aggregation rule. These are **bounds for the finite-grid quality screen, not rigorous thermodynamic bounds**, because the retained grid-based no-gap classifications are also numerical. Composition MAE is labelled with the number of checked endpoint rows that contribute. Do not pass the nullable column through `astype(bool)` or the old `lle_rows` helper; NaN must not become a positive or negative prediction by accident. Balanced accuracy requires the separately frozen negative set; the positive LLE table alone provides a detection rate, not specificity.

The optional P23-repair patch uses bounded least squares without clipping compositions inside the equations. It examines all sampled hull gaps, up to four, on nested 81/161/321 interior grids with fixed logarithmic tails. It rejects tiny trivial gaps, enforces the same residual and tangent thresholds, and requires agreement of the last two root sets within `5e-5`. Each pair-temperature has a 4,000-new-model-call ceiling. Exhaustion is recorded, not retried indefinitely. This is an A numerical correction, with a separate sidecar and prospective registration, not an E-equivalence claim against known questionable endpoints.

A three-point witness with a positive chord defect above `1e-7` can retain gap existence when endpoints remain unchecked. The script exposes this as `gap_witness_only`; endpoint MAE is unavailable. Floating-point function values are still not an interval certificate, and no global-completeness claim is made. Model failure, incomplete sampling or unaccepted roots otherwise leave the call unresolved.

The portable implementation recovered the regular-solution chi=3 endpoints `0.07072018168` and `0.92927981832` in 379 model calls, with residual `5.69e-16`. Ideal-mixture grid checks used 349 calls. A deliberately failed endpoint solver retained only a nonconvexity witness; a one-call budget returned unresolved. These are synthetic tests, not a forecast for water-containing Z0x systems.

If every distinct questionable call were different, `223+158+5=386` is an upper counting estimate before accounting for overlap and unchecked margins. At 4,000 calls each that would be 1,544,000 new activity-coefficient evaluations, plus legacy replays. Measure a fixed small batch before assigning a runner budget; do not label this a guaranteed minutes-long repair. The code records per-call work and walls. Keep rejected repairs, and report the denominator unchanged even if no call can be repaired.

## Exact setup, execution and acceptance commands

The helpers rely on the existing `scripts/r3_*.py` on the pinned main. H4 and P20–P23 install together without changing production defaults. All new outputs go under `$WORK`. Run the native generation jobs on the established free CPU environments; run every UD-backed evaluator check on the Mac. The portable tests require NumPy, SciPy, pandas and RDKit, with no PySCF.

The following creates a worktree from an existing populated checkout. Shared data/results are input assets. The one exception is the separately invoked P20 `apply`, which explicitly writes the original profile files after verification and backup. Do not run that command concurrently with a profile writer.

```bash
set -euo pipefail
export REPO="$PWD"
export BASE=33ebac0146ae2df4dd73fcf8a431cb6d7033554b
export REPORT="${REPORT:-$REPO/ZCOSMO_ROUND4_REPORT.md}"
export WORK="$(mktemp -d "${TMPDIR:-/tmp}/zcosmo-r4.XXXXXX")"
export TREE="$WORK/tree" PATCHES="$WORK/patches"
mkdir -p "$PATCHES"
python - "$REPORT" "$PATCHES" <<'PY'
from pathlib import Path
import re,sys
items=re.findall(r'<!-- PATCH:(H4|P20|P21|P22|P23|REG4) -->\s*```diff\n(.*?)\n```',Path(sys.argv[1]).read_text(),re.S)
assert len(items)==6 and len({name for name,_ in items})==6
for name,diff in items: Path(sys.argv[2],name+'.patch').write_text(diff+'\n')
PY
git -C "$REPO" worktree add --detach "$TREE" "$BASE"
for asset in data results; do
  test -d "$REPO/$asset"
  if test -e "$TREE/$asset"; then mv "$TREE/$asset" "$TREE/$asset.pinned-copy"; fi
  ln -s "$REPO/$asset" "$TREE/$asset"
done
for id in H4 P20 P21 P22 P23 REG4; do
  git -C "$TREE" apply --check "$PATCHES/$id.patch"
  git -C "$TREE" apply "$PATCHES/$id.patch"
done
cd "$TREE"
export PYTHONPATH=src OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export ZC_PCM3C=1 QC_MEM_MB=6000 MPLBACKEND=Agg
# Keep the existing profile protocol fixed during diagnostics. P18 deployment is metadata-only.
unset ZC_R3_COOH_FLAG ZC_BERNY_NOISE_EH ZC_SIGMA_OVERRIDE_DIR ZC_ONLY_KEYS
python -m pip freeze > "$WORK/environment.txt"
python -m py_compile scripts/r4_*.py
python scripts/r3_selftest.py --out "$WORK/r3-portable.json"
python scripts/r4_selftest.py --out "$WORK/r4-portable.json"
```

Before native work, verify the environment rather than quietly installing newer packages into a working production environment:

```bash
python - <<'PY'
from importlib.metadata import version
assert version('pyscf')=='2.14.0'
assert version('pyberny')=='0.7.0'
print('pyscf',version('pyscf'),'pyberny',version('pyberny'))
PY
```

For new P21/P22 sensitivities and P23 repair, adopt the proposed registration text before inspecting their outputs. It is a separate file so the report cannot falsely date an entry in `PREREGISTRATION.md`. The actual timestamp and experiment commit must be recorded by the maintainer. P18 already has its accepted registration; its deployment receipt is an execution record, not a new fit.

```bash
cat docs/astra/round4/REGISTRATION_PROPOSED.md >> PREREGISTRATION.md
git add PREREGISTRATION.md docs/astra/round4 scripts/r4_*.py
git commit -m "Register fixed round-4 diagnostics and LLE repair protocol"
export REG="$(git rev-parse HEAD)"
```

Do not stage or commit the shared asset symlink substitutions. The above explicit `git add` paths avoid them.

### P20 preparation and verification, on the Mac

Set `GEOMETRY_MAP` to a JSON mapping of keys to the actual saved geometry paths wherever an adjacent `.xyz.json` is missing. A missing map is allowed initially: the command lists exactly what is missing and stops without changing source profiles.

```bash
P18_ARGS=()
if test -n "${GEOMETRY_MAP:-}"; then P18_ARGS+=(--geometry-map "$GEOMETRY_MAP"); fi
python scripts/r4_metadata.py prepare --root "$REPO/data/pyscf_sigma" \
  --compounds "$REPO/data/benchmark/compounds.csv" "${P18_ARGS[@]}" \
  --out "$WORK/p18-bundle"
python scripts/r4_metadata.py verify --bundle "$WORK/p18-bundle"
python scripts/r4_metadata.py overlay --bundle "$WORK/p18-bundle" --out "$WORK/p18-corrected"
# A frozen original view must contain copies, not links that would change during apply.
python - "$WORK/p18-bundle" "$WORK/p18-original" "$WORK/gate-geometries" <<'PY'
from pathlib import Path
import json,shutil,sys
sys.path.insert(0,'scripts')
from r4_common import geometry
m=json.loads((Path(sys.argv[1])/'manifest.json').read_text())
p=Path(sys.argv[2]);g=Path(sys.argv[3]);p.mkdir();g.mkdir()
for r in m['profiles']:
    shutil.copy2(r['source'],p/(r['key']+'.sigma'))
    # The selected generating geometry is frozen independently of output metadata.
    sym,x=geometry(r['geometry'])
    (g/(r['key']+'.xyz.json')).write_text(json.dumps(dict(sym=sym,x=x.tolist(),
        source=r['geometry'],source_sha256=r['geometry_sha256'])))
assert len(list(p.glob('*.sigma')))==636
PY
python scripts/r3_orientation.py freeze --work "$WORK/p18-gate" \
  --geometry-dir "$WORK/gate-geometries" --registration P18-9d32e9e-accepted-613dd8f
for set in original corrected; do
  python scripts/r3_orientation.py score --work "$WORK/p18-gate" \
    --profile-set "$WORK/p18-$set" --out "$WORK/p18-gate-$set"
done
python scripts/r3_orientation.py score --work "$WORK/p18-gate" \
  --profile-set UD --out "$WORK/p18-gate-UD"
python - "$WORK" <<'PY'
from pathlib import Path
import json,sys,numpy as np,pandas as pd
w=Path(sys.argv[1]);m=json.loads((w/'p18-bundle/manifest.json').read_text())
changed={r['key'] for r in m['profiles'] if r['old_flag']!=r['new_flag']}
r=pd.read_csv(w/'p18-gate-original/values.csv').set_index('query')
c=pd.read_csv(w/'p18-gate-corrected/values.csv').set_index('query').loc[r.index]
u=pd.read_csv(w/'p18-gate-UD/values.csv').set_index('query').loc[r.index]
assert len(r)==2302 and r.key.nunique()==25 and r.index.is_unique
report={'keys':25,'rows':2302,'changed_flags':sorted(changed)}
for model in ['cosmosac_dsp','Z0x']:
    x=r[model].to_numpy(float);y=c[model].to_numpy(float);ok=np.isfinite(x)
    assert np.array_equal(ok,np.isfinite(y)) and ok.any()
    delta=abs(y-x)
    invariant=ok if model=='Z0x' else ok & ~r.key.isin(changed).to_numpy()
    assert invariant.any() and delta[invariant].max()<1e-10
    report[model]={'finite':int(ok.sum()),'max_change':float(delta[ok].max())}
ok=np.isfinite(c.cosmosac_dsp)&np.isfinite(u.cosmosac_dsp)
assert ok.any()
median=float(abs(c.loc[ok,'cosmosac_dsp']-u.loc[ok,'cosmosac_dsp']).median())
assert median<.15
report['median_vs_UD']=median
(w/'p18-gate.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
PY
```

The gate command exports coordinate JSONs from the declared generating geometries and records their original source hashes. It also handles a declared `.cosmo` geometry through the existing parser. This export does not replace or modify the original geometry in the deployment manifest.

Verify full-data invariance before deployment. These commands use the two frozen 636-file views and separate output directories/processes:

```bash
for set in original corrected; do
  for model in Z0x cosmosac2010 cosmosac_dsp; do
    ZC_SIGMA_OVERRIDE_DIR="$WORK/p18-$set" ZC_PRED="$WORK/p18-pred-$set" \
      python -m zcosmo.evaluate "$model" --tables idac --split all
  done
done
for model in Z0x cosmosac2010; do
  python scripts/r3_idac.py compare-fresh \
    --reference "$WORK/p18-pred-original/${model}__idac__all.csv" \
    --candidate "$WORK/p18-pred-corrected/${model}__idac__all.csv" \
    --tol 1e-10 --out "$WORK/p18-${model}-invariance.json"
done
python scripts/r3_idac.py audit \
  --reference "$WORK/p18-pred-original/cosmosac_dsp__idac__all.csv" \
  --candidate "$WORK/p18-pred-corrected/cosmosac_dsp__idac__all.csv" \
  --split test --out "$WORK/p18-dsp-change"
```

Only after those checks, deploy explicitly and record the receipt:

```bash
python scripts/r4_metadata.py apply --bundle "$WORK/p18-bundle" --backup "$WORK/p18-backup"
# Needed only for a deliberate rollback:
# python scripts/r4_metadata.py rollback --backup "$WORK/p18-backup"

# Recompute affected open-profile predictions in a new directory, never overwrite historical results.
ZC_SIGMA_OVERRIDE_DIR="$WORK/p18-corrected" ZC_PRED="$WORK/p18-dsp-predictions" \
  python -m zcosmo.evaluate cosmosac_dsp --tables idac,vle,he,lle --split all
```

Append the actual transaction manifest/hash and invariant-check results to `PREREGISTRATION.md` after execution, including the changed-key list. That list cannot be truthfully supplied here because the production/flagged profile files are not present in this runtime. Preserve both full-coverage and chain-excluded row manifests when producing scorecards. A 630-profile override directory by itself does **not** exclude the six chains: missing overrides can fall back to UD. Exclude their rows explicitly rather than relying on a missing file.

### P21 inventory and descriptor factorial

Use the original P16 `paired_rows.csv` to diagnose the already reported deficit. Its path is a local result artifact, not a guessed tracked repository path.

```bash
: "${P16_PAIRED_ROWS:?Set this to the frozen round-3 P16 paired_rows.csv}"
python scripts/r4_glycols.py inventory \
  --open-profiles "$WORK/p18-original" --paired-rows "$P16_PAIRED_ROWS" \
  --geometry-dir "$WORK/gate-geometries" --out "$WORK/polyol-ether-inventory"
python scripts/r4_glycols.py factorial \
  --paired-rows "$P16_PAIRED_ROWS" --keys "$WORK/polyol-ether-inventory/keys.txt" \
  --open-profiles "$WORK/p18-original" --registration "$REG" --out "$WORK/AVP"
```

This factorial is slower than a single evaluation because it intentionally uses isolated workers. Its cost is approximately `9 × number_of_ordered_pairs × (import/startup + evaluations_at_that_pair's_T)`. Do not translate that into a quantum speed-up. Accept the diagnostic only if the full-corner and Shapley identities and the complete finite-mask check pass. It writes unavailable observations and exits 2 on incomplete attribution.

The following freezes the nine native cases by chemical structure rather than guessing InChIKeys. It fails on missing UD/open geometry instead of switching conformers silently.

```bash
python - "$WORK/polyol-ether-inventory" "$WORK/native-cases.json" <<'PY'
from pathlib import Path
from rdkit import Chem
import pandas as pd,json,sys
root=Path(sys.argv[1]);d=pd.read_csv('data/benchmark/compounds.csv')
canon=lambda s:Chem.MolToSmiles(Chem.MolFromSmiles(s))
d['canonical']=d.smiles.map(canon)
cases=[]
for smi,sources in [('OCCO',['open','UD']),('OCCOCCO',['open','UD']),
                    ('OCCOCCOCCO',['open','UD']),('O',['open']),
                    ('CO',['open']),('CCCCCCCCC',['open'])]:
    k=d.loc[d.canonical==canon(smi),'inchikey'].tolist()
    assert len(k)==1,(smi,k)
    for source in sources:
        p=(root/'geometries'/f'{k[0]}.{source}.json').resolve()
        assert p.is_file(),str(p)
        cases.append(dict(key=k[0],source=source,smiles=smi,geometry=str(p)))
assert len(cases)==9
Path(sys.argv[2]).write_text(json.dumps(cases,indent=2))
PY
```

### P22 native generation, on free CPU machines

Portable algebra can run immediately. The native sphere test must run in the actual pinned PySCF environment:

```bash
python scripts/r4_charge.py analytic --out "$WORK/analytic-sphere.json"
python scripts/r4_charge.py sphere-native --out "$WORK/native-sphere.json"
```

The fixed nine-case run below uses the same machine sequentially by default, with one five-hour deadline per case. For runner distribution, dispatch those exact case records without modifying their source geometries or settings. Transfer the frozen coordinate JSONs as job inputs; they are sufficient for generation and do not require UD on the runner. UD is needed later for backed comparisons.

```bash
python - "$WORK/native-cases.json" "$WORK/charge" "$REG" <<'PY'
from pathlib import Path
import json,subprocess,sys
cases=json.loads(Path(sys.argv[1]).read_text());root=Path(sys.argv[2]);root.mkdir()
results=[]
for r in cases:
    tag=r['key']+'.'+r['source'];out=root/tag
    cmd=[sys.executable,'scripts/r4_charge.py','molecule','--geometry',r['geometry'],
         '--key',r['key'],'--out',str(out),'--registration',sys.argv[3],
         '--memory','6000','--projections']
    if r['source']=='open' and r['smiles'] in ['O','OCCOCCO','CCCCCCCCC']:
        cmd+=['--sweep','--quadrature']
    with (root/(tag+'.log')).open('w') as log:
        try:
            p=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,timeout=18000)
            status='complete' if p.returncode==0 else ('quadrature_inconclusive' if p.returncode==2 else 'failed')
        except subprocess.TimeoutExpired:
            status='deadline';p=None
    results.append(dict(**r,status=status,returncode=p.returncode if p else None))
    (root/'jobs.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
if any(r['status']!='complete' for r in results):raise SystemExit(2)
PY
```

A deadline or native failure is an incomplete experiment, not a successful negative finding. A quadrature failure does not authorize increasing levels until a desired partition appears. Record the failed preset and register any extension separately. The maximum nine-job deadline allocation is 45 runner-hours, a ceiling rather than a runtime prediction. The fixed-density solves can consume considerable memory at order 59; stop and report an allocation failure instead of silently reducing the mesh in one arm.

The charge report saves experimental baseline and projected profiles. Compare the *same generating geometry* in each arm. To evaluate a small diagnostic profile replacement, the existing R3 `worker` can target a key in its 25-key manifest. TEG is in that historical fixture; DEG and EG must not be silently omitted because they are outside the 25-key list. For DEG and the complete native panel, use a fresh `zcosmo.evaluate` process per frozen overlay and then the identity-aware `r3_idac.py` audit. The following creates panel overlays on the full open background without changing unrelated files:

```bash
python - "$WORK/native-cases.json" "$WORK/charge" "$WORK/p18-original" "$WORK/charge-views" <<'PY'
from pathlib import Path
import json,sys
cases=json.loads(Path(sys.argv[1]).read_text());raw=Path(sys.argv[2]);bg=Path(sys.argv[3]).resolve();out=Path(sys.argv[4]);out.mkdir()
for arm in ['baseline','UD_geometry','area_zero','capacitary_zero']:
    dest=out/arm;dest.mkdir()
    selected={r['key']:r for r in cases if r['source']=='open'}
    has_ud={r['key'] for r in cases if r['source']=='UD'}
    for f in sorted(bg.glob('*.sigma')):
        source=f
        if f.stem in selected:
            kind='UD' if arm=='UD_geometry' and f.stem in has_ud else 'open'
            source=raw/(f.stem+'.'+kind)
            if arm in ('area_zero','capacitary_zero'): source=source/arm
            source=source/f.name
        assert source.is_file(),str(source)
        (dest/f.name).symlink_to(source.resolve())
    assert len(list(dest.glob('*.sigma')))==636
PY
for arm in baseline UD_geometry area_zero capacitary_zero; do
  ZC_SIGMA_OVERRIDE_DIR="$WORK/charge-views/$arm" ZC_PRED="$WORK/charge-pred-$arm" \
    python -m zcosmo.evaluate Z0x --tables idac --split all
done
for arm in UD_geometry area_zero capacitary_zero; do
  python scripts/r3_idac.py audit \
    --reference "$WORK/charge-pred-baseline/Z0x__idac__all.csv" \
    --candidate "$WORK/charge-pred-$arm/Z0x__idac__all.csv" \
    --split all --out "$WORK/charge-effect-$arm"
done
```

Require identical identities and finite masks before interpreting an effect:

```bash
python - "$WORK" <<'PY'
from pathlib import Path
import sys,json,pandas as pd,numpy as np
sys.path.insert(0,'scripts')
from r3_common import keyed
w=Path(sys.argv[1]);r=keyed(pd.read_csv(w/'charge-pred-baseline/Z0x__idac__all.csv'))
x=r.pred_ln_gamma_inf.to_numpy(float);mask=np.isfinite(x);assert mask.any()
checks=[]
for arm in ['UD_geometry','area_zero','capacitary_zero']:
    q=keyed(pd.read_csv(w/f'charge-pred-{arm}/Z0x__idac__all.csv'))
    assert set(q.index)==set(r.index)
    y=q.loc[r.index,'pred_ln_gamma_inf'].to_numpy(float)
    assert np.array_equal(mask,np.isfinite(y)),arm
    checks.append(dict(arm=arm,rows=len(r),finite=int(mask.sum()),max_change=float(abs(y[mask]-x[mask]).max())))
(w/'charge-coverage.json').write_text(json.dumps(checks,indent=2))
print(json.dumps(checks,indent=2))
PY
```

Inspect the inventory's solvent-role rows and the controls, not only the aggregate MAE. Repeat with `cosmosac_dsp` only as a separately labelled evaluator sensitivity; do not confuse a changed dispersion flag with a changed charge. The `UD_geometry` arm uses the open quantum method at the saved UD glycol geometries, not UD surface charges. Label its orientation confounding as described above. All diagnostic profiles remain excluded from every production score and profile directory.

### P23 accounting and repair, on the Mac for the UD-based Z0x reference

The existing P14 JSONL sidecar and the matching predictions are experiment artifacts. Main still contains the original `evaluate.binodal`; the sidecar was measured in an experimental arm. These helpers do not assume P14 was merged.

```bash
: "${P14_SIDECARS:?Set this to the existing P14 JSONL file or directory}"
: "${P14_PREDICTIONS:?Set this to the matching Z0x__lle__all.csv}"
python scripts/r4_lle.py audit --sidecars "$P14_SIDECARS" \
  --predictions "$P14_PREDICTIONS" --model Z0x --split all --out "$WORK/lle-all"
python scripts/r4_lle.py audit --sidecars "$P14_SIDECARS" \
  --predictions "$P14_PREDICTIONS" --model Z0x --split test --out "$WORK/lle-test"
```

No new model call occurs in accounting. The exact old endpoint and indicator checks guard against mixing a sidecar with different profile sources or a different run. Review the test summary, the number of unchecked tangent margins, and the overlap of failure types before quoting revised statistics. The actual count changes cannot be computed from the aggregate numbers in `RESULTS.md` alone.

The repair gate first uses 20 deterministically selected previously good calls. Selection uses diagnostic validity, not experimental agreement:

```bash
python - "$P14_SIDECARS" "$WORK/lle-control.csv" <<'PY'
import sys,pandas as pd
sys.path.insert(0,'scripts')
from r4_lle import load_records,quality
records,_=load_records(sys.argv[1])
keys=[k for k in sorted(records) if k[0]=='Z0x' and quality(records[k])[0]==1.][:20]
assert len(keys)==20
pd.DataFrame([dict(model=k[0],c1=k[1],c2=k[2],binodal_T=k[3]) for k in keys]).to_csv(sys.argv[2],index=False)
PY
python scripts/r4_lle.py repair --sidecars "$P14_SIDECARS" \
  --calls "$WORK/lle-control.csv" --registration "$REG" --out "$WORK/lle-control.jsonl"
python - "$P14_SIDECARS" "$WORK/lle-control.jsonl" <<'PY'
import sys,numpy as np
sys.path.insert(0,'scripts')
from r4_lle import load_records
old,_=load_records(sys.argv[1]);new,_=load_records(sys.argv[2]);assert len(new)==20
for k,r in new.items():
    assert r['status']=='root_passes_refined_sampled_checks',(k,r['status'])
    b=max(r['roots'],key=lambda q:q['x'][1]-q['x'][0])
    assert b['residual']<1e-7 and b['sampled_tangent_margin']>=-1e-7
    assert np.max(abs(np.asarray(b['x'])-old[k]['returned']))<1e-4,k
print('20-call control gate passed')
PY
# Only after the control gate passes:
python scripts/r4_lle.py repair --sidecars "$P14_SIDECARS" \
  --calls "$WORK/lle-all/unresolved_calls.csv" --registration "$REG" \
  --out "$WORK/lle-repairs.jsonl"
python scripts/r4_lle.py audit --sidecars "$P14_SIDECARS" --repairs "$WORK/lle-repairs.jsonl" \
  --predictions "$P14_PREDICTIONS" --model Z0x --split test --out "$WORK/lle-test-repaired"
```

With a different open-profile background, pass that exact full directory using `--background`; the legacy replay must then reproduce its matching sidecar. Never use an open background with the stored UD sidecar merely because both are called Z0x. Every repair records profile hashes and the model/property source hashes. A changed finite-grid detection is a reported numerical correction, not proof that a previously reported experimental binary was actually miscible.

## Execution record and remaining limits

The portable test log records a 636-file synthetic P18 prepare/verify/apply/rollback round trip with byte-identical originals restored, unchanged raw rows and S1/S2 labels, and rejection of a tampered candidate. The geometry classifier was stubbed for that transaction test; it does not replace the real NIST parser acceptance gate. The native charge script reconstructs parser inputs and requires its traced bins to match the ordinary `to_profiles` output within `1e-10` before interpreting atom-level results.

The three-factor Shapley identity test had maximum discrepancy `8.88e-16`; the two raw charge projections satisfied their sums within `8.88e-16`. Independent Gaussian-sphere quadrature reproduced the analytic screening charge. LLE ideal/regular-solution, failed-refinement, exhausted-budget, and row-accounting tests passed. The existing R3 portable suite also passed, including identity-aware reordered-row checks. No native time or actual profile difference is inferred from those tests.

The new-file patches below were checked independently after their common helper dependency, and together. All added Python compiled. The full physical acceptance remains conditional: real classifier/metadata verification, the Mac-only 25/2,302 comparison, the nine molecular single points, the density partitions, and the actual LLE replay/repair were not executed. P18 remains accepted by the maintainer's recorded rule; this report provides a deployment transaction and checks without claiming that deployment has occurred.

## Sources inspected

[S1] `docs/astra/ROUND4_PROMPT.md`, blob `c7415ed0d43fd0754b55f8f792c829f2ddc1c483`, at the pinned reference.

[S2] `docs/astra/round3/RESULTS.md`, blob `c6de1f0a15d47cd596c56f5de00928f2a3238b1d`. All reported molecular timings and measured round-3 outcomes in this report are attributed to this record, not new executions here.

[S3] `PREREGISTRATION.md`, blob `c700606d2fc806cb25bab99824e5461a38e8c9cb`, including the earlier chain runs and the October 5 R3 registration/results. The P18 acceptance and P19 rejection are preserved.

[S4] `docs/OPTIMIZATION_BRIEF.md`; archived `docs/astra/round3/ZCOSMO_ROUND3_REPORT.md`, blob `da7bb899b9bff933ee69031e897575cfd6ff85fb`. The locally available archived report matches that Git blob.

[S5] All current `scripts/r3_*.py`, including `r3_common.py` (`bdddba8b5d5587891d945db585413c63371fa050`), `r3_metadata.py` (`a2cb3a167384b604c7be1134bfaa9e0ec76edf5d`), `r3_hybrid.py` (`752ee647f319f2f571c502b0ead4b82fd172c164`), `r3_precision.py` (`6fcdfeb94e75a0a1fbc85bdb31728e42757a62e4`), and the orientation, IDAC, gate and self-test helpers. These supply the existing frozen-row and separate-process interfaces.

[S6] `src/zcosmo/pyscf_cosmo.py`, blob `0f72e5383898d9c2cff21f2692ec6330c22d7a7a`; `pyscf_cosmo_v2.py`; merged `pcm_lu.py`. P18 remains opt-in in the fetched source.

[S7] `data/raw/nist/to_sigma.py`, blob `9f2e0d6f3bb4da4880f9bd6ad702847f9308ed1d`: geometry parsing, inferred bonds, Hsieh averaging, sign-based split, linear binning and HB redistribution.

[S9] `src/zcosmo/evaluate.py`, blob `e154f0d9e695957a66c600e8211a0d0bca010c8c`; `metrics.py`; archived round-2 P14 diff. P14's observational patch is not in the fetched production evaluator.

[S10] `src/zcosmo/z0x.py`, `cosmosac.py`, `models.py`, and `results/z_params/Z0.json`: London dispersion, profile-volume dependence, endpoint differentiation and the fitted dispersion flag path.

[S11] `data/pyscf_sigma/conformer_summary.csv`, blob `978a84ddf6ef1e3efb68ac1805b169df352dcb39`, together with the conformer registration in [S3].

[U1] Pinned PySCF source: `pyscf/pyscf`, tag `v2.14.0`, `pyscf/solvent/cosmors.py`, especially `get_pcm_parameters` and `write_cosmo_file`. The explicit outlying-charge TODO is in this pinned source, not an assumption about a future release.

[U2] Pinned PySCF `v2.14.0`, `pyscf/solvent/pcm.py`, `pyscf/dft/LebedevGrid.py`, density-grid and numerical-integration interfaces. The SWIG surface contains Gaussian charge exponents and switching-weighted areas; changing order changes more than an abstract histogram resolution.

[U3] Q-Chem 7.0 manual, section 11.2.3, “Polarizable Continuum Models,” conductor-like models and outlying-charge discussion. Used for the distinction between the conductor matrix problem and additional electronic-penetration treatment, not as evidence that PySCF applies such a correction.

## Unified diffs

All six blocks are extractable with the setup command. They add new paths relative to the pinned main and depend only on the inspected existing R3 helpers and normal project dependencies. They do not edit `PREREGISTRATION.md` automatically and do not submit a GitHub workflow.


<!-- PATCH:H4 -->
```diff
--- /dev/null
+++ b/scripts/r4_common.py
@@ -0,0 +1,148 @@
+"""Round-4 diagnostic helpers. No production defaults are changed."""
+from __future__ import annotations
+import importlib
+import json
+from pathlib import Path
+import sys
+import numpy as np
+import pandas as pd
+from scipy.spatial.distance import cdist
+from r3_common import digest, read_sigma, write_json, STALL_KEYS
+
+BASE = '33ebac0146ae2df4dd73fcf8a431cb6d7033554b'
+S1_KEY = 'MVLVMROFTAUDAG-UHFFFAOYSA-N'
+
+
+def parser_module():
+    sys.path.insert(0, str(Path('data/raw/nist').resolve()))
+    return importlib.import_module('to_sigma')
+
+
+def geometry(path):
+    """Read actual saved coordinates. Never substitute a new conformer for missing bytes."""
+    path = Path(path)
+    if path.suffix == '.cosmo':
+        d = parser_module().get_atom_DataFrame(path.read_text())
+        sym = list(d['atom'])
+        x = d[['x / A', 'y / A', 'z / A']].to_numpy(float)
+    else:
+        d = json.loads(path.read_text()); sym = list(d['sym']); x = np.asarray(d['x'], float)
+    if x.shape != (len(sym), 3) or not len(sym) or not np.isfinite(x).all():
+        raise ValueError(f'invalid geometry: {path}')
+    return sym, x
+
+
+def geometry_parser(sym, x):
+    ts = parser_module()
+    p = ts.Dmol3COSMOParser.__new__(ts.Dmol3COSMOParser)
+    p.df_atom = pd.DataFrame({'atom': sym})
+    p.dist_mat_atom = cdist(x, x)
+    p.is_water = sym.count('H') == 2 and sym.count('O') == 1 and len(sym) == 3
+    p.disp = p.get_dispersive_values()
+    return p
+
+
+def flag_for_geometry(sym, x):
+    p = geometry_parser(sym, x)
+    return 'H2O' if p.is_water else ('COOH' if p.disp.has_COOH else p.disp.dispersion_flag)
+
+
+def structure(smiles):
+    from rdkit import Chem
+    from rdkit.Chem import rdMolDescriptors
+    m = Chem.MolFromSmiles(smiles)
+    if m is None: raise ValueError(f'invalid SMILES {smiles}')
+    oh = len(m.GetSubstructMatches(Chem.MolFromSmarts('[OX2H1]')))
+    ether = len(m.GetSubstructMatches(Chem.MolFromSmarts('[#6;!$(C=O)][OX2][#6;!$(C=O)]')))
+    acid = m.HasSubstructMatch(Chem.MolFromSmarts('[CX3](=O)[OX2H1]'))
+    # Structural strata, not labels chosen after looking at errors.
+    if oh >= 2 and ether: group = 'polyol_with_ether'
+    elif oh >= 2: group = 'polyol_without_ether'
+    elif oh == 1 and ether: group = 'hydroxyether'
+    elif not oh and ether >= 2: group = 'polyether_no_OH'
+    elif not oh and ether: group = 'monoether_no_OH'
+    elif oh == 1: group = 'single_OH'
+    else: group = 'other'
+    return dict(group=group, OH_count=oh, ether_count=ether, has_COOH=bool(acid),
+                rotatable_bonds=int(rdMolDescriptors.CalcNumRotatableBonds(m)),
+                rings=int(rdMolDescriptors.CalcNumRings(m)), heavy_atoms=m.GetNumHeavyAtoms())
+
+
+def contacts(sym, x):
+    """Geometric contacts only; these are not an H-bond energy or a basin assignment."""
+    p = geometry_parser(sym, x)
+    classes = p.get_HB_classes_per_atom()
+    bonds = [p.get_bonds(i) for i in range(len(sym))]
+    rows = []
+    for donor, element in enumerate(sym):
+        if element not in ('O', 'N'): continue
+        for h, hsym in bonds[donor]:
+            if hsym != 'H': continue
+            for acc, asym in enumerate(sym):
+                if asym not in ('O', 'N') or acc == donor: continue
+                if acc in [j for j, _ in bonds[h]]: continue
+                a, b = x[donor] - x[h], x[acc] - x[h]
+                denom = np.linalg.norm(a) * np.linalg.norm(b)
+                if denom == 0: raise ValueError('coincident atoms')
+                angle = np.degrees(np.arccos(np.clip(a @ b / denom, -1., 1.)))
+                da, ha = np.linalg.norm(x[donor]-x[acc]), np.linalg.norm(b)
+                rows.append(dict(donor=donor, H=h, acceptor=acc, acceptor_class=classes[acc],
+                    DA_A=float(da), HA_A=float(ha), DHA_deg=float(angle),
+                    contact=bool(da <= 3.2 and ha <= 2.5 and angle >= 120.)))
+    return dict(atoms=[dict(i=i,element=sym[i],hb_class=classes[i],
+                            bonds=[j for j,_ in bonds[i]]) for i in range(len(sym))],
+                contacts=rows)
+
+
+def parser_trace(sym, x, seg):
+    """Reconstruct the exact registered parser inputs, retaining intermediate arrays."""
+    from zcosmo.pyscf_cosmo import BOHR, cavity_volume
+    p = geometry_parser(sym, x)
+    n = len(seg['q'])
+    p.df = pd.DataFrame({'n': np.arange(1,n+1), 'atom': seg['atom']+1,
+        'x / a.u.':seg['xyz'][:,0], 'y / a.u.':seg['xyz'][:,1], 'z / a.u.':seg['xyz'][:,2],
+        'charge / e':seg['q'], 'area / A^2':seg['area']})
+    for j, f in enumerate('xyz'):
+        p.df[f+' / A'] = seg['xyz'][:,j]*BOHR
+        p.df_atom[f+' / A'] = x[:,j]
+    p.area_A2 = float(seg['area'].sum()); p.volume_A3 = cavity_volume(seg,x/BOHR)
+    p.num_profiles=3; p.averaging='Hsieh'
+    p.df['rn / A'] = np.sqrt(seg['area']/np.pi)
+    p.df['rn^2 / A^2'] = p.df['rn / A']**2
+    p.sigma=seg['q']/seg['area']; p.rn2=p.df['rn^2 / A^2'].to_numpy()
+    p.dist_mat_squared=cdist(seg['xyz']*BOHR,seg['xyz']*BOHR)**2
+    p.df_atom['hb_class']=p.get_HB_classes_per_atom(); p.df_atom['Nbonds']=p.disp.Nbonds
+    p.sigma_averaged=p.average_sigmas(p.sigma)
+    p.sigma_nhb,p.sigma_OH,p.sigma_OT=p.split_profiles(p.sigma_averaged,3)
+    out=p.get_outputs()
+    atom=[]
+    for i, element in enumerate(sym):
+        use=seg['atom']==i; area=seg['area'][use]; raw=p.sigma[use]; av=p.sigma_averaged[use]
+        atom.append(dict(i=i,element=element,hb_class=str(p.df_atom.hb_class.iloc[i]),
+            area_A2=float(area.sum()),raw_q_e=float(seg['q'][use].sum()),
+            averaged_moment_e=float((area*av).sum()),
+            positive_tail_A2=float(area[av>=.01].sum()),negative_tail_A2=float(area[av<=-.01].sum())))
+    bins=np.stack([out.psigmaA_nhb,out.psigmaA_OH,out.psigmaA_OT])
+    return p, out, dict(raw_kept_q_e=float(seg['q'].sum()),
+        averaged_moment_e=float((seg['area']*p.sigma_averaged).sum()),
+        binned_moment_e=float((bins*out.sigmas).sum()),atom=atom,
+        pre_HB_area_A2={k:float(v[:,1].sum()) for k,v in
+                       [('NHB',p.sigma_nhb),('OH',p.sigma_OH),('OT',p.sigma_OT)]},
+        post_HB_area_A2=dict(zip(('NHB','OH','OT'),map(float,bins.sum(1)))))
+
+
+def selected_profiles(root, compounds):
+    """Select exactly the registered 630+5+1 collection, not all files in a directory."""
+    root=Path(root).resolve(); rows=[]
+    keys=list(compounds.inchikey)
+    if len(keys)!=636 or len(set(keys))!=636: raise ValueError('expected frozen 636 benchmark compounds')
+    for key in keys:
+        folder='s1_stalled' if key==S1_KEY else ('s2_stalled' if key in STALL_KEYS else 'profiles_v2')
+        src=root/folder/f'{key}.sigma'
+        if not src.is_file(): raise FileNotFoundError(src)
+        _,_,meta=read_sigma(src)
+        if meta.get('standard_INCHIKEY', key) != key: raise ValueError(f'profile key mismatch: {src}')
+        if folder!='profiles_v2' and meta.get('geometry_converged')!=('S1' if folder=='s1_stalled' else 'S2'):
+            raise ValueError(f'flagged status mismatch: {src}')
+        rows.append((key,folder,src))
+    return rows
--- /dev/null
+++ b/scripts/r4_selftest.py
@@ -0,0 +1,138 @@
+"""Portable round-4 regression tests. Native PySCF and real profiles are separate gates."""
+from __future__ import annotations
+import argparse
+from contextlib import redirect_stdout
+import io
+import json
+from pathlib import Path
+import tempfile
+from types import SimpleNamespace
+from unittest.mock import patch
+import numpy as np
+import pandas as pd
+from scipy.integrate import quad
+from scipy.optimize import brentq
+from r3_common import STALL_KEYS,write_json,write_sigma,digest
+import r4_charge as ch
+import r4_common as cm
+import r4_glycols as gl
+import r4_lle as lle
+import r4_metadata as md
+
+
+def algebra():
+    t=1.5
+    sphere=ch.gaussian_sphere(t)
+    density=lambda r:4/np.sqrt(np.pi)*r*r*np.exp(-r*r)
+    inside=quad(density,0,t,epsabs=1e-13)[0]
+    weighted_out=quad(lambda r:density(r)*t/r,t,np.inf,epsabs=1e-13)[0]
+    q=-(1-inside-weighted_out)
+    assert abs(q-sphere['screening_charge_e'])<1e-13
+    assert abs(quad(density,t,np.inf)[0]-sphere['electrons_outside'])<1e-13
+    rng=np.random.default_rng(4);a=rng.normal(size=(19,19));K=a@a.T+np.eye(19)
+    q=rng.normal(size=19);area=rng.uniform(.1,2,19)
+    qa,qc,c=ch.project(q,area,K)
+    assert max(abs(qa.sum()),abs(qc.sum()))<1e-12
+    assert np.ptp((qa-q)/area)<1e-12
+    assert np.ptp(K@(qc-q))<1e-11
+    vals={format(i,'03b'):rng.normal(size=100) for i in range(8)}
+    error=float(abs(gl.shapley_three(vals).sum(0)-(vals['111']-vals['000'])).max())
+    assert error<1e-12
+    # Row normalization preserves constants, not the area-weighted sigma moment.
+    M=np.array([[1.,2.],[3.,1.] ]);B=M/M.sum(1)[:,None]
+    weights=np.array([1.,2.]);sig=np.array([.01,-.005])
+    assert abs(weights@sig)<1e-15 and abs(weights@(B@sig))>1e-3
+    expected={'OCCO':('polyol_without_ether',2,0),
+              'OCCOCCO':('polyol_with_ether',2,1),
+              'OCCOCCOCCO':('polyol_with_ether',2,2),
+              'COCCOC':('polyether_no_OH',0,2)}
+    for smiles,(group,oh,ether) in expected.items():
+        s=cm.structure(smiles);assert (s['group'],s['OH_count'],s['ether_count'])==(group,oh,ether)
+    return dict(gaussian_sphere=sphere,quadrature_charge_e=q if np.ndim(q)==0 else -(1-inside-weighted_out),
+                shapley_max_error=error,projection_max_sum=float(max(abs(qa.sum()),abs(qc.sum()))))
+
+
+class Regular:
+    def __init__(self,chi):self.chi=chi
+    def lngamma(self,T,x):return self.chi*np.array([x[1]**2,x[0]**2])
+
+
+def lle_tests(tmp):
+    ideal=lle.strict_binodal(Regular(0),298.15)
+    assert ideal['status']=='no_gap_on_refined_grid' and not ideal['globally_certified']
+    reg=lle.strict_binodal(Regular(3),298.15)
+    assert reg['status']=='root_passes_refined_sampled_checks'
+    root=brentq(lambda x:np.log(x/(1-x))+3*(1-2*x),.001,.49,xtol=1e-14)
+    assert np.max(abs(np.array(reg['roots'][0]['x'])-[root,1-root]))<1e-10
+    def bad(fun,x0,**kw):return SimpleNamespace(x=np.asarray(x0),success=False)
+    with patch.object(lle,'least_squares',bad):
+        witness=lle.strict_binodal(Regular(3),298.15)
+    assert witness['status']=='gap_witness_only' and witness['nonconvex_witness']['depth']>0
+    exhausted=lle.strict_binodal(Regular(3),298.15,budget=1)
+    assert exhausted['status']=='unresolved' and exhausted['model_calls']==1
+    b=lle.bounds([1,np.nan,0],['a','a','b'])
+    assert b['rows']==3 and b['unresolved_rows']==1 and b['system_gap_found_bounds']==[0.,.5]
+    sidecars=[];rows=[]
+    for j,(status,ends,res,margin) in enumerate([
+          ('refined_root',[.1,.9],1e-10,0.),('refined_root',[.1,.9],.005,-.001),('no_gap_on_grid',None,None,None)]):
+        sidecars.append(dict(model='Z0x',c1=f'A{j}',c2='B',binodal_T=298.,status=status,
+                             returned=ends,residual_max=res,sampled_tangent_margin=margin))
+        rows.append(dict(c1=f'A{j}',c2='B',T=298.15,split='test_one',x1=.12,
+                         pred_split=ends is not None,pred_x1_I=ends[0] if ends else np.nan,
+                         pred_x1_II=ends[1] if ends else np.nan))
+    sp=tmp/'sidecar.jsonl';sp.write_text(''.join(json.dumps(r)+'\n' for r in sidecars))
+    pp=tmp/'pred.csv';pd.DataFrame(rows).to_csv(pp,index=False);original=digest(pp)
+    lle.audit(SimpleNamespace(sidecars=str(sp),predictions=str(pp),repairs=None,split='test',model='Z0x',out=str(tmp/'audit')))
+    got=pd.read_csv(tmp/'audit/quality_rows.csv');assert got.r4_split.isna().sum()==1 and len(got)==3
+    assert digest(pp)==original
+    return dict(regular_roots=reg['roots'],regular_model_calls=reg['model_calls'],
+                ideal_model_calls=ideal['model_calls'],bad_refinement_status=witness['status'],
+                exhausted_status=exhausted['status'],audit_rows=len(got),unknown_rows=1)
+
+
+def metadata_tests(tmp):
+    root=tmp/'assets';keys=[f'SYNTH{i:04d}' for i in range(630)]+list(STALL_KEYS)
+    compounds=pd.DataFrame(dict(inchikey=keys,smiles=['CC(=O)O']*636));cp=tmp/'compounds.csv';compounds.to_csv(cp,index=False)
+    source_hashes={}
+    for k in keys:
+        folder='s1_stalled' if k==cm.S1_KEY else ('s2_stalled' if k in STALL_KEYS else 'profiles_v2')
+        dest=root/folder/f'{k}.sigma';dest.parent.mkdir(parents=True,exist_ok=True)
+        p=np.zeros((3,51));p[0,25]=10
+        meta={'volume [A^3]':12.,'disp. flag':'HB-DONOR-ACCEPTOR','geometry_converged':True if folder=='profiles_v2' else ('S1' if folder=='s1_stalled' else 'S2'),
+              'standard_INCHIKEY':k}
+        write_sigma(dest,np.linspace(-.025,.025,51),p,meta)
+        write_json(dest.with_suffix('.xyz.json'),dict(sym=['O','H'],x=[[0.,0.,0.],[0.,0.,1.]]))
+        source_hashes[str(dest)]=digest(dest)
+    # Only the native geometry classifier is stubbed. Exercise real 636-file I/O,
+    # byte identity, manifest verification, backup, explicit apply and rollback.
+    parser=tmp/'parser.py';parser.write_text('portable classifier fixture\n')
+    real_digest=md.digest
+    def mapped_digest(p):return real_digest(parser if str(p)=='data/raw/nist/to_sigma.py' else p)
+    with patch.object(md,'flag_for_geometry',return_value='COOH'),patch.object(md,'digest',mapped_digest),redirect_stdout(io.StringIO()):
+        bundle=tmp/'bundle';backup=tmp/'backup'
+        md.prepare(SimpleNamespace(root=str(root),compounds=str(cp),geometry_map=None,out=str(bundle)))
+        manifest=md.verify_bundle(bundle,require_original=True)
+        for r in manifest['profiles']:
+            src=Path(r['source']);cand=bundle/r['relative']
+            assert src.read_bytes().partition(b'\n')[2]==cand.read_bytes().partition(b'\n')[2]
+            before=json.loads(src.read_text().splitlines()[0][8:]);after=json.loads(cand.read_text().splitlines()[0][8:])
+            assert before['geometry_converged']==after['geometry_converged']
+        md.apply(SimpleNamespace(bundle=str(bundle),backup=str(backup)))
+        assert all(digest(r['source'])==r['candidate_sha256'] for r in manifest['profiles'])
+        md.rollback(SimpleNamespace(backup=str(backup)))
+        assert all(digest(p)==h for p,h in source_hashes.items())
+        suspect=bundle/manifest['profiles'][0]['relative'];suspect.write_bytes(suspect.read_bytes()+b'\n')
+        try:md.verify_bundle(bundle,require_original=True)
+        except ValueError:pass
+        else:raise AssertionError('tampered candidate accepted')
+    return dict(profiles=636,round_trip='byte-identical originals',raw_rows='byte-identical',
+                S1_S2_flags='preserved',tamper='rejected',classifier='stub, not a native parser gate')
+
+
+def main():
+    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args()
+    with tempfile.TemporaryDirectory(prefix='r4-selftest-') as td:
+        tmp=Path(td);result=dict(algebra=algebra(),lle=lle_tests(tmp),metadata=metadata_tests(tmp))
+    result['native_pyscf_tested']=False
+    write_json(a.out,result);print(json.dumps(result,indent=2))
+if __name__=='__main__':main()
```

<!-- PATCH:P20 -->
```diff
--- /dev/null
+++ b/scripts/r4_metadata.py
@@ -0,0 +1,173 @@
+"""Deploy the accepted P18 correction with an auditable, metadata-only transaction.
+
+prepare never changes source files. apply is explicit and backs up all originals.
+A killed process can leave a partial application; rollback restores the complete bundle.
+"""
+from __future__ import annotations
+import argparse
+import hashlib
+import json
+import os
+from pathlib import Path
+import shutil
+import tempfile
+import numpy as np
+import pandas as pd
+from r3_common import digest, read_sigma, write_json
+from r4_common import BASE, geometry, flag_for_geometry, selected_profiles
+
+RULE='P18: registration 9d32e9e; acceptance recorded in 613dd8f, 2026-10-05'
+PROVENANCE={'p18_rule','p18_parent_sha256','p18_geometry_sha256'}
+
+
+def relabel_bytes(raw, flag, geometry_hash):
+    head, sep, body=raw.partition(b'\n')
+    if not sep or not head.startswith(b'# meta: '): raise ValueError('invalid sigma header')
+    old=json.loads(head[8:]); new=dict(old)
+    new.update({'disp. flag':flag,'p18_rule':RULE,
+        'p18_parent_sha256':hashlib.sha256(raw).hexdigest(),'p18_geometry_sha256':geometry_hash})
+    result=b'# meta: '+json.dumps(new,allow_nan=False).encode()+b'\n'+body
+    if result.partition(b'\n')[2]!=body: raise AssertionError('raw rows or comments changed')
+    for k in set(old)|set(new):
+        if k not in PROVENANCE|{'disp. flag'} and old.get(k)!=new.get(k):
+            raise AssertionError(f'unrelated metadata changed: {k}')
+    return result
+
+
+def prepare(a):
+    out=Path(a.out).resolve()
+    if out.exists(): raise FileExistsError(out)
+    root=Path(a.root).resolve(); compounds=pd.read_csv(a.compounds)
+    sources=selected_profiles(root,compounds)
+    gm=json.loads(Path(a.geometry_map).read_text()) if a.geometry_map else {}
+    unknown=set(gm)-set(compounds.inchikey)
+    if unknown: raise ValueError(f'geometry map has unknown keys: {sorted(unknown)}')
+    staged=[]; missing=[]
+    for key,folder,src in sources:
+        gp=Path(gm[key]).resolve() if key in gm else src.with_suffix('.xyz.json')
+        if not gp.is_file(): missing.append(dict(key=key,profile=str(src),needed_geometry=str(gp))); continue
+        sym,x=geometry(gp); flag=flag_for_geometry(sym,x)
+        raw=src.read_bytes(); new=relabel_bytes(raw,flag,digest(gp))
+        old=json.loads(raw.partition(b'\n')[0][8:])
+        if old.get('disp. flag') != flag and not (old.get('disp. flag') == 'HB-DONOR-ACCEPTOR' and flag == 'COOH'):
+            raise ValueError(f'unexpected non-P18 relabel for {key}; investigate geometry/provenance before deployment')
+        staged.append((dict(key=key,folder=folder,source=str(src),geometry=str(gp),
+            source_sha256=digest(src),geometry_sha256=digest(gp),old_flag=old.get('disp. flag'),new_flag=flag,
+            candidate_sha256=hashlib.sha256(new).hexdigest(),
+            raw_body_sha256=hashlib.sha256(raw.partition(b'\n')[2]).hexdigest(),
+            relative=f'{folder}/{key}.sigma'),new))
+    if missing:
+        print(json.dumps({'missing_geometry':missing,'action':'Supply actual profile-generating coordinates in --geometry-map. No substitution of an old checkpoint.'},indent=2))
+        raise SystemExit(2)
+    if len(staged)!=636: raise ValueError('incomplete plan')
+    out.parent.mkdir(parents=True,exist_ok=True)
+    tmp=Path(tempfile.mkdtemp(prefix='p18-stage-',dir=out.parent))
+    try:
+        for r,new in staged:
+            p=tmp/r['relative'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(new)
+        write_json(tmp/'manifest.json',dict(base=BASE,rule=RULE,root=str(root),
+            compounds_sha256=digest(a.compounds),parser_sha256=digest('data/raw/nist/to_sigma.py'),
+            profiles=[r for r,_ in staged]))
+        tmp.rename(out)
+    except BaseException:
+        shutil.rmtree(tmp,ignore_errors=True);raise
+    verify_bundle(out,require_original=True)
+    print(json.dumps({'profiles':636,'changed_flags':[r for r,_ in staged if r['old_flag']!=r['new_flag']],
+                      'bundle':str(out)},indent=2))
+
+
+def verify_bundle(bundle,require_original=False):
+    bundle=Path(bundle).resolve(); m=json.loads((bundle/'manifest.json').read_text())
+    if len(m['profiles'])!=636 or len({r['key'] for r in m['profiles']})!=636:
+        raise ValueError('incomplete manifest')
+    if digest('data/raw/nist/to_sigma.py')!=m['parser_sha256']: raise ValueError('parser changed')
+    for r in m['profiles']:
+        cp=bundle/r['relative']; raw=cp.read_bytes()
+        if digest(cp)!=r['candidate_sha256']: raise ValueError(f'candidate changed: {cp}')
+        if hashlib.sha256(raw.partition(b'\n')[2]).hexdigest()!=r['raw_body_sha256']:
+            raise ValueError('raw sigma rows changed')
+        if digest(r['geometry'])!=r['geometry_sha256']: raise ValueError('geometry changed')
+        sym,x=geometry(r['geometry'])
+        if flag_for_geometry(sym,x)!=r['new_flag']: raise ValueError('parser flag mismatch')
+        if require_original and digest(r['source'])!=r['source_sha256']:
+            raise ValueError(f'source changed: {r["source"]}')
+        read_sigma(cp)
+    return m
+
+
+def atomic_bytes(path,raw):
+    path=Path(path)
+    fd,name=tempfile.mkstemp(prefix=path.name+'.p18-',dir=path.parent)
+    try:
+        with os.fdopen(fd,'wb') as f:
+            f.write(raw);f.flush();os.fsync(f.fileno())
+        os.replace(name,path)
+    finally:
+        if os.path.exists(name): os.unlink(name)
+
+
+def apply(a):
+    bundle=Path(a.bundle).resolve(); m=verify_bundle(bundle,require_original=True)
+    backup=Path(a.backup).resolve()
+    if backup.exists(): raise FileExistsError(backup)
+    backup.mkdir(parents=True)
+    for r in m['profiles']:
+        p=backup/r['relative'];p.parent.mkdir(parents=True,exist_ok=True)
+        shutil.copy2(r['source'],p)
+        if digest(p)!=r['source_sha256']: raise ValueError('backup hash failed')
+    write_json(backup/'transaction.json',dict(bundle=str(bundle),manifest=m,status='backed_up',applied=[]))
+    done=[]
+    try:
+        for r in m['profiles']:
+            if digest(r['source'])!=r['source_sha256']: raise ValueError('concurrent modification')
+            atomic_bytes(r['source'],(bundle/r['relative']).read_bytes());done.append(r['key'])
+            write_json(backup/'transaction.json',dict(bundle=str(bundle),manifest=m,status='applying',applied=done))
+        for r in m['profiles']:
+            if digest(r['source'])!=r['candidate_sha256']: raise ValueError('deployed hash failed')
+        write_json(backup/'transaction.json',dict(bundle=str(bundle),manifest=m,status='applied',applied=done))
+    except BaseException:
+        for r in m['profiles']:
+            if digest(r['source']) in (r['source_sha256'],r['candidate_sha256']):
+                atomic_bytes(r['source'],(backup/r['relative']).read_bytes())
+        write_json(backup/'transaction.json',dict(bundle=str(bundle),manifest=m,status='failed_check_rollback',applied=done))
+        raise
+    print('Applied metadata-only P18 to 636 profiles; append the transaction hashes to PREREGISTRATION.md.')
+
+
+def rollback(a):
+    backup=Path(a.backup).resolve(); t=json.loads((backup/'transaction.json').read_text());m=t['manifest']
+    for r in m['profiles']:
+        if digest(backup/r['relative'])!=r['source_sha256']: raise ValueError('backup changed')
+        if digest(r['source']) not in (r['source_sha256'],r['candidate_sha256']):
+            raise ValueError(f'concurrent modification, refuse rollback: {r["source"]}')
+    for r in m['profiles']: atomic_bytes(r['source'],(backup/r['relative']).read_bytes())
+    t['status']='rolled_back';write_json(backup/'transaction.json',t)
+
+
+def overlay(a):
+    """Read-only unified view for scoring. Keeps the primary/flagged distinction in the bundle."""
+    b=Path(a.bundle).resolve();m=verify_bundle(b)
+    out=Path(a.out).resolve()
+    if out.exists(): raise FileExistsError(out)
+    out.mkdir(parents=True)
+    for r in m['profiles']:
+        if a.exclude_flagged and r['folder']!='profiles_v2': continue
+        (out/f'{r["key"]}.sigma').symlink_to(b/r['relative'])
+    write_json(out/'provenance.json',dict(bundle=str(b),exclude_flagged=a.exclude_flagged,
+        manifest_sha256=digest(b/'manifest.json')))
+
+
+def main():
+    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
+    q=s.add_parser('prepare');q.add_argument('--root',default='data/pyscf_sigma')
+    q.add_argument('--compounds',default='data/benchmark/compounds.csv');q.add_argument('--geometry-map')
+    q.add_argument('--out',required=True)
+    q=s.add_parser('verify');q.add_argument('--bundle',required=True)
+    q=s.add_parser('apply');q.add_argument('--bundle',required=True);q.add_argument('--backup',required=True)
+    q=s.add_parser('rollback');q.add_argument('--backup',required=True)
+    q=s.add_parser('overlay');q.add_argument('--bundle',required=True);q.add_argument('--out',required=True)
+    q.add_argument('--exclude-flagged',action='store_true')
+    a=p.parse_args()
+    if a.cmd=='verify': verify_bundle(a.bundle,require_original=True);print('P18 bundle verified')
+    else: globals()[a.cmd](a)
+if __name__=='__main__':main()
```

<!-- PATCH:P21 -->
```diff
--- /dev/null
+++ b/scripts/r4_glycols.py
@@ -0,0 +1,176 @@
+"""Glycol/polyol/ether inventory and diagnostic A,V,profile-shape factorial.
+
+The eight corners are sensitivity probes, not deployable or selected models.
+Every model evaluation uses a fresh worker and fixed dielectric/C6 input tables.
+"""
+from __future__ import annotations
+import argparse
+import itertools
+import json
+import math
+import os
+from pathlib import Path
+import subprocess
+import sys
+import tempfile
+import numpy as np
+import pandas as pd
+from r3_common import digest,read_sigma,write_sigma,write_json,profile_descriptors,WATER
+from r4_common import structure,geometry,contacts
+
+CONTROL_SMILES={'O','CO','CCCCO','CCCCCCCCC'}
+
+
+def inventory(a):
+    os.environ.pop('ZC_SIGMA_OVERRIDE_DIR',None)
+    from zcosmo.cosmosac import sigma_path,SIGMA_DIR
+    if not SIGMA_DIR.is_dir(): raise FileNotFoundError('Run UD-backed inventory on the asset-bearing Mac')
+    compounds=pd.read_csv(a.compounds)
+    idac=pd.read_csv(a.idac)
+    paired=pd.read_csv(a.paired_rows) if a.paired_rows else None
+    gm=json.loads(Path(a.geometry_map).read_text()) if a.geometry_map else {}
+    out=Path(a.out);out.mkdir(parents=True,exist_ok=True);rows=[];geo=[]
+    for r in compounds.itertuples():
+        d=structure(r.smiles)
+        selected=d['OH_count']>=2 or d['ether_count']>0 or r.smiles in CONTROL_SMILES
+        if not selected: continue
+        k=r.inchikey; op=Path(a.open_profiles)/f'{k}.sigma'; up=sigma_path(k)
+        record=dict(key=k,smiles=r.smiles,**d,
+            solute_rows=int((idac.solute==k).sum()),solvent_rows=int((idac.solvent==k).sum()))
+        for tag,p in [('open',op),('UD',up)]:
+            if p is None or not Path(p).is_file():
+                record[tag+'_available']=False;continue
+            record[tag+'_available']=True
+            record.update({tag+'_'+f:v for f,v in profile_descriptors(p).items()})
+        if paired is not None:
+            for role in ('solute','solvent'):
+                sub=paired[paired[role]==k]
+                record[role+'_scored_rows']=len(sub)
+                if len(sub):
+                    er=sub['ref']-sub.ln_gamma_inf; ec=sub.candidate-sub.ln_gamma_inf
+                    record[role+'_signed_delta_prediction']=float((ec-er).mean())
+                    record[role+'_delta_MAE_contribution']=float((abs(ec)-abs(er)).sum()/len(paired))
+        rows.append(record)
+        gp=Path(gm[k]) if k in gm else Path(a.geometry_dir)/f'{k}.xyz.json'
+        # Missing geometries are visible. They do not silently cause profile/score rows to disappear.
+        for tag,p in [('open',gp),('UD',Path(a.ud_cosmo)/(up.stem+'.cosmo') if up else None)]:
+            item=dict(key=k,source=tag,path=str(p) if p else None,available=p is not None and p.is_file())
+            if item['available']:
+                sym,x=geometry(p);item.update(sha256=digest(p),**contacts(sym,x))
+                write_json(out/'geometries'/f'{k}.{tag}.json',dict(sym=sym,x=x.tolist(),
+                    source=str(p.resolve()),source_sha256=digest(p)))
+            geo.append(item)
+    if not rows: raise ValueError('empty structural panel')
+    d=pd.DataFrame(rows);d.to_csv(out/'inventory.csv',index=False)
+    (out/'keys.txt').write_text('\n'.join(d.key)+'\n')
+    write_json(out/'geometries.json',geo)
+    write_json(out/'inputs.json',dict(compounds=digest(a.compounds),idac=digest(a.idac),
+        paired_rows=digest(a.paired_rows) if a.paired_rows else None,
+        open_profiles=str(Path(a.open_profiles).resolve()),selected=len(d),
+        note='All structural strata selected before prediction inspection; missing assets are explicit.'))
+
+
+def shapley_three(values):
+    """Exact three-factor Shapley identity for arrays at all eight corners."""
+    out=[]
+    for j in range(3):
+        total=np.zeros_like(np.asarray(values['000'],float))
+        others=[i for i in range(3) if i!=j]
+        for subset in itertools.chain.from_iterable(itertools.combinations(others,n) for n in range(3)):
+            bits=['0']*3
+            for i in subset: bits[i]='1'
+            before=''.join(bits);bits[j]='1';after=''.join(bits)
+            w=math.factorial(len(subset))*math.factorial(2-len(subset))/6
+            total+=w*(values[after]-values[before])
+        out.append(total)
+    return np.asarray(out)
+
+
+def worker(a):
+    os.environ.pop('ZC_SIGMA_OVERRIDE_DIR',None)
+    from zcosmo.cosmosac import sigma_path,SIGMA_DIR
+    if not SIGMA_DIR.is_dir(): raise FileNotFoundError('UD profiles unavailable')
+    rows=pd.read_csv(a.rows); pair=rows[['solute','solvent']].drop_duplicates()
+    if len(pair)!=1: raise ValueError('one ordered pair per worker')
+    solute,solvent=pair.iloc[0].tolist()
+    if solute==solvent: raise ValueError('self pair is not a solvent substitution')
+    op=Path(a.open_profiles)/f'{solvent}.sigma'; up=sigma_path(solvent)
+    if up is None: raise FileNotFoundError(solvent)
+    s,po,mo=read_sigma(op); _,pu,mu=read_sigma(up)
+    Ao,Au=float(po.sum()),float(pu.sum())
+    with tempfile.TemporaryDirectory(prefix='r4-factorial-') as td:
+        b=Path(td); solutep=Path(a.open_profiles)/f'{solute}.sigma'
+        if not solutep.is_file(): raise FileNotFoundError(solutep)
+        (b/solutep.name).symlink_to(solutep.resolve())
+        if a.corner=='UD': (b/f'{solvent}.sigma').symlink_to(Path(up).resolve())
+        else:
+            # Bit order is A, V, normalized 153-bin shape. Never change fitted constants.
+            iA,iV,iP=map(int,a.corner)
+            area=Au if iA else Ao; p=(pu/Au if iP else po/Ao)*area; meta=dict(mo)
+            meta.update({'area [A^2]':area,'volume [A^3]':mu['volume [A^3]'] if iV else mo['volume [A^3]'],
+                'r4_diagnostic':'AVP '+a.corner,'source':'counterfactual only, never adopted'})
+            write_sigma(b/f'{solvent}.sigma',s,p,meta)
+        os.environ['ZC_SIGMA_OVERRIDE_DIR']=td
+        from zcosmo.models import make_model
+        compounds=pd.read_csv(a.compounds);smi=dict(zip(compounds.inchikey,compounds.smiles))
+        model=make_model('Z0x',[solute,solvent],[smi[solute],smi[solvent]])
+        vals=[]
+        for r in rows.itertuples():
+            try: y=float(model.lngamma_inf(r.T,0));err=''
+            except Exception as e: y=np.nan;err=repr(e)
+            vals.append(dict(r3_row_id=r.r3_row_id,value=y,error=err))
+        pd.DataFrame(vals).to_csv(a.out,index=False)
+        write_json(str(a.out)+'.inputs.json',dict(open_solvent=digest(op),UD_solvent=digest(up),
+            open_solute=digest(solutep),dielectric=digest('results/qc/dielectric.csv'),
+            dispersion=digest('results/qc/dispersion.csv'),Z0=digest('results/z_params/Z0.json')))
+
+
+def factorial(a):
+    d=pd.read_csv(a.paired_rows)
+    if 'r3_row_id' not in d or d.r3_row_id.duplicated().any(): raise ValueError('use unique paired_rows from P16')
+    panel=set(Path(a.keys).read_text().split());d=d[d.solvent.isin(panel)].copy()
+    if d.empty: raise ValueError('selected solvents have no rows in the frozen scored set')
+    out=Path(a.out);out.mkdir(parents=True,exist_ok=True);joined=[]
+    corners=[''.join(c) for c in itertools.product('01',repeat=3)]
+    for j,(_,g) in enumerate(d.groupby(['solute','solvent'],sort=True)):
+        part=out/f'pair-{j:04d}';part.mkdir(exist_ok=True);rp=part/'rows.csv';g.to_csv(rp,index=False)
+        f=g.set_index('r3_row_id').copy()
+        for corner in corners+['UD']:
+            dest=part/f'{corner}.csv'
+            subprocess.run([sys.executable,str(Path(__file__).resolve()),'worker','--rows',str(rp),
+                '--corner',corner,'--open-profiles',a.open_profiles,'--compounds',a.compounds,
+                '--out',str(dest)],check=True)
+            q=pd.read_csv(dest).set_index('r3_row_id')
+            if not q.index.is_unique or set(q.index)!=set(f.index): raise ValueError('worker identity mismatch')
+            f[corner]=q.loc[f.index,'value']
+        valid=np.isfinite(f[corners+['UD']].to_numpy()).all(1);f['all_corners_finite']=valid
+        if valid.any() and abs(f.loc[valid,'111']-f.loc[valid,'UD']).max()>1e-10:
+            raise AssertionError('A,V,shape do not exhaust this Z0x solvent substitution')
+        vals={c:f[c].to_numpy(float) for c in corners}
+        phi=shapley_three(vals)
+        for k,v in zip(('A','V','shape'),phi): f['delta_lngamma_'+k]=v
+        if valid.any() and abs(phi.sum(0)[valid]-(vals['111']-vals['000'])[valid]).max()>1e-10:
+            raise AssertionError('Shapley identity failed')
+        joined.append(f)
+    result=pd.concat(joined);result.to_csv(out/'factorial_rows.csv')
+    write_json(out/'summary.json',dict(rows=len(result),finite_all=int(result.all_corners_finite.sum()),
+        unavailable=result.index[~result.all_corners_finite].tolist(),
+        direction='open solvent to UD A,V,shape; solute remains open; dielectric and C6 tables frozen',
+        registration=a.registration,paired_rows_sha256=digest(a.paired_rows)))
+    if not result.all_corners_finite.all(): raise SystemExit(2)
+
+
+def main():
+    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
+    q=s.add_parser('inventory');q.add_argument('--paired-rows');q.add_argument('--idac',default='data/benchmark/idac.csv')
+    q.add_argument('--geometry-dir',default='data/pyscf_sigma/profiles_v2');q.add_argument('--geometry-map')
+    q.add_argument('--ud-cosmo',default='data/raw/nist/UD/cosmo')
+    q=s.add_parser('factorial');q.add_argument('--paired-rows',required=True);q.add_argument('--keys',required=True)
+    q.add_argument('--registration',required=True)
+    q=s.add_parser('worker');q.add_argument('--rows',required=True)
+    q.add_argument('--corner',required=True,choices=[''.join(c) for c in itertools.product('01',repeat=3)]+['UD'])
+    for q in s.choices.values():
+        q.add_argument('--open-profiles',required=True);q.add_argument('--out',required=True)
+        q.add_argument('--compounds',default='data/benchmark/compounds.csv')
+    a=p.parse_args();globals()[a.cmd](a)
+if __name__=='__main__':main()
```

<!-- PATCH:P22 -->
```diff
--- /dev/null
+++ b/scripts/r4_charge.py
@@ -0,0 +1,211 @@
+"""Raw PCM charge and parser diagnostics, with explicitly unadopted A projections.
+
+The neutral Gaussian sphere is an analytic reference, not a molecule benchmark.
+No charge is silently renormalized. Native calculations require pinned PySCF.
+"""
+from __future__ import annotations
+import argparse
+from importlib.metadata import version
+import json
+from pathlib import Path
+import time
+import numpy as np
+from scipy.linalg import lu_factor,lu_solve
+from scipy.special import erf,erfc
+from scipy.spatial.distance import cdist
+from r3_common import digest,write_json,profile_descriptors
+from r4_common import geometry,parser_trace,contacts
+
+
+def gaussian_sphere(t,Z=1.,f=1.):
+    """Neutral point nucleus + normalized Gaussian electrons; zero boundary potential."""
+    return dict(t=float(t),total_solute_charge=0.,
+        screening_charge_e=float(-f*Z*erfc(t)),
+        electrons_outside=float(Z*(erfc(t)+2*t/np.sqrt(np.pi)*np.exp(-t*t))))
+
+
+def project(q,area,K):
+    """Two different A sensitivities. Neither is an outlying-charge correction."""
+    q=np.asarray(q,float);area=np.asarray(area,float);K=np.asarray(K,float)
+    if q.shape!=area.shape or K.shape!=(len(q),len(q)) or np.any(area<=0): raise ValueError('bad projection inputs')
+    c=np.linalg.solve(K,np.ones(len(q))); den=float(c.sum())
+    if not np.isfinite(den) or den<=0: raise ValueError('invalid capacitance direction')
+    qa=q-q.sum()*area/area.sum(); qc=q-q.sum()*c/den
+    for x in (qa,qc):
+        if abs(x.sum())>1e-10: raise AssertionError('charge constraint failed')
+    return qa,qc,c
+
+
+def pcm_settings(s,order,radius_scale=1.):
+    from pyscf.data import elements
+    from zcosmo.pyscf_cosmo import RADII,BOHR
+    s.method='C-PCM';s.eps=1e9;s.lebedev_order=order;s.vdw_scale=1.
+    table=np.zeros(120)
+    for el,r in RADII.items(): table[elements.charge(el)]=radius_scale*r/BOHR
+    s.radii_table=table
+
+
+def factory(sym,x,spin,basis,memory):
+    import pyscf
+    if pyscf.__version__!='2.14.0': raise RuntimeError('requires pyscf==2.14.0')
+    from pyscf import gto,dft
+    from zcosmo.pcm_lu import cache_pcm3c
+    mol=gto.M(atom=list(zip(sym,x.tolist())),basis=basis,unit='Angstrom',spin=spin,verbose=0,max_memory=memory)
+    mf=(dft.UKS(mol) if spin else dft.RKS(mol)).density_fit().PCM()
+    mf=cache_pcm3c(mf);mf.xc='b88,p86';mf.grids.level=3;mf.conv_tol=1e-9
+    pcm_settings(mf.with_solvent,29)
+    return mf
+
+
+def segments(s,q=None):
+    from zcosmo.pyscf_cosmo import BOHR
+    surf=s.surface; area=np.asarray(surf['area']);keep=area>1e-8
+    owners=np.concatenate([np.full(int(b-a),i) for i,(a,b) in enumerate(surf['gslice_by_atom'])])
+    q=np.asarray(s._intermediates['q'] if q is None else q)
+    return dict(xyz=np.asarray(surf['grid_coords'])[keep],q=q[keep],area=area[keep]*BOHR**2,atom=owners[keep]),keep
+
+
+def potential(coords,s,c):
+    """Potential of the discrete capacitary Gaussian layer, in atomic units."""
+    d=cdist(coords,np.asarray(s.surface['grid_coords']))
+    xi=np.asarray(s.surface['charge_exp'])[None,:]
+    value=np.empty_like(d); nz=d>1e-14
+    np.divide(erf(xi*d),d,out=value,where=nz)
+    value[~nz]=np.broadcast_to(2*xi/np.sqrt(np.pi),d.shape)[~nz]
+    return value@c
+
+
+def density_partition(mf,dm,s,level):
+    """A volume-quadrature check of q=-f integral rho*u, partitioned about the sphere union.
+
+    The sphere union is a declared diagnostic boundary. SWIG is smooth, so its
+    inside/outside split is not claimed to be a unique physical cavity partition.
+    """
+    from pyscf import dft
+    from pyscf.data import elements
+    from zcosmo.pyscf_cosmo import RADII,BOHR
+    mol=mf.mol;K=np.asarray(s._intermediates['K']);c=np.linalg.solve(K.T,np.ones(len(K)))
+    grids=dft.gen_grid.Grids(mol);grids.level=level;grids.build()
+    xyz=mol.atom_coords();rad=np.array([RADII[el]/BOHR for el in mol.elements])
+    N=Nu=Nout=Din=Dout=0.
+    for lo in range(0,len(grids.coords),256):
+        p=grids.coords[lo:lo+256];w=grids.weights[lo:lo+256]
+        ao=dft.numint.eval_ao(mol,p,deriv=0)
+        rho=dft.numint.eval_rho(mol,ao,dm,xctype='LDA')
+        u=potential(p,s,c);outside=(cdist(p,xyz)>=rad[None,:]).all(1)
+        wr=w*rho;N+=float(wr.sum());Nu+=float(wr@u);Nout+=float(wr[outside].sum())
+        z=wr*(1-u);Din+=float(z[~outside].sum());Dout+=float(z[outside].sum())
+    un=potential(xyz,s,c);Z=mol.atom_charges();Dn=float(Z@(1-un));f=float(s._intermediates['f_epsilon'])
+    q=float(np.asarray(s._intermediates['q']).sum());qhat=-f*(float(Z@un)-Nu)
+    parts=-f*(float(Z.sum())-N)+f*Dn-f*Din-f*Dout
+    if abs(parts-qhat)>1e-9: raise AssertionError('partition algebra failed')
+    return dict(level=level,points=len(grids.coords),electron_count=N,electron_count_error=N-mol.nelectron,
+        electrons_outside_union=Nout,nuclear_defect_e=Dn,electron_inside_defect_e=Din,
+        electron_outside_defect_e=Dout,screening_charge_e=q,quadrature_charge_e=qhat,
+        quadrature_charge_error_e=qhat-q,
+        nuclear_contribution_e=f*Dn,inside_contribution_e=-f*Din,outside_contribution_e=-f*Dout,
+        note='Interpret outlying charge only after both levels agree and total electron/charge quadrature converges.')
+
+
+def molecule(a):
+    sym,x=geometry(a.geometry);out=Path(a.out)
+    if out.exists() and any(out.iterdir()): raise FileExistsError(out)
+    out.mkdir(parents=True,exist_ok=True);t=time.perf_counter()
+    mf=factory(sym,x,a.spin,a.basis,a.memory);e=mf.kernel()
+    if not mf.converged or not np.isfinite(e): raise RuntimeError('SCF failed')
+    s=mf.with_solvent;it=s._intermediates;K=np.asarray(it['K']);q=np.asarray(it['q']);v=np.asarray(it['v_grids'])
+    R=np.asarray(it['R']);seg,keep=segments(s)
+    from zcosmo.pyscf_cosmo import to_profiles,write_sigma
+    native,meta=to_profiles(sym,x,seg);p,traceout,trace=parser_trace(sym,x,seg)
+    arr=lambda o:np.stack([o.psigmaA_nhb,o.psigmaA_OH,o.psigmaA_OT])
+    if np.max(abs(arr(native)-arr(traceout)))>1e-10: raise AssertionError('parser instrumentation changed bins')
+    meta.update(source='R4 charge diagnostic, not adopted',r4_registration=a.registration,
+        geometry_converged='R4-frozen',E_scf_Eh=float(e),input_geometry_sha256=digest(a.geometry))
+    write_sigma(out/f'{a.key}.sigma',native,meta,a.key)
+    np.savez_compressed(out/f'{a.key}.segments.npz',sym=np.asarray(sym),x=x,**seg)
+    dm=np.asarray(it['dm']);dm=dm.sum(axis=0) if dm.ndim==3 else dm
+    ne=float(np.einsum('ij,ji->',dm,mf.get_ovlp()))
+    rhs=R@v
+    report=dict(key=a.key,basis=a.basis,grid_level=3,lebedev_order=29,eps=1e9,
+        spin=a.spin,SCF_converged=True,electron_count_overlap=ne,declared_electrons=mf.mol.nelectron,
+        surface_points=len(q),kept_points=int(keep.sum()),raw_full_q_e=float(q.sum()),raw_kept_q_e=float(q[keep].sum()),
+        omitted_q_e=float(q[~keep].sum()),q_sym_sum_e=float(np.asarray(it['q_sym']).sum()),
+        q_vs_qsym_max_e=float(np.max(abs(q-np.asarray(it['q_sym'])))),
+        linear_residual_relative=float(np.max(abs(K@q-rhs))/max(1.,np.max(abs(rhs)))),
+        K_symmetry_relative=float(np.max(abs(K-K.T))/max(1.,np.max(abs(K)))),
+        parser=trace,geometry_contacts=contacts(sym,x),profile=profile_descriptors(out/f'{a.key}.sigma'),
+        native_pyscf=version('pyscf'),input_geometry_sha256=digest(a.geometry),registration=a.registration)
+    if abs(ne-mf.mol.nelectron)>1e-7 or report['linear_residual_relative']>1e-10:
+        raise AssertionError('electron count or PCM linear solve failed')
+    if a.projections:
+        qa,qc,c=project(q,np.asarray(s.surface['area']),K)
+        report['projections']={}
+        for name,newq in [('area_zero',qa),('capacitary_zero',qc)]:
+            sub=out/name;sub.mkdir();qs,_=segments(s,newq);z,mm=to_profiles(sym,x,qs)
+            mm.update(meta);mm.update(source='R4 A charge-constraint sensitivity, not OCC, not adopted',r4_projection=name)
+            write_sigma(sub/f'{a.key}.sigma',z,mm,a.key)
+            report['projections'][name]=dict(sum_q_e=float(newq.sum()),
+                boundary_residual_variation=float(np.ptp(K@(newq-q))),
+                descriptors=profile_descriptors(sub/f'{a.key}.sigma'))
+    if a.sweep:
+        from pyscf.solvent.pcm import PCM
+        from zcosmo.pcm_lu import CachedPCM
+        sweep=[]
+        for order,scale in [(29,1.),(41,1.),(59,1.),(29,1.10)]:
+            sp=CachedPCM(mf.mol);sp.max_memory=a.memory;pcm_settings(sp,order,scale)
+            sp._get_vind(dm)
+            sweep.append(dict(order=order,radius_scale=scale,frozen_density=True,
+                points=len(sp._intermediates['q']),sum_q_e=float(np.sum(sp._intermediates['q']))))
+        report['fixed_density_sweep']=sweep
+    if a.quadrature:
+        report['density_partitions']=[density_partition(mf,dm,s,level) for level in (4,5)]
+        a4,a5=report['density_partitions']
+        report['quadrature_gate']=bool(abs(a5['electron_count_error'])<1e-5 and
+            abs(a5['quadrature_charge_error_e'])<1e-5 and
+            abs(a5['electron_outside_defect_e']-a4['electron_outside_defect_e'])<1e-4 and
+            abs(a5['electron_inside_defect_e']-a4['electron_inside_defect_e'])<1e-4)
+    report['wall_s']=time.perf_counter()-t;write_json(out/'charge.json',report)
+    print(json.dumps(report,indent=2))
+    if a.quadrature and not report['quadrature_gate']: return 2
+    return 0
+
+
+def sphere_native(a):
+    import pyscf
+    if pyscf.__version__!='2.14.0': raise RuntimeError('requires pyscf==2.14.0')
+    from pyscf import gto
+    from pyscf.solvent.pcm import PCM
+    mol=gto.M(atom='He 0 0 0',basis='def2-svp',verbose=0)
+    records=[]; radius=4.
+    for order in (29,41,59):
+        s=PCM(mol);s.method='C-PCM';s.eps=1e9;s.lebedev_order=order
+        tab=np.full(120,radius);s.radii_table=tab;s.build()
+        K=s._intermediates['K'];xi=np.asarray(s.surface['charge_exp']);f=s._intermediates['f_epsilon']
+        lu=lu_factor(K)
+        for t in (6.,1.5):
+            alpha=(t/radius)**2;effective=xi*np.sqrt(alpha)/np.sqrt(xi*xi+alpha)
+            # Convolve the analytic source with the SAME Gaussian test functions as the PCM surface.
+            v=(erf(xi*radius)-erf(effective*radius))/radius
+            q=lu_solve(lu,-f*v)
+            exact=gaussian_sphere(t,f=f)
+            records.append(dict(order=order,points=len(q),**exact,discrete_screening_charge_e=float(q.sum()),
+                error_to_continuum_e=float(q.sum()-exact['screening_charge_e']),
+                residual=float(np.max(abs(K@q+f*v)))))
+    write_json(a.out,dict(records=records,note='Synthetic analytic source, not a molecular density. No SCF or experimental data.'))
+
+
+def main():
+    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
+    q=s.add_parser('analytic');q.add_argument('--out',required=True)
+    q=s.add_parser('sphere-native');q.add_argument('--out',required=True)
+    q=s.add_parser('molecule');q.add_argument('--geometry',required=True);q.add_argument('--key',required=True)
+    q.add_argument('--out',required=True);q.add_argument('--registration',required=True)
+    q.add_argument('--basis',choices=['def2-svp','def2-tzvp'],default='def2-tzvp')
+    q.add_argument('--spin',type=int,default=0);q.add_argument('--memory',type=int,default=6000)
+    q.add_argument('--quadrature',action='store_true');q.add_argument('--sweep',action='store_true')
+    q.add_argument('--projections',action='store_true')
+    a=p.parse_args()
+    if a.cmd=='analytic': write_json(a.out,dict(spheres=[gaussian_sphere(t) for t in (6.,1.5)]))
+    elif a.cmd=='sphere-native': sphere_native(a)
+    else: raise SystemExit(molecule(a))
+if __name__=='__main__':main()
```

<!-- PATCH:P23 -->
```diff
--- /dev/null
+++ b/scripts/r4_lle.py
@@ -0,0 +1,242 @@
+"""LLE quality accounting and an opt-in A numerical repair, separate from production.
+
+No unresolved call is converted to 'miscible'. Grid tests are never certificates
+of global stability or absence of narrower gaps. Original predictions are retained.
+"""
+from __future__ import annotations
+import argparse
+import hashlib
+import json
+import os
+from pathlib import Path
+import time
+import numpy as np
+import pandas as pd
+from scipy.optimize import least_squares
+from r3_common import digest,write_json
+
+RESIDUAL=1e-7
+MARGIN=1e-7
+
+
+def call_key(r):
+    return (str(r['model']),str(r['c1']),str(r['c2']),float(r.get('binodal_T',r.get('T'))))
+
+
+def load_records(path):
+    path=Path(path);files=sorted(path.rglob('*.jsonl')) if path.is_dir() else [path]
+    if not files: raise FileNotFoundError(path)
+    out={};duplicates=0
+    for p in files:
+        for line in p.read_text().splitlines():
+            if not line.strip(): continue
+            r=json.loads(line);k=call_key(r)
+            if k in out:
+                if out[k]!=r: raise ValueError(f'conflicting repeated audit record: {k}')
+                duplicates+=1
+            out[k]=r
+    if not out: raise ValueError('empty sidecar')
+    return out,dict(files=[dict(path=str(p.resolve()),sha256=digest(p)) for p in files],identical_duplicates=duplicates)
+
+
+def quality(r):
+    if r['status']=='no_gap_on_grid': return 0.,'no_gap_on_81_grid'
+    if r['status']!='refined_root': return np.nan,r['status']
+    residual=r.get('residual_max');margin=r.get('sampled_tangent_margin');b=r.get('returned')
+    if not isinstance(b,(list,tuple)) or len(b)!=2 or not 0<b[0]<b[1]<1 or b[1]-b[0]<=1e-4:
+        return np.nan,'invalid_endpoints'
+    if residual is None or not np.isfinite(residual) or residual>=RESIDUAL: return np.nan,'residual_failed'
+    if margin is None or not np.isfinite(margin): return np.nan,'tangent_unchecked'
+    if margin < -MARGIN: return np.nan,'negative_tangent_margin'
+    return 1.,'root_passes_sampled_checks'
+
+
+def bounds(decisions,systems):
+    """Keep every row and the original >1/2 per-system aggregation."""
+    d=np.asarray(decisions,float);systems=np.asarray(systems,str)
+    if len(d)!=len(systems) or not len(d): raise ValueError('empty or inconsistent denominator')
+    if not np.isin(d[np.isfinite(d)],[0.,1.]).all(): raise ValueError('invalid nullable decision')
+    low=np.nan_to_num(d,nan=0.);high=np.nan_to_num(d,nan=1.)
+    u=np.unique(systems)
+    return dict(rows=len(d),systems=len(u),unresolved_rows=int(np.isnan(d).sum()),
+        row_gap_found_bounds=[float(low.mean()),float(high.mean())],
+        system_gap_found_bounds=[float(np.mean([low[systems==s].mean()>.5 for s in u])),
+                                 float(np.mean([high[systems==s].mean()>.5 for s in u]))],
+        interpretation='Bounds for this finite-grid quality screen, not certified thermodynamic bounds.')
+
+
+def lower_gaps(xs,g):
+    hull=[]
+    for i in range(len(xs)):
+        while len(hull)>=2:
+            j,k=hull[-2:]
+            if (xs[k]-xs[j])*(g[i]-g[j])-(g[k]-g[j])*(xs[i]-xs[j])<=0: hull.pop()
+            else: break
+        hull.append(i)
+    return [(xs[i],xs[j]) for i,j in zip(hull[:-1],hull[1:]) if j-i>1]
+
+
+class BudgetExceeded(RuntimeError): pass
+
+
+def strict_binodal(model,T,budget=4000):
+    """Bounded numerical repair. No clipping inside equations; reject trivial roots."""
+    cache={};calls=0;history=[];witness=None
+    def unresolved(reason):
+        return dict(status='gap_witness_only' if witness else 'unresolved',reason=reason,
+                    history=history,model_calls=calls,nonconvex_witness=witness,globally_certified=False)
+    def lg(x):
+        nonlocal calls
+        x=float(x)
+        if not 0<x<1: raise ValueError('composition outside open interval')
+        if x not in cache:
+            if calls>=budget: raise BudgetExceeded('model-call budget exhausted')
+            calls+=1;y=np.asarray(model.lngamma(T,np.array([x,1-x])),float)
+            if y.shape!=(2,) or not np.isfinite(y).all(): raise ValueError('nonfinite model')
+            cache[x]=y
+        return cache[x]
+    def mu(x): return np.log([x,1-x])+lg(x)
+    try:
+        for n in (81,161,321):
+            xs=np.unique(np.r_[np.logspace(-8,-2,14),np.linspace(.02,.98,n),1-np.logspace(-2,-8,14)])
+            m=np.array([mu(x) for x in xs]);g=np.sum(np.c_[xs,1-xs]*m,axis=1)
+            gaps=lower_gaps(xs,g)
+            for a,b in gaps:
+                ia,ib=np.searchsorted(xs,[a,b]);inside=np.arange(ia+1,ib)
+                if not len(inside): continue
+                chord=g[ia]+(g[ib]-g[ia])*(xs[inside]-a)/(b-a)
+                j=int(inside[np.argmax(g[inside]-chord)])
+                depth=float(g[j]-(g[ia]+(g[ib]-g[ia])*(xs[j]-a)/(b-a)))
+                if depth>1e-7 and (witness is None or depth>witness['depth']):
+                    witness=dict(x=[float(a),float(xs[j]),float(b)],g=[float(g[ia]),float(g[j]),float(g[ib])],depth=depth)
+            if len(gaps)>4: return unresolved('more than four sampled gaps')
+            roots=[];failures=[]
+            for initial in gaps:
+                mid=sum(initial)/2;sep=min(1e-8,(initial[1]-initial[0])/8)
+                lb=[1e-10,mid+sep];ub=[mid-sep,1-1e-10]
+                def eq(v): return mu(v[0])-mu(v[1])
+                opt=least_squares(eq,np.asarray(initial),bounds=(lb,ub),
+                    xtol=1e-12,ftol=1e-12,gtol=1e-12,max_nfev=120,diff_step=1e-6)
+                a,b=map(float,opt.x);ma,mb=mu(a),mu(b);res=float(abs(ma-mb).max())
+                plane=(ma+mb)/2;margin=float(np.min(g-(np.c_[xs,1-xs]@plane)))
+                valid=bool(res<RESIDUAL and margin>=-MARGIN and b-a>1e-4)
+                r=dict(x=[a,b],residual=res,sampled_tangent_margin=margin,
+                       solver_success=bool(opt.success),accepted=valid)
+                (roots if valid else failures).append(r)
+            roots.sort(key=lambda r:r['x'][0])
+            history.append(dict(n=n,sampled_points=len(xs),sampled_gaps=len(gaps),roots=roots,failures=failures))
+        previous,last=history[-2:]
+        if previous['failures'] or last['failures']:
+            return unresolved('refinement/stability check failed')
+        p,q=previous['roots'],last['roots']
+        stable=len(p)==len(q) and all(np.max(abs(np.asarray(a['x'])-b['x']))<5e-5 for a,b in zip(p,q))
+        if not stable: return unresolved('grid refinement changed roots')
+        if not q and witness: return unresolved('positive nonconvexity witness without checked endpoints')
+        if not q:
+            return dict(status='no_gap_on_refined_grid',roots=[],history=history,model_calls=calls,
+                        globally_certified=False)
+        return dict(status='root_passes_refined_sampled_checks',roots=q,history=history,model_calls=calls,
+                    globally_certified=False,nonconvex_witness=witness)
+    except (BudgetExceeded,ValueError,RuntimeError,FloatingPointError) as e:
+        return unresolved(repr(e))
+
+
+def audit(a):
+    calls,provenance=load_records(a.sidecars)
+    repairs,rprov=load_records(a.repairs) if a.repairs else ({},None)
+    d=pd.read_csv(a.predictions).reset_index(drop=True)
+    if d['split'].isna().any(): raise ValueError('missing split labels')
+    if a.split=='test': d=d[d['split']!='train'].copy()
+    elif a.split=='train':d=d[d['split']=='train'].copy()
+    if not len(d): raise ValueError('empty requested split')
+    out=Path(a.out);out.mkdir(parents=True,exist_ok=True);rows=[];used=set();unknown={}
+    for index,r in d.iterrows():
+        key=(a.model,str(r.c1),str(r.c2),float(round(float(r['T'])/2)*2))
+        if key not in calls: raise ValueError(f'missing audit call for prediction row: {key}')
+        c=calls[key];used.add(key);b=c.get('returned')
+        pv=r.pred_split
+        if not isinstance(pv,(bool,np.bool_)): raise ValueError('pred_split must be Boolean, not strings or NaN')
+        if bool(pv)!=(b is not None): raise ValueError('sidecar and prediction disagree')
+        if b is not None and not np.allclose([r.pred_x1_I,r.pred_x1_II],b,rtol=0,atol=1e-12):
+            raise ValueError('sidecar endpoint mismatch')
+        decision,status=quality(c);xy=b
+        if key in repairs:
+            repair=repairs[key]
+            if repair.get('reference_call_sha256')!=hashlib.sha256(json.dumps(c,sort_keys=True).encode()).hexdigest():
+                raise ValueError('repair belongs to a different reference call')
+            status=repair['status']
+            if status=='root_passes_refined_sampled_checks':
+                decision=1.;xy=max(repair['roots'],key=lambda q:q['x'][1]-q['x'][0])['x']
+            elif status=='gap_witness_only': decision=1.;xy=None
+            elif status=='no_gap_on_refined_grid': decision=0.;xy=None
+            else: decision=np.nan;xy=None
+        if not np.isfinite(decision):
+            unknown[key]=dict(model=key[0],c1=key[1],c2=key[2],binodal_T=key[3],status=status)
+        rows.append(dict(original_row_index=int(index),r4_split=decision,r4_status=status,
+            r4_x1_I=xy[0] if decision==1. and xy is not None else np.nan,r4_x1_II=xy[1] if decision==1. and xy is not None else np.nan,
+            call_key=json.dumps(key)))
+    q=pd.DataFrame(rows,index=d.index);result=pd.concat([d,q],axis=1)
+    result.to_csv(out/'quality_rows.csv',index=False)
+    pd.DataFrame(list(unknown.values()),columns=['model','c1','c2','binodal_T','status']).to_csv(out/'unresolved_calls.csv',index=False)
+    systems=np.where(d.c1.to_numpy(str)<d.c2.to_numpy(str),d.c1+'|'+d.c2,d.c2+'|'+d.c1)
+    summary=bounds(q.r4_split,systems)
+    relevant=[calls[k] for k in used]
+    summary.update(model=a.model,split=a.split,unique_calls=len(used),legacy_gap_found_rows=float(d.pred_split.mean()),
+        statuses=q.r4_status.value_counts().to_dict(),source_sha256=digest(a.predictions),sidecar_inputs=provenance,
+        repairs=rprov,negative_margin_calls_raw=sum(c.get('sampled_tangent_margin',0) is not None and c.get('sampled_tangent_margin',0)<0 for c in relevant),
+        note='Primary prediction columns are unchanged. Do not pass nullable r4_split to metrics.lle_rows or astype(bool).')
+    good=(q.r4_split==1.) & np.isfinite(q[['r4_x1_I','r4_x1_II']].to_numpy()).all(1)
+    if good.any():
+        err=np.minimum(abs(d.loc[good,'x1']-q.loc[good,'r4_x1_I']),abs(d.loc[good,'x1']-q.loc[good,'r4_x1_II']))
+        summary['composition_MAE_on_checked_detections']=float(err.mean());summary['composition_MAE_denominator']=int(good.sum())
+    write_json(out/'summary.json',summary)
+
+
+def repair(a):
+    if not a.registration: raise ValueError('prospective registration identifier required')
+    calls,prov=load_records(a.sidecars);todo=pd.read_csv(a.calls)
+    if todo.empty: raise ValueError('no unresolved calls selected')
+    if a.background: os.environ['ZC_SIGMA_OVERRIDE_DIR']=str(Path(a.background).resolve())
+    else: os.environ.pop('ZC_SIGMA_OVERRIDE_DIR',None)
+    from zcosmo.models import make_model
+    from zcosmo.evaluate import binodal
+    from zcosmo.cosmosac import sigma_path
+    compounds=pd.read_csv(a.compounds);smi=dict(zip(compounds.inchikey,compounds.smiles))
+    path=Path(a.out)
+    if path.exists(): raise FileExistsError(path)
+    path.parent.mkdir(parents=True,exist_ok=True)
+    with path.open('w') as f:
+        for r in todo.itertuples():
+            key=(r.model,r.c1,r.c2,float(r.binodal_T));reference=calls[key]
+            model=make_model(r.model,[r.c1,r.c2],[smi[r.c1],smi[r.c2]])
+            used={}
+            for k in (r.c1,r.c2):
+                pp=sigma_path(k)
+                if pp is None: raise FileNotFoundError(k)
+                used[k]=dict(path=str(pp.resolve()),sha256=digest(pp))
+            replay=binodal(model,float(r.binodal_T));old=reference['returned']
+            if (replay is None)!=(old is None) or (old is not None and not np.allclose(replay,old,rtol=0,atol=1e-8)):
+                raise ValueError('legacy replay disagrees: freeze the correct profile/data/model source first')
+            model=make_model(r.model,[r.c1,r.c2],[smi[r.c1],smi[r.c2]])
+            t=time.perf_counter();answer=strict_binodal(model,float(r.binodal_T),budget=4000)
+            answer['profile_inputs']=used
+            answer.update(model=r.model,c1=r.c1,c2=r.c2,binodal_T=float(r.binodal_T),
+                registration=a.registration,wall_s=time.perf_counter()-t,
+                reference_call_sha256=hashlib.sha256(json.dumps(reference,sort_keys=True).encode()).hexdigest())
+            f.write(json.dumps(answer,allow_nan=False)+'\n');f.flush()
+    write_json(str(path)+'.inputs.json',dict(sidecars=prov,calls_sha256=digest(a.calls),
+        registration=a.registration,global_certification=False,
+        model_inputs={p:digest(p) for p in ('src/zcosmo/evaluate.py','src/zcosmo/z0x.py',
+            'src/zcosmo/cosmosac.py','results/z_params/Z0.json',
+            'results/qc/dielectric.csv','results/qc/dispersion.csv')}))
+
+
+def main():
+    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
+    q=s.add_parser('audit');q.add_argument('--sidecars',required=True);q.add_argument('--predictions',required=True)
+    q.add_argument('--model',default='Z0x');q.add_argument('--split',choices=['all','test','train'],default='test')
+    q.add_argument('--repairs');q.add_argument('--out',required=True)
+    q=s.add_parser('repair');q.add_argument('--sidecars',required=True);q.add_argument('--calls',required=True)
+    q.add_argument('--compounds',default='data/benchmark/compounds.csv');q.add_argument('--background');q.add_argument('--registration',required=True);q.add_argument('--out',required=True)
+    a=p.parse_args();globals()[a.cmd](a)
+if __name__=='__main__':main()
```

<!-- PATCH:REG4 -->
```diff
--- /dev/null
+++ b/docs/astra/round4/REGISTRATION_PROPOSED.md
@@ -0,0 +1,100 @@
+Round-4 proposed registration. This file is a proposal, not an assertion that it
+has been appended to PREREGISTRATION.md or that any native calculation has run.
+Commit the adopted text with its actual timestamp before new candidate outputs
+are inspected. Reference: 33ebac0146ae2df4dd73fcf8a431cb6d7033554b.
+
+P18 deployment implements the already accepted rule, registration 9d32e9e and
+acceptance 613dd8f. It preserves all raw profile bytes after the first newline,
+all metadata except the dispersion flag and explicit provenance, and the existing
+630 primary plus five S2 plus one S1 partition. The current geometry-based NIST
+classifier is authoritative. An unexpected change other than
+HB-DONOR-ACCEPTOR to COOH stops deployment for investigation. All 636 selected
+profiles and their actual generating geometries are hashed before deployment.
+Verify the 25/2302 gate and exact finite coverage on the Mac. Verify Z0x and
+COSMO-SAC 2010 prediction invariance to 1e-10 on the full existing IDAC row set;
+verify unchanged-target rows on the one-compound COSMO-SAC-dsp check to 1e-10;
+report the new UD compatibility statistic. Append the actual deployment receipt
+and rerun affected open-profile COSMO-SAC-dsp scores under new output names.
+No historical score is overwritten and no flagged geometry is promoted.
+
+P21 is a descriptive mechanism audit, not a fitted or selected model. Select all
+benchmark compounds with at least two structural OH groups or at least one
+non-carbonyl ether oxygen, plus the fixed water, methanol, 1-butanol and n-nonane
+controls, before examining their errors. Freeze the structural mapping, source
+files and row identities in the commit. Inventory all available UD/open profiles
+and geometries; missing data are reported without dropping score denominators.
+For selected solvent rows, evaluate the eight fixed combinations of open/UD
+area, volume and normalized 153-bin shape, with the solute kept open and the
+existing dielectric and C6 tables unchanged. Each corner runs in a separate
+process. Report the full-UD-solvent control and the exact Shapley identity, both
+with numerical tolerance 1e-10 and identical finite coverage. These hybrid
+profiles are diagnostic A substitutions and are never eligible for production.
+
+The initial native geometry panel consists of ethylene, diethylene and
+triethylene glycol at both their saved open and UD geometries, plus water,
+methanol and n-nonane at their saved open geometries. Use fixed BP86/def2-TZVP,
+the current auxiliary basis, XC grid 3/default pruning, C-PCM epsilon 1e9,
+Lebedev 29, project radii and conv_tol 1e-9, without geometry optimization or
+reorientation. Pin PySCF 2.14.0 and all other package versions for paired runs.
+This is at most nine single points. Its diagnostics include geometric O-H...O
+contacts, covalent HB tags, atom-owned surface area, raw and averaged charge
+moments, pre-split areas and final OH/OT/NHB areas. A geometric contact is not a
+measured H-bond energy. No choice is made on an experimental residual.
+
+P22 tests raw surface charge; it does not authorize charge neutralization in
+production. Validate the compact and diffuse neutral analytic Gaussian-sphere
+sources at fixed Lebedev orders 29, 41 and 59. On water, diethylene glycol and
+n-nonane in the native panel, recompute the PCM layer at fixed SCF density for
+those three orders and for one radius scale of 1.10 at order 29. No such layer
+is used in a score. For these molecules, integrate the same density and its
+discrete capacitary potential on independent level-4 and level-5 volume grids.
+Interpret the inside/outside decomposition only if level-5 total electron
+count and reconstructed charge agree within 1e-5 e and the two partition
+contributions change by less than 1e-4 e between levels. Failure is
+inconclusive, not evidence for or against outlying charge. The union of project
+vdW spheres is a stated diagnostic partition, not an exact SWIG boundary.
+
+Two zero-charge projections, uniform sigma shift and the capacitary constrained
+shift, are fixed A sensitivities. Compute both, never a fitted mixture of them,
+for the nine native panel profiles and re-run the unchanged averaging/split.
+Require each projected raw charge sum below 1e-10 e, report every subsequent
+moment and tail change, and compare the same model query identities in fresh
+processes with unchanged finite coverage. These projections are not an outlying
+charge correction and cannot be adopted on the basis of a smaller benchmark
+error. No output from this entry replaces a registered profile. A future
+physical correction or conformer protocol needs a new registration after this
+mechanism audit, with a fixed theoretical construction and a separate validation
+panel before experimental scoring.
+
+P23 first reports the existing P14 sidecar without changing a prediction.
+Classify residuals at 1e-7 and sampled tangent margins at -1e-7. Keep missing
+checks and coarse fallbacks as unresolved. Join records back to their exact
+ordered pair and existing rounded temperature, preserving every requested row
+and the original per-system majority aggregation. Preserve the old columns;
+report quality-screen bounds with unknown votes assigned 0 and 1 separately,
+and the explicit coverage of any endpoint-composition error. These are bounds
+on the finite-grid quality screen, not a global phase-equilibrium certificate.
+
+The opt-in P23 repair is an A numerical correction of the existing evaluator.
+Freeze the complete unresolved-call list before repairing it; do not select
+only favorable binaries. Preserve the model, pure-profile source and existing
+2-K temperature rounding. Use nested 81/161/321 interior grids plus the fixed
+logarithmic tails; try at most four sampled hull gaps and 4,000 new model calls
+per pair-temperature. Use bounded least squares without clipping the equations,
+residual <1e-7, sampled tangent margin >=-1e-7, gap width >1e-4, and agreement of
+the last two grids' root sets within 5e-5 in composition. Exhaustion and failures
+remain unknown. A strictly positive three-point nonconvexity witness supports
+gap existence alone; it supplies no accepted endpoint compositions. No-gap
+results remain explicitly finite-grid results. Record all outcomes, including
+regressions, before producing a separately labelled scorecard. The portable
+ideal/regular-solution and failure-injection tests must pass. For existing good
+roots, a fixed control panel (first 20 sorted calls) must retain gap status,
+meet the new residual/margin checks, and preserve endpoints within 1e-4; a
+failure blocks adoption and is reported. Repairs are saved as a sidecar until
+this gate and a full denominator audit pass. All earlier LLE scores remain.
+
+The six-chain convergence campaign receives zero additional optimization budget
+in this round. P19 remains rejected under its actual cost gate. S1/S2 status is
+preserved as an exploratory endpoint of the present campaign, not a proof of
+Berny convergence. A new optimization experiment requires a separate prospective
+budget and evidence that addresses a specific remaining failure mechanism.
```
