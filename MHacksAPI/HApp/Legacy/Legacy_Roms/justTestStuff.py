# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 17:02:19 2022

@author: Derek Joslin
"""

"""
@RomInputsBegin
#a dictionary to store the rom interrupts WARNING: will not compile as is a dictionary needs to be allocated to memory first
interruptDictionaryAddress = id({'romEscape': 0, 'romContinue': 0, 'romEnd': 0, 'romHaltSerial': 0, 'isSerialHalted': 0})
#api for using the braille tablet
BrailleDisplayAddress = id(engine)
#controls which number is displayed in demo
demoNumber = 100
#classic debug toggle 1-on 0-off
echo = 0
@RomInputsEnd
"""

import RomAPI as rs


class SampleController(rs.RomController):
    
    def __init__(self, interruptDictionaryAddress, engine, romSettings, debug):

        super().__init__(interruptDictionaryAddress, engine, romSettings, debug)
        
        #keyboard handler
        self.keyboard = TextKeyboard()
        
        #initialize all state objects and pass in the controller
        self.SampleStartMenu = SampleStartMenu(self)
        
        self.SampleEndMenu = SampleEndMenu(self)
        
        self.EndRom = ExitState(self)
        
        #current state of rom (user can intialize a default state)
        self.stateKey = 'Start Menu'

        #available states for the rom
        self.romStateDictionary = {'Start Menu' : self.SampleStartMenu,
                                   'End Menu' : self.SampleEndMenu,
                                   'Exit Rom' : self.EndRom}

        self.demoNumber = romSettings['demoNumber']
        
    def exitRom(self):
        self.engine.disconnect()
        print("disconnected")
        
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
        
    
    
    
class TextKeyboard(rs.RomKeyboard):
    
    
    def __init__(self, Controller):
        #user can make custom state intialization 
        super().__init__(Controller)
    
        
    def releaseWKey(self):
        currentState = self.Controller.getCurrentState()
        
        currentState.wKeyReleased()
        
        
        pass
    
    def holdWKey(self):
        pass
    
        
    def pressWKey(self):
        pass
    
    
    
    

#settings specific to the rom
romSettings = { 'demoNumber': int(demoNumber) }

ThisRom = SampleController(interruptDictionaryAddress, BrailleDisplayAddress, romSettings, int(echo))


shouldRomEnd = ThisRom.getInterruptFlag('romEnd')


#Main loop of the Rom
while shouldRomEnd == 0:
    
    #always step one tick into the current state
    ThisRom.stepCurrentState()
    
    #decide if peripheral communication is going to occur
    #Put NHAPI functions in here
    ThisRom.runEngineBuffer()
    
    #decide the next state to move into
    ThisRom.decideNextState()
    
    
    
    shouldRomEnd = ThisRom.getInterruptFlag('romEnd')
    
else:
    ThisRom.exitRom()

        
        