#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 13:32:09 2021

@author: niklas
"""


import os
import numpy as np

import cv2

from codpy.selector import Selector


class Detector(Selector):
    """
    Class of basic object detector. Inherits from Selector class.
    Has to be inherited and specified for use.
    
    """
    
    def __init__(self,
                 meanRefH = 150,
                 stdRefH = 10,
                 factor = 1.,
                 boxSize = 10,
                 lineWidth = 2):
        """
        Constructor.

        Parameters
        ----------
        meanRefH : float, optional
            mean of reference H color value. The default is 150.
        stdRefH : float, optional
            standard deviation of reference H color value. The default is 10.
        factor : float, optional
            color limit factor in coloured contour detection.
        boxSize : int, optional
            side length of bounding boxes. The default is 10.
        lineWidth : int, optional
            line width of bounding boxes. The default is 2.
        
        Returns
        -------
        None.

        """
        
        # call inherited constructor
        Selector.__init__(self, boxSize, lineWidth)
        
        # additional variables for colour detection
        self.meanRefH = meanRefH
        self.stdRefH = stdRefH
        self.factor = factor

    def selectColObjCen(self,
                         imgIn,
                         contours,                            
                         centers):
        """
        Select centers of coloured objects. Mean and standard deviation of reference
        H color value will be used to distinguish from non-coloured contours.

        Parameters
        ----------
        imgIn : numpy array
            input image.
        contours : list
            object contours.
        centers : list
            object centers.
            
        Returns
        -------
        uncObjCen : list
            centers of uncoloured objects.
        colObjCen : list
            centers of coloured objects.

        """
        
        # convert input image to grayscale
        imgGray = cv2.cvtColor(imgIn,
                               cv2.COLOR_BGR2GRAY)   
        
        # convert input image to HSV scale
        imgHSV = cv2.cvtColor(imgIn,
                              cv2.COLOR_BGR2HSV)
        
        # lists of centers of uncoloured and coloured objects
        uncObjCen = centers.copy()
        colObjCen = []
                
        # iterate over all object centers
        for i in range(len(centers)):
            # initialize and fill grayscale contour mask
            mask = np.zeros(imgGray.shape, np.uint8)
            cv2.drawContours(mask, contours[i], 0, 255, -1)
            
            # get mean HSV colors and mean H value for each object
            meanColor = cv2.mean(imgHSV, mask = mask)
            meanH = meanColor[0]

            # select colored ojects according to reference mean H value
            if ((meanH >= (self.meanRefH - self.factor * self.stdRefH)) and
                (meanH <= (self.meanRefH + self.factor * self.stdRefH))):
                colObjCen.append(centers[i])
        
        # delete coloured objects from uncoloured ones        
        for x in colObjCen:
            uncObjCen.remove(x)
            
        return uncObjCen, colObjCen

    def saveParameters(self, outDir):
        """
        save used detection parameters

        Parameters
        ----------
        outDir : string
            path to output directory.
            
        Returns
        -------
        None.

        """
        
        header = 'used detection parameters\n'
        
        # check, if output dir exists
        if not os.path.isdir(outDir):
            os.mkdir(outDir)
        
        # go to output dir
        os.chdir(outDir)

        # write parameters to file
        parFile = open('para.dat', 'w')
        
        parFile.write(header)
        line = 'meanRefH: ' + str(self.meanRefH) + '\n'
        parFile.write(line)
        line = 'stdRefH: ' + str(self.stdRefH) + '\n'
        parFile.write(line)
        line = 'factor: ' + str(self.factor) + '\n'
        parFile.write(line)
        
        parFile.close()
        
        # go back to working dir
        os.chdir('..')