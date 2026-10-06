Z-COSMO round 7: a controlled grid-response optimization trial

Reference: `Victor-Liang-ChE/zcosmo`, `main` at `ddf22b19f9e1750308bd11572786b44d407a80f9`, the snapshot containing the round-7 prompt and recorded round-6 results. All six patches below add new files relative to that snapshot. They leave the production geometry runner, profile files and historical results unchanged. A moving `main` is not interchangeable with this pinned reference. [S1–S4]

The next justified experiment is an optimization with the configured PySCF gradient object’s `grid_response=True`. Keep the original Berny convergence predicate and every energy setting unchanged. This tests a specific mismatch between the energy and the gradient supplied to the optimizer. It does not assume that the mismatch is the sole cause of every stall. The earlier P30 gate remains failed, and its unexecuted second stage remains unexecuted.

| Rank | ID | Class | Target and mechanism | Cost, saving arithmetic and acceptance burden | Effort |
|---:|---|:---:|---|---|---|
| 1 | P32 | A, numerical-gradient correction trial | Same SVP/DF/grid-2/C-PCM-17 energy; compare grid response off and on in fresh Berny runs | Calibration: 25 pairs, at most 25 four-core worker-hours. Pilot: three pairs, at most six more. A separate, conditional six-chain trial is capped at 66 worker-hours. No speed-up is assumed for an unfinished reference. | Moderate |
| 2 | P33 | E diagnostic accounting; A numerical reference evaluations | A prospective, uncertainty-aware directional energy/gradient consistency test | Five cases, at most 82 SCF evaluations and three gradients each; ten worker-hours maximum. It replaces neither the old P30 verdict nor Berny’s stopping rule. | Moderate |
| 3 | P34 | E read-only screening; A finite-displacement probes | Check a probability-style sample of completed profiles plus fixed structural sentinels, without optimization | At most 40 cases. Each uses one SVP SCF, two gradients and three TZVP profiles. Forty worker-hours maximum; no 630-molecule reoptimization. | Moderate |
| 4 | P35 | E reporting | Record the glycol mechanism as unresolved and specify evidence that would reopen it | Zero new quantum calculations. Avoids another profile-targeted conformer search with no identifiable reference inputs. | Low |
| Shared | H7 / REG7 | E infrastructure / prospective policy | Input hashes, scientific gates, isolated execution and proposed registration | No production adoption. Tests and source checks precede native jobs. | Shared |

For discretionary planning only, assigning P32/P33/P34 respectively 60/20/30 avoidable future worker-hours, decision-usefulness probabilities 0.5/0.6/0.4 and effort units 3/2/3 gives the brief’s `saving × probability / effort` scores of 10, 6 and 4. These are explicit planning assumptions, not observed savings or probabilities. The table’s hard execution caps are separate. P35 is a reporting decision, not a throughput claim. Savings overlap and must not be added.

## What the existing evidence supports

On the three P26-censored geometries, some torsional directions show a production gradient with the opposite sign to the energy’s finite difference. For example, the nonane bond-3–4 direction has a Richardson slope of about `+5.62e-5 Eh/Bohr`, a tight no-response gradient of `−1.76e-5`, and a tight full-response gradient of `+5.33e-5`. TEG and DME have comparable examples. These are promising reasons to test the optimization itself. [S5–S7]

They are not a completed causality test. A different nonane direction agrees more closely with the no-response gradient. The largest remaining full-response discrepancy is about `3.9e-5` for DME; methanol’s full-response discrepancy is not smaller than its original one. None of the five cases passed P30’s registered absolute consistency gate. In the old JSON, `missing_response_material=false` is conditional on a gate that failed. It does not establish that the omitted response is immaterial. [S5–S9]

The six stopped long chains were not directly tested in P30. The evidence concerns three different, shorter censored structures plus two controls. Extending the interpretation to all six long chains is a hypothesis. The new pilot is therefore a prerequisite to a bounded chain reattempt, not a reason to restart the old drivers immediately.

The relevant objective is a discretized energy, schematically

\[
 E_h(R)=\sum_g w_g(R)\,\epsilon_{xc}[\rho(R;r_g(R))]+E_{\mathrm{other}}(R).
\]

Its derivative includes the response of the quadrature points and partition weights. Pinned PySCF’s RKS gradient defaults to omitting that grid response. The density-fitted implementation has a full-response branch and retains auxiliary-basis response. The solvent gradient wrapper adds PCM contributions to the underlying gradient object. Enabling XC-grid response therefore addresses an identifiable term; it does not mean that the original calculation omitted every solvent or density-fitting response. [U1–U3]

Near a flat torsional direction, an omitted derivative term can be larger than the residual gradient. The predicted energy change then becomes a poor description of the computed energy change, damaging the trust update. This is a systematic consistency error, even when the resulting ratios look noisy. SCF convergence error, adaptive quadrature decisions and soft Hessian modes can coexist with it. A small gradient from the old approximate derivative is not sufficient evidence of stationarity of the full discretized energy.

## P32: optimize with the full gradient, without changing Berny’s predicate

The implementation targets `scripts/r7_plan.py`, `scripts/r7_optimize.py` and `.github/workflows/r7_review.yml`. H7 supplies the gate and isolation helpers. It reuses the inspected `r3_precision.factory` to construct the registered energy, but uses its ordinary, non-tight settings. The only scientific difference between the paired optimization arms is the gradient object’s `grid_response` setting.

The native API is:

```python
mf = factory(sym, xyz_A, spin, tight=False, memory=4000)
grad = mf.nuc_grad_method()
grad.grid_response = True
converged, mol = pyscf.geomopt.berny_solver.kernel(
    grad,
    maxsteps=budget,
    callback=callback,
    assert_convergence=True,
    gradientmax=4.5e-4,
    gradientrms=1.5e-4,
    stepmax=1.8e-3,
    steprms=1.2e-3,
)
```

The code verifies auxiliary-basis and solvent attachment and checks the scanner’s setting at every callback. Passing `grid_response=True` as a Berny keyword while still supplying an unconfigured mean-field object is not the implementation. The pinned wrapper accepts a gradient object and converts that object to its scanner. The callback occurs before `optimizer.send`; a callback’s gradient or step data are not used as a substitute for the wrapper’s final convergence Boolean. [U2–U4]

Keep BP86, def2-SVP, density fitting, grid level 2 and its pruning, project radii, C-PCM `eps=1e9`, Lebedev 17 and `conv_tol=1e-8`. Keep the default orbital-gradient SCF tolerance. Do not enable the rejected P15 noise override or the P19 tight stage. Do not introduce a finer grid, a new Hessian model or geomeTRIC into this experiment. Those would prevent attributing the result to grid response alone.

Both arms start with fresh optimizer histories at exactly the same coordinates. No `.bstate` is read. A previous Hessian estimated with inconsistent gradients is an inappropriate starting curvature model for the new arm. Fresh histories in the control are essential: if both arms finish, a fresh restart could be the explanation, rather than the response correction.

The original internal-coordinate gradient and step limits remain in force, including Berny’s rejection of an on-sphere step. A full-response success is described as “Berny-converged under the registered R7 full-response A protocol.” It is not described as reproduction of the old approximate-gradient algorithm. It must not be confirmed by switching back to the known suspect no-response gradient, which would answer a different question.

### Calibration and its decision rule

Use the historical 25 targets and all 2,302 query occurrences, not a newly selected panel. The repository’s `validation_set.csv` contains 26 entries, so taking that whole file or deleting one arbitrary entry is wrong. The planner requires the actual archived 2,302-occurrence manifest, extracts the 25 target identities and preserves repeated occurrences. Missing or conflicting manifests stop preparation. [S10]

Generate each target’s registered seed-7 xTB starting geometry once and freeze it before either arm. Optimize both arms from that geometry, rather than timing a polish from an already converged DFT geometry. Each arm has at most 100 quantum-gradient evaluations and 1,800 seconds including its final profile. The paired worker is therefore capped at one hour of native work. The shared xTB preparation is separately identified; it is not charged twice or used to make the paired ratio look better.

Every calibration molecule must reach the original Berny predicate in both arms. The final profile calculation remains the accepted TZVP/grid-3/C-PCM-29 construction, including the applied COOH metadata correction. All 25 profiles, SCF failures and censored runs are accounted for. A failed or censored calibration member blocks compatibility; it is not omitted from the denominator.

The numerical compatibility conditions retain the P15/P19-style checks: identical finite masks on the historical occurrences; maximum absolute COSMO-SAC-dsp change below `0.01` against the paired no-response control; median absolute COSMO-SAC-dsp difference from UD below `0.15`. The historical finite counts, 2,271 for COSMO-SAC-dsp and 2,302 for Z0x, are checked explicitly. Raw and normalized bin differences and every Z0x difference are reported. These are A gates, not a relabeling of the stricter E bin criterion. The gate runs on the Mac, in separate processes per immutable profile replacement, with P28’s exact endpoint enabled consistently in both Z0x arms.

There is one explicit prospective policy change from P19: a full/control wall ratio of `1.50` is retained as a routine-throughput indicator, not as a veto on a small, separately capped rescue trial. Calibration’s `passed` field means numerical compatibility, while `routine_throughput_indicator` reports that cost test separately. The absolute calibration, pilot and chain caps remain binding. This distinction is registered before R7 outputs because an algorithm can be too expensive as the default for every molecule but still be worthwhile for a fixed set whose baseline never finishes. P19 remains rejected under its original combined gate. Nothing here changes that historical decision or authorizes a default switch on the 630 completed profiles.

### Three-pair pilot before any long chain

Freeze exactly the final P26-censored geometries used by P30: nonane seed 20261006/rank 1, TEG seed 20261006/rank 1 and DME seed 20261005/rank 1. Their proposal identities, recorded 80-evaluation censoring and geometry hashes must match. The never-run tetraethylene glycol member is outside this trial. It is not substituted for a difficult case.

After calibration compatibility passes, run off/full arms for each of the three geometries, with fresh histories, at most 80 new gradient evaluations and one hour per arm. A capped run is a censored outcome. An SCF exception, wrong input, missing result or a deadline before the first valid gradient is an operational failure, not useful censoring.

The predeclared chain-escalation condition is at least two full-only successes among the three pairs, zero off-only successes, all six outcomes present and no operationally invalid result. A full-only success means the full-response arm reaches the original Berny predicate while its matched off arm remains censored at its fixed evaluation or wall budget. One paired improvement is suggestive but does not authorize the six-chain expenditure. If both arms succeed in all cases, this is evidence for restart sensitivity and does not satisfy the grid-response-specific escalation rule.

This is a small mechanism experiment, not a population-level significance test. Record exact convergence counts, evaluations and wall times. For cases that both finish, compare actual time-to-convergence. For a censored off arm, do not invent a baseline completion time or advertise an unmeasured speed-up. “Finished in N evaluations while its control was still unfinished at 80” is the correct statement.

### Conditional six-chain reattempt and replacement eligibility

Freeze all six final stopped checkpoints before examining pilot outcomes. The planner requires one explicitly designated geometry per key and never selects the newest file from several competing checkpoints. No old driver, shared working directory or optimizer pickle is reused. This is particularly important because a previous duplicate-process race wrote the same checkpoint files. [S3]

A positive compatibility-plus-pilot decision produces a hash-bound eligibility file. It is not a cloud dispatch. A separate maintainer authorization commit records the decision hash and the frozen chain-plan hash before the chain workflow can run. A negative or incomplete decision leaves the campaign closed.

Each of the six keys then receives exactly one off arm and one full arm, each with at most 100 new gradient evaluations and 19,800 seconds, or 5.5 hours. These are separate jobs, not an 11-hour pair placed on one six-hour runner. The outer job allows time for environment setup and artifact upload, but a hosted runner’s availability is not guaranteed. No arm is resumed, extended or retried after its outcome is read. All twelve outcomes enter the record.

For a full-response arm that actually converges, replacement eligibility additionally requires SCF success, unchanged covalent connectivity, a complete finite TZVP profile and correct protocol provenance. Compare it with that key’s current flagged profile on every existing IDAC occurrence involving the key and on the four fixed probes, in both roles at 250, 298.15 and 400 K. Require identical finite coverage and maximum change below `0.05` for both Z0x and COSMO-SAC-dsp. For a chain with no benchmark occurrence, the probe requirement remains; an empty observed-data set is not a pass by itself. This is a compatibility test against the flagged input, not proof that the flagged geometry was the true minimum.

The `replacements` command verifies all twelve outcomes and writes an eligibility manifest. It does not modify `profiles_v2`, the S1/S2 folders or their metadata. A later adoption commit may select an eligible full-response result, preserving the historical flagged bytes and retaining an explicit A protocol label. That commit must update protocol-aware selection and cache provenance. Simply copying an R7 profile into an old filename and attaching the old `profile_revision` would be false provenance. A changed source revision can also make the production cache treat old profiles as stale, so no batch driver should be launched during such a migration.

An off-arm success is recorded as an ordinary original-protocol success; it is not credited to grid response. Its use would require the normal input/provenance checks. A full-response success that fails the profile-compatibility check is still a valid optimization outcome, but it is not an authorized replacement. No failed chain is reclassified as converged because other chains succeeded.

### Cost on the existing free workers

The absolute P32 maximum is `25 × 2 × 0.5 + 3 × 2 × 1 + 6 × 2 × 5.5 = 97` four-core worker-hours, or 388 core-hours, with the last 66 worker-hours conditional on a positive pilot and separate authorization. This is a ceiling, not the expected run time. It is also not a claim that any provider grants 97 hours of free capacity on demand.

For intuition only, suppose response adds 25% to each gradient evaluation. Completing in 20 evaluations costs 25 old-evaluation equivalents. Against an off arm censored at 80, that uses 31.25% of the fixed comparison budget, but it is not a measured `3.2×` time-to-convergence. If the full arm also reaches the cap, the intervention has bought no completion. Actual calibration and pilot costs replace this illustrative arithmetic.

## P33: a consistency gate tied to a stated resolution

The previous test compared two finite-difference steps, formed a Richardson estimate and required errors several orders below Berny’s force limits. Its own uncertainty indicator exceeded its permitted threshold. Preserve that result. Do not re-score the archived P30 outputs against a looser threshold and call the old experiment successful. [S4–S9]

The new referee addresses a different, prospectively stated question: is a sampled directional derivative consistent with the implemented energy to one fifth of the tighter Cartesian force scale previously proposed for local stationarity, `5e-5 Eh/Bohr`? Its target is therefore

\[
\tau = (5\times10^{-5})/5 = 10^{-5}\;\mathrm{Eh/Bohr}.
\]

This is an accuracy allocation from the declared downstream purpose, not a fitted multiplier selected to make the archived numbers pass. The new experiment may still fail. A result with inadequate resolution must remain inconclusive.

Reuse the four deterministic P30 directions, but normalize each complete Cartesian direction to Euclidean norm one. P30 instead normalized the maximum atomic displacement to one, so its directional slopes have different norm factors for different molecules. The new report saves the normalization and does not compare old and new absolute slopes without transforming them.

Use the fixed centered-displacement ladder `h = 0.016, 0.008, 0.004, 0.002, 0.001 Bohr`. At every displaced geometry compute the energy at two fixed SCF precisions: `conv_tol=1e-11, conv_tol_grad=1e-7` and `conv_tol=1e-12, conv_tol_grad=1e-8`. The functional, basis and grid are unchanged. At the center compute the two full-response gradients and the stricter no-response gradient. There are two center SCFs plus `4 directions × 5 steps × 2 signs × 2 precisions = 80` displaced SCFs, for 82 SCFs and three gradients per case.

For each precision define

\[
 D(h)=\frac{E(R+hv)-E(R-hv)}{2h},\qquad
 R(h)=\frac{4D(h/2)-D(h)}{3}.
\]

The software uses the finest fixed Richardson result and builds an uncertainty indicator from the full change between the last two Richardson results, the last two tight/stricter precision differences, the center full-gradient precision difference and a conservative floating-point cancellation allowance. It does not pick whichever step happens to agree best with the gradient. It requires the Richardson sequence to stabilize and records retained-grid counts; a count change blocks an affirmative result.

Let `d=|g_full·v−R_finest|` and let `u` be that indicator. A direction passes only when `u ≤ τ/4` and `d+u ≤ τ`. It is inconsistent when the resolved lower discrepancy `d−u` exceeds `τ`. All other outcomes are inconclusive. A topology/stabilization warning also gives an inconclusive result. The same classification is made for the off-response gradient. Omitted response is marked material only when the full gradient passes and the off gradient is inconsistent; when the full reference is unresolved, that field is `null`, not `false`.

These are numerical engineering tests. The two SCF tolerances do not prove bounds on energy error, and unchanged grid counts do not prove that every adaptive grid decision is differentiable. A coincidentally small Richardson difference is possible. The result is not an interval-arithmetic certificate or a proof of stationarity in all directions. A future Hessian/thermal calculation needs its own accuracy budget and a corresponding validated gradient, not a Boolean borrowed from this screening test.

Run the same five geometries as P30. Each has a two-hour four-core cap, ten worker-hours total. No optimizer is run by this referee. Its result neither changes P30’s failed verdict nor activates the old R6 Hessian stage. P32 is a direct bounded intervention test and does not require all five P33 cases to pass before its pilot; however, no report should claim a fully validated energy derivative or a uniquely established root cause when P33 remains inconclusive.

A finer, fixed grid or different pruning policy could address residual quadrature effects, but it changes the discretized objective and would be another A experiment. Do not automatically try it after a failed case. First retain the error decomposition and decide whether the problem is insufficient finite-difference resolution, SCF sensitivity or a resolved derivative discrepancy. That is more informative than an unregistered grid sweep.

## P34: screen the 630 completed profiles without reoptimizing them

The omission is in the shared gradient path, so it can affect molecules that met the old convergence test. That does not establish that all 630 geometries are materially wrong. A full rerun is unnecessary for a first check, and a small old gradient cannot certify a small geometry error in a soft direction.

Freeze the entire primary-profile inventory and take 32 keys ordered by `SHA256('R7-primary-screen-v1|' + key)`. Add the fixed sentinel set water, methanol, nonane, EG, DEG, TEG, glycerol and propylene glycol. Overlap is deduplicated; the maximum is 40 cases. Selection uses neither ThermoML error nor a new gradient. Every selected geometry and its profile bytes are hashed before native work.

For each selected saved geometry, perform one SVP SCF and compute both off/full-response gradients at that same density. Record their difference and the full gradient separately. A response correction above `1e-5 Eh/Bohr` is a force-screen indicator, not a Berny convergence verdict. Cartesian components are not substituted for Berny’s internal-coordinate limits.

Project the full gradient out of rigid translations and rotations. Use its negative internal direction for one fixed stress test, normalized to maximum atomic motion one. Compute the unchanged TZVP profile at the center and at both signs of `0.010 Å` along that direction. When the projected gradient is numerically zero, use the fixed structural direction construction, not an error-selected displacement. This is three single points, no geometry optimization and no line search.

Recompute the center at the saved coordinates before comparing the stresses. Saved XYZ rounding means a newly computed center is not necessarily bit-identical to the original profile-generating geometry. Report the stored-versus-recomputed difference separately. Compare each stressed profile against its own center in fresh model processes using the fixed probes and both roles. Retain identical finite coverage and label any maximum ln-gamma change of `0.01` or more a positive sensitivity screen. Force and profile indicators are separate columns; neither is hidden by the other.

A positive stress demonstrates sensitivity at the declared displacement. A negative screen demonstrates stability only for the tested displacements and probes. It says nothing about whether the actual corrected optimum lies within `0.010 Å`. In a genuinely strongly convex neighborhood, a bound such as

\[
\|R-R_*\|\leq\|\nabla E(R)\|/\lambda_{\min}
\]

would need a valid curvature lower bound on that neighborhood, and a profile-error bound would also need control of the profile derivative. The observed soft modes are precisely why substituting “small force” for these missing ingredients would be unsafe.

The 32-key component permits a conditional sampling summary of this operational screen. The helper supplies an exact finite-population, one-sided upper count based on the hypergeometric distribution only when all 32 sampled outcomes are usable. Its interpretation assumes the predeclared hash ordering is treated as an error-independent random sample. With zero positives, the familiar binomial approximation is `1−0.05**(1/32) ≈ 0.0894`, which already shows why a clean sample would not certify all 630. The exact helper uses population size 630. Sentinels are reported descriptively and are not mixed into that sampling calculation. Missing, censored or failed cases remain visible and block the complete-sample bound.

The budget is at most 40 SVP SCFs, 80 gradients and 120 TZVP single points, with one worker-hour per case. The model-affinity checks run on the Mac. No completed profile is replaced by a stress profile. Positive evidence motivates a separately budgeted follow-up; negative evidence supports only a bounded statement about the sample and tested scale.

## P35: the glycol mechanism remains unresolved

Record the gap and stop the present profile-targeted conformer campaign. The sampled conformers do not span the UD tail for several glycols, and the unavailable UD generating inputs prevent a unique historical explanation. Continuing to choose extended conformers until the tail resembles UD would select a profile against a target, rather than implement a defined equilibrium model. [S11]

For fixed raw profiles `p_c` and nonnegative weights summing to one, any linear tail-area functional satisfies

\[
T\!\left(\sum_cw_cp_c\right)=\sum_cw_cT(p_c)
\in[\min_cT(p_c),\max_cT(p_c)].
\]

That is why no weighting of the supplied EG/DEG/TEG samples can reproduce the larger recorded UD tail. It does not rule out an unsampled conformer, a different electronic representation or a different cavity construction. A normalized-profile average has its own normalized-tail envelope; raw-area and normalized constraints must not be mixed. The sampled tail envelope also does not bound an ensemble chemical potential from a nonlinear, environment-dependent model.

Keep the limits of P25 explicit. Its particular basis, switching and averaging variants did not close the gap. It did not test every electronic method or recreate a DMol3 generating calculation. The earlier statement that the deficit is “already in the raw charges” is an upstream diagnosis within the open pipeline. Without the corresponding UD raw segment table, it is not a matched raw-open versus raw-UD measurement.

Evidence that would justify reopening this question includes identifiable UD coordinates and generating settings, an independently specified calculation with raw charges and a documented cavity, or a completed basin/thermal/transfer audit whose predicted observables can be checked without choosing on ThermoML. Absence from the Mac is not proof that no upstream author or archive can supply the inputs. Conversely, finding an input archive does not authorize using a guessed member or undocumented settings.

The R7 grid-response trial has a narrower role. A correction to stationarity could change sampled conformer energies or profiles, so old off-response conformer samples may need to be distinguished from new ones. Even a successful optimizer does not complete basin discovery, determine degeneracy or supply nuclear free energies. It does not adopt the unfinished P26 protocol, establish liquid conformer populations or prove that UD is the correct liquid profile. No extra quantum budget is allocated in P35 to chase the missing tail.

Water, glycerol and propylene glycol remain useful counterexamples to a universal “open OH tail is too small” story. P24 already showed that the same sign of a shape-induced prediction change can improve one solvent and worsen another because their starting biases differ. The H2O flag does not enter Z0x’s London term. Do not introduce a water-specific flag, an intramolecular-H-bond exclusion or a tail rescaling to force a common explanation. [S2, S11]

## Current claims and implementation defects to keep visible

The accepted P28 correction is retained consistently in new Z0x affinity checks. The archived matched headline of IDAC `0.8040` versus `0.9423` on 816 observations is explicitly pre-P28. The corrected standalone values, approximately `0.8397` on 828 UD observations and `0.9427` on 816 open630 observations, are not a matched comparison. Do not manufacture the corrected matched UD value by adding a standalone average increment. P28 was accepted on its numerical gate even though the test MAE rose slightly. [S2–S4]

Primary open coverage remains 630 Berny-converged profiles. The six S1/S2 inputs remain exploratory unless an individual result passes the newly registered replacement route. The open pipeline is a reproducible alternative profile source with documented model-dependent errors; the available matched results do not support accuracy equivalence to UD. VLE’s paired interval includes zero, while the IDAC and HE deficits have positive paired intervals. LLE detection on the positive LLE table is not balanced accuracy, and a gap witness supplies no accepted endpoint composition.

Several operational issues deserve explicit attention. The old shared-checkpoint driver race makes file locking a correctness requirement, not an optional optimization. A scientific gate failure must not be labeled wall-time censoring merely because both use exit code 2. A rejected first case must not prevent another independently registered case from running, as happened in an earlier slot loop. The new bounded runner records native scientific statuses separately from process failures, keeps persistent claim files and continues independent work without retrying a member. A green artifact-upload job is not evidence that a scientific gate passed.

The old callback is pre-send, and the learned Hessian is not an exact molecular Hessian. None of the new code treats a stored trust radius or model-Hessian eigenvalue as a stationarity certificate. Diagnostic memory limits are also advisory: `max_memory=4000` does not guarantee a four-gigabyte process RSS, especially for full grid response. An OOM is a failed trial case, not permission to change its grid or silently move it to an unlimited machine.

## Exact setup and execution commands

The scripts below consume private, existing assets where those assets actually reside. `H25` is the archived 2,302-occurrence CSV or a directory containing its unique copy. `STOPPED_CHECKPOINTS` is the explicitly designated folder of the six final stopped geometries. These are required scientific inputs, not filenames inferred from the current 26-entry validation list. `PROFILE_ROOT` is the Mac’s accepted `data/pyscf_sigma` collection. All UD-backed commands run on that Mac.

The native cloud workflow is supplied, but this report does not dispatch it. Installation commands reproduce the native pins used in the repository. They are commands for an environment with package access, not a claim that installation succeeded in this session.

```bash
set -euo pipefail
export REPO="$PWD"
export BASE=ddf22b19f9e1750308bd11572786b44d407a80f9
export REPORT="${REPORT:-$REPO/ZCOSMO_ROUND7_REPORT.md}"
export H25="${H25:?Set the path to the actual historical 2302-occurrence manifest}"
export STOPPED_CHECKPOINTS="${STOPPED_CHECKPOINTS:?Set the designated final six-checkpoint folder}"
export PROFILE_ROOT="${PROFILE_ROOT:-$REPO/data/pyscf_sigma}"
export WORK="$(mktemp -d "${TMPDIR:-/tmp}/zcosmo-r7.XXXXXX")"
export TREE="$WORK/repo"
export BRANCH="astra-round7-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$WORK/patches"
python - "$REPORT" "$WORK/patches" <<'PYCODE'
from pathlib import Path
import re,sys
text=Path(sys.argv[1]).read_text()
blocks=re.findall(r'<!-- PATCH:(H7|P32|P33|P34|P35|REG7) -->\s*```diff\n(.*?)\n```',text,re.S)
expected={'H7','P32','P33','P34','P35','REG7'}
assert len(blocks)==6 and {k for k,_ in blocks}==expected
for name,body in blocks:Path(sys.argv[2],name+'.patch').write_text(body+'\n')
PYCODE
git -C "$REPO" worktree add -b "$BRANCH" "$TREE" "$BASE"
test "$(git -C "$TREE" rev-parse HEAD)" = "$BASE"
for patch in H7 P32 P33 P34 P35 REG7; do
  git -C "$TREE" apply --check "$WORK/patches/$patch.patch"
  git -C "$TREE" apply "$WORK/patches/$patch.patch"
done
cd "$TREE"
export PYTHONPATH=src:scripts
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1
export ZC_PCM3C=1 ZC_PCM3C_MB=2000 MPLBACKEND=Agg
export ZC_R3_COOH_FLAG=1 ZC_R6_ENDPOINT=1
unset ZC_BERNY_STATE ZC_BERNY_REPLAY ZC_BERNY_NOISE_EH ZC_MAXSTEPS ZC_TRIC_PREOPT
unset ZC_SIGMA_OVERRIDE_DIR ZC_ONLY_KEYS
# Use the existing working Mac environment; do not silently change it mid-pair.
python -m pip freeze > "$WORK/mac-environment.txt"
python scripts/r7_selftest.py --out "$WORK/portable-tests.json"
python -m compileall -q scripts/r7_*.py
git diff --check
# The untracked UD asset directory alone is linked. Do not alias all data/ or results/.
test -d "$REPO/data/raw/nist/UD"
test ! -e data/raw/nist/UD
ln -s "$REPO/data/raw/nist/UD" data/raw/nist/UD
cat docs/astra/round7/PROPOSED_REGISTRATION.md >> PREREGISTRATION.md
printf '\nR7 registration committed at %s. Native plans and outcomes follow this entry.\n' \
  "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> PREREGISTRATION.md
git add scripts/r7_*.py .github/workflows/r7_review.yml docs/astra/round7 PREREGISTRATION.md
git commit -m 'Register bounded R7 response trial, referee and primary-profile screen'
export REG="$(git rev-parse HEAD)"
printf '%s\n' "$REG" > "$WORK/registration.txt"
```

Prepare complete open overlays without letting an absent open profile fall back to UD. This reads the accepted P20 collection and preserves the six flagged statuses.

```bash
python - "$PROFILE_ROOT" "$WORK" <<'PYCODE'
from pathlib import Path
import json,sys
import pandas as pd
from r4_common import selected_profiles
from r3_common import digest
root,work=Path(sys.argv[1]),Path(sys.argv[2])
records=selected_profiles(root,pd.read_csv('data/benchmark/compounds.csv'))
manifest=[]
for arm in ('open630','open636'):
    out=work/arm;out.mkdir()
    for key,folder,p in records:
        if arm=='open630' and folder!='profiles_v2':continue
        (out/(key+'.sigma')).symlink_to(p.resolve())
        manifest.append(dict(arm=arm,key=key,status=folder,path=str(p.resolve()),sha256=digest(p)))
assert len(list((work/'open630').glob('*.sigma')))==630
assert len(list((work/'open636').glob('*.sigma')))==636
(work/'open-inputs.json').write_text(json.dumps(manifest,indent=2)+'\n')
PYCODE
gh run download 37426006692 -R Victor-Liang-ChE/zcosmo -D "$WORK/p26-artifacts"
python scripts/r7_plan.py calibration --historical "$H25" \
  --registration "$REG" --out cloud/r7/calibration
python scripts/r7_plan.py pilot --artifacts "$WORK/p26-artifacts" \
  --registration "$REG" --out cloud/r7/pilot
python scripts/r7_plan.py chains --checkpoints "$STOPPED_CHECKPOINTS" \
  --registration "$REG" --out cloud/r7/chains
python scripts/r7_referee.py plan --pilot-plan cloud/r7/pilot/plan.json \
  --registration "$REG" --out cloud/r7/referee
python scripts/r7_screen.py plan --profile-root "$PROFILE_ROOT" \
  --registration "$REG" --out cloud/r7/screen
git add cloud/r7
git commit -m 'Freeze R7 input geometries, identities and native budgets before outcomes'
git push -u origin "$BRANCH"
export EXPERIMENT="$(git rev-parse HEAD)"
```

The planner does not reinterpret a missing artifact as a completed or censored member. If the historical run archive has expired, use a preserved, hash-matching copy. Do not generate a replacement start for the missing record. The stopped checkpoint plan is sealed before the pilot decision, but sealing a plan does not authorize executing it.

For each workflow dispatch below, identify the exact run by its experiment commit and the supplied `r7/<plan-path>` run name. This avoids downloading an unrelated “latest” run. Repeated identical dispatches are not allowed by the protocol; multiple matching run IDs require manual resolution, not selecting the favorable one.

```bash
export GH_REPO=Victor-Liang-ChE/zcosmo
get_run_id () {
  local plan="$1" expected_sha="$2"
  gh run list -R "$GH_REPO" --workflow r7_review.yml --branch "$BRANCH" \
    --limit 100 --json databaseId,headSha,displayTitle \
    > "$WORK/workflow-runs.json"
  python - "$WORK/workflow-runs.json" "$plan" "$expected_sha" <<'PYCODE'
import json,sys
rows=json.load(open(sys.argv[1]))
hits=[r['databaseId'] for r in rows
      if r['headSha']==sys.argv[3] and r['displayTitle']=='r7/'+sys.argv[2]]
if len(hits)!=1:raise SystemExit(f'Expected exactly one matching dispatch; got {hits}. No run was selected.')
print(hits[0])
PYCODE
}
# Calibration only. Watching a failed run does not prevent artifact recovery.
gh workflow run r7_review.yml -R "$GH_REPO" --ref "$BRANCH" \
  -f plan=cloud/r7/calibration/plan.json
CAL_RUN="$(get_run_id cloud/r7/calibration/plan.json "$EXPERIMENT")"
gh run watch "$CAL_RUN" -R "$GH_REPO" --exit-status || true
gh run download "$CAL_RUN" -R "$GH_REPO" -D "$WORK/calibration-results"
python scripts/r7_gate.py calibration --plan cloud/r7/calibration/plan.json \
  --results "$WORK/calibration-results" --out "$WORK/calibration-gate"
```

A newly dispatched run may not appear in `gh run list` immediately. In that case the run-ID command stops; rerun the lookup after the existing dispatch is visible, not the dispatch itself. The numerical gate’s JSON, not a workflow’s color, decides compatibility. The next commands require that pass and then perform the three-pair pilot.

```bash
python - "$WORK/calibration-gate/gate.json" <<'PYCODE'
import json,sys
d=json.load(open(sys.argv[1]))
assert d['passed'], 'Compatibility failed; pilot and chains are not authorized.'
print('Compatibility passed. Routine-throughput indicator:',d.get('routine_throughput_indicator'))
PYCODE
gh workflow run r7_review.yml -R "$GH_REPO" --ref "$BRANCH" \
  -f plan=cloud/r7/pilot/plan.json
PILOT_RUN="$(get_run_id cloud/r7/pilot/plan.json "$EXPERIMENT")"
gh run watch "$PILOT_RUN" -R "$GH_REPO" --exit-status || true
gh run download "$PILOT_RUN" -R "$GH_REPO" -D "$WORK/pilot-results"
mkdir -p docs/astra/round7/decisions
python scripts/r7_gate.py decide \
  --calibration "$WORK/calibration-gate/gate.json" \
  --pilot-plan cloud/r7/pilot/plan.json --pilot-results "$WORK/pilot-results" \
  --chains-plan cloud/r7/chains/plan.json \
  --out docs/astra/round7/decisions/chain-eligibility.json
```

A negative decision is saved and exits nonzero. Record it and stop the chain path. A positive decision only makes the reattempt eligible. The following block is the separate authorization and chain execution path, not part of the initial dispatch. It requires an explicit `AUTHORIZE_CHAINS=1` set by the maintainer after reviewing the saved decision.

```bash
: "${AUTHORIZE_CHAINS:?Review the positive decision and explicitly authorize the bounded six-chain trial}"
test "$AUTHORIZE_CHAINS" = 1
python - <<'PYCODE'
import json
from r7_common import sha
p='docs/astra/round7/decisions/chain-eligibility.json'
d=json.load(open(p))
assert d['eligible'], 'Negative decision: chains stay closed.'
with open('PREREGISTRATION.md','a') as f:
    f.write('\nR7 bounded chain reattempt authorized on the recorded positive decision. '
            'Decision SHA256 '+sha(p)+'. Chain-plan SHA256 '+sha('cloud/r7/chains/plan.json')+'. '
            'Exactly six keys and two arms, no retries or extensions.\n')
PYCODE
git add PREREGISTRATION.md docs/astra/round7/decisions/chain-eligibility.json
git commit -m 'Authorize R7 fixed six-chain trial after compatibility and paired pilot'
export AUTH="$(git rev-parse HEAD)"
git push
gh workflow run r7_review.yml -R "$GH_REPO" --ref "$BRANCH" \
  -f plan=cloud/r7/chains/plan.json \
  -f permit=docs/astra/round7/decisions/chain-eligibility.json \
  -f authorization="$AUTH"
CHAIN_RUN="$(get_run_id cloud/r7/chains/plan.json "$AUTH")"
gh run watch "$CHAIN_RUN" -R "$GH_REPO" --exit-status || true
gh run download "$CHAIN_RUN" -R "$GH_REPO" -D "$WORK/chain-results"
python scripts/r7_gate.py replacements --plan cloud/r7/chains/plan.json \
  --results "$WORK/chain-results" \
  --permit docs/astra/round7/decisions/chain-eligibility.json \
  --authorization "$AUTH" --background "$WORK/open636" \
  --out "$WORK/replacement-eligibility"
```

Inspect and archive the generated replacement-eligibility manifest before any separate adoption change. The command intentionally supplies no “copy into profiles_v2” action. Until protocol-aware adoption is committed, the original 630+6 selection stays in force. The fixed scientific check is executable; production promotion is not being claimed as completed by a file copy.

The referee can be run independently from the sealed input plan. Use the commit actually dispatched, especially if the branch now contains the chain authorization commit.

```bash
CURRENT_EXPERIMENT="$(git rev-parse HEAD)"
gh workflow run r7_review.yml -R "$GH_REPO" --ref "$BRANCH" \
  -f plan=cloud/r7/referee/plan.json
REFEREE_RUN="$(get_run_id cloud/r7/referee/plan.json "$CURRENT_EXPERIMENT")"
gh run watch "$REFEREE_RUN" -R "$GH_REPO" --exit-status || true
gh run download "$REFEREE_RUN" -R "$GH_REPO" -D "$WORK/referee-results"
python scripts/r7_referee.py check --plan cloud/r7/referee/plan.json \
  --results "$WORK/referee-results" --out "$WORK/referee-gate.json"
```

The primary-profile screen likewise executes its fixed list, regardless of which molecules were most interesting in the pilot. It does not optimize them. The Mac affinity loop below retains a failed or missing native case as an unresolved screen rather than dropping the key.

```bash
CURRENT_EXPERIMENT="$(git rev-parse HEAD)"
gh workflow run r7_review.yml -R "$GH_REPO" --ref "$BRANCH" \
  -f plan=cloud/r7/screen/plan.json
SCREEN_RUN="$(get_run_id cloud/r7/screen/plan.json "$CURRENT_EXPERIMENT")"
gh run watch "$SCREEN_RUN" -R "$GH_REPO" --exit-status || true
gh run download "$SCREEN_RUN" -R "$GH_REPO" -D "$WORK/screen-results"
python - "$WORK" <<'PYCODE'
from pathlib import Path
import json,subprocess,sys
work=Path(sys.argv[1]);plan=json.load(open('cloud/r7/screen/plan.json'))
# Use every selected key; missing native records remain in the final report.
from r7_common import sha
ph=sha('cloud/r7/screen/plan.json')
records=[]
for item in plan['cases']:
    key=item['key'];hits=[]
    for p in (work/'screen-results').rglob('result.json'):
        try:d=json.loads(p.read_text())
        except (OSError,ValueError):continue
        if d.get('key')==key and d.get('plan_sha256')==ph:hits.append((p,d))
    if len(hits)!=1 or hits[0][1].get('status')!='diagnostic_complete':
        records.append(dict(key=key,status='native_missing_or_failed'));continue
    p,d=hits[0]
    # The native screen writes center/minus/plus in its case directory.
    folder=p.parent
    cmd=[sys.executable,'scripts/r7_gate.py','affinities','--key',key,
         '--reference',str(folder/'center.sigma'),
         '--candidate',str(folder/'minus.sigma'),str(folder/'plus.sigma'),
         '--background',str(work/'open630'),
         '--registration',plan['registration'],'--limit','0.01',
         '--out',str(work/'screen-affinities'/key)]
    run=subprocess.run(cmd,check=False)
    records.append(dict(key=key,returncode=run.returncode))
(work/'screen-affinity-execution.json').write_text(json.dumps(records,indent=2)+'\n')
PYCODE
python scripts/r7_screen.py report --plan cloud/r7/screen/plan.json \
  --results "$WORK/screen-results" --affinities "$WORK/screen-affinities" \
  --out "$WORK/primary-screen.json"
```

The supplied native helpers also have `run_case` entry points for a local four-core venue. Use the same frozen plan, declared venue and wall cap, rather than changing settings after a hosted failure. Moving or retrying a failed case is a new execution decision that needs to be recorded; it is not an automatic recovery path.

The all-conditional R7 ceiling is `25 + 6 + 66 + 10 + 40 = 147` four-core worker-hours, or 588 core-hours. Most of that is optional chain work or the independent primary-profile screen. The reports must show actual counts and consumed time, including failures. xTB preparation and Mac-only evaluator time are additional, separately recorded work. No future task, cloud dispatch or production adoption has been performed by this report.

## Patch dependencies and application checks

H7 is the shared runtime and portable-test prerequisite. P32 adds the sealed-plan preparation and paired optimizer trial. P33 and P34 depend on H7 and reuse already registered repository helpers; P33’s input plan also reuses P32’s three archived pilot identities. P35 is a stand-alone documentation change. REG7 adds proposed text only; the setup command explicitly appends adopted text to `PREREGISTRATION.md` before native work.

All files are new, so the diffs are independent at the file-application level and can also be applied together. Runtime independence is different: applying P33 alone does not install H7. The local validation section generated below states the actual patch, syntax and portable-test outcomes. Temporary-tree patch checks are not a claim that the entire repository or Mac dataset was available here.

## Sources and provenance

[S1] `docs/astra/ROUND7_PROMPT.md`, pinned baseline above.
[S2] `docs/astra/round6/RESULTS.md` and its machine-readable data directory.
[S3] `PREREGISTRATION.md`, round-6 registration and result, and the preceding chain-stop record.
[S4] `docs/astra/round6/ZCOSMO_ROUND6_REPORT.md`, with `scripts/r6_*.py` and `.github/workflows/r6_referee.yml`.
[S5] `docs/astra/round6/data/p30/r6r_BKIMMITUMNQMOS.status.json`.
[S6] `docs/astra/round6/data/p30/r6r_ZIBGPFATKBEMQZ.status.json`.
[S7] `docs/astra/round6/data/p30/r6r_XTHFKEDIFFGKHM.status.json`.
[S8] `docs/astra/round6/data/p30/r6r_ethylene_glycol.status.json`.
[S9] `docs/astra/round6/data/p30/r6r_methanol.status.json`.
[S10] `data/pyscf_sigma/validation_set.csv`; historical occurrence semantics in the archived profile gates.
[S11] `docs/astra/round6/data/p29_inventory.json`, P29 result, and the archived P25/P26 records. Raw sampled envelopes do not describe unsampled basins.
[U1] PySCF tag `v2.14.0`, `pyscf/grad/rks.py`, default `grid_response=False` and full-response integration.
[U2] Same tag, `pyscf/df/grad/rks.py`, full-response branch and `auxbasis_response=True`.
[U3] Same tag, `pyscf/solvent/grad/pcm.py`, `make_grad_object` and `WithSolventGrad`.
[U4] Same tag, `pyscf/geomopt/berny_solver.py`, configured-gradient acceptance, callback ordering and returned convergence flag.

The repository references identify the exact code and measured evidence. All R7 thresholds and proposed decisions in this report are prospective constructions. Neither source citations nor a successful portable test constitute a new molecular result.


## Local execution record

| Check | Recorded outcome | Scope |
|---|---|---|
| Python compilation | Passed | 7 records |
| Portable self-test process and output | Passed | Local runtime only |
| Independent new-file patch application and hashes | Passed | 6 records |
| Combined new-file patch application and hashes | Passed | Local runtime only |
| Documented subcommand/flag help checks | Passed | 15 records |
| Report shell-block syntax | Passed | 7 records |
| Workflow shell and embedded Python syntax | Passed | 3 records |

The application checks used temporary Git trees and verified resulting file bytes. They do not establish that a full checkout of current main, native PySCF calculations, the Mac-only UD inputs or any hosted acceptance experiment was available. All changed implementation files are new; the pinned-worktree commands provide the real repository application check before use.

Portable test output:

```json
{
  "passed": true,
  "tests": {
    "FD_reference_error": 6.960435700031908e-12,
    "FD_indicator": 2.7829590378259204e-10,
    "tri_state_gate": "pass",
    "chain_escalation_negative_controls": "pass",
    "rigid_projection_residual": 7.771561172376096e-16,
    "configured_gradient_interface_mock": "pass, mock only",
    "historical_occurrences_and_finite_masks": "pass",
    "worker_status_lock_and_deadline": "pass",
    "berny_constants": {
      "gradientmax": 0.00045,
      "gradientrms": 0.00015,
      "stepmax": 0.0018,
      "steprms": 0.0012
    },
    "native_PySCF_test": false
  },
  "wall_s": 0.8811995129999559
}
```

A pinned PySCF 2.14.0 / pyberny 0.7.0 installation was attempted and did not complete successfully. The runtime package resolver did not provide the pinned distributions. This does not establish that they are unavailable in the working Python 3.11 environment. No native R7 acceptance result is claimed.

No R7 workflow was dispatched, no Mac-only profile comparison was performed and no production profile was promoted in this review. Earlier exploratory API-smoke records, when present locally, are not counted as molecular acceptance. The accepted R6 measurements in the analysis are repository results, not new measurements made here.

No additional successful runtime main recheck is claimed. The patch reference remains the connector-read round-7 snapshot stated at the beginning.

Patch byte identities:

| Patch | SHA256 |
|---|---|
| H7 | `cda595fa9cd616b4d31b7f8b6279737fe736c5cb249ab3c5857564c4a2bbd752` |
| P32 | `78fc30a561455cb432c5ade34b772ed1e3ea1a23a2efcb12f79aa16865ddf580` |
| P33 | `41a0ee5754512ceb082b59da3ab77a274982aadb5c13d59a1f70d0a718469611` |
| P34 | `ccb8c5aedd25b5c508f272859325b444a0f23175909bf33813cb2834725ee3e2` |
| P35 | `75ba6fb9a3596ef50c0803b293aa4e51da8181b03103853149ab7ee078d93330` |
| REG7 | `9281884ee69d51619e1a1b5cd082aa19aae3333960e3032bbb7a74ca75b36b36` |

## Unified diffs

<!-- PATCH:H7 -->
```diff
diff --git a/scripts/r7_common.py b/scripts/r7_common.py
new file mode 100644
--- /dev/null
+++ b/scripts/r7_common.py
@@ -0,0 +1,270 @@
+"""Round-7 read-only experiments. A successful diagnostic is not adoption."""
+from __future__ import annotations
+import hashlib
+import json
+import os
+import re
+import signal
+import subprocess
+import sys
+import time
+from pathlib import Path
+import numpy as np
+
+BASE = 'ddf22b19f9e1750308bd11572786b44d407a80f9'
+BERNY = dict(gradientmax=4.5e-4, gradientrms=1.5e-4,
+             stepmax=1.8e-3, steprms=1.2e-3)
+STALL = ('BTFJIXJJCSYFAL-UHFFFAOYSA-N','FLIACVVOZYBSBS-UHFFFAOYSA-N',
+         'HPEUJPJOZXNMSJ-UHFFFAOYSA-N','MVLVMROFTAUDAG-UHFFFAOYSA-N',
+         'OYHQOLUKZRVURQ-HZJYTTRNSA-N','PYGXAGIECVVIOZ-UHFFFAOYSA-N')
+PILOT = {
+ 'BKIMMITUMNQMOS-UHFFFAOYSA-N': ('s20261006-c1.json','7b9f8443a8f40cfb329a35b828777a03cedd91226863a15446995f5603b1659d'),
+ 'ZIBGPFATKBEMQZ-UHFFFAOYSA-N': ('s20261006-c1.json','538bb17a59324e1f1597934a044cdaa6843ea174f655e33669539fb538b39d5d'),
+ 'XTHFKEDIFFGKHM-UHFFFAOYSA-N': ('s20261005-c1.json','eb305508f6c6dcf68f610d0927af1977339dedc9da04238443c9acc20008df34')}
+PROBES = ('XLYOFNOQVPJJNP-UHFFFAOYSA-N','OKKJLVBELUTLKV-UHFFFAOYSA-N',
+          'BKIMMITUMNQMOS-UHFFFAOYSA-N','XTHFKEDIFFGKHM-UHFFFAOYSA-N')
+SENTINELS = PROBES[:3] + ('LYCAIKOWRPUZTN-UHFFFAOYSA-N',
+ 'MTHSVFCYNBDYFN-UHFFFAOYSA-N','ZIBGPFATKBEMQZ-UHFFFAOYSA-N',
+ 'PEDCQBHIVMGVHV-UHFFFAOYSA-N','DNIAPMSPPWPWGF-UHFFFAOYSA-N')
+
+def sha(path):
+    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
+
+def write(path, value):
+    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
+    tmp=path.with_name(path.name+'.tmp')
+    tmp.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
+    os.replace(tmp,path)
+
+def fresh(path):
+    p=Path(path).resolve(); p.mkdir(parents=True,exist_ok=False); return p
+
+def registration(value):
+    if not re.fullmatch(r'[0-9a-f]{40}',value):
+        raise ValueError('Use the actual full registration commit SHA, not a placeholder')
+    return value
+
+def geometry(path):
+    d=json.loads(Path(path).read_text()); sym=list(d['sym']); x=np.asarray(d['x'],float)
+    if x.shape!=(len(sym),3) or not len(sym) or not np.isfinite(x).all():
+        raise ValueError('Invalid saved geometry')
+    return sym,x
+
+def versions(native=False):
+    from importlib.metadata import version,PackageNotFoundError
+    result={}
+    for k in ('pyscf','pyberny','rdkit','numpy','scipy','pandas','tblite','ase'):
+        try: result[k]=version(k)
+        except PackageNotFoundError: result[k]=None
+    if native and (result['pyscf']!='2.14.0' or result['pyberny']!='0.7.0'):
+        raise RuntimeError('Requires pyscf 2.14.0 and pyberny 0.7.0')
+    return result
+
+def clean_environment():
+    for k in ('ZC_BERNY_NOISE_EH','ZC_MAXSTEPS','ZC_TRIC_PREOPT','ZC_BERNY_STATE',
+              'ZC_BERNY_REPLAY','ZC_SIGMA_OVERRIDE_DIR','ZC_ONLY_KEYS'):
+        os.environ.pop(k,None)
+    os.environ.update(ZC_PCM3C='1',ZC_R3_COOH_FLAG='1',ZC_R6_ENDPOINT='1')
+
+def factory(sym,x,spin=0,precision='production'):
+    """Use the inspected, unchanged R3 factory. Only precision diagnostics override SCF."""
+    from r3_precision import factory as original
+    mf=original(sym,np.asarray(x,float),spin,precision!='production',4000)
+    if precision=='strict':
+        mf.conv_tol=1e-12; mf.conv_tol_grad=1e-8
+    elif precision not in ('production','tight'):
+        raise ValueError(precision)
+    return mf
+
+def gradient(mf,response):
+    g=mf.nuc_grad_method(); g.grid_response=bool(response)
+    if not bool(getattr(g,'auxbasis_response',False)):
+        raise RuntimeError('Density-fitting auxiliary-basis response is missing')
+    if getattr(g.base,'with_solvent',None) is None:
+        raise RuntimeError('PCM response was detached')
+    return g
+
+def profile(sym,x,key,dest,spin,meta):
+    from zcosmo.pyscf_cosmo import cosmo_segments,to_profiles,write_sigma
+    seg,e=cosmo_segments(sym,x,spin=spin)
+    out,m=to_profiles(sym,x,seg); m.update(meta)
+    m.update(E_scf_Eh=float(e),standard_INCHIKEY=key)
+    write_sigma(dest,out,m,key)
+    return dict(path=str(Path(dest).resolve()),sha256=sha(dest),energy_Eh=float(e))
+
+def assert_connectivity(smiles,sym,x):
+    from rdkit import Chem
+    from r4_common import contacts
+    mol=Chem.AddHs(Chem.MolFromSmiles(smiles))
+    if sym!=[a.GetSymbol() for a in mol.GetAtoms()]:
+        raise ValueError('Saved geometry and declared atom order disagree')
+    expected=[sorted(n.GetIdx() for n in a.GetNeighbors()) for a in mol.GetAtoms()]
+    found=[sorted(a['bonds']) for a in contacts(sym,x)['atoms']]
+    if expected!=found: raise ValueError('Covalent connectivity changed')
+
+def load_plan(path):
+    p=Path(path).resolve(); m=json.loads(p.read_text())
+    if m['base']!=BASE: raise ValueError('Unexpected source baseline')
+    registration(m['registration'])
+    for source,digest in m.get('sources',{}).items():
+        if sha(source)!=digest:raise ValueError('Frozen experiment source changed: '+source)
+    if len({r['key'] for r in m['cases']})!=len(m['cases']):
+        raise ValueError('Duplicate plan case')
+    for r in m['cases']:
+        q=p.parent/r['geometry']
+        if sha(q)!=r['geometry_sha256']: raise ValueError('Frozen geometry changed')
+    return p,m
+
+def find_result(root,key,arm,plan_hash):
+    hits=[]
+    for p in Path(root).rglob('result.json'):
+        d=json.loads(p.read_text())
+        if d.get('key')==key and d.get('arm')==arm and d.get('plan_sha256')==plan_hash:
+            hits.append((p,d))
+    if len(hits)!=1: raise ValueError(f'Expected exactly one result for {key}/{arm}, found {len(hits)}')
+    return hits[0]
+
+def bounded(argv,out,seconds):
+    """One POSIX process group and one persistent claim per output. Never retry."""
+    out=Path(out).resolve(); out.parent.mkdir(parents=True,exist_ok=True)
+    lock=out.with_name(out.name+'.claim')
+    fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
+    with os.fdopen(fd,'w') as f: f.write(json.dumps(dict(pid=os.getpid(),argv=argv)))
+    if out.exists(): raise FileExistsError(out)
+    logpath=out.with_name(out.name+'.log'); start=time.monotonic(); timed=False
+    with logpath.open('wb') as log:
+        p=subprocess.Popen(argv,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
+        try: rc=p.wait(timeout=seconds)
+        except subprocess.TimeoutExpired:
+            timed=True
+            try: os.killpg(p.pid,signal.SIGTERM)
+            except ProcessLookupError: pass
+            try: rc=p.wait(timeout=5)
+            except subprocess.TimeoutExpired:
+                try: os.killpg(p.pid,signal.SIGKILL)
+                except ProcessLookupError: pass
+                rc=p.wait()
+    native={}
+    if (out/'result.json').is_file(): native=json.loads((out/'result.json').read_text())
+    status='deadline' if timed else ('completed' if rc==0 else 'child_failed')
+    # Scientific negative decisions can complete normally; do not call them censoring.
+    if not timed and native.get('status') in ('censored_evaluations','diagnostic_complete'):
+        status='completed'
+    record=dict(argv=argv,wall_s=time.monotonic()-start,deadline_s=seconds,
+                returncode=rc,execution_status=status,native_status=native.get('status'),
+                output=str(out),log_sha256=sha(logpath))
+    write(out.with_name(out.name+'.run.json'),record)
+    return record
+
+def internal_projection(x,v):
+    from scipy.linalg import null_space
+    y=np.asarray(x)-np.mean(x,axis=0); rigid=[]
+    for axis in np.eye(3):
+        rigid.extend([np.broadcast_to(axis,y.shape).ravel(),
+                      np.cross(np.broadcast_to(axis,y.shape),y).ravel()])
+    Q=null_space(np.asarray(rigid),rcond=1e-10)
+    return (Q@(Q.T@np.asarray(v).ravel())).reshape(y.shape)
+
+def verdict(reference,analytic,u,tau=1e-5):
+    """Finite-resolution equivalence assessment, not a certified error interval."""
+    if not np.isfinite([reference,analytic,u]).all() or u<0:
+        return 'inconclusive'
+    if u>tau/4: return 'inconclusive'
+    error=abs(reference-analytic)
+    if error+u<=tau: return 'consistent'
+    if error-u>tau: return 'inconsistent'
+    return 'inconclusive'
+
+def chain_decision(cal,pilots):
+    keys=set(PILOT)
+    if set(pilots)!=keys: raise ValueError('All three fixed pilot cases are required')
+    only_full=[]; only_off=[]; invalid=[]
+    allowed={'berny_converged','censored_evaluations','censored_deadline'}
+    for k,r in pilots.items():
+        if set(r)!= {'off','full'} or any(v not in allowed for v in r.values()):
+            invalid.append(k); continue
+        if r['full']=='berny_converged' and r['off']!='berny_converged':only_full.append(k)
+        if r['off']=='berny_converged' and r['full']!='berny_converged':only_off.append(k)
+    ok=bool(cal.get('passed') is True and len(only_full)>=2 and not only_off and not invalid)
+    return dict(eligible_for_chain_trial=ok,full_only=only_full,off_only=only_off,
+                invalid=invalid,pilots=pilots,rule='calibration numerical compatibility pass; >=2 full-only; zero off-only; no missing/failed pilot; targeted rescue has its own wall cap')
+
+
+def source_fingerprint(family):
+    shared=['scripts/r7_common.py','scripts/r7_gate.py','scripts/r3_precision.py',
+            'scripts/r4_common.py','data/raw/nist/to_sigma.py']
+    specific={'optimizer':['scripts/r7_plan.py','scripts/r7_optimize.py'],
+              'referee':['scripts/r7_referee.py','scripts/r6_referee.py'],
+              'screen':['scripts/r7_screen.py','scripts/r6_referee.py']}[family]
+    shared += ['src/zcosmo/'+n for n in ('pyscf_cosmo.py','pyscf_cosmo_v2.py','pcm_lu.py',
+                                        'cosmosac.py','z0x.py','models.py')]
+    return {p:sha(p) for p in shared+specific}
+
+
+FD_TAU=5e-5/5
+FD_STEPS=np.array([.016,.008,.004,.002,.001])
+
+def fd_assess(tight,strict,gtight,gfull,goff,topology_stable=True):
+    tight=np.asarray(tight,float);strict=np.asarray(strict,float)
+    if tight.shape!=(5,2) or strict.shape!=(5,2):raise ValueError('Five fixed +/- energy pairs are required')
+    if not np.isfinite([tight,strict]).all():raise ValueError('Nonfinite energy table')
+    d0=(tight[:,0]-tight[:,1])/(2*FD_STEPS)
+    d1=(strict[:,0]-strict[:,1])/(2*FD_STEPS)
+    r0=(4*d0[1:]-d0[:-1])/3;r1=(4*d1[1:]-d1[:-1])/3
+    trunc=abs(r1[-1]-r1[-2])  # Full difference, deliberately not an asserted /15 bound.
+    previous=abs(r1[-2]-r1[-3])
+    precision=max(abs(r1[-1]-r0[-1]),abs(r1[-2]-r0[-2]))
+    gradient_precision=abs(gfull-gtight)
+    h=FD_STEPS[-1];hl=FD_STEPS[-2]
+    rounding=8*np.finfo(float).eps*((4/3)*abs(strict[-1]).sum()/(2*h)
+                                     +(1/3)*abs(strict[-2]).sum()/(2*hl))
+    uncertainty=float(trunc+precision+gradient_precision+rounding)
+    stabilizing=bool(trunc<=previous or trunc<=FD_TAU/16)
+    f=verdict(float(r1[-1]),float(gfull),uncertainty,FD_TAU)
+    o=verdict(float(r1[-1]),float(goff),uncertainty,FD_TAU)
+    if not topology_stable or not stabilizing:f=o='inconclusive'
+    material=True if f=='consistent' and o=='inconsistent' else (False if f==o=='consistent' else None)
+    return dict(steps_Bohr=FD_STEPS.tolist(),central_tight=d0.tolist(),central_strict=d1.tolist(),
+        Richardson_tight=r0.tolist(),Richardson_strict=r1.tolist(),reference=float(r1[-1]),
+        truncation_indicator=float(trunc),precision_indicator=float(precision),
+        gradient_precision_indicator=float(gradient_precision),roundoff_indicator=float(rounding),
+        combined_indicator=uncertainty,indicator_ceiling=FD_TAU/4,tolerance=FD_TAU,
+        stabilizing=stabilizing,grid_count_stable=bool(topology_stable),
+        full_error=float(abs(gfull-r1[-1])),off_error=float(abs(goff-r1[-1])),
+        full_verdict=f,off_verdict=o,missing_response_material=material,
+        scope='Empirical finite-resolution assessment; no rigorous interval enclosure or global stationarity certificate')
+
+
+
+
+HIST_KEY_RE=re.compile(r'^[A-Z]{14}-[A-Z]{10}-[A-Z]$')
+
+def historical_queries(path):
+    """Read an explicit query file, or find the single archived 2302-occurrence table.
+
+    Field names may differ across archived harnesses. A target field is accepted
+    only if every entry is a full molecular key occurring in that row's pair.
+    No query is dropped, deduplicated, or reconstructed from an arbitrary 25.
+    """
+    import pandas as pd
+    path=Path(path); sources=[path] if path.is_file() else sorted(path.rglob('*.csv'))
+    candidates=[]
+    for p in sources:
+        try:d=pd.read_csv(p)
+        except (ValueError,UnicodeError):continue
+        if len(d)!=2302 or not {'solute','solvent','T'}<=set(d):continue
+        for c in d.columns:
+            if c in ('solute','solvent','T'):continue
+            v=d[c].astype(str)
+            if v.nunique()!=25 or not v.map(lambda x:bool(HIST_KEY_RE.fullmatch(x))).all():continue
+            if not ((v==d.solute)|(v==d.solvent)).all():continue
+            q=pd.DataFrame(dict(target=v,solute=d.solute,solvent=d.solvent,T=d['T'],
+                                occurrence=np.arange(len(d))))
+            if not np.isfinite(q['T']).all() or (q['T']<=0).any():raise ValueError('Invalid historical temperatures')
+            candidates.append((p,c,q))
+    if not candidates:
+        raise ValueError('No archived 25-target/2302-occurrence query table. Supply its exact CSV with --historical; do not use validation_set.csv alone.')
+    unique={q.to_csv(index=False): (p,c,q) for p,c,q in candidates}
+    if len(unique)!=1:raise ValueError('Conflicting historical query tables; supply the explicit registered CSV')
+    return next(iter(unique.values()))
+
diff --git a/scripts/r7_gate.py b/scripts/r7_gate.py
new file mode 100644
--- /dev/null
+++ b/scripts/r7_gate.py
@@ -0,0 +1,255 @@
+"""Mac-side R7 gates. Fresh processes per target/profile set; historical occurrences retained."""
+from __future__ import annotations
+import argparse
+import json
+import os
+import subprocess
+import sys
+import tempfile
+import time
+from pathlib import Path
+import numpy as np
+import pandas as pd
+from r7_common import (BASE,PILOT,PROBES,sha,write,fresh,load_plan,find_result,
+                       clean_environment,chain_decision,registration)
+
+MODELS=('cosmosac_dsp','Z0x')
+
+
+def worker(a):
+    spec=json.loads(Path(a.spec).read_text());clean_environment()
+    q=pd.read_csv(spec['queries']);q=q[q.target==spec['target']].copy()
+    if q.empty or q.occurrence.duplicated().any():raise ValueError('Invalid target query identities')
+    smi=pd.read_csv('data/benchmark/compounds.csv').set_index('inchikey').smiles.to_dict()
+    target=spec.get('profile');background=spec.get('background');used={}
+    with tempfile.TemporaryDirectory(prefix='r7-query-') as temp:
+        d=Path(temp)
+        if background:
+            for k in set(q[['solute','solvent']].to_numpy().ravel()):
+                src=Path(background)/(k+'.sigma')
+                if not src.is_file():raise FileNotFoundError(f'No authorized open profile for {k}')
+                (d/src.name).symlink_to(src.resolve())
+        if target:
+            dst=d/(spec['target']+'.sigma')
+            if dst.is_symlink():dst.unlink()
+            dst.symlink_to(Path(target).resolve())
+        if target or background:os.environ['ZC_SIGMA_OVERRIDE_DIR']=temp
+        from zcosmo.cosmosac import sigma_path,SIGMA_DIR
+        if not background and not SIGMA_DIR.is_dir():raise FileNotFoundError('UD-backed gate must run on the Mac with UD assets')
+        from zcosmo.models import make_model
+        records=[];cache={}
+        for r in q.itertuples():
+            keys=(r.solute,r.solvent)
+            for k in keys:
+                p=sigma_path(k)
+                if p is None:raise FileNotFoundError(k)
+                if background and p.resolve()!=(d/(k+'.sigma')).resolve():raise ValueError('Unauthorized UD fallback')
+                used[str(p.resolve())]=sha(p)
+            for name in MODELS:
+                try:
+                    ck=(name,keys)
+                    if ck not in cache:cache[ck]=make_model(name,list(keys),[smi[k] for k in keys])
+                    y=float(cache[ck].lngamma_inf(float(r.T),0))
+                    if not np.isfinite(y):raise ValueError('nonfinite model output')
+                    error=''
+                except Exception as e:y=None;error=type(e).__name__+': '+str(e)[:300]
+                records.append(dict(occurrence=int(r.occurrence),target=r.target,solute=r.solute,
+                    solvent=r.solvent,T=float(r.T),model=name,value=y,error=error))
+        if any(sha(p)!=h for p,h in used.items()):raise ValueError('Profile changed during evaluation')
+        write(a.out,dict(records=records,inputs=used,spec_sha256=sha(a.spec)))
+
+
+def evaluate(qpath,target,p,out,background=None):
+    spec=dict(queries=str(Path(qpath).resolve()),target=target,
+              profile=str(Path(p).resolve()) if p else None,
+              background=str(Path(background).resolve()) if background else None)
+    sp=Path(out).with_suffix('.spec.json');write(sp,spec)
+    subprocess.run([sys.executable,str(Path(__file__).resolve()),'worker','--spec',str(sp),
+                    '--out',str(out)],check=True)
+    return pd.DataFrame(json.loads(Path(out).read_text())['records'])
+
+
+def aligned_values(frame,q,model):
+    f=frame[frame.model==model].set_index('occurrence')
+    if not f.index.is_unique or set(f.index)!=set(q.occurrence):raise ValueError('Missing, extra, or duplicate result occurrence')
+    f=f.loc[q.occurrence]
+    for c in ('target','solute','solvent'):
+        if not np.array_equal(f[c].to_numpy(str),q[c].to_numpy(str)):raise ValueError('Query identity changed')
+    if not np.array_equal(f['T'].to_numpy(float),q['T'].to_numpy(float)):raise ValueError('Query temperature changed')
+    return pd.to_numeric(f.value,errors='raise').to_numpy(float)
+
+
+def compare_arrays(reference,candidate):
+    fr=np.isfinite(reference);fc=np.isfinite(candidate)
+    same=np.array_equal(fr,fc)
+    good=fr&fc
+    return dict(coverage_identical=bool(same),requested=len(fr),finite_reference=int(fr.sum()),
+        finite_candidate=int(fc.sum()),max_abs_change=float(np.max(abs(reference[good]-candidate[good]))) if good.any() else None,
+        median_abs_change=float(np.median(abs(reference[good]-candidate[good]))) if good.any() else None)
+
+
+def calibration(a):
+    plan,m=load_plan(a.plan)
+    if m['family']!='calibration' or len(m['cases'])!=25:raise ValueError('Expected complete historical 25 plan')
+    qpath=plan.parent/m['queries']
+    if sha(qpath)!=m['queries_sha256']:raise ValueError('Historical occurrences changed')
+    q=pd.read_csv(qpath)
+    if len(q)!=2302 or q.target.nunique()!=25:raise ValueError('Wrong historical universe')
+    out=fresh(a.out);frames={x:[] for x in ('off','full','UD')};runs=[];bins=[];t=time.monotonic()
+    for case in m['cases']:
+        key=case['key'];pfiles={};native={};runtime={}
+        for arm in ('off','full'):
+            p,r=find_result(a.results,key,arm,sha(plan));native[arm]=r
+            if r['status']!='berny_converged' or r.get('berny_converged') is not True:
+                raise ValueError(f'{key}/{arm} did not pass the original Berny predicate')
+            if r.get('grid_response')!=(arm=='full') or not 1<=r['evaluations']<=100:
+                raise ValueError('Wrong gradient setting or evaluation budget')
+            profile=p.parent/(key+'.sigma')
+            if sha(profile)!=r['profile']['sha256']:raise ValueError('Trial profile changed')
+            pfiles[arm]=profile
+            rr=p.parent.with_name(p.parent.name+'.run.json')
+            z=json.loads(rr.read_text())
+            if z['execution_status']!='completed' or z['returncode']!=0:raise ValueError('Worker did not complete successfully')
+            runtime[arm]=float(z['wall_s'])
+            frames[arm].append(evaluate(qpath,key,profile,out/(key+'-'+arm+'.json')))
+        if native['off']['input_geometry_sha256']!=native['full']['input_geometry_sha256'] or native['off']['packages']!=native['full']['packages']:
+            raise ValueError('Paired inputs/environments differ')
+        frames['UD'].append(evaluate(qpath,key,None,out/(key+'-UD.json')))
+        from r3_common import read_sigma
+        ps=[read_sigma(pfiles[k])[1] for k in ('off','full')]
+        bins.append(dict(key=key,max_raw_bin=float(abs(ps[0]-ps[1]).max()),
+            max_normalized_bin=float(abs(ps[0]/ps[0].sum()-ps[1]/ps[1].sum()).max()),
+            normalized_L1=float(abs(ps[0]/ps[0].sum()-ps[1]/ps[1].sum()).sum())))
+        runs.append(dict(key=key,wall_s=runtime,evaluations={k:native[k]['evaluations'] for k in native}))
+    frames={k:pd.concat(v,ignore_index=True) for k,v in frames.items()};checks={}
+    for model in MODELS:
+        values={k:aligned_values(v,q,model) for k,v in frames.items()}
+        checks[model]=dict(candidate_vs_control=compare_arrays(values['off'],values['full']),
+                           candidate_vs_UD=compare_arrays(values['UD'],values['full']))
+    off=sum(r['wall_s']['off'] for r in runs);full=sum(r['wall_s']['full'] for r in runs)
+    dsp=checks['cosmosac_dsp'];z0=checks['Z0x']
+    finite_ok=all(c['coverage_identical'] for x in checks.values() for c in x.values())
+    expected=(dsp['candidate_vs_control']['finite_reference']==2271 and z0['candidate_vs_control']['finite_reference']==2302)
+    passed=bool(finite_ok and expected and dsp['candidate_vs_control']['max_abs_change']<.01
+                and dsp['candidate_vs_UD']['median_abs_change']<.15)
+    report=dict(base=BASE,registration=m['registration'],passed=passed,plan_sha256=sha(plan),
+        rows=2302,targets=25,checks=checks,bins=bins,runs=runs,
+        gate_kind='P32_numerical_compatibility',
+        routine_throughput_indicator=bool(full/off<=1.50),routine_throughput_limit=1.50,
+        paired_worker_seconds=dict(off=off,full=full),wall_ratio=full/off,
+        shared_xtb_seconds=sum(r['shared_xtb_seconds'] for r in m['cases']),
+        timing_scope='Worker optimizer plus TZVP profile; one shared xTB preparation excluded from both arms',
+        gate_elapsed_s=time.monotonic()-t,adopted=False)
+    write(out/'gate.json',report)
+    if not passed:raise SystemExit(2)
+
+
+def decide(a):
+    cal=json.loads(Path(a.calibration).read_text());plan,m=load_plan(a.pilot_plan)
+    cp,cm=load_plan(a.chains_plan)
+    if m['family']!='pilot' or cm['family']!='chains':raise ValueError('Wrong plan families')
+    if cal['registration']!=m['registration'] or cm['registration']!=m['registration']:
+        raise ValueError('Registrations differ')
+    pilots={}
+    for k in PILOT:
+        pilots[k]={}
+        for arm in ('off','full'):
+            p,d=find_result(a.pilot_results,k,arm,sha(plan))
+            status=d.get('status','missing')
+            if d.get('evaluations',0)<1:status='operational_failure'
+            if status=='censored_evaluations' and d.get('evaluations')!=80:status='operational_failure'
+            if status=='berny_converged':
+                if d.get('grid_response')!=(arm=='full') or d.get('berny_converged') is not True:
+                    raise ValueError('Invalid pilot convergence record')
+                if sha(p.parent/(k+'.sigma'))!=d['profile']['sha256']:raise ValueError('Pilot profile changed')
+            pilots[k][arm]=status
+    d=chain_decision(cal,pilots)
+    d.update(base=BASE,registration=m['registration'],calibration_gate_sha256=sha(a.calibration),
+        pilot_plan_sha256=sha(plan),chains_plan_sha256=sha(cp),
+        not_a_conclusion_about='Untested chains, all 630 geometries, or the historical P30 gate')
+    write(a.out,d)
+    if not d['eligible_for_chain_trial']:raise SystemExit(2)
+
+
+def affinities(a):
+    """Compare one profile to its own reference, using fixed computational probes.
+
+    Optional IDAC queries supply identities and temperatures only. No measured
+    response is sent to workers. Background must be a complete open overlay.
+    """
+    registration(a.registration);out=fresh(a.out);rows=[]
+    if a.idac:
+        d=pd.read_csv(a.idac);d=d[(d.solute==a.key)|(d.solvent==a.key)]
+        rows.extend(dict(target=a.key,solute=r.solute,solvent=r.solvent,T=float(r.T)) for r in d.itertuples())
+    for k in PROBES:
+        if k==a.key:continue
+        for T in (250.,298.15,400.):
+            for i,j in ((a.key,k),(k,a.key)):
+                rows.append(dict(target=a.key,solute=i,solvent=j,T=T))
+    q=pd.DataFrame(rows);q['occurrence']=np.arange(len(q));qp=out/'queries.csv';q.to_csv(qp,index=False)
+    ref=evaluate(qp,a.key,a.reference,out/'reference.json',a.background);summaries=[]
+    for i,p in enumerate(a.candidate):
+        frame=evaluate(qp,a.key,p,out/f'candidate-{i}.json',a.background);check={}
+        for model in MODELS:
+            r=aligned_values(ref,q,model);c=aligned_values(frame,q,model);check[model]=compare_arrays(r,c)
+        summaries.append(dict(profile=str(Path(p).resolve()),sha256=sha(p),models=check,
+            passed=all(v['coverage_identical'] and v['max_abs_change'] is not None and v['max_abs_change']<a.limit for v in check.values())))
+    report=dict(key=a.key,registration=a.registration,reference_sha256=sha(a.reference),
+        limit=a.limit,rows=len(q),candidates=summaries,passed=all(x['passed'] for x in summaries),
+        scope='Finite fixed query set; not a bound on all compositions, temperatures, or geometries')
+    write(out/'gate.json',report)
+    if not report['passed']:raise SystemExit(2)
+
+
+
+def replacements(a):
+    from argparse import Namespace
+    from r7_common import STALL
+    plan,m=load_plan(a.plan);registration(a.authorization)
+    permit=json.loads(Path(a.permit).read_text())
+    if m['family']!='chains' or permit.get('eligible_for_chain_trial') is not True:
+        raise ValueError('No approved bounded chain trial')
+    if permit.get('chains_plan_sha256')!=sha(plan):raise ValueError('Chain inputs differ from approval')
+    evidence={(k,arm):find_result(a.results,k,arm,sha(plan)) for k in STALL for arm in ('off','full')}
+    out=fresh(a.out);records=[]
+    for k in STALL:
+        p,d=evidence[k,'full'];_,old=evidence[k,'off']
+        row=dict(key=k,off_status=old['status'],full_status=d['status'],replacement_eligible=False,
+                 full_result_sha256=sha(p),off_original_success=old['status']=='berny_converged')
+        if d['status']!='berny_converged':records.append(row);continue
+        target=p.parent/(k+'.sigma');reference=Path(a.background)/(k+'.sigma')
+        if sha(target)!=d['profile']['sha256']:raise ValueError('Chain candidate changed')
+        if d.get('authorization_commit')!=a.authorization or d.get('permit_sha256')!=sha(a.permit):
+            raise ValueError('Chain execution did not use the declared authorization')
+        meta=json.loads(reference.read_text().splitlines()[0][8:])
+        expected='S1' if k=='MVLVMROFTAUDAG-UHFFFAOYSA-N' else 'S2'
+        if meta.get('geometry_converged')!=expected:raise ValueError('Reference is not the selected flagged profile')
+        try:
+            affinities(Namespace(key=k,reference=str(reference),candidate=[str(target)],
+                background=a.background,out=str(out/k),registration=m['registration'],
+                idac='data/benchmark/idac.csv',limit=.05))
+        except SystemExit as e:
+            if e.code!=2:raise
+        g=out/k/'gate.json';check=json.loads(g.read_text())
+        row.update(replacement_eligible=bool(check['passed']),local_gate_sha256=sha(g),
+                   reference_sha256=sha(reference),candidate_sha256=sha(target))
+        records.append(row)
+    write(out/'promotions.json',dict(base=BASE,registration=m['registration'],
+        authorization=a.authorization,permit_sha256=sha(a.permit),records=records,
+        production_files_written=0,
+        note='Eligibility only. An adoption commit must update protocol-aware selection/cache provenance; do not copy a new A profile into an old cache fingerprint.'))
+
+
+def main():
+    p=argparse.ArgumentParser();s=p.add_subparsers(dest='command',required=True)
+    q=s.add_parser('worker');q.add_argument('--spec',required=True);q.add_argument('--out',required=True)
+    q=s.add_parser('calibration');q.add_argument('--plan',required=True);q.add_argument('--results',required=True);q.add_argument('--out',required=True)
+    q=s.add_parser('decide')
+    for name in ('calibration','pilot-plan','pilot-results','chains-plan','out'):q.add_argument('--'+name,required=True)
+    q=s.add_parser('affinities')
+    for name in ('key','reference','background','out','registration'):q.add_argument('--'+name,required=True)
+    q.add_argument('--candidate',action='append',required=True);q.add_argument('--limit',type=float,choices=[.01,.05],required=True);q.add_argument('--idac')
+    q=s.add_parser('replacements')
+    for name in ('plan','results','permit','authorization','background','out'):q.add_argument('--'+name,required=True)
+    a=p.parse_args();globals()[a.command](a)
+if __name__=='__main__':main()
diff --git a/scripts/r7_selftest.py b/scripts/r7_selftest.py
new file mode 100644
--- /dev/null
+++ b/scripts/r7_selftest.py
@@ -0,0 +1,95 @@
+"""Portable R7 software/math tests. This suite makes no PySCF acceptance claim."""
+from __future__ import annotations
+import argparse
+import json
+import sys
+import tempfile
+import time
+from pathlib import Path
+import numpy as np
+import pandas as pd
+from r7_common import PILOT,BERNY,verdict,chain_decision,internal_projection,bounded,gradient,write
+from r7_common import fd_assess as assess, FD_STEPS as STEPS, FD_TAU as TAU
+from r7_common import historical_queries
+from r7_gate import aligned_values,compare_arrays
+
+
+def run():
+    checks={}
+    def energy(x):return -100.+1.7e-4*x+.3*x*x+.7*x**3+.2*x**4+.05*x**5
+    table=np.array([[energy(h),energy(-h)] for h in STEPS])
+    ok=assess(table,table,1.7e-4,1.7e-4,1.7e-4)
+    assert ok['full_verdict']=='consistent'
+    bad=assess(table,table,1.7e-4+4*TAU,1.7e-4+4*TAU,1.7e-4)
+    assert bad['full_verdict']=='inconsistent'
+    noisy=table.copy();noisy[:,0]+=STEPS*1e-4;noisy[:,1]-=STEPS*1e-4
+    assert assess(noisy,table,1.7e-4,1.7e-4,1.7e-4)['full_verdict']=='inconclusive'
+    assert assess(table,table,1.7e-4,1.7e-4,1.7e-4,False)['full_verdict']=='inconclusive'
+    assert verdict(0,0,TAU/2)=='inconclusive'
+    checks['FD_reference_error']=abs(ok['reference']-1.7e-4)
+    checks['FD_indicator']=ok['combined_indicator']
+    checks['tri_state_gate']='pass'
+    keys=list(PILOT)
+    pilot={k:dict(off='censored_evaluations',full='berny_converged') for k in keys}
+    assert chain_decision({'passed':True},pilot)['eligible_for_chain_trial']
+    mixed={k:dict(v) for k,v in pilot.items()};mixed[keys[2]]=dict(off='berny_converged',full='censored_evaluations')
+    assert not chain_decision({'passed':True},mixed)['eligible_for_chain_trial']
+    mixed={k:dict(v) for k,v in pilot.items()};mixed[keys[2]]['off']='failed'
+    assert not chain_decision({'passed':True},mixed)['eligible_for_chain_trial']
+    assert not chain_decision({'passed':False},pilot)['eligible_for_chain_trial']
+    try:chain_decision({'passed':True},{keys[0]:pilot[keys[0]]})
+    except ValueError:pass
+    else:raise AssertionError('Missing pilot was accepted')
+    checks['chain_escalation_negative_controls']='pass'
+    x=np.array([[0.,0.,0.],[1.,0.,0.],[0.,1.,0.],[.2,.3,1.]])
+    v=internal_projection(x,np.random.default_rng(17).normal(size=x.shape))
+    trans=np.max(abs(v.sum(0)));torque=np.max(abs(np.cross(x-x.mean(0),v).sum(0)))
+    assert max(trans,torque)<1e-12
+    checks['rigid_projection_residual']=float(max(trans,torque))
+    class MF:
+        with_solvent=object()
+        def nuc_grad_method(self):
+            class G:auxbasis_response=True
+            g=G();g.base=self;return g
+    assert gradient(MF(),True).grid_response is True
+    checks['configured_gradient_interface_mock']='pass, mock only'
+    fakekeys=['A'*13+chr(65+i)+'-'+'B'*10+'-C' for i in range(25)]
+    q=pd.DataFrame(dict(target=[fakekeys[i%25] for i in range(2302)],
+        solute=[fakekeys[i%25] for i in range(2302)],solvent=['Z'*14+'-'+'B'*10+'-C']*2302,
+        T=[298.15]*2302,occurrence=np.arange(2302)))
+    with tempfile.TemporaryDirectory(prefix='r7-test-') as td:
+        root=Path(td);q.to_csv(root/'queries.csv',index=False)
+        _,_,found=historical_queries(root)
+        assert len(found)==2302 and found.target.nunique()==25
+        f=q.copy();f['model']='Z0x';f['value']=np.arange(2302,dtype=float);f.loc[0,'value']=np.nan
+        shuffled=f.sample(frac=1,random_state=2)
+        a=aligned_values(shuffled,q,'Z0x');b=aligned_values(f,q,'Z0x')
+        assert np.array_equal(a,b,equal_nan=True)
+        c=compare_arrays(a,b);assert c['coverage_identical'] and c['finite_reference']==2301
+        try:aligned_values(f.iloc[1:],q,'Z0x')
+        except ValueError:pass
+        else:raise AssertionError('Missing query accepted')
+        changed=b.copy();changed[0]=0
+        assert not compare_arrays(a,changed)['coverage_identical']
+        checks['historical_occurrences_and_finite_masks']='pass'
+        dest=root/'diagnostic'
+        code="from pathlib import Path;import json,sys;p=Path(sys.argv[1]);p.mkdir();(p/'result.json').write_text(json.dumps({'status':'diagnostic_complete','passed':False}));sys.exit(2)"
+        r=bounded([sys.executable,'-c',code,str(dest)],dest,5)
+        assert r['execution_status']=='completed' and r['native_status']=='diagnostic_complete'
+        try:bounded([sys.executable,'-c','pass'],dest,5)
+        except FileExistsError:pass
+        else:raise AssertionError('Duplicate output claim accepted')
+        deadline=root/'deadline'
+        r=bounded([sys.executable,'-c','import time;time.sleep(20)'],deadline,.1)
+        assert r['execution_status']=='deadline'
+        checks['worker_status_lock_and_deadline']='pass'
+    checks['berny_constants']=BERNY
+    checks['native_PySCF_test']=False
+    return checks
+
+
+def main():
+    p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args()
+    t=time.monotonic();d=run();write(a.out,dict(passed=True,tests=d,wall_s=time.monotonic()-t))
+    print(json.dumps(d,indent=2))
+if __name__=='__main__':main()
```

<!-- PATCH:P32 -->
```diff
diff --git a/scripts/r7_plan.py b/scripts/r7_plan.py
new file mode 100644
--- /dev/null
+++ b/scripts/r7_plan.py
@@ -0,0 +1,92 @@
+"""Freeze R7 inputs before trials. Never guess the historical 25 from the 26-row CSV."""
+from __future__ import annotations
+from r7_common import source_fingerprint, historical_queries
+import argparse
+import json
+import re
+import shutil
+import time
+from pathlib import Path
+import numpy as np
+import pandas as pd
+from r7_common import BASE,STALL,PILOT,sha,write,fresh,registration,geometry,versions
+
+KEY_RE=re.compile(r'^[A-Z]{14}-[A-Z]{10}-[A-Z]$')
+
+def record_geometry(out,key,source,sym=None,x=None):
+    dest=out/'geometries'/(key+'.json');dest.parent.mkdir(exist_ok=True)
+    if source is not None:
+        geometry(source);dest.write_bytes(Path(source).read_bytes())
+        provenance=dict(path=str(Path(source).resolve()),sha256=sha(source))
+    else:
+        write(dest,dict(sym=list(sym),x=np.asarray(x,float).tolist()));provenance=None
+    return str(dest.relative_to(out)),sha(dest),provenance
+
+def calibration(a):
+    reg=registration(a.registration);src,col,q=historical_queries(a.historical)
+    val=pd.read_csv('data/pyscf_sigma/validation_set.csv')
+    keys=sorted(q.target.unique());missing=set(keys)-set(val.inchikey)
+    if missing:raise ValueError('Historical target not in the validation source')
+    if val.inchikey.duplicated().any():raise ValueError('Ambiguous validation key')
+    smi=val.set_index('inchikey').smiles.to_dict();out=fresh(a.out);cases=[]
+    from zcosmo.pyscf_cosmo import xtb_geometry
+    for key in keys:
+        t=time.monotonic();sym,x=xtb_geometry(smi[key],seed=7)
+        elapsed=time.monotonic()-t;rel,digest,_=record_geometry(out,key,None,sym,x)
+        cases.append(dict(key=key,smiles=smi[key],spin=0,geometry=rel,
+                          geometry_sha256=digest,shared_xtb_seconds=elapsed))
+    q.to_csv(out/'queries.csv',index=False)
+    write(out/'plan.json',dict(sources=source_fingerprint('optimizer'),base=BASE,registration=reg,family='calibration',
+        cases=cases,queries='queries.csv',queries_sha256=sha(out/'queries.csv'),
+        historical_source=str(src.resolve()),historical_sha256=sha(src),target_column=col,
+        packages=versions(),budget=100,seconds_per_arm=1800,
+        start_protocol='One frozen seed-7 GFN2-xTB start shared by both arms; no saved DFT geometry is substituted'))
+
+def pilot(a):
+    reg=registration(a.registration);out=fresh(a.out);cases=[]
+    compounds=pd.read_csv('data/benchmark/compounds.csv').set_index('inchikey')
+    for key,(proposal,expected_geometry_sha) in PILOT.items():
+        pp=Path('cloud/r5/proposals')/key/'proposals.json';m=json.loads(pp.read_text())
+        selected=[c for c in m['cases'] if c['path']==proposal]
+        if len(selected)!=1:raise ValueError('Frozen P26 proposal missing')
+        input_hash=selected[0]['sha256'];hits=[]
+        for p in Path(a.artifacts).rglob('result.json'):
+            d=json.loads(p.read_text())
+            if d.get('input_sha256')==input_hash:hits.append((p,d))
+        if len(hits)!=1:raise ValueError(f'Require exactly one archived P26 result for {key}')
+        p,d=hits[0]
+        if d.get('status')!='censored' or d.get('evaluations')!=80:
+            raise ValueError('Not the registered censored P26 member')
+        source=p.parent/'latest.json'
+        if sha(source)!=expected_geometry_sha:raise ValueError('P30 geometry hash mismatch; no replacement checkpoint')
+        rel,h,prov=record_geometry(out,key,source)
+        cases.append(dict(key=key,smiles=str(compounds.loc[key,'smiles']),spin=0,
+            geometry=rel,geometry_sha256=h,source=prov,proposal_sha256=input_hash,
+            source_result_sha256=sha(p)))
+    write(out/'plan.json',dict(sources=source_fingerprint('optimizer'),base=BASE,registration=reg,family='pilot',cases=cases,
+        budget=80,seconds_per_arm=3600,packages=versions()))
+
+def chains(a):
+    reg=registration(a.registration);out=fresh(a.out);cases=[]
+    compounds=pd.read_csv('data/benchmark/compounds.csv').set_index('inchikey')
+    # Use the deliberately supplied final-checkpoint directory. Never choose the
+    # newest among conflicting files or read optimizer pickles from the old force field.
+    for key in STALL:
+        hits=list(Path(a.checkpoints).rglob(key+'.partial.json'))
+        if len(hits)!=1:raise ValueError(f'Exactly one designated checkpoint required for {key}')
+        rel,h,prov=record_geometry(out,key,hits[0])
+        cases.append(dict(key=key,smiles=str(compounds.loc[key,'smiles']),spin=0,
+                          geometry=rel,geometry_sha256=h,source=prov))
+    write(out/'plan.json',dict(sources=source_fingerprint('optimizer'),base=BASE,registration=reg,family='chains',cases=cases,
+        budget=100,seconds_per_arm=19800,packages=versions(),
+        execution_requires='A matching positive calibration-plus-pilot decision and a separate authorization commit'))
+
+def main():
+    p=argparse.ArgumentParser();s=p.add_subparsers(dest='command',required=True)
+    q=s.add_parser('calibration');q.add_argument('--historical',required=True)
+    q=s.add_parser('pilot');q.add_argument('--artifacts',required=True)
+    q=s.add_parser('chains');q.add_argument('--checkpoints',required=True)
+    for q in s.choices.values():
+        q.add_argument('--out',required=True);q.add_argument('--registration',required=True)
+    a=p.parse_args();globals()[a.command](a)
+if __name__=='__main__':main()
diff --git a/scripts/r7_optimize.py b/scripts/r7_optimize.py
new file mode 100644
--- /dev/null
+++ b/scripts/r7_optimize.py
@@ -0,0 +1,120 @@
+"""P32: one gradient-response intervention, fresh Berny histories, bounded paired runs."""
+from __future__ import annotations
+import argparse
+import json
+import os
+import sys
+import time
+from pathlib import Path
+import numpy as np
+from r7_common import (BASE,BERNY,sha,write,fresh,geometry,versions,clean_environment,
+    factory,gradient,profile,assert_connectivity,load_plan,bounded,registration)
+
+
+def validate_permit(a,m):
+    if m['family']!='chains':return
+    if not a.permit or not a.authorization:
+        raise ValueError('Six-chain jobs require a recorded positive decision and authorization commit')
+    registration(a.authorization);d=json.loads(Path(a.permit).read_text())
+    if d.get('eligible_for_chain_trial') is not True or d.get('registration')!=m['registration']:
+        raise ValueError('The supplied decision does not authorize this experiment')
+    if d.get('chains_plan_sha256')!=sha(a.plan):
+        raise ValueError('Chain inputs were not sealed in the approved decision')
+
+
+def native(a):
+    plan,m=load_plan(a.plan);validate_permit(a,m);packages=versions(native=True)
+    if m.get('packages',{}).get('rdkit') not in (None,packages['rdkit']):
+        raise RuntimeError('RDKit differs from the frozen starting-geometry environment')
+    if m['family'] not in ('calibration','pilot','chains'):raise ValueError('Not an optimizer plan')
+    expected={'calibration':(100,1800),'pilot':(80,3600),'chains':(100,19800)}[m['family']]
+    if (m['budget'],m['seconds_per_arm'])!=expected:raise ValueError('Budget differs from registration')
+    rec=next((r for r in m['cases'] if r['key']==a.key),None)
+    if rec is None:raise ValueError('Case not in frozen plan')
+    clean_environment();sym,x=geometry(plan.parent/rec['geometry']);out=fresh(a.out)
+    start=time.monotonic();trace=[];response=a.arm=='full'
+    common=dict(base=BASE,registration=m['registration'],plan_sha256=sha(plan),key=a.key,
+        family=m['family'],arm=a.arm,grid_response=response,packages=packages,
+        input_geometry_sha256=rec['geometry_sha256'],budget=m['budget'],
+        authorization_commit=a.authorization,permit_sha256=sha(a.permit) if a.permit else None,
+        berny_parameters=BERNY,adopted=False)
+    write(out/'result.json',dict(common,status='running'))
+    from pyscf.geomopt.berny_solver import kernel
+    mf=factory(sym,x,rec['spin'],'production');g=gradient(mf,response)
+    def cb(env):
+        scanner=env['g_scanner'];gg=np.asarray(env['gradients'])
+        if bool(scanner.grid_response)!=response:raise RuntimeError('Scanner lost grid-response setting')
+        if not bool(scanner.auxbasis_response):raise RuntimeError('Scanner lost DF response')
+        if scanner.base.with_solvent.method.upper()!='C-PCM':raise RuntimeError('Solvent method changed')
+        if not scanner.converged or not np.isfinite(env['energy']) or not np.isfinite(gg).all():
+            raise RuntimeError('Unconverged SCF/gradient is not a geometry evaluation')
+        state=env['optimizer']._state
+        trace.append(dict(cycle=int(env['cycle']),energy_Eh=float(env['energy']),
+            trust_pre_send=float(state.trust),cartesian_gmax=float(abs(gg).max()),
+            cartesian_grms=float(np.sqrt(np.mean(gg*gg))),
+            scf_cycles=int(getattr(scanner.base,'cycles',-1)),grid_response=bool(scanner.grid_response)))
+        if len(trace)>m['budget']:raise RuntimeError('Gradient-evaluation budget exceeded')
+        write(out/'trace.json',trace)
+        write(out/'latest.json',dict(sym=sym,x=env['mol'].atom_coords(unit='Angstrom').tolist(),
+                                    evaluations=len(trace),input_geometry_sha256=rec['geometry_sha256']))
+    try:
+        # grid_response is configured on Gradients, NOT passed as a Berny keyword.
+        converged,mol=kernel(g,maxsteps=m['budget'],callback=cb,assert_convergence=True,**BERNY)
+        result=dict(common,evaluations=len(trace),berny_converged=bool(converged),
+            wall_s=time.monotonic()-start,auxbasis=repr(mf.with_df.auxbasis),
+            resolved_auxiliary_basis=repr(getattr(getattr(mf.with_df,'auxmol',None),'basis',None)))
+        if not converged:
+            write(out/'result.json',dict(result,status='censored_evaluations'));return
+        x=mol.atom_coords(unit='Angstrom');assert_connectivity(rec['smiles'],sym,x)
+        geom=out/(a.key+'.xyz.json');write(geom,dict(sym=sym,x=x.tolist()))
+        desc=profile(sym,x,a.key,out/(a.key+'.sigma'),rec['spin'],
+            dict(geometry_converged=True,geometry_protocol='A-R7-grid-response' if response else 'R7-original-gradient-control',
+                 source='R7 isolated trial; not adopted',r7_registration=m['registration'],
+                 r7_plan_sha256=sha(plan),r7_input_geometry_sha256=rec['geometry_sha256']))
+        result.update(status='berny_converged',profile=desc,geometry_sha256=sha(geom),
+                      wall_s=time.monotonic()-start)
+        write(out/'result.json',result)
+    except Exception as e:
+        write(out/'result.json',dict(common,status='failed',error=repr(e),
+            evaluations=len(trace),wall_s=time.monotonic()-start))
+        raise
+
+
+def run_case(a):
+    plan,m=load_plan(a.plan);validate_permit(a,m)
+    r=next((r for r in m['cases'] if r['key']==a.key),None)
+    if r is None:raise ValueError('Unknown case')
+    if m['family']=='chains' and a.arm=='pair':
+        raise ValueError('One chain arm per worker: two 5.5-hour arms exceed the runner cap')
+    out=fresh(a.out)
+    arms=['off','full'] if a.arm=='pair' else [a.arm]
+    if len(arms)==2 and int(__import__('hashlib').sha256(a.key.encode()).hexdigest(),16)%2:
+        arms.reverse()
+    records=[]
+    for arm in arms:
+        dest=out/arm
+        cmd=[sys.executable,str(Path(__file__).resolve()),'native','--plan',str(plan),
+             '--key',a.key,'--arm',arm,'--out',str(dest)]
+        if a.permit:cmd+=['--permit',str(Path(a.permit).resolve()),'--authorization',a.authorization]
+        run=bounded(cmd,dest,int(m['seconds_per_arm']));records.append(run)
+        if run['execution_status']=='deadline':
+            old=json.loads((dest/'result.json').read_text()) if (dest/'result.json').exists() else {}
+            trace=json.loads((dest/'trace.json').read_text()) if (dest/'trace.json').is_file() else []
+            old.update(base=BASE,registration=m['registration'],plan_sha256=sha(plan),key=a.key,
+                       evaluations=len(trace),
+                       arm=arm,status='censored_deadline',deadline_s=m['seconds_per_arm'],
+                       wall_s=run['wall_s'],adopted=False)
+            write(dest/'result.json',old)
+        # Continue the other arm even after a scientific or operational failure.
+    write(out/'pair.json',dict(key=a.key,plan_sha256=sha(plan),order=arms,runs=records))
+    if any(r['execution_status']=='child_failed' for r in records):raise SystemExit(1)
+
+
+def main():
+    p=argparse.ArgumentParser();s=p.add_subparsers(dest='command',required=True)
+    for name in ('native','run_case'):
+        q=s.add_parser(name);q.add_argument('--plan',required=True);q.add_argument('--key',required=True)
+        q.add_argument('--arm',choices=['off','full'] if name=='native' else ['off','full','pair'],required=True)
+        q.add_argument('--out',required=True);q.add_argument('--permit');q.add_argument('--authorization')
+    a=p.parse_args();globals()[a.command](a)
+if __name__=='__main__':main()
diff --git a/.github/workflows/r7_review.yml b/.github/workflows/r7_review.yml
new file mode 100644
--- /dev/null
+++ b/.github/workflows/r7_review.yml
@@ -0,0 +1,111 @@
+name: r7-review
+run-name: r7/${{ inputs.plan }}
+# Manual experiment only. P32 chain plans require a committed positive permit.
+on:
+  workflow_dispatch:
+    inputs:
+      plan:
+        description: 'Committed cloud/r7/.../plan.json'
+        required: true
+        type: string
+      permit:
+        description: 'Committed chain decision JSON, only for chain family'
+        required: false
+        default: ''
+        type: string
+      authorization:
+        description: 'Full authorization commit SHA, only for chain family'
+        required: false
+        default: ''
+        type: string
+permissions:
+  contents: read
+env:
+  OMP_NUM_THREADS: '4'
+  OPENBLAS_NUM_THREADS: '1'
+  MKL_NUM_THREADS: '1'
+  BLIS_NUM_THREADS: '1'
+  ZC_PCM3C: '1'
+  ZC_PCM3C_MB: '2000'
+  PYTHONPATH: 'src:scripts'
+  MPLBACKEND: Agg
+jobs:
+  plan:
+    runs-on: ubuntu-latest
+    outputs:
+      matrix: ${{ steps.make.outputs.matrix }}
+    steps:
+      - uses: actions/checkout@v4
+        timeout-minutes: 3
+      - id: make
+        env:
+          PLAN_PATH: ${{ inputs.plan }}
+          PERMIT_PATH: ${{ inputs.permit }}
+          AUTHORIZATION: ${{ inputs.authorization }}
+        run: |
+          python - <<'PYCODE'
+          import hashlib,json,os,re
+          from pathlib import Path
+          root=Path.cwd().resolve();p=(root/os.environ['PLAN_PATH']).resolve()
+          if not p.is_relative_to(root/'cloud'/'r7'):raise ValueError('Plan must be committed under cloud/r7')
+          m=json.loads(p.read_text());family=m['family']
+          if family not in ('calibration','pilot','chains','referee','screen'):raise ValueError('Bad plan family')
+          if family=='chains':
+              q=(root/os.environ['PERMIT_PATH']).resolve()
+              if not q.is_relative_to(root/'cloud'/'r7'):raise ValueError('Bad permit location')
+              d=json.loads(q.read_text())
+              if d.get('eligible_for_chain_trial') is not True:raise ValueError('Chain escalation blocked')
+              if d.get('chains_plan_sha256')!=hashlib.sha256(p.read_bytes()).hexdigest():raise ValueError('Chain plan changed')
+              if not re.fullmatch('[0-9a-f]{40}',os.environ['AUTHORIZATION']):raise ValueError('Authorization commit required')
+          jobs=[]
+          for r in m['cases']:
+              if not re.fullmatch('[A-Z]{14}-[A-Z]{10}-[A-Z]',r['key']):raise ValueError('Invalid key')
+              for arm in (('off','full') if family=='chains' else ('pair',)):
+                  jobs.append({'key':r['key'],'arm':arm,'family':family})
+          with open(os.environ['GITHUB_OUTPUT'],'a') as f:f.write('matrix='+json.dumps({'include':jobs})+'\n')
+          PYCODE
+  case:
+    needs: plan
+    runs-on: ubuntu-latest
+    timeout-minutes: 355
+    strategy:
+      fail-fast: false
+      max-parallel: 20
+      matrix: ${{ fromJson(needs.plan.outputs.matrix) }}
+    steps:
+      - uses: actions/checkout@v4
+        timeout-minutes: 3
+      - uses: actions/setup-python@v5
+        timeout-minutes: 5
+        with:
+          python-version: '3.11'
+      - name: pinned native environment
+        timeout-minutes: 10
+        run: python -m pip install --retries 1 --timeout 30 pyscf==2.14.0 pyberny==0.7.0 rdkit==2026.03.6 numpy scipy pandas matplotlib
+      - name: bounded case
+        env:
+          PLAN_PATH: ${{ inputs.plan }}
+          PERMIT_PATH: ${{ inputs.permit }}
+          AUTHORIZATION: ${{ inputs.authorization }}
+          CASE_KEY: ${{ matrix.key }}
+          CASE_ARM: ${{ matrix.arm }}
+          CASE_FAMILY: ${{ matrix.family }}
+        run: |
+          python - <<'PYCODE'
+          import os,subprocess,sys
+          from pathlib import Path
+          family=os.environ['CASE_FAMILY'];key=os.environ['CASE_KEY'];arm=os.environ['CASE_ARM']
+          module='r7_optimize.py' if family in ('calibration','pilot','chains') else ('r7_referee.py' if family=='referee' else 'r7_screen.py')
+          out=Path('out')/key/(arm if family=='chains' else 'case')
+          args=[sys.executable,'scripts/'+module,'run_case','--plan',os.environ['PLAN_PATH'],'--key',key,'--out',str(out)]
+          if module=='r7_optimize.py':args+=['--arm',arm]
+          if family=='chains':args+=['--permit',os.environ['PERMIT_PATH'],'--authorization',os.environ['AUTHORIZATION']]
+          raise SystemExit(subprocess.run(args).returncode)
+          PYCODE
+      - uses: actions/upload-artifact@v4
+        timeout-minutes: 5
+        if: always()
+        with:
+          name: r7-${{ matrix.family }}-${{ matrix.key }}-${{ matrix.arm }}
+          path: out
+          retention-days: 60
```

<!-- PATCH:P33 -->
```diff
diff --git a/scripts/r7_referee.py b/scripts/r7_referee.py
new file mode 100644
--- /dev/null
+++ b/scripts/r7_referee.py
@@ -0,0 +1,120 @@
+"""P33: prospective finite-resolution derivative checks, not a retrospective P30 pass."""
+from __future__ import annotations
+from r7_common import source_fingerprint
+import argparse
+import json
+import sys
+import time
+from pathlib import Path
+import numpy as np
+from r7_common import (BASE,sha,write,fresh,geometry,versions,registration,clean_environment,
+                       factory,gradient,load_plan,bounded,verdict)
+
+from r7_common import fd_assess as assess, FD_TAU as TAU, FD_STEPS as STEPS
+
+def plan(a):
+    registration(a.registration);p,m=load_plan(a.pilot_plan);out=fresh(a.out);cases=[]
+    if m['family']!='pilot':raise ValueError('Use the fixed three-case P26 pilot plan')
+    for r in m['cases']:
+        dest=out/(r['key']+'.json');dest.write_bytes((p.parent/r['geometry']).read_bytes())
+        cases.append(dict(r,geometry=dest.name,geometry_sha256=sha(dest)))
+    original=Path('cloud/r5/shape-plan');old=json.loads((original/'manifest.json').read_text())
+    for name in ('methanol','ethylene_glycol'):
+        r=next(x for x in old['panel'] if x['name']==name);source=original/r['geometry']
+        if sha(source)!=r['geometry_sha256']:raise ValueError('Saved R5 control geometry changed')
+        dest=out/(r['key']+'.json');dest.write_bytes(source.read_bytes())
+        cases.append(dict(key=r['key'],smiles=r['smiles'],spin=r['spin'],geometry=dest.name,geometry_sha256=sha(dest)))
+    write(out/'plan.json',dict(sources=source_fingerprint('referee'),base=BASE,registration=a.registration,family='referee',cases=cases,
+        seconds_per_case=7200,maximum_SCF_per_case=82,maximum_gradients_per_case=3,
+        tolerance=TAU,steps_Bohr=STEPS.tolist()))
+
+
+def native(a):
+    p,m=load_plan(a.plan);v=versions(native=True)
+    if m['family']!='referee' or v['rdkit']!='2026.03.6':raise ValueError('Fixed R7 referee and RDKit 2026.03.6 required')
+    r=next((x for x in m['cases'] if x['key']==a.key),None)
+    if r is None:raise ValueError('Unknown referee case')
+    from r6_referee import probe_directions
+    from zcosmo.pyscf_cosmo import BOHR
+    clean_environment();sym,x=geometry(p.parent/r['geometry']);out=fresh(a.out);start=time.monotonic();calls=[]
+    def scf(pos,precision):
+        if time.monotonic()-start>6800:raise TimeoutError('Referee internal deadline')
+        mf=factory(sym,pos,r['spin'],precision);e=float(mf.kernel())
+        if not mf.converged or not np.isfinite(e):raise RuntimeError('SCF failed')
+        calls.append(dict(precision=precision,E_Eh=e,grid_points=len(mf.grids.coords),
+                          small_rho_cutoff=float(mf.small_rho_cutoff)))
+        write(out/'calls.json',calls)
+        return e,mf
+    write(out/'result.json',dict(status='running',key=a.key,input_geometry_sha256=r['geometry_sha256']))
+    try:
+        _,mt=scf(x,'tight');gt=np.asarray(gradient(mt,True).kernel())
+        _,ms=scf(x,'strict');gf=np.asarray(gradient(ms,True).kernel());go=np.asarray(gradient(ms,False).kernel())
+        if not np.isfinite([gt,gf,go]).all():raise ValueError('Nonfinite center gradient')
+        records=[]
+        for label,direction in probe_directions(r['smiles'],sym,x):
+            direction=direction/np.linalg.norm(direction)
+            tables={};counts=[]
+            for precision in ('tight','strict'):
+                vals=[]
+                for h in STEPS:
+                    pair=[]
+                    for sign in (1.,-1.):
+                        e,mf=scf(x+sign*h*BOHR*direction,precision)
+                        pair.append(e);counts.append(len(mf.grids.coords))
+                    vals.append(pair)
+                tables[precision]=vals
+            result=assess(tables['tight'],tables['strict'],float(np.sum(gt*direction)),
+                          float(np.sum(gf*direction)),float(np.sum(go*direction)),
+                          topology_stable=len(set(counts+[len(mt.grids.coords),len(ms.grids.coords)]))==1)
+            result.update(direction=label,unit_L2_direction=direction.tolist(),energies=tables,
+                          sampled_grid_counts=counts)
+            records.append(result);write(out/'directions.json',records)
+        if len(calls)>82:raise AssertionError('SCF budget exceeded')
+        np.savez_compressed(out/'gradients.npz',x_A=x,full_tight=gt,full_strict=gf,off_strict=go)
+        result=dict(base=BASE,registration=m['registration'],key=a.key,status='diagnostic_complete',
+            input_geometry_sha256=r['geometry_sha256'],plan_sha256=sha(p),records=records,
+            full_response_consistent=all(z['full_verdict']=='consistent' for z in records),
+            SCF_evaluations=len(calls),gradient_evaluations=3,wall_s=time.monotonic()-start,
+            center_full_gmax=float(abs(gf).max()),center_full_grms=float(np.sqrt(np.mean(gf*gf))),
+            adopted=False,authorizes_optimizer=False,authorizes_R6_stage2=False)
+        write(out/'result.json',result)
+        # Completed diagnostics return zero even when their scientific verdict is negative.
+    except Exception as e:
+        write(out/'result.json',dict(status='censored_deadline' if isinstance(e,TimeoutError) else 'failed',
+            error=repr(e),SCF_evaluations=len(calls),key=a.key,plan_sha256=sha(p),adopted=False))
+        raise
+
+
+def run_case(a):
+    p,m=load_plan(a.plan)
+    if m['family']!='referee':raise ValueError('Wrong family')
+    bounded([sys.executable,str(Path(__file__).resolve()),'native','--plan',str(p),
+             '--key',a.key,'--out',str(Path(a.out).resolve())],a.out,7200)
+
+
+def check(a):
+    p,m=load_plan(a.plan);results=[]
+    for r in m['cases']:
+        hits=[]
+        for f in Path(a.results).rglob('result.json'):
+            d=json.loads(f.read_text())
+            if d.get('key')==r['key'] and d.get('plan_sha256')==sha(p):hits.append((f,d))
+        if len(hits)!=1:raise ValueError('Missing or duplicate referee result')
+        f,d=hits[0]
+        if d.get('status')!='diagnostic_complete':raise ValueError('Incomplete referee')
+        if d['input_geometry_sha256']!=r['geometry_sha256']:raise ValueError('Geometry identity mismatch')
+        results.append(dict(key=r['key'],result_sha256=sha(f),passed=d['full_response_consistent']))
+    write(a.out,dict(passed=all(r['passed'] for r in results),cases=results,
+        registration=m['registration'],historical_P30_remains_failed=True,
+        scope='New R7 directional gate only; no Hessian or basin integration authorized'))
+    if not all(r['passed'] for r in results):raise SystemExit(2)
+
+
+def main():
+    p=argparse.ArgumentParser();s=p.add_subparsers(dest='command',required=True)
+    q=s.add_parser('plan');q.add_argument('--pilot-plan',required=True);q.add_argument('--registration',required=True);q.add_argument('--out',required=True)
+    for name in ('native','run_case'):
+        q=s.add_parser(name);q.add_argument('--plan',required=True);q.add_argument('--key',required=True);q.add_argument('--out',required=True)
+    q=s.add_parser('check');q.add_argument('--plan',required=True);q.add_argument('--results',required=True);q.add_argument('--out',required=True)
+    a=p.parse_args();globals()[a.command](a)
+if __name__=='__main__':main()
```

<!-- PATCH:P34 -->
```diff
diff --git a/scripts/r7_screen.py b/scripts/r7_screen.py
new file mode 100644
--- /dev/null
+++ b/scripts/r7_screen.py
@@ -0,0 +1,154 @@
+"""P34: a frozen primary-profile sample, fixed-coordinate gradients, and local stresses.
+
+No optimization, Hessian certificate, profile replacement, or claim about every
+geometry in a ball. Primary-set screen flags are not experimental errors.
+"""
+from __future__ import annotations
+from r7_common import source_fingerprint
+import argparse
+import hashlib
+import json
+import sys
+import time
+from pathlib import Path
+import numpy as np
+import pandas as pd
+from r7_common import (BASE,SENTINELS,sha,write,fresh,registration,geometry,versions,
+    factory,gradient,profile,load_plan,bounded,clean_environment,internal_projection)
+
+
+def plan(a):
+    from r4_common import selected_profiles
+    from zcosmo.pyscf_cosmo_v2 import OPEN_SHELL
+    registration(a.registration);out=fresh(a.out)
+    compounds=pd.read_csv('data/benchmark/compounds.csv');smi=compounds.set_index('inchikey').smiles.to_dict()
+    primary={k:p for k,folder,p in selected_profiles(a.profile_root,compounds) if folder=='profiles_v2'}
+    if len(primary)!=630:raise ValueError('The registered 630-member primary universe changed')
+    ordering=sorted(primary,key=lambda k:hashlib.sha256(('R7-primary-screen-v1|'+k).encode()).hexdigest())
+    sample=set(ordering[:32])
+    if not set(SENTINELS)<=set(primary):raise ValueError('A frozen sentinel is absent from primary')
+    chosen=sample|set(SENTINELS);cases=[];population={k:sha(p) for k,p in primary.items()}
+    for key in sorted(chosen):
+        source=primary[key];meta=json.loads(source.read_text().splitlines()[0][8:])
+        if meta.get('geometry_converged') is not True:raise ValueError('Primary convergence metadata absent')
+        original=source.with_suffix('.xyz.json');sym,x=geometry(original)
+        dest=out/'geometries'/(key+'.json');dest.parent.mkdir(exist_ok=True);dest.write_bytes(original.read_bytes())
+        ref=out/'references'/(key+'.sigma');ref.parent.mkdir(exist_ok=True);ref.write_bytes(source.read_bytes())
+        cases.append(dict(key=key,smiles=smi[key],spin=OPEN_SHELL.get(smi[key],0),
+            geometry=str(dest.relative_to(out)),geometry_sha256=sha(dest),
+            reference_profile=str(ref.relative_to(out)),reference_sha256=sha(ref),
+            probability_sample=key in sample,sentinel=key in SENTINELS))
+    write(out/'plan.json',dict(sources=source_fingerprint('screen'),base=BASE,registration=a.registration,family='screen',cases=cases,
+        population_profile_hashes=population,universe=630,probability_sample_size=32,
+        selection='SHA256 R7-primary-screen-v1|key, plus eight named structural sentinels',
+        stress_max_atom_displacement_A=.01,seconds_per_case=3600,packages=versions()))
+
+
+def native(a):
+    from r3_common import read_sigma
+    p,m=load_plan(a.plan);versions(native=True)
+    if m['family']!='screen':raise ValueError('Not the fixed primary screen')
+    r=next((q for q in m['cases'] if q['key']==a.key),None)
+    if r is None:raise ValueError('Key not selected in advance')
+    clean_environment();out=fresh(a.out);sym,x=geometry(p.parent/r['geometry']);t=time.monotonic()
+    common=dict(base=BASE,registration=m['registration'],key=a.key,plan_sha256=sha(p),
+                geometry_sha256=r['geometry_sha256'],adopted=False)
+    write(out/'result.json',dict(common,status='running'))
+    try:
+        mf=factory(sym,x,r['spin'],'production');e=float(mf.kernel())
+        if not mf.converged or not np.isfinite(e):raise RuntimeError('SCF failed')
+        off=np.asarray(gradient(mf,False).kernel());full=np.asarray(gradient(mf,True).kernel())
+        if not np.isfinite([off,full]).all():raise ValueError('Gradient failed')
+        v=-internal_projection(x,full);length=float(np.max(np.linalg.norm(v,axis=1)))
+        label='projected negative full-response gradient'
+        if length<1e-12:
+            from r6_referee import probe_directions
+            name,v=probe_directions(r['smiles'],sym,x)[0]
+            length=float(np.max(np.linalg.norm(v,axis=1)));label='fixed fallback '+name
+        v=v/length
+        np.savez_compressed(out/'gradients.npz',x_A=x,g_off=off,g_full=full,stress_direction=v)
+        outputs={}
+        for name,sign in (('center',0.),('minus',-1.),('plus',1.)):
+            if time.monotonic()-t>3400:raise TimeoutError('Fixed screen deadline')
+            outputs[name]=profile(sym,x+sign*.01*v,a.key,out/(name+'.sigma'),r['spin'],
+                dict(geometry_converged='R7-fixed-stress',source='R7 screen, not optimized or adopted',
+                     r7_registration=m['registration'],r7_plan_sha256=sha(p)))
+        _,center,_=read_sigma(out/'center.sigma');_,stored,_=read_sigma(p.parent/r['reference_profile'])
+        bin_changes={}
+        for name in ('minus','plus'):
+            _,z,_=read_sigma(out/(name+'.sigma'))
+            bin_changes[name]=dict(raw_max=float(abs(z-center).max()),
+                normalized_L1=float(abs(z/z.sum()-center/center.sum()).sum()))
+        write(out/'result.json',dict(common,status='diagnostic_complete',profiles=outputs,
+            SVP_energy_Eh=e,SVP_SCF=1,SVP_gradients=2,TZVP_single_points=3,
+            g_off_max=float(abs(off).max()),g_full_max=float(abs(full).max()),
+            response_change_max=float(abs(full-off).max()),response_force_flag=bool(abs(full-off).max()>1e-5),
+            direction=label,stress_A=.01,bin_changes=bin_changes,
+            stored_vs_recomputed_raw_max=float(abs(stored-center).max()),
+            wall_s=time.monotonic()-t,
+            scope='Finite directional stresses at saved coordinates; no minimum-displacement or basin-wide bound'))
+    except Exception as e:
+        write(out/'result.json',dict(common,status='censored_deadline' if isinstance(e,TimeoutError) else 'failed',
+                                    error=repr(e),wall_s=time.monotonic()-t))
+        raise
+
+
+def run_case(a):
+    p,m=load_plan(a.plan)
+    if m['family']!='screen':raise ValueError('Wrong plan')
+    bounded([sys.executable,str(Path(__file__).resolve()),'native','--plan',str(p),
+             '--key',a.key,'--out',str(Path(a.out).resolve())],a.out,3600)
+
+
+def report(a):
+    from scipy.stats import hypergeom
+    p,m=load_plan(a.plan);rows=[]
+    for case in m['cases']:
+        matches=[]
+        for f in Path(a.results).rglob('result.json'):
+            d=json.loads(f.read_text())
+            if d.get('key')==case['key'] and d.get('plan_sha256')==sha(p):matches.append((f,d))
+        row=dict(key=case['key'],probability_sample=case['probability_sample'],sentinel=case['sentinel'],screen_positive=None)
+        if len(matches)!=1:
+            row['status']='missing_or_duplicate_native';rows.append(row);continue
+        f,d=matches[0];row['native_sha256']=sha(f)
+        if d.get('status')!='diagnostic_complete':
+            row['status']=d.get('status','unknown');rows.append(row);continue
+        ag=Path(a.affinities)/case['key']/'gate.json'
+        if not ag.is_file():row['status']='missing_affinity';rows.append(row);continue
+        q=json.loads(ag.read_text())
+        if q.get('key')!=case['key'] or q.get('registration')!=m['registration'] or q.get('limit')!=.01:
+            raise ValueError('Wrong affinity evidence')
+        if q['reference_sha256']!=d['profiles']['center']['sha256']:
+            raise ValueError('Affinity center differs')
+        if {z['sha256'] for z in q['candidates']}!={d['profiles'][k]['sha256'] for k in ('minus','plus')}:
+            raise ValueError('Wrong stress candidates')
+        checks=[z for c in q['candidates'] for z in c['models'].values()]
+        complete=all(z['coverage_identical'] and z['max_abs_change'] is not None for z in checks)
+        row.update(status='complete' if complete else 'affinity_unresolved',
+            response_force_flag=d['response_force_flag'],response_change_max=d['response_change_max'],
+            max_affinity_change=max(z['max_abs_change'] or 0. for z in checks),affinity_sha256=sha(ag))
+        if complete:row['screen_positive']=row['max_affinity_change']>=.01
+        rows.append(row)
+    random=[r for r in rows if r['probability_sample']];N=630;n=len(random)
+    complete=all(r['screen_positive'] is not None for r in random)
+    upper=None
+    if complete:
+        k=sum(r['screen_positive'] for r in random)
+        accepted=[K for K in range(k,N-n+k+1) if hypergeom.cdf(k,N,K,n)>=.05]
+        upper=max(accepted)/N
+    write(a.out,dict(base=BASE,registration=m['registration'],rows=rows,
+        random_sample_complete=complete,one_sided_95_upper_fraction=upper,
+        interpretation='Sampling-model bound on this finite-stress screen ONLY, conditional on SHA ordering behaving as a uniform sample. Not an accuracy or stationarity bound.',
+        primary_profiles_changed=0))
+
+
+def main():
+    p=argparse.ArgumentParser();s=p.add_subparsers(dest='command',required=True)
+    q=s.add_parser('plan');q.add_argument('--profile-root',required=True);q.add_argument('--registration',required=True);q.add_argument('--out',required=True)
+    for name in ('native','run_case'):
+        q=s.add_parser(name);q.add_argument('--plan',required=True);q.add_argument('--key',required=True);q.add_argument('--out',required=True)
+    q=s.add_parser('report')
+    for name in ('plan','results','affinities','out'):q.add_argument('--'+name,required=True)
+    a=p.parse_args();globals()[a.command](a)
+if __name__=='__main__':main()
```

<!-- PATCH:P35 -->
```diff
diff --git a/docs/astra/round7/GLYCOL_STATUS.md b/docs/astra/round7/GLYCOL_STATUS.md
new file mode 100644
--- /dev/null
+++ b/docs/astra/round7/GLYCOL_STATUS.md
@@ -0,0 +1,15 @@
+Glycol profile discrepancy: unresolved mechanism, no envelope-matching campaign
+
+Reference source: ddf22b19f9e1750308bd11572786b44d407a80f9. Evidence is the frozen R5/R6 output, not a new ThermoML holdout.
+
+The P29 finite sample has maximum raw polar-tail areas of approximately 31.4, 34.8, 32.7 and 34.3 square angstroms for EG, DEG, TEG and tetraEG; the corresponding UD values are approximately 33.0, 38.0, 42.3 and 46.8. The last two catalogs are incomplete. For an arithmetic convex average of those raw area profiles, the tail cannot exceed the largest member's tail. This rules out reproducing those UD tails by positive weights on that particular sample. Normalized-profile averages have their own normalized-tail envelope; rescaling an average is a different intervention.
+
+This does not exclude unsampled basins, and it does not establish that UD represents the equilibrium liquid distribution. In particular, the stored open reference is outside some proposal envelopes. P25 varied two basis sizes and two switching prescriptions within one functional/model family. It did not compare all electronic methods or reproduce the unavailable DMol3 inputs. No UD raw segment table was available for a direct raw-to-raw comparison. The historical causal decomposition therefore remains unidentified.
+
+The R7 grid-response trial addresses a concrete numerical-gradient problem. Its completion criteria must not include proximity to UD tails or smaller ThermoML error. A successful response-gradient optimization would justify revisiting the stationarity of particular saved samples. It would not accept P26, validate a thermal basin partition, or authorize another ensemble calculation by itself.
+
+The current envelope-matching campaign receives zero additional QC budget. Do not choose extended conformers, discard intramolecular hydrogen bonds, tune a smoothing constant, or fit population weights to the UD histogram. Retain the 630-profile primary set and the six S1/S2 files with their actual provenance. Individual replacements require the separately registered optimizer and compatibility decisions.
+
+Evidence that can change this decision is concrete: recovery of the generating UD geometries and raw surface files together with their electronic/cavity settings; or independent, basis/grid/response-converged electrostatic references at frozen known geometries; or a complete, independently reproducible basin and nuclear-partition audit under one free-energy convention. Acquiring provenance is a zero-QC task. Any new physical calculation needs a fixed structural panel including water and branched polyol controls, and a prospective budget. Missing historical files on the Mac do not prove that no upstream archive exists.
+
+The present open-profile pipeline is a reproducible, explicitly tested alternative source of single-geometry sigma profiles. It is not an accuracy-equivalent UD replacement or an established phase-dependent conformer ensemble. P28's accepted endpoint correction does not remove this distinction. Keep pre-P28 matched comparisons labelled as such, and do not infer a corrected matched-subset mean from differently sized standalone means.
```

<!-- PATCH:REG7 -->
```diff
diff --git a/docs/astra/round7/PROPOSED_REGISTRATION.md b/docs/astra/round7/PROPOSED_REGISTRATION.md
new file mode 100644
--- /dev/null
+++ b/docs/astra/round7/PROPOSED_REGISTRATION.md
@@ -0,0 +1,31 @@
+Proposed R7 registration. This file is not evidence of adoption or execution.
+
+Append adopted text with the actual timestamp and commit identifier before generating new R7 starts or interpreting candidate output. Source baseline is ddf22b19f9e1750308bd11572786b44d407a80f9 plus the archived R7 patches. The R6 P30 gate remains failed and its stage 2 remains unrun. The following is a new experiment motivated by known data, not a fresh experimental holdout. P15/P17/P19 decisions stand. P20 and P28 remain accepted within their actual scopes. Nothing is fitted to ThermoML.
+
+P32 changes only the optimizer's XC grid response from False to True on the existing BP86/def2-SVP density-fitted grid-level-2 C-PCM conductor path, epsilon 1e9, Lebedev order 17, project radii, production SCF conv_tol 1e-8 and default orbital-gradient tolerance. Keep density-grid pruning unchanged. Keep auxiliary-basis and solvent gradients. Pin PySCF 2.14.0 and pyberny 0.7.0. Supply a configured Gradients object to berny_solver.kernel. Both arms use fresh optimizer histories and the unchanged gradientmax 4.5e-4, gradientrms 1.5e-4, stepmax 1.8e-3 and steprms 1.2e-3, including Berny's unchanged on-sphere predicate. No optimizer pickle, trust override, tighter SCF, finer grid, gradient-only stop, or original-force confirmation stage is added. The comparison is between gradients, not two convergence definitions.
+
+Freeze the exact historical 25 targets and 2302 query occurrences from their archived query manifest. validation_set.csv alone contains 26 candidates and must not redefine this set. Freeze one seed-7 GFN2-xTB start per calibration target before either arm. Run both arms sequentially on the same four-core worker, alternating order by SHA256(key) parity. Each calibration arm has 100 gradient evaluations and 1800 seconds including its TZVP profile. Record all failures and censoring. The 25-target numerical compatibility gate requires both arms to pass the original Berny predicate for all 25; identical finite coverage; maximum COSMO-SAC-dsp change below 0.01; and median absolute COSMO-SAC-dsp difference from UD below 0.15 on the frozen occurrences. Expect the historical 2271 finite dsp and 2302 finite Z0x occurrences; a count or mask mismatch blocks the gate. Use separate processes for each target/profile set. P18 flags and P28 exact endpoints are enabled identically in both arms. Report raw and normalized profile differences without reinterpreting E tolerances.
+
+Timing policy is explicitly separated before results: report optimizer-plus-profile worker time, excluding the one shared xTB preparation. The 1.50 ratio remains a routine-throughput indicator, not a criterion for targeted rescue of previously nonterminating cases. A bounded targeted rescue has its own wall-time ceiling and is not a proposal to change the default for all 630. This new policy does not alter the rejection of P19 under P19's original conjunctive cost gate.
+
+After calibration compatibility passes, run exactly the three P26-censored geometries used in P30: nonane seed 20261006 rank 1, TEG seed 20261006 rank 1 and DME seed 20261005 rank 1. Require the original proposal identities, recorded 80-evaluation censoring and the P30 geometry hashes. Both new arms start from the same frozen Cartesian coordinates with fresh histories, production SCF tolerances and the original Berny predicate. Each arm gets at most 80 new gradient evaluations and 3600 seconds including profile generation. A scientific censor is distinct from a native failure or a missing result. All six arm outcomes are required.
+
+The six-chain inputs are also frozen before pilot output is read: exactly one deliberately designated final saved checkpoint per fixed S1/S2 key, never an automatically chosen latest file among conflicts. No stopped driver or old optimizer pickle is restarted. A separate authorization commit may permit the chain stage only if the 25-target numerical compatibility gate passes, at least two of the three pilots converge with full response while their off controls remain censored, zero pilots converge only in the off arm, and there are no failed or missing pilot arms. Bind the authorization to the calibration gate and the already frozen chain-plan hash. If this decision fails, the chain campaign stays closed in R7.
+
+For each authorized chain, each arm has at most 100 gradient evaluations and 19800 seconds. Run the 12 arm-jobs independently, one arm per four-core worker, not a serial 11-hour pair. There is no resume or budget extension. Only the actual original Berny predicate evaluated with the declared gradient establishes that arm's convergence. Keep every result, including off-only successes and regressions. Do not claim omitted response caused all historical stalls from a subset of successful interventions.
+
+After a global acceptance record, a full-response chain result can become an individual replacement candidate only if the profile completed, connectivity and provenance checks pass, and its fixed local compatibility check passes. Compare against that chain's existing flagged profile in a complete unchanged open636 background, in separate processes: every benchmark IDAC identity involving the chain plus both-role water/methanol/nonane/DME probes at 250, 298.15 and 400 K. Require identical finite masks and maximum absolute change below 0.05 in both dsp and P28-Z0x on evaluable probes. A larger change leaves an explicitly Berny-converged A experimental geometry, but does not automatically replace a flagged profile. Raw bin differences are reported. Promotion is a separate recorded, backed-up metadata/provenance operation; no R7 helper writes profiles_v2. An off-arm original-protocol success is also reported and may follow the existing original-protocol replacement route. No blanket 630-profile regeneration is authorized.
+
+P33 is a new stationarity-referee diagnostic, separate from the optimizer test. Use the same five geometric identities as P30, but normalize each projected Cartesian probe to unit L2 norm. Do not apply the new gate to the old collectively normalized data as if it were the same test. The scientific target is tau=1e-5 Eh/Bohr, one fifth of R6's pre-existing 5e-5 Cartesian force target. This is an engineering numerical-accuracy budget, not a fitted statistical confidence limit.
+
+For each direction use the fixed Bohr ladder 0.016, 0.008, 0.004, 0.002, 0.001. Compute plus/minus energies at tight SCF (1e-11, orbital-gradient 1e-7) and strict SCF (1e-12, orbital-gradient 1e-8), retaining the same grid and cavity settings. Compute tight/full, strict/full and strict/off center gradients. Use the finest Richardson derivative; do not select the step that agrees best with a gradient. The uncertainty indicator is the full difference of the two finest strict Richardson estimates, plus the last-two-estimate tight/strict discrepancy, center-gradient precision discrepancy, and the explicitly computed floating-point cancellation allowance. Require indicator <=tau/4 and stabilization of the nested estimates. Changing density-pruned grid counts makes the result inconclusive. Counts are a topology warning, not proof that every retained-grid identity is unchanged.
+
+If absolute discrepancy plus the indicator is <=tau, label the directional result consistent. If discrepancy minus the indicator exceeds tau and the precision/stabilization checks pass, label it inconsistent. Otherwise label it inconclusive. This is an empirical finite-resolution test, not a rigorous interval enclosure. A coarse or noisy reference cannot earn a pass by widening a tolerance. missing_response_material is True only for consistent full response and inconsistent off response, False only when both are consistent at the declared tolerance, and otherwise unknown. Complete diagnostics remain diagnostic_complete regardless of their scientific verdict. At most 82 SCFs and three gradients per case, 7200 seconds per case. A pass authorizes neither the old P30 stage 2 nor any stationary-basin or harmonic-free-energy claim.
+
+P34 is a sampled audit of the frozen 630 primary profiles, not a census certificate. Choose the first 32 keys under SHA256('R7-primary-screen-v1|'+key), then add the eight fixed sentinels water, methanol, nonane, EG, DEG, TEG, glycerol and propylene glycol, counting overlaps once. Freeze the full population profile hashes and the saved geometry bytes before outcomes. On each selected geometry perform one production-SCF SVP calculation and off/full gradient evaluations at the same density. Then compute the unchanged TZVP profile at the center and at plus/minus 0.01 angstrom maximum atomic displacement along the projected negative full-response gradient. Remove rigid motion; use the fixed first R6 probe only if that direction is numerically zero. No minimization is performed. Report the stored-profile versus recomputed-center discrepancy separately, since saved XYZ coordinates may have been rounded.
+
+Use fixed both-role water/methanol/nonane/DME probes at 250, 298.15 and 400 K, complete open-profile overlays, fresh processes and P28. A finite-stress response of >=0.01 in either model is a screen-positive outcome. Coverage differences and absent outputs remain unresolved. Report gradient-response magnitudes separately; a 1e-5 Cartesian component difference is a force indicator, not Berny's internal-coordinate predicate. If a sampling-model upper fraction is reported, it concerns this screen only and is conditional on treating the frozen SHA ordering as uniform sampling. Sentinel evidence is descriptive. No finite-stress sample proves a profile bound over all nearby geometries or locates the corrected minimum. Maximum 40 case-hours on four-core workers; each case has one SVP SCF, two SVP gradients and three TZVP single points. No production relabel or full re-optimization is authorized.
+
+P35 records the glycol mechanism as unresolved under the available inputs. Positive weighting of the supplied sample cannot exceed its relevant tail envelope. That fact does not identify the historical UD geometry, exclude unsampled basins or rule out every electronic/cavity method. No new QC budget is assigned to matching the UD histogram. Reopening requires auditable generating inputs or an independently validated electrostatic/basin calculation on fixed controls. Water and branched polyols remain required counterexamples to any universal OH-only explanation.
+
+All jobs use immutable inputs, isolated output directories, exclusive claims and process-group deadlines. No automatic retry or stale-lock removal is allowed. Independent jobs continue after another member fails; every requested identity retains an outcome. UD-backed gates run on the Mac. Raw data and historical registrations remain unchanged. The total possible native ceiling, if every explicitly conditional stage is authorized, is 147 four-core worker-hours, not an expected duration or a claim of available account quota.
```

