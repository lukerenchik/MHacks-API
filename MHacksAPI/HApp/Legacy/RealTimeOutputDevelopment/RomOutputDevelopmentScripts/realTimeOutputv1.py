# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 14:42:29 2022

@author: Derek Joslin
"""

import NHAPI as nh
import keyboard

#create an api object
BrailleDisplay = nh.NHAPI()
BrailleDisplay.connect("COM10",1)
endRom = 0


while not keyboard.is_pressed('o') and (endRom is 0):
    #grab the state of the arduino
    state = BrailleDisplay.state()
    
    


else:

    BrailleDisplay.disconnect()










