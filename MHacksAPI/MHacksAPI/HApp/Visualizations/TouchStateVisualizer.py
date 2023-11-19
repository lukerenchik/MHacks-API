# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 12:20:33 2022

@author: Derek Joslin

"""

import DefaultMouseHandles as dm
import DefaultKeyboardHandles as dh

import CoordinateScalar as cs

from RealTimeStateVisualizer import StateVisualizer, StateVisualizerOperation
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc

class TouchVisualizer(StateVisualizer):

    def __init__(self, name, state, displaySize):
        
        super().__init__(name, state, displaySize)
        
        # set each label to have mouseTracking
        
        for pin in self.pinList:
            pin.setMouseTracking(True)
        
        # Create a TouchCursor
        self.TouchCursor = TouchCursor(parent=self)
        
        self.xCursorCoordinate = 0
        self.yCursorCoordinate = 0
        

    def moveCursor(self, xCoordinate, yCoordinate):
        
        positionString = "x:{0} y:{1} visualizer".format(xCoordinate, yCoordinate)
        
        self.xCursorCoordinate = xCoordinate
        self.yCursorCoordinate = yCoordinate
        
        # Move the cursor to the specified coordinates
        self.TouchCursor.move(xCoordinate, yCoordinate)
    
        
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
        
        
class TouchVisualizerOperation(StateVisualizerOperation):
    
    def __init__(self, name, MousePeripheral, TactileDisplay, StateVisualizer, margins):
        # initialize the braille display and pass in the visualizer 
        super().__init__(name, MousePeripheral, TactileDisplay, StateVisualizer)
        
        # provide a description
        self.description = "This operation collects the current state of the braille display and communicates with the touchscreen to update the visualizer."
        
        # execute the function continuously until otherwise
        executionParameters = {
            "executeDelay": 0, # a delay in milliseconds that starts the execution of the Operation after the flag dependencies have been met
            "executeContinuously": True, # a boolean value that determines if the Operation will execute forever
            "executionIntervalTime": 10, # an interval in milliseconds that determines the time between execution
        }
        
        self.setExecutionParameters(executionParameters)
        
        self.executable = self.execute
        
        self.createDebugString()
        
        self.margins = margins
        
    def startOperation(self):
        # get the dimensions of the Tactile Display
        self.touchScreenInputSize = self.TactileDisplay.getInputCursorDimensions()
        touchPosition = self.TactileDisplay.getTouchScreenPosition()
        
        self.xCurrentTouchCoordinate = touchPosition[0]
        self.yCurrentTouchCoordinate = touchPosition[1]
        
        # "Real GUI" Size
        self.realGuiWidth =  829#self.StateVisualizer.frameGeometry().width() #- leftMargin*2#(self.dotSize + 1) * self.nColumns
        self.realGuiHeight = 390#self.StateVisualizer.frameGeometry().height() #- topMargin*2#(self.dotSize + 1) * self.nRows
        
        # take the contents margin and subtract from the gui window
        leftMargin = self.margins.left()
        topMargin = self.margins.top()
    
        pinWidth = 41
        pinHeight = 19
        
        # get the size of the touch screen
        touchScreenDimensions = self.TactileDisplay.getInputCursorDimensions()
        
        touchWidth = touchScreenDimensions[0]
        touchHeight = touchScreenDimensions[1]
    
        # create a coordinate scaler
        regions = { "pin" : (pinWidth, pinHeight),
                    "touch" : (touchWidth, touchHeight),
                    "visualizer" : (self.realGuiWidth, self.realGuiHeight)
                   }
        
        self.scaler = cs.CoordinateScaler(regions)
    
    def execute(self):
        super().execute()
        # grab the position from the touchscreen
        
        # Get the x and y coordinates from the line edits
        touchPosition = self.TactileDisplay.getTouchScreenPosition()
                    
        xNewTouchCoordinate = touchPosition[0]
        yNewTouchCoordinate = touchPosition[1]
        
        positionString = "x:{0} y:{1} touch position".format(xNewTouchCoordinate, yNewTouchCoordinate)

        self.description = positionString
        self.createDebugString()
        
        significantChange = self.coordinateChangedSignificantly(xNewTouchCoordinate, yNewTouchCoordinate, 0.01)
        
        if significantChange:
            
            self.xCurrentTouchCoordinate = xNewTouchCoordinate
            self.yCurrentTouchCoordinate = yNewTouchCoordinate
            
            #print(f"x:{xNewTouchCoordinate} y:{yNewTouchCoordinate}")
            
            xVisualizerCoordinate, yVisualizerCoordinate = self.getVisualizerPosition(xNewTouchCoordinate, yNewTouchCoordinate)
            
            #print(f"x:{xVisualizerCoordinate} y:{yVisualizerCoordinate}")
            
            self.StateVisualizer.moveCursor(xVisualizerCoordinate, yVisualizerCoordinate)
            
        else:
            pass
            # print("no change")
            
        # update the pin position 
        xCursorCoordinate = self.MousePeripheral.xCoordinate
        yCursorCoordinate = self.MousePeripheral.yCoordinate
        
        # get the pin position from visualizer coordinate
        scaledDict = self.scaler.scale(xCursorCoordinate, yCursorCoordinate, "visualizer")
        
        # get the pin coordinate to highlight
        xPinCoordinate = scaledDict["pin"][0]
        yPinCoordinate = scaledDict["pin"][1]
        
        self.StateVisualizer.highlightPin = (xPinCoordinate, yPinCoordinate)
        
        
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
    
    
    def getPinPositon(self, xCoordinate, yCoordinate):
        
        scaledDict = self.scaler.scale(xCoordinate, yCoordinate, "touch")
        
        # get the pin coordinate to highlight
        xPinCoordinate = scaledDict["pin"][0]
        yPinCoordinate = scaledDict["pin"][1]
        
        return xPinCoordinate, yPinCoordinate
        
        
    def getVisualizerPosition(self, xCoordinate, yCoordinate):
        
        # take the contents margin and subtract from the gui window
        leftMargin = self.margins.left()
        topMargin = self.margins.top()
        
        scaledDict = self.scaler.scale(xCoordinate, yCoordinate, "touch")
        
        # get the visualizer coordinate
        xVisualizerCoordinate = scaledDict["visualizer"][0]
        yVisualizerCoordinate = scaledDict["visualizer"][1]
        
        xVisualizerCoordinate += leftMargin
        yVisualizerCoordinate += topMargin
        
        return xVisualizerCoordinate, yVisualizerCoordinate

# =============================================================================
#     def getPinPosition(self):
#         # grabs the pin in position that the cursor is over
#         return self.Visualizer.highlightPin
# =============================================================================
        
    def touchSelect(self):
        # select the point that the touch cursor is above
        print("x: {} y: {}".format(self.StateVisualizer.xCursorCoordinate, self.StateVisualizer.yCursorCoordinate))
        
        
    def clickSelect(self, xGuiCoordinate, yGuiCoordinate):

        #take the contents margin and subtract from the gui window
        leftMargin = self.margins.left()
        topMargin = self.margins.top()
        
        # get width and height of the visualizer window
        endXPosition = self.realGuiWidth - leftMargin
        endYPosition = self.realGuiHeight - topMargin
        
        positionString = "x:{0} y:{1} visualizer window".format(xGuiCoordinate, yGuiCoordinate)
        
        # if the cursor is in the viz window then move the touch cursor
        inUpperLeftBound = (xGuiCoordinate > leftMargin) and (yGuiCoordinate > topMargin)
        inLowerRightBound = (xGuiCoordinate < endXPosition) and (yGuiCoordinate < endYPosition)
        
        # if the cursor is in the viz window then move the touch cursor
        if inUpperLeftBound and inLowerRightBound:
            self.StateVisualizer.moveCursor(xGuiCoordinate, yGuiCoordinate)
        else:
            pass
            # print("oob")

    def moveAction(self, xGuiCoordinate, yGuiCoordinate):
        
        #take the contents margin and subtract from the gui window
        leftMargin = self.margins.left()
        topMargin = self.margins.top()
        
        # get width and height of the visualizer window
        endXPosition = self.realGuiWidth - leftMargin
        endYPosition = self.realGuiHeight - topMargin
        
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
            self.StateVisualizer.moveCursor(xGuiCoordinate, yGuiCoordinate)
        else:
            pass
            # print("oob")

class TouchVisualizerKeyboardHandles(dh.DefaultKeyboardHandles):
    
    def __init__(self, ControlCenter):
        super().__init__()
        self.ControlCenter = ControlCenter
        
    def KeySpaceHandler(self):
        VisualizerOperation = self.ControlCenter.getOperation("TouchVisualizerRefreshOperation")
        self.ControlCenter.interruptExecute(lambda: VisualizerOperation.touchSelect())

class TouchVisualizerMouseHandles(dm.DefaultMouseHandles):
    
    def __init__(self, ControlCenter):
        super().__init__()
        self.ControlCenter = ControlCenter
        
    def LeftButtonHandler(self, xCoordinate, yCoordinate):
        # Mouse click event for visualizer operator
        VisualizerOperation = self.ControlCenter.getOperation("TouchVisualizerRefreshOperation")
        self.ControlCenter.interruptExecute(lambda x=xCoordinate,y=yCoordinate: VisualizerOperation.clickSelect(x, y))
        
    def MoveHandler(self, xCoordinate, yCoordinate):
        # Turn off the touch screen tracker
        VisualizerOperation = self.ControlCenter.getOperation("TouchVisualizerRefreshOperation")
        self.ControlCenter.interruptExecute(lambda x=xCoordinate, y=yCoordinate: VisualizerOperation.moveAction(x, y))
        