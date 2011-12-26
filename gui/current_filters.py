#!/usr/bin/env python2

# Raphael Javaux <raphaeljavaux@gmail.com> - December 2011

import sys, cv2

from PyQt4 import QtGui
from PyQt4.QtCore import Qt

class CurrentFilters(QtGui.QGroupBox):
    """
        Widget which manage the list of filters which are applied to the image
    """    
    def __init__(self):
        super(CurrentFilters, self).__init__("Applied filters")

        self._init_hbox()
        
    def _init_hbox(self):
        self._hbox = QtGui.QHBoxLayout(self)

        self._init_filters_list()
        self._init_buttons_vbox()

    def _init_filters_list(self):
        self._filters_list = QtGui.QListView()

        self._filters_list.setSelectionMode(
            QtGui.QAbstractItemView.SingleSelection
        )
        self._hbox.addWidget(self._filters_list)

    def _init_buttons_vbox(self):
        self._buttons_vbox = QtGui.QVBoxLayout()
        self._buttons_vbox.setAlignment(Qt.AlignTop)

        self.up = QtGui.QPushButton(
            QtGui.QIcon.fromTheme("go-up"), "Move filter up"
        )
        self._buttons_vbox.addWidget(self.up)
        
        self.down = QtGui.QPushButton(
            QtGui.QIcon.fromTheme("go-down"), "Move filter down"
        )
        self._buttons_vbox.addWidget(self.down)

        self.down = QtGui.QPushButton(
            QtGui.QIcon.fromTheme("list-remove"), "Remove filter"
        )
        self._buttons_vbox.addWidget(self.down)

        self._hbox.addLayout(self._buttons_vbox)

#class FilterModel(QtGui.QAbstractListModel):
    #pass

class FilterDelegate(QtGui.QStyledItemDelegate):
    """
        Renders filter's information inside a list cell.

        ------------------------------------------
        -         -   Filter's name              -
        -  Result -   Rendering time             -
        -         -   Options                    -
        ------------------------------------------
    """
    THUMBS_WIDTH, THUMBS_HEIGHT = 100.0, 75.0

    def sizeHint(self, option, index):
        Qt.QSize(300, 100)
    
    def paint(self, painter, option, index):
        pass