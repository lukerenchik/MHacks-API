# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 10:14:59 2022

@author: Derek Joslin

"""

import csv
import errno
import os
#from PIL import Image 

class SlidesFileManagement():
    
    def __init__(self, PathManager):
        # Initialize a slides file by creating a folder in the cwd
# =============================================================================
#         self.rootSoftwarePath = os.getcwd() #"C://Users//derek//OneDrive//NewHaptics Shared//HapticOS//FC_GUI_API//"
#         self.rootSoftwarePath = self.rootSoftwarePath.split("FC_GUI_API\\", 1)
#         self.rootSoftwarePath = self.rootSoftwarePath[0] + "FC_GUI_API//"
# =============================================================================
        self.PathManager = PathManager        
        
        self.rootSoftwarePath = self.PathManager.rootSoftwarePath
        
        self.currentSlidesDirectory = self.rootSoftwarePath + "testScripts//SlidesTestScripts//SlidesTest1//"
        
        # create a first slide in cwd
        self.currentSlidePath = self.currentSlidesDirectory  + "Slide 1.csv"
        
    def currentNumSlides(self):
        # counts the number of files in self.currentslidesDirectory
        
        # Use os.listdir() to get a list of all the files and directories in the given directory
        files = os.listdir(self.currentSlidesDirectory)
        
        # Use len() to get the number of items in the list
        num_files = len(files)
        
        return num_files
        
    def createNewSlidesFile(self, newSlidesDirectory):
        # create a folder in cwd
        
        try:
            
            # make the slide folder
            os.mkdir(newSlidesDirectory)
            
            self.currentSlidesDirectory = newSlidesDirectory
            
            # test file
            dummyTestFile = [[0 for i in range(0, 41)] for j in range(0, 18)]
            
            # create an empty slide
            self.saveSlide("Slide 1", dummyTestFile)
                        
        except:
            print("failed to create slides file")
    
        
    def loadSlidesFile(self, newWorkingDirectory):
        # Reads the folder and grabs slide data from folder
        self.currentSlidesDirectory = newWorkingDirectory
        
     
        
    def openSlide(self, slideString):
        self.currentSlidePath = self.currentSlidesDirectory + "{}.csv".format(slideString)
        
        d = []
        with open(self.currentSlidePath, 'rt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                d.append(row)
        
        return d
    
    
    def deleteSlide(self, slideString):
        self.currentSlidePath = self.currentSlidesDirectory + "{}.csv".format(slideString)
        
        try:
            
            os.remove(self.currentSlidePath)
            
        except OSError as exc:
            
            if exc.errno != errno.EEXIST:
                
                raise
            
            pass
        
        
    
    def saveSlide(self, slideString, mat):
        print(slideString)
        
        self.currentSlidePath = self.currentSlidesDirectory + "{}.csv".format(slideString)
        
        with open(self.currentSlidePath, "w") as f:
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
        
    def makeCWD(self, directoryString):
        
        subDirectoryList = os.listdir(self.PathManager.pathToSoftwareFolder)
        
        for subdirectory in subDirectoryList:
            if subdirectory == directoryString:
                directioryPath = os.path.join(self.PathManager.pathToSoftwareFolder, subdirectory)
                print(directioryPath)
                os.chdir(directioryPath)