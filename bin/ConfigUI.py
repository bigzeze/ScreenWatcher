from PySide6.QtWidgets import QApplication,QWidget,QGroupBox,QLabel,QPushButton,QVBoxLayout,QHBoxLayout,QFileDialog
import sys

class ConfigUI(QWidget):
    def __init__(self):
        super(ConfigUI,self).__init__()
        self.resize(400,100)
        self.templeteLabel = QLabel('template path')
        self.templeteButton = QPushButton('select templetes')
        layout1 = QHBoxLayout()
        layout1.addWidget(self.templeteLabel)
        layout1.addWidget(self.templeteButton)
        self.templeteGroup = QGroupBox()
        self.templeteGroup.setLayout(layout1)

        self.audioLabel = QLabel('audio path')
        self.audioButton = QPushButton('select audio')
        layout2 = QHBoxLayout()
        layout2.addWidget(self.audioLabel)
        layout2.addWidget(self.audioButton)
        self.audioGroup = QGroupBox()
        self.audioGroup.setLayout(layout2)

        self.submitButton = QPushButton('ok')

        layout = QVBoxLayout()
        layout.addWidget(self.templeteGroup)
        layout.addWidget(self.audioGroup)
        layout.addWidget(self.submitButton)
        self.setLayout(layout)
    
    def templeteButtonClick(self):
        pass

    def 

if __name__ == "__main__":
    app = QApplication(sys.argv)  

    widget = ConfigUI()
    widget.show()

    sys.exit(app.exec()) 