Round 16 of the Z-COSMO review. Please read, in the Victor-Liang-ChE/zcosmo repo:

- `docs/OPTIMIZATION_BRIEF.md`, where the rules are unchanged
- your round-15 report, `docs/astra/round15/ZCOSMO_ROUND15_REPORT.md`
- the measured results, `docs/astra/round15/RESULTS.md`
- `PREREGISTRATION.md`, especially the original Z0 recipe ("London combining rule; weight 1 on the London term"), the session-1 ablation, and R14/R15
- `src/zcosmo/cosmosac.py`: `london_pair_w`, `london_lngamma` and `Mixture.lngamma_disp`
- `src/zcosmo/qc_disp.py` and `results/qc/dispersion.csv`
- the revised `manuscript/draft.md`

Summary of round 15:

- **The breakdown.** The registered factorial ran once on the same 963 exposed P52 VLE rows. It swapped Z0x's ingredients toward COSMO-SAC 2010, which has no dispersion term. The London dispersion term carries 67% of the 3.35-point gap (2.24 pp). Removing it alone takes AAD from 13.78% to 11.76% and moves the bias by −4.5 pp. The electrostatic closure carries 26%, and the hydrogen-bond constants 7%, mostly through interaction with dispersion.
- **The original plan was misdirected.** Item 1 of the "Next" list was based on the conductor-limit Z0 ablation and pointed at electrostatics. With Z0x, dispersion dominates.
- **Fixes and records.** The association-dispatch defect was repaired (P55), and the manuscript scope was revised (P56).

The current London term works like this:

- whole-molecule D4 C6 and polarizabilities
- the Slater–Kirkwood combining rule
- contact at the mean of two hard-sphere diameters built from COSMO cavity volumes
- exchange energy w = 2e₁₂ − e₁₁ − e₂₂ at that single distance
- a coordination factor of z/2 = 5
- a symmetric one-constant mole-fraction Margules form, A·x₂² and A·x₁², with weight 1

**Round-16 questions.**

1. **Physics audit of the London term.** Identify which assumptions in it are not first-principles consequences and could systematically overstate positive deviations. Candidates:
   - one-center C6 at center-to-center contact instead of distributed (atom-pair) dispersion over actual surface contacts
   - the 1/d⁶ distance from cavity-volume spheres
   - the z/2 coordination
   - mole-fraction rather than surface- or volume-fraction weighting, for unequal sizes
   - double counting with dispersion already implicit in the conductor-screened residual, or in the pure-component vapor pressures

   For each, give the direction of its effect on ln γ and on bubble pressure, and say whether a replacement follows from theory without any choice made on ThermoML.
2. **One fit-free alternative, frozen before scoring.** If the audit identifies a defensible replacement, specify exactly one, in code and registration, before any score. Examples: a segment-resolved surface-contact dispersion from atomic D4 C6 with COSMO segment areas, or a volume- or surface-fraction regular-solution form derived from the same C6 table. Declare how it will be evaluated honestly given exposure: a frozen single look on the old split, with exposure stated, or an external set if a custodian can supply one. Also declare what it must not worsen: IDAC, HE and LLE detection. "Delete the term" or "weight 0.5" are selections by error and are not acceptable. If none is defensible, say so.
3. **Endgame.** Say whether the paper should now be finalized with R15 as its explanatory centerpiece, and give the exact manuscript additions for the P54 result.

Constraints are unchanged:

- free compute only
- every model or protocol change registered in `PREREGISTRATION.md` before its output is used
- nothing fitted to the benchmark, and no constant chosen by ThermoML error
- UD profiles only on the Mac
- the 630 + 6 open profiles frozen

Return one markdown report as before: a ranked table, then diffs against current `main` and exact commands. Mark clearly what you executed versus what you only reasoned about.
