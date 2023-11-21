
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 10:43:20 2020

@author: Derek Joslin
"""

import HapticsEngine as he
import GraphicsEngine as ge



class NHAPI:
    
    
    def __init__(self):
        
        
        #create the backend haptics engine
        self.engine = he.HapticsEngine(15, 14)
        self.graphics = ge.GraphicsEngine(self.engine.return_desiredState())
        ## Alex: state = zeros(size(he.return_displaySize))
        
        full = 0
        width = 1
        update = 0
        times = 0


    def display_matrix(matrix, num):
        print("num: {}".format(num))
        print('---------------------------\n')
        print('\n'.join([' '.join(['{:4}'.format(item) for item in row])
                         for row in matrix]))
        print('---------------------------\n')


    def erase(self, onOff):
        if onOff == "on":
            self.graphics.set_output(False)
            print("erase on")
        else:
            self.graphics.set_output(True)
            print("erase off")

    def fill(onOff):
            global full
            if onOff == "on":
                full = 1
                print("fill on")
            else:
                full = 0
                print("fill off")
    
    def direct(onOff):
        global update
        if onOff == "on":
            update = 1
            print("direct on")
        else:
            update = 0
            print("direct off")
    
    def stroke(size):
        global width
        print("stroke is {0}".format(size))
        width = size
    
    def settings():
        global full
        global width
        global update
        print("fill setting {0}".format(full))
        print("stroke setting {0}".format(width))
        print("direct setting {0}".format(update))
        print("connection setting {0}".format(engine.check_connection()))
    
    
    def dot(coord):
        graphics.select_element(coord)
        print("desired state \n")
        display_matrix(engine.return_desiredState(), 0)
        engine.push_desiredState
    
    def line(start, end):
        graphics.make_line(start, end, width)
        print("desired state \n")
        display_matrix(engine.return_desiredState(), 0)
        engine.push_desiredState
    
    def curve(start, control1, control2, end):
        graphics.make_bezierCurve(start, control1, control2, end, width)
        print("desired state \n")
        display_matrix(engine.return_desiredState(), 0)
        engine.push_desiredState
    
    def circle(center, radius):
        graphics.make_circle(center, radius, width, full)
        print("desired state \n")
        display_matrix(engine.return_desiredState(), 0)
        engine.push_desiredState
    
    def rect(corner1, corner2):
        graphics.make_rectangle(corner1, corner2, width, full)
        print("desired state \n")
        display_matrix(engine.return_desiredState(), 0)
        engine.push_desiredState
    
    def triangle(point1, point2, point3):
        graphics.make_polygon(point1, [point2, point3], width, full)
        print("desired state \n")
        display_matrix(engine.return_desiredState(), 0)
        engine.push_desiredState
    
    def polygon(points):
        graphics.make_polygon(points[0], points[1:-1], width, full)
        print("desired state \n")
        display_matrix(engine.return_desiredState(), 0)
        engine.push_desiredState
    
    def braille(point, text):
        graphics.write_braille(point, text)
        print("desired state \n")
        display_matrix(engine.return_desiredState(), 0)
        engine.push_desiredState
    
    def latin(point, text, font, size):
        graphics.write_latin(point, text, font, size)
        print("desired state \n")
        display_matrix(engine.return_desiredState(), 0)
        engine.push_desiredState
    
    def clear():
        graphics.clear()
        print("desired state \n")
        display_matrix(engine.return_desiredState(), 0)
        engine.push_desiredState
        
    ### added at alex request
    def Fclear():
        engine.com.clear_all()
        clear()
    ###
    
    def size():
        engine.pull_displaySize()
        print("The size of the matrix is {}".format(engine.return_displaySize()))
        
    
    def state():
        print("current state \n")
        engine.pull_currentState()
        display_matrix(engine.return_currentState(), 0)
        return engine.return_currentState
    
    def desired():
        print("desired state \n")
        display_matrix(engine.return_desiredState(), 0)
        return engine.return_desiredState()
    
    def setMat(mat):
        engine.set_desiredState(mat)
        engine.push_desiredState
    
    def refresh():
        engine.push_desiredState()
    
    def connect(COM, *args):
        if len(args) > 0:
            if args(0) == 1:
                engine.comLink_on(COM, 1)
            print("comLink check is {}".format(engine.comLink_check()))
        else:
            engine.comLink_on(COM, 0)
    
    def disconnect():
        engine.comLink_off()
        print("comLink check is {}".format(engine.comLink_check()))
