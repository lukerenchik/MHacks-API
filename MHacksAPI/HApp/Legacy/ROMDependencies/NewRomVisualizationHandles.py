# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 11:35:34 2022

@author: Derek Joslin
"""


import DefaultRomVisualizationHandles as dh


class NewRomVisualizationHandles(dh.DefaultRomVisualizationHandles):
    
    def __init__(self):
        print("New handler initialized")
    
    def createActionsHandler(self):
        print("New Create action handler called")
        
    def createMenuHandler(self):
        print("New Create menu handler called")
        
    def createToolsHandler(self):
        print("New Create tool handler called")
        
    def connectControlsHandler(self):
        print("New Connect controls handler called")

    def setStylesHandler(self):
        print("New Set styles handler called")
        
