from PySide6 import QtWidgets

from app.state import AppState


class DOESetup(QtWidgets.QWidget):
    def __init__(self, state: AppState, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._state = state

        layout = QtWidgets.QFormLayout(self)
        self.method_combo = QtWidgets.QComboBox()
        self.method_combo.addItems(["Monte Carlo", "Latin Hypercube", "Full Factorial"])
        self.n_spin = QtWidgets.QSpinBox()
        self.n_spin.setRange(1, 10_000)
        self.n_spin.setValue(100)
        self.seed_spin = QtWidgets.QSpinBox()
        self.seed_spin.setRange(0, 1_000_000)
        layout.addRow("Method:", self.method_combo)
        layout.addRow("Number of samples:", self.n_spin)
        layout.addRow("Random seed:", self.seed_spin)
        # TODO: connect widgets to self._state.doe_settings
