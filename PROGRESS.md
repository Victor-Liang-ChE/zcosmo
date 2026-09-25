# Progress log

Plan: see the "First-Principles Activity Model: Research Plan" doc. Pre-registration: `PREREGISTRATION.md`.

## 2026-09-24 (session 1)

Done
- Phase 0: ThermoML snapshot (9,184 files, to mid-2017) parsed to 2.1M property values. Offline name ->
  InChIKey resolution (55% of names; the rest are mostly ionic liquids, salts and drugs, outside v1).
  Benchmark after scope + cleaning: IDAC 3,438 points, VLE 46,127, LLE 7,158, HE 27,366.
  Herington test on 853 testable VLE series; failed series dropped and logged. Split frozen (sha256 in
  `data/benchmark/splits.sha256`).
- Phase 1: COSMO-SAC 2010/dsp reimplemented in NumPy; matches the NIST benchmark code to 2e-9 in
  ln gamma on 400 random pairs (go/no-go passed). Modified UNIFAC (Dortmund) baseline via thermo + ugropy.
- Phase 2 (partial): NIST UD sigma profiles (2,259 compounds, DMol3) cover 86 to 92% of benchmark rows.
  Uncovered compounds are listed in `results/dft_gap_list.csv` for ORCA runs on the Mac.
- Phase 3: Z0 constants computed: Klamt electrostatic estimate (conductor limit), H-bond constants from
  17 B3LYP-D4/def2-TZVP counterpoise dimers (PySCF, xTB geometries), London dispersion from D4 C6.

- Scorecards (results/scorecard_*.md): Z0 ties COSMO-SAC 2010 on held-out IDAC (0.76 vs 0.82),
  wins when both molecules are unseen (0.53 vs 0.90, 12 systems), has the best LLE split detection
  (balanced accuracy 0.90 vs 0.84 / 0.81 UNIFAC, significant), loses on VLE (18.8% vs 8.6%) and HE.
  Z1 (one scale on train IDAC, s = 0.53) generalizes worse than Z0.
- DFT H-bond constants ~5,700 for all three classes (fitted: 4,014 / 3,016 / 932).
- Ablation + sensitivity: electrostatics in the conductor limit is the main VLE error source; H-bond
  closure choices barely matter; one universal c_hb works as well as three.
- Z0e (registered before running): f_pol from Onsager permittivities (xTB dipoles, D4 polarizabilities).
  VLE 20.1 -> 17.5% on test (significant vs Z0), IDAC unchanged.
- LLE false-positive test on 336 fully miscible systems (src/zcosmo/lle_negatives.py).

Next (in order)
1. Improve the permittivity model (Kirkwood g-factor from dimer DFT, or liquid volume from xTB-MD),
   then rescore Z0e; the VLE gap to COSMO-SAC 2010 (17.5 vs 11.9 on test) is the main open problem.
2. Run ORCA BP86/def2-TZVP COSMO on the gap list (Mac, ~150 molecules) so coverage reaches 100%.
3. Sensitivity: DFT level for dimers (def2-QZVP, DLPNO-CCSD(T) on 5 dimers), tail width, f_pol.
4. Conformer ensembles (CREST) for the 100 most flexible molecules.
5. Pull the current ThermoML archive (2017 to 2026) through the browser for a temporal test split.


## 2026-09-24 (session 2, native Mac compute)
- Native job runner (`_queue/worker.sh`) on the M4 Pro; conda env `zcosmo` (conda-forge only) with
  pyscf, xtb, crest, dftd4, tblite, torch, transformers.
- Full NIST ThermoML archive (2020 snapshot, 11,923 files, standard InChIKeys) downloaded and verified
  (sha256 231161b5...). Extended benchmark in `data/benchmark_ext/`, with a temporal set of 2017-2019
  publications (IDAC 356, VLE 10,983, HE 3,388 rows with profiles). The archive ends in 2019, so no data
  postdate HANNA's training.
- HANNA (Nat. Commun. 2026) added as a data-driven reference (in-sample for HANNA).
- New registered models: Z0s (dielectric variant chosen on train: optical n^2, harmonic mean) and Z0x
  (composition-dependent screening from Onsager permittivities, no fitted constants, no choices).
  Z0x on test: IDAC 0.76 (tie with COSMO-SAC 2010), VLE 14.2% (Z0 18.8%, COSMO-SAC 8.6%), LLE balanced
  accuracy 0.90 (beats COSMO-SAC and UNIFAC, ties HANNA 0.88).
- Temporal set: all zero-constant models are worse than COSMO-SAC on mean IDAC and VLE; median IDAC similar.
- CCSD(T)/CBS check on 5 dimers: B3LYP-D4 overbinds by 0.33-0.85 kcal/mol (~15%); sensitivity says
  this moves results by < 0.05 in IDAC MAE.
- Manuscript draft: `manuscript/draft.md` (intro and discussion still to write out in full).

Next (in order)
1. Write out the introduction and discussion; make figures (parity plots, error map, LLE ROC-style plot).
2. Association term: the biggest remaining Z0x misses are alcohols in inert solvents; test a
   first-principles association (Wertheim-type) contribution with DFT dimer energies.
3. ORCA/PySCF profiles for the 137 gap compounds (needs a DMol3-consistent recipe or a full recalculation).
4. Conformer ensembles for flexible molecules (CREST now available natively).


## 2026-09-24/25 (session 3)
- Job runner v2 (`_queue/worker.sh`): parallel jobs, per-job kill files, works with macOS bash 3.2.
- Z0w (registered): Wertheim association with dimerization free energies (B3LYP-D4 + xTB qRRHO).
  Fails as registered (test IDAC 0.97, VLE 27.4%) because aqueous systems over-associate; post hoc,
  non-aqueous IDAC 0.67 vs 0.88 for COSMO-SAC 2010 (significant). Diagnosis: gas-phase bonding entropy.
- Open profiles (`zcosmo.pyscf_cosmo`): acceptance test failed narrowly (median 0.153 vs 0.15 bar;
  water 1.14). 136/137 gap compounds computed; exploratory coverage table in
  `results/scorecard_all_gap_exploratory.md` (Z0x 0.69 vs COSMO-SAC 2010 1.00 on 218 IDAC points).
- Conformers: 50 flexible molecules, 244 conformers; ensemble vs lowest conformer changes ln gamma by a
  median 0.01 and accuracy not at all (`_queue/done/26_conformer_eval.sh.log`).
- Manuscript sections 3.5 to 3.7 added.

Open items (none required for the paper as it stands)
1. Condensed-phase bonding entropy for Z0w (the one concrete fix the data point to).
2. Water's open profile disagreement (1.14): cavity radius or basis for H.
3. Submission prep: references, figure captions, supplementary tables.


## 2026-09-25 (session 4 start)
- Incident: a job from session 2 (bg_13, a multiprocessing pool fed from stdin) was orphaned when the v1
  runner stopped and kept respawning failing workers overnight, writing a 13 GB error log. Killed all its
  processes and truncated the log (disk back from 4.5 GB to ~17 GB free). Runner v2 kills whole process trees;
  never start multiprocessing from stdin again (scripts/lle_parallel.py is the safe pattern). Runner stopped.
- Water profile check: the open pipeline's water profile is slightly less polarized than DMol3's (tails 13.6 vs
  14.4 A^2); solutes in water come out 1-2 ln units lower. DFT-optimized geometry closes about a third of it;
  cavity radii move the two directions in opposite ways, so radii are not the fix. Accuracy against
  experiment on water rows is actually better for the open profiles (0.81 vs 0.88).
- Manuscript: figure captions, supplementary index, reference list (to verify) added.

Roadmap toward a complete fit-free fluid package (ordered by leverage)
1. Fully open profiles v2 (register first): DFT-optimized geometries in the conductor, rerun the
   acceptance test once. Makes the package independent of licensed DMol3 files.
2. First-principles "teacher" tier: solvation free energies from machine-learned potential MD (alchemical
   FEP) for ~50-100 small binaries, no experimental input. Use it (a) to test Z0x where no data exist and
   (b) to learn corrections to Z0x from computed, not measured, data. Fit-free in the experimental sense.
3. Condensed-phase association (Z0w2): bonding entropy from liquid-state sampling of the teacher tier
   instead of gas-phase RRHO.
4. Fit-free pure-component vapor pressure from the same free energies (removes the last experimental input
   in VLE), then an equation-of-state layer for pressure.
5. Packaging: pip-installable `zcosmo` with a thermo-compatible activity model and a DWSIM/CAPE-OPEN plugin.

## Environment notes
- Cloud container: 2 cores; reaches PyPI and (via the Mac) GitHub only. NIST, Zenodo and PubChem are
  blocked from both shells, so data came from GitHub mirrors.
- The Mac shell available to Claude is a 4-core, 3 GB Linux VM; native M4 Pro compute goes through
  `_queue/worker.sh` (started by Victor in Terminal).

## How to resume (for a fresh session)
1. Read this file, `PREREGISTRATION.md` and the plan doc "First-Principles Activity Model: Research Plan"
   (claude.ai artifact 08a51efb-42bc-47a0-8af7-b50e662271e6), in that order.
2. Cloud setup: copy this folder's `src tests scripts data/benchmark data/processed results` and the raw
   archives `data/raw/thermoml_mobley/*.tgz`, `data/raw/nist_cosmosac/*.tgz` into the container
   (stage them), extract the NIST archive to `data/raw/nist/` (UD/sigma3, UD/complist.txt, val/), then
   `pip install --break-system-packages rdkit thermo ugropy pyscf dftd4 tblite ase pytest`.
   Verify with `PYTHONPATH=src python3 -m pytest -q tests` and that `data/benchmark/splits.sha256` is
   d414402911946b14165a168ce40b8c00694d52de245adb6451fb6f65d7a2ffb6. Never change the split.
3. Predictions are not stored here (too large); regenerate with `scripts/eval_models.sh MODEL`.
4. Take the first unfinished item under "Next". Register any new model in PREREGISTRATION.md before
   running it. Score with `python3 -m zcosmo.metrics ... --split test --ref cosmosac2010`.
5. Before ending: sync code/results back into this folder (tar with --overwrite, never delete), add a
   dated entry to this log, and update the plan doc's results section.
6. Stop the recurring task when the preprint draft exists and every "Next" item is done or ruled out.
