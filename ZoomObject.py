from IncorrectTypeException import IncorrectTypeException #Used to throw errors when input needs to be a specific type and isn't
from InvalidSizeException import InvalidSizeException #Used to throw errors when an input candidate list is an invalid size
import matplotlib as plt #used for checking image type

class ZoomObject:
    def __init__(self, image, padTop=0, padBottom=0, padLeft=0, padRight=0, height=0, width=0):
        if(not isinstance(image, plt.figure.Figure)):
            raise IncorrectTypeException("Images must be of type numpy.ndarray")
        self.image = image
        
        if(not isinstance(padTop, int)):
            raise IncorrectTypeException("Pixels padded must be int")
        self.padTop = padTop
        
        if(not isinstance(padBottom, int)):
            raise IncorrectTypeException("Pixels padded must be int")
        self.padBottom = padBottom
        
        if(not isinstance(padLeft, int)):
            raise IncorrectTypeException("Pixels padded must be int")
        self.padLeft = padLeft
        
        if(not isinstance(padRight, int)):
            raise IncorrectTypeException("Pixels padded must be int")
        self.padRight = padRight
        
        if(not isinstance(height, int)):
            raise IncorrectTypeException("Height must be int")
        self.height = height
        
        if(not isinstance(width, int)):
            raise IncorrectTypeException("Width must be int")
        self.width = width
        
    def getImage(self):
        return self.image
    
    def getPadTop(self):
        return self.padTop
    
    def getPadBottom(self):
        return self.padBottom
    
    def getPadLeft(self):
        return self.padLeft
    
    def getPadRight(self):
        return self.padRight
    
    def getHeight(self):
        return self.height
    
    def getWidth(self):
        return self.width