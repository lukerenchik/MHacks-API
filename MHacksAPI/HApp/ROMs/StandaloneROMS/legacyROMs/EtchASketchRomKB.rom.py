# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 16:15:54 2022

@author: Derek Joslin
"""

import NHAPI as nh
import time
import keyboard


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
            cursorPosition[0] -= 1
        else:
            pass
        
    if keyboard.is_pressed("right"):
        if cursorPosition[0] < 41:
            cursorPosition[0] += 1
        else:
            pass

engine = nh.NHAPI()

engine.connect("COM3",0)

displaySize = engine.return_displaySize()

nRows = displaySize[0]
nColumns = displaySize[1]

tic = 0
startPosition = [0,0]


echo = 1

cursorPosition = engine.getCursorPosition()
startPosition[0] = cursorPosition[0]
startPosition[1] = cursorPosition[1]

print("touch screen to start")
engine.braille((0,0),"touch a sketch, touch screen to start")
engine.desired()
engine.refresh()
engine.state()
engine.clear()
while startPosition == cursorPosition:
    keyboardControl()
    

while not keyboard.is_pressed('o'):
    
    keyboardControl()
    
    try:
        engine.dot((cursorPosition[1],cursorPosition[0]))
    except:
        print("error")
    
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
    
    
else:
    engine.clear()
    print("touch a sketch off")
    engine.braille((8,20),"touch a sketch off")
    engine.desired()
    engine.refresh()
    engine.state()
    time.sleep(0.5)

engine.disconnect()