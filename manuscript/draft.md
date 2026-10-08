# Replacing COSMO-SAC interaction constants without ThermoML regression: a pre-registered benchmark

Victor Liang (original draft 2026-09-24; evidence and scope updated 2026-10-08)

## Abstract

COSMO-SAC replaces binary-specific regression with molecular surface profiles and shared interaction
parameters. We ask how much accuracy is retained when its electrostatic and hydrogen-bond coefficients
and dispersion prescription are supplied by theory or quantum chemistry without regression to ThermoML. In the resulting model, Z0, the electrostatic misfit coefficient follows from Klamt's
estimate in the conductor limit, the three hydrogen-bond constants come from 17 counterpoise-corrected
B3LYP-D4/def2-TZVP dimer energies, and dispersion enters through a London term built from D4 molecular
C6 coefficients and polarizabilities. Z0 and Z0x do not regress their interaction constants to the
ThermoML benchmark. They retain the standard effective area and combinatorial normalization constants,
along with inherited profile-processing conventions. UD reference geometries have documented empirical
selection history, and VLE uses experimental pure-component vapor-pressure correlations. The claim is
therefore absence of new benchmark regression, not absence of every empirical upstream input.

We score Z0, two dielectric-screening refinements (Z0e, Z0x), COSMO-SAC 2010, COSMO-SAC-dsp and
modified UNIFAC (Dortmund) on a benchmark built from 9,184 ThermoML files (3,438 infinite-dilution
activity coefficients, 46,127 VLE, 7,158 LLE and 27,366 excess-enthalpy points), with a molecule-level
held-out split frozen before any model was run, and on a temporal set of 2017 to 2019 publications that
provide an additional historical collection. HANNA is included as a data-driven reference, with possible
training overlap. The original split was frozen prospectively, but later model development examined both
collections repeatedly; subsequent explanatory analyses do not constitute new untouched validation.

On held-out molecules Z0 matches COSMO-SAC 2010 for infinite-dilution activity coefficients (MAE in
ln gamma 0.76 vs 0.82, difference not significant) and detects liquid-liquid demixing more reliably than
both COSMO-SAC and UNIFAC (balanced accuracy 0.90 vs 0.84 and 0.81, significant). It is clearly worse for
bubble pressures (AAD 18.8% vs 8.6%) and on the temporal set. The DFT-derived hydrogen-bond constants are
nearly identical across the three COSMO-SAC classes (about 5,700 kcal A^4 mol^-1 e^-2), whereas the fitted
constants span 4,014 to 932. Earlier one-term ablations identify the electrostatic prescription as an
important sensitivity. Composition-dependent screening in Z0x reduces the historical VLE AAD to 14.2%.
A later retrospective diagnostic on a separate 963-row subset changes AAD from 13.78% to 13.07% when
experimental pure-liquid permittivities replace the stored estimates, versus 10.44% for COSMO-SAC 2010.
This small bulk-permittivity effect leaves the local contact approximation as an unresolved hypothesis,
not an established universal cause or an accepted new coefficient. HANNA, where its
training data reach, is far more accurate than every physics-based model, but it does not detect demixing
more reliably than Z0 on held-out molecules.

## 1. Introduction

Process simulators describe liquid mixtures mostly with correlative excess-Gibbs-energy models such as
NRTL and UNIQUAC, whose binary parameters are regressed from measurements of the same binary. When no
data exist, engineers fall back on predictive models. Group-contribution methods (modified UNIFAC) need
group-interaction parameters fitted to large databases and cannot treat groups that were never
parameterized. COSMO-RS and COSMO-SAC replace groups by the screening-charge distribution of each
molecule, computed with density functional theory in a conductor, and so apply to any molecule whose
structure is known. Their interaction model, however, still carries a small set of universal constants
(an effective contact area, the electrostatic misfit coefficient and its temperature dependence,
hydrogen-bond strengths and cutoffs, and in later versions dispersion parameters) that are fitted to
experimental infinite-dilution activity coefficients and phase equilibria. Published variants have refit shared parameters for different electronic-structure recipes. Their
reported accuracy must therefore be distinguished from that of the present no-new-regression variants.

Data-driven models have meanwhile become very accurate. HANNA, a thermodynamically consistent neural
network trained on about 824,000 Dortmund Data Bank points, outperforms modified UNIFAC across binary
VLE, LLE, infinite dilution and excess enthalpy. Where training data are dense, the case for
physics-based models therefore rests less on accuracy than on transferability and interpretability.

That case is only as strong as the physics is real. If COSMO-SAC's accuracy is carried mainly by its
fitted constants, it is a compact regression model; if it is carried by the sigma profiles, the constants
may admit more transferable physical estimates. We test specified replacements of the interaction
constants and dispersion model, while retaining the common molecular-surface and combinatorial
conventions. The benchmark and initial metrics were registered before predictions. Subsequent changes
were registered before their own execution, with prior exposure stated. Ablations identify conditional
model sensitivities; they do not uniquely identify a missing physical mechanism.

## 2. Methods

### 2.1 Data
ThermoML XML files (MobleyLab mirror of the NIST/TRC archive, publications to mid-2017) were flattened and
compounds resolved to InChIKeys offline, accepting a match only when the molecular formula agreed.
Scope: neutral molecules of C, H, N, O, F, Cl, Br, S with at most 25 heavy atoms, 250 to 450 K, pressures
below 500 kPa, both components subcritical. Quality filters: repeated IDAC measurements within 2 K had to
agree within 0.2 in ln gamma; VLE series with vapor compositions had to pass the Herington area test; LLE
systems needed both coexisting branches or at least five cloud points. Every rejection is logged.

Twenty percent of in-scope compounds were held out (seed 20260924, water always in training). Rows with
one held-out component form `test_one`, with two `test_both`. The split was hashed before any Z-model
prediction. A temporal set was built later from the complete NIST 2020 archive (11,923 files, standard
InChIKeys): rows from files absent from the 2017 mirror, i.e. publications from mid-2017 to 2019. These
postdate the fitting of COSMO-SAC 2010 (2010), COSMO-SAC-dsp (2014) and the UNIFAC parameter table used
(2016). This is the historical provenance description of those parameter tables, not proof that every
reference model or upstream input is unexposed to these measurements. HANNA may overlap these data.
Neither this temporal collection nor the repeatedly examined compound test split is a fresh holdout for
R10-R15 development. A future validation needs a custodian-led source and duplicate-series audit before
responses are revealed; relabeling an existing split cannot restore independence.

### 2.2 Reference models
COSMO-SAC 2010 and -dsp were reimplemented in NumPy and reproduce the NIST benchmark code (Bell et al.,
JCTC 2020) to 2e-9 in ln gamma on 400 random pairs. All COSMO models use the same NIST UD sigma
profiles (DMol3 BP/DNP, 2,259 compounds). Modified UNIFAC (Dortmund) uses the `thermo` package with
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

Refinements registered after the first results, before their own predictions:
Z0e scales c_ES by the COSMO dielectric factor f = (eps - 1)/(eps + 1/2) with eps from Onsager's equation
(GFN2-xTB dipoles, D4 polarizabilities, COSMO volumes), arithmetic mean over the pair. Z0x lets eps follow
the mixture composition (volume-fraction average) and defines an excess Gibbs energy from which
chemical potentials are differentiated. This construction is thermodynamically consistent analytically;
finite-difference implementation errors are assessed separately. The accepted P6 implementation uses an
analytic interior derivative. P28 supplies the exact pure endpoint of Z0x's same excess-Gibbs model when
ZC_R6_ENDPOINT=1; the adjacent finite-difference strip remains a distinct numerical approximation.
Historical tables below retain their original source versions and endpoint conventions. Z0s made one
train-selected choice among six dielectric variants (optical n^2, harmonic mean) and is labeled accordingly.

### 2.4 Protocol
Metrics: MAE in ln gamma_inf; AAD in bubble pressure at measured T and x with the same pure-component
vapor pressures for every model; MAE of H^E and its sign; for LLE, the share of two-phase systems where a
gap is predicted (recall) and the false-positive rate on 336 systems observed homogeneous over the full
composition range (from VLE series), combined into a balanced accuracy. All comparisons use rows every
model can predict. 95% intervals come from 1,000 bootstrap resamples over binary systems; a difference
counts when the paired interval excludes zero. Pre-registration and every later change are in
`PREREGISTRATION.md`.

Later read-only and explanatory rounds retain their own exact observation identities, common inputs
and requested denominators. Their exposure, failures and amendments are recorded separately. Bootstrap
intervals from the original tables do not remove later adaptive exposure. LLE split detection and checked
endpoint compositions have separate denominators; neither is a global phase-equilibrium certificate.

## 3. Results

Figures: `figures/fig1_idac_parity_test.png` (parity, held-out molecules), `figures/fig2_hbond_constants.png`,
`figures/fig3_tradeoff.png` (IDAC vs VLE error), `figures/fig4_lle_detection.png`,
`figures/fig5_error_map.png` (Z0x minus COSMO-SAC error by chemical family).

### 3.1 Historical compound-test results

These are the original main7 comparisons, preserved rather than regenerated with later code. See
`results/scorecard_test_main7.md` and its source-specific common subsets. Later explanatory scores must
not be subtracted from these values when their observation sets or numerical versions differ.

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

IDAC: 708 points in 163 systems (both unseen: 55 points, 12 systems). VLE: 9,432 points. LLE: 101
two-phase and 128 homogeneous test systems. *HANNA values are on the slightly larger common subset
without Z0s (762 IDAC points); HANNA has very likely seen these systems in training.

Key intervals: Z0 minus COSMO-SAC 2010 IDAC MAE [-0.17, +0.08] (tie); both unseen [-0.54, -0.22] (Z0
better, small sample); LLE balanced accuracy Z0 minus COSMO-SAC [+0.02, +0.11], Z0 minus UNIFAC
[+0.04, +0.14]; VLE AAD Z0 minus COSMO-SAC [+6.6, +14.5] points. Z0x keeps the IDAC tie ([-0.15, +0.07])
and the LLE advantage over COSMO-SAC ([+0.02, +0.11]) and UNIFAC ([+0.03, +0.13]) while cutting the VLE
deficit to [+3.2, +8.0] points. On LLE detection Z0 and Z0x tie HANNA on the test split
(Z0x minus HANNA [-0.03, +0.07]); HANNA's binodal compositions are far more accurate (0.05 vs 0.18).

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

254 IDAC points (54 systems), 7,722 VLE points, 2,058 H^E points. In this historical temporal comparison,
Z0x is significantly worse than COSMO-SAC on VLE (Z0x minus COSMO-SAC 2010:
[+1.2, +3.3] points) and on mean IDAC error, although their median IDAC error is comparable or lower; the
mean is carried by a small number of large misses.

### 3.3 Hydrogen-bond constants from quantum chemistry

| Class | Dimers | DFT-derived c_hb | Fitted COSMO-SAC 2010 |
|---|---|---|---|
| OH-OH | 5 | 5,712 +/- 538 | 4,014 |
| OH-OT | 7 | 5,988 +/- 1,032 | 3,016 |
| OT-OT | 5 | 5,611 +/- 1,833 | 932 |

A CCSD(T)/CBS check (CCSD(T)/aug-cc-pVDZ plus an MP2 aug-cc-pVTZ correction) at the same geometries on five
dimers shows B3LYP-D4 overbinding by 0.33 to 0.85 kcal/mol (mean 0.59, about 15%). Sensitivity runs show
that a 15 to 25% change in c_hb, a different segment-pairing closure, or a single universal c_hb for all
classes moves IDAC MAE by at most 0.05 and VLE AAD by under one point.

### 3.4 Which term carries the error
Replacing one fitted piece of COSMO-SAC-dsp at a time: theoretical electrostatics costs +0.03 in IDAC MAE
(not significant) but +6 points in VLE AAD; DFT hydrogen-bond constants cost +0.13 in IDAC; London
dispersion costs +0.17 in IDAC and slightly helps VLE. The larger electrostatic coefficients in Z0/Z0e
favor some dilute-property and demixing results, whereas the smaller optical-screening coefficient in
Z0s trades those results for lower VLE error. These are conditional one-term sensitivities, not an
additive partition of the later Z0x-to-2010 gap. By chemical family, Z0 is
the most accurate model for nonpolar solutes in aromatic solvents (alkenes in aromatics: 0.18 vs 0.40 for
COSMO-SAC and 1.05 for UNIFAC) and for alkanes in alcohols (0.66 vs 1.04), and fails for self-associating
solutes in inert solvents (alcohols in alkanes 3.7, in aromatics 3.4).

### 3.5 A first-principles association term (Z0w)
Z0w replaces the COSMO hydrogen-bond term by Wertheim TPT1 association with site-pair strengths
Delta_AB = (kT/P0) exp(-dG_AB/RT), where dG_AB is the dimerization free energy from the B3LYP-D4 binding
energy plus GFN2-xTB quasi-RRHO thermochemistry (registered before any prediction). As registered it fails:
held-out IDAC MAE 0.97 vs 0.80 for Z0x and VLE AAD 27.4% vs 15.2%, and it predicts false liquid-liquid
splits in 9.4% of miscible test systems (balanced accuracy 0.90, unchanged, because it finds more real
splits). The failure is entirely aqueous: organic solutes in water are overpredicted by 5 to 7 in
ln gamma_inf. Post hoc, on non-aqueous systems only, Z0w is the most accurate physics model (test IDAC MAE
0.67 vs 0.88 for COSMO-SAC 2010, bootstrap difference [-0.29, -0.09]; vs Z0x [-0.17, +0.04]). The
diagnosis is the gas-phase entropy in dG: bonding to a larger partner costs more rotational entropy
(water-acetone -121 J/mol/K vs water-water -87 J/mol/K), which makes cross-association about ten times
weaker than water self-association and turns water into an unrealistically closed network.

### 3.6 Coverage: open-source profiles for missing compounds
An open pipeline (PySCF BP86/def2-TZVP, C-PCM conductor limit, xTB geometries, NIST averaging and
splitting) was checked against the NIST/DMol3 profiles before use. On 25 molecules and 2,302 IDAC rows the
median change in COSMO-SAC-dsp ln gamma_inf was 0.153, just above the pre-set bar of 0.15 (water 1.14,
triethylene glycol 0.84), while accuracy against experiment was similar (MAE 0.79 vs 0.74). The profiles
were therefore not merged into the main benchmark. On the 136 previously uncovered compounds (exploratory,
218 IDAC points in 72 systems), Z0 and Z0x reach MAE 0.68 and 0.69 against 1.00 for COSMO-SAC 2010,
0.94 for COSMO-SAC-dsp, 0.55 for UNIFAC (79% coverage) and 0.11 for HANNA.

Later v2 conductor-optimized profiles passed the original median agreement gate at 0.1493, only 0.0007
below 0.15, and were retained as exploratory rather than an accuracy-equivalent UD replacement. The
frozen population contains 630 files passing the original Berny predicate and six separately flagged
S1/S2 files. The R2-R9 numerical review preserves accepted performance changes and rejected trials;
optimizer-state persistence is not relabeled E after its E gate failed. Omitted XC-grid response and the
incomplete earlier finite-difference referee limit stationarity claims. The corrected-gradient rollout
failed P32's compatibility gate, and the TEG energy-gradient mismatch remained unresolved when the
R8/R9 diagnostic budget closed. There is no accepted blanket re-polish or chain rescue. See
`docs/astra/round7/RESULTS.md`, `docs/astra/round8/RESULTS.md` and `docs/astra/round9/RESULTS.md`.

### 3.7 Conformer ensembles
For the 50 most flexible benchmark molecules (4.9 conformers on average, BP86/def2-SVP profiles), replacing
the lowest-energy conformer by the Boltzmann ensemble changed predictions very little: median
|d ln gamma_inf| 0.009 (COSMO-SAC-dsp) and 0.011 (Z0x), 90th percentile under 0.09, and no significant change
in accuracy (IDAC MAE difference [0.00, +0.01]; VLE [-0.35, +0.32] points). The lowest conformer carries
60% of the weight on average. This establishes a small effect for that finite proposal and weighting
scheme, not the absence of conformational effects or a validated phase-dependent ensemble.

R10 recovered and replayed all twelve fixed-panel UD raw files to their historical profiles. R11's
ordered open-method cross attributes the polar-tail gaps for ethylene, diethylene and triethylene glycol
mainly to stored coordinate inputs, including hydrogen positions and orientation. Tetraethylene glycol
is an exception: its raw-tail gap was mainly method, and its other tail contrasts were small. No member
passed the registered whole-profile attribution rule. These statements retain R11's original labels.

R12/P46a then scored exactly 142 already-inspected glycol-solvent observations with original open solutes
and a common P28 endpoint. Pooled MAE in ln gamma_inf was 1.813 for the original open solvent profiles,
0.702 for the open method at the recovered UD coordinates, and 0.419 for UD solvent profiles. The
coordinate-derived substitution removed 1.111, about 80% of the open-to-UD comparator MAE gap and 61% of
the original open absolute error; 139 rows improved and three worsened. Shape carried essentially all
of the factorial error reduction. Tetraethylene glycol recovered only 13% of its comparator gap. The
remaining 0.283 is a conditional difference of MAEs, not a universal method-error estimate. P47 located
same-geometry method differences toward the acceptor side and the EG/DEG/TEG coordinate differences
toward the donor-side tail; those partitions are not hydrogen-bond energies or binwise error causes.

This was retrospective explanatory ThermoML scoring. The UD notice reports database-level revisions
using vapor-pressure predictions without identifying which panel members were revised. The result does
not establish extended chains as the liquid conformations or adopt a geometry rule. P35 closed after
R13 with its explanatory finding; the liquid distribution remains unresolved and all 630+6 open files
remain frozen. See `docs/astra/round10/RESULTS.md` through `docs/astra/round13/RESULTS.md`.

### 3.8 Continuum desolvation of the association term (Z0w2)

Z0w over-weighted aqueous association, so Z0w2 adds the electrostatic continuum desolvation of each
hydrogen-bonded contact, computed with the same BP86/def2-TZVP C-PCM model as the profiles at the mixture's
own fit-free permittivity. The correction is +0.9 to +2.1 kcal/mol for O-H...O contacts (0.9 at eps = 2,
2.1 in the conductor limit), enough to cut water's association constant about 30-fold. It over-corrects.
On the test split the IDAC MAE rises to 0.902 against 0.800 for Z0x (paired difference +0.04 to +0.18),
while LLE balanced accuracy stays at 0.887. Only about 13% of water's donor sites remain bonded, far below
the roughly 85% expected for the liquid. Because the test split has now informed two association variants,
the next variant (3.9) is judged first on the temporal set.

### 3.9 A first-principles liquid-simulation teacher

The association constants that a continuum or gas-phase dimer calculation cannot supply can be measured
directly in simulated liquids. We use MACE-OFF23 (small), a machine-learned interatomic potential trained
only on DFT reference data, as a teacher. Speed was the obstacle: the stock ASE path managed 0.37 ns/day for
648 water atoms on an NVIDIA L4. Three exact changes remove most of it. The first is NVIDIA's
cuEquivariance fused tensor-product kernels (forces identical to 2-4e-6 eV/A). The second is batching many
small boxes per GPU. The third is a lean integrator that feeds the model directly, with a Verlet neighbour
list whose superset is filtered to the cutoff every step. This is exact because MACE's radial envelope is
identically zero beyond r_max. Aggregate throughput reaches 8.9 ns/day (about 24x), with every change
checked against reference forces. Two approximations were rejected by pre-registered gates: TF32 arithmetic
(force error 3e-3 eV/A) and hydrogen mass repartitioning with 1-2.5 fs steps (energy drift 2.3-183 times the
0.5 fs reference). Z0w3 inverts TPT1 on hydrogen-bond statistics from NPT simulations of seven liquids at
three temperatures (PREREGISTRATION.md, session 5b). The teacher is physically reasonable (water 87% bonded,
1.115 g/cm3; an independent engine gives 86% and 1.10), but Z0w3 fails badly: temporal IDAC MAE 2.19 against
1.45 for Z0x, aqueous test systems 4.79 against 1.76. The simulated association is strong (water Delta about
ten times the gas-phase dimer value). Overlap with electrostatic contributions in the COSMO reference is
a plausible architectural explanation. The explicit COSMO hydrogen-bond constants were already zero in
Z0w and its descendants, so merely turning that term off is not a new solution. The nitrogen-site
occupancy mismatch and temperature-fit failures also matter. The failed registrations stand; neither a
unique double-counting decomposition nor a successful replacement architecture was established.

A later, separate source regression must not be confused with these historical failures. Since P6,
Z0x's optimized interior dispatch bypassed the association subclasses' _g overrides; enabling P28 could
do so at pure endpoints as well. Archived Z0w/Z0w2/Z0w3 scores predate that change. P55's separate repair
restores full-subclass-g finite differences, including the historical one-sided endpoint approximation;
it does not supply an exact association endpoint or a new association score. Software regression tests
and any future physical validation are reported separately. No fourth association variant is accepted.

### 3.10 Dielectric ingredient and retrospective VLE oracle

R14/P51 screened 742 stored entries against a pinned public liquid-permittivity compilation using exact
identity and temperature rules. There were 248 valid matches at 298.15 K, with five additional matched
entries having invalid stored epsilon. The registered complete aggregate was therefore withheld.
Descriptive matched-only summaries are not substituted for that withheld aggregate or interpreted as
validation of the current Onsager approximation.

P52, after amendment P52a protecting the exact 630/1/5 profile selection, ran on 963 already-exposed
observations in 100 binary systems. All 2,889 requests were finite and the historical P6 baseline replay
matched. With identical UD profiles and frozen pure vapor pressures, row-weighted VLE AAD was 13.78%
for stored-epsilon Z0x, 13.07% for experimental-epsilon Z0x, and 10.44% for COSMO-SAC 2010. Equal-system
AAD was 13.90%, 13.19% and 10.65%, respectively. From unrounded outputs, the oracle removed about
0.72 percentage points, roughly 21% of the 3.35-point comparator gap; independently rounded table
entries need not subtract to the printed difference. There were 559 improved and 404 worsened rows.
Experimental epsilon was held at its 298.15 K value throughout, so this was not an epsilon(T) or HE test.

The oracle is an experimental-input, retrospective diagnostic, not a fit-free variant, a rigorous
headroom bound or a newly held-out score. The old main7 14.15/8.62 comparison uses a different subset.
R14 does not authorize a portfolio dielectric simulation campaign or identify a transferable local
contact coefficient. See `docs/astra/round14/RESULTS.md`. No R15 factorial result is asserted here.

## 4. Discussion

The historical benchmark shows that specified theory-derived interaction constants can retain useful
IDAC and demixing performance within a common COSMO-SAC framework. Z0x remains worse than COSMO-SAC 2010
for VLE on the displayed main7 and temporal subsets. This supports a quantitative account of the
tradeoff, without claiming that all empiricism has been removed or that the model is generally competitive.

The electrostatic contact prescription is a plausible research target, but bulk permittivity and local
segment response are different quantities. In the implemented mapping, increasing epsilon raises
f=(epsilon-1)/(epsilon+0.5) toward the conductor limit. The experimental-epsilon oracle yields only a
small improvement on its particular exposed sample. Earlier one-term ablations and that oracle do not
identify a unique universal correction, and their apparent gains cannot be added as independent causes.
A complete same-row factorial can quantify the contributions of the implemented ES, HB and dispersion
replacements under a stated allocation rule, including their interactions. Its fitted corners remain
diagnostics, never candidates selected by whichever ThermoML error is smallest.

Deriving a new contact kernel from reaction-field response or independent electronic calculations is
physically possible after the cavity, contact geometry and reference-energy partition are specified.
Electronic energy alone does not determine the angular and entropic contact free energy. A self-consistent
finite-dielectric profile model would also need consistent pure references and composition/temperature
derivatives; another dielectric scale on top of it is not automatically justified. No such new local
model is validated by the present evidence. A future design needs independent physical acceptance and
an exposure audit before any confirmatory comparison.

Association and direct simulation remain separate research programs. Reproducing a bonded fraction does
not validate the site thermodynamics, and an energy/force model does not automatically validate its
field response or chemical potentials. The numerical association repair changes neither the archived
scientific failures nor this assessment. The present work is ready for a limitations-aware account of
its completed evidence; a speculative native campaign need not delay that account.

## 5. Limitations

The retained effective area and combinatorial constants, sigma-processing conventions and empirical
history of some UD conformations limit the meaning of "fit-free". Z0/Z0x interaction constants were not
regressed to ThermoML. Z0s involves a train-selected discrete choice; Z1 is a fitted comparison. VLE
uses the same experimental pure-component vapor-pressure correlations in every arm. UD-backed main
results and exploratory open-profile results are different input versions.

The original compound and 2017-2019 temporal collections were repeatedly inspected during later
development. Neither is certified unexposed for another adaptive variant, and no new multi-system
holdout or data beyond HANNA's training has been certified. Historical confidence intervals keep their
original scope. Later explanatory ratios have no claimed generalization confidence interval.

The 630 original-gradient profiles and six S1/S2 profiles retain their actual provenance. A passed
historical agreement threshold is not proof of corrected-gradient stationarity, a liquid conformer
ensemble or equivalence to UD. P35's retrospective coordinate explanation and its tetraEG exception do
not identify a production geometry rule. LLE detection does not certify global stability or every
reported composition. Claims about new source versions require separate numerical checks.

## Data and code availability

The repository contains source code, registrations and public aggregate result records. UD-derived
geometries and detailed R10-R15 profile/prediction artifacts remain private on the Mac under the applicable
data-use terms. Some historical predictions and execution inputs are private or untracked; a public
checkout alone is not asserted to reproduce every historical table. Public result records retain plan
digests and scope, and their instructions identify required private assets without redistributing them.

## Figure captions

**Figure 1.** Predicted vs experimental ln gamma_inf for held-out molecules (test split, common subset of
762 points in 177 systems) for COSMO-SAC 2010, modified UNIFAC (Dortmund), Z0x and HANNA. HANNA was trained on
data that very likely include these systems.

**Figure 2.** Hydrogen-bond constants c_hb derived from 17 counterpoise-corrected B3LYP-D4/def2-TZVP dimers
(points; bars are class means) compared with the fitted COSMO-SAC 2010 values (blue bars).

**Figure 3.** Trade-off between infinite-dilution accuracy (IDAC MAE, x axis) and bubble-pressure accuracy
(VLE AAD, y axis) in the historical compound-test comparison. Larger electrostatic coefficients
(Z0, Z0e) favor some dilute properties; the smaller optical-screening prescription (Z0s) improves VLE
at the expense of other metrics. These are exposed comparisons, not evidence for one optimal coefficient.

**Figure 4.** Liquid-liquid split detection on held-out molecules: share of experimentally two-phase systems
where a gap is predicted vs share of experimentally homogeneous systems where a gap is wrongly predicted.

**Figure 5.** Z0x absolute error minus COSMO-SAC 2010 absolute error in ln gamma_inf by solute and solvent
family (all data, cells with at least 10 points). Blue: Z0x better; orange: COSMO-SAC better.

## Supplementary material (files in the repository)

S1 Pre-registration and every later change: `PREREGISTRATION.md`.
S2 Benchmark construction, rejection log and split hash: `data/benchmark/`, `data/processed/rejections.csv`.
S3 Dimer geometries and energies, CCSD(T) check, association thermochemistry: `results/qc/`.
S4 All scorecards with bootstrap intervals: `results/scorecard_*.md`.
S5 Error maps by chemical family: `results/error_map_idac_*.csv`.
S6 Open-profile validation and conformer comparison: `results/pyscf_profile_validation.csv`,
   `data/pyscf_sigma/conformer_summary.csv` (asset availability is stated above).
S7 Later numerical, glycol and dielectric evidence: `docs/astra/round2/RESULTS.md` through
   `docs/astra/round14/RESULTS.md`, with the registrations and private-plan digests referenced there.

## References (to verify against the publisher records before submission)

1. Klamt, A. Conductor-like screening model for real solvents. J. Phys. Chem. 1995, 99, 2224.
2. Lin, S.-T.; Sandler, S. I. A priori phase equilibrium prediction from a segment contribution solvation
   model. Ind. Eng. Chem. Res. 2002, 41, 899.
3. Mullins, E. et al. Sigma-profile database for using COSMO-based thermodynamic methods. Ind. Eng. Chem.
   Res. 2006, 45, 4389.
4. Hsieh, C.-M.; Sandler, S. I.; Lin, S.-T. Improvements of COSMO-SAC for vapor-liquid and liquid-liquid
   equilibrium predictions. Fluid Phase Equilib. 2010, 297, 90.
5. Hsieh, C.-M.; Lin, S.-T.; Vrabec, J. Considering the dispersive interactions in the COSMO-SAC model for
   more accurate predictions of fluid phase behavior. Fluid Phase Equilib. 2014, 367, 109.
6. Bell, I. H.; Mickoleit, E.; Hsieh, C.-M.; Lin, S.-T.; Vrabec, J.; Breitkopf, C.; Jäger, A. A benchmark
   open-source implementation of COSMO-SAC. J. Chem. Theory Comput. 2020, 16, 2635.
7. Gmehling, J.; Li, J.; Schiller, M. A modified UNIFAC model. 2. Present parameter matrix and results for
   different thermodynamic properties. Ind. Eng. Chem. Res. 1993, 32, 178.
8. Hoffmann, M. et al. (HANNA) Thermodynamically consistent machine learning model for excess Gibbs energy.
   Nat. Commun. 2026, doi:10.1038/s41467-026-71430-y.
9. Frenkel, M. et al. ThermoML, an XML-based approach for storage and exchange of experimental and critically
   evaluated thermophysical and thermochemical property data. J. Chem. Eng. Data 2006, 51, 1504 (series).
10. Herington, E. F. G. Tests for the consistency of experimental isobaric vapour-liquid equilibrium data.
    J. Inst. Petrol. 1951, 37, 457.
11. Onsager, L. Electric moments of molecules in liquids. J. Am. Chem. Soc. 1936, 58, 1486.
12. Wertheim, M. S. Fluids with highly directional attractive forces. J. Stat. Phys. 1984, 35, 19 (and 35, 35;
    1986, 42, 459; 42, 477).
13. Caldeweyher, E. et al. A generally applicable atomic-charge dependent London dispersion correction.
    J. Chem. Phys. 2019, 150, 154122.
14. Bannwarth, C.; Ehlert, S.; Grimme, S. GFN2-xTB. J. Chem. Theory Comput. 2019, 15, 1652.
15. Grimme, S. Supramolecular binding thermodynamics by dispersion-corrected density functional theory.
    Chem. Eur. J. 2012, 18, 9955.
16. Sun, Q. et al. Recent developments in the PySCF program package. J. Chem. Phys. 2020, 153, 024109.
17. Boys, S. F.; Bernardi, F. The calculation of small molecular interactions by the differences of separate
    total energies. Mol. Phys. 1970, 19, 553.
