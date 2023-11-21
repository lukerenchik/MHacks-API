# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 09:44:14 2022

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
    stateVisualizer = rv.RealTimeStateVisualizer(BrailleDisplay)
    
    BrailleDisplayAddress = id(BrailleDisplay)
    
    romHaltAddress = id(stateVisualizer.romHalt)
    pauseRomAddress = id(stateVisualizer.pauseRom)
    endRomAddress = id(stateVisualizer.endRom)
    
    ThisRom = rr.RomReader('C:/Users/derek/OneDrive/NewHaptics Shared/HapticOS/FC_GUI_API/APIv0.7-Coeus/v0.757-Coeus/ROMs/avalanche.rom')
    
    
    
    romSettings = ThisRom.getSettings()
    romInterrupts = ThisRom.getInterrupAddressNames()
    romComments = ThisRom.getDescriptions()
    interruptAddressDictionary = {'romHalted': romHaltAddress,
                                  'pauseRom': pauseRomAddress,
                                  'endRom': endRomAddress}
    
    romSettings['BrailleDisplayAddress'] = BrailleDisplayAddress
    romSettings['interruptAddressDictionary'] = interruptAddressDictionary
   
    
    
    
    ThisRom.setSettings(romSettings)
    
    ThisRom.executeRom()
    
    
    sys.exit(app.exec_())