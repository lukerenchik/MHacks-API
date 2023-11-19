# -*- coding: utf-8 -*-
"""
Created on Thu May 20 14:12:18 2021

@author: Derek Joslin
"""


import sys

from PyQt5.QtWidgets import QApplication

import HapticVisualizerMainWindow as hv

import NHAPI as nh


if __name__ == '__main__':
    
    
    app = QApplication([])


    BrailleDisplay = nh.NHAPI()
    #BrailleDisplay.connect("COM5",0)
    #BrailleDisplay.connectTouchScreen("COM7")
    

    MainVisualizerWindow = hv.HapticVisualizerMainWindow(0, BrailleDisplay)
    
    
    MainVisualizerWindow.showMaximized()
    
    
    MainVisualizerWindow.Console.eval_queued()
    

    sys.exit(app.exec_())