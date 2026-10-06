Z-COSMO round 6: exact endpoints, conformer reference states, and a bounded stationarity referee

Reference: `Victor-Liang-ChE/zcosmo`, `main` at `43213a5e61f591a19b4d3352a95315a62ee2aeb8`. The round-6 prompt, the complete archived round-5 report, R5 source helpers and workflows, and the measured R5 results govern this review. The archived R5 report and the existing source modified below were checked against their Git blob hashes. All six extractable patches target this reference. [S1–S7]

The first change worth testing is the analytic infinite-dilution endpoint. It requires no new quantum chemistry and corrects a known numerical approximation rather than choosing a profile convention. For conformers, the defensible target is a phase-dependent basin ensemble with consistent free-energy reference states. Neither the lowest conductor electronic energy nor exclusion of intramolecular hydrogen bonds defines that ensemble. The stopped six-chain campaign stays stopped. A separate five-geometry diagnostic tests whether omitted XC-grid response contributes to energy/gradient inconsistency before authorizing any additional mode analysis.

| Rank | ID | Class | Target and mechanism | Compute, saving, and acceptance burden | Effort |
|---:|---|:---:|---|---|---|
| 1 | P28 | A numerical correction | `Z0xBinary` exact pure endpoint; full-universe numerical audit | Zero QC. Typical cold segment work falls from seven solves to three; full timing remains to be measured. Accept against independent equations, not experimental MAE. | Moderate |
| 2 | P31 | E reporting | Render the existing matched P27 comparisons | Zero model evaluations and zero new bootstrap. Prevents mixing the 828-row and 816-row denominators. | Low |
| 3 | P29 | E inventory; A finite-basin model | Inventory P26 evidence; explicit conductor and phase-dependent reference states | Zero new quantum survey authorized in R6. Algebra and finite-state probes precede any costly ensemble campaign. No physical ensemble is accepted by these software tests. | Moderate to high |
| 4 | P30 | A diagnostic | Energy/gradient consistency, then conditional Hessian/profile stresses | At most five four-core worker-hours initially; at most ten more only after the fixed first-stage gate. No geometry optimization and no production relabel. | High |
| Shared | H6 | E instrumentation | Independent numerical checks, finite coverage, job isolation | Adds checking overhead, excluded from production timing. | Shared |
| Proposed text | REG6 | Registration | Freeze interpretation, budgets and gates | Must be adopted before new native results or corrected scores are used. | Administrative |

For the brief's saving × probability / effort criterion, P28 is the only proposed production accelerator. An illustrative allocation with 60% of evaluation time in the affected segment work gives `S = 1/(0.4 + 0.6 × 3/7) = 1.522`, a 34.3% saving. A subjective 0.9 implementation probability and effort 3 give 10.3 saved-time units per 100 affected units per effort. This is a planning calculation, not a benchmark. The other rows are scientific or reporting gates and have no defensible positive throughput estimate. They are ordered to avoid buying a new quantum campaign before resolving the inexpensive numerical question. Previously stopped work is not counted as a newly achieved saving.

What was executed here: the actual repository Z0x and COSMO-SAC algebra on synthetic profiles; a separate logarithmic segment-equation solve; component reversal and endpoint API checks; a finite-basin free-energy derivative test; mass-weighted Hessian projection on a synthetic diatomic; deterministic displacement construction; job censor/failure continuation; and a four-arm subprocess integration test. That integration test retained one matched nonfinite row per arm and rejected a missing result row. Python compilation, CLI help, patch application, and the report's command syntax were checked. The delivered test commands reproduce these software tests without PySCF or UD assets.

What was not executed: any new molecular SCF, native gradient/Hessian, actual all-benchmark endpoint audit, physical conformer population, Mac-only UD calculation, or corrected experimental score. PySCF installation was attempted and its resolver returned no matching `pyscf==2.14.0` distribution in this Python 3.13 runtime. This is an environment limitation, not evidence that the pinned release is unavailable on the working Python 3.11 machines. No cloud job was dispatched and no primary profile was modified.

The largest synthetic endpoint/reference difference was `1.2851e-10` ln units; the finite-basin one-conformer limit differed by `3.33e-16`; its analytic free-energy derivative differed from an independent finite difference by `2.92e-10`. Interior Z0x values in the regression test were unchanged. These are numerical implementation checks, not molecular acceptance results.

**What the project can state now, before P28**

The matched comparison is stronger and more precise than comparing standalone 0.839 with 0.942:

| P27 test quantity | Common rows / systems | Z0x-UD | Z0x-open630 | Open minus UD, paired 95% interval |
|---|---:|---:|---:|---|
| IDAC MAE, ln units | 816 / 201 | 0.8040 | 0.9423 | +0.0506 to +0.2379 |
| VLE pressure AAD, % | 12,403 / 428 | 15.9047 | 16.4133 | −0.7526 to +2.0951 percentage points |
| Excess-enthalpy MAE, J/mol | 8,573 / 348 | 618.64 | 699.33 | +50.91 to +108.83 J/mol |
| LLE row detection, finite-grid accounting | 2,469 / 100 | 0.88943 | 0.88335 | No paired interval claimed here |
| LLE system-majority detection, same systems | 2,469 / 100 | 0.84 | 0.82 | No paired interval claimed here |

These are the archived values, not reruns here. The IDAC and HE intervals support a deficit for the primary open-profile arm on the reused test set. The VLE numerical increase is small relative to its paired interval, which includes zero. The LLE comparison is operational gap detection on known LLE systems, not balanced accuracy or a proof of global equilibrium. [S3, S4]

For the matched LLE rows, UD has 2,140 checked endpoint rows with composition MAE 0.18009; open630 has 2,125 with MAE 0.17971. Each has 56 witness-only rows. The endpoint error denominators differ, so these two endpoint MAEs should not be advertised as a paired accuracy improvement. Both Z0x arms have zero unresolved rows under this finite-grid quality screen. COSMO-SAC-dsp still has 177 unresolved test rows in each corresponding arm; the Z0x result does not close that model's coverage problem. [S4]

A suitable headline is: “The open-source profile pipeline provides 630 Berny-converged benchmark profiles, plus six separately flagged exploratory profiles. With the same Z0x equations, the primary open profiles have higher test IDAC and excess-enthalpy errors than the UD profiles on matched observations. VLE and LLE comparisons are similar at the reported level of uncertainty and numerical resolution. The open profiles are a reproducible alternative input and coverage resource, not a validated accuracy-equivalent replacement for UD.”

Standalone UD IDAC remains 0.839365 on 828 rows; open636 is 0.976584 on those 828. The older 0.800 belongs to a different, 762-row model-list intersection. Preserve all of these with their denominators. All headline values above precede the proposed endpoint correction and must remain labelled that way if P28 is later adopted. [S3, S4]

P31 reads only the archived scorecard and refuses mismatched comparison counts. Its exact command is included after the common setup.

**Common setup, source isolation, and patch extraction**

The bundle contains H6, P28, P29, P30, P31 and REG6. The production edit is confined to an opt-in branch in `src/zcosmo/z0x.py`; everything else is a new helper or proposed registration file. Apply the bundle to an experiment worktree, not by overwriting the primary profiles. The shared tests import several proposal modules, so install the complete helper bundle before running them.

```bash
set -euo pipefail
export REPO="$PWD"
export BASE=43213a5e61f591a19b4d3352a95315a62ee2aeb8
export REPORT="${REPORT:-$REPO/ZCOSMO_ROUND6_REPORT.md}"
export WORK="$(mktemp -d "${TMPDIR:-/tmp}/zcosmo-r6.XXXXXX")"
export PATCHES="$WORK/patches"
mkdir -p "$PATCHES"
python - "$REPORT" "$PATCHES" <<'PY'
from pathlib import Path
import re, sys
blocks = re.findall(r'<!-- PATCH:(H6|P28|P29|P30|P31|REG6) -->\s*```diff\n(.*?)\n```',
                    Path(sys.argv[1]).read_text(), re.S)
assert len(blocks) == 6 and len({k for k, _ in blocks}) == 6
for key, text in blocks:
    Path(sys.argv[2], key + '.patch').write_text(text + '\n')
PY
git -C "$REPO" worktree add --detach "$WORK/review" "$BASE"
# Ignored Mac assets must not vanish in a clean worktree. Inputs remain read-only.
for asset in data results; do
  test -d "$REPO/$asset"
  if test -e "$WORK/review/$asset"; then
    mv "$WORK/review/$asset" "$WORK/review/$asset.pinned-copy"
  fi
  ln -s "$REPO/$asset" "$WORK/review/$asset"
done
for id in H6 P28 P29 P30 P31 REG6; do
  git -C "$WORK/review" apply --check "$PATCHES/$id.patch"
  git -C "$WORK/review" apply "$PATCHES/$id.patch"
done
cd "$WORK/review"
export PYTHONPATH=src:scripts OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export ZC_PCM3C=1 ZC_PCM3C_MB=2000 ZC_R6_ENDPOINT=0
unset ZC_SIGMA_OVERRIDE_DIR ZC_ONLY_KEYS ZC_BERNY_NOISE_EH ZC_MAXSTEPS
python -m pip freeze > "$WORK/environment.txt"
python scripts/r6_selftest.py > "$WORK/software-tests.json"
python scripts/r6_integration_test.py > "$WORK/process-tests.json"
python scripts/r6_headline.py --out "$WORK/P27-headline.md"
```

Use the already working asset-bearing Mac environment for P28 and all UD-backed calculations. For a separate native environment, the source-checked dependencies are:

```bash
python3.11 -m venv "$WORK/native-venv"
source "$WORK/native-venv/bin/activate"
python -m pip install 'pyscf==2.14.0' 'pyberny==0.7.0' \
  'rdkit==2026.03.6' numpy scipy pandas matplotlib
python -m pip freeze > "$WORK/native-environment.txt"
```

Do not use that installation block to upgrade the existing production environment. Its package versions and the source/profile hashes are inputs to the experiment. `REG6` is a proposed text file, not a registration event. Adopt the relevant text in `PREREGISTRATION.md`, commit it with its actual timestamp, then set `REG` to that commit before the new experiment commands below. No helper treats an uncommitted proposal as proof of authorization.

**P28: the exact endpoint is simpler than the interior derivative**

Write the dimensionless frozen-coefficient excess Gibbs function as `g(x,c)`, and the actual model as `g̃(x)=g(x,c(x))`. At a pure endpoint, every excess term vanishes for every coefficient:

\[
g(0,c)=g(1,c)=0,\qquad g_c(0,c)=g_c(1,c)=0.
\]

For example, a pure fluid's mixture segment solution equals its pure segment solution under the same kernel, so their residual contribution cancels. The combinatorial pure limit and the London exchange pure limit vanish as well. Therefore

\[
\widetilde g'(0)=g_x(0,c(0)),\qquad
\widetilde g'(1)=g_x(1,c(1)).
\]

The dielectric chain rule is essential in the interior, but its extra term is exactly zero at the pure endpoint. Consequently,

\[
\boxed{\ln\gamma_{1}^{\infty}(T)
=\ln\gamma_{1}^{\mathrm{frozen}}\bigl(T,x=(0,1);c=c(0)\bigr)}.
\]

The opposite endpoint follows by component exchange. This is an endpoint of the same underlying excess-Gibbs model, not the assumption that the dielectric is composition-independent everywhere. The code creates a fresh `Mixture` rather than using `_frozen`'s rounded-coefficient, first-insertion cache. [S5, S6]

The old `g(h)/h` endpoint has a leading truncation term `h g̃''(0)/2`. Strong curvature can therefore produce a substantial error even at `h=1e-4`. Shrinking h indefinitely is not a robust cure because segment-solver and floating-point errors are amplified by division by h. The archived R5 control establishes a 0.26 problem for one water-shape intervention, but does not contain a full-benchmark count of affected rows. Neither the 859-row intervention summary nor its mean profile-change magnitude is that prevalence count. P28 measures it explicitly. [S2, S3, S8]

The independent check solves

\[
y_m+\log\!\sum_n p_n E_{mn}e^{y_n}=0
\]

with its own log-sum-exp residual and Jacobian. For symmetric positive E and strictly positive p on its exact support, uniqueness follows from strict convexity of

\[
\Phi(y)=\frac12\sum_{mn}p_mp_nE_{mn}e^{y_m+y_n}-\sum_m p_my_m.
\]

The positive diagonal terms make its Hessian positive definite. This supports the reference equation, but the implemented residual tolerance is not an interval-arithmetic error certificate. Structural-zero bins are excluded from the unknowns and recovered from the same equation afterward; tiny positive bins are retained.

P28's gate covers all historical `has_sigma` IDAC rows, not just the problematic water rows. Each worker sees query identities and temperatures, without experimental responses. It evaluates old and corrected values independently, checks the pure limit and reversed component ordering, and compares against the independent log-equation reference. Matched nonfinite rows are retained; a changed finite mask fails comparability. The three-point h ladder is reported as a diagnostic rather than used to choose a favorable step.

Classification is A, a numerical correction: the exact formula can differ from main by more than the E threshold. The gate is max candidate/reference error below `1e-8`, reversed-index error below `1e-8`, endpoint API parity below `1e-10`, and solvent pure-limit error below `1e-9`, with independent equation residual at most `5e-12`. The original 25-profile bins are unchanged by construction; COSMO-SAC-dsp's P20 profile acceptance is not redefined by a Z0x endpoint correction.

```bash
: "${REG:?Set REG to the adopted R6 registration commit}"
python scripts/r6_endpoint.py prepare --profile-root data/pyscf_sigma \
  --registration "$REG" --out "$WORK/endpoint-inputs"
python scripts/r6_endpoint.py run --config "$WORK/endpoint-inputs/config.json" \
  --out "$WORK/endpoint-audit"
python scripts/r6_endpoint.py timing --config "$WORK/endpoint-inputs/config.json" \
  --out "$WORK/endpoint-timing"
```

`endpoint-audit/gate.json` contains all/test prevalence above 0.001, 0.01, 0.05 and 0.1 ln units. The per-arm CSVs retain every observation and its status. The solute and solvent tables localize the changes without dropping difficult systems. Fresh-process timing performs three repetitions in alternating flag order, outside the independent-reference and FD work.

After a numerical pass, record the decision before reading new experimental scores. An acceptance record has the exact fields `decision: "accepted"` and `numerical_gate_sha256`, equal to the digest of this gate. That record records a decision, not a command to manufacture one. Then:

```bash
: "${ENDPOINT_ACCEPTANCE_RECORD:?Path to the recorded acceptance of this exact gate}"
python scripts/r6_endpoint.py score --config "$WORK/endpoint-inputs/config.json" \
  --run "$WORK/endpoint-audit" --acceptance-record "$ENDPOINT_ACCEPTANCE_RECORD" \
  --out "$WORK/endpoint-corrected-IDAC"
```

The water-shape overlay remains a stress diagnostic even if the endpoint formula passes. A worse experimental MAE is not a reason to restore a known inaccurate endpoint. Conversely, an improved MAE is not the acceptance criterion.

The scope is deliberately narrow. `ZC_R6_ENDPOINT=1` changes exact x1=0 and x1=1 queries, including `lngamma_inf`; it leaves every interior composition untouched. The near-endpoint finite-difference strip may still be inaccurate and need not join the corrected endpoint smoothly. This patch does not claim a repaired full-composition derivative or a new LLE implementation. A later extension across that strip needs its own derivative and LLE checks. Existing exact-endpoint users should verify downstream output parity outside IDAC rather than silently relabelling every prior score as corrected.

**P29: choose a phase-dependent basin ensemble, with the reference made explicit**

A single conductor-energy minimum is defensible as a sampled zero-temperature reference or when a computed finite-temperature distribution is overwhelmingly concentrated there. It is not a generally valid liquid ensemble. Electronic energy alone omits basin entropy; a conductor is not the actual liquid environment. A rule removing intramolecular H-bonds would impose an infinite penalty on allowed molecular states. Choosing an extended conformer would impose another state-selection rule without deriving its probability.

The theory-first definition is a partition over distinct conformational basins. For basin a of chemical species i, define a common conductor-reference free energy

\[
G_{ia}^{C,0}(T)=E_{ia}^{C}+F_{ia}^{C,\mathrm{nuclear}}(T)-RT\log d_{ia}.
\]

The nuclear term contains ZPE and the basin's vibrational/torsional partition, with rotational contributions evaluated under a stated common convention. Molecular translational standard-state terms cancel between conformers of the same species. The degeneracy d counts physically distinct equivalent basin contributions; it is not the number of successful embeddings. Rotational symmetry and basin multiplicity must not count the same symmetry operation twice.

For a specified environment S,

\[
p_{ia}^{S}\propto
\exp\{-\beta[G_{ia}^{C,0}+\Delta\mu_{ia}^{C\to S}]\}.
\]

In a bulk liquid, the environment depends on the populations, so the populations and segment environment must be determined together. This distinction between reference and solution populations is consistent with the purpose of the perfectly screened reference in COSMO approaches. Published conformer work also shows why the stable conformer can differ between phases; that does not validate our proposed Z0x population closure. [U1, U2]

The intramolecular interaction is already represented, approximately, in the quantum energy and surface exposure. Do not add a second HB energy from the geometric contact count. The R5 contact information does not establish that the lowest-energy state is universally the “most H-bonded” one, and the earlier saved open EG/DEG/TEG geometries did not meet the registered contact predicate. Absence of a contact by that predicate is also not a proof of zero intramolecular interaction energy. [S3, S7]

Water lacks the flexible torsional alternatives at issue in the glycol series. Its profile can change for numerical/electronic reasons without a conformer selection explanation. Glycerol and propylene glycol have different OH placement and branching, so their basin entropies and exposed-polar distributions need not follow the linear oxyethylene homologues. The R5 data actually oppose a universal “more polar is better” claim: the UD water-shape substitution has a large effect but worsens its error, while the PG effect has the opposite sign from EG. Those observations constrain a theory; they are not weights with which to tune it. [S3]

An averaged histogram is not generally the correct ensemble chemical potential. If basin insertion works are u_a, the effective insertion free energy involves `-RT log Σ exp(-βu_a)`, not the work evaluated from an arithmetically averaged profile. The latter is a moment closure whose accuracy must be tested. For supplied profiles `P_a`, any positive mixture `Σw_a P_a` has a tail area within the supplied tail range. Its normalized profile is also a convex combination, with weights proportional to `w_a A_a`. Thus no positive weighting of a finite set can produce a tail outside that set's envelope. This is a useful falsification test for a proposed pool, not a statement about unseen conformers.

P26 demonstrated that sampled conformers can change profiles substantially. It did not demonstrate complete sampling, a thermal partition, or the liquid weights. Thirty-six stationary samples and three censored members do not become a complete 40-member protocol by discarding the missing outcomes. The skipped tetraEG proposal is explicitly retained as never run. [S3, S7]

**A concrete finite-basin Z0x closure for theory probes**

The new `r6_phase.py` supplies one explicit A closure, so “use Boltzmann weights” does not leave the reference-state problem hidden. It is not uniquely determined by the single-profile model and is not a validated substitute for DMol3/COSMO-RS.

Let a now index basin species, y their overall fractions, P_a their 153-bin area vector, and c_i the coefficient of pure chemical species i. Use the same frozen chemical permittivity and D4 data for all conformers of i. Let `Y_a(c_i)` be the pure-basin segment log-coefficient vector, and `e_ab` the absolute London contact energy using the existing combining rule and basin volumes. Define the hypothetical pure-conformer standard

\[
\frac{g_a^0}{RT}=
\frac{E_a^C+F_a^{\mathrm{nuclear}}}{RT}-\log d_a
+\frac{P_a\!\cdot Y_a(c_i)}{a_{\mathrm{eff}}}
+\frac{z w_{\mathrm{dsp}}e_{aa}}{2RT}.
\]

The absolute segment and London terms put all basins on an explicit common model reference before the pure-subtracted excess functional is added. Merely adding conductor energies to each basin's already-pure-subtracted `ln gamma` would leave the relative pure-basin standards unspecified.

The dimensionless total free energy per molecule is

\[
\mathcal F(y)=\sum_a y_a\,[g_a^0/(RT)+\log y_a]
+g_{\mathrm{ex}}^{\mathrm{microstate\ Z0x}}(y,T).
\]

The combinatorial and segment parts use the existing equations with more basin species. The coefficient remains volume-weighted through the chemical permittivities. The symmetric London extension is

\[
g_{\mathrm{disp}}^E=\frac{L}{2}\,y^T W y,
\quad L=\frac{z w_{\mathrm{dsp}}}{2RT},
\quad W_{ab}=2e_{ab}-e_{aa}-e_{bb}.
\]

For two single-conformer species this is exactly the original binary London expression. The coefficient derivative in each basin chemical potential is retained, with `Σy_a dc_a=0`, so the scalar free energy and its chemical potentials agree.

Minimize this free energy subject to the fixed total fraction of each chemical species. Compute the pure-solute and pure-solvent basin distributions separately. In the infinite-dilution solvent environment, form basin insertion offsets

\[
a_a=g_a^0/(RT)+\mu_a^E(y^{j,\mathrm{pure}}).
\]

Then

\[
\ln\gamma_i^\infty=-\log\!\sum_{a\in i}e^{-a_a}
-\mathcal F_i^{\mathrm{pure}}.
\]

The included regression proves numerically that one basin per chemical species recovers P28 and that the free-energy derivative agrees with the implemented chemical potentials. These checks detect standard-state and chain-rule errors without any measured response. They do not establish the adequacy of the absolute contact closure, harmonic treatment, frozen dielectric approximation, or finite search for the true liquid.

The finite solve allows at most four audited basins per species and two chemical species. Uniform and vertex-biased starts are fixed; every start must pass a population fixed-point check. The shared objective-call budget is 2,000 per equilibrium solve. Choosing the lowest of stationary solutions is a numerical multistart procedure, not global optimization certification.

**How the thermal inputs are computed, and what is not yet available**

The existing pipeline supplies the conductor geometry and TZVP electronic energy. P30 can supply a source-checked, mass-projected two-step Hessian diagnostic at an existing geometry. The helper computes harmonic nuclear free energies and a classical rigid-rotor contribution only for complete, audited inputs. It keeps signed frequencies and refuses a nonpositive harmonic mode. It does not use absolute frequencies or a “100 cm−1 floor” to rescue a state.

A low-barrier torsion is an important limitation even when both Hessian steps agree. A more physical partition must integrate the basin/periodic torsion, retaining its Jacobian and coupling to the other modes. Stable positive harmonic frequencies alone do not establish that the harmonic thermal amplitude remains inside that basin. The R6 harmonic catalog therefore remains a computational reference diagnostic. A physical ensemble cannot pass by entering zero for missing entropy or by declaring failed basins unimportant from their unconverged energies.

The eight structurally selected R5 validation molecules remain the separate validation panel; they are not replaced by whichever glycols look most favorable. A later complete ensemble protocol needs independent pool convergence, a thermal partition check, and fixed both-role affinity probes. The proposed thresholds are chemical free-energy agreement within 0.05 kcal/mol, normalized-profile L1 within 0.02, and maximum probe ln-gamma disagreement within 0.02 on water, methanol, nonane and dimethoxyethane at 250, 298.15 and 400 K. Identical finite coverage is required. Pool agreement alone does not bound missing basins.

No new quantum basin survey is authorized by P29 in this round. It inventories the existing samples and supplies the model definition and computational kernels. P30 has its own tightly bounded diagnostic budget. A new full conformer campaign would require a separate prospective budget rather than silently extending rejected P26.

```bash
# Read the archived P26 outputs. No workflow is dispatched by this download.
export P26_ARTIFACTS="$WORK/p26-artifacts"
gh run download 37426006692 -R Victor-Liang-ChE/zcosmo -D "$P26_ARTIFACTS"
python scripts/r6_ensemble.py inventory --proposals cloud/r5/proposals \
  --artifacts "$P26_ARTIFACTS" --registration "$REG" --out "$WORK/conformer-evidence"
```

For an already complete, audited basin set, the input schema to `r6_ensemble.py conductor` is a JSON object with `registration`, `basin_and_symmetry_audit`, and a `basins` array. Each entry names its `id`, actual `referee` output directory, its `status_sha256`, audited `rotational_symmetry_number`, and physical `degeneracy`. Those last values must come from the symmetry/basin audit; they are not supplied as invented constants in this report. All entries must be the same molecular species. The helper verifies native data/profile hashes and refuses incomplete thermal inputs.

```bash
# Conditional on a complete audit, not a license to invent missing thermal inputs.
: "${BASIN_CATALOG:?Path to the completed, hashed basin-and-symmetry catalog}"
python scripts/r6_ensemble.py conductor --catalog "$BASIN_CATALOG" \
  --out "$WORK/conductor-reference"
```

The output contains `catalog_250.json`, `catalog_298.15.json`, `catalog_400.json` and `reference_ensemble.json`. These are conductor-reference quantities, not accepted liquid populations. To combine two independently audited chemical catalogs at the same fixed temperature:

```bash
: "${CATALOG_I:?First audited chemical catalog at a fixed temperature}"
: "${CATALOG_J:?Second audited chemical catalog at that same temperature}"
python - "$CATALOG_I" "$CATALOG_J" "$WORK/binary-catalog.json" <<'PY'
import json, pathlib, sys
left, right = [json.loads(pathlib.Path(p).read_text()) for p in sys.argv[1:3]]
for key in ('T', 'registration', 'thermal_protocol'):
    assert left[key] == right[key], key
molecules = [{s['molecule'] for s in d['states']} for d in (left, right)]
assert all(len(s) == 1 for s in molecules) and molecules[0] != molecules[1]
out = dict(T=left['T'], registration=left['registration'],
           thermal_protocol=left['thermal_protocol'],
           basin_and_symmetry_audit=[left['basin_and_symmetry_audit'], right['basin_and_symmetry_audit']],
           states=left['states'] + right['states'])
p = pathlib.Path(sys.argv[3]); assert not p.exists()
p.write_text(json.dumps(out, indent=2, allow_nan=False))
PY
: "${SOLUTE_KEY:?Chemical key from the first catalog}"
: "${SOLVENT_KEY:?Chemical key from the second catalog}"
python scripts/r6_phase.py --catalog "$WORK/binary-catalog.json" \
  --solute "$SOLUTE_KEY" --solvent "$SOLVENT_KEY" --out "$WORK/phase-probe.json"
```

This conditional block consumes actual new quantum/thermal data when they exist. It is not executable to a physical answer from the present incomplete P26 summaries alone. The software tests exercise the same logic now using explicitly synthetic inputs. No R6 phase-probe result is authorized for ThermoML scoring.

**P30: separate force stationarity from flat-direction identifiability**

There is no universal theorem that a small gradient fixes a profile. In a region with Hessian bounded below by m>0, a stationary-point distance estimate scales like `||∇E||/m`. If an observable is locally Lipschitz with constant L, its corresponding error bound scales like `L ||∇E||/m`. On a soft torsion, m may be very small or not positively bounded. A tiny force can coexist with a wide range of nearly isoenergetic geometries and observables. This is why simply deleting Berny's on-sphere condition would not establish profile accuracy.

The archived diagnosis also says the unconstrained RFO step itself violates the step limits. Restoring a large trust radius alone does not address that. The old stopped-chain decision remains correct as an operational end to that campaign. It is not a theorem that every future discretization, optimizer, or thermal representation must fail. [S2, S3]

There is a specific source-level issue worth testing before another optimizer: in pinned PySCF 2.14.0, RKS gradients default to `grid_response=False`. The density-fitted RKS gradient supports the full-response branch and already includes auxiliary-basis response. Omitting the response of the geometry-dependent numerical integration grid can leave a small mismatch between the reported gradient and the derivative of the discretized energy. That mismatch may be unimportant at normal geometries yet material at the observed flat-surface scale. This is a hypothesis, not a diagnosis from the R5 timings. [U3, U4]

The exact API used is `mf.nuc_grad_method()`, then `gradient.grid_response=True`, then `gradient.kernel()`. The same solvated density-fitted object supplies the PCM and auxiliary responses. `r3_precision.factory` is reused for the original and tight SCF settings; no functional, basis, radius, pruning or Lebedev change is introduced. No `optimize()` wrapper or positional-callback assumption is involved. Signed frequencies are built from numerical Cartesian gradients, with masses from `mol.atom_mass_list(isotope_avg=True)`, and rigid translations/rotations are removed in mass-weighted coordinates.

The first-stage fixed cases are methanol and EG from the R5 structural plan, plus exactly the three P26 censored members: nonane, seed 20261006 rank 1; TEG, seed 20261006 rank 1; and dimethoxyethane, seed 20261005 rank 1. The archived input hashes and 80-evaluation outcomes must match. The six stopped long-chain keys are forbidden by the helper.

At each input, compute the original gradient and tight gradients with grid response off and on. Compare them against energy differences at ±0.003 and ±0.006 Bohr along four deterministic internal directions. The construction prefers heavy single-bond rotations and uses a fixed projected fallback. Two center SCFs plus sixteen displaced SCFs give 18 SCF evaluations and three gradients per case. Compare the two centered differences and their Richardson value. Do not interpret cProfile self time, a smaller gradient norm, or a successful SCF flag as evidence of gradient consistency.

```bash
python scripts/r6_jobs.py plan_referee --artifacts "$P26_ARTIFACTS" \
  --registration "$REG" --out "$WORK/local-referee"
python scripts/r6_jobs.py run --manifest "$WORK/local-referee/jobs.json" \
  --out "$WORK/local-referee-run"
```

Run these native commands in the pinned native environment. The manifest fixes each subprocess deadline, and records independent outcomes. Its serial launcher can be split into independent workers by distributing the frozen job entries; do not re-create proposals or let multiple workers share a checkpoint without the same lock. A nonzero result does not stop later independent entries. A stale lock is not removed automatically. This directly avoids the R5 `check=True` slot failure that prevented one unrelated proposal from running. [S7]

Only if all five cases satisfy the predeclared full-response consistency gate may the next block run:

```bash
python scripts/r6_jobs.py plan_modes --manifest "$WORK/local-referee/jobs.json" \
  --out "$WORK/local-modes"
python scripts/r6_jobs.py run --manifest "$WORK/local-modes/jobs.json" \
  --out "$WORK/local-modes-run"
```

The full-response error must be below `2e-7 Eh/Bohr` on all sampled directions, with the two-step FD uncertainty indicator below `1e-7`. A material omitted-response effect is reported only under the explicit relative and absolute tests in REG6. A failed first-stage gate stops escalation rather than prompting a new h or threshold chosen from its output.

The optional stage forms two finite-difference Hessians with the same 0.003/0.006 Bohr steps. The count is `12N+2` gradients, including center checks. The five cases together have a maximum planned count of 1,030 gradients, with no case above 360. At most two worker-hours per case includes those calculations and any subsequent profile stresses. Tight SCF plus full-response gradients are an A diagnostic change, not an E claim relative to the old force. No optimization runs.

A significant negative mode below −20 cm−1 or failure of the new diagnostic force targets prevents profile-stress escalation. These targets are deliberately named separately from Berny: max `5e-5`, RMS `1.5e-5 Eh/Bohr`. They do not reproduce its internal-coordinate or on-sphere predicate. If all vibrational modes are positive, the two Hessian steps must agree in harmonic F_vib within 0.05 kcal/mol at each fixed temperature before any harmonic catalog is produced. A near-zero or unstable thermal contribution remains unavailable; it is never made acceptable by a frequency floor.

For a passing stationary sample, compute the center and the six softest modes at both signs of 0.005 and 0.010 Å maximum-atom displacement. That is at most 25 TZVP profiles. The original sigma grid and averaging are unchanged. These stresses give an observed finite-set envelope. They do not certify a whole geometry ball, an unobserved torsion, or a global minimum.

The Mac-only affinity check uses P28 with each stress profile in a fresh process and a complete unchanged background. It tests both roles against the fixed water/methanol/nonane/dimethoxyethane probes at 250, 298.15 and 400 K. It checks identities, profile hashes and matching finite masks; maximum observed change must be below 0.01 ln units.

```bash
export OPEN_BACKGROUND="$(python - "$WORK/endpoint-inputs/config.json" <<'PY'
import json, sys
print(json.load(open(sys.argv[1]))['variants']['open636'])
PY
)"
python scripts/r6_stability.py run --manifest "$WORK/local-modes/jobs.json" \
  --background "$OPEN_BACKGROUND" --out "$WORK/local-affinity-stability"
```

This final check is a finite diagnostic. Even if it passes, the output has not passed the old Berny predicate and cannot silently replace an S1/S2 file or a primary profile. A production force/profile convergence rule would require a new independent validation, including limits on unsampled soft directions and thermal partition uncertainty. P30 tests whether that route is worth developing; it does not rescue the earlier rejected decisions.

**Cost and what a negative result would mean**

P28 and P31 require no quantum calculations. P29's inventory and finite-state implementation also require none; the necessary physical basin data are a separate constraint, not treated as free inputs. P30's first gate is capped at five four-core worker-hours, or 20 core-hours. Its optional stage adds at most ten worker-hours, or 40 core-hours, only after all initial cases pass. These are hard experimental budgets, not predicted completion times. Timeouts, memory failures and unavailable thermal partitions remain reported outcomes.

If full-grid response disagrees with independently stable energy differences, the derivative approximation remains unresolved and no optimizer trial is warranted from this report. If full response agrees but the local modes are unstable or extremely soft, the limiting question is basin/observable definition rather than simply Berny implementation. If the profile stresses pass but thermal F does not, the geometry can be locally adequate for a descriptor while being inadequate for a harmonic population calculation. Keeping those outcomes separate is more informative than a single “converged” flag.

The evidence supports important limits on interpretation. Without UD raw segment tables, an open raw tail and a UD processed tail are not a matched upstream comparison. For example, open DEG raw tail 40.7 Å² versus UD processed tail 38.0 Å² does not by itself prove that raw charge generation, rather than its interaction with smoothing, caused the final 27.7-versus-38.0 difference. The tested averaging perturbations being small is useful evidence, but it does not uniquely reconstruct the unavailable UD calculation. [S3] P25 tested the named SVP/TZVP and SWIG/ISWIG alternatives, not every level of theory or a matched DMol3 cavity/conformer. Missing UD geometries prevent unique historical attribution. P26's large conformer differences establish sensitivity, not that the correct liquid weights would recreate UD. A charge-neutrality projection remains unadopted, and its large HB response is not a reason to tune a neutrality convention to ThermoML. [S3, S8]

**Source and execution index**

[S1] `docs/astra/ROUND6_PROMPT.md`, current reference; Git blob `488428d068baecfdf7ef34336f542767ed4d0470`.

[S2] `PREREGISTRATION.md`, R5 registration/results and the October 5 stop decision; blob `e2440689efe12450a8e6522e261cea1f66f24062`.

[S3] `docs/astra/round5/RESULTS.md`, blob `88d669c4c8abc6269e55f3609d7ff390e7f6fc5c`, and its archived data summaries. These are the maintainer's measurements. They are not new calculations here.

[S4] `docs/astra/round5/data/scorecard_test.json`, blob `b6a82c84c36c09ac79e843d14d70c557530cc9c1`, and the accompanying `scorecard_test.md`. Matched row counts and paired intervals in this report come from the JSON pairwise entries.

[S5] `src/zcosmo/z0x.py`, complete source reconstructed and blob-verified: `80c3f1f3b61056a76678a80caf4120c58614adfe`. `src/zcosmo/cosmosac.py`, complete source reconstructed and blob-verified: `c226a668b7b9dba9e7400cda180fafd8faa700f3`.

[S6] `docs/astra/round5/ZCOSMO_ROUND5_REPORT.md`, full mounted copy matches current archived blob `6f418081ede1160393a1f9bee5106b4dc8f5d97e`. Its complete helper patches supplied the local R5 source used in the regression work. `scripts/r5_terms.py`, `r5_common.py`, `r5_shape.py`, `r5_scorecard.py` match fetched blobs `249c4411375bca46c7b9beed1e5cb10d1f163115`, `f5d21bb018b69a7d6125380f1218b0991dd5bc50`, `1d539ee44b1e925d2e6cd4e821111b56ac173401`, and `6dbc73b2215884c4106668ea4fc06c4366636b7b`.

[S7] `scripts/r5_conformers.py`, `cloud/r5/shape-plan/manifest.json`, `cloud/r5/proposals/`, archived `data/probe-selections/`, `.github/workflows/r5_conformers.yml` and `r5_native.yml`. Workflow blobs `96fa7ae0ab1d4905854e9cabca0507e4961e4c1a` and `cad4ca37deecab2d6994224aaa15f760c3478095` establish the frozen versions, budgets and slot behavior.

[S8] `docs/astra/round5/data/p24_terms_summary.json`, blob `5a4f472c2aee2758fd7763e5051c96858f5e5611`, and `p25_stage_comparison.csv`, blob `28f751319c697907454acb098f9f9e01499c2042`. They support the component and tested-method observations, not an all-benchmark endpoint-prevalence count.

[S9] `docs/OPTIMIZATION_BRIEF.md`, unchanged rules, blob `9042052e2c0884226db6f795d14f8ec8c0157bd4`.

[U1] Pung and Leito, “Predicting Relative Stability of Conformers in Solution with COSMO-RS,” Journal of Physical Chemistry A 121 (2017), 6823–6829, DOI `10.1021/acs.jpca.7b05197`. Used for the phase-dependence principle, not to borrow experimental calibration or claim validation of P29.

[U2] SCM, official COSMO-RS theory documentation, section on the perfectly screened reference and independent-segment approximation, accessed October 6, 2026. Our finite-basin extension and its gates are specified here rather than attributed to that implementation.

[U3] `pyscf/pyscf`, tag `v2.14.0`, `pyscf/grad/rks.py`, blob `e80fb801dbb9c06b8c97abf3cc33b404da3a0d81`: default `grid_response=False`, full-response branch and extra-force hook.

[U4] Same pinned upstream, `pyscf/df/grad/rks.py`, blob `c8facf9bd574d1b72bc9c3983723e03aacdbce9f`: DF full-grid response support and `auxbasis_response=True`. The native commands remain conditional because this runtime could not install PySCF.

The following diffs are the complete implementation bundle. They were checked against the reconstructed affected source, not against a claimed full repository clone or the inaccessible Mac assets.

**H6: complete unified diff**

<!-- PATCH:H6 -->
```diff
--- /dev/null
+++ b/scripts/r6_common.py
@@ -0,0 +1,72 @@
+"""Round-6 utilities. Output is separate from all registered profiles and scores."""
+from __future__ import annotations
+import hashlib
+import json
+from pathlib import Path
+import numpy as np
+
+BASE = '43213a5e61f591a19b4d3352a95315a62ee2aeb8'
+
+
+def sha(path):
+    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
+
+
+def write(path, obj):
+    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
+    tmp = p.with_name(p.name + '.tmp')
+    tmp.write_text(json.dumps(obj, indent=2, allow_nan=False) + '\n')
+    tmp.replace(p)
+
+
+def fresh(path):
+    p = Path(path).resolve()
+    if p.exists():
+        raise FileExistsError(p)
+    p.mkdir(parents=True)
+    return p
+
+
+def registration(text):
+    if not text or text.lower() in ('todo', 'pending', 'proposed', 'none'):
+        raise ValueError('Supply the actual prospective registration commit, not a placeholder')
+    return text
+
+
+def check_inputs(inputs):
+    for p, expected in inputs.items():
+        if sha(p) != expected:
+            raise ValueError('Frozen input changed: ' + p)
+
+
+def boltzmann(g_kcal, T, degeneracy=None):
+    """Finite-state partition function. Values must share one reference state."""
+    from scipy.special import logsumexp
+    g = np.asarray(g_kcal, float)
+    d = np.ones_like(g) if degeneracy is None else np.asarray(degeneracy, float)
+    if g.ndim != 1 or not len(g) or d.shape != g.shape or not np.isfinite(T) or T <= 0:
+        raise ValueError('invalid finite-state problem')
+    if not np.isfinite(g).all() or not np.isfinite(d).all() or (d <= 0).any():
+        raise ValueError('nonfinite energies or nonpositive degeneracy')
+    R = 0.00198720425864083
+    logw = np.log(d) - (g - g.min()) / (R*T)
+    logz = logsumexp(logw)
+    return np.exp(logw-logz), float(g.min()-R*T*logz)
+
+
+def profile_envelope(psigmaA):
+    """Convex-envelope statements about supplied samples, not unseen geometries."""
+    p = np.asarray(psigmaA, float)
+    if p.ndim != 3 or not len(p) or p.shape[1:] != (3, 51) or not np.isfinite(p).all() or (p < 0).any():
+        raise ValueError('expected nonnegative (conformers,3,51) profiles')
+    A = p.sum((1,2))
+    if (A <= 0).any(): raise ValueError('empty profile')
+    norm = p / A[:,None,None]
+    sig = np.linspace(-.025,.025,51)
+    tails = p[:,:,abs(sig)>=.01].sum((1,2))
+    fraction = tails/A
+    diameter = max(float(abs(a-b).sum()) for a in norm for b in norm)
+    return dict(raw_tail_min_A2=float(tails.min()),raw_tail_max_A2=float(tails.max()),
+                normalized_tail_min=float(fraction.min()),normalized_tail_max=float(fraction.max()),
+                normalized_L1_diameter=diameter,
+                meaning='Bounds cover convex averages of these samples only; no unsampled-basin bound.')
--- /dev/null
+++ b/scripts/r6_selftest.py
@@ -0,0 +1,158 @@
+"""Portable R6 tests. Synthetic inputs, not a Mac/UD or native PySCF acceptance run."""
+from __future__ import annotations
+import importlib.util
+import json
+import os
+from pathlib import Path
+import sys
+import tempfile
+import types
+import numpy as np
+from r6_common import boltzmann,profile_envelope
+
+
+def endpoint():
+    # Execute the actual current source with a synthetic, explicit input catalog.
+    import zcosmo.cosmosac as cs
+    prm=cs.Params(A_ES=11000.,B_ES=0.,c_OH_OH=5000.,c_OT_OT=4500.,c_OH_OT=4800.,disp_mode='london',w_dsp=1.)
+    profiles={}
+    sig=cs.SIG
+    for i,(A,V) in enumerate(((100.,80.),(180.,160.),(65.,40.))):
+        ps=np.zeros((3,51));ps[0]=np.exp(-((sig-.001*i)/.004)**2)
+        ps[1]=.15*np.exp(-((abs(sig)-.011)/.002)**2)
+        ps[2]=.1*np.exp(-((sig-.009)/.0025)**2)
+        ps[:,abs(sig)>.020]=0.
+        ps*=A/ps.sum();key=f'fake{i}'
+        profiles[key]=cs.Fluid(key,ps,A,V,'H2O' if i==2 else 'NHB',50.,{'synthetic':True})
+    original=cs.load_fluid;old_london=cs._london_table
+    cs.load_fluid=lambda k,*a:profiles[k]
+    cs._london_table=lambda p:{f'fake{i}':(200.+50*i,20.+3*i) for i in range(3)}
+    models=types.ModuleType('zcosmo.models');models.ROOT=Path.cwd();models.load_z_params=lambda n:prm
+    theory=types.ModuleType('zcosmo.zmodel');theory.c_es_theory=lambda fpol=1.:12226.235339788673*fpol
+    previous={name:sys.modules.get(name) for name in ('zcosmo.models','zcosmo.zmodel')}
+    sys.modules['zcosmo.models']=models;sys.modules['zcosmo.zmodel']=theory
+    previous_env=os.environ.get('ZC_R6_ENDPOINT')
+    try:
+        spec=importlib.util.spec_from_file_location('r6_test_model',Path('src/zcosmo/z0x.py'))
+        z=importlib.util.module_from_spec(spec);spec.loader.exec_module(z)
+        z._eps=lambda:{'fake0':5.,'fake1':30.,'fake2':70.}
+        from r6_endpoint import reference_value,fresh_stencils
+        errors=[];fd=[];rev=[];off=[]
+        for T in (250.,298.15,400.):
+            for a,b in (('fake0','fake1'),('fake1','fake2'),('fake2','fake0')):
+                m=z.Z0xBinary([a,b]);os.environ['ZC_R6_ENDPOINT']='0'
+                y=m.lngamma(T,np.array([.3,.7]));legacy=m.lngamma_inf(T,0)
+                os.environ['ZC_R6_ENDPOINT']='1';n=z.Z0xBinary([a,b]);new=n.lngamma_inf(T,0)
+                yr=n.lngamma(T,np.array([.3,.7]));off.append(float(abs(y-yr).max()))
+                ref,_=reference_value(n,T,0.);errors.append(abs(new-ref[0]))
+                reverse=z.Z0xBinary([b,a]).lngamma_inf(T,1);rev.append(abs(reverse-new))
+                if abs(n.lngamma(T,np.array([0.,1.]))[1])>1e-9:raise AssertionError('pure solvent does not vanish')
+                fd.append(min(abs(v-new) for v in fresh_stencils(n,T).values()))
+                os.environ['ZC_R6_ENDPOINT']='0'
+                if abs(n.lngamma_inf(T,0)-legacy)>1e-12:raise AssertionError('opt-out changed legacy endpoint')
+        assert max(errors)<1e-8 and max(rev)<1e-8 and max(off)==0. and max(fd)<1e-5
+        from r6_phase import PhaseModel
+        c0=12226.235339788673
+        states=[]
+        for i,key in enumerate(('fake0','fake1')):
+            states.append(dict(id=key,molecule=key,fluid=profiles[key],eps=[5.,30.][i],
+                C6_au=200.+50*i,alpha_au=20.+3*i,E_conductor_kcal=10.+i,F_nuclear_kcal=2.,degeneracy=1.))
+        pm=PhaseModel(states,298.15,prm,c0)
+        os.environ['ZC_R6_ENDPOINT']='1'
+        refz=z.Z0xBinary(['fake0','fake1'])
+        singleton_error=abs(pm.idac('fake0','fake1')['ln_gamma_inf']-refz.lngamma_inf(298.15,0))
+        assert singleton_error<1e-8,singleton_error
+        for u in (.01,.3,.8):
+            yy=np.array([u,1-u]);phase,_=pm.excess(yy)
+            assert abs(phase-refz.lngamma(298.15,yy)).max()<1e-8
+        from dataclasses import replace
+        other=replace(profiles['fake0'],key='fake0:basin2',psigA=profiles['fake0'].psigA.copy())
+        other.psigA=np.roll(other.psigA,1,axis=1)
+        alt=dict(states[0],id='second',fluid=other,E_conductor_kcal=10.4)
+        pm2=PhaseModel([states[0],alt,states[1]],298.15,prm,c0)
+        yy=np.array([.2,.3,.5]);ex,_=pm2.excess(yy);mu=pm2.g0+np.log(yy)+ex
+        direction=np.array([1.,-1.,0.]);h=1e-5
+        derivative=(pm2.free(yy+h*direction)-pm2.free(yy-h*direction))/(2*h)
+        gradient_error=abs(derivative-mu@direction);assert gradient_error<1e-6,gradient_error
+        pop=pm2.idac('fake0','fake1');assert abs(sum(pop['solute_trace_populations'])-1)<1e-12
+        return dict(phase_singleton_error=singleton_error,phase_derivative_error=gradient_error,endpoint_reference_max=max(errors),reverse_max=max(rev),interior_change=max(off),finite_difference_best_max=max(fd))
+    finally:
+        cs.load_fluid=original;cs._london_table=old_london
+        for name,value in previous.items():
+            if value is None:sys.modules.pop(name,None)
+            else:sys.modules[name]=value
+        if previous_env is None:os.environ.pop('ZC_R6_ENDPOINT',None)
+        else:os.environ['ZC_R6_ENDPOINT']=previous_env
+
+
+def ensemble():
+    w,f=boltzmann([0.,1.],298.15,[1.,2.]);v,g=boltzmann([20.,21.],298.15,[1.,2.])
+    assert np.max(abs(w-v))<1e-13 and abs((g-f)-20)<1e-13
+    # A twofold degeneracy is exactly two equal-energy, distinct microstates.
+    z,h=boltzmann([0.,1.,1.],298.15)
+    assert abs(w[0]-z[0])<1e-13 and abs(w[1]-z[1:].sum())<1e-13 and abs(f-h)<1e-13
+    ps=np.zeros((2,3,51));ps[0,0,25]=100.;ps[1,1,40]=50.
+    d=profile_envelope(ps)
+    rng=np.random.default_rng(8)
+    for _ in range(20):
+        q=rng.dirichlet([1.,1.]);mix=np.einsum('k,kij->ij',q,ps)
+        tail=mix[:,abs(np.linspace(-.025,.025,51))>=.01].sum()
+        assert d['raw_tail_min_A2']<=tail<=d['raw_tail_max_A2']
+    return dict(weight_sum=float(w.sum()),common_free_energy_shift=float(g-f))
+
+
+def modes():
+    from r6_referee import projected_modes,thermo_harmonic,probe_directions
+    x=np.array([[0.,0.,0.],[0.,0.,2.]])
+    masses=np.array([1.,1.]);v=np.array([0.,0.,-1.,0.,0.,1.])/np.sqrt(2)
+    H=.1*np.outer(v,v);vals,vecs,freq=projected_modes(H,x,masses)
+    assert len(vals)==1 and abs(vals[0]-.1)<1e-12 and freq[0]>1000
+    try:thermo_harmonic([-10.,100.],298.15)
+    except ValueError:pass
+    else:raise AssertionError('imaginary mode was hidden')
+    from rdkit import Chem
+    from rdkit.Chem import AllChem
+    m=Chem.AddHs(Chem.MolFromSmiles('OCCO'));assert AllChem.EmbedMolecule(m,randomSeed=7)==0
+    x=m.GetConformer().GetPositions();sym=[a.GetSymbol() for a in m.GetAtoms()]
+    d=probe_directions('OCCO',sym,x)
+    assert len(d)==4
+    for _,v in d:
+        assert abs(np.linalg.norm(v,axis=1).max()-1)<1e-12 and np.linalg.norm(v.sum(0))<1e-10
+    return dict(diatomic_frequency_cm1=float(freq[0]),directions=len(d))
+
+
+def jobs():
+    from r6_jobs import execute
+    with tempfile.TemporaryDirectory() as td:
+        p=Path(td);code=[2,0,1]
+        queue=[dict(id=f'j{i}',argv=[sys.executable,'-c',f'raise SystemExit({c})'],timeout_s=5,
+                    lock=str(p/f'j{i}.lock')) for i,c in enumerate(code)]
+        rc=execute(queue,p/'out',str(p),'portable-test')
+        d=json.loads((p/'out/jobs.json').read_text())
+        assert rc==2 and [r['status'] for r in d]==['censored','completed','failed']
+        assert not list(p.glob('*.lock'))
+        return dict(statuses=[r['status'] for r in d])
+
+
+def headline():
+    from r6_headline import render
+    d={'tables':{}}
+    for table in ('idac','vle','he'):
+        d['tables'][table]={'pairwise':[dict(model='Z0x',arm='open630',common_rows=2,
+            reference={'rows':2,'MAE':1.},candidate={'rows':2,'MAE':2.},delta_MAE_CI95=[.5,1.5])]}
+    lle=dict(rows=2,systems=1,row_gap_found_bounds=[.5,1.],system_gap_found_bounds=[0.,1.],
+             unresolved_rows=1,endpoint_rows=0,composition_MAE=None)
+    d['tables']['lle']={'pairwise':[dict(model='Z0x',arm='open630',common_rows=2,reference=lle,candidate=lle)]}
+    text=render(d);assert 'endpoint MAE None on 0' in text and 'false-positive rate' in text
+    d['tables']['idac']['pairwise'][0]['candidate']['rows']=1
+    try:render(d)
+    except ValueError:pass
+    else:raise AssertionError('different denominators accepted')
+    return dict(mismatched_denominator_rejected=True)
+
+
+def main():
+    result={}
+    for f in (endpoint,ensemble,modes,jobs,headline):result[f.__name__]=f()
+    print(json.dumps(result,indent=2))
+if __name__=='__main__':main()
--- /dev/null
+++ b/scripts/r6_integration_test.py
@@ -0,0 +1,43 @@
+"""Synthetic four-arm process/coverage regression. No quantum chemistry or experimental data."""
+import json, tempfile, shutil, subprocess, os, sys, hashlib
+from pathlib import Path
+import numpy as np,pandas as pd
+source=Path(__file__).resolve().parents[1]
+with tempfile.TemporaryDirectory() as temp:
+ root=Path(temp)
+ for rel in ('scripts/r6_common.py','scripts/r6_endpoint.py','scripts/r3_common.py','src/zcosmo/z0x.py','src/zcosmo/cosmosac.py'):
+  p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source/rel,p)
+ (root/'src/zcosmo/models.py').write_text("from pathlib import Path\nfrom zcosmo.cosmosac import Params\nROOT=Path(__file__).resolve().parents[2]\ndef load_z_params(n):return Params(A_ES=12000.,B_ES=0.,disp_mode='london')\n")
+ (root/'src/zcosmo/zmodel.py').write_text('def c_es_theory(fpol=1.):return 12226.235339788673*fpol\n')
+ keys=['fake-a','fake-b','BTFJIXJJCSYFAL-UHFFFAOYSA-N','missing-dielectric']
+ for folder in ('data/raw/nist/UD/sigma3','open630','open636','water_stress'):
+  p=root/folder;p.mkdir(parents=True)
+  for j,key in enumerate(keys):
+   if folder=='open630' and j==2:continue
+   g=np.linspace(-.025,.025,51);ps=np.zeros((3,51));ps[0]=np.exp(-((g-.001*j)/.004)**2)
+   ps[1]=.1*np.exp(-((abs(g)-.010)/.002)**2);ps[:,abs(g)>.019]=0;ps*=100/ps.sum()
+   with (p/(key+'.sigma')).open('w') as f:
+    f.write('# meta: '+json.dumps({'volume [A^3]':80.+j*5,'disp. flag':'NHB','disp. e/kB [K]':50.})+'\n')
+    np.savetxt(f,np.column_stack([np.tile(g,3),ps.ravel()]))
+ (root/'results/qc').mkdir(parents=True)
+ pd.DataFrame(dict(inchikey=keys[:3],eps=[5.,30.,8.])).to_csv(root/'results/qc/dielectric.csv',index=False)
+ pd.DataFrame(dict(inchikey=keys,C6_au=[200.,250.,180.,190.],alpha_au=[20.,25.,17.,18.])).to_csv(root/'results/qc/dispersion.csv',index=False)
+ rows=pd.DataFrame([['r0',keys[0],keys[1],298.15,'train'],['r1',keys[1],keys[0],298.15,'test_one'],['r2',keys[2],keys[1],298.15,'test_both'],['r3',keys[3],keys[1],298.15,'test_one']],columns=['r5_row_id','solute','solvent','T','split'])
+ experiment=root/'experiment';experiment.mkdir();rows.to_csv(experiment/'queries.csv',index=False)
+ digest=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
+ inputs={str(p):digest(p) for p in root.rglob('*.sigma')};inputs[str(experiment/'queries.csv')]=digest(experiment/'queries.csv')
+ cfg={'registration':'synthetic-acceptance-test','rows':str(experiment/'queries.csv'),'variants':{'UD':None,**{name:str(root/name) for name in ('open630','open636','water_stress')}},'inputs':inputs}
+ config=experiment/'config.json';config.write_text(json.dumps(cfg))
+ env=dict(os.environ,PYTHONPATH='src:scripts',OPENBLAS_NUM_THREADS='1')
+ def run(*argv):return subprocess.run([sys.executable,'scripts/r6_endpoint.py',*argv],cwd=root,env=env,capture_output=True,text=True)
+ p=run('run','--config',str(config),'--out',str(root/'audit'))
+ if p.returncode:raise RuntimeError(p.stdout+p.stderr)
+ gate=json.loads((root/'audit/gate.json').read_text());assert gate['numerical_gate']
+ for arm in cfg['variants']:
+  records=pd.read_csv(root/'audit'/f'{arm}.csv')
+  assert records.status.eq('baseline_nonfinite').sum()==1,arm
+ good=pd.read_csv(root/'audit/UD.csv');good.iloc[:-1].to_csv(root/'audit/UD.csv',index=False)
+ q=run('summarize','--config',str(config),'--out',str(root/'audit'));assert q.returncode!=0 and 'observation identity' in q.stderr
+ good.to_csv(root/'audit/UD.csv',index=False)
+ q=run('summarize','--config',str(config),'--out',str(root/'audit'));assert q.returncode==0,q.stderr
+ print(json.dumps({'four_arm_gate_passed':True,'missing_row_rejected':True,'rows_per_arm':4,'open630_excluded':1,'matched_nonfinite_retained_per_arm':1}))
```

**P28: complete unified diff**

<!-- PATCH:P28 -->
```diff
--- a/src/zcosmo/z0x.py
+++ b/src/zcosmo/z0x.py
@@ -2,6 +2,7 @@
 from __future__ import annotations
 
 from functools import lru_cache
+import os
 
 import numpy as np
 import pandas as pd
@@ -71,8 +72,22 @@
         dc = c_es_theory(fpol=1.0) * 1.5 * deps / (eps + 0.5) ** 2
         return lg + np.array([1 - x1, -x1]) * gc * dc
 
+    def _endpoint(self, T, x1):
+        """Exact pure endpoint of the same excess-Gibbs model, not a stencil.
+
+        g_c is zero at a pure endpoint because g(pure,c)=0 for every c.
+        Use a new Mixture to avoid the rounded-c, first-insertion cache.
+        """
+        if x1 not in (0.0, 1.0):
+            raise ValueError("_endpoint requires an exactly pure composition")
+        mix = Mixture(self.keys, self.z0.with_(A_ES=self._c(x1)))
+        return mix.lngamma(T, np.array([x1, 1.0 - x1]))
+
     def lngamma(self, T, x):
         x1 = float(x[0])
+        # Prospective A numerical correction. Defaults remain historical.
+        if x1 in (0.0, 1.0) and os.environ.get("ZC_R6_ENDPOINT", "0") == "1":
+            return self._endpoint(T, x1)
         h = self.H
         if h < x1 < 1 - h:
             return self._analytic(T, x1)
--- /dev/null
+++ b/scripts/r6_endpoint.py
@@ -0,0 +1,299 @@
+"""All-row endpoint audit. No experimental response is passed to a worker.
+
+Four source arms: UD, open630, open636, and the declared water-shape stress arm.
+Missing and excluded rows remain explicit. Nothing is scored or adopted here.
+"""
+from __future__ import annotations
+import argparse
+import json
+import os
+from pathlib import Path
+import subprocess
+import sys
+import time
+import numpy as np
+import pandas as pd
+from scipy.special import logsumexp
+from scipy.optimize import root
+from r6_common import BASE, sha, write, fresh, registration, check_inputs
+
+HS=(1e-4,1e-5,1e-6,1e-7,1e-8)
+
+
+def log_reference(E, p):
+    """Independent residual/Jacobian polish of the strictly convex log-state problem.
+
+    Structural zeros are kept. Positive bins are never thresholded.
+    """
+    from zcosmo.cosmosac import solve_gamma
+    E=np.asarray(E,float);p=np.asarray(p,float)
+    if not np.isfinite(E).all() or (E<=0).any() or not np.isfinite(p).all() or (p<0).any():
+        raise ValueError('nonpositive/invalid kernel or profile')
+    ix=np.flatnonzero(p>0)
+    if not len(ix):raise ValueError('empty profile')
+    le=np.log(E[:,ix])+np.log(p[ix])[None,:]
+    start=np.log(solve_gamma(E,p))[ix]
+    def fun(y):return y+logsumexp(le[ix]+y[None,:],axis=1)
+    def jac(y):
+        z=le[ix]+y[None,:];return np.eye(len(ix))+np.exp(z-logsumexp(z,axis=1)[:,None])
+    sol=root(fun,start,jac=jac,method='hybr',options={'xtol':1e-11})
+    y=sol.x
+    residual=float(abs(fun(y)).max())
+    # The equation residual decides numerical convergence, not only MINPACK's flag.
+    if residual>5e-12:raise RuntimeError(f'independent segment residual {residual}')
+    full=-logsumexp(le+y[None,:],axis=1)
+    return full,residual
+
+
+def reference_value(model,T,x1,parts=False):
+    from zcosmo.cosmosac import Mixture
+    mix=Mixture(model.keys,model.z0.with_(A_ES=model._c(x1)))
+    x=np.array([x1,1-x1]);pa=np.array([f.psigA.ravel() for f in mix.fl])
+    E=mix._E(T);ym,rm=log_reference(E,(x@pa)/(x@mix.A))
+    yi=[];res=[rm]
+    for p in pa:
+        y,r=log_reference(E,p/p.sum());yi.append(y);res.append(r)
+    resid=np.sum(pa*(ym-np.asarray(yi)),axis=1)/mix.prm.aeff
+    components=np.array([mix.lngamma_comb(x),resid,mix.lngamma_disp(x,T)])
+    if not np.isfinite(components).all():raise ValueError('nonfinite independent endpoint')
+    return (components if parts else components.sum(0)), max(res)
+
+
+def fresh_stencils(model,T):
+    """Three-point one-sided derivative of g, with c rebuilt exactly at every x.
+
+    Richardson columns are diagnostics; round-off amplification is reported.
+    """
+    cache={0.:0.};values={}
+    for h in HS:
+        for x in (h,2*h):
+            if x not in cache:
+                v,_=reference_value(model,T,x)
+                cache[x]=float(np.array([x,1-x])@v)
+        values[f'fd2_{h:g}']=(4*cache[h]-cache[2*h])/(2*h)
+    return values
+
+
+def prepare(a):
+    from r5_scorecard import freeze
+    from r3_common import WATER,read_sigma,write_sigma
+    out=fresh(a.out);reg=registration(a.registration)
+    freeze(argparse.Namespace(out=str(out/'assets'),profile_root=a.profile_root,registration=reg))
+    cfg=json.loads((out/'assets/config.json').read_text())
+    d=pd.read_csv(cfg['universe']['idac']['path'])
+    # Remove responses before handing any data to numerical acceptance workers.
+    q=d[['r5_row_id','solute','solvent','T','split']].copy()
+    q.to_csv(out/'queries.csv',index=False)
+    from zcosmo.cosmosac import sigma_path
+    os.environ.pop('ZC_SIGMA_OVERRIDE_DIR',None)
+    water=sigma_path(WATER)
+    if water is None:raise FileNotFoundError(WATER)
+    p=out/'water_stress';p.mkdir()
+    background=Path(cfg['overlays']['open636'])
+    for f in background.glob('*.sigma'):
+        if f.stem!=WATER:(p/f.name).symlink_to(f.resolve())
+    s,po,meta=read_sigma(background/(WATER+'.sigma'));_,pu,_=read_sigma(water)
+    meta.update(source='R6 diagnostic UD water shape at fixed open area and volume, not adopted')
+    write_sigma(p/(WATER+'.sigma'),s,pu/pu.sum()*po.sum(),meta)
+    inputs=dict(cfg['inputs']);inputs.update(cfg['open_inputs']);inputs.update(cfg['UD_inputs'])
+    for source in ('scripts/r6_endpoint.py','scripts/r6_common.py'):
+        inputs[str(Path(source).resolve())]=sha(source)
+    inputs[str((out/'queries.csv').resolve())]=sha(out/'queries.csv')
+    inputs[str((p/(WATER+'.sigma')).resolve())]=sha(p/(WATER+'.sigma'))
+    write(out/'config.json',dict(base=BASE,registration=reg,rows=str(out/'queries.csv'),
+          variants={'UD':None,'open630':cfg['overlays']['open630'],'open636':cfg['overlays']['open636'],
+                    'water_stress':str(p)},inputs=inputs))
+
+
+def worker(a):
+    cfg=json.loads(Path(a.config).read_text());check_inputs(cfg['inputs'])
+    reg=registration(cfg['registration']);directory=cfg['variants'][a.arm]
+    os.environ.pop('ZC_SIGMA_OVERRIDE_DIR',None);os.environ.pop('ZC_ONLY_KEYS',None)
+    if directory:os.environ['ZC_SIGMA_OVERRIDE_DIR']=directory
+    os.environ['ZC_R6_ENDPOINT']='0'
+    from zcosmo.z0x import Z0xBinary
+    from r3_common import STALL_KEYS
+    d=pd.read_csv(cfg['rows']);rows=[];cache={};t0=time.perf_counter()
+    for r in d.itertuples():
+        q=dict(r5_row_id=r.r5_row_id,solute=r.solute,solvent=r.solvent,T=float(r.T),split=r.split,status='',error='')
+        if a.arm=='open630' and (r.solute in STALL_KEYS or r.solvent in STALL_KEYS):
+            q['status']='excluded_by_design';rows.append(q);continue
+        if directory:
+            for k in (r.solute,r.solvent):
+                if not (Path(directory)/(k+'.sigma')).is_file():raise FileNotFoundError('No UD fallback: '+k)
+        key=(r.solute,r.solvent,float(r.T))
+        if key in cache:q.update(cache[key]);rows.append(q);continue
+        values={'legacy':np.nan,'candidate':np.nan};errors=[]
+        os.environ['ZC_R6_ENDPOINT']='0'
+        t=time.perf_counter()
+        try:
+            m=Z0xBinary([r.solute,r.solvent]);values['legacy']=float(m.lngamma_inf(r.T,0))
+        except Exception as ex:errors.append('legacy: '+repr(ex))
+        values['legacy_s']=time.perf_counter()-t
+        os.environ['ZC_R6_ENDPOINT']='1';t=time.perf_counter();new=None
+        try:
+            new=Z0xBinary([r.solute,r.solvent]);values['candidate']=float(new.lngamma_inf(r.T,0))
+        except Exception as ex:errors.append('candidate: '+repr(ex))
+        values['candidate_s']=time.perf_counter()-t
+        finite=np.isfinite([values['legacy'],values['candidate']])
+        if not finite.any():
+            values.update(status='baseline_nonfinite',error='; '.join(errors))
+        elif not finite.all():
+            values.update(status='coverage_changed',error='; '.join(errors))
+        else:
+            try:
+                ref,res=reference_value(new,r.T,0.);values['reference']=float(ref[0]);values['pure_solvent']=float(ref[1])
+                values['reference_residual']=res
+                rev=Z0xBinary([r.solvent,r.solute]);values['reverse_error']=abs(float(rev.lngamma_inf(r.T,1))-values['candidate'])
+                values['api_error']=abs(float(new.lngamma(r.T,np.array([0.,1.]))[0])-values['candidate'])
+                values['change']=values['candidate']-values['legacy']
+                values['reference_error']=abs(values['candidate']-values['reference'])
+                values.update(fresh_stencils(new,r.T))
+                err=np.array([abs(values[f'fd2_{h:g}']-values['reference']) for h in HS])
+                values['best_fd2_error']=float(err.min())
+                valid=(values['reference_error']<1e-8 and values['reverse_error']<1e-8 and
+                       values['api_error']<1e-10 and abs(ref[1])<1e-9)
+                values['status']='checked' if valid else 'check_failed'
+            except Exception as ex:values.update(status='check_failed',error=repr(ex))
+        cache[key]=values;q.update(values);rows.append(q)
+    output=pd.DataFrame(rows);output.to_csv(a.out,index=False)
+    check_inputs(cfg['inputs'])
+    write(str(a.out)+'.json',dict(base=BASE,registration=reg,arm=a.arm,rows=len(output),
+          unique_queries=len(cache),wall_s=time.perf_counter()-t0,statuses=output.status.value_counts().to_dict()))
+
+
+def summarize(a):
+    cfg=json.loads(Path(a.config).read_text());check_inputs(cfg['inputs']);result={};passed=True;artifacts={}
+    expected=pd.read_csv(cfg['rows']).set_index('r5_row_id')
+    from r3_common import STALL_KEYS
+    for arm in cfg['variants']:
+        d=pd.read_csv(Path(a.out)/(arm+'.csv'))
+        if d.r5_row_id.duplicated().any() or set(d.r5_row_id)!=set(expected.index):raise ValueError('missing, extra, or duplicate observation identity')
+        d=d.set_index('r5_row_id').loc[expected.index].reset_index()
+        for col in ('solute','solvent','split'):
+            if list(d[col])!=list(expected[col]):raise ValueError('query labels changed')
+        if not np.allclose(d['T'],expected['T'],atol=1e-12,rtol=0):raise ValueError('query temperatures changed')
+        excluded=(expected.solute.isin(STALL_KEYS)|expected.solvent.isin(STALL_KEYS)).to_numpy() if arm=='open630' else np.zeros(len(d),bool)
+        if not np.array_equal(d.status=='excluded_by_design',excluded):raise ValueError('exclusion policy changed')
+        artifacts[str((Path(a.out)/(arm+'.csv')).resolve())]=sha(Path(a.out)/(arm+'.csv'))
+        good=d.status=='checked';eligible=d.status!='excluded_by_design'
+        # Recheck numerical flags, so a malformed CSV cannot turn a failed result into a pass.
+        if good.any():
+            g=d.loc[good]
+            required=['legacy','candidate','reference','reference_error','reverse_error','api_error','pure_solvent']
+            if not np.isfinite(g[required].to_numpy(float)).all():raise ValueError('nonfinite checked result')
+            if not ((g.reference_error<1e-8)&(g.reverse_error<1e-8)&(g.api_error<1e-10)&(abs(g.pure_solvent)<1e-9)).all():
+                raise ValueError('checked status disagrees with numerical limits')
+        nf=d.status=='baseline_nonfinite'
+        if nf.any() and np.isfinite(d.loc[nf,['legacy','candidate']].to_numpy(float)).any():
+            raise ValueError('nonfinite status disagrees with values')
+        # Candidate is evaluated even when legacy failed. Preserve identical nonfinite coverage.
+        passed &= bool(d.loc[eligible,'status'].isin(['checked','baseline_nonfinite']).all() and good.any())
+        records=[]
+        for split in ('all','test'):
+            sub=d if split=='all' else d[d['split']!='train'];g=sub[sub.status=='checked']
+            rec=dict(split=split,requested=len(sub),checked=len(g),statuses=sub.status.value_counts().to_dict())
+            if len(g):
+                e=abs(g.change)
+                rec.update(mean_abs_change=float(e.mean()),max_abs_change=float(e.max()),
+                    counts_above={str(t):int((e>t).sum()) for t in (1e-3,1e-2,.05,.1)},
+                    max_reference_error=float(g.reference_error.max()),
+                    fd2_inconclusive_rows=int((g.best_fd2_error>=1e-5).sum()))
+            records.append(rec)
+        result[arm]=records
+        for role in ('solute','solvent'):
+            d[d.status=='checked'].groupby(role)['change'].agg(['count','mean','min','max']).to_csv(Path(a.out)/(arm+'-'+role+'s.csv'))
+    write(Path(a.out)/'gate.json',dict(base=BASE,registration=cfg['registration'],
+          numerical_gate=passed,arms=result,experimental_response_used=False,
+          config_sha256=sha(a.config),audit_csv_inputs=artifacts,
+          meaning='A numerical correction of the same endpoint model; historical scores stay unchanged.'))
+    if not passed:raise SystemExit(2)
+
+
+def run(a):
+    out=fresh(a.out);cfg=json.loads(Path(a.config).read_text())
+    for arm in cfg['variants']:
+        subprocess.run([sys.executable,str(Path(__file__).resolve()),'worker','--config',str(Path(a.config).resolve()),
+                        '--arm',arm,'--out',str(out/(arm+'.csv'))],check=True)
+    summarize(a)
+
+
+
+def timing_worker(a):
+    cfg=json.loads(Path(a.config).read_text());check_inputs(cfg['inputs'])
+    directory=cfg['variants'][a.arm]
+    os.environ.pop('ZC_SIGMA_OVERRIDE_DIR',None);os.environ.pop('ZC_ONLY_KEYS',None)
+    if directory:os.environ['ZC_SIGMA_OVERRIDE_DIR']=directory
+    os.environ['ZC_R6_ENDPOINT']=str(a.flag)
+    from zcosmo.z0x import Z0xBinary
+    from r3_common import STALL_KEYS
+    rows=pd.read_csv(cfg['rows']);cache={};values=[]
+    t=time.perf_counter()
+    for r in rows.itertuples():
+        if a.arm=='open630' and (r.solute in STALL_KEYS or r.solvent in STALL_KEYS):continue
+        key=(r.solute,r.solvent)
+        try:
+            if key not in cache:cache[key]=Z0xBinary(list(key))
+            v=float(cache[key].lngamma_inf(r.T,0))
+        except Exception:v=np.nan
+        values.append(v)
+    write(a.out,dict(flag=a.flag,arm=a.arm,rows=len(values),finite_rows=int(np.isfinite(values).sum()),wall_s=time.perf_counter()-t))
+    check_inputs(cfg['inputs'])
+
+
+def timing(a):
+    cfg=json.loads(Path(a.config).read_text());out=fresh(a.out);answer={}
+    for arm in cfg['variants']:
+        times={0:[],1:[]}
+        for rep in range(3):
+            for flag in ((0,1) if rep%2==0 else (1,0)):
+                p=out/f'{arm}-{rep}-{flag}.json'
+                subprocess.run([sys.executable,str(Path(__file__).resolve()),'timing_worker',
+                    '--config',str(Path(a.config).resolve()),'--arm',arm,'--flag',str(flag),'--out',str(p)],check=True)
+                times[flag].append(json.loads(p.read_text())['wall_s'])
+        answer[arm]=dict(legacy_s=times[0],candidate_s=times[1],
+                        median_speedup=float(np.median(times[0])/np.median(times[1])))
+    write(out/'summary.json',dict(timings=answer,scope='Fresh-process matched query sequence; no profiler or reference solve in the timed section.'))
+
+
+def score(a):
+    # This intentionally separate command reads responses only after numerical acceptance.
+    cfg=json.loads(Path(a.config).read_text());check_inputs(cfg['inputs'])
+    run=Path(a.run);gate=run/'gate.json';g=json.loads(gate.read_text())
+    check_inputs(g['audit_csv_inputs'])
+    if g['config_sha256']!=sha(a.config):raise ValueError('gate configuration changed')
+    decision=json.loads(Path(a.acceptance_record).read_text())
+    if not g['numerical_gate'] or decision.get('decision')!='accepted' or decision.get('numerical_gate_sha256')!=sha(gate):
+        raise ValueError('A recorded acceptance of this exact numerical gate is required')
+    from r3_common import cluster_ci
+    asset=json.loads((Path(a.config).parent/'assets/config.json').read_text())
+    record=asset['universe']['idac']
+    if sha(record['path'])!=record['sha256']:raise ValueError('frozen scoring universe changed')
+    u=pd.read_csv(record['path']).set_index('r5_row_id')
+    out=fresh(a.out);records=[]
+    for arm in cfg['variants']:
+        d=pd.read_csv(run/(arm+'.csv')).set_index('r5_row_id')
+        if set(d.index)!=set(u.index) or not d.index.is_unique:raise ValueError('score universe changed')
+        d['response']=u.loc[d.index,'ln_gamma_inf']
+        for split in ('all','test'):
+            q=d if split=='all' else d[d['split']!='train']
+            f=q[q.status=='checked'];er=f.legacy-f.response;ec=f.candidate-f.response
+            sid=np.where(f.solute<f.solvent,f.solute+'|'+f.solvent,f.solvent+'|'+f.solute)
+            records.append(dict(arm=arm,split=split,requested_rows=len(q),finite_paired_rows=len(f),
+                legacy_MAE=float(abs(er).mean()),candidate_MAE=float(abs(ec).mean()),
+                delta_MAE_CI95=cluster_ci(abs(ec)-abs(er),sid),
+                source='R6 numerical endpoint correction; historical P27 files not overwritten'))
+        d.to_csv(out/(arm+'.csv'))
+    write(out/'scores.json',dict(acceptance_sha256=sha(a.acceptance_record),tables=records))
+
+def main():
+    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
+    q=s.add_parser('prepare');q.add_argument('--profile-root',default='data/pyscf_sigma');q.add_argument('--registration',required=True);q.add_argument('--out',required=True)
+    for name in ('run','worker','summarize','timing','timing_worker'):
+        q=s.add_parser(name);q.add_argument('--config',required=True);q.add_argument('--out',required=True)
+        if name in ('worker','timing_worker'):q.add_argument('--arm',required=True)
+        if name=='timing_worker':q.add_argument('--flag',type=int,choices=[0,1],required=True)
+    q=s.add_parser('score');q.add_argument('--config',required=True);q.add_argument('--run',required=True)
+    q.add_argument('--acceptance-record',required=True);q.add_argument('--out',required=True)
+    a=p.parse_args();globals()[a.cmd](a)
+if __name__=='__main__':main()
```

**P29: complete unified diff**

<!-- PATCH:P29 -->
```diff
--- /dev/null
+++ b/scripts/r6_ensemble.py
@@ -0,0 +1,157 @@
+"""Conformer evidence audit and finite-state thermodynamic kernel.
+
+Electronic energies alone never define populations here. A liquid-population
+calculation requires nuclear and conductor-to-environment free energies; missing
+terms are errors, never silently zero. No profile or score is deployed.
+"""
+from __future__ import annotations
+import argparse
+import json
+from pathlib import Path
+import numpy as np
+from r3_common import read_sigma
+from r6_common import BASE,sha,write,fresh,registration,boltzmann,profile_envelope
+
+
+def inventory(a):
+    out=fresh(a.out);registration(a.registration)
+    manifests=sorted(Path(a.proposals).rglob('proposals.json'))
+    if not manifests:raise ValueError('no frozen proposals')
+    found={}
+    for p in sorted(Path(a.artifacts).rglob('result.json')):
+        r=json.loads(p.read_text());key=r.get('input_sha256')
+        if key:found.setdefault(key,[]).append((p,r))
+    rows=[]
+    for p in manifests:
+        m=json.loads(p.read_text())
+        cases=[c for c in m.get('cases',[]) if c['probe']]
+        if not cases:continue
+        states=[];profiles=[];energies=[];sources=[]
+        for c in cases:
+            proposal=p.parent/c['path']
+            if sha(proposal)!=c['sha256']:raise ValueError('frozen proposal changed')
+            hits=found.get(c['sha256'],[])
+            if len(hits)>1:raise ValueError('duplicate run for one frozen input: '+c['path'])
+            if not hits:
+                states.append(dict(proposal=c['path'],status='never_run'));continue
+            f,r=hits[0];states.append(dict(proposal=c['path'],status=r['status'],result_sha256=sha(f)))
+            if r['status']!='stationary_sample':continue
+            profile=f.parent/(m['key']+'.sigma')
+            if not profile.is_file():raise FileNotFoundError(profile)
+            _,v,_=read_sigma(profile);profiles.append(v);energies.append(r['E_TZVP_Eh']*627.509474)
+            sources.append(dict(profile=str(profile.resolve()),sha256=sha(profile),proposal=c['path']))
+        row=dict(key=m['key'],manifest_sha256=sha(p),expected=len(cases),states=states,
+                 complete=len(profiles)==len(cases),available_profiles=sources)
+        if profiles:
+            row['sampled_envelope']=profile_envelope(profiles)
+            row['electronic_energy_range_kcal']=[float(min(energies)),float(max(energies))]
+            row['population_status']='not computed: duplicate basins, degeneracy, nuclear entropy and environment transfer require an audit'
+        rows.append(row)
+    write(out/'inventory.json',dict(base=BASE,registration=a.registration,molecules=rows,
+          adoption=False,reference='Conductor electronic energies of the available P26 samples only'))
+
+
+def populations(a):
+    d=json.loads(Path(a.input).read_text());registration(d['registration'])
+    required=('basin','E_conductor_kcal','F_nuclear_kcal','mu_from_conductor_kcal','degeneracy')
+    states=d['states']
+    if not states or any(any(k not in s for k in required) for s in states):
+        raise ValueError('All basin free-energy terms must be supplied explicitly')
+    if len({s['basin'] for s in states})!=len(states):raise ValueError('duplicate basin, not degeneracy')
+    if d.get('environment') not in ('conductor','fixed_environment'):
+        raise ValueError('This kernel does not solve a self-consistent liquid environment')
+    if not d.get('common_standard_state') or not d.get('thermal_protocol'):
+        raise ValueError('Common energy reference and nuclear partition protocol are mandatory')
+    g=np.array([s['E_conductor_kcal']+s['F_nuclear_kcal']+s['mu_from_conductor_kcal'] for s in states])
+    if d['environment']=='conductor' and any(s['mu_from_conductor_kcal']!=0 for s in states):
+        raise ValueError('Conductor reference must not include its solvation energy twice')
+    w,f=boltzmann(g,float(d['T']),[s['degeneracy'] for s in states])
+    report=dict(T=d['T'],environment=d['environment'],states=[s['basin'] for s in states],
+                weights=w.tolist(),free_energy_kcal=f,adopted=False,input_sha256=sha(a.input),
+                note='For a liquid, environment potentials must be derivatives of a single specified free-energy functional.')
+    if all('profile' in s for s in states):
+        ps=[read_sigma(s['profile'])[1] for s in states]
+        report['sampled_envelope']=profile_envelope(ps)
+        report['average_psigmaA']=np.einsum('k,kij->ij',w,np.asarray(ps)).tolist()
+        report['warning']='Average profile is a moment approximation; its gamma is not the log partition-function chemical potential.'
+    write(a.out,report)
+
+
+
+def rotor_free_energy(x_A,masses,T,symmetry_number):
+    """Classical rigid-rotor contribution for the specified isolated isotropic reference.
+
+    Translational standard-state terms cancel within one molecular formula.
+    Symmetry is an input audited from molecular symmetry, never embedding count.
+    """
+    from scipy.constants import h,k,pi,physical_constants
+    x=np.asarray(x_A,float);m=np.asarray(masses,float)
+    if int(symmetry_number)!=symmetry_number or symmetry_number<1:raise ValueError('positive integer rotational symmetry number required')
+    x=x-np.average(x,axis=0,weights=m)
+    I=sum(w*(np.dot(r,r)*np.eye(3)-np.outer(r,r)) for w,r in zip(m,x))
+    vals=np.linalg.eigvalsh(I)*physical_constants['atomic mass constant'][0]*1e-20
+    factor=8*pi*pi*k*T/(h*h)
+    if vals[-1]<=0:raise ValueError('atomic species has no molecular rotor partition')
+    if vals[0]<1e-10*vals[-1]:q=factor*np.sqrt(vals[1]*vals[2])/symmetry_number
+    else:q=np.sqrt(pi)*factor**1.5*np.sqrt(np.prod(vals))/symmetry_number
+    return float(-.00198720425864083*T*np.log(q))
+
+
+def conductor(a):
+    """Build a reference-only thermal ensemble from a complete, audited basin catalog.
+
+    Does not turn reference weights into liquid weights or publish an activity coefficient.
+    """
+    from r6_referee import thermo_harmonic
+    catalog=json.loads(Path(a.catalog).read_text());registration(catalog['registration'])
+    entries=catalog['basins'];out=fresh(a.out)
+    if not entries or len({r['id'] for r in entries})!=len(entries):raise ValueError('distinct audited basins required')
+    if not catalog.get('basin_and_symmetry_audit'):raise ValueError('explicit basin/symmetry audit identifier required')
+    states=[];key=None;formula=None
+    for r in entries:
+        folder=Path(r['referee']);report=json.loads((folder/'status.json').read_text())
+        if sha(folder/'status.json')!=r['status_sha256']:raise ValueError('referee result changed')
+        if report['status']!='diagnostic_complete' or not report['force_gate'] or not report['thermal_gate']:
+            raise ValueError('all basin stationarity/thermal checks must pass')
+        if key is None:key=report['key']
+        if report['key']!=key:raise ValueError('one molecular species per conformer catalog')
+        if sha(folder/'local.npz')!=report['local_data_sha256'] or sha(folder/'center.sigma')!=report['center_profile_sha256']:
+            raise ValueError('native mode or profile data changed')
+        data=np.load(folder/'local.npz',allow_pickle=False)
+        atoms=tuple(sorted(data['sym'].tolist()))
+        if formula is None:formula=atoms
+        if atoms!=formula:raise ValueError('conformer stoichiometry changed')
+        states.append((r,report,data,read_sigma(folder/'center.sigma')))
+    import pandas as pd
+    eps=pd.read_csv('results/qc/dielectric.csv').set_index('inchikey').loc[key,'eps']
+    quantum=pd.read_csv('results/qc/dispersion.csv').set_index('inchikey').loc[key]
+    results=[]
+    for T in (250.,298.15,400.):
+        G=[];d=[];ps=[];vol=[];microstates=[]
+        for r,rep,dat,(_,p,meta) in states:
+            freq=rep['frequencies_cm1'][0]
+            internal=thermo_harmonic(freq,T)+rotor_free_energy(dat['x'],dat['masses'],T,r['rotational_symmetry_number'])
+            electronic=rep['center_E_TZVP_Eh']*627.509474
+            G.append(electronic+internal);d.append(r['degeneracy']);ps.append(p);vol.append(meta['volume [A^3]'])
+            profile=Path(r['referee'])/'center.sigma'
+            microstates.append(dict(id=r['id'],molecule=key,E_conductor_kcal=electronic,F_nuclear_kcal=internal,
+                degeneracy=r['degeneracy'],eps=float(eps),C6_au=float(quantum.C6_au),alpha_au=float(quantum.alpha_au),
+                profile=str(profile.resolve()),profile_sha256=sha(profile)))
+        w,f=boltzmann(G,T,d);mean=np.einsum('k,kij->ij',w,np.array(ps))
+        write(out/f'catalog_{T:g}.json',dict(T=T,states=microstates,registration=catalog['registration'],
+            thermal_protocol='R6 conductor harmonic plus classical rigid rotor',basin_and_symmetry_audit=catalog['basin_and_symmetry_audit'],
+            dielectric_sha256=sha('results/qc/dielectric.csv'),dispersion_sha256=sha('results/qc/dispersion.csv')))
+        results.append(dict(T=T,weights=w.tolist(),free_energy_kcal=f,mean_psigmaA=mean.tolist(),mean_volume_A3=float(w@vol),
+            delta_G_kcal=(np.array(G)-min(G)).tolist()))
+    write(out/'reference_ensemble.json',dict(key=key,basins=[r['id'] for r in entries],results=results,
+        catalog_sha256=sha(a.catalog),adopted=False,
+        scope='Finite listed-basin conductor reference, harmonic plus classical rigid rotor. No liquid transfer, no completeness certificate.'))
+
+def main():
+    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
+    q=s.add_parser('inventory');q.add_argument('--proposals',default='cloud/r5/proposals');q.add_argument('--artifacts',required=True)
+    q.add_argument('--out',required=True);q.add_argument('--registration',required=True)
+    q=s.add_parser('populations');q.add_argument('--input',required=True);q.add_argument('--out',required=True)
+    q=s.add_parser('conductor');q.add_argument('--catalog',required=True);q.add_argument('--out',required=True)
+    a=p.parse_args();globals()[a.cmd](a)
+if __name__=='__main__':main()
--- /dev/null
+++ b/scripts/r6_phase.py
@@ -0,0 +1,159 @@
+"""Prospective A finite-basin extension of Z0x, for computational probes only.
+
+Conductor energies plus nuclear free energies define intrinsic basin offsets.
+Pure-conformer contact and London terms supply explicit hypothetical pure-liquid
+standards. Equilibrate conformers before subtracting the pure chemical standard.
+No measured property is an input. A finite multistart solve is not a global certificate.
+"""
+from __future__ import annotations
+import argparse
+import itertools
+import json
+from pathlib import Path
+import numpy as np
+from scipy.optimize import minimize
+from scipy.special import softmax,logsumexp
+from r6_common import sha,write,registration
+
+
+class PhaseModel:
+    def __init__(self,states,T,prm,c0):
+        from zcosmo.cosmosac import R_KCAL,HARTREE_KCAL,BOHR_A,solve_gamma,delta_w
+        if not 250<=T<=400:raise ValueError('R6 probe temperatures are restricted to 250..400 K')
+        self.T=float(round(T,6));self.RT=R_KCAL*self.T;self.prm=prm;self.c0=float(c0)
+        self.states=states;self.labels=list(dict.fromkeys(s['molecule'] for s in states))
+        if len(self.labels)>2 or not self.labels:raise ValueError('one or two chemical species per R6 probe')
+        self.groups=[np.array([j for j,s in enumerate(states) if s['molecule']==name],int) for name in self.labels]
+        if any(len(g)>4 for g in self.groups):raise ValueError('at most four audited basins per species in this pilot')
+        self.fl=[s['fluid'] for s in states];self.pa=np.array([f.psigA.ravel() for f in self.fl]);self.A=self.pa.sum(1);self.V=np.array([f.V for f in self.fl])
+        self.eps=np.array([s['eps'] for s in states],float)
+        C=np.array([s['C6_au'] for s in states]);alpha=np.array([s['alpha_au'] for s in states])
+        if np.any(C<=0) or np.any(alpha<=0) or np.any(self.eps<1) or np.any(self.V<=0):raise ValueError('invalid pure input table')
+        for g in self.groups:
+            if not np.all(self.eps[g]==self.eps[g[0]]):raise ValueError('conformers retain the same frozen chemical permittivity')
+            if not np.all(C[g]==C[g[0]]) or not np.all(alpha[g]==alpha[g[0]]):raise ValueError('conformers retain the same frozen chemical D4 data')
+        d=2*(3*self.V/(4*np.pi))**(1/3)/BOHR_A
+        cij=2*C[:,None]*C[None,:]/((alpha[None,:]/alpha[:,None])*C[:,None]+(alpha[:,None]/alpha[None,:])*C[None,:])
+        self.e=-cij/((d[:,None]+d[None,:])/2)**6*HARTREE_KCAL
+        self.w=2*self.e-np.diag(self.e)[:,None]-np.diag(self.e)[None,:]
+        self.L=prm.w_dsp*prm.z/(2*self.RT)
+        energy=np.array([s['E_conductor_kcal']+s['F_nuclear_kcal'] for s in states],float)
+        deg=np.array([s['degeneracy'] for s in states],float)
+        if not np.isfinite(energy).all() or np.any(deg<=0) or not np.isfinite(deg).all():raise ValueError('invalid basin free energies or multiplicity')
+        # Separate energy gauges per chemical species cancel from every activity coefficient.
+        for g in self.groups:energy[g]-=energy[g].min()
+        self.g0=energy/self.RT-np.log(deg)
+        for a,f in enumerate(self.fl):
+            c=self.c0*(self.eps[a]-1)/(self.eps[a]+.5)
+            E=np.exp(-delta_w(self.T,prm.with_(A_ES=c))/self.RT)
+            y=np.log(solve_gamma(E,self.pa[a]/self.A[a]))
+            self.g0[a]+=self.pa[a]@y/prm.aeff+self.L*self.e[a,a]
+
+    def excess(self,x):
+        from zcosmo.cosmosac import Mixture,solve_gamma,_pure_lnG,SIG
+        x=np.asarray(x,float)
+        if x.shape!=(len(self.fl),) or np.any(x<0) or abs(x.sum()-1)>1e-10:raise ValueError('invalid microstate fractions')
+        V=x@self.V;eps=(x*self.V)@self.eps/V;c=self.c0*(eps-1)/(eps+.5)
+        prm=self.prm.with_(A_ES=c,disp_mode='none');mix=Mixture(None,prm,fluids=self.fl)
+        p=(x@self.pa)/(x@self.A);E=mix._E(self.T);ym=np.log(solve_gamma(E,p))
+        yp=np.array([_pure_lnG(f.key,self.T,prm,self.pa[j].tobytes()) for j,f in enumerate(self.fl)])
+        res=np.sum(self.pa*(ym-yp),axis=1)/prm.aeff
+        sig=np.tile(SIG,3);ED=E*(sig[:,None]+sig[None,:])**2
+        z=p*np.exp(ym);zp=self.pa/self.A[:,None]*np.exp(yp)
+        gc=((x@self.A)*(z@ED@z)-(x*self.A)@np.einsum('ki,ij,kj->k',zp,ED,zp))/(2*self.RT*prm.aeff)
+        dc=self.c0*1.5*self.V*(self.eps-eps)/(V*(eps+.5)**2)
+        gdisp=.5*self.L*(x@self.w@x);mudisp=self.L*(self.w@x)-gdisp
+        mu=mix.lngamma_comb(x)+res+gc*dc+mudisp
+        return mu,float(x@mu)
+
+    def free(self,x):
+        mu,ge=self.excess(x);positive=x>0
+        return float(x@self.g0+np.sum(x[positive]*np.log(x[positive]))+ge)
+
+    def equilibrium(self,chemical_x,budget=2000):
+        X=np.asarray(chemical_x,float)
+        if X.shape!=(len(self.groups),) or (X<0).any() or abs(X.sum()-1)>1e-12:raise ValueError('invalid chemical composition')
+        active=[(g,v) for g,v in zip(self.groups,X) if v>0]
+        size=sum(len(g)-1 for g,v in active);calls=0
+        def unpack(t):
+            x=np.zeros(len(self.fl));pos=0
+            for g,v in active:
+                w=softmax(np.r_[t[pos:pos+len(g)-1],0.]);pos+=len(g)-1;x[g]=v*w
+            return x
+        if size==0:
+            x=unpack(np.empty(0));return dict(x=x,free_energy_RT=self.free(x),model_calls=1,stationary=True,globally_certified=False)
+        starts=[np.zeros(size)]
+        for chosen in itertools.product(*(range(len(g)) for g,v in active)):
+            t=[]
+            for (g,v),j in zip(active,chosen):
+                a=np.zeros(len(g));a[j]=4.;t.extend((a-a[-1])[:-1])
+            starts.append(np.asarray(t))
+        records=[]
+        def objective(t):
+            nonlocal calls
+            calls+=1
+            if calls>budget:raise RuntimeError('fixed equilibrium model-call budget exhausted')
+            x=unpack(t);ex,ge=self.excess(x);positive=x>0
+            f=float(x@self.g0+np.sum(x[positive]*np.log(x[positive]))+ge)
+            grad=[]
+            for g,v in active:
+                w=x[g]/v;mu=self.g0[g]+np.log(x[g])+ex[g]
+                grad.extend((v*w*(mu-w@mu))[:-1])
+            return f,np.asarray(grad)
+        for t in starts:
+            ans=minimize(objective,t,jac=True,method='L-BFGS-B',bounds=[(-80.,80.)]*size,
+                         options={'ftol':1e-13,'gtol':1e-10,'maxiter':150,'maxls':30})
+            x=unpack(ans.x);ex,_=self.excess(x);error=0.
+            for g,v in active:error=max(error,float(abs(x[g]/v-softmax(-self.g0[g]-ex[g])).max()))
+            records.append(dict(x=x,F=self.free(x),fixed_point_error=error,optimizer_success=bool(ans.success)))
+        good=[r for r in records if r['fixed_point_error']<1e-8]
+        if len(good)!=len(records):raise RuntimeError('one or more fixed multistarts failed the stationarity check')
+        best=min(good,key=lambda r:r['F'])
+        return dict(x=best['x'],free_energy_RT=best['F'],model_calls=calls,stationary=True,
+                    stationary_free_energy_spread=max(r['F'] for r in good)-best['F'],globally_certified=False)
+
+    def idac(self,solute,solvent):
+        if solute==solvent or len(self.groups)!=2:raise ValueError('two distinct chemical species required')
+        i=self.labels.index(solute);j=self.labels.index(solvent)
+        xi=np.eye(2)[i];xj=np.eye(2)[j]
+        ri=self.equilibrium(xi);rj=self.equilibrium(xj)
+        ex,_=self.excess(rj['x']);group=self.groups[i]
+        insertion=self.g0[group]+ex[group]
+        value=-logsumexp(-insertion)-ri['free_energy_RT']
+        return dict(ln_gamma_inf=float(value),solute_trace_populations=softmax(-insertion).tolist(),
+            solute_pure_populations=ri['x'][group].tolist(),solvent_populations=rj['x'][self.groups[j]].tolist(),
+            pure_solute_model_calls=ri['model_calls'],pure_solvent_model_calls=rj['model_calls'],
+            globally_certified=False,adopted=False)
+
+
+def main():
+    p=argparse.ArgumentParser();p.add_argument('--catalog',required=True);p.add_argument('--solute',required=True);p.add_argument('--solvent',required=True);p.add_argument('--out',required=True)
+    a=p.parse_args()
+    from zcosmo.cosmosac import Fluid
+    from zcosmo.models import load_z_params
+    from zcosmo.zmodel import c_es_theory
+    from r3_common import read_sigma
+    d=json.loads(Path(a.catalog).read_text());registration(d['registration'])
+    if float(d['T']) not in (250.,298.15,400.):raise ValueError('R6 catalog temperature outside the fixed panel')
+    if not d.get('thermal_protocol') or not d.get('basin_and_symmetry_audit'):raise ValueError('thermal/reference and basin/symmetry provenance required')
+    import pandas as pd
+    eps_table=pd.read_csv('results/qc/dielectric.csv').set_index('inchikey')
+    d4_table=pd.read_csv('results/qc/dispersion.csv').set_index('inchikey')
+    states=[];inputs={p:sha(p) for p in ('results/qc/dielectric.csv','results/qc/dispersion.csv','results/z_params/Z0.json')}
+    for s in d['states']:
+        for k in ('id','molecule','E_conductor_kcal','F_nuclear_kcal','degeneracy','eps','C6_au','alpha_au','profile','profile_sha256'):
+            if k not in s:raise ValueError('missing basin input: '+k)
+        key=s['molecule']
+        if s['eps']!=float(eps_table.loc[key,'eps']) or s['C6_au']!=float(d4_table.loc[key,'C6_au']) or s['alpha_au']!=float(d4_table.loc[key,'alpha_au']):
+            raise ValueError('Frozen dielectric/D4 input changed')
+        if sha(s['profile'])!=s['profile_sha256']:raise ValueError('basin profile changed')
+        _,ps,m=read_sigma(s['profile']);r=dict(s);r['fluid']=Fluid(s['molecule']+':'+s['id'],ps,float(ps.sum()),m['volume [A^3]'],m.get('disp. flag','NHB'),None,m)
+        states.append(r);inputs[s['profile']]=s['profile_sha256']
+    if len({(s['molecule'],s['id']) for s in states})!=len(states):raise ValueError('duplicate basin ID')
+    model=PhaseModel(states,float(d['T']),load_z_params('Z0'),c_es_theory(fpol=1.))
+    answer=model.idac(a.solute,a.solvent);answer.update(T=d['T'],registration=d['registration'],catalog_sha256=sha(a.catalog),profile_inputs=inputs,
+        scope='New A finite-basin Z0x extension with explicit pure-conformer standards; theoretical probe only, not a registered score.')
+    from r6_common import check_inputs
+    check_inputs(inputs)
+    write(a.out,answer);print(json.dumps(answer,indent=2))
+if __name__=='__main__':main()
```

**P30: complete unified diff**

<!-- PATCH:P30 -->
```diff
--- /dev/null
+++ b/scripts/r6_jobs.py
@@ -0,0 +1,129 @@
+"""Run a frozen local job manifest with per-job locks, deadlines and explicit outcomes.
+
+A censored member cannot prevent independent later members from running.
+No retries, shell evaluation, workflow dispatch or stale-lock deletion are performed.
+"""
+from __future__ import annotations
+import argparse
+import json
+import os
+from pathlib import Path
+import signal
+import subprocess
+import sys
+import time
+from r6_common import sha,write,fresh,registration,check_inputs
+
+
+def execute(jobs,out,cwd,reg):
+    out=fresh(out);summary=[]
+    ids=[j['id'] for j in jobs]
+    if len(set(ids))!=len(ids) or not ids:raise ValueError('nonempty unique job ids required')
+    for j in jobs:
+        if not j['id'].replace('-','').replace('_','').isalnum():raise ValueError('unsafe job id')
+        command=j['argv'];limit=float(j['timeout_s'])
+        if not isinstance(command,list) or not command or not all(isinstance(v,str) for v in command):
+            raise ValueError('argv must be a nonempty string array, not a shell command')
+        if not 0<limit<=7200:raise ValueError('per-job timeout must be in (0,7200] seconds')
+        check_inputs(j.get('inputs',{}))
+        lock=Path(j['lock']).resolve();lock.parent.mkdir(parents=True,exist_ok=True)
+        # The manifest must assign the SAME lock to every writer of one output/checkpoint.
+        try:fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
+        except FileExistsError:
+            summary.append(dict(id=j['id'],status='locked_not_run'));write(out/'jobs.json',summary);continue
+        os.write(fd,json.dumps(dict(pid=os.getpid(),job=j['id'],registration=reg)).encode());os.close(fd)
+        started=time.perf_counter();p=None
+        try:
+            env=dict(os.environ);env.update(j.get('env',{}))
+            with (out/(j['id']+'.log')).open('wb') as f:
+                p=subprocess.Popen(command,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
+                timedout=False
+                try:rc=p.wait(timeout=limit)
+                except subprocess.TimeoutExpired:
+                    timedout=True
+                    os.killpg(p.pid,signal.SIGTERM)
+                    try:rc=p.wait(timeout=10)
+                    except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);rc=p.wait()
+            status='deadline' if timedout else ('completed' if rc==0 else 'censored' if rc==2 else 'failed')
+            summary.append(dict(id=j['id'],status=status,returncode=rc,wall_s=time.perf_counter()-started,
+                                command=command,registration=reg))
+        except Exception as ex:
+            summary.append(dict(id=j['id'],status='failed',error=repr(ex),wall_s=time.perf_counter()-started))
+        finally:
+            if p is not None and p.poll() is None:
+                os.killpg(p.pid,signal.SIGKILL);p.wait()
+            # Deliberately retained after an outer SIGKILL, which requires human review.
+            lock.unlink(missing_ok=True)
+        write(out/'jobs.json',summary)
+    return 0 if all(r['status']=='completed' for r in summary) else 2
+
+
+
+def plan_referee(a):
+    reg=registration(a.registration);out=fresh(a.out);cases=[]
+    root=Path(a.artifacts);inputs={}
+    plan=Path('cloud/r5/shape-plan/manifest.json');manifest=json.loads(plan.read_text());inputs[str(plan.resolve())]=sha(plan)
+    # Structural calibration controls, chosen before any new numerical result.
+    for name in ('methanol','ethylene_glycol'):
+        r=next(q for q in manifest['panel'] if q['name']==name)
+        gp=plan.parent/r['geometry']
+        if sha(gp)!=r['geometry_sha256']:raise ValueError('control geometry differs from frozen R5 bytes')
+        cases.append(dict(id=name,key=r['key'],smiles=r['smiles'],source=gp,spin=r['spin']))
+    targets=[('BKIMMITUMNQMOS-UHFFFAOYSA-N',20261006,1),
+             ('ZIBGPFATKBEMQZ-UHFFFAOYSA-N',20261006,1),
+             ('XTHFKEDIFFGKHM-UHFFFAOYSA-N',20261005,1)]
+    for key,seed,rank in targets:
+        pp=Path('cloud/r5/proposals')/key/f's{seed}-c{rank}.json'
+        if not pp.is_file():raise FileNotFoundError(pp)
+        proposal=json.loads(pp.read_text());identity=sha(pp);hits=[]
+        for path in root.rglob('result.json'):
+            r=json.loads(path.read_text())
+            if r.get('input_sha256')==identity:hits.append((path,r))
+        if len(hits)!=1:raise ValueError('exactly one archived result required for each frozen censored member')
+        path,r=hits[0]
+        if r['status']!='censored' or r['evaluations']!=80:raise ValueError('the frozen censoring result changed')
+        gp=path.parent/'latest.json'
+        cases.append(dict(id=key[:14],key=key,smiles=proposal['smiles'],source=gp,spin=proposal['spin']))
+        inputs[str(path.resolve())]=sha(path);inputs[str(pp.resolve())]=identity
+    env=dict(OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',ZC_PCM3C_MB='2000',ZC_PCM3C='1',PYTHONPATH='src:scripts')
+    jobs=[];records=[]
+    for r in cases:
+        gp=out/'geometries'/(r['id']+'.json');gp.parent.mkdir(exist_ok=True)
+        gp.write_bytes(Path(r['source']).read_bytes());inputs[str(gp)]=sha(gp)
+        dest=out/'consistency'/r['id']
+        jobs.append(dict(id=r['id'],argv=[sys.executable,str(Path('scripts/r6_referee.py').resolve()),'consistency',
+            '--geometry',str(gp),'--key',r['key'],'--smiles',r['smiles'],'--spin',str(r['spin']),
+            '--registration',reg,'--out',str(dest)],lock=str(out/'locks'/(r['id']+'.lock')),timeout_s=3600,env=env))
+        records.append(dict(id=r['id'],key=r['key'],smiles=r['smiles'],spin=r['spin'],geometry=str(gp),geometry_sha256=sha(gp),consistency=str(dest)))
+    for f in ('scripts/r6_referee.py','scripts/r6_jobs.py','scripts/r3_precision.py','src/zcosmo/pcm_lu.py','src/zcosmo/pyscf_cosmo.py'):
+        inputs[str(Path(f).resolve())]=sha(f)
+    write(out/'jobs.json',dict(registration=reg,cwd=os.getcwd(),inputs=inputs,jobs=jobs,cases=records))
+
+
+def plan_modes(a):
+    source=json.loads(Path(a.manifest).read_text());check_inputs(source['inputs']);out=fresh(a.out);jobs=[];inputs=dict(source['inputs'])
+    for r in source['cases']:
+        path=Path(r['consistency'])/'status.json';d=json.loads(path.read_text())
+        if d['status']!='diagnostic_complete' or not d['full_response_consistent'] or d['input_sha256']!=r['geometry_sha256']:
+            raise ValueError('all five fixed consistency cases must pass before optional Hessians')
+        inputs[str(path.resolve())]=sha(path)
+        env=source['jobs'][0]['env']
+        jobs.append(dict(id=r['id'],argv=[sys.executable,str(Path('scripts/r6_referee.py').resolve()),'modes',
+            '--geometry',r['geometry'],'--key',r['key'],'--spin',str(r['spin']),'--consistency',str(path),
+            '--registration',source['registration'],'--out',str(out/r['id'])],
+            lock=str(out/'locks'/(r['id']+'.lock')),timeout_s=7200,env=env))
+    write(out/'jobs.json',dict(registration=source['registration'],cwd=os.getcwd(),inputs=inputs,jobs=jobs))
+
+
+def main():
+    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
+    q=s.add_parser('run');q.add_argument('--manifest',required=True);q.add_argument('--out',required=True)
+    q=s.add_parser('plan_referee');q.add_argument('--artifacts',required=True);q.add_argument('--registration',required=True);q.add_argument('--out',required=True)
+    q=s.add_parser('plan_modes');q.add_argument('--manifest',required=True);q.add_argument('--out',required=True)
+    a=p.parse_args()
+    if a.cmd!='run':globals()[a.cmd](a);return
+    m=json.loads(Path(a.manifest).read_text());reg=registration(m['registration']);check_inputs(m.get('inputs',{}))
+    rc=execute(m['jobs'],a.out,m.get('cwd',os.getcwd()),reg)
+    write(Path(a.out)/'manifest.json',dict(input_sha256=sha(a.manifest),registration=reg))
+    raise SystemExit(rc)
+if __name__=='__main__':main()
--- /dev/null
+++ b/scripts/r6_referee.py
@@ -0,0 +1,247 @@
+"""Bounded local stationarity and profile-sensitivity diagnostic, NOT a new optimizer.
+
+No stopped long chain may enter this pilot. This produces no Berny convergence
+claim, Hessian positivity certificate, liquid ensemble, or production profile.
+The observed finite-stress envelope is not a bound over a geometry ball.
+"""
+from __future__ import annotations
+import argparse
+from importlib.metadata import version
+import json
+import os
+import time
+from pathlib import Path
+import numpy as np
+from scipy.linalg import null_space
+from scipy.constants import physical_constants, c, pi
+from r3_common import STALL_KEYS
+from r4_common import geometry
+from r6_common import BASE,sha,write,fresh,registration,profile_envelope
+
+
+def projected_modes(H, xyz_bohr, masses):
+    """Cartesian Hessian Eh/Bohr^2, masses in amu. Remove rigid-body subspace."""
+    x=np.asarray(xyz_bohr,float);m=np.asarray(masses,float)
+    n=len(m);r=x-np.average(x,axis=0,weights=m);sm=np.sqrt(m)
+    rigid=[]
+    for e in np.eye(3):
+        rigid.append((sm[:,None]*np.broadcast_to(e,(n,3))).ravel())
+        rigid.append((sm[:,None]*np.cross(np.broadcast_to(e,(n,3)),r)).ravel())
+    rigid=np.column_stack(rigid)
+    Q=null_space(rigid.T,rcond=1e-10)
+    mass=np.repeat(sm,3);K=np.asarray(H)/mass[:,None]/mass[None,:]
+    D=Q.T@((K+K.T)/2)@Q;vals,U=np.linalg.eigh(D)
+    vectors=(Q@U)/mass[:,None]
+    Eh=physical_constants['Hartree energy'][0]
+    bohr=physical_constants['Bohr radius'][0]
+    amu=physical_constants['atomic mass constant'][0]
+    scale=np.sqrt(Eh/(bohr*bohr*amu))/(2*pi*c*100)
+    freq=np.sign(vals)*np.sqrt(abs(vals))*scale
+    return vals,vectors,freq
+
+
+def thermo_harmonic(freq_cm,T):
+    """Diagnostic quantum harmonic internal free energy, no absolute-value/floor rescue."""
+    from scipy.constants import h,k,N_A
+    nu=np.asarray(freq_cm,float)
+    if (nu<=0).any() or not np.isfinite(nu).all():raise ValueError('nonpositive vibrational mode: harmonic partition invalid')
+    z=h*c*100*nu/(k*T)
+    return float(np.sum(.5*h*c*100*nu*N_A/4184 + .00198720425864083*T*np.log(-np.expm1(-z))))
+
+
+def modes(a):
+    reg=registration(a.registration)
+    if a.key in STALL_KEYS:raise ValueError('Stopped-chain campaign remains closed; this pilot excludes those six keys')
+    if version('pyscf')!='2.14.0' or version('pyberny')!='0.7.0':raise RuntimeError('Pinned PySCF/pyberny required')
+    from r3_precision import factory
+    from zcosmo.pyscf_cosmo import BOHR,cosmo_segments,to_profiles,write_sigma
+    sym,x=geometry(a.geometry)
+    evidence=json.loads(Path(a.consistency).read_text())
+    if evidence['input_sha256']!=sha(a.geometry) or not evidence['full_response_consistent']:
+        raise ValueError('Matched full-response consistency evidence required before Hessians')
+    os.environ['ZC_R3_COOH_FLAG']='1'
+    # Two central-difference Hessians plus two center checks; fixed ceiling.
+    expected=12*len(sym)+2
+    if expected>360:raise ValueError(f'{expected} gradients exceed the 360-call pilot cap')
+    out=fresh(a.out);start=time.perf_counter();records=[]
+    write(out/'status.json',dict(status='running',base=BASE,registration=reg,input_sha256=sha(a.geometry),expected_gradients=expected))
+    def check_deadline():
+        if time.perf_counter()-start>7000:raise TimeoutError('7000-second internal deadline; no extension')
+    def eg(pos,tight):
+        check_deadline()
+        mf=factory(sym,np.asarray(pos),a.spin,tight,4000)
+        e=mf.kernel()
+        if not mf.converged or not np.isfinite(e):raise RuntimeError('SCF failed')
+        grad=mf.nuc_grad_method();grad.grid_response=bool(tight)
+        g=np.asarray(grad.kernel())
+        if not np.isfinite(g).all():raise RuntimeError('nonfinite gradient')
+        records.append(dict(energy_Eh=float(e),gmax=float(abs(g).max()),tight=tight))
+        write(out/'calls.json',records)
+        return float(e),g,mf
+    try:
+        e0,g0,_=eg(x,False);e1,g1,mf=eg(x,True)
+        Hs=[]
+        for step in (.003,.006):  # Bohr, not Angstrom
+            H=np.zeros((3*len(sym),3*len(sym)))
+            for j in range(3*len(sym)):
+                delta=np.zeros_like(x);delta.ravel()[j]=step*BOHR
+                _,gp,_=eg(x+delta,True);_,gm,_=eg(x-delta,True)
+                H[:,j]=((gp-gm)/(2*step)).ravel()
+            Hs.append(H)
+        masses=mf.mol.atom_mass_list(isotope_avg=True)
+        modes=[projected_modes(H,x/BOHR,masses) for H in Hs]
+        freqs=[q[2] for q in modes];negative=any((nu < -20).any() for nu in freqs)
+        force_gate=bool(abs(g1).max()<5e-5 and np.sqrt(np.mean(g1*g1))<1.5e-5)
+        # Hessians are finite-difference diagnostics. Frequencies near zero are not clipped.
+        report=dict(base=BASE,registration=reg,key=a.key,input_sha256=sha(a.geometry),
+            original_energy_Eh=e0,tight_energy_Eh=e1,original_gmax=float(abs(g0).max()),
+            tight_gmax=float(abs(g1).max()),tight_grms=float(np.sqrt(np.mean(g1*g1))),
+            delta_gradient_max=float(abs(g1-g0).max()),force_gate=force_gate,
+            significant_negative_sampled_mode=negative,frequencies_cm1=[nu.tolist() for nu in freqs],
+            Hessian_step_difference_max=float(abs(Hs[0]-Hs[1]).max()),
+            Hessian_asymmetry_max=[float(abs(H-H.T).max()) for H in Hs],
+            gradients=len(records),Berny_converged=False,adopted=False)
+        np.savez_compressed(out/'local.npz',x=x,sym=np.array(sym),g_original=g0,g_tight=g1,H_small=Hs[0],H_large=Hs[1],masses=masses)
+        if negative or not force_gate:
+            report.update(status='stationarity_failed',wall_s=time.perf_counter()-start)
+            write(out/'status.json',report);return 2
+        # All candidate thermo numbers remain diagnostics; no floor for soft/imaginary modes.
+        if all((nu>0).all() for nu in freqs):
+            report['harmonic_F_kcal']={str(T):[thermo_harmonic(nu,T) for nu in freqs] for T in (250.,298.15,400.)}
+            report['thermal_gate']=max(abs(v[0]-v[1]) for v in report['harmonic_F_kcal'].values())<.05
+        else:report['thermal_gate']=False
+        ps=[];frames=[('center',x)];profile_energies=[]
+        # Fixed six softest vibrational directions, two amplitudes, both signs.
+        # 25 profiles maximum; counted separately from quantum gradients.
+        for j in range(min(6,modes[0][1].shape[1])):
+            v=modes[0][1][:,j].reshape(-1,3)
+            v=v/np.max(np.linalg.norm(v,axis=1))
+            for amp in (.005,.010):
+                for sign in (-1,1):frames.append((f'm{j}-a{amp}-s{sign}',x+sign*amp*v))
+        for name,pos in frames:
+            check_deadline();seg,e=cosmo_segments(sym,pos,spin=a.spin);p,meta=to_profiles(sym,pos,seg)
+            meta.update(source='R6 local stress diagnostic, not adopted',geometry_converged='R6-diagnostic',r6_registration=reg)
+            write_sigma(out/(name+'.sigma'),p,meta,a.key)
+            ps.append(np.array([p.psigmaA_nhb,p.psigmaA_OH,p.psigmaA_OT]));profile_energies.append(float(e))
+        report['center_E_TZVP_Eh']=profile_energies[0]
+        report['center_profile_sha256']=sha(out/'center.sigma')
+        report['local_data_sha256']=sha(out/'local.npz')
+        report['profiles']=len(ps);report['sampled_profile_envelope']=profile_envelope(ps)
+        report['scope']='Finite local stress sample; neither a basin-wide stability bound nor a local-minimum certificate.'
+        report['wall_s']=time.perf_counter()-start;report['status']='diagnostic_complete'
+        write(out/'status.json',report)
+    except Exception as ex:
+        write(out/'status.json',dict(status='censored' if isinstance(ex,TimeoutError) else 'failed',error=repr(ex),
+              gradients=len(records),wall_s=time.perf_counter()-start,registration=reg,input_sha256=sha(a.geometry),adopted=False))
+        raise
+
+
+
+def probe_directions(smiles,sym,x):
+    """First covalent heavy-atom single-bond rotations, then fixed internal directions.
+
+    Directions are derivatives at this geometry, not minimized conformers or an
+    H-bond filter. Units are dimensionless and max atomic displacement is one.
+    """
+    from rdkit import Chem
+    mol=Chem.AddHs(Chem.MolFromSmiles(smiles))
+    if sym!=[at.GetSymbol() for at in mol.GetAtoms()]:raise ValueError('declared atom order does not match geometry')
+    adj={a.GetIdx():[n.GetIdx() for n in a.GetNeighbors()] for a in mol.GetAtoms()}
+    candidates=[]
+    for b in mol.GetBonds():
+        i,j=b.GetBeginAtomIdx(),b.GetEndAtomIdx()
+        if b.IsInRing() or b.GetBondType()!=Chem.BondType.SINGLE or min(mol.GetAtomWithIdx(i).GetAtomicNum(),mol.GetAtomWithIdx(j).GetAtomicNum())<=1:continue
+        side={j};stack=[j]
+        while stack:
+            u=stack.pop()
+            for v in adj[u]:
+                if {u,v}=={i,j} or v in side:continue
+                side.add(v);stack.append(v)
+        axis=x[j]-x[i];axis=axis/np.linalg.norm(axis);v=np.zeros_like(x)
+        for k in side:v[k]=np.cross(axis,x[k]-x[j])
+        candidates.append((f'bond-{i}-{j}',v))
+    rng=np.random.default_rng(20261006)
+    candidates.extend((f'internal-{j}',rng.normal(size=x.shape)) for j in range(8))
+    centered=x-x.mean(0);rigid=[]
+    for e in np.eye(3):
+        rigid.extend([np.broadcast_to(e,x.shape).ravel(),np.cross(np.broadcast_to(e,x.shape),centered).ravel()])
+    Q=null_space(np.asarray(rigid),rcond=1e-10);ans=[]
+    for label,v in candidates:
+        v=(Q@(Q.T@v.ravel())).reshape(x.shape)
+        length=np.max(np.linalg.norm(v,axis=1))
+        if length<1e-10:continue
+        v=v/length
+        if ans:
+            matrix=np.column_stack([w.ravel() for _,w in ans]+[v.ravel()])
+            if np.linalg.matrix_rank(matrix,tol=1e-9)<=len(ans):continue
+        ans.append((label,v))
+        if len(ans)==4:break
+    if len(ans)<min(4,Q.shape[1]):raise ValueError('insufficient independent direction probes')
+    return ans
+
+
+def consistency(a):
+    reg=registration(a.registration)
+    if a.key in STALL_KEYS:raise ValueError('The six stopped chains are outside the R6 pilot')
+    if version('pyscf')!='2.14.0' or version('pyberny')!='0.7.0':raise RuntimeError('Pinned native environment required')
+    from r3_precision import factory
+    from zcosmo.pyscf_cosmo import BOHR
+    from rdkit import rdBase
+    if rdBase.rdkitVersion!='2026.03.6':raise RuntimeError('Match the frozen R5 RDKit 2026.03.6 direction convention')
+    sym,x=geometry(a.geometry);directions=probe_directions(a.smiles,sym,x)
+    out=fresh(a.out);start=time.perf_counter();energies=[]
+    def scf(pos,tight):
+        if time.perf_counter()-start>3400:raise TimeoutError('3400-second diagnostic deadline')
+        mf=factory(sym,pos,a.spin,tight,4000);e=mf.kernel()
+        if not mf.converged or not np.isfinite(e):raise RuntimeError('SCF did not converge')
+        energies.append(float(e));write(out/'energies.json',energies)
+        return float(e),mf
+    write(out/'status.json',dict(status='running',input_sha256=sha(a.geometry),registration=reg))
+    try:
+        _,normal=scf(x,False);go=normal.nuc_grad_method()
+        if go.grid_response:raise ValueError('Baseline grid_response differs from the registered default')
+        g0=np.asarray(go.kernel());_,tight=scf(x,True)
+        gt=tight.nuc_grad_method();gt.grid_response=False;g1=np.asarray(gt.kernel())
+        gf=tight.nuc_grad_method();gf.grid_response=True;g2=np.asarray(gf.kernel())
+        if not np.isfinite([g0,g1,g2]).all():raise ValueError('nonfinite gradient')
+        records=[]
+        for name,v in directions:
+            slopes=[]
+            for h in (.003,.006):
+                ep,_=scf(x+h*BOHR*v,True);em,_=scf(x-h*BOHR*v,True)
+                slopes.append((ep-em)/(2*h))
+            reference=(4*slopes[0]-slopes[1])/3
+            projected=[float(np.sum(g*v)) for g in (g0,g1,g2)]
+            records.append(dict(direction=name,fd=slopes,Richardson=reference,
+                fd_uncertainty_indicator=abs(slopes[0]-slopes[1])/3,
+                grad_original=projected[0],grad_tight_no_response=projected[1],grad_tight_full_response=projected[2],
+                original_error=abs(projected[0]-reference),tight_error=abs(projected[1]-reference),
+                full_error=abs(projected[2]-reference)))
+        stable=all(r['fd_uncertainty_indicator']<1e-7 for r in records)
+        full=max(r['full_error'] for r in records);old=max(r['tight_error'] for r in records)
+        passed=bool(stable and full<2e-7)
+        write(out/'status.json',dict(base=BASE,registration=reg,key=a.key,status='diagnostic_complete',
+            input_sha256=sha(a.geometry),records=records,SCF_evaluations=len(energies),gradient_evaluations=3,
+            response_gradient_change_max=float(abs(g2-g1).max()),original_vs_tight_change_max=float(abs(g1-g0).max()),
+            full_response_consistent=passed,missing_response_material=bool(passed and old>5*max(full,1e-10) and old>1e-6),
+            original_gmax=float(abs(g0).max()),full_gmax=float(abs(g2).max()),
+            wall_s=time.perf_counter()-start,adopted=False,
+            scope='Four sampled directional tests; not a proof of gradient consistency everywhere or Berny convergence.'))
+        if not passed:return 2
+        return 0
+    except Exception as e:
+        write(out/'status.json',dict(status='censored' if isinstance(e,TimeoutError) else 'failed',error=repr(e),
+            input_sha256=sha(a.geometry),registration=reg,SCF_evaluations=len(energies),adopted=False))
+        raise
+
+
+def main():
+    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
+    for name in ('consistency','modes'):
+        q=s.add_parser(name);q.add_argument('--geometry',required=True);q.add_argument('--key',required=True)
+        q.add_argument('--out',required=True);q.add_argument('--registration',required=True);q.add_argument('--spin',type=int,default=0)
+        if name=='consistency':q.add_argument('--smiles',required=True)
+        else:q.add_argument('--consistency',required=True)
+    a=p.parse_args();rc=globals()[a.cmd](a)
+    if rc:raise SystemExit(rc)
+if __name__=='__main__':main()
--- /dev/null
+++ b/scripts/r6_stability.py
@@ -0,0 +1,88 @@
+"""Finite local profile-stability probe. Fresh process per immutable profile replacement.
+
+This tests the saved stress points only. It never certifies all geometries in a
+ball, supplies a ThermoML score, or marks a geometry Berny-converged.
+"""
+from __future__ import annotations
+import argparse
+import json
+import os
+from pathlib import Path
+import subprocess
+import sys
+import tempfile
+import numpy as np
+from r6_common import sha,write,fresh,check_inputs
+
+PROBES=('XLYOFNOQVPJJNP-UHFFFAOYSA-N','OKKJLVBELUTLKV-UHFFFAOYSA-N',
+        'BKIMMITUMNQMOS-UHFFFAOYSA-N','XTHFKEDIFFGKHM-UHFFFAOYSA-N')
+
+
+def worker(a):
+    key=a.key;background=Path(a.background).resolve();required=set(PROBES)|{key}
+    inputs={}
+    with tempfile.TemporaryDirectory(prefix='r6-stress-') as td:
+        for k in required:
+            p=Path(a.profile).resolve() if k==key else background/(k+'.sigma')
+            if not p.is_file():raise FileNotFoundError('no UD fallback: '+str(p))
+            inputs[str(p)]=sha(p)
+            (Path(td)/(k+'.sigma')).symlink_to(p)
+        os.environ['ZC_SIGMA_OVERRIDE_DIR']=td;os.environ['ZC_R6_ENDPOINT']='1'
+        from zcosmo.z0x import Z0xBinary
+        rows=[]
+        for other in PROBES:
+            if other==key:continue
+            for T in (250.,298.15,400.):
+                for pair in ((key,other),(other,key)):
+                    try:value=float(Z0xBinary(list(pair)).lngamma_inf(T,0));error=''
+                    except Exception as e:value=None;error=repr(e)
+                    if value is not None and not np.isfinite(value):value=None;error='nonfinite'
+                    rows.append(dict(pair=pair,T=T,value=value,error=error))
+        check_inputs(inputs)
+        write(a.out,dict(profile_sha256=sha(a.profile),inputs=inputs,rows=rows))
+
+
+def run(a):
+    plan=json.loads(Path(a.manifest).read_text());check_inputs(plan['inputs']);out=fresh(a.out)
+    reports=[];eligible=True
+    for j in plan['jobs']:
+        folder=Path(j['argv'][j['argv'].index('--out')+1]);status=json.loads((folder/'status.json').read_text())
+        if status['status']!='diagnostic_complete' or not status.get('force_gate'):
+            reports.append(dict(case=j['id'],status='local_stationarity_not_established'));eligible=False;continue
+        key=status['key'];profiles=[folder/'center.sigma']+sorted(p for p in folder.glob('*.sigma') if p.name!='center.sigma')
+        if len(profiles)!=status['profiles']:raise ValueError('stress panel changed')
+        records=[]
+        for i,p in enumerate(profiles):
+            target=out/(j['id']+f'-{i}.json')
+            subprocess.run([sys.executable,str(Path(__file__).resolve()),'worker','--key',key,
+                '--background',a.background,'--profile',str(p),'--out',str(target)],check=True)
+            records.append(json.loads(target.read_text()))
+        ref=records[0]['rows'];largest=0.;valid=True
+        expected_n=6*sum(k!=key for k in PROBES)
+        if len(ref)!=expected_n:raise ValueError('incomplete reference probe panel')
+        for r in records[1:]:
+            if len(r['rows'])!=len(ref):raise ValueError('incomplete candidate probe panel')
+            check_inputs(r['inputs'])
+            for x,y in zip(ref,r['rows']):
+                if x['pair']!=y['pair'] or x['T']!=y['T']:raise ValueError('probe identity changed')
+                if (x['value'] is None)!=(y['value'] is None):valid=False
+                if x['value'] is not None and y['value'] is not None:largest=max(largest,abs(x['value']-y['value']))
+        check_inputs(records[0]['inputs'])
+        finite=sum(r['value'] is not None for r in ref)
+        ok=bool(valid and finite>0 and largest<.01)
+        reports.append(dict(case=j['id'],finite_reference_queries=finite,max_sampled_delta_lngamma=largest,
+                            profile_stability_gate=ok,stress_profiles=len(profiles),globally_certified=False))
+        eligible &= ok
+    check_inputs(plan['inputs'])
+    write(out/'summary.json',dict(registration=plan['registration'],cases=reports,all_fixed_cases_pass=eligible,
+        scope='A declared finite diagnostic, not an accepted force-only production convergence rule.',adopted=False))
+    if not eligible:raise SystemExit(2)
+
+
+def main():
+    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
+    q=s.add_parser('run');q.add_argument('--manifest',required=True);q.add_argument('--background',required=True);q.add_argument('--out',required=True)
+    q=s.add_parser('worker')
+    for name in ('key','background','profile','out'):q.add_argument('--'+name,required=True)
+    a=p.parse_args();globals()[a.cmd](a)
+if __name__=='__main__':main()
```

**P31: complete unified diff**

<!-- PATCH:P31 -->
```diff
--- /dev/null
+++ b/scripts/r6_headline.py
@@ -0,0 +1,54 @@
+"""Reformat archived P27 comparisons, preserving pairwise denominators and LLE scope.
+
+No prediction regeneration, input change, experimental selection or new bootstrap.
+"""
+from __future__ import annotations
+import argparse
+import json
+from pathlib import Path
+from r6_common import BASE,sha,write
+
+
+def extract(d):
+    tables=d['tables'];out={}
+    for table in ('idac','vle','he','lle'):
+        pairs=tables[table]['pairwise']
+        matches=[p for p in pairs if p['model']=='Z0x' and p['arm']=='open630']
+        if len(matches)!=1:raise ValueError('one matched Z0x/open630 comparison required per table')
+        p=matches[0];r,c=p['reference'],p['candidate']
+        if r['rows']!=c['rows'] or r['rows']!=p['common_rows']:raise ValueError('matched denominator changed')
+        out[table]=p
+    return out
+
+
+def render(d):
+    q=extract(d)
+    lines=['Z0x-UD versus primary open profiles, archived P27 matched comparisons','',
+        'Historical finite-difference endpoint implementation. No R6 endpoint correction is included.','',
+        '| Quantity | Common rows | UD | Open630 | Open minus UD 95% CI |',
+        '|---|---:|---:|---:|---|']
+    for table,label in [('idac','IDAC MAE, ln units'),('vle','VLE pressure AAD, %'),('he','HE MAE, J/mol')]:
+        p=q[table];r,c=p['reference'],p['candidate'];ci=p.get('delta_MAE_CI95')
+        if ci is None:raise ValueError('paired uncertainty missing')
+        lines.append(f"| {label} | {p['common_rows']} | {r['MAE']:.6g} | {c['MAE']:.6g} | [{ci[0]:.6g}, {ci[1]:.6g}] |")
+    p=q['lle'];r,c=p['reference'],p['candidate']
+    lines.extend(['','LLE detection uses finite-grid quality accounting, not a certificate of global equilibrium.'])
+    for name,z in [('UD',r),('open630',c)]:
+        lines.append(f"{name}: {z['rows']} common rows and {z['systems']} systems; row detection {z['row_gap_found_bounds']}; "
+                     f"system detection {z['system_gap_found_bounds']}; unresolved {z['unresolved_rows']}; "
+                     f"endpoint MAE {z.get('composition_MAE')} on {z['endpoint_rows']} checked endpoint rows.")
+    lines.extend(['','Witnesses count as detections only. The positive LLE table supplies no false-positive rate or balanced accuracy.',
+        'Open630 excludes six S1/S2 compounds by design. Open636 is a separate exploratory arm, not 636 Berny-converged profiles.',
+        'The earlier 0.839 standalone UD IDAC result has 828 rows; it must not be compared as though it shared the 816-row open630 denominator.'])
+    return '\n'.join(lines)+'\n'
+
+
+def main():
+    p=argparse.ArgumentParser();p.add_argument('--input',default='docs/astra/round5/data/scorecard_test.json');p.add_argument('--out',required=True)
+    a=p.parse_args();d=json.loads(Path(a.input).read_text());text=render(d)
+    target=Path(a.out)
+    if target.exists():raise FileExistsError(target)
+    target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
+    write(str(target)+'.json',dict(source_sha256=sha(a.input),report_base=BASE,source_base=d.get('base'),comparisons=extract(d)))
+    print(text)
+if __name__=='__main__':main()
```

**REG6: complete unified diff**

<!-- PATCH:REG6 -->
```diff
--- /dev/null
+++ b/docs/astra/round6/REGISTRATION_PROPOSED.md
@@ -0,0 +1,195 @@
+Round-6 proposed registration. This is not evidence that the text has been
+adopted. Append accepted text with the actual commit timestamp before a new
+candidate output is interpreted or used. Reference main is
+43213a5e61f591a19b4d3352a95315a62ee2aeb8 plus the six archived R6 patches.
+The hypotheses are motivated by the already observed R5 results. No new result
+is represented as an experimental holdout, and no ThermoML response selects
+any numerical constant, geometry, conformer, or population.
+
+The six stopped chains remain excluded from new native jobs. Their files keep
+S1/S2 status, primary profiles_v2 remains 630/636, and P26's full protocol is
+not resumed. P15/P17/P19 rejections stand. P20's accepted metadata correction
+and P23/P27 reporting remain in place. No R6 helper writes a production profile
+or silently changes a historical scorecard.
+
+P28 is a narrowly scoped A numerical correction of the Z0x infinite-dilution
+endpoint. For a pure solvent, evaluate the unchanged fixed-coefficient Mixture
+at the pure composition, with A_ES equal to the pure solvent's dielectric
+coefficient. The chain-rule term vanishes because the frozen-coefficient
+excess Gibbs energy is identically zero at either pure endpoint for every
+coefficient. Construct this Mixture without the rounded-c lookup. The switch
+ZC_R6_ENDPOINT=1 affects lngamma_inf and lngamma at exactly x1=0 or x1=1 only.
+Its default is off. Every finite interior composition, including the existing
+near-endpoint finite-difference strip, stays unchanged. This entry does not
+certify that strip, fix the finite-composition model, or authorize a correction
+in another Z0 variant. All profile bytes, dielectric and dispersion tables,
+functional forms, and fitted/theoretical constants remain unchanged.
+
+Freeze the historical has_sigma IDAC universe from the current P27 input CSVs,
+including every row identity and split label. Run UD, open630, open636, and
+one declared stress overlay in separate processes. The stress overlay uses
+UD's normalized water profile with the native open area and volume; all other
+profiles are open636. No experimental response is sent to numerical workers.
+Open630 excludes exactly rows involving S1/S2 keys, without UD fallback.
+The old and candidate endpoints are evaluated independently even when the old
+one fails. Require identical finite coverage in every arm; matched nonfinite
+rows remain in the requested denominator. Every old finite row must be checked.
+
+The independent reference solves the same segment equations in logarithms,
+using a separate residual/Jacobian evaluation and nonlinear polish. Require
+maximum log-equation residual <=5e-12, maximum candidate-reference difference
+<1e-8 in ln gamma, component-reversal agreement <1e-8, public endpoint API
+agreement <1e-10, and pure-solvent ln gamma <1e-9. Keep every positive profile
+bin; do not threshold tiny support. A malformed, missing, or extra result row
+fails the gate. Report three-point one-sided controls at h=1e-4, 1e-5, 1e-6,
+1e-7 and 1e-8 with fresh coefficient evaluation. These controls diagnose
+truncation/cancellation; no h is chosen by experimental error. FD rows lacking
+agreement within 1e-5 are explicitly inconclusive and do not replace the
+reference equation gate. The proof and independently checked endpoint solve,
+not a supposedly optimal tiny h, define the candidate.
+
+Report counts and magnitudes of changes above 1e-3, 1e-2, 0.05 and 0.1 on all
+and test rows, with separate solute/solvent summaries. Time three fresh-process
+repetitions per arm and flag, alternating order; do not time the expensive
+reference/FD checks as production. No measured speed-up is assumed. A numerical
+pass permits recording acceptance of this exact gate hash before running the
+separate score command. That command reports old and corrected IDAC results
+on identical rows, with 1000 system bootstrap draws and seed 7. The water stress
+arm is a diagnostic, never a deployable profile set. P27's historical outputs
+are retained. A worse experimental score does not reverse a proven numerical
+correction. Any finite-composition extension needs its own gate and accounting.
+
+P29 first inventories every frozen P26 probe proposal by input hash, retaining
+censored, failed and never-run members. Duplicate runs cannot be cherry-picked.
+Known-conformer tail ranges and normalized-L1 diameters describe the supplied
+finite set only, not unsampled basins. No electronic-energy population or
+embedding-frequency multiplicity is assigned to incomplete pools.
+
+The theory definition is a phase-dependent finite-basin ensemble, not a chosen
+extended geometry and not a rule excluding intramolecular hydrogen bonds.
+For each distinct basin, retain the conductor electronic energy, the nuclear
+partition contribution, and audited symmetry/multiplicity. The nuclear term
+includes ZPE and finite-temperature vibrations or an explicitly integrated
+hindered-rotor/basin contribution, with rotational terms on a common reference.
+The same molecular translational standard state cancels between its conformers.
+An imaginary or unconverged soft mode must not be replaced by its absolute
+value or an empirical frequency floor. Intramolecular H-bonds already affect
+the electronic energy and exposure; no extra penalty or reward is added.
+
+The provided reference-ensemble helper can compute a harmonic plus classical
+rigid-rotor diagnostic only from complete audited basin inputs. Require the
+P30 force, Hessian, and two-step thermal checks for every supplied basin and
+an explicit basin/symmetry audit identifier. Distinct minima must be deduplicated
+with atom/symmetry correspondence, not by embedding frequency. Rotational
+symmetry number and additional basin degeneracy are different inputs and cannot
+count the same symmetry twice. Harmonic numerical stability is not proof of an
+accurate low-barrier torsional partition. This helper produces a labelled finite
+conductor-reference ensemble only; its averaged profile is not a liquid chemical
+potential and its weights are not automatically liquid populations.
+
+The prospective finite-basin Z0x extension is frozen in scripts/r6_phase.py.
+It uses the unchanged combinatorial and segment equations over basin species,
+volume-weighted chemical permittivities, and the symmetric extension of the
+existing London contact exchange energy. All basins of one chemical species
+retain the same frozen chemical dielectric, C6, and polarizability values.
+Conductor electronic plus nuclear free energies are augmented with the model's
+absolute pure-conformer segment and London self-contact standards before
+adding the pure-subtracted excess mixture functional. Thus pure-liquid and
+infinite-dilution populations are minimized separately under one scalar free
+energy; conductor solvation is not added twice. This is a new A closure, not
+claimed to be uniquely implied by a final sigma histogram or by COSMO-RS.
+
+The finite-state pilot is restricted to two chemical species, at most four
+audited basins each, and T=250, 298.15 and 400 K. A catalog with more
+than four distinct relevant basins is outside this pilot; do not drop basins
+merely to meet the software cap. Use the fixed uniform and
+vertex-biased starts, a shared 2000 objective-call budget per equilibrium
+problem, and the fixed stationarity checks in the code. A failed multistart
+blocks the result; a lower stationary value is not a global certificate.
+The one-basin-per-species limit must reproduce P28 to <1e-8; analytic free-energy
+derivatives must agree with independent finite differences to <1e-7 in the
+portable test; energy-zero and population-normalization checks must pass.
+
+No new quantum basin survey is authorized by P29 in R6. The command examples
+consume only explicitly supplied and audited basin partitions. The present
+incomplete P26 files do not satisfy that requirement. A later physical ensemble
+validation requires a separate prospective sampling budget on all eight frozen
+R5 validation molecules. Independent complete basin catalogs must give chemical
+free energies within 0.05 kcal/mol, normalized average profiles within 0.02 L1,
+and both-role probe ln gamma within 0.02 at the three fixed temperatures, with
+identical finite coverage. The four probes remain water, methanol, nonane and
+1,2-dimethoxyethane. Thermal partition error must also be checked independently
+of discovery-pool agreement. No R6 ensemble output is authorized for ThermoML
+scoring or for replacing the 630 primary profiles, and P26 remains unaccepted.
+
+P30 tests a specific possible source of energy/gradient inconsistency before
+attempting any new optimizer. Pin pyscf=2.14.0, pyberny=0.7.0 and the R5 direction
+construction's RDKit=2026.03.6. Freeze five geometries: saved R5 methanol and
+ethylene glycol, plus the last archived geometry of exactly these P26 censored
+members: nonane seed 20261006 rank 1, TEG seed 20261006 rank 1, and
+1,2-dimethoxyethane seed 20261005 rank 1. Their recorded 80-evaluation outcomes
+and proposal hashes must match. Do not optimize these inputs or restart any of
+the six stopped chains. The never-run tetraEG proposal is not quietly added.
+
+Per geometry, compare the original energy/gradient with tighter SCF
+conv_tol=1e-11 and conv_tol_grad=1e-7 at the same BP86/def2-SVP, DF, grid level 2,
+default pruning, project radii, C-PCM eps=1e9 and Lebedev 17. At the tight center
+compute gradients with grid_response=False and True, retaining auxiliary-basis
+and PCM responses. Compute centered energy differences at 0.003 and 0.006 Bohr
+along four deterministic internal directions. The first directions are heavy
+single-bond rotations, with the fixed projected random fallback in the helper.
+This costs at most 18 SCF evaluations and three gradients per case.
+
+The two-step derivative uncertainty indicator must be <1e-7 Eh/Bohr and maximum
+full-response gradient discrepancy <2e-7 on all sampled directions. Material
+omitted response is reported only when the tight-no-response discrepancy is
+>1e-6 and >5 times the larger of the full-response discrepancy and 1e-10.
+This is a directional test, not a proof everywhere or a claim that omitted grid
+response caused the observed stalls. Maximum budget is one four-core worker-hour
+per case, with an internal 3400-second deadline. Inconclusive results stop the
+native escalation. Do not change a threshold after reading the outputs.
+
+Only if all five fixed consistency cases pass, the optional mode/stability
+stage is allowed on the same five geometries. Use two finite-difference Cartesian
+Hessians from tight full-response gradients at steps 0.003 and 0.006 Bohr. Project
+mass-weighted translations and rotations explicitly, and record Hessian asymmetry,
+step dependence and every signed frequency. Per case the count is 12N+2 gradients,
+never above 360. Significant negative modes below -20 cm^-1 or failure of the
+new diagnostic force targets (max 5e-5 and RMS 1.5e-5 Eh/Bohr) fail stationarity.
+This new diagnostic definition is NOT an equivalence to Berny's internal
+coordinate, step, or on-sphere predicate and is never written as Berny-converged.
+
+For passing stationary candidates, evaluate the center and both signs of 0.005
+and 0.010 Angstrom maximum-atom displacements along the six softest projected
+modes, at most 25 registered TZVP profiles per case. Keep orientation, all profile
+settings and P18 metadata fixed. For a harmonic partition diagnostic all
+vibrational frequencies must be positive and the two Hessian steps must change
+F_vib by <0.05 kcal/mol at every fixed temperature. Otherwise the thermal result
+is unavailable and a hindered-rotor/basin integration would need a separately
+registered budget. There is no silent soft-frequency regularization.
+
+The optional stage has a two-worker-hour cap per case, including its stress
+profiles, with an internal 7000-second deadline. Across both native stages the
+absolute budget is 15 four-core worker-hours, with no retries, no optimization,
+and no production relabel. On the Mac, compare stress profiles against their
+own center in separate processes against the four fixed probes, in both roles
+at 250, 298.15 and 400 K using P28. Require identical finite coverage and maximum
+sampled change in ln gamma <0.01. This is an observed finite-stress envelope,
+not a certified bound on every geometry in a ball or on every thermal basin.
+Even a pass authorizes no new S1/S2 acceptance route. A future convergence rule
+for production needs its own independent validation and registration.
+
+The job runner locks each output location before starting, terminates the whole
+process group on its fixed deadline, records all return codes, and continues
+independent jobs after a failure. It never automatically deletes a stale lock,
+retries a member, or dispatches a cloud workflow. Censoring must not hide a
+never-run member as it did in one R5 slot.
+
+P31 re-renders the archived P27 matched test comparisons, with their original
+confidence intervals and row identities. No prediction is regenerated and no
+new bootstrap is run. Report IDAC and HE deficits on matched rows; describe the
+VLE increase with its paired interval, which includes zero. Keep LLE checked
+roots, gap witnesses, sampled no-gap and unresolved statuses distinct. Detection
+rates on the positive LLE table are not balanced accuracy. All headline numbers
+are explicitly before P28. Rewording a headline does not alter the historical
+score, and open636 remains separately flagged exploratory coverage.
```

