#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 16:44:01 2017

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
API_KEY='3d42933f4c284a3b8dd2c5200e97da00'

#%%
#The info the item recevied from a quick search
'''
This an intermediate dict that is used obtained whena get request is made at the asset link
{
  "analytic_xml": {
    "_permissions": [
      "download"
    ],
    "type": "analytic_xml",
    "_links": {
      "_self": "https://api.planet.com/data/v1/assets/eyJpIjogIjIwMTYwNTMwXzE5MzkwNF8xMDU2MzE4X1JhcGlkRXllLTIiLCAiYyI6ICJSRU9ydGhvVGlsZSIsICJ0IjogImFuYWx5dGljX3htbCIsICJjdCI6ICJpdGVtLXR5cGUifQ",
      "type": "https://api.planet.com/data/v1/asset-types/analytic_xml",
      "activate": "https://api.planet.com/data/v1/assets/eyJpIjogIjIwMTYwNTMwXzE5MzkwNF8xMDU2MzE4X1JhcGlkRXllLTIiLCAiYyI6ICJSRU9ydGhvVGlsZSIsICJ0IjogImFuYWx5dGljX3htbCIsICJjdCI6ICJpdGVtLXR5cGUifQ/activate"
    },
    "md5_digest": null,
    "status": "inactive"
  },
  "visual": {
    "_permissions": [
      "download"
    ],
    "type": "visual",
    "_links": {
      "_self": "https://api.planet.com/data/v1/assets/eyJpIjogIjIwMTYwNTMwXzE5MzkwNF8xMDU2MzE4X1JhcGlkRXllLTIiLCAiYyI6ICJSRU9ydGhvVGlsZSIsICJ0IjogInZpc3VhbCIsICJjdCI6ICJpdGVtLXR5cGUifQ",
      "type": "https://api.planet.com/data/v1/asset-types/visual",
      "activate": "https://api.planet.com/data/v1/assets/eyJpIjogIjIwMTYwNTMwXzE5MzkwNF8xMDU2MzE4X1JhcGlkRXllLTIiLCAiYyI6ICJSRU9ydGhvVGlsZSIsICJ0IjogInZpc3VhbCIsICJjdCI6ICJpdGVtLXR5cGUifQ/activate"
    },
    "md5_digest": null,
    "status": "inactive"
  },
  "udm": {
    "_permissions": [
      "download"
    ],
    "type": "udm",
    "_links": {
      "_self": "https://api.planet.com/data/v1/assets/eyJpIjogIjIwMTYwNTMwXzE5MzkwNF8xMDU2MzE4X1JhcGlkRXllLTIiLCAiYyI6ICJSRU9ydGhvVGlsZSIsICJ0IjogInVkbSIsICJjdCI6ICJpdGVtLXR5cGUifQ",
      "type": "https://api.planet.com/data/v1/asset-types/udm",
      "activate": "https://api.planet.com/data/v1/assets/eyJpIjogIjIwMTYwNTMwXzE5MzkwNF8xMDU2MzE4X1JhcGlkRXllLTIiLCAiYyI6ICJSRU9ydGhvVGlsZSIsICJ0IjogInVkbSIsICJjdCI6ICJpdGVtLXR5cGUifQ/activate"
    },
    "md5_digest": null,
    "status": "inactive"
  },
  "visual_xml": {
    "_permissions": [
      "download"
    ],
    "type": "visual_xml",
    "_links": {
      "_self": "https://api.planet.com/data/v1/assets/eyJpIjogIjIwMTYwNTMwXzE5MzkwNF8xMDU2MzE4X1JhcGlkRXllLTIiLCAiYyI6ICJSRU9ydGhvVGlsZSIsICJ0IjogInZpc3VhbF94bWwiLCAiY3QiOiAiaXRlbS10eXBlIn0",
      "type": "https://api.planet.com/data/v1/asset-types/visual_xml",
      "activate": "https://api.planet.com/data/v1/assets/eyJpIjogIjIwMTYwNTMwXzE5MzkwNF8xMDU2MzE4X1JhcGlkRXllLTIiLCAiYyI6ICJSRU9ydGhvVGlsZSIsICJ0IjogInZpc3VhbF94bWwiLCAiY3QiOiAiaXRlbS10eXBlIn0/activate"
    },
    "md5_digest": null,
    "status": "inactive"
  },
  "analytic": {
    "_permissions": [
      "download"
    ],
    "type": "analytic",
    "_links": {
      "_self": "https://api.planet.com/data/v1/assets/eyJpIjogIjIwMTYwNTMwXzE5MzkwNF8xMDU2MzE4X1JhcGlkRXllLTIiLCAiYyI6ICJSRU9ydGhvVGlsZSIsICJ0IjogImFuYWx5dGljIiwgImN0IjogIml0ZW0tdHlwZSJ9",
      "type": "https://api.planet.com/data/v1/asset-types/analytic",
      "activate": "https://api.planet.com/data/v1/assets/eyJpIjogIjIwMTYwNTMwXzE5MzkwNF8xMDU2MzE4X1JhcGlkRXllLTIiLCAiYyI6ICJSRU9ydGhvVGlsZSIsICJ0IjogImFuYWx5dGljIiwgImN0IjogIml0ZW0tdHlwZSJ9/activate"
    },
    "md5_digest": null,
    "status": "inactive"
  }
}
    
'''
def getAllTiffs(filters):
    with open('subarea.json','w') as file:
        geojson = {
                "type": "FeatureCollection",
                "features": [{
                        "type": "Feature",
                        "properties": {},
                        "geometry": {
                                "type": "Polygon",
                                "coordinates": filters[0]['config'][0]['config']['coordinates']
                                }
                        }]
        }
        file.write(json.dumps(geojson,indent = 2))
    assets = []
    for i in range(0,4):
        assets.append(planetGetAssets(filters[i])['_links']['assets'])
        result =  requests.get(assets[i],
                    auth=HTTPBasicAuth(API_KEY, '')
                    )
        result = result.json()       
        response = requests.post(result['analytic']['_links']['activate'],
                                 auth=HTTPBasicAuth(API_KEY, ''))
        if(response.status_code == 202 or response.status_code == 204):
            print('(getAllTiff)Sucess:Asset[' + str(i) + '] has been activated')
        else:
            print('(getAllTiff)Error:Response ' + str(response))
    downloaded = [False, False, False, False]
    tiffs = [0,0,0,0]
    while(not downloaded[0] and not downloaded[1] and not downloaded[2] and not downloaded[3] ):
        for i in range(0,4):
            result = requests.get(assets[i],
                                    auth=HTTPBasicAuth(API_KEY, '')).json()
            if(result['analytic']['status'] == 'active' and not downloaded[i]):
                download_url = result['analytic']['location']
                vsicurl_url = '/vsicurl/' + download_url
                output_file = 'season_analytic_' + str(i) + '_subarea.tif'
                # GDAL Warp crops the image by our AOI, and saves it
                err = gdal.Warp(output_file, vsicurl_url, dstSRS = 'EPSG:4326', cutlineDSName = 'subarea.json', cropToCutline = True)
                print("(getAllTiff)Sucess: Downloaded image of subarea:" + output_file)
                downloaded[i] = True
                tiffs[i] = err.ReadAsArray()
            else:
                print('(getAllTiff) Message: Asset[' + str(i) + '] is ' + result['analytic']['status'])
    return tiffs
#%% 
def createFilters(coordinates):
    geometry_filter = {
            "type": "GeometryFilter",
            "field_name": "geometry",
            "config": coordinates
            }
    cloud_cover_filter = {
            "type": "RangeFilter",
            "field_name": "cloud_cover",
            "config": {
                        "lte": 0.05
                    }
            }
    year = int(time.strftime('%Y'))
    month = int(time.strftime('%m'))
    #seasons = ['Spring', 'Summer', 'Fall', 'Winter']
    date_range_filters = getDateRangeFilters(month, year)
    filters = []
    for i in range(0, 4):
        filters.append({
                "type": "AndFilter",
                "config": [geometry_filter, date_range_filters[i], cloud_cover_filter]
                })
    return filters
#%%
def getCurrentSeason(month):
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
    
#%%    
def getDateRangeFilters(month, year):
    season = getCurrentSeason(month)
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
#%%
'''
Quickly searches if an imagery staifying the filter occurs on the web server

sample output (a dictionary):
{
 'buckets': [
         {'count': 1, 'start_time': '2016-04-13T00:00:00.000000Z'},
         {'count': 1, 'start_time': '2016-04-17T00:00:00.000000Z'},
         {'count': 1, 'start_time': '2016-04-20T00:00:00.000000Z'},
         {'count': 1, 'start_time': '2016-05-01T00:00:00.000000Z'},
         {'count': 1, 'start_time': '2016-05-18T00:00:00.000000Z'},
         {'count': 1, 'start_time': '2016-05-26T00:00:00.000000Z'},
         {'count': 1, 'start_time': '2016-05-30T00:00:00.000000Z'}],
 'interval': 'day',
 'utc_offset': '+0h'
}
Imagery satisfying this filter occurs for 7 different times
    
'''
def planetGetStats(fil):
    stats_request = {
            "interval": "day",
            "item_types": ['REOrthoTile'], #["PSOrthoTile"],
            "filter": fil
            }
    result = requests.post(
            'https://api.planet.com/data/v1/stats',
            auth=HTTPBasicAuth(API_KEY, ''),
            json=stats_request)
    return result.json()
#%%
'''
Returns an dict that contains all the relavant information about the item. Next step is to get the data using 'assets' link
{
 '_links': {
         '_self': 'https://api.planet.com/data/v1/item-types/REOrthoTile/items/20160530_193904_1056318_RapidEye-2',
         'assets': 'https://api.planet.com/data/v1/item-types/REOrthoTile/items/20160530_193904_1056318_RapidEye-2/assets/',
         'thumbnail': 'https://api.planet.com/data/v1/item-types/REOrthoTile/items/20160530_193904_1056318_RapidEye-2/thumb'
         },
 '_permissions': [
         'assets.analytic:download',
         'assets.visual:download',
         'assets.analytic_xml:download',
         'assets.visual_xml:download',
         'assets.udm:download'
         ],
 'geometry': {
         'coordinates': [
                 [
                         [-122.185304, 37.512141],
                         [-122.187643, 37.295831],
                         [-121.916896, 37.293663],
                         [-121.913778, 37.509956],
                         [-122.185304, 37.512141]
                 ]
            ],
        'type': 'Polygon'
        },
 'id': '20160530_193904_1056318_RapidEye-2',
 'properties': {
         'acquired': '2016-05-30T19:39:04Z',
         'anomalous_pixels': 0,
         'black_fill': 0,
         'catalog_id': '25935369',
         'cloud_cover': 0,
         'columns': 5000,
         'epsg_code': 32610,
         'grid_cell': '1056318',
         'gsd': 6.5,
         'item_type': 'REOrthoTile',
         'origin_x': 571500,
         'origin_y': 4152500.0,
         'pixel_resolution': 5,
         'provider': 'rapideye',
         'published': '2016-08-18T01:56:59Z',
         'rows': 5000,
         'satellite_id': 'RapidEye-2',
         'strip_id': '25948594',
         'sun_azimuth': 157.4014,
         'sun_elevation': 73.64183,
         'updated': '2017-04-14T16:39:36Z',
         'usable_data': 1,
         'view_angle': 3.57447
         },
 'type': 'Feature'}
'''
def planetGetAssets(fil):
    search_request = {
        "interval": "day",
        "item_types": ['REOrthoTile'], #["PSOrthoTile"],
        "filter": fil
        }
    res = requests.post('https://api.planet.com/data/v1/quick-search',
                        auth=HTTPBasicAuth(API_KEY, ''),
                        json=search_request)    
    res_json = res.json()
    #TODO: Extend the search for the relavant AOI for all pages
    result = {}
    for item in res_json['features']:
        if(len(item['_permissions']) != 0 ):
            result = item
            break
    return result
#%%
'''This method will take coordinates as  
coordinates = {
  "type": "Polygon",
       "coordinates": [
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
}
'''
def computeNDVI(tiff):
    tiff = tiff.astype(int)
    ndvi = np.empty((tiff.shape[1], tiff.shape[2]),dtype = float)
    for i in range(0,tiff.shape[1]):
        for j in range(0,tiff.shape[2]):
            if(tiff[4,i,j] + tiff[2,i,j] == 0):
                ndvi[i,j] = 0
            else:
                ndvi[i,j] = (tiff[4,i,j] - tiff[2,i,j])/(tiff[4,i,j] + tiff[2,i,j])
    #plt.imshow(ndvi)
    total = 0
    count = 0
    for i in range(0,ndvi.shape[0]):
        for j in range(0,tiff.shape[1]):
            if(ndvi[i,j] != 0):
                total = total + ndvi[i,j] 
                count = count + 1
    return total/count
def computeGreenCoverGraph(coordinates):
    filters = createFilters(coordinates)
    for i in range(0,4):
        res = planetGetStats(filters[i])
        if(len(res["buckets"]) == 0):
            print("(computeGreenCoverGraph)Error: No images for filter["+ str(i) + "]")
        else:
            print("(computeGreenCoverGraph)Sucess: Found images for filter["+ str(i) + "]")
    tiffs = getAllTiffs(filters)
    ndvi = []
    labels = []
    seasons = ['Spring', 'Summer','Fall', 'Winter']
    current_season = getCurrentSeason(int(time.strftime('%m')))
    for i in range(0,4):
        ndvi.append(computeNDVI(tiffs[(current_season + i)%4]))
        labels.append(seasons[(current_season + i)%4])
        print("(computeGreenCoverGraph)Sucess: Computed NDVI for " + labels[i])
    plt.plot(ndvi)
    print(labels)
#%%
coordinates = {
        "type": "Polygon",
        "coordinates": [
          [
            [
              -122.958984375,
              41.410290812880795
            ],
            [
              -122.9381275177002,
              41.410290812880795
            ],
            [
              -122.9381275177002,
              41.42245604850197
            ],
            [
              -122.958984375,
              41.42245604850197
            ],
            [
              -122.958984375,
              41.410290812880795
            ]
          ]
        ]
      }
#%%
#filters = createFilters(coordinates)
#%%
#tiffs = getAllTiffs(filters)
#%%
computeGreenCoverGraph(coordinates)