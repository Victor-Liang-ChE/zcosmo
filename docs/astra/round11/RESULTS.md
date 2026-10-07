# Round 11: measured results

Reference: round 11 registered 2026-10-07 in f60722f (H11, P44, P45 and REG11 applied unchanged to 463ec1b). The private plan was frozen in 1ecca25 (plan SHA256 `b91657b7…d54e49`, in `PLAN_SHA256.txt`). One run on the Mac, queue job 396:

- Started 04:11 PDT and finished 04:21 PDT. Driver wall time was 594 s against the 22,500 s ceiling. The longest slots were tetraethylene glycol at 146 s and 128 s.
- 24 of 24 single-point slots were recorded, none was retried, and all 12 pairs completed.
- No optimizations, gradients or activity-model calls.
- Coordinates, dense profiles and raw surface tables stay private on the Mac. This file reports aggregate scalars from the allowlisted public summary.

No deviations from the registered commands. The Mac had no `.pyscf_conf.py` in the working or home directory, and `PYSCF_CONFIG_FILE` was unset.

## Same-input integrity: passed for all 12

Every fresh open-geometry repeat (R) reproduced its P25 archive (A) far inside the strict limits:

| quantity | worst case | limit |
|---|---|---|
| total SCF energy | about 7e-13 Eh | 1e-7 Eh |
| maximum raw bin | about 3e-11 Å² | 1e-4 Å² |
| normalized L1 | about 2e-12 | 1e-5 |
| net charge | about 6e-14 e | 1e-5 e |

The repeat drift in every tail term is ≤ 3e-11 Å². PCM linear-solve residuals are about 1e-16, electron-count errors are below 1e-13 e, and discarded-node charge is below 2e-11 e. So `paired_integrity_passed` is True, and the historical and current decompositions agree.

## Ordered decomposition

D = U − R is the total UD-minus-open gap. G = C − R is the coordinate term: our method at the UD geometry minus our method at our geometry. M = U − C is the method term: UD minus our method, both at the UD geometry. Tails are in Å², |σ| ≥ 0.01 e/Å².

The registered background scales come out as:

| measure | scale η |
|---|---|
| raw tail | 2.84 Å² |
| averaged tail | 1.97 Å² |
| final binned tail | 2.94 Å² |
| normalized shape (L1) | 0.359 |

| member | raw tail D / G / M | averaged tail D / G / M | final tail D / G / M | tail labels (raw, avg, final) | shape L1 D / G / M |
|---|---|---|---|---|---|
| ethylene glycol | 6.6 / 5.0 / 1.6 | 9.8 / 8.1 / 1.7 | 10.0 / 8.7 / 1.3 | geometry, geometry, geometry | 0.34 / 0.31 / 0.21 |
| diethylene glycol | 6.9 / 5.9 / 1.0 | 8.6 / 8.5 / 0.1 | 10.3 / 8.1 / 2.2 | geometry, geometry, geometry | 0.31 / 0.27 / 0.22 |
| triethylene glycol | 8.1 / 6.2 / 1.9 | 10.8 / 10.8 / 0.1 | 14.4 / 12.0 / 2.4 | geometry, geometry, geometry | 0.30 / 0.23 / 0.25 |
| tetraethylene glycol | 6.8 / 1.0 / 5.8 | 0.0 / 1.7 / −1.7 | 5.0 / 1.2 / 3.8 | method, small, small | 0.37 / 0.29 / 0.28 |
| glycerol | −4.6 / −1.9 / −2.6 | −2.0 / −2.4 / 0.4 | −2.3 / −2.4 / 0.1 | small, small, small | 0.37 / 0.26 / 0.22 |
| propylene glycol | −4.9 / −3.2 / −1.6 | −3.9 / −5.3 / 1.4 | −4.1 / −5.7 / 1.6 | small, small, small | 0.33 / 0.26 / 0.21 |
| dimethoxyethane | 1.6 / 1.1 / 0.5 | −3.4 / −3.3 / −0.1 | 0.0 / −3.1 / 3.1 | small, small, cancellation | 0.24 / 0.13 / 0.22 |
| n-nonane | about 0 | 0 | 0 | small | 0.25 / 0.15 / 0.17 |
| water (control) | 2.8 / −0.1 / 2.9 | 1.6 / 0.8 / 0.9 | 1.2 / 0.2 / 1.0 | descriptive | 0.36 / 0.14 / 0.37 |
| methanol (control) | 0.8 / −0.4 / 1.2 | 2.0 / 0.3 / 1.7 | 2.2 / 0.8 / 1.4 | descriptive | 0.29 / 0.19 / 0.24 |
| methoxyethanol (control) | 1.3 / 0.6 / 0.7 | 1.0 / 0.3 / 0.8 | 2.9 / 0.5 / 2.4 | descriptive | 0.19 / 0.11 / 0.19 |
| tetrahydrofuran (control) | 0.3 / 0.1 / 0.3 | 1.5 / 0.3 / 1.2 | 1.3 / 0.1 / 1.2 | descriptive | 0.14 / 0.08 / 0.13 |

Labels: "geometry" is `mainly_geometry`, "method" is `mainly_method`, "small" is `inconclusive_small_contrast`, and "cancellation" is `inconclusive_cancellation`.

**Registered headline labels.** No member received a geometry, method or both label for the profile gap as a whole:

- Each of the eight non-control members is `metric_dependent_or_inconclusive`.
- The four controls are `background_control_descriptive_only`.

The reason is the concurrence requirement. A whole-profile label needs the final-tail and normalized-shape labels to agree. Every normalized-shape contrast is `inconclusive_small_contrast`. The control set itself differs in normalized shape by up to 0.37 L1, which makes the shape scale 0.359. That puts the 2η threshold at 0.72, above every member's total. The registered rule is applied as written, and no threshold is revisited.

What the measured terms show, within those labels:

- **Linear glycols.** For ethylene, diethylene and triethylene glycol, all three tail measures are labeled mainly geometry. Replacing only the coordinates with the UD geometry, while keeping our open method, raises the final polar tail by 8.1 to 12.0 Å². That accounts for 79 to 87% of each final-tail gap; the method term is 1.3 to 2.4 Å². In the averaged tail, the geometry term accounts for essentially all of the DEG and TEG gaps.
- **Tetraethylene glycol** differs. Its raw-tail gap is mainly method (5.8 of 6.8 Å²), and its other two tail contrasts are small.
- **Glycerol and propylene glycol.** The geometry term carries the sign of the reversed gap: the open tail is larger, and the coordinate change lowers it by 2.4 and 5.7 Å² in the final tail. Both contrasts sit inside 2η, so they are labeled inconclusive.
- **Net charge** is unchanged by geometry. The −0.012 to −0.046 e open offset is the same at R_O and R_U, to within 0.003 e, for every member. It belongs to the method bundle, not the conformation.
- **Normalized shape.** The geometry and method terms are comparable (0.2 to 0.3 L1 each) and partly cancel. Our method differs from UD's in overall shape at every geometry, controls included, even where the polar tails agree.

What this does not establish: which conformation the liquid adopts, that the folded open geometries are wrong, or anything about IDAC error. The activity model was not run, and a profile decomposition is not an error decomposition. It is also an ordered decomposition: the reverse corner p_U(R_O) was not computed. Nothing is adopted, P35 remains open, and the 630 + 6 profiles are unchanged.

## P45, reporting: applied

In the registration commit, the README paragraph and the R10 RESULTS wording were updated: the RMSD-control language, the glycerol and propylene glycol Shapley signs, and "no new QC or model evaluation".
