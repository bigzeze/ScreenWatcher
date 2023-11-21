from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QScreen




if __name__ == '__main__':
    app = QApplication([])
    screens = QApplication.screens()
    for screen in screens:
        print(screen.serialNumber())
    app.exec_()