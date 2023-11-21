# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 15:14:11 2022

@author: Derek Joslin
"""

import time
import NHAPI as nh
import keyboard

def keyboardControl():
    global cursorPosition
    global nRows
    global nColumns
    cursorX = cursorPosition[0]
    cursorY = cursorPosition[1]
    if keyboard.is_pressed("down"):
        if cursorY > 0:
            cursorPosition[1] -= 4
        else:
            pass
        
    if keyboard.is_pressed("up"):
        if cursorY <= (nRows - 4):
            cursorPosition[1] += 4
        else:
            pass
        
    if keyboard.is_pressed("left"):
        if cursorX > 0:
            cursorPosition[0] -= 3
        else:
            pass
        
    if keyboard.is_pressed("right"):
        if cursorX <= (nColumns - 3):
            cursorPosition[0] += 3
        else:
            pass
def createFrog():
    global cursorPosition
    
    engine.rect((16 - cursorPosition[1],cursorPosition[0]), (18 - cursorPosition[1],cursorPosition[0] + 1))

def froggerPhysics(position, cursorPosition):
    global difficulty
    global difficultyIncrement
    global score
    global xIncrement
    global yIncrement
    global nColumns
    global nRows
    global yOffsetLine
    cursorX = cursorPosition[0]
    cursorY = cursorPosition[1]
    
    
    pongX = position[0]
    pongY = position[1]
    
    
    if pongX <= 3:
        xIncrement = 3
    
    if pongY <= 0:
        yIncrement = 4
    
    if pongX >= (nColumns - 3):
        xIncrement = -3
        
    if pongY >= (nRows - 4):
        yIncrement = -4
    """
    if (pongY is cursorY) and (pongX is cursorX):
        print("not okay to cross1")
        score = score + 1
    elif(pongY - 8 is cursorY) and (pongX is cursorX):
        print("not okay to cross2")
        score = score + 1
    elif(pongY - 12 is cursorY) and (pongX is cursorX):
        print("not okay to cross3")
        score = score + 1
    elif(pongY + 8 is cursorY) and (pongX is cursorX):
        print("not okay to cross4")
        score = score + 1
    elif(pongY + 12 is cursorY) and (pongX is cursorX):
        print("not okay to cross4")
        score = score + 1
    """  
    """
    for yOffset in yOffsetLine:
        if ( (pongY + yOffset) is cursorY) and (pongX is cursorX):
            print("not okay to cross")
            score = score + 1
    """
    newX = pongX + xIncrement
    newY = pongY + yIncrement

    
    return [newX,newY]


engine = nh.NHAPI()
engine.connect("COM3",0)

displaySize = engine.return_displaySize()

nRows = displaySize[0]
nColumns = displaySize[1]


xIncrement = 1
yIncrement = 1
difficultyIncrement = 1
score = 0

yOffsetLine = [0,-8,-12,8,12]
xOffsetLine = [0,-3,-6,-15,-18,-21,-30,-33,-36,9,12,15,18,27,33,39]

#game settings
difficulty = 12
echo = 0


tic = 0
pongPosition = [0,0]
startPosition = [0,0]



cursorPosition = [0,0]
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
        if difficultyIncrement%6 == 0:
            #increase difficulty and display score
            difficultyIncrement = 1
            if difficulty > 3:
                difficulty = difficulty - 1
                print("difficulty increased to {}".format(difficulty))
        
        if (currentTime) > (avalancheTimer):
            pongPosition = froggerPhysics(pongPosition,cursorPosition)
            avalancheTimer += 2
        keyboardControl()
        engine.setCursorPosition(cursorPosition)
        
        for (iY,yOffset) in enumerate(yOffsetLine):
            for (iX,xOffset) in enumerate(xOffsetLine):
                if iX%2 == 0:
                    xPos = pongPosition[0] + xOffset + 3
                    yPos = pongPosition[1] + yOffset
                if iY%2 == 0:
                    xPos = pongPosition[0] + xOffset
                    yPos = pongPosition[1] + yOffset + 4
                else:
                    xPos = pongPosition[0] + xOffset
                    yPos = pongPosition[1] + yOffset
                if xPos >= 3 and xPos <= (nColumns - 3):
                    engine.rect((16 - yPos,xPos), (18 - yPos,xPos + 1))
                    if (yPos is cursorPosition[1]) and (xPos is cursorPosition[0]):
                        print("not okay to cross x{1}y{2}".format((xOffset,yOffset)))
                        score = score + 1
                
                
            """
            engine.rect((16 - pongPosition[1],pongPosition[0]), (18 - pongPosition[1],pongPosition[0] + 1))
            engine.rect((16 - pongPosition[1]-8,pongPosition[0]), (18 - pongPosition[1]-8,pongPosition[0] + 1))
            engine.rect((16 - pongPosition[1]-12,pongPosition[0]), (18 - pongPosition[1]-12,pongPosition[0] + 1))
            engine.rect((16 - pongPosition[1]+8,pongPosition[0]), (18 - pongPosition[1]+8,pongPosition[0] + 1))
            engine.rect((16 - pongPosition[1]+12,pongPosition[0]), (18 - pongPosition[1]+12,pongPosition[0] + 1))
            """
        if echo:    
            print(pongPosition)

        createFrog()
        
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





