#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 15:41:20 2017

@author: sogoyal
"""
from app.plab.server import Server
from app.plab.geospatial import Geospatial


'''
Takes in coordinates - 
sample coordinate structure - 
coordinates = [
      [
        [
          -121.95789277553557,
          37.417830946910904
        ],
        [
          -121.95595085620879,
          37.416510162308874
        ],
        [
          -121.95349395275115,
          37.41863618802896
        ],
        [
          -121.95355296134949,
          37.41921561543447
        ],
        [
          -121.95789277553557,
          37.417830946910904
        ]
    ]
]
(latitute, longitude)
Returns the 4 images of seasons with NDVI
'''
def ndviImages(coordinates):
    geo = Geospatial('3d42933f4c284a3b8dd2c5200e97da00')
    filters = geo.createFilters(coordinates)
    images = geo.getImages(filters)
    i = 1
    for image in images:
        ndvi = geo.computeNDVI(image)
        geo.writeImageToFile("file" + str(i) + ".png", ndvi)
        i = i + 1

    