# Replacing COSMO-SAC interaction constants without ThermoML regression: a pre-registered benchmark

Victor Liang (original draft 2026-09-24; evidence and scope updated 2026-10-08)

## Abstract

COSMO-SAC predicts liquid-mixture properties from molecular surface profiles and shared interaction
parameters. We benchmark specified replacements of its interaction constants without regression to
ThermoML, while retaining inherited surface-processing and combinatorial conventions and
experimental pure-component vapor-pressure correlations. The initial Z0 recipe was registered before
its predictions; later variants were registered before their own evaluations, with prior data
exposure acknowledged. The historical compound-test comparison found no resolved IDAC difference
between Z0 and COSMO-SAC 2010 (MAE in ln gamma 0.76 versus 0.82), rather than establishing
statistical equivalence. The contemporaneous project record reports higher LLE detection balanced
accuracy, 0.90 versus 0.84 for COSMO-SAC 2010 and 0.81 for modified UNIFAC. Z0 had larger VLE
pressure and excess-enthalpy errors. Z0x's composition-dependent electrostatic prescription reduced
VLE AAD from 18.8% to 14.2%, versus 8.6% for COSMO-SAC 2010, on the historical main7 VLE subset. Z0x
also remained worse on the historical temporal collection.

On a separate, already-exposed panel of 963 observations in 100 systems, a registered factorial
attributed 2.24 percentage points, approximately 67% of the Z0x-to-2010 pressure-error gap, to the
implemented London dispersion closure. Electrostatic and hydrogen-bond replacements contributed 26%
and 7% under the same allocation. These are conditional error attributions, not fractions of
intermolecular physics. The one subsequently registered dispersion alternative, LV1, failed its
exposed tradeoff screen: VLE AAD changed from 13.78% to 13.13% without passing its uncertainty gate,
and IDAC and excess-enthalpy errors increased. No fitted factorial corner, term deletion, or LV1
variant was adopted. The completed study establishes useful but property-dependent performance
without new benchmark regression and identifies a consequential contact-model approximation. The VLE
gap remains unresolved, and this project's development campaign is closed. Open-profile and
numerical-provenance findings are reported separately from the UD-backed results.

## 1. Introduction

Process simulators describe liquid mixtures mostly with correlative excess-Gibbs-energy models such
as NRTL and UNIQUAC, whose binary parameters are regressed from measurements of the same binary.
When no data exist, engineers fall back on predictive models. Group-contribution methods (modified
UNIFAC) need group-interaction parameters fitted to large databases and cannot treat groups that
were never parameterized. COSMO-RS and COSMO-SAC replace groups by the screening-charge distribution
of each molecule, computed with density functional theory in a conductor. Application still requires
a supported chemical domain and a successfully generated, consistently processed profile. Their
interaction model, however, still carries a small set of universal constants (an effective contact
area, the electrostatic misfit coefficient and its temperature dependence, hydrogen-bond strengths
and cutoffs, and in later versions dispersion parameters) that are fitted to experimental
infinite-dilution activity coefficients and phase equilibria. Published variants have refit shared
parameters for different electronic-structure recipes. Their reported accuracy must therefore be
distinguished from that of the present no-new-regression variants.

HANNA is a thermodynamically constrained neural model trained on about 824,000 Dortmund Data Bank
points. Its publisher reports comparisons across binary phase equilibria and excess enthalpy [8].
The deployed model's training membership has not been matched row by row to this project's ThermoML
collection, so its results here are a data-driven reference rather than a certified unseen-data
contest. Transferability beyond the inspected chemical systems remains a separate question.

The present comparison tests specified approximations rather than separating all accuracy into a
physical part and a fitted part. We test specified replacements of the interaction constants and
dispersion model, while retaining the common molecular-surface and combinatorial conventions. The
benchmark and initial metrics were registered before predictions. Subsequent changes were registered
before their own execution, with prior exposure stated. Ablations identify conditional model
sensitivities; they do not uniquely identify a missing physical mechanism.

## 2. Methods

### 2.1 Data
ThermoML XML files (MobleyLab mirror of the NIST/TRC archive, publications to mid-2017) were flattened and
compounds resolved to InChIKeys offline, accepting a match only when the molecular formula agreed.
The registered chemical scope was neutral C/H/N/O/F/Cl/Br/S molecules with at most 25 heavy atoms,
250 <= T <= 450 K and P <= 500 kPa where pressure is supplied. In the implementation, the VLE critical-
temperature filter rejects T >= 0.98 Tc for either component when Tc is known; an unknown Tc does not
cause rejection. This is not a certificate that every retained observation is subcritical.
IDAC records are grouped by round(T/2)*2 K and compared with the within-bin median. Values within
0.2 in ln gamma are retained when at least half the group passes; singleton groups are retained.
Testable VLE series are screened by the Herington rule, including the registered near-ideal exception.
Untestable series are retained with an untested label, not described as having passed. LLE selection
uses the recorded two-branch or at-least-five-cloud-point rule. These source-level qualifications do
not change the frozen benchmark or its logged exclusions. See src/zcosmo/scope.py and PREREGISTRATION.md.

Twenty percent of in-scope compounds were held out (seed 20260924, water always in training). Rows
with one held-out component form `test_one`, with two `test_both`. The split was hashed before any
Z-model prediction. A temporal set was built later from the complete NIST 2020 archive (11,923
files, standard InChIKeys): rows from files absent from the 2017 mirror, i.e. publications from
mid-2017 to 2019. These postdate the fitting of COSMO-SAC 2010 (2010), COSMO-SAC-dsp (2014) and the
UNIFAC parameter table used (2016). This is the historical provenance description of those parameter
tables, not proof that every reference model or upstream input is unexposed to these measurements.
HANNA may overlap these data. Neither this temporal collection nor the repeatedly examined compound
test split is a fresh holdout for R10-R16 development. A future validation needs a custodian-led
source and duplicate-series audit before responses are revealed; relabeling an existing split cannot
restore independence.

### 2.2 Reference models
COSMO-SAC 2010 and -dsp were reimplemented in NumPy and reproduce the NIST benchmark code (Bell et al.,
JCTC 2020) to 2e-9 in ln gamma on 400 random pairs. The historical main comparisons use the same project UD sigma
profile collection (DMol3 BP/DNP; 2,259 entries reported by the project). Bell et al. describe a 2,261-
compound distributed database [6]; that publication count is not substituted for the project inventory. Modified UNIFAC (Dortmund) uses the `thermo` package with
automatic group assignment (`ugropy`). HANNA is the published ensemble (Nat. Commun. 2026).

### 2.3 The Z0 model
Both the stored Z0 recipe and the 2010 reference retain a_eff = 7.25 A^2, q0 = 79.53, r0 = 66.69 and
z = 10. These are common inherited conventions in this implementation; no independent derivation of the
numerical effective area is established by calling it a geometric identity. The stored NHB/OH/OT split
and its processing rules are also shared. Electrostatic misfit c_ES = alpha'/2 with
alpha' = 0.3 a_eff^1.5 / eps0 in the
conductor limit (12,226 kcal A^4 mol^-1 e^-2; the fitted 2010 value at 298.15 K is 8,197). Hydrogen bonding:
for each dimer, E_HB = c_ES (s_D + s_A)^2 - c_hb (s_D - s_A)^2 with s_D, s_A the mean charge density of the
most extreme a_eff of the donor and acceptor profiles; E_HB is the counterpoise-corrected B3LYP/def2-TZVP
binding energy including monomer deformation, with the D4 dispersion part removed. Dispersion: London
contact energies e_ij = -C6_ij / d_ij^6 from D4 molecular C6 and polarizabilities (London combining rule),
d_i the diameter of a sphere of COSMO cavity volume, entering as ln gamma_1 = (z/2) w x_2^2 / RT with
w = 2 e_12 - e_11 - e_22.

The D4 descriptors do not determine this liquid-contact model uniquely. The molecular one-center
far-field approximation, contact diameters derived from cavity volumes, coordination z=10 and random
mole-fraction contact statistics are additional approximations. The molecular C6 is a sum over all
atom pairs between two molecular copies; it is not an intramolecular pair-energy sum requiring a
factor of one half. The retained D4/MMFF inputs have their own model provenance. No adjustment to
these inputs or dispersion weight was made to fit the present ThermoML comparison.

Refinements registered after the first results, before their own predictions: Z0e scales c_ES by the
COSMO dielectric factor f = (eps - 1)/(eps + 1/2) with eps from Onsager's equation (GFN2-xTB
dipoles, D4 polarizabilities, COSMO volumes), arithmetic mean over the pair. Z0x lets eps follow the
mixture composition (volume-fraction average) and defines an excess Gibbs energy from which chemical
potentials are differentiated. This construction is thermodynamically consistent analytically;
finite-difference implementation errors are assessed separately. The accepted P6 implementation uses
an analytic interior derivative. P28 supplies the exact pure endpoint of Z0x's same excess-Gibbs
model when ZC_R6_ENDPOINT=1; the adjacent finite-difference strip remains a distinct numerical
approximation. Historical tables below retain their original source versions and endpoint
conventions. Z0s made one train-selected choice among six dielectric variants (optical n^2, harmonic
mean) and is labeled accordingly.

### 2.4 Protocol
Metrics: MAE in ln gamma_inf; AAD in bubble pressure at measured T and x with the same pure-component
vapor pressures for every model; MAE of H^E and sign correctness for |H^E| > 20 J/mol; for LLE, the share of two-phase systems where a
gap is predicted (recall) and the false-positive rate on 336 systems observed homogeneous over the full
composition range (from VLE series), combined into a balanced accuracy. IDAC, VLE and HE comparisons use their source-specific common
finite-prediction subsets; those subsets differ by property and comparator list. LLE detection uses
its specified positive and negative system collections, with endpoint-composition errors reported on
separate accepted subsets. Historical 95% intervals use 1,000 bootstrap resamples over binary systems;
an interval spanning zero means no resolved difference, not demonstrated equality or equivalence. Pre-registration and every later change are in
`PREREGISTRATION.md`.

Later read-only and explanatory rounds retain their own exact observation identities, common inputs
and requested denominators. Their exposure, failures and amendments are recorded separately.
Bootstrap intervals from the original tables do not remove later adaptive exposure. LLE split
detection and checked endpoint compositions have separate denominators; neither is a global
phase-equilibrium certificate.

## 3. Results

Figures: `figures/fig1_idac_parity_test.png` (parity, held-out molecules),
`figures/fig2_hbond_constants.png`, `figures/fig3_tradeoff.png` (IDAC vs VLE error),
`figures/fig4_lle_detection.png`, `figures/fig5_error_map.png` (Z0x minus COSMO-SAC error by
chemical family).

### 3.1 Historical compound-test results

The leading historical findings are the unresolved IDAC difference from COSMO-SAC 2010, the reported
LLE detection advantage, and larger VLE/HE errors. The following historical summary is preserved
rather than rescored. It combines property-specific sources: main7 for the first IDAC, VLE and HE
columns, main7/test_both for the second IDAC column, and contemporaneous detection summaries for
balanced accuracy. It is not a single eight-model common-subset calculation. The HANNA row and
precise early LLE intervals have a separate source-status note in Supplement S0. Later explanatory
scores must not be subtracted from this table when observations or numerical versions differ.

| Model | IDAC MAE | IDAC, both unseen | VLE AAD P % (median) | H^E MAE J/mol | LLE balanced accuracy |
|---|---|---|---|---|---|
| Mod. UNIFAC (Dortmund) | 0.45 | 0.44 | 11.3 (3.1) | 314 | 0.81 |
| COSMO-SAC 2010 | 0.82 | 0.90 | 8.6 (3.6) | 399 | 0.84 |
| COSMO-SAC-dsp | 0.67 | 0.66 | 9.2 (3.6) | 399 | 0.83 |
| Z0 | 0.76 | 0.53 | 18.8 (6.2) | 532 | 0.90 |
| Z0e | 0.79 | 0.57 | 15.7 (4.6) | 521 | 0.90 |
| Z0s (one choice on train) | 0.95 | 1.00 | 12.8 (4.2) | 571 | 0.70 |
| Z0x (no new ThermoML parameter regression) | 0.76 | 0.55 | 14.2 (4.5) | 522 | 0.90 |
| HANNA (trained on DDB, reference) | 0.24* | 0.24* | 7.1 (2.1)* | 70* | 0.88 |

The main7 counts are 708 IDAC observations in 163 systems, 55 in 12 systems for test_both, 9,432 VLE
observations, and 6,311 HE observations. The historical LLE summary concerns 101 positive and 128
negative test systems. The original draft assigned 762 IDAC observations to the separately reported
HANNA row. Its precise historical VLE/HE common subsets and the underlying early detection/bootstrap
artifact were not recovered in this public-file audit. These entries are retained as historical
reported values, with their provenance qualification in Supplement S0, not independently reproduced
results.

On the named main7 source, the Z0-minus-COSMO-SAC 2010 IDAC interval is [-0.170, +0.069]; for
main7/test_both it is [-0.552, -0.229]. The latter concerns only 55 observations in 12 systems. Z0's
unfiltered main7 VLE AAD interval is [+6.76, +14.61] percentage points. Z0x's corresponding IDAC
interval is [-0.153, +0.065] and its VLE interval [+3.19, +7.96]. Thus the IDAC difference is
unresolved, while the pressure deficit is resolved within that historical comparison. Sources are
the stored main7 JSON/Markdown and test_both main7 Markdown, not new bootstrap calculations. The
contemporaneous progress record reports a significant LLE detection advantage over COSMO-SAC and
UNIFAC. The exact early bootstrap output should accompany that inferential claim before submission;
the unverified precision is not inferred from the rounded balanced-accuracy values. A claimed tie
with HANNA is not an equivalence result. Supplement S0 preserves the old interval strings and their
status.

### 3.2 Temporal set (2017 to 2019 publications)

| Model | IDAC MAE (median) | VLE AAD P % (median) | H^E MAE J/mol |
|---|---|---|---|
| Mod. UNIFAC (Dortmund) | 0.30 (0.19) | 7.0 (2.6) | 167 |
| COSMO-SAC 2010 | 0.70 (0.42) | 7.3 (3.6) | 270 |
| COSMO-SAC-dsp | 0.60 (0.30) | 7.1 (3.1) | 270 |
| Z0 | 1.19 (0.32) | 11.0 (5.7) | 308 |
| Z0e | 1.17 (0.36) | 9.7 (4.7) | 296 |
| Z0x | 1.03 (0.30) | 9.5 (4.7) | 301 |
| Z0s | 1.08 (0.41) | 8.9 (4.2) | 394 |
| HANNA (reference) | 0.11 (0.07) | 5.1 (2.0) | 93 |

254 IDAC points (54 systems), 7,722 VLE points, 2,058 H^E points. In this historical temporal
comparison, Z0x is significantly worse than COSMO-SAC on VLE (Z0x minus COSMO-SAC 2010: [+1.2, +3.3]
points) and on mean IDAC error, although their median IDAC error is comparable or lower; the larger
mean than median indicates skewed absolute errors; the aggregate table alone does not count how many
observations account for the mean.

### 3.3 Hydrogen-bond constants from quantum chemistry

| Class | Dimers | DFT-derived c_hb | Fitted COSMO-SAC 2010 |
|---|---|---|---|
| OH-OH | 5 | 5,712 +/- 538 | 4,014 |
| OH-OT | 7 | 5,988 +/- 1,032 | 3,016 |
| OT-OT | 5 | 5,611 +/- 1,833 | 932 |

The +/- entries above are the sample standard deviations across the listed dimers, not confidence
intervals. A composite CCSD(T)/CBS estimate (CCSD(T)/aug-cc-pVDZ plus an MP2 aug-cc-pVTZ
correction), not a fully converged CCSD(T) basis-limit calculation, was used at the same geometries
for five dimers. B3LYP-D4 interactions were more attractive by 0.33 to 0.85 kcal/mol (mean 0.59,
about 15%). The stored, specific exploratory HB variants changed IDAC MAE by at most about 0.05 and
VLE AAD by under one percentage point on their own common subsets. This describes the tested
interventions, not every possible 15-25% perturbation. Sources: results/qc/ccsdt_check.csv,
results/qc/hb_constants_by_class.csv and results/scorecard_test_sensitivity.md.

### 3.4 Earlier ablations, distinct from the Z0x factorial
The all-data ablation has 3,070 common IDAC and 33,303 common VLE observations. Replacing one fitted
piece of COSMO-SAC-dsp at a time: theoretical electrostatics costs +0.03 in IDAC MAE
(not significant) but +6 points in VLE AAD; DFT hydrogen-bond constants cost +0.13 in IDAC; London
dispersion costs +0.17 in IDAC and lowers the VLE AAD point estimate, but its paired VLE interval
includes zero. These values come from results/scorecard_all_ablation.md. The larger electrostatic coefficients in Z0/Z0e
favor some dilute-property and demixing results, whereas the smaller optical-screening coefficient in
Z0s trades those results for lower VLE error. These are conditional one-term sensitivities, not an
additive partition of the later Z0x-to-2010 gap. The all-data family table reports MAE 0.18 for Z0
versus 0.40 for COSMO-SAC 2010 and 1.05 for UNIFAC for alkene/alkyne solutes in aromatic solvents
(146 observations). For alkanes in alcohols it reports 0.66 versus 1.04 (456 observations).
Z0 errors are 3.7 for alcohols in alkanes (38 observations) and 3.4 in aromatic solvents (27).
These are descriptive selected family comparisons, not universal superiority claims or an unseen
subgroup validation. Source: results/error_map_idac_all_long.csv.

### 3.5 Registered association failure

The registered Z0w association model failed its criteria. Its stored IDAC comparison reports MAE
0.969 versus 0.800 for Z0x on 762 observations in 177 systems; the paired difference interval
[-0.035, +0.400] does not establish an overall IDAC difference. The historical VLE and aqueous-error
records motivated later unsuccessful association changes. The non-aqueous result was post hoc, not a
new holdout. Supplement S3 retains the historical numerical statements and separates publicly
verified entries from private-artifact-dependent precision. Sources: results/scorecard_test_z0w.md,
PROGRESS.md, and PREREGISTRATION.md.

### 3.6 Open-profile and numerical scope

Open profiles are an exploratory alternative input, not an accuracy-equivalent UD replacement. The
v1 agreement gate failed at median 0.153 against 0.15; v2 passed narrowly at 0.1493 on the original
25-molecule/2,302-occurrence check. The frozen population remains 630 original-gradient Berny
profiles plus one selected S1 and five selected S2 files. Later tests resolved omitted grid-response
errors in specific directions, but failed the P32 compatibility gate and did not resolve every TEG
gradient question. No corrected-gradient rollout or chain rescue was accepted. The infrastructure
record, including matched open-versus-UD errors and accepted/rejected changes, is in Supplement S1.
None of these qualifications changes the UD-backed historical tables in this paper.

### 3.7 Glycol explanation and its limit

The R10-R13 provenance and ordered-cross investigation explains a specific glycol-solvent
discrepancy. On 142 exposed observations with original open solutes, replacing only the solvent
input by the open method at the recovered UD coordinates changed MAE from 1.813 to 0.702, versus
0.419 for UD solvents. The 1.111 reduction is about 80% of the open-to-UD comparator gap and 61% of
the original open error. Tetraethylene glycol recovered only 13%; R11's whole-profile attribution
labels remained inconclusive. This establishes neither the liquid conformer distribution nor a
production geometry rule. P35 is closed and all profiles remain frozen. Supplement S2 contains the
finite-ensemble qualifications, lineage details and the exact endpoint/denominator record.

### 3.8 Continuum desolvation of the association term (Z0w2)

Z0w over-weighted aqueous association, so Z0w2 adds the electrostatic continuum desolvation of each
hydrogen-bonded contact, computed with the same BP86/def2-TZVP C-PCM model as the profiles at the
mixture's own fit-free permittivity. The correction is +0.9 to +2.1 kcal/mol for O-H...O contacts
(0.9 at eps = 2, 2.1 in the conductor limit), enough to cut water's association constant about
30-fold. It over-corrects. On the test split the IDAC MAE rises to 0.902 against 0.800 for Z0x
(paired difference +0.04 to +0.18), while LLE balanced accuracy stays at 0.887. Only about 13% of
water's donor sites remain bonded, far below the roughly 85% expected for the liquid. Because the
test split has now informed two association variants, the next variant (3.9) is judged first on the
temporal set.

### 3.9 Liquid-simulation association and software provenance

The simulation-informed Z0w3 also failed: its own temporal comparison reports IDAC MAE 2.19 against
1.45 for Z0x, with large aqueous errors. Those values have different source-specific subsets from
the main temporal table. Model force-equivalence checks and short liquid-structure controls did not
establish accurate chemical potentials or a uniquely identified double-counting mechanism. P55
separately repaired a later association-dispatch regression; archived Z0w-family results predate it
and remain unchanged. No new association score was run. Supplement S3 contains the historical
timings and accuracy records, with their precise numerical scope.

### 3.10 Dielectric ingredient and retrospective VLE oracle

R14/P51 screened 742 stored entries against a pinned public liquid-permittivity compilation using
exact identity and temperature rules. There were 248 valid matches at 298.15 K, with five additional
matched entries having invalid stored epsilon. The registered complete aggregate was therefore
withheld. Descriptive matched-only summaries are not substituted for that withheld aggregate or
interpreted as validation of the current Onsager approximation.

P52, after amendment P52a protecting the exact 630/1/5 profile selection, ran on 963 already-exposed
observations in 100 binary systems. All 2,889 requests were finite and the historical P6 baseline
replay matched. With identical UD profiles and frozen pure vapor pressures, row-weighted VLE AAD was
13.78% for stored-epsilon Z0x, 13.07% for experimental-epsilon Z0x, and 10.44% for COSMO-SAC 2010.
Equal-system AAD was 13.90%, 13.19% and 10.65%, respectively. From unrounded outputs, the oracle
removed about 0.72 percentage points, roughly 21% of the 3.35-point comparator gap; independently
rounded table entries need not subtract to the printed difference. There were 559 improved and 404
worsened rows. Experimental epsilon was held at its 298.15 K value throughout, so this was not an
epsilon(T) or HE test.

The oracle is an experimental-input, retrospective diagnostic, not a fit-free variant, a rigorous
headroom bound or a newly held-out score. The old main7 14.15/8.62 comparison uses a different
subset. R14 does not authorize a portfolio dielectric simulation campaign or identify a transferable
local contact coefficient. See `docs/astra/round14/RESULTS.md`.

### 3.11 Same-row factorial identifies the London closure as the leading VLE discrepancy

R15/P54 reused exactly P52's 963 exposed observations in 100 binary systems, with the original UD
profiles and frozen pure-component saturation pressures. Eight distinct E/H/D corners were evaluated
once, where E replaces the complete Z0x electrostatic closure by the 2010 temperature-dependent
rule, H replaces the hydrogen-bond constants, and D replaces London by no explicit dispersion, as in
2010. The sign mask, stored profiles and effective segment area were shared. Profile convention and
area therefore contribute zero to this endpoint difference, without being certified physically
exact.

| E H D corner | AAD P % | bias % | equal-system AAD % |
|---|---:|---:|---:|
| 000, stored-epsilon Z0x | 13.78 | +1.44 | 13.90 |
| 100 | 12.63 | -0.35 | 12.73 |
| 010 | 13.97 | +6.56 | 14.05 |
| 001, no explicit dispersion | 11.76 | -2.79 | 12.00 |
| 110 | 12.86 | +4.66 | 12.94 |
| 101 | 11.04 | -4.34 | 11.26 |
| 011 | 11.00 | +1.53 | 11.24 |
| 111, COSMO-SAC 2010 | 10.44 | -0.02 | 10.65 |

The game value was negative absolute percentage-pressure error. Shapley error reductions were 2.24
percentage points for dispersion (67%), 0.88 for the electrostatic closure (26%) and 0.23 for
hydrogen-bond constants (7%). The gap is 3.35 percentage points in the unrounded output. The H/D
interaction was +0.95 and the E/D interaction -0.43 percentage points in the baseline-anchored
inclusion/exclusion decomposition. Hydrogen-bond replacement slightly worsened error on its own; its
net Shapley benefit arose through interactions. These quantities allocate error under the specified
interventions and loss function, not intermolecular binding energy or universal causal shares.

The one-at-a-time London removal reduces AAD by 2.02 percentage points. Its bias change, computed
from the displayed corner biases, is -2.79 - 1.44 = -4.23 percentage points. The separate -4.47
value is the Shapley-allocated dispersion bias contribution, not this one-at-a-time difference.
Independently rounded AADs explain small arithmetic differences such as 13.78 - 10.44 versus the
reported 3.35; they do not explain conflating these two bias statistics.

All 7,704 requests were finite. The 1,926 anchor requests reproduced their saved P52 pressures
exactly before intermediate corners ran, and the Shapley efficiency residual was at most 3e-14
percentage points. The run took 722 seconds on the Mac, without quantum calculations or a retry.
These are execution and accounting checks, not a new held-out accuracy certificate. See
`docs/astra/round15/RESULTS.md` for the source record and its test-environment qualification.

P54 changes the priority inferred from the earlier conductor-limit Z0 ablation: dispersion is the
leading contribution to this Z0x-to-2010 comparison. R14's approximately 21% epsilon-oracle recovery
and P54's ES share overlap and must not be added. Neither the best fitted corner nor removal of
London is adopted. Every historical model table and the 630+6 open profiles remain unchanged.

#### Registered negative result: LV1

R16/P58 tested exactly one registered A alternative, LV1, a cohesive-density volume regular-solution
replacement using the same molecular C6, polarizabilities and cavity volumes. The dispersion weight
remained one and z remained ten. It retained the existing residual and combinatorial model; it was
not a fitted weight or an adopted deletion of London. The design was motivated by the inspected P54
result and frozen before LV1 predictions. It was an exposed development screen, not a new holdout.

| Property and fixed collection | Z0x | LV1 | Reported change | Paired uncertainty / registered gate |
|---|---:|---:|---:|---|
| VLE AAD %, 963 observations / 100 systems | 13.78 | 13.13 | -0.65 pp | 95% CI [-1.72, +0.13]; one-sided upper +0.02; fail |
| IDAC MAE, 828 observations / 204 systems | 0.840 | 0.875 | +0.035 | 95% CI [+0.008, +0.067]; fail |
| HE MAE J/mol, 8,573 observations / 348 systems | 618.6 | 632.9 | +14.2 | 95% CI [+4.6, +25.1]; fail |
| HE sign correct, 8,316 observations | 0.838 | 0.834 | -0.004 | Non-worsening gate fails |
| LLE recall, 101 positive systems | 0.842 | 0.842 | 0 | One-sided lower 0; pass |
| LLE balanced accuracy | 0.893 | 0.897 | +0.004 | One-sided lower -0.008; fail |
| LLE false-positive rate, 128 negative systems | 0.055 | 0.047 | -0.008 | One-sided upper +0.016; fail |

The +14.2 J/mol HE change is the recorded result from unrounded values; subtraction of the
separately rounded endpoints gives +14.3. No historical value is replaced. All 171,701 baseline
requests were finite, all 963 VLE anchors replayed exactly, and no LLE grid job was unresolved. The
LLE screen used its registered two-grid detection rule and is not a new binodal-composition or
global-stability result. P58a excluded 51 pure-composition HE inputs before model calls, matching
the original evaluator's scope. The single run took 2,219 seconds and performed no quantum
calculation. The software test record retains its two macOS temporary-path assertion errors; it is
not reported as an all-platform pass.

LV1 failed the joint registered screen. Its pressure decrease did not meet the uncertainty gate, and
its IDAC and HE errors increased on the specified exposed collections. Its VLE AAD of 13.13% also
remains above the same-row COSMO-SAC 2010 value of 10.44%. No term removal, fitted corner, LV1
adoption, alternative weight or second candidate followed. This negative result closes the present
model-development campaign; it does not prove that all scalar-descriptor alternatives or all future
contact theories must fail. Source: docs/astra/round16/RESULTS.md and the R16/P58a registration.

## 4. Discussion

The historical benchmark shows that specified theory-derived interaction constants can retain useful
IDAC and demixing performance within a common COSMO-SAC framework. Z0x remains worse than COSMO-SAC
2010 for VLE on the displayed main7 and temporal subsets. This supports a quantitative account of
the tradeoff, without claiming that all empiricism has been removed or that the model is generally
competitive.

The strongest later explanatory result is P54's dispersion attribution on the fixed P52
observations. It is more directly relevant to the remaining Z0x discrepancy than the original
conductor-limit Z0 ablation. Bulk permittivity and local contact response remain different
quantities, but the small R14 oracle effect does not justify treating dielectric error as the
dominant unresolved cause. The London closure should be described as an approximate conversion of
electronic descriptors into an excess mixing free energy. P54 identifies that conversion as a
leading source of benchmark discrepancy; it does not isolate one failed geometric assumption or
prove double counting.

For positive C6, polarizabilities and cavity volumes, the implemented London exchange is
nonnegative: its unlike C6 does not exceed the geometric mean of its self coefficients, and its
arithmetic-mean contact diameter is at least their geometric mean. Consequently its Margules
contribution raises both component activities and bubble pressure relative to the same residual
without it. That restriction can increase or reduce absolute pressure error depending on the row. A
change to volume contact statistics requires differentiating a complete excess Gibbs energy, not
merely replacing mole fractions in a gamma formula. LV1 made that declared change and failed: its
VLE decrease was unresolved by the registered gate, while IDAC and HE errors increased. This is a
negative result for that particular cohesive-density closure, not evidence that actual London
dispersion should be absent or that the original molecular descriptors are intrinsically wrong. The
P54 fitted corners remain diagnostics and cannot be selected as models by their lower error.

Neither P54 nor the failed LV1 screen establishes a transferable contact kernel or identifies one
uniquely missing physical effect. Electronic response, contact geometry and the pure-reference
partition remain approximations of the implemented model. Their unresolved status is a limitation of
this completed study, not an authorization for another model or native calculation.

Association and direct simulation remain separate research programs. Reproducing a bonded fraction
does not validate the site thermodynamics, and an energy/force model does not automatically validate
its field response or chemical potentials. The numerical association repair changes neither the
archived scientific failures nor this assessment. The present work is being finalized with P54 as
the centerpiece of the later VLE explanation and LV1 as its registered negative follow-up. The VLE
gap remains open. The model-development question is closed for this project, with no additional
experiment, revised weight or model variant proposed. Submission preparation is limited to the
stated bibliography and historical-artifact checks. Such checks may recover existing evidence, but
do not authorize rescoring to manufacture missing precision.

## 5. Limitations

The retained effective area and combinatorial constants, sigma-processing conventions and empirical
history of some UD conformations limit the meaning of "fit-free". Z0/Z0x interaction constants were
not regressed to ThermoML. Z0s involves a train-selected discrete choice; Z1 is a fitted comparison.
VLE uses the same experimental pure-component vapor-pressure correlations in every arm. UD-backed
main results and exploratory open-profile results are different input versions.

The original compound and 2017-2019 temporal collections were repeatedly inspected during later
development. Neither is certified unexposed for another adaptive variant, and no new multi-system
holdout or data beyond HANNA's training has been certified. Historical confidence intervals keep
their original scope. Later explanatory ratios have no claimed generalization confidence interval.

The 630 original-gradient profiles and six S1/S2 profiles retain their actual provenance. A passed
historical agreement threshold is not proof of corrected-gradient stationarity, a liquid conformer
ensemble or equivalence to UD. P35's retrospective coordinate explanation and its tetraEG exception
do not identify a production geometry rule. LLE detection does not certify global stability or every
reported composition. Claims about new source versions require separate numerical checks.

## Data and code availability

The repository contains source code, registrations and public aggregate result records. UD-derived
geometries and detailed R10-R16 profile/prediction artifacts remain private on the Mac under the
applicable data-use terms. Some historical predictions and execution inputs are private or
untracked; a public checkout alone is not asserted to reproduce every historical table. Public
result records retain plan digests and scope, and their instructions identify required private
assets without redistributing them.

## Figure captions

**Figure 1.** Predicted vs experimental ln gamma_inf for held-out molecules (test split, common
subset of 762 points in 177 systems) for COSMO-SAC 2010, modified UNIFAC (Dortmund), Z0x and HANNA.
HANNA training overlap with these observations is possible and has not been resolved row by row.

**Figure 2.** Hydrogen-bond constants c_hb derived from 17 counterpoise-corrected B3LYP-D4/def2-TZVP
dimers (points; bars are class means) compared with the fitted COSMO-SAC 2010 values (blue bars).

**Figure 3.** Trade-off between infinite-dilution accuracy (IDAC MAE, x axis) and bubble-pressure
accuracy (VLE AAD, y axis) in the historical compound-test comparison. Larger electrostatic
coefficients (Z0, Z0e) favor some dilute properties; the smaller optical-screening prescription
(Z0s) improves VLE at the expense of other metrics. These are exposed comparisons, not evidence for
one optimal coefficient.

**Figure 4.** Historical liquid-liquid split detection: recall on the positive test-system
collection versus false-positive rate on the negative collection. This is one operating point per
model, not a threshold-swept ROC curve. The archived image exists; exact historical arrays and rates
require the already-generated private source artifacts identified in the figure audit.

**Figure 5.** Z0x absolute error minus COSMO-SAC 2010 absolute error in ln gamma_inf by solute and
solvent family (all data, cells with at least 10 points). Blue: Z0x better; orange: COSMO-SAC
better.

## Supplementary material (files in the repository)

S1 Pre-registration and every later change: `PREREGISTRATION.md`. S2 Benchmark construction,
rejection log and split hash: `data/benchmark/`, `data/processed/rejections.csv`. S3 Dimer
geometries and energies, CCSD(T) check, association thermochemistry: `results/qc/`. S4 All
scorecards with bootstrap intervals: `results/scorecard_*.md`. S5 Error maps by chemical family:
`results/error_map_idac_*.csv`. S6 Open-profile validation and conformer comparison:
`results/pyscf_profile_validation.csv`,    `data/pyscf_sigma/conformer_summary.csv` (asset
availability is stated above). S7 Later numerical, glycol, dielectric and dispersion evidence:
`docs/astra/round2/RESULTS.md` through    `docs/astra/round16/RESULTS.md`, with the registrations
and private-plan digests referenced there. S8 Supplementary narrative: `manuscript/supplement.md`;
claim and reference audit:    `docs/astra/round17/CLAIMS.json` and
`docs/astra/round17/REFERENCES.md`.

## References

1. Klamt, A. Conductor-like Screening Model for Real Solvents: A New Approach to the Quantitative Calculation
   of Solvation Phenomena. J. Phys. Chem. 1995, 99 (7), 2224-2235. doi:10.1021/j100007a062.
2. Lin, S.-T.; Sandler, S. I. A Priori Phase Equilibrium Prediction from a Segment Contribution Solvation
   Model. Ind. Eng. Chem. Res. 2002, 41 (5), 899-913. doi:10.1021/ie001047w.
   Related correction: Ind. Eng. Chem. Res. 2004, 43 (5), 1322. doi:10.1021/ie0308689.
3. Mullins, E. et al. Sigma-Profile Database for Using COSMO-Based Thermodynamic Methods.
   Ind. Eng. Chem. Res. 2006, 45 (12), 4389-4415. doi:10.1021/ie060370h.
4. Hsieh, C.-M.; Sandler, S. I.; Lin, S.-T. Improvements of COSMO-SAC for Vapor-Liquid and Liquid-Liquid
   Equilibrium Predictions. Fluid Phase Equilib. 2010, 297 (1), 90-97. doi:10.1016/j.fluid.2010.06.011.
5. Hsieh, C.-M.; Lin, S.-T.; Vrabec, J. Considering the Dispersive Interactions in the COSMO-SAC Model for
   More Accurate Predictions of Fluid Phase Behavior. Fluid Phase Equilib. 2014, 367, 109-116.
   doi:10.1016/j.fluid.2014.01.032. Corrigendum: 2014, 384, 14-15, doi:10.1016/j.fluid.2014.10.019
   (publisher text and implications remain to be checked; no numerical result is reinterpreted here).
6. Bell, I. H.; Mickoleit, E.; Hsieh, C.-M.; Lin, S.-T.; Vrabec, J.; Breitkopf, C.; Jäger, A.
   A Benchmark Open-Source Implementation of COSMO-SAC. J. Chem. Theory Comput. 2020, 16 (4), 2635-2646.
   doi:10.1021/acs.jctc.9b01016.
7. Gmehling, J.; Li, J.; Schiller, M. A Modified UNIFAC Model. 2. Present Parameter Matrix and Results for
   Different Thermodynamic Properties. Ind. Eng. Chem. Res. 1993, 32 (1), 178-193. doi:10.1021/ie00013a024.
8. Hoffmann, M.; Specht, T.; Göttl, Q.; Burger, J.; Mandt, S.; Hasse, H.; Jirasek, F.
   Thermodynamically Consistent Machine Learning Model for Excess Gibbs Energy.
   Nat. Commun. 2026, 17, 3485. doi:10.1038/s41467-026-71430-y.
9. Frenkel, M. et al. ThermoML: An XML-Based Approach for Storage and Exchange of Experimental and Critically
   Evaluated Thermophysical and Thermochemical Property Data. 1. Experimental Data.
   J. Chem. Eng. Data 2003, 48 (1), 2-13. doi:10.1021/je025645o.
10. Herington, E. F. G. Tests for the Consistency of Experimental Isobaric Vapour-Liquid Equilibrium Data.
    J. Inst. Petrol. 1951, 37, 457. Provisional: the original publisher record/title/page range has not
    been verified in this audit. Do not invent a DOI or infer the missing range.
11. Onsager, L. Electric Moments of Molecules in Liquids. J. Am. Chem. Soc. 1936, 58 (8), 1486-1493.
    doi:10.1021/ja01299a050.
12. Wertheim, M. S. Fluids with Highly Directional Attractive Forces. I. Statistical Thermodynamics.
    J. Stat. Phys. 1984, 35, 19-34. doi:10.1007/BF01017362; II. Thermodynamic Perturbation Theory and
    Integral Equations, 1984, 35, 35-47, doi:10.1007/BF01017363; III. Multiple Attraction Sites,
    1986, 42, 459-476, doi:10.1007/BF01127721; IV. Equilibrium Polymerization,
    1986, 42, 477-492, doi:10.1007/BF01127722.
13. Caldeweyher, E. et al. A Generally Applicable Atomic-Charge Dependent London Dispersion Correction.
    J. Chem. Phys. 2019, 150, 154122. doi:10.1063/1.5090222. Direct publisher verification remains
    outstanding; the author record supports the bibliographic identity.
14. Bannwarth, C.; Ehlert, S.; Grimme, S. GFN2-xTB: An Accurate and Broadly Parametrized Self-Consistent
    Tight-Binding Quantum Chemical Method with Multipole Electrostatics and Density-Dependent Dispersion
    Contributions. J. Chem. Theory Comput. 2019, 15 (3), 1652-1671. doi:10.1021/acs.jctc.8b01176.
15. Grimme, S. Supramolecular Binding Thermodynamics by Dispersion-Corrected Density Functional Theory.
    Chem. Eur. J. 2012, 18 (32), 9955-9964. doi:10.1002/chem.201200497.
16. Sun, Q. et al. Recent Developments in the PySCF Program Package. J. Chem. Phys. 2020, 153, 024109.
    doi:10.1063/5.0006074.
17. Boys, S. F.; Bernardi, F. The Calculation of Small Molecular Interactions by the Differences of Separate
    Total Energies. Some Procedures with Reduced Errors. Mol. Phys. 1970, 19 (4), 553-566.
    doi:10.1080/00268977000101561.
18. Constantinescu, D.; Gmehling, J. Further Development of Modified UNIFAC (Dortmund): Revision and
    Extension 6. J. Chem. Eng. Data 2016, 61 (8), 2738-2748. doi:10.1021/acs.jced.6b00136.
    The installed DOUFIP2016 table/version still needs an execution-artifact citation, beyond this paper.

Bibliographic metadata verification is not verification of every methodological assertion in an article.
The reference audit lists outstanding publisher and software/model-version checks before submission.
