"""Simple FPS counter helper for source statistics."""

from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class FPSCounter:
    """Maintain lightweight running FPS statistics."""

    frame_count: int = 0
    start_time: float = field(default_factory=time.perf_counter)

    def tick(self) -> None:
        """Register one processed frame."""
        self.frame_count += 1

    def value(self) -> float:
        """Compute average FPS since start."""
        elapsed = max(time.perf_counter() - self.start_time, 1e-9)
        return self.frame_count / elapsed
