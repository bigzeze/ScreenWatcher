from Tray import Tray
from ScreenWatcherCore import ScreenWatcher
from Configure import Configure
from PySide6.QtWidgets import QApplication, QMainWindow, QDockWidget
from PySide6.QtCore import Qt,Signal
from PySide6.QtGui import QIcon,QPixmap,QCloseEvent
import uuid

import sys
from qt_material import apply_stylesheet

class MainWindow(QMainWindow):
    def __init__(self,*args,**kargs):
        super().__init__(*args,**kargs)
        self.setWindowTitle('Screen Watcher')
        self.icon = QIcon(QPixmap('icons/icon.ico'))
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.setMinimumWidth(300)
        
        self.menu = self.menuBar()
        self.addWidget = self.menu.addAction('Add Watcher')
        self.addWidget.triggered.connect(self.createDockWidget)

        self.startButton = self.menu.addAction('Start All')
        self.startButton.triggered.connect(self.startAll)
        
        self.stopButton = self.menu.addAction('Stop All')
        self.stopButton.triggered.connect(self.stopAll)

        self.dockWidgets = []

        self.config = Configure()
        self.loadSavedWidgets()

    def loadSavedWidgets(self):
        uids = self.config.config.sections()
        for uid in uids:
            self.loadDockWidget(uid)
        if not uids:
            self.createDockWidget()

    def createDockWidget(self):
        uid = uuid.uuid1().hex
        self.config.addUid(uid)
        newDockWidget = WatcherDock(self.config,uid)
        newDockWidget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, newDockWidget)
        self.dockWidgets.append(newDockWidget)
        self.dockWidgets[-1].resizeSignal.connect(self.adjustSize)
        newDockWidget.closeSignal.connect(self.delete_dockwidget)
        newDockWidget.screenWatcher.resizeSignal.connect(self.adjustSize)
        print(newDockWidget.uid,' created')
        
    def loadDockWidget(self,uid):
        newDockWidget = WatcherDock(self.config,uid)
        newDockWidget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, newDockWidget)
        self.dockWidgets.append(newDockWidget)
        self.dockWidgets[-1].resizeSignal.connect(self.adjustSize)
        newDockWidget.closeSignal.connect(self.delete_dockwidget)
        newDockWidget.screenWatcher.resizeSignal.connect(self.adjustSize)
        print(newDockWidget.uid,' created')

    
    def delete_dockwidget(self,uid):
        for idx,dockWidget in enumerate(self.dockWidgets):
            if dockWidget.uid == uid:
                break
        self.dockWidgets.remove(self.dockWidgets[idx])
        self.config.removeUid(uid)
        self.allAjustSize()
        print(uid,' deleted')
    # def exit_change(self,lst):  # 放到核心类里
    #     self.exittype = lst[0]
    #     if lst[1]:
    #         self.writeconfig('exit')

    def closeEvent(self, event):
        event.ignore()
        self.hide()
    
    def allAjustSize(self):
        for dockWidget in self.dockWidgets:
            dockWidget.screenWatcher.adjustSize()
            dockWidget.adjustSize()
        self.adjustSize()
    
    def startAll(self):
        for widget in self.dockWidgets:
            widget.screenWatcher.startWatch()
    
    def stopAll(self):
        for widget in self.dockWidgets:
            widget.screenWatcher.endWatch()

class WatcherDock(QDockWidget):
    closeSignal = Signal(str)
    resizeSignal = Signal()
    def __init__(self,config,uid):
        #self.name = 'New Watcher'
        super().__init__(uid)
        self.config = config
        self.uid = uid
        self.screenWatcher = ScreenWatcher(self.config,self.uid)
        self.screenWatcher.setOuterChangeSizeFunction(self.adjustSize)
        self.screenWatcher.setOuterRenameFunction(self.setWindowTitle)
        self.screenWatcher.resizeSignal.connect(self.swResize)
        self.screenWatcher.getConfig()
        self.setWidget(self.screenWatcher)

        
    def closeEvent(self, event: QCloseEvent) -> None:
        self.closeSignal.emit(self.uid)
        return super().closeEvent(event)
    
    def swResize(self):
        self.resizeSignal.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv) 
    apply_stylesheet(app,theme='light_cyan.xml')
    widget = MainWindow() 
    widget.show() 
    tray = Tray(app=app,window=widget)

    sys.exit(app.exec()) 