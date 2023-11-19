# -*- coding: utf-8 -*-
"""
Created on Thu May 20 14:11:58 2021

@author: Derek Joslin
"""

from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg

import qrc_resources

import APIConsole as ac
import ToggleSwitch as ts

import IntegratedInputWindow as iw
import RealTimeStateVisualizer as rv

import FileManagement as fm
import ComFinder as cf
import KeyboardHandler as kb

import math

import string

#GUI object for function selection
class HapticVisualizerMainWindow(qw.QMainWindow):
    """ Window that holds all the operation functions """

    def __init__(self, style, NHAPI, parent = None):
        self.flashSplash()
        super().__init__(parent)
        FCIcon = qg.QIcon(":main_symbol")
        HELogo = qg.QPixmap(":HE_logo")
        HELogo = HELogo.scaled(175,175,qc.Qt.KeepAspectRatio)
        self.color = style
        self.NHAPI = NHAPI
        
# =============================================================================
#         style guide
#         rgb(85,216,211) -> light turquoise
#         rgb(41,178,170) -> dark turquoise
#         rgb(37,64,143) -> reflex blue
#         rgb(65,67,77) -> persian nights
# =============================================================================
        
        #create window
        self.setWindowTitle("FC Lab operation functions")
        self.setWindowIcon(FCIcon)
        
        #create status bar with the status and haptic engine ad
        self.statusBar = qw.QStatusBar()
        self.setStatusBar(self.statusBar)
        
        self.HEad = qw.QLabel()
        self.HEad.setPixmap(HELogo)
        self.centralWidget = qw.QLabel("Hello World")
        self.centralWidget.setWordWrap(True)
        self.pwr = qw.QLabel("POWERED BY")
        self.statusBar.addWidget(self.centralWidget,30)
        self.statusBar.addWidget(self.pwr)
        self.statusBar.addWidget(self.HEad)
        
        #console creation
        self.Console = ac.APIConsole(self.NHAPI)
        self.GuiDock = qw.QDockWidget("console", self, qc.Qt.Widget)
        self.GuiDock.setWidget(self.Console)
        self.Console.interpreter.exec_signal.connect(lambda: self.updateDocks())
        
        #create state views
        self.DesiredStateView = iw.IntegratedInputWindow(self.NHAPI)
        self.setCentralWidget(self.DesiredStateView)
        
        #self.CurrentStateView = rv.RealTimeStateVisualizer(self.NHAPI)
        #self.StateDock = qw.QDockWidget("state", self, qc.Qt.Widget)
        #self.StateDock.setWidget(self.CurrentStateView)
        #self.addDockWidget(qc.Qt.LeftDockWidgetArea, self.StateDock, qc.Qt.Vertical)
        
        #align widgets
        self.addDockWidget(qc.Qt.RightDockWidgetArea, self.GuiDock, qc.Qt.Vertical)
        
        #create the command dictionary, parameter dictionary, and coordinate history
        self.__commandDict = {}
        self.__coordHist = [None,None,None,None]
        self.__paramDict = {}

        #create dictionary formatter
        self.__commandFMT = PartialFormatter()

        #create window elements
        self.__createActions()
        self.__createMenuBar()
        self.__createToolBars()
        self.__connectControls()
        self.__setStyles()
        
        #create keyboard handler
        self.Keyboard = kb.KeyboardHandler(self.__coordSelector, self.__toolSelected, self.NHAPI)
        
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



    def keyPressEvent(self, event):
        self.Keyboard.handleKeyPress(event.key())
        event.accept()




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
        self.braille.triggered.connect(lambda: self.__toolSelected("braille","({coord1},{text})"))
        self.brailleBox = qw.QLineEdit(self)
        self.brailleBox.setMaximumWidth(100)
        def toolType():
            if not self.__commandDict["command"] == "latin":
                self.__toolSelected("braille","({coord1},{text})")

        self.brailleBox.textChanged.connect(toolType)
        self.brailleBox.textChanged.connect(lambda: self.__optionUpdated("coord1", self.__coordHist[-1]))
        self.brailleBox.textChanged.connect(lambda t: self.__optionUpdated("text", '"{0}"'.format(t)))
        self.brailleBox.textChanged.connect(lambda t: self.__optionUpdated("font", '"Arial"'))
# =============================================================================
#         self.brailleBox.returnPressed.connect(lambda: self.__toolSelected("braille","({coord1},{text})"))
#         self.brailleBox.returnPressed.connect(lambda: self.__optionUpdated("coord1", self.__coordHist[-1]))
#         self.brailleBox.returnPressed.connect(lambda: self.__optionUpdated("text", '"{0}\\n"'.format(self.brailleBox.text())))
# =============================================================================
        self.brailleBox.returnPressed.connect(lambda: self.brailleBox.insert("\\n"))

        #file actions
        self.saveDesired = qw.QAction("Save Desired State", self)
        def saveFile():
            #decide which state to save
            options = qw.QFileDialog.Options()
            options |= qw.QFileDialog.DontUseNativeDialog
            source = qw.QFileDialog.getSaveFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)[0]
            fm.saveCsv(source,self.NHAPI.return_desiredState())


        self.saveDesired.triggered.connect(saveFile)


        self.load = qw.QAction("Load",self)
        def loadFile():
            options = qw.QFileDialog.Options()
            options |= qw.QFileDialog.DontUseNativeDialog
            source = qw.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)[0]
            if source[-4:-1] == ".cs":
                matData = fm.openCsv(source)
                #format the matData properly from strings into ints
                return [[int(i) for i in row] for row in matData]
            elif source[-4:-1] == ".pn":
                matData = fm.openPng(source,self.NHAPI.return_displaySize())
                #format the matData properly from strings into ints
                return [[int(i) for i in row] for row in matData]
            elif source[-4:-1] == ".ro":
                fm.openRom(source)
                return
            else:
                return

        self.load.triggered.connect(lambda: self.__toolSelected("setMat","({matrix})"))
        self.load.triggered.connect(lambda: self.__optionUpdated("matrix", loadFile()))

        #control actions
        self.clear = qw.QAction(eraseIcon, "Clear", self)
        self.clear.triggered.connect(lambda: self.__toolSelected("clear","()"))
        self.Fclear = qw.QAction(FclearIcon, "Force clear", self)
        self.Fclear.triggered.connect(lambda: self.__toolSelected("Fclear","()"))
        self.times = qw.QAction("Times", self)
        self.times.triggered.connect(lambda: self.__toolSelected("times","({now})"))
        self.timesStepper = qw.QSpinBox()
        self.timesStepper.setRange(0,100000)
        self.timesStepper.setSingleStep(100)
        self.timesStepper.valueChanged.connect(lambda: self.__toolSelected("times", "({now})"))
        self.timesStepper.valueChanged.connect(lambda: self.__optionUpdated("now", self.timesStepper.value()))
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
        self.onOFF = qw.QPushButton("on/off")
        self.onOFF.setCheckable(True)
        self.onOFF.clicked.connect(lambda: self.__optionUpdated("on/off", self.onOFF.isChecked()))
        self.onOFF.setFocusPolicy(qc.Qt.NoFocus)
        self.strokeLabel = qw.QLabel("stroke size")
        self.strokeSize = qw.QSpinBox()
        self.strokeSize.setMinimum(1)
        self.strokeSize.valueChanged.connect(lambda: self.__toolSelected("stroke","({stroke size})"))
        self.strokeSize.valueChanged.connect(lambda: self.__optionUpdated("stroke size", self.strokeSize.value()))
        self.strokeSize.setFocusPolicy(qc.Qt.NoFocus)
        self.space = qw.QLabel(" " * 5)
        self.fontLabel = qw.QLabel("font size")
        self.fontSize = qw.QSpinBox()
        self.fontSize.setMinimum(8)
        self.fontSize.setFocusPolicy(qc.Qt.NoFocus)
        self.fontSize.valueChanged.connect(lambda: self.__optionUpdated("font size", self.fontSize.value()))
        self.space2 = qw.QLabel(" " * 5)
        self.directOnOFF = ts.ToggleSwitch("       Direct\n\n\n")
        self.directOnOFF.setCheckable(True)
        self.directOnOFF.clicked.connect(lambda: self.__toolSelected("direct", "({on/off-D})"))
        self.directOnOFF.clicked.connect(lambda: self.__optionUpdated("on/off-D", self.directOnOFF.isChecked()))
        self.directOnOFF.setFocusPolicy(qc.Qt.NoFocus)
        self.eraseOnOFF = ts.ToggleSwitch("        Input\n\n\n")
        self.eraseOnOFF.setCheckable(True)
        self.eraseOnOFF.clicked.connect(lambda: self.__toolSelected("erase", "({on/off-E})"))
        self.eraseOnOFF.clicked.connect(lambda: self.__optionUpdated("on/off-E", self.eraseOnOFF.isChecked()))
        self.eraseOnOFF.setFocusPolicy(qc.Qt.NoFocus)
        self.fillOnOFF = ts.ToggleSwitch("         Fill\n\n\n")
        self.fillOnOFF.setCheckable(True)
        self.fillOnOFF.clicked.connect(lambda: self.__toolSelected("fill", "({on/off-F})"))
        self.fillOnOFF.clicked.connect(lambda: self.__optionUpdated("on/off-F", self.fillOnOFF.isChecked()))
        self.fillOnOFF.setFocusPolicy(qc.Qt.NoFocus)
        self.space3 = qw.QLabel(" " * 5)

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
        connectMenu = qw.QMenu("Connect Board", self)
        connectMenu.aboutToShow.connect(lambda: self.__toolSelected("connect","({com})"))
        
        TouchConnectMenu = qw.QMenu("Connect Touch", self)
        TouchConnectMenu.aboutToShow.connect(lambda: self.__toolSelected("connectTouch","({com})"))

        #make a function to check the com ports create a list of com actions and add them to the connect Menu


        def findComs():
# =============================================================================
#             def getPort(port):
#                 mystring = str(port)
#                 return mystring
# =============================================================================
            #get list of com ports
            comList = cf.serial_ports()
            print(comList)
            #delete existing actions
            connectMenu.clear()
            TouchConnectMenu.clear()
            #create action for each port on the list and add to connectMenu
            while len(comList) > 0:
                action = qw.QAction(comList[-1], self)
                action.triggered.connect(lambda a,i = comList[-1]: self.__optionUpdated("com", '"{0}"'.format(i)))
                connectMenu.addAction(action)
                TouchConnectMenu.addAction(action)
                print(comList)
                comList.pop()
                #action.triggered.connect(lambda: self.DesiredStateView.updateWindowSize())

# =============================================================================
#             for port in comList:
#                 func = lambda: self.__optionUpdated("com", '"{0}"'.format(port))
#                 action = vw.ComAction(port, func, self)
#                 actionList['"{0}"'.format(port)] = action
#             for action in actionList:
#                 connectMenu.addAction(actionList[action])
# =============================================================================

        #self.getCOMS = qw.QAction("getcoms",self)
        #self.getCOMS.triggered.connect(lambda: findComs())
        boardMenu.aboutToShow.connect(findComs)


        boardMenu.addMenu(connectMenu)
        boardMenu.addMenu(TouchConnectMenu)
        


        boardMenu.addAction(self.disconnect)
        boardMenu.addAction(self.disconnectTouch)
        boardMenu.addAction(self.refresh)


        #create submenu for direct
        directMenu = qw.QMenu("Direct", self)
# =============================================================================
#         self.Off = qw.QAction("Off")
#         self.Off.triggered.connect(lambda: self.__optionUpdated("on/off", False))
#         self.On = qw.QAction("On")
#         self.Off.triggered.connect(lambda: self.__optionUpdated("on/off", True))
#         directMenu.addAction(self.Off)
#         directMenu.addAction(self.On)
# =============================================================================
        directMenu.addAction(self.directOff)
        directMenu.addAction(self.directOn)

        boardMenu.addMenu(directMenu)

        #add menu bars
        menuBar.addMenu(fileMenu)
        menuBar.addMenu(editMenu)
        menuBar.addMenu(helpMenu)
        menuBar.addMenu(controlMenu)
        menuBar.addMenu(boardMenu)

    def __createToolBars(self):
        #cursor Bar
        cursors = qw.QToolBar("cursors", self)
        #cursors.addAction(self.erase)
        cursors.addWidget(self.eraseOnOFF)
        cursors.addWidget(self.space)
        #cursors.addAction(self.fill)
        cursors.addWidget(self.fillOnOFF)
        cursors.addWidget(self.space2)
        cursors.addWidget(self.strokeLabel)
        cursors.addWidget(self.strokeSize)
        #cursors.setWidgetSize(qc.QSize(50,50))
        cursors.setMovable(False)


        #shape Bar
        shapes = qw.QToolBar("shapes", self)
        shapes.setToolButtonStyle(qc.Qt.ToolButtonTextUnderIcon)
        shapes.addAction(self.dot)
        shapes.addAction(self.cell)
        shapes.addAction(self.line)
        shapes.addAction(self.curve)
        shapes.addAction(self.circle)
        shapes.addAction(self.rect)
        shapes.addAction(self.triangle)
        shapes.addAction(self.polygon)
        shapes.setIconSize(qc.QSize(50,50))
        shapes.setMovable(False)

        #clear Bar
        clear = qw.QToolBar("clear", self)
        clear.setToolButtonStyle(qc.Qt.ToolButtonTextUnderIcon)
        clear.addAction(self.clear)
        clear.setIconSize(qc.QSize(50,50))
        clear.setMovable(False)
        clear.addAction(self.Fclear)

        #character Bar
        characters = qw.QToolBar("characters", self)
        characters.setToolButtonStyle(qc.Qt.ToolButtonTextUnderIcon)
        characters.addAction(self.braille)
        characters.addWidget(self.brailleBox)
        characters.setIconSize(qc.QSize(50,50))
        characters.setMovable(False)



# =============================================================================
#         #control Bar
#         control = qw.QToolBar("control", self)
#         control.addAction(self.refresh)
#         control.addAction(self.times)
#         control.addWidget(self.timesStepper)
#         control.addWidget(self.space2)
#         control.setIconSize(qc.QSize(50,50))
#         control.setMovable(False)
# =============================================================================


        #board Bar
        board = qw.QToolBar("board", self)
        board.setToolButtonStyle(qc.Qt.ToolButtonTextUnderIcon)
        board.addAction(self.refresh)
        board.addWidget(self.space3)

        #create submenu
        #board.addAction(self.direct)
        board.addWidget(self.directOnOFF)
        board.setIconSize(qc.QSize(50,50))
        board.setMovable(False)



        #add tool bars
        self.addToolBar(qc.Qt.TopToolBarArea, cursors)
        self.addToolBar(qc.Qt.LeftToolBarArea, shapes)
        self.addToolBar(qc.Qt.LeftToolBarArea, clear)
        self.addToolBar(qc.Qt.BottomToolBarArea, characters)
        #self.addToolBar(qc.Qt.TopToolBarArea, control)
        self.addToolBar(qc.Qt.TopToolBarArea, board)

    def __connectControls(self):
        self.DesiredStateView.widget.widget.addFunctionToButtons(self.__coordSelector)
        
    
    
    def __setStyles(self):


        if self.color:

            self.setStyleSheet(("border: 1px solid rgba(65,67,77, 100%);"
                            "font-family : Comfortaa;"
                            "color: rgb(255,255,245);"
                            "font-size: 13px;"
                            "background-color: rgb(85,216,211);"
                            "selection-color: rgb(65,67,77);"
                            "selection-background-color: rgba(37,64,143, 10%);" ))

            self.statusBar.setStyleSheet(("border: 1px solid rgba(65,67,77, 100%);"
                            "font-family : Comfortaa;"
                            "color: rgb(255,255,245);"
                            "font-size: 18px;"
                            "background-color: rgb(41,178,170);"
                            "selection-color: rgb(65,67,77);"
                            "selection-background-color: rgba(37,64,143, 10%);" ))

            self.Console.setStyleSheet(("border: 1px solid rgba(65,67,77, 100%);"
                            "font-family : Comfortaa;"
                            "color: rgb(255,255,245);"
                            "font-size: 18px;"
                            "background-color: rgb(85,216,211);"
                            "selection-color: rgb(65,67,77);"
                            "selection-background-color: rgba(37,64,143, 10%);" ))

            self.desiredDock.setStyleSheet(("border: 1px solid rgba(65,67,77, 100%);"
                            "font-family : Comfortaa;"
                            "color: rgb(255,255,245);"
                            "font-size: 18px;"
                            "background-color: rgb(41,178,170);"
                            "selection-color: rgb(65,67,77);"
                            "selection-background-color: rgba(37,64,143, 10%);" ))
        else:
            pass



    def __coordSelector(self, index):


        #only log a coord if coordinates are in the parameters
        coordList = [key for key, value in self.__paramDict.items() if 'coord' in key.lower()]
        #print(coordList)
        #print(len(coordList))


        if ("radius" in self.__paramDict) and self.__paramDict[coordList[-1]]:
            a = self.__paramDict[coordList[-1]][0]
            b = self.__paramDict[coordList[-1]][1]
            #print("({0},{1})".format(a,b))
            c = index[0]
            d = index[1]
            rad = math.sqrt((a-c)**2 + (b-d)**2)
            self.__paramDict.update({"radius" : rad})
            self.centralWidget.setText("<b>coordinate is ({0},{1})".format(index[0],index[1]))
            self.processCommand()

        elif len(coordList) != 0:
            #create a list of coordinates up to 50 long
            self.__coordHist.append(index)
            while len(self.__coordHist) > 50:
                self.__coordHist.pop(0)
            #assign the dynamic parameter coordinates
            else:
                self.__coordUpdater(index)

            self.centralWidget.setText("<b>coordinate is ({0},{1})".format(index[0],index[1]))
            self.processCommand()

        else:
            self.centralWidget.setText("<b>coordinate is ({0},{1})".format(index[0],index[1]))



    def __coordUpdater(self, newCoord):
        #create a dictionary of just the coordinate parameters
        coordDict = {key: value for key, value in self.__paramDict.items() if 'coord' in key.lower()}
        #create the assign order of the dictionary (so coord3 = coord2, coord2 = coord1... and so forth)
        assignOrder = [i + 1 for i in range(1,len(coordDict))][::-1]
        for i in range(0,len(coordDict) - 1):
            coordDict["coord{0}".format(assignOrder[i])] = coordDict["coord{0}".format(assignOrder[i] - 1)]
        coordDict["coord1"] = newCoord
        self.__paramDict.update(coordDict)


    def __optionUpdated(self, param, value):
        if value == True and not type(value) == int:
            value = '"on"'
        elif value == False and not type(value) == int:
            value = '"off"'
        self.__paramDict.update({param : value})
        self.centralWidget.setText("<b>{0} is {1}".format(param,value))



        #process the command when an option changes
        self.processCommand()


    def __toolSelected(self, tool, parameters):
        self.__commandDict["parameters"] = parameters
        self.__commandDict["command"] = tool
        #dynamically populate the parameter Dictionary with the parameters
        self.__assignParam(parameters)
        self.centralWidget.setText("<b>{command} selected with {parameters} parameters".format(**self.__commandDict))
        self.processCommand()


    def processCommand(self):
        #if there is no command with no parameters display nothing
        if not self.__commandDict:
            return
        #if the string formats without errors then execute otherwise display
        parameters = self.__commandFMT.format(self.__commandDict["parameters"],**self.__paramDict)
        if parameters.find("~~") == -1:
            #print("execute tool executed with {0}".format(parameters))
            self.executeTool()
        else:
            #print("console fill executed with {0}".format(parameters))
            self.consoleFill()


    def consoleFill(self):
        self.Console.clear_input_buffer()
        #format the parameters with values
        parameters = self.__commandFMT.format(self.__commandDict["parameters"],**self.__paramDict)
        commandStr = "{0}{1}".format(self.__commandDict["command"], parameters)
        self.Console.insert_input_text(commandStr)



    def executeTool(self):
        #self.DesiredStateView.state.layoutAboutToBeChanged.emit()
        #self.currentView.state.layoutAboutToBeChanged.emit()
        self.Console.clear_input_buffer()
        parameters = self.__commandFMT.format(self.__commandDict["parameters"],**self.__paramDict)
        commandStr = "{0}{1}".format(self.__commandDict["command"], parameters)
        self.Console.insert_input_text(commandStr)
        buffer = self.Console.input_buffer()
        self.Console.insert_input_text('\n', show_ps=False)
        self.Console.process_input(buffer)
        self.centralWidget.setText("<b>{0} was executed".format(commandStr))
        desiredState = self.NHAPI.return_desiredState() 
        #print(id(desiredState))
        self.DesiredStateView.widget.widget.updateState(desiredState)
        #self.updateDocks()
        #once the tool has been executed clear the previous command
        self.__clearParam()
        if len(self.__commandDict["parameters"]) > 2:
            self.__toolSelected(self.__commandDict["command"],self.__commandDict["parameters"])
            
    def updateDocks(self):
        #self.DesiredStateView.state.layoutChanged.emit()
        self.DesiredStateView.widget.widget.paintView()



    def __assignParam(self, parameters):
        #replace all the invalid characters inside the string
        parameters = parameters.replace(")","")
        parameters = parameters.replace("(","")
        parameters = parameters.replace("{","")
        parameters = parameters.replace("}","")
        #create the list of keys
        keyList = parameters.split(",")
        #create the None list
        noneList = [None for i in range(0,len(keyList))]
        #merge into paramDict using Dictionary comprehension
        newDict = {keyList[i]: noneList[i] for i in range(len(noneList))}
        #make an exception for on/off
        if 'on/off' in self.__paramDict:
            newDict.update({'on/off' : self.__paramDict['on/off']})

        if 'font size' in self.__paramDict:
            newDict.update({'font size' : self.paramDict['font size']})

        self.__paramDict = newDict

    def __clearParam(self):
        #there are some exception values for clearing parameter
        newDict = {}
        if 'on/off' in self.__paramDict:
            newDict.update({'on/off' : self.__paramDict['on/off']})

        if 'font size' in self.__paramDict:
            newDict.update({'font size' : self.paramDict['font size']})

        self.__paramDict = newDict

    def __clearCommand(self):
        self.__commandDict = {}

    def closeEvent(self, event):
        if self.NHAPI.comLink_check():
            self.NHAPI.comLink_off()
            event.accept()
        else:
            event.accept()


class PartialFormatter(string.Formatter):
    def __init__(self, missing='~~', bad_fmt='!!'):
        self.missing, self.bad_fmt=missing, bad_fmt

    def get_field(self, field_name, args, kwargs):
        # Handle a key not found
        try:
            val=super(PartialFormatter, self).get_field(field_name, args, kwargs)
            # Python 3, 'super().get_field(field_name, args, kwargs)' works
        except (KeyError, AttributeError):
            val=None,field_name
        return val

    def format_field(self, value, spec):
        # handle an invalid format
        if value==None: return self.missing
        try:
            return super(PartialFormatter, self).format_field(value, spec)
        except ValueError:
            if self.bad_fmt is not None: return self.bad_fmt
            else: raise
