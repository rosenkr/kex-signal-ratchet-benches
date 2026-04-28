#!/usr/bin/env bash
set -euo pipefail

echo "[v073] preparing output directory"
mkdir -p output/v073_3

echo "[v073] entering libsignal v0.73.3 protocol bench directory"
cd workspace/v073_3/libsignal/rust/protocol

echo "[v073] listing session benchmarks"
cargo bench --bench session -- --list 2>&1 | tee ../../../../../output/v073_3/session_list.txt

out="../../../../../output/v073_3/session_full.txt"

echo "[v073] running: session encrypt"
cargo bench --bench session -- '^session encrypt$' 2>&1 | tee "$out"

echo "[v073] running: session decrypt"
cargo bench --bench session -- '^session decrypt$' 2>&1 | tee -a "$out"

echo "[v073] running: session encrypt+decrypt 1 way"
cargo bench --bench session -- '^session encrypt\+decrypt 1 way$' 2>&1 | tee -a "$out"

echo "[v073] running: session encrypt+decrypt ping pong"
cargo bench --bench session -- '^session encrypt\+decrypt ping pong$' 2>&1 | tee -a "$out"

echo "[v073] done"
