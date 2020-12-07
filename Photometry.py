#This file was created by Julian Harrison
import numpy as np
import SlicePlot
#from MockDataObject import DataObject #Testing
#from MockSlice import Slice #Testing 
import DataObject
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import Slice
from Photometry_GUI import *
from GUIHandler import GUIHandler

def photometryPlot(dataObject):
    #Extract image from dataObject
    image = dataObject.getImageData()
    
    #Convert image into figure
    figure = plt.figure()
    plt.imshow(image)
    
    #Start GUI process
    handler = GUIHandler.getInstance()
    handler.setWindow("PhotometryGUI")
    handler.setPhotometryGUIData(figure, dataObject)

def performPhotometry(dataObject):
    slicePlots = dataObject.getSliceList()
    calibrationFactorList = []
    
    #Fill list with data on slice edges
    for slicePlot in slicePlots:
        #Get values for plotting
        tempX = slicePlot.getX()
        tempY = slicePlot.getY()
        tempWidth = slicePlot.getWidth()
        
        #Get slice edges
        slicePlotData = SlicePlot.performSlicePlot(dataObject, tempX, tempY, tempWidth)
        
        #Get slice brightness difference
        brightnessDifference, peak = SlicePlot.intensityDiff(dataObject, slicePlotData)
        
        #Get calibration factor
        callibrationFactor = SlicePlot.findCalibrationFactor(brightnessDifference, slicePlot.getActualBrightness())
        
        #Update slice with new data
        yl = slicePlotData[1]
        yh = slicePlotData[2]
        slicePlot.setYl(yl)
        slicePlot.setYh(yh)
        slicePlot.setBrightnessDiff(brightnessDifference)
        slicePlot.setPeak(peak)
        calibrationFactorList.append(callibrationFactor)
    
    meanCallibrationFactor = np.mean(calibrationFactorList)

    dataObject.setMeanCalibrationFactor(meanCallibrationFactor)

    return dataObject