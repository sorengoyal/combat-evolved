#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 19:32:56 2017

@author: sogoyal
"""

import unittest
from plab.server import Server
from tests.filters import posFilter, negFilter, coordinates

class TestServerMethods(unittest.TestCase):
    def setUp(self):
        self.server = Server('3d42933f4c284a3b8dd2c5200e97da00')
    
    def test_StatsRequest(self):
        result = self.server.postStatsRequest(posFilter)
        self.assertTrue(len(result) != 0)
    
    def test_SearchRequest(self):
        result = self.server.postSearchRequest(posFilter)
        self.assertTrue(len(result) != 0)
        
    def test_getAllAssets(self):
        item = {
            "_links": {
                "_self": "https://api.planet.com/data/v1/item-types/REOrthoTile/items/20170519_191515_1056318_RapidEye-4",
                "thumbnail": "https://api.planet.com/data/v1/item-types/REOrthoTile/items/20170519_191515_1056318_RapidEye-4/thumb",
                "assets": "https://api.planet.com/data/v1/item-types/REOrthoTile/items/20170519_191515_1056318_RapidEye-4/assets/"
            },
            "_permissions": [
                "assets.analytic:download",
                "assets.visual:download",
                "assets.analytic_xml:download",
                "assets.visual_xml:download",
                "assets.udm:download"
            ],
            "geometry": {
                "coordinates": [
                    [
                        [
                            -122.1909124,
                            37.5166863
                        ],
                        [
                            -121.9080559,
                            37.5144098
                        ],
                        [
                            -121.9113207,
                            37.2891051
                        ],
                        [
                            -122.193332,
                            37.291363
                        ],
                        [
                            -122.1909124,
                            37.5166863
                        ]
                    ]
                ],
                "type": "Polygon"
            },
            "properties": {
                "catalog_id": "31418201",
                "grid_cell": "1056318",
                "black_fill": 0,
                "sun_elevation": 69.63045,
                "acquired": "2017-05-19T19:15:15Z",
                "ground_control": True,
                "cloud_cover": 0,
                "rows": 5000,
                "updated": "2017-05-22T12:12:35Z",
                "usable_data": 1,
                "gsd": 6.5,
                "sun_azimuth": 144.6606,
                "published": "2017-05-20T14:14:25Z",
                "pixel_resolution": 5,
                "view_angle": 0.15156,
                "origin_x": 571500,
                "epsg_code": 32610,
                "strip_id": "31419041",
                "origin_y": 4152500,
                "satellite_id": "RapidEye-4",
                "item_type": "REOrthoTile",
                "provider": "rapideye",
                "anomalous_pixels": 0,
                "columns": 5000
            },
            "id": "20170519_191515_1056318_RapidEye-4",
            "type": "Feature"
        }
        assets = self.server.getAllAssets(item)
        self.assertTrue(len(assets) != 0)
        
    def test_postActivationRequest(self):
        asset = {
            "_permissions": [
              "download"
            ],
            "type": "analytic",
            "_links": {
              "_self": "https://api.planet.com/data/v1/assets/eyJpIjogIjIwMTYwNTMwXzE5MzkwNF8xMDU2MzE4X1JhcGlkRXllLTIiLCAiYyI6ICJSRU9ydGhvVGlsZSIsICJ0IjogImFuYWx5dGljIiwgImN0IjogIml0ZW0tdHlwZSJ9",
              "type": "https://api.planet.com/data/v1/asset-types/analytic",
              "activate": "https://api.planet.com/data/v1/assets/eyJpIjogIjIwMTYwNTMwXzE5MzkwNF8xMDU2MzE4X1JhcGlkRXllLTIiLCAiYyI6ICJSRU9ydGhvVGlsZSIsICJ0IjogImFuYWx5dGljIiwgImN0IjogIml0ZW0tdHlwZSJ9/activate"
            },
            "md5_digest": '',
            "status": "inactive"
          }
        response = self.server.postActivationRequest(asset)
        self.assertTrue(response.status_code == 202 or response.status_code == 204)
    
    def test_getActivationStatus(self):
        asset = {
            "_permissions": [
              "download"
            ],
            "type": "analytic",
            "_links": {
              "_self": "https://api.planet.com/data/v1/assets/eyJpIjogIjIwMTYwNTMwXzE5MzkwNF8xMDU2MzE4X1JhcGlkRXllLTIiLCAiYyI6ICJSRU9ydGhvVGlsZSIsICJ0IjogImFuYWx5dGljIiwgImN0IjogIml0ZW0tdHlwZSJ9",
              "type": "https://api.planet.com/data/v1/asset-types/analytic",
              "activate": "https://api.planet.com/data/v1/assets/eyJpIjogIjIwMTYwNTMwXzE5MzkwNF8xMDU2MzE4X1JhcGlkRXllLTIiLCAiYyI6ICJSRU9ydGhvVGlsZSIsICJ0IjogImFuYWx5dGljIiwgImN0IjogIml0ZW0tdHlwZSJ9/activate"
            },
            "md5_digest": '',
            "status": "inactive"
          }
        response = self.server.getActivationStatus(asset)
        self.assertTrue(response == 'activating' or response == 'active')
    
    def test_downloadImage(self):
        asset = {
            "_links": {
                "activate": "https://api.planet.com/data/v1/assets/eyJpIjogIjIwMTcwNTE5XzE5MTUxNV8xMDU2MzE4X1JhcGlkRXllLTQiLCAiYyI6ICJSRU9ydGhvVGlsZSIsICJ0IjogImFuYWx5dGljIiwgImN0IjogIml0ZW0tdHlwZSJ9/activate",
                "type": "https://api.planet.com/data/v1/asset-types/analytic",
                "_self": "https://api.planet.com/data/v1/assets/eyJpIjogIjIwMTcwNTE5XzE5MTUxNV8xMDU2MzE4X1JhcGlkRXllLTQiLCAiYyI6ICJSRU9ydGhvVGlsZSIsICJ0IjogImFuYWx5dGljIiwgImN0IjogIml0ZW0tdHlwZSJ9"
            },
            "type": "analytic",
            "expires_at": "2017-06-04T18:27:40.884133",
            "_permissions": [
                "download"
            ],
            "md5_digest": "e0b913dc48aa91f6c07b30d16017f8db",
            "location": "https://api.planet.com/data/v1/download?token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJvK0M3MlU4UnZxRnhHeUVXL0hKcmhWN2poNEZxM1Z3V2ZMOWVxSzBKaVlnNUNKY3hjSFFweWtMSGIxMU9DWFVKLzk3eC9sMnBBMnNzdXhia2ZxRXFIdz09IiwiaXRlbV90eXBlX2lkIjoiUkVPcnRob1RpbGUiLCJ0b2tlbl90eXBlIjoidHlwZWQtaXRlbSIsImV4cCI6MTQ5NjYwMDg2MCwiaXRlbV9pZCI6IjIwMTcwNTE5XzE5MTUxNV8xMDU2MzE4X1JhcGlkRXllLTQiLCJhc3NldF90eXBlIjoiYW5hbHl0aWMifQ._3g5cpTYzhphMTyY7tJqEkXfO6sMLNUCfkrSx7pyZRCP_2O9igytfvIh8ddyk-XptCVd1VbBzjZwDoV2tr2ZfA",
            "status": "active"
        }
        img = self.server.downloadImage(asset, aoi = coordinates)
        self.assertTrue(img.shape[0] == 5)        
