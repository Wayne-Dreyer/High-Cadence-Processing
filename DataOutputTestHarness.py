#This file was created by Julian Harrison
import MockDataObject
import DataOutput
import unittest
import os
from Slice import Slice


class DataOutputTestHarness(unittest.TestCase):
    fileLocation = os.path.abspath("E:\\Libraries\\Documents\\Uni\\Semester 2 2020\\CCP2\\Code\\HighCadenceProcessing\\TestData\\0100-fast-slew-5-sec.fit")
    saveLocation = os.path.abspath("E:\\Libraries\\Documents\\Uni\\Semester 2 2020\\CCP2\\Code\\HighCadenceProcessing")
    
    def testPixelOutput(self):
        dataObject = MockDataObject.DataObject(self.fileLocation)
        dataObject.setFlag("CheckPixels")
        dataObject.setPixelImage(dataObject.getImageData())
        
        DataOutput.outputDataToFile(dataObject, "PixelDataTest", self.saveLocation)
        
    def testPublicationOutput(self):
        dataObject = MockDataObject.DataObject(self.fileLocation)
        dataObject.setFlag("Publication")
        
        figure = DataOutput.newImage(dataObject.getImageData(), 6500, 6700)
        
        dataObject.setPublicationImage(figure)
        
        DataOutput.outputDataToFile(dataObject, "PublicationImageTest", self.saveLocation)
    
    def testOrbitsOutput(self):
        dataObject = MockDataObject.DataObject(self.fileLocation)
        dataObject.setFlag("Orbits")
        
        figure = DataOutput.newImage(dataObject.getImageData(), 6500, 6700)
        
        dataObject.setOrbitPlot(figure)
        
        DataOutput.outputDataToFile(dataObject, "OrbitPlot", self.saveLocation)
        
    def testSimulateOutput(self):
        dataObject = MockDataObject.DataObject(self.fileLocation)
        dataObject.setFlag("Simulate")
        
        dataObject.setSimulateImage(dataObject.getImageData())
        
        DataOutput.outputDataToFile(dataObject, "SimulateImageTest", self.saveLocation)
    
    def testZoomedImageOutput(self):
        dataObject = MockDataObject.DataObject(self.fileLocation)
        dataObject.setFlag("Zoomed")
        
        imageArray = []
        
        imageArray.append(dataObject.getImageData())
        imageArray.append(dataObject.getImageData())
        imageArray.append(dataObject.getImageData())
        imageArray.append(dataObject.getImageData())
        imageArray.append(dataObject.getImageData())
        
        dataObject.setZoomedImages(imageArray)
        
        DataOutput.outputDataToFile(dataObject, "ZoomedImageTest", self.saveLocation)
    
    def testPhotoplotOutput(self):
        dataObject = MockDataObject.DataObject(self.fileLocation)
        dataObject.setFlag("Photoplot")
        
        sliceOne = Slice(2905, 562, "Test star 1", 50, 1.2)
        sliceOne.setYh(612)
        sliceOne.setYl(512)
        sliceOne.setBrightnessDiff(200.25)
        dataObject.addSlice(sliceOne)
        sliceTwo = Slice(2986, 1514, "Test star 2", 30, 1.6)
        sliceTwo.setYh(1544)
        sliceTwo.setYl(1484)
        sliceTwo.setBrightnessDiff(120.46)
        dataObject.addSlice(sliceTwo)
        
        dataObject.setMeanCalibrationFactor(0.4)
        
        figure = DataOutput.newImage(dataObject.getImageData(), 6500, 6700)
        
        dataObject.setPhotoplotImage(figure)
        
        DataOutput.outputDataToFile(dataObject, "PhotoplotTest", self.saveLocation)