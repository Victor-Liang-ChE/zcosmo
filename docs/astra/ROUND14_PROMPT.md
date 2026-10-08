Round 14 of the Z-COSMO review. The glycol campaign (P35) closed in round 13. This round returns to the project's main question, how far COSMO-SAC can go with zero fitted constants, and to its largest measured loss: vapor-liquid equilibrium. Please read, in the Victor-Liang-ChE/zcosmo repo:

- `docs/OPTIMIZATION_BRIEF.md`, where the rules are unchanged
- `PREREGISTRATION.md` from the top. Read the original split, metrics and tiers, then the Z0e, Z0s, Z0x, Z0w, Z0w2 and Z0w3 registrations and results.
- `PROGRESS.md`, especially the session-1 ablation and "Next" list, and the session-5 MLIP-teacher and Z0w3 notes
- `results/scorecard_test_main7.md` and the temporal-set scorecards in `results/`
- `src/zcosmo/z0x.py`, `src/zcosmo/zmodel.py` (`c_es_theory`), `src/zcosmo/qc_dielectric.py` and `results/qc/dielectric.csv`
- the liquid-simulation code used for the Z0w3 teacher (`cloud/s15/` and related scripts), and `manuscript/draft.md`
- `docs/astra/round13/RESULTS.md` for the closeout state

Where things stand, test split (`results/scorecard_test_main7.md`):

| Metric | UNIFAC-Do | COSMO-SAC 2010 | Z0x |
|---|---|---|---|
| IDAC MAE (ln γ) | 0.446 | 0.815 | 0.762 |
| VLE AAD P | 11.3% | 8.6% | 14.2% |
| HE MAE (J/mol) | 314 | 399 | 522 |

Z0x is significantly better on LLE split detection, worse on the 2017–2019 temporal set, and needs no fitted constants.

Z0x's only medium-dependent ingredient is the dielectric factor f = (ε − 1)/(ε + 0.5). The pure-liquid ε comes from the Onsager equation, using an xTB dipole of one MMFF conformer, a D4 polarizability and the COSMO volume. Onsager ignores orientational correlation, which is the Kirkwood g-factor. So it should underestimate ε most for hydrogen-bonded liquids. The stored values already show this: water 52.9 against about 78 experimentally, and methanol 24.4 against about 33. Each better screening model has lowered VLE error: Z0 18.8% → Z0e 15.7% → Z0x 14.2%. The session-1 ablation names conductor-limit electrostatics as the main VLE error source. "Kirkwood g-factor or liquid volume" was the first item on the original "Next" list and was never done.

The project now has a fast liquid-simulation engine on free GPUs. MACE-OFF23 NPT runs gave water at 1.115 g/cc and 87% hydrogen-bonded, cross-checked on Kaggle. It does not natively produce dipoles.

**Round-14 questions.**

1. **A first-principles permittivity, and is it worth it?** Propose the smallest defensible way to replace Onsager ε with a fit-free value that includes orientational correlation. Options include:
   - dipole-fluctuation ε from liquid simulation, with a stated dipole or charge model on snapshots
   - Kirkwood g from cluster or dimer QM
   - Kirkwood–Fröhlich with a simulated g

   For each, give the physics and the error sources: dipole model, finite size, sampling length, polarizability double-counting with the COSMO screening, and temperature dependence. Give the free-compute cost for the roughly 740 compounds in `dielectric.csv`, or a declared subset with a stated fallback.
2. **Zero-QC ingredient check first.** Before any model is scored, can the ε ingredient be validated against experimental static permittivities? This is a property the project has never scored, from a public source you can verify exactly. Design that check: source, identity matching, metric and acceptance gate, fixed before any new ε is computed. Say whether the dielectric literature is genuinely independent of the ThermoML phase-equilibrium data. Also say whether the existing Onsager values' error on it already tells us how much VLE headroom a better ε could buy, by a zero-cost sensitivity: Z0x with experimental ε substituted where available, as a diagnostic, never an adopted model.
3. **The overused test split.** The 20% test split has been scored many times, and the 2017–2019 temporal set has also been scored. Propose how a new Z0x variant can be evaluated honestly. Options:
   - a design frozen before one confirmatory look, with exposure stated
   - a genuinely unexposed source: ThermoML or TRC releases after 2019, other open VLE/HE datasets, or a custodian-frozen subset

   For any source you name, give an exact, verifiable location and say what it contains. Do not guess URLs. Put the exposure audit before any score.
4. **Rank honestly against the alternatives.** Compare this with the association redesign that Z0w3 pointed to (replace, not add to, the COSMO hydrogen-bond term) and with simulation-based activity coefficients. If none has a real chance of closing the VLE gap to COSMO-SAC 2010 within free compute, say so. In that case recommend writing up the current results.

Constraints are unchanged:

- free compute only (owned Mac, free GitHub Actions, free Kaggle/Modal/Lightning allowances)
- every model or protocol change registered in `PREREGISTRATION.md` before its output is used
- nothing fitted to the benchmark, and no constant or choice selected by ThermoML error
- UD profiles exist only on the Mac
- the 630 + 6 open profiles stay frozen

Return one markdown report as before: a ranked table, then diffs against current `main` and exact commands. Mark clearly what you executed versus what you only reasoned about.
