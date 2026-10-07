R10-P41-P42-P43: UD provenance, zero-QC replay

Proposed registration. Append adopted text to PREREGISTRATION.md with the actual
commit identity before acquisition or comparison. This file alone is not an
acceptance record. The reviewed baseline is
4dc898521f6c49355e442be78f1e2570d3686aee. R8/R9's numerical-gradient campaign
remains closed. P32 remains failed; no stopped chain is restarted. P35 is opened
only for provenance acquisition and a descriptive same-parser comparison, not
for a claim that its physical mechanism is resolved.

The public source locations and raw Git blob identifiers were discovered during
this review. No new quantum computation or UD/open numerical comparison was
performed in that review. The design is motivated by previously inspected R4-R9
results, not a new experimental holdout. No ThermoML response, UD tail target or
conformer energy selects a parameter or a member.

P41 is E acquisition and integrity checking. Use only the twelve raw `.cosmo`
files and two provenance documents in scripts/r10_sources.py at public NIST
COSMOSAC commit 1b82456be38026719b16cad4076109bef3fcb309. Verify the exact Git
blob for each download and record a SHA256 of its bytes. Preserve line endings.
One request per file, a 30-second socket timeout and an 8 MB per-file ceiling;
no alternative source, automatic retry, file replacement or incomplete-success
claim. Retain every failed acquisition status. The twelve compounds are water,
methanol, EG, DEG, TEG, tetraethylene glycol, glycerol, propylene glycol,
2-methoxyethanol, 1,2-dimethoxyethane, THF and n-nonane, as in the fixed R5 panel.

The data notice is independent of any repository code license. The operator
must review applicable use rights and acknowledge them before acquisition.
Neither this registration nor public availability grants redistribution or
commercial-use permission. Downloaded data and detailed derived reports remain
outside the repository on the Mac. Do not place raw data, geometries or dense
replayed profiles in public Actions artifacts. This round launches no Actions
computation; downloading already-existing P25 artifacts is retrieval only.

P42 is E read-only input comparison with same-input numerical replay gates.
Before calculating descriptors, freeze the source files and all original
630+6 profile hashes. Freeze the twelve saved generating geometries and exactly
one original P25 TZVP/SWIG result per key. Match native geometry hashes against
cloud/r5/shape-plan/manifest.json and coordinates against both the stored NPZ
and primary saved JSON. Match each archived P25 Hsieh profile and Mac UD profile
to the SHA256 already recorded in p25_stage_comparison.csv. Missing, conflicting,
changed or duplicate sources stop preparation. No newly generated raw table
may silently replace an absent artifact. If archived artifacts are no longer
available, report that limitation; do not rerun their SCFs under this budget.

Match compound identities using the public list and the project's
ud_complist.csv, with explicit source and target keys. Propylene glycol maps
benchmark DNIAPMSPPWPWGF-UHFFFAOYSA-N to published
DNIAPMSPPWPWGF-VKHMYHEASA-N. This follows the existing unique-connectivity lookup
and is an explicit stereochemical limitation. Never use embedded .car numbers
as compound-list identifiers, or choose among ambiguous skeleton matches.

The external manifest records all input hashes, reviewed code hashes and the
normalized Mac package versions. Commit its SHA256, and only that SHA256, in
docs/astra/round10/PLAN_SHA256.txt before the first comparison. Pass that actual
plan commit to the comparison command. The actual registration commit must be
an ancestor of HEAD and contain this marker. The frozen source files and inputs
are checked again before and after the comparison; package drift blocks it.

Use the reviewed project to_sigma.py Git blob
9f2e0d6f3bb4da4880f9bd6ad702847f9308ed1d for both paths. Parse historical UD
DMol3 output using Dmol3COSMOParser(num_profiles=3, averaging='Hsieh'). Adapt
archived retained open segments using the existing r4_common.parser_trace.
Keep the 0.52917721067 Bohr-to-angstrom conversion and existing Hsieh and HB
constants. Read the actual charge column and recompute charge/area; do not use
the rounded printed density instead. Do not neutralize charges, choose a
correction column by closeness to a reference, clip a sigma, change atom
classification, or tune averaging. No new surface filter is applied to the
archived open table. A parser exception is a failed replay, not permission to
alter the parser in the same experiment.

Require every replay to reproduce its own stored 153-bin area profile with
maximum absolute difference strictly below 1e-8 square angstroms. UD area,
volume, averaging metadata and dispersion metadata must also match their
historical values at the stated 1e-8 numeric tolerance. Require binwise HB-area
conservation and total retained area within 1e-8 square angstroms. This is a
same-input integrity gate, not an E claim that open and UD physical profiles
match. There is no experimental accuracy acceptance criterion or model scoring
in R10. Primary-versus-P25 differences are reported separately and never used
to replace or relabel a primary file.

Only after a member passes its lineage/replay gate, compare its geometries and
raw distributions. Check observed covalent connectivity against declared RDKit
structures. Retain every heavy-atom graph isomorphism, with an explicit ceiling
of 256 that fails rather than truncates a symmetry search. Report each proper-
rotation heavy-atom RMSD and its heavy-chain and H-O-C-X dihedrals. Do not reflect,
reorient or modify a geometry used for charge averaging. Symmetry correspondence
is not conformer generation; graph matching does not certify stereochemistry.

Retain the existing contact definition from r4_common: donor-acceptor distance
at most 3.2 angstroms, H-acceptor distance at most 2.5 angstroms and D-H-A angle
at least 120 degrees. Report all candidate contact geometries and the indicator;
never interpret the indicator as an H-bond energy or exclude a structure using
it. Water and the branched-polyol controls remain in the panel even when their
responses differ from those of the linear glycols.

Report raw charge sums and area-weighted sigma distributions, then the
averaged distribution and pre/post-HB bins. Distinguish the raw tessera tail,
averaged continuous-segment tail and unnormalized final binned-profile tail.
The fixed tail threshold is absolute sigma at least 0.01 e/A^2, inclusive on the
rounded three-decimal output grid. Preserve normalized-profile distances and
atom-resolved areas. Do not pair tessera rows from different surfaces by ordinal.
Preserve original and corrected printed charge summaries and a rounding-only
charge-sum screen; that screen does not assign a new physical convention.

Read cavity metadata literally. Record the input setting called "Number of
Segments" separately from the actual table count, and record the embedded
.car name without treating it as a modern index. The public papers and tutorial
establish nominal electronic-method context. Mark per-file electronic-deck and
solver-history verification as absent unless independent exact records have
actually been obtained. File-header metadata cannot fill in an absent method.

All twelve requested identities retain outcomes. A failure blocks that member's
scientific comparison, while independent members continue. Overall success
requires all twelve lineage gates, exact input integrity and zero native/model
calls. A partial panel is labelled partial. No helper writes a .sigma file to a
production directory or changes an existing input. The budget is zero SCF calls,
zero quantum gradients, zero model evaluations and zero conformer searches.
There is no automatic native continuation, basis sweep or histogram-matching
stage. Code-only synthetic tests may run before registration and off the Mac;
actual UD-backed acquisition and replay run on the Mac.

Interpretation: successful replay links the public raw input to the historical
Mac sigma profile within tolerance. Different geometry with different raw
charge distribution identifies a joint historical difference, not its causal
partition. Identical geometry but different raw distributions points to the
remaining electronic/cavity representation, subject to the provenance checks.
A coordinate-only comparison cannot prove the equilibrium liquid distribution.
No observed difference selects a conformer or establishes that UD is the truth.

P43 is E reporting. Add a dated provenance update without rewriting historical
numbers or failed registrations. Clarify that prior raw-input absence described
the Mac holdings, and that P29's raw area-profile tail is not a pre-averaging
raw-segment tail. Record the public notice's empirical conformation-selection
history without asserting which glycol was revised or alleging ThermoML leakage.
Retain the statement that Z0x was not fitted to ThermoML, with no broader claim
that every upstream input was wholly uncalibrated. The physical glycol mechanism
remains unresolved. The frozen profile version and all earlier numerical
acceptance/rejection decisions remain unchanged.
