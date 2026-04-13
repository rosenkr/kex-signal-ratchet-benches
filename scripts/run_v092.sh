#!/usr/bin/env bash
set -euo pipefail

echo "[v092] preparing output directory"
mkdir -p output/v092_1

echo "[v092] entering libsignal v0.92.1 protocol bench directory"
cd workspace/v092_1/libsignal/rust/protocol

echo "[v092] listing session benchmarks"
cargo bench --bench session -- --list > ../../../../../output/v092_1/session_list.txt 2>&1

run_one() {
  local run_id="$1"
  local out="../../../../../output/v092_1/session_full_run${run_id}.txt"

  echo "[v092] run ${run_id}/3: encrypting on an existing chain"
  cargo bench --bench session -- '^encrypting on an existing chain$' > "$out" 2>&1

  echo "[v092] run ${run_id}/3: decrypting on an existing chain"
  cargo bench --bench session -- '^decrypting on an existing chain$' >> "$out" 2>&1

  echo "[v092] run ${run_id}/3: session encrypt+decrypt 1 way"
  cargo bench --bench session -- '^session encrypt\+decrypt 1 way$' >> "$out" 2>&1

  echo "[v092] run ${run_id}/3: session encrypt+decrypt ping pong"
  cargo bench --bench session -- '^session encrypt\+decrypt ping pong$' >> "$out" 2>&1
}

run_one 1
run_one 2
run_one 3

echo "[v092] done"
