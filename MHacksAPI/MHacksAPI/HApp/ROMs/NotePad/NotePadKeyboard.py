# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 15:12:42 2022

@author: Derek Joslin
"""

import RomAPI as rs

import DefaultKeyboardHandles as dh

class TextEditorKeyboardHandles(dh.DefaultKeyboardHandles):

    def __init__(self, textEditor, HAppControlCenter):
        super().__init__()

        self.HAppControlCenter = HAppControlCenter

        self.TactileDisplay = self.HAppControlCenter.getPeripheral("NewHaptics Display SarissaV1")
        self.TactileDisplayRefreshOperation = self.HAppControlCenter.getOperation("TactileDisplayRefreshOperation")

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
    def updateDisplay(self):
        self.HAppControlCenter.interruptExecute(lambda: self.TactileDisplayRefreshOperation.execute())

    def KeyLeftHandler(self):
        #perform cursor movement left
        self.editor.moveCursorBackward()
        self.updateDisplay()

    def KeyUpHandler(self):
        #perform cursor movement up
        self.editor.moveCursorUpward()
        self.updateDisplay()

    def KeyRightHandler(self):
        #perform cursor movement right
        self.editor.moveCursorForward()
        self.updateDisplay()

    def KeyDownHandler(self):
        #perform cursor movement down
        self.editor.moveCursorDownward()
        self.updateDisplay()

    def KeySpaceHandler(self):
        self.editor.insertCharacter(" ")
        self.updateDisplay()
    def KeyAHandler(self):
        self.editor.insertCharacter("a")
        self.updateDisplay()
        #print("Editor A key pressed")

    def KeyBHandler(self):
        self.editor.insertCharacter("b")
        self.updateDisplay()
       #print("Editor B key pressed")

    def KeyCHandler(self):
        self.editor.insertCharacter("c")
        self.updateDisplay()

       #print("Editor C key pressed")

    def KeyDHandler(self):
        self.editor.insertCharacter("d")
        self.updateDisplay()
       #print("Editor D key pressed")

    def KeyEHandler(self):
        self.editor.insertCharacter("e")
        self.updateDisplay()
       #print("Editor E key pressed")

    def KeyFHandler(self):
        self.editor.insertCharacter("f")
        self.updateDisplay()
       #print("Editor F key pressed")

    def KeyGHandler(self):
        self.editor.insertCharacter("g")
        self.updateDisplay()
       #print("Editor G key pressed")

    def KeyHHandler(self):
        self.editor.insertCharacter("h")
        self.updateDisplay()
       #print("Editor H key pressed")

    def KeyIHandler(self):
        self.editor.insertCharacter("i")
        self.updateDisplay()
       #print("Editor I key pressed")

    def KeyJHandler(self):
        self.editor.insertCharacter("j")
        self.updateDisplay()
       #print("Editor J key pressed")

    def KeyKHandler(self):
        self.editor.insertCharacter("k")
        self.updateDisplay()
       #print("Editor K key pressed")

    def KeyLHandler(self):
        self.editor.insertCharacter("l")
        self.updateDisplay()
       #print("Editor L key pressed")

    def KeyMHandler(self):
        self.editor.insertCharacter("m")
        self.updateDisplay()
       #print("Editor M key pressed")

    def KeyNHandler(self):
        self.editor.insertCharacter("n")
        self.updateDisplay()
       #print("Editor n key pressed")

    def KeyOHandler(self):
        self.editor.insertCharacter("o")
        self.updateDisplay()
       #print("Editor O key pressed")

    def KeyPHandler(self):
        self.editor.insertCharacter("p")
        self.updateDisplay()
       #print("Editor P key pressed")

    def KeyQHandler(self):
        self.editor.insertCharacter("q")
        self.updateDisplay()
       #print("Editor Q key pressed")

    def KeyRHandler(self):
        self.editor.insertCharacter("r")
        self.updateDisplay()
       #print("Editor R key pressed")

    def KeySHandler(self):
        self.editor.insertCharacter("s")
        self.updateDisplay()
       #print("Editor S key pressed")

    def KeyTHandler(self):
        self.editor.insertCharacter("t")
        self.updateDisplay()
       #print("Editor T key pressed")

    def KeyUHandler(self):
        self.editor.insertCharacter("u")
        self.updateDisplay()
       #print("Editor u key pressed")

    def KeyVHandler(self):
        self.editor.insertCharacter("v")
        self.updateDisplay()
       #print("Editor V key pressed")

    def KeyWHandler(self):
        self.editor.insertCharacter("w")
        self.updateDisplay()
       #print("Editor W key pressed")

    def KeyXHandler(self):
        self.editor.insertCharacter("x")
        self.updateDisplay()
       #print("Editor X key pressed")

    def KeyYHandler(self):
        self.editor.insertCharacter("y")
        self.updateDisplay()
        #print("Editor Y key pressed")

    def KeyZHandler(self):
        self.editor.insertCharacter("z")
        self.updateDisplay()
       #print("Editor z key pressed")

    def KeyBackSpaceHandler(self):
        self.editor.deleteCharacter()
        self.updateDisplay()

    def KeyEnterHandler(self):
        xPosition = self.editor.cursor[0]
        yPosition = self.editor.cursor[1]

        self.editor.createNewLine(yPosition, xPosition)
        self.editor.moveCursorDownward()
        self.editor.cursor[0] = 0
        self.updateDisplay()


    def KeyReturnHandler(self):
        xPosition = self.editor.cursor[0]
        yPosition = self.editor.cursor[1]

        self.editor.createNewLine(yPosition, xPosition)
        self.editor.moveCursorDownward()
        self.editor.cursor[0] = 0
        self.updateDisplay()

    def Key0Handler(self):
        self.editor.insertCharacter("0")
        self.updateDisplay()

    def Key1Handler(self):
        self.editor.insertCharacter("1")
        self.updateDisplay()

    def Key2Handler(self):
        self.editor.insertCharacter("2")
        self.updateDisplay()

    def Key3Handler(self):
        self.editor.insertCharacter("3")
        self.updateDisplay()

    def Key4Handler(self):
        self.editor.insertCharacter("4")
        self.updateDisplay()

    def Key5Handler(self):
        self.editor.insertCharacter("5")
        self.updateDisplay()

    def Key6Handler(self):
        self.editor.insertCharacter("6")
        self.updateDisplay()

    def Key7Handler(self):
        self.editor.insertCharacter("7")
        self.updateDisplay()

    def Key8Handler(self):
        self.editor.insertCharacter("8")
        self.updateDisplay()

    def Key9Handler(self):
        self.editor.insertCharacter("9")
        self.updateDisplay()

    def KeyParenLeftHandler(self):
        self.editor.insertCharacter("(")
        self.updateDisplay()

    def KeyParenRightHandler(self):
        self.editor.insertCharacter(")")
        self.updateDisplay()

    def KeyCommaHandler(self):
        self.editor.insertCharacter(",")
        self.updateDisplay()

    def KeyPlusHandler(self):
        self.editor.insertCharacter("+")
        self.updateDisplay()

    def KeyMinusHandler(self):
        self.editor.insertCharacter("-")
        self.updateDisplay()

    def KeyAsteriskHandler(self):
        self.editor.insertCharacter("*")
        self.updateDisplay()

    def KeyPeriodHandler(self):
        self.editor.insertCharacter(".")
        self.updateDisplay()

    def KeySlashHandler(self):
        self.editor.insertCharacter("\\")
        self.updateDisplay()

    def KeyColonHandler(self):
        self.editor.insertCharacter(":")
        self.updateDisplay()

    def KeySemicolonHandler(self):
        self.editor.insertCharacter(";")
        self.updateDisplay()

    def BracketLeftHandler(self):
        self.editor.insertCharacter("[")
        self.updateDisplay()

    def BracketRightHandler(self):
        self.editor.insertCharacter("]")
        self.updateDisplay()


    def EqualHandler(self):
        self.editor.insertCharacter("=")
        self.updateDisplay()


    def GreaterHandler(self):
        self.editor.insertCharacter(">")
        self.updateDisplay()


    def LessHandler(self):
        self.editor.insertCharacter("<")
        self.updateDisplay()


    def QuoteDblHandler(self):
        self.editor.insertCharacter('"')
        self.updateDisplay()


    def QuoteLeftHandler(self):
        self.editor.insertCharacter("'")
        self.updateDisplay()


    def KeyPageUpHandler(self):
        self.editor.pageUp()
        self.updateDisplay()


    def KeyPageDownHandler(self):
        self.editor.pageDown()
        self.updateDisplay()


    def KeyF1Handler(self):
        for characterList in self.editor.editorMatrix:
            print(characterList)
        self.updateDisplay()

    def KeyF2Handler(self):
        #reset the mode and period and duty cycle
        self.editor.clear()
        self.cursorMode = 0
        self.period = 0
        self.dutyCycle = 0.5
        self.editor.cursorMode = 5
        print(self.period)
        self.updateDisplay()

    def KeyF3Handler(self):
        print(self.editor.editorMatrixOutput())
        self.updateDisplay()

    def KeyF4Handler(self):
        self.editor.cursorMode += 1
        if self.editor.cursorMode > 5:
            self.editor.cursorMode = 0
        #self.editor.clear()
        print(self.editor.cursorMode)
        self.updateDisplay()

    def KeyF5Handler(self):
        filename = "C:/Users/NewHaptics01/OneDrive/NewHaptics Shared/HApp/testScripts/NotePadTestScripts/HGG.txt"
        self.editor.loadTxt(filename)
        self.editor.cursorMode = 0
        self.updateDisplay()

    def KeyF6Handler(self):
        filename = "C:/Users/derek/OneDrive/NewHaptics Shared/HapticOS/FC_GUI_API/APIv0.7-Coeus/v0.764-Coeus/testScripts/ArabicNumerals.txt"
        self.editor.loadTxt(filename)
        self.editor.cursorMode = 0
        self.updateDisplay()

    def KeyF7Handler(self):
        filename = "C:/Users/derek/OneDrive/NewHaptics Shared/HapticOS/FC_GUI_API/APIv0.7-Coeus/v0.764-Coeus/testScripts/CityPop.txt"
        self.editor.loadTxt(filename)
        self.editor.cursorMode = 0
        self.updateDisplay()

    def KeyF8Handler(self):
        filename = "C:/Users/derek/OneDrive/NewHaptics Shared/HapticOS/FC_GUI_API/APIv0.7-Coeus/v0.764-Coeus/testScripts/CityArea.txt"
        self.editor.loadTxt(filename)
        self.editor.cursorMode = 0
        self.updateDisplay()

    def KeyF9Handler(self):
        filename = "C:/Users/derek/OneDrive/NewHaptics Shared/HapticOS/FC_GUI_API/APIv0.7-Coeus/v0.764-Coeus/testScripts/History.txt"
        self.editor.loadTxt(filename)
        self.editor.cursorMode = 0
        self.updateDisplay()

    def KeyF10Handler(self):
        filename = "C:/Users/derek/OneDrive/NewHaptics Shared/HapticOS/FC_GUI_API/APIv0.7-Coeus/v0.764-Coeus/testScripts/English.txt"
        self.editor.loadTxt(filename)
        self.editor.cursorMode = 0

    def KeyF11Handler(self):
        filename = "C:/Users/derek/OneDrive/NewHaptics Shared/HApp/testScripts/NotePadTestScripts/fileTutorial.txt"
        self.editor.loadTxt(filename)
        self.editor.cursorMode = 0
        self.updateDisplay()

    def KeyF12Handler(self):
        filename = "C:/Users/derek/OneDrive/NewHaptics Shared/HApp/testScripts/NotePadTestScripts/FileNavigation.txt"
        self.editor.loadTxt(filename)
        self.editor.cursor[1] = 4
        self.editor.cursorMode = 1
        self.updateDisplay()

    def KeyEndHandler(self):
        if self.editor.period < 1000:
            self.editor.period += 10
            print(self.editor.period)
            print("timeLow{}".format(int(self.editor.period * self.editor.dutyCycle)))
        else:
            print("Maximum duty cycle of 1000 reached")
        self.updateDisplay()

    def KeyDeleteHandler(self):
        if self.editor.period > 10:
            self.editor.period -= 10
            print(self.editor.period)
            print("timeLow{}".format(int(self.editor.period * self.editor.dutyCycle)))
        else:
            print("Minimum period of 100 reached")
        self.updateDisplay()



    def KeyShiftHandler(self):
        if self.editor.dutyCycle > 0.15:
            self.editor.dutyCycle -= 0.05
            print(self.editor.dutyCycle)
            print("timeLow{}".format(int(self.editor.period * self.editor.dutyCycle)))
        else:
            print("Minimum duty cycle of 10 reached")
        self.updateDisplay()


    def KeyTabHandler(self):
        if self.editor.dutyCycle <= 1:
            self.editor.dutyCycle += 0.05
            print(self.editor.dutyCycle)
            print("timeLow{}".format(int(self.editor.period * self.editor.dutyCycle)))
        else:
            print("Max duty cycle 90 reached")
        self.updateDisplay()


    def KeyCapsLockHandler(self):
        if self.editor.touchScreenMode:
            # deactivate touch screen mode
            self.editor.touchScreenMode = 0
            print("Touch screen mode deactivated")
        else:
            # activate touch screen mode
            self.editor.touchScreenMode = 1
            print("Touch screen mode activated")
        self.updateDisplay()
