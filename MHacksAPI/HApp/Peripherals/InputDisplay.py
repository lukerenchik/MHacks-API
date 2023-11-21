# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 13:45:04 2022

@author: Derek Joslin
"""


from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg

import time
            
class InputDisplay(qw.QWidget):
    
    def __init__(self, state, cursorPosition, dim):
        
        """
        reads in a list of the current FC state. displays that state of 1s and 0s in a matrix of png images
        if val is a one, that element in the table reads in the raised image png. If the element is a zero that element reads in the
        lowered image png.
        """
        
        super().__init__()
        
        self.state = state
        self.cursorPosition = cursorPosition
        self.layout = noSpaceGridLayout()
        self.layout.setHorizontalSpacing(0)
        self.layout.setVerticalSpacing(0)
        
        self.pinList = []
        
        for yPosition,iRow in enumerate(state):
            for xPosition,iElement in enumerate(iRow):
                pinButton = pinDisplay(self.state,xPosition,yPosition,self.cursorPosition)
                pinButton.setSizePolicy(qw.QSizePolicy.Fixed, qw.QSizePolicy.Fixed)
                self.pinList.append(pinButton)
                self.layout.addWidget(pinButton,yPosition,xPosition)
                self.layout.setRowStretch(yPosition, 1)
                self.layout.setColumnStretch(xPosition, 1)
                self.layout.setColumnMinimumWidth(xPosition, 10)
                self.layout.setRowMinimumHeight(yPosition, 10)
                
        
                
        self.setLayout(self.layout)
        
        
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
        for pinButton in self.pinList:
            tic = time.perf_counter()
            #pinButton.repaint()
            toc = time.perf_counter()
            totTime += toc-tic
            #print(toc - tic)
        print(totTime)
        
        
class noSpaceGridLayout(qw.QGridLayout):
    
    def __init__(self):
        super().__init__()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.setHorizontalSpacing(0)
        self.setVerticalSpacing(0)        
        
  
class pinDisplay(qw.QPushButton):
    
    def __init__(self,state,xPosition,yPosition,cursorPosition):
        
        super().__init__()
        
        
        self.birthTime = time.perf_counter()
        self.timeAlive = time.perf_counter() - self.birthTime
        self.refreshCounter = 0
        self.paintCounter = 0
        
        self.cursorPosition = cursorPosition
        self.state = state
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.pinOn = self.state[self.yPosition][self.xPosition]
        
        self.setIcon(qg.QIcon(":emptyPin"))
        self.setMinimumWidth(10)
        self.setMinimumHeight(10)
        
        iconSize = self.sizeHint()
        iconSize.setHeight(iconSize.height() + 15)
        iconSize.setWidth(iconSize.width() + 15)
        self.setIconSize(iconSize)
        
        if self.cursorPosition == [self.xPosition,self.yPosition]:
                self.setIcon(qg.QIcon(":text"))
        elif self.pinOn:
                self.setIcon(qg.QIcon(":filledPin"))
        else:
            self.setIcon(qg.QIcon(":emptyPin"))
        
        
        self.clicked.connect(lambda: self.setCursorPosition())
        
    def setCursorPosition(self):
        print("test")
        self.cursorPosition[0] = self.xPosition
        self.cursorPosition[1] = self.yPosition
        print(self.cursorPosition)
        
    def iconChange(self):
        if (self.cursorPosition[0] is self.xPosition) and (self.cursorPosition[1] is self.yPosition):
                self.setIcon(qg.QIcon(":text"))
        if self.pinOn is not self.state[self.yPosition][self.xPosition]:
            self.pinOn = self.state[self.yPosition][self.xPosition]
            
            if (self.cursorPosition[0] is self.xPosition) and (self.cursorPosition[1] is self.yPosition):
                self.setIcon(qg.QIcon(":text"))
            elif self.pinOn:
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
    Engine.connectTouchScreen("COM7")
    
    displaySize = Engine.return_displaySize()
    
    nRows = displaySize[0]
    nColumns = displaySize[1]
    
    
    tic = 0
    cursorPosition = [0,0]
    
    
    Engine.setCursorPosition(cursorPosition)
    
    
    
    desiredView = RealTimeInputVisualizerv3.InputViewBox(desiredInput, Engine)
    
    aspectRatioBox = RealTimeInputVisualizerv3.AspectRatioWidget(desiredView)
    
    #desiredView = qw.QGraphicsView(aspectRatioBox)

    
    aspectRatioBox.show()
    
    sys.exit(app.exec_())
"""