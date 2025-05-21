import sys

from PySide6 import QtWidgets

from app.main_window import AppState, MainWindow


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("FMU Insight")

    state = AppState()
    window = MainWindow(state)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
