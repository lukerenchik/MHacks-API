# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 12:20:57 2022

@author: Derek Joslin
"""

import NHAPI as nh
import time

engine = nh.NHAPI()

engine.connect("COM5",0)
engine.connectTouchScreen("COM7")

tic = 0
position = [0,0]

while 1:
    try:
        engine.setCursorPosition(position)
        
        
        #if X > 13:
        #    X = 13
            
        #if Y > 14:
        #   Y = 14
        
        #Y = abs(19-Y)
        #X = abs(41-X)
        cursorPosition = engine.getCursorPosition()
        
        print("{0},{1}".format(cursorPosition[0],cursorPosition[1]))
        engine.dot((cursorPosition[1],cursorPosition[0]))
        
        
        engine.desired()
        engine.refresh()
        
        engine.state()
        
        toc = time.perf_counter()
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print("{0},{1}".format(position[0],position[1]))
        print(toc-tic)
        tic = time.perf_counter()
        engine.clear()
        
        if position[0] < 13:
            position[0] = position[0] + 1
        else:
            position[0] = 0
            position[1] = position[1] + 1
            
        if position[1] > 14:
            position[1] = 0
            
    except:
        print("error")
engine.disconnect()