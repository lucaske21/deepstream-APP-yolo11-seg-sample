# DeepStream Metadata Primer

- `NvDsBatchMeta`: per-batch metadata root.
- `NvDsFrameMeta`: frame-level metadata for each stream in batch.
- `NvDsObjectMeta`: object-level metadata (bbox, class, confidence, mask).
- `NvDsClassifierMeta`: optional secondary classification metadata.
- `NvDsInferTensorMeta`: raw tensor metadata from inference.

## Example Mapping

```text
NvDsBatchMeta
└── NvDsFrameMeta (stream 0)
    ├── NvDsObjectMeta (person, mask attached)
    └── NvDsDisplayMeta (OSD draw commands)
```
