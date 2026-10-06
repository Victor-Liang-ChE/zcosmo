# Proposed round-5 registration

This is proposed text, not evidence of registration. Append adopted text to
PREREGISTRATION.md with the actual commit timestamp before inspecting new
native outputs or scores. Reference code is main at
69b49116c2ae7574d7ae471f0a4ed7ba33d0db8b plus the archived R5 patches.
The experiment is motivated by already observed glycol, water and charge
sensitivities. It is not a fresh experimental holdout. Nothing is fitted to
ThermoML, and no recipe is selected by experimental error. P20 remains applied;
P23's accepted accounting remains; P15/P17/P19 rejections and S1/S2 labels stand.
The six-chain completion campaign remains closed.

P24 is an E component-accounting diagnostic of the unchanged Z0x implementation,
plus explicitly A electrostatic/HB-off interventions. Reproduce the frozen P22
859-row panel in separate processes for native, area-zero and capacitary-zero
profiles, with a complete unchanged open background. Also substitute only the
normalized UD shape, retaining native area and volume, for each of the six
fixed P22 molecules in separate arms. Do not pass experimental response values
to these workers. Decompose the actual one-sided h=1e-4 endpoint expression
into combinatorial, residual and London terms. Require total parity <1e-9 and
invariance to H2O/COOH flag relabeling <1e-10 in Z0x. Report the frozen-c exact
endpoint and h=1e-5/1e-6 controls; these do not replace the production stencil.
Use all four ES/HB on/off kernels and symmetric Shapley attribution, retaining
the interaction and finite masks. This is a model sensitivity decomposition,
not separately measurable ES/HB free energies. It does not adopt a neutrality
convention. All baseline and candidate coverage differences are failures of
comparability, not permission to discard unfavorable queries.

P25 freezes the twelve structures in r5_common.PANEL before new computation:
water, methanol, ethylene/diethylene/triethylene/tetraethylene glycol, glycerol,
propylene glycol, 2-methoxyethanol, 1,2-dimethoxyethane, tetrahydrofuran and
n-nonane. Resolve by stereo-aware canonical SMILES; ambiguous matches must
resolve to the exact structure-derived InChIKey or fail. These are structural
homologues and controls, not a claim that their historical errors were unseen.
Freeze saved geometry bytes; never invent the missing UD conformer. A separate
validation panel is the first eight SHA256('R5-validation-v1|'+InChIKey)-ordered
neutral, closed-shell, single-component covalent CHO structures with at most 13 heavy atoms, at least two rotatable bonds,
and either two OH groups or an ether, excluding the twelve and the historical
25. Insufficient eligible members or missing generating geometries abort the
plan. Freeze the manifest and package versions before native outputs.

On each of the twelve saved geometries, run three fixed single-point methods:
BP86/def2-TZVP/SWIG, BP86/def2-SVP/SWIG and BP86/def2-TZVP/ISWIG. All use the
project radii, C-PCM eps=1e9, Lebedev order 29, grid level 3/default pruning,
conv_tol=1e-9 and PySCF 2.14.0. The latter two are A diagnostic arms, not claims
of reproducing DMol3. Record the resolved auxiliary basis. At most 36 single
points, at most one hour per call. Reuse previous segments only on matching
geometry and method hashes. No density quadrature or new rotation recipe is
part of this trial.

For each saved segment table, retain raw charges and owner areas, the Hsieh
averaged sigmas, pre-HB bins and post-HB bins. Independently implement the
existing Hsieh formula and require max sigma difference <1e-10 e/A^2 and
binwise pre/post-HB total agreement <1e-8 A^2. Diagnose the segment-size effect
by the exact compressed equivalent of four coincident A/4,q/4 patches, and
by its point-patch limit. Both are A diagnostic sensitivities, not physical
remeshing or approved new averaging methods. The raw table is unchanged;
no out-of-range sigma is clipped into a usable profile. The existing radius,
decay and HB parameters are not adjusted. Compare stage distributions and
stored UD final shapes without using experimental responses. Missing UD
geometry prevents unique historical attribution and is reported as such.

P26 is conditional. Generate proposals with two fixed RDKit ETKDGv3 pools,
32 embeddings per pool, seeds 20261005 and 20261006, one thread, maxIterations
1000, pruning disabled. Pin the RDKit version recorded in the manifest.
MMFF94s, at most 500 iterations, supplies proposals only. A failed embedding or
MMFF member blocks that pool; there is no alternative seed or force-field
fallback. Select the lowest-MMFF proposal followed by three greedy farthest
proposals, using fixed-atom-order properly aligned heavy-atom-plus-donor-H RMSD.
RDKit/force-field priors are empirical proposal machinery, not fitted benchmark
model parameters. Each selected start is optimized by the unchanged registered
BP86/def2-SVP/DF/grid-2/C-PCM-17 CPU Berny path, at most 80 gradient evaluations
and one hour per proposal including the TZVP profile. PySCF=2.14.0 and
pyberny=0.7.0. Fresh histories; no P15 noise override, no P19 tight stage,
no optimizer pickle, no altered convergence predicate. All members must pass
Berny's actual convergence test and preserve covalent connectivity. Failed or
censored members are not omitted. The TZVP profile uses the accepted P18 flag.
Keep the converged orientation. O-H...O contacts use the already registered
geometric definition and are reported, never filtered or rewarded.

First run ranks 0 and 1 in each pool for the ten non-rigid structural panel
members, at most 40 optimizations. Water and methanol are rigid controls.
The full conformer protocol is authorized only by a prospective continuation
record when this probe contains reproducible distinct low-energy structures:
at least one pair within 3 kcal/mol of the sampled minimum, RMSD >=0.2 A,
and normalized-profile L1 >=0.02; report pool agreement and the other controls
without selecting a molecule by experimental error. This is justification for
further sampling, not proof that a conformer explains UD's historical profile.
Cross both pool winners on the same additional single-point methods when
separating method/conformer interactions, at most 40 extra single points.

If continued, complete all four proposals in each pool, reusing the already
computed members, and run the same full protocol on all eight separately
selected validation molecules. Select by lowest TZVP conductor electronic
energy alone, ties within 1e-7 Eh by frozen proposal rank. Do not assign
Boltzmann weights from embedding frequency or electronic energy, and do not
claim a global minimum or a temperature-dependent conformer ensemble.
The theoretical reproducibility gate requires all full pools to complete;
per molecule, independent pool minima must agree within 1e-4 Eh, aligned
heavy-plus-donor-H RMSD <=0.15 A, and normalized 153-bin L1 <=0.02. The selected
energy must not exceed the saved-geometry TZVP reference by more than 1e-4 Eh.
All eight validation members must pass. On fixed water/methanol/nonane/
dimethoxyethane probes at 250, 298.15 and 400 K in both solute/solvent roles
(192 queries), both models must be finite in both pools and maximum pool
prediction difference must be <0.02 for Z0x and COSMO-SAC-dsp. The full separate
validation budget is 64 worker-hours on four-core workers, with the per-member
80-evaluation/one-hour cap. Do not extend a censored member after reading it.

A pass establishes only computational reproducibility of a sampled-conformer
protocol. It permits one separately authorized exploratory experimental report
using the already frozen selections, not promotion of the 630 primary profiles.
The exact baseline profiles and all S1/S2 files remain read-only. Any future
conformer arm has its own directory and identity. A new claim of improved
experimental accuracy must report the fixed full comparison and paired CIs,
including water and the branched controls, whichever direction they move.
No best-error choice among conformers or recipes is allowed.

P27 regenerates Z0x, COSMO-SAC 2010 and COSMO-SAC-dsp in three separate profile
arms: UD, the 630 primary open profiles, and the 636 open profiles including
S1/S2. Every model/arm runs in a fresh process. Use the unchanged evaluate
formulas on the historical has_sigma universe for each table; attach immutable
row identities and freeze every source file/profile hash. Open630 marks the six
flagged compounds excluded by design, without falling back to UD. Report
standalone coverage and pairwise UD/open common subsets, never a hidden
intersection across all nine arms. All raw counts are written from the actual
frozen CSVs. Expanded non-UD coverage is a different table.

For LLE, reuse the previously tested P14 hook without changing its predictions,
then the accepted P23 thresholds, grids, 4000-call budget and old 2-K rounding.
For each arm first require the first 20 sorted good-call controls to retain
checked roots within 1e-4 of the legacy endpoints. Failure or fewer than 20
controls blocks that arm and is reported. Retain roots, gap witnesses, finite-grid
no-gap results and unresolved results as different statuses. Never give a
witness an endpoint error or turn an unknown into miscibility. Endpoint MAE
has its own explicit denominator. Report operational detection bounds and
system-majority bounds, not global phase-equilibrium certificates. This extends
accepted numerical accounting to additional profile/model arms; it does not
assume that UD repairs validate open-profile endpoints.

IDAC uses absolute ln-gamma errors and solvent-ranking rules already in metrics.
VLE uses the same psat source and homogeneous-liquid exclusion, with its own
coverage. HE uses the same 0.5 K central difference and sign threshold. System
bootstrap uses 1000 resamples, seed 7 reset per statistic/comparison; this is the
same estimator with explicitly fixed draws, not a promise of bitwise identity
to older CIs generated by the global RNG stream. Keep historical scorecards,
including 0.800/762 and 0.839/828, unchanged. Regenerated VLE/HE values are not
reported until the actual files exist. The reused experimental data are not
represented as a fresh holdout. Save all outputs outside historical results.
