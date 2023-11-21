# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 16:12:41 2022

@author: Derek Joslin
"""

import numpy as np

import Brailler as br




testList = [[False for i in range(0,41)] for j in range(0,19)]




dataMat = np.array(testList)




brailling = br.Brailler(dataMat, testList)




brailling.printCharacter([10,14],"V")




