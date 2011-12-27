#!/usr/bin/env python2

# Raphael Javaux <raphaeljavaux@gmail.com> - December 2011

import sys, cv2

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from filters.filter import Filter

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
        self._filters_list.setModel(FilterModel())
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
        self.data = [
            Filter("Flou"), Filter("Rotation")
        ]
    
    def rowCount(self, parent=None):
        return len(self.data)

    def data(self, index, role):
        if index.isValid() and role == Qt.DisplayRole:
            return self.data[index.row()]
        else:
            return None

class FilterDelegate(QtGui.QItemDelegate):
    """
        Renders filter's information inside a list cell.

        --------------------------------------------
        -           Title                          -
        -  Result   Filter's name   Rendering time -
        -           Options                        -
        --------------------------------------------
    """
    THUMBS_WIDTH, THUMBS_HEIGHT = 40.0, 30.0
    MARGIN = 5 # Borders margin
    SPACING = 7 # Space between elements

    def sizeHint(self, option, index):
        filter_ = index.data(Qt.DisplayRole).toPyObject()
        
        title_font, details_font = FilterDelegate.fonts()
        
        thumb_rect, title_rect, name_rect, rendering_rect, options_rect = \
            FilterDelegate.layout(filter_, title_font, details_font)
        
        bounds = thumb_rect.united(title_rect)\
                           .united(name_rect)\
                           .united(rendering_rect)\
                           .united(options_rect)
        
        return bounds.size()
    
    def paint(self, painter, option, index):
        filter_ = index.data(Qt.DisplayRole).toPyObject()
        
        title_font, details_font = FilterDelegate.fonts()
        
        # Gets colors for the current widget's status
        palette = option.palette
        if option.state & QtGui.QStyle.State_Selected:
            bg_color = palette.color(
                QtGui.QPalette.Active, QtGui.QPalette.Highlight
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
        
        # Compute layout
        thumb_rect, title_rect, name_rect, rendering_rect, options_rect = \
            FilterDelegate.layout(filter_, title_font, details_font)
        
        # Draws the filter's title
        painter.setFont(title_font)
        painter.drawText(title_rect, 0, filter_.title)

    @staticmethod
    def fonts():
        title_font = QtGui.QApplication.font()
        title_font.setWeight(QtGui.QFont.Bold)
        details_font = QtGui.QApplication.font()
        
        return title_font, details_font
    
    @staticmethod
    def layout(filter_, title_font, details_font):
        """ Gives the rectangles of the different elements of the cell. """
        thumb_rect = QtCore.QRect(
            QtCore.QPoint(FilterDelegate.MARGIN, FilterDelegate.MARGIN),
            QtCore.QSize(
                FilterDelegate.THUMBS_WIDTH, FilterDelegate.THUMBS_HEIGHT
            )
        )
        
        title_rect = QtCore.QRect(
            QtCore.QPoint(
                thumb_rect.right() + FilterDelegate.MARGIN,
                FilterDelegate.MARGIN
            ),
            QtGui.QFontMetrics(title_font).size(0, filter_.title)
        )
        
        name_rect = QtCore.QRect(
            QtCore.QPoint(
                thumb_rect.right() + FilterDelegate.MARGIN,
                title_rect.bottom() + FilterDelegate.SPACING
            ),
            QtGui.QFontMetrics(details_font).size(0, filter_.name)
        )
        
        rendering_rect = QtCore.QRect(
            QtCore.QPoint(
                name_rect.right() + FilterDelegate.SPACING,
                title_rect.bottom() + FilterDelegate.SPACING
            ),
            QtGui.QFontMetrics(details_font).size(
                0, str(filter_.rendering_time)
            )
        )
        
        options_rect = QtCore.QRect(
            QtCore.QPoint(
                thumb_rect.right() + FilterDelegate.MARGIN,
                name_rect.bottom() + FilterDelegate.SPACING
            ),
            QtGui.QFontMetrics(details_font).size(0, str(filter_.options))
        )
        
        return thumb_rect, title_rect, name_rect, rendering_rect, options_rect