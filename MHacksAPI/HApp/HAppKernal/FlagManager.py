# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 13:10:55 2023

@author: Derek Joslin

"""

""" class for an object which contains data that when in a certain state will be used to determine if an operation should execute """

from PyQt5.QtWidgets import QLabel

class Flag:
    
    def __init__(self, name):
        self.name = name
        self.debugString = ""
        self.state = 0
        
    def clearState(self):
        self.state = 0
        
    def setState(self, state):
        self.state = state
        
    def getState(self):
        # some value that can be matched against itself
        return self.state
    
# =============================================================================
#     def checkCondition(self, conditionState) -> bool:
#         return self.state == conditionState
# =============================================================================
        
class FlagManager:
    
    def __init__(self):
        self.flagDictionary = {}

    def addFlag(self, Flag):
        self.flagDictionary[Flag.name] = Flag
    
    def removeFlag(self, flagName):
        del self.flagDictionary[flagName]
        
    def getFlag(self, flagName):
        return self.flagDictionary.get(flagName)
        
    def getAllFlags(self):
        return self.flagDictionary.values()
    
    def printAllFlags(self):
        flagDebugText = "ARCS Flags-\n"
        for Flag in self.flagDictionary.values():
            flagDebugText += "{}\n".format(Flag.name)
            flagDebugText += "{}\n".format(Flag.debugString)
            flagDebugText += "state: {}\n".format(Flag.state)
        return flagDebugText
    
    def getFlagLabels(self):
        # create a list of labels for the peripherals
        flagLabelList = []

        for Flag in self.flagDictionary.values():
            # for each peripheral make a label
            Label = QLabel(Flag.name)
            
            # set the tooltip for this label to be the debug text of the peripheral
            Label.setToolTip(Flag.debugString)
            
            # add the perihperal label to the list
            flagLabelList.append(Label)

        return flagLabelList
# =============================================================================
# if __name__ == '__main__':
#     
#     FlagManager = HAppFlagManager()
#     flag1 = HAppFlag("flag1")
#     flag2 = HAppFlag("flag2")
#     
#     FlagManager.addFlag(flag1)
#     FlagManager.addFlag(flag2)
#     
#     print(FlagManager.getAllFlags())
#     # Output: [<__main__.Flag object at 0x7f1c1d4e7dd8>, <__main__.Flag object at 0x7f1c1d4e7e48>]
#     
#     FlagManager.removeFlag("flag1")
#     print(FlagManager.getAllFlags())
#     # Output: [<__main__.Flag object at 0x7f1c1d4e7e48>]
# 
#     myFlag = FlagManager.getFlag("flag2")
#     print(myFlag.name)
# =============================================================================
