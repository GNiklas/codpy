#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 13:11:49 2021

@author: niklas
"""


import os

import cv2


def readImgIn(inDir, imgFile):
    """
    Read input image.

    Parameters
    ----------
    inDir : string.
        absolute input directory.
    imgFile : string.
        input image filename.
        
    Returns
    -------
    imgIn : numpy array
        input image.

    """
    
    # path to image input file
    imgInPath = inDir + os.sep + imgFile
            
    # read BGR input image                
    imgIn = cv2.imread(imgInPath)
    
    return imgIn


def saveImgOut(outDir, imgFile, imgOut):
    """
    Save image with ROIs around objects 

    Parameters
    ----------
    outDir : string
        path to output directory.
    imgFile : string
        input image file name.
    imgOut : numpy array
        output image.
        
    Returns
    -------
    None.

    """
    
    # set output file path
    outPath = outDir + '/' + imgFile[:-4] + '_res' + imgFile[-4:]
    
    # write image to path
    cv2.imwrite(outPath, imgOut)

    
def saveResults(outDir, results):
    """
    Save detection results to file.
    
    Parameters
    ----------
    outDir : string
        path to output directory.
    results : list of lists
        results list for each image.

    Returns
    -------
    None.

    """
    
    header = 'imgName nTotObj nColObj\n'
    
    # check, if output dir exists
    if not os.path.isdir(outDir):
        os.mkdir(outDir)
    
    # go to output dir
    os.chdir(outDir)

    # write results to file
    resFile = open('results.csv', 'w')
    
    resFile.write(header)
    
    for result in results:
        line = result[0] + ' ' + result[1] + ' ' + result[2] + '\n'
        resFile.write(line)
        
    resFile.close()
    
    # go back to working dir
    os.chdir('..')