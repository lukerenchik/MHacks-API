# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 17:51:07 2021

@author: Derek Joslin
"""

import sys
import NHAPI as nh


if __name__ == '__main__':
    
    nh.connect("COM10")


    nh.dot((5,5))


    nh.disconnect()

    sys.exit()
    
