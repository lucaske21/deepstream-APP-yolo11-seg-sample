# Architecture

```mermaid
flowchart TD
  A[RTSP Source(s)] --> B[nvstreammux]
  B --> C[nvinfer
YOLO11-Seg + custom parser]
  C --> D[nvtracker]
  D --> E[nvdsosd]
  E --> F[Encoder + RTP Payloader]
  F --> G[RTSP Server Output]
```

The application follows componentized service construction to mirror PyServiceMaker responsibilities:

- SourceService
- InferenceService
- TrackerService
- OsdService
- SinkService
