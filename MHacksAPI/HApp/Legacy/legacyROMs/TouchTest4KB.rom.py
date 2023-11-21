# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 12:27:50 2022

@author: Derek Joslin
"""


import NHAPI as nh
import time
import keyboard as kb

engine = nh.NHAPI()

engine.connect("COM9",0)

displaySize = engine.return_displaySize()

nRows = displaySize[0]
nColumns = displaySize[1]



tic = 0
cursorPosition = [0,0]

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
        
        engine.dot((cursorPosition[1],cursorPosition[0]))
        
        
        engine.desired()
        engine.refresh()
        
        engine.state()
        
        toc = time.perf_counter()
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print("{0},{1}".format(cursorPosition[0],cursorPosition[1]))
        print(toc-tic)
        tic = time.perf_counter()
        engine.clear()
        
        if cursorPosition[0] < (nColumns - 1):
            cursorPosition[0] = cursorPosition[0] + 1
        else:
            cursorPosition[0] = 0
            cursorPosition[1] = cursorPosition[1] + 1
            
        if cursorPosition[1] > (nRows - 1):
            cursorPosition[1] = 0
            
    except:
        break
        print("error")
engine.disconnect()