from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from app.schemas.fmu import FmuOutput


@dataclass
class MetricSpec:
    signal: FmuOutput
    statistic: str = "max"
    lower: Optional[float] = None
    upper: Optional[float] = None
    objective: Optional[str] = None
