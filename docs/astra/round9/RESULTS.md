# Round 9: measured results and campaign closeout

Reference: round 9 registered 2026-10-07 in the commit that adds this report's patches (P39, P40 and REG9 applied unchanged to 83cf521). The native budget was zero. Nothing was dispatched to Actions, no SCF ran, and no profile, model default or historical result was edited.

## P39, zero-QC membership audit: reproduced

`r9_membership_audit.py` read the archived TEG PCM/pruned call log and verified it against Git blob `1273d62d…`. It then passed every assertion in the report. Its six self-tests pass, and it ran in 4 ms with no chemistry imports.

| displacement (Bohr) | + side count / membership | − side count / membership | minimum retained F, + side | strict central derivative (Eh/Bohr) |
|---:|---|---|---:|---:|
| center | 1340 / A | same | 1.197e-12 | – |
| 0.016 | 1340 / B | 1340 / A | 5.514e-13 | 2.3320e-5 |
| 0.008 | 1339 / C | 1340 / A | 3.734e-10 | 2.1536e-5 |
| 0.004 | 1339 / C | 1340 / A | 5.279e-10 | 2.0022e-5 |
| 0.002 | 1339 / C | 1340 / A | 5.814e-10 | 4.2519e-6 |
| 0.001 | 1339 / C | 1340 / A | 6.096e-10 | −2.94e-8 |

The XC grid has one membership across all 22 calls, and the PCM surface has three, A, B and C. The finest Richardson value reproduces the archived −1.4565463e-6 exactly.

**Correction to the round-8 RESULTS wording.** Round 8 said the 5.5e-13 minimum switching weight belonged to "those calls" where a node dropped out. That is wrong. The minimum is at +0.016 Bohr, where the count is unchanged (1,340) but the membership already differs from the center (B, not A). The positive-side membership is the same C at all four smaller steps. So the collapse of the central derivative between h = 0.004 and 0.002 does not line up with a new sampled membership change. The archive records only a minimum over the retained points. It does not identify which point was removed. The R8 verdict is not changed: TEG stays inconclusive and the mismatch stays unresolved. Output: `data/p39_membership_audit.json`.

The report's PySCF source claims were checked against the pinned 2.14.0 `pcm.py`:

- `switch_h` is the smoothstep t³(10 − 15t + 6t²), clipped to [0, 1].
- Distances below 1e-8 are set to zero.
- A point is retained when w·F > 1e-16.
- The S diagonal is ξ·sqrt(2/π)/F.

The Schur-complement argument, that a retained point's energy contribution vanishes in proportion to F, is reasoning and was not measured.

## P40, README: applied

The two lines recording the R8 unresolved mismatch and the closed diagnostic budget are appended to "Current evidence". A textual check confirms the earlier qualifications are retained, including the failed P32 gate and `ZC_R6_ENDPOINT=1`.

## Closeout

Victor chose to close the Astra review here. There is no round-10 prompt. Final state:

- **Profiles.** profiles_v2 has 630 primary profiles from the original-gradient Berny predicate, plus six S1/S2 profiles that stay flagged. No profile version changed after the chain runs stopped in R5.
- **Accepted.**
  - Z0x as a fit-free model.
  - The exact infinite-dilution endpoint (P28), opt-in through `ZC_R6_ENDPOINT=1`.
  - The P20 scope as registered.
- **Failed or unresolved.**
  - P30's gate.
  - P32's compatibility gate, at 0.0121 against 0.01. No corrected-gradient rollout and no chain rescue.
  - The P33 and P37 TEG energy-gradient mismatch (unresolved).
  - The glycol discrepancy, P35 (unresolved).
- **Measured, with a registered scope.** The grid-response force correction exceeds 1e-5 in 39/39 sampled geometries, and profiles respond to 0.01 Å displacements. That is sensitivity, not geometry error.
- **Reopening rule.** Further native work needs distinct evidence that isolates a specific error, such as an independently checked source correction with a reproducer, under a new prospective registration.

The README "Current evidence" section is the short public summary, and `PREREGISTRATION.md` holds every registration, amendment and result from R1 to R9.
