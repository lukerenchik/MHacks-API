# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 16:15:54 2022

@author: Derek Joslin
"""

import NHAPI as nh
import time
import keyboard





engine = nh.NHAPI()

engine.connect("COM3",0)
engine.connectTouchScreen("COM7")

displaySize = engine.return_displaySize()

nRows = displaySize[0]
nColumns = displaySize[1]

tic = 0
startPosition = [0,0]


echo = 0

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
    cursorPosition = engine.getCursorPosition()
    

while not keyboard.is_pressed('o'):
    
    cursorPosition = engine.getCursorPosition()
    
    try:
        engine.dot((cursorPosition[1],cursorPosition[0]))
    except:
        print("error")
    
    engine.desired()
    engine.refresh()
    
    engine.state()
    if keyboard.is_pressed('a'):  # if key 'a' is pressed 
        engine.clear()
    toc = time.perf_counter()
    if echo:
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print("{0},{1}".format(cursorPosition[0],cursorPosition[1]))
        print(toc-tic)
    tic = time.perf_counter()
    
    
else:
    engine.clear()
    engine.braille((9,20),"touch a sketch off")
    engine.desired()
    engine.refresh()
    engine.state()
    time.sleep(0.5)

engine.disconnect()