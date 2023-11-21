# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 10:48:21 2022

@author: Derek Joslin
"""

import ctypes

class RomControlBus(dict):

    def __init__(self, interruptAddressDictionary):
        super().__init__(interruptAddressDictionary)

    def getInterruptFlag(self, interruptString):
        interruptValue = ctypes.cast(self[interruptString], ctypes.py_object).value
        return interruptValue


romHalt = 0
pauseRom = 1
endRom = 0


romHaltAddress = id(romHalt)
pauseRomAddress = id(pauseRom)
endRomAddress = id(endRom)


interruptAddressDictionary = {'romHalted': romHaltAddress,
                              'pauseRom': pauseRomAddress,
                              'endRom': endRomAddress}

RomController = RomControlBus(interruptAddressDictionary)

print(RomController.getInterruptFlag('romHalted'))
print(RomController.getInterruptFlag('pauseRom'))
print(RomController.getInterruptFlag('endRom'))






