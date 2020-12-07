#This file was created by Wayne Dreyer.
#It serves to crate a difference image using the previously calculated average light intensity,
# as a simulation of the background noise, subtracting it from the image

import numpy as np
import ImageIntensity as imI
import matplotlib.pyplot as plt
#import DataObject as dataObject

#Takes in a data object, calls upon ImageIntensity functions to get relevant data, then creates new difference image based off this data
def simulate(obj):
    snr=obj.getSNR()
    originalImage = obj.getImageData()
    simulation = np.random.normal(imI.meanBrightness(obj), imI.stdBrightness(obj), (len(originalImage), (len(originalImage[0]))))
    simDiff = np.diff(simulation, axis=0)
    simMean = np.mean(simDiff)
    simstd=np.std(simDiff)
    #print("Residual simulated image mean and std =",simMean, simstd)
    #all indices with a value greater than signal to noise ratio*standard deviation
    simGreater=np.nonzero(simDiff>snr*simstd)
    #all indices with a value Less than signal to noise ratio*standard deviation
    simLess=np.nonzero(simDiff<-1*snr*simstd)
    
    
    plt.figure(figsize=(15,10))
    
    return simDiff
    
    
