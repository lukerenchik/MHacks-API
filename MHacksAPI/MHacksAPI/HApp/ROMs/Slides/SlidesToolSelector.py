# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 09:23:28 2022

@author: Derek Joslin
"""

class SlidesToolSelector():

    def __init__(self, toolKeyList, toolParameters):
        
        # tool function key list
        self.toolKeyList = toolKeyList
        
        # tool parameter Dictionary
        self.toolParameters = toolParameters
        
        # parametersKeys needed for the selected tool to execute
        self.parametersToExecute = []
        
        # Tool selected 
        self.selectedTool = 0
        self.selectedToolKey = ""
        self.parameterInputList = []

    def selectTool(self, toolKey):
        
        # selects the appropriate tool from the tools dictionary
        if toolKey in self.toolKeyList:
            self.selectedTool = toolKey
            print("The {} tool has been selected".format(toolKey))
            
            # get the parameters needed for tool to execute
            self.parameterInputList.clear()
            self.parametersToExecute = self.toolParameters[toolKey]
            
        else:
            print("Error: Invalid tool selected")

    def inputParameter(self, parameterValue):
        # add parameterKey to the parameter List
        self.parameterInputList.append(parameterValue)
        #print("This is the current list of inputs {}".format(self.parameterInputList))
        
        # Check if the list of parameters for the selected tool has reached the required length
        if len(self.parametersToExecute) == len(self.parameterInputList):
            
            # Define a dictionary of parameters
            parameterKwargs = {}
            for index,parameterKey in enumerate(self.parametersToExecute):
                parameterKwargs[parameterKey] = self.parameterInputList[index]

            # If the list of parameters has reached the required length, execute the tool's function
            self.parameterInputList.clear()
            
            # return the data needed to execute the operation in the kernal
            
            return (self.selectedTool, parameterKwargs)
            
        else:
            
            return 0