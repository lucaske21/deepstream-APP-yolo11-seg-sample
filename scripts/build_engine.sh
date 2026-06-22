#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ONNX_PATH="${REPO_ROOT}/models/yolo11-seg.onnx"
ENGINE_PATH="${REPO_ROOT}/models/yolo11-seg.engine"

if [[ ! -f "${ONNX_PATH}" ]]; then
  echo "Missing ONNX model: ${ONNX_PATH}" >&2
  exit 1
fi

trtexec \
  --onnx="${ONNX_PATH}" \
  --saveEngine="${ENGINE_PATH}" \
  --fp16 \
  --workspace=4096 \
  --verbose

echo "TensorRT engine generated at ${ENGINE_PATH}"
