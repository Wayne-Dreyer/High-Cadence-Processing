#This file was created by Tate Hagan
def validateTle(tlefile):
    valid = False
    if(checktle(tlefile)):
        valid = True
    if(checkthreele(tlefile)):
        valid = True
    return valid
        
def checktle(tlefile):
    valid = True
    with open(tlefile) as file:
        line = file.readline()
        ii = 1
        while line and valid:
            valid = (int(line[0]) == ii) #checks that the first character in each line follows the 1,2 rule of tle files
            line = file.readline()

            ii = ii + 1
            if(ii > 2):
                ii = 1
    return valid

def checkthreele(tlefile):
    valid = True
    with open(tlefile) as file:
        line = file.readline()
        ii = 0
        while line and valid:
            valid = (int(line[0]) == ii) #checks that the first character in each line follows the 0,1,2 rule of 3le files
            line = file.readline()

            ii = ii + 1
            if(ii > 2):
                ii = 0
    return valid
