# DeepStream 8.x + PyServiceMaker YOLO11-Seg Learning Repository

This educational repository demonstrates how to build an instance segmentation video analytics pipeline with NVIDIA DeepStream, TensorRT, GStreamer, and a custom parser for YOLO11-Seg output.

PyServiceMaker is NVIDIA's Python-first service abstraction pattern for composing reusable pipeline components. This repository mirrors that style with modular source, inference, tracker, OSD, and sink services.

## Pipeline Goal

```text
RTSP Source(s)
   ↓
nvstreammux
   ↓
nvinfer (YOLO11-Seg TensorRT engine + custom parser)
   ↓
nvtracker
   ↓
nvdsosd
   ↓
Encoder + RTSP Output
```

Workflow in code:

```text
pre_source(rtsp) → inf_segment → post_tracker → post_osd → post_sink(rtsp)
```

## Repository Layout

```text
configs/
models/
parsers/
app/
scripts/
docs/
tests/
```

## Quick Start

1. Build parser shared library:
   ```bash
   ./scripts/build_parser.sh
   ```
2. Build TensorRT engine from ONNX:
   ```bash
   ./scripts/build_engine.sh
   ```
3. Run app:
   ```bash
   ./scripts/run.sh
   ```

## Notes

- `models/yolo11-seg.onnx` and `models/yolo11-seg.engine` are placeholders. Replace with actual model artifacts.
- Python modules are intentionally structured as reusable service components for learning PyServiceMaker-like decomposition.
- The parser source minimizes host-device copies conceptually by decoding tensors directly from contiguous buffers and only creating host-side metadata at attachment time.
