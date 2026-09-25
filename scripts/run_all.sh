#!/usr/bin/env bash
# Full pipeline, from raw ThermoML XML to the scorecard.
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH=src
python3 src/zcosmo/thermoml_parse.py data/raw/thermoml data/processed
python3 - <<'EOF'
import pandas as pd
from pathlib import Path
from zcosmo.identity import load_ud, resolve
ud = load_ud(Path("data/raw/nist/UD/complist.txt")); ud.to_csv("data/processed/ud_complist.csv", index=False)
c = pd.read_csv("data/processed/tml_compounds.csv")
resolve(c[["name", "formula"]].drop_duplicates(), ud).to_csv("data/processed/tml_identity.csv", index=False)
EOF
python3 src/zcosmo/build_benchmark.py
python3 src/zcosmo/scope.py
sha256sum -c <(echo "$(cat data/benchmark/splits.sha256)  -") < data/benchmark/splits.json || echo "WARNING: split hash changed"
python3 -m zcosmo.qc_disp
python3 -m zcosmo.qc_hbond --basis def2-tzvp
python3 -m zcosmo.zmodel
python3 -m zcosmo.fit_z1
for m in unifac_do cosmosac2010 cosmosac_dsp Z0 Z1 abl_es abl_hb abl_disp Z0_nodisp; do
  python3 -m zcosmo.evaluate "$m"
done
python3 -m zcosmo.metrics unifac_do cosmosac2010 cosmosac_dsp Z0 Z1 --split test --ref cosmosac2010
python3 -m zcosmo.metrics unifac_do cosmosac2010 cosmosac_dsp Z0 Z1 --split test_both --ref cosmosac2010
python3 -m zcosmo.metrics cosmosac_dsp abl_es abl_hb abl_disp Z0_nodisp Z0 --split test --ref cosmosac_dsp --tag ablation
