# Round 2: measured results

Reference: `main` at `eab6c25` when the round-2 report was received (2026-10-04). Every number below comes from runs on GitHub Actions (ubuntu-latest, 4 threads, pyscf 2.14.0, pyberny 0.7.0) or on the Mac, and every decision is recorded in `PREREGISTRATION.md`.

## P15 (noise-aware Berny trust update, energy_noise 2e-7 Eh): run, REJECTED

Registered before any run (commit 2e9e459, 2026-10-04 01:49 PDT) with your text unchanged, plus an execution plan and a decision rule: accept only if the 25-molecule gates pass AND at least one stalled chain passes the original Berny test in the P15 arm within 100 evaluations.

- 25-molecule gate (run 37190183654): passed. 25/25 P15 geometries converged under the original test; 2302 rows with the same 31 non-finite in both arms; max |d ln γ∞| 2.15e-4 (limit 0.01); median vs UD 0.1493 (limit 0.15); paired wall 3217 s vs 3360 s (0.957); geometry evaluations 163 vs 168; max normalized-bin diff 6.5e-5, max raw psigmaA diff 0.0132 (reported).
- Long chains (run 37190177507): six frozen seeds, base and P15 arms, 100 evaluations each as two 50-step passes with the accepted state restart. All 12 arm-chains hit the cap in both passes. No chain converged in either arm.
- Before registration we read the six frozen states: predicted |dE| 5.7e-8 to 3.7e-7 Eh, trust 3.6e-4 to 5.9e-3; five of six were already below the default noise threshold at that step.
- Harness note: your `profile_gate`/compare assumes the UD reference profiles exist on the runner. They are gitignored (`data/raw/nist/UD`), so the compare job crashed; the identical H0 `profiles --mode A` comparison was run on the Mac from the run's artifacts.

## Long-chain stall rule S2 (your "orientation-aware metric" suggestion): registered, run, all six accepted (flagged)

Registered before computing (commit edac9d1). Per chain: NEW = checkpoint 100 evaluations after OLD; 8 fixed random rotations (scipy `Rotation.random(8, random_state=20261004)`); accept if gradient below Berny's limits, displacement ≤ 0.005 Å, max |d p(σ)| NEW vs OLD ≤ median rotation difference, ln γ∞ change < 0.05, and the profile differs from the chain's own xTB start by more than the largest rotation difference. Results (commit 3058802):

| chain | grad max | disp (Å) | T_med | T_max | NEW vs OLD | NEW vs xTB | NEW vs 0.02 Å nudge |
|---|---|---|---|---|---|---|---|
| BTFJIXJJCS | 3.3e-5 | 0.0009 | 0.896 | 1.275 | 5.8e-3 | 12.38 | 2.04 |
| FLIACVVOZY | 2.1e-5 | 0.0007 | 1.953 | 3.118 | 2.3e-3 | 9.30 | 1.11 |
| HPEUJPJOZX | 3.7e-5 | 0.0011 | 0.930 | 1.255 | 7.0e-3 | 12.13 | 1.47 |
| MVLVMROFTA | 3.3e-5 | 0.0018 | 0.772 | 1.587 | 1.67e-2 | 6.16 | 0.98 |
| OYHQOLUKZR | 1.9e-5 | 0.0016 | 1.144 | 1.669 | 7.6e-3 | 5.85 | 1.30 |
| PYGXAGIECV | 9.6e-5 | 0.0012 | 0.940 | 1.242 | 4.8e-3 | 3.09 | 0.82 |

Units for the p(σ) columns are max |d psigmaA| (Å²); profile peaks are about 60 to 90. ln γ∞ change NEW vs OLD: 1.4e-5 and 2.4e-5 on the two chains with benchmark rows.

**The important side finding:** a rigid rotation of one fixed geometry changes the registered TZVP profile by 0.48 to 3.1 in max |d psigmaA|, i.e. 1 to 4 percent of the peak. The single 0.001 rad rotation tested on 2026-10-01 gave only 1.6e-2, so the dependence grows with the rotation, which looks systematic (surface discretization relative to the molecule) rather than random noise. Every profile in `profiles_v2` was computed in one arbitrary orientation. A random 0.02 Å displacement also stays below T_med, so the p(σ) metric does not resolve geometry differences of that size.

## Exploratory Z0x-open, all 636 compounds (630 Berny-converged + 6 flagged S1/S2)

Test split, reference = stored Z0x predictions (UD profiles), commit b2ad606:

| | Z0x | Z0x-open |
|---|---|---|
| IDAC MAE, 828 points | 0.839 [0.705, 0.974] | 0.977 [0.841, 1.110] |
| dMAE CI | | +0.052 to +0.232 (worse) |
| IDAC bias | −0.212 | −0.368 |
| solvent-rank rho | 0.83 | 0.77 |
| LLE gap found, 101 systems | 0.84 | 0.82 |
| same, rows with the six chains removed (816 IDAC points) | 0.804 | 0.942 |

The stored Z0x reference gives 0.839 on this 828-point common subset, not the 0.800 quoted in earlier registrations; it was not regenerated.

## Not run

P10, P11, P12, P13, P14 and H2 have not been run yet. Nothing in the round-2 report was rejected without a test; they are waiting for prioritization (question 4 of round 3).
