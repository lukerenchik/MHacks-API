# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 11:46:34 2023

@author: Derek Joslin

"""

import DefaultMouseHandles as dm

class HAppMouseHandles(dm.DefaultMouseHandles):
    
    def __init__(self, StateVisualizer):
        self.StateVisualizer = StateVisualizer