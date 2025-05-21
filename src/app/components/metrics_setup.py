from __future__ import annotations

from PySide6 import QtWidgets

from app.state import AppState


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
