   
    # -*- coding: utf-8 -*-
"""
Created on Thu May 20 14:12:18 2021

@author: Derek Joslin
"""


from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg



class ToggleSwitch(qw.QPushButton):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setMaximumWidth(150)
        self.setMaximumHeight(150)

    def paintEvent(self, event):
        label = "ON" if self.isChecked() else "OFF"
        bg_color = qc.Qt.green if self.isChecked() else qc.Qt.red

        radius = 13
        width = 34
        center = self.rect().center()

        painter = qg.QPainter(self)
        painter.setRenderHint(qg.QPainter.Antialiasing)
        painter.setBrush(qg.QColor(0,0,0))

        pen = qg.QPen(qc.Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)
        
        painter.drawText(self.rect(), qc.Qt.AlignTop, "{0}".format(self.text()))
        painter.translate(center)
        painter.drawRoundedRect(qc.QRect(-width, -radius, 2*width, 2*radius), radius, radius)
        painter.setBrush(qg.QBrush(bg_color))
        sw_rect = qc.QRect(-radius, -radius, width + radius, 2*radius)
        if not self.isChecked():
            sw_rect.moveLeft(-width)
        painter.drawRoundedRect(sw_rect, radius, radius)
        painter.drawText(sw_rect, qc.Qt.AlignCenter, label)
        