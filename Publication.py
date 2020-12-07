# ****************************************************************
# Author: Sheldon Dorgelo
# Date (last edited): 02/11/2020
# Purpose: creates a plot with the detections highlighted for
#          easier viewing
# ****************************************************************

import DataObject
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

def publication(dataObject):
    # store annotated figure into data object
    dataObject.setAnnotatedImage(createAnnotatedImage(dataObject))

# creates an image with annotations to highlight detections
def createAnnotatedImage(dataObject):
    diffImg = dataObject.getDiffImg() # get the data from dataObject
    imgStd = dataObject.getImgStd()
    more = dataObject.getCandGt()
    less = dataObject.getCandLt()
    
    newFigure = plt.figure(figsize=(12,8))
    plt.imshow(diffImg,clim=(-imgStd, imgStd)) # set limit on displayed colours

    for i in range(len(more[0])): #from 0 to 1-number of bright detections
        text = (more[1][i],more[0][i]) # coordinates of detection in (x, y) form
        plt.annotate(text,(more[1][i],more[0][i]),color='black',fontsize='large',fontweight='bold',ha='center')
    for i in range(len(less[0])): #from 0 to 1-number of dark detections
        text = (less[1][i],less[0][i])
        plt.annotate(text,(less[1][i],less[0][i]),color='black',fontsize='large',fontweight='bold',ha='center')

    plt.plot(less[1],less[0],'bo') # plots blue dots for each dark detection
    plt.plot(more[1],more[0],'ro') # plots red dots for each bright detection
    plt.xlabel("Pixel number")
    plt.ylabel("Pixel number")
    plt.colorbar()
    
    return newFigure