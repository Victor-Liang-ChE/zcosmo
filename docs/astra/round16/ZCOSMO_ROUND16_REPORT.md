Z-COSMO round 16: audit the positive London bias, freeze one volume-based alternative, and finalize the P54 explanation

Reference main: `ca5c7e94627fcdebbf787afb688f8cab10e42a03` in `Victor-Liang-ChE/zcosmo`. This report responds to ROUND16_PROMPT.md and the completed R15 record. All patches below are prospective. No model has been scored here and no registration has been committed to the remote repository. The 630 primary plus one selected S1 and five selected S2 profiles remain frozen. P35 and the numerical-gradient campaign remain closed. [S1–S3]

| Rank | ID / pipeline / class | Target and mechanism | Expected saving or cost, with acceptance | Effort |
|---:|---|---|---|---|
| 1 | P57, London physics and input audit, E | `r16_london.LondonPair.old_audit`; `r16_review.freeze`. Factor the implemented exchange into nonnegative contributions and bind the old inputs to the P54 archive. | Zero new QC or activity calls for the audit. Prevents an unjustified factor-of-two correction or an error-selected weight change. The algebra identity must hold within its stated numerical tolerance. | Low |
| 2 | P58, exactly one dispersion alternative, A; paired computation reuse, E | `r16_london.DispersionChange`, `PairedLondon`; `r16_review` and `r16_stats`. Replace the molecular mole-fraction Margules term with the explicitly defined LV1 cohesive-density/volume regular-solution term. | One unchanged Z0x call supplies both arms, rather than two full residual evaluations. At most 180,000 baseline calls and 21,600 seconds on the owned Mac; zero QC or MD. A complete exposed screen must improve VLE and pass every IDAC/HE/LLE guard. No numerical improvement forecast is claimed. | Moderate |
| 3 | P59, manuscript and P54 clarification, E reporting | `manuscript/draft.md` and `docs/astra/round16/P54_CLARIFICATION.md`. Insert the completed factorial and distinguish its two bias statistics. | Zero model calls. Makes finalization independent of the outcome or execution of P58. Preserve all historical numerical tables. | Low |
| Shared | H16, T16, REG16 | Core arithmetic, software tests and proposed registration, embedded as independent patches | 58 new portable tests; no scientific acceptance follows merely from their success. | Low |

The ranking concerns useful decisions and avoided work. I have no defensible numerical probability that LV1 closes the VLE gap. The exact savings concern repeated computation, not a promised pressure-error reduction. Finalize the paper around P54 now; the one frozen alternative is an optional bounded development screen, not a condition for completing the paper.

What P54 establishes, and a reporting correction

The comparison is the specific 963 exposed observations in 100 systems, not the historical 9,432-row main7 comparison. P54 made 7,704 finite requests, reproduced both endpoint controls exactly, and allocated the unrounded 3.35-percentage-point AAD gap as 2.24 to dispersion, 0.88 to the electrostatic closure and 0.23 to hydrogen-bond constants. The associated percentages are approximately 67%, 26% and 7%. These are Shapley error allocations under the specified intervention set; they are not fractions of the real liquid's energy. Both endpoints had identical UD profiles and effective area, so those factors could not explain this endpoint difference. [S2]

The earlier conductor-limit Z0 ablation and P54 ask different questions. P54 makes a better case for examining the implemented London closure in Z0x than for spending the next budget on improved bulk permittivity. It does not show that real dispersion is unimportant, and it does not license choosing the no-dispersion corner as a new model. R14's epsilon-oracle recovery overlaps with P54's electrostatic intervention and cannot be added to it. [S2, S4]

There is a specific numerical wording issue. Removing London alone changes the displayed bias from +1.44% at 000 to -2.79% at 001, or **-4.23 percentage points**. The factor table's **-4.47** is the Shapley-allocated dispersion contribution to bias across the other ingredient contexts. Applying the allocation to the rounded corner biases gives -4.4733. The R15 prose and R16 summary should not describe this as the one-at-a-time shift. P59 clarifies it without silently rewriting the historical RESULTS file. The distinction does not alter the 2.24-point error attribution or the 2.02-point one-at-a-time AAD reduction. [S1, S2]

An exact structural restriction of the current London term

Write the positive self-contact magnitudes, in one consistent energy unit, as

\[
 u_i=C_{6,ii}/d_i^6,\qquad
 \kappa=\frac{C_{6,12}}{\sqrt{C_{6,11}C_{6,22}}},\qquad
 q=\left[\frac{2\sqrt{d_1d_2}}{d_1+d_2}\right]^6.
\]

The existing Slater-Kirkwood rule gives

\[
 \kappa=\frac{2}{t+t^{-1}}\leq1,
 \qquad t=\frac{\alpha_2\sqrt{C_{6,11}}}{\alpha_1\sqrt{C_{6,22}}}.
\]

The arithmetic-geometric-mean inequality gives q<=1. Substituting into the implemented exchange produces

\[
\begin{aligned}
 w&=u_1+u_2-2\kappa q\sqrt{u_1u_2}\\
  &=(\sqrt{u_1}-\sqrt{u_2})^2
    +2\sqrt{u_1u_2}(1-\kappa)
    +2\kappa\sqrt{u_1u_2}(1-q)\geq0.
\end{aligned}
\]

This is an algebraic property of the actual formula for positive descriptors and volumes. The three terms separate self-contact mismatch, spectral mismatch and the arithmetic-contact size factor. Their split is useful for auditing that formula; it is not another pressure-error attribution and cannot be mapped onto P54's 67% without evaluating the nonlinear model. The helper verifies the identity against the direct formula, retaining physical units. It uses stable hyperbolic-secant identities for close descriptors rather than clipping a negative numerical result to zero. [S5]

With the registered positive weight and z=10,

\[
 g_L^E=5w x_1x_2,\qquad
 \ln\gamma_{1,L}=\frac{5w}{RT}x_2^2,\qquad
 \ln\gamma_{2,L}=\frac{5w}{RT}x_1^2.
\]

Both contributions are nonnegative. At fixed residual activity coefficients and positive pure vapor pressures,

\[
 P=\sum_i x_i\gamma_{i,\mathrm{residual}}P_i^{\mathrm{sat}}
       \exp(\ln\gamma_{i,L})
\]

cannot decrease when this London term is added. It can improve an underpredicted pressure or worsen an overpredicted one. P54's average AAD penalty is measured evidence; the sign of each row's error change is not determined by this theorem. A fitted 2014 COSMO-SAC-dsp sign rule is not part of this theorem and must not be confused with the current London branch. [S2, S5]

Physics audit: which assumptions are choices and which directions are known

| Assumption | Physical status and possible replacement | Direction on activity coefficients and bubble pressure |
|---|---|---|
| One-center molecular C6 at a center-to-center contact | The molecular sum is a far-field descriptor. Actual atom-pair separations and anisotropic surface access matter at contact. Distributed, properly damped atomic dispersion is a more resolved construction only after contact geometries, environmental response and averaging are specified. The scalar table cannot recover them. | No general sign for the change from one-center to distributed dispersion. Strengthening unlike attraction relative to the self attractions lowers w and both old Margules contributions; strengthening self attractions raises them. A larger total binding magnitude alone says neither. |
| Cavity-volume sphere diameters and a single d^-6 separation | COSMO cavity volume is not a measured molar liquid volume or a universal hard-sphere contact. The sixth power is appropriate to an asymptotic pair term, but extending it to this particular contact is an approximation. A radial/orientational pair distribution would require an additional physical model. | Scaling all distances by s scales w and the old contributions by s^-6. Scaling all volumes by v at fixed descriptors scales them by v^-2. Differential changes have no universal sign. Increasing only d12 raises w; increasing only a self diameter lowers w. The arithmetic-mean d12 creates the nonnegative size term above relative to geometric-mean normalization, not proof that the latter is the true contact. |
| Slater-Kirkwood combination from static alpha and self C6 | A single-effective-oscillator closure replaces the full imaginary-frequency polarizability integral. It is an approximation, not an identity for arbitrary real molecules. Using a consistently computed full cross spectrum could remove this approximation, but is not encoded in the present two scalars. | In the implemented model kappa<=1 contributes a nonnegative mismatch penalty. The error of the approximate kappa relative to a better calculation can have either sign. Published atomic/ionic tests cannot establish molecular-liquid accuracy. [U1] |
| Coordination z/2=5 and random molecular contacts | One-half correctly avoids counting each bond twice in the assumed lattice. It is not a demonstrated factor-of-two bug. Coordination 10 and its use for whole molecules are inherited conventions, not values determined by D4. A contact distribution must fix coordination independently of ThermoML. | Lowering z lowers this positive energetic term, but that alone supplies no physical justification for choosing a lower z. Changing Params.z globally also changes the COSMO combinatorial term, so it is not an isolated dispersion test. |
| Mole-fraction symmetric Margules statistics for unequal sizes | The old term forces equal dispersion-only infinite-dilution contributions in the two orientations. A volume-based energetic regular-solution construction gives the required size factors through derivatives of a complete gE. Merely replacing x by phi in the existing gamma formula is generally thermodynamically inconsistent. | A consistent replacement redistributes the two contributions. Either can increase; their pressure-weighted sum is not guaranteed to fall. The selected LV1 model below tests this explicitly, retaining negative experimental outcomes. |
| Damping and many-body effects absent from the scalar liquid term | D4 property generation is not a complete DFT-D4 intermolecular energy evaluation. D4's full energy model has additional ingredients and damping parameters; the repository stores only molecular C6 and alpha. Adopting another damping model would be a separate choice. [U2, U3] | Suppressing all attractive contact magnitudes by a common factor suppresses w. Unequal suppression of self and unlike contacts need not. Many-body contributions likewise do not have a universal sign in the excess mixing quantity. |
| Dispersion counted in the conductor residual or pure vapor pressures | The current residual kernel explicitly contains electrostatic misfit and a hydrogen-bond term. The original HB matching removed a D4 binding contribution. A conductor calculation or a fitted reference convention can still carry indirect compensation, but P54 does not identify it uniquely. Pure vapor pressure provides the pure-component chemical-potential reference, not the excess mixture dispersion free energy. | There is no automatic “already in Psat, therefore remove it” cancellation. A legitimate excess dispersion term vanishes at pure composition and belongs alongside Psat. An unjustified duplicate positive mixing term would raise pressure, but that duplication must be demonstrated rather than assumed. [S3, S5, S6] |

The exact source function `qc_disp.descriptors` calls `DispersionModel.get_properties()` after a seeded embedding/MMFF geometry, sums its C6 matrix and its polarizabilities, and saves only two molecular descriptors. In the far-field interaction of two molecular copies, every atom in copy one interacts with every atom in copy two. The full sum, including entries whose two atom labels happen to have the same index, is appropriate to that descriptor. Taking a triangular intramolecular sum or inserting one-half would change its meaning. Conversely, those descriptors alone are not a validated contact free energy. [S6, U2]

The D4 method itself is a charge- and coordination-dependent model built from electronic-structure response data, with separate choices for evaluating damped dispersion energies. “Not fitted to this ThermoML benchmark” is the appropriate scope. It does not imply that the MMFF geometry, every D4 parametrization, the cavity radii and the liquid-contact construction are parameter-free first-principles consequences. The present proposal does not alter any of those stored descriptors. [S6, U3]

Source defects and avoidable work are separate from the physical audit. The descriptor generator does not check the fallback embedding return status or the MMFF convergence code, suppresses MMFF exceptions, and records later failures as two NaNs without a per-compound failure reason. It does not retain the generating geometry or atom-level response matrices in the molecular table. Those are reproducibility limitations, not proof that particular retained C6 values are wrong. P57 records invalid or duplicate descriptor identities and stops affected required comparisons; it does not rerun failed molecules under an unregistered recipe. The existing London dispatch also precedes the use_dsp check, so use_dsp=False alone does not remove a London term. LV1 avoids that trap by applying an explicit difference of two dispersion free energies rather than mutating a switch. [S5, S6]

Exactly one alternative: LV1

I propose one conditional A model: a **D4/SK cohesive-density volume regular-solution dispersion term**, called `R16-LV1-cohesive-density-SK-volume-regular-solution`. It is a thermodynamically defined alternative to molecular random-contact counting, not a claim to have derived the unique dispersion free energy of a liquid.

Retain the original u_i from cavity-sphere self contact, kappa from the same C6/alpha combination, z=10 and weight one. In the numerical convention where V_i is in cubic angstroms per molecule and u_i is in kcal/mol of contacts, define

\[
 c_i=\frac{5u_i}{V_i},\qquad
 c_{12}=\kappa\sqrt{c_1c_2},\qquad
 K=c_1+c_2-2c_{12}\geq0.
\]

The quantities c_i are an assumed cohesive-energy scale per numerical cavity volume, not experimental cohesive-energy densities. The corresponding physical energy density includes the common molar conversion, which cancels when forming the final molar excess energy.

Assume a homogeneous volume-random energetic density proportional to

\[
 -\left(\phi_1^2c_1+2\phi_1\phi_2c_{12}+\phi_2^2c_2\right),
 \qquad \phi_i=\frac{x_iV_i}{\bar V},\quad \bar V=x_1V_1+x_2V_2.
\]

Subtract the two linear pure-component references. Since x_i V_i=Vbar*phi_i, the molar excess dispersion term is

\[
 \boxed{g_V^E=\bar V\phi_1\phi_2K
        =\frac{x_1x_2V_1V_2}{\bar V}K.}
\]

Taking partial molar derivatives gives

\[
 \boxed{\ln\gamma_{1,V}=\frac{V_1\phi_2^2K}{RT},\qquad
        \ln\gamma_{2,V}=\frac{V_2\phi_1^2K}{RT}.}
\]

The volume factors are derived from this stated gE. They are not an arbitrary replacement of x in the old expression. This energetic structure is the regular-solution form; its use here with D4-derived cohesive scales and kappa is the declared additional approximation. No experimental heat of vaporization or solubility parameter is substituted. The ordinary COSMO combinatorial contribution stays intact, so no extra Flory-Huggins entropy is added. [U4]

For equal volumes, equal diameters give q=1, and V*K=5w. LV1 then reduces exactly to the old London Margules term. Identical fluids have zero excess contribution. Label exchange is symmetric, pure-solvent activity is one, and the analytic expression satisfies Gibbs-Duhem. Its dispersion-only infinite-dilution contributions have ratio V1/V2 rather than being forced equal. With the stored inputs held constant, the energetic gV is temperature independent and contributes that same energy to HE in the analytic limit. The implemented HE screen retains the existing finite-temperature-difference convention instead of mixing a new analytic enthalpy with an old baseline stencil.

LV1 is not a uniform downweight. A synthetic test with V=(40,320), C6=(100,6400) and alpha=(20,160), in the declared units, increases one component contribution and decreases the other at equal mole fraction; its molar excess energy also increases. This is an algebra test, not a molecular or experimental result. Nothing in the acceptance procedure searches these inputs or selects a coefficient to obtain lower pressure.

Several limitations are deliberate. The unlike cohesive normalization is a model assumption; D4 does not force it. The self energies still use molecular spheres and a fixed coordination. If a homologous sequence has C6 approximately proportional to molecular size squared and volume proportional to size, the retained self-contact energy is roughly constant, rather than an extensive liquid cohesive energy. Dividing it by cavity volume does not solve that scaling problem. LV1 also retains nonnegative dispersion excess energy and omits distributed contact geometry and many-body effects. These weaknesses prevent calling it a validated general liquid model. They do not prevent testing the one explicitly specified closure, at zero QC cost, without optimizing it on the benchmark.

A distributed atomic/surface-contact model is assessed, but is not a second candidate here. The table discards the atom-level matrices and generating coordinates. Recomputing 742 descriptor sets would not by itself determine interfacial orientations or liquid contact probabilities. For an illustrative 100-binary panel, 100 contact orientations with 25x25 atom pairs would already require 6.25 million pair evaluations, before rejection, damping or sampling convergence. That arithmetic can be inexpensive; its unvalidated contact ensemble is the actual issue. No new atom-level descriptor campaign, raw-UD download, or empirical contact selection is authorized by this report.

Exact reuse of the unchanged residual

The London term is additive and independent of the electrostatic coefficient. Therefore the proposed pair of models can share one unchanged Z0x call:

\[
 \boldsymbol\ell_{V}
 =\boldsymbol\ell_{\mathrm{Z0x}}
 +\mathcal D_x\{(g_V^E-g_L^E)/(RT)\},
\]

where D_x maps a molar binary excess energy to its two partial molar chemical potentials. The new code implements this explicitly. It never changes just a coefficient while retaining the wrong composition derivative. The existing electrostatic chain rule, HB constants and profile processing are untouched. [S5, S7]

In the analytic interior and P28 pure endpoints, the correction is the difference of the two analytic dispersion contributions. In the adjacent numerical strip, the correction is passed through the same old h=1e-4 finite-difference operation as the baseline gE. This preserves the existing numerical prescription, including its limitations. The new candidate is A relative to London; sharing the residual between the two stated models is E arithmetic, not a physical equivalence claim. No new sigma bins are generated and no E-equivalence claim is made for the candidate's changed infinite-dilution predictions.

The scalar calculation is O(1) per query after pair construction. A naive two-model experiment requires two baseline residual evaluations for each state; this implementation needs one. For the LLE screen, the two log-augmented grids contain 101 and 181 nodes; their exact union is 181. Reusing that union avoids 101 duplicate baseline evaluations per pair/temperature without rounding any distinct state together. These savings are exact query counts. File hashing, process startup and difficult segment solves mean the wall-clock gain need not be exactly twofold.

The frozen, exposed comparison and tradeoff gates

P58 is one fixed-design look at already exposed data. It neither reconstructs a new holdout nor claims that excluding glycol observations erases development exposure. No source is advertised as genuinely unexposed. The temporal set is left alone. A favorable result may be reported as a frozen development comparison; an untouched-generalization claim would require a separate custodian-controlled source audit. [S2–S4]

The VLE primary collection is exactly P54's 963 identities, with the original component order, temperatures, compositions and frozen Psat values. The new preparation invokes the unchanged R15 saved-output checker, retains its full source/input requirements and imports its saved baseline and 2010 pressures. It does not rerun P52 or choose a new sample. Before guard-property queries begin, every new unchanged-Z0x pressure must reproduce its P54 value to relative difference strictly below 1e-8. One failed anchor blocks the guard phase; it cannot be converted into a changed-baseline comparison.

IDAC, HE and positive LLE guard CSVs must be byte-identical to the reference-main original benchmark files, even when supplied as private copies. Their original test_one/test_both and has_sigma decisions are retained. Eligibility requires a valid same-source profile and positive finite C6, alpha and epsilon inputs, within the declared temperature scope. Every input-only exclusion is frozen before predictions. Malformed eligible responses stop preparation. A later solver failure cannot create a smaller favorable subset. The negative collection is the saved original 336-state archive, with its original test subset; its complete hash and one-state-per-eligible-binary identities are frozen rather than regenerated through a fresh discovery function. [S8]

All eligible IDAC observations use P28 consistently. HE uses the original central difference at T±0.5 K, common to both arms. The sign guard uses |HE|>20 J/mol. Candidate values are derived from saved, finite baseline vectors, so the exact same requested states enter both models. No experimental datum determines an input or parameter after the plan is frozen.

LLE uses common lower-convex-hull tests at the log-augmented 81- and 161-point interior grids. A gap exceeds 1e-7 in dimensionless g/(RT). Both grids must agree for each arm and state. Positive observations retain the existing 2 K evaluation rounding; negatives retain their recorded temperatures. A nonfinite or unresolved grid is not “miscible” and blocks complete acceptance. This is a declared numerical detection screen, not an exact binodal calculation or a global stability certificate. It is compared with its own freshly evaluated baseline under identical rules and does not replace an archived BA number.

| Property | Fixed success condition for this exposed screen |
|---|---|
| VLE | Candidate-minus-baseline AAD is negative, and its one-sided 95% paired-system bootstrap upper bound is below zero. |
| IDAC | Candidate-minus-baseline MAE and its one-sided upper bound are <=0. No positive allowed-worsening margin. |
| HE | The same zero-margin MAE condition, plus no decrease in sign correctness on the fixed |HE|>20 subset. |
| LLE detection | Recall and balanced accuracy do not decrease, including nonnegative one-sided lower bounds on their paired changes. False-positive rate and its change's upper bound do not increase. Every requested grid must be resolved. |

The bootstrap has 1,000 resamples and a fixed seed. LLE samples systems separately within its positive and negative classes; the positive system definition retains the more-than-half-of-observations rule. Counts remain separate for both classes. These bounds are predefined resampling filters on an exposed collection, not guarantees restored by having written a registration. A statistically inconclusive guard fails acceptance rather than passing because its interval contains zero.

Report the candidate-versus-saved-2010 AAD difference on the same 963 rows separately. Its point difference and upper bound must be <=0 before calling the gap closed on this exposed panel. Even that does not establish closure of the main7 or temporal gaps. Passing VLE alone is insufficient; passing every guard does not automatically change production defaults. The complete proposed registration includes all these distinctions.

Budget and operational controls

Let NI and NH be the frozen eligible IDAC and HE row counts. Let NL count the distinct ordered-pair/temperature LLE jobs, including positive and negative collections. Then

\[
 Q=963+N_I+2N_H+181N_L
\]

unchanged baseline calls generate both arms. A separate complete model evaluation for both arms would require 2Q such calls. Every plan is rejected before execution if Q exceeds 180,000. There is no automatic subsampling to fit the budget. The actual counts and exclusions are available from the private freeze, not guessed from earlier scorecard denominators.

The measured P54 average, 722/7704=0.09372 seconds per request including its run overhead, would give approximately 16,869 seconds for 180,000 requests. This is a planning extrapolation, not a native R16 benchmark. Grid compositions and process grouping can change the cost. The fixed model/orchestration ceiling is 21,600 seconds on the owned Mac, serial, four OpenMP threads and one BLAS thread, with at most 180 seconds per worker. Record closing read-only checks separately. No paid resources, GPU jobs or quantum calculations are needed. [S2]

The driver clears inherited experimental switches, uses explicit two-profile overlays in fresh subprocesses and writes attempt receipts before each query. It creates one permanent exclusive execution claim. All jobs receive terminal records, including blocked and budget-unstarted jobs. Input and output hashes are checked; missing or nonfinite values withhold complete tradeoff summaries. A complete but unfavorable screen stays complete with a false acceptance flag. Neither failure nor an unfavorable result authorizes another output directory, a new weight or a retry. Raw descriptors, per-pair decompositions, profiles and row-level outputs stay private. Only the aggregate error allowlist is eligible for separate human review before publication.

Manuscript endgame

P59 inserts the actual P54 attribution into the abstract and a dedicated results section, with all eight corners and the correct observation count. It updates the discussion from the older ES-first hypothesis to the measured London-first result for Z0x. It explains why the sign theorem concerns the implemented closure and why fitted or deleted-term corners remain diagnostics. It fixes the -4.23 versus -4.47 bias wording and adds a separate clarification rather than altering historical result files.

The patch leaves the earlier main7 and temporal numerical tables unchanged. It retains the R2-R9 gradient and optimizer qualifications, the frozen exploratory open-profile scope, the glycol coordinate explanation and tetraEG exception, P28/P55 endpoint distinctions, and the narrower claim about experimental inputs. The manuscript's bibliography remains explicitly pending its own publisher-level verification; this task has not silently converted every inherited reference into a verified citation. [S9]

The current record answers the main question usefully: electronic descriptors without new ThermoML regression can support some useful predictions, but the conversion from those descriptors to local liquid contacts has large conditional error. P54 makes that limitation concrete. The paper should be finalized with that explanation whether LV1 succeeds, fails, is incomplete or is never executed.

Execution and verification record

Executed here: repository and primary-source review; complete byte verification of the current manuscript, current COSMO-SAC solver and current Z0x source used in tests; reconstruction of unchanged R14/R15 helpers from the delivered reports; algebraic analysis and synthetic tests. Fifty-eight new tests passed, including actual segment-solver tests on synthetic profiles, derivative/endpoint checks, the 963-row synthetic freeze and mocked worker/driver failure tests. The unchanged R14 suite also passed its 45 tests in a separate process. Thus 103 portable tests passed in those two invocations. The R15 suite's recorded NumPy import-isolation issue is not relabeled resolved; the new tests avoid deleting and restoring the process module dictionary.

The source environment is a Git-blob-verified reconstruction of the relevant subset, not a full cloned repository. Real native constructors, actual Mac assets and the prior physical-run checker were mocked where explicitly identified in the tests. The table schema and retrieved entries were reviewed; a full real descriptor census and the per-P54-pair audit remain P57 work on the Mac. Neither a test fixture nor successful syntax is presented as the real 963-row experiment.

Not executed: any new molecular calculation, D4 regeneration, simulation, candidate molecular prediction, experimental score, Mac archive check, full guard collection freeze or production adoption. PySCF, DFT-D4, thermo and chemicals are absent here, and no new package installation was attempted. No UD file was accessed or redistributed, no remote repository was modified and no workflow was dispatched.

Patch extraction from this delivered report, independent and combined application, and command syntax checks passed. All 103 portable tests passed again from the freshly extracted and applied source. The patch groups are H16, P57P58, T16, P59 and REG16. H16/P57P58/T16 are interdependent at test/runtime, but their file diffs are independently applicable to the same pinned main.

Exact application, registration and execution commands

Save this Markdown report outside the repository and set `R16_REPORT` to that real path. These commands apply only the reviewed diff set. They do not reset the checkout or change production source. Run the software checks before adopting the registration.

```bash
set -euo pipefail
BASE=ca5c7e94627fcdebbf787afb688f8cab10e42a03
test "$(git rev-parse HEAD)" = "$BASE"
: "${R16_REPORT:?Set R16_REPORT to the downloaded ZCOSMO_ROUND16_REPORT.md}"
export R16_PATCHES="$(mktemp -d)"
python - <<'PY'
import os,re
from pathlib import Path
s=Path(os.environ['R16_REPORT']).read_text()
parts=re.findall(r'<!-- BEGIN PATCH (\w+) -->\s*```diff\n(.*?)\n```\s*<!-- END PATCH \1 -->',s,re.S)
assert [n for n,b in parts]==['H16','P57P58','T16','P59','REG16']
root=Path(os.environ['R16_PATCHES'])
for n,b in parts:(root/(n+'.patch')).write_text(b+'\n')
PY
for p in H16 P57P58 T16 P59 REG16; do
  git apply --check "$R16_PATCHES/$p.patch"
done
cat "$R16_PATCHES/H16.patch" "$R16_PATCHES/P57P58.patch" \
  "$R16_PATCHES/T16.patch" "$R16_PATCHES/P59.patch" \
  "$R16_PATCHES/REG16.patch" > "$R16_PATCHES/all.patch"
git apply --check "$R16_PATCHES/all.patch"
git apply "$R16_PATCHES/all.patch"
export PYTHONPATH=src:scripts
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python scripts/r16_selftest.py
python scripts/r14_selftest.py
python -m py_compile scripts/r16_london.py scripts/r16_stats.py \
  scripts/r16_review.py scripts/r16_selftest.py
git diff --check
git diff --quiet -- src/zcosmo results/qc results/z_params
```

The next block adopts the complete protocol. It is supplied for the maintainer to execute, not a claim that adoption happened during this review. Existing registrations are appended to, not overwritten. No experimental work starts merely from committing these files.

```bash
set -euo pipefail
umask 077
printf '\nRound 16 adopted at %s\n\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" >> PREREGISTRATION.md
cat docs/astra/round16/REGISTRATION_PROPOSED.md >> PREREGISTRATION.md
git add scripts/r16_london.py scripts/r16_stats.py scripts/r16_review.py \
  scripts/r16_selftest.py docs/astra/round16/REGISTRATION_PROPOSED.md \
  docs/astra/round16/P54_CLARIFICATION.md manuscript/draft.md PREREGISTRATION.md
git diff --cached --check
git commit -m "Register R16 London audit and single LV1 exposed tradeoff screen"
export R16_REG="$(git rev-parse HEAD)"
```

The real-data commands are for the asset-bearing native Mac, in its existing environment. `R15_PLAN` and `R15_RUN` must point to the original P54 private plan and complete run, not a synthetic fixture, newly regenerated archive or P52 directory. The known P54 digest commit is used below. `R16_NEGATIVE_ARCHIVE` can be set to the actual saved 336-state archive when it is stored elsewhere. An absent asset stops the process; these commands do not regenerate it.

```bash
set -euo pipefail
umask 077
: "${R16_REG:?Run the registration block first}"
: "${R15_PLAN:?Set to the original completed P54 private plan.json}"
: "${R15_RUN:?Set to the original completed P54 run directory}"
export R15_PLAN_COMMIT=3655e1126422238f5cf69a7197950285cb383fb4
export R16_PRIVATE="${R16_PRIVATE:-$HOME/zc-r16-lv1-20261008}"
export R16_NEGATIVE_ARCHIVE="${R16_NEGATIVE_ARCHIVE:-$PWD/results/predictions/lle_negatives.csv}"
export R16_UD_PROFILES="${R16_UD_PROFILES:-$PWD/data/raw/nist/UD/sigma3}"
export PYTHONPATH=src:scripts
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
test -f "$R15_PLAN"
test -f "$R15_RUN/summary.json"
test -f "$R16_NEGATIVE_ARCHIVE"
test -d "$R16_UD_PROFILES"
mkdir -p "$R16_PRIVATE"
chmod 700 "$R16_PRIVATE"
/usr/bin/time -p python scripts/r16_review.py freeze \
  --registration "$R16_REG" --r15-plan "$R15_PLAN" \
  --r15-plan-commit "$R15_PLAN_COMMIT" --r15-run "$R15_RUN" \
  --idac "$PWD/data/benchmark/idac.csv" --he "$PWD/data/benchmark/he.csv" \
  --positive "$PWD/data/benchmark/lle.csv" --negative "$R16_NEGATIVE_ARCHIVE" \
  --ud-profiles "$R16_UD_PROFILES" --out "$R16_PRIVATE/plan" \
  > "$R16_PRIVATE/freeze.log" 2>&1
python - <<'PY'
import json,os
from pathlib import Path
p=Path(os.environ['R16_PRIVATE'])/'plan/plan.json'
m=json.loads(p.read_text())
print('Frozen baseline requests:',m['baseline_requests'])
print('Requested guard rows:',{k:v['eligible_rows'] for k,v in m['coverage'].items()})
print('Production adoption:',m['design']['adopted'])
PY
cp "$R16_PRIVATE/plan/PLAN_SHA256.txt" docs/astra/round16/PLAN_SHA256.txt
git add docs/astra/round16/PLAN_SHA256.txt
git commit -m "Freeze R16 private LV1 plan digest and exact guard population"
export R16_PLAN_COMMIT="$(git rev-parse HEAD)"
```

Inspect `audit-private.json` and the preparation receipts locally. This is P57's old-formula audit, with zero new activity calls. Its terms must not be published as experimental-error shares. A budget or input failure is not permission to edit the selection and execute another recipe. The next block is exactly one claimed experiment.

```bash
set -euo pipefail
umask 077
: "${R16_PRIVATE:?Run the freeze block first}"
: "${R16_PLAN_COMMIT:?Commit the frozen plan digest first}"
export PYTHONPATH=src:scripts
set +e
/usr/bin/time -p python scripts/r16_review.py run \
  --plan "$R16_PRIVATE/plan/plan.json" --plan-commit "$R16_PLAN_COMMIT" \
  --out "$R16_PRIVATE/run" > "$R16_PRIVATE/run.log" 2>&1
rc=$?
set -e
if [ "$rc" -ne 0 ]; then
  printf 'R16 returned status %s. Preserve all receipts; do not retry or remove the claim.\n' "$rc"
  exit "$rc"
fi
python scripts/r16_review.py check \
  --plan "$R16_PRIVATE/plan/plan.json" --plan-commit "$R16_PLAN_COMMIT" \
  --run "$R16_PRIVATE/run" > "$R16_PRIVATE/check.log" 2>&1
python - <<'PY'
import json,os
from pathlib import Path
root=Path(os.environ['R16_PRIVATE'])/'run'
a=json.loads((root/'public-errors.json').read_text())
t=json.loads((root/'timing.json').read_text())
print(json.dumps({'status':a['status'],'acceptance':a['acceptance'],'timing':t},indent=2))
print('A complete run with acceptance.passed=false is an unfavorable result, not acceptance.')
print('No output here authorizes production adoption or a second candidate.')
PY
# Keep audit-private.json, private-predictions.json, plans and logs outside Git.
# public-errors.json is eligible only for a separate human-reviewed publication step.
```

`check` may be repeated without model calls. After an interrupted driver, `collect` can construct a failure summary from existing terminal and attempt receipts only; it cannot restart workers. It writes fresh summary files and is not a way to overwrite an already collected result. Never rerun `run` into another directory. The command exit status reports operational completeness, while the separate `acceptance.passed` field reports the declared exposed-screen decision.

Sources and exact scope

[S1] `docs/astra/ROUND16_PROMPT.md`, repository main at `ca5c7e94627fcdebbf787afb688f8cab10e42a03`. [S2] `docs/astra/round15/RESULTS.md`, same commit, Git blob `dd2eeb1fa384f320e338341cd72bd5479a69ba9c`. [S3] `PREREGISTRATION.md`, especially original London weight one, session-1 ablations and R14/R15, together with `docs/OPTIMIZATION_BRIEF.md`. These are primary project records, not new independent experiments.

[S4] `docs/astra/round14/RESULTS.md` and the delivered round-14/round-15 reports. The exact round-15 report was verified against Git blob `482b03e656e290c7913073783a4ace22ea250546`. Original results and later diagnostic denominators remain separate.

[S5] `src/zcosmo/cosmosac.py`, Git blob `c226a668b7b9dba9e7400cda180fafd8faa700f3`, especially `london_pair_w`, `london_lngamma` and `Mixture.lngamma_disp`. [S6] `src/zcosmo/qc_disp.py`, Git blob `86e4d8af89579149c3891debfc7e0c0205afc88b`; `results/qc/dispersion.csv`, Git blob `c999b0874860d6f27ca436f4b81eb115a1ddb34e`; and the original HB recipe in `src/zcosmo/zmodel.py`.

[S7] `src/zcosmo/z0x.py`, Git blob `c558d4e95db9b78f3b57d6a103a293e21feeb9af`; `src/zcosmo/models.py`; `scripts/r15_factorial.py`, Git blob `2b2e2f71bcee48eb0c503e429ead3d478b2e9450`; and `scripts/r15_math.py`, Git blob `6f944a7f8f44b5a42cdea88b10b4b45aa17002d2`. [S8] `src/zcosmo/evaluate.py`, `metrics.py`, `lle_negatives.py` and the frozen original benchmark paths. The exact private negative-archive bytes were not available here.

[S9] `manuscript/draft.md` at the reference main, Git blob `6cea4ec764d95588f8a6371cd36acdcaeb421fea`. Its full reconstructed bytes were verified before producing P59. The patch does not claim to have verified every inherited bibliography entry.

[U1] Gould and Bucko, *C6 coefficients and dipole polarizabilities for all atoms and many ions in rows 1–6 of the periodic table*, author version at `https://arxiv.org/abs/1604.02751`, DOI `10.1021/acs.jctc.6b00361`. Its tested combining relation is an approximation; its atomic/ionic results are not a validation of this molecular-liquid model.

[U2] Official DFT-D4 Python implementation, `https://dftd4.readthedocs.io/en/latest/_modules/dftd4/interface.html`, especially `get_properties` versus the damped energy interface. This was used to verify what the property call provides, not to regenerate descriptors with a newer installed package.

[U3] Caldeweyher et al., *A generally applicable atomic-charge dependent London dispersion correction*, J. Chem. Phys. 150, 154122 (2019), DOI `10.1063/1.5090222`. Author-method page: `https://www.chemie.uni-bonn.de/grimme/de/software/dft-d4`; author preprint and publication metadata: `https://www.cambridge.org/engage/chemrxiv/article-details/60c74060f96a006646286291`. The inspected method description distinguishes response coefficients and the complete energy correction.

[U4] Official regular-solution implementation and equations, `https://thermo.readthedocs.io/thermo.regular_solution.html`. The volume-weighted energetic structure supports the derivation under its assumptions. The particular D4 cohesive normalization in LV1 is an additional hypothesis of this report, not claimed to be validated by that documentation. No experimental solubility parameters from its examples were used.

All repository paths above are pinned to the reference commit unless a historical source version is explicitly named. External primary-source documentation was checked during this review; no new external measurement dataset was scored.


<!-- BEGIN PATCH H16 -->
```diff
diff --git a/scripts/r16_london.py b/scripts/r16_london.py
new file mode 100644
--- /dev/null
+++ b/scripts/r16_london.py
@@ -0,0 +1,197 @@
+"""One R16 candidate: D4-based volume regular-solution dispersion (LV1).
+
+A physical approximation, never an E-equivalent replacement for London.
+No production registry/default is modified. No data is read at import time.
+The original residual is evaluated once and shared by the two comparison arms.
+"""
+from __future__ import annotations
+
+from dataclasses import dataclass
+import math
+import os
+import numpy as np
+
+BOHR_A = 0.52917721067
+HARTREE_KCAL = 627.509474
+R_KCAL = 1.38064903e-23 * 6.022140758e23 / 4184.0  # Match current evaluator.
+RECIPE = 'R16-LV1-cohesive-density-SK-volume-regular-solution'
+
+
+def require(condition, message):
+    if not condition:
+        raise ValueError(message)
+
+
+def positive_pair(values, name):
+    a = np.array(values, dtype=float, copy=True)
+    require(a.shape == (2,) and np.isfinite(a).all() and (a > 0).all(),
+            'Expected two finite positive ' + name)
+    return a
+
+
+def state(T, x):
+    T = float(T)
+    a = np.asarray(x, dtype=float)
+    require(math.isfinite(T) and T > 0 and a.shape == (2,) and
+            np.isfinite(a).all() and (a >= 0).all() and (a <= 1).all() and
+            abs(float(a.sum()) - 1.0) <= 1e-14, 'Invalid binary state')
+    return T, a
+
+
+def sech_parts(t):
+    """sech(t), 1-sech(t), with a stable nonnegative small-difference term."""
+    t = abs(float(t))
+    a = math.exp(-t)
+    den = 1.0 + a*a
+    return 2.0*a/den, math.expm1(-t)**2/den
+
+
+@dataclass(frozen=True)
+class LondonPair:
+    c6: tuple
+    alpha: tuple
+    volumes: tuple
+
+    def __post_init__(self):
+        for name in ('c6', 'alpha', 'volumes'):
+            object.__setattr__(self, name, tuple(positive_pair(getattr(self, name), name)))
+        require(all(math.isfinite(v) and v > 0 for v in self.self_energies()),
+                'Descriptor/volume range gives invalid self-contact energy')
+
+    def diameters(self):
+        return 2.0 * (3.0*np.array(self.volumes)/(4.0*np.pi))**(1.0/3.0) / BOHR_A
+
+    def self_energies(self):
+        """Positive magnitudes u_i=C6_ii/d_i^6, kcal/mol of contacts."""
+        with np.errstate(over='raise', under='ignore', divide='raise', invalid='raise'):
+            return np.array(self.c6) / self.diameters()**6 * HARTREE_KCAL
+
+    def spectral(self):
+        c0, c1 = self.c6
+        a0, a1 = self.alpha
+        t = 0.5*(math.log(c0)-math.log(c1)) - math.log(a0) + math.log(a1)
+        return sech_parts(t)
+
+    def old_audit(self):
+        """Exact algebraic decomposition, not attribution of experimental error."""
+        u = self.self_energies()
+        di = self.diameters()
+        kappa, one_minus_kappa = self.spectral()
+        geom, _ = sech_parts(0.5*math.log(float(di[0]/di[1])))
+        q = geom**6
+        root = math.sqrt(float(u[0]*u[1]))
+        parts = ((math.sqrt(u[0])-math.sqrt(u[1]))**2,
+                 2*root*one_minus_kappa,
+                 2*root*kappa*(1-q))
+        # Direct reference expression follows current london_pair_w arithmetic.
+        c0, c1 = self.c6
+        a0, a1 = self.alpha
+        cross = 2*c0*c1 / ((a1/a0)*c0 + (a0/a1)*c1)
+        old_w = float((c0/di[0]**6 + c1/di[1]**6 -
+                       2*cross/((di[0]+di[1])/2)**6)*HARTREE_KCAL)
+        require(math.isfinite(old_w) and abs(old_w-sum(parts)) <=
+                1e-10*max(1.0, float(u.max())), 'London decomposition failed')
+        return dict(kappa=kappa, geometry_factor=q, self_energies_kcal=u.tolist(),
+                    w_kcal=old_w, components_kcal=dict(cohesive_mismatch=parts[0],
+                    spectral_mismatch=parts[1], arithmetic_contact_size=parts[2]))
+
+    def coefficients(self):
+        """Original Margules numerator L and new energy-density K.
+
+        L=(z/2)w, kcal/mol. K=(z/2)[u1/V1+u2/V2-
+        2*kappa*sqrt(u1*u2/(V1*V2))], kcal/mol/A^3. z=10 and weight=1
+        are inherited, explicitly unmodified conventions, not newly fitted.
+        """
+        old = 5.0*self.old_audit()['w_kcal']
+        u = self.self_energies()/np.array(self.volumes)
+        _, omk = self.spectral()
+        K = 5.0*((math.sqrt(u[0])-math.sqrt(u[1]))**2 +
+                 2*math.sqrt(float(u[0]*u[1]))*omk)
+        require(math.isfinite(K) and K >= 0, 'Invalid cohesive-density coefficient')
+        return old, K
+
+
+class DispersionChange:
+    """Only the difference between the two excess-Gibbs terms, at fixed inputs."""
+    def __init__(self, pair: LondonPair):
+        self.pair = pair
+        self.volumes = np.array(pair.volumes)
+        self.L, self.K = pair.coefficients()
+
+    def energies(self, x):
+        """Old and LV1 molar excess energies in kcal/mol (T independent)."""
+        _, x = state(1.0, x)
+        V = float(x @ self.volumes)
+        phi = x*self.volumes/V
+        return float(self.L*x[0]*x[1]), float(V*phi[0]*phi[1]*self.K)
+
+    def terms(self, T, x):
+        T, x = state(T, x)
+        phi = x*self.volumes/float(x @ self.volumes)
+        old = self.L * x[::-1]**2/(R_KCAL*T)
+        new = self.K * self.volumes * phi[::-1]**2/(R_KCAL*T)
+        return old, new
+
+    def delta(self, T, x, h=1e-4, exact_endpoint=True):
+        """Match the current base dispatch, including its near-endpoint stencil.
+
+        This avoids silently converting the adjacent numerical strip to a new
+        derivative prescription. P28 endpoints are exact only when enabled.
+        """
+        T, x = state(T, x)
+        t = float(x[0])
+        require(math.isfinite(h) and 0 < h < 0.5, 'Invalid stencil')
+        if h < t < 1-h or (t in (0., 1.) and exact_endpoint):
+            old, new = self.terms(T, x)
+            return new-old
+        def dg(v):
+            old, new = self.energies([v, 1-v])
+            return (new-old)/(R_KCAL*T)
+        lo, hi = max(t-h, 0.), min(t+h, 1.)
+        slope = (dg(hi)-dg(lo))/(hi-lo)
+        g = dg(t)
+        return np.array([g+(1-t)*slope, g-t*slope])
+
+
+class PairedLondon:
+    """Adapter for the unchanged Z0x baseline and exactly one LV1 candidate."""
+    ok = True
+
+    def __init__(self, baseline, pair: LondonPair):
+        p = baseline.z0
+        require(p.disp_mode == 'london' and p.w_dsp == 1.0 and p.z == 10.0,
+                'LV1 requires the original registered London convention')
+        require(np.array_equal(np.asarray(baseline.V), np.array(pair.volumes)),
+                'Density and COSMO-volume conventions differ')
+        self.baseline = baseline
+        self.change = DispersionChange(pair)
+
+    def paired(self, T, x):
+        T, x = state(T, x)
+        old = np.asarray(self.baseline.lngamma(T, x), dtype=float)
+        delta = self.change.delta(T, x, self.baseline.H,
+                os.environ.get('ZC_R6_ENDPOINT', '0') == '1')
+        require(old.shape == (2,) and np.isfinite(old).all(), 'Invalid baseline result')
+        new = old+delta
+        require(np.isfinite(new).all(), 'Invalid LV1 result')
+        return old, new
+
+    def lngamma(self, T, x):
+        return self.paired(T, x)[1]
+
+    def lngamma_inf(self, T, solute_index=0):
+        require(solute_index in (0, 1), 'Invalid solute index')
+        x = np.zeros(2); x[1-solute_index] = 1.0
+        return float(self.lngamma(T, x)[solute_index])
+
+
+def make_pair(keys):
+    """Real source imports are lazy; caller must freeze inputs before calling."""
+    from zcosmo.z0x import Z0xBinary
+    from zcosmo.cosmosac import _london_table, load_fluid
+    base = Z0xBinary(keys)
+    desc = _london_table(base.z0.london_table)
+    pair = LondonPair(tuple(desc[k][0] for k in keys),
+                      tuple(desc[k][1] for k in keys),
+                      tuple(load_fluid(k).V for k in keys))
+    return PairedLondon(base, pair)
diff --git a/scripts/r16_stats.py b/scripts/r16_stats.py
new file mode 100644
--- /dev/null
+++ b/scripts/r16_stats.py
@@ -0,0 +1,143 @@
+"""R16 fixed-design accounting. No model evaluation and no data acquisition."""
+from __future__ import annotations
+import hashlib
+import numpy as np
+from r16_london import require
+
+BOOTSTRAPS = 1000
+SEED = 'R16-LV1-fixed-look-20261008'
+GRID_SIZES = (81, 161)
+GAP_TOL = 1e-7  # dimensionless g/RT, numerical indicator, not a certificate
+
+
+def grids():
+    return tuple(np.unique(np.r_[np.logspace(-6, -2, 10),
+        np.linspace(.02, .98, n), 1-np.logspace(-2, -6, 10)]) for n in GRID_SIZES)
+
+
+def grid_union():
+    return np.unique(np.concatenate(grids()))
+
+
+def hull_gap(x, g):
+    x, g = np.asarray(x, float), np.asarray(g, float)
+    require(x.ndim == g.ndim == 1 and len(x) >= 3 and x.shape == g.shape and
+            np.isfinite(x).all() and np.isfinite(g).all() and
+            (np.diff(x) > 0).all(), 'Invalid convexity grid')
+    hull = []
+    for k in range(len(x)):
+        while len(hull) >= 2:
+            a, b = hull[-2:]
+            if (x[b]-x[a])*(g[k]-g[a])-(g[b]-g[a])*(x[k]-x[a]) > 0:
+                break
+            hull.pop()
+        hull.append(k)
+    line = np.interp(x, x[hull], g[hull])
+    gap = float(np.max(g-line))
+    return gap > GAP_TOL, gap
+
+
+def detection(lngamma):
+    """Same baseline/candidate grids. A disagreement is not called miscibility."""
+    union = grid_union(); a = np.asarray(lngamma, float)
+    require(a.shape == (len(union), 2) and np.isfinite(a).all(), 'Incomplete LLE grid')
+    indicators, gaps = [], []
+    for x in grids():
+        idx = np.searchsorted(union, x)
+        require(np.array_equal(union[idx], x), 'LLE grid identity drift')
+        g = x*np.log(x)+(1-x)*np.log1p(-x)+x*a[idx,0]+(1-x)*a[idx,1]
+        found, gap = hull_gap(x, g)
+        indicators.append(found); gaps.append(gap)
+    return dict(detected=indicators[0] if indicators[0] == indicators[1] else None,
+                grid_agreement=indicators[0] == indicators[1], gaps=gaps,
+                numerical_indicator_not_global_stability=True)
+
+
+def rng_for(label):
+    seed = int.from_bytes(hashlib.sha256((SEED+'|'+label).encode()).digest()[:8], 'big')
+    return np.random.default_rng(seed)
+
+
+def paired_summary(truth, values, systems, label, percent=False):
+    """Equal observation weight, with a paired system bootstrap.
+
+    Intervals describe this exposed collection; they are not fresh holdout
+    inference. One-sided 95% bounds use the 5th and 95th percentiles.
+    """
+    truth, values = np.asarray(truth, float), np.asarray(values, float)
+    require(truth.ndim == 1 and len(truth) > 0 and values.shape == (len(truth),2)
+            and len(systems) == len(truth) and np.isfinite(truth).all()
+            and np.isfinite(values).all(), 'Incomplete paired metric')
+    signed = values-truth[:,None]
+    if percent:
+        require((truth > 0).all(), 'Pressure must be positive')
+        signed *= 100/truth[:,None]
+    require(np.isfinite(signed).all(), 'Derived metric overflow')
+    losses = np.abs(signed)
+    unique = sorted(set(systems))
+    groups = [np.flatnonzero(np.array(systems) == s) for s in unique]
+    counts = np.array([len(i) for i in groups])
+    sums = np.array([losses[i].sum(0) for i in groups])
+    rng = rng_for(label); delta = []
+    for _ in range(BOOTSTRAPS):
+        sample = rng.integers(0, len(groups), len(groups))
+        means = sums[sample].sum(0)/counts[sample].sum()
+        delta.append(means[1]-means[0])
+    return dict(rows=len(truth), systems=len(groups), baseline=float(losses[:,0].mean()),
+        candidate=float(losses[:,1].mean()), change=float(np.diff(losses.mean(0))[0]),
+        bias=signed.mean(0).tolist(), equal_system=np.mean(sums/counts[:,None],axis=0).tolist(),
+        delta_CI95=np.quantile(delta,[.025,.975]).tolist(),
+        delta_one_sided_upper95=float(np.quantile(delta,.95)),
+        improved=int((losses[:,1] < losses[:,0]).sum()),
+        worsened=int((losses[:,1] > losses[:,0]).sum()),
+        scope='exposed fixed-design comparison; no restored holdout guarantee')
+
+
+def lle_summary(positive, negative):
+    """Rows: (system, baseline detection, candidate detection).
+
+    Positive systems use the original >half-of-observations rule. Negatives
+    must have exactly one saved state per unordered binary. No uncertain
+    state is permitted to enter this function as False.
+    """
+    require(positive and negative, 'Both LLE classes required')
+    def group(rows, is_negative=False):
+        result = []
+        systems = sorted({r[0] for r in rows})
+        for s in systems:
+            part = [(r[1],r[2]) for r in rows if r[0] == s]
+            require(all(type(v) is bool for p in part for v in p), 'Unresolved LLE detection')
+            if is_negative:
+                require(len(part) == 1, 'Duplicate negative binary')
+            result.append(np.array(part).mean(0) > .5)
+        return np.array(result, float), systems
+    p, ps = group(positive); n, ns = group(negative,True)
+    recall, fp = p.mean(0), n.mean(0)
+    ba = .5*(recall+1-fp)
+    rng = rng_for('lle'); changes = []
+    for _ in range(BOOTSTRAPS):
+        rp = p[rng.integers(0,len(p),len(p))].mean(0)
+        fn = n[rng.integers(0,len(n),len(n))].mean(0)
+        changes.append([rp[1]-rp[0],fn[1]-fn[0],.5*((rp[1]-rp[0])-(fn[1]-fn[0]))])
+    changes = np.array(changes)
+    return dict(positive_rows=len(positive),positive_systems=len(ps),negative_systems=len(ns),
+        recall=recall.tolist(),false_positive_rate=fp.tolist(),balanced_accuracy=ba.tolist(),
+        recall_change_lower95=float(np.quantile(changes[:,0],.05)),
+        false_positive_change_upper95=float(np.quantile(changes[:,1],.95)),
+        balanced_accuracy_change_lower95=float(np.quantile(changes[:,2],.05)),
+        numerical_indicator_not_global_stability=True)
+
+
+def gates(scores):
+    """No positive noninferiority margin; failure is recorded without tuning."""
+    v, i, h, l = (scores[k] for k in ('vle','idac','he','lle'))
+    flags = dict(vle_improves=v['change'] < 0 and v['delta_one_sided_upper95'] < 0,
+        idac_does_not_worsen=i['change'] <= 0 and i['delta_one_sided_upper95'] <= 0,
+        he_does_not_worsen=h['change'] <= 0 and h['delta_one_sided_upper95'] <= 0,
+        lle_recall_does_not_worsen=l['recall'][1] >= l['recall'][0] and l['recall_change_lower95'] >= 0,
+        lle_false_positives_do_not_worsen=l['false_positive_rate'][1] <= l['false_positive_rate'][0]
+            and l['false_positive_change_upper95'] <= 0,
+        lle_balanced_accuracy_does_not_worsen=l['balanced_accuracy'][1] >= l['balanced_accuracy'][0]
+            and l['balanced_accuracy_change_lower95'] >= 0)
+    return dict(checks=flags,passed=all(flags.values()),adopted=False,
+                scope='One exposed development screen, not universal or untouched validation')
```
<!-- END PATCH H16 -->

<!-- BEGIN PATCH P57P58 -->
```diff
diff --git a/scripts/r16_review.py b/scripts/r16_review.py
new file mode 100644
--- /dev/null
+++ b/scripts/r16_review.py
@@ -0,0 +1,448 @@
+"""Private R16 audit and one fixed LV1 screen. No QC, MD or production writes.
+
+P54's VLE rows and frozen saturation pressures are retained. Other properties
+use all input-covered original test rows. No runtime finite-subset selection.
+Only unchanged Z0x is queried; LV1 uses an exact additive correction to its gE.
+"""
+from __future__ import annotations
+import argparse
+import hashlib
+import json
+import math
+import os
+from pathlib import Path
+import subprocess
+import sys
+import time
+import numpy as np
+import r14_dielectric as d
+import r14_oracle as r14
+import r15_factorial as r15
+import r16_london as law
+import r16_stats as stats
+
+ROOT = d.ROOT
+BASE = 'ca5c7e94627fcdebbf787afb688f8cab10e42a03'
+MARKER = 'R16-P57-P58-P59: London audit, one LV1 screen, and P54 reporting'
+FILES = ('scripts/r16_london.py','scripts/r16_stats.py',
+         'scripts/r16_review.py','scripts/r16_selftest.py')
+DESIGN = dict(recipe=law.RECIPE,vle_rows=963,vle_systems=100,
+    source='completed original P54 and original benchmark test collections',
+    native_QC=0,MD_steps=0,max_baseline_requests=180000,driver_seconds=21600,
+    worker_seconds=180,OMP_threads=4,BLAS_threads=1,no_retries=True,
+    exact_endpoint=True,he_dT_K=.5,grid_sizes=list(stats.GRID_SIZES),gap_tolerance=stats.GAP_TOL,
+    baseline_relative_pressure_tolerance=1e-8,bootstrap_replicates=stats.BOOTSTRAPS,
+    bootstrap_seed=stats.SEED,adopted=False,exposed=True,
+    failure='withhold complete tradeoff/acceptance; never drop a failed row',
+    fallback='no candidate for unavailable input; explicitly counted before queries')
+
+
+def registration(commit):
+    r15.ancestor(commit);r15.ancestor(BASE,commit)
+    text=r15.git_bytes(commit,'PREREGISTRATION.md').decode()
+    d.require(MARKER in text and law.RECIPE in text,'R16 registration absent')
+    for rel in FILES:
+        d.require((ROOT/rel).read_bytes()==r15.git_bytes(commit,rel),'Unregistered R16 source: '+rel)
+    # No change to the participating baseline or to the P55 repair is allowed.
+    for p in (ROOT/'src/zcosmo').glob('*.py'):
+        rel=str(p.relative_to(ROOT))
+        d.require(p.read_bytes()==r15.git_bytes(BASE,rel),'Production source drift: '+rel)
+    for rel in ('results/qc/dispersion.csv','results/qc/dielectric.csv','results/z_params/Z0.json'):
+        d.require((ROOT/rel).read_bytes()==r15.git_bytes(BASE,rel),'Model table changed: '+rel)
+    return commit
+
+
+def read_profile(path):
+    lines=Path(path).read_text().splitlines()
+    d.require(lines and lines[0].startswith('# meta: '),'Profile metadata absent')
+    meta=json.loads(lines[0][8:]);a=np.loadtxt(path)
+    grid=np.tile(np.round(np.linspace(-.025,.025,51),3),3)
+    d.require(a.shape==(153,2) and np.isfinite(a).all() and
+        np.max(abs(a[:,0]-grid))<1e-12 and (a[:,1]>=0).all() and a[:,1].sum()>0,
+        'Invalid frozen sigma profile')
+    V=float(meta['volume [A^3]'])
+    d.require(math.isfinite(V) and V>0,'Invalid cavity volume')
+    return V
+
+
+def table_inputs():
+    rows=d.records(ROOT/'results/qc/dispersion.csv');tab={};bad=[]
+    for r in rows:
+        k=r['inchikey'];d.require(k and k not in tab,'Duplicate/missing dispersion identity')
+        v=[d.number(r.get(c)) for c in ('C6_au','alpha_au')]
+        tab[k]=v
+        if any(q is None or q<=0 for q in v):bad.append(k)
+    ers=d.records(ROOT/'results/qc/dielectric.csv');eps={}
+    for r in ers:
+        d.require(r['inchikey'] not in eps,'Duplicate dielectric identity')
+        eps[r['inchikey']]=d.number(r['eps'])
+    return tab,eps,dict(dispersion_rows=len(rows),invalid_descriptor_keys=bad)
+
+
+def flag(v):
+    if v in (True,'True','true','1',1):return True
+    if v in (False,'False','false','0',0):return False
+    raise ValueError('Ambiguous boolean metadata')
+
+
+def guard_rows(path,kind,available):
+    """Input-only eligibility, with every exclusion reason retained privately."""
+    original=d.records(path);selected=[];exclusions=[]
+    if kind=='negative':d.require(len(original)==336,'Not the original 336-state negative archive')
+    for i,r in enumerate(original):
+        if r.get('split') not in ('train','test_one','test_both'):
+            raise ValueError('Unknown original split label')
+        reason=None
+        if r['split']=='train':reason='original_train'
+        elif 'has_sigma' in r and not flag(r['has_sigma']):reason='original_no_sigma'
+        cols=('solute','solvent') if kind=='idac' else ('c1','c2')
+        keys=[r[c] for c in cols]
+        T=d.number(r.get('T'))
+        if reason is None and (T is None or not 250<=T<=450):reason='outside_temperature_scope'
+        if reason is None and keys[0]==keys[1]:reason='self_pair'
+        if reason is None:
+            failures=[available(k) for k in keys]
+            if any(q is not None for q in failures):reason='input_unavailable:'+','.join(q or 'ok' for q in failures)
+        if reason:
+            exclusions.append(dict(row_id=f'{kind}:{i}',reason=reason));continue
+        out=dict(row_id=f'{kind}:{i}',keys=keys,T=T,system='|'.join(sorted(keys)))
+        if kind=='idac':
+            out.update(x1=0.,truth=d.number(r.get('ln_gamma_inf')))
+        elif kind=='he':
+            out.update(x1=d.number(r.get('x1')),truth=d.number(r.get('HE_J')))
+            d.require(out['x1'] is not None and 0<out['x1']<1,'Invalid HE composition')
+        elif kind=='positive':
+            x=d.number(r.get('x1'));d.require(x is not None and 0<=x<=1,'Invalid LLE observation')
+            out.update(T=float(round(T/2)*2),observed_T=T,observed_x1=x)
+        if kind in ('idac','he'):d.require(out['truth'] is not None,'Invalid original response')
+        selected.append(out)
+    d.require(selected,'Empty fixed '+kind+' guard collection')
+    if kind=='negative':d.require(len({r['system'] for r in selected})==len(selected),'Duplicate negative systems')
+    return selected,dict(original_rows=len(original),eligible_rows=len(selected),exclusions=exclusions)
+
+
+def queries(task):
+    k=task['kind'];out=[]
+    if k in ('vle','idac','he'):
+        for r in task['members']:
+            offsets=(-DESIGN['he_dT_K'],DESIGN['he_dT_K']) if k=='he' else (0.,)
+            for j,dt in enumerate(offsets):
+                out.append(dict(query_id=r['row_id']+':'+str(j),T=r['T']+dt,x1=r['x1']))
+    else:
+        out=[dict(query_id=f'grid:{i}',T=task['T'],x1=float(x)) for i,x in enumerate(stats.grid_union())]
+    return out
+
+
+def tasks_for(vle,guards):
+    tasks=[]
+    for kind,rows in [('vle',vle),*((k,guards[k]) for k in ('idac','he','positive','negative'))]:
+        groups={}
+        for r in rows:
+            key=tuple(r['keys'])+((r['T'],) if kind in ('positive','negative') else ())
+            groups.setdefault(key,[]).append(r)
+        for key,members in sorted(groups.items()):
+            t=dict(id=f'job-{len(tasks):05d}',kind=kind,keys=list(key[:2]),members=members)
+            if kind in ('positive','negative'):t['T']=float(key[2])
+            t['queries']=queries(t);tasks.append(t)
+    return tasks
+
+
+def freeze(a):
+    d.mac();reg=registration(a.registration)
+    prior=argparse.Namespace(plan=a.r15_plan,plan_commit=a.r15_plan_commit,run=a.r15_run)
+    d.require(r15.check(prior)==0,'P54 saved check failed')
+    oldp,oldm=r15.load(a.r15_plan,a.r15_plan_commit)
+    vals,n,hashes=r15.arrays(oldm,a.r15_run,d.sha(oldp))
+    d.require(n==7704 and len(oldm['rows'])==963 and r15.anchor(oldm,vals)['passed'],
+              'Not the complete original P54 experiment')
+    tab,eps,census=table_inputs();profiles=dict(oldm['profiles']);volumes={};rejected={}
+    def available(k):
+        if k in rejected:return rejected[k]
+        if k not in tab or any(v is None or v<=0 for v in tab[k]):reason='dispersion'
+        elif k not in eps or eps[k] is None or eps[k]<1:reason='dielectric'
+        else:
+            try:
+                p=Path(profiles[k]) if k in profiles else r14.profile_path(k,a.ud_profiles)
+                volumes[k]=read_profile(p);profiles[k]=str(p.resolve());return None
+            except (OSError,ValueError,KeyError):reason='profile'
+        rejected[k]=reason;return reason
+    vle=[]
+    for i,r in enumerate(oldm['rows']):
+        keys=[r['c1'],r['c2']]
+        d.require(all(available(k) is None for k in keys),'P54 input missing; no row removal')
+        vle.append(dict(r,keys=keys,truth=r['P'],expected_P=float(vals[i,0]),reference_P=float(vals[i,7])))
+    d.require(len({r['row_id'] for r in vle})==963 and len({r['system'] for r in vle})==100,'P54 identity changed')
+    guards={};coverage={}
+    input_paths={k:Path(getattr(a,k)).expanduser().resolve() for k in ('idac','he','positive','negative')}
+    # Copies are permitted, a changed benchmark or newly selected split is not.
+    for kind,rel in (('idac','data/benchmark/idac.csv'),('he','data/benchmark/he.csv'),
+                     ('positive','data/benchmark/lle.csv')):
+        d.require(input_paths[kind].read_bytes()==r15.git_bytes(BASE,rel),
+                  'Guard is not the frozen original benchmark: '+kind)
+    for kind,p in input_paths.items():guards[kind],coverage[kind]=guard_rows(p,kind,available)
+    d.require(any(abs(r['truth'])>20 for r in guards['he']), 'HE sign guard has no eligible rows')
+    tasks=tasks_for(vle,guards);request_count=sum(len(t['queries']) for t in tasks)
+    d.require(request_count<=DESIGN['max_baseline_requests'],'Full fixed screen exceeds budget; no automatic downsampling')
+    pairs={};old_terms=[]
+    for keys in sorted({tuple(t['keys']) for t in tasks}):
+        q=law.LondonPair(tuple(tab[k][0] for k in keys),tuple(tab[k][1] for k in keys),tuple(volumes[k] for k in keys))
+        pairs['|'.join(keys)]=dict(c6=list(q.c6),alpha=list(q.alpha),volumes=list(q.volumes))
+        if any(tuple(r['keys'])==keys for r in vle):old_terms.append(dict(keys=list(keys),**q.old_audit()))
+    # P57 is an old-formula audit only. Candidate coefficients are first consumed
+    # by post-run analysis under the committed LV1 plan; no score is made here.
+    sources=[*(ROOT/r for r in FILES),*list((ROOT/'src/zcosmo').glob('*.py'))]
+    sources += [ROOT/'results/qc/dispersion.csv',ROOT/'results/qc/dielectric.csv',ROOT/'results/z_params/Z0.json']
+    sources += [ROOT/'scripts/r14_dielectric.py',ROOT/'scripts/r14_oracle.py',
+                ROOT/'scripts/r15_factorial.py',ROOT/'scripts/r15_math.py']
+    worker_inputs=d.fingerprint(sources)
+    inputs=dict(oldm['inputs']);inputs.update(hashes);inputs.update(worker_inputs)
+    inputs.update(d.fingerprint([oldp,oldp.parent/'execution_claim.json',Path(a.r15_run)/'summary.json',
+        Path(a.r15_run)/'public-errors.json',*input_paths.values(),*profiles.values()]))
+    out=d.private(a.out,True)
+    d.write(out/'audit-private.json',dict(descriptor_census=census,pairs=old_terms,
+        activity_calls=0,QCs=0,energy_terms_are_not_error_attributions=True))
+    inputs.update(d.fingerprint([out/'audit-private.json']))
+    m=dict(schema='r16-lv1-v1',base=BASE,registration=reg,design=DESIGN,environment=d.environment(),
+        inputs=inputs,worker_inputs=worker_inputs,profiles=profiles,pairs=pairs,tasks=tasks,
+        source_P54=dict(plan=str(oldp),commit=a.r15_plan_commit,run=str(Path(a.r15_run).resolve())),
+        protected_counts=oldm['protected_counts'],coverage=coverage,baseline_requests=request_count,
+        exposure=dict(old_compound_split='already exposed',temporal='not rescored; already exposed',
+          P54='963 exposed VLE rows; unchanged',custodian_holdout=None,recipe_fixed=law.RECIPE,
+          may_claim_unexposed=False,may_adopt=False))
+    d.check_inputs(inputs);d.write(out/'plan.json',m)
+    (out/'PLAN_SHA256.txt').write_text(d.sha(out/'plan.json')+'\n')
+    print('R16 private plan frozen; baseline request budget:',request_count)
+
+
+def load(plan,commit,full=True):
+    d.mac();p=d.private(plan);m=d.read(p);registration(m['registration'])
+    r15.ancestor(commit);r15.ancestor(m['registration'],commit)
+    d.require(r15.git_bytes(commit,'docs/astra/round16/PLAN_SHA256.txt').decode().strip()==d.sha(p),
+              'Plan digest not committed or changed')
+    d.require(m['schema']=='r16-lv1-v1' and m['base']==BASE and m['design']==DESIGN,'Design drift')
+    d.require(m['environment']==d.environment(),'Environment drift')
+    d.require(m['protected_counts']=={'profiles_v2':630,'s1_stalled':1,'s2_stalled':5},'Frozen population drift')
+    d.require(m['baseline_requests']==sum(len(t['queries']) for t in m['tasks'])<=DESIGN['max_baseline_requests'],
+              'Budget drift')
+    for t in m['tasks']:d.require(t['queries']==queries(t),'Query identity drift')
+    d.check_inputs(m['inputs'] if full else m['worker_inputs'])
+    return p,m
+
+
+def native_baseline(keys,profiles):
+    from zcosmo.z0x import Z0xBinary
+    from zcosmo.cosmosac import load_fluid,sigma_path
+    for k in keys:
+        d.require(sigma_path(k).resolve()==Path(profiles[k]).resolve(),'Silent profile fallback')
+        d.require(load_fluid(k).V==read_profile(profiles[k]),'Profile volume mismatch')
+    base=Z0xBinary(keys);pr=base.z0
+    d.require(pr.z==10. and pr.w_dsp==1. and pr.disp_mode=='london' and base.H==1e-4,
+              'Unexpected baseline London/derivative prescription')
+    return base
+
+
+def worker(a):
+    p,m=load(a.plan,a.plan_commit,False);task=next(t for t in m['tasks'] if t['id']==a.job)
+    claim=d.read(p.parent/'execution_claim.json');out=d.private(a.out)
+    d.require(claim==dict(plan_sha256=d.sha(p),output=str(out.parent)),'Worker outside claimed run')
+    d.require(out.name==task['id'],'Wrong worker directory')
+    checks={m['profiles'][k]:m['inputs'][str(Path(m['profiles'][k]).resolve())] for k in task['keys']}
+    d.check_inputs(checks);out=d.private(out,True);overlay=out/'overlay';overlay.mkdir(mode=0o700)
+    for key in list(os.environ):
+        if key.startswith('ZC_'):os.environ.pop(key)
+    os.environ['ZC_SIGMA_OVERRIDE_DIR']=str(overlay);os.environ['ZC_R6_ENDPOINT']='1'
+    for k in task['keys']:(overlay/(k+'.sigma')).symlink_to(m['profiles'][k])
+    base=native_baseline(task['keys'],m['profiles'])
+    values=[]
+    for j,q in enumerate(task['queries']):
+        d.write(out/f'attempt-{j:05d}.json',dict(query_id=q['query_id'],attempted=True))
+        value=None;error=None
+        try:
+            lg=np.asarray(base.lngamma(q['T'],np.array([q['x1'],1-q['x1']])),float)
+            d.require(lg.shape==(2,) and np.isfinite(lg).all(),'Nonfinite baseline')
+            value=lg.tolist()
+        except Exception as ex:error=type(ex).__name__
+        values.append(dict(query_id=q['query_id'],lngamma=value,error=error))
+    d.check_inputs(checks);d.check_inputs(m['worker_inputs'])
+    d.write(out/'result.json',dict(job=task['id'],plan_sha256=d.sha(p),values=values))
+
+
+def arrays(m,run,ph):
+    run=Path(run);raw={};hashes={};n=0
+    states={'not_started','not_run_budget','blocked_anchor','returned','timeout','launch_failed'}
+    for t in m['tasks']:
+        tp=run/(t['id']+'.terminal.json');term=d.read(tp);hashes.update(d.fingerprint([tp]))
+        d.require(term['job']==t['id'] and term['plan_sha256']==ph and term['state'] in states,'Terminal identity drift')
+        folder=run/t['id'];attempts=sorted(folder.glob('attempt-*.json'))
+        d.require(len(attempts)<=len(t['queries']),'Request budget exceeded')
+        for j,f in enumerate(attempts):
+            d.require(f.name==f'attempt-{j:05d}.json' and d.read(f)==dict(query_id=t['queries'][j]['query_id'],attempted=True),
+                      'Attempt receipt drift')
+        n+=len(attempts);hashes.update(d.fingerprint(attempts))
+        a=np.full((len(t['queries']),2),np.nan);dest=folder/'result.json'
+        if term['state']=='returned' and term['returncode']==0 and dest.is_file():
+            z=d.read(dest);hashes.update(d.fingerprint([dest]))
+            d.require(z['job']==t['id'] and z['plan_sha256']==ph and len(attempts)==len(t['queries'])
+                and [v['query_id'] for v in z['values']]==[q['query_id'] for q in t['queries']], 'Result identity drift')
+            for j,v in enumerate(z['values']):
+                if v['lngamma'] is not None:
+                    g=np.asarray(v['lngamma'],float);d.require(g.shape==(2,), 'Wrong component dimension');a[j]=g
+        raw[t['id']]=a
+    d.require(n<=m['baseline_requests'],'Actual request budget exceeded')
+    return raw,n,hashes
+
+
+def anchor(m,raw):
+    err=[];finite=0;requested=0
+    for t in m['tasks']:
+        if t['kind']!='vle':continue
+        for r,lg in zip(t['members'],raw[t['id']]):
+            requested+=1
+            if not np.isfinite(lg).all():continue
+            try:p=r14.pressure(lg,r['x1'],r['psat'])
+            except (ValueError,FloatingPointError):continue
+            e=abs(p/r['expected_P']-1)
+            if math.isfinite(e):err.append(e);finite+=1
+    value=max(err) if finite==requested and requested else None
+    return dict(requested=requested,finite=finite,max_relative_error=value,
+        passed=value is not None and value<DESIGN['baseline_relative_pressure_tolerance'])
+
+
+def analyze(m,raw):
+    ar=anchor(m,raw)
+    counts={k:dict(requested=0,finite=0) for k in ('vle','idac','he','positive','negative')}
+    for t in m['tasks']:
+        counts[t['kind']]['requested']+=len(t['queries'])
+        counts[t['kind']]['finite']+=int(np.isfinite(raw[t['id']]).all(1).sum())
+    status=dict(anchor=ar,query_coverage=counts,complete=False,adopted=False,
+                exposed=True,recipe=law.RECIPE,QC_calls=0)
+    if not ar['passed'] or any(v['requested']!=v['finite'] for v in counts.values()):
+        return dict(status=status,scores=None,acceptance=None,private_predictions=None)
+    records={k:[] for k in counts};uncertain=[]
+    try:
+        for t in m['tasks']:
+            ch=law.DispersionChange(law.LondonPair(**m['pairs']['|'.join(t['keys'])]))
+            b=raw[t['id']]
+            c=np.array([lg+ch.delta(q['T'],[q['x1'],1-q['x1']],exact_endpoint=True)
+                        for q,lg in zip(t['queries'],b)])
+            d.require(np.isfinite(c).all(),'Candidate arithmetic overflow')
+            if t['kind'] in ('positive','negative'):
+                ds=[stats.detection(z) for z in (b,c)]
+                if any(z['detected'] is None for z in ds):uncertain.append(t['id'])
+                for r in t['members']:
+                    records[t['kind']].append(dict(row_id=r['row_id'],system=r['system'],
+                        values=[z['detected'] for z in ds],diagnostics=ds))
+            else:
+                for j,r in enumerate(t['members']):
+                    if t['kind']=='vle':
+                        pred=[r14.pressure(z[j],r['x1'],r['psat']) for z in (b,c)]
+                    elif t['kind']=='idac':pred=[float(z[j,0]) for z in (b,c)]
+                    else:
+                        x=np.array([r['x1'],1-r['x1']]);dt=DESIGN['he_dT_K']
+                        pred=[float(-8.314462618*r['T']**2*(x@(z[2*j+1]-z[2*j]))/(2*dt)) for z in (b,c)]
+                    d.require(np.isfinite(pred).all(),'Nonfinite derived property')
+                    z=dict(row_id=r['row_id'],system=r['system'],truth=r['truth'],values=pred)
+                    if t['kind']=='vle':z['reference_P']=r['reference_P']
+                    records[t['kind']].append(z)
+    except (ValueError,FloatingPointError,OverflowError) as ex:
+        status['analysis_error']=type(ex).__name__
+        return dict(status=status,scores=None,acceptance=None,private_predictions=records)
+    status['unresolved_grid_jobs']=uncertain
+    if uncertain:return dict(status=status,scores=None,acceptance=None,private_predictions=records)
+    try:
+        scores={}
+        for kind in ('vle','idac','he'):
+            r=records[kind]
+            scores[kind]=stats.paired_summary([v['truth'] for v in r],[v['values'] for v in r],
+                          [v['system'] for v in r],kind,percent=kind=='vle')
+        vr=records['vle']
+        scores['vle_vs_2010']=stats.paired_summary([v['truth'] for v in vr],
+            [[v['reference_P'],v['values'][1]] for v in vr],[v['system'] for v in vr], 'vle_vs_2010',True)
+        scores['lle']=stats.lle_summary([(r['system'],*r['values']) for r in records['positive']],
+                                       [(r['system'],*r['values']) for r in records['negative']])
+        # HE sign is retained as an additional no-worsening point-estimate guard.
+        hr=[r for r in records['he'] if abs(r['truth'])>20.]
+        d.require(hr,'No HE sign-control rows')
+        sign=[float(np.mean([np.sign(r['values'][j])==np.sign(r['truth']) for r in hr])) for j in (0,1)]
+        scores['he']['sign_correct']=sign;scores['he']['sign_rows']=len(hr)
+        result=stats.gates(scores)
+        result['checks']['he_sign_does_not_worsen']=sign[1]>=sign[0]
+        result['passed']=all(result['checks'].values())
+        ref=scores['vle_vs_2010']
+        result['gap_closed_on_exposed_panel']=ref['change']<=0 and ref['delta_one_sided_upper95']<=0
+        status['complete']=True
+        return dict(status=status,scores=scores,acceptance=result,private_predictions=records)
+
+    except (ValueError,FloatingPointError,OverflowError) as ex:
+        status['analysis_error']=type(ex).__name__
+        return dict(status=status,scores=None,acceptance=None,private_predictions=records)
+
+
+def public(q):
+    return dict(status=q['status'],scores=q['scores'],acceptance=q['acceptance'],
+                statement='exposed one-recipe screen; no automatic production adoption')
+
+
+def collect(a):
+    p,m=load(a.plan,a.plan_commit);run=d.private(a.run)
+    d.require(d.read(p.parent/'execution_claim.json')==dict(plan_sha256=d.sha(p),output=str(run)),'Claim drift')
+    raw,n,h=arrays(m,run,d.sha(p));q=analyze(m,raw);d.check_inputs(m['inputs'])
+    d.write(run/'private-predictions.json',q['private_predictions'])
+    d.write(run/'summary.json',dict(plan_sha256=d.sha(p),baseline_requests=n,output_hashes=h,**public(q)))
+    d.write(run/'public-errors.json',public(q))
+    print('R16 complete:',q['status']['complete'],'screen passed:',q['acceptance'] and q['acceptance']['passed'])
+    return 0 if q['status']['complete'] else 2
+
+
+def run(a):
+    p,m=load(a.plan,a.plan_commit);out=d.private(a.out)
+    d.require(not out.exists(),'Output already exists')
+    d.write(p.parent/'execution_claim.json',dict(plan_sha256=d.sha(p),output=str(out)))
+    out=d.private(out,True);start=time.monotonic();env=dict(os.environ)
+    env.update(OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1')
+    for t in m['tasks']:
+        d.write(out/(t['id']+'.terminal.json'),dict(job=t['id'],plan_sha256=d.sha(p),state='not_started',returncode=None))
+    ar=None
+    for t in m['tasks']:
+        if t['kind']!='vle' and ar is None:ar=anchor(m,arrays(m,out,d.sha(p))[0])
+        remain=DESIGN['driver_seconds']-(time.monotonic()-start)
+        term=dict(job=t['id'],plan_sha256=d.sha(p),state='not_run_budget',returncode=None)
+        if t['kind']!='vle' and not ar['passed']:term['state']='blocked_anchor'
+        elif remain>1:
+            cmd=[sys.executable,str(Path(__file__).resolve()),'_worker','--plan',str(p),
+                 '--plan-commit',a.plan_commit,'--job',t['id'],'--out',str(out/t['id'])]
+            try:term.update(r14.launch(cmd,out/(t['id']+'.log'),min(remain,DESIGN['worker_seconds']),env))
+            except Exception:term['state']='launch_failed'
+        tmp=out/(t['id']+'.terminal.tmp');d.write(tmp,term);os.replace(tmp,out/(t['id']+'.terminal.json'))
+    native_seconds=time.monotonic()-start;closing=time.monotonic()
+    rc=collect(argparse.Namespace(plan=str(p),plan_commit=a.plan_commit,run=str(out)))
+    d.write(out/'timing.json',dict(baseline_model_wall_s=native_seconds,
+        closing_readonly_wall_s=time.monotonic()-closing,total_driver_wall_s=time.monotonic()-start))
+    return rc
+
+
+def check(a):
+    p,m=load(a.plan,a.plan_commit);run=d.private(a.run);z=d.read(run/'summary.json')
+    d.require(d.read(p.parent/'execution_claim.json')==dict(plan_sha256=d.sha(p),output=str(run)),'Claim drift')
+    raw,n,h=arrays(m,run,d.sha(p));q=analyze(m,raw)
+    d.require(z==dict(plan_sha256=d.sha(p),baseline_requests=n,output_hashes=h,**public(q)), 'Saved summary drift')
+    d.require(d.read(run/'private-predictions.json')==q['private_predictions'] and
+              d.read(run/'public-errors.json')==public(q), 'Derived outputs drift')
+    print('R16 checked without new model queries. Complete:',q['status']['complete'])
+    return 0 if q['status']['complete'] else 2
+
+
+def main():
+    ap=argparse.ArgumentParser(description=__doc__);sp=ap.add_subparsers(dest='cmd',required=True)
+    q=sp.add_parser('freeze');q.add_argument('--registration',required=True)
+    for arg in ('r15-plan','r15-plan-commit','r15-run','idac','he','positive','negative','ud-profiles','out'):
+        q.add_argument('--'+arg,required=True)
+    q.set_defaults(fn=freeze)
+    for name,fn in (('run',run),('collect',collect),('check',check),('_worker',worker)):
+        q=sp.add_parser(name);q.add_argument('--plan',required=True);q.add_argument('--plan-commit',required=True)
+        q.add_argument('--run' if name in ('collect','check') else '--out',required=True)
+        if name=='_worker':q.add_argument('--job',required=True)
+        q.set_defaults(fn=fn)
+    a=ap.parse_args();return a.fn(a)
+
+if __name__=='__main__':raise SystemExit(main())
```
<!-- END PATCH P57P58 -->

<!-- BEGIN PATCH T16 -->
```diff
diff --git a/scripts/r16_selftest.py b/scripts/r16_selftest.py
new file mode 100644
--- /dev/null
+++ b/scripts/r16_selftest.py
@@ -0,0 +1,522 @@
+"""Portable R16 tests. Synthetic inputs only; no module-cache clearing.
+
+The real current segment solver and the unchanged Z0x class AST are used for
+numerical tests, with synthetic profile/table providers. Mac/file/Git checks
+in driver tests are mocked explicitly. No scientific acceptance is implied.
+"""
+from __future__ import annotations
+import argparse
+import ast
+from contextlib import contextmanager
+from dataclasses import replace
+import hashlib
+import itertools
+import math
+import json
+import os
+from pathlib import Path
+import tempfile
+import types
+import unittest
+from unittest.mock import patch
+import numpy as np
+from scipy import linalg  # Import once, not through a restored module dictionary.
+import r16_london as law
+import r16_stats as st
+import r16_review as run
+from zcosmo import cosmosac as cs
+
+ROOT=Path(__file__).resolve().parents[1]
+
+
+def pair(volumes=(45.,130.),c6=(400.,3600.),alpha=(30.,100.)):
+    return law.LondonPair(c6,alpha,volumes)
+
+
+def profile(path,V=45.):
+    p=np.zeros((3,51));p[0,10]=30.;p[0,35]=40.;p[1,12]=15.;p[2,40]=15.
+    text='# meta: '+json.dumps({'volume [A^3]':V})+'\n'
+    text+=''.join(f'{s:.3f} {v:.15e}\n' for s,v in zip(np.tile(cs.SIG,3),p.ravel()))
+    Path(path).write_text(text)
+
+
+@contextmanager
+def actual_model(volumes=(45.,130.)):
+    p=cs.Params(A_ES=12226.235339788673,B_ES=0.,c_OH_OH=5712.229463082564,
+                c_OT_OT=5611.4027535161395,c_OH_OT=5987.642651646004,
+                disp_mode='london',w_dsp=1.)
+    a=np.zeros((3,51));a[0,14]=20;a[0,29]=20;a[1,12]=5;a[2,41]=5
+    b=np.zeros((3,51));b[0,18]=35;b[0,36]=45;b[1,11]=10;b[2,39]=10
+    fluids={k:cs.Fluid(k,v,float(v.sum()),V,'NHB',1.,{}) for k,v,V in zip(('A','B'),(a,b),volumes)}
+    tab={'A':(400.,30.),'B':(3600.,100.)}
+    path=ROOT/'src/zcosmo/z0x.py';tree=ast.parse(path.read_text())
+    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Z0xBinary')
+    ns=dict(np=np,os=os,Mixture=lambda keys,prm:cs.Mixture(keys,prm,fluids=[fluids[k] for k in keys]),
+            solve_gamma=cs.solve_gamma,_pure_lnG=cs._pure_lnG,SIG=cs.SIG,R_KCAL=cs.R_KCAL,
+            load_fluid=lambda k:fluids[k],load_z_params=lambda name:p,
+            _eps=lambda:{'A':2.5,'B':31.},c_es_theory=lambda fpol:12226.235339788673*fpol)
+    exec(compile(ast.Module(body=[cls],type_ignores=[]),str(path),'exec'),ns)
+    with patch.object(cs,'_london_table',return_value=tab),patch.dict(os.environ,{'ZC_R6_ENDPOINT':'1'}):
+        yield ns['Z0xBinary'](['A','B']),fluids,p
+
+
+class Algebra(unittest.TestCase):
+    def test_source_blobs(self):
+        for rel,expected in [('src/zcosmo/cosmosac.py','c226a668b7b9dba9e7400cda180fafd8faa700f3'),
+                             ('src/zcosmo/z0x.py','c558d4e95db9b78f3b57d6a103a293e21feeb9af')]:
+            b=(ROOT/rel).read_bytes()
+            self.assertEqual(hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest(),expected)
+
+    def test_decomposition_random(self):
+        rng=np.random.default_rng(16)
+        for _ in range(100):
+            p=pair(tuple(rng.uniform(20,400,2)),tuple(np.exp(rng.uniform(3,10,2))),tuple(rng.uniform(10,200,2)))
+            d=p.old_audit()
+            self.assertGreaterEqual(min(d['components_kcal'].values()),0.)
+            self.assertAlmostEqual(d['w_kcal'],sum(d['components_kcal'].values()),places=10)
+            self.assertGreaterEqual(d['w_kcal'],-1e-12)
+
+    def test_current_formula_reference(self):
+        p=pair();f=[types.SimpleNamespace(key=k,V=v) for k,v in zip(('A','B'),p.volumes)]
+        tab={k:v for k,v in zip(('A','B'),zip(p.c6,p.alpha))}
+        with patch.object(cs,'_london_table',return_value=tab):
+            self.assertAlmostEqual(p.old_audit()['w_kcal'],cs.london_pair_w(*f,'synthetic'),places=13)
+
+    def test_identical_species(self):
+        p=pair((90.,90.),(1600.,1600.),(60.,60.))
+        for v in p.old_audit()['components_kcal'].values():self.assertAlmostEqual(v,0.,places=13)
+        a,b=law.DispersionChange(p).terms(300.,[.23,.77])
+        np.testing.assert_allclose(a,0.,atol=1e-12);np.testing.assert_allclose(b,0.,atol=1e-12)
+
+    def test_equal_volumes_recover_original(self):
+        c=law.DispersionChange(pair((80.,80.)))
+        for x in (0.,.05,.5,.99,1.):
+            for T in (250.,298.15,450.):np.testing.assert_allclose(*c.terms(T,[x,1-x]),rtol=1e-12,atol=1e-12)
+
+    def test_exchange_symmetry(self):
+        p=pair();q=law.LondonPair(p.c6[::-1],p.alpha[::-1],p.volumes[::-1])
+        c,d=law.DispersionChange(p),law.DispersionChange(q)
+        for x in (0.,.17,.6,1.):
+            np.testing.assert_allclose(c.terms(333.,[x,1-x])[1],d.terms(333.,[1-x,x])[1][::-1],atol=1e-13)
+
+    def test_derivative_of_total_excess_energy(self):
+        c=law.DispersionChange(pair());T=317.;x=.36;h=1e-5
+        def g(t):return c.energies([t,1-t])[1]/(law.R_KCAL*T)
+        slope=(g(x+h)-g(x-h))/(2*h)
+        np.testing.assert_allclose(c.terms(T,[x,1-x])[1],[g(x)+(1-x)*slope,g(x)-x*slope],atol=2e-8,rtol=0)
+
+    def test_gibbs_duhem(self):
+        c=law.DispersionChange(pair());x=.42;h=1e-6
+        d=(c.terms(310.,[x+h,1-x-h])[1]-c.terms(310.,[x-h,1-x+h])[1])/(2*h)
+        self.assertLess(abs(np.dot([x,1-x],d)),1e-7)
+
+    def test_infinite_dilution_asymmetry(self):
+        c=law.DispersionChange(pair());T=300.
+        self.assertAlmostEqual(c.terms(T,[0.,1.])[1][0]/c.terms(T,[1.,0.])[1][1],45./130.,places=12)
+        self.assertEqual(c.terms(T,[0.,1.])[1][1],0.)
+
+    def test_temperature_and_enthalpy(self):
+        c=law.DispersionChange(pair());x=np.array([.3,.7]);T=333.;h=.5
+        exact=c.energies(x)[1]*8.314462618/law.R_KCAL
+        v=-(8.314462618*T*T)*x@(c.terms(T+h,x)[1]-c.terms(T-h,x)[1])/(2*h)
+        self.assertAlmostEqual(v/exact,T*T/(T*T-h*h),places=10)
+
+    def test_not_a_uniform_downweight(self):
+        c=law.DispersionChange(pair((40.,320.),(100.,6400.),(20.,160.)))
+        a,b=c.terms(300.,[.5,.5]);self.assertGreater(b[0],a[0]);self.assertLess(b[1],a[1])
+        self.assertGreater(c.energies([.5,.5])[1],c.energies([.5,.5])[0])
+
+    def test_old_pressure_monotone(self):
+        c=law.DispersionChange(pair());old,_=c.terms(300.,[.4,.6]);lg=np.array([-.3,.5])
+        self.assertGreater(run.r14.pressure(lg+old,.4,[80.,120.]),run.r14.pressure(lg,.4,[80.,120.]))
+
+    def test_stencil_strip(self):
+        c=law.DispersionChange(pair());T=300.;h=1e-4
+        for x in (0.,.00002,.0001,.9999,.99998,1.):
+            lo=max(0.,x-h);hi=min(1.,x+h)
+            def f(v):a,b=c.energies([v,1-v]);return (b-a)/(law.R_KCAL*T)
+            slope=(f(hi)-f(lo))/(hi-lo);v=f(x)
+            np.testing.assert_allclose(c.delta(T,[x,1-x],h,False),[v+(1-x)*slope,v-x*slope],atol=1e-12)
+
+    def test_invalid_inputs_fail(self):
+        for vals in ((0.,10.),(-1.,10.),(np.nan,10.),(np.inf,10.),(1.,)):
+            with self.assertRaises(ValueError):pair(c6=vals)
+        c=law.DispersionChange(pair())
+        for T,x in ((0,[.5,.5]),(np.nan,[.5,.5]),(300,[-.1,1.1]),(300,[.3,.6])):
+            with self.assertRaises(ValueError):c.terms(T,x)
+
+    def test_no_factor_two_error_in_c6_sum(self):
+        atomic=np.array([[1.,2.],[2.,4.]])
+        mol=atomic.sum();two_copies=sum(atomic[i,j] for i in range(2) for j in range(2))
+        self.assertEqual(mol,two_copies);self.assertNotEqual(mol,np.triu(atomic,1).sum())
+
+    def test_actual_model_equal_size(self):
+        with actual_model((80.,80.)) as (base,fl,p):
+            m=law.PairedLondon(base,pair((80.,80.)))
+            for x in (0.,.00002,.4,.99998,1.):
+                old,new=m.paired(330.,[x,1-x]);np.testing.assert_allclose(old,new,atol=2e-11,rtol=0)
+
+    def test_actual_model_preserves_residual_and_derivative(self):
+        with actual_model() as (base,fl,p):
+            m=law.PairedLondon(base,pair());T=325.;x=.37;h=2e-4
+            def g(t):
+                mix=cs.Mixture(['A','B'],p.with_(A_ES=base._c(t),disp_mode='none',use_dsp=False),fluids=list(fl.values()))
+                return float(np.dot([t,1-t],mix.lngamma(T,[t,1-t])))+m.change.energies([t,1-t])[1]/(law.R_KCAL*T)
+            gp=(g(x-2*h)-8*g(x-h)+8*g(x+h)-g(x+2*h))/(12*h)
+            np.testing.assert_allclose(m.lngamma(T,[x,1-x]),[g(x)+(1-x)*gp,g(x)-x*gp],atol=3e-6,rtol=0)
+
+    def test_actual_endpoints_and_strip(self):
+        with actual_model() as (base,fl,p):
+            m=law.PairedLondon(base,pair());T=310.
+            for flag,x in itertools.product(('0','1'),(0.,.00003,.99997,1.)):
+                with patch.dict(os.environ,{'ZC_R6_ENDPOINT':flag}):
+                    if x in (0.,1.) and flag=='1':
+                        pure=cs.Mixture(['A','B'],p.with_(A_ES=base._c(x),disp_mode='none'),fluids=list(fl.values()))
+                        expected=pure.lngamma(T,[x,1-x])+m.change.terms(T,[x,1-x])[1]
+                    else:
+                        def g(t):
+                            mix=cs.Mixture(['A','B'],p.with_(A_ES=base._c(t),disp_mode='none'),fluids=list(fl.values()))
+                            return np.dot([t,1-t],mix.lngamma(T,[t,1-t]))+m.change.energies([t,1-t])[1]/(law.R_KCAL*T)
+                        lo=max(x-base.H,0);hi=min(x+base.H,1);dg=(g(hi)-g(lo))/(hi-lo)
+                        expected=[g(x)+(1-x)*dg,g(x)-x*dg]
+                    np.testing.assert_allclose(m.lngamma(T,[x,1-x]),expected,atol=2e-8,rtol=0)
+
+    def test_one_baseline_call_for_two_arms(self):
+        with actual_model() as (base,fl,p):
+            m=law.PairedLondon(base,pair())
+            with patch.object(base,'lngamma',wraps=base.lngamma) as call:m.paired(300.,[.4,.6]);self.assertEqual(call.call_count,1)
+
+
+class Accounting(unittest.TestCase):
+    def test_grid_union_is_exact(self):
+        union=st.grid_union()
+        for g in st.grids():np.testing.assert_array_equal(union[np.searchsorted(union,g)],g)
+        self.assertLess(len(union),sum(map(len,st.grids())))
+
+    def test_convex_and_nonconvex(self):
+        x=st.grid_union();ideal=np.zeros((len(x),2))
+        self.assertFalse(st.detection(ideal)['detected'])
+        regular=np.c_[4*(1-x)**2,4*x*x]
+        self.assertTrue(st.detection(regular)['detected'])
+
+    def test_disagreement_is_inconclusive(self):
+        x=st.grid_union()
+        with patch.object(st,'hull_gap',side_effect=[(False,0.),(True,1e-5)]):
+            self.assertIsNone(st.detection(np.zeros((len(x),2)))['detected'])
+
+    def test_error_sign_and_system_weighting(self):
+        a=st.paired_summary([100.,100.,100.],[[90.,110.],[80.,90.],[120.,110.]],['a','a','b'],'s',True)
+        self.assertAlmostEqual(a['baseline'],50/3);self.assertAlmostEqual(a['candidate'],10.)
+        self.assertEqual(a['improved'],2);self.assertEqual(a['worsened'],0)
+        self.assertAlmostEqual(a['equal_system'][0],17.5)
+
+    def test_bootstrap_repeats_without_new_rng_state(self):
+        args=([0.,1.],[[2.,1.],[3.,2.]],['a','b'],'idac')
+        self.assertEqual(st.paired_summary(*args),st.paired_summary(*args))
+
+    def test_lle_guard_counts(self):
+        p=[('p',True,True),('p',False,True),('q',False,False)]
+        n=[('n',True,False),('m',False,False)]
+        a=st.lle_summary(p,n);self.assertEqual(a['recall'],[0.,.5]);self.assertEqual(a['false_positive_rate'],[.5,0.])
+
+    def test_uncertain_is_not_false(self):
+        with self.assertRaises(ValueError):st.lle_summary([('p',True,None)],[('n',False,False)])
+
+    def test_no_finite_subset(self):
+        with self.assertRaises(ValueError):st.paired_summary([1.],[[1.,np.nan]],['a'],'idac')
+
+    def test_no_worsening_gates(self):
+        a={'change':-1.,'delta_one_sided_upper95':-.5}
+        s=dict(vle=a,idac=dict(a),he=dict(a),lle=dict(recall=[.8,.8],false_positive_rate=[.1,.1],
+            balanced_accuracy=[.85,.85],recall_change_lower95=0.,false_positive_change_upper95=0.,
+            balanced_accuracy_change_lower95=0.))
+        self.assertTrue(st.gates(s)['passed']);s['he']['change']=.01;self.assertFalse(st.gates(s)['passed'])
+
+    def test_round15_bias_contrast_is_not_shapley(self):
+        self.assertAlmostEqual(-2.79-1.44,-4.23)
+        self.assertGreater(abs((-2.79-1.44)-(-4.47)),.02)
+
+
+class InputTests(unittest.TestCase):
+    def test_profile_units_and_validation(self):
+        with tempfile.TemporaryDirectory() as td:
+            p=Path(td)/'f.sigma';profile(p,83.);self.assertEqual(run.read_profile(p),83.)
+            text=p.read_text().replace('83.0','-83.0');p.write_text(text)
+            with self.assertRaises(ValueError):run.read_profile(p)
+
+    def test_csv_scope_is_input_only(self):
+        with tempfile.TemporaryDirectory() as td:
+            p=Path(td)/'idac.csv';p.write_text('solute,solvent,T,ln_gamma_inf,split,has_sigma\nA,B,300,1,test_one,True\nC,B,300,2,test_both,True\nA,B,300,3,train,True\n')
+            rows,c=run.guard_rows(p,'idac',lambda k:'descriptor' if k=='C' else None)
+            self.assertEqual(len(rows),1);self.assertEqual(c['original_rows'],3);self.assertEqual(len(c['exclusions']),2)
+
+    def test_bad_original_response_is_not_dropped(self):
+        with tempfile.TemporaryDirectory() as td:
+            p=Path(td)/'idac.csv';p.write_text('solute,solvent,T,ln_gamma_inf,split\nA,B,300,nan,test_one\n')
+            with self.assertRaises(ValueError):run.guard_rows(p,'idac',lambda k:None)
+
+    def test_negative_identity_count(self):
+        with tempfile.TemporaryDirectory() as td:
+            p=Path(td)/'n.csv';p.write_text('c1,c2,T,split\nA,B,300,test_one\n')
+            with self.assertRaises(ValueError):run.guard_rows(p,'negative',lambda k:None)
+
+    def test_duplicate_descriptor_identity(self):
+        with tempfile.TemporaryDirectory() as td:
+            root=Path(td);p=root/'results/qc';p.mkdir(parents=True)
+            (p/'dispersion.csv').write_text('inchikey,C6_au,alpha_au\nA,100,20\nA,200,30\n')
+            with patch.object(run,'ROOT',root):
+                with self.assertRaises(ValueError):run.table_inputs()
+
+    def test_queries_have_declared_derivative_cost(self):
+        t=dict(kind='he',members=[dict(row_id='he:0',T=300.,x1=.3)])
+        q=run.queries(t);self.assertEqual([v['T'] for v in q],[299.5,300.5])
+
+    def test_private_output_rejects_checkout(self):
+        with self.assertRaises(ValueError):run.d.private(ROOT/'data/private')
+
+
+def fixture():
+    keys=['A','B'];p=pair();change=law.DispersionChange(p)
+    vle=[dict(row_id='42',keys=keys,T=300.,x1=.4,truth=100.,P=100.,psat=[100.,100.],system='A|B',reference_P=95.,expected_P=0.)]
+    # A deterministic physically separable fake source, not a molecular model.
+    def model(T,x):return change.terms(T,x)[0]+np.array([.1*x[1]**2,.1*x[0]**2])
+    vle[0]['expected_P']=run.r14.pressure(model(300.,np.array([.4,.6])),.4,[100.,100.])
+    guards={
+      'idac':[dict(row_id='idac:0',keys=keys,T=300.,x1=0.,truth=.5,system='A|B')],
+      'he':[dict(row_id='he:0',keys=keys,T=300.,x1=.4,truth=100.,system='A|B')],
+      'positive':[dict(row_id='positive:0',keys=keys,T=300.,system='A|B')],
+      'negative':[dict(row_id='negative:0',keys=keys,T=320.,system='A|B')]}
+    tasks=run.tasks_for(vle,guards)
+    m=dict(tasks=tasks,pairs={'A|B':dict(c6=list(p.c6),alpha=list(p.alpha),volumes=list(p.volumes))},
+           inputs={},worker_inputs={},profiles={},baseline_requests=sum(len(t['queries']) for t in tasks))
+    raw={t['id']:np.array([model(q['T'],np.array([q['x1'],1-q['x1']])) for q in t['queries']]) for t in tasks}
+    return m,raw
+
+
+class DriverTests(unittest.TestCase):
+    def driver(self,td,bad_anchor=False,missing=False,timeout=False):
+        m,raw=fixture();root=Path(td);p=root/'plan.json';run.d.write(p,m);out=root/'output';used=[]
+        def launch(cmd,log,seconds,env):
+            jid=cmd[cmd.index('--job')+1];t=next(t for t in m['tasks'] if t['id']==jid)
+            folder=Path(cmd[cmd.index('--out')+1]);folder.mkdir();used.append(t['kind']);values=[]
+            for j,q in enumerate(t['queries']):
+                run.d.write(folder/f'attempt-{j:05d}.json',dict(query_id=q['query_id'],attempted=True))
+                value=(raw[jid][j]+(.1 if bad_anchor and t['kind']=='vle' else 0)).tolist()
+                if missing and t['kind']=='he' and j==0:value=None
+                values.append(dict(query_id=q['query_id'],lngamma=value,error=None))
+                if timeout and t['kind']=='he':return dict(state='timeout',returncode=-9)
+            run.d.write(folder/'result.json',dict(job=jid,plan_sha256=run.d.sha(p),values=values))
+            return dict(state='returned',returncode=0)
+        a=argparse.Namespace(plan=str(p),plan_commit='f'*40,out=str(out))
+        with patch.object(run,'load',return_value=(p,m)),patch.object(run.r14,'launch',side_effect=launch):
+            rc=run.run(a)
+            self.assertEqual(run.check(argparse.Namespace(plan=str(p),plan_commit='f'*40,run=str(out))),rc)
+        return rc,p,m,out,used
+
+    def test_complete_mocked_run_and_check(self):
+        with tempfile.TemporaryDirectory() as td:
+            rc,p,m,out,used=self.driver(td);self.assertEqual(rc,0);self.assertTrue(run.d.read(out/'summary.json')['status']['complete'])
+            self.assertEqual(run.d.read(out/'summary.json')['baseline_requests'],m['baseline_requests'])
+
+    def test_anchor_failure_blocks_guard_calls(self):
+        with tempfile.TemporaryDirectory() as td:
+            rc,p,m,out,used=self.driver(td,bad_anchor=True);self.assertEqual(rc,2);self.assertEqual(used,['vle'])
+            self.assertIsNone(run.d.read(out/'public-errors.json')['scores'])
+
+    def test_one_failed_value_blocks_acceptance(self):
+        with tempfile.TemporaryDirectory() as td:
+            rc,p,m,out,used=self.driver(td,missing=True);self.assertEqual(rc,2)
+            self.assertEqual(len(used),5);self.assertIsNone(run.d.read(out/'public-errors.json')['acceptance'])
+
+    def test_timeout_keeps_attempt_receipts(self):
+        with tempfile.TemporaryDirectory() as td:
+            rc,p,m,out,used=self.driver(td,timeout=True);self.assertEqual(rc,2)
+            self.assertEqual(run.d.read(out/'summary.json')['status']['query_coverage']['he']['finite'],0)
+
+    def test_tampered_output_refused(self):
+        with tempfile.TemporaryDirectory() as td:
+            rc,p,m,out,used=self.driver(td);t=m['tasks'][0];f=out/t['id']/'result.json';v=run.d.read(f)
+            v['values'][0]['lngamma'][0]+=.1;f.write_text(json.dumps(v))
+            with patch.object(run,'load',return_value=(p,m)):
+                with self.assertRaises(ValueError):run.check(argparse.Namespace(plan=str(p),plan_commit='f'*40,run=str(out)))
+
+    def test_second_claim_refused(self):
+        with tempfile.TemporaryDirectory() as td:
+            rc,p,m,out,used=self.driver(td)
+            with patch.object(run,'load',return_value=(p,m)):
+                with self.assertRaises(FileExistsError):run.run(argparse.Namespace(plan=str(p),plan_commit='f'*40,out=str(Path(td)/'another')))
+
+    def test_partial_finite_result_is_not_scored(self):
+        m,raw=fixture();first=next(t for t in m['tasks'] if t['kind']=='idac');raw[first['id']][0,0]=np.nan
+        q=run.analyze(m,raw);self.assertFalse(q['status']['complete']);self.assertIsNone(q['scores'])
+
+    def test_grid_disagreement_blocks_complete_tradeoff(self):
+        m,raw=fixture()
+        with patch.object(run.stats,'detection',return_value=dict(detected=None,grid_agreement=False,gaps=[0.,1.])):
+            q=run.analyze(m,raw);self.assertFalse(q['status']['complete']);self.assertTrue(q['status']['unresolved_grid_jobs'])
+
+    def test_declared_budget_no_second_candidate_query(self):
+        m,raw=fixture();self.assertEqual(m['baseline_requests'],1+1+2+2*len(st.grid_union()))
+        self.assertEqual(len(st.grids()),2)
+
+
+
+class ReproductionTests(unittest.TestCase):
+    def test_registration_binds_baseline_and_helpers(self):
+        with tempfile.TemporaryDirectory() as td:
+            root=Path(td);frozen={};reg='e'*40
+            files=list(run.FILES)+['src/zcosmo/example.py','results/qc/dispersion.csv',
+                'results/qc/dielectric.csv','results/z_params/Z0.json']
+            for rel in files:
+                p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(rel+'\n')
+                frozen[rel]=p.read_bytes()
+            def git(c,rel):
+                if rel=='PREREGISTRATION.md':return (run.MARKER+' '+law.RECIPE).encode()
+                return frozen[rel]
+            with patch.object(run,'ROOT',root),patch.object(run.r15,'ancestor'),patch.object(run.r15,'git_bytes',side_effect=git):
+                self.assertEqual(run.registration(reg),reg)
+                (root/files[0]).write_text('changed helper')
+                with self.assertRaises(ValueError):run.registration(reg)
+                (root/files[0]).write_bytes(frozen[files[0]])
+                (root/'src/zcosmo/example.py').write_text('changed baseline')
+                with self.assertRaises(ValueError):run.registration(reg)
+
+    def test_source_recipe_cannot_have_weight_changed(self):
+        with actual_model() as (b,f,p):
+            b.z0=p.with_(w_dsp=.5)
+            with self.assertRaises(ValueError):law.PairedLondon(b,pair())
+
+    def test_changed_volume_is_not_silent(self):
+        with actual_model() as (b,f,p):
+            with self.assertRaises(ValueError):law.PairedLondon(b,pair((44.,130.)))
+
+    def test_statistical_overflow_withholds_acceptance(self):
+        m,raw=fixture()
+        with patch.object(run.stats,'paired_summary',side_effect=FloatingPointError):
+            q=run.analyze(m,raw)
+        self.assertFalse(q['status']['complete']);self.assertIsNone(q['acceptance'])
+        self.assertEqual(q['status']['analysis_error'],'FloatingPointError')
+
+    def test_missing_he_sign_class_withholds_acceptance(self):
+        m,raw=fixture()
+        for t in m['tasks']:
+            if t['kind']=='he':t['members'][0]['truth']=0.
+        q=run.analyze(m,raw);self.assertFalse(q['status']['complete']);self.assertIsNone(q['scores'])
+
+    def test_scope_and_input_coverage_do_not_hide_failure(self):
+        with tempfile.TemporaryDirectory() as td:
+            p=Path(td)/'idac.csv'
+            p.write_text('solute,solvent,T,ln_gamma_inf,split,has_sigma\nA,B,300,2,test_one,True\nA,C,300,3,test_one,True\nA,B,299,2,test_one,False\nA,B,460,2,test_one,True\n')
+            rows,c=run.guard_rows(p,'idac',lambda k:'missing' if k=='C' else None)
+            self.assertEqual(len(rows),1);self.assertEqual(c['original_rows'],4)
+            self.assertEqual(len(c['exclusions']),3)
+
+    def test_unknown_split_refused(self):
+        with tempfile.TemporaryDirectory() as td:
+            p=Path(td)/'idac.csv';p.write_text('solute,solvent,T,ln_gamma_inf,split\nA,B,300,2,new_holdout\n')
+            with self.assertRaises(ValueError):run.guard_rows(p,'idac',lambda k:None)
+
+    def test_p54_bias_quantities_are_distinct(self):
+        # Public rounded numbers, not a candidate or experimental scoring run.
+        bias=np.array([1.44,-2.79,6.56,1.53,-.35,-4.34,4.66,-.02])
+        oat=bias[1]-bias[0]
+        shap=sum((math.factorial(len(S))*math.factorial(2-len(S))/6)*
+            (bias[sum(S)+1]-bias[sum(S)]) for S in ((),(2,),(4,),(2,4)))
+        self.assertAlmostEqual(oat,-4.23);self.assertAlmostEqual(shap,-4.473333333333333)
+        self.assertGreater(abs(oat-shap),.2)
+
+    def test_worker_calls_only_unchanged_baseline(self):
+        with tempfile.TemporaryDirectory() as td:
+            root=Path(td);out=root/'run/job-00000';prof=root/'p.sigma';profile(prof)
+            q=dict(query_id='idac:0:0',T=300.,x1=0.)
+            task=dict(id='job-00000',keys=['A','B'],queries=[q])
+            m=dict(tasks=[task],profiles={'A':str(prof),'B':str(prof)},
+                   inputs=run.d.fingerprint([prof]),worker_inputs={})
+            p=root/'plan.json';run.d.write(p,m)
+            run.d.write(root/'execution_claim.json',dict(plan_sha256=run.d.sha(p),output=str(out.parent)))
+            calls=[]
+            def lg(T,x):
+                calls.append((T,x.tolist(),os.environ.get('ZC_R6_ENDPOINT')))
+                self.assertTrue((out/'attempt-00000.json').is_file())
+                self.assertNotIn('ZC_UNREGISTERED',os.environ)
+                return np.array([.3,0.])
+            model=types.SimpleNamespace(lngamma=lg)
+            a=argparse.Namespace(plan=str(p),plan_commit='e'*40,job=task['id'],out=str(out))
+            with patch.object(run,'load',return_value=(p,m)),patch.object(run,'native_baseline',return_value=model),\
+                 patch.dict(os.environ,{'ZC_UNREGISTERED':'1'}):
+                run.worker(a)
+            self.assertEqual(len(calls),1);self.assertEqual(calls[0][2],'1')
+            self.assertEqual(run.d.read(out/'result.json')['values'][0]['lngamma'],[.3,0.])
+            self.assertTrue((out/'overlay/A.sigma').is_symlink())
+            with patch.object(run,'load',return_value=(p,m)),patch.object(run,'native_baseline',return_value=model):
+                with self.assertRaises(FileExistsError):run.worker(a)
+
+    def test_worker_nonfinite_retains_requested_identity(self):
+        with tempfile.TemporaryDirectory() as td:
+            root=Path(td);out=root/'run/job-00000';prof=root/'p.sigma';profile(prof)
+            task=dict(id='job-00000',keys=['A','B'],queries=[dict(query_id='x',T=300.,x1=.4)])
+            m=dict(tasks=[task],profiles={'A':str(prof),'B':str(prof)},inputs=run.d.fingerprint([prof]),worker_inputs={})
+            p=root/'plan.json';run.d.write(p,m);run.d.write(root/'execution_claim.json',dict(plan_sha256=run.d.sha(p),output=str(out.parent)))
+            with patch.object(run,'load',return_value=(p,m)),patch.object(run,'native_baseline',
+                return_value=types.SimpleNamespace(lngamma=lambda T,x:np.array([np.nan,0.]))),patch.dict(os.environ,{}):
+                run.worker(argparse.Namespace(plan=str(p),plan_commit='e'*40,job=task['id'],out=str(out)))
+            z=run.d.read(out/'result.json')['values'][0]
+            self.assertEqual(z['query_id'],'x');self.assertIsNone(z['lngamma']);self.assertIsNotNone(z['error'])
+
+    def freeze_fixture(self,td,budget=180000,changed_guard=False):
+        root=Path(td)/'checkout';root.mkdir();outside=Path(td)/'private';outside.mkdir()
+        for rel in (*run.FILES,'src/zcosmo/dummy.py','scripts/r14_dielectric.py','scripts/r14_oracle.py',
+                    'scripts/r15_factorial.py','scripts/r15_math.py'):
+            p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('# synthetic\n')
+        qc=root/'results/qc';qc.mkdir(parents=True)
+        (qc/'dispersion.csv').write_text('inchikey,C6_au,alpha_au\nA,400,30\nB,3600,100\n')
+        (qc/'dielectric.csv').write_text('inchikey,eps\nA,10\nB,20\n')
+        (root/'results/z_params').mkdir();(root/'results/z_params/Z0.json').write_text('{}')
+        ud=outside/'ud';ud.mkdir();profile(ud/'A.sigma',45.);profile(ud/'B.sigma',130.)
+        inp=outside/'inputs';inp.mkdir()
+        (inp/'idac.csv').write_text('solute,solvent,T,ln_gamma_inf,split\nA,B,300,1,test_one\n')
+        (inp/'he.csv').write_text('c1,c2,T,x1,HE_J,split\nA,B,300,.3,100,test_one\n')
+        (inp/'positive.csv').write_text('c1,c2,T,x1,split\nA,B,300,.1,test_one\n')
+        (inp/'negative.csv').write_text('c1,c2,T,split\nA,B,300,test_one\n'+'A,B,300,train\n'*335)
+        orig={'data/benchmark/'+n:(inp/(n if n!='lle.csv' else 'positive.csv')).read_bytes() for n in ('idac.csv','he.csv','lle.csv')}
+        if changed_guard:(inp/'idac.csv').write_text((inp/'idac.csv').read_text().replace(',1,test_one',',2,test_one'))
+        oldp=outside/'prior/plan.json';run.d.write(oldp,{'mock':True})
+        run.d.write(oldp.parent/'execution_claim.json',{'mock':True})
+        prev=outside/'prior-run';prev.mkdir();run.d.write(prev/'summary.json',{});run.d.write(prev/'public-errors.json',{})
+        # Only the source checker is mocked. The new 963-row freeze, hashes,
+        # job allocation and audit output execute through their real functions.
+        rows=[dict(row_id=str(i),c1='A',c2='B',T=300.,x1=.4,P=100.,psat=[100.,100.],system='mock-system-'+str(i%100)) for i in range(963)]
+        oldm=dict(rows=rows,profiles={'A':str(ud/'A.sigma'),'B':str(ud/'B.sigma')},inputs={},
+                  protected_counts={'profiles_v2':630,'s1_stalled':1,'s2_stalled':5})
+        a=argparse.Namespace(registration='e'*40,r15_plan=str(oldp),r15_plan_commit='f'*40,
+            r15_run=str(prev),out=str(outside/'plan'),ud_profiles=str(ud),**{k:str(inp/(k+'.csv')) for k in ('idac','he','positive','negative')})
+        with patch.object(run,'ROOT',root),patch.object(run.d,'mac'),patch.object(run,'registration',return_value='e'*40),\
+             patch.object(run.r15,'check',return_value=0),patch.object(run.r15,'load',return_value=(oldp,oldm)),\
+             patch.object(run.r15,'arrays',return_value=(np.full((963,8),100.),7704,{})),\
+             patch.object(run.r15,'anchor',return_value={'passed':True}),patch.object(run.r15,'git_bytes',side_effect=lambda c,p:orig[p]),\
+             patch.dict(run.DESIGN,{'max_baseline_requests':budget}):
+            run.freeze(a)
+        return Path(a.out)
+
+    def test_real_freeze_logic_with_mock_P54_archive(self):
+        with tempfile.TemporaryDirectory() as td:
+            p=self.freeze_fixture(td);m=run.d.read(p/'plan.json')
+            self.assertEqual(m['baseline_requests'],963+1+2+2*len(st.grid_union()))
+            self.assertEqual(len(m['tasks'][0]['members']),963)
+            self.assertFalse(m['exposure']['may_claim_unexposed'])
+            self.assertEqual(run.d.read(p/'audit-private.json')['activity_calls'],0)
+            self.assertEqual((p/'PLAN_SHA256.txt').read_text().strip(),run.d.sha(p/'plan.json'))
+            run.d.check_inputs(m['inputs'])
+
+    def test_full_guard_budget_never_downsamples(self):
+        with tempfile.TemporaryDirectory() as td:
+            with self.assertRaises(ValueError):self.freeze_fixture(td,budget=964)
+            self.assertFalse((Path(td)/'private/plan').exists())
+
+    def test_changed_benchmark_refused_before_new_plan(self):
+        with tempfile.TemporaryDirectory() as td:
+            with self.assertRaises(ValueError):self.freeze_fixture(td,changed_guard=True)
+            self.assertFalse((Path(td)/'private/plan').exists())
+
+
+if __name__=='__main__':unittest.main(verbosity=2)
```
<!-- END PATCH T16 -->

<!-- BEGIN PATCH P59 -->
```diff
diff --git a/manuscript/draft.md b/manuscript/draft.md
--- a/manuscript/draft.md
+++ b/manuscript/draft.md
@@ -32,8 +32,11 @@
 important sensitivity. Composition-dependent screening in Z0x reduces the historical VLE AAD to 14.2%.
 A later retrospective diagnostic on a separate 963-row subset changes AAD from 13.78% to 13.07% when
 experimental pure-liquid permittivities replace the stored estimates, versus 10.44% for COSMO-SAC 2010.
-This small bulk-permittivity effect leaves the local contact approximation as an unresolved hypothesis,
-not an established universal cause or an accepted new coefficient. HANNA, where its
+A registered same-row factorial subsequently assigns 2.24 percentage points, about 67% of the
+Z0x-to-2010 AAD gap, to replacing the London term with the reference's absence of explicit dispersion.
+The electrostatic closure contributes 26% and the hydrogen-bond constants 7% under this allocation.
+These exposed counterfactuals identify an implemented approximation to examine, not a transferable
+physical error fraction or permission to delete a term because its removal improves the benchmark. HANNA, where its
 training data reach, is far more accurate than every physics-based model, but it does not detect demixing
 more reliably than Z0 on held-out molecules.
 
@@ -104,6 +107,13 @@
 contact energies e_ij = -C6_ij / d_ij^6 from D4 molecular C6 and polarizabilities (London combining rule),
 d_i the diameter of a sphere of COSMO cavity volume, entering as ln gamma_1 = (z/2) w x_2^2 / RT with
 w = 2 e_12 - e_11 - e_22.
+
+The D4 descriptors do not determine this liquid-contact model uniquely. The molecular one-center
+far-field approximation, contact diameters derived from cavity volumes, coordination z=10 and random
+mole-fraction contact statistics are additional approximations. The molecular C6 is a sum over all
+atom pairs between two molecular copies; it is not an intramolecular pair-energy sum requiring a
+factor of one half. The retained D4/MMFF inputs have their own model provenance. No adjustment to
+these inputs or dispersion weight was made to fit the present ThermoML comparison.
 
 Refinements registered after the first results, before their own predictions:
 Z0e scales c_ES by the COSMO dielectric factor f = (eps - 1)/(eps + 1/2) with eps from Onsager's equation
@@ -328,7 +338,52 @@
 The oracle is an experimental-input, retrospective diagnostic, not a fit-free variant, a rigorous
 headroom bound or a newly held-out score. The old main7 14.15/8.62 comparison uses a different subset.
 R14 does not authorize a portfolio dielectric simulation campaign or identify a transferable local
-contact coefficient. See `docs/astra/round14/RESULTS.md`. No R15 factorial result is asserted here.
+contact coefficient. See `docs/astra/round14/RESULTS.md`.
+
+### 3.11 Same-row factorial identifies the London closure as the leading VLE discrepancy
+
+R15/P54 reused exactly P52's 963 exposed observations in 100 binary systems, with the original UD
+profiles and frozen pure-component saturation pressures. Eight distinct E/H/D corners were evaluated
+once, where E replaces the complete Z0x electrostatic closure by the 2010 temperature-dependent rule,
+H replaces the hydrogen-bond constants, and D replaces London by no explicit dispersion, as in 2010.
+The sign mask, stored profiles and effective segment area were shared. Profile convention and
+area therefore contribute zero to this endpoint difference, without being certified physically exact.
+
+| E H D corner | AAD P % | bias % | equal-system AAD % |
+|---|---:|---:|---:|
+| 000, stored-epsilon Z0x | 13.78 | +1.44 | 13.90 |
+| 100 | 12.63 | -0.35 | 12.73 |
+| 010 | 13.97 | +6.56 | 14.05 |
+| 001, no explicit dispersion | 11.76 | -2.79 | 12.00 |
+| 110 | 12.86 | +4.66 | 12.94 |
+| 101 | 11.04 | -4.34 | 11.26 |
+| 011 | 11.00 | +1.53 | 11.24 |
+| 111, COSMO-SAC 2010 | 10.44 | -0.02 | 10.65 |
+
+The game value was negative absolute percentage-pressure error. Shapley error reductions were
+2.24 percentage points for dispersion (67%), 0.88 for the electrostatic closure (26%) and 0.23 for
+hydrogen-bond constants (7%). The gap is 3.35 percentage points in the unrounded output. The H/D
+interaction was +0.95 and the E/D interaction -0.43 percentage points in the baseline-anchored
+inclusion/exclusion decomposition. Hydrogen-bond replacement slightly worsened error on its own;
+its net Shapley benefit arose through interactions. These quantities allocate error under the
+specified interventions and loss function, not intermolecular binding energy or universal causal shares.
+
+The one-at-a-time London removal reduces AAD by 2.02 percentage points. Its bias change, computed
+from the displayed corner biases, is -2.79 - 1.44 = -4.23 percentage points. The separate -4.47 value
+is the Shapley-allocated dispersion bias contribution, not this one-at-a-time difference. Independently
+rounded AADs explain small arithmetic differences such as 13.78 - 10.44 versus the reported 3.35;
+they do not explain conflating these two bias statistics.
+
+All 7,704 requests were finite. The 1,926 anchor requests reproduced their saved P52 pressures exactly
+before intermediate corners ran, and the Shapley efficiency residual was at most 3e-14 percentage
+points. The run took 722 seconds on the Mac, without quantum calculations or a retry. These are
+execution and accounting checks, not a new held-out accuracy certificate. See
+`docs/astra/round15/RESULTS.md` for the source record and its test-environment qualification.
+
+P54 changes the priority inferred from the earlier conductor-limit Z0 ablation: dispersion is the
+leading contribution to this Z0x-to-2010 comparison. R14's approximately 21% epsilon-oracle recovery
+and P54's ES share overlap and must not be added. Neither the best fitted corner nor removal of
+London is adopted. Every historical model table and the 630+6 open profiles remain unchanged.
 
 ## 4. Discussion
 
@@ -337,14 +392,23 @@
 for VLE on the displayed main7 and temporal subsets. This supports a quantitative account of the
 tradeoff, without claiming that all empiricism has been removed or that the model is generally competitive.
 
-The electrostatic contact prescription is a plausible research target, but bulk permittivity and local
-segment response are different quantities. In the implemented mapping, increasing epsilon raises
-f=(epsilon-1)/(epsilon+0.5) toward the conductor limit. The experimental-epsilon oracle yields only a
-small improvement on its particular exposed sample. Earlier one-term ablations and that oracle do not
-identify a unique universal correction, and their apparent gains cannot be added as independent causes.
-A complete same-row factorial can quantify the contributions of the implemented ES, HB and dispersion
-replacements under a stated allocation rule, including their interactions. Its fitted corners remain
-diagnostics, never candidates selected by whichever ThermoML error is smallest.
+The strongest later explanatory result is P54's dispersion attribution on the fixed P52 observations.
+It is more directly relevant to the remaining Z0x discrepancy than the original conductor-limit Z0
+ablation. Bulk permittivity and local contact response remain different quantities, but the small R14
+oracle effect does not justify treating dielectric error as the dominant unresolved cause. The London
+closure should be described as an approximate conversion of electronic descriptors into an excess
+mixing free energy. P54 identifies that conversion as a leading source of benchmark discrepancy;
+it does not isolate one failed geometric assumption or prove double counting.
+
+For positive C6, polarizabilities and cavity volumes, the implemented London exchange is nonnegative:
+its unlike C6 does not exceed the geometric mean of its self coefficients, and its arithmetic-mean
+contact diameter is at least their geometric mean. Consequently its Margules contribution raises
+both component activities and bubble pressure relative to the same residual without it. That
+restriction can increase or reduce absolute pressure error depending on the row. A change to volume
+contact statistics requires differentiating a complete excess Gibbs energy, not merely replacing
+mole fractions in the existing gamma formula. A physically specified alternative must retain its
+unfavorable outcomes and be evaluated under a new prospective, exposure-qualified protocol.
+The P54 fitted corners remain diagnostics and cannot be selected as models by their lower error.
 
 Deriving a new contact kernel from reaction-field response or independent electronic calculations is
 physically possible after the cavity, contact geometry and reference-energy partition are specified.
@@ -358,7 +422,10 @@
 not validate the site thermodynamics, and an energy/force model does not automatically validate its
 field response or chemical potentials. The numerical association repair changes neither the archived
 scientific failures nor this assessment. The present work is ready for a limitations-aware account of
-its completed evidence; a speculative native campaign need not delay that account.
+its completed evidence, with P54 as the centerpiece of the later VLE explanation. Finalization need
+not await an optional single-recipe dispersion screen, and a failed screen is not grounds to tune
+its weight or conceal the failure. Independent verification of bibliography and reproducibility
+assets remains part of submission preparation.
 
 ## 5. Limitations
 
@@ -416,8 +483,8 @@
 S5 Error maps by chemical family: `results/error_map_idac_*.csv`.
 S6 Open-profile validation and conformer comparison: `results/pyscf_profile_validation.csv`,
    `data/pyscf_sigma/conformer_summary.csv` (asset availability is stated above).
-S7 Later numerical, glycol and dielectric evidence: `docs/astra/round2/RESULTS.md` through
-   `docs/astra/round14/RESULTS.md`, with the registrations and private-plan digests referenced there.
+S7 Later numerical, glycol, dielectric and factorial evidence: `docs/astra/round2/RESULTS.md` through
+   `docs/astra/round15/RESULTS.md`, with the registrations and private-plan digests referenced there.
 
 ## References (to verify against the publisher records before submission)
 
diff --git a/docs/astra/round16/P54_CLARIFICATION.md b/docs/astra/round16/P54_CLARIFICATION.md
new file mode 100644
--- /dev/null
+++ b/docs/astra/round16/P54_CLARIFICATION.md
@@ -0,0 +1,17 @@
+P54 bias clarification, proposed for the round-16 record
+
+The round-15 corner table and factor table report different statistics. From
+corner 000 to corner 001, the displayed pressure bias changes from +1.44% to
+-2.79%, a one-at-a-time change of -4.23 percentage points. The factor table's
+-4.47 percentage points is the Shapley-allocated dispersion contribution to
+bias, averaged over all other ingredient contexts. The rounded corner table
+reproduces that allocation as approximately -4.4733 percentage points.
+
+The R15 prose and R16 prompt should not describe -4.47 as the one-at-a-time
+bias shift. This clarification preserves both original tables and every
+registered result; it does not rerun predictions or revise their denominators.
+The dispersion error-reduction attribution remains 2.24 percentage points
+(67%) and its one-at-a-time AAD reduction remains 2.02 percentage points.
+
+Source: ../round15/RESULTS.md at ca5c7e94627fcdebbf787afb688f8cab10e42a03.
+The updated manuscript distinguishes these quantities explicitly.
```
<!-- END PATCH P59 -->

<!-- BEGIN PATCH REG16 -->
```diff
diff --git a/docs/astra/round16/REGISTRATION_PROPOSED.md b/docs/astra/round16/REGISTRATION_PROPOSED.md
new file mode 100644
--- /dev/null
+++ b/docs/astra/round16/REGISTRATION_PROPOSED.md
@@ -0,0 +1,238 @@
+R16-P57-P58-P59: London audit, one LV1 screen, and P54 reporting
+
+Proposed registration, not an execution or adoption record. Append this text
+in full to PREREGISTRATION.md and commit it with the four R16 scripts before
+freezing a private R16 plan or using a new real-data result. Record the actual
+UTC adoption time. Reference main is ca5c7e94627fcdebbf787afb688f8cab10e42a03.
+
+P57 is E source/algebra reporting and a read-only audit of the original London
+inputs. P58 is exactly one A dispersion approximation, with E algebraic reuse
+of the unchanged Z0x calculation. P59 is E manuscript reporting. None modifies
+the production model registry, any source in src/zcosmo, a stored physical
+parameter, the UD input convention, or the 630 primary plus one selected S1
+and five selected S2 profiles. P55 and all preceding failure records remain.
+P35 and the numerical-gradient campaign remain closed.
+
+The new candidate is named R16-LV1-cohesive-density-SK-volume-regular-solution.
+Only this candidate and the unchanged stored-epsilon Z0x baseline are evaluated.
+The already saved P54 COSMO-SAC 2010 pressures are a comparator, not a new
+candidate. London deletion, a fitted corner, a weight change, another combining
+rule, an alternative damping prescription or a surface-fraction variant is
+not an authorized follow-up when a result is unfavorable.
+
+The scientific choice is explicitly informed by P54's exposed dispersion
+attribution. It is frozen before any LV1 molecular prediction or score. There
+is no claim that the old compound split or temporal collection becomes an
+untouched holdout. The new primary VLE comparison uses the identical 963 P54
+observations in 100 unordered systems. The temporal collection is not rescored.
+The original input-covered test_one/test_both IDAC and HE observations and
+LLE positive observations are guard collections. The saved 336-state negative
+archive supplies its input-covered original test_one/test_both subset. These
+collections are previously inspected, and their exposure is part of the result.
+No custodian-held, unexposed validation source has been certified here.
+
+Physical definition of LV1
+
+Use the existing molecular C6_ii and alpha_i from results/qc/dispersion.csv,
+with exactly their existing identities and values. Use the unchanged historical
+UD cavity volume V_i. All quantities must be finite and positive. No new D4
+call, geometry, charge, molecular response calculation or experimental cohesive
+energy is used. The temperature dependence of these inputs remains fixed.
+
+Convert V_i in A^3 to diameter d_i=2*(3*V_i/(4*pi))^(1/3)/BOHR_A. Define the
+positive self-contact magnitude u_i=C6_ii/d_i^6*HARTREE_KCAL in kcal/mol. Use
+the existing Slater-Kirkwood cross coefficient:
+C6_12=2*C6_11*C6_22/[(alpha_2/alpha_1)*C6_11+(alpha_1/alpha_2)*C6_22].
+Its normalized spectral factor is kappa=C6_12/sqrt(C6_11*C6_22).
+
+Keep z=10 and the dispersion weight exactly one. Define cohesive quantities
+c_i=5*u_i/V_i, c_12=kappa*sqrt(c_1*c_2), and K=c_1+c_2-2*c_12. For mole fractions
+x_i define Vbar=sum(x_i*V_i), phi_i=x_i*V_i/Vbar. The new molar excess dispersion
+free energy is gV=Vbar*phi_1*phi_2*K (kcal/mol). Its exact component contributions
+are ln_gammaV_1=V_1*phi_2^2*K/(R_KCAL*T) and
+ln_gammaV_2=V_2*phi_1^2*K/(R_KCAL*T).
+
+This follows by assuming a random homogeneous cohesive-energy density
+-(phi_1^2*c_1+2*phi_1*phi_2*c_12+phi_2^2*c_2) and subtracting its linear pure
+references. That density and cross normalization are declared approximations,
+not uniquely implied by the molecular C6 descriptors. The original sphere
+self-energy and coordination approximations remain. In particular, the model
+does not solve shape, finite-contact damping, many-body polarization or the
+cohesive-energy scaling of long chains. It is a thermodynamically defined,
+no-new-benchmark-regression test, not a universally first-principles liquid model.
+
+Do not add another combinatorial or Flory-Huggins entropy term. Keep every
+existing residual interaction, epsilon value, composition derivative and
+COSMO combinatorial constant unchanged. No pure vapor pressure is changed.
+For equal cavity volumes LV1 reduces to the existing London Margules term.
+For unequal volumes it need not reduce either component contribution or total
+pressure. Its failure on one property is not grounds to choose a different
+normalization or a favorable chemical subgroup.
+
+Numerical implementation and checks
+
+The baseline London free energy is gL=5*w*x_1*x_2. Both this term and gV are
+independent of the electrostatic coefficient. Query unchanged Z0x once and
+add the derivative of (gV-gL)/(R*T) to obtain LV1. This is exact reuse of the
+stated two models, not physical E-equivalence of LV1 and London. Enable P28
+for both arms. Preserve the base's adjacent finite-difference strip exactly:
+there, difference the scalar correction with the same h=1e-4 stencil. Do not
+silently upgrade that strip or create an exact association endpoint.
+
+Portable tests must pass before a plan is frozen. They verify positivity and
+label symmetry, the old exchange decomposition, identical/equal-volume limits,
+Gibbs-Duhem, derivative consistency, the HE temperature convention and one-call
+reuse. Tests involving the actual unchanged segment solver use synthetic
+profiles. Tests of native, Mac and prior-run adapters are labeled as mocks.
+No source module-cache clearing is permitted in these tests; the known R15
+NumPy import-isolation artifact is not resolved by calling an incomplete log a
+passing suite. Native end-to-end acceptance remains separate from portable tests.
+
+P57 decomposes only the original exchange energy. With
+q=[2*sqrt(d_1*d_2)/(d_1+d_2)]^6, the identity is
+w=(sqrt(u_1)-sqrt(u_2))^2+2*sqrt(u_1*u_2)*(1-kappa)
+  +2*kappa*sqrt(u_1*u_2)*(1-q).
+These terms are nonnegative for positive inputs. The arithmetic implementation
+checks the sum against the original formula to 1e-10*max(1,max(u_i)) kcal/mol.
+They are energy terms, not fractions of experimental error or a second Shapley
+analysis. The descriptor census and every per-pair quantity remain private.
+
+Inputs and prospective plan
+
+Run the original R15 saved-output checker on its unchanged helpers. Require
+the original complete P54 plan and digest commit, its exclusive run claim,
+7,704 requests, every finite corner and both replayed anchors. Preserve all
+963 original observation identities, component orientation, T, x, measured P
+and frozen saturation pressures. Reuse the P54 baseline and 2010 pressures.
+Do not construct a new oracle selection or replace its original pressures with
+values from a newer property package. Carry the P52a protected profile selection
+and the existing source-version bridge forward without broadening it.
+
+For the other properties, require the supplied IDAC, HE and positive-LLE CSV
+bytes to equal reference-main data/benchmark/idac.csv, he.csv and lle.csv,
+respectively. Copies at different private paths are allowed; new exports are
+not. The negative archive must be the saved original 336-state input used by
+the project; freeze its complete bytes and require one eligible state per
+unordered test binary. It is an operator-supplied historical asset, not newly
+reconstructed by negative_series(). Do not substitute a new negative archive.
+
+Eligible guard rows retain their original split, original has_sigma decision
+when present, 250<=T<=450 K, two different keys and valid physical input files.
+Eligibility is decided without running a model or looking at prediction error.
+Record every input-only exclusion, including missing descriptor, epsilon or
+unambiguous historical UD profile. A malformed eligible observation is a
+preparation failure, not a row to remove. No empty property class is accepted.
+The HE sign subset must contain observations with |HE|>20 J/mol. The guard
+selection is common to both arms and is fixed before all new queries.
+
+Freeze hashes of each reused private input, all baseline source files, the new
+helpers and installed package versions. Reject all baseline source/table drift
+from reference main, including a changed P55 implementation. Profile identity
+uses the existing exact-key or unique-connectivity UD rule, not a new chemical
+name match. Each worker resolves both explicit frozen files. No fallback to
+open profiles or to a different directory is allowed after a missing file.
+All original private receipts remain available. Only the new plan digest is
+committed in docs/astra/round16/PLAN_SHA256.txt before any new model call.
+
+Requested evaluation and guard definitions
+
+VLE: all 963 P54 rows, pressure in kPa from the same two saturation pressures.
+Before guard-property queries start, unchanged Z0x must reproduce every saved
+P54 baseline pressure to relative difference strictly below 1e-8. A failed or
+missing anchor blocks the guard phase. No alternate baseline or relaxed
+replay limit is authorized. All comparisons, including the stored 2010 arm,
+use these same 963 observations rather than the historical main7 denominator.
+
+IDAC: all frozen eligible test observations, with exact P28 solute index zero
+at x=(0,1). HE: all frozen eligible test observations, with the existing
+central temperature difference at T-0.5 and T+0.5 K. Use this same numerical
+HE convention in both arms and keep each original x. The held-constant
+volumes/descriptors imply a temperature-independent energetic gV; this does
+not validate a physical volume(T) or epsilon(T) model.
+
+LLE detection: preserve the positive observation identities and the original
+2 K evaluation-temperature rounding. Negative states keep their recorded T.
+For both arms evaluate the dimensionless total mixing free energy on the
+existing log-augmented 81-point interior grid and an independently checked
+161-point interior grid. Their exact union contains 181 compositions; reuse
+identical nodes without rounding nearby distinct values. A detected gap means
+maximum vertical distance above that grid's lower convex hull exceeds 1e-7
+in g/(RT). The grids must agree for each arm and state. Disagreement or a
+nonfinite grid is unresolved, never 'miscible', and blocks complete tradeoff
+acceptance. This is an explicit numerical detection screen, not a global
+stability certificate or an endpoint-composition score. Its baseline is freshly
+evaluated by the identical convention; it does not overwrite historical LLE BA.
+
+Positive system recall uses the original rule that more than half its retained
+observations have a detected gap. Negative false-positive rate uses one state
+per eligible binary. Balanced accuracy is (recall+1-FPR)/2. Keep the two classes'
+denominators separate. No endpoint composition is inferred from a hull segment.
+No LLE numerical result may be dropped from the acceptance denominator.
+
+For VLE, IDAC and HE report observation-weighted AAD/MAE and signed bias;
+also report equal-system averages and improved/worsened row counts. Use 1,000
+paired resamples of unordered binary systems, with the seed fixed in
+r16_stats.SEED. LLE resamples systems separately within its positive and
+negative classes. Report two-sided 95% intervals for error differences and
+use the specified one-sided 95% bounds for the gates below. These are
+exposure-qualified resampling summaries, not recovered untouched-test guarantees.
+
+All gates are required: VLE AAD change is negative and its one-sided upper
+bound is below zero. IDAC and HE MAE changes and their upper bounds are <=0.
+There is no positive allowed-worsening margin. HE sign correctness on |HE|>20
+must not decrease. LLE recall and balanced accuracy must not decrease, with
+lower bounds on their paired changes >=0; false-positive rate must not
+increase, with its change's upper bound <=0. Missing data or an unresolved
+numerical state is an incomplete screen, not a passed no-worsening gate.
+
+Separately, report whether the candidate-to-2010 VLE AAD difference and its
+upper bound are <=0 on the 963 rows. This is the limited 'gap closed on the
+exposed panel' indicator. Passing only VLE is insufficient. Passing every gate
+is success of this frozen exposed development screen, not a universal accuracy
+claim or automatic production adoption. A genuinely independent validation
+and an explicit later adoption decision are still required for that claim.
+
+Cost, execution and stopping
+
+Let NI and NH be the frozen eligible IDAC and HE row counts and NL the number
+of distinct ordered-pair/temperature positive and negative LLE jobs. The new
+baseline-call count is Q=963+NI+2*NH+181*NL. LV1 has no additional segment-solver
+calls. The full frozen design must fit Q<=180000; otherwise preparation stops
+with zero new model calls and no automatic downsampling or budget increase.
+The proportional 722/7704 seconds per P54 query is a planning reference only,
+not a measured R16 throughput. New LLE states may converge differently.
+
+Execute serially on the private asset-bearing Mac, at most four OpenMP threads
+and one BLAS thread. Each worker has 180 seconds within a total 21600-second
+baseline-query/orchestration allocation. A five-second process-group kill
+allowance is administrative, not additional scientific compute. Time closing
+read-only aggregation separately. Budget is zero SCFs, zero gradients, zero
+MD, no paid resource and no cloud dispatch. UD data, dense profiles, per-row
+results, private plans and logs stay outside every Git checkout and are never
+uploaded. Real work cannot run on a fixture or fabricated 'Mac' adapter.
+
+Create one permanent exclusive execution claim. Write each attempt receipt
+before calling the unchanged baseline. Record every job terminal state,
+including blocked, budget-unstarted, failed and timed-out jobs. Independent
+jobs continue within budget after another fails. There is no retry, resumption,
+claim deletion or second scientific output directory. Repeated saved-output
+checks are allowed with no new model calls. A complete but unfavorable run
+is retained and its acceptance Boolean stays false. Failure of a query or
+derived arithmetic withholds complete scores instead of taking a favorable
+finite intersection. A lost data archive is not permission to recompute it.
+
+Only aggregate errors, coverage counts, declared gate outcomes and timings are
+eligible for separate human review before publication. The software publishes
+nothing. P57 dense coefficient decompositions and per-row predictions remain
+private. No candidate coefficient is changed after seeing a result, including
+an IDAC or LLE failure. The original London model and historical records remain.
+
+P59 inserts P54's actual results in the abstract and a dedicated manuscript
+section, and updates the discussion and evidence references. It distinguishes
+the one-at-a-time bias change -4.23 percentage points from the dispersion
+Shapley bias allocation -4.47, without rewriting either historical table.
+All R2-R14 open-profile, gradient, glycol, epsilon and empirical-input
+qualifications remain. P54 is an explanatory centerpiece, not a proof that
+real dispersion is absent. Finalize the paper with this evidence whether LV1
+passes, fails, is operationally incomplete or is never executed. No speculative
+native or new-variant campaign is made a prerequisite for writing up the study.
```
<!-- END PATCH REG16 -->

Delivery validation, completed 2026-10-08

The report's five embedded diffs were extracted into a new directory, independently checked against the verified baseline subset, and applied together to a fresh local Git reconstruction. Every resulting file matched the tested working version byte-for-byte. Whitespace checks and Python compilation passed. The four Bash command blocks and their embedded Python were syntax checked; the freeze/run/check command-line interfaces were exercised with --help only.

The final extracted-source tests passed: R16 58/58 in 8.610 seconds and R14 45/45 in 0.416 seconds, in separate invocations. These are software-test timings, not model benchmarks. The initial validation found a trailing blank line at EOF in the test file; it was removed, and the extraction/application/whitespace checks were rerun successfully. An earlier combined tool invocation timed out after the test logs had completed; the final checks were run again explicitly. No scientific run was attempted or retried.

All 26 lines belonging to existing manuscript Markdown tables remain in their original order. Eight reused current source-file blobs were verified, including the complete manuscript. No src/zcosmo file is changed by these patches. Main was rechecked at ca5c7e94627fcdebbf787afb688f8cab10e42a03 before delivery. The real Mac experiment and its descriptor/guard census remain unexecuted.

Patch SHA256 values, for the newline-terminated extracted files:

`H16.patch`: `f6d039a78ec1a64668949f576ce7300f1d29e569ae7590abcc33f799ac9faa88`

`P57P58.patch`: `91efe5ffb8c14f8c30d95048cbcb8fca424ba9a05a1f641c8670b62a28fe715c`

`T16.patch`: `120bfd6525d94a785286d1ab25ced16a926f1e0724eef9b9bd40e5da526bcdd4`

`P59.patch`: `ba0d9a6646ac3d9731e2d96f22bee6fc149d94785518b0a252e6e0bc8afb0fa0`

`REG16.patch`: `5ef7a529e00dbeba127dc42a5b6d7bcab39da21e90428f5439f876d68f6e9fbe`
