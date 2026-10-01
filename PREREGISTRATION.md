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
