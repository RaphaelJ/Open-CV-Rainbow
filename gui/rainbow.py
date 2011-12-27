#!/usr/bin/env python2

# Raphael Javaux <raphaeljavaux@gmail.com> - December 2011

import sys, cv2
from PyQt4 import QtGui

from images import Images
from current_filters import CurrentFilters
from available_filters import AvailableFilters
from filter_options import FilterOptions

class Rainbow(QtGui.QMainWindow):
    def __init__(self):
        super(Rainbow, self).__init__()
        
        self.setWindowTitle("OpenCV Rainbow")
        self.setWindowIcon(QtGui.QIcon("icon.png"))

        self._init_toolbar()
        self._init_vbox()

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
        
        refresh = QtGui.QAction(
            QtGui.QIcon.fromTheme("view-refresh"), "Recompute image", self
        )
        refresh.setShortcuts(QtGui.QKeySequence.Refresh)
        refresh.triggered.connect(self.compute_image)
        bar.addAction(refresh)
        
        bar.addSeparator()
        
        quit = QtGui.QAction(
            QtGui.QIcon.fromTheme("application-exit"), "Quit", self
        )
        quit.setShortcuts(QtGui.QKeySequence.Quit)
        quit.triggered.connect(self.close)
        bar.addAction(quit)
    
    def _init_vbox(self):
        self._vbox = QtGui.QVBoxLayout()
        
        self.images = Images(self)
        self._vbox.addWidget(self.images)

        self._init_filters_grid()
        
        vbox_widget = QtGui.QWidget()
        vbox_widget.setLayout(self._vbox)
        self.setCentralWidget(vbox_widget)

    def _init_filters_grid(self):
        self._filters_grid = QtGui.QGridLayout()

        self.current_filters = CurrentFilters()
        self._filters_grid.addWidget(self.current_filters, 0, 0, 2, 1)

        self.available_filters = AvailableFilters()
        self._filters_grid.addWidget(self.available_filters, 0, 1, 1, 1)

        self.filter_options = FilterOptions()
        self._filters_grid.addWidget(self.filter_options, 1, 1, 1, 1)

        self._vbox.addLayout(self._filters_grid)

    def _open_image(self):
        """ Opens a File Dialog to select an image and displays it """
        filename = QtGui.QFileDialog.getOpenFileName(
            self, "Open image", "", "Image Files (*.png *.jpg *.bmp)"
        )

        if filename != "":
            cv_img = cv2.imread(str(filename))
            
            self.images.source = cv_img

    def compute_image(self):
        """ Compute the resuling image using the filters """
        self.images.result = self.images.source