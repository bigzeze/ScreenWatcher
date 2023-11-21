from MainWindow import Ui_Form
from SelectArea import SelectArea
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox
from PySide6.QtCore import QRect, QSize, QPoint, QTimer, Qt
from PySide6.QtGui import QTextCursor, QPixmap, QIcon
import time
#import pygame
import cv2 as cv
import os
import numpy as np
import configparser

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.SelectArea = SelectArea()


        self.ui.screenshoot.clicked.connect(self.HandleScreenShoot)
        self.ui.button.clicked.connect(self.HandleButton)
        self.ui.startbutton.clicked.connect(self.startintel)
        self.ui.endbutton.clicked.connect(self.stopintel)
        self.ui.clearbutton.clicked.connect(self.cleartext)
        self.ui.timebutton.clicked.connect(self.handletimebutton)

        self.start_pos = QPoint()  # upper left corner of screenshot
        self.end_pos = QPoint()  # lower right coner of screenshot
        self.detect_status = False  # is detecting or not
        self.matched = False  # if screenshot match templetes
        self.detect_screen = None # detect on which screen

        self.timer_interval = 2000  # interval of detection loop
        self.timer = QTimer()  # open a timer
        self.timer.setInterval(self.timer_interval)  # set interval
        self.timer.timeout.connect(self.ScreenDetect)  # timer binds detector

        self.imagepath = "./resources/image/templetes" # path
        self.images = []

        # 读取配置文件
        self.config = configparser.ConfigParser()
        self.readconfig()

        #pygame.init()
        #self.sound = pygame.mixer.Sound("resources/audio/alarm_audio.mp3")  # 读入声音文件

    def loadimages(self):
        self.images.clear()
        filenames = os.listdir(self.imagepath)  # imagepath下所有文件名
        for filename in filenames:
            self.images.append(cv.imread(self.imagepath + filename, 1))  # 读入图像文件

    def readconfig(self):
        try:
            self.config.read("localalert.ini", encoding="utf-8")
        except:
            print('config读取有误')
            return

        try:
            screennum = self.config.getint('pos','screen')
            startx = self.config.getint('pos', 'startx')
            starty = self.config.getint('pos', 'starty')
            endx = self.config.getint('pos', 'endx')
            endy = self.config.getint('pos', 'endy')
            self.detect_screen = QApplication.screens[screennum]
            self.changeDetectArea([startx, starty, endx, endy])
            self.start_pos = QPoint(startx, starty)
            self.end_pos = QPoint(endx, endy)
        except:
            print('截图位置有误')
            pass

        try:
            interval = self.config.getint('timer', 'interval')
            self.timer_interval = interval
            self.ui.timespin.setValue(self.timer_interval)
            self.timer.setInterval(self.timer_interval)
        except:
            print('间隔有误')
            pass

        try:
            uitype = self.config.getint('ui','uitype')
            self.ui.UISelect.setCurrentIndex(uitype)
            if uitype == 0:
                self.imagepath = "./resources/image/oldui/"
            else:
                self.imagepath = "./resources/image/newui/"
            self.loadimages()
        except:
            print('ui类型有误')
            pass

    def saveposconfig(self):
        screennum = QApplication.screens.index(self.detect_screen)
        startx = self.start_pos.x()
        starty = self.start_pos.y()
        endx = self.end_pos.x()
        endy = self.end_pos.y()
        if 'pos' not in self.config.sections():
            self.config.add_section('pos')
        self.config.set('pos','screen',str(screennum))
        self.config.set('pos', 'startx',str(startx))
        self.config.set('pos','starty',str(starty))
        self.config.set('pos','endx',str(endx))
        self.config.set('pos','endy',str(endy))
        self.config.write(open("localalert.ini", "w"))


    def savetimerconfig(self):
        if 'timer' not in self.config.sections():
            self.config.add_section('timer')
        self.config.set('timer','interval',str(self.timer_interval))
        self.config.write(open('localalert.ini', 'w'))
    def saveuiconfig(self):
        if 'ui' not in self.config.sections():
            self.config.add_section('ui')
        self.config.set('ui','uitype',str(self.ui.UISelect.currentIndex()))
        self.config.write(open('localalert.ini','w'))

    def HandleUIButton(self):
        if self.ui.UISelect.currentIndex()==0:
            self.imagepath = "./resources/image/oldui/"
        else:
            self.imagepath = "./resources/image/newui/"

        self.loadimages()

        QMessageBox.information(self, 'UI类型设置', 'UI设置为: ' + self.ui.UISelect.currentText(), QMessageBox.Yes)
        self.saveuiconfig()

    def ScreenDetect(self):  # 屏幕检测循环
        if not self.detect_status:
            self.ui.statuslabel.setText('')
            return

        self.ui.statuslabel.setText('正在预警 ' + time.strftime('%H:%M:%S'))

        self.ScreenShoot()  # 截屏
        exist_enemy = self.isenemy()  # 判断是否是敌对
        self.PrintImage()  # 显示图片
        if exist_enemy and not self.matched:
            self.alarm()
        if not exist_enemy and self.matched:
            self.alarmstop()

    def isenemy(self):  # 判断是否有敌对
        status_judge = False

        for image in self.images:

            res = cv.matchTemplate(self.cvimg, image, cv.TM_CCORR_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            if max_val > 0.99:
                status_judge = True
                return status_judge

        return status_judge

    def alarm(self):  # 敌对进入，报警
        self.matched = True
        self.ui.textEdit.append("<font color='red'>" + time.strftime('%H:%M:%S') + " 出现敌对</font>")
        self.ui.textEdit.moveCursor(QTextCursor.End)

        self.sound.play()

    def alarmstop(self):  # 敌对离开
        self.matched = False
        self.ui.textEdit.append("<font color='green'>" + time.strftime('%H:%M:%S') + " 敌对离开</font>")
        self.ui.textEdit.moveCursor(QTextCursor.End)

    def startintel(self):  # 开始预警按钮
        if self.start_pos == None or self.end_pos == None:  # 确认截屏区域有效
            QMessageBox.warning(self, '警告', '截屏区域无效')
            return
        if self.images == []:  # 确认图像模板是否有效
            QMessageBox.warning(self, '警告', 'UI类型未选择')
            return

        self.detect_status = True
        self.timer.start()
        self.ui.textEdit.setHtml("<font>" + time.strftime('%H:%M:%S') + ' 开始检测' + "</font>")
        self.ui.textEdit.moveCursor(QTextCursor.End)

    def stopintel(self):  # 结束预警按钮
        self.detect_status = False
        self.ui.textEdit.append("<font>" + time.strftime('%H:%M:%S') + ' 检测结束' + "</font>")
        self.ui.textEdit.moveCursor(QTextCursor.End)

    def HandleButton(self):  # 点击"确认"按钮，更新截图区域
        self.detect_status = False
        if self.ui.startx.text() == '' or self.ui.starty.text() == '' or self.ui.endx.text() == '' or self.ui.endy.text() == '':
            QMessageBox.warning(self, '警告', '输入有误')
            return
        self.start_pos = QPoint(int(self.ui.startx.text()), int(self.ui.starty.text()))
        self.end_pos = QPoint(int(self.ui.endx.text()), int(self.ui.endy.text()))
        self.ScreenShoot()
        self.PrintImage()

        self.saveposconfig()

    def HandleScreenShoot(self):  # 点击“截图框选”按钮，调出截图窗口
        self.stopintel()
        self.SelectArea.show()
        self.SelectArea._signal.connect(self.changeDetectArea)  # 截图窗口信号返回


    def changeDetectArea(self, lst):  # according to the signal of SelectArea: [screen,sx,sy,ex,ey] , change variables and textboxes. 
        self.detect_screen = lst[0]
        self.start_pos = QPoint(lst[1], lst[2])
        self.end_pos = QPoint(lst[3], lst[4])
        self.ui.startx.setText(str(lst[1]))
        self.ui.starty.setText(str(lst[2]))
        self.ui.endx.setText(str(lst[3]))
        self.ui.endy.setText(str(lst[4]))
        self.ScreenShoot()
        self.PrintImage()

        self.saveposconfig()

    def ScreenShoot(self):  # 截屏
        screenshot = QApplication.primaryScreen().grabWindow(QApplication.desktop().winId())
        rect = QRect(self.start_pos, self.end_pos)
        self.qtpixmap = screenshot.copy(rect)  #qt截图
        self.cvimg = self.qtpixmap_to_cvimg(self.qtpixmap)  #转换成cv图像
        # cv.imshow("im",self.cvimg)
        # self.qtpixmap.save('localshoot.png')

    def PrintImage(self):  # 打印区域截图
        # localshoot = QPixmap('localshoot.png')
        size = QSize(200, 450)
        pixImg = self.qtpixmap.scaled(size, Qt.IgnoreAspectRatio)  #缩放
        self.ui.imagebox.setPixmap(pixImg)  #显示

    def cleartext(self):  # 清空日志
        self.ui.textEdit.clear()

    def handletimebutton(self):  # 设置检测间隔
        self.timer_interval = int(self.ui.timespin.text())
        self.timer.setInterval(self.timer_interval)
        QMessageBox.information(self, '检测间隔设置', '检测间隔设置为' + self.ui.timespin.text(), QMessageBox.Yes)

        self.savetimerconfig()

    def qtpixmap_to_cvimg(self,qtpixmap):
        qimg = qtpixmap.toImage()
        temp_shape = (qimg.height(), qimg.bytesPerLine() * 8 // qimg.depth())
        temp_shape += (4,)
        ptr = qimg.bits()
        ptr.setsize(qimg.byteCount())
        result = np.array(ptr, dtype=np.uint8).reshape(temp_shape)
        result = result[..., :3]
        return result
