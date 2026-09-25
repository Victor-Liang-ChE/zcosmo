# Scorecard (test)

## IDAC  (889 points, 200 systems, common subset)

| model | coverage | MAE ln g_inf | 95% CI | median AE | within 0.3 | bias | selectivity rho | dMAE vs ref (CI) |
|---|---|---|---|---|---|---|---|---|
| unifac_do | 0.88 | 0.556 | [0.437, 0.674] | 0.210 | 0.65 | +0.148 | 0.68 (118) | [-0.335, -0.150] |
| cosmosac_dsp | 0.95 | 0.802 | [0.685, 0.921] | 0.465 | 0.31 | +0.108 | 0.31 (118) |  |

## VLE bubble pressure (10633 points)

| model | coverage | AAD P % | 95% CI | median AD P % | AAD y | dAAD vs ref (CI) |
|---|---|---|---|---|---|---|
| unifac_do | 0.81 | 9.23 | [6.88, 12.26] | 2.72 | 0.0211 | [-1.32, +0.91] |
| cosmosac_dsp | 0.82 | 9.51 | [7.24, 12.31] | 3.29 | 0.0123 |  |

## Excess enthalpy (6408 points)

| model | coverage | MAE J/mol | 95% CI | sign correct |
|---|---|---|---|---|
| unifac_do | 0.86 | 498 | [332, 706] | 0.92 |
| cosmosac_dsp | 0.96 | 427 | [368, 491] | 0.92 |

## LLE

| model | points | systems | gap found (systems) | MAE x when found |
|---|---|---|---|---|
| unifac_do | 2895 | 207 | 0.42 | 0.123 |
| cosmosac_dsp | 2895 | 207 | 0.40 | 0.147 |