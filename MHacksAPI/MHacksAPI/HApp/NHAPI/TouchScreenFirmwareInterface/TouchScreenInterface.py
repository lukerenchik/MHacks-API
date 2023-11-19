# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 11:09:02 2022

@author: Derek Joslin
"""

import serial
import matplotlib.pyplot as plt


class TouchScreenInterface:
    
     #the touch screen interface object contains a serial port connection object and commands to communicate with hardware

    def __init__(self, port, *args):
        #115200 for the embedded board
        self.port = serial.Serial(port, 57600, timeout=3)
                
        if len(args) > 0:
            if args[0] == 1:
                self.__echo = 1
            else:
                self.__echo = 0
        else:
            self.__echo = 0
        self.port.flush()
        
        if self.__echo:
            print(self.__recieveBuffer)
        else:
            pass

        self.touchCursorDimensions = (255,255)
        self.touchPinDisplayDimensions = (19,20)
        getVerticalPositionCommand   = [1, 2, 3, 0, 2, 3, 0, 3, 2, 1]
        getHorizontalPositionCommand   = [1, 2, 3, 0, 2, 2, 0, 3, 2, 1]
        self.getVerticalPositionCommand = bytearray(getVerticalPositionCommand)
        self.getHorizontalPositionCommand = bytearray(getHorizontalPositionCommand)
        self.verticalPosition = 0#self.getVerticalTouchPosition()
        self.horizontalPosition = 0#self.getHorizontalTouchPosition()


    #sets the echo of the com port onOff (0=Off, 1=On)
    def echo(self, onOff):
        if onOff:
            self.__echo = 1
        else:
            self.__echo = 0
    
    #opens the serial port
    def open(self):
        self.port.open()
        self.__readSerialResponse()

    #closes the serial port
    def close(self):
        self.port.close()

    #if echo is on prints the recieve data
    def __print_rx(self):
        read = self.__read_rx()
        if self.__echo:
            print(read)
        else:
            pass
        
    #reads in data on the serial line
    def __read_rx(self):
        # self.port.flush()
        self.__recieveBuffer = self.port.read(1)
        return self.__recieveBuffer #.decode('utf-8')
    
    #reads one byte and prints based on echo state
    def __readSerialResponse(self):
        read = self.port.read(1)
        if self.__echo:
            print(read)
        else:
            pass

    
    # Function 1: gets the vertical position
    def getVerticalTouchPosition(self):
        #create list with required parameters
        #getVerticalPositionCommand   = [1, 2, 3, 0, 2, 3, 0, 3, 2, 1]
        #output = getVerticalPositionCommand
        response = []
        
        
        #self.port.flush()
        #print(self.port.inWaiting())
        #select the get vertical position command
        self.port.write(self.getVerticalPositionCommand)

        response = self.port.read(10)
        self.verticalPosition = self.touchCursorDimensions[1]  - response[-4]
        
        #try:
            #response = self.port.read_until(b'\x02\x01')
            #print(self.port.inWaiting())
            #self.verticalPosition = 255 - response[-4]
        #except:
           # print(self.port.inWaiting())
           # print("error recieving vertical data")
        
    # Function 2: gets the horizontal position
    def getHorizontalTouchPosition(self):
        #create list with required parameters
        #getHorizontalPositionCommand   = [1, 2, 3, 0, 2, 2, 0, 3, 2, 1]
        #output = getHorizontalPositionCommand
        response = []

        #self.port.flush()
        #print(self.port.inWaiting())
        #select the get horizontal position command
        self.port.write(self.getHorizontalPositionCommand)

        response = self.port.read(10)
        
        self.horizontalPosition = self.touchCursorDimensions[0]  - response[-4]

        #try:
            #response = self.port.read_until(b'\x02\x01')
            #print(self.port.inWaiting())
            #self.horizontalPosition = 255  - response[-4]
       #except:
            #print(self.port.inWaiting())
            #print("error recieving horizontal data")
        
    # Function 3: returns tuple xy position of touch
    def getTouchPosition(self):
        #grab horizontal and vertical touch position and put in tuple
        #self.getVerticalTouchPosition()
        #self.getHorizontalTouchPosition()
        response = []
        #self.port.write(self.getHorizontalPositionCommand)
        #self.port.write(self.getVerticalPositionCommand)
        self.port.write(bytearray([30]))
        response = self.port.read(3)
        if self.__echo:
            print((response[2], response[1]))
        else:
            pass
        self.verticalPosition = response[1] #self.touchCursorDimensions[1] - response[-14]
        self.horizontalPosition = response[2] #self.touchCursorDimensions[0] - response[-4]
    
        return (self.horizontalPosition, self.verticalPosition)
    
    def getTouchScreenDimensions(self):
        return (self.touchCursorDimensions, self.touchPinDisplayDimensions)
    
    def getTouchScreenFormat(self):
        #grab values for the format of the touchScreen
        nPinRows = self.touchPinDisplayDimensions[1]
        nPinColumns = self.touchPinDisplayDimensions[0]
        
        cursorXLength = self.touchCursorDimensions[0]
        cursorYLength = self.touchCursorDimensions[1]
        
        #calculate the x and y dimension position multiplier
        pinXMultiplier = nPinRows/cursorXLength
        pinYMultiplier = nPinColumns/cursorYLength
        
        return (pinXMultiplier, pinYMultiplier)
        
        
    def plotTouch(self):
        plt.plot(self.horizontalPosition,self.verticalPosition, 'ro')
        plt.axis([0, self.touchPinDisplayDimensions[1], 0, self.touchPinDimensions[0]])
        plt.show()
        