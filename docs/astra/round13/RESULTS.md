# Round 13: measured results and P35 closeout

Reference: round 13 was adopted 2026-10-07. P49, P50 and REG13 were applied unchanged to e2b36c8, in the commit that records this round's registration. The native and model budget was zero: no SCF, no conformer search, no activity-model call and no Actions dispatch. The audit ran in the container on public files only. No UD-derived data was read.

## P50, public aggregate audit: passed

`r13_closeout.py` verified the round-12 RESULTS file against Git blob `c036e8e2…`. It then checked the P46a counts (EG 10, DEG 108, TEG 17, tetraEG 7, pooled 142) and confirmed that every printed difference and recovery agrees within its rounding interval. It took 2 ms. Output: `data/p50_public_closeout_audit.json`.

| quantity | value |
|---|---|
| MAE removed, open → C | 1.111 (printed 1.813 − 0.702) |
| Share of the open-to-UD comparator gap removed | 0.797 (rounding range 0.7963–0.7977) |
| Share of the original open absolute error removed | 0.613 |
| Residual C-to-UD MAE difference | 0.283 |
| DEG share of pooled rows | 76.1% |

"About 80%" therefore means 80% of the comparator gap, which is 61% of the open profiles' own absolute error. The residual is a difference of MAEs on these rows, not a mean C-versus-U prediction difference. The rounding ranges are not confidence intervals.

The audit also reproduced Astra's explicit sizing scenarios for a hypothetical 630-molecule conformer search. These are sizing figures, not budgets:

| search | final TZVP single points | SVP energy-gradient evaluations (illustrative) |
|---|---:|---:|
| 4 starts per molecule | 2,520 | 20,160 |
| 8 starts per molecule | 5,040 | 40,320 |

Self-tests: r13 15/15, r12 26/26, r11 22/22 and r10 20/20. All use mock adapters.

## P49, reporting: applied

The README replaces the stale "IDAC consequences unresolved" paragraph with the completed R10–R12 finding. `GLYCOL_STATUS.md` gains a dated round-13 closeout. Both keep these qualifications:

- the retrospective scope
- the tetraEG exception
- R11's inconclusive whole-profile labels
- the conditional method-bundle residual
- the frozen 630 + 6 profiles

All earlier RESULTS files and registrations are unchanged.

## Closeout of the Astra review

Victor chose to close after round 13. No round-14 prompt is written. The P35 explanatory campaign is closed:

- **Coordinates.** The stored coordinate inputs explain most of the linear-glycol polar-tail gaps (R11). On the 142 already-inspected rows, they explain about 80% of the open-to-UD glycol-solvent IDAC comparator gap (R12).
- **Exception.** Tetraethylene glycol is the exception, at 13%.
- **What stays unresolved.** Neither the liquid conformer distribution nor a production geometry rule is resolved. A rule chosen to reproduce the extended UD geometry would encode the inspected result, and no untouched validation set has been certified.
- **No adoption.** No crossed profile, conformer rule or ensemble is adopted. The 630 primary profiles and six S1/S2 profiles remain frozen.
- **Earlier decisions stand.** P30/P32 failures, R11 labels, P46a and the R8/R9 numerical-gradient closure stand as recorded.
- **Reopening.** A future geometry project needs a fully specified physical rule, complete computational acceptance criteria, and a genuinely unexposed validation source with an exposure audit. It also needs its own prospective registration and budget.

The README "Current evidence" section is the public summary. `PREREGISTRATION.md` holds every registration, amendment and result from R1 to R13.
