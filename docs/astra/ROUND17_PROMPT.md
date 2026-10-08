Round 17 of the Z-COSMO review: a final manuscript audit. No new experiments. Please read, in the Victor-Liang-ChE/zcosmo repo:

- `manuscript/draft.md` (current `main`)
- `PREREGISTRATION.md`, the complete record
- `docs/astra/round*/RESULTS.md` for rounds 2–16, the README "Current evidence" section, and `PROGRESS.md`
- the scorecards under `results/`

Where things stand:

- **R15.** The P54 factorial attributed 67% of Z0x's VLE gap to COSMO-SAC 2010, on 963 exposed rows, to the London dispersion closure.
- **R16.** The single frozen theory-based alternative, LV1, failed its registered screen. VLE fell only 0.65 points, not resolvably, and IDAC and HE got significantly worse. Nothing was adopted.
- **The open question is closed for this project.** The VLE gap stays open, and the paper is being finalized.

**Round-17 tasks** (zero QC, zero model calls):

1. **Claim-by-claim audit.** Check every numerical claim in `manuscript/draft.md` against its source file (scorecard, RESULTS or registration). List each mismatch, stale number, or claim stronger than its record, with the exact fix. Include the scope of "no fitted constants" and of the exposed-data results.
2. **Add R16.** Write the LV1 result into §3.11 and the discussion, as a registered negative result.
3. **Structure for submission.** Propose an order that leads with the main pre-registered findings:
   - IDAC tie with COSMO-SAC 2010
   - LLE detection win
   - VLE/HE losses
   - the factorial explanation of VLE

   The long R2–R14 infrastructure record (open profiles, gradients, glycols) should move to supplementary material with one-paragraph summaries.
4. **References and figures.** List which references still need publisher verification and which figures exist versus are only captioned. Give exact commands to regenerate the figures from committed data where possible.

Constraints are unchanged: no historical number is rewritten, and no new scoring is done. Return one markdown report: a ranked table, then diffs against current `main`, and mark what you executed.
