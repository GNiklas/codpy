#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 13:33:15 2021

@author: niklas
"""


import os
import cv2

import codpy.file_handling as fh
from codpy.detector import Detector


class ContourDetector(Detector):
    """
    Class of object detector by contour extraction.
    Inherits from basic Detector class.
    
    """
    
    def __init__(self,
                 meanRefH = 150,
                 stdRefH = 10,
                 factor = 1.,
                 boxSize = 10,
                 lineWidth = 2,
                 stdX = 5,
                 stdY = 5,
                 loThresh = 100,
                 hiThresh = 200,
                 dilIter = 2,
                 eroIter = 2):
        """
        Constructor.

        Parameters
        ----------
        meanRefH : float, optional
            mean of reference H color value. The default is 150.
        stdRefH : float, optional
            standard deviation of reference H color value. The default is 10.
        factor : float, optional
            color limit factor in colored contour detection.
        boxSize : int, optional
            side length of bounding boxes. The default is 10.
        lineWidth : int, optional
            line width of bounding boxes. The default is 2.
        stdX : int, optional
            x standard deviation of Gaussian blur for edge detection. The default is 5.
        stdY : int, optional
            y standard deviation of Gaussian blur for edge detection. The default is 5.            
        loThresh : int, optional
            lower threshold for edge detection. The default is 100.
        hiThresh : int, optional
            higher threshold for edge detection. The default is 200.
        dilIter : int, optional
            number of dilation iterations for edges. The default is 2.
        eroIter : int, optional
            number of erosion iterations for edges. The default is 2.
            
        Returns
        -------
        None.

        """
        
        # call inherited constructor
        Detector.__init__(self,
                          meanRefH,
                          stdRefH,
                          factor,
                          boxSize,
                          lineWidth)
        
        # additional variables for contour detection
        self.stdX = stdX
        self.stdY = stdY
        self.loThresh = loThresh
        self.hiThresh = hiThresh 
        self.dilIter = dilIter
        self.eroIter = eroIter

    def extractContours(self, imgIn):
        """
        Extract object contours from input image.

        Parameters
        ----------
        imgIn : numpy array
            input image.
            
        Returns
        -------
        contours : list
            object contours.

        """
        
        # convert input image to grayscale
        imgGray = cv2.cvtColor(imgIn,
                               cv2.COLOR_BGR2GRAY)
        
        # blur grayscale image        
        imgBlurred = cv2.GaussianBlur(imgGray, (self.stdX, self.stdY), 0)
        
        # detect edges in grayscale image
        imgCanny = cv2.Canny(imgBlurred,
                           self.loThresh,
                           self.hiThresh)
        
        # dilate and erode to close gaps
        imgDilated = cv2.dilate(imgCanny, None, iterations=self.dilIter)
        imgEroded = cv2.erode(imgDilated, None, iterations=self.eroIter)
        
        # find contours based on detected edges
        contours, _ = cv2.findContours(imgEroded,
                                         cv2.RETR_TREE,
                                         cv2.CHAIN_APPROX_SIMPLE)
    
        return contours
    
    def extractCenters(self, contours):
        """
        Extract centers of object contours.

        Parameters
        ----------
        contours : list
            object contours.
            
        Returns
        -------
        centers : list
            object centers.

        """
        
        centers = [None] * len(contours)
        contoursPoly = [None] * len(contours)
        boxes = [None] * len(contours)
        
        for i in range(len(contours)):
            
            # define bounding boxes around Contours
            contoursPoly[i] = cv2.approxPolyDP(contours[i], 3, True)
            boxes[i] = cv2.boundingRect(contoursPoly[i])
            
            center = (boxes[i][0], boxes[i][1])
            centers[i] = center
            
        return centers
    
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
        line = 'stdX: ' + str(self.stdX) + '\n'
        parFile.write(line)
        line = 'stdY: ' + str(self.stdY) + '\n'
        parFile.write(line)
        line = 'loThresh: ' + str(self.loThresh) + '\n'
        parFile.write(line)        
        line = 'hiThresh: ' + str(self.hiThresh) + '\n'
        parFile.write(line)
        line = 'dilIter: ' + str(self.dilIter) + '\n'
        parFile.write(line)
        line = 'eroIter: ' + str(self.eroIter) + '\n'
        parFile.write(line)
        
        parFile.close()
        
        # go back to working dir
        os.chdir('..')   
        
    def detect(self, relInDir='data', relOutDir = 'results'):
        """
        Object detection routine using contour extraction.

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
                
                # detect object contours
                contours = self.extractContours(imgIn)
                
                # extract object centers
                centers = self.extractCenters(contours)
                
                # select colored objects
                uncObjCen, colObjCen = self.selectColObjCen(imgIn,
                                                            contours,
                                                            centers)
                
                # manually select additional objects
                # or de-select existant ones
                imgOut, uncObjCen, colObjCen = self.manuallySelectCenters(imgIn,
                                                                      uncObjCen,
                                                                      colObjCen)
                
                fh.saveImgOut(outDir, imgFile, imgOut)
                
                # all object centers
                centers = uncObjCen + colObjCen

                # append results of image to list
                results.append([imgFile, str(len(centers)), str(len(colObjCen))])

        # save results and used parameters to files
        fh.saveResults(outDir, results)
        self.saveParameters(outDir)
