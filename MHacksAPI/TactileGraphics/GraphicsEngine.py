# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 10:18:00 2020

@author: Derek Joslin

"""

""" this is the new graphics engine which performs operations on a matrix and changes the values inside """

import numpy as np
import cairo
import Brailler as br
from FeatureMetadata import FeatureMetadata
from PIL import Image
import math

class GraphicsEngine(FeatureMetadata):
    def __init__(self, dimensions):
        super().__init__()
        self.dimensions = dimensions

        # round to nearest 20 multiple because cairo likes multiples of 20 for some reason
        self.cairoDimensions = (20*math.ceil(self.dimensions[0]/20), 20*math.ceil(self.dimensions[1]/20))
        
        self.matrix = np.ndarray(shape=(self.cairoDimensions[1], self.cairoDimensions[0]), dtype=np.uint8)
        #create the brailler
        self.Brailler = br.Brailler(self.matrix)

    def drawFeatures(self):
        self.img = cairo.ImageSurface(cairo.FORMAT_A8, self.cairoDimensions[0], self.cairoDimensions[1])
        self.ctx = cairo.Context(self.img)
        # Iterate through the features_metadata and draw each feature
        for featureId, featureMetadata in self.featuresMetadata.items():
            if featureMetadata.type == "braille":
                pass
            else:
                featureMetadata._drawFeature(self.ctx)

        # Update the matrix with the drawn features
        buf = self.img.get_data()
        self.matrix = np.ndarray(shape=(self.cairoDimensions[1], self.cairoDimensions[0]), dtype=np.uint8, buffer=buf)

        self.Brailler.data = self.matrix
        #self.Brailler = br.Brailler(self.matrix)
        for featureId, featureMetadata in self.featuresMetadata.items():
            if featureMetadata.type == "braille":
                self.writeBraille(featureMetadata)

    def writeBraille(self, BrailleFeature):
        # convert cells to coordinates
        startX = BrailleFeature.startCell[0] * 3
        startY = BrailleFeature.startCell[1] * 4
        # dimensions of the tactile display
        dim = self.dimensions
        dimRow = dim[1]
        dimCol = dim[0]
        
        # cycle through each axis and print a character
        for letter in BrailleFeature.brailleString:
            if letter == '\n':
                if startY + 3 < dimRow:
                    startX = 0
                    startY = startY + 4
                else:
                    break
            else:
                if startX + 2 <= dimCol:
                    self.Brailler.printCharacter([startX,startY],letter)
                    startX = startX + 3
                elif startY < (dimRow - 4):
                    startX = 0
                    startY = startY + 4
                    self.Brailler.printCharacter([startX,startY],letter)
                else:
                    pass
        
    def retrieveList(self):
        subMatrix = self.matrix[0:self.dimensions[1], 0:self.dimensions[0]]        
        subMatrix[subMatrix < 50] = 0
        subMatrix[subMatrix >= 50] = 1
        return subMatrix.tolist()
        
    def showImage(self):
        # Display the image using the PIL Image.show() method
        self.img = Image.fromarray(self.matrix)
        self.img.show()