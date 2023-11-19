# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 16:52:24 2023

@author: Derek Joslin

"""

import RomAPI as rs

import DefaultKeyboardHandles as dh

class AvalancheKeyboardHandles(dh.DefaultKeyboardHandles):
    
    def __init__(self, GameFlag):
        super().__init__()
        
        self.GameFlag = GameFlag
        
        self.godMode = 0
        #self.AvalancheModel = AvalancheModel


    def addAvalancheModel(self, AvalancheModel):
        self.AvalancheModel = AvalancheModel
        
    def KeyLeftHandler(self):
        #perform cursor movement left
        self.AvalancheModel.moveLeft()
        
    def KeyUpHandler(self):
        #perform cursor movement up
        if self.godMode:
            self.AvalancheModel.moveUp()
        
    def KeyRightHandler(self):
        #perform cursor movement right
        self.AvalancheModel.moveRight()
        
    def KeyDownHandler(self):
        #perform cursor movement down
        self.AvalancheModel.moveDown()
        
    def KeyCapsLockHandler(self):
        if not self.godMode:
            self.godMode = 1
            print("Gode Mode on")
        else:
            self.godMode = 0
            print("God Mode off")
        
    def KeySpaceHandler(self):
        if self.GameFlag.gameState == "Start Menu":
            self.GameFlag.gameState = "Game"
        else:
            self.GameFlag.gameState = "Start Menu"
            
    def KeyOHandler(self):
        self.GameFlag.gameState = "Exit Rom"