# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 09:18:57 2022

@author: Derek Joslin

"""

from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc

import FileManagement as fm
import PathManager
import ComFinder as cf

import APIConsole as ac

import KeyboardPeripheral as kb
import HAppKeyboardHandles as hk
import DefaultKeyboardHandles as dk

import MousePeripheral as mh
import HAppMouseHandles as hm
import DefaultMouseHandles as dm

import RomVisualizationHandler as rh
import DefaultRomVisualizationHandles as drvh

import NHAPI as nh
#import ToggleSwitch as ts

import TouchStateVisualizer as tsv
import RealTimeStateVisualizer as rtsv

import HAppOperations as ho
import ControlCenter as cc
import RomOperation as ro
import RomLauncher as rl

import RomVisualization as rv

import sys

import time

""" HApp MainWindow """

class HAppMainWindow(qw.QMainWindow):
    
    """ intialization functions """

    def __init__(self, PathManager, parent = None):
        
        self.flashSplash()
        super().__init__(parent)
        
        # set the mouse cursor to always be tracked
        self.setMouseTracking(True)
        self.setAttribute(qc.Qt.WA_TransparentForMouseEvents, True)
        
        # Set the cursor to be a red dot
        pixmap = qg.QPixmap(7.5, 7.5)
        pixmap.fill(qg.QColor(255, 0, 0))
        self.setCursor(qg.QCursor(pixmap))
        
        # get the margin for cursor tracking
        self.margins = self.layout().contentsMargins()
        
        # an extra widget
        
        self.ARCSLabel = qw.QLabel(self)#qw.QWidget(self)
        
        self.ARCSDock = qw.QDockWidget("ARCS Monitor", self, qc.Qt.Widget)
        self.ARCSDock.setWidget(self.ARCSLabel)
        self.addDockWidget(qc.Qt.RightDockWidgetArea, self.ARCSDock, qc.Qt.Vertical)
        
# =============================================================================
#         self.TactileDisplay.connect("COM12", 0)
#         self.TactileDisplay.connectTouch("COM7")
# =============================================================================
        
        # display and define logo
        FCIcon = qg.QIcon(":main_symbol")
        HELogo = qg.QPixmap(":HE_logo")
        HELogo = HELogo.scaled(175,175, qc.Qt.KeepAspectRatio)
        
        # self.color = style
        self.setStyleSheet("border: 1px solid blue;")
        
# =============================================================================
#         style guide
#         rgb(85,216,211) -> light turquoise
#         rgb(41,178,170) -> dark turquoise
#         rgb(37,64,143) -> reflex blue
#         rgb(65,67,77) -> persian nights
# =============================================================================
        
        # Create window
        self.setWindowTitle("HApp Main Window")
        self.setWindowIcon(FCIcon)
        
        # Create status bar with the status and haptic engine
        self.statusBar = qw.QStatusBar()
        self.setStatusBar(self.statusBar)
        
        # Create the ARCS Control Center
        self.HAppControlCenter = cc.ControlCenter(PathManager)
        self.HAppPathManager = self.HAppControlCenter.PathManager
        
        # Build a default keyboard
        self.DefaultKeyboardHandles = dk.DefaultKeyboardHandles()
        self.KeyboardPeripheral = kb.KeyboardPeripheral("Master Keyboard", self.DefaultKeyboardHandles)
        
        # add the Keyboard to the control center
        self.HAppControlCenter.addPeripheral(self.KeyboardPeripheral)
        
        # Build a default mouse
        self.DefaultMouseHandles = dm.DefaultMouseHandles()
        self.MousePeripheral = mh.MousePeripheral("Master Mouse", self.DefaultMouseHandles)
        
        # add the Mouse to the control center
        self.HAppControlCenter.addPeripheral(self.MousePeripheral)
        
        # create window elements
        self.__createActions()
        self.__createMenuBar()
        
        # update the ARCS status label
        self.UpdateMonitorOperation = cc.UpdateMonitorOperation("UpdateMonitorOperation", self.HAppControlCenter, self.ARCSLabel)
        self.HAppControlCenter.addOperation(self.UpdateMonitorOperation)
        
        # begin executing HApp operations
        self.HAppControlCenter.startLaunchingOperations(2)
        
        #qc.QTimer.singleShot(2000, lambda: self.quickConnect())
        
    def quickConnect(self):
        # ease of use
        self.connectDisplay("COM12")
        #qc.QTimer.singleShot(1000, lambda: self.connectTouchscreen("COM34"))
        #qc.QTimer.singleShot(2000, lambda: self.connectTouchscreen("COM7"))
        #ARCSLayout = self.HAppControlCenter.debugGetResourceLabels()
        #self.ARCSLabel.setLayout(ARCSLayout)
        
    def flashSplash(self):
        FCLogo = qg.QPixmap(":main_logo")
        FCLogo = FCLogo.scaled(1000,1000)
        
        self.splash = qw.QSplashScreen(FCLogo)
        
        # By default, SplashScreen will be in the center of the screen.
        # You can move it to a specific location if you want:
        # self.splash.move(10,10)
        
        self.splash.show()
        
        # Close SplashScreen after 2 seconds (2000 ms)
        qc.QTimer.singleShot(2000, self.splash.close)
        
        
    """ Keyboard related functions """
    
    def keyPressEvent(self, event):
        event.ignore()
        
        # Connect to KeyboardPeripheral class key press event
        self.KeyboardPeripheral.handleKeyPressEvent(event)
        
    def keyReleaseEvent(self, event):
        event.ignore()
        
        # Connect to KeyboardPeripheral class key release event
        self.KeyboardPeripheral.handleKeyReleaseEvent(event)
        
    """ Mouse related functions """
    
    def mouseMoveEvent(self, event):
        event.ignore()
        
        # Handle mouse movements using the event handlers assigned to the peripheral
        self.MousePeripheral.handleMouseMoveEvent(event)

    def mousePressEvent(self, event):
        event.ignore()
        
        # Handle the mouse press event using the handlers in the peripheral
        self.MousePeripheral.handleMouseEvent(event)
        
    """ actions which can be performed when selecting options """
        
    def __createActions(self):
        #create the icons for the tools
        fillIcon = qg.QIcon(":fill")
        strokeIcon = qg.QIcon(":stroke")
        refreshIcon = qg.QIcon(":refresh")
        eraseIcon = qg.QIcon(":erase")
        FclearIcon = qg.QIcon(":Fclear")
        dotIcon = qg.QIcon(":dot")
        cellIcon = qg.QIcon(":braille")
        lineIcon = qg.QIcon(":line")
        curveIcon = qg.QIcon(":curve")
        circleIcon = qg.QIcon(":circle")
        rectIcon = qg.QIcon(":square")
        triangleIcon = qg.QIcon(":triangle")
        polygonIcon = qg.QIcon(":polygon")
        brailleIcon = qg.QIcon(":braille")
        txtsizeIcon = qg.QIcon(":textTitle")


        #cursor tools
        self.erase = qw.QAction("Input", self)
        self.erase.triggered.connect(lambda: self.__toolSelected("erase","({on/off-E})"))
        self.fill = qw.QAction(fillIcon, "Fill", self)
        self.fill.triggered.connect(lambda: self.__toolSelected("fill","({on/off-F})"))
        self.stroke = qw.QAction(strokeIcon, "Stroke", self)
        self.stroke.triggered.connect(lambda: self.__toolSelected("stroke","({stroke size})"))

        #shape tools
        self.dot = qw.QAction(dotIcon, "Dot", self)
        self.dot.setIconText("Dot")
        self.dot.triggered.connect(lambda: self.__toolSelected("dot","({coord1})"))
        self.cell = qw.QAction(cellIcon, "cell", self)
        self.cell.setIconText("Cell")
        self.cell.triggered.connect(lambda: self.__toolSelected("cell","({coord1})"))
        self.line = qw.QAction(lineIcon, "Line", self)
        self.line.triggered.connect(lambda: self.__toolSelected("line","({coord2},{coord1})"))
        self.curve = qw.QAction(curveIcon, "Curve", self)
        self.curve.triggered.connect(lambda: self.__toolSelected("curve","({coord4},{coord3},{coord2},{coord1})"))
        self.circle = qw.QAction(circleIcon, "Circle", self)
        self.circle.triggered.connect(lambda: self.__toolSelected("circle","({coord1},{radius})"))
        self.rect = qw.QAction(rectIcon, "Rect", self)
        self.rect.triggered.connect(lambda: self.__toolSelected("rect","({coord2},{coord1})"))
        self.triangle = qw.QAction(triangleIcon, "Triangle", self)
        self.triangle.triggered.connect(lambda: self.__toolSelected("triangle","({coord3},{coord2},{coord1})"))
        self.polygon = qw.QAction(polygonIcon, "Polygon", self)
        self.polygon.triggered.connect(lambda: self.__toolSelected("polygon","({list1})"))

        #character tools
        self.braille = qw.QAction(brailleIcon, "Braille", self)
        #self.braille.triggered.connect(lambda: self.__toolSelected("braille","({coord1},{text})"))
        #self.brailleBox = qw.QLineEdit(self)
        #self.brailleBox.setMaximumWidth(100)
        
# =============================================================================
#         def toolType():
#             if not self.__commandDict["command"] == "latin":
#                 self.__toolSelected("braille","({coord1},{text})")
# =============================================================================

        #self.brailleBox.textChanged.connect(toolType)
        #self.brailleBox.textChanged.connect(lambda: self.__optionUpdated("coord1", self.__coordHist[-1]))
        #self.brailleBox.textChanged.connect(lambda t: self.__optionUpdated("text", '"{0}"'.format(t)))
        #self.brailleBox.textChanged.connect(lambda t: self.__optionUpdated("font", '"Arial"'))
        
# =============================================================================
#         self.brailleBox.returnPressed.connect(lambda: self.__toolSelected("braille","({coord1},{text})"))
#         self.brailleBox.returnPressed.connect(lambda: self.__optionUpdated("coord1", self.__coordHist[-1]))
#         self.brailleBox.returnPressed.connect(lambda: self.__optionUpdated("text", '"{0}\\n"'.format(self.brailleBox.text())))
# =============================================================================

        #self.brailleBox.returnPressed.connect(lambda: self.brailleBox.insert("\\n"))

        #file actions
        self.FileManager = fm.FileManagement(self)
        
        self.saveDesired = qw.QAction("Save Desired State", self)
        self.saveDesired.triggered.connect(lambda: self.FileManager.saveFile())
        
        self.load = qw.QAction("Load", self) #self.load.triggered.connect(lambda: self.__toolSelected("setMat","({matrix})"))
        self.load.triggered.connect(lambda: self.FileManager.loadFile()) #self.load.triggered.connect(lambda: self.__optionUpdated("matrix", loadFile()))
        
        #control actions
        self.clear = qw.QAction(eraseIcon, "Clear", self)
        self.clear.triggered.connect(lambda: self.__toolSelected("clear","()"))
        
        self.Fclear = qw.QAction(FclearIcon, "Force clear", self)
        self.Fclear.triggered.connect(lambda: self.__toolSelected("Fclear","()"))
        
        self.times = qw.QAction("Times", self)
        self.times.triggered.connect(lambda: self.__toolSelected("times","({now})"))
        
# =============================================================================
#         self.timesStepper = qw.QSpinBox()
#         self.timesStepper.setRange(0,100000)
#         self.timesStepper.setSingleStep(100)
# =============================================================================

        #self.timesStepper.valueChanged.connect(lambda: self.__toolSelected("times", "({now})"))
        # self.timesStepper.valueChanged.connect(lambda: self.__optionUpdated("now", self.timesStepper.value()))
        self.setMat = qw.QAction("Set Matrix", self)
        self.setMat.triggered.connect(lambda: self.__toolSelected("setMat","({matrix})"))


        #board actions
        self.connect = qw.QAction("Connect", self)
        self.connect.triggered.connect(lambda: self.__toolSelected("connect","({com})"))

        
        self.connectTouch = qw.QAction("Connect Touch", self)
        self.connectTouch.triggered.connect(lambda: self.__toolSelected("connectTouch","({com})"))
        self.disconnect = qw.QAction("Disconnect", self)
        self.disconnect.triggered.connect(lambda: self.__toolSelected("disconnect","()"))
        self.disconnectTouch = qw.QAction("Disconnect Touch", self)
        self.disconnectTouch.triggered.connect(lambda: self.__toolSelected("disconnectTouch","()"))
        self.refresh = qw.QAction(refreshIcon, "Refresh", self)
        self.refresh.triggered.connect(lambda: self.__toolSelected("refresh","()"))
        self.direct = qw.QAction("Direct")
        self.direct.triggered.connect(lambda: self.__toolSelected("direct", "({on/off-D})"))
        self.directOn = qw.QAction("On", self)
        self.directOn.triggered.connect(lambda: self.__toolSelected("direct", '("on")'))
        self.directOff = qw.QAction("Off", self)
        self.directOff.triggered.connect(lambda: self.__toolSelected("direct", '("off")'))


        #help actions
        self.settings = qw.QAction("Settings", self)
        self.settings.triggered.connect(lambda: self.__toolSelected("settings","()"))
        self.frames = qw.QAction("Frames", self)
        self.frames.triggered.connect(lambda: self.__toolSelected("frames","()"))

        #misc actions
        self.BoardIntializer = qw.QAction("Initialize Board", self)
        self.BoardIntializer.triggered.connect(lambda: self.intializeBoard())

# =============================================================================
#         self.onOFF = qw.QPushButton("on/off")
#         self.onOFF.setCheckable(True)
#         #self.onOFF.clicked.connect(lambda: self.__optionUpdated("on/off", self.onOFF.isChecked()))
#         self.onOFF.setFocusPolicy(qc.Qt.NoFocus)
#         self.strokeLabel = qw.QLabel("stroke size")
#         self.strokeSize = qw.QSpinBox()
#         self.strokeSize.setMinimum(1)
#         #self.strokeSize.valueChanged.connect(lambda: self.__toolSelected("stroke","({stroke size})"))
#         #self.strokeSize.valueChanged.connect(lambda: self.__optionUpdated("stroke size", self.strokeSize.value()))
#         self.strokeSize.setFocusPolicy(qc.Qt.NoFocus)
#         self.space = qw.QLabel(" " * 5)
#         self.fontLabel = qw.QLabel("font size")
#         self.fontSize = qw.QSpinBox()
#         self.fontSize.setMinimum(8)
#         self.fontSize.setFocusPolicy(qc.Qt.NoFocus)
#         #self.fontSize.valueChanged.connect(lambda: self.__optionUpdated("font size", self.fontSize.value()))
#         self.space2 = qw.QLabel(" " * 5)
#         self.directOnOFF = ts.ToggleSwitch("       Direct\n\n\n")
#         self.directOnOFF.setCheckable(True)
#         #self.directOnOFF.clicked.connect(lambda: self.__toolSelected("direct", "({on/off-D})"))
#         #self.directOnOFF.clicked.connect(lambda: self.__optionUpdated("on/off-D", self.directOnOFF.isChecked()))
#         self.directOnOFF.setFocusPolicy(qc.Qt.NoFocus)
#         self.eraseOnOFF = ts.ToggleSwitch("        Input\n\n\n")
#         self.eraseOnOFF.setCheckable(True)
#         #self.eraseOnOFF.clicked.connect(lambda: self.__toolSelected("erase", "({on/off-E})"))
#         #self.eraseOnOFF.clicked.connect(lambda: self.__optionUpdated("on/off-E", self.eraseOnOFF.isChecked()))
#         self.eraseOnOFF.setFocusPolicy(qc.Qt.NoFocus)
#         self.fillOnOFF = ts.ToggleSwitch("         Fill\n\n\n")
#         self.fillOnOFF.setCheckable(True)
#         #self.fillOnOFF.clicked.connect(lambda: self.__toolSelected("fill", "({on/off-F})"))
#         #self.fillOnOFF.clicked.connect(lambda: self.__optionUpdated("on/off-F", self.fillOnOFF.isChecked()))
#         self.fillOnOFF.setFocusPolicy(qc.Qt.NoFocus)
#         self.space3 = qw.QLabel(" " * 5)
# =============================================================================
        
    """ menu related functions to loading roms """
    
    def __createMenuBar(self):
        
        menuBar = qw.QMenuBar(self)
        self.setMenuBar(menuBar)
        #create menu bars
        #file menu
        fileMenu = qw.QMenu("&File", self)
        
        #load and save actions
        fileMenu.addAction(self.load)
        
        saveMenu = qw.QMenu("Save", self)
        saveMenu.addAction(self.saveDesired)
        
        fileMenu.addMenu(saveMenu)
        
        #edit menu
        editMenu = qw.QMenu("&Edit", self)
        editMenu.addAction(self.clear)
        editMenu.addAction(self.Fclear)
        
        #help menu
        helpMenu = qw.QMenu("&Help", self)
        helpMenu.addAction(self.settings)
        
        #control menu
        controlMenu = qw.QMenu("Control",self)
        controlMenu.addAction(self.refresh)
        controlMenu.addAction(self.setMat)
        
        #board menu
        boardMenu = qw.QMenu("Board", self)
        
        #create submenu for connect with dynamic com ports
        self.DisplayConnectMenu = qw.QMenu("Connect Display", self)
        self.TouchConnectMenu = qw.QMenu("Connect Touch", self)
        self.called = 0
    
        #make a function to check the com ports create a list of com actions and add them to the connect Menu
        
        def findComs():
    # =============================================================================
    #             def getPort(port):
    #                 mystring = str(port)
    #                 return mystring
    # =============================================================================
            #get list of com ports
            self.comList = cf.serial_ports()
            print(self.comList)
            
            #delete existing actions
            self.DisplayConnectMenu.clear()
            self.TouchConnectMenu.clear()
            
# =============================================================================
#             self.displayFunctionList = [lambda x=i: self.connectDisplay(self.comList[x]) for i in range(len(self.comList))]
#             self.touchFunctionList = [lambda x=i: self.connectTouchscreen(self.comList[x]) for i in range(len(self.comList))]
# 
# =============================================================================
           
            self.displayActionList = [displayConnector(self.comList[i], self) for i in range(len(self.comList))]
            self.touchActionList = [touchConnector(self.comList[i], self) for i in range(len(self.comList))]
        
            for action in self.displayActionList:
                self.DisplayConnectMenu.addAction(action)
                
            for action in self.touchActionList:
                self.TouchConnectMenu.addAction(action)
        
# =============================================================================
#             #create action for each port on the list and add to DisplayConnectMenu
#             for action,func in zip(self.displayActionList,self.displayFunctionList):
# 
#                 def newFunc():
#                     func()
#                 
#                 action.triggered.connect(newFunc)
#                 
#                 # add these actions to the connection menu
#                 self.DisplayConnectMenu.addAction(action)
#                 #func()
#                 #print(action.text())
#                 action.trigger()
# 
#             #create action for each port on the list and add to DisplayConnectMenu
#             for action,func in zip(self.touchActionList,self.touchFunctionList):
#                 
#                 def newFunc():
#                     func()
# 
#                 action.triggered.connect(newFunc)
#                 
#                 # add these actions to the connection menu
#                 self.TouchConnectMenu.addAction(action)
#                 #func()
#                 #print(action.text())
#                 action.trigger()
# =============================================================================
                
# =============================================================================
#             for action in self.TouchConnectMenu.actions():
#                 print(action.text())
#                 
#             for action in self.DisplayConnectMenu.actions():
#                 print(action.text())
# =============================================================================
        
        self.getCOMS = qw.QAction("getcoms",self)
        self.getCOMS.triggered.connect(lambda: findComs())
        boardMenu.aboutToShow.connect(findComs)
    
        print(self.DisplayConnectMenu.actions())
        print(self.TouchConnectMenu.actions())
        
        boardMenu.addMenu(self.DisplayConnectMenu)
        boardMenu.addMenu(self.TouchConnectMenu)
    
        boardMenu.addAction(self.disconnect)
        boardMenu.addAction(self.disconnectTouch)
        boardMenu.addAction(self.refresh)
        boardMenu.addAction(self.BoardIntializer)
    
        # create submenu for direct
        directMenu = qw.QMenu("Direct", self)
        directMenu.addAction(self.directOff)
        directMenu.addAction(self.directOn)
    
        boardMenu.addMenu(directMenu)
    
        # add menu bars
        menuBar.addMenu(fileMenu)
        menuBar.addMenu(editMenu)
        menuBar.addMenu(helpMenu)
        menuBar.addMenu(controlMenu)
        menuBar.addMenu(boardMenu)
        

    """ connect the display and touch """
    def connectDisplay(self, comString):
        self.TactileDisplay = nh.NHAPI("NewHaptics Display SarissaV1")
        self.TactileDisplay.connect(comString, 0)
        
        # add the tactile display to the control center
        self.HAppControlCenter.addPeripheral(self.TactileDisplay)
        
        # get the dimensions of the display
        state = self.TactileDisplay.state()
        displaySize = self.TactileDisplay.size()
        
        self.StateVisualizer = rtsv.StateVisualizer("StateVisualizer", state, displaySize)
        
        # create an operation to constantly refresh the visualizer and add it to the controller
        self.StateVisualizerRefreshOperation = rtsv.StateVisualizerOperation("StateVisualizerRefreshOperation",  self.MousePeripheral, self.TactileDisplay, self.StateVisualizer)
        
        # Build a HApp keyboard
        self.HAppKeyboardHandles = hk.HAppKeyboardHandles(self.StateVisualizerRefreshOperation)
        self.KeyboardPeripheral.setDefaultHandler(self.HAppKeyboardHandles)
        
        # Build a HApp mouse
        self.HAppMouseHandles = hm.HAppMouseHandles(self.StateVisualizerRefreshOperation)
        self.MousePeripheral.setDefaultHandler(self.HAppMouseHandles)
        
        # add it as a visualization to the control center
        self.HAppControlCenter.addVisualization(self.StateVisualizer)
        self.HAppControlCenter.addOperation(self.StateVisualizerRefreshOperation)
        
        # update the ARCS status label
        #self.ARCSLabel.setText(self.HAppControlCenter.debugPrintAllResources())
        
        self.setCentralWidget(self.StateVisualizer)
    
    def connectTouchscreen(self, comString):
        self.TactileDisplay.connectTouch("NewHaptics Touchscreen KausiaV1", comString)
        
        # get the dimensions of the display
        state = self.TactileDisplay.state()
        displaySize = self.TactileDisplay.size()
        
        if self.called == 0:
            # Create the real time visualizer
            self.TouchVisualizer = tsv.TouchVisualizer("TouchVisualizer", state, displaySize)
            
            # create an operation to constantly refresh the visualizer and add it to the controller
            self.TouchVisualizerRefreshOperation = tsv.TouchVisualizerOperation("TouchVisualizerRefreshOperation", self.MousePeripheral, self.TactileDisplay, self.TouchVisualizer, self.margins)
            
            # Build a HApp keyboard
            self.HAppKeyboardHandles = hk.HAppKeyboardHandles(self.TouchVisualizerRefreshOperation)
            self.KeyboardPeripheral.setDefaultHandler(self.HAppKeyboardHandles)
            
            # Build a HApp mouse
            self.HAppMouseHandles = hm.HAppMouseHandles(self.TouchVisualizerRefreshOperation)
            self.MousePeripheral.setDefaultHandler(self.HAppMouseHandles)
            
            # remove the state visualizer
            self.HAppControlCenter.killOperation("StateVisualizerRefreshOperation")
            self.HAppControlCenter.removeVisualization("StateVisualizer")
            
            # add it as a visualization to the control center
            self.HAppControlCenter.addVisualization(self.TouchVisualizer)
            self.HAppControlCenter.addOperation(self.TouchVisualizerRefreshOperation)
            
            # set the mouse and keyboard handlers inside main window
            self.TouchVisualizerKeyboardHandles = tsv.TouchVisualizerKeyboardHandles(self.HAppControlCenter)
            self.TouchVisualizerMouseHandles = tsv.TouchVisualizerMouseHandles(self.HAppControlCenter)
            
            # assign the touchvisualizer keyboard handles
            self.KeyboardPeripheral.setDefaultHandler(self.TouchVisualizerKeyboardHandles)
            self.MousePeripheral.setDefaultHandler(self.TouchVisualizerMouseHandles)
            
            # update the ARCS status label
            #self.ARCSLabel.setText(self.HAppControlCenter.debugPrintAllResources())
            
            self.setCentralWidget(self.TouchVisualizer)
            self.called = 1
        else:
            # remove the state visualizer
            self.HAppControlCenter.killOperation("TouchVisualizerRefreshOperation")
            self.HAppControlCenter.removeVisualization("TouchVisualizer")
            
            # Build a HApp keyboard
            self.HAppKeyboardHandles = hk.HAppKeyboardHandles(self.TouchVisualizerRefreshOperation)
            self.KeyboardPeripheral.setDefaultHandler(self.HAppKeyboardHandles)
            
            # Build a HApp mouse
            self.HAppMouseHandles = hm.HAppMouseHandles(self.TouchVisualizerRefreshOperation)
            self.MousePeripheral.setDefaultHandler(self.HAppMouseHandles)
            
            # Create the real time visualizer
            self.TouchVisualizer = tsv.TouchVisualizer("TouchVisualizer", state, displaySize)
            
            # create an operation to constantly refresh the visualizer and add it to the controller
            self.TouchVisualizerRefreshOperation = tsv.TouchVisualizerOperation("TouchVisualizerRefreshOperation", self.MousePeripheral, self.TactileDisplay, self.TouchVisualizer, self.margins)
            
            # add it as a visualization to the control center
            self.HAppControlCenter.addVisualization(self.TouchVisualizer)
            self.HAppControlCenter.addOperation(self.TouchVisualizerRefreshOperation)
            
            # set the mouse and keyboard handlers inside main window
            self.TouchVisualizerKeyboardHandles = tsv.TouchVisualizerKeyboardHandles(self.HAppControlCenter)
            self.TouchVisualizerMouseHandles = tsv.TouchVisualizerMouseHandles(self.HAppControlCenter)
            
            # assign the touchvisualizer keyboard handles
            self.KeyboardPeripheral.setDefaultHandler(self.TouchVisualizerKeyboardHandles)
            self.MousePeripheral.setDefaultHandler(self.TouchVisualizerMouseHandles)
            
            # update the ARCS status label
            #self.ARCSLabel.setText(self.HAppControlCenter.debugPrintAllResources())
            
            self.setCentralWidget(self.TouchVisualizer)
    
    """ ROM related functions """
        
    def initializeRom(self, filename):
        
        # read in the file name and use the RomLauncher to start the ROM in a seperate thread
        self.ThisRom = rl.RomLauncher(filename, self.HAppControlCenter)
        
        self.ThisRom.startRom()
        
        self.HAppControlCenter.addRom(self.ThisRom)
        
        self.ThisRom.stopEvent.set()
        
        
        

    """ connection subroutines """
    

class displayConnector(qw.QAction):
    
    def __init__(self, comString, parent):
        super().__init__(comString, parent)
        self.MainWindow = parent
        self.comString = comString
        self.triggered.connect(self.connectDisplay)
    
    def connectDisplay(self):
        # connects the tactile display and adds a real time visualization
# =============================================================================
#         # Create the real time visualizer
#         ComString = self.comList[comIndex]
# =============================================================================
        print("disp com" + self.comString)
        
        self.MainWindow.connectDisplay(self.comString)
        
        
    
class touchConnector(qw.QAction):

    def __init__(self, comString, parent):
        super().__init__(comString, parent)
        self.MainWindow = parent
        self.comString = comString
        self.triggered.connect(self.connectTouchscreen)
        
    def connectTouchscreen(self):
        # connects the touch screen and adds a touch visualization
        print("touch com" + self.comString)
        
        self.MainWindow.connectTouchscreen(self.comString)
        
        
# =============================================================================
# if __name__ == '__main__':
#     
#     
#     app = qw.QApplication([])
#     
#     MainWindow = HAppMainWindow()
#     
#     MainWindow.show()
#     
#     
#     #filename = 'C:/Users/derek/OneDrive/NewHaptics Shared/HapticOS/FC_GUI_API/APIv0.7-Coeus/v0.764-Coeus/ROMs/FileNavigator/FileNavigatorReady.rom'
#     
#     #MainWindow.initializeRom(filename)
#     
#     
#     sys.exit(app.exec_())
# =============================================================================
