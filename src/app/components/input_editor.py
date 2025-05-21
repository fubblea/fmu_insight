from __future__ import annotations

from PySide6 import QtWidgets

from app.state import AppState


class InputEditor(QtWidgets.QWidget):
    def __init__(self, state: AppState, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._state = state

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel("Input signal editor – TODO"))
