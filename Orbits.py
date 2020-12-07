# ****************************************************************
# Author: Sheldon Dorgelo
# Date (last edited): 03/11/2020
# Purpose: checks the list of known orbitting object and compares
#          them to detected candidates. If candidate is close to
#          position of a known orbitting object, that orbitting object
#          is added to the list of objects to plot
# ****************************************************************

import DataObject
import ephem
import math
import multiprocessing
from astropy.wcs import WCS #used for calculating ra and dec of 
import matplotlib.pyplot as plt #used for creating a new plot
from matplotlib.patches import Polygon

def orbits(dataObject):
    gatech = ephem.Observer()

    more = dataObject.getCandGt() # get the detected candidates
    less = dataObject.getCandLt()
    tle = dataObject.getTleData() # get the TLE or 3LE file
    tlel = dataObject.getTleLength() # get length of that file
    elementLines = 2 # for TLE files (default value)
    wcs = dataObject.getWcsInfo()

    # contains the lists for ra and dec of detected candidates
    candidateRA = []
    candidateDec = []

    manager = multiprocessing.Manager()
    matchesRA1 = manager.list()
    matchesRA2 = manager.list()
    matchesRA3 = manager.list()
    matchesRA4 = manager.list()
    matchesDec1 = manager.list()
    matchesDec2 = manager.list()
    matchesDec3 = manager.list()
    matchesDec4 = manager.list()
    firstMatchRA1 = manager.list()
    firstMatchRA2 = manager.list()
    firstMatchRA3 = manager.list()
    firstMatchRA4 = manager.list()
    firstMatchDec1 = manager.list()
    firstMatchDec2 = manager.list()
    firstMatchDec3 = manager.list()
    firstMatchDec4 = manager.list()
    matchesName1 = manager.list()
        
    tm = dataObject.getImageHeader()['DATE'] # extracts the date/time from the header of the image
    time = tm[:4]+'/'+tm[5:7]+'/'+tm[8:10]+' '+tm[11:13]+':'+tm[14:16]+':'+tm[17:] # formatted time
    date = ephem.Date(time)

    if(tle[0].startswith("0")): #check if the number of lines per element is 3
        elementLines = 3 # for 3LE files

    # calculate ra and dec for bright candidate objects and add to above lists
    for i in range(len(more[0])):
        r,d = wcs.all_pix2world(more[1][i], more[0][i],0)
        candidateRA.append(r)
        candidateDec.append(d)

    # calculate ra and dec for dark candidate objects and add to above lists
    for j in range(len(less[0])):
        r,d = wcs.all_pix2world(less[1][j], less[0][j],0)
        candidateRA.append(r)
        candidateDec.append(d)

    # set up multiprocessing to reduce computational times
    processA = multiprocessing.Process(target = calculatePositions, 
        args = [-60, -30, gatech, date, tle, tlel, elementLines, candidateRA, 
        candidateDec, matchesRA1, matchesDec1, matchesName1, firstMatchRA1, firstMatchDec1])
    processB = multiprocessing.Process(target = calculatePositions, 
        args = [-30, 0, gatech, date, tle, tlel, elementLines, candidateRA, 
        candidateDec, matchesRA2, matchesDec2, matchesName1, firstMatchRA2, firstMatchDec2])
    processC = multiprocessing.Process(target = calculatePositions, 
        args = [0, 30, gatech, date, tle, tlel, elementLines, candidateRA, 
        candidateDec, matchesRA3, matchesDec3, matchesName1, firstMatchRA3, firstMatchDec3])
    processD = multiprocessing.Process(target = calculatePositions, 
        args = [30, 60, gatech, date, tle, tlel, elementLines, candidateRA, 
        candidateDec, matchesRA4, matchesDec4, matchesName1, firstMatchRA4, firstMatchDec4])

    # do processing
    processA.start()
    processB.start()
    processC.start()
    processD.start()
    #wait until processes are finished
    processA.join()
    processB.join()
    processC.join()
    processD.join()

    #combine the lists and convert them into a python list
    matchesRA = list(matchesRA1) + list(matchesRA2) + list(matchesRA3) + list(matchesRA4)
    matchesDec = list(matchesDec1) + list(matchesDec2) + list(matchesDec3) + list(matchesDec4)
    firstMatchesRA = list(firstMatchRA1) + list(firstMatchRA2) + list(firstMatchRA3) + list(firstMatchRA4)
    firstMatchesDec = list(firstMatchDec1) + list(firstMatchDec2) + list(firstMatchDec3) + list(firstMatchDec4)
    matchesName = list(matchesName1)

    image = dataObject.getImageData()
    imageData = [] # will contain 4 elements: {[RA,dec(BL)], [RA,dec(BR)], [RA,dec(TR)], [RA,dec(TL)]}
    #INCREASING y coordinate correlates to INCREASING RA
    #INCREASING x coordinate correlates to DECREASING Dec

    # calculate ra and dec of all corners in the image
    imageData.append(wcs.all_pix2world(len(image[0]),0,0)) #bottom left
    imageData.append(wcs.all_pix2world(len(image[0]),len(image),0)) #bottom right
    imageData.append(wcs.all_pix2world(0,len(image),0)) # top right
    imageData.append(wcs.all_pix2world(0,0,0)) #top left

    # create and save the plot to data object
    dataObject.setOrbitPlot(createFigure(matchesRA, matchesDec, candidateRA, candidateDec, imageData,
        firstMatchesRA, firstMatchesDec, matchesName))

def calculatePositions(start, end, gatech, date, tle, tlel, elementLines, 
    candidateRA, candidateDec, matchesRA, matchesDec, matchesName, firstMatchRA, firstMatchDec):
    for dt in range(start, end): # total time = 120 seconds
        gatech.date = date + dt/86400 # 86400 = number of seconds in a day
        for i in range(0, tlel-1, elementLines): # for each element in catalog 
            try:          #"junk" is a placeholder string
                # FOR TLE: "junk", i, i+1; FOR 3LE: "junk", i+1, i+2
                sat = ephem.readtle("junk",tle[i+elementLines-2],tle[i+elementLines-1])
                sat.compute(gatech)                
                ra = math.degrees(float(repr(ephem.degrees(sat.ra))))
                dec = math.degrees(float(repr(ephem.degrees(sat.dec))))
                
                for j in range(len(candidateRA)): # compare against each detected candidate
                    if(abs(candidateRA[j]-ra) < 2 and abs(candidateDec[j]-dec) < 2):
                        matchesRA.append(ra)
                        matchesDec.append(dec)
                        #add name of orbitting object to list to be annotated in plot later (only for 3LE files)
                        if(elementLines == 3):
                            if not tle[i][2:] in matchesName: # get the actual name instead of "junk" if its a 3LE file
                                matchesName.append(tle[i][2:]) #name to be annotated without the '0 ' in front
                                firstMatchRA.append(ra)    #coordinates for annotation
                                firstMatchDec.append(dec)
            except RuntimeError as e:
                print(e) #probably a problem with the tle/3le file

def createFigure(matchesRA, matchesDec, candidateRA, candidateDec, imageData,
                 firstMatchesRA, firstMatchesDec, matchesName):
    newFigure = plt.figure(figsize=(12,8))

    plt.scatter(matchesRA, matchesDec, c = 'g') # plot orbitting objects in green
    plt.scatter(candidateRA, candidateDec, c = 'r') # plot candidate objects in red
    
    # set limits on x and y
    lowRA = min(candidateRA) - 2
    highRA = max(candidateRA) + 2
    lowDec = min(candidateDec) - 2
    highDec = max(candidateDec) + 2
    plt.xlim(lowRA, highRA)
    plt.ylim(lowDec, highDec)
    plt.xlabel("RA (deg)")
    plt.ylabel("Dec (deg)")

    #place names as annotations for orbiting objects
    for i in range(len(matchesName)):
        plt.annotate(matchesName[i],(firstMatchesRA[i], firstMatchesDec[i]),
            color='black',fontsize='small',ha='center')

    #add border to display the edges of the actual image
    plt.gca().add_patch(Polygon(imageData,fill=False,color='black',linewidth=1))
    
    return newFigure