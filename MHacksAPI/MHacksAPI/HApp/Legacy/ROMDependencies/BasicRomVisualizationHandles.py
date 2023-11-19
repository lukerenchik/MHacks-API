# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 12:48:13 2022

@author: Derek Joslin
"""

from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc

import DefaultRomVisualizationHandles as dh

class BasicRomVisualizationHandles(dh.DefaultRomVisualizationHandles):
    
    def __init__(self, interruptDictionary, RomExplorer):
        self.interruptDictionary = interruptDictionary
        self.RomExplorer = RomExplorer
        self.RomExplorer.setWindowTitle("Interrupt Control Panel")
        
    
    def createButtonsHandler(self):
        print("Basic interrupt dictionary buttons")
        self.escapeButton = qw.QPushButton('escape')
        self.escapeButton.move(25,25)
        self.continueButton = qw.QPushButton('continue')
        self.continueButton.move(25,75)
        self.endButton = qw.QPushButton('end')
        self.endButton.move(25,125)
        self.stopSerial = qw.QPushButton('stop serial')
        self.stopSerial.move(25,175)
        self.isSerialHalted = qw.QPushButton('print interrupt dictionary')
        self.isSerialHalted.move(25,225)
        
        self.escapeButton.clicked.connect(lambda: self.button("romEscape"))
        self.continueButton.clicked.connect(lambda: self.button("romContinue"))
        self.endButton.clicked.connect(lambda: self.button("romEnd"))
        self.stopSerial.clicked.connect(lambda: self.button("romHaltSerial"))
        self.isSerialHalted.clicked.connect(lambda: self.serialHalted())


    def createToolsHandler(self):
        print("Basic interrupt dictionary ToolBar")
        # Create a QToolBar
        self.toolbar = qw.QToolBar("Interrupt Dictionary ToolBar",self.RomExplorer)
    
        # Add the buttons to the toolbar
        self.toolbar.addWidget(self.escapeButton)
        self.toolbar.addWidget(self.continueButton)
        self.toolbar.addWidget(self.endButton)
        self.toolbar.addWidget(self.stopSerial)
        self.toolbar.addWidget(self.isSerialHalted)
        self.toolbar.setIconSize(qc.QSize(50,50))
        self.toolbar.setMovable(False)

        # Add the toolbar to the Rom window
        self.RomExplorer.addToolBar(self.toolbar)


        
    def button(self, keyword):
        if self.interruptDictionary[keyword]:
            self.interruptDictionary[keyword] = 0
        else:
            self.interruptDictionary[keyword] = 1
            
        if not ((keyword == 'romHaltSerial') or (keyword == 'romEnd')):
            qc.QTimer.singleShot(50, lambda: self.interruptOff(keyword))
            
        
    def interruptOff(self, keyword):
        self.interruptDictionary[keyword] = 0
            
    def serialHalted(self):
        print(self.interruptDictionary)

    def stopRom(self):
        self.endRom[0] = not self.endRom[0]
        
    def haltRom(self):
        self.interruptDictionary['romHaltSerial'] = 1
        #print(self.interruptDictionary)
        
    def resumeRom(self):
        self.interruptDictionary['romHaltSerial'] = 0
        #print(self.interruptDictionary)
        
        
    def createRomSettingsDialog(self):
        pass
        
# =============================================================================
#     
# 
# class SlidesVisualizationHandles(dh.DefaultRomVisualizationHandles):
#     
#     def __init__(self, interruptDictionary, RomExplorer):
#         super().__init__()
#         self.interruptDictionary = interruptDictionary
#         self.RomExplorer = RomExplorer
#         self.RomExplorer.setWindowTitle("Slides Rom Window")
#         
#         self.nSlides = 0
#         self.slidesDictionary = {}
#         
#     
#     def createActionsHandler(self):
#         # create qw.QAction objects here and use QAction.triggered.connect to connect custom functions
#         self.RomExplorer.loadAction = qw.QAction("Load", self.RomExplorer)
#         #self.RomExplorer.loadAction.triggered.connect(self.RomExplorer.loadFile)
#         self.RomExplorer.saveAction = qw.QAction("Save", self.RomExplorer)
#         #self.RomExplorer.saveAction.triggered.connect(self.RomExplorer.saveFile)
#         
#     def createButtonsHandler(self):
#         # create qw.QPushButton objects here and use QPushButton.triggered.connect to connect custom functions
#         self.RomExplorer.dotButton = qw.QPushButton("Dot", self.RomExplorer)
#         #self.RomExplorer.dotButton.triggered.connect(self.RomExplorer.drawDot)
#         self.RomExplorer.lineButton = qw.QPushButton("Line", self.RomExplorer)
#         #self.RomExplorer.lineButton.triggered.connect(self.RomExplorer.drawLine)
#         self.RomExplorer.curveButton = qw.QPushButton("Curve", self.RomExplorer)
#         #self.RomExplorer.curveButton.triggered.connect(self.RomExplorer.drawCurve)
#         self.RomExplorer.circleButton = qw.QPushButton("Circle", self.RomExplorer)
#         #self.RomExplorer.circleButton.triggered.connect(self.RomExplorer.drawCircle)
#         self.RomExplorer.rectangleButton = qw.QPushButton("Rectangle", self.RomExplorer)
#         #self.RomExplorer.rectangleButton.triggered.connect(self.RomExplorer.drawRectangle)
#         self.RomExplorer.triangleButton = qw.QPushButton("Triangle", self.RomExplorer)
#         #self.RomExplorer.triangleButton.triggered.connect(self.RomExplorer.drawTriangle)
#         self.RomExplorer.polygonButton = qw.QPushButton("Polygon", self.RomExplorer)
#         #self.RomExplorer.polygonButton.triggered.connect(self.RomExplorer.drawPolygon)
#         self.RomExplorer.clearButton = qw.QPushButton("Clear", self.RomExplorer)
#         #self.RomExplorer.clearButton.triggered.connect(self.RomExplorer.clear)
#         self.RomExplorer.addSlideButton = qw.QPushButton("Add Slide", self.RomExplorer)
#         self.RomExplorer.addSlideButton.clicked.connect(lambda: self.RomExplorer.addSlide(self.nSlides + 1))
#         self.RomExplorer.removeSlideButton = qw.QPushButton("Remove Slide", self.RomExplorer)
#         self.RomExplorer.removeSlideButton.clicked.connect(lambda: self.RomExplorer.removeSlide(self.nSlides))
#         
#         
#         # create the "Input ToggleSwitch" button
#         self.RomExplorer.inputButton = qw.QPushButton("Input")
#         #self.RomExplorer.inputButton.clicked.connect(self.RomExplorer.toggleInput)
# 
#         # create the "Fill ToggleSwitch" button
#         self.RomExplorer.fillButton = qw.QPushButton("Fill")
#         #self.RomExplorer.fillButton.clicked.connect(self.RomExplorer.toggleFill)
# 
#         # create the "Direct ToggleSwitch" button
#         self.RomExplorer.directButton = qw.QPushButton("Direct")
#         #self.RomExplorer.directButton.clicked.connect(self.RomExplorer.toggleDirect)
# 
#         # create the "Stroke Size Scrollwheel" button
#         self.RomExplorer.strokeButton = qw.QPushButton("Stroke")
#         #self.RomExplorer.strokeButton.clicked.connect(self.RomExplorer.adjustStrokeSize)
# 
#         # create the "Refresh Button" button
#         self.RomExplorer.refreshButton = qw.QPushButton("Refresh")
#         #self.RomExplorer.refreshButton.clicked.connect(self.RomExplorer.refresh)
#         
#     def createWidgetsHandler(self):
#         # create the "Stroke Size Scrollwheel" widget
#         
#         self.RomExplorer.strokeSize = qw.QSpinBox()
#         self.RomExplorer.strokeSize.setMinimum(1)
#         self.RomExplorer.strokeSize.setMaximum(10)
#         self.RomExplorer.strokeSize.setValue(1)
#         #self.RomExplorer.strokeSize.valueChanged.connect(self.RomExplorer.adjustStrokeSize)
# 
#         
#     def createToolsHandler(self):
#         # create qw.QToolBar objects here and use QToolBar.addWidget to add QPushButton widgets
#         self.RomExplorer.leftToolBar = qw.QToolBar("Left Toolbar", self.RomExplorer)
#         self.RomExplorer.leftToolBar.addWidget(self.RomExplorer.dotButton)
#         self.RomExplorer.leftToolBar.addWidget(self.RomExplorer.lineButton)
#         self.RomExplorer.leftToolBar.addWidget(self.RomExplorer.curveButton)
#         self.RomExplorer.leftToolBar.addWidget(self.RomExplorer.circleButton)
#         self.RomExplorer.leftToolBar.addWidget(self.RomExplorer.rectangleButton)
#         self.RomExplorer.leftToolBar.addWidget(self.RomExplorer.triangleButton)
#         self.RomExplorer.leftToolBar.addWidget(self.RomExplorer.polygonButton)
#         self.RomExplorer.leftToolBar.addWidget(self.RomExplorer.clearButton)
#         self.RomExplorer.leftToolBar.addWidget(self.RomExplorer.addSlideButton)
#         self.RomExplorer.leftToolBar.addWidget(self.RomExplorer.removeSlideButton)
#         self.RomExplorer.leftToolBar.setIconSize(qc.QSize(50,50))
#         self.RomExplorer.leftToolBar.setMovable(False)
#         self.RomExplorer.addToolBar(qc.Qt.LeftToolBarArea, self.RomExplorer.leftToolBar)
# 
#         # create the top toolbar
#         self.RomExplorer.topToolBar = qw.QToolBar("Top Toolbar", self.RomExplorer)
#         self.RomExplorer.topToolBar.addWidget(self.RomExplorer.inputButton)
#         self.RomExplorer.topToolBar.addWidget(self.RomExplorer.fillButton)
#         self.RomExplorer.topToolBar.addWidget(self.RomExplorer.directButton)
#         self.RomExplorer.topToolBar.addWidget(self.RomExplorer.strokeButton)
#         self.RomExplorer.topToolBar.addWidget(self.RomExplorer.strokeSize)
#         self.RomExplorer.topToolBar.setIconSize(qc.QSize(50,50))
#         self.RomExplorer.topToolBar.setMovable(False)
#         self.RomExplorer.addToolBar(qc.Qt.TopToolBarArea, self.RomExplorer.topToolBar)
#         
#         self.RomExplorer.rightToolBar = qw.QToolBar("Right Toolbar", self.RomExplorer)
#         self.RomExplorer.addToolBar(qc.Qt.RightToolBarArea, self.RomExplorer.rightToolBar)
#         
#     def createMenuHandler(self):
#         # create the File menu
#         self.RomExplorer.fileMenu = qw.QMenu('File')
#         self.RomExplorer.menuBar().addMenu(self.RomExplorer.fileMenu)
# 
#         # add the load and save actions to the File menu
#         self.RomExplorer.fileMenu.addAction(self.RomExplorer.loadAction)
#         self.RomExplorer.fileMenu.addAction(self.RomExplorer.saveAction)
#         pass
#         
#     def loadFile(self):
#         # load a file here
#         pass
#     
#     def saveFile(self):
#         # save a file here
#         pass
#     
#     def addSlide(self, slideNum):
#         # adds QPushButton to self.RomExplorer.rightToolBar
#         self.RomExplorer.nSlides += 1
#         slideString = "Slide {}".format(slideNum)
#         
#         # creates a QPushButton instance for this slide
#         button = qw.QPushButton(slideString, self)
#         button.clicked.connect(lambda: self.loadSlide(slideNum))
#         
#         # adds the push button to the slides dictionary and rightToolBar
#         buttonAction = self.RomExplorer.rightToolBar.addWidget(button)
#         self.RomExplorer.slidesDictionary[slideString] = buttonAction
#         
#     def removeSlide(self, slideNum):
#         # removes a QPushButton from self.RomExplorer.rightToolBar depending on the slide num
#         
#         if self.nSlides > 0:
#             slideString = "Slide {}".format(slideNum)
#             self.nSlides -= 1
#             
#             # remove widget from the rightToolBar
#             self.rightToolBar.removeAction(self.slidesDictionary[slideString])
#             
#             # delete the dictionary instance
#             del self.slidesDictionary[slideString]
#         else:
#             # all slides gone
#             pass
#     
#     def loadSlide(self, slideNum):
#         
#         print("slide{}".format(slideNum))
#   
#   
# =============================================================================
