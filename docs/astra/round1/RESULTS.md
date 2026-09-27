# Astra round 1: measured results (final, 2026-09-27 PDT)

Reference commit: 62172c7. The test harness H0 needed four fixes before it could run; all are in `patches/H0.patch`.

1. **Fixture always failed.** `old.T` is the pandas transpose, not the temperature column.
2. **Snapshot crashed on registered queries.** It asserted COSMO-SAC is finite for every registered query. 436 queries are non-finite in main too. They are now recorded, and `compare` requires identical coverage.
3. **Every base and P1 QC arm failed at once.** The Berny wrapper assumed `callback` is a keyword argument. `pyscf.geomopt.berny_solver.optimize` passes it positionally. P2 and P5 call the kernel with a keyword, so they ran.
4. **The profile check crashed.** `profiles()` asserted all 2,302 rows finite. 31 rows are non-finite in main. Now the candidate must have identical coverage, and only finite rows are compared.

QC arms ran on GitHub Actions (4 cores, 4 threads), one runner per molecule.

- **base and P1** (run 36317731128) ran back to back on the same runner, so their timings are paired.
- **P2 and P5** (run 36291809265) ran on other runners. Their timing comparisons against base carry runner-to-runner noise of about ±10–20%.

## Verdicts

**P1: PCM LU reuse (E). Accepted as E.**
- *Gate:* fixed-geometry check (dE < 1e-8, dG < 1e-6, dq < 1e-8), then the 25-molecule E-gate.
- *Result:* all gates pass.
  - Fixed geometry: dE ≤ 1.1e-13 Eh, dG ≤ 5.6e-14, dq ≤ 6.0e-14.
  - 25 molecules: max Δp 1.4e-8, max ΔpsigmaA 2.0e-6 Å², max Δln γ 2.7e-7.
  - Median vs UD is 0.1493, which reproduces the registered v2 acceptance value.
- *Measured speed:* 1.02× on 25 molecules (6,412 s vs 6,266 s), with identical Berny evaluations (168 = 168).
  - Water alone is 2.07×. Tiny molecules gain because the solvent-surface matrix setup is a large share of their runtime.
  - For real molecules the LU factorisation is **not** the bottleneck. The 1.6–3× hypothesis is not supported.

**P2: restart hygiene (E). Accepted as E.**
- *Gate:* 25-molecule E-gate plus the resume smoke test.
- *Result:* passes. Max Δln γ 2.7e-7. On resume, a second call is a validated cache hit (0 geometry evaluations).
- *Measured speed:* 1.06× (unpaired), with the same evaluations (168 = 168). It is a correctness fix, not a speed-up.

**P3: support-restricted safeguarded Newton (E). Accepted as E.**
- *Gate:* max Δln γ < 1e-3 with identical coverage.
- *Result:* passes. Max Δln γ 5.9e-9 over 43,934 queries (2,302 IDAC rows plus the grid), with identical coverage (436 non-finite in both).
- *Measured speed:* 4.5× across 3 single-thread repetitions on an M4 Pro. Base took 821/721/695 s; P3 took 170/168/163 s.

**P6: analytic Z0x interior derivative (E candidate). Not accepted as E; registration needed.**
- *Gate:* same as P3.
- *Result:* fails. Max Δln γ is 2.06e-3, and every excess case sits at x = 0.999 where the dilute component's ln γ is about 8–11.
  - A small-h reference shows main is the inaccurate one. For the worst case, main's ln γ₂ (h = 1e-4) is 9.600659; with h = 1e-5 it is 9.598748, h = 1e-6 gives 9.598729, h = 1e-7 gives 9.598728, and P6 gives 9.598728.
  - Main's central difference carries about 1.9e-3 truncation error there, while P6 matches the converged limit to 1e-6.
  - P6 is a numerical *correction*. It needs a registration entry before the scorecard uses it.
- *Measured speed:* 1.8× (459/449/442 s).

**P5: TRIC pre-stage then Berny (A). Rejected.**
- *Gate:* registered A test.
- *Result:* rejected. 2 of 25 molecules did not finish (decanoic acid, triethylene glycol).
- *Measured speed:* 0.81× (unpaired), with more evaluations (212 vs 143 on the 23 that finished). Several molecules got worse: 1,1-difluoroethane went from 5 to 21 evaluations, and 2-propanol from 6 to 12.

**P4, P7, P8: GPU. Not run.**
- No free GPU was available: Modal credits are exhausted until the monthly reset, and most of the Kaggle weekly quota went to the direct-route pilot.
- The direct route itself was shelved by its registered gate on 2026-09-27, which lowers the priority of P4, P7 and P8.

## What this says about where QC time goes

On these 25 molecules, time per molecule is dominated by the number of Berny cycles (4–15) times the cost of a BP86/def2-SVP C-PCM energy+gradient. The PCM linear solve is a small fraction of that cost. The 15 benchmark molecules still missing after five GitHub rounds are long flexible chains (C16–C20 acids, esters, alcohols and alkanes, plus two perfluoroalkanes). They exceed 6 h on 4 cores even with checkpoint/resume. They now run on the Mac without a time cap.
