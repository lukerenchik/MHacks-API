# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 11:48:52 2023

@author: Derek Joslin

"""

import sys
from PyQt5.QtWidgets import QApplication
import serial
import serial.tools.list_ports
import DeltaValueVisualizer

comports = list(serial.tools.list_ports.comports())
print(comports)
def generateTouchScreensList():
    # Get a list of available COM ports
    comports = list(serial.tools.list_ports.comports())
    
    # Check if any COM ports are available
    if not comports:
        print('No COM ports available')
        exit()
        
    print(comports)
    TouchScreenList = []
    for connection in comports:
        
        # Connect to the first available COM port
        port = connection.device
        baudrate = 115200  # Set the baud rate to use for the serial connection
        timeout = 1  # Set the timeout for reading from the serial connection
        
        TouchScreenList.append(serial.Serial(port, baudrate, timeout=timeout))
        
    return TouchScreenList

if __name__ == "__main__":
    TouchScreenList = generateTouchScreensList()
    app = QApplication(sys.argv)
    windowList = []
    for touchSerial in TouchScreenList:
        #print(touchSerial)
        windowList.append(DeltaValueVisualizer.SensorWindow(touchSerial))
        windowList[-1].show()
        
        
    sys.exit(app.exec())