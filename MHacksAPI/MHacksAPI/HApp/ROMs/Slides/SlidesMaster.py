# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 09:17:50 2022

@author: Derek Joslin
"""

import SlidesToolSelector as sts
import SlidesOperations as so
import SlidesMouse as sm
import SlidesKeyboard as sk
import SlidesCanvasNav as scn
import SlidesFileManagement as sfm

class SlidesMaster():
    
    def __init__(self, Controller):
        #contains all classes required to run a slides rom
        
        self.Controller = Controller
        
        self.TactileDisplay = self.Controller.HAppControlCenter.getPeripheral("NewHaptics Display SarissaV1")
        self.displaySize = self.TactileDisplay.return_displaySize()
        
        # create the ability to navigate and load slides
        self.FileManager = sfm.SlidesFileManagement(self.Controller.HAppControlCenter.PathManager)

        # Create the tool flag
        self.ToolFlag = so.ToolFlag("ToolFlag")
        self.Controller.HAppControlCenter.addFlag(self.ToolFlag)
        
        # Create the state flag
        self.DisplayFlag = so.DisplayFlag("DisplayFlag")
        self.Controller.HAppControlCenter.addFlag(self.DisplayFlag)
        
        # Create main operations"C://Users//derek//OneDrive//NewHaptics Shared//HapticOS//FC_GUI_API//APIv0.7-Coeus//v0.769-Coeus//testScripts//SlidesTestScripts//SlidesTest3"
        self.ToolExecuterOperation = so.ToolExecutionOperation("ToolExecuterOperation", self.TactileDisplay, self.ToolFlag)
        self.Controller.HAppControlCenter.addOperation(self.ToolExecuterOperation)
        
        # Operation for opening and loading slides
        self.SlideOperation = so.LoadSlideOperation("SlideOperation", self.TactileDisplay, self.DisplayFlag)
        self.Controller.HAppControlCenter.addOperation(self.SlideOperation)
        
        #Create the handlers
        self.MouseHandles = sm.SlidesMouseHandles(self)
        self.KeyboardHandles = sk.SlidesKeyboardHandles(self)
        
        # initialize the super class with the toolKeyList and the toolParameterDictionary
        
        
        # Implement the panning feature for loading the csv
        self.CanvasNavigation = scn.SlidesCanvasNav((19,41))
        
        # slide data storage
        self.nSlides = 0
        self.currentSlide = 0
        self.slidesDictionary = {}
        #super().__init__(toolKeyList, toolParameterDictionary)
        
    def selectTool(self, toolKey):
        # clear all options on the tool
        self.ToolFlag.clearState()
        
        # set the state of the flag to the currently selected tool
        self.ToolFlag.setState(toolKey)
        
        #print(self.ToolFlag.getState())
# =============================================================================
#         super().selectTool(toolKey)
#         # if there are no input parmeters auto execute
#         print(self.parametersToExecute)
#         if len(self.parametersToExecute) == 0:
#             parameterKwargs = {}
#             selectedTool = toolKey
#             
#             print(selectTool)
#             print(parameterKwargs)
#             
#             self.executeTool(selectedTool,parameterKwargs)
# =============================================================================
        
    def parameterClicked(self, parameter):
        # add the parameter to the Tool Flag
        if self.ToolFlag.state:
            self.ToolFlag.addParameter(parameter)
        else:
            print("no tool selected")
# =============================================================================
#         executionResult = self.inputParameter(parameter)
#         
#         if executionResult != 0:
#             # if result of click is not 0 then execute the braille display command
#             selectedTool = executionResult[0]
#             parameterKwargs = executionResult[1]
#             self.executeTool(selectedTool,parameterKwargs)
#         
#         print("Result of click is {}".format(executionResult))
# =============================================================================
        
    def executeTool(self, selectedTool, parameterKwargs):
        print("{} has been executed with {}".format(selectedTool, parameterKwargs))
        
        # temporary function to make a tool operation with appropriate parameters and execute in the kernal
# =============================================================================
#         self.Controller.HAppControlCenter.pauseExecutingOperations()
#         
#         # load the tool function and the parameters into the tool execution operation
#         self.ToolExecuterOperation.setTool(selectedTool, parameterKwargs)
# 
#         # execute the tool operation
#         self.Controller.HAppControlCenter.singleExecuteOperation(self.ToolExecuterOperation)
#         
#         self.Controller.HAppControlCenter.resumeExecutingOperations()
# =============================================================================
        
    def updateViewSpace(self):
        testMatrix = self.CanvasNavigation.extractViewSpace()
        
        self.DisplayFlag.setState(1)
        self.DisplayFlag.setMatrix(testMatrix)
        
# =============================================================================
#         # use matrix data to create an Operation which updates the display
#         self.Controller.HAppControlCenter.pauseExecutingOperations()
#         
#         # create and set load slide operation
#         self.LoadSlideOperation.setSlide(self.CanvasNavigation.extractViewSpace())
#         self.Controller.HAppControlCenter.singleExecuteOperation(self.LoadSlideOperation)
#         
#         self.Controller.HAppControlCenter.resumeExecutingOperations()
# =============================================================================
        
# =============================================================================
#     def getSlideData(self):
#         return self.BrailleDisplay.desired()
# =============================================================================

    def loadNextSlide(self):
        if self.currentSlide < self.nSlides:
            self.currentSlide += 1
            self.loadSlide(self.currentSlide)
        else:
            print("can't load next slide")
        
    def loadPreviousSlide(self):
        if self.currentSlide > 1:
            self.currentSlide -= 1
            self.loadSlide(self.currentSlide)
        else:
            print("can't load previous slide")
        

    def loadSlide(self, slideNum):
        # grab a slide.csv from the cwd
        self.currentSlide = slideNum
        slideString = "Slide {}".format(slideNum)
        print(slideString)
        
        #print(self.currentSlide)
        canvas = self.FileManager.openSlide(slideString)
        
        # set the current canvas to the new slide
        self.CanvasNavigation.setCanvas(canvas)
        
        # update the braille display with the new canvas
        self.updateViewSpace()
        
        
        
        