"""Inference service abstraction for YOLO11-Seg nvinfer stage."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InferenceConfig:
    """Configuration for nvinfer stage."""

    config_file: str


class InferenceService:
    """Represents the inf_segment stage in the service chain."""

    def __init__(self, cfg: InferenceConfig) -> None:
        self.cfg = cfg

    def describe(self) -> str:
        return f"inf_segment: nvinfer(config={self.cfg.config_file})"

    def gst_elements(self) -> list[str]:
        return ["nvinfer"]
