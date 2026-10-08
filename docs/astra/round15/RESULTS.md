# Round 15: measured results

Reference: round 15 was registered 2026-10-08 in 67f8493, with H15, P54, P55, P56 and REG15 applied unchanged to 3cd0a22. The P54 private plan was frozen in 3655e11. It ran on the Mac in queue job 411, once, with no retry and no quantum chemistry. Its inputs were the 963 P52 rows and 100 systems, reused under P52a with the oracle-plan-p52a and oracle-p52a directories. Row-level predictions stay private. This file reports the allowlisted aggregates.

Test record: all 34 R15 tests pass when run individually in the container. Run as one suite there, 5 of them error on a NumPy 2.4.4 module-reload import-isolation artifact. On the Mac (NumPy 2.4.6) the suite ran before P54, but the job log captured only its fixture output lines, not the unittest summary line. r14_selftest passes.

## P54, contact-ingredient factorial: complete

The run made 7,704 of 7,704 finite requests: 8 corners × 963 rows. Model run time was 722 s, against a planning estimate of 528 s and a cap of 7,200 s. Both anchor corners replayed their archived P52 pressures exactly (maximum relative error 0.0 on 1,926 requests) before the six intermediate corners ran. The Shapley efficiency error is ≤ 3e-14 percentage points.

The bit order is E H D. E is the electrostatic closure, H the hydrogen-bond constants, and D the dispersion term. A 0 means Z0x's ingredient and a 1 means COSMO-SAC 2010's. Effective area and profile convention are identical in both endpoints, so their contributions are exactly zero.

| corner | AAD P % | bias % | equal-system AAD % |
|---|---:|---:|---:|
| 000, stored-ε Z0x | 13.78 | +1.44 | 13.90 |
| 100, 2010 ES closure | 12.63 | −0.35 | 12.73 |
| 010, 2010 HB constants | 13.97 | +6.56 | 14.05 |
| 001, London term removed | 11.76 | −2.79 | 12.00 |
| 110 | 12.86 | +4.66 | 12.94 |
| 101 | 11.04 | −4.34 | 11.26 |
| 011 | 11.00 | +1.53 | 11.24 |
| 111, COSMO-SAC 2010 | 10.44 | −0.02 | 10.65 |

| factor | Shapley error reduction (pp) | share of the 3.35-pp gap | one at a time (pp) | bias change (pp) |
|---|---:|---:|---:|---:|
| London dispersion → none | 2.24 | 67% | 2.02 | −4.47 |
| electrostatic closure → 2010 | 0.88 | 26% | 1.16 | −1.69 |
| HB constants → 2010 | 0.23 | 7% | −0.18 | +4.70 |
| a_eff, profile convention (shared) | 0 | 0 | 0 | 0 |

The biggest interactions are D with H (+0.95 pp, the 011 term) and E with D (−0.43 pp).

Removing the London term carries two-thirds of the VLE gap to COSMO-SAC 2010 on these rows, and that dominance holds in the one-at-a-time view as well. On its own, the London term pushes predicted pressures up: removing it moves the bias by −4.5 pp. Swapping only the hydrogen-bond constants makes AAD slightly worse on its own (+4.7 pp bias). Most of its benefit appears only together with the dispersion change.

The electrostatic closure accounts for about a quarter of the gap. This is consistent with R14, where experimental ε recovered 21% inside the Z0x closure. The two are overlapping counterfactuals and must not be added.

What this means:

- On these 963 already-exposed rows, the D4/London dispersion term is the dominant contributor to Z0x's VLE deficit relative to COSMO-SAC 2010. The ES/dielectric mapping is secondary.
- The original "Next" list targeted the wrong term. That plan rested on the session-1 ablation of conductor-limit Z0, not Z0x.
- The fitted 2010 corners are diagnostics only. "Remove London because it scores better" is selection by ThermoML error and is not a permitted model change.
- Any revision of the dispersion term must come from physics registered before it is scored. Nothing is adopted.

## P55, association dispatch repair: applied

`Z0wBinary.lngamma` again differentiates the full subclass `_g` with the historical stencil. Z0x is byte-identical. No association score was run or authorized.

## P56, manuscript: applied

The revision does three things:

- It replaces the blanket "no fitted constants" wording with "no ThermoML regression of the interaction constants" and lists the retained empirical inputs.
- It adds the R10–R14 evidence.
- It preserves every historical table row, with one scoped model-label edit.

The P54 numbers above are not yet in the manuscript.
