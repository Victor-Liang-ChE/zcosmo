Round 9 of the Z-COSMO review. Please read, in the Victor-Liang-ChE/zcosmo repo:

- `docs/OPTIMIZATION_BRIEF.md`, where the rules are unchanged
- your round-8 report, `docs/astra/round8/ZCOSMO_ROUND8_REPORT.md`
- the measured round-8 results, `docs/astra/round8/RESULTS.md`, with the data in `docs/astra/round8/data/` (including per-call PCM and XC node counts in `data/native/*.calls.json`)
- the round-8 registration and results in `PREREGISTRATION.md`
- `scripts/r8_*.py`, `cloud/r8/` and `.github/workflows/r8_review.yml` on `main`, and the README "Current evidence" section

Summary of round 8:

- **P36** reproduced every archived R7 number with zero quantum evaluations.
- **P37** ran once, 8/8 jobs complete. The EG baseline (PCM, pruned) is full-response consistent, as in P33. The TEG baseline did not reproduce its resolved inconsistency. Its ladder stabilized (indicator 4.5e-7) with a 2.16e-5 discrepancy, but one PCM surface node with switching weight about 5.5e-13 drops out at the + displacement for h ≤ 0.008 Bohr. By the registered membership rule that makes the verdict inconclusive. The strict central differences collapse from 2.0e-5 (h = 0.004) to 4.3e-6 (0.002) and about 0 (0.001). XC grid membership was constant everywhere. The other arms did not stabilize or had the same PCM change. The explicit fixed-density PCM partial matches `PCM.grad` to 1e-13 in both cases, and CachedPCM3c matches stock PCM to roundoff.
- Per the registration, the TEG mismatch is archived as unresolved and the diagnostic budget is closed. **P38**'s README status is applied.

**Round-9 questions.**

1. **Is the archive final?** Does the P37 record (a single near-zero-weight PCM node switching on one side, with the step-size collapse of the central difference) count as the "new independent evidence or source-level correction" your R8 registration required for reopening? Answer from the code (`pyscf.solvent.pcm` switching and surface-point retention at the pinned 2.14.0) and the archived calls. If it does not, say so plainly and confirm the project should stop numerical diagnostics here.
2. **README audit.** Check the "Current evidence" section against everything now archived, including R8. Propose the minimal correction if any statement overreaches or omits a registered failure. If it is accurate, say so.
3. **Anything left that is cheap and decisive?** Only if it is zero-QC or under one free Actions job and answers a question the record leaves open about Z0x or the 630 profiles. Otherwise say that nothing further is warranted.

Constraints are unchanged: free compute only, every model or protocol change registered in `PREREGISTRATION.md` before its output is used, nothing fitted to the benchmark. UD profiles exist only on the Mac. Return one markdown report as before: a ranked table, then diffs against current `main` and exact commands. Mark clearly what you executed versus what you only reasoned about. A short report is fine if the answer is "close it."
