#!/usr/bin/env bash
set -euo pipefail

echo "[setup] loading pinned versions"
source config/versions.env

mkdir -p workspace/v073_3 workspace/v092_1 workspace/SPQR output

echo "[setup] cloning/updating libsignal old version workspace"
if [ ! -d workspace/v073_3/libsignal/.git ]; then
  git clone "$LIBSIGNAL_REPO" workspace/v073_3/libsignal
fi

echo "[setup] cloning/updating libsignal new version workspace"
if [ ! -d workspace/v092_1/libsignal/.git ]; then
  git clone "$LIBSIGNAL_REPO" workspace/v092_1/libsignal
fi

echo "[setup] cloning/updating SPQR workspace"
if [ ! -d workspace/SPQR/.git ]; then
  git clone "$SPQR_REPO" workspace/SPQR
fi

echo "[setup] marking mounted repos as safe for git"
git config --global --add safe.directory /app/workspace/v073_3/libsignal || true
git config --global --add safe.directory /app/workspace/v092_1/libsignal || true
git config --global --add safe.directory /app/workspace/SPQR || true
git config --global --add safe.directory "$(pwd)/workspace/v073_3/libsignal" || true
git config --global --add safe.directory "$(pwd)/workspace/v092_1/libsignal" || true
git config --global --add safe.directory "$(pwd)/workspace/SPQR" || true

echo "[setup] checking out libsignal old tag: $LIBSIGNAL_OLD_TAG"
git -C workspace/v073_3/libsignal fetch --tags
git -C workspace/v073_3/libsignal checkout "$LIBSIGNAL_OLD_TAG"

echo "[setup] checking out libsignal new tag: $LIBSIGNAL_NEW_TAG"
git -C workspace/v092_1/libsignal fetch --tags
git -C workspace/v092_1/libsignal checkout "$LIBSIGNAL_NEW_TAG"

echo "[setup] checking out SPQR ref: $SPQR_REF"
git -C workspace/SPQR fetch --tags
git -C workspace/SPQR checkout "$SPQR_REF"

echo "[setup] applying benchmark counter patches"
bash scripts/patch_workspace.sh

echo "[setup] writing version info"
mkdir -p output/metadata

{
  echo "libsignal_old_tag=$LIBSIGNAL_OLD_TAG"
  git -C workspace/v073_3/libsignal rev-parse HEAD
} > output/metadata/libsignal_old_version.txt

{
  echo "libsignal_new_tag=$LIBSIGNAL_NEW_TAG"
  git -C workspace/v092_1/libsignal rev-parse HEAD
} > output/metadata/libsignal_new_version.txt

{
  echo "spqr_ref=$SPQR_REF"
  git -C workspace/SPQR rev-parse HEAD
} > output/metadata/spqr_version.txt

echo "[setup] done"
