# ****************************************************************
# Author: Sheldon Dorgelo
# Date (last edited): 02/11/2020
# Purpose: tests the functionality of Publication.py
# Usage: python3 -m unittest TestPublication
# ****************************************************************

import unittest
import Publication
import DataObject #used for dummy object
import DataProcessor #used to detect candidates and store in dummy object
import matplotlib.pyplot as plt

class TestPublication(unittest.TestCase):
    def test_CreateAnnotatedImage(self):
        # checks if figure successfully created
        validfit = "Test-FOB-data/0097-fast-slew-5-sec.fit"
        testDataObject = DataObject.DataObject(validfit, "Publication", 10.0)
        DataProcessor.detectCandidates(testDataObject)
        Publication.publication(testDataObject)

        #print("Less: ",testDataObject.getCandLt())
        #print("More: ",testDataObject.getCandGt())

        # checks that a figure was created
        #plt.show() # uncomment this line to display the image (for manual testing purposes as described below)
        assert plt.gcf().number == 1

# --------------------------
# MANUAL TESTING NOTES
# --------------------------
# Due to not being able to test if all the data points have been correctly plotted,
# this needs to be manually checked.
#
# For this test object, these are the coordinates as found by data processor to be
# detections: Less are blue dots and More are red dots
#  - Less: (4463,148),(3245,153),(4748,303),(5081,373),(3050,527),(1543,804),(458,837),(4205,1027),(4472,1041),(5054,1041),
#          (931,1356),(4669,1363),(2253,1530),(2254,1530),(2253,1542),(2253,1562),(1909,1591),(2253,1594),(2254,1613),(2253,1628),
#          (2256,1682),(2254,1683),(2254,1687),(2256,1691),(2254,1695),(2256,1696),(2253,1710),(2253,1711),(2254,1711),(2254,1723),
#          (2483,1803),(1111,1841),(1628,2081),(628,2105),(3207,2505),(4000,2570),(3691,2636),(2323,2844),(2594,2989),(1085,3049),
#          (2940,3221),(1405,3309),(4333,3387),(5101,3398),(1256,3411),(2238,3439)
#  - More: (893,410),(4835,537),(54,1011),(4944,1015),(4638,1096),(1039,1163),(4829,1279),(2253,1529),(2252,1537),(2253,1537),
#          (2253,1541),(2254,1541),(2252,1545),(2253,1555),(2254,1555),(2252,1569),(2254,1579),(2254,1593),(2254,1635),(2255,1638),
#          (2256,1693),(2255,1704),(2253,1712),(1196,1723),(1401,1784),(2331,1903),(1842,2485),(3691,2635),(514,2965),(1033,2970)
# 
# These coordinates can also be displayed by uncommenting the print() lines above
#
# With these coordinates, the produced image (uncomment plt.show() above to display it) was
# manually checked to ensure that each coordinate with its corresponding colour is correct.
# Where the detections are bunched up, use the rectangle zoom functionality to display it clearer