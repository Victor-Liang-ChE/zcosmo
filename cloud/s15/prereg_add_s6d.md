- Methanol hydration retry 3 RESULT (bench14, finished 2026-09-26 2:12 PM PDT, recorded before follow-up):
  finite forces; min neighbour overlap 0.114 / 0.117 >= 0.03; TI -7.033 +- 0.229 (5-block SE <= 0.3),
  MBAR -7.157 kcal/mol (within 1 SE) -> feasibility gate PASSED. Autocorrelation SE 0.208, MBAR block
  bootstrap -7.10 +- 0.22. Caveat recorded now: bench13 (same system and start protocol, coarser windows)
  gave -6.25 +- 0.36; the two differ by 0.78 kcal/mol (1.8 combined SE, mostly stage 1: 3.95 vs 3.31),
  so single-run SEs likely understate the real uncertainty (slow modes longer than the block length).
  Hence the pilot below uses independent replicas. Orientation: experiment about -5.1 kcal/mol.
- Direct-route ln gamma_inf PILOT (registered 2026-09-26 2:40 PM PDT, before any pilot run):
  quantity: ln gamma_inf(i in j) = beta [mu_ex(i in j) - mu_ex(i in i)] + ln(rho_j / rho_i), rho = molar
  densities of the pure liquids from the MACE-OFF23-small NPT runs at 298.15 K (water 1.115 g/cm3, methanol
  0.874; cloud/liquids_results). Systems: methanol/water, both directions, 298.15 K. Four mu_ex runs
  (methanol in water, methanol in methanol, water in water, water in methanol), each: 64 lattice sites at the
  model's pure-solvent density (solute on one site, random orientations, MACE FIRE relaxation), bench14 path,
  windows, WCA constants, integrator and 30 ps/window (skin 0.9 A so the 11.98 A water box fits the GPU list).
  Replicas: seed 1 on Modal L4 now; seed 2 on another free GPU afterwards; mu_ex = replica mean, uncertainty =
  max(propagated TI SE, replica half-range). Fixed-volume boxes at the pure-solvent density are an
  approximation at infinite dilution (recorded, not corrected). Comparison: ThermoML IDAC for methanol in
  water and water in methanol within 293-303 K (and COSMO-SAC 2010 / Z0x predictions on the same points).
  This is a pilot of feasibility and accuracy only: no fitted constant enters, no Z0 model is changed from
  it, and whatever the numbers, extending the route needs its own registration (systems, compute budget).
  Informative outcomes, stated now: |error| <= 0.3 ln units in both directions with uncertainty <= 0.3 would
  justify a larger registered set; |error| > 0.7 in either direction, or uncertainty > 0.5, would shelve it.
