# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 12:30:01 2022

@author: Derek Joslin
"""


import sys
import os

class PathManager():
    
    def __init__(self, versionNumber, codeName):
        
        # Define the version and release of the HApplication
        self.softwareVersionNumber = "v" + versionNumber
        self.softwareReleaseVersion = self.softwareVersionNumber[:-2]
        
        self.softwareCodeName = codeName
        self.softwareIdentifier = self.softwareVersionNumber + "-" + self.softwareCodeName
        self.softwareReleaseIdentifier = self.softwareReleaseVersion + "-" + self.softwareCodeName
        
        # Create the names of the release and software folder
        self.softwareReleaseFolder = "API" + self.softwareReleaseIdentifier + "//"
        self.softwareFolder = self.softwareIdentifier + "//"

        # root path
        self.rootSoftwarePath = os.getcwd() #"C://Users//derek//OneDrive//NewHaptics Shared//HapticOS//FC_GUI_API//"
        self.rootSoftwarePath = self.rootSoftwarePath.split("HApp\\", 1)
        self.rootSoftwarePath = self.rootSoftwarePath[0] + "HApp//"
        print(self.rootSoftwarePath)
        
        # path to software folder of the current version
        self.pathToSoftwareFolder = self.rootSoftwarePath #+ self.softwareReleaseFolder + self.softwareFolder
        
        # Add the software folder to the Python path
        sys.path.append(self.pathToSoftwareFolder)
        
        # Add all subfolders of the current software folder to the Python path
        sys.path.append("C://Program Files//MATLAB//R2022b//bin")
        
    def addSubdirectories(self):
        
        # List all the subdirectories in the software folder
        subdirectories = [d for d in os.listdir(self.pathToSoftwareFolder) if os.path.isdir(os.path.join(self.pathToSoftwareFolder, d))]

        # Add each subdirectory to the Python path
        for subdirectory in subdirectories:
            if subdirectory != "Legacy":
                sys.path.append(os.path.join(self.pathToSoftwareFolder, subdirectory))
        
    def addDirectory(self, directoryPath):
        os.listdir(self.pathToSoftwareFolder)
        sys.path.append(directoryPath)
        
        
    def makeCWD(self, directoryString):
        
        subDirectoryList = os.listdir(self.pathToSoftwareFolder)
        
        for subdirectory in subDirectoryList:
            if subdirectory == directoryString:
                directioryPath = os.path.join(self.pathToSoftwareFolder, subdirectory)
                print(directioryPath)
                os.chdir(directioryPath)
        
# =============================================================================
# if __name__ == '__main__':
#     
#     
#     
#     HAppPathManager = PathManager("0.768", "Coeus")
# =============================================================================
    
    
    
    
    