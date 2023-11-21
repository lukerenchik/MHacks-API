# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 14:34:57 2023

@author: Derek Joslin

"""

import OperationsManager as om
import FlagManager as fm
import PeripheralManager as pm
import VisualizationManager as vm
from PyQt5.QtCore import QTimer 
from PyQt5.QtWidgets import QLabel, QVBoxLayout
import time

""" A class for an object which controls when operations execute and in what order they execute according to the flags set in the application """

class ControlCenter:
    def __init__(self, PathManager):
        self.FlagManager = fm.FlagManager()
        self.OperationManager = om.OperationManager()
        self.PeripheralManager = pm.PeripheralManager()
        self.VisualizationManager = vm.VisualizationManager()
        self.PathManager = PathManager
        
        # list for holding roms
        self.romList = []
        
        # Timer which creates the main loop of the application
        self.operationTimerDictionary = {}
        self.OperationsTimer = QTimer()
        self.OperationsTimer.timeout.connect(self.launchOperations)
        
        
    def addRom(self, Rom):
        self.romList.append(Rom)
        
    def pauseRoms(self):
        for Rom in self.romList:
            Rom.stopEvent.clear()
            
    def resumeRoms(self):
        for Rom in self.romList:
            Rom.stopEvent.set()
        
    def startLaunchingOperations(self, interval):
        self.OperationsTimer.start(interval)
        
    def addFlag(self, Flag):
        self.FlagManager.addFlag(Flag)
        
    def removeFlag(self, flagName):
        self.FlagManager.removeFlag(flagName)
        
    def getFlag(self, flagName):
        return self.FlagManager.getFlag(flagName)
        
    def getAllFlags(self):
        return self.FlagManager.getAllFlags()
        
    def addOperation(self, Operation):
        self.OperationManager.addOperation(Operation)
        
    def killOperation(self, operationName):
        Operation = self.OperationManager.getOperation(operationName)
        Operation.isStopped = 1
        self.stopExecutingOperation(Operation)
        
    def removeOperation(self, operationName):
        self.OperationManager.removeOperation(operationName)
        
    def getOperation(self, operationName):
        return self.OperationManager.getOperation(operationName)
        
    def getAllOperations(self):
        return self.OperationManager.getAllOperations()
    
    def interruptExecute(self, func):
        self.pauseRoms()
        func()
        self.resumeRoms()
        
    def addPeripheral(self, Peripheral):
        self.PeripheralManager.addPeripheral(Peripheral)
        
    def removePeripheral(self, peripheralName):
        self.PeripheralManager.removePeripheral(peripheralName)
        
    def getPeripheral(self, peripheralName):
        return self.PeripheralManager.getDevice(peripheralName)
        
    def getAllPeripherals(self):
        return self.PeripheralManager.getAllDevices()
    
# =============================================================================
#     def connectAllDevices(self):
#         self.PeripheralManager.connectAll()
#     
#     def disconnectAllDevices(self):
#         self.PeripheralManager.disconnectAll()
# =============================================================================
    
    def getStatusAllDevices(self):
        self.PeripheralManager.getStatusAll()
        
    def addVisualization(self, Visualization):
        self.VisualizationManager.addVisualization(Visualization)
        
    def removeVisualization(self, visualizationName):
        self.VisualizationManager.removeVisualization(visualizationName)
        
    def getVisualization(self, visualizationName):
        return self.VisualizationManager.getVisualization(visualizationName)
        
    def getAllVisualizations(self):
        return self.VisualizationManager.getAllVisualizations()
    
    def showAllVisualizations(self):
        self.VisualizationManager.showAll()
        
    def debugPrintAllResources(self):
        ARCSDebugText = "ARCS SYSTEM STATUS\n\n"
        ARCSDebugText += self.FlagManager.printAllFlags()
        ARCSDebugText += "\n"
        ARCSDebugText += self.OperationManager.printAllOperations()
        ARCSDebugText += "\n"
        ARCSDebugText += self.VisualizationManager.printAllVisualizations()
        ARCSDebugText += "\n"
        ARCSDebugText += self.PeripheralManager.printAllPeripherals()
        
        return ARCSDebugText
    
# =============================================================================
#     def debugGetResourceLabels(self):
#         # get the labels from each manager
#         flagLabelList = self.FlagManager.getFlagLabels()
#         operationLabelList = self.OperationManager.getOperationLabels()
#         visualizationLabelList = self.VisualizationManager.getVisualizationLabels()
#         peripheralLabelList = self.PeripheralManager.getPeripheralLabels()
#         
#         # create the generic ARCS Label
#         ARCSLabel = QLabel("ARCS SYSTEM STATUS\n\n")
#         ARCSLabelLayout = QVBoxLayout()
#         
#         # create a label for each section
#         FlagLabel = QLabel("ARCS Flags- \n")
#         OperationLabel = QLabel("ARCS Operations- \n")
#         VisualizationLabel = QLabel("ARCS Visualizations- \n")
#         PeripheralLabel = QLabel("ARCS Peripherals- \n")
#         
#         # add all labels in order to ARCSLabelLayout
#         ARCSLabelLayout.addWidget(ARCSLabel)
#         
#         ARCSLabelLayout.addWidget(FlagLabel)
#         for Label in flagLabelList:
#             ARCSLabelLayout.addWidget(Label)
#         
#         ARCSLabelLayout.addWidget(OperationLabel)
#         for Label in operationLabelList:
#             ARCSLabelLayout.addWidget(Label)
#             
#         ARCSLabelLayout.addWidget(VisualizationLabel)
#         for Label in visualizationLabelList:
#             ARCSLabelLayout.addWidget(Label)
#             
#         ARCSLabelLayout.addWidget(PeripheralLabel)
#         for Label in peripheralLabelList:
#             ARCSLabelLayout.addWidget(Label)
# 
#         return ARCSLabelLayout
# =============================================================================
    
    """
    This function uses a QTimer to continuously check all operations in the operation manager. 
    It checks if the Operation should be executed immediately, or if there are flag dependencies that must be 
    met before executing, and if those are met, it will execute the operation or if there is a time delay for executing.
    It also checks if the Operation should execute continuously and if so, it starts the execution of the
    """
    
    def launchOperations(self):
        self.pauseRoms()
        
        for Operation in self.OperationManager.getAllOperations():
                
            if Operation.ExecutionTimer:
                # if operation is running don't start it again
                continue

            # grab all relevant execution information from executionParameters
            
            # determines if it should execute
            executeOnFlags = Operation.executionParameters["executeOnFlags"]
            

            # Check if operation has flag dependencies that haven't been met
            if executeOnFlags:
                if not Operation.checkFlagConditions():#self.checkFlagConditions(executeOnFlags, Operation):
                    # the Operation does not meet all execute flag                    
                    continue

            # if operation made it here it should be executed 
            # below is how it starts execution
    
            # prepare the execute timer
            OperationExecutionTimer = OperationTimer(Operation, self.executeOperation)
            
            # add the timer to the op timer dictionary
            self.operationTimerDictionary[Operation.name] = OperationExecutionTimer
            
            # begin the operation
            OperationExecutionTimer.launchOperation()
        
        self.resumeRoms()
        
    def executeOperation(self, Operation):
        self.pauseRoms()
        
        timeToExecute = time.time()
        
        try:
            # grab all relevant execution information from executionParameters
            # determines the way it should stop execution
            executeTimeLimit = Operation.executionParameters["executionTimeLimit"]
            stopExecuteOnFlags = Operation.executionParameters["stopExecuteOnFlags"]
            stopExecuteDelay = Operation.executionParameters["stopExecuteDelay"]
            
            # Check for stopExecuteOnFlags
            if stopExecuteOnFlags:
                if self.checkFlagConditions(stopExecuteOnFlags):
                    # stop the execution of this Operation after the stop delay
                    QTimer.singleShot(stopExecuteDelay, lambda: self.stopExecutingOperation(Operation))
    
            # Check for how long the timer has been running for and compare to the time limit
            elapsedTime = time.time() - Operation.startTime
                
            Operation.lastExecuteTime = Operation.currentExecuteTime
            Operation.currentExecuteTime = time.time()
            Operation.timeBetween = Operation.currentExecuteTime - Operation.lastExecuteTime
            
            #print(elapsedTime)
            if executeTimeLimit:
                if int(elapsedTime*1000) > executeTimeLimit:
                    # stop the execution of this Operation after the stop delay
                    QTimer.singleShot(stopExecuteDelay, lambda: self.stopExecutingOperation(Operation))
                    
            # if the operation is ready to execute then execute it
            Operation.execute()
            
    
            if Operation.ExecutionTimer.isSingleShot():
                self.stopExecutingOperation(Operation)
                # grab all relevant execution information from executionParameters
                
        except Exception as e:
            print("Failed Operation: {}".format(Operation.name))
            print("An error occurred:")
            print(e)
        
        timeToExecute = time.time() - timeToExecute
        
        self.resumeRoms()
        #print("Operation{} took {} seconds".format(Operation.name, timeToExecute))
            
    def stopExecutingOperation(self, Operation):
        Operation.stopOperation()
        if Operation.isStopped:
            # remove the operation from the dictionary
            self.removeOperation(Operation.name)
            
            # kill the operation timer
            del self.operationTimerDictionary[Operation.name]
        
class OperationTimer(QTimer):
    
    def __init__(self, Operation, executerFunction):
        # start the operations execution with a delay
        super().__init__()
        
        self.Operation = Operation
        self.executerFunction = executerFunction
        self.timeout.connect(lambda: self.executerFunction(self.Operation))
        
        # parameters that determine how it should execute
        self.executeDelay = Operation.executionParameters["executeDelay"]
        self.executeContinuously = Operation.executionParameters["executeContinuously"]
        self.executeIntervalTime = Operation.executionParameters["executionIntervalTime"]
        
    def launchOperation(self):
        self.Operation.startOperation()
        self.Operation.ExecutionTimer = self
        
        if self.executeContinuously:
            # create the the interval
            self.setInterval(self.executeIntervalTime)
            self.setSingleShot(False)
        else:
            # set the operation to execute once
            self.setSingleShot(True)
            
        self.Operation.startTime = time.time()
        QTimer.singleShot(self.executeDelay, self.start)
    
class UpdateMonitorOperation(om.Operation):
    
    def __init__(self, name, ControlCenter, ARCSLabel):
        super().__init__(name)
        # inputs to the operation
        self.ControlCenter = ControlCenter
        self.inputDictionary["ControlCenter"] = self.ControlCenter
        
        # outputs to the operation
        self.ARCSLabel = ARCSLabel
        self.outputDictionary["ARCSLabel"] = self.ARCSLabel
    
        
        # provide a description
        self.description = "Updates the ARCs Monitor label."
        
        # execute the function continuously until otherwise
        executionParameters = {
            "executeDelay": 500, # a delay in milliseconds that starts the execution of the Operation after the flag dependencies have been met
            "executeContinuously": True, # a boolean value that determines if the Operation will execute forever
            "executionIntervalTime": 1, # an interval in milliseconds that determines the time between execution
        }
        
        self.setExecutionParameters(executionParameters)
        
        self.executable = self.execute
        
        self.createDebugString()
    
    def execute(self):
        # update the ARCS status label
        #ARCSLayout = self.ControlCenter.debugGetResourceLabels()
        #self.ARCSLabel.setLayout(ARCSLayout)
        self.ARCSLabel.setText(self.ControlCenter.debugPrintAllResources())
        
        
# =============================================================================
#     
# def func1():
#     print("func1")
#     
# def func2():
#     print("func2")
#     
# if __name__ == '__main__':
#     
#     HAppControlCenter = ControlCenter()
#     
#     # create the flags
#     
#     Flag1 = fm.Flag("flag1")
#     Flag1.setCondition(5)
#     
#     Flag2 = fm.Flag("flag2")
#     Flag2.setCondition(1)
#     
#     # create the operations
#     
#     Operation1 = om.Operation("operation1")
#     Operation1.addFunction(func1)
#     Operation1.addFlagDependencies(4)
#     Operation2 = om.Operation("operation2")
#     Operation2.addFunction(func2)
#     Operation2.addFlagDependencies(Flag2.getCondition())
#     
#     # create the peripherals
#     
#     Peripheral1 = pm.PeripheralDevice("peripheral1")
#     Peripheral2 = pm.PeripheralDevice("peripheral2")
#     
#     # add the resources to the Control Center
#     HAppControlCenter.addFlag(Flag1)
#     HAppControlCenter.addFlag(Flag2)
#     HAppControlCenter.addOperation(Operation1)
#     HAppControlCenter.addOperation(Operation2)
#     HAppControlCenter.addPeripheral(Peripheral1)
#     HAppControlCenter.addPeripheral(Peripheral2)
#     
#     FlagList = HAppControlCenter.getAllFlags()
#     for Flag in FlagList:
#         print(Flag.name)
#         print(Flag.getCondition())
#         
#     OperationList = HAppControlCenter.getAllOperations()
#     for Operation in OperationList:
#         print(Operation.name)
#         print(Operation.flagDependencies)
#         print(Operation.function)
#     
#     PeripheralList = HAppControlCenter.getAllPeripherals()
#     for Peripheral in PeripheralList:
#         print(Peripheral.name)
#         
#     for Flag in FlagList:
#         for Operation in OperationList:
#             if Operation.shouldExecute(Flag):
#                 # execute the function if it's flag is equal to yours
#                 
#                 Operation.execute()
#             
#         
# =============================================================================
