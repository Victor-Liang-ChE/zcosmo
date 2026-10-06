# Round 6: measured results

Reference: round 6 registered 2026-10-06 04:4x PDT in 5926ba1 (your six patches applied unchanged to 43213a5). P28 acceptance recorded in 64c4a3b before any corrected score was computed. P31, P28 and the P29 inventory ran on the Mac (queue jobs 364 to 368). P30 stage 1 ran on GitHub Actions run 37463154483, one runner per case, with pyscf 2.14.0, pyberny 0.7.0 and RDKit 2026.03.6. Machine-readable files are in `docs/astra/round6/data/`.

## P31, headline

`r6_headline.py` reproduces the archived P27 matched comparisons exactly:

| comparison | common rows | UD | open630 | open − UD, 95% CI |
|---|---|---|---|---|
| IDAC MAE | 816 | 0.8040 | 0.9423 | [0.0506, 0.2379] |
| VLE AAD% | 12,403 | 15.90 | 16.41 | [−0.75, 2.10] |
| HE MAE (J/mol) | 8,573 | 618.6 | 699.3 | [50.9, 108.8] |

LLE on the 2,469 common rows / 100 systems: row detection 0.889 (UD) vs 0.883 (open630), system detection 0.84 vs 0.82, endpoint MAE 0.1801 on 2,140 rows vs 0.1797 on 2,125. The open profiles are a reproducible alternative input, not an accuracy-equivalent replacement for UD.

## P28, exact Z0x infinite-dilution endpoint: accepted

- Numerical gate passed in all four arms (UD, open630, open636, water stress). Coverage: 3,252 rows (open630: 3,101 checked plus 151 excluded by design).
  - Maximum error against the independent log-equation reference: 2.73e-9 (limit 1e-8).
  - The reverse, API and pure-limit checks are inside their limits.
  - Finite coverage is identical, and no row has an inconclusive second-order finite-difference control.
- Prevalence of |exact − legacy| (all split / test split):

| arm | > 0.001 | > 0.01 | > 0.05 | > 0.1 | max |
|---|---|---|---|---|---|
| UD | 391 / 68 | 58 / 10 | 40 / 0 | 21 / 0 | 0.842 / 0.029 |
| open630 | 382 / 70 | 54 / 10 | 38 / 0 | 27 / 0 | 1.137 / 0.026 |

  The large changes sit in a few solvents: YNQLUTRBYVCPMQ (30 rows, up to 0.26), IMNFDUFMRHMDMM and TVMXDCGIABBOFY.
- Timing, fresh processes, three alternating repetitions: the exact endpoint is 3.06 to 3.25× faster.
- Acceptance record (64c4a3b, gate sha256 2f3df2e2…), then the corrected score. Paired Δ MAE is small and positive:

| arm | split | legacy MAE | corrected MAE | Δ MAE 95% CI |
|---|---|---|---|---|
| UD | test | 0.8394 | 0.8397 | [7.0e-5, 7.7e-4] |
| UD | all | 0.9318 | 0.9336 | [9.5e-4, 2.9e-3] |
| open630 | test | 0.9423 | 0.9427 | [6.8e-5, 6.7e-4] |
| open630 | all | 0.9893 | 0.9916 | [1.0e-3, 3.8e-3] |

  As registered, the correction is accepted on numerical grounds, not on MAE. Historical scorecards stay unchanged and labelled as finite-difference-endpoint results.

## P29, conformer evidence inventory (no new QC)

The inventory complete flag follows the registration. Six members are complete. Four are incomplete: nonane, TEG and dimethoxyethane each have one censored member, and tetraEG has one member never run.

Populations are not computed, because no basin, degeneracy, nuclear-entropy or transfer audit exists. The sampled envelopes do settle one question. No positive weighting can leave the sampled range, and for the glycols the UD tail lies above it:

| molecule | sampled tail range (Å²) | UD | stored open | E span (kcal/mol) |
|---|---|---|---|---|
| ethylene glycol | 22.8–31.4 | 33.0 | 23.0 | 1.5 |
| diethylene glycol | 23.7–34.8 | 38.0 | 27.7 | 3.5 |
| triethylene glycol (3 of 4) | 26.5–32.7 | 42.3 | 27.9 | 2.5 |
| tetraethylene glycol (3 of 4) | 24.4–34.3 | 46.8 | 41.8 | 5.3 |
| 2-methoxyethanol | 13.7–20.5 | 23.9 | 21.0 | 3.1 |
| dimethoxyethane (3 of 4) | 9.3–10.3 | 14.4 | 14.4 | 0.3 |
| glycerol | 27.1–35.1 | 35.0 | 37.3 | 2.3 |
| propylene glycol | 21.8–29.3 | 25.9 | 30.0 | 1.4 |
| THF | 8.26–8.37 | 9.6 | 8.4 | 0.01 |

## P30, stage 1: registered gate failed, escalation stopped

All five cases completed their 18 SCF and 3 gradient evaluations. Every case fails the registered full-response consistency gate, so stage 2 (Hessians and profile stresses) did not run.

The fixed gate cannot be met with the registered steps. It requires full-response error below 2e-7 Eh/Bohr with an FD uncertainty indicator below 1e-7. The measured FD uncertainty indicators are already 6e-7 to 8e-6 at the ±0.003/±0.006 Bohr steps. No threshold or step was changed after seeing this.

The directional data show a mechanism. In the three censored flexible chains, the original (grid response off) gradient disagrees with the energy's own finite difference by up to 7e-5 to 1.1e-4 Eh/Bohr, often with the wrong sign. With grid response on, the gradient follows the energy.

| case | max FD uncertainty | max error, original | max error, full response | max gradient component, original → full |
|---|---|---|---|---|
| n-nonane (P26 censored) | 4.3e-6 | 7.4e-5 | 9.0e-6 | 1.1e-5 → 9.1e-5 |
| triethylene glycol (P26 censored) | 1.6e-6 | 1.1e-4 | 1.5e-5 | 3.9e-5 → 8.5e-5 |
| dimethoxyethane (P26 censored) | 7.3e-6 | 8.8e-5 | 3.9e-5 | 2.5e-5 → 9.8e-5 |
| ethylene glycol (R5 saved) | 8.0e-6 | 2.6e-5 | 2.2e-5 | 7.9e-5 → 7.5e-5 |
| methanol (R5 saved) | 4.5e-6 | 3.6e-5 | 3.8e-5 | 2.8e-4 → 2.8e-4 |

Examples (Richardson FD vs original vs full-response gradient, Eh/Bohr):

- nonane torsion 3-4: +5.6e-5 / −1.8e-5 / +5.3e-5
- TEG torsion 2-3: +1.0e-4 / −1.1e-5 / +8.6e-5
- DME torsion 2-3: +8.0e-5 / −7.9e-6 / +6.5e-5

The rigid controls (methanol) and EG show no comparable effect. Tightening SCF changes the gradient by at most 7.5e-6 and fixes nothing.

Interpretation, not yet an accepted result: at these flat geometries, the gradient the optimizer uses is dominated by the omitted grid-response term. That gradient points against the energy it is minimizing along soft torsions. This is consistent with the noise-dominated Fletcher ratios and trust collapse diagnosed in the six stopped chains. It also suggests the "converged" force (1e-5) understates the true one (about 1e-4).

## Deviations and notes

- The P30 workflow planned the frozen manifest on each runner and split it by job id, as REG6 allows. `r6_jobs.py run` returns "censored" (rc 2) for every case because the consistency subcommand exits 2 when its gate fails. The status files say diagnostic_complete.
- `missing_response_material` is false in all cases only because the code evaluates it only when the full-response gate passes.
