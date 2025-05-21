from __future__ import annotations

from PySide6 import QtCore, QtGui, QtWidgets

from app.components.doe_setup import DOESetup
from app.components.input_editor import InputEditor
from app.components.metrics_setup import MetricsSetup
from app.components.param_table import ParameterTable
from app.components.prop_editor import PropertyEditor
from app.components.result_view import ResultsView
from app.state import AppState


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, state: AppState):
        super().__init__()
        self.state = state
        self.setWindowTitle("FMU Study")
        self.resize(1200, 800)

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
        tbar = self.addToolBar("Main")
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
        self.model_explorer = QtWidgets.QTreeView()
        self.model_explorer.setHeaderHidden(True)
        explorer_dock = QtWidgets.QDockWidget("Model Explorer", self)
        explorer_dock.setWidget(self.model_explorer)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, explorer_dock)

        # Property editor dock (right)
        prop_widget = PropertyEditor(self.state)
        prop_dock = QtWidgets.QDockWidget("Properties", self)
        prop_dock.setWidget(prop_widget)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, prop_dock)

        # Log dock (bottom)
        self.log_edit = QtWidgets.QTextEdit()
        self.log_edit.setReadOnly(True)
        log_dock = QtWidgets.QDockWidget("Log", self)
        log_dock.setWidget(self.log_edit)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.BottomDockWidgetArea, log_dock)

    # ───────────────────────────────────────────────────────────── Central ──

    def _build_central_tabs(self) -> None:
        tabs = QtWidgets.QTabWidget()
        self.setCentralWidget(tabs)

        self.param_tab = ParameterTable(self.state)
        self.input_tab = InputEditor(self.state)
        self.metrics_tab = MetricsSetup(self.state)
        self.doe_tab = DOESetup(self.state)
        self.results_tab = ResultsView(self.state)

        tabs.addTab(self.param_tab, "Parameter Table")
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

    # ─────────────────────────────────────────────── Slots / placeholders ──

    def load_fmu(self) -> None:
        """Open & parse an FMU (placeholder)."""
        # TODO: implement open‑file dialog + state update
        self.log("Load FMU – not implemented yet")

    def run_study(self) -> None:
        """Kick off the DOE run (placeholder)."""
        # TODO: spawn worker processes, update progress, enable results tab
        self.log("Run Study – not implemented yet")

    def stop_study(self) -> None:
        """Abort a running study (placeholder)."""
        self.log("Stop Study – not implemented yet")

    # ─────────────────────────────────────────────────────────── Helpers ──

    def log(self, msg: str) -> None:
        self.log_edit.append(msg)
