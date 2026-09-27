# Z-COSMO optimisation brief (for an external reviewer model)

Repo: `Victor-Liang-ChE/zcosmo`, snapshot of 2026-09-26. Read this file first, then the files it points to.

## What the project is

A fit-free COSMO-SAC-type activity-coefficient model ("Z0x") and an experimental direct route built on a
machine-learned potential. **No parameter may be fitted to experimental data.** Every model change is
pre-registered in `PREREGISTRATION.md` before it is scored against ThermoML. Read that file's rules before
proposing anything that would change a number the model produces.

Compute is free-tier only:

- GitHub Actions, 4-core runners with a 6 h cap each, 20 in parallel.
- Modal L4 (24 GB), limited free credits.
- Kaggle (4-core CPU, or a T4 GPU for 30 GPU-h per week, 12 h per session).
- Lightning T4.
- An M4 Pro Mac.
- A Windows PC with an RTX 2060 and 12 threads, running WSL.
- A Windows PC with an RTX 4070, not set up yet.

The goal of this review is to cut wall-clock time and compute cost in all three pipelines below, without
changing the physics. If a change would change the physics, flag it clearly as such.

## Rules for proposals

1. **Two classes, labelled.**
   - (E) Exact or numerically equivalent. Same functional, basis, grid, radii, solvent model and convergence
     meaning. The result must match the current code within a stated tolerance.
   - (A) Approximation. It changes results.
2. **Tolerances for (E).**
   - σ-profile bins: max |Δp| < 1e-4.
   - ln γ∞: < 1e-3 on the registered 25-molecule / 2,302-row check (`scripts/validate_pyscf_profiles_v2.py`).
   - MLIP forces: max |ΔF| < 1e-4 eV/Å against ASE's `MACECalculator`.
3. **(A) proposals must name the check that would accept them,** e.g. the median |Δln γ∞| < 0.15 acceptance
   test used for profiles v2. They are registered before use, never tuned against experimental data.
4. **For each proposal, give:**
   - target file and function
   - mechanism
   - expected speed-up with the arithmetic behind it
   - exactness or accuracy argument
   - a minimal unified diff against the current `main`
   - the exact command that benchmarks it and checks the tolerance
5. **Rank proposals** by (expected saving × probability it works) / effort.

## Pipeline 1: quantum-chemistry σ-profiles (the current bottleneck)

**Files:**

- `src/zcosmo/pyscf_cosmo_v2.py`
- `src/zcosmo/pyscf_cosmo.py`
- `.github/workflows/profiles_v2.yml`

**Method, fixed by registration:**

1. RDKit embedding, MMFF, then a GFN2-xTB gas-phase geometry (`tblite`).
2. BP86/def2-SVP geometry optimisation inside a conductor (C-PCM, ε = 1e9, Lebedev 17, project radii), with
   density fitting and grid level 2, using pyberny through `pyscf.geomopt`.
3. A BP86/def2-TZVP C-PCM single point (grid level 3, Lebedev 29, conv_tol 1e-9) that gives the surface
   charges.
4. Hsieh averaging and the NHB/OH/OT split into three 51-bin profiles.
5. Open-shell ground states (O₂) use UKS.

**Measured costs:**

- The median molecule takes minutes. Long flexible chains (C16–C20 fatty acids, esters and alcohols;
  perfluoroalkanes with 20–25 heavy atoms) take more than 6 h on 4 threads. Almost all of that time is Berny
  cycles.
- 598 of 636 profiles finished in the first round. 21 are still outstanding after three rounds.
- Checkpoint/resume of the Berny geometry was added on 2026-09-26: `*.partial.json` is written every cycle.

**Questions:**

- **Convergence and optimiser.** Are these the right algorithms and settings for fewer optimisation cycles?
  Consider:
  - geomeTRIC (TRIC internal coordinates) versus pyberny
  - an initial Hessian from GFN2-xTB or a model Hessian
  - optimising first at a cheaper level (xTB-ALPB conductor-like, or a smaller grid) and then only polishing
    at BP86/SVP
  - convergence thresholds relative to how much the σ-profile actually moves
- **Per-cycle cost.** Consider:
  - the choice of RI auxiliary basis
  - grid pruning
  - reusing the density matrix across Berny steps and from SVP to the TZVP guess
  - SCF convergence acceleration (ADIIS/EDIIS, level shift) for the problem cases
  - how the C-PCM gradient is evaluated
  - thread settings on 4-core runners
- **GPU4PySCF.** Could it do these exact calculations (same functional, basis, grids and C-PCM with custom
  radii)? We have L4, T4, RTX 2060 and RTX 4070 GPUs. What would reproduce our σ-profiles within tolerance,
  and what can't be matched?
- **Work distribution** across 20 parallel runners: currently largest-first round-robin, with resumption of
  checkpoints between runs.

## Pipeline 2: the COSMO-SAC evaluator (runs on every scoring pass: thousands of systems × T × x)

**Files:**

- `src/zcosmo/cosmosac.py`: `solve_gamma` is a damped successive substitution on a dense 153×153 matrix,
  tol 1e-10.
- `src/zcosmo/z0x.py`: Z0x differentiates g(x) by central finite differences because c_ES depends on
  composition. That means several `Mixture` builds and segment solves per point.
- `src/zcosmo/models.py`
- `scripts/eval_models.sh`
- `scripts/lle_parallel.py`

**Questions:**

- Newton or Anderson acceleration for the segment equations.
- Restricting the solve to the nonzero segments.
- Batched or vectorised solves over (T, x).
- An analytic derivative for Z0x (the model is a known function of x through φ-weighted ε).
- Caching.
- Can the whole scorecard run in minutes instead of hours on 4 cores?

## Pipeline 3: MLIP free energies (MACE-OFF23 small, float32, cuEquivariance)

**Files:**

- `cloud/s15/multi_mace.py`: many periodic systems in one disjoint graph, a GPU minimum-image neighbour list,
  a Verlet skin, and a per-step r < r_max edge filter.
- `cloud/s15/bench15_core.py`: two-stage cavity thermodynamic integration (TI) with all λ windows batched into
  one call; BAOAB Langevin; TI and MBAR estimators.
- `cloud/s14/fast_md.py`: half-edge symmetry, padding.
- `cloud/s14/bench11_core.py`
- `cloud/s14/zc_md.py`

**Measured on an L4:**

- One force call:
  - 192 atoms: 36.7 ms
  - 648 atoms: 36.3 ms
  - 5,184 atoms: 72 ms

  The engine is launch/overhead bound.
- Batching many systems into one call:
  - 16 × 192 atoms: 2.8 ms per system
  - 8 × 648 atoms: 9.3 ms per system
- Features:
  - Half-edge symmetry: exact, but only +12% at 5k atoms.
  - `torch.compile(mode="reduce-overhead")` with padding: failed (empty exception).
  - A distilled student for surrogate HMC: only 1.5× cheaper per call, so not worth it.
- Free-energy runs:
  - 28 λ windows × 192 atoms per call: 114–125 ms per step.
  - With methanol as solvent (384 atoms per box): 234 ms per step, with CUDA OOM warnings at about 16.5k nodes.
- Statistics: 30 ps per window gives a TI SE of about 0.23 kcal/mol. dU/dλ autocorrelation times reach 1.7–2.5
  ps at λ 0.6–0.85 and at small μ.

**Questions:**

- Making CUDA graphs work: static shapes, a padded edge list, the cuEq kernels, the autograd force path.
- Fusing the neighbour-list rebuild and filter.
- Memory, to fit more windows or replicas per call.
- Energy/force precision (float32 with interaction energies).
- **Statistical efficiency, likely the biggest lever:**
  - Hamiltonian replica exchange between λ windows, nearly free because every window is already in one batch
  - Gibbs sampling in λ, or expanded ensemble
  - better soft-core or WCA path constants for lower variance, where only variance changes and the endpoints
    stay exact
  - multiple-time-step integration
  - larger time steps with hydrogen mass repartitioning (and its effect on free energies)
  - optimal window placement from thermodynamic length
- What cost per ln γ∞ is realistic on these free GPUs?

## What to return

A single markdown answer containing:

1. The ranked table: id, pipeline, class E/A, expected speed-up, effort.
2. For each item, a diff plus a benchmark and check command.
3. Anything in the current code that you think is wrong or wasteful: bugs, redundant work, wrong defaults.

Keep proposals concrete enough to apply and test in one step. The maintainer's assistant will apply them,
benchmark them on the free hardware, record accept/reject against the tolerances above, and report back.
Later rounds will include those measurements, so proposals can be iterated.
