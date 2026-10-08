R16-P57-P58-P59: London audit, one LV1 screen, and P54 reporting

Proposed registration, not an execution or adoption record. Append this text
in full to PREREGISTRATION.md and commit it with the four R16 scripts before
freezing a private R16 plan or using a new real-data result. Record the actual
UTC adoption time. Reference main is ca5c7e94627fcdebbf787afb688f8cab10e42a03.

P57 is E source/algebra reporting and a read-only audit of the original London
inputs. P58 is exactly one A dispersion approximation, with E algebraic reuse
of the unchanged Z0x calculation. P59 is E manuscript reporting. None modifies
the production model registry, any source in src/zcosmo, a stored physical
parameter, the UD input convention, or the 630 primary plus one selected S1
and five selected S2 profiles. P55 and all preceding failure records remain.
P35 and the numerical-gradient campaign remain closed.

The new candidate is named R16-LV1-cohesive-density-SK-volume-regular-solution.
Only this candidate and the unchanged stored-epsilon Z0x baseline are evaluated.
The already saved P54 COSMO-SAC 2010 pressures are a comparator, not a new
candidate. London deletion, a fitted corner, a weight change, another combining
rule, an alternative damping prescription or a surface-fraction variant is
not an authorized follow-up when a result is unfavorable.

The scientific choice is explicitly informed by P54's exposed dispersion
attribution. It is frozen before any LV1 molecular prediction or score. There
is no claim that the old compound split or temporal collection becomes an
untouched holdout. The new primary VLE comparison uses the identical 963 P54
observations in 100 unordered systems. The temporal collection is not rescored.
The original input-covered test_one/test_both IDAC and HE observations and
LLE positive observations are guard collections. The saved 336-state negative
archive supplies its input-covered original test_one/test_both subset. These
collections are previously inspected, and their exposure is part of the result.
No custodian-held, unexposed validation source has been certified here.

Physical definition of LV1

Use the existing molecular C6_ii and alpha_i from results/qc/dispersion.csv,
with exactly their existing identities and values. Use the unchanged historical
UD cavity volume V_i. All quantities must be finite and positive. No new D4
call, geometry, charge, molecular response calculation or experimental cohesive
energy is used. The temperature dependence of these inputs remains fixed.

Convert V_i in A^3 to diameter d_i=2*(3*V_i/(4*pi))^(1/3)/BOHR_A. Define the
positive self-contact magnitude u_i=C6_ii/d_i^6*HARTREE_KCAL in kcal/mol. Use
the existing Slater-Kirkwood cross coefficient:
C6_12=2*C6_11*C6_22/[(alpha_2/alpha_1)*C6_11+(alpha_1/alpha_2)*C6_22].
Its normalized spectral factor is kappa=C6_12/sqrt(C6_11*C6_22).

Keep z=10 and the dispersion weight exactly one. Define cohesive quantities
c_i=5*u_i/V_i, c_12=kappa*sqrt(c_1*c_2), and K=c_1+c_2-2*c_12. For mole fractions
x_i define Vbar=sum(x_i*V_i), phi_i=x_i*V_i/Vbar. The new molar excess dispersion
free energy is gV=Vbar*phi_1*phi_2*K (kcal/mol). Its exact component contributions
are ln_gammaV_1=V_1*phi_2^2*K/(R_KCAL*T) and
ln_gammaV_2=V_2*phi_1^2*K/(R_KCAL*T).

This follows by assuming a random homogeneous cohesive-energy density
-(phi_1^2*c_1+2*phi_1*phi_2*c_12+phi_2^2*c_2) and subtracting its linear pure
references. That density and cross normalization are declared approximations,
not uniquely implied by the molecular C6 descriptors. The original sphere
self-energy and coordination approximations remain. In particular, the model
does not solve shape, finite-contact damping, many-body polarization or the
cohesive-energy scaling of long chains. It is a thermodynamically defined,
no-new-benchmark-regression test, not a universally first-principles liquid model.

Do not add another combinatorial or Flory-Huggins entropy term. Keep every
existing residual interaction, epsilon value, composition derivative and
COSMO combinatorial constant unchanged. No pure vapor pressure is changed.
For equal cavity volumes LV1 reduces to the existing London Margules term.
For unequal volumes it need not reduce either component contribution or total
pressure. Its failure on one property is not grounds to choose a different
normalization or a favorable chemical subgroup.

Numerical implementation and checks

The baseline London free energy is gL=5*w*x_1*x_2. Both this term and gV are
independent of the electrostatic coefficient. Query unchanged Z0x once and
add the derivative of (gV-gL)/(R*T) to obtain LV1. This is exact reuse of the
stated two models, not physical E-equivalence of LV1 and London. Enable P28
for both arms. Preserve the base's adjacent finite-difference strip exactly:
there, difference the scalar correction with the same h=1e-4 stencil. Do not
silently upgrade that strip or create an exact association endpoint.

Portable tests must pass before a plan is frozen. They verify positivity and
label symmetry, the old exchange decomposition, identical/equal-volume limits,
Gibbs-Duhem, derivative consistency, the HE temperature convention and one-call
reuse. Tests involving the actual unchanged segment solver use synthetic
profiles. Tests of native, Mac and prior-run adapters are labeled as mocks.
No source module-cache clearing is permitted in these tests; the known R15
NumPy import-isolation artifact is not resolved by calling an incomplete log a
passing suite. Native end-to-end acceptance remains separate from portable tests.

P57 decomposes only the original exchange energy. With
q=[2*sqrt(d_1*d_2)/(d_1+d_2)]^6, the identity is
w=(sqrt(u_1)-sqrt(u_2))^2+2*sqrt(u_1*u_2)*(1-kappa)
  +2*kappa*sqrt(u_1*u_2)*(1-q).
These terms are nonnegative for positive inputs. The arithmetic implementation
checks the sum against the original formula to 1e-10*max(1,max(u_i)) kcal/mol.
They are energy terms, not fractions of experimental error or a second Shapley
analysis. The descriptor census and every per-pair quantity remain private.

Inputs and prospective plan

Run the original R15 saved-output checker on its unchanged helpers. Require
the original complete P54 plan and digest commit, its exclusive run claim,
7,704 requests, every finite corner and both replayed anchors. Preserve all
963 original observation identities, component orientation, T, x, measured P
and frozen saturation pressures. Reuse the P54 baseline and 2010 pressures.
Do not construct a new oracle selection or replace its original pressures with
values from a newer property package. Carry the P52a protected profile selection
and the existing source-version bridge forward without broadening it.

For the other properties, require the supplied IDAC, HE and positive-LLE CSV
bytes to equal reference-main data/benchmark/idac.csv, he.csv and lle.csv,
respectively. Copies at different private paths are allowed; new exports are
not. The negative archive must be the saved original 336-state input used by
the project; freeze its complete bytes and require one eligible state per
unordered test binary. It is an operator-supplied historical asset, not newly
reconstructed by negative_series(). Do not substitute a new negative archive.

Eligible guard rows retain their original split, original has_sigma decision
when present, 250<=T<=450 K, two different keys and valid physical input files.
Eligibility is decided without running a model or looking at prediction error.
Record every input-only exclusion, including missing descriptor, epsilon or
unambiguous historical UD profile. A malformed eligible observation is a
preparation failure, not a row to remove. No empty property class is accepted.
The HE sign subset must contain observations with |HE|>20 J/mol. The guard
selection is common to both arms and is fixed before all new queries.

Freeze hashes of each reused private input, all baseline source files, the new
helpers and installed package versions. Reject all baseline source/table drift
from reference main, including a changed P55 implementation. Profile identity
uses the existing exact-key or unique-connectivity UD rule, not a new chemical
name match. Each worker resolves both explicit frozen files. No fallback to
open profiles or to a different directory is allowed after a missing file.
All original private receipts remain available. Only the new plan digest is
committed in docs/astra/round16/PLAN_SHA256.txt before any new model call.

Requested evaluation and guard definitions

VLE: all 963 P54 rows, pressure in kPa from the same two saturation pressures.
Before guard-property queries start, unchanged Z0x must reproduce every saved
P54 baseline pressure to relative difference strictly below 1e-8. A failed or
missing anchor blocks the guard phase. No alternate baseline or relaxed
replay limit is authorized. All comparisons, including the stored 2010 arm,
use these same 963 observations rather than the historical main7 denominator.

IDAC: all frozen eligible test observations, with exact P28 solute index zero
at x=(0,1). HE: all frozen eligible test observations, with the existing
central temperature difference at T-0.5 and T+0.5 K. Use this same numerical
HE convention in both arms and keep each original x. The held-constant
volumes/descriptors imply a temperature-independent energetic gV; this does
not validate a physical volume(T) or epsilon(T) model.

LLE detection: preserve the positive observation identities and the original
2 K evaluation-temperature rounding. Negative states keep their recorded T.
For both arms evaluate the dimensionless total mixing free energy on the
existing log-augmented 81-point interior grid and an independently checked
161-point interior grid. Their exact union contains 181 compositions; reuse
identical nodes without rounding nearby distinct values. A detected gap means
maximum vertical distance above that grid's lower convex hull exceeds 1e-7
in g/(RT). The grids must agree for each arm and state. Disagreement or a
nonfinite grid is unresolved, never 'miscible', and blocks complete tradeoff
acceptance. This is an explicit numerical detection screen, not a global
stability certificate or an endpoint-composition score. Its baseline is freshly
evaluated by the identical convention; it does not overwrite historical LLE BA.

Positive system recall uses the original rule that more than half its retained
observations have a detected gap. Negative false-positive rate uses one state
per eligible binary. Balanced accuracy is (recall+1-FPR)/2. Keep the two classes'
denominators separate. No endpoint composition is inferred from a hull segment.
No LLE numerical result may be dropped from the acceptance denominator.

For VLE, IDAC and HE report observation-weighted AAD/MAE and signed bias;
also report equal-system averages and improved/worsened row counts. Use 1,000
paired resamples of unordered binary systems, with the seed fixed in
r16_stats.SEED. LLE resamples systems separately within its positive and
negative classes. Report two-sided 95% intervals for error differences and
use the specified one-sided 95% bounds for the gates below. These are
exposure-qualified resampling summaries, not recovered untouched-test guarantees.

All gates are required: VLE AAD change is negative and its one-sided upper
bound is below zero. IDAC and HE MAE changes and their upper bounds are <=0.
There is no positive allowed-worsening margin. HE sign correctness on |HE|>20
must not decrease. LLE recall and balanced accuracy must not decrease, with
lower bounds on their paired changes >=0; false-positive rate must not
increase, with its change's upper bound <=0. Missing data or an unresolved
numerical state is an incomplete screen, not a passed no-worsening gate.

Separately, report whether the candidate-to-2010 VLE AAD difference and its
upper bound are <=0 on the 963 rows. This is the limited 'gap closed on the
exposed panel' indicator. Passing only VLE is insufficient. Passing every gate
is success of this frozen exposed development screen, not a universal accuracy
claim or automatic production adoption. A genuinely independent validation
and an explicit later adoption decision are still required for that claim.

Cost, execution and stopping

Let NI and NH be the frozen eligible IDAC and HE row counts and NL the number
of distinct ordered-pair/temperature positive and negative LLE jobs. The new
baseline-call count is Q=963+NI+2*NH+181*NL. LV1 has no additional segment-solver
calls. The full frozen design must fit Q<=180000; otherwise preparation stops
with zero new model calls and no automatic downsampling or budget increase.
The proportional 722/7704 seconds per P54 query is a planning reference only,
not a measured R16 throughput. New LLE states may converge differently.

Execute serially on the private asset-bearing Mac, at most four OpenMP threads
and one BLAS thread. Each worker has 180 seconds within a total 21600-second
baseline-query/orchestration allocation. A five-second process-group kill
allowance is administrative, not additional scientific compute. Time closing
read-only aggregation separately. Budget is zero SCFs, zero gradients, zero
MD, no paid resource and no cloud dispatch. UD data, dense profiles, per-row
results, private plans and logs stay outside every Git checkout and are never
uploaded. Real work cannot run on a fixture or fabricated 'Mac' adapter.

Create one permanent exclusive execution claim. Write each attempt receipt
before calling the unchanged baseline. Record every job terminal state,
including blocked, budget-unstarted, failed and timed-out jobs. Independent
jobs continue within budget after another fails. There is no retry, resumption,
claim deletion or second scientific output directory. Repeated saved-output
checks are allowed with no new model calls. A complete but unfavorable run
is retained and its acceptance Boolean stays false. Failure of a query or
derived arithmetic withholds complete scores instead of taking a favorable
finite intersection. A lost data archive is not permission to recompute it.

Only aggregate errors, coverage counts, declared gate outcomes and timings are
eligible for separate human review before publication. The software publishes
nothing. P57 dense coefficient decompositions and per-row predictions remain
private. No candidate coefficient is changed after seeing a result, including
an IDAC or LLE failure. The original London model and historical records remain.

P59 inserts P54's actual results in the abstract and a dedicated manuscript
section, and updates the discussion and evidence references. It distinguishes
the one-at-a-time bias change -4.23 percentage points from the dispersion
Shapley bias allocation -4.47, without rewriting either historical table.
All R2-R14 open-profile, gradient, glycol, epsilon and empirical-input
qualifications remain. P54 is an explanatory centerpiece, not a proof that
real dispersion is absent. Finalize the paper with this evidence whether LV1
passes, fails, is operationally incomplete or is never executed. No speculative
native or new-variant campaign is made a prerequisite for writing up the study.
