# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 15:12:42 2022

@author: Derek Joslin
"""

import RomAPI as rs


import DefaultKeyboardHandles as dh


class TextEditorKeyboardHandles(dh.DefaultKeyboardHandles):
    
    def __init__(self, textEditor):
        super().__init__()
        
        self.editor = textEditor
        
        
# =============================================================================
#     def stringPositionLocater(self):
#         #grab the x and y display positions
#         xPosition = self.editor.cursor[0]
#         yPosition = self.editor.cursor[1]
#         nColumns = self.editor.nBrailleCellColumns
#         nRows = self.editor.nBrailleCellRows
#         
#         #parse the current string to figure out the proper position
#         editorString = self.editor.editorString
#         
#         newLineStringList = editorString.split("\n")
#         
#         cursorStringPosition = 0
#         
#         virtualXPosition = 0
#         virtualYPosition = 0
# 
#         
#         for stringList in newLineStringList:
#             charCounter = 0
#             for character in stringList:
#                 virtualXPosition +=1
#                 cursorStringPosition += 1
#                 if virtualXPosition > nColumns:
#                     virtualXPosition = 0
#                     virtualYPosition += 1
#                     cursorStringPosition += 1
# 
#                 
#                 if virtualXPosition == xPosition and virtualYPosition == yPosition:
#                     break
#             if virtualXPosition == xPosition and virtualYPosition == yPosition:
#                 break
#             virtualYPosition += 1
#             cursorStringPosition = cursorStringPosition + 2
#         
#         print(self.editor.cursor)
#         print(cursorStringPosition)
#         return cursorStringPosition
#         
# =============================================================================
            
    def KeyLeftHandler(self):
        #perform cursor movement left
        self.editor.moveCursorBackward()
        
    def KeyUpHandler(self):
        #perform cursor movement up
        self.editor.moveCursorUpward()
        
    def KeyRightHandler(self):
        #perform cursor movement right
        self.editor.moveCursorForward()
        
    def KeyDownHandler(self):
        #perform cursor movement down
        self.editor.moveCursorDownward()


    def KeySpaceHandler(self):
        self.editor.insertCharacter(" ")
        
        
    def KeyAHandler(self):
        self.editor.insertCharacter("a")
        
        #print("Editor A key pressed")
        
    def KeyBHandler(self):
       self.editor.insertCharacter("b")
        
       #print("Editor B key pressed")
        
    def KeyCHandler(self):
       self.editor.insertCharacter("c")
        
       #print("Editor C key pressed")
        
    def KeyDHandler(self):
       self.editor.insertCharacter("d")
        
       #print("Editor D key pressed")
        
    def KeyEHandler(self):
       self.editor.insertCharacter("e")
        
       #print("Editor E key pressed")

    def KeyFHandler(self):
       self.editor.insertCharacter("f")
        
       #print("Editor F key pressed")
        
    def KeyGHandler(self):
       self.editor.insertCharacter("g")
        
       #print("Editor G key pressed")
        
    def KeyHHandler(self):
       self.editor.insertCharacter("h")
        
       #print("Editor H key pressed")
        
    def KeyIHandler(self):
       self.editor.insertCharacter("i")
        
       #print("Editor I key pressed")
        
    def KeyJHandler(self):
       self.editor.insertCharacter("j")
        
       #print("Editor J key pressed")
        
    def KeyKHandler(self):
       self.editor.insertCharacter("k")
        
       #print("Editor K key pressed")
        
    def KeyLHandler(self):
       self.editor.insertCharacter("l")
        
       #print("Editor L key pressed")
        
    def KeyMHandler(self):
       self.editor.insertCharacter("m")
        
       #print("Editor M key pressed")
        
    def KeyNHandler(self):
       self.editor.insertCharacter("n")
        
       #print("Editor n key pressed")
        
    def KeyOHandler(self):
       self.editor.insertCharacter("o")
        
       #print("Editor O key pressed")

    def KeyPHandler(self):
       self.editor.insertCharacter("p")
        
       #print("Editor P key pressed")
        
    def KeyQHandler(self):
       self.editor.insertCharacter("q")
        
       #print("Editor Q key pressed")
        
    def KeyRHandler(self):
       self.editor.insertCharacter("r")
        
       #print("Editor R key pressed")
        
    def KeySHandler(self):
       self.editor.insertCharacter("s")
        
       #print("Editor S key pressed")
        
    def KeyTHandler(self):
       self.editor.insertCharacter("t")
        
       #print("Editor T key pressed")
        
    def KeyUHandler(self):
       self.editor.insertCharacter("u")
        
       #print("Editor u key pressed")
        
    def KeyVHandler(self):
       self.editor.insertCharacter("v")
        
       #print("Editor V key pressed")
        
    def KeyWHandler(self):
       self.editor.insertCharacter("w")
        
       #print("Editor W key pressed")
        
    def KeyXHandler(self):
       self.editor.insertCharacter("x")
        
       #print("Editor X key pressed")
        
    def KeyYHandler(self):
       self.editor.insertCharacter("y")
        
       #print("Editor Y key pressed")
      
    def KeyZHandler(self):
       self.editor.insertCharacter("z")
        
       #print("Editor z key pressed")

    def KeyBackSpaceHandler(self):
        self.editor.deleteCharacter()
        
    def KeyEnterHandler(self):
        xPosition = self.editor.cursor[0]
        yPosition = self.editor.cursor[1]
        
        self.editor.createNewLine(yPosition, xPosition)
        self.editor.moveCursorDownward()
        self.editor.cursor[0] = 0
        
    def KeyReturnHandler(self):
        xPosition = self.editor.cursor[0]
        yPosition = self.editor.cursor[1]
        
        self.editor.createNewLine(yPosition, xPosition)
        self.editor.moveCursorDownward()
        self.editor.cursor[0] = 0
        
    def Key0Handler(self):
        self.editor.insertCharacter("0")
        
    def Key1Handler(self):
        self.editor.insertCharacter("1")
        
    def Key2Handler(self):
        self.editor.insertCharacter("2")
        
    def Key3Handler(self):
        self.editor.insertCharacter("3")
        
    def Key4Handler(self):
        self.editor.insertCharacter("4")
        
    def Key5Handler(self):
        self.editor.insertCharacter("5")
        
    def Key6Handler(self):
        self.editor.insertCharacter("6")
        
    def Key7Handler(self):
        self.editor.insertCharacter("7")
        
    def Key8Handler(self):
        self.editor.insertCharacter("8")
        
    def Key9Handler(self):
        self.editor.insertCharacter("9")
        
    def KeyParenLeftHandler(self):
        self.editor.insertCharacter("(")
        
    def KeyParenRightHandler(self):
        self.editor.insertCharacter(")")
        
    def KeyCommaHandler(self):
        self.editor.insertCharacter(",")
        
    def KeyPlusHandler(self):
        self.editor.insertCharacter("+")
        
    def KeyMinusHandler(self):
        self.editor.insertCharacter("-")
        
    def KeyAsteriskHandler(self):
        self.editor.insertCharacter("*")
        
    def KeyPeriodHandler(self):
        self.editor.insertCharacter(".")
        
    def KeySlashHandler(self):
        self.editor.insertCharacter("\\")
        
    def KeyColonHandler(self):
        self.editor.insertCharacter(":")
        
    def KeySemicolonHandler(self):
        self.editor.insertCharacter(";")
        
    def BracketLeftHandler(self):
        self.editor.insertCharacter("[")        
        
    def BracketRightHandler(self):
        self.editor.insertCharacter("]")
        
    def EqualHandler(self):
        self.editor.insertCharacter("=")
        
    def GreaterHandler(self):
        self.editor.insertCharacter(">")
        
    def LessHandler(self):
        self.editor.insertCharacter("<")
        
    def QuoteDblHandler(self):
        self.editor.insertCharacter('"')
        
    def QuoteLeftHandler(self):
        self.editor.insertCharacter("'")
        
    def KeyPageUpHandler(self):
        self.editor.pageUp()
    
    def KeyPageDownHandler(self):
        self.editor.pageDown()
        
    def KeyF1Handler(self):
        for characterList in self.editor.editorMatrix:
            print(characterList)
        
    def KeyF2Handler(self):
        #reset the mode and period and duty cycle
        self.editor.clear()
        self.cursorMode = 0
        self.period = 100
        self.dutyCycle = 0.5
        self.editor.cursorMode = 0
        
        
    def KeyF3Handler(self):
        print(self.editor.editorMatrixOutput())
        
    def KeyF4Handler(self):
        self.editor.cursorMode += 1
        if self.editor.cursorMode > 4:
            self.editor.cursorMode = 0
        #self.editor.clear()
        print(self.editor.cursorMode)
        
    def KeyF5Handler(self):
        filename = "C:/Users/derek/OneDrive/NewHaptics Shared/HapticOS/FC_GUI_API/APIv0.7-Coeus/v0.764-Coeus/testScripts/SampleDocument.txt"
        self.editor.loadTxt(filename)
        self.editor.cursorMode = 0

        
        
    def KeyF6Handler(self):
        filename = "C:/Users/derek/OneDrive/NewHaptics Shared/HapticOS/FC_GUI_API/APIv0.7-Coeus/v0.764-Coeus/testScripts/ArabicNumerals.txt"
        self.editor.loadTxt(filename)
        self.editor.cursorMode = 0
        


    def KeyF7Handler(self):
        filename = "C:/Users/derek/OneDrive/NewHaptics Shared/HapticOS/FC_GUI_API/APIv0.7-Coeus/v0.764-Coeus/testScripts/CityPop.txt"
        self.editor.loadTxt(filename)
        self.editor.cursorMode = 0


        
    def KeyF8Handler(self):
        filename = "C:/Users/derek/OneDrive/NewHaptics Shared/HapticOS/FC_GUI_API/APIv0.7-Coeus/v0.764-Coeus/testScripts/CityArea.txt"
        self.editor.loadTxt(filename)
        self.editor.cursorMode = 0

        
    def KeyF9Handler(self):
        filename = "C:/Users/derek/OneDrive/NewHaptics Shared/HapticOS/FC_GUI_API/APIv0.7-Coeus/v0.764-Coeus/testScripts/History.txt"
        self.editor.loadTxt(filename)
        self.editor.cursorMode = 0

        
    def KeyF10Handler(self):
        filename = "C:/Users/derek/OneDrive/NewHaptics Shared/HapticOS/FC_GUI_API/APIv0.7-Coeus/v0.764-Coeus/testScripts/English.txt"
        self.editor.loadTxt(filename)
        self.editor.cursorMode = 0

        
    def KeyF11Handler(self):
        filename = "C:/Users/derek/OneDrive/NewHaptics Shared/HapticOS/FC_GUI_API/APIv0.7-Coeus/v0.764-Coeus/testScripts/Math.txt"
        self.editor.loadTxt(filename)
        self.editor.cursorMode = 0


    def KeyF12Handler(self):
        filename = "C:/Users/derek/OneDrive/NewHaptics Shared/HapticOS/FC_GUI_API/APIv0.7-Coeus/v0.764-Coeus/testScripts/FileNavigationTouch.txt"
        self.editor.loadTxt(filename)
        self.editor.cursor[1] = 4
        self.editor.cursorMode = 1


    def KeyEndHandler(self):
        if self.editor.period < 1000:
            self.editor.period += 10
            print(self.editor.period)
            print("timeLow{}".format(int(self.editor.period * self.editor.dutyCycle)))
        else:
            print("Maximum duty cycle of 1000 reached")


    def KeyDeleteHandler(self):
        if self.editor.period > 10:
            self.editor.period -= 10
            print(self.editor.period)
            print("timeLow{}".format(int(self.editor.period * self.editor.dutyCycle)))
        else:
            print("Minimum period of 100 reached")
        
        
    def KeyShiftHandler(self):
        if self.editor.dutyCycle > 0.15:
            self.editor.dutyCycle -= 0.05
            print(self.editor.dutyCycle)
            print("timeLow{}".format(int(self.editor.period * self.editor.dutyCycle)))
        else:
            print("Minimum duty cycle of 10 reached")
            
            
    def KeyTabHandler(self):
        if self.editor.dutyCycle < 0.9:
            self.editor.dutyCycle += 0.05
            print(self.editor.dutyCycle)
            print("timeLow{}".format(int(self.editor.period * self.editor.dutyCycle)))
        else:
            print("Max duty cycle 90 reached")
        
        
    def KeyCapsLockHandler(self):
        if self.editor.touchScreenMode:
            # deactivate touch screen mode
            self.editor.touchScreenMode = 0
            print("Touch screen mode deactivated")
        else:
            # activate touch screen mode
            self.editor.touchScreenMode = 1
            print("Touch screen mode activated")
