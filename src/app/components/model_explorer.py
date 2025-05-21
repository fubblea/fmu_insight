from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from app.schemas.fmu import FmuInput, FmuOutput, FmuParameter
from app.state import AppState

DESCRIPTION_PLACEHOLDER = "Select a property to view more details"


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
        self.description.setText(DESCRIPTION_PLACEHOLDER)

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.addWidget(self.search_box)
        self._layout.addWidget(self.tree_view)
        self._layout.addWidget(self.description)
        self.setLayout(self._layout)

        # Signal Wiring
        self.tree_view.itemSelectionChanged.connect(self._on_selection_changed)
        self.search_box.textChanged.connect(self._filter_tree)

    # Callbacks

    def _on_selection_changed(self):
        items = self.tree_view.selectedItems()
        v: FmuParameter | FmuInput | FmuOutput | None = (
            items[0].data(0, Qt.ItemDataRole.UserRole) if items else None
        )
        self.update_description(v)

    def _filter_tree(self, text: str):
        text = text.lower().strip()

        for i in range(self.tree_view.topLevelItemCount()):
            category = self.tree_view.topLevelItem(i)
            if category is None:
                continue

            any_child_visible = False

            for j in range(category.childCount()):
                child = category.child(j)
                match = text in child.text(0).lower() if text else True
                child.setHidden(not match)
                any_child_visible |= match

            category.setHidden(not any_child_visible)

    # Public Helpers

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

    def update_description(self, v: FmuParameter | FmuInput | FmuOutput | None):
        if v is not None:
            self.description.setText(f"""
Name = {v.name}
Description = {v._raw.description}
Unit = {v.unit}
Type = {v.type}
Default = {v._raw.start}
            """)
        else:
            self.description.setText(DESCRIPTION_PLACEHOLDER)
