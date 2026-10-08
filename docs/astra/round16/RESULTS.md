# Round 16: measured results

Reference: round 16 was registered 2026-10-08 in 2e8e5e8, with H16, P57P58, T16, P59 and REG16 applied unchanged to ca5c7e9. Amendment P58a followed in a6fa8be, and the LV1 plan was frozen in af4ce5b. Everything ran on the Mac in queue jobs 413 to 415. There was one P58 run, with no retry and zero quantum chemistry. Row-level outputs and the P57 audit stay private. This file reports the allowlisted aggregates.

## Amendment P58a and the test record

The first freeze stopped with zero model calls, because 51 test-split HE rows have x1 exactly 0 or 1. The original evaluator, `zcosmo.evaluate.predict_he`, never predicts at a pure composition, so those rows were never in any HE score. P58a excludes exactly those rows as input-only and changes nothing else. The first private directory is retained, and the run used a fresh one.

`r16_selftest` passes 58/58 in the container. On the Mac, 2 tests error with "Worker outside claimed run". This is the R10 macOS artifact: the tests compare a `/var` temp path with its `/private/var` resolution. The real private directory is under `$HOME`, which has no such alias.

## P58, LV1 exposed tradeoff screen: complete, FAILED

| collection | queries requested / finite |
|---|---:|
| VLE | 963 / 963 |
| IDAC | 828 / 828 |
| HE | 17,146 / 17,146 |
| LLE positive grid points | 129,596 / 129,596 |
| LLE negative grid points | 23,168 / 23,168 |

There were no unresolved LLE grid jobs. The unchanged Z0x baseline replayed all 963 P54 VLE pressures exactly. Model wall time was 2,219 s, against a 21,600 s cap and a planning estimate of about 16,000 s. That was 0.013 s per request, far below the P54 average.

| property | Z0x baseline | LV1 | change | paired 95% CI | gate |
|---|---:|---:|---:|---|---|
| VLE AAD % (963 rows, 100 systems) | 13.78 | 13.13 | −0.65 | [−1.72, +0.13]; one-sided upper +0.02 | fail (bound not below 0) |
| IDAC MAE (828 rows, 204 systems) | 0.840 | 0.875 | +0.035 | [+0.008, +0.067] | fail (worse) |
| HE MAE J/mol (8,573 rows, 348 systems) | 618.6 | 632.9 | +14.2 | [+4.6, +25.1] | fail (worse) |
| HE sign correct (8,316 rows) | 0.838 | 0.834 | −0.004 | – | fail |
| LLE recall (101 positive systems) | 0.842 | 0.842 | 0 | lower bound 0 | pass |
| LLE balanced accuracy | 0.893 | 0.897 | +0.004 | lower bound −0.008 | fail (bound below 0) |
| LLE false-positive rate (128 negatives) | 0.055 | 0.047 | −0.008 | upper bound +0.016 | fail (bound above 0) |

LV1 vs COSMO-SAC 2010 on the same VLE rows: 13.13% against 10.44%. The gap is not closed.

`acceptance.passed = false`. LV1 moves VLE in the right direction, but not by a resolvable amount, and it significantly worsens IDAC and HE. Under the registered rules it is a recorded unfavorable result. It is not adopted, and no second candidate, weight change or retry is authorized.

What this means: the one theory-derived replacement for the London closure that the current scalar D4 descriptors support does not fix the term R15 identified. The London term's contribution to the VLE gap is real on these rows. A first-principles fix would need information the current pipeline does not have, such as distributed contact geometry or many-body dispersion. Any such route needs a new prospective design and budget.

## P59, manuscript: applied

In the registration commit, §3.11 adds the P54 factorial, and the abstract and discussion are updated from "electrostatics first" to "the London closure first, for Z0x". The −4.23 vs −4.47 bias wording is clarified in `P54_CLARIFICATION.md`. The LV1 result above is not yet in the manuscript.
