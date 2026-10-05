Round 3 of the Z-COSMO review. Please read, in the Victor-Liang-ChE/zcosmo repo:

- `docs/OPTIMIZATION_BRIEF.md`, where the rules are unchanged
- your round-2 report, `docs/astra/round2/ZCOSMO_ROUND2_REPORT.md`
- the measured round-2 results, `docs/astra/round2/RESULTS.md`
- the entries in `PREREGISTRATION.md` from 2026-10-04 (P15 registration and result, rule S2 registration and result, the exploratory Z0x-open scorecard)
- the S2 code, `cloud/s19/s2_item.py` and `cloud/s19/s2_evaluate.py`

Summary of round 2:

- **P15 was registered and run exactly as you proposed, and rejected.** The 25-molecule gates passed (max |d ln γ∞| 2.15e-4, wall 0.957×), but none of the six stalled chains converged in 100 evaluations in either arm.
- **Your orientation-aware metric was registered as rule S2 and accepted all six chains, flagged and outside `profiles_v2`.** The calibration exposed something bigger: rotating a fixed geometry changes the registered TZVP profile by 1 to 4 percent of its peak (max |d psigmaA| 0.48 to 3.1). That applies to every one of the 636 profiles.
- **The exploratory Z0x-open scorecard on all 636 compounds is worse than Z0x on IDAC** (test MAE 0.977 vs 0.839, dMAE CI +0.052 to +0.232) and about the same on LLE.
- **P10, P11, P12, P13, P14 and H2 have not been run.**
- **Harness note:** the UD reference profiles (`data/raw/nist/UD`) are gitignored and not on the runners, so any check that loads UD must run where they exist. We ran the P15 comparison on the Mac for that reason.

**Round-3 questions.**

1. **Orientation dependence of the profiles.** Explain the mechanism in the pinned pyscf 2.14.0 C-PCM path we use for profiles (`cosmo_segments` in `src/zcosmo/pyscf_cosmo.py`: Lebedev 29 per atom, switching, Hsieh averaging in `data/raw/nist/to_sigma.py`). Why does the effect grow with rotation angle? Then give a measured-first plan with exact commands for its size in ln γ∞ on the 25 validation molecules: a fixed set of rotations, separate processes per profile set (the profile cache in `load_fluid` is keyed by InChIKey, not by directory). Then propose fixes and classify each as E or A with an acceptance test. Candidates: a canonical principal-axis orientation, averaging the profile over a fixed rotation set, a finer Lebedev order, or changes to the averaging step. Say whether the UD (DMol3) reference profiles are likely to have the same issue.
2. **Why are the open profiles worse than UD on IDAC?** Give a diagnostic plan with commands that splits the 0.977 vs 0.839 gap by compound class and by solute/solvent role. Water stood out at acceptance (median |d ln γ∞| 0.82 over 450 rows). Separate what orientation (question 1) could explain from systematic differences: geometry protocol, basis, radii, averaging radius, or the NHB/OH/OT split. Nothing gets tuned to the benchmark; anything that changes profiles must be a registered A change with a fixed acceptance test.
3. **The stalled chains, properly.** Berny stalls because energy changes of about 1e-7 Eh sit at the SCF/C-PCM noise level (conv_tol 1e-8, grid level 2). Would a final stage with tighter `conv_tol` and/or a finer grid let the registered Berny test pass? Or a different optimiser for the last stage only (geomeTRIC with criteria mapped exactly onto Berny's)? Give one A-class proposal with a registered acceptance test, an evaluation budget, and the exact pyscf 2.14.0 / pyberny 0.7.0 API you rely on, checked against the source. A Berny-converged profile would replace the flagged S1/S2 one.
4. **Prioritize the unrun round-2 candidates (P10, P11, P12, P13, P14, H2)** now that QC throughput no longer blocks anything: all 636 compounds have profiles, and only re-runs for questions 1 to 3 remain. Say which are still worth running, in which order, and which to drop.
5. **The Z0x reference discrepancy:** the stored predictions give test IDAC MAE 0.839 on an 828-point common subset, while earlier registrations quote 0.800. Tell us how to check which is right, given `zcosmo.metrics` and `zcosmo.evaluate`.

Constraints are unchanged: free compute only, every model or protocol change registered in `PREREGISTRATION.md` before its output is used, nothing fitted to the benchmark. Return one markdown report as before: a ranked table, then diffs against current `main` and exact commands. Mark clearly what you actually executed versus what you only reasoned about. Last time pyscf could not be installed in your runtime; if that happens again, say so and keep every native claim conditional.
