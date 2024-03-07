
from WatcherUI import WatcherUI
from SelectArea import SelectArea
#from Configure import Configure
from ConfigUI import ConfigUI
from ImageTools import *
from PySide6.QtWidgets import QApplication,QMessageBox
from PySide6.QtCore import Qt,QTimer
import cv2
import numpy as np
import os
import playsound
import logging
import time
import sys

class ScreenWatcher(WatcherUI):
    def __init__(self) -> None:
        super(ScreenWatcher,self).__init__()
        
        self.watchStatus = False
        self.matched = False
        
        #self.readconfig()

        self.timer = QTimer()
        self.timer.timeout.connect(self.screenDetect)
        self.templetes = []
        self.detectRect = None
        self.qtpixmap = None
        self.cvimg = None
        logging.basicConfig(level=logging.INFO,filename='log.txt',filemode='a')

        #self.loadConfig()
        #self.changeSetting([self.templetePath,self.audioPath,self.interval])
        #self.changeArea()

    def setOuterChangeSizeFunction(self,func):
        self.outerChangeSizeFunc = func
    
    def outerChangeSize(self):
        self.outerChangeSizeFunc()

    def startWatch(self):
        if self.detectRect == None:
            QMessageBox.warning(self, 'Warning', 'Detecting area not asgined.')
            return
        if self.templetes == []:  
            QMessageBox.warning(self, 'Warning', 'Templete path not asgined.')
            return
        if self.audioPath == '':
            QMessageBox.warning(self,'Warning','Audio path not asgined.')
            return 
        
        self.watchStatus = True
        self.timer.start()
        self.stateButtion.setText('End Watch')
        logging.info(time.strftime('%y/%m/%d %H:%M:%S' + ' Start watching.'))
    
    def endWatch(self):
        if self.watchStatus == True:
            self.watchStatus = False
            self.timer.stop()
            self.stateButtion.setText('Start Watch')
            self.noticeLabel.setText('')
            logging.info(time.strftime('%y/%m/%d %H:%M:%S') + ' End watching.')

    def screenDetect(self):
        self.screenShoot() 
        matched = self.templeteMatch()  
        self.showImage()
        if matched:
            self.matchedTrigger()
        else:
            self.unmathcedTrigger()

    def showImage(self):
        self.qtpixmap = cvimg_to_qtpixmap(self.cvimg)
        self.graphLabel.setPixmap(self.qtpixmap)
        self.adjustSize()


    def templeteMatch(self):  
        tag = False
        for templete in self.templetes:
            w,h =np.shape(templete)[:-1]
            res = cv2.matchTemplate(self.cvimg, templete, cv2.TM_CCORR_NORMED)
            threshold = 0.99
            loc = np.where( res >= threshold)
            for pt in zip(*loc[::-1]):
                cv2.rectangle(self.cvimg, pt, (pt[0] + w, pt[1] + h), (255,255,255), 2)
                tag = True
            #cv2.imwrite('res.png',self.cvimg)
            #self.endWatch()
            #break
        return tag

    def matchedTrigger(self):
        if self.matched == False:
            self.matched = True
            self.notice()
            logging.info(time.strftime('%y/%m/%d %H:%M:%S') + ' Temlete matched.')
        self.noticeLabel.setText('<font color=red>Templete Matched ' + time.strftime('%H:%M:%S')+'</font>')

    def unmathcedTrigger(self):
        if self.matched == True:
            self.matched = False
            logging.info(time.strftime('%y/%m/%d %H:%M:%S') + ' Temlete disappeared.')
        self.noticeLabel.setText('<font color=green>Watching ' + time.strftime('%H:%M:%S')+'</font>')

    def notice(self):
        playsound.playsound(self.audioPath)

    def changeSetting(self,lst):
        (self.templetePath,self.audioPath) = lst[:-1]
        self.loadImages()
        self.interval = eval(lst[-1])
        self.timer.setInterval(self.interval)
    
    def changeArea(self,lst):
        (self.screenIndex,self.detectRect) = lst
        self.screenShoot()
        self.graphLabel.setPixmap(self.qtpixmap)
        self.adjustSize()
        self.outerChangeSizeFunc()

    def loadImages(self):
        self.templetes.clear()
        filenames = os.listdir(self.templetePath)
        for filename in filenames:
            self.templetes.append(cv2.imread(self.templetePath + '/' +filename, 1))

    def screenShoot(self):
        screenshot = QApplication.screens()[self.screenIndex].grabWindow(0)
        self.qtpixmap = screenshot.copy(self.detectRect)
        self.cvimg = qtpixmap_to_cvimg(self.qtpixmap)

    def areaButtonClicked(self):
        self.endWatch()
        self.selectArea = SelectArea()
        self.selectArea.show()
        self.selectArea._signal.connect(self.changeArea)

    def configButtonClicked(self):
        self.endWatch()
        self.configUI = ConfigUI([self.templetePath,self.audioPath,self.interval])
        self.configUI.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.configUI.show()
        self.configUI._signal.connect(self.changeSetting)

    def stateBUttionClicked(self):
        if self.watchStatus == False:
            self.startWatch()
        else:
            self.endWatch()


if __name__ == "__main__":
    app = QApplication(sys.argv)  

    widget = ScreenWatcher()
    widget.show()

    sys.exit(app.exec()) 