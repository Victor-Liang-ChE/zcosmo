# Round 8: measured results

Reference: round 8 registered 2026-10-06 in 333b2ab (your five patches H8, P36, P37, P38 and REG8 applied unchanged to 58cc629). The P37 plan was frozen in 54e0ebc (plan sha256 `4cad30e6…bd892`). One P37 dispatch, Actions run 37565712769, ran on the plan commit. All eight jobs completed and none was rerun. Collection and checks ran on the Mac (queue jobs 385 to 388).

One bookkeeping deviation: `plan.json` records the registration as fc898fb, the container commit, not 333b2ab. The patch was made in the container and applied on the Mac with `git am`, which rewrote the commit ID. Both commits have the identical tree, a6c0eac. The plan commits d1da8bf and 54e0ebc also share a tree, 8aa9c79. No file content differs, and the design is unchanged.

## P36, read-only evidence audit: reproduced

`r8_evidence.py` reproduces every archived R7 number from `docs/astra/round7/data` with zero quantum or model evaluations, and all of the report's assertions pass.

| item | value |
|---|---|
| P32 max dsp change | 0.012074145054630225 (limit 0.01, recorded failed) |
| P32 median dsp change | 1.66e-4 |
| P32 worker time, off / full | 2,635.7 s / 2,986.2 s, ratio 1.1330 |
| P33 | 4 complete, 3 resolved omitted-response directions, 1 full-inconsistent |
| P34 | 40 requested: 35 positive, 0 negative, 4 unresolved, 1 missing; force > 1e-5 in 39/39; no sampling bound |

Output: `data/p36_evidence.json`. No new scientific gate passed.

## P37, final stage-isolation diagnostic: baseline not reproduced, budget closed

The run was 8/8 complete, with no missing or failed identity. Total native wall time was 4,151 s. TEG arms took 653 to 1,299 s each and EG arms 62 to 113 s. The collector's `baseline_P33_pattern_reproduced` is **False**. Under the registration, no other arm may be read as removing the TEG discrepancy, and the budget closes with the mismatch archived as unresolved.

τ = 1e-5 Eh/Bohr. The steps are 0.016, 0.008, 0.004, 0.002 and 0.001 Bohr. "Error" is |FD reference − full-response directional gradient|.

| case | arm | full | off | full error | indicator | stabilizing | membership stable |
|---|---|---|---|---|---|---|---|
| TEG 3-4 | pcm_pruned (baseline) | inconclusive | inconclusive | 2.16e-5 | 4.5e-7 | yes | **no** |
| TEG 3-4 | pcm_unpruned | inconclusive | inconclusive | 1.20e-5 | 1.4e-6 | yes | **no** |
| TEG 3-4 | vacuum_pruned | inconclusive | inconclusive | 1.22e-5 | 1.4e-5 | no | yes |
| TEG 3-4 | vacuum_unpruned | inconclusive | inconclusive | 1.06e-6 | 8.4e-6 | no | yes |
| EG 2-3 | pcm_pruned (baseline) | **consistent** | consistent | 8.5e-10 | 1.3e-6 | yes | yes |
| EG 2-3 | pcm_unpruned | inconclusive | inconclusive | 2.69e-5 | 1.5e-5 | no | yes |
| EG 2-3 | vacuum_pruned | inconclusive | inconclusive | 1.47e-5 | 4.6e-6 | no | yes |
| EG 2-3 | vacuum_unpruned | inconclusive | inconclusive | 1.18e-5 | 3.6e-6 | no | yes |

**The EG baseline reproduces** P33's consistency. **The TEG baseline does not reproduce the resolved inconsistency.** Its ladder stabilized with a small indicator (4.5e-7, ceiling 2.5e-6). The discrepancy of 2.16e-5 would otherwise exceed τ by more than the indicator. But PCM surface-node membership changed along the ladder, and by the registered rule that makes the verdict inconclusive.

That membership change is specific:

- Both TEG PCM arms have 1,340 retained surface nodes at the center and at ±0.016 Bohr.
- At the + displacement of 0.008, 0.004, 0.002 and 0.001 Bohr, one node drops out (1,339). The − side keeps 1,340.
- The minimum retained switching weight in those calls is 5.5e-13.
- The XC grid membership is identical across all 22 calls in every arm, pruned and unpruned (one signature each).

Strict central differences in the TEG baseline are 2.33e-5, 2.15e-5, 2.00e-5, 4.25e-6 and −2.9e-8 for decreasing h. The difference collapses between h = 0.004 and 0.002 Bohr, and the Richardson reference is −1.46e-6. Ladders on both EG PCM arms and both vacuum arms of either case kept their membership. Every one except the EG baseline failed to stabilize within τ/4.

The SCF and full-response quadratures matched at both precisions in all eight arms, with identical node membership and weights.

The explicit PCM partial derivative at fixed AO density (two cases, 22 explicit energies and 2 gradients each) behaved as follows:

| case | layer verdict | layer error | cache/stock parity |
|---|---|---|---|
| TEG | inconclusive (membership change) | 3.1e-14 | passed (ΔE 6.9e-16 Eh, Δg 3.0e-16) |
| EG | consistent | 2.7e-13 | passed (ΔE 3.7e-16 Eh, Δg 2.4e-16) |

The explicit PCM partial derivative agrees with `PCM.grad(P0)` to 1e-13 or better in both cases. Only the TEG verdict is formally inconclusive, because of the same one-node membership change. CachedPCM3c and stock PCM agree to roundoff, so the cache is not implicated. No cache was changed or newly accepted.

Under the registration, these are the only readings allowed: the TEG arm-to-arm contrasts are not interpreted, and nothing is attributed to XC pruning, because no unpruned arm resolved. Nothing authorizes an optimizer, a 630-profile re-polish, a chain retry or a corrected-gradient default; all of the collector's `authorizes_*` flags are False. The P33 and P30 decisions are not rewritten.

Outputs: `data/p37_diagnostic.json`, plus per-arm `result`, `calls`, `layer`, `run` and `terminal` records in `data/native/`.

## P38, README closing status: applied

The short "Current evidence" section is appended to `README.md` in the registration commit, as supplied.

## State after round 8

The six S1/S2 chains stay flagged and profiles_v2 stays 630/636. No profile version changed. The diagnostic budget registered in R8 is spent and closed. Reopening the TEG mismatch requires new independent evidence, auditable inputs or a source-level correction, under a separate registration.
