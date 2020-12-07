#This file was created by Julian Harrison
#from DataObject import DataObject #Data will be stored in this format throughout its processing
#from MockDataObject import DataObject #Used for testing purposes
import DataObject
from Output_GUI import OutputGUI
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from astropy.io import fits #Used to save fits file
import os
from datetime import datetime
import platform
import ImageIntensity
from GUIHandler import GUIHandler
import ZoomObject

#Method to be called after processing which will save the data into a text file at the correct place in the file directory

def outputDataToGUI(dataObject, cmin=6500, cmax=6700): #Default values subject to change
    #Create string for data output to GUI
    dataString = None

    #Flag specific behaviour
    flag = dataObject.getFlag()
    if flag == "CheckPixels":
        #Create pixel image as a figure
        figure = dataObject.getPixelImage()
    elif flag == "Publication":
        #Create publication image as a figure
        figure = dataObject.getAnnotatedImage()
    elif flag == "Orbits":
        #Create orbits image as a figure
        figure = dataObject.getOrbitPlot()
    elif flag == "Simulate":
        #Create simulate image as a figure
        simulateImage = dataObject.getSimulateImage()
        figure = newImage(simulateImage, cmin, cmax) 
    elif flag == "Zoomed":
        #Create zoomed image as a figure
        zoomedObjects = dataObject.getZoomedImages()
        
        figures = []
        
        for zoomObject in zoomedObjects:
            figure = zoomObject.getImage()
            figures.append(figure)
        
        handler = GUIHandler.getInstance()
        handler.setWindow("OutputGUI")
        handler.setMultipleOutputGUIData(figures, dataObject, dataString)
            
    elif flag == "Photoplot":
        #Create and prepare figure
        figure = dataObject.getPhotoplotImage()
        
        #Set data string to correct values
        dataString = formatPhotometryData(dataObject)
    
    #Prepare the Output GUI
    if(flag != "Zoomed"):
        handler = GUIHandler.getInstance()
        handler.setWindow("OutputGUI")
        handler.setOutputGUIData(figure, dataObject, dataString)

#Replot the image with different cmin and cmax values
def getFilteredPlot(cmin, cmax, figure):
    #Change figure clim values
    plt.clim(cmin, cmax)
    
    return figure

#Prepares a figure object to be used by the GUI
def newImage(image, cmin, cmax):
    #Create figure
    newImage = plt.figure(figsize=(10,8))
    
    #Set image data into figure
    plt.imshow(image, clim=(cmin,cmax))
    
    #Set axes and a colourbar
    plt.xlabel("Pixel number")
    plt.ylabel("Pixel number")
    plt.colorbar()
    
    return newImage

def outputDataToFile(dataObject, inFileName = "", inFileLocation = ""):
    
    #Get processing flag
    flag = dataObject.getFlag()
        
    if((inFileName == "") and (inFileLocation == "")): #No file name or location
        
        #Create file name and path
        currentDateTime = datetime.now()
        dtString = currentDateTime.strftime("%d_%m_%Y__%H_%M_%S")
        fileName = os.path.join(getDefaultFileLocation(), dtString)
        
        #Check directory exists
        if(not(os.path.isdir(getDefaultFileLocation()))):
            os.makedirs(getDefaultFileLocation())
            
        #Save data to file
        #saveImageData(dataObject, fileName)
        saveData(dataObject, fileName, flag)
        
    elif ((inFileLocation == "") and not (inFileName == "")): #File name but no file location
        
        #Create file name and path
        fileName = os.path.join(getDefaultFileLocation(), inFileName)
        
        #Check directory exists
        if(not(os.path.isdir(getDefaultFileLocation()))):
            os.makedirs(getDefaultFileLocation())
        
        #Save data to file
        #saveImageData(dataObject, fileName)
        saveData(dataObject, fileName, flag)
        
    elif (not (inFileLocation == "") and not(inFileName == "")): #Both file name and location
        
        #Create file name and path
        fileName = os.path.join(inFileLocation, inFileName)
        
        #Check directory exists
        if(not(os.path.isdir(inFileLocation))):
            os.makedirs(inFileLocation)
            
        #Save data to file
        #saveImageData(dataObject, fileName)
        saveData(dataObject, fileName, flag)
    else:
        raise ValueError("Cannot save file with only a file path")
        
def saveData(dataObject, filename, flag):
    #Set ImageData file name
    imageFileName = os.path.join(filename, "image.fit")

    if not os.path.isdir(filename):
        os.mkdir(filename)

    if flag == "CheckPixels":
        #Set pixelData filename
        pixelDataFileName = os.path.join(filename, "checkPixels.png")

        #Retrieve and save pixel data
        savePixelData(dataObject, pixelDataFileName)
    elif flag == "Publication":
        #Set publication filename
        publicationDataFileName = os.path.join(filename, "publication.png")

        #Retrieve and save publication data
        savePublicationData(dataObject, publicationDataFileName)
    elif flag == "Orbits":
        #Set orbits filename
        #orbitsDataFileName = os.path.join(filename, "orbits.txt")
        orbitsDataFileName = os.path.join(filename, "orbits.png")

        #Retrieve and save orbits data
        saveOrbitsData(dataObject, orbitsDataFileName)
    elif flag == "Simulate":
        simulateDataFileName = os.path.join(filename, "simulate.png")

        #Retrieve and save simulate data
        saveSimulateData(dataObject, simulateDataFileName)
    elif flag == "Zoomed":
        zoomedDataFileName = os.path.join(filename, "zoomed")

        #Retrieve and save zoomed data
        saveZoomedImageData(dataObject, zoomedDataFileName)   
    elif flag == "Photoplot":
        #Retrieve and save photoplot data
        savePhotoPlotData(dataObject, filename)
    
def savePixelData(dataObject, fileName):
    #TODO May need modifying to suit the completed process
    figure = dataObject.getPixelImage()
    
    saveImageData(figure, fileName)

def savePublicationData(dataObject, fileName):
    figure = dataObject.getAnnotatedImage()
    
    saveImageData(figure, fileName)

def saveOrbitsData(dataObject, fileName):
    #TODO May need modifying to suit the completed process
    #Get orbits image from dataObject
    figure = dataObject.getOrbitPlot()
    
    #Save image to file
    saveImageData(figure, fileName)

def saveSimulateData(dataObject, fileName):
    #TODO May need modifying to suit the completed process
    #Get simulate image from dataObject
    simulateArray = dataObject.getSimulateImage()
    
    #Create figure for saving image
    figure = newImage(simulateArray, 6500, 6700)
    
    #Save image to file
    saveImageData(figure, fileName)

def saveZoomedImageData(dataObject, fileName):
    #Get zoomed image from dataObject 
    zoomedObjects = dataObject.getZoomedImages()
    
    ii = 1
    
    for zoomObject in zoomedObjects:
        #Get figure
        figure = zoomObject.getImage()
        
        tempFileName = fileName + str(ii)
        tempFileName = tempFileName + ".png"
        ii = ii + 1
        
        #Save image to file
        saveImageData(figure, tempFileName)

def savePhotoPlotData(dataObject, fileName):
    #Retrieve photometry data from the dataObject in a format suitable for human consumption
    outputString = formatPhotometryData(dataObject)
    
    figure = dataObject.getPhotoplotImage()
    
    dataFileName = os.path.join(fileName, "data.txt")
    imageFileName = os.path.join(fileName, "image.png")
    
    #Save text data to file
    saveTextToFile(outputString, dataFileName)
    
    #Save annotated image to file
    saveImageData(figure, imageFileName)
    
def saveTextToFile(inText, fileName):
    try:
        file = open(fileName, "w")
        file.write(inText)
        file.close()
    except IOError:
        try:
            file.close() 
        except IOError:
            #Failed to close file
            pass
        
def saveImageData(imageData, fileName):
    #Ensure filename is correctly formatted
    fileName = os.path.abspath(fileName)
    
    #Save image data
    try:
        imageData.savefig(fileName)
    except OSError as err:
        print("Error with saving: " + fileName +" to file")
    
#Creates a default file location within the Pictures Folder
def getDefaultFileLocation(): #Warning: Can be quite slow. This function is intended as a backup
    
    #Find Pictures file
    filePath = ""
    
    #Get operation system
    if(platform.system() == 'Windows'):
        start = "\\Libraries\\" #Windows
    elif(platform.system() == 'Linux'):
        start = "\\home\\" #Linux
        
    for dirpath, dirnames, filenames in os.walk(start):
        for dirname in dirnames:
            if(dirname == "Pictures"):
                filePath = os.path.join(dirpath, "Pictures")
        
    today = datetime.today()
    outputFileLocation = os.path.join(filePath, "HighCadenceProcessing")
    outputFileLocation = os.path.join(outputFileLocation, today.strftime("%d_%m_%y"))
    return outputFileLocation

def formatPhotometryData(dataObject):
    #Get slice data
    sliceList = dataObject.getSliceList()
        
    #Get data from photometry into text format
    dataString = "Photometry:\n\n"
    dataString = dataString + "Background brightness: {}\n".format(ImageIntensity.meanBrightness(dataObject))
    #dataString = dataString + "Calibration factor: {}\n".format(dataObject.getMeanCalibrationFactor())
    
    #Set slice counter
    ii = 0
    
    #Get data from each string into text format
    dataString = dataString + "\n_________________________________________\nSlices: \n\n"
    
    for slice in sliceList:
        ii = ii + 1
        dataString = dataString + "Slice {}\n\n".format(ii)
        
        sliceDataString = "Peak brightness: {}\n".format(slice.getPeak())
        sliceDataString = sliceDataString + "X: {}\nY: {}".format(slice.getX(), slice.getY())
        sliceDataString = sliceDataString + "Star magnitude: {}\n".format(slice.getActualBrightness())
        sliceDataString = sliceDataString + "___________________________\n"
        dataString = dataString + sliceDataString
        #dataString = dataString + slice.toString() + "\n_________________________\n"
        
    return dataString