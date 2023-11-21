# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 14:12:22 2023

@author: Derek Joslin

"""

import Features as f

class FeatureMetadata:
    def __init__(self):
        self.featuresMetadata = {}

    def addPoint(self, coordinates):
        feature = f.Point(coordinates)
        self.featuresMetadata[feature.id] = feature

    def addLine(self, startPoint, endPoint, width):
        feature = f.Line(startPoint, endPoint, width)
        self.featuresMetadata[feature.id] = feature

    def addCurve(self, controlPoints, width):
        feature = f.Curve(controlPoints, width)
        self.featuresMetadata[feature.id] = feature

    def addTriangle(self, vertices, width):
        feature = f.Triangle(vertices, width)
        self.featuresMetadata[feature.id] = feature

    def addCircle(self, startPoint, radius, width):
        feature = f.Circle(startPoint, radius, width)
        self.featuresMetadata[feature.id] = feature

    def addEllipse(self, center, major_axis, minor_axis, angle, width):
        feature = f.Ellipse(center, major_axis, minor_axis, angle, width)
        self.featuresMetadata[feature.id] = feature

    def addArc(self, center, radius, start_angle, end_angle, width):
        feature = f.Arc(center, radius, start_angle, end_angle, width)
        self.featuresMetadata[feature.id] = feature

    def addPolygon(self, vertices, width):
        feature = f.Polygon(vertices, width)
        self.featuresMetadata[feature.id] = feature

    def addRectangle(self, startPoint, endPoint, width):
        feature = f.Rectangle(startPoint, endPoint, width)
        self.featuresMetadata[feature.id] = feature

    def addQuadrilateral(self, vertices, width):
        feature = f.Quadrilateral(vertices, width)
        self.featuresMetadata[feature.id] = feature
        
    def addBraille(self, cellPosition, brailleString):
        feature = f.Braille(cellPosition, brailleString)
        self.featuresMetadata[feature.id] = feature
        
    def addFeature(self, feature):
        self.featuresMetadata[feature.id] = feature

    def sortFeatures(self, attribute, ascending=True):
        sorted_features = sorted(self.featuresMetadata.values(), key=lambda x: getattr(x, attribute), reverse=not ascending)
        self.featuresMetadata = {feature.id: feature for feature in sorted_features}

    def updateFeature(self, feature_id, new_values):
        if feature_id in self.featuresMetadata:
            feature = self.featuresMetadata[feature_id]
            for attr, value in new_values.items():
                if hasattr(feature, attr):
                    setattr(feature, attr, value)
        else:
            raise ValueError(f"Feature with ID '{feature_id}' not found in featuresMetadata.")

    def clearFeatures(self):
        self.featuresMetadata = {}
