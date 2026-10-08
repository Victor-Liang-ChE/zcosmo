R14-P51-P52-P53: exposure, dielectric ingredient, and oracle diagnostic

Proposed text. Append this complete text to PREREGISTRATION.md and commit it
with the three reviewed helpers before acquiring the reference, computing an
ingredient score, or freezing the oracle plan. Record the actual adoption time.
Base: 864aaac1e85eda31a43f24e856770c7f56ccb760. This is a new main-question
investigation, not a reopening of P35 or the R8/R9 numerical-gradient campaign.
All 630 primary and six S1/S2 profiles remain frozen. No production model or
experimental reference value is adopted. The R13 closeout remains historical.

P51 is E read-only source acquisition and ingredient analysis. P52 is an A,
experimental-input, retrospective explanatory VLE diagnostic, with E integrity
checks. P53 is E reporting. R14 authorizes zero new SCF attempts, zero quantum
gradients, zero conformer searches, zero new molecular-dynamics steps and zero
paid or cloud jobs. Real data operations occur only on the private Mac. No
raw UD data, dense profiles, row-level predictions or private paths enter Git.
The helpers upload nothing. Synthetic software tests may run elsewhere.

Exposure precedes scoring. The original 20-percent compound split and the
2017-2019 temporal collection have both been examined repeatedly. Retain their
historical identities, but do not describe them as newly untouched. P35's
142 observations and its structural follow-ups remain exposed. Excluding them
cannot restore blindness to the previously examined aggregate scorecards.
The public CRC-derived dielectric table is a different measured property,
not a verified independent laboratory sample. Its schema and some values,
including the approximate water/methanol discrepancies, informed this design.
No systematic comparison of the complete stored epsilon table with it has yet
been performed in this review. Record hashes of the public registrations,
progress log, main7/temporal scorecards, manuscript and closeout records in the
exposure receipt. Private queue histories and every collaborator's past
exposure have not been exhaustively audited. This receipt does not certify a
new holdout. Only the exposed retrospective oracle is authorized.

Acquire exactly the liquid-permittivity TSV from CalebBell/chemicals commit
e79047588b30cfabc564c79fb26d760c746877d7, path
chemicals/Electrolytes/Permittivity (Dielectric Constant) of Liquids.tsv,
Git blob bf12ffba51b478a021acc6ed58778c04deb9b988. Preserve its bytes and record
SHA256. One request, 30-second socket timeout, maximum 2 MB, no automatic
retry or alternative reference source. A failed request retains a receipt;
rerunning into an existing directory is forbidden. Store the reference and
all outputs privately outside any Git checkout.

Use all entries of the current results/qc/dielectric.csv, including failed
entries in the coverage accounting. Resolve an exact InChIKey through the
existing data/processed_ext/ud_complist.csv to exactly one checksum-valid CAS.
Require that CAS to map to exactly one project key and one reference row.
No names, connectivity-only fallback, racemate substitutions, or selected
synonyms resolve an ambiguous dielectric identity. Missing identity or
reference values are explicit coverage outcomes, never zero error.

The reference state is 298.15 K. Use A+B*T+C*T^2+D*T^3 only inside the source's
stated Tmin/Tmax range and when A and B are present. Missing higher-order C/D
coefficients are zero as in the documented polynomial representation. Otherwise
accept only a tabulated point within 0.10 K. Do not extrapolate, rescale a
293.2 K value to 298.15 K, infer a temperature from its chemical name, or use
optical permittivity as static permittivity. Values must be finite and >=1.
If any reference-matched entry has an invalid stored epsilon, withhold a
complete aggregate rather than silently removing it. Report the entire
population and the reason-specific coverage counts. The retained reference
state is the liquid state described by the compilation, not proof of a
stable ambient-pressure liquid for every compound in the portfolio.

Freeze input and helper hashes, installed numerical package versions and the
exposure receipt before computing P51 outputs. Metrics are equal-compound mean
and median absolute log epsilon error, signed log bias, mean and maximum
relative epsilon error, and mean absolute error in f=(epsilon-1)/(epsilon+0.5).
These metrics assess an ingredient. They are not an estimate of VLE error or a
gate accepting the existing Onsager approximation. Checks of saved inputs and
arithmetic may be repeated without new scores from a changed recipe.

For a possible future physical pilot, the fixed four liquids are water,
methanol, acetonitrile and benzene, identified by r14_dielectric.PILOT. A new
candidate must independently pass its separately registered dipole/sampling
validation and have complete reference coverage on all four. Prespecified
ingredient criteria are mean absolute log error <=80 percent of the same-panel
Onsager error, mean absolute f error <=0.02, maximum relative epsilon error
<=25 percent, and no individual absolute log-error deterioration >0.05.
These are engineering pilot criteria, not a confidence interval or a license
to fit g to measurements. The helper's Boolean validation inputs are not a
substitute for the actual physical receipts. No candidate-generating protocol,
MD run, dipole training or production rollout is authorized here. Those need a
new registration with reproducible model files and numerical validation.

P52 uses an operator-designated original Z0x VLE prediction archive containing
c1,c2,T,x1,P,pred_P,split. Hash it in its entirety. Query identities are original
file-row ordinals bound to that hash, not names. Restrict to its original
test_one/test_both rows, 250-450 K, 0<P<=500 kPa, strict interior compositions
1e-4<x1<1-1e-4, finite positive archived prediction, and P51 references for
both components. Do not select by observed error, hydrogen-bond class, epsilon
error, or hoped-for improvement. All exclusion reasons are counted. This is an
explicitly reference-covered, exposed subset, not the original main7 common set.

Select at most 100 unordered binary systems by SHA256('R14-oracle-v1|'+system).
Within each, retain at most ten eligible observations under SHA256 of the
original file-row identity. Preserve ordered component representation and the
original temperatures and compositions. Freeze the resulting identities and
actual counts. The maximum is 1,000 observations, with three arm requests per
observation, hence 3,000 activity-model API calls. These counts do not denote
internal segment iterations. A smaller eligible universe is reported as such.

Use the original UD profiles, unchanged, for all three arms. Record the exact
profile paths resolved by the existing exact-key/unique-connectivity rule and
provide both profiles explicitly in a private per-worker overlay. Keep the
explicit dielectric CAS policy stricter than that historical profile policy.
Protect hashes of exactly 630 profiles_v2, one S1 and five S2 files. Freeze the
Z0 parameter, dispersion and dielectric tables, the compound table used by the
existing vapor-pressure provider, all current zcosmo Python sources, the new
helpers and installed package versions. Source or input drift stops execution.

Freeze pure-component vapor pressures through the existing zcosmo.scope.psat
function using its InChIKey interface. Its output and the archived experimental
pressures are kPa. These same positive finite values enter every arm. This
preparation invokes the existing property provider, but no activity model.
Changed pure vapor-pressure inputs are not part of the epsilon intervention.
Archive the frozen values privately with the plan.

The three arms are current Z0x with its stored epsilon, current Z0x with the
P51 experimental epsilon at 298.15 K, and COSMO-SAC 2010. The experimental values
remain constant with temperature, just like current Z0x's stored table; this
is not an epsilon(T) experiment. Replace only the instance's two epsilon
values before any query, leaving its volume-fraction mixing rule and its
composition derivative intact. Clear its instance mixture cache. Do not
replace only c_ES while accidentally retaining an old dc_ES/dx. Enable P28
identically, though the selected rows are outside the endpoint strip. All
Z0/HB/London constants and input profiles remain unchanged. This experiment
does not change the meaning of a fit-free production model: its experimental-
epsilon arm is expressly NOT fit-free and can never be adopted by this result.

Before the experimental-epsilon or COSMO-SAC arm starts, reproduce every
selected archived Z0x pressure with the current stored-epsilon baseline at
relative difference <1e-7. Require finite coverage on every selected identity.
A mismatch blocks both later arms. A historical source-version or property-
provider discrepancy requires a separate reproduction decision, not a relaxed
gate after seeing the oracle. A blocked run is not evidence against the
permittivity hypothesis. No old scorecard or historical endpoint result is
overwritten.

Use one fresh subprocess for each ordered pair and arm; preserve selected
row order within that process. Clear inherited ZC_* settings before creating
the model. Each attempted query has a prewritten receipt. All requested jobs
have terminal records, including blocked and unstarted ones. Each subprocess
has 120 seconds; the serial Mac driver has 7,200 seconds including orchestration,
with a five-second process-kill allowance rather than additional scientific
compute. At most four OpenMP threads and one BLAS thread. No second claimed
run, retry, resume, alternate outcome directory or automatic budget extension.
Independent jobs continue after another fails within the remaining allocation.

The private oracle plan is bound to a committed SHA256 in
 docs/astra/round14/ORACLE_PLAN_SHA256.txt
before the first activity call. The registration and plan commits must be
ancestors of the execution checkout. The registration checker also verifies
the exact three helper files against their committed registration versions.
Do not change the helpers between an accepted registration and execution.

Require every requested new prediction to be finite before issuing complete
aggregate errors. Do not select a favorable finite intersection. On the fixed
subset report row-weighted AAD and signed pressure bias, equal-system AAD,
paired oracle-minus-baseline AAD, residual oracle-minus-COSMO-SAC AAD, and
improved/worsened counts. A signed comparator-gap recovery is reported only
for a positive baseline-minus-COSMO-SAC AAD gap above 1e-6 percentage points;
it is not clipped. Report all outcomes, including worse scores. No inferential
confidence interval or production-acceptance threshold is attached to this
exposed explanatory sample. The old 14.15/8.62 main7 comparison is not used as
the denominator for this newly selected sample.

Only the allowlisted aggregate error summary, after separate operator review,
is eligible for publication. Per-row predictions, parameter inputs, detailed
receipts and logs stay on the Mac. The independent check recomputes the saved
arithmetic and hashes without any model calls. No favorable oracle outcome
selects a physical recipe, fits a constant, authorizes 740 liquid simulations,
or grants a new confirmatory look at an old split. An unhelpful result supports
writing up current limitations; a helpful result identifies limited headroom
under this particular closure, not a rigorous upper bound.

P53 records a dielectric-development status separate from P35. Retain all
original benchmarks with their actual common subsets and their exposure.
A new physical variant needs an independently verified field/dipole model,
finite-size and sampling tests, and a genuinely unexposed custodian-frozen
validation source or an explicitly exposed fixed-design confirmation. The
current Z0w inheritance/dispatch concern is a source-version audit item; no
association code or historical failure is changed under R14. No fourth
association fit or simulation-based activity-coefficient campaign is authorized.
