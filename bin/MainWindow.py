from Tray import Tray
from ScreenWatcher import ScreenWatcher
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
        self.icon = QIcon(QPixmap('icon.ico'))
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.setMinimumWidth(300)
        
        self.menu = self.menuBar()
        self.addWidget = self.menu.addAction('Add Watcher')
        self.addWidget.triggered.connect(self.createDockWidget)
        self.dockWidgets = []
        self.createDockWidget()
    


    def createDockWidget(self):
        uid = uuid.uuid1().hex
        newDockWidget = WatcherDock(uid)
        newDockWidget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, newDockWidget)
        self.dockWidgets.append(newDockWidget)
        newDockWidget.closeSignal.connect(self.delete_dockwidget)
        newDockWidget.screenWatcher.resizeSignal.connect(self.adjustSize)
        print(newDockWidget.uid,' created')
    
    def delete_dockwidget(self,uid):
        for idx,dockWidget in enumerate(self.dockWidgets):
            if dockWidget.uid == uid:
                break
        self.dockWidgets.remove(self.dockWidgets[idx])
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
        

class WatcherDock(QDockWidget):
    closeSignal = Signal(str)
    def __init__(self,uid):
        #self.name = 'New Watcher'
        super().__init__()
        self.uid = uid
        self.screenWatcher = ScreenWatcher()
        self.screenWatcher.setUid(self.uid)
        self.screenWatcher.setOuterChangeSizeFunction(self.adjustSize)
        self.setWidget(self.screenWatcher)
        
    def closeEvent(self, event: QCloseEvent) -> None:
        self.closeSignal.emit(self.uid)
        return super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv) 
    apply_stylesheet(app,theme='light_cyan.xml')
    widget = MainWindow() 
    widget.show() 
    tray = Tray(app=app,window=widget)

    sys.exit(app.exec()) 
        


    