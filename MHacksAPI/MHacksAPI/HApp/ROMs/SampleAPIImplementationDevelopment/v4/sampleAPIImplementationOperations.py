# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 15:12:55 2022

@author: Derek Joslin
"""

import RomAPI as rs


class SampleOperation(rs.RomOperation):
    
    def __init__(self, Controller):
        super().__init__()
        self.Controller = Controller
        
    def execute(self):
        serialHaltInterrupt = self.Controller.getInterruptFlag('romHaltSerial')
        #idk interrupt communication somehow
        if serialHaltInterrupt:
            #stop the romvisualizer
            self.Controller.OperationsController.stopExecutingOperation("VisualizationRefreshOperation")
        else:
            #turn it back on
            self.Controller.OperationsController.startExecutingOperation("VisualizationRefreshOperation")