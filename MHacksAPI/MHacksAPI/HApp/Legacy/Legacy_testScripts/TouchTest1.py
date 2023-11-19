# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 11:55:42 2022

@author: Derek Joslin
"""

import TouchScreenInterface as ts


sensor = ts.TouchScreenInterface("COM7")

position = sensor.getTouchPosition()

print(position)