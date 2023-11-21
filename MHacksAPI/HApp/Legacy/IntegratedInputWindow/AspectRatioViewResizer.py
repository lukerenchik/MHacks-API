# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 09:37:46 2022

@author: Derek Joslin
"""

from PyQt5 import QtWidgets as qw
#import pyqtgraph as pg


class AspectRatioWidget(qw.QWidget):
    
    def __init__(self, widget, margin):
        super().__init__()
        self.widget = widget
        self.marginSpace = margin
        layoutWidth = widget.sizeHint().width() + self.marginSpace[0]
        layoutHeight = widget.sizeHint().height() + self.marginSpace[1]
        
        self.aspect_ratio = layoutWidth / layoutHeight
        self.setLayout(qw.QBoxLayout(qw.QBoxLayout.LeftToRight, self))
        #  add spacer, then widget, then spacer
        self.layout().addItem(qw.QSpacerItem(0, 0))
        self.layout().addWidget(widget)
        self.layout().addItem(qw.QSpacerItem(0, 0))
    
    def resizeEvent(self, e):
        w = e.size().width() + self.marginSpace[0]
        h = e.size().height() + self.marginSpace[1]
    
        if w / h > self.aspect_ratio:  # too wide
            self.layout().setDirection(qw.QBoxLayout.LeftToRight)
            widget_stretch = h * self.aspect_ratio
            outer_stretch = (w - widget_stretch) / 2 + 2.5
        else:  # too tall
            self.layout().setDirection(qw.QBoxLayout.TopToBottom)
            widget_stretch = w / self.aspect_ratio
            outer_stretch = (h - widget_stretch) / 2 + 2.5
    
        self.layout().setStretch(0, outer_stretch)
        self.layout().setStretch(1, widget_stretch)
        self.layout().setStretch(2, outer_stretch)
    
    
class AspectRatioLayoutWidget(qw.QWidget):
    
    def __init__(self, widget):
        super().__init__()
        nRows = widget.layout.rowCount()
        nColumns = widget.layout.columnCount()
        layoutItem = widget.layout.itemAtPosition(0,0)
        
        layoutItemWidth = layoutItem.sizeHint().width()
        layoutItemHeight = layoutItem.sizeHint().height()
        layoutWidth = layoutItemWidth*nColumns
        layoutHeight = layoutItemHeight*nRows
        
        self.aspect_ratio = layoutWidth / layoutHeight
        self.setLayout(qw.QBoxLayout(qw.QBoxLayout.LeftToRight, self))
        #  add spacer, then widget, then spacer
        self.layout().addItem(qw.QSpacerItem(0, 0))
        self.layout().addWidget(widget)
        self.layout().addItem(qw.QSpacerItem(0, 0))
    
    def resizeEvent(self, e):
        w = e.size().width()
        h = e.size().height()
    
        if w / h > self.aspect_ratio:  # too wide
            self.layout().setDirection(qw.QBoxLayout.LeftToRight)
            widget_stretch = h * self.aspect_ratio
            outer_stretch = (w - widget_stretch) / 2 + 2.5
        else:  # too tall
            self.layout().setDirection(qw.QBoxLayout.TopToBottom)
            widget_stretch = w / self.aspect_ratio
            outer_stretch = (h - widget_stretch) / 2 + 2.5
    
        self.layout().setStretch(0, outer_stretch)
        self.layout().setStretch(1, widget_stretch)
        self.layout().setStretch(2, outer_stretch)
        
    """
class AspectRatioWidget(qw.QWidget):
    
    def __init__(self, widget):
        super().__init__()
        self.aspect_ratio = widget.size().width() / widget.size().height()
        layout = qw.QGridLayout()
        self.setLayout(layout)
        #  add spacer, then widget, then spacer
        layout.addWidget(widget,0,0)
        self.heightWidget = qw.QLabel()
        self.widthWidget = qw.QLabel()
        layout.addWidget(self.heightWidget,0,1)
        layout.addWidget(self.widthWidget,1,0)
        
    def resizeEvent(self, e):
        w = e.size().width()
        h = e.size().height()

        if w / h > self.aspect_ratio:  # too wide
            widget_stretch = h * self.aspect_ratio
            width_stretch = (w - widget_stretch) / 2 + 0.5
            self.widthWidget.resize(width_stretch,self.heightWidget.size().height())
        else:  # too tall
            widget_stretch = w / self.aspect_ratio
            height_stretch = (h - widget_stretch) / 2 + 0.5
            self.heightWidget.resize(self.heightWidget.size().width, height_stretch)
        
        """