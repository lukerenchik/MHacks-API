# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 10:26:35 2022

@author: Derek Joslin
"""

import romReader as rr
import NHAPI as nh
import sys

filename = "C:/Users/derek/OneDrive/NewHaptics Shared/HapticOS/FC_GUI_API/APIv0.7-Coeus/v0.73-Coeus/superHotPongRom.py"

pongRom = rr.romReader(filename)


pongRom.executeRom()

