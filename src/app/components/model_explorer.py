from functools import partial

from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import QPoint, Qt

from app.schemas.fmu import FmuInput, FmuOutput, FmuParameter
from app.schemas.metrics_spec import MetricSpec
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
        self.tree_view.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.ContiguousSelection
        )
        self.tree_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        self.description = QtWidgets.QLabel(DESCRIPTION_PLACEHOLDER, self)
        self.description.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

        self.desc_scroll = QtWidgets.QScrollArea(self)
        self.desc_scroll.setMinimumHeight(50)
        self.desc_scroll.setWidgetResizable(True)
        self.desc_scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.desc_scroll.setWidget(self.description)

        self._splitter = QtWidgets.QSplitter(Qt.Orientation.Vertical, self)
        self._splitter.addWidget(self.tree_view)
        self._splitter.addWidget(self.desc_scroll)
        self._splitter.setStretchFactor(0, 3)
        self._splitter.setChildrenCollapsible(False)

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setContentsMargins(5, 0, 5, 0)
        self._layout.addWidget(self.search_box)
        self._layout.addWidget(self._splitter)
        self.setLayout(self._layout)

        # Signal Wiring
        self.tree_view.itemSelectionChanged.connect(self._on_selection_changed)
        self.tree_view.customContextMenuRequested.connect(self._show_context_menu)
        self.search_box.textChanged.connect(self._filter_tree)

    # Callbacks

    def _show_context_menu(self, pos: QPoint) -> None:
        selected = self.tree_view.selectedItems()
        if not selected:
            return

        menu = QtWidgets.QMenu(self)

        menu.addAction("Add to Study", partial(self._change_selected, add=True))
        menu.addAction("Remove from Study", partial(self._change_selected, add=False))

        # Show the menu under the cursor
        global_pos = self.tree_view.viewport().mapToGlobal(pos)
        menu.exec(global_pos)

    def _change_selected(self, *, add: bool) -> None:
        for item in self.tree_view.selectedItems():
            obj = item.data(0, Qt.ItemDataRole.UserRole)
            if obj is None:
                continue

            if isinstance(obj, FmuParameter):
                if add:
                    self._state.parameters.setdefault(obj.name, obj)
                else:
                    self._state.parameters.pop(obj.name, None)

            elif isinstance(obj, FmuInput):
                if add:
                    self._state.inputs.setdefault(obj.name, obj)
                else:
                    self._state.inputs.pop(obj.name, None)

            elif isinstance(obj, FmuOutput):
                if add:
                    if all(m.signal.name != obj.name for m in self._state.metrics):
                        self._state.metrics.append(
                            MetricSpec(
                                signal=obj, statistic="max", lower=None, upper=None
                            )
                        )
                else:
                    self._state.metrics[:] = [
                        m for m in self._state.metrics if m.signal.name != obj.name
                    ]

            self._apply_icon(item, obj)

    def _apply_icon(self, item: QtWidgets.QTreeWidgetItem, obj) -> None:
        selected = (
            isinstance(obj, FmuParameter)
            and obj.name in self._state.parameters
            or isinstance(obj, FmuInput)
            and obj.name in self._state.inputs
            or isinstance(obj, FmuOutput)
            and any(m.signal.name == obj.name for m in self._state.metrics)
        )
        item.setIcon(
            0,
            QtGui.QIcon.fromTheme(QtGui.QIcon.ThemeIcon.EditFind)
            if selected
            else QtGui.QIcon(),
        )

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

        def _create_root(title: str) -> QtWidgets.QTreeWidgetItem:
            item = QtWidgets.QTreeWidgetItem(self.tree_view, [title])
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            return item

        param_root = _create_root("Parameters")
        input_root = _create_root("Inputs")
        output_root = _create_root("Outputs")

        def _create_child(
            root: QtWidgets.QTreeWidgetItem,
            name: str,
            var: FmuParameter | FmuInput | FmuOutput,
        ) -> QtWidgets.QTreeWidgetItem:
            item = QtWidgets.QTreeWidgetItem(root, [name])
            item.setData(0, Qt.ItemDataRole.UserRole, var)
            self._apply_icon(item, var)
            return item

        for name, var in self._state.fmu_variables.items():
            if isinstance(var, FmuParameter):
                _item = _create_child(param_root, name, var)
            elif isinstance(var, FmuInput):
                _item = _create_child(input_root, name, var)
            elif isinstance(var, FmuOutput):
                _item = _create_child(output_root, name, var)
            else:
                continue

    def update_description(self, v: FmuParameter | FmuInput | FmuOutput | None):
        if v is not None:
            self.description.setText(f"""
Name = {v.name}
Description = {v._raw.description}
Unit = {v._raw.unit}
Type = {v._raw.type}
Default = {v._raw.start}
            """)
        else:
            self.description.setText(DESCRIPTION_PLACEHOLDER)
