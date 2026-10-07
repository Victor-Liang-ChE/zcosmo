Round-8 proposed registration. This text is not a claim that it has been adopted.
Append the accepted text with the actual commit timestamp before new candidate
computation. The source baseline is 58cc629df42156c0b7862710057318db0a495dbb plus
these archived R8 helpers. The hypotheses are motivated by known R7 outcomes;
this is neither a new ThermoML holdout nor selection by experimental error.

P32 remains rejected under its actual maximum-dsp compatibility limit of 0.01.
Neither its 0.012074 result nor the small median changes authorize its pilot or
chain stages. The six stopped chains retain S1/S2 labels and receive no native
budget in R8. The 630 primary profiles remain a frozen original-gradient data
version. R8 authorizes no re-polish, new profile, profile promotion, re-scoring,
conformer weighting, or change to a production default. P35 stays unresolved.
P20 and P28 retain their accepted, explicitly scoped status. P28 remains opt-in
in the current code; this registration does not change its deployment switch.

P36 is E read-only bookkeeping. Reproduce the archived R7 denominators and
recorded decisions, preserving native failures and inconclusive directions.
Report P32 timing from its paired runs. Do not infer a count or identity of
above-limit queries from an extrema-only JSON. Keep P34's 35 positive screens,
four affinity-coverage failures and one unfinished native case separate. Do
not estimate population prevalence or turn fixed-displacement sensitivity into
an error estimate at the corrected minimum. Historical files remain unchanged.

P37 is one final A stage-isolation diagnostic, not a relaxed referee or an
optimizer trial. Freeze exactly the archived P33 TEG bond-3-4 direction that
was resolved inconsistent with full response and the EG bond-2-3 consistent
control. They are targeted diagnostic identities, not a random sample. Use
their existing full-precision unit-L2 Cartesian vectors and exact generating
geometry hashes from cloud/r7/referee and docs/astra/round7/data/referee.
No new conformer, reorientation, random direction or step-size selection is
allowed. Freeze the plan and code hashes before native output.

Cross PCM on/off with the existing angular pruning/None, yielding four arms
per case and eight jobs in total. Use BP86/def2-SVP, the existing DF auxiliary
basis, XC grid level 2, and, when attached, C-PCM epsilon 1e9, Lebedev 17 and
project radii. The no-PCM arms are genuine vacuum controls at the same nuclear
coordinates, not claims that their electron density matches the PCM density.
Check the actual runtime small_rho_cutoff is zero. An unexpected nonzero value
is an environment mismatch and stops the job; do not silently force it to zero.
Angular pruning and density-based point removal are different settings.

Pin PySCF 2.14.0 and pyberny 0.7.0 using normalized package versions. Record
NumPy/SciPy versions and the loaded upstream source hashes. Native jobs use
four OpenMP threads, one BLAS thread, 4000 MB nominal PySCF memory and a 2000 MB
PCM integral cache. No tighter integral threshold, denser radial grid, alternative
SCF solver, modified PCM switching, or other functional/basis is substituted.

Per arm compute tight and strict center SCFs, with (conv_tol,conv_tol_grad)
equal to (1e-11,1e-7) and (1e-12,1e-8), respectively. Compute tight/full-response,
strict/full-response and strict/off center gradients, retaining DF auxiliary
and, where present, PCM derivatives. Compute both signs of the fixed Bohr
ladder 0.016,0.008,0.004,0.002,0.001 at each precision. All five energy pairs
are required; the finest Richardson estimate is the reference, not a selected
best-agreement step. This is exactly 22 SCF calls and three full molecular
gradient calls per completed arm.

Retain P33's tau=1e-5 Eh/Bohr and its unchanged finite-resolution decision rule.
The uncertainty indicator is the difference of the finest strict Richardson
estimates plus tight/strict, center-gradient and roundoff indicators. Require
its value at most tau/4 and stabilization. Consistency requires discrepancy
plus indicator at most tau; inconsistency requires discrepancy minus indicator
greater than tau; other outcomes are inconclusive. This is not a rigorous
interval enclosure. No outcome is promoted by increasing uncertainty or changing
a threshold. The old P33 and P30 decisions are never overwritten or re-gated.

Track retained XC points by generating atom and atomic-template ordinal,
ignoring zero-weight padding, and PCM points by generating atom and Lebedev
ordinal. Equal point counts alone do not establish identical membership. A
membership change along a ladder makes its assessment inconclusive. Compare
the SCF quadrature with the full-response quadrature at both centers, requiring
identical node membership and matching weights (absolute 1e-12, relative 1e-10).
A discrepancy is recorded and also makes the derivative verdict inconclusive.
These are quadrature representation checks, not universal AO-screening proofs.

In each PCM/pruned arm additionally test the explicit PCM partial derivative
at the strict center. Freeze the AO density coefficient matrix P0, retain the
same AO labels and basis, move the atom-centered basis and PCM surface with
the geometry, and solve the surface charges anew. Do not set frozen=True.
Compare the derivative of E_PCM(R,P0) with PCM.grad(P0). The off-center overlap
electron count can change because the basis moves; report it, never renormalize
P0. This derivative is not the PCM energy derivative along a relaxed SCF curve
and is not a fixed physical real-space density derivative.

Use stock PCM and the existing CachedPCM3c independently at the center and the
ten displacements: 22 explicit PCM energy calls and two PCM gradient calls per
case. Require linear-solve relative residual at most 1e-10. Cache/stock parity
is an E diagnostic, maximum center/displaced energy difference below 1e-9 Eh and
maximum center gradient difference below 1e-8 Eh/Bohr. Apply the unchanged
finite-resolution ladder calculation to the layer, retaining its interpretation
as two float64 implementations, not an independent high-precision oracle.
No cache implementation is changed or newly accepted by this test.

The budget is eight one-hour four-core native jobs, with a 3400-second internal
deadline and a 3600-second process-group deadline. Maximum totals are 176 SCF
calls, 24 molecular gradients, 44 explicit PCM energy calls and four PCM gradients.
Installation, planning and artifact transfer are outside the native-time count;
no paid resource or guarantee of available account quota is implied. No retry,
continuation, new optimizer history or budget extension is authorized. Reuse
no prior native result as an unlabelled new observation. Preserve every failed
or missing job. Scientific negatives can complete; execution failures must
propagate a nonzero status and receive a terminal execution record. Collection
requires one result and bounded execution record per requested identity.

First require the PCM/pruned baseline to reproduce the TEG inconsistency and
the EG consistency before interpreting another arm as removing that discrepancy.
Failure to reproduce is informative but does not demonstrate a fix.
Interpret only resolved contrasts. An unpruned-arm improvement is evidence
of dependence on angular quadrature, not proof that all pruning is a bug or
that the new energy is physically more accurate. A vacuum/PCM contrast alone
cannot isolate an additive solvent error because the SCF density changes.
A resolved explicit-layer failure localizes an issue to the PCM partial
calculation at this density and surface; it does not by itself identify a
particular switching term. A passing layer and failing total derivative leaves
SCF, other derivative terms or integral/quadrature screening as possibilities.
A cache/stock discrepancy is reported before making a physical attribution.

Neither a pass nor a favorable contrast authorizes corrected-gradient defaults,
a 630-profile re-polish, six-chain jobs, an ensemble or experimental scoring.
If the fixed contrasts remain inconclusive or fail operationally, archive the
unresolved mismatch and close this diagnostic budget. Reopening would require
new independent evidence, auditable inputs or a source-level correction, then
a separate registration. There is no automatic next parameter sweep.

P38 is E reporting only. Append the supplied short README status, linking the
archived evidence. Preserve distinctions between original-predicate convergence,
full-energy stationarity, numerical acceptance and experimental accuracy.
