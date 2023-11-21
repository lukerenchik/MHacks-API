# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 10:20:19 2022

@author: Derek Joslin
"""

import RomReader as rr

import NHAPI as nh


BrailleDisplay = nh.NHAPI()

BrailleDisplay.connect("COM5")

BrailleDisplayAddress = id(BrailleDisplay)


ThisRom = rr.RomReader('C:/Users/derek/OneDrive/NewHaptics Shared/HapticOS/FC_GUI_API/APIv0.7-Coeus/v0.756-Coeus/ROMs/avalanche.rom')
    
romSettings = ThisRom.getSettings()
romComments = ThisRom.getDescriptions()

romSettings['BrailleDisplayAddress'] = BrailleDisplayAddress

ThisRom.setSettings(romSettings)

ThisRom.executeRom()



