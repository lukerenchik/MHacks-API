# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 15:11:53 2022

@author: Derek Joslin
"""

import RomAPI as rs

class SampleStartMenu(rs.RomState):
    
    def __init__(self, Controller):
        #user can make custom state intialization 
        super().__init__(Controller)

    def stepState(self):
        #redefined by user in the appropriate subclass
        #print('state running')
        pass
    
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
            
            return 'End Menu'
        
        elif romEscape:
            
            print("hi")
            
            return 'Start Menu'
        
        else:
            #continue with program execution
        
            return 'Start Menu'
        
class SampleEndMenu(rs.RomState):
    
    def __init__(self, Controller):
        #user can make custom state intialization 
        super().__init__(Controller)
        #self.counter = 0

    def stepState(self):
        #redefined by user in the appropriate subclass
        #print('state running')
        pass
    
    def startState(self):
        #display the start screen
        #self.Controller.addEngineFunction(self.bootMenu)
        print('End Menu Began')
        
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
        
            return 'End Menu'
        
        
class ExitState(rs.RomState):
    
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