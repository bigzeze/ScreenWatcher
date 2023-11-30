from Tray import Tray
from ScreenWatcher import ScreenWatcher
from PySide6.QtWidgets import QApplication, QMainWindow, QDockWidget
from PySide6.QtCore import Qt,Signal
from PySide6.QtGui import QIcon,QPixmap,QCloseEvent

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
        self.addwidget = self.menu.addAction('Add Watcher')
        self.addwidget.triggered.connect(self.create_dockwidget)
        self.dockwidgets = []
        self.create_dockwidget()

    def create_dockwidget(self):
        idx = len(self.dockwidgets)
        dockWidget = WatcherDock('Watcher '+str(idx+1),idx)
        dockWidget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dockWidget)
        self.dockwidgets.append(dockWidget)
        dockWidget.closeSignal.connect(self.delete_dockwidget)
        dockWidget.screenwatcher.resizeSignal.connect(self.adjustSize)
    
    def delete_dockwidget(self,index):
        print(index)
        self.dockwidgets.remove(self.dockwidgets[index])
        for idx,wighet  in enumerate(self.dockwidgets):
            wighet.setWindowTitle('Watcher '+str(idx+1))
            wighet.setIndex(idx)

    # def exit_change(self,lst):  # 放到核心类里
    #     self.exittype = lst[0]
    #     if lst[1]:
    #         self.writeconfig('exit')

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        

class WatcherDock(QDockWidget):
    closeSignal = Signal(int)
    def __init__(self,name,idx):
        super().__init__(name)
        self.idx = idx
        self.screenwatcher = ScreenWatcher(self.idx)
        self.setWidget(self.screenwatcher)
        
    def closeEvent(self, event: QCloseEvent) -> None:
        self.closeSignal.emit(self.idx)
        return super().closeEvent(event)
    
    def setIndex(self,idx):
        self.idx =idx
        self.screenwatcher.setIndex(idx)


if __name__ == "__main__":
    app = QApplication(sys.argv) 
    apply_stylesheet(app,theme='light_cyan.xml')
    widget = MainWindow() 
    widget.show() 
    tray = Tray(app=app,window=widget)

    sys.exit(app.exec()) 
        


    