
## Proposed R2 noise-aware Berny trial, class A

Register this text with its actual commit timestamp before any trial profile or
score is read. This trial is motivated by the previously observed stalls, so it
is not a blind discovery. Pyberny is fixed at 0.7.0. Its energy_noise parameter is
set to 2e-7 Eh, including in a restored BernyState; every energy, gradient, basis,
auxiliary basis, XC grid and PCM setting is unchanged. The original Berny
convergence criteria, including the on-sphere condition, remain mandatory.
No experimental response selects this value. There is one candidate, no sweep.

The comparison uses the historical 25-molecule/2302-row manifest, with identical
finite coverage. All 25 candidates must pass the original Berny test; maximum
absolute change in COSMO-SAC-dsp ln gamma-infinity against current-main profiles
must be below 0.01; the median absolute difference against UD must remain below
0.15. Report both normalized distributions and raw psigmaA bins, without
reinterpreting either existing E or fallback limit. Paired total wall time on
the 25 molecules must be no more than 1.10 times reference. Separately freeze and
hash the six current long-chain geometries before the trial. Run at most 100 new
CPU gradient evaluations per chain, from the same geometry and optimizer state
in each arm, with the same already-accepted A-class restart protocol. At least
one formerly stalled chain must newly pass the original Berny test within that
budget, and all resulting profiles remain exploratory until the 25-molecule
checks pass. An unfinished arm is censored, not assigned an invented time to
convergence. No S1 failure is reclassified by this trial. Rejection leaves the
accepted GPU-prestage and A-class restart protocols unchanged.
