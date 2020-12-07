# ****************************************************************
# Author: Sheldon Dorgelo
# Date (last edited): 23/10/2020
# Purpose: tests Orbits.py
# Usage: python3 -m unittest TestOrbits
# ****************************************************************

import DataObject
import DataProcessor
import Orbits
from astropy.io import fits
import matplotlib.pyplot as plt
import time as tm
import unittest

class TestOrbits(unittest.TestCase):
    def test_PlotCreation(self):
        # checks if a plot is produced
        validtle = "Test-FOB-data/3le-2019-12-19-08-40-18.txt"
        validfit = "Test-FOB-data/0097-fast-slew-5-sec.fit"
        validfits = "Test-FOB-data/97-wcs.fits"
        validflag = 'Orbits'
        validsnr = 10.0
        testDataObject = DataObject.DataObject(validfit, validflag, validsnr)
        testDataObject.setTle(validtle)
        testDataObject.setFits(validfits)
        DataProcessor.detectCandidates(testDataObject)

        start = tm.time() # used for testing how long the calculations took

        Orbits.orbits(testDataObject)

        end = tm.time()
        #print("Orbits took", end-start, "seconds") #uncomment to display time taken

        plt.show() # uncomment to display image
        assert plt.gcf().number == 1