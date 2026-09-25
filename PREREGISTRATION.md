# Pre-registration

Written 2026-09-24, before any Z0, Z1 or ablation prediction was computed.
Changes after that date are listed at the bottom with a reason.

## Data
ThermoML archive snapshot (MobleyLab mirror, files up to mid-2017; 9,184 XML files).
Compounds resolved to InChIKey offline (NIST UD list, then `chemicals`, formula must match).
Scope: neutral C/H/N/O/F/Cl/Br/S molecules, at most 25 heavy atoms, 250 to 450 K, P at most 500 kPa,
both components subcritical. Rejections logged with reasons in `data/processed/rejections.csv`.

Quality filters: IDAC repeats within 2 K must agree within 0.2 in ln gamma (outliers dropped).
VLE series with vapor compositions must pass the Herington area test (D < 10, or D - J < 10 isobaric;
absolute area imbalance < 0.03 accepted for near-ideal systems).

Split: 20% of compounds held out (seed 20260924, water always in train). A row is `test_one` when one
component is held out, `test_both` when both are. The split file is hashed in `data/benchmark/splits.sha256`.

## Models compared
`unifac_do` (modified UNIFAC Dortmund, thermo + ugropy groups), `cosmosac2010`, `cosmosac_dsp`
(NIST implementation constants, reproduced to 2e-9 in ln gamma), `Z0`, `Z1`, and ablations
`abl_es`, `abl_hb`, `abl_disp`, `Z0_nodisp`. All COSMO models use the same NIST UD sigma profiles.

## Z0 recipe (no experimental input)
See `src/zcosmo/zmodel.py` docstring. The choices below were fixed before results:
conductor limit f_pol = 1; dispersion part removed from dimer energies; one contacting segment pair per
H-bond; tail width = a_eff; London combining rule; weight 1 on the London term.

## Metrics (primary first)
IDAC: MAE in ln gamma_inf. VLE: AAD in bubble pressure (%) at measured T, x using the same pure-component
vapor pressures (thermo package correlations) for every model. HE: MAE (J/mol) and sign correctness for
|HE| > 20 J/mol. LLE: share of experimental two-phase systems where a gap is predicted, MAE of the nearest
binodal composition. Solvent screening: median Spearman rho of predicted vs experimental selectivity
ln(g_a/g_b) across solvents, solute pairs with at least 5 common solvents.
All comparisons on the common subset where every model predicts. 95% CIs by bootstrap over binary systems
(1,000 resamples). A difference counts only when the paired CI excludes zero.

## Tier thresholds (from the plan)
Useful: Z0 IDAC MAE within 1.5x of cosmosac2010 on test, plus coverage beyond UNIFAC.
Competitive: Z0 or Z1 beats cosmosac2010 and ties or beats unifac_do on test_both, selectivity rho >= 0.8.
Frontier: needs a HANNA comparison on post-training data (not possible with this snapshot).

## Known limitations fixed in advance
The 2017 snapshot makes a temporal split against HANNA impossible. The NIST UD profiles and the
dsp dispersion energies were produced by groups who fitted COSMO-SAC constants to experimental data;
the profiles themselves are DFT (DMol3 BP/DNP) and contain no fitted numbers, but the averaging radius
and sigma_hb split follow the fitted model's conventions.

## Changes after registration
- 2026-09-24, before any Z0/Z1 result: added an LLE filter (both coexisting branches or at least 5 cloud
  points), because isolated single compositions of fully miscible pairs (toluene + cyclohexane) were
  entering as "two-phase" data. The held-out set is now drawn from all in-scope compounds rather than
  from compounds present in the tables, so later cleaning cannot move it. Split re-frozen, sha256
  d414402911946b14165a168ce40b8c00694d52de245adb6451fb6f65d7a2ffb6. Baseline predictions were recomputed.
- 2026-09-24, before any Z0/Z1 result: sigma profiles are matched on the stereo-free InChIKey block when
  the exact key is missing and exactly one UD profile shares that block (racemates and stereo labels
  from the name resolver). Coverage rose from 86-92% to 92-94% of rows; the split hash is unchanged.
- 2026-09-24, before any Z0/Z1 result: the solvent-screening metric was redefined. The pairwise
  selectivity version was dominated by near-identical solute pairs (butene isomers) where the
  selectivity is inside the measurement noise. New definition: per solute, Spearman rho between
  predicted and experimental ln gamma_inf across solvents (T closest to 298 K, >= 5 solvents,
  experimental spread >= 1 ln unit); report the median over solutes.
- 2026-09-24, after the first Z0 results: sensitivity variants `sens_fpol`, `sens_hbdisp`, `sens_tail2`,
  `sens_univhb` were added. They are exploratory, chosen after seeing Z0 results, and are never used as
  the headline model.

## Z0e (registered 2026-09-24, after the Z0 results, before any Z0e prediction)
Motivation: ablation and sensitivity point at the conductor-limit electrostatics. Z0e keeps every Z0
constant and replaces f_pol = 1 by f_pol = (eps - 1)/(eps + 0.5), the COSMO dielectric scaling, with eps
computed without experimental data: Onsager's equation for each pure liquid at 298.15 K using the
GFN2-xTB dipole moment (RDKit MMFF conformer), the D4 static polarizability (Clausius-Mossotti for
n^2) and the COSMO cavity volume as the volume per molecule. For a binary, eps is the arithmetic mean of
the two pure-liquid values, so c_ES is constant across composition and Gibbs-Duhem holds.
Z0e is judged on the same scorecard; the headline stays Z0 unless Z0e is better on the test split.

## Session 2 registrations (2026-09-24, before the corresponding predictions)
- `hanna`: HANNA ensemble (marco-hoffmann/HANNA, Nat. Commun. 2026) run through the same scorecard as a
  data-driven reference. It was trained on ~824k Dortmund Data Bank points up to its release, so every
  benchmark row is potentially in its training set; it is reported as a reference, never as a held-out
  competitor. The ThermoML archive ends with 2019 publications, so no post-HANNA temporal test exists.
- Extended benchmark (if the NIST 2020 archive downloads): rows from files that are not in the 2017
  mirror form a `temporal` set (publications mid-2017 to 2019). The existing held-out compound list is
  kept; compounds new to the extended set are assigned to test when int(sha256(InChIKey), 16) % 5 == 0.
  The frozen v1 benchmark and its hash stay the primary result.
- Z0e-variant selection (registered before running): 6 theory variants of the dielectric factor,
  eps combination rule {arithmetic, geometric, harmonic mean of the pure-liquid values} x eps type
  {Onsager static eps, optical n^2 from Clausius-Mossotti}. The variant is chosen by the TRAIN split only
  (sum of the IDAC MAE rank and the VLE median-absolute-deviation rank on train, using a fixed random
  sample of 4,000 train VLE rows; the median is used because three-phase rows dominate the mean), then scored once on test as `Z0s`.
  Z0 stays the headline zero-constant model; Z0s involves one discrete choice made on training data.
- VLE data-quality fix (applies to every model equally): VLE rows whose liquid composition lies inside
  an experimentally measured liquid-liquid gap of the same binary (LLE table, within 5 K) are three-phase
  data and are excluded from the VLE score. Reported alongside the unfiltered number.
- Z0s selection result (train only): four variants tied on the summed rank (optical arithmetic,
  geometric, harmonic; static harmonic). Tie broken by the first criterion, train IDAC MAE:
  optical n^2 with the harmonic mean (0.902). Recorded before any Z0s test prediction.
- Z0x (registered after seeing that one electrostatic strength cannot serve both dilute (IDAC, LLE)
  and finite-concentration (VLE) data, before any Z0x prediction). Hypothesis: the dielectric factor
  should follow the local medium, i.e. the mixture composition. Z0x keeps every Z0 constant; the
  electrostatic coefficient is c_ES(x) = f(eps_mix(x)) * 0.3 a_eff^1.5 / (2 eps0), with eps_mix the
  COSMO-volume-fraction average of the Onsager pure-liquid permittivities (same values as Z0e).
  Thermodynamic consistency is enforced by defining g(x) = sum_i x_i ln gamma_i evaluated with c_ES(x)
  held fixed, and deriving ln gamma_i from g by numerical differentiation (Gibbs-Duhem exact).
  No constants are fitted and no choice is made on data.

## Session 3 registrations (2026-09-24, before any corresponding prediction)
- Z0w (association): Z0x with the COSMO hydrogen-bond term switched off (c_hb = 0) and a Wertheim
  TPT1 association contribution added. Site scheme fixed a priori from structure: every H on O or N is
  one donor site; each O carries 2 acceptor sites; each N carries 1. Site-pair association strength
  Delta_AB(T) = (kT/P0) * exp(-dG_AB(T)/RT) per molecule pair, the dimerization constant of that
  donor/acceptor contact in the ideal-gas standard state, with dG = dE (B3LYP-D4/def2-TZVP,
  counterpoise, incl. deformation) + dG_RRHO (GFN2-xTB harmonic thermochemistry, quasi-RRHO for low modes,
  dimer minus monomers). dH and dS are taken at 298.15 K and held constant with T. Donor/acceptor classes:
  donor {OH, NH}, acceptor {hydroxyl/water O, other O, N}; each class pair uses the mean dG over the
  computed dimers of that class pair; class pairs without a dimer use the mean over all dimers.
  Concentrations use the COSMO cavity volume as the volume per molecule. g_assoc(x) = sum_i x_i
  sum_A (ln X_A - X_A/2 + 1/2) minus the pure-component values; ln gamma from the total g(x) (Z0x part with
  c_hb = 0 plus association) by numerical differentiation. No fitted constants, no choices on data.
- Profiles for missing compounds (`pyscf_cosmo`): BP86/def2-TZVP C-PCM in the conductor limit on
  GFN2-xTB geometries, Klamt COSMO radii, averaged and split into NHB/OH/OT exactly as the NIST
  `to_sigma.py` does for UD. Accepted for use only if, on >= 20 molecules that also have UD profiles,
  the median |difference| in COSMO-SAC-dsp ln gamma_inf over all their benchmark IDAC rows is < 0.15.
  Rows involving gap compounds are scored as a separate "coverage" table so v1 numbers do not move.
- Conformers: for the 50 most flexible benchmark molecules (rotatable bonds), CREST (GFN2-xTB)
  ensembles within 3 kcal/mol, pyscf_cosmo profiles per conformer, Boltzmann-weighted (xTB free energies
  at 298 K). Effect measured as COSMO-SAC-dsp and Z0x predictions with the single lowest conformer vs the
  ensemble, both from pyscf_cosmo, on benchmark rows involving those molecules.
- Conformers, change before any conformer result: CREST is not available in the cloud workspace, so
  conformers come from RDKit ETKDG (50 embeddings, seed 7) + GFN2-xTB relaxation, deduplicated by
  heavy-atom RMSD < 0.5 A or |dE| < 0.1 kcal/mol, keeping at most 5 within 3 kcal/mol (xTB). Boltzmann
  weights use the BP86/def2-TZVP conductor-screened SCF energies at 298.15 K (the COSMO-RS convention),
  not xTB free energies. The ensemble profile is the weighted sum of conformer profiles; area and volume
  are weighted the same way.
- Z0w result recorded before any exploratory follow-up: see results/scorecard_*_z0w.md.
- pyscf_cosmo acceptance test result (2026-09-24): 25 molecules, 2,302 IDAC rows, median |d ln gamma_inf|
  = 0.153 vs the 0.15 bar, so the open profiles are REJECTED as a drop-in for UD in the main scorecard.
  Largest differences: water 1.14 (450 rows), triethylene glycol 0.84. Experimental MAE on the same rows
  0.744 (UD) vs 0.787 (pyscf). Gap-compound rows are therefore reported only as an exploratory table.
- Conformers, change before any conformer result: 244 conformers of up to 25 heavy atoms are too costly
  at def2-TZVP, so conformer profiles use BP86/def2-SVP (same C-PCM, radii and averaging). The lowest-vs-
  ensemble comparison is internal to this one method, so the basis does not bias it.
- Results recorded 2026-09-25: Z0w fails as registered (aqueous over-association); conformer ensembles
  change predictions negligibly; open profiles rejected by the acceptance test (see PROGRESS.md).

## Session 5 registrations (2026-09-25, before any Z0w2 prediction)
- MLIP teacher tier (MACE-OFF23 alchemical FEP) is shelved on throughput, before any prediction: best
  measured speed was 0.73 ns/day for 648 atoms on a free Kaggle GPU (0.12 on the M4 Pro CPU; MPS fails in
  float64). A 20-window decoupling at ~2 ns/window needs ~55 GPU-days per solute vs 30 GPU-h/week free.
  MACE-OFF23 is also ASL (non-commercial) licensed. Revisit if a faster fit-free MLIP appears.
- Z0w2 (condensed-phase association). Honesty note: this change is motivated by the Z0w test-set failure
  (aqueous over-association), so Z0w2 test numbers are a second look at the same test set, not a clean
  held-out test; the temporal set (2017-2019) is its cleanest check. Definition: identical to Z0w except
  the site-pair free energy includes the electrostatic continuum desolvation of the contact,
  dG_AB,liq(T, eps) = dH_AB - T dS_AB + ddG_solv,AB(eps), with
  ddG_solv = [G_solv(AB) - G_solv(A) - G_solv(B)] from BP86/def2-TZVP C-PCM (Klamt radii, same as the
  profiles), monomers frozen at their dimer geometry, on the grid eps = {2, 4, 8, 16, 32, 64, conductor};
  interpolated linearly in f = (eps-1)/eps with ddG = 0 at f = 0; class-mean per donor/acceptor class
  pair exactly as dH and dS. eps is the COSMO-volume-fraction mixture of the fit-free Onsager pure-liquid
  permittivities (the Z0x values), evaluated at each composition; pure-component reference terms use each
  pure liquid's own eps. ddG_solv is held constant with T. No fitted constants.
  Success criteria (fixed now): on the test split, Z0w2 IDAC MAE < Z0x (0.800) with the paired bootstrap CI
  excluding 0, AND aqueous-system IDAC MAE not worse than Z0x; LLE balanced accuracy >= 0.88; temporal-set
  IDAC MAE reported alongside. Otherwise Z0w2 is recorded as failed.
- Open profiles v2 (registered 2026-09-25, before any v2 profile is computed): as v1 (`pyscf_cosmo`) but
  the geometry is optimised at BP86/def2-SVP inside the conductor (C-PCM, eps -> inf, Klamt radii,
  pyberny optimiser, from the GFN2-xTB start), which is the COSMO convention the DMol3/UD set follows.
  Same BP86/def2-TZVP C-PCM single point, Hsieh averaging and NHB/OH/OT split. Computed for all 636
  benchmark compounds on GitHub Actions runners (identical code, pinned pyscf 2.14.0). Acceptance test is
  the v1 test unchanged: >= 20 molecules with UD profiles, median |d ln gamma_inf| (COSMO-SAC-dsp) over
  their benchmark IDAC rows < 0.15. If accepted, an all-open-profile version of Z0x (Z0x-open) is scored
  as a secondary table; if not, v2 profiles are used only for gap compounds, as v1.
- Z0w2 check on water (before scoring): electrostatic desolvation of the water dimer rises smoothly from
  +0.88 (eps 2) to +2.06 kcal/mol (conductor), i.e. ~30x weaker association in liquid water.
