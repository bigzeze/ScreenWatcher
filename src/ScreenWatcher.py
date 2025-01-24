from Tray import Tray
from ScreenWatcherCore import ScreenWatcher
from Configure import Configure
from PySide6.QtWidgets import QApplication, QMainWindow, QDockWidget
from PySide6.QtCore import Qt, Signal, QUrl
from PySide6.QtGui import QIcon, QPixmap, QCloseEvent, QDesktopServices
import uuid
import os
import sys
from qt_material import apply_stylesheet

class MainWindow(QMainWindow):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.currentPath = os.path.dirname(os.path.abspath(__file__))
        self.setWindowTitle('Screen Watcher')
        self.icon = QIcon(QPixmap(self.currentPath+'/../Resources/icons/icon.ico'))
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.setMinimumWidth(300)
        
        self.set_menu()

        self.dockWidgets = []
        self.config = Configure()
        self.loadSavedWidgets()

    def set_menu(self):
        if os.name == 'nt':
            self.menu = self.menuBar()
        elif os.name == 'posix':
            self.menubar = self.menuBar()
            self.menu = self.menubar.addMenu('Watchers')
        self.addWidget = self.menu.addAction('Add Watcher')
        self.addWidget.triggered.connect(self.createDockWidget)

        self.startButton = self.menu.addAction('Start All')
        self.startButton.triggered.connect(self.startAll)
        
        self.stopButton = self.menu.addAction('Stop All')
        self.stopButton.triggered.connect(self.stopAll)

        
        if os.name == 'nt':
            self.logButton = self.menu.addAction('Show Log')
            self.logButton.triggered.connect(self.showConfig)
        else:
            self.logmenu = self.menubar.addMenu('Log')
            self.logButton = self.logmenu.addAction('Show Log')
            self.logButton.triggered.connect(self.showConfig)

    def showConfig(self):
        self.logfile = self.currentPath + ('/../log.txt')
        print(self.logfile)
        try:
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.logfile))
        except:
            pass
    def loadSavedWidgets(self):
        uids = self.config.config.sections()
        for idx, uid in enumerate(uids):
            self.loadDockWidget(uid, idx)
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
        #print(newDockWidget.uid,' created')

    def loadDockWidget(self, uid, idx=0):
        newDockWidget = WatcherDock(self.config, uid)
        newDockWidget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        if idx == 0:
            self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, newDockWidget)
        else:
            self.tabifyDockWidget(self.dockWidgets[idx - 1], newDockWidget)
        self.dockWidgets.append(newDockWidget)
        self.dockWidgets[-1].resizeSignal.connect(self.adjustSize)
        newDockWidget.closeSignal.connect(self.delete_dockwidget)
        newDockWidget.screenWatcher.resizeSignal.connect(self.adjustSize)
        #print(newDockWidget.uid,' created')

    
    def delete_dockwidget(self,uid):
        for idx,dockWidget in enumerate(self.dockWidgets):
            if dockWidget.uid == uid:
                break
        self.dockWidgets.remove(self.dockWidgets[idx])
        self.config.removeUid(uid)
        self.allAjustSize()
        #print(uid,' deleted')
    # def exit_change(self,lst):  # 放到核心类里
    #     self.exittype = lst[0]
    #     if lst[1]:
    #         self.writeconfig('exit')

    def closeEvent(self, event):
        if os.name == 'nt':
            event.ignore()
            self.hide()
        else:
            return super().closeEvent(event)
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
    apply_stylesheet(app, theme='light_cyan.xml')
    widget = MainWindow() 
    widget.show() 
    if os.name == 'nt':
        tray = Tray(app=app, window=widget)
    sys.exit(app.exec())