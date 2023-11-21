# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 15:02:11 2023

@author: Derek Joslin

"""


import DefaultMouseHandles as dh

class PongMouseHandles(dh.DefaultMouseHandles):
    
    def __init__(self, PongModel, HAppControlCenter):
        super().__init__()
        
        self.HAppControlCenter = HAppControlCenter
        
        self.PongModel = PongModel
        
    