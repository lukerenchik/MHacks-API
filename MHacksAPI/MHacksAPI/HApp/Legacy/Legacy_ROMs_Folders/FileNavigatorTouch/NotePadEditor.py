# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 13:52:37 2022

@author: Derek Joslin

"""

import TextEditor as tt


class NotePadEditor(tt.TextEditor):

    def pageUp(self):
        
        self.boundingBox[0] -= self.nBrailleCellRows
        self.boundingBox[1] -= self.nBrailleCellRows
        self.cursor[1] -= self.nBrailleCellRows
        self.cursor[0] = self.cursorLimiter[self.cursor[1]][0]
        
        if self.boundingBox[0] < 0:
            self.boundingBox[1] = self.nBrailleCellRows - 1
            self.boundingBox[0] = 0
            self.cursor[1] = 0
            self.cursor[0] = self.cursorLimiter[self.cursor[1]][0]
        
    def pageDown(self):
        
        self.boundingBox[0] += self.nBrailleCellRows
        self.boundingBox[1] += self.nBrailleCellRows
        self.cursor[1] += self.nBrailleCellRows
        
        if self.boundingBox[1] > len(self.cursorLimiter):
            self.boundingBox[1] = len(self.cursorLimiter) - 1
            self.boundingBox[0] = len(self.cursorLimiter) - 1 - self.nBrailleCellRows
            self.cursor[1] = self.boundingBox[0]
            self.cursor[0] = self.cursorLimiter[self.cursor[1]][0]
        elif self.boundingBox[0] < 0:
            self.boundingBox[0] = 0
            self.cursor[1] = self.boundingBox[0]
            self.cursor[0] = self.cursorLimiter[self.cursor[1]][0]
        
    def moveCursorDownward(self):
        
        yPosition = self.cursor[1]
        super().moveCursorDownward()
            
        #if the cursor is at the bottom of the bounding box then increase bounding
        print(self.boundingBox[1] == yPosition)
        if self.boundingBox[1] == yPosition:
            self.boundingBox[0] += 1
            self.boundingBox[1] += 1
            
        if len(self.cursorLimiter) - 1 > yPosition:
            self.cursor[0] = self.cursorLimiter[yPosition + 1][0]#self.nBrailleCellColumns - 1#self.cursorLimiter[self.cursor[1] + 1][0]
            self.cursor[1] = yPosition + 1
            

    def moveCursorUpward(self):
        
        yPosition = self.cursor[1]
        
        super().moveCursorUpward()
        
        #if the cursor is at the bottom of the bounding box then increase bounding
        print(self.boundingBox[0] == yPosition)
        if self.boundingBox[0] == yPosition and self.boundingBox[0] > 0:
            self.boundingBox[0] -= 1
            self.boundingBox[1] -= 1
            
        if self.boundingBox[0] > 0:
            self.cursor[0] = self.cursorLimiter[yPosition - 1][0]#self.nBrailleCellColumns - 1#self.cursorLimiter[self.cursor[1] + 1][0]
            self.cursor[1] = yPosition - 1

    def moveCursorForward(self):
        xPosition = self.cursor[0]
        yPosition = self.cursor[1]
        nColumns = self.nBrailleCellColumns
        nRows = self.nBrailleCellRows
        
        ableToMoveForward = xPosition < (nColumns - 1) and self.limiterForwardCheck()
        #check if able to move down when cursor is in x postion 0
        self.cursor[0] = 0
        ableToMoveDown = yPosition < (len(self.cursorLimiter) - 1) and self.limiterDownCheck()
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
            self.cursor[0] = 0
            
            if self.boundingBox[1] == yPosition:
                self.boundingBox[0] += 1
                self.boundingBox[1] += 1
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
            
            if self.boundingBox[0] == yPosition and self.boundingBox[0] > 0:
                self.boundingBox[0] -= 1
                self.boundingBox[1] -= 1
            #print("move up")
            #print(self.cursor)
        else:
            print("hit top corner")

    def editorMatrixOutput(self):
        
        #go through text inside the bounding box and add carraige every 13 characters
        startRow = self.boundingBox[0]
        endRow = self.boundingBox[1]
        
        
        boundedMatrix = self.editorMatrix[startRow:endRow + 1]
        
        newText = ""
        nChar = 0
        
        for characterList in boundedMatrix:
            for character in characterList:
                newText = newText + character
    
            newText = newText + "\n"
    
        newText = newText[0:-1]
        
        return newText
    
        
    def loadTxt(self, filename):
        self.clear()
        notePadFile = open(filename, "r")
        notePadString = notePadFile.read()
    
        notePadList = notePadString.split("\n")
        
        numChar = 0
        
        for notePadLine in notePadList:
            for character in notePadLine:
                self.insertCharacter(character)
                numChar += 1
                if numChar > self.nBrailleCellColumns - 1:
                    numChar = 0
                    #make newline
                    xPosition = self.cursor[0]
                    yPosition = self.cursor[1]
                    
                    self.createNewLine(yPosition, xPosition)
                    self.moveCursorDownward()
                    self.cursor[0] = 0
            
            #make newline
            numChar = 0
            xPosition = self.cursor[0]
            yPosition = self.cursor[1]
            
            self.createNewLine(yPosition, xPosition)
            self.moveCursorDownward()
            self.cursor[0] = 0
        
        self.boundingBox = [0, self.nBrailleCellRows - 1]
        self.cursor = [0,0] #in cell format
        
        