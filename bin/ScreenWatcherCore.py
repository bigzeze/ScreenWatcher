
from WatcherUI import WatcherUI
from SelectArea import SelectArea
#from Configure import Configure
from ConfigUI import ConfigUI
from ImageTools import *
from PySide6.QtWidgets import QApplication,QMessageBox
from PySide6.QtCore import Qt,QTimer,Signal,QRect,QPoint
import cv2
import numpy as np
import os
import pygame
import logging
import time
import sys

class ScreenWatcher(WatcherUI):
    resizeSignal = Signal()
    def __init__(self,config,uid) -> None:
        super(ScreenWatcher,self).__init__()
        self.areaButton.clicked.connect(self.areaButtonClicked)
        self.configButton.clicked.connect(self.configButtonClicked)
        self.stateButtion.clicked.connect(self.stateBUttionClicked)

        pygame.init()

        self.config = config
        self.uid = uid
        self.watchStatus = False
        self.matched = False
        
        #self.readconfig()

        self.timer = QTimer()
        self.timer.timeout.connect(self.screenDetect)
        self.templetes = []
        self.detectRect = None
        self.qtpixmap = None
        self.cvimg = None
        logging.basicConfig(level=logging.INFO,filename='log.txt',filemode='a',encoding='utf-8')

        #self.loadConfig()
        #self.changeSetting([self.templetePath,self.audioPath,self.interval])
        #self.changeArea()

        self.templetePath = None
        self.audioPath = None
        self.screenIndex = None
        self.detectRect = None
        self.interval = None

        self.name = self.uid
    
    def getConfig(self):
        configure = self.config.config
        try:
            self.name = configure[self.uid]['name']
            self.outerRename()
        except:
            configure[self.uid]['name'] = self.uid
            self.config.save()
            self.name = self.uid
            print(self.uid,' does not have saved name')
        try:
            self.templetePath = configure[self.uid]['templetePath']
            self.loadImages()
        except:
            print(self.uid,' does not have saved imagepath')
        try:
            self.audioPath = configure[self.uid]['audioPath']
            self.loadSound()
        except:
            print(self.uid,' does not have saved audiopath')
        try:
            self.screenIndex = eval(configure[self.uid]['screenIndex'])
            startx = eval(configure[self.uid]['startx'])
            starty = eval(configure[self.uid]['starty'])
            endx = eval(configure[self.uid]['endx'])
            endy = eval(configure[self.uid]['endy'])
            self.detectRect = QRect(QPoint(startx,starty),QPoint(endx,endy))
            self.screenShoot()
            self.graphLabel.setPixmap(self.qtpixmap)
            self.myresize()
            self.outerChangeSize()
        except:
            print(self.uid,' does not have saved capture positon')
        try:
            self.interval = eval(configure[self.uid]['interval'])
            self.timer.setInterval(self.interval)
        except:
            print(self.uid,' does not have saved interval')


    def setOuterChangeSizeFunction(self,func):
        self.outerChangeSizeFunc = func
    
    def outerChangeSize(self):
        self.outerChangeSizeFunc()
    
    def setOuterRenameFunction(self,func):
        self.outerRenameFunc = func

    def outerRename(self):
        self.outerRenameFunc(self.name)

    def startWatch(self):
        if self.screenIndex == None:
            QMessageBox.warning(self, 'Warning', 'Detecting screen not asgined.')
            return
        if self.detectRect == None:
            QMessageBox.warning(self, 'Warning', 'Detecting area not asgined.')
            return
        if self.templetes == []:  
            QMessageBox.warning(self, 'Warning', 'Templete path not asgined.')
            return
        if self.audioPath == '' or None:
            QMessageBox.warning(self,'Warning','Audio path not asgined.')
            return 
        if self.interval == None:
            QMessageBox.warning(self,'Warning','interval not asgined.')
            return 
        
        self.watchStatus = True
        self.timer.start()
        self.stateButtion.setText('End Watch')
        logging.info(time.strftime('%y/%m/%d %H:%M:%S ' + self.name +' Start watching.'))
    
    def endWatch(self):
        if self.watchStatus == True:
            self.watchStatus = False
            self.timer.stop()
            self.stateButtion.setText('Start Watch')
            self.noticeLabel.setText('')
            logging.info(time.strftime('%y/%m/%d %H:%M:%S ') + self.name + ' End watching.')

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
        self.myresize()


    def templeteMatch(self):  
        tag = False
        for templete in self.templetes:
            w,h =np.shape(templete)[:-1]
            res = cv2.matchTemplate(self.cvimg, templete, cv2.TM_CCORR_NORMED)
            threshold = 0.99
            loc = np.where( res >= threshold)
            for pt in zip(*loc[::-1]):
                cv2.rectangle(self.cvimg, pt, (pt[0] + h, pt[1] + w), (20,50,155), 2)
                tag = True
            #cv2.imwrite('res.png',self.cvimg)
            #self.endWatch()
            #break
        return tag

    def matchedTrigger(self):
        if self.matched == False:
            self.matched = True
            self.notice()
            logging.info(time.strftime('%y/%m/%d %H:%M:%S ') + self.name + ' Temlete matched.')
        self.noticeLabel.setText('<font color=red>Templete Matched ' + time.strftime('%H:%M:%S') + '</font>')

    def unmathcedTrigger(self):
        if self.matched == True:
            self.matched = False
            logging.info(time.strftime('%y/%m/%d %H:%M:%S ') + self.name + ' Temlete disappeared.')
        self.noticeLabel.setText('<font color=green>Watching ' + time.strftime('%H:%M:%S') + '</font>')

    def notice(self):
        self.sound.play()

    def changeSetting(self,lst):
        (self.name,self.templetePath,self.audioPath) = lst[:-1]
        self.outerRename()
        self.loadImages()
        self.loadSound()
        self.interval = eval(lst[-1])
        self.timer.setInterval(self.interval)
        config = self.config.config
        config[self.uid]['name'] = self.name
        config[self.uid]['templetePath'] = self.templetePath
        config[self.uid]['audioPath'] = self.audioPath
        config[self.uid]['interval'] = str(self.interval)
        self.config.save()
    
    def changeArea(self,lst):
        (self.screenIndex,self.detectRect) = lst
        self.screenShoot()
        self.graphLabel.setPixmap(self.qtpixmap)
        self.myresize()
        self.outerChangeSize()
        config = self.config.config
        config[self.uid]['screenIndex'] = str(self.screenIndex)
        config[self.uid]['startx'] = str(self.detectRect.topLeft().x())
        config[self.uid]['starty'] = str(self.detectRect.topLeft().y())
        config[self.uid]['endx'] = str(self.detectRect.bottomRight().x())
        config[self.uid]['endy'] = str(self.detectRect.bottomRight().y())
        self.config.save()

    def loadImages(self):
        self.templetes.clear()
        filenames = os.listdir(self.templetePath)
        for filename in filenames:
            self.templetes.append(cv2.imread(self.templetePath + '/' +filename, 1))
    
    def loadSound(self):
        self.sound = pygame.mixer.Sound(self.audioPath)

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
        self.configUI = ConfigUI([self.name,self.templetePath,self.audioPath,self.interval])
        self.configUI.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.configUI.show()
        self.configUI._signal.connect(self.changeSetting)

    def stateBUttionClicked(self):
        if self.watchStatus == False:
            self.startWatch()
        else:
            self.endWatch()
    
    def myresize(self):
        self.adjustSize()
        self.resizeSignal.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)  

    widget = ScreenWatcher()
    widget.show()

    sys.exit(app.exec()) 