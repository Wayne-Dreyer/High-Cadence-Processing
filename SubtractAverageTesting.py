#This file was created by Wayne Dreyer
#It serves to test the noise reduction subtraction functions

#Usage python -m unittest SubtractAverageTesting

import unittest
from unittest.mock import Mock
import SubtractAverage
import numpy as np

class SubtractAverageTesting(unittest.TestCase):
    
    #This checks to ensure the returned array has a size no larger than the original
    def test_IsPositive(self):
        mockedObject = Mock()
        mockedObject.getImageData()
        mockedObject.getSNR()
        mockedObject.getSNR.return_value = 10.00
        mockedObject.getImageData.return_value = np.linspace((1,2),(10,20),10)
        self.assertGreater(len(np.linspace((1,2),(10,20),10)), len(SubtractAverage.simulate(mockedObject)))