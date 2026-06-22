"""Application entrypoint for the DeepStream YOLO11-Seg learning service."""

from __future__ import annotations

from app.pipeline.inference import InferenceService
from app.pipeline.osd import OsdService
from app.pipeline.sink import SinkService
from app.pipeline.source import SourceService
from app.pipeline.tracker import TrackerService
from app.utils.config import load_pipeline_config
from app.utils.logger import configure_logging, get_logger

LOGGER = get_logger(__name__)


def build_service(config_path: str):
    """Build the ordered service chain for pipeline assembly.

    Args:
        config_path: Path to YAML configuration.

    Returns:
        List of configured service components in processing order.
    """
    cfg = load_pipeline_config(config_path)
    configure_logging(cfg.service.log_level)

    return [
        SourceService(cfg.source),
        InferenceService(cfg.inference),
        TrackerService(cfg.tracker),
        OsdService(),
        SinkService(cfg.sink),
    ]


def main(config_path: str = "configs/pipeline.yaml") -> int:
    """Create and print a pipeline plan for teaching and validation."""
    chain = build_service(config_path)
    LOGGER.info("DeepStream YOLO11-Seg service initialized with %d components", len(chain))
    for idx, component in enumerate(chain, start=1):
        LOGGER.info("%d. %s", idx, component.describe())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
