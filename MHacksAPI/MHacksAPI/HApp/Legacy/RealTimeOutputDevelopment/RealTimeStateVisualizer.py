# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 11:44:29 2022

@author: Derek Joslin
"""

from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc

import VisualizationManager as vm

import HAppOperations as ho

import qrc_resources

class RealTimeStateVisualizer(vm.Visualization):
    
    def __init__(self, name, state, displaySize, parent=None):
        
        super().__init__(name)
        
        self.setStyleSheet("border: 1px dotted black;")
        
        self.highlightPin = (0,0)
        self.dotSize = 20
        self.BrailleSize = 4
        self.setMouseTracking(True)
        # create display size and state stuff
        self.state = state
        self.nRows = displaySize[0]
        self.nColumns = displaySize[1]
        self.blank = qg.QPixmap(":dot")
        self.blank = self.blank.scaled(qc.QSize(self.dotSize,self.dotSize))
        self.emptyPin = qg.QPixmap(":emptyPin")
        self.emptyPin = self.emptyPin.scaled(qc.QSize(self.dotSize,self.dotSize))
        self.filledPin = qg.QPixmap(":filledPin")
        self.filledPin = self.filledPin.scaled(qc.QSize(self.dotSize,self.dotSize))
        self.grid = qw.QGridLayout()
        self.grid.setHorizontalSpacing(0)
        self.grid.setVerticalSpacing(0)
        self.pinList = []
        
        self.grid.setHorizontalSpacing(0)
        self.grid.setVerticalSpacing(0)
        for iRow in range(0,displaySize[0]):
            for iColumn in range(0,displaySize[1]):
                if ((iRow + 1) % self.BrailleSize == 0) or ((iColumn + 1) % 3 == 0):
                    pinImage = qw.QLabel()
                    pinImage.setFixedSize(qc.QSize(self.dotSize,self.dotSize))
                    #pinImage.setPixmap(self.blank)
                    self.pinList.append(pinImage)
                    self.grid.addWidget(self.pinList[-1],iRow,iColumn)
                    self.grid.setRowStretch(iRow, 1)
                    self.grid.setColumnStretch(iColumn, 1)
                    self.grid.setColumnMinimumWidth(iColumn, 10)
                    self.grid.setRowMinimumHeight(iRow, 10)
                else:
                    pinImage = qw.QLabel()
                    pinImage.setPixmap(self.emptyPin)
                    self.pinList.append(pinImage)
                    self.grid.addWidget(self.pinList[-1],iRow,iColumn)
                    self.grid.setRowStretch(iRow, 1)
                    self.grid.setColumnStretch(iColumn, 1)
                    self.grid.setColumnMinimumWidth(iColumn, 10)
                    self.grid.setRowMinimumHeight(iRow, 10)
                 
        self.setLayout(self.grid)
        #self.setGeometry(50,50,320,200)
        self.setWindowTitle("Real Time State Visualizer")
        
        
    def resizeOutput(self):
        #to be implemented in order to resize the display
        pass
        
        
    def refreshPins(self, state):
        self.state = state
        iPin = 0
        for iRow,rowList in enumerate(state):
            for iColumn,iElement in enumerate(rowList):
                if ((iRow + 1) % self.BrailleSize == 0) or ((iColumn + 1) % 3 == 0):
                    self.pinList[iPin].clear()
                else:
                    if not iElement:
                        self.pinList[iPin].setPixmap(self.emptyPin)
                    else:
                        self.pinList[iPin].setPixmap(self.filledPin)
                        
                if int(self.highlightPin[0]) == iColumn and int(self.highlightPin[1]) == iRow:
                    self.pinList[iPin].setPixmap(self.blank)
                iPin += 1


class defaultVisualizerOperation(ho.HAppOperation):
    
    def __init__(self, Engine, Visualizer):
        super().__init__()
        self.Visualizer = Visualizer
        self.BrailleDisplay = Engine
        self.isStopped = 0
    
    def execute(self):
        if self.isStopped:
            print("visualizer stopped")
        else:
            self.grabFirmwareState()

    def delayedExecute(self):
        self.singleShot(10, self.grabFirmwareState())
    
    def startOperation(self):
        #starts the HApp operation
        self.isStopped = 0
        
    def stopOperation(self):
        #stops the HApp operation
        self.isStopped = 1

    def pauseOperation(self):
        #pauses the HApp operation
        pass
        
    def grabFirmwareState(self):
        #get the state from the firmware
        state = self.BrailleDisplay.return_currentState()

        #refresh the visualizer state
        self.Visualizer.refreshPins(state)


                
                