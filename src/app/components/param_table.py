from __future__ import annotations

from PySide6 import QtWidgets

from app.state import AppState


class ParameterTable(QtWidgets.QWidget):
    def __init__(self, state: AppState, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._state = state

        layout = QtWidgets.QVBoxLayout(self)
        self.table = QtWidgets.QTableView()
        layout.addWidget(self.table)
        # TODO: bind table model to self._state.parameters
