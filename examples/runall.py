#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 13:20:48 2021

@author: niklas
"""


from codpy.contour_detector import ContourDetector

detector = ContourDetector(meanRefH = 170,
                           stdRefH = 10,
                           boxSize=30.)
detector.detect()