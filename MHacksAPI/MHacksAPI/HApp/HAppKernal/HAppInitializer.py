# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 11:23:43 2022

@author: Derek Joslin

"""

import PathManager as pm
import pyqtconsole
import cairo
import serial
from pyqtconsole.console import PythonConsole
import sys

# create the path manager and add the subdirectories
HAppPathManager = pm.PathManager("0.773", "Coeus")
HAppPathManager.addSubdirectories()

# =============================================================================
# for path in sys.path:
#     print(path)
# =============================================================================

# import the remaining HApp Libraries
import HAppMainWindow as hm
from PyQt5 import QtWidgets as qw

import sys

if __name__ == '__main__':
    
    app = qw.QApplication([])
    
    MainWindow = hm.HAppMainWindow(HAppPathManager)
    
    MainWindow.show()
    
    #filename = 'C:/Users/derek/OneDrive/NewHaptics Shared/HapticOS/FC_GUI_API/APIv0.7-Coeus/v0.764-Coeus/ROMs/FileNavigator/FileNavigatorReady.rom'
    
    #MainWindow.initializeRom(filename)
    
    sys.exit(app.exec_())