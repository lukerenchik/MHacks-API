# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 12:21:47 2022

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



class RomControlBus():

    def __init__(self, interruptDictionaryAddress):
        self.interruptDictionary = ctypes.cast(interruptDictionaryAddress, ctypes.py_object).value
        print(id(self.interruptDictionary))

    def getInterruptFlag(self, interruptString):
        interruptValue = self.interruptDictionary[interruptString]
        return interruptValue
    
    def setInterruptFlag(self, interruptString, interruptValue):
        self.interruptDictionary[interruptString] = interruptValue


class romTemplate:
    
    def __init__(self, api, difficultySetting, debug, difficultyRate, baseFallTime, RomController):
        """ initializing rom resources """
        
        self.RomController = RomController
        self.engine = api
        #self.engine.connect(engineComport,0)
        displaySize = self.engine.return_displaySize()
        self.nRows = displaySize[0]
        self.nColumns = displaySize[1]
        
        #game settings
        self.baseFallTime = baseFallTime
        self.difficultyRate = difficultyRate
        self.difficultySetting = difficultySetting
        self.echo = debug


    def displayBraille(self, position, brailleString):
        self.engine.braille(position,brailleString)
        self.engine.desired()
        self.engine.refresh()
        self.engine.state()

        
    def startMenu(self):
        self.engine.clear()
        print("press space key to start")
        self.displayBraille((0,0), "press space key to start")
        
        while not  or :
            #grab appropriate interrupts
            
            self.RomController.getInterruptFlag('romEscape')
            self.RomController.getInterruptFlag('romContinue')
            pass
        else:
            self.startNewGame()
        
    def mainGameLoop(self):
        
        print("Game Started")

        while not (self.RomController.getInterruptFlag('romEscape') or (self.yIncrement is 0) or self.RomController.getInterruptFlag('romEnd')):
            #print("pauseRom: {}".format(romController.getPauseRom()))
            #print("endRom: {}".format(romController.getEndRom()))
            if not self.RomController.getInterruptFlag('romHaltSerial'):
                if self.RomController.getInterruptFlag('isSerialHalted') is 1:
                    #unhalt rom
                    self.RomController.setInterruptFlag('isSerialHalted',0)
                    print("rom not halted")
                    
                self.gameDifficultyCalculation()
            
                self.gamePhysics()
            
                self.timingControls()
            
                self.gameControlsUpdate()
            
                self.gameGraphicsRender()
           
                self.createPaddles()
            
                self.peripheralCommunication()
            
                self.timingCalculations()
            
                self.debugInfo()
                
            if (self.RomController.getInterruptFlag('romHaltSerial') is 1) and (not self.RomController.getInterruptFlag('isSerialHalted')):
                #set rom to halted state
                self.RomController.setInterruptFlag('isSerialHalted',1)
                print("rom halted")

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
       
    
    def peripheralCommunication(self):
        """ communicate with peripherals """
        
        self.engine.desired()
        self.engine.refresh()
        
        self.engine.state()
        self.engine.clear()
        
        
    def timingCalculations(self):
        """ timing calculations """
        self.toc = time.perf_counter()
        self.currentTime = self.toc - self.tic
        if self.echo:
            print(self.currentTime)
            
   
    def debugInfo(self):
        """ debug info """
        if self.echo:
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            print("{0},{1}".format(self.cursorPosition[0],self.cursorPosition[1]))
            print(self.toc - self.tic)


    def timingControls(self):
        """ Timing Controls """
        if (self.currentTime) > (self.avalancheTimer):
            self.avalancheTimer += self.baseFallTime + self.difficulty*0.2
            
        

    
    def exitScreen(self):
        """ exit screen  """
        print("You Lose!")
        print("score is {}".format(self.score))
        self.engine.braille((0,0),"you lose score is {}".format(self.score))
        self.engine.desired()
        self.engine.refresh()
        self.engine.state()
        
    def scoreScreen(self):
        """ displays score """
        self.engine.clear()
        print("score is {}".format(self.score))
        x = -3
        y = 0
        for i in range(0,self.score):
            x += 3
            if x > 41:
                x = 0
                y += 4
            self.engine.rect((y,x),(y+2,x+1))
        self.engine.desired()
        self.engine.refresh()
        self.engine.state()
        while not (self.RomController.getInterruptFlag('romContinue') or self.RomController.getInterruptFlag('romEscape')):
            pass
        time.sleep(0.2)
                
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
        
    def exitRom(self):
       self.engine.disconnect()
        
        
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


#values to share externally
BrailleDisplay = ctypes.cast(BrailleDisplayAddress, ctypes.py_object).value
RomController = RomControlBus(interruptDictionaryAddress)

#create the rom object with inputs
#comport for the arduino tactile display
#controls how fast avalanches fall 5-1
#classic debug toggle 1-on 0-off

rom = romTemplate(BrailleDisplay, float(difficulty), int(echo), int(difficultyRate), float(baseFallTime), RomController)

#rom.engine.com.port.write(bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]))

shouldRomEnd = 0

#Main loop of the Rom

while shouldRomEnd is 0:
    
    #these are submenus
    
    
    rom.startMenu()
    
    #between menu check if the rom should end
    shouldRomEnd = RomController.getInterruptFlag('romEnd')
    if shouldRomEnd is 1:
        #quit the rom
        break
        
    rom.mainGameLoop()
    
    shouldRomEnd = RomController.getInterruptFlag('romEnd')
    if shouldRomEnd is 1:
        #quit the rom
        break
    
    rom.scoreScreen()
    
    #check to see if the rom should end at the exit screen
    shouldRomEnd = RomController.getInterruptFlag('romEnd')
    
else:
    rom.exitScreen()
    rom.exitRom()