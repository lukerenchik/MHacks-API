# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 15:01:46 2023

@author: Derek Joslin

"""

import RomAPI as rs

import DefaultKeyboardHandles as dh

class PongKeyboardHandles(dh.DefaultKeyboardHandles):
    
    def __init__(self, GameFlag):
        super().__init__()
        
        self.GameFlag = GameFlag
        
        self.godMode = 0
        #self.PongModel = PongModel


    def addPongModel(self, PongModel):
        self.PongModel = PongModel
        
    def KeyLeftHandler(self):
        #perform cursor movement left
        self.PongModel.moveLeft()
        
    def KeyUpHandler(self):
        #perform cursor movement up
        if self.godMode:
            self.PongModel.moveUp()
        
    def KeyRightHandler(self):
        #perform cursor movement right
        self.PongModel.moveRight()
        
    def KeyDownHandler(self):
        #perform cursor movement down
        self.PongModel.moveDown()
        
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