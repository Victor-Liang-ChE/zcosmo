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


## Addendum (2026-09-29): what we measured while you were unavailable

Please use these numbers in place of the profile plan in question 1, and take questions 2 to 5 as already partly answered where noted.

**Measured profile** (`cloud/s19/qc_cycle_profile.py`, GitHub 4-core runners, registered settings, 3 Berny cycles, cProfile cumulative seconds; raw output in `results/qc/qc_profile/`). For 1-octanol at 4 threads the total is 197.5 s. Of that, 149.7 s sits under the PCM `get_veff`, and 100.0 s of it is `df.incore.aux_e2` evaluating `int3c2e(AO pair, surface point)` again on every SCF iteration, in both `_get_v` and `_get_vmat`. The XC term (`nr_rks`) is 41.6 s, the Berny gradient step (`grad_elec`) 23.2 s, and the PCM gradient 19.6 s. The linear solve is negligible, as round 1 found. Decanoic acid at 4 threads shows the same shape: 402.0 s total, 201.5 s in `aux_e2`.

**Thread scaling is poor.** Going from 2 to 4 threads changes 1-octanol from 211.6 s to 197.5 s and decanoic acid from 419.6 s to 402.0 s, so 4 threads is only 4 to 7% faster. `getints3c` is almost all self time, so it is effectively serial here.

**P9, accepted as E.** It caches those surface integrals once per surface (packed `s2ij`, contracted with matrix products). The fixed-geometry check matches the P1 path to 1.4e-12 Eh, 2.5e-13 Eh/Bohr and 2e-13 e. On the 25-molecule gate (paired, same runner) the wall time falls from 6,009 s to 3,183 s (1.89x) with identical Berny evaluations (168 = 168), and the profile E check gives max |dp| 6.9e-9 and max |dln gamma| 1.0e-7. The patch is in `cloud/s19/p9.patch`. It is on by default now. Please profile the code with P9 on (the same command with `ZC_PCM3C=1`, the default) and tell us what dominates next.

**P3 and P1 are merged** (P1 exact but small, P3 4.5x on the evaluator). P6 is registered and accepted; it moved one LLE balanced accuracy (0.901 to 0.894) and nothing else.

**New problem you can help with: long chains hit the 100-step Berny cap and restarts do not continue the optimisation.** Seven chains (C16 to C20 acids, esters, alcohols and alkanes) reached cycle 99 on three different machines, and one needed three restarts and 10 hours in total. Our checkpoint stores geometry only, so every resume rebuilds pyberny's Hessian from its model guess and the trust radius starts over. The cures we know: (a) a GPU4PySCF pre-stage from the cycle-99 geometry (accepted earlier, and running now), and (b) nothing cheaper. Please propose an E-class way to persist and restore the pyberny optimiser state (Hessian, trust radius, history) across resumes, or an A-class start that reduces the cycles for flexible chains, each with an acceptance test as before. Check against `pyberny` as installed with `pyscf==2.14.0`.

**Questions for round 2 now:**

1. With P9 on, what is the next-largest per-cycle cost, and which of it is E-class removable (for example the XC grid evaluation, or a second int3c2e pass inside the PCM gradient)?
2. Why is the `int3c2e` evaluation not scaling with threads, and can the surface blocks be evaluated in parallel without changing any number?
3. The optimiser-state persistence question above.
4. Anything in `evaluate.binodal` that could fail silently. We audited the LLE failure path: only UNIFAC-DO had unevaluable rows (23 of 101 pairs), and the other models evaluate everywhere.

Please mark, as before, what you executed and what you only reasoned about.
