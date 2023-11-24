from typing import Optional
import PySide6.QtCore
from PySide6.QtWidgets import QApplication,QWidget,QLabel,QPushButton,QCheckBox,QHBoxLayout,QVBoxLayout
from PySide6.QtCore import Qt,Signal


# class ExitChoose(QWidget):
#     _signal = Signal(list)
#     def __init__(self):
#         super(ExitChoose,self).__init__()
#         self.setWindowTitle("Notice")
#         self.resize(300,100)
#         self.setWindowModality(Qt.WindowModality.WindowModal)
#         self.label = QLabel("Pressing close button means:")
#         self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.butt_exit = QPushButton('Exit')
#         self.butt_tray = QPushButton('To Taskbar')
#         self.checkbox = QCheckBox("remember me")
#         hlayout1 = QHBoxLayout()
#         hlayout1.addWidget(self.butt_exit)
#         hlayout1.addWidget(self.butt_tray)
#         hlayout2 = QHBoxLayout()
#         hlayout2.addWidget(self.checkbox)
#         hlayout2.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         vlayout = QVBoxLayout()
#         vlayout.addWidget(self.label)
#         vlayout.addLayout(hlayout1)
#         vlayout.addLayout(hlayout2)
#         self.setLayout(vlayout)
    
#         self.butt_exit.clicked.connect(self.choose)
#         self.butt_tray.clicked.connect(self.choose)
#     def choose(self):
#         state = 0 if self.checkbox.checkState else 1
#         if self.sender() == self.butt_exit:
#             self._signal.emit([0,state])
#         else:
#             self._signal.emit([1,state])
#         self.close()
        
if __name__ == '__main__':
    app = QApplication([])
    win = ExitChoose()
    # win.setWindowFlags(Qt.WindowStaysOnTopHint)
    win.show()
    app.exec_()
