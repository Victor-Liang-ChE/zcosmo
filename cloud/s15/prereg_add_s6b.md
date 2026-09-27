- bench12 RESULT (2026-09-26 10:25 AM PDT, recorded before any follow-up):
  A2) Batching is exact (max|dF| 2.1-3.4e-6 eV/A for every replica count). Throughput on the L4 relative
      to one 192-atom box at 36.7 ms/call (bench11): 16 boxes in one call 44.4 ms -> 2.8 ms per box (~13x);
      648-atom boxes 36.3 -> 9.3 ms per box at 8 per call (3.9x). ACCEPTED; MultiMACE is the production engine
      for independent replicas and lambda windows.
  D2) Cavity path, water decoupled from 63 waters, 22 windows batched (96.3 ms/step for all, ~25x vs running
      the windows serially with 3 calls each), 9 ps/window: no non-finite forces; min neighbour MBAR overlap
      0.140 (stage 1) and 0.145 (stage 2), >= 0.03; TI -7.434 vs MBAR -7.489 kcal/mol (agree within 1 SE);
      TI standard error 0.336 kcal/mol > 0.3 bar -> gate FAILED on precision only (stage 2 alone 0.281).
      The divergence of bench11 D is gone (<dU/dl> at l = 0 is +0.085 +- 0.015 eV). Orientation only, not
      used for any decision: MACE-OFF23-small gives -7.4 kcal/mol for water in its own liquid (experiment
      about -6.3), in line with its ~10% density overestimate.
- Methanol hydration feasibility (registered 2026-09-26 10:40 AM PDT, before running; bench13, Modal L4):
  identical path, windows, WCA constants, integrator and estimators as bench12 D2; system: methanol replacing
  one water (the nearest other water removed; 62 waters, same box, MACE FIRE relaxation to fmax 0.3 eV/A);
  production raised from 8 to 20 ps per window because the only bench12 failure was statistical precision
  (SE scales as 1/sqrt(time); no free-energy value informed this). Gate as registered earlier: min neighbour
  overlap >= 0.03, TI standard error <= 0.3 kcal/mol, plus finite forces and TI-MBAR agreement within 2 SE.
  The number is compared with experiment only after the gate is judged, and no model is changed from it.
