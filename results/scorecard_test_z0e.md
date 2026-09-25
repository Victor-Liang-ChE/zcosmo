# Scorecard (test)

## IDAC  (812 points, 200 systems, common subset)

| model | coverage | MAE ln g_inf | 95% CI | median AE | within 0.3 | bias | solvent-rank rho | dMAE vs ref (CI) |
|---|---|---|---|---|---|---|---|---|
| cosmosac2010 | 1.00 | 0.869 | [0.777, 0.964] | 0.633 | 0.15 | -0.583 | 0.89 (10) | [-0.064, +0.156] |
| Z0 | 0.98 | 0.814 | [0.664, 0.950] | 0.480 | 0.31 | -0.188 | 0.81 (10) |  |
| Z0e | 0.98 | 0.834 | [0.706, 0.966] | 0.562 | 0.27 | -0.246 | 0.79 (10) | [-0.003, +0.046] |

## VLE bubble pressure (12311 points)

| model | coverage | AAD P % | 95% CI | median AD P % | AAD y | dAAD vs ref (CI) |
|---|---|---|---|---|---|---|
| cosmosac2010 | 0.88 | 11.93 | [9.87, 14.11] | 4.21 | 0.0237 | [-11.47, -5.25] |
| Z0 | 0.86 | 20.06 | [16.50, 23.99] | 6.82 | 0.032 |  |
| Z0e | 0.86 | 17.46 | [14.29, 20.96] | 5.17 | 0.0286 | [-3.53, -1.84] |

## Excess enthalpy (8004 points)

| model | coverage | MAE J/mol | 95% CI | sign correct |
|---|---|---|---|---|
| cosmosac2010 | 0.99 | 431 | [377, 488] | 0.90 |
| Z0 | 0.93 | 630 | [556, 712] | 0.82 |
| Z0e | 0.93 | 613 | [537, 698] | 0.83 |
