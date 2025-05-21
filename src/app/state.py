from pathlib import Path

from fmpy.util import fmu_info


class AppState:
    fmu_path = Path()

    def load_fmu(self, fmu_path: Path, return_info: bool = False) -> str | None:
        self.fmu_path = fmu_path

        if return_info:
            return fmu_info(str(fmu_path), ["input", "output", "parameter"])
