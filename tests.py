#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 20:45:09 2017

@author: sogoyal
"""

from app.tests.TestServerMethods import TestServerMethods
from app.tests.TestGeospatial import TestGeospatial
import unittest

API_KEY = '3d42933f4c284a3b8dd2c5200e97da00'
suite = unittest.TestSuite()
loader = unittest.TestLoader()

suite.addTests(loader.loadTestsFromTestCase(TestServerMethods))
#suite.addTests(loader.loadTestsFromTestCase(TestGeospatial))
runner = unittest.TextTestRunner(verbosity=3)
runner.run(suite)
