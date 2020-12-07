# ****************************************************************
# Author: Sheldon Dorgelo
# Date (last edited): 26/10/2020
# Purpose: takes in the data to be processed, decides which
#          process to use and returns the processed data
# ****************************************************************

import Publication
import Orbits
import SubtractAverage
import ZoomImage
import Photometry
import DataObject # for accessing data
import DataOutput # for displaying processed data
import InvalidFlagException # used when this file comes across an invalid flag
import numpy as np # used for data processing

# filter images and direct other components to perform operations on the data
def processData(data):   
    flag = data.getFlag()

    # figures out which processing needs to be done based on the flag
    if(flag == 'CheckPixels'): # process = check pixels
        ZoomImage.checkPixels(data)
        DataOutput.outputDataToGUI(data)
    elif(flag == 'Publication'): # process = publication
        detectCandidates(data)
        Publication.publication(data) #pass data object to publication component
        DataOutput.outputDataToGUI(data)
    elif(flag == 'Orbits'): # process = orbits
        detectCandidates(data)
        Orbits.orbits(data)
        DataOutput.outputDataToGUI(data)
    elif(flag == 'Simulate'): # process = simulate
        simulateImage = SubtractAverage.simulate(data)
        data.setSimulateImage(simulateImage)
        DataOutput.outputDataToGUI(data)
    elif(flag == 'Zoomed'): # process = zoomed image
        detectCandidates(data)
        ZoomImage.zoomImage(data)
        DataOutput.outputDataToGUI(data)
    else: # flag == 'Photoplot' and process = photometry plot
        Photometry.photometryPlot(data)

# detect bright/dark pixels
def detectCandidates(data):
    imgInt16 = data.getImageData16()# get the image as int16 for processing
    snr = data.getSNR() # signal to noise ratio

    # Calculate image mean and standard deviation
    imgMean = np.mean(imgInt16) # get average of image
    imgStd = np.std(imgInt16) # get standard deviation of image

    # Create a differenced image
    diffImg = np.diff(imgInt16, axis=0)
    diffImgMean = np.mean(diffImg)
    diffImgStd = np.std(diffImg)

    # Find detections above SNR limit (snr = 10) in differenced image
    more = np.nonzero(diffImg > snr*diffImgStd) # detecting significant increases in brightness
    less = np.nonzero(diffImg < -1*snr*diffImgStd) # detecting significant decreases in brightness

    #store detections and differenced image in data object
    data.setCandGt(more)
    data.setCandLt(less)
    data.setImgStd(imgStd)
    data.setDiffImg(diffImg)