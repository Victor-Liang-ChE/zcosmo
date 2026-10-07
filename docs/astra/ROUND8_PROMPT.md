Round 8 of the Z-COSMO review. Please read, in the Victor-Liang-ChE/zcosmo repo:

- `docs/OPTIMIZATION_BRIEF.md`, where the rules are unchanged
- your round-7 report, `docs/astra/round7/ZCOSMO_ROUND7_REPORT.md`
- the measured round-7 results, `docs/astra/round7/RESULTS.md`, with the data in `docs/astra/round7/data/`
- the round-7 registration, its amendments P34a and P33a, and the results in `PREREGISTRATION.md`
- `scripts/r7_*.py`, `cloud/r7/` and `.github/workflows/r7_review.yml` on `main`

Summary of round 7:

- **P32.** All 25 calibration targets converged under the original Berny predicate with grid response on and off, at a wall ratio of 1.13. The registered compatibility gate failed on its maximum COSMO-SAC-dsp change: 0.0121 against 0.01. The median change is 1.7e-4, and the largest profile differences are in flexible molecules (L1 up to 0.017). So the pilot and the six-chain stage were not run.
- **P33.** The referee resolved the omitted grid response as a real gradient error in three directions (nonane ×2, TEG ×1). There, the no-response gradient is inconsistent at τ = 1e-5 and the full-response gradient is consistent. One TEG direction stays inconsistent even with full response, at 2.2e-5. Most other directions were inconclusive because the FD ladder did not stabilize. Methanol's SCF failed.
- **P34.** Grid response changes the force by more than 1e-5 in 39 of 39 sampled primary geometries. A ±0.01 Å stress along the corrected force changes probe affinities by ≥ 0.01 in 35 of them (up to 0.66). One case never finished, so no sampling bound exists.
- **P35** is recorded: the glycol gap is unresolved.

**Round-8 questions.**

1. **The P32 gate outcome.** The compatibility gate failed by 0.002 on a single query, while everything else in the trial looked clean. Under the rules, is there any defensible next step for the six chains? Or should the project accept that the grid-response question is answered (the gradient was wrong) and the six stay flagged? If you propose a new experiment, it must be a new registration with its own rationale, not a relaxed rerun of P32. Say what it would establish that P32 did not.
2. **What P34 means for the 630 primary profiles.** Essentially every sampled geometry has a grid-response force correction above 1e-5, and its profile is sensitive at 0.01 Å. Is a corrected-gradient re-polish of the primary set warranted? If so, give a registered, bounded design on free 4-core runners (630 molecules), with a compatibility gate set before any outputs. If not, say what the project should state about the existing profiles.
3. **The P33 ladder.** Most directions were inconclusive because the Richardson sequence did not stabilize, and one full-response direction is resolved as inconsistent. What does that imply about the remaining energy-gradient mismatch, for example XC grid pruning or PCM switching? Is it worth one more registered diagnostic, or should it be documented and closed?
4. **Project status.** After seven rounds, write the shortest honest summary of what the open-profile pipeline and Z0x have and have not established, as a closing section that could go in the README.

Constraints are unchanged: free compute only, every model or protocol change registered in `PREREGISTRATION.md` before its output is used, nothing fitted to the benchmark. UD profiles exist only on the Mac, so any UD-backed check runs there. Return one markdown report as before: a ranked table, then diffs against current `main` and exact commands. Mark clearly what you executed versus what you only reasoned about. If pyscf cannot be installed in your runtime, say so and keep native claims conditional.
