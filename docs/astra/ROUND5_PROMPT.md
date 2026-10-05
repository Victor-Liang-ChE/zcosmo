Round 5 of the Z-COSMO review. Please read, in the Victor-Liang-ChE/zcosmo repo:

- `docs/OPTIMIZATION_BRIEF.md`, where the rules are unchanged
- your round-4 report, `docs/astra/round4/ZCOSMO_ROUND4_REPORT.md`
- the measured round-4 results, `docs/astra/round4/RESULTS.md`
- the `PREREGISTRATION.md` round-4 registration and its results entry
- `scripts/r4_*.py`, `cloud/r4/native/` and `.github/workflows/r4_charge.yml` on `main`

Summary of round 4:

- **P20 is applied.** 30 profiles changed HB-DONOR-ACCEPTOR → COOH. Raw bodies are unchanged, Z0x and COSMO-SAC 2010 are exactly invariant on all 3,252 IDAC rows, and the UD median is 0.1362. COSMO-SAC-dsp was rescored into new output names.
- **P23 closed the LLE question.** The full strict repair of all 280 unresolved calls took 2 minutes and left none unresolved: 136 refined roots and 144 gap witnesses. Gap-found equals the old upper bound (test rows 0.890, systems 0.842), so the reported LLE statistic stands. The composition-error denominator grows modestly.
- **P21 located the glycol deficit in the profile shape.** UD area or volume alone changes almost nothing (under 0.05 everywhere). The normalized 153-bin shape alone takes the 332-row panel MAE from 1.311 to 0.845. In EG, DEG, TEG and tetraethylene glycol it removes a large negative bias for alkane solutes. Water as solvent shifts just as much with the UD shape, but gets worse (1.55 → 2.07).
- **P22 identified the net charge as outlying charge.** It persists from Lebedev 29 to 59 (change under 7e-4 e), halves when the radii grow by 10 percent, and the sphere test reproduces the analytic −0.0339 e. All three registered quadrature gates (DEG, water, nonane) were inconclusive. Zero-charge projections move tail and OH/OT areas by at most 0.3 Å². Z0x still responds strongly: the mean change is 0.35 in ln γ∞, and MAE on the 859 panel rows goes from 1.783 to 1.668 (COSMO-SAC-dsp 1.184 → 1.216). For DEG as solvent this is 1.740 → 1.640, against 0.371 with the UD solvent, so it is not the glycol mechanism. Nothing is adopted.
- **No intramolecular hydrogen bond** in the open EG/DEG/TEG geometries meets the registered contact criteria (closest H···O 2.2 to 2.4 Å at about 110°). The UD geometries are not available on disk, so the open-versus-UD geometry arm could not run.

**Round-5 questions.**

1. **Where the shape difference comes from.** The deficit is in the shape of the glycol profile. Area, volume and net charge are ruled out, and the UD geometries are unavailable. What measurement now separates the following?
   - conformer: the open conformer versus whatever UD used
   - level of theory and cavity construction: our BP86/def2-TZVP C-PCM with project radii, versus UD's DMol3-style COSMO
   - the averaging and HB split

   Water as solvent moves the other way, and so do glycerol and propylene glycol. Any explanation has to account for that. Propose a measured-first, fit-free test with exact commands, on a fixed panel that is not chosen by experimental error.
2. **A conformer protocol, if justified.** If question 1 points to conformers, specify a complete A protocol before any scoring: generation, optimization level, selection or Boltzmann weighting, and handling of intramolecular H-bonds. Give its theoretical acceptance gates and a separate validation panel, its free-compute cost on 4-core runners, and how the 630 primary profiles stay frozen until it passes.
3. **Water, and the net-moment sensitivity of Z0x.** The UD water shape makes Z0x worse for water as solvent while the open one is better. Is this a property of the Z0x water treatment (the H2O flag, dispersion) rather than of the profiles? Separately, a net-charge projection that leaves areas within 0.3 Å² moves Z0x by 0.35 on average (max 1.26). Which Z0x term carries that sensitivity, and is it physically intended? Is there a theory-only (not benchmark-selected) argument for or against a charge-neutral profile convention? What check would decide each question without fitting?
4. **Reporting.** With P20 applied and P23 repaired, what is the honest primary scorecard now? Cover Z0x and the open-profile arm, IDAC, VLE, HE and LLE with repaired-status columns. Give an exact command set that regenerates it from `main` and the Mac-only UD profiles, with denominators stated.

Constraints are unchanged: free compute only, every model or protocol change registered in `PREREGISTRATION.md` before its output is used, nothing fitted to the benchmark. UD profiles exist only on the Mac, so any UD-backed check runs there. Return one markdown report as before: a ranked table, then diffs against current `main` and exact commands. Mark clearly what you executed versus what you only reasoned about. If pyscf cannot be installed in your runtime, say so and keep native claims conditional.
