#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 22:11:16 2017

@author: sogoyal
"""

import unittest
from plab.server import Server
from plab.geospatial import Geospatial
from tests.filters import posFilter, negFilter, coordinates
import numpy as np

class TestGeospatial(unittest.TestCase):
    def setUp(self):
        self.geospatial = Geospatial('3d42933f4c284a3b8dd2c5200e97da00')
        
    def test_checkExistence(self):
        self.assertTrue(self.geospatial.checkExistence(posFilter))
        self.assertFalse(self.geospatial.checkExistence(negFilter))
        
    def test_createFilters(self):
        filters = self.geospatial.createFilters(coordinates)
        self.assertTrue(len(filters) == 4)
        for fil in filters:
            self.assertTrue(len(fil['config']) == 3)
    
    #@unittest.skip("Remove this whenever this is read")        
    def test_getImage(self):
        with self.assertRaises(AssertionError):
            self.geospatial.getImage(posFilter)
        image = self.geospatial.getImage([posFilter])
        self.assertTrue(len(image) != 0)
        self.assertTrue(image[0].shape[0] != 0)
        with self.assertRaises(Exception):
            self.geospatial.getImage([negFilter])
    
    def test_computeNDVI(self):
        mat = np.zeros([5,2,2], dtype = int)
        mat[4,0,0] = 2
        mat[2,0,0] = 1
        ndvi = self.geospatial.computeNDVI(mat)
        self.assertAlmostEqual(ndvi[0,0], (2-1)/(2+1))
    
    def test_getSeason(self):
        labels = [3, 3, 3, 
                  0, 0,
                  1, 1, 1,
                  2, 2, 2,
                  3]
        for month in range(1, 13):
            self.assertTrue(labels[month - 1] 
                == self.geospatial.getSeason(month))
        