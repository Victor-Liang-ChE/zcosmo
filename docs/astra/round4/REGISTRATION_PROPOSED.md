Round-4 proposed registration. This file is a proposal, not an assertion that it
has been appended to PREREGISTRATION.md or that any native calculation has run.
Commit the adopted text with its actual timestamp before new candidate outputs
are inspected. Reference: 33ebac0146ae2df4dd73fcf8a431cb6d7033554b.

P18 deployment implements the already accepted rule, registration 9d32e9e and
acceptance 613dd8f. It preserves all raw profile bytes after the first newline,
all metadata except the dispersion flag and explicit provenance, and the existing
630 primary plus five S2 plus one S1 partition. The current geometry-based NIST
classifier is authoritative. An unexpected change other than
HB-DONOR-ACCEPTOR to COOH stops deployment for investigation. All 636 selected
profiles and their actual generating geometries are hashed before deployment.
Verify the 25/2302 gate and exact finite coverage on the Mac. Verify Z0x and
COSMO-SAC 2010 prediction invariance to 1e-10 on the full existing IDAC row set;
verify unchanged-target rows on the one-compound COSMO-SAC-dsp check to 1e-10;
report the new UD compatibility statistic. Append the actual deployment receipt
and rerun affected open-profile COSMO-SAC-dsp scores under new output names.
No historical score is overwritten and no flagged geometry is promoted.

P21 is a descriptive mechanism audit, not a fitted or selected model. Select all
benchmark compounds with at least two structural OH groups or at least one
non-carbonyl ether oxygen, plus the fixed water, methanol, 1-butanol and n-nonane
controls, before examining their errors. Freeze the structural mapping, source
files and row identities in the commit. Inventory all available UD/open profiles
and geometries; missing data are reported without dropping score denominators.
For selected solvent rows, evaluate the eight fixed combinations of open/UD
area, volume and normalized 153-bin shape, with the solute kept open and the
existing dielectric and C6 tables unchanged. Each corner runs in a separate
process. Report the full-UD-solvent control and the exact Shapley identity, both
with numerical tolerance 1e-10 and identical finite coverage. These hybrid
profiles are diagnostic A substitutions and are never eligible for production.

The initial native geometry panel consists of ethylene, diethylene and
triethylene glycol at both their saved open and UD geometries, plus water,
methanol and n-nonane at their saved open geometries. Use fixed BP86/def2-TZVP,
the current auxiliary basis, XC grid 3/default pruning, C-PCM epsilon 1e9,
Lebedev 29, project radii and conv_tol 1e-9, without geometry optimization or
reorientation. Pin PySCF 2.14.0 and all other package versions for paired runs.
This is at most nine single points. Its diagnostics include geometric O-H...O
contacts, covalent HB tags, atom-owned surface area, raw and averaged charge
moments, pre-split areas and final OH/OT/NHB areas. A geometric contact is not a
measured H-bond energy. No choice is made on an experimental residual.

P22 tests raw surface charge; it does not authorize charge neutralization in
production. Validate the compact and diffuse neutral analytic Gaussian-sphere
sources at fixed Lebedev orders 29, 41 and 59. On water, diethylene glycol and
n-nonane in the native panel, recompute the PCM layer at fixed SCF density for
those three orders and for one radius scale of 1.10 at order 29. No such layer
is used in a score. For these molecules, integrate the same density and its
discrete capacitary potential on independent level-4 and level-5 volume grids.
Interpret the inside/outside decomposition only if level-5 total electron
count and reconstructed charge agree within 1e-5 e and the two partition
contributions change by less than 1e-4 e between levels. Failure is
inconclusive, not evidence for or against outlying charge. The union of project
vdW spheres is a stated diagnostic partition, not an exact SWIG boundary.

Two zero-charge projections, uniform sigma shift and the capacitary constrained
shift, are fixed A sensitivities. Compute both, never a fitted mixture of them,
for the nine native panel profiles and re-run the unchanged averaging/split.
Require each projected raw charge sum below 1e-10 e, report every subsequent
moment and tail change, and compare the same model query identities in fresh
processes with unchanged finite coverage. These projections are not an outlying
charge correction and cannot be adopted on the basis of a smaller benchmark
error. No output from this entry replaces a registered profile. A future
physical correction or conformer protocol needs a new registration after this
mechanism audit, with a fixed theoretical construction and a separate validation
panel before experimental scoring.

P23 first reports the existing P14 sidecar without changing a prediction.
Classify residuals at 1e-7 and sampled tangent margins at -1e-7. Keep missing
checks and coarse fallbacks as unresolved. Join records back to their exact
ordered pair and existing rounded temperature, preserving every requested row
and the original per-system majority aggregation. Preserve the old columns;
report quality-screen bounds with unknown votes assigned 0 and 1 separately,
and the explicit coverage of any endpoint-composition error. These are bounds
on the finite-grid quality screen, not a global phase-equilibrium certificate.

The opt-in P23 repair is an A numerical correction of the existing evaluator.
Freeze the complete unresolved-call list before repairing it; do not select
only favorable binaries. Preserve the model, pure-profile source and existing
2-K temperature rounding. Use nested 81/161/321 interior grids plus the fixed
logarithmic tails; try at most four sampled hull gaps and 4,000 new model calls
per pair-temperature. Use bounded least squares without clipping the equations,
residual <1e-7, sampled tangent margin >=-1e-7, gap width >1e-4, and agreement of
the last two grids' root sets within 5e-5 in composition. Exhaustion and failures
remain unknown. A strictly positive three-point nonconvexity witness supports
gap existence alone; it supplies no accepted endpoint compositions. No-gap
results remain explicitly finite-grid results. Record all outcomes, including
regressions, before producing a separately labelled scorecard. The portable
ideal/regular-solution and failure-injection tests must pass. For existing good
roots, a fixed control panel (first 20 sorted calls) must retain gap status,
meet the new residual/margin checks, and preserve endpoints within 1e-4; a
failure blocks adoption and is reported. Repairs are saved as a sidecar until
this gate and a full denominator audit pass. All earlier LLE scores remain.

The six-chain convergence campaign receives zero additional optimization budget
in this round. P19 remains rejected under its actual cost gate. S1/S2 status is
preserved as an exploratory endpoint of the present campaign, not a proof of
Berny convergence. A new optimization experiment requires a separate prospective
budget and evidence that addresses a specific remaining failure mechanism.
