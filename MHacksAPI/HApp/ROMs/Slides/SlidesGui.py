
import RomAPI as rs
import SlidesOperations as so

import SlidesFileManagement as sfm
from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc


class SlidesVisualizationHandles(rs.RomVisualizationHandles):
    
    def __init__(self, RomExplorer, MasterModel):
        print("Slides handler initialized")
        
        self.MasterModel = MasterModel
        self.FileManager = self.MasterModel.FileManager
        
        self.MasterModel.nSlides = 0
        self.MasterModel.currentSlide = 0
        self.MasterModel.slidesDictionary = {}
        
        self.RomExplorer = RomExplorer
        self.RomExplorer.setWindowTitle("Slides Rom Window")
# =============================================================================
#         # create a slide button for a files in slides path
#         self.createSlideButtons(self.FileManager.currentNumSlides())
# =============================================================================
        
        
    def createActionsHandler(self):
        print("Create Slides Actions")
        # create qw.QAction objects here and use QAction.triggered.connect to connect custom functions
        self.RomExplorer.newAction = qw.QAction("New", self.RomExplorer)
        self.RomExplorer.newAction.triggered.connect(self.newFile)
        self.RomExplorer.loadAction = qw.QAction("Load", self.RomExplorer)
        self.RomExplorer.loadAction.triggered.connect(self.loadFile)
        self.RomExplorer.saveAction = qw.QAction("Save", self.RomExplorer)
        self.RomExplorer.saveAction.triggered.connect(self.saveFile)
        
        
    def createButtonsHandler(self):
        print("Create Slides Buttons")
        
        # create buttons for drawing
        self.RomExplorer.dotButton = qw.QPushButton("Dot", self.RomExplorer)
        self.RomExplorer.dotButton.clicked.connect(lambda: self.MasterModel.selectTool("drawDot"))
        self.RomExplorer.lineButton = qw.QPushButton("Line", self.RomExplorer)
        self.RomExplorer.lineButton.clicked.connect(lambda: self.MasterModel.selectTool("drawLine"))
        self.RomExplorer.curveButton = qw.QPushButton("Curve", self.RomExplorer)
        self.RomExplorer.curveButton.clicked.connect(lambda: self.MasterModel.selectTool("drawCurve"))
        self.RomExplorer.circleButton = qw.QPushButton("Circle", self.RomExplorer)
        self.RomExplorer.circleButton.clicked.connect(lambda: self.MasterModel.selectTool("drawCircle"))
        self.RomExplorer.rectangleButton = qw.QPushButton("Rectangle", self.RomExplorer)
        self.RomExplorer.rectangleButton.clicked.connect(lambda: self.MasterModel.selectTool("drawRectangle"))
        self.RomExplorer.triangleButton = qw.QPushButton("Triangle", self.RomExplorer)
        self.RomExplorer.triangleButton.clicked.connect(lambda: self.MasterModel.selectTool("drawTriangle"))
        self.RomExplorer.polygonButton = qw.QPushButton("Polygon", self.RomExplorer)
        self.RomExplorer.polygonButton.clicked.connect(lambda: self.MasterModel.selectTool("drawPolygon"))
        self.RomExplorer.clearButton = qw.QPushButton("Clear", self.RomExplorer)
        self.RomExplorer.clearButton.clicked.connect(lambda: self.MasterModel.selectTool("selectClear"))
        
        
        # create add and delete slides buttons
        self.RomExplorer.addSlideButton = qw.QPushButton("Add Slide", self.RomExplorer)
        self.RomExplorer.addSlideButton.clicked.connect(lambda: self.createSlide(self.MasterModel.nSlides + 1))
        self.RomExplorer.removeSlideButton = qw.QPushButton("Remove Slide", self.RomExplorer)
        self.RomExplorer.removeSlideButton.clicked.connect(lambda: self.removeSlide(self.MasterModel.nSlides))
        
        
        # create the buttons for options and settings
        self.RomExplorer.inputButton = qw.QPushButton("Input", self.RomExplorer)
        self.RomExplorer.inputButton.clicked.connect(lambda: self.MasterModel.selectTool("toggleInput"))
        self.RomExplorer.fillButton = qw.QPushButton("Fill", self.RomExplorer)
        self.RomExplorer.fillButton.clicked.connect(lambda: self.MasterModel.selectTool("toggleFill"))
        self.RomExplorer.directButton = qw.QPushButton("Direct", self.RomExplorer)
        self.RomExplorer.directButton.clicked.connect(lambda: self.MasterModel.selectTool("toggleDirect"))
        self.RomExplorer.strokeButton = qw.QPushButton("Stroke", self.RomExplorer)
        self.RomExplorer.strokeButton.clicked.connect(lambda: self.MasterModel.selectTool("adjustStrokeSize"))
        self.RomExplorer.refreshButton = qw.QPushButton("Refresh", self.RomExplorer)
        self.RomExplorer.refreshButton.clicked.connect(lambda: self.MasterModel.selectTool("refresh"))
        
        
# =============================================================================
#         # test button
#         self.RomExplorer.inputButton = qw.QPushButton("Move Right", self.RomExplorer)
#         self.RomExplorer.inputButton.clicked.connect(lambda: self.MasterModel.CanvasNavigation.moveRight())
#         self.RomExplorer.inputButton.clicked.connect(lambda: self.MasterModel.updateViewSpace())
#         self.RomExplorer.fillButton = qw.QPushButton("Move Down", self.RomExplorer)
#         self.RomExplorer.fillButton.clicked.connect(lambda: self.MasterModel.CanvasNavigation.moveDown())
#         self.RomExplorer.fillButton.clicked.connect(lambda: self.MasterModel.updateViewSpace())
#         self.RomExplorer.directButton = qw.QPushButton("Move Left", self.RomExplorer)
#         self.RomExplorer.directButton.clicked.connect(lambda: self.MasterModel.CanvasNavigation.moveLeft())
#         self.RomExplorer.directButton.clicked.connect(lambda: self.MasterModel.updateViewSpace())
#         self.RomExplorer.strokeButton = qw.QPushButton("Move Up", self.RomExplorer)
#         self.RomExplorer.strokeButton.clicked.connect(lambda: self.MasterModel.CanvasNavigation.moveUp())
#         self.RomExplorer.refreshButton.clicked.connect(lambda: self.MasterModel.updateViewSpace())
#         self.RomExplorer.refreshButton = qw.QPushButton("Refresh", self.RomExplorer)
#         self.RomExplorer.refreshButton.clicked.connect(lambda: self.MasterModel.updateViewSpace())
# =============================================================================
        
    def createWidgetsHandler(self):
        print("Create Slides Widgets")
        # create the "Stroke Size Scrollwheel" widget
        
        self.RomExplorer.strokeSize = qw.QSpinBox()
        self.RomExplorer.strokeSize.setMinimum(1)
        self.RomExplorer.strokeSize.setMaximum(10)
        self.RomExplorer.strokeSize.setValue(1)
        #self.RomExplorer.strokeSize.valueChanged.connect(self.RomExplorer.adjustStrokeSize)
        
        
    def createToolsHandler(self):
        print("Create Slides Tools")
        # create qw.QToolBar objects here and use QToolBar.addWidget to add QPushButton widgets
        self.RomExplorer.leftToolBar = qw.QToolBar("Left Toolbar", self.RomExplorer)
        self.RomExplorer.leftToolBar.addWidget(self.RomExplorer.dotButton)
        self.RomExplorer.leftToolBar.addWidget(self.RomExplorer.lineButton)
        self.RomExplorer.leftToolBar.addWidget(self.RomExplorer.curveButton)
        self.RomExplorer.leftToolBar.addWidget(self.RomExplorer.circleButton)
        self.RomExplorer.leftToolBar.addWidget(self.RomExplorer.rectangleButton)
        self.RomExplorer.leftToolBar.addWidget(self.RomExplorer.triangleButton)
        self.RomExplorer.leftToolBar.addWidget(self.RomExplorer.polygonButton)
        self.RomExplorer.leftToolBar.addWidget(self.RomExplorer.clearButton)
        self.RomExplorer.leftToolBar.addWidget(self.RomExplorer.addSlideButton)
        self.RomExplorer.leftToolBar.addWidget(self.RomExplorer.removeSlideButton)
        self.RomExplorer.leftToolBar.setIconSize(qc.QSize(50,50))
        self.RomExplorer.leftToolBar.setMovable(False)
        self.RomExplorer.addToolBar(qc.Qt.LeftToolBarArea, self.RomExplorer.leftToolBar)
        
        # create the top toolbar
        self.RomExplorer.topToolBar = qw.QToolBar("Top Toolbar", self.RomExplorer)
        self.RomExplorer.topToolBar.addWidget(self.RomExplorer.inputButton)
        self.RomExplorer.topToolBar.addWidget(self.RomExplorer.fillButton)
        self.RomExplorer.topToolBar.addWidget(self.RomExplorer.directButton)
        self.RomExplorer.topToolBar.addWidget(self.RomExplorer.strokeButton)
        self.RomExplorer.topToolBar.addWidget(self.RomExplorer.strokeSize)
        self.RomExplorer.topToolBar.addWidget(self.RomExplorer.refreshButton)
        self.RomExplorer.topToolBar.setIconSize(qc.QSize(50,50))
        self.RomExplorer.topToolBar.setMovable(False)
        self.RomExplorer.addToolBar(qc.Qt.TopToolBarArea, self.RomExplorer.topToolBar)
        
        self.RomExplorer.rightToolBar = qw.QToolBar("Right Toolbar", self.RomExplorer)
        self.RomExplorer.addToolBar(qc.Qt.RightToolBarArea, self.RomExplorer.rightToolBar)
        
    def createMenuHandler(self):
        print("Create Slides Menu")
        # create the File menu
        self.RomExplorer.fileMenu = qw.QMenu('File')
        self.RomExplorer.menuBar().addMenu(self.RomExplorer.fileMenu)
        
        # add the load and save actions to the File menu
        self.RomExplorer.fileMenu.addAction(self.RomExplorer.newAction)
        self.RomExplorer.fileMenu.addAction(self.RomExplorer.loadAction)
        self.RomExplorer.fileMenu.addAction(self.RomExplorer.saveAction)
        
    def newFile(self):
        # create a new folder in the Root
        self.FileManager.makeCWD("testScripts")
        
        options = qw.QFileDialog.Options()
        options |= qw.QFileDialog.DontUseNativeDialog
        fileName, _ = qw.QFileDialog.getSaveFileName(self.RomExplorer,"Save File", options=options)
        if fileName:
            source = fileName + "//"
            self.FileManager.createNewSlidesFile(source)
            self.reloadSlides()
            print(source)
            
    def loadFile(self):
        # load a file here
        self.FileManager.makeCWD("testScripts")

        options = qw.QFileDialog.Options()
        options |= qw.QFileDialog.DontUseNativeDialog
        options |= qw.QFileDialog.ShowDirsOnly
        directory = qw.QFileDialog.getExistingDirectory(self.RomExplorer, "Load File", "", options=options)
        if directory:
            source = directory + "//"
            print(source)
            self.FileManager.loadSlidesFile(source)
            self.reloadSlides()
    
    def saveFile(self):
        # save currentSlide
        slideString = "Slide {}".format(self.MasterModel.currentSlide)
        self.FileManager.saveSlide(slideString, self.MasterModel.TactileDisplay.return_desiredState())

        
    def reloadSlides(self):
        # clear all the slide buttons and reload the slides
        for slide in self.MasterModel.slidesDictionary.values():
            self.RomExplorer.rightToolBar.removeAction(slide)
            
        self.MasterModel.nSlides = 0
        self.MasterModel.currentSlide = 0
        self.MasterModel.slidesDictionary.clear()
        
        self.createSlideButtons(self.FileManager.currentNumSlides())
        
    def createSlideButtons(self, nSlides):
        
        for i in range(1,nSlides + 1):
            self.addSlide(i)
    
        self.MasterModel.currentSlide = 1
        
    def overwriteSlide(self):
        
        mat = self.MasterModel.getSlideData()
        print(mat)
        slideString = "Slide {}".format(self.MasterModel.currentSlide)
        self.FileManager.saveSlide(slideString, mat)
        
        
    def addSlide(self, slideNum):
        # adds QPushButton to self.RomExplorer.rightToolBar
        self.MasterModel.nSlides += 1
        slideString = "Slide {}".format(slideNum)
        
        # creates a QPushButton instance for this slide
        button = qw.QPushButton(slideString, self.RomExplorer)
        button.clicked.connect(lambda: self.MasterModel.loadSlide(slideNum))
        
        # adds the push button to the slides dictionary and rightToolBar
        buttonAction = self.RomExplorer.rightToolBar.addWidget(button)
        self.MasterModel.slidesDictionary[slideString] = buttonAction
        
    def createSlide(self, slideNum):
        slideString = "Slide {}".format(slideNum)
        # add a slide.csv to cwd
        nColumns = self.MasterModel.displaySize[1]
        nRows = self.MasterModel.displaySize[0]
        
        dummyTestFile = [[0 for i in range(0, nColumns)] for j in range(0, nRows)]
        self.FileManager.saveSlide(slideString, dummyTestFile)
        self.addSlide(slideNum)
        
        
    def removeSlide(self, slideNum):
        # removes a QPushButton from self.RomExplorer.rightToolBar depending on the slide num
        if self.MasterModel.nSlides > 0:
            slideString = "Slide {}".format(slideNum)
            self.MasterModel.nSlides -= 1
            
            # remove widget from the rightToolBar
            self.RomExplorer.rightToolBar.removeAction(self.MasterModel.slidesDictionary[slideString])
            
            # delete slide.csv from cwd
            #self.FileManager.deleteSlide(slideString)
            
            # delete the dictionary instance
            del self.MasterModel.slidesDictionary[slideString]
        else:
            # all slides gone
            pass
            
    def loadSlide(self, slideNum):
        # grab a slide.csv from the cwd
        self.MasterModel.currentSlide = slideNum
        slideString = "Slide {}".format(slideNum)
        
        #print(self.MasterModel.currentSlide)
        canvas = self.FileManager.openSlide(slideString)
        
        # set the current canvas to the new slide
        self.MasterModel.CanvasNavigation.setCanvas(canvas)
        
        # update the braille display with the new canvas
        self.MasterModel.updateViewSpace()
        