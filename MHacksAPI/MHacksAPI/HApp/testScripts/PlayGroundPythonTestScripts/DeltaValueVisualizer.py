# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 11:20:45 2023

@author: Derek Joslin

"""


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel
from PyQt5 import QtGui as qg
import time
import PyQt5.QtCore as qc
import serial.tools.list_ports
import serial
import numpy as np


class SensorWindow(QMainWindow):
    def __init__(self, touchSerial):
        super().__init__()

        self.setWindowTitle("Sensor Heatmap")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.grid_layout = QGridLayout(self.central_widget)

        self.startTime = 0
        self.endTime = 0


        self.sensorList = []
        # Create labels for each sensor
        for i in range(35):
            sensor = QLabel()
            self.sensorList.append(sensor)
            sensor.setAlignment(qc.Qt.AlignCenter)
            self.grid_layout.addWidget(sensor, i // 7, i % 7)
            
        self.sensorDataMatrix = np.ones([5,7])
            
        self.touchPointList = []
# =============================================================================
#         # Get a list of available COM ports
#         comports = list(serial.tools.list_ports.comports())
#         
#         # Check if any COM ports are available
#         if not comports:
#             print('No COM ports available')
#             exit()
#             
#         # Connect to the first available COM port
#         port = comports[0].device
#         baudrate = 115200  # Set the baud rate to use for the serial connection
#         timeout = 1  # Set the timeout for reading from the serial connection
# =============================================================================
        
        self.ser = touchSerial#serial.Serial(port, baudrate, timeout=timeout)
        
        # Print information about the connected port
        print(f'Connected to {self.ser.name} ({self.ser.baudrate} baud)')

        # Send byte array
        self.byte_array = bytearray([1, 2, 3, 0, 2, 4, 35, 0, 3, 2, 1])
        self.ser.write(self.byte_array)

        self.comportBytes = []  # Create empty list to store received bytes
        
        # Create a QTimer that calls collect_sensor_data() every 1000 ms
        self.timer = qc.QTimer(self)
        self.timer.timeout.connect(self.collect_sensor_data)
        self.timer.start(1)
    
    def collect_sensor_data(self):
        # Read data from the COM port and parse the information
        # Update the sensor values using setSensorValues() function
        #print("collecting sensor data")

        sensorValues = []
        if self.ser.in_waiting > 44:  # Check if there are bytes in the input buffer
            # read all bytes
            # get time when timer ends
            self.startTime = time.perf_counter()
            while self.ser.in_waiting > 0:
            # self.startTime = time.perf_counter()
                byte = self.ser.read(45)  # Read a single byte from the serial port
                #print(byte)
                self.comportBytes = list(bytearray(byte))  # Add the byte to the list
        
            self.endTime = time.perf_counter()
            print("time to collect data: {}".format(self.endTime - self.startTime))
            #print(self.comportBytes)
            # self.comportBytes.clear()
            # self.ser.write(self.byte_array)
            #self.ser.flush()

            
        i = 0
        if len(self.comportBytes) == 45:
            self.comportBytes[0:7] = []
            self.comportBytes[-3:-1] = []
            byteString = ""
            for byte in self.comportBytes:
                smolString = ' {} '.format(byte)#format(int.from_bytes(byte, byteorder='big', signed=False))
                byteString += smolString
                sensorValues.append(smolString)
                i += 1
                if i > 5:
                    byteString += "\n"
                    i = 0
            self.comportBytes.clear()
            self.ser.write(self.byte_array)
            
            # start the timer to measure data collection time

            self.setSensorValues(sensorValues)
            
    def setSensorValues(self, sensorValues):
        # Set the value of each sensor label based on input values
        self.sensorDataMatrix = np.ones([5,7])
        
        sensorValues.pop()
        iRow = 4
        iColumn = 6
        try:
            for value in sensorValues:
                self.sensorDataMatrix[iRow][iColumn] = value
                iRow -= 1
                if iRow == -1:
                    iColumn -= 1
                    iRow = 4
        except:
            print(self.sensorDataMatrix)

        iRow = 0
        iColumn = 0
        for i,sensor in enumerate(self.sensorList):            
            try:                
                #sensor.setText(sensorValues[i])
                emptyPalette = qg.QPalette()
                emptyPalette.setColor(qg.QPalette.Window, qg.QColor("transparent"))
                sensor.setPalette(emptyPalette)
                sensor.setText('{}'.format(self.sensorDataMatrix[iRow][iColumn]))
                iColumn += 1
                if iColumn % 7 == 0:
                    iColumn = 0
                    iRow += 1
            except:
                pass            
            
        self.generateRedDots()
            
            
    def generateRedDots(self):
        # function to create a red dot wherever there are touch points
# =============================================================================
#         self.redDot = QLabel(self)
#         self.redDot.setStyleSheet("border: 5 px solid red")
#         self.redDot.setAutoFillBackground(True)
#         self.redDot.setFixedSize(10, 10)
#         
# =============================================================================
        # run center of mass function
        
        
        
        self.generateTouchPointList()
        
        
        #if maxValue > 7:
        # create red dot for each point in center of mass
        for point in self.touchPointList:
            
            # get the Qlabel at the index
            redDot = self.grid_layout.itemAtPosition(point[0],point[1])
            redDot = redDot.widget()
            redDot.setStyleSheet("border: 5 px solid red")
            # Set the background color to red
            palette = qg.QPalette()
            palette.setColor(qg.QPalette.Background, qg.QColor("red"))
            redDot.setAutoFillBackground(True)
            redDot.setPalette(palette)
        
    def generateTouchPointList(self):
        #self.touchPointList.clear()
        #largeIndex = np.argmax(self.sensorDataMatrix)
        #touchIndex = np.unravel_index(largeIndex, self.sensorDataMatrix.shape)
        
        self.endTime = time.perf_counter()
        print("time between data collections: {}".format(self.endTime - self.startTime))
        
        # calculate the index of all values above 7 in the array
        
        self.touchPointList = np.argwhere(self.sensorDataMatrix > 10)
        #print(self.touchPointList)
        
        self.startTime = time.perf_counter()
        
        
        
        #self.touchPointList.append(touchIndex)
        #return np.max(self.sensorDataMatrix)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SensorWindow()
    window.show()
    sys.exit(app.exec_())







