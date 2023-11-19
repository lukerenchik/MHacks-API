# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 15:11:42 2022

@author: derek
"""

import cairo

# Set up the canvas
WIDTH, HEIGHT = 500, 500
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)

# Draw the boat
ctx.move_to(200, 100)
ctx.line_to(300, 100)
ctx.line_to(350, 150)
ctx.line_to(200, 150)
ctx.close_path()
ctx.set_source_rgb(0, 0, 0)  # Set the color to black
ctx.fill()

# Draw the sails
ctx.move_to(250, 100)
ctx.line_to(250, 50)
ctx.line_to(350, 50)
ctx.line_to(350, 100)
ctx.close_path()
ctx.set_source_rgb(1, 1, 1)  # Set the color to white
ctx.fill()

# Save the image
surface.write_to_png("boat.png")
