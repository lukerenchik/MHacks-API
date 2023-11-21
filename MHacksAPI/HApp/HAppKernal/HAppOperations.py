# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 14:07:19 2022

@author: Derek Joslin

"""

from PyQt5 import QtCore as qc
#import matlab.engine

""" essentially the main loop of the application """

class HAppOperationControl():
    
    def __init__(self, Engine, KeyboardHandler, MouseHandler):
        
        super().__init__()
        
        # peripheral control
        self.BrailleDisplay = Engine
        self.KeyboardHandler = KeyboardHandler
        self.MouseHandler = MouseHandler
        
        # include the rom runner
   
        
   
        # keeps track of rom gui objects and operations
        self.peripheralsDictionary = {}
        self.visualizationsDictionary = {}
        self.operationsDictionary = {}
        
        
        #self.matlabEngine = matlab.engine.start_matlab() #"-desktop"
        self.isPaused = 0
        
    def setVisualization(self, visualizationString, VisualizationHandler):
        self.visualizationsDictionary[visualizationString] = VisualizationHandler
        
    def setVisualizationHandler(self, visualizationString, VisualizationHandles):
        self.visualizationsDictionary[visualizationString].setNewRomVisualizationHandler(VisualizationHandles)
        
    def getVisualization(self, visualizationString):
        return self.visualizationsDictionary[visualizationString]
        
    def setOperation(self, operationString, Operation):
        #add an operation to the operations dictionary
        self.operationsDictionary[operationString] = Operation
        
    def getOperation(self, operationString):
        return self.operationsDictionary[operationString]
        
    def singleExecuteOperation(self, Operation):
        # Executes the operation a single time
        Operation.execute()
        
    def startExecutingOperations(self, timeInterval):
        self.setInterval(timeInterval)
        self.timeout.connect(self.executeOperations)
        self.start()
        
    def stopExecutingOperations(self):
        self.stop()
        
    def pauseExecutingOperations(self):
        self.isPaused = 1
        
    def resumeExecutingOperations(self):
        self.isPaused = 0
        
    def executeOperations(self):
        if self.isPaused:
            pass
        else:
            operationsToExecute = [self.operationsDictionary]
            for opDictionary in operationsToExecute:
                for key in opDictionary:
                    Operation = opDictionary[key]
                    #do something to execute it
                    Operation.execute()
                    pass
        
    def stopExecutingOperation(self, operationString):
       Operation = self.operationsDictionary[operationString]
       print(operationString + " has stopped executing")
       Operation.stopOperation()
    
    def startExecutingOperation(self, operationString):
       Operation = self.operationsDictionary[operationString]
       Operation.startOperation()
    
    def restartExecutingOperation(self, operationString):
        Operation = self.operationsDictionary[operationString]
        Operation.restartOperation()
    
    def matlabEvaluate(self, inputCommand):
        response = 1#self.matlabEngine.eval(inputCommand)
        return response
    
class HAppOperation(qc.QTimer):
    
    def __init__(self):
        self.operationOn = 1
        super().__init__()
        
    def execute(self):
        self.defaultHappOperation()

    def delayedExecute(self):
        self.singleShot(10, self.defaultHappOperation())

    def startOperation(self):
        #starts the HApp operation
        self.setInterval(10)
        self.timeout.connect(self.defaultHappOperation)
        self.start()

    def stopOperation(self):
        #stops the HApp operation
        self.operationOn = 0
        self.stop()

    def pauseOperation(self):
        #pauses the HApp operation
        pass
        
    def restartOperation(self):
        pass
        
        
    def defaultHappOperation(self):
        print("this is the default HApp operation")
        