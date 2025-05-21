from __future__ import annotations

from PySide6 import QtCore, QtGui, QtWidgets

from app.state import AppState


class ResultsView(QtWidgets.QWidget):
    def __init__(self, state: AppState, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._state = state

        layout = QtWidgets.QVBoxLayout(self)
        self.placeholder = QtWidgets.QLabel("Results plots – appear after run")
        self.placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.placeholder)
