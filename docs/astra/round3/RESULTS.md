# Round 3: measured results

Reference: Round 3 registered 2026-10-05 00:12 PDT (commit 9d32e9e, your six patches applied unchanged), experiment frozen in 0e8a918, results recorded in 613dd8f. Native items ran on GitHub Actions (pyscf 2.14.0, pyberny 0.7.0); every UD-backed score and gate ran on the Mac.

## P16, IDAC audit

- A fresh Z0x evaluation reproduces the stored predictions to 2.9e-10. There is no drift.
- 0.839 is Z0x on all 828 test rows (204 systems). The 0.800 quoted since 2026-09-25 is the same predictions on the 762-row common subset of a scorecard that also contained unifac_do, cosmosac2010 and Z0w. Both numbers stand with their denominators.
- The open deficit (+0.137) is a solvent-role effect. Your four-corner attribution gives solvent +0.236, solute −0.099.
- Diethylene glycol as solvent alone contributes +0.137 (108 rows, MAE 0.69 → 1.74). Triethylene glycol adds +0.024 and ethylene glycol +0.023. The solutes are mostly alkanes and alkenes (n-nonane +0.046, 1-heptene +0.018, n-octane +0.015).
- Water as solvent improves (−0.016).

Profile observables, open vs UD (Mac, `profile_descriptors`):

| compound | source | area Å² | volume Å³ | net σ moment | tail area Å² | NHB Å² | OH Å² | OT Å² |
|---|---|---|---|---|---|---|---|---|
| diethylene glycol | open | 154.9 | 130.6 | −0.0339 | 27.7 | 126.0 | 26.8 | 2.1 |
| diethylene glycol | UD | 152.0 | 136.6 | −0.0028 | 38.0 | 114.8 | 31.3 | 5.9 |
| triethylene glycol | open | 208.2 | 182.6 | −0.0350 | 27.9 | 177.2 | 24.8 | 6.2 |
| triethylene glycol | UD | 204.4 | 191.3 | −0.0032 | 42.3 | 161.4 | 31.3 | 11.7 |
| ethylene glycol | open | 99.1 | 78.1 | −0.0227 | 23.0 | 75.4 | 23.8 | 0.0 |
| ethylene glycol | UD | 99.0 | 81.5 | −0.0028 | 33.0 | 67.6 | 31.4 | 0.0 |
| n-nonane | open | 224.8 | 201.1 | −0.0424 | 0.0 | 224.8 | 0 | 0 |
| n-nonane | UD | 216.9 | 211.7 | −0.0063 | 0.0 | 216.9 | 0 | 0 |

The open glycol profiles have about a third less polar tail area and less OH/OT area than UD. Their volumes are 4 to 5 percent smaller and their areas 2 to 4 percent larger. Every open profile carries a net σ moment of −0.02 to −0.04, against about −0.003 for UD; the raw C-PCM charge sums in the item diagnostics are about −0.03 e.

## P17, orientation

- 290 TZVP single points completed. Co-rotating existing segments reproduces the profile to 2.8e-14. Identity and repeat are identical, and the identity reproduces the historical acceptance statistic (0.1493).
- Eight random rotations change ln γ∞ on the 2,302 occurrences by a mean of 0.008 (COSMO-SAC-dsp) and 0.011 (Z0x) per rotation, with panel maxima of 0.076 and 0.111. cube90 changes nothing.
- On the fixed-axis angle ladder, max |d psigmaA| grows up to about 0.1 rad, then saturates (water 0.021 at 0.001 rad, 0.21 at 0.01, 0.60 at 0.1, 0.54 at 0.5, 0.58 at 1.0).
- Surface-normal closure defects reach 0.43 Å² and origin-shift volume changes 0.39 Å³.
- Conclusion: orientation is a real but small uncertainty (about 0.01 in ln γ) and cannot explain the 0.137 deficit.

All three A recipes were rejected by their registered gates:

| recipe | rotation invariance | compatibility gate (max COSMO-SAC-dsp change < 0.05, median vs UD < 0.15) |
|---|---|---|
| canonical | exact (panel max 2e-10), passes | fails: 0.0567, median 0.1502 |
| Lebedev 41 | 0.069 / 0.070 vs required ≤ half and < 0.01, fails | fails: 0.075 |
| mean8 | mean8 vs mean8b 0.021 / 0.030 (bound 0.01), vs mean16 0.010 / 0.015 (bound 0.005), fails | fails: 0.054 |

## P18, COOH flag: accepted

- On the 25 compounds, one changes flag: decanoic acid, from HB-DONOR-ACCEPTOR to COOH.
- Raw rows are unchanged, Z0x is unchanged, and every other compound is unchanged.
- The acceptance statistic becomes 0.1362, against 0.1493 uncorrected.
- It is not yet applied to `profiles_v2` or to any score.

## P19, final precision: rejected

- Calibration: all 25 passed the original confirmation test in both arms (61 evaluations each).
- Profile change tight vs control: max 1.1e-4 (COSMO-SAC-dsp) and 2.1e-4 (Z0x).
- Paired wall time was 2988 s vs 1311 s, a ratio of 2.28 against the 1.50 limit. As registered, the six chains were not run.

## Round-2 P14, LLE sidecar

- Audit off and audit on give identical Z0x LLE predictions (6,581 rows).
- The audit records 2,255 binodal calls:
  - 1,842 refined roots
  - 408 with no gap on the 81-point grid (returned None)
  - 5 coarse-hull fallbacks (`ier` 5)
- Of the refined roots, 223 fail the residual check, with residuals up to 5e-3 and most involving water.
- 158 calls have a negative sampled tangent margin.
- Nothing was rescored.
