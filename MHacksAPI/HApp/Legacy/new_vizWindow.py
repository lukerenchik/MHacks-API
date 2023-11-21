# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 15:25:34 2020

@author: Derek Joslin
"""

from copy import deepcopy

from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
import qrc_resources

import NHAPI as nh

import new_vizWidgets as vw



import string


#GUI object for function selection
class vizWindow(qw.QMainWindow):
    """ Window that holds all the operation functions """

    def __init__(self, api, style, parent = None):
        super().__init__(parent)
        self.__api = api
        FCIcon = qg.QIcon(":main_symbol")
        HELogo = qg.QPixmap(":HE_logo")
        HELogo = HELogo.scaled(175,175,qc.Qt.KeepAspectRatio)
        self.color = style

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


       


        #create state views
        self.desiredView = vw.displayMat(nh.desired(), (50,50))
        self.desiredDock = qw.QDockWidget("desired state", self, qc.Qt.Widget)
        self.desiredDock.setWidget(self.desiredView)
        self.desiredDock.setMaximumWidth(900)

        #align widgets
        self.setCentralWidget(self.desiredDock)
        #self.addDockWidget(qc.Qt.BottomDockWidgetArea, self.labelDock)
        #self.currentView.setAlignment(qc.Qt.AlignTop | qc.Qt.AlignLeft)
        #self.desiredView.setAlignment(qc.Qt.AlignBottom | qc.Qt.AlignLeft)

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

        #resize the state views
        self.desiredView.resizeColumnsToContents()
        #self.currentView.resizeColumnsToContents()
        self.desiredView.resizeRowsToContents()
        #self.currentView.resizeRowsToContents()


    def flashSplash(self):
        FCLogo = qg.QPixmap(":main_logo")
        FCLogo = FCLogo.scaled(1000,1000)

        self.splash = qw.QSplashScreen(FCLogo)

        # By default, SplashScreen will be in the center of the screen.
        # You can move it to a specific location if you want:
        # self.splash.move(10,10)

        self.splash.show()

        # Close SplashScreen after 2 seconds (2000 ms)
        qc.QTimer.singleShot(1000, self.splash.close)


    def __createActions(self):
        #create the icons for the tools
        fillIcon = qg.QIcon(":fill")
        strokeIcon = qg.QIcon(":stroke")
        refreshIcon = qg.QIcon(":refresh")
        eraseIcon = qg.QIcon(":erase")
        dotIcon = qg.QIcon(":dot")
        lineIcon = qg.QIcon(":line")
        curveIcon = qg.QIcon(":curve")
        circleIcon = qg.QIcon(":circle")
        rectIcon = qg.QIcon(":square")
        triangleIcon = qg.QIcon(":triangle")
        polygonIcon = qg.QIcon(":polygon")
        brailleIcon = qg.QIcon(":braille")
        latinIcon = qg.QIcon(":text")
        txtsizeIcon = qg.QIcon(":textTitle")


        #cursor tools
        self.erase = qw.QAction("Input", self)
        self.erase.triggered.connect(lambda: self.api.erase())
        self.fill = qw.QAction(fillIcon, "Fill", self)
        self.fill.triggered.connect(lambda: self.__toolSelected("fill","({on/off-F})"))
        self.stroke = qw.QAction(strokeIcon, "Stroke", self)
        self.stroke.triggered.connect(lambda: self.__toolSelected("stroke","({stroke size})"))

        #shape tools
        self.dot = qw.QAction(dotIcon, "Dot", self)
        self.dot.setIconText("Dot")
        self.dot.triggered.connect(lambda: self.__toolSelected("dot","({coord1})"))
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
        self.latin = qw.QAction(latinIcon, "Latin", self)
        self.latin.triggered.connect(lambda: self.__toolSelected("latin","({coord1},{text},{font},{font size})"))
        self.latin.triggered.connect(lambda: self.__optionUpdated("font", '"Arial"'))

        
        #control actions
        self.clear = qw.QAction(eraseIcon, "Clear", self)
        self.clear.triggered.connect(lambda: self.__toolSelected("clear","()"))
        self.Fclear = qw.QAction("Fclear", self)
        self.Fclear.triggered.connect(lambda: self.__toolSelected("Fclear","()"))
        self.refresh = qw.QAction("Simulate Refresh", self)
        self.refresh.triggered.connect(lambda: self.__toolSelected("refresh","()"))
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
        self.disconnect = qw.QAction("Disconnect", self)
        self.disconnect.triggered.connect(lambda: self.__toolSelected("disconnect","()"))
        self.quickRefresh = qw.QAction(refreshIcon, "Refresh", self)
        self.quickRefresh.triggered.connect(lambda: self.__toolSelected("quickRefresh","()"))
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
        self.space = qw.QLabel(" " * 300)
        self.fontLabel = qw.QLabel("font size")
        self.fontSize = qw.QSpinBox()
        self.fontSize.setMinimum(8)
        self.fontSize.setFocusPolicy(qc.Qt.NoFocus)
        self.fontSize.valueChanged.connect(lambda: self.__optionUpdated("font size", self.fontSize.value()))
        self.space2 = qw.QLabel(" " * 20)
        self.directOnOFF = vw.MySwitch("       Direct\n\n\n")
        self.directOnOFF.setCheckable(True)
        self.directOnOFF.clicked.connect(lambda: self.__toolSelected("direct", "({on/off-D})"))
        self.directOnOFF.clicked.connect(lambda: self.__optionUpdated("on/off-D", self.directOnOFF.isChecked()))
        self.directOnOFF.setFocusPolicy(qc.Qt.NoFocus)
        self.eraseOnOFF = vw.MySwitch("        Input\n\n\n")
        self.eraseOnOFF.setCheckable(True)
        self.eraseOnOFF.clicked.connect(lambda: self.__toolSelected("erase", "({on/off-E})"))
        self.eraseOnOFF.clicked.connect(lambda: self.__optionUpdated("on/off-E", self.eraseOnOFF.isChecked()))
        self.eraseOnOFF.setFocusPolicy(qc.Qt.NoFocus)
        self.fillOnOFF = vw.MySwitch("         Fill\n\n\n")
        self.fillOnOFF.setCheckable(True)
        self.fillOnOFF.clicked.connect(lambda: self.__toolSelected("fill", "({on/off-F})"))
        self.fillOnOFF.clicked.connect(lambda: self.__optionUpdated("on/off-F", self.fillOnOFF.isChecked()))
        self.fillOnOFF.setFocusPolicy(qc.Qt.NoFocus)
        self.space3 = qw.QLabel(" " * 20)

    def __createMenuBar(self):
        menuBar = qw.QMenuBar(self)
        self.setMenuBar(menuBar)
        #create menu bars

        #edit menu
        editMenu = qw.QMenu("&Edit", self)
        editMenu.addAction(self.clear)
        editMenu.addAction(self.Fclear)

        #help menu
        helpMenu = qw.QMenu("&Help", self)
        helpMenu.addAction(self.settings)
        helpMenu.addAction(self.frames)

        #control menu
        controlMenu = qw.QMenu("Control",self)
        controlMenu.addAction(self.refresh)
        controlMenu.addAction(self.times)
        controlMenu.addAction(self.setMat)


        #board menu
        boardMenu = qw.QMenu("Board", self)
  

    def __createToolBars(self):
        #cursor Bar
        cursors = qw.QToolBar("cursors", self)
        #cursors.addAction(self.erase)
        cursors.addWidget(self.eraseOnOFF)
        #cursors.addAction(self.fill)
        cursors.addWidget(self.fillOnOFF)
        cursors.addWidget(self.strokeLabel)
        cursors.addWidget(self.strokeSize)
        cursors.addWidget(self.space)
        #cursors.setWidgetSize(qc.QSize(50,50))
        cursors.setMovable(False)


        #shape Bar
        shapes = qw.QToolBar("shapes", self)
        shapes.setToolButtonStyle(qc.Qt.ToolButtonTextUnderIcon)
        shapes.addAction(self.dot)
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
        characters.addAction(self.latin)
        characters.addWidget(self.fontLabel)
        characters.addWidget(self.fontSize)
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
        board.addAction(self.quickRefresh)

        #create submenu
        #board.addAction(self.direct)
        board.addWidget(self.directOnOFF)
        board.addWidget(self.space3)
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
        self.desiredView.clicked.connect(lambda index = self.desiredView.currentIndex: self.__coordSelector((index.row(),index.column())))

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

            self.console.setStyleSheet(("border: 1px solid rgba(65,67,77, 100%);"
                            "font-family : Comfortaa;"
                            "color: rgb(255,255,245);"
                            "font-size: 18px;"
                            "background-color: rgb(85,216,211);"
                            "selection-color: rgb(65,67,77);"
                            "selection-background-color: rgba(37,64,143, 10%);" ))

            self.currentDock.setStyleSheet(("border: 1px solid rgba(65,67,77, 100%);"
                            "font-family : Comfortaa;"
                            "color: rgb(255,255,245);"
                            "font-size: 18px;"
                            "background-color: rgb(41,178,170);"
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




    def updateDocks(self):
        self.desiredView.state.layoutChanged.emit()
        #self.desiredView.update()
        #self.currentView.update()

    def closeEvent(self, event):
        if nh.comLink_check():
            nh.disconnect()
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
