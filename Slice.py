#This file was created by Tate Hagan
class Slice:
    def __init__(self, x, y, name, width, actualBrightness):
        self.x = x
        self.y = y
        self.name = name
        self.width = width
        self.actualBrightness = actualBrightness
        
        self.yl = None
        self.yh = None
        self.brightnessDiff = None
        self.peak = None
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getName(self):
        return self.name
    
    def getWidth(self):
        return self.width
    
    def getActualBrightness(self):
        return self.actualBrightness

    #The below three methods are used to set output fields
    def setYl(self, yl):
        self.yl = yl
    
    def setYh(self, yh):
        self.yh = yh

    def setBrightnessDiff(self, brightnessDiff):
        self.brightnessDiff = brightnessDiff
    
    def setPeak(self, inPeak):
        self.peak = inPeak

    #The below three methods are used to retrieve output data
    def getYl(self):
        return self.yl
    
    def getYh(self):
        return self.yh
    
    def getBrightnessDiff(self):
        return self.brightnessDiff
    
    def getPeak(self):
        return self.peak
    
    #Used for checking equality by Test harness
    def equals(self, other):
        isEqual = False
        if(isinstance(other, Slice)):
            isEqual = ( (self.x == other.getX()) and (self.y == other.getY()) and (self.name == other.getName()) and (self.width == other.getWidth()) and (self.yl == other.getYl()) and (self.yh == other.getYh()) and (self.brightnessDiff == other.getBrightnessDiff()) and (self.peak == other.getPeak()) )
        return isEqual
    
    #Used for output by Test harness
    def toString(self):
        return "x:{}\ny:{}\nname:{}\nwidth:{}\nyl:{}\nyh:{}\nbrightness diff:{}\npeak{}".format(self.x,self.y,self.name,self.width, self.yl, self.yh, self.brightnessDiff, self.peak)