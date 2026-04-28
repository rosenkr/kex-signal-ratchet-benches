#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

apply_patch() {
  local dir="$1"
  local patch="$2"
  echo "[patch] applying $patch to $dir"
  git -C "$dir" apply --ignore-whitespace "$REPO_ROOT/patches/$patch"
}

echo "[patch] applying workspace modifications"

apply_patch workspace/v073_3/libsignal v073_libsignal.patch
apply_patch workspace/v092_1/libsignal v092_libsignal.patch
apply_patch workspace/SPQR            spqr.patch

echo "[patch] done"
