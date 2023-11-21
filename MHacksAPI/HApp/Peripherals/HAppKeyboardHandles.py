# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 11:45:42 2023

@author: Derek Joslin

"""

import DefaultKeyboardHandles as dk

class HAppKeyboardHandles(dk.DefaultKeyboardHandles):
    
    def __init__(self, StateVisualizer):
        self.StateVisualizer = StateVisualizer
        
    def KeyTabHandler(self):
        self.StateVisualizer.changeDisplay()
        print("changing display")