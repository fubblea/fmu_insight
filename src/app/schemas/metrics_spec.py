from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class MetricSpec:
    """Specification of a result metric / constraint."""

    signal: str
    statistic: str = "max"
    lower: Optional[float] = None
    upper: Optional[float] = None
    objective: Optional[str] = None
