# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 16:40:30 2022

@author: Derek Joslin
"""


import RomAPI as rs
import SlidesOperations as no
import SlidesMaster as sm


class SlidesStartMenu(rs.RomState):
    
    def __init__(self, Controller):
        #user can make custom state intialization 
        super().__init__(Controller)

    def stepState(self):
        #redefined by user in the appropriate subclass
        print('state running')
        
    def startState(self):
        #display the start screen
        #self.Controller.addEngineFunction(self.bootMenu)
        print('Start Menu Began')
        
        
    def closeState(self):
        #clear the screen of all information and shut down start screen processes
        print('Start Menu Close')


    def getNextState(self):
        #get values for the truth table
        romContinue = self.Controller.getInterruptFlagTrigger('romContinue')
        romEscape = self.Controller.getInterruptFlagTrigger('romEscape')
        
        #truth table for start Menu
        if romContinue:
            #exit the current state and rom entirely 
            
            return 'Text Editor'
        
        elif romEscape:
            
            print("hi")
            
            return 'Start Menu'
        
        else:
            #continue with program execution
        
            return 'Text Editor'
        
class SlidesTool(rs.RomState):
    
    def __init__(self, Controller):
        #user can make custom state intialization 
        super().__init__(Controller)
        self.BrailleDisplay = self.Controller.HAppControlCenter.getPeripheral("NewHaptics Display SarissaV1")
        self.displayText = ""

        #self.counter = 0

    def stepState(self):
        #redefined by user in the appropriate subclass
        #print('Editor running')
        pass
# =============================================================================
#         if len(self.TextEditor.inputCommand) > 0:
#             try:        
#                 output = self.Controller.OperationsController.matlabEvaluate(self.TextEditor.inputCommand)
#                 print(output)
#             except:
#                 print("failed to execute matlab operation")
#             self.TextEditor.inputCommand = ""
#             
#         else:
#             pass
# =============================================================================
            
    def startState(self):
        
        #create a text editor object for this state
        print('Slides Tools Begin')
        self.MasterModel = sm.SlidesMaster(self.Controller)
        self.MasterModel.selectTool("drawDot")
        
        # set the mouse handler for the rom
        MousePeripheral = self.Controller.HAppControlCenter.getPeripheral("Master Mouse")
        MousePeripheral.setNewMouseHandler(self.MasterModel.MouseHandles)
        
        # set the keyboard handler for the rom
        KeyboardPeripheral = self.Controller.HAppControlCenter.getPeripheral("Master Keyboard")
        KeyboardPeripheral.setNewKeyboardHandler(self.MasterModel.KeyboardHandles)
        
        # set the visualization for the rom
        self.UpdateSlidesGuiOperation = no.UpdateSlidesGuiOperation("Update Slides Operation", self.Controller, self.MasterModel)
        self.Controller.HAppControlCenter.addOperation(self.UpdateSlidesGuiOperation)
                
    def closeState(self):
        #clear the screen of all information and shut down start screen processes
        
        print('End Menu Close')

    def getNextState(self):
        #get values for the truth table
        romContinue = self.Controller.getInterruptFlagTrigger('romContinue')
        romEscape = self.Controller.getInterruptFlagTrigger('romEscape')
        
        #truth table for start Menu
        if romContinue:
            #exit the current state and rom entirely 
            
            return 'Start Menu'
        
        elif romEscape:
            
            return 'Exit Rom'
            
        else:
            #continue with program execution
        
            return 'Text Editor'
        
class SlidesExitState(rs.RomState):
    
    def __init__(self, Controller):
        #user can make custom state intialization 
        super().__init__(Controller)

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
        
        
    def closeState(self):
        #clear the screen of all information and shut down start screen processes
        print('Exit State Close')


    def getNextState(self):
        #get values for the truth table
        self.Controller.setInterruptFlag('romEnd',1)
        
        return 'Exit Rom'
