# Scorecard (test)

## IDAC  (723 points, 166 systems, common subset)

| model | coverage | MAE ln g_inf | 95% CI | median AE | within 0.3 | bias | solvent-rank rho | dMAE vs ref (CI) |
|---|---|---|---|---|---|---|---|---|
| unifac_do | 0.94 | 0.443 | [0.344, 0.566] | 0.203 | 0.64 | -0.047 | 0.96 (6) | [-0.460, -0.287] |
| cosmosac2010 | 1.00 | 0.817 | [0.711, 0.920] | 0.559 | 0.15 | -0.472 | 0.93 (6) |  |
| cosmosac_dsp | 0.92 | 0.678 | [0.583, 0.782] | 0.449 | 0.25 | -0.312 | 0.93 (6) | [-0.175, -0.102] |

## VLE bubble pressure (9544 points)

| model | coverage | AAD P % | 95% CI | median AD P % | AAD y | dAAD vs ref (CI) |
|---|---|---|---|---|---|---|
| unifac_do | 0.77 | 11.22 | [7.06, 18.15] | 3.16 | 0.0262 | [-0.78, +7.90] |
| cosmosac2010 | 0.88 | 8.59 | [7.15, 10.25] | 3.66 | 0.0167 |  |
| cosmosac_dsp | 0.75 | 9.18 | [7.37, 11.28] | 3.58 | 0.0142 | [+0.06, +1.22] |

## Excess enthalpy (6812 points)

| model | coverage | MAE J/mol | 95% CI | sign correct |
|---|---|---|---|---|
| unifac_do | 0.87 | 323 | [239, 432] | 0.92 |
| cosmosac2010 | 0.99 | 410 | [352, 464] | 0.95 |
| cosmosac_dsp | 0.87 | 410 | [348, 466] | 0.95 |

## LLE

| model | points | systems | gap found (systems) | MAE x when found |
|---|---|---|---|---|
| unifac_do | 2475 | 101 | 0.65 | 0.112 |
| cosmosac2010 | 2475 | 101 | 0.67 | 0.140 |
| cosmosac_dsp | 2475 | 101 | 0.67 | 0.139 |