from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication,QWidget,QLabel,QPushButton,QVBoxLayout,QHBoxLayout
from PySide6.QtCore import Qt,Signal
from PySide6.QtGui import QResizeEvent
import sys

class WatcherUI(QWidget):
    resizeSignal = Signal()
    def __init__(self) -> None:
        super().__init__()
        self.graphLabel = QLabel()
        self.graphLabel.setPixmap(QPixmap('icon.ico'))
        self.noticeLabel = QLabel()
        self.noticeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.areaButton = QPushButton('Select Area')
        self.configButton = QPushButton('Setting')
        self.stateButtion = QPushButton('Start Watch')

        self.areaButton.clicked.connect(self.areaButtonClicked)
        self.configButton.clicked.connect(self.configButtonClicked)
        self.stateButtion.clicked.connect(self.stateBUttionClicked)

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

