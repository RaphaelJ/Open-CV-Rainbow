#!/usr/bin/env python2

# Raphael Javaux <raphaeljavaux@gmail.com> - December 2011

import sys, cv2

from PyQt4 import QtGui
from PyQt4.QtCore import Qt

class AvailableFilters(QtGui.QGroupBox):
    """
        Widget which displays a list of available filters.
    """    
    def __init__(self):
        super(AvailableFilters, self).__init__("Available filters")

        self._init_hbox()
        
    def _init_hbox(self):
        self._hbox = QtGui.QHBoxLayout(self)
        self._hbox.setAlignment(Qt.AlignTop)

        self._init_filters_list()
        self._init_buttons_vbox()

    def _init_filters_list(self):
        self._filters_list = QtGui.QListWidget()
        self._filters_list.setSelectionMode(
            QtGui.QAbstractItemView.SingleSelection
        )
        self._hbox.addWidget(self._filters_list)

    def _init_buttons_vbox(self):
        self._buttons_vbox = QtGui.QVBoxLayout()
        self._buttons_vbox.setAlignment(Qt.AlignTop)

        self.add = QtGui.QPushButton(
            QtGui.QIcon.fromTheme("list-add"), "Insert filter"
        )
        self._buttons_vbox.addWidget(self.add)

        self._hbox.addLayout(self._buttons_vbox)