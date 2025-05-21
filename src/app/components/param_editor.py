from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from app.state import AppState


class ParamEditor(QtWidgets.QWidget):
    def __init__(self, state: AppState, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._state = state

        self._layout = QtWidgets.QHBoxLayout(self)

        self._left_box = QtWidgets.QGroupBox("Active Params")
        self._right_box = QtWidgets.QGroupBox("Params Editor")

        self.active_params = QtWidgets.QTreeWidget()
        self.active_params.setHeaderHidden(True)

        self._right_layout = QtWidgets.QHBoxLayout(self._left_box)
        self._right_layout.addWidget(self.active_params)

        self.form = QtWidgets.QFormLayout(self._right_box)
        self.name_edit = QtWidgets.QLineEdit()
        self.name_edit.setReadOnly(True)
        self.unit_edit = QtWidgets.QLineEdit()
        self.unit_edit.setReadOnly(True)
        self.value_edit = QtWidgets.QLineEdit()
        self.min_edit = QtWidgets.QLineEdit()
        self.min_edit.setPlaceholderText("min")
        self.max_edit = QtWidgets.QLineEdit()
        self.max_edit.setPlaceholderText("max")
        self.dist_combo = QtWidgets.QComboBox()
        self.dist_combo.addItems(["Uniform", "Normal"])

        self.form.addRow("Name:", self.name_edit)
        self.form.addRow("Unit:", self.unit_edit)
        self.form.addRow("Fixed value:", self.value_edit)
        self.form.addRow("Range:", self._hbox(self.min_edit, self.max_edit))
        self.form.addRow("Distribution:", self.dist_combo)

        self._splitter = QtWidgets.QSplitter(Qt.Orientation.Horizontal)
        self._splitter.addWidget(self._left_box)
        self._splitter.addWidget(self._right_box)
        self._splitter.setStretchFactor(3, 0)
        self._splitter.setSizes([100, 250])
        self._splitter.setChildrenCollapsible(False)

        self._layout.addWidget(self._splitter)

        self.setLayout(self._layout)

    @staticmethod
    def _hbox(*widgets: QtWidgets.QWidget) -> QtWidgets.QWidget:
        w = QtWidgets.QWidget()
        lay = QtWidgets.QHBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        for wid in widgets:
            lay.addWidget(wid)
        lay.addStretch(1)
        return w
