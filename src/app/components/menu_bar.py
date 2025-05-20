from PySide6.QtWidgets import QMenuBar

from app.state import AppState


class MenuBar(QMenuBar):
    def __init__(self, state: AppState):
        super().__init__()

        self.setFixedHeight(32)

        self.addMenu("&File")
