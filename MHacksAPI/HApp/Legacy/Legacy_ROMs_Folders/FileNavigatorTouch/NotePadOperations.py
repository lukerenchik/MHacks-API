# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 15:12:55 2022

@author: Derek Joslin
"""

import RomAPI as rs


class BrailleDisplayRefreshOperation(rs.RomOperation):
    
    def __init__(self, engine):
        super().__init__()
        self.BrailleDisplay = engine
        self.displayUpdate = 0
        
    def execute(self):
        if self.operationOn:
            self.refreshDisplay()
            
    def refreshDisplay(self):
        if self.displayUpdate == 20:
            self.BrailleDisplay.refresh()
            self.displayUpdate = 0
        else:
            self.displayUpdate += 1
            
    def restartOperation(self):
        self.displayUpdate = 0
        
    def stopOperation(self):
        self.operationOn = 0
        
class GetTouchScreenOperation(rs.RomOperation):
    
    def __init__(self, Controller, Editor):
        super().__init__()
        self.Controller = Controller
        self.BrailleDisplay = self.Controller.OperationsController.BrailleDisplay
        self.TextEditor = Editor
        self.BrailleCellColumn = 0
        self.BrailleCellRow = 0
        self.touchScreenTimer = 0
        
    def stopOperation(self):
        self.operationOn = 0
        
    def execute(self):
        if self.operationOn:
            self.getTouchScreenCursor()
       
            
    def getTouchScreenCursor(self):
        #check the position of the touch screen
        if self.touchScreenTimer > 50:
            self.touchScreenTimer = 0
            
            pinCursor = self.BrailleDisplay.getPinCursorPosition()
            
            #print("Old Touch Screen Braille Position {0},{1}".format(self.BrailleCellColumn, self.BrailleCellRow))
            
            newBrailleCellColumn = int((pinCursor[1] + 1)/3)
            newBrailleCellRow = int((pinCursor[0] + 1)/4)
            
            if newBrailleCellRow == 5:
                newBrailleCellRow = 4
            
            #print("New Touch Screen Braille Position {0},{1}".format(newBrailleCellColumn, newBrailleCellRow))
            
            
            #if the touch screen position is different than the text editor position set text editor to touch screen position
            if (self.BrailleCellRow != newBrailleCellRow or self.BrailleCellColumn != newBrailleCellColumn) and self.TextEditor.touchScreenMode :
                
                self.BrailleCellColumn = newBrailleCellColumn
                self.BrailleCellRow = newBrailleCellRow
                
                #set the TextEditor y position to the touch position
                self.TextEditor.cursor[1] = self.BrailleCellRow + self.TextEditor.boundingBox[0]
                self.TextEditor.cursor[0] = self.BrailleCellColumn
                print("New Braille Position {0}".format(self.BrailleCellRow))
                print("New Editor Position {0}".format(self.TextEditor.cursor[1]))
                print("New Pin Position {0}".format(pinCursor[0]))
                
        else:
            self.touchScreenTimer += 1
        
            
    
class BlinkCursorOperation(rs.RomOperation):
    
    def __init__(self, Controller, Editor):
        super().__init__()
        self.Controller = Controller
        self.BrailleDisplay = self.Controller.OperationsController.BrailleDisplay
        self.TextEditor = Editor
        self.displayString = ""
        self.cursorBlinker = 0
# =============================================================================
#         self.displayText = ""
# =============================================================================
    def stopOperation(self):
        self.operationOn = 0
            
    def cursorBlink(self):
        #check the position of the text editor
        cellXPosition = self.TextEditor.cursor[0]
        cellYPosition = self.TextEditor.cursor[1] - self.TextEditor.boundingBox[0]
        
        brailleXPosition = cellXPosition*3
        brailleYPosition = cellYPosition*4
        
        pinPosition = (brailleXPosition,brailleYPosition)
        
        
        self.BrailleDisplay.setPinCursorPosition(pinPosition)
        
        #when cursor location moves outside of bounding box switch bounding box location
        pinCursor = self.BrailleDisplay.grabPinCursor()
        
        #control refresh
        if self.displayString != self.TextEditor.editorMatrixOutput():
            self.displayString = self.TextEditor.editorMatrixOutput()
            self.Controller.OperationsController.restartExecutingOperation("BrailleDisplayRefreshOperation")
            
            
        try:
            self.renderCursor(pinCursor, self.TextEditor.period, self.TextEditor.dutyCycle)
        except:
            print("unable to render cursor")
                
        self.cursorBlinker += 1
    
    def execute(self):
        if self.operationOn:
            self.cursorBlink()
        
    def renderCursor(self, pinCursor, period, dutyCycle): #, period, dutyCycle
        
# =============================================================================
#         #make the pin cursor position blink
#         if self.cursorBlinker == 100:
#             self.cursorBlinker = 0
#             self.BrailleDisplay.braille((0,0),self.TextEditor.editorMatrixOutput())
#             
#             #turn the cursor on
#             self.cursorOn(pinCursor)
#             
#             
#         elif self.cursorBlinker == 50:
#             self.BrailleDisplay.braille((0,0),self.TextEditor.editorMatrixOutput())
#             
#             #turn the cursor off
#             self.cursorOff(pinCursor)
# 
#             
#             self.Controller.OperationsController.restartExecutingOperation("BrailleDisplayRefreshOperation")
#         
# =============================================================================
        #calculate the number of times the cursor should blink
        #numBlinks = period // dutyCycle
        #print(numBlinks)
        timeLow = int(period * dutyCycle)
        
        #make the pin cursor position blink
        if self.cursorBlinker > period:
            #print(self.cursorBlinker)
            self.cursorBlinker = 0
            self.BrailleDisplay.braille((0,0),self.TextEditor.editorMatrixOutput())
            
            #turn the cursor on
            self.cursorOn(pinCursor)

        elif self.cursorBlinker == timeLow:
            #print(self.cursorBlinker)
            self.BrailleDisplay.braille((0,0),self.TextEditor.editorMatrixOutput())
            
            #turn the cursor off
            self.cursorOff(pinCursor)
    
            #restart the refresh operation
            self.Controller.OperationsController.restartExecutingOperation("BrailleDisplayRefreshOperation")

        
    def cursorOn(self, pinCursor):
        
        if self.TextEditor.cursorMode == 0:
            #just blink the cursor like normal
            self.BrailleDisplay.rect((pinCursor[1],pinCursor[0]),(pinCursor[1] + 3,pinCursor[0] + 1))
            
            
        elif self.TextEditor.cursorMode == 1:
            #force cursor to left side
            self.BrailleDisplay.rect( (pinCursor[1], 0), (pinCursor[1] + 3, 1) )

            
        elif self.TextEditor.cursorMode == 2:
            #force cursor to left unblinking
            self.BrailleDisplay.rect( (pinCursor[1], 0), (pinCursor[1] + 3, 1) )

            

        elif self.TextEditor.cursorMode == 3:
            #blink line 1
            self.BrailleDisplay.rect( (pinCursor[1], 0), (pinCursor[1] + 3, 1)  )
            
            
        elif self.TextEditor.cursorMode == 4:
            #blink line 0
            self.BrailleDisplay.rect( (pinCursor[1], 0), (pinCursor[1] + 3, 1) )
            
            
            
        elif self.TextEditor.cursorMode == 5:
            pass
        
        else:
            #just blink the cursor like normal
            self.BrailleDisplay.rect((pinCursor[1],pinCursor[0]),(pinCursor[1] + 3,pinCursor[0] + 1))
            
            
    def cursorOff(self, pinCursor):
        
        if self.TextEditor.cursorMode == 0:
            #just blink the cursor like normal
            pass
            
        elif self.TextEditor.cursorMode == 1:
            #force cursor to left side
            pass
            
        elif self.TextEditor.cursorMode == 2:
            #force cursor to left unblinking
            self.BrailleDisplay.rect( (pinCursor[1], 0), (pinCursor[1] + 3, 1) )
            
        elif self.TextEditor.cursorMode == 3:
            #blink line 1
            self.BrailleDisplay.rect( (pinCursor[1], 0), (pinCursor[1] + 3, 1) )
            self.BrailleDisplay.fill("on")
            self.BrailleDisplay.rect( (pinCursor[1], 0), (pinCursor[1] + 3, 41) )
            self.BrailleDisplay.fill("off")

            
        elif self.TextEditor.cursorMode == 4:
            #blink line 0
            
            self.BrailleDisplay.erase("on")
            self.BrailleDisplay.fill("on")
            self.BrailleDisplay.rect( (pinCursor[1], 3), (pinCursor[1] + 3, 41) )
            self.BrailleDisplay.fill("off")
            self.BrailleDisplay.rect( (pinCursor[1], 3), (pinCursor[1] + 3, 41) )
            self.BrailleDisplay.erase("off")
            self.BrailleDisplay.rect( (pinCursor[1], 0), (pinCursor[1] + 3, 1) )
            
        elif self.TextEditor.cursorMode == 5:
            pass
        
        else:
            pass
        
        
        