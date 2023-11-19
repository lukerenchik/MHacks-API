# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 11:21:11 2022

@author: Derek Joslin
"""


import DefaultKeyboardHandles as dh

class NewKeyboardHandles(dh.DefaultKeyboardHandles):
    
    def __init__(self):
        
        super().__init__()
        
    def KeyLeftHandler(self):
        print("new left key pressed")
        
    def KeyUpHandler(self):
        print("new up key pressed")
        
    def KeyRightHandler(self):
        print("new right key pressed")
        
    def KeyDownHandler(self):
        print("new down key pressed")

