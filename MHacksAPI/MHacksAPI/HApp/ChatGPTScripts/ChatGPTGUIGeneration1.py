# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 14:10:45 2022

@author: derek
"""

from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc
import sys

class AppVisualization(qw.QDialog):

    def __init__(self, parent = None):
        super().__init__(parent)
        
        # slides dictionary for storing slide data
        self.nSlides = 0
        self.slidesDictionary = {}
        
        # create a mainwindow
        self.mainWindow = qw.QMainWindow()
        
        # create the qt layout to attach to the mainwindow
        self.layout = qw.QHBoxLayout()
        
        # add the layout to the mainwindow
        self.layout.addWidget(self.mainWindow)
        self.setLayout(self.layout)
        
        # create the GUI objects
        self.createActions()
        self.createButtons()
        self.createWidgets()
        self.createMenuBar()
        self.createToolBars()
        self.mainWindow.clear()
        self.show()
        

    def createActions(self):
        # create qw.QAction objects here and use QAction.triggered.connect to connect custom functions
        self.loadAction = qw.QAction("Load", self)
        #self.loadAction.triggered.connect(self.loadFile)
        self.saveAction = qw.QAction("Save", self)
        #self.saveAction.triggered.connect(self.saveFile)

    def createButtons(self):
        # create qw.QPushButton objects here and use QPushButton.triggered.connect to connect custom functions
        self.dotButton = qw.QPushButton("Dot", self)
        #self.dotButton.triggered.connect(self.drawDot)
        self.lineButton = qw.QPushButton("Line", self)
        #self.lineButton.triggered.connect(self.drawLine)
        self.curveButton = qw.QPushButton("Curve", self)
        #self.curveButton.triggered.connect(self.drawCurve)
        self.circleButton = qw.QPushButton("Circle", self)
        #self.circleButton.triggered.connect(self.drawCircle)
        self.rectangleButton = qw.QPushButton("Rectangle", self)
        #self.rectangleButton.triggered.connect(self.drawRectangle)
        self.triangleButton = qw.QPushButton("Triangle", self)
        #self.triangleButton.triggered.connect(self.drawTriangle)
        self.polygonButton = qw.QPushButton("Polygon", self)
        #self.polygonButton.triggered.connect(self.drawPolygon)
        self.clearButton = qw.QPushButton("Clear", self)
        #self.clearButton.triggered.connect(self.clear)
        self.addSlideButton = qw.QPushButton("Add Slide", self)
        self.addSlideButton.clicked.connect(lambda: self.addSlide(self.nSlides + 1))
        self.removeSlideButton = qw.QPushButton("Remove Slide", self)
        self.removeSlideButton.clicked.connect(lambda: self.removeSlide(self.nSlides))
        
        
        # create the "Input ToggleSwitch" button
        self.inputButton = qw.QPushButton("Input")
        #self.inputButton.clicked.connect(self.toggleInput)

        # create the "Fill ToggleSwitch" button
        self.fillButton = qw.QPushButton("Fill")
        #self.fillButton.clicked.connect(self.toggleFill)

        # create the "Direct ToggleSwitch" button
        self.directButton = qw.QPushButton("Direct")
        #self.directButton.clicked.connect(self.toggleDirect)

        # create the "Stroke Size Scrollwheel" button
        self.strokeButton = qw.QPushButton("Stroke")
        #self.strokeButton.clicked.connect(self.adjustStrokeSize)

        # create the "Refresh Button" button
        self.refreshButton = qw.QPushButton("Refresh")
        #self.refreshButton.clicked.connect(self.refresh)

    def createWidgets(self):
        # create the "Stroke Size Scrollwheel" widget
        self.strokeSize = qw.QSpinBox()
        self.strokeSize.setMinimum(1)
        self.strokeSize.setMaximum(10)
        self.strokeSize.setValue(1)
        #self.strokeSize.valueChanged.connect(self.adjustStrokeSize)

    def createToolBars(self):
        # create qw.QToolBar objects here and use QToolBar.addWidget to add QPushButton widgets
        self.leftToolBar = qw.QToolBar("Left Toolbar", self)
        self.leftToolBar.addWidget(self.dotButton)
        self.leftToolBar.addWidget(self.lineButton)
        self.leftToolBar.addWidget(self.curveButton)
        self.leftToolBar.addWidget(self.circleButton)
        self.leftToolBar.addWidget(self.rectangleButton)
        self.leftToolBar.addWidget(self.triangleButton)
        self.leftToolBar.addWidget(self.polygonButton)
        self.leftToolBar.addWidget(self.clearButton)
        self.leftToolBar.addWidget(self.addSlideButton)
        self.leftToolBar.addWidget(self.removeSlideButton)
        self.leftToolBar.setIconSize(qc.QSize(50,50))
        self.leftToolBar.setMovable(False)
        self.mainWindow.addToolBar(qc.Qt.LeftToolBarArea, self.leftToolBar)


        # create the top toolbar
        self.topToolBar = qw.QToolBar("Top Toolbar", self)
        self.topToolBar.addWidget(self.inputButton)
        self.topToolBar.addWidget(self.fillButton)
        self.topToolBar.addWidget(self.directButton)
        self.topToolBar.addWidget(self.strokeButton)
        self.topToolBar.addWidget(self.strokeSize)
        self.topToolBar.setIconSize(qc.QSize(50,50))
        self.topToolBar.setMovable(False)
        self.mainWindow.addToolBar(qc.Qt.TopToolBarArea, self.topToolBar)
        
        self.rightToolBar = qw.QToolBar("Right Toolbar", self)
        self.mainWindow.addToolBar(qc.Qt.RightToolBarArea, self.rightToolBar)
# =============================================================================
#         self.rightToolBar.addSlide(1)
#         self.rightToolBar.addSlide(2)
#         self.rightTool
# =============================================================================

    def createMenuBar(self):
        # create the File menu
        fileMenu = self.mainWindow.menuBar().addMenu('File')

        # add the load and save actions to the File menu
        fileMenu.addAction(self.loadAction)
        fileMenu.addAction(self.saveAction)

    def loadFile(self):
        # load a file here
        pass

    def saveFile(self):
        # save a file here
        pass

    def addSlide(self, slideNum):
        # adds QPushButton to self.rightToolBar
        self.nSlides += 1
        slideString = "Slide {}".format(slideNum)
        
        # creates a QPushButton instance for this slide
        button = qw.QPushButton(slideString, self)
        button.clicked.connect(lambda: self.loadSlide(slideNum))
        
        # adds the push button to the slides dictionary and rightToolBar
        buttonAction = self.rightToolBar.addWidget(button)
        self.slidesDictionary[slideString] = buttonAction
        
    def removeSlide(self, slideNum):
        # removes a QPushButton from self.rightToolBar depending on the slide num
        
        if self.nSlides > 0:
            slideString = "Slide {}".format(slideNum)
            self.nSlides -= 1
            
            # remove widget from the rightToolBar
            self.rightToolBar.removeAction(self.slidesDictionary[slideString])
            
            # delete the dictionary instance
            del self.slidesDictionary[slideString]
        else:
            # all slides gone
            pass

    def loadSlide(self, slideNum):
        
        print("slide{}".format(slideNum))
        
        
        
if __name__ == '__main__':
    
    app = qw.QApplication([])
    
    MainWindow = AppVisualization()
    
    
    
    sys.exit(app.exec_())
    