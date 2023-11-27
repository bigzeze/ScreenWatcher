from PySide6.QtWidgets import QApplication,QWidget,QGroupBox,QLabel,QPushButton,QVBoxLayout,QHBoxLayout,QFileDialog,QMessageBox,QSpinBox
from PySide6.QtCore import Qt,Signal
from PySide6.QtGui import QIcon,QPixmap
import sys

class ConfigUI(QWidget):
    _signal = Signal(list)
    def __init__(self,parent):
        super(ConfigUI,self).__init__()
        self.parnt = parent
        self.templetePath = parent.templetePath
        self.audioPath = parent.audioPath

        self.setWindowTitle('Setting')
        self.icon = QIcon(QPixmap('icon.ico'))
        self.setMinimumWidth(600)
        self.templeteLabel = QLabel(self.templetePath)
        self.templeteButton = QPushButton('select templetes')
        self.templeteButton.setFixedWidth(200)
        layout1 = QHBoxLayout()
        layout1.addWidget(self.templeteLabel)
        layout1.addWidget(self.templeteButton)
        self.templeteGroup = QGroupBox()
        self.templeteGroup.setLayout(layout1)

        self.audioLabel = QLabel(self.audioPath)
        self.audioButton = QPushButton('select audio')
        self.audioButton.setFixedWidth(200)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.audioLabel)
        layout2.addWidget(self.audioButton)
        self.audioGroup = QGroupBox()
        self.audioGroup.setLayout(layout2)

        self.intervalLabel = QLabel('Set time interval:')
        self.intervalSpin = QSpinBox()
        self.intervalSpin.setMinimum(500)
        self.intervalSpin.setMaximum(50000)
        self.intervalSpin.setSingleStep(500)
        self.intervalSpin.setProperty("value", parent.interval)
        self.intervalSpin.setFixedWidth(200)
        layout3 = QHBoxLayout()
        layout3.addWidget(self.intervalLabel)
        layout3.addWidget(self.intervalSpin)
        self.intervalGroup = QGroupBox()
        self.intervalGroup.setLayout(layout3)

        self.submitButton = QPushButton('ok')

        layout = QVBoxLayout()
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
        self.templeteLabel.setText(self.templetePath)
        self.adjustSize()

    def audioButtonClick(self):
        self.audioPath = QFileDialog.getOpenFileName(self,'Select File','./','All Files (*);;MP3 Files (*.mp3)')[0]
        self.audioLabel.setText(self.audioPath)
        self.adjustSize()
    
    def submitButtonClick(self):
        if self.audioPath=='' or self.templetePath=='':
            QMessageBox.warning(self,'Warning','Both templetes and audio paths should be designated',QMessageBox.StandardButton.Ok)
        else:
            self._signal.emit([self.templetePath,self.audioPath[0],self.intervalSpin.text()])
            self.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)  

    widget = ConfigUI()
    widget.show()

    sys.exit(app.exec()) 