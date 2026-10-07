Round 12 of the Z-COSMO review. It continues the P35 glycol question. Please read, in the Victor-Liang-ChE/zcosmo repo:

- `docs/OPTIMIZATION_BRIEF.md`, where the rules are unchanged
- your round-11 report, `docs/astra/round11/ZCOSMO_ROUND11_REPORT.md`
- the measured results, `docs/astra/round11/RESULTS.md`
- the R10 and R11 registrations and results in `PREREGISTRATION.md`, `docs/astra/round10/RESULTS.md` and `docs/astra/round7/GLYCOL_STATUS.md`
- `scripts/r11_*.py` and `scripts/r10_*.py` on `main`, plus the P21 factorial code and results in `docs/astra/round4/RESULTS.md`

Summary of round 11:

- **The run.** 24/24 single points ran once on the Mac in 594 s. Same-input parity passed for all twelve members, to about 1e-12.
- **Tail labels.** For EG, DEG and TEG, every tail measure is mainly geometry. Our open method at the UD geometry raises the final polar tail by 8.1–12.0 Å², which is 79–87% of each gap. The method term is 1.3–2.4 Å².
- **Other members.** TetraEG's raw-tail gap is mainly method, and its other tails are small. Glycerol and propylene glycol carry the reversed sign in the geometry term but sit inside 2η.
- **Headline labels.** No member got a whole-profile label. Every normalized-shape contrast was small relative to the control-derived shape scale (η = 0.359 L1). The controls themselves differ from UD in normalized shape by up to 0.37 at near-matching geometry.
- **Net charge.** The open net charge (−0.012 to −0.046 e) does not change with geometry. It belongs to the method bundle.

**Round-12 questions.**

1. **Does the profile result matter for predictions?** The tail gap in the linear glycols is mostly coordinate input, but the error that matters is in ln γ∞. Design the smallest registered explanatory evaluation that asks how much of the P21 glycol-solvent IDAC error disappears when the frozen open profiles are replaced by C = p_O(R_U): our method at the UD geometry, using the same P21 rows and solutes. Keep the P21 factorial structure, so area, volume and shape stay separable. Constraints:
   - It must be explanatory only. No adoption, and no selecting a geometry because it scores better.
   - The C profiles derive from UD coordinates, so they stay private on the Mac. Only aggregate errors may be published.
   - Say whether it counts as scoring against ThermoML under the brief, and how to report it so it cannot be read as a fitted improvement.
   - If you judge it not worth running, say why.
2. **The shape scale.** The registered shape background is dominated by method-only differences in the controls. Without changing R11's labels, say what that implies: our open method and DMol3/UD differ in normalized shape at nearly fixed geometry by about as much as the glycol gaps. Is there a zero-QC analysis of the archived R11 profiles (private, on the Mac) that would locate where in σ those method differences sit, for example the hydrogen-bond donor versus acceptor regions or the non-polar centre?
3. **Closing P35, or the next step.** Given R10 and R11, can P35 now be restated as "glycol tail gap mainly from the stored conformation; mechanism for the liquid unresolved"? Propose the exact wording. Otherwise, is there a defensible next experiment on free compute? Your R11 report sketched a phase-dependent conformer free-energy protocol. Say whether any version of it is affordable here, or whether P35 should be closed with the explanatory finding.

Constraints are unchanged:

- Free compute only. UD-derived data stays on the Mac.
- Every protocol change is registered in `PREREGISTRATION.md` before its output is used.
- Nothing is fitted to the benchmark, and no geometry is chosen by experimental error.
- The 630 + 6 profiles stay frozen unless a separately registered decision says otherwise.

Return one markdown report as before: a ranked table, then diffs against current `main` and exact commands. Mark clearly what you executed versus what you only reasoned about.
