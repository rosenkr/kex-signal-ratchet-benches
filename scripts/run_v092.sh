#!/usr/bin/env bash
set -euo pipefail

echo "[v092] preparing output directory"
mkdir -p output/v092_1

echo "[v092] entering libsignal v0.92.1 protocol bench directory"
cd workspace/v092_1/libsignal/rust/protocol

echo "[v092] listing session benchmarks"
cargo bench --bench session -- --list 2>&1 | tee ../../../../../output/v092_1/session_list.txt

out="../../../../../output/v092_1/session_full.txt"

echo "[v092] running: encrypting on an existing chain"
cargo bench --bench session -- '^encrypting on an existing chain$' 2>&1 | tee "$out"

echo "[v092] running: decrypting on an existing chain"
cargo bench --bench session -- '^decrypting on an existing chain$' 2>&1 | tee -a "$out"

echo "[v092] running: session encrypt+decrypt 1 way"
cargo bench --bench session -- '^session encrypt\+decrypt 1 way$' 2>&1 | tee -a "$out"

echo "[v092] running: session encrypt+decrypt ping pong"
cargo bench --bench session -- '^session encrypt\+decrypt ping pong$' 2>&1 | tee -a "$out"

echo "[v092] done"
