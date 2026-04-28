#!/usr/bin/env bash
set -euo pipefail

echo "[spqr] preparing output directory"
mkdir -p output/spqr

echo "[spqr] entering SPQR repo"
cd workspace/SPQR

echo "[spqr] listing spqr benchmarks"
cargo +nightly bench --bench spqr -- --list 2>&1 | tee ../../output/spqr/spqr_list.txt

echo "[spqr] listing chain benchmarks"
cargo +nightly bench --bench chain -- --list 2>&1 | tee ../../output/spqr/chain_list.txt

echo "[spqr] running spqr bench target"
cargo +nightly bench --bench spqr 2>&1 | tee ../../output/spqr/spqr_full.txt

echo "[spqr] running chain bench target"
cargo +nightly bench --bench chain 2>&1 | tee ../../output/spqr/chain_full.txt

echo "[spqr] done"
