# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 15:53:36 2022

@author: Derek Joslin
"""

import NHAPI as nh
import time
import keyboard


BrailleDisplay = nh.NHAPI()
BrailleDisplay.connect("COM12",0)
BrailleDisplay.connectTouchScreen("COM7")

pinDimensions = BrailleDisplay.getPinCursorDimensions()
inputDimensions = BrailleDisplay.getInputCursorDimensions()

pinPosition = BrailleDisplay.getPinCursorPosition()
inputPosition = BrailleDisplay.getInputCursorPosition()

while not keyboard.is_pressed('o'):
    
    tic = time.perf_counter()
    pinPosition = BrailleDisplay.getPinCursorPosition()
    inputPosition = BrailleDisplay.getInputCursorPosition()
    toc = time.perf_counter()
    print(pinPosition)
    print(inputPosition)
    
    
    
    
    
    
BrailleDisplay.disconnect()