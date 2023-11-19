# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 10:59:52 2020

@author: Derek Joslin
"""
import numpy as np


#class to tween frames of a matrix using a predefined algorithm
class TactileTweener:

    def __init__(self,**kwargs):
        self.__refreshProtocols = {'row by row': self.rowByrow, 'column element by element': self.column_elementByelement, 'row element by element': self.row_elementByelement}
        self.__refreshProtocols.update(kwargs)

    def add_refreshProtocol(self,**kwargs):
        self.__refreshProtocols.update(kwargs)

    def get_tweenFrames(self, startState, endState, protocol):
        #create an array of matrices starting with the first matrix
        rows = len(startState)
        columns = len(startState[0])
        frames = [{'state' : startState, 'element change' : [[False] * rows] * columns}]

# =============================================================================
#         x = 0
# 
# 
#         print('frame: {0}'.format(x))
#         x += 1
#         print('---------------------------\n\r')
#         print('\n'.join([''.join(['{:4}'.format(item) for item in row])
#                          for row in frames[-1]['state']]))
#         print('T/F')
#         print('\n'.join([''.join(['{:4}'.format(item) for item in row])
#                          for row in frames[-1]['element change']]))
# =============================================================================

        while frames[-1]['state'] != endState:
            newFrame = self.__refreshProtocols[protocol](frames[-1]['state'],endState)
            #check which frames are different to calculate frames later on
            elementChanges = (np.array(frames[-1]['state']) != np.array(newFrame)).tolist()
            frames.append({'state' : newFrame, 'element change' : elementChanges})
# =============================================================================
#             print('frame: {0}'.format(x))
#             x += 1
#             print('---------------------------\n\r')
#             print('\n'.join([''.join(['{:4}'.format(item) for item in row])
#                              for row in frames[-1]['state']]))
#             print('T/F')
#             print('\n'.join([''.join(['{:4}'.format(item) for item in row])
#                              for row in frames[-1]['element change']]))
# =============================================================================
        else:
# =============================================================================
#             print('frame: inf')
#             print('---------------------------\n\r')
#             print('\n'.join([''.join(['{:4}'.format(item) for item in row])
#                              for row in frames[-1]['state']]))
#             print('T/F')
#             print('\n'.join([''.join(['{:4}'.format(item) for item in row])
#       for row in frames[-1]['element change']]))
# =============================================================================

            return frames

    #change one row at a time in order of precedence
    def rowByrow(self,startMatrix,targetMatrix):
        #if equal return target
        if startMatrix == targetMatrix:
            return targetMatrix
        else:
            newMatrix = startMatrix.copy()
            #change the first row that is different
            for index, (startRow,targetRow) in enumerate(zip(startMatrix,targetMatrix)):
                if startRow != targetRow:
                    newMatrix[index] = targetRow
                    #return the changed matrix
                    return newMatrix

    #changes one element in order of precedence
    def column_elementByelement(self,startMatrix,targetMatrix):
        #if equal return target
        if startMatrix == targetMatrix:
            return targetMatrix
        else:
            newMatrix = startMatrix.copy()
            #change the first element that is different
            for columnIndex in range(0,len(targetMatrix[0])):
                #iterate through all the column elements
                for rowIndex, (startElement, targetElement) in enumerate(zip([row[columnIndex] for row in startMatrix],[row[columnIndex] for row in targetMatrix])):
                    if startElement != targetElement:
                        newMatrix[rowIndex][columnIndex] = targetElement
                        return newMatrix

    def row_elementByelement(self,startMatrix,targetMatrix):
        if startMatrix == targetMatrix:
            return targetMatrix
        else:
            newMatrix = startMatrix.copy()
            #change the first element in row that is different
            for rowIndex, (startRow,targetRow) in enumerate(zip(startMatrix,targetMatrix)):
                for columnIndex, (startElement, targetElement) in enumerate(zip(startRow,targetRow)):
                    if startElement != targetElement:
                        newMatrix[rowIndex][columnIndex] = targetElement
                        return newMatrix
