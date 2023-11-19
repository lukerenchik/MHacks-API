# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 14:11:19 2023

@author: Derek Joslin

"""

import DefaultMouseHandles as dh

class AvalancheMouseHandles(dh.DefaultMouseHandles):
    
    def __init__(self, AvalancheModel, HAppControlCenter):
        super().__init__()
        
        self.HAppControlCenter = HAppControlCenter
        
        self.AvalancheModel = AvalancheModel
        
    