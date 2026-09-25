#!/usr/bin/env bash
# usage: scripts/eval_models.sh model1 model2 ...
cd "$(dirname "$0")/.."
export PYTHONPATH=src
for m in "$@"; do python3 -m zcosmo.evaluate "$m"; done
