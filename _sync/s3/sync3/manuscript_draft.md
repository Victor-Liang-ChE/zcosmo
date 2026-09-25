# How far can COSMO-SAC go without fitted constants? A pre-registered benchmark on NIST ThermoML data

Victor Liang (draft, 2026-09-24)

## Abstract

Predictive activity-coefficient models such as COSMO-SAC avoid binary interaction parameters, yet every
variant in use still fits 8 to 15 universal constants to experimental phase-equilibrium data. We ask how
much accuracy is lost when each of those constants is replaced by a number computed from theory or
quantum chemistry. In the resulting model, Z0, the electrostatic misfit coefficient follows from Klamt's
estimate in the conductor limit, the three hydrogen-bond constants come from 17 counterpoise-corrected
B3LYP-D4/def2-TZVP dimer energies, and dispersion enters through a London term built from D4 molecular
C6 coefficients and polarizabilities. No experimental thermodynamic data are used anywhere in Z0.

We score Z0, two dielectric-screening refinements (Z0e, Z0x), COSMO-SAC 2010, COSMO-SAC-dsp and
modified UNIFAC (Dortmund) on a benchmark built from 9,184 ThermoML files (3,438 infinite-dilution
activity coefficients, 46,127 VLE, 7,158 LLE and 27,366 excess-enthalpy points), with a molecule-level
held-out split frozen before any model was run, and on a temporal set of 2017 to 2019 publications that
postdate the fits of all reference models. HANNA, a neural model trained on 824k Dortmund Data Bank
points, is included as a data-driven reference.

On held-out molecules Z0 matches COSMO-SAC 2010 for infinite-dilution activity coefficients (MAE in
ln gamma 0.76 vs 0.82, difference not significant) and detects liquid-liquid demixing more reliably than
both COSMO-SAC and UNIFAC (balanced accuracy 0.90 vs 0.84 and 0.81, significant). It is clearly worse for
bubble pressures (AAD 18.8% vs 8.6%) and on the temporal set. The DFT-derived hydrogen-bond constants are
nearly identical across the three COSMO-SAC classes (about 5,700 kcal A^4 mol^-1 e^-2), whereas the fitted
constants span 4,014 to 932. Ablations trace most of the remaining error to one term, the electrostatic
misfit in the conductor limit: no single screening strength serves dilute and concentrated mixtures at
once. Composition-dependent screening derived from first-principles permittivities (Z0x) recovers part of
the gap (VLE AAD 14.2%) without any fitted number, keeping the IDAC and LLE results. HANNA, where its
training data reach, is far more accurate than every physics-based model, but it does not detect demixing
more reliably than Z0 on held-out molecules.

## 1. Introduction

(To write: role of NRTL/UNIQUAC vs predictive models; UNIFAC and COSMO-RS/SAC; recent refits (TZVPD-FINE,
openCOSMO-RS-Phi); data-driven models (HANNA, GNNs); the open question of how much of COSMO-SAC's
accuracy is carried by its fitted constants rather than by the sigma-profile physics.)

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
(2016). HANNA's training data very likely include them.

### 2.2 Reference models
COSMO-SAC 2010 and -dsp were reimplemented in NumPy and reproduce the NIST benchmark code (Bell et al.,
JCTC 2020) to 2e-9 in ln gamma on 400 random pairs. All COSMO models use the same NIST UD sigma
profiles (DMol3 BP/DNP, 2,259 compounds). Modified UNIFAC (Dortmund) uses the `thermo` package with
automatic group assignment (`ugropy`). HANNA is the published ensemble (Nat. Commun. 2026).

### 2.3 The Z0 model
(Equations to typeset.) Effective segment area a_eff = pi r_av^2 = 7.25 A^2, a geometric identity with the
profile-averaging radius. Electrostatic misfit c_ES = alpha'/2 with alpha' = 0.3 a_eff^1.5 / eps0 in the
conductor limit (12,226 kcal A^4 mol^-1 e^-2; the fitted 2010 value at 298 K is 8,197). Hydrogen bonding:
for each dimer, E_HB = c_ES (s_D + s_A)^2 - c_hb (s_D - s_A)^2 with s_D, s_A the mean charge density of the
most extreme a_eff of the donor and acceptor profiles; E_HB is the counterpoise-corrected B3LYP/def2-TZVP
binding energy including monomer deformation, with the D4 dispersion part removed. Dispersion: London
contact energies e_ij = -C6_ij / d_ij^6 from D4 molecular C6 and polarizabilities (London combining rule),
d_i the diameter of a sphere of COSMO cavity volume, entering as ln gamma_1 = (z/2) w x_2^2 / RT with
w = 2 e_12 - e_11 - e_22.

Refinements registered after the first results, before their own predictions:
Z0e scales c_ES by the COSMO dielectric factor f = (eps - 1)/(eps + 1/2) with eps from Onsager's equation
(GFN2-xTB dipoles, D4 polarizabilities, COSMO volumes), arithmetic mean over the pair. Z0x lets eps follow
the mixture composition (volume-fraction average) and derives ln gamma_i from the resulting g^E by
numerical differentiation, so Gibbs-Duhem holds exactly. Z0s picks one of six dielectric variants on the
training split only (it chose the optical permittivity n^2 with a harmonic mean).

### 2.4 Protocol
Metrics: MAE in ln gamma_inf; AAD in bubble pressure at measured T and x with the same pure-component
vapor pressures for every model; MAE of H^E and its sign; for LLE, the share of two-phase systems where a
gap is predicted (recall) and the false-positive rate on 336 systems observed homogeneous over the full
composition range (from VLE series), combined into a balanced accuracy. All comparisons use rows every
model can predict. 95% intervals come from 1,000 bootstrap resamples over binary systems; a difference
counts when the paired interval excludes zero. Pre-registration and every later change are in
`PREREGISTRATION.md`.

## 3. Results

### 3.1 Held-out molecules (test split)

| Model | IDAC MAE | IDAC, both unseen | VLE AAD P % (median) | H^E MAE J/mol | LLE balanced accuracy |
|---|---|---|---|---|---|
| Mod. UNIFAC (Dortmund) | 0.45 | 0.44 | 11.3 (3.1) | 314 | 0.81 |
| COSMO-SAC 2010 | 0.82 | 0.90 | 8.6 (3.6) | 399 | 0.84 |
| COSMO-SAC-dsp | 0.67 | 0.66 | 9.2 (3.6) | 399 | 0.83 |
| Z0 | 0.76 | 0.53 | 18.8 (6.2) | 532 | 0.90 |
| Z0e | 0.79 | 0.57 | 15.7 (4.6) | 521 | 0.90 |
| Z0s (one choice on train) | 0.95 | 1.00 | 12.8 (4.2) | 571 | 0.70 |
| Z0x (no fitted constants, no choices) | 0.76 | 0.55 | 14.2 (4.5) | 522 | 0.90 |
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

254 IDAC points (54 systems), 7,722 VLE points, 2,058 H^E points. On data that postdate every reference
fit, the zero-constant models are significantly worse than COSMO-SAC on VLE (Z0x minus COSMO-SAC 2010:
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
dispersion costs +0.17 in IDAC and slightly helps VLE. Stronger screening (Z0, Z0e) favors dilute
properties and LLE detection; weaker screening (Z0s) favors VLE but loses both. By chemical family, Z0 is
the most accurate model for nonpolar solutes in aromatic solvents (alkenes in aromatics: 0.18 vs 0.40 for
COSMO-SAC and 1.05 for UNIFAC) and for alkanes in alcohols (0.66 vs 1.04), and fails for self-associating
solutes in inert solvents (alcohols in alkanes 3.7, in aromatics 3.4).

## 4. Discussion
(To write.) Main messages: (i) the sigma-profile physics alone, with constants from theory, reaches
COSMO-SAC 2010 accuracy for dilute properties on unseen molecules and beats it for LLE detection; (ii) the
fitted hydrogen-bond constants, especially OT-OT, do not correspond to hydrogen-bond energetics and
absorb other deficiencies; (iii) the decisive missing physics is dielectric screening of the misfit
energy, which must depend on the local medium; (iv) data-driven models such as HANNA are far more accurate
wherever their training data reach, so the case for physics-based models rests on transferability and
interpretability, which a fully out-of-distribution test would have to confirm.

## 5. Limitations
ThermoML ends with 2019 publications, so no test postdates HANNA's training data. Profiles come from one
DFT source (DMol3), whose averaging conventions follow the fitted model. 137 benchmark compounds lack a
profile. Pure-component vapor pressures are experimental correlations. Conformers are single structures.

## Data and code availability
All code, the frozen benchmark, split hashes, predictions and scorecards are in the project repository
(`src/zcosmo`, `data/benchmark`, `results/`).
