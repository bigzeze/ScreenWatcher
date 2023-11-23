from Tray import Tray
from Configure import Configure
from FunctionalWindows import ExitChoose
import PySide6.QtCore
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QDockWidget, QSystemTrayIcon, QTabWidget, QWidget, QVBoxLayout, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon,QPixmap,QAction

import sys
from qt_material import apply_stylesheet

class MainWindow(QMainWindow,Configure):
    def __init__(self,*args,**kargs):
        super().__init__(*args,**kargs)
        self.setWindowTitle('Screen Watcher')
        self.icon = QIcon(QPixmap('icon.ico'))
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        
        self.dockwidgets = []
        self.create_dockwidget('1')

    def create_dockwidget(self,name):
        dockWidget = QDockWidget(name, self)
        dockWidget.setAllowedAreas(Qt.TopDockWidgetArea |
                                    Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, dockWidget)
        self.dockwidgets.append(dockWidget)
    
    def closeEvent(self, event):
        if self.exittype==None:
            chooseWindow = ExitChoose()
            chooseWindow.show()
            chooseWindow._signal.connect(self.exit_change)
        if self.exittype==0:
            self.close()
        else:
            event.ignore()
            self.hide()
    
    def exit_change(self,lst):  # 放到核心类里
        self.exittype = lst[0]
        if lst[1]:
            self.writeconfig('exit')
        


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建APP，将运行脚本时（可能的）的其他参数传给Qt以初始化
    apply_stylesheet(app,theme='light_cyan.xml')
    widget = MainWindow()  # 实例化一个MyWidget类对象
    widget.show()  # 显示窗口
    tray = Tray(app=app,window=widget)

    sys.exit(app.exec()) 
        


    