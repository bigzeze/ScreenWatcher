from PySide6.QtWidgets import QApplication,QWidget,QMessageBox
from PySide6.QtCore import QTimer
from PySide6.QtGui import qRed,qBlue,qGreen,QPixmap
import cv2
import numpy as np
import os
import playsound
import logging
import time

class SWCore(QWidget):
    def __init__(self) -> None:
        super(SWCore,self).__init__()
        self.watchStatus = False
        self.templetePath = r'D:\EVE-Localalert\resources\image\newui'
        self.templetes = []
        self.audioPath = r'D:\EVE-Localalert\resources\audio\alarm_audio.mp3'

        self.screenIndex = None
        self.detectRect = None

        self.qtpixmap = None
        self.cvimg = None

        self.interval = '2000'
        self.timer = QTimer()
        self.timer.timeout.connect(self.screenDetect)
        logging.basicConfig(level=logging.INFO,filename='log.txt',filemode='a')

        self.detected = False

        #self.loadConfig()
        self.changeSetting([self.templetePath,self.audioPath,self.interval])
        #self.changeArea()

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
        logging.info('start watching')
    
    def endWatch(self):
        self.watchStatus = False
        self.timer.stop()
        self.stateButtion.setText('Start Watch')
        logging.info('end watching')

    def screenDetect(self):
        self.noticeLabel.setText('Watching ' + time.strftime('%H:%M:%S'))
        self.screenShoot() 
        detected = self.templeteMatch()  
        #self.PrintImage()  # 显示图片
        #if exist_enemy and not self.matched:
        #    self.alarm()
        #if not exist_enemy and self.matched:
        #    self.alarmstop()
    
    def templeteMatch(self):  
        for templete in self.templetes:
            w,h =np.shape(templete)[:-1]
            res = cv2.matchTemplate(self.cvimg, templete, cv2.TM_CCORR_NORMED)
            threshold = 0.9
            loc = np.where( res >= threshold)
            for pt in zip(*loc[::-1]):
                cv2.rectangle(self.cvimg, pt, (pt[0] + w, pt[1] + h), (255,255,255), 2)
            cv2.imwrite('res.png',self.cvimg)
            self.endWatch()
            break
        #return status_judge

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

    def loadImages(self):
        self.templetes.clear()
        filenames = os.listdir(self.templetePath)
        for filename in filenames:
            self.templetes.append(cv2.imread(self.templetePath + '/' +filename, 1))

    def screenShoot(self):
        screenshot = QApplication.screens()[self.screenIndex].grabWindow(0)
        self.qtpixmap = screenshot.copy(self.detectRect)
        self.cvimg = self.qtpixmap_to_cvimg(self.qtpixmap)

    def qtpixmap_to_cvimg(self,pixmap:QPixmap):
        qimg = pixmap.toImage()
        tmp = qimg
        cv_image = np.zeros((tmp.height(), tmp.width(), 3), dtype=np.uint8)
        for row in range(0, tmp.height()):
            for col in range(0,tmp.width()):
                r = qRed(tmp.pixel(col, row))
                g = qGreen(tmp.pixel(col, row))
                b = qBlue(tmp.pixel(col, row))
                cv_image[row,col,0] = b
                cv_image[row,col,1] = g
                cv_image[row,col,2] = r
        return cv_image