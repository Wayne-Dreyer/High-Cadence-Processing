#This file was created by Wayne Dreyer
#It serves to create a zoomed/cropped image around the detected candidate

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PIL import Image
import math
from ZoomObject import ZoomObject
#import DataObject as dataObject

#Takes in path to the image we wish to zoom, the x y coordinates of the candidate 
#And a zoomfactor ie 2x would be to half the current dimensions of the image with candidate as close to center as possible 
def zoomImage(dataObject):
    imgList = []
    zoomFactor = dataObject.getZoomFactor()
    more = dataObject.getCandGt()
    for i in range(len(more[0])):
        candX, candY = (more[1][i], more[0][i])
        result = createZoomed(candX, candY, dataObject.getZoomFactor(), dataObject)
        imgList.append(ZoomObject(result[0], result[1], result[2], result[3], result[4], int(result[5]), int(result[6])))

    less = dataObject.getCandLt()
    for i in range(len(less[0])):
        candX, candY = (less[1][i],less[0][i])
        result = createZoomed(candX, candY, dataObject.getZoomFactor(), dataObject)
        imgList.append(ZoomObject(result[0], result[1], result[2], result[3], result[4], int(result[5]), int(result[6])))

    dataObject.setZoomedImages(imgList)

def checkPixels(dataObject):
    xCoord = dataObject.getCheckX()
    yCoord = dataObject.getCheckY()
    zoomfactor = dataObject.getCheckFactor()
    img, padTop, padBottom, padLeft, padRight, height, width = createZoomed(xCoord, yCoord, zoomfactor, dataObject)
    dataObject.setPixelImage(img)
    dataObject.setPadTop(padTop)
    dataObject.setPadBottom(padBottom)
    dataObject.setPadLeft(padLeft)
    dataObject.setPadRight(padRight)
    dataObject.setHeight(int(height))
    dataObject.setWidth(int(width))

def createZoomed(xCoord, yCoord, zoomFactor, dataObject):
    originalImage = dataObject.getImageData()
    height = len(originalImage)
    width = len(originalImage[0])
    newWidth = width/zoomFactor
    newHeight = height/zoomFactor
    padLeft = 0
    padRight = 0
    padBottom = 0
    padTop = 0
    
    #Calculate new image width as range of original image
    if((width - xCoord > newWidth/2) and (xCoord > newWidth/2)): #theres enough space to have candidate at center on x axis
        left = math.floor(xCoord - newWidth/2)
        right = math.floor(xCoord + newWidth/2)
    elif(not(width - xCoord > newWidth/2)): # if there is not enough space to the right of candidate
        right = width
        left = math.floor(xCoord - newWidth/2)
        padRight = newWidth - (right-left) #the difference between the calculated width and possible width = needed padding
    elif(not(xCoord > newWidth/2)): #if there is not enough space to the left of the candidate
        left = 0
        right = math.floor(xCoord + newWidth/2)
        padLeft = newWidth - (right-left) #the difference between the calculated width and possible width = needed padding

    #calculate new image height as range of original image height
    if((height - yCoord > newHeight/2) and (yCoord > newHeight/2)): #theres enough space to have candidate at center on y axis
        bottom = math.floor(yCoord - newHeight/2)
        top = math.floor(yCoord + newHeight/2)
    elif(not(height - yCoord > newHeight/2)): # if there is not enough space to the bottom of candidate
        top = height
        bottom = math.floor(yCoord - newHeight/2)
        padBottom = newHeight - (top-bottom) #the difference between the calculated height and possible height = needed padding
    elif(not(yCoord > newHeight/2)): #if there is not enough space to the top of the candidate
        bottom = 0
        top = math.floor(yCoord + newHeight/2)
        padTop = newHeight - (top-bottom) #the difference between the calculated height and possible height = needed padding

    
    #the actual cropping
    #croppedImage = originalImage.crop((left, bottom, right, top)) 

    #plt.axis(left, right, bottom, top)  ##This is how you crop a plot from matplotlib, however this doesn't actually crop the data just what is displayed
    croppedImage = originalImage[bottom:top, left:right] # slicing/cropping the image array
    return newFigure(croppedImage, 6500, 6700, ((len(croppedImage[0]) + padLeft + padRight)/2), ((len(croppedImage) + padTop + padBottom)/2), xCoord, yCoord), math.floor(padTop), math.floor(padBottom), math.floor(padLeft), math.floor(padRight), newWidth, newHeight

def newFigure(image, cmin, cmax, xLocation, yLocation, xCoord, yCoord):
    #Create figure
    newFig = plt.figure(figsize=(10,8))
    
    #Set image data into figure
    plt.imshow(image, clim=(cmin,cmax))
    
    #Set axes and a colourbar
    plt.xlabel("Pixel number")
    plt.ylabel("Pixel number")
    plt.colorbar()
    
    #Annotate the figure
    text=(xCoord,yCoord)
    plt.plot(xLocation, yLocation, 'bo')
    plt.annotate(text,(xLocation,yLocation), color='black', fontsize='large',fontweight='bold')
    
    return newFig

def showImage(zoomedImage):
        plt.imshow(zoomedImage)
        
def saveImage(filename, zoomedImage):
        plt.imshow(zoomImage)
        plt.savefig(filename)

