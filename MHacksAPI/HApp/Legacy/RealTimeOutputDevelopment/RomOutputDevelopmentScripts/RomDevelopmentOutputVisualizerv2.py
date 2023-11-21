# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 11:23:22 2022

@author: Derek Joslin
"""

from PyQt5.QtWidgets import QApplication

import RealTimeStateVisualizer as rv

import NHAPI as nh

import RomReader as rr

import sys

#read in a rom and create a nhapi and have them running and displaying to the output at the same time


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    
    #create an api object
    BrailleDisplay = nh.NHAPI()
    BrailleDisplay.connect("COM5",0)
    
    BrailleDisplayAddress = id(BrailleDisplay)
    
    ThisRom = rr.RomReader('C:/Users/derek/OneDrive/NewHaptics Shared/HapticOS/FC_GUI_API/APIv0.7-Coeus/v0.758-Coeus/ROMs/avalanche2.rom')
    
    romSettings = ThisRom.getSettings()
    romInterruptNames = ThisRom.getInterruptNames()
    romComments = ThisRom.getDescriptions()

    stateVisualizer = rv.RealTimeStateVisualizer(BrailleDisplay)

    for romInterruptString in romInterruptNames:
        stateVisualizer.interruptDictionary[romInterruptString] = 0
    
    interruptDictionaryAddress = id(stateVisualizer.interruptDictionary)
    
    romSettings['BrailleDisplayAddress'] = BrailleDisplayAddress
    romSettings['interruptDictionaryAddress'] = interruptDictionaryAddress
   
    ThisRom.setSettings(romSettings)
    
    ThisRom.executeRom()
    
    sys.exit(app.exec_())