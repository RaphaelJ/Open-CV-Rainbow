#!/usr/bin/env python2

# Raphael Javaux <raphaeljavaux@gmail.com> - December 2011

import sys, cv
from PyQt4 import QtGui

class Rainbow(QtGui.QWidget):
    def __init__(self):
        super(Rainbow, self).__init__()
        
        self.setWindowTitle('OpenCV Rainbow')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        
        qbtn = QtGui.QPushButton('Quit', self)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    w = Rainbow()
    w.show()
    
    sys.exit(app.exec_())

    main()