Round 4 of the Z-COSMO review. Please read, in the Victor-Liang-ChE/zcosmo repo:

- `docs/OPTIMIZATION_BRIEF.md`, where the rules are unchanged
- your round-3 report, `docs/astra/round3/ZCOSMO_ROUND3_REPORT.md`
- the measured round-3 results, `docs/astra/round3/RESULTS.md`
- the `PREREGISTRATION.md` entries of 2026-10-05 (the round-3 registration and its results)
- `scripts/r3_*.py`, which now live on `main`

Summary of round 3:

- **P16 explained both IDAC puzzles.** The 0.800 vs 0.839 difference is a denominator: 762 common rows vs all 828. The open-profile deficit is almost entirely diethylene glycol used as a solvent, with alkane and alkene solutes. The open glycol profiles have a third less polar tail area than UD.
- **Orientation is small:** about 0.01 in ln γ∞, max 0.11. All three orientation recipes failed their registered gates.
- **P18 (the COOH flag) passed** and is waiting to be applied.
- **P19 passed every check except wall time:** 2.28× against a 1.50 limit. So the long chains were not run.
- **The P14 LLE sidecar is identical with audit on and off.** It found 223 refined roots that fail the residual check, 158 negative tangent margins, and 5 coarse-hull fallbacks.
- **A new observation:** every open profile carries a net σ moment of −0.02 to −0.04 (raw charge sum about −0.03 e), against about −0.003 for UD.

**Round-4 questions.**

1. **Glycols as solvents.** Explain why the open diethylene, triethylene and ethylene glycol profiles make Z0x so much worse for alkane and alkene solutes. Use the numbers in `RESULTS.md`: less polar tail area, less OH/OT area, smaller volume. Candidates:
   - the optimized geometry: an intramolecular O–H···O hydrogen bond in the conductor-optimized conformer, versus the UD conformer
   - the conformer choice in general
   - radii or switching around the ether oxygens
   - the HB classification and split in `to_sigma.py`
   - the net-charge issue in question 2

   Give a measured-first diagnostic plan with exact commands. Check whether the effect is specific to these solvents or shows up in other flexible polyols and ethers in the benchmark. Any fix must be a registered A change with a fixed acceptance test. Nothing may be tuned to the benchmark.
2. **Net surface charge.** Why does the pinned pyscf 2.14.0 C-PCM path give a total surface charge of about −0.03 e for neutral molecules at ε = 1e9? Consider outlying charge, the switching function, Lebedev 29, Gaussian charge widths, and the basis. Is a charge renormalization (a scale or shift onto zero total) physically justified as an A correction? How would it interact with the glycol tail-area deficit? Give a test that separates a real outlying-charge effect from a numerical defect.
3. **Applying P18.** Give the exact metadata-only relabel of `profiles_v2` (and of the flagged S1/S2 profiles) under the accepted rule, with the verification. List which stored scores must be rerun and which, like Z0x, cannot change.
4. **The six stalled chains.** P19 converged everything in the calibration and failed only on wall time. Is there any bounded convergence route left that is worth registering? Or should the question be closed, with the flagged S1/S2 profiles as the final answer? Be concrete about cost on free 4-core runners.
5. **LLE sidecar.** What do the 223 residual failures, the 158 negative tangent margins and the 5 hull fallbacks mean for the reported LLE statistics? Many involve water. Propose an E or A treatment that keeps the denominators honest, with the check that decides it.

Constraints are unchanged: free compute only, every model or protocol change registered in `PREREGISTRATION.md` before its output is used, nothing fitted to the benchmark. UD profiles exist only on the Mac, so any UD-backed check runs there. Return one markdown report as before: a ranked table, then diffs against current `main` and exact commands. Mark clearly what you executed versus what you only reasoned about. If pyscf cannot be installed in your runtime, say so and keep native claims conditional.
