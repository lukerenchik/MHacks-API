# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 16:11:07 2022

@author: Derek Joslin
"""

"""
@RomInputsBegin
#a dictionary to store the rom interrupts WARNING: will not compile as is a dictionary needs to be allocated to memory first
interruptDictionaryAddress = id({'romEscape': 0, 'romContinue': 0, 'romEnd': 0, 'romHaltSerial': 0, 'isSerialHalted': 0})
#comport for the arduino tactile display
BrailleDisplayAddress = id(engine)
#controls how fast avalanches fall 11-14
difficulty = 11
#how many avalanches per difficulty increase
difficultyRate = 5
#controls how fast the avalanche falls at highest difficulty
baseFallTime = 0.2
#classic debug toggle 1-on 0-off
echo = 0
@RomInputsEnd
"""


import time
import NHAPI as nh
import random
import ctypes
#import keyboard

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
    
    def __init__(self, interruptDictionaryAddress, engine, romSettings, debug):
        
        #intialize the control interrupt super class
        super().__init__(interruptDictionaryAddress)
        
        #define the state objects
        self.StartMenu = StartMenu()
        self.Game = Avalanche()
        self.ScoreMenu = ScoreMenu()
        
        #current state of rom
        self.stateKey = 'Avalanche Start Menu'
        
        #available states for the rom
        self.romStateDictionary = { 'Avalanche Start Menu' : self.StartMenu,
                                    'Avalanche Game' : self.Game,
                                    'Avalanche Score': self.ScoreMenu }
        
        self.engine = engine
        #self.engine.connect(engineComport,0)
        displaySize = self.engine.return_displaySize()
        self.nRows = displaySize[0]
        self.nColumns = displaySize[1]

        #debug
        self.debug = debug

        #game settings
        self.baseFallTime = romSettings['baseFallTime']
        self.difficultyRate = romSettings['difficultyRate']
        self.difficultySetting = romSettings['difficultySetting']
        
        
    def stepCurrentState(self):
        if self.stateKey == 'Exit Rom':
            pass
        else:
            #get the current rom that is running and run its step function
            currentState = self.getCurrentState()
            
            currentState.stepState()
        
        
    def decideNextState(self):

        #get the rom's current state
        currentState = self.getCurrentState()
        oldStateKey = self.stateKey
        
        #calculate which state to go to next from current state
        newStateKey = currentState.getNextState(self)
    
        #if new State Key is rom exit exit rom immediately
        if newStateKey == 'Exit Rom':
            self.stateKey = newStateKey
            pass
        #switch to the next rom state or if the same state do nothing
        elif oldStateKey == newStateKey:
            pass
        
        else:
            #close all operations of the current state
            currentState.closeState()
            
            #initialize all of the operations of the next state
            nextState = self.romStateDictionary[newStateKey]
            nextState.startState()
            
            #switch to the next state
            self.switchState(newStateKey)
        
        
    def getCurrentState(self):
        return self.romStateDictionary[self.stateKey]


    def switchState(self, stateKey):
        self.stateKey = stateKey
        
        
    def runCommonFunctions(self):
        pass
    
    def exitRom(self):
        self.engine.disconnect()
        print("disconnected")
    
class StartMenu():
    
    def __init__(self):
        #do nothing to begin start menu
        pass
    
    def stepState(self):
        #do nothing while running this state
        print("display start Menu")

    def startState(self):
        #display the start screen
        print("Start Menu Begin")
# =============================================================================
#         brailleString = "press space key to start"
#         self.engine.clear()
#         
#         print(brailleString)
#         self.engine.braille((0,0),brailleString)
#         self.engine.desired()
#         self.engine.refresh()
#         self.engine.state()
# =============================================================================
        
        
    def closeState(self):
        #clear the screen of all information and shut down start screen processes
        print("Start Menu Close")

# =============================================================================
#         self.engine.clear()
#         self.engine.desired()
#         self.engine.refresh()
#         self.engine.state()
# =============================================================================
        

    def getNextState(self, Controller):
        #get values for the truth table
        romEscape = Controller.getInterruptFlagTrigger('romEscape')
        romContinue = Controller.getInterruptFlagTrigger('romContinue')
        romEnd = Controller.getInterruptFlag('romEnd')
        
        #truth table for start Menu
        if romEnd:
            #exit the current state and rom entirely 
            
            return 'Exit Rom'
            
        elif romEscape:
            #restart the start menu
            self.startState()
            
            
            return 'Avalanche Start Menu'
            
        elif romContinue:
            #move to the next state
            
            return 'Avalanche Game'
        
        else:
            #continue with program execution
        
            return 'Avalanche Start Menu'
      
        
class Avalanche():
    
    def __init__(self):
        #do nothing to begin start menu
        pass
    
    def stepState(self):
        #do nothing while running this state
        print("display Avalanche")


    def startState(self):
        print("Game Started")
        
        
    def closeState(self):
        #clear the screen of all information and shut down start screen processes
        print("Game Closed")
        

    def getNextState(self, Controller):
        #get values for the truth table
        romEscape = Controller.getInterruptFlagTrigger('romEscape')
        romContinue = Controller.getInterruptFlagTrigger('romContinue')
        romEnd = Controller.getInterruptFlag('romEnd')
        
        #truth table for start Menu
        if romEnd:
            #exit the current state and rom entirely 
            
            return 'Exit Rom'
            
        elif romEscape:
            #return to the start menu
            #self.closeState()
            
            return 'Avalanche Start Menu'
            
        elif romContinue:
            #move to the next state
            
            return 'Avalanche Score'
        
        else:
            #continue with program execution
        
            return 'Avalanche Game'
        
        
    def gamePhysics(self):
        """ game physics """
        if (self.currentTime) > (self.avalancheTimer):
            self.pongPosition = self.avalanchePhysics(self.pongPosition,self.cursorPosition)
            """
            if difficulty < 4 and (currentTime) > (avalancheTimer + 0.2):
                pong2Position = avalanchePhysics(pong2Position, cursorPosition)
            """
    
    def gameDifficultyCalculation(self):
        """ game difficulty calculation """
        if self.difficultyIncrement%self.difficultyRate == 0:
            #increase difficulty and display score
            self.difficultyIncrement = 1
            if self.difficulty > 1:
                self.difficulty = self.difficulty - 0.5
                print("difficulty increased to {}".format(self.difficulty))
    
    def gameControlsUpdate(self):
        """ game controls update """
        self.keyboardControl()
        self.engine.setPinCursorPosition(self.cursorPosition)

    
    def gameGraphicsRender(self):
        """ game graphics render """
        self.engine.line((self.pongPosition[1] - 2,self.pongPosition[0]), (self.pongPosition[1] - 2,self.pongPosition[0] + 2))
        self.engine.line((self.pongPosition[1] - 1,self.pongPosition[0]), (self.pongPosition[1] - 1,self.pongPosition[0] + 2))
        self.engine.line((self.pongPosition[1],self.pongPosition[0]), (self.pongPosition[1],self.pongPosition[0] + 2))
        
        """
        if difficulty < 4:
            self.engine.line((self.pong2Position[1] - 2,self.pong2Position[0]), (self.pong2Position[1] - 2,self.pong2Position[0] + 2))
            self.engine.line((self.pong2Position[1] - 1,self.pong2Position[0]), (self.pong2Position[1] - 1,self.pong2Position[0] + 2))
            self.engine.line((self.pong2Position[1],self.pong2Position[0]), (self.pong2Position[1],self.pong2Position[0] + 2))
        """
        if self.echo:    
            print(self.pongPosition)
            
            
    def timingCalculations(self):
        """ timing calculations """
        self.toc = time.perf_counter()
        self.currentTime = self.toc - self.tic
        if self.echo:
            print(self.currentTime)
            
    def timingControls(self):
        """ Timing Controls """
        if (self.currentTime) > (self.avalancheTimer):
            self.avalancheTimer += self.baseFallTime + self.difficulty*0.2
            
            
    def createPaddles(self):
        
        self.engine.stroke(2)
        for paddleRow in range(0,int(self.difficulty),4):
            self.engine.line((18 - paddleRow,self.cursorPosition[0] - 4), (18 - paddleRow,self.cursorPosition[0] + 5))
        self.engine.stroke(1)
        """
        try:
            if cursorPosition[0] > 4:
                engine.line((16,cursorPosition[0]-3),(16,cursorPosition[0]-4))
            if cursorPosition[1] < 41:
                engine.line((16,cursorPosition[0]+3),(16,cursorPosition[0]+4))
        except:
            if echo:
                print("out of bounds")
                
        """
    def avalanchePhysics(self, position, cursorPosition):
        lineValues = [i for i in range(self.cursorPosition[0] - 4, self.cursorPosition[0] + 4)]
        yValues =  [17 - i for i in range(0,int(self.difficulty),4)]
        pongX = position[0]
        pongY = position[1]
        
        if pongX >= (self.nColumns):
            self.xIncrement = -1 
        
        if pongY >= (self.nRows):
            self.yIncrement = 0
        
        if pongX < 0:
            self.xIncrement = 1
            
        if pongY < 0:
            self.yIncrement = 1
            
        if (pongY in yValues) and (pongX in lineValues):
            pongX = random.randint(0,13)*3
            pongY = 0
            """
            if difficulty == 3:
                if pongX > 20:
                    xIncrement = -1
                else:
                    xIncrement = 1
            """
            self.score = self.score + 1
            self.difficultyIncrement = self.difficultyIncrement + 1
            
        newX = pongX + self.xIncrement
        newY = pongY + self.yIncrement
        
        if newY%4 is 0:
            newY = newY + self.yIncrement
    
        if newX%3 is 0:
            newX = newX + self.xIncrement
        
        return [newX,newY]
        
        
        
class ScoreMenu():
    
    def __init__(self):
        #do nothing to begin start menu
        pass
    
    def stepState(self):
        #do nothing while running this state
        print("display Score Menu")

    def startState(self):
        #display the start screen
        print("Score Menu Start")
        
        
    def closeState(self):
        #clear the screen of all information and shut down start screen processes
        print("Score Menu Close")
        

    def getNextState(self, Controller):
        #get values for the truth table
        romEscape = Controller.getInterruptFlagTrigger('romEscape')
        romContinue = Controller.getInterruptFlagTrigger('romContinue')
        romEnd = Controller.getInterruptFlag('romEnd')
        
        #truth table for start Menu
        if romEnd:
            #exit the current state and rom entirely 
            
            return 'Exit Rom'
            
        elif romEscape:
            #restart the start menu
            
            
            return 'Avalanche Start Menu'
            
        elif romContinue:
            #move to the next state
            
            return 'Avalanche Start Menu'
        
        else:
            #continue with program execution
        
            return 'Avalanche Score'
        

#The haptics engine object
BrailleDisplay = ctypes.cast(BrailleDisplayAddress, ctypes.py_object).value

#settings specific to the rom
romSettings = { 'baseFallTime': float(baseFallTime),
                'difficultyRate': int(difficultyRate),
                'difficultySetting': float(difficulty) }

ThisRom = RomController(interruptDictionaryAddress, BrailleDisplay, romSettings, int(echo))


shouldRomEnd = ThisRom.getInterruptFlag('romEnd')

#Main loop of the Rom
while shouldRomEnd is 0:
    
    #always step one tick into the current state
    ThisRom.stepCurrentState()
    
# =============================================================================
#     shouldRomEnd = ThisRom.getInterruptFlag('romEnd')
#     if shouldRomEnd:
#         break
#     
# =============================================================================
    #decide if peripheral communication is going to occur
    #Put NHAPI functions in here
    ThisRom.runCommonFunctions()
    
# =============================================================================
#     shouldRomEnd = ThisRom.getInterruptFlag('romEnd')
#     if shouldRomEnd:
#         break
# =============================================================================
    
    #decide the next state to move into
    ThisRom.decideNextState()
    shouldRomEnd = ThisRom.getInterruptFlag('romEnd')
else:
    ThisRom.exitRom()

