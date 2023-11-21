# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 11:44:29 2022

@author: Derek Joslin

"""

from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc

import VisualizationManager as vm
import CoordinateScalar as cs

import OperationsManager as om

import qrc_resources

class StateVisualizer(vm.Visualization):

    def __init__(self, name, state, displaySize, parent=None):

        super().__init__(name)

        # mouse tracking ability
        self.setMouseTracking(True)
        self.setAttribute(qc.Qt.WA_TransparentForMouseEvents, True)

        self.setStyleSheet("border: 1px dotted black;")
        self.uniformDot = False
        self.highlightPin = (0,0)
        self.dotSize = 20
        self.BrailleSize = 5
        self.setMouseTracking(True)
        # create display size and state stuff
        self.state = state
        self.nRows = displaySize[0]
        self.nColumns = displaySize[1]
        self.blank = qg.QPixmap(":dot")
        self.blank = self.blank.scaled(qc.QSize(self.dotSize * 0.9,self.dotSize * 0.9))
        self.emptyPin = qg.QPixmap(":emptyPin")
        self.emptyPin = self.emptyPin.scaled(qc.QSize(self.dotSize * 0.9,self.dotSize * 0.9))
        self.filledPin = qg.QPixmap(":filledPin")
        self.filledPin = self.filledPin.scaled(qc.QSize(self.dotSize * 0.9,self.dotSize * 0.9))
        self.grid = qw.QGridLayout()
        self.grid.setHorizontalSpacing(0)
        self.grid.setVerticalSpacing(0)
        self.pinList = []

        self.grid.setHorizontalSpacing(0)
        self.grid.setVerticalSpacing(0)
        for iRow in range(0,displaySize[0] + 1):
            for iColumn in range(0,displaySize[1]):
                if ((iRow + 1) % self.BrailleSize == 0) or ((iColumn + 1) % 3 == 0) or self.uniformDot:
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
                if ((iRow + 1) % self.BrailleSize == 0) or ((iColumn + 1) % 3 == 0) and not self.uniformDot:
                    self.pinList[iPin].clear()
                else:
                    if not iElement:
                        self.pinList[iPin].setPixmap(self.emptyPin)
                    else:
                        self.pinList[iPin].setPixmap(self.filledPin)

                if int(self.highlightPin[0]) == iColumn and int(self.highlightPin[1]) == iRow:
                    self.pinList[iPin].setPixmap(self.blank)
                iPin += 1

class StateVisualizerOperation(om.Operation):

    def __init__(self, name, MousePeripheral, TactileDisplay, StateVisualizer):
        super().__init__(name)

        # inputs to the operation
        self.MousePeripheral = MousePeripheral
        self.inputDictionary[self.MousePeripheral.name] = self.MousePeripheral

        self.TactileDisplay = TactileDisplay
        self.inputDictionary[self.TactileDisplay.name] = self.TactileDisplay

        # outputs to the operation
        self.StateVisualizer = StateVisualizer
        self.outputDictionary[self.StateVisualizer.name] = self.StateVisualizer

        # provide a description
        self.description = "This operation collects the current state of the braille display from memory and updates the state visualizer with it."

        # execute the function continuously until otherwise
        executionParameters = {
            "executeDelay": 2500, # a delay in milliseconds that starts the execution of the Operation after the flag dependencies have been met
            "executeContinuously": True, # a boolean value that determines if the Operation will execute forever
            "executionIntervalTime": 50, # an interval in milliseconds that determines the time between execution
        }

        self.setExecutionParameters(executionParameters)

        self.executable = self.execute

        self.createDebugString()

    def startOperation(self):

        # "Real GUI" Size
        self.realGuiWidth =  829#self.StateVisualizer.frameGeometry().width() #- leftMargin*2#(self.dotSize + 1) * self.nColumns
        self.realGuiHeight = 390#self.StateVisualizer.frameGeometry().height() #- topMargin*2#(self.dotSize + 1) * self.nRows

        pinWidth = 41
        pinHeight = 19

        # create a coordinate scaler
        regions = { "pin" : (pinWidth, pinHeight),
                    "visualizer" : (self.realGuiWidth, self.realGuiHeight)
                   }

        self.scaler = cs.CoordinateScaler(regions)

    def execute(self):
        # get the state from the firmware
        state = self.TactileDisplay.state()
        state = self.TactileDisplay.return_currentState()

        # update the pin position
        xCursorCoordinate = self.MousePeripheral.xCoordinate
        yCursorCoordinate = self.MousePeripheral.yCoordinate

        # get the pin position from visualizer coordinate
        scaledDict = self.scaler.scale(xCursorCoordinate, yCursorCoordinate, "visualizer")

        # get the pin coordinate to highlight
        xPinCoordinate = scaledDict["pin"][0]
        yPinCoordinate = scaledDict["pin"][1]

        self.StateVisualizer.highlightPin = (xPinCoordinate, yPinCoordinate)

        # refresh the visualizer state
        self.StateVisualizer.refreshPins(state)

    def changeDisplay(self):
        if self.StateVisualizer.BrailleSize == 4:
            self.StateVisualizer.BrailleSize = 5
        elif self.StateVisualizer.BrailleSize == 5:
            self.StateVisualizer.uniformDot = True
            self.StateVisualizer.BrailleSize = 20
        else:
            self.StateVisualizer.uniformDot = False
            self.StateVisualizer.BrailleSize = 4
