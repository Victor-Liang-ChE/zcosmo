# Z-COSMO: how far can COSMO-SAC go with zero fitted constants?

Research code for a predictive activity-coefficient model whose interaction constants come from
theory and quantum chemistry instead of experimental fits, benchmarked against modified UNIFAC
(Dortmund) and COSMO-SAC 2010 / dsp on NIST ThermoML data. The plan and the pass/fail criteria
live in `PREREGISTRATION.md`; current status and next steps in `PROGRESS.md`; results in `results/`.

## Layout
```
data/raw/            ThermoML XML snapshot (MobleyLab mirror), NIST COSMO-SAC profiles (UD, VT2005)
data/processed/      flattened ThermoML tables, identity map, rejection log
data/benchmark/      frozen benchmark tables (idac, vle, lle, he), compounds, splits (+ sha256)
src/zcosmo/
  thermoml_parse.py  XML -> long tables
  identity.py        compound name -> InChIKey, formula-checked, offline
  build_benchmark.py long tables -> IDAC / VLE / LLE / HE rows
  scope.py           scope, quality filters (Herington), molecule-level splits
  cosmosac.py        COSMO-SAC 2010 / dsp (matches NIST to 2e-9) + London dispersion term
  baselines.py       modified UNIFAC (Dortmund)
  qc_hbond.py        B3LYP-D4/def2-TZVP counterpoise H-bond dimer energies (PySCF, xTB geometries)
  qc_disp.py         D4 molecular C6 and polarizabilities
  zmodel.py          builds Z0 and the ablation parameter sets
  fit_z1.py          one global scale on train IDAC -> Z1
  evaluate.py        predictions for every table
  metrics.py         scorecard with system-level bootstrap CIs
tests/               NIST reproduction test, Gibbs-Duhem test
```

## Reproduce
```
pip install numpy scipy pandas lxml rdkit thermo ugropy pyscf dftd4 tblite ase pytest
export PYTHONPATH=src
python src/zcosmo/thermoml_parse.py data/raw/thermoml data/processed
python -c "from zcosmo.identity import *"   # see scripts/run_all.sh for the full chain
bash scripts/run_all.sh
```

## Current evidence

The open workflow produced 630 profiles that passed the original Berny predicate,
plus six separately flagged S1/S2 profiles. Resolved errors from omitted XC-grid
response and incomplete finite-difference checks limit stationarity claims.
The corrected-gradient calibration failed its preregistered compatibility gate;
no corrected-gradient rollout or chain rescue is accepted. Displacement sensitivity
does not measure geometry error, and the liquid-state explanation of the glycol
discrepancy remains unresolved.
Z0x was not fitted to ThermoML. Its exact infinite-dilution endpoint passed an
independent numerical gate and is enabled with `ZC_R6_ENDPOINT=1`. Archived matched benchmark
comparisons favor UD over open profiles for IDAC and excess enthalpy; the VLE
interval includes zero. LLE detection and checked endpoint compositions have
separate denominators and are not global phase-equilibrium certificates.
The [round-8 stage-isolation test](docs/astra/round8/RESULTS.md) left the TEG
energy-gradient mismatch unresolved; its numerical diagnostic budget is closed.
See [round-7 evidence](docs/astra/round7/RESULTS.md) and
[endpoint acceptance](docs/astra/round6/RESULTS.md).

The [round-10 replay](docs/astra/round10/RESULTS.md) linked all twelve recovered
UD raw files to their historical profiles. The [round-11 ordered cross](docs/astra/round11/RESULTS.md)
attributed the polar-tail gaps for ethylene, diethylene and triethylene glycol
mainly to stored coordinate inputs, without a whole-profile attribution label.
Tetraethylene glycol differed: its raw-tail gap was mainly method.

In [round-12 retrospective scoring](docs/astra/round12/RESULTS.md), on 142
already-inspected glycol-solvent observations, using our open method at the UD
solvent coordinates reduced MAE in ln gamma from 1.813 to 0.702, versus 0.419
for the UD-solvent comparator. Original open solute profiles and Z0x were held
fixed. This removes about 80% of the open-to-UD comparator error gap, mainly
through shape; tetraethylene glycol recovers only 13%. The remaining 0.283
pooled MAE difference is conditional on the same-coordinate method-bundle
comparison. It is not the total remaining experimental error or a universal
method-error bound.

These inspected-row results do not establish the liquid conformer distribution
or a held-out accuracy improvement. No crossed profile or conformer-selection
rule is adopted. The 630 primary plus six flagged profiles remain frozen.
P35's present explanatory campaign is closed with these findings; its liquid-state
mechanism remains unresolved. The separate numerical-gradient campaign stays closed.

R17 manuscript closeout (2026-10-08): the subsequent [R15 factorial](docs/astra/round15/RESULTS.md)
attributes 2.24 percentage points, about 67% of the Z0x-to-2010 VLE gap on 963 exposed observations,
to the implemented London closure. The [R16 LV1 screen](docs/astra/round16/RESULTS.md) failed its
registered tradeoff gates and is not adopted. The VLE gap remains unresolved and the model-development
campaign is closed for this project. The manuscript and supplement retain the unfavorable result,
actual source-specific denominators and numerical qualifications. "Fit-free" here means no new
ThermoML regression of the interaction constants, not absence of all empirical upstream inputs.
The reproduction commands above describe the historical full workflow; they are not authorization to
rerun it during R17. Only the zero-model reporting commands in the R17 report are proposed now.
Existing bibliography and artifact checks remain editorial submission tasks, not a new research budget.
