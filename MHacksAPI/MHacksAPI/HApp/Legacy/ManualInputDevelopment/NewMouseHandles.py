# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 10:54:51 2022

@author: Derek Joslin

"""

import DefaultMouseHandles as dm

class NewMouseHandles(dm.DefaultMouseHandles):
    
    def __init__(self):
        super().__init__()
        
    def LeftButtonHandler(self, xCoordinate, yCoordinate):
        print("New left mouse button clicked")
    