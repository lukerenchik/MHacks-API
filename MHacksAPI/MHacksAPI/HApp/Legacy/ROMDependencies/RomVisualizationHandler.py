# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 11:27:42 2022

@author: Derek Joslin
"""


class RomVisualizationHandler():
    
    def __init__(self, RomVisualizationHandles, RomWindow):
        
        self.RomWindow = RomWindow
        self.DefaultRomVisualizationHandles = RomVisualizationHandles
        self.RomVisualizationHandles = RomVisualizationHandles
        
    def setNewRomVisualizationHandler(self, RomVisualizationHandles):
        
        self.RomVisualizationHandles = RomVisualizationHandles
        self.RomWindow.regenerateWindow()
        
    def revertToDefaultHandler(self):
        self.RomVisualizationHandles = self.DefaultRomVisualizationHandles
        self.RomWindow.regenerateWindow()
        
    def createActions(self):
        self.RomVisualizationHandles.createActionsHandler()
        
    def createButtons(self):
        self.RomVisualizationHandles.createButtonsHandler()
        
    def createWidgets(self):
        self.RomVisualizationHandles.createWidgetsHandler()
        
    def createMenuBar(self):
        self.RomVisualizationHandles.createMenuHandler()
        
    def createToolBars(self):
        self.RomVisualizationHandles.createToolsHandler()
        
    def connectControls(self):
        self.RomVisualizationHandles.connectControlsHandler()
        
    def setStyles(self):
        self.RomVisualizationHandles.setStylesHandler()