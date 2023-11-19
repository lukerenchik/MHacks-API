# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 16:19:04 2022

@author: Derek Joslin
"""

import TouchScreenInterface as ts
import time
import keyboard


Sensor = ts.TouchScreenInterface("COM7",0)



touchScreenDimensions = Sensor.getTouchScreenDimensions()
touchPosition = Sensor.getTouchPosition()

positionList = []

while not keyboard.is_pressed('o'):
    
    tic = time.perf_counter()
    touchPosition = Sensor.getTouchPosition()
    positionList.append(touchPosition)
    toc = time.perf_counter()
    print(touchPosition)  
    
Sensor.close()