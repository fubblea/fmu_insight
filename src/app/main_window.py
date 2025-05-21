from pathlib import Path

from PySide6 import QtCore, QtGui, QtWidgets

from app.components.doe_setup import DOESetup
from app.components.input_editor import InputEditor
from app.components.metrics_setup import MetricsSetup
from app.components.model_explorer import ModelExplorer
from app.components.param_editor import ParamEditor
from app.components.result_view import ResultsView
from app.state import AppState


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, state: AppState):
        super().__init__()
        self.state = state
        self.setWindowTitle("FMU Insight")
        self.setMinimumSize(1200, 800)

        self._build_menu()
        self._build_toolbar()
        self._build_docks()
        self._build_central_tabs()
        self._build_status_bar()

    # ─────────────────────────────────────────────────────────────────── Menu ──

    def _build_menu(self) -> None:
        mbar = self.menuBar()
        file_menu = mbar.addMenu("&File")
        act_open = QtGui.QAction("Open FMU…", self)
        act_open.triggered.connect(self.load_fmu)
        act_save = QtGui.QAction("Save Study…", self)
        act_quit = QtGui.QAction("Quit", self)
        act_quit.triggered.connect(QtWidgets.QApplication.quit)
        file_menu.addActions([act_open, act_save])
        file_menu.addSeparator()
        file_menu.addAction(act_quit)

    # ─────────────────────────────────────────────────────────────── Toolbar ──

    def _build_toolbar(self) -> None:
        tbar = self.addToolBar("Toolbar")
        tbar.setMovable(False)

        act_open = QtGui.QAction(QtGui.QIcon.fromTheme("document-open"), "Open", self)
        act_open.triggered.connect(self.load_fmu)
        act_run = QtGui.QAction(
            QtGui.QIcon.fromTheme("media-playback-start"), "Run Study", self
        )
        act_run.triggered.connect(self.run_study)
        act_stop = QtGui.QAction(
            QtGui.QIcon.fromTheme(QtGui.QIcon.ThemeIcon.MediaPlaybackStop), "Stop", self
        )
        act_stop.triggered.connect(self.stop_study)

        tbar.addActions([act_open, act_run, act_stop])

    # ─────────────────────────────────────────────────────────────── Docks ──

    def _build_docks(self) -> None:
        # Model explorer dock (left)
        self.model_explorer = ModelExplorer(self.state)
        explorer_dock = QtWidgets.QDockWidget("Model Explorer", self)
        explorer_dock.setWidget(self.model_explorer)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, explorer_dock)

        # Log dock (bottom)
        self.log_edit = QtWidgets.QTextEdit()
        self.log_edit.setReadOnly(True)
        log_dock = QtWidgets.QDockWidget("Log", self)
        log_dock.setWidget(self.log_edit)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.BottomDockWidgetArea, log_dock)
        log_dock.hide()

    # ───────────────────────────────────────────────────────────── Central ──

    def _build_central_tabs(self) -> None:
        tabs = QtWidgets.QTabWidget()
        tabs.setMinimumWidth(500)
        self.setCentralWidget(tabs)

        self.param_editor = ParamEditor(self.state)
        self.input_tab = InputEditor(self.state)
        self.metrics_tab = MetricsSetup(self.state)
        self.doe_tab = DOESetup(self.state)
        self.results_tab = ResultsView(self.state)

        tabs.addTab(self.param_editor, "Parameter Editor")
        tabs.addTab(self.input_tab, "Input Signals")
        tabs.addTab(self.metrics_tab, "Metrics Setup")
        tabs.addTab(self.doe_tab, "DOE Setup")
        tabs.addTab(self.results_tab, "Results")

        # Disable Results until a run is completed
        tabs.setTabEnabled(tabs.indexOf(self.results_tab), False)
        self._tabs = tabs

    # ────────────────────────────────────────────────────────── Status bar ──

    def _build_status_bar(self) -> None:
        self.progress = QtWidgets.QProgressBar(maximum=100)
        self.statusBar().addPermanentWidget(self.progress)
        self.statusBar().showMessage("Ready", timeout=10000)

    # ────────────────────────────────────────────────────────── Callbacks ──

    def load_fmu(self) -> None:
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            caption="Select FMU file",
            dir="",
            filter="FMU files (*.fmu)",
        )

        if file_path:
            info = self.state.load_fmu(Path(file_path), return_info=True)
            assert info is not None, "Could not load FMU"

            self.update_status("Loaded FMU")
            self.log("-------------------------------------")
            self.log(info)
            self.log("-------------------------------------")

            self.model_explorer.rebuild_tree()
            self.log("Rebuilt model_explorer tree")

    def run_study(self) -> None:
        # TODO: spawn worker processes, update progress, enable results tab
        self.log("Run Study - not implemented yet")

    def stop_study(self) -> None:
        # TODO: Stop
        self.log("Stop Study - not implemented yet")

    # ─────────────────────────────────────────────────────────── Helpers ──

    def update_status(self, msg: str):
        self.statusBar().showMessage(msg, timeout=10000)

    def log(self, msg: str) -> None:
        self.log_edit.append(msg)
