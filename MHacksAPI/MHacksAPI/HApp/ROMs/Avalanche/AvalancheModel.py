# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 16:49:54 2023

@author: Derek Joslin

"""

import time
import random
import AvalancheOperations as ao

class AvalancheModel:
    
    def __init__(self, GameFlag, displaySize, debug):
        """ initializing rom resources """
        
        self.GameFlag = GameFlag

        self.nRows = displaySize[0]
        self.nColumns = displaySize[1]
        
        self.GameFlag.nColumns = self.nColumns
        self.GameFlag.nRows = self.nRows
        
        self.difficultySetting = self.GameFlag.difficulty
        self.startNewGame()
        
        # game settings
        self.echo = debug
        
    def mainGameLoop(self):
        
        self.gameDifficultyCalculation()
        
        self.gamePhysics()
        
        self.timingControls()
        
        self.timingCalculations()


    def gameDifficultyCalculation(self):
        """ game difficulty calculation """
        
        if self.GameFlag.difficultyIncrement%5 == 0:
            #increase difficulty and display score
            self.GameFlag.difficultyIncrement = 1
            if self.GameFlag.difficulty > 1:
                self.GameFlag.difficulty = self.GameFlag.difficulty - 0.5
                print("difficulty increased to {}".format(self.GameFlag.difficulty))

    def gamePhysics(self):
        """ game physics """
        pongPosition = self.GameFlag.pongPosition
        cursorPosition = self.GameFlag.cursorPosition
        if (self.currentTime) > (self.avalancheTimer):
            pongPosition = self.avalanchePhysics(pongPosition, cursorPosition)
            self.GameFlag.setPongPosition(pongPosition)
            
        
        """
        if difficulty < 4 and (currentTime) > (avalancheTimer + 0.2):
            pong2Position = avalanchePhysics(pong2Position, cursorPosition)
        """
    

    def timingCalculations(self):
        """ timing calculations """
        self.endTime = time.perf_counter()
        self.currentTime = self.endTime - self.startTime
        if self.echo:
            print(self.currentTime)
            
    def debugInfo(self):
        """ debug info """
        if self.echo:
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            print("{0},{1}".format(self.GameFlag.cursorPosition[0],self.GameFlag.cursorPosition[1]))
            print(self.endTime - self.startTime)

    def timingControls(self):
        """ Timing Controls """
        if (self.currentTime) > (self.avalancheTimer):
            self.avalancheTimer += 0.2 + self.GameFlag.difficulty*0.2

    def startNewGame(self):
        """ reset game conditions """
        self.GameFlag.resetGame()
        
        """ initialize timers """
        self.startTime = time.perf_counter()
        self.avalancheTimer = 0
        self.endTime = time.perf_counter()
        self.currentTime = self.endTime - self.startTime
        
    """ user input movement actions """
        
    def moveUp(self):
        pongPosition = self.GameFlag.pongPosition
        if pongPosition[1] > 0:
            pongPosition[1] -= 1
            self.GameFlag.setPongPosition(pongPosition)
        else:
            pass
        
    def moveDown(self):
        pongPosition = self.GameFlag.pongPosition
        cursorPosition = self.GameFlag.cursorPosition
        if pongPosition[1] < 17:
            pongPosition[1] = 17
            self.GameFlag.setPongPosition(pongPosition)
            pongPosition = self.avalanchePhysics(pongPosition, cursorPosition)
            self.GameFlag.setPongPosition(pongPosition)
        else:
            pass        
        
    def moveRight(self):
        cursorPosition = self.GameFlag.cursorPosition
        if cursorPosition[0] < (self.nColumns - 3):
            cursorPosition[0] += 3
            self.GameFlag.setCursorPosition(cursorPosition)
        else:
            pass
            
    def moveLeft(self):
        cursorPosition = self.GameFlag.cursorPosition
        if cursorPosition[0] > 0:
            cursorPosition[0] -= 3
            self.GameFlag.setCursorPosition(cursorPosition)
        else:
            pass
        
    """ Game Calculations """
        
    def createPaddles(self):
        
        #self.TactileDisplay.stroke(2)
        for paddleRow in range(0,int(self.GameFlag.difficulty),4):
            pass
            #self.TactileDisplay.line((18 - paddleRow,self.GameFlag.cursorPosition[0] - 4), (18 - paddleRow,self.GameFlag.cursorPosition[0] + 5))
        #self.TactileDisplay.stroke(1)
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
        lineValues = [i for i in range(self.GameFlag.cursorPosition[0] - 2, self.GameFlag.cursorPosition[0] + 7)]
        yValues =  [17 - i for i in range(0,int(self.GameFlag.difficulty),4)]
        pongX = position[0]
        pongY = position[1]
        
        if pongX >= (self.nColumns):
            self.GameFlag.xIncrement = -1 
        
        if pongY >= (self.nRows):
            self.GameFlag.yIncrement = 0
        
        if pongX < 0:
            self.GameFlag.xIncrement = 1
            
        if pongY < 0:
            self.GameFlag.yIncrement = 1
            
        if (pongY in yValues) and (pongX in lineValues):
            pongX = random.randint(0,int(self.nColumns/3))*3
            pongY = 0
            """
            if difficulty == 3:
                if pongX > 20:
                    xIncrement = -1
                else:
                    xIncrement = 1
            """
            self.GameFlag.score = self.GameFlag.score + 1
            self.GameFlag.difficultyIncrement = self.GameFlag.difficultyIncrement + 1
            
        if pongY == 18:
            self.GameFlag.setGameState("Score Menu")
            
        newX = pongX + self.GameFlag.xIncrement
        newY = pongY + self.GameFlag.yIncrement
        if newY%4 is 0:
            newY = newY + self.GameFlag.yIncrement
        if newX%3 is 0:
            newX = newX + self.GameFlag.xIncrement
        
        return [newX,newY]