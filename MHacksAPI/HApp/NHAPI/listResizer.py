# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 13:41:48 2022

@author: Derek Joslin
"""



def listResizer(listToResize, nColumns, nRows):
    #cutoff the columns
    for index,row in enumerate(listToResize):
        listToResize[index] = [False for i in range(0,nColumns)]
        
    #cutoff the rows
    if len(listToResize) > nRows:    
        listToResize[nRows:] = []
    elif len(listToResize) < nRows:
        while len(listToResize) < nRows:
            listToResize.append([False for i in range(0,nColumns)])
    else:
        pass
    
        
    
    
    
desiredState = [[False for i in range(0,41)] for j in range(0,19)]
print(id(desiredState))
listResizer(desiredState, 41, 19)

print(id(desiredState))



    
    
    




