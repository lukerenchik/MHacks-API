# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 09:36:23 2022

@author: Derek Joslin
"""

from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc




class CursorGraphicsScene(qw.QGraphicsScene):

    def __init__(self, margin):
        super().__init__()
        self.viewMarginSize = margin        
        
    def drawCursor(self):
        self.cursorGraphic = self.addRect(CursorGraphic(-10,-10,10,10), qg.QPen(qc.Qt.red), qg.QBrush(qc.Qt.red));


    def updateCursorPosition(self, cursorDimensions, cursorPosition, sceneWidth, sceneHeight):
        
        
        cursorWidth = cursorDimensions[0]
        cursorHeight = cursorDimensions[1]
        
        cursorXPosition = cursorPosition[0]
        cursorYPosition = cursorPosition[1]
        
        cursorXPositionPercentage = cursorXPosition/cursorWidth
        cursorYPositionPercentage = cursorYPosition/cursorHeight
        
        sceneXPosition = sceneWidth*cursorXPositionPercentage
        sceneYPosition = sceneHeight*cursorYPositionPercentage
        
        """
        print("----------")
        print(cursorPosition)
        print(sceneWidth)
        print(sceneHeight)
        print((sceneXPosition, sceneYPosition))
        print("----------")
        """
        
        self.cursorGraphic.setPos(sceneXPosition + 20, sceneYPosition + 20)
        
    def changeSize(self, sceneWidth,sceneHeight):
        self.setSceneRect(15,15,sceneWidth + self.viewMarginSize, sceneHeight + self.viewMarginSize)
        
        
class CursorGraphic(qc.QRectF):
    
    def __init__(self, xPosition, yPosition, width, height):
        super().__init__(xPosition, yPosition, width, height)
        
        
    def paintEvent(self, event):
        super().paintEvent(event)