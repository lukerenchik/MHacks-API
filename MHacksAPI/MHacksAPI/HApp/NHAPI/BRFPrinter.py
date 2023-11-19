# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 12:52:30 2022

@author: Derek Joslin
"""

import Brailler as b
import numpy as np

import math
import os


class BRFPrinter(b.Brailler):
    
    def __init__(self, data, state):
    
        # Create the brailler
        super().__init__(data, state)
        
        
    def openBRF(self, filePath):
        
        # Open the file in read mode
        with open('Butterfly-book-tips-card.brf', 'r') as file:
          # Read the contents of the file into a variable
          self.fileContents = file.read()

        # Print the contents of the file as a string
        self.fileContentsPages = self.fileContents.split("\x0c")
        for page in self.fileContentsPages:
            print(page)

    def displayPage(self, pageNum):
        
        pageString = self.fileContentsPages[pageNum]
        
        pageLines = pageString.split("\n")
        
        xCoordinate = 0
        yCoordinate = 0
        for lineList in pageLines:
            for character in lineList:
                self.printCharacter((xCoordinate,yCoordinate), character)
                print(character, end="")
                xCoordinate += 3
                #print("{0},".format(xCoordinate), end="")
                if xCoordinate > 117:
                    xCoordinate = 0
            print("")
            yCoordinate += 4
            xCoordinate = 0
            if yCoordinate > 43:
                return self.state

    
    
    def savePage(self, state, name):
        print(state)
        
        currentSlidePath = "C://Users//derek//OneDrive//NewHaptics Shared//HapticOS//FC_GUI_API//APIv0.7-Coeus//v0.766-Coeus//RealTimeOutputDevelopment//{}.csv".format(name)
        
        with open(currentSlidePath, "w") as f:
            for row in state:
                for (i,elem) in enumerate(row):
                    if elem == True:
                        f.write("{0}".format(1))
                    elif elem == False:
                        f.write("{0}".format(0))
                    if i is not len(row) - 1:
                        f.write(",")
                f.write("\n")
        f.close()
