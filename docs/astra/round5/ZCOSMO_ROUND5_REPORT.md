# Z-COSMO round 5: resolving profile-shape mechanisms without selecting on experimental error

Reference: `Victor-Liang-ChE/zcosmo`, `main = 69b49116c2ae7574d7ae471f0a4ed7ba33d0db8b`. This review uses `ROUND5_PROMPT.md`, the full archived round-4 report, its measured results, the round-4 registrations, and the current R4 helpers and native-input workflow. Source identifiers are collected at the end. The six patches below are H5, P24, P25, P26, P27 and REG5. They add experimental/reporting helpers and reuse the already tested P14 audit hook. They do not relabel another production profile or silently adopt a charge convention. [S1–S8]

The next useful calculation is a term-resolved replay of the existing charge and shape substitutions. It costs no quantum calculations. The important new shape diagnostic is **surface-patch-size sensitivity of the averaging**, separated from the HB redistribution. A bounded conformer probe is justified as a mechanism experiment, but an all-compound conformer campaign is not yet justified.

What was executed here: reconstruction and Git-blob checks of the archived R3/R4 helper sources; Python compilation and CLI checks of the new helpers; portable numerical tests; a synthetic nine-arm scorecard test with shuffled row order and excluded/witness rows; and new-file/P14-context patch-application checks. RDKit 2025.09.4 ran two identical EG proposal-generation pools, including MMFF94s optimization, with identical selected coordinates. This was proposal generation from a synthetic EG start, not a new DFT result.

What was not executed: PySCF, native molecular profiles, the actual P22 term replay, the new conformer gates, the Mac-only UD comparisons, or a real regenerated scorecard. The runtime has Python 3.13; the attempted pinned PySCF/pyberny download failed because its package host could not be resolved. That is a network/environment limitation, not evidence that the releases do not exist. No full repository clone or cloud workflow was launched. Native claims below remain conditional on the specified checks.

## Ranked work

| Priority | ID | Mechanism and target | Class | Cost or saving arithmetic | Effort |
|---:|---|---|:---:|---|---|
| Prerequisite | P27 | Regenerate identity-aligned score arms and carry P23 detection/endpoint status into reporting | E reporting; accepted A repair extended under controls | Zero QC calls. Nine evaluator arms; each LLE repair retains the 4,000-call cap. Reuse the validated equations instead of creating another optimizer. | Moderate |
| 1 | P24 | Exact Z0x component accounting, then ES/HB intervention attribution | E accounting; A diagnostic interventions | Zero QC calls; nine profile-set workers over the frozen 859-row panel. Reuse existing P22 profiles. | Low |
| 2 | P25 | Cross saved geometries with fixed basis/cavity settings and inspect averaging stages | E parity controls; A method/postprocessing sensitivities | At most 36 initial single points, versus 630 for a blind full rerun. Conditional avoided work is `594 × t_SP`; no measured speed-up is claimed. | Moderate |
| 3 | P26 probe | Two independent proposal pools on ten non-rigid structural controls | A | At most 40 optimizations, 80 gradient evaluations each, one hour per proposal. Reuse these members if the full protocol is subsequently authorized. | Moderate |
| Conditional | P26 full | Lowest sampled conductor-energy profile, with a separate eight-molecule validation panel | A | Forty additional discovery-panel optimizations and 64 validation optimizations; no rerun of the 630 primary profiles. | High |
| Shared | H5 / REG5 | Utilities, portable tests, and prospective registration text | E instrumentation / proposed policy | No production prediction or profile change. | Shared |

P27 and H5 are correctness/reporting prerequisites. To make the compute ranking explicit under the brief's rule, a planning scenario assigns P24/P25/P26-probe respectively 50/40/20 avoidable worker-hours, probabilities of a useful decision of 0.8/0.5/0.3, and effort units 1/3/5. The resulting saving-times-probability divided by effort is 40, 6.67 and 1.2. These are subjective planning inputs, not measured savings or discovery probabilities; the overlapping budgets cannot be added. Replace them with the actual upcoming workload. No whole-pipeline speed-up is claimed for these diagnostics. P20 remains applied. P15, the P17 orientation recipes and P19 remain rejected under their actual gates. The six-chain campaign remains closed. [S2, S3]

## What round 4 does and does not identify

The area/volume/shape factorial establishes a causal substitution effect **inside the frozen Z0x model**. On its 332-row panel, changing normalized solvent shape alone moved MAE from 1.311 to 0.845; changing area or volume alone barely moved it. That does not identify which quantum or postprocessing operation produced the different shape. The raw outlying-charge projections also do not explain the glycol deficit: DEG moved from 1.740 to 1.640, whereas replacing its whole shape with UD gave 0.371 in that panel. Those are different fixed panels and interventions; their MAEs must not be pooled. [S2]

The water observation is consistent with a common *direction* of shape sensitivity and opposite starting errors. UD shape raises predicted ln gamma by about 1.057 for water-solvent rows and by about 1.372 for DEG-solvent rows in the reported factorial. The open-water mean bias was already positive, +0.683, while DEG's was strongly negative, −1.730. A positive prediction shift can therefore hurt water while helping DEG. Propylene glycol's shape contribution was negative, −0.861; glycerol's was small, +0.037. A theory that treats every OH-containing liquid as one profile defect is already inconsistent with these controls. [S2]

There is an identifiability limit worth stating precisely. With only a stored 153-bin UD histogram, no generating UD geometry and no UD raw segment table, one cannot uniquely decompose its difference into conformer, electronic method, cavity construction and averaging. Many upstream combinations produce the same histogram. The proposed crossed experiment separates those effects **within a known open calculation** and can falsify broad explanations. It cannot reconstruct “whatever UD used” from the final histogram alone. A future exact DMol3/NWChem comparison would require frozen generating inputs and a new backend-specific registration. ISWIG is not being called “DMol3 COSMO.” [S2, S5, U1, U2]

## P24: water and the charge sensitivity belong to identifiable model terms

Targets: `scripts/r5_terms.py`, using the unchanged `Z0xBinary` and `Mixture` implementations. No production function is replaced.

For the actual infinite-dilution call, the code uses the one-sided `h = 1e-4` endpoint formula, not P6's analytic interior branch. Write the frozen-composition activity vector as the sum of combinatorial, residual and London contributions, and define `g_k(x) = x · ln_gamma_k(x)` for each contribution. The exact accounting of the implemented solute endpoint is

\[
L_k=g_k(0)+\frac{g_k(h)-g_k(0)}{h},\qquad
\ln\gamma_1^{\infty,\mathrm{implemented}}=\sum_k L_k.
\]

The patch preserves the actual rounded-coefficient `_mix` cache convention when checking this identity. It also reports the frozen-solvent-coefficient limiting result and the smaller `h = 1e-5, 1e-6` stencils as diagnostics. A small-h result is not installed as another endpoint correction. The parity gate is `max |sum(components) − actual call| < 1e-9`. [S9, S10]

The answer to the first water question is unambiguous in this code: **the H2O dispersion flag does not enter Z0x's London term**. London uses the stored molecular C6/polarizability values and cavity volumes. Relabeling a water `Fluid.disp_flag` to NHB must leave Z0x unchanged. The patch actually performs that intervention. COSMO-SAC-dsp is different: its empirical dispersion sign rule reads H2O/COOH flags. These models must not be conflated. [S10, S11]

For P22's charge projections, the geometries, areas and volumes are unchanged, and the dielectric/C6 tables are frozen. Consequently the combinatorial and London changes are zero apart from rounding. **The observed 0.35 mean change is carried by the segment residual contribution, including the endpoint differentiation of that contribution.** The available summary does not determine its ES/HB partition. The patch measures that rather than guessing that all of it is electrostatic. [S2, S9–S11]

Use four residual kernels: neither interaction, electrostatics only, HB only, and both. For the *change* caused by a profile intervention, the symmetric electrostatic attribution is

\[
\Phi_{ES}=\tfrac12[(\Delta L_{10}-\Delta L_{00})+
                         (\Delta L_{11}-\Delta L_{01})],
\]

with the analogous HB attribution. Their sum equals `ΔL11 − ΔL00`. These are controlled-intervention attributions, not separately measurable electrostatic and hydrogen-bond free energies. The nonlinear segment solve and the pure-liquid reference couple the mechanisms.

A small change in tail **area** does not imply a small change in the residual chemical potential. Charge density moves within the occupied bins; interaction weights are exponential in `−ΔW/RT`; the residual is multiplied by the number of effective molecular segments. Nor is the first moment a sufficient statistic for a complete profile. Report the full distribution change and the term identity alongside the moment. The P22 experiment neutralized only its six selected molecules in an otherwise unchanged open background. Its 0.35 result is not a measured prediction change after neutralizing all 636 molecules. [S2, S10]

There is also a useful theory-only control. With HB switched off and **all continuous sigma labels shifted by the same δ**, keeping their probabilities and all A/V data fixed,

\[
W'_{ij}=c(\sigma_i+\sigma_j+2\delta)^2=W_{ij}+a_i+a_j,
\quad a_i=4c\delta\sigma_i+2c\delta^2.
\]

Therefore `E' = D E D`, with `D_ii = exp(−a_i/RT)`, and the fixed-point solution transforms as `Gamma'_i = exp(a_i/RT) Gamma_i`. The additive shift cancels between mixture and pure-segment log coefficients. The frozen residual, and hence the Z0x construction pointwise in composition, is invariant. The portable test verified the kernel identity to `2.22e-16` and the residual identity to `8.95e-16` on synthetic distributions.

This does **not** justify molecule-specific neutralization. Such a projection uses different shifts `δ_m = −Q_m/A_m`; the HB activation/splitting can change; finite-grid rebinning is a different operation; and the capacitary projection is not even a uniform sigma shift. The common-label identity is a diagnostic for implementation/convention errors, not an adoption argument.

The theory-only argument against simply enforcing zero is the grounded-conductor boundary condition with outlying density: a neutral source can induce a nonzero total apparent screening charge. P22's Gaussian sphere verifies that mechanism. The molecular volume-quadrature gates remained inconclusive, so their quantitative inside/outside partition must still not be presented as validated. PySCF's COSMO export documents that outlying-charge correction is not implemented. [S2, U3]

A neutral-profile convention can be justified only after specifying a consistent corrected electrostatic representation: what charge is assigned outside the cavity, what boundary condition is imposed, and how the corrected potential and energy are related. A charge-only constraint is not enough. Recent NWChem work explicitly distinguishes correction of charges from correction of the associated potential. This is a reason to test a physically specified correction later, not a reason to adopt whichever zero-charge projection improves MAE. [U2]

Decision checks without fitting: reproduce the P22 analytic sphere and linear-solve residual; verify the component and common-label identities; measure per-component changes in the fixed panel; require a future correction to pass its own potential/energy/gradient consistency and grid-convergence checks before an experimental score is read. Neither a good moment nor agreement between two arbitrary projections is a physical validation.

## P25: isolate averaging before calling the missing tail a conformer effect

Targets: `scripts/r5_shape.py` and the independent formula in `r5_common.py`.

The HB postprocessing has a strong exact invariant. In each sigma bin the parser multiplies OH and OT contributions by `P_hb` and transfers their complement to NHB. Thus

\[
p_{NHB}^{post}+p_{OH}^{post}+p_{OT}^{post}
=p_{NHB}^{pre}+p_{OH}^{pre}+p_{OT}^{pre}.
\]

The sign/atom classification may alter which interaction block receives area, but it cannot remove total polar-tail area. The deficit in the **summed** glycol tail must arise before that redistribution, or from a different underlying input table. This narrows the diagnosis substantially. The new code tests the invariant bin by bin and retains the pre-split arrays. Conditional OH/OT fractions are compared only in occupied bins. [S5]

The next nontrivial issue is that the same Hsieh constants do not imply the same smoothing when the tesserae have different areas. The implemented average is

\[
\bar\sigma_i=\frac{\sum_j w_{ij}\sigma_j}{\sum_jw_{ij}},\quad
w_{ij}=\frac{r_j^2r_{av}^2}{r_j^2+r_{av}^2}
\exp\!\left[-\frac{3.57d_{ij}^2}{r_j^2+r_{av}^2}\right],
\quad r_j^2=A_j/\pi,
\quad r_{av}^2=7.25/\pi.
\]

Individual patch area enters the smoothing length as well as its weight. Two surfaces with similar total area can therefore give different averaged tails even with otherwise similar charge-density fields. This is a sensitivity of the actual discrete prescription, not evidence that its constants should be tuned. Averaging also need not preserve the area-weighted first moment, because row normalization is not area-weighted double stochasticity. Raw charge sum, averaged moment and final binned moment are different observables. [S5, S6]

The patch compares the exact original calculation with two fixed **A sensitivities**: replace each patch by four coincident `A/4,q/4` patches, evaluated through an algebraically compressed formula, and take the corresponding point-patch limit. Coordinates and raw charge density stay fixed. This isolates dependence on nominal patch size without a new SCF. It is not physical remeshing, and neither alternative is an approved replacement for Hsieh averaging. The literal-duplication portable check agreed to `1.73e-18 e/Å²`. A new physical averaging protocol would still require a separate construction and gate.

The fixed twelve-member panel is water, methanol, EG/DEG/TEG/tetraEG, glycerol, propylene glycol, 2-methoxyethanol, 1,2-dimethoxyethane, THF and nonane. Homologues, branching and donor-free controls are included before new calculations. Their known historical errors are not pretended to be unseen. A separately frozen eight-member structural validation panel excludes these and the historical 25, and is selected by a fixed SHA ordering, not error. Missing or ambiguous molecular identities fail the planner; names are not used to merge inconsistent compounds.

At each saved geometry run TZVP/SWIG, SVP/SWIG and TZVP/ISWIG, with BP86, project radii, conductor epsilon, Lebedev 29 and XC grid 3 fixed. SVP is a basis-sensitivity probe, not “a better basis.” ISWIG is a cavity-switching probe, not DMol3. PySCF 2.14.0 source implements both switching branches. Preserve the actual resolved DF auxiliary basis and every geometry hash. No density quadrature or repetition of rejected orientation recipes is required. [U1]

The resulting matrix separates several possibilities. A total-spectrum difference already visible in raw charges and owner-resolved distributions points upstream of HB splitting. A large raw-to-Hsieh change, or strong coincident-subdivision sensitivity, identifies averaging as an important mediator. Different conditional OH/OT fractions with similar total spectra identify a block-assignment effect. A large fixed-geometry SWIG/ISWIG effect identifies cavity construction as a plausible contributor. A large change across low-energy conformers at one fixed method identifies conformational sensitivity. Cross the two independently selected pool winners through the same additional methods to measure the conformer-by-method interaction instead of assuming these effects add.

Compare all of these distributions for the controls, including water and the branched polyols. Water has no analogous chain conformer ambiguity, so a water response in the same postprocessing test is evidence against an exclusively conformational explanation. Glycerol and PG are necessary controls for a generic “more OH means missing tail” explanation. No measurement of the current open conformer can establish that an unobserved UD conformer contains an intramolecular H-bond. Report the actual contact geometry and donor/acceptor exposure rather than constructing that story after seeing an error.

## P26: a complete conditional A conformer protocol

Target: `scripts/r5_conformers.py`. This is a **sampled-lowest-conductor-energy single-profile protocol**, not a finite-temperature ensemble.

Use two ETKDGv3 pools of 32 embeddings, seeds 20261005 and 20261006, one thread and `maxIterations=1000`, with pruning disabled. MMFF94s relaxes proposals for at most 500 iterations. It is empirical proposal machinery, already distinct from the quantum model; no ThermoML response trains or selects it. Pin the RDKit version in the frozen manifest. A failed member blocks the pool. There is no seed search, alternate force-field fallback, or geometry invented for a missing input. The official RDKit parameter interface and the local proposal test support these calls. [U4]

From each pool choose the lowest-MMFF proposal and then three greedy farthest proposals. Diversity uses proper fixed-atom-order alignment of heavy atoms **and donor hydrogens**, so an OH orientation can count even when the heavy backbone is similar. Do not assign a thermodynamic degeneracy from how often ETKDG found a basin.

Every chosen start receives the existing CPU BP86/SVP/DF/grid-2/C-PCM-17 Berny calculation, with the original convergence predicate and at most 80 gradient evaluations. The exact API used is `pyscf.geomopt.berny_solver.kernel(mf, maxsteps=80, callback=..., assert_convergence=True)`, pinned to PySCF 2.14.0 and pyberny 0.7.0. The callback reads the source-documented `g_scanner`, `optimizer` and `mol` fields. No Hessian transplant, optimizer pickle, P15 override or P19 precision stage is introduced. Keep the converged orientation, compute the registered TZVP profile, and preserve P18's accepted flag. The saved-reference file travels beside each proposal so its hash is meaningful on another worker. Native execution of this new runner is still untested here. [S12, U5]

Intramolecular H-bonds are neither prohibited nor rewarded. Preserve covalent connectivity, record the already registered O-H...O contact criteria, and let the fixed conductor electronic energy rank the outcomes. Berny convergence is not a proof of a global minimum or a Hessian certificate; the helper calls the output a stationary sample.

The first probe uses only two proposals per pool on ten non-rigid panel members, at most 40 optimizations. Water and methanol remain rigid controls. A continuation needs a predeclared low-energy shape-sensitive pair, within 3 kcal/mol of the sampled minimum, aligned RMSD at least 0.2 Å and normalized profile L1 at least 0.02, with independent-pool results reported. This can justify sampling, not prove that the missing historical UD conformer caused the original error. If no such sensitivity appears in the bounded probe, do not launch a larger conformer campaign from this result.

If continued, finish the eight frozen starts per molecule and run the same protocol on the separate eight-member panel. Select by TZVP conductor energy alone, ties within `1e-7 Eh` by frozen rank. I do not recommend electronic-energy Boltzmann weighting here: it would claim an ensemble without vibrational/rotational free energies, basin degeneracies or composition-dependent conformer populations. A genuine ensemble would need those choices registered explicitly rather than treating embedding frequencies as weights.

The theoretical reproducibility gates are fixed in REG5 and implemented in `select`/`gate`: both pool minima within `1e-4 Eh`, aligned heavy-plus-donor-H RMSD at most 0.15 Å, normalized 153-bin L1 at most 0.02, and selected energy not above the saved-geometry reference by more than `1e-4 Eh`. All eight validation members must complete. Use water, methanol, nonane and dimethoxyethane as fixed affinity probes at 250, 298.15 and 400 K in both roles, 192 queries. Every query must be finite, with maximum independent-pool difference below 0.02 for both Z0x and COSMO-SAC-dsp. No experimental values enter these gates.

A pass means the sampled protocol is reproducible enough for one separately authorized exploratory score. It is not evidence that it improves accuracy. The eight-member panel is computationally separate, not a newly untouched experimental holdout. The 630 primary profiles and all S1/S2 files remain frozen even after a pass; any eventual conformer arm has a different directory and identifier.

A transparent cost model uses `C = n_conf × (n_grad × t_grad + t_SP)`. For illustration only, `n_grad=12`, `t_grad=30 s` and `t_SP=60 s` give seven minutes per conformer: 4.67 worker-hours for the 40-member probe, another 4.67 for the remaining discovery members, and 7.47 for 64 validation members. That is 16.8 four-core worker-hours, or 67.2 core-hours, before the small fixed-geometry matrix. These are planning inputs, not new measurements. Replace them with the first complete native timing, without changing acceptance after seeing errors.

The hard cap is one hour per proposal plus 80 gradient evaluations. Therefore the maximum optimization allocation is 40 worker-hours for the probe and, only if separately continued, 104 more for the remaining discovery and validation work. A deadline creates a censored member and blocks acceptance; it never authorizes another restart. The separate validation cap is 64 worker-hours. No task needs a paid GPU or a runner longer than the free six-hour limit.

## P27: the honest scorecard after P20 and P23

In this comparison, the primary reference remains the registered **UD-profile Z0x**. The 630-profile open arm is a secondary numerical/model comparison. The 636-profile open arm is explicitly exploratory because six geometries carry S1/S2 status. Earlier decisions about the project's headline Z0 model are not rewritten by this report.

| Quantity | Supported result now | Required qualification |
|---|---|---|
| Z0x-UD IDAC | MAE about 0.839 on 828 test points; about 0.800 on the historical 762-point multi-model intersection | Both values are valid with their own denominators. |
| Z0x-open including S1/S2 | Historical paired MAE about 0.977 on 828 points | P20 leaves Z0x unchanged; this remains an exploratory reused-test result. |
| Comparison excluding the six chains | Historical UD/open MAEs about 0.804 / 0.942 on 816 common points | These are the paired subset values, not a universal standalone coverage number. |
| Open COSMO-SAC-dsp after P20, excluding flagged chains | MAE 0.8001 on 750 test rows / 175 systems | It is not comparable to Z0x's 828-row MAE without a common-subset column. |
| Repaired Z0x-UD LLE, test | Operational gap-found 0.8897 over 2,475 rows; system majority 0.8416 over 101 systems | Checked endpoint MAE 0.1799 uses 2,142 rows only. Witnesses have no accepted endpoint error. |
| Repaired Z0x-UD LLE, all | Operational gap-found 0.8453 over 6,581 rows; system majority 0.7954 over 303 systems | Checked endpoint MAE 0.1647 uses 5,278 rows. |
| Open-arm LLE repaired statuses | Must be regenerated for that arm | The UD repair cannot be copied to different profiles. |
| VLE and HE comparisons | New values are not established by the retrieved results | Generate both arms with the same vapor-pressure source/caloric stencil, then report actual finite common denominators. |

The P20 output sizes, IDAC 3,252, VLE 43,042, HE 24,777 and LLE 6,581, are input/output row counts for that recorded run, not universal finite comparison denominators. P27 prints the counts from the actual frozen table universe and the per-arm exclusions. It uses the historical `has_sigma` filtering from `evaluate.run`; a separate expanded non-UD coverage table is outside this comparison. [S2, S3, S13]

The 144 repaired gap witnesses establish detection for those calls but do not supply endpoints. The remaining “no gap on the 81-point grid” calls also do not prove global miscibility. P23 resolved the reporting uncertainty for its finite-grid detection statistic, not the mathematical completeness of every binary phase diagram. The new reporter preserves this wording and the distinct statuses. It does not compute balanced accuracy from the positive LLE table alone. [S7]

P27 runs Z0x, COSMO-SAC 2010 and COSMO-SAC-dsp in UD/open630/open636 arms, one fresh process each. It freezes observation IDs and source hashes; open630 never fills excluded compounds from UD. Continuous metrics use pairwise common subsets rather than an invisible nine-model intersection. IDAC uses the existing ranking rule; VLE uses the same `psat` and the existing homogeneous-liquid exclusion; HE keeps the 0.5 K derivative stencil and sign threshold. System bootstraps use 1,000 resamples with seed 7 reset per statistic, so old CI endpoints need not be bitwise identical to the earlier global RNG sequence. This reporting detail is declared prospectively. [S13, S14]

For each LLE arm, the same first-20-sorted-good-call control gate precedes use of the strict P23 repair. Fewer controls or a regression blocks that arm instead of manufacturing a complete scorecard. Historical files are never overwritten. The regenerated JSON contains requested, eligible, finite/common, unresolved and checked-endpoint counts; the Markdown is a readable summary of that full record.

## Setup and exact commands

Save this report and set `REPORT` to its path. Use an existing asset-bearing Mac checkout for UD-backed work. Native tasks can run in the same pinned Python 3.11 environment on free four-core workers. The installation command below is a specification for those machines, not a claim that it worked in this runtime.

```bash
python3.11 -m venv .venv-r5
source .venv-r5/bin/activate
python -m pip install 'pyscf==2.14.0' 'pyberny==0.7.0' \
  rdkit tblite ase numpy scipy pandas matplotlib thermo chemicals ugropy
python -m pip freeze > r5-environment.txt
```

Do not upgrade this environment between arms. The planner records RDKit's actual version and generation refuses a different version. Existing macOS UD assets, dielectric/C6 tables and NIST parser remain required inputs.

Extract and apply in a disposable experiment checkout. All patches target the pinned main; runtime dependencies are explicit: every helper needs H5/current R3/R4 utilities, P26's affinity gate also needs P24, and the full portable test imports P27. P27 includes the unchanged archived P14 hook because current main still lacks the `audit` argument.

```bash
set -euo pipefail
export BASE=69b49116c2ae7574d7ae471f0a4ed7ba33d0db8b
export REPORT="${REPORT:-$PWD/ZCOSMO_ROUND5_REPORT.md}"
export WORK="$(mktemp -d "${TMPDIR:-/tmp}/zcosmo-r5.XXXXXX")"
python - "$REPORT" "$WORK" <<'PYCODE'
from pathlib import Path
import re,sys
text=Path(sys.argv[1]).read_text();out=Path(sys.argv[2])/'patches';out.mkdir()
blocks=re.findall(r'<!-- PATCH:(H5|P24|P25|P26|P27|REG5) -->\s*```diff\n(.*?)\n```',text,re.S)
assert len(blocks)==6 and len({x for x,_ in blocks})==6
for name,body in blocks:(out/(name+'.patch')).write_text(body+'\n')
PYCODE
# Run from the pinned, populated experiment checkout, not an unrelated working branch.
test "$(git rev-parse HEAD)" = "$BASE"
for id in H5 P24 P25 P26 P27 REG5; do
  git apply --check "$WORK/patches/$id.patch"
  git apply "$WORK/patches/$id.patch"
done
export PYTHONPATH=src:scripts OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export ZC_PCM3C=1 ZC_PCM3C_MB=2000 MPLBACKEND=Agg
unset ZC_ONLY_KEYS ZC_SIGMA_OVERRIDE_DIR ZC_BENCH ZC_PRED ZC_PRED_SPLIT ZC_LLE_AUDIT_DIR
unset ZC_BERNY_NOISE_EH ZC_MAXSTEPS ZC_TRIC_PREOPT
python scripts/r5_selftest.py --rdkit --out "$WORK/portable.json"
```

REG5 creates a *proposed* registration file. Adopt and commit its text with the actual timestamp before new candidate output is used, then set `REG` to that actual registration identifier. A nonempty string is provenance, not proof of registration.

```bash
: "${REG:?Set REG to the actual adopted round-5 registration identifier}"
export REG
```

P27, one regeneration command on the Mac. This also freezes complete profile overlays for the other diagnostics. A failed arm leaves explicit artifacts but no accepted full scorecard.

```bash
python scripts/r5_scorecard.py run --profile-root data/pyscf_sigma \
  --registration "$REG" --out "$WORK/scorecard"
export OPEN="$WORK/scorecard/overlays/open636"
# Outputs: scorecard_all.json/.md and scorecard_test.json/.md,
# per-model/arm CSVs, LLE control records and complete repair/status logs.
```

For staged execution rather than a nine-arm run, `freeze` replaces `run`; call `worker --run "$WORK/scorecard" --model Z0x --arm UD` and the other declared model/arm combinations, then `summarize --run "$WORK/scorecard" --split test`. Do not report missing worker output as a zero or as successful coverage. Archive the actual universe row counts and environment file with the final report.

P24, on the Mac. `R4_ARTIFACTS` must contain the native and two projected `.sigma` sets from the registered P22 run, including the separately completed Mac nonane case. The helper accepts duplicate files only when their bytes agree, and refuses missing/conflicting artifacts. Do not rerun the failed 20-GB density quadrature merely to reconstruct these already-written profiles.

```bash
: "${R4_ARTIFACTS:?Directory containing the complete P22 native/projection artifacts}"
python scripts/r5_terms.py prepare --background "$OPEN" --artifacts "$R4_ARTIFACTS" \
  --registration "$REG" --out "$WORK/terms-inputs"
python scripts/r5_terms.py run --config "$WORK/terms-inputs/config.json" \
  --out "$WORK/terms-results"
```

The six shape-only UD variants and the two charge projections are included automatically. `summary.json` reports the actual component and ES/HB changes without experimental MAE. The per-row files include endpoint-stencil controls and flag invariance. If the native panel cannot reproduce its stored source to the existing P22 tolerance, resolve the artifact provenance before interpreting sensitivity.

P25 planning and the Mac-only descriptor check:

```bash
python scripts/r5_shape.py plan --registration "$REG" --out "$WORK/shape-plan"
python scripts/r5_shape.py descriptors --manifest "$WORK/shape-plan/manifest.json" \
  --open-profiles "$OPEN" --out "$WORK/profile-descriptors.json"
export PLAN="$WORK/shape-plan"
export NATIVE="$WORK/native"
```

The manifest and its `geometries/` directory can travel together to the four-core worker. For a matrix job set `R5_SLOT` and `R5_SLOTS` before this command, for example slot numbers 0 through 19 with 20 slots. The default runs serially. Every subprocess has a one-hour deadline; a timeout/failure stops its slot and is not treated as a successful case.

```bash
python - <<'PYCODE'
import json,os,subprocess,sys
from pathlib import Path
plan=Path(os.environ['PLAN']).resolve();m=json.loads((plan/'manifest.json').read_text())
root=Path(os.environ['NATIVE']).resolve();slot=int(os.getenv('R5_SLOT','0'));slots=int(os.getenv('R5_SLOTS','1'))
assert slots>0 and 0<=slot<slots
jobs=[(r,method) for r in m['panel'] for method in ('tz_swig','svp_swig','tz_iswig')]
for j,(r,method) in enumerate(jobs):
    if j%slots!=slot:continue
    dest=root/r['key']/method;dest.parent.mkdir(parents=True,exist_ok=True)
    with (dest.parent/(method+'.log')).open('w') as log:
        subprocess.run([sys.executable,'scripts/r5_shape.py','native','--geometry',str(plan/r['geometry']),
            '--key',r['key'],'--method',method,'--memory','4000','--registration',os.environ['REG'],
            '--out',str(dest)],stdout=log,stderr=subprocess.STDOUT,check=True,timeout=3600)
PYCODE
# After collecting all slots back on the Mac:
python scripts/r5_shape.py collect --results "$NATIVE" --out "$WORK/stage-comparison.csv"
```

Existing R4 segments can be inspected without SCF with `r5_shape.py post --segments FILE --key KEY --registration "$REG" --out NEW_DIRECTORY`. That is a diagnostic of those exact bytes, not permission to silently replace the frozen R5 saved-geometry baseline. The method matrix keeps SCF and averaging interventions separate.

P26, first freeze proposals on the planner's RDKit version. This creates portable `reference.json` files beside the individual starts.

```bash
export PROPOSALS="$WORK/proposals"
python - <<'PYCODE'
import json,os,subprocess,sys
from pathlib import Path
m=json.loads((Path(os.environ['PLAN'])/'manifest.json').read_text())
for r in m['panel']:
    subprocess.run([sys.executable,'scripts/r5_conformers.py','generate',
        '--manifest',str(Path(os.environ['PLAN'])/'manifest.json'),'--panel','panel','--key',r['key'],
        '--registration',os.environ['REG'],'--out',str(Path(os.environ['PROPOSALS'])/r['key'])],check=True)
PYCODE
export CONFORMERS="$WORK/conformers"
export R5_STAGE=probe
python - <<'PYCODE'
import json,os,subprocess,sys
from pathlib import Path
jobs=[]
for p in sorted(Path(os.environ['PROPOSALS']).rglob('proposals.json')):
    d=json.loads(p.read_text())
    for c in d['cases']:
        if os.environ['R5_STAGE']=='probe' and not c['probe']:continue
        jobs.append((d['key'],p.parent/c['path']))
slot=int(os.getenv('R5_SLOT','0'));slots=int(os.getenv('R5_SLOTS','1'))
assert slots>0 and 0<=slot<slots
for j,(key,p) in enumerate(jobs):
    if j%slots!=slot:continue
    dest=Path(os.environ['CONFORMERS'])/key/p.stem;dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists():
        # Reuse only in a separately authorized full-stage continuation; select verifies the input hash.
        if os.environ['R5_STAGE']=='full':continue
        raise FileExistsError(dest)
    with (dest.parent/(p.stem+'.log')).open('w') as log:
        subprocess.run([sys.executable,'scripts/r5_conformers.py','optimize','--input',str(p),
            '--memory','4000','--registration',os.environ['REG'],'--out',str(dest)],
            stdout=log,stderr=subprocess.STDOUT,check=True,timeout=3600)
PYCODE
```

After artifact collection, create one selection record per non-rigid member. The command deliberately requires all expected proposal results and the frozen native reference.

```bash
mkdir -p "$WORK/probe-selections"
python - <<'PYCODE'
import json,os,subprocess,sys
from pathlib import Path
for p in sorted(Path(os.environ['PROPOSALS']).rglob('proposals.json')):
    d=json.loads(p.read_text())
    if d['rigid']:continue
    k=d['key']
    subprocess.run([sys.executable,'scripts/r5_conformers.py','select','--proposals',str(p),
        '--results',str(Path(os.environ['CONFORMERS'])/k),'--stage','probe',
        '--reference-native',str(Path(os.environ['NATIVE'])/k/'tz_swig/native.json'),
        '--registration',os.environ['REG'],'--out',str(Path(os.environ['WORK'])/'probe-selections'/(k+'.json'))],check=True)
PYCODE
```

The `low_energy_shape_sensitive_pairs` records decide whether the fixed trigger was observed; they do not pick the closest UD profile. Conditional continuation uses the same proposal files with `R5_STAGE=full`, not a new seed. For the separate eight-member validation panel, run `generate --panel validation` from the same manifest, then the same optimizer loop at `full`. Compute its eight saved-geometry `tz_swig` reference single points with the same P25 native command. Call `select --stage full` for every member into a dedicated validation-selection directory. Then the implemented gate is:

```bash
python scripts/r5_conformers.py gate --manifest "$PLAN/manifest.json" \
  --selections "$WORK/validation-selections" --background "$OPEN" \
  --registration "$REG" --out "$WORK/conformer-validation"
```

A missing member, a censored native job, an internal reproducibility failure or nonfinite affinity probe blocks acceptance. Every selected pool and its frozen input hash remains auditable. No command here copies selected profiles into `profiles_v2`.

## Portable verification and remaining limitations

The supplied test checked proper alignment to `7.77e-16 Å`, exact compressed patch subdivision to `1.73e-18`, linear-bin area conservation exactly in the fixture and first-moment conservation to `6.94e-18`, HB binwise conservation to `4.44e-16`, and the common-label ES identity above. Real SciPy bounded least squares was exercised on synthetic ideal/regular-solution models. A separate synthetic nine-arm report test verified row reordering, S1/S2 exclusion and the distinction between a gap witness and a checked endpoint denominator. These tests do not establish real-model finite coverage or phase-diagram completeness.

The requested native four-core tests and all Mac-only UD-backed results still decide scientific acceptance. The real 859-row term attribution, which controls show averaging sensitivity, whether the conditional conformer trigger occurs, and the regenerated VLE/HE figures are not known from this review. No native measurement, historical-cause identification or improved benchmark score is claimed in their absence.

The report's scientific conclusions that do not require another native run are narrower and useful: H2O flags cannot cause a London-Z0x shape substitution; fixed-A/V charge projections change its residual term; the HB redistribution cannot change total sigma-bin area; common ES label shifts have an exact cancellation; and existing final UD bins do not uniquely identify their missing generating conformer or cavity. Those conclusions determine which measurements are worth funding with the free compute budget.

## Full extractable patches


### H5

<!-- PATCH:H5 -->
```diff
--- /dev/null
+++ b/scripts/r5_common.py
@@ -0,0 +1,126 @@
+"""Round-5 read-only experiment utilities. No production model is patched."""
+from __future__ import annotations
+import hashlib
+import json
+from pathlib import Path
+import numpy as np
+import pandas as pd
+from scipy.spatial.distance import cdist
+from r3_common import digest, read_sigma, write_json, STALL_KEYS
+
+BASE = '69b49116c2ae7574d7ae471f0a4ed7ba33d0db8b'
+PANEL = (
+ ('water','O'), ('methanol','CO'), ('ethylene_glycol','OCCO'),
+ ('diethylene_glycol','OCCOCCO'), ('triethylene_glycol','OCCOCCOCCO'),
+ ('tetraethylene_glycol','OCCOCCOCCOCCO'), ('glycerol','OCC(O)CO'),
+ ('propylene_glycol','CC(O)CO'), ('methoxyethanol','COCCO'),
+ ('dimethoxyethane','COCCOC'), ('tetrahydrofuran','C1CCOC1'),
+ ('nonane','CCCCCCCCC'))
+
+
+def fresh(path):
+    p=Path(path).resolve()
+    if p.exists(): raise FileExistsError(f'use a new output path: {p}')
+    p.mkdir(parents=True)
+    return p
+
+
+def require_registration(value):
+    if not str(value).strip(): raise ValueError('record the prospective registration identifier')
+    return str(value)
+
+
+def fingerprint(paths):
+    return {str(Path(p).resolve()):digest(p) for p in paths}
+
+
+def check_fingerprint(record):
+    for p,h in record.items():
+        if digest(p)!=h: raise ValueError(f'input changed: {p}')
+
+
+def canonical_smiles(s):
+    from rdkit import Chem
+    m=Chem.MolFromSmiles(s)
+    if m is None: raise ValueError(s)
+    return Chem.MolToSmiles(m,isomericSmiles=True)
+
+
+def align(x, reference, indices=None):
+    """Proper Kabsch alignment in the fixed atom order; not atom permutation."""
+    x=np.asarray(x,float); y=np.asarray(reference,float)
+    if x.shape!=y.shape or x.ndim!=2 or x.shape[1]!=3: raise ValueError('coordinate mismatch')
+    if not np.isfinite(x).all() or not np.isfinite(y).all(): raise ValueError('nonfinite coordinates')
+    ii=np.arange(len(x)) if indices is None else np.asarray(indices,int)
+    a=x[ii].mean(0);b=y[ii].mean(0)
+    u,_,vt=np.linalg.svd((x[ii]-a).T@(y[ii]-b))
+    d=np.ones(3);d[-1]=1. if np.linalg.det(u@vt)>=0 else -1.
+    return (x-a)@(u@np.diag(d)@vt)+b
+
+
+def rmsd(x,y,indices=None):
+    ii=np.arange(len(x)) if indices is None else np.asarray(indices,int)
+    return float(np.sqrt(np.mean(np.sum((align(x,y,ii)[ii]-np.asarray(y)[ii])**2,axis=1))))
+
+
+def charge_average(xyz_A, area_A2, sigma, subdivision=1., block=128):
+    """Hsieh formula; infinity is an A point-patch-limit sensitivity, not a new default.
+
+    subdivision m is algebraically the result of replacing each patch by m
+    coincident patches with A/m and q/m. It is not a physical surface remesh.
+    """
+    x=np.asarray(xyz_A,float);a=np.asarray(area_A2,float);s=np.asarray(sigma,float)
+    if x.shape!=(len(a),3) or s.shape!=a.shape or np.any(a<=0): raise ValueError('invalid segments')
+    if not (np.isfinite(x).all() and np.isfinite(a).all() and np.isfinite(s).all()): raise ValueError('nonfinite segments')
+    if subdivision not in (1.,4.,np.inf): raise ValueError('fixed diagnostic subdivisions are 1, 4, infinity')
+    rav2=7.25/np.pi; rn2=np.zeros_like(a) if np.isinf(subdivision) else a/(np.pi*subdivision)
+    # Constants independent of j cancel between numerator and denominator.
+    pref=a/(rn2+rav2);out=np.empty_like(s)
+    for lo in range(0,len(a),block):
+        w=np.exp(-3.57*cdist(x[lo:lo+block],x,'sqeuclidean')/(rn2+rav2))*pref
+        out[lo:lo+block]=(w@s)/w.sum(1)
+    return out
+
+
+def bin_linear(sigma, area, grid):
+    """Independent mass/first-moment preserving interpolation; no clipping."""
+    s=np.asarray(sigma,float);a=np.asarray(area,float);g=np.asarray(grid,float)
+    if s.shape!=a.shape or np.any(a<0) or not np.isfinite(s).all(): raise ValueError('invalid bin inputs')
+    if np.any(s<g[0]-1e-12) or np.any(s>g[-1]+1e-12): raise ValueError('out-of-range sigma, do not clip')
+    # Tiny endpoint roundoff only. A genuinely out-of-range value already failed.
+    s=np.minimum(np.maximum(s,g[0]),g[-1]);j=np.searchsorted(g,s,side='right')-1
+    j=np.minimum(j,len(g)-2);t=(s-g[j])/(g[j+1]-g[j]);p=np.zeros_like(g)
+    np.add.at(p,j,a*(1-t));np.add.at(p,j+1,a*t)
+    return p
+
+
+def observation_ids(df, table):
+    """Identity from source observations only, independent of predictions and row order."""
+    required={'idac':['file','dataset','solute','solvent','T','ln_gamma_inf','split'],
+              'vle':['file','dataset','c1','c2','T','x1','P','split'],
+              'he':['file','dataset','c1','c2','T','x1','HE_J','split'],
+              'lle':['file','dataset','c1','c2','T','x1','split']}[table]
+    if set(required)-set(df): raise ValueError(f'{table}: missing identity fields {set(required)-set(df)}')
+    cols=required+[c for c in ('year','method','gamma_inf','y1','P','temporal') if c in df and c not in required]
+    def value(v):
+        if pd.isna(v): return None
+        if isinstance(v,(float,np.floating)): return format(float(v),'.15g')
+        return str(v)
+    keys=pd.Series([hashlib.sha256(json.dumps([value(v) for v in row],separators=(',',':')).encode()).hexdigest()
+                    for row in df[cols].itertuples(index=False,name=None)],index=df.index)
+    return (keys+':'+keys.groupby(keys).cumcount().astype(str)).to_numpy()
+
+
+def pairs(df,table):
+    return ('solute','solvent') if table=='idac' else ('c1','c2')
+
+
+def systems(df,table):
+    a,b=pairs(df,table);x=df[a].to_numpy(str);y=df[b].to_numpy(str)
+    return np.where(x<y,x+'|'+y,y+'|'+x)
+
+
+def subset(df, split):
+    if df['split'].isna().any() or not df['split'].isin(['train','test_one','test_both']).all():
+        raise ValueError('invalid split labels')
+    return df if split=='all' else df[df['split']!='train'] if split=='test' else df[df['split']==split]
--- /dev/null
+++ b/scripts/r5_selftest.py
@@ -0,0 +1,115 @@
+"""Portable R5 tests. Synthetic data and RDKit proposals, never native QC acceptance."""
+from __future__ import annotations
+import argparse
+import json
+from pathlib import Path
+import tempfile
+import time
+import numpy as np
+import pandas as pd
+from scipy.spatial.transform import Rotation
+from r3_common import write_json
+from r5_common import align,rmsd,charge_average,bin_linear,observation_ids
+from r5_terms import stencil,compare
+from r4_lle import strict_binodal,bounds
+
+
+def coefficients(E,p):
+    G=np.ones(len(p))
+    for _ in range(10000):
+        Gn=1/(E@(p*G));nextG=.5*(G+Gn)
+        if np.max(abs(np.log(nextG/G)))<1e-13:return nextG
+        G=nextG
+    raise AssertionError('test segment solver did not converge')
+
+
+def gauge_test():
+    # Shift the labels, not an interpolated/binned approximation to their distributions.
+    rng=np.random.default_rng(12);s=np.linspace(-.02,.02,17);c=8000.;RT=.593;shift=.0004
+    p=rng.random(17);p/=p.sum();q=rng.random(17);q/=q.sum();mix=.3*p+.7*q
+    E=np.exp(-c*(s[:,None]+s[None,:])**2/RT)
+    Et=np.exp(-c*(s[:,None]+s[None,:]+2*shift)**2/RT)
+    a=4*c*shift*s+2*c*shift**2;factor=np.exp(-a/RT)
+    err=float(abs(Et-E*factor[:,None]*factor[None,:]).max())
+    gm,gp=coefficients(E,mix),coefficients(E,p)
+    hm,hp=coefficients(Et,mix),coefficients(Et,p)
+    residual=float(abs(p@(np.log(gm)-np.log(gp))-p@(np.log(hm)-np.log(hp))))
+    if err>1e-12 or residual>1e-10:raise AssertionError('common-shift gauge identity failed')
+    return dict(kernel_error=err,residual_error=residual)
+
+
+def tests():
+    rng=np.random.default_rng(7);x=rng.normal(size=(11,3));R=Rotation.random(random_state=13).as_matrix()
+    y=x@R+np.array([4.,-2.,1.]);alignment=float(abs(align(y,x)-x).max())
+    if alignment>1e-12:raise AssertionError('Kabsch rotation failure')
+    area=rng.uniform(.05,2.,11);sig=rng.uniform(-.02,.02,11)
+    v=charge_average(x,area,sig,4.)
+    # Literal four-way duplication is an independent check of the algebraic compressed formula.
+    xx=np.repeat(x,4,axis=0);aa=np.repeat(area/4,4);ss=np.repeat(sig,4)
+    literal=charge_average(xx,aa,ss,1.)[::4]
+    subdivision=float(abs(v-literal).max())
+    if subdivision>1e-12:raise AssertionError('patch-subdivision identity failed')
+    grid=np.linspace(-.025,.025,51);p=bin_linear(sig,area,grid)
+    mass=float(abs(p.sum()-area.sum()));moment=float(abs(p@grid-area@sig))
+    if max(mass,moment)>1e-12:raise AssertionError('bin mass/moment failure')
+    hb=rng.uniform(0,.5,(2,51));pre=rng.uniform(0,1,(3,51));ph=1-np.exp(-grid**2/(2*.007**2))
+    post=pre.copy();post[1:]*=ph;post[0]+=(pre[1]+pre[2])*(1-ph)
+    split=float(abs(post.sum(0)-pre.sum(0)).max())
+    if split>1e-12:raise AssertionError('HB conservation identity failure')
+    p0=np.array([0.,0.,0.]);phs=np.array([2.,3.,5.])*1e-4
+    if not np.allclose(stencil(p0,phs,1e-4),[2,3,5]):raise AssertionError('endpoint component algebra')
+    base=pd.DataFrame(dict(file=['a','b'],dataset=[1,2],solute=['x','y'],solvent=['z','z'],T=[298.,300.],
+           ln_gamma_inf=[1.,2.],split=['train','test_one']))
+    ids=observation_ids(base,'idac');reverse=observation_ids(base.iloc[::-1].reset_index(drop=True),'idac')
+    if list(ids)!=list(reverse[::-1]):raise AssertionError('observation ids depend on row order')
+    r=pd.DataFrame(dict(r5_row_id=['a','b'],solute=['x','y'],solvent=['z','z'],T=[298.,300.],
+        total=[3.,4.],comb=[1.,1.],residual=[1.,2.],london=[1.,1.],kernel_00=[0.,0.],
+        kernel_10=[.4,.5],kernel_01=[.4,.5],kernel_11=[1.,2.],endpoint_stencil_error=[.01,.01]))
+    c=r.copy();c['total']+=.1;c['residual']+=.1;c['kernel_11']+=.1
+    d=compare(r,c.iloc[::-1]);assert abs(d.ES_shapley+d.HB_shapley-.1).max()<1e-12
+    bad=c.copy();bad.loc[0,'total']=np.nan
+    try:compare(r,bad)
+    except ValueError:pass
+    else:raise AssertionError('finite coverage guard failed')
+    class Ideal:
+        def lngamma(self,T,x):return np.zeros(2)
+    class Regular:
+        def lngamma(self,T,x):return np.array([3*x[1]**2,3*x[0]**2])
+    ideal=strict_binodal(Ideal(),298.15);regular=strict_binodal(Regular(),298.15)
+    if ideal['status']!='no_gap_on_refined_grid' or regular['status']!='root_passes_refined_sampled_checks':
+        raise AssertionError('real SciPy synthetic LLE check failed')
+    b=bounds([1.,np.nan,0.,1.],['a','a','b','b'])
+    if b['row_gap_found_bounds']!=[.5,.75] or b['unresolved_rows']!=1:raise AssertionError('denominator bounds failed')
+    # Exercise the actual report's endpoint denominator with a witness and an unknown.
+    from r5_scorecard import lle_metrics
+    q=pd.DataFrame(dict(c1=['a']*4,c2=['b']*4,r5_detection=[1.,1.,0.,np.nan],x1=[.1,.2,.3,.4],
+        r5_x1_I=[.1,np.nan,np.nan,np.nan],r5_x1_II=[.9,np.nan,np.nan,np.nan],
+        r5_lle_status=['root_passes_sampled_checks','gap_witness_only','no_gap_on_81_grid','unresolved'],pred_split=[1.,1.,0.,1.]))
+    lm=lle_metrics(q)
+    if lm['endpoint_rows']!=1 or lm['rows']!=4 or lm['unresolved_rows']!=1:raise AssertionError('witness leaked into endpoint MAE')
+    return dict(alignment_error_A=alignment,subdivision_error=subdivision,bin_mass_error=mass,
+        bin_moment_error=moment,HB_total_bin_error=split,gauge=gauge_test(),
+        ideal_status=ideal['status'],regular_status=regular['status'],denominator_checks='passed',
+        scope='Portable synthetic checks, not native quantum chemistry or production score acceptance.')
+
+
+def rdkit_test():
+    from rdkit import Chem,rdBase
+    from rdkit.Chem import AllChem
+    from r5_conformers import proposal_pool
+    m=Chem.AddHs(Chem.MolFromSmiles('OCCO'));p=AllChem.ETKDGv3();p.randomSeed=7
+    if AllChem.EmbedMolecule(m,p)!=0:raise AssertionError('test reference failed to embed')
+    x=m.GetConformer().GetPositions();t=time.perf_counter()
+    _,a=proposal_pool('OCCO',x,20261005);_,b=proposal_pool('OCCO',x,20261005)
+    error=max(float(abs(u['x']-v['x']).max()) for u,v in zip(a,b))
+    if error!=0. or [u['cid'] for u in a]!=[u['cid'] for u in b]:raise AssertionError('proposal reproducibility failed')
+    return dict(rdkit=rdBase.rdkitVersion,molecule='synthetic EG start',pools=2,selected_per_pool=len(a),
+         max_coordinate_difference_A=error,wall_s=time.perf_counter()-t,scope='proposal generation only, no DFT')
+
+
+def main():
+    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--rdkit',action='store_true');a=p.parse_args()
+    d=tests()
+    if a.rdkit:d['RDKit']=rdkit_test()
+    write_json(a.out,d);print(json.dumps(d,indent=2))
+if __name__=='__main__':main()
```

### P24

<!-- PATCH:P24 -->
```diff
--- /dev/null
+++ b/scripts/r5_terms.py
@@ -0,0 +1,210 @@
+"""E accounting of actual Z0x IDAC; A ES/HB interventions used only diagnostically.
+
+Run a separate worker per frozen profile set. No fitting, no table writes.
+A component decomposition is additive; ES and HB Shapley attributions are not
+claimed to be separately measurable physical free energies.
+"""
+from __future__ import annotations
+import argparse
+from dataclasses import replace
+import json
+import os
+from pathlib import Path
+import subprocess
+import sys
+import shutil
+import numpy as np
+import pandas as pd
+from r3_common import digest, write_json
+from r5_common import fresh, observation_ids, fingerprint, check_fingerprint, require_registration
+
+
+def stencil(parts0, partsh, h):
+    return np.asarray(parts0)+(np.asarray(partsh)-np.asarray(parts0))/h
+
+
+def account(model,T,es=True,hb=True,h=None,flags=False):
+    from zcosmo.cosmosac import Mixture
+    h=model.H if h is None else h
+    pieces=[];limits=[]
+    for x0 in (0.,h):
+        x=np.array([x0,1-x0]);c=model._c(x0)
+        # Preserve the actual rounded-c cache convention when establishing parity.
+        model._frozen(T,x0,c); original=model._mix[round(c,6)]
+        prm=original.prm.with_(A_ES=original.prm.A_ES if es else 0.,
+             B_ES=original.prm.B_ES if es else 0.,
+             c_OH_OH=original.prm.c_OH_OH if hb else 0.,
+             c_OT_OT=original.prm.c_OT_OT if hb else 0.,
+             c_OH_OT=original.prm.c_OH_OT if hb else 0.)
+        fl=original.fl if not flags else [replace(f,disp_flag='NHB') for f in original.fl]
+        mix=Mixture(None,prm,fluids=fl)
+        terms=np.array([mix.lngamma_comb(x),mix.lngamma_resid(T,x),mix.lngamma_disp(x,T)])
+        pieces.append(terms@x)
+        if x0==0.: limits=terms[:,0]
+    out=stencil(pieces[0],pieces[1],h)
+    return out,np.asarray(limits)
+
+
+def worker(a):
+    config=json.loads(Path(a.config).read_text()); spec=config['variants'][a.variant]
+    for name in ('ZC_SIGMA_OVERRIDE_DIR','ZC_ONLY_KEYS'): os.environ.pop(name,None)
+    if spec.get('directory'): os.environ['ZC_SIGMA_OVERRIDE_DIR']=str(Path(spec['directory']).resolve())
+    from zcosmo.cosmosac import sigma_path
+    from zcosmo.models import make_model
+    rows=pd.read_csv(config['rows'])
+    if 'r5_row_id' not in rows: rows['r5_row_id']=observation_ids(rows,'idac')
+    if rows.r5_row_id.duplicated().any(): raise ValueError('duplicate row ids')
+    compounds=pd.read_csv(config.get('compounds','data/benchmark/compounds.csv'))
+    smi=dict(zip(compounds.inchikey,compounds.smiles));cache={};records=[];inputs={};max_parity=0.;max_flag=0.
+    for r in rows.itertuples():
+        key=(r.solute,r.solvent)
+        for k in key:
+            p=sigma_path(k)
+            if p is None: raise FileNotFoundError(k)
+            # Open overlays must be complete for the supplied queries, not mixed with UD by accident.
+            if spec.get('directory') and p.resolve()!=(Path(spec['directory'])/f'{k}.sigma').resolve():
+                raise ValueError(f'profile fallback in {a.variant}: {k}')
+            inputs[str(p.resolve())]=digest(p)
+        rec=dict(r5_row_id=r.r5_row_id,solute=r.solute,solvent=r.solvent,T=float(r.T),error='')
+        try:
+            if key not in cache: cache[key]=make_model('Z0x',list(key),[smi[k] for k in key])
+            m=cache[key]
+            actual=float(m.lngamma_inf(r.T,0));base,lim=account(m,r.T)
+            discrepancy=abs(base.sum()-actual)
+            if not np.isfinite(actual) or not np.isfinite(base).all(): raise ValueError('nonfinite Z0x query')
+            if discrepancy>1e-9: raise AssertionError(f'component parity failure: {discrepancy}')
+            max_parity=max(max_parity,discrepancy)
+            flag,_=account(m,r.T,flags=True);max_flag=max(max_flag,float(abs(flag-base).max()))
+            if np.max(abs(flag-base))>1e-10: raise AssertionError('H2O/COOH flags reached London Z0x')
+            try:
+                dsp=make_model('cosmosac_dsp',list(key),[smi[k] for k in key]).lngamma_inf(r.T,0)
+            except Exception: dsp=np.nan
+            rec.update(dsp_total=float(dsp),total=actual,comb=float(base[0]),residual=float(base[1]),london=float(base[2]),
+                       exact_limit=float(lim.sum()),endpoint_stencil_error=float(actual-lim.sum()),
+                       solvent_c_ES=float(m._c(0.)),flag_change=float(flag.sum()-actual))
+            for es,hb in ((False,False),(True,False),(False,True),(True,True)):
+                q,_=account(m,r.T,es,hb)
+                rec[f'kernel_{int(es)}{int(hb)}']=float(q[1])
+            for h in (1e-5,1e-6):
+                q,_=account(m,r.T,h=h);rec[f'stencil_{h:g}']=float(q.sum())
+        except AssertionError: raise
+        except Exception as e:
+            rec['error']=type(e).__name__+': '+str(e)
+        records.append(rec)
+    out=Path(a.out);pd.DataFrame(records).to_csv(out,index=False)
+    check_fingerprint(inputs)
+    write_json(str(out)+'.json',dict(variant=a.variant,profile_inputs=inputs,rows=len(rows),
+        max_parity=max_parity,max_flag=max_flag,registration=config['registration']))
+
+
+def compare(reference,candidate):
+    r=reference.set_index('r5_row_id');c=candidate.set_index('r5_row_id')
+    if not r.index.is_unique or set(r.index)!=set(c.index): raise ValueError('query identity mismatch')
+    c=c.loc[r.index];required=['total','comb','residual','london','kernel_00','kernel_10','kernel_01','kernel_11']
+    if any(k not in r or k not in c for k in required): raise ValueError('no evaluable component rows')
+    finite=np.isfinite(r[required].to_numpy(float)).all(1)
+    if not np.array_equal(finite,np.isfinite(c[required].to_numpy(float)).all(1)):
+        raise ValueError('finite coverage differs; do not interpret a partial effect as the original panel')
+    out=c[['solute','solvent','T']].copy();out['finite_all']=finite
+    for k in required+['endpoint_stencil_error']:
+        out['delta_'+k]=c[k]-r[k]
+    d={k:out['delta_kernel_'+k] for k in ('00','10','01','11')}
+    out['ES_shapley']=.5*((d['10']-d['00'])+(d['11']-d['01']))
+    out['HB_shapley']=.5*((d['01']-d['00'])+(d['11']-d['10']))
+    if finite.any():
+        err=out.ES_shapley+out.HB_shapley-(d['11']-d['00'])
+        if abs(err[finite]).max()>1e-10: raise AssertionError('ES/HB identity failed')
+        additive=out.delta_comb+out.delta_residual+out.delta_london-out.delta_total
+        if abs(additive[finite]).max()>2e-9: raise AssertionError('component identity failed')
+    return out
+
+
+def run(a):
+    cfg=json.loads(Path(a.config).read_text());require_registration(cfg['registration'])
+    if 'inputs' in cfg: check_fingerprint(cfg['inputs'])
+    if 'reference' not in cfg['variants']: raise ValueError('name the reference variant explicitly')
+    out=fresh(a.out);frames={}
+    for v in cfg['variants']:
+        p=out/(v+'.csv')
+        subprocess.run([sys.executable,str(Path(__file__).resolve()),'worker','--config',str(Path(a.config).resolve()),
+                        '--variant',v,'--out',str(p)],check=True)
+        frames[v]=pd.read_csv(p)
+    summaries=[]
+    for v in frames:
+        if v=='reference': continue
+        d=compare(frames['reference'],frames[v]);d.to_csv(out/(v+'-delta.csv'))
+        for solvent,g in [('ALL',d)]+list(d.groupby('solvent',sort=True)):
+            good=g[g.finite_all]
+            s=dict(variant=v,solvent=solvent,rows=len(g),finite=len(good))
+            for k in ('delta_total','delta_comb','delta_residual','delta_london','ES_shapley','HB_shapley','delta_endpoint_stencil_error'):
+                s[k+'_mean']=float(good[k].mean()) if len(good) else None
+                s[k+'_mean_abs']=float(good[k].abs().mean()) if len(good) else None
+                s[k+'_max_abs']=float(good[k].abs().max()) if len(good) else None
+            summaries.append(s)
+    write_json(out/'summary.json',dict(config_sha256=digest(a.config),registration=cfg['registration'],
+        summaries=summaries,note='No experimental response is used; four kernels are diagnostic interventions.'))
+
+
+
+def prepare(a):
+    """Freeze the P22 projection panel plus six one-profile UD-shape probes on the Mac."""
+    from r3_common import read_sigma,write_sigma
+    require_registration(a.registration);out=fresh(a.out)
+    root=Path(a.artifacts).resolve();background=Path(a.background).resolve()
+    keys=('LYCAIKOWRPUZTN-UHFFFAOYSA-N','MTHSVFCYNBDYFN-UHFFFAOYSA-N',
+          'ZIBGPFATKBEMQZ-UHFFFAOYSA-N','OKKJLVBELUTLKV-UHFFFAOYSA-N',
+          'XLYOFNOQVPJJNP-UHFFFAOYSA-N','BKIMMITUMNQMOS-UHFFFAOYSA-N')
+    d=pd.read_csv(a.idac);d=d[d.solute.isin(keys)|d.solvent.isin(keys)].copy()
+    d['r5_row_id']=observation_ids(d,'idac')
+    if len(d)!=859: raise ValueError('P22 frozen panel is not 859 rows; resolve the input version')
+    # Experimental responses are deliberately not passed to the term workers.
+    rows=out/'queries.csv';d[['r5_row_id','solute','solvent','T']].to_csv(rows,index=False)
+    inputs=fingerprint([a.idac,a.compounds]);paths={}
+    for key in keys:
+        for variant in ('native','area_zero','capacitary_zero'):
+            hits=[p for p in root.rglob(key+'.sigma') if
+                  (p.parent.name==variant if variant!='native' else p.parent.name not in ('area_zero','capacitary_zero'))]
+            # A repeated identical artifact is acceptable; conflicting native outputs are not.
+            hashes={digest(p) for p in hits}
+            if len(hashes)!=1: raise ValueError(f'{key}/{variant}: missing or conflicting artifacts')
+            paths[key,variant]=sorted(hits)[0].resolve();inputs[str(paths[key,variant])]=next(iter(hashes))
+    source={p.stem:p.resolve() for p in background.glob('*.sigma')}
+    needed=set(d[['solute','solvent']].to_numpy().ravel())
+    if needed-set(source): raise ValueError('background is incomplete; no UD fallback is authorized')
+    variants={}
+    for name,kind in [('reference','native'),('area_zero','area_zero'),('capacitary_zero','capacitary_zero')]:
+        folder=out/name;folder.mkdir()
+        for key in needed:
+            p=paths[key,kind] if key in keys else source[key]
+            (folder/(key+'.sigma')).symlink_to(p);inputs[str(p)]=digest(p)
+        variants[name]={'directory':str(folder)}
+    os.environ.pop('ZC_SIGMA_OVERRIDE_DIR',None)
+    from zcosmo.cosmosac import sigma_path,SIGMA_DIR
+    if not SIGMA_DIR.is_dir(): raise FileNotFoundError('UD-shape diagnostics require Mac-only UD assets')
+    for key in keys:
+        folder=out/('UDshape_'+key[:14]);folder.mkdir()
+        for other in needed:
+            if other!=key: (folder/(other+'.sigma')).symlink_to(out/'reference'/(other+'.sigma'))
+        sig,po,meta=read_sigma(out/'reference'/(key+'.sigma'));ud=sigma_path(key)
+        if ud is None: raise FileNotFoundError(key)
+        _,pu,_=read_sigma(ud);inputs[str(Path(ud).resolve())]=digest(ud)
+        meta.update(source='R5 shape-only diagnostic; original area/volume/metadata retained')
+        write_sigma(folder/(key+'.sigma'),sig,pu/pu.sum()*po.sum(),meta)
+        variants[folder.name]={'directory':str(folder)}
+    inputs.update(fingerprint(['results/qc/dielectric.csv','results/qc/dispersion.csv','results/z_params/Z0.json',
+          'src/zcosmo/cosmosac.py','src/zcosmo/z0x.py',str(rows)]))
+    write_json(out/'config.json',dict(variants=variants,rows=str(rows),compounds=str(Path(a.compounds).resolve()),
+         registration=a.registration,inputs=inputs,keys=keys,
+         note='P22 panel; one fresh worker per immutable profile overlay; no experimental response in queries.'))
+
+
+def main():
+    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
+    for name in ('run','worker'):
+        q=s.add_parser(name);q.add_argument('--config',required=True);q.add_argument('--out',required=True)
+        if name=='worker': q.add_argument('--variant',required=True)
+    q=s.add_parser('prepare');q.add_argument('--background',required=True);q.add_argument('--artifacts',required=True)
+    q.add_argument('--out',required=True);q.add_argument('--registration',required=True)
+    q.add_argument('--idac',default='data/benchmark/idac.csv');q.add_argument('--compounds',default='data/benchmark/compounds.csv')
+    a=p.parse_args();globals()[a.cmd](a)
+if __name__=='__main__':main()
```

### P25

<!-- PATCH:P25 -->
```diff
--- /dev/null
+++ b/scripts/r5_shape.py
@@ -0,0 +1,183 @@
+"""Fixed structural panel, crossed quantum settings, and stage-resolved sigma profiles.
+
+No UD geometry is invented. No profile recipe is selected by experimental error.
+The point-patch limit is an A diagnostic of Hsieh averaging, never a default.
+"""
+from __future__ import annotations
+import argparse
+import json
+from pathlib import Path
+import os
+import time
+import numpy as np
+import pandas as pd
+from r3_common import digest, read_sigma, write_sigma, write_json, profile_descriptors
+from r4_common import geometry, structure, contacts, parser_trace, selected_profiles
+from r5_common import (BASE,PANEL,fresh,canonical_smiles,charge_average,bin_linear,
+                       require_registration,check_fingerprint)
+
+
+def plan(a):
+    from rdkit import Chem, rdBase
+    compounds=pd.read_csv(a.compounds)
+    if compounds.inchikey.duplicated().any(): raise ValueError('duplicate compound keys')
+    by={}
+    for r in compounds.itertuples(): by.setdefault(canonical_smiles(r.smiles),[]).append(r)
+    panel=[]
+    for name,s in PANEL:
+        match=by.get(canonical_smiles(s),[])
+        if len(match)>1:
+            expected=Chem.MolToInchiKey(Chem.MolFromSmiles(s))
+            match=[r for r in match if r.inchikey==expected]
+        if len(match)!=1: raise ValueError(f'{name}: expected one exact stereo-aware SMILES match, got {len(match)}')
+        r=match[0];panel.append(dict(name=name,key=r.inchikey,smiles=r.smiles,**structure(r.smiles)))
+    historical=set(pd.read_csv('results/pyscf_profile_validation.csv',usecols=['key']).key)
+    excluded=historical|{r['key'] for r in panel};eligible=[]
+    import hashlib
+    for r in compounds.itertuples():
+        st=structure(r.smiles);m=Chem.MolFromSmiles(r.smiles)
+        if r.inchikey in excluded or st['heavy_atoms']>13 or st['rotatable_bonds']<2: continue
+        if (len(Chem.GetMolFrags(m))!=1 or any(x.GetAtomicNum() not in (1,6,8) or
+             x.GetFormalCharge()!=0 or x.GetNumRadicalElectrons()!=0 for x in m.GetAtoms())): continue
+        if st['OH_count']<2 and st['ether_count']<1: continue
+        eligible.append(dict(name=r.inchikey,key=r.inchikey,smiles=r.smiles,**st,
+            order=hashlib.sha256(('R5-validation-v1|'+r.inchikey).encode()).hexdigest()))
+    eligible.sort(key=lambda r:r['order'])
+    if len(eligible)<8: raise ValueError('fewer than eight separate validation members; no substitution rule is authorized')
+    validation=eligible[:8];gm=json.loads(Path(a.geometry_map).read_text()) if a.geometry_map else {}
+    out=fresh(a.out)
+    for r in panel+validation:
+        k=r['key'];p=Path(gm[k]) if k in gm else Path(a.geometry_dir)/(k+'.xyz.json')
+        if not p.is_file():
+            alt=Path('cloud/r4/native')/(k+'.open.json')
+            if alt.is_file(): p=alt
+            else: raise FileNotFoundError(f'{k}: provide the saved generating geometry; no re-embedding fallback')
+        sym,x=geometry(p);m=Chem.AddHs(Chem.MolFromSmiles(r['smiles']))
+        if sym!=[at.GetSymbol() for at in m.GetAtoms()]: raise ValueError(f'{k}: atom order differs')
+        dest=out/'geometries'/(k+'.json')
+        write_json(dest,dict(sym=sym,x=x.tolist()))
+        r.update(geometry=str(dest.relative_to(out)),geometry_sha256=digest(dest),source_geometry=str(p.resolve()),
+                 source_sha256=digest(p),spin=0)
+    manifest=dict(base=BASE,registration=require_registration(a.registration),panel=panel,validation=validation,
+        selection='fixed homologues/branched/rigid controls; validation first 8 SHA-ordered eligible structures, excluding panel and historical 25',
+        compounds=str(Path(a.compounds)),compounds_sha256=digest(a.compounds),rdkit=rdBase.rdkitVersion)
+    write_json(out/'manifest.json',manifest)
+    print(json.dumps({'panel_keys':[r['key'] for r in panel],'validation_keys':[r['key'] for r in validation]},indent=2))
+
+
+def process(sym,x,seg,out,key,registration):
+    from zcosmo.pyscf_cosmo import BOHR
+    p,reference,trace=parser_trace(sym,x,seg)
+    arr=lambda o:np.stack([o.psigmaA_nhb,o.psigmaA_OH,o.psigmaA_OT])
+    original=arr(reference);grid=reference.sigmas;area=seg['area'];raw=seg['q']/area
+    independent=charge_average(seg['xyz']*BOHR,area,raw,1.)
+    discrepancy=float(abs(independent-p.sigma_averaged).max())
+    if discrepancy>1e-10: raise AssertionError('independent Hsieh formula failed parity')
+    base_total=bin_linear(p.sigma_averaged,area,grid)
+    if abs(original.sum(0)-base_total).max()>1e-8: raise AssertionError('HB split changed total bin distribution')
+    report={'key':key,'registration':registration,'native_trace':trace,'geometry_contacts':contacts(sym,x),
+            'Hsieh_parity_e_A2':discrepancy,'raw_abs_tail_A2':float(area[abs(raw)>=.01].sum()),
+            'raw_second_moment':float(area@(raw*raw)/area.sum()),'variants':{}}
+    for label,m in [('hsieh',1.),('coincident4',4.),('point_limit',np.inf)]:
+        avg=charge_average(seg['xyz']*BOHR,area,raw,m)
+        p.sigma_averaged=avg
+        p.sigma_nhb,p.sigma_OH,p.sigma_OT=p.split_profiles(avg,3)
+        z=p.get_outputs();ps=arr(z);total=bin_linear(avg,area,z.sigmas)
+        if abs(ps.sum(0)-total).max()>1e-8: raise AssertionError('binwise conservation failure')
+        meta=dict(z.meta);meta.update(source='R5 stage diagnostic, not adopted',r5_recipe=label,
+            r5_registration=registration,geometry_converged='R5-frozen')
+        ek=meta.get('disp. e/kB [K]')
+        if ek is not None and not np.isfinite(ek): meta['disp. e/kB [K]']=None
+        path=out/label/(key+'.sigma');write_sigma(path,z.sigmas,ps,meta)
+        pre=np.array([bin_linear(v[:,0],v[:,1],grid) for v in (p.sigma_nhb,p.sigma_OH,p.sigma_OT)])
+        np.savez_compressed(out/(label+'.stages.npz'),sigma=grid,total=total,pre_HB=pre,post_HB=ps,
+             averaged_sigma=avg,area=area,raw_sigma=raw,owner=seg['atom'])
+        report['variants'][label]=dict(**profile_descriptors(path),
+             averaging_moment_e=float(area@avg),pre_HB_A2=pre.sum(1).tolist())
+    write_json(out/'stages.json',report)
+    return report
+
+
+def post(a):
+    with np.load(a.segments,allow_pickle=False) as d:
+        sym=d['sym'].tolist();x=d['x'];seg={k:d[k] for k in ('xyz','q','area','atom')}
+    out=fresh(a.out);process(sym,x,seg,out,a.key,require_registration(a.registration))
+    write_json(out/'inputs.json',dict(segments=str(Path(a.segments).resolve()),sha256=digest(a.segments)))
+
+
+def native(a):
+    from importlib.metadata import version
+    if version('pyscf')!='2.14.0': raise RuntimeError('requires pinned pyscf==2.14.0')
+    from r4_charge import factory,segments
+    sym,x=geometry(a.geometry);out=fresh(a.out);t=time.perf_counter()
+    basis='def2-svp' if a.method=='svp_swig' else 'def2-tzvp'
+    mf=factory(sym,x,a.spin,basis,a.memory)
+    method='ISWIG' if a.method=='tz_iswig' else 'SWIG'
+    if not hasattr(mf.with_solvent,'surface_discretization_method'): raise RuntimeError('required PCM API unavailable')
+    mf.with_solvent.surface_discretization_method=method
+    e=mf.kernel()
+    if not mf.converged or not np.isfinite(e): raise RuntimeError('unconverged native SCF')
+    seg,_=segments(mf.with_solvent)
+    np.savez_compressed(out/(a.key+'.segments.npz'),sym=np.array(sym),x=x,**seg)
+    process(sym,x,seg,out,a.key,require_registration(a.registration))
+    aux=getattr(mf.with_df,'auxmol',None)
+    write_json(out/'native.json',dict(key=a.key,method=a.method,geometry=str(Path(a.geometry).resolve()),
+        geometry_sha256=digest(a.geometry),energy_Eh=float(e),SCF_converged=True,
+        basis=basis,XC='b88,p86',grid_level=3,lebedev_order=29,eps=1e9,surface_discretization=method,
+        auxiliary_basis=str(getattr(aux,'basis',getattr(mf.with_df,'auxbasis',None))),
+        wall_s=time.perf_counter()-t,registration=a.registration,pyscf=version('pyscf')))
+
+
+def descriptors(a):
+    m=json.loads(Path(a.manifest).read_text());os.environ.pop('ZC_SIGMA_OVERRIDE_DIR',None)
+    from zcosmo.cosmosac import sigma_path
+    rows=[]
+    for r in m['panel']+m['validation']:
+        for source,path in [('open',Path(a.open_profiles)/(r['key']+'.sigma')),('UD',sigma_path(r['key']))]:
+            if path is None or not Path(path).is_file(): raise FileNotFoundError(f"{source}: {r['key']}")
+            s,p,meta=read_sigma(path);tot=p.sum(0);occ=tot>0
+            rows.append(dict(key=r['key'],name=r['name'],source=source,**profile_descriptors(path),
+                normalized_total= (tot/tot.sum()).tolist(),OH_fraction=np.divide(p[1],tot,out=np.zeros_like(tot),where=occ).tolist(),
+                OT_fraction=np.divide(p[2],tot,out=np.zeros_like(tot),where=occ).tolist(),occupied_bins=occ.tolist()))
+    write_json(a.out,dict(manifest_sha256=digest(a.manifest),profiles=rows,
+        note='Conditional HB fractions at unoccupied bins are undefined, encoded as zero plus an explicit occupancy mask.'))
+
+
+
+def collect(a):
+    """Compare stage outputs with stored UD bins, never experimental response values."""
+    os.environ.pop('ZC_SIGMA_OVERRIDE_DIR',None)
+    from zcosmo.cosmosac import sigma_path,SIGMA_DIR
+    if not SIGMA_DIR.is_dir(): raise FileNotFoundError('UD-backed collection runs on the Mac')
+    records=[]
+    for path in sorted(Path(a.results).rglob('stages.json')):
+        d=json.loads(path.read_text());key=d['key'];ud=sigma_path(key)
+        if ud is None: raise FileNotFoundError(key)
+        _,u,_=read_sigma(ud);un=u/u.sum()
+        for label in ('hsieh','coincident4','point_limit'):
+            pth=path.parent/label/(key+'.sigma');sig,p,meta=read_sigma(pth);pn=p/p.sum()
+            desc=profile_descriptors(pth)
+            records.append(dict(key=key,case=str(path.parent),recipe=label,UD_sha256=digest(ud),
+                 normalized_153_L1=float(abs(pn-un).sum()),
+                 normalized_total_L1=float(abs(pn.sum(0)-un.sum(0)).sum()),
+                 raw_second_moment=d['raw_second_moment'],raw_abs_tail_A2=d['raw_abs_tail_A2'],
+                 **{k:v for k,v in desc.items() if not isinstance(v,(dict,list))}))
+    if not records:raise ValueError('no completed stage diagnostics')
+    pd.DataFrame(records).to_csv(a.out,index=False)
+
+
+def main():
+    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
+    q=s.add_parser('plan');q.add_argument('--compounds',default='data/benchmark/compounds.csv')
+    q.add_argument('--geometry-dir',default='data/pyscf_sigma/profiles_v2');q.add_argument('--geometry-map')
+    q.add_argument('--out',required=True);q.add_argument('--registration',required=True)
+    q=s.add_parser('post');q.add_argument('--segments',required=True);q.add_argument('--key',required=True)
+    q.add_argument('--out',required=True);q.add_argument('--registration',required=True)
+    q=s.add_parser('native');q.add_argument('--geometry',required=True);q.add_argument('--key',required=True)
+    q.add_argument('--method',choices=['tz_swig','svp_swig','tz_iswig'],required=True)
+    q.add_argument('--spin',type=int,default=0);q.add_argument('--memory',type=int,default=4000)
+    q.add_argument('--out',required=True);q.add_argument('--registration',required=True)
+    q=s.add_parser('descriptors');q.add_argument('--manifest',required=True);q.add_argument('--open-profiles',required=True);q.add_argument('--out',required=True)
+    q=s.add_parser('collect');q.add_argument('--results',required=True);q.add_argument('--out',required=True)
+    a=p.parse_args();globals()[a.cmd](a)
+if __name__=='__main__':main()
```

### P26

<!-- PATCH:P26 -->
```diff
--- /dev/null
+++ b/scripts/r5_conformers.py
@@ -0,0 +1,265 @@
+"""Conditional A protocol: sampled lowest conductor-energy conformer, not an ensemble.
+
+Two independent deterministic proposal pools. MMFF only generates starts.
+No conformer is selected by a profile match, an experimental value, or an H-bond filter.
+No production directory is written. A capped or failed member blocks acceptance.
+"""
+from __future__ import annotations
+import argparse
+import json
+import os
+from pathlib import Path
+import time
+import numpy as np
+from r3_common import digest,write_json,read_sigma
+from r4_common import geometry,contacts
+from r5_common import fresh,align,rmsd,require_registration
+
+SEEDS=(20261005,20261006)
+
+
+def molecular_indices(m):
+    heavy=[a.GetIdx() for a in m.GetAtoms() if a.GetAtomicNum()>1]
+    donorH=[a.GetIdx() for a in m.GetAtoms() if a.GetAtomicNum()==1 and any(n.GetAtomicNum() in (7,8) for n in a.GetNeighbors())]
+    return heavy,heavy+donorH
+
+
+def proposal_pool(smiles,reference,seed):
+    from rdkit import Chem
+    from rdkit.Chem import AllChem
+    m=Chem.AddHs(Chem.MolFromSmiles(smiles));heavy,metric=molecular_indices(m)
+    if len(m.GetAtoms())!=len(reference): raise ValueError('atom-order/size mismatch')
+    params=AllChem.ETKDGv3();params.randomSeed=seed;params.numThreads=1
+    params.maxIterations=1000;params.pruneRmsThresh=-1.;params.enforceChirality=True
+    ids=list(AllChem.EmbedMultipleConfs(m,numConfs=32,params=params))
+    if len(ids)!=32: raise RuntimeError('32 requested conformers did not embed; do not replace the seed')
+    props=AllChem.MMFFGetMoleculeProperties(m,mmffVariant='MMFF94s')
+    if props is None: raise RuntimeError('MMFF94s parameters unavailable')
+    candidates=[];failures=[]
+    for cid in ids:
+        ff=AllChem.MMFFGetMoleculeForceField(m,props,confId=cid)
+        if ff is None: raise RuntimeError('missing MMFF force field')
+        status=ff.Minimize(maxIts=500)
+        if status!=0: failures.append(int(cid));continue
+        x=align(m.GetConformer(cid).GetPositions(),reference,heavy)
+        candidates.append(dict(cid=int(cid),MMFF_energy_kcal=float(ff.CalcEnergy()),x=x))
+    if failures: raise RuntimeError(f'MMFF failed for proposal ids {failures}; pool is incomplete')
+    first=min(range(len(candidates)),key=lambda i:(candidates[i]['MMFF_energy_kcal'],candidates[i]['cid']))
+    chosen=[first]
+    for _ in range(3):
+        remaining=[i for i in range(len(candidates)) if i not in chosen]
+        distances={i:min(rmsd(candidates[i]['x'],candidates[j]['x'],metric) for j in chosen) for i in remaining}
+        pick=max(remaining,key=lambda i:(distances[i],-candidates[i]['cid']))
+        chosen.append(pick)
+    return m,[candidates[i] for i in chosen]
+
+
+def generate(a):
+    from rdkit import Chem,rdBase
+    m=json.loads(Path(a.manifest).read_text());registration=require_registration(a.registration)
+    if rdBase.rdkitVersion!=m['rdkit']: raise RuntimeError('RDKit differs from the frozen planner environment')
+    records=m[a.panel];r=next((q for q in records if q['key']==a.key),None)
+    if r is None: raise ValueError('key not in selected frozen panel')
+    ref=Path(r['geometry']);ref=ref if ref.is_absolute() else Path(a.manifest).resolve().parent/ref
+    if digest(ref)!=r['geometry_sha256']: raise ValueError('frozen geometry changed')
+    sym,x=geometry(ref);out=fresh(a.out);cases=[]
+    (out/'reference.json').write_bytes(ref.read_bytes())
+    # Rigid controls get the saved geometry only, never a fictional conformer gain.
+    rigid=r['name'] in ('water','methanol')
+    if rigid:
+        write_json(out/'proposals.json',dict(key=a.key,rigid=True,cases=[],registration=registration));return
+    for seed in SEEDS:
+        mol,pool=proposal_pool(r['smiles'],x,seed)
+        if sym!=[at.GetSymbol() for at in mol.GetAtoms()]: raise ValueError('proposal atom order differs')
+        for rank,p in enumerate(pool):
+            path=out/f's{seed}-c{rank}.json'
+            record=dict(key=a.key,smiles=r['smiles'],sym=sym,x=p['x'].tolist(),seed=seed,rank=rank,
+                MMFF_proposal_id=p['cid'],MMFF_energy_kcal=p['MMFF_energy_kcal'],
+                reference='reference.json',reference_sha256=r['geometry_sha256'],spin=r['spin'],
+                registration=registration,rdkit=rdBase.rdkitVersion)
+            write_json(path,record)
+            cases.append(dict(path=path.name,sha256=digest(path),seed=seed,rank=rank,probe=rank<2))
+    write_json(out/'proposals.json',dict(key=a.key,smiles=r['smiles'],cases=cases,rigid=False,registration=registration,
+        reference_sha256=r['geometry_sha256'],
+        selection='lowest MMFF start plus three farthest starts; metric includes donor hydrogens',
+        note='Probe runs ranks 0,1 per pool. Conditional full protocol runs all four, never a new seed.'))
+
+
+def optimize(a):
+    from importlib.metadata import version
+    if version('pyscf')!='2.14.0' or version('pyberny')!='0.7.0': raise RuntimeError('requires pinned PySCF/pyberny')
+    from pyscf.geomopt.berny_solver import kernel
+    from r3_precision import factory
+    from zcosmo.pyscf_cosmo import cosmo_segments,to_profiles,write_sigma
+    g=json.loads(Path(a.input).read_text());registration=require_registration(a.registration)
+    ref=Path(g['reference']);ref=ref if ref.is_absolute() else Path(a.input).resolve().parent/ref
+    if digest(ref)!=g['reference_sha256']: raise ValueError('reference changed')
+    sym,x=list(g['sym']),np.asarray(g['x'],float);out=fresh(a.out);records=[];t=time.perf_counter()
+    from rdkit import Chem,rdBase
+    if rdBase.rdkitVersion!=g['rdkit']:raise RuntimeError('RDKit differs from the frozen proposal environment')
+    mol=Chem.AddHs(Chem.MolFromSmiles(g['smiles']));heavy,_=molecular_indices(mol)
+    if sym!=[q.GetSymbol() for q in mol.GetAtoms()]: raise ValueError('atom order changed')
+    mf=factory(sym,x,g['spin'],False,a.memory)  # unchanged registered SVP/PCM/DF/grid settings
+    def callback(env):
+        if not env['g_scanner'].converged or not np.isfinite(env['energy']) or not np.isfinite(env['gradients']).all(): raise RuntimeError('SCF gradient did not converge')
+        state=env['optimizer']._state
+        records.append(dict(cycle=int(env['cycle']),energy=float(env['energy']),trust=float(state.trust)))
+        write_json(out/'trace.json',records)
+        write_json(out/'latest.json',dict(sym=sym,x=env['mol'].atom_coords(unit='Angstrom').tolist()))
+    write_json(out/'result.json',dict(status='running',input_sha256=digest(a.input),registration=registration))
+    try:
+        converged,m2=kernel(mf,maxsteps=80,callback=callback,assert_convergence=True)
+        if not converged:
+            write_json(out/'result.json',dict(status='censored',evaluations=len(records),budget=80,
+                input_sha256=digest(a.input),wall_s=time.perf_counter()-t,registration=registration));return 2
+        x=m2.atom_coords(unit='Angstrom')
+        # Keep the evaluated Berny coordinates; do not rotate the converged geometry.
+        os.environ['ZC_R3_COOH_FLAG']='1'
+        seg,e=cosmo_segments(sym,x,spin=g['spin']);p,meta=to_profiles(sym,x,seg)
+        # Connectivity must agree exactly with the declared RDKit structure.
+        con=contacts(sym,x);expected=[sorted(n.GetIdx() for n in at.GetNeighbors()) for at in mol.GetAtoms()]
+        actual=[sorted(row['bonds']) for row in con['atoms']]
+        if expected!=actual: raise ValueError('covalent connectivity changed')
+        meta.update(geometry_converged=True,source='R5 conformer trial, not adopted',
+             geometry_protocol='A-R5-two-pool-lowest-conductor-energy',registration=registration,E_scf_Eh=float(e))
+        write_sigma(out/(g['key']+'.sigma'),p,meta,g['key'])
+        write_json(out/(g['key']+'.xyz.json'),dict(sym=sym,x=x.tolist()))
+        np.savez_compressed(out/(g['key']+'.segments.npz'),sym=np.array(sym),x=x,**seg)
+        write_json(out/'result.json',dict(status='stationary_sample',key=g['key'],seed=g['seed'],rank=g['rank'],
+            E_TZVP_Eh=float(e),evaluations=len(records),wall_s=time.perf_counter()-t,
+            profile=str(out/(g['key']+'.sigma')),geometry=str(out/(g['key']+'.xyz.json')),
+            input_sha256=digest(a.input),registration=registration,contacts=con,
+            caveat='Berny convergence is not a Hessian certificate or proof of a global conformer minimum.'))
+        return 0
+    except Exception as e:
+        write_json(out/'result.json',dict(status='failed',error=repr(e),evaluations=len(records),
+             wall_s=time.perf_counter()-t,input_sha256=digest(a.input),registration=registration));raise
+
+
+def select(a):
+    require_registration(a.registration)
+    proposals=json.loads(Path(a.proposals).read_text())
+    reference=json.loads(Path(a.reference_native).read_text())
+    if reference['key']!=proposals['key'] or reference['method']!='tz_swig' or not reference['SCF_converged']:
+        raise ValueError('reference must be the registered frozen-geometry TZVP/SWIG single point')
+    if reference['geometry_sha256']!=proposals['reference_sha256']:raise ValueError('reference geometry hash mismatch')
+    if proposals.get('rigid'): raise ValueError('rigid controls have no conformer selection')
+    expected=[c for c in proposals['cases'] if a.stage=='full' or c['probe']]
+    if len(expected)!=(8 if a.stage=='full' else 4): raise ValueError('wrong frozen proposal count')
+    root=Path(a.results);runs=[]
+    for c in expected:
+        hits=[]
+        for p in sorted(root.rglob('result.json')):
+            d=json.loads(p.read_text())
+            if d.get('input_sha256')==c['sha256']:hits.append((p,d))
+        if len(hits)!=1: raise ValueError('require exactly one recorded run per frozen proposal; no cherry-picked reruns')
+        path,d=hits[0]
+        if d['status']!='stationary_sample': raise ValueError(f'incomplete pool: {path}')
+        for field,suffix in [('profile','.sigma'),('geometry','.xyz.json')]:
+            local=path.parent/(proposals['key']+suffix)
+            if not local.is_file(): raise FileNotFoundError(local)
+            d[field]=str(local.resolve())
+        runs.append(d)
+    best=[]
+    for seed in SEEDS:
+        group=[r for r in runs if r['seed']==seed]
+        floor=min(r['E_TZVP_Eh'] for r in group)
+        # Within 1e-7 Eh use the frozen proposal rank, not a profile/benchmark value.
+        best.append(min([r for r in group if r['E_TZVP_Eh']<=floor+1e-7],key=lambda r:r['rank']))
+    (sym,x),(_,y)=[geometry(r['geometry']) for r in best]
+    from rdkit import Chem
+    mol=Chem.AddHs(Chem.MolFromSmiles(proposals['smiles']));_,metric=molecular_indices(mol)
+    dE=abs(best[0]['E_TZVP_Eh']-best[1]['E_TZVP_Eh']);geo=rmsd(x,y,metric)
+    s,p,_=read_sigma(best[0]['profile']);_,q,_=read_sigma(best[1]['profile'])
+    distance=float(abs(p/p.sum()-q/q.sum()).sum())
+    winner=min(best,key=lambda r:(r['E_TZVP_Eh'],r['seed'],r['rank']))
+    nearby=[]
+    floor=min(r['E_TZVP_Eh'] for r in runs)
+    for i,a0 in enumerate(runs):
+        for b0 in runs[i+1:]:
+            if max(a0['E_TZVP_Eh'],b0['E_TZVP_Eh'])>floor+3/627.509474: continue
+            _,xa=geometry(a0['geometry']);_,xb=geometry(b0['geometry'])
+            _,pa,_=read_sigma(a0['profile']);_,pb,_=read_sigma(b0['profile'])
+            rr=rmsd(xa,xb,metric);lp=float(abs(pa/pa.sum()-pb/pb.sum()).sum())
+            if rr>=.2 and lp>=.02: nearby.append(dict(profiles=[a0['profile'],b0['profile']],RMSD_A=rr,L1=lp))
+    lower=winner['E_TZVP_Eh']<=reference['energy_Eh']+1e-4
+    write_json(a.out,dict(key=proposals['key'],stage=a.stage,best_by_pool=best,candidate=winner,
+        energy_disagreement_Eh=dE,heavy_plus_donorH_RMSD_A=geo,normalized_L1=distance,
+        reference_energy_Eh=reference['energy_Eh'],not_higher_than_reference=bool(lower),
+        internal_gate=bool(dE<=1e-4 and geo<=.15 and distance<=.02 and lower),
+        low_energy_shape_sensitive_pairs=nearby,
+        selected_by='TZVP conductor electronic energy only; no Boltzmann or embedding-frequency weights',
+        registration=a.registration,total_evaluations=sum(r['evaluations'] for r in runs),
+        total_wall_s=sum(r['wall_s'] for r in runs),not_adopted=True))
+
+
+
+def gate(a):
+    """Separate validation panel only; computational probes have no experimental responses."""
+    import subprocess,sys
+    from r3_common import STALL_KEYS
+    from r5_common import check_fingerprint
+    manifest=json.loads(Path(a.manifest).read_text());require_registration(a.registration)
+    out=fresh(a.out);chosen={};summaries=[]
+    for rec in manifest['validation']:
+        candidates=[]
+        for p in Path(a.selections).rglob('*.json'):
+            d=json.loads(p.read_text())
+            if d.get('key')==rec['key'] and d.get('stage')=='full' and 'best_by_pool' in d: candidates.append(d)
+        if len(candidates)!=1: raise ValueError('exactly one full selection record per validation molecule required')
+        d=candidates[0]
+        if not d['internal_gate']: raise ValueError('seed agreement or reference-energy gate failed')
+        chosen[rec['key']]=d['best_by_pool'];summaries.append(d)
+    if len(chosen)!=8: raise ValueError('expected all eight separate validation molecules')
+    names={'water','methanol','nonane','dimethoxyethane'}
+    probes=[r['key'] for r in manifest['panel'] if r['name'] in names]
+    if len(probes)!=4: raise ValueError('fixed probe panel incomplete')
+    rows=[]
+    for k in sorted(chosen):
+        for other in probes:
+            for T in (250.,298.15,400.):
+                for i,j in ((k,other),(other,k)):
+                    rows.append(dict(r5_row_id=f'{i}|{j}|{T}',solute=i,solvent=j,T=T))
+    import pandas as pd
+    queries=out/'queries.csv';pd.DataFrame(rows).to_csv(queries,index=False)
+    background=Path(a.background).resolve();needed=set(chosen)|set(probes);variants={}
+    for name,ix in [('reference',0),('pool2',1)]:
+        folder=out/name;folder.mkdir()
+        for k in needed:
+            path=Path(chosen[k][ix]['profile']) if k in chosen else background/(k+'.sigma')
+            if not path.is_file(): raise FileNotFoundError(path)
+            (folder/(k+'.sigma')).symlink_to(path.resolve())
+        variants[name]={'directory':str(folder)}
+    cfg=out/'config.json';write_json(cfg,dict(variants=variants,rows=str(queries),
+        compounds=manifest['compounds'],registration=a.registration))
+    subprocess.run([sys.executable,str(Path(__file__).with_name('r5_terms.py')),'run','--config',str(cfg),
+                    '--out',str(out/'probe-results')],check=True)
+    frames=[pd.read_csv(out/'probe-results'/(name+'.csv')).set_index('r5_row_id') for name in variants]
+    r,c=frames;c=c.loc[r.index]
+    errors={}
+    for col in ('total','dsp_total'):
+        if not np.isfinite(r[col]).all() or not np.isfinite(c[col]).all(): raise ValueError('all 192 theoretical probes must be finite')
+        errors[col]=float(abs(r[col]-c[col]).max())
+    timing=sum(q['total_wall_s'] for q in summaries)
+    accepted=max(errors.values())<.02 and timing<=64*3600
+    write_json(out/'gate.json',dict(accepted=accepted,probe_rows=len(rows),seed_disagreement=errors,
+         aggregate_validation_worker_hours=timing/3600,validation_budget_worker_hours=64,
+         registration=a.registration,scope='eligible for one separately authorized exploratory score; no primary replacement',
+         note='No experimental response or UD profile enters this numerical reproducibility gate.'))
+    if not accepted:return 2
+    return 0
+
+
+def main():
+    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
+    q=s.add_parser('generate');q.add_argument('--manifest',required=True);q.add_argument('--key',required=True)
+    q.add_argument('--panel',choices=['panel','validation'],default='panel');q.add_argument('--out',required=True);q.add_argument('--registration',required=True)
+    q=s.add_parser('optimize');q.add_argument('--input',required=True);q.add_argument('--out',required=True)
+    q.add_argument('--memory',type=int,default=4000);q.add_argument('--registration',required=True)
+    q=s.add_parser('select');q.add_argument('--proposals',required=True);q.add_argument('--results',required=True)
+    q.add_argument('--reference-native',required=True);q.add_argument('--stage',choices=['probe','full'],required=True);q.add_argument('--out',required=True);q.add_argument('--registration',required=True)
+    q=s.add_parser('gate');q.add_argument('--manifest',required=True);q.add_argument('--selections',required=True)
+    q.add_argument('--background',required=True);q.add_argument('--out',required=True);q.add_argument('--registration',required=True)
+    a=p.parse_args();answer=globals()[a.cmd](a)
+    if isinstance(answer,int): raise SystemExit(answer)
+if __name__=='__main__':main()
```

### P27

<!-- PATCH:P27 -->
```diff
--- a/src/zcosmo/evaluate.py
+++ b/src/zcosmo/evaluate.py
@@ -85,14 +85,20 @@
     return out
 
 
-def binodal(m, T, n=81):
+def binodal(m, T, n=81, audit=None):
     """Return (x1_I, x1_II) of the liquid-liquid split at T, or None if miscible."""
+    def note(**values):
+        if audit is not None:
+            audit.update(values)
+    note(status="started", T=float(T), grid_n=int(n))
     xs = np.concatenate([np.logspace(-6, -2, 10), np.linspace(0.02, 0.98, n), 1 - np.logspace(-2, -6, 10)])
     try:
         lg = np.array([m.lngamma(T, np.array([x, 1 - x])) for x in xs])
-    except Exception:
+    except Exception as exc:
+        note(status="grid_evaluation_failed", error=repr(exc))
         return None
     if not np.all(np.isfinite(lg)):
+        note(status="nonfinite_grid", nonfinite_values=int((~np.isfinite(lg)).sum()))
         return None
     g = xs * np.log(xs) + (1 - xs) * np.log(1 - xs) + xs * lg[:, 0] + (1 - xs) * lg[:, 1]
     # lower convex hull
@@ -112,8 +118,12 @@
     for a, b in zip(hx[:-1], hx[1:]):
         if idx[b] - idx[a] > 1 and (best is None or b - a > best[1] - best[0]):
             best = (a, b)
+    gaps = [(a, b) for a, b in zip(hx[:-1], hx[1:]) if idx[b] - idx[a] > 1]
+    note(grid_gap_count=len(gaps), grid_gaps=gaps)
     if best is None:
+        note(status="no_gap_on_grid")  # This is not a proof of global miscibility.
         return None
+    sampled = {}  # Audit only: reuse evaluations already made by fsolve.
 
     def eqs(v):
         xa, xb = v
@@ -121,14 +131,28 @@
         xb = min(max(xb, 1e-9), 1 - 1e-9)
         la = m.lngamma(T, np.array([xa, 1 - xa]))
         lb = m.lngamma(T, np.array([xb, 1 - xb]))
+        if audit is not None:
+            sampled[tuple(v)] = (xa, xb, np.array(la, copy=True), np.array(lb, copy=True))
+            if len(sampled) > 16:
+                del sampled[next(iter(sampled))]
         return [np.log(xa) + la[0] - np.log(xb) - lb[0], np.log(1 - xa) + la[1] - np.log(1 - xb) - lb[1]]
 
     try:
-        sol, info, ier, _ = fsolve(eqs, best, full_output=True)
+        sol, info, ier, message = fsolve(eqs, best, full_output=True)
+        residual = float(np.max(np.abs(info.get("fvec", [np.nan]))))
+        note(ier=int(ier), solver_message=str(message), nfev=int(info.get("nfev", -1)),
+             residual_max=residual if np.isfinite(residual) else None)
+        if audit is not None and tuple(sol) in sampled:
+            xa, xb, la, lb = sampled[tuple(sol)]
+            mu = np.log([xa, 1-xa]) + la
+            margin = float(np.min(g - (xs * mu[0] + (1-xs) * mu[1])))
+            note(sampled_tangent_margin=margin if np.isfinite(margin) else None)
         if ier == 1 and 0 < sol[0] < sol[1] < 1 and sol[1] - sol[0] > 1e-4:
+            note(status="refined_root", residual_pass=bool(np.isfinite(residual) and residual < 1e-7))
             return float(sol[0]), float(sol[1])
-    except Exception:
-        pass
+    except Exception as exc:
+        note(refinement_error=repr(exc))
+    note(status="coarse_hull_fallback")
     return best
 
 
@@ -144,7 +168,18 @@
         Tk = round(r.T / 2) * 2
         bk = (k, Tk)
         if bk not in bcache:
-            bcache[bk] = binodal(cache[k], float(Tk))
+            directory = os.environ.get("ZC_LLE_AUDIT_DIR")
+            audit = {} if directory else None
+            bcache[bk] = binodal(cache[k], float(Tk), audit=audit)
+            if audit is not None:
+                import json
+                audit.update(model=model_name, c1=k[0], c2=k[1],
+                             first_requested_T=float(r.T), binodal_T=float(Tk),
+                             returned=bcache[bk])
+                path = Path(directory)
+                path.mkdir(parents=True, exist_ok=True)
+                with (path / f"lle-{os.getpid()}.jsonl").open("a") as handle:
+                    handle.write(json.dumps(audit, allow_nan=False) + "\n")
         b = bcache[bk]
         if b is not None:
             split[i] = True
--- /dev/null
+++ b/scripts/r5_scorecard.py
@@ -0,0 +1,263 @@
+"""Regenerate nine score arms in separate processes, with P23 LLE status accounting.
+
+Requires the already tested P14 audit hook (included in this patch). Uses the
+unchanged evaluate prediction routines. Historical files and profiles are read-only.
+"""
+from __future__ import annotations
+import argparse
+import hashlib
+import inspect
+import json
+import os
+from pathlib import Path
+import subprocess
+import sys
+import time
+import numpy as np
+import pandas as pd
+from r3_common import digest,write_json,cluster_ci
+from r4_common import selected_profiles
+from r4_lle import quality,strict_binodal,bounds
+from r5_common import (BASE,fresh,observation_ids,pairs,systems,subset,
+                        require_registration,fingerprint,check_fingerprint,STALL_KEYS)
+
+TABLES=('idac','vle','he','lle')
+MODELS=('Z0x','cosmosac2010','cosmosac_dsp')
+
+
+def freeze(a):
+    require_registration(a.registration);out=fresh(a.out)
+    compounds=pd.read_csv('data/benchmark/compounds.csv')
+    sources=selected_profiles(a.profile_root,compounds)
+    open_inputs={};inventory=[]
+    for arm in ('open630','open636'):
+        p=out/'overlays'/arm;p.mkdir(parents=True)
+        for key,folder,source in sources:
+            if arm=='open630' and folder!='profiles_v2': continue
+            meta=json.loads(source.read_text().splitlines()[0][8:])
+            if 'p18_rule' not in meta: raise ValueError(f'P20 deployment provenance missing: {source}')
+            (p/(key+'.sigma')).symlink_to(source.resolve());open_inputs[str(source.resolve())]=digest(source)
+            inventory.append(dict(arm=arm,key=key,status=folder,path=str(source.resolve()),sha256=digest(source)))
+    os.environ.pop('ZC_SIGMA_OVERRIDE_DIR',None)
+    from zcosmo.cosmosac import sigma_path,SIGMA_DIR
+    if not SIGMA_DIR.is_dir(): raise FileNotFoundError('UD-backed regeneration must run on the asset-bearing Mac')
+    ud_inputs={}
+    for table in TABLES:
+        d=pd.read_csv('data/benchmark/'+table+'.csv')
+        if 'has_sigma' in d:
+            if not d.has_sigma.isin([True,False]).all(): raise ValueError('invalid has_sigma labels')
+            d=d[d.has_sigma].copy()
+        d=d.reset_index(drop=True);d['r5_row_id']=observation_ids(d,table)
+        subset(d,'all')  # validate split labels before any evaluation
+        if d.r5_row_id.duplicated().any(): raise ValueError('row IDs are not unique')
+        for k in set(d[list(pairs(d,table))].to_numpy().ravel()):
+            p=sigma_path(k)
+            if p is None: raise FileNotFoundError(f'UD missing for declared has_sigma row: {k}')
+            ud_inputs[str(p.resolve())]=digest(p)
+        dest=out/'universe'/(table+'.csv');dest.parent.mkdir(exist_ok=True);d.to_csv(dest,index=False)
+    modelpaths=['src/zcosmo/'+n for n in ('cosmosac.py','z0x.py','models.py','evaluate.py','metrics.py','scope.py','zmodel.py','baselines.py')]
+    modelpaths+=['results/qc/dielectric.csv','results/qc/dispersion.csv','results/z_params/Z0.json']
+    modelpaths+=['scripts/r4_lle.py','scripts/r5_scorecard.py','scripts/r5_common.py']
+    inputs=fingerprint(modelpaths+['data/benchmark/'+t+'.csv' for t in TABLES]+['data/benchmark/compounds.csv'])
+    from importlib.metadata import version,PackageNotFoundError
+    packages={}
+    for name in ('numpy','scipy','pandas','thermo','chemicals','rdkit','pyscf','pyberny'):
+        try:packages[name]=version(name)
+        except PackageNotFoundError:packages[name]=None
+    config=dict(packages=packages,base=BASE,registration=a.registration,profile_root=str(Path(a.profile_root).resolve()),
+        inputs=inputs,open_inputs=open_inputs,UD_inputs=ud_inputs,
+        universe={t:dict(path=str((out/'universe'/(t+'.csv')).resolve()),sha256=digest(out/'universe'/(t+'.csv'))) for t in TABLES},
+        overlays={k:str((out/'overlays'/k).resolve()) for k in ('open630','open636')},
+        note='Fixed historical has_sigma universe. Expanded non-UD coverage requires a different labelled table.')
+    write_json(out/'config.json',config);pd.DataFrame(inventory).to_csv(out/'profile_inventory.csv',index=False)
+
+
+def worker(a):
+    root=Path(a.run).resolve();cfg=json.loads((root/'config.json').read_text())
+    check_fingerprint(cfg['inputs']);check_fingerprint(cfg['UD_inputs']);check_fingerprint(cfg['open_inputs'])
+    for name in ('ZC_SIGMA_OVERRIDE_DIR','ZC_ONLY_KEYS','ZC_LLE_AUDIT_DIR','ZC_BENCH','ZC_PRED'):os.environ.pop(name,None)
+    if a.arm!='UD': os.environ['ZC_SIGMA_OVERRIDE_DIR']=cfg['overlays'][a.arm]
+    from zcosmo import evaluate as ev
+    from zcosmo.models import make_model
+    from zcosmo.cosmosac import sigma_path
+    if 'audit' not in inspect.signature(ev.binodal).parameters: raise RuntimeError('apply the P14 hook included with P27')
+    smi=ev._smiles();out=fresh(root/'predictions'/a.model/a.arm);t0=time.perf_counter()
+    for table in TABLES:
+        u=cfg['universe'][table]
+        if digest(u['path'])!=u['sha256']: raise ValueError('frozen universe changed')
+        d=pd.read_csv(u['path']);ca,cb=pairs(d,table)
+        eligible=~(d[ca].isin(STALL_KEYS)|d[cb].isin(STALL_KEYS)) if a.arm=='open630' else pd.Series(True,index=d.index)
+        d['profile_eligible']=eligible;d['r5_eval_status']=np.where(eligible,'pending','excluded_S1_S2_by_design')
+        sub=d[eligible].copy().reset_index(drop=True)
+        if a.arm!='UD':
+            for k in set(sub[[ca,cb]].to_numpy().ravel()):
+                p=Path(cfg['overlays'][a.arm])/(k+'.sigma')
+                if not p.is_file() or sigma_path(k).resolve()!=p.resolve(): raise ValueError('unintended fallback to UD')
+        if table=='idac':
+            columns=['pred_ln_gamma_inf'];values=[ev.predict_idac(a.model,sub,smi)]
+        elif table=='vle':
+            columns=['pred_P','pred_y1'];values=list(ev.predict_vle(a.model,sub,smi))
+        elif table=='he':
+            columns=['pred_HE_J'];values=[ev.predict_he(a.model,sub,smi)]
+        else:
+            columns=['pred_split','pred_x1_I','pred_x1_II','r5_detection','r5_x1_I','r5_x1_II']
+            values=[np.full(len(sub),np.nan) for _ in columns];status=[];models={};calls={}
+            # Extend the accepted repair only after the same first-20-good control gate per arm.
+            controls=[]
+            unique=sorted({(r.c1,r.c2,float(round(float(r.T)/2)*2)) for r in sub.itertuples()})
+            for c1,c2,T in unique:
+                model=make_model(a.model,[c1,c2],[smi[c1],smi[c2]])
+                oldaudit={};old=ev.binodal(model,T,audit=oldaudit);oldaudit['returned']=old
+                if quality(oldaudit)[0]!=1.:continue
+                answer=strict_binodal(make_model(a.model,[c1,c2],[smi[c1],smi[c2]]),T,budget=4000)
+                same=(answer['status']=='root_passes_refined_sampled_checks' and
+                      any(np.max(abs(np.asarray(q['x'])-old))<1e-4 for q in answer.get('roots',[])))
+                controls.append(dict(c1=c1,c2=c2,T=T,passed=bool(same),answer=answer))
+                if not same:raise ValueError('P23 extension control failed; this score arm is not accepted')
+                if len(controls)==20:break
+            write_json(out/'lle_controls.json',dict(controls=controls,passed=len(controls)==20))
+            if len(controls)!=20:raise ValueError('fewer than 20 good controls; report inconclusive, do not weaken the gate')
+            with (out/'lle_calls.jsonl').open('w') as handle:
+                for i,r in enumerate(sub.itertuples()):
+                    pair=(r.c1,r.c2);T=float(round(float(r.T)/2)*2);key=(pair,T)
+                    if pair not in models: models[pair]=make_model(a.model,list(pair),[smi[k] for k in pair])
+                    if key not in calls:
+                        audit={};b=ev.binodal(models[pair],T,audit=audit)
+                        audit.update(model=a.model,c1=pair[0],c2=pair[1],binodal_T=T,returned=b)
+                        decision,label=quality(audit);xy=b;repair=None
+                        if not np.isfinite(decision):
+                            # The same accepted P23 finite-grid repair, no new thresholds.
+                            fresh_model=make_model(a.model,list(pair),[smi[k] for k in pair])
+                            repair=strict_binodal(fresh_model,T,budget=4000);label=repair['status'];xy=None
+                            if label=='root_passes_refined_sampled_checks':
+                                decision=1.;xy=max(repair['roots'],key=lambda z:z['x'][1]-z['x'][0])['x']
+                            elif label=='gap_witness_only':decision=1.
+                            elif label=='no_gap_on_refined_grid':decision=0.
+                            else:decision=np.nan
+                        calls[key]=(b,decision,label,xy)
+                        handle.write(json.dumps(dict(legacy=audit,repair=repair,registration=cfg['registration']),allow_nan=False)+'\n');handle.flush()
+                    b,decision,label,xy=calls[key]
+                    values[0][i]=float(b is not None)
+                    if b is not None:values[1][i],values[2][i]=b
+                    values[3][i]=decision
+                    if decision==1. and xy is not None: values[4][i],values[5][i]=xy
+                    status.append(label)
+            d['r5_lle_status']='not_eligible';d.loc[eligible,'r5_lle_status']=status
+        for c,v in zip(columns,values):d[c]=np.nan;d.loc[eligible,c]=v
+        finite=np.isfinite(np.stack(values,axis=1)).all(1) if table!='lle' else np.isfinite(values[3])
+        d.loc[eligible,'r5_eval_status']=np.where(finite,'evaluated','nonfinite_or_unresolved')
+        d.to_csv(out/(table+'.csv'),index=False)
+    check_fingerprint(cfg['inputs']);check_fingerprint(cfg['UD_inputs']);check_fingerprint(cfg['open_inputs'])
+    write_json(out/'timing.json',dict(model=a.model,arm=a.arm,wall_s=time.perf_counter()-t0,registration=cfg['registration']))
+
+
+def scalar_metrics(d,table):
+    sid=systems(d,table)
+    if table=='idac':
+        pred=d.pred_ln_gamma_inf.to_numpy(float);target=d.ln_gamma_inf.to_numpy(float);e=pred-target
+        from zcosmo.metrics import selectivity_spearman
+        rho,n=selectivity_spearman(d,'pred_ln_gamma_inf')
+        extra=dict(bias=float(e.mean()),solvent_rank_rho=float(rho) if np.isfinite(rho) else None,ranking_solutes=n)
+    elif table=='vle':
+        e=100*(d.pred_P-d.P).to_numpy(float)/d.P.to_numpy(float)
+        from zcosmo.metrics import three_phase_mask
+        homogeneous=~three_phase_mask(d)
+        ym=np.isfinite(d[['pred_y1','y1']].to_numpy()).all(1) if 'y1' in d else np.zeros(len(d),bool)
+        extra=dict(homogeneous_rows=int(homogeneous.sum()),three_phase_rows=int((~homogeneous).sum()),
+            homogeneous_AAD_pct=float(abs(e[homogeneous]).mean()) if homogeneous.any() else None,
+            vapor_y_rows=int(ym.sum()),vapor_y_AAD=float(abs(d.loc[ym,'pred_y1']-d.loc[ym,'y1']).mean()) if ym.any() else None)
+    else:
+        e=(d.pred_HE_J-d.HE_J).to_numpy(float);large=abs(d.HE_J.to_numpy(float))>20
+        extra=dict(sign_rows=int(large.sum()),sign_correct=float((np.sign(d.pred_HE_J.to_numpy()[large])==np.sign(d.HE_J.to_numpy()[large])).mean()) if large.any() else None)
+    return dict(rows=len(d),systems=len(np.unique(sid)),MAE=float(abs(e).mean()),
+                MAE_CI95=cluster_ci(abs(e),sid),**extra),e
+
+
+def eligibility(d,table):
+    if table=='idac':cols=['pred_ln_gamma_inf','ln_gamma_inf']
+    elif table=='vle':cols=['pred_P','P']
+    elif table=='he':cols=['pred_HE_J','HE_J']
+    else:return d.profile_eligible.to_numpy(bool)
+    finite=np.isfinite(d[cols].to_numpy(float)).all(1)&d.profile_eligible.to_numpy(bool)
+    if table=='vle':finite&=d.P.to_numpy(float)>0
+    return finite
+
+
+def lle_metrics(d):
+    result=bounds(d.r5_detection.to_numpy(float),systems(d,'lle'))
+    valid=(d.r5_detection==1.)&np.isfinite(d[['r5_x1_I','r5_x1_II','x1']].to_numpy(float)).all(1)
+    result['endpoint_rows']=int(valid.sum())
+    result['composition_MAE']=float(np.minimum(abs(d.loc[valid,'x1']-d.loc[valid,'r5_x1_I']),
+                  abs(d.loc[valid,'x1']-d.loc[valid,'r5_x1_II'])).mean()) if valid.any() else None
+    result['statuses']=d.r5_lle_status.value_counts().to_dict()
+    result['legacy_gap_found_rows']=float(d.pred_split.mean())
+    result['meaning']='Operational finite-grid detection, not a certificate of miscibility or global stability. Witnesses have no endpoint MAE.'
+    return result
+
+
+def summarize(a):
+    root=Path(a.run).resolve();cfg=json.loads((root/'config.json').read_text())
+    report={'base':BASE,'registration':cfg['registration'],'tables':{},'scope':'Z0x-UD remains reference; open630 secondary; open636 includes exploratory S1/S2'}
+    lines=['Z-COSMO regenerated scorecard, '+a.split,'',report['scope'],'']
+    for table in TABLES:
+        frames={}
+        for model in MODELS:
+            for arm in ('UD','open630','open636'):
+                p=root/'predictions'/model/arm/(table+'.csv');d=pd.read_csv(p)
+                if d.r5_row_id.duplicated().any():raise ValueError('duplicate prediction identities')
+                frames[(model,arm)]=subset(d,a.split).set_index('r5_row_id',drop=False)
+        first=next(iter(frames.values()))
+        if any(set(d.index)!=set(first.index) for d in frames.values()): raise ValueError('denominator identity mismatch')
+        standalone={};paired=[]
+        for (model,arm),d in frames.items():
+            eligible=d[d.profile_eligible]
+            if table=='lle':ans=lle_metrics(eligible)
+            else:
+                valid=eligibility(d,table)
+                ans,_=scalar_metrics(d.loc[valid],table) if valid.any() else ({'rows':0},None)
+                ans.update(requested_rows=len(d),profile_eligible_rows=len(eligible),unavailable_rows=int((~valid).sum()))
+            standalone[model+'/'+arm]=ans
+        # Fixed pairwise intersections, never a hidden intersection over all nine arms.
+        for model in MODELS:
+            r=frames[(model,'UD')]
+            for arm in ('open630','open636'):
+                c=frames[(model,arm)].loc[r.index]
+                common=eligibility(r,table)&eligibility(c,table)
+                rr,cc=r.loc[common],c.loc[common]
+                if table=='lle':
+                    pair=dict(reference=lle_metrics(rr),candidate=lle_metrics(cc))
+                elif len(rr):
+                    rm,er=scalar_metrics(rr,table);cm,ec=scalar_metrics(cc,table)
+                    pair=dict(reference=rm,candidate=cm,delta_MAE_CI95=cluster_ci(abs(ec)-abs(er),systems(rr,table)))
+                else:pair=dict(reference={'rows':0},candidate={'rows':0})
+                pair.update(model=model,arm=arm,common_rows=len(rr),row_ids_sha256=hashlib.sha256('\n'.join(rr.index).encode()).hexdigest())
+                paired.append(pair)
+        report['tables'][table]=dict(standalone=standalone,pairwise=paired)
+        lines+=['Table: '+table,'','| Model / profiles | Rows | Systems | Error or detection | Status |','|---|---:|---:|---|---|']
+        for name,r in standalone.items():
+            if table=='lle':value=str(r['row_gap_found_bounds']);status=f"{r['endpoint_rows']} checked endpoint rows; {r['unresolved_rows']} unresolved"
+            else:value=str(r.get('MAE'));status=f"{r.get('unavailable_rows',0)} unavailable of {r.get('requested_rows',0)}"
+            lines.append(f"| {name} | {r['rows']} | {r.get('systems','')} | {value} | {status} |")
+        lines+=['','Pairwise comparison denominators and CIs are in scorecard.json; each open arm is compared with UD on identical row identities.','']
+    write_json(root/('scorecard_'+a.split+'.json'),report)
+    (root/('scorecard_'+a.split+'.md')).write_text('\n'.join(lines)+'\n')
+
+
+def run(a):
+    freeze(a)
+    for model in MODELS:
+        for arm in ('UD','open630','open636'):
+            subprocess.run([sys.executable,str(Path(__file__).resolve()),'worker','--run',str(Path(a.out).resolve()),
+                            '--model',model,'--arm',arm],check=True)
+    for split in ('all','test'):
+        summarize(argparse.Namespace(run=a.out,split=split))
+
+
+def main():
+    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
+    for name in ('run','freeze'):
+        q=s.add_parser(name);q.add_argument('--profile-root',default='data/pyscf_sigma');q.add_argument('--out',required=True);q.add_argument('--registration',required=True)
+    q=s.add_parser('worker');q.add_argument('--run',required=True);q.add_argument('--model',choices=MODELS,required=True);q.add_argument('--arm',choices=['UD','open630','open636'],required=True)
+    q=s.add_parser('summarize');q.add_argument('--run',required=True);q.add_argument('--split',choices=['all','test','train'],default='test')
+    a=p.parse_args();globals()[a.cmd](a)
+if __name__=='__main__':main()
```

### REG5

<!-- PATCH:REG5 -->
```diff
--- /dev/null
+++ b/docs/astra/round5/REGISTRATION_PROPOSED.md
@@ -0,0 +1,148 @@
+# Proposed round-5 registration
+
+This is proposed text, not evidence of registration. Append adopted text to
+PREREGISTRATION.md with the actual commit timestamp before inspecting new
+native outputs or scores. Reference code is main at
+69b49116c2ae7574d7ae471f0a4ed7ba33d0db8b plus the archived R5 patches.
+The experiment is motivated by already observed glycol, water and charge
+sensitivities. It is not a fresh experimental holdout. Nothing is fitted to
+ThermoML, and no recipe is selected by experimental error. P20 remains applied;
+P23's accepted accounting remains; P15/P17/P19 rejections and S1/S2 labels stand.
+The six-chain completion campaign remains closed.
+
+P24 is an E component-accounting diagnostic of the unchanged Z0x implementation,
+plus explicitly A electrostatic/HB-off interventions. Reproduce the frozen P22
+859-row panel in separate processes for native, area-zero and capacitary-zero
+profiles, with a complete unchanged open background. Also substitute only the
+normalized UD shape, retaining native area and volume, for each of the six
+fixed P22 molecules in separate arms. Do not pass experimental response values
+to these workers. Decompose the actual one-sided h=1e-4 endpoint expression
+into combinatorial, residual and London terms. Require total parity <1e-9 and
+invariance to H2O/COOH flag relabeling <1e-10 in Z0x. Report the frozen-c exact
+endpoint and h=1e-5/1e-6 controls; these do not replace the production stencil.
+Use all four ES/HB on/off kernels and symmetric Shapley attribution, retaining
+the interaction and finite masks. This is a model sensitivity decomposition,
+not separately measurable ES/HB free energies. It does not adopt a neutrality
+convention. All baseline and candidate coverage differences are failures of
+comparability, not permission to discard unfavorable queries.
+
+P25 freezes the twelve structures in r5_common.PANEL before new computation:
+water, methanol, ethylene/diethylene/triethylene/tetraethylene glycol, glycerol,
+propylene glycol, 2-methoxyethanol, 1,2-dimethoxyethane, tetrahydrofuran and
+n-nonane. Resolve by stereo-aware canonical SMILES; ambiguous matches must
+resolve to the exact structure-derived InChIKey or fail. These are structural
+homologues and controls, not a claim that their historical errors were unseen.
+Freeze saved geometry bytes; never invent the missing UD conformer. A separate
+validation panel is the first eight SHA256('R5-validation-v1|'+InChIKey)-ordered
+neutral, closed-shell, single-component covalent CHO structures with at most 13 heavy atoms, at least two rotatable bonds,
+and either two OH groups or an ether, excluding the twelve and the historical
+25. Insufficient eligible members or missing generating geometries abort the
+plan. Freeze the manifest and package versions before native outputs.
+
+On each of the twelve saved geometries, run three fixed single-point methods:
+BP86/def2-TZVP/SWIG, BP86/def2-SVP/SWIG and BP86/def2-TZVP/ISWIG. All use the
+project radii, C-PCM eps=1e9, Lebedev order 29, grid level 3/default pruning,
+conv_tol=1e-9 and PySCF 2.14.0. The latter two are A diagnostic arms, not claims
+of reproducing DMol3. Record the resolved auxiliary basis. At most 36 single
+points, at most one hour per call. Reuse previous segments only on matching
+geometry and method hashes. No density quadrature or new rotation recipe is
+part of this trial.
+
+For each saved segment table, retain raw charges and owner areas, the Hsieh
+averaged sigmas, pre-HB bins and post-HB bins. Independently implement the
+existing Hsieh formula and require max sigma difference <1e-10 e/A^2 and
+binwise pre/post-HB total agreement <1e-8 A^2. Diagnose the segment-size effect
+by the exact compressed equivalent of four coincident A/4,q/4 patches, and
+by its point-patch limit. Both are A diagnostic sensitivities, not physical
+remeshing or approved new averaging methods. The raw table is unchanged;
+no out-of-range sigma is clipped into a usable profile. The existing radius,
+decay and HB parameters are not adjusted. Compare stage distributions and
+stored UD final shapes without using experimental responses. Missing UD
+geometry prevents unique historical attribution and is reported as such.
+
+P26 is conditional. Generate proposals with two fixed RDKit ETKDGv3 pools,
+32 embeddings per pool, seeds 20261005 and 20261006, one thread, maxIterations
+1000, pruning disabled. Pin the RDKit version recorded in the manifest.
+MMFF94s, at most 500 iterations, supplies proposals only. A failed embedding or
+MMFF member blocks that pool; there is no alternative seed or force-field
+fallback. Select the lowest-MMFF proposal followed by three greedy farthest
+proposals, using fixed-atom-order properly aligned heavy-atom-plus-donor-H RMSD.
+RDKit/force-field priors are empirical proposal machinery, not fitted benchmark
+model parameters. Each selected start is optimized by the unchanged registered
+BP86/def2-SVP/DF/grid-2/C-PCM-17 CPU Berny path, at most 80 gradient evaluations
+and one hour per proposal including the TZVP profile. PySCF=2.14.0 and
+pyberny=0.7.0. Fresh histories; no P15 noise override, no P19 tight stage,
+no optimizer pickle, no altered convergence predicate. All members must pass
+Berny's actual convergence test and preserve covalent connectivity. Failed or
+censored members are not omitted. The TZVP profile uses the accepted P18 flag.
+Keep the converged orientation. O-H...O contacts use the already registered
+geometric definition and are reported, never filtered or rewarded.
+
+First run ranks 0 and 1 in each pool for the ten non-rigid structural panel
+members, at most 40 optimizations. Water and methanol are rigid controls.
+The full conformer protocol is authorized only by a prospective continuation
+record when this probe contains reproducible distinct low-energy structures:
+at least one pair within 3 kcal/mol of the sampled minimum, RMSD >=0.2 A,
+and normalized-profile L1 >=0.02; report pool agreement and the other controls
+without selecting a molecule by experimental error. This is justification for
+further sampling, not proof that a conformer explains UD's historical profile.
+Cross both pool winners on the same additional single-point methods when
+separating method/conformer interactions, at most 40 extra single points.
+
+If continued, complete all four proposals in each pool, reusing the already
+computed members, and run the same full protocol on all eight separately
+selected validation molecules. Select by lowest TZVP conductor electronic
+energy alone, ties within 1e-7 Eh by frozen proposal rank. Do not assign
+Boltzmann weights from embedding frequency or electronic energy, and do not
+claim a global minimum or a temperature-dependent conformer ensemble.
+The theoretical reproducibility gate requires all full pools to complete;
+per molecule, independent pool minima must agree within 1e-4 Eh, aligned
+heavy-plus-donor-H RMSD <=0.15 A, and normalized 153-bin L1 <=0.02. The selected
+energy must not exceed the saved-geometry TZVP reference by more than 1e-4 Eh.
+All eight validation members must pass. On fixed water/methanol/nonane/
+dimethoxyethane probes at 250, 298.15 and 400 K in both solute/solvent roles
+(192 queries), both models must be finite in both pools and maximum pool
+prediction difference must be <0.02 for Z0x and COSMO-SAC-dsp. The full separate
+validation budget is 64 worker-hours on four-core workers, with the per-member
+80-evaluation/one-hour cap. Do not extend a censored member after reading it.
+
+A pass establishes only computational reproducibility of a sampled-conformer
+protocol. It permits one separately authorized exploratory experimental report
+using the already frozen selections, not promotion of the 630 primary profiles.
+The exact baseline profiles and all S1/S2 files remain read-only. Any future
+conformer arm has its own directory and identity. A new claim of improved
+experimental accuracy must report the fixed full comparison and paired CIs,
+including water and the branched controls, whichever direction they move.
+No best-error choice among conformers or recipes is allowed.
+
+P27 regenerates Z0x, COSMO-SAC 2010 and COSMO-SAC-dsp in three separate profile
+arms: UD, the 630 primary open profiles, and the 636 open profiles including
+S1/S2. Every model/arm runs in a fresh process. Use the unchanged evaluate
+formulas on the historical has_sigma universe for each table; attach immutable
+row identities and freeze every source file/profile hash. Open630 marks the six
+flagged compounds excluded by design, without falling back to UD. Report
+standalone coverage and pairwise UD/open common subsets, never a hidden
+intersection across all nine arms. All raw counts are written from the actual
+frozen CSVs. Expanded non-UD coverage is a different table.
+
+For LLE, reuse the previously tested P14 hook without changing its predictions,
+then the accepted P23 thresholds, grids, 4000-call budget and old 2-K rounding.
+For each arm first require the first 20 sorted good-call controls to retain
+checked roots within 1e-4 of the legacy endpoints. Failure or fewer than 20
+controls blocks that arm and is reported. Retain roots, gap witnesses, finite-grid
+no-gap results and unresolved results as different statuses. Never give a
+witness an endpoint error or turn an unknown into miscibility. Endpoint MAE
+has its own explicit denominator. Report operational detection bounds and
+system-majority bounds, not global phase-equilibrium certificates. This extends
+accepted numerical accounting to additional profile/model arms; it does not
+assume that UD repairs validate open-profile endpoints.
+
+IDAC uses absolute ln-gamma errors and solvent-ranking rules already in metrics.
+VLE uses the same psat source and homogeneous-liquid exclusion, with its own
+coverage. HE uses the same 0.5 K central difference and sign threshold. System
+bootstrap uses 1000 resamples, seed 7 reset per statistic/comparison; this is the
+same estimator with explicitly fixed draws, not a promise of bitwise identity
+to older CIs generated by the global RNG stream. Keep historical scorecards,
+including 0.800/762 and 0.839/828, unchanged. Regenerated VLE/HE values are not
+reported until the actual files exist. The reused experimental data are not
+represented as a fresh holdout. Save all outputs outside historical results.
```

## Source and provenance index

All repository sources below were checked at `69b49116c2ae7574d7ae471f0a4ed7ba33d0db8b`, unless another pinned version is explicitly stated. References are to source content, not claims that a native calculation was executed here.

| ID | Source | Evidence used |
|---|---|---|
| S1 | `docs/astra/ROUND5_PROMPT.md`; `docs/OPTIMIZATION_BRIEF.md` | Round scope, E/A rules, free-compute and registration constraints. |
| S2 | `docs/astra/round4/RESULTS.md` | P20/P21/P22/P23 outcomes, factorial signs, projections, measured repair counts and time. |
| S3 | `PREREGISTRATION.md`, round-4 entry and results | Accepted P20 application, existing repair rule, inconclusive quadratures, closed chain budget. |
| S4 | `docs/astra/round4/ZCOSMO_ROUND4_REPORT.md`, blob `a6be69a6b9b9cd6e4cea383863d9f11d506f9197` | Full previous report and its embedded patches; attached copy matches this blob. |
| S5 | `data/raw/nist/to_sigma.py`, blob `9f2e0d6f3bb4da4880f9bd6ad702847f9308ed1d` | Hsieh weights, HB classification, binning and area transfer. |
| S6 | `scripts/r4_common.py`; `scripts/r4_charge.py` | Stage traces, Gaussian-sphere reference, projections, density-quadrature gate and memory caveat. |
| S7 | `scripts/r4_lle.py`, blob `11123f95886f304c0e8d356e043745c41e6e305e` | Root/witness/status distinctions, finite-grid qualification, budgets and denominator bounds. |
| S8 | `scripts/r4_glycols.py`; `scripts/r4_metadata.py`; `scripts/r4_selftest.py` | Structural selection, AVP factorial, accepted metadata transaction, portable controls. |
| S9 | `src/zcosmo/z0x.py`, blob `80c3f1f3b61056a76678a80caf4120c58614adfe` | Actual one-sided endpoint, rounded-c cache, interior analytic branch and dielectric dependence. |
| S10 | `src/zcosmo/cosmosac.py`, blob `c226a668b7b9dba9e7400cda180fafd8faa700f3` | Segment equations, residual/pure reference, ES/HB kernel and London implementation. |
| S11 | `results/z_params/Z0.json`; `src/zcosmo/models.py` | Z0x uses the frozen London-mode Z0 parameters rather than the empirical dispersion flag. |
| S12 | `scripts/r3_precision.py`; `src/zcosmo/pyscf_cosmo.py` | Original CPU factory, registered settings, TZVP profile extraction, accepted COOH option. |
| S13 | `src/zcosmo/evaluate.py`, blob `e154f0d9e695957a66c600e8211a0d0bca010c8c` | Current main still lacks P14; filtering, device-independent prediction formulas and 2-K LLE rounding. |
| S14 | `src/zcosmo/metrics.py`; `scripts/r3_common.py` | Metric definitions, bootstrap, row/split rules and helper functions. |
| S15 | `cloud/r4/native/cases.json`, its six geometry JSON files; `.github/workflows/r4_charge.yml` | Exact native input panel, source coordinates and the original workflow's return-code/artifact conventions. |
| U1 | PySCF `v2.14.0/pyscf/solvent/pcm.py`, blob `8d11cfa0966a0990dc94d31df73a50c86b2d5eb8` | SWIG and ISWIG construction, area/Gaussian-width conventions. |
| U2 | “Recent Improvements to the NWChem COSMO Module,” JCTC 21 (2025), 11573–11584, DOI `10.1021/acs.jctc.5c01368` | Charge and potential consistency in outlying-charge corrections; not a backend used by this experiment. |
| U3 | Official PySCF solvent/COSMO-RS API documentation, `pyscf.solvent.cosmors.get_pcm_parameters`; source `pyscf/solvent/cosmors.py` | Explicit statement that outlying-charge correction is not implemented. |
| U4 | Official RDKit Book, conformer-generation parameters; RDKit Cookbook ETKDGv3 examples | Parameter API, reproducible seeds/thread settings and empirical proposal machinery. |
| U5 | PySCF `v2.14.0/pyscf/geomopt/berny_solver.py`, blob `1f3f4d7bc7652da45a68c325e69123b9eb88a222`; pyberny tag `0.7.0` | Kernel return, callback timing, convergence flag, unchanged Berny predicate. |

The pre-existing R4 helper blobs reconstructed from the archived report were verified as follows: `r4_common.py d96484bbd0aed5aafeb47d038f6485055f425ecb`; `r4_charge.py 5fb839d20dec4175a1a1b6473ea7041d3fc192e5`; `r4_lle.py 11123f95886f304c0e8d356e043745c41e6e305e`; `r4_glycols.py cb9f54af424d33e5c1f1e148429eb93ee9b7cf94`; `r4_metadata.py 5858aa6366cb7576a345271c8bc97227b2de0f1a`.

Patch validation was against the new paths plus a context-only reconstruction of the unchanged P14 target hunks. That is not a claim of having cloned or built the full repository. Run `git apply --check` in the pinned checkout as shown before applying. The complete new helper files compiled locally. Native/real-data gates remain outstanding.
