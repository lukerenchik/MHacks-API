# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 13:16:11 2022

@author: Derek Joslin
"""

import time
import NHAPI as nh
import keyboard
import random

def keyboardControl():
    global cursorPosition
    
    if keyboard.is_pressed("up"):
        if cursorPosition[1] > 0:
            cursorPosition[1] -= 1
        else:
            pass
        
    if keyboard.is_pressed("down"):
        if cursorPosition[1] < 19:
            cursorPosition[1] += 1
        else:
            pass
        
    if keyboard.is_pressed("left"):
        if cursorPosition[0] > 0:
            cursorPosition[0] -= 3
        else:
            pass
        
    if keyboard.is_pressed("right"):
        if cursorPosition[0] < 41:
            cursorPosition[0] += 3
        else:
            pass
        
def createPaddles():
    global cursorPosition
    
    engine.stroke(2)
    for paddleRow in range(0,difficulty,4):
        engine.line((18 - paddleRow,cursorPosition[0] - 4), (18 - paddleRow,cursorPosition[0] + 5))
    engine.stroke(1)
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
def avalanchePhysics(position, cursorPosition):
    global difficulty
    global difficultyIncrement
    global score
    global xIncrement
    global yIncrement
    global nColumns
    global nRows
    lineValues = [i for i in range(cursorPosition[0] - 4, cursorPosition[0] + 4)]
    yValues =  [18 - i for i in range(0,difficulty,4)]
    pongX = position[0]
    pongY = position[1]
    
    
    if pongX >= (nColumns):
        xIncrement = -1 
    
    if pongY >= (nRows):
        yIncrement = 0
    
    if pongX < 0:
        xIncrement = 1
        
    if pongY < 0:
        yIncrement = 1
        
    if (pongY in yValues) and (pongX in lineValues):
        multiplier = ((cursorPosition[0]/41)/2) + ((pongY/19)/2)
        if (multiplier > 0.4) and (multiplier < 0.6):
            if (multiplier < 0.5):
                multiplier += 0.45
            elif (multiplier >= 0.5):
                multiplier -= 0.45
        pongX = int(41 - 41*multiplier)
        pongY = 0
        """
        if difficulty == 3:
            if pongX > 20:
                xIncrement = -1
            else:
                xIncrement = 1
        """
        score = score + 1
        difficultyIncrement = difficultyIncrement + 1
        
    newX = pongX + xIncrement
    newY = pongY + yIncrement
    if newY%4 is 0:
        newY = newY + yIncrement

    if newX%3 is 0:
        newX = newX + xIncrement
    
    return [newX,newY]


engine = nh.NHAPI()
engine.connect("COM3",0)

displaySize = engine.return_displaySize()

nRows = displaySize[0]
nColumns = displaySize[1]


xIncrement = 0
yIncrement = 1
difficultyIncrement = 1
score = 0

#game settings
difficulty = 4
echo = 1


tic = 0
pongPosition = [0,0]
startPosition = [0,0]



cursorPosition = [1,1]
startPosition[0] = cursorPosition[0]
startPosition[1] = cursorPosition[1]

print("press arrow key to start")
engine.braille((0,0),"press arrow key to start")
engine.desired()
engine.refresh()
engine.state()
while startPosition == cursorPosition:
    keyboardControl()
    
tic = time.perf_counter()
avalancheTimer = 0
toc = time.perf_counter()
currentTime = toc - tic
while yIncrement is not 0:
        if difficultyIncrement%15 == 0:
            #increase difficulty and display score
            difficultyIncrement = 1
            if difficulty > 3:
                difficulty = difficulty - 1
                print("difficulty increased to {}".format(difficulty))
        
        if (currentTime) > (avalancheTimer):
            pongPosition = avalanchePhysics(pongPosition,cursorPosition)
            avalancheTimer += 0.25
        keyboardControl()
        engine.setCursorPosition(cursorPosition)
              
        engine.line((pongPosition[1] - 2,pongPosition[0]), (pongPosition[1] - 2,pongPosition[0] + 2))
        engine.line((pongPosition[1] - 1,pongPosition[0]), (pongPosition[1] - 1,pongPosition[0] + 2))
        engine.line((pongPosition[1],pongPosition[0]), (pongPosition[1],pongPosition[0] + 2))
        if echo:    
            print(pongPosition)

        createPaddles()
        
        engine.desired()
        engine.refresh()
        
        engine.state()
        
        if echo:
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            print("{0},{1}".format(cursorPosition[0],cursorPosition[1]))
            print(toc - tic)
        toc = time.perf_counter()
        currentTime = toc - tic
        engine.clear()
else:
    
    print("You Lose!")
    print("score is {}".format(score))
    engine.braille((0,0),"you lose score is {}".format(score))
    engine.desired()
    engine.refresh()
    engine.state()
    
    

engine.disconnect()





