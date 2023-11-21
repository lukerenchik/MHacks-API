# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 15:37:58 2022

@author: Derek Joslin
"""

from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc
#import pyqtgraph as pg

import qrc_resources

from pyqtconsole.console import PythonConsole
import pyqtconsole.highlighter as hl

import time

import sys

from PyQt5.QtWidgets import QApplication

import NHAPI as nh

import keyboard



class DotVisualizer(qw.QWidget):

    def __init__(self, displaySize,nhAPI):
        super().__init__()


        self.nhAPI = nhAPI
        self.state = self.nhAPI.state()
        self.emptyPin = qg.QPixmap(":emptyPin")
        self.emptyPin = self.emptyPin.scaled(qc.QSize(30,30))
        self.filledPin = qg.QPixmap(":filledPin")
        self.filledPin = self.filledPin.scaled(qc.QSize(30,30))
        self.grid = qw.QGridLayout()
        self.pinList = []
        
        self.grabButton = qw.QPushButton()
        
        self.grabButton.clicked.connect(lambda: self.grabData())
        
        for iRow in range(0,displaySize[0]):
            for iColumn in range(0,displaySize[1]):
                pinImage = qw.QLabel()
                pinImage.setPixmap(self.emptyPin)
                self.pinList.append(pinImage)
                self.grid.addWidget(self.pinList[-1],iRow,iColumn)
                
                
                
        self.grid.addWidget(self.grabButton,20,20)
        self.setLayout(self.grid)
        self.setGeometry(50,50,320,200)
        self.setWindowTitle("Real Time State Visualizer")
        self.startVisual()
        self.show()

    def startVisual(self):
        # Repeating timer, calls random_pick over and over.
        self.grabFirmwareStateTimer = qc.QTimer()
        self.grabFirmwareStateTimer.setInterval(25)
        self.grabFirmwareStateTimer.timeout.connect(self.grabFirmwareState)
        self.grabFirmwareStateTimer.start()

        # Single oneshot which stops the selection after 5 seconds
       # qc.QTimer.singleShot(5000, self.stopVisual)

    def stopVisual(self):
        # Stop the random selection
        self.grabFirmwareStateTimer.stop()

        # The current pick is in self.current_selection


    def grabFirmwareState(self):
        self.stopVisual()
        # Store the current selection, so we have it at the end in stop_selection.
        self.state = self.nhAPI.state()
        
        self.refreshPins()
        
        self.startVisual()
        
    def refreshPins(self):
        
        iPin = 0
        for iRow,rowList in enumerate(self.state):
            for iColumn,iElement in enumerate(rowList):
                if not iElement:
                    self.pinList[iPin].setPixmap(self.emptyPin)
                else:
                    self.pinList[iPin].setPixmap(self.filledPin)
                iPin += 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #create an api object
    BrailleDisplay = nh.NHAPI()
    BrailleDisplay.connect("COM5",1)
    endRom = 0
    
    
    displaySize = BrailleDisplay.size()
    ex = DotVisualizer(displaySize, BrailleDisplay)
    
    sys.exit(app.exec_())

"""

while not keyboard.is_pressed('o') and (endRom is 0):
    #grab the state of the arduino
    state = BrailleDisplay.state()
    
    


else:

    BrailleDisplay.disconnect()
"""
