"""Tracker component abstraction for post-inference object association."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TrackerConfig:
    """Configuration for nvtracker stage."""

    config_file: str


class TrackerService:
    """Represents post_tracker processing stage."""

    def __init__(self, cfg: TrackerConfig) -> None:
        self.cfg = cfg

    def describe(self) -> str:
        return f"post_tracker: nvtracker(config={self.cfg.config_file})"

    def gst_elements(self) -> list[str]:
        return ["nvtracker"]
