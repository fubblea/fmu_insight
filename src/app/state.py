from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.schemas.metrics_spec import MetricSpec


@dataclass
class AppState:
    """Single source of truth for the application state."""

    fmu_path: Optional[Path] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    inputs: Dict[str, Any] = field(default_factory=dict)
    metrics: List[MetricSpec] = field(default_factory=list)
    doe_settings: Dict[str, Any] = field(default_factory=dict)
    results: Optional[Any] = None

    def has_study(self) -> bool:
        return bool(self.parameters) and bool(self.doe_settings)
