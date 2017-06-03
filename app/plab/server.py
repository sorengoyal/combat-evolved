#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 18:35:17 2017

@author: sogoyal
"""
import os
import requests
from requests.auth import HTTPBasicAuth
import json
#from osgeo import gdal
# our demo filter that filters by geometry, date and cloud cover
from osgeo import gdal
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import time
import numpy as np
class Server:
    def __init__(self, api_key):
        self.API_KEY = api_key
        self.session = requests.Session()
        self.session.auth = (self.API_KEY, '')
    
    '''
    Returns a count of items
    '''
    def postStatsRequest(self, filters):
        stats_request = {
            "interval": "day",
            "item_types": ['REOrthoTile'], #["PSOrthoTile"],
            "filter": filters
        }
        result = self.session.post('https://api.planet.com/data/v1/stats',
            json=stats_request)
        return result.json()
    
    '''
    Returns a list of items
    '''    
    def postSearchRequest(self, filters):
        search_request = {
            "interval": "day",
            "item_types": ['REOrthoTile'], #["PSOrthoTile"],
            "filter": filters
        }
        res = self.session.post('https://api.planet.com/data/v1/quick-search',
                            json=search_request)    
        return res.json()
    
    '''
    item -  a dict containg the link to the asset
    returns - a dict containing the asset
    '''
    def getAllAssets(self, item):
        assets =  self.session.get(item['_links']['assets'])
        return assets.json()

    '''
    asset - a single asset of the item, should be dict containing the activation link
    Returns  -  response.status_code == 204 => activation requested posted, 202 => activation successful
    '''
    def postActivationRequest(self, asset):
        response = self.session.post(asset['_links']['activate'])
        return response
    
    '''
    Returns - a string 'Inactive', 'Activating', or 'Active'
    '''
    def getActivationStatus(self, asset):
        response = self.session.get(asset['_links']['_self'])
        return response.json()['status']
  
    #TODO:Complete this and write a test for this method
    def downloadImage(asset, aoi=None, output_file = None):
        download_url = asset['location']
        if(aoi == None):
            #do nothing for now
            return np.empty([0,0,0])
        else:
            vsicurl_url = '/vsicurl/' + download_url
            output_file_name = 'temp.tif'
            # GDAL Warp crops the image by our AOI, and saves it
            err = gdal.Warp(output_file, vsicurl_url, dstSRS = 'EPSG:4326', cutlineDSName = 'subarea.json', cropToCutline = True)
            if(output_file == None):
                os.remove(output_file_name)
            else:
                os.rename(output_file_name, output_file)
            return err.ReadAsArray()    