# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 10:43:20 2020

@author: Derek Joslin

"""

import HapticsEngine as he
import GraphicsEngine as ge

class NHAPI(he.HapticsEngine):

    def __init__(self, name):
        #create the backend haptics engine
        
        # Get the number of rows and columns of the tactile display
        super().__init__(name)
        
        self.makeGraphics()
        self.echo = 0

        self.full = 0
        self.width = 1
        self.autoRefresh = 0
        
    def makeGraphics(self):
        """ if the haptics engine is connected then create a virtual graphics object """
        self.graphics = ge.GraphicsEngine(self.return_desiredState())

    def display_matrix(self, matrix, num):
        self.__apiPrint("num: {}".format(num))
        self.__apiPrint('---------------------------\n')
        self.__apiPrint('\n'.join([' '.join(['{:4}'.format(item) for item in row])
                         for row in matrix]))
        self.__apiPrint('---------------------------\n')

    def displayMatrix(self, matrix):
        print('---------------------------\n')
        print('\n'.join([' '.join(['{:4}'.format(item) for item in row])
                         for row in matrix]))
        print('---------------------------\n')

    def erase(self, onOff):
        if onOff == "on":
            self.graphics.set_output(False)
            self.__apiPrint("erase on")
        else:
            self.graphics.set_output(True)
            self.__apiPrint("erase off")

    def fill(self, onOff):
            if onOff == "on":
                self.full = 1
                self.__apiPrint("fill on")
            else:
                self.full = 0
                self.__apiPrint("fill off")

    def direct(self, onOff):
        if onOff == "on":
            self.autoRefresh = 1
            self.__apiPrint("direct on")
        else:
            self.autoRefresh = 0
            self.__apiPrint("direct off")

    def stroke(self, size):
        self.__apiPrint("stroke is {0}".format(size))
        self.width = size

    def settings(self):
        self.__apiPrint("fill setting {0}".format(self.full))
        self.__apiPrint("stroke setting {0}".format(self.width))
        self.__apiPrint("direct setting {0}".format(self.autoRefresh))
        self.__apiPrint("connection setting {0}".format(self.comLink_check()))


    def dot(self, coord):
        self.graphics.select_element(coord)
        self.__apiPrint("desired state \n")
        self.display_matrix(self.return_desiredState(), 0)
        if self.autoRefresh:
            self.refresh()
            
    def cell(self, coord):
        self.graphics.select_cell(coord)
        self.__apiPrint("desired state \n")
        self.display_matrix(self.return_desiredState(), 0)
        if self.autoRefresh:
            self.refresh()
        

    def line(self, start, end):
        self.graphics.make_line(start, end, self.width)
        self.__apiPrint("desired state \n")
        self.display_matrix(self.return_desiredState(), 0)
        if self.autoRefresh:
            self.refresh()

    def curve(self, start, control1, control2, end):
        self.graphics.make_bezierCurve(start, control1, control2, end, self.width)
        self.__apiPrint("desired state \n")
        self.display_matrix(self.return_desiredState(), 0)
        if self.autoRefresh:
            self.refresh()

    def circle(self, center, radius):
        self.graphics.make_circle(center, radius, self.width, self.full)
        self.__apiPrint("desired state \n")
        self.display_matrix(self.return_desiredState(), 0)
        if self.autoRefresh:
            self.refresh()

    def rect(self, corner1, corner2):
        self.graphics.make_rectangle(corner1, corner2, self.width, self.full)
        self.__apiPrint("desired state \n")
        self.display_matrix(self.return_desiredState(), 0)
        if self.autoRefresh:
            self.refresh()

    def triangle(self, point1, point2, point3):
        self.graphics.make_polygon(point1, [point2, point3], self.width, self.full)
        self.__apiPrint("desired state \n")
        self.display_matrix(self.return_desiredState(), 0)
        if self.autoRefresh:
            self.refresh()

    def polygon(self, points):
        self.graphics.make_polygon(points[0], points[1:-1], self.width, self.full)
        self.__apiPrint("desired state \n")
        self.display_matrix(self.return_desiredState(), 0)
        if self.autoRefresh:
            self.refresh()

    def braille(self, point, text):
        self.clear()
        self.graphics.write_braille(point, text)
        self.__apiPrint("desired state \n")
        self.display_matrix(self.return_desiredState(), 0)
        if self.autoRefresh:
            self.refresh()

    def latin(self, point, text, font, size):
        self.graphics.write_latin(point, text, font, size)
        self.__apiPrint("desired state \n")
        self.display_matrix(self.return_desiredState(), 0)
        if self.autoRefresh:
            self.refresh()

    def clear(self):
        self.graphics.clear()
        self.__apiPrint("desired state \n")
        self.display_matrix(self.return_desiredState(), 0)
        if self.autoRefresh:
            self.refresh()

    ### added at alex request
    def Fclear(self):
        if self.comLink_check():
            self.com.forceClearAll()
        self.clear()
    ###

    #gets size of the chip and displays
    def size(self):
        if self.comLink_check():
            self.pull_displaySize()
        self.__apiPrint("The size of the matrix is {}".format(self.return_displaySize()))
        return self.return_displaySize()

    #gets the current state and displays it
    def state(self):
        self.__apiPrint("current state \n")
        if self.comLink_check():
            self.pull_currentState()
        self.display_matrix(self.return_currentState(), 0)
        return self.return_currentState()

    #gets the desired state and displays it
    def desired(self):
        self.__apiPrint("desired state \n")
        self.set_desiredState(self.graphics.state)
        self.display_matrix(self.return_desiredState(), 0)
        return self.return_desiredState()

    def setMat(self, mat):
        self.set_desiredState(mat)
        self.makeGraphics()
        if self.autoRefresh:
            self.refresh()

    def refresh(self):
        self.push_desiredState()
        self.__apiPrint("refreshed")
        
    def cursorPos(self):
        self.getCursorPosition()
        self.__apiPrint("cursor position is {}".format(self.getCursorPosition()))

    def connectTouch(self, name, COM):
        self.connectTouchScreen(name, COM)
        self.__apiPrint("the touch screen has been connected")

    def connect(self, COM, *args):
        if len(args) > 0:
            if args[0] == 1:
                self.comLink_on(COM, 1)
                self.echo = 1
            else:
                self.comLink_on(COM, 0)
                self.echo = 0
            self.__apiPrint("comLink check is {}".format(self.comLink_check()))
        else:
            self.comLink_on(COM, 0)
            self.echo = 0
        self.size()
        self.makeGraphics()

    def disconnect(self):
        self.comLink_off()
        self.__apiPrint("comLink check is {}".format(self.comLink_check()))
        
        
    def disconnectTouch(self):
        self.disconnectTouchScreen()
        self.__apiPrint("touchLink check is {}".format(self.checkTouchLink()))

        
        
    def __apiPrint(self, text):
        if self.echo:
            print(text)
        else:
            pass
