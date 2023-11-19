# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 17:35:39 2020

@author: Derek Joslin
"""

import csv
#from PIL import Image 
#import numpy

#import RomRunner as rr

from PyQt5 import QtWidgets as qw
#from PyQt5 import QtCore as qc

class FileManagement():
    
    def __init__(self, HAppMainWindow):
        self.MainWindow = HAppMainWindow
        print("File Manager Initialized")
        
    def saveFile(self):
        #decide which state to save
        options = qw.QFileDialog.Options()
        options |= qw.QFileDialog.DontUseNativeDialog
        source = qw.QFileDialog.getSaveFileName(self.MainWindow,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)[0]
        self.saveCsv(source,self.MainWindow.BrailleDisplay.return_desiredState())
        
    def loadFile(self):
        #navigate to the Roms folder
        self.MainWindow.HAppControlCenter.PathManager.makeCWD("ROMs")
        
        options = qw.QFileDialog.Options()
        options |= qw.QFileDialog.DontUseNativeDialog
        source = qw.QFileDialog.getOpenFileName(self.MainWindow,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)[0]
        if source[-4:-1] == ".cs":
            matData = self.openCsv(source)
            #format the matData properly from strings into ints
            return [[int(i) for i in row] for row in matData]
        elif source[-4:-1] == ".pn":
            matData = self.openPng(source,self.MainWindow.BrailleDisplay.return_displaySize())
            #format the matData properly from strings into ints
            return [[int(i) for i in row] for row in matData]
        elif source[-4:-1] == ".ro":
            self.openRom(source)
            return
        else:
            return
    
    
    def openTxt(self, filename):
    # =============================================================================
    #     print(repr(open(filename, 'rb').read(200))) # dump 1st 200 bytes of file
    #     data = open(filename, 'rb').read()
    #     print(data.find('\x00'))
    #     print(data.count('\x00'))
    # =============================================================================
        d = {}
        with open(filename, 'rt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            for row in csv_reader:
                d[row[0]] = row[1:]
        return d
        
    def openCsv(self, filename):
    # =============================================================================
    #     print(repr(open(filename, 'rb').read(200))) # dump 1st 200 bytes of file
    #     data = open(filename, 'rb').read()
    #     print(data.find('\x00'))
    #     print(data.count('\x00'))
    # =============================================================================
        d = []
        with open(filename, 'rt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                d.append(row)
        return d
    
# =============================================================================
#     def openPng(self, filename,size):
#         with Image.open(filename) as p:
#             print(p.format)
#             print(p.mode)
#             print(p.size)
#             p = p.resize(size,Image.ANTIALIAS)
#             pix = (numpy.array(p)).tolist()
#             #go through image and convert all lists in list to black and white
#             for (i,row) in enumerate(pix):
#                 for (j,RGB) in enumerate(row):
#                     if p.mode == "RGBA":
#                         if RGB[3] > 100:
#                             pix[i][j] = 1
#                         else:
#                             pix[i][j] = 0
#                     else:
#                         if (sum(RGB)/3) < 250:
#                             pix[i][j] = 1
#                         else:
#                             pix[i][j] = 0
#             print(pix)
#             return pix
# =============================================================================
        
        
        
    def openRom(self, filename):
        """Read in tactile roms"""
        
        #filename = 'C:/Users/derek/OneDrive/NewHaptics Shared/HapticOS/FC_GUI_API/APIv0.7-Coeus/v0.762-Coeus/ROMs/NotePad/NotePadReady.rom'
        
        self.MainWindow.initializeRom(filename)
        
    def saveCsv(self, filename, mat):
        
        with open(filename, "w") as f:
            for row in mat:
                for (i,elem) in enumerate(row):
                    if elem == True:
                        f.write("{0}".format(1))
                    elif elem == False:
                        f.write("{0}".format(0))
                    if i is not len(row) - 1:
                        f.write(",")
                f.write("\n")
        f.close()
            
# =============================================================================
#         thisRom = rr.RomReader(filename)
#         romSettings = thisRom.getSettings()
#         romComments = thisRom.getDescriptions()
#         
#         def startRom(romSettings,romSettingsKeys):
#             for romSetting in romSettingsKeys:
#                 romSettings[romSetting] = romSettingQLineInputs[romSetting].text()
#             thisRom.setSettings(romSettings)
#             romState = thisRom.executeRom()
#             romStateWindow = qw.QDialog()
#             romStateWindow.setWindowTitle(str(romState))
#             romStateWindow.exec_()
#             
#             
#         def endRom(thisRom):
#             thisRom.endRom()
#             #thisRom = rr.romReader(filename)
#         
#         #open pop up menu to select desired settings
#         romSettingsWindow = qw.QDialog()
#         romSettingsWindow.setWindowTitle("rom settings window")
#         settingInputLocationX = 0
#         settingInputLocationY = 0
#         romSettingQLineInputs = {}
#         romSettingKeys = list(romSettings.keys())
#         for (i,romSetting) in enumerate(romSettingKeys):
#             #create qt label for setting
#             romSettingLabel = qw.QLabel(romSetting,romSettingsWindow)
#             romSettingLabel.move(settingInputLocationX,settingInputLocationY)
#             romSettingComment = qw.QLabel(romComments[i],romSettingsWindow)
#             romSettingComment.move(settingInputLocationX,settingInputLocationY + 25)
#             
#             #create input box for setting
#             romSettingQLineInputs[romSetting] = qw.QLineEdit(romSettings[romSetting],romSettingsWindow)
#             romSettingQLineInputs[romSetting].move(settingInputLocationX + 100,settingInputLocationY)
#             
#             settingInputLocationY += 50
#         
#         #create execute rom button
#         executeRomButton = qw.QPushButton("Execute Rom", romSettingsWindow)
#         executeRomButton.move(settingInputLocationX,settingInputLocationY)
#         
#         executeRomButton.clicked.connect(lambda:startRom(romSettings,romSettingKeys))
#         
#         #create end rom button
#         endRomButton = qw.QPushButton("End Rom", romSettingsWindow)
#         endRomButton.move(settingInputLocationX + 100,settingInputLocationY)
#         
#         endRomButton.clicked.connect(lambda:endRom(thisRom))
#         
#         """
#         print(romSettings)
#         
#         romSettings = {romSettingsKeys[0]: "COM3",
#                         romSettingsKeys[1]: 4,
#                         romSettingsKeys[2]: 1}
#         """
#         romSettingsWindow.exec_()
#         
# =============================================================================
