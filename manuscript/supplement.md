# Supplementary evidence and source qualifications

This supplement accompanies the R17 manuscript-only revision. It records completed work; it
authorizes zero new quantum calculations and zero activity-model requests. Original registrations,
scorecards and RESULTS files remain unchanged. Section labels from earlier drafts are preserved in
descriptions so that historical claims can be located. Numerical statements below are attributed to
existing records, not to a new data analysis. Source status is recorded in
docs/astra/round17/CLAIMS.json.

## S0. Historical statistics requiring source qualification

The main historical table combines multiple property-specific sources. Its seven non-HANNA IDAC, VLE
and HE entries match main7 after rounding. Its test_both column matches test_both/main7. The early
LLE balanced-accuracy summary is supported by the contemporaneous progress record, which describes
the advantage as significant. The exact original bootstrap output and the separate historical HANNA
test arrays were not recovered in the reviewed public files. Recovering these already-generated
artifacts is an editorial provenance task. No rerun, fresh bootstrap or model call is authorized by
this note.

The original draft printed Z0-minus-COSMO-SAC IDAC [-0.17, +0.08] and VLE [+6.6, +14.5]. The former
is compatible with main6 rounding, and the latter with results/scorecard_test.md; neither is the
interval of the named main7 source. It also printed test_both [-0.54, -0.22], which does not
reproduce the main7/test_both interval [-0.552, -0.229]. The corrected prose names main7 and uses
its stored values. All original scorecards remain immutable; the edit repairs citation/version
assignment, not results.

The following old precision remains a historical draft assertion pending the existing source
artifact, not a freshly verified inferential result: LLE BA Z0-minus-COSMO-SAC [+0.02, +0.11],
Z0-minus-UNIFAC [+0.04, +0.14], Z0x-minus-COSMO-SAC [+0.02, +0.11], Z0x-minus-UNIFAC [+0.03, +0.13],
and Z0x-minus-HANNA [-0.03, +0.07]. The old binodal comparison was 0.05 versus 0.18; its exact
endpoint denominator and source artifact remain required. The historical HANNA row was IDAC 0.24
(including 0.24 on test_both), VLE 7.1% (median 2.1%), HE 70 J/mol and BA 0.88. Preserve these
reported values, but do not substitute another subset to reconstruct them. An interval containing
zero indicates no resolved difference, not equivalence. The manuscript's quantitative table is
explicitly marked historical.

## S1. Open profiles and numerical infrastructure

An open pipeline (PySCF BP86/def2-TZVP, C-PCM conductor limit, xTB geometries, NIST averaging and
splitting) was checked against the NIST/DMol3 profiles before use. On the registered
25-molecule/2,302-IDAC-occurrence check the median change in COSMO-SAC-dsp ln gamma_inf was 0.153,
just above the pre-set bar of 0.15 (water 1.14, triethylene glycol 0.84), with reported experimental
MAEs 0.79 versus 0.74. The profiles were therefore not merged into the main benchmark. On the 136
previously uncovered compounds (exploratory, 218 IDAC points in 72 systems), Z0 and Z0x reach MAE
0.68 and 0.69 against 1.00 for COSMO-SAC 2010, 0.94 for COSMO-SAC-dsp, 0.55 for UNIFAC (79%
coverage) and 0.11 for HANNA.

Later v2 conductor-optimized profiles passed the original median agreement gate at 0.1493, only
0.0007 below 0.15, and were retained as exploratory rather than an accuracy-equivalent UD
replacement. The frozen population contains 630 files passing the original Berny predicate and six
separately flagged S1/S2 files. The R2-R9 numerical review preserves accepted performance changes
and rejected trials; optimizer-state persistence is not relabeled E after its E gate failed. Omitted
XC-grid response and the incomplete earlier finite-difference referee limit stationarity claims. The
corrected-gradient rollout failed P32's compatibility gate, and the TEG energy-gradient mismatch
remained unresolved when the R8/R9 diagnostic budget closed. There is no accepted blanket re-polish
or chain rescue. See `docs/astra/round7/RESULTS.md`, `docs/astra/round8/RESULTS.md` and
`docs/astra/round9/RESULTS.md`.

 The original median comparison is an input-compatibility gate, not proof of identical predictions.
R6/P31 reproduces the later matched-input errors: IDAC 0.8040 (UD) versus 0.9423 (open630) on 816
observations, paired difference CI [0.0506, 0.2379]; VLE 15.90% versus 16.41% on 12,403
observations, CI [-0.75, 2.10]; and HE 618.6 versus 699.3 J/mol on 8,573 observations, CI [50.9,
108.8]. Thus VLE has no resolved difference in that comparison, while the displayed IDAC and HE
differences favor UD. These are different subsets from main7 and precede the opt-in P28 endpoint
correction.

R6 accepted P28 on numerical grounds: maximum error 2.73e-9 against a 1e-8 reference gate and
measured endpoint speed-up 3.06-3.25. The corrected test IDAC MAEs were slightly larger, not
optimized for error: UD 0.8394 to 0.8397 and open630 0.9423 to 0.9427. Historical endpoint tables
remain unchanged.

R7 resolved omitted-response errors in three sampled directions, but no case passed an all-direction
stationarity certificate. P32's maximum dsp change was 0.0121 against the strict 0.01 compatibility
limit, despite both arms reaching the original Berny predicate. The pilot and chain stage did not
run. P34 requested 40 cases: 35 stress-positive, four unresolved and one missing. Its 0.01 angstrom
imposed displacements measured sensitivity, not the unknown distance to a corrected optimum. The
incomplete probability sample supplies no population bound. R8/R9 closed the remaining TEG
diagnostic as unresolved; the tiny retained switching weight did not establish a one-node cause for
the finite-difference collapse.

R2-R4 accepted performance changes and metadata operations retain their individual E/A labels and
checks. In particular, the failed E classification of optimizer-state persistence is not reversed;
its A acceptance is a different record. P20 protects exactly 630 primary, one S1 and five S2
selected profiles, rather than every superseded file in those folders. Gap witnesses in the later
LLE audit support detection only; they do not supply converged endpoint compositions. These controls
do not restore a general numerical-stationarity claim for the historical open-profile geometries.

Sources: docs/astra/round2/RESULTS.md through round9/RESULTS.md, the complete PREREGISTRATION.md,
and results/scorecard_all_gap_exploratory.md. Detailed profiles and relevant execution assets remain
private on the Mac; the public aggregate audit is not a replacement for native acceptance.

## S2. Conformer and glycol evidence

For the 50 most flexible benchmark molecules (4.9 conformers on average, BP86/def2-SVP profiles),
replacing the lowest-energy conformer by the Boltzmann ensemble changed predictions very little:
median |d ln gamma_inf| 0.009 (COSMO-SAC-dsp) and 0.011 (Z0x), 90th percentile under 0.09, and the
original draft reported IDAC MAE difference [0.00, +0.01] and VLE [-0.35, +0.32] points. Those
rounded intervals alone do not establish equivalence or even reveal the unrounded lower IDAC bound.
The lowest conformer carries 60% of the weight on average. This establishes a small effect for that
finite proposal and weighting scheme, not the absence of conformational effects or a validated
phase-dependent ensemble.

R10 recovered and replayed all twelve fixed-panel UD raw files to their historical profiles. R11's
ordered open-method cross attributes the polar-tail gaps for ethylene, diethylene and triethylene
glycol mainly to stored coordinate inputs, including hydrogen positions and orientation.
Tetraethylene glycol is an exception: its raw-tail gap was mainly method, and its other tail
contrasts were small. No member passed the registered whole-profile attribution rule. These
statements retain R11's original labels.

R12/P46a then scored exactly 142 already-inspected glycol-solvent observations with original open
solutes and a common P28 endpoint. Pooled MAE in ln gamma_inf was 1.813 for the original open
solvent profiles, 0.702 for the open method at the recovered UD coordinates, and 0.419 for UD
solvent profiles. The coordinate-derived substitution removed 1.111, about 80% of the open-to-UD
comparator MAE gap and 61% of the original open absolute error; 139 rows improved and three
worsened. Shape carried essentially all of the factorial error reduction. Tetraethylene glycol
recovered only 13% of its comparator gap. The remaining 0.283 is a conditional difference of MAEs,
not a universal method-error estimate. P47 located same-geometry method differences toward the
acceptor side and the EG/DEG/TEG coordinate differences toward the donor-side tail; those partitions
are not hydrogen-bond energies or binwise error causes.

This was retrospective explanatory ThermoML scoring. The UD notice reports database-level revisions
using vapor-pressure predictions without identifying which panel members were revised. The result
does not establish extended chains as the liquid conformations or adopt a geometry rule. P35 closed
after R13 with its explanatory finding; the liquid distribution remains unresolved and all 630+6
open files remain frozen. See `docs/astra/round10/RESULTS.md` through
`docs/astra/round13/RESULTS.md`.

 The 50-molecule/244-conformer description and median approximately 0.01 are corroborated by
PROGRESS.md. The more precise 0.009/0.011 medians, percentile, weight and interval statements above
retain the old draft's numerical record, but their cited private queue log
(_queue/done/26_conformer_eval.sh.log) was not read in R17. They are not marked independently
verified. R5/P26's later incomplete proposal pools did not accept an ensemble or invalidate the
earlier finite-pool record.

R10 verified twelve raw-file/profile lineages, not exact electronic input decks. R11's attribution
is ordered, because the reverse UD-method/open-coordinate corner was not computed. The 0.359
normalized- shape background was control-derived, not stochastic numerical noise. R12/P46a fixed EG
at ten rather than nine observations by exact identity before scoring; the total is 142, not the
superseded 141. Every solute remained the original open input, and the primary comparison used P28
for all arms. R13 closed the explanatory campaign with the liquid-state mechanism unresolved.
Nothing authorizes using extended UD conformations because they reproduce the already-inspected
result.

Sources: docs/astra/round5/RESULTS.md, round6/RESULTS.md, and round10/RESULTS.md through
round13/RESULTS.md.

## S3. Association failures and simulation provenance

Z0w replaces the COSMO hydrogen-bond term by Wertheim TPT1 association with site-pair strengths
Delta_AB = (kT/P0) exp(-dG_AB/RT), where dG_AB is the dimerization free energy from the B3LYP-D4
binding energy plus GFN2-xTB quasi-RRHO thermochemistry (registered before any prediction). As
registered it fails: held-out IDAC MAE 0.97 vs 0.80 for Z0x and VLE AAD 27.4% vs 15.2%, and it
predicts false liquid-liquid splits in 9.4% of miscible test systems (balanced accuracy 0.90,
unchanged, because it finds more real splits). The historical interpretation identifies the largest
errors as aqueous: organic solutes in water are overpredicted by 5 to 7 in ln gamma_inf. Post hoc,
on non-aqueous systems only, the historical draft reports smaller Z0w errors among its listed
comparators (test IDAC MAE 0.67 vs 0.88 for COSMO-SAC 2010, bootstrap difference [-0.29, -0.09]; vs
Z0x [-0.17, +0.04]). A proposed diagnosis is the gas-phase entropy in dG: bonding to a larger
partner costs more rotational entropy (water-acetone -121 J/mol/K vs water-water -87 J/mol/K), which
makes cross-association about ten times weaker than water self-association and turns water into an
unrealistically closed network.

 The overall stored IDAC difference interval is [-0.035, +0.400] on 762 observations / 177 systems
(results/scorecard_test_z0w.md); the failed registration is not a claim of a resolved overall IDAC
increase. The specific non-aqueous interval endpoints in the old paragraph require their already-
computed private artifact before submission. PROGRESS.md corroborates the rounded non-aqueous means
and historical VLE failure. The -121 and -87 J/mol/K examples are supported by the stored
results/qc/assoc_thermo.csv entries. This is the model's gas-phase thermochemistry, not a measured
liquid bonding entropy or a proof that no other term contributed to the failure.

 The association constants that a continuum or gas-phase dimer calculation cannot supply can be
measured directly in simulated liquids. We use MACE-OFF23 (small), a machine-learned interatomic
potential trained only on DFT reference data, as a teacher. Speed was the obstacle: the stock ASE
path managed 0.37 ns/day for 648 water atoms on an NVIDIA L4. Three exact changes remove most of it.
The first is NVIDIA's cuEquivariance fused tensor-product kernels (forces identical to 2-4e-6 eV/A).
The second is batching many small boxes per GPU. The third is a lean integrator that feeds the model
directly, with a Verlet neighbour list whose superset is filtered to the cutoff every step. This is
exact because MACE's radial envelope is identically zero beyond r_max. Aggregate throughput reaches
8.9 ns/day (about 24x), with every change checked against reference forces. Two approximations were
rejected by pre-registered gates: TF32 arithmetic (force error 3e-3 eV/A) and hydrogen mass
repartitioning with 1-2.5 fs steps (energy drift 2.3-183 times the 0.5 fs reference). Z0w3 inverts
TPT1 on hydrogen-bond statistics from NPT simulations of seven liquids at three temperatures
(PREREGISTRATION.md, session 5b). The registered short water controls were inside their stated
acceptance window (water 87% bonded, 1.115 g/cm3; an independent engine gives 86% and 1.10), but
Z0w3 fails badly: temporal IDAC MAE 2.19 against 1.45 for Z0x, aqueous test systems 4.79 against
1.76. The simulated association is strong (water Delta about ten times the gas-phase dimer value).
Overlap with electrostatic contributions in the COSMO reference is a plausible architectural
explanation. The explicit COSMO hydrogen-bond constants were already zero in Z0w and its
descendants, so merely turning that term off is not a new solution. The nitrogen-site occupancy
mismatch and temperature-fit failures also matter. The failed registrations stand; neither a unique
double-counting decomposition nor a successful replacement architecture was established.

A later, separate source regression must not be confused with these historical failures. Since P6,
Z0x's optimized interior dispatch bypassed the association subclasses' _g overrides; enabling P28
could do so at pure endpoints as well. Archived Z0w/Z0w2/Z0w3 scores predate that change. P55's
separate repair restores full-subclass-g finite differences, including the historical one-sided
endpoint approximation; it does not supply an exact association endpoint or a new association score.
Software regression tests and any future physical validation are reported separately. No fourth
association variant is accepted.

 The equivalence language above concerns the checked energy/force evaluation paths. It does not
prove that finite-step thermostatted dynamics samples an exact equilibrium distribution, or that an
energy/force-trained potential predicts accurate chemical potentials. The MACE-OFF23 weight file,
execution environment and corresponding primary model publication need exact version citations in
the submission archive. R17 does not invent them or rerun simulation. The HMR and TF32 failures
remain recorded under their original criteria, and the historical Z0w3 scores predate the P6
dispatch defect.

Sources: PREREGISTRATION.md session 5b and speed-up results, PROGRESS.md session 5,
docs/astra/round14/RESULTS.md and round15/RESULTS.md. The original NPT driver and several detailed
score/bootstrap outputs are not asserted to be reconstructible from the public checkout alone.

## S4. Exposure, amendment and failure ledger

R2-R9 contain performance trials, failed stationarity/compatibility gates and an unresolved
numerical closeout. R10-R13 contain recovered input lineage and exposed glycol explanations. R14's
experimental- epsilon oracle and R15's fitted-ingredient cube are diagnostics. R16's LV1 is a
complete but failed registered A screen. These are not pooled into one newly held-out experiment.
P46a, P52a and P58a were input-integrity amendments made before the respective affected model calls,
and their superseded preparation attempts remain in the original records. No R17 editorial action
changes an acceptance gate, denominator, stored number or model default.

The submission lead should be historical IDAC comparison, historical LLE detection, VLE/HE losses,
then P54 and its LV1 negative follow-up. The infrastructure narratives above can be supplementary
sections referenced by one paragraph each in the main text. Current subsection numbers are retained
in this review patch so the requested additions remain in 3.11; typesetting renumbering may follow
without changing results. See the R17 audit for the exact proposed reading order and figure
inventory.
