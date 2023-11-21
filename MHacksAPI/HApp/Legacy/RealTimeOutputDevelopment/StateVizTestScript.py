# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 14:48:19 2022

@author: Derek Joslin
"""

import RealTimeStateVisualizer as rtsv
import BRFPrinter as bp
import numpy as np
import math


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5 import QtCore as qc


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.saveFile = 0
        self.page = 0
        # Set the main window properties
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 600, 400)

        # create the brf file
        state = [[0 for _ in range(120)] for _ in range(51)]
        newMat = np.array(state)
        dim = newMat.shape   
        newDim = (math.ceil(dim[0]/20)*20, math.ceil(dim[1]/20)*20)
        data = np.zeros((newDim[0],newDim[1]), dtype=np.uint8)

        # Read in a braille brf file and print it into a matrix
        self.reader = bp.BRFPrinter(data, state)
        
        self.reader.openBRF("C://Users//derek//OneDrive//NewHaptics Shared//HapticOS//FC_GUI_API//APIv0.7-Coeus//v0.766-Coeus//RealTimeOutputDevelopment//")
        
        self.saveFile = self.reader.displayPage(self.page)
        self.reader.savePage(self.saveFile, "Slide {}".format(self.page + 1))
# =============================================================================
#         for lis in reader.state:
#             print(lis)
# =============================================================================
        
        # Create a widget to be displayed as the central widget
        self.central_widget = rtsv.RealTimeStateVisualizer(self.reader.state,[51,120])
        self.setCentralWidget(self.central_widget)
        self.central_widget.refreshPins(self.reader.state)
        
    def keyPressEvent(self, event):
        
        key = event.key()
        if key == qc.Qt.Key_Left:
            self.page -= 1
            print(self.page)
            if self.page >= 0:
                self.saveFile = self.reader.displayPage(self.page)
                self.central_widget.refreshPins(self.reader.state)
                self.reader.savePage(self.saveFile,"Slide {}".format(self.page + 1))
        elif key == qc.Qt.Key_Right:
            self.page += 1
            print(self.page)
            if self.page >= 0:
                self.saveFile = self.reader.displayPage(self.page)
                self.central_widget.refreshPins(self.reader.state)
                self.reader.savePage(self.saveFile,"Slide {}".format(self.page + 1))
                
                

if __name__ == '__main__':
    # Create the Qt application
    app = QApplication(sys.argv)

    # Create and show the main window
    window = MainWindow()
    window.show()

    # Run the Qt application loop
    sys.exit(app.exec_())



