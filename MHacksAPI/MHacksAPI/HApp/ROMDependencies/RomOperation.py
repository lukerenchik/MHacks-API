# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 14:13:09 2022

@author: Derek Joslin

"""

import OperationsManager as om

import RomReader as rre
import RomRunner as rru
import RomVisualization as rv

""" Operation responsible for starting rom """

class RomOperation(om.Operation):
    
    def __init__(self, name, ControlCenter, filename, PathManager):
        
        super().__init__(name)
        
        self.RomStarter = rru.RomRunner(ControlCenter)
        self.RomStarter.getRomData(filename)
        self.romSettings = self.RomStarter.ThisRom.getSettings()
        self.romComments = self.RomStarter.ThisRom.getDescriptions()
        self.romSettingsKeys = list(self.romSettings.keys())
        self.filename = filename
        self.HAppPathManager = PathManager
        
    def execute(self):
        
        self.defaultHappOperation()

# =============================================================================
#     def delayedExecute(self):
#         
#         self.singleShot(10, self.defaultHappOperation())
# 
# =============================================================================
    def startOperation(self, romSettingQLineInputs):
        
        #starts the HApp operation
        self.startRom(romSettingQLineInputs)

    def stopOperation(self):
        
        #stops the HApp operation
        
        self.endRom()

# =============================================================================
#     def pauseOperation(self):
#         
#         #pauses the HApp operation
#         pass
#         
#     def restartOperation(self):
#         
#         pass
#         
# =============================================================================
        
    def defaultHappOperation(self):
        print("this is the Rom Operation")
        
        
    def startRom(self, romSettingQLineInputs):
        
        for romSettingKey in self.romSettingsKeys:
            if romSettingKey == "interruptDictionaryAddress" or romSettingKey == "OperationsControlAddress":
                pass
            else:
                self.romSettings[romSettingKey] = romSettingQLineInputs[romSettingKey].text()
                
        self.RomStarter.passValuesToRom()
        #add the rom to the python path
        fileFolderList = self.filename.split("/")

        folderDirectory = ""

        for folder in fileFolderList[:-1]:
            folderDirectory = folderDirectory + folder + "//"
        
        self.HAppPathManager.addDirectory(folderDirectory)
        self.RomStarter.startRom()
        
        
    def endRom(self):
        self.RomStarter.ThisRom.endRom()
        #thisRom = rr.romReader(filename)