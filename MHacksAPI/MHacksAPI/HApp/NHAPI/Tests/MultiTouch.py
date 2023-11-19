# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 16:02:13 2023

@author: Derek Joslin

"""

import NHAPI as nh
import TouchScreenInterface as ts


TactileDisplay = nh.NHAPI("test")

# connect to the tactile display
TactileDisplay.connect("COM12", 0)

# connect to the first touchscreen
#TactileDisplay.connectTouchScreen("wow", "COM21")

# connect to the second touchscreen
TactileDisplay.connectTouchScreen("wat", "COM7")


touch1 = TactileDisplay.TouchScreenList[0]
#touch2 = TactileDisplay.TouchScreenList[1]

position1 = touch1.getTouchPosition()
#position2 = touch2.getTouchPosition()


print(position1)
#print(position2)


combinedPosition = TactileDisplay.getTouchScreenPosition()

print(combinedPosition)


while 1:
    combinedPosition = TactileDisplay.getTouchScreenPosition()
    touchScreenDimensions = TactileDisplay.getInputCursorDimensions()
    
    print("The Touchscreen dimensions are {}".format(touchScreenDimensions))
    print("The current TouchScreen position is {}".format(combinedPosition))
    

