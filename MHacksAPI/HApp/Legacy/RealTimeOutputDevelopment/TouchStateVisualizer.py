# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 12:20:33 2022

@author: Derek Joslin

"""

import DefaultMouseHandles as dm
import DefaultKeyboardHandles as dh

import CoordinateScalar as cs

import RealTimeStateVisualizer as rtsv
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc

class TouchStateVisualizer(rtsv.RealTimeStateVisualizer):

    def __init__(self, state, displaySize, CursorLabel, margins):
        
        super().__init__(state, displaySize)
        
        self.margins = margins
        
        # mouse tracking ability
        self.setMouseTracking(True)
        self.setAttribute(qc.Qt.WA_TransparentForMouseEvents, True)
        
        # set each label to have mouseTracking
        
        for pin in self.pinList:
            pin.setMouseTracking(True)
        
        # Create a label to display the mouse position
        self.CursorLabel = CursorLabel
        
        # Create a TouchCursor
        self.TouchCursor = TouchCursor(parent=self)
        
        self.scalerMade = 0
 
    def createScaler(self):
        # "Real GUI" Size
        realGuiWidth = self.width()#(self.dotSize + 1) * self.nColumns
        realGuiHeight = self.height()#(self.dotSize + 1) * self.nRows

        # create a coordinate scaler
        regions = { "pin" : (42, 20),
                    "touch" : (255*2, 255),
                    "visualizer" : (realGuiWidth, realGuiHeight)
                   }
        
        self.scaler = cs.CoordinateScaler(regions)
        
        #print(realGuiWidth)
        #print(realGuiHeight)
        self.scalerMade = 1

    def moveCursor(self, xCoordinate, yCoordinate, coordinateType):
        
        # if the scaler does not exist create it
        if self.scalerMade:
            pass
        else:
            self.createScaler()
        
        # take the contents margin and subtract from the gui window
        leftMargin = self.margins.left()
        topMargin = self.margins.top()
        
        # coordinate types: pin, touch, gui
        # check which coordinate type the is being recieved
        if coordinateType == "Gui":
            xCoordinate -= leftMargin
            yCoordinate -= topMargin
        
            scaledDict = self.scaler.scale(xCoordinate, yCoordinate, "visualizer")
            
        else:
            
            scaledDict = self.scaler.scale(xCoordinate, yCoordinate, coordinateType)

        # get the pin coordinate to highlight
        xPinCoordinate = scaledDict["pin"][0]
        yPinCoordinate = scaledDict["pin"][1]
        
        self.highlightPin = (xPinCoordinate, yPinCoordinate)
        
        xNewVisualizerGuiCoordinate = scaledDict["visualizer"][0]
        yNewVisualizerGuiCoordinate = scaledDict["visualizer"][1]
        
        positionString = "x:{0} y:{1} visualizer".format(xNewVisualizerGuiCoordinate, yNewVisualizerGuiCoordinate)
            
        
        xNewVisualizerGuiCoordinate += leftMargin
        yNewVisualizerGuiCoordinate += topMargin
        
        # Move the cursor to the specified coordinates
        self.TouchCursor.move(xNewVisualizerGuiCoordinate, yNewVisualizerGuiCoordinate)
        

    def selectPoint(self):
        self.CursorLabel.setText("select")
        
class TouchCursor(qw.QLabel):
    
    def __init__(self, parent):
        
        super().__init__(parent)

        self.setStyleSheet("border: 5px solid green;")

        # Set the background color to red
        palette = qg.QPalette()
        palette.setColor(qg.QPalette.Background, qg.QColor("green"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # Set the size of the label
        self.setFixedSize(7.5, 7.5)
        
        # start in the (0,0) position
        self.move(0, 0)
        
class TouchVisualizerOperation(rtsv.defaultVisualizerOperation):
    
    def __init__(self, Engine, Visualizer):
        # initialize the braille display and pass in the visualizer 
        super().__init__(Engine, Visualizer)
        self.touchScreenInputSize = self.BrailleDisplay.getInputCursorDimensions()
        touchPosition = self.BrailleDisplay.getInputCursorPosition()
                    
        self.xCurrentTouchCoordinate = touchPosition[0]
        self.yCurrentTouchCoordinate = touchPosition[1]
    
    def changeDisplay(self):
        if self.Visualizer.BrailleSize == 4:
            self.Visualizer.BrailleSize = 5
        else:
            self.Visualizer.BrailleSize = 4
    
    def getPinPosition(self):
        # grabs the pin in position that the cursor is over
        return self.Visualizer.highlightPin
    
    def execute(self):
        super().execute()
        if self.isStopped:
            pass
        else:
            # grab the position from the touchscreen
            
            # Get the x and y coordinates from the line edits
            touchPosition = self.BrailleDisplay.getInputCursorPosition()
                        
            xNewTouchCoordinate = touchPosition[0]
            yNewTouchCoordinate = touchPosition[1]
            
            positionString = "x:{0} y:{1} touch".format(xNewTouchCoordinate, yNewTouchCoordinate)
                
            # print(positionString)
            
            significantChange = self.coordinateChangedSignificantly(xNewTouchCoordinate, yNewTouchCoordinate, 0.01)
            
            if significantChange:
                
                self.xCurrentTouchCoordinate = xNewTouchCoordinate
                self.yCurrentTouchCoordinate = yNewTouchCoordinate
                
                self.Visualizer.moveCursor(xNewTouchCoordinate, yNewTouchCoordinate, 'touch')
                
            else:
                pass
                # print("no change")
                
    def coordinateChangedSignificantly(self, newX, newY, boundedPercent):
        # Calculate the difference between the current and previous x and y coordinates
        xDifference = abs(self.xCurrentTouchCoordinate - newX)
        yDifference = abs(self.yCurrentTouchCoordinate - newY)
        
        positionString = "x:{0} y:{1} old touch".format(self.xCurrentTouchCoordinate, self.yCurrentTouchCoordinate)
    
        #print(positionString)
    
        # Calculate the maximum distance the coordinate could have moved while staying within the bounds
        xMaxDifference = self.touchScreenInputSize[0] * boundedPercent
        yMaxDifference = self.touchScreenInputSize[1] * boundedPercent
    
        positionString = "x:{0} y:{1} touch Max Difference".format(xMaxDifference, yMaxDifference)
    
        #print(positionString)
    
        # Return True if the coordinate has moved more than 5% in either the x or y direction
        return (xDifference > xMaxDifference) or (yDifference > yMaxDifference)
            
    def touchSelect(self):
        # select the point that the touch cursor is above
        self.Visualizer.selectPoint()
        
        
    def clickSelect(self, xGuiCoordinate, yGuiCoordinate):
        self.stopOperation()
        # select the point that the mouse is on
        # Update the mouse position label when the mouse moves
# =============================================================================
#         print("click")
#         
#         positionString = "x:{0} y:{1} GUI Position QMainWindow Offset".format(xCoordinate, yCoordinate)
#         
#         print(positionString)
#         
# =============================================================================

        #take the contents margin and subtract from the gui window
        leftMargin = self.Visualizer.margins.left()
        topMargin = self.Visualizer.margins.top()
        
        # get width and height of the visualizer window
        endXPosition = self.Visualizer.width() - leftMargin
        endYPosition = self.Visualizer.height() - topMargin
        
        positionString = "x:{0} y:{1} visualizer window".format(xGuiCoordinate, yGuiCoordinate)

        #print(positionString)
        
        self.Visualizer.CursorLabel.setText(positionString)
        
        # if the cursor is in the viz window then move the touch cursor
        inUpperLeftBound = (xGuiCoordinate > leftMargin) and (yGuiCoordinate > topMargin)
        inLowerRightBound = (xGuiCoordinate < endXPosition) and (yGuiCoordinate < endYPosition)
        
        # if the cursor is in the viz window then move the touch cursor
        if inUpperLeftBound and inLowerRightBound:
            self.Visualizer.moveCursor(xGuiCoordinate, yGuiCoordinate, "Gui")
        else:
            pass
            # print("oob")
        
        self.startOperation()

    def moveAction(self, xGuiCoordinate, yGuiCoordinate):
        self.stopOperation()
        
        #take the contents margin and subtract from the gui window
        leftMargin = self.Visualizer.margins.left()
        topMargin = self.Visualizer.margins.top()
        
        # get width and height of the visualizer window
        endXPosition = self.Visualizer.width() - leftMargin
        endYPosition = self.Visualizer.height() - topMargin
        
        # Get the current cursor position
# =============================================================================
#         positionString = "x:{0} y:{1} visualizer window".format(self.Visualizer.width(), self.Visualizer.height())
#         
#         print(positionString)
# =============================================================================

        # if the cursor is in the viz window then move the touch cursor
        inUpperLeftBound = (xGuiCoordinate > leftMargin) and (yGuiCoordinate > topMargin)
        inLowerRightBound = (xGuiCoordinate < endXPosition) and (yGuiCoordinate < endYPosition)
        
        if inUpperLeftBound and inLowerRightBound:
            self.Visualizer.moveCursor(xGuiCoordinate, yGuiCoordinate, "Gui")
        else:
            pass
            # print("oob")

        # after 10 milliseconds turn the touchscreen back on
        self.startOperation()

class TouchVisualizerKeyboardHandles(dh.DefaultKeyboardHandles):
    
    def __init__(self, Operation):
        super().__init__()
        self.VisualizerOperator = Operation
        
    def KeySpaceHandler(self):
        self.VisualizerOperator.touchSelect()

class TouchVisualizerMouseHandles(dm.DefaultMouseHandles):
    
    def __init__(self, Operation, margins):
        super().__init__()
        self.VisualizerOperator = Operation
        self.margins = margins
        
    def LeftButtonHandler(self, xCoordinate, yCoordinate):
        # Mouse click event for visualizer operator
        self.VisualizerOperator.clickSelect(xCoordinate, yCoordinate)
        
    def MoveHandler(self, xCoordinate, yCoordinate):
        # Turn off the touch screen tracker
        self.VisualizerOperator.moveAction(xCoordinate, yCoordinate)
        