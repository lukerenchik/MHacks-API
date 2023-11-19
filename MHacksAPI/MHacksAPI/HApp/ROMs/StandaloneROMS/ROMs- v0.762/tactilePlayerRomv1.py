# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 10:43:01 2022

@author: Derek Joslin
"""

import time
import NHAPI as nh
import keyboard

def touchToBegin():
    global engine
    global startPosition
    global cursorPosition
    print("touch screen to start")
    engine.braille((0,0),"touch screen to start")
    engine.desired()
    engine.refresh()
    engine.state()
    while startPosition == cursorPosition:
        cursorPosition = engine.getCursorPosition()

def startScreen():
    global engine
    engine.braille((0,0),"move your finger on the touch screen to change bar size")
    engine.desired()
    engine.refresh()
    engine.state()

engine = nh.NHAPI()
engine.connect("COM9",0)
engine.connectTouchScreen("COM7")

displaySize = engine.return_displaySize()


nRows = displaySize[0]
nColumns = displaySize[1]

xIncrement = 1
yIncrement = 1
score = 0

#game settings
echo = 0

tic = 0
startPosition = [0,0]


cursorPosition = engine.getCursorPosition()
startPosition[0] = cursorPosition[0]
startPosition[1] = cursorPosition[1]


touchToBegin()

startScreen()

while not keyboard.is_pressed('o'):
        
        cursorPosition = engine.getCursorPosition()
        
        if startPosition != cursorPosition:
            engine.setCursorPosition(cursorPosition)
            
            
            engine.stroke(3)
            engine.line((17,0), (17,cursorPosition[0]))
            
            
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
            
        startPosition[0] = cursorPosition[0]
        startPosition[1] = cursorPosition[1]
else:
    print("Exited Program")
    engine.braille((0,0),"exited program")
    engine.desired()
    engine.refresh()
    engine.state()
    

engine.disconnect()









