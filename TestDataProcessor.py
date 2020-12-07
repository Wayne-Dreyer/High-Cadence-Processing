# file created by Sheldon Dorgelo
# this file is used to test DataProcessor.py

import DataProcessor # file being tested
import DataObject # data used for testing
from astropy.io import fits
import numpy as np

#-----------------------------------------------------------------------------
# Testing detectCandidates function
#-----------------------------------------------------------------------------

print("\nBeginning manual test for detectCandidates function")

print("Opening test file...")
hdul = fits.open('Test-FOB-data/IMG_11-final.fit') # file path may need to be edited for other systems
data = hdul[0].data

imgInt16 = data.astype(np.int16)
snr = 10 # signal to noise ratio = 10:1

# Calculate image mean and standard deviation
imgMean = np.mean(imgInt16) # get average of image
imgStd = np.std(imgInt16) # get standard deviation of image

print("Image mean = ", imgMean, "\nImage standard deviation = ", imgStd)
print("Correct image mean = ", 6558.1) #Based on siril statistics

# Create a differenced image
diffImg = np.diff(imgInt16, axis=0)
diffImgMean = np.mean(diffImg)
diffImgStd = np.std(diffImg)
print("Diff image mean = ", diffImgMean, "\nDiff image standard deviation = ", diffImgStd)

# Find detections above SNR limit (snr = 10) in differenced image
more = np.nonzero(diffImg > snr*diffImgStd)
less = np.nonzero(diffImg < -1*snr*diffImgStd)
print("More = ", more)
print("Less = ", less)

print("There should be a detection at roughly x =", 115, "y =", 1659)

# x = 3461, y = 5190 on image
# x = 5190, y = 3461 in siril
# Bright pixels exist at about (1659, 3346) according to siril when manually checking
# on siril, the x axis is bottom starting bottom left, y axis is side starting top right
# on image, x asis is side starting bottom left, y axis is side starting bottom left
# these coordinates would correlate to x = 115 (3461-3346), y = 1659