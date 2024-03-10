from PySide6.QtGui import QPixmap,QImage,qRed,qGreen,qBlue
import cv2
import numpy as np

def qtpixmap_to_cvimg(pixmap:QPixmap):
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

def cvimg_to_qtpixmap(cvimg):
    height, width, depth = cvimg.shape
    cvimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
    qimage = QImage(cvimg.data, width, height, width * depth, QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(qimage)
    return pixmap