# Astra round 1: measured results

Reference commit 62172c7. Harness H0 with three fixes found while running it (all in `patches/H0.patch`):
(1) `old.T` is the pandas transpose, not the temperature column, so the fixture check always failed;
(2) the snapshot asserted COSMO-SAC is finite for every registered query, but 436 queries (dilute pairs COSMO-SAC
cannot evaluate) are non-finite in main too; they are now recorded and `compare` requires identical coverage;
(3) the Berny wrapper assumed `callback` is a keyword, but `pyscf.geomopt.berny_solver.optimize` passes it
positionally, so every `base`/`P1` QC arm failed immediately (P2/P5 call the kernel with a keyword and ran).

| Id | Class | Gate | Result | Speed |
|---|---|---|---|---|
| P1 PCM LU reuse | E | fixed-geometry: dE < 1e-8, dG < 1e-6, dq < 1e-8 | PASS: water/O2, SVP/TZVP: dE <= 1.1e-13 Eh, dG <= 5.6e-14, dq <= 6.0e-14 | fixed geometry 1.1-1.5x (tiny molecules, 2 threads) |
| P1 | E | 25-molecule profile E-gate | water only so far: identical geometry, max d(psigma) 1.4e-11 A^2; full run = GitHub 36317731128 (base+P1) | water end-to-end 13.3 s -> 6.4 s (2.07x), same 4 geometry evaluations |
| P3 safeguarded Newton, support-restricted | E | max d ln gamma < 1e-3, identical coverage | PASS: 5.9e-9 over 43,934 queries (2,302 IDAC + grid), coverage identical | 1 thread M4 Pro, 3 reps: base 821/721/695 s, P3 170/168/163 s -> 4.5x (4.85x rep 1) |
| P6 analytic Z0x interior derivative | E candidate | same | FAIL as E: max 2.06e-3 (> 1e-3); all excess at x = 0.999 with the dilute component's ln gamma ~ 8-11, e.g. Z0x ethylene-glycol-type pairs at 250 K. Likely main's central difference (h = 1e-4) truncation where g(x) curves sharply, i.e. P6 may be the more accurate one; not accepted until checked against a small-h reference | 1.8x (459/449/442 s) |
| P2 restart hygiene | E | 25-molecule E-gate + resume smoke | pending base arm (P2 arm itself: 25/25 profiles; resume smoke: second resume is a cache hit, 0 geometry evaluations) | pending |
| P5 TRIC pre-stage | A | registered accuracy test | pending base arm (P5 arm: 23/25 profiles, 2 did not finish) | pending |
| P4, P7, P8 | A/E/E | GPU | not run yet (no free GPU slot; Modal credits exhausted until the monthly reset) | - |
