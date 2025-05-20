from PySide6.QtWidgets import QMainWindow, QSplitter

from app.components.menu_bar import MenuBar
from app.components.prop_editor import PropEditor
from app.components.prop_tree import PropTree
from app.state import AppState


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FMU Insight")

        # Init app state
        self.app_state = AppState()

        # Create property editor
        self.prop_editor = PropEditor(state=self.app_state)

        # Create property tree
        self.prop_tree = PropTree(state=self.app_state)

        splitter = QSplitter()
        splitter.addWidget(self.prop_tree)
        splitter.addWidget(self.prop_editor)
        splitter.setStretchFactor(1, 1)  # give property panel more flex

        # Menu bar
        menu_bar = MenuBar(state=self.app_state)
        self.setMenuBar(menu_bar)

        # Set main widget
        self.setCentralWidget(splitter)
