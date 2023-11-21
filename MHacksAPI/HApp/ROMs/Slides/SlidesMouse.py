# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 11:25:46 2022

@author: Derek Joslin

"""

import RomAPI as rs

class SlidesMouseHandles(rs.RomMouseHandles):
    
    def __init__(self, MasterModel):
        super().__init__()
        
        self.MasterModel = MasterModel
        
        # check if the touchscreen is attached or not
        VisualizerOperator = self.MasterModel.Controller.HAppControlCenter.getOperation("TouchVisualizerRefreshOperation")
        if VisualizerOperator is not None:
            self.VisualizerOperator = VisualizerOperator
        else:
            print("no touch screen attached")
            
        VisualizerOperator = self.MasterModel.Controller.HAppControlCenter.getOperation("StateVisualizerRefreshOperation")
        if VisualizerOperator is not None:
            self.VisualizerOperator = VisualizerOperator
        else:
            print("no device attached")
                
                
    def LeftButtonHandler(self, xCoordinate, yCoordinate):
        VisualizerOperation = self.MasterModel.Controller.HAppControlCenter.getOperation("TouchVisualizerRefreshOperation")
        if VisualizerOperation is not None:
            self.MasterModel.Controller.HAppControlCenter.interruptExecute(lambda x=xCoordinate,y=yCoordinate: VisualizerOperation.clickSelect(x, y))
        else:
            pass
     
        
        # Mouse click event for visualizer operator
        scaler = self.VisualizerOperator.scaler
        
        # get the pin position from GUI coordinate
        scaledDict = scaler.scale(xCoordinate, yCoordinate, "visualizer")
         
        # get the pin coordinate to highlight
        xPinCoordinate = scaledDict["pin"][0]
        yPinCoordinate = scaledDict["pin"][1]
        
        #self.MasterModel.parameterClicked([int(pinSelected[1]), int(pinSelected[0])])
        self.MasterModel.parameterClicked([int(yPinCoordinate), int(xPinCoordinate)])
        
    def MoveHandler(self, xCoordinate, yCoordinate):
        # Turn off the touch screen tracker
        VisualizerOperation = self.MasterModel.Controller.HAppControlCenter.getOperation("TouchVisualizerRefreshOperation")
        if VisualizerOperation is not None:
            self.MasterModel.Controller.HAppControlCenter.interruptExecute(lambda x=xCoordinate,y=yCoordinate: VisualizerOperation.moveAction(x, y))
        else:
            pass
        