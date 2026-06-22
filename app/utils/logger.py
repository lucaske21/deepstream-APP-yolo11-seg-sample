"""Logging utilities."""

from __future__ import annotations

import logging


_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def configure_logging(level: str = "INFO") -> None:
    """Configure root logger with project-wide format."""
    logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO), format=_FORMAT)


def get_logger(name: str) -> logging.Logger:
    """Get named logger."""
    return logging.getLogger(name)
