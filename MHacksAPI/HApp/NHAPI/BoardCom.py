# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 11:39:32 2020

@author: Derek Joslin
"""

import serial
import time

class BoardCom:
    
     #the Board Com object contains a serial port connection object and commands to communicate with hardware

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
        self.__recieveBuffer = self.port.read_until(b'\xFF')
        
        if self.__echo:
            print(self.__recieveBuffer)
        else:
            pass

        self.numRows = self.get_numRows()
        self.numCols = self.get_numCols()
        self.numBytesPerRow = self.get_numBytesPerRow()

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
        # self.port.flushInput()
        self.__recieveBuffer = self.port.read(1)
        return self.__recieveBuffer #.decode('utf-8')
    
    #reads one byte and prints based on echo state
    def __readSerialResponse(self):
        read = self.port.read(1)
        if self.__echo:
            print(read)
        else:
            pass

    
    # Function 1: Sets state of a row on the chip
    def set_row(self, rowIndex, rowData):
        #create list with required parameters
        output = []
        
        #select the set Row Function (1)
        output.append(1)
        self.port.write(bytearray(output))
        
        output = []
        
        #add the row index to the list
        output.append(rowIndex-1) #accomodate 0 index on embedded size
        
        #take list of rowData and add it to the list, but concatenated with 8 elements as a byte
        row = list(map(int, rowData))
        fill = 0
        N = 8
        tempList = row + [fill] * N
        subList = [tempList[n:n+N] for n in range(0, len(row), N)]
        
        for lst in subList:
            s = '0b' + ''.join(map(str, lst))
            output.append(int(s, base=2))
        
        #send as bytearray with each parameter as a byte
        response = self.port.write(bytearray(output))
        #time.sleep(0.015)
        
        #print the recieved bit if echo is on
        self.__readSerialResponse()
        
    # Function 2: Sets display matrix to all 0s and turns all electronic valves OFF    
    def forceClearAll(self):
        #create list of bytes to send
        output = []
        
        #select the second function
        output.append(2)
        
        #send the byte array
        self.port.write(bytearray(output))
        
        #print the recieved bit
        self.__readSerialResponse()

    # Function 3: Returns the current state of the matrix
    def get_matrix(self):
        
        #flush the port
        self.port.flushInput()
        
        #create list of bytes to be sent
        output = []
        #select function 3
        output.append(3)
        
        
        #send the command
        self.port.write(bytearray(output))
        #time.sleep(0.03)
        

            
            
            
        
        #read the current matrix state
        # self.port.flushInput()

        # self.__recieveBuffer = self.port.read_until(b'\x03')
        N = int.from_bytes(self.numBytesPerRow,"big") * int.from_bytes(self.numRows,"big")
        self.__recieveBuffer = self.port.read(N)
        
        
        if self.__echo:
            print(self.__recieveBuffer)
        else:
            pass

        self.__readSerialResponse() # Alex: read final byte reporting function number
        
        #print(self.__recieveBuffer)
        #return the recieve buffer
        return self.__recieveBuffer    
        
    # Function 4: Returns 1 if matrix is in the process of refreshing, 0 if done refreshing.        
    def is_idle(self):
        #create list to be the output
        output = []
        
        #select the fourth function
        output.append(4)
        
        #send the byte
        self.port.write(bytearray(output))
        
        #read whether the device is idle
        # self.__recieveBuffer = self.port.read_until(b'\x0b')
        self.__recieveBuffer_value = self.port.read(1)

        #read the output on the serial port
        self.__readSerialResponse()

        return self.__recieveBuffer_value
        
    # Function 5: Turns all electronic valves OFF    
    def turn_off(self):
        #create the list for output
        output = []
        
        #select the fifth function
        output.append(5)
        
        #send the byte
        self.port.write(bytearray(output))
        
        #read the output on the serial port
        self.__readSerialResponse()
        
    # Function 6: Turns source pressure ON
    def turn_on(self):
        #create a list for the output
        output = []
        
        #select the sixth function
        output.append(6)
        
        #send the command
        self.port.write(bytearray(output))
        
        
        
        #read the output on the serial port
        self.__readSerialResponse()
        
        
        
        # Function 7: Sets value of matrix to desired state. Input is m x n array, where m = numRows and n=numCols of matrix.
    def set_matrix(self, mat):
        
        #create a list for the output
        output = []
        
        #flush the port
        self.port.flushInput()
        
        #select the first function as set matrix is implementing set row
        #output.append(1)
        
        #response = self.port.write(bytearray(output))
         
        #take list of rows and create byte arrays out of each row
        rowIndex = 1
        for rowData in mat:    
            self.set_row(rowIndex,rowData)
            rowIndex += 1            
            
            
        test = 1
    
    # Function 7: Sets value of matrix to desired state. Input is m x n array, where m = numRows and n=numCols of matrix.
    def setMatrix(self, mat):
        #create a list for the output
        output = []
        
        #select the seventh function
        output.append(7)
        
        #flush the port
        self.port.flushInput()
        
        #take list of rows and create byte arrays out of each row
        fill = 0
        N = 8
        for rowData in mat:
            row = list(map(int, rowData))[::-1]
            tempList = row + [fill] * N
            subList = [tempList[n:n+N] for n in range(0, len(row), N)]
            for lst in subList:
                s = '0b' + ''.join(map(str, lst))
                output.append(int(s, base=2))
    
        #send the command
        #n = len(output)
        test = self.port.write(bytearray(output))
        #self.port.write(bytearray(output[0:n/2]))
        
        #self.port.write(bytearray(output[n/2:n-1]))
        
        #read the output on the serial port
        self.__readSerialResponse()
        
    # Function 8: Sets state of single dot. Inputs: (row_index=1:num_rows, col_index=1:num_cols, state=0,1)  
    def set_dot(self, rowIndex, colIndex, data):
        #create output list
        output = []
        
        #select the eighth function
        output.append(8)
        
        #add the row index column index and state
        output.append(rowIndex-1) # accomodate 0 index shift
        output.append(colIndex-1) # accomodate 0 index shift
        output.append(data)
        
        #send the command
        self.port.write(bytearray(output))
        
        #read the output on the serial port
        self.__readSerialResponse()
        
    # Function 9: Sets state of all dots ON or OFF. Input: (state=0,1)    
    def set_all(self, data):
        #create output list
        output = []
        
        #select function
        output.append(9)
        
        #add the desired data for the state to be set to
        output.append(data)
        
        #send the command
        self.port.write(bytearray(output))
        
        #read the output on the serial port
        self.__readSerialResponse()
    
    # Function 10: Returns number of rows of dot matrix
    def get_numRows(self):
        #create output list
        output = []
        
        #select function
        output.append(10)
        
        #send the command
        self.port.write(bytearray(output))
        #time.sleep(0.003)


        self.__recieveBuffer = self.port.read(1)

        self.__readSerialResponse()

        return self.__recieveBuffer
        
    # Function 11: Returns number of columns of dot matrix
    def get_numCols(self):
        #create output list
        output = []
        
        #select function
        output.append(11)
        
        #send the command
        self.port.write(bytearray(output))
        #time.sleep(0.002)
        
        #receive the data
        self.__recieveBuffer = self.port.read(1)

        #read serial function identification response      
        self.__readSerialResponse()

        return self.__recieveBuffer

    # Function 12: Returns number of bytes to expect per row of the matrix. 
    def get_numBytesPerRow(self):
        #create output list
        output = []
        
        #select function
        output.append(12)
        
        #send the command
        self.port.write(bytearray(output))
        #time.sleep(0.002)
        
        #receive the data
        self.__recieveBuffer = self.port.read(1)

        #read serial function identification response      
        self.__readSerialResponse()

        return self.__recieveBuffer