# Z-COSMO round 2: post-P9 costs, restart fidelity, and silent LLE failures

Reference: `Victor-Liang-ChE/zcosmo`, `main` at `eab6c2510264f7f3cf4db00cd1c247ad71500b14`. All implementation diffs below independently target this reference. The September 29 addendum governs the questions; the subsequent registrations through October 1 govern what is already accepted or rejected. Source references are collected at the end.

**Decision:** measure the post-P9 residual cost before assigning another large whole-QC speed-up. The strongest new per-cycle candidates are removal of the PCM gradient's auxiliary-center integral pass and materialization of the existing DF-J tensor within each geometry. The outstanding chains need a separate convergence diagnosis: state persistence is already deployed as an accepted A-class change, and the latest records identify an on-sphere stall at very small gradients. Repeating the rejected TRIC pre-stage is not the next experiment. [S1–S5]

**Execution record.** I verified the Git blob hashes of every existing file modified by these diffs, applied each patch independently in a local test tree, compiled the resulting Python, and ran the supplied portable algebra/control-flow tests. The gradient contraction test differed by at most `9.094947017729282e-13` on synthetic tensors. The LLE tests used the actual SciPy `fsolve` on ideal and regular-solution models, plus explicit failure injections. They confirmed unchanged return values and model-call sequences when auditing is enabled.

**Not executed:** a native PySCF calculation, a post-P9 molecular timing, GPU inference, the 25-molecule gate, or a full scorecard. PySCF and pyberny were absent; an attempted installation of `pyscf==2.14.0 pyberny==0.7.0` returned “No matching distribution found” from this runtime's resolver. That is an environment limitation, not a claim that the releases do not exist. Consequently, these are source-checked implementation candidates, not native-API-certified implementations. The native commands below are required before adoption. In particular, no synthetic test is presented as having satisfied the prompt's actual-PySCF requirement.

## What the newer evidence changes

P1's measured whole-profile improvement is **1.02×**, not my round-1 estimate of 1.6–3×. Keep its exact algebra but do not use its isolated linear-algebra microbenchmark as a QC forecast. P3's measured evaluator gain is 4.5×. P9's paired 25-molecule result is 6,009 to 3,183 seconds, or **1.888×**, with 168 gradient evaluations in both arms. These are your recorded measurements, not new runs here. [S1, S2, S3]

P6 is already registered, checked, and merged. Its interior derivative matched the prescribed Richardson reference to `2.0e-6` on 250 finite queries. There is no reason to append another prospective P6 registration after its results are known. Preserve the original scores and the separately reported corrected scores, including LLE balanced accuracy 0.901 to 0.894. [S3]

Optimizer persistence is also already implemented. The replacement gate recorded 40 evaluations uninterrupted, 50 with state restoration, and 60 with geometry-only restoration over the four final test molecules. The accepted gain over geometry-only restart is `60/50 = 1.20` in **evaluation count**, not a measured 1.20× wall-time guarantee. Its raw-bin E gate failed, and its A-class acceptance on ln gamma remains the correct classification. The code comment calling this branch E is stale. [S3, S4]

The latest registration records **630/636 primary profiles**, six outstanding Berny-converged profiles, and one separately flagged S1 acceptance. That supersedes the prompt's earlier count of 15 missing profiles. At this reference, the prompt's `data/pyscf_sigma/v2_missing.csv` and `cloud/s19/p9.patch` paths returned Not Found. I used the merged P9 implementation and the later registrations rather than inventing their contents. [S3, S5]

## Ranked proposals

E below means an equivalence **candidate**, pending native and full-profile gates. A changes the numerical trajectory and needs the stated prospective acceptance. H2 is shared instrumentation. P14 is an observability prerequisite, rather than a claimed acceleration.

The priority score is explicitly hypothetical: `affected upcoming hours × saved fraction × probability / effort`. To make the ordering reproducible, use 100 future QC hours, including 40 stall-affected hours and 10 short-restart-affected hours. These overlapping budgets are not observed allocations and savings must not be added. Effort units and probabilities are engineering judgments. Replace them with your actual work mix after the first native results.

| Rank | ID | Target | Class | Conditional performance estimate | Planning arithmetic | Effort | Priority score |
|---:|---|---|:---:|---|---|---:|---:|
| 1 | P10 | PCM gradient: one `ip1` pass instead of `ip1` plus `ip2` | E | Roughly 1.03–1.10× QC if the removable pass is 3–9% of post-P9 wall time | `100 × (1−1/1.06) × .85 / 1` | 1 | 4.81 |
| 2 | P11 | DF-J: materialize the same tensor once per geometry | E | Roughly 1.04–1.15× if repeated direct-J integrals remain material; may lose when disk-bound | `100 × (1−1/1.10) × .60 / 2` | 2 | 2.73 |
| 3 | P15 | Fixed noise-aware Berny trust-update trial | A | No defensible measured speed-up on a nonterminating reference; planning scenario saves half the stall budget | `40 × .50 × .25 / 2` | 2 | 2.50 |
| 4 | P13 | Ordered parallel construction of P9's cached surface block | E | Can be slower; 1.00–1.07× overall is a test hypothesis, not a fourfold forecast | `100 × (1−1/1.04) × .30 / 2` | 2 | 0.58 |
| 5 | P12 | Complete pre-send checkpoint with quantum-result replay and orbital state | E* | Short-cap gate could remove 10 repeated calls: `50/40 = 1.25`; 300-step passes give a much smaller ceiling | `10 × .20 × .60 / 5` | 5 | 0.24 |
| Prerequisite | P14 | LLE diagnostic sidecar without changing predictions | E | Approximately 1× or slightly slower; no speed claim | Correctness/coverage evidence | 1 | Not scored |
| Prerequisite | H2 | Native profiling and gates, portable tests | E instrumentation | Profiling adds overhead; do not time production under the profiler | Measurement | Shared | Not scored |

`E*`: P12's recovery target is the uninterrupted registered CPU algorithm. It does **not** retroactively turn the accepted A restart into E. Before replacing existing A-produced outputs, compare against those outputs as well. A difference outside the E gate must remain a recorded A numerical correction, even when the new run reproduces the uninterrupted reference.

P10/P11/P13 modify the same module. P12/P15 modify the geometry runner. Test independently first. Their gains are not multiplicative without a combined run and a repeated E gate.

## Common setup and acceptance

Use one already working CPU environment for both arms. For the state and trust-update trials, pyberny is explicitly pinned to **0.7.0** because the inspected restart representation is that version's dataclass. The production workflow currently pins PySCF but leaves pyberny unpinned. Do not silently upgrade a production environment or reuse a pickled optimizer across package versions. Record the environment once and keep it unchanged for the pair. [S8, U3]

A separate trial environment can be provisioned with the following commands. They are installation instructions, not a claim that installation succeeded here.

```bash
python3.11 -m venv .venv-r2
source .venv-r2/bin/activate
python -m pip install 'pyscf==2.14.0' 'pyberny==0.7.0' \
  rdkit tblite ase pandas scipy matplotlib threadpoolctl
python -m pip freeze > r2-environment.txt
```

Save this report locally, set `REPORT`, and extract its seven patches. The corrected repository H0 is used, not the original round-1 attachment. Generated outputs stay outside the shared input assets.

```bash
set -euo pipefail
export REPO="$PWD"
export BASE=eab6c2510264f7f3cf4db00cd1c247ad71500b14
export REPORT="${REPORT:-$REPO/ZCOSMO_ROUND2_REPORT.md}"
export WORK="$(mktemp -d "${TMPDIR:-/tmp}/zcosmo-r2.XXXXXX")"
export PATCHES="$WORK/patches"
mkdir -p "$PATCHES" "$WORK/postP9" "$WORK/checks"
python - "$REPORT" "$PATCHES" <<'PYCODE'
from pathlib import Path
import re, sys
blocks = re.findall(r'<!-- PATCH:(H2|P1[0-5]) -->\s*```diff\n(.*?)\n```',
                    Path(sys.argv[1]).read_text(), re.S)
assert len(blocks) == 7 and len({k for k,_ in blocks}) == 7
for key, text in blocks:
    Path(sys.argv[2], key+'.patch').write_text(text+'\n')
PYCODE
make_tree () {
  local id="$1" tree="$WORK/$1"
  git -C "$REPO" worktree add --detach "$tree" "$BASE"
  for asset in data results; do
    test -d "$REPO/$asset"
    if test -e "$tree/$asset"; then mv "$tree/$asset" "$tree/$asset.pinned-copy"; fi
    ln -s "$REPO/$asset" "$tree/$asset"
  done
  git -C "$tree" apply --check "$PATCHES/H2.patch"
  git -C "$tree" apply "$PATCHES/H2.patch"
  if ! test -f "$tree/scripts/optimization_check.py"; then
    git -C "$tree" apply --check docs/astra/round1/patches/H0.patch
    git -C "$tree" apply docs/astra/round1/patches/H0.patch
  fi
  if test "$id" != base; then
    git -C "$tree" apply --check "$PATCHES/$id.patch"
    git -C "$tree" apply "$PATCHES/$id.patch"
  fi
}
make_tree base
export PYTHONPATH=src OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1
export QC_MEM_MB=10000 ZC_PCM3C=1 ZC_PCM3C_MB=4000
export ZC_BERNY_STATE=0 ZC_BERNY_REPLAY=0
unset ZC_MAXSTEPS ZC_BERNY_NOISE_EH ZC_PCM_GRAD1 ZC_DF_STORE ZC_PCM3C_WORKERS ZC_TRIC_PREOPT
python -m pip freeze > "$WORK/environment.txt"
```

The memory values reproduce the intended 4-core trial configuration, but are not a hard process-memory limit. Reduce both arms' budgets together on smaller machines and record the change. In particular, a 4 GB P9 cache can coexist with a large gradient temporary and a second DF tensor.

The E profile gate remains: all 25 molecules and the same 2,302 historical row occurrences; identical finite coverage; maximum normalized-bin difference below `1e-4`; maximum **raw stored psigmaA-bin** difference below `1e-4`; maximum finite ln gamma-infinity difference below `1e-3`. The corrected H0 reports the 31 baseline-nonfinite rows rather than turning them into zeros or dropping mismatches. It is not permissible to silently switch the raw-bin criterion to a relative one. [S9]

Compute the fresh reference once per fixed environment. `qc` must succeed, not merely leave some files behind.

```bash
(cd "$WORK/base"; python scripts/optimization_check.py qc --out "$WORK/qc-reference")
profile_gate () {
  local id="$1" flag="$2" value="$3"
  (cd "$WORK/$id"
   env "$flag=$value" python scripts/optimization_check.py qc --out "$WORK/qc-$id"
   env "$flag=$value" python scripts/optimization_check.py profiles \
     --reference "$WORK/qc-reference" --candidate "$WORK/qc-$id" \
     --mode E --out "$WORK/checks/$id-profiles.json")
}
```

The per-proposal commands below assume this setup. For an initial screening run, do the inexpensive portable and fixed-geometry checks before generating the 25 candidates.

## Post-P9 measurement: what can and cannot be concluded now

The fetched `results/qc/qc_profile/` directory contains the four earlier 2-thread/4-thread summaries, not a post-P9 breakdown. The octanol file explicitly shows the old `pcm.py:_get_v` and `_get_vmat`. Therefore **the next-largest measured post-P9 component is not established by the available files**. [S7]

The old profile still identifies useful candidates. Octanol spent 41.6 seconds under SCF `nr_rks`, 18.6 under PCM `grad_qv`, and 18.2 under the direct DF-J path. These are surviving categories, not new timings. The 100 seconds in `aux_e2` includes calls from more than one caller, including derivatives. The 149.7 seconds under solvent-attached `get_veff` also contains the underlying gas-phase Fock build. Neither is an exclusive PCM-only bucket. Subtracting 100 from 197.5 and declaring the remainder the new runtime would be incorrect. [S7]

H2 records inclusive timers, exclusive time relative to instrumented children, SCF iteration counts, actual geometry evaluations, resolved auxiliary basis, cache allocation, CPU time/wall time, and full profiler paths. Its verbose logger/cProfile run is diagnostic; the quiet full-profile comparison supplies the end-to-end timing. It also prevents `ZC_MAXSTEPS=300` from silently overriding a requested three-cycle trace, and it accepts only the runner's specific iteration-cap error as an expected stop.

```bash
(cd "$WORK/base"
 python scripts/round2_check.py trace --smiles CCCCCCCCO --cycles 3 \
   --out "$WORK/postP9/octanol-t4" > "$WORK/postP9/octanol-t4.log" 2>&1
 for t in 1 2; do
   OMP_NUM_THREADS="$t" python scripts/round2_check.py trace \
     --xyz "$WORK/postP9/octanol-t4/start.json" --cycles 3 \
     --out "$WORK/postP9/octanol-t$t" > "$WORK/postP9/octanol-t$t.log" 2>&1
 done
 python scripts/round2_check.py trace --smiles 'C(CCCCCC)CCC(=O)O' --cycles 3 \
   --out "$WORK/postP9/decanoic-t4" > "$WORK/postP9/decanoic-t4.log" 2>&1
 python scripts/round2_check.py trace \
   --xyz cloud/s19/seeds/FLIACVVOZYBSBS-UHFFFAOYSA-N.partial.json \
   --use-state --cycles 3 --out "$WORK/postP9/stalled-state" \
   > "$WORK/postP9/stalled-state.log" 2>&1)
```

The last command reads a trusted committed legacy optimizer checkpoint, copies it into the output directory, and profiles the accepted A restart without altering the committed seed. It exposes the pre-send trust radius and previous predicted energy change. It is a different experiment from creating a new Hessian at that geometry.

Repeat the 4-thread octanol run once with BLAS also at four threads, then compare quiet timings before choosing settings. The `getints3c` driver already contains an OpenMP parallel region and a dynamic work-sharing loop. cProfile self time around a C call includes elapsed time while native threads run; it cannot prove serial execution. Oversubscription, CPU quota, the native OpenMP runtime, shell scheduling, and memory traffic are competing explanations. The new CPU/wall and threadpool metadata discriminate some of them; the old summaries do not. [U4]

```bash
(cd "$WORK/base"
 OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4 BLIS_NUM_THREADS=4 \
 python scripts/round2_check.py trace --xyz "$WORK/postP9/octanol-t4/start.json" \
   --cycles 3 --out "$WORK/postP9/octanol-t4-blas4" \
   > "$WORK/postP9/octanol-t4-blas4.log" 2>&1)
```

There is another size-dependent issue: P9 caches only the first budget-sized surface block. Later blocks are recomputed in both contractions. For an illustrative 600-AO/6,000-point case, packed storage is `8 × 600 × 601/2 × 6000 = 8.6544 GB`. A 4 GB cache holds only about 46.2% of that tensor. Thus the medium molecule and an outstanding long chain can have different residual bottlenecks. H2 reports both allocated and required cache bytes; do not rank XC above remaining surface integrals without checking this ratio. [S5]

## P10, E candidate: remove the second PCM gradient integral pass

Target: `src/zcosmo/pcm_lu.py`, `CachedPCM3c.grad` and `_grad_qv_onepass`.

The pinned `grad_qv` evaluates `int3c2e_ip1` and `int3c2e_ip2` separately. At fixed Gaussian exponents, translational invariance gives

\[
B^\alpha_{ijP} = -A^\alpha_{ijP}-A^\alpha_{jiP},
\]

where A is the derivative associated with the first AO center and B with the auxiliary center. Consequently,

\[
\sum_{ij}B^\alpha_{ijP}D_{ij}q_P
=-\sum_{ij}A^\alpha_{ijP}(D_{ij}+D_{ji})q_P.
\]

This eliminates the separate `ip2` integral evaluation. The AO-center contraction, nuclear term, and PCM surface/solver derivative remain. No density-fitting approximation, grid, radius, basis, SCF tolerance, or optimizer criterion changes. The solvent gradient wrapper spin-sums the UKS density before invoking `PCM.grad`, matching the proposed real two-dimensional input contract. [U1]

The speed ceiling is the removed pass, not the entire PCM gradient. If that pass occupies fraction f of post-P9 wall time and costs nearly disappear, `S ≈ 1/(1−f)`. At f=.03 and .09, this is 1.031× and 1.099×. The old 18.6-second `grad_qv` total is not a measurement of its `ip2` share, and the new density contraction still costs time.

The native check first verifies the **integral-level identity**, then compares complete energies, gradients and q at both basis levels for water/RKS and oxygen/UKS. The 25-profile gate is still mandatory because tiny gradient differences can alter a finite optimizer trajectory. The portable test only verified the contraction and block summation, not libcint's derivative convention.

<!-- PATCH:P10 -->
```diff
--- a/src/zcosmo/pcm_lu.py
+++ b/src/zcosmo/pcm_lu.py
@@ -52,6 +52,13 @@
 
 
 class CachedPCM3c(CachedPCM):
+    def grad(self, dm):
+        if os.environ.get("ZC_PCM_GRAD1", "0") != "1":
+            return super().grad(dm)
+        from pyscf.solvent.grad.pcm import grad_nuc, grad_solver
+        return (_grad_qv_onepass(self, dm) + grad_nuc(self, dm)
+                + grad_solver(self, dm))
+
     def _zc_blocks(self):
         it = self._intermediates if self._intermediates is not None else {}
         grid = self.surface["grid_coords"]
@@ -117,3 +124,46 @@
     new.__dict__.update(mf.with_solvent.__dict__)
     mf.with_solvent = new
     return mf
+
+
+def _grad_qv_onepass(pcmobj, dm):
+    """PySCF 2.14.0 grad_qv, deriving the auxiliary-center term from ip1.
+
+    At fixed Gaussian exponents, ip2[i,j,k] = -ip1[i,j,k]-ip1[j,i,k].
+    All surface-shape and nuclear terms remain in the upstream functions.
+    """
+    from pyscf.lib import logger
+    if not pcmobj._intermediates:
+        pcmobj.build()
+    dm = np.asarray(dm)
+    if dm.ndim != 2 or np.iscomplexobj(dm):
+        raise ValueError("Expected the real spin-summed ground-state density")
+    old = pcmobj._intermediates.get("dm")
+    if old is None or np.linalg.norm(old - dm) >= 1e-10:
+        pcmobj._get_vind(dm)
+    mol = pcmobj.mol
+    t0 = logger.process_clock(), logger.perf_counter()
+    surf = pcmobj.surface
+    q = pcmobj._intermediates["q_sym"]
+    ng, nao = len(q), mol.nao
+    memory = pcmobj.max_memory - lib.current_memory()[0]
+    # Keep the registered driver's ip1 block partition and summation order.
+    block = int(max(memory * .9e6 / 8 / nao**2 / 3, 400))
+    intor = mol._add_suffix("int3c2e_ip1")
+    opt = gto.moleintor.make_cintopt(mol._atm, mol._bas, mol._env, intor)
+    dvj = np.zeros((3, nao)); dq = np.empty((3, ng))
+    dsym = dm + dm.T
+    for lo, hi in lib.prange(0, ng, block):
+        aux = gto.fakemol_for_charges(surf["grid_coords"][lo:hi],
+                                    expnt=surf["charge_exp"][lo:hi]**2)
+        aux.cart = mol.cart
+        a = df.incore.aux_e2(mol, aux, intor=intor, aosym="s1", cintopt=opt)
+        dvj += np.einsum("xijk,ij,k->xi", a, dm, q[lo:hi])
+        dq[:, lo:hi] = -np.einsum("xijk,ij,k->xk", a, dsym, q[lo:hi])
+        del a
+    solute = 2 * np.asarray([dvj[:, lo:hi].sum(axis=1)
+                             for lo, hi in mol.aoslice_by_atom()[:, 2:]])
+    surface = np.asarray([dq[:, lo:hi].sum(axis=1)
+                          for lo, hi in surf["gslice_by_atom"]])
+    logger.new_logger(mol).timer_debug1("R2 ip1-only grad_qv", *t0)
+    return solute + surface
```

```bash
make_tree P10
(cd "$WORK/P10"
 python scripts/round2_logic.py P10 --out "$WORK/checks/P10-portable.json"
 python scripts/round2_check.py fixed --flag ZC_PCM_GRAD1 --identity \
   --out "$WORK/checks/P10-fixed.json"
 ZC_PCM3C_MB=0.05 python scripts/round2_check.py fixed --flag ZC_PCM_GRAD1 --identity \
   --out "$WORK/checks/P10-partial-cache.json"
 ZC_PCM_GRAD1=1 python scripts/round2_check.py trace \
   --xyz "$WORK/postP9/octanol-t4/start.json" --cycles 3 \
   --out "$WORK/postP9/P10" > "$WORK/postP9/P10.log" 2>&1)
profile_gate P10 ZC_PCM_GRAD1 1
```

Reject on any identity, surface-order, E/G/q, finite-coverage, or profile-gate failure. A fixed-geometry pass alone is not adoption.

## P11, E candidate: stop taking the direct-J route on every SCF iteration

Target: `src/zcosmo/pcm_lu.py`, `StoredJDF.get_jk` and `_store_j_tensor`.

For this nonhybrid functional, PySCF's DF driver takes a direct-J path when K is not requested and `_cderi` has not been built. That path remains visible in the old profile. The proposal explicitly calls the existing DF tensor builder once per geometry, then uses the existing stored-tensor J contraction. It retains the same automatically resolved auxiliary basis and the native RAM/HDF5 storage decision. `DF.reset(mol)` clears `_cderi`, so no tensor or metric is carried over an atomic displacement. [U5]

For I SCF J evaluations, compare `I × t_direct` with `t_build + I × t_contract`. For example, I=10, `t_direct=1.5 s`, `t_build=4 s`, and `t_contract=.15 s` gives 15 versus 5.5 seconds, or 2.73× **for J only**. If J is 15% of post-P9 wall time, the corresponding whole-cycle factor is `1/(.85 + .15/2.73) = 1.105`. These are illustrative inputs to measure, not new timings. Disk I/O or a small SCF iteration count can eliminate the benefit.

This changes the integral-evaluation route and floating-point accumulation, so it is an E candidate rather than a claim of bitwise identity. Do not use `mol.incore_anyway` to force an oversized allocation. A 1,000-auxiliary/300-AO packed tensor alone is about 361 MB, in addition to the P9 surface cache. Report peak resident memory and whether DF chose disk storage.

<!-- PATCH:P11 -->
```diff
--- a/src/zcosmo/pcm_lu.py
+++ b/src/zcosmo/pcm_lu.py
@@ -40,6 +40,8 @@
     new = CachedPCM(old.mol)
     new.__dict__.update(old.__dict__)
     mf.with_solvent = new
+    if os.environ.get("ZC_DF_STORE", "0") == "1":
+        mf = _store_j_tensor(mf)
     return mf
 
 
@@ -117,3 +119,27 @@
     new.__dict__.update(mf.with_solvent.__dict__)
     mf.with_solvent = new
     return mf
+
+
+class StoredJDF(df.DF):
+    """Materialize the same auxiliary-basis tensor once per molecular geometry.
+
+    DF.reset clears _cderi. DF.build retains its native RAM/HDF5 decision;
+    never set mol.incore_anyway or carry the tensor over a geometry change.
+    """
+    def get_jk(self, dm, hermi=1, with_j=True, with_k=True,
+               direct_scf_tol=1e-13, omega=None):
+        if omega is None and with_j and not with_k and self._cderi is None:
+            self.build()
+        return super().get_jk(dm, hermi=hermi, with_j=with_j, with_k=with_k,
+                              direct_scf_tol=direct_scf_tol, omega=omega)
+
+
+def _store_j_tensor(mf):
+    old = mf.with_df
+    if type(old) is not df.DF:
+        raise TypeError("R2 stored-J trial requires the unmodified CPU DF class")
+    new = StoredJDF(old.mol, auxbasis=old.auxbasis)
+    new.__dict__.update(old.__dict__)
+    mf.with_df = new
+    return mf
```

```bash
make_tree P11
(cd "$WORK/P11"
 python scripts/round2_logic.py P11 --out "$WORK/checks/P11-portable.json"
 python scripts/round2_check.py fixed --flag ZC_DF_STORE --out "$WORK/checks/P11-fixed.json"
 ZC_DF_STORE=1 python scripts/round2_check.py trace \
   --xyz "$WORK/postP9/octanol-t4/start.json" --cycles 3 \
   --out "$WORK/postP9/P11" > "$WORK/postP9/P11.log" 2>&1)
profile_gate P11 ZC_DF_STORE 1
```

The fixed check also covers the DF-gradient code using the substituted DF subclass. Its compatibility with the actual native installation is not established by the portable subclass test.

## P15, A: a single noise-aware trust-update trial, not relaxed convergence

Target: `src/zcosmo/pyscf_cosmo_v2.py`, `dft_geometry`; prospective registration text in `docs/astra/round2/P15_PREREGISTRATION.md`.

In the inspected pyberny 0.7.0 source, `energy_noise` defaults to `2e-8 Eh`. When the magnitude of the **predicted** energy change is below ten times that value, the trust-update routine avoids the ordinary actual/predicted energy ratio and can enlarge a boundary-limited trust radius. The candidate changes only this optimizer parameter to `2e-7 Eh`, including the parameter stored in a restored state. Passing a new keyword alone is insufficient: Berny's restart constructor restores the old parameter object and ignores the fresh keyword overrides. [U3]

This directly targets the reported small-gradient/on-sphere failure mechanism while keeping the original Berny convergence test. It does not declare a stalled geometry converged. It is A because its trajectory can differ, and an observed energy change of `1e-7 Eh` is not itself a measured SCF noise estimate. If the trace already shows predicted changes below `2e-7 Eh`, the old noise branch is already active; changing the setting may do nothing. If they exceed `2e-6 Eh`, both settings use the usual ratio. The potentially different branch lies between those bounds.

There is no legitimate finite time-to-convergence speed-up for a reference that has not converged. The trial's fixed budget and success count decide usefulness. The planning score assumes half of the stall budget could be avoided; that is explicitly a speculative allocation, not an observed speed-up.

The included registration requires unchanged finite coverage, all 25 validation molecules converged under the original test, max change in finite ln gamma-infinity below .01 against current main, median difference against UD below .15, and no more than 10% paired wall-time regression on the 25. It separately caps the six frozen long-chain trials at 100 new gradient evaluations each. Candidate profiles remain outside the primary profile directory. Nothing in this proposal changes the already-failed S1 or fallback tests.

<!-- PATCH:P15 -->
```diff
--- a/src/zcosmo/pyscf_cosmo_v2.py
+++ b/src/zcosmo/pyscf_cosmo_v2.py
@@ -27,7 +27,8 @@
                     ("pyscf_cosmo.py", "pyscf_cosmo_v2.py", "pcm_lu.py") if (here / name).exists())
     packages = [(name, version(name)) for name in ("pyscf", "pyberny", "rdkit", "tblite", "ase", "numpy", "scipy")]
     return hashlib.sha256(code + json.dumps(packages).encode()
-                          + os.environ.get("ZC_TRIC_PREOPT", "0").encode()).hexdigest()
+                          + os.environ.get("ZC_TRIC_PREOPT", "0").encode()
+                          + os.environ.get("ZC_BERNY_NOISE_EH", "").encode()).hexdigest()
 
 
 def dft_geometry(sym, xyz_A, basis="def2-svp", maxsteps=100, partial=None, spin=0):
@@ -71,6 +72,16 @@
                 kw["restart"] = st
         except Exception:
             kw = {}
+    noise = os.environ.get("ZC_BERNY_NOISE_EH")
+    if noise:
+        from importlib.metadata import version
+        from dataclasses import replace
+        if version("pyberny") != "0.7.0" or float(noise) != 2e-7:
+            raise ValueError("R2 A-trial is fixed at pyberny 0.7.0, energy_noise=2e-7 Eh")
+        kw["energy_noise"] = 2e-7
+        if "restart" in kw:
+            # Berny ignores keyword parameters when restart is supplied.
+            kw["restart"]["params"] = replace(kw["restart"]["params"], energy_noise=2e-7)
     def cb(env):
         if partial is not None and env.get("mol") is not None:
             tmp = str(partial) + ".tmp"
@@ -134,6 +145,8 @@
         out, meta = to_profiles(sym, x, seg)
         meta["E_scf_Eh"] = e
         meta["geometry_converged"] = True
+        if os.environ.get("ZC_BERNY_NOISE_EH"):
+            meta["geometry_protocol"] = "A-R2-noise-aware-trust-2e-7-Eh"
         meta["profile_revision"] = profile_revision()
         meta["source"] = "pyscf_cosmo_v2 BP86/def2-SVP conductor geometry; BP86/def2-TZVP conductor profile"
         meta["geometry"] = "BP86/def2-SVP C-PCM conductor (pyberny)" + (" [resumed from checkpoint]" if resumed else "")
--- /dev/null
+++ b/docs/astra/round2/P15_PREREGISTRATION.md
@@ -0,0 +1,26 @@
+
+## Proposed R2 noise-aware Berny trial, class A
+
+Register this text with its actual commit timestamp before any trial profile or
+score is read. This trial is motivated by the previously observed stalls, so it
+is not a blind discovery. Pyberny is fixed at 0.7.0. Its energy_noise parameter is
+set to 2e-7 Eh, including in a restored BernyState; every energy, gradient, basis,
+auxiliary basis, XC grid and PCM setting is unchanged. The original Berny
+convergence criteria, including the on-sphere condition, remain mandatory.
+No experimental response selects this value. There is one candidate, no sweep.
+
+The comparison uses the historical 25-molecule/2302-row manifest, with identical
+finite coverage. All 25 candidates must pass the original Berny test; maximum
+absolute change in COSMO-SAC-dsp ln gamma-infinity against current-main profiles
+must be below 0.01; the median absolute difference against UD must remain below
+0.15. Report both normalized distributions and raw psigmaA bins, without
+reinterpreting either existing E or fallback limit. Paired total wall time on
+the 25 molecules must be no more than 1.10 times reference. Separately freeze and
+hash the six current long-chain geometries before the trial. Run at most 100 new
+CPU gradient evaluations per chain, from the same geometry and optimizer state
+in each arm, with the same already-accepted A-class restart protocol. At least
+one formerly stalled chain must newly pass the original Berny test within that
+budget, and all resulting profiles remain exploratory until the 25-molecule
+checks pass. An unfinished arm is censored, not assigned an invented time to
+convergence. No S1 failure is reclassified by this trial. Rejection leaves the
+accepted GPU-prestage and A-class restart protocols unchanged.
```

```bash
make_tree P15
# Record/commit the prospective registration before reading any P15 trial output.
(cd "$WORK/P15"
 cat docs/astra/round2/P15_PREREGISTRATION.md >> PREREGISTRATION.md
 python scripts/round2_logic.py P15 --out "$WORK/checks/P15-portable.json"
 ZC_BERNY_NOISE_EH=2e-7 python scripts/optimization_check.py qc --out "$WORK/qc-P15"
 python scripts/optimization_check.py profiles --reference "$WORK/qc-reference" \
   --candidate "$WORK/qc-P15" --mode A --out "$WORK/checks/P15-profiles.json")
python - "$WORK" <<'PYCODE'
import json, pathlib, sys
w=pathlib.Path(sys.argv[1]); p=json.loads((w/'checks/P15-profiles.json').read_text())
r=json.loads((w/'qc-reference/timing.json').read_text())
c=json.loads((w/'qc-P15/timing.json').read_text())
assert p['max_delta_lngamma'] < .01
assert c['wall_s'] <= 1.10*r['wall_s']
print('P15 validation gates pass; long-chain budget experiment remains separate')
PYCODE
```

For the long-chain arm, copy each frozen checkpoint pair to an output directory, never modify the seed in place. This command targets the six recorded prefixes without assuming the unspecified suffixes. It also writes a seed-hash manifest before running anything.

```bash
python - "$REPO" "$WORK" <<'PYCODE'
from pathlib import Path
import hashlib, json, shutil, sys
repo,work=map(Path,sys.argv[1:]); prefixes=['BTFJIXJJCS','FLIACVVOZY','HPEUJPJOZX','MVLVMROFTA','OYHQOLUKZR','PYGXAGIECV']
manifest={}; keys=[]
for prefix in prefixes:
    matches=list((repo/'cloud/s19/seeds').glob(prefix+'*.partial.json'))
    assert len(matches)==1,(prefix,matches)
    geometry=matches[0]; key=geometry.name.removesuffix('.partial.json'); keys.append(key)
    state=Path(str(geometry)+'.bstate'); assert state.is_file(), state
    for source in [geometry,state]:
        manifest[source.name]=hashlib.sha256(source.read_bytes()).hexdigest()
        for arm in ['base','P15']:
            dest=work/'long'/arm;dest.mkdir(parents=True,exist_ok=True)
            shutil.copy2(source,dest/source.name)
(work/'long/seed-sha256.json').write_text(json.dumps(manifest,indent=2))
(work/'long/keys.txt').write_text(','.join(keys))
PYCODE
for arm in base P15; do
  noise=''; test "$arm" = base || noise=2e-7
  (cd "$WORK/$arm"
   set +e
   ZC_BERNY_STATE=1 ZC_MAXSTEPS=100 ZC_BERNY_NOISE_EH="$noise" \
   python -u -m zcosmo.pyscf_cosmo_v2 "$WORK/long/$arm" data/benchmark/compounds.csv \
     --keys "$(cat "$WORK/long/keys.txt")" > "$WORK/long/$arm.log" 2>&1
   printf '%s\n' "$?" > "$WORK/long/$arm.exit")
done
```

An exit status from an unfinished chain is not acceptance. Examine each per-molecule status: a Berny cap is censored; an SCF exception or other error is a failed trial. Require at least one newly Berny-converged chain, with all the prior validation gates passed, before calling the trial useful. Do not move any candidate into `profiles_v2` automatically.

## P13, E candidate: disjoint surface blocks with bounded worker scratch

Target: `src/zcosmo/pcm_lu.py`, `CachedPCM3c._zc_blocks` and `_parallel_surface_3c`.

The new option parallelizes only construction of P9's retained surface block. Each worker owns its fake-charge molecule and integral optimizer, runs one native OpenMP thread, and writes a disjoint fixed slice of the final tensor. The contraction happens later in the original column order. Uncached tail blocks retain the current path. It neither constructs separate molecular systems nor distributes an SCF density update across processes.

This is a test of scheduling granularity, not a claim that libcint is serial. On a four-core runner, four Python workers each launching four OpenMP workers is the wrong experiment. The worker initializer sets its OpenMP task's thread-count control variable to one; the main thread's setting is left alone. Native thread-local behavior and thread safety still require the actual PySCF run. The portable test exercised only a mock of that contract. [U4]

The final cache is preallocated in its original order. Additional worker output scratch is targeted at 128 MiB in aggregate for the molecular sizes here; libcint's own buffers and the retained cache are additional memory. For a fraction f=.05 of cycle time in cached-block construction and a component improvement of 2×, the whole-cycle gain is only `1/(.95+.05/2)=1.026`. If construction is already efficiently parallel, extra scheduling and copies can be slower. Reject unless the measured retained-block construction improves and quiet end-to-end QC is not slower.

<!-- PATCH:P13 -->
```diff
--- a/src/zcosmo/pcm_lu.py
+++ b/src/zcosmo/pcm_lu.py
@@ -73,7 +73,12 @@
                 blocks.append((p0, p1, None)); continue
             fm = gto.fakemol_for_charges(grid[p0:p1], expnt=exps[p0:p1] ** 2)
             fm.cart = mol.cart
-            blocks.append((p0, p1, df.incore.aux_e2(mol, fm, intor=int3c2e, aosym="s2ij", cintopt=cintopt)))
+            workers = int(os.environ.get("ZC_PCM3C_WORKERS", "1"))
+            if workers == 1:
+                v = df.incore.aux_e2(mol, fm, intor=int3c2e, aosym="s2ij", cintopt=cintopt)
+            else:
+                v = _parallel_surface_3c(mol, grid[p0:p1], exps[p0:p1], int3c2e, workers)
+            blocks.append((p0, p1, v))
         if self._intermediates is not None:
             self._intermediates["_zc_3c"] = (grid, blocks)
         return blocks
@@ -117,3 +122,38 @@
     new.__dict__.update(mf.with_solvent.__dict__)
     mf.with_solvent = new
     return mf
+
+
+def _parallel_surface_3c(mol, grid, exps, intor, workers):
+    """Disjoint, ordered surface columns; one native OpenMP thread per worker.
+
+    The main thread's OpenMP setting is left unchanged. Worker threads own
+    their optimizer and fake molecule. No reduction runs in completion order.
+    This is opt-in: the upstream driver already uses OpenMP.
+    """
+    from concurrent.futures import ThreadPoolExecutor
+    import threading
+    if workers not in (2, 4):
+        raise ValueError("ZC_PCM3C_WORKERS must be 1, 2 or 4")
+    if len(grid) == 0:
+        return np.empty((mol.nao * (mol.nao + 1)//2, 0))
+    npair = mol.nao * (mol.nao + 1)//2
+    # 128 MiB aggregate worker output scratch, in addition to the final cache.
+    cols = max(1, min(128, (128 * 1024**2)//(workers * 8 * npair)))
+    answer = np.empty((npair, len(grid)), order="F")
+    local = threading.local()
+    def init():
+        # omp_set_num_threads affects the calling worker's OpenMP ICV.
+        lib.num_threads(1)
+        local.opt = gto.moleintor.make_cintopt(mol._atm, mol._bas, mol._env, intor)
+    def compute(lo):
+        hi = min(len(grid), lo + cols)
+        fm = gto.fakemol_for_charges(grid[lo:hi], expnt=exps[lo:hi]**2)
+        fm.cart = mol.cart
+        block = df.incore.aux_e2(mol, fm, intor=intor, aosym="s2ij", cintopt=local.opt)
+        answer[:, lo:hi] = block
+        return None
+    with ThreadPoolExecutor(max_workers=workers, initializer=init) as pool:
+        for _ in pool.map(compute, range(0, len(grid), cols)):
+            pass
+    return answer
```

```bash
make_tree P13
(cd "$WORK/P13"
 python scripts/round2_logic.py P13 --out "$WORK/checks/P13-portable.json"
 python scripts/round2_check.py fixed --flag ZC_PCM3C_WORKERS --baseline 1 --value 4 \
   --out "$WORK/checks/P13-fixed.json"
 ZC_PCM3C_MB=0.05 python scripts/round2_check.py fixed \
   --flag ZC_PCM3C_WORKERS --baseline 1 --value 4 \
   --out "$WORK/checks/P13-partial-cache.json"
 ZC_PCM3C_WORKERS=4 python scripts/round2_check.py trace \
   --xyz "$WORK/postP9/octanol-t4/start.json" --cycles 3 \
   --out "$WORK/postP9/P13" > "$WORK/postP9/P13.log" 2>&1)
profile_gate P13 ZC_PCM3C_WORKERS 4
```

Do not remove the order check or loosen the profile tolerance to rescue a marginal threading gain. Also test two workers before choosing a deployment setting; choose by wall time under the same correctness gate, not by the number of workers.

## P12, E recovery candidate: checkpoint the pending quantum result and SCF state

Target: `src/zcosmo/pyscf_cosmo_v2.py`, `dft_geometry`/`run_one`, and new `src/zcosmo/berny_replay.py`.

The existing callback runs **before** `optimizer.send((energy, gradient))`. Its saved state is therefore a valid pre-send state. It is not correct to accuse that implementation of saving a post-update Hessian with a pre-update geometry. Its actual limitation is that the completed quantum result is absent, and the restarted SCF lacks the preceding orbital state. It repeats the pending evaluation, then continues from a slightly different finite-accuracy SCF result. Your measurements show the resulting trajectories are close but not E at the raw-bin criterion. [S3, S4, U2]

The new bundle stores that pre-send optimizer state together with its already computed energy/gradient and SCF orbitals. On resume, the actual upstream Berny loop requests the pending geometry; a scanner wrapper returns the stored result exactly once. Berny then executes its ordinary `send` update. Subsequent steps call the normal gradient scanner, with the previous orbitals restored so its existing density-matrix reuse is retained. No Hessian is converted between coordinate systems and no GFN2-xTB curvature is substituted.

A single versioned bundle is authoritative. Its human-readable JSON checkpoint is a mirror. This avoids treating two separately replaced files as one atomic transaction. Versions, inspected Berny source, settings and local driver hashes enter the compatibility fingerprint. Corruption or a fingerprint mismatch fails explicitly. Legacy bstate files do not establish this stronger contract; the candidate starts a new recovery chain from their geometry and warns. Only trusted owner-controlled artifacts may be loaded: a checksum does not make pickle safe for untrusted inputs.

The mathematical recovery argument assumes the same numerical environment and the inspected default scanner/DIIS behavior. Persistent custom DIIS objects are rejected. Cross-machine bitwise replay is not promised. The native four-molecule gate checks the entire actual-evaluation geometry/energy/gradient trace, not just a final geometry. It requires at least two forced restarts. The full 25-profile gate then decides E against the uninterrupted reference. Existing A-produced outputs must retain their classification and provenance.

The maximum useful saving is the repeated work actually removed. For the recorded artificial short-cap case, 50 calls could become 40, or 1.25× before serialization overhead. With a 300-evaluation pass, removing one replay costs only about `1/300` of the force evaluations, approximately 0.3%. This patch is principally about restart fidelity and provenance. It is not a cure for an already persistent on-sphere stall.

<!-- PATCH:P12 -->
```diff
--- a/src/zcosmo/pyscf_cosmo_v2.py
+++ b/src/zcosmo/pyscf_cosmo_v2.py
@@ -24,7 +24,7 @@
     from importlib.metadata import version
     here = Path(__file__).resolve().parent
     code = b"".join((here / name).read_bytes() for name in
-                    ("pyscf_cosmo.py", "pyscf_cosmo_v2.py", "pcm_lu.py") if (here / name).exists())
+                    ("pyscf_cosmo.py", "pyscf_cosmo_v2.py", "pcm_lu.py", "berny_replay.py") if (here / name).exists())
     packages = [(name, version(name)) for name in ("pyscf", "pyberny", "rdkit", "tblite", "ase", "numpy", "scipy")]
     return hashlib.sha256(code + json.dumps(packages).encode()
                           + os.environ.get("ZC_TRIC_PREOPT", "0").encode()).hexdigest()
@@ -54,9 +54,18 @@
     for el, r in RADII.items():
         table[elements.charge(el)] = r / BOHR
     s.radii_table = table
-    # E-class restart (registered 2026-09-30, off unless ZC_BERNY_STATE=1): the pyberny optimiser state (Hessian, trust
+    if os.environ.get("ZC_BERNY_REPLAY", "0") == "1":
+        if partial is None:
+            raise ValueError("R2 replay needs a checkpoint path")
+        from zcosmo.berny_replay import kernel as replay_kernel
+        limit = int(os.environ.get("ZC_MAXSTEPS", maxsteps))
+        converged, m2 = replay_kernel(mf, partial, limit)
+        if not converged:
+            raise RuntimeError(f"Berny did not converge in {limit} steps; checkpoint retained")
+        return np.asarray(m2.atom_coords(unit="Angstrom"))
+    # A-class restart (accepted 2026-09-30; the original E gate failed): the pyberny optimiser state (Hessian, trust
     # radius, history) is pickled next to the geometry checkpoint and restored on resume, so a resumed run continues
-    # exactly the optimisation an uninterrupted run would have done. ZC_MAXSTEPS only overrides the per-pass step cap.
+    # an A-class restart trajectory. ZC_MAXSTEPS only overrides the per-pass step cap.
     keep_state = os.environ.get("ZC_BERNY_STATE", "0") == "1" and partial is not None
     maxsteps = int(os.environ.get("ZC_MAXSTEPS", maxsteps))
     state_path = str(partial) + ".bstate" if keep_state else None
@@ -121,7 +130,12 @@
         mol = Chem.AddHs(Chem.MolFromSmiles(row["smiles"]))
         sym = [a.GetSymbol() for a in mol.GetAtoms()]
         resumed = False
-        if partial.exists():
+        if os.environ.get("ZC_BERNY_REPLAY", "0") == "1":
+            from zcosmo.berny_replay import checkpoint_geometry
+            trial = checkpoint_geometry(partial, sym)
+            if trial is not None:
+                x0, resumed = trial, True
+        if not resumed and partial.exists():
             p = json.loads(partial.read_text())
             trial = np.asarray(p["x"], dtype=float)
             if p["sym"] == sym and trial.shape == (len(sym), 3) and np.isfinite(trial).all():
--- /dev/null
+++ b/src/zcosmo/berny_replay.py
@@ -0,0 +1,163 @@
+"""Opt-in pre-send Berny checkpoint, with the completed quantum result.
+
+Only load bstate files created by this code in trusted, owner-controlled job
+artifacts. Pickle is not a safe interchange format for untrusted input.
+"""
+from __future__ import annotations
+import hashlib
+import inspect
+import json
+import os
+import pickle
+import warnings
+from dataclasses import fields, is_dataclass
+from importlib.metadata import version
+from pathlib import Path
+import numpy as np
+
+MAGIC = b"ZCOSMO-BERNY-REPLAY-1\n"
+ORBITALS = ("mo_coeff", "mo_occ", "mo_energy", "e_tot", "converged", "cycles")
+
+
+def _atomic(path, data):
+    path = Path(path)
+    tmp = path.with_name(path.name + ".tmp")
+    with tmp.open("wb") as f:
+        f.write(data); f.flush(); os.fsync(f.fileno())
+    os.replace(tmp, path)
+
+
+def _read(path):
+    with Path(path).open("rb") as f:
+        if f.readline() != MAGIC:
+            return None, None
+        line = f.readline(16 * 1024**2)
+        if not line.endswith(b"\n"):
+            raise ValueError("Malformed R2 checkpoint header")
+        header = json.loads(line)
+        payload = f.read()
+    if hashlib.sha256(payload).hexdigest() != header["sha256"]:
+        raise ValueError("Corrupt R2 checkpoint; retain the previous artifact")
+    return header, payload
+
+
+def checkpoint_geometry(partial, symbols):
+    """The versioned atomic bundle, not its JSON mirror, is authoritative."""
+    path = Path(str(partial) + ".bstate")
+    if not path.exists():
+        return None
+    h, _ = _read(path)
+    if h is None:
+        return None
+    x = np.asarray(h["xyz_A"], dtype=float)
+    if h["symbols"] != list(symbols) or x.shape != (len(symbols), 3) or not np.isfinite(x).all():
+        raise ValueError("R2 checkpoint atom order/geometry mismatch")
+    return x
+
+
+def _identity(mf):
+    from berny import Berny
+    import pyscf
+    if pyscf.__version__ != "2.14.0" or version("pyberny") != "0.7.0":
+        raise RuntimeError("R2 replay trial requires PySCF 2.14.0 and pyberny 0.7.0")
+    if "restart" not in inspect.signature(Berny).parameters:
+        raise RuntimeError("Unsupported Berny restart API")
+    if not isinstance(mf.diis, bool):
+        raise TypeError("Persistent/custom DIIS objects need a separate checkpoint contract")
+    s = mf.with_solvent
+    settings = dict(
+        packages={p: version(p) for p in ("pyscf", "pyberny", "numpy", "scipy")},
+        berny_source=hashlib.sha256(inspect.getsource(Berny).encode()).hexdigest(),
+        molecule=[mf.mol.atom_symbol(i) for i in range(mf.mol.natm)],
+        basis=mf.mol._basis, cart=mf.mol.cart, charge=mf.mol.charge, spin=mf.mol.spin,
+        xc=mf.xc, grid_level=mf.grids.level, prune=repr(mf.grids.prune.__name__),
+        auxbasis=mf.with_df.auxbasis, radii=np.asarray(s.radii_table).tolist(),
+        eps=s.eps, method=s.method, lebedev=s.lebedev_order,
+        memory=mf.max_memory, scf={k: getattr(mf, k) for k in
+            ("conv_tol", "conv_tol_grad", "max_cycle", "diis", "diis_space",
+             "diis_start_cycle", "direct_scf", "direct_scf_tol", "level_shift", "damp")},
+        environment={k: os.environ.get(k) for k in
+            ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "ZC_PCM3C",
+             "ZC_PCM3C_MB", "ZC_PCM_GRAD1", "ZC_DF_STORE", "ZC_PCM3C_WORKERS")},
+        code={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in
+              (Path(__file__), Path(__file__).with_name("pyscf_cosmo_v2.py"),
+               Path(__file__).with_name("pcm_lu.py"))},
+    )
+    return hashlib.sha256(json.dumps(settings, sort_keys=True, default=str).encode()).hexdigest()
+
+
+def _restore(base, saved):
+    for key, value in saved.items():
+        setattr(base, key, value)
+
+
+class _ReplayOnce:
+    def __call__(self, mol_or_geom, **kwargs):
+        pending = self._r2_pending
+        if pending is None:
+            self._r2_replayed = False
+            return super().__call__(mol_or_geom, **kwargs)
+        if kwargs:
+            raise TypeError("Unexpected gradient-scanner kwargs during pending-result replay")
+        x = mol_or_geom.atom_coords(unit="Angstrom")
+        if not np.allclose(x, pending["xyz_A"], atol=1e-12, rtol=0):
+            raise ValueError("Pending quantum result is for a different geometry")
+        self.reset(mol_or_geom)
+        _restore(self.base, pending["orbitals"])
+        self.base._last_mol_fp = self.base.mol.ao_loc.copy()
+        self._r2_pending = None
+        self._r2_replayed = True
+        return pending["energy"], pending["gradient"].copy()
+
+
+def kernel(mf, partial, maxsteps):
+    """Run the *upstream* Berny kernel. Never substitute its convergence test."""
+    from pyscf import lib
+    from pyscf.geomopt import berny_solver
+    identity = _identity(mf)
+    path = Path(str(partial) + ".bstate")
+    saved = None
+    if path.exists():
+        header, payload = _read(path)
+        if header is None:
+            warnings.warn("Legacy A-class bstate: starting a new R2 chain from JSON geometry")
+        else:
+            if header["identity"] != identity:
+                raise ValueError("R2 settings/version mismatch; do not silently downgrade this restart")
+            # Only trusted local job artifacts are supported. The digest is not authentication.
+            saved = pickle.loads(payload)
+            mf.reset(mf.mol.set_geom_(header["xyz_A"], unit="Angstrom", inplace=False))
+            _restore(mf, saved["pending"]["orbitals"])
+    scan = mf.nuc_grad_method().as_scanner()
+    scan = lib.set_class(scan, (_ReplayOnce, scan.__class__), "R2ReplayGradientScanner")
+    scan._r2_pending = None if saved is None else saved["pending"]
+    scan._r2_replayed = False
+    count = [0 if saved is None else saved["real_evaluations"]]
+    kw = {} if saved is None else {"restart": saved["optimizer"]}
+
+    def callback(env):
+        scanner = env["g_scanner"]
+        if not scanner.converged:
+            raise RuntimeError("Cannot checkpoint an unconverged SCF gradient")
+        state = env["optimizer"]._state
+        if not is_dataclass(state):
+            raise TypeError("Expected pyberny 0.7.0 BernyState")
+        x = env["mol"].atom_coords(unit="Angstrom")
+        if not np.allclose(state.geom.coords, x, atol=1e-12, rtol=0):
+            raise ValueError("Berny state is not in the expected pre-send phase")
+        if not scanner._r2_replayed:
+            count[0] += 1
+        orbitals = {k: getattr(scanner.base, k) for k in ORBITALS}
+        pending = dict(xyz_A=x, energy=float(env["energy"]),
+                       gradient=np.array(env["gradients"], copy=True), orbitals=orbitals)
+        record = dict(optimizer={f.name: getattr(state, f.name) for f in fields(state)},
+                      pending=pending, real_evaluations=count[0])
+        payload = pickle.dumps(record, protocol=5)
+        header = dict(identity=identity, symbols=[mf.mol.atom_symbol(i) for i in range(mf.mol.natm)],
+                      xyz_A=x.tolist(), sha256=hashlib.sha256(payload).hexdigest())
+        _atomic(path, MAGIC + json.dumps(header, sort_keys=True).encode() + b"\n" + payload)
+        # Legacy-readable mirror. A crash between these writes still leaves one authoritative bundle.
+        _atomic(partial, json.dumps(dict(sym=header["symbols"], x=header["xyz_A"],
+            cycle=int(env["cycle"]), real_evaluations=count[0])).encode())
+
+    return berny_solver.kernel(scan, maxsteps=maxsteps, callback=callback, **kw)
```

```bash
make_tree P12
(cd "$WORK/P12"
 python scripts/round2_logic.py P12 --out "$WORK/checks/P12-portable.json"
 for key in GHVNFZFCNZKVNT-UHFFFAOYSA-N ZIBGPFATKBEMQZ-UHFFFAOYSA-N \
            IMNFDUFMRHMDMM-UHFFFAOYSA-N PWGJDPKCLMLPJW-UHFFFAOYSA-N; do
   python scripts/round2_check.py state --key "$key" --cap 2 \
     --out "$WORK/state-$key"
 done
 ZC_BERNY_REPLAY=1 python scripts/round2_check.py resume-qc --cap 2 --out "$WORK/qc-P12"
 python scripts/optimization_check.py profiles --reference "$WORK/qc-reference" \
   --candidate "$WORK/qc-P12" --mode E --out "$WORK/checks/P12-profiles.json")
```

The `state` command records replayed callbacks separately from real quantum evaluations. A previous reporting bug that counted the final deleted checkpoint as a full cap is therefore not reproduced. A failure of the uninterrupted-reference trace or raw-bin gate rejects the stronger E recovery claim. It does not invalidate the already accepted A persistence protocol.

## P14, E diagnostics: make LLE outcomes distinguishable without changing scores

Target: `src/zcosmo/evaluate.py`, `binodal` and `predict_lle`.

The supplied audit that non-UNIFAC models evaluate everywhere only addresses one failure class. The current function also returns a coarse hull pair when refinement raises or fails, accepts an `ier==1` root without checking the chemical-potential residual, clips trial compositions before evaluation, and selects only the widest grid gap. A finite 101-point search cannot certify the absence of a narrow gap. A coarse grid can also miss additional gaps. Separately, `predict_lle` rounds temperatures to a 2 K grid. These are algorithmic qualifications even when every initial evaluation is finite. [S6]

P14 leaves all current numerical decisions intact. It records grid-evaluation failures separately from “no gap found on this grid,” reports solver status and residual, identifies coarse fallbacks, and reports a sampled tangent margin when an already-computed root evaluation is available. The margin is a diagnostic at existing sample points, not a global stability certificate. It adds **no model evaluations**, so it does not change the order in which Z0x's rounded caches are populated.

Changing failed evaluations to a different scored denominator, rejecting coarse fallbacks, changing the temperature rounding, or refining the phase-search mesh would change reported numbers. Those require a separately registered numerical correction and side-by-side scores. This patch deliberately does not smuggle those changes into an E optimization.

The portable test obtains the regular-solution coexistence pair `(0.14479410825607045, 0.8552058917439407)` for chi=2.5 and detects injected false-success residuals. Audit-on and audit-off runs have identical values and identical model-call sequences in the tested cases.

<!-- PATCH:P14 -->
```diff
--- a/src/zcosmo/evaluate.py
+++ b/src/zcosmo/evaluate.py
@@ -85,14 +85,20 @@
     return out
 
 
-def binodal(m, T, n=81):
+def binodal(m, T, n=81, audit=None):
     """Return (x1_I, x1_II) of the liquid-liquid split at T, or None if miscible."""
+    def note(**values):
+        if audit is not None:
+            audit.update(values)
+    note(status="started", T=float(T), grid_n=int(n))
     xs = np.concatenate([np.logspace(-6, -2, 10), np.linspace(0.02, 0.98, n), 1 - np.logspace(-2, -6, 10)])
     try:
         lg = np.array([m.lngamma(T, np.array([x, 1 - x])) for x in xs])
-    except Exception:
+    except Exception as exc:
+        note(status="grid_evaluation_failed", error=repr(exc))
         return None
     if not np.all(np.isfinite(lg)):
+        note(status="nonfinite_grid", nonfinite_values=int((~np.isfinite(lg)).sum()))
         return None
     g = xs * np.log(xs) + (1 - xs) * np.log(1 - xs) + xs * lg[:, 0] + (1 - xs) * lg[:, 1]
     # lower convex hull
@@ -112,8 +118,12 @@
     for a, b in zip(hx[:-1], hx[1:]):
         if idx[b] - idx[a] > 1 and (best is None or b - a > best[1] - best[0]):
             best = (a, b)
+    gaps = [(a, b) for a, b in zip(hx[:-1], hx[1:]) if idx[b] - idx[a] > 1]
+    note(grid_gap_count=len(gaps), grid_gaps=gaps)
     if best is None:
+        note(status="no_gap_on_grid")  # This is not a proof of global miscibility.
         return None
+    sampled = {}  # Audit only: reuse evaluations already made by fsolve.
 
     def eqs(v):
         xa, xb = v
@@ -121,14 +131,28 @@
         xb = min(max(xb, 1e-9), 1 - 1e-9)
         la = m.lngamma(T, np.array([xa, 1 - xa]))
         lb = m.lngamma(T, np.array([xb, 1 - xb]))
+        if audit is not None:
+            sampled[tuple(v)] = (xa, xb, np.array(la, copy=True), np.array(lb, copy=True))
+            if len(sampled) > 16:
+                del sampled[next(iter(sampled))]
         return [np.log(xa) + la[0] - np.log(xb) - lb[0], np.log(1 - xa) + la[1] - np.log(1 - xb) - lb[1]]
 
     try:
-        sol, info, ier, _ = fsolve(eqs, best, full_output=True)
+        sol, info, ier, message = fsolve(eqs, best, full_output=True)
+        residual = float(np.max(np.abs(info.get("fvec", [np.nan]))))
+        note(ier=int(ier), solver_message=str(message), nfev=int(info.get("nfev", -1)),
+             residual_max=residual if np.isfinite(residual) else None)
+        if audit is not None and tuple(sol) in sampled:
+            xa, xb, la, lb = sampled[tuple(sol)]
+            mu = np.log([xa, 1-xa]) + la
+            margin = float(np.min(g - (xs * mu[0] + (1-xs) * mu[1])))
+            note(sampled_tangent_margin=margin if np.isfinite(margin) else None)
         if ier == 1 and 0 < sol[0] < sol[1] < 1 and sol[1] - sol[0] > 1e-4:
+            note(status="refined_root", residual_pass=bool(np.isfinite(residual) and residual < 1e-7))
             return float(sol[0]), float(sol[1])
-    except Exception:
-        pass
+    except Exception as exc:
+        note(refinement_error=repr(exc))
+    note(status="coarse_hull_fallback")
     return best
 
 
@@ -144,7 +168,18 @@
         Tk = round(r.T / 2) * 2
         bk = (k, Tk)
         if bk not in bcache:
-            bcache[bk] = binodal(cache[k], float(Tk))
+            directory = os.environ.get("ZC_LLE_AUDIT_DIR")
+            audit = {} if directory else None
+            bcache[bk] = binodal(cache[k], float(Tk), audit=audit)
+            if audit is not None:
+                import json
+                audit.update(model=model_name, c1=k[0], c2=k[1],
+                             first_requested_T=float(r.T), binodal_T=float(Tk),
+                             returned=bcache[bk])
+                path = Path(directory)
+                path.mkdir(parents=True, exist_ok=True)
+                with (path / f"lle-{os.getpid()}.jsonl").open("a") as handle:
+                    handle.write(json.dumps(audit, allow_nan=False) + "\n")
         b = bcache[bk]
         if b is not None:
             split[i] = True
```

```bash
make_tree P14
(cd "$WORK/P14"; python scripts/round2_logic.py P14 --out "$WORK/checks/P14-portable.json")
for arm in base P14; do
  for model in unifac_do cosmosac2010 cosmosac_dsp Z0x; do
    (cd "$WORK/$arm"
     ZC_PRED="$WORK/lle-$arm" ZC_LLE_AUDIT_DIR="$WORK/lle-audit-$arm" \
       python -m zcosmo.evaluate "$model" --tables lle --split all)
  done
done
python - "$WORK" <<'PYCODE'
from pathlib import Path
import pandas as pd, sys
w=Path(sys.argv[1])
for r in sorted((w/'lle-base').glob('*__lle__all.csv')):
    c=w/'lle-P14'/r.name
    pd.testing.assert_frame_equal(pd.read_csv(r), pd.read_csv(c), check_exact=True)
    print('unchanged',r.name)
PYCODE
python - "$WORK/lle-audit-P14" <<'PYCODE'
from pathlib import Path
from collections import Counter
import json,sys
rows=[json.loads(line) for p in Path(sys.argv[1]).glob('*.jsonl') for line in p.read_text().splitlines()]
assert rows
print(Counter((r['model'],r['status']) for r in rows))
print('refined roots failing residual check:',sum(r['status']=='refined_root' and not r['residual_pass'] for r in rows))
print('coarse fallbacks:',sum(r['status']=='coarse_hull_fallback' for r in rows))
PYCODE
```

Each sidecar entry describes one cached pair/rounded-temperature evaluation, not every original data row. Runtime overhead comes from bookkeeping and JSON output; no speed-up is claimed.

## Remaining decisions and waste to avoid

The current PySCF scanner already reuses the preceding density matrix when the AO layout matches. “Reuse density between Berny steps” is not a new optimization. What is missing on a process restart is a compatible electronic starting state, addressed specifically by P12. Reusing a J-fit metric or atom-centered quadrature arrays after atoms have moved is not the same exact operation as reusing them within one geometry. [U2, U5]

The stored-tensor proposal keeps `direct_scf_tol` unchanged. A looser screening threshold, different auxiliary basis, altered pruning, smaller grid, or different convergence tolerance would need its own numerical gate and potentially an A registration. There is no profile evidence here supporting those changes as the next lever. XC AO caching is also deferred: it removes only AO evaluation, not the density-dependent XC contractions, and its memory competes with both existing caches. First measure that subcomponent after P9.

GPU4PySCF is no longer an unanswered feasibility question. The recorded 4070 Super test using gpu4pyscf 1.8.1 and CPU PySCF 2.14.0 found energy differences at most `6.4e-10 Eh`, but gradient differences up to `1e-5 Eh/Bohr` and different octanol surface sizes: 1535 versus 1533 at SVP, 3433 versus 3429 at TZVP. Equal energies do not establish identical gradients or comparable q entries. Sorting vectors cannot repair a different discretized surface. The accepted GPU pre-stage followed by registered CPU polish is A and should remain so. The recorded 7.3×/10.9× octanol timings belong to that 4070 Super comparison, not automatically to a T4 or 6 GB 2060. I do not provide another purportedly identical GPU path or install recipe as a new accepted proposal when the actual project gate already disproved that claim. [S3]

Likewise, the P6 paragraph requested in the original round-2 prompt is already present with a completed check. Its exact operative rule is the analytic interior derivative of the same g, retention of the old one-sided endpoint treatment within `1e-4`, identical finite coverage on the prescribed 250 queries, and max disagreement with the specified Richardson reference below `1e-4`. It passed at `2e-6`. No duplicate preregistration or re-use of the old E comparison is appropriate. [S3]

The on-sphere evidence deserves attention, but neither tiny Cartesian gradients nor small displacement establishes that a stalled point passed Berny's original test. Keep the existing rejections. The one-molecule rigid-rotation test shows **orientation/discretization sensitivity** of the raw profile: a `0.001 rad` rotation changed a bin by .016. It does not establish a universal stochastic noise floor or justify silently replacing the failed .001 absolute criterion with a relative criterion. Calibrating a new orientation-aware profile metric would be a separate, explicitly post-hoc-motivated registration on a frozen set of molecules and rotations. P15 instead attempts to satisfy the original test without changing its limits. [S3]

Profile-cache invalidation is a real hazard. Changing `ZC_SIGMA_OVERRIDE_DIR` in one Python process does not change the key of `load_fluid`'s cache. Your discarded zero-difference run is evidence of that failure mode. The gates here load explicit reference/candidate directories and compare the finite masks; scorecard comparisons use separate processes. A zero sensitivity result from an in-process environment switch is not valid evidence. [S3, S9]

Finally, keep the direct MACE route shelved under its existing registered result. An improved replica-exchange implementation would not by itself repair the model's recorded free-energy discrepancy. None of this round's compute instructions revives that project or launches a cloud job. [S1, S3]

## Shared harness H2

This includes the actual native checks to run and the portable tests executed here. The latter deliberately state `PORTABLE_ONLY_NOT_NATIVE_ACCEPTANCE`. The corrected repository H0 retains responsibility for the frozen profile manifest, including nonfinite coverage. No experimental response is used to choose an optimizer parameter or a performance variant.

<!-- PATCH:H2 -->
```diff
--- /dev/null
+++ b/scripts/round2_check.py
@@ -0,0 +1,346 @@
+"""Round-2 diagnostics, no experimental response values or score fitting.
+
+Native QC subcommands require the real PySCF 2.14.0 installation. Syntax or
+logic tests do not establish native API compatibility or E acceptance.
+"""
+from __future__ import annotations
+import argparse
+import cProfile
+import functools
+import hashlib
+import importlib
+import inspect
+import json
+import os
+import pstats
+import sys
+import threading
+import time
+from contextlib import contextmanager
+from importlib.metadata import version
+from pathlib import Path
+import numpy as np
+
+
+def write(path, obj):
+    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
+    path.write_text(json.dumps(obj, indent=2, allow_nan=False) + "\n")
+    print(json.dumps(obj, allow_nan=False))
+
+
+@contextmanager
+def environment(**values):
+    old = {k: os.environ.get(k) for k in values}
+    for k, v in values.items():
+        if v is None: os.environ.pop(k, None)
+        else: os.environ[k] = str(v)
+    try: yield
+    finally:
+        for k, v in old.items():
+            if v is None: os.environ.pop(k, None)
+            else: os.environ[k] = v
+
+
+def runtime():
+    import pyscf
+    from pyscf import lib
+    from threadpoolctl import threadpool_info
+    if pyscf.__version__ != "2.14.0":
+        raise RuntimeError("This trial is specified against PySCF 2.14.0")
+    return dict(pyscf=pyscf.__version__, pyberny=version("pyberny"),
+        numpy=np.__version__, scipy=version("scipy"),
+        pyscf_threads=lib.num_threads(), pools=threadpool_info(),
+        affinity=sorted(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else None,
+        flags={k: v for k, v in os.environ.items() if k.startswith("ZC_") or k.endswith("NUM_THREADS")})
+
+
+@contextmanager
+def observe_berny(receive, verbose=None):
+    """Bind against the actual signature: optimize passes callback positionally."""
+    from pyscf.geomopt import berny_solver
+    original = berny_solver.kernel
+    signature = inspect.signature(original)
+    @functools.wraps(original)
+    def wrapped(*args, **kwargs):
+        bound = signature.bind_partial(*args, **kwargs)
+        old = bound.arguments.get("callback")
+        method = bound.arguments.get("method")
+        if verbose is not None:
+            for obj in (method, method.mol, getattr(method, "with_solvent", None),
+                        getattr(method, "with_df", None), getattr(method, "grids", None)):
+                if obj is not None: obj.verbose = verbose
+        def callback(env):
+            if old is not None: old(env)
+            receive(env)
+        bound.arguments["callback"] = callback
+        return original(*bound.args, **bound.kwargs)
+    berny_solver.kernel = wrapped
+    try: yield
+    finally: berny_solver.kernel = original
+
+
+class Timers:
+    """Inclusive wall time and exclusive time relative to instrumented children.
+
+    cProfile only observes its calling thread. These wrappers also observe the
+    optional P13 worker threads. Summed worker time is not elapsed job time.
+    """
+    def __init__(self):
+        self.old = []; self.rows = {}; self.local = threading.local(); self.lock = threading.Lock()
+    def install(self, owner, name, label=None):
+        original = getattr(owner, name, None)
+        if not callable(original): return
+        base = label or owner.__name__ + "." + name
+        @functools.wraps(original)
+        def wrapped(*args, **kwargs):
+            label_ = base
+            if name == "aux_e2": label_ += ":" + str(kwargs.get("intor", "int3c2e"))
+            stack = getattr(self.local, "stack", None)
+            if stack is None: stack = self.local.stack = []
+            frame = [time.perf_counter(), 0.]; stack.append(frame)
+            try: return original(*args, **kwargs)
+            finally:
+                elapsed = time.perf_counter() - frame[0]; stack.pop()
+                if stack: stack[-1][1] += elapsed
+                with self.lock:
+                    row = self.rows.setdefault(label_, dict(calls=0, inclusive_s=0., exclusive_instrumented_s=0.))
+                    row["calls"] += 1; row["inclusive_s"] += elapsed
+                    row["exclusive_instrumented_s"] += elapsed - frame[1]
+        self.old.append((owner, name, original)); setattr(owner, name, wrapped)
+    def close(self):
+        for obj, name, old in reversed(self.old): setattr(obj, name, old)
+
+
+def trace(a):
+    from zcosmo.pyscf_cosmo import xtb_geometry
+    from zcosmo import pyscf_cosmo_v2 as q
+    from zcosmo import pcm_lu
+    meta = runtime()
+    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
+    if a.xyz:
+        d = json.loads(Path(a.xyz).read_text()); sym, x = d["sym"], np.asarray(d["x"])
+    else:
+        sym, x = xtb_geometry(a.smiles)
+    write(out / "start.json", dict(sym=list(sym), x=np.asarray(x).tolist()))
+    partial = None
+    if a.use_state:
+        import shutil
+        if not a.xyz: raise ValueError("--use-state requires --xyz pointing to a trusted legacy checkpoint")
+        source = Path(str(a.xyz)+".bstate")
+        if not source.is_file(): raise FileNotFoundError(source)
+        partial = out/"trace.partial.json"
+        shutil.copyfile(a.xyz, partial)
+        shutil.copyfile(source, str(partial)+".bstate")
+    timers = Timers()
+    for mod, funcs in [
+        ("pyscf.scf.hf", ["kernel"]), ("pyscf.df.df_jk", ["get_jk"]),
+        ("pyscf.dft.numint", ["nr_rks", "nr_uks"]),
+        ("pyscf.grad.rhf", ["grad_elec"]),
+        ("pyscf.grad.rks", ["get_vxc"]), ("pyscf.grad.uks", ["get_vxc"]),
+        ("pyscf.solvent.grad.pcm", ["grad_qv", "grad_nuc", "grad_solver"]),
+        ("pyscf.df.incore", ["aux_e2"]),
+    ]:
+        module = importlib.import_module(mod)
+        for f in funcs: timers.install(module, f)
+    for cls, funcs in [(pcm_lu.CachedPCM, ["_get_vind"]),
+                       (pcm_lu.CachedPCM3c, ["_get_v", "_get_vmat", "_zc_blocks"])]:
+        for f in funcs: timers.install(cls, f)
+    if hasattr(pcm_lu, "_grad_qv_onepass"): timers.install(pcm_lu, "_grad_qv_onepass")
+    events = []
+    def event(env):
+        scanner = env["g_scanner"]; base = scanner.base; s = base.with_solvent
+        cache = s._intermediates.get("_zc_3c")
+        allocated = sum(v.nbytes for _, _, v in cache[1] if v is not None) if cache else 0
+        nao = base.mol.nao; ng = len(s.surface["grid_coords"])
+        state = env["optimizer"]._state
+        predicted, interpolated = getattr(state, "predicted", None), getattr(state, "interpolated", None)
+        predicted_drop = None if predicted is None or interpolated is None else float(predicted.E-interpolated.E)
+        events.append(dict(cycle=int(env["cycle"]), energy_Eh=float(env["energy"]),
+            trust_before_send=float(state.trust), previous_predicted_dE=predicted_drop,
+            energy_noise_Eh=float(getattr(state.params, "energy_noise", 0.)),
+            scf_cycles=int(getattr(base, "cycles", -1)), nao=nao, surface_points=ng,
+            cache_bytes=allocated, full_packed_cache_bytes=8 * nao * (nao+1)//2 * ng,
+            auxbasis=str(base.with_df.auxbasis),
+            resolved_auxbasis=str(getattr(base.with_df.auxmol, "basis", None)),
+            gradient_max=float(np.abs(env["gradients"]).max())))
+    profiler = cProfile.Profile(); stopped = None
+    start = time.perf_counter(); cpu = time.process_time()
+    try:
+        with environment(ZC_PCM3C="1", ZC_BERNY_STATE="1" if a.use_state else "0", ZC_BERNY_REPLAY="0", ZC_MAXSTEPS=a.cycles, ZC_BERNY_NOISE_EH=None):
+            with observe_berny(event, verbose=6):
+                profiler.enable()
+                try:
+                    q.dft_geometry(sym, np.asarray(x), maxsteps=a.cycles, partial=partial)
+                except RuntimeError as exc:
+                    if str(exc) != f"Berny did not converge in {a.cycles} steps; checkpoint retained" or len(events) != a.cycles:
+                        raise
+                    stopped = "requested_cycle_cap"
+                finally: profiler.disable()
+    finally: timers.close()
+    wall = time.perf_counter()-start; cpu = time.process_time()-cpu
+    profiler.dump_stats(str(out / "cycle.prof"))
+    with (out / "cprofile.txt").open("w") as f:
+        stats = pstats.Stats(profiler, stream=f); stats.sort_stats("cumulative").print_stats(80)
+        stats.sort_stats("tottime").print_stats(60)
+    import resource
+    write(out / "trace.json", dict(runtime=meta, wall_s=wall, cpu_s=cpu, cpu_over_wall=cpu/wall,
+        maxrss_platform_units=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
+        stop=stopped or "converged", effective_cycle_cap=a.cycles, effective_PCM3C=1,
+        actual_geometry_evaluations=len(events), cycles=events,
+        timers=timers.rows, timer_note="Nested totals overlap; worker sums are not job elapsed time."))
+
+
+def method(atoms, spin, basis, level, lebedev, tol):
+    from pyscf import gto, dft
+    from pyscf.data import elements
+    from zcosmo.pyscf_cosmo import BOHR, RADII
+    from zcosmo.pcm_lu import cache_pcm3c
+    mol = gto.M(atom=atoms, unit="Angstrom", spin=spin, basis=basis, verbose=0,
+                max_memory=int(os.environ.get("QC_MEM_MB", "3000")))
+    mf = (dft.UKS(mol) if spin else dft.RKS(mol)).density_fit().PCM()
+    mf = cache_pcm3c(mf); mf.xc = "b88,p86"; mf.grids.level = level; mf.conv_tol = tol
+    s = mf.with_solvent; s.method = "C-PCM"; s.eps = 1e9; s.lebedev_order = lebedev
+    table = np.zeros(120)
+    for el, radius in RADII.items(): table[elements.charge(el)] = radius / BOHR
+    s.radii_table = table
+    return mf
+
+
+def fixed(a):
+    meta = runtime(); rows = []
+    levels = [("def2-svp", 2, 17, 1e-8), ("def2-tzvp", 3, 29, 1e-9)]
+    for label, atoms, spin in [("water", "O 0 0 0; H 0 .76 .59; H 0 -.76 .59", 0),
+                                ("oxygen", "O 0 0 0; O 0 0 1.21", 2)]:
+        for spec in levels:
+            arms = []
+            for value in (a.baseline, a.value):
+                with environment(**{a.flag: value}):
+                    mf = method(atoms, spin, *spec); start = time.perf_counter()
+                    e = mf.kernel()
+                    if not mf.converged: raise RuntimeError("Fixed-geometry SCF did not converge")
+                    grad = mf.nuc_grad_method().kernel(); elapsed = time.perf_counter()-start
+                    s = mf.with_solvent
+                    arms.append((float(e), np.array(grad), s._intermediates["q"].copy(),
+                                 s.surface["grid_coords"].copy(), elapsed))
+                    if a.identity:
+                        from pyscf import gto, df
+                        ids = np.linspace(0, len(s.surface["grid_coords"])-1, 16, dtype=int)
+                        fm = gto.fakemol_for_charges(s.surface["grid_coords"][ids],
+                                                   expnt=s.surface["charge_exp"][ids]**2)
+                        fm.cart = mf.mol.cart
+                        ip1 = df.incore.aux_e2(mf.mol, fm, intor="int3c2e_ip1", aosym="s1")
+                        ip2 = df.incore.aux_e2(mf.mol, fm, intor="int3c2e_ip2", aosym="s1")
+                        error = float(np.max(np.abs(ip2 + ip1 + ip1.transpose(0,2,1,3))))
+                        if error >= 1e-10: raise AssertionError((label, spec[0], "translation identity", error))
+                    del mf
+            b, c = arms
+            if not np.array_equal(b[3], c[3]): raise AssertionError("Surface geometry/order changed")
+            de, dg, dq = abs(b[0]-c[0]), float(np.abs(b[1]-c[1]).max()), float(np.abs(b[2]-c[2]).max())
+            if not all(np.isfinite(v) for v in (de, dg, dq)): raise AssertionError("Nonfinite fixed comparison")
+            rows.append(dict(molecule=label, basis=spec[0], energy_Eh=de, gradient_Eh_Bohr=dg,
+                charge_e=dq, reference_s=b[4], candidate_s=c[4]))
+            if not (de < 1e-8 and dg < 1e-6 and dq < 1e-8):
+                write(a.out, dict(runtime=meta, checks=rows, status="FAIL")); raise SystemExit(1)
+    write(a.out, dict(runtime=meta, checks=rows, status="FIXED_GEOMETRY_PASS_NOT_PROFILE_ACCEPTANCE"))
+
+
+GATE = {
+    "GHVNFZFCNZKVNT-UHFFFAOYSA-N": "C(CCCCCC)CCC(=O)O",
+    "ZIBGPFATKBEMQZ-UHFFFAOYSA-N": "OCCOCCOCCO",
+    "IMNFDUFMRHMDMM-UHFFFAOYSA-N": "CCCCCCC",
+    "PWGJDPKCLMLPJW-UHFFFAOYSA-N": "NCCCCCCCCN",
+}
+
+
+def state(a):
+    from zcosmo import pyscf_cosmo_v2 as q
+    from zcosmo.pyscf_cosmo import xtb_geometry
+    runtime()
+    if version("pyberny") != "0.7.0": raise RuntimeError("This gate specifies pyberny 0.7.0")
+    root = Path(a.out); root.mkdir(parents=True, exist_ok=True)
+    if any(root.glob("*/*.sigma")): raise ValueError("State gate needs fresh output")
+    sym, start = xtb_geometry(GATE[a.key]); reports = {}; arrays = {}
+    for arm in ("full", "replay"):
+        out = root / arm; out.mkdir(exist_ok=True)
+        write(out / f"{a.key}.partial.json", dict(sym=sym, x=start.tolist(), cycle=-1))
+        events = []; passes = 0; t0 = time.perf_counter()
+        def event(env):
+            scanner = env["g_scanner"]
+            events.append(dict(pass_index=passes, replayed=bool(getattr(scanner, "_r2_replayed", False)),
+                energy=float(env["energy"]), xyz=env["mol"].atom_coords(unit="Angstrom").tolist(),
+                gradient=np.asarray(env["gradients"]).tolist(),
+                scf_cycles=int(getattr(scanner.base, "cycles", -1))))
+        with environment(ZC_BERNY_STATE="0", ZC_BERNY_REPLAY="1" if arm=="replay" else "0",
+                         ZC_MAXSTEPS=a.cap if arm=="replay" else 300):
+            with observe_berny(event):
+                for passes in range(1, 301):
+                    _, status, _ = q.run_one(dict(inchikey=a.key, smiles=GATE[a.key]), out)
+                    if status == "ok": break
+                    if "Berny did not converge in" not in status: raise RuntimeError(status)
+                else: raise RuntimeError("State gate exhausted 300 passes")
+        real = [e for e in events if not e["replayed"]]
+        reports[arm] = dict(passes=passes, real_evaluations=len(real), replays=len(events)-len(real),
+                            wall_s=time.perf_counter()-t0)
+        write(out / "events.json", events)
+        arrays[arm] = np.loadtxt(out / f"{a.key}.sigma")
+    x, y = arrays["full"][:,1], arrays["replay"][:,1]
+    full_events = json.loads((root / "full/events.json").read_text())
+    replay_events = [e for e in json.loads((root / "replay/events.json").read_text()) if not e["replayed"]]
+    matched = len(full_events) == len(replay_events)
+    trace_dx = max(float(np.max(np.abs(np.array(b["xyz"])-c["xyz"]))) for b,c in zip(full_events,replay_events)) if matched else None
+    trace_de = max(abs(b["energy"]-c["energy"]) for b,c in zip(full_events,replay_events)) if matched else None
+    trace_dg = max(float(np.max(np.abs(np.array(b["gradient"])-c["gradient"]))) for b,c in zip(full_events,replay_events)) if matched else None
+    profile_meta = {arm: json.loads((root/arm/f"{a.key}.sigma").read_text().splitlines()[0][len("# meta: "):]) for arm in ("full", "replay")}
+    final_de = abs(profile_meta["full"]["E_scf_Eh"]-profile_meta["replay"]["E_scf_Eh"])
+    result = dict(arms=reports, final_TZVP_delta_Eh=final_de, trace_max_dx_A=trace_dx, trace_max_dE_Eh=trace_de,
+                  trace_max_dG_Eh_Bohr=trace_dg, raw_bin_max=float(np.abs(x-y).max()),
+                  normalized_bin_max=float(np.abs(x/x.sum()-y/y.sum()).max()))
+    result["pass"] = bool(reports["replay"]["passes"]>=3 and
+        matched and trace_dx < 1e-6 and trace_de < 1e-8 and trace_dg < 1e-6 and final_de < 1e-6 and
+        result["raw_bin_max"]<1e-4 and result["normalized_bin_max"]<1e-4)
+    write(root / "comparison.json", result)
+    if not result["pass"]: raise SystemExit(1)
+
+
+def resume_qc(a):
+    from zcosmo import pyscf_cosmo_v2 as q
+    from optimization_check import fixture
+    runtime()
+    val, _ = fixture()
+    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
+    if list(out.glob("*.sigma")): raise ValueError("Use a fresh resume-qc output directory")
+    traces=[]; reports=[]; current=[None]; start=time.perf_counter()
+    def event(env):
+        traces.append(dict(key=current[0], replayed=bool(getattr(env["g_scanner"], "_r2_replayed", False))))
+    with environment(ZC_MAXSTEPS=a.cap):
+        with observe_berny(event):
+            for row in val.to_dict("records"):
+                current[0]=row["inchikey"]; t=time.perf_counter()
+                for attempt in range(1,301):
+                    key, status, _=q.run_one(row,out)
+                    if status == "ok": break
+                    if "Berny did not converge in" not in status: raise RuntimeError((key,status))
+                else: raise RuntimeError((key,"exhausted 300 passes"))
+                reports.append(dict(key=key,passes=attempt,wall_s=time.perf_counter()-t))
+    write(out/"resume-timing.json",dict(wall_s=time.perf_counter()-start,molecules=reports,
+        real_evaluations=sum(not t["replayed"] for t in traces),replays=sum(t["replayed"] for t in traces)))
+
+
+def main():
+    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="command", required=True)
+    p = sub.add_parser("trace"); inp = p.add_mutually_exclusive_group(required=True)
+    inp.add_argument("--smiles"); inp.add_argument("--xyz")
+    p.add_argument("--cycles", type=int, default=3); p.add_argument("--out", required=True); p.add_argument("--use-state", action="store_true")
+    p = sub.add_parser("fixed"); p.add_argument("--flag", choices=["ZC_PCM_GRAD1", "ZC_DF_STORE", "ZC_PCM3C_WORKERS"], required=True)
+    p.add_argument("--baseline", default="0"); p.add_argument("--value", default="1")
+    p.add_argument("--identity", action="store_true"); p.add_argument("--out", required=True)
+    p = sub.add_parser("state"); p.add_argument("--key", choices=list(GATE), required=True)
+    p.add_argument("--cap", type=int, default=2); p.add_argument("--out", required=True)
+    p = sub.add_parser("resume-qc"); p.add_argument("--out", required=True); p.add_argument("--cap",type=int,default=2)
+    args = ap.parse_args()
+    if args.command == "trace" and args.cycles < 1: ap.error("cycles must be positive")
+    if args.command in ("state", "resume-qc") and args.cap < 2: ap.error("cap must leave room for replay plus a new step")
+    globals()[args.command.replace("-", "_")](args)
+
+
+if __name__ == "__main__": main()
--- /dev/null
+++ b/scripts/round2_logic.py
@@ -0,0 +1,165 @@
+"""Portable algebra/control-flow tests. These do NOT run PySCF or prove E acceptance."""
+import argparse, ast, importlib.util, json, sys, tempfile, types
+from pathlib import Path
+import numpy as np
+
+
+def definitions(path, names, namespace):
+    tree = ast.parse(Path(path).read_text())
+    chosen = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
+    if len(chosen) != len(names): raise AssertionError((path, names))
+    exec(compile(ast.Module(body=chosen, type_ignores=[]), str(path), 'exec'), namespace)
+    return namespace
+
+
+def p10(root):
+    rng = np.random.default_rng(42); errors=[]
+    for nao, ng in ((3, 11), (5, 1201), (7, 401)):
+        a = rng.normal(size=(3, nao, nao, ng)); b = -a-a.transpose(0,2,1,3)
+        dm = rng.normal(size=(nao,nao)); q = rng.normal(size=ng)
+        parts = [(0, ng//2), (ng//2,ng)]; aos = np.array([[0,0,0,nao//2],[0,0,nao//2,nao]])
+        mol = types.SimpleNamespace(nao=nao,cart=False,_atm=None,_bas=None,_env=None,
+            _add_suffix=lambda name:name, aoslice_by_atom=lambda:aos)
+        grid = np.c_[np.arange(ng), np.zeros((ng,2))]
+        pcm = types.SimpleNamespace(mol=mol,max_memory=0, _intermediates={'dm':dm,'q_sym':q},
+            surface={'grid_coords':grid,'charge_exp':np.ones(ng),'gslice_by_atom':parts})
+        calls=[]
+        def aux_e2(mol, aux, **kwargs):
+            calls.append(kwargs['intor']); assert kwargs['intor']=='int3c2e_ip1'
+            return a[:,:,:,aux.indices]
+        gto = types.SimpleNamespace(moleintor=types.SimpleNamespace(make_cintopt=lambda *a:None),
+            fakemol_for_charges=lambda xyz,expnt:types.SimpleNamespace(indices=xyz[:,0].astype(int)))
+        lib = types.SimpleNamespace(current_memory=lambda:(0,),prange=lambda lo,hi,step:
+            [(i,min(i+step,hi)) for i in range(lo,hi,step)])
+        logger = types.SimpleNamespace(process_clock=lambda:0,perf_counter=lambda:0,
+            new_logger=lambda mol:types.SimpleNamespace(timer_debug1=lambda *a:None))
+        fake = types.ModuleType('pyscf.lib'); fake.logger=logger
+        prior = sys.modules.get('pyscf.lib'); sys.modules['pyscf.lib']=fake
+        try:
+            ns=definitions(root/'src/zcosmo/pcm_lu.py',['_grad_qv_onepass'],
+                 dict(np=np,gto=gto,lib=lib,df=types.SimpleNamespace(incore=types.SimpleNamespace(aux_e2=aux_e2))))
+            result=ns['_grad_qv_onepass'](pcm,dm)
+        finally:
+            if prior is None:sys.modules.pop('pyscf.lib',None)
+            else:sys.modules['pyscf.lib']=prior
+        dv=np.einsum('xijk,ij,k->xi',a,dm,q)
+        dq=np.einsum('xijk,ij,k->xk',b,dm,q)
+        ref=2*np.array([dv[:,lo:hi].sum(1) for lo,hi in aos[:,2:]])+np.array([dq[:,lo:hi].sum(1) for lo,hi in parts])
+        errors.append(float(abs(result-ref).max()))
+        assert errors[-1] < 1e-10 and len(calls)==(ng+399)//400
+    return dict(max_contraction_error=max(errors), cases=len(errors), native_integrals=False)
+
+
+def p11(root):
+    class DF:
+        def __init__(self,mol=None,auxbasis=None):self.mol=mol;self.auxbasis=auxbasis;self._cderi=None;self.builds=0
+        def build(self):self._cderi=np.ones((2,2));self.builds+=1
+        def reset(self):self._cderi=None
+        def get_jk(self,dm,**kw):return dm.copy(),None
+    ns=definitions(root/'src/zcosmo/pcm_lu.py',['StoredJDF','_store_j_tensor'],dict(df=types.SimpleNamespace(DF=DF)))
+    mf=types.SimpleNamespace(with_df=DF('mol','same-aux'));ns['_store_j_tensor'](mf)
+    for _ in range(3):mf.with_df.get_jk(np.eye(2),with_k=False)
+    assert mf.with_df.builds==1
+    mf.with_df.reset();mf.with_df.get_jk(np.eye(2),with_k=False)
+    assert mf.with_df.builds==2 and mf.with_df.auxbasis=='same-aux'
+    return dict(builds_after_repeated_calls_and_reset=2,native_df=False)
+
+
+def p12(root):
+    path=root/'src/zcosmo/berny_replay.py'
+    spec=importlib.util.spec_from_file_location('round2_replay_under_test',path)
+    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
+    import pickle,hashlib
+    with tempfile.TemporaryDirectory() as tmp:
+        partial=Path(tmp)/'test.partial.json';state=Path(str(partial)+'.bstate')
+        payload=pickle.dumps({'array':np.arange(5.)},protocol=5)
+        header=dict(symbols=['H'],xyz_A=[[1.,2.,3.]],sha256=hashlib.sha256(payload).hexdigest())
+        mod._atomic(state,mod.MAGIC+json.dumps(header).encode()+b'\n'+payload)
+        assert np.array_equal(mod.checkpoint_geometry(partial,['H']),[[1.,2.,3.]])
+        h,p=mod._read(state);assert p==payload
+        state.write_bytes(state.read_bytes()[:-1]+b'x')
+        try:mod._read(state)
+        except ValueError:pass
+        else:raise AssertionError('Corruption accepted')
+    class Mol:
+        def atom_coords(self,unit):return np.array([[1.,2.,3.]])
+        ao_loc=np.array([0,1])
+    class Scan:
+        def __init__(self):self.base=types.SimpleNamespace(mol=Mol());self.real=0
+        def reset(self,mol):self.base.mol=mol
+        def __call__(self,mol,**kw):self.real+=1;return 2.,np.zeros((1,3))
+    C=type('ReplayTest',(mod._ReplayOnce,Scan),{})
+    obj=C();obj._r2_pending=dict(xyz_A=np.array([[1.,2.,3.]]),energy=1.,gradient=np.ones((1,3)),orbitals={'mo_coeff':np.eye(2)})
+    e,g=obj(Mol());assert e==1 and obj.real==0 and obj._r2_replayed
+    assert np.array_equal(obj.base.mo_coeff,np.eye(2))
+    e,g=obj(Mol());assert e==2 and obj.real==1 and not obj._r2_replayed
+    return dict(atomic_bundle=True,corruption_rejected=True,replay_once=True,native_scanner=False)
+
+
+def p13(root):
+    import threading
+    local=threading.local();local.n=4;seen=[];lock=threading.Lock()
+    def threads(n):local.n=n
+    def opt(*a):return object()
+    def aux(mol,fm,**kw):
+        with lock:seen.append(getattr(local,'n',-1))
+        return np.arange(6.)[:,None]+fm.xyz[:,0][None,:]*100
+    lib=types.SimpleNamespace(num_threads=threads)
+    gto=types.SimpleNamespace(moleintor=types.SimpleNamespace(make_cintopt=opt),
+        fakemol_for_charges=lambda xyz,expnt:types.SimpleNamespace(xyz=xyz))
+    ns=definitions(root/'src/zcosmo/pcm_lu.py',['_parallel_surface_3c'],dict(np=np,lib=lib,gto=gto,
+        df=types.SimpleNamespace(incore=types.SimpleNamespace(aux_e2=aux))))
+    mol=types.SimpleNamespace(nao=3,cart=False,_atm=None,_bas=None,_env=None)
+    grid=np.c_[np.arange(513),np.zeros((513,2))]
+    for workers in (2,4):
+        ans=ns['_parallel_surface_3c'](mol,grid,np.ones(513),'int3c2e',workers)
+        assert np.array_equal(ans,np.arange(6.)[:,None]+100*np.arange(513)[None,:])
+    assert set(seen)=={1} and local.n==4
+    return dict(disjoint_column_order=True,worker_icv_mock=1,parent_icv_mock=4,native_openmp=False)
+
+
+def p14(root):
+    from scipy.optimize import fsolve
+    source=root/'src/zcosmo/evaluate.py'
+    original=source.read_text()
+    ns=definitions(source,['binodal'],dict(np=np,fsolve=fsolve))
+    fn=ns['binodal'];out={}
+    class Model:
+        def __init__(self,chi=0,mode='finite'):self.chi=chi;self.mode=mode;self.calls=[]
+        def lngamma(self,T,x):
+            self.calls.append((float(T),tuple(x)))
+            if self.mode=='error':raise ValueError('intentional')
+            if self.mode=='nan':return np.full(2,np.nan)
+            return self.chi*np.array([x[1]**2,x[0]**2])
+    for name,model,expected in [('ideal',Model(),'no_gap_on_grid'),('regular',Model(2.5),'refined_root'),
+        ('nan',Model(mode='nan'),'nonfinite_grid'),('error',Model(mode='error'),'grid_evaluation_failed')]:
+        audit={};value=fn(model,298.15,audit=audit);out[name]=dict(value=value,audit=audit)
+        assert audit['status']==expected
+        plain=Model(model.chi,model.mode);baseline=fn(plain,298.15)
+        assert baseline==value and plain.calls==model.calls,'Audit changed model call sequence'
+    for ier in (1,5):
+        def fake(fun,x,**kw):return np.array([.2,.8]),{'fvec':np.ones(2),'nfev':0},ier,'intentional mock'
+        ns['fsolve']=fake; audit={};value=fn(Model(2.5),298.15,audit=audit)
+        assert audit['status']==('refined_root' if ier==1 else 'coarse_hull_fallback')
+        if ier==1:assert not audit['residual_pass']
+        out['mock_ier_'+str(ier)]=audit
+    return out
+
+
+def p15(root):
+    text=(root/'src/zcosmo/pyscf_cosmo_v2.py').read_text()
+    assert 'replace(kw["restart"]["params"], energy_noise=2e-7)' in text
+    assert 'float(noise) != 2e-7' in text
+    assert 'A-R2-noise-aware-trust-2e-7-Eh' in text
+    return dict(option_and_restart_update_present=True,native_optimizer=False)
+
+
+def main():
+    ap=argparse.ArgumentParser();ap.add_argument('patch',choices=['P10','P11','P12','P13','P14','P15'])
+    ap.add_argument('--root',type=Path,default=Path.cwd());ap.add_argument('--out',type=Path)
+    a=ap.parse_args();answer=globals()[a.patch.lower()](a.root)
+    result=dict(patch=a.patch,kind='PORTABLE_ONLY_NOT_NATIVE_ACCEPTANCE',result=answer)
+    text=json.dumps(result,indent=2,allow_nan=False);print(text)
+    if a.out:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(text+'\n')
+
+if __name__=='__main__':main()
```

## Local verification evidence

```json
{
  "base": "eab6c2510264f7f3cf4db00cd1c247ad71500b14",
  "verified_git_blobs": {
    "src/zcosmo/pcm_lu.py": "f31533d998ed35a90349bfbe1e6553407fae5ee8",
    "src/zcosmo/pyscf_cosmo_v2.py": "7a5f723045d8e3c62c958daf696918b810c76811",
    "src/zcosmo/evaluate.py": "e154f0d9e695957a66c600e8211a0d0bca010c8c"
  },
  "checks": [
    {
      "patch": "P10",
      "independent_apply": true,
      "python_syntax": true,
      "portable_test": true
    },
    {
      "patch": "P11",
      "independent_apply": true,
      "python_syntax": true,
      "portable_test": true
    },
    {
      "patch": "P12",
      "independent_apply": true,
      "python_syntax": true,
      "portable_test": true
    },
    {
      "patch": "P13",
      "independent_apply": true,
      "python_syntax": true,
      "portable_test": true
    },
    {
      "patch": "P14",
      "independent_apply": true,
      "python_syntax": true,
      "portable_test": true
    },
    {
      "patch": "P15",
      "independent_apply": true,
      "python_syntax": true,
      "portable_test": true
    }
  ],
  "native_pyscf_executed": false,
  "gpu_executed": false,
  "post_P9_molecular_profile_executed": false,
  "install_attempt": "evidence/native-install.txt",
  "patch_sha256": {
    "P13.patch": "c87d4e0a8be3829ada127750971e09f76b3bed13f3608d3a814e94893cbd9090",
    "P15.patch": "ac1b622be354f7f31462b1acf16fc1528e79ae9fa3c62bbfb40fb4827ac4258b",
    "P10.patch": "0bf432e3e35c8966f19e497ecb90287f52e1481475f4f9a6f38461a17d513f3e",
    "P14.patch": "a440d842b7026122a89e4dade77497064c7e45efe243d67477f19a855ab90652",
    "H2.patch": "6fe11be4ccbe744158254ebaf47deb9d84797dc94a633c5f7986be94fd0fba08",
    "P11.patch": "539a595a2323109a4fb342c8925faa27ba9cc559dbe57f55ea128ca95f5c5817",
    "P12.patch": "e40ebc373810e425bb1185e0abdefb1fb4bda5e39be38d8e052ee1b36e31a218"
  }
}
```

## Source map

All S references are in `Victor-Liang-ChE/zcosmo` at `eab6c2510264f7f3cf4db00cd1c247ad71500b14`, unless the entry explicitly identifies the earlier report reference.

| Reference | Source |
|---|---|
| S1 | `docs/astra/ROUND2_PROMPT.md`, including September 29 addendum; blob `ea01aef1aa8161634fdf45842ca075a7b36bb8cb` |
| S2 | `docs/astra/round1/RESULTS.md`; original report `docs/astra/round1/ZCOSMO_OPTIMIZATION_REPORT.md`, blob `4fd5b5675e6aeffa465774a87065aa9a954a7a3a` |
| S3 | `PREREGISTRATION.md`, including GPU, P6, P9, replacement state gate and October 1 S1 records; blob `895b313463f1b1a8041431137831167e1fee7e32` |
| S4 | `src/zcosmo/pyscf_cosmo_v2.py`; blob `7a5f723045d8e3c62c958daf696918b810c76811` |
| S5 | `src/zcosmo/pcm_lu.py`; blob `f31533d998ed35a90349bfbe1e6553407fae5ee8` |
| S6 | `src/zcosmo/evaluate.py`; blob `e154f0d9e695957a66c600e8211a0d0bca010c8c` |
| S7 | `cloud/s19/qc_cycle_profile.py` and `results/qc/qc_profile/prof_octanol_t4_summary.txt`; profiler blob `490309b4958150bcaae9b5ba58fba329566ff208`, summary blob `aee1307cd885f61fa6688a84f94d5c668cfc0853` |
| S8 | `.github/workflows/profiles_v2.yml`; blob `73020ec8c12d351e0c877bc2be4a105b21e43c7f`; `cloud/s19/kaggle_lc.py`; committed seed directory |
| S9 | Corrected `docs/astra/round1/patches/H0.patch`; blob `4579efa8102928bfb8df556363aaaed6104f89e4`; original `docs/OPTIMIZATION_BRIEF.md` |
| U1 | `pyscf/pyscf`, tag `v2.14.0`, `pyscf/solvent/grad/pcm.py`, particularly `grad_qv` and `WithSolventGrad.kernel`; blob `7e81cbe95427171db013f44716e2ec0c3644dd2a` |
| U2 | `pyscf/pyscf`, tag `v2.14.0`, `pyscf/geomopt/berny_solver.py`, `pyscf/scf/hf.py` (`SCF_Scanner`), and `pyscf/grad/rhf.py` (`SCF_GradScanner`) |
| U3 | `pyberny/pyberny`, commit `8f200b868b5b42247cbac7e2c5cec27811671fdd`, `src/berny/berny.py`; `BernyState`, restart constructor, `send`, `update_trust`, `is_converged`; blob `cbecf60ce5b2d24c81c90454d2ddba2c586dd3af` |
| U4 | `pyscf/pyscf`, tag `v2.14.0`, `pyscf/lib/gto/fill_nr_3c.c`, `GTOnr3c_drv`; blob `71460ad1a1614303368ce8b6e502b2b9088492d5` |
| U5 | `pyscf/pyscf`, tag `v2.14.0`, `pyscf/df/df_jk.py` (`get_jk`) and `pyscf/df/df.py` (`build`, `reset`); blobs `30c6fb6e4f2a4f2f38a9f42c0e57354f8cccdb92`, `47c37775a00cc6176812b974adbec4931fc7cca6` |

The immediate next deliverable from a native run is the post-P9 trace and fixed-geometry P10/P11 checks, not another extrapolated large speed-up. Accept/reject records should include the flags, package freeze, resolved auxiliary basis, memory use and full finite-coverage gate.

