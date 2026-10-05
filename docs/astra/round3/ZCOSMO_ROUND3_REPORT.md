# Z-COSMO round 3: profile orientation, IDAC provenance, and bounded final convergence

Reference: `Victor-Liang-ChE/zcosmo`, `main = c515e38e1a7fd91a02e1ff1f1209a81b67a7d49d`. Its commit timestamp is October 5, 2026, 04:33 UTC, which is October 4 in California. The round-3 prompt and October 4 registrations govern this report. All six patches below target this snapshot. The source index at the end identifies the inspected files and pinned upstream APIs. [S1–S5]

The next task is to measure how much orientation moves **ln gamma**, while reconciling the stored IDAC comparisons. Another broad geometry-optimization or GPU campaign is not justified first. The raw-bin observation is substantial, but it does not establish that orientation explains the 0.138 MAE deficit. There is also a specific metadata defect worth isolating: `to_profiles()` discards the NIST parser's special `COOH` dispersion flag. That affects COSMO-SAC-dsp, including the profile acceptance statistic, but does not directly affect Z0x's London dispersion. [S2, S6–S9]

P15 remains rejected. S2 remains an accepted, explicitly flagged A protocol. Primary `profiles_v2` remains 630/636; exploratory coverage is 636 after adding six S1/S2 profiles. The round-2 record establishes percent-level raw-bin sensitivity on the tested six chains and rotations, not the same sensitivity for every member of the 636-compound set. [S2, S5]

What I executed: full reconstruction and Git-blob verification of `pyscf_cosmo.py`, and source-context verification of the `profile_revision()` hunk in `pyscf_cosmo_v2.py`; independent and combined patch-application checks against the reconstructed, blob-verified changed source; Python compilation; the supplied portable tests; and synthetic end-to-end tests of the 25-key/2,302-occurrence manifest, the three rotation averages, finite-coverage gates, and source-change rejection. The body-frame test used four geometries and 100 rotations each, with maximum coordinate disagreement `6.22e-15 Å`. The Hsieh formula co-rotation check differed by `8.67e-19 e/Å²`. A test using the actual repository `cavity_volume()` verified the translation identity below to `2.22e-16 Å³`. These are software/mathematical checks, not native quantum-chemistry acceptance.

What I did not execute: PySCF SCF, quantum gradients, real sigma-profile generation, the UD-backed 2,302-row comparison, the stored 828-row score reconstruction, or a new production scorecard. PySCF and pyberny were absent. An actual installation attempt for `pyscf==2.14.0 pyberny==0.7.0` failed in this runtime's resolver; direct network access also failed. This does not mean those releases are unavailable generally. Every native effectiveness or equivalence claim remains conditional on the supplied commands. The stored `results/predictions/Z0x__idac__all.csv` also returned Not Found through the repository connector, so I do not manufacture its row-level contents.

## Ranked work

Correctness and measurement are prerequisites to the brief's performance ranking. There is no defensible measured saving for a new profile recipe yet. The table therefore gives explicit work counts rather than assigning an invented wall-clock speed-up. The ordering favors preventing an unnecessary 636-profile rerun, then inexpensive corrections and reuse of work already measured. For subsequent performance trials, use the original rule `remaining_calls × saving_per_call × probability / effort`; the post-P9 per-call saving must be measured, not inferred from an older cumulative profile.

| Order | ID / mode | Target and purpose | E/A status | Work or conditional speed arithmetic | Effort |
|---:|---|---|---|---|---|
| prerequisite | H3 | Shared manifests, comparison gates, portable tests | E diagnostic utilities; no production result changed | No SCF or gradient calls | Low |
| 1 | P16 | `metrics`/`evaluate` provenance; class and role attribution | E descriptive audit | Reuses CSVs; four-corner attribution costs four evaluator passes per ordered pair, not four QC runs | Low to medium |
| 2 | P17 / raw | `cosmo_segments` and `to_profiles` orientation measurement | E instrumentation only; rotated profiles are not claimed E-equivalent | `25 × (identity + repeat + 8 rotations + cube90) + 3 × 5 angles = 290` single points | Medium |
| 3 | P18 | Preserve `COOH` metadata, with a zero-SCF reconstruction | A numerical correction, opt-in | No new SCF for existing profiles: change only verified metadata; raw sigma rows stay identical | Low |
| 4 | P17 / mean8 | Equal-weight rotational quadrature averaging | A profile protocol | Eight single points per geometry from scratch; no extra SCF after the primary random-rotation panel. Disjoint/nested validation adds `25 × 8 = 200` single points | Low additional effort |
| 5 | P17 / canonical | Fixed proper body frame with degeneracy handling | A profile protocol | Approximately one ordinary single point per future profile, plus negligible coordinate algebra; validation is `25 × 9 = 225` single points | Medium |
| 6 | P17 / lebedev41 | Finer PCM discretization, unchanged XC grid and averaging | A profile protocol | 590 rather than 302 angular points per atom; about 1.95 times surface-integral storage and 3.82 times dense surface-matrix storage before changed switching/pruning | Medium |
| 7 | P19 | Tighter SCF final stage, followed by the actual original Berny test | A geometry protocol | At most 80 tighter-SCF gradient evaluations plus 20 original-setting evaluations per arm/molecule; no speed-up claimed against a censored reference | Medium |

P17 contains several explicit experimental modes in one new-file diff. They are distinct recipes, selected only by their documented command-line mode. Applying the code does not combine them or enable any recipe in production. P18's production hook defaults **off**. The proposed registration fixes the numerical gates before their native outputs are examined; it does not authorize choosing the recipe with the lowest experimental MAE.

## Setup, assets, registration, and patch extraction

Use the populated local repository on the Mac for all UD-backed scoring. The source checkout alone is insufficient because UD profiles are ignored by Git. Native item jobs can run separately on free CPU runners and return their experiment directories. These commands do not launch a cloud service or use paid credits.

Save this report as `ZCOSMO_ROUND3_REPORT.md`. From the populated repository, extract and apply the experimental code in a disposable worktree:

```bash
set -euo pipefail
export REPO="$PWD"
export BASE=c515e38e1a7fd91a02e1ff1f1209a81b67a7d49d
export REPORT="${REPORT:-$REPO/ZCOSMO_ROUND3_REPORT.md}"
export WORK="$(mktemp -d "${TMPDIR:-/tmp}/zcosmo-r3.XXXXXX")"
export TREE="$WORK/tree"
export PATCHES="$WORK/patches"
mkdir -p "$PATCHES"
python - "$REPORT" "$PATCHES" <<'PY'
from pathlib import Path
import re, sys
text=Path(sys.argv[1]).read_text()
blocks=re.findall(r'<!-- PATCH:(H3|P16|P17|P18|P19|REG) -->\s*```diff\n(.*?)\n```',text,re.S)
assert len(blocks)==6 and len({n for n,_ in blocks})==6
for name,body in blocks:
    Path(sys.argv[2],name+'.patch').write_text(body+'\n')
PY
git -C "$REPO" worktree add --detach "$TREE" "$BASE"
# Share immutable input assets, not outputs. Do not run the old scorecard CLI here.
for asset in data results; do
  test -d "$REPO/$asset"
  if test -e "$TREE/$asset"; then mv "$TREE/$asset" "$TREE/$asset.pinned-copy"; fi
  ln -s "$REPO/$asset" "$TREE/$asset"
done
for id in H3 P16 P17 P18 P19 REG; do
  git -C "$TREE" apply --check "$PATCHES/$id.patch"
  git -C "$TREE" apply "$PATCHES/$id.patch"
done
cd "$TREE"
export PYTHONPATH=src:scripts
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export ZC_PCM3C=1 ZC_R3_COOH_FLAG=0 QC_MEM_MB=6000
unset ZC_SIGMA_OVERRIDE_DIR ZC_BERNY_NOISE_EH ZC_TRIC_PREOPT ZC_MAXSTEPS
unset ZC_BENCH ZC_PRED ZC_PRED_SPLIT
python -m pip freeze > "$WORK/environment.txt"
python scripts/r3_selftest.py --volume-source src/zcosmo/pyscf_cosmo.py \
  --out "$WORK/portable-tests.json"
```

For native generation, use the already working pinned environment. A clean environment would require the following, but installation did not succeed here:

```bash
python -m pip install 'pyscf==2.14.0' 'pyberny==0.7.0' \
  rdkit tblite ase numpy scipy pandas matplotlib
```

Keep the resulting environment fixed across arms. Pyberny's `0.7.0` tag resolves to `8f200b868b5b42247cbac7e2c5cec27811671fdd`; the inspected source is that tag, not a guessed `v0.7.0` or today's development branch. [U3]

`REG.patch` adds proposed text to `docs/astra/round3/PROPOSED_REGISTRATION.md`. **It is not itself a claim that registration has happened.** Review that text and append it in the maintainer's normal working branch before generating or reading any new native candidate output:

```bash
# Run in the maintainer's normal branch, not as an unnoticed edit to shared inputs.
cat "$TREE/docs/astra/round3/PROPOSED_REGISTRATION.md" >> "$REPO/PREREGISTRATION.md"
git -C "$REPO" add PREREGISTRATION.md
git -C "$REPO" commit -m "Register fixed R3 profile reliability and precision experiments"
export REGISTRATION_COMMIT="$(git -C "$REPO" rev-parse HEAD)"
```

This is an explicit maintainer action, not something performed by this review. Preserve the patch files and commit hash with the output. The new scripts never write into `profiles_v2` or stored scorecards. Avoid running the production all-compounds generator merely because applying a source patch changes `profile_revision()` and invalidates text-hash cache hits.

## P16: determine what the IDAC gap actually compares

The current `metrics.scorecard()` computes a row-weighted MAE on the intersection of nonmissing predictions for **every model in its `models` argument**. Its test split is `split != 'train'`, not just `test_both`. Its default file suffix is `__all.csv`, even when scoring the test split; `ZC_PRED_SPLIT` can change that suffix. `evaluate` controls the benchmark directory, applies profile-coverage filtering, and writes predictions under `ZC_PRED`. These choices must be reconstructed before treating 0.800 and 0.839 as contradictory. [S10, S11]

There is a real robustness issue: `metrics` combines per-model masks positionally without checking observation identities. Equal row counts do not prove equal rows or equal ordering. The audit supplied here joins by observation provenance, including the experimental record and duplicate occurrence, rather than only `(solute, solvent, T)`. It refuses indistinguishable duplicate observations with different predictions. It also distinguishes NaN from infinity: `.notna()` in the existing scorer admits infinity, whereas the audit requires finite values. No actual infinity or misalignment in the stored 828-point comparison is asserted without its CSVs. [S10]

Start with the available local inventory. The repository's `results/scorecard_test.json` that I could read is an older 708-point comparison of UNIFAC, COSMO-SAC, Z0, and Z1, with no Z0x entry. It cannot establish the historical 0.800 by itself. [S12]

```bash
cd "$TREE"
python scripts/r3_idac.py inventory --root "$REPO/results" \
  > "$WORK/idac-inventory.json"
# Use the actual local candidate path returned by the inventory or the scoring job.
export REF_IDAC="$REPO/results/predictions/Z0x__idac__all.csv"
: "${OPEN_IDAC:?Set OPEN_IDAC to the actual stored 636-profile Z0x-open IDAC CSV}"
test -f "$REF_IDAC" && test -f "$OPEN_IDAC"
/usr/bin/time -p python scripts/r3_idac.py audit \
  --reference "$REF_IDAC" --candidate "$OPEN_IDAC" \
  --compounds "$REPO/data/benchmark/compounds.csv" --split test \
  --expect-points 828 --out "$WORK/idac-audit"
```

The inventory also reports local JSON scorecards containing Z0x, including their model list and point count. Once the historical model list is known, supply exactly those prediction files as `--mask LABEL=CSV`. For example, the following is valid only when the historical scorecard actually names these comparison models:

```bash
python scripts/r3_idac.py audit \
  --reference "$REF_IDAC" --candidate "$OPEN_IDAC" --split test \
  --mask "unifac_do=$REPO/results/predictions/unifac_do__idac__all.csv" \
  --mask "cosmosac_dsp=$REPO/results/predictions/cosmosac_dsp__idac__all.csv" \
  --out "$WORK/historical-mask-audit"
```

The output `denominators.csv` reports Z0x alone, each supplied model intersection, the entire supplied intersection, the open/UD common subset, and that common subset excluding the six flagged chains. It records input and row-ID hashes. A model-list intersection that reproduces 0.800 with unchanged Z0x predictions would establish a denominator explanation. A changed observation set or changed finite mask establishes a coverage/input difference. A same-row comparison of values can establish prediction drift; matching physical input assets are still needed before calling that a code regression.

For a fresh calculation, leave every original file untouched and use the exact benchmark/model assets corresponding to the stored snapshot. This command is for the asset-bearing Mac:

```bash
test -d "$REPO/data/raw/nist/UD/sigma3"
mkdir -p "$WORK/fresh-UD"
(cd "$TREE"
 unset ZC_SIGMA_OVERRIDE_DIR ZC_PRED_SPLIT
 ZC_BENCH="$REPO/data/benchmark" ZC_PRED="$WORK/fresh-UD" \
   python -m zcosmo.evaluate Z0x --tables idac --split all)
python scripts/r3_idac.py compare-fresh \
  --reference "$REF_IDAC" --candidate "$WORK/fresh-UD/Z0x__idac__all.csv" \
  --out "$WORK/fresh-versus-stored.json"
```

Do not overwrite the historical result if this fails. Inspect the recorded observation identities, profile resolution, dielectric/dispersion tables, and environment. P6's interior derivative correction leaves the implemented infinite-dilution endpoint branch unchanged; it is not by itself an explanation for an IDAC difference. Bootstrap random-number consumption can change a reported confidence interval, but cannot change the point-estimate MAE. The audit resets its pair-bootstrap seed for each statistic, so its confidence intervals need not reproduce the old scorer's globally consumed RNG sequence bit for bit. [S9, S10]

### Class and role decomposition, without fitting

The same audit writes `by_solute_class.csv`, `by_solvent_class.csv`, `class_by_role.csv`, `by_water_role.csv`, and per-compound tables. Its chemistry categories are fixed structural rules in the patch, with a separate multifunctional category. They are descriptive categories, not adjustable predictors. Each exclusive partition reports

\[
\Delta_c=\frac{1}{N}\sum_{r\in c}\bigl(|\hat y_{open,r}-y_r|-|\hat y_{UD,r}-y_r|\bigr).
\]

These contributions sum to the total MAE difference on the fixed common rows. Reporting only each class's within-class MAE would hide whether a small class explains much of the overall change. The script also reports binary-system counts and system-bootstrap intervals; many temperature rows from one pair are not independent systems.

Water is separated into solute and solvent roles. The earlier 0.82 median difference over 450 acceptance occurrences is a difference in predictions under a different check, not water's contribution to the 828-point test MAE. Likewise, removing 151 IDAC rows before split/common filtering leaves 816 rather than 828 common test points, a removal of 12 from that particular denominator. The supplied rounded scores have the same 0.138 deficit with or without the six chains. Completing those chains differently cannot plausibly be the main remedy for the existing comparison. [S2, S5]

For causal attribution to **which profile is substituted**, run the optional four-corner check after assembling the actual 636-profile directory used for the stored open score. Do not automatically prefer an S2 file over the registered S1 exception for MVLVMROFTA; use exactly the original scoring inputs.

```bash
: "${OPEN_PROFILES:?Set OPEN_PROFILES to the exact 630 plus 6 S1/S2 directory used by the open scoring job}"
/usr/bin/time -p python scripts/r3_hybrid.py run \
  --paired-rows "$WORK/idac-audit/paired_rows.csv" \
  --open-profiles "$OPEN_PROFILES" --model Z0x \
  --out "$WORK/role-hybrid"
```

Each ordered binary gets fresh processes for UD/UD, open/UD, UD/open, and open/open. With values `uu, ou, uo, oo`, solute and solvent contributions are

\[
D_s=\tfrac12[(ou-uu)+(oo-uo)],\quad
D_v=\tfrac12[(uo-uu)+(oo-ou)],\quad D_s+D_v=oo-uu.
\]

Applying the same identity to absolute errors decomposes the MAE change, including interactions, without assigning the entire nonadditivity to whichever profile happened to be swapped first. The worker uses the actual `make_model()` rather than a rewritten Z0x formula. It records profile paths and hashes and reports fresh/stored corner discrepancies. If a mixed corner is nonfinite, the script reports unavailable rows and refuses to call the remainder a decomposition of the full score.

For Z0x, “profile substitution” includes its area and volume as consumed by the model. The fixed dielectric table stays fixed; the profile volume still changes mixture volume fractions and London contact distances. This is intentional attribution of the implemented pipeline, not an isolated sigma-shape sensitivity. [S8, S9]

## P17: mechanism and measured-first orientation experiment

In the pinned `gen_surface`, each atom receives `atom_center + radius × fixed_Lebedev_direction`. The directions remain in the laboratory frame when only the molecule rotates. The neighboring atoms therefore obscure different nodes. SWIG assigns each node a product of switching functions, and the area is `4 pi × angular_weight × radius² × switch`. Tiny switched nodes are removed upstream, and the wrapper additionally removes areas below `1e-8 bohr²`. The surviving locations, effective areas, Gaussian charge widths, and surface matrix can change. The self-consistent reaction potential and charges can consequently change as well. The DFT XC grid is another finite atom-centered angular quadrature. [S6, U1]

For C-PCM, schematically `q = -f S^{-1} v`, with `f=(epsilon-1)/epsilon`. Finite energy agreement is not sufficient to establish agreement of the local charge-density distribution. The profile conversion divides each charge by its segment area before averaging. It then deposits the averaged densities onto fixed sigma bins and partitions their HB contribution. Changes concentrated in narrow peaks or tails can produce visibly different raw bins without a comparable relative energy difference. [S6, S7, U1]

The actual Hsieh step is

\[
\bar\sigma_m=\frac{\sum_n W_{mn}\sigma_n}{\sum_n W_{mn}},\qquad
W_{mn}=\frac{r_n^2r_{av}^2}{r_n^2+r_{av}^2}
\exp\!\left[-\frac{3.57\,|r_m-r_n|^2}{r_n^2+r_{av}^2}\right],
\]

where `r_n²=A_n/pi` and `r_av²=7.25/pi Å²`. This expression is rotationally invariant when the **same segments, areas, and charges** are co-rotated. It does not make a newly sampled, orientation-dependent surface invariant. The HB class calculation uses molecular connectivity inferred from distances; the split also uses the sign of averaged sigma. Binning uses neighboring sigma-grid points, followed by the code's `sigma_0=0.007` HB weighting. The metadata label `sigma_hb=0.0084` is not the constant used in that final weighting expression. No replacement constant is proposed. [S7]

Small rotations ordinarily move nodes only a small distance relative to the molecule, so the change initially tends to be small. A larger rotation explores a more different discretization. This is not a monotonic angle law: the axis, symmetry, node pruning, and bin locations matter. Some proper cubic rotations map a Lebedev grid onto itself. The fixed `cube90` control and single-axis angle ladder distinguish this from a claim that every larger angle must give a larger error. [U1, U2]

There is an additional check worth making. The implemented cavity volume is

\[
V=\frac13\sum_m A_m r_m\cdot n_m.
\]

For an exactly closed continuous surface, `sum A_m n_m=0`. A finite switched quadrature need not satisfy that discrete identity. Translating all positions by `t` gives, in this implementation,

\[
V' - V=\frac13 t\cdot\sum_m A_m n_m.
\]

The supplied item script measures this closure defect and verifies the identity using the actual volume function. This is a mathematical vulnerability, not a measured large volume error for the real 636 profiles. Its magnitude must be recorded before blaming volume for IDAC. It also explains why the co-rotation control rotates around the origin: centering and then rotating would mix pure rotation with translation sensitivity. [S6]

### Freeze exact inputs and run the primary panel

The historical test contains 25 compounds and 2,302 **occurrences** because it replaces one validation compound at a time. It is not necessarily 2,302 unique benchmark observations. Preserve that manifest. The current candidate CSV has an extra entry; the script freezes the historical set using only the saved key and temperature columns, not experimental response values.

```bash
cd "$TREE"
: "${REGISTRATION_COMMIT:?Register the fixed protocol before the native experiment}"
export EXP="$WORK/orientation"
python scripts/r3_orientation.py freeze --work "$EXP" \
  --geometry-dir "$REPO/data/pyscf_sigma/profiles_v2" \
  --registration "$REGISTRATION_COMMIT"
# Each iteration is also a complete independent runner task.
while read -r key; do
  for rot in id repeat r0 r1 r2 r3 r4 r5 r6 r7 cube90; do
    python scripts/r3_orientation.py item --work "$EXP" --key "$key" \
      --method raw --rotation "$rot"
  done
done < "$EXP/keys.txt"
# Fixed angle controls: water, methanol, decanoic acid, not selected from the results.
for key in XLYOFNOQVPJJNP-UHFFFAOYSA-N OKKJLVBELUTLKV-UHFFFAOYSA-N GHVNFZFCNZKVNT-UHFFFAOYSA-N; do
  for rot in a001 a01 a1 a5 a10; do
    python scripts/r3_orientation.py item --work "$EXP" --key "$key" \
      --method raw --rotation "$rot"
  done
done
```

Export/import the complete `$EXP` directory when splitting generation across runners; keep the frozen manifest and source hashes unchanged. The script refuses a silent reuse of an existing profile. Each native item calls the actual registered `cosmo_segments` and `to_profiles`, keeps the same spin convention, and reports its wall time, segment count, charge sum, profile moments, raw area and volume. It also saves the segment data for independent analysis. It does not reoptimize any geometry.

A source-file hash mismatch is a new experiment, not a warning to ignore. A saved `.xyz.json` is rounded by the production runner to five decimals. That is why identity and repeat identity are recomputed from the frozen saved coordinates. A mismatch between this identity and the old stored profile cannot all be attributed to rotation. [S13]

Run the prediction part only where UD exists:

```bash
test -d "$REPO/data/raw/nist/UD/sigma3"
python scripts/r3_orientation.py score --work "$EXP" --profile-set UD \
  --out "$WORK/orient-score-UD"
for rot in id repeat r0 r1 r2 r3 r4 r5 r6 r7 cube90; do
  python scripts/r3_orientation.py score --work "$EXP" \
    --profile-set "$EXP/raw/$rot" --out "$WORK/orient-score-raw-$rot"
done
args=()
for rot in repeat r0 r1 r2 r3 r4 r5 r6 r7 cube90; do
  args+=(--candidate "$rot=$WORK/orient-score-raw-$rot/values.csv")
done
python scripts/r3_orientation.py compare \
  --reference "$WORK/orient-score-raw-id/values.csv" "${args[@]}" \
  --out "$WORK/orient-compare-raw"
```

The generated `row_deltas.csv` and `comparison.json` report both activity models, role-specific changes, and exact finite coverage. Every target/profile-set combination uses a separate process. Strictly, `load_fluid` caches `(inchikey, explicit sigma_dir)`; the **environment override directory** is missing from that key. The separate-process rule avoids that actual hazard and prevents accidentally reusing a model instance initialized from another profile set. [S8]

The primary comparison substitutes one compound into a UD background, matching the historical acceptance design. Repeat it with `--background "$OPEN_PROFILES"` and an explicit identity profile set to assess the same compounds in the open background. The worker requires every partner profile in that background instead of silently substituting UD. This is a sensitivity panel, not an estimate of orientation error for all 636 compounds.

For any fixed set of scored observations,

\[
|\operatorname{MAE}(\hat y_R)-\operatorname{MAE}(\hat y_I)|
\leq \operatorname{mean}|\hat y_R-\hat y_I|.
\]

Use this inequality on matching rows. An orientation-induced mean shift far below 0.138 on the actual 828-row comparison could rule out orientation as the whole explanation there. The 25-compound subset alone cannot establish that bound for unseen compounds or for simultaneously changing both profiles in every binary. Large sensitivity would establish an uncertainty problem, not prove that averaging improves experimental agreement.

### The A fixes and their tests

Canonical orientation costs almost nothing beyond one ordinary single point. `canonical_xyz` uses a mass-centered proper frame, fixes signs using atom-index-stable molecular anchors, and falls back to molecular anchors when principal moments are degenerate. Linear molecules receive an explicit one-dimensional representation. This handles the usual principal-axis sign/degeneracy failure, but it is **not atom-permutation canonicalization** and can be nonsmooth when a geometry crosses an anchor or degeneracy threshold. Use it only for the terminal single-point protocol, not inside a gradient optimizer. It removes an arbitrary input-orientation choice for a fixed atom ordering; it does not remove the locked-in angular quadrature bias.

```bash
while read -r key; do
  for rot in id r0 r1 r2 r3 r4 r5 r6 r7; do
    python scripts/r3_orientation.py item --work "$EXP" --key "$key" \
      --method canonical --rotation "$rot"
  done
done < "$EXP/keys.txt"
```

Rotation averaging uses the arithmetic average of the **raw area bins**, with area equal to their sum and volume averaged consistently. Averaging normalized profiles while separately averaging area would define a different weighting. `ln gamma(mean profile)` is generally not `mean ln gamma(profile)`. The first is the candidate implemented here. A finite eight-rotation set is not exactly invariant under arbitrary rotations, and no `1/sqrt(8)` improvement is promised for deterministic quadrature error.

```bash
python scripts/r3_orientation.py average --work "$EXP" --method mean8
# Predeclared disjoint extension for consistency, not a redraw after seeing the first eight.
while read -r key; do
  for rot in r8 r9 r10 r11 r12 r13 r14 r15; do
    python scripts/r3_orientation.py item --work "$EXP" --key "$key" \
      --method raw --rotation "$rot"
  done
done < "$EXP/keys.txt"
python scripts/r3_orientation.py average --work "$EXP" --method mean8b
python scripts/r3_orientation.py average --work "$EXP" --method mean16
```

Lebedev 41 uses 590 points per atom versus 302 at order 29. In PySCF's SWIG scheme, increasing the order also decreases `R_sw/R = sqrt(14/N)` and changes the charge exponent table. Consequently, this is not just a denser integration of an otherwise identical finite cavity. Dense surface memory scales approximately as `(590/302)^2 = 3.82`; a dense factorization term would scale as the cube, about 7.46. These are component/storage estimates, not a whole-SCF runtime forecast. The surface-integral cache and the dense Hsieh matrices need separate memory accounting. [U1, U2]

```bash
while read -r key; do
  for rot in id r0 r1 r2 r3 r4 r5 r6 r7; do
    python scripts/r3_orientation.py item --work "$EXP" --key "$key" \
      --method lebedev41 --rotation "$rot"
  done
done < "$EXP/keys.txt"
```

Score each completed candidate directory, then run the fixed gates. The following function covers the two single-orientation recipes:

```bash
score_recipe () {
  local method="$1"
  for rot in id r0 r1 r2 r3 r4 r5 r6 r7; do
    python scripts/r3_orientation.py score --work "$EXP" \
      --profile-set "$EXP/$method/$rot" --out "$WORK/score-$method-$rot"
  done
  local args=()
  for rot in r0 r1 r2 r3 r4 r5 r6 r7; do
    args+=(--candidate "$rot=$WORK/score-$method-$rot/values.csv")
  done
  python scripts/r3_orientation.py compare \
    --reference "$WORK/score-$method-id/values.csv" "${args[@]}" \
    --out "$WORK/compare-$method"
  python scripts/r3_gate.py profiles --mode A --max-change .05 \
    --reference "$WORK/orient-score-raw-id/values.csv" \
    --candidate "$WORK/score-$method-id/values.csv" \
    --ud "$WORK/orient-score-UD/values.csv" \
    --reference-dir "$EXP/raw/id" --candidate-dir "$EXP/$method/id" \
    --out "$WORK/gate-$method.json"
}
score_recipe canonical
python scripts/r3_gate.py panel --reference "$WORK/orient-compare-raw/comparison.json" \
  --candidate "$WORK/compare-canonical/comparison.json" --bound .001 \
  --out "$WORK/gate-canonical-rotation.json"
score_recipe lebedev41
python scripts/r3_gate.py panel --reference "$WORK/orient-compare-raw/comparison.json" \
  --candidate "$WORK/compare-lebedev41/comparison.json" --bound .01 --ratio .5 \
  --out "$WORK/gate-lebedev41-rotation.json"
for method in mean8 mean8b mean16; do
  python scripts/r3_orientation.py score --work "$EXP" \
    --profile-set "$EXP/$method/id" --out "$WORK/score-$method"
done
python scripts/r3_gate.py profiles --mode A --max-change .05 \
  --reference "$WORK/orient-score-raw-id/values.csv" \
  --candidate "$WORK/score-mean8/values.csv" --ud "$WORK/orient-score-UD/values.csv" \
  --reference-dir "$EXP/raw/id" --candidate-dir "$EXP/mean8/id" \
  --out "$WORK/gate-mean8.json"
for model in cosmosac_dsp Z0x; do
  for spec in mean8b:.01 mean16:.005; do
    other="${spec%:*}"; bound="${spec#*:}"
    python scripts/r3_gate.py stability \
      --reference "$WORK/orient-score-raw-id/values.csv" \
      --reference-other "$WORK/orient-score-raw-id/values.csv" \
      --candidate "$WORK/score-mean8/values.csv" \
      --candidate-other "$WORK/score-$other/values.csv" \
      --model "$model" --bound "$bound" --out "$WORK/gate-mean8-$other-$model.json"
  done
done
```

The A compatibility gate requires unchanged finite coverage for both models, maximum COSMO-SAC-dsp change below 0.05 versus the fresh identity, and median difference from UD below 0.15. The independent stability conditions are in the registration. A raw identity already failing its historical acceptance statistic must be reported, not repaired by changing the new limits. The E gate remains available with `--mode E`; it checks raw and normalized bin differences below `1e-4` and both modeled ln-gamma changes below `1e-3`. No A recipe is predeclared to satisfy it.

Changing Hsieh's averaging radius, decay factor, or HB split is not recommended in this round. The existing distance-only averaging should first pass the co-rotation control. Broadening it to make the raw-bin plot smoother would alter the model and could conceal the underlying quadrature error. An algebraically equivalent blocked implementation could be E for memory reduction, but would not cure orientation sensitivity.

UD profiles are also finite numerical calculations, so some orientation sensitivity is plausible. Its size, handling of surface orientation, and comparability to this PySCF SWIG calculation are **not established** by the stored UD files. Reprocessing a co-rotated DMol3 segment table tests the parser only; it does not test regenerating that table after rotating the molecule. Establishing a DMol3 orientation error requires rerunning the original electronic/surface procedure at fixed geometry and settings. No DMol3 run or percent-level UD estimate is claimed here. [S7]

## P18 and the systematic open-versus-UD diagnostic

The current wrapper calls `p.get_outputs()`, then discards its metadata and reconstructs metadata with `p.get_meta()`. The former assigns `COOH` when `p.disp.has_COOH`; the latter does not. The wrapper restores water's special flag but not the acid flag. P18 adds an opt-in correction and a metadata-only reconstruction script using the same geometry-based NIST classifier. Its flag is also included in the profile-revision fingerprint, so a cached uncorrected profile cannot masquerade as a corrected one when the flag changes. The raw profile rows are copied unchanged. [S6, S7]

```bash
/usr/bin/time -p python scripts/r3_metadata.py \
  --profile-dir "$EXP/raw/id" --geometry-dir "$EXP/geometries" \
  --keys "$EXP/keys.txt" --registration "$REGISTRATION_COMMIT" \
  --out "$WORK/COOH-corrected"
python scripts/r3_orientation.py score --work "$EXP" \
  --profile-set "$WORK/COOH-corrected" --out "$WORK/score-COOH"
python scripts/r3_orientation.py compare \
  --reference "$WORK/orient-score-raw-id/values.csv" \
  --candidate "COOH=$WORK/score-COOH/values.csv" --out "$WORK/compare-COOH"
python - "$WORK/COOH-corrected/metadata_audit.json" \
  "$WORK/orient-score-raw-id/values.csv" "$WORK/score-COOH/values.csv" <<'PY'
import json,sys,numpy as np,pandas as pd
m=json.load(open(sys.argv[1])); unchanged={x['key'] for x in m['profiles'] if x['old_flag']==x['new_flag']}
a=pd.read_csv(sys.argv[2]).set_index('query'); b=pd.read_csv(sys.argv[3]).set_index('query').loc[a.index]
for model in ['cosmosac_dsp','Z0x']:
    x=a[model].to_numpy(); y=b[model].to_numpy(); valid=np.isfinite(x)
    assert np.array_equal(valid,np.isfinite(y))
    check=valid if model=='Z0x' else valid & a.key.isin(unchanged).to_numpy()
    assert not check.any() or np.max(np.abs(y[check]-x[check]))<1e-10
print('metadata invariants pass; COSMO-SAC-dsp acid changes still require reporting')
PY
```

After registration and acceptance, `ZC_R3_COOH_FLAG=1` enables the correction for newly generated profiles. The supplied reconstruction already applies it to its experimental copies without rerunning SCF. Report the old UD acceptance statistic again, including failure if the corrected metadata misses the thin 0.15 criterion. Do not restore the wrong flag to recover an acceptance margin. This is a numerical correction with potentially changed predictions, hence A under the unchanged rules.

The broader IDAC deficit cannot be assigned to a single cause from the available aggregate figures. The old acceptance gate measured median COSMO-SAC-dsp prediction differences for one substituted compound at a time. The exploratory score uses Z0x, changes both profiles, and covers a different population. A small median difference neither controls the tails of absolute error nor guarantees a small full-model MAE difference. [S2, S5, S8–S10]

Use the class/role audit and four-corner results to choose **which discrepancy to characterize**, not which parameter value improves experimental MAE. Before any new basis/radius/averaging experiment, export the existing observables for UD and open profiles:

```bash
python - "$EXP/keys.txt" "$EXP/raw/id" "$WORK/profile-observables.csv" <<'PY'
from pathlib import Path
import sys,pandas as pd
from zcosmo.cosmosac import sigma_path,SIGMA_DIR
from r3_common import profile_descriptors
rows=[]
for k in Path(sys.argv[1]).read_text().split():
    for source,p in [('open',Path(sys.argv[2])/f'{k}.sigma'),('UD',sigma_path(k,str(SIGMA_DIR)))]:
        if p is None: raise FileNotFoundError(k)
        rows.append(dict(key=k,source=source,**profile_descriptors(p)))
pd.DataFrame(rows).to_csv(sys.argv[3],index=False)
PY
```

Interpret the resulting differences as follows. A persistent shift in area/volume under otherwise stable orientation points toward cavity geometry or discretization conventions. A persistent difference in total profile shape or tail area at fixed geometry and radii points toward electronic/surface-charge conventions or basis effects. Differences between the total profile and its OH/OT partition require checking atom/HB assignment and the exact parser settings. The stored profile first moment is the first moment **after averaging and binning**, not the same observable as the raw PCM charge sum saved by the native item.

Water deserves early inspection because of its large acceptance discrepancy, but it must be tested in both roles and with both models. Keep BP86, the basis, project radii, dielectric limit, and Hsieh parameters fixed during the orientation study. A later geometry/basis/radius factorial must hold the other variables fixed and be separately registered. In particular, “def2-TZVP versus DMol3 DNP” is not a controlled basis-only comparison when geometry, cavity construction, and surface charges come from different programs. A matching BP label and nominal radii do not establish identical discretized Hamiltonians or cavity volumes. [S5–S7]

The existing Z0x dielectric table is not recomputed when a profile is swapped. However, the swapped volume changes volume fractions and the London contact distances. For the pure London contact term, a spherical contact diameter scales as `V^(1/3)`, so the `C6/d^6` magnitude scales as `V^-2`. This makes volume a meaningful diagnostic independently of raw-bin orientation differences. It is not evidence that volume actually accounts for the observed error without the row-level counterfactual results. [S8, S9]

## P19: one bounded final-stage precision experiment

The observation “energy changes are about 1e-7 Eh while conv_tol is 1e-8” is a reason to test SCF precision, not a measurement of a random energy-noise distribution. Deterministic quadrature error can repeat identically. The SCF stopping test and the geometry stopping test are different: in the pinned HF driver, an unspecified orbital-gradient tolerance becomes `sqrt(conv_tol)`, approximately `1e-4` at the original setting. Small energy changes alone need not imply equally well-converged gradients. [U4]

I propose tightening only SCF precision in the pre-stage, with `conv_tol=1e-11` and `conv_tol_grad=1e-7`, while retaining grid level 2 and the original PCM discretization. This isolates electronic convergence better than simultaneously changing grids and optimizer. A finer grid could be useful in a different trial, but changes the numerical objective and does not guarantee an easier original-grid confirmation. Tighter SCF cannot remove surface/XC quadrature error or repair an optimizer conditioning problem by itself.

`r3_precision.py` allocates at most 80 evaluations to that stage and at most 20 to an **original-setting Berny confirmation**. The control uses the original SCF settings in both stages, with the same fresh-history resets. The candidate does not inherit a Hessian whose history mixed old and new electronic tolerances. It never reads a `.bstate` file and never uses the rejected P15 override.

This uses `pyscf.geomopt.berny_solver.kernel(mf, maxsteps=..., callback=..., assert_convergence=True)` and checks the returned convergence flag. The callback checks SCF convergence before recording an evaluation. The pinned solver calls the callback before `optimizer.send`; the code does not treat the callback's pre-send optimizer flag as final convergence. Pyberny's convergence uses internal-coordinate gradients and steps, and rejects an on-sphere step. GeomeTRIC's Cartesian criteria cannot be made exactly identical merely by converting Å to bohr or matching threshold numbers, so another “mapped exactly” TRIC finish is not proposed. [U3–U5]

Run the 25-molecule last-stage calibration first, from the same frozen saved geometries:

```bash
for arm in control tight; do
  mkdir -p "$WORK/P19-$arm-profiles"
  while read -r key; do
    python scripts/r3_precision.py --input "$EXP/geometries/$key.xyz.json" \
      --key "$key" --arm "$arm" --registration "$REGISTRATION_COMMIT" \
      --out "$WORK/P19/$arm/$key"
    cp "$WORK/P19/$arm/$key/$key.sigma" "$WORK/P19-$arm-profiles/"
  done < "$EXP/keys.txt"
  python scripts/r3_orientation.py score --work "$EXP" \
    --profile-set "$WORK/P19-$arm-profiles" --out "$WORK/score-P19-$arm"
done
python scripts/r3_gate.py profiles --mode A --max-change .01 \
  --reference "$WORK/score-P19-control/values.csv" \
  --candidate "$WORK/score-P19-tight/values.csv" --ud "$WORK/orient-score-UD/values.csv" \
  --reference-dir "$WORK/P19-control-profiles" --candidate-dir "$WORK/P19-tight-profiles" \
  --out "$WORK/gate-P19-profiles.json"
python - "$WORK/P19" <<'PY'
from pathlib import Path
import json,sys
p=Path(sys.argv[1]); totals={}
for arm in ['control','tight']:
    r=[json.loads(f.read_text()) for f in sorted((p/arm).glob('*/result.json'))]
    assert len(r)==25 and all(x['original_berny_pass'] and x['evaluations']<=100 for x in r)
    totals[arm]=sum(x['wall_s'] for x in r)
assert totals['tight']<=1.50*totals['control'],totals
print(totals)
PY
```

The historical 25 do not include the triplet O2; the CLI exposes `--spin 2` for a separate O2 API/control calculation rather than silently running it as a singlet. Each individual key/arm invocation is an independent free-runner task. Keep the environment and hardware paired when using the wall-time ratio. Missing successful outputs reject the gate; a partial file is not a completed molecule.

Only after that gate passes, run the six frozen chain geometries in both arms. The following example explicitly uses the committed seed geometries, whose hashes must be archived before either arm; it does not claim those files are the S2 NEW artifacts. A different latest-seed directory requires its own frozen manifest before the comparison.

```bash
python - "$WORK/chain-inputs.json" <<'PY'
from pathlib import Path
from r3_common import STALL_KEYS,digest,write_json
rows=[]
for k in STALL_KEYS:
    p=Path('cloud/s19/seeds')/f'{k}.partial.json'
    rows.append(dict(key=k,path=str(p.resolve()),sha256=digest(p)))
write_json(__import__('sys').argv[1],rows)
PY
# Each key/arm is one task. On Linux runners, reserve time for saving artifacts.
python - "$WORK/chain-inputs.json" "$WORK" "$REGISTRATION_COMMIT" <<'PY'
import json,subprocess,sys
from pathlib import Path
from r3_common import digest,write_json
rows=json.load(open(sys.argv[1])); root=Path(sys.argv[2]); registration=sys.argv[3]; outcomes=[]
for r in rows:
    assert digest(r['path'])==r['sha256']
    for arm in ['control','tight']:
        out=root/'P19-chains'/arm/r['key']
        cmd=[sys.executable,'scripts/r3_precision.py','--input',r['path'],'--key',r['key'],
             '--arm',arm,'--registration',registration,'--out',str(out)]
        try:
            p=subprocess.run(cmd,timeout=19200)
            status='completed' if p.returncode==0 else ('censored_budget' if p.returncode==2 else 'failed')
        except subprocess.TimeoutExpired:
            status='censored_deadline'
        outcomes.append(dict(key=r['key'],arm=arm,status=status))
        write_json(root/'P19-chain-outcomes.json',outcomes)
PY
```

The loop is a local orchestration example; split its individual invocations across existing free runners instead of trying to put all twelve into one six-hour job. There is no automatic extension after inspecting a censored result. The registration requires at least one tight-arm original-confirmation success whose control remains censored, in addition to all 25 calibration gates. An SCF exception is a failure, not evidence of convergence. Only actual original-confirmation successes may replace flagged profiles after acceptance and explicit provenance recording.

No speed-up number is justified for a reference that never finished. Report gradient counts, SCF iterations, elapsed times, and the number of successful versus censored chains. If both arms converge because of a fresh-history reset, that does not establish a benefit from tighter SCF. If neither converges, close this trial rather than searching a series of tolerances on the same outcomes.

## Unrun round-2 work: revised order and scope

| Order | Candidate | Decision now | Reason and required gate |
|---:|---|---|---|
| 1 | P14 | Run the diagnostic sidecar | LLE still matters. Finite initial evaluations do not establish successful root refinement, small residuals, or global phase stability. Preserve predictions while recording failures. |
| 2 | H2 | Run native API checks and one targeted timing, not another broad campaign | Establish the actual post-P9 cost of the single-point work used by P17. The old cumulative profile is not this measurement. |
| 3 | P11 | Conditional small pilot | Stored DF-J can help repeated SCF J builds in hundreds of new single points. Require fixed-geometry energy/gradient/q checks, memory reporting, and the original E gate. Drop if the paired saving does not repay validation. |
| 4 | P10 | Defer until P19 or another gradient workload is justified | Its saved `ip2` pass affects gradients, not the majority of terminal profile single points in the orientation panel. It is not disproven. |
| 5 | P13 | Drop from this round's active queue | Native integrals already have OpenMP; extra block parallelism is speculative and adds memory/concurrency complexity. Revisit only after a measured bottleneck. |
| 6 | P12 | Drop from this round's active queue | Stronger checkpoint fidelity remains worthwhile engineering, but short-restart arithmetic no longer blocks coverage. The bounded P19 experiment deliberately uses fresh histories and does not need this implementation. |

P10/P11/P12/P13 have not been rejected by evidence; “defer/drop from this queue” is a resource decision. P15, in contrast, was actually tested and rejected. [S2, S3]

For the retained candidates, extract the original diffs from the repository's round-2 report. Do not assume a stale patch applies merely because its name is unchanged:

```bash
python - "$REPO/docs/astra/round2/ZCOSMO_ROUND2_REPORT.md" "$WORK/r2-patches" <<'PY'
from pathlib import Path
import re,sys
out=Path(sys.argv[2]);out.mkdir()
for name,body in re.findall(r'<!-- PATCH:(H2|P1[0-5]) -->\s*```diff\n(.*?)\n```',Path(sys.argv[1]).read_text(),re.S):
    (out/(name+'.patch')).write_text(body+'\n')
PY
# In a separate experiment tree, after a successful --check:
git apply --check "$WORK/r2-patches/H2.patch"
git apply "$WORK/r2-patches/H2.patch"
git apply --check "$WORK/r2-patches/P14.patch"
git apply "$WORK/r2-patches/P14.patch"
python scripts/round2_check.py --help
# In this separate tree, not in the already frozen P17 experiment:
for arm in audit-off audit-on; do
  mkdir -p "$WORK/lle-$arm"
  if [ "$arm" = audit-on ]; then
    export ZC_LLE_AUDIT_DIR="$WORK/lle-audit"
  else
    unset ZC_LLE_AUDIT_DIR
  fi
  ZC_PRED="$WORK/lle-$arm" python -m zcosmo.evaluate Z0x --tables lle --split all
done
unset ZC_LLE_AUDIT_DIR
python - "$WORK" <<'PY'
from pathlib import Path
import pandas as pd,sys
w=Path(sys.argv[1])
pd.testing.assert_frame_equal(pd.read_csv(w/'lle-audit-off/Z0x__lle__all.csv'),
                             pd.read_csv(w/'lle-audit-on/Z0x__lle__all.csv'),check_exact=True)
print('P14 on/off predictions identical')
PY
# P11 is a separate optional pilot. Do not mistake a no-op flag for a test.
git apply --check "$WORK/r2-patches/P11.patch"
git apply "$WORK/r2-patches/P11.patch"
python scripts/round2_check.py fixed --flag ZC_DF_STORE --out "$WORK/P11-fixed.json"
ZC_DF_STORE=0 python scripts/round2_check.py trace --smiles CCCCCCCCO --cycles 3 --out "$WORK/P11-base"
ZC_DF_STORE=1 python scripts/round2_check.py trace --xyz "$WORK/P11-base/start.json" --cycles 3 --out "$WORK/P11-candidate"
# Native checks were not run here; a microcheck does not replace the 25-profile E gate.
```

For a prospective performance decision, use actual remaining work. If there are `N` remaining single points, P11 pays for its validation only when `N × (t_reference - t_candidate)` exceeds the validation and integration cost. Its component model is still `I × t_direct_J` versus `t_build + I × t_stored_J`; a benefit on one molecule does not establish a full-panel speed-up. No old 1.6–3× PCM estimate is reused.

## Additional audit findings and limits

S2's `s2_item.py` records a Cartesian component maximum as “maximum atomic displacement.” Its 0.02 Å perturbation is also normalized by the maximum component, so the maximum atomwise Euclidean displacement can be as large as `sqrt(3) × 0.02 Å`. The recorded old/new component maxima are sufficiently small that this bound alone does not overturn their 0.005 Å displacement condition. The perturbation control's stated size should be corrected in later reporting. [S4]

The S2 gradient item does not explicitly assert SCF convergence before recording the gradient; `s2_evaluate` accepts the first matching artifact path and hardcodes the 100-evaluation separation. Its ln-gamma condition also treats an empty finite intersection like a genuinely zero-row compound when masks match. A nonempty all-nonfinite query set should be reported as unavailable, not used as positive evidence. These are audit defects, not proof that the recorded six-chain decisions were wrong. Confirm the existing job logs and artifact lineage; do not rewrite historical decisions from a source-code suspicion. [S4]

The existing fallback path may mix open and UD partners when an override directory is incomplete. The new open-background and hybrid workers require exact partner files and record their resolution. The sidecar code does not assume that changing an environment variable clears cached fluids. [S4, S8]

The S2 test deliberately tolerated changes below a typical rotation difference. It established the registered operational condition, not distance to an unknown exactly converged profile. Its raw-bin comparison also failed to resolve the report-only perturbation at the claimed scale. The new orientation study must not be used retrospectively to change S1, S2, or the rejected P15 outcome. [S2, S5]

LLE `gap_found_systems` is a detection statistic on positive two-phase systems. It is not balanced accuracy, which also needs negative systems. The round-3 .84/.82 comparison should retain that label. P14 can make numerical fallback outcomes visible, but a changed denominator, a new binodal algorithm, or removal of failed systems is a separate scored numerical correction. [S10, S11]

## Implementation diffs

The following six patches are complete. H3 is shared code; P16 through P19 and REG are independently represented against the pinned source. All may be applied together for experimentation. P18 leaves its production behavior unchanged unless the explicit A flag is enabled. The native commands, not the portable tests or the source inspection, decide adoption.


### H3

<!-- PATCH:H3 -->
```diff
--- /dev/null
+++ b/scripts/r3_common.py
@@ -0,0 +1,152 @@
+"""Round-3 audit utilities. No model parameters and no production writes."""
+from __future__ import annotations
+import hashlib
+import json
+from pathlib import Path
+import numpy as np
+import pandas as pd
+
+BASE = 'c515e38e1a7fd91a02e1ff1f1209a81b67a7d49d'
+STALL_KEYS = (
+ 'BTFJIXJJCSYFAL-UHFFFAOYSA-N', 'FLIACVVOZYBSBS-UHFFFAOYSA-N',
+ 'HPEUJPJOZXNMSJ-UHFFFAOYSA-N', 'MVLVMROFTAUDAG-UHFFFAOYSA-N',
+ 'OYHQOLUKZRVURQ-HZJYTTRNSA-N', 'PYGXAGIECVVIOZ-UHFFFAOYSA-N')
+WATER = 'XLYOFNOQVPJJNP-UHFFFAOYSA-N'
+
+def digest(path):
+    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
+
+def write_json(path, obj):
+    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
+    tmp = path.with_name(path.name + '.tmp')
+    tmp.write_text(json.dumps(obj, indent=2, allow_nan=False) + '\n')
+    tmp.replace(path)
+
+def scalar(x):
+    if pd.isna(x): return None
+    if isinstance(x, (float, np.floating)): return format(float(x), '.12g')
+    if isinstance(x, (int, np.integer)): return str(int(x))
+    return str(x)
+
+def row_ids(df, prediction='pred_ln_gamma_inf'):
+    """Observation identity, not (solute, solvent, T) alone. Refuse ambiguous duplicates."""
+    required = ['file', 'dataset', 'solute', 'solvent', 'T', 'method', 'ln_gamma_inf', 'split']
+    missing = set(required) - set(df)
+    if missing: raise ValueError(f'missing observation identity fields: {sorted(missing)}')
+    payload = [json.dumps([scalar(v) for v in row], separators=(',', ':'))
+               for row in df[required].itertuples(index=False, name=None)]
+    base = pd.Series([hashlib.sha256(p.encode()).hexdigest() for p in payload], index=df.index)
+    if prediction in df:
+        for _, idx in base.groupby(base).groups.items():
+            vals = df.loc[idx, prediction].to_numpy(float)
+            if len(vals) > 1 and not np.all((vals == vals[0]) | (np.isnan(vals) & np.isnan(vals[0]))):
+                raise ValueError('indistinguishable duplicate observations have different predictions; attach original row IDs')
+    occ = base.groupby(base).cumcount().astype(str)
+    return (base + ':' + occ).to_numpy(str)
+
+def keyed(df):
+    df = df.reset_index(drop=True).copy()
+    df['r3_row_id'] = row_ids(df)
+    return df.set_index('r3_row_id', drop=False)
+
+def select_split(df, split):
+    if df['split'].isna().any(): raise ValueError('missing split labels are not a test set')
+    if not df['split'].isin(['train', 'test_one', 'test_both']).all():
+        raise ValueError('unexpected split labels; use a separately declared manifest')
+    if split == 'all': return df
+    if split == 'test': return df[df['split'] != 'train']
+    if split in ('train', 'test_one', 'test_both'): return df[df['split'] == split]
+    raise ValueError(split)
+
+def system_ids(df):
+    a, b = df.solute.to_numpy(str), df.solvent.to_numpy(str)
+    return np.where(a < b, a + '|' + b, b + '|' + a)
+
+def cluster_ci(values, systems, seed=7, repeats=1000):
+    """Mean of row values; pairs, rather than rows, are resampled."""
+    values = np.asarray(values, float)
+    if not len(values): return None
+    u, inv = np.unique(np.asarray(systems, str), return_inverse=True)
+    groups = [np.flatnonzero(inv == j) for j in range(len(u))]
+    rng = np.random.default_rng(seed)
+    means = [float(values[np.concatenate([groups[j] for j in rng.integers(len(u), size=len(u))])].mean())
+             for _ in range(repeats)]
+    return np.quantile(means, [.025, .975]).tolist()
+
+def read_sigma(path):
+    path = Path(path)
+    lines = path.read_text().splitlines()
+    if not lines or not lines[0].startswith('# meta: '): raise ValueError(f'invalid profile header: {path}')
+    meta = json.loads(lines[0][8:]); a = np.loadtxt(path)
+    if a.shape != (153, 2) or not np.isfinite(a).all(): raise ValueError(f'invalid profile: {path}')
+    grid, p = a[:, 0].reshape(3,51), a[:,1].reshape(3,51)
+    if not np.allclose(grid, np.linspace(-.025,.025,51)[None,:], atol=1e-12, rtol=0):
+        raise ValueError('sigma grid changed')
+    if (p < 0).any() or p.sum() <= 0 or not np.isfinite(meta['volume [A^3]']) or meta['volume [A^3]'] <= 0:
+        raise ValueError('nonphysical profile')
+    return grid[0], p, meta
+
+def profile_descriptors(path):
+    s, p, m = read_sigma(path); A = float(p.sum()); normalized = p / A
+    out = dict(area_A2=A, volume_A3=float(m['volume [A^3]']),
+               normalization=1., net_sigma_moment=float((p*s).sum()),
+               sigma_second_moment=float((normalized*s*s).sum()),
+               tail_area_A2=float(p[:,abs(s)>=.01].sum()),
+               flag=m.get('disp. flag'), averaging=m.get('averaging'),
+               r_av_A=m.get('r_av [A]'), f_decay=m.get('f_decay'),
+               source_sha256=digest(path))
+    for j, block in enumerate(('NHB','OH','OT')):
+        out[block+'_area_A2'] = float(p[j].sum())
+    return out
+
+def write_sigma(path, sigma, p, meta):
+    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
+    with path.open('w') as f:
+        f.write('# meta: ' + json.dumps(meta, allow_nan=False) + '\n')
+        f.write('# sigma [e/A^2] psigmaA [A^2]; NHB, OH, OT\n')
+        for block in p:
+            for s, a in zip(sigma, block): f.write(f'{s:.3f} {a:.14e}\n')
+
+def rotations():
+    from scipy.spatial.transform import Rotation
+    # First eight reproduce S2 exactly; r8..r15 are a predeclared extension, not a redraw.
+    ans = {'id': np.eye(3), 'repeat': np.eye(3)}
+    ans.update({f'r{i}': q for i,q in enumerate(Rotation.random(16, random_state=20261004).as_matrix())})
+    axis=np.array([1.,2.,3.]); axis/=np.linalg.norm(axis)
+    for label, angle in [('a001',.001),('a01',.01),('a1',.1),('a5',.5),('a10',1.)]:
+        ans[label]=Rotation.from_rotvec(angle*axis).as_matrix()
+    ans['cube90']=Rotation.from_euler('x',90,degrees=True).as_matrix()
+    return ans
+
+def canonical_xyz(x, weights=None):
+    """Proper, fixed-atom-order body frame; degenerate inertia uses molecular anchors.
+
+    This does NOT claim chemical atom-permutation canonicalization. Centering and
+    reorientation change the finite quadrature and are an A protocol.
+    """
+    x=np.asarray(x,float)
+    if x.ndim!=2 or x.shape[1]!=3 or not np.isfinite(x).all(): raise ValueError('invalid coordinates')
+    w=np.ones(len(x)) if weights is None else np.asarray(weights,float)
+    if w.shape!=(len(x),) or (w<=0).any(): raise ValueError('invalid weights')
+    y=x-np.average(x,axis=0,weights=w)
+    I=np.eye(3)*np.sum(w[:,None]*y*y)-(y*w[:,None]).T@y
+    vals, vecs=np.linalg.eigh(I)
+    def choose(scores):
+        # Atom-index tie breaking is invariant to rotation within this relative tolerance.
+        mx=float(np.max(scores)); tol=1e-10*max(mx,1.)
+        return int(np.flatnonzero(scores>=mx-tol)[0])
+    if np.max(np.linalg.norm(y,axis=1)) < 1e-12: return np.zeros_like(y)
+    separated=np.min(np.diff(vals))>1e-8*max(float(np.max(abs(vals))),1.)
+    if separated:
+        e1,e2=vecs[:,0].copy(),vecs[:,1].copy()
+        for e in (e1,e2):
+            pr=y@e; j=choose(abs(pr))
+            if pr[j]<0: e*=-1
+    else:
+        e1=y[choose(np.sum(y*y,axis=1))].copy(); e1/=np.linalg.norm(e1)
+        ort=y-np.outer(y@e1,e1); j=choose(np.sum(ort*ort,axis=1))
+        if np.linalg.norm(ort[j])<1e-10:
+            return np.c_[y@e1,np.zeros((len(y),2))]  # Linear molecules, no arbitrary transverse axis.
+        e2=ort[j]/np.linalg.norm(ort[j])
+    e3=np.cross(e1,e2); e3/=np.linalg.norm(e3); e2=np.cross(e3,e1)
+    return y@np.column_stack([e1,e2,e3])
--- /dev/null
+++ b/scripts/r3_gate.py
@@ -0,0 +1,78 @@
+"""Explicit numeric gates; no experimental response values are loaded here."""
+from __future__ import annotations
+import argparse
+import json
+from pathlib import Path
+import numpy as np
+import pandas as pd
+from r3_common import read_sigma,write_json
+
+def paired(reference,candidate,model):
+    r=pd.read_csv(reference).set_index('query'); c=pd.read_csv(candidate).set_index('query')
+    if not r.index.is_unique or not c.index.is_unique or set(r.index)!=set(c.index): raise ValueError('query mismatch')
+    if len(r)!=2302: raise ValueError('expected historical 2302 occurrences')
+    c=c.loc[r.index]; x=r[model].to_numpy(float); y=c[model].to_numpy(float); ok=np.isfinite(x)
+    if not np.array_equal(ok,np.isfinite(y)) or not ok.any(): raise ValueError('changed or empty finite coverage')
+    return r,c,ok,abs(y[ok]-x[ok])
+
+def profiles(a):
+    r,c,ok,dc=paired(a.reference,a.candidate,'cosmosac_dsp')
+    _,_,_,dz=paired(a.reference,a.candidate,'Z0x')
+    ud=pd.read_csv(a.ud).set_index('query')
+    if set(ud.index)!=set(r.index): raise ValueError('UD query mismatch')
+    u=ud.loc[r.index,'cosmosac_dsp'].to_numpy(float); y=c.cosmosac_dsp.to_numpy(float)
+    uu=ok&np.isfinite(u)
+    if not uu.any(): raise ValueError('UD comparison empty')
+    max_raw=0.;max_norm=0.;max_area=0.;max_vol=0.
+    keys=sorted(r.key.unique())
+    if len(keys)!=25: raise ValueError('expected 25 keys')
+    for k in keys:
+        _,p,pm=read_sigma(Path(a.reference_dir)/f'{k}.sigma')
+        _,q,qm=read_sigma(Path(a.candidate_dir)/f'{k}.sigma')
+        max_raw=max(max_raw,float(abs(p-q).max()));max_norm=max(max_norm,float(abs(p/p.sum()-q/q.sum()).max()))
+        max_area=max(max_area,float(abs(p.sum()-q.sum())));max_vol=max(max_vol,abs(pm['volume [A^3]']-qm['volume [A^3]']))
+    med=float(np.median(abs(y[uu]-u[uu])))
+    passed=bool(max_raw<1e-4 and max_norm<1e-4 and dc.max()<1e-3 and dz.max()<1e-3) if a.mode=='E' else bool(dc.max()<a.max_change and med<.15)
+    report=dict(mode=a.mode,keys=25,rows=2302,finite_cosmosac=int(ok.sum()),UD_comparisons=int(uu.sum()),
+        max_delta_lngamma_cosmosac=float(dc.max()),max_delta_lngamma_Z0x=float(dz.max()),median_cosmosac_vs_UD=med,
+        max_raw_bin_A2=max_raw,max_normalized_bin=max_norm,max_area_A2=max_area,max_volume_A3=max_vol,passed=passed)
+    write_json(a.out,report)
+    if not passed: raise SystemExit('profile numeric gate failed; nothing is adopted')
+
+def stability(a):
+    _,_,_,b=paired(a.reference,a.reference_other,a.model)
+    _,_,_,c=paired(a.candidate,a.candidate_other,a.model)
+    bm=float(b.max());cm=float(c.max())
+    passed=cm<a.bound and (a.ratio is None or cm<=a.ratio*bm)
+    write_json(a.out,dict(model=a.model,reference_max=bm,candidate_max=cm,bound=a.bound,ratio=a.ratio,passed=bool(passed)))
+    if not passed: raise SystemExit('stability gate failed')
+
+def panel(a):
+    b=json.loads(Path(a.reference).read_text()); c=json.loads(Path(a.candidate).read_text())
+    if not b['coverage_pass'] or not c['coverage_pass']: raise ValueError('coverage failed')
+    result=[]
+    for model in ('cosmosac_dsp','Z0x'):
+        maxima=[]
+        for doc in (b,c):
+            rows=[r for r in doc['summaries'] if r['model']==model and 'role' not in r and r['label'] in [f'r{i}' for i in range(8)]]
+            if len(rows)!=8 or len({r['label'] for r in rows})!=8 or any(r['max_abs'] is None for r in rows): raise ValueError('requires all eight fixed rotations')
+            maxima.append(max(r['max_abs'] for r in rows))
+        bm,cm=maxima
+        result.append(dict(model=model,reference_max=bm,candidate_max=cm,passed=bool(cm<a.bound and (a.ratio is None or cm<=a.ratio*bm))))
+    write_json(a.out,dict(bound=a.bound,ratio=a.ratio,results=result))
+    if not all(r['passed'] for r in result): raise SystemExit('orientation panel gate failed')
+
+def main():
+    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
+    q=s.add_parser('profiles')
+    for name in ('reference','candidate','ud','reference-dir','candidate-dir','out'): q.add_argument('--'+name,required=True)
+    q.add_argument('--mode',choices=['E','A'],required=True);q.add_argument('--max-change',type=float,default=.05)
+    q=s.add_parser('stability')
+    for name in ('reference','reference-other','candidate','candidate-other','out'):q.add_argument('--'+name,required=True)
+    q.add_argument('--bound',type=float,required=True);q.add_argument('--ratio',type=float)
+    q.add_argument('--model',choices=['cosmosac_dsp','Z0x'],default='cosmosac_dsp')
+    q=s.add_parser('panel')
+    for name in ('reference','candidate','out'):q.add_argument('--'+name,required=True)
+    q.add_argument('--bound',type=float,required=True);q.add_argument('--ratio',type=float)
+    a=p.parse_args();globals()[a.cmd](a)
+if __name__=='__main__':main()
--- /dev/null
+++ b/scripts/r3_selftest.py
@@ -0,0 +1,101 @@
+"""Portable regression tests. No native PySCF or UD data is exercised by these tests."""
+from __future__ import annotations
+import argparse
+import ast
+import contextlib
+import importlib.util
+import io
+import json
+from pathlib import Path
+import subprocess
+import sys
+import tempfile
+from types import SimpleNamespace
+import numpy as np
+import pandas as pd
+from scipy.spatial.distance import cdist
+from scipy.spatial.transform import Rotation
+from r3_common import canonical_xyz,rotations,keyed,write_sigma,read_sigma,write_json
+from r3_idac import chemical_class
+
+def run(a):
+    result={};rng=np.random.default_rng(19)
+    cases=[np.array([[0,0,0],[0,.76,.59],[0,-.76,.59]]),np.array([[0,0,0],[0,0,1.21]]),
+           np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]]),rng.normal(size=(10,3))]
+    error=0.
+    for x in cases:
+        for R in Rotation.random(100,random_state=7).as_matrix():
+            error=max(error,float(abs(canonical_xyz(x@R.T+[5,-2,3])-canonical_xyz(x)).max()))
+    if error>=1e-10: raise AssertionError('body frame is not rotation covariant')
+    result['canonical_max_coordinate_difference_A']=error
+    result['canonical_test_geometries']=len(cases);result['rotations_per_geometry']=100
+    if not np.array_equal(np.array([rotations()[f'r{i}'] for i in range(8)]),Rotation.random(8,random_state=20261004).as_matrix()):
+        raise AssertionError('S2 rotations not reproduced')
+    # Formula-level test of Hsieh averaging on a co-rotated FIXED segment set.
+    x=rng.normal(size=(40,3));areas=rng.uniform(.01,1,40);sig=rng.normal(0,.003,40);rn2=areas/np.pi;rav=7.25/np.pi
+    def avg(y):
+        M=np.exp(-3.57*cdist(y,y)**2/(rn2+rav))*rn2*rav/(rn2+rav)
+        return (M*sig).sum(1)/M.sum(1)
+    er=float(abs(avg(x)-avg(x@rotations()['r0'].T)).max())
+    if er>1e-12: raise AssertionError('Hsieh formula co-rotation test failed')
+    result['Hsieh_formula_max_difference_e_A2']=er
+    # Four-corner Shapley identity, including the nonlinear absolute-error transformation.
+    uu,ou,uo,oo,obs=rng.normal(size=(5,50));s=.5*((ou-uu)+(oo-uo));v=.5*((uo-uu)+(oo-ou))
+    if abs(s+v-(oo-uu)).max()>1e-12: raise AssertionError('prediction attribution')
+    e=[abs(t-obs) for t in (uu,ou,uo,oo)];es=.5*((e[1]-e[0])+(e[3]-e[2]));ev=.5*((e[2]-e[0])+(e[3]-e[1]))
+    if abs(es+ev-(e[3]-e[0])).max()>1e-12: raise AssertionError('error attribution')
+    result['Shapley_identity_pass']=True
+    if chemical_class('CC(=O)O')!='carboxylic_acid' or chemical_class('O')!='water' or chemical_class('CC(=O)OC')!='ester': raise AssertionError('fixed structural classes')
+    with tempfile.TemporaryDirectory(prefix='r3-test-') as td:
+        t=Path(td); rows=[]
+        for i in range(30):
+            rows.append(dict(file=f'{i}.xml',dataset=i,solute=['k1','k2','k3'][i%3],solvent=['k3','k1','k2'][i%3],
+                T=298.15,method='synthetic',ln_gamma_inf=i/30,split='train' if i<6 else 'test_one',pred_ln_gamma_inf=i/30+.2))
+        r=pd.DataFrame(rows);c=r.copy();c.pred_ln_gamma_inf+=.1
+        c=c.sample(frac=1,random_state=8).reset_index(drop=True)
+        r.to_csv(t/'ref.csv',index=False);c.to_csv(t/'candidate.csv',index=False)
+        pd.DataFrame(dict(inchikey=['k1','k2','k3'],smiles=['O','CO','CCCC'])).to_csv(t/'compounds.csv',index=False)
+        scripts=Path(__file__).resolve().parent
+        subprocess.run([sys.executable,str(scripts/'r3_idac.py'),'audit','--reference',str(t/'ref.csv'),
+            '--candidate',str(t/'candidate.csv'),'--compounds',str(t/'compounds.csv'),'--out',str(t/'audit'),
+            '--expect-points','24'],check=True,stdout=subprocess.DEVNULL)
+        report=json.loads((t/'audit/audit.json').read_text())
+        if report['same_row_identity_and_order'] or abs(report['common']['delta_mae']-.1)>1e-12: raise AssertionError('identity alignment failed')
+        for group in ('solute_class','solvent_class','water_role'):
+            table=pd.read_csv(t/f'audit/by_{group}.csv')
+            if abs(table.contribution_to_total_delta_mae.sum()-.1)>1e-12: raise AssertionError('nonadditive class contributions')
+        result['reordered_IDAC_rows_joined']=24
+        duplicate=pd.concat([r.iloc[[0]],r.iloc[[0]]],ignore_index=True);duplicate.loc[1,'pred_ln_gamma_inf']+=1
+        try:keyed(duplicate)
+        except ValueError:pass
+        else:raise AssertionError('ambiguous duplicate was accepted')
+        bad=c.copy();bad.loc[0,'pred_ln_gamma_inf']=np.inf;bad.to_csv(t/'bad.csv',index=False)
+        f=subprocess.run([sys.executable,str(scripts/'r3_idac.py'),'compare-fresh','--reference',str(t/'ref.csv'),
+            '--candidate',str(t/'bad.csv'),'--out',str(t/'no.json')],capture_output=True)
+        if f.returncode==0:raise AssertionError('nonfinite mismatch accepted')
+        result['duplicate_and_nonfinite_guards_pass']=True
+        grid=np.linspace(-.025,.025,51);p=rng.uniform(size=(3,51))
+        meta={'volume [A^3]':100.,'area [A^2]':float(p.sum()),'disp. flag':'NHB'}
+        write_sigma(t/'a.sigma',grid,p,meta);_,q,_=read_sigma(t/'a.sigma')
+        if abs(p-q).max()>1e-13:raise AssertionError('profile round trip')
+        result['sigma_round_trip_max_A2']=float(abs(p-q).max())
+    # Version-sensitive calls are source-shape checks, NOT native API executions.
+    tree=ast.parse((Path(__file__).parent/'r3_precision.py').read_text())
+    kernels=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='kernel']
+    if len(kernels)!=1 or {k.arg for k in kernels[0].keywords}!={'maxsteps','callback','assert_convergence'}:raise AssertionError('unexpected Berny interface')
+    result['precision_budget']=dict(pre=80,original_confirmation=20)
+    # Exercise the actual repository volume routine when an explicit source copy is supplied.
+    if a.volume_source:
+        spec=importlib.util.spec_from_file_location('r3_volume_source',a.volume_source);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
+        xyz=np.array([[0.,0.,0.]]);r=rng.normal(size=(20,3));r/=np.linalg.norm(r,axis=1)[:,None];r*=2
+        area=rng.uniform(size=20);seg=dict(xyz=r/m.BOHR,area=area,atom=np.zeros(20,dtype=int))
+        shift=np.array([1.,2.,3.]);s2=dict(seg,xyz=(r+shift)/m.BOHR)
+        obs=m.cavity_volume(s2,(xyz+shift)/m.BOHR)-m.cavity_volume(seg,xyz/m.BOHR)
+        pred=shift@((r/2)*area[:,None]).sum(0)/3
+        if abs(obs-pred)>1e-12:raise AssertionError('finite-surface volume translation identity')
+        result['actual_volume_function_translation_identity_error_A3']=float(abs(obs-pred))
+    write_json(a.out,result);print(json.dumps(result,indent=2))
+
+def main():
+    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--volume-source');run(p.parse_args())
+if __name__=='__main__':main()
```

### P16

<!-- PATCH:P16 -->
```diff
--- /dev/null
+++ b/scripts/r3_idac.py
@@ -0,0 +1,160 @@
+"""Stored-prediction provenance, common-subset, and descriptive class/role audits.
+
+Never edits predictions or model constants. Run where the stored CSVs exist.
+"""
+from __future__ import annotations
+import argparse
+import json
+from pathlib import Path
+import time
+import numpy as np
+import pandas as pd
+from r3_common import (digest, keyed, select_split, system_ids, cluster_ci,
+                       write_json, STALL_KEYS, WATER)
+
+PRED='pred_ln_gamma_inf'
+
+def chemical_class(smiles):
+    from rdkit import Chem
+    m=Chem.MolFromSmiles(smiles)
+    if m is None: raise ValueError(f'invalid SMILES: {smiles}')
+    atoms=[a.GetAtomicNum() for a in m.GetAtoms() if a.GetAtomicNum()!=1]
+    if atoms==[8]: return 'water'
+    tests=[('carboxylic_acid','[CX3](=O)[OX2H1]'),
+           ('amide','[CX3](=O)[NX3]'),('ester','[CX3](=O)[OX2][#6]'),
+           ('alcohol','[CX4][OX2H1]'),('phenol','[c][OX2H1]'),
+           ('ether','[#6;!$(C=O)][OX2][#6;!$(C=O)]'),
+           ('carbonyl','[CX3;!$(C(=O)[O,N])]=O'),
+           ('amine','[NX3;!$(N-C=O)]'),('aromatic_N','[n]'),('nitrile','[C]#[N]')]
+    tags=[name for name,smarts in tests if m.HasSubstructMatch(Chem.MolFromSmarts(smarts))]
+    if len(tags)>1: return 'multifunctional'
+    if tags: return tags[0]
+    if set(atoms)<={6}: return 'aromatic_hydrocarbon' if any(a.GetIsAromatic() for a in m.GetAtoms()) else 'aliphatic_hydrocarbon'
+    if any(z in (9,17,35) for z in atoms): return 'halogenated_other'
+    if 16 in atoms: return 'sulfur_other'
+    return 'other'
+
+def summarize(df, total=None, bootstrap=True):
+    if df.empty: return {'n_rows':0,'n_systems':0}
+    er=df.ref.to_numpy(float)-df.ln_gamma_inf.to_numpy(float)
+    ec=df.candidate.to_numpy(float)-df.ln_gamma_inf.to_numpy(float)
+    dae=abs(ec)-abs(er); s=system_ids(df)
+    n=len(df); total=n if total is None else total
+    out=dict(n_rows=n,n_systems=int(len(np.unique(s))),
+        mae_ref=float(abs(er).mean()),mae_candidate=float(abs(ec).mean()),
+        bias_ref=float(er.mean()),bias_candidate=float(ec.mean()),
+        delta_mae=float(dae.mean()),delta_prediction_mean=float((ec-er).mean()),
+        contribution_to_total_delta_mae=float(dae.sum()/total))
+    if bootstrap: out['delta_mae_CI95']=cluster_ci(dae,s)
+    return out
+
+def audit(a):
+    start=time.perf_counter(); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
+    r0=pd.read_csv(a.reference); c0=pd.read_csv(a.candidate)
+    r=keyed(r0); c=keyed(c0)
+    pos_identity=(len(r)==len(c) and np.array_equal(r.index,c.index))
+    r=select_split(r,a.split); c=select_split(c,a.split)
+    ids=r.index.intersection(c.index,sort=False)
+    aligned=r.loc[ids].copy(); aligned['ref']=r.loc[ids,PRED]; aligned['candidate']=c.loc[ids,PRED]
+    finite=np.isfinite(aligned[['ref','candidate','ln_gamma_inf']].to_numpy(float)).all(1)
+    common=aligned.loc[finite].copy()
+    if common.empty: raise ValueError('no finite common observations')
+    excluded=[]
+    for key in r.index.difference(c.index): excluded.append((key,'missing_in_candidate'))
+    for key in c.index.difference(r.index): excluded.append((key,'missing_in_reference'))
+    for key in aligned.index[~finite]: excluded.append((key,'nonfinite_prediction_or_response'))
+    pd.DataFrame(excluded,columns=['r3_row_id','reason']).to_csv(out/'excluded.csv',index=False)
+    smi=pd.read_csv(a.compounds,usecols=['inchikey','smiles'])
+    if smi.inchikey.duplicated().any(): raise ValueError('duplicate compound keys')
+    classes={k:chemical_class(s) for k,s in zip(smi.inchikey,smi.smiles)}
+    for role in ('solute','solvent'):
+        common[role+'_class']=common[role].map(classes)
+        if common[role+'_class'].isna().any(): raise ValueError(f'missing {role} class')
+    common['water_role']=np.where(common.solute==WATER,'water_solute',
+                         np.where(common.solvent==WATER,'water_solvent','no_water'))
+    common['flagged']=common.solute.isin(STALL_KEYS)|common.solvent.isin(STALL_KEYS)
+    common['delta_prediction']=common.candidate-common.ref
+    common['delta_absolute_error']=(common.candidate-common.ln_gamma_inf).abs()-(common.ref-common.ln_gamma_inf).abs()
+    common.to_csv(out/'paired_rows.csv',index=False)
+    for group in ['solute_class','solvent_class','water_role','solute','solvent']:
+        rows=[]
+        for label,g in common.groupby(group,sort=True):
+            row={group:label}; row.update(summarize(g,len(common),bootstrap=group.endswith('class') or group=='water_role')); rows.append(row)
+        pd.DataFrame(rows).to_csv(out/f'by_{group}.csv',index=False)
+    cross=[]
+    for (s,v),g in common.groupby(['solute_class','solvent_class'],sort=True):
+        x=dict(solute_class=s,solvent_class=v); x.update(summarize(g,len(common),False)); cross.append(x)
+    pd.DataFrame(cross).to_csv(out/'class_by_role.csv',index=False)
+    # Model masks are evaluated on the SAME reference observations, with identity joins.
+    mask_rows=[]
+    def masked(label,keep):
+        if not keep.any(): mask_rows.append(dict(mask=label,n_rows=0)); return
+        d=r.loc[keep]; e=d[PRED].to_numpy(float)-d.ln_gamma_inf.to_numpy(float)
+        mask_rows.append(dict(mask=label,n_rows=len(d),n_systems=len(np.unique(system_ids(d))),
+            reference_mae=float(abs(e).mean()),reference_bias=float(e.mean())))
+    rf=np.isfinite(r[[PRED,'ln_gamma_inf']].to_numpy(float)).all(1)
+    masked('reference_alone_finite',rf)
+    jointly=rf.copy()
+    for spec in a.mask:
+        label,path=spec.split('=',1); f=select_split(keyed(pd.read_csv(path)),a.split)
+        v=f[PRED].reindex(r.index).to_numpy(float)
+        valid=rf & np.isfinite(v)
+        masked('reference_and_'+label,valid); jointly &= np.isfinite(v)
+    if a.mask: masked('reference_and_all_supplied_masks',jointly)
+    in_common=r.index.isin(common.index)
+    masked('reference_and_candidate_finite',rf&in_common)
+    mask_no_stall=rf&in_common&~(r.solute.isin(STALL_KEYS)|r.solvent.isin(STALL_KEYS)).to_numpy()
+    masked('common_without_flagged_chains',mask_no_stall)
+    pd.DataFrame(mask_rows).to_csv(out/'denominators.csv',index=False)
+    result=dict(reference_sha256=digest(a.reference),candidate_sha256=digest(a.candidate),
+        mask_inputs=[dict(label=q.split('=',1)[0],path=str(Path(q.split('=',1)[1]).resolve()),sha256=digest(q.split('=',1)[1])) for q in a.mask],
+        same_row_identity_and_order=bool(pos_identity),split=a.split,
+        reference_split_rows=len(r),candidate_split_rows=len(c),identity_intersection=len(ids),
+        rows_excluded=len(excluded),infinite_ref=int(np.isinf(r[PRED]).sum()),infinite_candidate=int(np.isinf(c[PRED]).sum()),
+        common=summarize(common),without_flagged=summarize(common.loc[~common.flagged]),
+        flagged=summarize(common.loc[common.flagged]),
+        common_row_ids_sha256=__import__('hashlib').sha256('\n'.join(common.index).encode()).hexdigest(),
+        wall_s=time.perf_counter()-start)
+    write_json(out/'audit.json',result)
+    if a.expect_points is not None and len(common)!=a.expect_points: raise AssertionError('common row count does not reproduce the cited scorecard')
+    print(json.dumps(result,indent=2))
+
+def inventory(a):
+    rows=[]
+    for p in sorted(Path(a.root).rglob('*__idac__*.csv')):
+        d=pd.read_csv(p)
+        if PRED not in d: continue
+        rows.append(dict(path=str(p.resolve()),sha256=digest(p),rows=len(d),
+            test_rows=int((d['split']!='train').sum()) if 'split' in d else None))
+    cards=[]
+    for p in sorted(Path(a.root).rglob('*scorecard*.json')):
+        try:
+            c=json.loads(p.read_text()); table=c.get('tables',{}).get('idac',{})
+            if 'Z0x' in table: cards.append(dict(path=str(p.resolve()),sha256=digest(p),models=c.get('models'),split=c.get('split'),n_points=table.get('n_points'),Z0x=table['Z0x']))
+        except (ValueError,TypeError): continue
+    print(json.dumps(dict(predictions=rows,Z0x_scorecards=cards),indent=2))
+
+def compare_fresh(a):
+    r=keyed(pd.read_csv(a.reference)); c=keyed(pd.read_csv(a.candidate))
+    if set(r.index)!=set(c.index): raise ValueError('fresh/stored identity coverage changed; audit inputs before a numerical comparison')
+    x=r[PRED].to_numpy(float); y=c.loc[r.index,PRED].to_numpy(float)
+    mask=np.isfinite(x)
+    if not np.array_equal(mask,np.isfinite(y)): raise ValueError('fresh/stored finite coverage changed')
+    if not mask.any(): raise ValueError('no finite comparisons')
+    err=float(abs(x[mask]-y[mask]).max())
+    result=dict(rows=len(x),finite=int(mask.sum()),max_delta_lngamma=err,
+                reference_sha256=digest(a.reference),candidate_sha256=digest(a.candidate))
+    write_json(a.out,result)
+    if err>=a.tol: raise AssertionError(f'fresh/stored mismatch {err} >= {a.tol}')
+
+def main():
+    p=argparse.ArgumentParser(); s=p.add_subparsers(dest='cmd',required=True)
+    q=s.add_parser('inventory'); q.add_argument('--root',default='results')
+    q=s.add_parser('audit'); q.add_argument('--reference',required=True); q.add_argument('--candidate',required=True)
+    q.add_argument('--compounds',default='data/benchmark/compounds.csv'); q.add_argument('--split',default='test',choices=['test','train','test_one','test_both','all'])
+    q.add_argument('--mask',action='append',default=[],help='LABEL=prediction.csv; reproduce the historical model list')
+    q.add_argument('--expect-points',type=int); q.add_argument('--out',required=True)
+    q=s.add_parser('compare-fresh'); q.add_argument('--reference',required=True); q.add_argument('--candidate',required=True)
+    q.add_argument('--out',required=True); q.add_argument('--tol',type=float,default=1e-3)
+    a=p.parse_args(); globals()[a.cmd.replace('-','_')](a)
+if __name__=='__main__': main()
--- /dev/null
+++ b/scripts/r3_hybrid.py
@@ -0,0 +1,86 @@
+"""Diagnostic four-corner substitution: UD/open solute x UD/open solvent.
+
+One fresh worker per ordered pair and corner. No altered profile, fitted parameter,
+or production output. Prediction and absolute-error Shapley attributions both sum exactly.
+"""
+from __future__ import annotations
+import argparse
+import json
+import os
+from pathlib import Path
+import subprocess
+import sys
+import tempfile
+import numpy as np
+import pandas as pd
+from r3_common import keyed, digest, write_json
+
+def worker(a):
+    os.environ.pop('ZC_SIGMA_OVERRIDE_DIR',None)
+    from zcosmo.cosmosac import sigma_path
+    rows=pd.read_csv(a.rows); pairs=rows[['solute','solvent']].drop_duplicates()
+    if len(pairs)!=1: raise ValueError('worker must have exactly one ordered pair')
+    solute,solvent=pairs.iloc[0].tolist()
+    if solute==solvent: raise ValueError('a self-pair does not define two independent profile substitutions')
+    used={}
+    with tempfile.TemporaryDirectory(prefix='r3-hybrid-') as td:
+        for key,kind in zip((solute,solvent),a.corner):
+            p=Path(a.open_profiles)/f'{key}.sigma' if kind=='o' else sigma_path(key)
+            if p is None or not Path(p).is_file(): raise FileNotFoundError(str(p))
+            p=Path(p).resolve(); (Path(td)/f'{key}.sigma').symlink_to(p)
+            used[key]=dict(source=kind,path=str(p),sha256=digest(p))
+        os.environ['ZC_SIGMA_OVERRIDE_DIR']=td
+        from zcosmo.models import make_model
+        compounds=pd.read_csv(a.compounds); smi=dict(zip(compounds.inchikey,compounds.smiles))
+        m=make_model(a.model,[solute,solvent],[smi[solute],smi[solvent]])
+        records=[]
+        for r in rows.itertuples():
+            try: value=float(m.lngamma_inf(r.T,0)); error=''
+            except Exception as ex: value=np.nan; error=type(ex).__name__+': '+str(ex)[:200]
+            records.append(dict(r3_row_id=r.r3_row_id,value=value,error=error))
+        pd.DataFrame(records).to_csv(a.out,index=False); write_json(str(a.out)+'.inputs.json',used)
+
+def run(a):
+    d=pd.read_csv(a.paired_rows)
+    if 'r3_row_id' not in d or d.r3_row_id.duplicated().any(): raise ValueError('use audit/paired_rows.csv with unique row IDs')
+    out=Path(a.out); out.mkdir(parents=True,exist_ok=True); joined=[]
+    for j,(_,g) in enumerate(d.groupby(['solute','solvent'],sort=True)):
+        part=out/f'pair-{j:04d}'; part.mkdir(exist_ok=True)
+        rows=part/'rows.csv'; g.to_csv(rows,index=False); frame=g.set_index('r3_row_id').copy()
+        for corner in ('uu','ou','uo','oo'):
+            target=part/f'{corner}.csv'
+            subprocess.run([sys.executable,str(Path(__file__).resolve()),'worker','--rows',str(rows),
+                '--open-profiles',a.open_profiles,'--corner',corner,'--model',a.model,
+                '--compounds',a.compounds,'--out',str(target)],check=True)
+            value=pd.read_csv(target).set_index('r3_row_id')
+            frame[corner]=value.loc[frame.index,'value']
+        joined.append(frame)
+    d=pd.concat(joined); valid=np.isfinite(d[['uu','ou','uo','oo']].to_numpy()).all(1)
+    d['all_corners_finite']=valid
+    for tag,transform in [('prediction',lambda x:x),('absolute_error',lambda x:(x-d.ln_gamma_inf).abs())]:
+        uu,ou,uo,oo=[transform(d[k]) for k in ('uu','ou','uo','oo')]
+        d[tag+'_solute']=.5*((ou-uu)+(oo-uo))
+        d[tag+'_solvent']=.5*((uo-uu)+(oo-ou))
+        residual=d[tag+'_solute']+d[tag+'_solvent']-(oo-uu)
+        if valid.any() and abs(residual[valid]).max()>1e-10: raise AssertionError('attribution identity failed')
+    d.reset_index().to_csv(out/'hybrid_rows.csv',index=False)
+    report=dict(model=a.model,rows=len(d),all_corners_finite=int(valid.sum()),
+        unavailable_rows=d.index[~valid].tolist(),paired_rows_sha256=digest(a.paired_rows))
+    if valid.any():
+        report['mean_solute_delta_MAE']=float(d.loc[valid,'absolute_error_solute'].mean())
+        report['mean_solvent_delta_MAE']=float(d.loc[valid,'absolute_error_solvent'].mean())
+        report['mean_total_delta_MAE']=float(((d.loc[valid,'oo']-d.loc[valid,'ln_gamma_inf']).abs()-(d.loc[valid,'uu']-d.loc[valid,'ln_gamma_inf']).abs()).mean())
+        report['fresh_UD_vs_stored_ref_max']=float(abs(d.loc[valid,'uu']-d.loc[valid,'ref']).max())
+        report['fresh_open_vs_stored_candidate_max']=float(abs(d.loc[valid,'oo']-d.loc[valid,'candidate']).max())
+    write_json(out/'hybrid.json',report)
+    if not valid.all(): raise SystemExit('nonfinite corner(s): partial attribution recorded, not a decomposition of the full cited score')
+
+def main():
+    p=argparse.ArgumentParser(); s=p.add_subparsers(dest='cmd',required=True)
+    for name in ('run','worker'):
+        q=s.add_parser(name); q.add_argument('--open-profiles',required=True); q.add_argument('--out',required=True)
+        q.add_argument('--model',choices=['Z0x','cosmosac_dsp'],default='Z0x'); q.add_argument('--compounds',default='data/benchmark/compounds.csv')
+        if name=='run': q.add_argument('--paired-rows',required=True)
+        else: q.add_argument('--rows',required=True); q.add_argument('--corner',choices=['uu','ou','uo','oo'],required=True)
+    a=p.parse_args(); globals()[a.cmd](a)
+if __name__=='__main__': main()
```

### P17

<!-- PATCH:P17 -->
```diff
--- /dev/null
+++ b/scripts/r3_orientation.py
@@ -0,0 +1,241 @@
+"""Frozen-geometry orientation experiment. Native items need PySCF; scoring needs local UD assets.
+
+All generated profiles stay in a separate experiment directory. A rotated/reoriented,
+rotation-averaged, or finer-surface profile is NOT an accepted production profile.
+"""
+from __future__ import annotations
+import argparse
+from collections import Counter
+import json
+import os
+from pathlib import Path
+import shutil
+import subprocess
+import sys
+import tempfile
+import time
+import numpy as np
+import pandas as pd
+from r3_common import (BASE, digest, write_json, rotations, canonical_xyz,
+                       read_sigma, write_sigma, profile_descriptors)
+
+PHYSICS=['src/zcosmo/pyscf_cosmo.py','src/zcosmo/pcm_lu.py',
+         'data/raw/nist/to_sigma.py','src/zcosmo/cosmosac.py','src/zcosmo/z0x.py',
+         'src/zcosmo/models.py','results/z_params/Z0.json',
+         'results/qc/dielectric.csv','results/qc/dispersion.csv']
+
+def manifest(work): return json.loads((Path(work)/'manifest.json').read_text())
+
+def freeze(a):
+    work=Path(a.work).resolve()
+    if work.exists() and any(work.iterdir()): raise ValueError('freeze into a new directory')
+    work.mkdir(parents=True,exist_ok=True)
+    old=pd.read_csv('results/pyscf_profile_validation.csv',usecols=['key','T'])
+    if len(old)!=2302 or old.key.nunique()!=25: raise ValueError('historical fixture changed')
+    val=pd.read_csv('data/pyscf_sigma/validation_set.csv')
+    val=val[val.inchikey.isin(old.key.unique())]
+    if len(val)!=25 or val.inchikey.duplicated().any(): raise ValueError('validation keys changed')
+    d=pd.read_csv('data/benchmark/idac.csv',usecols=['file','dataset','solute','solvent','T','method','has_sigma'])
+    if d.has_sigma.dtype!=bool: raise ValueError('has_sigma is not Boolean')
+    d=d[d.has_sigma]; records=[]; geoms={}
+    for k,smi in zip(val.inchikey,val.smiles):
+        p=Path(a.geometry_dir)/f'{k}.xyz.json'
+        g=json.loads(p.read_text()); x=np.asarray(g['x'],float)
+        if x.shape!=(len(g['sym']),3) or not np.isfinite(x).all(): raise ValueError(f'bad geometry {p}')
+        q=work/'geometries'/p.name; q.parent.mkdir(exist_ok=True); shutil.copy2(p,q)
+        geoms[k]=dict(file=str(q.relative_to(work)),sha256=digest(q),smiles=smi,
+                      note='Frozen stored coordinates. run_one rounds xyz.json to 5 decimals; identity is recomputed.')
+        for i,r in d[(d.solute==k)|(d.solvent==k)].iterrows():
+            records.append(dict(query=f'{k}:{i}',key=k,solute=r.solute,solvent=r.solvent,T=float(r['T']),
+                                role='solute' if r.solute==k else 'solvent',benchmark_row=int(i)))
+    rows=pd.DataFrame(records)
+    if len(rows)!=2302 or Counter(zip(rows.key,rows['T']))!=Counter(zip(old.key,old['T'])):
+        raise ValueError('historical 25/2302 occurrence manifest mismatch')
+    rows.to_csv(work/'queries.csv',index=False)
+    package_versions={}
+    from importlib.metadata import version, PackageNotFoundError
+    for name in ['numpy','scipy','pandas','pyscf','pyberny','rdkit']:
+        try: package_versions[name]=version(name)
+        except PackageNotFoundError: package_versions[name]='not installed on manifest host'
+    files=sorted(set(PHYSICS) | {str(p) for p in Path('src/zcosmo').rglob('*.py')}
+                 | {str(p) for p in Path('scripts').glob('r3_*.py')})
+    hashes={p:digest(p) for p in files}
+    write_json(work/'manifest.json',dict(reference=BASE,geometries=geoms,physics_sha256=hashes,
+        queries_sha256=digest(work/'queries.csv'),rotations={k:v.tolist() for k,v in rotations().items()},
+        packages_on_manifest_host=package_versions,registration=a.registration,
+        cooh_flag=os.environ.get('ZC_R3_COOH_FLAG','0')))
+    (work/'keys.txt').write_text('\n'.join(geoms)+'\n')
+    print(f'Frozen {len(geoms)} geometries / {len(rows)} query occurrences at {work}')
+
+def check_inputs(work):
+    m=manifest(work)
+    if os.environ.get('ZC_R3_COOH_FLAG','0')!=m['cooh_flag']: raise ValueError('COOH protocol changed; freeze a new experiment')
+    if digest(Path(work)/'queries.csv')!=m['queries_sha256']: raise ValueError('query manifest changed')
+    for p,h in m['physics_sha256'].items():
+        if digest(p)!=h: raise ValueError(f'physics/input file changed: {p}; freeze a separate arm')
+    return m
+
+def item(a):
+    m=check_inputs(a.work)
+    import pyscf
+    if pyscf.__version__!='2.14.0': raise RuntimeError('native gate requires pyscf==2.14.0')
+    from zcosmo.pyscf_cosmo import cosmo_segments, to_profiles, write_sigma as native_write, BOHR, cavity_volume
+    from zcosmo.pyscf_cosmo_v2 import OPEN_SHELL
+    from rdkit import Chem
+    gref=m['geometries'][a.key]; path=Path(a.work)/gref['file']
+    if digest(path)!=gref['sha256']: raise ValueError('geometry changed')
+    g=json.loads(path.read_text()); sym=g['sym']; x=np.asarray(g['x'],float)
+    R=np.asarray(m['rotations'][a.rotation]); centroid=x.mean(0)
+    x=(x-centroid)@R.T+centroid
+    if a.method=='canonical':
+        table=Chem.GetPeriodicTable(); masses=[table.GetAtomicWeight(s) for s in sym]
+        x=canonical_xyz(x,masses)
+    target=Path(a.work)/a.method/a.rotation; target.mkdir(parents=True,exist_ok=True)
+    dest=target/f'{a.key}.sigma'
+    if dest.exists(): raise FileExistsError(f'{dest}; use a fresh arm, do not silently reuse an output')
+    order=41 if a.method=='lebedev41' else 29
+    t=time.perf_counter(); seg,e=cosmo_segments(sym,x,lebedev=order,spin=OPEN_SHELL.get(gref['smiles'],0))
+    out,meta=to_profiles(sym,x,seg)
+    meta.update(source='R3 experiment, not adopted',geometry_converged='R3-frozen-geometry',
+        r3_method=a.method,r3_rotation=a.rotation,registration=m['registration'],
+        input_geometry_sha256=gref['sha256'],E_scf_Eh=float(e),lebedev_order=order)
+    native_write(dest,out,meta,a.key)
+    np.savez_compressed(target/f'{a.key}.segments.npz',x=x,sym=np.asarray(sym),**seg)
+    # Co-rotating existing segments tests the parser, NOT new electronic/surface quadrature.
+    Q=rotations()['r3']; segq=dict(seg); segq['xyz']=seg['xyz']@Q.T
+    oq,mq=to_profiles(sym,x@Q.T,segq)
+    p=np.stack([out.psigmaA_nhb,out.psigmaA_OH,out.psigmaA_OT])
+    pq=np.stack([oq.psigmaA_nhb,oq.psigmaA_OH,oq.psigmaA_OT])
+    parser_error=float(abs(p-pq).max())
+    normals=seg['xyz']*BOHR-x[np.asarray(seg['atom'],int)]
+    normals/=np.linalg.norm(normals,axis=1)[:,None]
+    flux=(normals*seg['area'][:,None]).sum(0)
+    # A finite surface can violate area-normal closure and make the volume origin-dependent.
+    shift=np.array([1.,2.,3.]); shifted=dict(seg); shifted['xyz']=seg['xyz']+shift/BOHR
+    v0=cavity_volume(seg,x/BOHR); vt=cavity_volume(shifted,(x+shift)/BOHR)
+    report=dict(key=a.key,method=a.method,rotation=a.rotation,segments=len(seg['q']),
+        sum_q_e=float(np.sum(seg['q'])),parser_corotation_max_dpsigmaA=parser_error,
+        parser_corotation_dvolume_A3=float(abs(meta['volume [A^3]']-mq['volume [A^3]'])),
+        surface_normal_closure_A2=flux.tolist(),translation_volume_observed_A3=float(vt-v0),
+        translation_volume_predicted_A3=float(shift@flux/3),
+        profile_sha256=digest(dest),wall_s=time.perf_counter()-t,descriptors=profile_descriptors(dest))
+    write_json(target/f'{a.key}.diagnostic.json',report)
+    if parser_error>=1e-7: raise AssertionError('co-rotated parser control failed; investigate before attributing variation to SCF')
+    if abs((vt-v0)-shift@flux/3)>1e-8: raise AssertionError('translation-volume identity failed')
+    print(json.dumps(report))
+
+def average(a):
+    m=check_inputs(a.work); n=16 if a.method=='mean16' else 8; offset=8 if a.method=='mean8b' else 0
+    target=Path(a.work)/a.method/'id'; target.mkdir(parents=True,exist_ok=True)
+    keys=[a.key] if a.key else list(m['geometries'])
+    for k in keys:
+        files=[Path(a.work)/'raw'/f'r{i}'/f'{k}.sigma' for i in range(offset,offset+n)]
+        loaded=[read_sigma(p) for p in files]
+        flags=[v[2].get('disp. flag') for v in loaded]
+        if len(set(flags))!=1: raise ValueError('orientation changed the discrete dispersion flag')
+        sigma=loaded[0][0]; p=np.mean([v[1] for v in loaded],axis=0); meta=dict(loaded[0][2])
+        meta.update({'area [A^2]':float(p.sum()),'volume [A^3]':float(np.mean([v[2]['volume [A^3]'] for v in loaded])),
+                     'r3_method':a.method,'r3_rotation':'id','source':'R3 equal-weight profile-quadrature average, not a conformer ensemble',
+                     'members_sha256':[digest(f) for f in files], 'E_scf_Eh':float(np.mean([v[2]['E_scf_Eh'] for v in loaded]))})
+        dest=target/f'{k}.sigma'
+        if dest.exists(): raise FileExistsError(dest)
+        write_sigma(dest,sigma,p,meta)
+
+def worker(a):
+    # A new process for EACH target/profile set, including UD. Never switch loader environments in process.
+    work=Path(a.work); m=check_inputs(work)
+    rows=pd.read_csv(work/'queries.csv'); rows=rows[rows.key==a.key]
+    os.environ.pop('ZC_SIGMA_OVERRIDE_DIR',None)
+    from zcosmo.cosmosac import SIGMA_DIR
+    if not SIGMA_DIR.is_dir(): raise FileNotFoundError('UD profiles absent: run score on the asset-bearing Mac, not a bare Actions runner')
+    with tempfile.TemporaryDirectory(prefix='r3-profile-set-') as td:
+        if a.background and a.profile_set=='UD':
+            raise ValueError('UD baseline requires the UD background; open-background reference must be an explicit identity profile set')
+        if a.background:
+            bg=Path(a.background).resolve()
+            for k in set(rows.solute)|set(rows.solvent):
+                f=bg/f'{k}.sigma'
+                if not f.is_file(): raise FileNotFoundError(f'missing exact open-background profile {f}')
+                (Path(td)/f.name).symlink_to(f)
+        if a.profile_set!='UD':
+            f=Path(a.profile_set).resolve()/f'{a.key}.sigma'
+            if not f.is_file(): raise FileNotFoundError(f)
+            target=Path(td)/f.name
+            if target.is_symlink() or target.exists(): target.unlink()
+            target.symlink_to(f)
+        os.environ['ZC_SIGMA_OVERRIDE_DIR']=td
+        from zcosmo.models import make_model
+        from zcosmo.cosmosac import sigma_path
+        compounds=pd.read_csv('data/benchmark/compounds.csv'); smi=dict(zip(compounds.inchikey,compounds.smiles))
+        used={}
+        for k in set(rows.solute)|set(rows.solvent):
+            p=sigma_path(k)
+            if p is None: raise FileNotFoundError(k)
+            used[k]=dict(path=str(p.resolve()),sha256=digest(p))
+        cache={}; records=[]
+        for r in rows.itertuples():
+            result=dict(query=r.query,key=r.key,solute=r.solute,solvent=r.solvent,T=r.T,role=r.role)
+            for name in ('cosmosac_dsp','Z0x'):
+                mk=(name,r.solute,r.solvent)
+                try:
+                    if mk not in cache: cache[mk]=make_model(name,[r.solute,r.solvent],[smi[r.solute],smi[r.solvent]])
+                    result[name]=float(cache[mk].lngamma_inf(r.T,0)); result[name+'_error']=''
+                except Exception as ex:
+                    result[name]=np.nan; result[name+'_error']=type(ex).__name__+': '+str(ex)[:200]
+            records.append(result)
+        pd.DataFrame(records).to_csv(a.out,index=False)
+        write_json(str(a.out)+'.inputs.json',used)
+
+def score(a):
+    work=Path(a.work); m=check_inputs(work); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
+    chunks=[]; t=time.perf_counter()
+    for k in m['geometries']:
+        p=out/f'{k}.csv'
+        cmd=[sys.executable,str(Path(__file__).resolve()),'worker','--work',str(work),'--key',k,
+             '--profile-set',a.profile_set,'--out',str(p)]
+        if a.background: cmd += ['--background',a.background]
+        subprocess.run(cmd,check=True); chunks.append(pd.read_csv(p))
+    d=pd.concat(chunks,ignore_index=True)
+    if len(d)!=2302 or d['query'].duplicated().any(): raise ValueError('missing/duplicate query occurrences')
+    d.to_csv(out/'values.csv',index=False)
+    write_json(out/'timing.json',dict(wall_s=time.perf_counter()-t,rows=len(d),profile_set=a.profile_set,background=a.background))
+
+def compare(a):
+    base=pd.read_csv(a.reference).set_index('query'); changes=[]; failed=False
+    summaries=[]
+    for spec in a.candidate:
+        label,path=spec.split('=',1); d=pd.read_csv(path).set_index('query')
+        if set(d.index)!=set(base.index): raise ValueError('query identity mismatch')
+        d=d.loc[base.index]
+        for model in ('cosmosac_dsp','Z0x'):
+            x=base[model].to_numpy(float); y=d[model].to_numpy(float)
+            mask=np.isfinite(x); same=np.array_equal(mask,np.isfinite(y))
+            if not same or not mask.any(): failed=True
+            valid=mask&np.isfinite(y); delta=y[valid]-x[valid]
+            summaries.append(dict(label=label,model=model,rows=len(x),finite_reference=int(mask.sum()),
+                same_finite_mask=bool(same),max_abs=float(abs(delta).max()) if len(delta) else None,
+                median_abs=float(np.median(abs(delta))) if len(delta) else None,
+                mean_abs=float(abs(delta).mean()) if len(delta) else None))
+            for role in ('solute','solvent'):
+                sub=valid&(base.role.to_numpy()==role)
+                if sub.any(): summaries.append(dict(label=label,model=model,role=role,rows=int(sub.sum()),max_abs=float(abs(y[sub]-x[sub]).max()),mean_abs=float(abs(y[sub]-x[sub]).mean())))
+            q=base.loc[valid,['key','solute','solvent','T','role']].copy(); q['query']=q.index
+            q['label']=label; q['model']=model; q['delta']=delta; changes.append(q)
+    out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
+    pd.concat(changes).to_csv(out/'row_deltas.csv',index=False)
+    write_json(out/'comparison.json',dict(summaries=summaries,coverage_pass=not failed))
+    print(json.dumps(summaries,indent=2))
+    if failed: raise SystemExit('coverage mismatch or empty finite comparison; not accepted')
+
+def main():
+    p=argparse.ArgumentParser(); s=p.add_subparsers(dest='cmd',required=True)
+    q=s.add_parser('freeze'); q.add_argument('--work',required=True); q.add_argument('--geometry-dir',required=True); q.add_argument('--registration',required=True)
+    q=s.add_parser('item'); q.add_argument('--work',required=True); q.add_argument('--key',required=True)
+    q.add_argument('--method',choices=['raw','canonical','lebedev41'],default='raw'); q.add_argument('--rotation',choices=list(rotations()),default='id')
+    q=s.add_parser('average'); q.add_argument('--work',required=True); q.add_argument('--method',choices=['mean8','mean8b','mean16'],required=True); q.add_argument('--key')
+    for name in ('score','worker'):
+        q=s.add_parser(name); q.add_argument('--work',required=True); q.add_argument('--profile-set',required=True); q.add_argument('--out',required=True); q.add_argument('--background')
+        if name=='worker': q.add_argument('--key',required=True)
+    q=s.add_parser('compare'); q.add_argument('--reference',required=True); q.add_argument('--candidate',action='append',required=True); q.add_argument('--out',required=True)
+    a=p.parse_args(); globals()[a.cmd](a)
+if __name__=='__main__': main()
```

### P18

<!-- PATCH:P18 -->
```diff
--- a/src/zcosmo/pyscf_cosmo.py
+++ b/src/zcosmo/pyscf_cosmo.py
@@ -120,6 +120,9 @@
     out = p.get_outputs()
     meta = p.get_meta()
     meta["disp. flag"] = "H2O" if p.is_water else p.disp.dispersion_flag
+    # R3 A correction: opt-in until the metadata-only gate is registered and accepted.
+    if os.environ.get("ZC_R3_COOH_FLAG", "0") == "1" and p.disp.has_COOH and not p.is_water:
+        meta["disp. flag"] = "COOH"
     meta["disp. e/kB [K]"] = None if p.disp.dispersive_molecule is None or np.isnan(p.disp.dispersive_molecule) \
         else float(p.disp.dispersive_molecule)
     return out, meta
--- a/src/zcosmo/pyscf_cosmo_v2.py
+++ b/src/zcosmo/pyscf_cosmo_v2.py
@@ -13,7 +13,8 @@
     packages = [(name, version(name)) for name in ("pyscf", "pyberny", "rdkit", "tblite", "ase", "numpy", "scipy")]
     return hashlib.sha256(code + json.dumps(packages).encode()
                           + os.environ.get("ZC_TRIC_PREOPT", "0").encode()
-                          + os.environ.get("ZC_BERNY_NOISE_EH", "").encode()).hexdigest()
+                          + os.environ.get("ZC_BERNY_NOISE_EH", "").encode()
+                          + os.environ.get("ZC_R3_COOH_FLAG", "0").encode()).hexdigest()
 
 
 def dft_geometry(sym, xyz_A, basis="def2-svp", maxsteps=100, partial=None, spin=0):
--- /dev/null
+++ b/scripts/r3_metadata.py
@@ -0,0 +1,47 @@
+"""A-class COOH metadata repair using the existing NIST geometry-based classifier.
+
+No SCF. The raw sigma rows are copied byte-for-byte. No input file is modified.
+Register before generating candidate profiles; changing this flag changes COSMO-SAC-dsp.
+"""
+from __future__ import annotations
+import argparse
+import json
+from pathlib import Path
+import sys
+import numpy as np
+import pandas as pd
+from scipy.spatial.distance import cdist
+from r3_common import digest,write_json,read_sigma
+
+def run(a):
+    sys.path.insert(0,str(Path('data/raw/nist').resolve()))
+    import to_sigma as ts
+    out=Path(a.out);out.mkdir(parents=True,exist_ok=True); report=[]
+    keys=Path(a.keys).read_text().split()
+    if len(keys)!=len(set(keys)) or not keys: raise ValueError('invalid key manifest')
+    for k in keys:
+        src=Path(a.profile_dir)/f'{k}.sigma'; xyz=Path(a.geometry_dir)/f'{k}.xyz.json'
+        g=json.loads(xyz.read_text()); sym=g['sym']; x=np.asarray(g['x'],float)
+        if x.shape!=(len(sym),3) or not np.isfinite(x).all(): raise ValueError('invalid geometry')
+        p=ts.Dmol3COSMOParser.__new__(ts.Dmol3COSMOParser)
+        p.df_atom=pd.DataFrame(dict(atom=sym));p.dist_mat_atom=cdist(x,x)
+        p.is_water=sym.count('H')==2 and sym.count('O')==1 and len(sym)==3
+        disp=p.get_dispersive_values()
+        flag='H2O' if p.is_water else ('COOH' if disp.has_COOH else disp.dispersion_flag)
+        _,_,meta=read_sigma(src);old=meta.get('disp. flag')
+        meta.update({'disp. flag':flag,'r3_protocol':'COOH metadata correction, not adopted',
+                     'r3_registration':a.registration,'r3_parent_sha256':digest(src)})
+        lines=src.read_text().splitlines(keepends=True);target=out/src.name
+        if target.exists(): raise FileExistsError(target)
+        target.write_text('# meta: '+json.dumps(meta,allow_nan=False)+'\n'+''.join(lines[1:]))
+        if not np.array_equal(np.loadtxt(src),np.loadtxt(target)): raise AssertionError('sigma rows changed')
+        report.append(dict(key=k,old_flag=old,new_flag=flag,has_COOH=bool(disp.has_COOH),
+                           geometry_sha256=digest(xyz),source_sha256=digest(src),candidate_sha256=digest(target)))
+    write_json(out/'metadata_audit.json',dict(registration=a.registration,
+        parser_sha256=digest('data/raw/nist/to_sigma.py'),profiles=report))
+
+def main():
+    p=argparse.ArgumentParser()
+    for name in ('profile-dir','geometry-dir','keys','out','registration'):p.add_argument('--'+name,required=True)
+    run(p.parse_args())
+if __name__=='__main__':main()
```

### P19

<!-- PATCH:P19 -->
```diff
--- /dev/null
+++ b/scripts/r3_precision.py
@@ -0,0 +1,85 @@
+"""One prospective A trial: 80 tighter-SCF Berny evaluations, then <=20 original evaluations.
+
+The control has the identical 80+20 structure with original SCF tolerances throughout.
+Both stages start fresh optimizer histories. No .bstate file is read. All output is experimental.
+"""
+from __future__ import annotations
+import argparse
+from importlib.metadata import version
+import json
+from pathlib import Path
+import time
+import numpy as np
+from r3_common import digest, write_json
+
+def factory(sym, xyz, spin, tight, memory):
+    from pyscf import gto, dft
+    from pyscf.data import elements
+    from zcosmo.pyscf_cosmo import BOHR, RADII
+    from zcosmo.pcm_lu import cache_pcm3c
+    mol=gto.M(atom=list(zip(sym,xyz.tolist())),unit='Angstrom',basis='def2-svp',
+              spin=spin,verbose=0,max_memory=memory)
+    mf=(dft.UKS(mol) if spin else dft.RKS(mol)).density_fit().PCM()
+    mf=cache_pcm3c(mf); mf.xc='b88,p86'; mf.grids.level=2
+    mf.conv_tol=1e-11 if tight else 1e-8
+    mf.conv_tol_grad=1e-7 if tight else None
+    s=mf.with_solvent; s.method='C-PCM'; s.eps=1e9; s.lebedev_order=17
+    table=np.zeros(120)
+    for element,r in RADII.items(): table[elements.charge(element)]=r/BOHR
+    s.radii_table=table
+    return mf
+
+def run(a):
+    if version('pyscf')!='2.14.0' or version('pyberny')!='0.7.0':
+        raise RuntimeError('requires pyscf 2.14.0 and pyberny 0.7.0')
+    from pyscf.geomopt.berny_solver import kernel
+    from zcosmo.pyscf_cosmo import cosmo_segments, to_profiles, write_sigma
+    out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
+    if any(out.iterdir()): raise FileExistsError('use a fresh arm directory')
+    g=json.loads(Path(a.input).read_text()); sym=g['sym']; x=np.asarray(g['x'],float)
+    if x.shape!=(len(sym),3) or not np.isfinite(x).all(): raise ValueError('bad input geometry')
+    records=[]; t=time.perf_counter(); stages=[]
+    for name,cap,tight in [('pre',80,a.arm=='tight'),('confirm',20,False)]:
+        mf=factory(sym,x,a.spin,tight,a.memory)
+        stage_records=[]
+        def callback(env):
+            scanner=env['g_scanner']; gradient=np.asarray(env['gradients'],float)
+            if not scanner.converged or not np.isfinite(gradient).all():
+                raise RuntimeError('unconverged SCF or nonfinite gradient is not an optimizer step')
+            state=env['optimizer']._state
+            r=dict(stage=name,cycle=int(env['cycle']),energy_Eh=float(env['energy']),
+                gradient_max_Eh_Bohr=float(abs(gradient).max()),
+                scf_cycles=int(getattr(scanner.base,'cycles',-1)),
+                trust_pre_send=float(state.trust))
+            stage_records.append(r); records.append(r)
+            write_json(out/'trace.json',records)
+            write_json(out/'latest.json',dict(sym=sym,x=env['mol'].atom_coords(unit='Angstrom').tolist(),
+                stage=name,evaluations=len(records),registration=a.registration))
+        st=time.perf_counter()
+        converged,mol=kernel(mf,maxsteps=cap,callback=callback,assert_convergence=True)
+        x=mol.atom_coords(unit='Angstrom')
+        stages.append(dict(stage=name,budget=cap,evaluations=len(stage_records),converged=bool(converged),
+                           tight_scf=tight,wall_s=time.perf_counter()-st))
+    original_pass=bool(stages[-1]['converged'])
+    report=dict(arm=a.arm,key=a.key,registration=a.registration,input_sha256=digest(a.input),
+        pyscf=version('pyscf'),pyberny=version('pyberny'),stages=stages,
+        evaluations=len(records),original_berny_pass=original_pass,wall_s=time.perf_counter()-t)
+    write_json(out/'result.json',report)
+    if not original_pass:
+        print(json.dumps(report)); return 2  # Budget exhausted, not successful convergence.
+    seg,e=cosmo_segments(sym,np.asarray(x),spin=a.spin)
+    p,meta=to_profiles(sym,np.asarray(x),seg)
+    meta.update(geometry_converged=True,geometry_protocol='R3-A-tight-SCF-80-plus-original-20' if a.arm=='tight' else 'R3-control-original-80-plus-20',
+                source='R3 trial, not adopted',E_scf_Eh=float(e),registration=a.registration)
+    write_sigma(out/f'{a.key}.sigma',p,meta,a.key)
+    write_json(out/f'{a.key}.xyz.json',dict(sym=sym,x=x.tolist()))
+    report.update(profile_energy_Eh=float(e),profile_sha256=digest(out/f'{a.key}.sigma'),
+                  wall_s=time.perf_counter()-t)
+    write_json(out/'result.json',report); print(json.dumps(report)); return 0
+
+def main():
+    p=argparse.ArgumentParser(); p.add_argument('--input',required=True); p.add_argument('--key',required=True)
+    p.add_argument('--arm',choices=['control','tight'],required=True); p.add_argument('--out',required=True)
+    p.add_argument('--spin',type=int,default=0); p.add_argument('--memory',type=int,default=6000)
+    p.add_argument('--registration',required=True); raise SystemExit(run(p.parse_args()))
+if __name__=='__main__': main()
```

### REG

<!-- PATCH:REG -->
```diff
--- /dev/null
+++ b/docs/astra/round3/PROPOSED_REGISTRATION.md
@@ -0,0 +1,15 @@
+## R3 prospective profile reliability and final-precision experiments
+
+This entry is registered with the actual commit timestamp before any R3 native candidate output or score is read. It is motivated by the known R2/P15 rejection, S2 rotation results, and exploratory Z0x-open deficit; it is not a new held-out discovery. The historical P15, S1, S2, and Z0x-open decisions remain unchanged. Reference code is c515e38e1a7fd91a02e1ff1f1209a81b67a7d49d plus the explicitly archived R3 experimental helpers. All output directories are separate from profiles_v2 and all stored scorecards. No experimental response determines a parameter or selects a profile recipe.
+
+P16 audits existing predictions by immutable observation identity, finite coverage, model-list intersection, split, and class/role. The class mapping and four-corner UD/open solute/solvent attribution in scripts/r3_idac.py and r3_hybrid.py are frozen by this commit. These are descriptive post hoc diagnostics. No prediction or experimental value is rewritten. Historical scores are preserved with their original denominator and provenance; a discrepant score is corrected only in a separately identified report.
+
+P17 raw orientation experiment freezes the historical 25 keys and 2,302 query occurrences, plus the saved geometry bytes, source hashes, and fixed rotation matrices. Recompute an identity profile at those exact coordinates rather than treating a rounded XYZ file as identical to the original SCF geometry. For all 25, compute identity, a repeat identity, cube90, and r0 through r7 from scipy Rotation.random(16, random_state=20261004); its first eight equal S2's rotation set. On water, methanol, and decanoic acid additionally use rotations of 0.001, 0.01, 0.1, 0.5, and 1.0 radians about normalized (1,2,3). This is 290 TZVP single points. Every profile uses pinned pyscf 2.14.0, the unchanged BP86/def2-TZVP, grid level 3/default pruning, C-PCM epsilon 1e9, project radii, Lebedev 29 and conv_tol 1e-9. The source's q, Hsieh averaging, and split are unchanged. Co-rotation of already-computed segments is an E postprocessing control, not a new electronic calculation. Report raw and normalized bins separately, area, volume, charge sum, the surface-normal closure defect, and translated/co-rotated volume checks. Use separate processes per profile set and molecule for the registered one-compound replacement check, with identical finite masks. Measure both COSMO-SAC-dsp and Z0x, including solute and solvent roles; no amount of raw-bin variation alone establishes a ln gamma error.
+
+P17 A candidates are fixed here: canonical proper body-frame orientation with the deterministic degeneracy/atom-order rules in r3_common.canonical_xyz; equal-weight averages of raw psigmaA and volume over r0..r7 (mean8), r8..r15 (mean8b), and r0..r15 (mean16); and Lebedev order 41 with every other single-point/postprocessing setting unchanged. These are distinct experimental recipes, never combined implicitly. The averaging extension costs 200 additional raw TZVP single points. Canonical and Lebedev41 validation each use identity plus r0..r7 on all 25, at most 225 new single points per recipe. The canonical recipe must reproduce its own identity ln gamma across all eight rotations to max 1e-3 for both models. Lebedev41 must reduce the panel maximum orientation difference by at least one half and leave it below 0.01 for both models. Mean8 versus the disjoint mean8b must differ by max less than 0.01 in both models, and mean8 versus mean16 by max less than 0.005; these are finite-set consistency checks, not proofs of rotational invariance or continuum convergence. Each candidate additionally requires identical finite coverage versus the raw identity reference for both models, max COSMO-SAC-dsp ln gamma change below 0.05, and median COSMO-SAC-dsp difference versus UD below 0.15 on the frozen 2,302 occurrences. All changes in Z0x and both bin metrics are reported. The old E thresholds are not relaxed. Passing makes a recipe eligible for a separately authorized exploratory scoring pass, not an automatic replacement of the 630 primary profiles. There is no selection by best experimental MAE. A wider averaging radius, a new decay constant, or altered HB splitting is not authorized by this entry.
+
+P18 is an A numerical correction of profile metadata: preserve the NIST parser's COOH flag for a molecule whose own geometry-based parser sets has_COOH. Water retains H2O. Use ZC_R3_COOH_FLAG=1 only in an explicitly designated arm, or the metadata-only reconstruction in scripts/r3_metadata.py. Acceptance requires byte-identical raw sigma rows, unchanged metadata values other than the flag and explicit provenance fields, exact agreement with the existing parser's H2O/COOH/other flag rule, and identical finite coverage on the 25/2,302 check. In the one-compound substitution check, rows targeting a compound whose flag is unchanged must remain unchanged within 1e-10; Z0x predictions must remain unchanged within 1e-10 because its London dispersion does not use this flag. Report all COSMO-SAC-dsp changes and rerun the old UD acceptance statistic. If its median criterion fails, this corrected profile protocol is recorded as not accepted as a UD substitute, rather than restoring an incorrect flag to obtain a pass. The correction is not claimed to explain the Z0x-open deficit. Nothing is rescored silently.
+
+P19 is a single A final-precision trial, not an optimizer/threshold sweep. Pin pyscf 2.14.0 and pyberny 0.7.0. Starting from the same frozen geometry in each arm with fresh Berny histories, give the candidate at most 80 gradient evaluations at BP86/def2-SVP with the same DF auxiliary basis, grid level 2/default pruning, C-PCM epsilon 1e9/Lebedev 17/project radii, but conv_tol=1e-11 and conv_tol_grad=1e-7. Give the control the same 80-evaluation stage with original SCF tolerances. Then both arms receive at most 20 evaluations with a fresh Berny optimizer and all original registered settings, including conv_tol=1e-8 and its default orbital-gradient tolerance. Only convergence of this original-settings confirmation stage counts. The original internal-coordinate gradient/step tests and on-sphere rejection remain unchanged. No P15 noise override, looser geometry threshold, finer grid, different optimizer, or existing optimizer pickle is used. Native SCF failures are failures; exhausted budgets are censored. Never extend an arm after inspecting the result.
+
+For P19, first run both arms from the frozen saved geometries of all 25 validation molecules. All 25 must pass the original confirmation test, have identical finite coverage, max COSMO-SAC-dsp ln gamma change below 0.01 against the control, and median difference from UD below 0.15. Paired total wall time must be at most 1.50 times control; raw and normalized bins are reported without changing the historical E gates. Freeze and hash six chain inputs before either arm runs. A maximum of 100 total new quantum gradient evaluations per arm/chain is permitted, with a fixed runner deadline reserved for saving artifacts. The long-chain usefulness condition is at least one original-confirmation success in the tight arm whose control remains censored. Both this condition and the 25-molecule gate must pass. After acceptance, only chains passing the actual original confirmation test may replace S1/S2 profiles, with explicit A protocol metadata and side-by-side reporting. No flagged geometry is reclassified on a small Cartesian gradient alone.
```

## Source and execution record

All repository paths in S1–S13 refer to `Victor-Liang-ChE/zcosmo` at `c515e38e1a7fd91a02e1ff1f1209a81b67a7d49d`. The GitHub connector supplied these contents. Source identifiers below are Git blob hashes, not newly computed scientific results. Main was rechecked and remained at this commit before delivery.

| ID | Source | Verified identifier / relevant portion |
|---|---|---|
| S1 | `docs/astra/ROUND3_PROMPT.md`; `docs/OPTIMIZATION_BRIEF.md` | `b4c7a76d9a0cbdfab010e97fc713db38d32a4a2d`; `9042052e2c0884226db6f795d14f8ec8c0157bd4` |
| S2 | `docs/astra/round2/RESULTS.md` | `6da753d4b62210817abf98b25da7e1e12458ee45`; P15, S2, exploratory scorecard, unrun candidates |
| S3 | `docs/astra/round2/ZCOSMO_ROUND2_REPORT.md` | `25cc3faa43ab47c2a2681617ba6465d834e1c330`; complete local copy matched the repository blob, including old patches |
| S4 | `cloud/s19/s2_item.py`; `cloud/s19/s2_evaluate.py` | `8fe9e88bab956d2fec64f07664aec4eb9d1085f3`; `10a779b2cc33bf8fec5fefa93fa511181ffd7df5` |
| S5 | `PREREGISTRATION.md` | `f69e89ab19462b9bc35b1a5981d9837980b9ab3c`; October 4 registration/result entries and earlier referenced acceptance definitions |
| S6 | `src/zcosmo/pyscf_cosmo.py` | `049d01e6d3d90e5b1d0d2abcc337806c79a32295`; reconstructed full file matched this hash; `cosmo_segments`, `cavity_volume`, `to_profiles` |
| S7 | `data/raw/nist/to_sigma.py` | `9f2e0d6f3bb4da4880f9bd6ad702847f9308ed1d`; geometry/dispersion classification, Hsieh averaging, HB split, weighted binning, metadata |
| S8 | `src/zcosmo/cosmosac.py`; `results/z_params/Z0.json` | `c226a668b7b9dba9e7400cda180fafd8faa700f3`; `b19f9d403e6a958bc6a5651887de32f26631861e`; profile loader and London configuration |
| S9 | `src/zcosmo/z0x.py` | `80c3f1f3b61056a76678a80caf4120c58614adfe`; profile volumes, frozen dielectric table, interior derivative, unchanged endpoint branch |
| S10 | `src/zcosmo/metrics.py` | `25a25f26540a48433bbd78172671be2716b95598`; positional common masks, split/file selection, row-weighted metrics, bootstrap, LLE statistic |
| S11 | `src/zcosmo/evaluate.py` | `e154f0d9e695957a66c600e8211a0d0bca010c8c`; filtering, prediction paths, binodal fallback, 2 K temperature cache |
| S12 | `results/scorecard_test.json`; `data/benchmark/idac.csv` | `5a951e02f7f08ad4368228a51b0fdb0e285a99c6`; `0b20ebe7401af1b271eec99ddc6601f2871f8a54`; inspected scorecard and observation schema, not an invented full prediction CSV |
| S13 | `src/zcosmo/pyscf_cosmo_v2.py` | `1fd46da836fb219bba5de778386723aad42c8e88`; original settings, P15 opt-in, checkpointing, five-decimal saved XYZ |
| U1 | `pyscf/pyscf`, tag `v2.14.0`, `pyscf/solvent/pcm.py` | `8d11cfa0966a0990dc94d31df73a50c86b2d5eb8`; `gen_surface`, SWIG, area, Gaussian exponents, surface matrix |
| U2 | `pyscf/pyscf`, tag `v2.14.0`, `pyscf/dft/LebedevGrid.py` | `0fdfd69f451560616d34ff2cce4ce00a301e5214`; orders 29 and 41 map to 302 and 590 points |
| U3 | `pyberny/pyberny`, tag `0.7.0`, `src/berny/berny.py` | Tag commit `8f200b868b5b42247cbac7e2c5cec27811671fdd`, blob `cbecf60ce5b2d24c81c90454d2ddba2c586dd3af`; `BernyParams`, state, `is_converged` |
| U4 | `pyscf/pyscf`, tag `v2.14.0`, `pyscf/scf/hf.py` | `fee8d2b3a88b212612842fffc043e9217a205b14`; SCF kernel and orbital-gradient default |
| U5 | `pyscf/pyscf`, tag `v2.14.0`, `pyscf/geomopt/berny_solver.py` | `1f3f4d7bc7652da45a68c325e69123b9eb88a222`; callback order, native scanner, `kernel` return contract |

The `pyscf_cosmo_v2.py` application fixture contains the fetched fingerprint-function context, not a reconstructed executable quantum pipeline. Only the one-line fingerprint change is delivered in its diff.

The exact native install attempt failed with “Could not find a version that satisfies the requirement pyscf==2.14.0” in this runtime. No native output is substituted by the synthetic tests. The test numbers below are expressly synthetic or algebraic, and the 31 nonfinite rows in the synthetic fixture were deliberately constructed to test the guard rather than retrieved from a new scientific calculation.

Portable test output:

```json
{
  "canonical_max_coordinate_difference_A": 6.217248937900877e-15,
  "canonical_test_geometries": 4,
  "rotations_per_geometry": 100,
  "Hsieh_formula_max_difference_e_A2": 8.673617379884035e-19,
  "Shapley_identity_pass": true,
  "reordered_IDAC_rows_joined": 24,
  "duplicate_and_nonfinite_guards_pass": true,
  "sigma_round_trip_max_A2": 4.996003610813204e-16,
  "precision_budget": {
    "pre": 80,
    "original_confirmation": 20
  },
  "actual_volume_function_translation_identity_error_A3": 2.220446049250313e-16
}
```

Additional synthetic integration checks executed:

```json
[
  "freeze: 25-key/2302 occurrence manifest and source hashes",
  "mean8, disjoint mean8b, and mean16 aggregate the intended raw members",
  "profile E gate preserves and reports 31 jointly nonfinite synthetic rows",
  "profile E gate exits nonzero for a 0.01 synthetic ln-gamma discrepancy",
  "full eight-rotation panel comparison and panel gate",
  "mutated source input is rejected before reusing a frozen experiment"
]
```

Patch archive SHA-256 values:

```text
70afd9dd4f4280d0aee9e654fde338d50ed73df1ac4700a6d3c680137fc1d4d3  H3.patch
f77ec9213dbcaf074d97f764c2ac18c310fa1370bb478e7f68cdfc7b4c5fe7a4  P16.patch
84da2e6d7c5ec9409495bf48575f74c9d0995a89137c32548357d18dd22efcbd  P17.patch
cd245c8d90832dfb2778dee04e2f80a21419acba76fce13047616810602ab5f9  P18.patch
a98e89fc23e347e6ff777e3e20684e54284a4f01806a6f2a15d0984b1603fa64  P19.patch
0e96fe84330f21bb1bddeb734cbe58cd412b44701f9d45dbfcefeddcc61c3a0c  REG.patch
```

The next evidence should be the identity-aligned score audit and the fixed-rotation ln-gamma panel. Keep the historical primary set and flagged exploratory set distinct until those results justify a separately registered change.
