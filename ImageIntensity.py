#This file was created by Wayne Dreyer
import numpy as np 
#import DataObject as DataObject

#Calculates the mean and standard deviation of light intensity in the given image data

#Takes in a data object, gets the image array from that object and returns the arrays mean as a float
def meanBrightness(obj):
    imageData = obj.getImageData()
    data16 = imageData.astype(np.int16) #don't know why prototype code converts data to int16, need to look at output data of dataobject.imagedata()
    imageMean = np.mean(data16)
    return imageMean


#Takes in a data object, gets the image array from that object and returns the arrays standard deviation as a float
def stdBrightness(obj):
    imageData = obj.getImageData()
    data16 = imageData.astype(np.int16) #Same as above, converted to int16, awaiting completion of dataobject to view imagedata
    imageStd = np.std(data16)
    return imageStd
