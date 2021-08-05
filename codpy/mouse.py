#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 13:12:38 2021

@author: niklas
"""


import cv2


class Callbacks():
    """
    Class of mouse callbacks.
    
    """
    
    def __init__(self,
                 img,
                 title,
                 param = [10, 1, (125, 125, 125), (0, 0, 255)]):
        """
        Constructor.

        Parameters
        ----------
        img : numpy array
            input image.
        title : string
            image title.
        param : list, optional
            parameters to use in mouse callback.
        param[0] : int, optional
            ROI bounding box size. The default is 10.
        param[1] : int, optional
            ROI bounding box linewidth. The default is 1.
        param[2] : tuple, optional
            No-ROI bounding box linecolor (RGB).
            The default is (125, 125, 125).
        param[3] : tuple, optional
            ROI bounding box linecolor (RGB).
            The default is (0, 0, 255).
            
        Returns
        -------
        None.

        """
        
        self.img = img
        self.title = title

        # image for marking objects
        self.imgOut = self.img.copy()
        
        # ROI bounding box parameters
        self.boxSize = param[0]
        self.lineWidth = param[1]
        self.boxColorNoROI = param[2]
        self.boxColorROI = param[3]
        
        # lists of No-ROI and ROI centers
        self.NoROICenters = []
        self.ROICenters = []
        
    def setCenters(self, NoROICenters = [], ROICenters = []):
        """
        Set No-ROI and ROI centers.

        Parameters
        ----------
        NoROICenters : list, optional
            No-ROI centers. The default is [].
        ROICenters : list, optional
            ROI centers. The default is [].

        Returns
        -------
        None.

        """
        
        self.NoROICenters = NoROICenters
        self.ROICenters = ROICenters
    
    def getCenters(self):
        """
        Get No-ROI and ROI centers.

        Returns
        -------
        list
            No-ROI centers.
        list
            ROI centers.

        """
        
        return self.NoROICenters, self.ROICenters
    
    def getImgOut(self):
        """
        Get marked output image.

        Returns
        -------
        imgOut : numpy array
            input image with ROIs around objects.

        """
        
        return self.imgOut
    
    def markROIs(self):
        """
        Mark regions of interest in image.

        Returns
        -------
        None.

        """
        
        # re-new output image
        self.imgOut = self.img.copy()
        
        # mark No-ROIs with bounding box of first color
        for i in range(len(self.NoROICenters)):
            cv2.rectangle(self.imgOut,
                          (int(self.NoROICenters[i][0]-self.boxSize/2),
                           int(self.NoROICenters[i][1]-self.boxSize/2)),
                          (int(self.NoROICenters[i][0]+self.boxSize/2),
                           int(self.NoROICenters[i][1]+self.boxSize/2)),
                          self.boxColorNoROI,
                          self.lineWidth)
        
        # mark ROIs with bounding box of second color
        for i in range(len(self.ROICenters)):
            cv2.rectangle(self.imgOut,
                          (int(self.ROICenters[i][0]-self.boxSize/2),
                           int(self.ROICenters[i][1]-self.boxSize/2)),
                          (int(self.ROICenters[i][0]+self.boxSize/2),
                           int(self.ROICenters[i][1]+self.boxSize/2)),
                          self.boxColorROI,
                          self.lineWidth)
        
        cv2.imshow(self.title, self.imgOut)
    
    def selectROI(self):
        """
        Select ROIs by mouse callback.

        Returns
        -------
        None.

        """
        
        done = False 
        
        # temp lists to delete from during loop
        NoROICentersTemp = self.NoROICenters.copy()
        ROICentersTemp = self.ROICenters.copy()
        
        # check, if center falls within No-ROI list
        for i in range(len(self.NoROICenters)):
            if ((self.center[0] > self.NoROICenters[i][0]-self.boxSize/2) and
                (self.center[1] > self.NoROICenters[i][1]-self.boxSize/2) and                
                (self.center[0] < self.NoROICenters[i][0]+self.boxSize/2) and
                (self.center[1] < self.NoROICenters[i][1]+self.boxSize/2)):
                
                done = True
                
                # if already No-ROI, append to ROIs
                ROICentersTemp.append(self.NoROICenters[i])
                # and delete from temp No-ROI
                del NoROICentersTemp[i]
                break
            
        # if center wasn't found in NoROIs 
        if not done:
            NoROICentersTemp.append(self.center)
        
        # set lists to temp lists
        self.ROICenters = ROICentersTemp
        self.NoROICenters = NoROICentersTemp
        
    def deselectROI(self):
        """
        De-select ROI by mouse callback.

        Returns
        -------
        None.

        """
        
        done = False
        
        # temp lists to delete from during loop
        NoROICentersTemp = self.NoROICenters.copy()
        ROICentersTemp = self.ROICenters.copy()
        
        # check, if center falls within ROI
        for i in range(len(self.ROICenters)):
            if ((self.center[0] > self.ROICenters[i][0]-self.boxSize/2) and
                (self.center[1] > self.ROICenters[i][1]-self.boxSize/2) and                
                (self.center[0] < self.ROICenters[i][0]+self.boxSize/2) and
                (self.center[1] < self.ROICenters[i][1]+self.boxSize/2)):
                
                done = True
                
                # delete de-selected ROI from temp ROI list
                del ROICentersTemp[i]
                # and append to No-ROIs
                NoROICentersTemp.append(self.ROICenters[i])
                break
            
        # if center wasn't found in ROIs
        if not done:
            # check, if center falls within No-ROI
            for i in range(len(self.NoROICenters)):
                if ((self.center[0] > self.NoROICenters[i][0]-self.boxSize/2) and
                    (self.center[1] > self.NoROICenters[i][1]-self.boxSize/2) and                
                    (self.center[0] < self.NoROICenters[i][0]+self.boxSize/2) and
                    (self.center[1] < self.NoROICenters[i][1]+self.boxSize/2)):
                    
                    # delete de-selected ROI from temp ROI list
                    del NoROICentersTemp[i]
                    break
                
        # set lists to temp lists
        self.ROICenters = ROICentersTemp
        self.NoROICenters = NoROICentersTemp
        
    def selectFixedROIs(self, event, x, y, flags, param):
        """
        Select and de-select fixed-sized ROIs by mouse callback.
        Actual method to use in cv2.setMouseCallback.

        Parameters
        ----------
        event : mouse event
            event to trigger mouse callback.
        x : int
            cursor x-coordinate.
        y : int
            cursor y-coordinate.
        flags : string
            flags.
        param : list
            parameter list.

        Returns
        -------
        None.

        """
        
        # select ROI by left mouseclick
        if event == cv2.EVENT_LBUTTONDOWN:           
            self.center = (x, y)
            self.selectROI()
            
        # de-select ROI by right mouseclick
        if event == cv2.EVENT_RBUTTONDOWN:
            self.center = (x, y)
            self.deselectROI()