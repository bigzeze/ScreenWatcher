from ScreenWatcherCore import SWCore
from SelectArea import SelectArea
from ConfigUI import ConfigUI
from PySide6.QtGui import QPixmap,QColor
from PySide6.QtWidgets import QApplication,QWidget,QDockWidget,QLabel,QPushButton,QVBoxLayout,QHBoxLayout
from PySide6.QtCore import Qt,Signal,Slot
from PySide6.QtGui import QCloseEvent,QResizeEvent
import sys

class WatcherDock(QDockWidget):
    closeSignal = Signal(int)
    def __init__(self,name,idx):
        super().__init__(name)
        self.idx = idx
        self.watcherui = WatcherUI()
        self.setWidget(self.watcherui)
        
    def closeEvent(self, event: QCloseEvent) -> None:
        self.closeSignal.emit(self.idx)
        return super().closeEvent(event)
    
    def setIndex(self,idx):
        self.idx =idx

class WatcherUI(SWCore):
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

    #在WatcherUI和SWCore里实现各种功能

    def areaButtonClicked(self):
        self.endWatch()
        self.selectArea = SelectArea()
        self.selectArea.show()
        self.selectArea._signal.connect(self.changeArea)

    def configButtonClicked(self):
        self.endWatch()
        self.configUI = ConfigUI(self)
        self.configUI.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.configUI.show()
        self.configUI._signal.connect(self.changeSetting)

    def stateBUttionClicked(self):
        if self.watchStatus == False:
            self.startWatch()
        else:
            self.endWatch()
    
    def resizeEvent(self, event: QResizeEvent) -> None:
        self.resizeSignal.emit()
        return super().resizeEvent(event)

    



if __name__ == "__main__":
    app = QApplication(sys.argv)  

    widget = WatcherDock('Watcher 1',0)
    widget.show()

    sys.exit(app.exec()) 