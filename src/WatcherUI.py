from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication,QWidget,QLabel,QPushButton,QVBoxLayout,QHBoxLayout
from PySide6.QtCore import Qt,Signal
from PySide6.QtGui import QResizeEvent
import sys
import os

class WatcherUI(QWidget):
    resizeSignal = Signal()
    def __init__(self) -> None:
        super().__init__()
        self.graphLabel = QLabel()
        self.currentPath = os.path.dirname(os.path.abspath(__file__))
        if os.name == 'posix':
            self.graphLabel.setPixmap(QPixmap(self.currentPath+'/../Resources/icons/icon.ico'))
        if os.name == 'nt':
            self.graphLabel.setPixmap(QPixmap('./Resources/icons/icon.ico')) # if you start via python the directory should be set as self.currentPath+'/../Resources/icons/icon.ico'
        self.noticeLabel = QLabel()
        self.noticeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.areaButton = QPushButton('Select Area')
        self.configButton = QPushButton('Setting')
        self.stateButtion = QPushButton('Start Watch')

        hlayout = QHBoxLayout(self)
        vlayout1 = QVBoxLayout(self)
        vlayout1.addWidget(self.graphLabel)
        vlayout1.addWidget(self.noticeLabel)

        vlayout2 = QVBoxLayout(self)
        vlayout2.addWidget(self.areaButton)
        vlayout2.addWidget(self.configButton)
        vlayout2.addWidget(self.stateButtion)
        vlayout2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        hlayout.addLayout(vlayout1)
        hlayout.addLayout(vlayout2)
        self.setLayout(hlayout)
    
    def resizeEvent(self, event: QResizeEvent) -> None:
        self.resizeSignal.emit()
        return super().resizeEvent(event)

