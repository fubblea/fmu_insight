from pathlib import Path

from fmpy import read_model_description
from fmpy.util import fmu_info, get_start_values


class Property:
    def __init__(self, name: str, value: float) -> None:
        self.name = name
        self.value = value


class AppState:
    fmu_path = Path()

    param_inclusions: list[Property] = []
    output_inclusions: list[Property] = []

    param_available: list[Property] = []
    output_available: list[Property] = []

    def __init__(self, parent=None) -> None:
        self.parent = parent

    def load_fmu(self, fmu_path: Path, return_info: bool = False) -> str | None:
        self.fmu_path = fmu_path

        # Get variables
        start_values = get_start_values(str(fmu_path))
        model_vars = read_model_description(str(fmu_path))

        for v in model_vars.modelVariables:
            if v.causality == "output":
                self.output_available.append(Property(name=v.name, value=0))
            elif v.causality == "parameter":
                self.param_available.append(
                    Property(name=v.name, value=start_values[v.name])
                )

        if return_info:
            return fmu_info(str(fmu_path), ["input", "output", "parameter"])
