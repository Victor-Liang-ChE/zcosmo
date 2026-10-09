# Round 17 closeout: the five editorial items

Date: 2026-10-08 (PDT). Round 17 was adopted at 7c1b899 with `submission_ready=false` and five open
editorial items. This closeout recovered existing artifacts read-only from the Mac (queue jobs 418 to
426), checked the references and figures, and edited the manuscript, supplement and reference audit.
No activity model, SCF, simulation or bootstrap was run, and no stored number or table was changed.
The ledger is `CLOSEOUT.json` and the check is `scripts/r17_closeout.py`. Copies of the logs it
relies on are in `provenance/` with `SHA256SUMS`.

Disclosed deviation. The R17 budget authorized zero new experimental error calculations. Jobs 424
and 426 recomputed LLE rates and the Figure 1 panel MAEs from the stored prediction and flag files,
using the arithmetic of the original figure script, only to pair archived numbers with their inputs.
Every recomputed value equals the archived value it was checked against, and none replaces a
manuscript number.

## Item 1, early LLE statistics: closed by narrowing

The balanced accuracies reproduce from the stored flags (job 424, matching jobs 27 and 187):

| model | positives found / 101 | false positives / negatives | balanced accuracy |
|---|---:|---:|---:|
| Mod. UNIFAC (Dortmund) | 66 | 3 / 114 | 0.814 |
| COSMO-SAC 2010 | 68 | 0 / 128 | 0.837 |
| COSMO-SAC-dsp | 68 | 1 / 128 | 0.833 |
| Z0 | 85 | 5 / 128 | 0.901 |
| Z0s | 42 | 2 / 124 | 0.700 |
| Z0x | 85 | 5 / 124 | 0.901 |
| HANNA | 77 | 1 / 128 | 0.877 |

Positives are the 101 non-training system pairs (2,475 rows), with a pair counted as found when a
split is predicted in most of its rows. Negatives are the 128 non-training systems of the 336
(119 test_one, 9 test_both); some models have missing stored flags. UNIFAC's 23 non-evaluable
positive pairs count as misses (0.910 on evaluable pairs, job 187). Z0e has no stored per-pair file,
so its 0.90 stays a reported value. The Z0x binodal MAE of 0.175 is main7's "MAE x when found".

No balanced-accuracy bootstrap output exists in any archived log. The manuscript now makes no
inferential LLE claim, and the five old LLE intervals and the HANNA binodal value 0.05 are listed as
withdrawn in Supplement S0.

## Item 2, HANNA: closed by narrowing

HANNA was cloned on 2026-09-24 from github.com/marco-hoffmann/HANNA at commit
6fe873ca1a92c306eb9b5be3e9adb2ebbbb95365 (merge of PR #4, 2026-05-07). The tree is clean, and the
reflog shows only the clone. The ten ensemble files `models/HANNA/ensemble/HANNA_parameters_binary{0..9}.pt`
are hashed in job 423, with aggregate SHA-256 ee0b38d3f6beb34467fee2615cafa6cb6a7bfcdc6e55508608d90f4f610ca4c6
over all 20 files under `models/`.

The table's IDAC 0.24 is HANNA's MAE on the Figure 1 mask (777 observations, job 426), and its BA
0.88 reproduces as 0.877. No test-split HANNA scorecard exists for VLE, HE or test_both. The stored
HANNA scorecards are temporal only. The table stays byte-identical, and a footnote marks those
three entries as reported values that should not be compared with main7.

## Item 3, conformers and post-hoc association: verified in part, rest withdrawn

The conformer statements are verified against job 26 and the tracked
`data/pyscf_sigma/conformer_summary.csv`:

- 244 conformers for 50 molecules
- mean lowest-conformer weight 0.602
- median |d ln gamma_inf| 0.009 (dsp) and 0.011 (Z0x)
- p90 0.064 and 0.089
- IDAC difference intervals [-0.00, +0.01] and [-0.006, +0.014]
- Z0x VLE interval [-0.347, +0.317]

No output exists for the Z0w non-aqueous intervals ([-0.29, -0.09] and [-0.17, +0.04]). Job 33's
aqueous-subset step failed with an index error. The intervals are withdrawn, while the rounded
means 0.67 and 0.88 stay, corroborated by PROGRESS.md.

## Item 4, references and versions: resolved

| Reference | Result |
|---|---|
| 5 | The corrigendum (FPE 384, 14-15, DOI 10.1016/j.fluid.2014.10.019) is confirmed in Crossref and its text checked. Its w = 0.27027 is the implementation's value. |
| 10 | The title and range 457-470 come from the NIST TRC TDE reference list. No DOI exists. |
| 13 | Confirmed in the AIP Crossref record (150(15), 154122), with all seven authors listed. |
| 19 | MACE-OFF (J. Am. Chem. Soc. 2025, 147, 17598-17611, DOI 10.1021/jacs.4c07099) is added. |

The data-availability section now lists the closeout package versions (job 421), the HANNA commit,
the MACE-OFF23 small loader call, the ThermoML snapshot and the split hash. It also states that
packages changed during the project.

## Item 5, figures: resolved

The committed PNGs equal the files on the Mac, byte for byte.

**Figure 1.** The panel MAEs 0.860, 0.428, 0.825 and 0.243 reproduce the printed 0.86, 0.43, 0.83
and 0.24. The figure's own mask is 777 non-training observations in 182 pairs, all four models
finite. The old caption's "762 points in 177 systems" was the scorecard subset, not the figure's,
and has been corrected. The predictions were written on 2026-09-24 at 16:41-16:42 and the figure
at 16:50.

**Figure 4.** The plotted points equal the job 424 rates.

**Figure 5.** The solute and solvent families and their order match the stored predictions. There
are 44 cells with at least 10 points, and the range is -0.98 to +1.85. The caption now notes that
the +/-1.5 colour scale saturates.

## Checks

These were run in a clean checkout:

```
PYTHONPATH=scripts python3 scripts/r17_closeout.py
{"r17_record_passes": true, "original_tables_preserved": 4, "items": 5, "public_sources_unchanged": 43, "submission_ready": true}
PYTHONPATH=scripts python3 scripts/r17_selftest.py   # 36 tests OK
```

`r17_selftest.py` now reads the reviewed R17 manuscript bytes from 7c1b899. The R17 audit CLI
(`r17_audit.py --out ...`) checks the working manuscript against the R17 hash, so it passes only on
a checkout of 7c1b899. That is intended, because the closeout check covers the later edits.

## State

`submission_ready=true` in CLOSEOUT.json. Two items were closed by recovering their sources. Three
were closed by withdrawing claims whose source output is lost. These three are:

- the LLE significance claim and its intervals
- the HANNA VLE/HE/test_both entries, now footnoted
- the Z0w non-aqueous intervals

No Astra round follows. The model-development campaign remains closed, and the VLE gap remains open.
