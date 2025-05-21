from PySide6.QtWidgets import QWidget

from app.state import AppState


class PropEditor(QWidget):
    def __init__(self, state: AppState, parent=None):
        super().__init__(parent)
