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
import keyboard

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
        self.StartMenu = StartMenu(self)
        self.Game = Avalanche(self)
        self.ScoreMenu = ScoreMenu(self)
        
        #current state of rom
        self.stateKey = 'Avalanche Start Menu'
        
        #available states for the rom
        self.romStateDictionary = { 'Avalanche Start Menu' : self.StartMenu,
                                    'Avalanche Game' : self.Game,
                                    'Avalanche Score': self.ScoreMenu }
        
        self.engine = engine
        #self.Controller.engine.connect(engineComport,0)
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
        #romHalt = self.getInterruptFlag('romHaltSerial')
        if self.stateKey == 'Exit Rom':
            pass
        #elif romHalt:
        #    self.setInterruptFlag('isSerialHalted',1)
        else:
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
    
    def __init__(self, Controller):
        #do nothing to begin start menu
        self.Controller = Controller
    
    def stepState(self):
        #do nothing while running this state
        pass
    
    def startState(self):
        #display the start screen
        brailleString = "press space key to start"
        self.Controller.engine.clear()
        
        print(brailleString)
        self.Controller.engine.braille((0,0),brailleString)
        self.Controller.engine.desired()
        self.Controller.engine.refresh()
        self.Controller.engine.state()
        
        
    def closeState(self):
        #clear the screen of all information and shut down start screen processes
        self.Controller.engine.clear()
        self.Controller.engine.desired()
        self.Controller.engine.refresh()
        self.Controller.engine.state()
        

    def getNextState(self):
        #get values for the truth table
        romEscape = self.Controller.getInterruptFlagTrigger('romEscape')
        romContinue = self.Controller.getInterruptFlagTrigger('romContinue')
        romEnd = self.Controller.getInterruptFlag('romEnd')
        
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
    
    def __init__(self, Controller):
        #do nothing to begin start menu
        self.Controller = Controller
    
    def stepState(self):
        #do nothing while running this state
        #print("display Avalanche")
        
        self.gameDifficultyCalculation()
        
        self.gamePhysics()
        
        self.timingControls()
        
        self.gameControlsUpdate()
        
        self.gameGraphicsRender()
        
        self.createPaddles()
        
        self.timingCalculations()
        
        if self.Controller.getInterruptFlag('romHaltSerial'):
            self.Controller.setInterruptFlag('isSerialHalted',1)
        else:
            self.Controller.setInterruptFlag('isSerialHalted',0)
            self.peripheralCommunication()
        
        self.keyboardControl()
    
        
    def startState(self):
        print("Game Started")
        self.startNewGame()
        
    def closeState(self):
        #clear the screen of all information and shut down start screen processes
        self.Controller.engine.clear()
        self.Controller.engine.desired()
        self.Controller.engine.refresh()
        self.Controller.engine.state()
        

    def getNextState(self):
        #get values for the truth table
        romEscape = self.Controller.getInterruptFlagTrigger('romEscape')
        romContinue = self.Controller.getInterruptFlagTrigger('romContinue')
        romEnd = self.Controller.getInterruptFlag('romEnd')
        
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
        
    def startNewGame(self):
        """ initializing game settings """
        self.difficulty = 15 - self.Controller.difficultySetting
        
        """ establishing game mechanics """
        self.xIncrement = 0
        self.yIncrement = 1
        self.difficultyIncrement = 1
        self.score = 0
        
        """ initializing game physics """
        self.tic = 0
        self.pongPosition = [0,0]
        self.pong2Position = [0,0]
        self.startPosition = [0,0]
        
        """ initializing controls """
        self.cursorPosition = [1,1]
        self.startPosition[0] = self.cursorPosition[0]
        self.startPosition[1] = self.cursorPosition[1]

        """ initialize timers """        
        self.tic = time.perf_counter()
        self.avalancheTimer = 0
        self.keyboardTimer = 0
        self.toc = time.perf_counter()
        self.currentTime = self.toc - self.tic
        
    def peripheralCommunication(self):
        """ communicate with peripherals """
        
        self.Controller.engine.desired()
        self.Controller.engine.refresh()
        
        self.Controller.engine.state()
        self.Controller.engine.clear()
        
    def keyboardControl(self):
        
        if self.currentTime > self.keyboardTimer:
            if keyboard.is_pressed("up"):
                self.keyboardTimer = 0
                if self.cursorPosition[1] > 0:
                    self.cursorPosition[1] -= 1
                else:
                    pass
                
            if keyboard.is_pressed("down"):
                if self.pongPosition[1] < 17:
                    self.pongPosition[1] += 1
                else:
                    pass
                
            if keyboard.is_pressed("left"):
                self.keyboardTimer = self.currentTime + 0.1
                if self.cursorPosition[0] > 0:
                    self.cursorPosition[0] -= 3
                else:
                    pass
                
            if keyboard.is_pressed("right"):
                self.keyboardTimer = self.currentTime + 0.1
                if self.cursorPosition[0] < 41:
                    self.cursorPosition[0] += 3
                else:
                    pass
        
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
        if self.difficultyIncrement%self.Controller.difficultyRate == 0:
            #increase difficulty and display score
            self.difficultyIncrement = 1
            if self.difficulty > 1:
                self.difficulty = self.difficulty - 0.5
                print("difficulty increased to {}".format(self.difficulty))
    
    def gameControlsUpdate(self):
        """ game controls update """
        #self.keyboardControl()
        self.cursorPosition = (0,0)
        self.Controller.engine.setPinCursorPosition(self.cursorPosition)

    
    def gameGraphicsRender(self):
        """ game graphics render """
        self.Controller.engine.line((self.pongPosition[1] - 2,self.pongPosition[0]), (self.pongPosition[1] - 2,self.pongPosition[0] + 2))
        self.Controller.engine.line((self.pongPosition[1] - 1,self.pongPosition[0]), (self.pongPosition[1] - 1,self.pongPosition[0] + 2))
        self.Controller.engine.line((self.pongPosition[1],self.pongPosition[0]), (self.pongPosition[1],self.pongPosition[0] + 2))
        
        """
        if difficulty < 4:
            self.Controller.engine.line((self.pong2Position[1] - 2,self.pong2Position[0]), (self.pong2Position[1] - 2,self.pong2Position[0] + 2))
            self.Controller.engine.line((self.pong2Position[1] - 1,self.pong2Position[0]), (self.pong2Position[1] - 1,self.pong2Position[0] + 2))
            self.Controller.engine.line((self.pong2Position[1],self.pong2Position[0]), (self.pong2Position[1],self.pong2Position[0] + 2))
        """
        if self.Controller.debug:
            print(self.pongPosition)
            
            
    def timingCalculations(self):
        """ timing calculations """
        self.toc = time.perf_counter()
        self.currentTime = self.toc - self.tic
        if self.Controller.debug:
            print(self.currentTime)
            
    def timingControls(self):
        """ Timing Controls """
        if (self.currentTime) > (self.avalancheTimer):
            self.avalancheTimer += self.Controller.baseFallTime + self.difficulty*0.2
            
            
    def createPaddles(self):
        
        self.Controller.engine.stroke(2)
        for paddleRow in range(0,int(self.difficulty),4):
            self.Controller.engine.line((18 - paddleRow,self.cursorPosition[0] - 4), (18 - paddleRow,self.cursorPosition[0] + 5))
        self.Controller.engine.stroke(1)
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
        
        if pongX >= (self.Controller.nColumns):
            self.xIncrement = -1 
        
        if pongY >= (self.Controller.nRows):
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
    
    def __init__(self, Controller):
        #do nothing to begin start menu
        self.Controller = Controller
    
    def stepState(self):
        #do nothing while running this state
        #print("display Score Menu")
        pass

    def startState(self):
        #display the start screen
        self.Controller.engine.clear()
        print("score is {}".format(5))
        self.printScore(5)
        self.Controller.engine.desired()
        self.Controller.engine.refresh()
        self.Controller.engine.state()
        
    def closeState(self):
        #clear the screen of all information and shut down start screen processes
        print("Score Menu Close")
        self.Controller.engine.clear()
        self.Controller.engine.desired()
        self.Controller.engine.refresh()
        self.Controller.engine.state()

    def getNextState(self):
        #get values for the truth table
        romEscape = self.Controller.getInterruptFlagTrigger('romEscape')
        romContinue = self.Controller.getInterruptFlagTrigger('romContinue')
        romEnd = self.Controller.getInterruptFlag('romEnd')
        
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
        
    def printScore(self, score):
        x = -3
        y = 0
        for i in range(0, score):
            x += 3
            if x > 41:
                x = 0
                y += 4
                self.Controller.engine.rect((y,x),(y+2,x+1))


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

