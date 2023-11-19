# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 10:40:45 2022

@author: Derek Joslin

"""


class DefaultMouseHandles():
    
    def __init__(self):
        #do nothing
        pass
        
    def LeftButtonHandler(self, xCoordinate, yCoordinate):
        print("Left mouse button clicked")
        
    def RightButtonHandler(self, xCoordrdinate, yCoordinate):
        print("Right mouse button clicked")
        
    def MoveHandler(self, xCoordrdinate, yCoordinate):
        print("Mouse has been moved")
        