# Z-COSMO optimization audit — ranked, independently testable proposals

**Repository:** `Victor-Liang-ChE/zcosmo`  
**Reference:** `main` = `62172c7e7bb59737d28b115b9ef37311a98bb6cc`, rechecked after the review.  
**Scope:** the complete optimization brief, every source file it names, `PREREGISTRATION.md`, the actual profile validator and fixture, the evaluation entry point, and the 28-window Modal configuration. Source identifiers are collected at the end.

## Decision

**First reduce the cost of a QC geometry step by caching the PCM matrix factorization. In parallel, test replica exchange by free-energy uncertainty per GPU-hour—not by steps per second.** The best demonstrated local evaluator improvement is a support-restricted, safeguarded Newton solver. A second useful evaluator change removes the interior Z0x finite-difference stencil analytically.

There are **eight proposals, eight independent implementation patches, and one shared benchmark patch, H0**. Each implementation diff targets the reference commit, not another proposal. Do not apply all eight sequentially and assume conflicts or interacting numerical effects have been resolved. In particular, P1/P2/P5 share QC code, and P7/P8 share the MACE engine. Test independently first; then merge accepted changes and rerun the same gates.

**What was actually tested here.** I reconstructed seven affected source files and verified their Git blob hashes against the fetched files. All implementation hunks pass `git apply --check` against that snapshot; the prospective-registration hunks match the fetched lines 169–172. Python compilation passes. CPU tests exercised the new segment solver, the analytic derivative identity, LU algebra, the PCM adapter against a mock of its pinned interface, neighbor construction/microbatching against a differentiable mock model, and exchange decisions against full Hamiltonian energy differences. **PySCF, ASE/MACE inference, CUDA, the real 25-molecule profile calculation, and the full scorecard were not run here.** The supplied physical benchmark commands—not the synthetic tests—decide acceptance.

All E labels below mean **equivalence candidates with a mathematical basis**, not completed production acceptance. P4 is deliberately **A for the complete finite-time-step sampler**, even though its exchange move preserves the canonical distribution exactly. P5 is A because an optimizer change can change the basin reached. Neither proposal fits experimental data.

## Ranked table

The brief gives timings but not the allocation of future work. To make the requested ranking reproducible rather than pretending to know that allocation, the score below assumes **60 QC, 38 free-energy, and 2 evaluator hours per 100 hours of upcoming work**. Six of the QC hours are assumed to be restart-related work. The score is `affected_hours × (1 − 1/S) × probability / effort`. Probabilities are subjective engineering priors; effort units measure integration/validation burden, not promised completion time. Savings overlap and must not be added.

| Rank | Patch | Pipeline and mechanism | Class | Speed-up hypothesis used for ranking | Probability / effort units | Score |
|---:|---|---|:---:|---|---|---:|
| 1 | P1 | QC: one PCM LU factorization per geometry | E | **1.6–3×** total QC if repeated PCM solves account for 40–70% of runtime; ranking uses 2× | 0.90 / 2 | 13.50 |
| 2 | P4 | Free energy: within-stage Hamiltonian exchange, joint uncertainty analysis | **A** | **1.5–3× statistical efficiency**, conditional on a measured reduction in integrated variance; ranking uses 2× | 0.60 / 3 | 3.80 |
| 3 | P3 | COSMO-SAC: exact support reduction + safeguarded log-Newton | E | **2–10× segment solve**, conservative 4× evaluator hypothesis | 0.90 / 1 | 1.35 |
| 4 | P5 | QC: TRIC pre-optimization, original Berny final convergence test | **A** | **1.1–1.5×** on difficult geometries; can be slower; ranking uses 1.3× | 0.45 / 5 | 1.25 |
| 5 | P2 | QC: trustworthy restart/output handling and runner scheduling | E | Almost 1× cold arithmetic; **1.3× assumed on restart-affected work**, potentially much higher only when avoiding duplicate completed jobs | 0.90 / 1 | 1.25 |
| 6 | P6 | Z0x: analytic interior dielectric-chain-rule correction | E | **1.8–3× interior evaluations** before P3; no acceleration at infinite-dilution endpoints; ranking uses 1.8× | 0.80 / 2 | 0.36 |
| 7 | P7 | MACE: group neighbor-list construction by graph size/cell | E | **1.02–1.10× MD**, contingent on measured rebuild overhead; ranking uses 1.05× | 0.70 / 4 | 0.32 |
| 8 | P8 | MACE: whole-graph microbatching to bound activation memory | E | **0.6–0.9×** a full batch that already fits; enables otherwise-OOM jobs | 0.95 / 1 | ≤0 on a fitting batch |

P2's convergence guard is a **correctness prerequisite** regardless of its performance rank. H0 applies an equivalent guard to the reference benchmark so an unconverged main-branch geometry cannot become the purported ground truth.

## Acceptance definitions and common setup

For profiles, `p` means the normalized 153-entry distribution `psigmaA / sum(psigmaA)`, including all three blocks. H0 also reports the **raw stored-bin difference in Å²** so the normalization is explicit. Its E gates are identical sigma grids, all 25 molecules, exactly 2,302 historical rows, `max|Δp| < 1e-4`, and `max|Δlnγ∞| < 1e-3`. To avoid weakening the bin criterion through a normalization convention, H0 additionally requires `max_delta_psigmaA_A2 < 1e-4` on the raw stored column. Both bin differences are reported separately.

The existing validator is **not an E-equivalence test**: it compares candidate profiles with UD, permits missing candidates, prints `REJECT` without a failing exit status, and the current candidate list has 26 entries. H0 freezes the historical 25/2,302 manifest from the **key and temperature columns only** of `results/pyscf_profile_validation.csv`, checks coverage, and never reads experimental response values. A fixture mismatch is a failure to resolve, not permission to drop rows. [R2, R16, R17, R18]

Use the same data assets, parameter files, molecular weights/checkpoints, package environment and thread settings for each paired run. Do not rebuild the unpinned Modal environment between the two arms. Record `pip freeze`, the model/checkpoint hash, hardware, and the relevant commit. The report does not launch cloud jobs or spend credits.

### Extract the patches once

Save this report as `ZCOSMO_OPTIMIZATION_REPORT.md`, then run the following from an existing, populated repository. `REPORT` may instead be an absolute path to this report. The extraction reads only fenced diffs marked `PATCH:...`.

```bash
set -euo pipefail
export REPO="$PWD"
export BASE=62172c7e7bb59737d28b115b9ef37311a98bb6cc
export REPORT="${REPORT:-$REPO/ZCOSMO_OPTIMIZATION_REPORT.md}"
export WORK="$(mktemp -d "${TMPDIR:-/tmp}/zcosmo-review.XXXXXX")"
export PATCHES="$WORK/patches"
mkdir -p "$PATCHES"
python - "$REPORT" "$PATCHES" <<'PY'
import pathlib, re, sys
text = pathlib.Path(sys.argv[1]).read_text()
blocks = re.findall(r'<!-- PATCH:(H0|P[1-8]) -->\s*```diff\n(.*?)\n```', text, re.S)
assert len(blocks) == 9 and len({name for name, _ in blocks}) == 9
for name, diff in blocks:
    pathlib.Path(sys.argv[2], name + '.patch').write_text(diff + '\n')
PY
# Worktrees contain pinned code. Shared assets are read-only inputs to these commands.
make_tree () {
    local id="$1" tree="$WORK/$1"
    git -C "$REPO" worktree add --detach "$tree" "$BASE"
    for asset in data results; do
        test -d "$REPO/$asset"
        if test -e "$tree/$asset"; then mv "$tree/$asset" "$tree/$asset.pinned-copy"; fi
        ln -s "$REPO/$asset" "$tree/$asset"
    done
    git -C "$tree" apply --check "$PATCHES/H0.patch"
    git -C "$tree" apply "$PATCHES/H0.patch"
    if test "$id" != base; then
        git -C "$tree" apply --check "$PATCHES/$id.patch"
        git -C "$tree" apply "$PATCHES/$id.patch"
    fi
}
make_tree base
python -m pip freeze > "$WORK/environment.txt"
printf 'WORK=%s\nPATCHES=%s\n' "$WORK" "$PATCHES"
```

The shared `data`/`results` links prevent ignored local assets from silently disappearing in worktrees. **All generated outputs below go under `$WORK`; none of these commands runs the old validator that writes into shared `results`.** Keep those inputs unchanged for the duration of the comparison. These worktrees are experiment copies, not branches to merge wholesale.

For QC use the preregistered PySCF 2.14.0 environment with pyberny, RDKit, tblite, ASE, NumPy, SciPy, pandas and the NIST conversion dependency available. For MACE use the already working environment and checkpoint. `pymbar` and SciPy are required for the new statistical checker. H0 is printed in full in the final appendix.


## 1. P1 — E: cache the CPU PCM factorization, not the answer


**Targets:** `pyscf_cosmo_v2.dft_geometry`, `pyscf_cosmo.cosmo_segments`, and a new `src/zcosmo/pcm_lu.py`.

**Mechanism.** The pinned PySCF 2.14.0 CPU implementation calls `numpy.linalg.solve(K, …)` and `numpy.linalg.solve(K.T, …)` inside every `_get_vind` evaluation. At a fixed geometry the surface matrix does not change with the SCF density. Both calls therefore refactor a matrix that could have been factored once. The patch stores one LU factorization in that geometry's `_intermediates`, checks matrix identity before reuse, and uses forward and transposed triangular solves. A geometry reset or a new `K` invalidates the factorization. [R3, R4, U1]

It deliberately preserves **both** terms:

$$q=K^{-1}Rv,\qquad q_t=R^TK^{-T}v,\qquad q_{sym}=(q+q_t)/2.$$

It preserves `q` separately from `q_sym`, because the profile extractor reads `q`. It does not assume exact matrix symmetry, form an inverse, change cavity radii, change the conductor factor, change an auxiliary basis, or replace the gradient with finite differences. Gradient code and solvent integrals remain upstream code.

**Arithmetic.** If `I` solvent-potential evaluations occur at one geometry, the current factorization work is approximately `2I × (2/3)n_surface³`; the patch performs approximately `(2/3)n_surface³`, plus the same-order `O(I n_surface²)` substitutions. For `I=10`, that is 20 factorizations versus one, **not** a promised 20× QC speed-up. With a factorizable-runtime fraction `f`, use `S_total = 1 / [(1−f)+f/S_component]`. Taking `S_component=20` gives 1.61× at `f=.40` and 2.99× at `f=.70`. Gradient/integral work, surface construction, and Hsieh averaging remain.

**Measured here, only as an algebraic microbenchmark:** for a 768×768 positive-definite test matrix, ten pairs of solves took 0.3006 s with repeated NumPy solves and 0.03964 s with one SciPy LU, or 7.58×. The largest transposed-solve discrepancy in the separate nonsymmetric-right-hand-side check was `1.13e-14`; the mock PCM energy/matrix discrepancy was `1.07e-14`. This is not a PySCF benchmark and must not be transferred to an L4 or a GitHub runner.

**Memory trade-off.** The extra retained factorization is approximately `8 n_surface²` bytes: 200 MB at 5,000 surface points, plus pivots and transient workspace. Check peak resident memory. Do not “extend” this patch into a dense cache of every AO-pair/surface integral: at 600 AOs and 6,000 surface points that tensor alone is `600²×6000×8 = 17.28 GB`.

**Acceptance.** H0's `pcm-check` independently checks water/RKS and O₂/UKS at both production levels, including analytic gradients and charges. The 25-profile test then checks geometry-dependent outputs. Reject an E promotion if it changes a final basin enough to miss the profile/lnγ gates, even though the linear algebra is mathematically equivalent. The version guard intentionally prevents silent use after a PySCF upgrade.


### Unified diff — P1

<!-- PATCH:P1 -->
```diff
--- /dev/null
+++ b/src/zcosmo/pcm_lu.py
@@ -0,0 +1,42 @@
+"""PySCF 2.14.0 PCM: one LU factorization per surface, unchanged equations."""
+import numpy as np
+import pyscf
+from scipy.linalg import lu_factor, lu_solve
+from pyscf.solvent.pcm import PCM
+
+
+class CachedPCM(PCM):
+    def _get_vind(self, dms):
+        if not self._intermediates:
+            self.build()
+        it = self._intermediates
+        K, R = it["K"], it["R"]
+        cached = it.get("_zc_lu")
+        if cached is None or cached[0] is not K:
+            cached = (K, lu_factor(np.array(K, order="F", copy=True),
+                                  overwrite_a=True, check_finite=True))
+            it["_zc_lu"] = cached
+        nao = dms.shape[-1]
+        dms = dms.reshape(-1, nao, nao)
+        if len(dms) == 2:
+            dms = (dms[0] + dms[1]).reshape(-1, nao, nao)
+        v = self.v_grids_n - self._get_v(dms)
+        q = lu_solve(cached[1], R @ v.T, check_finite=True).T
+        vK = lu_solve(cached[1], v.T, trans=1, check_finite=True)
+        qt = (R.T @ vK).T
+        qs = (q + qt) / 2.0
+        vmat = self._get_vmat(qs)
+        it.update(q=q[0], q_sym=qs[0], v_grids=v[0], dm=dms)
+        return 0.5 * np.dot(qs[0], v[0]), vmat[0]
+
+
+def cache_pcm(mf):
+    if pyscf.__version__ != "2.14.0":
+        raise RuntimeError("Revalidate CachedPCM before changing PySCF 2.14.0")
+    old = mf.with_solvent
+    if type(old) is not PCM:
+        raise TypeError("Expected an unmodified CPU PCM object")
+    new = CachedPCM(old.mol)
+    new.__dict__.update(old.__dict__)
+    mf.with_solvent = new
+    return mf
--- a/src/zcosmo/pyscf_cosmo.py
+++ b/src/zcosmo/pyscf_cosmo.py
@@ -49,6 +49,8 @@
     mol = gto.M(atom=[(s, tuple(p)) for s, p in zip(sym, xyz_A)], basis=basis, unit="Angstrom", verbose=0,
                 spin=spin, max_memory=int(os.environ.get("QC_MEM_MB", "4000")))
     mf = (dft.UKS(mol) if spin else dft.RKS(mol)).density_fit().PCM()
+    from zcosmo.pcm_lu import cache_pcm
+    mf = cache_pcm(mf)
     mf.xc = "b88,p86"
     mf.grids.level = 3
     mf.conv_tol = 1e-9
--- a/src/zcosmo/pyscf_cosmo_v2.py
+++ b/src/zcosmo/pyscf_cosmo_v2.py
@@ -29,6 +29,8 @@
     mol = gto.M(atom=[(s, tuple(p)) for s, p in zip(sym, xyz_A)], basis=basis, unit="Angstrom", verbose=0,
                 spin=spin, max_memory=int(os.environ.get("QC_MEM_MB", "3000")))
     mf = (dft.UKS(mol) if spin else dft.RKS(mol)).density_fit().PCM()
+    from zcosmo.pcm_lu import cache_pcm
+    mf = cache_pcm(mf)
     mf.xc = "b88,p86"
     mf.grids.level = 2
     mf.conv_tol = 1e-8
```

### Apply, benchmark and check

Run in the setup shell. Generate the reference profiles once, before changing the shared environment. A pre-existing output directory must not be reused as a timing benchmark.

```bash
make_tree P1
(
  cd "$WORK/P1"
  export PYTHONPATH=src OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4 QC_MEM_MB=10000
  python scripts/optimization_check.py pcm-check --out "$WORK/P1-fixed-geometry.json"
)
(
  cd "$WORK/base"
  export PYTHONPATH=src OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4 QC_MEM_MB=10000
  python scripts/optimization_check.py qc --out "$WORK/qc-base"
)
(
  cd "$WORK/P1"
  export PYTHONPATH=src OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4 QC_MEM_MB=10000
  python scripts/optimization_check.py qc --out "$WORK/qc-P1"
  python scripts/optimization_check.py profiles --mode E \
    --reference "$WORK/qc-base" --candidate "$WORK/qc-P1" --out "$WORK/P1-profile-check.json"
)
```

Compare `timing.json` and the recorded geometry evaluations, not merely the final single-point duration. Repeat the fixed-geometry timing in fresh processes with 1, 2 and 4 threads before choosing runner thread settings; fewer geometry cycles and cheaper cycles are different effects.

## 2. P4 — A: exchange Hamiltonians without claiming the finite-step sampler is exact


**Target:** `cloud/s15/bench15_core.py`: `stage_D2`, new `exchange_pairs`, and covariance-preserving TI error diagnostics. The patch also adds a prospective entry to `PREREGISTRATION.md`; it does not backdate the existing pilot.

**Mechanism.** Exchange adjacent λ windows within stage 2 and adjacent μ windows within stage 1, on alternating odd/even sweeps every 100 steps. Both stages already have the information needed to evaluate swap probabilities without another cross-Hamiltonian MACE evaluation. Swap **the entire physical configuration and its velocities**, keep Hamiltonian slots fixed, and recompute forces before the next integration step. Do not just permute the old forces. Keep the molecular species, masses, box and temperature identical across each exchange group. No swap crosses the stage boundary. [R10, R11, R19]

For stage 2 write `H_i(q)=H_0(q)+λ_i D(q)`, where `D=E_full−E_solvent−E_solute−U_WCA`. The accepted-swap log ratio is

$$\log a_{ij}=\beta(\lambda_j-\lambda_i)[D(q_j)-D(q_i)].$$

For stage 1, with `U[row configuration, column μ state]`, it is

$$\log a_{ij}=-\beta[U(q_j,\mu_i)+U(q_i,\mu_j)-U(q_i,\mu_i)-U(q_j,\mu_j)].$$

These signs were checked against full Hamiltonian energy differences for 200 CPU test configurations. The acceptance decisions and window permutations passed. This is not an MD sampling benchmark.

**Why A rather than E for the runner.** The Metropolis swap preserves the product canonical distribution. But the existing un-Metropolized BAOAB integrator at finite `dt` is not itself an exact canonical kernel. Composing it with canonical swaps can change its discretization-biased stationary distribution. “The swap obeys detailed balance” is not a proof that the complete discrete-time runner is equivalent to main. The patch therefore provides `ZC_DT_FS=.25` as well as the original `.5` and holds the recording interval at 10 fs. The A acceptance gate includes a time-step-halving comparison. No Hamiltonian parameter is being fitted or altered.

**Arithmetic.** At one exchange sweep per 100 ordinary steps, refreshing forces adds about 1% to MACE call count. It also forces more neighbor rebuilds and incurs coordinate/WCA/RNG work: budget roughly 2–8% overhead until measured. If the relevant integrated autocorrelation time falls from 2.5 ps to 1.0 ps with 4% overhead and unchanged observable variance, the gain is `2.5/(1.0×1.04)=2.40×` effective samples per wall time. There is no guaranteed gain: poor overlap or a slow mode orthogonal to λ can make exchange ineffective.

**Measure the right quantity.** For fixed precision, compare `Var(estimated ΔG) × total_wall_time`, not just `ESS`, swap acceptance, or the slowest individual window. With exchange, time-lagged cross-window covariance matters. Form the simultaneous TI time series `Y_t = Σ wλ Dλ,t + Σ wμ Dμ,t` and estimate its uncertainty in time blocks. The patch changes the printed five-block diagnostic to use this joint series, while H0 uses equilibration detection, blocks tied to estimated statistical inefficiency, and independent run replicates. Five blocks alone remain insufficient evidence. [U4]

**Acceptance.** Require the unchanged fixed-frame force gate, the same recorded model/checkpoint and environment, adequate stationary blocks, and a 90% confidence interval for the free-energy difference contained within ±0.10 kcal/mol. Apply that equivalence criterion both to no-exchange versus exchange and to `.5` versus `.25` fs. An underpowered comparison is **INCONCLUSIVE**, not accepted because a difference is nonsignificant. The ±0.10 criterion is a proposed, prospective sampler criterion; it is not an existing repo claim. H0 reports a pilot efficiency estimate, not a confidence-certified speed-up.


### Unified diff — P4

<!-- PATCH:P4 -->
```diff
--- a/cloud/s15/bench15_core.py
+++ b/cloud/s15/bench15_core.py
@@ -1,7 +1,7 @@
 """bench12 (L4): (A2) exact multi-system batching throughput; (D2) two-stage cavity TI for decoupling one water
 from 63 waters with MACE-OFF23 small, all lambda windows batched into ONE MACE graph per step.
 
-D2 path (registered before running, PREREGISTRATION.md 2026-09-26):
+D2 exploratory path (earlier registration not found; see prospective optimization audit P4):
   stage 1 (decoupled solute): grow a purely repulsive soft-core WCA cavity between solute and solvent atoms,
       U1(mu) = U_MACE(solvent) + U_MACE(solute) + U_scWCA(mu)
   stage 2: U2(l) = l U_MACE(full) + (1 - l) [U_MACE(solvent) + U_MACE(solute) + U_WCA]
@@ -20,6 +20,10 @@
 
 CONV = 9.648533212e-3; KB = 8.617333e-5; T = 298.15; KT = KB * T; EV2KCAL = 23.0605
 EPS = 1.0 / EV2KCAL; ALPHA = 0.5
+DT = float(os.environ.get("ZC_DT_FS", "0.5"))
+if DT not in (0.25, 0.5):
+    raise ValueError("validated comparison supports dt = 0.25 or 0.5 fs")
+STRIDE = int(round(10.0 / DT))
 PROD = int(os.environ.get("ZC_PROD_STEPS", "16000")); EQ = int(os.environ.get("ZC_EQ_STEPS", "2000"))
 out = []
 DEV = "cuda" if torch.cuda.is_available() else "cpu"
@@ -111,6 +115,39 @@
     return box, len(molecule(MOLS[solute]))
 
 
+def exchange_pairs(lam, du, cavity, parity, generator):
+    """Return a permutation of physical window slots; no swap crosses the two stages."""
+    w2, w1 = len(lam), cavity.shape[0]
+    perm = torch.arange(w2 + w1, device=du.device)
+    accepted = torch.zeros(2, device=du.device, dtype=torch.long)
+    attempted = torch.zeros_like(accepted)
+    for stage, count, offset in ((0, w2, 0), (1, w1, w2)):
+        i = torch.arange(parity, count - 1, 2, device=du.device)
+        j = i + 1
+        if stage == 0:
+            loga = (lam[j].double() - lam[i].double()) * (du[j].double() - du[i].double()) / KT
+        else:
+            u = cavity.double()  # row=config, column=state
+            loga = -(u[j, i] + u[i, j] - u[i, i] - u[j, j]) / KT
+        uniform = torch.rand(i.shape, device=du.device, generator=generator, dtype=torch.float64)
+        ok = torch.isfinite(loga) & (torch.log(uniform) < torch.minimum(loga, torch.zeros_like(loga)))
+        # Fixed-shape assignments, even when no pair is accepted.
+        perm[i + offset] = torch.where(ok, j, i) + offset
+        perm[j + offset] = torch.where(ok, i, j) + offset
+        accepted[stage] = ok.sum()
+        attempted[stage] = i.numel()
+    return perm, accepted, attempted
+
+
+def ti_weights(grid):
+    grid = np.asarray(grid, float)
+    if len(grid) < 2 or grid[0] != 0 or grid[-1] != 1 or not (np.diff(grid) > 0).all():
+        raise ValueError("TI grid must strictly increase from zero to one")
+    w = np.zeros(len(grid)); dx = np.diff(grid)
+    w[:-1] += dx / 2; w[1:] += dx / 2
+    return w
+
+
 def stage_D2():
     c = teacher(); name = os.environ.get("ZC_SOLUTE", "water"); solvent = os.environ.get("ZC_SOLVENT", "water")
     seed = int(os.environ.get("ZC_SEED", "1"))
@@ -125,15 +162,23 @@
     if os.environ.get("ZC_MU1"): mu1 = [float(v) for v in os.environ["ZC_MU1"].split(",")]
     if os.environ.get("ZC_TEST"): lam2, mu1 = [0.0, 0.5, 1.0], [0.0, 1.0]
     W2, W1 = len(lam2), len(mu1); W = W2 + W1
+    ti_weights(lam2); ti_weights(mu1)
+    exchange_every = int(os.environ.get("ZC_EXCHANGE_EVERY", "0"))
+    if exchange_every < 0:
+        raise ValueError("ZC_EXCHANGE_EVERY must be nonnegative")
+    accepted = torch.zeros(2, device=DEV, dtype=torch.long)
+    attempted = torch.zeros_like(accepted)
+    walkers = torch.arange(W, device=DEV)
+    walker_history = []
     # equilibrate one coupled box, then start every window from it
     one = MultiMACE(c, [at], skin=0.9); m1 = torch.tensor(at.get_masses(), dtype=torch.float32, device=DEV)[:, None]
     g = torch.Generator(device=DEV).manual_seed(7 + 1000 * seed)
     x = torch.tensor(at.positions, dtype=torch.float32, device=DEV); v = torch.randn(x.shape, device=DEV, generator=g) * torch.sqrt(KT / m1 * CONV)
-    c1 = math.exp(-0.01 * 0.5); _, F = one.forces(x)
+    c1 = math.exp(-0.01 * DT); _, F = one.forces(x)
     for s in range(PRE):
-        v += 0.25 * F / m1 * CONV; x += 0.25 * v
+        v += (0.5 * DT) * F / m1 * CONV; x += (0.5 * DT) * v
         v = c1 * v + math.sqrt(1 - c1 * c1) * torch.sqrt(KT / m1 * CONV) * torch.randn(x.shape, device=DEV, generator=g)
-        x += 0.25 * v; _, F = one.forces(x); v += 0.25 * F / m1 * CONV
+        x += (0.5 * DT) * v; _, F = one.forces(x); v += (0.5 * DT) * F / m1 * CONV
     # graphs: per stage-2 window [full, solvent, solute]; per stage-1 window [solvent, solute]
     systems, idx, wnode = [], [], []
     for w in range(W):
@@ -169,13 +214,25 @@
 
     t0 = time.time(); F, du2, xs, xv = force(); rec2, rec1, rec1d = [], [], []
     for s in range(EQ + PROD):
-        V += 0.25 * F / m * CONV; X += 0.25 * V
+        V += (0.5 * DT) * F / m * CONV; X += (0.5 * DT) * V
         V = c1 * V + math.sqrt(1 - c1 * c1) * torch.sqrt(KT / m * CONV) * torch.randn(X.shape, device=DEV, generator=g)
-        X += 0.25 * V; F, du2, xs, xv = force(); V += 0.25 * F / m * CONV
+        X += (0.5 * DT) * V; F, du2, xs, xv = force(); V += (0.5 * DT) * F / m * CONV
+        if exchange_every and (s + 1) % exchange_every == 0:
+            with torch.no_grad():
+                cavity = wca(xs[W2:], xv[W2:], L, sig, mu_all)
+                parity = ((s + 1) // exchange_every - 1) % 2
+                perm, ac, tr = exchange_pairs(lamt, du2, cavity, parity, g)
+                X.copy_(X.view(W, n, 3)[perm].reshape_as(X))
+                V.copy_(V.view(W, n, 3)[perm].reshape_as(V))
+                walkers = walkers[perm]
+                accepted += ac; attempted += tr
+            # Forces belong to Hamiltonian slots, not to walkers: old F cannot be permuted.
+            F, du2, xs, xv = force()
         if not torch.isfinite(F).all():
             log(f"D2 non-finite forces at step {s}"); return
-        if s >= EQ and s % 20 == 0:
+        if s >= EQ and (s - EQ) % STRIDE == 0:
             rec2.append(du2.cpu().numpy())
+            walker_history.append(walkers.cpu().numpy())
             with torch.no_grad():
                 u_all = wca(xs[W2:], xv[W2:], L, sig, mu_all)             # (W1, K1) U_wca of each stage-1 sample at every mu
                 mu_g = mut.clone().requires_grad_(True)
@@ -186,7 +243,10 @@
             log(f"D2 speed: {(time.time()-t0)/(s+1)*1000:.1f} ms/step for all {W} windows (rebuilds {mm.n_rebuild})")
     wall = time.time() - t0
     rec2, rec1, rec1d = np.array(rec2), np.array(rec1), np.array(rec1d)      # (S,W2), (S,W1,K1), (S,W1)
-    np.savez(f"/tmp/d2_{name}_in_{solvent}_s{seed}.npz", lam2=lam2, mu1=mu1, rec2=rec2, rec1=rec1, rec1d=rec1d)
+    np.savez(f"/tmp/d2_{name}_in_{solvent}_s{seed}.npz", lam2=lam2, mu1=mu1, rec2=rec2, rec1=rec1, rec1d=rec1d,
+             wall_s=wall, dt_fs=DT, sample_fs=10.0, exchange_every=exchange_every, walkers=np.asarray(walker_history),
+             accepted=accepted.cpu().numpy(), attempted=attempted.cpu().numpy())
+    log(f"D2 exchange accepted/attempted by stage: {accepted.tolist()} / {attempted.tolist()}")
     json.dump({"lam2": lam2, "mu1": mu1}, open("/tmp/d2.json", "w"))
     bet = 1 / KT; S = rec2.shape[0]
     # TI
@@ -196,6 +256,10 @@
         w = np.zeros(len(xk)); dx = np.diff(xk); w[:-1] += dx / 2; w[1:] += dx / 2
         return float(w @ yk), float(np.sqrt((w ** 2) @ sk ** 2))
     g2, e2 = trap(lam2, m2, se2); g1, e1 = trap(mu1, m1d, se1)
+    y2, y1 = rec2 @ ti_weights(lam2), rec1d @ ti_weights(mu1)
+    e2, e1 = block_se(y2), block_se(y1)
+    joint_se = block_se(y2 + y1)  # Preserve cross-window and cross-lag covariance.
+    # These five-block errors remain feasibility diagnostics, not an acceptance certificate.
     for k in range(W2): log(f"D2 stage2 l={lam2[k]:.2f}: <dU/dl> {m2[k]:+.4f} eV (se {se2[k]:.4f}, sd {rec2[:, k].std():.4f})")
     for k in range(W1): log(f"D2 stage1 mu={mu1[k]:.2f}: <dU/dmu> {m1d[k]:+.4f} eV (se {se1[k]:.4f})")
     # MBAR (reduced potentials differ only by the lambda- or mu-dependent parts)
@@ -208,7 +272,7 @@
     log(f"D2 stage1 (cavity growth, decoupled): TI {g1*EV2KCAL:+.3f} +- {e1*EV2KCAL:.3f}, MBAR {G1m:+.3f} kcal/mol; min neighbour overlap {ov1:.3f}")
     log(f"D2 stage2 (cavity -> full MACE):      TI {g2*EV2KCAL:+.3f} +- {e2*EV2KCAL:.3f}, MBAR {G2m:+.3f} kcal/mol; min neighbour overlap {ov2:.3f}")
     log(f"D2 coupling free energy of {name} in MACE-OFF23-small {solvent} (298 K, {S} samples/window x 10 fs, "
-        f"{(EQ+PROD)*0.5/1000:.1f} ps/window, wall {wall/60:.0f} min): TI {(g1+g2)*EV2KCAL:+.3f} +- {math.hypot(e1,e2)*EV2KCAL:.3f}, "
+        f"{(EQ+PROD)*DT/1000:.1f} ps/window, wall {wall/60:.0f} min): TI {(g1+g2)*EV2KCAL:+.3f} +- {joint_se*EV2KCAL:.3f}, "
         f"MBAR {G1m+G2m:+.3f} kcal/mol  [feasibility only]")
 
 
--- a/PREREGISTRATION.md
+++ b/PREREGISTRATION.md
@@ -169,4 +169,19 @@
   the v1 test unchanged: >= 20 molecules with UD profiles, median |d ln gamma_inf| (COSMO-SAC-dsp) over
   their benchmark IDAC rows < 0.15. If accepted, an all-open-profile version of Z0x (Z0x-open) is scored
   as a secondary table; if not, v2 profiles are used only for gap compounds, as v1.
+- Optimization audit P4 (effective only when this prospective entry is committed): the previously
+  computed D2 pilot is exploratory, not retroactively preregistered. For a new sampler comparison use
+  the existing two-stage soft-core WCA/MACE Hamiltonians without changing endpoints, weights,
+  masses, temperature, density or WCA parameters. The main comparison uses the same 0.5 fs time step. Use the 15 lambda / 13 mu grids from
+  cloud/s15/modal_bench15.py. Compare exchange disabled against odd/even adjacent within-stage
+  Hamiltonian exchanges every 100 steps, swapping coordinates and velocities and refreshing forces.
+  Use independent seeds 11--14 for reference and 31--34 for exchange, 20000 equilibration steps and
+  60000 production steps initially. Evaluate covariance-preserving block uncertainties and total
+  wall cost, not acceptance rate alone. A 90% interval for the free-energy difference must lie within
+  +/-0.10 kcal/mol; insufficient precision is inconclusive. Extend both arms identically in length
+  before considering a new protocol. No experimental activities, energies, or densities enter selection.
+  This is an A sampler candidate: canonical exchange is exact, but finite-step BAOAB is not an exact
+  canonical kernel. Also compare exchange at 0.25 fs with seeds 51--54, doubling equilibration,
+  production and pre-equilibration steps and using exchanges every 200 steps to hold physical times
+  fixed. Require the same +/-0.10 kcal/mol equivalence gate; otherwise do not accept this sampler.
 - Z0w2 check on water (before scoring): electrostatic desolvation of the water dimer rises smoothly from
```

### Apply, benchmark and check

Commit the prospective protocol before running either statistical comparison. This records a new experiment; it does not retroactively validate the old D2 runs.

```bash
make_tree P4
(
  cd "$WORK/P4"
  git add PREREGISTRATION.md cloud/s15/bench15_core.py scripts/optimization_check.py
  git commit -m "Preregister P4 exchange and time-step equivalence experiment"
  git rev-parse HEAD > "$WORK/P4-registration-commit.txt"
  PYTHONPATH=src python scripts/optimization_check.py mace \
    --reference "$WORK/base" --out "$WORK/P4-force-check.json"
)
# Four independent reference runs; same 28-window grid, 10 ps equilibration, 30 ps production.
for seed in 11 12 13 14; do
  (cd "$WORK/base"; PYTHONPATH=src python scripts/optimization_check.py fe-run \
    --seed "$seed" --exchange 0 --out "$WORK/fe-base-$seed")
done
for seed in 31 32 33 34; do
  (cd "$WORK/P4"; PYTHONPATH=src python scripts/optimization_check.py fe-run \
    --seed "$seed" --exchange 100 --out "$WORK/fe-P4-$seed")
done
# Hold all physical durations and the 50 fs exchange interval fixed when halving dt.
for seed in 51 52 53 54; do
  (cd "$WORK/P4"; PYTHONPATH=src python scripts/optimization_check.py fe-run \
    --seed "$seed" --dt .25 --eq 40000 --prod 120000 --exchange 200 \
    --out "$WORK/fe-P4-halfdt-$seed")
done
(cd "$WORK/P4"; PYTHONPATH=src python scripts/optimization_check.py fe-check \
  --reference "$WORK"/fe-base-{11,12,13,14}/samples.npz \
  --candidate "$WORK"/fe-P4-{31,32,33,34}/samples.npz --out "$WORK/P4-equivalence.json")
(cd "$WORK/P4"; PYTHONPATH=src python scripts/optimization_check.py fe-check \
  --reference "$WORK"/fe-P4-{31,32,33,34}/samples.npz \
  --candidate "$WORK"/fe-P4-halfdt-{51,52,53,54}/samples.npz --out "$WORK/P4-dt-check.json")
```

The commands above use water in water. Repeat the accepted protocol with `--solute methanol --solvent water` and the other cross/self combinations before generalizing the gain. Run seeds sequentially on one GPU; do not launch all arrays concurrently on a free-tier device. Exit 2 means insufficient statistical evidence. A 30 ps pilot may well be too short for the ±0.10 gate; the preregistration permits symmetric length extension, not threshold relaxation.

## 3. P3 — E: exact active support with safeguarded Newton acceleration


**Target:** `src/zcosmo/cosmosac.py::solve_gamma`.

**Mechanism.** Let `S={j:p_j>0}`. Only columns in `S` contribute to the segment equations. Solve the active equations, then reconstruct **all 153 values**, including inactive bins:

$$\Gamma_i=\left[\sum_{j\in S}E_{ij}p_j\Gamma_j\right]^{-1}.$$

An inactive solvent bin may still be sampled by the infinitely dilute solute. Returning ones or zeros there is wrong. The patch never removes a small positive bin and does not change the grid. Every eighth damped update it tries a Newton step in `y=ln Γ`, with residual backtracking and the old damped update as fallback. [R6]

With `A_ij=E_ij p_j` on the active support,

$$r_i(y)=y_i+\log\sum_j A_{ij}e^{y_j},\qquad
J_{ij}=\delta_{ij}+\frac{A_{ij}e^{y_j}}{\sum_k A_{ik}e^{y_k}}.$$

The exponentiated update stays positive. The Newton step is capped and accepted only if the log-equation residual decreases. The final returned vector must satisfy the **complete** fixed-point residual below `2e-10`; an iteration-limit failure raises instead of silently returning an unconverged vector.

**Exactness argument.** Support reduction is algebraic elimination of terms with exactly zero weight. Newton and successive substitution solve the same equations. For strictly positive symmetric `E` and positive active probabilities, the potential

$$\Phi(y)=\tfrac12\sum_{ij}p_i p_j E_{ij}e^{y_i+y_j}-\sum_i p_i y_i$$

is strictly convex and coercive; its stationary point gives the unique positive solution. This argument must not be invoked after floating-point underflow has destroyed strict positivity. The residual and output comparisons still apply; overflow/underflow cases need a separate log-domain treatment, not an unsupported universal-convergence claim.

**Arithmetic and measured CPU test.** At 24 active bins the matrix-vector product shrinks from `153²=23,409` entries to `24²=576`, a 40.6× reduction in that operation. That alone is not a useful whole-solver prediction: the first implementation I tested was slower because extra per-iteration validation dominated these tiny matrix operations. In the final hybrid, the representative 298.15 K, 24-bin synthetic case fell from **453 damped iterations to 25 outer iterations**, taking **7.60 ms → 0.740 ms, or 10.27×**. Corresponding 48-bin and 153-bin cases gave 10.53× and 2.93×. The tests use valid synthetic normalized profiles and the repository's actual interaction-energy formula, not the experimental benchmark distribution.

Across 18 tested profiles/temperatures, `max|Δln Γ| = 1.05e-8` against main and the maximum new full residual was `9.95e-11`. The forward difference can exceed `1e-10` because the old step-based convergence criterion is not a condition-number-independent forward-error bound. None of this substitutes for `Δlnγ∞ < 1e-3` on the real 2,302 rows.

**Expected application gain:** 2–10× in segment solves, with lower whole-scorecard gain. If 80% of runtime is accelerated 5×, Amdahl gives `1/(.2+.8/5)=2.78×`, not 5×. Compare cold processes as well as warmed caches; a synthetic matrix-vector ratio is not a scoring-pass speed-up.


### Unified diff — P3

<!-- PATCH:P3 -->
```diff
--- a/src/zcosmo/cosmosac.py
+++ b/src/zcosmo/cosmosac.py
@@ -116,16 +116,47 @@
     E = exp(-DeltaW/RT). Only segments with nonzero probability matter for the
     sums; others still get a value from the same fixed-point expression.
     """
-    AA = E * ps[None, :]
-    G = np.ones(153)
-    for _ in range(max_iter):
+    from scipy.linalg import solve
+    ps = np.asarray(ps, dtype=float)
+    if (E.shape != (ps.size, ps.size) or not np.isfinite(ps).all()
+            or (ps < 0).any() or not np.isfinite(E).all() or (E < 0).any()):
+        raise ValueError("invalid segment kernel or profile")
+    active = np.flatnonzero(ps > 0)  # Never threshold small positive bins.
+    if not active.size:
+        raise ValueError("empty segment profile")
+    columns = E[:, active] * ps[active][None, :]
+    AA = np.ascontiguousarray(columns[active])
+    G = np.ones(active.size)
+    eye = np.eye(active.size)
+    for iteration in range(max_iter):
         Gn = 1.0 / (AA @ G)
         Gm = 0.5 * (G + Gn)
         if np.max(np.abs((Gm - Gn) / Gm)) < tol:
-            G = Gm
-            break
+            full = 1.0 / (columns @ Gm)
+            residual = full * (columns @ full[active]) - 1.0
+            if np.isfinite(full).all() and np.max(np.abs(residual)) < 2 * tol:
+                return full
         G = Gm
-    return G
+        if iteration % 8 == 7:
+            # Newton in log(G), with residual backtracking. Failed trials retain the
+            # original damped iterate; no extrapolated or thresholded profile is used.
+            den = AA @ G
+            residual = np.log(G) + np.log(den)
+            norm = np.max(np.abs(residual))
+            try:
+                J = eye + (AA * G[None, :]) / den[:, None]
+                step = solve(J, -residual, check_finite=True)
+            except (ValueError, np.linalg.LinAlgError):
+                continue
+            step /= max(1.0, np.max(np.abs(step)) / 4.0)
+            for scale in (1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125):
+                trial = G * np.exp(scale * step)
+                nr = np.log(trial) + np.log(AA @ trial)
+                if np.isfinite(nr).all() and np.max(np.abs(nr)) < norm * (1 - 1e-4 * scale):
+                    G = trial
+                    break
+    raise RuntimeError(f"segment equations not converged after {max_iter} iterations")
+
 
 
 @lru_cache(maxsize=4096)
```

### Apply, benchmark and check

The snapshot includes all 2,302 registered COSMO-SAC queries, Z0x coverage, and a fixed composition/temperature grid. It compares predictions only, not experimental errors.

```bash
make_tree P3
(cd "$WORK/base"; PYTHONPATH=src OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python scripts/optimization_check.py snapshot --grid --out "$WORK/models-base.npz")
(cd "$WORK/P3"; PYTHONPATH=src OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python scripts/optimization_check.py snapshot --grid --out "$WORK/models-P3.npz")
(cd "$WORK/P3"; PYTHONPATH=src python scripts/optimization_check.py compare \
  --reference "$WORK/models-base.npz" --candidate "$WORK/models-P3.npz" \
  --out "$WORK/P3-model-check.json")
```

Run three fresh-process repetitions before quoting timing. Any changed finite/missing coverage fails. This is a representative evaluator benchmark, not certification of every LLE binodal; the whole-scorecard regression requirements are stated below.

## 4. P5 — A: TRIC preconditioning followed by the original Berny stopping test


**Target:** `src/zcosmo/pyscf_cosmo_v2.py::dft_geometry`, plus a prospective registration entry.

**Mechanism.** Keep the xTB start and the same BP86/def2-SVP conductor Hamiltonian. Optionally run geomeTRIC/TRIC for at most 60 optimizer steps, then pass its geometry/scanner into the original Berny kernel and require Berny's original convergence test to succeed. Keep the final TZVP calculation and profile conversion untouched. The switch is `ZC_TRIC_PREOPT=1`; the default remains Berny. [R3, U2, U3]

This intentionally does **not** claim that geomeTRIC's defaults equal Berny's defaults. Their displacement coordinates/units and several thresholds differ. TRIC supplies a different coordinate representation and optimization history; Berny supplies the final registered stopping criterion. The existing PySCF scanner already reuses a density guess between geometry steps, so this proposal is not charging a second time for an optimization that main already performs.

**Why A.** Equal functional/basis/solvent and an equal final stopping test do not ensure the same minimum. A flexible chain can reach another conformer. The output is therefore an A candidate until prospectively accepted, not an automatic E promotion. A partly completed TRIC pre-stage is allowed to continue into Berny, but an unconverged final Berny stage is not allowed to produce a profile.

**Arithmetic.** Suppose a hard case needs 90 expensive evaluations with Berny, versus 45 TRIC evaluations plus 15 Berny-polish evaluations at comparable cost. The geometry-stage gain is `90/(45+15)=1.50×`. If geometry is 90% of total time, that is `1/(.1+.9/1.5)=1.43×` overall. A 60-step TRIC stage followed by another 90 Berny evaluations is a loss. These counts are scenarios, not measurements. TRIC is especially motivated by coordinate-conditioning problems; its treatment of multiple fragments is not a guarantee for one covalently connected alkyl chain.

**Acceptance.** Commit the protocol first, keep all 25 molecules, require final Berny convergence and the existing median `|Δlnγ∞| versus UD < .15`. Report failures, final energies and changed conformers. Do not select whichever conformer agrees best with experiment, remove the hard molecules, relax the criterion, or relabel a failed A test as E. Even acceptance grants only the secondary open-profile role already described in the preregistration, not permission to replace the main scorecard.

**Not included:** a blindly supplied xTB Hessian. In the pinned PySCF geomeTRIC adapter, the `hessian='file:…'` route can compute/write the method's own Hessian; it is not safe to assume that this consumes an existing xTB Hessian without expensive DFT work. A cheap Hessian needs an audited interface, consistent units/projection and a separate controlled test. The ordinary minimization patch below requests no exact Hessian. [U2]


### Unified diff — P5

<!-- PATCH:P5 -->
```diff
--- a/src/zcosmo/pyscf_cosmo_v2.py
+++ b/src/zcosmo/pyscf_cosmo_v2.py
@@ -25,7 +25,7 @@
     convergence criteria; only the Berny Hessian guess restarts)."""
     from pyscf import gto, dft
     from pyscf.data import elements
-    from pyscf.geomopt.berny_solver import optimize
+    from pyscf.geomopt.berny_solver import kernel
     mol = gto.M(atom=[(s, tuple(p)) for s, p in zip(sym, xyz_A)], basis=basis, unit="Angstrom", verbose=0,
                 spin=spin, max_memory=int(os.environ.get("QC_MEM_MB", "3000")))
     mf = (dft.UKS(mol) if spin else dft.RKS(mol)).density_fit().PCM()
@@ -45,9 +45,22 @@
             tmp = str(partial) + ".tmp"
             with open(tmp, "w") as f:
                 json.dump({"sym": list(sym), "x": np.round(env["mol"].atom_coords(unit="Angstrom"), 6).tolist(),
-                           "cycle": int(env.get("cycle", -1))}, f)
+                           "cycle": int(env.get("cycle", getattr(env.get("self"), "cycle", -1)))}, f)
             os.replace(tmp, partial)
-    m2 = optimize(mf, maxsteps=maxsteps, callback=cb)
+    if os.environ.get("ZC_TRIC_PREOPT", "0") == "1":
+        from pyscf.geomopt.geometric_solver import kernel as tric_kernel
+        # A preconditioner only; the original Berny kernel supplies the final convergence test.
+        scanner = mf.nuc_grad_method().as_scanner()
+        _, pre = tric_kernel(scanner, maxsteps=60, coordsys="tric", callback=cb,
+                             convergence_energy=1e-6, convergence_grms=3e-4,
+                             convergence_gmax=4.5e-4, convergence_drms=1.2e-3,
+                             convergence_dmax=1.8e-3)
+        scanner.reset(pre)
+        converged, m2 = kernel(scanner, maxsteps=maxsteps, callback=cb)
+    else:
+        converged, m2 = kernel(mf, maxsteps=maxsteps, callback=cb)
+    if not converged:
+        raise RuntimeError("Final Berny geometry has not converged; do not produce a profile")
     return np.asarray(m2.atom_coords(unit="Angstrom"))
 
 
@@ -74,6 +87,7 @@
         seg, e = cosmo_segments(sym, x, spin=spin)
         out, meta = to_profiles(sym, x, seg)
         meta["E_scf_Eh"] = e
+        meta["tric_preopt"] = os.environ.get("ZC_TRIC_PREOPT", "0") == "1"
         meta["geometry"] = "BP86/def2-SVP C-PCM conductor (pyberny)" + (" [resumed from checkpoint]" if resumed else "")
         write_sigma(dest, out, meta, key)
         with open(Path(outdir) / f"{key}.xyz.json", "w") as f:
--- a/PREREGISTRATION.md
+++ b/PREREGISTRATION.md
@@ -169,4 +169,15 @@
   the v1 test unchanged: >= 20 molecules with UD profiles, median |d ln gamma_inf| (COSMO-SAC-dsp) over
   their benchmark IDAC rows < 0.15. If accepted, an all-open-profile version of Z0x (Z0x-open) is scored
   as a secondary table; if not, v2 profiles are used only for gap compounds, as v1.
+- Optimization audit P5 (effective only when this prospective entry is committed): test a geomeTRIC
+  TRIC pre-optimization capped at 60 optimizer steps at the unchanged BP86/def2-SVP conductor
+  level, followed by the original pyberny kernel with its original convergence settings and 100-step
+  cap. Keep the xTB start, final BP86/def2-TZVP calculation, grids, radii, spin treatment and profile
+  conversion unchanged. This is an A candidate because a different optimizer can select a different
+  basin. Freeze the historical 25-molecule/2302-row manifest using only key and T from
+  results/pyscf_profile_validation.csv. Require all 25 profiles, final Berny convergence, and the
+  existing median |d ln gamma_inf| versus UD < 0.15. Publish failures and changed basins; do not
+  select starts, optimizer settings, or molecules using experimental responses. Passing this test
+  authorizes only the secondary open-profile role already specified above, not replacement of the
+  preregistered main scorecard. Record package versions and the commit of this entry before running.
 - Z0w2 check on water (before scoring): electrostatic desolvation of the water dimer rises smoothly from
```

### Apply, benchmark and check

Install/lock geomeTRIC 1.1 in the QC environment **before both reference and candidate runs**, retaining PySCF 2.14.0 and the same NumPy/SciPy versions. If installing it changes shared dependencies, regenerate the reference.

```bash
make_tree P5
(
  cd "$WORK/P5"
  git add PREREGISTRATION.md src/zcosmo/pyscf_cosmo_v2.py scripts/optimization_check.py
  git commit -m "Preregister P5 TRIC pre-stage with Berny final convergence"
  git rev-parse HEAD > "$WORK/P5-registration-commit.txt"
  export PYTHONPATH=src OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4 QC_MEM_MB=10000
  ZC_TRIC_PREOPT=1 python scripts/optimization_check.py qc --out "$WORK/qc-P5"
  python scripts/optimization_check.py profiles --mode A \
    --reference "$WORK/qc-base" --candidate "$WORK/qc-P5" --out "$WORK/P5-accuracy-check.json"
)
```

Use the reference generated in P1 only when its package/data environment is unchanged. The trace distinguishes TRIC from Berny evaluations. A speed comparison must include the pre-stage, polish and failures; do not report only the shortened final Berny portion.

## 5. P2 — E: stop accepting incomplete work and make restarts useful


**Targets:** `pyscf_cosmo_v2.dft_geometry/run_one/main`, `pyscf_cosmo.write_sigma`, and `.github/workflows/profiles_v2.yml`.

**Confirmed issues.** PySCF 2.14's Berny `kernel` returns `(converged, molecule)`, while `optimize` discards the flag. Main uses the latter, so a returned geometry is not proof of optimization convergence. Main also performs xTB before checking the saved geometry, sorts compounds in ascending heavy-atom order despite the brief saying largest-first, has a fixed 20-element job matrix despite an arbitrary `nchunks` input, and only seeds partials—not completed profiles—between runs. [R3, R4, R5, U2]

**Mechanism.** Use `kernel` and fail closed on nonconvergence; inspect and validate a checkpoint before running xTB; write full-precision checkpoint coordinates; atomically replace completed sigma files; require a convergence declaration and a source/package fingerprint for completed-cache hits; fix metadata that incorrectly describes v2 geometry as xTB-only; sort largest-first; generate exactly the requested 1–20 chunks; propagate ordinary failures; and stop computation at 320 minutes to reserve part of the 355-minute job limit for artifact upload.

The output fingerprint includes the QC source and relevant package versions. It intentionally prevents silently importing completed files produced by a different implementation. **Legacy sigma files without the convergence flag are not blessed retroactively**: this patch recomputes them when used as cache inputs. Legacy partials still carry only atom/coordinate information; cross-method partial reuse must be excluded by the maintainer. Full Berny optimizer history is not restored.

**Arithmetic.** If xTB takes 60 s and the remaining restarted work takes 1,800 s, skipping xTB gives only `(1800+60)/1800=1.033×`. It will not rescue a six-hour DFT tail by itself. If a later, correctly fingerprinted retry contains 16 already-completed equal-cost molecules and 4 incomplete ones, not recomputing the 16 changes useful work from 20 units to 4, up to 5× for that retry. That scenario does **not** describe the existing legacy artifacts, and it does not apply when `--keys` already selects only unfinished compounds. Scheduling improves the wall-time tail; it does not remove quantum arithmetic.

**Exactness.** For convergent cold calculations the numerical method is unchanged. The convergence/output guards change invalid-output behavior, not valid scientific results. The checkpoint precision/restart path must still pass profile equivalence; a restarted optimizer is not trajectory-identical because the Berny Hessian/trust history is absent. The 320-minute timeout is an operational reserve, not a promise that artifact upload always succeeds after arbitrary infrastructure failures.


### Unified diff — P2

<!-- PATCH:P2 -->
```diff
--- a/src/zcosmo/pyscf_cosmo_v2.py
+++ b/src/zcosmo/pyscf_cosmo_v2.py
@@ -19,13 +19,24 @@
 from zcosmo.pyscf_cosmo import BOHR, RADII, cosmo_segments, to_profiles, write_sigma, xtb_geometry
 
 
+def profile_revision():
+    import hashlib
+    from importlib.metadata import version
+    here = Path(__file__).resolve().parent
+    code = b"".join((here / name).read_bytes() for name in
+                    ("pyscf_cosmo.py", "pyscf_cosmo_v2.py", "pcm_lu.py") if (here / name).exists())
+    packages = [(name, version(name)) for name in ("pyscf", "pyberny", "rdkit", "tblite", "ase", "numpy", "scipy")]
+    return hashlib.sha256(code + json.dumps(packages).encode()
+                          + os.environ.get("ZC_TRIC_PREOPT", "0").encode()).hexdigest()
+
+
 def dft_geometry(sym, xyz_A, basis="def2-svp", maxsteps=100, partial=None, spin=0):
     """partial: optional JSON path; the current geometry is written there after every Berny cycle so a job
     killed by a wall-clock cap can resume from its last geometry (same functional, basis, solvent and
     convergence criteria; only the Berny Hessian guess restarts)."""
     from pyscf import gto, dft
     from pyscf.data import elements
-    from pyscf.geomopt.berny_solver import optimize
+    from pyscf.geomopt.berny_solver import kernel
     mol = gto.M(atom=[(s, tuple(p)) for s, p in zip(sym, xyz_A)], basis=basis, unit="Angstrom", verbose=0,
                 spin=spin, max_memory=int(os.environ.get("QC_MEM_MB", "3000")))
     mf = (dft.UKS(mol) if spin else dft.RKS(mol)).density_fit().PCM()
@@ -44,10 +55,12 @@
         if partial is not None and env.get("mol") is not None:
             tmp = str(partial) + ".tmp"
             with open(tmp, "w") as f:
-                json.dump({"sym": list(sym), "x": np.round(env["mol"].atom_coords(unit="Angstrom"), 6).tolist(),
+                json.dump({"sym": list(sym), "x": env["mol"].atom_coords(unit="Angstrom").tolist(),
                            "cycle": int(env.get("cycle", -1))}, f)
             os.replace(tmp, partial)
-    m2 = optimize(mf, maxsteps=maxsteps, callback=cb)
+    converged, m2 = kernel(mf, maxsteps=maxsteps, callback=cb)
+    if not converged:
+        raise RuntimeError(f"Berny did not converge in {maxsteps} steps; checkpoint retained")
     return np.asarray(m2.atom_coords(unit="Angstrom"))
 
 
@@ -55,27 +68,50 @@
 OPEN_SHELL = {"O=O": 2}
 
 
+def complete_profile(path):
+    """Legacy files without a convergence declaration are not certified cache hits."""
+    try:
+        meta = json.loads(path.read_text().splitlines()[0][len("# meta: "):])
+        a = np.loadtxt(path)
+        return (meta.get("geometry_converged") is True
+                and meta.get("profile_revision") == profile_revision() and a.shape == (153, 2)
+                and np.isfinite(a).all() and (a[:, 1] >= 0).all() and a[:, 1].sum() > 0)
+    except (OSError, ValueError, IndexError):
+        return False
+
+
 def run_one(row, outdir):
     key = row["inchikey"]
     dest = Path(outdir) / f"{key}.sigma"
-    if dest.exists():
+    if complete_profile(dest):
         return key, "exists", 0.0
     t = time.time()
     try:
-        sym, x0 = xtb_geometry(row["smiles"])
         partial = Path(outdir) / f"{key}.partial.json"
+        # Atom order comes from the same RDKit construction, without an xTB optimization.
+        from rdkit import Chem
+        mol = Chem.AddHs(Chem.MolFromSmiles(row["smiles"]))
+        sym = [a.GetSymbol() for a in mol.GetAtoms()]
         resumed = False
         if partial.exists():
             p = json.loads(partial.read_text())
-            if p["sym"] == list(sym):
-                x0, resumed = p["x"], True
+            trial = np.asarray(p["x"], dtype=float)
+            if p["sym"] == sym and trial.shape == (len(sym), 3) and np.isfinite(trial).all():
+                x0, resumed = trial, True
+        if not resumed:
+            sym, x0 = xtb_geometry(row["smiles"])
         spin = OPEN_SHELL.get(row["smiles"], 0)
         x = dft_geometry(sym, np.asarray(x0), partial=partial, spin=spin)
         seg, e = cosmo_segments(sym, x, spin=spin)
         out, meta = to_profiles(sym, x, seg)
         meta["E_scf_Eh"] = e
+        meta["geometry_converged"] = True
+        meta["profile_revision"] = profile_revision()
+        meta["source"] = "pyscf_cosmo_v2 BP86/def2-SVP conductor geometry; BP86/def2-TZVP conductor profile"
         meta["geometry"] = "BP86/def2-SVP C-PCM conductor (pyberny)" + (" [resumed from checkpoint]" if resumed else "")
-        write_sigma(dest, out, meta, key)
+        tmp = dest.with_suffix(".sigma.tmp")
+        write_sigma(tmp, out, meta, key)
+        os.replace(tmp, dest)
         with open(Path(outdir) / f"{key}.xyz.json", "w") as f:
             json.dump({"sym": sym, "x": np.round(x, 5).tolist()}, f)
         partial.unlink(missing_ok=True)
@@ -92,15 +128,21 @@
     ap.add_argument("--nchunks", type=int, default=1)
     ap.add_argument("--keys", default="")
     a = ap.parse_args()
+    if not (1 <= a.nchunks <= 20 and 0 <= a.chunk < a.nchunks):
+        ap.error("require 1 <= nchunks <= 20 and 0 <= chunk < nchunks")
     Path(a.outdir).mkdir(parents=True, exist_ok=True)
     d = pd.read_csv(a.csv)
     if a.keys:
         d = d[d.inchikey.isin(a.keys.split(","))]
-    d = d.sort_values(["heavy_atoms", "inchikey"]).reset_index(drop=True)
+    d = d.sort_values(["heavy_atoms", "inchikey"], ascending=[False, True]).reset_index(drop=True)
     d = d.iloc[a.chunk::a.nchunks]  # round-robin so chunks are balanced by size
+    failed = False
     for r in d.to_dict("records"):
         k, st, dt = run_one(r, a.outdir)
         print(k, st, f"{dt:.0f}s", flush=True)
+        failed |= st.startswith("fail:")
+    if failed:
+        raise SystemExit(1)
 
 
 if __name__ == "__main__":
--- a/src/zcosmo/pyscf_cosmo.py
+++ b/src/zcosmo/pyscf_cosmo.py
@@ -125,7 +125,7 @@
 def write_sigma(path, out, meta, key):
     meta = dict(meta)
     meta["standard_INCHIKEY"] = key
-    meta["source"] = "pyscf_cosmo BP86/def2-TZVP C-PCM conductor, GFN2-xTB geometry"
+    meta.setdefault("source", "pyscf_cosmo BP86/def2-TZVP C-PCM conductor, GFN2-xTB geometry")
     with open(path, "w") as f:
         f.write("# meta: " + json.dumps(meta) + "\n")
         f.write("# Rows are given as: sigma [e/A^2] followed by a space, then psigmaA [A^2]\n")
--- a/.github/workflows/profiles_v2.yml
+++ b/.github/workflows/profiles_v2.yml
@@ -9,14 +9,28 @@
   contents: read
   actions: read
 jobs:
+  plan:
+    runs-on: ubuntu-latest
+    outputs:
+      matrix: ${{ steps.matrix.outputs.matrix }}
+    steps:
+      - id: matrix
+        env: {NCHUNKS: "${{ inputs.nchunks }}"}
+        run: |
+          python - <<'PYCODE' >> "$GITHUB_OUTPUT"
+          import json, os
+          n = int(os.environ["NCHUNKS"])
+          assert 1 <= n <= 20, "nchunks must be between 1 and 20"
+          print("matrix=" + json.dumps({"chunk": list(range(n))}))
+          PYCODE
   profiles:
+    needs: plan
     runs-on: ubuntu-latest
     timeout-minutes: 355
     strategy:
       fail-fast: false
       max-parallel: 20
-      matrix:
-        chunk: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
+      matrix: ${{ fromJSON(needs.plan.outputs.matrix) }}
     env:
       OMP_NUM_THREADS: "4"
       QC_MEM_MB: "10000"
@@ -32,9 +46,18 @@
         env: {GH_TOKEN: "${{ github.token }}"}
         run: |
           mkdir -p out seed
-          gh run download ${{ inputs.seed_run }} -R ${{ github.repository }} -D seed || true
-          find seed -name '*.partial.json' -exec cp {} out/ \; ; ls out | wc -l
-      - run: python -m zcosmo.pyscf_cosmo_v2 out data/benchmark/compounds.csv --chunk ${{ matrix.chunk }} --nchunks ${{ inputs.nchunks }} --keys "${{ inputs.keys }}" 2>&1 | grep -v -i warn | tee out_${{ matrix.chunk }}.log
+          gh run download "${{ inputs.seed_run }}" -R "${{ github.repository }}" -D seed
+          find seed -type f \( -name '*.partial.json' -o -name '*.sigma' -o -name '*.xyz.json' \) -exec cp {} out/ \;
+          # Only files marked geometry_converged=true will be reused by the runner.
+          ls out | wc -l
+      - name: compute with time reserved for artifact upload
+        env: {PROFILE_KEYS: "${{ inputs.keys }}"}
+        run: |
+          set +e
+          timeout --signal=TERM --kill-after=20s 19200s python -u -m zcosmo.pyscf_cosmo_v2 out data/benchmark/compounds.csv --chunk ${{ matrix.chunk }} --nchunks ${{ inputs.nchunks }} --keys "$PROFILE_KEYS" 2>&1 | tee out_${{ matrix.chunk }}.log
+          rc=${PIPESTATUS[0]}
+          if [ "$rc" = 124 ]; then echo "Compute deadline: uploading checkpoints"; exit 0; fi
+          exit "$rc"
       - uses: actions/upload-artifact@v4
         if: always()
         with: {name: "profiles_v2_${{ github.run_id }}_${{ matrix.chunk }}", path: "out*", retention-days: 14}
```

### Apply, benchmark and check

First compare a complete fresh candidate run with the validated reference, then deliberately interrupt and resume water as a smoke test. H0 treats the intentional interruption separately from a scientific failure.

```bash
make_tree P2
(
  cd "$WORK/P2"
  export PYTHONPATH=src OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4 QC_MEM_MB=10000
  python scripts/optimization_check.py qc --out "$WORK/qc-P2"
  python scripts/optimization_check.py profiles --mode E \
    --reference "$WORK/qc-base" --candidate "$WORK/qc-P2" --out "$WORK/P2-profile-check.json"
  python scripts/optimization_check.py qc --key XLYOFNOQVPJJNP-UHFFFAOYSA-N \
    --interrupt-cycle 1 --out "$WORK/P2-resume-smoke"
  python scripts/optimization_check.py qc --key XLYOFNOQVPJJNP-UHFFFAOYSA-N \
    --resume --out "$WORK/P2-resume-smoke"
  # A second resume call must be a validated cache hit, not another geometry optimization.
  python scripts/optimization_check.py qc --key XLYOFNOQVPJJNP-UHFFFAOYSA-N \
    --resume --out "$WORK/P2-resume-smoke"
)
```

The one-molecule smoke test checks restart mechanics, not the full E gate. The preceding 25-molecule comparison is mandatory. The workflow matrix is now derived from `nchunks`; validate the workflow on an actual dispatch before treating upload/recovery as verified infrastructure. No cloud workflow was dispatched in this review.

## 6. P6 — E candidate: analytic Z0x interior derivatives with the existing endpoint stencil retained


**Target:** `src/zcosmo/z0x.py::Z0xBinary.lngamma`, new `_analytic`.

**Mechanism.** The current central difference evaluates `g(x−h), g(x), g(x+h)` at three different dielectric coefficients. Each coefficient can require a new mixture solve and two new pure-reference solves. The analytic replacement uses one mixture solution and its two pure references. Crucially, it differentiates the **pure reference terms as well as the mixture term**. It needs no implicit linear solve beyond the segment solution itself. [R7]

Here is the derivation used for the patch. Let `c=A_ES`, `p` be the mixture's normalized profile, `y=lnΓ`, `z=p⊙exp(y)`, and `D_mn=(σ_m+σ_n)²`. Repeated sigma values cover all three profile blocks. Define

$$M(p,y)=z^T(E\odot D)z.$$

At the symmetric-kernel fixed point, the row-stochastic matrix `P_ij=Γ_i E_ij p_j Γ_j` has stationary measure `p`. Differentiating the log segment equations and left-multiplying by `p` gives

$$p^T\partial_c y=\frac{M(p,y)}{2RT}.$$

For the residual excess Gibbs energy,

$$g_c=\frac{\bar A M(p,y)-\sum_i x_i A_i M(p_i,y_i)}{2RTa_{eff}},\qquad \bar A=\sum_i x_i A_i.$$

For the volume-weighted dielectric and `c=C(ε−1)/(ε+1/2)`,

$$\epsilon'=\frac{V_0V_1(\epsilon_0-\epsilon_1)}{[xV_0+(1-x)V_1]^2},\qquad
c'=C\frac{3\epsilon'/2}{(\epsilon+1/2)^2}.$$

Thus the consistent chemical potentials are

$$\ln\boldsymbol\gamma=\ln\boldsymbol\gamma_{\text{frozen }c}+
\begin{pmatrix}1-x\\-x\end{pmatrix}g_c c'.$$

The combinatorial and registered dispersion terms do not introduce another `c` derivative. The patch uses the same rounded temperature as the cached segment kernel for this derivative.

**Numerical-equivalence boundary.** The formula is an exact derivative of the intended continuous `g`, **not an identity for main's finite-`h` difference**. Therefore the patch retains the original implementation for `x≤H` and `x≥1−H`, including the infinite-dilution endpoints. Interior promotion requires the fixed-grid prediction comparison below. The six-case synthetic identity test gave a maximum discrepancy of `8.92e-9` versus a centered derivative at `h=1e-5`; that is not a real-mixture acceptance result.

**Arithmetic.** With cold coefficient-specific pure caches, main makes about `3×(1 mixture + 2 pure)=9` segment solves; the patch makes `1+2=3`, plus inexpensive moment contractions. With warm pure caches it changes three mixture solves to one. The ceiling is approximately 3× for those interior calls, with a practical hypothesis of 1.8–3×. **The registered IDAC endpoint calls are deliberately not accelerated by P6.** Benefit is in interior VLE/HE/LLE work. P3 and P6 savings overlap; measure their merged speed-up rather than multiplying headline figures.


### Unified diff — P6

<!-- PATCH:P6 -->
```diff
--- a/src/zcosmo/z0x.py
+++ b/src/zcosmo/z0x.py
@@ -6,7 +6,7 @@
 import numpy as np
 import pandas as pd
 
-from zcosmo.cosmosac import Mixture, load_fluid
+from zcosmo.cosmosac import Mixture, load_fluid, solve_gamma, _pure_lnG, SIG, R_KCAL
 from zcosmo.models import load_z_params, ROOT
 from zcosmo.zmodel import c_es_theory
 
@@ -46,9 +46,36 @@
         lg = self._frozen(T, x1, self._c(x1))
         return x1 * lg[0] + (1 - x1) * lg[1]
 
+    def _analytic(self, T, x1):
+        x = np.array([x1, 1 - x1])
+        mix = Mixture(self.keys, self.z0.with_(A_ES=self._c(x1)))
+        A, aeff = mix.A, mix.prm.aeff
+        psA = np.array([f.psigA.ravel() for f in mix.fl])
+        p = (x @ psA) / (x @ A)
+        E = mix._E(T)
+        ym = np.log(solve_gamma(E, p))
+        yi = np.array([_pure_lnG(f.key, round(float(T), 6), mix.prm, psA[i].tobytes())
+                       for i, f in enumerate(mix.fl)])
+        lg = (mix.lngamma_comb(x) + np.sum(psA * (ym - yi), axis=1) / aeff
+              + mix.lngamma_disp(x, T))
+        sig = np.tile(SIG, 3)
+        ED = E * (sig[:, None] + sig[None, :]) ** 2
+        z = p * np.exp(ym)
+        zpure = (psA / A[:, None]) * np.exp(yi)
+        moment = z @ ED @ z
+        pure_moments = np.einsum("ki,ij,kj->k", zpure, ED, zpure)
+        gc = ((x @ A) * moment - (x * A) @ pure_moments) / (2 * R_KCAL * round(float(T), 6) * aeff)
+        volume = x @ self.V
+        eps = (x * self.V) @ self.eps / volume
+        deps = self.V.prod() * (self.eps[0] - self.eps[1]) / volume ** 2
+        dc = c_es_theory(fpol=1.0) * 1.5 * deps / (eps + 0.5) ** 2
+        return lg + np.array([1 - x1, -x1]) * gc * dc
+
     def lngamma(self, T, x):
         x1 = float(x[0])
         h = self.H
+        if h < x1 < 1 - h:
+            return self._analytic(T, x1)
         a, b = max(x1 - h, 0.0), min(x1 + h, 1.0)
         dg = (self._g(T, b) - self._g(T, a)) / (b - a)
         g = self._g(T, x1)
```

### Apply, benchmark and check

```bash
make_tree P6
# Generate models-base.npz with P3's reference command if it is not already present.
(cd "$WORK/P6"; PYTHONPATH=src OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python scripts/optimization_check.py snapshot --grid --out "$WORK/models-P6.npz")
(cd "$WORK/P6"; PYTHONPATH=src python scripts/optimization_check.py compare \
  --reference "$WORK/models-base.npz" --candidate "$WORK/models-P6.npz" \
  --out "$WORK/P6-model-check.json")
```

Reject the E promotion if any finite-grid difference exceeds `1e-3`, if coverage changes, or if the merged full-scorecard regression changes a phase classification. Do not justify a finite-stencil disagreement by calling the new derivative “more exact”; that would require an A decision.

## 7. P7 — E: group GPU neighbor construction and remove per-graph scalar transfers


**Target:** `cloud/s15/multi_mace.py::__init__/_build`.

**Mechanism.** Main loops through every graph, obtains `float(self.L[g])` from a device tensor, constructs a full pairwise matrix, and extracts a variable-length edge list. Store the already-known cell lengths as CPU metadata at initialization, validate the cubic/PBC assumptions, group graphs by equal atom count and cell length, precompute upper-triangular pair indices, and build up to eight equal-shaped graph lists together. Keep reverse edges, image shifts, the original skin condition and the per-force-call true-cutoff filter. [R10]

For the 28-window water setup there are **71 MACE graphs**, not 28: `3×15 + 2×13`. Their sizes are mainly 192, 189 and 3. The grouped patch needs approximately `ceil(15/8)+ceil(28/8)+ceil(28/8)=10` nonzero extractions rather than 71 and removes 71 repeated device-scalar cell reads per rebuild. It also uses triangular rather than square candidate pairs. This does not fuse the whole MD step into one CUDA kernel.

**Arithmetic.** If a rebuild costs 20 ms every 20 steps, its amortized cost is 1 ms in a 120 ms step. Cutting rebuild cost by 3× saves only 0.667 ms, or about **1.006×** overall. If rebuild/filter/synchronization overhead instead accounts for 12% of runtime and the modified portion is halved, the ceiling is `1/(.88+.12/2)=1.064×`. This is why its rank is below sampling efficiency. The actual fraction must come from a rebuilding trajectory, not only translated, unchanged-edge timing frames.

**Exactness.** Groups are disjoint; graph offsets and both image-shift directions are preserved. The same minimum-image algorithm is valid only for fully periodic cubic cells with `L>2(r_cut+skin)`, now explicitly checked. Edge ordering can change floating-point reductions, so numerical equivalence still requires all-graph ASE comparisons. Near-cutoff membership and nonfinite/large-displacement cases deserve additional trajectory tests. CPU mock-model comparisons at float32 and float64 passed with zero observed force/energy difference, including rebuilds and an unwrapped periodic displacement; those tests do not certify CUDA MACE.


### Unified diff — P7

<!-- PATCH:P7 -->
```diff
--- a/cloud/s15/multi_mace.py
+++ b/cloud/s15/multi_mace.py
@@ -38,6 +38,15 @@
                 bd[k] = vs[0]
         self.bd = bd
         self.L = torch.tensor([float(a.cell[0, 0]) for a in systems], dtype=self.dtype, device=self.dev)
+        self.groups = {}
+        for g, a in enumerate(systems):
+            L = float(a.cell[0, 0])
+            if not np.all(a.pbc) or not np.allclose(np.asarray(a.cell), np.eye(3) * L, rtol=0, atol=1e-10):
+                raise ValueError("MultiMACE requires fully periodic cubic cells")
+            if L <= 2 * (self.rc + self.skin):
+                raise ValueError("box too small for minimum-image list")
+            self.groups.setdefault((len(a), L), []).append(g)
+        self.pairs = {n: torch.triu_indices(n, n, 1, device=self.dev) for n, _ in self.groups}
         self.cells = torch.stack([torch.tensor(np.asarray(a.cell), dtype=self.dtype, device=self.dev) for a in systems])
         self.sys = torch.cat([torch.full((n,), g, device=self.dev, dtype=torch.long) for g, n in enumerate(self.n)])
         self.n_rebuild = 0
@@ -46,17 +55,22 @@
     def _build(self, pos):
         rc = self.rc + self.skin
         E, US = [], []
-        for g in range(self.G):
-            a, b = int(self.off[g]), int(self.off[g + 1]); L = float(self.L[g])
-            assert L > 2 * rc, "box too small for the minimum-image GPU list"
-            x = pos[a:b]
-            d = x[None, :, :] - x[:, None, :]
-            S = -torch.round(d / L)
-            r = (d + S * L).norm(dim=-1)
-            m = torch.triu(r < rc, diagonal=1)
-            i, j = m.nonzero(as_tuple=True); Sc = S[i, j]
-            E.append(torch.stack([torch.cat([i, j]), torch.cat([j, i])]) + a)
-            US.append(torch.cat([Sc, -Sc]))
+        for (n, L), graphs in self.groups.items():
+            i, j = self.pairs[n]
+            # Bound temporary storage; each group has equal n and an exactly equal cubic L.
+            for first in range(0, len(graphs), 8):
+                gs = graphs[first:first + 8]
+                offsets = torch.tensor(self.off[gs], device=self.dev)
+                ids = offsets[:, None] + torch.arange(n, device=self.dev)[None, :]
+                x = pos[ids]
+                d = x[:, j] - x[:, i]
+                S = -torch.round(d / L)
+                keep = (d + S * L).square().sum(-1) < rc * rc
+                gidx, pair = keep.nonzero(as_tuple=True)
+                a, b = offsets[gidx] + i[pair], offsets[gidx] + j[pair]
+                Sc = S[gidx, pair]
+                E.append(torch.stack([torch.cat([a, b]), torch.cat([b, a])]))
+                US.append(torch.cat([Sc, -Sc]))
         self.ei = torch.cat(E, 1); self.us = torch.cat(US, 0).to(self.dtype)
         self.sh = torch.bmm(self.us[:, None, :], self.cells[self.sys[self.ei[0]]])[:, 0]
         self.x_ref = pos.detach().clone(); self.n_rebuild += 1
```

### Apply, benchmark and check

```bash
make_tree P7
(cd "$WORK/P7"; PYTHONPATH=src python scripts/optimization_check.py mace \
  --reference "$WORK/base" --full --out "$WORK/P7-MACE-check.json")
```

This checks every graph against ASE at several fixed frames, times ordinary calls separately from forced rebuilds, and reports peak allocated memory. It does not mistake the rebuilt-call speed-up for the full-trajectory speed-up. Benchmark on the actual L4/T4/consumer GPU, using the same cached checkpoint and cuEq setting for both implementations.

## 8. P8 — E: fit memory by splitting whole graphs, not by deleting windows or edges


**Target:** `cloud/s15/multi_mace.py::__init__/forces`.

**Mechanism.** Honor `ZC_MAX_GRAPH_NODES`. Greedily partition the list of complete independent graphs into subbatches, share the same model object, evaluate those subbatches sequentially, and concatenate energies and forces in their original order. A single graph larger than the cap fails explicitly. No spatial partition cuts an interacting graph, and the physical force assembly in the runner remains unchanged.

**Memory arithmetic.** The 15 λ / 13 μ calculation duplicates a physical box in the full and separated Hamiltonian graphs. Total graph nodes are `n(2×15+13)=43n`: **8,256 for 192-atom water boxes and 16,512 for 384-atom methanol boxes**. That explains the reported approximately 16.5k-node warning. A cap of 8,000 nodes splits the latter into at least three graph-preserving pieces (ceil(16512/8000)=3; greedy packing can require more), reducing simultaneous activations while retaining all 28 physical windows. A node cap is a proxy, not a guaranteed VRAM bound; edge count and model activations matter. [R11, R19]

**Speed claim.** This is a feasibility patch. If two/three smaller calls cost 0.14/0.10 s each instead of one fitting 0.234 s call, the total can be slower. There is no justified positive speed-up on a batch that already fits. On a device where main OOMs, successful sampling is preferable to no result, but “infinite speed-up” would be a misleading metric.

**Exactness.** Independent graph energies add and their force derivatives are independent. The model weights are shared, not copied or retrained. Floating-point batching/reduction differences still need the ASE force gate. The CPU mock tests passed; **no claim is made that 8,000 nodes fit a 6 GB RTX 2060**. Start with small safe validation batches and raise the cap only using measured memory headroom, not the warning threshold from a different GPU.


### Unified diff — P8

<!-- PATCH:P8 -->
```diff
--- a/cloud/s15/multi_mace.py
+++ b/cloud/s15/multi_mace.py
@@ -7,6 +7,7 @@
 Exactness: MACE message passing only runs along edges, and edges only join nodes of the same system, so each
 system's energy (per-graph readout) and forces are identical to evaluating it alone. Neighbour lists are GPU
 minimum-image lists per system with a Verlet skin and the per-step r < r_max filter (as in zc_md / fast_md)."""
+import os
 import numpy as np, torch
 
 NODE_KEYS = {"positions", "node_attrs", "forces", "density_coefficients"}
@@ -14,8 +15,25 @@
 
 
 class MultiMACE:
-    def __init__(self, calc, systems, skin=1.0):
+    def __init__(self, calc, systems, skin=1.0, max_nodes=None):
         """systems: list of ASE Atoms (periodic, cubic, L > 2 (r_max + skin))."""
+        limit = int(os.environ.get("ZC_MAX_GRAPH_NODES", "0")) if max_nodes is None else max_nodes
+        if limit < 0:
+            raise ValueError("max_nodes must be nonnegative")
+        self.parts = []
+        if limit and sum(map(len, systems)) > limit:
+            start, nodes = 0, 0
+            for j, at in enumerate(systems):
+                if len(at) > limit:
+                    raise ValueError("a single graph exceeds the node limit; do not split its atoms")
+                if nodes + len(at) > limit:
+                    self.parts.append(MultiMACE(calc, systems[start:j], skin, max_nodes=0))
+                    start, nodes = j, 0
+                nodes += len(at)
+            self.parts.append(MultiMACE(calc, systems[start:], skin, max_nodes=0))
+            self.G, self.M = len(systems), sum(map(len, systems))
+            self.n_rebuild = sum(p.n_rebuild for p in self.parts)
+            return
         self.calc, self.model = calc, calc.models[0]
         self.rc = float(self.model.r_max); self.skin = skin
         p = next(self.model.parameters()); self.dev, self.dtype = p.device, p.dtype
@@ -63,6 +81,13 @@
 
     def forces(self, pos):
         """pos: (M,3) unwrapped positions of all systems stacked. Returns (energies (G,), forces (M,3))."""
+        if self.parts:
+            energies, forces, start = [], [], 0
+            for part in self.parts:
+                e, f = part.forces(pos[start:start + part.M])
+                energies.append(e); forces.append(f); start += part.M
+            self.n_rebuild = sum(p.n_rebuild for p in self.parts)
+            return torch.cat(energies), torch.cat(forces)
         if (pos - self.x_ref).norm(dim=1).max() > 0.5 * self.skin:
             self._build(pos)
         s, r = self.ei
```

### Apply, benchmark and check

```bash
make_tree P8
# Accuracy can be tested without requiring the reference full batch to fit the GPU.
(cd "$WORK/P8"; ZC_MAX_GRAPH_NODES=2000 PYTHONPATH=src \
  python scripts/optimization_check.py mace --reference "$WORK/base" \
  --serial-reference --out "$WORK/P8-small-force-check.json")
# Capacity/throughput trial: same complete 28-window collection, smaller activation batches.
(cd "$WORK/P8"; ZC_MAX_GRAPH_NODES=4000 PYTHONPATH=src \
  python scripts/optimization_check.py mace --reference "$WORK/base" \
  --serial-reference --full --out "$WORK/P8-capacity-check.json")
```

`--serial-reference` checks every graph against ASE forces and compares both energy and forces with a single-graph instance of the original engine; it does not claim a full-batch main timing. The benchmark uses water boxes. A methanol production capacity test must also be run before selecting its cap. If this is needed to fit P4 on a smaller GPU, merge P8 into that experiment deliberately, use the same batching cap in both statistical arms, and rerun the force gate.

## Bugs, misleading defaults and wasted work in current main

The following are observations about the pinned code, not claims that every listed problem has already affected a published result.

| Severity | Finding and consequence | Status in this report |
|---|---|---|
| High | Berny `optimize()` discards the convergence flag; a returned geometry can be treated as a successful profile source. | P2 fixes it; H0 guards the reference too. [R3, U2] |
| High | `solve_gamma` returns after 5,000 iterations without reporting failure. Near difficult states this can contaminate derived finite differences or equilibrium calculations. | P3 adds a full residual and explicit failure. [R6] |
| High | D2's header claims a September 26 preregistration that is absent from the fetched `PREREGISTRATION.md`. | P4 adds a **new prospective** entry and labels the prior pilot exploratory. [R2, R11] |
| High | The v2 validation script is an A-versus-UD test, not an E-versus-main test; it skips missing profiles and does not exit unsuccessfully on `REJECT`. The candidate CSV contains 26 entries although the recorded completed validation has 25/2,302. | H0 freezes and checks coverage; the old script is not repurposed as an E certificate. [R16–R18] |
| High | `fast_md.FastMACE.forces` assumes the first half of the edge list is paired with reversed edges in the second half, even when `gpu_nl=False` delegates edge ordering to the generic parent/matscipy builder. That ordering contract is not established. | Do not trust that baseline/half-edge path without constructing or verifying the pairing. P7/P8 do not use it. [R12, R14] |
| High | `evaluate.predict_lle` can treat a missing/failed model or failed binodal search as “no split,” rather than distinguishing failure from miscibility. | Unfixed; preserve a separate failure/coverage category before interpreting LLE accuracy. [R15] |
| Medium | The D2 five-block TI uncertainty is weakly supported at the reported autocorrelation times, and the independent-window quadrature error formula is inappropriate after adding exchanges. | P4 fixes the joint observable; H0 uses stronger diagnostics and can return inconclusive. [R11] |
| Medium | The custom MBAR iteration can hit its cap silently. Neighbor overlap alone is not a complete convergence/error check. | Unfixed; do not certify MBAR results solely from the current printed numbers. H0's proposed acceptance is TI-based. [R11] |
| Medium | The s15 runner catches top-level exceptions and may exit zero; its end-of-run NPZ write is not an MD checkpoint. The Modal wrapper does not turn every subprocess failure into a failed job. | H0 checks failure logs and requires a newly written, finite sample file. This observation is about these files, not a claim that the newer pilot runner elsewhere has no checkpoint. [R11, R19] |
| Medium | xTB is run before loading the saved Berny coordinates; a valid DFT restart can waste xTB work or fail before reaching its checkpoint. | P2 fixes the ordering. [R3] |
| Medium | A geometry-only JSON restart loses Hessian/trust/SCF history; rounding to six decimals also prevents exact trajectory continuation. | P2 retains more coordinate precision, but is not a full-state restart implementation. [R3] |
| Medium | The workflow's 20 jobs are inconsistent with arbitrary `nchunks`: fewer requested chunks cause overlapping selections; more leave chunks uncovered. Current sorting is smallest-first. | P2 fixes both. [R3, R5] |
| Medium | A `.sigma` file's mere existence is treated as completion, and writes are not atomic; v2's shared writer reports xTB geometry in its source metadata. | P2 adds validity/provenance checks, atomic output and correct metadata. [R3, R4] |
| Medium | The QC workflow's warning filter obscures diagnostics, and a hard job timeout can prevent a later upload step from recovering the last checkpoint. | P2 retains logs and reserves upload time; infrastructure failures remain possible. [R5] |
| Medium | The A2 force check tests only the last replica. This cannot validate graph offsets/forces for every earlier replica. | H0 checks every graph. [R11] |
| Medium | `MultiMACE` treats `cell[0,0]` as a complete cubic cell description without checking general cell shape/PBC. | P7 adds scope guards; it does not implement triclinic periodicity. [R10] |
| Medium | The s14 surrogate test's last 40 frames also occur in its training set; that force MAE is not independent generalization evidence. A teacher-force call is followed by another teacher energy pass in `int_energy`. | Do not use that MAE as a held-out result; retain/reuse teacher energies when refactoring that experimental path. [R13] |
| Medium | The current LLE evaluator rounds temperatures to 2 K. It also has a coarse-hull fallback if the nonlinear binodal refinement fails. | Existing approximations; removing them is not an E runtime optimization. Report their use/failure explicitly. [R15] |
| Memory | `_E_cached` permits about **731.5 MiB** of matrix payload. `_pure_lnG` permits about **233.5 MiB** of returned arrays, plus roughly as much profile-byte key payload and Python overhead. `Z0xBinary._mix` is unbounded. Multiple processes can multiply this footprint. | Measure RSS/cache hit rates. Smaller caches preserve equations but are not claimed to improve speed without measurements. [R6, R7] |
| Reproducibility | `load_fluid` caches by its explicit arguments, not by the current override environment variable. Changing `ZC_SIGMA_OVERRIDE_DIR` inside one process can retain old fluids. | The commands use fresh processes or explicit profile directories; do not switch overrides in-place without clearing the relevant caches. [R6] |
| Reproducibility | `_frozen` keys a mixture by `round(c,6)` but stores the first unrounded `c`; two calls in one rounded bucket can depend on call order. MACE/cuEq/other package versions in the Modal image are unpinned. | Separate numerical cache quantization from exact caching; freeze packages/checkpoints before comparing results. P6 avoids this cache for interior evaluations but keeps the legacy endpoint behavior. [R7, R19] |

Two additional convergence guards merit attention before expanding the chemistry: xTB's `BFGS.run` and the MD packing `FIRE.run` return convergence information that is not checked here. Also, unsupported elements get no nonzero radius in the project's sparse radius table unless explicitly added; do not assume that every arbitrary input is in scope. These are input/quality guard issues, not evidence that all existing compounds failed. [R4, R11]

## Answers to the remaining optimization questions

### QC: what not to change under an E label

**Density reuse is already present inside the geometry scanner.** The PySCF SCF scanner uses its previous orbitals/density as a guess when compatible. A fresh `dft.RKS` at each Berny step is not what this code does. A separate SVP→TZVP density projection and a saved density on restart are still possible, but they only save initialization/SCF iterations at the handoff or restart; they do not remove a long chain's geometry cycles. For example, saving 5 minutes from a 180-minute optimization plus a 12-minute single point yields `192/187=1.027×`. A basis-projected guess can change which SCF solution is reached, particularly for an unrestricted state, so compare the final state as well as the convergence flag. [U5]

**RI auxiliary basis, pruning and cheap preoptimization.** Density fitting and a pruned DFT grid are already in use. Selecting a different auxiliary basis or dropping more grid points is not automatically E: it changes an existing numerical approximation and, under the brief's strict definition, grid changes belong in A. An xTB-ALPB or smaller-grid pre-stage followed by the original final polish is a legitimate A experiment, but ALPB is not the registered C-PCM Hamiltonian and a final polish does not prove basin identity. Do not loosen geometry or SCF thresholds based only on a few visually similar profiles. Register the cheaper stage/threshold and test all required profiles, not only easy molecules.

**SCF acceleration.** ADIIS/EDIIS or a damped startup can help cases with troublesome SCF histories; they cannot be assumed to accelerate already short, well-behaved SCFs. A final unshifted calculation is necessary after a level shift, and the same state must be checked. Log SCF iterations per geometry evaluation first. The current PCM gradient is analytic; replacing a supposed finite-difference PCM gradient is not an available saving. P1 attacks a verified cost inside that analytic workflow. [U1, U5]

**Four-core thread settings.** Benchmark identical fixed geometries at 1, 2 and 4 threads with `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS` and `MKL_NUM_THREADS` explicitly set. Do not run four four-thread QC jobs on one four-core runner and call that fourfold parallelism. The 20-runner farm is independent parallelism. For the tiny COSMO-SAC matrix solves and multi-process LLE, start with one BLAS thread per process and at most four worker processes, then measure memory and throughput. `lle_parallel.py` defaults to eight workers. [R9]

### GPU4PySCF: feasible capability, not a demonstrated drop-in speed-up on these GPUs

The official GPU4PySCF interface advertises density-fitted GGA, unrestricted calculations and PCM gradients. The inspected PCM implementation accepts custom radii and the cavity settings and already caches its matrix LU. Thus the BP86/DF/PCM components are not intrinsically CPU-only. [U6, U7]

An E attempt must preserve **BP86, both primary/auxiliary bases, grid construction and pruning, custom radii, surface discretization, finite `eps=1e9`, UKS spin, convergence tests and Hsieh conversion**, using double precision for the QC path. It must extract the same `q` rather than substitute a different symmetrized charge, and handle CPU/GPU array conversion explicitly. Do not enable a looser iterative low-memory PCM solver and still claim an unchanged solve. Keep the CPU NIST/Hsieh postprocessor initially.

I have **not** supplied a one-line `to_gpu()` “solution”: the inspected source is not a pinned, hardware-tested environment matching this repo, and none of the available GPUs was accessible here. The advertised A100-versus-single-core example is not an L4/T4/RTX2060/RTX4070 forecast. Confirm those device/package combinations, the custom surface and O₂ gradient path with fixed-geometry comparisons, then the complete profile gate. Unsupported combinations must fail or dispatch to CPU rather than silently changing the method. The P1 CPU patch is immediately testable without consuming scarce GPU credits.

### CUDA graphs, padding, half edges and precision

A padded edge count alone does not make the complete force computation graph-static. The present path still has a displacement-dependent host branch, a variable-length `nonzero`/filter, new tensors, and autograd force evaluation. Capture must use stable storage/shapes for the supported cuEq forward **and backward**, warm the kernels, and keep rebuild/control work outside the captured region. Padding must also be proved to contribute exactly zero energy/force for the actual model; arbitrary self-edges outside the cutoff are not a universal proof. Preserve the full traceback rather than logging only its last, possibly empty, line. [R12, R13]

The paired half-edge idea itself can be valid, but only with a proved canonical/reverse pairing and the correct parity of spherical harmonics. Fix the non-GPU-list ordering problem before treating its comparisons as trustworthy. A reported 12% half-edge improvement does not warrant a second headline estimate without accounting for overlap with batching and capture.

Do not use `torch.inference_mode()` to eliminate the autograd work needed for forces. Likewise, converting an already-rounded float32 graph energy to float64 does **not** recover lost bits. Accumulating interaction energies in float64 before full/solvent/solute cancellation may help, but needs inspection of the actual MACE readout and energy/force consistency tests. Force agreement alone does not bound a cancellation-induced free-energy bias. [R10–R14]

### More statistical efficiency after P4

**Window placement.** For independent windows with per-sample variance `σ_i²`, integrated correlation time `τ_i`, quadrature weight `w_i`, and cost rate `c_i`, the large-sample variance behaves as `Σ w_i² (2τ_i σ_i²)/t_i`. At a fixed cost `Σ c_i t_i`, optimal duration is proportional to `|w_i| σ_i sqrt(2τ_i/c_i)`. For equal cost and smoothly spaced windows, placement should account for autocorrelation as well as thermodynamic length; using `σ` alone is not enough for these slow windows. With replica exchange, cross-window covariance invalidates a naive independent-window allocation—use the joint observable or an estimator influence function.

Use a **separate pilot**, select a schedule from variance/overlap only, then freeze it before production. The current runner gives every window equal length and its TI estimate has finite-grid bias. Reducing 28 windows to 20 is only a 1.4× force-count ceiling if cost is linear in windows; small-batch overhead makes that optimistic, and lost overlap or larger trapezoid bias can erase it. A proposed new grid/path needs a prospective numerical acceptance criterion, not selection against experimental activity coefficients. No untested grid is smuggled into P4.

**Expanded ensemble/Gibbs λ moves.** These could exploit the same cheap cross-state energies, but their occupation weights must be frozen after pilot adaptation and the estimates must account for biased state visitation. They are alternatives to investigate after the simpler exchange comparison, not independent multiplicative speed-ups to add to it.

**Soft-core/WCA path constants.** Exact endpoint partition functions do not depend on the intermediate path, but finite-grid TI bias, overlap, equilibration and numerical singularities do. Endpoint identity alone does not prove an unchanged finite-run answer. Tune intermediate-path choices only using separately generated sampling diagnostics, register/freeze them, and verify endpoints and integration/MBAR convergence.

**Hydrogen mass repartitioning.** Changing masses cancels from a classical configurational free-energy difference when the same mass convention applies to both endpoints and no inconsistent kinetic/constraint normalization is introduced. It still changes dynamics and the finite-step integration error. A larger time step therefore needs an A time-step study, not a blanket E label. Constraints can also change the ensemble. Multiple-time-step integration similarly requires a defined force split and controlled integration error; there is no validated cheap, infrequently evaluated residual split in the supplied runner. The already measured 1.5× student is not automatically a useful replacement.

## Realistic cost per ln γ∞ under the brief's measured rates

Interpret the reported 0.23 kcal/mol as the standard error of **one total coupling leg** at 30 ps/window, and assume the same error for the corresponding pure-reference leg. At 298.15 K, the runner's constants give `kBT=0.592484 kcal/mol`. Independent legs then give

$$SE(\ln\gamma^\infty)\simeq\sqrt{0.23^2+0.23^2}/0.592484=0.549.$$

At 0.5 fs, 30 ps is 60,000 steps. Using 0.120 s per 28-window water-like step gives **2 GPU-hours per production leg**. Under the favorable `SE∝t^{-1/2}` scaling assumption, targeting `SE(lnγ∞)=0.10` requires `(0.549/.10)²=30.14` times the production, approximately **904 ps/window and 120.6 GPU-hours for two water-like legs**. At the reported 0.234 s methanol-like step cost, the analogous arithmetic is roughly 235 GPU-hours if both legs had that rate and the same variance. Cross/pure legs generally have different rates and variances.

These are conditional projections, **not precision-certified forecasts**: the original five-block error may be inaccurate, and equilibration, startup, density uncertainty, finite-size, time-step, quadrature and model errors are not included. The 30 ps comparison commands above deliberately use longer equilibration than the old default. A 2.4× statistical gain with an independent 1.1× engine gain would reduce 120.6 h to about **45.7 h**, not to minutes. Reusing a well-converged pure-solute reference across multiple solvents can amortize that reference, but its uncertainty must remain in every reported difference.

The coupling-leg difference is also not, by itself, the complete mole-fraction activity coefficient. With compatible classical excess-chemical-potential conventions in the thermodynamic limit,

$$\ln\gamma_i^\infty(j)=\beta[\mu_i^{ex}(j)-\mu_i^{ex}(i)]
+\ln[\rho_j^{number}/\rho_i^{number}].$$

This follows by subtracting `μ_i=kBT ln(ρ_i Λ_i³)+μ_i^ex` from the pure reference definition; use number density, not an unconverted ratio of mass densities. The finite 63-solvent/one-solute setup and NVT/model-density choice need corresponding finite-size/standard-state treatment. These points affect the final observable and are separate from faster force calls.

## Can the whole scorecard become minutes rather than hours?

Possibly **tens of minutes**, depending on the current runtime distribution; not established yet. If 90% of a two-hour scorecard is accelerated 20× by the accepted combined evaluator changes, the overall gain is `1/(.10+.90/20)=6.90×`, giving about 17.4 minutes. To get two hours down to five minutes requires a 24× total gain and a nonaccelerated fraction below 4.17%, even with an infinitely fast accelerated portion.

After independently accepting P3/P6, run the actual `zcosmo.evaluate` entry point for the same model list and `idac,vle,he,lle` tables with separate `ZC_PRED` directories and one BLAS thread per worker. Compare generated predictions, coverage and failures before looking at experimental scores. IDAC uses the mandatory `1e-3` lnγ gate; additional prospective regression gates should include VLE mole fractions at `1e-3`, relative pressure at `1e-3`, HE at 0.5 J/mol, LLE compositions at `1e-4`, and unchanged resolved split classifications. Near-critical or previously failed cases must be investigated, not silently treated as agreement. These extra table gates are deliberately explicit proposals, not existing registration claims. No whole-scorecard timing or acceptance is claimed in this report.

## Test record and limitations

Local tests used Linux/x86-64, NumPy 2.3.5, SciPy 1.17.0, and Torch 2.10.0 CPU, with one numerical-library thread. The synthetic solver timing is the average of 30 calls per case; it is not a hardware-comparative benchmark. The derivative check used six synthetic mixtures/compositions. The graph tests used a differentiable mock potential at float32/float64, not MACE. The PCM adapter test used a mock of the pinned interface, not PySCF. The physical commands are supplied precisely because these local checks cannot establish the brief's real-molecule and CUDA tolerances.

No proposed branch was pushed, no existing result was overwritten, no experiment was scored, and no GPU/cloud workload was launched. Prospective entries are contained in P4/P5 only; they take effect when the maintainer commits them before running those experiments.

## Appendix — H0: shared benchmark and acceptance harness

This is supporting code, not a scientific model change or a ninth speed-up proposal. It deliberately fails on missing coverage and distinguishes an underpowered statistical comparison from acceptance. Its confidence estimates rely on adequate equilibration/blocking and independent run replicates; they are not a theorem about an arbitrary nonstationary trajectory.

<!-- PATCH:H0 -->
```diff
--- /dev/null
+++ b/scripts/optimization_check.py
@@ -0,0 +1,346 @@
+"""Fail-closed optimization benchmarks. Run from a zcosmo checkout with PYTHONPATH=src.
+Uses no experimental response values. Exit 2 means statistically inconclusive, not accepted.
+"""
+from __future__ import annotations
+import argparse, hashlib, importlib.util, json, os, shutil, subprocess, sys, time
+from collections import Counter
+from pathlib import Path
+import numpy as np
+import pandas as pd
+
+ROOT = Path.cwd()
+
+def write(path, data):
+    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
+    path.write_text(json.dumps(data, indent=2, allow_nan=False))
+    print(json.dumps(data, indent=2, allow_nan=False))
+
+def fixture():
+    # Freeze the historical 25/2302 check, not the current 26-entry candidate list.
+    p = ROOT / 'results/pyscf_profile_validation.csv'
+    old = pd.read_csv(p, usecols=['key', 'T'])
+    assert len(old) == 2302 and old.key.nunique() == 25, 'historical fixture changed'
+    val = pd.read_csv('data/pyscf_sigma/validation_set.csv')
+    val = val[val.inchikey.isin(old.key.unique())]
+    assert val.inchikey.nunique() == 25 and len(val) == 25
+    table = pd.read_csv('data/benchmark/idac.csv', usecols=['solute', 'solvent', 'T', 'has_sigma'])
+    table = table[table.has_sigma]
+    rows = [(k, r.solute, r.solvent, float(r.T)) for k in val.inchikey
+            for r in table[(table.solute == k) | (table.solvent == k)].itertuples()]
+    assert len(rows) == 2302, 'row coverage differs from the recorded test; do not silently skip'
+    assert Counter((k, t) for k, _, _, t in rows) == Counter(zip(old.key, old.T))
+    return val, rows
+
+def pcm_check(a):
+    from pyscf import gto, dft
+    from pyscf.data import elements
+    from zcosmo.pyscf_cosmo import RADII, BOHR
+    from zcosmo.pcm_lu import cache_pcm
+    checks=[]
+    for label,atoms,spin in [('water','O 0 0 0; H 0 .76 .59; H 0 -.76 .59',0),
+                             ('oxygen','O 0 0 0; O 0 0 1.21',2)]:
+        for basis,level,lebedev,tol in [('def2-svp',2,17,1e-8),('def2-tzvp',3,29,1e-9)]:
+            outputs=[];times=[]
+            for cached in [False,True]:
+                mol=gto.M(atom=atoms,unit='Angstrom',basis=basis,spin=spin,verbose=0,
+                          max_memory=int(os.environ.get('QC_MEM_MB','3000')))
+                mf=(dft.UKS(mol) if spin else dft.RKS(mol)).density_fit().PCM()
+                mf.xc='b88,p86';mf.grids.level=level;mf.conv_tol=tol
+                solvent=mf.with_solvent;solvent.method='C-PCM';solvent.eps=1e9;solvent.lebedev_order=lebedev
+                radii=np.zeros(120)
+                for element,value in RADII.items():radii[elements.charge(element)]=value/BOHR
+                solvent.radii_table=radii
+                if cached:mf=cache_pcm(mf)
+                start=time.perf_counter();energy=mf.kernel();assert mf.converged
+                gradient=mf.nuc_grad_method().kernel();times.append(time.perf_counter()-start)
+                outputs.append((float(energy),np.asarray(gradient),np.asarray(mf.with_solvent._intermediates['q'])))
+            x,y=outputs
+            de=abs(y[0]-x[0]);dg=float(abs(y[1]-x[1]).max());dq=float(abs(y[2]-x[2]).max())
+            checks.append(dict(molecule=label,basis=basis,delta_energy_Eh=de,
+                               max_delta_gradient_Eh_Bohr=dg,max_delta_q_e=dq,
+                               reference_s=times[0],candidate_s=times[1]))
+            assert de<1e-8 and dg<1e-6 and dq<1e-8
+    write(a.out,dict(checks=checks))
+
+
+def qc(a):
+    from zcosmo import pyscf_cosmo_v2 as q
+    from pyscf.geomopt import berny_solver
+    val, _ = fixture()
+    if a.key:
+        val = val[val.inchikey == a.key]
+        assert len(val) == 1
+    dest = Path(a.out).resolve(); dest.mkdir(parents=True, exist_ok=True)
+    if not a.resume:
+        assert not list(dest.glob('*.sigma')), 'benchmark output must be fresh (or use --resume)'
+    traces, statuses = [], []
+    current = ['']; interrupted = [False]
+    def wrap(original, label, require_convergence):
+        def traced(*args, **kw):
+            cb = kw.pop('callback', None)
+            def callback(env):
+                if cb:
+                    cb(env)
+                scanner = env.get('g_scanner')
+                gradient = np.asarray(env.get('gradients'), float)
+                traces.append(dict(key=current[0], optimizer=label,
+                    energy=float(env['energy']), gradient=gradient.tolist(),
+                    scf_cycles=int(getattr(getattr(scanner, 'base', None), 'cycles', -1))))
+                write_trace = dest / 'trace.json'
+                write_trace.write_text(json.dumps(traces))
+                if a.interrupt_cycle and sum(r['key'] == current[0] for r in traces) == a.interrupt_cycle:
+                    interrupted[0] = True
+                    raise InterruptedError('intentional checkpoint benchmark')
+            ans = original(*args, callback=callback, **kw)
+            if require_convergence and not ans[0]:
+                raise RuntimeError('unconverged baseline or candidate geometry; not a valid reference')
+            return ans
+        return traced
+    berny_solver.kernel = wrap(berny_solver.kernel, 'berny', True)
+    try:
+        from pyscf.geomopt import geometric_solver
+        geometric_solver.kernel = wrap(geometric_solver.kernel, 'tric', False)
+    except ImportError:
+        pass
+    t = time.perf_counter()
+    for row in val.to_dict('records'):
+        current[0] = row['inchikey']
+        key, status, dt = q.run_one(row, dest)
+        statuses.append(dict(key=key, status=status, wall_s=dt))
+        if interrupted[0]:
+            assert list(dest.glob('*.partial.json'))
+            break
+        assert status in ('ok', 'exists'), (key, status)
+    write(dest/'timing.json', dict(wall_s=time.perf_counter()-t, molecules=statuses,
+        geometry_evaluations=len(traces), interrupted=interrupted[0]))
+
+def profiles(a):
+    from zcosmo.cosmosac import load_fluid, Mixture, Params
+    val, rows = fixture()
+    for k in val.inchikey:
+        assert (Path(a.candidate)/f'{k}.sigma').is_file(), f'missing exact candidate file: {k}'
+        if a.reference:
+            assert (Path(a.reference)/f'{k}.sigma').is_file(), f'missing exact reference file: {k}'
+            assert np.array_equal(np.loadtxt(Path(a.candidate)/f'{k}.sigma')[:,0],
+                                  np.loadtxt(Path(a.reference)/f'{k}.sigma')[:,0]), 'sigma grid changed'
+    cand = {k: load_fluid(k, str(Path(a.candidate).resolve())) for k in val.inchikey}
+    ud = {k: load_fluid(k) for k in val.inchikey}
+    ref = {k: load_fluid(k, str(Path(a.reference).resolve())) for k in val.inchikey} if a.reference else ud
+    max_dpa = max(float(abs(cand[k].psigA-ref[k].psigA).max()) for k in cand)
+    max_dp = max(float(abs(cand[k].psigA/cand[k].A-ref[k].psigA/ref[k].A).max()) for k in cand)
+    differences, versus_ud = [], []
+    t = time.perf_counter()
+    for k, solute, solvent, T in rows:
+        other = solvent if solute == k else solute
+        fo = load_fluid(other)
+        def value(f):
+            pair = [f, fo] if solute == k else [fo, f]
+            return Mixture(None, Params(), fluids=pair).lngamma_inf(T, 0)
+        lr, lc, lu = value(ref[k]), value(cand[k]), value(ud[k])
+        assert np.isfinite([lr, lc, lu]).all()
+        differences.append(abs(lc-lr)); versus_ud.append(abs(lc-lu))
+    result = dict(molecules=25, rows=len(rows), max_delta_p=max_dp, max_delta_psigmaA_A2=max_dpa,
+        max_delta_lngamma=float(max(differences)), median_delta_vs_UD=float(np.median(versus_ud)),
+        check_wall_s=time.perf_counter()-t, mode=a.mode)
+    write(a.out, result)
+    if a.mode == 'E':
+        assert a.reference, 'E requires current-main profiles as reference, not UD'
+        assert max_dp < 1e-4 and max_dpa < 1e-4 and max(differences) < 1e-3
+    else:
+        assert np.median(versus_ud) < .15
+
+def snapshot(a):
+    from zcosmo.models import make_model
+    _, rows = fixture()
+    compounds = pd.read_csv('data/benchmark/compounds.csv', usecols=['inchikey','smiles'])
+    smi = dict(zip(compounds.inchikey, compounds.smiles))
+    queries = [(s,v,T,0.0) for _,s,v,T in rows]
+    if a.grid:
+        xs = [0., 1e-8, 1e-4, .001, .01, .1, .25, .5, .75, .9, .99, .999, 1-1e-4, 1-1e-8, 1.]
+        queries += [(s,v,T,x) for s,v in sorted({(s,v) for _,s,v,_ in rows})
+                    for T in [250.,298.15,450.] for x in xs]
+    values, labels, cache = [], [], {}
+    start = time.perf_counter()
+    for name in ['cosmosac_dsp','Z0x']:
+        for s,v,T,x in queries:
+            k=(name,s,v)
+            if k not in cache:
+                cache[k]=make_model(name,[s,v],[smi[s],smi[v]])
+            y=np.asarray(cache[k].lngamma(T,np.array([x,1-x])),float)
+            # Missing Z0x inputs must be recorded, not silently dropped. COSMO is mandatory.
+            if name == 'cosmosac_dsp':
+                assert np.isfinite(y).all(), (name,s,v,T,x)
+            values.append(y);labels.append((name,s,v,T,x))
+    elapsed=time.perf_counter()-start
+    digest=hashlib.sha256(json.dumps(labels).encode()).hexdigest()
+    np.savez(a.out, values=values, labels_hash=digest, wall_s=elapsed, idac_rows=2302)
+    print(json.dumps(dict(rows=len(values), wall_s=elapsed, finite_values=int(np.isfinite(values).sum()))))
+
+def compare(a):
+    r=np.load(a.reference);c=np.load(a.candidate)
+    assert str(r['labels_hash']) == str(c['labels_hash']), 'query mismatch'
+    yr,yc=r['values'],c['values']
+    assert yr.shape == yc.shape and np.array_equal(np.isfinite(yr),np.isfinite(yc)), 'coverage changed'
+    valid=np.isfinite(yr)
+    assert valid.any()
+    error=float(np.max(abs(yc[valid]-yr[valid])))
+    result=dict(max_delta_lngamma=error, reference_wall_s=float(r['wall_s']),
+                candidate_wall_s=float(c['wall_s']), speedup=float(r['wall_s']/c['wall_s']))
+    write(a.out,result)
+    assert error < 1e-3
+
+def load_module(name,path):
+    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec)
+    sys.modules[name]=m;spec.loader.exec_module(m);return m
+
+def mace(a):
+    import torch
+    sys.path.insert(0,str(ROOT/'cloud/s15'))
+    from bench15_core import teacher
+    from bench6_core import water_box
+    import multi_mace
+    refmod=load_module('reference_multi_mace',Path(a.reference)/'cloud/s15/multi_mace.py')
+    calc=teacher(); dev=next(calc.models[0].parameters()).device
+    dtype=next(calc.models[0].parameters()).dtype
+    base=water_box(4)
+    w2,w1=(15,13) if a.full else (2,2)
+    systems=([base,base[3:],base[:3]]*w2 + [base[3:],base[:3]]*w1)
+    original=refmod.MultiMACE(calc,systems,.9) if not a.serial_reference else None
+    serial=[refmod.MultiMACE(calc,[at],.9) for at in systems] if a.serial_reference else None
+    candidate=multi_mace.MultiMACE(calc,systems,.9)
+    x=torch.cat([torch.tensor(at.positions,device=dev,dtype=dtype) for at in systems])
+    off=np.cumsum([0]+list(map(len,systems)))
+    max_force,max_energy=0.,0.
+    rng=np.random.default_rng(7)
+    frames=[]
+    for shift in [0.,.005,.6,float(base.cell[0,0])+1.2]:
+        frames.append(x+shift+torch.tensor(rng.normal(0,.001,x.shape),device=dev,dtype=dtype))
+    for frame in frames:
+        ec,fc=candidate.forces(frame)
+        if original is not None:
+            er,fr=original.forces(frame)
+            max_force=max(max_force,float((fr-fc).abs().max()))
+            max_energy=max(max_energy,float((er-ec).abs().max()))
+        for i,at in enumerate(systems):
+            if serial is not None:
+                er,fr=serial[i].forces(frame[off[i]:off[i+1]])
+                max_energy=max(max_energy,float((er[0]-ec[i]).abs()))
+                max_force=max(max_force,float((fr-fc[off[i]:off[i+1]]).abs().max()))
+            q=at.copy();q.positions=frame[off[i]:off[i+1]].detach().cpu().double().numpy();q.calc=calc
+            f=q.get_forces();err=float(abs(f-fc[off[i]:off[i+1]].cpu().numpy()).max())
+            max_force=max(max_force,err)
+    assert max_force < 1e-4, max_force
+    assert max_energy < 1e-4, max_energy
+    def sync():
+        if dev.type=='cuda':torch.cuda.synchronize()
+    def timed(engine,rebuild):
+        if engine is None:return None
+        engine.forces(x);sync();t=time.perf_counter()
+        for i in range(30):engine.forces(x+(0.6*i if rebuild else .00001*i))
+        sync();return (time.perf_counter()-t)/30
+    if dev.type=='cuda':torch.cuda.reset_peak_memory_stats()
+    fast=timed(candidate,False); rebuild=timed(candidate,True)
+    peak=torch.cuda.max_memory_allocated() if dev.type=='cuda' else 0
+    normal=timed(original,False);old_rebuild=timed(original,True)
+    write(a.out,dict(graphs=len(systems),nodes=len(x), max_force_error_eV_A=max_force,
+        max_energy_difference_eV=max_energy, candidate_s=fast, candidate_rebuild_s=rebuild,
+        reference_s=normal, reference_rebuild_s=old_rebuild, peak_allocated_bytes=peak,
+        dtype=str(dtype),device=str(dev),torch=torch.__version__))
+
+L2='0,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.65,0.7,0.75,0.8,0.85,0.9,1'
+M1='0,0.025,0.05,0.075,0.1,0.15,0.2,0.35,0.5,0.65,0.8,0.9,1'
+
+def fe_run(a):
+    out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
+    if a.dt != .5:
+        assert 'ZC_DT_FS' in Path('cloud/s15/bench15_core.py').read_text(), 'this revision has no dt switch'
+    env=dict(os.environ,ZC_DT_FS=str(a.dt),ZC_PRE_STEPS=str(round(1000/a.dt)),ZC_SOLUTE=a.solute,ZC_SOLVENT=a.solvent,ZC_SEED=str(a.seed),
+             ZC_EXCHANGE_EVERY=str(a.exchange),ZC_PROD_STEPS=str(a.prod),ZC_EQ_STEPS=str(a.eq),
+             ZC_LAM2=L2,ZC_MU1=M1)
+    env.pop('ZC_TEST',None)
+    path=Path(f'/tmp/d2_{a.solute}_in_{a.solvent}_s{a.seed}.npz')
+    before=path.stat().st_mtime_ns if path.exists() else -1
+    start=time.perf_counter()
+    with (out/'run.log').open('w') as f:
+        subprocess.run([sys.executable,'-u','cloud/s15/bench15_core.py'],env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
+    elapsed=time.perf_counter()-start
+    log=(out/'run.log').read_text()
+    assert 'stage_D2 failed:' not in log and 'D2 non-finite forces' not in log, 'runner reported failure'
+    assert path.exists() and path.stat().st_mtime_ns != before, 'runner failed without writing new samples'
+    d=dict(np.load(path));assert all(np.isfinite(d[k]).all() for k in ['rec2','rec1','rec1d'])
+    # End-to-end wall includes packing, FIRE, pre-equilibration and initialization.
+    d['wall_total_s']=elapsed;d['seed']=a.seed;d['exchange_every']=a.exchange;d['dt_fs']=a.dt
+    np.savez(out/'samples.npz',**d)
+    write(out/'timing.json',dict(wall_s=elapsed,frames=int(len(d['rec2'])),seed=a.seed,exchange=a.exchange))
+
+def weights(grid):
+    grid=np.asarray(grid,float);assert grid[0]==0 and grid[-1]==1 and (np.diff(grid)>0).all()
+    w=np.zeros(len(grid));dx=np.diff(grid);w[:-1]+=dx/2;w[1:]+=dx/2;return w
+
+def fe_check(a):
+    from pymbar import timeseries
+    from scipy.stats import t as student
+    EV=23.0605
+    summaries=[];all_grids=[];diagnostics=[];seen_paths=set();seen_seeds=set()
+    for paths in [a.reference,a.candidate]:
+        means=[];run_se=[];walls=[];counts=[]
+        for path in paths:
+            resolved=str(Path(path).resolve())
+            assert resolved not in seen_paths, 'duplicate trajectory is not an independent replicate'
+            seen_paths.add(resolved)
+            d=np.load(path)
+            seed=int(d['seed']);assert seed not in seen_seeds, 'the registered comparisons require independent seeds'
+            seen_seeds.add(seed)
+            q=np.c_[d['rec2'],d['rec1d']]
+            assert np.isfinite(q).all()
+            w=np.r_[weights(d['lam2']),weights(d['mu1'])]
+            all_grids.append((d['lam2'],d['mu1']))
+            # Common time trimming preserves simultaneous cross-window covariance.
+            starts=[int(timeseries.detect_equilibration(q[:,i])[0]) if np.std(q[:,i])>1e-14 else 0 for i in range(q.shape[1])]
+            start=max(starts);q=q[start:]
+            if len(q)<100:
+                print('INCONCLUSIVE: too few stationary samples'); raise SystemExit(2)
+            y=q@w*EV
+            gs=[float(timeseries.statistical_inefficiency(q[:,i])) if np.std(q[:,i])>1e-14 else 1. for i in range(q.shape[1])]
+            gy=float(timeseries.statistical_inefficiency(y)) if np.std(y)>1e-14 else 1.
+            # g = 1 + 2 tau/dt; choose blocks at least 5 tau and at least g samples.
+            block=max(1,int(np.ceil(2.5*max(gs+[gy]))))
+            n=len(y)//block
+            diagnostics.append(dict(path=path,discarded=start,g_max=max(gs),g_joint=gy,block_frames=block,blocks=n))
+            if n<2:
+                print(json.dumps(diagnostics,indent=2));raise SystemExit(2)
+            bm=y[:n*block].reshape(n,block).mean(1)
+            means.append(float(bm.mean()));run_se.append(float(bm.std(ddof=1)/np.sqrt(n)))
+            walls.append(float(d['wall_total_s']));counts.append(n)
+        if len(means)<4 or sum(counts)<8:
+            print(json.dumps(diagnostics,indent=2));raise SystemExit(2)
+        # Replicates, not individual windows, are independent. Use the larger uncertainty estimate.
+        mean=float(np.mean(means));var=max(float(np.var(means,ddof=1)/len(means)),float(np.sum(np.square(run_se))/len(means)**2))
+        summaries.append(dict(mean=mean,var_mean=var,wall_s=sum(walls),runs=len(means),blocks=sum(counts)))
+    for g in all_grids:
+        assert np.array_equal(g[0],all_grids[0][0]) and np.array_equal(g[1],all_grids[0][1]), 'path grids changed'
+    r,c=summaries;delta=c['mean']-r['mean'];se=np.sqrt(r['var_mean']+c['var_mean'])
+    df=min(r['runs'],c['runs'])-1
+    half=float(student.ppf(.95,df)*se)
+    # Variance(mean)*total wall, not ESS alone, determines time to a fixed free-energy error.
+    gain=r['var_mean']*r['wall_s']/(c['var_mean']*c['wall_s']) if c['var_mean']>0 else None
+    equivalent=abs(delta)+half < .10
+    write(a.out,dict(reference=r,candidate=c,delta_kcal=delta,CI90=[delta-half,delta+half],
+        pilot_efficiency_gain=gain,equivalent_within_0_10_kcal=equivalent,diagnostics=diagnostics,
+        status='PILOT_EQUIVALENCE' if equivalent else 'INCONCLUSIVE'))
+    if not equivalent:raise SystemExit(2)
+    # A positive pilot is not a proof of speedup or absence of common time-step/quadrature bias.
+
+def main():
+    ap=argparse.ArgumentParser();sub=ap.add_subparsers(dest='cmd',required=True)
+    p=sub.add_parser('pcm-check');p.add_argument('--out',required=True)
+    p=sub.add_parser('qc');p.add_argument('--out',required=True);p.add_argument('--key');p.add_argument('--resume',action='store_true');p.add_argument('--interrupt-cycle',type=int,default=0)
+    p=sub.add_parser('profiles');p.add_argument('--reference');p.add_argument('--candidate',required=True);p.add_argument('--mode',choices=['E','A'],required=True);p.add_argument('--out',required=True)
+    p=sub.add_parser('snapshot');p.add_argument('--out',required=True);p.add_argument('--grid',action='store_true')
+    p=sub.add_parser('compare');p.add_argument('--reference',required=True);p.add_argument('--candidate',required=True);p.add_argument('--out',required=True)
+    p=sub.add_parser('mace');p.add_argument('--reference',required=True);p.add_argument('--out',required=True);p.add_argument('--full',action='store_true');p.add_argument('--serial-reference',action='store_true')
+    p=sub.add_parser('fe-run');p.add_argument('--out',required=True);p.add_argument('--dt',type=float,choices=[.25,.5],default=.5);p.add_argument('--seed',type=int,required=True);p.add_argument('--exchange',type=int,default=0);p.add_argument('--prod',type=int,default=60000);p.add_argument('--eq',type=int,default=20000);p.add_argument('--solute',default='water');p.add_argument('--solvent',default='water')
+    p=sub.add_parser('fe-check');p.add_argument('--reference',nargs='+',required=True);p.add_argument('--candidate',nargs='+',required=True);p.add_argument('--out',required=True)
+    a=ap.parse_args();globals()[a.cmd.replace('-','_')](a)
+
+if __name__=='__main__':main()
```

## Source map

All `R` sources below are at `62172c7e7bb59737d28b115b9ef37311a98bb6cc`, except that the optimization brief itself identifies the September 26 snapshot. The branch was checked again and still pointed to that commit. `U` sources are primary upstream implementations/documentation. Paths and version identifiers are supplied so the claims are auditable independently of this chat.

| ID | Source |
|---|---|
| R1 | `docs/OPTIMIZATION_BRIEF.md` |
| R2 | `PREREGISTRATION.md` |
| R3 | `src/zcosmo/pyscf_cosmo_v2.py` |
| R4 | `src/zcosmo/pyscf_cosmo.py` |
| R5 | `.github/workflows/profiles_v2.yml` |
| R6 | `src/zcosmo/cosmosac.py` |
| R7 | `src/zcosmo/z0x.py` |
| R8 | `src/zcosmo/models.py`, `scripts/eval_models.sh` |
| R9 | `scripts/lle_parallel.py` |
| R10 | `cloud/s15/multi_mace.py` |
| R11 | `cloud/s15/bench15_core.py` |
| R12 | `cloud/s14/fast_md.py` |
| R13 | `cloud/s14/bench11_core.py` |
| R14 | `cloud/s14/zc_md.py` |
| R15 | `src/zcosmo/evaluate.py` |
| R16 | `scripts/validate_pyscf_profiles_v2.py` |
| R17 | `data/pyscf_sigma/validation_set.csv` |
| R18 | `results/pyscf_profile_validation.csv` — historical fixture keys/temperatures |
| R19 | `cloud/s15/modal_bench15.py` — actual 15+13 grids and deployment |
| U1 | PySCF **v2.14.0**, `pyscf/solvent/pcm.py`, especially `PCM._get_vind` |
| U2 | PySCF **v2.14.0**, `pyscf/geomopt/berny_solver.py` and `geometric_solver.py` |
| U3 | geomeTRIC “How It Works,” coordinate systems, optimization and stopping tests |
| U4 | PyMBAR `timeseries` documentation: equilibration and statistical inefficiency |
| U5 | PySCF `scf.hf.SCF_Scanner` implementation and SCF documentation |
| U6 | PySCF “GPU Acceleration (GPU4PySCF)” documentation |
| U7 | Inspected GPU4PySCF `gpu4pyscf/solvent/pcm.py`, blob `41248b7c3036ce6a6689c69d1bfd5c69c13e4633`; capability evidence, **not a pinned benchmark environment** |

```text
Repository source prefix:
https://github.com/Victor-Liang-ChE/zcosmo/blob/62172c7e7bb59737d28b115b9ef37311a98bb6cc/

Pinned upstream implementations:
https://github.com/pyscf/pyscf/blob/v2.14.0/pyscf/solvent/pcm.py
https://github.com/pyscf/pyscf/blob/v2.14.0/pyscf/geomopt/berny_solver.py
https://github.com/pyscf/pyscf/blob/v2.14.0/pyscf/geomopt/geometric_solver.py
https://github.com/pyscf/pyscf/blob/v2.14.0/pyscf/scf/hf.py

Primary documentation:
https://geometric.readthedocs.io/en/latest/how-it-works.html
https://pymbar.readthedocs.io/en/stable/timeseries.html
https://pyscf.org/user/gpu.html
```

**Bottom line:** P1 targets verified wasted quantum work; P4 tests the likely dominant statistical opportunity without hiding finite-step bias; P3 has the strongest local measured speed-up; and P5 is a controlled optimizer experiment rather than a promise that changing optimizers preserves a conformer. Apply independent patches, preserve the failed cases, and promote only what passes its declared gate.
