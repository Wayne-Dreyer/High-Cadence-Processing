#This file was created by Julian Harrison
import unittest
from MockDataObject import DataObject #Testing
from MockSlice import Slice
import Photometry
import os

class PhotometryTestHarness(unittest.TestCase):
    #Location of a fitsfile - for testing purposes change add a fitsfile to your computer and change the directory to match your computer
    fileLocation = os.path.abspath("E:\\Libraries\\Documents\\Uni\\Semester 2 2020\\CCP2\\Code\\HighCadenceProcessing\\TestData\\0100-fast-slew-5-sec.fit")
    
    #Tests that the using the SlicePlot list inside a mock DataObject can be used correctly by Photometry to repeatedly call SlicePlot functions for difference Slices
    def testWithMockDataObject(self):
        #Create mock DataObject
        dataObject = DataObject(self.fileLocation)
        dataObject = Photometry.performPhotometry(dataObject)
        
        #Get mock slices from DataObject
        sliceList = dataObject.getSliceList()
        
        #Get Slices from mock DataObject
        sliceOne = sliceList[0]
        sliceTwo = sliceList[1]
        sliceThree = sliceList[2]
        
        #Test slices have correct positions for edges of slice
        self.assertEqual(sliceOne.getYL(), 2848)
        self.assertEqual(sliceOne.getYH(), 2948)
        self.assertEqual(sliceTwo.getYL(), 1916)
        self.assertEqual(sliceTwo.getYH(), 1976)
        self.assertEqual(sliceThree.getYL(), 2910)
        self.assertEqual(sliceThree.getYH(), 3010)
        
        #Test brightnessDiff values are appropriate
        self.assertAlmostEqual(sliceOne.getBrightnessDiff(), 358.2439214612141)
        self.assertAlmostEqual(sliceTwo.getBrightnessDiff(), 284.96392146121434)
        self.assertAlmostEqual(sliceThree.getBrightnessDiff(), 2.493921461214086)
        
        #Test mean calibration factor
        self.assertAlmostEqual(dataObject.getMeanCalibrationFactor(), 0.33154828879279772)
        
        #Test slices have correct difference in brightness to background
        #TODO Needs brightnessDiff function to be fully functional