Z-COSMO round 10: recover the public UD inputs before another quantum calculation

Reference: `Victor-Liang-ChE/zcosmo`, `main = 4dc898521f6c49355e442be78f1e2570d3686aee`. The four extractable patches in this report target that snapshot. The R8/R9 numerical-gradient campaign stays closed. The current 630 primary profiles and six S1/S2 files remain unchanged. Sources S1-S8 and U1-U8 below identify the reviewed records and public distributions.

The answer to question 1 is yes: the missing raw UD `.cosmo` files are publicly accessible in NIST's COSMOSAC repository, including all four glycols and the fixed controls. Their absence from the Mac did not establish their absence upstream. This is sufficient reason to prioritize a zero-QC provenance and same-parser replay. It is not yet proof that every recovered file generated the exact profile used locally, nor complete recovery of each electronic input deck. Those distinctions are enforced by the proposed gates. [U1, U2; S2]

| Rank | ID | Pipeline / target | Class | Mechanism and expected saving | Effort |
|---:|---|---|:---:|---|---|
| 1 | P41 | Profile-input provenance, `r10_sources.py` | E integrity | Retrieve twelve pinned raw files and two provenance documents. Zero SCF calls. Recover historical information that a new calculation cannot reconstruct. | Low |
| 2 | P42 | `r10_replay.py`, with `r10_selftest.py` | E same-input replay and read-only comparison | Verify lineage, then compare the two raw tables through the same Hsieh/HB code. Zero quantum or activity-model evaluations; 24 raw-table replays for a complete twelve-member panel. | Moderate |
| 3 | P43 | README, P35 dated annotation, current provenance note | E reporting | Correct the scope of the missing-input and raw-tail statements while preserving historical results. No numerical output changes. | Low |
| Shared | REG10 | Proposed registration text | E policy / provenance | Freeze the actual registration and comparison-manifest digest before use. No experiment is claimed accepted by supplying this text. | Low |

For the brief's ranking arithmetic, an illustrative alternative is a twelve-member, two-geometry panel requiring 24 new single points, each costing `t_SP` four-core worker-hours. That is a planning comparator, not an authorized experiment. P41/P42 cost zero SCFs. Using explicitly subjective decision-yield probabilities 0.9/0.7 and effort units 1/2 gives `24 t_SP × 0.9 / 1 = 21.6 t_SP` and `24 t_SP × 0.7 / 2 = 8.4 t_SP`. These overlapping avoided-work estimates cannot be added; no measured whole-pipeline speed-up is claimed. P43 is necessary reporting rather than a compute optimization. P41 ranks first independently of those planning assumptions because it actually recovers the missing class of evidence.

The conditional physical-test branch in question 2 is not reached. This report proposes zero new SCFs, zero geometry optimizations and no Actions compute workflow. It does not supply another inexpensive basis comparison and label it a basis/grid/response-converged reference. The actual Mac replay comes before any decision about a new physical calculation.

What was verified publicly

The following are verified repository files, not guessed paths. Each link is pinned to `usnistgov/COSMOSAC` commit `1b82456be38026719b16cad4076109bef3fcb309`; P41 verifies the full file's Git blob on acquisition and records SHA256. The raw files are not included in this report or its patches. The fixed panel is the twelve-member R5 panel, not a new subset chosen by experimental error. [U1; S5]

| Member | Verified raw file | Git blob |
|---|---|---|
| water | [XLYOFNOQVPJJNP-UHFFFAOYSA-N.cosmo](https://github.com/usnistgov/COSMOSAC/blob/1b82456be38026719b16cad4076109bef3fcb309/profiles/UD/cosmo/XLYOFNOQVPJJNP-UHFFFAOYSA-N.cosmo) | `3d23436d2b3025016350174f12f6acdd8d032867` |
| methanol | [OKKJLVBELUTLKV-UHFFFAOYSA-N.cosmo](https://github.com/usnistgov/COSMOSAC/blob/1b82456be38026719b16cad4076109bef3fcb309/profiles/UD/cosmo/OKKJLVBELUTLKV-UHFFFAOYSA-N.cosmo) | `3c69191c1aa5f04e7e9ee15e1fb83d4fd84e677b` |
| ethylene glycol | [LYCAIKOWRPUZTN-UHFFFAOYSA-N.cosmo](https://github.com/usnistgov/COSMOSAC/blob/1b82456be38026719b16cad4076109bef3fcb309/profiles/UD/cosmo/LYCAIKOWRPUZTN-UHFFFAOYSA-N.cosmo) | `b0cc75c9c38912e5a73f2b7d2c375c063169f4da` |
| diethylene glycol | [MTHSVFCYNBDYFN-UHFFFAOYSA-N.cosmo](https://github.com/usnistgov/COSMOSAC/blob/1b82456be38026719b16cad4076109bef3fcb309/profiles/UD/cosmo/MTHSVFCYNBDYFN-UHFFFAOYSA-N.cosmo) | `46c92287b77d7854f8e141e7df2745e99a12f09a` |
| triethylene glycol | [ZIBGPFATKBEMQZ-UHFFFAOYSA-N.cosmo](https://github.com/usnistgov/COSMOSAC/blob/1b82456be38026719b16cad4076109bef3fcb309/profiles/UD/cosmo/ZIBGPFATKBEMQZ-UHFFFAOYSA-N.cosmo) | `0668b927572f4ef4fdb17e5492001bd5698a04e5` |
| tetraethylene glycol | [UWHCKJMYHZGTIT-UHFFFAOYSA-N.cosmo](https://github.com/usnistgov/COSMOSAC/blob/1b82456be38026719b16cad4076109bef3fcb309/profiles/UD/cosmo/UWHCKJMYHZGTIT-UHFFFAOYSA-N.cosmo) | `5f79ef7c81b9eb669b0ca5f1ff943c9cac30ba0d` |
| glycerol | [PEDCQBHIVMGVHV-UHFFFAOYSA-N.cosmo](https://github.com/usnistgov/COSMOSAC/blob/1b82456be38026719b16cad4076109bef3fcb309/profiles/UD/cosmo/PEDCQBHIVMGVHV-UHFFFAOYSA-N.cosmo) | `39e1c2167fb3ca26308ef97f75bf2eab8a289f3a` |
| propylene glycol | [DNIAPMSPPWPWGF-VKHMYHEASA-N.cosmo](https://github.com/usnistgov/COSMOSAC/blob/1b82456be38026719b16cad4076109bef3fcb309/profiles/UD/cosmo/DNIAPMSPPWPWGF-VKHMYHEASA-N.cosmo) | `68f1bbda2363037e5246e69b1145a239908d0b8b` |
| methoxyethanol | [XNWFRZJHXBZDAG-UHFFFAOYSA-N.cosmo](https://github.com/usnistgov/COSMOSAC/blob/1b82456be38026719b16cad4076109bef3fcb309/profiles/UD/cosmo/XNWFRZJHXBZDAG-UHFFFAOYSA-N.cosmo) | `f29e58fcc3f30f49122367613221fe46314f0c98` |
| dimethoxyethane | [XTHFKEDIFFGKHM-UHFFFAOYSA-N.cosmo](https://github.com/usnistgov/COSMOSAC/blob/1b82456be38026719b16cad4076109bef3fcb309/profiles/UD/cosmo/XTHFKEDIFFGKHM-UHFFFAOYSA-N.cosmo) | `eea387e357e7bcb6be3441ffac3224d9de77708a` |
| tetrahydrofuran | [WYURNTSHIVDZCO-UHFFFAOYSA-N.cosmo](https://github.com/usnistgov/COSMOSAC/blob/1b82456be38026719b16cad4076109bef3fcb309/profiles/UD/cosmo/WYURNTSHIVDZCO-UHFFFAOYSA-N.cosmo) | `360b38b378ab42a9098df97b84708fd5b4bc2bce` |
| nonane | [BKIMMITUMNQMOS-UHFFFAOYSA-N.cosmo](https://github.com/usnistgov/COSMOSAC/blob/1b82456be38026719b16cad4076109bef3fcb309/profiles/UD/cosmo/BKIMMITUMNQMOS-UHFFFAOYSA-N.cosmo) | `3122e6a49334515b0f56edf3a8586fe54e7d7efd` |

Eleven source keys equal their benchmark keys. Propylene glycol is the explicit exception: the benchmark uses `DNIAPMSPPWPWGF-UHFFFAOYSA-N`; the published file is `DNIAPMSPPWPWGF-VKHMYHEASA-N`. The former raw-file path returned 404. The latter is present, and the project index identifies its stereospecific SMILES. This is consistent with the existing `sigma_path` unique-connectivity fallback, not an exact stereo-aware identity. P41/P42 retain both keys and do not certify stereochemistry from graph matching. [U1; S7]

The glycol headers include a conductor dielectric, input grid/segmentation settings and atomic radii. EG, for example, records basic grid 1082, segmentation setting 92, solvent radius 1.30 and matrix cutoff 7.00, with no radius increment. Its actual surface table has 406 rows. The atomic coordinates are in the embedded molecular-car block; surface positions are labelled in atomic units. The parser uses angstroms for atomic coordinates and converts surface coordinates from Bohr. The input setting 92 must not be used to size the surface table. [U1; S7]

The same EG raw blob is present at NIST's `v1.0.1` tag. The recovered information is not newly invented for this review. Its embedded `552.car` is not a valid cross-database join key: the current project UD index assigns 552 to 1-heptadecanol. P42 joins by explicit chemical identity and historical profile hashes, never by that embedded ordinal. [U1; S7]

Public distribution and method-documentation inventory

| Source and exact location | What is verified and what remains unverified |
|---|---|
| [NIST UD raw directory](https://github.com/usnistgov/COSMOSAC/tree/1b82456be38026719b16cad4076109bef3fcb309/profiles/UD/cosmo), with [compound list](https://github.com/usnistgov/COSMOSAC/blob/1b82456be38026719b16cad4076109bef3fcb309/profiles/UD/complist.txt) | Twelve exact raw paths and their Git blob identifiers were confirmed. Selected file blocks were inspected, including geometry and segment records. The source list gives chemical identities; per-file full electronic decks have not been established. |
| [NIST UD notice](https://github.com/usnistgov/COSMOSAC/blob/1b82456be38026719b16cad4076109bef3fcb309/profiles/UD/Readme.txt) | Describes the UD/later-addition provenance, points to generation papers and states data-use restrictions. This is not a blanket code-license grant for the data. |
| [NIST GitHub releases](https://api.github.com/repos/usnistgov/COSMOSAC/releases?per_page=20) | The release API advertises `COSMOSAC_v1.0.0.zip` and `COSMOSAC_v1.0.1.zip`. Their exact download locations are below. The binary archives were not unpacked here, so their individual member lists are not claimed verified. |
| [Zenodo record 3669311](https://zenodo.org/records/3669311) | The v1.0 repository archive `usnistgov/COSMOSAC-v1.0.zip` is listed, with an MD5 and size. The record is verified; the ZIP contents were not unpacked. |
| [VT official database page](https://design.che.vt.edu/Downloads/VT_Sigma_Profile_Databases.html) | Advertises VT-2005 raw COSMO, geometry-optimization OUTMOL and energy-calculation OUTMOL archives, alongside profiles and indexes. Download links were followed, but binary contents were not inspected. Correspondence to the revised UD glycol files is unverified. |
| [NIST repository's VT2005 directory](https://github.com/usnistgov/COSMOSAC/tree/1b82456be38026719b16cad4076109bef3fcb309/profiles/VT2005) | The inspected directory supplies a Fortran implementation, database index and processed sigma profiles. It must not be substituted for the UD raw directory or assumed to contain the VT OUTMOL archives. |
| [Bell et al., 2020, DOI 10.1021/acs.jctc.9b01016](https://www.nist.gov/publications/benchmark-open-source-implementation-cosmo-sac) | The accessible paper describes the raw-file/postprocessing distribution and nominal DMol3 GGA/VWN-BP/DNP calculation family. Its public-data and method passages were inspected in the PDF, including page images. |
| [VT profile-generation tutorial](https://design.che.vt.edu/content/design_che_vt_edu/en/Downloads/VT_Sigma_Profile_Databases/_jcr_content/content/download_1303237808/file.res/VT-2005_Sigma_Profile_Generation_Procedure.pdf) | Accessible PDF with illustrated method and COSMO settings. Pages 18, 21 and 28, using PDF page numbers, were visually inspected. It documents a nominal procedure; it does not establish every option actually used for a particular revised UD member. |
| [Mullins et al., 2006, DOI 10.1021/ie060370h](https://pubs.acs.org/doi/10.1021/ie060370h) | The VT-generation paper is an identified primary method reference. It is not evidence that a VT index number identifies the same conformation in a revised UD collection. |
| [Xiong et al., 2014, DOI 10.1021/ie404410v](https://pubs.acs.org/doi/10.1021/ie404410v), [supporting-information collection](https://acs.figshare.com/collections/An_Improvement_to_COSMO_SAC_for_Predicting_Thermodynamic_Properties/2338636) | Identified source for the conformation-revision history. The SI description advertises quantum-method information; the underlying SI files were not downloaded and matched to this panel. |
| [Fingerhut et al., 2017, DOI 10.1021/acs.iecr.7b01360](https://pubs.acs.org/doi/abs/10.1021/acs.iecr.7b01360) | Identified assessment/addition provenance. Its advertised SI is not asserted to be a verified archive of the twelve UD generating inputs. |

The verified release-asset locations are [NIST v1.0.0](https://github.com/usnistgov/COSMOSAC/releases/download/v1.0/COSMOSAC_v1.0.0.zip) and [NIST v1.0.1](https://github.com/usnistgov/COSMOSAC/releases/download/v1.0.1/COSMOSAC_v1.0.1.zip). The official VT page's advertised raw and log links are [COSMO files](https://design.che.vt.edu/content/design_che_vt_edu/en/Downloads/VT_Sigma_Profile_Databases/_jcr_content/content/download_1702511376/file.res/VT-2005_COSMO_Files_v2.zip), [GO OUTMOL files](https://design.che.vt.edu/content/design_che_vt_edu/en/Downloads/VT_Sigma_Profile_Databases/_jcr_content/content/download_1242743743/file.res/VT-2005_GO_OUTMOL_Files_v2.zip), and [EC OUTMOL files](https://design.che.vt.edu/content/design_che_vt_edu/en/Downloads/VT_Sigma_Profile_Databases/_jcr_content/content/download_588111127/file.res/VT-2005_EC_OUTMOL_Files_v2.zip). These are confirmed advertised links, not a claim that their archive members were downloaded or validated. The direct NIST raw-file route is the verified path used by P41. [U3-U5]

Nominal method provenance is useful but incomplete. The tutorial specifies VWN-BP and discusses its local-correlation choice, plus a DNP basis version. That does not establish implementation-level identity with PySCF's `b88,p86` and def2 basis sets. File headers supply the actual printed cavity information; papers/tutorials supply nominal electronic context; exact per-job decks and convergence histories are still unverified. The proposed result JSON deliberately contains `electronic_input_deck_verified: false`. [U6, U7; S7]

The UD notice also reports that roughly a third of database conformations were revised based on vapor-pressure predictions. That is an upstream empirical-selection qualification, not proof that a particular glycol was revised or that this project's ThermoML rows were used. Retain “Z0x was not fitted to ThermoML.” Do not expand it into “every reference input was selected without empirical information,” and do not equate the UD histogram with an equilibrium liquid ensemble. [U2, U8]

P41: acquisition that preserves identifiable raw inputs

Targets are `catalog`, `acquire` and `check` in `scripts/r10_sources.py`. The source filenames and twelve Git blobs are fixed in code. The command retrieves those files and the notice/index on the Mac, preserves their bytes and writes a local SHA256 manifest. One failed download leaves the acquisition incomplete. There is no alternative filename, mirror search or retry loop hidden in the command.

The file notice permits specified academic/non-profit use and restricts redistribution. Review that notice before acknowledging the acquisition flag. This report is not permission for commercial deployment, redistribution or uploading the database to a public repository. All recovered raw data and detailed derived reports are placed outside the repository. The report and patches contain source locations and code, not the raw database. [U2]

The budget is fourteen GET requests and zero quantum/model evaluations. The implementation has an 8 MB per-file ceiling and a 30-second socket timeout, not a promise of a completion time. `acquisition.json` records actual wall time. A successful acquisition proves byte identity with the pinned distribution, not that those bytes generated the project's local profiles. P42 supplies that separate check.

P42: a registered same-parser comparison, before physical attribution

Targets are `freeze`, `run_member`, `compare` and `check` in `scripts/r10_replay.py`. The sources are the recovered UD raw tables, the Mac UD sigma files and the already-computed P25 TZVP/SWIG raw archives. No new geometry is generated. The old R5 single-point run is an artifact source, not a workflow to dispatch again.

The first gate is historical lineage. P25's existing CSV records both `UD_sha256` and `source_sha256`. P42 requires the exact Mac UD profile and the exact archived open Hsieh profile recorded there, with the original P25 native geometry hash. The archived segment coordinates must equal the frozen R5 geometry, and the saved primary coordinates must match as well. Duplicate or missing artifact matches block preparation. This prevents comparing a newly downloaded historical file against a conveniently substituted modern profile. All original 630+6 files are hashed before preparation and checked after the replay. [S5, S7]

The comparison manifest is external to the repository. Its SHA256 is committed before descriptor computation. The registration commit, helper code hashes and normalized package versions are also checked. This is a portable specification of a particular comparison, rather than “whatever files happen to be in a directory.” The full Mac asset replay was not performed here.

Both raw tables use the existing project parser, Git blob `9f2e0d6f3bb4da4880f9bd6ad702847f9308ed1d`, with Hsieh averaging and three NHB/OH/OT profiles. The UD path uses `Dmol3COSMOParser`; the open path uses the already-established `r4_common.parser_trace` adapter. Each must reproduce its own stored area profile with `max |Δ bin| < 1e-8 Å²`. The UD metadata and binwise HB-area conservation have explicit checks. This stricter same-input replay tolerance is not an acceptance criterion requiring open and UD physics to agree. No production model changes, so no new activity-coefficient compatibility claim is being made. [S7]

The raw charge density is recomputed from the printed charge divided by area, following the existing parser. Rounded charge-density columns are not substituted. The code separately retains the printed original and corrected charge sums and checks their consistency with a sum of half-last-decimal rounding allowances. This can expose a convention ambiguity but cannot establish a physically correct neutrality prescription. It applies no charge shift. The open comparison uses the archived retained P25 tesserae, not a reconstruction of discarded surface points. [S7; U1]

For geometry, element-labelled connectivity and attached-hydrogen counts provide the atom correspondence. Every admissible heavy-atom correspondence is retained, with a fail-closed cap of 256. The code reports proper-rotation RMSD and both heavy-chain and H-O-C-X torsions for each mapping. RMSD alignment is descriptive only; it never rotates coordinates used for averaging. Propylene glycol's source/benchmark stereochemical difference remains explicit rather than disappearing in an alignment.

The O-H···O contact rule is the existing one: donor-acceptor distance no more than 3.2 Å, H-acceptor distance no more than 2.5 Å and D-H-A angle at least 120°. The output retains all candidate distances and angles. It does not call a geometric contact an H-bond energy, exclude a conformation or assign a statistical weight. [S7]

Distribution comparisons include raw and averaged charge-density distances, atom-resolved surface areas and the complete pre/post-HB bins. The quantities called “tail” are distinguished explicitly: the area of raw tesserae satisfying `|q/A| ≥ 0.01`, the area selected after continuous averaging, and the tail of the final binned profile. They need not agree. In P29, “raw area profile” meant an unnormalized final profile, not a pre-averaging tessera distribution. No pointwise matching of unrelated surface rows is used. [S2, S5-S7]

Every requested member retains an outcome. A lineage failure blocks that member's comparison while later independent members continue; the overall gate needs all twelve. A successful panel gives reproducible observations about known input files. It does not assign a percentage of the historical gap to conformation.

To see the remaining causal limitation, write the common postprocessed profile from method `M` at geometry `R` as `p_M(R)`. The two historical inputs provide `p_U(R_U)` and `p_O(R_O)`. Formally,

\[
p_U(R_U)-p_O(R_O)
=[p_O(R_U)-p_O(R_O)]+[p_U(R_U)-p_O(R_U)].
\]

The uncomputed crossed quantity `p_O(R_U)` is what separates a geometry intervention within the open method from the remaining difference at the UD geometry. Recovering the files reveals `R_U`; it does not compute that crossed quantity. Identical geometries would narrow the interpretation to the remaining electronic/cavity/data representation. Different geometries with different raw spectra leave both explanations available. Neither outcome establishes the equilibrium liquid distribution. This is why P42 is descriptive and why the conditional physical-reference proposal is deferred rather than silently added.

A later crossed single point would itself still be a fixed-method intervention, not an independently basis/grid/response-converged reference. A physical-reference claim would need a different registered error budget and numerical evidence. There is no basis for treating the old P25 SVP/TZVP and SWIG/ISWIG tests as that independent reference. No such native calculation is authorized in R10. [S2, S5]

P43: current wording, without rewriting historical experiments

The README's present statement that the glycol mechanism is unresolved is appropriate. Its statements about original Berny convergence and the failed corrected-gradient compatibility gate should remain. Add a short current link saying that public raw inputs were located and that the Mac lineage check is pending. The R9 closeout concerns the numerical-gradient campaign; recovering glycol provenance is a different task and does not undo that closeout. [S2, S3, S8]

Two historical descriptions need a narrower reading. “UD geometries were unavailable” describes the Mac holdings during those experiments. “The deficit was already in raw charges” in the R5 discussion was not a direct UD/open raw-table comparison, because the UD table had not been available to that run. P25 identified sensitivities within the tested open calculation, not a unique historical electronic cause. P43 appends this qualification to the current P35 record and the new provenance note. It preserves all measured R4-R6 numbers rather than retrospectively editing them into a different experiment. [S2, S4-S6]

The meaningful accuracy claim is that the frozen model/profile combination gave a negative glycol-solvent bias on the stated experimental panel. “The open profiles are physically wrong” is stronger and unsupported. “UD is the correct liquid distribution” is also unsupported. Water and branched polyols are retained precisely because their responses do not follow a universal linear-glycol rule. A related identifier correction: the net-charge intervention referenced as P23 in the R10 prompt was P22; P23 was the LLE work. [S1, S4]

Executed and unexecuted

Executed here: connected-GitHub source/path inspection; inspection of the official distribution pages and relevant PDF page images; inspection of the required R4-R9 results and relevant data tables; Git-blob verification of the README/P35 base texts; four independent patch-application checks and their combined application; Python/CLI checks; and twenty portable tests. The tests include an end-to-end `run_member` adapter exercise with synthetic water and mocked legacy adapters, symmetry/dihedral checks, failed-lineage handling and retention of missing/failed rows. They are not a replay of real UD data. The verification record below states that explicitly.

Not executed: a full repository clone, real acquisition to the Mac, the complete real parser against all recovered files, any UD/open numerical comparison, any quantum calculation, activity-model evaluation or scorecard. The runtime has no PySCF installation; none was needed or attempted for these zero-QC helpers. A direct container network attempt failed at DNS resolution, while the connected GitHub and web tools supplied the source inspection. It would be inaccurate to describe the publicly inspected files as a locally parsed, fully validated dataset.

No physical mechanism was newly accepted. Native budgets remain zero. The source discovery is the result established in this round; the supplied Mac commands perform the prospective lineage comparison.

Application and exact commands

Save this Markdown report outside the repository. The following extractor writes the four labelled patches from the report and refuses an unexpected patch set. `REPORT` must point to the saved report. It creates only a local patch directory and does not touch the source repository.

```bash
set -euo pipefail
export REPORT="$HOME/Downloads/ZCOSMO_ROUND10_REPORT.md"
export PATCHDIR="$HOME/zc-r10-patches"
python - <<'PY'
import os,re
from pathlib import Path
text=Path(os.environ['REPORT']).read_text()
pattern=r'<!-- BEGIN PATCH (\w+) -->\n```diff\n(.*?)\n```\n<!-- END PATCH \1 -->'
parts=re.findall(pattern,text,re.S)
assert [name for name,_ in parts]==['P41','P42','P43','REG10']
out=Path(os.environ['PATCHDIR']);out.mkdir(parents=True,exist_ok=False)
for name,diff in parts:(out/(name+'.patch')).write_text(diff+'\n')
print('Extracted',len(parts),'patches')
PY
```

From a clean zcosmo checkout on the Mac, apply and commit the proposed protocol before acquisition. The four patches can be application-checked independently; P42 requires P41 at runtime. The explicit `git status` guard catches untracked files as well. No command below dispatches an Actions workflow.

```bash
set -euo pipefail
test -z "$(git status --porcelain)"
git switch -c astra-round10 4dc898521f6c49355e442be78f1e2570d3686aee
for p in P41 P42 P43 REG10; do git apply --check "$PATCHDIR/$p.patch"; done
for p in P41 P42 P43 REG10; do git apply "$PATCHDIR/$p.patch"; done
git diff --check
export PYTHONPATH=src:scripts
export MPLBACKEND=Agg
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python scripts/r10_selftest.py
python scripts/r10_sources.py catalog
printf '\n' >> PREREGISTRATION.md
cat docs/astra/round10/REGISTRATION_PROPOSED.md >> PREREGISTRATION.md
git add scripts/r10_sources.py scripts/r10_replay.py scripts/r10_selftest.py \
  README.md docs/astra/round7/GLYCOL_STATUS.md docs/astra/round10 PREREGISTRATION.md
git commit -m "Register R10 zero-QC UD provenance and replay"
export REG="$(git rev-parse HEAD)"
```

The replay requires NumPy, SciPy, pandas, RDKit, packaging and matplotlib, all of which are already used by the existing analysis stack or parser. Keep the Mac environment stable. The manifest records normalized installed versions rather than silently installing a different quantum package. The portable tests here used RDKit 2025.9.4; that does not claim parity with a completed Mac data replay. Actual Mac package values are frozen before comparison.

After reviewing the linked UD notice and establishing applicable use rights, run P41. The explicit acknowledgment below records the operator's decision; it grants no rights. Choose a fresh private directory outside the repository.

```bash
set -euo pipefail
export R10="$HOME/zc-r10-provenance-20261007"
mkdir "$R10"
python scripts/r10_sources.py acquire --registration "$REG" \
  --acknowledge-ud-terms --out "$R10/source"
python scripts/r10_sources.py check --source-root "$R10/source"
```

Retrieve the original P25 artifacts, not P26 conformer outputs or P34 stresses. This downloads a previous run; it does not run it. If the artifacts are unavailable or already retained elsewhere, use their verified retained location as `--open-artifacts`. Missing raw data blocks the comparison; it does not authorize replacing the run with new SCFs.

```bash
set -euo pipefail
gh run download 37423042495 -R Victor-Liang-ChE/zcosmo -D "$R10/p25"
python scripts/r10_replay.py freeze \
  --source-root "$R10/source" --open-artifacts "$R10/p25" \
  --profile-root data/pyscf_sigma --ud-dir data/raw/nist/UD/sigma3 \
  --registration "$REG" --out "$R10/frozen"
cp "$R10/frozen/PLAN_SHA256.txt" docs/astra/round10/PLAN_SHA256.txt
git add docs/astra/round10/PLAN_SHA256.txt
git commit -m "Freeze R10 source and artifact identity manifest"
export PLAN_COMMIT="$(git rev-parse HEAD)"
python scripts/r10_replay.py compare --manifest "$R10/frozen/manifest.json" \
  --plan-commit "$PLAN_COMMIT" --out "$R10/comparison"
python scripts/r10_replay.py check --summary "$R10/comparison/summary.json"
```

The benchmark is the recorded wall time in `acquisition.json` and `comparison/summary.json`, separately. Do not count the historical P25 compute as new replay time, or compare this read-only task's duration with an optimizer's scientific output. The complete check requires twelve successful lineage gates, with zero SCF/model calls. Its 1e-8 Å² criterion measures same-input numerical replay, not open-to-UD accuracy.

P43's document check is independent of Mac-only numerical data. It verifies that the closeout is retained and the new source discovery is stated without claiming adoption.

```bash
python - <<'PY'
from pathlib import Path
r=Path('README.md').read_text()
g=Path('docs/astra/round7/GLYCOL_STATUS.md').read_text()
p=Path('docs/astra/round10/PROVENANCE_STATUS.md').read_text()
assert 'its numerical diagnostic budget is closed' in r
assert 'round-10 provenance review' in r
assert 'same-parser comparison' in g
assert '630 primary and six S1/S2 files stay' in g
assert 'not proof of a particular' in p
assert 'No such comparison has yet been executed' in p
print('R10 reporting scope checks passed')
PY
```

After the real replay, append its results with manifest hashes to a new results record. Do not leave the current provenance note's “not yet executed” statement as a current claim after a successful run; date the new outcome. A passing replay still does not authorize a profile replacement or physical-method sweep.

Source references

S1 is [the pinned R10 prompt](https://github.com/Victor-Liang-ChE/zcosmo/blob/4dc898521f6c49355e442be78f1e2570d3686aee/docs/astra/ROUND10_PROMPT.md) and [optimization rules](https://github.com/Victor-Liang-ChE/zcosmo/blob/4dc898521f6c49355e442be78f1e2570d3686aee/docs/OPTIMIZATION_BRIEF.md). S2 is [P35's status](https://github.com/Victor-Liang-ChE/zcosmo/blob/4dc898521f6c49355e442be78f1e2570d3686aee/docs/astra/round7/GLYCOL_STATUS.md) and its text in [PREREGISTRATION.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/4dc898521f6c49355e442be78f1e2570d3686aee/PREREGISTRATION.md). S3 is [R9 closeout](https://github.com/Victor-Liang-ChE/zcosmo/blob/4dc898521f6c49355e442be78f1e2570d3686aee/docs/astra/round9/RESULTS.md), read alongside the archived R9 report.

S4 is [R4 RESULTS](https://github.com/Victor-Liang-ChE/zcosmo/blob/4dc898521f6c49355e442be78f1e2570d3686aee/docs/astra/round4/RESULTS.md). There is no `docs/astra/round4/data/` directory in the inspected snapshot, so no such raw result bundle is claimed inspected. S5 is [R5 RESULTS](https://github.com/Victor-Liang-ChE/zcosmo/blob/4dc898521f6c49355e442be78f1e2570d3686aee/docs/astra/round5/RESULTS.md) with the [P25 stage CSV](https://github.com/Victor-Liang-ChE/zcosmo/blob/4dc898521f6c49355e442be78f1e2570d3686aee/docs/astra/round5/data/p25_stage_comparison.csv) and other archived R5 data. S6 is [R6 RESULTS](https://github.com/Victor-Liang-ChE/zcosmo/blob/4dc898521f6c49355e442be78f1e2570d3686aee/docs/astra/round6/RESULTS.md) and the [P29 inventory](https://github.com/Victor-Liang-ChE/zcosmo/blob/4dc898521f6c49355e442be78f1e2570d3686aee/docs/astra/round6/data/p29_inventory.json).

S7 denotes the pinned [parser](https://github.com/Victor-Liang-ChE/zcosmo/blob/4dc898521f6c49355e442be78f1e2570d3686aee/data/raw/nist/to_sigma.py), [UD index](https://github.com/Victor-Liang-ChE/zcosmo/blob/4dc898521f6c49355e442be78f1e2570d3686aee/data/processed_ext/ud_complist.csv), [profile generator](https://github.com/Victor-Liang-ChE/zcosmo/blob/4dc898521f6c49355e442be78f1e2570d3686aee/src/zcosmo/pyscf_cosmo.py), [R5 generation/collection helper](https://github.com/Victor-Liang-ChE/zcosmo/blob/4dc898521f6c49355e442be78f1e2570d3686aee/scripts/r5_shape.py), [R4 parser/contact adapter](https://github.com/Victor-Liang-ChE/zcosmo/blob/4dc898521f6c49355e442be78f1e2570d3686aee/scripts/r4_common.py), [COSMO-SAC implementation](https://github.com/Victor-Liang-ChE/zcosmo/blob/4dc898521f6c49355e442be78f1e2570d3686aee/src/zcosmo/cosmosac.py) and [Z0x implementation](https://github.com/Victor-Liang-ChE/zcosmo/blob/4dc898521f6c49355e442be78f1e2570d3686aee/src/zcosmo/z0x.py). S8 is the [pinned README](https://github.com/Victor-Liang-ChE/zcosmo/blob/4dc898521f6c49355e442be78f1e2570d3686aee/README.md).

U1 denotes the verified raw-file table above and the [same EG blob at v1.0.1](https://github.com/usnistgov/COSMOSAC/blob/v1.0.1/profiles/UD/cosmo/LYCAIKOWRPUZTN-UHFFFAOYSA-N.cosmo). U2 is the linked NIST UD notice. U3 is the linked release API/assets. U4 is the linked Zenodo record. U5 is the linked VT distribution page and advertised archives. U6 is Bell et al., with the accessible [NIST manuscript PDF](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=928356), especially its UD-method and data-distribution passages on PDF pages 16 and 18. U7 is the VT generation tutorial, especially PDF pages 18, 21 and 28. U8 denotes the linked Mullins, Xiong and Fingerhut papers and the supporting-information record actually inspected. An identified paper or advertised SI is not a claim that every attached data member was recovered.

Extractable patches

The following four diffs are against the pinned source. The only pre-existing files changed are the README and P35 status, whose base Git blobs were verified as `ed6fb9c547e541fd68b128ebdaa3e620e3f4c706` and `1200ff44df5a76619e34a4b52bc14ed7a30d27ac`. All Python helpers and round-10 records are new. Nothing changes the model, parser or profile-generator implementation.

<!-- BEGIN PATCH P41 -->
```diff
diff --git a/scripts/r10_sources.py b/scripts/r10_sources.py
new file mode 100644
--- /dev/null
+++ b/scripts/r10_sources.py
@@ -0,0 +1,193 @@
+"""P41: acquire the fixed public UD inputs. No quantum or model evaluation.
+
+Run the real acquisition on the asset-bearing Mac after registration. The data
+notice is separate from the code license. This helper does not grant use rights.
+"""
+from __future__ import annotations
+import argparse
+import hashlib
+import json
+from pathlib import Path
+import re
+import subprocess
+import sys
+import time
+import urllib.request
+
+BASE = '4dc898521f6c49355e442be78f1e2570d3686aee'
+UPSTREAM = '1b82456be38026719b16cad4076109bef3fcb309'
+PARSER_BLOB = '9f2e0d6f3bb4da4880f9bd6ad702847f9308ed1d'
+MARKER = 'R10-P41-P42-P43: UD provenance, zero-QC replay'
+PLAN_RECORD = 'docs/astra/round10/PLAN_SHA256.txt'
+ROOT = Path(__file__).resolve().parents[1]
+# name, benchmark key, published source key, verified upstream Git blob
+DATA = (
+ ('water','XLYOFNOQVPJJNP-UHFFFAOYSA-N','XLYOFNOQVPJJNP-UHFFFAOYSA-N','3d23436d2b3025016350174f12f6acdd8d032867'),
+ ('methanol','OKKJLVBELUTLKV-UHFFFAOYSA-N','OKKJLVBELUTLKV-UHFFFAOYSA-N','3c69191c1aa5f04e7e9ee15e1fb83d4fd84e677b'),
+ ('ethylene_glycol','LYCAIKOWRPUZTN-UHFFFAOYSA-N','LYCAIKOWRPUZTN-UHFFFAOYSA-N','b0cc75c9c38912e5a73f2b7d2c375c063169f4da'),
+ ('diethylene_glycol','MTHSVFCYNBDYFN-UHFFFAOYSA-N','MTHSVFCYNBDYFN-UHFFFAOYSA-N','46c92287b77d7854f8e141e7df2745e99a12f09a'),
+ ('triethylene_glycol','ZIBGPFATKBEMQZ-UHFFFAOYSA-N','ZIBGPFATKBEMQZ-UHFFFAOYSA-N','0668b927572f4ef4fdb17e5492001bd5698a04e5'),
+ ('tetraethylene_glycol','UWHCKJMYHZGTIT-UHFFFAOYSA-N','UWHCKJMYHZGTIT-UHFFFAOYSA-N','5f79ef7c81b9eb669b0ca5f1ff943c9cac30ba0d'),
+ ('glycerol','PEDCQBHIVMGVHV-UHFFFAOYSA-N','PEDCQBHIVMGVHV-UHFFFAOYSA-N','39e1c2167fb3ca26308ef97f75bf2eab8a289f3a'),
+ ('propylene_glycol','DNIAPMSPPWPWGF-UHFFFAOYSA-N','DNIAPMSPPWPWGF-VKHMYHEASA-N','68f1bbda2363037e5246e69b1145a239908d0b8b'),
+ ('methoxyethanol','XNWFRZJHXBZDAG-UHFFFAOYSA-N','XNWFRZJHXBZDAG-UHFFFAOYSA-N','f29e58fcc3f30f49122367613221fe46314f0c98'),
+ ('dimethoxyethane','XTHFKEDIFFGKHM-UHFFFAOYSA-N','XTHFKEDIFFGKHM-UHFFFAOYSA-N','eea387e357e7bcb6be3441ffac3224d9de77708a'),
+ ('tetrahydrofuran','WYURNTSHIVDZCO-UHFFFAOYSA-N','WYURNTSHIVDZCO-UHFFFAOYSA-N','360b38b378ab42a9098df97b84708fd5b4bc2bce'),
+ ('nonane','BKIMMITUMNQMOS-UHFFFAOYSA-N','BKIMMITUMNQMOS-UHFFFAOYSA-N','3122e6a49334515b0f56edf3a8586fe54e7d7efd'),
+)
+
+
+def sha(path: str | Path) -> str:
+    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
+
+
+def blob(data: bytes) -> str:
+    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
+
+
+def read(path: str | Path):
+    return json.loads(Path(path).read_text())
+
+
+def write(path: str | Path, value) -> None:
+    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
+    text=json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n'
+    tmp=p.with_name(p.name+'.tmp'); tmp.write_text(text); tmp.replace(p)
+
+
+def git(*args: str) -> bytes:
+    return subprocess.check_output(['git','-C',str(ROOT),*args],stderr=subprocess.PIPE)
+
+
+def registration(commit: str) -> dict:
+    if not re.fullmatch('[0-9a-f]{40}',commit):
+        raise ValueError('Use the actual full registration commit SHA')
+    git('merge-base','--is-ancestor',BASE,'HEAD')
+    git('merge-base','--is-ancestor',commit,'HEAD')
+    text=git('show',commit+':PREREGISTRATION.md')
+    if MARKER.encode() not in text:
+        raise ValueError('The commit does not contain the R10 registration marker')
+    return dict(commit=commit,preregistration_sha256=hashlib.sha256(text).hexdigest())
+
+
+def committed_sources(paths: list[str]) -> dict:
+    result={}
+    for name in paths:
+        data=(ROOT/name).read_bytes()
+        if data!=git('show','HEAD:'+name):
+            raise ValueError('Commit the reviewed source before use: '+name)
+        result[name]=hashlib.sha256(data).hexdigest()
+    return result
+
+
+def verify_sources(sources: dict) -> None:
+    for name,expected in sources.items():
+        if sha(ROOT/name)!=expected:
+            raise ValueError('Source changed: '+name)
+
+
+def record(path: str | Path) -> dict:
+    p=Path(path).resolve(strict=True)
+    if not p.is_file(): raise ValueError('Not a file: '+str(p))
+    return dict(path=str(p),sha256=sha(p))
+
+
+def verify_record(r: dict) -> Path:
+    p=Path(r['path'])
+    if not p.is_file() or sha(p)!=r['sha256']:
+        raise ValueError('Frozen input missing or changed: '+str(p))
+    return p
+
+
+def private_output(path: str | Path) -> Path:
+    p=Path(path).expanduser().resolve()
+    if p.is_relative_to(ROOT) or ROOT.is_relative_to(p):
+        raise ValueError('Keep recovered raw inputs and reports outside the repository')
+    if p.exists(): raise FileExistsError(p)
+    return p
+
+
+def mac() -> None:
+    if sys.platform!='darwin':
+        raise RuntimeError('UD-backed acquisition/replay is registered on the Mac only')
+
+
+def catalog() -> list[dict]:
+    items=[]
+    for name,key,source,expected in DATA:
+        path='profiles/UD/cosmo/'+source+'.cosmo'
+        items.append(dict(name=name,key=key,source_key=source,relative_path=path,
+            expected_git_blob=expected,
+            url=f'https://raw.githubusercontent.com/usnistgov/COSMOSAC/{UPSTREAM}/{path}'))
+    for path,expected in (
+        ('profiles/UD/Readme.txt','a536b2b8b76ba687b5f134d402baad73efb92150'),
+        ('profiles/UD/complist.txt','565a7be9a604b7e0670e724b141fdc349c59459d')):
+        items.append(dict(relative_path=path,expected_git_blob=expected,
+            url=f'https://raw.githubusercontent.com/usnistgov/COSMOSAC/{UPSTREAM}/{path}'))
+    return items
+
+
+def verify_download(data: bytes, expected: str) -> None:
+    if blob(data)!=expected:
+        raise ValueError('Downloaded bytes do not match the verified upstream Git blob')
+
+
+def acquire(a) -> int:
+    mac(); reg=registration(a.registration)
+    if not a.acknowledge_ud_terms:
+        raise ValueError('Read the UD data notice and explicitly acknowledge applicable rights')
+    source=committed_sources(['scripts/r10_sources.py'])
+    out=private_output(a.out); out.mkdir(parents=True,exist_ok=False)
+    start=time.perf_counter(); records=[]
+    for item in catalog():
+        r=dict(item,status='pending'); records.append(r)
+        try:
+            req=urllib.request.Request(item['url'],headers={'User-Agent':'zcosmo-R10-provenance'})
+            with urllib.request.urlopen(req,timeout=30) as response:
+                data=response.read(8_000_001)
+                if response.status!=200 or len(data)>8_000_000:
+                    raise ValueError('Unexpected status or file larger than the fixed 8 MB ceiling')
+            verify_download(data,item['expected_git_blob'])
+            dest=out/item['relative_path']; dest.parent.mkdir(parents=True,exist_ok=True)
+            with dest.open('xb') as f: f.write(data)
+            r.update(status='verified',sha256=sha(dest),bytes=len(data))
+        except Exception as exc:
+            r.update(status='unavailable',error=type(exc).__name__+': '+str(exc))
+        write(out/'acquisition.json',dict(base=BASE,upstream=UPSTREAM,registration=reg,
+            records=records,sources=source,SCF_calls=0,model_calls=0,complete=False))
+    complete=all(r['status']=='verified' for r in records)
+    verify_sources(source)
+    write(out/'acquisition.json',dict(base=BASE,upstream=UPSTREAM,registration=reg,
+        records=records,sources=source,SCF_calls=0,model_calls=0,complete=complete,
+        wall_s=time.perf_counter()-start,
+        rights='UD notice applies; no redistribution or commercial-use permission is granted here'))
+    return 0 if complete else 2
+
+
+def check(a) -> int:
+    root=Path(a.source_root).resolve(); d=read(root/'acquisition.json')
+    if d.get('upstream')!=UPSTREAM or d.get('complete') is not True:
+        raise ValueError('Incomplete or different acquisition')
+    expected=catalog()
+    if len(d['records'])!=len(expected): raise ValueError('Wrong acquisition count')
+    by={r['relative_path']:r for r in d['records']}
+    if len(by)!=len(expected): raise ValueError('Duplicate acquisition record')
+    for e in expected:
+        r=by[e['relative_path']]; p=root/e['relative_path']
+        verify_download(p.read_bytes(),e['expected_git_blob'])
+        if r.get('status')!='verified' or sha(p)!=r['sha256']:
+            raise ValueError('Acquisition record mismatch')
+    print('Verified 12 COSMO files and 2 provenance documents; no SCF or model evaluation')
+    return 0
+
+
+def main() -> int:
+    p=argparse.ArgumentParser(description=__doc__); s=p.add_subparsers(dest='cmd',required=True)
+    q=s.add_parser('catalog'); q.set_defaults(fn=lambda a:print(json.dumps(catalog(),indent=2)))
+    q=s.add_parser('acquire'); q.add_argument('--out',required=True)
+    q.add_argument('--registration',required=True); q.add_argument('--acknowledge-ud-terms',action='store_true')
+    q.set_defaults(fn=acquire)
+    q=s.add_parser('check'); q.add_argument('--source-root',required=True); q.set_defaults(fn=check)
+    a=p.parse_args(); return a.fn(a) or 0
+
+if __name__=='__main__': raise SystemExit(main())
```
<!-- END PATCH P41 -->

<!-- BEGIN PATCH P42 -->
```diff
diff --git a/scripts/r10_replay.py b/scripts/r10_replay.py
new file mode 100644
--- /dev/null
+++ b/scripts/r10_replay.py
@@ -0,0 +1,509 @@
+"""P42: Mac-only, zero-QC replay of recovered UD and archived P25 raw tables.
+
+No optimizer, SCF, activity-coefficient evaluation, histogram fitting, or profile
+installation is reachable from this CLI. Outputs stay outside the repository.
+"""
+from __future__ import annotations
+import argparse
+from collections import Counter
+from decimal import Decimal
+import hashlib
+from importlib.metadata import version
+import json
+import os
+from pathlib import Path
+import re
+import sys
+import time
+import numpy as np
+import pandas as pd
+from packaging.version import Version
+from scipy.stats import wasserstein_distance
+from r10_sources import (BASE,UPSTREAM,PARSER_BLOB,DATA,PLAN_RECORD,ROOT,sha,blob,
+    read,write,record,verify_record,registration,committed_sources,verify_sources,
+    private_output,mac,check as check_acquisition)
+
+SCHEMA='R10-replay-v1'
+BIN_TOL=1e-8  # A^2, replay of the SAME published table, not an open/UD physics gate
+MAX_SEGMENTS=10000
+SOURCE_FILES=['scripts/r10_sources.py','scripts/r10_replay.py',
+    'data/raw/nist/to_sigma.py','scripts/r4_common.py','scripts/r3_common.py',
+    'src/zcosmo/pyscf_cosmo.py','src/zcosmo/cosmosac.py','src/zcosmo/z0x.py']
+R5_PLAN='cloud/r5/shape-plan/manifest.json'
+R5_STAGES='docs/astra/round5/data/p25_stage_comparison.csv'
+
+
+def packages() -> dict:
+    return {p:str(Version(version(p))) for p in ('numpy','scipy','pandas','rdkit','packaging','matplotlib')}
+
+
+def parser_module():
+    folder=ROOT/'data/raw/nist'
+    if blob((folder/'to_sigma.py').read_bytes())!=PARSER_BLOB:
+        raise ValueError('The reviewed parser changed; re-register before a new replay')
+    sys.path.insert(0,str(folder))
+    import to_sigma
+    if Path(to_sigma.__file__).resolve()!=folder/'to_sigma.py':
+        raise ValueError('Another to_sigma module is already imported')
+    return to_sigma
+
+
+def read_profile(path):
+    lines=Path(path).read_text().splitlines()
+    if not lines or not lines[0].startswith('# meta: '):
+        raise ValueError('Missing sigma metadata')
+    meta=json.loads(lines[0][8:])
+    values=np.array([[float(v) for v in line.split()] for line in lines
+                     if line.strip() and not line.lstrip().startswith('#')])
+    axis=np.round(np.linspace(-.025,.025,51),3)
+    if values.shape!=(153,2) or not np.isfinite(values).all():
+        raise ValueError('Need all 153 finite profile rows')
+    if not np.allclose(values[:,0],np.tile(axis,3),rtol=0,atol=1e-12):
+        raise ValueError('Unexpected sigma grid or block order')
+    p=values[:,1].reshape(3,51)
+    if (p<0).any() or p.sum()<=0: raise ValueError('Invalid profile area')
+    return axis,p,meta
+
+
+def historical_ud_path(folder: Path,key: str) -> Path:
+    exact=folder/(key+'.sigma')
+    if exact.is_file(): return exact
+    hits=sorted(folder.glob(key[:14]+'*.sigma'))
+    if len(hits)!=1: raise ValueError('Missing or ambiguous historical UD lookup: '+key)
+    return hits[0]
+
+
+def validate_geometry(sym,x):
+    sym=list(sym);x=np.asarray(x,dtype=float)
+    if not sym or x.shape!=(len(sym),3) or not np.isfinite(x).all():
+        raise ValueError('Invalid molecular coordinates')
+    if any(s not in ('H','C','O') for s in sym):
+        raise ValueError('R10 is restricted to the frozen CHO panel')
+    return sym,x
+
+
+def load_npz(path):
+    with np.load(path,allow_pickle=False) as d:
+        if not {'sym','x','xyz','q','area','atom'}<=set(d.files):
+            raise ValueError('Incomplete P25 segment archive')
+        sym,x=validate_geometry(d['sym'].tolist(),d['x'])
+        seg={k:np.array(d[k],copy=True) for k in ('xyz','q','area','atom')}
+    validate_segments(seg,len(sym))
+    return sym,x,seg
+
+
+def validate_segments(s,natoms):
+    area=np.asarray(s['area']);n=len(area);owner=np.asarray(s['atom'])
+    if not 0<n<=MAX_SEGMENTS or s['xyz'].shape!=(n,3) or s['q'].shape!=(n,) or owner.shape!=(n,):
+        raise ValueError('Invalid surface shape or fixed memory ceiling exceeded')
+    if any(not np.isfinite(v).all() for v in s.values()) or (area<=0).any():
+        raise ValueError('Nonfinite or nonpositive surface inputs')
+    if not np.array_equal(owner,owner.astype(int)) or (owner<0).any() or (owner>=natoms).any():
+        raise ValueError('Owner indices must be zero-based integers within this geometry')
+
+
+def freeze(a) -> int:
+    mac();reg=registration(a.registration);ts=parser_module()
+    sources=committed_sources(SOURCE_FILES)
+    acquired=Path(a.source_root).resolve()
+    check_acquisition(argparse.Namespace(source_root=str(acquired)))
+    if read(acquired/'acquisition.json')['registration']!=reg:
+        raise ValueError('Acquisition belongs to a different registration')
+    shape_path=ROOT/R5_PLAN;shape=read(shape_path)
+    panel={r['key']:r for r in shape['panel']}
+    if len(shape['panel'])!=12 or set(panel)!={r[1] for r in DATA}:
+        raise ValueError('The fixed R5 panel changed')
+    stages_path=ROOT/R5_STAGES
+    if blob(stages_path.read_bytes())!='28f751319c697907454acb098f9f9e01499c2042':
+        raise ValueError('Historical P25 output table changed')
+    # Only identities and provenance hashes are used to select the archived files.
+    stages=pd.read_csv(stages_path,usecols=['key','case','recipe','UD_sha256','source_sha256'])
+    stages=stages[(stages.recipe=='hsieh') & stages['case'].str.rstrip('/').str.endswith('/tz_swig')]
+    if len(stages)!=12 or set(stages.key)!=set(panel) or stages.key.duplicated().any():
+        raise ValueError('Expected exactly the twelve P25 TZVP/SWIG/Hsieh records')
+    stage_by={r.key:r for r in stages.itertuples()}
+    comp_path=ROOT/'data/processed_ext/ud_complist.csv';comp=pd.read_csv(comp_path)
+    from r4_common import selected_profiles
+    compounds_path=ROOT/'data/benchmark/compounds.csv'
+    population=selected_profiles(a.profile_root,pd.read_csv(compounds_path))
+    by_key={k:p for k,_folder,p in population}
+    protected=[record(p) for _k,_folder,p in population]
+    if len(protected)!=636:raise ValueError('The original 630+6 population changed')
+    ud_dir=Path(a.ud_dir).resolve()
+    artifact_root=Path(a.open_artifacts).resolve()
+    candidates=list(artifact_root.rglob('native.json'));rows=[]
+    official=(acquired/'profiles/UD/complist.txt').read_text()
+    from rdkit import Chem
+    for name,key,source,git_blob in DATA:
+        r=panel[key];s=stage_by[key]
+        idx=comp[comp.inchikey==source]
+        if len(idx)!=1:raise ValueError('Source index identity is missing or ambiguous: '+source)
+        idx=idx.iloc[0]
+        if Chem.MolToInchiKey(Chem.MolFromSmiles(str(idx.smiles)))!=source:
+            raise ValueError('Published SMILES and source key disagree')
+        if sum(bool(line.split()) and line.split()[-1]==source for line in official.splitlines())!=1:
+            raise ValueError('Published source key is not unique in the downloaded index')
+        raw=acquired/'profiles/UD/cosmo'/(source+'.cosmo')
+        if blob(raw.read_bytes())!=git_blob:raise ValueError('Raw source changed')
+        ud=historical_ud_path(ud_dir,key)
+        if sha(ud)!=s.UD_sha256:raise ValueError('Mac UD bytes differ from the P25 comparison: '+key)
+        _axis,_ps,meta=read_profile(ud)
+        if meta.get('standard_INCHIKEY') not in (key,source):
+            raise ValueError('UD metadata identity conflicts with the declared mapping')
+        hits=[]
+        for p in candidates:
+            d=read(p)
+            if d.get('key')==key and d.get('method')=='tz_swig':hits.append((p,d))
+        if len(hits)!=1:raise ValueError('Require one original P25 TZVP/SWIG artifact per key: '+key)
+        npth,native=hits[0];folder=npth.parent
+        expected=dict(SCF_converged=True,basis='def2-tzvp',XC='b88,p86',grid_level=3,
+                      lebedev_order=29,eps=1e9,surface_discretization='SWIG')
+        if any(native.get(k)!=v for k,v in expected.items()):raise ValueError('P25 method/provenance mismatch')
+        if native.get('geometry_sha256')!=r['geometry_sha256']:
+            raise ValueError('P25 result has a different generating geometry')
+        geom=shape_path.parent/r['geometry'];gd=read(geom)
+        if sha(geom)!=r['geometry_sha256']:raise ValueError('R5 generating geometry changed')
+        seg=folder/(key+'.segments.npz');sym,x,_=load_npz(seg)
+        if sym!=gd['sym'] or not np.array_equal(x,np.asarray(gd['x'])):
+            raise ValueError('Segments do not belong to the frozen R5 geometry')
+        old=folder/'hsieh'/(key+'.sigma')
+        if sha(old)!=s.source_sha256:raise ValueError('P25 raw replay reference does not match the archive')
+        primary=by_key[key];pg=primary.with_suffix('.xyz.json');gprim=read(pg)
+        if gprim['sym']!=sym or not np.array_equal(np.asarray(gprim['x']),x):
+            raise ValueError('Saved primary geometry differs from P25; no substitute is authorized')
+        protected.append(record(pg))
+        rows.append(dict(name=name,key=key,source_key=source,source_git_blob=git_blob,
+            stereo_alias=source!=key,open_smiles=r['smiles'],source_smiles=str(idx.smiles),
+            published_index_id=int(idx.ud_id),published_name=str(idx['name']),CAS=str(idx.cas),
+            raw=record(raw),UD_profile=record(ud),segments=record(seg),native=record(npth),
+            archived_open_profile=record(old),primary_profile=record(primary),geometry=record(geom)))
+    inputs=[record(shape_path),record(stages_path),record(comp_path),record(compounds_path),
+            record(acquired/'acquisition.json'),record(acquired/'profiles/UD/complist.txt'),
+            record(acquired/'profiles/UD/Readme.txt')]
+    out=private_output(a.out);out.mkdir(parents=True,exist_ok=False)
+    manifest=dict(schema=SCHEMA,base=BASE,upstream=UPSTREAM,registration=reg,sources=sources,
+        packages=packages(),rows=rows,inputs=inputs,protected_population=protected,
+        bin_tolerance_A2=BIN_TOL,SCF_budget=0,model_evaluation_budget=0,
+        notes='Freeze paths and hashes only. The P25 source table links the exact historical UD and open bytes.')
+    write(out/'manifest.json',manifest)
+    (out/'PLAN_SHA256.txt').write_text(sha(out/'manifest.json')+'\n')
+    print('Plan ready; commit PLAN_SHA256.txt before compare:',sha(out/'manifest.json'))
+    return 0
+
+
+def verify_manifest(path,plan_commit):
+    from r10_sources import git
+    if not re.fullmatch('[0-9a-f]{40}',plan_commit):raise ValueError('Full plan-record commit required')
+    git('merge-base','--is-ancestor',plan_commit,'HEAD')
+    wanted=git('show',plan_commit+':'+PLAN_RECORD).decode().strip()
+    if wanted!=sha(path):raise ValueError('Plan digest was not committed before use')
+    m=read(path)
+    if m['schema']!=SCHEMA or m['base']!=BASE or m['upstream']!=UPSTREAM:
+        raise ValueError('Different replay definition')
+    if registration(m['registration']['commit'])!=m['registration']:
+        raise ValueError('Registration identity changed')
+    if packages()!=m['packages']:raise ValueError('Package versions changed after freezing')
+    if m.get('SCF_budget')!=0 or m.get('model_evaluation_budget')!=0 or m['bin_tolerance_A2']!=BIN_TOL:
+        raise ValueError('Budget or tolerance changed')
+    if len(m['rows'])!=12 or {r['key'] for r in m['rows']}!={r[1] for r in DATA}:
+        raise ValueError('Panel incomplete or duplicated')
+    verify_sources(m['sources'])
+    for r in m['inputs']+m['protected_population']:verify_record(r)
+    for r in m['rows']:
+        for field in ('raw','UD_profile','segments','native','archived_open_profile','primary_profile','geometry'):
+            verify_record(r[field])
+    return m
+
+
+def heavy_graph(sym,adj):
+    """Saturated CHO connectivity and attached-H counts, no stereochemical claim."""
+    n=len(sym)
+    if len(adj)!=n:raise ValueError('Bad adjacency')
+    for i,neighbors in enumerate(adj):
+        if len(set(neighbors))!=len(neighbors) or any(j<0 or j>=n or j==i or i not in adj[j] for j in neighbors):
+            raise ValueError('Invalid covalent graph')
+        if sym[i]=='H' and (len(neighbors)!=1 or sym[neighbors[0]]=='H'):
+            raise ValueError('Unsupported hydrogen connectivity')
+    nodes=[i for i,s in enumerate(sym) if s!='H']
+    graph={i:set(j for j in adj[i] if sym[j]!='H') for i in nodes}
+    labels={i:(sym[i],sum(sym[j]=='H' for j in adj[i]),len(graph[i])) for i in nodes}
+    return nodes,graph,labels
+
+
+def graph_maps(sym_a,adj_a,sym_b,adj_b,limit=256):
+    na,ga,la=heavy_graph(sym_a,adj_a);nb,gb,lb=heavy_graph(sym_b,adj_b)
+    if Counter(sym_a)!=Counter(sym_b) or len(na)!=len(nb):raise ValueError('Molecular formulas differ')
+    options={i:[j for j in nb if la[i]==lb[j]] for i in na}
+    order=sorted(na,key=lambda i:(len(options[i]),-len(ga[i]),i));out=[]
+    def visit(k,m,used):
+        if k==len(order):
+            out.append(dict(m))
+            if len(out)>limit:raise ValueError('More than 256 symmetry correspondences; no truncation')
+            return
+        i=order[k]
+        for j in options[i]:
+            if j in used:continue
+            if all((u in ga[i])==(v in gb[j]) for u,v in m.items()):
+                m[i]=j;used.add(j);visit(k+1,m,used);used.remove(j);del m[i]
+    visit(0,{},set())
+    if not out:raise ValueError('Geometry connectivity differs from the declared structure')
+    return sorted(out,key=lambda m:tuple(m[i] for i in sorted(m)))
+
+
+def proper_rmsd(x,y):
+    x=np.asarray(x,float);y=np.asarray(y,float)
+    x=x-x.mean(0);y=y-y.mean(0)
+    u,_,vh=np.linalg.svd(x.T@y);d=np.eye(3);d[-1,-1]=np.sign(np.linalg.det(u@vh))
+    return float(np.sqrt(np.mean(np.sum((x@u@d@vh-y)**2,axis=1))))
+
+
+def dihedral(x,quad):
+    a,b,c,d=np.asarray(x)[list(quad)];axis=c-b;norm=np.linalg.norm(axis)
+    if norm<1e-12:return None
+    axis=axis/norm;u=a-b;v=d-c
+    u=u-(u@axis)*axis;v=v-(v@axis)*axis
+    if min(np.linalg.norm(u),np.linalg.norm(v))<1e-10:return None
+    return float(np.degrees(np.arctan2(np.cross(axis,u)@v,u@v)))
+
+
+def delta_angle(a,b):
+    return None if a is None or b is None else float((b-a+180)%360-180)
+
+
+def geometry_comparison(osym,ox,usym,ux,oc,uc):
+    oa=[r['bonds'] for r in oc['atoms']];ua=[r['bonds'] for r in uc['atoms']]
+    maps=graph_maps(osym,oa,usym,ua);nodes,graph,_=heavy_graph(osym,oa)
+    paths=set()
+    for j in nodes:
+        for k in graph[j]:
+            for i in graph[j]-{k}:
+                for l in graph[k]-{j}:
+                    q=(i,j,k,l)
+                    if len(set(q))==4:paths.add(min(q,q[::-1]))
+    result=[]
+    for m in maps:
+        torsions=[]
+        for q in sorted(paths):
+            target=tuple(m[i] for i in q);a=dihedral(ox,q);b=dihedral(ux,target)
+            torsions.append(dict(kind='heavy',open_atoms=[i+1 for i in q],UD_atoms=[i+1 for i in target],
+                                 open_deg=a,UD_deg=b,delta_deg=delta_angle(a,b)))
+        for o in nodes:
+            hs=[h for h in oa[o] if osym[h]=='H']
+            uhs=[h for h in ua[m[o]] if usym[h]=='H']
+            if osym[o]!='O' or len(hs)!=1 or len(uhs)!=1:continue
+            for carbon in graph[o]:
+                if osym[carbon]!='C':continue
+                for end in graph[carbon]-{o}:
+                    q=(hs[0],o,carbon,end);target=(uhs[0],m[o],m[carbon],m[end])
+                    a=dihedral(ox,q);b=dihedral(ux,target)
+                    torsions.append(dict(kind='OH',open_atoms=[i+1 for i in q],UD_atoms=[i+1 for i in target],
+                                         open_deg=a,UD_deg=b,delta_deg=delta_angle(a,b)))
+        result.append(dict(heavy_mapping_1based=[[i+1,m[i]+1] for i in sorted(m)],
+            heavy_RMSD_A=proper_rmsd(ox[sorted(m)],ux[[m[i] for i in sorted(m)]]),dihedrals=torsions))
+    return dict(correspondences=result,count=len(result),contacts_open=oc['contacts'],contacts_UD=uc['contacts'],
+        contacts_indexing='contacts retain zero-based indices from r4_common; dihedrals/maps above are one-based',
+        scope='All connectivity correspondences retained; proper rotations only for RMSD; no geometry is rotated for averaging')
+
+
+def output_array(output):
+    return np.stack([output.psigmaA_nhb,output.psigmaA_OH,output.psigmaA_OT])
+
+
+def stages(parser,output):
+    df=parser.df;area=df['area / A^2'].to_numpy(float)
+    q=df['charge / e'].to_numpy(float)
+    if not 0<len(area)<=MAX_SEGMENTS or not np.isfinite(area).all() or (area<=0).any() or not np.isfinite(q).all():
+        raise ValueError('Invalid or oversized retained raw table')
+    raw=q/area
+    avg=np.asarray(parser.sigma_averaged,float);p=output_array(output)
+    axis=np.round(np.asarray(output.sigmas),3)
+    pre=np.stack([parser_module().weightbin_sigmas(v,output.sigmas)
+                  for v in (parser.sigma_nhb,parser.sigma_OH,parser.sigma_OT)])
+    total=parser_module().weightbin_sigmas(np.c_[avg,area],output.sigmas)
+    if not np.isfinite(p).all() or (p<0).any() or p.sum()<=0:raise ValueError('Invalid replay profile')
+    conservation=float(np.max(abs(p.sum(0)-total)))
+    if conservation>BIN_TOL or abs(p.sum()-area.sum())>BIN_TOL:
+        raise ValueError('HB/bin conservation failed')
+    owner=df.atom.to_numpy(int)-1
+    if (owner<0).any() or (owner>=len(parser.df_atom)).any():
+        raise ValueError('Invalid raw-table atom owner')
+    atomrows=[]
+    for i in range(len(parser.df_atom)):
+        use=owner==i
+        atomrows.append(dict(atom_1based=i+1,element=str(parser.df_atom.atom.iloc[i]),
+            hb_class=str(parser.df_atom.hb_class.iloc[i]),area_A2=float(area[use].sum()),
+            raw_q_e=float(q[use].sum()),raw_abs_tail_A2=float(area[use & (abs(raw)>=.01)].sum()),
+            averaged_abs_tail_A2=float(area[use & (abs(avg)>=.01)].sum())))
+    desc=dict(segments=len(area),area_sum_A2=float(area.sum()),header_area_A2=float(parser.area_A2),
+        volume_A3=float(parser.volume_A3),raw_q_sum_e=float(q.sum()),
+        raw_sigma_min=float(raw.min()),raw_sigma_max=float(raw.max()),
+        printed_sigma_max_difference=(float(np.max(abs(raw-df['charge/area / e/A^2'].to_numpy(float))))
+            if 'charge/area / e/A^2' in df else None),
+        raw_abs_tail_A2=float(area[abs(raw)>=.01].sum()),
+        averaged_segment_abs_tail_A2=float(area[abs(avg)>=.01].sum()),
+        final_binned_tail_A2=float(p[:,abs(axis)>=.01].sum()),
+        averaged_moment_e=float(area@avg),binned_moment_e=float((p*axis).sum()),
+        binwise_HB_conservation_max_A2=conservation,pre_HB_area_A2=pre.sum(1).tolist(),
+        post_HB_area_A2=p.sum(1).tolist(),atoms=atomrows,
+        post_HB_bins_A2=p.tolist(),pre_HB_bins_A2=pre.tolist())
+    return desc,(raw,area,avg,p)
+
+
+def printed_charge_audit(text,actual_sum):
+    fields={}
+    for name,pattern in (
+        ('original',r'Sum of polarization charges\s*=\s*([-+\d.Ee]+)'),
+        ('corrected',r'Sum of polarization charges\(corr\.\)\s*=\s*([-+\d.Ee]+)')):
+        m=re.search(pattern,text)
+        if m:fields[name]=m.group(1)
+    tokens=[]
+    for line in text.splitlines():
+        parts=line.split()
+        if len(parts)==9 and all(re.fullmatch(r'\d+',v) for v in parts[:2]):
+            try:[Decimal(v) for v in parts[2:]]
+            except Exception:continue
+            tokens.append(parts[5])
+    if not tokens:raise ValueError('No printed DMol segment charge tokens')
+    budget=sum(.5*10.**Decimal(v).as_tuple().exponent for v in tokens)
+    candidates={}
+    for name,token in fields.items():
+        h=float(token);u=.5*10.**Decimal(token).as_tuple().exponent
+        candidates[name]=dict(value_e=h,difference_e=float(actual_sum-h),
+            rounding_consistent=bool(abs(actual_sum-h)<=budget+u+1e-12))
+    return dict(printed_segment_count=len(tokens),charge_column_sum_e=float(actual_sum),
+        charge_column_half_last_decimal_sum_e=float(budget),header_candidates=candidates,
+        meaning='Rounding-only consistency screen, not a correction recipe or a proof of which charge convention was used')
+
+
+def cavity_header(text):
+    labels=('Dielectric Constant','Basic Grid Size','Number of Segments','Solvent Radius',
+            'A - Matrix Cutoff','Radius Increment')
+    out={}
+    for label in labels:
+        m=re.search(r'^\s*'+re.escape(label)+r'\s*=\s*(.*?)\s*$',text,re.M)
+        out[label]=m.group(1) if m else None
+    m=re.search(r'total number of segments\s*:\s*(\d+)',text,re.I)
+    out['actual_segment_record_count']=int(m.group(1)) if m else None
+    m=re.search(r'Molecular car file\s*:\s*([^\r\n]+)',text)
+    out['embedded_car_name']=m.group(1).strip() if m else None
+    block=text.split('COSMO-RS Atomic data',1)
+    radii=[]
+    if len(block)==2:
+        for line in block[1].split('Segment information:',1)[0].splitlines():
+            m=re.fullmatch(r'\s*(\d+)\s+([A-Za-z]+\d*)\s+([-+\d.Ee]+)\s+([-+\d.Ee]+)\s+([-+\d.Ee]+)\s+([-+\d.Ee]+)\s*',line)
+            if m:radii.append(dict(atom_1based=int(m.group(1)),label=m.group(2),radius_A=float(m.group(3))))
+    out['atomic_radii']=radii
+    out['electronic_input_deck_verified']=False
+    out['electronic_protocol_source']='Bell et al. 2020 and VT tutorial; nominal VWN-BP/DNP, not per-file input proof'
+    return out
+
+
+def run_member(r,ts):
+    from r4_common import parser_trace,contacts
+    from zcosmo.pyscf_cosmo import BOHR,RADII
+    if ts.BOHR_TO_ANGSTROM!=BOHR:raise ValueError('Different Bohr conversions in the two raw-table adapters')
+    from rdkit import Chem
+    raw=Path(r['raw']['path']);up=ts.Dmol3COSMOParser(str(raw),num_profiles=3,averaging='Hsieh')
+    uo=up.get_outputs();usym=list(up.df_atom.atom)
+    ux=up.df_atom[['x / A','y / A','z / A']].to_numpy(float)
+    validate_geometry(usym,ux)
+    osym,ox,seg=load_npz(r['segments']['path'])
+    op,oo,_=parser_trace(osym,ox,seg)
+    ud_axis,ud_p,ud_meta=read_profile(r['UD_profile']['path'])
+    _axis,old_p,old_meta=read_profile(r['archived_open_profile']['path'])
+    _axis,primary_p,_=read_profile(r['primary_profile']['path'])
+    ud_diff=float(np.max(abs(output_array(uo)-ud_p)))
+    open_diff=float(np.max(abs(output_array(oo)-old_p)))
+    meta_checks={k:bool(np.isclose(float(uo.meta[k]),float(ud_meta[k]),rtol=0,atol=1e-8))
+                 for k in ('area [A^2]','volume [A^3]','r_av [A]','f_decay','sigma_hb [e/A^2]')}
+    meta_checks['averaging']=uo.meta.get('averaging')==ud_meta.get('averaging')=='Hsieh'
+    meta_checks['disp_flag']=uo.meta['disp. flag']==ud_meta.get('disp. flag')
+    meta_checks['dispersion_value']=bool(np.isclose(float(uo.meta['disp. e/kB [K]']),
+        float(ud_meta['disp. e/kB [K]']),rtol=0,atol=1e-8))
+    if ud_diff>=BIN_TOL or open_diff>=BIN_TOL or not all(meta_checks.values()):
+        raise ValueError(json.dumps(dict(lineage_replay_failed=True,UD_max=ud_diff,
+                                        open_max=open_diff,metadata=meta_checks)))
+    uc=contacts(usym,ux);oc=contacts(osym,ox)
+    # Independently declared structural identities must fit both observed graphs.
+    for smiles,sym,c in ((r['source_smiles'],usym,uc),(r['open_smiles'],osym,oc)):
+        mol=Chem.AddHs(Chem.MolFromSmiles(smiles))
+        es=[a.GetSymbol() for a in mol.GetAtoms()]
+        ea=[[a.GetIdx() for a in atom.GetNeighbors()] for atom in mol.GetAtoms()]
+        graph_maps(es,ea,sym,[a['bonds'] for a in c['atoms']])
+    ud,uv=stages(up,uo);od,ov=stages(op,oo)
+    geom=geometry_comparison(osym,ox,usym,ux,oc,uc)
+    text=raw.read_text();headers=cavity_header(text)
+    if headers['actual_segment_record_count']!=len(up.df):raise ValueError('Printed segment count differs from parsed table')
+    if len(headers['atomic_radii'])!=len(usym):raise ValueError('Atomic-radius block missing or incomplete')
+    qa=printed_charge_audit(text,ud['raw_q_sum_e'])
+    if qa['printed_segment_count']!=len(up.df):raise ValueError('Charge-token count differs from parser')
+    un=uv[3]/uv[3].sum();on=ov[3]/ov[3].sum()
+    comparison=dict(normalized_153_L1=float(abs(un-on).sum()),
+        normalized_total_L1=float(abs(un.sum(0)-on.sum(0)).sum()),
+        raw_area_weighted_W1_e_A2=float(wasserstein_distance(uv[0],ov[0],uv[1],ov[1])),
+        averaged_area_weighted_W1_e_A2=float(wasserstein_distance(uv[2],ov[2],uv[1],ov[1])),
+        delta_final_tail_UD_minus_open_A2=ud['final_binned_tail_A2']-od['final_binned_tail_A2'],
+        note='Distributions on different surfaces; no pointwise tessera correspondence or method/conformer causal separation',
+        open_surface_scope='The archived retained P25 table, without reconstructing discarded tesserae')
+    return dict(key=r['key'],source_key=r['source_key'],stereo_alias=r['stereo_alias'],
+        status='replay_passed',lineage_checks=dict(UD_max_raw_bin_A2=ud_diff,
+        open_max_raw_bin_A2=open_diff,metadata=meta_checks,
+        primary_vs_P25_max_raw_bin_A2=float(abs(primary_p-old_p).max())),
+        cavity_input_fields=headers,open_atomic_radii_A={s:RADII[s] for s in set(osym)},
+        BOHR_TO_ANGSTROM=float(ts.BOHR_TO_ANGSTROM),printed_charge_audit=qa,
+        geometry=geom,UD=ud,open=od,comparison=comparison,
+        stereo_scope='PG source is stereospecific; its benchmark alias is unspecified. Graph matching alone does not certify stereochemistry.',
+        mechanism_resolved=False,adopted=False)
+
+
+def compare(a) -> int:
+    mac();m=verify_manifest(a.manifest,a.plan_commit);ts=parser_module()
+    os.environ['ZC_R3_COOH_FLAG']='1'  # accepted metadata convention, no COOH in this fixed panel
+    out=private_output(a.out);out.mkdir(parents=True,exist_ok=False)
+    start=time.perf_counter();results=[]
+    for r in m['rows']:
+        try:d=run_member(r,ts)
+        except Exception as exc:
+            d=dict(key=r['key'],source_key=r['source_key'],status='blocked',
+                   error=type(exc).__name__+': '+str(exc),adopted=False)
+        results.append(d);write(out/(r['key']+'.json'),d)
+        write(out/'summary.json',dict(complete=False,requested=12,processed=len(results),rows=results,
+            SCF_calls=0,model_calls=0,adopted=False,mechanism_resolved=False))
+    verify_manifest(a.manifest,a.plan_commit)
+    if any(name=='pyscf' or name.startswith('pyscf.') for name in sys.modules):
+        raise RuntimeError('Unexpected native PySCF import during a zero-QC replay')
+    passed=all(r['status']=='replay_passed' for r in results)
+    write(out/'summary.json',dict(schema=SCHEMA,complete=True,all_lineage_gates_passed=passed,
+        requested=12,processed=12,rows=results,base=BASE,registration=m['registration'],
+        manifest_sha256=sha(a.manifest),plan_commit=a.plan_commit,packages=m['packages'],
+        wall_s=time.perf_counter()-start,SCF_calls=0,model_calls=0,adopted=False,
+        mechanism_resolved=False,native_calculations_authorized=False,
+        summary_scope='Same-parser input comparison. A successful replay links stored bytes; it is not a liquid-state or method-accuracy validation.'))
+    return 0 if passed else 2
+
+
+def check(a) -> int:
+    d=read(a.summary)
+    if d.get('schema')!=SCHEMA or d.get('complete') is not True or d.get('all_lineage_gates_passed') is not True:
+        raise ValueError('Lineage/replay incomplete or failed; do not interpret a partial panel as complete')
+    if len(d['rows'])!=12 or {r['key'] for r in d['rows']}!={r[1] for r in DATA}:
+        raise ValueError('Missing, extra, or duplicate member')
+    if any(r.get('status')!='replay_passed' for r in d['rows']):raise ValueError('Blocked member')
+    if d.get('SCF_calls')!=0 or d.get('model_calls')!=0 or d.get('adopted') is not False:
+        raise ValueError('This is not the registered zero-QC, non-adopting replay')
+    print('All 12 lineage/replay gates passed; mechanism and production adoption remain unresolved')
+    return 0
+
+
+def main() -> int:
+    if Path.cwd().resolve()!=ROOT:raise ValueError('Run this command from the repository root')
+    p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='cmd',required=True)
+    q=s.add_parser('freeze');q.add_argument('--source-root',required=True);q.add_argument('--open-artifacts',required=True)
+    q.add_argument('--profile-root',default='data/pyscf_sigma');q.add_argument('--ud-dir',default='data/raw/nist/UD/sigma3')
+    q.add_argument('--registration',required=True);q.add_argument('--out',required=True);q.set_defaults(fn=freeze)
+    q=s.add_parser('compare');q.add_argument('--manifest',required=True);q.add_argument('--plan-commit',required=True)
+    q.add_argument('--out',required=True);q.set_defaults(fn=compare)
+    q=s.add_parser('check');q.add_argument('--summary',required=True);q.set_defaults(fn=check)
+    a=p.parse_args();return a.fn(a)
+
+if __name__=='__main__':raise SystemExit(main())
diff --git a/scripts/r10_selftest.py b/scripts/r10_selftest.py
new file mode 100644
--- /dev/null
+++ b/scripts/r10_selftest.py
@@ -0,0 +1,284 @@
+"""Portable tests of R10 bookkeeping/geometry math, not a UD or quantum calculation."""
+from __future__ import annotations
+import argparse
+from contextlib import ExitStack
+import json
+from pathlib import Path
+import tempfile
+import types
+import unittest
+from unittest.mock import patch
+import numpy as np
+import pandas as pd
+import r10_sources as src
+import r10_replay as replay
+
+
+def sigma_file(path,p,meta=None):
+    m=meta or {'volume [A^3]':10.}
+    text='# meta: '+json.dumps(m)+'\n'
+    grid=np.round(np.linspace(-.025,.025,51),3)
+    text+=''.join(f'{s:.3f} {a:.16e}\n' for s,a in zip(np.tile(grid,3),np.asarray(p).ravel()))
+    Path(path).write_text(text)
+
+
+def binning(values,grid):
+    p=np.zeros(51)
+    for sigma,area in np.asarray(values).reshape(-1,2):
+        if not grid[0]<sigma<grid[-1]:raise ValueError('synthetic test sigma outside interior grid')
+        left=min(int((sigma-grid[0])/(grid[1]-grid[0])),49)
+        f=(sigma-grid[left])/(grid[left+1]-grid[left])
+        p[left]+=area*(1-f);p[left+1]+=area*f
+    return p
+
+
+class TestSources(unittest.TestCase):
+    def test_verified_catalog(self):
+        c=src.catalog();self.assertEqual(len(c),14)
+        self.assertEqual(len({r['relative_path'] for r in c}),14)
+        self.assertEqual(len(src.DATA),12)
+        for r in c:self.assertEqual(len(r['expected_git_blob']),40)
+        aliases=[r for r in c if 'source_key' in r and r['source_key']!=r['key']]
+        self.assertEqual(len(aliases),1)
+        self.assertEqual(aliases[0]['source_key'],'DNIAPMSPPWPWGF-VKHMYHEASA-N')
+
+    def test_exact_download_bytes(self):
+        b=b'not real COSMO data\r\n'
+        src.verify_download(b,src.blob(b))
+        with self.assertRaises(ValueError):src.verify_download(b.replace(b'\r\n',b'\n'),src.blob(b))
+
+    def test_frozen_input_mutation(self):
+        with tempfile.TemporaryDirectory() as t:
+            p=Path(t)/'file';p.write_bytes(b'original');r=src.record(p)
+            self.assertEqual(src.verify_record(r),p)
+            p.write_bytes(b'mutated')
+            with self.assertRaises(ValueError):src.verify_record(r)
+
+    def test_output_root_is_private_and_fresh(self):
+        with self.assertRaises(ValueError):src.private_output(src.ROOT/'production')
+        with tempfile.TemporaryDirectory() as t:
+            with self.assertRaises(FileExistsError):src.private_output(t)
+            self.assertEqual(src.private_output(Path(t)/'new'),Path(t)/'new')
+
+    def test_json_rejects_nonfinite(self):
+        with tempfile.TemporaryDirectory() as t:
+            with self.assertRaises(ValueError):src.write(Path(t)/'bad.json',{'value':np.nan})
+
+    def test_lookup_is_explicit_and_unique(self):
+        key='DNIAPMSPPWPWGF-UHFFFAOYSA-N'
+        with tempfile.TemporaryDirectory() as t:
+            root=Path(t);source=root/'DNIAPMSPPWPWGF-VKHMYHEASA-N.sigma';source.write_text('fixture')
+            self.assertEqual(replay.historical_ud_path(root,key),source)
+            (root/'DNIAPMSPPWPWGF-SYNTHETICA-N.sigma').write_text('another')
+            with self.assertRaises(ValueError):replay.historical_ud_path(root,key)
+            exact=root/(key+'.sigma');exact.write_text('exact fixture')
+            self.assertEqual(replay.historical_ud_path(root,key),exact)
+
+
+class TestArrays(unittest.TestCase):
+    def test_sigma_roundtrip_and_wrong_order(self):
+        rng=np.random.default_rng(20261007);p=rng.random((3,51))
+        with tempfile.TemporaryDirectory() as t:
+            f=Path(t)/'a.sigma';sigma_file(f,p)
+            axis,q,_=replay.read_profile(f);self.assertLess(abs(p-q).max(),1e-15)
+            lines=f.read_text().splitlines();lines[1]='0.024 1.0';f.write_text('\n'.join(lines))
+            with self.assertRaises(ValueError):replay.read_profile(f)
+
+    def test_sigma_nonfinite_and_negative(self):
+        with tempfile.TemporaryDirectory() as t:
+            f=Path(t)/'a.sigma';p=np.ones((3,51));p[0,0]=np.nan;sigma_file(f,p)
+            with self.assertRaises(ValueError):replay.read_profile(f)
+            p[0,0]=-1.;sigma_file(f,p)
+            with self.assertRaises(ValueError):replay.read_profile(f)
+
+    def test_npz_shapes_and_owner(self):
+        with tempfile.TemporaryDirectory() as t:
+            f=Path(t)/'s.npz'
+            kw=dict(sym=np.array(['O','H','H']),x=np.eye(3),xyz=np.eye(3),q=np.zeros(3),area=np.ones(3),atom=np.arange(3))
+            np.savez(f,**kw);self.assertEqual(replay.load_npz(f)[0],['O','H','H'])
+            kw['atom']=np.array([0,1,3]);np.savez(f,**kw)
+            with self.assertRaises(ValueError):replay.load_npz(f)
+            kw['atom']=np.array([0.,1.,1.5]);np.savez(f,**kw)
+            with self.assertRaises(ValueError):replay.load_npz(f)
+
+    def test_stages_separate_raw_and_binned_tail(self):
+        grid=np.arange(-.025,.025+.0001,.001)
+        area=np.array([2.,3.]);q=np.array([.024,-.024]);av=np.array([.004,-.006])
+        parser=types.SimpleNamespace(df=pd.DataFrame({'area / A^2':area,'charge / e':q,'atom':[1,2]}),
+            df_atom=pd.DataFrame({'atom':['O','H'],'hb_class':['OH','OH']}),
+            sigma_averaged=av,sigma_nhb=np.c_[av,area],sigma_OH=np.empty((0,2)),sigma_OT=np.empty((0,2)),
+            area_A2=5.,volume_A3=10.)
+        total=binning(np.c_[av,area],grid)
+        result=types.SimpleNamespace(sigmas=grid,psigmaA_nhb=total.copy(),psigmaA_OH=np.zeros(51),psigmaA_OT=np.zeros(51))
+        with patch.object(replay,'parser_module',return_value=types.SimpleNamespace(weightbin_sigmas=binning)):
+            desc,_=replay.stages(parser,result)
+            self.assertEqual(desc['raw_abs_tail_A2'],2.)
+            self.assertEqual(desc['final_binned_tail_A2'],0.)
+            result.psigmaA_nhb[25]+=1e-4
+            with self.assertRaises(ValueError):replay.stages(parser,result)
+
+    def test_printed_charge_audit_not_neutralization(self):
+        text='''Sum of polarization charges = -0.01000
+Sum of polarization charges(corr.) = 0.00000
+1 1 0.00000 0.00000 0.00000 -0.00500 1.00000 -0.00500 0.0
+2 1 1.00000 0.00000 0.00000 -0.00500 1.00000 -0.00500 0.0
+'''
+        r=replay.printed_charge_audit(text,-.01000)
+        self.assertEqual(r['printed_segment_count'],2)
+        self.assertAlmostEqual(r['charge_column_half_last_decimal_sum_e'],1e-5)
+        self.assertTrue(r['header_candidates']['original']['rounding_consistent'])
+        self.assertFalse(r['header_candidates']['corrected']['rounding_consistent'])
+
+    def test_cavity_setting_is_not_actual_segment_count(self):
+        text=''' Dielectric Constant = infinity
+ Number of Segments = 92
+ Molecular car file :
+552.car
+ COSMO-RS Atomic data
+ 1 O1 1.72 0.1 16.0 0.01
+ 2 H1 1.30 -0.1 8.0 -0.01
+ Segment information:
+ total number of segments: 406
+'''
+        d=replay.cavity_header(text)
+        self.assertEqual(d['Number of Segments'],'92')
+        self.assertEqual(d['actual_segment_record_count'],406)
+        self.assertEqual(d['embedded_car_name'],'552.car')
+        self.assertEqual(len(d['atomic_radii']),2)
+        self.assertFalse(d['electronic_input_deck_verified'])
+
+
+class TestGeometry(unittest.TestCase):
+    def test_graph_permutation_and_symmetry(self):
+        # Synthetic O-C-C-O graph with hydrogens. No geometry optimization.
+        sym=['O','C','C','O','H','H','H','H','H','H']
+        adj=[[1,4],[0,2,5,6],[1,3,7,8],[2,9],[0],[1],[1],[2],[2],[3]]
+        perm=[3,2,1,0,9,8,7,6,5,4];inv={v:i for i,v in enumerate(perm)}
+        sb=[sym[i] for i in perm];ab=[[inv[j] for j in adj[i]] for i in perm]
+        maps=replay.graph_maps(sym,adj,sb,ab);self.assertEqual(len(maps),2)
+        with self.assertRaises(ValueError):replay.graph_maps(sym,adj,sb,ab,limit=1)
+
+    def test_graph_wrong_formula_or_connectivity(self):
+        a=['C','O','H'];g=[[1],[0,2],[1]]
+        with self.assertRaises(ValueError):replay.graph_maps(a,g,['C','N','H'],g)
+        with self.assertRaises(ValueError):replay.graph_maps(a,g,a,[[1],[0],[]])
+
+    def test_proper_rotation_rejects_reflection(self):
+        rng=np.random.default_rng(4);x=rng.normal(size=(8,3))
+        q,_=np.linalg.qr(rng.normal(size=(3,3)));q[:,0]*=np.linalg.det(q)
+        self.assertLess(replay.proper_rmsd(x,x@q+[4,2,1]),2e-15)
+        y=x.copy();y[:,0]*=-1
+        self.assertGreater(replay.proper_rmsd(x,y),.1)
+
+    def test_dihedral_periodicity_and_singularity(self):
+        a=np.array([[1.,0,0],[0,0,0],[0,1,0],[0,1,1]])
+        self.assertAlmostEqual(abs(replay.dihedral(a,(0,1,2,3))),90.)
+        self.assertEqual(replay.delta_angle(179.,-179.),2.)
+        self.assertIsNone(replay.dihedral(np.zeros((4,3)),(0,1,2,3)))
+
+
+class TestResults(unittest.TestCase):
+    def test_failure_does_not_drop_later_members(self):
+        manifest={'rows':[dict(key=r[1],source_key=r[2]) for r in src.DATA],
+                  'registration':{'commit':'a'*40},'packages':{}}
+        bad=src.DATA[2][1]
+        def member(r,ts):
+            if r['key']==bad:raise ValueError('synthetic parity failure')
+            return dict(key=r['key'],status='replay_passed',adopted=False)
+        with tempfile.TemporaryDirectory() as t,ExitStack() as stack:
+            p=Path(t)/'manifest.json';src.write(p,manifest)
+            stack.enter_context(patch.object(replay,'mac'))
+            stack.enter_context(patch.object(replay,'verify_manifest',return_value=manifest))
+            stack.enter_context(patch.object(replay,'parser_module',return_value=None))
+            stack.enter_context(patch.object(replay,'run_member',side_effect=member))
+            rc=replay.compare(argparse.Namespace(manifest=str(p),plan_commit='b'*40,out=str(Path(t)/'out')))
+            d=src.read(Path(t)/'out/summary.json')
+            self.assertEqual(rc,2);self.assertEqual(d['processed'],12)
+            self.assertEqual(sum(r['status']=='blocked' for r in d['rows']),1)
+            self.assertFalse(d['all_lineage_gates_passed'])
+            with self.assertRaises(ValueError):replay.check(argparse.Namespace(summary=Path(t)/'out/summary.json'))
+
+    def test_checker_rejects_missing_or_duplicated_member(self):
+        d=dict(schema=replay.SCHEMA,complete=True,all_lineage_gates_passed=True,
+               rows=[dict(key=r[1],status='replay_passed') for r in src.DATA],SCF_calls=0,model_calls=0,adopted=False)
+        with tempfile.TemporaryDirectory() as t:
+            p=Path(t)/'summary.json';src.write(p,d)
+            self.assertEqual(replay.check(argparse.Namespace(summary=p)),0)
+            d['rows'][-1]=d['rows'][0];src.write(p,d)
+            with self.assertRaises(ValueError):replay.check(argparse.Namespace(summary=p))
+
+
+    def test_member_adapter_and_lineage_gate(self):
+        # Exercise run_member, not just the component routines. Synthetic water,
+        # mocked legacy adapters; this is deliberately NOT an actual UD replay.
+        sym=['O','H','H'];x=np.array([[0.,0,0],[.96,0,0],[-.24,.93,0]])
+        area=np.array([2.,1.,1.]);charge=np.array([.01,-.005,-.005])
+        avg=np.array([.004,-.003,-.003]);grid=np.arange(-.025,.025+.0001,.001)
+        meta={'area [A^2]':4.,'volume [A^3]':10.,'r_av [A]':1.5,'f_decay':3.57,
+              'disp. flag':'H2O','disp. e/kB [K]':70.,'averaging':'Hsieh','sigma_hb [e/A^2]':.0084}
+        total=binning(np.c_[avg,area],grid)
+        output=types.SimpleNamespace(sigmas=grid,psigmaA_nhb=total,
+            psigmaA_OH=np.zeros(51),psigmaA_OT=np.zeros(51),meta=meta)
+        def parser():
+            return types.SimpleNamespace(
+                df=pd.DataFrame({'area / A^2':area,'charge / e':charge,'atom':[1,2,3]}),
+                df_atom=pd.DataFrame({'atom':sym,'hb_class':['OH']*3,
+                                     'x / A':x[:,0],'y / A':x[:,1],'z / A':x[:,2]}),
+                area_A2=4.,volume_A3=10.,sigma_averaged=avg,
+                sigma_nhb=np.c_[avg,area],sigma_OH=np.empty((0,2)),sigma_OT=np.empty((0,2)),
+                get_outputs=lambda:output)
+        ts=types.SimpleNamespace(BOHR_TO_ANGSTROM=.52917721067,
+             Dmol3COSMOParser=lambda *a,**k:parser(),weightbin_sigmas=binning)
+        rc=types.ModuleType('r4_common')
+        rc.parser_trace=lambda *a:(parser(),output,{})
+        rc.contacts=lambda *a:{'atoms':[{'bonds':[1,2]},{'bonds':[0]},{'bonds':[0]}],'contacts':[]}
+        z=types.ModuleType('zcosmo');z.__path__=[]
+        pc=types.ModuleType('zcosmo.pyscf_cosmo');pc.BOHR=ts.BOHR_TO_ANGSTROM;pc.RADII={'H':1.3,'O':1.72}
+        z.pyscf_cosmo=pc
+        with tempfile.TemporaryDirectory() as t,ExitStack() as stack:
+            root=Path(t);raw=root/'synthetic.cosmo'
+            raw.write_text('''Dielectric Constant = infinity
+COSMO-RS Atomic data
+ 1 O1 1.72 0.01 2.0 0.005
+ 2 H1 1.30 -0.005 1.0 -0.005
+ 3 H2 1.30 -0.005 1.0 -0.005
+Segment information:
+total number of segments: 3
+Sum of polarization charges = 0.00000
+1 1 0.0 0.0 0.0 0.01000 2.0 0.005 0.0
+2 2 1.0 0.0 0.0 -0.00500 1.0 -0.005 0.0
+3 3 0.0 1.0 0.0 -0.00500 1.0 -0.005 0.0
+''')
+            npz=root/'a.npz';np.savez(npz,sym=sym,x=x,xyz=x,area=area,q=charge,atom=np.arange(3))
+            a=replay.output_array(output)
+            for f in ('ud.sigma','old.sigma','primary.sigma'):sigma_file(root/f,a,meta)
+            r=dict(key=src.DATA[0][1],source_key=src.DATA[0][2],stereo_alias=False,
+                source_smiles='O',open_smiles='O',raw=src.record(raw),segments=src.record(npz),
+                UD_profile=src.record(root/'ud.sigma'),archived_open_profile=src.record(root/'old.sigma'),
+                primary_profile=src.record(root/'primary.sigma'))
+            stack.enter_context(patch.dict('sys.modules',{'r4_common':rc,'zcosmo':z,'zcosmo.pyscf_cosmo':pc}))
+            stack.enter_context(patch.object(replay,'parser_module',return_value=ts))
+            d=replay.run_member(r,ts)
+            self.assertEqual(d['status'],'replay_passed')
+            self.assertEqual(d['geometry']['count'],1)
+            self.assertFalse(d['mechanism_resolved'])
+            self.assertLess(d['lineage_checks']['UD_max_raw_bin_A2'],1e-14)
+            a[0,25]+=1e-5;sigma_file(root/'ud.sigma',a,meta)
+            with self.assertRaises(ValueError):replay.run_member(r,ts)
+
+    def test_mac_requirement_is_not_a_native_install_requirement(self):
+        with patch.object(src.sys,'platform','linux'):
+            with self.assertRaises(RuntimeError):src.mac()
+        with patch.object(src.sys,'platform','darwin'):src.mac()
+
+
+def main():
+    p=argparse.ArgumentParser();p.add_argument('--out');a=p.parse_args()
+    suite=unittest.defaultTestLoader.loadTestsFromModule(__import__(__name__))
+    result=unittest.TextTestRunner(verbosity=2).run(suite)
+    summary=dict(tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),
+                 passed=result.wasSuccessful(),scope='Portable synthetic checks only',SCF_calls=0,UD_comparisons=0)
+    if a.out:src.write(a.out,summary)
+    return 0 if result.wasSuccessful() else 1
+
+if __name__=='__main__':raise SystemExit(main())
```
<!-- END PATCH P42 -->

<!-- BEGIN PATCH P43 -->
```diff
diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -52,3 +52,8 @@
 energy-gradient mismatch unresolved; its numerical diagnostic budget is closed.
 See [round-7 evidence](docs/astra/round7/RESULTS.md) and
 [endpoint acceptance](docs/astra/round6/RESULTS.md).
+
+A [round-10 provenance review](docs/astra/round10/PROVENANCE_STATUS.md) located
+public UD geometry and raw-surface files. Matching those files to the Mac's
+historical profiles remains a separate zero-QC replay; the glycol mechanism
+and the closed numerical-gradient campaign are unchanged.
diff --git a/docs/astra/round7/GLYCOL_STATUS.md b/docs/astra/round7/GLYCOL_STATUS.md
--- a/docs/astra/round7/GLYCOL_STATUS.md
+++ b/docs/astra/round7/GLYCOL_STATUS.md
@@ -13,3 +13,29 @@
 Evidence that can change this decision is concrete: recovery of the generating UD geometries and raw surface files together with their electronic/cavity settings; or independent, basis/grid/response-converged electrostatic references at frozen known geometries; or a complete, independently reproducible basin and nuclear-partition audit under one free-energy convention. Acquiring provenance is a zero-QC task. Any new physical calculation needs a fixed structural panel including water and branched polyol controls, and a prospective budget. Missing historical files on the Mac do not prove that no upstream archive exists.
 
 The present open-profile pipeline is a reproducible, explicitly tested alternative source of single-geometry sigma profiles. It is not an accuracy-equivalent UD replacement or an established phase-dependent conformer ensemble. P28's accepted endpoint correction does not remove this distinction. Keep pre-P28 matched comparisons labelled as such, and do not infer a corrected matched-subset mean from differently sized standalone means.
+
+Update, 2026-10-07, round-10 source discovery. The statements above about
+unavailable UD raw inputs describe the project's holdings during R4-R9. The
+NIST COSMOSAC repository contains public .cosmo files for the fixed R5 panel,
+including all four glycols. These contain atomic coordinates and surface rows,
+with cavity parameters. Published nominal electronic-method documentation is
+available, but the exact electronic deck and convergence history for each file
+are not thereby verified. The next step is the registered zero-QC lineage and
+same-parser comparison described in [the provenance record](../round10/PROVENANCE_STATUS.md).
+This discovery does not itself identify the cause of the glycol prediction gap.
+
+Here, the P29 "raw area profile" means an unnormalized final sigma profile,
+not the pre-averaging charge density of the original tesserae. Those two tail
+measures must remain distinct. P25 located sensitivity within the tested open
+pipeline but had no matched UD raw table; it did not establish a unique
+historical raw-charge or electronic-method cause. The earlier numerical values
+and finite-sample envelope statements are retained with those scopes.
+
+The public UD notice reports that some database conformations were revised
+using vapor-pressure predictions. It does not identify which members of this
+panel were revised. Z0x's absence of ThermoML fitting does not establish that
+all upstream reference inputs were selected without empirical information.
+UD is a documented comparator, not a validated equilibrium conformer ensemble.
+No new quantum calculation, conformer selection or production replacement is
+authorized by this source discovery. The 630 primary and six S1/S2 files stay
+frozen, and the numerical-gradient campaign remains closed.
diff --git a/docs/astra/round10/PROVENANCE_STATUS.md b/docs/astra/round10/PROVENANCE_STATUS.md
new file mode 100644
--- /dev/null
+++ b/docs/astra/round10/PROVENANCE_STATUS.md
@@ -0,0 +1,53 @@
+UD glycol provenance, source discovery only
+
+The public NIST COSMOSAC distribution at commit
+`1b82456be38026719b16cad4076109bef3fcb309` contains DMol3 `.cosmo` files for
+all twelve members of the fixed R5 panel. The reviewed zcosmo baseline is
+`4dc898521f6c49355e442be78f1e2570d3686aee`. Exact paths and Git blob identifiers
+are in `scripts/r10_sources.py`; `catalog` prints the pinned retrieval URLs.
+
+[The public raw directory](https://github.com/usnistgov/COSMOSAC/tree/1b82456be38026719b16cad4076109bef3fcb309/profiles/UD/cosmo)
+contains embedded atomic coordinates, surface positions and charges, with
+per-atom radii and printed cavity settings. For EG the embedded `552.car` is
+not the current compound-list identifier: the project index uses 552 for a
+different compound. Source filenames, explicit molecular identities and hashes
+must govern the mapping. An input setting labelled "Number of Segments" is
+also distinct from the actual surface-table row count.
+
+The propylene-glycol source is `DNIAPMSPPWPWGF-VKHMYHEASA-N`, while the benchmark
+uses `DNIAPMSPPWPWGF-UHFFFAOYSA-N`. This is the existing unique-connectivity
+lookup, made explicit, not proof that their stereochemical declarations are
+identical. No undisclosed filename or atom-order substitution is allowed.
+
+[The UD data notice](https://github.com/usnistgov/COSMOSAC/blob/1b82456be38026719b16cad4076109bef3fcb309/profiles/UD/Readme.txt)
+reports a mixture of UD and later additions, and revisions to some conformations
+based on vapor-pressure predictions. It supplies no per-glycol revision label.
+The notice also limits permitted use and redistribution. Public accessibility
+is not a grant of unrestricted commercial-use or redistribution rights.
+Recovered files and detailed replay outputs remain in private local storage,
+not in this repository or in a public Actions artifact.
+
+[Bell et al., 2020](https://doi.org/10.1021/acs.jctc.9b01016) and the
+[VT profile-generation materials](https://design.che.vt.edu/Downloads/VT_Sigma_Profile_Databases.html)
+describe the nominal DMol3 GGA/VWN-BP/DNP procedure. This is literature-level
+provenance, not proof of a particular file's full electronic input or convergence
+history. The downloaded `.cosmo` header directly establishes its printed cavity
+parameters. The exact electronic decks and output logs remain unverified for
+the twelve individual files. The VT site advertises raw-COSMO and GO/EC OUTMOL
+archives; their individual contents and correspondence to revised UD members
+were not verified in this review.
+
+P41/P42 first require the recovered raw tables to regenerate the exact Mac UD
+profiles whose hashes are already recorded by P25. The archived open TZVP/SWIG
+tables are replayed through the same pinned Hsieh/NHB/OH/OT implementation and
+checked against their own P25 profile hashes. A successful replay establishes
+input lineage within numerical tolerance. It does not establish liquid-state
+accuracy or separate conformer effects from electronic/cavity effects when both
+historical geometry and method differ. No such comparison has yet been executed
+on the Mac as part of this report.
+
+Geometry descriptors retain all graph correspondences and the original contact
+criteria. Raw segment distributions and unnormalized final-profile tails are
+reported separately. No new conformer or electrostatic correction is selected.
+The P35 mechanism remains unresolved pending evidence, the numerical-gradient
+campaign stays closed, and the 630+6 profile version remains unchanged.
```
<!-- END PATCH P43 -->

<!-- BEGIN PATCH REG10 -->
```diff
diff --git a/docs/astra/round10/REGISTRATION_PROPOSED.md b/docs/astra/round10/REGISTRATION_PROPOSED.md
new file mode 100644
--- /dev/null
+++ b/docs/astra/round10/REGISTRATION_PROPOSED.md
@@ -0,0 +1,139 @@
+R10-P41-P42-P43: UD provenance, zero-QC replay
+
+Proposed registration. Append adopted text to PREREGISTRATION.md with the actual
+commit identity before acquisition or comparison. This file alone is not an
+acceptance record. The reviewed baseline is
+4dc898521f6c49355e442be78f1e2570d3686aee. R8/R9's numerical-gradient campaign
+remains closed. P32 remains failed; no stopped chain is restarted. P35 is opened
+only for provenance acquisition and a descriptive same-parser comparison, not
+for a claim that its physical mechanism is resolved.
+
+The public source locations and raw Git blob identifiers were discovered during
+this review. No new quantum computation or UD/open numerical comparison was
+performed in that review. The design is motivated by previously inspected R4-R9
+results, not a new experimental holdout. No ThermoML response, UD tail target or
+conformer energy selects a parameter or a member.
+
+P41 is E acquisition and integrity checking. Use only the twelve raw `.cosmo`
+files and two provenance documents in scripts/r10_sources.py at public NIST
+COSMOSAC commit 1b82456be38026719b16cad4076109bef3fcb309. Verify the exact Git
+blob for each download and record a SHA256 of its bytes. Preserve line endings.
+One request per file, a 30-second socket timeout and an 8 MB per-file ceiling;
+no alternative source, automatic retry, file replacement or incomplete-success
+claim. Retain every failed acquisition status. The twelve compounds are water,
+methanol, EG, DEG, TEG, tetraethylene glycol, glycerol, propylene glycol,
+2-methoxyethanol, 1,2-dimethoxyethane, THF and n-nonane, as in the fixed R5 panel.
+
+The data notice is independent of any repository code license. The operator
+must review applicable use rights and acknowledge them before acquisition.
+Neither this registration nor public availability grants redistribution or
+commercial-use permission. Downloaded data and detailed derived reports remain
+outside the repository on the Mac. Do not place raw data, geometries or dense
+replayed profiles in public Actions artifacts. This round launches no Actions
+computation; downloading already-existing P25 artifacts is retrieval only.
+
+P42 is E read-only input comparison with same-input numerical replay gates.
+Before calculating descriptors, freeze the source files and all original
+630+6 profile hashes. Freeze the twelve saved generating geometries and exactly
+one original P25 TZVP/SWIG result per key. Match native geometry hashes against
+cloud/r5/shape-plan/manifest.json and coordinates against both the stored NPZ
+and primary saved JSON. Match each archived P25 Hsieh profile and Mac UD profile
+to the SHA256 already recorded in p25_stage_comparison.csv. Missing, conflicting,
+changed or duplicate sources stop preparation. No newly generated raw table
+may silently replace an absent artifact. If archived artifacts are no longer
+available, report that limitation; do not rerun their SCFs under this budget.
+
+Match compound identities using the public list and the project's
+ud_complist.csv, with explicit source and target keys. Propylene glycol maps
+benchmark DNIAPMSPPWPWGF-UHFFFAOYSA-N to published
+DNIAPMSPPWPWGF-VKHMYHEASA-N. This follows the existing unique-connectivity lookup
+and is an explicit stereochemical limitation. Never use embedded .car numbers
+as compound-list identifiers, or choose among ambiguous skeleton matches.
+
+The external manifest records all input hashes, reviewed code hashes and the
+normalized Mac package versions. Commit its SHA256, and only that SHA256, in
+docs/astra/round10/PLAN_SHA256.txt before the first comparison. Pass that actual
+plan commit to the comparison command. The actual registration commit must be
+an ancestor of HEAD and contain this marker. The frozen source files and inputs
+are checked again before and after the comparison; package drift blocks it.
+
+Use the reviewed project to_sigma.py Git blob
+9f2e0d6f3bb4da4880f9bd6ad702847f9308ed1d for both paths. Parse historical UD
+DMol3 output using Dmol3COSMOParser(num_profiles=3, averaging='Hsieh'). Adapt
+archived retained open segments using the existing r4_common.parser_trace.
+Keep the 0.52917721067 Bohr-to-angstrom conversion and existing Hsieh and HB
+constants. Read the actual charge column and recompute charge/area; do not use
+the rounded printed density instead. Do not neutralize charges, choose a
+correction column by closeness to a reference, clip a sigma, change atom
+classification, or tune averaging. No new surface filter is applied to the
+archived open table. A parser exception is a failed replay, not permission to
+alter the parser in the same experiment.
+
+Require every replay to reproduce its own stored 153-bin area profile with
+maximum absolute difference strictly below 1e-8 square angstroms. UD area,
+volume, averaging metadata and dispersion metadata must also match their
+historical values at the stated 1e-8 numeric tolerance. Require binwise HB-area
+conservation and total retained area within 1e-8 square angstroms. This is a
+same-input integrity gate, not an E claim that open and UD physical profiles
+match. There is no experimental accuracy acceptance criterion or model scoring
+in R10. Primary-versus-P25 differences are reported separately and never used
+to replace or relabel a primary file.
+
+Only after a member passes its lineage/replay gate, compare its geometries and
+raw distributions. Check observed covalent connectivity against declared RDKit
+structures. Retain every heavy-atom graph isomorphism, with an explicit ceiling
+of 256 that fails rather than truncates a symmetry search. Report each proper-
+rotation heavy-atom RMSD and its heavy-chain and H-O-C-X dihedrals. Do not reflect,
+reorient or modify a geometry used for charge averaging. Symmetry correspondence
+is not conformer generation; graph matching does not certify stereochemistry.
+
+Retain the existing contact definition from r4_common: donor-acceptor distance
+at most 3.2 angstroms, H-acceptor distance at most 2.5 angstroms and D-H-A angle
+at least 120 degrees. Report all candidate contact geometries and the indicator;
+never interpret the indicator as an H-bond energy or exclude a structure using
+it. Water and the branched-polyol controls remain in the panel even when their
+responses differ from those of the linear glycols.
+
+Report raw charge sums and area-weighted sigma distributions, then the
+averaged distribution and pre/post-HB bins. Distinguish the raw tessera tail,
+averaged continuous-segment tail and unnormalized final binned-profile tail.
+The fixed tail threshold is absolute sigma at least 0.01 e/A^2, inclusive on the
+rounded three-decimal output grid. Preserve normalized-profile distances and
+atom-resolved areas. Do not pair tessera rows from different surfaces by ordinal.
+Preserve original and corrected printed charge summaries and a rounding-only
+charge-sum screen; that screen does not assign a new physical convention.
+
+Read cavity metadata literally. Record the input setting called "Number of
+Segments" separately from the actual table count, and record the embedded
+.car name without treating it as a modern index. The public papers and tutorial
+establish nominal electronic-method context. Mark per-file electronic-deck and
+solver-history verification as absent unless independent exact records have
+actually been obtained. File-header metadata cannot fill in an absent method.
+
+All twelve requested identities retain outcomes. A failure blocks that member's
+scientific comparison, while independent members continue. Overall success
+requires all twelve lineage gates, exact input integrity and zero native/model
+calls. A partial panel is labelled partial. No helper writes a .sigma file to a
+production directory or changes an existing input. The budget is zero SCF calls,
+zero quantum gradients, zero model evaluations and zero conformer searches.
+There is no automatic native continuation, basis sweep or histogram-matching
+stage. Code-only synthetic tests may run before registration and off the Mac;
+actual UD-backed acquisition and replay run on the Mac.
+
+Interpretation: successful replay links the public raw input to the historical
+Mac sigma profile within tolerance. Different geometry with different raw
+charge distribution identifies a joint historical difference, not its causal
+partition. Identical geometry but different raw distributions points to the
+remaining electronic/cavity representation, subject to the provenance checks.
+A coordinate-only comparison cannot prove the equilibrium liquid distribution.
+No observed difference selects a conformer or establishes that UD is the truth.
+
+P43 is E reporting. Add a dated provenance update without rewriting historical
+numbers or failed registrations. Clarify that prior raw-input absence described
+the Mac holdings, and that P29's raw area-profile tail is not a pre-averaging
+raw-segment tail. Record the public notice's empirical conformation-selection
+history without asserting which glycol was revised or alleging ThermoML leakage.
+Retain the statement that Z0x was not fitted to ThermoML, with no broader claim
+that every upstream input was wholly uncalibrated. The physical glycol mechanism
+remains unresolved. The frozen profile version and all earlier numerical
+acceptance/rejection decisions remain unchanged.
```
<!-- END PATCH REG10 -->

Local verification record

This record describes local software and patch checks. It is not a native or Mac UD acceptance record.

```json
{
  "base": "4dc898521f6c49355e442be78f1e2570d3686aee",
  "base_scope": "Partial local worktree, exact verified README and GLYCOL_STATUS blobs, not a full clone",
  "checks": [
    {
      "patch": "P41",
      "independent_apply_check": true,
      "files": [
        "scripts/r10_sources.py"
      ]
    },
    {
      "patch": "P42",
      "independent_apply_check": true,
      "files": [
        "scripts/r10_replay.py",
        "scripts/r10_selftest.py"
      ]
    },
    {
      "patch": "P43",
      "independent_apply_check": true,
      "files": [
        "README.md",
        "docs/astra/round7/GLYCOL_STATUS.md",
        "docs/astra/round10/PROVENANCE_STATUS.md"
      ]
    },
    {
      "patch": "REG10",
      "independent_apply_check": true,
      "files": [
        "docs/astra/round10/REGISTRATION_PROPOSED.md"
      ]
    }
  ],
  "combined_apply_check": true,
  "syntax_checks": true,
  "CLI_help_and_catalog": true,
  "portable_tests": {
    "SCF_calls": 0,
    "UD_comparisons": 0,
    "errors": 0,
    "failures": 0,
    "passed": true,
    "scope": "Portable synthetic checks only",
    "tests": 20
  },
  "SCF_calls": 0,
  "actual_UD_comparisons": 0,
  "production_changes": 0,
  "patch_sha256": {
    "P41": "c938116326269dcb91e2060eb9e9b493db51578e9ff1c7b2d6dc123f9ffe7891",
    "P42": "4118cbb5938ca9bd0ecaae2f7c9a7527a21077898b1ec215ff4508614c90323e",
    "P43": "c1e816ce1ef1bd5722cbceaaa4eef4be0525568bf8800dfd389b64d179e2f99a",
    "REG10": "2f15a5b7c4c732822fb6e3268a35edddbcb6ea4d242c3c139df1b53a23eab375"
  },
  "reporting_scope_check": true
}
```

Closing decision

Recover and replay the known public inputs first. P35 is open only for this zero-QC provenance comparison; its physical mechanism remains unresolved. There is no new numerical-gradient budget and no change to the 630+6 profile version.
