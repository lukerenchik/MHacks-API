# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 16:10:19 2022

@author: Derek Joslin
"""

import sys
from PyQt5 import QtCore as qc
from PyQt5.QtGui import QColor, QPalette, QPixmap, QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit
import TouchScreenInterface as ts


class MainWindow(QMainWindow):
    
    def __init__(self):
        
        super().__init__()
        
        self.sensor = ts.TouchScreenInterface("COM7",0)

        # Set the cursor to be a red dot
        pixmap = QPixmap(6, 6)
        pixmap.fill(QColor(255, 0, 0))
        self.setCursor(QCursor(pixmap))

        # Create a widget and set it as the central widget
        self.widget = CursorTracker(self)
        self.setCentralWidget(self.widget)

        # Create line edits for entering the x and y coordinates
        #self.xLineEdit = QLineEdit(self)
        #self.yLineEdit = QLineEdit(self)

        # Create a button for moving the cursor
        #self.moveButton = QPushButton("Move Cursor", self)
        #self.moveButton.clicked.connect(self.moveCursor)

        # Create a redbox
        self.TouchCursor = TouchCursor(self)
        #self.setCursor(QCursor(self.redBox))

        # Create layouts to organize the widgets
# =============================================================================
#         hbox = QHBoxLayout()
#         hbox.addWidget(self.xLineEdit)
#         hbox.addWidget(self.yLineEdit)
# =============================================================================

        #vbox = QVBoxLayout()
        #vbox.addLayout(hbox)
        #vbox.addWidget(self.moveButton)

        #self.setLayout(vbox)

        self.TouchUpdater = qc.QTimer()
        self.TouchUpdater.setInterval(10)
        self.TouchUpdater.timeout.connect(lambda: self.moveCursor())
        self.TouchUpdater.start()

    def moveCursor(self):
        # Get the x and y coordinates from the line edits
        position = self.sensor.getTouchPosition()
        
        self.x = int(position[0])
        self.y = int(position[1])

        # Move the cursor to the specified coordinates
# =============================================================================
#         QApplication.setOverrideCursor(QCursor(Qt.BlankCursor))
#         QApplication.restoreOverrideCursor()
#         QApplication.beep()
# =============================================================================

        self.widget.TouchCursor.move(self.x, self.y)
        
        
    def selectPoint(self):
        # do math to make point selection a percentage of the screen for point conversion
        
        self.widget.positionLabel.setText(f"Mouse position: ({self.x}, {self.y})")


    def keyPressEvent(self, event):
        key = event.key()
        
        if key == qc.Qt.Key_Space:
            
            self.selectPoint()
        
        
        
class CursorTracker(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        
        # Create the RedBox label and add it to the widget
        self.TouchCursor = TouchCursor(self)
        self.TouchCursor.move(0, 0)
        
        # Create a label to display the mouse position
        self.positionLabel = QLabel(self)
        self.positionLabel.setFixedSize(300,50)
        self.positionLabel.setText("Mouse position: (0, 0)")

    def mouseMoveEvent(self, event):
        # Get the current cursor position
        x = event.pos().x()
        y = event.pos().y()

        # Move the RedBox label to the cursor position
        self.TouchCursor.move(x, y)
        
    def mousePressEvent(self, event):
        # Update the mouse position label when the mouse moves
        self.positionLabel.setText(f"Mouse position: ({event.x()}, {event.y()})")
       
        
class TouchCursor(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set the background color to red
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor("green"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # Set the size of the label
        self.setFixedSize(5, 5)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
