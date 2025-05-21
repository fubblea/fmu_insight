from pathlib import Path

from fmpy import read_model_description
from fmpy.util import fmu_info, get_start_values


class FmuProperty:
    def __init__(
        self,
        name: str,
        unit: str,
        type: str,
        description: str | None = None,
        value: float | None = None,
    ) -> None:
        self.name = name
        self.unit = unit
        self.type = type
        self.description = description
        self.value = value


class AppState:
    fmu_path = Path()

    param_inclusions: list[FmuProperty] = []
    output_inclusions: list[FmuProperty] = []

    param_available: list[FmuProperty] = []
    output_available: list[FmuProperty] = []

    current_prop_edit: FmuProperty | None = None

    def __init__(self, parent=None) -> None:
        self.parent = parent

    def load_fmu(self, fmu_path: Path, return_info: bool = False) -> str | None:
        self.fmu_path = fmu_path

        # Get variables
        start_values = get_start_values(str(fmu_path))
        model_vars = read_model_description(str(fmu_path))

        for v in model_vars.modelVariables:
            if v.causality == "output":
                self.output_available.append(
                    FmuProperty(name=v.name, unit=v.unit, type=v.type)
                )
            elif v.causality == "parameter":
                self.param_available.append(
                    FmuProperty(
                        name=v.name,
                        unit=v.unit,
                        type=v.type,
                        value=start_values[v.name],
                    )
                )

        if return_info:
            return fmu_info(str(fmu_path), ["input", "output", "parameter"])
