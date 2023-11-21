# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 11:09:02 2022

@author: Derek Joslin
"""

import serial
import PeripheralManager as pm

class TouchScreenInterface(pm.PeripheralDevice):
    
     # the touch screen interface object contains a serial port connection object and commands to communicate with hardware

    def __init__(self, name, port, *args):
        super().__init__(name)
        
        # 115200 for the embedded board
        self.port = serial.Serial(port, 115200, timeout=3)
                
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
        self.horizontalPosition = 0
        self.verticalPosition = 0
        
        # create the debug text from the device specifications
        self.debugInputDimensionString = "Input Dimensions xLength:{} yLength:{}\n".format(255,255)
        self.debugPinDimensionString = "Pin Dimensions rows:{} columns:{}\n".format(19,20)
        
        getVerticalPositionCommand   = [1, 2, 3, 0, 2, 3, 0, 3, 2, 1]
        getHorizontalPositionCommand   = [1, 2, 3, 0, 2, 2, 0, 3, 2, 1]
        self.getVerticalPositionCommand = bytearray(getVerticalPositionCommand)
        self.getHorizontalPositionCommand = bytearray(getHorizontalPositionCommand)
        self.verticalPosition = self.getVerticalTouchPosition()
        self.horizontalPosition = self.getHorizontalTouchPosition()


    def createDebugString(self):
        self.debugString = self.debugInputDimensionString + self.debugPinDimensionString + self.debugPositionString
        
        
    # sets the echo of the com port onOff (0=Off, 1=On)
    def echo(self, onOff):
        if onOff:
            self.__echo = 1
        else:
            self.__echo = 0
    
    # opens the serial port
    def open(self):
        self.port.open()
        self.__readSerialResponse()

    # closes the serial port
    def close(self):
        self.port.close()

    # if echo is on prints the recieve data
    def __print_rx(self):
        read = self.__read_rx()
        if self.__echo:
            print(read)
        else:
            pass
        
    # reads in data on the serial line
    def __read_rx(self):
        # self.port.flush()
        self.__recieveBuffer = self.port.read(1)
        return self.__recieveBuffer #.decode('utf-8')
    
    # reads one byte and prints based on echo state
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
        
        
        # self.port.flush()
        # print(self.port.inWaiting())
        # select the get vertical position command
        self.port.write(self.getVerticalPositionCommand)

        response = self.port.read(10)
        self.verticalPosition = self.touchCursorDimensions[1]  - response[-4]
        
        # create position debug
        self.debugPositionString = "Input position xCoordinate:{} yCoordinate:{}\n".format(self.horizontalPosition, self.verticalPosition)
        self.createDebugString()
        
        # try:
            # response = self.port.read_until(b'\x02\x01')
            # print(self.port.inWaiting())
            # self.verticalPosition = 255 - response[-4]
        # except:
           # print(self.port.inWaiting())
           # print("error recieving vertical data")
        
    # Function 2: gets the horizontal position
    def getHorizontalTouchPosition(self):
        # create list with required parameters
        # getHorizontalPositionCommand   = [1, 2, 3, 0, 2, 2, 0, 3, 2, 1]
        # output = getHorizontalPositionCommand
        response = []

        # self.port.flush()
        # print(self.port.inWaiting())
        # select the get horizontal position command
        self.port.write(self.getHorizontalPositionCommand)

        response = self.port.read(10)
        
        self.horizontalPosition = self.touchCursorDimensions[0]  - response[-4]
        
        # create position debug
        self.debugPositionString = "Input position xCoordinate:{} yCoordinate:{}\n".format(self.horizontalPosition, self.verticalPosition)
        self.createDebugString()

        # try:
            # response = self.port.read_until(b'\x02\x01')
            # print(self.port.inWaiting())
            # self.horizontalPosition = 255  - response[-4]
       # except:
            # print(self.port.inWaiting())
            # print("error recieving horizontal data")
        
    # Function 3: returns tuple xy position of touch
    def getTouchPosition(self):
        # grab horizontal and vertical touch position and put in tuple
        # self.getVerticalTouchPosition()
        # self.getHorizontalTouchPosition()
        response = []
        self.port.write(self.getHorizontalPositionCommand)
        self.port.write(self.getVerticalPositionCommand)
        response = self.port.read(20)
        if self.__echo:
            print((response[-4], response[-14]))
        else:
            pass
        self.verticalPosition = self.touchCursorDimensions[1] - response[-14]
        self.horizontalPosition = self.touchCursorDimensions[0] - response[-4]
    
        # create position debug
        self.debugPositionString = "Input position xCoordinate:{} yCoordinate:{}\n".format(self.horizontalPosition, self.verticalPosition)
        self.createDebugString()
    
        return [self.verticalPosition, self.horizontalPosition]
    
    def getTouchScreenDimensions(self):
        return (self.touchCursorDimensions, self.touchPinDisplayDimensions)
    
    def getOldPosition(self):
        return [self.verticalPosition, self.horizontalPosition]
    
    def getTouchScreenFormat(self):
        # grab values for the format of the touchScreen
        nPinRows = self.touchPinDisplayDimensions[1]
        nPinColumns = self.touchPinDisplayDimensions[0]
        
        cursorXLength = self.touchCursorDimensions[0]
        cursorYLength = self.touchCursorDimensions[1]
        
        # calculate the x and y dimension position multiplier
        pinXMultiplier = nPinRows/cursorXLength
        pinYMultiplier = nPinColumns/cursorYLength
        
        return (pinXMultiplier, pinYMultiplier)
        
        
# =============================================================================
#     def plotTouch(self):
#         plt.plot(self.horizontalPosition,self.verticalPosition, 'ro')
#         plt.axis([0, self.touchPinDisplayDimensions[1], 0, self.touchPinDimensions[0]])
#         plt.show()
# =============================================================================
        