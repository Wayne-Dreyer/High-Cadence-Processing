#This file was created by Tate Hagan
from astropy.io import fits #Used to read fits files
from astropy import wcs #Used for WCS
import os #used for the isfile() method to check if a string refers to a file
from EmptyFileException import EmptyFileException #Used to throw errors when values aren't read in from file
from IncorrectTypeException import IncorrectTypeException #Used to throw errors when input needs to be a specific type and isn't
from NoSliceException import NoSliceException #Used to throw errors when a value of slice is attempted to be set or retrieved when no slice exists
from InvalidSizeException import InvalidSizeException #Used to throw errors when an input candidate list is an invalid size
from InvalidCoordException import InvalidCoordException #Used to throw errors when the zoomed image coordinate is out of range
from InvalidZoomFactorException import InvalidZoomFactorException #Used to throw errors when Zoom Factor is negative
from InvalidFlagException import InvalidFlagException #Used to throw errors when Flag is invalid
from ValidateTle import validateTle
import numpy as np #used for getImageData16
from Slice import Slice #Used for Photoplot
from ZoomObject import ZoomObject #Used for Zoomed
import matplotlib as plt #used for checking type on annotated image

class DataObject:
    def __init__(self, fitFile, flag, snr):
        #Initially sets values to None
        self.img = None
        self.imgHeader = None
        self.flag = None
        self.snr = None
        
        #Initialises fields for candidate data
        self.candGt = () #Initialises tuples to being empty
        self.candLt = ()
        self.imgStd = None
        self.diffImg = None
        
        #validates snr
        if(not isinstance(snr, float)):
            raise IncorrectTypeException("snr must be of type float")
        self.snr = snr
        
        #reads fit file
        try:            
            with fits.open(fitFile) as imghdul: #using the with keyword means that the file will be closed even if an exception is thrown
                self.img = imghdul[0].data
                self.imgHeader = imghdul[0].header
        except ValueError:
            raise EmptyFileException('Img filename is empty')
        except OSError:
            raise EmptyFileException('Img file is not the correct format or is corrupted')
        
        if self.img is None:
            raise EmptyFileException('Img is null')
                
        #validates flag
        if(not ( (flag == 'Photoplot') or (flag == 'Publication') or (flag == 'CheckPixels') or (flag == 'Simulate') or (flag == 'Zoomed') or (flag == 'Orbits') ) ):
            raise InvalidFlagException("Flag must be Photoplot, Publication, CheckPixels, Simulate, Zoomed or Orbits")
        self.flag = flag
        
        #Initialises fields for selected flag
        if(self.flag == 'Photoplot'):
            #Initialise Photoplot fields
            self.Slices = [] #Initialises slice list to an empty list
            self.currSlice = None
            self.meanCalibrationFactor = 0.0 #Will be used for the output of the Photometry component
            self.photoImage = None #Will be used for image with slices marked
        elif(self.flag == 'Publication'):
            #Initialise Publication fields
            self.annotated = None #Output for Publication component
        elif(self.flag == 'CheckPixels'):
            self.checkX = -1 #Data for CheckPixels component, initialised to invalid values
            self.checkY = -1
            self.checkFactor = 0.0 #Zoom factor to use, named this to avoid confusion with that of the zoomed image component
            self.pixelImage = None #Output for CheckPixels component
            self.padTop = 0
            self.padBottom = 0
            self.padLeft = 0
            self.padRight = 0
            self.height = 0
            self.width = 0
        elif(self.flag == 'Simulate'):
            self.simulateImage = None #Output for Simulate component
        elif(self.flag == 'Zoomed'):
            #Initialise Zoomed fields
            self.zoomFactor = 0.0 #Data for CheckPixels component, initialised to invalid values
            self.zoomedImages = None #Output from CreateZoomedImage component
        elif(self.flag == 'Orbits'):
            #Initialise Orbits fields
            self.tleData = None #Initialises input
            self.tleLength = None
            self.wcsinfo = None
            self.orbitPlot = None #Output from Orbits component

#Getters for input data
    def getImageData(self):
        return self.img
    
    def getImageData16(self):
        return (self.img).astype(np.int16)
    
    def getImageHeader(self):
        return self.imgHeader
    
    def getFlag(self):
        return self.flag
    
    def getSNR(self):
        return self.snr
    
#Setters and getters for generic data
    def setCandGt(self, incandGt):
        if(not isinstance(incandGt, tuple)): #checks that input is a tuple
            raise IncorrectTypeException('Value must be a tuple')
        if(not len(incandGt) == 2): #Checks that tuple has exactly 2 elements
            raise InvalidSizeException('Size must be 2')
        if(not isinstance(incandGt[0], np.ndarray) and not isinstance(incandGt[1], np.ndarray)): #Checks that tuple elements are ndarrays
            raise IncorrectTypeException('Tuple elements must be ndarrays')
        try:
            if(not isinstance(incandGt[0][0], np.int64)): #Checks that the array elements are of type int64
                raise IncorrectTypeException('Values in tuple must be of type int64')
        except IndexError:
            pass #There were no candidates detected
        if(not len(incandGt[0])==len(incandGt[1])):
            raise InvalidSizeException('Arrays must be of equal size')
        self.candGt = incandGt
        
    def getCandGt(self):
        return self.candGt
    
    def setCandLt(self, incandLt):
        if(not isinstance(incandLt, tuple)):
            raise IncorrectTypeException('Value must be a tuple')
        if(not len(incandLt) == 2):
            raise InvalidSizeException('Size must be 2')
        if(not isinstance(incandLt[0], np.ndarray) and not isinstance(incandLt[1], np.ndarray)):
            raise IncorrectTypeException('Tuple elements must be ndarrays')
        try:
            if(not isinstance(incandLt[0][0], np.int64)):
                raise IncorrectTypeException('Values in tuple must be of type int64')
        except IndexError:
            pass #There were no candidates detected
        if(not len(incandLt[0])==len(incandLt[1])):
            raise InvalidSizeException('Arrays must be of equal size')
        self.candLt = incandLt
        
    def getCandLt(self):
        return self.candLt
    
    def setImgStd(self, inImgStd):
        if(not isinstance(inImgStd, np.float64)):
            raise IncorrectTypeException('Value must be a float64')
        self.imgStd = inImgStd
    
    def getImgStd(self):
        return self.imgStd
    
    def setDiffImg(self, inDiffImg):
        if(not isinstance(inDiffImg, np.ndarray)):
            raise IncorrectTypeException('Value must be an ndarray')
        self.diffImg = inDiffImg
    
    def getDiffImg(self):
        return self.diffImg

#Setters and getters for Photoplot
    #Initial slice input to add a slice to the list
    def setSlice(self, x, y, name, width, brightness):
        if(not (self.flag == 'Photoplot')):
            raise InvalidFlagException("This function is for Photoplot flag only")
        if( (not isinstance(x, int)) or (not isinstance(y, int)) or (not isinstance(width, int)) or (not isinstance(brightness, float)) ):
            raise IncorrectTypeException('x, y and width must be integers and brightness must be float')
        self.currSlice = Slice(x, y, name, width, brightness)
        self.Slices.append(self.currSlice)

    #Retrieves the current slice
    def getCurrSlice(self):
        if(not (self.flag == 'Photoplot')):
            raise InvalidFlagException("This function is for Photoplot flag only")
        return self.currSlice
    
    #The next three functions are used to set slice output
    def setSliceYl(self, yl):
        if(not (self.flag == 'Photoplot')):
            raise InvalidFlagException("This function is for Photoplot flag only")
        if(self.currSlice == None):
            raise NoSliceException('No slice to set data for')
        if(not isinstance(yl, int)):
            raise IncorrectTypeException('Value must be an Integer')
        self.currSlice.setYl(yl)
    
    def setSliceYh(self, yh):
        if(not (self.flag == 'Photoplot')):
            raise InvalidFlagException("This function is for Photoplot flag only")
        if(self.currSlice == None):
            raise NoSliceException('No slice to set data for')
        if(not isinstance(yh, int)):
            raise IncorrectTypeException('Value must be an Integer')
        self.currSlice.setYh(yh)
    
    def setSliceBrightnessDiff(self, brightnessDiff):
        if(not (self.flag == 'Photoplot')):
            raise InvalidFlagException("This function is for Photoplot flag only")
        if(self.currSlice == None):
            raise NoSliceException('No slice to set data for')
        if(not isinstance(brightnessDiff, int)):
            raise IncorrectTypeException('Value must be an Integer')
        self.currSlice.setBrightnessDiff(brightnessDiff)
    
    #Used by the Data Output component to retrieve the slice list details
    def getSliceList(self):
        if(not (self.flag == 'Photoplot')):
            raise InvalidFlagException("This function is for Photoplot flag only")
        return self.Slices
    
    def setMeanCalibrationFactor(self, meanCalibrationFactor):
        if(not (self.flag == 'Photoplot')):
            raise InvalidFlagException("This function is for Photoplot flag only")
        if(not isinstance(meanCalibrationFactor, float)):
            raise IncorrectTypeException('Mean Calibration Factor must be a float')
        self.meanCalibrationFactor = meanCalibrationFactor
    
    def getMeanCalibrationFactor(self):
        if(not (self.flag == 'Photoplot')):
            raise InvalidFlagException("This function is for Photoplot flag only")
        return self.meanCalibrationFactor
    
    def setPhotoplotImage(self, inPhotoImage):
        if(not (self.flag == 'Photoplot')):
            raise InvalidFlagException('This function is for Photoplot flag only')
        if(not isinstance(inPhotoImage, plt.figure.Figure)):
            raise IncorrectTypeException("Photoplot Image must be a matplotlib.figure.Figure")
        self.photoImage = inPhotoImage
    
    def getPhotoplotImage(self):
        if(not (self.flag == 'Photoplot')):
            raise InvalidFlagException('This function is for Photoplot flag only')
        return self.photoImage
    
#Setters and getters for Publication
    def setAnnotatedImage(self, inAnnotatedImage):
        if(not (self.flag == 'Publication')):
            raise InvalidFlagException("This function is for Publication flag only")
        if(not isinstance(inAnnotatedImage, plt.figure.Figure)):
            raise IncorrectTypeException("Annotated Image must be a matplotlib.figure.Figure")
        self.annotated = inAnnotatedImage
    
    def getAnnotatedImage(self):
        if(not (self.flag == 'Publication')):
            raise InvalidFlagException("This function is for Publication flag only")
        return self.annotated
    
#Setters and getters for CheckPixels
    def setCheckX(self, inCheckX):
        if(not (self.flag == 'CheckPixels')):
            raise InvalidFlagException("This function is for Check Pixels flag only")
        if(not isinstance(inCheckX, int)):
            raise IncorrectTypeException("Coordinate must be int")
        yMax, xMax = self.img.shape
        if( not( (inCheckX > 0) and (inCheckX < xMax) ) ):
            raise InvalidCoordException("x Coordinate is out of bounds. Must be from 0 to {}.".format(xMax))
        self.checkX = inCheckX
    
    def getCheckX(self):
        if(not (self.flag == 'CheckPixels')):
            raise InvalidFlagException("This function is for Check Pixels flag only")
        return self.checkX
    
    def setCheckY(self, inCheckY):
        if(not (self.flag == 'CheckPixels')):
            raise InvalidFlagException("This function is for Check Pixels flag only")
        if(not isinstance(inCheckY, int)):
            raise IncorrectTypeException("Coordinate must be int")
        yMax, xMax = self.img.shape
        if( not( (inCheckY > 0) and (inCheckY < yMax) ) ):
            raise InvalidCoordException("y Coordinate is out of bounds. Must be from 0 to {}.".format(yMax))
        self.checkY = inCheckY
        
    def getCheckY(self):
        if(not (self.flag == 'CheckPixels')):
            raise InvalidFlagException("This function is for Check Pixels flag only")
        return self.checkY
    
    def setCheckFactor(self, inCheckFactor):
        if(not (self.flag == 'CheckPixels')):
            raise InvalidFlagException("This function is for Check Pixels flag only")
        if(not isinstance(inCheckFactor, float)):
            raise IncorrectTypeException("Check Zoom Factor must be float")
        if(not inCheckFactor > 0.0):
            raise InvalidZoomFactorException("Check Zoom Factor must be positive")
        self.checkFactor = inCheckFactor
    
    def getCheckFactor(self):
        if(not (self.flag == 'CheckPixels')):
            raise InvalidFlagException("This function is for Check Pixels flag only")
        return self.checkFactor
    
    def setPixelImage(self, inPixelImage):
        if(not (self.flag == 'CheckPixels')):
            raise InvalidFlagException("This function is for Check Pixels flag only")
        if(not isinstance(inPixelImage, plt.figure.Figure)):
            raise IncorrectTypeException("Pixel image must be a Figure")
        self.pixelImage = inPixelImage

    def getPixelImage(self):
        if(not (self.flag == 'CheckPixels')):
            raise InvalidFlagException("This function is for Check Pixels flag only")
        return self.pixelImage
    
    def setPadTop(self, inPadTop):
        if(not(self.flag == 'CheckPixels')):
            raise InvalidFlagException("This function is for CheckPixels flag only")
        if(not isinstance(inPadTop, int)):
            raise IncorrectTypeException("inPadTop must be an int")
        self.padTop = inPadTop
    
    def getPadTop(self):
        if(not(self.flag == 'CheckPixels')):
            raise InvalidFlagException("This function is for CheckPixels flag only")
        return self.padTop
    
    def setPadBottom(self, inPadBottom):
        if(not(self.flag == 'CheckPixels')):
            raise InvalidFlagException("This function is for CheckPixels flag only")
        if(not isinstance(inPadBottom, int)):
            raise IncorrectTypeException("inPadTop must be an int")
        self.padBottom = inPadBottom
    
    def getPadBottom(self):
        if(not(self.flag == 'CheckPixels')):
            raise InvalidFlagException("This function is for CheckPixels flag only")
        return self.padBottom
    
    def setPadLeft(self, inPadLeft):
        if(not(self.flag == 'CheckPixels')):
            raise InvalidFlagException("This function is for CheckPixels flag only")
        if(not isinstance(inPadLeft, int)):
            raise IncorrectTypeException("inPadTop must be an int")
        self.padLeft = inPadLeft
    
    def getPadLeft(self):
        if(not(self.flag == 'CheckPixels')):
            raise InvalidFlagException("This function is for CheckPixels flag only")
        return self.padLeft
    
    def setPadRight(self, inPadRight):
        if(not(self.flag == 'CheckPixels')):
            raise InvalidFlagException("This function is for CheckPixels flag only")
        if(not isinstance(inPadRight, int)):
            raise IncorrectTypeException("inPadTop must be an int")
        self.padRight = inPadRight
    
    def getPadRight(self):
        if(not(self.flag == 'CheckPixels')):
            raise InvalidFlagException("This function is for CheckPixels flag only")
        return self.padRight

    def setHeight(self, inHeight):
        if(not(self.flag == 'CheckPixels')):
            raise InvalidFlagException("This function is for CheckPixels flag only")
        if(not isinstance(inHeight, int)):
            raise IncorrectTypeException("inHeight must be an int")
        self.height = inHeight
    
    def getHeight(self):
        if(not(self.flag == 'CheckPixels')):
            raise InvalidFlagException("This function is for CheckPixels flag only")
        return self.height
    
    def setWidth(self, inWidth):
        if(not(self.flag == 'CheckPixels')):
            raise InvalidFlagException("This function is for CheckPixels flag only")
        if(not isinstance(inWidth, int)):
            raise IncorrectTypeException("inWidth must be an int")
        self.width = inWidth
    
    def getWidth(self):
        if(not(self.flag == 'CheckPixels')):
            raise InvalidFlagException("This function is for CheckPixels flag only")
        return self.width
    
#Setters and getters for Simulate
    def setSimulateImage(self, inSimulateImage):
        if(not (self.flag == 'Simulate')):
            raise InvalidFlagException("This function is for Simulate flag only")
        if(not isinstance(inSimulateImage, np.ndarray)):
            raise IncorrectTypeException("Simulate Image must be a numpy.ndarray")
        if(not (inSimulateImage.ndim == 2)):
            raise InvalidSizeException("Must be 2d")
        self.simulateImage = inSimulateImage

    def getSimulateImage(self):
        if(not (self.flag == 'Simulate')):
            raise InvalidFlagException("This function is for Simulate flag only")
        return self.simulateImage
    
#Setters and getters for Zoomed
    def setZoomFactor(self, inZoomFactor):
        if(not (self.flag == 'Zoomed')):
            raise InvalidFlagException("This function is for Zoomed flag only")
        if(not isinstance(inZoomFactor, float)):
            raise IncorrectTypeException("Zoom Factor must be float")
        if(not inZoomFactor > 0.0):
            raise InvalidZoomFactorException("Zoom Factor must be positive")
        self.zoomFactor = inZoomFactor
    
    def getZoomFactor(self):
        if(not (self.flag == 'Zoomed')):
            raise InvalidFlagException("This function is for Zoomed flag only")
        return self.zoomFactor
    
    def setZoomedImages(self, inZoomedImages):
        if(not (self.flag == 'Zoomed')):
            raise InvalidFlagException("This function is for Zoomed flag only")
        if(not isinstance(inZoomedImages, list)):
            raise IncorrectTypeException("ZoomedImages must be a list of zoomed images")
        try:
            if(not isinstance(inZoomedImages[0], ZoomObject)):
                raise IncorrectTypeException("Individual list elements must be ZoomObjects")
            self.zoomedImages = inZoomedImages
        except IndexError:
            self.zoomedImages = []
    
    def getZoomedImages(self):
        if(not (self.flag == 'Zoomed')):
            raise InvalidFlagException("This function is for Zoomed flag only")
        return self.zoomedImages
    
#Setters and getters for Orbits
    def setTle(self, tleFile):
        if(not (self.flag == 'Orbits')):
            raise InvalidFlagException("This function is for Orbits flag only")
        #reads tle file
        try:
            if(not os.path.isfile(tleFile)):
                raise EmptyFileException('Tle file does not exist')
            if(not validateTle(tleFile)):
                raise EmptyFileException('Tle file is not correctly formatted')
            with open(tleFile) as tle:
                self.tleData=tle.readlines()
                self.tleLength=len(self.tleData)
        except ValueError:
            raise EmptyFileException('Tle filename is empty')
        
        if ( (self.tleData is None) | (self.tleLength is None) ):
            raise EmptyFileException('Tle is null')
    
    def getTleData(self):
        if(not (self.flag == 'Orbits')):
            raise InvalidFlagException("This function is for Orbits flag only")
        return self.tleData
    
    def getTleLength(self):
        if(not (self.flag == 'Orbits')):
            raise InvalidFlagException("This function is for Orbits flag only")
        return self.tleLength

    def setFits(self, fitsFile):
        if(not (self.flag == 'Orbits')):
            raise InvalidFlagException("This function is for Orbits flag only")
        #reads fits file
        try:
            with fits.open(fitsFile):
                self.wcsinfo = wcs.WCS(fitsFile)
        except ValueError:
            raise EmptyFileException('Wcs filename is empty')
        except OSError:
            raise EmptyFileException('Wcs file is not the correct format or is corrupted')
            
        if self.wcsinfo is None:
            raise EmptyFileException('Wcs is null')
            
    def getWcsInfo(self):
        if(not (self.flag == 'Orbits')):
            raise InvalidFlagException("This function is for Orbits flag only")
        return self.wcsinfo

    def setOrbitPlot(self, inOrbitPlot):
        if(not (self.flag == 'Orbits')):
            raise InvalidFlagException("This function is for Orbits flag only")
        if(not isinstance(inOrbitPlot, plt.figure.Figure)):
            raise IncorrectTypeException("OrbitPlot must be of type matplotlib.figure.Figure")
        self.orbitPlot = inOrbitPlot
    
    def getOrbitPlot(self):
        if(not (self.flag == 'Orbits')):
            raise InvalidFlagException("This function is for Orbits flag only")
        return self.orbitPlot