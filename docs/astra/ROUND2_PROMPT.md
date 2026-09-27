Round 2 of the Z-COSMO optimisation review. Please read, in the Victor-Liang-ChE/zcosmo repo:

- `docs/OPTIMIZATION_BRIEF.md`, where the rules are unchanged
- your round-1 report, `docs/astra/round1/ZCOSMO_OPTIMIZATION_REPORT.md`
- the measured results, `docs/astra/round1/RESULTS.md`
- the corrected harness, `docs/astra/round1/patches/H0.patch`

Summary of what happened to your round-1 proposals:

- **Accepted as E.**
  - P3 (4.5×, max Δln γ 5.9e-9).
  - P1 (exact, but only 1.02× on the 25 real molecules; 2.07× on water alone).
  - P2 (exact; a correctness fix, not a speed-up).
- **Rejected.**
  - P5: 0.81×, 212 vs 143 Berny evaluations, and 2 of 25 molecules did not finish.
- **Not E, but more accurate than main.**
  - P6 fails the 1e-3 equivalence gate because main's central difference (h = 1e-4) has about 1.9e-3 truncation error near x = 0.999. P6 matches a converged small-h reference to 1e-6. It needs a registration, not a code fix.
- **Not run.**
  - P4, P7 and P8: no free GPU available.
  - The direct MLIP route was shelved by its registered gate: ln γ∞ of methanol in water came out −2.07 ± 0.66 vs +0.49 from experiment. The failure comes from the potential, not sampling. So statistical-efficiency work on it is now low priority.
- **Your harness had four bugs,** all fixed and described in `RESULTS.md`.
  - `old.T` in pandas is the transpose, not the temperature column.
  - It asserted finiteness on registered rows that are non-finite in main too. This happened in two places, snapshot and profiles.
  - Its Berny wrapper assumed `callback` is passed as a keyword, but pyscf's `optimize()` passes it positionally.

  Please run anything you propose against the actual pinned `pyscf==2.14.0` API before claiming it applies.

**Round-2 question.** The QC cost is now clearly "Berny cycles × (BP86/def2-SVP C-PCM energy+gradient)". The PCM solve is not the bottleneck. 15 long flexible chains still exceed 6 h on 4 cores even with checkpoint/resume: C16–C20 fatty acids, esters, alcohols, alkanes, and two perfluoroalkanes (the list is in `data/pyscf_sigma/v2_missing.csv`). Please:

1. Give a **measured-first profile plan**. Use `pyscf.lib.logger` timers or cProfile on one representative medium molecule (e.g. 1-octanol) to split one geometry cycle into:
   - SCF iterations × Fock build (DF-J/K, XC grid)
   - the gradient terms (DF gradient, XC gradient, C-PCM gradient)
   - Berny overhead

   Give the exact command. We will run it and send back the numbers.
2. **E-class ideas for the per-cycle cost** that keep every registered setting (BP86, def2-SVP / def2-universal-jkfit, grid level 2 with pyscf's default pruning, the project radii, C-PCM with ε = 1e9 and Lebedev 17, conv_tol 1e-8). For example:
   - a better SCF initial guess across Berny steps than what the scanner already does
   - DIIS settings
   - `direct_scf` / integral screening thresholds that are exactly equivalent at the stated tolerance
   - avoiding recomputation of the grid or the J-fit metric per step
   - OpenMP/BLAS settings for 4-core runners
3. **A-class ideas for the number of cycles,** each with a registered-acceptance plan. We already know TRIC-as-prestage was worse. Consider:
   - Berny's own settings (trust radius, initial Hessian from a cheap model or GFN2-xTB with a verified unit/projection path)
   - better starting geometries: a CREST or xTB conformer search in C-PCM-like ALPB, then choose the start by BP86 single points
   - a two-level scheme that finishes with the registered Berny convergence test
4. **GPU4PySCF on the free GPUs we have** (T4 16 GB on Kaggle, RTX 2060 6 GB, RTX 4070 12 GB). Give an exact install and a fixed-geometry equivalence test against the CPU path:
   - energies, gradients, and the surface charge vector `q` at SVP and TZVP, water and O₂ (UKS)
   - custom radii, ε = 1e9
   - float64

   State honestly which pieces (custom radii table, C-PCM gradient, UKS, grid pruning) are not supported identically.
5. **The P6 registration text:** a short, exact paragraph for `PREREGISTRATION.md` accepting the analytic derivative as a numerical correction, with the check that would be run.

Return one markdown report as before: a ranked table, then diffs against current `main` and exact commands. Mark clearly what you actually executed versus what you only reasoned about.
