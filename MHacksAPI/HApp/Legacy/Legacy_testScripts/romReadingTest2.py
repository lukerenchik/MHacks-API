# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 15:46:14 2022

@author: Derek Joslin
"""


import romReader as rr

filename = "C:\\Users\\derek\\OneDrive\\NewHaptics Shared\\HapticOS\\FC_GUI_API\\APIv0.7-Coeus\\v0.75-Coeus\\ROMs\\avalanche.rom"



thisRom = rr.romReader(filename)

romSettings = thisRom.getSettings()

print(romSettings)


#thisRom.executeRom()