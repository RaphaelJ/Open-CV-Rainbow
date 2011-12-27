#!/usr/bin/env python2

# Raphael Javaux <raphaeljavaux@gmail.com> - December 2011

import sys, cv2

from PyQt4 import QtGui
from PyQt4.QtCore import Qt

class FilterOptions(QtGui.QGroupBox):
    """
        Widget which displays a form to edit filter options in real time.
    """    
    def __init__(self):
        super(FilterOptions, self).__init__("Filter options")

        self.setVisible(False)

        self._init_form()
        
    def _init_form(self):
        pass