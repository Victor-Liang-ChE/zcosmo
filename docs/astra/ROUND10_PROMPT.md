Round 10 of the Z-COSMO review. The numerical-gradient campaign is closed (R8, R9). This round changes topic to the largest measured accuracy problem: the glycol gap, recorded as unresolved in P35. Please read, in the Victor-Liang-ChE/zcosmo repo:

- `docs/OPTIMIZATION_BRIEF.md`, where the rules are unchanged
- `docs/astra/round7/GLYCOL_STATUS.md`, the P35 record and its reopening conditions, and the P35 text in `PREREGISTRATION.md`
- `docs/astra/round4/RESULTS.md` (P21 A/V/shape factorial and the net-charge test), `docs/astra/round5/RESULTS.md` (P25 shape-stage matrix, P26/P29 conformer proposals) and `docs/astra/round6/RESULTS.md`, with their `data/` folders
- `docs/astra/round9/RESULTS.md`, the closeout state
- `data/raw/nist/to_sigma.py`, `data/processed_ext/ud_complist.csv`, `src/zcosmo/cosmosac.py`, `src/zcosmo/z0x.py`, and the open-profile generator under `scripts/`

What is already measured:

- **P21 factorial (332 paired rows, 14 solvents).** For the glycol solvents, almost all of the open-versus-UD error difference is profile shape, not area or volume. The MAE in ln γ∞ is listed as open / UD solvent, followed by the shape term:
  - ethylene glycol: 2.48 / 0.39, shape term 2.55
  - diethylene glycol: 1.74 / 0.37, shape term 1.37
  - triethylene glycol: 2.09 / 0.56, shape term 1.50
  - tetraethylene glycol: 1.24 / 0.73, shape term 0.47

  The open profiles make alkane and alkene solutes far too soluble (bias −1.2 to −2.5). Water has a shape effect of the same sign, but there the UD shape is worse (1.55 → 2.07). Glycerol and propylene glycol show little or the opposite effect.
- **P23 net charge.** The net charge is −0.01 to −0.045 e. Neutralizing it accounts for under a tenth of the DEG deficit.
- **P25 shape-stage matrix (36 single points).** The polar tail is |σ| ≥ 0.01 area. TZVP/SWIG reproduces the stored open profiles: the DEG polar tail is 27.7 Å² against UD 38.0. ISWIG versus SWIG changes the tail by at most 0.1 Å². SVP lowers the tail. The deficit is already present in the raw charges, before averaging. The open/UD tails are:
  - EG: 23.0 / 33.0
  - DEG: 27.7 / 38.0
  - TEG: 27.9 / 42.3
  - tetraEG: 41.8 / 46.8

  Rigid controls are within about 2 Å². Propylene glycol goes the other way (30.0 / 25.9).
- **P29.** No positive weighting of the sampled conformers can reach the UD tails, because a convex average cannot exceed its largest member. Unsampled basins are not excluded, and UD is not established as the right liquid distribution.
- **UD provenance on the Mac.** `data/raw/nist/UD/` holds only `complist.txt` and the `sigma3/` profiles. There are no geometries, no `.cosmo` files and no record of electronic or cavity settings. `to_sigma.py`, from the NIST COSMO-SAC tooling, converts DMol3 `.cosmo` output (geometry plus segments) to profiles. So the UD profiles came from DMol3 COSMO files that the project never had.

**Round-10 questions.**

1. **Provenance, at zero cost.** P35's first reopening condition is recovery of the generating UD geometries and raw surface files, with their electronic and cavity settings. Do these exist publicly? Look at the NIST COSMO-SAC repository and its data releases, the University of Delaware / VT-2005 sigma-profile database distributions, and the papers that describe them. For each source, give an exact, verifiable location and say what it contains. Do not guess URLs: if you cannot confirm a file exists, say so. If the glycol `.cosmo` files exist, propose a zero-QC registered comparison: their geometries against our open geometries (dihedrals, intramolecular O–H···O contacts) and their raw segments against our raw segments, run through the same `to_sigma.py` averaging.
2. **If provenance fails, is one bounded physical test justified?** P35's second condition is an independent, basis/grid/response-converged electrostatic reference at frozen known geometries, on a fixed panel that includes water and branched polyol controls. Is there a design on free 4-core Actions runners, within a stated SCF budget, that could tell "wrong geometry or conformer" apart from "different electronic/cavity method"? For example, fixed EG and DEG geometries in open-chain and intramolecular-H-bond conformers, with water, glycerol and propylene glycol as controls. Say what each outcome would establish and what it could not. If no affordable design can separate those explanations, say so and recommend keeping P35 closed.
3. **What should be claimed meanwhile?** Check that the README and RESULTS language on glycols does not overreach in either direction, for example implying that UD is the truth or that the open profiles are wrong.

Constraints are unchanged:

- Free compute only.
- Every model or protocol change is registered in `PREREGISTRATION.md` before its output is used.
- Nothing is fitted to the benchmark. No envelope matching, no fitting of conformer weights to the UD histogram, and no smoothing-constant tuning.
- The 630 + 6 profiles stay frozen unless a separately registered decision says otherwise.
- UD profiles exist only on the Mac, so any UD-backed check runs there.

Return one markdown report as before: a ranked table, then diffs against current `main` and exact commands. Mark clearly what you executed versus what you only reasoned about. If question 1 succeeds, rank it first, ahead of any QC.
