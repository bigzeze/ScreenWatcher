from PySide6.QtWidgets import QWidget,QMenu,QSystemTrayIcon
from PySide6.QtGui import QIcon,QPixmap,QAction
import resources

class Tray(QWidget):
    def __init__(self, app, window):
        super(Tray,self).__init__()
        self.__app = app
        self.__window = window
        self.icon = QIcon(QPixmap('icons/icon.ico'))

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.create_tray_menu()
        self.tray.show()


    def create_tray_menu(self):
        showAction = QAction("&Show", self)
        showAction.triggered.connect(self.show_ui)
        quitAction = QAction("&Quit", self)
        quitAction.triggered.connect(self.quit_ui)
        self.trayMenu = QMenu(self)
        self.trayMenu.addAction(showAction)
        self.trayMenu.addSeparator()
        self.trayMenu.addAction(quitAction)
        self.tray.setContextMenu(self.trayMenu)
        self.tray.activated.connect(self.treat_activate)
    
    def show_ui(self):
        self.__window.show()
    def quit_ui(self):
        self.__app.exit()
    def treat_activate(self,act):
        if act == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_ui()