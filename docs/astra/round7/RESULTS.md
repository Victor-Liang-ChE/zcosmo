# Round 7: measured results

Reference: round 7 registered 2026-10-06 in 6a51e75 (your six patches applied unchanged to ddf22b1). Plans frozen in 95c8d88 (calibration, pilot, chains, referee). Two registered amendments, both made before any affected computation:

- **P34a (ef2fa58).** The screen plan required a `geometry_converged` flag that 626 of the 630 primary profiles predate. It now accepts their recorded "(pyberny)" geometry provenance.
- **P33a (29e9bf2).** The referee compared RDKit to the literal `'2026.03.6'`, but pip reports the PEP 440-normalized `'2026.3.6'`. Every case stopped in 0.2 s before any SCF. It now compares normalized versions, and the referee plan was re-frozen in 97db7ea.

The P34 screen plan was frozen in a8c5de0. Void dispatches (no computation): 37546518712 (referee, version string), 37546536602 and 37546787100 (screen, before its plan existed). Measured runs:

- calibration 37546500861
- referee 37547463603
- screen 37546971488

All UD-backed gates ran on the Mac (queue jobs 372 to 383).

## P32, grid-response optimizer trial: compatibility gate failed, pilot and chains not run

All 25 calibration targets reached the original Berny predicate in both arms (fresh histories, the same frozen seed-7 xTB start). Both arms are equally fast:

- Gradient evaluations were within ±2 per target, except TEG: 14 (off) vs 9 (full).
- Paired worker time was 2,636 s (off) against 2,986 s (full), a ratio of 1.13 (routine-throughput indicator 1.50: within).

| check (2,302 historical occurrences) | result | limit |
|---|---|---|
| finite coverage, COSMO-SAC-dsp / Z0x | 2,271 / 2,302 in both arms, identical masks | identical |
| max \|COSMO-SAC-dsp change\|, full vs off | **0.0121** | < 0.01 |
| median \|COSMO-SAC-dsp change\| | 1.7e-4 | reported |
| max / median \|Z0x change\| (P28 endpoint) | 0.0170 / 1.4e-4 | reported |
| median \|COSMO-SAC-dsp − UD\| (full arm) | 0.136 | < 0.15 |

- The registered compatibility gate fails on the maximum change, 0.0121 against 0.01. As registered, the three-pair pilot was not dispatched, and the six-chain stage stays closed with no permit.
- The largest profile differences between arms are in flexible molecules: GHVNFZFCNZKVNT (normalized L1 0.017), triethylene glycol (0.015) and PWGJDPKCLMLPJW (0.010). All others are ≤ 0.003.
- Reading: with the full gradient, these molecules settle into slightly different geometries, enough to move one dsp query by 0.012. That is a real geometry change, not a failure to converge.

## P33, uncertainty-aware consistency referee (τ = 1e-5 Eh/Bohr)

- **Completion.** Four of the five cases completed: 82 SCF and 3 gradients each, grid counts stable. Methanol failed with "SCF failed" after 21 SCF evaluations. It is recorded as a native failure, not retried.
- **Inconclusive directions.** Most were inconclusive because the Richardson ladder did not stabilize within the τ/4 indicator ceiling (2.5e-6).
- **Resolved directions:**

| case | direction | full-response verdict | off verdict | omitted response material |
|---|---|---|---|---|
| n-nonane | bond 0-1 | consistent (err 4.7e-6) | inconsistent (1.9e-5) | **yes** |
| n-nonane | bond 1-2 | consistent (0) | inconsistent (1.9e-5) | **yes** |
| n-nonane | bond 2-3 | consistent | consistent | no |
| triethylene glycol | bond 1-2 | consistent (4.7e-7) | inconsistent (1.7e-5) | **yes** |
| triethylene glycol | bond 3-4 | **inconsistent** (2.2e-5) | inconclusive | unknown |
| ethylene glycol | bond 2-3 | consistent | consistent | no |
| dimethoxyethane | all four | inconclusive | inconclusive | unknown |

- **The omitted grid response is a resolved error.** The no-response gradient fails the registered τ in three directions (nonane ×2, TEG ×1), where the full-response gradient passes.
- **Grid response does not settle every direction.** In one TEG direction, even the full-response gradient disagrees with its own energy by 2.2e-5, a resolved discrepancy beyond τ.
- **Overall flag.** `full_response_consistent` is false for every case, because the per-case verdict needs every direction resolved.

## P34, primary-profile screen (32 SHA-sampled + 8 sentinels, no optimization)

- 39 of 40 native cases completed. XIRNKXNNONJFQO stayed "running", so its runner ended before the case recorded a final status. The probability sample is therefore incomplete and no sampling bound is reported, as registered.
- Grid-response force indicator: at the saved geometries, the off/full gradient difference exceeds 1e-5 Eh/Bohr in 39 of 39 completed cases (up to 3.3e-4).
- Finite-stress affinity screen (±0.010 Å along the projected full-response gradient, fixed probes, P28 Z0x and COSMO-SAC-dsp):
  - 35 cases are screen-positive (max |Δ ln γ| ≥ 0.01). The largest changes are 0.66 (PGMYKACGEOXYJE), 0.55, 0.40 (methanol sentinel), 0.37 and 0.31.
  - 4 cases are unresolved because finite coverage changed (GWQOOADXMVQEFT, RAHZWNYVWXNFOC, SUVIGLJNEAMWEG, VYMPLPIFKRHAAC).
  - None is screen-negative.
- Interpretation, as registered: profiles respond measurably to 0.01 Å displacements along the corrected force for essentially every sampled molecule. This shows sensitivity at the tested scale. It does not show that the stored geometries are that far from the corrected optimum. No primary profile was changed.

## P35, glycol mechanism

The glycol tail gap is recorded as unresolved under the available inputs, with the registered reopening conditions. No QC budget was spent.

## Deviations and notes

- Plans and dispatches ran on main, not on a separate experiment branch. Run identification used the exact run IDs above instead of the report's run-name lookup, because void same-name runs exist.
- Every gate was decided by its JSON output, not by the workflow's green status. Several workflow jobs show green even though their case failed.
