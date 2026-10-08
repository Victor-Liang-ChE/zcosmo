# Round 14: measured results

Reference: round 14 was registered 2026-10-08 in 834b929, with P51, P52, H14, P53 and REG14 applied unchanged to 864aaac. Amendment P52a followed in c782585, and the oracle plan was frozen in e0f1608. Everything ran on the Mac in queue jobs 407 to 409. There were no SCF calls and no new quantum chemistry or simulation of any kind. P52 made one oracle run with no retry. Reference tables, plans and row-level predictions stay private on the Mac. This file reports the allowlisted aggregates.

## Amendment P52a and the operational record

The first P52 freeze, under 834b929, stopped at its own integrity check with zero model calls: "protected profile count differs in s1_stalled". On the Mac, `data/pyscf_sigma/s1_stalled` holds 6 files and `s2_stalled` holds 5, because those folders also keep superseded copies. The registered 630 + 5 + 1 population is a per-key selection, `r4_common.selected_profiles`, which has been in use since R4.

P52a changes only `protected_profiles()`, so that it fingerprints exactly that selection. The helpers are byte-bound to their registration commit, so the following were re-executed under c782585, each into a fresh directory:

- the CRC acquisition: one GET, with the same Git blob bf12ffba
- P51

The re-executed P51 rows are identical to the first run's.

Two fresh-directory retries were needed after P52a, both before any model call:

- The first P51 rerun was refused because its source receipt carried the old registration.
- The first oracle-plan directory already existed, left by the failed freeze.

All earlier directories are retained.

## P51, dielectric ingredient audit: complete, registered aggregate withheld

The stored table covers 742 compounds. The pinned CRC compilation (CalebBell/chemicals e790475) matches 248 of them by exact InChIKey → CAS → reference at 298.15 K.

| status | count |
|---|---:|
| matched | 248 |
| CAS not in the reference | 181 |
| missing or ambiguous key → CAS | 173 |
| no reference value at the declared temperature | 135 |
| invalid stored ε | 5 |

Because 5 stored values are invalid (missing or non-finite), the registered rule withholds the complete-comparison aggregate (`baseline_metrics: null`). The audit made zero SCF calls and zero model calls, and took 0.01 s.

The following figures are a descriptive census of the 248 matched rows, computed afterwards from the private row file. They are not the registered metric.

| reference ε | rows | mean log bias, stored vs reference | mean absolute log error |
|---|---:|---:|---:|
| < 10 | 175 | +0.53 (about 1.7× too high) | 0.60 |
| ≥ 10 | 73 | +0.04 | 0.64 |

So the Onsager table's largest systematic error is overestimating ε for weakly polar liquids. The underestimate for water (52.9 vs 78.4) and methanol is real but is not the dominant pattern. The table carries no orientational correlation, yet its main bias runs the other way, which points to the dipole, volume or local-field approximations.

## P52, experimental-ε oracle: complete

The selection used a fixed SHA ordering, with no error used in choosing. It took 100 systems and 963 observations out of 6,039 eligible test-split rows in 209 systems, from the accepted P6 Z0x VLE archive (`results/p6/Z0x__vle__all.csv`).

The run made 2,889 of 2,889 finite requests in 198 s against the 7,200 s cap. The stored-ε baseline replayed the archived pressures exactly: maximum relative error 0.0 on all 963 rows. All three arms use the same profiles and saturation pressures.

| arm | AAD P % | equal-system AAD % | bias % |
|---|---:|---:|---:|
| Z0x, stored ε | 13.78 | 13.90 | +1.44 |
| Z0x, experimental ε at 298 K | 13.07 | 13.19 | +0.34 |
| COSMO-SAC 2010 | 10.44 | 10.65 | −0.02 |

Replacing every matched ε with its experimental value lowers VLE AAD by 0.72 percentage points. That recovers 21% of the 3.35-point gap to COSMO-SAC 2010 on these rows. 559 rows improved and 404 worsened.

Under the registered decision table, this is the first outcome: a small pressure change despite large ε errors. Even perfect bulk permittivities move this selected sample only modestly under the current closure. That does not justify a portfolio liquid-simulation campaign for ε. This is retrospective and exposed. The experimental-ε arm is not fit-free and is never a production model, and no generalization interval is claimed.

## P53 and the association-dispatch finding

P53's status note (`STATUS_PROPOSED.md`) is recorded as supplied. It includes the manuscript wording correction: say that Z0/Z0x interaction constants were not regressed to ThermoML, not that no experimental information enters anywhere.

The registration confirmed a real code defect. Since P6 (2bef48f, 2026-09-28), `Z0xBinary.lngamma` calls `_analytic` in the interior and `_endpoint` under P28. Both bypass the `_g` override in `Z0wBinary` and its subclasses. The archived Z0w, Z0w2 and Z0w3 predictions (2026-09-25/26) predate this and are unaffected. Fresh association predictions on current `main` are quarantined until a separately registered repair.

## State after round 14

- The dielectric lever is small. On this sample, a perfect ε recovers about a fifth of the VLE gap to COSMO-SAC 2010.
- The remaining four-fifths sits elsewhere: the contact/closure mapping, association and hydrogen bonding, or the profiles.
- No model, table or profile changed. Nothing was adopted.
