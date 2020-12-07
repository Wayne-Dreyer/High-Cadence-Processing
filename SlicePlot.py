#This file was created by Julian Harrison
import numpy as np
import ImageIntensity
import DataObject
#from MockDataObject import DataObject #Test cases

#Receives the location of a star to draw a sliceplot for, and returns the three values for a sliceplot
#Function can receive a recommended margin of error (inWid) otherwise it uses the default of 50
def performSlicePlot(dataObject, inX, inY, inWid = 0):
    #Set up data16 datatype
    
    #Set the width of the margin of error
    if(inWid == 0):
        wid = 50
    else:
        wid = inWid
    
    #Get the maximum x Coordinate
    imageData = dataObject.getImageData()
    yMax, xMax = imageData.shape #The image data contains the y value in the first array
    
    finalY = adjustYCoordinateToMatchData(inY, yMax) #The coordinates retrieved are set from the top-left being [0, 0], whereas the data is stored as the bottom-left being [0, 0]
    
    #Get the locations of the edges for the plot
    if not finalY - wid < 0:
        sl = finalY - wid
    else:
        sl = 0
    if not finalY + wid > yMax:
        sh = finalY + wid
    else:
        sh = yMax
    
    #Get slice through star
    sliceData = [inX, sl, sh]
    
    return sliceData

#Adjusts the Y coordinate to get the correct location of the selected pixel in the data
def adjustYCoordinateToMatchData(inY, yMax):
    finalY = (yMax - inY - 1) #Inverts the Y coordinate and then removes 1 to find the correct location on the data
    
    return finalY

#TODO This function is currently not working as intended due to issues with extracting the brightness from the file
def intensityDiff(dataObject, inSliceData):
    #Get the mean brightness of the image
    meanImageBrightness = ImageIntensity.meanBrightness(dataObject)
    
    #Get the mean brightness of the slice
    imageData = dataObject.getImageData()
    sliceLength = inSliceData[2] - inSliceData[1]
    
    #Create brightness array
    brightnessArray = []
    
    peak = 0
    
    for ii in range(sliceLength):
        #Get location of pixel
        #TODO May need changing depending on DataObject
        #xLength = dataObject.getXLength()
        arrayPositionX = inSliceData[0]
        arrayPositionY = inSliceData[1] + ii
        
        #Get brightness and add it to array
        pixel = imageData[arrayPositionY, arrayPositionX] #Note: imageData is stored as [y, x]
        brightnessArray.append(pixel.astype(np.int16))
        
        #Get peak brightness in slice
        if(pixel.astype(np.int16) > peak):
            peak = pixel
    
    #Get average brightness of slice
    meanSliceBrightness = np.mean(brightnessArray)
    
    intensityDifference = meanSliceBrightness - meanImageBrightness
    
    return intensityDifference, peak

#Function currently assumes brightness given in apparent brightness measure
def findCalibrationFactor(brightnessDifference, actualBrightness):
    estimatedFluxDensity = 3650 / (2.516 ** actualBrightness) #Gets the flux density value based on the apparent magnitude
    
    calibrationFactor = brightnessDifference / estimatedFluxDensity
    
    return calibrationFactor