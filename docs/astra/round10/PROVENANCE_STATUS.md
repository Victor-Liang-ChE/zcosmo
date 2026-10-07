UD glycol provenance, source discovery only

The public NIST COSMOSAC distribution at commit
`1b82456be38026719b16cad4076109bef3fcb309` contains DMol3 `.cosmo` files for
all twelve members of the fixed R5 panel. The reviewed zcosmo baseline is
`4dc898521f6c49355e442be78f1e2570d3686aee`. Exact paths and Git blob identifiers
are in `scripts/r10_sources.py`; `catalog` prints the pinned retrieval URLs.

[The public raw directory](https://github.com/usnistgov/COSMOSAC/tree/1b82456be38026719b16cad4076109bef3fcb309/profiles/UD/cosmo)
contains embedded atomic coordinates, surface positions and charges, with
per-atom radii and printed cavity settings. For EG the embedded `552.car` is
not the current compound-list identifier: the project index uses 552 for a
different compound. Source filenames, explicit molecular identities and hashes
must govern the mapping. An input setting labelled "Number of Segments" is
also distinct from the actual surface-table row count.

The propylene-glycol source is `DNIAPMSPPWPWGF-VKHMYHEASA-N`, while the benchmark
uses `DNIAPMSPPWPWGF-UHFFFAOYSA-N`. This is the existing unique-connectivity
lookup, made explicit, not proof that their stereochemical declarations are
identical. No undisclosed filename or atom-order substitution is allowed.

[The UD data notice](https://github.com/usnistgov/COSMOSAC/blob/1b82456be38026719b16cad4076109bef3fcb309/profiles/UD/Readme.txt)
reports a mixture of UD and later additions, and revisions to some conformations
based on vapor-pressure predictions. It supplies no per-glycol revision label.
The notice also limits permitted use and redistribution. Public accessibility
is not a grant of unrestricted commercial-use or redistribution rights.
Recovered files and detailed replay outputs remain in private local storage,
not in this repository or in a public Actions artifact.

[Bell et al., 2020](https://doi.org/10.1021/acs.jctc.9b01016) and the
[VT profile-generation materials](https://design.che.vt.edu/Downloads/VT_Sigma_Profile_Databases.html)
describe the nominal DMol3 GGA/VWN-BP/DNP procedure. This is literature-level
provenance, not proof of a particular file's full electronic input or convergence
history. The downloaded `.cosmo` header directly establishes its printed cavity
parameters. The exact electronic decks and output logs remain unverified for
the twelve individual files. The VT site advertises raw-COSMO and GO/EC OUTMOL
archives; their individual contents and correspondence to revised UD members
were not verified in this review.

P41/P42 first require the recovered raw tables to regenerate the exact Mac UD
profiles whose hashes are already recorded by P25. The archived open TZVP/SWIG
tables are replayed through the same pinned Hsieh/NHB/OH/OT implementation and
checked against their own P25 profile hashes. A successful replay establishes
input lineage within numerical tolerance. It does not establish liquid-state
accuracy or separate conformer effects from electronic/cavity effects when both
historical geometry and method differ. No such comparison has yet been executed
on the Mac as part of this report.

Geometry descriptors retain all graph correspondences and the original contact
criteria. Raw segment distributions and unnormalized final-profile tails are
reported separately. No new conformer or electrostatic correction is selected.
The P35 mechanism remains unresolved pending evidence, the numerical-gradient
campaign stays closed, and the 630+6 profile version remains unchanged.

Outcome, 2026-10-07: the comparison was executed on the Mac (manifest ba033e4). All twelve lineage/replay gates passed, with zero SCF and zero model calls. Descriptors and their limits are recorded in `docs/astra/round10/RESULTS.md`. P35 remains unresolved.
