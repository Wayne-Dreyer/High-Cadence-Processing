#This file was created by Julian Harrison
from MockSlice import Slice 
from astropy.io import fits
from EmptyFileException import EmptyFileException

class DataObject:
    __imageData = None
    __xLength = 0
    __yLength = 0
    __sliceList = []
    __calibrationFactor = 0.0
    __photoPlotImage = None
    __zoomedImage = None
    __publicationImage = None
    __flag = ""
    __pixelImage = None
    __orbitsImage = None
    __simulateImage = None
    
    def __init__(self, fitFile):
        #self.imageData = "This is a test string. \nIt's purpose is to test the data output function"
        #TODO Give image data proper set of image data
        try:
            with fits.open(fitFile) as imghdul:
                self.__imageData = imghdul[0].data
        except ValueError:
            raise EmptyFileException("File name is invalid")
        except OSError:
            raise EmptyFileException("File is invalid, either corrupted or an incorrect format")
        
        #list of slicePlotLocations
        """slicePlotList = []
        sliceOne = Slice(2905, 562, "Test star 1", 50, 1.2)
        slicePlotList.append(sliceOne)
        sliceTwo = Slice(2986, 1514, "Test star 2", 30, 1.6)
        slicePlotList.append(sliceTwo)
        sliceThree = Slice(700, 500, "Background", 50, 6.78)
        slicePlotList.append(sliceThree)
        self.sliceList = slicePlotList"""
        
    def getImageData(self):
        return self.__imageData
    
    def addSlice(self, slice):
        self.__sliceList.append(slice)
    
    def getSliceList(self):
        return self.__sliceList
    
    def setMeanCalibrationFactor(self, calibrationFactor):
        self.__calibrationFactor = calibrationFactor
        
    def getMeanCalibrationFactor(self):
        return self.__calibrationFactor
    
    def setPhotoplotImage(self, image):
        self.__photoPlotImage = image
    
    def getPhotoplotImage(self):
        return self.__photoPlotImage
    
    def setZoomedImages(self, image):
        self.__zoomedImage = image
        
    def getZoomedImages(self):
        return self.__zoomedImage

    def setPublicationImage(self, image):
        self.__publicationImage = image
        
    def getAnnotatedImage(self):
        return self.__publicationImage
    
    def setFlag(self, flag):
        if(not ( (flag == 'Photoplot') or (flag == 'Publication') or (flag == 'CheckPixels') or (flag == 'Simulate') or (flag == 'Zoomed') or (flag == 'Orbits') ) ):
            #raise InvalidFlagException("Flag must be Photoplot, Publication, CheckPixels, Simulate, Zoomed or Orbits")
            raise ImportError("Flag invalid")
        self.__flag = flag
    
    def getFlag(self):
        return self.__flag
    
    def setPixelImage(self, image):
        self.__pixelImage = image
        
    def getPixelImage(self):
        return self.__pixelImage
    
    def setOrbitPlot(self, image):
        self.__orbitsImage = image
        
    def getOrbitPlot(self):
        return self.__orbitsImage
    
    def setSimulateImage(self, image):
        self.simulateImage = image
        
    def getSimulateImage(self):
        return self.simulateImage