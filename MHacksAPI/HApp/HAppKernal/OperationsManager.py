# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 13:10:00 2023

@author: Derek Joslin

"""

""" class for an object which contains a function that needs to be executed at some point in the program """

from PyQt5.QtWidgets import QLabel

class Operation():
    
    def __init__(self, name):
        self.name = name
        self.description = ""
        self.debugString = ""
        self.executable = self.defaultExecution
        self.ExecutionTimer = None
        self.startTime = None
        self.isStopped = False
        
        # keep trakc of time between exectuion 
        self.lastExecuteTime = 0
        self.currentExecuteTime = 0
        self.timeBetween = 0
        
        # default execution parameter values
        
        # determines if it should execute
        executeOnFlags = None
        
        # determines the way it should start execution
        executeDelay = 0
        executeContinuously = False
        executeIntervalTime = None
        
        # determines the way it should stop execution
        executeTimeLimit = None
        stopExecuteOnFlags = None
        stopExecuteDelay = 0
        
        # default execution parameters
        self.executionParameters = {
        "executeOnFlags": executeOnFlags, # a set of flag dependencies that when met start executing the Operation
        "executeDelay": executeDelay, # a delay in milliseconds that starts the execution of the Operation after the flag dependencies have been met
        "executeContinuously": executeContinuously, # a boolean value that determines if the Operation will execute forever
        "executionIntervalTime": executeIntervalTime, # an interval in milliseconds that determines the time between execution
        "executionTimeLimit": executeTimeLimit, # the time in milliseconds that the operation executes for
        "stopExecuteOnFlags": stopExecuteOnFlags, # a set of flag dependencies that when met stop execution of the Operation
        "stopExecuteDelay": stopExecuteDelay # a delay in milliseconds that determines how long after the stopExecuteOnFlags the Operation Stops
        }
        
        # List inputs to the operation
        self.inputDictionary = {}
        
        # List the outputs to the operation
        self.outputDictionary = {}
        
    def createDebugString(self):
        inputString = "inputs: "
        for inputKey in self.inputDictionary.keys():
            inputString += "{},".format(inputKey)
        inputString += "\n"
        
        outputString = "outputs: "
        for outputKey in self.outputDictionary:
            outputString += "{},".format(outputKey)
        outputString += "\n"
        
        executionString = "execution parameters: "
        for parameter in self.executionParameters.items():
            # only add a parameter if it differs from default
            executionString += "{} = {},".format(parameter[0], parameter[1])
        executionString += "\n"
        
        timeString = "time between executions {}".format(self.timeBetween) + "\n"
        
        self.debugString = inputString + outputString + timeString + self.description
        
    def setFunction(self, func):
        self.function = func
        
    def checkFlagConditions(self):
        return True
    
    def setExecutionParameters(self, parameters: dict[str , any]):
        for key, value in parameters.items():
            if key in self.executionParameters:
                self.executionParameters[key] = value
            
    def getExecutionParameters(self):
        return self.executionParameters

    def execute(self):
        return self.executable()

    def startOperation(self):
        # What to execute when the operation starts
        pass

    def stopOperation(self):
        # What to execute when the operation stops
        if self.ExecutionTimer:
            #print("stopping operation: {}".format(self.name))
            self.ExecutionTimer.stop()
            self.ExecutionTimer.timeout.disconnect()
            #print("did execution stop?: {}".format(self.ExecutionTimer.timerId()))
            del self.ExecutionTimer
        if self.startTime:
            del self.startTime
        self.ExecutionTimer = None
        self.startTime = None
        self.isStopped = True
        
    def restartOperation(self):
        # Reintializes the operation as if it was just created
        pass
        
    def defaultExecution(self):
        print("this is the default operation")
        

class OperationManager():
    
    def __init__(self):
        self.operationDictionary = {}

    def addOperation(self, Operation):
        self.operationDictionary[Operation.name] = Operation
    
    def removeOperation(self, operationName):
        #self.operationDictionary[operationName].stopOperation()
        del self.operationDictionary[operationName]
        
    def getOperation(self, operationName):
        return self.operationDictionary.get(operationName)
        
    def getAllOperations(self):
        return self.operationDictionary.values()
    
    def executeOperation(self, operationName):
        Operation = self.operationDictionary.get(operationName)
# =============================================================================
#         if Operation:
#             # check if all the dependencies are met before executing
#             for flagName in Operation.flagDependencies:
# 
#                 if not flag:
#                     raise ValueError(f"Missing dependency: {flag_name}")
#             return Operation.execute()
# =============================================================================
    
    def printAllOperations(self):
        operationDebugText = "ARCS Operations-\n"
        for Operation in self.operationDictionary.values():
            operationDebugText += "{}\n".format(Operation.name)
            operationDebugText += "{}\n".format(Operation.debugString)
            
# =============================================================================
#             operationDebugText += "----Flag Dependencies: {}\n".format(Operation.flagDependencies)
#             operationDebugText += "----Function: {}\n".format(Operation.function)
# =============================================================================
    
        return operationDebugText
    
    def getOperationLabels(self):
        # create a list of labels for the peripherals
        operationLabelList = []

        for Operation in self.operationDictionary.values():
            # for each peripheral make a label
            Label = QLabel(Operation.name)
            
            # set the tooltip for this label to be the debug text of the peripheral
            Label.setToolTip(Operation.debugString)
            
            # add the perihperal label to the list
            operationLabelList.append(Label)

        return operationLabelList
# =============================================================================
# if __name__ == '__main__':
#     
#     OperationManager = HAppOperationManager()
#     
#     def func1():
#         return "Executed func1"
#     
#     def func2():
#         return "Executed func2"
#     
#     Operation1 = HAppOperation("operation1")
#     Operation2 = HAppOperation("operation2")
#     
#     OperationManager.addOperation(Operation1)
#     OperationManager.addOperation(Operation2)
#     
#     print(OperationManager.getAllOperations())
#     # Output: "Executed func1"
# =============================================================================

    