#!/usr/bin/env bash
set -euo pipefail

echo "[v073] preparing output directory"
mkdir -p output/v073_3

echo "[v073] entering libsignal v0.73.3 protocol bench directory"
cd workspace/v073_3/libsignal/rust/protocol

echo "[v073] listing session benchmarks"
cargo bench --bench session -- --list 2>&1 | tee ../../../../../output/v073_3/session_list.txt


run_one() {
  local run_id="$1"
  local out="../../../../../output/v073_3/session_full_run${run_id}.txt"

  echo "[v073] run ${run_id}/3: session encrypt"
  cargo bench --bench session -- '^session encrypt$' > "$out" 2>&1

  echo "[v073] run ${run_id}/3: session decrypt"
  cargo bench --bench session -- '^session decrypt$' >> "$out" 2>&1

  echo "[v073] run ${run_id}/3: session encrypt+decrypt 1 way"
  cargo bench --bench session -- '^session encrypt\+decrypt 1 way$' >> "$out" 2>&1

  echo "[v073] run ${run_id}/3: session encrypt+decrypt ping pong"
  cargo bench --bench session -- '^session encrypt\+decrypt ping pong$' >> "$out" 2>&1
}

run_one 1
run_one 2
run_one 3

echo "[v073] done"
