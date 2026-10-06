Round-6 proposed registration. This is not evidence that the text has been
adopted. Append accepted text with the actual commit timestamp before a new
candidate output is interpreted or used. Reference main is
43213a5e61f591a19b4d3352a95315a62ee2aeb8 plus the six archived R6 patches.
The hypotheses are motivated by the already observed R5 results. No new result
is represented as an experimental holdout, and no ThermoML response selects
any numerical constant, geometry, conformer, or population.

The six stopped chains remain excluded from new native jobs. Their files keep
S1/S2 status, primary profiles_v2 remains 630/636, and P26's full protocol is
not resumed. P15/P17/P19 rejections stand. P20's accepted metadata correction
and P23/P27 reporting remain in place. No R6 helper writes a production profile
or silently changes a historical scorecard.

P28 is a narrowly scoped A numerical correction of the Z0x infinite-dilution
endpoint. For a pure solvent, evaluate the unchanged fixed-coefficient Mixture
at the pure composition, with A_ES equal to the pure solvent's dielectric
coefficient. The chain-rule term vanishes because the frozen-coefficient
excess Gibbs energy is identically zero at either pure endpoint for every
coefficient. Construct this Mixture without the rounded-c lookup. The switch
ZC_R6_ENDPOINT=1 affects lngamma_inf and lngamma at exactly x1=0 or x1=1 only.
Its default is off. Every finite interior composition, including the existing
near-endpoint finite-difference strip, stays unchanged. This entry does not
certify that strip, fix the finite-composition model, or authorize a correction
in another Z0 variant. All profile bytes, dielectric and dispersion tables,
functional forms, and fitted/theoretical constants remain unchanged.

Freeze the historical has_sigma IDAC universe from the current P27 input CSVs,
including every row identity and split label. Run UD, open630, open636, and
one declared stress overlay in separate processes. The stress overlay uses
UD's normalized water profile with the native open area and volume; all other
profiles are open636. No experimental response is sent to numerical workers.
Open630 excludes exactly rows involving S1/S2 keys, without UD fallback.
The old and candidate endpoints are evaluated independently even when the old
one fails. Require identical finite coverage in every arm; matched nonfinite
rows remain in the requested denominator. Every old finite row must be checked.

The independent reference solves the same segment equations in logarithms,
using a separate residual/Jacobian evaluation and nonlinear polish. Require
maximum log-equation residual <=5e-12, maximum candidate-reference difference
<1e-8 in ln gamma, component-reversal agreement <1e-8, public endpoint API
agreement <1e-10, and pure-solvent ln gamma <1e-9. Keep every positive profile
bin; do not threshold tiny support. A malformed, missing, or extra result row
fails the gate. Report three-point one-sided controls at h=1e-4, 1e-5, 1e-6,
1e-7 and 1e-8 with fresh coefficient evaluation. These controls diagnose
truncation/cancellation; no h is chosen by experimental error. FD rows lacking
agreement within 1e-5 are explicitly inconclusive and do not replace the
reference equation gate. The proof and independently checked endpoint solve,
not a supposedly optimal tiny h, define the candidate.

Report counts and magnitudes of changes above 1e-3, 1e-2, 0.05 and 0.1 on all
and test rows, with separate solute/solvent summaries. Time three fresh-process
repetitions per arm and flag, alternating order; do not time the expensive
reference/FD checks as production. No measured speed-up is assumed. A numerical
pass permits recording acceptance of this exact gate hash before running the
separate score command. That command reports old and corrected IDAC results
on identical rows, with 1000 system bootstrap draws and seed 7. The water stress
arm is a diagnostic, never a deployable profile set. P27's historical outputs
are retained. A worse experimental score does not reverse a proven numerical
correction. Any finite-composition extension needs its own gate and accounting.

P29 first inventories every frozen P26 probe proposal by input hash, retaining
censored, failed and never-run members. Duplicate runs cannot be cherry-picked.
Known-conformer tail ranges and normalized-L1 diameters describe the supplied
finite set only, not unsampled basins. No electronic-energy population or
embedding-frequency multiplicity is assigned to incomplete pools.

The theory definition is a phase-dependent finite-basin ensemble, not a chosen
extended geometry and not a rule excluding intramolecular hydrogen bonds.
For each distinct basin, retain the conductor electronic energy, the nuclear
partition contribution, and audited symmetry/multiplicity. The nuclear term
includes ZPE and finite-temperature vibrations or an explicitly integrated
hindered-rotor/basin contribution, with rotational terms on a common reference.
The same molecular translational standard state cancels between its conformers.
An imaginary or unconverged soft mode must not be replaced by its absolute
value or an empirical frequency floor. Intramolecular H-bonds already affect
the electronic energy and exposure; no extra penalty or reward is added.

The provided reference-ensemble helper can compute a harmonic plus classical
rigid-rotor diagnostic only from complete audited basin inputs. Require the
P30 force, Hessian, and two-step thermal checks for every supplied basin and
an explicit basin/symmetry audit identifier. Distinct minima must be deduplicated
with atom/symmetry correspondence, not by embedding frequency. Rotational
symmetry number and additional basin degeneracy are different inputs and cannot
count the same symmetry twice. Harmonic numerical stability is not proof of an
accurate low-barrier torsional partition. This helper produces a labelled finite
conductor-reference ensemble only; its averaged profile is not a liquid chemical
potential and its weights are not automatically liquid populations.

The prospective finite-basin Z0x extension is frozen in scripts/r6_phase.py.
It uses the unchanged combinatorial and segment equations over basin species,
volume-weighted chemical permittivities, and the symmetric extension of the
existing London contact exchange energy. All basins of one chemical species
retain the same frozen chemical dielectric, C6, and polarizability values.
Conductor electronic plus nuclear free energies are augmented with the model's
absolute pure-conformer segment and London self-contact standards before
adding the pure-subtracted excess mixture functional. Thus pure-liquid and
infinite-dilution populations are minimized separately under one scalar free
energy; conductor solvation is not added twice. This is a new A closure, not
claimed to be uniquely implied by a final sigma histogram or by COSMO-RS.

The finite-state pilot is restricted to two chemical species, at most four
audited basins each, and T=250, 298.15 and 400 K. A catalog with more
than four distinct relevant basins is outside this pilot; do not drop basins
merely to meet the software cap. Use the fixed uniform and
vertex-biased starts, a shared 2000 objective-call budget per equilibrium
problem, and the fixed stationarity checks in the code. A failed multistart
blocks the result; a lower stationary value is not a global certificate.
The one-basin-per-species limit must reproduce P28 to <1e-8; analytic free-energy
derivatives must agree with independent finite differences to <1e-7 in the
portable test; energy-zero and population-normalization checks must pass.

No new quantum basin survey is authorized by P29 in R6. The command examples
consume only explicitly supplied and audited basin partitions. The present
incomplete P26 files do not satisfy that requirement. A later physical ensemble
validation requires a separate prospective sampling budget on all eight frozen
R5 validation molecules. Independent complete basin catalogs must give chemical
free energies within 0.05 kcal/mol, normalized average profiles within 0.02 L1,
and both-role probe ln gamma within 0.02 at the three fixed temperatures, with
identical finite coverage. The four probes remain water, methanol, nonane and
1,2-dimethoxyethane. Thermal partition error must also be checked independently
of discovery-pool agreement. No R6 ensemble output is authorized for ThermoML
scoring or for replacing the 630 primary profiles, and P26 remains unaccepted.

P30 tests a specific possible source of energy/gradient inconsistency before
attempting any new optimizer. Pin pyscf=2.14.0, pyberny=0.7.0 and the R5 direction
construction's RDKit=2026.03.6. Freeze five geometries: saved R5 methanol and
ethylene glycol, plus the last archived geometry of exactly these P26 censored
members: nonane seed 20261006 rank 1, TEG seed 20261006 rank 1, and
1,2-dimethoxyethane seed 20261005 rank 1. Their recorded 80-evaluation outcomes
and proposal hashes must match. Do not optimize these inputs or restart any of
the six stopped chains. The never-run tetraEG proposal is not quietly added.

Per geometry, compare the original energy/gradient with tighter SCF
conv_tol=1e-11 and conv_tol_grad=1e-7 at the same BP86/def2-SVP, DF, grid level 2,
default pruning, project radii, C-PCM eps=1e9 and Lebedev 17. At the tight center
compute gradients with grid_response=False and True, retaining auxiliary-basis
and PCM responses. Compute centered energy differences at 0.003 and 0.006 Bohr
along four deterministic internal directions. The first directions are heavy
single-bond rotations, with the fixed projected random fallback in the helper.
This costs at most 18 SCF evaluations and three gradients per case.

The two-step derivative uncertainty indicator must be <1e-7 Eh/Bohr and maximum
full-response gradient discrepancy <2e-7 on all sampled directions. Material
omitted response is reported only when the tight-no-response discrepancy is
>1e-6 and >5 times the larger of the full-response discrepancy and 1e-10.
This is a directional test, not a proof everywhere or a claim that omitted grid
response caused the observed stalls. Maximum budget is one four-core worker-hour
per case, with an internal 3400-second deadline. Inconclusive results stop the
native escalation. Do not change a threshold after reading the outputs.

Only if all five fixed consistency cases pass, the optional mode/stability
stage is allowed on the same five geometries. Use two finite-difference Cartesian
Hessians from tight full-response gradients at steps 0.003 and 0.006 Bohr. Project
mass-weighted translations and rotations explicitly, and record Hessian asymmetry,
step dependence and every signed frequency. Per case the count is 12N+2 gradients,
never above 360. Significant negative modes below -20 cm^-1 or failure of the
new diagnostic force targets (max 5e-5 and RMS 1.5e-5 Eh/Bohr) fail stationarity.
This new diagnostic definition is NOT an equivalence to Berny's internal
coordinate, step, or on-sphere predicate and is never written as Berny-converged.

For passing stationary candidates, evaluate the center and both signs of 0.005
and 0.010 Angstrom maximum-atom displacements along the six softest projected
modes, at most 25 registered TZVP profiles per case. Keep orientation, all profile
settings and P18 metadata fixed. For a harmonic partition diagnostic all
vibrational frequencies must be positive and the two Hessian steps must change
F_vib by <0.05 kcal/mol at every fixed temperature. Otherwise the thermal result
is unavailable and a hindered-rotor/basin integration would need a separately
registered budget. There is no silent soft-frequency regularization.

The optional stage has a two-worker-hour cap per case, including its stress
profiles, with an internal 7000-second deadline. Across both native stages the
absolute budget is 15 four-core worker-hours, with no retries, no optimization,
and no production relabel. On the Mac, compare stress profiles against their
own center in separate processes against the four fixed probes, in both roles
at 250, 298.15 and 400 K using P28. Require identical finite coverage and maximum
sampled change in ln gamma <0.01. This is an observed finite-stress envelope,
not a certified bound on every geometry in a ball or on every thermal basin.
Even a pass authorizes no new S1/S2 acceptance route. A future convergence rule
for production needs its own independent validation and registration.

The job runner locks each output location before starting, terminates the whole
process group on its fixed deadline, records all return codes, and continues
independent jobs after a failure. It never automatically deletes a stale lock,
retries a member, or dispatches a cloud workflow. Censoring must not hide a
never-run member as it did in one R5 slot.

P31 re-renders the archived P27 matched test comparisons, with their original
confidence intervals and row identities. No prediction is regenerated and no
new bootstrap is run. Report IDAC and HE deficits on matched rows; describe the
VLE increase with its paired interval, which includes zero. Keep LLE checked
roots, gap witnesses, sampled no-gap and unresolved statuses distinct. Detection
rates on the positive LLE table are not balanced accuracy. All headline numbers
are explicitly before P28. Rewording a headline does not alter the historical
score, and open636 remains separately flagged exploratory coverage.
