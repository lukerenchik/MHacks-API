# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 15:05:54 2023

@author: Derek Joslin
"""

import sys
from PyQt5.QtWidgets import QApplication

import TouchStateVisualizer as tsv
import NHAPI as nh
import TouchScreenInterface as ts


if __name__ == "__main__":
    app = QApplication(sys.argv)
    BrailleDisplay = nh.NHAPI()
    BrailleDisplay.connect("COM12", 0)
    sensor = ts.TouchScreenInterface("COM7",0)

    state = BrailleDisplay.state()
    displaySize = BrailleDisplay.size()

    touchViz = tsv.TouchStateVisualizer(state, displaySize, sensor)
    touchViz.show()
    
    sys.exit(app.exec_())