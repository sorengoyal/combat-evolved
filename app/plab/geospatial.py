#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 11:48:27 2017

@author: sogoyal
"""
import logging
import os
import requests

import json
import time
#from osgeo import gdal
# our demo filter that filters by geometry, date and cloud cover
from osgeo import gdal
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from app.plab.server import Server

class Geospatial:
    def __init__(self, api_key):
        self.server = Server(api_key)
        self.seasonOrder = []
        self.logger = logging.getLogger("root."+ __name__)
        
    def checkExistence(self, fil):
        result = self.server.postStatsRequest(fil)
        if(len(result) == 0):
            return False
        result = self.server.postSearchRequest(fil)
        #TODO:Can be improved by searching for an image with the least amount of cloud cover
        for item in result:
            if(len(item['_permissions']) != 0 ):
                return True
    '''
    The format of the coordinates should be (longitude, latitude)
    '''
    def createFilters(self, coordinates):
        
        geometry_filter = {
            "type": "GeometryFilter",
            "field_name": "geometry",
            "config": {
                "type": "Polygon",
                "coordinates": coordinates
                }
            }
        cloud_cover_filter = {
                "type": "RangeFilter",
                "field_name": "cloud_cover",
                "config": {
                            "lte": 0.05
                        }
                }
        month = int(time.strftime('%m'))
        year = int(time.strftime('%Y'))
        curSeason = self.getSeason(month)
        self.seasonOrder = [(i + curSeason)%4 for i in range(0, 4)]
        date_range_filters = self.getDateRangeFilters(month, year)
        filters = []
        for i in range(0, 4):
            filters.append({
                    "type": "AndFilter",
                    "config": [geometry_filter, date_range_filters[i], cloud_cover_filter]
                    })
        return filters
        
    def getImage(self, fil):
        items = self.server.postSearchRequest(fil)
        if(len(items) == 0):
            raise Exception("No Items found for filter:\n" + json.dumps(fil, indent=2))
        item = {}
        for i in items:
            if(len(i['_permissions']) != 0 ):
                item = i
        asset = self.server.getAllAssets(item)['analytic']
        response = self.server.postActivationRequest(asset)
        if(not(response.status_code == 204 or response.status_code == 202)):
            raise Exception("Response Code: " + str(response.status_code) +"Could not activate asset:\n" + json.dumps(asset, indent=2))    
        status = 'activating'
        while(status == 'activating'):
            status = self.server.getActivationStatus(asset)
        self.logger.debug("getImages Activated Asset")
        asset = self.server.getAllAssets(item)['analytic']
        coordinates = fil['config'][0]['config']['coordinates']
        image = self.server.downloadImage(asset, aoi = coordinates)
        self.logger.info("getImage Downloaded image")
        self.logger.debug("getImage shape of image:" + str(image.shape))
        return image
    '''
    image - A minimum takes a multispectral image of shape - [bands, height*, width*]
    For REOrthoTile
    '''
    def computeNDVI(self, image):
        image = image.astype(int)
        ndvi = np.empty((image.shape[1], image.shape[2]),dtype = float)
        mask = np.ndarray(ndvi.shape)
        for i in range(0,image.shape[1]):
            for j in range(0,image.shape[2]):
                if(image[4,i,j] + image[2,i,j] == 0):
                    ndvi[i,j] = 0 #Non-Pixel marker
                    mask[i,j] = 0
                else:
                    ndvi[i,j] = (image[4,i,j] - image[2,i,j])/(image[4,i,j] + image[2,i,j])
                    mask[i,j] = 1
        return (ndvi, mask)

    def getSeason(self, month):
        '''
        Spring - 04 - 05
        Summer - 06 to 08
        Fall - 09 to 11
        Winter - 12 - 03
        
        '''
        if(4 <= month and month <= 5):
            return 0
        elif(6 <= month and month <= 8 ):
            return 1
        elif(9 <= month and month <= 11):
            return 2
        elif(0 <= month%12 and month%12 <= 3):
            return 3
    
    def getDateRangeFilters(self, month, year):
        season = self.getSeason(month)       
        if(season == 3 and month <= 3):
            year = year - 1
        filters = []
        filters.append({
            "type": "DateRangeFilter",
            "field_name": "acquired",
            "config": {
                    "gte": str(year-1) + "-04-01T00:00:00.000Z",
                    "lte": str(year-1) + "-05-31T00:00:00.000Z"
                    }
            })
        filters.append({
            "type": "DateRangeFilter",
            "field_name": "acquired",
            "config": {
                    "gte": str(year-1) + "-06-01T00:00:00.000Z",
                    "lte": str(year-1) + "-08-31T00:00:00.000Z"
                    }
            })
        filters.append({
            "type": "DateRangeFilter",
            "field_name": "acquired",
            "config": {
                    "gte": str(year-1) + "-09-01T00:00:00.000Z",
                    "lte": str(year-1) + "-11-30T00:00:00.000Z"
                    }
            })
        filters.append({
            "type": "DateRangeFilter",
            "field_name": "acquired",
            "config": {
                    "gte": str(year-1) + "-12-01T00:00:00.000Z",
                    "lte": str(year) + "-03-31T00:00:00.000Z"
                    }
            })
        if(season > 0): #spring dates change unless season is spring
            filters[0]['config'] = {
                    "gte": str(year) + "-04-01T00:00:00.000Z",
                    "lte": str(year) + "-05-31T00:00:00.000Z"
                    }
        if(season > 1): #summer dates change for all season beyond summer
            filters[1]['config'] = {
                    "gte": str(year) + "-06-01T00:00:00.000Z",
                    "lte": str(year) + "-08-31T00:00:00.000Z"
                    }
        if(season > 2): #summer dates change for all season beyond summer
            filters[2]['config'] = {
                    "gte": str(year) + "-09-01T00:00:00.000Z",
                    "lte": str(year) + "-11-31T00:00:00.000Z"
                    }
        return filters
    #def readImageFromFile(self):
        
    def writeImageToFile(self, filename, image, mask = None):
        assert(len(image.shape) <= 3) #Maximum a 3D array
        if(len(image.shape) == 3): #Maximum of 3 colors
            image.shape[0] <=3
        self.logger.info("writeImageToFile Image Shape " + str(image.shape))
        self.logger.info("writeImageToFile Mask Shape " + str(mask.shape))         
        plt.imsave(fname = filename, arr = image, cmap = plt.get_cmap('Greens'))
        if(mask != None):
            image = plt.imread(filename)
            new_image = np.ndarray(image.shape, dtype = float)
            new_image[:,:,0:3] = image[:,:,0:3]
            new_image[:,:,3] = image[:,:,3]*mask[:,:]
            plt.imsave(fname = filename, arr = new_image)
        self.logger.info("writeImageToFile Wrote file " + filename)         