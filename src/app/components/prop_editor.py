from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFormLayout, QLabel, QWidget

from app.state import AppState


class PropEditor(QWidget):
    def __init__(self, state: AppState, parent=None):
        super().__init__(parent)
        self.app_state = state

        self._form = QFormLayout(self)
        self._form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

    def update_current_prop(self):
        # Remove existing rows
        while self._form.rowCount():
            self._form.removeRow(0)

        if not self.app_state.current_prop_edit:
            self._form.addRow(QLabel("Select a property from the left"))
            return
        else:
            self._form.addRow(QLabel(f"Name = {self.app_state.current_prop_edit.name}"))
            self._form.addRow(
                QLabel(
                    f"Value = {self.app_state.current_prop_edit.value} {self.app_state.current_prop_edit.unit}"
                )
            )
