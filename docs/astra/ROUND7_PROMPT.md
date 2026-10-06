Round 7 of the Z-COSMO review. Please read, in the Victor-Liang-ChE/zcosmo repo:

- `docs/OPTIMIZATION_BRIEF.md`, where the rules are unchanged
- your round-6 report, `docs/astra/round6/ZCOSMO_ROUND6_REPORT.md`
- the measured round-6 results, `docs/astra/round6/RESULTS.md`, with the data in `docs/astra/round6/data/`
- the round-6 registration and results in `PREREGISTRATION.md`
- `scripts/r6_*.py` and `.github/workflows/r6_referee.yml` on `main`

Summary of round 6:

- **P31.** Your headline table reproduces the P27 matched comparisons. Open630 is worse than UD for IDAC (+0.05 to +0.24) and HE (+51 to +109 J/mol). VLE is within noise.
- **P28 was accepted on its numerical gate.** Maximum reference error is 2.7e-9 in all four arms, and the evaluation is 3.1 to 3.2× faster. Exact minus legacy exceeds 0.1 on 21 to 27 all-split rows, concentrated in three solvents, and on no test rows. The corrected test IDAC MAE moves by +0.0003 to +0.0004.
- **P29 bounded what the sampled conformers can do.** For EG, DEG, TEG, tetraEG, 2-methoxyethanol and DME, the UD tail lies above the sampled-conformer envelope. So no weighting of those samples reproduces UD. Populations were not computed.
- **P30 stage 1 failed its registered gate, so stage 2 did not run.** The fixed 2e-7 Eh/Bohr gate was unreachable: the FD uncertainty at the registered steps is already 6e-7 to 8e-6. The directional data are striking, though. In the three P26-censored flexible molecules (nonane, TEG, DME), the production gradient without grid response disagrees with the energy's own finite difference by up to 7e-5 to 1.1e-4 Eh/Bohr, often with the opposite sign along torsions. The full-response gradient follows the energy within about 1e-5. Methanol and EG show no such effect.

**Round-7 questions.**

1. **Is the omitted grid response the root cause of the Berny stalls?** That covers the six stopped long chains and the three P26 censored members. Design a registered, fit-free A test of the optimization itself, with `grid_response=True` on the existing SVP/DF/grid-2/C-PCM-17 path, or a fixed alternative such as a finer grid if that is the better-founded fix. Use the original Berny predicate unchanged, a fixed evaluation budget, and the 25-molecule compatibility gate already used for P15/P19. Say whether, and under what decision rule, the six chains may be re-attempted, and what would let a converged result replace a flagged S1/S2 profile. Include the cost on free 4-core runners.
2. **The P30 gate itself.** Propose a consistency gate whose thresholds are attainable at the stated FD uncertainty, fixed in advance, for any later stationarity referee. Do not tune it to the observed numbers.
3. **Does the grid-response omission matter beyond the stalled molecules?** All 630 primary profiles were optimized with the same gradient. Give a cheap, registered check, with no full re-optimization, of whether their geometries or profiles are materially affected.
4. **The conformer conclusion.** UD lies outside the sampled envelopes for the glycols. Is there a principled next step at all, given the missing UD inputs, or should the project record the glycol gap as unresolved and move on? Be concrete about what evidence would change that answer.

Constraints are unchanged: free compute only, every model or protocol change registered in `PREREGISTRATION.md` before its output is used, nothing fitted to the benchmark. UD profiles exist only on the Mac, so any UD-backed check runs there. Return one markdown report as before: a ranked table, then diffs against current `main` and exact commands. Mark clearly what you executed versus what you only reasoned about. If pyscf cannot be installed in your runtime, say so and keep native claims conditional.
