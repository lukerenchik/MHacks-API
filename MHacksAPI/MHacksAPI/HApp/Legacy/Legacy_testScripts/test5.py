# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 14:38:21 2022

@author: alex
"""

import BoardCom as b


comm  = b.BoardCom("COM3", 1)

testOutput = [0,1,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,1,1,1,0,1,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,1,1,1,1]

#testOutput = [0,71,28,116,113,199,128]

#comm.port.write(bytearray(1))

#comm.port.write(bytearray(testOutput))

#comm.port.read(1)

comm.set_row(1,testOutput)

returnMatrix = comm.get_matrix()

print(returnMatrix)

comm.close()

