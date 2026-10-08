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
- Z0w2 result (2026-09-25, recorded before any follow-up): FAILED. Test IDAC MAE 0.902 vs Z0x 0.800
  (paired dMAE CI +0.041 to +0.177); LLE balanced accuracy 0.887. See PROGRESS.md session 5.
- MLIP association referee (diagnostic only, registered before running): MACE-OFF23 small, float32,
  NPT Berendsen 40 ps then Langevin NVT 30 ps at 298.15 K, 1 bar, 0.5 fs, 64 water / 27 methanol;
  report density and the fraction of hydroxyl H donors hydrogen bonded (O..O < 3.5 A, H-Od..Oa < 30 deg).
  Used only to compare against the bonded fractions implied by Z0w and Z0w2; any model built from it
  (e.g. association strengths obtained by inverting TPT1 on simulated bonded fractions) must be registered
  separately and judged first on the temporal set, since the test set has had two association looks.
- MLIP engine speed-ups (2026-09-25, accuracy gates fixed before each run; results):
  cuEquivariance fused kernels: max|dF| vs e3nn float32 2-4e-6 eV/A (gate 1e-3) -> ACCEPTED.
  TF32 matmuls: max|dF| 2.5-3.1e-3 eV/A -> REJECTED (gate 1e-3).
  Timestep/HMR NVE gate (|drift| < 0.01 kT/atom/ns): FAILED for every setting, including the 0.5 fs
  no-HMR reference (0.044; float32 model). Relative to it: HMR 1.0 fs 2.3x, 1.5 fs 6.2x, 2.0 fs 7.7x,
  2.5 fs blow-up (183x). Production stays at 0.5 fs, no HMR. A larger step may only be adopted through a
  newly registered test (drift <= 2x reference AND density, O-O RDF and H-bond fraction equal to the 0.5 fs
  run within 2 standard errors in thermostatted runs).
  Verlet-skin lean engine (zc_md.VerletMACE): exact by construction (MACE cutoff envelope is 0 beyond r_max);
  gate max|dF| vs the ASE path < 1e-4 eV/A along a Langevin trajectory.

## Session 5b registration: Z0w3 (2026-09-25 3:40 PM PDT, before any Z0w3 simulation result is seen)
- Idea: keep Z0w's Wertheim TPT1 form, but take each donor/acceptor class-pair strength Delta_da from
  first-principles liquid simulations instead of gas-phase dimers. Teacher: MACE-OFF23 small (trained on
  DFT only; no experimental data), float32 with cuEquivariance kernels (verified identical to e3nn to
  4e-6 eV/A), exact Verlet-skin engine, BAOAB Langevin 0.5 fs (gamma 0.01/fs), molecular Monte-Carlo
  barostat at 1.01325 bar (every 25 steps), 30 ps equilibration + 60 ps production, one run per liquid
  and temperature, start box from RDKit vdW volumes at packing 0.45 (no experimental density used).
- Liquids (fixed now): water (64), methanol (40), ethanol (30), n-propylamine (24), water/acetone
  (48/16), water/pyridine (48/12), n-propylamine/water (16/32); temperatures 278.15, 298.15, 323.15 K.
- H-bond criterion (fixed): donor H on O or N; acceptor O or N on another molecule; D..A < 3.5 A and
  angle H-D..A < 30 deg; each donor H assigned to at most one acceptor (nearest qualifying). Acceptor sites:
  O = 2, N = 1 (as Z0w).
- Inversion (TPT1 mass action, per liquid and T): Delta_da = f(d->a) / (c_a * n_a * X_a * X_d), where
  f(d->a) = mean bonds from class-d donors to class-a acceptors per d donor site, X_d = 1 - sum_a f(d->a),
  X_a = 1 - acceptor-site occupancy of class a, c_a = number density of class-a molecules computed with the
  model's own convention (mole fraction / COSMO-volume mixture volume), n_a = sites per molecule.
- Aggregation: per class pair and T, geometric mean over liquids providing that pair (weighted by bond
  counts); ln Delta vs 1/T fitted linearly over the three temperatures; class pairs never observed use the
  mean ln Delta of observed pairs (as Z0w). Everything else identical to Z0w.
- Go/no-go before inversion (fixed): the pure-water run at 298.15 K must give a bonded donor fraction in
  [0.70, 0.95] and a density within 15% of 1.0 g/cm3 (a sanity check of the teacher, not a fit); otherwise
  Z0w3 is abandoned. Kaggle ASE-engine run of water/methanol is an independent cross-check of the engine.
- Evaluation: primary = temporal set (2017-2019 publications) IDAC MAE vs Z0x and COSMO-SAC 2010, paired
  bootstrap; secondary = test split (already looked at twice for association, reported as such); LLE
  balanced accuracy >= 0.88. Success: temporal IDAC MAE < Z0x with CI excluding 0 and aqueous subset not worse.
- Z0w3 protocol deviation (2026-09-25 5:20 PM PDT, before any Z0w3 result was read): the propylamine/water start
  box had overlapping molecules (random lattice placement), the run blew up to NaN within 30 steps on every
  platform. Only that liquid is rerun with a clash-free builder (random insertion, >= 2.0 A between molecules,
  start packing 0.20 instead of 0.45) plus a steepest-descent pre-relaxation and a NaN guard (md_liquid_v3.py).
  Start conditions affect only equilibration, not the equilibrium averages used; the other six liquids keep
  the original builder. All other registered settings unchanged.
- Distillation (registered 2026-09-25 5:45 PM PDT, before any student is trained): a smaller MACE student
  (fewer channels, same cutoff 4.5 A) is trained only on MACE-OFF23 teacher energies and forces for frames of the
  target liquids (saved every 1 ps from teacher runs via md_liquid_v4 --frames; 90/10 frame split by run).
  Acceptance gates, all required: (1) held-out force MAE vs teacher < 20 meV/A; (2) in a 60 ps NPT run of
  water and methanol, density, O-O RDF first-peak height and bonded-donor fraction within 2 standard errors of
  the teacher runs; (3) speed-up >= 3x at equal batch. Any number reported from student sampling is reweighted
  to the teacher (Zwanzig / MBAR end-point reweighting on saved frames) and is used only if the effective
  sample size is >= 10% of frames; otherwise the teacher is rerun. The student never replaces the teacher's
  numbers directly.
- Open profiles v2 acceptance result (2026-09-25 5:30 PM PDT): 555 of 636 profiles finished before the
  GitHub Actions 350-min cap (81 largest re-dispatched). Registered test on the same 25 molecules / 2,302
  IDAC rows: median |d ln gamma_inf| = 0.1493 vs the 0.15 bar -> ACCEPT, by a margin of 0.0007 (v1: 0.153,
  reject). Mean 0.323; water still differs most (0.82 over 450 rows), triethylene glycol 0.93. Experimental
  MAE on those rows: UD 0.744, v2 0.769. Per the registration, Z0x-open (all profiles v2) is scored as a
  secondary table once all 636 exist; given the thin margin it is reported as exploratory, not a replacement.
- MLIP teacher cross-check (Kaggle, independent ASE engine + Berendsen barostat, 64 water / 27 methanol,
  298 K): water density 1.100 +- 0.017 g/cm3, bonded donor fraction 0.863; methanol 0.827 +- 0.057,
  0.909. MACE-OFF23 small overestimates water density by ~10% (inside the registered +-15% window).
- Z0w3 go/no-go (registered check, 2026-09-25 7:07 PM PDT): pure water 298.15 K bonded donor fraction 0.871,
  density 1.115 g/cm3 -> PASS; proceed to scoring once all 21 runs exist. Observed limitation recorded
  without changing the rule: pyridine N and propylamine N sometimes accept more than one H-bond in the
  simulation (occupancy > 1 per the model's single N site), so the inversion drops those points (e.g.
  water/pyridine 323 K OH->N); OH->N then rests on fewer points.
- Operations: Lightning studio auto-stopped at ~7:10 PM before the 278 K runs wrote results; restarted and
  resumed from checkpoints (no settings changed). Modal apps holding the NaN-stuck original
  propylamine/water processes were stopped after their healthy runs finished.
- Z0w3 RESULT (2026-09-25 11:05 PM PDT, recorded before any follow-up): FAILED the registered criterion.
  Temporal set (primary): IDAC MAE 2.192 [1.292, 3.143] vs Z0x 1.451 and COSMO-SAC 2010 0.925; bias +2.12;
  VLE AAD 37.6% (Z0x 11.3%); hE MAE 1021 J/mol (Z0x 349). Test split: IDAC MAE 1.072 vs 0.800 (paired CI
  +0.06 to +0.54); aqueous subset 4.79 vs 1.76 for Z0x. Median error and fraction within 0.3 improved slightly
  (test 0.48 / 0.40 vs 0.51 / 0.29), i.e. many non-aqueous systems got better while aqueous systems became far
  too non-ideal. The simulation-derived strengths are large (water ln Delta 6.5 at 298 K, ~700 A^3, ten times
  the gas-phase value) and, combined with the Z0x residual term that already carries part of the
  hydrogen-bond electrostatics, over-associate. OH->N temperature fit is unphysical (a = 23.6, b = -4374 K)
  because nitrogen accepts >1 H-bond in the simulations but one site in the model. Three association
  variants have now failed; no further TPT1 variant is scored on these data sets.
- Z0w3 LLE (test): recall 0.87, false-positive rate 0.164 (all 336 negatives: 0.223), balanced accuracy
  0.854 < 0.88 bar -> also fails the LLE criterion.
- Direct route (planned, NOT yet registered for scoring; 2026-09-26 12:30 AM PDT): ln gamma_inf(i in j) =
  beta [mu_ex(i in j) - mu_ex(i in pure i)] + ln(rho_j / rho_i,pure) (molar densities from the same NPT runs),
  mu_ex by alchemical decoupling with the MACE-OFF teacher. Open problems to settle in a feasibility phase
  before any registration: (1) MLIPs have no soft-core, so decoupling uses end-state interpolation
  U(l) = l U(full) + (1-l)[U(solvent) + U(solute)], which may diverge near l = 0; (2) cost: ~16 windows x
  0.1-0.2 ns x 3 force calls per step for ~250 atoms is roughly 0.5-1 GPU-day per ln gamma_inf on an L4.
  Feasibility gate (to be registered with numbers after one timing run): methanol hydration free energy with
  window overlap >= 0.03 between neighbours and statistical error <= 0.3 kcal/mol, before any comparison to
  experiment. Depends on the 4070 (WSL + cuEq) and on distillation for affordable throughput.
- Speed-up suite (registered 2026-09-26 ~8:00 AM PDT, before the run; bench11 on a Modal L4):
  A) GPU minimum-image neighbour list, half-edge symmetry (spherical harmonics x (-1)^l, radial MLP shared),
     static padding with dummy edges beyond r_max, CUDA graphs via torch.compile: each accepted only if
     max|dF| vs the ASE reference < 1e-4 eV/A (they are exact by construction; CPU pre-test gave 2-3e-6).
  C) Surrogate-driven HMC (student MACE distilled on the fly from teacher frames; leapfrog with student forces,
     Metropolis accept with teacher interaction energy + kinetic energy): samples the teacher distribution
     exactly by construction; usefulness gate = acceptance >= 0.3 at >= 10 student steps per teacher call, and
     O-O RDF peak position equal to plain teacher MD within one 0.025 A bin (sanity, short runs).
  D) End-state-interpolation TI probe for decoupling one water from 63 waters (11 windows x 1 ps): feasibility
     only (no blow-up near lambda = 0; <dU/dl> profile used to set thermodynamic-length-optimal windows).
     No free energy from D is used for any model or comparison.
- Speed-up suite RESULTS (bench11, Modal L4, finished 2026-09-26 9:31 AM PDT; recorded before any follow-up):
  A) GPU minimum-image neighbour list: exact (max|dF| 2.3e-6 / 3.9e-6 eV/A at 648 / 5,184 atoms) -> ACCEPTED.
     Per-step cost 73.9 -> 68.1 ms (648 atoms), 71.6 -> 72.7 ms (5,184); list rebuild 14 -> 0.9 ms and
     108 -> 20 ms. Half-edge symmetry: exact (3.3e-6 / 4.0e-6) -> ACCEPTED as an option; slower at 648 atoms
     (76.0 ms) and 12% faster at 5,184 (64.1 ms). Padding + CUDA graphs via torch.compile: FAILED to run
     (empty exception text); not used. Key observation: 648 and 5,184 atoms cost the same per step, i.e. the
     engine is launch/overhead bound at these sizes, so the lever is putting more independent work in one call.
  C) Surrogate HMC with a distilled student: student (16 ch, L=0, 2 layers) force MAE 28.9 meV/A vs teacher,
     but only 1.5x cheaper per call (24.1 vs 36.7 ms at 192 atoms; overhead bound). Acceptance 0.61 (n=10,
     0.5 fs), 0.34 (n=20, 0.5 fs), 0.15 (n=20, 1 fs). O-O peak 2.862 / 2.888 / 2.787 A vs teacher MD 2.787 A.
     Gate (acceptance >= 0.3 with >= 10 student steps AND peak within one 0.025 A bin) is met by no setting
     -> FAILED. (HMC is exact by construction; the peak miss is from 150 correlated trajectories started from
     one frame, but the gate is recorded as failed and distillation is shelved: at ~1.1x net speed-up it
     would not pay even if it passed.)
  D) End-state interpolation TI (water out of 63 waters, 11 x 1.5 ps): lambda = 0 gives <dU/dl> ~ 1.4e10 eV
     (solvent atoms sit on the non-interacting solute, where the full-system MACE energy is meaningless);
     lambda = 0.02 still 1.22 +- 0.78 eV -> the "no blow-up near lambda = 0" gate FAILED. Linear end-state
     interpolation is not used. (Script then crashed on np.trapz, removed in NumPy 2.4; no estimate is used.)
- Profiles v2 operational change (2026-09-26 8:45 AM PDT): pyberny progress is checkpointed every cycle and a
  killed optimisation resumes from its last geometry (same functional, basis, solvent, radii, convergence
  criteria; only Berny's Hessian guess restarts). Water test: resumed vs uninterrupted geometry agree to
  5e-7 A. Profiles computed this way carry "[resumed from checkpoint]" in their metadata.
- bench12 (registered 2026-09-26 ~10:15 AM PDT, before running; Modal L4):
  A2) Exact multi-system batching (MultiMACE): G independent periodic systems as one disjoint graph.
      Gate: max|dF| of a replica vs its single ASE evaluation < 1e-4 eV/A (CPU float64 pre-test: 5e-15).
      Throughput reported for 1-32 replicas of 192 atoms and 1-8 of 648.
  D2) Two-stage cavity path for decoupling (replaces linear end-state interpolation):
      stage 1 (solute already decoupled): U1(mu) = U(solvent) + U(solute) + soft-core WCA(mu) between solute
      and solvent atoms (Beutler alpha 0.5, eps 1 kcal/mol, sigma 2.4 A heavy-heavy, 1.4 A pairs with H);
      stage 2: U2(l) = l U(full) + (1 - l) [U(solvent) + U(solute) + WCA]. Both ends are the exact physical
      states, so the path constants cannot change dG, only its variance; they were chosen from atom sizes
      and H-bond distances, not from any free-energy result. All 22 windows (12 stage-2, 10 stage-1) run in
      one batched MACE call per step; 1 ps pre-equilibration, then 1 ps + 8 ps per window at 0.5 fs, BAOAB
      Langevin (gamma 10/ps), samples every 10 fs. Estimators: TI (trapezoid, 5-block standard errors) and
      MBAR. Feasibility gate for the path (on this water-in-water system): no non-finite forces; min
      neighbour MBAR overlap >= 0.03 in both stages; TI standard error <= 0.3 kcal/mol; TI and MBAR agree
      within 2 standard errors. The resulting number (MACE-OFF23-small water in its own liquid) is reported
      for orientation only; it is not compared with experiment for any model decision. If the path passes,
      the registered methanol-hydration feasibility run follows with the same settings.
- bench12 RESULT (2026-09-26 10:25 AM PDT, recorded before any follow-up):
  A2) Batching is exact (max|dF| 2.1-3.4e-6 eV/A for every replica count). Throughput on the L4 relative
      to one 192-atom box at 36.7 ms/call (bench11): 16 boxes in one call 44.4 ms -> 2.8 ms per box (~13x);
      648-atom boxes 36.3 -> 9.3 ms per box at 8 per call (3.9x). ACCEPTED; MultiMACE is the production engine
      for independent replicas and lambda windows.
  D2) Cavity path, water decoupled from 63 waters, 22 windows batched (96.3 ms/step for all, ~25x vs running
      the windows serially with 3 calls each), 9 ps/window: no non-finite forces; min neighbour MBAR overlap
      0.140 (stage 1) and 0.145 (stage 2), >= 0.03; TI -7.434 vs MBAR -7.489 kcal/mol (agree within 1 SE);
      TI standard error 0.336 kcal/mol > 0.3 bar -> gate FAILED on precision only (stage 2 alone 0.281).
      The divergence of bench11 D is gone (<dU/dl> at l = 0 is +0.085 +- 0.015 eV). Orientation only, not
      used for any decision: MACE-OFF23-small gives -7.4 kcal/mol for water in its own liquid (experiment
      about -6.3), in line with its ~10% density overestimate.
- Methanol hydration feasibility (registered 2026-09-26 10:40 AM PDT, before running; bench13, Modal L4):
  identical path, windows, WCA constants, integrator and estimators as bench12 D2; system: methanol replacing
  one water (the nearest other water removed; 62 waters, same box, MACE FIRE relaxation to fmax 0.3 eV/A);
  production raised from 8 to 20 ps per window because the only bench12 failure was statistical precision
  (SE scales as 1/sqrt(time); no free-energy value informed this). Gate as registered earlier: min neighbour
  overlap >= 0.03, TI standard error <= 0.3 kcal/mol, plus finite forces and TI-MBAR agreement within 2 SE.
  The number is compared with experiment only after the gate is judged, and no model is changed from it.
- Methanol hydration feasibility RESULT (bench13, finished 2026-09-26 11:49 AM PDT; recorded before follow-up):
  finite forces throughout; min neighbour MBAR overlap 0.146 (stage 1) / 0.156 (stage 2) >= 0.03; TI -6.254 vs
  MBAR -6.409 kcal/mol (within 1 SE); TI standard error 0.361 kcal/mol > 0.3 -> gate FAILED again on
  precision. Diagnosis (post hoc, from the saved samples): 2.3x longer sampling did not shrink the 5-block SE
  because the variance sits in two places: the steep soft-core region of stage 1 (mu 0.05-0.1, 36% of the
  variance) and stage 2 at l = 0.7-0.8, where dU/dl decorrelates in 1.8-2.6 ps (38%). Autocorrelation-based
  TI SE 0.327; MBAR block bootstrap -6.37 +- 0.27 (MBAR is not the registered estimator; reported only).
  Orientation (not used for decisions): -6.3 to -6.4 vs experiment about -5.1 kcal/mol; water in water was
  -7.4 vs -6.3, i.e. MACE-OFF23-small over-binds both by ~1.1-1.3 kcal/mol, which would largely cancel in
  ln gamma_inf = beta[mu_ex(i in j) - mu_ex(i in i)] + ln(rho_j/rho_i) if it is solute-specific.
- Methanol hydration, retry 3 (registered 2026-09-26 12:10 PM PDT, before running; bench14): same system, path
  constants, integrator and gate (TI 5-block SE <= 0.3 kcal/mol, overlap >= 0.03, TI-MBAR within 2 SE). Only
  window placement and length change, targeted at the measured variance: stage 1 mu = 0, .025, .05, .075, .1,
  .15, .2, .35, .5, .65, .8, .9, 1; stage 2 l = 0, .05, .1, .2, .3, .4, .5, .6, .65, .7, .75, .8, .85, .9, 1;
  30 ps production per window (28 windows batched). If this fails, the direct route is recorded as not
  feasible at this precision on free compute and the pilot is not registered.
- Methanol hydration retry 3 RESULT (bench14, finished 2026-09-26 2:12 PM PDT, recorded before follow-up):
  finite forces; min neighbour overlap 0.114 / 0.117 >= 0.03; TI -7.033 +- 0.229 (5-block SE <= 0.3),
  MBAR -7.157 kcal/mol (within 1 SE) -> feasibility gate PASSED. Autocorrelation SE 0.208, MBAR block
  bootstrap -7.10 +- 0.22. Caveat recorded now: bench13 (same system and start protocol, coarser windows)
  gave -6.25 +- 0.36; the two differ by 0.78 kcal/mol (1.8 combined SE, mostly stage 1: 3.95 vs 3.31),
  so single-run SEs likely understate the real uncertainty (slow modes longer than the block length).
  Hence the pilot below uses independent replicas. Orientation: experiment about -5.1 kcal/mol.
- Direct-route ln gamma_inf PILOT (registered 2026-09-26 2:40 PM PDT, before any pilot run):
  quantity: ln gamma_inf(i in j) = beta [mu_ex(i in j) - mu_ex(i in i)] + ln(rho_j / rho_i), rho = molar
  densities of the pure liquids from the MACE-OFF23-small NPT runs at 298.15 K (water 1.115 g/cm3, methanol
  0.874; cloud/liquids_results). Systems: methanol/water, both directions, 298.15 K. Four mu_ex runs
  (methanol in water, methanol in methanol, water in water, water in methanol), each: 64 lattice sites at the
  model's pure-solvent density (solute on one site, random orientations, MACE FIRE relaxation), bench14 path,
  windows, WCA constants, integrator and 30 ps/window (skin 0.9 A so the 11.98 A water box fits the GPU list).
  Replicas: seed 1 on Modal L4 now; seed 2 on another free GPU afterwards; mu_ex = replica mean, uncertainty =
  max(propagated TI SE, replica half-range). Fixed-volume boxes at the pure-solvent density are an
  approximation at infinite dilution (recorded, not corrected). Comparison: ThermoML IDAC for methanol in
  water and water in methanol within 293-303 K (and COSMO-SAC 2010 / Z0x predictions on the same points).
  This is a pilot of feasibility and accuracy only: no fitted constant enters, no Z0 model is changed from
  it, and whatever the numbers, extending the route needs its own registration (systems, compute budget).
  Informative outcomes, stated now: |error| <= 0.3 ln units in both directions with uncertainty <= 0.3 would
  justify a larger registered set; |error| > 0.7 in either direction, or uncertainty > 0.5, would shelve it.
- Profiles v2 operational change (2026-09-26 2:35 PM PDT): O2 failed in every round (closed-shell RKS SCF and
  gradients do not converge for a triplet). Open-shell ground states are now treated spin-unrestricted
  (UKS, 2S = 2 for O=O; list OPEN_SHELL in pyscf_cosmo_v2.py); all closed-shell molecules are unchanged. O2 v2
  profile computed on the Mac (commit 82c4f19). Round 3 (GitHub run 36250934743) added 16 more profiles
  (615/636 with O2); the 21 left are long flexible chains that hit the 6 h runner cap; round 4 (run
  36273318385) uses Berny checkpoints so a cancelled runner's progress is kept for resumption.
- Direct-route ln gamma_inf PILOT RESULT (2026-09-27 5:20 AM PDT, recorded before any follow-up). Replica 1 ran on
  Kaggle T4 GPUs (Modal credits ran out mid-run on 2026-09-26; nothing from the Modal attempt was used), bench15
  settings as registered, 31 ps/window, 28 windows. Coupling free energies (TI +- 5-block SE / MBAR, kcal/mol):
  methanol in water -5.287 +- 0.284 / -5.574; methanol in methanol -3.577 +- 0.271 / -3.630; water in water
  -6.872 +- 0.214 / -6.889; water in methanol -5.684 +- 0.207 / -5.775. All four meet the per-run precision
  gate (SE <= 0.3). With the registered formula and MACE densities (ln(rho_w/rho_m) = +0.819):
  ln gamma_inf(methanol in water) = -2.07 +- 0.66 (MBAR -2.46) vs ThermoML 0.487 (293.15/303.15 K mean,
  2005 set; train split) -> error -2.56. ln gamma_inf(water in methanol) = +1.19 +- 0.50 (MBAR 1.06); no ThermoML
  point in 293-303 K, so not scored. Registered outcome: |error| > 0.7 in a scored direction -> the direct route
  is SHELVED. Replica 2 is not run: it would have to move the result by ~2.5 ln units, 4 SE.
  Diagnosis (post hoc, orientation only): against experimental solvation free energies derived from vapour
  pressures and densities (water in water about -6.3, methanol in water about -5.1, methanol in methanol about
  -4.9 kcal/mol), the model's methanol self-solvation is ~1.3 kcal/mol too weak while the aqueous legs are
  within ~0.2-0.6, so the failure is the potential (MACE-OFF23 small; its methanol density 0.874 vs 0.787 g/cm3
  experimental is also off by 11%), not the sampling. No model constant is changed from this result.
- GPU4PySCF equivalence test (2026-09-27 4:35 PM PDT, RTX 4070 Super, gpu4pyscf 1.8.1, pyscf 2.14.0 CPU reference on the
  same machine, 16 threads): energies agree to <= 6.4e-10 Eh, but it is NOT numerically equivalent: gradients differ by
  up to 1.0e-5 Eh/Bohr (1-octanol SVP) and the C-PCM surface has a different number of points (1535 vs 1533 at SVP,
  3433 vs 3429 at TZVP), so surface charges cannot be compared point by point. Speed: 7.3x (SVP) and 10.9x (TZVP) on
  1-octanol; small molecules gain little. GPU4PySCF is therefore not used to produce any profile.
- GPU pre-stage for the remaining long-chain profiles (registered now, before any use): GPU4PySCF optimises the
  BP86/def2-SVP C-PCM geometry (same functional, basis, radii, eps, Lebedev 17, grid 2) from the usual GFN2-xTB start;
  its final geometry is only a STARTING POINT handed to the registered CPU code as a Berny checkpoint. The CPU path
  (pyscf 2.14, unchanged) re-optimises until the registered Berny convergence test passes, then computes the TZVP
  single point and the profile. Only the starting geometry changes (class A: a different start can reach a different
  conformer). Check before use: the protocol is run on 4 molecules that already have registered CPU profiles
  (decanoic acid, triethylene glycol, heptane, 1,8-diaminooctane); it is accepted if all 4 converge and every
  infinite-dilution ln gamma on their benchmark rows (COSMO-SAC-dsp) changes by < 0.01 vs the existing CPU profiles.
  If rejected, the long chains are completed by the CPU path alone (Mac / 4070 CPU cores).
- GPU pre-stage CHECK RESULT (2026-09-27 5:30 PM PDT, recorded before the protocol's output is used): all 4
  validation molecules converged under the registered CPU Berny test after the GPU start (CPU polish + TZVP: heptane
  90 s, 1,8-diaminooctane 263 s, triethylene glycol 315 s, decanoic acid 493 s on 8 threads, vs 1,668 s for the full
  CPU run of decanoic acid on a 4-core runner). Against the existing CPU v2 profiles: max |d p(sigma)| 1.2e-5, identical
  cavity areas, and over 412 benchmark rows (6 non-finite in both, skipped) the largest change in infinite-dilution
  ln gamma (COSMO-SAC-dsp) is 1e-4, far below the 0.01 bar -> ACCEPTED. The protocol now completes the 15 missing v2
  long chains (resuming from their GitHub Berny checkpoints) and the last 2 ext compounds on the RTX 4070 Super PC.
- P6, analytic interior derivative for Z0x (registered 2026-09-28, before its output is used in any score). Z0x gets
  ln gamma_i from g(x) and dg/dx because c_ES depends on composition. Until now dg/dx was a central finite difference
  with h = 1e-4. Astra round 1 found (and our check confirmed) that this carries up to ~1.9e-3 truncation error in
  ln gamma of the dilute component near x = 0.999, where ln gamma is about 8-11. P6 replaces it with the exact
  derivative of the same g(x) (frozen-c segment solution plus the analytic dc_ES/dx term). Within h of either pure
  end, including infinite dilution, the old one-sided difference is kept, so every ln gamma-infinity is unchanged.
  This is a numerical correction of the same model, not a new model: no constant, no functional form and no data
  enter it. CHECK (run after this entry is pushed; nothing experimental is used): on 250 fixed queries (the first
  50 distinct test-split VLE pairs with profiles, T of their first row, x1 in {0.001, 0.01, 0.5, 0.99, 0.999}), P6
  must agree with a Richardson-extrapolated central difference (h = 2e-4 and 1e-4) to max |d ln gamma| < 1e-4 with
  identical finite coverage. If accepted, P6 becomes the Z0x implementation for all later scoring. The registered
  Z0x scores stay as recorded; the test-split VLE, HE and LLE scores are recomputed with P6 once and reported beside
  them, whichever direction they move. If rejected, main's finite difference stays and P6 is dropped.
- P6 CHECK RESULT (2026-09-28 8:55 AM PDT, recorded before any P6 score is computed): 250 of 250 queries finite
  for both P6 and the reference (identical coverage). max |P6 - Richardson reference| = 2.0e-6, below the 1e-4 bar;
  the old h = 1e-4 finite difference is off by up to 3.1e-4 on the same queries -> ACCEPTED. P6 is now the Z0x
  implementation (analytic interior derivative; one-sided difference within 1e-4 of the pure ends, so ln
  gamma-infinity is unchanged). Details: results/p6_check_out.txt.
- P6 SCORES (2026-09-28, computed once as registered; the registered Z0x numbers stay as recorded). Test split,
  pre-P6 vs P6 Z0x on identical rows: IDAC unchanged by construction (MAE 0.839 both); VLE AAD P 16.13% both
  (largest single-point change 4.5e-5 relative); H^E MAE 619 J/mol both (largest change 3e-9 J/mol); LLE recall
  0.842 both, false-positive rate on the 128 test negatives 0.040 -> 0.055 (5 -> 7), balanced accuracy 0.901 ->
  0.894. The only visible effect of the corrected derivative is two marginal LLE negatives now splitting.
- P9 (E, 2026-09-28): cache the C-PCM surface 3-centre integrals once per surface instead of recomputing them twice
  per SCF iteration (pyscf 2.14 does this with aosym s1). Found by profiling one Berny cycle on GitHub runners
  (~45% of wall time). Fixed-geometry check vs the P1 path (water, O2 UKS, 1-octanol; SVP and TZVP; also the
  memory-limited partial cache): dE <= 1.4e-12 Eh, dG <= 2.5e-13 Eh/Bohr, dq <= 2e-13 e. Paired 25-molecule gate
  (run 36463641537, same runner per molecule): identical Berny evaluations (168 = 168), wall 6,009 s -> 3,183 s
  (1.89x); profile E check below. Setting: ZC_PCM3C (default on after acceptance; 0 restores the P1 path).
  Profile E check (25 molecules): molecules 25, rows 2302, nonfinite_rows 31, max_delta_p 6.9e-09, max_delta_psigmaA_A2 8.2e-07, max_delta_lngamma 1e-07, median_delta_vs_UD 0.15, check_wall_s 9, mode E -> ACCEPTED as E; P9 is now the default.
- Long-chain convergence fallback (registered 2026-09-29 3:00 PM PDT, before any fallback profile exists; class A, used only for
  flagged profiles). Seven benchmark chains (C16-C20 acids/esters/alcohols/alkanes, perfluoroalkanes) did not pass the registered
  Berny test in 200 CPU steps on GitHub runners (twice, 4.5 h each), while three sibling chains needed 2 to 4 restarts and up to 10 h.
  The registered rule stays: a profile is produced only from a geometry that passes the Berny test. FALLBACK, allowed only for a
  chain that has still not converged after the GPU pre-stage plus at least 300 further CPU Berny steps: take its last geometry, run
  the registered TZVP single point and averaging, and flag the profile "fallback" everywhere it is used. VALIDATION (must pass
  before any fallback profile enters a score): for the chains that DID converge after passing through a non-converged checkpoint
  (MJELOWOAIA, QIQXTHQIDY, QUKHPBOCBW), recompute the profile at their last non-converged checkpoint and compare with their
  converged profile: max |d p(sigma)| < 1e-3 and, over every benchmark row that involves them, max |d ln gamma-infinity| (COSMO-SAC-dsp)
  < 0.05. If the validation fails, fallback profiles are not used and those chains stay out of the scored set. Any scorecard that
  includes fallback profiles is reported beside one that excludes them.

- Long-chain fallback validation RESULT (run 2026-09-29 about 8 PM PDT, after the registration above; job 221, cloud/s19/fallback_validate.py). Two of the three registered test chains could be used: QIQXTHQIDY and QUKHPBOCBW, from their last non-converged checkpoints (GitHub run 36486689683 artifacts, Berny cycle 80 for QIQX). MJELOWOAIA could not be tested because its earlier checkpoints were overwritten. Measured against their converged profiles: max |d p(sigma)| = 5.81e-3 (QIQX) and 5.62e-3 (QUKH), against the registered limit of 1e-3, so the sigma-profile criterion FAILS as registered. The ln gamma-infinity criterion passes with a wide margin: over all 72 benchmark rows involving these two chains, max |d ln gamma-inf| = 4.43e-5 (median 7.05e-6) against the limit of 0.05. Consequence under the registered rule: validation failed, so fallback profiles are NOT used and the seven open chains stay out of the scored set until they converge under the Berny test. The limit is not changed after the fact. Context for any later, separately registered decision: the profile peak is 77.4 and 53.8, so the deviations are about 7.5e-5 and 1.0e-4 of peak; a relative criterion would have passed, but it has not been registered and no fallback profile has been scored.

- Berny optimiser-state persistence for the long-chain completion (E-class candidate; registered 2026-09-30 about 4:15 PM PDT, before any gate output is used). Problem: the long chains hit the 100-step Berny cap repeatedly, and the geometry checkpoint restarts pyberny with a fresh model Hessian and trust radius every pass. Change: with ZC_BERNY_STATE=1 (default off; no registered profile has been produced with it) pyscf_cosmo_v2 pickles the pyberny optimiser state (Hessian, trust radius, internal coordinates, step history) next to the geometry checkpoint after every cycle and passes it back through pyberny's own restart argument on resume, if the stored geometry matches the checkpoint geometry to 1e-4 A (otherwise it falls back to geometry-only resume). ZC_MAXSTEPS overrides the per-pass step cap so the gate can force restarts. Functional, basis, C-PCM settings, grids, Berny convergence test and the TZVP profile step are unchanged; the claim is that a run resumed this way follows the same optimisation as an uninterrupted run, so the class is E (numerics only). Local pre-check on 1-heptanol (2 cores, per-pass cap 4, before this registration, not used for any decision): uninterrupted 9 gradient evaluations; state-restored 3 passes, 11 evaluations (9 plus one repeated evaluation per restart), final geometry max |dx| 1.5e-5 A.
  Gate (GitHub Actions, workflow bstate_gate.yml, cloud/s19/bstate_gate.py and bstate_compare.py): 1-octanol (KBPLFHHGFOOTCA) and decanoic acid (WWZKQHOCKIZLMA), three arms each from the same GFN2-xTB start: full (no cap, no state), state (per-pass cap 5, state restored) and geom (per-pass cap 5, geometry-only resume = today's behaviour). The arm runs must finish under the registered Berny test. Accepted if, for BOTH molecules, (i) the state arm needs at most (full evaluations + number of restarts + 1) gradient evaluations and needs at least 2 restarts (otherwise the cap is lowered and the gate rerun), (ii) its final coordinates differ from the full arm by at most 1e-3 A (max abs), (iii) its final SCF energy differs by at most 1e-6 Eh, and (iv) its sigma profile differs by at most 1e-4 (max abs over the 153 bins) from the full arm. The geom arm is reported for comparison only. If accepted, ZC_BERNY_STATE=1 is used for the further passes on the open long chains (checkpoints written before this change have no state, so the first pass after switching still starts from the model Hessian). If rejected, it is not used. Either way a long-chain profile still has to pass the registered Berny convergence test before it is merged, and the fallback rule (no profiles from non-converged geometries) is unchanged.
- bstate gate, first run and runner correction (2026-09-30 about 4:50 PM PDT, written before any of its geometry, energy or profile comparisons were read). GitHub run 36790048897 finished (all six arms completed under the registered Berny test). Its gradient-evaluation counts are INVALID: the runner read the last pass's cycle count from the checkpoint, but run_one deletes the checkpoint on success, so the final pass was recorded as the cap (100 for the full arms, 5 for the capped arms). What was seen before this note: only the pass counts, octanol state 3 and geom 2, decanoic acid state 4 and geom 5, which do not enter the criteria. The runner now records the cycle count before the checkpoint is deleted (same commit as this note) and the gate is rerun in full (same molecules, same three arms, same criteria, nothing else changed). Criterion (i) is decided from the rerun. Criteria (ii) to (iv) will be reported from BOTH runs; if the two runs disagree on a pass/fail, that is reported and the stricter outcome stands.
- bstate gate, run 1 criteria (ii) to (iv) and re-classification (2026-09-30 about 5:00 PM PDT; the run 1 numbers below were read, the run 2 numbers and all ln gamma numbers have NOT been read). Run 1 (GitHub 36790048897), state arm vs uninterrupted arm: 1-octanol max |dx| 1.3e-4 A, dE 1.3e-7 Eh, max |dp(sigma)| 1.68e-3; decanoic acid max |dx| 2.4e-4 A, dE 2.4e-7 Eh, max |dp(sigma)| 3.24e-3. Criteria (ii) and (iii) pass; criterion (iv) (max |dp| <= 1e-4) FAILS for both molecules. So the registered E-class claim is NOT met: a state-restored run does not reproduce the uninterrupted run to the registered numerical precision (the profile peak is of order 50 to 80, so the deviations are about 2e-5 to 6e-5 of peak, the same size as the converged-geometry noise already seen between converged runs of this protocol). For reference, the geometry-only restart arm (today's behaviour) is farther from the uninterrupted run: dx 6.3e-4 / 1.3e-2 A, dE 1.1e-6 / 7.5e-6 Eh, max |dp| 6.1e-3 / 1.9e-1 (decanoic acid's geom arm reached a clearly different geometry). Consequence: state persistence is NOT accepted as E-class, and its registered E-class limit is not changed.
  Separate, new registration as an A-class change (the same rule used for the accepted GPU pre-stage: a different restart path may land in a different converged geometry, so the acceptance is on the quantity that is scored), made after seeing the run 1 numbers above and before any ln gamma number is read: ZC_BERNY_STATE=1 is accepted for the long-chain completion if, for BOTH gate molecules and BOTH gate runs (36790048897 and the rerun), the state arm converged under the registered Berny test and every infinite-dilution ln gamma on the benchmark rows involving the molecule (COSMO-SAC-dsp, computed with cloud/s19/fallback_validate.py lng, sigma override directory = the arm's output) differs from the uninterrupted arm by less than 0.01 (the bar used for the GPU pre-stage). Criterion (i) (gradient evaluations: state arm <= uninterrupted + number of restarts + 1, at least 2 restarts) is unchanged and is decided on the rerun (36792759472). Both must hold. If either fails, state persistence is not used and the long chains continue on the current path.
- bstate gate, rerun results, two corrections and replacement gate molecules (2026-09-30 about 5:25 PM PDT; no ln gamma number has been read). (a) Rerun 36792759472 reproduced run 1 exactly for the state arm (same dx, dE and dp(sigma); criterion (iv) still fails, so the E-class claim stays rejected) and gave valid evaluation counts: 1-octanol full 10, state 12 (3 passes), geom 9 (2 passes); octanoic acid full 16, state 19 (4 passes), geom 21 (5 passes). Criterion (i) passes for the state arm on both. (b) Naming error in the registration above: WWZKQHOCKIZLMA is octanoic acid, not decanoic acid. (c) 1-octanol and octanoic acid have NO rows in the IDAC benchmark (0 rows with a sigma profile), so the registered A-class ln gamma criterion cannot be evaluated on them; the ln gamma comparison scripts returned 0 rows, so nothing was read. (d) What the gate has shown so far is that state persistence does not beat today's geometry-only restart in evaluation count on these small molecules (12 vs 9, 19 vs 21), so no efficiency gain is established.
  Replacement gate, registered before it is run: the same three arms (full, state, geom; same runner, caps and criteria) on the four molecules of the accepted GPU pre-stage check, which do have benchmark rows: decanoic acid GHVNFZFCNZKVNT-UHFFFAOYSA-N (89 rows), triethylene glycol ZIBGPFATKBEMQZ-UHFFFAOYSA-N (127), heptane IMNFDUFMRHMDMM-UHFFFAOYSA-N (98) and 1,8-diaminooctane PWGJDPKCLMLPJW-UHFFFAOYSA-N (104). State persistence is accepted for use on the long chains only if ALL of: (1) every state arm converges under the registered Berny test; (2) over all benchmark rows involving these four molecules, max |d ln gamma-inf| (COSMO-SAC-dsp, cloud/s19/fallback_validate.py lng, sigma override = arm output) between the state arm and the full arm is below 0.01; (3) criterion (i) as registered (state evaluations <= full + restarts + 1, at least 2 restarts per molecule, else the cap is lowered for that molecule and it is rerun); and (4) summed over the four molecules, the state arm needs no more gradient evaluations than the geom arm (otherwise there is no reason to switch). The E-class criteria (ii) to (iv) are reported but do not decide. If any fails, state persistence is not used and this line of work ends. Criterion (4) is new and was added after seeing the octanol and octanoic acid counts above; the molecules are different, so it is a prospective test, not a re-reading.
- bstate replacement gate, partial result and heptane rerun (2026-09-30 about 5:45 PM PDT, GitHub run 36794779866, ln gamma read; heptane at the lowered cap NOT yet run). All twelve arms completed under the registered Berny test, so criterion (1) holds. Criterion (2): over all 398 benchmark rows involving the four molecules (392 finite in all arms, 6 non-finite in all arms), the state arm differs from the uninterrupted arm by at most 5.7e-5 in ln gamma-inf (median 5.2e-6), far below 0.01; the geometry-only arm (today's restart) differs by up to 5.3e-4 (median 9.9e-5), also below 0.01. Criterion (3), state evaluations <= full + restarts + 1 with at least 2 restarts: decanoic acid 12 vs 10 (2 restarts), triethylene glycol 18 vs 15 (3), 1,8-diaminooctane 12 vs 10 (2): pass; heptane converged in one pass at cap 5 (5 evaluations, 0 restarts), so under the registered rule it is rerun with the cap lowered to 2 (all three arms). Criterion (4) (summed state evaluations <= summed geom evaluations) is computed after that rerun; so far decanoic acid 12 vs 18, triethylene glycol 18 vs 13, 1,8-diaminooctane 12 vs 13, heptane 5 vs 5 at cap 5 (47 vs 49, to be recomputed with the heptane cap-2 counts). Reported only (E-class): state-arm max |dp(sigma)| 1.7e-3, 1.1e-3, 6.2e-4 and 7e-11 against 5.6e-2, 1.7e-2, 4.9e-2 and 1e-10 for the geometry-only arm, i.e. the state arm stays 10 to 90 times closer to the uninterrupted profile than today's restart does, but still above the E-class limit of 1e-4. The workflow and runner gained a per-pass cap input (GATE_CAP, default 5) for the heptane rerun; nothing else changed.
- bstate replacement gate: ACCEPTED as an A-class change for the long-chain completion (2026-09-30 about 6:00 PM PDT; heptane rerun read). Heptane at per-pass cap 2 (GitHub run 36797288810): full 5 evaluations, state 8 (4 passes, 3 restarts), geom 16 (8 passes); state vs full max |d ln gamma-inf| over 98 rows (92 finite) 1.7e-5, geom 8.7e-4; state max |dp(sigma)| 1.3e-3, geom 9.1e-2. All four registered criteria hold: (1) all 12+3 state arms converged under the registered Berny test; (2) max |d ln gamma-inf| state vs full over the 398 benchmark rows of the four molecules is 5.7e-5, below 0.01; (3) evaluations state <= full + restarts + 1 with >= 2 restarts: decanoic acid 12 vs 10, triethylene glycol 18 vs 15, 1,8-diaminooctane 12 vs 10, heptane (cap 2) 8 vs 5; (4) summed over the four molecules the state arm needs 50 gradient evaluations against 60 for the geometry-only restart (12+18+12+8 vs 18+13+13+16). The E-class claim stays rejected (state-arm max |dp(sigma)| is 6e-4 to 1.7e-3 against the E limit of 1e-4) and is not used as an equivalence claim; the acceptance is A-class, on the scored quantity. Use: ZC_BERNY_STATE=1 for the continuing passes on the six open long chains (BTFJIXJJCSYFAL, FLIACVVOZYBSBS, HPEUJPJOZXNMSJ, MVLVMROFTAUDAG, OYHQOLUKZRVURQ-HZJYTTRNSA-N, PYGXAGIECVVIOZ), from their current geometry checkpoints (no optimiser state exists for them yet, so the first pass after the switch rebuilds the model Hessian). A profile from these runs is merged only if it passes the registered Berny convergence test. First deployment: GitHub Actions workflow open-profiles-v2 with ZC_BERNY_STATE=1 and a per-pass cap of 300 steps (the run is limited by its 320-minute compute deadline instead; the checkpoint and the .bstate file are uploaded as artifacts and can seed the next run), seeded from the geometry checkpoints that the previous Actions run (36754184540) returned.

- Long-chain STALL rule S1 (registered 2026-10-01 06:43 PDT (commit 979d518; the time was filled in afterwards because a sed error left a placeholder), before any S1 profile exists; class A; flagged; exploratory use only). This is NOT the
  fallback of 2026-09-29, which failed its validation and stays unused. Facts established by diagnostics only (no sigma profile was computed or used):
  after 5 or more 100-step Berny passes the six open chains (BTFJIXJJCS, FLIACVVOZY, HPEUJPJOZX, MVLVMROFTA, OYHQOLUKZR, PYGXAGIECV) have
  an internal-coordinate gradient of max 1.4e-5 to 6.7e-5 (rms 5e-6 to 1.4e-5) and energy changes of order 1e-7 Eh per cycle, and the last 5.5 h run
  (about 100 cycles each) moved their geometries by at most 0.002 Angstrom. At the FLIACVVOZY checkpoint (53 atoms) a Cartesian gradient evaluation
  with the registered settings gives max 1.7e-5, rms 6.4e-6 Eh/Bohr (grids level 3: 1.75e-5, 6.8e-6), i.e. 25x below Berny's own gradient thresholds
  (max 4.5e-4, rms 1.5e-4). Berny's per-cycle log shows the only unmet criterion is "Minimization on sphere": the quadratic step is always on the
  trust sphere because the softest mode has curvature 1.0e-3 and the trust radius, driven by energy changes (1e-7 Eh) that are at the noise of the
  SCF/C-PCM energy, oscillates between 4e-4 and 4e-3. Berny therefore cannot declare convergence although the geometry is stationary.
  RULE S1 (all of a, b, c are required; thresholds fixed here): a long chain that has not been declared converged after at least 5 passes of 100 Berny
  steps may be accepted at its latest checkpoint if (a) one Cartesian gradient evaluation at that checkpoint with the unchanged registered settings
  (BP86/def2-SVP, density fitting, C-PCM conductor, grids level 2, Lebedev 17) has max < 4.5e-4 and rms < 1.5e-4 Eh/Bohr, i.e. Berny's own gradient
  criteria; (b) the checkpoint is at least 90 optimiser cycles after the earlier checkpoint it was restarted from (separate runs) and the maximum
  atomic displacement between the two is <= 0.005 Angstrom; (c) the registered TZVP profiles computed at the two checkpoints differ by max |d p(sigma)| < 1e-3
  and, over every benchmark row involving the chain that has a COSMO-SAC-dsp value in both, max |d ln gamma-infinity| < 0.05 (the same limits as the
  2026-09-29 fallback validation, not loosened; if a chain has no such rows, criterion c reduces to the p(sigma) limit and this is stated). What c measures is
  stability of the profile under about 100 further optimiser cycles, not distance to a Berny-converged profile, which cannot be computed for these chains.
  Accepted profiles are written outside profiles_v2 (data/pyscf_sigma/s1_stalled), carry meta geometry_converged="S1", and enter any score only
  in a second column: every scorecard that includes S1 profiles is reported beside one that excludes the rows involving them. Berny-converged profiles
  remain the primary set. The optimisation jobs on GitHub Actions, Kaggle, the 4070 and the 2060 PC continue unchanged in case a chain does converge
  by the registered test; a Berny-converged profile replaces the S1 profile for that chain.

- Long-chain stall rule S1, RESULTS (recorded 2026-10-01 10:27 PDT; computed 2026-10-01 06:43 to 10:23 PDT with cloud/s19/stall_accept.py after the registration above; nothing was changed
  after seeing them). Per chain: atoms; optimiser cycles since resume at the new checkpoint; max atomic displacement vs the checkpoint of the previous run (Angstrom); Cartesian gradient max / rms
  (Eh/Bohr; limits 4.5e-4 / 1.5e-4); max |d p(sigma)| between the profiles at the two checkpoints (limit 1e-3); peak p(sigma)A.
  FLIACVVOZY 53; 133; 0.0007; 1.7e-5 / 6.4e-6; 2.35e-3; 69.2 -> a ok, b ok, c FAILS (p(sigma)).
  BTFJIXJJCS 63; 92; 0.0020; 3.3e-5 / 8.0e-6; 1.32e-2; 89.7 -> a ok, b ok, c FAILS.
  OYHQOLUKZR 52; 127; 0.0016; 1.9e-5 / 5.3e-6; 7.06e-3; 61.9 -> a ok, b ok, c FAILS.
  HPEUJPJOZX 59; 104; 0.0002; 4.1e-5 / 8.7e-6; 2.68e-3; 83.9 -> a ok, b ok, c FAILS.
  PYGXAGIECV 56; 140; 0.0003; 9.7e-5 / 2.2e-5; 1.057e-3; 70.9 -> a ok, b ok, c FAILS (by 6 percent).
  MVLVMROFTA 62; 96; 0.0000; 3.8e-5 / 1.1e-5; 2.9e-5; 88.5 -> a ok, b ok, c ok. It has no row at all in data/benchmark/idac.csv, so the ln gamma half of c is empty and c reduces to the p(sigma) limit, as registered.
  Under rule S1 as registered: MVLVMROFTA is ACCEPTED (flagged geometry_converged="S1", file data/pyscf_sigma/s1_stalled/MVLVMROFTAUDAG-UHFFFAOYSA-N.sigma, NOT in profiles_v2, only in a second scorecard column). Its geometry did not move between the two
  checkpoints at all (0.0000 A), so criterion b and the small p(sigma) difference are satisfied trivially; its acceptance rests on criterion a (gradient far below Berny's thresholds). The other five are NOT accepted and stay out of every scored set;
  the p(sigma) limit is not changed. Berny-converged profiles remain the primary set (profiles_v2 stays at 630/636).
  Informational, not an acceptance route (computed after the five rejections): (1) ln gamma-infinity sensitivity, COSMO-SAC-dsp, S1-new vs S1-old profile, each evaluated in its own process: OYHQOLUKZR 67 benchmark rows, max |d ln gamma| 6.7e-5;
  BTFJIXJJCS 84 rows, max 2.8e-5 (limit 0.05); FLIACVVOZY, HPEUJPJOZX, MVLVMROFTA and PYGXAGIECV have no rows in idac.csv. A first run (job 290) printed exactly 0.0 because both profile sets were evaluated in one process and the profile is cached after the first load;
  it was discarded and redone (job 292). (2) Profile noise floor (job 289, one chain, one rotation): the FLIACVVOZY profile recomputed at its new checkpoint geometry rigidly rotated by 0.001 rad, nothing else changed, differs from the unrotated profile by
  max |d p(sigma)| = 1.6e-2, i.e. larger than the p(sigma) differences between the checkpoints of all five rejected chains (1.1e-3 to 1.3e-2). So the p(sigma) limit of 1e-3 (shared with the 2026-09-29 fallback validation, whose
  deviations of 5.6e-3 and 5.8e-3 were also below this floor) lies well below the numerical noise of the profile calculation and can only be met by two evaluations in the same orientation with essentially identical geometry; it does not measure whether geometries differ.
  Caveat: one rotation on one molecule. NOT applied: a noise-referenced profile limit (for example relative to the measured rotation floor, together with the unchanged 0.05 ln gamma limit) would be a new rule, to be registered separately before any use and to be put to
  the Astra review on 2026-10-02; until then no profile of the five rejected chains is used anywhere.

## Proposed R2 noise-aware Berny trial, class A

Register this text with its actual commit timestamp before any trial profile or
score is read. This trial is motivated by the previously observed stalls, so it
is not a blind discovery. Pyberny is fixed at 0.7.0. Its energy_noise parameter is
set to 2e-7 Eh, including in a restored BernyState; every energy, gradient, basis,
auxiliary basis, XC grid and PCM setting is unchanged. The original Berny
convergence criteria, including the on-sphere condition, remain mandatory.
No experimental response selects this value. There is one candidate, no sweep.

The comparison uses the historical 25-molecule/2302-row manifest, with identical
finite coverage. All 25 candidates must pass the original Berny test; maximum
absolute change in COSMO-SAC-dsp ln gamma-infinity against current-main profiles
must be below 0.01; the median absolute difference against UD must remain below
0.15. Report both normalized distributions and raw psigmaA bins, without
reinterpreting either existing E or fallback limit. Paired total wall time on
the 25 molecules must be no more than 1.10 times reference. Separately freeze and
hash the six current long-chain geometries before the trial. Run at most 100 new
CPU gradient evaluations per chain, from the same geometry and optimizer state
in each arm, with the same already-accepted A-class restart protocol. At least
one formerly stalled chain must newly pass the original Berny test within that
budget, and all resulting profiles remain exploratory until the 25-molecule
checks pass. An unfinished arm is censored, not assigned an invented time to
convergence. No S1 failure is reclassified by this trial. Rejection leaves the
accepted GPU-prestage and A-class restart protocols unchanged.

Execution plan for the P15 trial above (registered in the same commit, 2026-10-04 01:49 PDT, before any P15 run exists; code at
this commit = main eab6c25 plus Astra's P15 patch, applied unchanged; Astra report saved as docs/astra/round2/ZCOSMO_ROUND2_REPORT.md).
Compute: GitHub Actions ubuntu-latest runners, 4 threads, pyscf 2.14.0, pyberny pinned 0.7.0 in both arms.
(1) Long chains, workflow .github/workflows/p15_long.yml: the six seeds as committed in cloud/s19/seeds at this commit
(last changed in 8c03cc8; geometry + optimizer state from Actions run 36826764833), copied, never modified, sha256 printed per job.
Arms base (pyberny defaults) and P15 (ZC_BERNY_NOISE_EH=2e-7) run concurrently on separate runners. Each arm gets 100 new gradient
evaluations as two consecutive 50-step passes (ZC_BERNY_STATE=1, the accepted A-class restart; each restart, including the first,
re-evaluates the checkpoint geometry once, identically in both arms) because one 100-step pass does not reliably fit in a 6-hour job.
A chain that has not passed the original Berny test after the second pass is censored. Chain wall time is not gated.
(2) 25-molecule validation, workflow .github/workflows/p15_gate.yml: per molecule, reference arm (defaults) then P15, back to back
on one runner (as the P9 gate), H0 harness (docs/astra/round1/patches/H0.patch); paired wall time = sum over the 25 molecules.
Gates exactly as in the text above: all 25 P15 geometries pass the original Berny test, identical finite coverage,
max |d ln gamma-inf| < 0.01 vs the reference arm, median |d| vs UD < 0.15, paired wall <= 1.10 x reference; max normalized and raw
psigmaA bin differences reported, not gated.
Decision rule: P15 is accepted (class A) only if the 25-molecule gates pass AND at least one of the six chains passes the original
Berny test in the P15 arm within its 100 evaluations. If accepted, each chain profile produced by the P15 arm may enter profiles_v2,
marked geometry_protocol "A-R2-noise-aware-trust-2e-7-Eh"; the result is recorded here before any such profile is scored. If not
accepted, no P15 profile is used anywhere. A chain that converges in the base arm is an ordinary Berny-converged profile under the
existing protocol. The 4070 and PC2 continue the existing protocol unchanged throughout.
Pre-trial state, read from the frozen optimizer states before registration (not trial output): the predicted energy changes stored
in the six states are 5.7e-8 to 3.7e-7 Eh in magnitude, trust radii 3.6e-4 to 5.9e-3; five of six are below the default noise-branch
threshold (2e-7) at this step, all six below the P15 threshold (2e-6). So the default branch is already active at some steps; the trial
tests whether removing the ratio-branch shrinks for predicted changes between 2e-7 and 2e-6 Eh lets the steps leave the trust sphere.

- P15 noise-aware Berny trust update (energy_noise 2e-7 Eh, class A), RESULTS (recorded 2026-10-04 08:58 PDT; registered 2026-10-04 01:49 PDT in 2e9e459, before any run).
  Decision: REJECTED. The 25-molecule gates passed, but the second registered condition failed: no chain passed the original Berny test in the P15 arm
  within its 100 evaluations. No P15 profile is used anywhere; the accepted GPU-prestage and A-class restart protocols are unchanged; no S1 decision changes.
  (1) 25-molecule validation, Actions run 37190183654 (per molecule, reference then P15 on one runner): 25/25 P15 geometries passed the original Berny test;
  2302 rows with the same 31 non-finite rows in both arms; max |d ln gamma-inf| (COSMO-SAC-dsp, P15 vs reference) 2.15e-4 (limit 0.01); median |d| vs UD 0.1493
  (limit 0.15); paired wall 3217 s vs 3360 s = 0.957 (limit 1.10); geometry evaluations 163 vs 168; reported, not gated: max normalized-bin difference 6.5e-5,
  max raw psigmaA-bin difference 0.0132. Deviation in execution, not in criteria: the workflow's compare job stopped before evaluating because the UD reference
  profiles (data/raw/nist/UD) are gitignored and absent on the runner; the identical H0 'profiles --mode A' comparison and the registered gate arithmetic were
  run on the Mac from that run's artifacts (queue job 311).
  (2) Long chains, Actions run 37190177507, six frozen seeds, arms base and P15, two 50-step passes each with the accepted state restart: all 12 arm-chains
  ended both passes with 'Berny did not converge in 50 steps' (cycle 49 of 49 each pass), i.e. all censored at 100 evaluations in both arms. BTFJIXJJCS,
  FLIACVVOZY, HPEUJPJOZX, MVLVMROFTA, OYHQOLUKZR, PYGXAGIECV: base censored, P15 censored. Pass wall times 1h45m to 3h28m per job.
  profiles_v2 stays 630/636. The six chains remain open under the existing protocol (4070 and PC2 continue); MVLVMROFTA remains the single flagged S1 profile
  outside profiles_v2.

- Long-chain stall rule S2, orientation-referenced profile stability (registered 2026-10-04 14:09 PDT, before any S2 computation exists; class A; flagged; exploratory use
  only). Motivation, stated plainly: this rule is post hoc. It was designed after S1 rejected five chains on its absolute p(sigma) limit (1e-3) and after one
  diagnostic (FLIACVVOZY, one 0.001 rad rotation) showed that re-orienting an identical geometry changes the profile by 1.6e-2, more than the
  checkpoint-to-checkpoint differences S1 rejected (1.1e-3 to 1.3e-2), and after P15 (energy_noise 2e-7 Eh) failed to make any chain pass Berny's test.
  The Astra round-2 review (docs/astra/round2/ZCOSMO_ROUND2_REPORT.md) said the S1 limit must not be silently replaced, and that an orientation-aware metric
  needs its own registration on a frozen set of molecules and rotations. This is that registration. S1, its results, and the P15 result stand unchanged.
  Frozen inputs: the six chains BTFJIXJJCS, FLIACVVOZY, HPEUJPJOZX, MVLVMROFTA, OYHQOLUKZR, PYGXAGIECV. OLD checkpoint = cloud/s19/seeds as committed in
  8c03cc8. NEW checkpoint = the base-arm checkpoint after pass 2 of Actions run 37190177507 (artifact p15long2_<KEY>_base), i.e. 100 gradient evaluations
  later under the existing protocol (pyberny defaults, accepted state restart). Neither geometry nor any profile at the NEW checkpoint has been examined
  before this registration. Rotations: scipy Rotation.random(8, random_state=20261004), applied about the centroid of the NEW geometry; fixed here, no
  re-draw. All profiles: the registered TZVP conductor profile (cosmo_segments + to_profiles, unchanged); p(sigma) compared as in S1 (max |d psigmaA| over
  the three profiles). Code: cloud/s19/s2_item.py (one item per job), .github/workflows/s2_profiles.yml (Actions, pyscf 2.14.0, pyberny 0.7.0),
  cloud/s19/s2_evaluate.py (run on the Mac, where the UD reference profiles needed for ln gamma are present).
  RULE S2 (all of a, b, c1, c2, d are required; thresholds fixed here). For each chain: (a) Cartesian gradient at NEW with the registered settings,
  max < 4.5e-4 and rms < 1.5e-4 Eh/Bohr (as S1); (b) max atomic displacement NEW vs OLD <= 0.005 Angstrom with 100 gradient evaluations between them
  (as S1); T_med and T_max = the median and the maximum, over the 8 rotations, of max |d p(sigma)| between the NEW profile and the NEW geometry rotated;
  (c1) max |d p(sigma)| between the NEW and OLD profiles <= T_med, i.e. 100 further optimiser cycles change the profile by no more than a typical rigid
  re-orientation of one fixed geometry does; (c2) over every benchmark row involving the chain (data/benchmark/idac.csv, COSMO-SAC-dsp, every other compound
  from profiles_v2, NEW and OLD evaluated in separate processes) identical finite coverage and max |d ln gamma-infinity| < 0.05 (the S1 limit, not loosened;
  if a chain has no such rows, c2 reduces to coverage and this is stated); (d) discrimination control: max |d p(sigma)| between the NEW profile and the
  profile at the chain's own xTB start geometry (RDKit seed 7, GFN2-xTB, the construction the optimisation started from) > T_max. If d fails, the metric
  cannot tell this chain's DFT geometry from its starting geometry and the chain is not accepted. Reported, not gated: the profile at NEW plus a random
  displacement scaled to max 0.02 Angstrom (numpy default_rng(20261004)), its d p(sigma) against NEW, and every rotation angle.
  Use: accepted profiles (the NEW profile) go to data/pyscf_sigma/s2_stalled with meta geometry_converged="S2", outside profiles_v2, and enter any score only
  in a second column beside a score that excludes them, exactly as S1. MVLVMROFTA keeps its S1 profile; S2 is computed and reported for it but does not
  replace it. If all six chains then hold an S1 or S2 profile, the Z0x-open exploratory scoring vs Z0x on the test split is run once on profiles_v2 plus
  those six flagged profiles, labelled "636 incl. 6 stall-accepted (S1/S2)", and reported beside the existing 630-profile coverage. It does not count as
  profiles_v2 reaching 636/636, and no primary result changes. A Berny-converged profile, if one ever arrives from the 4070 or PC2, replaces the S1/S2
  profile for that chain. Results are recorded here before any S2 profile is used.

- Long-chain stall rule S2, RESULTS (recorded 2026-10-04 16:15 PDT; Actions run 37234965922, 78/78 items succeeded; evaluated with cloud/s19/s2_evaluate.py on the Mac, queue job 318;
  nothing changed after seeing them). Per chain: Cartesian gradient max / rms at NEW (Eh/Bohr); max displacement NEW vs OLD (A, 100 evaluations apart); T_med / T_max
  (median / max over the 8 fixed rotations of max |d p(sigma)|, same units as psigmaA); max |d p(sigma)| NEW vs OLD; ln gamma rows, max |d ln gamma| NEW vs OLD;
  max |d p(sigma)| NEW vs xTB start (must exceed T_max); report-only: NEW vs NEW+0.02 A random displacement.
  BTFJIXJJCS 3.3e-5 / 8.0e-6; 0.0009; 0.896 / 1.275; 5.8e-3; 84 rows, 1.4e-5; 12.38; 2.04 -> a b c1 c2 d all hold: ACCEPTED.
  FLIACVVOZY 2.1e-5 / 6.7e-6; 0.0007; 1.953 / 3.118; 2.3e-3; 0 rows (c2 = coverage only); 9.30; 1.11 -> ACCEPTED.
  HPEUJPJOZX 3.7e-5 / 8.3e-6; 0.0011; 0.930 / 1.255; 7.0e-3; 0 rows; 12.13; 1.47 -> ACCEPTED.
  MVLVMROFTA 3.3e-5 / 1.1e-5; 0.0018; 0.772 / 1.587; 1.67e-2; 0 rows; 6.16; 0.98 -> ACCEPTED by S2; as registered it keeps its S1 profile.
  OYHQOLUKZR 1.9e-5 / 5.5e-6; 0.0016; 1.144 / 1.669; 7.6e-3; 67 rows, 2.4e-5; 5.85; 1.30 -> ACCEPTED.
  PYGXAGIECV 9.6e-5 / 2.2e-5; 0.0012; 0.940 / 1.242; 4.8e-3; 0 rows; 3.09; 0.82 -> ACCEPTED.
  What these numbers mean, stated so they are not over-read: (1) A full random rigid rotation of one fixed geometry changes the TZVP profile by 0.48 to 3.1 in max
  |d psigmaA| (peaks are about 60 to 90), i.e. one to a few percent, about 30 to 200 times the single 0.001 rad diagnostic of 2026-10-01 (1.6e-2). The profiles
  of this protocol are therefore orientation-dependent at the percent level; this applies to every profile in profiles_v2, each computed in one orientation.
  (2) The checkpoint-to-checkpoint changes (2.3e-3 to 1.7e-2) are 50 to 800 times below T_med, so c1 holds by a wide margin and would also have held against the
  smallest rotation (min 0.48). (3) The report-only control shows that a random 0.02 A displacement (4 times the b limit) also changes the profile by less than
  T_med for every chain, so at the scale of the orientation floor the p(sigma) metric does not resolve geometry differences of that size; the acceptance rests
  on a and b (gradients 5 to 25 times below Berny's limits, displacement <= 0.0018 A over 100 evaluations) together with d, which shows the metric does separate
  the DFT geometry from the xTB start. (4) ln gamma-infinity changes NEW vs OLD are 1.4e-5 and 2.4e-5 on the two chains with benchmark rows.
  Use, as registered: BTFJIXJJCS, FLIACVVOZY, HPEUJPJOZX, OYHQOLUKZR and PYGXAGIECV get their NEW profile in data/pyscf_sigma/s2_stalled (meta
  geometry_converged="S2"); MVLVMROFTA keeps data/pyscf_sigma/s1_stalled. profiles_v2 stays 630/636; nothing primary changes. All six chains now hold a flagged
  profile, so the Z0x-open exploratory scoring on profiles_v2 plus these six is run once next, labelled "636 incl. 6 stall-accepted (S1/S2)", with a column
  that excludes every row involving the six. Not tested and not claimed: how much the percent-level orientation dependence moves ln gamma across the whole set.

- Z0x-open, EXPLORATORY, "636 incl. 6 stall-accepted (S1/S2)" (recorded 2026-10-04 18:20 PDT; computed 2026-10-04 16:15 to 17:59 PDT, queue job 319). Z0x evaluated with every
  compound's profile taken from profiles_v2 (630, Berny-converged) plus the six flagged long-chain profiles (MVLVMROFTA S1, the other five S2); reference = the stored
  Z0x predictions (results/predictions, UD profiles). Test split, metrics as in the scorecard. Only IDAC and LLE have a stored Z0x reference, so VLE and HE were predicted
  but not compared. profiles_v2 is still 630/636; this is not the registered 636/636 run and changes no primary result.
  All rows: IDAC (828 points, 204 systems) MAE Z0x 0.839 [0.705, 0.974], Z0x-open 0.977 [0.841, 1.110], dMAE CI [+0.052, +0.232] (open is worse); bias -0.212 vs -0.368;
  within 0.3: 0.28 vs 0.26; solvent-rank rho 0.83 vs 0.77. LLE (2475 points, 101 systems): gap found 0.84 vs 0.82, MAE x when found 0.175 vs 0.175.
  Excluding every row that involves one of the six chains (151 IDAC and 6 LLE rows dropped): IDAC (816 points, 201 systems) MAE 0.804 [0.687, 0.933] vs 0.942
  [0.805, 1.084], dMAE CI [+0.051, +0.230]; LLE (2469 points, 100 systems) gap found 0.84 vs 0.82. The six flagged profiles barely move the comparison; the deficit
  of open profiles against UD is the same with or without them, consistent with the 2026-09-25 v2 acceptance margin (median 0.1493 vs 0.15).
  Note: the stored Z0x reference gives 0.839 on this 828-point common subset, not the 0.800 quoted earlier for the test split; the reference file was not regenerated here.

- Round 3 (Astra report docs/astra/round3/ZCOSMO_ROUND3_REPORT.md, received 2026-10-05). Victor chose "register all, run in order". The text below is Astra's
  proposed registration (docs/astra/round3/PROPOSED_REGISTRATION.md) appended unchanged, registered 2026-10-05 00:12 PDT in the same commit as the six patches (H3, P16, P17,
  P18, P19, REG, applied unchanged to c515e38; P18 production flag default off) and before any R3 native output exists. Execution notes, fixed here: native P17/P19
  items run on GitHub Actions (ubuntu-latest, pyscf 2.14.0, pyberny 0.7.0, 4 threads) from the experiment frozen in cloud/r3/orientation (frozen on the Mac from
  data/pyscf_sigma/profiles_v2 geometries, committed right after this entry); every UD-backed score, gate and the P16/P18 work runs on the Mac, where the UD
  profiles exist, in a worktree of this commit. Order: P16, P17 raw panel, P18 on the raw identity profiles, the P17 A recipes, P19, then the round-2 P14 sidecar.

## R3 prospective profile reliability and final-precision experiments

This entry is registered with the actual commit timestamp before any R3 native candidate output or score is read. It is motivated by the known R2/P15 rejection, S2 rotation results, and exploratory Z0x-open deficit; it is not a new held-out discovery. The historical P15, S1, S2, and Z0x-open decisions remain unchanged. Reference code is c515e38e1a7fd91a02e1ff1f1209a81b67a7d49d plus the explicitly archived R3 experimental helpers. All output directories are separate from profiles_v2 and all stored scorecards. No experimental response determines a parameter or selects a profile recipe.

P16 audits existing predictions by immutable observation identity, finite coverage, model-list intersection, split, and class/role. The class mapping and four-corner UD/open solute/solvent attribution in scripts/r3_idac.py and r3_hybrid.py are frozen by this commit. These are descriptive post hoc diagnostics. No prediction or experimental value is rewritten. Historical scores are preserved with their original denominator and provenance; a discrepant score is corrected only in a separately identified report.

P17 raw orientation experiment freezes the historical 25 keys and 2,302 query occurrences, plus the saved geometry bytes, source hashes, and fixed rotation matrices. Recompute an identity profile at those exact coordinates rather than treating a rounded XYZ file as identical to the original SCF geometry. For all 25, compute identity, a repeat identity, cube90, and r0 through r7 from scipy Rotation.random(16, random_state=20261004); its first eight equal S2's rotation set. On water, methanol, and decanoic acid additionally use rotations of 0.001, 0.01, 0.1, 0.5, and 1.0 radians about normalized (1,2,3). This is 290 TZVP single points. Every profile uses pinned pyscf 2.14.0, the unchanged BP86/def2-TZVP, grid level 3/default pruning, C-PCM epsilon 1e9, project radii, Lebedev 29 and conv_tol 1e-9. The source's q, Hsieh averaging, and split are unchanged. Co-rotation of already-computed segments is an E postprocessing control, not a new electronic calculation. Report raw and normalized bins separately, area, volume, charge sum, the surface-normal closure defect, and translated/co-rotated volume checks. Use separate processes per profile set and molecule for the registered one-compound replacement check, with identical finite masks. Measure both COSMO-SAC-dsp and Z0x, including solute and solvent roles; no amount of raw-bin variation alone establishes a ln gamma error.

P17 A candidates are fixed here: canonical proper body-frame orientation with the deterministic degeneracy/atom-order rules in r3_common.canonical_xyz; equal-weight averages of raw psigmaA and volume over r0..r7 (mean8), r8..r15 (mean8b), and r0..r15 (mean16); and Lebedev order 41 with every other single-point/postprocessing setting unchanged. These are distinct experimental recipes, never combined implicitly. The averaging extension costs 200 additional raw TZVP single points. Canonical and Lebedev41 validation each use identity plus r0..r7 on all 25, at most 225 new single points per recipe. The canonical recipe must reproduce its own identity ln gamma across all eight rotations to max 1e-3 for both models. Lebedev41 must reduce the panel maximum orientation difference by at least one half and leave it below 0.01 for both models. Mean8 versus the disjoint mean8b must differ by max less than 0.01 in both models, and mean8 versus mean16 by max less than 0.005; these are finite-set consistency checks, not proofs of rotational invariance or continuum convergence. Each candidate additionally requires identical finite coverage versus the raw identity reference for both models, max COSMO-SAC-dsp ln gamma change below 0.05, and median COSMO-SAC-dsp difference versus UD below 0.15 on the frozen 2,302 occurrences. All changes in Z0x and both bin metrics are reported. The old E thresholds are not relaxed. Passing makes a recipe eligible for a separately authorized exploratory scoring pass, not an automatic replacement of the 630 primary profiles. There is no selection by best experimental MAE. A wider averaging radius, a new decay constant, or altered HB splitting is not authorized by this entry.

P18 is an A numerical correction of profile metadata: preserve the NIST parser's COOH flag for a molecule whose own geometry-based parser sets has_COOH. Water retains H2O. Use ZC_R3_COOH_FLAG=1 only in an explicitly designated arm, or the metadata-only reconstruction in scripts/r3_metadata.py. Acceptance requires byte-identical raw sigma rows, unchanged metadata values other than the flag and explicit provenance fields, exact agreement with the existing parser's H2O/COOH/other flag rule, and identical finite coverage on the 25/2,302 check. In the one-compound substitution check, rows targeting a compound whose flag is unchanged must remain unchanged within 1e-10; Z0x predictions must remain unchanged within 1e-10 because its London dispersion does not use this flag. Report all COSMO-SAC-dsp changes and rerun the old UD acceptance statistic. If its median criterion fails, this corrected profile protocol is recorded as not accepted as a UD substitute, rather than restoring an incorrect flag to obtain a pass. The correction is not claimed to explain the Z0x-open deficit. Nothing is rescored silently.

P19 is a single A final-precision trial, not an optimizer/threshold sweep. Pin pyscf 2.14.0 and pyberny 0.7.0. Starting from the same frozen geometry in each arm with fresh Berny histories, give the candidate at most 80 gradient evaluations at BP86/def2-SVP with the same DF auxiliary basis, grid level 2/default pruning, C-PCM epsilon 1e9/Lebedev 17/project radii, but conv_tol=1e-11 and conv_tol_grad=1e-7. Give the control the same 80-evaluation stage with original SCF tolerances. Then both arms receive at most 20 evaluations with a fresh Berny optimizer and all original registered settings, including conv_tol=1e-8 and its default orbital-gradient tolerance. Only convergence of this original-settings confirmation stage counts. The original internal-coordinate gradient/step tests and on-sphere rejection remain unchanged. No P15 noise override, looser geometry threshold, finer grid, different optimizer, or existing optimizer pickle is used. Native SCF failures are failures; exhausted budgets are censored. Never extend an arm after inspecting the result.

For P19, first run both arms from the frozen saved geometries of all 25 validation molecules. All 25 must pass the original confirmation test, have identical finite coverage, max COSMO-SAC-dsp ln gamma change below 0.01 against the control, and median difference from UD below 0.15. Paired total wall time must be at most 1.50 times control; raw and normalized bins are reported without changing the historical E gates. Freeze and hash six chain inputs before either arm runs. A maximum of 100 total new quantum gradient evaluations per arm/chain is permitted, with a fixed runner deadline reserved for saving artifacts. The long-chain usefulness condition is at least one original-confirmation success in the tight arm whose control remains censored. Both this condition and the 25-molecule gate must pass. After acceptance, only chains passing the actual original confirmation test may replace S1/S2 profiles, with explicit A protocol metadata and side-by-side reporting. No flagged geometry is reclassified on a small Cartesian gradient alone.

- Round 3 RESULTS (recorded 2026-10-05 02:41 PDT; registered 2026-10-05 00:12 PDT in 9d32e9e, experiment frozen in 0e8a918; native items on GitHub Actions runs 37276471441,
  37278651575, 37278662729, 37278674224 (P17) and 37276959037 (P19 calibration); every UD-backed score and gate on the Mac, queue jobs 323, 324, 326, 328, 329).
  P16 IDAC audit (descriptive). A fresh Z0x evaluation reproduces the stored predictions to 2.9e-10, so there is no prediction drift. Z0x test IDAC MAE is 0.839
  on all 828 test rows (204 systems); the 0.800 quoted since 2026-09-25 is the same predictions on the 762-row common subset of the scorecard that also contained
  unifac_do, cosmosac2010 and Z0w (results/scorecard_test_z0w*.json). Both numbers stand with their denominators. The exploratory Z0x-open deficit (+0.137 on 828
  rows) is a solvent-role effect: four-corner attribution gives solvent +0.236, solute -0.099. By solvent class, "multifunctional" solvents contribute +0.163
  (136 rows, MAE 0.73 -> 1.72); by compound, diethylene glycol as solvent alone contributes +0.137 (108 rows, MAE 0.69 -> 1.74), triethylene glycol +0.024,
  ethylene glycol +0.023; the solutes in those rows are mostly alkanes and alkenes (n-nonane +0.046, 1-heptene +0.018, n-octane +0.015). Water as solvent
  improves (-0.016). Removing the six flagged chains changes nothing material.
  P17 raw orientation panel (290 TZVP single points, all completed). Co-rotating existing segments reproduces the profile to 2.8e-14 (the parser is invariant;
  the dependence comes from the surface/SCF). Identity and repeat are identical; the identity profile reproduces the historical acceptance statistic (median
  0.1493). Eight random rotations change ln gamma-inf on the 2,302 occurrences by a mean of 0.008 (COSMO-SAC-dsp) and 0.011 (Z0x) per rotation; panel maxima
  0.076 and 0.111; cube90 changes nothing (< 2e-4). Fixed-axis angle ladder (max |d psigmaA| vs identity, water / methanol / decanoic acid): 0.001 rad
  0.021 / 0.008 / 0.012; 0.01 rad 0.21 / 0.089 / 0.11; 0.1 rad 0.60 / 0.39 / 1.16; 0.5 rad 0.54 / 0.48 / 0.56; 1.0 rad 0.58 / 0.56 / 0.89, i.e. the
  change grows up to about 0.1 rad and then saturates. Surface-normal closure defects reach 0.43 A2, origin-shift volume changes 0.39 A3. Conclusion:
  orientation is a real but small uncertainty in ln gamma (about 0.01 typical) and cannot explain the 0.137 deficit.
  P17 A recipes, registered gates, all NOT accepted: canonical orientation is exactly rotation-invariant (panel max 2e-10, gate passes) but fails the
  compatibility gate (max COSMO-SAC-dsp change 0.0567 > 0.05; median vs UD 0.1502 > 0.15); Lebedev 41 reduces the panel maximum only from 0.076/0.111 to
  0.069/0.070 (needs half and < 0.01: fails) and fails compatibility (0.075 > 0.05); mean8 fails compatibility (0.054 > 0.05) and its finite-set
  stability (mean8 vs mean8b 0.021 / 0.030 vs 0.01; mean8 vs mean16 0.010 / 0.015 vs 0.005). The single-orientation production profiles stay as they are.
  P18 COOH flag: ACCEPTED as an A metadata correction. On the 25, one compound changes flag (decanoic acid HB-DONOR-ACCEPTOR -> COOH); raw sigma rows
  unchanged; all registered invariants pass (Z0x predictions unchanged to 0; COSMO-SAC-dsp unchanged for every other compound); coverage identical; the
  historical acceptance statistic with the corrected flag is 0.1362 (limit 0.15; uncorrected 0.1493). Not yet applied to profiles_v2 or to any score:
  ZC_R3_COOH_FLAG stays 0 in production until a separate step regenerates or relabels the stored profiles and records it here.
  P19 final-precision trial: NOT accepted. Calibration on the 25 (both arms, fresh histories): all 25 pass the original confirmation in both arms (61
  evaluations each), profile changes tight vs control max 1.1e-4 (COSMO-SAC-dsp) and 2.1e-4 (Z0x), median vs UD 0.1494, but paired wall 2988 s vs 1311 s
  = 2.28 x (limit 1.50), so the calibration gate fails and, as registered, the six long chains were not run. No P19 profile is used.
  Observed and not yet explained (no test registered): every open profile examined carries a nonzero net first sigma moment (-0.013 to -0.029 for water,
  methanol and n-hexane; UD about -0.003), consistent with the raw C-PCM charge sums of about -0.03 e seen in the item diagnostics.

- Round 4 (Astra report docs/astra/round4/ZCOSMO_ROUND4_REPORT.md, received 2026-10-05). Victor chose "register all, run in order". The text below is
  Astra's proposed registration (docs/astra/round4/REGISTRATION_PROPOSED.md) appended unchanged, registered 2026-10-05 12:02 PDT in the same commit as its six
  patches (H4, P20, P21, P22, P23, REG4, applied unchanged to 33ebac0; new scripts only, production defaults unchanged) and before any round-4 output
  exists. Also decided here: the six-chain optimisation campaign is CLOSED (no new optimisation budget; 630 Berny-converged primary profiles plus six
  flagged S1/S2 exploratory profiles; the 4070 and PC2 jobs may keep running the existing protocol and a Berny-converged result would still replace a
  flagged profile). Execution notes, fixed here: generating geometries for the flagged profiles are MVLVMROFTA = cloud/s19/seeds partial.json at 8c03cc8
  (the S1 NEW checkpoint) and the other five = the base-arm pass-2 checkpoints of run 37190177507 (the S2 NEW checkpoints); P22 native single points run on
  GitHub Actions (pyscf 2.14.0); every UD-backed check runs on the Mac. Order: P20 prepare/verify/gates, P20 apply and COSMO-SAC-dsp rescore, P23
  accounting, P21 inventory and factorial, P22 native panel, P23 20-call control gate, then a measured small repair batch before any full repair run.

Round-4 proposed registration. This file is a proposal, not an assertion that it
has been appended to PREREGISTRATION.md or that any native calculation has run.
Commit the adopted text with its actual timestamp before new candidate outputs
are inspected. Reference: 33ebac0146ae2df4dd73fcf8a431cb6d7033554b.

P18 deployment implements the already accepted rule, registration 9d32e9e and
acceptance 613dd8f. It preserves all raw profile bytes after the first newline,
all metadata except the dispersion flag and explicit provenance, and the existing
630 primary plus five S2 plus one S1 partition. The current geometry-based NIST
classifier is authoritative. An unexpected change other than
HB-DONOR-ACCEPTOR to COOH stops deployment for investigation. All 636 selected
profiles and their actual generating geometries are hashed before deployment.
Verify the 25/2302 gate and exact finite coverage on the Mac. Verify Z0x and
COSMO-SAC 2010 prediction invariance to 1e-10 on the full existing IDAC row set;
verify unchanged-target rows on the one-compound COSMO-SAC-dsp check to 1e-10;
report the new UD compatibility statistic. Append the actual deployment receipt
and rerun affected open-profile COSMO-SAC-dsp scores under new output names.
No historical score is overwritten and no flagged geometry is promoted.

P21 is a descriptive mechanism audit, not a fitted or selected model. Select all
benchmark compounds with at least two structural OH groups or at least one
non-carbonyl ether oxygen, plus the fixed water, methanol, 1-butanol and n-nonane
controls, before examining their errors. Freeze the structural mapping, source
files and row identities in the commit. Inventory all available UD/open profiles
and geometries; missing data are reported without dropping score denominators.
For selected solvent rows, evaluate the eight fixed combinations of open/UD
area, volume and normalized 153-bin shape, with the solute kept open and the
existing dielectric and C6 tables unchanged. Each corner runs in a separate
process. Report the full-UD-solvent control and the exact Shapley identity, both
with numerical tolerance 1e-10 and identical finite coverage. These hybrid
profiles are diagnostic A substitutions and are never eligible for production.

The initial native geometry panel consists of ethylene, diethylene and
triethylene glycol at both their saved open and UD geometries, plus water,
methanol and n-nonane at their saved open geometries. Use fixed BP86/def2-TZVP,
the current auxiliary basis, XC grid 3/default pruning, C-PCM epsilon 1e9,
Lebedev 29, project radii and conv_tol 1e-9, without geometry optimization or
reorientation. Pin PySCF 2.14.0 and all other package versions for paired runs.
This is at most nine single points. Its diagnostics include geometric O-H...O
contacts, covalent HB tags, atom-owned surface area, raw and averaged charge
moments, pre-split areas and final OH/OT/NHB areas. A geometric contact is not a
measured H-bond energy. No choice is made on an experimental residual.

P22 tests raw surface charge; it does not authorize charge neutralization in
production. Validate the compact and diffuse neutral analytic Gaussian-sphere
sources at fixed Lebedev orders 29, 41 and 59. On water, diethylene glycol and
n-nonane in the native panel, recompute the PCM layer at fixed SCF density for
those three orders and for one radius scale of 1.10 at order 29. No such layer
is used in a score. For these molecules, integrate the same density and its
discrete capacitary potential on independent level-4 and level-5 volume grids.
Interpret the inside/outside decomposition only if level-5 total electron
count and reconstructed charge agree within 1e-5 e and the two partition
contributions change by less than 1e-4 e between levels. Failure is
inconclusive, not evidence for or against outlying charge. The union of project
vdW spheres is a stated diagnostic partition, not an exact SWIG boundary.

Two zero-charge projections, uniform sigma shift and the capacitary constrained
shift, are fixed A sensitivities. Compute both, never a fitted mixture of them,
for the nine native panel profiles and re-run the unchanged averaging/split.
Require each projected raw charge sum below 1e-10 e, report every subsequent
moment and tail change, and compare the same model query identities in fresh
processes with unchanged finite coverage. These projections are not an outlying
charge correction and cannot be adopted on the basis of a smaller benchmark
error. No output from this entry replaces a registered profile. A future
physical correction or conformer protocol needs a new registration after this
mechanism audit, with a fixed theoretical construction and a separate validation
panel before experimental scoring.

P23 first reports the existing P14 sidecar without changing a prediction.
Classify residuals at 1e-7 and sampled tangent margins at -1e-7. Keep missing
checks and coarse fallbacks as unresolved. Join records back to their exact
ordered pair and existing rounded temperature, preserving every requested row
and the original per-system majority aggregation. Preserve the old columns;
report quality-screen bounds with unknown votes assigned 0 and 1 separately,
and the explicit coverage of any endpoint-composition error. These are bounds
on the finite-grid quality screen, not a global phase-equilibrium certificate.

The opt-in P23 repair is an A numerical correction of the existing evaluator.
Freeze the complete unresolved-call list before repairing it; do not select
only favorable binaries. Preserve the model, pure-profile source and existing
2-K temperature rounding. Use nested 81/161/321 interior grids plus the fixed
logarithmic tails; try at most four sampled hull gaps and 4,000 new model calls
per pair-temperature. Use bounded least squares without clipping the equations,
residual <1e-7, sampled tangent margin >=-1e-7, gap width >1e-4, and agreement of
the last two grids' root sets within 5e-5 in composition. Exhaustion and failures
remain unknown. A strictly positive three-point nonconvexity witness supports
gap existence alone; it supplies no accepted endpoint compositions. No-gap
results remain explicitly finite-grid results. Record all outcomes, including
regressions, before producing a separately labelled scorecard. The portable
ideal/regular-solution and failure-injection tests must pass. For existing good
roots, a fixed control panel (first 20 sorted calls) must retain gap status,
meet the new residual/margin checks, and preserve endpoints within 1e-4; a
failure blocks adoption and is reported. Repairs are saved as a sidecar until
this gate and a full denominator audit pass. All earlier LLE scores remain.

The six-chain convergence campaign receives zero additional optimization budget
in this round. P19 remains rejected under its actual cost gate. S1/S2 status is
preserved as an exploratory endpoint of the present campaign, not a proof of
Berny convergence. A new optimization experiment requires a separate prospective
budget and evidence that addresses a specific remaining failure mechanism.

- Round 4 RESULTS (recorded 2026-10-05 16:10 PDT; registered 2026-10-05 12:02 PDT in b61301d; frozen P22 open panel and workflow in 3216fbe; Mac queue jobs
  337 to 347; P22 single points on GitHub Actions run 37367539367 (retry attempt) except n-nonane). Details in docs/astra/round4/RESULTS.md.
  P20 APPLIED (job 337). Bundle manifest sha256 e203da8ee623ce78ca89dfde4e46f3b0b72613fc2d01978303fd565be10bc4c5 over all 636 selected profiles (630 profiles_v2,
  five S2, one S1). 30 profiles change HB-DONOR-ACCEPTOR -> COOH (one flagged S2, OYHQOLUKZRVURQ); no other transition; raw bodies byte-identical. 25/2302
  gate: coverage identical, Z0x max change 0, COSMO-SAC-dsp max change 0.319 on changed targets, median vs UD 0.1362. Full IDAC (3252 rows): Z0x and COSMO-SAC
  2010 max |change| 0 with identical prediction hashes. Open-profile COSMO-SAC-dsp test IDAC without flagged chains (750 rows): 0.8009 -> 0.8001. Rollback copy
  kept; corrected COSMO-SAC-dsp predictions written to results/predictions_p18_dsp (new name; no historical output overwritten).
  P23 accounting (Z0x): all 6581 rows / 303 systems / 2255 calls, 554 unresolved rows, row gap-found bounds [0.761, 0.845], system [0.683, 0.795]; test
  2475 / 101 / 716, 103 unresolved, rows [0.848, 0.890], systems [0.752, 0.842]. Control gate (first 20 sorted good calls) PASSED. Measured batch of 20 test
  calls: 13 s. Full repair of the frozen list of 280 unresolved calls: 127 s, 136 refined roots, 144 gap witnesses only, 0 unresolved. With repairs, gap-found
  is exact and equals the old upper bound: all rows 0.8453, systems 0.7954; test rows 0.8897, systems 0.8416. Composition MAE on checked detections: all
  0.1647 (5278 rows), test 0.1799 (2142). The repaired accounting is a separately labelled sidecar; all earlier LLE scores remain.
  P21: inventory of 96 keys; no UD .cosmo geometries exist (validation_data.zip holds only a CSV). Factorial on 332 rows / 14 solvents, all corners finite;
  corner 000 reproduces the stored open prediction to 8e-11, corner 111 equals the full UD solvent exactly, Shapley identity 1e-10. MAE 000 1.311, UD area only
  1.317, UD volume only 1.305, UD shape only 0.845, UD solvent 0.836. Area and volume Shapley terms < 0.05 for every solvent; shape terms DEG +1.372 (MAE
  1.740 -> 0.371), TEG +1.497, EG +2.550, tetraethylene glycol +0.465, water +1.057 (MAE 1.546 -> 2.073, worse), glycerol +0.037, propylene glycol -0.861.
  P22: sphere-native reproduces the analytic Gaussian-sphere values (t = 1.5: continuum -0.033895 e; Lebedev 29/41/59 -0.034250/-0.034077/-0.033984). Open
  panel raw charge sums (e): EG -0.02258, methanol -0.01864, TEG -0.03543, DEG -0.03041 (41: -0.03030, 59: -0.03026, radius x1.10: -0.01608), water -0.01241
  (-0.01243, -0.01245, -0.00587), n-nonane -0.04481 (-0.04433, -0.04414, -0.02525). Quadrature gates for DEG, water and nonane all fail as registered, so the
  inside/outside partition is inconclusive and not interpreted. No registered O-H...O contact in EG/DEG/TEG. Zero-charge projections: sums < 1e-16, tail and
  OH/OT/NHB area changes <= 0.3 A2; on 859 IDAC rows with identical finite masks, Z0x mean/max |change| 0.35/1.26 (MAE 1.783 -> 1.668), COSMO-SAC-dsp
  0.17/0.57 (1.184 -> 1.216); DEG as solvent Z0x 1.740 -> 1.640. Fresh native profiles reproduce stored open ones to 3e-5 in ln gamma. Nothing adopted.
  Deviations: P22 UD-geometry arm not run (geometries unavailable); first dispatch never acquired a hosted runner; the nonane case was killed on the runner
  (exit 143, peak memory 20 GB measured on the Mac) and the identical command ran on the Mac (job 346); job 347 overlapped job 346's quadrature step, after
  the nonane .sigma and projection files were written. Chain campaign stays closed; profiles_v2 630/636.

- Long-chain diagnosis and stop (2026-10-05 ~21:10 PDT, Victor's decision "stop all chain runs"). Zero-QC read of the six pickled Berny states
  (Mac job 352, pyberny 0.7.0, 4070 checkpoints at cycles 160-299 of their latest 300-step passes): all six are force-converged far below Berny's
  limits (internal gradient RMS 3.8e-6 to 1.17e-5 vs 1.5e-4; max 1.4e-5 to 5.1e-5 vs 4.5e-4) but every step is a minimization on the trust sphere,
  which Berny's predicate counts as not converged. Trust radii have collapsed to 2.8e-4 to 2.9e-3 (L2 over 275-357 internal coordinates, i.e. about
  1e-4 per coordinate) because predicted energy changes (5.8e-8 to 3.5e-7 Eh) are the size of the observed energy noise (|E(previous)-E(best)|
  3.5e-8 to 3.7e-7 Eh), so Fletcher's ratio is noise-dominated. The learned Hessians have soft modes (lowest eigenvalue 2.2e-4 to 2.8e-3), so the
  unconstrained RFO step is large (norm 0.038 to 0.27; RMS 2.0e-3 to 1.6e-2, above the 1.2e-3 step limit by itself). A fresh model-Hessian
  optimizer at the same points would also fail the step-maximum test (2.6e-3 to 8.4e-3 vs 1.8e-3). Conclusion: these flexible chains cannot satisfy
  Berny's step/on-sphere predicate at the present SCF/grid/PCM energy noise; more cycles cannot finish them. A separate operational defect was found:
  three lc_driver2 loops were alive on the 4070 and two processes optimized FLIACVVOZYBSBS simultaneously on the same checkpoint files (a pgrep race).
  All long-chain drivers on the 4070 were stopped (job 353: three driver loops and both duplicate processes; WSL and Windows untouched); PC2 had no
  chain process running. Checkpoints are kept. profiles_v2 stays 630/636 with the six flagged S1/S2
  exploratory profiles; nothing is reclassified by this diagnosis.

- Round 5 (Astra report docs/astra/round5/ZCOSMO_ROUND5_REPORT.md, received 2026-10-05). Victor chose "register all, run in order". The six patches
  (H5, P24, P25, P26, P27, REG5) are applied unchanged to 69b4911 in the same commit as this text, before any round-5 output exists. Portable self-test
  (r5_selftest.py, container run before registration) reproduces the report's values exactly (alignment 7.8e-16 A, subdivision 1.7e-18, HB bin
  total 4.4e-16, gauge kernel 2.2e-16 / residual 8.9e-16, denominator checks passed). The P27 change to src/zcosmo/evaluate.py is the archived P14
  audit hook (off unless ZC_LLE_AUDIT_DIR is set; P14 showed identical predictions with it on and off). Execution notes fixed here: every UD-backed
  step (P27, P24, P25 descriptors, P26 affinity gate) runs on the Mac; P25 native single points and P26 optimizations run on free four-core workers
  (GitHub Actions matrix, or the Mac if a runner is unavailable, recorded as a venue deviation) with pyscf 2.14.0 and pyberny 0.7.0. Order: P27,
  P24, P25 (plan, descriptors, native matrix, collect), then the P26 probe (at most 40 optimizations) and its continuation record. The text below is
  Astra's proposed registration appended unchanged.

This is proposed text, not evidence of registration. Append adopted text to
PREREGISTRATION.md with the actual commit timestamp before inspecting new
native outputs or scores. Reference code is main at
69b49116c2ae7574d7ae471f0a4ed7ba33d0db8b plus the archived R5 patches.
The experiment is motivated by already observed glycol, water and charge
sensitivities. It is not a fresh experimental holdout. Nothing is fitted to
ThermoML, and no recipe is selected by experimental error. P20 remains applied;
P23's accepted accounting remains; P15/P17/P19 rejections and S1/S2 labels stand.
The six-chain completion campaign remains closed.

P24 is an E component-accounting diagnostic of the unchanged Z0x implementation,
plus explicitly A electrostatic/HB-off interventions. Reproduce the frozen P22
859-row panel in separate processes for native, area-zero and capacitary-zero
profiles, with a complete unchanged open background. Also substitute only the
normalized UD shape, retaining native area and volume, for each of the six
fixed P22 molecules in separate arms. Do not pass experimental response values
to these workers. Decompose the actual one-sided h=1e-4 endpoint expression
into combinatorial, residual and London terms. Require total parity <1e-9 and
invariance to H2O/COOH flag relabeling <1e-10 in Z0x. Report the frozen-c exact
endpoint and h=1e-5/1e-6 controls; these do not replace the production stencil.
Use all four ES/HB on/off kernels and symmetric Shapley attribution, retaining
the interaction and finite masks. This is a model sensitivity decomposition,
not separately measurable ES/HB free energies. It does not adopt a neutrality
convention. All baseline and candidate coverage differences are failures of
comparability, not permission to discard unfavorable queries.

P25 freezes the twelve structures in r5_common.PANEL before new computation:
water, methanol, ethylene/diethylene/triethylene/tetraethylene glycol, glycerol,
propylene glycol, 2-methoxyethanol, 1,2-dimethoxyethane, tetrahydrofuran and
n-nonane. Resolve by stereo-aware canonical SMILES; ambiguous matches must
resolve to the exact structure-derived InChIKey or fail. These are structural
homologues and controls, not a claim that their historical errors were unseen.
Freeze saved geometry bytes; never invent the missing UD conformer. A separate
validation panel is the first eight SHA256('R5-validation-v1|'+InChIKey)-ordered
neutral, closed-shell, single-component covalent CHO structures with at most 13 heavy atoms, at least two rotatable bonds,
and either two OH groups or an ether, excluding the twelve and the historical
25. Insufficient eligible members or missing generating geometries abort the
plan. Freeze the manifest and package versions before native outputs.

On each of the twelve saved geometries, run three fixed single-point methods:
BP86/def2-TZVP/SWIG, BP86/def2-SVP/SWIG and BP86/def2-TZVP/ISWIG. All use the
project radii, C-PCM eps=1e9, Lebedev order 29, grid level 3/default pruning,
conv_tol=1e-9 and PySCF 2.14.0. The latter two are A diagnostic arms, not claims
of reproducing DMol3. Record the resolved auxiliary basis. At most 36 single
points, at most one hour per call. Reuse previous segments only on matching
geometry and method hashes. No density quadrature or new rotation recipe is
part of this trial.

For each saved segment table, retain raw charges and owner areas, the Hsieh
averaged sigmas, pre-HB bins and post-HB bins. Independently implement the
existing Hsieh formula and require max sigma difference <1e-10 e/A^2 and
binwise pre/post-HB total agreement <1e-8 A^2. Diagnose the segment-size effect
by the exact compressed equivalent of four coincident A/4,q/4 patches, and
by its point-patch limit. Both are A diagnostic sensitivities, not physical
remeshing or approved new averaging methods. The raw table is unchanged;
no out-of-range sigma is clipped into a usable profile. The existing radius,
decay and HB parameters are not adjusted. Compare stage distributions and
stored UD final shapes without using experimental responses. Missing UD
geometry prevents unique historical attribution and is reported as such.

P26 is conditional. Generate proposals with two fixed RDKit ETKDGv3 pools,
32 embeddings per pool, seeds 20261005 and 20261006, one thread, maxIterations
1000, pruning disabled. Pin the RDKit version recorded in the manifest.
MMFF94s, at most 500 iterations, supplies proposals only. A failed embedding or
MMFF member blocks that pool; there is no alternative seed or force-field
fallback. Select the lowest-MMFF proposal followed by three greedy farthest
proposals, using fixed-atom-order properly aligned heavy-atom-plus-donor-H RMSD.
RDKit/force-field priors are empirical proposal machinery, not fitted benchmark
model parameters. Each selected start is optimized by the unchanged registered
BP86/def2-SVP/DF/grid-2/C-PCM-17 CPU Berny path, at most 80 gradient evaluations
and one hour per proposal including the TZVP profile. PySCF=2.14.0 and
pyberny=0.7.0. Fresh histories; no P15 noise override, no P19 tight stage,
no optimizer pickle, no altered convergence predicate. All members must pass
Berny's actual convergence test and preserve covalent connectivity. Failed or
censored members are not omitted. The TZVP profile uses the accepted P18 flag.
Keep the converged orientation. O-H...O contacts use the already registered
geometric definition and are reported, never filtered or rewarded.

First run ranks 0 and 1 in each pool for the ten non-rigid structural panel
members, at most 40 optimizations. Water and methanol are rigid controls.
The full conformer protocol is authorized only by a prospective continuation
record when this probe contains reproducible distinct low-energy structures:
at least one pair within 3 kcal/mol of the sampled minimum, RMSD >=0.2 A,
and normalized-profile L1 >=0.02; report pool agreement and the other controls
without selecting a molecule by experimental error. This is justification for
further sampling, not proof that a conformer explains UD's historical profile.
Cross both pool winners on the same additional single-point methods when
separating method/conformer interactions, at most 40 extra single points.

If continued, complete all four proposals in each pool, reusing the already
computed members, and run the same full protocol on all eight separately
selected validation molecules. Select by lowest TZVP conductor electronic
energy alone, ties within 1e-7 Eh by frozen proposal rank. Do not assign
Boltzmann weights from embedding frequency or electronic energy, and do not
claim a global minimum or a temperature-dependent conformer ensemble.
The theoretical reproducibility gate requires all full pools to complete;
per molecule, independent pool minima must agree within 1e-4 Eh, aligned
heavy-plus-donor-H RMSD <=0.15 A, and normalized 153-bin L1 <=0.02. The selected
energy must not exceed the saved-geometry TZVP reference by more than 1e-4 Eh.
All eight validation members must pass. On fixed water/methanol/nonane/
dimethoxyethane probes at 250, 298.15 and 400 K in both solute/solvent roles
(192 queries), both models must be finite in both pools and maximum pool
prediction difference must be <0.02 for Z0x and COSMO-SAC-dsp. The full separate
validation budget is 64 worker-hours on four-core workers, with the per-member
80-evaluation/one-hour cap. Do not extend a censored member after reading it.

A pass establishes only computational reproducibility of a sampled-conformer
protocol. It permits one separately authorized exploratory experimental report
using the already frozen selections, not promotion of the 630 primary profiles.
The exact baseline profiles and all S1/S2 files remain read-only. Any future
conformer arm has its own directory and identity. A new claim of improved
experimental accuracy must report the fixed full comparison and paired CIs,
including water and the branched controls, whichever direction they move.
No best-error choice among conformers or recipes is allowed.

P27 regenerates Z0x, COSMO-SAC 2010 and COSMO-SAC-dsp in three separate profile
arms: UD, the 630 primary open profiles, and the 636 open profiles including
S1/S2. Every model/arm runs in a fresh process. Use the unchanged evaluate
formulas on the historical has_sigma universe for each table; attach immutable
row identities and freeze every source file/profile hash. Open630 marks the six
flagged compounds excluded by design, without falling back to UD. Report
standalone coverage and pairwise UD/open common subsets, never a hidden
intersection across all nine arms. All raw counts are written from the actual
frozen CSVs. Expanded non-UD coverage is a different table.

For LLE, reuse the previously tested P14 hook without changing its predictions,
then the accepted P23 thresholds, grids, 4000-call budget and old 2-K rounding.
For each arm first require the first 20 sorted good-call controls to retain
checked roots within 1e-4 of the legacy endpoints. Failure or fewer than 20
controls blocks that arm and is reported. Retain roots, gap witnesses, finite-grid
no-gap results and unresolved results as different statuses. Never give a
witness an endpoint error or turn an unknown into miscibility. Endpoint MAE
has its own explicit denominator. Report operational detection bounds and
system-majority bounds, not global phase-equilibrium certificates. This extends
accepted numerical accounting to additional profile/model arms; it does not
assume that UD repairs validate open-profile endpoints.

IDAC uses absolute ln-gamma errors and solvent-ranking rules already in metrics.
VLE uses the same psat source and homogeneous-liquid exclusion, with its own
coverage. HE uses the same 0.5 K central difference and sign threshold. System
bootstrap uses 1000 resamples, seed 7 reset per statistic/comparison; this is the
same estimator with explicitly fixed draws, not a promise of bitwise identity
to older CIs generated by the global RNG stream. Keep historical scorecards,
including 0.800/762 and 0.839/828, unchanged. Regenerated VLE/HE values are not
reported until the actual files exist. The reused experimental data are not
represented as a fresh holdout. Save all outputs outside historical results.

- Round 5 RESULTS (recorded 2026-10-06 ~02:30 PDT; registered 2026-10-05 22:27 PDT in e126d31; P25 plan frozen 5eeb9eb; P26 proposals frozen 9bbe83e; Mac
  jobs 355-362; P25 native on Actions run 37423042495; P26 probe on Actions run 37426006692). Details and data in docs/astra/round5/RESULTS.md and data/.
  P27: all nine arms complete, all LLE 20-call control gates passed. Test split standalone: Z0x IDAC UD 0.839 (828) / open630 0.942 (816) / open636 0.977
  (828); paired on 816 rows UD 0.804 [0.687, 0.933] vs open630 0.942 [0.822, 1.075]. VLE AAD% UD 16.13 / open630 16.41; HE MAE UD 619 / open630 699
  J/mol (sign correct 0.838 / 0.799); LLE gap-found rows UD 0.890 / open630 0.883. COSMO-SAC 2010 IDAC 0.871 / 0.987; COSMO-SAC-dsp 0.679 (762) / 0.800
  (750), with 177 unresolved dsp LLE rows in each arm. Historical values reproduced exactly.
  P24: component identity holds; combinatorial changes <= 3e-13 and London exactly 0 in every intervention, so every effect is in the residual term.
  Charge projections: mean residual change +0.325 / +0.322 (ES +0.12, HB +0.21); water as solvent +0.57 (HB +0.40). UD-shape-only, solvent rows:
  EG +2.35 (ES +1.82, HB +0.53), DEG +1.37 (ES +1.05, HB +0.33), TEG +1.14 (ES +0.74, HB +0.40), water +1.02 (ES +0.74, HB +0.28), methanol +0.21,
  nonane -0.05. Endpoint-stencil controls differ from production by <= 3e-3 except the water UD-shape arm (0.26).
  P25: 36/36 single points; Hsieh parity <= 3e-17; binwise HB conservation holds. Averaging recipes change the tail <= 0.2 A2, ISWIG vs SWIG <= 0.1 A2,
  SVP lowers it 2-3 A2 (away from UD). Raw-charge tail already carries the glycol deficit. TZVP/SWIG vs UD tail: EG 23.0/33.0, DEG 27.7/38.0, TEG
  27.9/42.3, tetraEG 41.8/46.8, water 26.5/27.7, methanol 15.7/17.9, glycerol 37.3/35.0, PG 30.0/25.9. Deviation: descriptors ran on the panel only
  (validation member QCDWFXQBSFUVSP has no UD profile).
  P26 probe: 39/40 ran; 36 stationary samples; 3 censored at 80 evaluations (nonane, TEG, dimethoxyethane; same flat-surface Berny behaviour as the
  chains); one tetraEG proposal never ran because a censored member stopped its slot (check=True). Registered selection on the six complete members:
  continuation trigger met in five (EG, DEG, glycerol, PG, THF; L1 up to 0.38). Lowest-conductor-energy selection moves tails further below UD (DEG 23.7,
  EG 22.8, glycerol 28.9, PG 22.2, methoxyethanol 13.7 A2). Decision (Victor, 2026-10-06): full P26 not continued; incomplete members block acceptance;
  nothing scored or adopted.

- Round 6 (Astra report docs/astra/round6/ZCOSMO_ROUND6_REPORT.md, received 2026-10-06). Victor chose "register all, run in order". The six patches
  (H6, P28, P29, P30, P31, REG6) are applied unchanged to 43213a5 in the same commit as this text, before any round-6 output exists. Verified before
  registration: both portable suites pass in the container with the report's values (endpoint reference 1.29e-10, finite-basin singleton 3.3e-16,
  derivative 2.9e-10, four-arm integration gate, missing-row rejection); r6_headline.py reproduces the archived P27 matched comparisons exactly; Z0x
  infinite dilution uses the one-sided h=1e-4 stencil and the frozen Mixture includes the London term; pinned PySCF 2.14.0 pyscf/grad/rks.py defaults
  grid_response to False. The z0x.py change is opt-in (ZC_R6_ENDPOINT=1, default off). Execution notes fixed here: P31, P28 (prepare, run, timing, and
  the corrected IDAC score only after an acceptance record of the exact numerical gate is committed) and the P29 inventory run on the Mac; P30 native
  stage 1 (five cases) and, only if its fixed gate passes, stage 2 run on GitHub Actions with pyscf 2.14.0, pyberny 0.7.0 and rdkit 2026.03.6 (Mac as
  a recorded venue deviation if a runner is unavailable); the P30 affinity stability check runs on the Mac. Order: P31, P28, P29 inventory, P30.
  The text below is Astra's proposed registration appended unchanged.

adopted. Append accepted text with the actual commit timestamp before a new
candidate output is interpreted or used. Reference main is
43213a5e61f591a19b4d3352a95315a62ee2aeb8 plus the six archived R6 patches.
The hypotheses are motivated by the already observed R5 results. No new result
is represented as an experimental holdout, and no ThermoML response selects
any numerical constant, geometry, conformer, or population.

The six stopped chains remain excluded from new native jobs. Their files keep
S1/S2 status, primary profiles_v2 remains 630/636, and P26's full protocol is
not resumed. P15/P17/P19 rejections stand. P20's accepted metadata correction
and P23/P27 reporting remain in place. No R6 helper writes a production profile
or silently changes a historical scorecard.

P28 is a narrowly scoped A numerical correction of the Z0x infinite-dilution
endpoint. For a pure solvent, evaluate the unchanged fixed-coefficient Mixture
at the pure composition, with A_ES equal to the pure solvent's dielectric
coefficient. The chain-rule term vanishes because the frozen-coefficient
excess Gibbs energy is identically zero at either pure endpoint for every
coefficient. Construct this Mixture without the rounded-c lookup. The switch
ZC_R6_ENDPOINT=1 affects lngamma_inf and lngamma at exactly x1=0 or x1=1 only.
Its default is off. Every finite interior composition, including the existing
near-endpoint finite-difference strip, stays unchanged. This entry does not
certify that strip, fix the finite-composition model, or authorize a correction
in another Z0 variant. All profile bytes, dielectric and dispersion tables,
functional forms, and fitted/theoretical constants remain unchanged.

Freeze the historical has_sigma IDAC universe from the current P27 input CSVs,
including every row identity and split label. Run UD, open630, open636, and
one declared stress overlay in separate processes. The stress overlay uses
UD's normalized water profile with the native open area and volume; all other
profiles are open636. No experimental response is sent to numerical workers.
Open630 excludes exactly rows involving S1/S2 keys, without UD fallback.
The old and candidate endpoints are evaluated independently even when the old
one fails. Require identical finite coverage in every arm; matched nonfinite
rows remain in the requested denominator. Every old finite row must be checked.

The independent reference solves the same segment equations in logarithms,
using a separate residual/Jacobian evaluation and nonlinear polish. Require
maximum log-equation residual <=5e-12, maximum candidate-reference difference
<1e-8 in ln gamma, component-reversal agreement <1e-8, public endpoint API
agreement <1e-10, and pure-solvent ln gamma <1e-9. Keep every positive profile
bin; do not threshold tiny support. A malformed, missing, or extra result row
fails the gate. Report three-point one-sided controls at h=1e-4, 1e-5, 1e-6,
1e-7 and 1e-8 with fresh coefficient evaluation. These controls diagnose
truncation/cancellation; no h is chosen by experimental error. FD rows lacking
agreement within 1e-5 are explicitly inconclusive and do not replace the
reference equation gate. The proof and independently checked endpoint solve,
not a supposedly optimal tiny h, define the candidate.

Report counts and magnitudes of changes above 1e-3, 1e-2, 0.05 and 0.1 on all
and test rows, with separate solute/solvent summaries. Time three fresh-process
repetitions per arm and flag, alternating order; do not time the expensive
reference/FD checks as production. No measured speed-up is assumed. A numerical
pass permits recording acceptance of this exact gate hash before running the
separate score command. That command reports old and corrected IDAC results
on identical rows, with 1000 system bootstrap draws and seed 7. The water stress
arm is a diagnostic, never a deployable profile set. P27's historical outputs
are retained. A worse experimental score does not reverse a proven numerical
correction. Any finite-composition extension needs its own gate and accounting.

P29 first inventories every frozen P26 probe proposal by input hash, retaining
censored, failed and never-run members. Duplicate runs cannot be cherry-picked.
Known-conformer tail ranges and normalized-L1 diameters describe the supplied
finite set only, not unsampled basins. No electronic-energy population or
embedding-frequency multiplicity is assigned to incomplete pools.

The theory definition is a phase-dependent finite-basin ensemble, not a chosen
extended geometry and not a rule excluding intramolecular hydrogen bonds.
For each distinct basin, retain the conductor electronic energy, the nuclear
partition contribution, and audited symmetry/multiplicity. The nuclear term
includes ZPE and finite-temperature vibrations or an explicitly integrated
hindered-rotor/basin contribution, with rotational terms on a common reference.
The same molecular translational standard state cancels between its conformers.
An imaginary or unconverged soft mode must not be replaced by its absolute
value or an empirical frequency floor. Intramolecular H-bonds already affect
the electronic energy and exposure; no extra penalty or reward is added.

The provided reference-ensemble helper can compute a harmonic plus classical
rigid-rotor diagnostic only from complete audited basin inputs. Require the
P30 force, Hessian, and two-step thermal checks for every supplied basin and
an explicit basin/symmetry audit identifier. Distinct minima must be deduplicated
with atom/symmetry correspondence, not by embedding frequency. Rotational
symmetry number and additional basin degeneracy are different inputs and cannot
count the same symmetry twice. Harmonic numerical stability is not proof of an
accurate low-barrier torsional partition. This helper produces a labelled finite
conductor-reference ensemble only; its averaged profile is not a liquid chemical
potential and its weights are not automatically liquid populations.

The prospective finite-basin Z0x extension is frozen in scripts/r6_phase.py.
It uses the unchanged combinatorial and segment equations over basin species,
volume-weighted chemical permittivities, and the symmetric extension of the
existing London contact exchange energy. All basins of one chemical species
retain the same frozen chemical dielectric, C6, and polarizability values.
Conductor electronic plus nuclear free energies are augmented with the model's
absolute pure-conformer segment and London self-contact standards before
adding the pure-subtracted excess mixture functional. Thus pure-liquid and
infinite-dilution populations are minimized separately under one scalar free
energy; conductor solvation is not added twice. This is a new A closure, not
claimed to be uniquely implied by a final sigma histogram or by COSMO-RS.

The finite-state pilot is restricted to two chemical species, at most four
audited basins each, and T=250, 298.15 and 400 K. A catalog with more
than four distinct relevant basins is outside this pilot; do not drop basins
merely to meet the software cap. Use the fixed uniform and
vertex-biased starts, a shared 2000 objective-call budget per equilibrium
problem, and the fixed stationarity checks in the code. A failed multistart
blocks the result; a lower stationary value is not a global certificate.
The one-basin-per-species limit must reproduce P28 to <1e-8; analytic free-energy
derivatives must agree with independent finite differences to <1e-7 in the
portable test; energy-zero and population-normalization checks must pass.

No new quantum basin survey is authorized by P29 in R6. The command examples
consume only explicitly supplied and audited basin partitions. The present
incomplete P26 files do not satisfy that requirement. A later physical ensemble
validation requires a separate prospective sampling budget on all eight frozen
R5 validation molecules. Independent complete basin catalogs must give chemical
free energies within 0.05 kcal/mol, normalized average profiles within 0.02 L1,
and both-role probe ln gamma within 0.02 at the three fixed temperatures, with
identical finite coverage. The four probes remain water, methanol, nonane and
1,2-dimethoxyethane. Thermal partition error must also be checked independently
of discovery-pool agreement. No R6 ensemble output is authorized for ThermoML
scoring or for replacing the 630 primary profiles, and P26 remains unaccepted.

P30 tests a specific possible source of energy/gradient inconsistency before
attempting any new optimizer. Pin pyscf=2.14.0, pyberny=0.7.0 and the R5 direction
construction's RDKit=2026.03.6. Freeze five geometries: saved R5 methanol and
ethylene glycol, plus the last archived geometry of exactly these P26 censored
members: nonane seed 20261006 rank 1, TEG seed 20261006 rank 1, and
1,2-dimethoxyethane seed 20261005 rank 1. Their recorded 80-evaluation outcomes
and proposal hashes must match. Do not optimize these inputs or restart any of
the six stopped chains. The never-run tetraEG proposal is not quietly added.

Per geometry, compare the original energy/gradient with tighter SCF
conv_tol=1e-11 and conv_tol_grad=1e-7 at the same BP86/def2-SVP, DF, grid level 2,
default pruning, project radii, C-PCM eps=1e9 and Lebedev 17. At the tight center
compute gradients with grid_response=False and True, retaining auxiliary-basis
and PCM responses. Compute centered energy differences at 0.003 and 0.006 Bohr
along four deterministic internal directions. The first directions are heavy
single-bond rotations, with the fixed projected random fallback in the helper.
This costs at most 18 SCF evaluations and three gradients per case.

The two-step derivative uncertainty indicator must be <1e-7 Eh/Bohr and maximum
full-response gradient discrepancy <2e-7 on all sampled directions. Material
omitted response is reported only when the tight-no-response discrepancy is
>1e-6 and >5 times the larger of the full-response discrepancy and 1e-10.
This is a directional test, not a proof everywhere or a claim that omitted grid
response caused the observed stalls. Maximum budget is one four-core worker-hour
per case, with an internal 3400-second deadline. Inconclusive results stop the
native escalation. Do not change a threshold after reading the outputs.

Only if all five fixed consistency cases pass, the optional mode/stability
stage is allowed on the same five geometries. Use two finite-difference Cartesian
Hessians from tight full-response gradients at steps 0.003 and 0.006 Bohr. Project
mass-weighted translations and rotations explicitly, and record Hessian asymmetry,
step dependence and every signed frequency. Per case the count is 12N+2 gradients,
never above 360. Significant negative modes below -20 cm^-1 or failure of the
new diagnostic force targets (max 5e-5 and RMS 1.5e-5 Eh/Bohr) fail stationarity.
This new diagnostic definition is NOT an equivalence to Berny's internal
coordinate, step, or on-sphere predicate and is never written as Berny-converged.

For passing stationary candidates, evaluate the center and both signs of 0.005
and 0.010 Angstrom maximum-atom displacements along the six softest projected
modes, at most 25 registered TZVP profiles per case. Keep orientation, all profile
settings and P18 metadata fixed. For a harmonic partition diagnostic all
vibrational frequencies must be positive and the two Hessian steps must change
F_vib by <0.05 kcal/mol at every fixed temperature. Otherwise the thermal result
is unavailable and a hindered-rotor/basin integration would need a separately
registered budget. There is no silent soft-frequency regularization.

The optional stage has a two-worker-hour cap per case, including its stress
profiles, with an internal 7000-second deadline. Across both native stages the
absolute budget is 15 four-core worker-hours, with no retries, no optimization,
and no production relabel. On the Mac, compare stress profiles against their
own center in separate processes against the four fixed probes, in both roles
at 250, 298.15 and 400 K using P28. Require identical finite coverage and maximum
sampled change in ln gamma <0.01. This is an observed finite-stress envelope,
not a certified bound on every geometry in a ball or on every thermal basin.
Even a pass authorizes no new S1/S2 acceptance route. A future convergence rule
for production needs its own independent validation and registration.

The job runner locks each output location before starting, terminates the whole
process group on its fixed deadline, records all return codes, and continues
independent jobs after a failure. It never automatically deletes a stale lock,
retries a member, or dispatches a cloud workflow. Censoring must not hide a
never-run member as it did in one R5 slot.

P31 re-renders the archived P27 matched test comparisons, with their original
confidence intervals and row identities. No prediction is regenerated and no
new bootstrap is run. Report IDAC and HE deficits on matched rows; describe the
VLE increase with its paired interval, which includes zero. Keep LLE checked
roots, gap witnesses, sampled no-gap and unresolved statuses distinct. Detection
rates on the positive LLE table are not balanced accuracy. All headline numbers
are explicitly before P28. Rewording a headline does not alter the historical
score, and open636 remains separately flagged exploratory coverage.

- Round 6 RESULTS (recorded 2026-10-06 ~07:00 PDT; registered 2026-10-06 04:49 PDT in 5926ba1; P28 acceptance 64c4a3b; Mac jobs 364-370; P30 stage 1
  on Actions run 37463154483). Details and data in docs/astra/round6/RESULTS.md and data/.
  P31: headline reproduces the P27 matched comparisons exactly (IDAC 816 rows 0.8040 vs 0.9423, CI [0.0506, 0.2379]; VLE CI [-0.75, 2.10]; HE CI
  [50.9, 108.8] J/mol).
  P28 ACCEPTED (numerical gate, all four arms): max reference error 2.73e-9; identical finite coverage; prevalence |exact-legacy| > 0.1 on 21 (UD) / 27
  (open630) all-split rows and 0 test rows; max change 0.84 (UD) / 1.14 (open630), concentrated in YNQLUTRBYVCPMQ, IMNFDUFMRHMDMM, TVMXDCGIABBOFY;
  3.06-3.25x faster. Acceptance recorded (gate sha256 2f3df2e2e1c333f4936e9effc7c8ef160f3b01808dd48ea0072eb83aff0d4dbc) before scoring. Corrected test
  IDAC MAE UD 0.8394 -> 0.8397, open630 0.9423 -> 0.9427; all split +0.0019 / +0.0023. Historical scorecards unchanged.
  P29 inventory: 6 complete, 4 incomplete members; no populations computed. Sampled tail envelopes lie below UD for EG (max 31.4 vs 33.0), DEG (34.8 vs
  38.0), TEG (32.7 vs 42.3), tetraEG (34.3 vs 46.8), 2-methoxyethanol (20.5 vs 23.9), DME (10.3 vs 14.4); no positive weighting of these samples can
  reproduce UD.
  P30 stage 1: all five cases diagnostic_complete; full_response_consistent false in all five (registered gate 2e-7 Eh/Bohr with FD uncertainty
  < 1e-7; measured FD uncertainty 6e-7 to 8e-6), so stage 2 was not run. Observed: in the P26-censored nonane/TEG/DME the original gradient errs vs
  Richardson FD by up to 7.4e-5 / 1.1e-4 / 8.8e-5 Eh/Bohr (often opposite sign on torsions), the full-response gradient by 9.0e-6 / 1.5e-5 / 3.9e-5;
  methanol and EG show no such difference; tight SCF changes gradients <= 7.5e-6. Interpretation (not accepted): the omitted grid response dominates
  the optimizer's gradient at these flat geometries.

- Round 7 (Astra report docs/astra/round7/ZCOSMO_ROUND7_REPORT.md, received 2026-10-06). Victor chose "register all, run in order". The six patches
  (H7, P32, P33, P34, P35, REG7) are applied unchanged to ddf22b1 in the same commit as this text, before any round-7 start geometry, plan or output
  exists. Verified before registration: all patches apply; r7_selftest.py passes in the container (FD reference error 7.0e-12, tri-state gate,
  chain-escalation negative controls, rigid projection 7.8e-16, historical occurrence/mask checks, worker lock/deadline); the historical 25-target /
  2,302-occurrence manifest is cloud/r3/orientation/queries.csv (target column "key", accepted by r7_common.historical_queries). Execution notes fixed
  here: plans are frozen on the Mac and committed under cloud/r7 on main (not a separate branch); the six designated stopped checkpoints are the final
  *.partial.json files in the 4070 output folder after the 2026-10-05 stop (job 353), copied once into the frozen chain plan; native cases run through
  .github/workflows/r7_review.yml on GitHub Actions; every UD-backed gate runs on the Mac. Order: P35 (this record), P32 calibration, P33 referee and
  P34 screen (independent of P32), P32 pilot only after the calibration gate passes, and the chain stage only after the decide permit is positive AND a
  separate authorization from Victor is committed.

Append adopted text with the actual timestamp and commit identifier before generating new R7 starts or interpreting candidate output. Source baseline is ddf22b19f9e1750308bd11572786b44d407a80f9 plus the archived R7 patches. The R6 P30 gate remains failed and its stage 2 remains unrun. The following is a new experiment motivated by known data, not a fresh experimental holdout. P15/P17/P19 decisions stand. P20 and P28 remain accepted within their actual scopes. Nothing is fitted to ThermoML.

P32 changes only the optimizer's XC grid response from False to True on the existing BP86/def2-SVP density-fitted grid-level-2 C-PCM conductor path, epsilon 1e9, Lebedev order 17, project radii, production SCF conv_tol 1e-8 and default orbital-gradient tolerance. Keep density-grid pruning unchanged. Keep auxiliary-basis and solvent gradients. Pin PySCF 2.14.0 and pyberny 0.7.0. Supply a configured Gradients object to berny_solver.kernel. Both arms use fresh optimizer histories and the unchanged gradientmax 4.5e-4, gradientrms 1.5e-4, stepmax 1.8e-3 and steprms 1.2e-3, including Berny's unchanged on-sphere predicate. No optimizer pickle, trust override, tighter SCF, finer grid, gradient-only stop, or original-force confirmation stage is added. The comparison is between gradients, not two convergence definitions.

Freeze the exact historical 25 targets and 2302 query occurrences from their archived query manifest. validation_set.csv alone contains 26 candidates and must not redefine this set. Freeze one seed-7 GFN2-xTB start per calibration target before either arm. Run both arms sequentially on the same four-core worker, alternating order by SHA256(key) parity. Each calibration arm has 100 gradient evaluations and 1800 seconds including its TZVP profile. Record all failures and censoring. The 25-target numerical compatibility gate requires both arms to pass the original Berny predicate for all 25; identical finite coverage; maximum COSMO-SAC-dsp change below 0.01; and median absolute COSMO-SAC-dsp difference from UD below 0.15 on the frozen occurrences. Expect the historical 2271 finite dsp and 2302 finite Z0x occurrences; a count or mask mismatch blocks the gate. Use separate processes for each target/profile set. P18 flags and P28 exact endpoints are enabled identically in both arms. Report raw and normalized profile differences without reinterpreting E tolerances.

Timing policy is explicitly separated before results: report optimizer-plus-profile worker time, excluding the one shared xTB preparation. The 1.50 ratio remains a routine-throughput indicator, not a criterion for targeted rescue of previously nonterminating cases. A bounded targeted rescue has its own wall-time ceiling and is not a proposal to change the default for all 630. This new policy does not alter the rejection of P19 under P19's original conjunctive cost gate.

After calibration compatibility passes, run exactly the three P26-censored geometries used in P30: nonane seed 20261006 rank 1, TEG seed 20261006 rank 1 and DME seed 20261005 rank 1. Require the original proposal identities, recorded 80-evaluation censoring and the P30 geometry hashes. Both new arms start from the same frozen Cartesian coordinates with fresh histories, production SCF tolerances and the original Berny predicate. Each arm gets at most 80 new gradient evaluations and 3600 seconds including profile generation. A scientific censor is distinct from a native failure or a missing result. All six arm outcomes are required.

The six-chain inputs are also frozen before pilot output is read: exactly one deliberately designated final saved checkpoint per fixed S1/S2 key, never an automatically chosen latest file among conflicts. No stopped driver or old optimizer pickle is restarted. A separate authorization commit may permit the chain stage only if the 25-target numerical compatibility gate passes, at least two of the three pilots converge with full response while their off controls remain censored, zero pilots converge only in the off arm, and there are no failed or missing pilot arms. Bind the authorization to the calibration gate and the already frozen chain-plan hash. If this decision fails, the chain campaign stays closed in R7.

For each authorized chain, each arm has at most 100 gradient evaluations and 19800 seconds. Run the 12 arm-jobs independently, one arm per four-core worker, not a serial 11-hour pair. There is no resume or budget extension. Only the actual original Berny predicate evaluated with the declared gradient establishes that arm's convergence. Keep every result, including off-only successes and regressions. Do not claim omitted response caused all historical stalls from a subset of successful interventions.

After a global acceptance record, a full-response chain result can become an individual replacement candidate only if the profile completed, connectivity and provenance checks pass, and its fixed local compatibility check passes. Compare against that chain's existing flagged profile in a complete unchanged open636 background, in separate processes: every benchmark IDAC identity involving the chain plus both-role water/methanol/nonane/DME probes at 250, 298.15 and 400 K. Require identical finite masks and maximum absolute change below 0.05 in both dsp and P28-Z0x on evaluable probes. A larger change leaves an explicitly Berny-converged A experimental geometry, but does not automatically replace a flagged profile. Raw bin differences are reported. Promotion is a separate recorded, backed-up metadata/provenance operation; no R7 helper writes profiles_v2. An off-arm original-protocol success is also reported and may follow the existing original-protocol replacement route. No blanket 630-profile regeneration is authorized.

P33 is a new stationarity-referee diagnostic, separate from the optimizer test. Use the same five geometric identities as P30, but normalize each projected Cartesian probe to unit L2 norm. Do not apply the new gate to the old collectively normalized data as if it were the same test. The scientific target is tau=1e-5 Eh/Bohr, one fifth of R6's pre-existing 5e-5 Cartesian force target. This is an engineering numerical-accuracy budget, not a fitted statistical confidence limit.

For each direction use the fixed Bohr ladder 0.016, 0.008, 0.004, 0.002, 0.001. Compute plus/minus energies at tight SCF (1e-11, orbital-gradient 1e-7) and strict SCF (1e-12, orbital-gradient 1e-8), retaining the same grid and cavity settings. Compute tight/full, strict/full and strict/off center gradients. Use the finest Richardson derivative; do not select the step that agrees best with a gradient. The uncertainty indicator is the full difference of the two finest strict Richardson estimates, plus the last-two-estimate tight/strict discrepancy, center-gradient precision discrepancy, and the explicitly computed floating-point cancellation allowance. Require indicator <=tau/4 and stabilization of the nested estimates. Changing density-pruned grid counts makes the result inconclusive. Counts are a topology warning, not proof that every retained-grid identity is unchanged.

If absolute discrepancy plus the indicator is <=tau, label the directional result consistent. If discrepancy minus the indicator exceeds tau and the precision/stabilization checks pass, label it inconsistent. Otherwise label it inconclusive. This is an empirical finite-resolution test, not a rigorous interval enclosure. A coarse or noisy reference cannot earn a pass by widening a tolerance. missing_response_material is True only for consistent full response and inconsistent off response, False only when both are consistent at the declared tolerance, and otherwise unknown. Complete diagnostics remain diagnostic_complete regardless of their scientific verdict. At most 82 SCFs and three gradients per case, 7200 seconds per case. A pass authorizes neither the old P30 stage 2 nor any stationary-basin or harmonic-free-energy claim.

P34 is a sampled audit of the frozen 630 primary profiles, not a census certificate. Choose the first 32 keys under SHA256('R7-primary-screen-v1|'+key), then add the eight fixed sentinels water, methanol, nonane, EG, DEG, TEG, glycerol and propylene glycol, counting overlaps once. Freeze the full population profile hashes and the saved geometry bytes before outcomes. On each selected geometry perform one production-SCF SVP calculation and off/full gradient evaluations at the same density. Then compute the unchanged TZVP profile at the center and at plus/minus 0.01 angstrom maximum atomic displacement along the projected negative full-response gradient. Remove rigid motion; use the fixed first R6 probe only if that direction is numerically zero. No minimization is performed. Report the stored-profile versus recomputed-center discrepancy separately, since saved XYZ coordinates may have been rounded.

Use fixed both-role water/methanol/nonane/DME probes at 250, 298.15 and 400 K, complete open-profile overlays, fresh processes and P28. A finite-stress response of >=0.01 in either model is a screen-positive outcome. Coverage differences and absent outputs remain unresolved. Report gradient-response magnitudes separately; a 1e-5 Cartesian component difference is a force indicator, not Berny's internal-coordinate predicate. If a sampling-model upper fraction is reported, it concerns this screen only and is conditional on treating the frozen SHA ordering as uniform sampling. Sentinel evidence is descriptive. No finite-stress sample proves a profile bound over all nearby geometries or locates the corrected minimum. Maximum 40 case-hours on four-core workers; each case has one SVP SCF, two SVP gradients and three TZVP single points. No production relabel or full re-optimization is authorized.

P35 records the glycol mechanism as unresolved under the available inputs. Positive weighting of the supplied sample cannot exceed its relevant tail envelope. That fact does not identify the historical UD geometry, exclude unsampled basins or rule out every electronic/cavity method. No new QC budget is assigned to matching the UD histogram. Reopening requires auditable generating inputs or an independently validated electrostatic/basin calculation on fixed controls. Water and branched polyols remain required counterexamples to any universal OH-only explanation.

All jobs use immutable inputs, isolated output directories, exclusive claims and process-group deadlines. No automatic retry or stale-lock removal is allowed. Independent jobs continue after another member fails; every requested identity retains an outcome. UD-backed gates run on the Mac. Raw data and historical registrations remain unchanged. The total possible native ceiling, if every explicitly conditional stage is authorized, is 147 four-core worker-hours, not an expected duration or a claim of available account quota.

- R7 amendment P34a (2026-10-06, before any P34 plan or output; the first screen plan attempt in Mac job 372 stopped at the metadata check and
  produced nothing). r7_screen.py plan required meta geometry_converged=True, but 626 of the 630 primary profiles predate that field (4 carry it).
  Every primary profile records meta "geometry" = "BP86/def2-SVP C-PCM conductor (pyberny)" (621) or the same with "[resumed from checkpoint]"
  (9), and pyscf_cosmo_v2 writes a profile only after Berny reports convergence. The amendment accepts that legacy provenance string when the
  geometry_converged field is absent; an explicit non-True value still fails. Selection, sentinels, budgets and gates are unchanged. A workflow
  dispatch for cloud/r7/screen/plan.json made before the plan existed (run 37546536602) is void.

- R7 amendment P33a (2026-10-06, before any P33 computation). The first P33 dispatch (Actions run 37546518712) stopped every case in 0.2 s at the
  package check: r7_referee.py compared importlib's version string to the literal '2026.03.6', but pip reports the pinned RDKit 2026.03.6 as the
  PEP 440-normalized '2026.3.6' (the same string the frozen R7 plans record). No SCF ran and nothing was computed. The amendment compares normalized
  versions; the pin itself is unchanged. Because the plan records the script hash, cloud/r7/referee is re-frozen with the same five cases, geometries,
  ladder, tolerance and budgets, and dispatched once more. Run 37546518712 is void as an execution failure, not a scientific outcome.

- Round 7 RESULTS (recorded 2026-10-06 ~19:00 PDT; registered 6a51e75; plans 95c8d88, screen a8c5de0, referee 97db7ea; amendments P34a ef2fa58 and
  P33a 29e9bf2; Actions runs calibration 37546500861, referee 37547463603, screen 37546971488; void dispatches 37546518712, 37546536602, 37546787100;
  Mac jobs 372-383). Details and data in docs/astra/round7/RESULTS.md and data/.
  P32 calibration: 25/25 targets reach the original Berny predicate in both arms; wall ratio 1.13; identical finite masks (dsp 2271, Z0x 2302);
  max |dsp change| full vs off 0.0121 (limit 0.01), median 1.7e-4; max |Z0x change| 0.0170; median |dsp - UD| 0.136. Compatibility gate FAILED;
  pilot not dispatched; no chain permit; the six-chain campaign stays closed and the S1/S2 flags stand.
  P33: 4/5 cases diagnostic_complete (methanol SCF failed after 21 SCFs). Resolved directions: full consistent / off inconsistent (omitted response
  material) in nonane bond 0-1 and 1-2 and TEG bond 1-2; full inconsistent in TEG bond 3-4 (2.2e-5 > tau 1e-5); both consistent in nonane bond 2-3
  and EG bond 2-3; all other directions inconclusive (Richardson ladder not stabilized within the tau/4 ceiling).
  P34: 39/40 cases complete (XIRNKXNNONJFQO never recorded a final status), so no sampling bound. Off/full force difference > 1e-5 Eh/Bohr in 39/39
  (max 3.3e-4). +/-0.01 A stress: 35 screen-positive (max |d ln gamma| >= 0.01; largest 0.66), 4 unresolved (finite coverage changed), 0 negative.
  No primary profile changed.
  P35: glycol mechanism recorded as unresolved with the registered reopening conditions.

- Round 8 (Astra report docs/astra/round8/ZCOSMO_ROUND8_REPORT.md, received 2026-10-06). Registered by the routine "register all, run in order"
  default. The five patches (H8, P36, P37, P38, REG8) are applied unchanged to 58cc629 in the same commit as this text, before any round-8 plan or
  output exists. Verified before registration: all patches apply; r8_selftest.py passes in the container (10 tests; PCM matrix-derivative error
  4.1e-13, FD reference error 9.0e-12); r8_evidence.py reproduces the archived R7 numbers (P32 max dsp change 0.012074, P33 4 complete / 3 resolved
  omitted-response / 1 full-inconsistent, P34 40/35/0/4/1 with no sampling bound); the pinned PySCF 2.14.0 rks.py sets small_rho_cutoff default 0.
  P38 (README closing status) is included in this commit. P37 budget: one dispatch of 8 one-hour Actions jobs, no automatic rerun, no chain retry,
  no 630-profile re-polish, no corrected-gradient default. The Astra text below is adopted verbatim.

Round-8 proposed registration. This text is not a claim that it has been adopted.
Append the accepted text with the actual commit timestamp before new candidate
computation. The source baseline is 58cc629df42156c0b7862710057318db0a495dbb plus
these archived R8 helpers. The hypotheses are motivated by known R7 outcomes;
this is neither a new ThermoML holdout nor selection by experimental error.

P32 remains rejected under its actual maximum-dsp compatibility limit of 0.01.
Neither its 0.012074 result nor the small median changes authorize its pilot or
chain stages. The six stopped chains retain S1/S2 labels and receive no native
budget in R8. The 630 primary profiles remain a frozen original-gradient data
version. R8 authorizes no re-polish, new profile, profile promotion, re-scoring,
conformer weighting, or change to a production default. P35 stays unresolved.
P20 and P28 retain their accepted, explicitly scoped status. P28 remains opt-in
in the current code; this registration does not change its deployment switch.

P36 is E read-only bookkeeping. Reproduce the archived R7 denominators and
recorded decisions, preserving native failures and inconclusive directions.
Report P32 timing from its paired runs. Do not infer a count or identity of
above-limit queries from an extrema-only JSON. Keep P34's 35 positive screens,
four affinity-coverage failures and one unfinished native case separate. Do
not estimate population prevalence or turn fixed-displacement sensitivity into
an error estimate at the corrected minimum. Historical files remain unchanged.

P37 is one final A stage-isolation diagnostic, not a relaxed referee or an
optimizer trial. Freeze exactly the archived P33 TEG bond-3-4 direction that
was resolved inconsistent with full response and the EG bond-2-3 consistent
control. They are targeted diagnostic identities, not a random sample. Use
their existing full-precision unit-L2 Cartesian vectors and exact generating
geometry hashes from cloud/r7/referee and docs/astra/round7/data/referee.
No new conformer, reorientation, random direction or step-size selection is
allowed. Freeze the plan and code hashes before native output.

Cross PCM on/off with the existing angular pruning/None, yielding four arms
per case and eight jobs in total. Use BP86/def2-SVP, the existing DF auxiliary
basis, XC grid level 2, and, when attached, C-PCM epsilon 1e9, Lebedev 17 and
project radii. The no-PCM arms are genuine vacuum controls at the same nuclear
coordinates, not claims that their electron density matches the PCM density.
Check the actual runtime small_rho_cutoff is zero. An unexpected nonzero value
is an environment mismatch and stops the job; do not silently force it to zero.
Angular pruning and density-based point removal are different settings.

Pin PySCF 2.14.0 and pyberny 0.7.0 using normalized package versions. Record
NumPy/SciPy versions and the loaded upstream source hashes. Native jobs use
four OpenMP threads, one BLAS thread, 4000 MB nominal PySCF memory and a 2000 MB
PCM integral cache. No tighter integral threshold, denser radial grid, alternative
SCF solver, modified PCM switching, or other functional/basis is substituted.

Per arm compute tight and strict center SCFs, with (conv_tol,conv_tol_grad)
equal to (1e-11,1e-7) and (1e-12,1e-8), respectively. Compute tight/full-response,
strict/full-response and strict/off center gradients, retaining DF auxiliary
and, where present, PCM derivatives. Compute both signs of the fixed Bohr
ladder 0.016,0.008,0.004,0.002,0.001 at each precision. All five energy pairs
are required; the finest Richardson estimate is the reference, not a selected
best-agreement step. This is exactly 22 SCF calls and three full molecular
gradient calls per completed arm.

Retain P33's tau=1e-5 Eh/Bohr and its unchanged finite-resolution decision rule.
The uncertainty indicator is the difference of the finest strict Richardson
estimates plus tight/strict, center-gradient and roundoff indicators. Require
its value at most tau/4 and stabilization. Consistency requires discrepancy
plus indicator at most tau; inconsistency requires discrepancy minus indicator
greater than tau; other outcomes are inconclusive. This is not a rigorous
interval enclosure. No outcome is promoted by increasing uncertainty or changing
a threshold. The old P33 and P30 decisions are never overwritten or re-gated.

Track retained XC points by generating atom and atomic-template ordinal,
ignoring zero-weight padding, and PCM points by generating atom and Lebedev
ordinal. Equal point counts alone do not establish identical membership. A
membership change along a ladder makes its assessment inconclusive. Compare
the SCF quadrature with the full-response quadrature at both centers, requiring
identical node membership and matching weights (absolute 1e-12, relative 1e-10).
A discrepancy is recorded and also makes the derivative verdict inconclusive.
These are quadrature representation checks, not universal AO-screening proofs.

In each PCM/pruned arm additionally test the explicit PCM partial derivative
at the strict center. Freeze the AO density coefficient matrix P0, retain the
same AO labels and basis, move the atom-centered basis and PCM surface with
the geometry, and solve the surface charges anew. Do not set frozen=True.
Compare the derivative of E_PCM(R,P0) with PCM.grad(P0). The off-center overlap
electron count can change because the basis moves; report it, never renormalize
P0. This derivative is not the PCM energy derivative along a relaxed SCF curve
and is not a fixed physical real-space density derivative.

Use stock PCM and the existing CachedPCM3c independently at the center and the
ten displacements: 22 explicit PCM energy calls and two PCM gradient calls per
case. Require linear-solve relative residual at most 1e-10. Cache/stock parity
is an E diagnostic, maximum center/displaced energy difference below 1e-9 Eh and
maximum center gradient difference below 1e-8 Eh/Bohr. Apply the unchanged
finite-resolution ladder calculation to the layer, retaining its interpretation
as two float64 implementations, not an independent high-precision oracle.
No cache implementation is changed or newly accepted by this test.

The budget is eight one-hour four-core native jobs, with a 3400-second internal
deadline and a 3600-second process-group deadline. Maximum totals are 176 SCF
calls, 24 molecular gradients, 44 explicit PCM energy calls and four PCM gradients.
Installation, planning and artifact transfer are outside the native-time count;
no paid resource or guarantee of available account quota is implied. No retry,
continuation, new optimizer history or budget extension is authorized. Reuse
no prior native result as an unlabelled new observation. Preserve every failed
or missing job. Scientific negatives can complete; execution failures must
propagate a nonzero status and receive a terminal execution record. Collection
requires one result and bounded execution record per requested identity.

First require the PCM/pruned baseline to reproduce the TEG inconsistency and
the EG consistency before interpreting another arm as removing that discrepancy.
Failure to reproduce is informative but does not demonstrate a fix.
Interpret only resolved contrasts. An unpruned-arm improvement is evidence
of dependence on angular quadrature, not proof that all pruning is a bug or
that the new energy is physically more accurate. A vacuum/PCM contrast alone
cannot isolate an additive solvent error because the SCF density changes.
A resolved explicit-layer failure localizes an issue to the PCM partial
calculation at this density and surface; it does not by itself identify a
particular switching term. A passing layer and failing total derivative leaves
SCF, other derivative terms or integral/quadrature screening as possibilities.
A cache/stock discrepancy is reported before making a physical attribution.

Neither a pass nor a favorable contrast authorizes corrected-gradient defaults,
a 630-profile re-polish, six-chain jobs, an ensemble or experimental scoring.
If the fixed contrasts remain inconclusive or fail operationally, archive the
unresolved mismatch and close this diagnostic budget. Reopening would require
new independent evidence, auditable inputs or a source-level correction, then
a separate registration. There is no automatic next parameter sweep.

P38 is E reporting only. Append the supplied short README status, linking the
archived evidence. Preserve distinctions between original-predicate convergence,
full-energy stationarity, numerical acceptance and experimental accuracy.

- Round 8 RESULTS (recorded 2026-10-06 ~21:50 PDT; registered 333b2ab; plan 54e0ebc; one P37 dispatch, Actions run 37565712769, 8/8 jobs completed,
  none rerun). Deviation: plan.json records the registration as fc898fb (the container commit before `git am`), which is tree-identical (a6c0eac) to 333b2ab.
  P36: all archived R7 numbers reproduced with zero quantum evaluations; no new gate passed.
  P37: baseline_P33_pattern_reproduced = False. EG 2-3 pcm_pruned is full-consistent (error 8.5e-10), reproducing P33. TEG 3-4 pcm_pruned is inconclusive:
  the ladder stabilized (indicator 4.5e-7) with a discrepancy of 2.16e-5, but one PCM surface node (minimum switching weight 5.5e-13) left the retained
  set at the + displacement for h <= 0.008 Bohr, a membership change that makes the verdict inconclusive. The other six arms are inconclusive (four did not
  stabilize; TEG pcm_unpruned has the same membership change). XC grid membership was constant in every arm. The SCF and response quadratures matched.
  Explicit PCM partial at fixed AO density: EG consistent (2.7e-13), TEG inconclusive by membership (error 3.1e-14). CachedPCM3c and stock PCM parity
  passed (<= 7e-16). Per the registration, no contrast is interpreted, the TEG mismatch is archived as unresolved, and the R8 diagnostic budget is closed.
  No optimizer, re-polish, chain retry or default change is authorized. No profile version changed.
  P38: README "Current evidence" section applied in 333b2ab.

- Round 9 (Astra report docs/astra/round9/ZCOSMO_ROUND9_REPORT.md, received 2026-10-07). Victor chose "register, run, then close". The three patches
  (P39, P40, REG9) are applied unchanged to 83cf521 in the same commit as this text, before the P39 audit output exists. Verified before registration:
  all patches apply; r9_membership_audit.py self-test passes (6 tests); the pinned PySCF 2.14.0 pcm.py matches the report's source claims (switch_h
  smoothstep clipped to [0,1], distances below 1e-8 zeroed, retention when w*F > 1e-16, S diagonal xi*sqrt(2/pi)/F). Native budget for R9 is zero.
  The Astra text below is adopted verbatim.

Round-9 proposed closeout record. Record adoption with the actual commit ID.
Reference main: 83cf52163d806ef0c92ba2002094832824122d59.

P39 is an E, zero-QC replay of the existing P37 TEG PCM/pruned call log.
It checks the exact archived Git blob and preserves all 22 call identities.
It reports node counts separately from membership hashes and identifies the
location of the minimum over retained switching weights. It does not identify
a removed node from a minimum, change a referee verdict, recompute a model,
or create a new scientific acceptance gate. Prior read-only analysis of this
archive is explicitly retrospective, not a preregistered discovery.

P40 appends the R8 unresolved-mismatch and closed-budget status to the README.
No historical registration, result, source profile, or model default is edited.
P32 remains failed. P30/P33/P37 outcomes keep their original qualifications.
P20/P28 keep their existing scoped acceptance. The 630 original-gradient
profiles and six S1/S2 profiles remain unchanged. P35 stays unresolved.

The R9 native budget is zero: no Actions dispatch, new SCF, geometry re-polish,
chain retry, profile generation, or experimental scoring. P37's observed
membership changes are not, on their own, independent validation of a source
correction. Further native work requires distinct evidence that isolates a
specific error and a separate prospective authorization. This note creates
no automatic continuation and does not reopen the R8 budget.

- Round 9 RESULTS and campaign closeout (recorded 2026-10-07). P39: the archived TEG PCM/pruned log matched blob 1273d62d; all report assertions
  pass (XC memberships 1, PCM memberships 3, equal-count membership change at +0.016 Bohr only, minimum retained switch 5.5136e-13 located there,
  positive-side membership constant for h <= 0.008, finest Richardson -1.456546290986201e-6). This corrects the R8 RESULTS wording that tied the
  minimum to the calls where a node dropped out; the R8 verdict is unchanged (inconclusive, unresolved). P40: README lines applied and checked.
  Zero native work. Victor chose to close the Astra review after R9; no ROUND10 prompt is written. Reopening needs distinct evidence and a new
  prospective registration.

- Round 9 closeout amended (2026-10-07): Victor reopened the Astra review for round 10 on the P35 glycol question (docs/astra/ROUND10_PROMPT.md).
  The R8/R9 numerical-gradient campaign stays closed. No budget or protocol change is registered by this note; any R10 work needs its own registration.

- Round 10 (Astra report docs/astra/round10/ZCOSMO_ROUND10_REPORT.md, received 2026-10-07). Victor chose "run all" and confirmed the project is
  academic/non-profit use under the NIST UD notice (no redistribution: raw .cosmo files and detailed derived tables stay outside the repository).
  The four patches (P41, P42, P43, REG10) are applied unchanged to 4dc8985 in the same commit as this text, before any acquisition, manifest or
  comparison output exists. Verified before registration: all patches apply; r10_selftest.py passes in the container (20 tests); the NIST notice
  and the EG raw file at usnistgov/COSMOSAC 1b82456 are retrievable and the EG Git blob matches b0cc75c9. Native budget: zero SCF, zero model calls.
  The Astra text below is adopted verbatim.

R10-P41-P42-P43: UD provenance, zero-QC replay

Proposed registration. Append adopted text to PREREGISTRATION.md with the actual
commit identity before acquisition or comparison. This file alone is not an
acceptance record. The reviewed baseline is
4dc898521f6c49355e442be78f1e2570d3686aee. R8/R9's numerical-gradient campaign
remains closed. P32 remains failed; no stopped chain is restarted. P35 is opened
only for provenance acquisition and a descriptive same-parser comparison, not
for a claim that its physical mechanism is resolved.

The public source locations and raw Git blob identifiers were discovered during
this review. No new quantum computation or UD/open numerical comparison was
performed in that review. The design is motivated by previously inspected R4-R9
results, not a new experimental holdout. No ThermoML response, UD tail target or
conformer energy selects a parameter or a member.

P41 is E acquisition and integrity checking. Use only the twelve raw `.cosmo`
files and two provenance documents in scripts/r10_sources.py at public NIST
COSMOSAC commit 1b82456be38026719b16cad4076109bef3fcb309. Verify the exact Git
blob for each download and record a SHA256 of its bytes. Preserve line endings.
One request per file, a 30-second socket timeout and an 8 MB per-file ceiling;
no alternative source, automatic retry, file replacement or incomplete-success
claim. Retain every failed acquisition status. The twelve compounds are water,
methanol, EG, DEG, TEG, tetraethylene glycol, glycerol, propylene glycol,
2-methoxyethanol, 1,2-dimethoxyethane, THF and n-nonane, as in the fixed R5 panel.

The data notice is independent of any repository code license. The operator
must review applicable use rights and acknowledge them before acquisition.
Neither this registration nor public availability grants redistribution or
commercial-use permission. Downloaded data and detailed derived reports remain
outside the repository on the Mac. Do not place raw data, geometries or dense
replayed profiles in public Actions artifacts. This round launches no Actions
computation; downloading already-existing P25 artifacts is retrieval only.

P42 is E read-only input comparison with same-input numerical replay gates.
Before calculating descriptors, freeze the source files and all original
630+6 profile hashes. Freeze the twelve saved generating geometries and exactly
one original P25 TZVP/SWIG result per key. Match native geometry hashes against
cloud/r5/shape-plan/manifest.json and coordinates against both the stored NPZ
and primary saved JSON. Match each archived P25 Hsieh profile and Mac UD profile
to the SHA256 already recorded in p25_stage_comparison.csv. Missing, conflicting,
changed or duplicate sources stop preparation. No newly generated raw table
may silently replace an absent artifact. If archived artifacts are no longer
available, report that limitation; do not rerun their SCFs under this budget.

Match compound identities using the public list and the project's
ud_complist.csv, with explicit source and target keys. Propylene glycol maps
benchmark DNIAPMSPPWPWGF-UHFFFAOYSA-N to published
DNIAPMSPPWPWGF-VKHMYHEASA-N. This follows the existing unique-connectivity lookup
and is an explicit stereochemical limitation. Never use embedded .car numbers
as compound-list identifiers, or choose among ambiguous skeleton matches.

The external manifest records all input hashes, reviewed code hashes and the
normalized Mac package versions. Commit its SHA256, and only that SHA256, in
docs/astra/round10/PLAN_SHA256.txt before the first comparison. Pass that actual
plan commit to the comparison command. The actual registration commit must be
an ancestor of HEAD and contain this marker. The frozen source files and inputs
are checked again before and after the comparison; package drift blocks it.

Use the reviewed project to_sigma.py Git blob
9f2e0d6f3bb4da4880f9bd6ad702847f9308ed1d for both paths. Parse historical UD
DMol3 output using Dmol3COSMOParser(num_profiles=3, averaging='Hsieh'). Adapt
archived retained open segments using the existing r4_common.parser_trace.
Keep the 0.52917721067 Bohr-to-angstrom conversion and existing Hsieh and HB
constants. Read the actual charge column and recompute charge/area; do not use
the rounded printed density instead. Do not neutralize charges, choose a
correction column by closeness to a reference, clip a sigma, change atom
classification, or tune averaging. No new surface filter is applied to the
archived open table. A parser exception is a failed replay, not permission to
alter the parser in the same experiment.

Require every replay to reproduce its own stored 153-bin area profile with
maximum absolute difference strictly below 1e-8 square angstroms. UD area,
volume, averaging metadata and dispersion metadata must also match their
historical values at the stated 1e-8 numeric tolerance. Require binwise HB-area
conservation and total retained area within 1e-8 square angstroms. This is a
same-input integrity gate, not an E claim that open and UD physical profiles
match. There is no experimental accuracy acceptance criterion or model scoring
in R10. Primary-versus-P25 differences are reported separately and never used
to replace or relabel a primary file.

Only after a member passes its lineage/replay gate, compare its geometries and
raw distributions. Check observed covalent connectivity against declared RDKit
structures. Retain every heavy-atom graph isomorphism, with an explicit ceiling
of 256 that fails rather than truncates a symmetry search. Report each proper-
rotation heavy-atom RMSD and its heavy-chain and H-O-C-X dihedrals. Do not reflect,
reorient or modify a geometry used for charge averaging. Symmetry correspondence
is not conformer generation; graph matching does not certify stereochemistry.

Retain the existing contact definition from r4_common: donor-acceptor distance
at most 3.2 angstroms, H-acceptor distance at most 2.5 angstroms and D-H-A angle
at least 120 degrees. Report all candidate contact geometries and the indicator;
never interpret the indicator as an H-bond energy or exclude a structure using
it. Water and the branched-polyol controls remain in the panel even when their
responses differ from those of the linear glycols.

Report raw charge sums and area-weighted sigma distributions, then the
averaged distribution and pre/post-HB bins. Distinguish the raw tessera tail,
averaged continuous-segment tail and unnormalized final binned-profile tail.
The fixed tail threshold is absolute sigma at least 0.01 e/A^2, inclusive on the
rounded three-decimal output grid. Preserve normalized-profile distances and
atom-resolved areas. Do not pair tessera rows from different surfaces by ordinal.
Preserve original and corrected printed charge summaries and a rounding-only
charge-sum screen; that screen does not assign a new physical convention.

Read cavity metadata literally. Record the input setting called "Number of
Segments" separately from the actual table count, and record the embedded
.car name without treating it as a modern index. The public papers and tutorial
establish nominal electronic-method context. Mark per-file electronic-deck and
solver-history verification as absent unless independent exact records have
actually been obtained. File-header metadata cannot fill in an absent method.

All twelve requested identities retain outcomes. A failure blocks that member's
scientific comparison, while independent members continue. Overall success
requires all twelve lineage gates, exact input integrity and zero native/model
calls. A partial panel is labelled partial. No helper writes a .sigma file to a
production directory or changes an existing input. The budget is zero SCF calls,
zero quantum gradients, zero model evaluations and zero conformer searches.
There is no automatic native continuation, basis sweep or histogram-matching
stage. Code-only synthetic tests may run before registration and off the Mac;
actual UD-backed acquisition and replay run on the Mac.

Interpretation: successful replay links the public raw input to the historical
Mac sigma profile within tolerance. Different geometry with different raw
charge distribution identifies a joint historical difference, not its causal
partition. Identical geometry but different raw distributions points to the
remaining electronic/cavity representation, subject to the provenance checks.
A coordinate-only comparison cannot prove the equilibrium liquid distribution.
No observed difference selects a conformer or establishes that UD is the truth.

P43 is E reporting. Add a dated provenance update without rewriting historical
numbers or failed registrations. Clarify that prior raw-input absence described
the Mac holdings, and that P29's raw area-profile tail is not a pre-averaging
raw-segment tail. Record the public notice's empirical conformation-selection
history without asserting which glycol was revised or alleging ThermoML leakage.
Retain the statement that Z0x was not fitted to ThermoML, with no broader claim
that every upstream input was wholly uncalibrated. The physical glycol mechanism
remains unresolved. The frozen profile version and all earlier numerical
acceptance/rejection decisions remain unchanged.

- Round 10 RESULTS (recorded 2026-10-07; registered 39cd85d; manifest frozen ba033e4, SHA256 4acf76db...fca0f; Mac queue jobs 392-394; 0 SCF, 0 model calls).
  P41: 12 UD raw files + 2 provenance documents acquired, all Git blobs matched; raw files kept outside the repository under the NIST academic-use notice.
  P42: all 12 lineage/replay gates passed (UD raw tables regenerate the Mac UD profiles to ~1e-14 A^2; open P25 tables regenerate their own profiles).
  Descriptive only: the four UD linear glycols are fully extended all-anti chains with no OH...O approach (H-A >= 3.9 A); the open geometries are gauche-
  folded with H-A 2.2-2.4 A (no member meets the registered contact rule). Raw polar tails UD/open: EG 41.0/34.5, DEG 47.6/40.7, TEG 57.1/49.0,
  tetraEG 67.9/61.1; glycerol and propylene glycol reverse (48.3/52.9, 33.3/38.1). At matched geometry (water, methanol, THF, methoxyethanol) raw tails
  differ by 0.4-2.9 A^2. Open tables carry net charge -0.012 to -0.045 e vs UD ~-0.001. No causal partition: p_O(R_U) was not computed. Nothing adopted.
  Deviations: two r10 self-tests fail on macOS only (/var vs /private/var path comparison in the test assertions; all 20 pass on Linux); freeze used the
  main checkout's data/pyscf_sigma as --profile-root because profiles_v2 is untracked; the first freeze attempt failed before writing any output.
  P43: applied in 39cd85d; PROVENANCE_STATUS.md given a dated outcome line.

Round 11 prospective registration recorded 2026-10-07T11:10:40Z. The following design is adopted before plan generation or native output.
- Round 11 (Astra report docs/astra/round11/ZCOSMO_ROUND11_REPORT.md, received 2026-10-07). Victor chose "register all, run on Mac". The four patches
  (H11, P44, P45, REG11) are applied unchanged to 463ec1b in the same commit as this text. Verified before registration: all patches apply; r11_selftest
  (22 tests) and r10_selftest (20 tests, with H11's resolved-path assertion fix) pass in the container; P44's declared single-point settings match
  r4_charge.factory (b88,p86, def2-TZVP density fitting, grid level 3, conv_tol 1e-9, C-PCM eps 1e9, Lebedev 29, CachedPCM3c). Budget: 24 SCF slots,
  900 s each, 22500 s driver ceiling, Mac only, one run, no retry. The Astra text below is adopted verbatim.

R11-P44-P45: private fixed-geometry crossed profiles

Proposed registration, not an acceptance record. Append this text to
PREREGISTRATION.md and commit it with the reviewed helpers before freezing a
new plan. Base: 463ec1be5c0edfad1e8effd334a17fc44cd27405. This experiment is
motivated by the observed R10 input-lineage and geometry results; those results
are not a fresh holdout. R8/R9's numerical-gradient campaign remains closed.
The 630 primary profiles and six flagged S1/S2 files remain frozen. P30/P32 and
other prior scientific decisions are not reopened or overwritten.

P44 is an A coordinate-input diagnostic with E same-input integrity controls.
It does not change the open electronic method, introduce a conformer rule, or
claim independent basis/grid/response convergence. Use exactly the twelve
members and explicit source keys in r10_sources.DATA. Require the completed
R10 private manifest and summary, their recorded plan commit, all twelve
successful lineage gates, and all original input and protected-profile hashes.
A missing private asset cannot be substituted, downloaded anew as a different
version, re-embedded, or generated by another SCF.

Real preparation, native execution and collection occur only on the private
asset-bearing Mac, never on GitHub Actions, another CI system, or this review's
container. Native and dense derived data stay in private directories outside
all Git checkouts, with restrictive local permissions. Use the twelve already
acquired raw UD files. Do not commit their coordinates, raw tesserae, dense
profiles or private paths. The helper's public-summary.json is an allowlist of
aggregate scalar descriptors and decisions, and still requires operator review
before publication. No helper uploads an artifact or alters a production file.

Freeze the R10 manifest and summary hashes, exact helper source hashes and
normalized installed package versions in a private R11 plan. Pin PySCF 2.14.0;
retain the R10 NumPy/SciPy/pandas/RDKit/parser environment. Record Python version
and machine architecture. Commit only the new plan's SHA256 to
 docs/astra/round11/PLAN_SHA256.txt
before any SCF. Require the actual registration and plan commits to be ancestors
of the executing HEAD. Package, source, input or protected-file drift blocks
execution. Only the R10 test assertions for path aliases change; the R10
scientific helpers and numerical gates remain unchanged.

For every member run one new open-method calculation at its exact P25 stored
geometry RO and one at the exact atomic coordinates extracted from the recovered
UD raw file RU. Retain each file's own atom order, coordinate origin and
orientation. No Kabsch alignment, canonical rotation, reflection, optimization,
H-bond selection or modified bond geometry is applied to a calculation. The
RO/RU order is the fixed SHA256(key)-parity order stored in the plan. All pairs
run sequentially, each slot in a fresh subprocess. Geometry attribution means
this full coordinate-input change; it is not an isolated torsional or H-bond
intervention and may include finite-grid orientation dependence. The explicit
PG stereochemical alias is retained without claiming identical stereochemistry.

Use the unchanged r4_charge.factory and segments functions used by P25's
TZVP/SWIG arm. They use BP86 (b88,p86), def2-TZVP, existing density fitting,
XC grid level 3 with unchanged pruning, conv_tol 1e-9 and default orbital-gradient
tolerance/SCF cycle limit, C-PCM epsilon 1e9, SWIG, Lebedev order 29 and the
project's radii. Keep CachedPCM3c, its 2000 MB cache budget and nominal 4000 MB
PySCF memory. Use four OpenMP threads and one BLAS thread. Verify SWIG and the
method settings rather than accepting a changed default. No custom PySCF config (environment, working-directory or home file),
new SCF solver, extra grid, charge correction, alternative guess, or gradient
calculation is introduced. Save loaded upstream source hashes and runtime
settings. One kernel call is one SCF attempt, not one SCF iteration.

The budget is 24 SCF attempts, zero molecular gradients, zero optimizations and
zero activity-model evaluations. Each subprocess has a 900-second wall ceiling,
including its profile postprocessing. Thus reserved native slots total at most
21600 seconds (six serial Mac hours); the driver has a 22500-second allocation
including orchestration. A five-second process-kill/accounting allowance per
slot is not extra scientific compute. Remaining slots are not started once the
driver allocation is spent. Final zero-QC verification is reported separately,
not hidden as another SCF budget. The plan has a permanent exclusive execution
claim. No retry, resume, stale-claim removal, alternative output run, or budget
extension is authorized. Independent slots continue after an earlier failure;
missing, failed and timed-out identities remain in the requested denominator.
No finished output can be replaced by a later favorable attempt.

Require finite SCF energy and native convergence, electron-count error at most
1e-7 e, and relative PCM linear-system residual at most 1e-10. Preserve the
existing retained-surface filter, area > 1e-8 bohr^2. Record all/retained/discarded
net charges and areas, with conservation checks at 1e-12 e and 1e-9 A2. The
nonzero total screening charge is not itself a failure. Retained raw sigma
outliers outside +/-0.025 e/A2 are not clipped or deleted. Report counts, area
fractions, signed and absolute charge contributions, minimum patch areas and
area-weighted sigma quantiles at 1, 5, 50, 95 and 99 percent. Report pre-filter
extrema separately. Do not infer importance from a minimum sigma or node count
alone. No neutralization or per-atom charge reassignment is allowed.

Process every table through the identical pinned to_sigma.py Hsieh/NHB/OH/OT
implementation and r4_common.parser_trace. Keep raw tessera tails, continuously
averaged tessera tails and final binned tails distinct. Each tail uses
absolute sigma >=0.01 e/A2, with the final grid rounded to three decimal places
before the inclusive comparison. Keep unnormalized area profiles and separately
normalized profiles. Do not normalize a difference or equate different-surface
rows by tessera ordinal. Parser/domain failures are failed outputs; their completed native raw records
remain private and available for accounting, without permission to change the parser.

Reproduce the old R10 lineage/replay checks before attribution. For each new RO
repeat versus its own P25 archive require strict differences below: 1e-4 A2
maximum profile bin, 1e-5 normalized-profile L1, 1e-7 Eh total energy, 1e-5 e
retained net charge, 1e-4 A2 total area and 1e-4 A3 cavity volume. These are
same-input reproducibility tests, not an open-versus-UD agreement gate. This
experiment performs no 25/2302 affinity test and makes no new global E claim
for a changed production model. A larger cross-method or cross-geometry effect
does not fail scientific acceptance. Failure of any native/lineage/parity
control blocks the complete-panel attribution labels; partial results remain.

For each observable save U, A, R, C, where U is the replayed UD result, A the
archived P25 open result, R the new RO repeat and C the new RU crossed result.
The requested historical decomposition is U-A=(C-A)+(U-C). The simultaneous
current-run decomposition is U-R=(C-R)+(U-C). Report R-A explicitly and check
both telescoping identities; do not hide reproducibility drift in a geometry
term. Save the full 153-bin area and normalized-profile differences privately.
Report signed scalar terms for every tail and net charge. No tail percentage
is used as a percentage of ln gamma, MAE, or experimental error explained.

The fixed background controls are water, methanol, methoxyethanol and THF.
They are near-matching heavy-atom controls, not exact-geometry nulls or estimates
of random SCF noise. For each scalar tail define the prospective background
scale eta as the maximum of 0.5 A2, the largest control |U-R|, the largest
control |C-R|, and four times the largest |R-A| across all twelve members.
For normalized-profile L1 use the same rule with norms and a 0.01 floor.
These formulas and control identities are fixed before crossed results. Their
realized values are reported; no control is dropped, no threshold is tuned and
no unresolved control is treated as zero. No statistical confidence level or
basis/grid convergence is implied by eta.

For each signed tail let D=U-R, G=C-R, M=U-C. Significant opposite signs,
G*M<0 with min(|G|,|M|)>eta, give inconclusive_cancellation. Otherwise |D|<=2 eta
is inconclusive_small_contrast. A geometry-dominant label requires G to have
D's sign, |G|>eta and |M|<=max(eta,|D|/4). Interchange G and M for method-dominant.
If both have D's sign and each magnitude exceeds eta, after the dominance
checks, label both. Remaining cases are inconclusive_borderline. This is an
operational effect-size convention, not a physical correctness test.

For the normalized 153-bin differences use L1 norms Dn,Gn,Mn. Define cancellation
excess Gn+Mn-Dn. If it exceeds max(2 eta,Dn/4), label inconclusive_cancellation;
otherwise Dn<=2 eta is a small contrast. Geometry dominance requires
Mn<=max(eta,Dn/4) and Gn>eta; method dominance is the reverse. Otherwise label
both if Gn and Mn exceed eta, and inconclusive if they do not. Report the norms
and cancellation excess. Repeating each classification with the archived
instead of fresh RO result must leave the label unchanged, or that metric is
inconclusive_repeat_boundary. Controls themselves remain descriptive. For every
other member a broad profile-gap label is issued only when final binned-tail
and normalized-shape labels agree on mainly_geometry, mainly_method or both.
All other outcomes are metric-dependent or inconclusive. Net-charge and outlier
changes are supporting diagnostics, not tie-breakers or selection criteria.

An ordered decomposition does not identify the uncomputed reverse-method
interaction or establish a unique, method-independent causal percentage.
Even geometry dominance would not justify choosing the UD structure, rejecting
folded states, changing the contact-angle rule, or weighting conformers to
match the UD histogram. A future condensed-phase basin rule would require a
common free-energy convention and independent sampling/thermal validation,
including all eligible polyols and the water/branched controls. It receives
zero budget and no adoption authorization in R11. A profile average is not
assumed to equal a phase-equilibrated chemical potential. The existing incomplete
P26/P29 pools are not accepted as an ensemble.

P45 is E reporting. Update the README to acknowledge the completed R10 lineage
replay. Qualify the R10 controls as near-matching heavy-atom geometries, avoid
calling methoxyethanol rigid, and state that no per-glycol empirical-revision
label has been verified. Distinguish glycerol's small positive P21 shape shift
from propylene glycol's negative one. Preserve every measured number and prior failure.
Do not claim the crossed calculation has run merely because this protocol
and its code are committed. Record actual outcomes separately afterward.

- Round 11 RESULTS (recorded 2026-10-07; registered f60722f; private plan frozen 1ecca25, SHA256 b91657b7...d54e49; Mac queue job 396, one run,
  24/24 slots, driver 594 s, no retry; 0 optimizations, 0 gradients, 0 model calls). Same-input parity passed for all 12 (energy <= 7e-13 Eh,
  max bin <= 3e-11 A^2). Registered headline labels: all 8 non-control members metric_dependent_or_inconclusive, 4 controls descriptive, because every
  normalized-shape contrast is inconclusive_small_contrast (shape eta 0.359 L1 from the controls). Tail labels: EG, DEG, TEG mainly_geometry in raw,
  averaged and final tails (final-tail coordinate term 8.1-12.0 A^2 of gaps 10.0-14.4; method term 1.3-2.4); tetraEG raw tail mainly_method, others
  small; glycerol, PG, DME, nonane inconclusive. Open net charge is unchanged by the coordinate change (within 0.003 e). Nothing adopted; P35 open.

Round 12 prospective registration recorded 2026-10-08T01:06:10.024880+00:00. The following design is adopted before new plans or outputs.

- Round 12 (Astra report docs/astra/round12/ZCOSMO_ROUND12_REPORT.md, received 2026-10-07). Victor chose "register all, run in order".
  The four patches (H12, P46P47, P48, REG12) are applied unchanged to a93a1c9 in the same commit as this text. Verified before registration: all
  patches apply; r12 (26), r11 (22) and r10 (20) self-tests pass in the container; the original P21 archive (/tmp/r4work/AVP, 73 pair folders) and
  open snapshot (/tmp/r4work/p18-original, 636 files) are present on the Mac. P46 is retrospective explanatory scoring against ThermoML on 141
  already-inspected P21 glycol-solvent rows; it adopts nothing. Budget: <= 1,551 lngamma requests, 7,200 s, one run, no retry; zero QC.

R12-P46-P47-P48: private explanatory scoring and regional accounting

Proposed registration. Adopt and commit this complete text in PREREGISTRATION.md
before either new plan is frozen or any new R12 output is interpreted. Reference
main: a93a1c9abbec32e0af7ff259a8db6fa550bb34a9. The design is motivated by already
inspected R4-R11 outcomes, not by a new held-out experiment. Previous P30/P32
failures and P33/P37 decisions are not reopened. The numerical-gradient campaign
stays closed. The 630 primary and six S1/S2 production profiles remain unchanged.

P46 is A explanatory input substitution, with E replay/accounting checks. It
IS scoring against ThermoML under the optimization brief: experimental ln gamma
values are used to compute errors. No C profile, geometry, mixture parameter or
conformer weight may be selected from the result. C is the already frozen R11
open-method profile at that member's historical UD coordinate input. All such
data stay on the private asset-bearing Mac. No new quantum calculation,
optimization, molecular gradient, conformer search or fitted parameter is allowed.

Require the completed R11 private plan, its original committed digest and its
successful 12-member/24-slot integrity record. Run the original R11 checker,
retain its package/source/lineage requirements and protect its frozen 630+6
population. R10/R11 scientific helpers remain unchanged. Freeze hashes of the
new helpers and every reused input; retain the installed environment. Only
plan digests enter Git. No coordinates, dense profiles, per-row predictions,
logs or private paths may be committed or uploaded. Synthetic software tests
may execute outside the Mac and before registration.

P46 uses the ORIGINAL P21 factorial_rows.csv, summary.json and complete per-pair
rows, corner predictions and *.csv.inputs.json receipts. The archive must contain
332 unique r3_row_id observations and 14 solvent identities. Verify every pair's
solute, solvent, temperature and experimental value against the top-level table.
Verify per-pair predictions against the original nine output columns. The four
pre-stated scored identities and row counts are EG LYCAIKOWRPUZTN-UHFFFAOYSA-N (9),
DEG MTHSVFCYNBDYFN-UHFFFAOYSA-N (108), TEG ZIBGPFATKBEMQZ-UHFFFAOYSA-N (17), and
tetraEG UWHCKJMYHZGTIT-UHFFFAOYSA-N (7), totaling 141. Selection is by these exact
keys, not by a solvent-name synonym, error sign or R11 label. TetraEG remains
included despite its different R11 attribution. The other 191 P21 observations
remain in the read-only archive identity/hash audit, explicitly outside the new C scoring
subset. Do not change the 141-row scientific denominator or claim a new 332-row
C score. The original query rows are not rebuilt from a newer benchmark export.

Use the exact original P21 open solute and open solvent profile bytes. The
original per-corner receipts must match their SHA256 values, the UD solvent
bytes and the dielectric.csv, dispersion.csv and Z0.json tables. Recover the
original snapshot if necessary; do not silently replace it with current files
whose metadata hashes differ. P21/R11 UD profiles for the four targets must
match the already verified lineage. Missing, ambiguous or altered archives stop
preparation. No new SCF is authorized to recreate an absent private artifact.

Before C scoring, replay the original P21 open-solvent (000) and full-UD-solvent
anchors on the same 141 target observations using the HISTORICAL endpoint
(ZC_R6_ENDPOINT=0). This is 2*141=282 requested lngamma_inf evaluations. Audit
all 332 original archive identities and all nine per-corner stored outputs and
input receipts without new model calls. Check the archived 111/full-UD identity
to 1e-10. The 282 fresh anchor identities and finite coverage must match;
maximum absolute replay difference must be strictly below 1e-8 in ln gamma.
This is a same-input anchor gate, not a claim that every historical intermediate
corner was recalculated, or a relaxation of E/P32/scientific accuracy gates.
If anchor replay fails, record the failure and block every C-scoring job.
Do not change a solver or endpoint to make the old comparison pass.

The primary new evaluation uses the accepted P28 EXACT endpoint consistently
for O, all C-factorial corners and the full U solvent (ZC_R6_ENDPOINT=1).
For every one of the 141 rows, evaluate the eight O-to-C corners and U: 1269
requested calls. Keep the solute's original open profile in every corner.
Bit order is area, cavity volume, normalized 153-bin shape, exactly as P21.
For bit vector (a,v,s), use A=A_C if a else A_O; V=V_C if v else V_O;
and the shape C/A_C if s else O/A_O. Multiply the chosen normalized shape by
the chosen area. Retain original open metadata in the factorial. Z0x's physical
constants, chemical dielectric data, London data and chemical identities are
unchanged. The full-U anchor uses the original UD solvent file. This is not
an all-UD mixture and no solute is replaced merely because it is another glycol.

One worker handles one ordered pair and one corner in a fresh process. Its
temporary overlay must resolve BOTH requested profiles explicitly; a missing
open solute cannot fall back to UD. Clear inherited ZC_* experiment switches
and set the declared endpoint and private overlay before model construction.
Do not reuse a process-global profile cache across corners. No new data loader,
segment solver, endpoint approximation or physical model is introduced.

The maximum is 1551 requested model API calls, zero SCFs and zero gradients.
The job count is 11 times the number of target ordered pairs, computed from
the frozen inputs, not guessed here. The two replay anchors precede the nine
new endpoint-consistent evaluations for each target observation. Calls denote lngamma_inf
requests, not individual internal segment iterations. Run serially on the Mac,
with at most four OpenMP threads and one BLAS thread. Each worker has 120 seconds;
the model-run allocation is 7200 seconds including orchestration. A process-group
kill/accounting allowance of five seconds is not extra scientific computation.
Record closing zero-model integrity/aggregation time separately if it extends
the allocation. No parallel cloud workflow, paid resource, retry, resumption,
stale-claim deletion or second run of a claimed plan is authorized. Every
planned job retains a terminal state, even when it is blocked or never starts.

Failure handling is part of the design. Preserve requested row identities and
finite/nonfinite counts for every arm. Do not form a smaller favorable intersection.
A failed historical replay blocks the new stage. A missing, failed or nonfinite
new result blocks complete-panel error summaries; retain its diagnostic receipt
and the remaining completed values privately. A green process or workflow state
is not numerical acceptance. Independent jobs continue within the fixed budget.
The original input hashes and the protected production population are rechecked
after execution. Checks of saved output may be repeated without new model calls.

Report errors on the 141 fixed rows per solvent, pooled with original row weights,
and with equal solvent weighting as a declared secondary summary. DEG contributes
108 of 141 rows to the pooled score. For y_O,y_C,y_U and experimental y, report
MAE and bias. The removed absolute error is mean(|y_O-y|-|y_C-y|); the remaining
UD-comparator gap is mean(|y_C-y|-|y_U-y|). Their sum must equal the O-to-U MAE
gap. A recovery fraction is reported only for a positive denominator above
1e-6, is signed and is never clipped to [0,1]. Negative values and values above
one remain visible. No confidence interval, success threshold or production
acceptance is inferred from this retrospective fraction.

Apply the unchanged P21 shapley_three function twice to the complete eight-corner
cube: once to predictions and once to negative absolute errors. The second
calculation gives additive area/volume/shape contributions to absolute-error
reduction. Taking absolute values of prediction Shapley terms is not equivalent.
Require both efficiency identities to 1e-10. Positive/negative contributions and
interactions remain visible. A C-minus-O prediction change is not automatically
an error reduction. Report the legacy-versus-P28 O and U endpoint bridge on the
same target rows; never subtract a legacy O score from an exact C score. No
post-P28 value overwrites P21 or a historical scorecard.

The original P21 profile is the primary baseline, even if its bytes differ from
the R11 repeat. Hence P46 is explicitly a FROZEN-INPUT C-substitution explanation.
It is not a new pure torsional or hydrogen-bond causal estimate, and it does not
relabel the R11 profile decomposition. Dense per-row values and counterfactual
profiles stay private. Prediction Shapley values remain private; only aggregate bias and MAE statistics
and absolute-error-reduction Shapley values enter the public allowlist.
Only that aggregate error summary is eligible for separate human review before publication. The software never
uploads or copies it into Git. Publish improvements and deteriorations under
the same predetermined headings, clearly labelled retrospective explanatory
ThermoML scoring, not a fitted improvement or a new validated profile version.

P47 is an independent E read-only analysis with zero QC and zero model calls.
Freeze its own plan digest, so it can proceed even if the P21 archive is absent.
Use all twelve verified R11 members and all four archived profile families:
U (UD), A (P25 archive), R (fresh open-geometry repeat), C (crossed UD geometry).
Normalize each family by its OWN area before taking a normalized difference.
Use D=U-R, G=C-R, M=U-C and repeat drift R-A. Preserve the R11 classification
object unchanged, including the 0.359 realized scale and all inconclusive labels.
Do not substitute a new eta, exclude water, subtract a background vector, or
reinterpret the regions as independent hypothesis tests.

Partition the fixed 51-point sigma grid by integer millithresholds into five
bands: sigma<=-0.010; -0.010<sigma<=-0.005; |sigma|<0.005;
0.005<=sigma<0.010; sigma>=0.010 e/A2. Cross these bands with the existing NHB,
OH and OT channels. Each of the 153 entries belongs to exactly one of 15 cells.
Report each cell's signed mass change, L1 contribution and first moment, for
unnormalized and normalized profiles separately. Regional L1 shares sum to one
when the total is nonzero; use null for zero-total shares. Require conservation
of signed mass, L1 and moments to the implemented 1e-12 scaled arithmetic bound.
Also collapse the HB channels at each sigma and report L1_153-L1_51, the amount
of channel cancellation hidden by a total-profile projection. This is a
representation diagnostic, not an attribution to an HB energy term.

The positive and negative OH/OT regions use the existing acceptor-side and
donor-side parser convention. NHB entries remain NHB irrespective of sign.
The centre is a low-|sigma| region, not a proof of nonpolar chemistry. Raw
outlier tesserae and net surface charge are not reconstructed from a normalized,
smoothed histogram. P47 cannot infer a nonlinear ln gamma contribution from a
regional profile norm. All region tables remain private; no regional or dense
profile data are included in P46's public error summary.

P48 records the scope of the established result. The polar-tail gaps for EG,
DEG and TEG are mainly due to stored coordinate inputs under the registered
ordered open-method cross. TetraEG is an explicit exception, with a mainly-method
raw-tail gap and small other tail contrasts. No whole-profile attribution label
passed. No conformation is thereby established as the liquid distribution, no
UD structure is adopted, and no IDAC improvement is claimed before P46 executes.
The numerical-gradient campaign remains closed.

After these bounded read-only/explanatory tasks, archive the findings whether
favorable, unfavorable, operationally incomplete or inconclusive. The liquid-
state mechanism and a production conformer rule remain unresolved. R12 provides
no native or ensemble budget and no automatic continuation. A phase-dependent
free-energy protocol would require separately validated basin populations,
thermal contributions and common reference conventions on the full eligible
class and controls; the existing finite samples and R11 single points do not
supply them. A cheap calculation on incomplete inputs is not acceptance of such
a protocol. Historical profiles and scientific decisions remain unchanged.

- R12 amendment P46a (2026-10-07, before any P46 plan or model call). The registered P46 freeze stopped with "P21 universe or recorded completeness
  changed" (zero model calls). Inspection of the original archive (/tmp/r4work/AVP on the Mac): factorial_rows.csv has 332 rows with 13 unique
  solvent InChIKeys and 14 solvent names. The EG key LYCAIKOWRPUZTN-UHFFFAOYSA-N carries 10 rows: 9 named "ethylene glycol" and 1 named
  "1,2-dihydroxyethane", the same molecule. The registration fixed both "selection is by these exact keys, not by a solvent-name synonym" and an EG
  count of 9 (141 total), which contradict each other on this archive. Victor chose exact-key selection. P46a changes only the counts: EG 10 rows,
  142 scored rows, 13 solvent keys, 190 audit-only rows, 284 legacy and 1,278 exact requests (1,562 maximum). Code changes are limited to those
  constants in scripts/r12_review.py, scripts/r12_analysis.py and the matching r12_selftest.py fixture/assertions (26/26 pass). Every other P46 rule,
  tolerance, budget and interpretation is unchanged. P47 (already run under 76e3092) is unaffected.

- Round 12 RESULTS (recorded 2026-10-07; registered 05c35c8; amendment P46a d6b7e25; plans 76e3092 regions, fbba5e0 factorial; Mac jobs 399-401;
  0 SCF). P47: 12/12 members, 0 model calls; the same-geometry method term is centre-heavy (largest normalized L1 share in 11/12) with UD gaining
  positive-tail area in every polar member; the EG/DEG/TEG coordinate term moves area from the centre to the negative (donor-side) tail; channel
  cancellation <= 0.019. P46 (retrospective explanatory ThermoML scoring, 142 rows under P46a): 1,562/1,562 finite requests in 427 s; historical
  anchors reproduced to 4.4e-16. Pooled MAE O 1.813, C 0.702 (1.111 removed), U 0.419 (signed recovery 0.80; 139/142 rows improved; Shapley shape
  +1.103, area +0.009, volume -0.001). Per solvent recovery: EG 0.97, DEG 0.80, TEG 0.75, tetraEG 0.13. Not held out, not adopted; P35 open;
  630 + 6 profiles unchanged.

Round 13 reporting closeout adopted 2026-10-08T05:12:37.357610+00:00. Zero new native or model budget.

- Round 13 (Astra report docs/astra/round13/ZCOSMO_ROUND13_REPORT.md, received 2026-10-07). Victor chose "register, then close".
  P49, P50 and REG13 are applied unchanged to e2b36c8 in this commit. Verified before adoption: patches apply; r13 (15), r12 (26), r11 (22) and
  r10 (20) self-tests pass in the container; the public R12 RESULTS.md matches blob c036e8e2. Zero native or model budget.

R13-P49-P50: P35 explanatory closeout, no production geometry rule

Proposed record, not a claim of adoption. Append the adopted text to
PREREGISTRATION.md with the actual timestamp and commit before running the new
reporting command. Base: e2b36c8c5c2273f47ee6df21975b295b93689ca8.
The review has already inspected the public R10-R12 outcomes and performed
retrospective arithmetic on their rounded summaries. No new holdout or
prospectively discovered scientific effect is claimed.

P49 is E reporting. Replace the stale README statements about unmeasured IDAC
consequences and append a dated P35 closeout. Preserve the R10 lineage result,
R11's tail-specific ordered attribution, its inconclusive whole-profile labels,
and the tetraethylene-glycol exception. Record the P46a denominator of 142,
including ten EG observations, rather than the superseded name-based count.
The approximately 80 percent recovery refers to the O-to-U comparator MAE gap
on inspected rows with original open solutes and the same P28 endpoint. The
remaining C-to-U MAE difference is a conditional method-bundle contrast, not
C's entire experimental error or a universal method-error estimate. Preserve
all unfavorable rows and the retrospective scope.

Close the present P35 explanatory campaign. This is a stopping decision, not
acceptance of a liquid-conformer explanation. No most-extended, minimum-energy
or ensemble recipe is adopted. The frozen 630 primary plus six S1/S2 profiles
and all existing model defaults remain unchanged. P30/P32 failures, R11 labels,
P46a and R8/R9's numerical-gradient closure are not rewritten.

P50 is an E standard-library reporting check of public aggregates only. Require
the exact Git blob c036e8e24aa45a03aed0485664b3a26cd842c17f for the archived
R12 RESULTS.md. Check the published counts and independent rounding ranges,
then reproduce explicitly labelled hypothetical portfolio-sizing arithmetic.
Rounding ranges are not confidence intervals. This does not rerun the private
P46 checker, score ThermoML, certify its row-level inputs, or create a new
scientific gate. Read no private plan, geometry, surface file or profile.
Do not fetch an alternative result when a hash mismatches. Write a fresh
reporting output only; never overwrite a historical file. Repeating this
zero-model integrity check is allowed and is not another scientific run.

The cost scenarios allocate four or eight starts to each of 630 molecules for
sizing. They do not claim that all 630 require that many starts or that the
small-panel median is their mean runtime. A nominal single-point extrapolation
excludes geometry search, thermal quantities and independent validation. A
four-core worker-hour is wall time on four allocated cores, not a core-hour.
Twenty-way division is an ideal capacity calculation, not a promised schedule
or a claim of available free account quota. No scenario is an execution budget.

The authorized new native/model budget is zero: no SCF, gradient, conformer
proposal, optimization, molecular dynamics or activity-model request. There
is no Actions dispatch or private-Mac scoring task. UD-derived data stays
private on the Mac and is not copied by these helpers. The public summary
check can run on any local machine because it reads only already published
aggregate text. Code-only tests can run before the reporting record is adopted.

A future geometry project would first need one fully specified physical rule,
complete computational acceptance criteria and a genuinely unexposed validation
source with an exposure/overlap audit. Water and branched polyols remain required
controls; their already-inspected results do not become independent holdouts.
No current test split is certified fresh by this record. Such a project needs
its own prospective registration and budget. This closeout creates no automatic
continuation or permission to select conformers from the R12 accuracy result.

- Round 13 RESULTS and Astra-review closeout (recorded 2026-10-07; zero native/model work). P50: public R12 aggregates verified against blob
  c036e8e2; P46a counts and all printed differences/recoveries consistent within rounding; comparator-gap recovery 0.797 (rounding range
  0.7963-0.7977), 0.613 of the original open absolute error, residual MAE difference 0.283. P49 applied. Victor chose to close the review after R13;
  no ROUND14 prompt. P35 explanatory campaign closed; liquid conformer distribution and any production geometry rule remain unresolved; 630 + 6
  profiles frozen.

- Round 14 prompt (2026-10-08): after the R13 closeout Victor asked whether anything could still beat the rivals; the review reopens on the main
  question (VLE electrostatics / first-principles permittivity), not on P35. No budget or protocol change is registered by this note.

Round 14 adopted at 2026-10-08T10:51:15Z

- Round 14 (Astra report docs/astra/round14/ZCOSMO_ROUND14_REPORT.md, received 2026-10-08). Victor chose "register all, run P51 then P52". The five
  patches (P51, P52, H14, P53, REG14) are applied unchanged to 864aaac in this commit. Verified before adoption: patches apply; r14_selftest passes;
  the pinned CRC permittivity TSV (CalebBell/chemicals e790475) downloads with Git blob bf12ffba; the association-dispatch finding is confirmed
  in source: since 2bef48f (P6, 2026-09-28) Z0xBinary.lngamma calls _analytic in the interior and _endpoint under P28, bypassing the _g override
  of Z0wBinary and its descendants. Archived Z0w/Z0w2/Z0w3 predictions (2026-09-25/26) predate it; fresh association predictions on current main
  are quarantined until a separately registered repair. The P52 archive is results/p6/Z0x__vle__all.csv (the accepted P6 Z0x run, 2026-09-28).
  The Astra text below is adopted verbatim.

R14-P51-P52-P53: exposure, dielectric ingredient, and oracle diagnostic

Proposed text. Append this complete text to PREREGISTRATION.md and commit it
with the three reviewed helpers before acquiring the reference, computing an
ingredient score, or freezing the oracle plan. Record the actual adoption time.
Base: 864aaac1e85eda31a43f24e856770c7f56ccb760. This is a new main-question
investigation, not a reopening of P35 or the R8/R9 numerical-gradient campaign.
All 630 primary and six S1/S2 profiles remain frozen. No production model or
experimental reference value is adopted. The R13 closeout remains historical.

P51 is E read-only source acquisition and ingredient analysis. P52 is an A,
experimental-input, retrospective explanatory VLE diagnostic, with E integrity
checks. P53 is E reporting. R14 authorizes zero new SCF attempts, zero quantum
gradients, zero conformer searches, zero new molecular-dynamics steps and zero
paid or cloud jobs. Real data operations occur only on the private Mac. No
raw UD data, dense profiles, row-level predictions or private paths enter Git.
The helpers upload nothing. Synthetic software tests may run elsewhere.

Exposure precedes scoring. The original 20-percent compound split and the
2017-2019 temporal collection have both been examined repeatedly. Retain their
historical identities, but do not describe them as newly untouched. P35's
142 observations and its structural follow-ups remain exposed. Excluding them
cannot restore blindness to the previously examined aggregate scorecards.
The public CRC-derived dielectric table is a different measured property,
not a verified independent laboratory sample. Its schema and some values,
including the approximate water/methanol discrepancies, informed this design.
No systematic comparison of the complete stored epsilon table with it has yet
been performed in this review. Record hashes of the public registrations,
progress log, main7/temporal scorecards, manuscript and closeout records in the
exposure receipt. Private queue histories and every collaborator's past
exposure have not been exhaustively audited. This receipt does not certify a
new holdout. Only the exposed retrospective oracle is authorized.

Acquire exactly the liquid-permittivity TSV from CalebBell/chemicals commit
e79047588b30cfabc564c79fb26d760c746877d7, path
chemicals/Electrolytes/Permittivity (Dielectric Constant) of Liquids.tsv,
Git blob bf12ffba51b478a021acc6ed58778c04deb9b988. Preserve its bytes and record
SHA256. One request, 30-second socket timeout, maximum 2 MB, no automatic
retry or alternative reference source. A failed request retains a receipt;
rerunning into an existing directory is forbidden. Store the reference and
all outputs privately outside any Git checkout.

Use all entries of the current results/qc/dielectric.csv, including failed
entries in the coverage accounting. Resolve an exact InChIKey through the
existing data/processed_ext/ud_complist.csv to exactly one checksum-valid CAS.
Require that CAS to map to exactly one project key and one reference row.
No names, connectivity-only fallback, racemate substitutions, or selected
synonyms resolve an ambiguous dielectric identity. Missing identity or
reference values are explicit coverage outcomes, never zero error.

The reference state is 298.15 K. Use A+B*T+C*T^2+D*T^3 only inside the source's
stated Tmin/Tmax range and when A and B are present. Missing higher-order C/D
coefficients are zero as in the documented polynomial representation. Otherwise
accept only a tabulated point within 0.10 K. Do not extrapolate, rescale a
293.2 K value to 298.15 K, infer a temperature from its chemical name, or use
optical permittivity as static permittivity. Values must be finite and >=1.
If any reference-matched entry has an invalid stored epsilon, withhold a
complete aggregate rather than silently removing it. Report the entire
population and the reason-specific coverage counts. The retained reference
state is the liquid state described by the compilation, not proof of a
stable ambient-pressure liquid for every compound in the portfolio.

Freeze input and helper hashes, installed numerical package versions and the
exposure receipt before computing P51 outputs. Metrics are equal-compound mean
and median absolute log epsilon error, signed log bias, mean and maximum
relative epsilon error, and mean absolute error in f=(epsilon-1)/(epsilon+0.5).
These metrics assess an ingredient. They are not an estimate of VLE error or a
gate accepting the existing Onsager approximation. Checks of saved inputs and
arithmetic may be repeated without new scores from a changed recipe.

For a possible future physical pilot, the fixed four liquids are water,
methanol, acetonitrile and benzene, identified by r14_dielectric.PILOT. A new
candidate must independently pass its separately registered dipole/sampling
validation and have complete reference coverage on all four. Prespecified
ingredient criteria are mean absolute log error <=80 percent of the same-panel
Onsager error, mean absolute f error <=0.02, maximum relative epsilon error
<=25 percent, and no individual absolute log-error deterioration >0.05.
These are engineering pilot criteria, not a confidence interval or a license
to fit g to measurements. The helper's Boolean validation inputs are not a
substitute for the actual physical receipts. No candidate-generating protocol,
MD run, dipole training or production rollout is authorized here. Those need a
new registration with reproducible model files and numerical validation.

P52 uses an operator-designated original Z0x VLE prediction archive containing
c1,c2,T,x1,P,pred_P,split. Hash it in its entirety. Query identities are original
file-row ordinals bound to that hash, not names. Restrict to its original
test_one/test_both rows, 250-450 K, 0<P<=500 kPa, strict interior compositions
1e-4<x1<1-1e-4, finite positive archived prediction, and P51 references for
both components. Do not select by observed error, hydrogen-bond class, epsilon
error, or hoped-for improvement. All exclusion reasons are counted. This is an
explicitly reference-covered, exposed subset, not the original main7 common set.

Select at most 100 unordered binary systems by SHA256('R14-oracle-v1|'+system).
Within each, retain at most ten eligible observations under SHA256 of the
original file-row identity. Preserve ordered component representation and the
original temperatures and compositions. Freeze the resulting identities and
actual counts. The maximum is 1,000 observations, with three arm requests per
observation, hence 3,000 activity-model API calls. These counts do not denote
internal segment iterations. A smaller eligible universe is reported as such.

Use the original UD profiles, unchanged, for all three arms. Record the exact
profile paths resolved by the existing exact-key/unique-connectivity rule and
provide both profiles explicitly in a private per-worker overlay. Keep the
explicit dielectric CAS policy stricter than that historical profile policy.
Protect hashes of exactly 630 profiles_v2, one S1 and five S2 files. Freeze the
Z0 parameter, dispersion and dielectric tables, the compound table used by the
existing vapor-pressure provider, all current zcosmo Python sources, the new
helpers and installed package versions. Source or input drift stops execution.

Freeze pure-component vapor pressures through the existing zcosmo.scope.psat
function using its InChIKey interface. Its output and the archived experimental
pressures are kPa. These same positive finite values enter every arm. This
preparation invokes the existing property provider, but no activity model.
Changed pure vapor-pressure inputs are not part of the epsilon intervention.
Archive the frozen values privately with the plan.

The three arms are current Z0x with its stored epsilon, current Z0x with the
P51 experimental epsilon at 298.15 K, and COSMO-SAC 2010. The experimental values
remain constant with temperature, just like current Z0x's stored table; this
is not an epsilon(T) experiment. Replace only the instance's two epsilon
values before any query, leaving its volume-fraction mixing rule and its
composition derivative intact. Clear its instance mixture cache. Do not
replace only c_ES while accidentally retaining an old dc_ES/dx. Enable P28
identically, though the selected rows are outside the endpoint strip. All
Z0/HB/London constants and input profiles remain unchanged. This experiment
does not change the meaning of a fit-free production model: its experimental-
epsilon arm is expressly NOT fit-free and can never be adopted by this result.

Before the experimental-epsilon or COSMO-SAC arm starts, reproduce every
selected archived Z0x pressure with the current stored-epsilon baseline at
relative difference <1e-7. Require finite coverage on every selected identity.
A mismatch blocks both later arms. A historical source-version or property-
provider discrepancy requires a separate reproduction decision, not a relaxed
gate after seeing the oracle. A blocked run is not evidence against the
permittivity hypothesis. No old scorecard or historical endpoint result is
overwritten.

Use one fresh subprocess for each ordered pair and arm; preserve selected
row order within that process. Clear inherited ZC_* settings before creating
the model. Each attempted query has a prewritten receipt. All requested jobs
have terminal records, including blocked and unstarted ones. Each subprocess
has 120 seconds; the serial Mac driver has 7,200 seconds including orchestration,
with a five-second process-kill allowance rather than additional scientific
compute. At most four OpenMP threads and one BLAS thread. No second claimed
run, retry, resume, alternate outcome directory or automatic budget extension.
Independent jobs continue after another fails within the remaining allocation.

The private oracle plan is bound to a committed SHA256 in
 docs/astra/round14/ORACLE_PLAN_SHA256.txt
before the first activity call. The registration and plan commits must be
ancestors of the execution checkout. The registration checker also verifies
the exact three helper files against their committed registration versions.
Do not change the helpers between an accepted registration and execution.

Require every requested new prediction to be finite before issuing complete
aggregate errors. Do not select a favorable finite intersection. On the fixed
subset report row-weighted AAD and signed pressure bias, equal-system AAD,
paired oracle-minus-baseline AAD, residual oracle-minus-COSMO-SAC AAD, and
improved/worsened counts. A signed comparator-gap recovery is reported only
for a positive baseline-minus-COSMO-SAC AAD gap above 1e-6 percentage points;
it is not clipped. Report all outcomes, including worse scores. No inferential
confidence interval or production-acceptance threshold is attached to this
exposed explanatory sample. The old 14.15/8.62 main7 comparison is not used as
the denominator for this newly selected sample.

Only the allowlisted aggregate error summary, after separate operator review,
is eligible for publication. Per-row predictions, parameter inputs, detailed
receipts and logs stay on the Mac. The independent check recomputes the saved
arithmetic and hashes without any model calls. No favorable oracle outcome
selects a physical recipe, fits a constant, authorizes 740 liquid simulations,
or grants a new confirmatory look at an old split. An unhelpful result supports
writing up current limitations; a helpful result identifies limited headroom
under this particular closure, not a rigorous upper bound.

P53 records a dielectric-development status separate from P35. Retain all
original benchmarks with their actual common subsets and their exposure.
A new physical variant needs an independently verified field/dipole model,
finite-size and sampling tests, and a genuinely unexposed custodian-frozen
validation source or an explicitly exposed fixed-design confirmation. The
current Z0w inheritance/dispatch concern is a source-version audit item; no
association code or historical failure is changed under R14. No fourth
association fit or simulation-based activity-coefficient campaign is authorized.

- R14 amendment P52a (2026-10-08, before any P52 plan or model call). The registered P52 freeze stopped with "protected profile count differs in
  s1_stalled" (zero model calls). On the Mac, data/pyscf_sigma/s1_stalled holds 6 files and s2_stalled 5: the registered 630+5+1 population is a
  per-key selection (scripts/r4_common.selected_profiles, used since R4), not every *.sigma file in those folders, which also hold superseded
  copies. P52a changes only scripts/r14_oracle.py protected_profiles() to fingerprint exactly that selection and require the 630/1/5 split.
  No selection, metric, budget or interpretation changes. Because the helpers are bound to their registration commit, P51 (deterministic,
  zero-model) is re-executed once under this commit into a fresh directory; the first P51 output under 834b929 is retained and both are compared.

- Round 14 RESULTS (recorded 2026-10-08; registered 834b929; amendment P52a c782585; oracle plan e0f1608; Mac jobs 407-409; 0 SCF).
  P51: 742 stored eps; 248 matched to the pinned CRC table (181 CAS absent, 173 key->CAS missing/ambiguous, 135 no 298.15 K value, 5 invalid
  stored eps). The 5 invalid values withhold the registered complete aggregate. Descriptive census of matched rows: reference eps < 10, 175 rows,
  mean log bias +0.53; eps >= 10, 73 rows, +0.04. P51 was re-executed under c782585 with identical rows.
  P52 (one run, 100 systems / 963 rows by fixed SHA order, 2,889/2,889 finite requests, 198 s; baseline replay exact): VLE AAD stored-eps Z0x
  13.78%, experimental-eps Z0x 13.07%, COSMO-SAC 2010 10.44% on the same rows; experimental eps recovers 0.72 of the 3.35-point gap (21%);
  559 rows improved, 404 worsened. Registered reading: small lever; no portfolio permittivity campaign. Association-dispatch defect recorded
  (fresh Z0w* predictions on current main quarantined). Nothing adopted.

Round 15 adopted at 2026-10-08T12:01:37Z

- Round 15 (Astra report docs/astra/round15/ZCOSMO_ROUND15_REPORT.md, received 2026-10-08). Victor chose "register all, run P54". The five patches
  (H15, P54, P55, P56, REG15) are applied unchanged to 3cd0a22 in this commit. Verified before adoption: patches apply; src/zcosmo/z0x.py is
  byte-identical; every historical manuscript table row is preserved apart from the scoped Z0x label; r14_selftest passes; all 34 r15 tests pass when
  run individually in the container (as a single suite, 5 error there with a NumPy 2.4.4 "cannot load module more than once" import-isolation
  artifact; the suite is re-run on the Mac before P54). The R14 private plan/run used by P54 are the P52a ones (oracle-plan-p52a, oracle-p52a).
  P55 changes association dispatch only; no association score is authorized. The Astra text below is adopted verbatim.

R15-P54-P55-P56: contact attribution, association dispatch, and manuscript scope

Proposed text, not an adoption or execution record. Append this complete text
with the actual adoption time to PREREGISTRATION.md and commit the reviewed
helpers, association repair and manuscript edits before any real-data plan is
prepared or any new output is used. Reference main is
3cd0a22888b40699d5f4994f5ba2e5cd274703df. This design follows the inspected R14
results, including P52a, and has no claim to a new held-out validation set.
Earlier registrations and results, P35's closeout and the R8/R9 numerical-gradient
closure remain unchanged. The 630 primary and six selected S1/S2 open profiles
remain frozen. There is no new QC, molecular-dynamics or conformer budget.

P54 is an A fitted-ingredient explanatory intervention with E same-input and
finite-game accounting checks. It is retrospective ThermoML scoring. A fitted
constant is never adopted, optimized or selected from these results. No hybrid
corner becomes a new production model even if its error is smaller. No optional
parameter sweep, favorable ordering, alternative subset or accuracy-based
stopping rule is introduced.

Use exactly the completed private P52 plan and its 963 observations in 100
unordered binary systems. Require its actual committed digest, completed
2889-request receipt, exact baseline replay and original immutable input hashes.
P52a's protected selection is profiles_v2=630, s1_stalled=1, s2_stalled=5. Preserve
the superseded source files as well; do not delete, merge or regenerate them.
Query identity remains the original file-row identifier from P52, including
its ordered components, T, x1, experimental pressure and frozen pure pressures.
Do not reconstruct the selection from a current CSV or a rounded result table.
The baseline is stored-epsilon Z0x, not the experimental-epsilon oracle.

There is one explicit source-version bridge. P55 modifies only z0w.py, which
neither P52 nor P54 invokes. If that file's archived source hash differs at the
current checkout path, require its archived SHA256 to match the original bytes
at this reference main and its current bytes to match the R15 registration.
Record both hashes. All other archived scientific inputs and participating
sources must still match exactly. The original R14 checker is not altered or
claimed to have accepted changed inputs. The new adapter independently checks
P52's saved result identities, accounting and aggregate arithmetic. Original
exposure receipts remain historical records, not live claims that public
reporting documents have never subsequently changed. The current Z0x, cosmosac,
zmodel and model-registry sources and the Z0/dielectric/dispersion tables must
also match reference main; source paths in another worktree do not authorize
changes to the executing model.

The nominal five players are electrostatic closure, HB constants/rule,
London/dispersion, effective area, and profile convention. In these exact
endpoints only the first three differ. Both use the same UD bytes and the
same stored NHB/OH/OT convention, sign mask, aeff=7.25, q0=79.53, r0=66.69 and
z=10. Treat effective area and profile convention as dummy players. Their zero
contributions concern this endpoint difference, not their physical importance.
Any unexpected difference in a shared ingredient fails preparation, rather than
creating a new physical intervention after the results.

Bits are E,H,D. E=0 retains the complete Z0x composition-dependent c_ES rule
and its dc_ES/dx term. E=1 uses the 2010 composition-independent coefficient
A_ES+B_ES/T^2, including its original temperature dependence and dc_ES/dx=0.
Do not change only _c while retaining Z0x's old composition derivative.
H=0 uses the existing Z0 OH-OH/OH-OT/OT-OT constants, without recomputing the
dimer matching after another bit changes. H=1 uses the 2010 constants. The
opposite-sign contact mask and stored profile split are identical; no separate
cutoff or profile reprocessing is introduced. D=0 retains Z0's London term.
D=1 disables explicit dispersion, as in the repository's COSMO-SAC 2010 target,
not COSMO-SAC-dsp 2014. It must change the London mode as well as use_dsp because
the current London branch runs before the use_dsp test. The all-one parameter
object must equal Params(use_dsp=False).

Evaluate the eight unique corners once per observation. Lift these to all
32 nominal five-player corners by exact reuse of the two dummy factors; no
extra model calls are required. The budget is 8*963=7704 lngamma requests.
First run both endpoint controls, 000 and 111, for all 963 observations:
1926 requests. Both must be finite positive pressures and reproduce P52's
stored-epsilon Z0x and 2010 pressures to strict relative difference <1e-8.
They also preserve P52's already-passed historical P6 baseline audit. Failure
of either fresh endpoint blocks all six intermediate corners, retaining
requested identities and the failure receipts. No tolerance is relaxed.
If both pass, run all six intermediate corners, 5778 further requests.

No activity solver, scientific parameter, profile, vapor pressure or dielectric
table is regenerated. Use the unchanged segment solver and Z0x interior
derivative. Enable P28 consistently, though every selected x1 is outside its
endpoint strip. Clear inherited ZC_* switches and supply explicit private
profile overlays for both components, preserving the historical exact-key or
unique-connectivity profile selection. Missing profiles cannot fall back to
another source. The explicit profile grids must match the expected 153 rows
and common sigma grid. Each ordered pair/corner is a fresh process; its rows
keep P52 order. Actual ordered-pair job count is computed from the plan, not
assumed equal to the unordered-system count.

Real preparation, execution and collection occur only on the asset-bearing
Mac, outside CI and Git checkouts for outputs. Preserve the R14 installed
numerical environment, all reused data hashes and the new code hashes. Commit
only the private plan's SHA256 in docs/astra/round15/PLAN_SHA256.txt before the
first model query. Registration and plan commits must be ancestors of the
executing HEAD. Private plans, paths, UD data, overlays, dense profiles,
row-level predictions and logs are never uploaded or written into Git.
The helper has no upload operation and no production-profile writer.

The driver runs serially with four OpenMP threads and one BLAS thread. Each
worker has at most 120 seconds, within a 7200-second model-run allocation. The
five-second process-kill/accounting allowance is not extra scientific compute.
Post-run read-only validation time is reported separately. Every planned job
has a terminal record even if blocked, unstarted or interrupted. An attempt
receipt is written before each model query. A permanent exclusive claim binds
a plan to one run. No retry, resume, stale-claim removal, second output run,
free-tier cloud dispatch or paid resource is authorized. All completed and
unfavorable results are retained. A failed or nonfinite corner withholds the
complete-panel attribution; no smaller finite intersection is selected.

At each row compute signed percent pressure error and absolute percent pressure
error from the fixed experimental pressure. The Shapley game value is negative
absolute error, so positive contribution means absolute error removed. Also
report signed-bias contributions separately. Compute all five-player Shapley
values and independently verify equality to the three-active-player result,
zero dummy contributions, and efficiency per row to <1e-8 percentage points.
Check inclusion/exclusion interactions and the signed-bias identity to the
same bound. Invalid derived arithmetic blocks complete aggregation.

Publish all eight corner AADs and signed biases, plus improved/worsened counts,
row-weighted and equal-system errors, all five signed factor contributions and
all seven nonempty active-factor inclusion/exclusion interactions. These are
fixed algebraic summaries, not choices among different primary metrics. Report
one-at-a-time substitutions alongside Shapley rather than replacing them with
whichever looks favorable. Gap shares are signed, unclipped and withheld when
the baseline-minus-2010 gap is <=1e-6 percentage points. Shares need not fall
inside [0,1]. Interaction allocations are conditional on this intervention set
and loss function, not unique physical causal percentages. No new inferential
confidence interval, global accuracy claim or production-acceptance threshold
is attached to this exposed sample. The earlier epsilon-oracle recovery and
new ES attribution overlap and must not be added as independent effects.

The complete public output is the explicit aggregate error allowlist after
separate operator review. All row data remain private. The independent check
reconstructs summaries and verifies receipts without another model request.
Checks may be repeated, but a claimed scientific run may not. After completion
or failure, archive the outcome without an automatic native continuation.

P55 is an A numerical correction relative to defective current-main association
predictions, with an E software-restoration comparison to the historical
full-_g finite-difference prescription. Add only a Z0wBinary.lngamma override
that differentiates self._g at the old H=1e-4 and returns g+(1-x)g' and g-xg'.
Z0w2 and subclasses preserving this method inherit dynamic _g/_ga dispatch.
The optimized Z0x implementation is unchanged. The historical one-sided endpoint
error remains; P28's exact Z0x endpoint must not be claimed exact for association.
No site strength, _solve_X tolerance, pure reference, temperature interpolation
or physical association architecture changes. The inherited Z0w3 implementation
is not in current src and is not certified by a generic descendant test.

Software acceptance requires tests on Z0w, Z0w2 and synthetic descendants with
nonzero added g, at interior and endpoint-strip boundaries and both pure
endpoints, with P28 both off and on. Compare to the explicit historical stencil
to 1e-12 in synthetic ln gamma, test nonzero association mass action with synthetic
strengths, and keep Z0x endpoint/corner outputs unchanged. Test the full-G identity
and the retained O(H) endpoint error explicitly. These are code regression checks,
not the 25-molecule/2302-row profile gate or a new ThermoML acceptance result.
No fresh Z0w-family experimental scoring is authorized. The recorded historical
association failures predate P6 and remain untouched. Further association work
requires an independently defined reference-energy partition and site-model
validation; switching off the explicit COSMO HB term was already done.

P56 is E reporting. Update manuscript scope and historical version labels,
acknowledge inherited constants/profile conventions and empirical upstream
inputs, add the accepted-but-exploratory v2 profile history and corrected-gradient
limitations, and record the R10-R13 glycol result with P46a and the tetraEG
exception. Include P51's withheld aggregate and the completed P52/P52a oracle
on its own 963-row subset, preserving rounding and exposure qualifications.
Retain historical numerical tables and failures; do not claim P54 has run when
its code is merely committed. The paper may be finalized with its completed
evidence; references and artifact availability still require a submission audit.
No universal fit-free contact coefficient or successful new architecture is
established or adopted by this record.

- Round 15 RESULTS (recorded 2026-10-08; registered 67f8493; plan 3655e11; Mac job 411; 0 QC). P54: 7,704/7,704 finite requests in 722 s on the
  963 P52 rows; anchors replayed exactly. Corner AADs: Z0x 13.78%, ES->2010 12.63%, HB->2010 13.97%, London removed 11.76%, all three (COSMO-SAC
  2010) 10.44%. Shapley shares of the 3.35-pp gap: London->none 2.24 pp (67%), ES closure 0.88 pp (26%), HB constants 0.23 pp (7%); a_eff and
  profile convention exactly 0. Fitted-ingredient diagnostic only; no corner is a model. P55 dispatch repair and P56 manuscript scope applied.

Round 16 adopted at 2026-10-08T13:53:21Z

- Round 16 (Astra report docs/astra/round16/ZCOSMO_ROUND16_REPORT.md, received 2026-10-08). Victor chose "register all, run LV1 screen". The five
  patches (H16, P57P58, T16, P59, REG16) are applied unchanged to ca5c7e9 in this commit. Verified before adoption: patches apply; r16_selftest
  (58) and r14_selftest (45) pass in the container; git diff --check clean; src/zcosmo, results/qc and results/z_params untouched. LV1 reduces
  exactly to the old London Margules term for equal volumes (checked algebraically). The P54 inputs are the R15 private plan/run
  ($HOME/zc-r15-contact-20261008); the negative LLE archive is the original results/predictions/lle_negatives.csv in the main Mac checkout.
  The Astra text below is adopted verbatim.

R16-P57-P58-P59: London audit, one LV1 screen, and P54 reporting

Proposed registration, not an execution or adoption record. Append this text
in full to PREREGISTRATION.md and commit it with the four R16 scripts before
freezing a private R16 plan or using a new real-data result. Record the actual
UTC adoption time. Reference main is ca5c7e94627fcdebbf787afb688f8cab10e42a03.

P57 is E source/algebra reporting and a read-only audit of the original London
inputs. P58 is exactly one A dispersion approximation, with E algebraic reuse
of the unchanged Z0x calculation. P59 is E manuscript reporting. None modifies
the production model registry, any source in src/zcosmo, a stored physical
parameter, the UD input convention, or the 630 primary plus one selected S1
and five selected S2 profiles. P55 and all preceding failure records remain.
P35 and the numerical-gradient campaign remain closed.

The new candidate is named R16-LV1-cohesive-density-SK-volume-regular-solution.
Only this candidate and the unchanged stored-epsilon Z0x baseline are evaluated.
The already saved P54 COSMO-SAC 2010 pressures are a comparator, not a new
candidate. London deletion, a fitted corner, a weight change, another combining
rule, an alternative damping prescription or a surface-fraction variant is
not an authorized follow-up when a result is unfavorable.

The scientific choice is explicitly informed by P54's exposed dispersion
attribution. It is frozen before any LV1 molecular prediction or score. There
is no claim that the old compound split or temporal collection becomes an
untouched holdout. The new primary VLE comparison uses the identical 963 P54
observations in 100 unordered systems. The temporal collection is not rescored.
The original input-covered test_one/test_both IDAC and HE observations and
LLE positive observations are guard collections. The saved 336-state negative
archive supplies its input-covered original test_one/test_both subset. These
collections are previously inspected, and their exposure is part of the result.
No custodian-held, unexposed validation source has been certified here.

Physical definition of LV1

Use the existing molecular C6_ii and alpha_i from results/qc/dispersion.csv,
with exactly their existing identities and values. Use the unchanged historical
UD cavity volume V_i. All quantities must be finite and positive. No new D4
call, geometry, charge, molecular response calculation or experimental cohesive
energy is used. The temperature dependence of these inputs remains fixed.

Convert V_i in A^3 to diameter d_i=2*(3*V_i/(4*pi))^(1/3)/BOHR_A. Define the
positive self-contact magnitude u_i=C6_ii/d_i^6*HARTREE_KCAL in kcal/mol. Use
the existing Slater-Kirkwood cross coefficient:
C6_12=2*C6_11*C6_22/[(alpha_2/alpha_1)*C6_11+(alpha_1/alpha_2)*C6_22].
Its normalized spectral factor is kappa=C6_12/sqrt(C6_11*C6_22).

Keep z=10 and the dispersion weight exactly one. Define cohesive quantities
c_i=5*u_i/V_i, c_12=kappa*sqrt(c_1*c_2), and K=c_1+c_2-2*c_12. For mole fractions
x_i define Vbar=sum(x_i*V_i), phi_i=x_i*V_i/Vbar. The new molar excess dispersion
free energy is gV=Vbar*phi_1*phi_2*K (kcal/mol). Its exact component contributions
are ln_gammaV_1=V_1*phi_2^2*K/(R_KCAL*T) and
ln_gammaV_2=V_2*phi_1^2*K/(R_KCAL*T).

This follows by assuming a random homogeneous cohesive-energy density
-(phi_1^2*c_1+2*phi_1*phi_2*c_12+phi_2^2*c_2) and subtracting its linear pure
references. That density and cross normalization are declared approximations,
not uniquely implied by the molecular C6 descriptors. The original sphere
self-energy and coordination approximations remain. In particular, the model
does not solve shape, finite-contact damping, many-body polarization or the
cohesive-energy scaling of long chains. It is a thermodynamically defined,
no-new-benchmark-regression test, not a universally first-principles liquid model.

Do not add another combinatorial or Flory-Huggins entropy term. Keep every
existing residual interaction, epsilon value, composition derivative and
COSMO combinatorial constant unchanged. No pure vapor pressure is changed.
For equal cavity volumes LV1 reduces to the existing London Margules term.
For unequal volumes it need not reduce either component contribution or total
pressure. Its failure on one property is not grounds to choose a different
normalization or a favorable chemical subgroup.

Numerical implementation and checks

The baseline London free energy is gL=5*w*x_1*x_2. Both this term and gV are
independent of the electrostatic coefficient. Query unchanged Z0x once and
add the derivative of (gV-gL)/(R*T) to obtain LV1. This is exact reuse of the
stated two models, not physical E-equivalence of LV1 and London. Enable P28
for both arms. Preserve the base's adjacent finite-difference strip exactly:
there, difference the scalar correction with the same h=1e-4 stencil. Do not
silently upgrade that strip or create an exact association endpoint.

Portable tests must pass before a plan is frozen. They verify positivity and
label symmetry, the old exchange decomposition, identical/equal-volume limits,
Gibbs-Duhem, derivative consistency, the HE temperature convention and one-call
reuse. Tests involving the actual unchanged segment solver use synthetic
profiles. Tests of native, Mac and prior-run adapters are labeled as mocks.
No source module-cache clearing is permitted in these tests; the known R15
NumPy import-isolation artifact is not resolved by calling an incomplete log a
passing suite. Native end-to-end acceptance remains separate from portable tests.

P57 decomposes only the original exchange energy. With
q=[2*sqrt(d_1*d_2)/(d_1+d_2)]^6, the identity is
w=(sqrt(u_1)-sqrt(u_2))^2+2*sqrt(u_1*u_2)*(1-kappa)
  +2*kappa*sqrt(u_1*u_2)*(1-q).
These terms are nonnegative for positive inputs. The arithmetic implementation
checks the sum against the original formula to 1e-10*max(1,max(u_i)) kcal/mol.
They are energy terms, not fractions of experimental error or a second Shapley
analysis. The descriptor census and every per-pair quantity remain private.

Inputs and prospective plan

Run the original R15 saved-output checker on its unchanged helpers. Require
the original complete P54 plan and digest commit, its exclusive run claim,
7,704 requests, every finite corner and both replayed anchors. Preserve all
963 original observation identities, component orientation, T, x, measured P
and frozen saturation pressures. Reuse the P54 baseline and 2010 pressures.
Do not construct a new oracle selection or replace its original pressures with
values from a newer property package. Carry the P52a protected profile selection
and the existing source-version bridge forward without broadening it.

For the other properties, require the supplied IDAC, HE and positive-LLE CSV
bytes to equal reference-main data/benchmark/idac.csv, he.csv and lle.csv,
respectively. Copies at different private paths are allowed; new exports are
not. The negative archive must be the saved original 336-state input used by
the project; freeze its complete bytes and require one eligible state per
unordered test binary. It is an operator-supplied historical asset, not newly
reconstructed by negative_series(). Do not substitute a new negative archive.

Eligible guard rows retain their original split, original has_sigma decision
when present, 250<=T<=450 K, two different keys and valid physical input files.
Eligibility is decided without running a model or looking at prediction error.
Record every input-only exclusion, including missing descriptor, epsilon or
unambiguous historical UD profile. A malformed eligible observation is a
preparation failure, not a row to remove. No empty property class is accepted.
The HE sign subset must contain observations with |HE|>20 J/mol. The guard
selection is common to both arms and is fixed before all new queries.

Freeze hashes of each reused private input, all baseline source files, the new
helpers and installed package versions. Reject all baseline source/table drift
from reference main, including a changed P55 implementation. Profile identity
uses the existing exact-key or unique-connectivity UD rule, not a new chemical
name match. Each worker resolves both explicit frozen files. No fallback to
open profiles or to a different directory is allowed after a missing file.
All original private receipts remain available. Only the new plan digest is
committed in docs/astra/round16/PLAN_SHA256.txt before any new model call.

Requested evaluation and guard definitions

VLE: all 963 P54 rows, pressure in kPa from the same two saturation pressures.
Before guard-property queries start, unchanged Z0x must reproduce every saved
P54 baseline pressure to relative difference strictly below 1e-8. A failed or
missing anchor blocks the guard phase. No alternate baseline or relaxed
replay limit is authorized. All comparisons, including the stored 2010 arm,
use these same 963 observations rather than the historical main7 denominator.

IDAC: all frozen eligible test observations, with exact P28 solute index zero
at x=(0,1). HE: all frozen eligible test observations, with the existing
central temperature difference at T-0.5 and T+0.5 K. Use this same numerical
HE convention in both arms and keep each original x. The held-constant
volumes/descriptors imply a temperature-independent energetic gV; this does
not validate a physical volume(T) or epsilon(T) model.

LLE detection: preserve the positive observation identities and the original
2 K evaluation-temperature rounding. Negative states keep their recorded T.
For both arms evaluate the dimensionless total mixing free energy on the
existing log-augmented 81-point interior grid and an independently checked
161-point interior grid. Their exact union contains 181 compositions; reuse
identical nodes without rounding nearby distinct values. A detected gap means
maximum vertical distance above that grid's lower convex hull exceeds 1e-7
in g/(RT). The grids must agree for each arm and state. Disagreement or a
nonfinite grid is unresolved, never 'miscible', and blocks complete tradeoff
acceptance. This is an explicit numerical detection screen, not a global
stability certificate or an endpoint-composition score. Its baseline is freshly
evaluated by the identical convention; it does not overwrite historical LLE BA.

Positive system recall uses the original rule that more than half its retained
observations have a detected gap. Negative false-positive rate uses one state
per eligible binary. Balanced accuracy is (recall+1-FPR)/2. Keep the two classes'
denominators separate. No endpoint composition is inferred from a hull segment.
No LLE numerical result may be dropped from the acceptance denominator.

For VLE, IDAC and HE report observation-weighted AAD/MAE and signed bias;
also report equal-system averages and improved/worsened row counts. Use 1,000
paired resamples of unordered binary systems, with the seed fixed in
r16_stats.SEED. LLE resamples systems separately within its positive and
negative classes. Report two-sided 95% intervals for error differences and
use the specified one-sided 95% bounds for the gates below. These are
exposure-qualified resampling summaries, not recovered untouched-test guarantees.

All gates are required: VLE AAD change is negative and its one-sided upper
bound is below zero. IDAC and HE MAE changes and their upper bounds are <=0.
There is no positive allowed-worsening margin. HE sign correctness on |HE|>20
must not decrease. LLE recall and balanced accuracy must not decrease, with
lower bounds on their paired changes >=0; false-positive rate must not
increase, with its change's upper bound <=0. Missing data or an unresolved
numerical state is an incomplete screen, not a passed no-worsening gate.

Separately, report whether the candidate-to-2010 VLE AAD difference and its
upper bound are <=0 on the 963 rows. This is the limited 'gap closed on the
exposed panel' indicator. Passing only VLE is insufficient. Passing every gate
is success of this frozen exposed development screen, not a universal accuracy
claim or automatic production adoption. A genuinely independent validation
and an explicit later adoption decision are still required for that claim.

Cost, execution and stopping

Let NI and NH be the frozen eligible IDAC and HE row counts and NL the number
of distinct ordered-pair/temperature positive and negative LLE jobs. The new
baseline-call count is Q=963+NI+2*NH+181*NL. LV1 has no additional segment-solver
calls. The full frozen design must fit Q<=180000; otherwise preparation stops
with zero new model calls and no automatic downsampling or budget increase.
The proportional 722/7704 seconds per P54 query is a planning reference only,
not a measured R16 throughput. New LLE states may converge differently.

Execute serially on the private asset-bearing Mac, at most four OpenMP threads
and one BLAS thread. Each worker has 180 seconds within a total 21600-second
baseline-query/orchestration allocation. A five-second process-group kill
allowance is administrative, not additional scientific compute. Time closing
read-only aggregation separately. Budget is zero SCFs, zero gradients, zero
MD, no paid resource and no cloud dispatch. UD data, dense profiles, per-row
results, private plans and logs stay outside every Git checkout and are never
uploaded. Real work cannot run on a fixture or fabricated 'Mac' adapter.

Create one permanent exclusive execution claim. Write each attempt receipt
before calling the unchanged baseline. Record every job terminal state,
including blocked, budget-unstarted, failed and timed-out jobs. Independent
jobs continue within budget after another fails. There is no retry, resumption,
claim deletion or second scientific output directory. Repeated saved-output
checks are allowed with no new model calls. A complete but unfavorable run
is retained and its acceptance Boolean stays false. Failure of a query or
derived arithmetic withholds complete scores instead of taking a favorable
finite intersection. A lost data archive is not permission to recompute it.

Only aggregate errors, coverage counts, declared gate outcomes and timings are
eligible for separate human review before publication. The software publishes
nothing. P57 dense coefficient decompositions and per-row predictions remain
private. No candidate coefficient is changed after seeing a result, including
an IDAC or LLE failure. The original London model and historical records remain.

P59 inserts P54's actual results in the abstract and a dedicated manuscript
section, and updates the discussion and evidence references. It distinguishes
the one-at-a-time bias change -4.23 percentage points from the dispersion
Shapley bias allocation -4.47, without rewriting either historical table.
All R2-R14 open-profile, gradient, glycol, epsilon and empirical-input
qualifications remain. P54 is an explanatory centerpiece, not a proof that
real dispersion is absent. Finalize the paper with this evidence whether LV1
passes, fails, is operationally incomplete or is never executed. No speculative
native or new-variant campaign is made a prerequisite for writing up the study.
