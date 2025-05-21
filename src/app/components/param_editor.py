from PySide6 import QtWidgets

from app.state import AppState


class ParamEditor(QtWidgets.QWidget):
    def __init__(self, state: AppState, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._state = state

        self.form = QtWidgets.QFormLayout(self)
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
        # TODO: populate/commit edits according to selection in model explorer

    @staticmethod
    def _hbox(*widgets: QtWidgets.QWidget) -> QtWidgets.QWidget:
        w = QtWidgets.QWidget()
        lay = QtWidgets.QHBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        for wid in widgets:
            lay.addWidget(wid)
        lay.addStretch(1)
        return w
