# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 14:49:48 2022

@author: Derek Joslin
"""

import NotePadEditor as npe


class FileNavigatorEditor(npe.NotePadEditor):

    def __init__(self, nDotRows, nDotColumns):
        
        super().__init__(nDotRows, nDotColumns)
        
        self.lineSelect = 0
        self.cursorMode = 0
        self.period = 100
        self.dutyCycle = 0.5
        self.touchScreenMode = 0
        