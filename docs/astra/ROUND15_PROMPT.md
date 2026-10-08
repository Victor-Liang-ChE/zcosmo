Round 15 of the Z-COSMO review. Please read, in the Victor-Liang-ChE/zcosmo repo:

- `docs/OPTIMIZATION_BRIEF.md`, where the rules are unchanged
- your round-14 report, `docs/astra/round14/ZCOSMO_ROUND14_REPORT.md`
- the measured results, `docs/astra/round14/RESULTS.md`, including amendment P52a
- `PREREGISTRATION.md`, especially the original Z0 recipe, the Z0/Z0e/Z0s/Z0x/Z0w* registrations, and R14
- `src/zcosmo/zmodel.py`, `src/zcosmo/z0x.py`, `src/zcosmo/z0w.py`, `src/zcosmo/cosmosac.py` and `manuscript/draft.md`

Summary of round 14:

- **P52 oracle.** Replacing every matched pure-liquid ε with its experimental value moved Z0x VLE AAD only from 13.78% to 13.07%. COSMO-SAC 2010 was at 10.44%. This was on 100 systems / 963 exposed test rows, with an exact baseline replay. Bulk ε accounts for about 21% of the gap. 559 rows improved and 404 worsened.
- **P51 ingredient audit.** 248 of 742 stored ε matched the CRC table. As a descriptive census, the Onsager values overestimate ε for weakly polar liquids by about 1.7× (mean log bias +0.53 on 175 rows with ε < 10). For high-ε liquids they are nearly unbiased on average.
- **Code defect.** A real defect is confirmed: since P6, `Z0xBinary.lngamma` bypasses the Z0w* `_g` override. Archived association results predate it.
- **Contact coefficient.** In your R14 report you noted something about the coefficients. The conductor-limit contact coefficient is c0 = 12,226. COSMO-SAC 2010's fitted value at 298 K is about 8,197. Matching them would need f ≈ 0.67, or ε ≈ 4 in the current mapping. Bulk ε is not the right knob: the gap seems to live in the mapping from a dielectric picture to the local segment-contact energy.

**Round-15 questions.**

1. **Where is the remaining VLE gap?** Propose a zero-QC, registered decomposition on the same 963 oracle rows (private, Mac). Use a factorial or Shapley design, as in P21/P46. Between Z0x and COSMO-SAC 2010, swap one ingredient at a time:
   - electrostatic contact coefficient
   - hydrogen-bond constant and cutoff
   - London/dispersion term
   - a_eff
   - profile convention

   The aim is to locate which term carries the pressure error. Mark clearly that swapping in a fitted 2010 constant is a diagnostic, never a model.
2. **Is there a first-principles local contact coefficient?** If the decomposition points at the electrostatic misfit prefactor, say whether a defensible fit-free derivation of the local segment-contact coefficient exists that is not the bulk-ε Onsager mapping. Candidates include:
   - a local reaction-field model at segment scale
   - an explicit pair-contact screening from dimer or cluster DFT
   - a self-consistent conductor-to-dielectric correction of the profiles themselves

   Assess physics, circularity risk, and free-compute cost. If none exists, say so.
3. **Association repair and value.** Specify the minimal registered repair of the Z0w* dispatch defect with a regression test. Then say whether any association redesign still deserves a look, given Z0w3's double-counting diagnosis.
4. **Endgame.** If neither (1) nor (2) gives a defensible, affordable path to closing the VLE gap, recommend finalizing the paper. List the exact manuscript changes the R2–R14 record requires: open-profile scope, the grid-response gradient finding, the glycol explanation, the ε oracle, and the wording correction on experimental inputs.

Constraints are unchanged:

- free compute only
- every model or protocol change registered in `PREREGISTRATION.md` before its output is used
- nothing fitted to the benchmark, and no constant chosen by ThermoML error
- UD profiles only on the Mac
- the 630 + 6 open profiles frozen

Return one markdown report as before: a ranked table, then diffs against current `main` and exact commands. Mark clearly what you executed versus what you only reasoned about.
