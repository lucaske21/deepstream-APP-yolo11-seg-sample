# Parser Tutorial: `nvdsparse_yolo_instance_mask.cpp`

## Parsing Steps

1. Read detection and prototype tensors from `outputLayersInfo`.
2. Decode bbox center-width-height to pixel coordinates.
3. Select top class score and apply per-class threshold.
4. Decode mask coefficients for each candidate.
5. Run class-aware NMS.
6. Multiply mask coefficients with prototype tensor to build binary masks.
7. Populate `NvDsInferInstanceMaskInfo` and attach to object list.

## Why this is efficient

- Reads TensorRT output as contiguous float buffers.
- Performs decoding in-place over these buffers.
- Only allocates host memory once per finalized mask metadata object.
