# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 11:59:37 2022

@author: derek
"""


class SlidesCanvasNav():

    def __init__(self, displaySize):
        
        self.canvas = [[]]#[[0 for _ in range(nColumns)] for _ in range(nRows)] # loaded file
        
        self.loadStartPoint = [0,0]
        self.loadEndPoint = [displaySize[1], displaySize[0]]
        
        self.viewingSpace = [self.loadStartPoint, self.loadEndPoint]
        
    def setCanvas(self, newCanvas):
        self.canvas = newCanvas
        #print("canvas = {}".format(newCanvas))        

    # Function to move the viewSpace up
    def moveUp(self):
         if self.loadStartPoint[1] > 0:
             self.loadStartPoint[1] -= 4
             self.loadEndPoint[1] -= 4
             self.viewingSpace = [self.loadStartPoint, self.loadEndPoint]
         else:
             print("hit top of canvas")
        
    # Function to move the viewSpace down
    def moveDown(self):
        if self.loadEndPoint[1] < len(self.canvas):
            self.loadStartPoint[1] += 4
            self.loadEndPoint[1] += 4
            self.viewingSpace = [self.loadStartPoint, self.loadEndPoint]
        else:
            print("hit bottom of canvas")
        
    # Function to move the viewSpace left
    def moveLeft(self):
        if self.loadStartPoint[0] > 0:
            self.loadStartPoint[0] -= 3
            self.loadEndPoint[0] -= 3
            self.viewingSpace = [self.loadStartPoint, self.loadEndPoint]
        else:
            print("hit left boundry of canvas")
    
    # Function to move the viewSpace right
    def moveRight(self):
        if self.loadEndPoint[0] < len(self.canvas[0]):
            self.loadStartPoint[0] += 3
            self.loadEndPoint[0] += 3
            self.viewingSpace = [self.loadStartPoint, self.loadEndPoint]
        else:
            print("hit right boundry of canvas")
        
    # returns the part of the canvas in the viewing space
    def extractViewSpace(self):
        startRow = self.viewingSpace[0][1]
        endRow = self.viewingSpace[1][1]
        startCol = self.viewingSpace[0][0]
        endCol = self.viewingSpace[1][0]
        viewSpace = []
        for row in self.canvas[startRow:endRow]:
            viewSpace.append(row[startCol:endCol])
        return viewSpace
    
    
# =============================================================================
# nRows = 51
# nColumns = 120
# 
# canvas = [[0 for _ in range(nColumns)] for _ in range(nRows)]
# 
# 
# FileManager = sm.SlidesFileManagement()
# 
# canvas = FileManager.openSlide("Slide 1")
# 
# nav = SlidesCanvasNav(canvas, [41, 18])
# 
# for i in range(0,50):
#     nav.moveDown()
#     
# for i in range(0,25):
#     nav.moveRight()
# 
# viewSpace = nav.extractViewSpace()
# for row in viewSpace:
#     print(row)
# print(nav.viewingSpace)
# 
# =============================================================================
