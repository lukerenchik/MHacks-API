# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 15:12:42 2022

@author: Derek Joslin
"""

import RomAPI as rs


class SampleKeyboardHandles(rs.RomKeyboardHandles):
    
    def __init__(self, Controller):
        super().__init__()
        
        self.Controller = Controller
        
    def KeyUpHandler(self):
        #turn romContinue on
        self.Controller.setInterruptFlag('romContinue', 1)
        
    def KeyDownHandler(self):
        #turn escape on
        self.Controller.setInterruptFlag('romHaltSerial', 1)
        
    def KeyAHandler(self):
        #turn escape on
        self.Controller.setInterruptFlag('romHaltSerial', 0)
        