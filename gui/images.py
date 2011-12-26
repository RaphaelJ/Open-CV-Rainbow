#!/usr/bin/env python2

# Raphael Javaux <raphaeljavaux@gmail.com> - December 2011

import sys, cv2
from PyQt4 import QtGui
from PyQt4.QtCore import *  

class Images(QtGui.QWidget):
    """ Widget which shows the source and the result image """
    IMAGES_WIDTH, IMAGES_HEIGHT = 400.0, 300.0
    
    # Source image (OpenCV)
    _source = None
    # Result image (OpenCV)
    _result = None
    
    def __init__(self, rainbow):
        super(Images, self).__init__()

        self._rainbow = rainbow

        self._init_hbox()

    @property
    def source(self):
        return self._source
    
    @source.setter
    def source(self, val):
        """ Sets _source, compute result and shows the new image """
        self._source = val
        
        if val != None:
            Images._display_cv_image(self._source_label, val)
            self._rainbow.compute_image()
        else:
            self.result = None            
        
    @property
    def result(self):
        return self._result
    
    @result.setter
    def result(self, val):
        """ Sets _result and shows the new image """
        self._result = val

        if val != None:
            Images._display_cv_image(self._result_label, val)
        
    def _init_hbox(self):
        class ClickableLabel(QtGui.QLabel):
            """ A simple QLabel which emits the clicked event """
            def mouseReleaseEvent(self, ev):
                self.emit(SIGNAL('clicked()')) 
        
        def put_in_groupbox(widget, title):
            """ Puts a single widget inside a titled QGroupBox """
            box = QtGui.QGroupBox(title)
            layout = QtGui.QHBoxLayout()
            layout.addWidget(widget)
            box.setLayout(layout)
            return box
        
        def set_label_size(qt_label):
            """
                Initialises the size of the label to the images's maximum size
            """
            qt_label.setFixedSize(
                Images.IMAGES_WIDTH, Images.IMAGES_HEIGHT
            )
        
        self._hbox = QtGui.QHBoxLayout()
        self._hbox.setSizeConstraint(QtGui.QLayout.SetMinimumSize)

        self._source_label = ClickableLabel()
        self.connect(
            self._source_label, SIGNAL('clicked()'),
            lambda: Images.full_size_image(self.source)
        )
        set_label_size(self._source_label)
        self._hbox.addWidget(put_in_groupbox(self._source_label, "Source"))
        
        self._result_label = ClickableLabel()
        self.connect(
            self._result_label, SIGNAL('clicked()'),
            lambda: Images.full_size_image(self.result)
        )
        set_label_size(self._result_label)
        self._hbox.addWidget(put_in_groupbox(self._result_label, "Result"))
        
        self.setLayout(self._hbox)

    @staticmethod
    def full_size_image(cv_image):
        """ Displays an image within a QDialog """
        if cv_image != None:
            dialog = QtGui.QDialog(self._rainbow)
            dialog.setWindowTitle("Image preview")

            label = QtGui.QLabel()
            Images._display_cv_image(label, cv_image, resize=False)

            layout = QtGui.QHBoxLayout()
            layout.addWidget(label)
            dialog.setLayout(layout)
            
            dialog.exec_()

    @staticmethod
    def resize_for_interface(cv_img):
        """
            Resizes an image from OpenCV to be displayed in the interface,
            keeping the image's ratio.
        """

        height, width, channels = cv_img.shape
        width_ratio = width / Images.IMAGES_WIDTH
        height_ratio = height / Images.IMAGES_HEIGHT

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
    def _display_cv_image(qt_label, cv_img, resize=True):
        """ Puts an OpenCV image inside a QLabel """
        qt_img = Images.cv_image_to_qt_image(
            Images.resize_for_interface(cv_img) if resize else cv_img
        )

        qt_label.setPixmap(QtGui.QPixmap.fromImage(qt_img))