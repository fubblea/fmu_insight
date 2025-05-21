from pathlib import Path

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
        start_values = get_start_values(fmu_path)

        key: str
        value: str
        for key, value in start_values.items():
            if not key.__contains__("outputAlias"):
                new_item = Property(name=key, value=float(value))
                self.output_available.append(new_item)

        if return_info:
            return fmu_info(str(fmu_path), ["input", "output", "parameter"])
