# -*- coding: utf-8 -*-
"""
Created on Thu May 20 11:45:08 2021

@author: NewHaptics01
"""


import BoardCom as bc


rowSize = 14

com = bc.BoardCom("COM5")
ARDState = com.newGet_matrix()
state = []
for byte in ARDState:
    
    binary = list(bin(byte))
    del binary[0:2]
    binary = [int(i) for i in binary]
    
    while len(binary) != 8:
        binary.insert(0,0)

    binary = binary[::-1]
    
    state.append(binary)

del state[-1]

ARDState = []
ARDState.append([])

rowElem = 14
rowIndex = 0

for byte in state:
    
    rowElem = rowElem - 8
    
    
    if rowElem > 0:
        ARDState[rowIndex].extend(byte)
    else:
        ARDState[rowIndex].extend(byte[0:rowElem])
        ARDState.append([])
        rowIndex = rowIndex + 1
        rowElem = 14
        
del ARDState[-1]
    

ARDState = [[bool(i) for i in row] for row in ARDState]

#state = np.array(state)
#state = np.reshape(state, (14,15))

com.close()
