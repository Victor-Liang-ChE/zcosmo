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
does not measure geometry error, and the glycol discrepancy remains unresolved.
Z0x was not fitted to ThermoML. Its exact infinite-dilution endpoint passed an
independent numerical gate and is enabled with `ZC_R6_ENDPOINT=1`. Archived matched benchmark
comparisons favor UD over open profiles for IDAC and excess enthalpy; the VLE
interval includes zero. LLE detection and checked endpoint compositions have
separate denominators and are not global phase-equilibrium certificates.
See [round-7 evidence](docs/astra/round7/RESULTS.md) and
[endpoint acceptance](docs/astra/round6/RESULTS.md).
