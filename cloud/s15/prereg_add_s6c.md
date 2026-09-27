- Methanol hydration feasibility RESULT (bench13, finished 2026-09-26 11:49 AM PDT; recorded before follow-up):
  finite forces throughout; min neighbour MBAR overlap 0.146 (stage 1) / 0.156 (stage 2) >= 0.03; TI -6.254 vs
  MBAR -6.409 kcal/mol (within 1 SE); TI standard error 0.361 kcal/mol > 0.3 -> gate FAILED again on
  precision. Diagnosis (post hoc, from the saved samples): 2.3x longer sampling did not shrink the 5-block SE
  because the variance sits in two places: the steep soft-core region of stage 1 (mu 0.05-0.1, 36% of the
  variance) and stage 2 at l = 0.7-0.8, where dU/dl decorrelates in 1.8-2.6 ps (38%). Autocorrelation-based
  TI SE 0.327; MBAR block bootstrap -6.37 +- 0.27 (MBAR is not the registered estimator; reported only).
  Orientation (not used for decisions): -6.3 to -6.4 vs experiment about -5.1 kcal/mol; water in water was
  -7.4 vs -6.3, i.e. MACE-OFF23-small over-binds both by ~1.1-1.3 kcal/mol, which would largely cancel in
  ln gamma_inf = beta[mu_ex(i in j) - mu_ex(i in i)] + ln(rho_j/rho_i) if it is solute-specific.
- Methanol hydration, retry 3 (registered 2026-09-26 12:10 PM PDT, before running; bench14): same system, path
  constants, integrator and gate (TI 5-block SE <= 0.3 kcal/mol, overlap >= 0.03, TI-MBAR within 2 SE). Only
  window placement and length change, targeted at the measured variance: stage 1 mu = 0, .025, .05, .075, .1,
  .15, .2, .35, .5, .65, .8, .9, 1; stage 2 l = 0, .05, .1, .2, .3, .4, .5, .6, .65, .7, .75, .8, .85, .9, 1;
  30 ps production per window (28 windows batched). If this fails, the direct route is recorded as not
  feasible at this precision on free compute and the pilot is not registered.
