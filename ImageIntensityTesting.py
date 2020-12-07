#This file was created by Wayne Dreyer
#It serves to test the imageIntensity functions
#Usage python -m unittest ImageIntensityTesting.py
import unittest
from unittest.mock import Mock
import ImageIntensity
import numpy as np

class ImageIntensityTesting(unittest.TestCase):

    def test_mean(self):
        mockedObject = Mock()
        mockedObject.getImageData()
        mockedObject.getImageData.return_value = np.arange(1000)
        self.assertEqual(ImageIntensity.meanBrightness(mockedObject), 499.5)

    def test_std(self):
        mockedObject = Mock()
        mockedObject.getImageData()
        mockedObject.getImageData.return_value = np.array([1,1,1,1])
        self.assertEqual(ImageIntensity.stdBrightness(mockedObject), 0.0)
        
