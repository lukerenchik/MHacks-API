# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 12:47:27 2021

@author: Derek Joslin
"""

import sys

import NHAPI as nh


import time

import numpy as np

import pyqtgraph as pg

from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore as qc
from PyQt5 import QtWidgets as qw


import threading


ARDState = [[1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, ],
         [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, ],
         [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, ],
         [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, ],
         [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, ],
         [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, ],
         [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, ],
         [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, ],
         [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, ],
         [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ],
         [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, ],
         [0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, ],
         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, ],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]]



#Matrix display funcmtion
def display_matrix(matrix, num):
    print("num: {}".format(num))
    print('---------------------------\n')
    print('\n'.join([' '.join(['{:4}'.format(item) for item in row])
                     for row in matrix]))
    print('---------------------------\n')



#create a visual plot for the current state
class stateDisplay(pg.PlotWidget):
    
    """
    Will recieve the state data and generate a scatter plot of icons that looks similar to the device display
    uses pin icons for the scatter plot icons. Automatically creates the board of the right size.
    """

    def __init__(self, state):
        
        super().__init__()
        
        
        #clear pen
        self.pen = pg.mkPen(color=(0, 0, 0))
        
        self.state = state
        newMat = np.array(state)
        dim = newMat.shape
        self.__columns = dim[1]
        self.__rows = dim[0]
        self.__numElem = self.__columns*self.__rows
        self.createDisplay()
        
        
    
    def createDisplay(self):
        
        #clear the widget
        self.clear()
        
        
        #put the current state into a form that is plottable
        columnIndices = [i for i in range(0,self.__columns)]*self.__rows
        rowIndices = []
        for i in range(0,self.__rows):    
            rowIndices = rowIndices + [i]*self.__columns
            
        self.display = self.plot(columnIndices, rowIndices, pen=self.pen, symbol = 'o')
        self.setXRange(0,self.__columns)
        self.setYRange(0,self.__rows)
        self.invertY()
        
        
    def updateDisplay(self, newState):
        columnIndices = []
        rowIndices = []
        self.state = newState
        
        for rowIndex,row in enumerate(self.state):
            for colIndex,val in enumerate(row):
                if val:
                    #print(colIndex)
                    columnIndices.append(colIndex)
                    rowIndices.append(rowIndex)
                else:
                    pass
        
        #print(columnIndices)
        #print(rowIndices)
        
        self.display.setData(columnIndices,rowIndices)
        self.setXRange(0,self.__columns)
        self.setYRange(0,self.__rows)
        self.invertY()




def displayUpdater():
    #connect to the board
    api = nh.NHAPI()
    api.connect("COM10")
    
    time.sleep(4)
    
    #loop reading from the arduino and updating the display
    while 1:
        #loop recieving the matrix from the arduino and displaying the result
        outputBuffer = []
        #grab the matrix from the arduino
        outputBuffer.append(3)
        ARDState = api.state()
    
        try:
            ARDState = api.state()
            #replace with updating the display
            monitor.updateDisplay(ARDState)
        except: 
            print(ARDState)



if __name__ == '__main__':
    app = QApplication([])


    #create all the graphics features
    window = qw.QMainWindow()
    dock = qw.QDockWidget("current state", window, qc.Qt.Widget)
    window.setCentralWidget(dock)
    monitor = stateDisplay(ARDState)    
    dock.setWidget(monitor)
    monitor.updateDisplay(ARDState)
    window.show()#Maximized()
    
    
    ARDState = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]]
    
    #monitor.updateDisplay(ARDState)
    
    #window.show()
    
    
# =============================================================================
#     #connect to the board
#     port = serial.Serial("COM10", 57600, timeout = 1)
#     
#     time.sleep(4)
#     
#     #loop recieving the matrix from the arduino and displaying the result
#     outputBuffer = []
#     #grab the matrix from the arduino
#     outputBuffer.append(3)
#     
#     
#     
#     #loop reading from the arduino and updating the display
#     for i in range(0,50):
#         time.sleep(0.1)
#         port.write(bytearray(outputBuffer))
#     
#         port.flush()
#         ARDState = port.read_until(b'\x03')
#     
#         try:
#             #convert to list
#             ARDState = np.array(list(ARDState))
#             
#             ARDState = np.delete(ARDState, -1)
#             ARDState = np.reshape(ARDState, (15,14))
#             
#             #convert the matrix to a list
#             ARDState = ARDState.tolist()
#             
#             #replace with updating the display
#             monitor.updateDisplay(ARDState)
#         except: 
#             print(ARDState)     
#     
#     port.close()
# =============================================================================
    
    
    
    updateThread = threading.Thread(target = displayUpdater)
    updateThread.start()
    
    
    
    sys.exit(app.exec_())


