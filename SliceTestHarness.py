#This file was created by Julian Harrison
import unittest
from Slice import Slice

#These tests are set to test the recent addition of the actualBrightess variable within Slice
class SliceTestHarness(unittest.TestCase):
    
    def testObjectCreation(self):
        slice = Slice(2000, 2500, "Star 1", 30, 20000)
        
        self.assertEqual(slice.getX(), 2000)
        self.assertEqual(slice.getY(), 2500)
        self.assertEqual(slice.getName(), "Star 1")
        self.assertEqual(slice.getWidth(), 30)
        self.assertEqual(slice.getActualBrightness(), 20000)
        
    def testBrightnessChange(self):
        slice = Slice(2000, 2500, "Star 1", 50, 20000)
        
        slice.setActualBrightness(22000)
        
        self.assertEqual(slice.getActualBrightness(), 22000)
        
    def testEqualsMethod(self):
        sliceOne = Slice(2000, 2500, "Star 1", 50, 20000)
        sliceTwo = Slice(2000, 2500, "Star 1", 50, 20000)
        
        self.assertTrue(sliceOne.equals(sliceTwo))