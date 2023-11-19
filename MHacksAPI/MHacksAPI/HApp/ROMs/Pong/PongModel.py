# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 15:01:58 2023

@author: Derek Joslin

"""

import time
import random
import PongOperations as ao

class PongModel:
    
    def __init__(self, GameFlag, debug):
        """ initializing rom resources """
        
        self.GameFlag = GameFlag

        self.nRows = 19#displaySize[0]
        self.nColumns = 41#displaySize[1]
        
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
        if (self.currentTime) > (self.PongTimer):
            pongPosition = self.pongPhysics(pongPosition, cursorPosition)
            self.GameFlag.setPongPosition(pongPosition)
            
        
        """
        if difficulty < 4 and (currentTime) > (PongTimer + 0.2):
            pong2Position = pongPhysics(pong2Position, cursorPosition)
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
        if (self.currentTime) > (self.PongTimer):
            self.PongTimer += 0.2 + self.GameFlag.difficulty*0.2

    def startNewGame(self):
        """ reset game conditions """
        self.GameFlag.resetGame()
        
        """ initialize timers """
        self.startTime = time.perf_counter()
        self.PongTimer = 0
        self.endTime = time.perf_counter()
        self.currentTime = self.endTime - self.startTime
        
    """ user input movement actions """
        
    def moveUp(self):
        cursorPosition = self.GameFlag.cursorPosition
        if cursorPosition[1] > 0:
            cursorPosition[1] -= 0
            self.GameFlag.setCursorPosition(cursorPosition)
        else:
            pass
        
    def moveDown(self):
        pongPosition = self.GameFlag.pongPosition
        cursorPosition = self.GameFlag.cursorPosition
        pongPosition = self.pongPhysics(pongPosition, cursorPosition)
        self.GameFlag.setPongPosition(pongPosition)
# =============================================================================
#         cursorPosition = self.GameFlag.cursorPosition
#         if cursorPosition[1] < 19:
#             cursorPosition[1] += 0
#             self.GameFlag.setCursorPosition(cursorPosition)
#         else:
#             pass        
# =============================================================================
        
    def moveRight(self):
        cursorPosition = self.GameFlag.cursorPosition
        if cursorPosition[0] < 37:
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
        
    def pongPhysics(self, position, cursorPosition):
        lineValues = [i for i in range(self.GameFlag.cursorPosition[0] - 2, self.GameFlag.cursorPosition[0] + 7)]
        yValues =  [17 - i for i in range(0,int(self.GameFlag.difficulty),4)]
        pongX = position[0]
        pongY = position[1]
        
        if pongX >= (self.nColumns - 1):
            self.GameFlag.xIncrement = -1
        
        if pongY >= (self.nRows - 3):
            self.GameFlag.yIncrement = 0
        
        if pongX < 1:
            self.GameFlag.xIncrement = 1
            
        if pongY < 1:
            self.GameFlag.yIncrement = 1
            
        if (pongY is 17) and (pongX in lineValues):
            self.GameFlag.yIncrement = -1
            self.GameFlag.score = self.GameFlag.score + 1
            self.GameFlag.difficultyIncrement = self.GameFlag.difficultyIncrement + 1
        elif pongY > 16:
            self.GameFlag.setGameState("Score Menu")
            
            
        newX = pongX + self.GameFlag.xIncrement
        newY = pongY + self.GameFlag.yIncrement
        
        if newY%4 is 0:
            newY = newY + self.GameFlag.yIncrement
        if newX%3 is 0:
            newX = newX + self.GameFlag.xIncrement
            
        return [newX,newY]
    
    
    