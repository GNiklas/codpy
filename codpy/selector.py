#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 13:13:27 2021

@author: niklas
"""


import os

import cv2

import codpy.file_handling as fh
from codpy.mouse import Callbacks


class Selector():
    """
    Class for manual colored object selection.
    
    """
    
    def __init__(self, boxSize = 10, lineWidth = 2):
        """
        Constructor.

        Parameters
        ----------
        boxSize : int, optional
            side length of bounding boxes. The default is 10.
        lineWidth : int, optional
            line width of bounding boxes. The default is 2.
        
        Returns
        -------
        None.

        """
        
        # variables
        self.boxSize = boxSize
        self.lineWidth = lineWidth
        
        # use different colors for bounding boxes
        # grey
        self.boxColorUncolObj = (125, 125, 125)
        # red
        self.boxColorColObj = (0, 0, 255)
    
    def manuallySelectCenters(self,
                              imgIn,
                              uncObjCen = [],
                              colObjCen = []):
        
        """
        Select centers of colored and uncolored objects by mouseclick.
        
        Parameters
        ----------
        imgIn : numpy array
            input image.
        uncObjCen : list, optional
            centers of uncloured objects. The default is [].
        colObjCen : list, optional
            centers of colored objects. The default is [].
            
        Returns
        -------
        imgOut : numpy array
            image with objects marked in it
        uncObjCen : list
            centers of uncloured objects.
        colObjCen : list
            centers of colored objects.
        
        """
        
        title = "select objects"
        cv2.namedWindow(title)
        
        param = [self.boxSize,
                 self.lineWidth,
                 self.boxColorUncolObj,
                 self.boxColorColObj]

        mouseCallback = Callbacks(imgIn, title, param)
        mouseCallback.setCenters(uncObjCen, colObjCen)
        cv2.setMouseCallback(title, mouseCallback.selectFixedROIs)
        
        while True:
            # re-draw bounding boxes in each step
            mouseCallback.markROIs()
    
            key = cv2.waitKey(1) & 0xFF
            
            # deselect all objects with "d"
            if key == ord("d"):
                mouseCallback.setCenters([], [])
                
            # leave on return
            if key == ord("\r"):
                break
            
        # get marked object centers
        uncObjCen, colObjCen = mouseCallback.getCenters()

        # get marked images
        imgOut = mouseCallback.getImgOut()

        cv2.destroyAllWindows()        
        
        return imgOut, uncObjCen, colObjCen
        
    def select(self, relInDir='data', relOutDir = 'results'):
        """
        colored object selection routine using mouse callbacks.

        Parameters
        ----------
        relInDir : string, optional
            relative input directory. The default is "data".
        relOutDir : string, optional
            relative output directory. The default is "results".
            
        Returns
        -------
        None.

        """

        # results to save
        results = []
        
        # absolute input and output directories
        inDir = os.getcwd() + os.sep + relInDir
        outDir = os.getcwd() + os.sep + relOutDir
        
        # go through all images in input dir
        for imgFile in os.listdir(inDir):
            if imgFile.endswith('.jpg'):
                
                # read input image
                imgIn = fh.readImgIn(inDir, imgFile)
                
                # manually select objects
                imgOut, uncObjCen, colObjCen = self.manuallySelectCenters(imgIn)
                
                fh.saveImgOut(outDir, imgFile, imgOut)
                
                # all object centers
                centers = uncObjCen + colObjCen

                # append results of image to list
                results.append([imgFile, str(len(centers)), str(len(colObjCen))])
            
        # save results and used parameters to files
        fh.saveResults(outDir, results)
