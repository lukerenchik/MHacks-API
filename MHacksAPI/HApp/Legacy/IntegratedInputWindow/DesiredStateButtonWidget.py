# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 12:40:22 2022

@author: Derek Joslin
"""

from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg

import qrc_resources

import sys
from PyQt5.QtWidgets import QApplication


import AspectRatioViewResizer as ar
import NHAPI as nh
import time

class DesiredStateButtonInputWidget(qw.QWidget):

    def __init__(self, nhapi):
        
        """
        reads in a list of the current FC state. displays that state of 1s and 0s in a matrix of png images
        if val is a one, that element in the table reads in the raised image png. If the element is a zero that element reads in the
        lowered image png.
        """
        
        super().__init__()
        
        self.NHAPI = nhapi
        self.cursorPosition = nhapi.getPinCursorPosition()
        self.layout = noSpaceGridLayout()
        self.layout.setHorizontalSpacing(0)
        self.layout.setVerticalSpacing(0)
        
        self.pinList = []
        displaySize = self.NHAPI.return_displaySize()
        #print(displaySize)
    
        print(displaySize)
        for yPosition in range(0,displaySize[0]):
            for xPosition in range(0,displaySize[1]):
                self.createPin(xPosition, yPosition)
                
        self.setLayout(self.layout)
        
        
    def resizeLayout(self, newSize):
        xLength = newSize[1]
        yLength = newSize[0]
        for pin in self.pinList:
            if pin.xPosition > xLength or pin.yPosition > yLength:
                #self.removePin(pin.xPosition,pin.yPosition)
                del pin                
                    
    
    def createPin(self,xPosition,yPosition):
        pinButton = pinDisplay(self.NHAPI,xPosition,yPosition)
        pinButton.setSizePolicy(qw.QSizePolicy.Fixed, qw.QSizePolicy.Fixed)
        self.pinList.append(pinButton)
        self.layout.addWidget(pinButton,yPosition,xPosition)
        self.layout.setRowStretch(yPosition, 1)
        self.layout.setColumnStretch(xPosition, 1)
        self.layout.setColumnMinimumWidth(xPosition, 10)
        self.layout.setRowMinimumHeight(yPosition, 10)
        
    def removePin(self, xPosition, yPosition):
        self.layout()
        
    def updateState(self,newState):
        self.paintView()
        
        
    def paintView(self):
        totTime = 0
        for pinButton in self.pinList:
            tic = time.perf_counter()
            pinButton.update()
            toc = time.perf_counter()
            totTime += toc-tic
            #print(toc - tic)
        #for pinButton in self.pinList:
            #tic = time.perf_counter()
            #pinButton.repaint()
           # toc = time.perf_counter()
            #totTime += toc-tic
            #print(toc - tic)
        #print(totTime)
        
    def addFunctionToButtons(self, func):
        #self.coordList = []
        for pinButton in self.pinList:
            #self.coordList.append((pinButton.yPosition,pinButton.xPosition))
            pinButton.addFunctionToButton(func)
            #clicked.connect(lambda: func(self.coordList[-1]))
            #print(self.coordList[-1])
            
class noSpaceGridLayout(qw.QGridLayout):
    
    def __init__(self):
        super().__init__()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.setHorizontalSpacing(0)
        self.setVerticalSpacing(0)        
        
        
class pinDisplay(qw.QPushButton):
    
    def __init__(self,nhapi,xPosition,yPosition):
        
        super().__init__()
        
        self.NHAPI = nhapi
        self.birthTime = time.perf_counter()
        self.timeAlive = time.perf_counter() - self.birthTime
        self.refreshCounter = 0
        self.paintCounter = 0
        
        self.pinCursorPosition = nhapi.getPinCursorPosition()
        self.inputCursorPosition = nhapi.getInputCursorPosition()
        self.state = nhapi.return_desiredState()
        #print(id(self.state))
        self.xPosition = xPosition
        self.yPosition = yPosition
        
        self.pinOn = self.state[self.yPosition][self.xPosition]
        
        self.setIcon(qg.QIcon(":emptyPin"))
        self.setMinimumWidth(3)
        self.setMinimumHeight(3)
        
        iconSize = self.sizeHint()
        iconSize.setHeight(iconSize.height() + 15)
        iconSize.setWidth(iconSize.width() + 15)
        self.setIconSize(iconSize)
        if self.pinOn:
                self.setIcon(qg.QIcon(":filledPin"))
        else:
            self.setIcon(qg.QIcon(":emptyPin"))
        
        
        self.clicked.connect(lambda: self.setCursorPosition())
        
        
    def setCursorPosition(self):
        
        pinPosition = (self.xPosition, self.yPosition)
        
        self.NHAPI.setPinCursorPosition(pinPosition)
        self.NHAPI.setInputCursorPositionWithPinCursor()
        
        
    def addFunctionToButton(self, func):
        self.clicked.connect(lambda: func((self.yPosition,self.xPosition)))
        
        
    def iconChange(self):
        self.state = self.NHAPI.return_desiredState()
        if self.pinOn is not self.state[self.yPosition][self.xPosition]:
            self.pinOn = self.state[self.yPosition][self.xPosition]
            
            if self.pinOn:
                self.setIcon(qg.QIcon(":filledPin"))
            else:
                self.setIcon(qg.QIcon(":emptyPin"))
            
                
            
    def resizeEvent(self, event):
        super().resizeEvent(event)
        iconSize = self.size()
        iconSize.setHeight(iconSize.height())
        iconSize.setWidth(iconSize.width())
        self.setIconSize(iconSize)
        
        
        
    def paintEvent(self, event):
        self.iconChange()
        if self.style().proxy().objectName() != 'windowsvista':
            super().paintEvent(event)
            return
        opt = qw.QStyleOptionButton()
        self.initStyleOption(opt)
        opt.rect.adjust(-5, -5, 5, 5)
        qp = qw.QStylePainter(self)
        qp.drawControl(qw.QStyle.CE_PushButton, opt)
        
    
    def refreshButton(self):
        self.timeAlive = time.perf_counter() - self.birthTime
        if self.timeAlive > self.refreshCounter:
            print("refresh")
            return True
        else:
            return False
    

    
"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    #create an api object
    Engine = nh.NHAPI()

    Engine.connect("COM5",0)
    #Engine.connectTouchScreen("COM7")
    
    #ex = CursorGraphicsView(Engine)
    test = DesiredStateButtonInputWidget(Engine)
    #test.show()
    
    aspectRatioBox = ar.AspectRatioWidget(test)
    aspectRatioBox.show()
    sys.exit(app.exec_())
"""