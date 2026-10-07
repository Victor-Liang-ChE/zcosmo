# Round 10: measured results

Reference: round 10 registered 2026-10-07 in 39cd85d (P41, P42, P43 and REG10 applied unchanged to 4dc8985). The comparison manifest was frozen in ba033e4 (SHA256 `4acf76db…fca0f`, in `PLAN_SHA256.txt`). Everything ran on the Mac in queue jobs 392 to 394. Nothing was computed: 0 SCF calls and 0 model calls. Acquisition took 5.9 s of wall time and the comparison 2.9 s.

Use terms: Victor confirmed the project is academic and non-profit before acquisition, as the NIST UD notice requires. The twelve raw `.cosmo` files and the detailed per-member comparison JSON stay in a private folder on the Mac, outside the repository. This file reports aggregate descriptors only.

Deviations, none of which affects any numerical result:

- **Self-test on macOS.** `r10_selftest.py` had 2 of 20 tests fail on the Mac: `test_frozen_input_mutation` and `test_output_root_is_private_and_fresh`. Both compare a resolved temporary path (`/private/var/…`) with an unresolved one (`/var/…`). macOS links `/var` to `/private/var`. These are test-assertion artifacts. The code under test resolved paths correctly, and all 20 tests passed in the Linux container before registration.
- **Profile root.** The first `freeze` failed before writing anything, because the registration worktree has no `profiles_v2/`. Those profiles are untracked data in the main Mac checkout. It was rerun with `--profile-root` pointing to the main checkout's `data/pyscf_sigma`. The lineage gates then confirmed those exact P25-recorded hashes.

## P41, acquisition: complete

All twelve raw UD files and the two provenance documents were retrieved from `usnistgov/COSMOSAC` at 1b82456, and every Git blob matched. The UD notice reads: free for non-profit, academic purposes; redistribution without the authors' consent is prohibited. It also says the UD set revised the conformations of about a third of the VT-2005 compounds, based on vapor-pressure predictions.

## P42, same-parser replay: all twelve lineage gates passed

Every recovered UD raw table regenerates the exact Mac UD sigma profile, with a maximum bin difference of about 1e-14 Å². Every archived P25 open table regenerates its own stored profile. Each `.cosmo` file is therefore the input that produced the UD profile used throughout R4 to R6. The electronic input decks themselves are still unverified (`electronic_input_deck_verified: false`).

Tails are in Å² of |σ| ≥ 0.01 e/Å², given as UD / open. Raw is the tessera area before averaging, averaged is after Hsieh averaging, and final is the binned profile.

| member | raw tail | averaged tail | final tail | heavy RMSD (Å) | heavy backbone, UD vs open | closest OH···O H–A distance (Å), UD / open |
|---|---|---|---|---:|---|---|
| ethylene glycol | 41.0 / 34.5 | 31.0 / 21.2 | 33.0 / 23.0 | 0.69 | anti (176°) vs gauche (57°) | 3.98 / 2.19 |
| diethylene glycol | 47.6 / 40.7 | 34.0 / 25.4 | 38.0 / 27.7 | 1.11 | all anti vs two gauche | 3.93 / 2.37 |
| triethylene glycol | 57.1 / 49.0 | 36.5 / 25.7 | 42.3 / 27.9 | 1.03 | all anti vs four gauche | 3.93 / 2.27 |
| tetraethylene glycol | 67.9 / 61.1 | 37.7 / 37.7 | 46.8 / 41.8 | 1.58 | all anti vs seven gauche | 3.92 / 2.28 |
| glycerol | 48.3 / 52.9 | 32.3 / 34.4 | 35.0 / 37.3 | 0.68 | mixed, both | 2.30 / 2.21 |
| propylene glycol | 33.3 / 38.1 | 23.9 / 27.8 | 25.9 / 30.0 | 0.83 | anti/gauche swapped | 2.21 / 3.91 |
| methoxyethanol | 29.4 / 28.1 | 20.8 / 19.8 | 23.9 / 21.0 | 0.02 | same | 3.93 / 3.93 |
| dimethoxyethane | 19.2 / 17.6 | 10.3 / 13.7 | 14.4 / 14.4 | 0.60 | one gauche in open | – |
| water | 34.1 / 31.2 | 26.8 / 25.2 | 27.7 / 26.5 | 0.00 | – | – |
| methanol | 20.7 / 19.9 | 16.8 / 14.9 | 17.9 / 15.7 | 0.01 | – | – |
| tetrahydrofuran | 10.6 / 10.2 | 9.2 / 7.7 | 9.6 / 8.4 | 0.01 | same | – |
| nonane | 0.0 / 0.1 | 0.0 / 0.0 | 0.0 / 0.0 | 0.88 | all anti vs three gauche | – |

No member meets the registered O–H···O contact rule (D–A ≤ 3.2 Å, H–A ≤ 2.5 Å, angle ≥ 120°) in either source. The open linear glycols have H–A distances of 2.2 to 2.4 Å, which fail only the angle criterion.

Other descriptors:

- **Net charge.** Every open table carries a net charge of −0.012 to −0.045 e (the known P22 offset). UD tables are −0.001 to −0.002 e.
- **Charge outliers.** Open tables have much more negative extreme tessera charge densities, for example σ_min −0.086 against −0.024 for propylene glycol, and −0.091 against −0.020 for tetraethylene glycol.
- **Surface resolution.** Open tables have about 3.5 times as many surface segments.
- **Totals.** Total areas agree within 1 to 4%.

What this establishes, and what it does not:

- **Geometry differs systematically.** The four UD linear glycols are fully extended, all-anti chains with no OH group near another oxygen. The open geometries all fold, with gauche O–C–C–O units and a terminal OH about 2.2 to 2.4 Å from an oxygen. For glycerol and propylene glycol the direction reverses: the UD geometry has the short OH···O approach, or both do. Those are exactly the two polyols where the P21 shape effect had the opposite sign. In the four linear glycols and propylene glycol, the geometry with the short OH···O approach has the smaller polar tail. Glycerol does not fit this simple picture: both geometries have a short approach, and the open tail is the larger one.
- **Method difference at matched geometry is small.** Where the geometries match (water, methanol, THF, methoxyethanol, RMSD ≤ 0.02 Å), the raw tails differ by 0.4 to 2.9 Å². The linear glycols differ by 6.5 to 8.1 Å² raw and 8.6 to 10.8 Å² after averaging (tetraethylene glycol excepted).
- **This is still descriptive.** It is not a causal partition. Under the registered decomposition, the crossed quantity p_O(R_U), the open method evaluated at the UD geometry, was not computed. The method difference at matched geometry is measured only on small rigid molecules, not on glycols. Nothing here shows which conformation is right for the liquid. UD's extended chains were partly revised to fit vapor pressures, so they are not an independent gas- or liquid-phase reference. Nothing is adopted: P35 stays unresolved, and the 630 + 6 profiles are unchanged.

## P43, reporting: applied

In the registration commit, the README, `GLYCOL_STATUS.md` and `PROVENANCE_STATUS.md` were updated as supplied. A dated outcome line is appended to `PROVENANCE_STATUS.md` with this record, so its "not yet executed" sentence is no longer the current status.
