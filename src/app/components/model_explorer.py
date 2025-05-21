from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from app.schemas.fmu import FmuInput, FmuOutput, FmuParameter
from app.state import AppState


class ModelExplorer(QtWidgets.QWidget):
    def __init__(self, state: AppState, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._state = state

        self.setMinimumWidth(200)

        self.search_box = QtWidgets.QLineEdit()
        self.search_box.setPlaceholderText("Filter")

        self.tree_view = QtWidgets.QTreeWidget()
        self.tree_view.setHeaderHidden(True)

        self.description = QtWidgets.QLabel()
        self.description.setFixedWidth(50)

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.addWidget(self.search_box)
        self._layout.addWidget(self.tree_view)
        self._layout.addWidget(self.description)
        self.setLayout(self._layout)

    def rebuild_tree(self):
        self.tree_view.clear()

        param_root = QtWidgets.QTreeWidgetItem(self.tree_view, ["Parameters"])
        input_root = QtWidgets.QTreeWidgetItem(self.tree_view, ["Inputs"])
        output_root = QtWidgets.QTreeWidgetItem(self.tree_view, ["Outputs"])

        for name, var in self._state.fmu_variables.items():
            if isinstance(var, FmuParameter):
                item = QtWidgets.QTreeWidgetItem(param_root, [name])
                item.setData(0, Qt.ItemDataRole.UserRole, var)
            elif isinstance(var, FmuInput):
                item = QtWidgets.QTreeWidgetItem(input_root, [name])
                item.setData(0, Qt.ItemDataRole.UserRole, var)
            elif isinstance(var, FmuOutput):
                item = QtWidgets.QTreeWidgetItem(output_root, [name])
                item.setData(0, Qt.ItemDataRole.UserRole, var)
