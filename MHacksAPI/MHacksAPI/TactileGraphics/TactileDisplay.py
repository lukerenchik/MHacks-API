# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 12:25:03 2020

@author: Derek Joslin

"""

import copy
from DisplaySerial import DisplaySerial


class TactileDisplay(DisplaySerial):
    
    def __init__(self, *args):
        super().__init__(*args)
        self.getSize()
        self.refreshRate = 290


    def getSize(self):
        self.nRows = self.getNRows()
        self.nColumns = self.getNColumns()
        self.nBytesPerRow = self.getNBytesPerRow()
        self.nBytesPerColumn = self.getNBytesPerColumn()
        
        
    def setRefreshRate(self, _refreshRate):
        # default setup
        setup = 5
        # default hold
        hold = 50
        self.refreshRate = _refreshRate
        pulseWidth = _refreshRate - setup - hold
        # variable pulse width
        self.setRefreshParameters([setup, hold, pulseWidth])
        
    # add more error handling to the setRow command
    def _setRowErrorHandler(self, rowIndex, rowData):
        # run the regular function if passing all error handling
        super()._setRowErrorHandler(rowIndex, rowData)
        
        rowDataLength = len(rowData)
        
        # check that the proper size row bytes are sent
        if rowDataLength != self.nColumns:
            raise ValueError(f"""input to setRow has the incorrect
                             number of column dots being set. Number of columns on the device is {self.nColumns},
                             number of columns given in setRow command is {rowDataLength}""")
                             
        # check that the row being indexed is within the proper limitations of the device
        if rowIndex > self.nRows or rowIndex < 0:
            raise ValueError(f"""the row being set in the setRow command ({rowIndex})
                             has a value which is greater than the number of rows on the device ({self.nRows})
                             or less than 0 (bad).""")
              
                             
