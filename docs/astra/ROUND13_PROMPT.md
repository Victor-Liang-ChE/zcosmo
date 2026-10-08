Round 13 of the Z-COSMO review. It continues the P35 glycol question. Please read, in the Victor-Liang-ChE/zcosmo repo:

- `docs/OPTIMIZATION_BRIEF.md`, where the rules are unchanged
- your round-12 report, `docs/astra/round12/ZCOSMO_ROUND12_REPORT.md`
- the measured results, `docs/astra/round12/RESULTS.md`, including amendment P46a
- the R10–R12 registrations and results in `PREREGISTRATION.md`, with `docs/astra/round11/RESULTS.md` and `docs/astra/round7/GLYCOL_STATUS.md`
- `scripts/r12_*.py` on `main`, plus the open-profile generator and conformer pipeline (`src/zcosmo/pyscf_cosmo.py` and the geometry/conformer scripts it uses)

Summary of round 12:

- **P46a.** The registered design hard-coded 9 EG rows, but exact-key selection gives 10, because "1,2-dihydroxyethane" is the same InChIKey. P46a was registered before any model call; it changes only the counts (142 rows, 13 keys).
- **P46, retrospective explanatory scoring.** The run made 1,562/1,562 finite requests, and the historical anchors reproduced to 4e-16. Keeping our open method and Z0x but using the UD coordinates for the solvent (C) gives:
  - Pooled glycol-solvent IDAC MAE: O 1.81, C 0.70, U 0.42.
  - That removes 80% of the O-to-U gap. 139/142 rows improved, and nearly all of the gain is through shape.
  - Recovery per solvent: EG 0.97, DEG 0.80, TEG 0.75, tetraEG 0.13.
- **P47, regional accounting.**
  - At fixed geometry, UD's surface is more polarized on the acceptor side than ours: centre area moves to the positive tail.
  - The EG/DEG/TEG coordinate change moves centre area to the donor-side tail, consistent with exposed hydroxyl hydrogens.
  - Channel cancellation is small.

**Round-13 questions.**

1. **Is there a defensible, prospective geometry rule?** The explanatory result is strong, but it was obtained on inspected rows using UD coordinates, which were partly revised against vapor pressures. Could the open pipeline adopt a geometry rule chosen without ThermoML or UD reference? Examples:
   - a declared conformer-search plus selection criterion applied to every flexible molecule, such as condensed-phase-energy, conductor-energy or most-extended rules
   - an ensemble with a stated free-energy weighting

   Then assess the rule.
   - Say which rules are physically defensible.
   - Say whether any can be validated without circularity. For example: on a held-out split of ThermoML or another property, with the glycol rows already inspected excluded from acceptance, and with water and branched polyols as required controls.
   - Give the free-compute cost for the 630 profiles.

   If none is defensible at this stage, say so.
2. **Wording.** Propose the exact P35 and README text that records the R10–R12 chain:
   - stored-coordinate dominance of the linear-glycol tails
   - 80% of the retrospective glycol IDAC gap removed by coordinates alone
   - the tetraEG exception
   - the method-bundle residual

   It must not imply that the extended conformation is correct for the liquid, or that anything was adopted.
3. **Close or continue.** If no prospective rule is affordable and testable, recommend closing P35 with the explanatory finding. If one is, give the smallest registered first step, preferably one that costs zero or very little QC.

Constraints are unchanged:

- Free compute only.
- UD-derived data stays on the Mac.
- Every protocol change is registered in `PREREGISTRATION.md` before its output is used.
- Nothing is fitted to the benchmark, and no geometry is chosen by experimental error.
- The 630 + 6 profiles stay frozen unless a separately registered decision says otherwise.

Return one markdown report as before: a ranked table, then diffs against current `main` and exact commands. Mark clearly what you executed versus what you only reasoned about.
