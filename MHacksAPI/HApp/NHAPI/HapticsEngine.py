# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 12:25:03 2020

@author: Derek Joslin
"""

import copy
import BoardCom as bc
import TouchScreenInterface as ts
import PeripheralManager as pm


class HapticsEngine(pm.PeripheralDevice):

    # Haptics Engine creates a COM port connection to the embedded processor.
    # HE maintains two primary arrays, currentState and desiredState. 
    #   - currentState is populated with the current emebedded state of dot matrix by using pull_currentState. 
    #   - desiredState is sent to the embedded processor using push_desiredState
    #   - return_currentState and return_desiredState prints the respective arrays for viewing

    #haptics engine can also contain a cursor

    def __init__(self, name, port = ''):
        
        super().__init__(name)
        
        #initialize a cursor position
        self.__pinCursorPosition = [0,0]
        self.__inputCursorPosition = [0,0]
        self.isLinkingCursor = False
        self.TouchScreenList = []
        self.TouchPosition = []
        
        #create default desired and current state
        self.__numRows = 19
        self.__numColumns = 41
        self.__currentState = [[False for i in range(0,self.__numColumns)] for j in range(0,self.__numRows)]
        self.__desiredState = [[False for i in range(0,self.__numColumns)] for j in range(0,self.__numRows)]
        
        self.debugString = "size: rows:{} columns:{}".format(self.__numRows, self.__numColumns)
        
        
        if port == '':
            self.__comLink = False
            self.__touchLink = False
        else:
            self.comLink_on(port,0)
            self.__touchLink = False
            self.pull_displaySize()
        
    def listResizer(self, listToResize, nColumns, nRows):
        #cutoff the columns
        for index,row in enumerate(listToResize):
            listToResize[index] = [False for i in range(0,nColumns)]
            
        #cutoff the rows
        if len(listToResize) > nRows:    
            listToResize[nRows:] = []
        elif len(listToResize) < nRows:
            while len(listToResize) < nRows:
                listToResize.append([False for i in range(0,nColumns)])
        else:
            pass
        
        return listToResize
        
         
    def pull_displaySize(self):
        """ grabs the number of rows and columns from the embedded processor and sets up currentState and desiredState arrays"""

        self.__numRows = int.from_bytes(self.com.get_numRows(),"big")
        self.__numColumns = int.from_bytes(self.com.get_numCols(),"big")
        self.debugString = "size: rows:{} columns:{}\n".format(self.__numRows, self.__numColumns)
        self.__currentState = self.listResizer(self.__currentState, self.__numColumns, self.__numRows)
        self.__desiredState = self.listResizer(self.__desiredState, self.__numColumns, self.__numRows)

    def display_matrix(self, matrix):
        """ displays the matrix in table view"""
        # print("num: {}".format(num))
        print('---------------------------\n')
        print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                         for row in matrix]))
        print('---------------------------\n')

    def return_displaySize(self):
        """ returns the current number of rows and columns """
        return (self.__numRows, self.__numColumns)


    def return_currentState(self):
        """ returns the current state of the chip """
        return self.__currentState
    
    
    def pull_currentState(self):
        """  grabs the current state from the emebdded side and stores it in currentState """
         
        matrix_state = self.com.get_matrix()
        state = []
        for byte in matrix_state:
            
            binary = list(bin(byte))
            del binary[0:2]
            binary = [int(i) for i in binary]
            
            while len(binary) != 8:
                binary.insert(0,0)
        
            binary = binary[::-1]
            
            state.append(binary)
        
        # del state[-1]
        
        matrix_state = []
        matrix_state.append([])
        
        columnIndex = 0
        rowIndex = 0
        
        for byte in state:
            
            if columnIndex > (self.__numColumns - 8):
                extensionNum = self.__numColumns - columnIndex
                matrix_state[rowIndex].extend(byte[0:extensionNum])
                #matrix_state[rowIndex].reverse()
                matrix_state.append([])
                columnIndex = 0
                rowIndex = rowIndex + 1
            else:
                matrix_state[rowIndex].extend(byte)
                columnIndex = columnIndex + 8
        
        matrix_state = [[bool(i) for i in row] for row in matrix_state]
        
        #reverese items inside list
        #matrix_state.reverse()
       
        #reverse each item inside the list using map function(Better than doing loops...)
        #matrix_state = list(map(lambda x: x[::-1], matrix_state))
        
        for rowIndex,row in enumerate(matrix_state):
            for elemIndex,elem in enumerate(row):
                self.__currentState[rowIndex][elemIndex] = copy.deepcopy(elem)

    def return_desiredState(self):
        """ returns the desired state of the dot matrix """
        return self.__desiredState

    def set_desiredState(self, newState):
        """ sets a desired state of the dot matrix """
        for rowIndex,row in enumerate(newState):
            for elemIndex,elem in enumerate(row):
                self.__desiredState[rowIndex][elemIndex] = copy.deepcopy(elem)
                
    def push_desiredState(self):
        """ sends the desired state of the dot matrix to the embedded side resulting in a refresh"""     
        #sendMatrix = np.array(self.__desiredState)
        #flipMatrix = np.fliplr(sendMatrix)
        
        #only refresh rows which need refresh
        rowIndex = 1
        for (desiredRowData,currentRowData) in zip(self.__desiredState,self.__currentState):
            #currentRowData.reverse()
            if desiredRowData != currentRowData:
                #programmatically flip data in currentRowData to desired
                currentRowData.clear()
                currentRowData.extend(desiredRowData)
                self.com.set_row(rowIndex,desiredRowData)
            rowIndex += 1  
        
    

    def comLink_on(self, COM, *args):
        """ creates connection to embedded side and initializes dot matrix size"""  
        if len(args) > 0:
            if args[0] == 1:
                onOff = 1
            else:
                onOff = 0
        else:
            onOff = 0
        
        self.com = bc.BoardCom(COM, onOff)
        self.pull_displaySize()
        self.__comLink = True

    def comLink_off(self):
        """ removes connection to embedded side """  
        self.__comLink = False
        self.com.close()
        del self.com

    def comLink_check(self):
        """ checks connection to embedded side """  
        return self.__comLink
    
    
    def setInputCursorPosition(self, position):
        self.__inputCursorPosition[0] = position[0]
        self.__inputCursorPosition[1] = position[1]
    
    
    def setPinCursorPosition(self, position):
        self.__pinCursorPosition[0] = position[0]
        self.__pinCursorPosition[1] = position[1]
        
    def setInputCursorPositionWithPinCursor(self):
        pinDimensions = self.getPinCursorDimensions()
        inputDimensions = self.getInputCursorDimensions()
        
        pinXPosition = self.__pinCursorPosition[0]
        pinYPosition = self.__pinCursorPosition[1]
        
        #Calculate the stepsize
        inputXStepSize = inputDimensions[0]/pinDimensions[0]
        inputYStepSize = inputDimensions[1]/pinDimensions[1]

        inputXPosition = inputXStepSize*pinXPosition
        inputYPosition = inputYStepSize*pinYPosition
        
        self.setInputCursorPosition((inputXPosition,inputYPosition))

        
    def setPinCursorPositionWithInputCursor(self):
        pinDimensions = self.getPinCursorDimensions()
        inputDimensions = self.getInputCursorDimensions()
        
        inputXPosition = self.__inputCursorPosition[0]
        inputYPosition = self.__inputCursorPosition[1]
        
        #Calculate the stepsize
        pinXStepSize = pinDimensions[0]/inputDimensions[0]
        pinYStepSize = pinDimensions[1]/inputDimensions[1]

        pinXPosition = int(pinXStepSize*inputXPosition)
        pinYPosition = int(pinYStepSize*inputYPosition)
        
        self.setPinCursorPosition((pinXPosition,pinYPosition))
        
        #print(self.grabPinCursor())
        
        
    def grabInputCursor(self):
        return self.__inputCursorPosition
    
    def grabPinCursor(self):
        return self.__pinCursorPosition
        
# =============================================================================
#     def getInputCursorPosition(self):
#         #somehow handles multiple touch screens
#         if self.__touchLink and self.__touchOn:
#             inputCursorDimensions = self.getInputCursorDimensions()
#             inputCursorXDimension = inputCursorDimensions[0]
#             inputCursorYDimension = inputCursorDimensions[1]
#             
#             oldVerticalPosition = self.touchScreen.verticalPosition
#             oldHorizontalPosition = self.touchScreen.horizontalPosition
#             newPosition = self.touchScreen.getTouchPosition()
#         
#             if newPosition[0] is oldHorizontalPosition and newPosition[1] is oldVerticalPosition:
#                 return self.__inputCursorPosition
#             else:
#                  #convert from touch screen size to haptic engine size and set new cursor position
#                  X = newPosition[1]
#                  Y = newPosition[0]
#                  
#                  self.setInputCursorPosition((X,Y))
#                  self.setPinCursorPositionWithInputCursor()
# 
#                  return self.__inputCursorPosition
#         else:
#             return self.__inputCursorPosition
#     
#     def getPinCursorPosition(self):
#         #handles the position of the cursor in pin space
#         
#         if self.__touchLink and self.__touchOn:
#             pinCursorDimensions = self.getPinCursorDimensions()
#             pinCursorXDimension = pinCursorDimensions[0]
#             pinCursorYDimension = pinCursorDimensions[1]
#             
#             oldVerticalPosition = self.__pinCursorPosition[0]
#             oldHorizontalPosition = self.__pinCursorPosition[1]
#             newPosition = self.touchScreen.getTouchPosition()
#         
#             if newPosition[0] is oldHorizontalPosition and newPosition[1] is oldVerticalPosition:
#                 return self.__pinCursorPosition
#             else:
#                  formatMultiplier = self.touchScreen.getTouchScreenFormat()
#                  #convert from touch screen size to haptic engine size and set new cursor position
#                  X = int(newPosition[0]*formatMultiplier[0])
#                  Y = int(newPosition[1]*formatMultiplier[1])
#                  
#                  self.setPinCursorPosition((X,Y))
#                  return self.__pinCursorPosition
#         else:
#             return self.__pinCursorPosition
# =============================================================================
            
        
    def getInputCursorDimensions(self):
        width = 0
        height = 0
        for Touchscreen in self.TouchScreenList:
            tDimensions = Touchscreen.getTouchScreenDimensions()
            # grab the input dimensions not the pin
            tDimensions = tDimensions[0]
            width += tDimensions[0]
            height = tDimensions[1]
            
        touchScreenCursorDimensions = (width, height)

        """
        if self.__touchLink:
            touchScreenDimnsions = self.touchScreen.getTouchScreenDimensions()
            touchScreenCursorDimensions = touchScreenDimnsions[0]
        else:
            touchScreenCursorDimensions = (255,255)
        """

        return touchScreenCursorDimensions
    
    def getPinCursorDimensions(self):
        pinHeight = self.__numRows
        pinWidth = self.__numColumns
        
        return (pinWidth, pinHeight)
    
    """ cycle through multiple Touchscreens and returns the position if the touch position has changed """
       
    def getTouchScreenPosition(self):
        for i, Touchscreen in enumerate(self.TouchScreenList):
            oldPosition = Touchscreen.getOldPosition()
            newPosition = Touchscreen.getTouchPosition()
            if oldPosition != newPosition:
                newPosition[0] += Touchscreen.touchCursorDimensions[0]*i
                self.setInputCursorPosition(newPosition)
                return self.grabInputCursor()
        
        return self.grabInputCursor()
        
       
    def connectTouchScreen(self, name, COM):
       self.TouchScreenList.append(ts.TouchScreenInterface(name, COM, 0))
       self.__touchLink = True
       self.__touchOn = True
       position = self.TouchScreenList[-1].getTouchPosition()
       self.setInputCursorPosition(position)
       
    def turnOffTouchScreen(self):
       self.__touchOn = False
       
    def turnOnTouchScreen(self):
       self.__touchOn = True
       
    def disconnectTouchScreen(self):
       if self.__touchLink:
          self.touchScreen.close()
          self.__touchOn = False
          self.__touchLink = False
   
    def checkTouchLink(self):
        return self.__touchLink
    
       
    
    
