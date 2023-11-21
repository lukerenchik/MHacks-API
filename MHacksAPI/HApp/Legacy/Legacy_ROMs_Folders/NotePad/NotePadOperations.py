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
        if self.displayUpdate == 20:
            self.BrailleDisplay.refresh()
            self.displayUpdate = 0
        else:
            self.displayUpdate += 1
            
    def restartOperation(self):
        self.displayUpdate = 0
            
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
        
        
    def execute(self):
        
        cellXPosition = self.TextEditor.cursor[0]
        cellYPosition = self.TextEditor.cursor[1] - self.TextEditor.boundingBox[0]
        
        
        brailleXPosition = cellXPosition*3
        brailleYPosition = cellYPosition*4
        
        
        pinPosition = (brailleXPosition,brailleYPosition)
        #print(pinPosition)

        
        #self.Editor.editorBoxFormatter(self.Editor.editorString)
        #print(pinPosition)
        
        
        #put the text in the editor
# =============================================================================
#         self.displayText = self.TextEditor.outputStringFormatter()
#         self.TextEditor.textChanged.disconnect()
#         self.TextEditor.clear()
#         self.TextEditor.setPlainText(self.displayText)
#         self.TextEditor.textChanged.connect(lambda: self.textChangeFunction())
# =============================================================================
        
        self.BrailleDisplay.setPinCursorPosition(pinPosition)
        #print(self.TextEditor.editorString)
        #print(id(self.BrailleDisplay))
        
        #when cursor location moves outside of bounding box switch bounding box location
        pinCursor = self.BrailleDisplay.grabPinCursor()
        
        if self.displayString != self.TextEditor.editorMatrixOutput():
            self.displayString = self.TextEditor.editorMatrixOutput()
            self.Controller.OperationsController.restartExecutingOperation("BrailleDisplayRefreshOperation")
            
        #make the pin cursor position blink
        if self.cursorBlinker == 50:
            self.cursorBlinker = 0
            self.BrailleDisplay.braille((0,0),self.TextEditor.editorMatrixOutput())
            #self.BrailleDisplay.erase("on")
            #self.Controller.BrailleDisplay.fill("on")
            self.BrailleDisplay.rect((pinCursor[1],pinCursor[0]),(pinCursor[1] + 3,pinCursor[0] + 1))
            for limiter in self.TextEditor.cursorLimiter: 
                try:
                    xPosition = limiter[0]*3
                    yPosition = limiter[1]*4
                    #self.BrailleDisplay.line((yPosition,xPosition + 2),(yPosition + 3, 41))
                except:
                    print(self.TextEditor.cursorLimiter)
                    pass
            #self.Controller.BrailleDisplay.fill("off")
            #self.Controller.OperationsController.BrailleDisplay.erase("off")
        elif self.cursorBlinker == 25:
            self.BrailleDisplay.braille((0,0),self.TextEditor.editorMatrixOutput())
            for limiter in self.TextEditor.cursorLimiter:  
                try:
                    xPosition = limiter[0]*3
                    yPosition = limiter[1]*4
                    #self.BrailleDisplay.line((yPosition,xPosition + 2),(yPosition + 3, 41))
                except:
                    print(self.TextEditor.cursorLimiter)
                    pass
            self.Controller.OperationsController.restartExecutingOperation("BrailleDisplayRefreshOperation")
          
# =============================================================================
#         if self.cursorBlinker == 0:
#             for limiter in self.TextEditor.cursorLimiter:  
#                 xPosition = limiter[0]*3
#                 yPosition = limiter[1]*4
#                 self.BrailleDisplay.line((yPosition,xPosition + 2),(yPosition + 3,xPosition + 2))
# =============================================================================
                
        self.cursorBlinker += 1
            
        
        