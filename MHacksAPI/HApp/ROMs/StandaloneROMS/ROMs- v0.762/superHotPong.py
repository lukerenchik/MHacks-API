# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 14:53:47 2022

@author: Derek Joslin
"""

import NHAPI as nh
import time

engine = nh.NHAPI()

engine.connect("COM3",0)
engine.connectTouchScreen("COM7")

displaySize = engine.return_displaySize()

nRows = displaySize[0]
nColumns = displaySize[1]

xIncrement = 1
yIncrement = 1
score = 0
difficulty = 5

tic = 0
pongPosition = [1,1]
startPosition = [0,0]

def pongPhysics(position, cursorPosition):
    global difficulty
    global score
    lineValues = [i for i in range(cursorPosition[0] - difficulty, cursorPosition[0] + difficulty)]
    pongX = position[0]
    pongY = position[1]
    global xIncrement
    global yIncrement
    
    if pongX > (nColumns - 2):
        xIncrement = -1
    
    if pongY > (nRows - 1):
        yIncrement = -100
    
    if pongX < 1:
        xIncrement = 1
        
    if pongY < 1:
        yIncrement = 1
        
    if (pongY is 17) and (pongX in lineValues):
        yIncrement = -1
        score = score + 1
        
        
    newX = pongX + xIncrement
    newY = pongY + yIncrement
    
    return [newX,newY]

cursorPosition = engine.getCursorPosition()
startPosition[0] = cursorPosition[0]
startPosition[1] = cursorPosition[1]

print("touch screen to start")
while startPosition == cursorPosition:
    cursorPosition = engine.getCursorPosition()
    
for j in range(0,3):
    for i in range(0,25):
        print("SUPA")
    engine.braille((9,20),"supa")
    engine.desired()
    engine.refresh()
    engine.state()
    time.sleep(0.5)
    for i in range(0,25):
        print("HOT")
    engine.braille((9,20),"hot")
    engine.desired()
    engine.refresh()
    engine.state()
    time.sleep(0.5)
    
while 1:
    try:
        cursorPosition = engine.getCursorPosition()
        if startPosition != cursorPosition:
            engine.setCursorPosition(cursorPosition)
            
            
            #if X > 13:
            #    X = 13
                
            #if Y > 14:
            #   Y = 14
            
            #Y = abs(19-Y)
            #X = abs(41-X)
            
            pongPosition = pongPhysics(pongPosition,cursorPosition)
            engine.dot((pongPosition[1],pongPosition[0]))
            print(pongPosition)
            engine.line((18,cursorPosition[0] - difficulty), (18,cursorPosition[0] + difficulty))
            
            
            engine.desired()
            engine.refresh()
            
            engine.state()
            
            toc = time.perf_counter()
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            print("{0},{1}".format(cursorPosition[0],cursorPosition[1]))
            print(toc-tic)
            tic = time.perf_counter()
            engine.clear()
            
        startPosition[0] = cursorPosition[0]
        startPosition[1] = cursorPosition[1]
    except:
        print("You Lose!")
        print("score is {}".format(score))
        break
engine.disconnect()



