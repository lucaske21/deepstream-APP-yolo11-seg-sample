"""Metadata probe helpers for visualizing segmentation output."""

from __future__ import annotations

from typing import Any, Dict


def summarize_object_meta(object_meta: Dict[str, Any]) -> str:
    """Create educational summary string for one object metadata item."""
    label = object_meta.get("label", "unknown")
    confidence = float(object_meta.get("confidence", 0.0))
    has_mask = bool(object_meta.get("has_mask", False))
    return f"label={label} confidence={confidence:.2f} mask={has_mask}"
