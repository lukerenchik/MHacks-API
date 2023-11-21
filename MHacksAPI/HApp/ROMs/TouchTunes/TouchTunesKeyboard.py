# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 17:02:58 2023

@author: Derek Joslin

"""


import DefaultKeyboardHandles as dh

""" class to handle keyboard inputs for the touch tunes rom """

# class to handle keyboard inputs for the touch tunes rom
class TouchTunesKeyboardHandles(dh.DefaultKeyboardHandles):
    
    # constructor
    def __init__(self, TouchTunesModel, TunesFlag):
        # add the model to the keyboards
        self.TouchTunesModel = TouchTunesModel
        
        # The number of rows in the device
        
        # flag for Touch Tunes
        self.TunesFlag = TunesFlag
        
        # keep track of selected bar
        self.barSelectedIndex = 0
        
    # handles key up event
    def KeyUpHandler(self):
        # if selected bar is not at the top
        if self.barSelectedIndex > 0:
            # move the selection one row up
            self.barSelectedIndex -= 1
        
        # select the bar on the touch tunes model
        self.TouchTunesModel.selectBar(self.barSelectedIndex)
 
        # update the selected bar index in TouchTunesFlag
        self.TunesFlag.barSelectedIndex = self.barSelectedIndex
        
        # set the flag state to 1 to indicate a change in state
        self.TunesFlag.setState(1)
        
    # handles key down event
    def KeyDownHandler(self):
        # if selected bar is not at the bottom
        if self.barSelectedIndex < (self.TouchTunesModel.nRows - 1):
            # move the selection one row down
            self.barSelectedIndex += 1
        
        # select the bar on the touch tunes model
        self.TouchTunesModel.selectBar(self.barSelectedIndex)
        
        # update the selected bar index in TouchTunesFlag
        self.TunesFlag.barSelectedIndex = self.barSelectedIndex
        
        # set the flag state to 1 to indicate a change in state
        self.TunesFlag.setState(1)
        
    # handles key right event
    def KeyRightHandler(self):
        # select the bar and get the current length
        self.TouchTunesModel.selectBar(self.barSelectedIndex)
        length = self.TouchTunesModel.getBarLength()
                
        # increment the length by 1
        if length < self.TouchTunesModel.nColumns:
            length += 1
        
        # assign the new length to the TouchTunesFlag
        self.TunesFlag.barLength = length
        
        # set the new length for the selected bar in the TouchTunesModel
        self.TouchTunesModel.setBarLength(length)
        
        # set the flag state to 1 to indicate a change in state
        self.TunesFlag.setState(1)
        
    # handles key left event
    def KeyLeftHandler(self):
        # select the bar and get the current length
        self.TouchTunesModel.selectBar(self.barSelectedIndex)
        length = self.TouchTunesModel.getBarLength()
        
        if length > 0:
        # decrement the length by 1
            length -= 1
        
        # assign the new length to the TouchTunesFlag
        self.TunesFlag.barLength = length
        
        # set the new length for the selected bar in the TouchTunesModel
        self.TouchTunesModel.setBarLength(length)
        
        # set the flag state to 1 to indicate a change in state
        self.TunesFlag.setState(1)
        
    def KeyOHandler(self):
        self.TunesFlag.gameState = "Exit Rom"