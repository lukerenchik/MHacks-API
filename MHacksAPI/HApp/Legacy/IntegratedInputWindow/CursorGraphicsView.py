# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 09:37:21 2022

@author: Derek Joslin
"""

from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc
import CursorGraphicsScene




class CursorGraphicsView(qw.QGraphicsView):
    
    def __init__(self, nhAPI,widget):# widgetList
        super().__init__()
        
        
        self.NHAPI = nhAPI
        self.inputCursorPosition = self.NHAPI.getInputCursorPosition()
        self.widget = widget
        
        #self.DesiredStateInputGrid = DesiredStateButtonInputWidgetv4.DesiredStateButtonInputWidget(nhAPI)
        self.scene = CursorGraphicsScene.CursorGraphicsScene(-30)
        
        #read in all widgets to put in the view
        sceneWidth = self.width()
        sceneHeight = self.height()
        self.scene.addWidget(widget)
        widget.resize(sceneWidth,sceneHeight)
        for pin in widget.pinList:
            pin.pressed.connect(lambda: self.stopVisual())
            pin.released.connect(lambda: self.startVisual())
    
        
        self.scene.changeSize(sceneWidth, sceneHeight)
        self.scene.drawCursor()
        
        self.setScene(self.scene)
        
        self.setWindowTitle("Real Time Input Visualizer")
        
        self.startVisual()
        
        
        #self.show()
        
        

    def startVisual(self):
        # Repeating timer, calls random_pick over and over.
        self.grabFirmwareStateTimer = qc.QTimer()
        self.grabFirmwareStateTimer.setInterval(25)
        self.grabFirmwareStateTimer.timeout.connect(self.grabCursorPosition)
        self.grabFirmwareStateTimer.start()
        # Single oneshot which stops the selection after 5 seconds
        # qc.QTimer.singleShot(5000, self.stopVisual)

    def stopVisual(self):
        # Stop the random selection
        self.grabFirmwareStateTimer.stop()
        # The current pick is in self.current_selection


    def grabCursorPosition(self):
        self.stopVisual()
        
        # Store the current selection, so we have it at the end in stop_selection.
        self.inputCursorPosition = self.NHAPI.getInputCursorPosition()
        self.inputCursorDimensions = self.NHAPI.getInputCursorDimensions()
        
        #update the displaySize
        #self.re
        
        
        self.scene.updateCursorPosition(self.inputCursorDimensions, self.inputCursorPosition, self.width() - 25, self.height() - 25)
        
        #press the pin button at that value
        #self.widgetList[0].pinList[5].clicked.emit()
        
        #print(self.inputCursorPosition)
        
        self.startVisual()
        
        
    def resizeEvent(self, e):
        sceneWidth = self.width()
        sceneHeight = self.height()
        self.widget.resize(sceneWidth,sceneHeight)
        
        #print("----------")
        #print(layoutWidth)
        #print(layoutHeight)
        #print("----------")
        
        self.scene.changeSize(sceneWidth, sceneHeight)