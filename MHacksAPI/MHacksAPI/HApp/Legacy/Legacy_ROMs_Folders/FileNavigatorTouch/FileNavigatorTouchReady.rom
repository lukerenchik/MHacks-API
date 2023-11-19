# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 10:29:05 2022

@author: Derek Joslin
"""

"""
@RomInputsBegin
#a dictionary to store the rom interrupts WARNING: will not compile as is a dictionary needs to be allocated to memory first
interruptDictionaryAddress = id({'romEscape': 0, 'romContinue': 0, 'romEnd': 0, 'romHaltSerial': 0, 'isSerialHalted': 0})
#api for using the braille tablet
OperationsControlAddress = id(HAppOperationControl)
#controls which number is displayed in demo
demoNumber = 100
#classic debug toggle 1-on 0-off
echo = 0
@RomInputsEnd
"""

import RomAPI as rs

import NotePadStates as ns


class NotePadController(rs.RomController):
    
    def __init__(self, interruptDictionaryAddress, OperationsAddress, romSettings, debug):

        super().__init__(interruptDictionaryAddress, OperationsAddress, romSettings, debug)
        

        #initialize all state objects and pass in the controller
        self.NotePadStartMenu = ns.NotePadStartMenu(self)
        
        self.NotePadTextEditor = ns.NotePadTextEditor(self)
        
        self.EndRom = ns.NotePadExitState(self)
        
        #current state of rom (user can intialize a default state)
        self.stateKey = 'Start Menu'


        #available states for the rom
        self.romStateDictionary = {'Start Menu' : self.NotePadStartMenu,
                                   'Text Editor' : self.NotePadTextEditor,
                                   'Exit Rom' : self.EndRom}

        self.demoNumber = romSettings['demoNumber']
        
    def exitRom(self):
        #self.engine.disconnect()
        print("disconnected")
        


#settings specific to the rom
romSettings = { 'demoNumber': int(demoNumber) }

ThisRom = NotePadController(interruptDictionaryAddress, OperationsControlAddress, romSettings, int(echo))


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

        
        