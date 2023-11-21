# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 12:57:16 2022

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
echo = 0

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
    


while 1:
    try:
        engine.setCursorPosition(cursorPosition)
        
        
        #if X > 13:
        #    X = 13
            
        #if Y > 14:
        #   Y = 14
        
        #Y = abs(19-Y)
        #X = abs(41-X)
        cursorPosition = engine.getCursorPosition()
        pongPosition = pongPhysics(pongPosition,cursorPosition)
        engine.dot((pongPosition[1],pongPosition[0]))
        if echo:    
            print(pongPosition)

        engine.line((18,cursorPosition[0] - difficulty), (18,cursorPosition[0] + difficulty))
        
        
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
    except:
        print("You Lose!")
        print("score is {}".format(score))
        break
engine.disconnect()



