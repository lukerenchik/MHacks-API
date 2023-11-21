# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 15:02:37 2023

@author: Derek Joslin

"""

import RomAPI as rs
import PongModel as am
import PongOperations as ao

#import RomRunner as rr



class PongStartMenu(rs.RomState):
    
    def __init__(self, Controller):
        #user can make custom state intialization 
        super().__init__(Controller)
        self.PongGraphicsRender = self.Controller.PongGraphicsRender
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
        
class PongGame(rs.RomState):
    
    def __init__(self, Controller):
        #user can make custom state intialization
        super().__init__(Controller)
        self.HAppControlCenter = self.Controller.HAppControlCenter
        self.TactileDisplay = self.HAppControlCenter.getPeripheral("NewHaptics Display SarissaV1")
        self.GameFlag = self.Controller.GameFlag
        self.PongGraphicsRender = self.Controller.PongGraphicsRender
        self.PongKeyboardHandles = self.Controller.PongKeyboardHandles

        self.displayText = ""

        #self.counter = 0

    def stepState(self):
        #redefined by user in the appropriate subclass
        #print('Editor running')
        self.PongModel.mainGameLoop()
        #self.Controller.HAppControlCenter.interruptExecute(lambda: self.PongModel.gameGraphicsRender())

            
    def startState(self):
        #create a text editor object for this state
        print('Text Editor Begin')
        # create Pong model
        self.PongModel = am.PongModel(self.GameFlag, 0)
        
        # create the keyboard that operates on the Pong model
        self.PongKeyboardHandles.addPongModel(self.PongModel)
        
        # create the mouse handles that operate on the model
        #self.PongMouseHandles = amo.PongMouseHandles(self.PongModel, self.Controller.HAppControlCenter)

# =============================================================================
#         # create a mouse peripheral and then set the handles for the mouse
#         MousePeripheral = self.Controller.HAppControlCenter.getPeripheral("Master Mouse")
#         MousePeripheral.setNewMouseHandler(self.PongMouseHandles)
# =============================================================================
        
    def closeState(self):
        #clear the screen of all information and shut down start screen processes
        
        print('End Menu Close')

    def getNextState(self):
        if self.GameFlag.gameState == "Score Menu":
            return "Game"
        else:
            return self.GameFlag.gameState
            
class PongExitState(rs.RomState):
    
    def __init__(self, Controller):
        #user can make custom state intialization 
        super().__init__(Controller)
        self.PongGraphicsRender = self.Controller.PongGraphicsRender
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