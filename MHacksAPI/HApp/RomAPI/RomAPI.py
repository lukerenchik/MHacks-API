# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 11:18:01 2022

@author: Derek Joslin
"""

import ctypes
import DefaultKeyboardHandles as dh
import DefaultMouseHandles as dm
import DefaultRomVisualizationHandles as dr
import OperationsManager as om
import FlagManager as fm


class RomControlBus:

    def __init__(self, interruptDictionaryAddress):
        self.interruptDictionary = ctypes.cast(interruptDictionaryAddress, ctypes.py_object).value
        self.interruptGrabDictionary = {}
        for key in self.interruptDictionary:
            self.interruptGrabDictionary[key] = 0
            

    def getInterruptFlag(self, interruptString):
        interruptValue = self.interruptDictionary[interruptString]
        return interruptValue
    
    def setInterruptFlag(self, interruptString, interruptValue):
        self.interruptDictionary[interruptString] = interruptValue


    def getInterruptFlagTrigger(self, interruptString):
        
        #check to see if the interrupt is active
        if self.interruptDictionary[interruptString] == 0:
            self.interruptGrabDictionary[interruptString] = 0
            return 0
            
        #if the interrupt is active see if it has been grabbed
        elif self.interruptGrabDictionary[interruptString]:
            return 0
        else:
            self.interruptGrabDictionary[interruptString] = 1
            interruptValue = self.interruptDictionary[interruptString]
            return interruptValue


class RomController(RomControlBus):
    
    def __init__(self, interruptDictionaryAddress, ControlCenterAddress, romSettings, debug):
        
        #intialize the control interrupt super class
        super().__init__(interruptDictionaryAddress)
        
        
        #define the state objects (user reimplements this and adds to dictionary)
# =============================================================================
#         self.StartMenu = StartMenu()
#         self.Game = Avalanche()
#         self.ScoreMenu = ScoreMenu()
# =============================================================================
        
        
        #current state of rom (user can intialize a default state)
        self.stateKey = ''
        
# =============================================================================
#         self.stateKey = 
# =============================================================================
        
        #available states for the rom
        self.romStateDictionary = {}
        
# =============================================================================
#         self.romStateDictionary = { 'Avalanche Start Menu' : self.StartMenu,
#                                     'Avalanche Game' : self.Game,
#                                     'Avalanche Score': self.ScoreMenu }
# =============================================================================
        
        #default api functionality
        self.HAppControlCenter = ctypes.cast(ControlCenterAddress, ctypes.py_object).value
        
        #default debug option
        self.debug = debug
        
        #list to hold api functions which need to be executed
        self.engineExecutionBuffer = []
        
        def initializeSize():
            BrailleDisplay = self.HAppControlCenter.getPeripheral("NewHaptics Display SarissaV1")
            displaySize = BrailleDisplay.return_displaySize()
            self.nRows = displaySize[0]
            self.nColumns = displaySize[1]
            
        self.addEngineFunction(initializeSize)

        #game settings (user reimplements)
# =============================================================================
#         self.baseFallTime = romSettings['baseFallTime']
#         self.difficultyRate = romSettings['difficultyRate']
#         self.difficultySetting = romSettings['difficultySetting']
# =============================================================================
        
    def startCurrentState(self):
        #get the current rom that is running and run its step function
        currentState = self.getCurrentState()
        
        currentState.startState()
        
    def stepCurrentState(self):
        #get the current rom that is running and run its step function
        currentState = self.getCurrentState()
        
        currentState.stepState()

        
        
    def decideNextState(self):

        #get the rom's current state
        currentState = self.getCurrentState()
        oldStateKey = self.stateKey
        
        #calculate which state to go to next from current state
        newStateKey = currentState.getNextState()

        #if new State Key is rom exit exit rom immediately
        #switch to the next rom state or if the same state do nothing
        if oldStateKey == newStateKey:
            pass
        
        else:
            #close all operations of the current state
            currentState.closeState()
            
            #initialize all of the operations of the next state
            nextState = self.romStateDictionary[newStateKey]
            nextState.startState()
            
            #switch to the next state
            self.switchState(newStateKey)
            

    def runEngineBuffer(self):
        #reimplemented by user to run all functions used across applications like nhapi or the serial port

        #loop through the buffer and execute all required functions
        for function in self.engineExecutionBuffer:
            #execute the function
            function()
    
    def getCurrentState(self):
        return self.romStateDictionary[self.stateKey]

    def switchState(self, stateKey):
        self.stateKey = stateKey
    
    def addEngineFunction(self, function):
        self.engineExecutionBuffer.append(function)
    
    def exitRom(self):
        pass
        
        
class RomState():
    
    def __init__(self, Controller):
        #pass the rom controller into the state
        self.Controller = Controller
    
    def stepState(self):
        #redefined by user in the appropriate subclass
        pass

    def startState(self):
        #display the start screen
        #self.Controller.addEngineFunction(self.bootMenu)
        pass
        
    def closeState(self):
        #clear the screen of all information and shut down start screen processes
        pass

    def getNextState(self, RomController):
        #get values for the truth table
        pass
        
# =============================================================================
#         romEscape = RomController.getInterruptFlag('romEscape')
#         romContinue = RomController.getInterruptFlag('romContinue')
#         romEnd = RomController.getInterruptFlag('romEnd')
#         
#         #truth table for start Menu
#         if romEnd:
#             #exit the current state and rom entirely 
#             
#             return 'Exit Rom'
#             
#         elif romEscape:
#             #restart the start menu
#             self.startState()
#             
#             
#             return 'Avalanche Start Menu'
#             
#         elif romContinue:
#             #move to the next state
#             
#             return 'Avalanche Game'
#         
#         else:
#             #continue with program execution
#         
#             return 'Avalanche Start Menu'
# =============================================================================
        
        
# =============================================================================
#     def bootMenu(self):
#         brailleString = "press space key to start"
#         self.engine.clear()
#         
#         print(brailleString)
#         self.engine.braille((0,0),brailleString)
#         self.engine.desired()
#         self.engine.refresh()
#         self.engine.state()
# =============================================================================
        


class RomKeyboardHandles(dh.DefaultKeyboardHandles):
    
    def __init__(self):
        super().__init__()
        
class RomMouseHandles(dm.DefaultMouseHandles):
    
    def __init__(self):
        super().__init__()
        
class RomOperation(om.Operation):
        
    def __init__(self, name):
        super().__init__(name)
        
class RomFlag(fm.Flag):
    
    def __init__(self, name):
        super().__init__(name)
        
class RomVisualizationHandles(dr.DefaultRomVisualizationHandles):
        
    def __init__(self):
        super().__init__()
        
