#This file was created by Tate Hagan
from EmptyFileException import EmptyFileException #imports the Errors that can be thrown by the Data Object
from IncorrectTypeException import IncorrectTypeException
from NoSliceException import NoSliceException
from InvalidSizeException import InvalidSizeException
from InvalidCoordException import InvalidCoordException
from InvalidZoomFactorException import InvalidZoomFactorException
from InvalidFlagException import InvalidFlagException
from DataObject import DataObject #imports the Data Object to be tested
from Slice import Slice #for testing slice methods
from ZoomObject import ZoomObject #Used for Zoomed
import numpy as np #For ImageData16
from astropy.io import fits #For fits file reading
from astropy import wcs #Used for WCS
import matplotlib.pyplot as plt

#Filepaths are hardcoded, may need to be altered on other systems with different data
pathinit = "D:/Capstone Project/Sprint-2/"
pathlegit = pathinit + "TestData/" #The TestData directory provided by the client
validtle = pathlegit + "3le-2019-12-19-08-40-18.txt"
validfit = pathlegit + "0097-fast-slew-5-sec.fit"
validfits = pathlegit + "97-wcs.fits"
pathnonlegit = pathinit + "Non-Formatted Files/"
emptytext = pathnonlegit + "ex1.txt" #An empty text file
blahtext = pathnonlegit + "ex2.txt" #A text file that just has the word 'blah'

validsnr = 10.0

print("Checking test paths:\nValid TLE:{}\nValid Image:{}\nValid WCS:{}\nEmpty Text:{}".format(validtle, validfit, validfits, emptytext))

tests = 0
successes = 0
failures = 0

print("Testing Data Object constructor")

print("Test constructor when no filename passed in")
try:
    tests = tests + 1
    data = DataObject("", 'Photoplot', validsnr)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except EmptyFileException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test constructor with valid input")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Photoplot', validsnr)
    print("SUCCESS-Doesn't throw error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws error:")
    print(e)
    failures = failures + 1

print("Test constructor with non-formatted fit")
try:
    tests = tests + 1
    data = DataObject(emptytext, 'Photoplot', validsnr)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except EmptyFileException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test constructor with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'NotAValidFlag', validsnr)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test constructor with non-float SNR")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Photoplot', "Not a float")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a different function
print("Test getImageData")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Photoplot', validsnr)
    imgOut = data.getImageData()
    with fits.open(validfit) as imghdul: #using the with keyword means that the file will be closed even if an exception is thrown
        imgExp = imghdul[0].data

    comparison = (imgExp == imgOut)
    if(comparison.all()):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(imgExp, imgOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

#We do not space out text for functions with only one test
print("Test getImageData16")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Photoplot', validsnr)
    img16Out = data.getImageData16()
    with fits.open(validfit) as imghdul:
        img = imghdul[0].data
    img16Exp = img.astype(np.int16)
    
    comparison16 = (img16Exp == img16Out)
    if(comparison16.all()):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(img16Exp, img16Out))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test getImageHeader")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Photoplot', validsnr)
    imgHeaderOut = data.getImageHeader()
    with fits.open(validfit) as imghdul:
        imgHeaderExp = imghdul[0].header
    if(imgHeaderExp == imgHeaderOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(imgHeaderExp, imgHeaderOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test getFlag")
try:
    tests = tests + 1
    flagExp = 'Publication'
    data = DataObject(validfit, flagExp, validsnr)
    flagOut = data.getFlag()
    if(flagExp == flagOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(flagExp, flagOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test getSNR")
try:
    tests = tests + 1
    snrExp = 5.0
    data = DataObject(validfit, 'Publication', snrExp)
    snrOut = data.getSNR()
    if(snrExp == snrOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(snrExp, snrOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test setCandGt")
print("Test setCandGt with valid input")
try:
    tests = tests + 1
    correctField0 = np.array([1,2,3]).astype(np.int64)
    correctField1 = np.array([4,5,6]).astype(np.int64)
    correctField = (correctField0, correctField1)
    
    data = DataObject(validfit, 'CheckPixels', validsnr)
    data.setCandGt(correctField)
    print("SUCCESS-No crash")
    successes = successes + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setCandGt with non-tuple")
try:
    tests = tests + 1
    nontuple = 7
    data = DataObject(validfit, 'CheckPixels', validsnr)
    data.setCandGt(nontuple)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1
    
print("Test setCandGt with wrong number of tuple elements")
try:
    tests = tests + 1
    element0 = np.array([1,2]).astype(np.int64)
    element1 = np.array([2,3]).astype(np.int64)
    element2 = np.array([3,4]).astype(np.int64)
    wrongElementTuple = (element0, element1, element2)
    data = DataObject(validfit, 'CheckPixels', validsnr)
    data.setCandGt(wrongElementTuple)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidSizeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setCandGt with non-array elements")
try:
    tests = tests + 1

    wrongElementTypeTuple = (1,2)
    
    data = DataObject(validfit, 'Orbits', validsnr)
    data.setCandGt(wrongElementTypeTuple)
    print("FAILURE-Doesn't throw error")
    failures = failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setCandGt with array elements of incorrect type")
try:
    tests = tests + 1
    
    wrongType0 = np.array([1,2,3]) #No cast to int64
    wrongType1 = np.array([4,5,6])
    wrongtypetuple = (wrongType0, wrongType1)
    
    data = DataObject(validfit, 'Simulate', validsnr)
    data.setCandGt(wrongtypetuple)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setCandGt with unequal array lengths")
try:
    tests = tests + 1
    
    arr0 = np.array([1,2,3]).astype(np.int64)
    arr1 = np.array([4]).astype(np.int64)
    unequalArraysTuple = (arr0, arr1)
    
    data = DataObject(validfit, 'Simulate', validsnr)
    data.setCandGt(unequalArraysTuple)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidSizeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a different function
print("Test getCandGt")
try:
    tests = tests + 1
    candGtExp0 = np.array([1,2,3]).astype(np.int64)
    candGtExp1 = np.array([4,5,6]).astype(np.int64)
    candGtExp = (candGtExp0, candGtExp1)

    data = DataObject(validfit, 'Publication', validsnr)
    data.setCandGt(candGtExp)
    candGtOut = data.getCandGt()
    if(candGtExp == candGtOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(candGtExp, candGtOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test setCandLt")
print("Test setCandLt with valid input")
try:
    tests = tests + 1
    correctField0 = np.array([1,2,3]).astype(np.int64)
    correctField1 = np.array([4,5,6]).astype(np.int64)
    correctField = (correctField0, correctField1)
    
    data = DataObject(validfit, 'Photoplot', validsnr)
    data.setCandLt(correctField)
    print("SUCCESS-No crash")
    successes = successes + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setCandLt with non-tuple")
try:
    tests = tests + 1
    nontuple = 7
    data = DataObject(validfit, 'Photoplot', validsnr)
    data.setCandLt(nontuple)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1
    
print("Test setCandLt with wrong number of tuple elements")
try:
    tests = tests + 1
    element0 = np.array([1,2]).astype(np.int64)
    element1 = np.array([2,3]).astype(np.int64)
    element2 = np.array([3,4]).astype(np.int64)
    wrongElementTuple = (element0, element1, element2)
    data = DataObject(validfit, 'Photoplot', validsnr)
    data.setCandLt(wrongElementTuple)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidSizeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setCandLt with non-array elements")
try:
    tests = tests + 1

    wrongElementTypeTuple = (1,2)
    
    data = DataObject(validfit, 'Photoplot', validsnr)
    data.setCandLt(wrongElementTypeTuple)
    print("FAILURE-Doesn't throw error")
    failures = failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setCandLt with array elements of incorrect type")
try:
    tests = tests + 1
    
    wrongType0 = np.array([1,2,3]) #No cast to int64
    wrongType1 = np.array([4,5,6])
    wrongtypetuple = (wrongType0, wrongType1)
    
    data = DataObject(validfit, 'Photoplot', validsnr)
    data.setCandLt(wrongtypetuple)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setCandLt with unequal array lengths")
try:
    tests = tests + 1
    
    arr0 = np.array([1,2,3]).astype(np.int64)
    arr1 = np.array([4]).astype(np.int64)
    unequalArraysTuple = (arr0, arr1)
    
    data = DataObject(validfit, 'Photoplot', validsnr)
    data.setCandLt(unequalArraysTuple)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidSizeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a different function
print("Test getCandLt")
try:
    tests = tests + 1
    candLtExp0 = np.array([1,2,3]).astype(np.int64)
    candLtExp1 = np.array([4,5,6]).astype(np.int64)
    candLtExp = (candLtExp0, candLtExp1)

    data = DataObject(validfit, 'Photoplot', validsnr)
    data.setCandLt(candLtExp)
    candLtOut = data.getCandLt()
    if(candLtExp == candLtOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(candLtExp, candLtOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test setImgStd")
print("Test setImgStd with valid input")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Publication', validsnr)
    data.setImgStd(np.float64(10))
    print("SUCCESS-Doesn't throw error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setImgStd with invalid input")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Publication', validsnr)
    data.setImgStd("Not a float64")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1
    
print("-----------------------") #Spaces out text as we are now testing a different function
print("Test getImgStd")
print("Test getImgStd with valid conditions")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Publication', validsnr)
    imgStdExp = np.float64(10)
    data.setImgStd(imgStdExp)
    imgStdOut = data.getImgStd()
    if(imgStdExp == imgStdOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(imgStdExp, imgStdOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test setDiffImg")
print("Test setDiffImg with valid input")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Publication', validsnr)
    arr = np.array([1,2,3])
    data.setDiffImg(arr)
    print("SUCCESS-Doesn't throw error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setDiffImg with invalid input")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Publication', validsnr)
    data.setDiffImg("Not an ndarray")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1
    
print("-----------------------") #Spaces out text as we are now testing a different function
print("Test getDiffImg")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Publication', validsnr)
    diffImgExp = np.array([1,2,3])
    data.setDiffImg(diffImgExp)
    diffImgOut = data.getDiffImg()
    comparison = (diffImgExp == diffImgOut)
    if(comparison.all()):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(diffImgExp, diffImgOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

#Test Photoplot functions
print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test setSlice")
print("Test setSlice with valid input")
try:
    tests = tests + 1
    slice1 = Slice(20,30,"Slice1",10, 600.0)
    slice2 = Slice(40,50,"Slice2",15, 450.0)
    slice3 = Slice(60,70,"Slice3",20, 230.0)
    slicesExp = []
    slicesExp.append(slice1)
    slicesExp.append(slice2)
    slicesExp.append(slice3)
    data = DataObject(validfit,'Photoplot', validsnr)
    data.setSlice(20,30,"Slice1",10, 600.0)
    data.setSlice(40,50,"Slice2",15, 450.0)
    data.setSlice(60,70,"Slice3",20, 230.0)
    slicesOut = data.getSliceList()
    
    equal = False
    if(len(slicesExp) == len(slicesOut)):
        equal = True
        ii = 0
        while( (ii < len(slicesExp)) and equal):
            if(not(slicesExp[ii].equals(slicesOut[ii]))):
                equal = False
            ii = ii + 1
    if(equal):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        slicesExpString = []
        for jj in range(len(slicesExp)): #iterates from jj=0 to kk=len(slicesExp)-1
            sliceExp = slicesExp[ii]
            slicesExpString.append(sliceExp.toString)
                    
        slicesOutString = []
        for kk in range(len(slicesOut)):
            sliceOut = slicesOut[ii]
            slicesOutString.append(sliceOut.toString)
        
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted{}".format(slicesExpString, slicesOutString))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setSlice with non-integer x")
try:
    tests = tests + 1
    data = DataObject(validfit,'Photoplot', validsnr)
    data.setSlice("x",30,"Slice",5, 600.0)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setSlice with non-integer y")
try:
    tests = tests + 1
    data = DataObject(validfit,'Photoplot', validsnr)
    data.setSlice(20,"y","Slice",3, 450.0)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setSlice with non-integer width")
try:
    tests = tests + 1
    data = DataObject(validfit,'Photoplot', validsnr)
    data.setSlice(20,30,"Slice","width", 300.0)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setSlice with non-float brightness")
try:
    tests = tests + 1
    data = DataObject(validfit,'Photoplot',validsnr)
    data.setSlice(20,30,"Slice",5,"Brightness")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1
    
print("Test setSlice with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit,'Publication',validsnr)
    data.setSlice(20,30,"Slice",5,300.0)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a different function
print("Test getCurrSlice")
print("Test getCurrSlice with valid conditions")
try:
    tests = tests + 1
    sliceExp = Slice(10,20,"Slice",5, 600.0)
    data = DataObject(validfit,'Photoplot',validsnr)
    data.setSlice(10,20,"Slice",5, 600.0)
    sliceOut = data.getCurrSlice()
    
    sliceExpString = sliceExp.toString()
    sliceOutString = sliceOut.toString()
    if(sliceExpString == sliceOutString):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(sliceExpString,sliceOutString))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test getCurrSlice with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit,'Publication',validsnr)
    sliceOut = data.getCurrSlice()
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test setSliceYl")
print("Test setSliceYl with valid input")
try:
    tests = tests + 1
    data = DataObject(validfit,'Photoplot',validsnr)
    sliceYlExp = 15
    data.setSlice(20,40,"SliceTest",5,600.0)
    data.setSliceYl(sliceYlExp)
    sliceOut = data.getCurrSlice()
    sliceYlOut = sliceOut.getYl()
    if(sliceYlExp == sliceYlOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(sliceYlExp, sliceYlOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setSliceYl with no Slice created")
try:
    tests = tests + 1
    data = DataObject(validfit,'Photoplot',validsnr)
    data.setSliceYl(25)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except NoSliceException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setSliceYl with non-integer yl")
try:
    tests = tests + 1
    data = DataObject(validfit,'Photoplot',validsnr)
    data.setSlice(20,30,"Slice",5,600.0)
    data.setSliceYl("yl")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1
    
print("Test setSliceYl with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit,'Publication',validsnr)
    data.setSliceYl(7)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test setSliceYh")
print("Test setSliceYh with valid input")
try:
    tests = tests + 1
    data = DataObject(validfit,'Photoplot',validsnr)
    sliceYhExp = 55
    data.setSlice(30,50,"SliceTest",5,600.0)
    data.setSliceYh(sliceYhExp)
    sliceOut = data.getCurrSlice()
    sliceYhOut = sliceOut.getYh()
    if(sliceYhExp == sliceYhOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted{}".format(sliceYhExp,sliceYhOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setSliceYh with no Slice created")
try:
    tests = tests + 1
    data = DataObject(validfit,'Photoplot',validsnr)
    data.setSliceYh(50)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except NoSliceException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setSliceYh with non-integer yh")
try:
    tests = tests + 1
    data = DataObject(validfit,'Photoplot',validsnr)
    data.setSlice(20,30,"Slice",5,600.0)
    data.setSliceYh("yh")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setSliceYh with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Publication',validsnr)
    data.setSliceYh(3)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1
    

print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test setSliceBrightnessDiff")
print("Test setSliceBrightnessDiff with valid input")
try:
    tests = tests + 1
    sliceTest = Slice(40,70,"SliceTest",3,600.0)
    data = DataObject(validfit,'Photoplot',validsnr)
    sliceBrightnessDiffExp = 25
    data.setSlice(40,70,"SliceTest",3,600.0)
    data.setSliceBrightnessDiff(sliceBrightnessDiffExp)
    sliceOut = data.getCurrSlice()
    sliceBrightnessDiffOut = sliceOut.getBrightnessDiff()
    if(sliceBrightnessDiffExp == sliceBrightnessDiffOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected{}\nOutputted:{}".format(sliceBrightnessDiffExp,sliceBrightnessDiffOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setSliceBrightnessDiff with no Slice created")
try:
    tests = tests + 1
    data = DataObject(validfit,'Photoplot',validsnr)
    data.setSliceBrightnessDiff(30)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except NoSliceException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setSliceBrightnessDiff with non-integer brightnessDiff")
try:
    tests = tests + 1
    data = DataObject(validfit,'Photoplot',validsnr)
    data.setSlice(20,30,"Slice",5,600.0)
    data.setSliceBrightnessDiff("BrightnessDiff")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setSliceBrightnessDiff with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Publication',validsnr)
    data.setSliceBrightnessDiff(3)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a different function
print("Test getSliceList")
print("Test getSliceList with valid conditions")
try:
    tests = tests + 1
    slicesExp = []
    data = DataObject(validfit, 'Photoplot',validsnr)
    slicesOut = data.getSliceList()
    if(slicesExp == slicesOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(slicesExp, slicesOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1
    
print("Test getSliceList with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Publication',validsnr)
    slices = data.getSliceList()
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a different function

print("Test setMeanCalibrationFactor")
print("Test setMeanCalibrationFactor with valid input")
try:
    tests = tests + 1
    data = DataObject(validfit,'Photoplot',validsnr)
    meanExp = 450.0
    data.setMeanCalibrationFactor(meanExp)
    meanOut = data.getMeanCalibrationFactor()
    if(meanExp == meanOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(meanExp, meanOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setMeanCalibrationFactor with non-float input")
try:
    tests = tests + 1
    data = DataObject(validfit,'Photoplot',validsnr)
    data.setMeanCalibrationFactor("NotAFloat")
    print("FAILURE-No error occurred")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setMeanCalibrationFactor with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Publication',validsnr)
    data.setMeanCalibrationFactor(2.5)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1
    
print("Test getMeanCalibrationFactor with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Publication',validsnr)
    cal = data.getMeanCalibrationFactor()
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a different function
print("Test setPhotoplotImage")
print("Test setPhotoplotImage with valid conditions")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Photoplot', validsnr)
    figure = plt.figure()
    data.setPhotoplotImage(figure)
    print("SUCCESS-Doesn't throw error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setPhotoplotImage with incorrect type")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Photoplot', validsnr)
    data.setPhotoplotImage("Not a matplotlib.figure.Figure")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setPhotoplotImage with incorrect flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Publication', validsnr)
    figure = plt.figure()
    data.setPhotoplotImage(figure)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test getPhotoplotImage")
print("Test getPhotoplotImage with valid conditions")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Photoplot', validsnr)
    photoImgExp = plt.figure()
    data.setPhotoplotImage(photoImgExp)
    photoImgOut = data.getPhotoplotImage()
    if(photoImgExp == photoImgOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(photoImgExp, photoImgOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test getPhotoplotImage with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Publication', validsnr)
    photoImg = data.getPhotoplotImage()
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

#Test Publication functions
print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test setAnnotatedImage")
print("Test setAnnotatedImage with valid input")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Publication',validsnr)
    figure = plt.figure()
    data.setAnnotatedImage(figure)
    print("SUCCESS-Doesn't throw error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setAnnotatedImage with invalid type")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Publication',validsnr)
    data.setAnnotatedImage("Not a pyplot figure")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error")
    failures = failures + 1

print("Test setAnnotatedImage with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels',validsnr)
    figure = plt.figure()
    data.setAnnotatedImage(figure)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a different function
print("Test getAnnotatedImage")
print("Test getAnnotatedImage with valid conditions")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Publication',validsnr)
    figureExp = plt.figure()
    data.setAnnotatedImage(figureExp)
    figureOut = data.getAnnotatedImage()
    if(figureExp == figureOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(figureExp, figureOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1
    
print("Test getAnnotatedImage with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels',validsnr)
    fig = data.getAnnotatedImage()
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

#Test CheckPixels functions
print("-----------------------") #Spaces out text as we are now testing a different function
print("Test setCheckX")
print("Test setCheckX with valid input")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels',validsnr)
    data.setCheckX(1)
    print("SUCCESS-Doesn't throw error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setCheckX with invalid type")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels',validsnr)
    data.setCheckX("Not an int")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setCheckX with invalid value")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels',validsnr)
    data.setCheckX(-1)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidCoordException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1
    
print("Test setCheckX with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Simulate',validsnr)
    data.setCheckX(1)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a different function
print("Test getCheckX with valid conditions")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels',validsnr)
    checkXExp = 10
    data.setCheckX(checkXExp)
    checkXOut = data.getCheckX()
    if(checkXExp == checkXOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(checkXExp, checkXOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test getCheckX with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Simulate',validsnr)
    checkX = data.getCheckX()
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test setCheckY")
print("Test setCheckY with valid input")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels',validsnr)
    data.setCheckY(10)
    print("SUCCESS-Doesn't throw error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setCheckY with invalid type")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels',validsnr)
    data.setCheckY("Not an int")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setCheckY with invalid value")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels',validsnr)
    data.setCheckY(-1)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidCoordException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1
    
print("Test setCheckY with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Simulate',validsnr)
    data.setCheckY(1)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a different function
print("Test getCheckY")
print("Test getCheckY with valid conditions")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels',validsnr)
    checkYExp = 100
    data.setCheckY(checkYExp)
    checkYOut = data.getCheckY()
    if(checkYExp == checkYOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(checkYExp, checkYOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test getCheckY with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Simulate',validsnr)
    checkY = data.getCheckY()
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing function with multiple tests
print("Test setCheckFactor")
print("Test setCheckFactor with valid input")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels',validsnr)
    data.setCheckFactor(float(1.0))
    print("SUCCESS-Doesn't throw error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setCheckFactor with invalid type")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels',validsnr)
    data.setCheckFactor("Not a float")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setCheckFactor with invalid value")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels',validsnr)
    data.setCheckFactor(float(-0.1))
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidZoomFactorException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setCheckFactor with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Simulate',validsnr)
    data.setCheckFactor(float(1.0))
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a different function
print("Test getCheckFactor")
print("Test getCheckFactor with valid conditions")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels',validsnr)
    checkFactorExp = float(2.5)
    data.setCheckFactor(checkFactorExp)
    checkFactorOut = data.getCheckFactor()
    if(checkFactorExp == checkFactorOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(checkFactorExp, checkFactorOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1
    
print("Test getCheckFactor with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Simulate',validsnr)
    zoomFactor = data.getCheckFactor()
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a different function
print("Test setPixelImage")
print("Test setPixelImage with valid inputs")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels', validsnr)
    valid = plt.figure()
    data.setPixelImage(valid)
    print("SUCCESS-Doesn't throw error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setPixelImage with invalid type")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels', validsnr)
    data.setPixelImage(1)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1
    
print("Test setPixelImage with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Simulate',validsnr)
    valid = plt.figure()
    data.setPixelImage(valid)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a different function
print("Test getPixelImage")
print("Test getPixelImage with valid conditions")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels',validsnr)
    pixImgExp = plt.figure()
    data.setPixelImage(pixImgExp)
    pixImgOut = data.getPixelImage()
    if(pixImgExp == pixImgOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(pixImgExp, pixImgOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test getPixelImage with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Simulate',validsnr)
    pixImg = data.getPixelImage()
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test setPadTop")
print("Test setPadTop with valid input")
try:
    tests = tests + 1
    data = DataObject(validfit,'CheckPixels',validsnr)
    data.setPadTop(20)
    print("SUCCESS-Doesn't throw error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setPadTop with non-integer input")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels', validsnr)
    data.setPadTop("Not an int")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Doesn't throw error")
    failures = failures + 1

print("Test setPadTop with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Simulate', validsnr)
    data.setPadTop(25)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Doesn't throw error")
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test getPadTop")
print("Test getPadTop with valid conditions")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels', validsnr)
    padTopExp = 25
    data.setPadTop(padTopExp)
    padTopOut = data.getPadTop()
    if(padTopExp == padTopOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted{}".format(padTopExp, padTopOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test getPadTop with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Simulate', validsnr)
    data.getPadTop()
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test setPadBottom")
print("Test setPadBottom with valid input")
try:
    tests = tests + 1
    data = DataObject(validfit,'CheckPixels',validsnr)
    data.setPadBottom(20)
    print("SUCCESS-Doesn't throw error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setPadBottom with non-integer input")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels', validsnr)
    data.setPadBottom("Not an int")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Doesn't throw error")
    failures = failures + 1

print("Test setPadBottom with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Simulate', validsnr)
    data.setPadBottom(25)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Doesn't throw error")
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test getPadBottom")
print("Test getPadBottom with valid conditions")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels', validsnr)
    padBottomExp = 25
    data.setPadBottom(padBottomExp)
    padBottomOut = data.getPadBottom()
    if(padBottomExp == padBottomOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted{}".format(padBottomExp, padBottomOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test getPadBottom with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Simulate', validsnr)
    data.getPadBottom()
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test setPadLeft")
print("Test setPadLeft with valid input")
try:
    tests = tests + 1
    data = DataObject(validfit,'CheckPixels',validsnr)
    data.setPadLeft(20)
    print("SUCCESS-Doesn't throw error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setPadLeft with non-integer input")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels', validsnr)
    data.setPadLeft("Not an int")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Doesn't throw error")
    failures = failures + 1

print("Test setPadLeft with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Simulate', validsnr)
    data.setPadLeft(25)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Doesn't throw error")
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test getPadLeft")
print("Test getPadLeft with valid conditions")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels', validsnr)
    padLeftExp = 25
    data.setPadLeft(padLeftExp)
    padLeftOut = data.getPadLeft()
    if(padLeftExp == padLeftOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted{}".format(padLeftExp, padLeftOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test getPadLeft with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Simulate', validsnr)
    data.getPadLeft()
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test setPadRight")
print("Test setPadRight with valid input")
try:
    tests = tests + 1
    data = DataObject(validfit,'CheckPixels',validsnr)
    data.setPadRight(20)
    print("SUCCESS-Doesn't throw error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setPadRight with non-integer input")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels', validsnr)
    data.setPadRight("Not an int")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Doesn't throw error")
    failures = failures + 1

print("Test setPadRight with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Simulate', validsnr)
    data.setPadRight(25)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Doesn't throw error")
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test getPadRight")
print("Test getPadRight with valid conditions")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels', validsnr)
    padRightExp = 25
    data.setPadRight(padRightExp)
    padRightOut = data.getPadRight()
    if(padRightExp == padRightOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted{}".format(padRightExp, padRightOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test getPadRight with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Simulate', validsnr)
    data.getPadRight()
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test setHeight")
print("Test setHeight with valid conditions")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels', validsnr)
    data.setHeight(15)
    print("SUCCESS-Doesn't throw error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setHeight with invalid input type")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels', validsnr)
    data.setHeight("Not an int")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setHeight with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Simulate', validsnr)
    data.setHeight(15)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a different function
print("Test getHeight")
print("Test getHeight with valid conditions")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels', validsnr)
    heightExp = 15
    data.setHeight(heightExp)
    heightOut = data.getHeight()
    if(heightExp == heightOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(heightExp, heightOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1
    
print("Test getHeight with invaid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Simulate', validsnr)
    data.getHeight()
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test setWidth")
print("Test setWidth with valid conditions")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels', validsnr)
    data.setWidth(15)
    print("SUCCESS-Doesn't throw error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setWidth with invalid input type")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels', validsnr)
    data.setWidth("Not an int")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setWidth with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Simulate', validsnr)
    data.setWidth(15)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a different function
print("Test getWidth")
print("Test getWidth with valid conditions")
try:
    tests = tests + 1
    data = DataObject(validfit, 'CheckPixels', validsnr)
    widthExp = 15
    data.setWidth(widthExp)
    widthOut = data.getWidth()
    if(widthExp == widthOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(widthExp, widthOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1
    
print("Test getWidth with invaid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Simulate', validsnr)
    data.getWidth()
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

#Test Simulate functions
print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test setSimulateImage")
print("Test setSimulateImage with valid input")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Simulate',validsnr)
    correctField = data.getImageData16()
    data.setSimulateImage(correctField)
    print("SUCCESS-Doesn't throw error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setSimulate image with invalid input type")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Simulate',validsnr)
    data.setSimulateImage("Not a numpy.ndarray")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1
    
print("Test setSimulateImage with wrong number of dimensions")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Simulate', validsnr)
    onlyonedim = np.array([1,2,3]).astype(np.int16)
    data.setSimulateImage(onlyonedim)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidSizeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setSimulateImage with incorrect flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Zoomed',validsnr)
    correctField0 = np.array([1,2,3]).astype(np.int16)
    correctField1 = np.array([4,5,6]).astype(np.int16)
    correctField = (correctField0, correctField1)
    
    data.setSimulateImage(correctField)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test getSimulateImage")
print("Test getSimulateImage with valid conditions")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Simulate',validsnr)
    simulateExp = data.getImageData16()
    data.setSimulateImage(simulateExp)
    simulateOut = data.getSimulateImage()
    comparison = (simulateExp == simulateOut)
    if(comparison.all()):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(figureExp, figureOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test getSimulateImage with incorrect flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Zoomed',validsnr)
    data.getSimulateImage()
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

#Test Zoom Functions
print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test setZoomFactor")
print("Test setZoomFactor with valid input")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Zoomed',validsnr)
    data.setZoomFactor(float(1.0))
    print("SUCCESS-Doesn't throw error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setZoomFactor with invalid type")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Zoomed',validsnr)
    data.setZoomFactor("Not a float")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setZoomFactor with invalid value")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Zoomed',validsnr)
    data.setZoomFactor(float(-0.1))
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidZoomFactorException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setZoomFactor with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Orbits',validsnr)
    data.setZoomFactor(float(1.0))
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a different function
print("Test getZoomFactor")
print("Test getZoomFactor with valid conditions")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Zoomed',validsnr)
    zoomFactorExp = float(2.5)
    data.setZoomFactor(zoomFactorExp)
    zoomFactorOut = data.getZoomFactor()
    if(zoomFactorExp == zoomFactorOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(zoomFactorExp, zoomFactorOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1
    
print("Test getZoomFactor with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Orbits',validsnr)
    zoomFactor = data.getZoomFactor()
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test setZoomedImages")
print("Test setZoomedImages with valid input")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Zoomed', validsnr)
    zoomedObj = ZoomObject(image=plt.figure())
    zoomedImgs = [zoomedObj]
    data.setZoomedImages(zoomedImgs)
    print("SUCCESS-Doesn't throw error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setZoomedImages with non-list input")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Zoomed', validsnr)
    data.setZoomedImages("Not a list")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error")
    print(e)
    failures = failures + 1

print("Test setZoomedImages with non-ZoomObject element in list")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Zoomed', validsnr)
    nonZoomList = []
    nonZoomList.append(3)
    data.setZoomedImages(nonZoomList)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setZoomedImages with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Orbits', validsnr)
    zoomedObj = ZoomObject(image=plt.figure())
    zoomedImgs = [zoomedObj]
    data.setZoomedImages(zoomedImgs)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1
    
print("-----------------------") #Spaces out text as we are now testing a different function
print("Test getZoomedImages")
print("Test getZoomedImages with valid input")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Zoomed', validsnr)
    zoomedObj = ZoomObject(image=plt.figure())
    zoomedImgsExp = [zoomedObj]
    data.setZoomedImages(zoomedImgsExp)
    zoomedImgsOut = data.getZoomedImages()
    if(zoomedImgsExp == zoomedImgsOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(zoomedImgsExp, zoomedImgsOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test getZoomedImages with invalid flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Orbits', validsnr)
    zoomedImgsOut = data.getZoomedImages()
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

#Test Orbit functions
print("-----------------------") #Spaces out text as we are now testing a function with multiple tests
print("Test setTle")
print("Test setTle with valid input")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Orbits', validsnr)
    data.setTle(validtle)
    print("SUCCESS-Doesn't throw error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1
    
print("Test setTle with non-formatted tle")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Orbits', validsnr)
    data.setTle(blahtext)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except EmptyFileException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setTle with empty filename")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Orbits', validsnr)
    data.setTle("")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except EmptyFileException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setTle with wrong flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Photoplot', validsnr)
    data.setTle(validtle)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a different function
print("Test getTleData")
print("Test getTleData with valid conditions")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Orbits', validsnr)
    data.setTle(validtle)
    tleDataOut = data.getTleData()
    with open(validtle) as tle:
        tleDataExp=tle.readlines()
    if(tleDataExp == tleDataOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(tleDataExp, tleDataOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1
    
print("Test getTleData with wrong flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Photoplot', validsnr)
    data.getTleData()
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a different function
print("Test getTleLength")
print("Test getTleData with valid conditions")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Orbits', validsnr)
    data.setTle(validtle)
    tleLengthOut = data.getTleLength()
    with open(validtle) as tle:
        tleData = tle.readlines()
        tleLengthExp=len(tleData)
    if(tleLengthExp == tleLengthOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(tleLengthExp, tleLengthOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test getTleData with wrong flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Photoplot', validsnr)
    data.getTleLength()
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a different function
print("Test setFits")
print("Test setFits with valid input")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Orbits', validsnr)
    data.setFits(validfits)
    print("SUCCESS-Doesn't throw error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test setFits with non-formatted fits")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Orbits', validsnr)
    data.setFits(emptytext)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except EmptyFileException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1
    
print("Test setFits with empty filename")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Orbits', validsnr)
    data.setFits("")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except EmptyFileException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1
    
print("Test setFits with wrong flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Photoplot', validsnr)
    data.setFits(validfits)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a different function
print("Test getWcsInfo")
print("Test getWcsInfo with valid conditions")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Orbits', validsnr)
    data.setFits(validfits)
    wcsInfoOut = data.getWcsInfo()
    wcsInfoExp = None
    with fits.open(validfits):
        wcsInfoExp = wcs.WCS(validfits)

    wcsInfoExpStr = wcsInfoExp.to_header_string()
    wcsInfoOutStr = wcsInfoOut.to_header_string()
    if(wcsInfoExpStr == wcsInfoOutStr):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(wcsInfoExp, wcsInfoOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1

print("Test getWcsInfo with wrong flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Photoplot', validsnr)
    data.getWcsInfo()
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1
    
print("-----------------------") #Spaces out text as we are now testing a different function
print("Test setOrbitPlot")
print("Test setOrbitPlot with valid conditions")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Orbits',validsnr)
    figure = plt.figure()
    data.setOrbitPlot(figure)
    print("SUCCESS-Doesn't throw error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1
    
print("Test setOrbitPlot with invalid type")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Orbits',validsnr)
    data.setOrbitPlot("Not a figure")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("Test setOrbitPlot with incorrect flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Photoplot',validsnr)
    figure = plt.figure()
    data.setOrbitPlot(figure)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are now testing a different function
print("Test getOrbitPlot")
print("Test getOrbitPlot with valid conditions")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Orbits',validsnr)
    figureExp = plt.figure()
    data.setOrbitPlot(figureExp)
    figureOut = data.getOrbitPlot()
    if(figureExp == figureOut):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:{}\nOutputted:{}".format(figureExp, figureOut))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occurred:")
    print(e)
    failures = failures + 1
    
print("Test getOrbitPlot with incorrect flag")
try:
    tests = tests + 1
    data = DataObject(validfit, 'Photoplot',validsnr)
    data.getOrbitPlot()
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidFlagException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are finished testing
print("-----------------------")
print("Tests: {}".format(tests))
print("Successes: {}".format(successes))
print("Failures: {}".format(failures))