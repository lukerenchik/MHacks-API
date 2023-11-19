# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 14:03:07 2023

@author: Derek Joslin

"""


class CoordinateScaler:
    
    def __init__(self, boundedRegions):
        self.boundedRegions = boundedRegions
        self.scalesDictionary = {}
        
        self.calculateScalesDictionary()
        
    def calculateScalesDictionary(self):
        # create a dictionary for each region
        for fromRegionKey in self.boundedRegions.keys():
            # create the scales for all other regions
            fromRegionScalarDictionary = self.createScalars(fromRegionKey)
            
            # add this to the scalesDictionary
            self.scalesDictionary[fromRegionKey] = fromRegionScalarDictionary
            
    def createScalars(self, fromRegionKey):
        # create a dictionary to hold all of the scalars
        scalarDictionary = {}
        
        
        # cycle through each to region and find the x and y scale
        for toRegionKey in self.boundedRegions.keys():
            # if the toRegion is the same as from region create a 1,1 ratio
            if toRegionKey == fromRegionKey:
                scalarDictionary[toRegionKey] = (1,1)
            
            # otherwise calculate the scaling factor
            fromRegionSize = self.boundedRegions[fromRegionKey]
            toRegionSize = self.boundedRegions[toRegionKey]
            
            toRegionScalar = self.calculateScalar(fromRegionSize, toRegionSize)
            
            # append the scalar value to dictionary
            scalarDictionary[toRegionKey] = toRegionScalar
            
        return scalarDictionary
            
    
    def calculateScalar(self, fromRegionSize, toRegionSize):
        # grab the widths and heights    
        fromRegionWidth = fromRegionSize[0]
        fromRegionHeight = fromRegionSize[1]
        
        toRegionWidth = toRegionSize[0]
        toRegionHeight = toRegionSize[1]
        
        xScalar = toRegionWidth / fromRegionWidth
        yScalar = toRegionHeight / fromRegionHeight
        
        return (xScalar,yScalar)
    

    def scale(self, fromRegionXCoordinate, fromRegionYCoordinate, fromRegionKey):
        # get dictionary for from region scalars
        toRegionScalesDictionary = self.scalesDictionary[fromRegionKey]
        
        toRegionResultsDictionary = {}
        
        for toRegionKey in toRegionScalesDictionary.keys():
            scalar = toRegionScalesDictionary[toRegionKey]
            
            
            toRegionXCoordinate = fromRegionXCoordinate * scalar[0]
            toRegionYCoordinate = fromRegionYCoordinate * scalar[1]
            toRegionResultsDictionary[toRegionKey] = (toRegionXCoordinate, toRegionYCoordinate)
            
        return toRegionResultsDictionary
    


    
regions = { "pin" : (41, 19),
            "touch" : (255*2, 255),
            "visualizer" : (800, 500)
           }


scaler = CoordinateScaler(regions)  # create a scaler that scales coordinates based on the sizes of multiple bounded regions

scaledDict = scaler.scale(5, 5, "pin")

print(scaledDict)
    

# =============================================================================
# regions = { "bounded region 1" : (100, 200),
#             "bounded region 2" : (200, 400),
#             "bounded region 3" : (300, 600)
#            }
# 
# 
# scaler = CoordinateScaler(regions)  # create a scaler that scales coordinates based on the sizes of multiple bounded regions
# 
# scaledDict = scaler.scale(30, 60, "bounded region 3")
# 
# print(scaledDict)
# =============================================================================

