# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 14:34:43 2022

@author: Derek Joslin
"""

import time
import NHAPI as nh
import keyboard

def pongPhysics(position, cursorPosition):
    global difficulty
    global difficultyIncrement
    global score
    global xIncrement
    global yIncrement
    global nColumns
    global nRows
    lineValues = [i for i in range(position[0] - difficulty, position[0] + difficulty)]
    pongX = position[0]
    pongY = position[1]
    
    
    if pongX >= (nColumns - 1):
        xIncrement = -1
    
    if pongY >= (nRows - 3):
        yIncrement = 0
    
    if pongX < 1:
        xIncrement = 1
        
    if pongY < 1:
        yIncrement = 1
        
    if (pongY is 15) and (pongX in lineValues):
        yIncrement = -1
        score = score + 1
        difficultyIncrement = difficultyIncrement + 1
        
    newX = pongX + xIncrement
    newY = pongY + yIncrement
   # if newY%4 is 0:
   #     newY = newY + yIncrement

   # if newX%3 is 0:
   #     newX = newX + xIncrement
   
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

#game settings
difficulty = 8
echo = 1


tic = 0
pongPosition = [1,1]
startPosition = [0,0]
cursorPosition = [0,0]


startPosition[0] = cursorPosition[0]
startPosition[1] = cursorPosition[1]

print("touch screen to start")
engine.braille((0,0),"touch screen to start")
engine.desired()
engine.refresh()
engine.state()
engine.Fclear()
    
    
cursorPosition = pongPosition
while not keyboard.is_pressed('o'):
        time.sleep(0.3)
        if difficultyIncrement%6 == 0:
            #increase difficulty and display score
            difficultyIncrement = 1
            if difficulty > 3:
                difficulty = difficulty - 1
                print("difficulty increased to {}".format(difficulty))
        
        pongPosition = pongPhysics(pongPosition,cursorPosition)
        engine.setCursorPosition(pongPosition)
              
        engine.fill("on")
        engine.circle((pongPosition[1],pongPosition[0]),2)
        engine.fill("off")
        if echo:    
            print(pongPosition)

        engine.stroke(3)
        engine.line((17,pongPosition[0] - difficulty), (17,pongPosition[0] + difficulty))
        engine.stroke(1)
        
        engine.desired()
        engine.refresh()
        
        engine.state()
        
        toc = time.perf_counter()
        if echo:
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            print("{0},{1}".format(cursorPosition[0],cursorPosition[1]))
            print(toc-tic)
        tic = time.perf_counter()
        engine.clear()
else:
    
    print("You Lose!")
    print("score is {}".format(score))
    engine.braille((0,0),"you lose score is {}".format(score))
    engine.desired()
    engine.refresh()
    engine.state()
    
    

engine.disconnect()







