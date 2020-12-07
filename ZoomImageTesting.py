#This file was created by Wayne Dreyer
#It serves to test the imageZooming functions
#All Files in ./TestImages are critical to this testing

#Usage python -m unittest ZoomImageTesting

import unittest
import ZoomImage
import os
from PIL import Image
from PIL import ImageChops
from unittest.mock import Mock
import numpy as np

class ZoomImageTesting(unittest.TestCase):

    ##This test checks if the returned image is identical to a known correct image
    def test_imageAgainstKnown(self):
        expectedResult = Image.open("./TestImages/moon512-512-3x.PNG")
        newImage = ZoomImage.zoomImage("./TestImages/moon1024x1024.jpg", 512, 512, 3)
        #The image is temporarily saved as PIL can make minor quality changes when saving images that can cause diff results to change
        newImage.save("temp2.PNG", format=None) 
        newImage = Image.open('./temp2.PNG')
        diff = ImageChops.difference(newImage, expectedResult)
        os.remove('./temp2.PNG') #Calling on the operating system to delete the temporarily saved file
        self.assertFalse(diff.getbbox())


    ##This test checks to ensure the returned image is of the expected dimensions
    def test_imageSize(self):
        mockedObject = Mock()
        mockedObject.getImageData()
        mockedObject.getZoomX()
        mockedObject.getZoomY()
        mockedObject.getZoomFactor()
        mockedObject.getImageData.return_value = np.arange(1000000).reshape(1000,1000)
        mockedObject.getZoomX.return_value = 500
        mockedObject.getZoomY.return_value = 500
        mockedObject.getZoomFactor.return_value = 2
        self.assertEqual(len(ZoomImage.zoomImage(mockedObject)), 500) #Ensuring height is correct
        self.assertEqual(len(ZoomImage.zoomImage(mockedObject)[0]), 500) #Ensuring width is correct


        #newImage = ZoomImage.zoomImage("./TestImages/moon1024x1024.jpg", 512, 512, 3)
        #width, height = newImage.size #Get the size of the returned image
        #self.assertEqual(height, 340) #Ensuring the height of the new image is the expected 340px
        #self.assertEqual(width, 340) #Ensuring the height of the new image is the expected 340px

    ##Testing to ensure we can create a zoomed image given a candidate location near the edge of the image
    def test_offCenter(self):
        try:
            newImage = ZoomImage.zoomImage("./TestImages/moon1024x1024.jpg", 1, 1, 3) #Candidate locaton 1,1 with 3x zoom
        except SystemError:
            self.fail("test_offCenter failed due to an exception") #if a SystemError occurred fail the test


    
        
