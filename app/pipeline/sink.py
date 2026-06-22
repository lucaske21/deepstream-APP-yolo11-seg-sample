"""RTSP sink service abstraction."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SinkConfig:
    """Configuration for sink stage."""

    rtsp_port: int
    mount_path: str
    codec: str
    bitrate: int


class SinkService:
    """Represents post_sink(rtsp) stage."""

    def __init__(self, cfg: SinkConfig) -> None:
        self.cfg = cfg

    def describe(self) -> str:
        return (
            f"post_sink(rtsp): encoder={self.cfg.codec}, bitrate={self.cfg.bitrate}, "
            f"url=rtsp://localhost:{self.cfg.rtsp_port}{self.cfg.mount_path}"
        )

    def gst_elements(self) -> list[str]:
        codec = self.cfg.codec.lower()
        encoder = "nvv4l2h264enc" if codec == "h264" else "nvv4l2h265enc"
        payloader = "rtph264pay" if codec == "h264" else "rtph265pay"
        return [encoder, payloader, "gst-rtsp-server"]
