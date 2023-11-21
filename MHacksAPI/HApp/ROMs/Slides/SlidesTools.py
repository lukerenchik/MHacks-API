# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 16:59:15 2022

@author: Derek Joslin
"""


import inspect

class SlidesTools():

    def __init__(self, BrailleDisplay):
        # assign the braille display api object
        self.BrailleDisplay = BrailleDisplay
        
        # create a dictionary to hold functions from SlidesTools
        self.toolFunctions = {}
        
        # create a dictionary to hold parameters from SlidesTools
        self.toolParameters = {}
        
        # get a list of all methods in the SlidesTools class
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        
        # iterate over the list of methods and add each method to the dictionary
        for toolKey, method in methods:
            if toolKey != "__init__":
                self.toolFunctions[toolKey] = method
            
                
                # get the list of parameters for the current method
                parameters = inspect.signature(method).parameters
                parameters = parameters.items()
                parameterKeys = [k for k, v in parameters]
                
                # create a dictionary for the current method that adds each parameter to a list
                self.toolParameters[toolKey] = parameterKeys
                
# =============================================================================
#         # print the dictionary
#         for tool in self.toolFunctions:
#             print("the tool is {}".format(tool))
#             params = self.toolParameters[tool]
#             print("it's parameters are {}".format(params))
# =============================================================================
            
            
            
            
    def executeSelectedTool(self):
        # execute the selected tool with its parameters
        self.selectedTool(**self.toolParameterKwargs)
        
    def setTool(self, toolFunctionHandle, toolParameterKwargs):
        # set the tool to execute with its parameter arguements
        self.selectedTool = toolFunctionHandle
        self.toolParameterKwargs = toolParameterKwargs

    #cursor tools
    def erase(self):
        self.BrailleDisplay.erase("on/off-E")
        
    def fill(self):
        self.BrailleDisplay.fill("on/off-F")
    
    def stroke(self):
        self.BrailleDisplay.stroke("({stroke size})")

    #shape tools
    def drawDot(self, coord1):
        print("drawing dot at {0}".format(coord1))
        self.BrailleDisplay.dot(coord1)
    
    def drawCell(self, coord1):
        self.BrailleDisplay.cell(coord1)
    
    def drawLine(self, coord2, coord1):
        print("drawing line at {0},{1}".format(coord1, coord2))
        self.BrailleDisplay.line(coord2, coord1)
    
    def drawCurve(self, coord4, coord3, coord2, coord1):
        
        self.BrailleDisplay.curve(coord4, coord3, coord2, coord1)
    
    def drawCircle(self, coord1, radius):
        self.BrailleDisplay.circle(coord1, radius)
    
    def drawRectangle(self, coord2, coord1):
        print("drawing rectangle at {0},{1}".format(coord1, coord2))
        self.BrailleDisplay.rect(coord2, coord1)
    
    def drawTriangle(self, coord3, coord2, coord1):
        self.BrailleDisplay.triangle(coord3, coord2, coord1)
    
    def drawPolygon(self, list1):
        self.BrailleDisplay.polygon(list1)

    #character tools
    def braille(self, coord1, text):
        self.BrailleDisplay.braille(coord1, text)

    #load tools
    def load(self, matrix):
        self.BrailleDisplay.setMat(matrix)

    #control actions
    def clear(self):
        self.BrailleDisplay.clear()
    
    def Fclear(self):
        self.BrailleDisplay.Fclear()
    
    def times(self, now):
        self.BrailleDisplay.times(now)
    
    def setMat(self, matrix):
        self.BrailleDisplay.setMat(matrix)

    #board actions
    def connect(self, com):
        
        self.BrailleDisplay.connect(com)
        
    def connectTouch(self, com):
        
        self.BrailleDisplay.connectTouch(com)
    
    def disconnect(self):
    
        self.BrailleDisplay.disconnect()
    
    def disconnectTouch(self):
    
        self.BrailleDisplay.disconnectTouch()
    
    def refresh(self):
    
        self.BrailleDisplay.refresh()
    
    def direct(self, on_off):
    
        self.BrailleDisplay.direct(on_off)

    #cursor tools
    def selectErase(self):
        
        self.BrailleDisplay.erase("on/off-E")

    #character tools
    def selectCharacter(self, coord1):
        
        self.BrailleDisplay.dot(coord1)

    #load tools
    def selectDot(self, coord1):
        
        self.BrailleDisplay.dot(coord1)

    #control tools
    def selectClear(self):
        
        self.BrailleDisplay.clear()

    #board tools
    def selectConnect(self, com):
        
        self.BrailleDisplay.connect(com)

    #help tools
    def selectSettings(self):
        
        self.BrailleDisplay.settings()

    #misc tools
    def toggleInput(self, onOff):
        
        self.BrailleDisplay.onOff(onOff)

    def adjustStrokeSize(self, strokeSize):
        
        self.BrailleDisplay.strokeSize(strokeSize)

    def selectFontSize(self, fontSize):
        
        self.BrailleDisplay.fontSize(fontSize)

    def toggleDirect(self, onOff):
        
        self.BrailleDisplay.directOnOff(onOff)

    def selectEraseOnOff(self, onOff):
        
        self.BrailleDisplay.eraseOnOff(onOff)

    def toggleFill(self, onOff):
        
        self.BrailleDisplay.fillOnOff(onOff)