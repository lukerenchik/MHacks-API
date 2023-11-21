# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 15:12:55 2022

@author: Derek Joslin
"""

import RomAPI as rs
import time

class TactileDisplayRefreshOperation(rs.RomOperation):

    def __init__(self, name, TactileDisplay, TextEditor):
        super().__init__(name)

        # inputs to the operation
        self.TextEditor = TextEditor
        self.inputDictionary["Text Editor"] = self.TextEditor

        # outputs to the operation
        self.TactileDisplay = TactileDisplay
        self.outputDictionary[self.TactileDisplay.name] = self.TactileDisplay

        # provide a description
        self.description = "This operation refreshs the display when keys are typed. It's execution is interupt based."

        self.executable = self.execute

        self.createDebugString()


    def execute(self):
        self.TactileDisplay.braille((0,0),self.TextEditor.editorMatrixOutput())

        self.TactileDisplay.refresh()

# =============================================================================
#     def checkFlagConditions(self):
#         # grab the state of DisplayFlag
#         displayState = self.DisplayFlag.state
#
#         # get the current state of the tactile display
#         if displayState:
#             # compare the flag matrix to the current state of the Tactile Display
#             return True
#         else:
#             # if they are not the same then return false
#             return False
# =============================================================================

# =============================================================================
# class GetTouchScreenOperation(rs.RomOperation):
#
#     def __init__(self, Controller, Editor):
#         super().__init__()
#         self.Controller = Controller
#         self.TactileDisplay = self.Controller.HAppControlCenter.TactileDisplay
#         self.TextEditor = Editor
#         self.BrailleCellColumn = 0
#         self.BrailleCellRow = 0
#         self.touchScreenTimer = 0
#
#     def stopOperation(self):
#         self.operationOn = 0
#
#     def execute(self):
#         if self.operationOn:
#             self.getTouchScreenCursor()
#
#
#     def getTouchScreenCursor(self):
#         #check the position of the touch screen
#         if self.touchScreenTimer > 50:
#             self.touchScreenTimer = 0
#
#             pinCursor = self.TactileDisplay.getPinCursorPosition()
#
#             #print("Old Touch Screen Braille Position {0},{1}".format(self.BrailleCellColumn, self.BrailleCellRow))
#
#             newBrailleCellColumn = int((pinCursor[1] + 1)/3)
#             newBrailleCellRow = int((pinCursor[0] + 1)/4)
#
#             if newBrailleCellRow == 5:
#                 newBrailleCellRow = 4
#
#             #print("New Touch Screen Braille Position {0},{1}".format(newBrailleCellColumn, newBrailleCellRow))
#
#
#             #if the touch screen position is different than the text editor position set text editor to touch screen position
#             if (self.BrailleCellRow != newBrailleCellRow or self.BrailleCellColumn != newBrailleCellColumn) and self.TextEditor.touchScreenMode :
#
#                 self.BrailleCellColumn = newBrailleCellColumn
#                 self.BrailleCellRow = newBrailleCellRow
#
#                 #set the TextEditor y position to the touch position
#                 self.TextEditor.cursor[1] = self.BrailleCellRow + self.TextEditor.boundingBox[0]
#                 self.TextEditor.cursor[0] = self.BrailleCellColumn
#                 print("New Braille Position {0}".format(self.BrailleCellRow))
#                 print("New Editor Position {0}".format(self.TextEditor.cursor[1]))
#                 print("New Pin Position {0}".format(pinCursor[0]))
#
#         else:
#             self.touchScreenTimer += 1
# =============================================================================



class BlinkCursorOperation(rs.RomOperation):

    def __init__(self, name, Controller, Editor):
        super().__init__(name)
        self.createDebugString()
        self.HAppControlCenter = Controller.HAppControlCenter
        self.cursorBlinker = 0

        # inputs to the operation
        self.TextEditor = Editor
        self.outputDictionary["Text Editor"] = self.TextEditor

        # outputs to the operation
        self.TactileDisplay = Controller.HAppControlCenter.getPeripheral("NewHaptics Display SarissaV1")
        self.outputDictionary[self.TactileDisplay.name] = self.TactileDisplay

        # provide a description
        self.description = "This operation refreshs the display when keys are typed."

        # execute the function continuously until otherwise
        executionParameters = {
            "executeDelay": 0, # a delay in milliseconds that starts the execution of the Operation after the flag dependencies have been met
            "executeContinuously": True, # a boolean value that determines if the Operation will execute forever
            "executionIntervalTime": 1, # an interval in milliseconds that determines the time between execution
        }

        self.setExecutionParameters(executionParameters)

        self.executable = self.execute

        self.createDebugString()

    def execute(self):
        # just print the text editor output to see if the limitation is on rom side
        self.cursorBlink()
        self.TactileDisplay.refresh()

        # update the description with the state of the text editor
        cursorString = "Cursor Location: {}".format(self.TextEditor.cursor)
        cursorLimiterString = "Cursor Limiter: {}".format(self.TextEditor.cursorLimiter)
        editorString = "Editor String: {}".format(self.TextEditor.editorMatrix)
        editorBoxString = "Editor Box: {}".format(self.TextEditor.editorBox)

        self.description = cursorString + "\n" + cursorLimiterString + "\n" + editorString + "\n"  + editorBoxString
        self.createDebugString()

    def cursorBlink(self):
        #check the position of the text editor
        cellXPosition = self.TextEditor.cursor[0]
        cellYPosition = self.TextEditor.cursor[1] - self.TextEditor.boundingBox[0]

        brailleXPosition = cellXPosition*3
        brailleYPosition = cellYPosition*4

        pinPosition = (brailleXPosition,brailleYPosition)

        self.TactileDisplay.setPinCursorPosition(pinPosition)

        #when cursor location moves outside of bounding box switch bounding box location
        pinCursor = self.TactileDisplay.grabPinCursor()

        #control refresh
# =============================================================================
#         if self.displayString != self.TextEditor.editorMatrixOutput():
#             self.displayString = self.TextEditor.editorMatrixOutput()
#             self.Controller.HAppControlCenter.restartExecutingOperation("TactileDisplayRefreshOperation")
#
# =============================================================================

        try:
            self.renderCursor(pinCursor, self.TextEditor.period, self.TextEditor.dutyCycle)
        except:
            print("unable to render cursor")

        self.cursorBlinker += 1

    def renderCursor(self, pinCursor, period, dutyCycle): #, period, dutyCycle

# =============================================================================
#         #make the pin cursor position blink
#         if self.cursorBlinker == 100:
#             self.cursorBlinker = 0
#             self.TactileDisplay.braille((0,0),self.TextEditor.editorMatrixOutput())
#
#             #turn the cursor on
#             self.cursorOn(pinCursor)
#
#
#         elif self.cursorBlinker == 50:
#             self.TactileDisplay.braille((0,0),self.TextEditor.editorMatrixOutput())
#
#             #turn the cursor off
#             self.cursorOff(pinCursor)
#
#
#             self.Controller.HAppControlCenter.restartExecutingOperation("TactileDisplayRefreshOperation")
#
# =============================================================================
        self.cursorBlinker = 0
        self.TactileDisplay.braille((0,0), self.TextEditor.editorMatrixOutput())


        #turn the cursor on
        self.cursorOn(pinCursor)

        #calculate the number of times the cursor should blink
        #numBlinks = period // dutyCycle
        #print(numBlinks)
        # timeLow = int(period * dutyCycle)
        #
        # #make the pin cursor position blink
        # if self.cursorBlinker > period:
        #     #print(self.cursorBlinker)
        #     self.cursorBlinker = 0
        #     self.TactileDisplay.braille((0,0),self.TextEditor.editorMatrixOutput())
        #
        #     #turn the cursor on
        #     self.cursorOn(pinCursor)
        #
        # elif self.cursorBlinker == timeLow:
        #     #print(self.cursorBlinker)
        #     self.TactileDisplay.braille((0,0),self.TextEditor.editorMatrixOutput())
        #     self.cursorOff(pinCursor)


            #restart the refresh operation
            #self.Controller.HAppControlCenter.restartExecutingOperation("TactileDisplayRefreshOperation")


    def cursorOn(self, pinCursor):

        if self.TextEditor.cursorMode == 0:
            #just blink the cursor like normal
            self.TactileDisplay.rect((pinCursor[1],pinCursor[0]),(pinCursor[1] + 3,pinCursor[0] + 1))


        elif self.TextEditor.cursorMode == 1:
            #force cursor to left side
            self.TactileDisplay.rect( (pinCursor[1], 0), (pinCursor[1] + 3, 1) )


        elif self.TextEditor.cursorMode == 2:
            #force cursor to left unblinking
            self.TactileDisplay.rect( (pinCursor[1], 0), (pinCursor[1] + 3, 1) )



        elif self.TextEditor.cursorMode == 3:
            #blink line 1
            self.TactileDisplay.rect( (pinCursor[1], 0), (pinCursor[1] + 3, 1)  )


        elif self.TextEditor.cursorMode == 4:
            #blink line 0
            self.TactileDisplay.rect( (pinCursor[1], 0), (pinCursor[1] + 3, 1) )



        elif self.TextEditor.cursorMode == 5:
            self.TactileDisplay.erase("on")
            self.TactileDisplay.dot((pinCursor[1], pinCursor[0]))
            self.TactileDisplay.dot((pinCursor[1] + 1, pinCursor[0]))
            self.TactileDisplay.dot((pinCursor[1], pinCursor[0] + 1))
            self.TactileDisplay.dot((pinCursor[1] + 1, pinCursor[0] + 1))
            self.TactileDisplay.erase("off")
            self.TactileDisplay.dot((pinCursor[1] + 2, pinCursor[0]))
            self.TactileDisplay.dot((pinCursor[1] + 2, pinCursor[0] + 1))

        else:
            #just blink the cursor like normal
            self.TactileDisplay.rect((pinCursor[1],pinCursor[0]),(pinCursor[1] + 3,pinCursor[0] + 1))


    def cursorOff(self, pinCursor):

        if self.TextEditor.cursorMode == 0:
            #just blink the cursor like normal
            pass

        elif self.TextEditor.cursorMode == 1:
            #force cursor to left side
            pass

        elif self.TextEditor.cursorMode == 2:
            #force cursor to left unblinking
            self.TactileDisplay.rect( (pinCursor[1], 0), (pinCursor[1] + 3, 1) )

        elif self.TextEditor.cursorMode == 3:
            #blink line 1
            self.TactileDisplay.rect( (pinCursor[1], 0), (pinCursor[1] + 3, 1) )
            self.TactileDisplay.fill("on")
            self.TactileDisplay.rect( (pinCursor[1], 0), (pinCursor[1] + 3, 41) )
            self.TactileDisplay.fill("off")


        elif self.TextEditor.cursorMode == 4:
            #blink line 0

            self.TactileDisplay.erase("on")
            self.TactileDisplay.fill("on")
            self.TactileDisplay.rect( (pinCursor[1], 3), (pinCursor[1] + 3, 41) )
            self.TactileDisplay.fill("off")
            self.TactileDisplay.rect( (pinCursor[1], 3), (pinCursor[1] + 3, 41) )
            self.TactileDisplay.erase("off")
            self.TactileDisplay.rect( (pinCursor[1], 0), (pinCursor[1] + 3, 1) )

        elif self.TextEditor.cursorMode == 5:
            pass

        else:
            pass


class DisplayFlag(rs.RomFlag):

    def __init__(self, name):
        super().__init__(name)
        self.debugString = "This flag indicates to send the state"
        self.matrix = 0

    def clearState(self):
        super().clearState()
        self.matrix = 0

    def setMatrix(self, state):
        self.matrix = state
