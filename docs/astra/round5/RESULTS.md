# Round 5: measured results

Reference: round 5 registered 2026-10-05 22:27 PDT in e126d31 (your six patches applied unchanged to 69b4911). P25 plan frozen in 5eeb9eb, P26 proposals frozen in 9bbe83e. P27, P24 and every UD-backed step ran on the Mac (queue jobs 355 to 362). P25 single points ran on GitHub Actions run 37423042495, P26 optimizations on run 37426006692 (pyscf 2.14.0, pyberny 0.7.0, RDKit 2026.03.6). Machine-readable outputs are in `docs/astra/round5/data/`.

## Long-chain diagnosis (recorded with the registration)

Before round 5, the six stalled chains were diagnosed from their pickled Berny states, with no new quantum calculations:

- **Forces are converged.** Internal gradient RMS is 3.8e-6 to 1.2e-5 against the 1.5e-4 limit.
- **Every step is clipped to the trust radius**, which Berny counts as "not converged". The trust radius has collapsed to 3e-4 to 3e-3 (L2 norm over 275 to 357 coordinates). The cause is that predicted energy changes (6e-8 to 3.5e-7 Eh) are the size of the energy noise.
- **The learned Hessians have soft modes** (lowest eigenvalue 2e-4 to 3e-3). The unconstrained step is therefore 0.04 to 0.27 long, which fails the step limits even without the trust radius.
- **A fresh model-Hessian optimizer would also fail** the step-maximum test at these points.

The chain drivers were stopped. A pgrep race had also left two processes optimizing FLIACVVOZYBSBS on the same checkpoint files. profiles_v2 stays 630/636 with the six flagged S1/S2.

## P27, regenerated scorecard

All nine model/profile arms ran in fresh processes on the frozen has_sigma universe. Every LLE arm passed its 20-good-call control gate. Test split, standalone:

| model / profiles | IDAC MAE (rows) | VLE AAD% (rows) | HE MAE J/mol (rows) | LLE gap-found rows (systems) |
|---|---|---|---|---|
| Z0x / UD | 0.839 (828) | 16.13 (12,551) | 619 (8,573) | 0.890 (0.842) |
| Z0x / open630 | 0.942 (816) | 16.41 (12,403) | 699 (8,573) | 0.883 |
| Z0x / open636 | 0.977 (828) | 16.61 (12,551) | 699 (8,573) | 0.884 |
| COSMO-SAC 2010 / UD | 0.871 (828) | 11.79 | 437 | 0.688 |
| COSMO-SAC 2010 / open630 | 0.987 (816) | 11.97 | 467 | 0.629 |
| COSMO-SAC-dsp / UD | 0.679 (762) | 13.99 (10,709) | 435 (7,508) | [0.683, 0.754], 177 unresolved |
| COSMO-SAC-dsp / open630 | 0.800 (750) | 14.22 | 463 | [0.631, 0.703], 177 unresolved |

Paired on identical rows, Z0x test IDAC is 0.804 for UD [CI 0.687, 0.933] against 0.942 for open630 [0.822, 1.075] on 816 rows. HE sign correctness is 0.838 for UD against 0.799 for open. The reproduced numbers match the historical ones exactly: 0.839/828 and 0.800/750 COSMO-SAC-dsp open. All-split tables, coverage counts and pairwise CIs are in `data/scorecard_all.md`, `data/scorecard_test.md` and `data/scorecard_test.json`.

## P24, Z0x term accounting (859-row panel, no experimental values)

- The component identity holds on every row. Combinatorial changes are at most 3e-13, and London changes are exactly 0 in every intervention.
- The H2O/COOH flag cannot reach Z0x. Every change lives in the residual term, including its endpoint differentiation.
- Charge projections (area-zero / capacitary-zero) change the residual by a mean of +0.325 / +0.322 (mean |Δ| 0.35, max 1.26):
  - Split across all rows: ES +0.12, HB +0.21.
  - Water as solvent carries most of it: +0.57, of which HB +0.40 and ES +0.17.
  - Glycols as solvent: +0.05 to +0.15, almost entirely ES.
- UD-shape-only substitution, solvent rows of that molecule:

| molecule | Δ total | ES | HB |
|---|---|---|---|
| ethylene glycol | +2.35 | +1.82 | +0.53 |
| diethylene glycol | +1.37 | +1.05 | +0.33 |
| triethylene glycol | +1.14 | +0.74 | +0.40 |
| water | +1.02 | +0.74 | +0.28 |
| methanol | +0.21 | +0.16 | +0.05 |
| n-nonane | −0.05 | −0.05 | 0.00 |

- Endpoint-stencil controls (h = 1e-5, 1e-6) differ from the production stencil by at most 3e-3 on these rows. The exception is the water UD-shape arm, at 0.26: the one-sided h = 1e-4 stencil is not converged for that profile.

## P25, shape-stage matrix (36 single points, all gates passed)

- **Gates.** All 36 single points finished, the independent Hsieh implementation agrees to at most 3e-17, and binwise HB conservation holds. The descriptor step ran on the 12 panel members only, because validation member QCDWFXQBSFUVSP has no UD profile (deviation).
- **TZVP/SWIG reproduces the stored open profiles.** Polar tail in Å² for diethylene glycol: 27.65 here against 27.7 stored.
- **Averaging recipe changes almost nothing.** Hsieh, coincident-4 subdivision and the point limit change the tail by at most 0.2 Å² and the normalized L1 to UD by at most 0.004.
- **ISWIG versus SWIG** changes the tail by at most 0.1 Å² (tetraethylene glycol).
- **SVP versus TZVP** lowers the tail by 2 to 3 Å² for every polar molecule, which moves away from UD. It also raises L1 to UD in all but tetraethylene glycol.
- **Raw charges already carry the deficit.** Raw |σ| ≥ 0.01 area (TZVP/SWIG) is 40.7 Å² for diethylene glycol and 31.2 Å² for water. So the gap is present before averaging and the HB split.
- **Final tail, TZVP/SWIG versus UD (Å²):**

| molecule | TZVP/SWIG | UD |
|---|---|---|
| water | 26.5 | 27.7 |
| methanol | 15.7 | 17.9 |
| ethylene glycol | 23.0 | 33.0 |
| diethylene glycol | 27.7 | 38.0 |
| triethylene glycol | 27.9 | 42.3 |
| tetraethylene glycol | 41.8 | 46.8 |
| glycerol | 37.3 | 35.0 |
| propylene glycol | 30.0 | 25.9 |
| 2-methoxyethanol | 21.0 | 23.9 |
| dimethoxyethane | 14.4 | 14.4 |
| THF | 8.4 | 9.6 |

- **Conclusion.** No basis, cavity-switching or averaging variant closes the 10 to 14 Å² deficit for EG, DEG and TEG, while the rigid controls are within about 2 Å². Glycerol and propylene glycol go the other way.

## P26, conformer probe (two pools, ranks 0 and 1, ten non-rigid members)

- **Runs.** 39 of 40 optimizations ran; median 8 gradient evaluations, at most 2,061 s.
  - 36 reached a stationary sample.
  - Three were censored at the 80-evaluation cap: n-nonane s20261006-c1, triethylene glycol s20261006-c1 and dimethoxyethane s20261005-c1. They show the same slow, flat-surface Berny behaviour as the long chains.
  - One tetraethylene glycol proposal (s20261006-c1) never ran. Its slot stopped after an earlier censored member raised in the slot loop (check=True).
- **Selection.** The registered selection therefore ran for the six members whose pools were complete.

| member | pool ΔE (kcal/mol) | pool RMSD (Å) | pool L1 | winner vs saved geometry (kcal/mol) | selected tail / open / UD (Å²) | trigger pairs |
|---|---|---|---|---|---|---|
| ethylene glycol | 0.01 | 0.60 | 0.064 | −0.01 | 22.8 / 23.0 / 33.0 | 6 (L1 to 0.32) |
| diethylene glycol | 0.00 | 0.00 | 0.000 | +0.02 | 23.7 / 27.7 / 38.0 | 2 (L1 0.38) |
| glycerol | 1.01 | 0.84 | 0.230 | −1.28 | 28.9 / 37.3 / 35.0 | 6 |
| propylene glycol | 0.00 | 0.45 | 0.083 | −0.94 | 22.2 / 30.0 / 25.9 | 5 |
| 2-methoxyethanol | 0.00 | 0.00 | 0.000 | −1.46 | 13.7 / 21.0 / 23.9 | 0 |
| THF | 0.00 | 0.00 | 0.000 | −0.01 | 8.3 / 8.4 / 9.6 | 4 (L1 0.03) |

- **The continuation trigger was met** in five of the six complete members: a pair within 3 kcal/mol, RMSD ≥ 0.2 Å, L1 ≥ 0.02. Within 3 kcal/mol, conformers change the normalized profile by L1 up to 0.38, larger than any method or averaging effect in P25.
- **Energy-minimum selection moves glycol tails the wrong way.** Picking the lowest conductor-energy conformer moves the glycol and glycerol tails further below UD, not toward it. Diethylene glycol drops to 23.7 Å² against 27.7 open and 38.0 UD.
- **Decision (Victor, 2026-10-06).** The full P26 protocol is not continued. The 4 incomplete members block any P26 acceptance, and no conformer profile is scored or adopted.

## Deviations and notes

- The P25 descriptors ran on the panel only. QCDWFXQBSFUVSP (validation) has no UD profile; it is not needed for the P26 gate.
- In the P26 probe workflow, one censored member stopped its slot (check=True), so one proposal never ran.
- P25 and P26 ran on GitHub Actions as registered; P27 and P24 ran on the Mac.
