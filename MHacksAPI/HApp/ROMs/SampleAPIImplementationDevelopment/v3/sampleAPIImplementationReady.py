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


class SampleController(rs.RomController):
    
    def __init__(self, interruptDictionaryAddress, OperationsAddress, romSettings, debug):

        super().__init__(interruptDictionaryAddress, OperationsAddress, romSettings, debug)
        
        #create rom keyboard handler 
        self.SampleHandles = SampleKeyboardHandles(self)
        
        #creat a sample operation
        self.SampleOperation = SampleOperation(self)
        
        
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
        
        #set a new keyboard handler 
        self.OperationsController.KeyboardHandler.setNewKeyboardHandler(self.SampleHandles)
        self.OperationsController.setOperation("serial interrupt", self.SampleOperation)
        
    def exitRom(self):
        self.OperationsController.BrailleDisplay.disconnect()
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
        
    
class SampleKeyboardHandles(rs.RomKeyboardHandles):
    
    def __init__(self, Controller):
        super().__init__()
        
        self.Controller = Controller
        
    def KeyUpHandler(self):
        #turn romContinue on
        self.Controller.setInterruptFlag('romContinue', 1)
        
    def KeyDownHandler(self):
        #turn escape on
        self.Controller.setInterruptFlag('romHaltSerial', 1)
        
    def KeyAHandler(self):
        #turn escape on
        self.Controller.setInterruptFlag('romHaltSerial', 0)
        
class SampleOperation(rs.RomOperation):
    
    def __init__(self, Controller):
        super().__init__()
        self.Controller = Controller
        
    def execute(self):
        serialHaltInterrupt = self.Controller.getInterruptFlag('romHaltSerial')
        #idk interrupt communication somehow
        if serialHaltInterrupt:
            #stop the romvisualizer
            self.Controller.OperationsController.stopExecutingOperation("VisualizationRefreshOperation")
        else:
            #turn it back on
            self.Controller.OperationsController.startExecutingOperation("VisualizationRefreshOperation")
        

#settings specific to the rom
romSettings = { 'demoNumber': int(demoNumber) }

ThisRom = SampleController(interruptDictionaryAddress, OperationsControlAddress, romSettings, int(echo))


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

        
        