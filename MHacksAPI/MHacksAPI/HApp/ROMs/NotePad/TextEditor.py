# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 12:52:45 2022

@author: Derek Joslin
"""

import NotePadKeyboard as nk
import time


class TextEditor():

    def __init__(self, nDotRows, nDotColumns, HAppControlCenter):
        
        #add one as the last line doesn't count
        self.nBrailleCellColumns = int((nDotColumns + 1)/3)
        self.nBrailleCellRows = int((nDotRows + 1)/4)
        
        self.startTime = 0
        self.endTime = 0
        
        #bounding box contains indices of first and last list to display
        self.boundingBox = [0, self.nBrailleCellRows - 1]
        
        self.cursor = [0,0] #in cell format
        
        self.cursorLimiter = [[0,0]]
        
        self.inputCommand = ""
        
        #create cursor Limiters for every line
# =============================================================================
#         for iRow in range(0,self.nBrailleCellRows):
#             self.cursorLimiter.append([0,iRow])
#             if iRow > 0:
#                 limiter =  self.cursorLimiter[-1]
#                 limiter[0] = limiter[0] - 1
#                 self.cursorLimiter[-1] = limiter
#                 print(self.cursorLimiter[-1])
# =============================================================================

        self.editorString = ""
        self.editorMatrix = [[]]
        
        newLineList = []
        self.editorBox = []
        self.KeyboardHandles = nk.TextEditorKeyboardHandles(self, HAppControlCenter)

    def deleteCursorLimit(self, yPosition):
        limiter = self.cursorLimiter[yPosition]
        priorLimiter = self.cursorLimiter[yPosition - 1]
        limiterXLength = 0

        if limiter[0] > 0:
            #delete limit and add excess to previous limit
            limiterXLength = limiter[0]
            priorLimiter[0] += limiterXLength
            
            self.cursorLimiter[yPosition - 1] = priorLimiter
            
            for index,limiter in enumerate(self.cursorLimiter):
                if index > (yPosition):
                    limiter[1] -= 1
                    #print("limiter pushed down")
                    
            self.cursorLimiter.pop(yPosition)
            
        else:
            #termination case
            if yPosition == 0:
                #hit end of editor do nothing
                print("hit beginning of the editor")
            else:
                #delete the limiter
                #shuffle the rest of the cursor limits
                for index,limiter in enumerate(self.cursorLimiter):
                    if index > (yPosition):
                        limiter[1] -= 1
                        #print("limiter pushed down")
                self.cursorLimiter.pop(yPosition)

                #print("limiter deleted")
        
    def cursorLimiterCheck(self):
        #returns true or false depending on if you can move to that location
        xPosition = self.editor.cursor[0]
        yPosition = self.editor.cursor[1]
        limiter = self.cursorLimiter[yPosition]

    def resetCursorLimit(self, yPosition):
        #add a cursorLimiter at the current position
        limiter = self.cursorLimiter[yPosition]
        limiter[0] = 0
        self.cursorLimiter[yPosition] = limiter
        #print(self.cursorLimiter)

    def moveCursorLimitBackward(self, yPosition):
        limiter = self.cursorLimiter[yPosition]

        #determine if limit can be moved backwards
        if limiter[0] > 0:
            #move limit backwards
            limiter[0] -= 1
            self.cursorLimiter[yPosition] = limiter
            #print(self.cursorLimiter)
        else:
            #termination case
            if yPosition == 0:
                #hit end of editor do nothing
                print("hit beginning of the editor")
            else:
                #delete the limiter
                #shuffle the rest of the cursor limits
                for index,limiter in enumerate(self.cursorLimiter):
                    if index > (yPosition):
                        limiter[1] -= 1
                       # print("limiter pushed down")
                self.cursorLimiter.pop(yPosition)

                #print("limiter deleted")
        
        #print(self.cursorLimiter)

    def moveCursorLimitForward(self, yPosition):
        limiter = self.cursorLimiter[yPosition]
        
        #determine if limit can be moved forwards
        if limiter[0] < (self.nBrailleCellColumns - 1):
            #move limit forwards
            limiter[0] += 1
        else:
            if yPosition < self.nBrailleCellRows - 1:
# =============================================================================
#                 self.autoEndline = False
#                 self.createNewLine(yPosition, self.nBrailleCellColumns)
#                 
# =============================================================================
                self.moveCursorLimitNewLine(yPosition)
                #self.editorMatrix.insert(yPosition + 1,[])
            else:
                print("hit end of editor")
            
        #self.cursorLimiter[yPosition] = limiter
        #print(self.cursorLimiter)
    
    def moveCursorLimitNewLine(self, yPosition):
        
        #freeze the current limiter and create a new limiter
        if len(self.cursorLimiter) > (yPosition + 1):
            pass
        else:
            self.cursorLimiter.append([2,yPosition + 1])
            limiter = self.cursorLimiter[yPosition + 1]
            print(limiter)
        #move the limiter to the beginning
        
    def createNewLine(self, yPosition, xPosition):
        
        #creates a new line right below the input yPosition
        self.editorMatrix.insert(yPosition + 1,[])
        
        #move xPosition text down and cut it off
        bumpText = self.editorMatrix[yPosition][xPosition:]
        self.editorMatrix[yPosition + 1] = bumpText
        del self.editorMatrix[yPosition][xPosition:]
        
        #subtract length from cursor limit
        self.cursorLimiter[yPosition][0] -= len(bumpText)
        #insert the new limiter right below the current position
        insertLimiter = [len(bumpText),yPosition + 1]
        
        self.cursorLimiter.insert(yPosition + 1, insertLimiter)
        
        for index,limiter in enumerate(self.cursorLimiter):
            if index > (yPosition + 1):
                limiter[1] += 1
        
    def cursorMoveNewLine(self):
        xPosition = self.cursor[0]
        yPosition = self.cursor[1]
        nColumns = self.nBrailleCellColumns
        nRows = self.nBrailleCellRows


        if yPosition < (nRows - 1):
            self.cursor[1] = yPosition + 1
            self.cursor[0] = 0
            #print("move down")
        else:
            print("hit bottom")
        
    def moveCursorForward(self):
        xPosition = self.cursor[0]
        yPosition = self.cursor[1]
        nColumns = self.nBrailleCellColumns
        nRows = self.nBrailleCellRows
        
        ableToMoveForward = xPosition < (nColumns - 1) and self.limiterForwardCheck()
        #check if able to move down when cursor is in x postion 0
        self.cursor[0] = 0
        ableToMoveDown = yPosition < (nRows - 1) and self.limiterDownCheck()
        self.cursor[0] = xPosition

        #check if able to move forward
        if ableToMoveForward:
            #move forward
            self.cursor[0] = xPosition + 1
            #print("move right")
            #print(self.cursor)
        elif ableToMoveDown:
            #move down
            self.cursor[1] = yPosition + 1
            self.cursor[0] = 1
            #print("move down")
            #print(self.cursor)
        else:
            #do nothing
            print("hit bottom corner")
        #determine how to move forwards
        
    def moveCursorBackward(self):
        xPosition = self.cursor[0]
        yPosition = self.cursor[1]
        nColumns = self.nBrailleCellColumns
        nRows = self.nBrailleCellRows
        
        #check if able to move backward
        ableToMoveBackward = xPosition > 0 and self.limiterBackCheck()
        
        #check if able to move down when cursor is in the far x position
        ableToMoveUp = yPosition > 0
        
        
        #then determine how to move backwards
        
        if ableToMoveBackward:
            self.cursor[0] = xPosition - 1
            #print("move left")
            #print(self.cursor)
        elif ableToMoveUp:
            self.cursor[1] = yPosition - 1
            self.cursor[0] = self.cursorLimiter[yPosition-1][0]
            #print("move up")
            #print(self.cursor)
        else:
            print("hit top corner")
            
    def moveCursorUpward(self):
        #perform cursor movement up
        xPosition = self.cursor[0]
        yPosition = self.cursor[1]
        nRows = self.nBrailleCellRows
        
        ableToMoveUpward = yPosition > 0 and self.limiterUpCheck()
        
        if ableToMoveUpward:
            self.cursor[1] = yPosition - 1
            #print("new up key pressed")
        elif yPosition > 0:
            self.cursor[0] = self.cursorLimiter[yPosition - 1][0]
            self.cursor[1] = yPosition - 1
        else:
            print("hit upper edge")
            
    def moveCursorDownward(self):
        #perform cursor downward
        xPosition = self.cursor[0]
        yPosition = self.cursor[1]
        nRows = self.nBrailleCellRows
        
        ableToMoveDownward = yPosition < (nRows - 1) and self.limiterDownCheck()
        ableToMoveDownwardBottom = yPosition < (nRows - 1) and (len(self.cursorLimiter) > yPosition + 1)
        
# =============================================================================
#         self.cursorLimiter[yPosition+1][0]
#         ableToMoveDownwardXMove = 
#         self.cursorLimiter[yPosition+1][0]
# =============================================================================

        
        if ableToMoveDownward:
            self.cursor[1] = yPosition + 1
            #print("new down key pressed")
        elif ableToMoveDownwardBottom:
            self.cursor[0] = self.cursorLimiter[yPosition + 1][0]
            self.cursor[1] = yPosition + 1
# =============================================================================
#         elif :
#             self.cursorLimiter[yPosition+1][0]
# =============================================================================
        else:
            print("hit end of editor")
        
    def insertCharacter(self, character):
        self.startTime = time.time()
        
        #inserts a character at the cursor location
        xPosition = self.cursor[0]
        yPosition = self.cursor[1]
        
        #reformat the matrix back to display size
        #self.editorMatrix = self.reformatMatrixToDisplaySize(self.editorMatrix,self.nBrailleCellColumns)
        
        # add the character to the matrix
        self.addCharacterToMatrix(yPosition,xPosition,character)
        
        # move the cursor limit of the row forward
        self.moveCursorLimitForward(yPosition)
        
        # move the cursor forward
        self.moveCursorForward()
        
        
        
        self.endTime = time.time()
        execution_time = self.endTime - self.startTime
        #print(f"Outside text editor Execution time: {execution_time} seconds")
        
    def addCharacterToMatrix(self, yPosition,xPosition, character):
        #editorMatrixRows = len(self.editorMatrix)
        
        #print(yPosition)
        #print(self.editorMatrix[yPosition])
        
        #insert a row with the added character into the list
        if len(self.editorMatrix[yPosition]) < self.nBrailleCellColumns - 1:
            if yPosition != self.nBrailleCellRows - 1 or xPosition != self.nBrailleCellColumns - 1:
                insertRow = self.editorMatrix[yPosition][:xPosition] + [character] + self.editorMatrix[yPosition][xPosition:]
            
                self.editorMatrix[yPosition] = insertRow
                
        elif yPosition < self.nBrailleCellRows:

            insertRow = self.editorMatrix[yPosition][:xPosition] + [character] + self.editorMatrix[yPosition][xPosition:]
        
            self.editorMatrix[yPosition] = insertRow
            
            self.characterOverflow(yPosition)
        
            
        else:
            print("hit end of editor")
            
    def characterOverflow(self, yPosition):
        #this function takes the editor matrix and shifts the excess data down one line
        lineAlreadyBelow = len(self.editorMatrix) > (yPosition + 1)
        if lineAlreadyBelow:    
            isLineBelowLength = len(self.editorMatrix[yPosition + 1]) < self.nBrailleCellColumns
        noLineBelow = not lineAlreadyBelow
        
        #if a line is already below run overflow line function
        if lineAlreadyBelow and isLineBelowLength:
            #print("The overflow function needs to be ran")
            
            #print(self.editorMatrix)
            #first grab the overflow row
            overflowRow = self.editorMatrix[yPosition]
            #strip the excess characters
            excessCharacters = overflowRow[self.nBrailleCellColumns - 1:]
            #concatenate them with the next row
            self.editorMatrix[yPosition + 1] = excessCharacters + self.editorMatrix[yPosition + 1]
            #delete the excess of previous row
            self.editorMatrix[yPosition] = overflowRow[:self.nBrailleCellColumns - 1]

            #for the length of excessCharacters added push cursor limit
            for iCharacter in range(0,len(excessCharacters)):
                self.moveCursorLimitForward(yPosition + 1)
                
                
            #print(self.editorMatrix)
            
        #if there is no line below create a new line and run overflow line function
        else:
# =============================================================================
#             something = self.autoEndline
#             #print("A new line needs to be inserted below")
#             if something:
#                 self.autoEndline = False
#             else:
# =============================================================================
            self.createNewLine(yPosition, self.nBrailleCellColumns)
            self.characterOverflow(yPosition)
            print("oh noes")

        
        
                
    def deleteCharacter(self):
        xPosition = self.cursor[0]
        yPosition = self.cursor[1]
        
        #move the cursor backwards
        self.moveCursorBackward()
        
        #move the cursor limit of the row backward
        if xPosition > 0:
            self.moveCursorLimitBackward(yPosition)
        else:
            self.deleteCursorLimit(yPosition)
        
        self.removeCharacterFromMatrix(yPosition, xPosition)
        
        
    def removeCharacterFromMatrix(self, yPosition, xPosition):
        #editorMatrixRows = len(self.editorMatrix)
        appendRow = []
        #Just pop the character from the matrix
        
        if xPosition > 0:
            self.editorMatrix[yPosition].pop(xPosition - 1)
        else:
            if yPosition > 0:
                #move the text of the current line to previous line
                appendRow = self.editorMatrix[yPosition]
                
                #self.editorMatrix.pop(yPosition)
                
                #append the row
                self.editorMatrix[yPosition - 1] = self.editorMatrix[yPosition - 1] + appendRow
                
                newRowLength = len(self.editorMatrix[yPosition-1])
                
                if newRowLength < self.nBrailleCellColumns:
                    #if there is no excess just pop the row
                    self.editorMatrix.pop(yPosition)
                else:
                    #if there is excess extract it and add to the bottom row
                    excessRow = self.editorMatrix[yPosition - 1][self.nBrailleCellColumns - 1:]
                    self.editorMatrix[yPosition - 1] = self.editorMatrix[yPosition - 1][:self.nBrailleCellColumns - 1]
                    
                    self.editorMatrix[yPosition] = excessRow
                    
                    excessRowLength = len(excessRow)
                    
                    #add a new cursor limit in yPosition
                    #self.cursorLimiter.insert(yPosition, [excessRowLength, yPosition])
                
                    #set the cursor limit of the previous line to its max value
                    self.cursorLimiter[yPosition - 1] = [self.nBrailleCellColumns - 1, yPosition - 1]
                
                    print(self.cursorLimiter)
                
                print("no chacter to pop just delete line")
            else:
                print("hit the beginning of the editor")
            
    def limiterForwardCheck(self):
        #checks if the cursor can move forward
        xPosition = self.cursor[0]
        yPosition = self.cursor[1]
        nColumns = self.nBrailleCellColumns
        nRows = self.nBrailleCellRows
        
        limiter = self.cursorLimiter[yPosition]
        
        if limiter[0] > xPosition:
            #can move forward
            return True
        else:
            return False
            print("can't move forward")
        
    
    def limiterBackCheck(self):
        xPosition = self.cursor[0]
        yPosition = self.cursor[1]
        nColumns = self.nBrailleCellColumns
        nRows = self.nBrailleCellRows
        
        #really only matters when at the end of a line
        if xPosition != 0:
            return True
        else:
            return False
        
        
    
    def limiterDownCheck(self):
        xPosition = self.cursor[0]
        yPosition = self.cursor[1]
        nColumns = self.nBrailleCellColumns
        nRows = self.nBrailleCellRows
        
        if len(self.cursorLimiter) > (yPosition + 1):
            limiter = self.cursorLimiter[yPosition + 1]
            if limiter[0] >= xPosition:
                return True
            else:
                print("unable to move directly down")
                return False
        else:
            #can't move forward here
            return False
    
        
    def limiterUpCheck(self):
        xPosition = self.cursor[0]
        yPosition = self.cursor[1]
        nColumns = self.nBrailleCellColumns
        nRows = self.nBrailleCellRows
        
        #just down in reverse
        if yPosition > 0:
            limiter = self.cursorLimiter[yPosition - 1]
            if limiter[0] >= xPosition:
                return True
            else:
                print("unable to move directly up")
                return False
        else:
            #hit the upper limit
            return False
            print("hit the top of the editor")
            
    def checkLimiterInPosition(self, xPosition, yPosition):
        for limiter in self.cursorLimiter:
            if limiter[0] == xPosition and limiter[1] == yPosition:
                return True
        return False
            
    
    def reformatMatrixToDisplaySize(self,inputMatrix,nColumns):
        #reformat the list
        newMatrix = [[]]
        
        limiter = self.cursorLimiter[0]
        
        xIndex = 0
        yIndex = 0
        for stringList in inputMatrix:
            
            for character in stringList:
                newMatrix[yIndex].append(character)
                xIndex += 1
                limiter = self.cursorLimiter[0]
                if xIndex > (limiter[0] - 1):
                    xIndex = 0
                    yIndex += 1
                    newMatrix.append([])
            
        return newMatrix

        
    def editorMatrixOutput(self):
        #go through text and add carraige every 13 characters
        newText = ""
        nChar = 0
        
        for characterList in self.editorMatrix:
            for character in characterList:
                newText = newText + character
    
            newText = newText + "\n"
    
        newText = newText[0:-1]
        return newText
    
    
    def clear(self):
        self.boundingBox = [0, self.nBrailleCellRows - 1]
        self.cursor = [0,0] #in cell format
        self.cursorLimiter = [[0,0]]
        self.editorString = ""
        self.editorMatrix = [[]]
        
        newLineList = []
        self.editorBox = []
        
    
    
    
