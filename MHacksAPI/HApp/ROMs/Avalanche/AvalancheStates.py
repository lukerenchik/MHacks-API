# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 16:53:40 2023

@author: Derek Joslin

"""

import RomAPI as rs
import AvalancheModel as am
import AvalancheOperations as ao

#import RomRunner as rr



class AvalancheStartMenu(rs.RomState):
    
    def __init__(self, Controller):
        #user can make custom state intialization 
        super().__init__(Controller)
        self.AvalancheGraphicsRender = self.Controller.AvalancheGraphicsRender
        self.GameFlag = self.Controller.GameFlag
        
    def stepState(self):
        #redefined by user in the appropriate subclass
        # print('state running')
        pass
        
    
    def startState(self):
        #display the start screen
        #self.Controller.addEngineFunction(self.bootMenu)
        print('Start Menu Began')
        self.GameFlag.setState(1)
                
    def closeState(self):
        #clear the screen of all information and shut down start screen processes
        print('Start Menu Close')


    def getNextState(self):
        #determin the next state
        return self.GameFlag.gameState
        
class AvalancheGame(rs.RomState):
    
    def __init__(self, Controller):
        #user can make custom state intialization
        super().__init__(Controller)
        self.HAppControlCenter = self.Controller.HAppControlCenter
        self.TactileDisplay = self.HAppControlCenter.getPeripheral("NewHaptics Display SarissaV1")
        self.GameFlag = self.Controller.GameFlag
        self.AvalancheGraphicsRender = self.Controller.AvalancheGraphicsRender
        self.AvalancheKeyboardHandles = self.Controller.AvalancheKeyboardHandles

        self.displayText = ""

        #self.counter = 0

    def stepState(self):
        #redefined by user in the appropriate subclass
        #print('Editor running')
        self.AvalancheModel.mainGameLoop()
        #self.Controller.HAppControlCenter.interruptExecute(lambda: self.AvalancheModel.gameGraphicsRender())

            
    def startState(self):
        #create a text editor object for this state
        print('Text Editor Begin')
        # create avalanche model
        size = self.TactileDisplay.return_displaySize()
        self.AvalancheModel = am.AvalancheModel(self.GameFlag, size, 0)
        
        # create the keyboard that operates on the avalanche model
        self.AvalancheKeyboardHandles.addAvalancheModel(self.AvalancheModel)
        
        # create the mouse handles that operate on the model
        #self.AvalancheMouseHandles = amo.AvalancheMouseHandles(self.AvalancheModel, self.Controller.HAppControlCenter)

# =============================================================================
#         # create a mouse peripheral and then set the handles for the mouse
#         MousePeripheral = self.Controller.HAppControlCenter.getPeripheral("Master Mouse")
#         MousePeripheral.setNewMouseHandler(self.AvalancheMouseHandles)
# =============================================================================
        
    def closeState(self):
        #clear the screen of all information and shut down start screen processes
        
        print('End Menu Close')

    def getNextState(self):
        if self.GameFlag.gameState == "Score Menu":
            return "Game"
        else:
            return self.GameFlag.gameState
            
class AvalancheExitState(rs.RomState):
    
    def __init__(self, Controller):
        #user can make custom state intialization 
        super().__init__(Controller)
        self.AvalancheGraphicsRender = self.Controller.AvalancheGraphicsRender
        self.GameFlag = self.Controller.GameFlag


    def stepState(self):
        #redefined by user in the appropriate subclass
        #print('state running')
        #print('Exit State Print')
        pass
        #print("disconnected")
    
    def startState(self):
        #display the start screen
        #self.Controller.addEngineFunction(self.bootMenu)
        print('Exit State Began')
        self.GameFlag.setState(1)
        
    def closeState(self):
        #clear the screen of all information and shut down start screen processes
        print('Exit State Close')


    def getNextState(self):
        #get values for the truth table
        self.Controller.setInterruptFlag('romEnd',1)
        
        return 'Exit Rom'