# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 16:15:59 2023

@author: Derek Joslin

"""

class TouchTunesModel:
    def __init__(self, nColumns, nRows, TunesFlag):
        self.TunesFlag = TunesFlag
        self.nColumns = nColumns
        self.nRows = nRows
        self.barIndex = 0
        self.bars = [0 for i in range(self.nRows)]

    def setBarLength(self, newLength):
        if self.barIndex >= 0 and self.barIndex < self.nColumns:
            self.bars[self.barIndex] = newLength
            
    def selectBar(self, newBarIndex):
        self.TunesFlag.barSelectedIndex = newBarIndex
        if newBarIndex >= 0 and newBarIndex < self.nRows:
            self.barIndex = newBarIndex
            
    def getBarLength(self):
        return self.bars[self.barIndex]