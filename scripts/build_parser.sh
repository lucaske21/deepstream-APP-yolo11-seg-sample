#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_DIR="${REPO_ROOT}/parsers/build"

mkdir -p "${BUILD_DIR}"
cmake -S "${REPO_ROOT}/parsers" -B "${BUILD_DIR}"
cmake --build "${BUILD_DIR}" -- -j"$(nproc)"

echo "Parser built at ${BUILD_DIR}/libnvdsparse_yolo_instance_mask.so"
