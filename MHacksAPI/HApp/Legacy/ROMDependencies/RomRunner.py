# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 11:13:11 2022

@author: Derek Joslin
"""

from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc

import NewKeyboardHandles as nkh
import NewRomVisualizationHandles as nrv
import BasicRomVisualizationHandles as brh

#import TextEditor as te

import RomReader as rr
import RomVisualization as rv

import time


class RomRunner():
    
    def __init__(self, OperationsController):
        
        #An instance of the haptics engine will already exist
        self.OperationsController = OperationsController
        self.NewKeyboardHandles = nkh.NewKeyboardHandles()
        
        #self.Editor = te.TextEditor()
        
        
    def getRomData(self, filename):
        self.ThisRom = rr.RomReader(filename)
        
        self.interruptDictionary = self.ThisRom.createInterruptDictionary()
        self.romSettings = self.ThisRom.getSettings()
        self.romComments = self.ThisRom.getDescriptions()
        
        #need to ask rom how it wants to be displayed
        #TBD
        
        
    def passValuesToRom(self):
        OperationsControlAddress = id(self.OperationsController)
        self.romSettings['OperationsControlAddress'] = OperationsControlAddress
        self.ThisRom.setSettings(self.romSettings)
        
        
    def startRom(self):
        
        #create the visualization for the rom and pass in the required values
        #self.TextEditor = BrailleEdit(self.BrailleDisplay)
        self.OperationsController.KeyboardHandler.setNewKeyboardHandler(self.NewKeyboardHandles)
        

        self.ThisRom.setSettings(self.romSettings)
        
        self.ThisRom.executeRom()
        
        self.RomVisualization = rv.RomVisualization(self.interruptDictionary)
        
        self.OperationsController.setVisualization("RomVisualization" ,self.RomVisualization.VisualizationHandler)
        
        self.NewRomVisualizationHandles = brh.BasicRomVisualizationHandles(self.interruptDictionary, self.RomVisualization.RomExplorer)
        self.OperationsController.setVisualizationHandler("RomVisualization", self.NewRomVisualizationHandles)
        #self.ViewUpdater = RomViewUpdater(self)
        
        #self.TextEditor.show()
        
        self.RomVisualization.show()
        #self.RomVisualization.controlDialog.show()


#create a note pad for running functions takes in text as a pyqt script
class BrailleEdit(qw.QTextEdit):
    
    def __init__(self):
        super().__init__()
        #fixedWidth = qt.QReal
        
        #self.setLineWrapColumnOrWidth(20)
        #self.setFixedWidth(20)
        courierFont = qg.QFont("Courier")
        courierFont.setPointSize(800)
        self.setFont(courierFont)
        self.show()
        
        #self.setPageSize(qc.QSize(200, 200))
        #self.engine = engine
        
# =============================================================================
#         
#         
#     def getCursorPosition(self):
#         textCursor = self.textCursor()
#         startLine = qg.QTextCursor.StartOfLine
#         moveDown = qg.QTextCursor.Down
#         
# # =============================================================================
# #         if textCursor.columnNumber() > 13:
# #             #insert new line
# #             self.insertPlainText("\n")
# #             self.moveCursor(startLine, qg.QTextCursor.MoveAnchor)
# #             self.moveCursor(moveDown, qg.QTextCursor.MoveAnchor)
# # =============================================================================
#             
#         testText = self.toPlainText()
#         
#         #go through the text  and count the number of rows
#         splitText = testText.split("\n")
#         documentPosition = textCursor.position()
#         blockNumber = textCursor.blockNumber()
#         documentPositionWithoutBlocks = documentPosition - blockNumber
# 
#         totChar = 0
#         nChar = 0
#         nRows = 0
#         for characterList in splitText:
#             for character in characterList:
#                 if nChar > 14:
#                     nRows = nRows + 1
#                     nChar = 0
#                 else:
#                     nChar = nChar + 1
#                 totChar = totChar + 1
#                 if (documentPosition - blockNumber) == totChar:
#                     print(nRows)
#                     break
#             if (documentPosition - blockNumber) == totChar:
#                 break
#             nRows = nRows + 1
# 
#                     
#         #print(nRows)
# # =============================================================================
# #         documentPosition = textCursor.position()# - textCursor.blockNumber())
# #         blockNumber = textCursor.blockNumber()
# #         
# #         #documentPosition + blockNumber*x
# #         
# #         print(documentPosition)
# #         print(blockNumber)
# #         
# #         documentPositionWithoutBlocks = documentPosition - blockNumber
# #         
# #         print(documentPositionWithoutBlocks)
# #         
# #         print(documentPositionWithoutBlocks/14)
# #         print(int(documentPositionWithoutBlocks/14))
# # =============================================================================
#         
#         xPinPosition = textCursor.columnNumber()
#         
#         yPinPosition = nRows
#         
#         return (xPinPosition,yPinPosition)
#             
#     
#     def changeCursorLocation(self, x):
#         #get the start of the line and move between start and end
#         endLine = qg.QTextCursor.EndOfLine
#         startLine = qg.QTextCursor.StartOfLine
#         moveRight = qg.QTextCursor.Right
#         moveLeft = qg.QTextCursor.Left
#         
#         self.moveCursor(startLine)
#         
#         for i in range(0,x):
#             self.moveCursor(moveRight, qg.QTextCursor.MoveAnchor)
#             
# # =============================================================================
# #         tempCursor = self.textCursor
# #         tempCursor.setPosition(5, qg.QTextCursor.Left, qg.QTextCursor.MoveAnchor)
# #         self.setTextCursor(tempCursor)
# # =============================================================================
#         
#         
#         #when the text changes run the braille command with that text
#         
#         
# =============================================================================
        
    
#read in a rom and create a nhapi and have them running and displaying to the output at the same time
# =============================================================================
# 
# if __name__ == '__main__':
#     
#     
#     app = qw.QApplication([])
#     
#     RomStarter = RomRunner()
#     
#     filename = 'C:/Users/derek/OneDrive/NewHaptics Shared/HapticOS/FC_GUI_API/APIv0.7-Coeus/v0.758-Coeus/ROMs/sampleAPIImplementationReady.rom'
#     
#     RomStarter.getRomData(filename)
# 
#     RomStarter.passValuesToRom()
#     
#     RomStarter.startRom()
#     
#     sys.exit(app.exec_())
# =============================================================================
    

    