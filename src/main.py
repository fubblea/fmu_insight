import sys

from PySide6.QtWidgets import (
    QApplication,
)

from app.main_window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()

    window.setMinimumSize(800, 500)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
