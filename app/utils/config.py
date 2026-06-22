"""YAML configuration loader for service components."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import yaml

from app.pipeline.inference import InferenceConfig
from app.pipeline.sink import SinkConfig
from app.pipeline.source import SourceConfig
from app.pipeline.tracker import TrackerConfig


@dataclass(frozen=True)
class ServiceConfig:
    """Top-level service settings."""

    name: str
    log_level: str


@dataclass(frozen=True)
class PipelineConfig:
    """Typed aggregate configuration."""

    service: ServiceConfig
    source: SourceConfig
    inference: InferenceConfig
    tracker: TrackerConfig
    sink: SinkConfig


def _read_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def load_pipeline_config(path: str) -> PipelineConfig:
    """Load and validate pipeline settings from YAML file."""
    data = _read_yaml(Path(path))

    service = ServiceConfig(**data["service"])
    source = SourceConfig(**data["source"])
    inference = InferenceConfig(**data["inference"])
    tracker = TrackerConfig(**data["tracker"])
    sink = SinkConfig(**data["sink"])

    return PipelineConfig(
        service=service,
        source=source,
        inference=inference,
        tracker=tracker,
        sink=sink,
    )
