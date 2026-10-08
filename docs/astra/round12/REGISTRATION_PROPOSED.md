R12-P46-P47-P48: private explanatory scoring and regional accounting

Proposed registration. Adopt and commit this complete text in PREREGISTRATION.md
before either new plan is frozen or any new R12 output is interpreted. Reference
main: a93a1c9abbec32e0af7ff259a8db6fa550bb34a9. The design is motivated by already
inspected R4-R11 outcomes, not by a new held-out experiment. Previous P30/P32
failures and P33/P37 decisions are not reopened. The numerical-gradient campaign
stays closed. The 630 primary and six S1/S2 production profiles remain unchanged.

P46 is A explanatory input substitution, with E replay/accounting checks. It
IS scoring against ThermoML under the optimization brief: experimental ln gamma
values are used to compute errors. No C profile, geometry, mixture parameter or
conformer weight may be selected from the result. C is the already frozen R11
open-method profile at that member's historical UD coordinate input. All such
data stay on the private asset-bearing Mac. No new quantum calculation,
optimization, molecular gradient, conformer search or fitted parameter is allowed.

Require the completed R11 private plan, its original committed digest and its
successful 12-member/24-slot integrity record. Run the original R11 checker,
retain its package/source/lineage requirements and protect its frozen 630+6
population. R10/R11 scientific helpers remain unchanged. Freeze hashes of the
new helpers and every reused input; retain the installed environment. Only
plan digests enter Git. No coordinates, dense profiles, per-row predictions,
logs or private paths may be committed or uploaded. Synthetic software tests
may execute outside the Mac and before registration.

P46 uses the ORIGINAL P21 factorial_rows.csv, summary.json and complete per-pair
rows, corner predictions and *.csv.inputs.json receipts. The archive must contain
332 unique r3_row_id observations and 14 solvent identities. Verify every pair's
solute, solvent, temperature and experimental value against the top-level table.
Verify per-pair predictions against the original nine output columns. The four
pre-stated scored identities and row counts are EG LYCAIKOWRPUZTN-UHFFFAOYSA-N (9),
DEG MTHSVFCYNBDYFN-UHFFFAOYSA-N (108), TEG ZIBGPFATKBEMQZ-UHFFFAOYSA-N (17), and
tetraEG UWHCKJMYHZGTIT-UHFFFAOYSA-N (7), totaling 141. Selection is by these exact
keys, not by a solvent-name synonym, error sign or R11 label. TetraEG remains
included despite its different R11 attribution. The other 191 P21 observations
remain in the read-only archive identity/hash audit, explicitly outside the new C scoring
subset. Do not change the 141-row scientific denominator or claim a new 332-row
C score. The original query rows are not rebuilt from a newer benchmark export.

Use the exact original P21 open solute and open solvent profile bytes. The
original per-corner receipts must match their SHA256 values, the UD solvent
bytes and the dielectric.csv, dispersion.csv and Z0.json tables. Recover the
original snapshot if necessary; do not silently replace it with current files
whose metadata hashes differ. P21/R11 UD profiles for the four targets must
match the already verified lineage. Missing, ambiguous or altered archives stop
preparation. No new SCF is authorized to recreate an absent private artifact.

Before C scoring, replay the original P21 open-solvent (000) and full-UD-solvent
anchors on the same 141 target observations using the HISTORICAL endpoint
(ZC_R6_ENDPOINT=0). This is 2*141=282 requested lngamma_inf evaluations. Audit
all 332 original archive identities and all nine per-corner stored outputs and
input receipts without new model calls. Check the archived 111/full-UD identity
to 1e-10. The 282 fresh anchor identities and finite coverage must match;
maximum absolute replay difference must be strictly below 1e-8 in ln gamma.
This is a same-input anchor gate, not a claim that every historical intermediate
corner was recalculated, or a relaxation of E/P32/scientific accuracy gates.
If anchor replay fails, record the failure and block every C-scoring job.
Do not change a solver or endpoint to make the old comparison pass.

The primary new evaluation uses the accepted P28 EXACT endpoint consistently
for O, all C-factorial corners and the full U solvent (ZC_R6_ENDPOINT=1).
For every one of the 141 rows, evaluate the eight O-to-C corners and U: 1269
requested calls. Keep the solute's original open profile in every corner.
Bit order is area, cavity volume, normalized 153-bin shape, exactly as P21.
For bit vector (a,v,s), use A=A_C if a else A_O; V=V_C if v else V_O;
and the shape C/A_C if s else O/A_O. Multiply the chosen normalized shape by
the chosen area. Retain original open metadata in the factorial. Z0x's physical
constants, chemical dielectric data, London data and chemical identities are
unchanged. The full-U anchor uses the original UD solvent file. This is not
an all-UD mixture and no solute is replaced merely because it is another glycol.

One worker handles one ordered pair and one corner in a fresh process. Its
temporary overlay must resolve BOTH requested profiles explicitly; a missing
open solute cannot fall back to UD. Clear inherited ZC_* experiment switches
and set the declared endpoint and private overlay before model construction.
Do not reuse a process-global profile cache across corners. No new data loader,
segment solver, endpoint approximation or physical model is introduced.

The maximum is 1551 requested model API calls, zero SCFs and zero gradients.
The job count is 11 times the number of target ordered pairs, computed from
the frozen inputs, not guessed here. The two replay anchors precede the nine
new endpoint-consistent evaluations for each target observation. Calls denote lngamma_inf
requests, not individual internal segment iterations. Run serially on the Mac,
with at most four OpenMP threads and one BLAS thread. Each worker has 120 seconds;
the model-run allocation is 7200 seconds including orchestration. A process-group
kill/accounting allowance of five seconds is not extra scientific computation.
Record closing zero-model integrity/aggregation time separately if it extends
the allocation. No parallel cloud workflow, paid resource, retry, resumption,
stale-claim deletion or second run of a claimed plan is authorized. Every
planned job retains a terminal state, even when it is blocked or never starts.

Failure handling is part of the design. Preserve requested row identities and
finite/nonfinite counts for every arm. Do not form a smaller favorable intersection.
A failed historical replay blocks the new stage. A missing, failed or nonfinite
new result blocks complete-panel error summaries; retain its diagnostic receipt
and the remaining completed values privately. A green process or workflow state
is not numerical acceptance. Independent jobs continue within the fixed budget.
The original input hashes and the protected production population are rechecked
after execution. Checks of saved output may be repeated without new model calls.

Report errors on the 141 fixed rows per solvent, pooled with original row weights,
and with equal solvent weighting as a declared secondary summary. DEG contributes
108 of 141 rows to the pooled score. For y_O,y_C,y_U and experimental y, report
MAE and bias. The removed absolute error is mean(|y_O-y|-|y_C-y|); the remaining
UD-comparator gap is mean(|y_C-y|-|y_U-y|). Their sum must equal the O-to-U MAE
gap. A recovery fraction is reported only for a positive denominator above
1e-6, is signed and is never clipped to [0,1]. Negative values and values above
one remain visible. No confidence interval, success threshold or production
acceptance is inferred from this retrospective fraction.

Apply the unchanged P21 shapley_three function twice to the complete eight-corner
cube: once to predictions and once to negative absolute errors. The second
calculation gives additive area/volume/shape contributions to absolute-error
reduction. Taking absolute values of prediction Shapley terms is not equivalent.
Require both efficiency identities to 1e-10. Positive/negative contributions and
interactions remain visible. A C-minus-O prediction change is not automatically
an error reduction. Report the legacy-versus-P28 O and U endpoint bridge on the
same target rows; never subtract a legacy O score from an exact C score. No
post-P28 value overwrites P21 or a historical scorecard.

The original P21 profile is the primary baseline, even if its bytes differ from
the R11 repeat. Hence P46 is explicitly a FROZEN-INPUT C-substitution explanation.
It is not a new pure torsional or hydrogen-bond causal estimate, and it does not
relabel the R11 profile decomposition. Dense per-row values and counterfactual
profiles stay private. Prediction Shapley values remain private; only aggregate bias and MAE statistics
and absolute-error-reduction Shapley values enter the public allowlist.
Only that aggregate error summary is eligible for separate human review before publication. The software never
uploads or copies it into Git. Publish improvements and deteriorations under
the same predetermined headings, clearly labelled retrospective explanatory
ThermoML scoring, not a fitted improvement or a new validated profile version.

P47 is an independent E read-only analysis with zero QC and zero model calls.
Freeze its own plan digest, so it can proceed even if the P21 archive is absent.
Use all twelve verified R11 members and all four archived profile families:
U (UD), A (P25 archive), R (fresh open-geometry repeat), C (crossed UD geometry).
Normalize each family by its OWN area before taking a normalized difference.
Use D=U-R, G=C-R, M=U-C and repeat drift R-A. Preserve the R11 classification
object unchanged, including the 0.359 realized scale and all inconclusive labels.
Do not substitute a new eta, exclude water, subtract a background vector, or
reinterpret the regions as independent hypothesis tests.

Partition the fixed 51-point sigma grid by integer millithresholds into five
bands: sigma<=-0.010; -0.010<sigma<=-0.005; |sigma|<0.005;
0.005<=sigma<0.010; sigma>=0.010 e/A2. Cross these bands with the existing NHB,
OH and OT channels. Each of the 153 entries belongs to exactly one of 15 cells.
Report each cell's signed mass change, L1 contribution and first moment, for
unnormalized and normalized profiles separately. Regional L1 shares sum to one
when the total is nonzero; use null for zero-total shares. Require conservation
of signed mass, L1 and moments to the implemented 1e-12 scaled arithmetic bound.
Also collapse the HB channels at each sigma and report L1_153-L1_51, the amount
of channel cancellation hidden by a total-profile projection. This is a
representation diagnostic, not an attribution to an HB energy term.

The positive and negative OH/OT regions use the existing acceptor-side and
donor-side parser convention. NHB entries remain NHB irrespective of sign.
The centre is a low-|sigma| region, not a proof of nonpolar chemistry. Raw
outlier tesserae and net surface charge are not reconstructed from a normalized,
smoothed histogram. P47 cannot infer a nonlinear ln gamma contribution from a
regional profile norm. All region tables remain private; no regional or dense
profile data are included in P46's public error summary.

P48 records the scope of the established result. The polar-tail gaps for EG,
DEG and TEG are mainly due to stored coordinate inputs under the registered
ordered open-method cross. TetraEG is an explicit exception, with a mainly-method
raw-tail gap and small other tail contrasts. No whole-profile attribution label
passed. No conformation is thereby established as the liquid distribution, no
UD structure is adopted, and no IDAC improvement is claimed before P46 executes.
The numerical-gradient campaign remains closed.

After these bounded read-only/explanatory tasks, archive the findings whether
favorable, unfavorable, operationally incomplete or inconclusive. The liquid-
state mechanism and a production conformer rule remain unresolved. R12 provides
no native or ensemble budget and no automatic continuation. A phase-dependent
free-energy protocol would require separately validated basin populations,
thermal contributions and common reference conventions on the full eligible
class and controls; the existing finite samples and R11 single points do not
supply them. A cheap calculation on incomplete inputs is not acceptance of such
a protocol. Historical profiles and scientific decisions remain unchanged.
