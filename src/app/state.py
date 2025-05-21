from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from fmpy import read_model_description
from fmpy.util import fmu_info

from app.schemas.fmu import FmuInput, FmuOutput, FmuParameter
from app.schemas.metrics_spec import MetricSpec


@dataclass
class AppState:
    """Single source of truth for the application state."""

    fmu_path: Optional[Path] = None
    fmu_variables: Dict[str, FmuParameter | FmuInput | FmuOutput] = field(
        default_factory=dict
    )

    parameters: Dict[str, FmuParameter] = field(default_factory=dict)
    inputs: Dict[str, FmuInput] = field(default_factory=dict)
    metrics: List[MetricSpec] = field(default_factory=list)
    doe_settings: Dict[str, Any] = field(default_factory=dict)

    results: Optional[Any] = None

    def has_study(self) -> bool:
        return bool(self.parameters) and bool(self.doe_settings)

    def load_fmu(self, fmu_path: Path, return_info: bool = False) -> str | None:
        self.fmu_path = fmu_path

        # Get variables
        model_vars = read_model_description(str(fmu_path))

        for v in model_vars.modelVariables:
            if v.causality == "output":
                self.fmu_variables[v.name] = FmuOutput.from_scalar_variable(v)
            elif v.causality == "parameter":
                self.fmu_variables[v.name] = FmuParameter.from_scalar_variable(v)
            elif v.causality == "input":
                self.fmu_variables[v.name] = FmuInput.from_scalar_variable(v)

        if return_info:
            return fmu_info(str(fmu_path), ["input", "output", "parameter"])
