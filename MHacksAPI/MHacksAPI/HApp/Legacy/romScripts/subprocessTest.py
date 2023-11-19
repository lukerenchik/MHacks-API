# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 13:31:26 2022

@author: Derek Joslin
"""

import NHAPI as nh
import romReader as rr
import subprocess
import threading
import sys

superHotFile = "C:/Users/derek/OneDrive/NewHaptics Shared/HapticOS/FC_GUI_API/APIv0.7-Coeus/v0.73-Coeus/superHotPongRom.py"

filename = "C:/Users/derek/OneDrive/Documents/dist/HapticVisualizer/HapticVisualizer.exe"

engine = nh.NHAPI()
engine.connect("COM3",0)
engine.connectTouchScreen("COM7")

apiString = str(id(engine))

#pongRom = rr.romReader(superHotFile)

#pongRom.executeRom([8,0])

subprocess.call([sys.executable,superHotFile,'8','0',apiString],shell=True)
