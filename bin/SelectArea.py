from PySide6.QtWidgets import QApplication,QWidget
from PySide6.QtGui import QBitmap,QPainter,QPen,QBrush
from PySide6.QtCore import Qt,Signal,QPoint,QRect,QSize
import sys


class WScreenShot(QWidget):
    _signal=Signal(list)
    def __init__(self, screen, parent=None):
        super(WScreenShot, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet('''background-color:black; ''')
        self.setWindowOpacity(0.6)
        self.detectscreen = screen
        #screens = QApplication.screens()
        self.geometry = self.detectscreen.geometry()
        #desktopRect = QDesktopWidget().screenGeometry()
        self.setGeometry(self.geometry)
        self.setCursor(Qt.CrossCursor)
        self.blackMask = QBitmap(self.detectscreen.size())
        self.blackMask.fill(Qt.black)
        self.mask = self.blackMask.copy()
        self.isDrawing = False
        self.startPoint = QPoint()
        self.endPoint = QPoint()

    def paintEvent(self, event):
        if self.isDrawing:
            self.mask = self.blackMask.copy()
            pp = QPainter(self.mask)
            pen = QPen()
            pen.setStyle(Qt.NoPen)
            pp.setPen(pen)
            brush = QBrush(Qt.white)
            pp.setBrush(brush)
            pp.drawRect(QRect(self.startPoint, self.endPoint))
            self.setMask(QBitmap(self.mask))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPoint = event.pos()
            self.endPoint = self.startPoint
            self.isDrawing = True

    def mouseMoveEvent(self, event):
        if self.isDrawing:
            self.endPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.endPoint = event.pos()
            self.close()
            ratio = self.detectscreen.devicePixelRatio()
            print(self.startPoint,self.endPoint)
            self.startPoint,self.endPoint = QPoint(min(self.startPoint.x(),self.endPoint.x())*ratio,min(self.startPoint.y(),self.endPoint.y())*ratio),\
                                            QPoint(max(self.startPoint.x(),self.endPoint.x())*ratio,max(self.startPoint.y(),self.endPoint.y())*ratio)
            print(self.startPoint,self.endPoint)
            self._signal.emit([self.detectscreen,QRect(self.startPoint,self.endPoint)])

class SelectArea(QWidget):
    _signal = Signal(list)
    def __init__(self) -> None:
        super(SelectArea,self).__init__()
        self.detectscreens = QApplication.screens()
        self.windows = [WScreenShot(screen) for screen in self.detectscreens]
    
    def show(self):
        for window in self.windows:
            window.show()
            window._signal.connect(self.get_signal)
    
    def get_signal(self,lst):
        detscreen = lst[0]
        index = None
        for idx,screen in enumerate(self.detectscreens):
            if screen==detscreen:
                index = idx
                break

        for window in self.windows:
            window.close()
        #print(lst)
        self._signal.emit([index,lst[1]])

    
if __name__ == '__main__':
    app = QApplication([])
    win = SelectArea()
    # win.setWindowFlags(Qt.WindowStaysOnTopHint)

    win.show()
    app.exec_()
