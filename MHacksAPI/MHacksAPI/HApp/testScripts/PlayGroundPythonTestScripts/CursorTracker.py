# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 15:08:22 2022

@author: Derek Joslin
"""



#import RealTimeStateVisualizer as rtsv


import sys
from PyQt5.QtCore import Qt, QPoint, QEvent
from PyQt5.QtGui import QColor, QPixmap, QPainter, QBrush, QCursor, QMouseEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget

import sys
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor, QPixmap, QPainter, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit

class CursorMover(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the size and position of the widget
        self.setGeometry(100, 100, 400, 300)

        # Set the cursor to be a red dot
        pixmap = QPixmap(6, 6)
        pixmap.fill(QColor(255, 0, 0))
        self.setCursor(QCursor(pixmap))

        # Create a label to display the mouse position
        self.positionLabel = QLabel(self)
        self.positionLabel.setText("Mouse position: (0, 0)")

        # Create line edits for entering the x and y coordinates
        self.xLineEdit = QLineEdit(self)
        self.yLineEdit = QLineEdit(self)

        # Create a button for moving the cursor
        self.moveButton = QPushButton("Move Cursor", self)
        self.moveButton.clicked.connect(self.moveCursor)

        # Create a redbox
        self.redBox = RedBox(self)
        #self.setCursor(QCursor(self.redBox))

        # Create layouts to organize the widgets
        hbox = QHBoxLayout()
        hbox.addWidget(self.xLineEdit)
        hbox.addWidget(self.yLineEdit)

        vbox = QVBoxLayout()
        vbox.addWidget(self.positionLabel)
        vbox.addLayout(hbox)
        vbox.addWidget(self.moveButton)

        self.setLayout(vbox)

    def moveCursor(self):
        # Get the x and y coordinates from the line edits
        x = int(self.xLineEdit.text())
        y = int(self.yLineEdit.text())

        # Move the cursor to the specified coordinates
        QApplication.setOverrideCursor(QCursor(Qt.BlankCursor))
        QApplication.restoreOverrideCursor()
        QApplication.beep()
        self.redBox.move(QPoint(x, y))
        self.mouseMoveEvent(QMouseEvent(QEvent.MouseMove, QPoint(x, y), Qt.NoButton, Qt.NoButton, Qt.NoModifier))

    def mouseMoveEvent(self, event):
        # Update the mouse position label when the mouse moves
        self.positionLabel.setText(f"Mouse position: ({event.x()}, {event.y()})")
        # Get the current cursor position
        x = event.pos().x()
        y = event.pos().y()

        # Move the RedBox label to the cursor position
        self.redBox.move(x, y)

class RedBox(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set the size and position of the box
        self.setGeometry(5, 5, 5, 5)

        # Set the background color to red
        self.setStyleSheet("background-color: red;")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = CursorMover()
    widget.show()
    sys.exit(app.exec_())

