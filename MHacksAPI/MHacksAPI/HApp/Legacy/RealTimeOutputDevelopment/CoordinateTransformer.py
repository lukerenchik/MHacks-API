# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 12:37:33 2023

@author: Derek Joslin

"""

# =============================================================================
# xAbsoluteGuiCoordinate = 0
# yAbsoluteGuiCoordinate = 0
# 
# xRelativeGuiCoordinate = 0
# yRelativeGuiCoordinate = 0
# 
# xTouchCoordinate = 0
# yTouchCoordinate = 0
# 
# =============================================================================

xPinCoordinate = 0
yPinCoordinate = 0

absoluteGuiWidth = 1000
absoluteGuiHeight = 500

relativeGuiWidth = 800
relativeGuiHeight = 400

touchWidth = 255*2
touchHeight = 255

pinWidth = 41
pinHeight = 19


class CoordinateTransformer:
    
    def __init__(self):
        # Dictionary to store the transform functions for each coordinate system
        self.transforms = {}

    def add_transform(self, from_system, to_system, transform_function):
        # Store the transform function in the transforms dictionary
        self.transforms[(from_system, to_system)] = transform_function

    def transform(self, x, y, from_system, to_system):
        # Get the transform function from the transforms dictionary
        transform_function = self.transforms[(from_system, to_system)]

        # Call the transform function and return the result
        return transform_function(x, y)
    
    def get_all_coordinates(self, x, y, from_system):
       # Dictionary to store the coordinates in all coordinate systems
       coordinates = {}

       # Iterate over all coordinate systems
       for to_system in self.transforms.keys():
           # Skip if the from_system and to_system are the same
           if from_system == to_system:
               continue

           # Transform the coordinates and add them to the dictionary
           x_new, y_new = self.transform(x, y, from_system, to_system)
           coordinates[to_system] = (x_new, y_new)

       # Return the dictionary of coordinates
       return coordinates

transformer = CoordinateTransformer()



# =============================================================================
# # Add a transform function to transform from absolute GUI coordinates to relative GUI coordinates
# def absolute_to_relative(x, y):
#     return x - absoluteGuiWidth / 2, y - absoluteGuiHeight / 2
# 
# transformer.add_transform("absolute_gui", "relative_gui", absolute_to_relative)
# 
# # Add a transform function to transform from relative GUI coordinates to touch coordinates
# def relative_to_touch(x, y):
#     return x + relativeGuiWidth / 2, y + relativeGuiHeight / 2
# 
# transformer.add_transform("relative_gui", "touch", relative_to_touch)
# 
# # Add a transform function to transform from touch coordinates to pin coordinates
# def touch_to_pin(x, y):
#     return x + touchWidth / 2, y + touchHeight / 2
# 
# transformer.add_transform("touch", "pin", touch_to_pin)
# 
# =============================================================================

# Get the coordinates in all coordinate systems given the pin coordinates
coordinates = transformer.get_all_coordinates(xPinCoordinate, yPinCoordinate, "pin")

print(coordinates)

# =============================================================================
# 
# 
# # Transform from absolute GUI coordinates to pin coordinates
# x, y = transformer.transform(xAbsoluteGuiCoordinate, yAbsoluteGuiCoordinate, "absolute_gui", "pin")
# print("x:{} y:{} pin coordinates".format(x, y))
# 
# 
# # Transform from touch coordinates to relative GUI coordinates
# x, y = transformer.transform(xTouchCoordinate, yTouchCoordinate, "touch", "relative_gui")
# print("x:{} y:{} relative GUI coordinates".format(x, y))
# 
# 
# # Transform from pin coordinates to absolute GUI coordinates
# x, y = transformer.transform(xPinCoordinate, yPinCoordinate, "pin", "absolute_gui")
# print("x:{} y:{} pin coordinates".format(x, y))
# 
# =============================================================================


