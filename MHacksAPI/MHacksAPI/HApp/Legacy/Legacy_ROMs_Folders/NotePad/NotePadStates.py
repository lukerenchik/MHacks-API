# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 15:11:53 2022

@author: Derek Joslin
"""

import RomAPI as rs
import NotePadOperations as no
import NotePadEditor as ne
#import RomRunner as rr


class NotePadStartMenu(rs.RomState):
    
    def __init__(self, Controller):
        #user can make custom state intialization 
        super().__init__(Controller)

    def stepState(self):
        #redefined by user in the appropriate subclass
        #print('state running')
        pass
    
    def startState(self):
        #display the start screen
        #self.Controller.addEngineFunction(self.bootMenu)
        print('Start Menu Began')
        
    def closeState(self):
        #clear the screen of all information and shut down start screen processes
        print('Start Menu Close')


    def getNextState(self):
        #get values for the truth table
        romContinue = self.Controller.getInterruptFlagTrigger('romContinue')
        romEscape = self.Controller.getInterruptFlagTrigger('romEscape')
        
        #truth table for start Menu
        if romContinue:
            #exit the current state and rom entirely 
            
            return 'Text Editor'
        
        elif romEscape:
            
            print("hi")
            
            return 'Start Menu'
        
        else:
            #continue with program execution
        
            return 'Start Menu'
        
class NotePadTextEditor(rs.RomState):
    
    def __init__(self, Controller):
        #user can make custom state intialization 
        super().__init__(Controller)
        self.BrailleDisplay = self.Controller.OperationsController.BrailleDisplay
        self.displayText = ""

        #self.counter = 0

    def stepState(self):
        #redefined by user in the appropriate subclass
        #print('Editor running')
        if len(self.TextEditor.inputCommand) > 0:
            try:        
                output = self.Controller.OperationsController.matlabEvaluate(self.TextEditor.inputCommand)
                print(output)
            except:
                print("failed to execute matlab operation")
            self.TextEditor.inputCommand = ""
            
        else:
            pass
            
            
    def startState(self):
        #create a text editor object for this state
        print('Text Editor Begin')
        self.Controller.OperationsController.pauseExecutingOperations()
        #create a braille edit gui
        #self.NotePadGUI = rr.BrailleEdit()
        
        #get the size of the Braille Display
        displaySize = self.BrailleDisplay.return_displaySize()
        nRows = displaySize[0]
        nColumns = displaySize[1]
        self.TextEditor = ne.NotePadEditor(nRows, nColumns)
        self.Controller.OperationsController.KeyboardHandler.setNewKeyboardHandler(self.TextEditor.KeyboardHandles)
        
        
        #create an operation that tracks the editor cursor and decides where it is
        #to do
        
        #create an operation that blinks the cursor of the Braille Display
        self.BlinkCursorOperation = no.BlinkCursorOperation(self.Controller, self.TextEditor)
        self.Controller.OperationsController.setOperation("BlinkCursorOperation", self.BlinkCursorOperation)
        
        #create an operation that decides when to send the desired state over the serial port
        self.BrailleDisplayRefreshOperation = no.BrailleDisplayRefreshOperation(self.Controller.OperationsController.BrailleDisplay)
        self.Controller.OperationsController.setOperation("BrailleDisplayRefreshOperation", self.BrailleDisplayRefreshOperation)
        
        self.Controller.OperationsController.resumeExecutingOperations()
        
        
    def closeState(self):
        #clear the screen of all information and shut down start screen processes
        #close the operation
        
        
        print('End Menu Close')

    def getNextState(self):
        #get values for the truth table
        romContinue = self.Controller.getInterruptFlagTrigger('romContinue')
        romEscape = self.Controller.getInterruptFlagTrigger('romEscape')
        
        #truth table for start Menu
        if romContinue:
            #exit the current state and rom entirely 
            
            return 'Start Menu'
        
        elif romEscape:
            
            return 'Exit Rom'
            
        else:
            #continue with program execution
        
            return 'Text Editor'
        
class NotePadExitState(rs.RomState):
    
    def __init__(self, Controller):
        #user can make custom state intialization 
        super().__init__(Controller)

    def stepState(self):
        #redefined by user in the appropriate subclass
        #print('state running')
        #print('Exit State Print')
        pass
        #print("disconnected")
    
    def startState(self):
        #display the start screen
        #self.Controller.addEngineFunction(self.bootMenu)
        print('Exit State Began')
        
        
    def closeState(self):
        #clear the screen of all information and shut down start screen processes
        print('Exit State Close')


    def getNextState(self):
        #get values for the truth table
        self.Controller.setInterruptFlag('romEnd',1)
        
        return 'Exit Rom'
    
# =============================================================================
#     
# class TextEditorUpdater():
#         
#     def __init__(self, Controller):
#         self.Controller = Controller
#         self.Controller.TextEditor.textChanged.connect(lambda: self.startTextChangeTimer())
#         self.Controller.TextEditor.cursorPositionChanged.connect(lambda: self.cursorLocationChanged())
#         self.textChangeTimer = None
#         self.cursorBlinker = 0
#         self.displayText = ""
#         self.Editor = Controller.Editor
#         qc.QTimer.singleShot(1000, self.startRomViewUpdater)
#         
#         
#     def startRomViewUpdater(self):
#         # starts a timer which determines how to update the current view
#         self.RomViewUpdaterTimer = qc.QTimer()
#         self.RomViewUpdaterTimer.setInterval(50)
#         self.RomViewUpdaterTimer.timeout.connect(self.updateRomView)
#         self.RomViewUpdaterTimer.start()
# 
#     def stopRomViewUpdater(self):
#         self.RomViewUpdaterTimer.stop()
#         
# 
#     def updateRomView(self):
#         self.stopRomViewUpdater()
#         
#         #grab the text from the qLine edit
#         #displayText = self.Controller.TextEditor.toPlainText()
#         
# # =============================================================================
# #         toc = time.perf_counter()
# #         print(toc - tic)
# #         tic = toc
# # =============================================================================
#         
# 
# # =============================================================================
# #         toc = time.perf_counter()
# #         print(toc - tic)
# #         tic = toc
# # =============================================================================
#         #update the cursor position to the text editor position
#         #print(self.Editor.cursor)
#         
#         #print((self.Editor.cursor[0],self.Editor.cursor[1]))
#         
# # =============================================================================
# #         self.Controller.RomVisualization.grabFirmwareState()
# # =============================================================================
# # =============================================================================
# #         toc = time.perf_counter()
# #         print(toc - tic)
# #         tic = toc
# # =============================================================================
# # =============================================================================
# #         #get the touch screen position
# #         self.Controller.TextEditor.cursorPosition = self.Controller.BrailleDisplay.getPinCursorPosition()
# #         print(self.Controller.TextEditor.cursorPosition)
# #         
# #         
# #         #get the cursor from the display and move the text edit cursor to that location
# #         self.TextEditor.changeCursorLocation(self.TextEditor.cursorPosition[0])
# #         
# # =============================================================================
#         
#         self.startRomViewUpdater()
#         
#     def startTextChangeTimer(self):
#         #if there is already a timer stop it and start a new one
#         if self.textChangeTimer is None:
#             self.textChangeTimer = qc.QTimer.singleShot(5, self.textChangeFunction)
#         else:
#             self.stopTextChangeTimer()
#             self.textChangeTimer = qc.QTimer.singleShot(5, self.textChangeFunction)
#         
#     def stopTextChangeTimer(self):
#         dispatcher = qc.QAbstractEventDispatcher.instance()
#         dispatcher.unregisterTimers(self.textChangeTimer)
#         self.textChangeTimer = None        
#         
#     def textChangeFunction(self):
#         self.stopRomViewUpdater()
#         #print("text change test")
#         #self.reformatToDisplay()
#         self.displayText = self.Controller.TextEditor.toPlainText()
#         
#         editorBox = self.Editor.editorBoxFormatter(self.displayText)
#         
#         #print(self.displayText)
#         
#         #send the display text
#         
#         #self.Controller.BrailleDisplay.braille((0,0),self.displayText)
#         #self.Controller.BrailleDisplay.refresh()
#         #print(displayText)
#         self.updateRomView()
#         
#         self.stopTextChangeTimer()
# 
#         self.startRomViewUpdater()
#         
#     def reformatToDisplay(self):
#         TextCursor = self.Controller.TextEditor.textCursor()
#         
#         #get the cursor position
#         position = self.Controller.TextEditor.getCursorPosition()
#         
#         moveDown = qg.QTextCursor.Down
#         
#         oldText = self.Controller.TextEditor.toPlainText()
#             
#         self.displayText = self.Controller.TextEditor.toPlainText()
#         
#         
#         #self.displayText = self.displayText.replace("\n","")
#         
#         #print(self.displayText)
#         #go through text and add carraige every 13 characters
#         newText = self.stringReformatter(self.displayText)
# 
# # =============================================================================
# #             
# #         self.displayText = newText
# #         self.Controller.TextEditor.textChanged.disconnect()
# #         self.Controller.TextEditor.clear()
# #         self.Controller.TextEditor.setPlainText(self.displayText)
# #         self.Controller.TextEditor.textChanged.connect(lambda: self.textChangeFunction())
# # =============================================================================
#         
#         start = qg.QTextCursor.Start
#         moveRight = qg.QTextCursor.Right
#         moveDown = qg.QTextCursor.Down
#         self.Controller.TextEditor.moveCursor(start, qg.QTextCursor.MoveAnchor)
#         
#        
#         for y in range(0,position[1]):
#             self.Controller.TextEditor.moveCursor(moveDown)
#             
#         isCharacter = 1
#         #if delete do not move right one
#         if len(oldText) > len(self.displayText):
#             isCharacter = -1
#         else:
#             isCharacter = 1
#             
#         for x in range(0,position[0] + isCharacter):
#             self.Controller.TextEditor.moveCursor(moveRight, qg.QTextCursor.MoveAnchor)
#                 
#         #insert new line
#         #self.Controller.TextEditor.insertPlainText("\n")
#         #self.Controller.TextEditor.moveCursor(startLine, qg.QTextCursor.MoveAnchor)
#         #self.Controller.TextEditor.moveCursor(moveDown, qg.QTextCursor.MoveAnchor)
#         
#         #self.displayText = self.Controller.TextEditor.toPlainText()
#         
#     def stringReformatter(self,testText):
#         
# 
#         #go through text and add carraige every 13 characters
#         newText = ""
#         parseText = testText.split("\n")
#         nChar = 0
#         
#         for characterList in parseText:
#             #print(characterList)
#             nChar = 0
#             for character in characterList:
#                 #if list greater than length of braille display than add \n
#                 nChar = nChar + 1
#                 if nChar%14 == 0:
#                     
#                     newText = newText + "\n" + character
#                     nChar = nChar + 1
#                 else:
#                     newText = newText + character
#             
#             newText = newText + "\n"
# 
#         newText = newText[0:-1]
#         return newText
#         
#     def cursorLocationChanged(self):
#         
#         characterPosition = self.Controller.TextEditor.getCursorPosition()
#         #print(characterPosition)
#         #convert the character position into a pin cursor position
#         characterHeight = 4
#         characterWidth = 3
#         #print(characterPosition)
#         xPinPosition = characterPosition[0]*characterWidth
#         yPinPosition = characterPosition[1]*characterHeight
#         pinPosition = (xPinPosition,yPinPosition)
#         
#         self.Controller.BrailleDisplay.setPinCursorPosition(pinPosition)
#         
#         
#     def startAllOtherTimers(self):
#         pass
#         
#     def stopAllOtherTimers(self):
#         pass
#         
#     
#     
#     
#     
#     
#     
# =============================================================================
    