from PySide6.QtWidgets import QTreeWidget

from app.state import AppState


class PropTree(QTreeWidget):
    def __init__(self, state: AppState):
        super().__init__()

        self.setHeaderLabel("Properties")
        self.setMinimumWidth(200)
