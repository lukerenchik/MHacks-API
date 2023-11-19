# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 13:46:06 2023

@author: Derek Joslin

"""


class CoordinateTransformer:
    def __init__(self, *bounded_regions):
        self.bounded_regions = bounded_regions
        self.transforms = {}
        
        # Generate the transform for each bounded region
        for region in bounded_regions:
            width = region["width"]
            height = region["height"]
            
            transform = [[width/2, 0, width/2], [0, height/2, height/2], [0, 0, 1]]
            
            self.transforms[region["name"]] = transform
    
    
    def transform(self, x, y, region_name):
        # Get the transform for the specified region
        transform = self.transforms[region_name]
        
        # Apply the transform to the coordinates
        transformed_x = transform[0][0] * x + transform[0][1] * y + transform[0][2]
        transformed_y = transform[1][0] * x + transform[1][1] * y + transform[1][2]
        
        # Return a dictionary with the transformed coordinates for all bounded regions
        transformed_coords = {}
        for region in self.bounded_regions:
            if region["name"] == region_name:
                continue
            transformed_coords[region["name"]] = (transformed_x, transformed_y)
        return transformed_coords





# Create the bounded regions
region1 = {"name": "bounded region 1", "width": 41, "height": 19}
region2 = {"name": "bounded region 2", "width": 255*2, "height": 255}
region3 = {"name": "bounded region 3", "width": 1000, "height": 500}

# Create an instance of the CoordinateTransformer class
transformer = CoordinateTransformer(region1, region3)

# Transform the coordinates (10, 20) from bounded region 1 to all other bounded regions
transformed_coords = transformer.transform(41, 19, "bounded region 1")

print(transformed_coords)

