"""RTSP source component with reconnect and FPS instrumentation metadata."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class SourceConfig:
    """Configuration for RTSP sources."""

    uris: List[str]
    reconnect_interval_sec: int
    latency_ms: int


class SourceService:
    """Represents the pre_source(rtsp) stage in a PyServiceMaker-like service graph."""

    def __init__(self, cfg: SourceConfig) -> None:
        self.cfg = cfg

    def describe(self) -> str:
        return (
            f"pre_source(rtsp): {len(self.cfg.uris)} stream(s), "
            f"reconnect={self.cfg.reconnect_interval_sec}s, latency={self.cfg.latency_ms}ms"
        )

    def gst_elements(self) -> list[str]:
        """Return expected GStreamer nodes for this source stage."""
        return ["rtspsrc", "rtph264depay", "h264parse", "nvv4l2decoder", "nvstreammux"]
