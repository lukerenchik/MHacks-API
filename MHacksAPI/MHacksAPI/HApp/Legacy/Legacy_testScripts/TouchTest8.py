# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 10:43:34 2022

@author: derek
"""

import serial
import time

#sensor = ts.TouchScreenInterface("COM11",0)
port = serial.Serial("COM11", 57600, timeout=3)

time.sleep(2)

port.write(bytearray([30]))

#response = port.read(2)

#position = (response[0], response[1])#sensor.getTouchPosition()