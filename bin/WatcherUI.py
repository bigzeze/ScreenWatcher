from ScreenWatcherCore import SWCore
import PySide6.QtGui
from PySide6.QtWidgets import QApplication,QWidget,QDockWidget,QLabel,QPushButton,QVBoxLayout,QHBoxLayout
from PySide6.QtCore import Qt,Signal,Slot
from PySide6.QtGui import QCloseEvent
import sys

class WatcherDock(QDockWidget):
    _signal = Signal(int)
    def __init__(self,name,idx):
        super().__init__(name)
        self.idx = idx
        self.watcherui = WatcherUI()
        self.setWidget(self.watcherui)
        
    def closeEvent(self, event: QCloseEvent) -> None:
        self._signal.emit(self.idx)
        return super().closeEvent(event)
    
    def setIndex(self,idx):
        self.idx =idx

class WatcherUI(QWidget,SWCore):
    
    def __init__(self) -> None:
        super().__init__()
        self.graphLabel = QLabel('graph label')
        self.noticeLabel = QLabel('notice label')
        self.noticeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.configButton = QPushButton('Setting')
        self.stateButtion = QPushButton('Start Watch')

        self.configButton.clicked.connect(self.configButtonClicked)
        self.stateButtion.clicked.connect(self.stateBUttionClicked)

        hview = QHBoxLayout(self)
        hview.addWidget(self.graphLabel)

        vview = QVBoxLayout(self)
        vview.addWidget(self.noticeLabel)
        vview.addWidget(self.configButton)
        vview.addWidget(self.stateButtion)
        vview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        hview.addLayout(vview)

        self.setLayout(hview)

    #在WatcherUI和SWCore里实现各种功能

    def configButtonClicked(self):
        pass

    def stateBUttionClicked(self):
        pass

    



if __name__ == "__main__":
    app = QApplication(sys.argv)  

    widget = WatcherDock('Watcher 1',0)
    widget.show()

    sys.exit(app.exec()) 