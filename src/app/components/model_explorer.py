from PySide6 import QtWidgets

from app.state import AppState


class ModelExplorer(QtWidgets.QWidget):
    def __init__(self, state: AppState, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._state = state

        self.setMinimumWidth(200)

        self.search_box = QtWidgets.QLineEdit()
        self.search_box.setPlaceholderText("Filter")

        self.tree_view = QtWidgets.QTreeView()
        self.tree_view.setHeaderHidden(True)

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.addWidget(self.search_box)
        self._layout.addWidget(self.tree_view)
        self.setLayout(self._layout)
