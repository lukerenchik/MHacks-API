# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 16:09:17 2023

@author: Derek Joslin

"""


import RomAPI as rs
import TouchTunesModel as tm
import TouchTunesOperations as to
import TouchTunesKeyboard as tk

class TunesStartMenu(rs.RomState):
    
    def __init__(self, Controller):
        # get the needed resources from the Control Center
        super().__init__(Controller)
        self.HAppControlCenter = self.Controller.HAppControlCenter
        self.TactileDisplay = self.HAppControlCenter.getPeripheral("NewHaptics Display SarissaV1")
        
    def startState(self):
        # create the flag
        self.TunesFlag = to.TunesFlag("Touch Tunes Flag")
        self.HAppControlCenter.addFlag(self.TunesFlag)
        
        # create the model
        self.TouchTunesModel = tm.TouchTunesModel(14, 5, self.TunesFlag)
        
        # create the bar rendering operation and add it to the HAppControlCenter
        self.TunesGraphicsRender = to.TunesGraphicsRender("TouchTunesGraphicsRender", self.TactileDisplay, self.TunesFlag, self.TouchTunesModel)
        self.HAppControlCenter.addOperation(self.TunesGraphicsRender)

        # create the keyboard controls for the device
        self.TouchTunesKeyboardHandles = tk.TouchTunesKeyboardHandles(self.TouchTunesModel, self.TunesFlag)
        
        # assign the keyboard to the peripheral device
        self.KeyboardPeripheral = self.HAppControlCenter.getPeripheral("Master Keyboard")
        self.KeyboardPeripheral.setNewKeyboardHandler(self.TouchTunesKeyboardHandles)
    
    def getNextState(self):
        # the only other state is Exit Rom
        return self.TunesFlag.gameState