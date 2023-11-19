# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 15:16:09 2022

@author: Derek Joslin
"""

import cairo
import math

# Set up the canvas
WIDTH, HEIGHT = 500, 500
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)

# Draw the ocean
ctx.rectangle(0, 0, WIDTH, HEIGHT)
ctx.set_source_rgb(0, 0.5, 1)  # Set the color to blue
ctx.fill()


# Draw the boat
ctx.move_to(200, 100)
ctx.line_to(300, 100)
ctx.line_to(350, 150)
ctx.line_to(200, 150)
ctx.close_path()
ctx.set_source_rgb(1, 0.5, 0)  # Set the color to orange
ctx.fill()

# Draw the deck
ctx.rectangle(220, 100, 80, 50)
ctx.set_source_rgb(0.8, 0.8, 0.8)  # Set the color to gray
ctx.fill()

# Draw the mast
ctx.move_to(290, 100)
ctx.line_to(290, 50)
ctx.set_line_width(3)
ctx.set_source_rgb(0.5, 0.5, 0.5)  # Set the color to dark gray
ctx.stroke()

# Draw the sails
ctx.move_to(250, 100)
ctx.line_to(250, 50)
ctx.line_to(350, 50)
ctx.line_to(350, 100)
ctx.close_path()
ctx.set_source_rgb(1, 1, 1)  # Set the color to white
ctx.fill()

# Draw the crew members
ctx.arc(230, 120, 5, 0, 2*math.pi)  # Head
ctx.arc(250, 120, 5, 0, 2*math.pi)  # Head
ctx.arc(270, 120, 5, 0, 2*math.pi)  # Head
ctx.set_source_rgb(0, 0, 0)  # Set the color to black
ctx.fill()


# Move to the upper right corner of the screen
ctx.move_to(WIDTH, 0)

# Draw a line to the bottom left corner of the screen
ctx.line_to(0, HEIGHT)

# Stroke the line on the context
ctx.stroke()


# Save the image
surface.write_to_png("caraval.png")
