import sys
from PyQt6.QtWidgets import QApplication
from ui.window import FolderCreator


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = FolderCreator()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
