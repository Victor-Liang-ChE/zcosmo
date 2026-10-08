# Round 12: measured results

Reference: round 12 was registered 2026-10-07 in 05c35c8, with H12, P46P47, P48 and REG12 applied unchanged to a93a1c9.

| step | commit | private plan SHA256 |
|---|---|---|
| P47 regional plan frozen | 76e3092 | `ad79e84c…ed40` |
| Amendment P46a registered | d6b7e25 | – |
| P46 factorial plan frozen | fbba5e0 | `8b985a22…a9ae` |

Everything ran on the Mac, in queue jobs 399 to 401: zero SCF calls, no optimization, and one run of each task with no retry. Profiles, row predictions and per-member regional tables stay private on the Mac. This file reports the allowlisted aggregates.

## Amendment P46a (before any P46 model call)

The first P46 freeze stopped at its own input check, with zero model calls. The registration fixed EG at 9 rows (141 total) and 14 solvent identities. The original P21 archive has 13 solvent InChIKeys under 14 names. The EG key carries 10 rows: 9 named "ethylene glycol" and 1 named "1,2-dihydroxyethane", the same molecule. The registration also said selection is "by these exact keys, not by a solvent-name synonym", so the two rules conflict on this archive.

Victor chose exact-key selection. P46a changes only the counts: 142 scored rows, 13 keys, 190 audit-only rows, and 284 legacy plus 1,278 exact requests (1,562 maximum). Every other rule, tolerance, budget and interpretation is unchanged. The record is in `PREREGISTRATION.md`.

## P46, retrospective explanatory scoring: complete

The run made 1,562 of 1,562 requests, all finite, in 427 s of wall time against the 7,200 s allocation. The historical-anchor gate passed: all 284 historical O and U anchors reproduced their P21 values to 4.4e-16. The endpoint bridge (historical endpoint → P28) moves O and U MAE by at most 4e-4 on these rows. All primary comparisons use the P28 exact endpoint.

The three solvent profiles compared are:

| label | solvent profile | source |
|---|---|---|
| O | open | frozen P21 input |
| C | our open method at the UD geometry | R11 RU |
| U | UD | – |

The solute is the original open profile in all three. Errors are in ln γ∞.

| solvent | rows | MAE O | MAE C | MAE U | removed O→C | signed recovery | rows improved / worsened |
|---|---:|---:|---:|---:|---:|---:|---|
| ethylene glycol | 10 | 2.541 | 0.559 | 0.498 | 1.982 | 0.97 | 10 / 0 |
| diethylene glycol | 108 | 1.740 | 0.648 | 0.371 | 1.092 | 0.80 | 105 / 3 |
| triethylene glycol | 17 | 2.088 | 0.934 | 0.556 | 1.153 | 0.75 | 17 / 0 |
| tetraethylene glycol | 7 | 1.242 | 1.175 | 0.731 | 0.067 | 0.13 | 7 / 0 |
| **pooled** | **142** | **1.813** | **0.702** | **0.419** | **1.111** | **0.80** | **139 / 3** |

The equal-solvent mean MAE goes from 1.903 (O) to 0.829 (C), against 0.539 (U).

Biases are all negative, meaning the alkanes and alkenes are predicted too soluble:

| profile | pooled bias |
|---|---:|
| O | −1.81 |
| C | −0.69 |
| U | −0.37 |

The pooled Shapley breakdown of the absolute-error reduction is shape +1.103, area +0.009 and volume −0.001. They sum to the 1.111 removed. The per-solvent splits are the same: shape carries essentially all of it.

What this establishes: on these 142 already-inspected rows, swapping the stored open solvent coordinates for the UD coordinates, while keeping our open method and Z0x unchanged, removes about 80% of the open-to-UD glycol-solvent IDAC error gap. Nearly all of the change comes through profile shape. The residual 0.28 MAE between C and U is the method bundle.

TetraEG is the exception. The coordinate change removes only 13% of its gap, which matches its R11 tail attribution (raw tail mainly method). The ordering of the four solvents follows R11 member by member. Under the R11 rules no member received a whole-profile label, so the prediction-level result is the more decisive one here.

What this does not establish:

- This is retrospective scoring against ThermoML on rows inspected in R4 to R11. It is not held out, not a fitted improvement, and not grounds to adopt C or UD geometries.
- It does not show that the extended UD chains are the liquid conformation. The UD notice says roughly a third of its conformations were revised using vapor pressures, without naming members.
- It does not decompose the 630-profile benchmark.
- Nothing is adopted. P35 stays open in its registered form, and the 630 + 6 profiles are unchanged.

## P47, regional accounting: complete

All twelve members were processed in 2.0 s, with no model calls, and the R11 labels are unchanged. Panel-level patterns only; per-member tables stay private:

- **Method term (U − C, same geometry, normalized).** The centre band (|σ| < 0.005) carries the largest share of L1 in eleven of the twelve members (water is the exception), and all of it in nonane. Every polar member gains positive-tail area, and every hydroxyl-bearing member also loses centre area. In other words, at the same geometry the UD/DMol3 surface is more strongly polarized on the acceptor side than ours. This is why the shape background was large even in controls with matching tails.
- **Coordinate term (C − R, normalized).** In EG, DEG and TEG the coordinate change removes centre area (signed −0.11, −0.07, −0.02) and adds negative-tail area (+0.04 to +0.05). This is the donor-side OH region by the parser's convention, which matches exposed hydroxyl hydrogens in the extended chains.
- **Channel cancellation** (L1 over 153 bins minus L1 over the collapsed 51) is at most 0.019 for every term. That is small against totals of 0.08 to 0.37, so no large NHB/OH/OT redistribution is hidden in the total-σ view.

These are descriptive partitions, not hydrogen-bond energies or error attributions by bin.

## P48, reporting: applied

In the registration commit, the README paragraph and the dated P35 annotation were updated with the R11 tail finding and the tetraEG exception, as supplied.
