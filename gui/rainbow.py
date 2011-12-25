#!/usr/bin/env python2

# Raphael Javaux <raphaeljavaux@gmail.com> - December 2011

import sys, cv2
from PyQt4 import QtGui

class Rainbow(QtGui.QMainWindow):
    IMAGES_WIDTH, IMAGES_HEIGHT = 400.0, 300.0
    
    # Source image (OpenCV)
    _source = None
    # Result image (OpenCV)
    _result = None
    
    def __init__(self):
        super(Rainbow, self).__init__()
        
        self.setWindowTitle("OpenCV Rainbow")
        self.setWindowIcon(QtGui.QIcon("icon.png"))

        self._init_toolbar()
        self._init_vbox()

    @property
    def source(self):
        return self._source
    
    @source.setter
    def source(self, val):
        """ Sets _source and shows the new image """
        self._source = val
        Rainbow._display_cv_image(self._source_label, val)
        
    @property
    def result(self):
        return self._result
    
    @result.setter
    def result(self, val):
        """ Sets _result and shows the new image """
        self._result = val
        Rainbow._display_cv_image(self._result_label, val)

    def _init_toolbar(self):
        bar = self.addToolBar("Main toolbar")
        
        open_image = QtGui.QAction(
            QtGui.QIcon.fromTheme("folder-image"), "Open image", self
        )
        open_image.setShortcuts(QtGui.QKeySequence.Open)
        open_image.triggered.connect(self._open_image)
        bar.addAction(open_image)
        
        bar.addSeparator()
        
        open_bow = QtGui.QAction(
            QtGui.QIcon.fromTheme("document-open"), "Open filters document",
            self
        )
        bar.addAction(open_bow)
        
        save_bow = QtGui.QAction(
            QtGui.QIcon.fromTheme("document-save"), "Save filters document",
            self
        )
        bar.addAction(save_bow)
        
        bar.addSeparator()
        
        save_bow = QtGui.QAction(
            QtGui.QIcon.fromTheme("view-refresh"), "Recompute image", self
        )
        bar.addAction(save_bow)
        
        bar.addSeparator()
        
        quit = QtGui.QAction(
            QtGui.QIcon.fromTheme("application-exit"), "Quit", self
        )
        quit.setShortcuts(QtGui.QKeySequence.Quit)
        quit.triggered.connect(self.close)
        bar.addAction(quit)
    
    def _init_vbox(self):
        self._vbox = QtGui.QVBoxLayout()
        
        self._source_label = QtGui.QLabel(self)
        self._source_label.setFixedSize(
            Rainbow.IMAGES_WIDTH, Rainbow.IMAGES_HEIGHT
        )
        self._vbox.addWidget(self._source_label)
        
        self._result_label = QtGui.QLabel(self)
        self._vbox.addWidget(self._result_label)
        
        vbox_widget = QtGui.QWidget()
        vbox_widget.setLayout(self._vbox)
        self.setCentralWidget(vbox_widget)
    
    def _init_images(self):
        

    def _open_image(self):
        """ Opens a File Dialog to select an image and displays it """
        filename = QtGui.QFileDialog.getOpenFileName(
            self, "Open image", "", "Image Files (*.png *.jpg *.bmp)"
        )

        if filename != "":
            cv_img = cv2.imread(str(filename))
            
            self.source = cv_img

    @staticmethod
    def resize_for_interface(cv_img):
        """
            Resizes an image from OpenCV to be displayed in the interface,
            keeping the image's ratio.
        """

        height, width, channels = cv_img.shape
        width_ratio = width / IMAGES_WIDTH
        height_ratio = height / IMAGES_HEIGHT

        ratio = max(width_ratio, height_ratio)

        if ratio > 1:
            new_size = (int(width / ratio), int(height / ratio))
            return cv2.resize(cv_img, new_size)
        else:
            # No need to resize
            return cv_img

    @staticmethod
    def cv_image_to_qt_image(cv_img):
        """ Converts an OpenCV image into a Qt image """
        height, width, channels = cv_img.shape

        ##return QtGui.QImage(
            ##cv_img.data, width, height, QtGui.QImage.Format_ARGB32
        ##)
        
        qt_img = QtGui.QImage(width, height, QtGui.QImage.Format_RGB888)

        for i, line in enumerate(cv_img):
            for j, pix in enumerate(line):
                qt_img.setPixel(j, i, QtGui.qRgb(pix[2], pix[1], pix[0]))

        return qt_img
            
    @staticmethod
    def _display_cv_image(qt_label, cv_img):
        """ Puts an OpenCV image inside a QLabel """
        qt_img = Rainbow.cv_image_to_qt_image(
            Rainbow.resize_for_interface(cv_img)
        )

        qt_label.setPixmap(QtGui.QPixmap.fromImage(qt_img))

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    w = Rainbow()
    w.show()
    
    sys.exit(app.exec_())