# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 10:02:52 2022

@author: Derek Joslin
"""
from PyQt5.QtWidgets import QApplication
import sys

import DesiredStateButtonWidget as dw
import CursorGraphicsView as cg
import AspectRatioViewResizer as ar

import NHAPI as nh

class IntegratedInputWindow(ar.AspectRatioWidget):
    
    
    def __init__(self, nhapi):
        
        self.NHAPI = nhapi
        self.DesiredStateInputGrid = dw.DesiredStateButtonInputWidget(nhapi)
            
        #aspectRatioBox = ar.AspectRatioWidget(DesiredStateInputGrid)
        #aspectRatioBox.show()
    
        #AspectRatioLayoutResizer = vw.AspectRatioLayoutWidget(DesiredStateInputGrid)
        #self.widgetList = [DesiredStateInputGrid]
        
        self.CursorGraphicsView = cg.CursorGraphicsView(nhapi, self.DesiredStateInputGrid)
        
        
        #CursorGraphicsView.show()
        margin = (1200,0)
        super().__init__(self.CursorGraphicsView, margin)
        
        
        
# =============================================================================
#     def updateWindowSize(self):
#         #run all necessary things to resize the window
#         
#         newDisplaySize = self.NHAPI.return_displaySize()
#         print(newDisplaySize)
#         
#         
#         #for DesiredStateInputGrid make sure to resize it keeping pins that exist and adding ones that don't
#         #check the layout for pins that exist and add a pin when it doesn't
#         self.DesiredStateInputGrid.resizeLayout(newDisplaySize)
# =============================================================================
        
        
"""
if __name__ == '__main__':

    app = QApplication(sys.argv)

    #create an api object
    Engine = nh.NHAPI()
    
    
    #Engine.connect("COM5",0)
    #Engine.connectTouchScreen("COM7")

    #displaySize = Engine.return_displaySize()
    #print(displaySize)

    inputWindow = IntegratedInputWindow(Engine)
    inputWindow.show()
    


    sys.exit(app.exec_())
"""