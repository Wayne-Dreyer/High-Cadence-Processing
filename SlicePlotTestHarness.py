#This file was created by Julian Harrison
import unittest
from unittest.mock import Mock
import SlicePlot
import numpy as np
from MockDataObject import DataObject
import os
import ImageIntensity #Testing

class SlicePlotTestHarness(unittest.TestCase):
    #Location of a fitsfile - for testing purposes change add a fitsfile to your computer and change the directory to match your computer
    fileLocation = os.path.abspath("E:\\Libraries\\Documents\\Uni\\Semester 2 2020\\CCP2\\Code\\HighCadenceProcessing\\TestData\\0100-fast-slew-5-sec.fit")
    #fileLocation = os.path.abspath("E:\\Libraries\\Documents\\Uni\\Semester 2 2020\\CCP2\\Code\\HighCadenceProcessing\\TestData\\IM_19-final.fit")
    
    #Tests for slicePlot function
    
    #Test performSlicePlot works with a margin of error provided  
    def testMarginOfError(self):
        dataObject = DataObject(self.fileLocation)
        yMax, xMax = dataObject.getImageData().shape
        outX = 20
        outY = (yMax - 30 - 1)
        marginOfError = 5
        #result = [30, 15, 25]
        result = [20, 25, 35]
        self.assertEqual(SlicePlot.performSlicePlot(dataObject, outX, outY, marginOfError), result)
        
    #Test performSlicePlot works without a margin of error provided 
    def testNoMarginOfError(self):
        dataObject = DataObject(self.fileLocation)
        yMax, xMax = dataObject.getImageData().shape
        outX = 920
        outY = (yMax - 1150 - 1)
        #result = [1150, 870, 970]
        result = [920, 1100, 1200]
        self.assertEqual(SlicePlot.performSlicePlot(dataObject, outX, outY), result)
    
    #Test performSlicePlot will correctly prevent the slice from having a value below 0
    def testMarginBelowMinimum(self):
        dataObject = DataObject(self.fileLocation)
        yMax, xMax = dataObject.getImageData().shape
        outX = 20
        outY = (yMax - 30 - 1)
        marginOfError = 50
        #result = [30, 0, 70]
        result = [20, 0, 80]
        self.assertEqual(SlicePlot.performSlicePlot(dataObject, outX, outY), result)
        
    #Test performSlicePlot will correctly prevent the slice from having a value above the maximum Y value of the image
    def testMarginAboveMaximum(self):
        dataObject = DataObject(self.fileLocation)
        yMax, xMax = dataObject.getImageData().shape
        outX = 1000
        outY = (yMax - 3421 - 1)
        marginOfError = 50
        #result = [1000, 3371, 3461]
        result = [1000, 3371, 3461]
        self.assertEqual(SlicePlot.performSlicePlot(dataObject, outX, outY), result)
        
    
    #Tests for intensityDiff function
    
    #Test intensityDiff's value returned when provided with a star's position in a fits file 
    def testIntensityDifferenceOnStar(self):
        dataObject = DataObject(self.fileLocation)
        yMax, xMax = dataObject.getImageData().shape
        outX = 2986
        outY = 1514
        marginOfError = 30
        #result = #Currently no known way to get result without using this method
        slicePlotData = SlicePlot.performSlicePlot(dataObject, outX, outY, marginOfError) #Assumes slicePlot function fully works
        
        #Can't current use assertEqual() since it is unknown how to obtain the results beforehand
        intensityDifference = SlicePlot.intensityDiff(dataObject, slicePlotData)
        print("Star difference: " + str(intensityDifference))
    
    #Test intensityDiff's value returned when provided with a part of the background's position in a fits file
    def testIntensityDifferenceOnBackground(self):
        dataObject = DataObject(self.fileLocation)
        yMax, xMax = dataObject.getImageData().shape
        outX = 700 #1600
        outY = 500 #1600
        marginOfError = 50
        #result = #Currently no known way to get result without using this method
        slicePlotData = SlicePlot.performSlicePlot(dataObject, outX, outY, marginOfError) #Assumes slicePlot function fully works
        
        #Can't current use assertEqual() since it is unknown how to obtain the results beforehand
        intensityDifference = SlicePlot.intensityDiff(dataObject, slicePlotData)
        print("Not star difference: " + str(intensityDifference))
        
    #Get the value of the average brightness of the image for evaluation purposes
    def testIntensityOfBackground(self):
        dataObject = DataObject(self.fileLocation)
        print("Background brightness: " + str(ImageIntensity.meanBrightness(dataObject)))
        
    #Tests that the data provided by the fits file does not have values beyond the size of the image (This one is for the Y coordinates)
    def testYOutOfBounds(self):
        dataObject = DataObject(self.fileLocation)
        imageData = dataObject.getImageData()
        
        try:
            pixel = imageData[3461, 5190].astype(np.int16) #Note: imageData is stored as [y, x]
        except IndexError:
            pass
        
        self.assertRaises(IndexError)
        
    #Tests that the data provided by the fits file does not have values beyond the size of the image (This one is for the X coordinates)
    def testXOutOfBounds(self):
        dataObject = DataObject(self.fileLocation)
        imageData = dataObject.getImageData()
        
        try:
            pixel = imageData[3460, 5191].astype(np.int16) #Note: imageData is stored as [y, x]
        except IndexError:
            pass
        
        self.assertRaises(IndexError)
        
    #Prints a series of pixel brightness values for evaluation purposes
    def testPixelBrightness(self):
        dataObject = DataObject(self.fileLocation)
        outX = 2905
        outY = 620

        imageData = dataObject.getImageData()
        yMax, xMax = imageData.shape        
        
        """pixel = imageData[2548, 2713].astype(np.int16)
        print("Pixel brightness - star bright: " + str(pixel))
        pixel = imageData[2548, 2714].astype(np.int16)
        print("Pixel brightness - star dim: " + str(pixel))
        pixel = imageData[2554, 2711].astype(np.int16)
        print("Pixel brightness - background bright: " + str(pixel))
        pixel = imageData[2553, 2711].astype(np.int16)
        print("Pixel brightness - background dark: " + str(pixel))"""
        
        pixel = imageData[(yMax - 2703 - 1), 2548].astype(np.int16)
        print("Pixel brightness - star bright: " + str(pixel))
        pixel = imageData[(yMax - 2704 - 1), 2548].astype(np.int16)
        print("Pixel brightness - star dim: " + str(pixel))
        pixel = imageData[(yMax - 2711 - 1), 2554].astype(np.int16)
        print("Pixel brightness - background bright: " + str(pixel))
        pixel = imageData[(yMax - 2711 - 1), 2553].astype(np.int16)
        print("Pixel brightness - background dark: " + str(pixel))
        
        print(imageData.shape)
        
    def testCalibrationFactor(self):
        actualBrightness = 1.65
        brightnessDiff = 320.01
        self.assertAlmostEquals(SlicePlot.findCalibrationFactor(brightnessDiff, actualBrightness), 0.40183081297868130490075462674991)

        actualBrightness = 1.65
        brightnessDiff = 270.15
        self.assertAlmostEquals(SlicePlot.findCalibrationFactor(brightnessDiff, actualBrightness), 0.33922250594103545051385538707068)
        
        actualBrightness = 1.65
        brightnessDiff = 1507.13
        self.assertAlmostEqual(SlicePlot.findCalibrationFactor(brightnessDiff, actualBrightness), 1.8924760887614760634201253729996)

        actualBrightness = 0.0
        brightnessDiff = 3650
        self.assertAlmostEqual(SlicePlot.findCalibrationFactor(brightnessDiff, actualBrightness), 1.00000000000000000000000000000)
        
        actualBrightness = 2.12
        brightnessDiff = 364.8739214612142
        self.assertAlmostEqual(SlicePlot.findCalibrationFactor(brightnessDiff, actualBrightness), 0.70689760419447884025245210949539)
        
        #This test is very slow
    """def testLocationOfBrightestAndDimestPixels(self):
        dataObject = DataObject(self.fileLocation)
        imageData = dataObject.getImageData()
        
        brightestPixel = 0
        brightestPixelLocationX = 0
        brightestPixelLocationY = 0
        dimestPixel = 65535
        dimestPixelLocationX = 0
        dimestPixelLocationY = 0
        
        yMax, xMax = imageData.shape
        
        for ii in range(yMax):
            for jj in range(xMax):
                pixelBrightness = imageData[ii][jj].astype(np.int16)
                if pixelBrightness > brightestPixel:
                    brightestPixel = pixelBrightness
                    brightestPixelLocationY = ii
                    brightestPixelLocationX = jj
                if pixelBrightness < dimestPixel:
                    dimestPixel = pixelBrightness
                    dimestPixelLocationY = ii
                    dimestPixelLocationX = jj
                    
        print("Brightest pixel: {}".format(brightestPixel))
        print("X:{}, Y:{}".format(brightestPixelLocationX, brightestPixelLocationY))
        print("Dimest pixel: {}".format(dimestPixel))
        print("X:{}, Y:{}".format(dimestPixelLocationX, dimestPixelLocationY))"""