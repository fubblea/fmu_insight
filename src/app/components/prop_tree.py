from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem

from app.state import AppState, FmuProperty


class PropTree(QTreeWidget):
    request_current_edit_prop_change = Signal()

    def __init__(self, state: AppState, parent=None):
        super().__init__(parent)
        self.app_state = state

        self.setHeaderHidden(True)
        self.setMinimumWidth(200)

        self.recreate_tree()

        # Signal Wiring
        self.itemSelectionChanged.connect(self._on_selection_changed)

    def _on_selection_changed(self) -> None:
        items = self.selectedItems()
        props: FmuProperty | None = (
            items[0].data(0, Qt.ItemDataRole.UserRole) if items else None
        )
        self.app_state.current_prop_edit = props
        self.request_current_edit_prop_change.emit()

    def recreate_tree(self):
        self.clear()

        inclusions_root = QTreeWidgetItem(self, ["Inclusions"])
        available_root = QTreeWidgetItem(self, ["Available"])

        params_include_root = QTreeWidgetItem(inclusions_root, ["Parameters"])
        for include in self.app_state.param_inclusions:
            item = QTreeWidgetItem(params_include_root, [include.name])
            item.setData(0, Qt.ItemDataRole.UserRole, include)

        outputs_include_root = QTreeWidgetItem(inclusions_root, ["Outputs"])
        for include in self.app_state.output_inclusions:
            item = QTreeWidgetItem(outputs_include_root, [include.name])
            item.setData(0, Qt.ItemDataRole.UserRole, include)

        params_avail_root = QTreeWidgetItem(available_root, ["Parameters"])
        for include in self.app_state.param_available:
            item = QTreeWidgetItem(params_avail_root, [include.name])
            item.setData(0, Qt.ItemDataRole.UserRole, include)

        outputs_avail_root = QTreeWidgetItem(available_root, ["Outputs"])
        for include in self.app_state.output_available:
            item = QTreeWidgetItem(outputs_avail_root, [include.name])
            item.setData(0, Qt.ItemDataRole.UserRole, include)
