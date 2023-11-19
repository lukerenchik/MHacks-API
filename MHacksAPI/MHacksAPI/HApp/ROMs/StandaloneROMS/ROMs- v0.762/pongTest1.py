# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 13:19:07 2022

@author: Derek Joslin
"""
pongPosition = [2,2]
cursorPosition = [0,0]
xIncrement = 1
yIncrement = 1

def pongPhysics(position, cursorPosition):
    lineValues = [i for i in range(cursorPosition[0], cursorPosition[0] + 5)]
    pongX = position[0]
    pongY = position[1]
    global xIncrement
    global yIncrement
    
    if pongX > (41 - 1):
        xIncrement = -1
    
    if pongY > (19 - 1):
        yIncrement = -1
    
    if pongX < 1:
        xIncrement = 1
        
    if pongY < 1:
        yIncrement = 1
        
        
    newX = pongX + xIncrement
    newY = pongY + yIncrement
    
    return [newX,newY]



while 1:
    try:
        print(pongPosition)
        
        
        pongPosition = pongPhysics(pongPosition,cursorPosition)
    except:
        break