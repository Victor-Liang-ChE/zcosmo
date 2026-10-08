Z-COSMO round 15: attribute the implemented contact-model gap, repair association dispatch, and finish the evidence record

Reference: `Victor-Liang-ChE/zcosmo`, `main = 3cd0a22888b40699d5f4994f5ba2e5cd274703df`. The round-15 prompt, the amended P52 result and the original research rules govern this report. The branch was rechecked before delivery and still points to this commit. The five patches below are prospective. They do not record adoption or a new private-data result. P35 and the numerical-gradient campaign remain closed, and the 630 primary plus six selected S1/S2 open profiles remain unchanged. [S1, S2]

| Rank | ID and class | Target functions/files | Mechanism and acceptance | Expected saving or cost | Effort |
|---:|---|---|---|---|---|
| 1 | P54, A diagnostic with E accounting controls | `scripts/r15_factorial.py`: `archive`, `freeze`, `worker`, `run`, `check`; `r15_math.py`: `make_corner`, `summary` | Complete the contact-ingredient factorial on exactly the original 963 P52 rows. Both fresh endpoint models must replay their archived pressures before intermediate corners run. No fitted corner is a candidate for adoption. | 7,704 requests rather than 30,816 for a naive five-factor cube: 75% fewer requests, or 4× request-level efficiency. Zero QC. | Moderate |
| 2 | P55, A correction relative to defective current outputs; E restoration of the historical software prescription | `src/zcosmo/z0w.py`: `Z0wBinary.lngamma`; targeted tests in H15 | Restore differentiation through the complete subclass `_g`, preserving the old finite-difference convention. No new strengths, endpoint formula or association scoring. | Correctness repair, not a speed-up. Three complete excess-Gibbs evaluations per request restore work the broken dispatch omitted. | Low |
| 3 | P56, E reporting | `manuscript/draft.md` | Update input scope, numerical provenance and R10–R14 evidence without replacing historical numerical tables or asserting a P54 result. | No model calls. Avoids making a speculative native campaign a prerequisite to writing up the completed study. | Low |
| Shared | H15 and REG15 | `r15_math.py`, `r15_selftest.py`, proposed registration | Exact finite-game arithmetic, synthetic numerical regressions, immutable-input checks and a private one-run protocol. | No additional physical experiment. | Low |

The ranking combines the value of answering the remaining question with implementation effort. The reduction from 32 to eight distinct corners is an exact counting result. It is not a fourfold acceleration of the segment solver. There is no defensible numerical probability that a new physical coefficient will close the VLE gap, so none is invented for the ranking.

My recommendation is to run this one bounded explanatory factorial, retain the association software repair after its regression checks, and finalize the paper around the completed evidence. A local-contact research project is physically possible, but the current results do not identify a ready, validated replacement coefficient. The factorial should inform an explanation, not initiate an automatic sequence of fitted variants or native simulations.

P54: what actually differs between the endpoints

The baseline is the P52 stored-epsilon Z0x model. It is not the experimental-epsilon oracle. The other endpoint is the repository's COSMO-SAC 2010 model, `Params(use_dsp=False)`. Both consume the same historical UD profiles. The requested five nominal factors therefore contain only three active differences. The shared ingredients are important to the absolute predictions, but cannot explain an endpoint difference when their values are identical. [S3–S6]

| Requested ingredient | Stored-epsilon Z0x endpoint | COSMO-SAC 2010 endpoint | Registered intervention |
|---|---|---|---|
| Electrostatic contact coefficient | `c0*f(eps_mix(x))`, with the existing composition derivative | `6525.69 + 1.4859e8/T²`, independent of composition | Swap the entire ES closure, including whether `dc/dx` is present. |
| HB constants and cutoff | The original Z0 OH-OH/OH-OT/OT-OT constants, approximately 5712.23/5987.64/5611.40 | 4013.78/3016.43/932.31 | Swap these constants. Keep the common sign mask and stored HB split unchanged. |
| London/dispersion | D4/London term with weight 1 | No explicit dispersion term | Remove London; do not substitute the fitted 2014 dsp term. |
| Effective segment area | 7.25 Å² | 7.25 Å² | Exact dummy player. No new area value is invented. |
| Profile convention | The same P52 UD bytes, NHB/OH/OT channels and sigma grid | Identical | Exact dummy player. No raw-table replay or new profile generation. |

The combinatorial constants `q0=79.53`, `r0=66.69` and `z=10` are also shared. The current interaction matrix contains no separately adjustable HB threshold parameter: the contact mask is `sigma_m*sigma_n < 0`, applied within the existing HB channels. The stored profile split has its own convention. Importing a cutoff from an older COSMO-SAC or another COSMO-RS variant would introduce a new intervention absent from either endpoint. Official parameter documentation independently confirms the listed 2010 coefficients and effective area; the executing repository remains the source of truth for this comparison. [S3–S5, U1]

There is a concrete dispersion trap. In `Mixture.lngamma_disp`, the London branch executes before the `use_dsp` check. Setting `use_dsp=False` on Z0 alone leaves London active. P54 sets the mode to the reference's `dsp` value and disables `use_dsp`, as well as copying its inactive weight. The all-swapped parameter object must equal `Params(use_dsp=False)`. This is a guard against accidentally calling a 2014-dsp hybrid “2010.” [S3]

Likewise, changing only `Z0xBinary._c` would leave `_analytic` computing the derivative of the old composition-dependent coefficient. That would not be the derivative of the intended excess Gibbs energy. The ES=1 branch uses the existing `Mixture` implementation with its composition-independent `A+B/T²`. ES=0 retains the existing Z0x class and analytic chain rule while changing only the declared HB/dispersion parameters. No new derivative implementation is introduced. [S4]

The HB constants are frozen numerical inputs to this factorial. Their original derivation used the theoretical ES coefficient when matching dimer energies. Recomputing them after each ES swap would couple two players and would no longer be the requested fixed-ingredient experiment. The resulting hybrids are deliberately counterfactual. Their attribution is conditional on this definition, not a claim that every corner represents an independently derived physical theory. [S5]

Let `E,H,D` denote the active bits, with zero meaning Z0x and one meaning the 2010 ingredient. Evaluate all eight combinations. The exact five-player game is obtained by assigning the same value to all four choices of the two shared bits. Adding these dummy players does not change any active Shapley value. H15 calculates both versions and verifies that identity, rather than just reporting a three-player calculation as though five independent quantities had been changed.

The observable is pressure error, not a sigma-tail norm or an arbitrary coefficient difference. For row i and corner b, the frozen query gives

\[
 P_i(b)=x_i\exp(\ell_{1,i}(b))P^{\rm sat}_{1,i}
 +(1-x_i)\exp(\ell_{2,i}(b))P^{\rm sat}_{2,i},
 \qquad L_i(b)=100\left|P_i(b)/P_i^{\rm exp}-1\right|.
\]

The two stored pure pressures, units and observation identity come directly from P52. The game value is `v_i(b)=-L_i(b)`. For player j in the five-player game,

\[
 \phi_{j,i}=\sum_{S\subseteq N\setminus\{j\}}
 \frac{|S|!(4-|S|)!}{5!}
 \{v_i(S\cup\{j\})-v_i(S)\}.
\]

Consequently, `sum_j phi_j,i = L_i(000)-L_i(111)`. Positive contributions remove absolute percentage error; negative contributions make it worse under this allocation. Apply the same operation separately to signed percentage error to explain bias. Taking an absolute value of a prediction shift is not an error attribution: moving a pressure from 90 to 110 kPa when the observed value is 100 kPa removes no absolute error.

The public aggregate carries every corner's AAD and bias, improved/worsened counts, row-weighted and equal-system errors, all five factor contributions, and the seven baseline-anchored nonempty inclusion/exclusion interactions of the active cube. One-at-a-time changes are reported alongside the Shapley contributions. The two-factor interaction, for example, is

\[
 I_{EH}=v(110)-v(100)-v(010)+v(000).
\]

The three-factor interaction is defined by the full inclusion/exclusion sum. Interactions plus the singleton effects telescope to the endpoint change. They are not independent physical energy terms. Neither a negative contribution nor a share greater than one is clipped. A recovery share is unavailable when the positive baseline-to-2010 gap is at most `1e-6` percentage points. The arithmetic identities are checked per row to `1e-8` percentage points.

This directly answers “which implemented replacement carries the pressure error?” It does not answer “what fraction of the true liquid physics is electrostatic?” A large ES contribution would localize the benefit of changing this closure in the specified model. Strong ES/HB interactions would argue against interpreting the prefactor independently of the HB recipe. A large dispersion contribution would be evidence to report, even though it is not the leading hypothesis. A small ES contribution would weaken the proposed ES-centered explanation. No result is predicted here.

In particular, R14's approximately 21% oracle recovery and a future ES Shapley share are overlapping counterfactuals. They must not be added. P52 changed pure epsilon within the Z0x closure, while P54 changes the complete closure to the 2010 prescription and also evaluates its interactions with other ingredients. [S2]

Same-row integrity, privacy and cost

Preparation consumes the original completed P52 plan, its digest commit and run receipts. It checks all 963 unique observation identities and 100 unordered systems, the 2,889 recorded requests, original baseline parity and saved aggregate arithmetic. It carries forward the P52a selection of `630 profiles_v2 + 1 s1_stalled + 5 s2_stalled`; it does not rescan folders and accidentally select superseded copies. The files and scientific inputs are rehashed before and after the new run. [S2, S6]

The two new anchor corners run first on every row, costing `2*963 = 1,926` requests. Both must be finite positive pressures and reproduce their own saved P52 pressures with relative error strictly below `1e-8`. Only then can the other six corners run, costing `6*963 = 5,778` requests. Total: `7,704`. This preserves the P6 source-version bridge already established by P52, without rescoring a fresh CSV or mixing the experimental-epsilon arm into the baseline.

Each ordered-pair/corner is a fresh subprocess. The actual number of ordered pairs is read from the private plan; 100 unordered systems does not prove there are exactly 100 ordered pairs. Each component must resolve to its explicitly frozen private profile. Missing assets cannot fall back to UD from another location or to an open profile. Inherited experimental switches are cleared. P28 is set consistently, although all P52 compositions are in the interior region and therefore do not use its pure endpoint.

The actual P52 run took 198 seconds for 2,889 requests. A purely proportional planning estimate is `198*(7704/2889) = 528 seconds`, conditional on similar average evaluation and orchestration costs. Some hybrid contact kernels can converge differently, so this is not a measured R15 timing or a guarantee. The registered allocation is 7,200 seconds, serial on the Mac, with 120 seconds per worker and a five-second kill/accounting allowance. The reporting/check phase is timed separately. [S2]

Failure preserves the requested denominator. One failed anchor blocks intermediate corners. One failed new corner withholds complete-panel attribution rather than dropping its row. Every job has a terminal record and every query has a pre-call attempt receipt. An exclusive claim prevents retries into a different output folder. Repeated saved-output checks are allowed and perform no model requests. Only the aggregate error allowlist can be considered for publication after human review; profiles, row predictions and private paths stay on the Mac.

P55 changes a source file that the original P52 manifest hashed, although P52 never called its association classes. Simply applying all patches and invoking the old checker would therefore fail on that source hash. The new adapter has one explicit nonparticipant-source bridge for `src/zcosmo/z0w.py`: the historical hash must equal the reference-main bytes, and the executing file must equal the R15 registration. Every other old scientific input remains exact. The original R14 checker is unchanged, and its original execution is not retrospectively reclassified. Current participating model sources and tables are independently compared with reference main, including when old paths point into another worktree. This avoids both an unusable command sequence and a general exemption from source-integrity checks.

A first-principles local contact coefficient: what can be derived

There are defensible local-response formulations. There is no single replacement number determined by the current observations. In the existing scalar recipe,

\[
 c_0=\frac{0.3\,a_{\rm eff}^{3/2}}{2\epsilon_0}
 =12226.23534,
 \qquad c_{2010}(298.15)=8197.24225.
\]

Their ratio is approximately `0.67046`, corresponding algebraically to epsilon approximately `4.052` in the present mapping. That inversion is not a prediction of a local dielectric constant. Choosing epsilon=4 because it recreates a fitted coefficient would import the fitted target into the new theory. The same issue applies to picking a contact separation, cavity thickness or average orientation because it reproduces the desired number. [S3, S5]

Dimensional analysis explains the area exponent but not the prefactor. For a charge patch of area A and linear size proportional to the square root of A, total charge scales as `Q=sigma*A`. Coulomb energy then scales as `Q²/(epsilon0*sqrt(A))`, or `sigma²*A^(3/2)/epsilon0`. The dimensionless coefficient depends on the patch geometry, boundary response and the reference used for removing conductor screening. Calling the exponent theoretical does not derive all those ingredients.

One constructive route is a fixed linear-response model. Let q denote declared contact-charge coordinates and u the environmental polarization degrees of freedom, in one consistent electrostatic convention. Assume a stable quadratic energy

\[
 E(q,u)=\tfrac12q^T K_{qq}q+q^TK_{qu}u+
         \tfrac12u^TK_{uu}u,\qquad K_{uu}>0.
\]

Minimization gives `u*=-K_uu^{-1}K_uq q` and

\[
 K_{\rm eff}=K_{qq}-K_{qu}K_{uu}^{-1}K_{uq}.
\]

After specifying contact and conductor reference operators, a declared mismatch mode `q=lambda*v` has curvature

\[
 c_{\rm mode}=\tfrac12v^T
   (K_{\rm eff}^{\rm contact}-K_{\rm eff}^{\rm reference})v.
\]

The units of v must make lambda the chosen sigma mismatch. This is an explicit derivation for a specified model. It is not yet the scalar kernel used by every segment pair in COSMO-SAC. The cavity and polarization operator, as well as the mapping from molecular screening charges to q, must be defined independently. Averaging over contact orientations needs a physical distribution. Electronic minimization alone does not determine that distribution or its entropy. A thermal integral over u also has a determinant term; replacing the liquid contact free energy by its minimum energy discards information.

There is an additional reference-energy issue worth making explicit. For fixed T, a segment kernel transformed as

\[
 W'_{st}=W_{st}+u_s+u_t
\]

has `Gamma'_s = exp(u_s/RT)*Gamma_s` in the segment fixed-point equation. The same transformation applies to mixture and pure profiles evaluated with that kernel, so the extra terms cancel in `ln Gamma_mix - ln Gamma_pure`. Thus a fit to arbitrary absolute contact energies can constrain directions that do not change the pure-referenced activity coefficient at all. A meaningful independent contact comparison must preserve the reference convention and identify observable exchange effects. H15 verifies this cancellation using the actual segment solver on synthetic profiles; it is not a new molecular calculation.

| Research route, all A if introduced into production | Physical opportunity | What is still missing; circularity risk | Explicit free-compute sizing, not an authorized experiment |
|---|---|---|---|
| Local reaction-field or boundary-response kernel | Compute a response operator for independently specified finite patches, with the conductor stabilization removed once. This can replace a bulk scalar response assumption. | Patch shape, contact separation and environmental susceptibility are not fixed by bulk epsilon. A fitted “local epsilon” or hand-selected geometric prefactor would encode the answer. A converged toy boundary problem is not validation of a liquid kernel. | Eight fixed geometries at 128, 256 and 512 surface unknowns require zero SCFs. One dense LU per case costs about `(2/3)*8*(128³+256³+512³) = 0.816 billion` floating-point operations, before matrix construction and checks; a 512-square float64 matrix is 2 MiB. Classical algebra is affordable. The physical definition is the limiting step. |
| Independent dimer/cluster response | Constrained charge or field perturbations at frozen independently chosen contacts can estimate contact-response curvatures. Separate monomer and conductor references expose polarization/deformation effects. | A total binding energy includes more than ES misfit. Dividing it by a sigma mismatch would absorb HB, dispersion and repulsion, including physics already used to derive the HB constants. Basis, counterpoise and fragment definitions need independent checks. A dimer does not by itself supply condensed-phase contact populations. | An illustrative eight-contact panel, three frozen geometries each, two reference conditions and five perturbation amplitudes is `8*3*2*5=240` SCF attempts. At an assumed 30–120 seconds each: 2–8 four-core worker-hours. This excludes optimizer work, constrained-DFT implementation and basis/response validation. No timing was measured for these calculations. |
| Self-consistent conductor-to-dielectric profiles | Let molecular polarization respond to the declared environment, rather than changing only a contact prefactor. A variational model could couple profiles and mixture response consistently. | Finite-epsilon PCM exists, but a consistent activity model needs polarization free energies, pure references and composition/temperature derivatives. Merely rescaling q and also multiplying the contact energy can count the response twice. Profiles changed by environment cannot be used with the old derivative formula unchanged. | A small illustrative eight-molecule, three-environment, three-iteration calculation is 72 single points, 0.6–2.4 worker-hours at the same assumed rate. Applying even this crude grid to 742 compounds is 6,678 single points, 55.7–222.6 worker-hours, before validation or composition/temperature coverage. This is not a complete self-consistent convergence budget. |

The response derivation above is my mathematical construction under stated assumptions, not a claim that a particular external package implements a validated parameter-free Z0x correction. Published self-consistent continuum formulations establish that density and solvent response can be treated together, but their fitted non-electrostatic terms do not become fit-free because the polarization equations are self-consistent. Official PySCF documentation provides the actual PCM interface; it does not validate its use as a new local contact closure. [U2, U3]

The most defensible future direction, conditional on a substantial ES attribution, would be an independently specified contact-response audit, with numerical curvature and reference-energy checks before any ThermoML comparison. It would need a fixed structural panel including non-HB contacts and aqueous/branched controls, not contacts selected from P54's worst errors. A new coefficient must be frozen from that physical calculation before a separately audited validation set is exposed. Native code and a complete scientific acceptance protocol for such an audit are not supplied or authorized here. The 240-SCF figure only shows that a narrow research pilot could be affordable, not that it would close the VLE deficit.

P55: minimal association repair and its meaning

The defect is real and local. The subclasses add association through `_g`, but the optimized base-class `lngamma` takes `_analytic` for interior compositions and optionally `_endpoint` at pure compositions. Those paths do not call the overridden `_g`. The small patch adds `Z0wBinary.lngamma`, which always differentiates the complete `self._g` using the historical stencil. `Z0w2` and normal descendants inherit the repair. Z0x itself remains byte-for-byte unchanged. [S4, S7]

With `h=1e-4`, `a=max(x-h,0)` and `b=min(x+h,1)`, it evaluates

\[
 d=[g(b)-g(a)]/(b-a),\quad
 (\ell_1,\ell_2)=(g(x)+(1-x)d,\ g(x)-xd).
\]

This restores the intended source-level dispatch. It deliberately retains the old one-sided endpoint approximation. For the simple association contribution `g=alpha*x*(1-x)`, the dilute endpoint from this stencil is `alpha*(1-h)`, not the exact `alpha`. P28's argument for a frozen-coefficient Z0x endpoint does not remove association's separate endpoint derivative. Calling this fix E-equivalent to defective current main, or claiming a new exact association endpoint, would be wrong.

Software acceptance compares the restored method against the explicit historical full-g stencil to `1e-12` on synthetic values at pure endpoints, strip boundaries and interior compositions, with P28 on and off. Tests include nonzero `_ga` and direct `_g` descendants. A separate test uses the actual site mass-action code with synthetic strengths. The actual NumPy contact solver checks the eight hybrid models against independently differentiated excess Gibbs energies. These tests do not access a chemical benchmark, certify a private Z0w3 driver absent from current `src`, or claim the 25-molecule/2,302-row agreement gate.

The patch makes no association strength or site-model change. The silent iteration-limit exit in `_solve_X` remains a distinct issue and is documented rather than repaired under another label. Archived Z0w/Z0w2/Z0w3 failures predate P6, as R14 records, so this later code defect cannot explain them away. No fresh association score is authorized. [S2, S7]

A replacement association architecture still deserves theoretical attention, but “switch off the COSMO HB term” was already implemented. An independently justified partition must distinguish the reference interactions from the association free energy, along with site multiplicity, saturation and pure-fluid subtraction. Z0w3's excessive aqueous nonideality and nitrogen occupancy problem are constraints on that work, not evidence selecting a fourth variant. An independently derived association model could be useful; adding another fitted or hand-rescaled strength on the same inspected scorecards is not justified by this repair. [S7, S8]

P56: manuscript changes supplied now

The paper can tell a substantive story without promising that all empirical input has vanished or that the remaining VLE loss has one proven cause. The patch makes the following concrete revisions; it does not regenerate a numerical table.

| Location | Exact change of claim |
|---|---|
| Title, abstract, introduction | Replace the blanket removal-of-every-fitted-constant claim with replacement of specified interaction constants without ThermoML regression. Identify retained effective area and combinatorial conventions, profile processing, UD conformation-selection history and experimental pure vapor pressures. |
| Methods and historical results | State the original prospectively frozen split and later exposure separately. Retain original main7 and temporal numbers and their different common subsets. Distinguish P6's interior derivative, P28's pure Z0x endpoint and the adjacent historical stencil. |
| Open-profile section | Preserve v1's failed agreement test and v2's narrow historical pass, both with the actual exploratory scope. Record 630 original-Berny profiles plus six flagged files, the response-gradient compatibility failure and unresolved TEG mismatch. Do not turn performance optimizations into a stationarity guarantee. |
| Conformer/glycol section | Limit the early small ensemble effect to that finite experiment. Add R10 lineage, R11's scoped tail attribution, P46a's 142 rows, the 80%-of-comparator-gap versus 61%-of-original-error distinction, tetraEG's 13% exception and the conditional 0.283 MAE residual. Preserve P35's closeout and lack of a liquid-conformer rule. |
| New dielectric section | Record P51's withheld complete aggregate, not a fabricated baseline-validation pass. Add P52/P52a's 963-row result, endpoint replay, 13.78/13.07/10.44 AADs and fixed-298.15-K scope. Its approximately 21% recovery is not a bound on all possible dielectric corrections. |
| Association and discussion | Preserve historical failures, state the later dispatch regression separately, and distinguish an architectural double-counting hypothesis from a proved unique mechanism. Remove the assertion that bulk dielectric screening is the established decisive missing physics. |
| Limitations and availability | State that the study retains empirical upstream ingredients and reused data. Keep UD-derived private artifacts out of the claimed public reproduction package. Preserve LLE detection/composition qualifications and the need for a submission-time reference/artifact audit. |

The earlier wording `a_eff=pi*r_av²=7.25` does not establish an independent derivation of the retained effective area. The manuscript now states what the code actually fixes. Historical registrations and source comments describing the original motivation are left intact, with the later scope correction identified as such. [S3, S5, S9]

No P54 attribution numbers are inserted in the manuscript. After its registered run, its complete result or failure can be added as a separately dated record. The paper's main conclusions do not require choosing a favorable hybrid. The new manuscript prose and preserved historical tables are a working revision, not a claim that all old bibliography entries and figure files have been independently verified for submission.

Execution and verification

Executed in this review: current-source and registration review, reconstruction and Git-blob verification of the source files used for local numerical tests, algebra and cost checks, and the delivered-code tests. The local reconstruction is a source subset, not a full repository clone. The segment solver, Z0x and repaired association classes were exercised with synthetic profiles and synthetic strength/table inputs. No production or UD profile was placed in that reconstruction.

The R15 suite passed 34 tests. It includes a complete synthetic 963-row/100-system P52 receipt-adapter check, real numerical hybrid workers on synthetic profile files, all-corner derivative checks, association dispatch regressions, failure/identity mutations and harmless subprocess timeout checks. The unchanged R14 suite passed 45 tests. Together these are 79 portable tests, not 79 molecules or experimental checks. All five diffs passed independent and combined application checks on the byte-verified source reconstruction. Shell syntax and embedded Python compilation passed. Re-extraction and application from this delivered Markdown also passed. The historical manuscript numerical tables are unchanged, apart from a scoped model-label edit, and `z0x.py` remains byte-for-byte unchanged.

Not executed: the real Mac archive replay for P54, any of its 7,704 real model requests, fresh association benchmarking, local-contact quantum calculations, MD, profile generation or a remote repository write. PySCF was not needed or installed. The fitted-factor pressure contributions remain unknown until the registered private run. The only R14 scientific numbers quoted here are its already published aggregate results.

Exact application, registration and benchmark/check commands

The five patches are individually applicable to the pinned baseline, but H15 tests require P54 and P55 to be applied. All five are applied together below. Run from a clean tracked checkout of the reference commit; existing ignored private data need not be removed. Save this report outside the repository.

```bash
set -euo pipefail
BASE=3cd0a22888b40699d5f4994f5ba2e5cd274703df
test "$(git rev-parse HEAD)" = "$BASE"
git diff --quiet
git diff --cached --quiet
: "${R15_REPORT:?Set R15_REPORT to the saved ZCOSMO_ROUND15_REPORT.md}"
export R15_PATCHES="$(mktemp -d)"
python - <<'PY'
import os,re
from pathlib import Path
text=Path(os.environ['R15_REPORT']).read_text()
items=re.findall(r'<!-- BEGIN PATCH (\w+) -->\s*```diff\n(.*?)\n```\s*<!-- END PATCH \1 -->',text,re.S)
assert [x[0] for x in items]==['H15','P54','P55','P56','REG15']
root=Path(os.environ['R15_PATCHES'])
for name,body in items:
    (root/(name+'.patch')).write_text(body+'\n')
PY
for p in H15 P54 P55 P56 REG15; do
  git apply --check "$R15_PATCHES/$p.patch"
done
cat "$R15_PATCHES/H15.patch" "$R15_PATCHES/P54.patch" \
  "$R15_PATCHES/P55.patch" "$R15_PATCHES/P56.patch" \
  "$R15_PATCHES/REG15.patch" > "$R15_PATCHES/all.patch"
git apply --check "$R15_PATCHES/all.patch"
git apply "$R15_PATCHES/all.patch"
export PYTHONPATH=src:scripts
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /usr/bin/time -p python scripts/r15_selftest.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python scripts/r14_selftest.py
python -m py_compile scripts/r15_math.py scripts/r15_factorial.py \
  scripts/r15_selftest.py src/zcosmo/z0w.py
python - <<'PY'
import subprocess
from pathlib import Path
base='3cd0a22888b40699d5f4994f5ba2e5cd274703df'
old=subprocess.check_output(['git','show',base+':manuscript/draft.md'],text=True)
new=Path('manuscript/draft.md').read_text()
oldrows=[s for s in old.splitlines() if s.startswith('|')]
newrows=[s for s in new.splitlines() if s.startswith('|')]
oldrows=[s.replace('Z0x (no fitted constants, no choices)',
                  'Z0x (no new ThermoML parameter regression)') for s in oldrows]
assert oldrows==newrows, 'A historical manuscript table changed'
assert subprocess.check_output(['git','show',base+':src/zcosmo/z0x.py'])==Path('src/zcosmo/z0x.py').read_bytes()
print('Historical table values and optimized Z0x source preserved.')
PY
```

The next block is an operator adoption step. It is not executed by this report. It records the software repair and manuscript edits with the diagnostic protocol before any private-data preparation. No physical association score is permitted by it.

```bash
set -euo pipefail
umask 077
printf '\nRound 15 adopted at %s\n\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" >> PREREGISTRATION.md
cat docs/astra/round15/REGISTRATION_PROPOSED.md >> PREREGISTRATION.md
git add scripts/r15_math.py scripts/r15_factorial.py scripts/r15_selftest.py \
  src/zcosmo/z0w.py manuscript/draft.md \
  docs/astra/round15/REGISTRATION_PROPOSED.md PREREGISTRATION.md
git commit -m "Register R15 contact attribution, association dispatch and manuscript scope"
export R15_REG="$(git rev-parse HEAD)"
export PYTHONPATH=src:scripts
```

For P54, supply the actual original P52 private paths. The R14 plan digest was frozen in the recorded `e0f1608` commit; resolving it below obtains its full identity rather than inventing one. Missing private assets stop the protocol. Do not rerun R14 to recreate them under this budget.

```bash
set -euo pipefail
umask 077
: "${R15_REG:?Run the registration block first}"
: "${R14_PLAN:?Set to the completed P52 private oracle plan.json}"
: "${R14_RUN:?Set to its completed private oracle output directory}"
export R14_PLAN_COMMIT="$(git rev-parse 'e0f1608^{commit}')"
export R15_PRIVATE="${R15_PRIVATE:-$HOME/zc-r15-contact-20261008}"
test ! -e "$R15_PRIVATE"
mkdir -m 700 "$R15_PRIVATE"
export PYTHONPATH=src:scripts
/usr/bin/time -p python scripts/r15_factorial.py freeze \
  --registration "$R15_REG" --r14-plan "$R14_PLAN" \
  --r14-plan-commit "$R14_PLAN_COMMIT" --r14-run "$R14_RUN" \
  --out "$R15_PRIVATE/plan" > "$R15_PRIVATE/freeze.log" 2>&1
cp "$R15_PRIVATE/plan/PLAN_SHA256.txt" docs/astra/round15/PLAN_SHA256.txt
git add docs/astra/round15/PLAN_SHA256.txt
git commit -m "Freeze R15 private 963-row contact-factorial plan digest"
export R15_PLAN_COMMIT="$(git rev-parse HEAD)"
set +e
/usr/bin/time -p python scripts/r15_factorial.py run \
  --plan "$R15_PRIVATE/plan/plan.json" --plan-commit "$R15_PLAN_COMMIT" \
  --out "$R15_PRIVATE/run" > "$R15_PRIVATE/run.log" 2>&1
rc=$?
set -e
if [ "$rc" -ne 0 ]; then
  printf 'R15 returned status %s. Retain all receipts; do not retry the run.\n' "$rc"
  exit "$rc"
fi
/usr/bin/time -p python scripts/r15_factorial.py check \
  --plan "$R15_PRIVATE/plan/plan.json" --plan-commit "$R15_PLAN_COMMIT" \
  --run "$R15_PRIVATE/run" > "$R15_PRIVATE/check.log" 2>&1
python - <<'PY'
import json,os
from pathlib import Path
p=Path(os.environ['R15_PRIVATE'])/'run'
s=json.loads((p/'summary.json').read_text())
t=json.loads((p/'timing.json').read_text())
print(json.dumps({'attempted_model_calls':s['attempted_model_calls'],
                  'model_run_wall_s':t['model_run_wall_s'],
                  'collection_wall_s':s['collection_wall_s'],
                  'complete':s['status']['complete']},indent=2))
PY
# Review run/public-errors.json before a separate publication decision.
# Do not publish plan.json, private-rows.json, overlays or logs.
```

A saved-output `check` can be repeated without model calls. If the driver is interrupted before collection, the `collect` command can account for existing terminal receipts without restarting workers; it creates a result only when one does not already exist. An incomplete result is not a scientific pass. Neither command removes an execution claim or authorizes replacement attempts.

Source record

[S1] `docs/astra/ROUND15_PROMPT.md` and `docs/OPTIMIZATION_BRIEF.md` at the reference main. [S2] `docs/astra/round14/RESULTS.md`, including P52a and the dispatch audit. [S3] `src/zcosmo/cosmosac.py` and `results/z_params/Z0.json`. [S4] `src/zcosmo/z0x.py`. [S5] `src/zcosmo/zmodel.py` and the original Z0/Z0x registrations. [S6] `scripts/r14_oracle.py`, `r14_dielectric.py`, `r14_selftest.py` and the original round-14 report, qualified by the later P52a amendment. [S7] `src/zcosmo/z0w.py`. [S8] The Z0w-family registrations and recorded results in `PREREGISTRATION.md`; `PROGRESS.md` session 5. [S9] `manuscript/draft.md`, with `docs/astra/round7/RESULTS.md` through `docs/astra/round14/RESULTS.md` for the cited later evidence. These repository paths are pinned to `3cd0a22888b40699d5f4994f5ba2e5cd274703df`, not mutable main.

[U1] Official SCM parameter documentation, COSMO-SAC 2010 column and mapping of the electrostatic expression: `https://www.scm.com/doc/COSMO-RS/COSMO-RS_and_COSMO-SAC_parameters.html`. Used for parameter provenance, not as evidence of a successful fit-free correction.

[U2] Andreussi, Dabo and Marzari, “Revised self-consistent continuum solvation in electronic-structure calculations,” author manuscript `https://arxiv.org/abs/1112.5332`. Its abstract explicitly describes fitted non-electrostatic/solvation components. Used to distinguish a self-consistent formulation from a claim of zero empirical calibration.

[U3] Official PySCF solvent documentation: `https://pyscf.org/user/solvent.html`. Existing PCM capability does not establish a thermodynamically consistent new activity-coefficient model. The quadratic and segment-gauge identities in this report are derived explicitly above, not attributed to a source that was not inspected.

[U4] Bell et al., “A Benchmark Open-Source Implementation of COSMO-SAC,” JCTC 2020, NIST publication record: `https://www.nist.gov/publications/benchmark-open-source-implementation-cosmo-sac`. Used for the benchmark implementation's provenance. No real NIST profile was evaluated in this review.

Local source-integrity record

The existing-file patch targets and numerical-test dependencies below were checked against their repository Git blob identifiers before local testing. This establishes the reconstructed file bytes, not a complete local clone or execution against private Mac assets.

| Source file | Bytes | Verified Git blob |
|---|---:|---|
| `src/zcosmo/cosmosac.py` | 10483 | `c226a668b7b9dba9e7400cda180fafd8faa700f3` |
| `src/zcosmo/z0x.py` | 3795 | `c558d4e95db9b78f3b57d6a103a293e21feeb9af` |
| `src/zcosmo/z0w.py` | 6539 | `97abef58804bfad1d890a9335f0e8ee52c486fa4` |
| `manuscript/draft.md` | 25280 | `89eb8618eb6e025e3757feef0006b501d01203e0` |
| `scripts/r14_dielectric.py` | 16029 | `ae2f350ce4d9acc9ab737f669828e861d028853b` |
| `scripts/r14_oracle.py` | 18251 | `5cf54f48fed292fe1081ca3fc19ca946411a90fc` |
| `scripts/r14_selftest.py` | 16312 | `49d68323a9ddfdb3d8d3af79a81d7c698e217f95` |

Extractable patches

H15 contains the shared arithmetic and tests. P54 uses H15 and the unchanged R14 helpers. The execution protocol applies all patches together so that its explicit association-source bridge can account for P55. P56 contains the manuscript changes; REG15 is proposed registration text, not an adoption record.

<!-- BEGIN PATCH H15 -->
```diff
diff --git a/scripts/r15_math.py b/scripts/r15_math.py
new file mode 100644
--- /dev/null
+++ b/scripts/r15_math.py
@@ -0,0 +1,171 @@
+"""R15 finite-game accounting and endpoint-preserving diagnostic model factory.
+
+No chemistry data is read until make_corner is called. All fitted substitutions
+are explanatory interventions, never candidates for production selection.
+"""
+from __future__ import annotations
+import itertools
+import math
+import numpy as np
+
+FACTORS = ('electrostatic_closure', 'HB_constants', 'London_to_none',
+           'aeff_shared', 'profile_convention_shared')
+CORNERS = tuple(f'{i:03b}' for i in range(8))
+ANCHORS = ('000', '111')
+INTERMEDIATE = tuple(c for c in CORNERS if c not in ANCHORS)
+TOL_PP = 1e-8
+
+
+def require(ok, message):
+    if not ok:
+        raise ValueError(message)
+
+
+def shared_audit(z0, target):
+    """A drift is a failed design, not permission to invent another factor."""
+    shared = ('aeff', 'q0', 'r0', 'z', 'london_table', 'disp_override')
+    require(all(getattr(z0, n) == getattr(target, n) for n in shared),
+            'Non-registered endpoint difference in shared ingredients')
+    require(z0.aeff == target.aeff == 7.25 and z0.B_ES == 0.0,
+            'Expected common aeff and historical Z0 ES definition')
+    require(z0.disp_mode == 'london' and z0.w_dsp == 1.0 and z0.use_dsp,
+            'Expected Z0 London endpoint')
+    require(target.disp_mode == 'dsp' and not target.use_dsp,
+            '2010 target must have no explicit dispersion, not fitted 2014 dsp')
+    return dict(shared={n: getattr(z0, n) for n in shared},
+        HB_cutoff='same stored NHB/OH/OT split and delta_w opposite-sign mask',
+        profile='identical frozen P52 UD bytes for both components in every corner')
+
+
+def make_corner(keys, corner):
+    """Use existing production kernels, including dc/dx only on the Z0x side."""
+    require(corner in CORNERS, 'Unknown three-bit corner')
+    from zcosmo.cosmosac import Params, Mixture
+    from zcosmo.models import load_z_params
+    from zcosmo.z0x import Z0xBinary
+    z0, target = load_z_params('Z0'), Params(use_dsp=False)
+    shared_audit(z0, target)
+    e, h, disp = map(int, corner)
+    kw = {}
+    if h:
+        kw.update({n: getattr(target, n) for n in ('c_OH_OH', 'c_OT_OT', 'c_OH_OT')})
+    if disp:
+        kw.update(use_dsp=False, disp_mode=target.disp_mode, w_dsp=target.w_dsp)
+    if e:
+        kw.update(A_ES=target.A_ES, B_ES=target.B_ES)
+    p = z0.with_(**kw)
+    if corner == '111':
+        require(p == target, 'All-swapped corner does not exhaust target differences')
+    if e:
+        # c(T)=A+B/T^2 is independent of composition: dc/dx = 0.
+        return Mixture(keys, p)
+    model = Z0xBinary(keys)
+    model.z0 = p
+    model._mix.clear()
+    return model
+
+
+def shapley(values):
+    """Exact finite-game Shapley values, first string character is player zero."""
+    n = len(next(iter(values)))
+    names = tuple(f'{i:0{n}b}' for i in range(2**n))
+    require(set(values) == set(names), 'Incomplete cube')
+    arrays = {s: np.asarray(values[s], float) for s in names}
+    shape = arrays[names[0]].shape
+    require(all(a.shape == shape and np.isfinite(a).all() for a in arrays.values()),
+            'Nonfinite or misaligned cube')
+    ans = np.zeros((n,) + shape)
+    for j in range(n):
+        for s in names:
+            if s[j] == '1':
+                continue
+            k = s.count('1')
+            t = s[:j] + '1' + s[j+1:]
+            weight = math.factorial(k) * math.factorial(n-k-1) / math.factorial(n)
+            ans[j] += weight * (arrays[t] - arrays[s])
+    return ans
+
+
+def lift_five(values):
+    require(set(values) == set(CORNERS), 'Incomplete active cube')
+    return {f'{i:05b}': values[f'{i:05b}'[:3]] for i in range(32)}
+
+
+def dividends(values):
+    """Baseline-anchored inclusion/exclusion interactions, not extra experiments."""
+    out = {}
+    for s in CORNERS[1:]:
+        active = [j for j, b in enumerate(s) if b == '1']
+        v = np.zeros_like(np.asarray(values['000'], float))
+        for bits in itertools.product('01', repeat=len(active)):
+            t = ['0'] * 3
+            for j, bit in zip(active, bits):
+                t[j] = bit
+            v += (-1)**(len(active)-bits.count('1')) * np.asarray(values[''.join(t)], float)
+        out[s] = v
+    return out
+
+
+def summary(rows, predictions, anchors_passed):
+    """Fixed denominator; a single failed corner withholds complete attribution."""
+    a = np.asarray(predictions, float)
+    require(len(rows) > 0 and a.shape == (len(rows), 8), 'Wrong factorial dimensions')
+    ids = [str(r['row_id']) for r in rows]
+    require(len(set(ids)) == len(ids), 'Duplicate observation identity')
+    truth = np.array([r['P'] for r in rows], float)
+    require(np.isfinite(truth).all() and (truth > 0).all(), 'Invalid frozen pressure')
+    finite = np.isfinite(a) & (a > 0)
+    status = dict(requested_rows=len(rows), requested_corners=8,
+        requested_values=8*len(rows), finite_by_corner=dict(zip(CORNERS, finite.sum(0).tolist())),
+        complete=bool(finite.all() and anchors_passed), anchors_passed=bool(anchors_passed),
+        adopted=False, retrospective=True, fitted_substitutions=True)
+    if not status['complete']:
+        return dict(status=status, public_errors=None, private_rows=None)
+    with np.errstate(over='ignore', invalid='ignore', divide='ignore'):
+        signed = 100*(a/truth[:, None]-1)
+    if not np.isfinite(signed).all():
+        status.update(complete=False, derived_error_nonfinite=int((~np.isfinite(signed)).sum()))
+        return dict(status=status, public_errors=None, private_rows=None)
+    errors = np.abs(signed)
+    value = {c: -errors[:, j] for j, c in enumerate(CORNERS)}
+    bias_value = {c: signed[:, j] for j, c in enumerate(CORNERS)}
+    phi = shapley(lift_five(value))
+    bias_phi = shapley(lift_five(bias_value))
+    three = shapley(value)
+    efficiency = float(np.max(np.abs(phi.sum(0) - (errors[:, 0]-errors[:, 7]))))
+    require(efficiency < TOL_PP, 'Error Shapley efficiency failed')
+    require(np.max(np.abs(bias_phi.sum(0)-(signed[:, 7]-signed[:, 0]))) < TOL_PP,
+            'Signed-pressure Shapley efficiency failed')
+    require(np.max(np.abs(phi[:3]-three)) < TOL_PP and np.array_equal(phi[3:], np.zeros_like(phi[3:])),
+            'Shared-factor dummy-player identity failed')
+    dd = dividends(value)
+    require(np.max(np.abs(sum(dd.values())-(errors[:, 0]-errors[:, 7]))) < TOL_PP,
+            'Interaction efficiency failed')
+    systems = sorted({r['system'] for r in rows})
+    group = [np.array([r['system'] == s for r in rows]) for s in systems]
+    avg = lambda x: float(np.mean(x))
+    macro = lambda x: float(np.mean([np.mean(x[g]) for g in group]))
+    public = dict(rows=len(rows), systems=len(systems), corners={}, factors={}, interactions={},
+        max_efficiency_error_pp=efficiency, no_generalization_CI=True,
+        profile_source='P52 UD for both endpoints; no profile-source claim',
+        direction='stored-epsilon Z0x to COSMO-SAC 2010, not experimental-epsilon Z0x')
+    for j, c in enumerate(CORNERS):
+        public['corners'][c] = dict(AAD_percent=avg(errors[:, j]), bias_percent=avg(signed[:, j]),
+            equal_system_AAD_percent=macro(errors[:, j]),
+            improved_vs_000=int((errors[:, j] < errors[:, 0]).sum()),
+            worsened_vs_000=int((errors[:, j] > errors[:, 0]).sum()))
+    gap = avg(errors[:, 0]-errors[:, 7])
+    public['endpoint_gap_pp'] = gap
+    for j, name in enumerate(FACTORS):
+        public['factors'][name] = dict(error_reduction_pp=avg(phi[j]),
+            equal_system_error_reduction_pp=macro(phi[j]),
+            signed_bias_change_pp=avg(bias_phi[j]),
+            gap_share=None if gap <= 1e-6 else avg(phi[j])/gap,
+            one_at_a_time_error_reduction_pp=avg(errors[:, 0]-errors[:, int(''.join('1' if i==j else '0' for i in range(3)),2)])
+                if j < 3 else 0.0)
+    public['interactions'] = {s: dict(error_reduction_pp=avg(v),
+        equal_system_error_reduction_pp=macro(v)) for s, v in dd.items()}
+    private = [dict(row_id=ids[i], pressure_kPa=a[i].tolist(),
+        absolute_percent_error=errors[i].tolist(), error_ShAP_pp=phi[:, i].tolist(),
+        signed_bias_ShAP_pp=bias_phi[:, i].tolist()) for i in range(len(rows))]
+    return dict(status=status, public_errors=public, private_rows=private)
diff --git a/scripts/r15_selftest.py b/scripts/r15_selftest.py
new file mode 100644
--- /dev/null
+++ b/scripts/r15_selftest.py
@@ -0,0 +1,394 @@
+"""Portable R15 tests. Synthetic profiles, fake table loaders, no UD or ThermoML.
+
+Numerical tests use the actual NumPy segment solver and actual Z0x/Z0w classes.
+Process tests mock scientific workers; one harmless subprocess checks timeout.
+"""
+from __future__ import annotations
+import argparse
+from contextlib import contextmanager
+import importlib.util
+import itertools
+import json
+import os
+from pathlib import Path
+import sys
+import tempfile
+import types
+import unittest
+from unittest.mock import patch
+import numpy as np
+import r15_math as a
+import r15_factorial as r
+
+
+@contextmanager
+def engines():
+    root=Path(__file__).resolve().parents[1]
+    package=types.ModuleType('zcosmo');package.__path__=[str(root/'src/zcosmo')]
+    def module(name,path):
+        spec=importlib.util.spec_from_file_location(name,path)
+        mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod)
+        return mod
+    with patch.dict(sys.modules,{'zcosmo':package}):
+        c=module('zcosmo.cosmosac',root/'src/zcosmo/cosmosac.py')
+        models=types.ModuleType('zcosmo.models');zm=types.ModuleType('zcosmo.zmodel')
+        qc=types.ModuleType('zcosmo.qc_hbond');qc.DIMERS=()
+        z0=c.Params(A_ES=12226.235339788673,B_ES=0.0,c_OH_OH=5712.229463082564,
+                    c_OT_OT=5611.4027535161395,c_OH_OT=5987.642651646004,
+                    disp_mode='london',w_dsp=1.0)
+        models.ROOT=root;models.load_z_params=lambda name:z0
+        zm.c_es_theory=lambda aeff=7.25,fpol=1.:fpol*.3*aeff**1.5/2.395e-4/2
+        sys.modules.update({'zcosmo.models':models,'zcosmo.zmodel':zm,'zcosmo.qc_hbond':qc})
+        fluids={}
+        for i,key in enumerate(('A','B')):
+            p=np.zeros((3,51));p[0,[15,22,25,30,38]]=[2,8,9,5,1]
+            p[1,[8,12,39,42]]=[1+2*i,2+i,4-i,1]
+            p[2,[10,20,36,41]]=[1,2,3+i,1]
+            p *= (90+30*i)/p.sum()
+            fluids[key]=c.Fluid(key,p,float(p.sum()),80.+30*i,'NHB',None,{})
+        c.load_fluid=lambda k:fluids[k]
+        c._london_table=lambda path:{'A':(1000.,10.),'B':(1600.,14.)}
+        x=module('zcosmo.z0x',root/'src/zcosmo/z0x.py');x._eps=lambda:{'A':3.,'B':35.}
+        w=module('zcosmo.z0w',root/'src/zcosmo/z0w.py')
+        yield c,x,w,z0
+
+
+def fixture(n=6):
+    rows=[dict(row_id=str(i),c1='A'+str(i%2),c2='B',T=298.15,x1=.3,P=100.,
+               psat=[50.,80.],system='A'+str(i%2)+'|B') for i in range(n)]
+    def val(row,c):
+        e,h,d=map(int,c)
+        return 112.+int(row['row_id'])/10-6*e+2*h-3*d+e*h
+    preds=np.array([[val(row,c) for c in a.CORNERS] for row in rows])
+    m=dict(rows=rows,jobs=r.jobs_for(rows),prior_anchors=preds[:,[0,7]].tolist())
+    return m,preds,val
+
+
+class Arithmetic(unittest.TestCase):
+    def test_dummy_factor_exactness(self):
+        rng=np.random.default_rng(7);v={c:rng.normal(size=11) for c in a.CORNERS}
+        full=a.shapley(a.lift_five(v));small=a.shapley(v)
+        np.testing.assert_allclose(full[:3],small,atol=1e-12,rtol=0)
+        np.testing.assert_array_equal(full[3:],np.zeros_like(full[3:]))
+
+    def test_interaction_allocates_to_its_members(self):
+        v={c:np.array([6*int(c[0])*int(c[1])]) for c in a.CORNERS}
+        np.testing.assert_allclose(a.shapley(v).ravel(),[3,3,0],atol=1e-14)
+        dd=a.dividends(v);self.assertEqual(dd['110'][0],6.)
+        self.assertEqual(sum(v[0] for v in dd.values()),6.)
+
+    def test_full_five_way_efficiency(self):
+        m,p,_=fixture();z=a.summary(m['rows'],p,True)
+        self.assertTrue(z['status']['complete'])
+        q=z['public_errors'];self.assertAlmostEqual(sum(v['error_reduction_pp'] for v in q['factors'].values()),q['endpoint_gap_pp'])
+        self.assertEqual(q['factors']['profile_convention_shared']['error_reduction_pp'],0.)
+
+    def test_error_not_absolute_pressure_change(self):
+        rows=[dict(row_id='r',P=100.,system='x|y')]
+        p=np.array([[90. if c[0]=='0' else 110. for c in a.CORNERS]])
+        z=a.summary(rows,p,True)['public_errors']
+        self.assertAlmostEqual(z['factors']['electrostatic_closure']['error_reduction_pp'],0.)
+        self.assertAlmostEqual(z['factors']['electrostatic_closure']['signed_bias_change_pp'],20.)
+
+    def test_nonfinite_preserves_universe(self):
+        m,p,_=fixture();p[0,2]=np.nan;z=a.summary(m['rows'],p,True)
+        self.assertFalse(z['status']['complete']);self.assertIsNone(z['public_errors'])
+        self.assertEqual(z['status']['requested_rows'],6)
+        self.assertEqual(z['status']['finite_by_corner']['010'],5)
+
+    def test_derived_error_overflow_is_not_a_complete_score(self):
+        m,p,_=fixture();m['rows'][0]['P']=1e-300;p[0,2]=1e300
+        q=a.summary(m['rows'],p,True)
+        self.assertFalse(q['status']['complete']);self.assertIsNone(q['public_errors'])
+        self.assertEqual(q['status']['derived_error_nonfinite'],1)
+
+    def test_failed_anchors_withhold_complete_result(self):
+        m,p,_=fixture();self.assertIsNone(a.summary(m['rows'],p,False)['public_errors'])
+
+    def test_duplicate_ids_fail(self):
+        m,p,_=fixture();m['rows'][1]['row_id']='0'
+        with self.assertRaises(ValueError):a.summary(m['rows'],p,True)
+
+    def test_negative_contribution_and_unclipped_share(self):
+        m,p,_=fixture();q=a.summary(m['rows'],p,True)['public_errors']
+        self.assertLess(q['factors']['HB_constants']['error_reduction_pp'],0)
+        self.assertGreater(q['factors']['electrostatic_closure']['gap_share'],0)
+
+    def test_incomplete_cube_fails(self):
+        with self.assertRaises(ValueError):a.shapley({'000':np.ones(2)})
+
+    def test_budget_arithmetic(self):
+        rows=[]
+        for j in range(100):
+            for k in range(10 if j<63 else 9):
+                rows.append(dict(c1=str(j),c2='b'))
+        self.assertEqual(len(rows),963);jobs=r.jobs_for(rows)
+        self.assertEqual(len(jobs),800)
+        self.assertEqual(sum(len(j['indices']) for j in jobs if j['corner'] in a.ANCHORS),1926)
+        self.assertEqual(sum(len(j['indices']) for j in jobs),7704)
+
+
+class ModelTests(unittest.TestCase):
+    def test_endpoint_models_unchanged(self):
+        with engines() as (c,x,w,z0):
+            for T,xx in itertools.product((298.15,360.),(.2,.63)):
+                comp=np.array([xx,1-xx])
+                np.testing.assert_array_equal(a.make_corner(['A','B'],'000').lngamma(T,comp),x.Z0xBinary(['A','B']).lngamma(T,comp))
+                np.testing.assert_array_equal(a.make_corner(['A','B'],'111').lngamma(T,comp),c.Mixture(['A','B'],c.Params(use_dsp=False)).lngamma(T,comp))
+
+    def test_shared_drift_fails(self):
+        with engines() as (c,x,w,z0):
+            for n,v in (('aeff',8.),('q0',80.),('r0',70.),('z',8.)):
+                with self.assertRaises(ValueError):a.shared_audit(z0.with_(**{n:v}),c.Params(use_dsp=False))
+
+    def test_London_really_switches_off(self):
+        with engines() as (c,x,w,z0):
+            p=a.make_corner(['A','B'],'001').z0
+            self.assertNotEqual(p.disp_mode,'london');self.assertFalse(p.use_dsp)
+            np.testing.assert_array_equal(c.Mixture(['A','B'],p).lngamma_disp([.4,.6],298.15),[0.,0.])
+            self.assertGreater(abs(c.Mixture(['A','B'],z0).lngamma_disp([.4,.6],298.15)).max(),0.)
+
+    def test_constant_ES_never_uses_variable_dc_dx(self):
+        with engines() as (c,x,w,z0):
+            with patch.object(x.Z0xBinary,'_analytic',side_effect=AssertionError('wrong branch')):
+                self.assertTrue(np.isfinite(a.make_corner(['A','B'],'100').lngamma(298.15,[.3,.7])).all())
+
+    def test_hybrid_derivatives_from_excess_g(self):
+        with engines() as (c,x,w,z0):
+            for bits in a.CORNERS:
+                model=a.make_corner(['A','B'],bits);T=330.;xx=.37;h=2e-4
+                def g(t):
+                    if bits[0]=='0':
+                        mx=c.Mixture(['A','B'],model.z0.with_(A_ES=model._c(t)))
+                    else:mx=model
+                    return float(np.array([t,1-t])@mx.lngamma(T,[t,1-t]))
+                derivative=(g(xx-2*h)-8*g(xx-h)+8*g(xx+h)-g(xx+2*h))/(12*h)
+                expected=np.array([g(xx)+(1-xx)*derivative,g(xx)-xx*derivative])
+                np.testing.assert_allclose(model.lngamma(T,[xx,1-xx]),expected,atol=2e-6,rtol=0)
+
+    def test_contact_energy_gauge_cancels_in_pure_referenced_residual(self):
+        with engines() as (c,x,w,z0):
+            T=310.;weights=np.array([.37,.63]);fl=[c.load_fluid(k) for k in ('A','B')]
+            ps=np.array([f.psigA.ravel() for f in fl]);areas=ps.sum(1)
+            pm=weights@ps/(weights@areas)
+            W=c.delta_w(T,z0);u=np.linspace(-.15,.12,153)
+            def residual(W):
+                E=np.exp(-W/(c.R_KCAL*T));gm=np.log(c.solve_gamma(E,pm))
+                gp=np.array([np.log(c.solve_gamma(E,v/v.sum())) for v in ps])
+                return np.sum(ps*(gm-gp),axis=1)/z0.aeff
+            np.testing.assert_allclose(residual(W),residual(W+u[:,None]+u[None,:]),atol=2e-8,rtol=0)
+
+    def test_HB_mask_shared(self):
+        with engines() as (c,x,w,z0):
+            other=z0.with_(c_OH_OH=c.Params().c_OH_OH,c_OT_OT=c.Params().c_OT_OT,c_OH_OT=c.Params().c_OH_OT)
+            diff=c.delta_w(298.15,z0)-c.delta_w(298.15,other)
+            sig=np.tile(c.SIG,3);same=sig[:,None]*sig[None,:]>=0
+            np.testing.assert_array_equal(diff[same],np.zeros_like(diff[same]))
+            np.testing.assert_array_equal(diff[:51],np.zeros_like(diff[:51]))
+
+    def test_association_all_branches_restore_full_g(self):
+        with engines() as (c,x,w,z0):
+            class Descendant(w.Z0w2Binary):
+                def _ga(self,T,t):return .7*t*(1-t)*(1+.2*t)*298.15/T
+            for cls in (w.Z0wBinary,w.Z0w2Binary,Descendant):
+                obj=cls.__new__(cls)
+                if cls is not Descendant:obj._ga=types.MethodType(lambda self,T,t:.7*t*(1-t)*298.15/T,obj)
+                # Keep the real association _g and override only the residual data source.
+                with patch.object(x.Z0xBinary,'_g',lambda self,T,t:.2*t*(1-t)),\
+                     patch.object(obj,'_analytic',side_effect=AssertionError('association bypassed')),\
+                     patch.object(obj,'_endpoint',side_effect=AssertionError('P28 bypassed')):
+                    for flag,T,t in itertools.product(('0','1'),(278.15,350.),(0.,.00005,.0001,.3,.9999,.99995,1.)):
+                        with patch.dict(os.environ,{'ZC_R6_ENDPOINT':flag}):
+                            lo=max(0,t-obj.H);hi=min(1,t+obj.H)
+                            gp=(obj._g(T,hi)-obj._g(T,lo))/(hi-lo);g0=obj._g(T,t)
+                            expected=np.array([g0+(1-t)*gp,g0-t*gp])
+                            np.testing.assert_allclose(obj.lngamma(T,[t,1-t]),expected,rtol=0,atol=1e-12)
+                            self.assertAlmostEqual(float(np.array([t,1-t])@obj.lngamma(T,[t,1-t])),g0,places=12)
+                    self.assertAlmostEqual(obj.lngamma_inf(298.15,0),obj.lngamma(298.15,[0.,1.])[0],places=12)
+
+    def test_actual_site_mass_action_with_synthetic_strengths(self):
+        with engines() as (c,x,w,z0):
+            strengths={(dd,aa):18.+3*j for j,(dd,aa) in enumerate(itertools.product(w.DONORS,w.ACCEPTORS))}
+            with patch.object(w,'delta',return_value=strengths),\
+                 patch.object(w,'delta_liq',side_effect=lambda T,e:{k:v*(1+.002*e) for k,v in strengths.items()}):
+                for cls in (w.Z0wBinary,w.Z0w2Binary):
+                    obj=cls(['A','B'],['O','CO'])
+                    T=298.15;t=.31
+                    part=obj._ga(T,t)
+                    self.assertGreater(abs(part),1e-8)
+                    full=obj.lngamma(T,[t,1-t])
+                    original=obj._ga
+                    obj._ga=lambda T,x:0.
+                    without=obj.lngamma(T,[t,1-t])
+                    obj._ga=original
+                    dg=(original(T,t+obj.H)-original(T,t-obj.H))/(2*obj.H)
+                    np.testing.assert_allclose(full-without,[part+(1-t)*dg,part-t*dg],atol=2e-11,rtol=0)
+                    self.assertAlmostEqual(original(T,0.),0.,places=12)
+                    self.assertAlmostEqual(original(T,1.),0.,places=12)
+
+    def test_endpoint_error_is_historical_not_claimed_exact(self):
+        with engines() as (c,x,w,z0):
+            obj=w.Z0wBinary.__new__(w.Z0wBinary);obj._g=lambda T,t:2*t*(1-t)
+            for t,j in ((0.,0),(1.,1)):
+                self.assertAlmostEqual(obj.lngamma(300.,[t,1-t])[j],2*(1-obj.H),places=11)
+
+    def test_direct_g_override_descendant(self):
+        with engines() as (c,x,w,z0):
+            class Other(w.Z0wBinary):
+                def _g(self,T,t):return 1.5*t*(1-t)
+            obj=Other.__new__(Other)
+            np.testing.assert_allclose(obj.lngamma(300.,[.3,.7]),[1.5*.7**2,1.5*.3**2],atol=1e-11,rtol=0)
+
+
+class RunnerTests(unittest.TestCase):
+    def driver(self,tmp,bad_anchor=False,missing=False):
+        m,preds,value=fixture();root=Path(tmp);plan=root/'plan.json';r.d.write(plan,m)
+        out=root/'run';used=[]
+        def launch(cmd,log,seconds,env):
+            jid=cmd[cmd.index('--job')+1];job=next(j for j in m['jobs'] if j['id']==jid)
+            folder=Path(cmd[cmd.index('--out')+1]);folder.mkdir();used.append(job['corner'])
+            vals=[]
+            for n,i in enumerate(job['indices']):
+                row=m['rows'][i];r.d.write(folder/f'attempt-{n:04d}.json',dict(row_id=row['row_id'],attempted=True))
+                v=value(row,job['corner'])+(.01 if bad_anchor and job['corner']=='000' else 0)
+                if missing and job['corner']=='010' and n==0:v=None
+                vals.append(dict(row_id=row['row_id'],value=v,error=None))
+            r.d.write(folder/'result.json',dict(job=jid,corner=job['corner'],plan_sha256=r.d.sha(plan),
+                requested=len(vals),attempted=len(vals),values=vals,wall_s=.1))
+            return dict(state='returned',returncode=0)
+        m['inputs']={str(plan):r.d.sha(plan)}
+        args=argparse.Namespace(plan=str(plan),plan_commit='f'*40,out=str(out))
+        with patch.object(r,'load',return_value=(plan,m)),patch.object(r.old,'launch',side_effect=launch):
+            rc=r.run(args)
+            self.assertEqual(r.check(argparse.Namespace(plan=str(plan),plan_commit='f'*40,run=str(out))),rc)
+        return rc,m,plan,out,used
+
+    def test_complete_run_and_saved_check(self):
+        with tempfile.TemporaryDirectory() as tmp:
+            rc,m,p,out,used=self.driver(tmp)
+            self.assertEqual(rc,0);self.assertEqual(r.d.read(out/'summary.json')['attempted_model_calls'],48)
+            self.assertTrue(r.d.read(out/'public-errors.json')['status']['complete'])
+            self.assertEqual(len(used),16)
+
+    def test_anchor_blocks_all_six_intermediates(self):
+        with tempfile.TemporaryDirectory() as tmp:
+            rc,m,p,out,used=self.driver(tmp,bad_anchor=True)
+            self.assertEqual(rc,2);self.assertEqual(set(used),set(a.ANCHORS))
+            self.assertEqual(r.d.read(out/'summary.json')['attempted_model_calls'],12)
+            self.assertIsNone(r.d.read(out/'public-errors.json')['aggregate_errors'])
+
+    def test_nonfinite_row_not_removed(self):
+        with tempfile.TemporaryDirectory() as tmp:
+            rc,m,p,out,used=self.driver(tmp,missing=True);self.assertEqual(rc,2)
+            z=r.d.read(out/'public-errors.json');self.assertEqual(z['status']['requested_rows'],6)
+            self.assertIsNone(z['aggregate_errors'])
+
+    def test_changed_prediction_detected(self):
+        with tempfile.TemporaryDirectory() as tmp:
+            rc,m,p,out,used=self.driver(tmp);rp=out/'job-0000/result.json';z=r.d.read(rp);z['values'][0]['value']+=1
+            rp.write_text(json.dumps(z))
+            with patch.object(r,'load',return_value=(p,m)):
+                with self.assertRaises(ValueError):r.check(argparse.Namespace(plan=str(p),plan_commit='f'*40,run=str(out)))
+
+    def test_claim_prevents_repeat(self):
+        with tempfile.TemporaryDirectory() as tmp:
+            rc,m,p,out,used=self.driver(tmp)
+            with patch.object(r,'load',return_value=(p,m)):
+                with self.assertRaises(FileExistsError):r.run(argparse.Namespace(plan=str(p),plan_commit='f'*40,out=str(out)+'2'))
+
+    def test_row_order_mutation_detected(self):
+        with tempfile.TemporaryDirectory() as tmp:
+            rc,m,p,out,used=self.driver(tmp);rp=out/'job-0000/result.json';z=r.d.read(rp);z['values'].reverse();rp.write_text(json.dumps(z))
+            with self.assertRaises(ValueError):r.arrays(m,out,r.d.sha(p))
+
+    def test_worker_with_real_numerical_kernels_and_synthetic_profiles(self):
+        with tempfile.TemporaryDirectory() as tmp, engines() as (c,x,w,z0), patch.dict(os.environ):
+            root=Path(tmp);profiles={}
+            for key in ('A','B'):
+                fl=c.load_fluid(key);path=root/(key+'.sigma')
+                with path.open('w') as stream:
+                    stream.write('# synthetic test only\n')
+                    np.savetxt(stream,np.c_[np.tile(c.SIG,3),fl.psigA.ravel()],fmt='%.18e')
+                profiles[key]=str(path)
+            rows=[dict(row_id=str(i),c1='A',c2='B',system='A|B',T=310.,x1=t,P=100.,psat=[110.,70.])
+                  for i,t in enumerate((.2,.65))]
+            m=dict(rows=rows,jobs=r.jobs_for(rows),profiles=profiles,
+                   inputs=r.d.fingerprint(profiles.values()),worker_inputs={})
+            plan=root/'plan.json';r.d.write(plan,m);run=root/'run';run.mkdir()
+            r.d.write(root/'execution_claim.json',dict(plan_sha256=r.d.sha(plan),output=str(run)))
+            before=r.d.fingerprint(profiles.values())
+            for job in m['jobs']:
+                args=argparse.Namespace(plan=str(plan),plan_commit='f'*40,job=job['id'],out=str(run/job['id']))
+                with patch.object(r,'load',return_value=(plan,m)):
+                    r.worker(args)
+                result=r.d.read(run/job['id']/'result.json')
+                self.assertEqual(result['attempted'],2)
+                model=a.make_corner(['A','B'],job['corner'])
+                for row,v in zip(rows,result['values']):
+                    expected=r.old.pressure(model.lngamma(row['T'],[row['x1'],1-row['x1']]),row['x1'],row['psat'])
+                    self.assertAlmostEqual(v['value'],expected,places=11)
+            self.assertEqual(before,r.d.fingerprint(profiles.values()))
+
+    def test_actual_R14_archive_receipt_adapter(self):
+        with tempfile.TemporaryDirectory() as tmp:
+            root=Path(tmp);run=root/'run';run.mkdir();plan=root/'plan.json'
+            rows=[]
+            for j in range(100):
+                for k in range(10 if j<63 else 9):
+                    rows.append(dict(row_id=str(len(rows)),c1=f'A{j:03}',c2='B',system=f'A{j:03}|B',
+                        T=298.15,x1=.4,P=100.,archived_pred_P=112.,psat=[80.,110.]))
+            jobs=[]
+            for arm in r.old.ARMS:
+                for j in range(100):
+                    idx=[i for i,row in enumerate(rows) if row['c1']==f'A{j:03}']
+                    jobs.append(dict(id=f'job-{len(jobs):04d}',arm=arm,keys=[f'A{j:03}','B'],indices=idx))
+            m=dict(registration='a'*40,schema='r14-oracle-v1',design=r.old.DESIGN,environment=r.d.environment(),
+                inputs={},ingredient_manifest={'inputs':{}},exposure={'may_claim_unexposed':False},
+                protected_counts={'profiles_v2':630,'s1_stalled':1,'s2_stalled':5},rows=rows,jobs=jobs,census={})
+            r.d.write(plan,m);ph=r.d.sha(plan)
+            r.d.write(root/'execution_claim.json',dict(plan_sha256=ph,output=str(run)))
+            for job in jobs:
+                folder=run/job['id'];folder.mkdir();vals=[]
+                for j,i in enumerate(job['indices']):
+                    row=rows[i];r.d.write(folder/f'attempt-{j:04d}.json',dict(row_id=row['row_id'],attempted=True))
+                    vals.append(dict(row_id=row['row_id'],value=112.-r.old.ARMS.index(job['arm']),error=None))
+                r.d.write(folder/'result.json',dict(job=job['id'],arm=job['arm'],plan_sha256=ph,
+                    requested=len(vals),attempted=len(vals),values=vals))
+                r.d.write(run/(job['id']+'.terminal.json'),dict(job=job['id'],plan_sha256=ph,state='returned',returncode=0))
+            v,n,h=r.old.arrays(m,run,ph);ar=r.old.anchor_pass(rows,v[:,0]);q=r.old.error_summary(rows,v)
+            r.d.write(run/'summary.json',dict(plan_sha256=ph,anchor=ar,output_hashes=h,
+                attempted_model_calls=n,**q))
+            r.d.write(run/'public-errors.json',dict(status=q['status'],anchor=ar,aggregate_errors=q['aggregate_errors'],
+                census=m['census'],interpretation=r.old.DESIGN['result'],adopted=False,SCF_calls=0))
+            with patch.object(r.d,'registration'),patch.object(r,'ancestor'),patch.object(r,'git_bytes',return_value=(ph+'\n').encode()):
+                out,got,receipts,bridges=r.archive(str(plan),'b'*40,str(run),'c'*40)
+                self.assertEqual(got.shape,(963,3));self.assertEqual(len(out['rows']),963)
+                self.assertGreater(len(receipts),3000);self.assertEqual(bridges,[])
+                bad=run/'job-0000'/'attempt-0000.json';bad.write_text('{}')
+                with self.assertRaises(ValueError):r.archive(str(plan),'b'*40,str(run),'c'*40)
+
+    def test_only_explicit_source_bridge(self):
+        with tempfile.TemporaryDirectory() as tmp:
+            root=Path(tmp);src=root/r.ASSOC;src.parent.mkdir(parents=True);src.write_bytes(b'new')
+            expected=__import__('hashlib').sha256(b'old').hexdigest()
+            with patch.object(r,'ROOT',root),patch.object(r,'git_bytes',side_effect=lambda commit,rel:b'old' if commit==r.BASE else b'new'):
+                self.assertEqual(len(r.check_old_inputs({str(src):expected},'c'*40)),1)
+                other=root/'other.dat';other.write_bytes(b'new')
+                with self.assertRaises(ValueError):r.check_old_inputs({str(other):expected},'c'*40)
+
+    def test_private_output_cannot_enter_git(self):
+        with tempfile.TemporaryDirectory() as tmp:
+            root=Path(tmp);(root/'.git').mkdir()
+            with self.assertRaises(ValueError):r.d.private(root/'out',True)
+
+    def test_public_allowlist_has_no_rows(self):
+        m,p,_=fixture();q=a.summary(m['rows'],p,True);pub=r.public(q,{'passed':True})
+        self.assertNotIn('private_rows',pub);self.assertNotIn('profiles',pub)
+        self.assertNotIn('row_id',json.dumps(pub))
+
+    def test_timeout_is_terminal(self):
+        with tempfile.TemporaryDirectory() as tmp:
+            z=r.old.launch([sys.executable,'-c','import time; time.sleep(2)'],Path(tmp)/'log',.03,dict(os.environ))
+            self.assertEqual(z['state'],'timeout')
+
+if __name__=='__main__':unittest.main()
```
<!-- END PATCH H15 -->

<!-- BEGIN PATCH P54 -->
```diff
diff --git a/scripts/r15_factorial.py b/scripts/r15_factorial.py
new file mode 100644
--- /dev/null
+++ b/scripts/r15_factorial.py
@@ -0,0 +1,313 @@
+"""Mac-only R15 fitted-ingredient attribution on the exact archived P52 rows.
+
+No QC, sampling, profile generation, parameter fitting, or production writes.
+The archived R14 controls are audited separately from the new factorial.
+"""
+from __future__ import annotations
+import argparse
+import hashlib
+import os
+from pathlib import Path
+import re
+import subprocess
+import sys
+import time
+import numpy as np
+import r14_dielectric as d
+import r14_oracle as old
+import r15_math as a
+
+ROOT = d.ROOT
+BASE = '3cd0a22888b40699d5f4994f5ba2e5cd274703df'
+MARKER = 'R15-P54-P55-P56: contact attribution, association dispatch, and manuscript scope'
+FILES = ('scripts/r15_math.py', 'scripts/r15_factorial.py', 'scripts/r15_selftest.py')
+ASSOC = 'src/zcosmo/z0w.py'
+DESIGN = dict(rows=963, systems=100, factors=list(a.FACTORS), active_corners=list(a.CORNERS),
+    order=list(a.ANCHORS+a.INTERMEDIATE), shared_aeff=7.25,
+    source='original private P52 plan and completed run',
+    baseline='stored-epsilon Z0x', target='COSMO-SAC 2010 without explicit dispersion',
+    requests=7704, anchors=1926, remaining=5778, seconds_per_worker=120,
+    driver_seconds=7200, workers_in_parallel=1, anchor_relative_tolerance=1e-8,
+    adopted=False, QC_calls=0, scoring='exposed retrospective ThermoML diagnostic',
+    no_new_subset=True, no_tuning=True, no_retries=True)
+
+
+def git_bytes(commit, rel):
+    return subprocess.check_output(['git', 'show', commit+':'+rel], cwd=ROOT)
+
+
+def ancestor(commit, child='HEAD'):
+    d.require(re.fullmatch(r'[0-9a-f]{40}', commit) is not None, 'Use full commit identity')
+    subprocess.run(['git','merge-base','--is-ancestor',commit,child], cwd=ROOT,
+                   check=True, capture_output=True)
+
+
+def registration(commit):
+    ancestor(commit); ancestor(BASE, commit)
+    d.require(MARKER in git_bytes(commit, 'PREREGISTRATION.md').decode(), 'R15 registration absent')
+    for rel in (*FILES, ASSOC):
+        d.require((ROOT/rel).read_bytes() == git_bytes(commit, rel), 'Unregistered source drift: '+rel)
+    for rel in ('src/zcosmo/cosmosac.py','src/zcosmo/z0x.py',
+                'src/zcosmo/zmodel.py','src/zcosmo/models.py',
+                'results/z_params/Z0.json','results/qc/dielectric.csv',
+                'results/qc/dispersion.csv'):
+        d.require((ROOT/rel).read_bytes() == git_bytes(BASE,rel),
+                  'Participating model source differs from reviewed main: '+rel)
+    return commit
+
+
+def check_old_inputs(saved, reg):
+    """One explicit nonparticipant-source bridge, not a weakened R14 checker.
+
+    P55 changes z0w.py. P52 did not call it. All old data and all participating
+    model sources must still match. The old R14 check remains unmodified.
+    """
+    bridges=[]
+    for name, expected in saved.items():
+        p=Path(name).resolve()
+        if d.sha(p) == expected:
+            continue
+        d.require(p == (ROOT/ASSOC).resolve(), 'Historical input mutation: '+p.name)
+        original=git_bytes(BASE,ASSOC)
+        d.require(hashlib.sha256(original).hexdigest() == expected,
+                  'Historical association file was not the reviewed baseline')
+        d.require(p.read_bytes() == git_bytes(reg,ASSOC), 'Association repair differs from registration')
+        bridges.append(dict(relative_path=ASSOC, old_sha256=expected, new_sha256=d.sha(p),
+                            scope='not invoked by P52 or P54'))
+    return bridges
+
+
+def archive(plan, plan_commit, run, reg):
+    """Replay only archived hashes/arithmetic. Never call an activity model."""
+    p=d.private(plan); rp=d.private(run); m=d.read(p)
+    d.registration(m['registration']); ancestor(plan_commit)
+    ancestor(m['registration'], plan_commit)
+    d.require(git_bytes(plan_commit,'docs/astra/round14/ORACLE_PLAN_SHA256.txt').decode().strip()==d.sha(p),
+              'Wrong R14 plan digest')
+    d.require(m['schema']=='r14-oracle-v1' and m['design']==old.DESIGN,
+              'Unexpected R14 design')
+    d.require(m['environment']==d.environment(), 'R14 environment changed')
+    bridges=check_old_inputs(m['inputs'],reg)
+    bridges+=check_old_inputs(m['ingredient_manifest']['inputs'],reg)
+    d.require(m['exposure']['may_claim_unexposed'] is False and
+              m['protected_counts']=={'profiles_v2':630,'s1_stalled':1,'s2_stalled':5},
+              'Historical exposure or protected selection changed')
+    d.require(d.read(p.parent/'execution_claim.json')==dict(plan_sha256=d.sha(p),output=str(rp)),
+              'Different R14 claimed run')
+    v,n,h=old.arrays(m,rp,d.sha(p)); z=d.read(rp/'summary.json')
+    ar=old.anchor_pass(m['rows'],v[:,0]); fresh=old.error_summary(m['rows'],v)
+    d.require(ar['passed'] and fresh['status']['complete'] and n==2889,
+              'R14 is not the completed 2889-request result')
+    d.require(z['plan_sha256']==d.sha(p) and z['anchor']==ar and z['output_hashes']==h and
+              z['attempted_model_calls']==n and z['status']==fresh['status'] and
+              z['aggregate_errors']==fresh['aggregate_errors'], 'R14 summary changed')
+    expected=dict(status=fresh['status'],anchor=ar,aggregate_errors=fresh['aggregate_errors'],
+                  census=m['census'],interpretation=old.DESIGN['result'],adopted=False,SCF_calls=0)
+    d.require(d.read(rp/'public-errors.json')==expected, 'R14 public receipt changed')
+    # Identity counts come from a completed private plan, not rounded public tables.
+    rows=m['rows']; ids=[r['row_id'] for r in rows]
+    d.require(len(rows)==963 and len(set(ids))==963 and len({r['system'] for r in rows})==100,
+              'Not the requested 963-row/100-system universe')
+    for r in rows:
+        d.require(250<=r['T']<=450 and 0<r['P']<=500 and 1e-4<r['x1']<1-1e-4,
+                  'P52 query outside its stated scope; no silent removal')
+        d.require(r['system']=='|'.join(sorted((r['c1'],r['c2']))) and r['c1']!=r['c2'],
+                  'Historical pair identity changed')
+        d.require(np.isfinite(r['psat']).all() and min(r['psat'])>0, 'Invalid saved psat')
+    receipts=dict(h)
+    receipts.update(d.fingerprint([p,p.parent/'execution_claim.json',rp/'summary.json',rp/'public-errors.json']))
+    receipts.update({name:d.sha(name) for name in m['inputs']})
+    receipts.update({name:d.sha(name) for name in m['ingredient_manifest']['inputs']})
+    return m,v,receipts,bridges
+
+
+def jobs_for(rows):
+    pairs=sorted({(r['c1'],r['c2']) for r in rows}); jobs=[]
+    for corner in a.ANCHORS+a.INTERMEDIATE:
+        for pair in pairs:
+            idx=[i for i,r in enumerate(rows) if (r['c1'],r['c2'])==pair]
+            jobs.append(dict(id=f'job-{len(jobs):04d}',corner=corner,keys=list(pair),indices=idx))
+    d.require(sum(len(j['indices']) for j in jobs)==8*len(rows), 'Request count mismatch')
+    return jobs
+
+
+def freeze(args):
+    d.mac();reg=registration(args.registration)
+    previous,values,inputs,bridges=archive(args.r14_plan,args.r14_plan_commit,args.r14_run,reg)
+    from zcosmo.cosmosac import Params
+    params=d.read(ROOT/'results/z_params/Z0.json')['params']
+    params['disp_override']=tuple(tuple(v) for v in params.get('disp_override',()))
+    audit=a.shared_audit(Params(**params),Params(use_dsp=False))
+    sources=[*list((ROOT/'src/zcosmo').glob('*.py')),
+             *(ROOT/rel for rel in FILES),ROOT/'scripts/r14_dielectric.py',
+             ROOT/'scripts/r14_oracle.py',ROOT/'scripts/r14_selftest.py']
+    sources+= [ROOT/'results/z_params/Z0.json',ROOT/'results/qc/dispersion.csv',ROOT/'results/qc/dielectric.csv']
+    worker_inputs=d.fingerprint(sources);inputs.update(worker_inputs)
+    rows=previous['rows'];jobs=jobs_for(rows)
+    d.require(sum(len(j['indices']) for j in jobs)==DESIGN['requests'], 'Fixed budget changed')
+    out=d.private(args.out,True)
+    m=dict(schema='r15-factorial-v1',base=BASE,registration=reg,design=DESIGN,
+        environment=d.environment(),inputs=inputs,worker_inputs=worker_inputs,
+        archive=dict(plan=str(d.private(args.r14_plan)),plan_commit=args.r14_plan_commit,
+                     run=str(d.private(args.r14_run))),
+        source_bridge=bridges,rows=rows,jobs=jobs,profiles=previous['profiles'],
+        prior_anchors=values[:,[0,2]].tolist(),shared_audit=audit,
+        protected_counts=previous['protected_counts'],exposure=previous['exposure'])
+    d.check_inputs(inputs);d.write(out/'plan.json',m)
+    (out/'PLAN_SHA256.txt').write_text(d.sha(out/'plan.json')+'\n')
+    print('R15 private plan frozen: 963 rows; 7704 requests; no new model calls.')
+
+
+def load(plan,commit,full=True):
+    d.mac();p=d.private(plan);m=d.read(p);registration(m['registration'])
+    ancestor(commit);ancestor(m['registration'],commit)
+    d.require(git_bytes(commit,'docs/astra/round15/PLAN_SHA256.txt').decode().strip()==d.sha(p),
+              'Uncommitted or altered R15 plan')
+    d.require(m['schema']=='r15-factorial-v1' and m['base']==BASE and m['design']==DESIGN,
+              'R15 design changed')
+    d.require(m['environment']==d.environment(), 'Package environment drift')
+    d.require(m['jobs']==jobs_for(m['rows']) and len(m['rows'])==DESIGN['rows'], 'Job identity drift')
+    d.check_inputs(m['inputs'] if full else m['worker_inputs'])
+    return p,m
+
+
+def worker(args):
+    p,m=load(args.plan,args.plan_commit,False)
+    job=next(j for j in m['jobs'] if j['id']==args.job)
+    claim=d.read(p.parent/'execution_claim.json');out=d.private(args.out)
+    d.require(claim['plan_sha256']==d.sha(p) and out==Path(claim['output'])/job['id'],
+              'Worker outside the single claimed run')
+    for k in job['keys']:
+        d.require(d.sha(m['profiles'][k])==m['inputs'][str(Path(m['profiles'][k]).resolve())],
+                  'Frozen profile changed')
+    out=d.private(out,True)
+    for k in list(os.environ):
+        if k.startswith('ZC_'):os.environ.pop(k)
+    ov=out/'overlay';ov.mkdir(mode=0o700)
+    for key in job['keys']:(ov/(key+'.sigma')).symlink_to(Path(m['profiles'][key]))
+    os.environ['ZC_SIGMA_OVERRIDE_DIR']=str(ov);os.environ['ZC_R6_ENDPOINT']='1'
+    from zcosmo.cosmosac import load_fluid,sigma_path,SIG
+    for key in job['keys']:
+        d.require(sigma_path(key).resolve()==Path(m['profiles'][key]).resolve(), 'Unexpected fallback profile')
+        fl=load_fluid(key);raw=np.loadtxt(m['profiles'][key])
+        d.require(raw.shape==(153,2) and np.allclose(raw[:,0],np.tile(SIG,3),rtol=0,atol=1e-12)
+                  and np.isfinite(raw).all() and (raw[:,1]>=0).all()
+                  and np.array_equal(fl.psigA.ravel(),raw[:,1]) and fl.A>0 and fl.V>0,
+                  'Invalid or mismatched stored sigma grid')
+    model=a.make_corner(job['keys'],job['corner']);vals=[];start=time.monotonic()
+    for i in job['indices']:
+        r=m['rows'][i];value=None;error=None
+        d.write(out/f'attempt-{len(vals):04d}.json',dict(row_id=r['row_id'],attempted=True))
+        try:value=old.pressure(model.lngamma(r['T'],np.array([r['x1'],1-r['x1']])),r['x1'],r['psat'])
+        except Exception as ex:error=type(ex).__name__
+        vals.append(dict(row_id=r['row_id'],value=value,error=error))
+    d.check_inputs(m['worker_inputs'])
+    d.check_inputs({str(Path(m['profiles'][k]).resolve()):m['inputs'][str(Path(m['profiles'][k]).resolve())]
+                    for k in job['keys']})
+    d.write(out/'result.json',dict(job=job['id'],corner=job['corner'],plan_sha256=d.sha(p),
+        requested=len(job['indices']),attempted=len(vals),values=vals,wall_s=time.monotonic()-start))
+
+
+def arrays(m,run,plan_hash):
+    run=Path(run);values=np.full((len(m['rows']),8),np.nan);hashes={};attempts=0
+    for job in m['jobs']:
+        tp=run/(job['id']+'.terminal.json');term=d.read(tp);hashes.update(d.fingerprint([tp]))
+        d.require(term['job']==job['id'] and term['plan_sha256']==plan_hash, 'Terminal identity changed')
+        folder=run/job['id'];started=sorted(folder.glob('attempt-*.json'))
+        expected=[m['rows'][i]['row_id'] for i in job['indices']]
+        d.require(len(started)<=len(expected), 'Query ceiling exceeded')
+        for j,sp in enumerate(started):
+            d.require(sp.name==f'attempt-{j:04d}.json' and
+                d.read(sp)==dict(row_id=expected[j],attempted=True), 'Attempt receipt changed')
+        attempts+=len(started);hashes.update(d.fingerprint(started));rp=folder/'result.json'
+        if term['state']!='returned' or term['returncode']!=0 or not rp.is_file():continue
+        z=d.read(rp);hashes.update(d.fingerprint([rp]))
+        d.require(z['job']==job['id'] and z['corner']==job['corner'] and z['plan_sha256']==plan_hash
+                  and z['attempted']==z['requested']==len(expected)==len(started)
+                  and [v['row_id'] for v in z['values']]==expected, 'Worker result identity changed')
+        for i,v in zip(job['indices'],z['values']):
+            if v['value'] is not None:values[i,a.CORNERS.index(job['corner'])]=float(v['value'])
+    d.require(attempts<=DESIGN['requests'], 'R15 request ceiling exceeded')
+    return values,attempts,hashes
+
+
+def anchor(m,values):
+    now=np.asarray(values)[:,[0,7]];prior=np.asarray(m['prior_anchors'],float)
+    d.require(now.shape==prior.shape and np.isfinite(prior).all() and (prior>0).all(), 'Invalid archived anchors')
+    finite=np.isfinite(now)&(now>0)
+    with np.errstate(over='ignore', invalid='ignore'):
+        relative=abs(now/prior-1)
+    err=float(np.max(relative)) if finite.all() and np.isfinite(relative).all() else None
+    return dict(passed=bool(err is not None and err<DESIGN['anchor_relative_tolerance']),
+        requested=int(now.size),finite=int(finite.sum()),max_relative_pressure_error=err)
+
+
+def public(result,ar):
+    return dict(status=result['status'],anchors=ar,aggregate_errors=result['public_errors'],
+        adopted=False,QC_calls=0,interpretation='retrospective fitted-ingredient diagnostic; not a selected model')
+
+
+def collect(args):
+    start=time.monotonic();p,m=load(args.plan,args.plan_commit);run=d.private(args.run)
+    d.require(d.read(p.parent/'execution_claim.json')==dict(plan_sha256=d.sha(p),output=str(run)), 'Run claim changed')
+    v,n,h=arrays(m,run,d.sha(p));ar=anchor(m,v);q=a.summary(m['rows'],v,ar['passed'])
+    d.check_inputs(m['inputs'])
+    z=dict(plan_sha256=d.sha(p),attempted_model_calls=n,anchors=ar,
+           status=q['status'],public_errors=q['public_errors'],output_hashes=h,
+           collection_wall_s=time.monotonic()-start,QC_calls=0,source_profiles_unchanged=True)
+    d.write(run/'private-rows.json',q['private_rows']);d.write(run/'summary.json',z)
+    d.write(run/'public-errors.json',public(q,ar))
+    print('R15 saved result complete:',q['status']['complete'])
+    return 0 if q['status']['complete'] else 2
+
+
+def run(args):
+    p,m=load(args.plan,args.plan_commit);out=d.private(args.out)
+    d.write(p.parent/'execution_claim.json',dict(plan_sha256=d.sha(p),output=str(out)))
+    out=d.private(out,True);start=time.monotonic();env=dict(os.environ)
+    env.update(OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1')
+    for j in m['jobs']:
+        d.write(out/(j['id']+'.terminal.json'),dict(job=j['id'],plan_sha256=d.sha(p),state='not_started',returncode=None))
+    ar=None
+    for j in m['jobs']:
+        if j['corner'] not in a.ANCHORS and ar is None:
+            v,_,_=arrays(m,out,d.sha(p));ar=anchor(m,v)
+        remain=DESIGN['driver_seconds']-(time.monotonic()-start)
+        term=dict(job=j['id'],plan_sha256=d.sha(p),state='not_run_budget',returncode=None)
+        if j['corner'] not in a.ANCHORS and not ar['passed']:term['state']='blocked_anchors'
+        elif remain>1:
+            cmd=[sys.executable,str(Path(__file__).resolve()),'_worker','--plan',str(p),
+                 '--plan-commit',args.plan_commit,'--job',j['id'],'--out',str(out/j['id'])]
+            try:term.update(old.launch(cmd,out/(j['id']+'.log'),min(remain,DESIGN['seconds_per_worker']),env))
+            except Exception:term.update(state='launch_failed')
+        tmp=out/(j['id']+'.terminal.tmp');d.write(tmp,term);os.replace(tmp,out/(j['id']+'.terminal.json'))
+    d.write(out/'timing.json',dict(model_run_wall_s=time.monotonic()-start))
+    return collect(argparse.Namespace(plan=args.plan,plan_commit=args.plan_commit,run=str(out)))
+
+
+def check(args):
+    p,m=load(args.plan,args.plan_commit);run=d.private(args.run);z=d.read(run/'summary.json')
+    d.require(d.read(p.parent/'execution_claim.json')==dict(plan_sha256=d.sha(p),output=str(run)), 'Run claim changed')
+    v,n,h=arrays(m,run,d.sha(p));ar=anchor(m,v);q=a.summary(m['rows'],v,ar['passed'])
+    d.require(z['plan_sha256']==d.sha(p) and z['attempted_model_calls']==n and z['anchors']==ar
+        and z['status']==q['status'] and z['public_errors']==q['public_errors'] and z['output_hashes']==h,
+        'Saved R15 result changed')
+    d.require(d.read(run/'private-rows.json')==q['private_rows'] and
+              d.read(run/'public-errors.json')==public(q,ar), 'Derived output changed')
+    print('R15 checked without new activity calls. Complete:',q['status']['complete'])
+    return 0 if q['status']['complete'] else 2
+
+
+def main():
+    p=argparse.ArgumentParser(description=__doc__);sp=p.add_subparsers(dest='cmd',required=True)
+    q=sp.add_parser('freeze');q.add_argument('--registration',required=True)
+    q.add_argument('--r14-plan',required=True);q.add_argument('--r14-plan-commit',required=True)
+    q.add_argument('--r14-run',required=True);q.add_argument('--out',required=True);q.set_defaults(fn=freeze)
+    for name,fn in (('run',run),('collect',collect),('check',check),('_worker',worker)):
+        q=sp.add_parser(name);q.add_argument('--plan',required=True);q.add_argument('--plan-commit',required=True)
+        q.add_argument('--run' if name in ('collect','check') else '--out',required=True)
+        if name=='_worker':q.add_argument('--job',required=True)
+        q.set_defaults(fn=fn)
+    args=p.parse_args();return args.fn(args)
+
+if __name__=='__main__':raise SystemExit(main())
```
<!-- END PATCH P54 -->

<!-- BEGIN PATCH P55 -->
```diff
diff --git a/src/zcosmo/z0w.py b/src/zcosmo/z0w.py
--- a/src/zcosmo/z0w.py
+++ b/src/zcosmo/z0w.py
@@ -126,6 +126,20 @@
         self.Vm = np.array([load_fluid(k).V for k in keys])
         self._pure = {}
 
+    def lngamma(self, T, x):
+        """R15: restore differentiation of the full subclass excess Gibbs energy.
+
+        This is the pre-P6 stencil, including its one-sided endpoint error.
+        P28 is exact for Z0x only; it must not bypass an association override.
+        Z0x itself retains its optimized derivative and accepted endpoint path.
+        """
+        x1 = float(x[0])
+        h = self.H
+        a, b = max(x1 - h, 0.0), min(x1 + h, 1.0)
+        dg = (self._g(T, b) - self._g(T, a)) / (b - a)
+        g = self._g(T, x1)
+        return np.array([g + (1 - x1) * dg, g - x1 * dg])
+
     def _ga(self, T, x1):
         D = delta(T)
         key = round(T, 6)
```
<!-- END PATCH P55 -->

<!-- BEGIN PATCH P56 -->
```diff
diff --git a/manuscript/draft.md b/manuscript/draft.md
--- a/manuscript/draft.md
+++ b/manuscript/draft.md
@@ -1,33 +1,39 @@
-# How far can COSMO-SAC go without fitted constants? A pre-registered benchmark on NIST ThermoML data
-
-Victor Liang (draft, 2026-09-24)
+# Replacing COSMO-SAC interaction constants without ThermoML regression: a pre-registered benchmark
+
+Victor Liang (original draft 2026-09-24; evidence and scope updated 2026-10-08)
 
 ## Abstract
 
-Predictive activity-coefficient models such as COSMO-SAC avoid binary interaction parameters, yet every
-variant in use still fits 8 to 15 universal constants to experimental phase-equilibrium data. We ask how
-much accuracy is lost when each of those constants is replaced by a number computed from theory or
-quantum chemistry. In the resulting model, Z0, the electrostatic misfit coefficient follows from Klamt's
+COSMO-SAC replaces binary-specific regression with molecular surface profiles and shared interaction
+parameters. We ask how much accuracy is retained when its electrostatic and hydrogen-bond coefficients
+and dispersion prescription are supplied by theory or quantum chemistry without regression to ThermoML. In the resulting model, Z0, the electrostatic misfit coefficient follows from Klamt's
 estimate in the conductor limit, the three hydrogen-bond constants come from 17 counterpoise-corrected
 B3LYP-D4/def2-TZVP dimer energies, and dispersion enters through a London term built from D4 molecular
-C6 coefficients and polarizabilities. No experimental thermodynamic data are used anywhere in Z0.
+C6 coefficients and polarizabilities. Z0 and Z0x do not regress their interaction constants to the
+ThermoML benchmark. They retain the standard effective area and combinatorial normalization constants,
+along with inherited profile-processing conventions. UD reference geometries have documented empirical
+selection history, and VLE uses experimental pure-component vapor-pressure correlations. The claim is
+therefore absence of new benchmark regression, not absence of every empirical upstream input.
 
 We score Z0, two dielectric-screening refinements (Z0e, Z0x), COSMO-SAC 2010, COSMO-SAC-dsp and
 modified UNIFAC (Dortmund) on a benchmark built from 9,184 ThermoML files (3,438 infinite-dilution
 activity coefficients, 46,127 VLE, 7,158 LLE and 27,366 excess-enthalpy points), with a molecule-level
 held-out split frozen before any model was run, and on a temporal set of 2017 to 2019 publications that
-postdate the fits of all reference models. HANNA, a neural model trained on 824k Dortmund Data Bank
-points, is included as a data-driven reference.
+provide an additional historical collection. HANNA is included as a data-driven reference, with possible
+training overlap. The original split was frozen prospectively, but later model development examined both
+collections repeatedly; subsequent explanatory analyses do not constitute new untouched validation.
 
 On held-out molecules Z0 matches COSMO-SAC 2010 for infinite-dilution activity coefficients (MAE in
 ln gamma 0.76 vs 0.82, difference not significant) and detects liquid-liquid demixing more reliably than
 both COSMO-SAC and UNIFAC (balanced accuracy 0.90 vs 0.84 and 0.81, significant). It is clearly worse for
 bubble pressures (AAD 18.8% vs 8.6%) and on the temporal set. The DFT-derived hydrogen-bond constants are
 nearly identical across the three COSMO-SAC classes (about 5,700 kcal A^4 mol^-1 e^-2), whereas the fitted
-constants span 4,014 to 932. Ablations trace most of the remaining error to one term, the electrostatic
-misfit in the conductor limit: no single screening strength serves dilute and concentrated mixtures at
-once. Composition-dependent screening derived from first-principles permittivities (Z0x) recovers part of
-the gap (VLE AAD 14.2%) without any fitted number, keeping the IDAC and LLE results. HANNA, where its
+constants span 4,014 to 932. Earlier one-term ablations identify the electrostatic prescription as an
+important sensitivity. Composition-dependent screening in Z0x reduces the historical VLE AAD to 14.2%.
+A later retrospective diagnostic on a separate 963-row subset changes AAD from 13.78% to 13.07% when
+experimental pure-liquid permittivities replace the stored estimates, versus 10.44% for COSMO-SAC 2010.
+This small bulk-permittivity effect leaves the local contact approximation as an unresolved hypothesis,
+not an established universal cause or an accepted new coefficient. HANNA, where its
 training data reach, is far more accurate than every physics-based model, but it does not detect demixing
 more reliably than Z0 on held-out molecules.
 
@@ -42,9 +48,8 @@
 structure is known. Their interaction model, however, still carries a small set of universal constants
 (an effective contact area, the electrostatic misfit coefficient and its temperature dependence,
 hydrogen-bond strengths and cutoffs, and in later versions dispersion parameters) that are fitted to
-experimental infinite-dilution activity coefficients and phase equilibria. Recent work has refit these
-constants at higher levels of quantum chemistry and extended the framework to an equation of state,
-always by regression against experiment.
+experimental infinite-dilution activity coefficients and phase equilibria. Published variants have refit shared parameters for different electronic-structure recipes. Their
+reported accuracy must therefore be distinguished from that of the present no-new-regression variants.
 
 Data-driven models have meanwhile become very accurate. HANNA, a thermodynamically consistent neural
 network trained on about 824,000 Dortmund Data Bank points, outperforms modified UNIFAC across binary
@@ -53,11 +58,11 @@
 
 That case is only as strong as the physics is real. If COSMO-SAC's accuracy is carried mainly by its
 fitted constants, it is a compact regression model; if it is carried by the sigma profiles, the constants
-should be computable. We test this directly. We replace every fitted constant of COSMO-SAC by a value
-from theory or quantum chemistry, pre-register the benchmark and the metrics, and score the result
-against fitted COSMO-SAC, modified UNIFAC and HANNA on held-out molecules and on data published after
-the reference models were fitted. We then use ablations to find which physical term carries the
-remaining error.
+may admit more transferable physical estimates. We test specified replacements of the interaction
+constants and dispersion model, while retaining the common molecular-surface and combinatorial
+conventions. The benchmark and initial metrics were registered before predictions. Subsequent changes
+were registered before their own execution, with prior exposure stated. Ablations identify conditional
+model sensitivities; they do not uniquely identify a missing physical mechanism.
 
 ## 2. Methods
 
@@ -74,7 +79,11 @@
 prediction. A temporal set was built later from the complete NIST 2020 archive (11,923 files, standard
 InChIKeys): rows from files absent from the 2017 mirror, i.e. publications from mid-2017 to 2019. These
 postdate the fitting of COSMO-SAC 2010 (2010), COSMO-SAC-dsp (2014) and the UNIFAC parameter table used
-(2016). HANNA's training data very likely include them.
+(2016). This is the historical provenance description of those parameter tables, not proof that every
+reference model or upstream input is unexposed to these measurements. HANNA may overlap these data.
+Neither this temporal collection nor the repeatedly examined compound test split is a fresh holdout for
+R10-R15 development. A future validation needs a custodian-led source and duplicate-series audit before
+responses are revealed; relabeling an existing split cannot restore independence.
 
 ### 2.2 Reference models
 COSMO-SAC 2010 and -dsp were reimplemented in NumPy and reproduce the NIST benchmark code (Bell et al.,
@@ -83,9 +92,12 @@
 automatic group assignment (`ugropy`). HANNA is the published ensemble (Nat. Commun. 2026).
 
 ### 2.3 The Z0 model
-(Equations to typeset.) Effective segment area a_eff = pi r_av^2 = 7.25 A^2, a geometric identity with the
-profile-averaging radius. Electrostatic misfit c_ES = alpha'/2 with alpha' = 0.3 a_eff^1.5 / eps0 in the
-conductor limit (12,226 kcal A^4 mol^-1 e^-2; the fitted 2010 value at 298 K is 8,197). Hydrogen bonding:
+Both the stored Z0 recipe and the 2010 reference retain a_eff = 7.25 A^2, q0 = 79.53, r0 = 66.69 and
+z = 10. These are common inherited conventions in this implementation; no independent derivation of the
+numerical effective area is established by calling it a geometric identity. The stored NHB/OH/OT split
+and its processing rules are also shared. Electrostatic misfit c_ES = alpha'/2 with
+alpha' = 0.3 a_eff^1.5 / eps0 in the
+conductor limit (12,226 kcal A^4 mol^-1 e^-2; the fitted 2010 value at 298.15 K is 8,197). Hydrogen bonding:
 for each dimer, E_HB = c_ES (s_D + s_A)^2 - c_hb (s_D - s_A)^2 with s_D, s_A the mean charge density of the
 most extreme a_eff of the donor and acceptor profiles; E_HB is the counterpoise-corrected B3LYP/def2-TZVP
 binding energy including monomer deformation, with the D4 dispersion part removed. Dispersion: London
@@ -96,9 +108,13 @@
 Refinements registered after the first results, before their own predictions:
 Z0e scales c_ES by the COSMO dielectric factor f = (eps - 1)/(eps + 1/2) with eps from Onsager's equation
 (GFN2-xTB dipoles, D4 polarizabilities, COSMO volumes), arithmetic mean over the pair. Z0x lets eps follow
-the mixture composition (volume-fraction average) and derives ln gamma_i from the resulting g^E by
-numerical differentiation, so Gibbs-Duhem holds exactly. Z0s picks one of six dielectric variants on the
-training split only (it chose the optical permittivity n^2 with a harmonic mean).
+the mixture composition (volume-fraction average) and defines an excess Gibbs energy from which
+chemical potentials are differentiated. This construction is thermodynamically consistent analytically;
+finite-difference implementation errors are assessed separately. The accepted P6 implementation uses an
+analytic interior derivative. P28 supplies the exact pure endpoint of Z0x's same excess-Gibbs model when
+ZC_R6_ENDPOINT=1; the adjacent finite-difference strip remains a distinct numerical approximation.
+Historical tables below retain their original source versions and endpoint conventions. Z0s made one
+train-selected choice among six dielectric variants (optical n^2, harmonic mean) and is labeled accordingly.
 
 ### 2.4 Protocol
 Metrics: MAE in ln gamma_inf; AAD in bubble pressure at measured T and x with the same pure-component
@@ -109,13 +125,22 @@
 counts when the paired interval excludes zero. Pre-registration and every later change are in
 `PREREGISTRATION.md`.
 
+Later read-only and explanatory rounds retain their own exact observation identities, common inputs
+and requested denominators. Their exposure, failures and amendments are recorded separately. Bootstrap
+intervals from the original tables do not remove later adaptive exposure. LLE split detection and checked
+endpoint compositions have separate denominators; neither is a global phase-equilibrium certificate.
+
 ## 3. Results
 
 Figures: `figures/fig1_idac_parity_test.png` (parity, held-out molecules), `figures/fig2_hbond_constants.png`,
 `figures/fig3_tradeoff.png` (IDAC vs VLE error), `figures/fig4_lle_detection.png`,
 `figures/fig5_error_map.png` (Z0x minus COSMO-SAC error by chemical family).
 
-### 3.1 Held-out molecules (test split)
+### 3.1 Historical compound-test results
+
+These are the original main7 comparisons, preserved rather than regenerated with later code. See
+`results/scorecard_test_main7.md` and its source-specific common subsets. Later explanatory scores must
+not be subtracted from these values when their observation sets or numerical versions differ.
 
 | Model | IDAC MAE | IDAC, both unseen | VLE AAD P % (median) | H^E MAE J/mol | LLE balanced accuracy |
 |---|---|---|---|---|---|
@@ -125,7 +150,7 @@
 | Z0 | 0.76 | 0.53 | 18.8 (6.2) | 532 | 0.90 |
 | Z0e | 0.79 | 0.57 | 15.7 (4.6) | 521 | 0.90 |
 | Z0s (one choice on train) | 0.95 | 1.00 | 12.8 (4.2) | 571 | 0.70 |
-| Z0x (no fitted constants, no choices) | 0.76 | 0.55 | 14.2 (4.5) | 522 | 0.90 |
+| Z0x (no new ThermoML parameter regression) | 0.76 | 0.55 | 14.2 (4.5) | 522 | 0.90 |
 | HANNA (trained on DDB, reference) | 0.24* | 0.24* | 7.1 (2.1)* | 70* | 0.88 |
 
 IDAC: 708 points in 163 systems (both unseen: 55 points, 12 systems). VLE: 9,432 points. LLE: 101
@@ -152,8 +177,8 @@
 | Z0s | 1.08 (0.41) | 8.9 (4.2) | 394 |
 | HANNA (reference) | 0.11 (0.07) | 5.1 (2.0) | 93 |
 
-254 IDAC points (54 systems), 7,722 VLE points, 2,058 H^E points. On data that postdate every reference
-fit, the zero-constant models are significantly worse than COSMO-SAC on VLE (Z0x minus COSMO-SAC 2010:
+254 IDAC points (54 systems), 7,722 VLE points, 2,058 H^E points. In this historical temporal comparison,
+Z0x is significantly worse than COSMO-SAC on VLE (Z0x minus COSMO-SAC 2010:
 [+1.2, +3.3] points) and on mean IDAC error, although their median IDAC error is comparable or lower; the
 mean is carried by a small number of large misses.
 
@@ -173,8 +198,10 @@
 ### 3.4 Which term carries the error
 Replacing one fitted piece of COSMO-SAC-dsp at a time: theoretical electrostatics costs +0.03 in IDAC MAE
 (not significant) but +6 points in VLE AAD; DFT hydrogen-bond constants cost +0.13 in IDAC; London
-dispersion costs +0.17 in IDAC and slightly helps VLE. Stronger screening (Z0, Z0e) favors dilute
-properties and LLE detection; weaker screening (Z0s) favors VLE but loses both. By chemical family, Z0 is
+dispersion costs +0.17 in IDAC and slightly helps VLE. The larger electrostatic coefficients in Z0/Z0e
+favor some dilute-property and demixing results, whereas the smaller optical-screening coefficient in
+Z0s trades those results for lower VLE error. These are conditional one-term sensitivities, not an
+additive partition of the later Z0x-to-2010 gap. By chemical family, Z0 is
 the most accurate model for nonpolar solutes in aromatic solvents (alkenes in aromatics: 0.18 vs 0.40 for
 COSMO-SAC and 1.05 for UNIFAC) and for alkanes in alcohols (0.66 vs 1.04), and fails for self-associating
 solutes in inert solvents (alcohols in alkanes 3.7, in aromatics 3.4).
@@ -201,12 +228,45 @@
 218 IDAC points in 72 systems), Z0 and Z0x reach MAE 0.68 and 0.69 against 1.00 for COSMO-SAC 2010,
 0.94 for COSMO-SAC-dsp, 0.55 for UNIFAC (79% coverage) and 0.11 for HANNA.
 
+Later v2 conductor-optimized profiles passed the original median agreement gate at 0.1493, only 0.0007
+below 0.15, and were retained as exploratory rather than an accuracy-equivalent UD replacement. The
+frozen population contains 630 files passing the original Berny predicate and six separately flagged
+S1/S2 files. The R2-R9 numerical review preserves accepted performance changes and rejected trials;
+optimizer-state persistence is not relabeled E after its E gate failed. Omitted XC-grid response and the
+incomplete earlier finite-difference referee limit stationarity claims. The corrected-gradient rollout
+failed P32's compatibility gate, and the TEG energy-gradient mismatch remained unresolved when the
+R8/R9 diagnostic budget closed. There is no accepted blanket re-polish or chain rescue. See
+`docs/astra/round7/RESULTS.md`, `docs/astra/round8/RESULTS.md` and `docs/astra/round9/RESULTS.md`.
+
 ### 3.7 Conformer ensembles
 For the 50 most flexible benchmark molecules (4.9 conformers on average, BP86/def2-SVP profiles), replacing
 the lowest-energy conformer by the Boltzmann ensemble changed predictions very little: median
 |d ln gamma_inf| 0.009 (COSMO-SAC-dsp) and 0.011 (Z0x), 90th percentile under 0.09, and no significant change
 in accuracy (IDAC MAE difference [0.00, +0.01]; VLE [-0.35, +0.32] points). The lowest conformer carries
-60% of the weight on average. Conformer treatment is not a meaningful error source at this level.
+60% of the weight on average. This establishes a small effect for that finite proposal and weighting
+scheme, not the absence of conformational effects or a validated phase-dependent ensemble.
+
+R10 recovered and replayed all twelve fixed-panel UD raw files to their historical profiles. R11's
+ordered open-method cross attributes the polar-tail gaps for ethylene, diethylene and triethylene glycol
+mainly to stored coordinate inputs, including hydrogen positions and orientation. Tetraethylene glycol
+is an exception: its raw-tail gap was mainly method, and its other tail contrasts were small. No member
+passed the registered whole-profile attribution rule. These statements retain R11's original labels.
+
+R12/P46a then scored exactly 142 already-inspected glycol-solvent observations with original open solutes
+and a common P28 endpoint. Pooled MAE in ln gamma_inf was 1.813 for the original open solvent profiles,
+0.702 for the open method at the recovered UD coordinates, and 0.419 for UD solvent profiles. The
+coordinate-derived substitution removed 1.111, about 80% of the open-to-UD comparator MAE gap and 61% of
+the original open absolute error; 139 rows improved and three worsened. Shape carried essentially all
+of the factorial error reduction. Tetraethylene glycol recovered only 13% of its comparator gap. The
+remaining 0.283 is a conditional difference of MAEs, not a universal method-error estimate. P47 located
+same-geometry method differences toward the acceptor side and the EG/DEG/TEG coordinate differences
+toward the donor-side tail; those partitions are not hydrogen-bond energies or binwise error causes.
+
+This was retrospective explanatory ThermoML scoring. The UD notice reports database-level revisions
+using vapor-pressure predictions without identifying which panel members were revised. The result does
+not establish extended chains as the liquid conformations or adopt a geometry rule. P35 closed after
+R13 with its explanatory finding; the liquid distribution remains unresolved and all 630+6 open files
+remain frozen. See `docs/astra/round10/RESULTS.md` through `docs/astra/round13/RESULTS.md`.
 
 ### 3.8 Continuum desolvation of the association term (Z0w2)
 
@@ -235,50 +295,97 @@
 three temperatures (PREREGISTRATION.md, session 5b). The teacher is physically reasonable (water 87% bonded,
 1.115 g/cm3; an independent engine gives 86% and 1.10), but Z0w3 fails badly: temporal IDAC MAE 2.19 against
 1.45 for Z0x, aqueous test systems 4.79 against 1.76. The simulated association is strong (water Delta about
-ten times the gas-phase dimer value), and adding it on top of a COSMO residual that already contains much of
-the hydrogen-bond electrostatics counts the same physics twice. Three association variants have now failed
-for complementary reasons (too strong from gas-phase dimers, too weak after continuum desolvation, too strong
-again when taken from the liquid), which points to the additive architecture rather than to the constants.
+ten times the gas-phase dimer value). Overlap with electrostatic contributions in the COSMO reference is
+a plausible architectural explanation. The explicit COSMO hydrogen-bond constants were already zero in
+Z0w and its descendants, so merely turning that term off is not a new solution. The nitrogen-site
+occupancy mismatch and temperature-fit failures also matter. The failed registrations stand; neither a
+unique double-counting decomposition nor a successful replacement architecture was established.
+
+A later, separate source regression must not be confused with these historical failures. Since P6,
+Z0x's optimized interior dispatch bypassed the association subclasses' _g overrides; enabling P28 could
+do so at pure endpoints as well. Archived Z0w/Z0w2/Z0w3 scores predate that change. P55's separate repair
+restores full-subclass-g finite differences, including the historical one-sided endpoint approximation;
+it does not supply an exact association endpoint or a new association score. Software regression tests
+and any future physical validation are reported separately. No fourth association variant is accepted.
+
+### 3.10 Dielectric ingredient and retrospective VLE oracle
+
+R14/P51 screened 742 stored entries against a pinned public liquid-permittivity compilation using exact
+identity and temperature rules. There were 248 valid matches at 298.15 K, with five additional matched
+entries having invalid stored epsilon. The registered complete aggregate was therefore withheld.
+Descriptive matched-only summaries are not substituted for that withheld aggregate or interpreted as
+validation of the current Onsager approximation.
+
+P52, after amendment P52a protecting the exact 630/1/5 profile selection, ran on 963 already-exposed
+observations in 100 binary systems. All 2,889 requests were finite and the historical P6 baseline replay
+matched. With identical UD profiles and frozen pure vapor pressures, row-weighted VLE AAD was 13.78%
+for stored-epsilon Z0x, 13.07% for experimental-epsilon Z0x, and 10.44% for COSMO-SAC 2010. Equal-system
+AAD was 13.90%, 13.19% and 10.65%, respectively. From unrounded outputs, the oracle removed about
+0.72 percentage points, roughly 21% of the 3.35-point comparator gap; independently rounded table
+entries need not subtract to the printed difference. There were 559 improved and 404 worsened rows.
+Experimental epsilon was held at its 298.15 K value throughout, so this was not an epsilon(T) or HE test.
+
+The oracle is an experimental-input, retrospective diagnostic, not a fit-free variant, a rigorous
+headroom bound or a newly held-out score. The old main7 14.15/8.62 comparison uses a different subset.
+R14 does not authorize a portfolio dielectric simulation campaign or identify a transferable local
+contact coefficient. See `docs/astra/round14/RESULTS.md`. No R15 factorial result is asserted here.
 
 ## 4. Discussion
 
-Three results stand out. First, the sigma-profile physics with constants from theory alone reaches the
-accuracy of fitted COSMO-SAC 2010 for infinite-dilution activity coefficients of molecules outside the
-training split, and it predicts liquid-liquid demixing more reliably than both COSMO-SAC and modified
-UNIFAC, at the level of HANNA. Z0x achieves this with no regression and no data-driven choice. A large
-part of COSMO-SAC's predictive power therefore does come from the profiles rather than from the fit.
-
-Second, the fitted hydrogen-bond constants do not measure hydrogen bonding. Quantum chemistry puts all
-three COSMO-SAC classes at about 5,700 kcal A^4 mol^-1 e^-2, with a single universal value performing as
-well as three. The fitted OT-OT constant is six times smaller. A CCSD(T) check changes the DFT values by
-about 15%, far less than this gap. The fit is compensating for something else, most plausibly the missing
-entropy of hydrogen-bond formation and the too-strong electrostatics discussed next, which also
-explains why the largest remaining misses are self-associating solutes in inert solvents.
-
-Third, the decisive missing physics is dielectric screening of the misfit energy. The conductor limit
-overestimates electrostatic penalties; screening with a pair-averaged permittivity helps; making the
-screening follow the local composition helps more, and it does so without breaking thermodynamic
-consistency. Choosing a weaker screening on training data improves VLE but degrades dilute properties
-and demixing, so no single constant can serve both regimes, and fitted models hide this by averaging over
-them. A first-principles Wertheim association term fixes self-associating solutes in inert solvents but, with
-gas-phase bonding entropies, breaks aqueous mixtures; a condensed-phase estimate of the bonding entropy is
-the specific open problem.
-
-The zero-constant models are not competitive in general. On data published after the reference models
-were fitted they are significantly worse than COSMO-SAC on VLE and on mean infinite-dilution error, and
-HANNA is far more accurate than any physics-based model wherever its training data reach. The value of
-the approach lies in what it explains and in chemistry without data. Testing that second claim requires
-molecules and data outside every model's training set, which the ThermoML archive, ending in 2019,
-cannot provide.
+The historical benchmark shows that specified theory-derived interaction constants can retain useful
+IDAC and demixing performance within a common COSMO-SAC framework. Z0x remains worse than COSMO-SAC 2010
+for VLE on the displayed main7 and temporal subsets. This supports a quantitative account of the
+tradeoff, without claiming that all empiricism has been removed or that the model is generally competitive.
+
+The electrostatic contact prescription is a plausible research target, but bulk permittivity and local
+segment response are different quantities. In the implemented mapping, increasing epsilon raises
+f=(epsilon-1)/(epsilon+0.5) toward the conductor limit. The experimental-epsilon oracle yields only a
+small improvement on its particular exposed sample. Earlier one-term ablations and that oracle do not
+identify a unique universal correction, and their apparent gains cannot be added as independent causes.
+A complete same-row factorial can quantify the contributions of the implemented ES, HB and dispersion
+replacements under a stated allocation rule, including their interactions. Its fitted corners remain
+diagnostics, never candidates selected by whichever ThermoML error is smallest.
+
+Deriving a new contact kernel from reaction-field response or independent electronic calculations is
+physically possible after the cavity, contact geometry and reference-energy partition are specified.
+Electronic energy alone does not determine the angular and entropic contact free energy. A self-consistent
+finite-dielectric profile model would also need consistent pure references and composition/temperature
+derivatives; another dielectric scale on top of it is not automatically justified. No such new local
+model is validated by the present evidence. A future design needs independent physical acceptance and
+an exposure audit before any confirmatory comparison.
+
+Association and direct simulation remain separate research programs. Reproducing a bonded fraction does
+not validate the site thermodynamics, and an energy/force model does not automatically validate its
+field response or chemical potentials. The numerical association repair changes neither the archived
+scientific failures nor this assessment. The present work is ready for a limitations-aware account of
+its completed evidence; a speculative native campaign need not delay that account.
 
 ## 5. Limitations
-ThermoML ends with 2019 publications, so no test postdates HANNA's training data. Profiles come from one
-DFT source (DMol3), whose averaging conventions follow the fitted model. The open profile pipeline narrowly failed its agreement test with the DMol3 profiles, so
-uncovered compounds are reported only as an exploratory table. Pure-component vapor pressures are experimental correlations. Conformers are single structures.
+
+The retained effective area and combinatorial constants, sigma-processing conventions and empirical
+history of some UD conformations limit the meaning of "fit-free". Z0/Z0x interaction constants were not
+regressed to ThermoML. Z0s involves a train-selected discrete choice; Z1 is a fitted comparison. VLE
+uses the same experimental pure-component vapor-pressure correlations in every arm. UD-backed main
+results and exploratory open-profile results are different input versions.
+
+The original compound and 2017-2019 temporal collections were repeatedly inspected during later
+development. Neither is certified unexposed for another adaptive variant, and no new multi-system
+holdout or data beyond HANNA's training has been certified. Historical confidence intervals keep their
+original scope. Later explanatory ratios have no claimed generalization confidence interval.
+
+The 630 original-gradient profiles and six S1/S2 profiles retain their actual provenance. A passed
+historical agreement threshold is not proof of corrected-gradient stationarity, a liquid conformer
+ensemble or equivalence to UD. P35's retrospective coordinate explanation and its tetraEG exception do
+not identify a production geometry rule. LLE detection does not certify global stability or every
+reported composition. Claims about new source versions require separate numerical checks.
 
 ## Data and code availability
-All code, the frozen benchmark, split hashes, predictions and scorecards are in the project repository
-(`src/zcosmo`, `data/benchmark`, `results/`).
+
+The repository contains source code, registrations and public aggregate result records. UD-derived
+geometries and detailed R10-R15 profile/prediction artifacts remain private on the Mac under the applicable
+data-use terms. Some historical predictions and execution inputs are private or untracked; a public
+checkout alone is not asserted to reproduce every historical table. Public result records retain plan
+digests and scope, and their instructions identify required private assets without redistributing them.
 
 ## Figure captions
 
@@ -290,8 +397,9 @@
 (points; bars are class means) compared with the fitted COSMO-SAC 2010 values (blue bars).
 
 **Figure 3.** Trade-off between infinite-dilution accuracy (IDAC MAE, x axis) and bubble-pressure accuracy
-(VLE AAD, y axis) on held-out molecules. Stronger dielectric screening (Z0, Z0e) favours dilute properties;
-weaker screening (Z0s) favours VLE; composition-dependent screening (Z0x) sits between them.
+(VLE AAD, y axis) in the historical compound-test comparison. Larger electrostatic coefficients
+(Z0, Z0e) favor some dilute properties; the smaller optical-screening prescription (Z0s) improves VLE
+at the expense of other metrics. These are exposed comparisons, not evidence for one optimal coefficient.
 
 **Figure 4.** Liquid-liquid split detection on held-out molecules: share of experimentally two-phase systems
 where a gap is predicted vs share of experimentally homogeneous systems where a gap is wrongly predicted.
@@ -307,7 +415,9 @@
 S4 All scorecards with bootstrap intervals: `results/scorecard_*.md`.
 S5 Error maps by chemical family: `results/error_map_idac_*.csv`.
 S6 Open-profile validation and conformer comparison: `results/pyscf_profile_validation.csv`,
-   `data/pyscf_sigma/conformer_summary.csv`.
+   `data/pyscf_sigma/conformer_summary.csv` (asset availability is stated above).
+S7 Later numerical, glycol and dielectric evidence: `docs/astra/round2/RESULTS.md` through
+   `docs/astra/round14/RESULTS.md`, with the registrations and private-plan digests referenced there.
 
 ## References (to verify against the publisher records before submission)
 
```
<!-- END PATCH P56 -->

<!-- BEGIN PATCH REG15 -->
```diff
diff --git a/docs/astra/round15/REGISTRATION_PROPOSED.md b/docs/astra/round15/REGISTRATION_PROPOSED.md
new file mode 100644
--- /dev/null
+++ b/docs/astra/round15/REGISTRATION_PROPOSED.md
@@ -0,0 +1,169 @@
+R15-P54-P55-P56: contact attribution, association dispatch, and manuscript scope
+
+Proposed text, not an adoption or execution record. Append this complete text
+with the actual adoption time to PREREGISTRATION.md and commit the reviewed
+helpers, association repair and manuscript edits before any real-data plan is
+prepared or any new output is used. Reference main is
+3cd0a22888b40699d5f4994f5ba2e5cd274703df. This design follows the inspected R14
+results, including P52a, and has no claim to a new held-out validation set.
+Earlier registrations and results, P35's closeout and the R8/R9 numerical-gradient
+closure remain unchanged. The 630 primary and six selected S1/S2 open profiles
+remain frozen. There is no new QC, molecular-dynamics or conformer budget.
+
+P54 is an A fitted-ingredient explanatory intervention with E same-input and
+finite-game accounting checks. It is retrospective ThermoML scoring. A fitted
+constant is never adopted, optimized or selected from these results. No hybrid
+corner becomes a new production model even if its error is smaller. No optional
+parameter sweep, favorable ordering, alternative subset or accuracy-based
+stopping rule is introduced.
+
+Use exactly the completed private P52 plan and its 963 observations in 100
+unordered binary systems. Require its actual committed digest, completed
+2889-request receipt, exact baseline replay and original immutable input hashes.
+P52a's protected selection is profiles_v2=630, s1_stalled=1, s2_stalled=5. Preserve
+the superseded source files as well; do not delete, merge or regenerate them.
+Query identity remains the original file-row identifier from P52, including
+its ordered components, T, x1, experimental pressure and frozen pure pressures.
+Do not reconstruct the selection from a current CSV or a rounded result table.
+The baseline is stored-epsilon Z0x, not the experimental-epsilon oracle.
+
+There is one explicit source-version bridge. P55 modifies only z0w.py, which
+neither P52 nor P54 invokes. If that file's archived source hash differs at the
+current checkout path, require its archived SHA256 to match the original bytes
+at this reference main and its current bytes to match the R15 registration.
+Record both hashes. All other archived scientific inputs and participating
+sources must still match exactly. The original R14 checker is not altered or
+claimed to have accepted changed inputs. The new adapter independently checks
+P52's saved result identities, accounting and aggregate arithmetic. Original
+exposure receipts remain historical records, not live claims that public
+reporting documents have never subsequently changed. The current Z0x, cosmosac,
+zmodel and model-registry sources and the Z0/dielectric/dispersion tables must
+also match reference main; source paths in another worktree do not authorize
+changes to the executing model.
+
+The nominal five players are electrostatic closure, HB constants/rule,
+London/dispersion, effective area, and profile convention. In these exact
+endpoints only the first three differ. Both use the same UD bytes and the
+same stored NHB/OH/OT convention, sign mask, aeff=7.25, q0=79.53, r0=66.69 and
+z=10. Treat effective area and profile convention as dummy players. Their zero
+contributions concern this endpoint difference, not their physical importance.
+Any unexpected difference in a shared ingredient fails preparation, rather than
+creating a new physical intervention after the results.
+
+Bits are E,H,D. E=0 retains the complete Z0x composition-dependent c_ES rule
+and its dc_ES/dx term. E=1 uses the 2010 composition-independent coefficient
+A_ES+B_ES/T^2, including its original temperature dependence and dc_ES/dx=0.
+Do not change only _c while retaining Z0x's old composition derivative.
+H=0 uses the existing Z0 OH-OH/OH-OT/OT-OT constants, without recomputing the
+dimer matching after another bit changes. H=1 uses the 2010 constants. The
+opposite-sign contact mask and stored profile split are identical; no separate
+cutoff or profile reprocessing is introduced. D=0 retains Z0's London term.
+D=1 disables explicit dispersion, as in the repository's COSMO-SAC 2010 target,
+not COSMO-SAC-dsp 2014. It must change the London mode as well as use_dsp because
+the current London branch runs before the use_dsp test. The all-one parameter
+object must equal Params(use_dsp=False).
+
+Evaluate the eight unique corners once per observation. Lift these to all
+32 nominal five-player corners by exact reuse of the two dummy factors; no
+extra model calls are required. The budget is 8*963=7704 lngamma requests.
+First run both endpoint controls, 000 and 111, for all 963 observations:
+1926 requests. Both must be finite positive pressures and reproduce P52's
+stored-epsilon Z0x and 2010 pressures to strict relative difference <1e-8.
+They also preserve P52's already-passed historical P6 baseline audit. Failure
+of either fresh endpoint blocks all six intermediate corners, retaining
+requested identities and the failure receipts. No tolerance is relaxed.
+If both pass, run all six intermediate corners, 5778 further requests.
+
+No activity solver, scientific parameter, profile, vapor pressure or dielectric
+table is regenerated. Use the unchanged segment solver and Z0x interior
+derivative. Enable P28 consistently, though every selected x1 is outside its
+endpoint strip. Clear inherited ZC_* switches and supply explicit private
+profile overlays for both components, preserving the historical exact-key or
+unique-connectivity profile selection. Missing profiles cannot fall back to
+another source. The explicit profile grids must match the expected 153 rows
+and common sigma grid. Each ordered pair/corner is a fresh process; its rows
+keep P52 order. Actual ordered-pair job count is computed from the plan, not
+assumed equal to the unordered-system count.
+
+Real preparation, execution and collection occur only on the asset-bearing
+Mac, outside CI and Git checkouts for outputs. Preserve the R14 installed
+numerical environment, all reused data hashes and the new code hashes. Commit
+only the private plan's SHA256 in docs/astra/round15/PLAN_SHA256.txt before the
+first model query. Registration and plan commits must be ancestors of the
+executing HEAD. Private plans, paths, UD data, overlays, dense profiles,
+row-level predictions and logs are never uploaded or written into Git.
+The helper has no upload operation and no production-profile writer.
+
+The driver runs serially with four OpenMP threads and one BLAS thread. Each
+worker has at most 120 seconds, within a 7200-second model-run allocation. The
+five-second process-kill/accounting allowance is not extra scientific compute.
+Post-run read-only validation time is reported separately. Every planned job
+has a terminal record even if blocked, unstarted or interrupted. An attempt
+receipt is written before each model query. A permanent exclusive claim binds
+a plan to one run. No retry, resume, stale-claim removal, second output run,
+free-tier cloud dispatch or paid resource is authorized. All completed and
+unfavorable results are retained. A failed or nonfinite corner withholds the
+complete-panel attribution; no smaller finite intersection is selected.
+
+At each row compute signed percent pressure error and absolute percent pressure
+error from the fixed experimental pressure. The Shapley game value is negative
+absolute error, so positive contribution means absolute error removed. Also
+report signed-bias contributions separately. Compute all five-player Shapley
+values and independently verify equality to the three-active-player result,
+zero dummy contributions, and efficiency per row to <1e-8 percentage points.
+Check inclusion/exclusion interactions and the signed-bias identity to the
+same bound. Invalid derived arithmetic blocks complete aggregation.
+
+Publish all eight corner AADs and signed biases, plus improved/worsened counts,
+row-weighted and equal-system errors, all five signed factor contributions and
+all seven nonempty active-factor inclusion/exclusion interactions. These are
+fixed algebraic summaries, not choices among different primary metrics. Report
+one-at-a-time substitutions alongside Shapley rather than replacing them with
+whichever looks favorable. Gap shares are signed, unclipped and withheld when
+the baseline-minus-2010 gap is <=1e-6 percentage points. Shares need not fall
+inside [0,1]. Interaction allocations are conditional on this intervention set
+and loss function, not unique physical causal percentages. No new inferential
+confidence interval, global accuracy claim or production-acceptance threshold
+is attached to this exposed sample. The earlier epsilon-oracle recovery and
+new ES attribution overlap and must not be added as independent effects.
+
+The complete public output is the explicit aggregate error allowlist after
+separate operator review. All row data remain private. The independent check
+reconstructs summaries and verifies receipts without another model request.
+Checks may be repeated, but a claimed scientific run may not. After completion
+or failure, archive the outcome without an automatic native continuation.
+
+P55 is an A numerical correction relative to defective current-main association
+predictions, with an E software-restoration comparison to the historical
+full-_g finite-difference prescription. Add only a Z0wBinary.lngamma override
+that differentiates self._g at the old H=1e-4 and returns g+(1-x)g' and g-xg'.
+Z0w2 and subclasses preserving this method inherit dynamic _g/_ga dispatch.
+The optimized Z0x implementation is unchanged. The historical one-sided endpoint
+error remains; P28's exact Z0x endpoint must not be claimed exact for association.
+No site strength, _solve_X tolerance, pure reference, temperature interpolation
+or physical association architecture changes. The inherited Z0w3 implementation
+is not in current src and is not certified by a generic descendant test.
+
+Software acceptance requires tests on Z0w, Z0w2 and synthetic descendants with
+nonzero added g, at interior and endpoint-strip boundaries and both pure
+endpoints, with P28 both off and on. Compare to the explicit historical stencil
+to 1e-12 in synthetic ln gamma, test nonzero association mass action with synthetic
+strengths, and keep Z0x endpoint/corner outputs unchanged. Test the full-G identity
+and the retained O(H) endpoint error explicitly. These are code regression checks,
+not the 25-molecule/2302-row profile gate or a new ThermoML acceptance result.
+No fresh Z0w-family experimental scoring is authorized. The recorded historical
+association failures predate P6 and remain untouched. Further association work
+requires an independently defined reference-energy partition and site-model
+validation; switching off the explicit COSMO HB term was already done.
+
+P56 is E reporting. Update manuscript scope and historical version labels,
+acknowledge inherited constants/profile conventions and empirical upstream
+inputs, add the accepted-but-exploratory v2 profile history and corrected-gradient
+limitations, and record the R10-R13 glycol result with P46a and the tetraEG
+exception. Include P51's withheld aggregate and the completed P52/P52a oracle
+on its own 963-row subset, preserving rounding and exposure qualifications.
+Retain historical numerical tables and failures; do not claim P54 has run when
+its code is merely committed. The paper may be finalized with its completed
+evidence; references and artifact availability still require a submission audit.
+No universal fit-free contact coefficient or successful new architecture is
+established or adopted by this record.
```
<!-- END PATCH REG15 -->
