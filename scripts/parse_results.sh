#!/usr/bin/env bash
set -euo pipefail

echo "[parse] preparing parsed output directories"
mkdir -p output/v073_3 output/v092_1 output/spqr

echo "[parse] parsing libsignal v0.73.3 session logs"
python3 parsers/parse_criterion.py \
  --criterion-root workspace/v073_3/libsignal/target/criterion \
  output/v073_3/session_full.txt \
  > output/v073_3/session_values.csv

echo "[parse] parsing libsignal v0.92.1 session logs"
python3 parsers/parse_criterion.py \
  --criterion-root workspace/v092_1/libsignal/target/criterion \
  output/v092_1/session_full.txt \
  > output/v092_1/session_values.csv

echo "[parse] parsing standalone SPQR logs"
python3 parsers/parse_spqr_benches.py \
  output/spqr/spqr_full.txt \
  > output/spqr/spqr_values.csv

python3 parsers/parse_spqr_benches.py \
  output/spqr/chain_full.txt \
  > output/spqr/chain_values.csv

echo "[parse] writing markdown summary"
python3 scripts/write_summary.py

echo "[parse] done"
