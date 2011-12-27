#!/usr/bin/env python2

# Raphael Javaux <raphaeljavaux@gmail.com> - December 2011

import sys, cv2

from PyQt4 import QtGui, QtCore
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
        
        self._filters_list.setItemDelegate(FilterDelegate())
        self._filters_model = FilterModel()
        self._filters_list.setModel(self._filters_model)
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

class FilterModel(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super(FilterModel, self).__init__(parent)
        self.data = [10, 12]
    
    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.data)

    def data(self, index, role):
        if index.isValid() and role == Qt.DisplayRole:
            return QtCore.QVariant(self.data[index.row()])
        else:
            return QtCore.QVariant(None)

class FilterDelegate(QtGui.QItemDelegate):
    """
        Renders filter's information inside a list cell.

        --------------------------------------------
        -           Title                          -
        -  Result   Filter's name - Rendering time -
        -           Options                        -
        --------------------------------------------
    """
    THUMBS_WIDTH, THUMBS_HEIGHT = 40.0, 30.0
    MARGIN = 5 # Borders margin
    SPACING = 7 # Space between elements

    def sizeHint(self, option, index):
        return QtCore.QSize(25, 75)
    
    def paint(self, painter, option, index):
        # Initializes fonts
        title_font = QtGui.QApplication.font()
        title_font.setWeight(QtGui.QFont.Bold)
        details_font = QtGui.QApplication.font()        
        
        # Gets colors for the current widget's status
        palette = option.palette
        if option.state & QtGui.QStyle.State_Selected:
            bg_color = palette.color(
                QtGui.QPalette.Disabled, QtGui.QPalette.Highlight
            )
            fg_color = palette.color(
                QtGui.QPalette.Active, QtGui.QPalette.HighlightedText
            )
        else:
            bg_color = palette.color(
                QtGui.QPalette.Active, QtGui.QPalette.Base
            )
            fg_color = palette.color(
                QtGui.QPalette.Active, QtGui.QPalette.WindowText
            )

        # Draws the background
        painter.fillRect(option.rect, bg_color)

        # Draws the filter's title
        painter.setFont(title_font)
        painter.drawText()

    @staticmethod
    def layout(filter_, title_font, details_font):
        """ Gives the rectangles of the different elements of the cell. """
        thumb_rect = QtCore.QRect(
            FilterDelegate.MARGIN, FilterDelegate.MARGIN,
            FilterDelegate.THUMBS_WIDTH, FilterDelegate.THUMBS_HEIGHT
        )
        
        title_rect = QtCore.QRect(
            thumb_rect.right + FilterDelegate.MARGIN, FilterDelegate.MARGIN
            QtGui.QFontMetrics(title_font).size(0, filter_.title)
        )
        
        name_rect = QtCore.QRect(
            thumb_rect.right + FilterDelegate.SPACING,
            title_rect.bottom + FilterDelegate.MARGIN
            QtGui.QFontMetrics(details_font).size(0, filter_.name)
        )

        return thumb_rect, title_rect, name_rect