# Z-COSMO round 17: final manuscript audit and model-development closeout

Reference: `Victor-Liang-ChE/zcosmo`, `main = 35ab60046f3f4a7566d8eeee6b13172a6d0becc2`.
The original manuscript is Git blob `edf2eae2b30fb97b8934c4e86c81a09685e8704d`.
This review follows the round-17 prompt and the completed R16/P58a record. It proposes reporting edits
only. No scientific source, parameter table, profile, historical scorecard or RESULTS file is changed.
The dated registration text below is a proposal until the maintainer adopts it.

| Rank | ID / class | Target and mechanism | Acceptance and exact check | Saving / effort |
|---:|---|---|---|---|
| 1 | P60 / E editorial | `manuscript/draft.md`, new `manuscript/supplement.md`, dated README append. Insert the complete LV1 failure, repair source/interpretation errors, and separate infrastructure from the principal results. | Preserve all four existing numerical tables verbatim. Verify the original manuscript blob, reviewed output hashes and the LV1 negative-result text with P61/H17. | Zero scientific computation. Resolves the main submission issue without another experiment. Moderate editing effort. |
| 2 | P61 / E evidence accounting | `CLAIMS.json`, `REFERENCES.md`, `scripts/r17_audit.py`. Index all original numerical paragraphs; distinguish verified public quantities from narrative-only or unrecovered precision. | Exact public-source hashes, claim-location/text checks and immutable historical tables. A software pass deliberately leaves `submission_ready=false` while editorial evidence is outstanding. | Zero model calls. Avoids rescoring to replace missing historical provenance. Moderate source-audit effort. |
| 3 | P62 / E public-data rendering | `scripts/r17_figures.py`. Isolate Figures 2 and 3 from the old script's private-prediction imports. Render stored quantities only into a fresh directory. | Pinned public inputs, fixed comparator/denominator checks and PNG smoke tests. No pixel-equivalence claim. | No prediction loading or metric calculation. Two public-data figures become independently renderable; no numerical solver acceleration claimed. Low effort. |
| Shared | H17 / E software tests; REG17 / E reporting record | New portable tests and an explicit zero-science closeout registration. | Commands below; 36 final portable tests pass. | No new scientific experiment or acceptance decision. |

The ranking reflects submission value and effort, not an invented probability of scientific improvement.
There is no A proposal and no new model in this round. The development campaign should close with its
recorded limitations. The remaining work is editorial provenance, not a reopened VLE optimization plan.

## Decision and the principal findings

Finalize the paper around the original performance tradeoff, followed by P54's conditional attribution
and the negative LV1 follow-up. R16 does not leave an optional dispersion screen pending: it completed
that screen once and failed its registered criteria. VLE AAD changed from 13.78% to 13.13%, with a paired
95% interval of [-1.72, +0.13] percentage points and a one-sided upper bound of +0.02. IDAC MAE increased
from 0.840 to 0.875, and HE MAE from 618.6 to 632.9 J/mol. The original result reports an unrounded HE
increase of 14.2 J/mol; replacing it by the 14.3 obtained from independently rounded endpoints would be
an editorial error. The failed screen is a useful finding, not a missing successful result. [R16]

P54 remains the strongest later explanation of this implemented Z0x-to-2010 VLE difference: dispersion
receives 2.24 percentage points, about 67% of the 3.35-point gap on the 963 exposed observations.
The E/H/D cube is an error attribution under fixed interventions. It does not assign physical energy
fractions, establish a universal error source, or justify selecting the best fitted corner as a model.
The unchanged shared profiles and effective area have zero contribution to that endpoint difference,
not certified zero error in nature. R14's epsilon substitution and P54's ES contribution are overlapping
counterfactuals and must not be added. [R14] [R15]

The audit identifies substantive corrections beyond adding R16. The abstract's IDAC “matches” and the
text's “ties” should become “no resolved difference”; the original test was not an equivalence test.
The methods overstate the input filters: untestable VLE series are retained, IDAC comparisons use a
rounded-temperature bin and median rule, and a missing critical temperature is not a rejection.
The first historical table combines property-specific main7 columns, a test_both column and separately
reported early LLE/HANNA values. It must not be described as one eight-model common-subset scorecard.
The proposed patch makes these distinctions without rerunning a filter or changing a data row. [PR] [M7] [BOTH] [SCOPE]

Several exact early inferential statements remain source-qualified rather than certified. The public
progress log corroborates the reported LLE advantage and describes it as significant, but I did not
recover its precise original bootstrap artifact. The main7 file does not supply the separately reported
historical HANNA row. The manuscript's detailed old conformer and non-aqueous association intervals also
require the already-produced private artifacts. The patch preserves these historical numbers with an
explicit Supplement S0/S2/S3 qualification; it does not manufacture a source, substitute a new common
subset or infer a paired interval from rounded point estimates. These are submission evidence gaps,
not authorization to make new model or bootstrap calls. [PG] [M7] [W1]

## Exact numerical and interpretation corrections

| Original location at the pinned base | Finding | Exact disposition |
|---|---|---|
| Abstract, lines 18-24 | “Split frozen before any model was run” is broader than the initial registration record. | State that the initial recipe/split preceded Z0 predictions and that later changes preceded their own output, with prior exposure retained. |
| Abstract and §3.1, lines 26-41 and 170-175 | Non-rejection is called a tie or match. | Use “no resolved difference.” Do not imply equivalence or noninferiority, and do not use an unresolved comparison as evidence that the models are equal. |
| §2.1, lines 72-89 | Claimed subcritical status and quality-filter wording exceed the implemented rules. | Document 250 <= T <= 450 K, P <= 500 kPa where supplied, known-Tc VLE rejection at T >= 0.98 Tc, untestable VLE retention, and the IDAC `round(T/2)*2` median rule. Frozen data are unchanged. |
| §2.2, lines 91-95 | Project inventory and publication database count can be confused. | Preserve the project's reported 2,259 entries; distinguish Bell et al.'s 2,261-compound distribution. Neither count is substituted for the other. |
| §2.4 and §3.1 | A single all-model/common-row description is applied too widely. | Name the property-specific masks and LLE detection/endpoint denominators. The historical table is preserved as a composite summary, with a source-status footnote. |
| §3.1, Z0 IDAC interval | Draft [-0.17, +0.08] is not the named main7 interval; it agrees with another historical source's rounding. | Use main7 [-0.170, +0.069]. Preserve the old string and provenance distinction in S0. |
| §3.1, Z0 test_both interval | Draft [-0.54, -0.22] does not reproduce the cited main7/test_both output. | Use the stored [-0.552, -0.229], with 55 observations in 12 systems. |
| §3.1, Z0 VLE interval | Draft [+6.6, +14.5] matches the older generic scorecard, not main7. | Use the unfiltered main7 interval [+6.76, +14.61] percentage points. Do not choose a different interval because it is more favorable. |
| §3.1, Z0x intervals | Rounded draft values are broadly compatible, but the source should be explicit. | State main7 IDAC [-0.153, +0.065] and VLE [+3.19, +7.96]. |
| §3.1, early LLE/HANNA precision | Exact bootstrap/endpoint artifacts were not recovered in this public-file audit. | Keep reported point values with qualification; preserve precise old claims in S0 pending the original artifact. Do not assert a new equivalence result with HANNA. |
| §3.2 | A small number of outliers is inferred from aggregate means/medians. | Say the displayed error distribution is skewed; those summaries do not determine the count of observations carrying the mean. |
| §3.3 | “CCSD(T)/CBS” can be read as a fully converged reference, and +/- is unlabeled. | Identify the composite CCSD(T)/aug-cc-pVDZ plus MP2 correction estimate. Label the HB table's +/- as across-dimer sample SD, not CI. |
| §3.3-3.4 | Selected sensitivities are described as broad perturbation bounds; old London VLE improvement is unqualified. | Restrict the bounds to the tested variants. Give the old ablation's 3,070 IDAC / 33,303 VLE scope and note that its London VLE interval includes zero. |
| §3.4 family claims | “Alkenes” abbreviates the combined alkene/alkyne class, and “most accurate” is too broad. | Use the exact class with counts: 146 alkene/alkyne-aromatic, 456 alkane-alcohol, 38 alcohol-alkane and 27 alcohol-aromatic observations. Report descriptive comparisons only. |
| §3.5 | Failed registration is conflated with a resolved overall IDAC difference; aqueous explanation is too categorical. | Give the stored overall interval [-0.035, +0.400]. Retain the failed registration; describe the aqueous mechanism as an interpretation rather than a unique proven cause. |
| §3.6-3.7 | Infrastructure and numerical provenance interrupt the central comparison. | Move detailed chronology to S1/S2; keep one paragraph each on open-profile scope and the glycol finding. Original-gradient convergence, failed P32 and P35 closeout remain explicit. |
| §3.7 detailed old ensemble statistics | The public progress record supports 50 molecules, 244 conformers and median approximately 0.01; it does not expose the full precision quoted in the draft. | Retain the detailed values in S2 as legacy reported values pending `_queue/done/26_conformer_eval.sh.log`, rather than certify them without that artifact. |
| §3.9 | Force-path equivalence can be mistaken for exact finite-step sampling or validated chemical potentials. | Move timing details to S3 and restrict equivalence to its measured energy/force checks. Preserve failures and source-version distinctions. |
| §3.10 | The CRC oracle can be overread as perfect epsilon at all temperatures. | Preserve the exact reference-covered, 298.15 K substitution and exposed 963-row scope. It is neither a production model nor a rigorous attainable headroom bound. |
| §3.11, P54 | Existing -4.23 versus -4.47 distinction is correct. | Retain it: -4.23 is the displayed one-at-a-time bias difference; -4.47 is a Shapley allocation. Do not “repair” one into the other. |
| §3.11 and discussion | LV1 is still prospective or absent. | Add the entire completed failed screen, fixed counts, bounds, P58a scope and no-adoption outcome. Replace the optional-screen language with closeout. |
| Data availability and README | Later evidence stops at R13/R15 in some inventories. | Update the manuscript/supplement inventory through R16 and append a dated README closeout. Preserve every earlier README byte. The old full-workflow reproduction commands are not R17 authorization. |
| Reference 9 | The 2006, 51, 1504 “series” placeholder does not identify the verified Part 1 paper. | Cite Frenkel et al., JCED 2003, 48(1), 2-13, DOI 10.1021/je025645o. Record the remaining reference checks explicitly. |

The source-dependent intervals above are transcriptions of existing outputs, not a new bootstrap.
The E classification applies to editorial/accounting changes; it does not relabel any prior physical
approximation or imply that the old and revised prose are semantically equivalent where the old claim
was wrong. All original numerical tables remain byte-for-byte in the revised manuscript. [M7] [BOTH] [GENERIC] [ABL] [SENS] [FAMILY] [W1] [R15] [R16]

## LV1 belongs next to the factorial

The proposed §3.11 addition is fully supplied in P60. It includes the following fixed record rather than
just a favorable VLE point estimate. [R16]

| Quantity | Recorded result | Interpretation to preserve |
|---|---|---|
| VLE, 963 observations / 100 systems | 13.78% -> 13.13%; change -0.65 pp; 95% CI [-1.72, +0.13]; one-sided upper +0.02 | Fails the registered improvement bound. Still above the same-row 2010 value of 10.44%. |
| IDAC, 828 / 204 | 0.840 -> 0.875; +0.035; CI [+0.008, +0.067] | Worsens on this exposed collection and fails the guard. |
| HE, 8,573 / 348 | 618.6 -> 632.9 J/mol; reported +14.2; CI [+4.6, +25.1] | Worsens; preserve the unrounded-result difference. |
| HE sign, 8,316 observations | 0.838 -> 0.834 | Non-worsening fails. |
| LLE recall, 101 positives | 0.842 -> 0.842; one-sided lower 0 | This guard passes. |
| LLE balanced accuracy | 0.893 -> 0.897; lower -0.008 | The favorable point estimate does not pass the non-worsening bound. |
| LLE false-positive rate, 128 negatives | 0.055 -> 0.047; upper +0.016 | The favorable point estimate does not pass the bound. |

The finite query counts sum to `963 + 828 + 17,146 + 129,596 + 23,168 = 171,701`. HE includes the two
stored temperature-side requests per observation. This addition is accounting of the published run,
not new thermodynamic scoring. The original 51 pure-composition HE exclusions occurred before model
calls under P58a. All VLE anchors replayed exactly and no LLE grid job was unresolved. Those facts make
the screen complete; they do not make its failed accuracy gates pass. The 2,219-second runtime is a
recorded execution cost, not a controlled new speed-up estimate. [R16]

The discussion states the resulting end point directly: the VLE gap remains open, LV1 is not adopted,
and this project's model-development campaign is closed. P54 localizes a consequential implemented
approximation without identifying one uniquely wrong microscopic assumption. The LV1 failure does not
prove that every scalar-descriptor closure or future theory is impossible. That logical qualification
is not a proposal to continue the campaign.

## Submission structure

Use the scientific result, rather than the succession of assistant rounds, as the reading order.
The preferred main-paper order is the initial no-new-regression recipe and scope, the historical IDAC
comparison, the historical LLE detection finding, and the VLE/HE deficit. The temporal collection follows
as a separately exposed historical check. Then present the same-row P54 cube, its conditional Shapley
allocation and the complete LV1 negative follow-up. The epsilon oracle is a short precursor to that
argument, not the principal unresolved lever. [PR] [M7] [TEMP] [R14] [R15] [R16]

| Submission location | Material |
|---|---|
| Main results opening | Historical IDAC: no resolved difference from 2010, not equivalence. Report LLE detection point advantage with its historical source and the provenance check for exact early inferential precision. Follow immediately with larger VLE/HE errors. |
| Main historical comparison table | Retain current numbers and explicitly identify the composite, property-specific sources. HANNA remains a data-driven reference with unresolved row-level training overlap. |
| Main explanatory result | Current §3.11 P54 and LV1. Keep the fixed 963 observations, all corners, nonadditivity of overlapping interventions and the unfavorable screen. |
| Main short scope paragraphs | One paragraph on exploratory open profiles and numerical stationarity limits; one on the 142-row glycol explanation and its tetraEG exception. |
| Supplement S0 | Source-version corrections and early historical precision whose original artifacts remain to be recovered. |
| Supplement S1/S2 | Detailed R2-R9 numerical/optimization history, endpoint/input comparisons and R10-R13 lineage/coordinate/glycol record. |
| Supplement S3/S4 | Association failures, simulation timing/force scope, dispatch repair and exposure/amendment chronology. |
| Final limitations/availability | Inherited empirical conventions, pure Psat inputs, exposed collections, failed variants, private UD artifacts and the absence of a validated production geometry or replacement contact rule. |

The review patch keeps the familiar subsection numbers, so the requested LV1 text is in §3.11 and the
historical cross-references stay traceable. The table gives the typesetting reading order; renumbering
is an editorial operation after the claim checks, not a new result. Long infrastructure paragraphs
have already been moved into the supplied supplement, with source-qualified summaries in the main
text. The original long numerical record is retained rather than silently discarded.

“Fit-free” should be expanded wherever it could be misread: Z0/Z0x interaction constants were not newly
regressed to ThermoML. The common effective area and combinatorial conventions remain inherited,
Z0s made a training-selected discrete choice, Z1 is fitted, UD geometry provenance includes empirical
selection history, and VLE uses correlative experimental pure-component vapor pressures. A physically
motivated rule chosen after an exposed failure can still be preregistered before its own output, but
that does not turn the old collection back into an untouched test. [PR] [R10] [R14] [R15] [R16]

## Reproducibility and references

All five captioned PNGs are committed. That establishes existence, not visual correctness or recovery
of their exact historical masks. The old plotting script loads private prediction files before its
public-only sections. It also computes metrics and can omit missing model inputs. Therefore the R17
commands below do not run that script. P62 reads only the public per-dimer/class-mean CSVs and stored
main7 JSON values for Figures 2 and 3. Figures 1, 4 and 5 may be exported from the immutable Git objects;
that is not a claim to regenerate them from public raw predictions. [FIG]

The complete reference and figure inventory follows in the appended audit, and is also applied as
`docs/astra/round17/REFERENCES.md`. Most bibliographic metadata has been checked against primary publisher
records. Herington's original title/page range, direct D4 publisher retrieval and the contents of the
2014 COSMO-SAC-dsp corrigendum remain open. MACE/HANNA weight files and executed software/data versions
need their existing provenance citations. No missing version is guessed. The old precise LLE and some
conformer/association statistics need their existing artifacts before they can be labeled fully audited.

These unresolved items are finite editorial gates. Do not rerun simulations, evaluate an alternative
model or make a fresh bootstrap to fill them. The mechanical audit emits `submission_ready=false`
even when all checks pass, because document integrity cannot establish unobserved historical evidence.

## What was executed

The manuscript and README were reconstructed and independently verified against their Git blob hashes
before editing. The complete required registration/results record was inspected through the repository
connector, with additional relevant scorecards and source definitions. Publisher metadata checks were
performed for the bibliography. The final 36 portable tests exercise document/claim integrity, immutable
source checks, independent-rounding compatibility, path resolution and synthetic public-figure data.
The tests include raster smoke tests with synthetic quantities. No model is imported or evaluated.

Independent and combined patch checks, extraction from this report, Python compilation and shell syntax
checks are reported in the verification block below. This is a verified source-subset reconstruction,
not a full clone. The full 43-source Git-object audit and actual public-data redraw require the complete
checkout and were not run end to end here. Original figure pixels and private prediction arrays were
not inspected. No private UD input, new QC, new activity request, new experimental score or new bootstrap
was used. No remote file or repository was modified.

## Exact application and reporting commands

Save the report outside the checkout. Start at the exact reference commit. These commands apply only
the reviewed manuscript/reporting changes; they do not run the historical reproduction pipeline.

```bash
set -euo pipefail
BASE=35ab60046f3f4a7566d8eeee6b13172a6d0becc2
test "$(git rev-parse HEAD)" = "$BASE"
: "${R17_REPORT:?Set R17_REPORT to the downloaded ZCOSMO_ROUND17_REPORT.md}"
export R17_REPORT
export R17_PATCHES="$(mktemp -d)"
python - <<'PY'
import os,re
from pathlib import Path
text=Path(os.environ['R17_REPORT']).read_text()
items=re.findall(r'<!-- BEGIN PATCH (\w+) -->\s*```diff\n(.*?)\n```\s*<!-- END PATCH \1 -->',text,re.S)
assert [name for name,_ in items]==['P60','P61','P62','H17','REG17']
root=Path(os.environ['R17_PATCHES'])
for name,body in items:
    (root/(name+'.patch')).write_text(body+'\n')
PY
for p in P60 P61 P62 H17 REG17; do
  git apply --check "$R17_PATCHES/$p.patch"
done
cat "$R17_PATCHES/P60.patch" "$R17_PATCHES/P61.patch" \
  "$R17_PATCHES/P62.patch" "$R17_PATCHES/H17.patch" \
  "$R17_PATCHES/REG17.patch" > "$R17_PATCHES/all.patch"
git apply --check "$R17_PATCHES/all.patch"
git apply "$R17_PATCHES/all.patch"
unset R17_TEST_ORIGINAL
PYTHONPATH=scripts python scripts/r17_selftest.py
python -m py_compile scripts/r17_audit.py scripts/r17_figures.py scripts/r17_selftest.py
```

Adoption appends the new reporting record without changing any historical registration. The old
PREREGISTRATION prefix and reviewed README append have explicit integrity checks.

```bash
set -euo pipefail
umask 077
printf '\nRound 17 adopted at %s\n\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" >> PREREGISTRATION.md
cat docs/astra/round17/REGISTRATION_PROPOSED.md >> PREREGISTRATION.md
git add README.md manuscript/draft.md manuscript/supplement.md \
  docs/astra/round17/CLAIMS.json docs/astra/round17/REFERENCES.md \
  docs/astra/round17/REGISTRATION_PROPOSED.md scripts/r17_audit.py \
  scripts/r17_figures.py scripts/r17_selftest.py PREREGISTRATION.md
git commit -m "Register R17 manuscript-only audit and model-development closeout"
export R17_OUT="$(mktemp -d "${TMPDIR:-/tmp}/zcosmo-r17.XXXXXX")"
/usr/bin/time -p env PYTHONPATH=scripts python scripts/r17_audit.py \
  --out "$R17_OUT/audit" > "$R17_OUT/audit.log" 2>&1
# A mechanical pass reports submission_ready=false until the listed evidence gaps are resolved.
```

The source-hash audit intentionally stops on a mismatch. Do not delete a hash check or substitute an
unrelated scorecard. It can be repeated into a new output directory because it creates no new score.
The three plotting inputs must be present from the complete public checkout; missing files are not
replaced with guessed values or private prediction calls.

```bash
set -euo pipefail
: "${R17_OUT:?Run the reporting setup block first}"
/usr/bin/time -p env PYTHONPATH=scripts python scripts/r17_figures.py \
  --out "$R17_OUT/public-figures" > "$R17_OUT/public-figures.log" 2>&1
```

For the other figures, the following is an exact archived-image export, not a regenerated metric or
new plot. Every written image is compared with its pinned blob before it is saved. No existing output
file can be overwritten.

```bash
set -euo pipefail
: "${R17_OUT:?Run the reporting setup block first}"
export R17_OUT
python - <<'PY'
import hashlib,json,os,subprocess
from pathlib import Path
base='35ab60046f3f4a7566d8eeee6b13172a6d0becc2'
out=Path(os.environ['R17_OUT']).resolve()/'archived-images'
out.mkdir(mode=0o700,exist_ok=False)
ledger=json.loads(Path('docs/astra/round17/CLAIMS.json').read_text())
for item in ledger['figures']:
    name=Path(item['path']).name
    if name.startswith(('fig2_','fig3_')):
        continue
    data=subprocess.check_output(['git','show',base+':'+item['path']])
    digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert digest==item['blob'] and len(data)==item['bytes'], name
    with (out/name).open('xb') as f:
        f.write(data)
print('Exported existing Figures 1, 4 and 5. No metrics recomputed.')
PY
```

The commands contain no invocation of `evaluate`, `metrics`, a profile generator, a queue runner or a
cloud workflow. They also make no claim that a public redraw alone resolves the private figure-source
questions.

## Complete original-manuscript claim index

The ledger contains 68 digit-bearing blocks, including 12 section-number blocks. The 56 non-structural entries below cover every original numerical paragraph, entire numerical table and bibliography block. Index coverage is mechanical; each disposition states how far the underlying evidence was actually verified. The exact original text hashes and public-source blob inventory are in P61. Line references are to the 520-line original at the pinned base, not the revised layout.

| ID / original lines | Claim group | Audit disposition | Required handling |
|---|---|---|---|
| C01 / 3-3 | Original 2026-09-24 / revision 2026-10-08 dates | editorial | Preserve; R17 is an editorial revision, not a new experimental date. |
| C02 / 7-16 | 17 dimers, theory/QC interaction constants and inherited empirical inputs | scope correction | Keep no-new-ThermoML-regression claim; do not imply every convention or upstream input is first-principles. |
| C03 / 18-24 | 9184 files; IDAC3438 VLE46127 LLE7158 HE27366; split chronology | scope correction | Counts agree with session 1. Say split frozen before Z0 predictions, not before every model run. Preserve later exposure. |
| C04 / 26-41 | Abstract IDAC/LLE/VLE means, HB counts, epsilon oracle and P54 shares | mixed source precision | Use no resolved IDAC difference. Cite LLE as contemporaneous reported advantage, not independently recovered exact bootstrap. Add LV1 negative result; limit P54 to963rows. |
| C06 / 57-60 | HANNA about824000 DDB observations | publisher checked | Publisher specifies824481; rounded claim valid. Do not infer per-row overlap or general superiority from this local comparison. |
| C08 / 72-78 | 25heavy atoms;250-450K;500kPa;2K/.2IDAC;Herington;5cloudpoints | scope correction | Document binned median IDAC filter, retained untestable VLE and known-Tc-only rejection at0.98Tc; boundaries inclusive. |
| C09 / 80-89 | 20%,seed20260924,11923files,2017-2019,reference years2010/2014/2016 | scope correction | Preserve historical dates. Table-fit dates do not prove all upstream data independent; old collections are exposed. |
| C10 / 91-95 | NIST implementation2e-9 on400pairs;localUD2259 vs publication2261 | public record | Distinguish reported code gate and project inventory from Bell publication count; no gate re-executed. |
| C11 / 97-109 | aeff7.25 q079.53 r066.69 z10; cES12226/8197;17dimer recipe | verified source | Preserve constants; state inherited conventions. Rounded cES values follow documented formulas, not independently fitted numbers. |
| C12 / 111-116 | one-center C6,d^-6,z/2=5 and pure-reference cancellation | scope correction | Retain declared modeling assumptions. Pure Psat does not automatically double count an excess mixing term. |
| C13 / 118-127 | f=(eps-1)/(eps+1/2),P6 analyticinterior,P28opt-in,6Z0svariants | public record | Preserve P6/P28 numerical distinction; Z0s is a training-selected choice and historical endpoints are not overwritten. |
| C14 / 129-136 | 336negative states;1000systembootstraps andpaired95% | scope correction | Common masks are property-specific; LLE has distinct detection/endpoint denominators; CI0 is not equivalence. |
| C16 / 145-147 | Five figure filenames | asset metadata checked | All five files exist in manuscript/figures; metadata only, not a pixel/data audit. Safe regeneration only2/3 from public aggregates. |
| C18 / 151-153 | main7 vs composite table provenance | scope correction | Label first table composite: main7 property entries, test_both column, historical BA summary and separate HANNA row. |
| C19 / 155-164 | All cells in historical8-model table | partially verified | Preserve exact table. Seven-model IDAC/VLE/HE cells and both-unseen cells match after rounding. BA precision/HANNA row require original artifacts, explicitly qualified inS0. |
| C20 / 166-168 | 708/163;55/12;9432;101/128;HANNA762 | partially verified | Add confirmed6311HE count; do not assign a762IDAC count to HANNA VLE/HE. Exact early detection/HANNA arrays not recovered. |
| C21 / 170-175 | Z0IDAC[-.17,+.08],both[-.54,-.22],VLE[6.6,14.5];LLE/HANNApreciseCIs | mismatch and unverified precision | Use main7[-.170,+.069],test_both[-.552,-.229],VLE[6.76,14.61]. Preserve old strings inS0. Exact early LLE/HANNA CIs remain unverified; do not call CI0 a tie. |
| C23 / 179-188 | Every temporal8-model table cell | verified source | Preserve verbatim; correct rounded values on this separate common subset. |
| C24 / 190-193 | 254/54IDAC;7722VLE;2058HE;Z0xVLECI[1.2,3.3] | scope correction | Counts and CIrounding agree. Means/medians alone do not count how many large misses dominate. |
| C26 / 197-201 | HB5/7/5;5712+/-538,5988+/-1032,5611+/-1833;4014/3016/932 | verified source | Preserve exact table; +/- values are sampleSD across dimers, notCI. |
| C27 / 203-206 | 5CCSDT/CBS estimates;.33-.85mean.59about15%;.05IDAC/1ppHBsensitivity | scope correction | Name composite CBSestimate, not exactbasislimit. Perturbation bounds describe testedvariants only. |
| C28 / 208-217 | Old ablation+.03/+.13/+.17IDAC,+6VLE;family.18/.40/1.05,.66/1.04,3.7/3.4 | scope correction | Old all-data startingdsp notZ0x. LondonVLEpointdecrease unresolved. Familylabelalkene/alkyne andcounts146/456/38/27, not universal mostaccurate. |
| C29 / 219-230 | Z0w.97/.80;27.4/15.2VLE;.094FP;.90BA;aqueous5-7;nonaq.67/.88;entropy-121/-87 | partially verified | Main uses verified .969/.800[-.035,+.400]. Move detailed historical claims toS3; exact posthoc CIs[-.29,-.09],[-.17,+.04] require private existing artifact. Aqueous diagnosis not proof of uniquecause. |
| C30 / 232-239 | v125/2302;.153/.15,water1.14,TEG.84;MAE.79/.74;gap136,218/72and6scores | public record | Move toS1. Target2302 is historical occurrence denominator, not proof allfinite; gatecompatibility not equivalence;136computed not218uniquecompounds. |
| C31 / 241-249 | v2.1493 margin.0007;630+6;R2-R9;P32failure | public record | Main oneparagraph and S1detail. Keeporiginalgradient stationarityscope, Aoptimizerstateclassification and failedgate. |
| C32 / 251-257 | 50molecules244confsavg4.9;medians.009/.011,p90<.09,CI[.00,.01]/[-.35,.32],weight60% | private precision unverified | Publiclog supports50/244and~.01; detailedqueuefile absent from audit. Retain preciselegacyclaims inS2withpendingartifactlabel; no assertionofequivalence. |
| C33 / 259-263 | 12lineages;EG/DEG/TEGtailgeometry;tetraexception;no fullprofilelabel | public record | Move detail toS2; orderedcross includesH/orientation, not independently identified liquidconformation. |
| C34 / 265-273 | 142;1.813/.702/.419;1.111;80%gap61%own;139/3;13%;.283 | public record | Preserve exact meaning and endpoint. .283 is differenceofMAEs notmeanpredictiondifference oruniversalmethodeffect. |
| C35 / 275-279 | R10-R13empiricalUDhistory,P35closeout,630+6 | public record | Preserve scope; database-level conformation revision does not identify individualglycolselection. |
| C37 / 283-290 | w2.9-2.1solvation,.902/.800CI.04-.18BA.887,13%donors | public record | Numerics supportedrecord; failedcriterion stands. Approximate85%liquid reference not newly independentlyvalidated; later temporal is nowexposed. |
| C39 / 294-312 | MACE.37ns/day648;force2-4e-6;8.9~24x;TF32.003;HMR2.3-183;21liquidstates;w3errors | public record | Move infrastructuretoS3. Exactforcepath checks notequilibrium sampling/chemicalpotential validation; distinct w3temporaldenominator; physicaldiagnosis remainshypothesis. |
| C40 / 314-319 | P6dispatch,P28endpoint,P55restoration | public record | Retain historicalassociationpredictions unaffected; repairno newscore and no exactassociationendpoint. |
| C42 / 323-327 | P51742/248validplus5matchedinvalid,298.15K | public record | Registeredaggregatewithheld correctly; do notsubstitute matched-onlydescriptives. |
| C43 / 329-336 | P52963/100;2889;13.78/13.07/10.44;equal13.90/13.19/10.65;.72/21%/3.35;559/404 | public record | All agree atrecordprecision. Independentlyroundedendpoints may differ from unrounded difference. Fixed298epsilon notfullε(T). |
| C44 / 338-341 | P52notfitfree;main7different14.15/8.62 | public record | Preserve diagnosticandnoheadroombound labels; noportfolioMDauthorization. |
| C46 / 345-350 | 963/100;8EHDcorners;2dummyfactors | public record | Preserve retrospective intervention definition; dummyzerosonlybetween specifiedendpoints. |
| C47 / 352-361 | All eight P54cornerAAD/bias/equal-systemvalues | verified source | Preserve exact table. |
| C48 / 363-369 | 2.24/67%,.88/26%,.23/7%;3.35gap;HD+.95ED-.43 | public record | Preserve conditionalShapleyerrorallocation, not causalenergypercent. |
| C49 / 371-375 | 2.02AAD;onefactorbias-4.23versusShapley-4.47 | public record | Currentclarificationcorrect; retain. No roundingexplanation forconflatingdifferentstatistics. |
| C50 / 377-381 | 7704finite1926anchors3e-14efficiency722s | public record | Preserve measuredaccounting; portabletestqualificationnotallMacsummarypass. |
| C51 / 383-386 | 21%eps andESshareoverlap;630+6 | public record | Preserve nonadditivity,noadoption;appendLV1failure tosame3.11section. |
| C53 / 390-393 | Z0xVLEworse main7/temporal | scope correction | Preserveproperty-dependentusefulness; avoidgeneralcompetitiveorzeroempiricismclaim. |
| C54 / 395-401 | P54leadingZ0xexplanation,R14smalllever | public record | Keepconditionalclosureattribution; notuniquedoublecountingoronegeometrycause. |
| C55 / 403-411 | C6positive Londonnonnegative; prospectivealternative language | reasoning and stale status | Keepalreadyreportedalgebra restriction, notpositiverow-errorclaim. ReplaceprospectiveLV1text bycomplete failedscreen. |
| C56 / 421-428 | P54papercentrepiece,optionalfutureLV1screen | stale status | Screenalreadyranandfailed. Close modeldevelopment; editorialsourcechecks only; no proposedvariant. |
| C58 / 432-436 | Z0/Z0xnofitting,Z0strainchoice,Z1fitted | public record | Preserve andaddsoftware/weightversioncitations pending. EmpiricalPsat andprofileconventions remain. |
| C59 / 438-441 | 2017-2019exposure,bootstrapgenerality | public record | Preserveexposure;R16CIs exposedwithincollectionresampling notrestoredholdout. |
| C60 / 443-447 | 630+6,correctedgradient/ensemble/certification limits | public record | Preserve limits andclosedstatus. |
| C61 / 451-455 | R10-R15privateartifacts | asset scope | Extend toR16; publiccheckoutnotfullprivate-table reproduction. No redistributionornewscoring. |
| C62 / 459-461 | Fig1762/177parityandHANNAoverlap | asset metadata checked | Imageexists butrows/masknotpixelverified. Existingprivatepredictionfilesneededfororiginalplot. No regenerationusingmodelcalls. |
| C63 / 463-464 | Fig217dimers/meansvsfitted | asset metadata checked | Imageexists. Newpublic-only helpercanrender fromcommittedCSV without touchingpredictioncode; notbyteidenticalclaim. |
| C64 / 466-469 | Fig3tradeofffrommain7pointestimates | asset metadata checked | Imageexists. Newhelperreads storedmeans only; nobootstraporrescoring; eachaxisownpropertymask. |
| C65 / 471-472 | Fig4LLErecall/FPR | asset metadata checked | Imageexists,privatearraysrequired. OneoperatingpointpermodelnotfullROC;exportarchivedbytes onlyinR17. |
| C66 / 474-475 | Fig5familycellsn>=10 | asset metadata checked | Imageexists. CommittedfamilyCSVmayhaveothercommonmask; donotrebrandalternativeaggregaterenderasoriginalregeneration. |
| C67 / 479-487 | S1-S7sourceinventorythroughR15 | asset scope | UpdatethroughR16,addactualsupplementandclaimledger; detailedprivateassetsnotrepresentedaspresentpublicdata. |
| C68 / 491-520 | Every reference1-17year/volume/pageandDOI | reference audit | Bibliographyauditall17. Correct9to2003Part1;name12series;verifiedDOIs,flag10and13directpublishercheck,5corrigendumcontent andsoftwarecitations. |

## Reference and figure inventory supplied with the patch

### Bibliographic identity and remaining verification

This is an editorial audit, not a new literature-selected model. Bibliographic identity and the contents
of a paper are different checks. A publisher metadata record can establish a DOI and page range without
validating every scientific claim attributed to the paper. The original reference numbers are retained.
Issue-publication years are used instead of later digitization dates or earlier online dates.

| Reference | Metadata established | Primary location | Remaining issue / manuscript action |
|---|---|---|---|
| 1, Klamt | J. Phys. Chem. 1995, 99(7), 2224-2235 | https://doi.org/10.1021/j100007a062 | Expand title and pages. Do not use the website's 2002 digitization date as the publication year. |
| 2, Lin and Sandler | Ind. Eng. Chem. Res. 2002, 41(5), 899-913 | https://doi.org/10.1021/ie001047w | Add DOI and the related 2004 correction, 43(5), 1322, https://doi.org/10.1021/ie0308689. No inference that current 2010 code is affected without checking its equations. |
| 3, Mullins et al. | Ind. Eng. Chem. Res. 2006, 45(12), 4389-4415 | https://doi.org/10.1021/ie060370h | Add full range and DOI; distinguish this database publication from the project's UD inventory. |
| 4, Hsieh et al. | Fluid Phase Equilib. 2010, 297(1), 90-97 | https://doi.org/10.1016/j.fluid.2010.06.011 | Add exact DOI/range; model constants remain those of the pinned implementation. |
| 5, Hsieh et al. | Fluid Phase Equilib. 2014, 367, 109-116 | https://doi.org/10.1016/j.fluid.2014.01.032 | A corrigendum exists at 384, 14-15, DOI 10.1016/j.fluid.2014.10.019. Its author-institution record is verified; original publisher text and implications remain outstanding. |
| 6, Bell et al. | J. Chem. Theory Comput. 2020, 16(4), 2635-2646 | https://pubs.acs.org/doi/abs/10.1021/acs.jctc.9b01016 | Complete citation verified at ACS. Its 2,261-compound distribution count is distinct from the project's reported 2,259-entry inventory. |
| 7, Gmehling et al. | Ind. Eng. Chem. Res. 1993, 32(1), 178-193 | https://doi.org/10.1021/ie00013a024 | Cite the actual 2016 parameter update as well; the 1993 paper alone does not identify the DOUFIP2016 software table. |
| 8, Hoffmann et al. | Nat. Commun. 2026, 17, 3485; published 14 April 2026 | https://www.nature.com/articles/s41467-026-71430-y | Publisher gives 824,481 data points. The project still needs its deployed weight/version receipt and row-overlap scope; publication metadata does not recover those. |
| 9, Frenkel et al. | Part 1 is J. Chem. Eng. Data 2003, 48(1), 2-13 | https://pubs.acs.org/doi/abs/10.1021/je025645o | Replace the draft's unspecific 2006, 51, 1504 series placeholder with this identified Part 1 article. Online December 2002 does not change the 2003 issue citation. |
| 10, Herington | The draft identifies J. Inst. Petrol. 1951, 37, 457 | No original publisher record recovered | Keep explicitly provisional. Title and complete range need a primary archival record; do not manufacture a DOI. A later paper citing these coordinates is not the original source. |
| 11, Onsager | J. Am. Chem. Soc. 1936, 58(8), 1486-1493 | https://doi.org/10.1021/ja01299a050 | Complete DOI and range; the implementation's convention needs its own code citation. |
| 12, Wertheim I-IV | 1984, 35, 19-34 and 35-47; 1986, 42, 459-476 and 477-492 | https://doi.org/10.1007/BF01017362 ; https://doi.org/10.1007/BF01017363 ; https://doi.org/10.1007/BF01127721 ; https://doi.org/10.1007/BF01127722 | Replace the incomplete parenthetical series reference with explicit I-IV identities. These papers do not validate the project's particular site mapping or inversion. |
| 13, Caldeweyher et al. | J. Chem. Phys. 2019, 150(15), 154122, DOI 10.1063/1.5090222 | https://www.cambridge.org/engage/chemrxiv/article-details/60c74060f96a006646286291 | Author preprint/version-of-record link supports identity. Direct AIP publisher retrieval was unsuccessful, so direct publisher verification stays open. Do not cite a preprint DOI as the final journal DOI. |
| 14, Bannwarth et al. | J. Chem. Theory Comput. 2019, 15(3), 1652-1671 | https://doi.org/10.1021/acs.jctc.8b01176 | Complete GFN2-xTB title, DOI and range; actual tblite/geometry versions are separate provenance. |
| 15, Grimme | Chem. Eur. J. 2012, 18(32), 9955-9964 | https://doi.org/10.1002/chem.201200497 | Complete range and DOI. Do not treat model quasi-RRHO thermochemistry as a measured liquid entropy. |
| 16, Sun et al. | J. Chem. Phys. 2020, 153(2), 024109 | https://doi.org/10.1063/5.0006074 | Complete citation. A package paper does not specify the pinned PySCF 2.14.0 source used in later diagnostics. |
| 17, Boys and Bernardi | Mol. Phys. 1970, 19(4), 553-566 | https://doi.org/10.1080/00268977000101561 | Use the original DOI and publication year, not a later reprint or digitization. |
| Added 18, Constantinescu and Gmehling | J. Chem. Eng. Data 2016, 61(8), 2738-2748 | https://doi.org/10.1021/acs.jced.6b00136 | Identify the 2016 update; also record the installed thermo parameter-table revision from existing execution receipts. |

The corrigendum author record is
https://scholars.ncu.edu.tw/zh/publications/corrigendum-to-considering-the-dispersive-interactions-in-the-cos/ .
No correction's uninspected contents are asserted here. The complete reference audit uses publisher
records where accessible and labels the remaining author-record-only or unrecovered identities.

The submission archive should also identify the already-used MACE-OFF23 weight file and its corresponding
primary publication, along with exact model/software/data versions for PySCF, D4, GFN2-xTB/tblite, RDKit,
pyberny, thermo/ugropy, HANNA and the ThermoML snapshot. Method citations for the chosen basis/functional
and numerical integration belong in the supplement. These items must be taken from existing execution
receipts; R17 does not invent a package version, generate new chemistry or certify an absent model hash.
This is a finite editorial checklist, not a proposal to acquire a new validation dataset.

### Figure inventory

All five captioned PNG files exist under manuscript/figures at the pinned R17 base. The GitHub tree and
file metadata were checked, not their pixels or private underlying arrays. There is no caption-only
figure among those five. No additional P54 or LV1 figure is asserted to exist.

| Figure | Committed file | Git blob | Bytes | What can be done without scoring |
|---|---|---|---:|---|
| 1 | fig1_idac_parity_test.png | 72659886f5d3b451cf00adfe536a3715b1d6553a | 164834 | Export existing image. Original regeneration needs the exact historical private prediction CSVs and mask; no regenerated MAE in R17. |
| 2 | fig2_hbond_constants.png | c22a980ff1e3266e8865b84a2bac9c9deebe6367 | 36908 | Render from committed per-dimer and stored class-mean CSVs using r17_figures.py. |
| 3 | fig3_tradeoff.png | 62205ae989a86687abf91d99bdd9b1010d7cb46a | 45885 | Render stored main7 IDAC and VLE means using r17_figures.py, with each axis's own denominator. |
| 4 | fig4_lle_detection.png | 03560344877b0867a97b806b7014ebb477a7d8b5 | 44921 | Export existing image. Original private positive/negative arrays are needed for provenance; one operating point per model is not a full ROC curve. |
| 5 | fig5_error_map.png | 78e50e66d2dc842667e0ed5aa2a9e42a42a7fece | 78089 | Export existing image. Committed family aggregates are not certified to have the original figure's common mask, so do not relabel an alternative rendering as an exact regeneration. |

The old scripts/make_figures.py reads private prediction files at module import before the public-only
figure sections. It can also recompute metrics and silently skip absent model inputs. It is therefore
not the zero-score regeneration command for R17. The isolated helper reads only three fixed public
files and writes Figures 2 and 3 into a fresh external directory. It promises data-source fidelity,
not pixel identity with the original plotting environment. Exporting Figures 1, 4 and 5 from the Git
object preserves their exact original bytes but does not replace their pending source-array audit.

## Source inventory

Repository citations refer to the pinned commit. The connector-reported blob hashes are retained below; this local review independently reconstructed and hashed the original manuscript and README. It did not locally materialize or rehash every listed file. The full-checkout command performs the latter checks without reading private predictions.

| Public source | Git blob |
|---|---|
| [PREREGISTRATION.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/PREREGISTRATION.md) | `c1b84665223940e3042c4d16c8ce3006479ead3d` |
| [PROGRESS.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/PROGRESS.md) | `216bb364f496e7846c8a450643768e521eb4b546` |
| [README.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/README.md) | `263447947ec5b953b1e5d5e9259aaef22cb6fb62` |
| [src/zcosmo/scope.py](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/src/zcosmo/scope.py) | `894d89cee8e33bb194f60e54469302236b77df5b` |
| [src/zcosmo/cosmosac.py](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/src/zcosmo/cosmosac.py) | `c226a668b7b9dba9e7400cda180fafd8faa700f3` |
| [src/zcosmo/z0x.py](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/src/zcosmo/z0x.py) | `c558d4e95db9b78f3b57d6a103a293e21feeb9af` |
| [results/scorecard_test_main7.json](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/results/scorecard_test_main7.json) | `aee303792afcdff48e90aa74d074802a3bb7596b` |
| [results/scorecard_test_main7.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/results/scorecard_test_main7.md) | `f180ea4d506619e010f2ba0a673965d4aa22163e` |
| [results/scorecard_test_both_main7.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/results/scorecard_test_both_main7.md) | `c3e3bfd5df6e32cdec5c6e8c1b21a5b952ea0ce7` |
| [results/scorecard_test_main6.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/results/scorecard_test_main6.md) | `9d5ae19484dc21844e3b14360d156b7bc99b350b` |
| [results/scorecard_test.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/results/scorecard_test.md) | `bce8eed067c3eb436b9d3343199790f50bb13305` |
| [results/scorecard_temporal_ext.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/results/scorecard_temporal_ext.md) | `c8895658373b0c1e582a63b3256d1f116dd56620` |
| [results/scorecard_temporal_test_ext.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/results/scorecard_temporal_test_ext.md) | `076dd6365ab13c7ac32f7ab74aa0c4abc2b2f65d` |
| [results/scorecard_all_ablation.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/results/scorecard_all_ablation.md) | `37f3a51e5d94eca2f5447740ed3ec959e22d5dd6` |
| [results/scorecard_test_sensitivity.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/results/scorecard_test_sensitivity.md) | `e283a7a59ebd6454a3a7404ba5c63074a6557710` |
| [results/scorecard_all_gap_exploratory.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/results/scorecard_all_gap_exploratory.md) | `7b2637440112e1e5290e1026bd9d3fd87b5822d8` |
| [results/scorecard_test_z0w.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/results/scorecard_test_z0w.md) | `720b2bb8e407b38f778debe9e93e0448e10f9c6e` |
| [results/error_map_idac_all_long.csv](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/results/error_map_idac_all_long.csv) | `b1caa4827ebe9df0f98e3f8006a6d5c27b8857aa` |
| [results/qc/ccsdt_check.csv](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/results/qc/ccsdt_check.csv) | `10aeaafb0ccb2ef0a8d6c17d00de4c3a9c926135` |
| [results/qc/hb_constants_per_dimer.csv](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/results/qc/hb_constants_per_dimer.csv) | `bd249aaf7ad01e5fd70a7357766c6db6e5cf1307` |
| [results/qc/hb_constants_by_class.csv](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/results/qc/hb_constants_by_class.csv) | `fe225ee279fd80fc599c871955011370ddafb5e0` |
| [results/qc/assoc_thermo.csv](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/results/qc/assoc_thermo.csv) | `a7044b9c0023d28d92f8aee7af1225c4f2f21b37` |
| [scripts/make_figures.py](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/scripts/make_figures.py) | `7238311999c7ede74ea35acfdff2544710a05836` |
| [docs/astra/round2/RESULTS.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round2/RESULTS.md) | `6da753d4b62210817abf98b25da7e1e12458ee45` |
| [docs/astra/round3/RESULTS.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round3/RESULTS.md) | `c6de1f0a15d47cd596c56f5de00928f2a3238b1d` |
| [docs/astra/round4/RESULTS.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round4/RESULTS.md) | `428e5b4e0ce8801a5f55ac16d5a1a9a9217d400a` |
| [docs/astra/round5/RESULTS.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round5/RESULTS.md) | `88d669c4c8abc6269e55f3609d7ff390e7f6fc5c` |
| [docs/astra/round6/RESULTS.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round6/RESULTS.md) | `4dfc953f8cff9846f1810cb01ef82719569a9a8e` |
| [docs/astra/round7/RESULTS.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round7/RESULTS.md) | `ef78bceea953b5bfc4167aa28ea366e58ffe5213` |
| [docs/astra/round8/RESULTS.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round8/RESULTS.md) | `d34dc87a3d0724740df4c344bb481ff4ee861583` |
| [docs/astra/round9/RESULTS.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round9/RESULTS.md) | `00f6d3b81c4da803cefbe5da9024b8d4ba453f07` |
| [docs/astra/round10/RESULTS.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round10/RESULTS.md) | `0656f37159bbeb6f7a18477f91b513e46f3c3e0c` |
| [docs/astra/round11/RESULTS.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round11/RESULTS.md) | `458210e730623727b6e94881511459bd48c187aa` |
| [docs/astra/round12/RESULTS.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round12/RESULTS.md) | `c036e8e24aa45a03aed0485664b3a26cd842c17f` |
| [docs/astra/round13/RESULTS.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round13/RESULTS.md) | `8d5885b430e3dda0d44db49d50a5303f2499fa50` |
| [docs/astra/round14/RESULTS.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round14/RESULTS.md) | `90b8a880d4c887f3dce09d67592c5383bf02f295` |
| [docs/astra/round15/RESULTS.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round15/RESULTS.md) | `dd2eeb1fa384f320e338341cd72bd5479a69ba9c` |
| [docs/astra/round16/RESULTS.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round16/RESULTS.md) | `328926b9c40209fa4bcac371575fd0794697ad3b` |
| [manuscript/figures/fig1_idac_parity_test.png](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/manuscript/figures/fig1_idac_parity_test.png) | `72659886f5d3b451cf00adfe536a3715b1d6553a` |
| [manuscript/figures/fig2_hbond_constants.png](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/manuscript/figures/fig2_hbond_constants.png) | `c22a980ff1e3266e8865b84a2bac9c9deebe6367` |
| [manuscript/figures/fig3_tradeoff.png](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/manuscript/figures/fig3_tradeoff.png) | `62205ae989a86687abf91d99bdd9b1010d7cb46a` |
| [manuscript/figures/fig4_lle_detection.png](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/manuscript/figures/fig4_lle_detection.png) | `03560344877b0867a97b806b7014ebb477a7d8b5` |
| [manuscript/figures/fig5_error_map.png](https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/manuscript/figures/fig5_error_map.png) | `78e50e66d2dc842667e0ed5aa2a9e42a42a7fece` |

[PR]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/PREREGISTRATION.md
[PG]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/PROGRESS.md
[M7]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/results/scorecard_test_main7.json
[BOTH]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/results/scorecard_test_both_main7.md
[SCOPE]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/src/zcosmo/scope.py
[GENERIC]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/results/scorecard_test.md
[ABL]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/results/scorecard_all_ablation.md
[SENS]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/results/scorecard_test_sensitivity.md
[FAMILY]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/results/error_map_idac_all_long.csv
[W1]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/results/scorecard_test_z0w.md
[TEMP]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/results/scorecard_temporal_ext.md
[FIG]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/scripts/make_figures.py
[R2]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round2/RESULTS.md
[R3]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round3/RESULTS.md
[R4]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round4/RESULTS.md
[R5]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round5/RESULTS.md
[R6]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round6/RESULTS.md
[R7]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round7/RESULTS.md
[R8]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round8/RESULTS.md
[R9]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round9/RESULTS.md
[R10]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round10/RESULTS.md
[R11]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round11/RESULTS.md
[R12]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round12/RESULTS.md
[R13]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round13/RESULTS.md
[R14]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round14/RESULTS.md
[R15]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round15/RESULTS.md
[R16]: https://github.com/Victor-Liang-ChE/zcosmo/blob/35ab60046f3f4a7566d8eeee6b13172a6d0becc2/docs/astra/round16/RESULTS.md

## Verification record

Completed here: all five independent patch-application checks and the combined check passed. The patches were then extracted from this report, applied to a fresh Git-blob-verified source subset, and the nine resulting files matched the reviewed versions. All 36 portable tests passed in the extracted checkout. Python compilation, four Bash-block syntax checks, two embedded-Python parse checks and `git diff --check` also passed. All four original manuscript numerical tables remain verbatim, and the original README bytes remain an unchanged prefix of its dated append.

These are software and editorial checks. The tests use synthetic reporting inputs where full repository assets are required. The local checkout is a verified source-subset reconstruction, not a full clone. The complete 43-source audit command was not run end-to-end against a full checkout, and the actual public-data figure regeneration was not executed. Figure-rendering tests used synthetic inputs; the committed figures were checked through repository metadata, not a pixel-by-pixel visual audit. Those remaining commands are supplied above without being represented as completed.

No new quantum calculation, activity-model query, simulation, experimental scoring, bootstrap or remote repository modification was performed. No private UD data was accessed or redistributed. Passing these mechanical checks does not resolve the explicitly listed historical-source and bibliography gaps, so the reporting tool deliberately does not certify submission readiness.

The extractable patch SHA256 values are:

| Patch | SHA256 |
|---|---|
| P60 | `93eb91bb5fc12c9f4070b358b6e50169e0260bb0a4a6268bc0ee20308d442159` |
| P61 | `15e389f68c48f3294f453fa1f3119c19ce7488a6b19c780072b4784741bad4d1` |
| P62 | `75d00662eb8fc02e7a851d46ffa14286c2410c7979035a381250f4781e424ce6` |
| H17 | `44d096e63559b8f07740ce79452fa25d02cb1bbafa6079b3c3eda05ac07e2660` |
| REG17 | `d48debf363a7b64e889cd53942b9c3a090c4a711854419b84df14a47d4918ad5` |

## Extractable patches

Each patch has an independent `git apply --check` target at the reference main. H17 execution depends on P60-P62, and the adoption block includes REG17. There are no modifications under `src/`, `results/`, or older `docs/astra/round*/RESULTS.md` paths. The registration proposal is appended only by the explicit maintainer command.

<!-- BEGIN PATCH P60 -->
```diff
diff --git a/README.md b/README.md
index 2634479..61e12e4 100644
--- a/README.md
+++ b/README.md
@@ -75,3 +75,14 @@ or a held-out accuracy improvement. No crossed profile or conformer-selection
 rule is adopted. The 630 primary plus six flagged profiles remain frozen.
 P35's present explanatory campaign is closed with these findings; its liquid-state
 mechanism remains unresolved. The separate numerical-gradient campaign stays closed.
+
+R17 manuscript closeout (2026-10-08): the subsequent [R15 factorial](docs/astra/round15/RESULTS.md)
+attributes 2.24 percentage points, about 67% of the Z0x-to-2010 VLE gap on 963 exposed observations,
+to the implemented London closure. The [R16 LV1 screen](docs/astra/round16/RESULTS.md) failed its
+registered tradeoff gates and is not adopted. The VLE gap remains unresolved and the model-development
+campaign is closed for this project. The manuscript and supplement retain the unfavorable result,
+actual source-specific denominators and numerical qualifications. "Fit-free" here means no new
+ThermoML regression of the interaction constants, not absence of all empirical upstream inputs.
+The reproduction commands above describe the historical full workflow; they are not authorization to
+rerun it during R17. Only the zero-model reporting commands in the R17 report are proposed now.
+Existing bibliography and artifact checks remain editorial submission tasks, not a new research budget.
diff --git a/manuscript/draft.md b/manuscript/draft.md
index edf2eae..e5a68b5 100644
--- a/manuscript/draft.md
+++ b/manuscript/draft.md
@@ -4,94 +4,93 @@ Victor Liang (original draft 2026-09-24; evidence and scope updated 2026-10-08)
 
 ## Abstract
 
-COSMO-SAC replaces binary-specific regression with molecular surface profiles and shared interaction
-parameters. We ask how much accuracy is retained when its electrostatic and hydrogen-bond coefficients
-and dispersion prescription are supplied by theory or quantum chemistry without regression to ThermoML. In the resulting model, Z0, the electrostatic misfit coefficient follows from Klamt's
-estimate in the conductor limit, the three hydrogen-bond constants come from 17 counterpoise-corrected
-B3LYP-D4/def2-TZVP dimer energies, and dispersion enters through a London term built from D4 molecular
-C6 coefficients and polarizabilities. Z0 and Z0x do not regress their interaction constants to the
-ThermoML benchmark. They retain the standard effective area and combinatorial normalization constants,
-along with inherited profile-processing conventions. UD reference geometries have documented empirical
-selection history, and VLE uses experimental pure-component vapor-pressure correlations. The claim is
-therefore absence of new benchmark regression, not absence of every empirical upstream input.
-
-We score Z0, two dielectric-screening refinements (Z0e, Z0x), COSMO-SAC 2010, COSMO-SAC-dsp and
-modified UNIFAC (Dortmund) on a benchmark built from 9,184 ThermoML files (3,438 infinite-dilution
-activity coefficients, 46,127 VLE, 7,158 LLE and 27,366 excess-enthalpy points), with a molecule-level
-held-out split frozen before any model was run, and on a temporal set of 2017 to 2019 publications that
-provide an additional historical collection. HANNA is included as a data-driven reference, with possible
-training overlap. The original split was frozen prospectively, but later model development examined both
-collections repeatedly; subsequent explanatory analyses do not constitute new untouched validation.
-
-On held-out molecules Z0 matches COSMO-SAC 2010 for infinite-dilution activity coefficients (MAE in
-ln gamma 0.76 vs 0.82, difference not significant) and detects liquid-liquid demixing more reliably than
-both COSMO-SAC and UNIFAC (balanced accuracy 0.90 vs 0.84 and 0.81, significant). It is clearly worse for
-bubble pressures (AAD 18.8% vs 8.6%) and on the temporal set. The DFT-derived hydrogen-bond constants are
-nearly identical across the three COSMO-SAC classes (about 5,700 kcal A^4 mol^-1 e^-2), whereas the fitted
-constants span 4,014 to 932. Earlier one-term ablations identify the electrostatic prescription as an
-important sensitivity. Composition-dependent screening in Z0x reduces the historical VLE AAD to 14.2%.
-A later retrospective diagnostic on a separate 963-row subset changes AAD from 13.78% to 13.07% when
-experimental pure-liquid permittivities replace the stored estimates, versus 10.44% for COSMO-SAC 2010.
-A registered same-row factorial subsequently assigns 2.24 percentage points, about 67% of the
-Z0x-to-2010 AAD gap, to replacing the London term with the reference's absence of explicit dispersion.
-The electrostatic closure contributes 26% and the hydrogen-bond constants 7% under this allocation.
-These exposed counterfactuals identify an implemented approximation to examine, not a transferable
-physical error fraction or permission to delete a term because its removal improves the benchmark. HANNA, where its
-training data reach, is far more accurate than every physics-based model, but it does not detect demixing
-more reliably than Z0 on held-out molecules.
+COSMO-SAC predicts liquid-mixture properties from molecular surface profiles and shared interaction
+parameters. We benchmark specified replacements of its interaction constants without regression to
+ThermoML, while retaining inherited surface-processing and combinatorial conventions and
+experimental pure-component vapor-pressure correlations. The initial Z0 recipe was registered before
+its predictions; later variants were registered before their own evaluations, with prior data
+exposure acknowledged. The historical compound-test comparison found no resolved IDAC difference
+between Z0 and COSMO-SAC 2010 (MAE in ln gamma 0.76 versus 0.82), rather than establishing
+statistical equivalence. The contemporaneous project record reports higher LLE detection balanced
+accuracy, 0.90 versus 0.84 for COSMO-SAC 2010 and 0.81 for modified UNIFAC. Z0 had larger VLE
+pressure and excess-enthalpy errors. Z0x's composition-dependent electrostatic prescription reduced
+VLE AAD from 18.8% to 14.2%, versus 8.6% for COSMO-SAC 2010, on the historical main7 VLE subset. Z0x
+also remained worse on the historical temporal collection.
+
+On a separate, already-exposed panel of 963 observations in 100 systems, a registered factorial
+attributed 2.24 percentage points, approximately 67% of the Z0x-to-2010 pressure-error gap, to the
+implemented London dispersion closure. Electrostatic and hydrogen-bond replacements contributed 26%
+and 7% under the same allocation. These are conditional error attributions, not fractions of
+intermolecular physics. The one subsequently registered dispersion alternative, LV1, failed its
+exposed tradeoff screen: VLE AAD changed from 13.78% to 13.13% without passing its uncertainty gate,
+and IDAC and excess-enthalpy errors increased. No fitted factorial corner, term deletion, or LV1
+variant was adopted. The completed study establishes useful but property-dependent performance
+without new benchmark regression and identifies a consequential contact-model approximation. The VLE
+gap remains unresolved, and this project's development campaign is closed. Open-profile and
+numerical-provenance findings are reported separately from the UD-backed results.
 
 ## 1. Introduction
 
-Process simulators describe liquid mixtures mostly with correlative excess-Gibbs-energy models such as
-NRTL and UNIQUAC, whose binary parameters are regressed from measurements of the same binary. When no
-data exist, engineers fall back on predictive models. Group-contribution methods (modified UNIFAC) need
-group-interaction parameters fitted to large databases and cannot treat groups that were never
-parameterized. COSMO-RS and COSMO-SAC replace groups by the screening-charge distribution of each
-molecule, computed with density functional theory in a conductor, and so apply to any molecule whose
-structure is known. Their interaction model, however, still carries a small set of universal constants
-(an effective contact area, the electrostatic misfit coefficient and its temperature dependence,
-hydrogen-bond strengths and cutoffs, and in later versions dispersion parameters) that are fitted to
-experimental infinite-dilution activity coefficients and phase equilibria. Published variants have refit shared parameters for different electronic-structure recipes. Their
-reported accuracy must therefore be distinguished from that of the present no-new-regression variants.
-
-Data-driven models have meanwhile become very accurate. HANNA, a thermodynamically consistent neural
-network trained on about 824,000 Dortmund Data Bank points, outperforms modified UNIFAC across binary
-VLE, LLE, infinite dilution and excess enthalpy. Where training data are dense, the case for
-physics-based models therefore rests less on accuracy than on transferability and interpretability.
-
-That case is only as strong as the physics is real. If COSMO-SAC's accuracy is carried mainly by its
-fitted constants, it is a compact regression model; if it is carried by the sigma profiles, the constants
-may admit more transferable physical estimates. We test specified replacements of the interaction
-constants and dispersion model, while retaining the common molecular-surface and combinatorial
-conventions. The benchmark and initial metrics were registered before predictions. Subsequent changes
-were registered before their own execution, with prior exposure stated. Ablations identify conditional
-model sensitivities; they do not uniquely identify a missing physical mechanism.
+Process simulators describe liquid mixtures mostly with correlative excess-Gibbs-energy models such
+as NRTL and UNIQUAC, whose binary parameters are regressed from measurements of the same binary.
+When no data exist, engineers fall back on predictive models. Group-contribution methods (modified
+UNIFAC) need group-interaction parameters fitted to large databases and cannot treat groups that
+were never parameterized. COSMO-RS and COSMO-SAC replace groups by the screening-charge distribution
+of each molecule, computed with density functional theory in a conductor. Application still requires
+a supported chemical domain and a successfully generated, consistently processed profile. Their
+interaction model, however, still carries a small set of universal constants (an effective contact
+area, the electrostatic misfit coefficient and its temperature dependence, hydrogen-bond strengths
+and cutoffs, and in later versions dispersion parameters) that are fitted to experimental
+infinite-dilution activity coefficients and phase equilibria. Published variants have refit shared
+parameters for different electronic-structure recipes. Their reported accuracy must therefore be
+distinguished from that of the present no-new-regression variants.
+
+HANNA is a thermodynamically constrained neural model trained on about 824,000 Dortmund Data Bank
+points. Its publisher reports comparisons across binary phase equilibria and excess enthalpy [8].
+The deployed model's training membership has not been matched row by row to this project's ThermoML
+collection, so its results here are a data-driven reference rather than a certified unseen-data
+contest. Transferability beyond the inspected chemical systems remains a separate question.
+
+The present comparison tests specified approximations rather than separating all accuracy into a
+physical part and a fitted part. We test specified replacements of the interaction constants and
+dispersion model, while retaining the common molecular-surface and combinatorial conventions. The
+benchmark and initial metrics were registered before predictions. Subsequent changes were registered
+before their own execution, with prior exposure stated. Ablations identify conditional model
+sensitivities; they do not uniquely identify a missing physical mechanism.
 
 ## 2. Methods
 
 ### 2.1 Data
 ThermoML XML files (MobleyLab mirror of the NIST/TRC archive, publications to mid-2017) were flattened and
 compounds resolved to InChIKeys offline, accepting a match only when the molecular formula agreed.
-Scope: neutral molecules of C, H, N, O, F, Cl, Br, S with at most 25 heavy atoms, 250 to 450 K, pressures
-below 500 kPa, both components subcritical. Quality filters: repeated IDAC measurements within 2 K had to
-agree within 0.2 in ln gamma; VLE series with vapor compositions had to pass the Herington area test; LLE
-systems needed both coexisting branches or at least five cloud points. Every rejection is logged.
-
-Twenty percent of in-scope compounds were held out (seed 20260924, water always in training). Rows with
-one held-out component form `test_one`, with two `test_both`. The split was hashed before any Z-model
-prediction. A temporal set was built later from the complete NIST 2020 archive (11,923 files, standard
-InChIKeys): rows from files absent from the 2017 mirror, i.e. publications from mid-2017 to 2019. These
-postdate the fitting of COSMO-SAC 2010 (2010), COSMO-SAC-dsp (2014) and the UNIFAC parameter table used
-(2016). This is the historical provenance description of those parameter tables, not proof that every
-reference model or upstream input is unexposed to these measurements. HANNA may overlap these data.
-Neither this temporal collection nor the repeatedly examined compound test split is a fresh holdout for
-R10-R15 development. A future validation needs a custodian-led source and duplicate-series audit before
-responses are revealed; relabeling an existing split cannot restore independence.
+The registered chemical scope was neutral C/H/N/O/F/Cl/Br/S molecules with at most 25 heavy atoms,
+250 <= T <= 450 K and P <= 500 kPa where pressure is supplied. In the implementation, the VLE critical-
+temperature filter rejects T >= 0.98 Tc for either component when Tc is known; an unknown Tc does not
+cause rejection. This is not a certificate that every retained observation is subcritical.
+IDAC records are grouped by round(T/2)*2 K and compared with the within-bin median. Values within
+0.2 in ln gamma are retained when at least half the group passes; singleton groups are retained.
+Testable VLE series are screened by the Herington rule, including the registered near-ideal exception.
+Untestable series are retained with an untested label, not described as having passed. LLE selection
+uses the recorded two-branch or at-least-five-cloud-point rule. These source-level qualifications do
+not change the frozen benchmark or its logged exclusions. See src/zcosmo/scope.py and PREREGISTRATION.md.
+
+Twenty percent of in-scope compounds were held out (seed 20260924, water always in training). Rows
+with one held-out component form `test_one`, with two `test_both`. The split was hashed before any
+Z-model prediction. A temporal set was built later from the complete NIST 2020 archive (11,923
+files, standard InChIKeys): rows from files absent from the 2017 mirror, i.e. publications from
+mid-2017 to 2019. These postdate the fitting of COSMO-SAC 2010 (2010), COSMO-SAC-dsp (2014) and the
+UNIFAC parameter table used (2016). This is the historical provenance description of those parameter
+tables, not proof that every reference model or upstream input is unexposed to these measurements.
+HANNA may overlap these data. Neither this temporal collection nor the repeatedly examined compound
+test split is a fresh holdout for R10-R16 development. A future validation needs a custodian-led
+source and duplicate-series audit before responses are revealed; relabeling an existing split cannot
+restore independence.
 
 ### 2.2 Reference models
 COSMO-SAC 2010 and -dsp were reimplemented in NumPy and reproduce the NIST benchmark code (Bell et al.,
-JCTC 2020) to 2e-9 in ln gamma on 400 random pairs. All COSMO models use the same NIST UD sigma
-profiles (DMol3 BP/DNP, 2,259 compounds). Modified UNIFAC (Dortmund) uses the `thermo` package with
+JCTC 2020) to 2e-9 in ln gamma on 400 random pairs. The historical main comparisons use the same project UD sigma
+profile collection (DMol3 BP/DNP; 2,259 entries reported by the project). Bell et al. describe a 2,261-
+compound distributed database [6]; that publication count is not substituted for the project inventory. Modified UNIFAC (Dortmund) uses the `thermo` package with
 automatic group assignment (`ugropy`). HANNA is the published ensemble (Nat. Commun. 2026).
 
 ### 2.3 The Z0 model
@@ -115,42 +114,51 @@ atom pairs between two molecular copies; it is not an intramolecular pair-energy
 factor of one half. The retained D4/MMFF inputs have their own model provenance. No adjustment to
 these inputs or dispersion weight was made to fit the present ThermoML comparison.
 
-Refinements registered after the first results, before their own predictions:
-Z0e scales c_ES by the COSMO dielectric factor f = (eps - 1)/(eps + 1/2) with eps from Onsager's equation
-(GFN2-xTB dipoles, D4 polarizabilities, COSMO volumes), arithmetic mean over the pair. Z0x lets eps follow
-the mixture composition (volume-fraction average) and defines an excess Gibbs energy from which
-chemical potentials are differentiated. This construction is thermodynamically consistent analytically;
-finite-difference implementation errors are assessed separately. The accepted P6 implementation uses an
-analytic interior derivative. P28 supplies the exact pure endpoint of Z0x's same excess-Gibbs model when
-ZC_R6_ENDPOINT=1; the adjacent finite-difference strip remains a distinct numerical approximation.
-Historical tables below retain their original source versions and endpoint conventions. Z0s made one
-train-selected choice among six dielectric variants (optical n^2, harmonic mean) and is labeled accordingly.
+Refinements registered after the first results, before their own predictions: Z0e scales c_ES by the
+COSMO dielectric factor f = (eps - 1)/(eps + 1/2) with eps from Onsager's equation (GFN2-xTB
+dipoles, D4 polarizabilities, COSMO volumes), arithmetic mean over the pair. Z0x lets eps follow the
+mixture composition (volume-fraction average) and defines an excess Gibbs energy from which chemical
+potentials are differentiated. This construction is thermodynamically consistent analytically;
+finite-difference implementation errors are assessed separately. The accepted P6 implementation uses
+an analytic interior derivative. P28 supplies the exact pure endpoint of Z0x's same excess-Gibbs
+model when ZC_R6_ENDPOINT=1; the adjacent finite-difference strip remains a distinct numerical
+approximation. Historical tables below retain their original source versions and endpoint
+conventions. Z0s made one train-selected choice among six dielectric variants (optical n^2, harmonic
+mean) and is labeled accordingly.
 
 ### 2.4 Protocol
 Metrics: MAE in ln gamma_inf; AAD in bubble pressure at measured T and x with the same pure-component
-vapor pressures for every model; MAE of H^E and its sign; for LLE, the share of two-phase systems where a
+vapor pressures for every model; MAE of H^E and sign correctness for |H^E| > 20 J/mol; for LLE, the share of two-phase systems where a
 gap is predicted (recall) and the false-positive rate on 336 systems observed homogeneous over the full
-composition range (from VLE series), combined into a balanced accuracy. All comparisons use rows every
-model can predict. 95% intervals come from 1,000 bootstrap resamples over binary systems; a difference
-counts when the paired interval excludes zero. Pre-registration and every later change are in
+composition range (from VLE series), combined into a balanced accuracy. IDAC, VLE and HE comparisons use their source-specific common
+finite-prediction subsets; those subsets differ by property and comparator list. LLE detection uses
+its specified positive and negative system collections, with endpoint-composition errors reported on
+separate accepted subsets. Historical 95% intervals use 1,000 bootstrap resamples over binary systems;
+an interval spanning zero means no resolved difference, not demonstrated equality or equivalence. Pre-registration and every later change are in
 `PREREGISTRATION.md`.
 
 Later read-only and explanatory rounds retain their own exact observation identities, common inputs
-and requested denominators. Their exposure, failures and amendments are recorded separately. Bootstrap
-intervals from the original tables do not remove later adaptive exposure. LLE split detection and checked
-endpoint compositions have separate denominators; neither is a global phase-equilibrium certificate.
+and requested denominators. Their exposure, failures and amendments are recorded separately.
+Bootstrap intervals from the original tables do not remove later adaptive exposure. LLE split
+detection and checked endpoint compositions have separate denominators; neither is a global
+phase-equilibrium certificate.
 
 ## 3. Results
 
-Figures: `figures/fig1_idac_parity_test.png` (parity, held-out molecules), `figures/fig2_hbond_constants.png`,
-`figures/fig3_tradeoff.png` (IDAC vs VLE error), `figures/fig4_lle_detection.png`,
-`figures/fig5_error_map.png` (Z0x minus COSMO-SAC error by chemical family).
+Figures: `figures/fig1_idac_parity_test.png` (parity, held-out molecules),
+`figures/fig2_hbond_constants.png`, `figures/fig3_tradeoff.png` (IDAC vs VLE error),
+`figures/fig4_lle_detection.png`, `figures/fig5_error_map.png` (Z0x minus COSMO-SAC error by
+chemical family).
 
 ### 3.1 Historical compound-test results
 
-These are the original main7 comparisons, preserved rather than regenerated with later code. See
-`results/scorecard_test_main7.md` and its source-specific common subsets. Later explanatory scores must
-not be subtracted from these values when their observation sets or numerical versions differ.
+The leading historical findings are the unresolved IDAC difference from COSMO-SAC 2010, the reported
+LLE detection advantage, and larger VLE/HE errors. The following historical summary is preserved
+rather than rescored. It combines property-specific sources: main7 for the first IDAC, VLE and HE
+columns, main7/test_both for the second IDAC column, and contemporaneous detection summaries for
+balanced accuracy. It is not a single eight-model common-subset calculation. The HANNA row and
+precise early LLE intervals have a separate source-status note in Supplement S0. Later explanatory
+scores must not be subtracted from this table when observations or numerical versions differ.
 
 | Model | IDAC MAE | IDAC, both unseen | VLE AAD P % (median) | H^E MAE J/mol | LLE balanced accuracy |
 |---|---|---|---|---|---|
@@ -163,16 +171,25 @@ not be subtracted from these values when their observation sets or numerical ver
 | Z0x (no new ThermoML parameter regression) | 0.76 | 0.55 | 14.2 (4.5) | 522 | 0.90 |
 | HANNA (trained on DDB, reference) | 0.24* | 0.24* | 7.1 (2.1)* | 70* | 0.88 |
 
-IDAC: 708 points in 163 systems (both unseen: 55 points, 12 systems). VLE: 9,432 points. LLE: 101
-two-phase and 128 homogeneous test systems. *HANNA values are on the slightly larger common subset
-without Z0s (762 IDAC points); HANNA has very likely seen these systems in training.
-
-Key intervals: Z0 minus COSMO-SAC 2010 IDAC MAE [-0.17, +0.08] (tie); both unseen [-0.54, -0.22] (Z0
-better, small sample); LLE balanced accuracy Z0 minus COSMO-SAC [+0.02, +0.11], Z0 minus UNIFAC
-[+0.04, +0.14]; VLE AAD Z0 minus COSMO-SAC [+6.6, +14.5] points. Z0x keeps the IDAC tie ([-0.15, +0.07])
-and the LLE advantage over COSMO-SAC ([+0.02, +0.11]) and UNIFAC ([+0.03, +0.13]) while cutting the VLE
-deficit to [+3.2, +8.0] points. On LLE detection Z0 and Z0x tie HANNA on the test split
-(Z0x minus HANNA [-0.03, +0.07]); HANNA's binodal compositions are far more accurate (0.05 vs 0.18).
+The main7 counts are 708 IDAC observations in 163 systems, 55 in 12 systems for test_both, 9,432 VLE
+observations, and 6,311 HE observations. The historical LLE summary concerns 101 positive and 128
+negative test systems. The original draft assigned 762 IDAC observations to the separately reported
+HANNA row. Its precise historical VLE/HE common subsets and the underlying early detection/bootstrap
+artifact were not recovered in this public-file audit. These entries are retained as historical
+reported values, with their provenance qualification in Supplement S0, not independently reproduced
+results.
+
+On the named main7 source, the Z0-minus-COSMO-SAC 2010 IDAC interval is [-0.170, +0.069]; for
+main7/test_both it is [-0.552, -0.229]. The latter concerns only 55 observations in 12 systems. Z0's
+unfiltered main7 VLE AAD interval is [+6.76, +14.61] percentage points. Z0x's corresponding IDAC
+interval is [-0.153, +0.065] and its VLE interval [+3.19, +7.96]. Thus the IDAC difference is
+unresolved, while the pressure deficit is resolved within that historical comparison. Sources are
+the stored main7 JSON/Markdown and test_both main7 Markdown, not new bootstrap calculations. The
+contemporaneous progress record reports a significant LLE detection advantage over COSMO-SAC and
+UNIFAC. The exact early bootstrap output should accompany that inferential claim before submission;
+the unverified precision is not inferred from the rounded balanced-accuracy values. A claimed tie
+with HANNA is not an equivalence result. Supplement S0 preserves the old interval strings and their
+status.
 
 ### 3.2 Temporal set (2017 to 2019 publications)
 
@@ -187,10 +204,11 @@ deficit to [+3.2, +8.0] points. On LLE detection Z0 and Z0x tie HANNA on the tes
 | Z0s | 1.08 (0.41) | 8.9 (4.2) | 394 |
 | HANNA (reference) | 0.11 (0.07) | 5.1 (2.0) | 93 |
 
-254 IDAC points (54 systems), 7,722 VLE points, 2,058 H^E points. In this historical temporal comparison,
-Z0x is significantly worse than COSMO-SAC on VLE (Z0x minus COSMO-SAC 2010:
-[+1.2, +3.3] points) and on mean IDAC error, although their median IDAC error is comparable or lower; the
-mean is carried by a small number of large misses.
+254 IDAC points (54 systems), 7,722 VLE points, 2,058 H^E points. In this historical temporal
+comparison, Z0x is significantly worse than COSMO-SAC on VLE (Z0x minus COSMO-SAC 2010: [+1.2, +3.3]
+points) and on mean IDAC error, although their median IDAC error is comparable or lower; the larger
+mean than median indicates skewed absolute errors; the aggregate table alone does not count how many
+observations account for the mean.
 
 ### 3.3 Hydrogen-bond constants from quantum chemistry
 
@@ -200,154 +218,116 @@ mean is carried by a small number of large misses.
 | OH-OT | 7 | 5,988 +/- 1,032 | 3,016 |
 | OT-OT | 5 | 5,611 +/- 1,833 | 932 |
 
-A CCSD(T)/CBS check (CCSD(T)/aug-cc-pVDZ plus an MP2 aug-cc-pVTZ correction) at the same geometries on five
-dimers shows B3LYP-D4 overbinding by 0.33 to 0.85 kcal/mol (mean 0.59, about 15%). Sensitivity runs show
-that a 15 to 25% change in c_hb, a different segment-pairing closure, or a single universal c_hb for all
-classes moves IDAC MAE by at most 0.05 and VLE AAD by under one point.
-
-### 3.4 Which term carries the error
-Replacing one fitted piece of COSMO-SAC-dsp at a time: theoretical electrostatics costs +0.03 in IDAC MAE
+The +/- entries above are the sample standard deviations across the listed dimers, not confidence
+intervals. A composite CCSD(T)/CBS estimate (CCSD(T)/aug-cc-pVDZ plus an MP2 aug-cc-pVTZ
+correction), not a fully converged CCSD(T) basis-limit calculation, was used at the same geometries
+for five dimers. B3LYP-D4 interactions were more attractive by 0.33 to 0.85 kcal/mol (mean 0.59,
+about 15%). The stored, specific exploratory HB variants changed IDAC MAE by at most about 0.05 and
+VLE AAD by under one percentage point on their own common subsets. This describes the tested
+interventions, not every possible 15-25% perturbation. Sources: results/qc/ccsdt_check.csv,
+results/qc/hb_constants_by_class.csv and results/scorecard_test_sensitivity.md.
+
+### 3.4 Earlier ablations, distinct from the Z0x factorial
+The all-data ablation has 3,070 common IDAC and 33,303 common VLE observations. Replacing one fitted
+piece of COSMO-SAC-dsp at a time: theoretical electrostatics costs +0.03 in IDAC MAE
 (not significant) but +6 points in VLE AAD; DFT hydrogen-bond constants cost +0.13 in IDAC; London
-dispersion costs +0.17 in IDAC and slightly helps VLE. The larger electrostatic coefficients in Z0/Z0e
+dispersion costs +0.17 in IDAC and lowers the VLE AAD point estimate, but its paired VLE interval
+includes zero. These values come from results/scorecard_all_ablation.md. The larger electrostatic coefficients in Z0/Z0e
 favor some dilute-property and demixing results, whereas the smaller optical-screening coefficient in
 Z0s trades those results for lower VLE error. These are conditional one-term sensitivities, not an
-additive partition of the later Z0x-to-2010 gap. By chemical family, Z0 is
-the most accurate model for nonpolar solutes in aromatic solvents (alkenes in aromatics: 0.18 vs 0.40 for
-COSMO-SAC and 1.05 for UNIFAC) and for alkanes in alcohols (0.66 vs 1.04), and fails for self-associating
-solutes in inert solvents (alcohols in alkanes 3.7, in aromatics 3.4).
-
-### 3.5 A first-principles association term (Z0w)
-Z0w replaces the COSMO hydrogen-bond term by Wertheim TPT1 association with site-pair strengths
-Delta_AB = (kT/P0) exp(-dG_AB/RT), where dG_AB is the dimerization free energy from the B3LYP-D4 binding
-energy plus GFN2-xTB quasi-RRHO thermochemistry (registered before any prediction). As registered it fails:
-held-out IDAC MAE 0.97 vs 0.80 for Z0x and VLE AAD 27.4% vs 15.2%, and it predicts false liquid-liquid
-splits in 9.4% of miscible test systems (balanced accuracy 0.90, unchanged, because it finds more real
-splits). The failure is entirely aqueous: organic solutes in water are overpredicted by 5 to 7 in
-ln gamma_inf. Post hoc, on non-aqueous systems only, Z0w is the most accurate physics model (test IDAC MAE
-0.67 vs 0.88 for COSMO-SAC 2010, bootstrap difference [-0.29, -0.09]; vs Z0x [-0.17, +0.04]). The
-diagnosis is the gas-phase entropy in dG: bonding to a larger partner costs more rotational entropy
-(water-acetone -121 J/mol/K vs water-water -87 J/mol/K), which makes cross-association about ten times
-weaker than water self-association and turns water into an unrealistically closed network.
-
-### 3.6 Coverage: open-source profiles for missing compounds
-An open pipeline (PySCF BP86/def2-TZVP, C-PCM conductor limit, xTB geometries, NIST averaging and
-splitting) was checked against the NIST/DMol3 profiles before use. On 25 molecules and 2,302 IDAC rows the
-median change in COSMO-SAC-dsp ln gamma_inf was 0.153, just above the pre-set bar of 0.15 (water 1.14,
-triethylene glycol 0.84), while accuracy against experiment was similar (MAE 0.79 vs 0.74). The profiles
-were therefore not merged into the main benchmark. On the 136 previously uncovered compounds (exploratory,
-218 IDAC points in 72 systems), Z0 and Z0x reach MAE 0.68 and 0.69 against 1.00 for COSMO-SAC 2010,
-0.94 for COSMO-SAC-dsp, 0.55 for UNIFAC (79% coverage) and 0.11 for HANNA.
-
-Later v2 conductor-optimized profiles passed the original median agreement gate at 0.1493, only 0.0007
-below 0.15, and were retained as exploratory rather than an accuracy-equivalent UD replacement. The
-frozen population contains 630 files passing the original Berny predicate and six separately flagged
-S1/S2 files. The R2-R9 numerical review preserves accepted performance changes and rejected trials;
-optimizer-state persistence is not relabeled E after its E gate failed. Omitted XC-grid response and the
-incomplete earlier finite-difference referee limit stationarity claims. The corrected-gradient rollout
-failed P32's compatibility gate, and the TEG energy-gradient mismatch remained unresolved when the
-R8/R9 diagnostic budget closed. There is no accepted blanket re-polish or chain rescue. See
-`docs/astra/round7/RESULTS.md`, `docs/astra/round8/RESULTS.md` and `docs/astra/round9/RESULTS.md`.
-
-### 3.7 Conformer ensembles
-For the 50 most flexible benchmark molecules (4.9 conformers on average, BP86/def2-SVP profiles), replacing
-the lowest-energy conformer by the Boltzmann ensemble changed predictions very little: median
-|d ln gamma_inf| 0.009 (COSMO-SAC-dsp) and 0.011 (Z0x), 90th percentile under 0.09, and no significant change
-in accuracy (IDAC MAE difference [0.00, +0.01]; VLE [-0.35, +0.32] points). The lowest conformer carries
-60% of the weight on average. This establishes a small effect for that finite proposal and weighting
-scheme, not the absence of conformational effects or a validated phase-dependent ensemble.
-
-R10 recovered and replayed all twelve fixed-panel UD raw files to their historical profiles. R11's
-ordered open-method cross attributes the polar-tail gaps for ethylene, diethylene and triethylene glycol
-mainly to stored coordinate inputs, including hydrogen positions and orientation. Tetraethylene glycol
-is an exception: its raw-tail gap was mainly method, and its other tail contrasts were small. No member
-passed the registered whole-profile attribution rule. These statements retain R11's original labels.
-
-R12/P46a then scored exactly 142 already-inspected glycol-solvent observations with original open solutes
-and a common P28 endpoint. Pooled MAE in ln gamma_inf was 1.813 for the original open solvent profiles,
-0.702 for the open method at the recovered UD coordinates, and 0.419 for UD solvent profiles. The
-coordinate-derived substitution removed 1.111, about 80% of the open-to-UD comparator MAE gap and 61% of
-the original open absolute error; 139 rows improved and three worsened. Shape carried essentially all
-of the factorial error reduction. Tetraethylene glycol recovered only 13% of its comparator gap. The
-remaining 0.283 is a conditional difference of MAEs, not a universal method-error estimate. P47 located
-same-geometry method differences toward the acceptor side and the EG/DEG/TEG coordinate differences
-toward the donor-side tail; those partitions are not hydrogen-bond energies or binwise error causes.
-
-This was retrospective explanatory ThermoML scoring. The UD notice reports database-level revisions
-using vapor-pressure predictions without identifying which panel members were revised. The result does
-not establish extended chains as the liquid conformations or adopt a geometry rule. P35 closed after
-R13 with its explanatory finding; the liquid distribution remains unresolved and all 630+6 open files
-remain frozen. See `docs/astra/round10/RESULTS.md` through `docs/astra/round13/RESULTS.md`.
+additive partition of the later Z0x-to-2010 gap. The all-data family table reports MAE 0.18 for Z0
+versus 0.40 for COSMO-SAC 2010 and 1.05 for UNIFAC for alkene/alkyne solutes in aromatic solvents
+(146 observations). For alkanes in alcohols it reports 0.66 versus 1.04 (456 observations).
+Z0 errors are 3.7 for alcohols in alkanes (38 observations) and 3.4 in aromatic solvents (27).
+These are descriptive selected family comparisons, not universal superiority claims or an unseen
+subgroup validation. Source: results/error_map_idac_all_long.csv.
+
+### 3.5 Registered association failure
+
+The registered Z0w association model failed its criteria. Its stored IDAC comparison reports MAE
+0.969 versus 0.800 for Z0x on 762 observations in 177 systems; the paired difference interval
+[-0.035, +0.400] does not establish an overall IDAC difference. The historical VLE and aqueous-error
+records motivated later unsuccessful association changes. The non-aqueous result was post hoc, not a
+new holdout. Supplement S3 retains the historical numerical statements and separates publicly
+verified entries from private-artifact-dependent precision. Sources: results/scorecard_test_z0w.md,
+PROGRESS.md, and PREREGISTRATION.md.
+
+### 3.6 Open-profile and numerical scope
+
+Open profiles are an exploratory alternative input, not an accuracy-equivalent UD replacement. The
+v1 agreement gate failed at median 0.153 against 0.15; v2 passed narrowly at 0.1493 on the original
+25-molecule/2,302-occurrence check. The frozen population remains 630 original-gradient Berny
+profiles plus one selected S1 and five selected S2 files. Later tests resolved omitted grid-response
+errors in specific directions, but failed the P32 compatibility gate and did not resolve every TEG
+gradient question. No corrected-gradient rollout or chain rescue was accepted. The infrastructure
+record, including matched open-versus-UD errors and accepted/rejected changes, is in Supplement S1.
+None of these qualifications changes the UD-backed historical tables in this paper.
+
+### 3.7 Glycol explanation and its limit
+
+The R10-R13 provenance and ordered-cross investigation explains a specific glycol-solvent
+discrepancy. On 142 exposed observations with original open solutes, replacing only the solvent
+input by the open method at the recovered UD coordinates changed MAE from 1.813 to 0.702, versus
+0.419 for UD solvents. The 1.111 reduction is about 80% of the open-to-UD comparator gap and 61% of
+the original open error. Tetraethylene glycol recovered only 13%; R11's whole-profile attribution
+labels remained inconclusive. This establishes neither the liquid conformer distribution nor a
+production geometry rule. P35 is closed and all profiles remain frozen. Supplement S2 contains the
+finite-ensemble qualifications, lineage details and the exact endpoint/denominator record.
 
 ### 3.8 Continuum desolvation of the association term (Z0w2)
 
 Z0w over-weighted aqueous association, so Z0w2 adds the electrostatic continuum desolvation of each
-hydrogen-bonded contact, computed with the same BP86/def2-TZVP C-PCM model as the profiles at the mixture's
-own fit-free permittivity. The correction is +0.9 to +2.1 kcal/mol for O-H...O contacts (0.9 at eps = 2,
-2.1 in the conductor limit), enough to cut water's association constant about 30-fold. It over-corrects.
-On the test split the IDAC MAE rises to 0.902 against 0.800 for Z0x (paired difference +0.04 to +0.18),
-while LLE balanced accuracy stays at 0.887. Only about 13% of water's donor sites remain bonded, far below
-the roughly 85% expected for the liquid. Because the test split has now informed two association variants,
-the next variant (3.9) is judged first on the temporal set.
-
-### 3.9 A first-principles liquid-simulation teacher
-
-The association constants that a continuum or gas-phase dimer calculation cannot supply can be measured
-directly in simulated liquids. We use MACE-OFF23 (small), a machine-learned interatomic potential trained
-only on DFT reference data, as a teacher. Speed was the obstacle: the stock ASE path managed 0.37 ns/day for
-648 water atoms on an NVIDIA L4. Three exact changes remove most of it. The first is NVIDIA's
-cuEquivariance fused tensor-product kernels (forces identical to 2-4e-6 eV/A). The second is batching many
-small boxes per GPU. The third is a lean integrator that feeds the model directly, with a Verlet neighbour
-list whose superset is filtered to the cutoff every step. This is exact because MACE's radial envelope is
-identically zero beyond r_max. Aggregate throughput reaches 8.9 ns/day (about 24x), with every change
-checked against reference forces. Two approximations were rejected by pre-registered gates: TF32 arithmetic
-(force error 3e-3 eV/A) and hydrogen mass repartitioning with 1-2.5 fs steps (energy drift 2.3-183 times the
-0.5 fs reference). Z0w3 inverts TPT1 on hydrogen-bond statistics from NPT simulations of seven liquids at
-three temperatures (PREREGISTRATION.md, session 5b). The teacher is physically reasonable (water 87% bonded,
-1.115 g/cm3; an independent engine gives 86% and 1.10), but Z0w3 fails badly: temporal IDAC MAE 2.19 against
-1.45 for Z0x, aqueous test systems 4.79 against 1.76. The simulated association is strong (water Delta about
-ten times the gas-phase dimer value). Overlap with electrostatic contributions in the COSMO reference is
-a plausible architectural explanation. The explicit COSMO hydrogen-bond constants were already zero in
-Z0w and its descendants, so merely turning that term off is not a new solution. The nitrogen-site
-occupancy mismatch and temperature-fit failures also matter. The failed registrations stand; neither a
-unique double-counting decomposition nor a successful replacement architecture was established.
-
-A later, separate source regression must not be confused with these historical failures. Since P6,
-Z0x's optimized interior dispatch bypassed the association subclasses' _g overrides; enabling P28 could
-do so at pure endpoints as well. Archived Z0w/Z0w2/Z0w3 scores predate that change. P55's separate repair
-restores full-subclass-g finite differences, including the historical one-sided endpoint approximation;
-it does not supply an exact association endpoint or a new association score. Software regression tests
-and any future physical validation are reported separately. No fourth association variant is accepted.
+hydrogen-bonded contact, computed with the same BP86/def2-TZVP C-PCM model as the profiles at the
+mixture's own fit-free permittivity. The correction is +0.9 to +2.1 kcal/mol for O-H...O contacts
+(0.9 at eps = 2, 2.1 in the conductor limit), enough to cut water's association constant about
+30-fold. It over-corrects. On the test split the IDAC MAE rises to 0.902 against 0.800 for Z0x
+(paired difference +0.04 to +0.18), while LLE balanced accuracy stays at 0.887. Only about 13% of
+water's donor sites remain bonded, far below the roughly 85% expected for the liquid. Because the
+test split has now informed two association variants, the next variant (3.9) is judged first on the
+temporal set.
+
+### 3.9 Liquid-simulation association and software provenance
+
+The simulation-informed Z0w3 also failed: its own temporal comparison reports IDAC MAE 2.19 against
+1.45 for Z0x, with large aqueous errors. Those values have different source-specific subsets from
+the main temporal table. Model force-equivalence checks and short liquid-structure controls did not
+establish accurate chemical potentials or a uniquely identified double-counting mechanism. P55
+separately repaired a later association-dispatch regression; archived Z0w-family results predate it
+and remain unchanged. No new association score was run. Supplement S3 contains the historical
+timings and accuracy records, with their precise numerical scope.
 
 ### 3.10 Dielectric ingredient and retrospective VLE oracle
 
-R14/P51 screened 742 stored entries against a pinned public liquid-permittivity compilation using exact
-identity and temperature rules. There were 248 valid matches at 298.15 K, with five additional matched
-entries having invalid stored epsilon. The registered complete aggregate was therefore withheld.
-Descriptive matched-only summaries are not substituted for that withheld aggregate or interpreted as
-validation of the current Onsager approximation.
+R14/P51 screened 742 stored entries against a pinned public liquid-permittivity compilation using
+exact identity and temperature rules. There were 248 valid matches at 298.15 K, with five additional
+matched entries having invalid stored epsilon. The registered complete aggregate was therefore
+withheld. Descriptive matched-only summaries are not substituted for that withheld aggregate or
+interpreted as validation of the current Onsager approximation.
 
 P52, after amendment P52a protecting the exact 630/1/5 profile selection, ran on 963 already-exposed
-observations in 100 binary systems. All 2,889 requests were finite and the historical P6 baseline replay
-matched. With identical UD profiles and frozen pure vapor pressures, row-weighted VLE AAD was 13.78%
-for stored-epsilon Z0x, 13.07% for experimental-epsilon Z0x, and 10.44% for COSMO-SAC 2010. Equal-system
-AAD was 13.90%, 13.19% and 10.65%, respectively. From unrounded outputs, the oracle removed about
-0.72 percentage points, roughly 21% of the 3.35-point comparator gap; independently rounded table
-entries need not subtract to the printed difference. There were 559 improved and 404 worsened rows.
-Experimental epsilon was held at its 298.15 K value throughout, so this was not an epsilon(T) or HE test.
+observations in 100 binary systems. All 2,889 requests were finite and the historical P6 baseline
+replay matched. With identical UD profiles and frozen pure vapor pressures, row-weighted VLE AAD was
+13.78% for stored-epsilon Z0x, 13.07% for experimental-epsilon Z0x, and 10.44% for COSMO-SAC 2010.
+Equal-system AAD was 13.90%, 13.19% and 10.65%, respectively. From unrounded outputs, the oracle
+removed about 0.72 percentage points, roughly 21% of the 3.35-point comparator gap; independently
+rounded table entries need not subtract to the printed difference. There were 559 improved and 404
+worsened rows. Experimental epsilon was held at its 298.15 K value throughout, so this was not an
+epsilon(T) or HE test.
 
 The oracle is an experimental-input, retrospective diagnostic, not a fit-free variant, a rigorous
-headroom bound or a newly held-out score. The old main7 14.15/8.62 comparison uses a different subset.
-R14 does not authorize a portfolio dielectric simulation campaign or identify a transferable local
-contact coefficient. See `docs/astra/round14/RESULTS.md`.
+headroom bound or a newly held-out score. The old main7 14.15/8.62 comparison uses a different
+subset. R14 does not authorize a portfolio dielectric simulation campaign or identify a transferable
+local contact coefficient. See `docs/astra/round14/RESULTS.md`.
 
 ### 3.11 Same-row factorial identifies the London closure as the leading VLE discrepancy
 
 R15/P54 reused exactly P52's 963 exposed observations in 100 binary systems, with the original UD
 profiles and frozen pure-component saturation pressures. Eight distinct E/H/D corners were evaluated
-once, where E replaces the complete Z0x electrostatic closure by the 2010 temperature-dependent rule,
-H replaces the hydrogen-bond constants, and D replaces London by no explicit dispersion, as in 2010.
-The sign mask, stored profiles and effective segment area were shared. Profile convention and
-area therefore contribute zero to this endpoint difference, without being certified physically exact.
+once, where E replaces the complete Z0x electrostatic closure by the 2010 temperature-dependent
+rule, H replaces the hydrogen-bond constants, and D replaces London by no explicit dispersion, as in
+2010. The sign mask, stored profiles and effective segment area were shared. Profile convention and
+area therefore contribute zero to this endpoint difference, without being certified physically
+exact.
 
 | E H D corner | AAD P % | bias % | equal-system AAD % |
 |---|---:|---:|---:|
@@ -360,24 +340,24 @@ area therefore contribute zero to this endpoint difference, without being certif
 | 011 | 11.00 | +1.53 | 11.24 |
 | 111, COSMO-SAC 2010 | 10.44 | -0.02 | 10.65 |
 
-The game value was negative absolute percentage-pressure error. Shapley error reductions were
-2.24 percentage points for dispersion (67%), 0.88 for the electrostatic closure (26%) and 0.23 for
+The game value was negative absolute percentage-pressure error. Shapley error reductions were 2.24
+percentage points for dispersion (67%), 0.88 for the electrostatic closure (26%) and 0.23 for
 hydrogen-bond constants (7%). The gap is 3.35 percentage points in the unrounded output. The H/D
 interaction was +0.95 and the E/D interaction -0.43 percentage points in the baseline-anchored
-inclusion/exclusion decomposition. Hydrogen-bond replacement slightly worsened error on its own;
-its net Shapley benefit arose through interactions. These quantities allocate error under the
-specified interventions and loss function, not intermolecular binding energy or universal causal shares.
+inclusion/exclusion decomposition. Hydrogen-bond replacement slightly worsened error on its own; its
+net Shapley benefit arose through interactions. These quantities allocate error under the specified
+interventions and loss function, not intermolecular binding energy or universal causal shares.
 
 The one-at-a-time London removal reduces AAD by 2.02 percentage points. Its bias change, computed
-from the displayed corner biases, is -2.79 - 1.44 = -4.23 percentage points. The separate -4.47 value
-is the Shapley-allocated dispersion bias contribution, not this one-at-a-time difference. Independently
-rounded AADs explain small arithmetic differences such as 13.78 - 10.44 versus the reported 3.35;
-they do not explain conflating these two bias statistics.
-
-All 7,704 requests were finite. The 1,926 anchor requests reproduced their saved P52 pressures exactly
-before intermediate corners ran, and the Shapley efficiency residual was at most 3e-14 percentage
-points. The run took 722 seconds on the Mac, without quantum calculations or a retry. These are
-execution and accounting checks, not a new held-out accuracy certificate. See
+from the displayed corner biases, is -2.79 - 1.44 = -4.23 percentage points. The separate -4.47
+value is the Shapley-allocated dispersion bias contribution, not this one-at-a-time difference.
+Independently rounded AADs explain small arithmetic differences such as 13.78 - 10.44 versus the
+reported 3.35; they do not explain conflating these two bias statistics.
+
+All 7,704 requests were finite. The 1,926 anchor requests reproduced their saved P52 pressures
+exactly before intermediate corners ran, and the Shapley efficiency residual was at most 3e-14
+percentage points. The run took 722 seconds on the Mac, without quantum calculations or a retry.
+These are execution and accounting checks, not a new held-out accuracy certificate. See
 `docs/astra/round15/RESULTS.md` for the source record and its test-environment qualification.
 
 P54 changes the priority inferred from the earlier conductor-limit Z0 ablation: dispersion is the
@@ -385,136 +365,202 @@ leading contribution to this Z0x-to-2010 comparison. R14's approximately 21% eps
 and P54's ES share overlap and must not be added. Neither the best fitted corner nor removal of
 London is adopted. Every historical model table and the 630+6 open profiles remain unchanged.
 
+#### Registered negative result: LV1
+
+R16/P58 tested exactly one registered A alternative, LV1, a cohesive-density volume regular-solution
+replacement using the same molecular C6, polarizabilities and cavity volumes. The dispersion weight
+remained one and z remained ten. It retained the existing residual and combinatorial model; it was
+not a fitted weight or an adopted deletion of London. The design was motivated by the inspected P54
+result and frozen before LV1 predictions. It was an exposed development screen, not a new holdout.
+
+| Property and fixed collection | Z0x | LV1 | Reported change | Paired uncertainty / registered gate |
+|---|---:|---:|---:|---|
+| VLE AAD %, 963 observations / 100 systems | 13.78 | 13.13 | -0.65 pp | 95% CI [-1.72, +0.13]; one-sided upper +0.02; fail |
+| IDAC MAE, 828 observations / 204 systems | 0.840 | 0.875 | +0.035 | 95% CI [+0.008, +0.067]; fail |
+| HE MAE J/mol, 8,573 observations / 348 systems | 618.6 | 632.9 | +14.2 | 95% CI [+4.6, +25.1]; fail |
+| HE sign correct, 8,316 observations | 0.838 | 0.834 | -0.004 | Non-worsening gate fails |
+| LLE recall, 101 positive systems | 0.842 | 0.842 | 0 | One-sided lower 0; pass |
+| LLE balanced accuracy | 0.893 | 0.897 | +0.004 | One-sided lower -0.008; fail |
+| LLE false-positive rate, 128 negative systems | 0.055 | 0.047 | -0.008 | One-sided upper +0.016; fail |
+
+The +14.2 J/mol HE change is the recorded result from unrounded values; subtraction of the
+separately rounded endpoints gives +14.3. No historical value is replaced. All 171,701 baseline
+requests were finite, all 963 VLE anchors replayed exactly, and no LLE grid job was unresolved. The
+LLE screen used its registered two-grid detection rule and is not a new binodal-composition or
+global-stability result. P58a excluded 51 pure-composition HE inputs before model calls, matching
+the original evaluator's scope. The single run took 2,219 seconds and performed no quantum
+calculation. The software test record retains its two macOS temporary-path assertion errors; it is
+not reported as an all-platform pass.
+
+LV1 failed the joint registered screen. Its pressure decrease did not meet the uncertainty gate, and
+its IDAC and HE errors increased on the specified exposed collections. Its VLE AAD of 13.13% also
+remains above the same-row COSMO-SAC 2010 value of 10.44%. No term removal, fitted corner, LV1
+adoption, alternative weight or second candidate followed. This negative result closes the present
+model-development campaign; it does not prove that all scalar-descriptor alternatives or all future
+contact theories must fail. Source: docs/astra/round16/RESULTS.md and the R16/P58a registration.
+
 ## 4. Discussion
 
 The historical benchmark shows that specified theory-derived interaction constants can retain useful
-IDAC and demixing performance within a common COSMO-SAC framework. Z0x remains worse than COSMO-SAC 2010
-for VLE on the displayed main7 and temporal subsets. This supports a quantitative account of the
-tradeoff, without claiming that all empiricism has been removed or that the model is generally competitive.
-
-The strongest later explanatory result is P54's dispersion attribution on the fixed P52 observations.
-It is more directly relevant to the remaining Z0x discrepancy than the original conductor-limit Z0
-ablation. Bulk permittivity and local contact response remain different quantities, but the small R14
-oracle effect does not justify treating dielectric error as the dominant unresolved cause. The London
-closure should be described as an approximate conversion of electronic descriptors into an excess
-mixing free energy. P54 identifies that conversion as a leading source of benchmark discrepancy;
-it does not isolate one failed geometric assumption or prove double counting.
-
-For positive C6, polarizabilities and cavity volumes, the implemented London exchange is nonnegative:
-its unlike C6 does not exceed the geometric mean of its self coefficients, and its arithmetic-mean
-contact diameter is at least their geometric mean. Consequently its Margules contribution raises
-both component activities and bubble pressure relative to the same residual without it. That
-restriction can increase or reduce absolute pressure error depending on the row. A change to volume
-contact statistics requires differentiating a complete excess Gibbs energy, not merely replacing
-mole fractions in the existing gamma formula. A physically specified alternative must retain its
-unfavorable outcomes and be evaluated under a new prospective, exposure-qualified protocol.
-The P54 fitted corners remain diagnostics and cannot be selected as models by their lower error.
-
-Deriving a new contact kernel from reaction-field response or independent electronic calculations is
-physically possible after the cavity, contact geometry and reference-energy partition are specified.
-Electronic energy alone does not determine the angular and entropic contact free energy. A self-consistent
-finite-dielectric profile model would also need consistent pure references and composition/temperature
-derivatives; another dielectric scale on top of it is not automatically justified. No such new local
-model is validated by the present evidence. A future design needs independent physical acceptance and
-an exposure audit before any confirmatory comparison.
-
-Association and direct simulation remain separate research programs. Reproducing a bonded fraction does
-not validate the site thermodynamics, and an energy/force model does not automatically validate its
-field response or chemical potentials. The numerical association repair changes neither the archived
-scientific failures nor this assessment. The present work is ready for a limitations-aware account of
-its completed evidence, with P54 as the centerpiece of the later VLE explanation. Finalization need
-not await an optional single-recipe dispersion screen, and a failed screen is not grounds to tune
-its weight or conceal the failure. Independent verification of bibliography and reproducibility
-assets remains part of submission preparation.
+IDAC and demixing performance within a common COSMO-SAC framework. Z0x remains worse than COSMO-SAC
+2010 for VLE on the displayed main7 and temporal subsets. This supports a quantitative account of
+the tradeoff, without claiming that all empiricism has been removed or that the model is generally
+competitive.
+
+The strongest later explanatory result is P54's dispersion attribution on the fixed P52
+observations. It is more directly relevant to the remaining Z0x discrepancy than the original
+conductor-limit Z0 ablation. Bulk permittivity and local contact response remain different
+quantities, but the small R14 oracle effect does not justify treating dielectric error as the
+dominant unresolved cause. The London closure should be described as an approximate conversion of
+electronic descriptors into an excess mixing free energy. P54 identifies that conversion as a
+leading source of benchmark discrepancy; it does not isolate one failed geometric assumption or
+prove double counting.
+
+For positive C6, polarizabilities and cavity volumes, the implemented London exchange is
+nonnegative: its unlike C6 does not exceed the geometric mean of its self coefficients, and its
+arithmetic-mean contact diameter is at least their geometric mean. Consequently its Margules
+contribution raises both component activities and bubble pressure relative to the same residual
+without it. That restriction can increase or reduce absolute pressure error depending on the row. A
+change to volume contact statistics requires differentiating a complete excess Gibbs energy, not
+merely replacing mole fractions in a gamma formula. LV1 made that declared change and failed: its
+VLE decrease was unresolved by the registered gate, while IDAC and HE errors increased. This is a
+negative result for that particular cohesive-density closure, not evidence that actual London
+dispersion should be absent or that the original molecular descriptors are intrinsically wrong. The
+P54 fitted corners remain diagnostics and cannot be selected as models by their lower error.
+
+Neither P54 nor the failed LV1 screen establishes a transferable contact kernel or identifies one
+uniquely missing physical effect. Electronic response, contact geometry and the pure-reference
+partition remain approximations of the implemented model. Their unresolved status is a limitation of
+this completed study, not an authorization for another model or native calculation.
+
+Association and direct simulation remain separate research programs. Reproducing a bonded fraction
+does not validate the site thermodynamics, and an energy/force model does not automatically validate
+its field response or chemical potentials. The numerical association repair changes neither the
+archived scientific failures nor this assessment. The present work is being finalized with P54 as
+the centerpiece of the later VLE explanation and LV1 as its registered negative follow-up. The VLE
+gap remains open. The model-development question is closed for this project, with no additional
+experiment, revised weight or model variant proposed. Submission preparation is limited to the
+stated bibliography and historical-artifact checks. Such checks may recover existing evidence, but
+do not authorize rescoring to manufacture missing precision.
 
 ## 5. Limitations
 
 The retained effective area and combinatorial constants, sigma-processing conventions and empirical
-history of some UD conformations limit the meaning of "fit-free". Z0/Z0x interaction constants were not
-regressed to ThermoML. Z0s involves a train-selected discrete choice; Z1 is a fitted comparison. VLE
-uses the same experimental pure-component vapor-pressure correlations in every arm. UD-backed main
-results and exploratory open-profile results are different input versions.
+history of some UD conformations limit the meaning of "fit-free". Z0/Z0x interaction constants were
+not regressed to ThermoML. Z0s involves a train-selected discrete choice; Z1 is a fitted comparison.
+VLE uses the same experimental pure-component vapor-pressure correlations in every arm. UD-backed
+main results and exploratory open-profile results are different input versions.
 
 The original compound and 2017-2019 temporal collections were repeatedly inspected during later
 development. Neither is certified unexposed for another adaptive variant, and no new multi-system
-holdout or data beyond HANNA's training has been certified. Historical confidence intervals keep their
-original scope. Later explanatory ratios have no claimed generalization confidence interval.
+holdout or data beyond HANNA's training has been certified. Historical confidence intervals keep
+their original scope. Later explanatory ratios have no claimed generalization confidence interval.
 
 The 630 original-gradient profiles and six S1/S2 profiles retain their actual provenance. A passed
 historical agreement threshold is not proof of corrected-gradient stationarity, a liquid conformer
-ensemble or equivalence to UD. P35's retrospective coordinate explanation and its tetraEG exception do
-not identify a production geometry rule. LLE detection does not certify global stability or every
+ensemble or equivalence to UD. P35's retrospective coordinate explanation and its tetraEG exception
+do not identify a production geometry rule. LLE detection does not certify global stability or every
 reported composition. Claims about new source versions require separate numerical checks.
 
 ## Data and code availability
 
 The repository contains source code, registrations and public aggregate result records. UD-derived
-geometries and detailed R10-R15 profile/prediction artifacts remain private on the Mac under the applicable
-data-use terms. Some historical predictions and execution inputs are private or untracked; a public
-checkout alone is not asserted to reproduce every historical table. Public result records retain plan
-digests and scope, and their instructions identify required private assets without redistributing them.
+geometries and detailed R10-R16 profile/prediction artifacts remain private on the Mac under the
+applicable data-use terms. Some historical predictions and execution inputs are private or
+untracked; a public checkout alone is not asserted to reproduce every historical table. Public
+result records retain plan digests and scope, and their instructions identify required private
+assets without redistributing them.
 
 ## Figure captions
 
-**Figure 1.** Predicted vs experimental ln gamma_inf for held-out molecules (test split, common subset of
-762 points in 177 systems) for COSMO-SAC 2010, modified UNIFAC (Dortmund), Z0x and HANNA. HANNA was trained on
-data that very likely include these systems.
+**Figure 1.** Predicted vs experimental ln gamma_inf for held-out molecules (test split, common
+subset of 762 points in 177 systems) for COSMO-SAC 2010, modified UNIFAC (Dortmund), Z0x and HANNA.
+HANNA training overlap with these observations is possible and has not been resolved row by row.
 
-**Figure 2.** Hydrogen-bond constants c_hb derived from 17 counterpoise-corrected B3LYP-D4/def2-TZVP dimers
-(points; bars are class means) compared with the fitted COSMO-SAC 2010 values (blue bars).
+**Figure 2.** Hydrogen-bond constants c_hb derived from 17 counterpoise-corrected B3LYP-D4/def2-TZVP
+dimers (points; bars are class means) compared with the fitted COSMO-SAC 2010 values (blue bars).
 
-**Figure 3.** Trade-off between infinite-dilution accuracy (IDAC MAE, x axis) and bubble-pressure accuracy
-(VLE AAD, y axis) in the historical compound-test comparison. Larger electrostatic coefficients
-(Z0, Z0e) favor some dilute properties; the smaller optical-screening prescription (Z0s) improves VLE
-at the expense of other metrics. These are exposed comparisons, not evidence for one optimal coefficient.
+**Figure 3.** Trade-off between infinite-dilution accuracy (IDAC MAE, x axis) and bubble-pressure
+accuracy (VLE AAD, y axis) in the historical compound-test comparison. Larger electrostatic
+coefficients (Z0, Z0e) favor some dilute properties; the smaller optical-screening prescription
+(Z0s) improves VLE at the expense of other metrics. These are exposed comparisons, not evidence for
+one optimal coefficient.
 
-**Figure 4.** Liquid-liquid split detection on held-out molecules: share of experimentally two-phase systems
-where a gap is predicted vs share of experimentally homogeneous systems where a gap is wrongly predicted.
+**Figure 4.** Historical liquid-liquid split detection: recall on the positive test-system
+collection versus false-positive rate on the negative collection. This is one operating point per
+model, not a threshold-swept ROC curve. The archived image exists; exact historical arrays and rates
+require the already-generated private source artifacts identified in the figure audit.
 
-**Figure 5.** Z0x absolute error minus COSMO-SAC 2010 absolute error in ln gamma_inf by solute and solvent
-family (all data, cells with at least 10 points). Blue: Z0x better; orange: COSMO-SAC better.
+**Figure 5.** Z0x absolute error minus COSMO-SAC 2010 absolute error in ln gamma_inf by solute and
+solvent family (all data, cells with at least 10 points). Blue: Z0x better; orange: COSMO-SAC
+better.
 
 ## Supplementary material (files in the repository)
 
-S1 Pre-registration and every later change: `PREREGISTRATION.md`.
-S2 Benchmark construction, rejection log and split hash: `data/benchmark/`, `data/processed/rejections.csv`.
-S3 Dimer geometries and energies, CCSD(T) check, association thermochemistry: `results/qc/`.
-S4 All scorecards with bootstrap intervals: `results/scorecard_*.md`.
-S5 Error maps by chemical family: `results/error_map_idac_*.csv`.
-S6 Open-profile validation and conformer comparison: `results/pyscf_profile_validation.csv`,
-   `data/pyscf_sigma/conformer_summary.csv` (asset availability is stated above).
-S7 Later numerical, glycol, dielectric and factorial evidence: `docs/astra/round2/RESULTS.md` through
-   `docs/astra/round15/RESULTS.md`, with the registrations and private-plan digests referenced there.
-
-## References (to verify against the publisher records before submission)
-
-1. Klamt, A. Conductor-like screening model for real solvents. J. Phys. Chem. 1995, 99, 2224.
-2. Lin, S.-T.; Sandler, S. I. A priori phase equilibrium prediction from a segment contribution solvation
-   model. Ind. Eng. Chem. Res. 2002, 41, 899.
-3. Mullins, E. et al. Sigma-profile database for using COSMO-based thermodynamic methods. Ind. Eng. Chem.
-   Res. 2006, 45, 4389.
-4. Hsieh, C.-M.; Sandler, S. I.; Lin, S.-T. Improvements of COSMO-SAC for vapor-liquid and liquid-liquid
-   equilibrium predictions. Fluid Phase Equilib. 2010, 297, 90.
-5. Hsieh, C.-M.; Lin, S.-T.; Vrabec, J. Considering the dispersive interactions in the COSMO-SAC model for
-   more accurate predictions of fluid phase behavior. Fluid Phase Equilib. 2014, 367, 109.
-6. Bell, I. H.; Mickoleit, E.; Hsieh, C.-M.; Lin, S.-T.; Vrabec, J.; Breitkopf, C.; Jäger, A. A benchmark
-   open-source implementation of COSMO-SAC. J. Chem. Theory Comput. 2020, 16, 2635.
-7. Gmehling, J.; Li, J.; Schiller, M. A modified UNIFAC model. 2. Present parameter matrix and results for
-   different thermodynamic properties. Ind. Eng. Chem. Res. 1993, 32, 178.
-8. Hoffmann, M. et al. (HANNA) Thermodynamically consistent machine learning model for excess Gibbs energy.
-   Nat. Commun. 2026, doi:10.1038/s41467-026-71430-y.
-9. Frenkel, M. et al. ThermoML, an XML-based approach for storage and exchange of experimental and critically
-   evaluated thermophysical and thermochemical property data. J. Chem. Eng. Data 2006, 51, 1504 (series).
-10. Herington, E. F. G. Tests for the consistency of experimental isobaric vapour-liquid equilibrium data.
-    J. Inst. Petrol. 1951, 37, 457.
-11. Onsager, L. Electric moments of molecules in liquids. J. Am. Chem. Soc. 1936, 58, 1486.
-12. Wertheim, M. S. Fluids with highly directional attractive forces. J. Stat. Phys. 1984, 35, 19 (and 35, 35;
-    1986, 42, 459; 42, 477).
-13. Caldeweyher, E. et al. A generally applicable atomic-charge dependent London dispersion correction.
-    J. Chem. Phys. 2019, 150, 154122.
-14. Bannwarth, C.; Ehlert, S.; Grimme, S. GFN2-xTB. J. Chem. Theory Comput. 2019, 15, 1652.
-15. Grimme, S. Supramolecular binding thermodynamics by dispersion-corrected density functional theory.
-    Chem. Eur. J. 2012, 18, 9955.
-16. Sun, Q. et al. Recent developments in the PySCF program package. J. Chem. Phys. 2020, 153, 024109.
-17. Boys, S. F.; Bernardi, F. The calculation of small molecular interactions by the differences of separate
-    total energies. Mol. Phys. 1970, 19, 553.
+S1 Pre-registration and every later change: `PREREGISTRATION.md`. S2 Benchmark construction,
+rejection log and split hash: `data/benchmark/`, `data/processed/rejections.csv`. S3 Dimer
+geometries and energies, CCSD(T) check, association thermochemistry: `results/qc/`. S4 All
+scorecards with bootstrap intervals: `results/scorecard_*.md`. S5 Error maps by chemical family:
+`results/error_map_idac_*.csv`. S6 Open-profile validation and conformer comparison:
+`results/pyscf_profile_validation.csv`,    `data/pyscf_sigma/conformer_summary.csv` (asset
+availability is stated above). S7 Later numerical, glycol, dielectric and dispersion evidence:
+`docs/astra/round2/RESULTS.md` through    `docs/astra/round16/RESULTS.md`, with the registrations
+and private-plan digests referenced there. S8 Supplementary narrative: `manuscript/supplement.md`;
+claim and reference audit:    `docs/astra/round17/CLAIMS.json` and
+`docs/astra/round17/REFERENCES.md`.
+
+## References
+
+1. Klamt, A. Conductor-like Screening Model for Real Solvents: A New Approach to the Quantitative Calculation
+   of Solvation Phenomena. J. Phys. Chem. 1995, 99 (7), 2224-2235. doi:10.1021/j100007a062.
+2. Lin, S.-T.; Sandler, S. I. A Priori Phase Equilibrium Prediction from a Segment Contribution Solvation
+   Model. Ind. Eng. Chem. Res. 2002, 41 (5), 899-913. doi:10.1021/ie001047w.
+   Related correction: Ind. Eng. Chem. Res. 2004, 43 (5), 1322. doi:10.1021/ie0308689.
+3. Mullins, E. et al. Sigma-Profile Database for Using COSMO-Based Thermodynamic Methods.
+   Ind. Eng. Chem. Res. 2006, 45 (12), 4389-4415. doi:10.1021/ie060370h.
+4. Hsieh, C.-M.; Sandler, S. I.; Lin, S.-T. Improvements of COSMO-SAC for Vapor-Liquid and Liquid-Liquid
+   Equilibrium Predictions. Fluid Phase Equilib. 2010, 297 (1), 90-97. doi:10.1016/j.fluid.2010.06.011.
+5. Hsieh, C.-M.; Lin, S.-T.; Vrabec, J. Considering the Dispersive Interactions in the COSMO-SAC Model for
+   More Accurate Predictions of Fluid Phase Behavior. Fluid Phase Equilib. 2014, 367, 109-116.
+   doi:10.1016/j.fluid.2014.01.032. Corrigendum: 2014, 384, 14-15, doi:10.1016/j.fluid.2014.10.019
+   (publisher text and implications remain to be checked; no numerical result is reinterpreted here).
+6. Bell, I. H.; Mickoleit, E.; Hsieh, C.-M.; Lin, S.-T.; Vrabec, J.; Breitkopf, C.; Jäger, A.
+   A Benchmark Open-Source Implementation of COSMO-SAC. J. Chem. Theory Comput. 2020, 16 (4), 2635-2646.
+   doi:10.1021/acs.jctc.9b01016.
+7. Gmehling, J.; Li, J.; Schiller, M. A Modified UNIFAC Model. 2. Present Parameter Matrix and Results for
+   Different Thermodynamic Properties. Ind. Eng. Chem. Res. 1993, 32 (1), 178-193. doi:10.1021/ie00013a024.
+8. Hoffmann, M.; Specht, T.; Göttl, Q.; Burger, J.; Mandt, S.; Hasse, H.; Jirasek, F.
+   Thermodynamically Consistent Machine Learning Model for Excess Gibbs Energy.
+   Nat. Commun. 2026, 17, 3485. doi:10.1038/s41467-026-71430-y.
+9. Frenkel, M. et al. ThermoML: An XML-Based Approach for Storage and Exchange of Experimental and Critically
+   Evaluated Thermophysical and Thermochemical Property Data. 1. Experimental Data.
+   J. Chem. Eng. Data 2003, 48 (1), 2-13. doi:10.1021/je025645o.
+10. Herington, E. F. G. Tests for the Consistency of Experimental Isobaric Vapour-Liquid Equilibrium Data.
+    J. Inst. Petrol. 1951, 37, 457. Provisional: the original publisher record/title/page range has not
+    been verified in this audit. Do not invent a DOI or infer the missing range.
+11. Onsager, L. Electric Moments of Molecules in Liquids. J. Am. Chem. Soc. 1936, 58 (8), 1486-1493.
+    doi:10.1021/ja01299a050.
+12. Wertheim, M. S. Fluids with Highly Directional Attractive Forces. I. Statistical Thermodynamics.
+    J. Stat. Phys. 1984, 35, 19-34. doi:10.1007/BF01017362; II. Thermodynamic Perturbation Theory and
+    Integral Equations, 1984, 35, 35-47, doi:10.1007/BF01017363; III. Multiple Attraction Sites,
+    1986, 42, 459-476, doi:10.1007/BF01127721; IV. Equilibrium Polymerization,
+    1986, 42, 477-492, doi:10.1007/BF01127722.
+13. Caldeweyher, E. et al. A Generally Applicable Atomic-Charge Dependent London Dispersion Correction.
+    J. Chem. Phys. 2019, 150, 154122. doi:10.1063/1.5090222. Direct publisher verification remains
+    outstanding; the author record supports the bibliographic identity.
+14. Bannwarth, C.; Ehlert, S.; Grimme, S. GFN2-xTB: An Accurate and Broadly Parametrized Self-Consistent
+    Tight-Binding Quantum Chemical Method with Multipole Electrostatics and Density-Dependent Dispersion
+    Contributions. J. Chem. Theory Comput. 2019, 15 (3), 1652-1671. doi:10.1021/acs.jctc.8b01176.
+15. Grimme, S. Supramolecular Binding Thermodynamics by Dispersion-Corrected Density Functional Theory.
+    Chem. Eur. J. 2012, 18 (32), 9955-9964. doi:10.1002/chem.201200497.
+16. Sun, Q. et al. Recent Developments in the PySCF Program Package. J. Chem. Phys. 2020, 153, 024109.
+    doi:10.1063/5.0006074.
+17. Boys, S. F.; Bernardi, F. The Calculation of Small Molecular Interactions by the Differences of Separate
+    Total Energies. Some Procedures with Reduced Errors. Mol. Phys. 1970, 19 (4), 553-566.
+    doi:10.1080/00268977000101561.
+18. Constantinescu, D.; Gmehling, J. Further Development of Modified UNIFAC (Dortmund): Revision and
+    Extension 6. J. Chem. Eng. Data 2016, 61 (8), 2738-2748. doi:10.1021/acs.jced.6b00136.
+    The installed DOUFIP2016 table/version still needs an execution-artifact citation, beyond this paper.
+
+Bibliographic metadata verification is not verification of every methodological assertion in an article.
+The reference audit lists outstanding publisher and software/model-version checks before submission.
diff --git a/manuscript/supplement.md b/manuscript/supplement.md
new file mode 100644
index 0000000..2226c54
--- /dev/null
+++ b/manuscript/supplement.md
@@ -0,0 +1,228 @@
+# Supplementary evidence and source qualifications
+
+This supplement accompanies the R17 manuscript-only revision. It records completed work; it
+authorizes zero new quantum calculations and zero activity-model requests. Original registrations,
+scorecards and RESULTS files remain unchanged. Section labels from earlier drafts are preserved in
+descriptions so that historical claims can be located. Numerical statements below are attributed to
+existing records, not to a new data analysis. Source status is recorded in
+docs/astra/round17/CLAIMS.json.
+
+## S0. Historical statistics requiring source qualification
+
+The main historical table combines multiple property-specific sources. Its seven non-HANNA IDAC, VLE
+and HE entries match main7 after rounding. Its test_both column matches test_both/main7. The early
+LLE balanced-accuracy summary is supported by the contemporaneous progress record, which describes
+the advantage as significant. The exact original bootstrap output and the separate historical HANNA
+test arrays were not recovered in the reviewed public files. Recovering these already-generated
+artifacts is an editorial provenance task. No rerun, fresh bootstrap or model call is authorized by
+this note.
+
+The original draft printed Z0-minus-COSMO-SAC IDAC [-0.17, +0.08] and VLE [+6.6, +14.5]. The former
+is compatible with main6 rounding, and the latter with results/scorecard_test.md; neither is the
+interval of the named main7 source. It also printed test_both [-0.54, -0.22], which does not
+reproduce the main7/test_both interval [-0.552, -0.229]. The corrected prose names main7 and uses
+its stored values. All original scorecards remain immutable; the edit repairs citation/version
+assignment, not results.
+
+The following old precision remains a historical draft assertion pending the existing source
+artifact, not a freshly verified inferential result: LLE BA Z0-minus-COSMO-SAC [+0.02, +0.11],
+Z0-minus-UNIFAC [+0.04, +0.14], Z0x-minus-COSMO-SAC [+0.02, +0.11], Z0x-minus-UNIFAC [+0.03, +0.13],
+and Z0x-minus-HANNA [-0.03, +0.07]. The old binodal comparison was 0.05 versus 0.18; its exact
+endpoint denominator and source artifact remain required. The historical HANNA row was IDAC 0.24
+(including 0.24 on test_both), VLE 7.1% (median 2.1%), HE 70 J/mol and BA 0.88. Preserve these
+reported values, but do not substitute another subset to reconstruct them. An interval containing
+zero indicates no resolved difference, not equivalence. The manuscript's quantitative table is
+explicitly marked historical.
+
+## S1. Open profiles and numerical infrastructure
+
+An open pipeline (PySCF BP86/def2-TZVP, C-PCM conductor limit, xTB geometries, NIST averaging and
+splitting) was checked against the NIST/DMol3 profiles before use. On the registered
+25-molecule/2,302-IDAC-occurrence check the median change in COSMO-SAC-dsp ln gamma_inf was 0.153,
+just above the pre-set bar of 0.15 (water 1.14, triethylene glycol 0.84), with reported experimental
+MAEs 0.79 versus 0.74. The profiles were therefore not merged into the main benchmark. On the 136
+previously uncovered compounds (exploratory, 218 IDAC points in 72 systems), Z0 and Z0x reach MAE
+0.68 and 0.69 against 1.00 for COSMO-SAC 2010, 0.94 for COSMO-SAC-dsp, 0.55 for UNIFAC (79%
+coverage) and 0.11 for HANNA.
+
+Later v2 conductor-optimized profiles passed the original median agreement gate at 0.1493, only
+0.0007 below 0.15, and were retained as exploratory rather than an accuracy-equivalent UD
+replacement. The frozen population contains 630 files passing the original Berny predicate and six
+separately flagged S1/S2 files. The R2-R9 numerical review preserves accepted performance changes
+and rejected trials; optimizer-state persistence is not relabeled E after its E gate failed. Omitted
+XC-grid response and the incomplete earlier finite-difference referee limit stationarity claims. The
+corrected-gradient rollout failed P32's compatibility gate, and the TEG energy-gradient mismatch
+remained unresolved when the R8/R9 diagnostic budget closed. There is no accepted blanket re-polish
+or chain rescue. See `docs/astra/round7/RESULTS.md`, `docs/astra/round8/RESULTS.md` and
+`docs/astra/round9/RESULTS.md`.
+
+ The original median comparison is an input-compatibility gate, not proof of identical predictions.
+R6/P31 reproduces the later matched-input errors: IDAC 0.8040 (UD) versus 0.9423 (open630) on 816
+observations, paired difference CI [0.0506, 0.2379]; VLE 15.90% versus 16.41% on 12,403
+observations, CI [-0.75, 2.10]; and HE 618.6 versus 699.3 J/mol on 8,573 observations, CI [50.9,
+108.8]. Thus VLE has no resolved difference in that comparison, while the displayed IDAC and HE
+differences favor UD. These are different subsets from main7 and precede the opt-in P28 endpoint
+correction.
+
+R6 accepted P28 on numerical grounds: maximum error 2.73e-9 against a 1e-8 reference gate and
+measured endpoint speed-up 3.06-3.25. The corrected test IDAC MAEs were slightly larger, not
+optimized for error: UD 0.8394 to 0.8397 and open630 0.9423 to 0.9427. Historical endpoint tables
+remain unchanged.
+
+R7 resolved omitted-response errors in three sampled directions, but no case passed an all-direction
+stationarity certificate. P32's maximum dsp change was 0.0121 against the strict 0.01 compatibility
+limit, despite both arms reaching the original Berny predicate. The pilot and chain stage did not
+run. P34 requested 40 cases: 35 stress-positive, four unresolved and one missing. Its 0.01 angstrom
+imposed displacements measured sensitivity, not the unknown distance to a corrected optimum. The
+incomplete probability sample supplies no population bound. R8/R9 closed the remaining TEG
+diagnostic as unresolved; the tiny retained switching weight did not establish a one-node cause for
+the finite-difference collapse.
+
+R2-R4 accepted performance changes and metadata operations retain their individual E/A labels and
+checks. In particular, the failed E classification of optimizer-state persistence is not reversed;
+its A acceptance is a different record. P20 protects exactly 630 primary, one S1 and five S2
+selected profiles, rather than every superseded file in those folders. Gap witnesses in the later
+LLE audit support detection only; they do not supply converged endpoint compositions. These controls
+do not restore a general numerical-stationarity claim for the historical open-profile geometries.
+
+Sources: docs/astra/round2/RESULTS.md through round9/RESULTS.md, the complete PREREGISTRATION.md,
+and results/scorecard_all_gap_exploratory.md. Detailed profiles and relevant execution assets remain
+private on the Mac; the public aggregate audit is not a replacement for native acceptance.
+
+## S2. Conformer and glycol evidence
+
+For the 50 most flexible benchmark molecules (4.9 conformers on average, BP86/def2-SVP profiles),
+replacing the lowest-energy conformer by the Boltzmann ensemble changed predictions very little:
+median |d ln gamma_inf| 0.009 (COSMO-SAC-dsp) and 0.011 (Z0x), 90th percentile under 0.09, and the
+original draft reported IDAC MAE difference [0.00, +0.01] and VLE [-0.35, +0.32] points. Those
+rounded intervals alone do not establish equivalence or even reveal the unrounded lower IDAC bound.
+The lowest conformer carries 60% of the weight on average. This establishes a small effect for that
+finite proposal and weighting scheme, not the absence of conformational effects or a validated
+phase-dependent ensemble.
+
+R10 recovered and replayed all twelve fixed-panel UD raw files to their historical profiles. R11's
+ordered open-method cross attributes the polar-tail gaps for ethylene, diethylene and triethylene
+glycol mainly to stored coordinate inputs, including hydrogen positions and orientation.
+Tetraethylene glycol is an exception: its raw-tail gap was mainly method, and its other tail
+contrasts were small. No member passed the registered whole-profile attribution rule. These
+statements retain R11's original labels.
+
+R12/P46a then scored exactly 142 already-inspected glycol-solvent observations with original open
+solutes and a common P28 endpoint. Pooled MAE in ln gamma_inf was 1.813 for the original open
+solvent profiles, 0.702 for the open method at the recovered UD coordinates, and 0.419 for UD
+solvent profiles. The coordinate-derived substitution removed 1.111, about 80% of the open-to-UD
+comparator MAE gap and 61% of the original open absolute error; 139 rows improved and three
+worsened. Shape carried essentially all of the factorial error reduction. Tetraethylene glycol
+recovered only 13% of its comparator gap. The remaining 0.283 is a conditional difference of MAEs,
+not a universal method-error estimate. P47 located same-geometry method differences toward the
+acceptor side and the EG/DEG/TEG coordinate differences toward the donor-side tail; those partitions
+are not hydrogen-bond energies or binwise error causes.
+
+This was retrospective explanatory ThermoML scoring. The UD notice reports database-level revisions
+using vapor-pressure predictions without identifying which panel members were revised. The result
+does not establish extended chains as the liquid conformations or adopt a geometry rule. P35 closed
+after R13 with its explanatory finding; the liquid distribution remains unresolved and all 630+6
+open files remain frozen. See `docs/astra/round10/RESULTS.md` through
+`docs/astra/round13/RESULTS.md`.
+
+ The 50-molecule/244-conformer description and median approximately 0.01 are corroborated by
+PROGRESS.md. The more precise 0.009/0.011 medians, percentile, weight and interval statements above
+retain the old draft's numerical record, but their cited private queue log
+(_queue/done/26_conformer_eval.sh.log) was not read in R17. They are not marked independently
+verified. R5/P26's later incomplete proposal pools did not accept an ensemble or invalidate the
+earlier finite-pool record.
+
+R10 verified twelve raw-file/profile lineages, not exact electronic input decks. R11's attribution
+is ordered, because the reverse UD-method/open-coordinate corner was not computed. The 0.359
+normalized- shape background was control-derived, not stochastic numerical noise. R12/P46a fixed EG
+at ten rather than nine observations by exact identity before scoring; the total is 142, not the
+superseded 141. Every solute remained the original open input, and the primary comparison used P28
+for all arms. R13 closed the explanatory campaign with the liquid-state mechanism unresolved.
+Nothing authorizes using extended UD conformations because they reproduce the already-inspected
+result.
+
+Sources: docs/astra/round5/RESULTS.md, round6/RESULTS.md, and round10/RESULTS.md through
+round13/RESULTS.md.
+
+## S3. Association failures and simulation provenance
+
+Z0w replaces the COSMO hydrogen-bond term by Wertheim TPT1 association with site-pair strengths
+Delta_AB = (kT/P0) exp(-dG_AB/RT), where dG_AB is the dimerization free energy from the B3LYP-D4
+binding energy plus GFN2-xTB quasi-RRHO thermochemistry (registered before any prediction). As
+registered it fails: held-out IDAC MAE 0.97 vs 0.80 for Z0x and VLE AAD 27.4% vs 15.2%, and it
+predicts false liquid-liquid splits in 9.4% of miscible test systems (balanced accuracy 0.90,
+unchanged, because it finds more real splits). The historical interpretation identifies the largest
+errors as aqueous: organic solutes in water are overpredicted by 5 to 7 in ln gamma_inf. Post hoc,
+on non-aqueous systems only, the historical draft reports smaller Z0w errors among its listed
+comparators (test IDAC MAE 0.67 vs 0.88 for COSMO-SAC 2010, bootstrap difference [-0.29, -0.09]; vs
+Z0x [-0.17, +0.04]). A proposed diagnosis is the gas-phase entropy in dG: bonding to a larger
+partner costs more rotational entropy (water-acetone -121 J/mol/K vs water-water -87 J/mol/K), which
+makes cross-association about ten times weaker than water self-association and turns water into an
+unrealistically closed network.
+
+ The overall stored IDAC difference interval is [-0.035, +0.400] on 762 observations / 177 systems
+(results/scorecard_test_z0w.md); the failed registration is not a claim of a resolved overall IDAC
+increase. The specific non-aqueous interval endpoints in the old paragraph require their already-
+computed private artifact before submission. PROGRESS.md corroborates the rounded non-aqueous means
+and historical VLE failure. The -121 and -87 J/mol/K examples are supported by the stored
+results/qc/assoc_thermo.csv entries. This is the model's gas-phase thermochemistry, not a measured
+liquid bonding entropy or a proof that no other term contributed to the failure.
+
+ The association constants that a continuum or gas-phase dimer calculation cannot supply can be
+measured directly in simulated liquids. We use MACE-OFF23 (small), a machine-learned interatomic
+potential trained only on DFT reference data, as a teacher. Speed was the obstacle: the stock ASE
+path managed 0.37 ns/day for 648 water atoms on an NVIDIA L4. Three exact changes remove most of it.
+The first is NVIDIA's cuEquivariance fused tensor-product kernels (forces identical to 2-4e-6 eV/A).
+The second is batching many small boxes per GPU. The third is a lean integrator that feeds the model
+directly, with a Verlet neighbour list whose superset is filtered to the cutoff every step. This is
+exact because MACE's radial envelope is identically zero beyond r_max. Aggregate throughput reaches
+8.9 ns/day (about 24x), with every change checked against reference forces. Two approximations were
+rejected by pre-registered gates: TF32 arithmetic (force error 3e-3 eV/A) and hydrogen mass
+repartitioning with 1-2.5 fs steps (energy drift 2.3-183 times the 0.5 fs reference). Z0w3 inverts
+TPT1 on hydrogen-bond statistics from NPT simulations of seven liquids at three temperatures
+(PREREGISTRATION.md, session 5b). The registered short water controls were inside their stated
+acceptance window (water 87% bonded, 1.115 g/cm3; an independent engine gives 86% and 1.10), but
+Z0w3 fails badly: temporal IDAC MAE 2.19 against 1.45 for Z0x, aqueous test systems 4.79 against
+1.76. The simulated association is strong (water Delta about ten times the gas-phase dimer value).
+Overlap with electrostatic contributions in the COSMO reference is a plausible architectural
+explanation. The explicit COSMO hydrogen-bond constants were already zero in Z0w and its
+descendants, so merely turning that term off is not a new solution. The nitrogen-site occupancy
+mismatch and temperature-fit failures also matter. The failed registrations stand; neither a unique
+double-counting decomposition nor a successful replacement architecture was established.
+
+A later, separate source regression must not be confused with these historical failures. Since P6,
+Z0x's optimized interior dispatch bypassed the association subclasses' _g overrides; enabling P28
+could do so at pure endpoints as well. Archived Z0w/Z0w2/Z0w3 scores predate that change. P55's
+separate repair restores full-subclass-g finite differences, including the historical one-sided
+endpoint approximation; it does not supply an exact association endpoint or a new association score.
+Software regression tests and any future physical validation are reported separately. No fourth
+association variant is accepted.
+
+ The equivalence language above concerns the checked energy/force evaluation paths. It does not
+prove that finite-step thermostatted dynamics samples an exact equilibrium distribution, or that an
+energy/force-trained potential predicts accurate chemical potentials. The MACE-OFF23 weight file,
+execution environment and corresponding primary model publication need exact version citations in
+the submission archive. R17 does not invent them or rerun simulation. The HMR and TF32 failures
+remain recorded under their original criteria, and the historical Z0w3 scores predate the P6
+dispatch defect.
+
+Sources: PREREGISTRATION.md session 5b and speed-up results, PROGRESS.md session 5,
+docs/astra/round14/RESULTS.md and round15/RESULTS.md. The original NPT driver and several detailed
+score/bootstrap outputs are not asserted to be reconstructible from the public checkout alone.
+
+## S4. Exposure, amendment and failure ledger
+
+R2-R9 contain performance trials, failed stationarity/compatibility gates and an unresolved
+numerical closeout. R10-R13 contain recovered input lineage and exposed glycol explanations. R14's
+experimental- epsilon oracle and R15's fitted-ingredient cube are diagnostics. R16's LV1 is a
+complete but failed registered A screen. These are not pooled into one newly held-out experiment.
+P46a, P52a and P58a were input-integrity amendments made before the respective affected model calls,
+and their superseded preparation attempts remain in the original records. No R17 editorial action
+changes an acceptance gate, denominator, stored number or model default.
+
+The submission lead should be historical IDAC comparison, historical LLE detection, VLE/HE losses,
+then P54 and its LV1 negative follow-up. The infrastructure narratives above can be supplementary
+sections referenced by one paragraph each in the main text. Current subsection numbers are retained
+in this review patch so the requested additions remain in 3.11; typesetting renumbering may follow
+without changing results. See the R17 audit for the exact proposed reading order and figure
+inventory.
```
<!-- END PATCH P60 -->

<!-- BEGIN PATCH P61 -->
```diff
diff --git a/docs/astra/round17/CLAIMS.json b/docs/astra/round17/CLAIMS.json
new file mode 100644
index 0000000..43c8a52
--- /dev/null
+++ b/docs/astra/round17/CLAIMS.json
@@ -0,0 +1,968 @@
+{
+  "schema": "r17-manuscript-audit-v1",
+  "base": "35ab60046f3f4a7566d8eeee6b13172a6d0becc2",
+  "original_path": "manuscript/draft.md",
+  "original_blob": "edf2eae2b30fb97b8934c4e86c81a09685e8704d",
+  "original_lines": 520,
+  "revised_sha256": "e203574d5988d478e10cf1bfbece839114461c85aa444c4cb05430c289844f13",
+  "supplement_sha256": "dd1ef7a283f1d48726e20d3b70cf98571cbe557089f2ffbfffb910f065fab731",
+  "sources": {
+    "PREREGISTRATION.md": "c1b84665223940e3042c4d16c8ce3006479ead3d",
+    "PROGRESS.md": "216bb364f496e7846c8a450643768e521eb4b546",
+    "README.md": "263447947ec5b953b1e5d5e9259aaef22cb6fb62",
+    "src/zcosmo/scope.py": "894d89cee8e33bb194f60e54469302236b77df5b",
+    "src/zcosmo/cosmosac.py": "c226a668b7b9dba9e7400cda180fafd8faa700f3",
+    "src/zcosmo/z0x.py": "c558d4e95db9b78f3b57d6a103a293e21feeb9af",
+    "results/scorecard_test_main7.json": "aee303792afcdff48e90aa74d074802a3bb7596b",
+    "results/scorecard_test_main7.md": "f180ea4d506619e010f2ba0a673965d4aa22163e",
+    "results/scorecard_test_both_main7.md": "c3e3bfd5df6e32cdec5c6e8c1b21a5b952ea0ce7",
+    "results/scorecard_test_main6.md": "9d5ae19484dc21844e3b14360d156b7bc99b350b",
+    "results/scorecard_test.md": "bce8eed067c3eb436b9d3343199790f50bb13305",
+    "results/scorecard_temporal_ext.md": "c8895658373b0c1e582a63b3256d1f116dd56620",
+    "results/scorecard_temporal_test_ext.md": "076dd6365ab13c7ac32f7ab74aa0c4abc2b2f65d",
+    "results/scorecard_all_ablation.md": "37f3a51e5d94eca2f5447740ed3ec959e22d5dd6",
+    "results/scorecard_test_sensitivity.md": "e283a7a59ebd6454a3a7404ba5c63074a6557710",
+    "results/scorecard_all_gap_exploratory.md": "7b2637440112e1e5290e1026bd9d3fd87b5822d8",
+    "results/scorecard_test_z0w.md": "720b2bb8e407b38f778debe9e93e0448e10f9c6e",
+    "results/error_map_idac_all_long.csv": "b1caa4827ebe9df0f98e3f8006a6d5c27b8857aa",
+    "results/qc/ccsdt_check.csv": "10aeaafb0ccb2ef0a8d6c17d00de4c3a9c926135",
+    "results/qc/hb_constants_per_dimer.csv": "bd249aaf7ad01e5fd70a7357766c6db6e5cf1307",
+    "results/qc/hb_constants_by_class.csv": "fe225ee279fd80fc599c871955011370ddafb5e0",
+    "results/qc/assoc_thermo.csv": "a7044b9c0023d28d92f8aee7af1225c4f2f21b37",
+    "scripts/make_figures.py": "7238311999c7ede74ea35acfdff2544710a05836",
+    "docs/astra/round2/RESULTS.md": "6da753d4b62210817abf98b25da7e1e12458ee45",
+    "docs/astra/round3/RESULTS.md": "c6de1f0a15d47cd596c56f5de00928f2a3238b1d",
+    "docs/astra/round4/RESULTS.md": "428e5b4e0ce8801a5f55ac16d5a1a9a9217d400a",
+    "docs/astra/round5/RESULTS.md": "88d669c4c8abc6269e55f3609d7ff390e7f6fc5c",
+    "docs/astra/round6/RESULTS.md": "4dfc953f8cff9846f1810cb01ef82719569a9a8e",
+    "docs/astra/round7/RESULTS.md": "ef78bceea953b5bfc4167aa28ea366e58ffe5213",
+    "docs/astra/round8/RESULTS.md": "d34dc87a3d0724740df4c344bb481ff4ee861583",
+    "docs/astra/round9/RESULTS.md": "00f6d3b81c4da803cefbe5da9024b8d4ba453f07",
+    "docs/astra/round10/RESULTS.md": "0656f37159bbeb6f7a18477f91b513e46f3c3e0c",
+    "docs/astra/round11/RESULTS.md": "458210e730623727b6e94881511459bd48c187aa",
+    "docs/astra/round12/RESULTS.md": "c036e8e24aa45a03aed0485664b3a26cd842c17f",
+    "docs/astra/round13/RESULTS.md": "8d5885b430e3dda0d44db49d50a5303f2499fa50",
+    "docs/astra/round14/RESULTS.md": "90b8a880d4c887f3dce09d67592c5383bf02f295",
+    "docs/astra/round15/RESULTS.md": "dd2eeb1fa384f320e338341cd72bd5479a69ba9c",
+    "docs/astra/round16/RESULTS.md": "328926b9c40209fa4bcac371575fd0794697ad3b",
+    "manuscript/figures/fig1_idac_parity_test.png": "72659886f5d3b451cf00adfe536a3715b1d6553a",
+    "manuscript/figures/fig2_hbond_constants.png": "c22a980ff1e3266e8865b84a2bac9c9deebe6367",
+    "manuscript/figures/fig3_tradeoff.png": "62205ae989a86687abf91d99bdd9b1010d7cb46a",
+    "manuscript/figures/fig4_lle_detection.png": "03560344877b0867a97b806b7014ebb477a7d8b5",
+    "manuscript/figures/fig5_error_map.png": "78e50e66d2dc842667e0ed5aa2a9e42a42a7fece"
+  },
+  "claims": [
+    {
+      "id": "C01",
+      "start_line": 3,
+      "end_line": 3,
+      "original_sha256": "f9c57ee6da28abff75b565ded25cd984d24e320bca4393fcbbeebaf64338b645",
+      "status": "editorial",
+      "claim": "Original 2026-09-24 / revision 2026-10-08 dates",
+      "sources": [
+        "PROGRESS.md"
+      ],
+      "fix": "Preserve; R17 is an editorial revision, not a new experimental date."
+    },
+    {
+      "id": "C02",
+      "start_line": 7,
+      "end_line": 16,
+      "original_sha256": "8bd77e3bcae75104dcad9736c26a87a376fc0b4089c12a7869f273bad88ca856",
+      "status": "scope_correction",
+      "claim": "17 dimers, theory/QC interaction constants and inherited empirical inputs",
+      "sources": [
+        "PREREGISTRATION.md",
+        "results/qc/hb_constants_by_class.csv",
+        "docs/astra/round10/RESULTS.md"
+      ],
+      "fix": "Keep no-new-ThermoML-regression claim; do not imply every convention or upstream input is first-principles."
+    },
+    {
+      "id": "C03",
+      "start_line": 18,
+      "end_line": 24,
+      "original_sha256": "5b096361a913b6825d5aac027691c152befb66ddf4fdf587d100c769245c22af",
+      "status": "scope_correction",
+      "claim": "9184 files; IDAC3438 VLE46127 LLE7158 HE27366; split chronology",
+      "sources": [
+        "PROGRESS.md",
+        "PREREGISTRATION.md"
+      ],
+      "fix": "Counts agree with session 1. Say split frozen before Z0 predictions, not before every model run. Preserve later exposure."
+    },
+    {
+      "id": "C04",
+      "start_line": 26,
+      "end_line": 41,
+      "original_sha256": "6a6e13477d01199665de883ede9b81c07979e43a368a9194f911fd55fa5a08ef",
+      "status": "mixed_source_precision",
+      "claim": "Abstract IDAC/LLE/VLE means, HB counts, epsilon oracle and P54 shares",
+      "sources": [
+        "results/scorecard_test_main7.json",
+        "results/scorecard_test_main7.md",
+        "PROGRESS.md",
+        "docs/astra/round14/RESULTS.md",
+        "docs/astra/round15/RESULTS.md",
+        "docs/astra/round16/RESULTS.md"
+      ],
+      "fix": "Use no resolved IDAC difference. Cite LLE as contemporaneous reported advantage, not independently recovered exact bootstrap. Add LV1 negative result; limit P54 to963rows."
+    },
+    {
+      "id": "C05",
+      "start_line": 43,
+      "end_line": 43,
+      "original_sha256": "e569d07d3d78b3857cd1582a9bd94ee38bd3c9c8dd7ff6e5f1bc25777006fefd",
+      "status": "structural",
+      "claim": "Section number/title",
+      "sources": [],
+      "fix": "Retain review numbering; submission reading order proposed separately."
+    },
+    {
+      "id": "C06",
+      "start_line": 57,
+      "end_line": 60,
+      "original_sha256": "788420bb5ad315398aeb270c172c18bf918d71570c38b13be18abf8fa28a3372",
+      "status": "publisher_checked",
+      "claim": "HANNA about824000 DDB observations",
+      "sources": [
+        "REF8"
+      ],
+      "fix": "Publisher specifies824481; rounded claim valid. Do not infer per-row overlap or general superiority from this local comparison."
+    },
+    {
+      "id": "C07",
+      "start_line": 70,
+      "end_line": 70,
+      "original_sha256": "2fc4703bd8f7cc604a6ab110bbb57fbe93eef80f582a49aad84f17cdb3035a32",
+      "status": "structural",
+      "claim": "Section number/title",
+      "sources": [],
+      "fix": "Retain review numbering; submission reading order proposed separately."
+    },
+    {
+      "id": "C08",
+      "start_line": 72,
+      "end_line": 78,
+      "original_sha256": "e48c2538a3fe0145148107ebe8dcb7df903d7590a80383c96aab9906373f7f61",
+      "status": "scope_correction",
+      "claim": "25heavy atoms;250-450K;500kPa;2K/.2IDAC;Herington;5cloudpoints",
+      "sources": [
+        "PREREGISTRATION.md",
+        "src/zcosmo/scope.py"
+      ],
+      "fix": "Document binned median IDAC filter, retained untestable VLE and known-Tc-only rejection at0.98Tc; boundaries inclusive."
+    },
+    {
+      "id": "C09",
+      "start_line": 80,
+      "end_line": 89,
+      "original_sha256": "51bc3bf766115a69ed6a05c20d1a61fa33c2a1543f703f1ffd1c0612d8608dff",
+      "status": "scope_correction",
+      "claim": "20%,seed20260924,11923files,2017-2019,reference years2010/2014/2016",
+      "sources": [
+        "PREREGISTRATION.md",
+        "PROGRESS.md"
+      ],
+      "fix": "Preserve historical dates. Table-fit dates do not prove all upstream data independent; old collections are exposed."
+    },
+    {
+      "id": "C10",
+      "start_line": 91,
+      "end_line": 95,
+      "original_sha256": "10da41ccc606c0622a2f6c5962a3078574c4468f81d50f3b6945da32a5496c1b",
+      "status": "public_record",
+      "claim": "NIST implementation2e-9 on400pairs;localUD2259 vs publication2261",
+      "sources": [
+        "PROGRESS.md"
+      ],
+      "fix": "Distinguish reported code gate and project inventory from Bell publication count; no gate re-executed."
+    },
+    {
+      "id": "C11",
+      "start_line": 97,
+      "end_line": 109,
+      "original_sha256": "a0e7a317a044385f2d22e28d609eadb4840a311f5b703dfafbaed197a44ece75",
+      "status": "verified_source",
+      "claim": "aeff7.25 q079.53 r066.69 z10; cES12226/8197;17dimer recipe",
+      "sources": [
+        "PREREGISTRATION.md",
+        "src/zcosmo/cosmosac.py"
+      ],
+      "fix": "Preserve constants; state inherited conventions. Rounded cES values follow documented formulas, not independently fitted numbers."
+    },
+    {
+      "id": "C12",
+      "start_line": 111,
+      "end_line": 116,
+      "original_sha256": "9a7bf6d32135ad6168e602c7a6c7aaa621937d170d37c6a27801ca8f04aa9076",
+      "status": "scope_correction",
+      "claim": "one-center C6,d^-6,z/2=5 and pure-reference cancellation",
+      "sources": [
+        "PREREGISTRATION.md",
+        "src/zcosmo/cosmosac.py"
+      ],
+      "fix": "Retain declared modeling assumptions. Pure Psat does not automatically double count an excess mixing term."
+    },
+    {
+      "id": "C13",
+      "start_line": 118,
+      "end_line": 127,
+      "original_sha256": "48ea72e3baef17068b7168e881098b944037c5a02ba795df472cf8a244cf90d0",
+      "status": "public_record",
+      "claim": "f=(eps-1)/(eps+1/2),P6 analyticinterior,P28opt-in,6Z0svariants",
+      "sources": [
+        "PREREGISTRATION.md",
+        "src/zcosmo/z0x.py",
+        "docs/astra/round6/RESULTS.md"
+      ],
+      "fix": "Preserve P6/P28 numerical distinction; Z0s is a training-selected choice and historical endpoints are not overwritten."
+    },
+    {
+      "id": "C14",
+      "start_line": 129,
+      "end_line": 136,
+      "original_sha256": "da771ed81e0c45ba08e06f3d8f93f9793e797ab32cd35f99599d34164d0d40c7",
+      "status": "scope_correction",
+      "claim": "336negative states;1000systembootstraps andpaired95%",
+      "sources": [
+        "PREREGISTRATION.md",
+        "src/zcosmo/cosmosac.py"
+      ],
+      "fix": "Common masks are property-specific; LLE has distinct detection/endpoint denominators; CI0 is not equivalence."
+    },
+    {
+      "id": "C15",
+      "start_line": 143,
+      "end_line": 143,
+      "original_sha256": "5047a6434c1f4da26dadc98704b407724ce664694f93948e467ef9c5f9ade4bf",
+      "status": "structural",
+      "claim": "Section number/title",
+      "sources": [],
+      "fix": "Retain review numbering; submission reading order proposed separately."
+    },
+    {
+      "id": "C16",
+      "start_line": 145,
+      "end_line": 147,
+      "original_sha256": "3b235a0b14ca5f33b883cfa8b2b2f825e74ab866311d4484e3e759c1cb0c9c0e",
+      "status": "asset_metadata_checked",
+      "claim": "Five figure filenames",
+      "sources": [
+        "scripts/make_figures.py"
+      ],
+      "fix": "All five files exist in manuscript/figures; metadata only, not a pixel/data audit. Safe regeneration only2/3 from public aggregates."
+    },
+    {
+      "id": "C17",
+      "start_line": 149,
+      "end_line": 149,
+      "original_sha256": "0f1ca9310a84c58c9554baba26412d459afef21e40f2136cb1d516aae5aff09f",
+      "status": "structural",
+      "claim": "Section number/title",
+      "sources": [],
+      "fix": "Retain review numbering; submission reading order proposed separately."
+    },
+    {
+      "id": "C18",
+      "start_line": 151,
+      "end_line": 153,
+      "original_sha256": "40077f76d7cd2484ce0a37c14b8a2eed3811b3fa652e3d1487412c9da47b34d4",
+      "status": "scope_correction",
+      "claim": "main7 vs composite table provenance",
+      "sources": [
+        "results/scorecard_test_main7.json",
+        "results/scorecard_test_main7.md",
+        "results/scorecard_test_both_main7.md",
+        "PROGRESS.md"
+      ],
+      "fix": "Label first table composite: main7 property entries, test_both column, historical BA summary and separate HANNA row."
+    },
+    {
+      "id": "C19",
+      "start_line": 155,
+      "end_line": 164,
+      "original_sha256": "1ec04cbabc44f1826bee285346c282e7a20c7ac1fbed98297a880d39918b6531",
+      "status": "partially_verified",
+      "claim": "All cells in historical8-model table",
+      "sources": [
+        "results/scorecard_test_main7.json",
+        "results/scorecard_test_main7.md",
+        "results/scorecard_test_both_main7.md",
+        "PROGRESS.md"
+      ],
+      "fix": "Preserve exact table. Seven-model IDAC/VLE/HE cells and both-unseen cells match after rounding. BA precision/HANNA row require original artifacts, explicitly qualified inS0."
+    },
+    {
+      "id": "C20",
+      "start_line": 166,
+      "end_line": 168,
+      "original_sha256": "17d033f6943fe4f0de4273b6b995144d370d73c80e9497674f5b2c4e15fd2b9c",
+      "status": "partially_verified",
+      "claim": "708/163;55/12;9432;101/128;HANNA762",
+      "sources": [
+        "results/scorecard_test_main7.json",
+        "results/scorecard_test_main7.md",
+        "results/scorecard_test_both_main7.md",
+        "PROGRESS.md"
+      ],
+      "fix": "Add confirmed6311HE count; do not assign a762IDAC count to HANNA VLE/HE. Exact early detection/HANNA arrays not recovered."
+    },
+    {
+      "id": "C21",
+      "start_line": 170,
+      "end_line": 175,
+      "original_sha256": "ad370f2512c55a5899029c64519b5c47b516d128f5d5c1717f59644d0bc91099",
+      "status": "mismatch_and_unverified_precision",
+      "claim": "Z0IDAC[-.17,+.08],both[-.54,-.22],VLE[6.6,14.5];LLE/HANNApreciseCIs",
+      "sources": [
+        "results/scorecard_test_main7.json",
+        "results/scorecard_test_main7.md",
+        "results/scorecard_test_both_main7.md",
+        "results/scorecard_test_main6.md",
+        "results/scorecard_test.md",
+        "PROGRESS.md"
+      ],
+      "fix": "Use main7[-.170,+.069],test_both[-.552,-.229],VLE[6.76,14.61]. Preserve old strings inS0. Exact early LLE/HANNA CIs remain unverified; do not call CI0 a tie."
+    },
+    {
+      "id": "C22",
+      "start_line": 177,
+      "end_line": 177,
+      "original_sha256": "c6d7a2b62b0da8f1d234d0119f04abeaeb950c7fe06c28859a476e0e9369e3af",
+      "status": "structural",
+      "claim": "Section number/title",
+      "sources": [],
+      "fix": "Retain review numbering; submission reading order proposed separately."
+    },
+    {
+      "id": "C23",
+      "start_line": 179,
+      "end_line": 188,
+      "original_sha256": "66de13a7e03fa5cb1bddcf5d2b282c7ffd4985c005092996eed5d450939b1063",
+      "status": "verified_source",
+      "claim": "Every temporal8-model table cell",
+      "sources": [
+        "results/scorecard_temporal_ext.md"
+      ],
+      "fix": "Preserve verbatim; correct rounded values on this separate common subset."
+    },
+    {
+      "id": "C24",
+      "start_line": 190,
+      "end_line": 193,
+      "original_sha256": "96bb138df7380970c474b6d192a5ff4379ec536459c818d1545694302c0320d7",
+      "status": "scope_correction",
+      "claim": "254/54IDAC;7722VLE;2058HE;Z0xVLECI[1.2,3.3]",
+      "sources": [
+        "results/scorecard_temporal_ext.md"
+      ],
+      "fix": "Counts and CIrounding agree. Means/medians alone do not count how many large misses dominate."
+    },
+    {
+      "id": "C25",
+      "start_line": 195,
+      "end_line": 195,
+      "original_sha256": "b489b55c23566f292a73394093c4e2824036f9064febe866d5f68f6999c5b32b",
+      "status": "structural",
+      "claim": "Section number/title",
+      "sources": [],
+      "fix": "Retain review numbering; submission reading order proposed separately."
+    },
+    {
+      "id": "C26",
+      "start_line": 197,
+      "end_line": 201,
+      "original_sha256": "782c9804116ed6cd0215d26f487a635f1c96eed8c823f7f681dc09605b7b9679",
+      "status": "verified_source",
+      "claim": "HB5/7/5;5712+/-538,5988+/-1032,5611+/-1833;4014/3016/932",
+      "sources": [
+        "results/qc/hb_constants_by_class.csv",
+        "src/zcosmo/cosmosac.py"
+      ],
+      "fix": "Preserve exact table; +/- values are sampleSD across dimers, notCI."
+    },
+    {
+      "id": "C27",
+      "start_line": 203,
+      "end_line": 206,
+      "original_sha256": "a137a13bca5d386a358a9552a227895ad3ca8360a3ade405c3acc65c9bc5bf15",
+      "status": "scope_correction",
+      "claim": "5CCSDT/CBS estimates;.33-.85mean.59about15%;.05IDAC/1ppHBsensitivity",
+      "sources": [
+        "results/qc/ccsdt_check.csv",
+        "results/scorecard_test_sensitivity.md",
+        "PROGRESS.md"
+      ],
+      "fix": "Name composite CBSestimate, not exactbasislimit. Perturbation bounds describe testedvariants only."
+    },
+    {
+      "id": "C28",
+      "start_line": 208,
+      "end_line": 217,
+      "original_sha256": "4cef5753b83fdc12d4c3f2d25f150fbc3ed2b3cb46698df1e775234ed35d7f08",
+      "status": "scope_correction",
+      "claim": "Old ablation+.03/+.13/+.17IDAC,+6VLE;family.18/.40/1.05,.66/1.04,3.7/3.4",
+      "sources": [
+        "results/scorecard_all_ablation.md",
+        "results/error_map_idac_all_long.csv"
+      ],
+      "fix": "Old all-data startingdsp notZ0x. LondonVLEpointdecrease unresolved. Familylabelalkene/alkyne andcounts146/456/38/27, not universal mostaccurate."
+    },
+    {
+      "id": "C29",
+      "start_line": 219,
+      "end_line": 230,
+      "original_sha256": "6e92c0791bcc580938d520235028b0e1e6964679dae32ad4d8f87ba043fc69ba",
+      "status": "partially_verified",
+      "claim": "Z0w.97/.80;27.4/15.2VLE;.094FP;.90BA;aqueous5-7;nonaq.67/.88;entropy-121/-87",
+      "sources": [
+        "results/scorecard_test_z0w.md",
+        "results/qc/assoc_thermo.csv",
+        "PROGRESS.md",
+        "PREREGISTRATION.md"
+      ],
+      "fix": "Main uses verified .969/.800[-.035,+.400]. Move detailed historical claims toS3; exact posthoc CIs[-.29,-.09],[-.17,+.04] require private existing artifact. Aqueous diagnosis not proof of uniquecause."
+    },
+    {
+      "id": "C30",
+      "start_line": 232,
+      "end_line": 239,
+      "original_sha256": "b52e7389e6fef931bd5dfc235bd8fe9d38ae3b4a30cc2a9ba5609a2b19dd1a62",
+      "status": "public_record",
+      "claim": "v125/2302;.153/.15,water1.14,TEG.84;MAE.79/.74;gap136,218/72and6scores",
+      "sources": [
+        "PREREGISTRATION.md",
+        "results/scorecard_all_gap_exploratory.md",
+        "PROGRESS.md"
+      ],
+      "fix": "Move toS1. Target2302 is historical occurrence denominator, not proof allfinite; gatecompatibility not equivalence;136computed not218uniquecompounds."
+    },
+    {
+      "id": "C31",
+      "start_line": 241,
+      "end_line": 249,
+      "original_sha256": "e8f131d8a9cc36e036f0aa9514260d534d794352531e3fd8fc3551d2c2010dd5",
+      "status": "public_record",
+      "claim": "v2.1493 margin.0007;630+6;R2-R9;P32failure",
+      "sources": [
+        "PREREGISTRATION.md",
+        "docs/astra/round2/RESULTS.md",
+        "docs/astra/round3/RESULTS.md",
+        "docs/astra/round4/RESULTS.md",
+        "docs/astra/round7/RESULTS.md",
+        "docs/astra/round8/RESULTS.md",
+        "docs/astra/round9/RESULTS.md"
+      ],
+      "fix": "Main oneparagraph and S1detail. Keeporiginalgradient stationarityscope, Aoptimizerstateclassification and failedgate."
+    },
+    {
+      "id": "C32",
+      "start_line": 251,
+      "end_line": 257,
+      "original_sha256": "60c00f78b9eeae9da61ef18e3782790215243e567066a92f39575a6e544aa4e3",
+      "status": "private_precision_unverified",
+      "claim": "50molecules244confsavg4.9;medians.009/.011,p90<.09,CI[.00,.01]/[-.35,.32],weight60%",
+      "sources": [
+        "PROGRESS.md",
+        "PREREGISTRATION.md"
+      ],
+      "fix": "Publiclog supports50/244and~.01; detailedqueuefile absent from audit. Retain preciselegacyclaims inS2withpendingartifactlabel; no assertionofequivalence."
+    },
+    {
+      "id": "C33",
+      "start_line": 259,
+      "end_line": 263,
+      "original_sha256": "7f07b6f474612b2b69b480b6f91185e2f070b08e1ec753d2b45467df524db757",
+      "status": "public_record",
+      "claim": "12lineages;EG/DEG/TEGtailgeometry;tetraexception;no fullprofilelabel",
+      "sources": [
+        "docs/astra/round10/RESULTS.md",
+        "docs/astra/round11/RESULTS.md"
+      ],
+      "fix": "Move detail toS2; orderedcross includesH/orientation, not independently identified liquidconformation."
+    },
+    {
+      "id": "C34",
+      "start_line": 265,
+      "end_line": 273,
+      "original_sha256": "333d1b574b94dd504d514ceea2830977176ef09e28c8b6aa124fb0e024ba9876",
+      "status": "public_record",
+      "claim": "142;1.813/.702/.419;1.111;80%gap61%own;139/3;13%;.283",
+      "sources": [
+        "docs/astra/round12/RESULTS.md",
+        "docs/astra/round13/RESULTS.md"
+      ],
+      "fix": "Preserve exact meaning and endpoint. .283 is differenceofMAEs notmeanpredictiondifference oruniversalmethodeffect."
+    },
+    {
+      "id": "C35",
+      "start_line": 275,
+      "end_line": 279,
+      "original_sha256": "a5ce724986e5ac5b942218999d822aa0b65a07d727f612bdf8fc352d64d60643",
+      "status": "public_record",
+      "claim": "R10-R13empiricalUDhistory,P35closeout,630+6",
+      "sources": [
+        "docs/astra/round10/RESULTS.md",
+        "docs/astra/round11/RESULTS.md",
+        "docs/astra/round12/RESULTS.md",
+        "docs/astra/round13/RESULTS.md"
+      ],
+      "fix": "Preserve scope; database-level conformation revision does not identify individualglycolselection."
+    },
+    {
+      "id": "C36",
+      "start_line": 281,
+      "end_line": 281,
+      "original_sha256": "c66ee660648c1e5c8f7dccac03c5c8824bc64d63a705039b2e8f1bd5a6da8c5b",
+      "status": "structural",
+      "claim": "Section number/title",
+      "sources": [],
+      "fix": "Retain review numbering; submission reading order proposed separately."
+    },
+    {
+      "id": "C37",
+      "start_line": 283,
+      "end_line": 290,
+      "original_sha256": "17b6ac2c277f87b4806ceca174e0d64398da28bcb69ffa663121de698a6bc001",
+      "status": "public_record",
+      "claim": "w2.9-2.1solvation,.902/.800CI.04-.18BA.887,13%donors",
+      "sources": [
+        "PREREGISTRATION.md",
+        "PROGRESS.md"
+      ],
+      "fix": "Numerics supportedrecord; failedcriterion stands. Approximate85%liquid reference not newly independentlyvalidated; later temporal is nowexposed."
+    },
+    {
+      "id": "C38",
+      "start_line": 292,
+      "end_line": 292,
+      "original_sha256": "3b31df675aa6d4d39e02f877e4528158f479e73cf848e8b598aa126af9affa6a",
+      "status": "structural",
+      "claim": "Section number/title",
+      "sources": [],
+      "fix": "Retain review numbering; submission reading order proposed separately."
+    },
+    {
+      "id": "C39",
+      "start_line": 294,
+      "end_line": 312,
+      "original_sha256": "479caa4ec5b234973719ba3c3773fb31b7ba8314563d0e71c2e1ee2053a9fce7",
+      "status": "public_record",
+      "claim": "MACE.37ns/day648;force2-4e-6;8.9~24x;TF32.003;HMR2.3-183;21liquidstates;w3errors",
+      "sources": [
+        "PREREGISTRATION.md",
+        "PROGRESS.md"
+      ],
+      "fix": "Move infrastructuretoS3. Exactforcepath checks notequilibrium sampling/chemicalpotential validation; distinct w3temporaldenominator; physicaldiagnosis remainshypothesis."
+    },
+    {
+      "id": "C40",
+      "start_line": 314,
+      "end_line": 319,
+      "original_sha256": "1f855ef8aa1cf8b062b19638e5ea7986a7ce23ffed2d7acce3d7a2daa24d53a0",
+      "status": "public_record",
+      "claim": "P6dispatch,P28endpoint,P55restoration",
+      "sources": [
+        "docs/astra/round14/RESULTS.md",
+        "docs/astra/round15/RESULTS.md"
+      ],
+      "fix": "Retain historicalassociationpredictions unaffected; repairno newscore and no exactassociationendpoint."
+    },
+    {
+      "id": "C41",
+      "start_line": 321,
+      "end_line": 321,
+      "original_sha256": "fbe852ce1ba99bed234ffcaf97fa1a9e8b604f4e22802158f0c3c3e8c8e2bb8a",
+      "status": "structural",
+      "claim": "Section number/title",
+      "sources": [],
+      "fix": "Retain review numbering; submission reading order proposed separately."
+    },
+    {
+      "id": "C42",
+      "start_line": 323,
+      "end_line": 327,
+      "original_sha256": "c54905a9fb837dd4b733898ea162beee52ade9f0773407221b25d5005a489766",
+      "status": "public_record",
+      "claim": "P51742/248validplus5matchedinvalid,298.15K",
+      "sources": [
+        "docs/astra/round14/RESULTS.md"
+      ],
+      "fix": "Registeredaggregatewithheld correctly; do notsubstitute matched-onlydescriptives."
+    },
+    {
+      "id": "C43",
+      "start_line": 329,
+      "end_line": 336,
+      "original_sha256": "11ee0eabc970743c18181d2fb97da6cb01c667ef8aa0c840e6d87925e851e827",
+      "status": "public_record",
+      "claim": "P52963/100;2889;13.78/13.07/10.44;equal13.90/13.19/10.65;.72/21%/3.35;559/404",
+      "sources": [
+        "docs/astra/round14/RESULTS.md"
+      ],
+      "fix": "All agree atrecordprecision. Independentlyroundedendpoints may differ from unrounded difference. Fixed298epsilon notfullε(T)."
+    },
+    {
+      "id": "C44",
+      "start_line": 338,
+      "end_line": 341,
+      "original_sha256": "608d77cf9875c352786297df5917ebe5507f33034654428a5be02990d9e1c4d3",
+      "status": "public_record",
+      "claim": "P52notfitfree;main7different14.15/8.62",
+      "sources": [
+        "docs/astra/round14/RESULTS.md"
+      ],
+      "fix": "Preserve diagnosticandnoheadroombound labels; noportfolioMDauthorization."
+    },
+    {
+      "id": "C45",
+      "start_line": 343,
+      "end_line": 343,
+      "original_sha256": "057a9aea0fc64dd941d33541ccaecbc8f1eb1e1a0d7b568d34e8265c1f0f6cf2",
+      "status": "structural",
+      "claim": "Section number/title",
+      "sources": [],
+      "fix": "Retain review numbering; submission reading order proposed separately."
+    },
+    {
+      "id": "C46",
+      "start_line": 345,
+      "end_line": 350,
+      "original_sha256": "b5a4399ec2c38e4e95d433feb097da21c73f425c3b2778725730d3e4d8853af4",
+      "status": "public_record",
+      "claim": "963/100;8EHDcorners;2dummyfactors",
+      "sources": [
+        "docs/astra/round15/RESULTS.md",
+        "docs/astra/round16/RESULTS.md"
+      ],
+      "fix": "Preserve retrospective intervention definition; dummyzerosonlybetween specifiedendpoints."
+    },
+    {
+      "id": "C47",
+      "start_line": 352,
+      "end_line": 361,
+      "original_sha256": "ed56c3b78f0f93b2d8888e59f25cdae46e8ce247818a82169ccea52c84863f74",
+      "status": "verified_source",
+      "claim": "All eight P54cornerAAD/bias/equal-systemvalues",
+      "sources": [
+        "docs/astra/round15/RESULTS.md"
+      ],
+      "fix": "Preserve exact table."
+    },
+    {
+      "id": "C48",
+      "start_line": 363,
+      "end_line": 369,
+      "original_sha256": "f1c1d880c9133c42de6db6b6ea0fce4f40daac3346e4dc501d3ee68597ce8855",
+      "status": "public_record",
+      "claim": "2.24/67%,.88/26%,.23/7%;3.35gap;HD+.95ED-.43",
+      "sources": [
+        "docs/astra/round15/RESULTS.md"
+      ],
+      "fix": "Preserve conditionalShapleyerrorallocation, not causalenergypercent."
+    },
+    {
+      "id": "C49",
+      "start_line": 371,
+      "end_line": 375,
+      "original_sha256": "c2f3125656ec89162ce4571c05ff90dfab8ae813ed52d2f40be08a2b1b37f03b",
+      "status": "public_record",
+      "claim": "2.02AAD;onefactorbias-4.23versusShapley-4.47",
+      "sources": [
+        "docs/astra/round15/RESULTS.md",
+        "docs/astra/round16/RESULTS.md"
+      ],
+      "fix": "Currentclarificationcorrect; retain. No roundingexplanation forconflatingdifferentstatistics."
+    },
+    {
+      "id": "C50",
+      "start_line": 377,
+      "end_line": 381,
+      "original_sha256": "ceab9a321b892269e788170aa2ee88e6758badf9338301266a99e3a80575b129",
+      "status": "public_record",
+      "claim": "7704finite1926anchors3e-14efficiency722s",
+      "sources": [
+        "docs/astra/round15/RESULTS.md"
+      ],
+      "fix": "Preserve measuredaccounting; portabletestqualificationnotallMacsummarypass."
+    },
+    {
+      "id": "C51",
+      "start_line": 383,
+      "end_line": 386,
+      "original_sha256": "54ebdfd362af926e5abd2eba1c2faa4515b1ee3c42c13b86f790151cbd79e906",
+      "status": "public_record",
+      "claim": "21%eps andESshareoverlap;630+6",
+      "sources": [
+        "docs/astra/round14/RESULTS.md",
+        "docs/astra/round15/RESULTS.md"
+      ],
+      "fix": "Preserve nonadditivity,noadoption;appendLV1failure tosame3.11section."
+    },
+    {
+      "id": "C52",
+      "start_line": 388,
+      "end_line": 388,
+      "original_sha256": "df2c73358e96e3e08ad73bed73e9e674d0cd21f6a0e8b18785469899127b57b2",
+      "status": "structural",
+      "claim": "Section number/title",
+      "sources": [],
+      "fix": "Retain review numbering; submission reading order proposed separately."
+    },
+    {
+      "id": "C53",
+      "start_line": 390,
+      "end_line": 393,
+      "original_sha256": "fda53fdb593bfb499889b338fc3a6f514c287ad864563ed532e260cd2410ea1c",
+      "status": "scope_correction",
+      "claim": "Z0xVLEworse main7/temporal",
+      "sources": [
+        "results/scorecard_test_main7.json",
+        "results/scorecard_test_main7.md",
+        "results/scorecard_temporal_ext.md"
+      ],
+      "fix": "Preserveproperty-dependentusefulness; avoidgeneralcompetitiveorzeroempiricismclaim."
+    },
+    {
+      "id": "C54",
+      "start_line": 395,
+      "end_line": 401,
+      "original_sha256": "6323612483793c58e42a19452eff10dc633af1db16b0bcd6094a310267036061",
+      "status": "public_record",
+      "claim": "P54leadingZ0xexplanation,R14smalllever",
+      "sources": [
+        "docs/astra/round14/RESULTS.md",
+        "docs/astra/round15/RESULTS.md"
+      ],
+      "fix": "Keepconditionalclosureattribution; notuniquedoublecountingoronegeometrycause."
+    },
+    {
+      "id": "C55",
+      "start_line": 403,
+      "end_line": 411,
+      "original_sha256": "ec0b9b4c2da16765d7720cb3dce7a6ac30f12f103b65ac7544dc52b00153e0e0",
+      "status": "reasoning_and_stale_status",
+      "claim": "C6positive Londonnonnegative; prospectivealternative language",
+      "sources": [
+        "src/zcosmo/cosmosac.py",
+        "docs/astra/round16/RESULTS.md"
+      ],
+      "fix": "Keepalreadyreportedalgebra restriction, notpositiverow-errorclaim. ReplaceprospectiveLV1text bycomplete failedscreen."
+    },
+    {
+      "id": "C56",
+      "start_line": 421,
+      "end_line": 428,
+      "original_sha256": "de21cff7071df8b74ac9c3ef51be8f1235cf82233f18f3f851f4c912615ef204",
+      "status": "stale_status",
+      "claim": "P54papercentrepiece,optionalfutureLV1screen",
+      "sources": [
+        "docs/astra/round16/RESULTS.md"
+      ],
+      "fix": "Screenalreadyranandfailed. Close modeldevelopment; editorialsourcechecks only; no proposedvariant."
+    },
+    {
+      "id": "C57",
+      "start_line": 430,
+      "end_line": 430,
+      "original_sha256": "bc1a7012243c4ecaa5594725f9221acf9d24259daeb30397358dd793d039cfe0",
+      "status": "structural",
+      "claim": "Section number/title",
+      "sources": [],
+      "fix": "Retain review numbering; submission reading order proposed separately."
+    },
+    {
+      "id": "C58",
+      "start_line": 432,
+      "end_line": 436,
+      "original_sha256": "9536bda01a7d00edc70cc3172ef5d43506a72a02181b0e3c7fc35b98c3f464bb",
+      "status": "public_record",
+      "claim": "Z0/Z0xnofitting,Z0strainchoice,Z1fitted",
+      "sources": [
+        "PREREGISTRATION.md",
+        "docs/astra/round14/RESULTS.md",
+        "docs/astra/round15/RESULTS.md"
+      ],
+      "fix": "Preserve andaddsoftware/weightversioncitations pending. EmpiricalPsat andprofileconventions remain."
+    },
+    {
+      "id": "C59",
+      "start_line": 438,
+      "end_line": 441,
+      "original_sha256": "2f3cdbbeb0cf38e1faff210a7d0e6ed90a3969a2fb7a10b7f0fefaceff6be777",
+      "status": "public_record",
+      "claim": "2017-2019exposure,bootstrapgenerality",
+      "sources": [
+        "PREREGISTRATION.md",
+        "docs/astra/round16/RESULTS.md"
+      ],
+      "fix": "Preserveexposure;R16CIs exposedwithincollectionresampling notrestoredholdout."
+    },
+    {
+      "id": "C60",
+      "start_line": 443,
+      "end_line": 447,
+      "original_sha256": "c6125f80c9e3f8d175616fa9e79811e43985695b6842ce2ce7604c14af88f0e2",
+      "status": "public_record",
+      "claim": "630+6,correctedgradient/ensemble/certification limits",
+      "sources": [
+        "docs/astra/round7/RESULTS.md",
+        "docs/astra/round8/RESULTS.md",
+        "docs/astra/round9/RESULTS.md",
+        "docs/astra/round13/RESULTS.md"
+      ],
+      "fix": "Preserve limits andclosedstatus."
+    },
+    {
+      "id": "C61",
+      "start_line": 451,
+      "end_line": 455,
+      "original_sha256": "d6cdbeb938a9e331946db6296feb0a9ad10a7cb0248f4d8b15aab397a307c7ee",
+      "status": "asset_scope",
+      "claim": "R10-R15privateartifacts",
+      "sources": [
+        "PREREGISTRATION.md",
+        "docs/astra/round16/RESULTS.md"
+      ],
+      "fix": "Extend toR16; publiccheckoutnotfullprivate-table reproduction. No redistributionornewscoring."
+    },
+    {
+      "id": "C62",
+      "start_line": 459,
+      "end_line": 461,
+      "original_sha256": "35604e1a8701f39b2e50517902bc99a4beae415d6004556cb61673bad267e9c9",
+      "status": "asset_metadata_checked",
+      "claim": "Fig1762/177parityandHANNAoverlap",
+      "sources": [
+        "scripts/make_figures.py"
+      ],
+      "fix": "Imageexists butrows/masknotpixelverified. Existingprivatepredictionfilesneededfororiginalplot. No regenerationusingmodelcalls."
+    },
+    {
+      "id": "C63",
+      "start_line": 463,
+      "end_line": 464,
+      "original_sha256": "ab7a8429887d2d9b76edf167c8b346a218d67a2d7321ce833412c52d1bfe1eb3",
+      "status": "asset_metadata_checked",
+      "claim": "Fig217dimers/meansvsfitted",
+      "sources": [
+        "results/qc/hb_constants_per_dimer.csv",
+        "results/qc/hb_constants_by_class.csv"
+      ],
+      "fix": "Imageexists. Newpublic-only helpercanrender fromcommittedCSV without touchingpredictioncode; notbyteidenticalclaim."
+    },
+    {
+      "id": "C64",
+      "start_line": 466,
+      "end_line": 469,
+      "original_sha256": "bc49669039114ffad228e398094bc283d8d6a14e1dca9a469817f2822a770737",
+      "status": "asset_metadata_checked",
+      "claim": "Fig3tradeofffrommain7pointestimates",
+      "sources": [
+        "results/scorecard_test_main7.json",
+        "results/scorecard_test_main7.md",
+        "scripts/make_figures.py"
+      ],
+      "fix": "Imageexists. Newhelperreads storedmeans only; nobootstraporrescoring; eachaxisownpropertymask."
+    },
+    {
+      "id": "C65",
+      "start_line": 471,
+      "end_line": 472,
+      "original_sha256": "5dd4338e207a32b60f5f4124e23f32c8a2c56f354d6a7a49b37659031e203f2b",
+      "status": "asset_metadata_checked",
+      "claim": "Fig4LLErecall/FPR",
+      "sources": [
+        "scripts/make_figures.py"
+      ],
+      "fix": "Imageexists,privatearraysrequired. OneoperatingpointpermodelnotfullROC;exportarchivedbytes onlyinR17."
+    },
+    {
+      "id": "C66",
+      "start_line": 474,
+      "end_line": 475,
+      "original_sha256": "58220e00d2f85051bc990eb54df23aa756ac244efda83433af83b25cd73e9f5b",
+      "status": "asset_metadata_checked",
+      "claim": "Fig5familycellsn>=10",
+      "sources": [
+        "scripts/make_figures.py",
+        "results/error_map_idac_all_long.csv"
+      ],
+      "fix": "Imageexists. CommittedfamilyCSVmayhaveothercommonmask; donotrebrandalternativeaggregaterenderasoriginalregeneration."
+    },
+    {
+      "id": "C67",
+      "start_line": 479,
+      "end_line": 487,
+      "original_sha256": "9f766d4988452777d8427c061b036a73484866f1059889a6f9cc1299b5148117",
+      "status": "asset_scope",
+      "claim": "S1-S7sourceinventorythroughR15",
+      "sources": [
+        "PREREGISTRATION.md",
+        "docs/astra/round16/RESULTS.md"
+      ],
+      "fix": "UpdatethroughR16,addactualsupplementandclaimledger; detailedprivateassetsnotrepresentedaspresentpublicdata."
+    },
+    {
+      "id": "C68",
+      "start_line": 491,
+      "end_line": 520,
+      "original_sha256": "04ff473c7aa57224647ea52664d8aca20728f4a896430e4fd67d63cc25429300",
+      "status": "reference_audit",
+      "claim": "Every reference1-17year/volume/pageandDOI",
+      "sources": [
+        "REFERENCES.md"
+      ],
+      "fix": "Bibliographyauditall17. Correct9to2003Part1;name12series;verifiedDOIs,flag10and13directpublishercheck,5corrigendumcontent andsoftwarecitations."
+    }
+  ],
+  "figures": [
+    {
+      "path": "manuscript/figures/fig1_idac_parity_test.png",
+      "blob": "72659886f5d3b451cf00adfe536a3715b1d6553a",
+      "bytes": 164834,
+      "pixels_inspected": false
+    },
+    {
+      "path": "manuscript/figures/fig2_hbond_constants.png",
+      "blob": "c22a980ff1e3266e8865b84a2bac9c9deebe6367",
+      "bytes": 36908,
+      "pixels_inspected": false
+    },
+    {
+      "path": "manuscript/figures/fig3_tradeoff.png",
+      "blob": "62205ae989a86687abf91d99bdd9b1010d7cb46a",
+      "bytes": 45885,
+      "pixels_inspected": false
+    },
+    {
+      "path": "manuscript/figures/fig4_lle_detection.png",
+      "blob": "03560344877b0867a97b806b7014ebb477a7d8b5",
+      "bytes": 44921,
+      "pixels_inspected": false
+    },
+    {
+      "path": "manuscript/figures/fig5_error_map.png",
+      "blob": "78e50e66d2dc842667e0ed5aa2a9e42a42a7fece",
+      "bytes": 78089,
+      "pixels_inspected": false
+    }
+  ],
+  "meanings": {
+    "coverage": "Every original digit-bearing paragraph is indexed. This is mechanical completeness, not proof of semantic correctness.",
+    "public_record": "Correspondence with already published aggregate prose, without recomputing its private scientific data."
+  },
+  "submission_ready": false,
+  "open_items": [
+    "Recover existing source-specific early LLE bootstrap output, negative-state selection and endpoint composition denominators before retaining precise inferential claims.",
+    "Recover existing historical HANNA test scorecard and model-weight/version receipt; do not infer its per-property subsets from 762 IDAC observations.",
+    "Recover the already-produced private conformer and post-hoc association outputs before treating their precise draft-only intervals as verified.",
+    "Complete reference10 publisher/title/pages, reference13 directpublisher, and reference5 corrigendum text checks; add exact software/data/modelversioncitations.",
+    "Inspect archived figurepixels and pairfigures1/4/5 with their original input hashes and masks; do not rescore."
+  ],
+  "new_experiments_authorized": false,
+  "edited_sources": {
+    "README.md": "b3d8e59050e8a70fb627e4a67eee408427b119e020b597cdef082505581dae35"
+  }
+}
diff --git a/docs/astra/round17/REFERENCES.md b/docs/astra/round17/REFERENCES.md
new file mode 100644
index 0000000..fc03122
--- /dev/null
+++ b/docs/astra/round17/REFERENCES.md
@@ -0,0 +1,60 @@
+# R17 bibliography and figure-source audit
+
+This is an editorial audit, not a new literature-selected model. Bibliographic identity and the contents
+of a paper are different checks. A publisher metadata record can establish a DOI and page range without
+validating every scientific claim attributed to the paper. The original reference numbers are retained.
+Issue-publication years are used instead of later digitization dates or earlier online dates.
+
+| Reference | Metadata established | Primary location | Remaining issue / manuscript action |
+|---|---|---|---|
+| 1, Klamt | J. Phys. Chem. 1995, 99(7), 2224-2235 | https://doi.org/10.1021/j100007a062 | Expand title and pages. Do not use the website's 2002 digitization date as the publication year. |
+| 2, Lin and Sandler | Ind. Eng. Chem. Res. 2002, 41(5), 899-913 | https://doi.org/10.1021/ie001047w | Add DOI and the related 2004 correction, 43(5), 1322, https://doi.org/10.1021/ie0308689. No inference that current 2010 code is affected without checking its equations. |
+| 3, Mullins et al. | Ind. Eng. Chem. Res. 2006, 45(12), 4389-4415 | https://doi.org/10.1021/ie060370h | Add full range and DOI; distinguish this database publication from the project's UD inventory. |
+| 4, Hsieh et al. | Fluid Phase Equilib. 2010, 297(1), 90-97 | https://doi.org/10.1016/j.fluid.2010.06.011 | Add exact DOI/range; model constants remain those of the pinned implementation. |
+| 5, Hsieh et al. | Fluid Phase Equilib. 2014, 367, 109-116 | https://doi.org/10.1016/j.fluid.2014.01.032 | A corrigendum exists at 384, 14-15, DOI 10.1016/j.fluid.2014.10.019. Its author-institution record is verified; original publisher text and implications remain outstanding. |
+| 6, Bell et al. | J. Chem. Theory Comput. 2020, 16(4), 2635-2646 | https://pubs.acs.org/doi/abs/10.1021/acs.jctc.9b01016 | Complete citation verified at ACS. Its 2,261-compound distribution count is distinct from the project's reported 2,259-entry inventory. |
+| 7, Gmehling et al. | Ind. Eng. Chem. Res. 1993, 32(1), 178-193 | https://doi.org/10.1021/ie00013a024 | Cite the actual 2016 parameter update as well; the 1993 paper alone does not identify the DOUFIP2016 software table. |
+| 8, Hoffmann et al. | Nat. Commun. 2026, 17, 3485; published 14 April 2026 | https://www.nature.com/articles/s41467-026-71430-y | Publisher gives 824,481 data points. The project still needs its deployed weight/version receipt and row-overlap scope; publication metadata does not recover those. |
+| 9, Frenkel et al. | Part 1 is J. Chem. Eng. Data 2003, 48(1), 2-13 | https://pubs.acs.org/doi/abs/10.1021/je025645o | Replace the draft's unspecific 2006, 51, 1504 series placeholder with this identified Part 1 article. Online December 2002 does not change the 2003 issue citation. |
+| 10, Herington | The draft identifies J. Inst. Petrol. 1951, 37, 457 | No original publisher record recovered | Keep explicitly provisional. Title and complete range need a primary archival record; do not manufacture a DOI. A later paper citing these coordinates is not the original source. |
+| 11, Onsager | J. Am. Chem. Soc. 1936, 58(8), 1486-1493 | https://doi.org/10.1021/ja01299a050 | Complete DOI and range; the implementation's convention needs its own code citation. |
+| 12, Wertheim I-IV | 1984, 35, 19-34 and 35-47; 1986, 42, 459-476 and 477-492 | https://doi.org/10.1007/BF01017362 ; https://doi.org/10.1007/BF01017363 ; https://doi.org/10.1007/BF01127721 ; https://doi.org/10.1007/BF01127722 | Replace the incomplete parenthetical series reference with explicit I-IV identities. These papers do not validate the project's particular site mapping or inversion. |
+| 13, Caldeweyher et al. | J. Chem. Phys. 2019, 150(15), 154122, DOI 10.1063/1.5090222 | https://www.cambridge.org/engage/chemrxiv/article-details/60c74060f96a006646286291 | Author preprint/version-of-record link supports identity. Direct AIP publisher retrieval was unsuccessful, so direct publisher verification stays open. Do not cite a preprint DOI as the final journal DOI. |
+| 14, Bannwarth et al. | J. Chem. Theory Comput. 2019, 15(3), 1652-1671 | https://doi.org/10.1021/acs.jctc.8b01176 | Complete GFN2-xTB title, DOI and range; actual tblite/geometry versions are separate provenance. |
+| 15, Grimme | Chem. Eur. J. 2012, 18(32), 9955-9964 | https://doi.org/10.1002/chem.201200497 | Complete range and DOI. Do not treat model quasi-RRHO thermochemistry as a measured liquid entropy. |
+| 16, Sun et al. | J. Chem. Phys. 2020, 153(2), 024109 | https://doi.org/10.1063/5.0006074 | Complete citation. A package paper does not specify the pinned PySCF 2.14.0 source used in later diagnostics. |
+| 17, Boys and Bernardi | Mol. Phys. 1970, 19(4), 553-566 | https://doi.org/10.1080/00268977000101561 | Use the original DOI and publication year, not a later reprint or digitization. |
+| Added 18, Constantinescu and Gmehling | J. Chem. Eng. Data 2016, 61(8), 2738-2748 | https://doi.org/10.1021/acs.jced.6b00136 | Identify the 2016 update; also record the installed thermo parameter-table revision from existing execution receipts. |
+
+The corrigendum author record is
+https://scholars.ncu.edu.tw/zh/publications/corrigendum-to-considering-the-dispersive-interactions-in-the-cos/ .
+No correction's uninspected contents are asserted here. The complete reference audit uses publisher
+records where accessible and labels the remaining author-record-only or unrecovered identities.
+
+The submission archive should also identify the already-used MACE-OFF23 weight file and its corresponding
+primary publication, along with exact model/software/data versions for PySCF, D4, GFN2-xTB/tblite, RDKit,
+pyberny, thermo/ugropy, HANNA and the ThermoML snapshot. Method citations for the chosen basis/functional
+and numerical integration belong in the supplement. These items must be taken from existing execution
+receipts; R17 does not invent a package version, generate new chemistry or certify an absent model hash.
+This is a finite editorial checklist, not a proposal to acquire a new validation dataset.
+
+## Figure inventory
+
+All five captioned PNG files exist under manuscript/figures at the pinned R17 base. The GitHub tree and
+file metadata were checked, not their pixels or private underlying arrays. There is no caption-only
+figure among those five. No additional P54 or LV1 figure is asserted to exist.
+
+| Figure | Committed file | Git blob | Bytes | What can be done without scoring |
+|---|---|---|---:|---|
+| 1 | fig1_idac_parity_test.png | 72659886f5d3b451cf00adfe536a3715b1d6553a | 164834 | Export existing image. Original regeneration needs the exact historical private prediction CSVs and mask; no regenerated MAE in R17. |
+| 2 | fig2_hbond_constants.png | c22a980ff1e3266e8865b84a2bac9c9deebe6367 | 36908 | Render from committed per-dimer and stored class-mean CSVs using r17_figures.py. |
+| 3 | fig3_tradeoff.png | 62205ae989a86687abf91d99bdd9b1010d7cb46a | 45885 | Render stored main7 IDAC and VLE means using r17_figures.py, with each axis's own denominator. |
+| 4 | fig4_lle_detection.png | 03560344877b0867a97b806b7014ebb477a7d8b5 | 44921 | Export existing image. Original private positive/negative arrays are needed for provenance; one operating point per model is not a full ROC curve. |
+| 5 | fig5_error_map.png | 78e50e66d2dc842667e0ed5aa2a9e42a42a7fece | 78089 | Export existing image. Committed family aggregates are not certified to have the original figure's common mask, so do not relabel an alternative rendering as an exact regeneration. |
+
+The old scripts/make_figures.py reads private prediction files at module import before the public-only
+figure sections. It can also recompute metrics and silently skip absent model inputs. It is therefore
+not the zero-score regeneration command for R17. The isolated helper reads only three fixed public
+files and writes Figures 2 and 3 into a fresh external directory. It promises data-source fidelity,
+not pixel identity with the original plotting environment. Exporting Figures 1, 4 and 5 from the Git
+object preserves their exact original bytes but does not replace their pending source-array audit.
diff --git a/scripts/r17_audit.py b/scripts/r17_audit.py
new file mode 100644
index 0000000..fae505c
--- /dev/null
+++ b/scripts/r17_audit.py
@@ -0,0 +1,171 @@
+"""R17 reporting checks only. Never imports a model or reads prediction/profile data.
+
+Default CLI requires the actual pinned Git objects in an asset-independent checkout.
+A successful mechanical audit is not a claim that all editorial evidence is verified.
+"""
+from __future__ import annotations
+import argparse
+import hashlib
+import json
+import re
+import subprocess
+from decimal import Decimal
+from pathlib import Path
+
+BASE = '35ab60046f3f4a7566d8eeee6b13172a6d0becc2'
+ORIGINAL_BLOB = 'edf2eae2b30fb97b8934c4e86c81a09685e8704d'
+ROOT = Path(__file__).resolve().parents[1]
+
+
+def require(condition: bool, message: str) -> None:
+    if not condition:
+        raise ValueError(message)
+
+
+def blob(data: bytes) -> str:
+    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
+
+
+def sha(data: bytes) -> str:
+    return hashlib.sha256(data).hexdigest()
+
+
+def tables(text: str) -> list[str]:
+    return re.findall(r'(?m)^\|[^\n]*(?:\n\|[^\n]*)+', text)
+
+
+def numeric_blocks(text: str) -> list[tuple[int, int, str]]:
+    result = []
+    for match in re.finditer(r'\S[^\n]*(?:\n(?!\n)[^\n]+)*', text):
+        if re.search(r'\d', match.group()):
+            result.append((text.count('\n', 0, match.start()) + 1,
+                           text.count('\n', 0, match.end()) + 1, match.group()))
+    return result
+
+
+def documents(original: bytes, revised: bytes, supplement: bytes, ledger: dict) -> dict:
+    """Check supplied documents, without implying that external sources were re-read."""
+    require(ledger['base'] == BASE, 'wrong base in claim ledger')
+    require(blob(original) == ORIGINAL_BLOB == ledger['original_blob'], 'original manuscript changed')
+    require(sha(revised) == ledger['revised_sha256'], 'revised manuscript differs from reviewed patch')
+    require(sha(supplement) == ledger['supplement_sha256'], 'supplement differs from reviewed patch')
+    old, new, sup = (x.decode('utf-8') for x in (original, revised, supplement))
+    blocks = numeric_blocks(old)
+    claims = ledger['claims']
+    require(len(blocks) == len(claims), 'missing or additional claim block')
+    require(len({c['id'] for c in claims}) == len(claims), 'duplicate claim id')
+    for (a, b, text), claim in zip(blocks, claims):
+        require((a, b) == (claim['start_line'], claim['end_line']), 'claim location mismatch')
+        require(sha(text.encode()) == claim['original_sha256'], 'claim text mismatch')
+        require(bool(claim['status'] and claim['fix']), 'claim lacks a disposition')
+    old_tables = tables(old)
+    require(all(table in new + '\n' + sup for table in old_tables), 'an original table was changed or lost')
+    lv1 = new.split('#### Registered negative result: LV1\n', 1)
+    require(len(lv1) == 2, 'LV1 result missing')
+    result_text = lv1[1].split('## 4. Discussion', 1)[0]
+    for token in ('[-1.72, +0.13]', '[+0.008, +0.067]', '[+4.6, +25.1]',
+                  '13.13%', '10.44%', '+14.2', '171,701', '51 pure-composition',
+                  'failed the joint registered screen'):
+        require(token in result_text, 'missing LV1 qualification: ' + token)
+    discussion = new.split('## 4. Discussion', 1)[1].split('## 5. Limitations', 1)[0]
+    require('LV1 made that declared change and failed' in discussion, 'discussion omits LV1 failure')
+    require('closed for this project' in discussion, 'project closeout missing')
+    require('No fitted factorial corner' in new, 'no-adoption statement missing')
+    require(ledger['submission_ready'] is False and len(ledger['open_items']) > 0,
+            'unverified editorial items silently marked complete')
+    return dict(numeric_blocks_indexed=len(blocks), original_tables_preserved=len(old_tables),
+                lv1_record_present=True, manuscript_blob_before=blob(original),
+                manuscript_sha256_after=sha(revised), new_model_calls=0, new_QC_calls=0,
+                submission_ready=False, open_items=ledger['open_items'],
+                scope='Mechanical document checks. Claim dispositions are a human source audit, not a proof.')
+
+
+
+def rounded_difference_compatible(left: str, right: str, difference: str, digits: int) -> bool:
+    """Conservative compatibility of independently rounded public values; never a CI."""
+    require(isinstance(digits, int) and 0 <= digits <= 12, 'invalid rounding precision')
+    a, b, d = (Decimal(x) for x in (left, right, difference))
+    require(all(x.is_finite() for x in (a, b, d)), 'nonfinite printed value')
+    half = Decimal(5) * (Decimal(10) ** (-digits - 1))
+    # left - right ranges over +/- 2 half-units; the printed difference over +/- half.
+    return max(a - b - 2 * half, d - half) <= min(a - b + 2 * half, d + half)
+
+
+def safe_relative(path: str) -> None:
+    p = Path(path)
+    require(not p.is_absolute() and '..' not in p.parts and path != '', 'unsafe source path')
+    allowed = (path in ('PREREGISTRATION.md', 'PROGRESS.md', 'README.md', 'manuscript/draft.md') or
+               path.startswith(('docs/astra/', 'results/scorecard_', 'results/error_map_',
+                                'results/qc/', 'src/zcosmo/', 'scripts/', 'manuscript/figures/')))
+    require(allowed and 'predictions' not in p.parts, 'source outside public audit allowlist')
+
+
+def git_bytes(root: Path, path: str) -> bytes:
+    safe_relative(path)
+    return subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=root,
+                                   stderr=subprocess.PIPE)
+
+
+def sources(root: Path, expected: dict[str, str], reviewed_changes: dict | None = None) -> dict:
+    """Read only the hard-coded public sources and compare object and working bytes."""
+    verified = {}
+    for path, digest in expected.items():
+        safe_relative(path)
+        data = git_bytes(root, path)
+        require(blob(data) == digest, 'pinned source object differs: ' + path)
+        target = (root / path).resolve()
+        require(target.is_relative_to(root.resolve()), 'source symlink leaves checkout: ' + path)
+        current = target.read_bytes()
+        if path in (reviewed_changes or {}):
+            require(path == 'README.md' and current.startswith(data)
+                    and sha(current) == reviewed_changes[path], 'reviewed README append differs')
+        elif path == 'PREREGISTRATION.md' and current != data:
+            proposed = (root / 'docs/astra/round17/REGISTRATION_PROPOSED.md').read_bytes()
+            require(current.startswith(data) and proposed in current[len(data):]
+                    and b'Round 17 adopted at ' in current[len(data):],
+                    'historical registration changed or R17 append missing')
+        else:
+            require(current == data, 'working source differs: ' + path)
+        verified[path] = dict(git_blob=digest, bytes=len(data), sha256=sha(data))
+    return verified
+
+
+def fresh_output(path: Path, root: Path) -> Path:
+    path = path.expanduser().resolve()
+    require(not path.is_relative_to(root.resolve()), 'output must be outside the checkout')
+    require(not any((p / '.git').exists() for p in (path, *path.parents)), 'output is inside a Git checkout')
+    path.mkdir(mode=0o700, parents=True, exist_ok=False)
+    return path
+
+
+def run(root: Path, output: Path) -> dict:
+    root = root.resolve()
+    ledger = json.loads((root / 'docs/astra/round17/CLAIMS.json').read_text())
+    require(ledger['base'] == BASE, 'wrong audit base')
+    subprocess.run(['git', 'merge-base', '--is-ancestor', BASE, 'HEAD'], cwd=root,
+                   check=True, capture_output=True)
+    result = documents(git_bytes(root, 'manuscript/draft.md'),
+                       (root / 'manuscript/draft.md').read_bytes(),
+                       (root / 'manuscript/supplement.md').read_bytes(), ledger)
+    result['public_sources_verified'] = sources(root, ledger['sources'], ledger.get('edited_sources'))
+    result['historical_private_statistics_recomputed'] = False
+    result['figure_pixels_reviewed'] = False
+    result['base_commit'] = BASE
+    out = fresh_output(output, root)
+    (out / 'audit.json').write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
+    return result
+
+
+def main() -> None:
+    parser = argparse.ArgumentParser(description=__doc__)
+    parser.add_argument('--root', type=Path, default=ROOT)
+    parser.add_argument('--out', type=Path, required=True)
+    args = parser.parse_args()
+    result = run(args.root, args.out)
+    print(json.dumps(dict(mechanical_checks='passed',
+                          source_objects=len(result['public_sources_verified']),
+                          submission_ready=False, remaining_editorial_items=len(result['open_items']))))
+
+
+if __name__ == '__main__':
+    main()
```
<!-- END PATCH P61 -->

<!-- BEGIN PATCH P62 -->
```diff
diff --git a/scripts/r17_figures.py b/scripts/r17_figures.py
new file mode 100644
index 0000000..8115bee
--- /dev/null
+++ b/scripts/r17_figures.py
@@ -0,0 +1,128 @@
+"""Render only Figures 2 and 3 from pinned public, precomputed quantities.
+
+No prediction files, model imports, bootstrap or new thermodynamic scores.
+Original image files are never overwritten. Raster equality is not claimed.
+"""
+from __future__ import annotations
+import argparse
+import csv
+import io
+import json
+import math
+from pathlib import Path
+from r17_audit import BASE, ROOT, blob, fresh_output, require, sha
+
+INPUTS = {
+    'results/qc/hb_constants_per_dimer.csv': 'bd249aaf7ad01e5fd70a7357766c6db6e5cf1307',
+    'results/qc/hb_constants_by_class.csv': 'fe225ee279fd80fc599c871955011370ddafb5e0',
+    'results/scorecard_test_main7.json': 'aee303792afcdff48e90aa74d074802a3bb7596b',
+}
+CLASSES = ('OH-OH', 'OH-OT', 'OT-OT')
+MODELS = ('unifac_do', 'cosmosac2010', 'cosmosac_dsp', 'Z0', 'Z0e', 'Z0s', 'Z0x')
+FITTED = (4013.78, 3016.43, 932.31)
+NAMES = ('UNIFAC-Do', 'COSMO-SAC 2010', 'COSMO-SAC-dsp', 'Z0', 'Z0e', 'Z0s', 'Z0x')
+
+
+def positive(value: object) -> float:
+    value = float(value)
+    require(math.isfinite(value) and value > 0, 'invalid stored plot quantity')
+    return value
+
+
+def figure2_data(per_dimer: bytes, classes: bytes) -> dict:
+    """Use stored class means, not a newly fitted/re-estimated parameter."""
+    rows = list(csv.DictReader(io.StringIO(per_dimer.decode())))
+    means = list(csv.DictReader(io.StringIO(classes.decode())))
+    require(len(rows) == 17 and len(means) == 3, 'HB table dimensions changed')
+    require(len({r['label'] for r in rows}) == 17, 'duplicate dimer identity')
+    require({r['cls'] for r in means} == set(CLASSES), 'HB class identities changed')
+    groups = {c: [positive(r['c_hb']) for r in rows if r['cls'] == c] for c in CLASSES}
+    counts = [len(groups[c]) for c in CLASSES]
+    require(counts == [5, 7, 5], 'dimer-class counts changed')
+    by = {r['cls']: r for r in means}
+    require([int(by[c]['count']) for c in CLASSES] == counts, 'stored class count mismatch')
+    return dict(classes=list(CLASSES), groups=groups,
+                means=[positive(by[c]['mean']) for c in CLASSES], fitted=list(FITTED), count=17)
+
+
+def figure3_data(scorecard: bytes) -> dict:
+    data = json.loads(scorecard)
+    require(data['split'] == 'test', 'wrong scorecard split')
+    require(set(data['models']) == set(MODELS), 'main7 comparator list changed')
+    idac, vle = data['tables']['idac'], data['tables']['vle']
+    require(idac['n_points'] == 708 and idac['n_systems'] == 163 and vle['n_points'] == 9432,
+            'main7 plot denominators changed')
+    return dict(models=list(MODELS), labels=list(NAMES),
+                IDAC=[positive(idac[m]['MAE_ln_gamma_inf']) for m in MODELS],
+                VLE=[positive(vle[m]['AAD_P_pct']) for m in MODELS],
+                IDAC_rows=708, IDAC_systems=163, VLE_rows=9432)
+
+
+def render2(data: dict, filename: Path) -> None:
+    import matplotlib
+    matplotlib.use('Agg')
+    import matplotlib.pyplot as plt
+    fig, ax = plt.subplots(figsize=(6.8, 4.5))
+    for i, cls in enumerate(data['classes']):
+        # Fixed offsets distinguish points. They do not encode another observation.
+        values = data['groups'][cls]
+        n = len(values)
+        offsets = [0.0] if n == 1 else [-0.10 + 0.20 * j / (n - 1) for j in range(n)]
+        ax.scatter([i + off for off in offsets], values, s=26,
+                   label='Dimer estimates' if i == 0 else None)
+    ax.scatter(range(3), data['means'], marker='_', s=700, linewidths=2.4, label='Stored class mean')
+    ax.scatter(range(3), data['fitted'], marker='D', s=55, label='COSMO-SAC 2010')
+    ax.set_xticks(range(3), data['classes'])
+    ax.set_ylabel(r'$c_{HB}$ (kcal $\mathrm{\AA}^4$ mol$^{-1}$ e$^{-2}$)')
+    ax.set_title('Historical hydrogen-bond coefficients')
+    ax.legend(fontsize=9)
+    fig.tight_layout()
+    fig.savefig(filename, dpi=200)
+    plt.close(fig)
+
+
+def render3(data: dict, filename: Path) -> None:
+    import matplotlib
+    matplotlib.use('Agg')
+    import matplotlib.pyplot as plt
+    fig, ax = plt.subplots(figsize=(7.0, 4.8))
+    for name, x, y in zip(data['labels'], data['IDAC'], data['VLE']):
+        ax.scatter([x], [y], s=45)
+        ax.annotate(name, (x, y), xytext=(5, 5), textcoords='offset points', fontsize=9)
+    ax.set_xlabel(r'IDAC MAE in $\ln\gamma^\infty$ (708 observations)')
+    ax.set_ylabel('VLE pressure AAD, % (9,432 observations)')
+    ax.set_title('Stored main7 point estimates, property-specific subsets')
+    ax.margins(x=0.2, y=0.15)
+    fig.tight_layout()
+    fig.savefig(filename, dpi=200)
+    plt.close(fig)
+
+
+def run(root: Path, out: Path) -> None:
+    root = root.resolve()
+    inputs = {}
+    for path, expected in INPUTS.items():
+        target = (root / path).resolve()
+        require(target.is_relative_to(root), 'input symlink leaves checkout')
+        data = target.read_bytes()
+        require(blob(data) == expected, 'pinned public plot input differs: ' + path)
+        inputs[path] = data
+    h = figure2_data(inputs['results/qc/hb_constants_per_dimer.csv'],
+                     inputs['results/qc/hb_constants_by_class.csv'])
+    t = figure3_data(inputs['results/scorecard_test_main7.json'])
+    output = fresh_output(out, root)
+    render2(h, output / 'fig2_hbond_constants.png')
+    render3(t, output / 'fig3_tradeoff.png')
+    receipt = dict(base=BASE, inputs={p: dict(git_blob=blob(b), sha256=sha(b)) for p, b in inputs.items()},
+                   outputs={p.name: sha(p.read_bytes()) for p in sorted(output.glob('*.png'))},
+                   new_model_calls=0, new_scores_computed=False, pixels_equal_to_archived=False)
+    (output / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
+    print('Rendered Figures 2 and 3 from stored public quantities. Originals unchanged.')
+
+
+if __name__ == '__main__':
+    ap = argparse.ArgumentParser(description=__doc__)
+    ap.add_argument('--root', type=Path, default=ROOT)
+    ap.add_argument('--out', type=Path, required=True)
+    args = ap.parse_args()
+    run(args.root, args.out)
```
<!-- END PATCH P62 -->

<!-- BEGIN PATCH H17 -->
```diff
diff --git a/scripts/r17_selftest.py b/scripts/r17_selftest.py
new file mode 100644
index 0000000..897379e
--- /dev/null
+++ b/scripts/r17_selftest.py
@@ -0,0 +1,238 @@
+"""Portable R17 document and plotting tests. No model, private data or score execution."""
+from __future__ import annotations
+import copy
+import csv
+import io
+import json
+import os
+from pathlib import Path
+import subprocess
+import tempfile
+import unittest
+from unittest.mock import patch
+import r17_audit as audit
+import r17_figures as figures
+
+
+def hb_fixture() -> tuple[bytes, bytes]:
+    strings = io.StringIO()
+    writer = csv.writer(strings, lineterminator='\n')
+    writer.writerow(['label', 'cls', 'c_hb'])
+    groups = io.StringIO()
+    writer2 = csv.writer(groups, lineterminator='\n')
+    writer2.writerow(['cls', 'mean', 'std', 'count'])
+    for cls, count in zip(figures.CLASSES, (5, 7, 5)):
+        for i in range(count):
+            writer.writerow([f'{cls}-{i}', cls, 100.0 + i])
+        writer2.writerow([cls, 123.0, 10.0, count])
+    return strings.getvalue().encode(), groups.getvalue().encode()
+
+
+def score_fixture() -> bytes:
+    idac = {m: {'MAE_ln_gamma_inf': 0.2 + i / 100} for i, m in enumerate(figures.MODELS)}
+    vle = {m: {'AAD_P_pct': 5.0 + i} for i, m in enumerate(figures.MODELS)}
+    idac.update(n_points=708, n_systems=163)
+    vle.update(n_points=9432)
+    return json.dumps(dict(split='test', models=list(figures.MODELS), tables=dict(idac=idac, vle=vle))).encode()
+
+
+class Documents(unittest.TestCase):
+    @classmethod
+    def setUpClass(cls):
+        root = audit.ROOT
+        supplied = os.environ.get('R17_TEST_ORIGINAL')
+        # Local reconstruction may supply an exact-blob original; normal checkout uses pinned Git.
+        cls.original = Path(supplied).read_bytes() if supplied else audit.git_bytes(root, 'manuscript/draft.md')
+        audit.require(audit.blob(cls.original) == audit.ORIGINAL_BLOB, 'test original is not exact reference')
+        cls.revised = (root / 'manuscript/draft.md').read_bytes()
+        cls.supp = (root / 'manuscript/supplement.md').read_bytes()
+        cls.ledger = json.loads((root / 'docs/astra/round17/CLAIMS.json').read_text())
+
+    def check(self, **kw):
+        args = dict(original=self.original, revised=self.revised, supplement=self.supp, ledger=self.ledger)
+        args.update(kw)
+        return audit.documents(**args)
+
+    def test_exact_reviewed_documents(self):
+        out = self.check()
+        self.assertEqual(out['numeric_blocks_indexed'], 68)
+        self.assertEqual(out['original_tables_preserved'], 4)
+        self.assertFalse(out['submission_ready'])
+
+    def test_original_tamper(self):
+        with self.assertRaises(ValueError): self.check(original=self.original + b'\n')
+
+    def test_revised_tamper(self):
+        with self.assertRaises(ValueError): self.check(revised=self.revised + b'\n')
+
+    def test_supplement_tamper(self):
+        with self.assertRaises(ValueError): self.check(supplement=self.supp + b'\n')
+
+    def test_missing_claim(self):
+        ledger = copy.deepcopy(self.ledger); ledger['claims'].pop()
+        with self.assertRaises(ValueError): self.check(ledger=ledger)
+
+    def test_claim_location(self):
+        ledger = copy.deepcopy(self.ledger); ledger['claims'][1]['start_line'] += 1
+        with self.assertRaises(ValueError): self.check(ledger=ledger)
+
+    def test_duplicate_claim_id(self):
+        ledger = copy.deepcopy(self.ledger); ledger['claims'][1]['id'] = ledger['claims'][0]['id']
+        with self.assertRaises(ValueError): self.check(ledger=ledger)
+
+    def test_fabricated_ready_flag(self):
+        ledger = copy.deepcopy(self.ledger); ledger['submission_ready'] = True
+        with self.assertRaises(ValueError): self.check(ledger=ledger)
+
+    def test_no_unexplained_original_table_loss(self):
+        old = audit.tables(self.original.decode())[0]
+        revised = self.revised.replace(old.encode(), b'')
+        ledger = copy.deepcopy(self.ledger); ledger['revised_sha256'] = audit.sha(revised)
+        with self.assertRaises(ValueError): self.check(revised=revised, ledger=ledger)
+
+    def test_lost_lv1_qualification(self):
+        revised = self.revised.replace(b'failed the joint registered screen', b'passed this screen')
+        ledger = copy.deepcopy(self.ledger); ledger['revised_sha256'] = audit.sha(revised)
+        with self.assertRaises(ValueError): self.check(revised=revised, ledger=ledger)
+
+
+class ArithmeticAndSafety(unittest.TestCase):
+    def test_blob_known_empty(self):
+        self.assertEqual(audit.blob(b''), 'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391')
+
+    def test_rounding_he_is_compatible(self):
+        self.assertTrue(audit.rounded_difference_compatible('632.9', '618.6', '14.2', 1))
+
+    def test_shapley_bias_is_not_singleton(self):
+        self.assertFalse(audit.rounded_difference_compatible('-2.79', '1.44', '-4.47', 2))
+
+    def test_rounding_nonfinite(self):
+        with self.assertRaises(ValueError): audit.rounded_difference_compatible('NaN', '1', '0', 2)
+
+    def test_rounding_invalid_precision(self):
+        with self.assertRaises(ValueError): audit.rounded_difference_compatible('1', '1', '0', -1)
+
+    def test_paths(self):
+        for valid in ('manuscript/draft.md', 'results/scorecard_test_main7.json', 'PREREGISTRATION.md'):
+            audit.safe_relative(valid)
+        for invalid in ('../secrets', '/tmp/file', 'data/raw/nist/UD/x.sigma', 'results/predictions/x.csv'):
+            with self.subTest(invalid=invalid), self.assertRaises(ValueError): audit.safe_relative(invalid)
+
+    def test_fresh_path_is_resolved(self):
+        with tempfile.TemporaryDirectory() as temp:
+            parent = Path(temp).resolve(); root = parent / 'repo'; root.mkdir()
+            out = audit.fresh_output(parent / 'report', root)
+            self.assertEqual(out, (parent / 'report').resolve())
+            with self.assertRaises(FileExistsError): audit.fresh_output(out, root)
+
+    def test_inside_checkout_rejected(self):
+        with tempfile.TemporaryDirectory() as temp:
+            root = Path(temp).resolve(); (root / '.git').mkdir()
+            with self.assertRaises(ValueError): audit.fresh_output(root / 'bad', root)
+
+    def test_other_checkout_rejected(self):
+        with tempfile.TemporaryDirectory() as temp:
+            root = Path(temp).resolve(); repo = root / 'repo'; repo.mkdir()
+            other = root / 'other'; other.mkdir(); (other / '.git').mkdir()
+            with self.assertRaises(ValueError): audit.fresh_output(other / 'out', repo)
+
+    def test_source_hash_mismatch_stops(self):
+        with tempfile.TemporaryDirectory() as temp, patch.object(audit, 'git_bytes', return_value=b'changed'):
+            with self.assertRaises(ValueError): audit.sources(Path(temp), {'README.md': '0' * 40})
+
+    def test_working_source_mismatch_stops(self):
+        with tempfile.TemporaryDirectory() as temp, patch.object(audit, 'git_bytes', return_value=b'original'):
+            root = Path(temp); (root / 'README.md').write_bytes(b'changed')
+            with self.assertRaises(ValueError): audit.sources(root, {'README.md': audit.blob(b'original')})
+
+    def test_exact_source_passes(self):
+        with tempfile.TemporaryDirectory() as temp, patch.object(audit, 'git_bytes', return_value=b'original'):
+            root = Path(temp); (root / 'README.md').write_bytes(b'original')
+            result = audit.sources(root, {'README.md': audit.blob(b'original')})
+            self.assertEqual(result['README.md']['bytes'], 8)
+
+    def test_reviewed_readme_append(self):
+        with tempfile.TemporaryDirectory() as temp, patch.object(audit, 'git_bytes', return_value=b'original'):
+            root = Path(temp); current = b'original\nreviewed append'; (root / 'README.md').write_bytes(current)
+            audit.sources(root, {'README.md': audit.blob(b'original')}, {'README.md': audit.sha(current)})
+            with self.assertRaises(ValueError):
+                audit.sources(root, {'README.md': audit.blob(b'original')}, {'README.md': '0' * 64})
+
+    def test_source_symlink_escape(self):
+        with tempfile.TemporaryDirectory() as temp, patch.object(audit, 'git_bytes', return_value=b'original'):
+            parent = Path(temp).resolve(); root = parent / 'repo'; root.mkdir()
+            external = parent / 'file'; external.write_bytes(b'original')
+            (root / 'README.md').symlink_to(external)
+            with self.assertRaises(ValueError): audit.sources(root, {'README.md': audit.blob(b'original')})
+
+    def test_registration_append_preserves_history(self):
+        with tempfile.TemporaryDirectory() as temp, patch.object(audit, 'git_bytes', return_value=b'original'):
+            root = Path(temp); proposed = root / 'docs/astra/round17/REGISTRATION_PROPOSED.md'
+            proposed.parent.mkdir(parents=True); proposed.write_bytes(b'R17 proposal')
+            (root / 'PREREGISTRATION.md').write_bytes(b'original\nRound 17 adopted at DATE\nR17 proposal')
+            audit.sources(root, {'PREREGISTRATION.md': audit.blob(b'original')})
+            (root / 'PREREGISTRATION.md').write_bytes(b'revised history\nRound 17 adopted at DATE\nR17 proposal')
+            with self.assertRaises(ValueError): audit.sources(root, {'PREREGISTRATION.md': audit.blob(b'original')})
+
+
+class FigureData(unittest.TestCase):
+    def test_hb_uses_stored_means(self):
+        data = figures.figure2_data(*hb_fixture())
+        self.assertEqual(data['means'], [123.0] * 3)
+        self.assertEqual(data['count'], 17)
+
+    def test_hb_missing_dimer(self):
+        a, b = hb_fixture()
+        a = b'\n'.join(a.splitlines()[:-1]) + b'\n'
+        with self.assertRaises(ValueError): figures.figure2_data(a, b)
+
+    def test_hb_nonfinite(self):
+        a, b = hb_fixture(); a = a.replace(b'100.0', b'nan', 1)
+        with self.assertRaises(ValueError): figures.figure2_data(a, b)
+
+    def test_hb_duplicate_identity(self):
+        a, b = hb_fixture(); a = a.replace(b'OH-OH-1,', b'OH-OH-0,', 1)
+        with self.assertRaises(ValueError): figures.figure2_data(a, b)
+
+    def test_main7_stored_values(self):
+        d = figures.figure3_data(score_fixture())
+        self.assertEqual(d['IDAC_rows'], 708)
+        self.assertEqual(d['VLE_rows'], 9432)
+        self.assertEqual(d['VLE'][0], 5.0)
+
+    def test_main7_wrong_denominator(self):
+        d = json.loads(score_fixture()); d['tables']['idac']['n_points'] = 762
+        with self.assertRaises(ValueError): figures.figure3_data(json.dumps(d).encode())
+
+    def test_main7_wrong_models(self):
+        d = json.loads(score_fixture()); d['models'].append('hanna')
+        with self.assertRaises(ValueError): figures.figure3_data(json.dumps(d).encode())
+
+    def test_main7_nonfinite(self):
+        d = json.loads(score_fixture()); d['tables']['vle']['Z0x']['AAD_P_pct'] = float('nan')
+        with self.assertRaises(ValueError): figures.figure3_data(json.dumps(d).encode())
+
+    def test_render_synthetic_fig2(self):
+        with tempfile.TemporaryDirectory() as temp:
+            path = Path(temp) / 'fig2.png'
+            figures.render2(figures.figure2_data(*hb_fixture()), path)
+            self.assertEqual(path.read_bytes()[:8], b'\x89PNG\r\n\x1a\n')
+
+    def test_render_synthetic_fig3(self):
+        with tempfile.TemporaryDirectory() as temp:
+            path = Path(temp) / 'fig3.png'
+            figures.render3(figures.figure3_data(score_fixture()), path)
+            self.assertEqual(path.read_bytes()[:8], b'\x89PNG\r\n\x1a\n')
+
+    def test_real_cli_wrong_input_hash_before_output(self):
+        with tempfile.TemporaryDirectory() as temp:
+            root = Path(temp) / 'repo'; root.mkdir()
+            for path in figures.INPUTS:
+                p = root / path; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(b'wrong')
+            out = Path(temp) / 'out'
+            with self.assertRaises(ValueError): figures.run(root, out)
+            self.assertFalse(out.exists())
+
+
+if __name__ == '__main__':
+    unittest.main(verbosity=2)
```
<!-- END PATCH H17 -->

<!-- BEGIN PATCH REG17 -->
```diff
diff --git a/docs/astra/round17/REGISTRATION_PROPOSED.md b/docs/astra/round17/REGISTRATION_PROPOSED.md
new file mode 100644
index 0000000..14df6b1
--- /dev/null
+++ b/docs/astra/round17/REGISTRATION_PROPOSED.md
@@ -0,0 +1,49 @@
+R17-P60-P61-P62: final manuscript and evidence closeout
+
+Proposed reporting text. Append this complete text with the actual adoption time to PREREGISTRATION.md
+before using the revised manuscript or new reporting outputs. Commit the reviewed manuscript, supplement,
+claim/reference ledger and reporting helpers together. Base: 35ab60046f3f4a7566d8eeee6b13172a6d0becc2.
+This is an E editorial/reporting revision. It changes no scientific model or experimental protocol.
+README.md receives only the reviewed dated R17 closeout append; its prior text remains byte-for-byte intact.
+
+P60 revises manuscript/draft.md, moves the longer numerical/profile/conformer/simulation chronology into
+manuscript/supplement.md, and adds the completed R16/P58 negative result to section 3.11 and the discussion.
+All four pre-existing manuscript numerical tables are preserved verbatim, in the main text or supplement.
+The historical scorecards, RESULTS files and old registration text are immutable. Corrected manuscript
+confidence intervals are explicitly tied to their named main7 source. The displaced old strings and
+unrecovered precise claims retain their source qualification in Supplement S0 instead of being silently
+reconstructed from other subsets. A confidence interval including zero is not an equivalence result.
+
+Record the complete LV1 failure, with the original observation/system counts and separate one-sided
+bounds. The rounded HE endpoints 618.6 and 632.9 do not overwrite the recorded unrounded change +14.2.
+P58a's 51 pure-composition HE exclusions and the macOS fixture errors remain visible. The favorable LLE
+point estimates do not override failed uncertainty gates. LV1 is not adopted and no second candidate,
+changed weight, term deletion, native investigation or score retry is authorized. The VLE gap remains
+unresolved; the model-development campaign is closed for this project.
+
+P61 indexes every original digit-bearing manuscript paragraph and each entire numerical table, with
+source-specific dispositions. The mechanical coverage check is not a claim of semantic proof or a new
+reproduction of private statistics. The checked public Git objects are pinned in CLAIMS.json. The original
+registration text can only receive this dated append, never be rewritten. Existing unresolved provenance
+items keep submission_ready=false, even when all software checks pass. Recovering an already-generated
+source artifact is allowed as editorial work; generating replacement predictions or bootstraps is not.
+
+P62 redraws only Figures 2 and 3 from the pinned public per-dimer, stored class-mean and main7 scorecard
+files. It imports no activity model, reads no private prediction/profile data and computes no new score.
+It writes to a fresh directory outside every Git checkout and leaves the committed original images intact.
+The existing Figure 1/4/5 PNGs may be exported byte-for-byte from Git, but their exact original regeneration
+requires the original private arrays and masks. Do not run scripts/make_figures.py as a zero-score shortcut.
+The new public redraw does not promise pixel equality with the archived plots. Metadata existence is
+not a completed visual or row-level figure audit.
+
+Complete the explicitly listed publisher and historical-artifact checks before claiming submission-ready
+bibliography and reproducibility. The reference audit's unresolved Herington record, D4 direct publisher
+retrieval and COSMO-SAC-dsp corrigendum text are not marked checked by inference. No new data source is
+selected and no exposure label is reset. The original and temporal test collections remain exposed for
+later development; P54 is a conditional attribution and P58 a failed exposed screen.
+
+Authorized budgets: zero new SCF attempts, zero gradients, zero optimization or MD steps, zero activity-
+model requests and zero new experimental error/bootstrap calculations. No Actions, paid resource, cloud
+job or private-data upload. No profile edits: 630 primary plus one selected S1 and five selected S2 files
+remain frozen. Source/document checks and synthetic unit tests may be repeated. Output folders are fresh
+and prior artifacts are never overwritten. All patches are local proposals until adopted by the maintainer.
```
<!-- END PATCH REG17 -->

