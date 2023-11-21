# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 15:40:06 2022

@author: Derek Joslin
"""

from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc

import RomVisualizationHandler as rh
import DefaultRomVisualizationHandles as drvh
import NewRomVisualizationHandles as nrvh

import BasicRomVisualizationHandles as brvh

class RomVisualization(qw.QDialog):
    
    def __init__(self, interruptDictionary):
        super().__init__()
        #put a main window in the QDialog and add elements to the main window
        
        # create a mainwindow
        self.RomExplorer = qw.QMainWindow()
        RomExplorerLayout = self.RomExplorer.layout()
        print(RomExplorerLayout.itemAt(0))
        # create the qt layout to attach to the mainwindow
        self.RomLayout = qw.QHBoxLayout()
        
        # add the RomExplorer to the layout
        self.RomLayout.addWidget(self.RomExplorer)
        self.setLayout(self.RomLayout)
        
        # initialize the BasicRomVisualizationHandles class
        #self.VisualizationHandles = brvh.SlidesVisualizationHandles(interruptDictionary, self.RomWindow)
        
        # initialize the NewRomVisualizationHandles class
        #self.VisualizationHandles = nrvh.NewRomVisualizationHandles()
        
        # initialize the RomVisualizationHandles class
        self.VisualizationHandles = drvh.DefaultRomVisualizationHandles()
        
        # initialize the RomVisualizationHandler class
        self.VisualizationHandler = rh.RomVisualizationHandler(self.VisualizationHandles, self)
        
        # run the intialization functions for the VisualizationHandler
        self.generateWindow()
        
    def regenerateWindow(self):
        # clear the RomWindow
        # Remove all widgets from the layout
        print("Regenerate Window")
        RomExplorerLayout = self.RomExplorer.layout()
        
        widgets = []
        print(RomExplorerLayout.count())
        print(RomExplorerLayout.itemAt(0))
        while RomExplorerLayout.itemAt(0) != None:
            widget = RomExplorerLayout.itemAt(0).widget()
            RomExplorerLayout.removeWidget(widget)
            widgets.append(widget)
        
        # Delete the widgets
        for widget in widgets:
            widget.deleteLater()
        
        # create new RomWindow elements
# =============================================================================
#         self.RomWindow = qw.QMainWindow()
#         self.RomLayout.addWidget(self.RomWindow)
#         self.setLayout(self.RomLayout)
# =============================================================================
        
        self.generateWindow()
        
    def generateWindow(self):
        # add visual elements
        self.VisualizationHandler.createActions()
        self.VisualizationHandler.createButtons()
        self.VisualizationHandler.createWidgets()
        self.VisualizationHandler.createMenuBar()
        self.VisualizationHandler.createToolBars()
        self.VisualizationHandler.connectControls()
        self.VisualizationHandler.setStyles()
        