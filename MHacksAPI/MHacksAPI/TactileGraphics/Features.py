# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 17:36:47 2023

@author: Derek Joslin

"""

import uuid
import numpy as np
# feature types        

class Feature:
    def __init__(self, width):
        self.width = width
        self.type = "generic feature"
        self.id = str(uuid.uuid4())
        
    def _drawFeature(self, ctx):
        pass

class Point(Feature):
    def __init__(self, coordinates):
        super().__init__(0)
        self.coordinates = coordinates
        self.type = "point"
        
    def _drawFeature(self, ctx, point_size=1):
            x, y = self.coordinates
            ctx.arc(x, y, point_size, 0, 2 * np.pi)
            ctx.fill()
        
class Line(Feature):
    def __init__(self, startPoint, endPoint, width):
        super().__init__(width)
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.type = "line"
    
    def _drawFeature(self, ctx):
        x1, y1 = self.startPoint
        x2, y2 = self.endPoint
        # Set line width
        ctx.set_line_width(self.width)
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.stroke()
        
class Curve(Feature):
    def __init__(self, controlPoints, width):
        super().__init__(width)
        self.controlPoints = controlPoints
        self.type = "curve"
    
    def _drawFeature(self, ctx):
        x1, y1 = self.controlPoints[0]
        x2, y2 = self.controlPoints[1]
        x3, y3 = self.controlPoints[2]
        # Set line width
        ctx.set_line_width(self.width)
        ctx.move_to(x1, y1)
        ctx.curve_to(x1, y1, x2, y2, x3, y3)
        ctx.stroke()

class Triangle(Feature):
    def __init__(self, vertices, width):
        super().__init__(width)
        self.vertices = vertices
        self.type = "triangle"
        
    def _drawFeature(self, ctx):
        x1, y1 = self.vertices[0]
        x2, y2 = self.vertices[1]
        x3, y3 = self.vertices[2]

        ctx.set_line_width(self.width)
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.line_to(x3, y3)
        ctx.close_path()
        ctx.stroke()
        
class Circle(Feature):
    def __init__(self, center, radius, width):
        super().__init__(width)
        self.center = center
        self.radius = radius
        self.type = "circle"
        
    def _drawFeature(self, ctx):
        x, y = self.center
        # Set line width
        ctx.set_line_width(self.width)
        ctx.arc(x, y, self.radius, 0, 2 * np.pi)
        ctx.stroke()
        
class Ellipse(Feature):
    def __init__(self, center, major_axis, minor_axis, angle, width):
        super().__init__(width)
        self.center = center
        self.major_axis = major_axis
        self.minor_axis = minor_axis
        self.angle = angle
        self.type = "ellipse"
    
    def _drawFeature(self, ctx):
        cx, cy = self.center
        ctx.save()
        ctx.translate(cx, cy)
        ctx.rotate(self.angle)
        ctx.scale(self.major_axis, self.minor_axis)
        ctx.arc(0, 0, 1, 0, 2 * np.pi)
        ctx.restore()
        ctx.set_line_width(self.width)
        ctx.stroke()

class Arc(Feature):
    def __init__(self, center, radius, start_angle, end_angle, width):
        super().__init__(width)
        self.center = center
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.type = "arc"
        
    def _drawFeature(self, ctx):
        x, y = self.center
        ctx.set_line_width(self.width)
        ctx.arc(x, y, self.radius, self.start_angle, self.end_angle)
        ctx.stroke()

class Rectangle(Feature):
    def __init__(self, startPoint, endPoint, width):
        super().__init__(width)
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.type = "rectangle"
        
    def _drawFeature(self, ctx):
        x1, y1 = self.startPoint
        x2, y2 = self.endPoint
        # Set line width
        ctx.set_line_width(self.width)
        ctx.rectangle(x1, y1, abs(x2 - x1), abs(y2 - y1))
        ctx.stroke()
        
class Quadrilateral(Feature):
    def __init__(self, vertices, width):
        super().__init__(width)
        self.vertices = vertices
        self.type = "quadrilateral"
        
    def _drawFeature(self, ctx):
        x1, y1 = self.vertices[0]
        ctx.set_line_width(self.width)
        ctx.move_to(x1, y1)
        for x, y in self.vertices[1:]:
            ctx.line_to(x, y)
        ctx.close_path()
        ctx.stroke()

class Polygon(Feature):
    def __init__(self, vertices, width):
        super().__init__(width)
        self.vertices = vertices
        self.type = "polygon"
        
    def _drawFeature(self, ctx):
        x1, y1 = self.vertices[0]
        # Set line width
        ctx.set_line_width(self.width)
        ctx.move_to(x1, y1)
        for x, y in self.vertices[1:]:
            ctx.line_to(x, y)
        ctx.close_path()
        ctx.stroke()
        
class VerticalScrollbar(Line):
    def __init__(self, startPoint, length):
        width = 2
        self.length = length
        self.anchorPoint = startPoint
        #self.endPoint = (startPoint[0] + width, startPoint[1] + self.length)
        barPoint = (startPoint[0] + 2, startPoint[1] + 1)
        super().__init__(startPoint, barPoint, 1)
        self.setPosition(0)
        self.type = "verticalScrollbar"

    def setPosition(self, completionPercentage):
        offset = int(self.length * completionPercentage) + 0.5
        self.startPoint = (self.anchorPoint[0], self.anchorPoint[1] + offset)
        self.endPoint = (self.anchorPoint[0] + 2, self.anchorPoint[1] + offset)

class HorizontalScrollbar(Line):
    def __init__(self, startPoint, length):
        self.length = length
        height = 2
        self.anchorPoint = startPoint
        barPoint = (startPoint[0] + 1, startPoint[1] + 2)
        super().__init__(startPoint, barPoint, 1)
        self.setPosition(0)
        self.type = "horizontalScrollbar"
        
    def setPosition(self, completionPercentage):
        offset = int(self.length * completionPercentage) + 0.5
        self.startPoint = (self.anchorPoint[0] + offset, self.anchorPoint[1])
        self.endPoint = (self.anchorPoint[0] + offset, self.anchorPoint[1] + 2)
        
class Braille(Feature):
    def __init__(self, startCell, brailleString):
        super().__init__(0)
        self.startCell = startCell
        self.brailleString = brailleString
        self.type = "braille"
        self.id = str(uuid.uuid4())

class LayPipe(Feature):
    def __init__(self, circleStartCell, LineStartCell, circleRadius, LineEndCell, Stroke, BrailleText, brailleTextStart):
        super().__init__(0)
        self.circleStartCell = circleStartCell
        self.LineStartCell = LineStartCell
        self.circleRadius = circleRadius
        self.LineEndCell = LineEndCell
        self.Stroke = Stroke
        self.brailleTextStart = brailleTextStart
        self.shaft = Line(self.LineStartCell, self.LineEndCell, self.Stroke)
        self.balls = Circle(self.circleStartCell, self.circleRadius, self.Stroke)
        # self.textComingOut = Braille(brailleTextStart, BrailleText)


    def _drawFeature(self, ctx):
        self.balls._drawFeature(ctx)
        self.shaft._drawFeature(ctx)
        # self._drawFeature(ctx)

        # draw line
        # draw braille