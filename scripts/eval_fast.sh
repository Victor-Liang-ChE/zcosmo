#!/usr/bin/env bash
# IDAC + VLE + HE only (no LLE), for sensitivity variants
cd "$(dirname "$0")/.."
export PYTHONPATH=src
for m in "$@"; do python3 -m zcosmo.evaluate "$m" --tables idac,vle,he; done
