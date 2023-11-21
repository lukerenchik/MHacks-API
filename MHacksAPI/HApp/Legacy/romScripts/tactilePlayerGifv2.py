# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 14:53:31 2022

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
    lineValues = [i for i in range(pongPosition[0] - difficulty, pongPosition[0] + difficulty)]
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


def touchToBegin():
    global engine
    global startPosition
    global cursorPosition
    cursorPosition = engine.getCursorPosition()
    startPosition[0] = cursorPosition[0]
    startPosition[1] = cursorPosition[1]
    print("touch screen to start")
    engine.braille((16,0),"touch screen to start")
    engine.desired()
    engine.refresh()
    engine.state()
    while startPosition == cursorPosition:
        cursorPosition = engine.getCursorPosition()
        
    engine.clear()

def startScreen():
    global engine
    engine.braille((0,0),"move your finger on the touch screen to change bar size")
    engine.desired()
    engine.refresh()
    engine.state()
    
def createBars():
    global engine
    global bar1
    global bar2
    global bar3
    global pongPosition
    engine.stroke(3)
    
    if pongPosition[1] < 7:
        bar1 = pongPosition[0]
    elif pongPosition[1] < 14:
        bar2 = pongPosition[0]
    else:
        bar3 = pongPosition[0]
    engine.clear()    
    engine.line((1,0), (1,bar1))
    engine.line((10,0), (10,bar2))
    engine.line((17,0), (17,bar3))

engine = nh.NHAPI()
engine.connect("COM9",0)
engine.connectTouchScreen("COM7")

displaySize = engine.return_displaySize()


nRows = displaySize[0]
nColumns = displaySize[1]


bar1 = 0
bar2 = 0
bar3 = 0

xIncrement = 1
yIncrement = 1
score = 0

#game settings
echo = 0

tic = 0
startPosition = [0,0]
pongPosition = [1,1]

startScreen()

touchToBegin()



while not keyboard.is_pressed('o'):
        
        pongPosition = pongPhysics(pongPosition,cursorPosition)
        createBars()
        
        engine.desired()
        engine.refresh()
        
        engine.state()
        
        if keyboard.is_pressed('a'):  # if key 'q' is pressed 
            engine.clear()
        
        toc = time.perf_counter()
        if echo:
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            print("{0},{1}".format(cursorPosition[0],cursorPosition[1]))
            print(toc-tic)
        tic = time.perf_counter()
            
            
        startPosition[0] = cursorPosition[0]
        startPosition[1] = cursorPosition[1]
else:
    print("Exited Program")
    engine.braille((0,0),"exited program")
    engine.desired()
    engine.refresh()
    engine.state()
    

engine.disconnect()









