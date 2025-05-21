from pathlib import Path

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog, QMenuBar

from app.state import AppState


class MenuBar(QMenuBar):
    def __init__(self, state: AppState, parent=None):
        super().__init__(parent)
        self.state = state  # keep a reference

        self.setFixedHeight(32)

        # ─── File menu ─────────────────────────────────────────────────────────
        file_menu = self.addMenu("&File")

        load_fmu_action = QAction("Load FMU…", self)
        load_fmu_action.setShortcut("Ctrl+O")
        load_fmu_action.triggered.connect(self._on_load_fmu)
        file_menu.addAction(load_fmu_action)

    # ──────────────────────────────────────────────────────────────────────────
    def _on_load_fmu(self) -> None:
        """Open a dialog, let the user choose an FMU file, and store the path."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            caption="Select FMU file",
            dir="",
            filter="FMU files (*.fmu)",
        )
        if file_path:
            self.state.load_fmu(Path(file_path))
