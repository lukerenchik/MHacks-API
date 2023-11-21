# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 10:58:08 2022

@author: Derek Joslin
"""

import RomReader as rr


ThisRom = rr.RomReader('C:/Users/derek/OneDrive/NewHaptics Shared/HapticOS/FC_GUI_API/APIv0.7-Coeus/v0.757-Coeus/ROMs/avalanche.rom')
    
romSettings = ThisRom.getSettings()
romComments = ThisRom.getDescriptions()


romInterrupts = ThisRom.getInterrupAddressNames()

print(romInterrupts[0])
#print(romSettings['interruptAddressDictionary'])
# =============================================================================
# 
# #take interrupt dictionary string and turn it into a dictionary
# interruptAddressDictionary = romSettings['interruptAddressDictionary']
# interruptAddressDictionary = interruptAddressDictionary.replace('{', "")
# interrupts = interruptAddressDictionary.split(',')
# interruptNames = []
# for interrupt in interrupts:
#     interruptName = interrupt.split(':')
#     interruptName = interruptName[0]
#     interruptNames.append(interruptName)
#     
#     
# print(interruptNames)
# =============================================================================
