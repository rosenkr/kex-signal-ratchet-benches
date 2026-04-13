#!/usr/bin/env bash
set -euo pipefail

echo "[spqr] preparing output directory"
mkdir -p output/spqr

echo "[spqr] entering SPQR repo"
cd workspace/SPQR

echo "[spqr] listing spqr benchmarks"
cargo +nightly bench --bench spqr -- --list > ../../output/spqr/spqr_list.txt 2>&1

echo "[spqr] listing chain benchmarks"
cargo +nightly bench --bench chain -- --list > ../../output/spqr/chain_list.txt 2>&1

echo "[spqr] running spqr bench target (1/3)"
cargo +nightly bench --bench spqr > ../../output/spqr/spqr_full_run1.txt 2>&1

echo "[spqr] running spqr bench target (2/3)"
cargo +nightly bench --bench spqr > ../../output/spqr/spqr_full_run2.txt 2>&1

echo "[spqr] running spqr bench target (3/3)"
cargo +nightly bench --bench spqr > ../../output/spqr/spqr_full_run3.txt 2>&1

echo "[spqr] running chain bench target (1/3)"
cargo +nightly bench --bench chain > ../../output/spqr/chain_full_run1.txt 2>&1

echo "[spqr] running chain bench target (2/3)"
cargo +nightly bench --bench chain > ../../output/spqr/chain_full_run2.txt 2>&1

echo "[spqr] running chain bench target (3/3)"
cargo +nightly bench --bench chain > ../../output/spqr/chain_full_run3.txt 2>&1

echo "[spqr] done"
