#This file was created by Julian Harrison

class Slice:
    __x = 0
    __y = 0
    __name = ""
    __width = 0
    __yl = 0
    __yh = 0
    __brightnessDifference = 0
    
    def __init__(self, x, y, name, width, actualBrightness):
        self.x = x
        self.y = y
        self.name = name
        self.width = width
        self.yl = 0
        self.yh = 0
        self.brightnessDifference = 0
        self.actualBrightness = actualBrightness
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getName(self):
        return self.name
    
    def getWidth(self):
        return self.width
    
    def getYL(self):
        return self.yl
    
    def setYL(self, yl):
        self.yl = yl
        
    def getYH(self):
        return self.yh
    
    def setYH(self, yh):
        self.yh = yh
    
    def getBrightnessDiff(self):
        return self.brightnessDifference
    
    def setBrightnessDiff(self, brightnessDifference):
        self.brightnessDifference = brightnessDifference
        
    def getActualBrightness(self):
        return self.actualBrightness
    
    def setActualBrightness(self, actualBrightness):
        self.actualBrightness = actualBrightness