# -*- coding: utf-8 -*-
"""
Created on Thu May 20 14:10:58 2021

@author: Derek Joslin
"""

#import pyqtgraph as pg

import qrc_resources

from pyqtconsole.console import PythonConsole
import pyqtconsole.highlighter as hl

#override close event
class APIConsole(PythonConsole):
    def __init__(self, api, OperationsController):
        
        self.OperationsController = OperationsController
        self.api = api

        super().__init__(formats={
            'keyword':    hl.format('blue', 'bold'),
            'operator':   hl.format('red'),
            'brace':      hl.format('darkGray'),
            'defclass':   hl.format('black', 'bold'),
            'string':     hl.format('magenta'),
            'string2':    hl.format('darkMagenta'),
            'comment':    hl.format('darkGreen', 'italic'),
            'self':       hl.format('black', 'italic'),
            'numbers':    hl.format('brown'),
            'inprompt':   hl.format('darkBlue', 'bold'),
            'outprompt':  hl.format('darkRed', 'bold'),
            })



        #add all the api functions to the gui console
        super().push_local_ns('erase', self.api.erase)
        super().push_local_ns('fill', self.api.fill)
        super().push_local_ns('stroke', self.api.stroke)
        super().push_local_ns('direct', self.api.direct)
        super().push_local_ns('dot', self.api.dot)
        super().push_local_ns('cell', self.api.cell)
        super().push_local_ns('line', self.api.line)
        super().push_local_ns('curve', self.api.curve)
        super().push_local_ns('circle', self.api.circle)
        super().push_local_ns('rect', self.api.rect)
        super().push_local_ns('triangle', self.api.triangle)
        super().push_local_ns('polygon', self.api.polygon)
        super().push_local_ns('latin', self.api.latin)
        super().push_local_ns('braille', self.api.braille)
        super().push_local_ns('clear', self.api.clear)
        super().push_local_ns('Fclear', self.api.Fclear)
        super().push_local_ns('state', self.api.state)
        super().push_local_ns('desired', self.api.desired)
        super().push_local_ns('refresh', self.api.refresh)
        super().push_local_ns('setMat', self.api.setMat)
        super().push_local_ns('size', self.api.size)
        super().push_local_ns('connect', self.api.connect)
        super().push_local_ns('disconnect', self.api.disconnect)
        super().push_local_ns('settings', self.api.settings)
        super().push_local_ns('cursorPos', self.api.cursorPos)
        super().push_local_ns('connectTouch', self.api.connectTouch)
        super().push_local_ns('disconnectTouch', self.api.disconnectTouch)
        
        
        
        # =============================================================================
        #         super().push_local_ns("test", self.testFunction)
        #         super().push_local_ns('dot', self.consoleDot)
        # =============================================================================
        
        

    def closeEvent(self,event):
        if self.api.comLink_check():
            self.api.comLink_check()
            event.accept()
        else:
            event.accept()
            
# =============================================================================
#             
#         #put the current state into a form that is plottable
#         columnIndices = [i for i in range(0,self.__columns)]*self.__rows
#         rowIndices = []
#         for i in range(0,self.__rows):    
#             rowIndices = rowIndices + [i]*self.__columns
#             
#         self.display = self.plot(columnIndices, rowIndices, pen=self.pen, symbol = 'o')
#         self.setXRange(0,self.__columns)
#         self.setYRange(0,self.__rows)
#         self.invertY()
# =============================================================================
        
        
    def testFunction(self):
        print("this is a function test")
        
# =============================================================================
#         
#     def consoleDot(self, coord):
#         self.OperationsController.pauseExecutingOperations()
#         print("this is a test")
#         self.api.dot(coord)
#         self.OperationsController.resumeExecutingOperations()
#         
#         
# =============================================================================
        

# =============================================================================
#         
#     def updateDisplay(self):
#         columnIndices = []
#         rowIndices = []
#         
#         
#         for rowIndex,row in enumerate(self.state):
#             for colIndex,val in enumerate(row):
#                 if val:
#                     #print(colIndex)
#                     columnIndices.append(colIndex)
#                     rowIndices.append(rowIndex)
#                 else:
#                     pass
#         
#         #print(columnIndices)
#         #print(rowIndices)
#         
#         self.display.setData(columnIndices,rowIndices)
#         
# 
# =============================================================================
