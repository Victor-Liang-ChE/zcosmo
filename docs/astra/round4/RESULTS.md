# Round 4: measured results

Reference: round 4 registered 2026-10-05 12:02 PDT (commit b61301d, your patches applied unchanged on 33ebac0). Frozen P22 native panel and workflow in 3216fbe. Every UD-backed step ran on the Mac (queue jobs 337 to 347). P22 single points ran on GitHub Actions run 37367539367 (pyscf 2.14.0), except n-nonane (see deviations).

## P20, COOH deployment: applied

- `r4_metadata.py prepare/verify` on all 636 selected profiles (630 profiles_v2, five S2, one S1). Bundle manifest sha256 `e203da8ee623ce78ca89dfde4e46f3b0b72613fc2d01978303fd565be10bc4c5`. Raw bodies after the first line are byte-identical. Only the flag and provenance fields change.
- 30 profiles change flag, all HB-DONOR-ACCEPTOR → COOH. One of them, OYHQOLUKZRVURQ, is a flagged S2 profile. No other flag transition occurred.
- 25/2,302 gate: coverage identical (Z0x 2,302 finite, COSMO-SAC-dsp 2,271), Z0x max change 0, COSMO-SAC-dsp max change on changed targets 0.319, UD compatibility median 0.1362 (limit 0.15). Passed.
- Full IDAC invariance (3,252 rows, separate processes): Z0x and COSMO-SAC 2010 both max |Δ ln γ∞| = 0 with identical prediction hashes.
- Open-profile COSMO-SAC-dsp test IDAC, without the flagged chains (750 rows, 175 systems): MAE 0.8009 → 0.8001, bias −0.544 → −0.546.
- Applied in job 337, with a rollback copy kept. COSMO-SAC-dsp with the corrected open profiles was rescored into a new directory, `results/predictions_p18_dsp` (IDAC 3,252 / VLE 43,042 / HE 24,777 / LLE 6,581 rows). No historical output was overwritten.

## P23, LLE accounting and repair

Accounting of the existing P14 sidecar (Z0x, no prediction changed):

| split | rows / systems | unique calls | unresolved rows | row gap-found bounds | system bounds | composition MAE (n) |
|---|---|---|---|---|---|---|
| all | 6,581 / 303 | 2,255 | 554 | [0.761, 0.845] | [0.683, 0.795] | 0.171 (5,009) |
| test | 2,475 / 101 | 716 | 103 | [0.848, 0.890] | [0.752, 0.842] | 0.183 (2,099) |

Statuses on all rows: 5,009 roots pass the sampled checks, 1,018 no gap on the 81 grid, 430 residual failed, 114 negative margin, 10 hull fallback.

- Control gate: the first 20 sorted good calls, re-solved by the strict repair, all keep a root that passes, with endpoints within 1e-4 of the stored ones. The legacy replay matched for every call. Passed.
- Measured batch: 20 unresolved test calls in 13 s (7 refined roots, 13 gap witnesses only).
- Full repair, frozen list of all 280 unresolved calls: 127 s wall, 113,782 model calls. Result: 136 roots pass the refined checks, 144 gap witnesses only, 0 no gap, 0 still unresolved.
- Re-accounting with repairs: unresolved rows 0 in both splits. Gap-found becomes exact and equals the old upper bound: all rows 0.8453, systems 0.7954; test rows 0.8897, systems 0.8416. Composition MAE on checked detections: all 0.1647 (5,278 rows), test 0.1799 (2,142).
- Every unresolved call has a gap. For 144 of them the gap is supported only by a nonconvexity witness, and those rows carry no accepted endpoint compositions. The old gap-found statistic therefore stands. The composition MAE denominator grows by 269 (all) and 43 (test) rows.

## P21, polyol/ether inventory and A/V/shape factorial

- Inventory: 96 keys (structural polyols and ethers plus the four controls), selected before any error was inspected. No UD `.cosmo` geometries exist on disk (`validation_data.zip` is a single CSV), so UD geometries are unavailable. Open geometries exist for all.
- Factorial: 332 frozen paired rows over 14 solvents, all eight corners plus full UD solvent finite for every row. Corner 000 reproduces the stored open prediction to 8e-11 and corner 111 equals full UD solvent exactly. The Shapley identity holds to 1e-10. Accepted as executed.

| corner | MAE |
|---|---|
| all open (000) | 1.311 |
| UD area only | 1.317 |
| UD volume only | 1.305 |
| UD shape only | 0.845 |
| UD solvent (111) | 0.836 |

Per solvent (mean Shapley contributions to ln γ∞, open → UD solvent):

| solvent | rows | MAE open | MAE UD solvent | ΔA | ΔV | Δshape | open bias |
|---|---|---|---|---|---|---|---|
| diethylene glycol | 108 | 1.740 | 0.371 | −0.000 | 0.018 | 1.372 | −1.730 |
| glycerol | 80 | 0.789 | 0.874 | −0.019 | 0.014 | 0.037 | −0.406 |
| water | 62 | 1.546 | 2.073 | 0.006 | −0.005 | 1.057 | 0.683 |
| triethylene glycol | 17 | 2.088 | 0.556 | 0.005 | 0.029 | 1.497 | −2.088 |
| tetrahydropyran | 10 | 0.357 | 0.330 | 0.027 | 0.007 | −0.007 | −0.357 |
| 1-butanol | 9 | 0.390 | 0.345 | 0.011 | 0.018 | 0.016 | −0.390 |
| ethylene glycol | 9 | 2.482 | 0.387 | −0.002 | −0.016 | 2.550 | −2.482 |
| methanol | 9 | 0.206 | 0.086 | −0.010 | −0.001 | 0.257 | −0.188 |
| 1,1-diethoxyethane | 8 | 0.211 | 0.228 | 0.013 | 0.049 | −0.045 | 0.211 |
| tetraethylene glycol | 7 | 1.243 | 0.731 | 0.008 | 0.038 | 0.465 | −1.243 |
| nonane | 6 | 0.795 | 0.792 | 0.010 | 0.034 | −0.047 | 0.795 |
| methyl cellosolve | 4 | 0.364 | 0.459 | −0.033 | −0.006 | 0.221 | −0.364 |
| propylene glycol | 2 | 1.002 | 1.916 | −0.048 | −0.004 | −0.861 | −1.002 |
| 1,2-dihydroxyethane | 1 | 3.075 | 1.491 | −0.004 | −0.034 | 1.622 | −3.075 |

- Area and volume contribute less than 0.05 for every solvent. The normalized 153-bin shape carries the whole substitution effect.
- In the glycols (EG, DEG, TEG, tetraethylene glycol) the open shape makes the alkane/alkene solutes far too soluble: bias −1.2 to −2.5, removed by the UD shape. Glycerol, propylene glycol and the mono-ethers show little or the opposite effect.
- Water as solvent has a large shape effect of the same sign (+1.06), but there the UD shape makes the error worse (1.55 → 2.07). So "UD shape is better" is not a general rule. The glycol shape difference is something specific to those geometries or profiles.
- By solute class: aliphatic hydrocarbons (199 rows) Δshape +1.00, MAE 1.38 → 0.45; alcohols (46) Δshape +1.03 but MAE 1.60 → 2.49 (mostly water-solvent rows); aromatics (53) Δshape +0.07.

## P22, net surface charge

Analytic and sphere-native checks (Gaussian sphere, He-like source, radius 4):

- t = 6: screening charge 0 to 1e-16 at Lebedev 29/41/59.
- t = 1.5: continuum −0.033895 e; discrete −0.034250 / −0.034077 / −0.033984 e at orders 29 / 41 / 59. The discrete error falls with order (−3.6e-4 → −8.9e-5). The PCM layer reproduces the analytic outlying-charge value for a neutral source.

Native open-geometry panel (BP86/def2-TZVP, Lebedev 29, ε = 1e9, all SCF converged, electron counts exact):

| compound | raw Σq (e) | order 41 | order 59 | radius × 1.10 | quadrature gate |
|---|---|---|---|---|---|
| ethylene glycol | −0.02258 | | | | not run |
| methanol | −0.01864 | | | | not run |
| triethylene glycol | −0.03543 | | | | not run |
| diethylene glycol | −0.03041 | −0.03030 | −0.03026 | −0.01608 | fails (inconclusive) |
| water | −0.01241 | −0.01243 | −0.01245 | −0.00587 | fails (inconclusive) |
| n-nonane (Mac) | −0.04481 | −0.04433 | −0.04414 | −0.02525 | fails (inconclusive) |

- The net charge does not converge away with the Lebedev order (changes from order 29 to 59 of 1.5e-4 e for DEG and water and 6.7e-4 e for nonane), so it is not a Lebedev discretization defect. Enlarging the cavity by 10 percent roughly halves it, which is the signature of electron density penetrating outside the cavity.
- Quadrature gates as registered: DEG's level-4 and level-5 inside defects differ by 3.3e-4 e (bound 1e-4). Water's level-5 reconstructed-charge error is 1.27e-5 e (bound 1e-5). Nonane's level-5 electron-count error is 1.4e-5 and its inside defects differ by 6.6e-4 e between levels. All three are therefore inconclusive, and the inside/outside split is not interpreted, although at both levels the outside-electron contribution is about the size of the screening charge (DEG 0.031, water 0.0127, nonane 0.045 e).
- Zero-charge projections (uniform area shift and capacitary shift, sums below 1e-16): they change the final profiles very little. Averaged net σ moment: EG −0.0227 → −0.0001 / −0.0002; DEG −0.0339 → −0.0034 / −0.0037; TEG −0.0350 → +0.0004 / +0.0002; nonane −0.0424 → +0.0024 / +0.0020; water −0.0128 → −0.0004 / −0.0005; methanol −0.0188 → −0.0002 / −0.0002. Tail area changes by at most 0.3 Å² (DEG 27.65 → 27.84 / 27.92 Å², against UD 38.0). OH/OT/NHB areas change by at most 0.3 Å².
- Prediction comparison (job 347): 859 IDAC rows touching the six panel compounds, open background profiles, one fresh process per variant. Finite masks are identical in every variant (Z0x 859, COSMO-SAC-dsp 845). The fresh native profiles reproduce the stored open profiles to 3e-5 in ln γ∞.

| variant | Z0x max / mean abs change vs native | Z0x MAE | dsp max / mean abs change | dsp MAE |
|---|---|---|---|---|
| native (= stored open) | 0 / 0 | 1.783 | 0 / 0 | 1.184 |
| area_zero | 1.264 / 0.349 | 1.667 | 0.567 / 0.175 | 1.215 |
| capacitary_zero | 1.260 / 0.347 | 1.668 | 0.562 / 0.174 | 1.216 |

  The two projections agree with each other closely. They are small in the profile but not in Z0x: the mean change is 0.35 in ln γ∞, so Z0x is sensitive to the net σ moment. Z0x MAE by solvent, native → capacitary_zero: DEG 1.740 → 1.640 (UD solvent 0.371), TEG 1.591 → 1.544, EG 2.259 → 2.132, water 1.945 → 1.767, methanol 0.241 → 0.224. As registered, none of this is used to adopt anything.
- Conclusion: the −0.01 to −0.045 e net charge behaves like outlying charge from the electron density, not like a discretization defect. Neutralizing it barely changes the profile areas, but Z0x responds with a mean change of 0.35 in ln γ∞. It accounts for under a tenth of the DEG deficit (1.740 → 1.640 against 0.371 with the UD solvent), so it is not the glycol mechanism. Nothing is adopted.

## Deviations and execution notes

- The P22 UD-geometry arm (EG, DEG and TEG at UD geometries) could not run: no UD `.cosmo` or geometry files exist on the Mac, and `validation_data.zip` contains only a CSV. The open arm ran alone.
- P22 venue: the first dispatch of run 37367539367 was never picked up by a hosted runner. The retry ran normally, but its n-nonane job was killed after 3 minutes (exit 143, consistent with memory during the level-5 quadrature). The identical registered command ran on the Mac instead (job 346, 135 s, peak memory 20 GB, which explains the runner kill on a 16 GB runner). Job 347 started while job 346 was still in its quadrature step. The nonane .sigma and projection files it used are written before the quadrature, and the fresh native profiles match the stored ones to 3e-5.
- P20 was applied before P23 and P21, in the registered order. The P23 repair used the full frozen list of unresolved calls after the 20-call control gate and the measured batch.
- The six-chain campaign stayed closed. The 4070 and PC2 continue the old protocol with no new completions (630/636 Berny-converged).
