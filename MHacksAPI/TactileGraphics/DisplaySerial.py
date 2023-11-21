# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 11:39:32 2020

@author: Derek Joslin

"""

# =============================================================================
# This class is the software driver for the 
# serialCommunication library section of the
# firmware code. 
# It currently runs with the HapticsEngineFirmware
# but in the future will also communicate
# with the software module
# example code at the bottom
# =============================================================================

import serial
from SerialErrorCodes import *
import time

class DisplaySerial(serial.Serial):

    def __init__(self, *args):
        try:
            # if there is more than a single arguement intialize with baudrate
            if len(args) > 1:
                super().__init__(args[0], args[1], timeout=args[2])
            else:
                # default baudrate is 115200
                super().__init__(args[0], 115200, timeout=3)
        except Exception as e:
            if e is ValueError:
                raise ValueError(f"""{args} is an incorrect arguement.
                      To create DisplaySerial parameters should be 
                      comportString, baudrate, timeout
                      default is "[yourComportString]", 115200, 3""")
# =============================================================================
#             if e is serial.SerialException:
#                 raise serial.SerialException(f"""Have you tried plugging in the display, dingus?""")
# =============================================================================

        # 2 second delay for nano connection
        time.sleep(2)
        
        # write a 255 to the device in order to confirm the connection ie handshake
        self.write(bytearray([255]))
        
        # read the confirmation byte
        confirmByte = self.read(1)

        # check if the response byte exists
        if len(confirmByte):
            pass
        else: 
            raise IOError(f"{SERIAL_NO_CONFIRMBYTE_RESPONSE_ERROR}")
        
        # there is a confirmation bit to read to ensure the connection occured
        if confirmByte[0] == 255:
            pass
        else:
            raise IOError(f"{SERIAL_INCORRECT_CONFIRMBYTE_RESPONSE_ERROR}")
        
        # create command history
        self._commandHistory = []
        
        # create a dirty flag to keep track of if a new command has been recieved 
        self._isDirty = False
        
        # IMPORTANT: add commands to this list
        # create a dictionary to hold the names of all the serial commands 
        self._commands = {
            1: self.setRow,
            2: self.forceClearAll,
            3: self.getMatrix,
            5: self.setAllValvesOff,
            6: self.setSourceValvesOn,
            10: self.getNRows,
            11: self.getNColumns,
            12: self.getNBytesPerRow,
            13: self.setRefreshParameters,
            14: self.getRefreshParameters,
            15: self.getRowValveArray,
            16: self.setRowValveArrayAssignment,
            17: self.getColumnValveArray,
            18: self.setColumnValveArrayAssignment,
            19: self.setRowValveStateArray,
            20: self.setColumnValveStateArray,
            21: self.setRefreshMatrix,
            23: self.getNBytesPerColumn,
            29: self.readAnalogIndex,
            32: self.setValveStateArray,
            35: self.setSolenoidDriver,
            36: self.getSolenoidDriver,
            37: self.setRefreshStateParameters,
            38: self.getRefreshStateParameters,
            39: self.setSource,
            40: self.readAnalog,
            41: self.readButtonMatrix,
            42: self.setSolenoidDriverProtocols,
            43: self.getSolenoidDriverProtocols,
            44: self.setRefreshMatrixProtocols,
            45: self.getRefreshMatrixProtocols,
            46: self.getSolenoidDriverState,
            47: self.getRefreshMatrixState
            }
        
        # create a variable to keep track of the current command
        self._currentCommand = None

    @property
    def isDirty(self):
        return self._isDirty

    @property
    def commandHistory(self):
        self._isDirty = False
        return self._commandHistory
        
    @property
    def currentCommand(self):
        return self._currentCommand
    
    @property
    def commands(self):
        return self._commands
    
    @commands.setter
    def my_dict(self, commandFunctionPair):
        commandByte, serialFunction = commandFunctionPair
        
        if not (0 <= commandByte <= 255):
            raise TypeError("The commandByte must be between 0 and 255")
            
        if not callable(serialFunction):
            raise TypeError("The serialFunction must be a function handle")
            
        self._commands[commandByte] = serialFunction

    def __setitem__(self, commandByte, serialFunction):
        if not (0 <= commandByte <= 255):
            raise TypeError("The commandByte must be between 0 and 255")
            
        if not callable(serialFunction):
            raise TypeError("The serialFunction must be a function handle")

        self._commands[commandByte] = serialFunction

    def __getitem__(self, commandByte):
        if not (0 <= commandByte <= 255):
            raise TypeError("The commandByte must be between 0 and 255")
            
        return self._commands[commandByte]
    
    def sendCommand(self, commandByte):
        # select the current command byte
        self._currentCommand = commandByte
        
        # write the command byte to the serial port
        self.write(bytearray([self._currentCommand]))
        
        # mark the command history as dirty
        self._isDirty = True
        
    def clearBuffer(self):
        bufferDump = []
        while self.in_waiting > 0:
            bufferDump.append(self.read(1)[0])
            
        return bufferDump
    
    def createByteList(self, inputList):
        lengthOfByte = 8
        
        # Pad the data so that all of the row data can fit into a multiple of 8 bits
        padList = inputList + [0] * lengthOfByte
        
        # Create a list with each element as a byte representing 8 bits of data in the rowData
        byteList = [padList[n:n+lengthOfByte] for n in range(0, len(padList), lengthOfByte)]
        
        return byteList[:-1]
    
    def condenseByteList(self, inputList, bitOrder):
        outputList = []
        for byte in inputList:
            if bitOrder == 'msb':
                msbString = '0b' +''.join(map(str, byte))
                outputList.append(int(msbString, base=2))

            if bitOrder == 'lsb':
                lsbString = '0b' + ''.join(reversed(msbString))
                outputList.append(int(lsbString, base=2))
            
        return outputList
    
    # TODO: Move this to the tactile display class
    # internal helper function to quickly aquire important values
    def getSize(self):
        self.nRows = self.getNRows()
        self.nColumns = self.getNColumns()
        self.nBytesPerRow = self.getNBytesPerRow()
        self.nBytesPerColumn = self.getNBytesPerColumn()

# =============================================================================
#     start of the serial communication interface functions
# =============================================================================

    # Function 1: Sets state of a row on the chip
    def setRow(self, rowIndex, rowData):
        # run function error handler
        self._setRowErrorHandler(rowIndex, rowData)
        
        # send function command
        self.sendCommand(1)

        # create an output buffer
        outputBuffer = []
        outputBuffer.append(rowIndex)
        
        # split the rowData into lists of binary which form bytes
        byteList = self.createByteList(rowData)
        
        # condense those bytes into integers
        intByteList = self.condenseByteList(byteList,'msb')

        # add them to the output buffer
        outputBuffer.extend(intByteList)

        # send as bytearray with each parameter as a byte
        self.write(bytearray(outputBuffer))

        responseList = self.receiveCommandResponse(0)

    # error handler
    def _setRowErrorHandler(self, rowIndex, rowData):
        if not isinstance(rowIndex, int) and isinstance(rowData,list):
            raise TypeError(f"""input to setRow has the incorrect
                             data type should be int and list
                             rowIndex: {rowIndex}
                             rowData: {rowData}""")
         
        # check that every element in rowData is an int
        for byte in rowData:
            if not isinstance(byte, int):
                raise ValueError("rowData for setRow must contain only integer elements")
            if byte > 1:
                raise ValueError(f"dot values on the tactile display must be set to either a 1 or 0. {rowData}")

    # Function 2: Sets display matrix to all 0s and turns all electronic valves OFF
    def forceClearAll(self):
        self.sendCommand(2)

        responseList = self.receiveCommandResponse(1)

        #print the recieved bit
        return responseList[0]

    # Function 3: Returns the current state of the matrix
    def getMatrix(self):
        self.sendCommand(3)
        nMatrixBytes = self.nBytesPerRow * self.nRows

        return self.receiveCommandResponse(nMatrixBytes)

    # Function 5: Turns all electronic valves OFF
    def setAllValvesOff(self):
      self.sendCommand(5)

      self.receiveCommandResponse(0)

    # Function 6: Turns source pressure ON
    def setSourceValvesOn(self):
      self.sendCommand(6)

      self.receiveCommandResponse(0)


    # Function 10: Returns number of rows of dot matrix
    def getNRows(self):
        #send the function 10 command
        self.sendCommand(10)

        responseList = self.receiveCommandResponse(1)

        return responseList[0]

    # Function 11: Returns number of columns of dot matrix
    def getNColumns(self):
        #send the function 11 command
        self.sendCommand(11)

        responseList = self.receiveCommandResponse(1)

        return responseList[0]

    # Function 12: Returns number of bytes to expect per row of the matrix.
    def getNBytesPerRow(self):
        #send the function 12 command
        self.sendCommand(12)

        responseList = self.receiveCommandResponse(1)

        return responseList[0]

    # Function 13: Update setup, hold, and pulse width
    def setRefreshParameters(self, settingArray):
        self.sendCommand(13)

        self.write(bytearray(self.intToByte(settingArray)))

        self.receiveCommandResponse(0)

    # Function 14: get the setup, hold, and pulse width
    def getRefreshParameters(self):
        self.sendCommand(14)

        responseList = self.receiveCommandResponse(6)

        newList = self.byteToInt(responseList)
        return newList

    # Function 15: Gets the RowValveArray
    def getRowValveArray(self):
        self.sendCommand(15)

        responseList = self.receiveCommandResponse(self.nRows)

        return responseList

    # Function 16: Sets the state of elements in rowValveArray
    def setRowValveArrayAssignment(self, rowValveArray):
        self.sendCommand(16)

        self.write(bytearray(rowValveArray))

        self.receiveCommandResponse(0)

    # Function 17: Gets the Column valve array assignments
    def getColumnValveArray(self):
        # send the function 17 command
        self.sendCommand(17)

        responseList = self.receiveCommandResponse(self.nColumns)

        return responseList

    # Function 18: Sets the start of elements in columnValveArray
    def setColumnValveArrayAssignment(self, columnValveArray):
        self.sendCommand(18)

        self.write(bytearray(columnValveArray))

        self.receiveCommandResponse(0)

    # Function 19: Sets the state of all valves in a row
    def setRowValveStateArray(self, valveStateArray):
        # send the function 19 command
        self.sendCommand(19)

        self.write(bytearray(valveStateArray))

        self.receiveCommandResponse(0)

    # Function 20: Sets the state of all valves in a column
    def setColumnValveStateArray(self, valveStateArray):
        self.sendCommand(20)

        self.write(bytearray(valveStateArray))

        self.receiveCommandResponse(0)

    # Function 21: turns off the refresh matrix
    def setRefreshMatrix(self, onOff):
        self.sendCommand(21)

        self.write(bytearray([onOff]))

        self.receiveCommandResponse(0)

    # Function 23: Gets the number of bytes in a column
    def getNBytesPerColumn(self):
        # send the function 23 command
        self.sendCommand(23)

        responseList = self.receiveCommandResponse(1)

        return responseList[0]
    
    # Function 29:  Returns the analog reading at the specified index
    def readAnalogIndex(self, index):
        self.sendCommand(29)
        
        self.write(bytearray([index]))

        responseList = self.receiveCommandResponse(2)

        newList = self.byteToInt(responseList)
        return newList

    # Function 32: Sets the state of all valves in a column
    def setValveStateArray(self, valveStateArray):
        self.sendCommand(32)

        self.write(bytearray(valveStateArray))

        self.receiveCommandResponse(0)

    # Function 35: sets the parameters relating to driving the solenoids
    def setSolenoidDriver(self, settingArray):
        self.sendCommand(35)

        self.write(bytearray(self.intToByte(settingArray)))

        self.receiveCommandResponse(0)

    # Function 36: retieves the current value of parameters related to driving solenoids
    def getSolenoidDriver(self):
        self.sendCommand(36)

        responseList = self.receiveCommandResponse(8)

        newList = self.byteToInt(responseList)
        return newList

    # Function 37: sets the Refresh Matrix parementers dealing with the state
    def setRefreshStateParameters(self, settingArray):
        self.sendCommand(37)

        self.write(bytearray(self.intToByte(settingArray)))

        self.receiveCommandResponse(0)

    # Function 38: get the the Refresh matrix parameters dealing with the state
    def getRefreshStateParameters(self):
        self.sendCommand(38)

        responseList = self.receiveCommandResponse(10)

        newList = self.byteToInt(responseList)
        return newList

    # Function 39: set Source based on a 1 or 0
    def setSource(self, onOff):
        self.sendCommand(39)

        self.write(bytearray([onOff]))

        self.receiveCommandResponse(0)

    # Function 40: Returns the analog readings of the arduino
    def readAnalog(self):
        self.sendCommand(40)
        
        responseList = self.receiveCommandResponse(10)

        newList = self.byteToInt(responseList)
        return newList
    
    # Function 41: Returns the byte value of all the button inputs for the button matrix
    def readButtonMatrix(self):
        self.sendCommand(41)
        
        responseList = self.receiveCommandResponse(4)

        return responseList

    # Function 42: Sets the solenoid Driver protocol Parameters
    def setSolenoidDriverProtocols(self, protocolSettingList):
        self.sendCommand(42)

        self.write(bytearray(protocolSettingList))

        self.receiveCommandResponse(0)

    # Function 43: gets which solenoid driver protocols are active
    def getSolenoidDriverProtocols(self):
        self.sendCommand(43)
        
        responseList = self.receiveCommandResponse(1)
        
        return responseList
        
    # Function 44: sets the RefreshMatrix Protocols
    def setRefreshMatrixProtocols(self, protocolSettingList):
        self.sendCommand(44)
        
        self.write(bytearray(protocolSettingList))
        
        self.receiveCommandResponse(0)
    
    # Function 45: gets which refresh matrix protocols are active
    def getRefreshMatrixProtocols(self):
        self.sendCommand(45)
        
        responseList = self.receiveCommandResponse(4)
        
        return responseList
    
    # Function 46: gets the current state of the Solenoid Driver State machine
    def getSolenoidDriverState(self):
        self.sendCommand(46)
        
        responseList = self.receiveCommandResponse(3)
        
        return responseList
    
    # Function 47: gets the current state of the refresh matrix State machine
    def getRefreshMatrixState(self):
        self.sendCommand(47)
        
        responseList = self.receiveCommandResponse(3)
        
        return responseList
    
    def receiveCommandResponse(self, responseBytes):

        if responseBytes > 0:
            responseList = []

            response = self.read(responseBytes)

            for byte in response:
                responseList.append(byte)

        else:
            responseList = None

        # read the confirm byte
        confirmByte = int.from_bytes(self.read(1), byteorder='big', signed=False)

        # raise an error if the confirmByte is not equal to the commandByte
        if confirmByte != self.currentCommand:
            raise IOError(f""" The confirm byte sent from the device ({confirmByte})
                          is not equal to the expected Confirm Byte {self.currentCommand} 
                          ({self._commands[self.currentCommand].__name__})""")
            
        # add the command history to the list
        self._commandHistory.append((confirmByte, responseList))
        
        # reset the current command
        self._currentCommand = None
        
        return responseList

    def intToByte(self, intList):

        # Convert list of uint16s to list of uint8s
        byteList = []
        for value in intList:
            lowerByte = value & 0xFF
            upperByte = (value >> 8) & 0xFF
            byteList.append(lowerByte)
            byteList.append(upperByte)

        return byteList

    def byteToInt(self, byteList):
        # Convert list of uint8s to list of uint16s
        intList = []
        for i in range(0, len(byteList), 2):
            lowerByte = byteList[i]
            upperByte = byteList[i + 1]
            uint16Value = (upperByte << 8) | lowerByte
            intList.append(uint16Value)
        # Displaying the results
        return intList


if __name__ == "__main__":

    # Create a DisplaySerial object with a specified COM port and baud rate
    displaySerial = DisplaySerial("COM11", 115200, 3)
    
    # Get and set display parameters
    displaySerial.getSize()
    
    # display each parameter
    nRows = displaySerial.getNRows()
    nColumns = displaySerial.getNColumns()
    nBytesPerRow = displaySerial.getNBytesPerRow()
    nBytesPerColumn = displaySerial.getNBytesPerColumn()

    # Set a row with sample data (you would replace the second parameter with your actual data)
    displaySerial.setRow(1, [0,1,0,1,0,1,0,1])

    # Clear all and get the matrix state
    displaySerial.forceClearAll()
    matrixState = displaySerial.getMatrix()

    # Work with valve arrays
    displaySerial.setAllValvesOff()
    displaySerial.setSourceValvesOn()
    rowValveArray = displaySerial.getRowValveArray()
    displaySerial.setRowValveArrayAssignment([1]*nRows)
    columnValveArray = displaySerial.getColumnValveArray()
    displaySerial.setColumnValveArrayAssignment([1]*nColumns)

    # Set and get refresh parameters
    displaySerial.setRefreshParameters([100, 100, 100])
    refreshParameters = displaySerial.getRefreshParameters()

    # Set and get solenoid driver settings
    displaySerial.setSolenoidDriver([100, 100, 100, 100])
    solenoidDriverSettings = displaySerial.getSolenoidDriver()

    # Set and get refresh state parameters
    displaySerial.setRefreshStateParameters([1, 2, 3, 4, 5])
    refreshStateParameters = displaySerial.getRefreshStateParameters()

    # Set and get various states and parameters
    displaySerial.setRefreshMatrix(1)
    displaySerial.setSource(1)
    displaySerial.setValveStateArray([1, 0, 1, 0])
    displaySerial.setRowValveStateArray([1, 0, 1, 0])
    displaySerial.setColumnValveStateArray([1, 0, 1, 0])

    # Read analog indices and values
    analogIndexValue = displaySerial.readAnalogIndex(0)
    analogValues = displaySerial.readAnalog()

    # Read button matrix
    buttonMatrixValues = displaySerial.readButtonMatrix()

    # Set and get solenoid driver and refresh matrix protocols
    displaySerial.setSolenoidDriverProtocols([1, 1, 1, 1])
    solenoidDriverProtocols = displaySerial.getSolenoidDriverProtocols()
    displaySerial.setRefreshMatrixProtocols([1, 1, 1, 1])
    refreshMatrixProtocols = displaySerial.getRefreshMatrixProtocols()

    # Get the current state of the Solenoid Driver and Refresh Matrix state machines
    solenoidDriverState = displaySerial.getSolenoidDriverState()
    refreshMatrixState = displaySerial.getRefreshMatrixState()

    # Print the results of some of the function calls to check the results
    print("Number of rows: ", nRows)
    print("Matrix state: ", matrixState)
    print("Refresh parameters: ", refreshParameters)
    print("Solenoid driver settings: ", solenoidDriverSettings)
    print("Refresh state parameters: ", refreshStateParameters)
    print("Analog index value: ", analogIndexValue)
    print("Analog values: ", analogValues)
    print("Button matrix values: ", buttonMatrixValues)
    print("Solenoid driver protocols: ", solenoidDriverProtocols)
    print("Refresh matrix protocols: ", refreshMatrixProtocols)
    print("Solenoid driver state: ", solenoidDriverState)
    print("Refresh matrix state: ", refreshMatrixState)
