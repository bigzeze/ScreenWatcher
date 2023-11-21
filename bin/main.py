from ScreenWatcher import MainWindow
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

if __name__=='__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon('icon.ico'))
    win = MainWindow()
    # win.setWindowFlags(Qt.WindowStaysOnTopHint)
    win.show()
    app.exec_()