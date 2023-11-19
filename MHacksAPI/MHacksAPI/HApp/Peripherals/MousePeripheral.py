# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 10:15:15 2022

@author: Derek Joslin

"""

from PyQt5 import QtCore as qc
import PeripheralManager as pm

class MousePeripheral(pm.PeripheralDevice):
    
    def __init__(self, name, MouseHandles):
        super().__init__(name)
        
        self.DefaultMouseHandles = MouseHandles
        self.MouseHandles = MouseHandles
        
        self.xCoordinate = 0
        self.yCoordinate = 0
        
    def setNewMouseHandler(self, NewMouseHandles):
        
        self.MouseHandles = NewMouseHandles
        
    def revertToDefaultHandler(self):
        
        self.MouseHandles = self.DefaultMouseHandles
        
    def setDefaultHandler(self, DefaultMouseHandles):
        
        self.DefaultMouseHandles = DefaultMouseHandles
        self.MouseHandles = DefaultMouseHandles
        
    def handleMouseEvent(self, MouseEvent):
        
        xCoordinate = MouseEvent.x()
        yCoordinate = MouseEvent.y()
        
        yStart = 23
        
        if yCoordinate > yStart:
            yCoordinate -= yStart
        else:
            yCoordinate = 0
            
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
        self.debugString = "Mouse Position: x:{} y:{}".format(xCoordinate, yCoordinate)

# =============================================================================
#         # Get the widget's width and height and margins
#         width = visualization.width()
#         height = visualization.height()
#         margins = visualization.contentsMargins()
#         
#         # Subtract the top and left margins from the widget's size
#         layoutWidth = width - margins.left()
#         layoutHeight = height - margins.top()
#         
#         # Calculate x and y as percentages of the widget size
#         x = xCoordinate / layoutWidth
#         y = yCoordinate / layoutHeight
# 
#         #self.cursor_position_label.setText("Cursor position: ({:.2f}%, {:.2f}%)".format(x * 100, y * 100))
# 
#         # Convert x and y to row and column indices
#         row = int(y * (visualization.nRows - 1))
#         col = int(x * (visualization.nColumns - 1))
#         
# =============================================================================
        
        # Check if the left mouse button is clicked
        if MouseEvent.button() == qc.Qt.LeftButton:
            
            self.MouseHandles.LeftButtonHandler(xCoordinate, yCoordinate)
            
        # Check if the right mouse button is clicked
        elif MouseEvent.button() == qc.Qt.RightButton:
            
            self.MouseHandles.RightButtonHandler(xCoordinate, yCoordinate)
            
        else:
            
            print("no handler for that Mouse event")
        
        
    def handleMouseMoveEvent(self, MouseEvent):
             
        
        xCoordinate = MouseEvent.x()
        yCoordinate = MouseEvent.y()
        
        yStart = 23
        
        if yCoordinate > yStart:
            yCoordinate -= yStart
        else:
            yCoordinate = 0
        
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
        
        self.debugString = "Mouse Position: x:{} y:{}".format(xCoordinate, yCoordinate)

# =============================================================================
#         # Get the widget's width and height and margins
#         width = visualization.width()
#         height = visualization.height()
#         margins = visualization.contentsMargins()
#         
#         # Subtract the top and left margins from the widget's size
#         layoutWidth = width - margins.left()
#         layoutHeight = height - margins.top()
#         
#         # Calculate x and y as percentages of the widget size
#         x = xCoordinate / layoutWidth
#         y = yCoordinate / layoutHeight
# 
#         #self.cursor_position_label.setText("Cursor position: ({:.2f}%, {:.2f}%)".format(x * 100, y * 100))
# 
#         # Convert x and y to row and column indices
#         row = int(y * (visualization.nRows - 1))
#         col = int(x * (visualization.nColumns - 1))
#         
# =============================================================================

        self.MouseHandles.MoveHandler(xCoordinate, yCoordinate)        