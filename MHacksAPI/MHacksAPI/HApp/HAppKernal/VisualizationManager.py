# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 13:10:23 2023

@author: Derek Joslin

"""

from PyQt5.QtWidgets import QDialog, QLabel

class Visualization(QDialog):
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.name = name
        self.setWindowTitle(self.name)
        self.debugString = ""
    
    
class VisualizationManager:
    def __init__(self):
        self.visualizationDictionary = {}
        
    def addVisualization(self, Visualization):
        self.visualizationDictionary[Visualization.name] = Visualization
        
    def removeVisualization(self, visualizationName):
        del self.visualizationDictionary[visualizationName]
        
    def getVisualization(self, visualizationName):
        return self.visualizationDictionary.get(visualizationName)
        
    def getAllVisualizations(self):
        return self.visualizationDictionary.values()
    
    def showAll(self):
        for Visualization in self.Visualization.values():
            Visualization.show()
            
    def closeAll(self):
        for Visualization in self.Visualization.values():
            Visualization.close()

    def printAllVisualizations(self):
        visualizationDebugText = "ARCS Visualizations-\n"
        for Visualization in self.visualizationDictionary.values():
            visualizationDebugText += "{}\n".format(Visualization.name)
            #visualizationDebugText += "{}\n".format(Visualization.debugString)
            
        return visualizationDebugText

    def getVisualizationLabels(self):
        # create a list of labels for the peripherals
        visualizationLabelList = []

        for Visualization in self.visualizationDictionary.values():
            # for each peripheral make a label
            Label = QLabel(Visualization.name)
            
            # set the tooltip for this label to be the debug text of the peripheral
            Label.setToolTip(Visualization.debugString)
            
            # add the perihperal label to the list
            visualizationLabelList.append(Label)

        return visualizationLabelList
    
# =============================================================================
# if __name__ == '__main__':
#     
#     visualization_manager = VisualizationManager()
# 
#     vis1 = Visualization("Visualization 1")
#     vis2 = Visualization("Visualization 2")
#     
#     visualization_manager.add_visualization(vis1)
#     visualization_manager.add_visualization(vis2)
#     
#     print(visualization_manager.get_all_visualizations())
#     # Output: [<__main__.Visualization object at 0x7f1c1d4e7dd8>, <__main__.Visualization object at 0x7f1c1d4e7e48>]
#     
#     visualization_manager.remove_visualization("Visualization 1")
#     print(visualization_manager.get_all_visualizations())
#     # Output: [<__main__.Visualization object at 0x7f1c1d4e7e48>]
# =============================================================================
