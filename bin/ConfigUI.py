from PySide6.QtWidgets import QApplication,QWidget,QGroupBox,QLabel,QPushButton,QVBoxLayout,QHBoxLayout,QFileDialog,QMessageBox,QSpinBox,QLineEdit
from PySide6.QtCore import Qt,Signal
from PySide6.QtGui import QIcon,QPixmap
import resources
import sys

class ConfigUI(QWidget):
    _signal = Signal(list)
    def __init__(self,args):
        super(ConfigUI,self).__init__()
        self.args = args
        self.name = args[0]
        self.templetePath = args[1]
        self.audioPath = args[2]
        self.interval = args[3]


        self.setWindowTitle('Setting')
        self.icon = QIcon(QPixmap('icons/configure.ico'))
        self.setWindowIcon(self.icon)
        self.setMinimumWidth(600)

        self.nameLabel = QLabel("<center><font size='4'>set watcher name:</font></center>")
        self.nameLineEdit = QLineEdit(self.name)
        layout0 = QHBoxLayout()
        layout0.addWidget(self.nameLabel)
        layout0.addWidget(self.nameLineEdit)
        self.nameGroup = QGroupBox()
        self.nameGroup.setLayout(layout0)
        self.nameGroup.setTitle('Watcher Nmae')

        self.templeteLineEdit = QLineEdit(self.templetePath)
        self.templeteButton = QPushButton('select templetes')
        self.templeteButton.setFixedWidth(200)
        layout1 = QHBoxLayout()
        layout1.addWidget(self.templeteLineEdit)
        layout1.addWidget(self.templeteButton)
        self.templeteGroup = QGroupBox()
        self.templeteGroup.setLayout(layout1)
        self.templeteGroup.setTitle('Templete Path')

        self.audioLineEdit = QLineEdit(self.audioPath)
        self.audioButton = QPushButton('select audio')
        self.audioButton.setFixedWidth(200)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.audioLineEdit)
        layout2.addWidget(self.audioButton)
        self.audioGroup = QGroupBox()
        self.audioGroup.setLayout(layout2)
        self.audioGroup.setTitle('Audio Path')

        self.intervalLabel = QLabel("<center><font size='4'>set detect interval:</font></center>")
        self.intervalSpin = QSpinBox()
        self.intervalSpin.setMinimum(500)
        self.intervalSpin.setMaximum(50000)
        self.intervalSpin.setSingleStep(500)
        self.intervalSpin.setProperty("value", args[3])
        self.intervalSpin.setFixedWidth(200)
        layout3 = QHBoxLayout()
        layout3.addWidget(self.intervalLabel)
        layout3.addWidget(self.intervalSpin)
        self.intervalGroup = QGroupBox()
        self.intervalGroup.setLayout(layout3)
        self.intervalGroup.setTitle('Interval')

        self.submitButton = QPushButton('ok')

        layout = QVBoxLayout()
        layout.addWidget(self.nameGroup)
        layout.addWidget(self.templeteGroup)
        layout.addWidget(self.audioGroup)
        layout.addWidget(self.intervalGroup)
        layout.addWidget(self.submitButton)
        self.setLayout(layout)

        self.templeteButton.clicked.connect(self.templeteButtonClick)
        self.audioButton.clicked.connect(self.audioButtonClick)
        self.submitButton.clicked.connect(self.submitButtonClick)
    
    def templeteButtonClick(self):
        self.templetePath = QFileDialog.getExistingDirectory(self,'Select Path','./')
        self.templeteLineEdit.setText(self.templetePath)
        self.adjustSize()

    def audioButtonClick(self):
        self.audioPath = QFileDialog.getOpenFileName(self,'Select File','./','All Files (*);;MP3 Files (*.mp3)')[0]
        self.audioLineEdit.setText(self.audioPath)
        self.adjustSize()
    
    def submitButtonClick(self):
        if self.audioPath=='' or self.templetePath=='':
            QMessageBox.warning(self,'Warning','Both templetes and audio paths should be designated',QMessageBox.StandardButton.Ok)
        else:
            self._signal.emit([self.nameLineEdit.text(),self.templetePath,self.audioPath,self.intervalSpin.text()])
            self.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)  

    widget = ConfigUI()
    widget.show()

    sys.exit(app.exec()) 