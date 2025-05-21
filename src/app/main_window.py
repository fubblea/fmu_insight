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
        self.prop_editor.update_current_prop()

        # Create property tree
        self.prop_tree = PropTree(
            state=self.app_state,
        )

        main_splitter = QSplitter()
        main_splitter.addWidget(self.prop_tree)
        main_splitter.addWidget(self.prop_editor)
        main_splitter.setStretchFactor(1, 1)  # give property panel more flex

        # Menu bar
        self.menu_bar = MenuBar(state=self.app_state, parent=self)
        self.setMenuBar(self.menu_bar)

        # Set main widget
        self.setCentralWidget(main_splitter)

        # Signal wiring
        self.menu_bar.request_tree_rebuild.connect(self.prop_tree.recreate_tree)
        self.prop_tree.request_current_edit_prop_change.connect(
            self.prop_editor.update_current_prop
        )
