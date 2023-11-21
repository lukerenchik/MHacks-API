# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 09:33:59 2022

@author: Derek Joslin
"""


""" SlidesToolSelector Class """

import SlidesTool as st

class SlidesToolSelector():


    def __init__(self):

        self.Tools = st.SlidesTools()

        # create a dictionary to hold functions from SlidesTools


        # create a dictionary to hold parameters from SlidesTools




    def selectTool(self, tool):
        # selects the appropriate tool from the tools dictionary




    def inputParamet(self, parameter):
        # gives an input parameter and adds it to the parameter dictionary

        # executes the selected tool's function when the parameters are met


#Implement the functions in the SlidesToolSelector Class to Select a tool and then take in parameters for that tool and execute the tool when it's parameters have been filled.

""" SlidesTools Class """

class SlidesTools():

    def __init__(self):
        self.toolSelector = nh.NHAPI()

    #cursor tools
    def erase(self):
        self.toolSelector.erase("on/off-E")

    def fill(self):
        self.toolSelector.fill("on/off-F")

    def stroke(self):
        self.toolSelector.stroke("({stroke size})")

    #shape tools
    def dot(self, coord1):
        self.toolSelector.dot(coord1)

    def cell(self, coord1):
        self.toolSelector.cell(coord1)

    def line(self, coord2, coord1):
        self.toolSelector.line(coord2, coord1)

    def curve(self, coord4, coord3, coord2, coord1):

        self.toolSelector.curve(coord4, coord3, coord2, coord1)

    def circle(self, coord1, radius):
        self.toolSelector.circle(coord1, radius)

    def rect(self, coord2, coord1):
        self.toolSelector.rect(coord2, coord1)

    def triangle(self, coord3, coord2, coord1):
        self.toolSelector.triangle(coord3, coord2, coord1)

    def polygon(self, list1):
        self.toolSelector.polygon(list1)

    #character tools
    def braille(self, coord1, text):
        self.toolSelector.braille(coord1, text)

    #load tools
    def load(self, matrix):
        self.toolSelector.setMat(matrix)

    #control actions
    def clear(self):
        self.toolSelector.clear()

    def Fclear(self):
        self.toolSelector.Fclear()

    def times(self, now):
        self.toolSelector.times(now)

    def setMat(self, matrix):
        self.toolSelector.setMat(matrix)

    #board actions
    def connect(self, com):

        self.toolSelector.connect(com)

    def connectTouch(self, com):

        self.toolSelector.connectTouch(com)

    def disconnect(self):

        self.toolSelector.disconnect()

    def disconnectTouch(self):

        self.toolSelector.disconnectTouch()

    def refresh(self):

        self.toolSelector.refresh()

    def direct(self, on_off):

        self.toolSelector.direct(on_off)

    #cursor tools
    def selectErase(self):

        self.toolSelector.erase("on/off-E")

    #character tools
    def selectCharacter(self, coord1):

        self.toolSelector.dot(coord1)

    #load tools
    def selectDot(self, coord1):

        self.toolSelector.dot(coord1)

    #control tools
    def selectClear(self):

        self.toolSelector.clear()

    #board tools
    def selectConnect(self, com):

        self.toolSelector.connect(com)

    #help tools
    def selectSettings(self):

        self.toolSelector.settings()

    #misc tools
    def selectOnOff(self, onOff):

        self.toolSelector.onOff(onOff)

    def selectStrokeSize(self, strokeSize):

        self.toolSelector.strokeSize(strokeSize)

    def selectFontSize(self, fontSize):

        self.toolSelector.fontSize(fontSize)

    def selectDirectOnOff(self, onOff):

        self.toolSelector.directOnOff(onOff)

    def selectEraseOnOff(self, onOff):

        self.toolSelector.eraseOnOff(onOff)

    def selectFillOnOff(self, onOff):

        self.toolSelector.fillOnOff(onOff)

# create a dictionary toolFunctions and fill it with all functions in the SlidesTools class.

# create a dictionary to hold functions from SlidesTools
self.tool_functions = {}

# create a dictionary to hold parameters from SlidesTools
self.tool_parameters = {}


Now Create a dictionary of dictionaries called toolParameters that stores the parameters of each method in tool_functions.

import inspect

class SlidesTools():

    def __init__(self):
        self.toolSelector = nh.NHAPI()

    #cursor tools
    def erase(self):
        self.toolSelector.erase("on/off-E")

    # other methods here

tool_functions = {}
toolParameters = {}

# get a list of all methods in the SlidesTools class
methods = inspect.getmembers(SlidesTools, predicate=inspect.ismethod)

# iterate over the list of methods and add each method to the dictionary
for name, method in methods:
    tool_functions[name] = method

    # get the list of parameters for the current method
    params = inspect.signature(method).parameters

    # create a dictionary for the current method that maps each parameter to its default value (if any)
    method_params = {param: params[param].default for param in params}

    # add the dictionary of parameters for the current method to the toolParameters dictionary
    toolParameters[name] = method_params

# print the toolParameters dictionary
print(toolParameters)


""" Input Parameter Function """

def inputParameters(self, parameterKey, toolFunctions, toolParameters, selectedTool):
    # Given a dictionary of tool Functions and a dictionary of tool Parameters

    # use the parameterKey and selectedTool to add the parameter to a list of parameters a execute the tool's function when the parameter list is full.


Complete the inputParameter function to take in parameters and auto execute the selected tool when the parameters have been met.



def testFunc(input1, input2, input3, input4):

    print(input1)
    print(input2)
    print(input3)
    print(input4)


kwargs = {input1 :"a",
          input2 : "b",
          input3 :"c",
          input4 : "d"}

testFunc(kwargs)

How do I pass in kwargs as the parameters?

# Import the OrderedDict class from the collections module
from collections import OrderedDict

# Create an ordered dictionary
my_dict = OrderedDict()
my_dict['a'] = 1
my_dict['b'] = 2
my_dict['c'] = 3

# Get a list of tuples containing key-value pairs
items = my_dict.items()

# Extract the keys and values into separate lists
keys = [k for k, v in items]
values = [v for k, v in items]

# Print the keys and values
print(keys)  # Output: ['a', 'b', 'c']
print(values)  # Output: [1, 2, 3]

class HAppMainWindow(qw.QMainWindow):
    def __init__(self):

        # Create superclassed QWidget RealTimeVisualization
        self.RealTimeVisualization = rtsv.RealTimeStateVisualizer(state, displaySize)
        self.setCentralWidget(self.RealTimeVisualization)


    def mousePressEvent(self, event):
            x = event.x()
            y = event.y()

            self.cursor_position_label.setText("Cursor position: ({}, {})".format(x, y))

Rewrite this mousePressEvent to give x and y as a percentage of the RealTimeVisualization QWidget window size.


RealTimeVisualization has two properties nRows and nColumns, add a conversion to the x and y of tho mousePressEvent which returns the row and column position in RealTimeVisualization based on the mouse click.
