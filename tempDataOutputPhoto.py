#This file was created by Josh Renshaw
#This is a PLACEHOLDER file to enable testing of the Photometry/Output GUIs
from FOBPhoto import *

class tempDataOutput:
    def getPlot(self):
        return example_image

    def getNewPlot(self, inLow, inHigh):
        new_fig = newImage(self, inLow, inHigh)
        return new_fig
        
