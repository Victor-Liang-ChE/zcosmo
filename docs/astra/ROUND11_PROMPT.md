Round 11 of the Z-COSMO review. It continues the P35 glycol question from round 10. Please read, in the Victor-Liang-ChE/zcosmo repo:

- `docs/OPTIMIZATION_BRIEF.md`, where the rules are unchanged
- your round-10 report, `docs/astra/round10/ZCOSMO_ROUND10_REPORT.md`
- the measured results, `docs/astra/round10/RESULTS.md`, and `docs/astra/round10/PROVENANCE_STATUS.md`
- the round-10 registration and results in `PREREGISTRATION.md`, and `docs/astra/round7/GLYCOL_STATUS.md`
- `scripts/r10_*.py`, `scripts/r5_shape.py`, `src/zcosmo/pyscf_cosmo.py` and `scripts/r4_common.py` on `main`

Summary of round 10:

- **P41 and P42 ran on the Mac with zero QC.** All twelve UD raw files were recovered from NIST, and all twelve lineage gates passed. Each recovered `.cosmo` file regenerates the exact UD profile used since R4, and each archived P25 open table regenerates its own profile.
- **Geometry differs systematically.**
  - The four UD linear glycols are fully extended all-anti chains with no OH···O approach (H–A ≥ 3.9 Å).
  - Our open geometries are gauche-folded, with a terminal OH 2.2–2.4 Å from an oxygen. The angle criterion means none meets the registered contact rule.
  - Glycerol and propylene glycol, where the P21 shape effect had the opposite sign, reverse: UD has the short approach, or both do.
- **Polar tails, UD / open.** Raw: EG 41.0 / 34.5, DEG 47.6 / 40.7, TEG 57.1 / 49.0, tetraEG 67.9 / 61.1. After averaging the gaps grow to 8.6–10.8 Å², except tetraEG.
- **Method difference at matched geometry.** Water, methanol, THF and methoxyethanol (RMSD ≤ 0.02 Å) differ by only 0.4–2.9 Å² raw.
- **Open tables.** They also carry net charge −0.012 to −0.045 e (UD about −0.001) and much more extreme negative tessera charges.
- **Still descriptive.** No causal partition exists, because the crossed quantity p_O(R_U), our open method at the UD geometry, was not computed.
- **Usage constraint.** The NIST notice allows academic, non-profit use and forbids redistribution. UD coordinates therefore cannot be committed to this public repo or passed to public GitHub Actions logs and artifacts. Any calculation on them runs on the Mac.

**Round-11 questions.**

1. **The crossed single point.** Design the smallest registered experiment that computes p_O(R_U): the existing open TZVP/SWIG C-PCM single point, unchanged, at each frozen UD geometry for the twelve-member panel. Run it on the Mac only, with no optimization and no outputs containing coordinates committed. It must produce:
   - the geometry term p_O(R_U) − p_O(R_O)
   - the method term p_U(R_U) − p_O(R_U)

   For each member, give a pre-stated decision table:
   - What outcome would say the glycol gap is mainly geometry?
   - What would say it is mainly method?
   - What would say both?
   - What would be inconclusive, given the matched-geometry controls as a noise scale?

   Include the net-charge and outlier-tessera checks, a wall-time budget for the Mac, and the parity check that the open method reproduces its own P25 profile at R_O.
2. **What a geometry answer could and could not justify.** Suppose the geometry term dominates. UD's extended chains were partly chosen by fitting vapor pressures, so they are not an independent reference. Is there any defensible, prospectively registered conformer rule, not chosen by ThermoML error, that could change which glycol geometry the open pipeline uses? One example would be a condensed-phase free-energy criterion applied to all polyols, including water and the branched controls. If not, say the result is explanatory only.
3. **Wording.** Check that RESULTS and README statements about the round-10 geometry finding stay descriptive.

Constraints are unchanged:

- Free compute only. UD-backed and UD-coordinate work runs on the Mac.
- Every protocol change is registered in `PREREGISTRATION.md` before its output is used.
- Nothing is fitted to the benchmark: no geometry or conformer weight is chosen by experimental error.
- The 630 + 6 profiles stay frozen unless a separately registered decision says otherwise.

Return one markdown report as before: a ranked table, then diffs against current `main` and exact commands. Mark clearly what you executed versus what you only reasoned about.
