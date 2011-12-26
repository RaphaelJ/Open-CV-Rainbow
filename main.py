#!/usr/bin/env python2

# Raphael Javaux <raphaeljavaux@gmail.com> - December 2011

import sys
from PyQt4 import QtGui

from gui import rainbow

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    w = rainbow.Rainbow()
    w.show()
    
    sys.exit(app.exec_())