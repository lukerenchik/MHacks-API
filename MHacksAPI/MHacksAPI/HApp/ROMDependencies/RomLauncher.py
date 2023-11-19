# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 10:52:11 2023

@author: Derek Joslin

"""

import RomReader as rr
import RomVisualization as rv


class RomLauncher(rr.RomReader):
    
    def __init__(self, romFilePath, HAppControlCenter):
        super().__init__(romFilePath)
        
        # save the path to the rom file
        self.romFilePath = romFilePath
        
        # add the HApp control center to the class
        self.HAppControlCenter = HAppControlCenter
        
        # add the Roms containing folder to the python path
        self.addROMFolderToPath()
        
        # get the ROMs settings and description
        self.interruptDictionary = self.createInterruptDictionary()
        
        # load the address of the Control center into the rom settings
        OperationsControlAddress = id(self.HAppControlCenter)
        self.romSettings['OperationsControlAddress'] = OperationsControlAddress
        

    def startRom(self):
        # passes all necessary values to the rom in order to start it
        self.setSettings(self.romSettings)
        
        self.RomVisualization = rv.RomVisualization("RomVisualizer", self.HAppControlCenter)
        self.HAppControlCenter.addVisualization(self.RomVisualization)
                
        print("rom settings are {}".format(self.romSettings))
        self.executeRom()
        
        
        
    def addROMFolderToPath(self):
        print("Adding ROM folders to path...")
        #add the rom to the python path
        fileFolderList = self.romFilePath.split("/")

        folderDirectory = ""

        for folder in fileFolderList[:-1]:
            folderDirectory = folderDirectory + folder + "//"
            
        print(folderDirectory)

        self.HAppControlCenter.PathManager.addDirectory(folderDirectory)