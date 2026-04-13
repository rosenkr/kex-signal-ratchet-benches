#!/usr/bin/env bash
set -euo pipefail

echo "[pipeline] starting full benchmark pipeline"

bash scripts/setup.sh
bash scripts/run_v073.sh
bash scripts/run_v092.sh
bash scripts/run_spqr.sh
bash scripts/parse_results.sh

echo "[pipeline] finished successfully"
echo "[pipeline] outputs written to ./output"
