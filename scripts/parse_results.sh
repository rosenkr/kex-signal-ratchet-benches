#!/usr/bin/env bash
set -euo pipefail

echo "[parse] preparing parsed output directories"
mkdir -p output/v073_3 output/v092_1 output/spqr

echo "[parse] parsing libsignal v0.73.3 session logs"
python3 parsers/parse_criterion.py \
  output/v073_3/session_full_run1.txt \
  output/v073_3/session_full_run2.txt \
  output/v073_3/session_full_run3.txt \
  > output/v073_3/session_extracted.csv

echo "[parse] parsing libsignal v0.92.1 session logs"
python3 parsers/parse_criterion.py \
  output/v092_1/session_full_run1.txt \
  output/v092_1/session_full_run2.txt \
  output/v092_1/session_full_run3.txt \
  > output/v092_1/session_extracted.csv

echo "[parse] computing libsignal session medians"
python3 parsers/median_criterion.py output/v073_3/session_extracted.csv \
  > output/v073_3/session_medians.csv

python3 parsers/median_criterion.py output/v092_1/session_extracted.csv \
  > output/v092_1/session_medians.csv

echo "[parse] parsing standalone SPQR logs"
python3 parsers/parse_spqr_benches.py \
  output/spqr/spqr_full_run1.txt \
  output/spqr/spqr_full_run2.txt \
  output/spqr/spqr_full_run3.txt \
  > output/spqr/spqr_extracted.csv

python3 parsers/parse_spqr_benches.py \
  output/spqr/chain_full_run1.txt \
  output/spqr/chain_full_run2.txt \
  output/spqr/chain_full_run3.txt \
  > output/spqr/chain_extracted.csv

echo "[parse] computing standalone SPQR medians"
python3 parsers/median_spqr.py output/spqr/spqr_extracted.csv \
  > output/spqr/spqr_medians.csv

python3 parsers/median_spqr.py output/spqr/chain_extracted.csv \
  > output/spqr/chain_medians.csv

echo "[parse] writing markdown summary"
python3 scripts/write_summary.py

echo "[parse] done"
