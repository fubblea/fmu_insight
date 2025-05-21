from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from PySide6 import QtCore, QtGui, QtWidgets


@dataclass
class AppState:
    """Single source of truth for the application state."""

    fmu_path: Optional[Path] = None
    parameters: Dict[str, Any] = field(default_factory=dict)  # name → value / range
    inputs: Dict[str, Any] = field(default_factory=dict)  # name → signal data
    metrics: List[MetricSpec] = field(default_factory=list)
    doe_settings: Dict[str, Any] = field(default_factory=dict)  # method, N, seed, …
    results: Optional[Any] = None  # placeholder for results DataFrame / ndarray

    # Convenience helpers -----------------------------------------------------
    def has_study(self) -> bool:
        return bool(self.parameters) and bool(self.doe_settings)


# ────────────────────────────────────────────────────────────────────────────────
#  Placeholder widgets for tab contents
# ────────────────────────────────────────────────────────────────────────────────


class ParameterTable(QtWidgets.QWidget):
    def __init__(self, state: AppState, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._state = state

        layout = QtWidgets.QVBoxLayout(self)
        self.table = QtWidgets.QTableView()
        layout.addWidget(self.table)
        # TODO: bind table model to self._state.parameters


class InputSignals(QtWidgets.QWidget):
    def __init__(self, state: AppState, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._state = state

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel("Input signal editor – TODO"))


class DOESetup(QtWidgets.QWidget):
    def __init__(self, state: AppState, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._state = state

        layout = QtWidgets.QFormLayout(self)
        self.method_combo = QtWidgets.QComboBox()
        self.method_combo.addItems(["Monte Carlo", "Latin Hypercube", "Full Factorial"])
        self.n_spin = QtWidgets.QSpinBox()
        self.n_spin.setRange(1, 10_000)
        self.n_spin.setValue(100)
        self.seed_spin = QtWidgets.QSpinBox()
        self.seed_spin.setRange(0, 1_000_000)
        layout.addRow("Method:", self.method_combo)
        layout.addRow("Number of samples:", self.n_spin)
        layout.addRow("Random seed:", self.seed_spin)
        # TODO: connect widgets to self._state.doe_settings


class ResultsView(QtWidgets.QWidget):
    def __init__(self, state: AppState, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._state = state

        layout = QtWidgets.QVBoxLayout(self)
        self.placeholder = QtWidgets.QLabel("Results plots – appear after run")
        self.placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.placeholder)


@dataclass
class MetricSpec:
    """Specification of a result metric / constraint."""

    signal: str  # name of the output / expression
    statistic: str = "max"  # max, min, mean, …
    lower: Optional[float] = None
    upper: Optional[float] = None
    objective: Optional[str] = None  # optimise? minimise / maximise


class MetricsSetup(QtWidgets.QWidget):
    """Select inputs/outputs of interest and define metrics / constraints."""

    def __init__(self, state: AppState, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._state = state

        main = QtWidgets.QHBoxLayout(self)

        # Left – available signals list -------------------------------------------------
        left_box = QtWidgets.QGroupBox("Available outputs / signals")
        left_layout = QtWidgets.QVBoxLayout(left_box)
        self.signal_list = QtWidgets.QListWidget()
        left_layout.addWidget(self.signal_list)
        # TODO: populate this list from FMU after load

        # Right – metric table ----------------------------------------------------------
        right_box = QtWidgets.QGroupBox("Metrics & constraints")
        right_layout = QtWidgets.QVBoxLayout(right_box)

        self.metric_table = QtWidgets.QTableWidget(0, 5)
        self.metric_table.setHorizontalHeaderLabels(
            [
                "Signal",
                "Statistic",
                "Lower bound",
                "Upper bound",
                "Objective",
            ]
        )
        self.metric_table.verticalHeader().setVisible(False)
        self.metric_table.horizontalHeader().setStretchLastSection(True)
        right_layout.addWidget(self.metric_table)

        btn_row = QtWidgets.QHBoxLayout()
        self.btn_add = QtWidgets.QPushButton("Add ⧉ from selection")
        self.btn_remove = QtWidgets.QPushButton("Remove selected")
        btn_row.addWidget(self.btn_add)
        btn_row.addWidget(self.btn_remove)
        btn_row.addStretch(1)
        right_layout.addLayout(btn_row)
        # TODO: wire buttons to modify self.metric_table & self._state.metrics

        main.addWidget(left_box, 2)
        main.addWidget(right_box, 3)


# ────────────────────────────────────────────────────────────────────────────────
#  Dock: Property editor
# ────────────────────────────────────────────────────────────────────────────────


class PropertyEditor(QtWidgets.QWidget):
    def __init__(self, state: AppState, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._state = state

        self.form = QtWidgets.QFormLayout(self)
        self.name_edit = QtWidgets.QLineEdit()
        self.name_edit.setReadOnly(True)
        self.unit_edit = QtWidgets.QLineEdit()
        self.unit_edit.setReadOnly(True)
        self.value_edit = QtWidgets.QLineEdit()
        self.min_edit = QtWidgets.QLineEdit()
        self.min_edit.setPlaceholderText("min")
        self.max_edit = QtWidgets.QLineEdit()
        self.max_edit.setPlaceholderText("max")
        self.dist_combo = QtWidgets.QComboBox()
        self.dist_combo.addItems(["Uniform", "Normal"])

        self.form.addRow("Name:", self.name_edit)
        self.form.addRow("Unit:", self.unit_edit)
        self.form.addRow("Fixed value:", self.value_edit)
        self.form.addRow("Range:", self._hbox(self.min_edit, self.max_edit))
        self.form.addRow("Distribution:", self.dist_combo)
        # TODO: populate/commit edits according to selection in model explorer

    @staticmethod
    def _hbox(*widgets: QtWidgets.QWidget) -> QtWidgets.QWidget:
        w = QtWidgets.QWidget()
        lay = QtWidgets.QHBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        for wid in widgets:
            lay.addWidget(wid)
        lay.addStretch(1)
        return w


# ────────────────────────────────────────────────────────────────────────────────
#  Main window
# ────────────────────────────────────────────────────────────────────────────────


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
        act_stop = QtGui.QAction(QtGui.QIcon.fromTheme("process-stop"), "Stop", self)
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
        self.input_tab = InputSignals(self.state)
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
        self.statusBar().showMessage("Ready")

    # ─────────────────────────────────────────────── Slots / placeholders ──

    @QtCore.Slot()
    def load_fmu(self) -> None:  # noqa: D401 – Qt‑slot naming convention
        """Open & parse an FMU (placeholder)."""
        # TODO: implement open‑file dialog + state update
        self.log("Load FMU – not implemented yet")

    @QtCore.Slot()
    def run_study(self) -> None:  # noqa: D401
        """Kick off the DOE run (placeholder)."""
        # TODO: spawn worker processes, update progress, enable results tab
        self.log("Run Study – not implemented yet")

    @QtCore.Slot()
    def stop_study(self) -> None:  # noqa: D401
        """Abort a running study (placeholder)."""
        self.log("Stop Study – not implemented yet")

    # ─────────────────────────────────────────────────────────── Helpers ──

    def log(self, msg: str) -> None:
        self.log_edit.append(msg)
