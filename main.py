#!/usr/bin/env python2

# Raphael Javaux <raphaeljavaux@gmail.com> - December 2011

import sys, cv2
from PyQt4 import QtGui

class Rainbow(QtGui.QMainWindow):
    def __init__(self):
        super(Rainbow, self).__init__()
        
        self.setWindowTitle("OpenCV Rainbow")
        self.setWindowIcon(QtGui.QIcon("icon.png"))

        self._init_toolbar()
        #self._init_hbox()

        self._source_label = QtGui.QLabel(self)
        self.setCentralWidget(self._source_label)
        self.source = None

    def _init_toolbar(self):
        bar = self.addToolBar("Main toolbar")
        
        open_image = QtGui.QAction(
            QtGui.QIcon.fromTheme("document-open"), "Open image", self
        )
        open_image.setShortcuts(QtGui.QKeySequence.Open)
        open_image.triggered.connect(self._open_image)
        
        bar.addAction(open_image)

    def _open_image(self):
        """ Opens a File Dialog to select an image and displays it """
        filename = QtGui.QFileDialog.getOpenFileName(
            self, "Open image", "", "Image Files (*.png *.jpg *.bmp)"
        )

        if filename != "":
            cv_img = cv2.imread(str(filename))
            
            qt_img = Rainbow._cv_image_to_qt_image(
                Rainbow._resize_for_interface(cv_img)
            )

            self._source_label.setPixmap(QtGui.QPixmap.fromImage(qt_img))
            self.source = cv_img

    @staticmethod
    def _resize_for_interface(cv_img):
        """
            Resizes an image from OpenCV to be displayed in the interface,
            keeping the image's ratio.
        """
        MAX_WIDTH, MAX_HEIGHT = 400.0, 300.0

        height, width, channels = cv_img.shape
        width_ratio = width / MAX_WIDTH
        height_ratio = height / MAX_HEIGHT

        ratio = max(width_ratio, height_ratio)

        if ratio > 1:
            new_size = (int(width / ratio), int(height / ratio))
            return cv2.resize(cv_img, new_size)
        else:
            # No need to resize
            return cv_img

    @staticmethod
    def _cv_image_to_qt_image(cv_img):
        height, width, channels = cv_img.shape

        ##return QtGui.QImage(
            ##cv_img.data, width, height, QtGui.QImage.Format_ARGB32
        ##)
        
        qt_img = QtGui.QImage(width, height, QtGui.QImage.Format_RGB888)

        for i, line in enumerate(cv_img):
            for j, pix in enumerate(line):
                qt_img.setPixel(j, i, QtGui.qRgb(pix[2], pix[1], pix[0]))

        return qt_img
                

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    w = Rainbow()
    w.show()
    
    sys.exit(app.exec_())