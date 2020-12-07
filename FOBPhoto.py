#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 21:12:45 2019

@author: stingay
"""

import numpy as np
from astropy.wcs import WCS
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import math
import ephem

# set up tests for orbiting objects

gatech=ephem.Observer()
gatech.lon='115.9033'
gatech.lat='-32.0525'
gatech.elevation=20

#tlefile=open('Test-FOB-data/tle-2019-11-16.txt')
#tlefile=open('Test-FOB-data/3le-2019-12-19-08-40-18.txt')
tlefile=open('Test-FOB-data/3le-2019-12-27-15-10-14.txt')
tle=tlefile.readlines()
tlel=len(tle)

# which frame are we looking at?
frame=97

# xcoords of detections
xhit=[3691,1185,1033,3265,3415]

# y coords of detections
yhit=[2635,1294,2445,2296,3063]

# detection frames
order=[97,99,102,103,106]

# ra/dec of dectections for detections around 15:16 UT
rac1=[42.91,43.94,44.03,44.87]
decc1=[2.86,2.94,1.84,1.78]

# ra/dec of detection around 15:06 UT
rac2=[38.39]
decc2=[1.57]

if frame in order:
    hitindex=order.index(frame)
    xcand=xhit[hitindex]
    ycand=yhit[hitindex]

############################################################################
# Test data

if (frame==97):
    hdul = fits.open('Test-FOB-data/0097-fast-slew-5-sec.fit')
    pos=27
    ctime='2019/11/16 15:06:08'
    w=WCS('Test-FOB-data/97-wcs.fits')

# 3691 2635 27 (location of candidate)
#
# Star locations and counts
#2253 1624 1063
#4772 2180 127
#4634 1568 129
#4640 1562 110
#4367 3297 80
#3775 1477 55
#1508 3339 51
#1298 1754 50
#3874 2207 38
#3493 2363 36
#2298 2738 36 (single detection)
#2148 353 30 (single detection)
#2390 628 29 (single detection)

#hdul = fits.open('Test-FOB-data/0098-fast-slew-5-sec.fit')

if (frame==99):
    hdul = fits.open('Test-FOB-data/0099-fast-slew-5-sec.fit')
    pos=4
    ctime='2019/11/16 15:16:10'
    w=WCS('Test-FOB-data/99-wcs.fits')

# 1185 1294 4 (location of candidate)
#
# Star locations and counts
#2907 3227 342.38015709315914
#2988 2268 300.12515709315903
#2550 1112 223.31015709315852
#5078 188 168.51015709315834
#756 1151 148.6051570931586
#3503 1069 98.85015709315849
#4998 550 89.93515709315852
#1991 633 51.915157093158996
#2649 966 51.51515709315845
#3269 255 46.75515709315914
#253 2686 46.51515709315845
#4252 3157 46.46015709315907
#3053 1562 43.06015709315852
#1052 1409 40.790157093158996
#923 3077 36.675157093159214
#3559 2852 36.89515709315856
#2084 1249 36.33015709315896
#4086 184 36.295157093159105
#4156 100 34.51515709315845
#224 913 28.540157093158996

#hdul = fits.open('Test-FOB-data/0100-fast-slew-5-sec.fit')

#hdul = fits.open('Test-FOB-data/0101-fast-slew-5-sec.fit')

if (frame==102):
    hdul = fits.open('Test-FOB-data/0102-fast-slew-5-sec.fit')
    pos=8
    ctime='2019/11/16 15:16:32'
    w=WCS('Test-FOB-data/102-wcs.fits')

# 1033 2445 8 (location of candidate)
#
# Star locations and counts
#2902 2292 370.17318833475656
#2983 1333 264.0831883347564
#2545 179 186.59818833475583
#750 230 126.0131883347558
#3187 3173 114.05818833475587
#3499 133 83.58818833475652
#4246 2235 49.22318833475583
#250 1752 42.33818833475652
#920 2154 42.31318833475598
#1047 485 32.578188334756305
#3554 1942 31.408188334756233
#2079 340 29.86818833475627
#3050 648 29.218188334755723 (single detection)
#2644 100 29.098188334755832 (single detection)
#4343 477 28.328188334756305 (single detection)

if (frame==103):
    hdul = fits.open('Test-FOB-data/0103-fast-slew-5-sec.fit')
    pos=9
    ctime='2019/11/16 15:16:39'
    w=WCS('Test-FOB-data/103-wcs.fits')

# 3265 2296 9 (location of candidate)
#
# Star locations and counts
#2901 2000 338.94024016859566
#2982 1040 263.2902401685951
#3185 2854 119.9652401685953
#248 1441 45.52024016859559
#918 1853 41.810240168595556
#4245 1957 38.870240168595046
#1044 172 35.45024016859497
#3048 337 32.98024016859563 (single detection)
#3553 1650 32.135240168595374

#hdul = fits.open('Test-FOB-data/0104-fast-slew-5-sec.fit')

#hdul = fits.open('Test-FOB-data/0105-fast-slew-5-sec.fit')

if (frame==106):
    hdul = fits.open('Test-FOB-data/0106-fast-slew-5-sec.fit')
    pos=12
    ctime='2019/11/16 15:17:00'
    w=WCS('Test-FOB-data/106-wcs.fits')

# 3415 3063 12 (location of candidate)
#
# Star locations and counts
#2896 1076 374
#2977 116 241
#3180 1944 143
#2720 2653 125 HD18509
#3681 3038 93
#242 544 46
#913 939 46
#4506 29 46 45
#4240 1020 41
#5078 3359 35 HD18582

#hdul = fits.open('Test-FOB-data/0107-fast-slew-5-sec.fit')

############################################################################
# Cosmic ray data
#
if (frame==11):
    hdul = fits.open('Test-FOB-data/IMG_11-final.fit')
    pos=23

if (frame==12):
    hdul = fits.open('Test-FOB-data/IMG_12-final.fit')
    pos=0

if (frame==13):
    hdul = fits.open('Test-FOB-data/IMG_13-final.fit')
    pos=0

if (frame==14):
    hdul = fits.open('Test-FOB-data/IMG_14-final.fit')
    pos=0

if (frame==15):
    hdul = fits.open('Test-FOB-data/IMG_15-final.fit')
    pos=0

if (frame==16):
    hdul = fits.open('Test-FOB-data/IMG_16-final.fit')
    pos=0

if (frame==17):
    hdul = fits.open('Test-FOB-data/IMG_17-final.fit')
    pos=0

if (frame==18):
    hdul = fits.open('Test-FOB-data/IMG_18-final.fit')
    pos=0

if (frame==19):
    hdul = fits.open('Test-FOB-data/IM_19-final.fit')
    pos=0

if (frame==20):
    hdul = fits.open('Test-FOB-data/IMG_20-final.fit')
    pos=0

############################################################################

hdul.info()
data=hdul[0].data

# do astrometry
astro=0

# do test for orbiting objects
orbit=0

# do plot of satellites in vicinity
satplot=0

# check astrometry and satellite positions
checksat=0

# plot photometry data
plotmag=0

# simulate image
simulate=0

# publication images
pub=1

# calculate magnitudes
calcmag=0

# check pixel location in another frame
checkpix=0

# check cosmic rays
checkray=0

# coordinates for NED search
ned=0

# plot slice
slicel=1

#r,d coordinates
rd=0

# SNR for detection in difference image
snr=10

# number of pixels on x axis
xpix=3461

# number of pixels on y axis
ypix=5190

# counts per detection (normalisation by eye)
norm=1.65e5
fhit=np.array([575,1673,1001,361,716])/norm
fhite=np.array([29,42,36,29,31])/norm
fhitp=fhit+fhite
fhitn=fhit-fhite

# calculate magnitudes of candidates
if (calcmag==1):
    for count in fhitp:
        calcc=-2.5*math.log10(count)
        print(calcc)

    for count in fhit:
        calcc=-2.5*math.log10(count)
        print(calcc)

    for count in fhitn:
        calcc=-2.5*math.log10(count)
        print(calcc)

# photometry
stars=["HD18509","HD18582","HD18368","HD18216","HD18012","HD18682","HD18204","HD15694","HD17791","HD17779","HD17780","BD+01 501","HD17690","HD17616","HD15821","HD15820","HD15845"]
vmags=np.array([7.55,7.78,7.61,6.583,6.74,7.78,8.44,5.269,6.95,7.37,7.96,9.42,7.64,6.83,7.75,8.88,8.87])
counts=np.array([122.21,93.95,162.42,390.00,290.61,92,97,1256,219,158,94,111,125,220,163,100,77])
errcounts=3*np.array([27.42,26.90,27.38,28.94,27.32,27,27,37,28,28,28,27,27,27,28,28,28])

# calculate expected V magnitude
vmagc=np.array(range(50,100,1))/10
ymag=1.65*10**(5-vmagc/2.5)

# plot known V magnitudes and measured counts against expected
if (plotmag==1):
    plt.figure(figsize=(5,5))
    plt.scatter(vmags,counts)
    plt.plot(vmagc,ymag)
    plt.errorbar(vmags,counts,errcounts,linestyle="None")
    plt.xlabel("V magnitude")
    plt.ylabel("Peak pixel value")
    ##plt.savefig("photometry.pdf")

if (rd==1):
    # get ra and dec for candidate
    r, d = w.all_pix2world(xcand, ycand, 0)
    print(r,d)

# print list of coordinates for NED search
if (ned==1):
    for ri in range(0,354,2):
        print(r+ri/54000,d)
        print(r-ri/54000,d)

# test for proximity of orbiting objects
if (orbit==1):
    date=ephem.Date(ctime)
    for dt in range(-10,10):
        gatech.date=date+dt/86400
        print(dt,gatech.date)
#        for tlei in range(0,tlel-1,3):
        for tlei in range(0,tlel-1,2):
            try:
#                sat=ephem.readtle(tle[tlei],tle[tlei+1],tle[tlei+2])
                sat=ephem.readtle("junk",tle[tlei],tle[tlei+1])
                sat.compute(gatech)
                satra=math.degrees(float(repr(ephem.degrees(sat.ra))))
                satdec=math.degrees(float(repr(ephem.degrees(sat.dec))))
                if (abs(r-satra)<1 and abs(d-satdec)<1):
                    print(tlel,tlei,tle[tlei],tle[tlei+1],tle[tlei+2])
                    dist=math.sqrt(abs(r-satra)**2+abs(d-satdec)**2)
                    print(r,satra,d,satdec,dist)
            except:
                print('Exception detected')

# make plot of satellites in the vicinity
if (satplot==1):
    satr=[]
    satd=[]
    stime1='2019/11/16 15:16:30'
    stime2='2019/11/16 15:06:00'
#    refr=38
    refr=41
    refd=2
    date=ephem.Date(stime1)
    for dt in range(-60,60):
        gatech.date=date+dt/86400
#        for tlei in range(0,tlel-1,3):
        for tlei in range(0,tlel-1,2):
            try:
                sat=ephem.readtle(tle[tlei],tle[tlei+1],tle[tlei+2])
#                sat=ephem.readtle("junk",tle[tlei],tle[tlei+1])
                sat.compute(gatech)
                satra=math.degrees(float(repr(ephem.degrees(sat.ra))))
                satdec=math.degrees(float(repr(ephem.degrees(sat.dec))))
                if (abs(refr-satra)<10 and abs(refd-satdec)<10):
                    dist=math.sqrt(abs(r-satra)**2+abs(d-satdec)**2)
                    satr.append(satra)
                    satd.append(satdec)
            except:
                print('Exception detected - probably faultly TLE')

    plt.figure(figsize=(5,5))
    plt.scatter(satr,satd)
    plt.scatter(rac1,decc1)
    plt.xlim(44-5,44+5)
    plt.ylim(refd-5,refd+5)
    plt.xlabel("RA (deg)")
    plt.ylabel("Dec (deg)")
    ##plt.savefig("satellites.pdf")

# check astrometry and satellite positions
if (checksat==1):
    xcheck=[]
    ycheck=[]
    ncheck=[]
#   to match 75 mm image
    hdulcheck = fits.open('Test-FOB-data/satellites.fit')
    wcheck=WCS('Test-FOB-data/wcs-cz-3-stage-3.fits')
#   to match 500 mm image
#    hdulcheck = fits.open('Test-FOB-data/500mm-sat.fit')
#    wcheck=WCS('Test-FOB-data/wcs-500mm.fits')
    datacheck=hdulcheck[0].data
    datacheck16=datacheck.astype(np.int16)
    meancheck=np.mean(datacheck16)

#   exposure time (matches cz-3: 20559), 75 mm image
    ctimecheck='2019/12/27 13:37:42'
#   to match other satellite, 75 mm image
#    ctimecheck='2019/12/27 13:38:15'
#   to match 500 mm image
#    ctimecheck='2019/12/27 12:19:34'
    gacheck=ephem.Observer()
    gacheck.lon='115.9033'
    gacheck.lat='-32.0525'
    gacheck.elevation=28
    datecheck=ephem.Date(ctimecheck)

#   to match 75 mm image
    refrcheck=99.728
    refdcheck=-21.682
#   to match 500 mm image
#    refrcheck=95.111
#    refdcheck=-53.655

#   to match 75 mm image
    siriusr=101.2875
    siriusdec=-16.7161
    xsir,ysir=wcheck.all_world2pix(siriusr, siriusdec, 0)
    xcheck.append(xsir)
    ycheck.append(ysir)
    ncheck.append('Sirius')
#   to match 500 mm image
#    canopusr=95.9875
#    canopusdec=-52.6955
#    xcan,ycan=wcheck.all_world2pix(canopusr, canopusdec, 0)
#    xcheck.append(xcan)
#    ycheck.append(ycan)
#    ncheck.append('Canopus')
    for dtcheck in range(0,5):
        gacheck.date=datecheck+dtcheck/86400
        for tlei in range(0,tlel-1,3):
            try:
                sat=ephem.readtle(tle[tlei],tle[tlei+1],tle[tlei+2])
                sat.compute(gacheck)
                satra=math.degrees(float(repr(ephem.degrees(sat.ra))))
                satdec=math.degrees(float(repr(ephem.degrees(sat.dec))))
                xcoord, ycoord = wcheck.all_world2pix(satra, satdec, 0)
                if (xcoord>0 and xcoord<5190 and ycoord>0 and ycoord<3461):
                    xcheck.append(xcoord)
                    ycheck.append(ycoord)
                    str1=tle[tlei].strip('\n')
                    str2=str1.strip('0 ')
                    if (dtcheck==0):
                        ncheck.append(str2)
            except:
                print('Exception detected - probably faultly TLE')

    plt.figure(figsize=(10,10))
    plt.imshow(datacheck16,clim=(6270,7000))
    plt.scatter(xcheck,ycheck,color='r',s=9)
    plt.xlim(0,5190)
    plt.ylim(3461,0)
    for i, txt in enumerate(ncheck):
        plt.annotate(txt, (xcheck[i]-500, ycheck[i]-100),color='w',fontsize='large',fontweight='bold')
#   to match 75 mm image
    plt.gca().add_patch(Rectangle((2300,400),500,500,linewidth=2,edgecolor='r',facecolor='none'))
    plt.gca().add_patch(Rectangle((2000,2100),500,500,linewidth=2,edgecolor='r',facecolor='none'))
    plt.xlabel("Pixel number")
    plt.ylabel("Pixel number")
#   to match 75 mm image
    ##plt.savefig("check-sat.pdf",bbox_inches='tight')
#   to match 500 mm image
#    ##plt.savefig("check-sat-500mm.pdf",bbox_inches='tight')

# convert to int16 and calculate image mean and std
data16=data.astype(np.int16)
meandata=np.mean(data16)
low=meandata-100
high=meandata+100
stddata=np.std(data16)
print("Image mean and standard deviation =",meandata,stddata)

# do astrometry via matched filter
mi=[]
mj=[]
if (astro==1):
    mij=np.empty((3461,5190),dtype=float)
    for i in range(100,3360):
        for j in range(0,5189):
            match=np.mean(data16[i-100:i+100,j])-meandata
            if (match>stddata):
                mij[i][j]=match

    for j in range(0,5189):
        imax=np.argmax(mij[:,j])
        if (mij[imax][j]>0):
            print(j,imax,mij[imax][j])
            mj.append(j)
            mi.append(imax)

# calculate and plot simulated image with noise
if (simulate==1):
    sim=np.random.normal(meandata,stddata,(xpix,ypix))
    simdiff=np.diff(sim,axis=0)
    simmean=np.mean(simdiff)
    simstd=np.std(simdiff)
    print("Residual simulated image mean and std =",simmean, simstd)
    simgt=np.nonzero(simdiff>snr*simstd)
    simlt=np.nonzero(simdiff<-1*snr*simstd)

    plt.figure(figsize=(15,10))
    imgplot=plt.imshow(sim,clim=(low,high))
    plt.colorbar()

    plt.figure(figsize=(15,10))
    imgplot=plt.imshow(simdiff,clim=(-1*simstd,simstd))
    plt.plot(simlt[1],simlt[0]+25,'bo')
    plt.plot(simgt[1],simgt[0],'ro')
    plt.colorbar()
    ##plt.savefig("sim.pdf")

# calculate slice along x axis to measure star pixel values

# yl is the y axis value for a star trail, xl is the x axis location centre to plot
yl=3050
xl=3670

# width of box to plot
wid=50

sl=xl-wid
sh=xl+wid

# get slice through star
slice=data16[yl,:]
meanslice=np.mean(slice)
stdslice=np.std(slice)
maxslice=np.max(slice[sl:sh])
pixv=maxslice-meanslice
print("Star slice mean, standard deviation, max, and pixel above mean =",meanslice,stdslice,maxslice,pixv)

# plot slice through star
if (slicel==1):
    plt.figure(figsize=(12,10))
    plt.title("slice containing stars")
    plt.xlabel("Pixel number")
    plt.ylabel("Pixel value")
    plt.plot(range(sl,sh),slice[sl:sh])
    #plt.savefig("slice.pdf")

# form difference image
diff=np.diff(data16,axis=0)
diffmean=np.mean(diff)
diffstd=np.std(diff)
print("Residual image mean and standard deviation =",diffmean, diffstd)

# detect hits above snr limit
gt=np.nonzero(diff>snr*diffstd)
lt=np.nonzero(diff<-1*snr*diffstd)

# plot image and astrometry
plt.figure(figsize=(15,10))
imgplot=plt.imshow(data16,clim=(low,high))
plt.plot([0,len(slice)-1],[yl,yl])
plt.scatter(mj,mi)
plt.gca().add_patch(Rectangle((gt[1][pos]-wid,gt[0][pos]-wid),2*wid,2*wid,linewidth=2,edgecolor='r',facecolor='none'))
plt.xlabel("Pixel number")
plt.ylabel("Pixel number")
plt.colorbar()
#plt.savefig("test.pdf")

# plot difference image, hits for this frame, and list of candidates
plt.figure(figsize=(15,10))
imgplot=plt.imshow(diff,clim=(-1*stddata,stddata))
plt.gca().add_patch(Rectangle((gt[1][pos]-wid,gt[0][pos]-wid),2*wid,2*wid,linewidth=2,edgecolor='r',facecolor='none'))
plt.plot(lt[1],lt[0]+25,'bo')
plt.plot(gt[1],gt[0],'ro')
if (checkray==0):
    plt.plot(xhit,yhit,'wo')
    for i, txt in enumerate(order):
        plt.annotate(txt, (xhit[i], yhit[i]),color='w',fontsize='large',fontweight='bold')
plt.xlabel("Pixel number")
plt.ylabel("Pixel number")
plt.colorbar()
##plt.savefig("difference-image-signals.pdf")

# publication image plots
if (pub==1):
    example_image = plt.figure()
    imgplot=plt.imshow(data16,clim=(low,high))
    plt.xlabel("Pixel number")
    plt.ylabel("Pixel number")
    plt.colorbar()
    #plt.savefig("example-image.pdf")

    plt.figure(figsize=(15,10))
    imgplot=plt.imshow(diff,clim=(-1*stddata,stddata))
    for i, txt in enumerate(order):
        plt.annotate(txt, (xhit[i], yhit[i]),color='w',fontsize='large',fontweight='bold')
    plt.gca().add_patch(Rectangle((gt[1][pos]-wid,gt[0][pos]-wid),2*wid,2*wid,linewidth=2,edgecolor='r',facecolor='none'))
    plt.plot(lt[1],lt[0]+5,'bo')
    plt.plot(gt[1],gt[0],'ro')
    plt.plot(xhit,yhit,'wo')
    plt.xlabel("Pixel number")
    plt.ylabel("Pixel number")
    plt.colorbar()
    #plt.savefig("difference-image-signals.pdf")

def newImage(self, cmin, cmax):
    new_example_image = plt.figure()
    plt.imshow(data16,clim=(cmin,cmax))
    plt.xlabel("Pixel number")
    plt.ylabel("Pixel number")
    plt.colorbar()
    return new_example_image
    ##plt.savefig("example-image.pdf")

# find sub-image of difference image around candidate and plot it
if (checkray==0):
    candiff=diff[gt[0][pos]-wid:gt[0][pos]+wid,gt[1][pos]-wid:gt[1][pos]+wid]

    diff_zoom = plt.figure()
    plt.axis([0,2*wid,0,2*wid])
    imgplot=plt.imshow(candiff,clim=(-1*snr*stddata,snr*stddata))
    plt.xlabel("Pixel number")
    plt.ylabel("Pixel number")
    plt.colorbar()
    ##plt.savefig("diff-zoom.pdf")

# find sub-image of image around candidate and plot it, report the max
    candat=data[gt[0][pos]-wid:gt[0][pos]+wid,gt[1][pos]-wid:gt[1][pos]+wid]

    max=np.max(candat)
    meancand=np.mean(candat)
    maxmag=max-meancand
    stdcand=np.std(candat)
    print("Pixel value above mean, max, mean and standard deviation in candidate box =",maxmag,max,meancand,stdcand)
    print("position of candidate in residual =",gt[1][pos],gt[0][pos])

    image_zoom = plt.figure()
    plt.axis([0,2*wid,0,2*wid])
    imgplot=plt.imshow(candat,clim=(low,1.05*high))
    plt.xlabel("Pixel number")
    plt.ylabel("Pixel number")
    plt.colorbar()
    ##plt.savefig("image-zoom.pdf")

# check zoom at custom location
if (checkpix==1):
    fcheck=106

    if (fcheck==97):
        hdul = fits.open('Test-FOB-data/0097-fast-slew-5-sec.fit')

    if (fcheck==99):
        hdul = fits.open('Test-FOB-data/0099-fast-slew-5-sec.fit')

    if (fcheck==102):
        hdul = fits.open('Test-FOB-data/0102-fast-slew-5-sec.fit')

    if (fcheck==103):
        hdul = fits.open('Test-FOB-data/0103-fast-slew-5-sec.fit')

    if (fcheck==106):
        hdul = fits.open('Test-FOB-data/0106-fast-slew-5-sec.fit')

    datac=hdul[0].data

    candc=datac[gt[0][pos]-wid:gt[0][pos]+wid,gt[1][pos]-wid:gt[1][pos]+wid]

    plt.figure()
    plt.axis([0,2*wid,0,2*wid])
    imgplot=plt.imshow(candc,clim=(low,1.05*high))
    plt.xlabel("Pixel number")
    plt.ylabel("Pixel number")
    plt.colorbar()
    ##plt.savefig("check-zoom.pdf")
