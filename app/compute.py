#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 15:41:20 2017

@author: sogoyal
"""
from app.plab.geospatial import Geospatial
import time

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
    graph = []#{"Spring": 0, "Summer": 0, "Fall": 0, "Winter": 0}
    images = []
    masks = []
    maxvalue = 0
    for i in range(0,1):
        image = geo.getImage(filters[i])
        ndvi, mask = geo.computeNDVI(image)
        graph.append(ndvi.sum()/mask.sum())
        images.append(image)
        masks.append(mask)
        if(maxvalue < ndvi.max()):
            maxvalue = ndvi.max()
    for i in range(0,1):
        image = images[i]
        mask = masks[i]
        for m in range(0,image.shape[0]):
            for n in range(0,image.shape[1]):
                image[m,n] = 255*image[m,n]/maxvalue
        geo.writeImageToFile("app/images/file" + str(i) + ".png", ndvi, mask)
