"""
Constants.py

Various things.

"""

import cv2
import os
#from UtilLib import *

# change these to get the correct white balance with your LED panel
# strictly this needs to be done on a pixel by pixel or panel by panel basis
# due to variations in manufacture
# blue and green leds are normally brighter than red so we lower them
# as starting point white=  1 unit of blue + two units of red plus + four units of green LEDs.
# which translated to these ratios :-
#redAdjust=1.0
#greenAdjust=0.25
#blueAdjust=0.5

# my panel adjustment
# used in Panel.py when the frameBuffer is being sent to the RGBMatrix
redAdjust=1.0
greenAdjust=0.8
blueAdjust=0.5

# image channels in numpy arrays
HLS_H=0
HLS_S=2
HLS_L=1

# HSV is used by Chain to make brightness adjustments easier
HSV_H=0
HSV_S=1
HSV_V=2

# you probably need to
RGB_R=2
RGB_G=1
RGB_B=0

ALPHA=3
ALIAS=4 # used by chains

# used by Font to handle font types differently
BDF_FONTTYPE=0
HERSHEY_FONTTYPE=1
TRUETYPE_FONTTYPE=2
OPENTYPE_FONTTYPE=3
UNKNOWN_FONTTYPE=4


# conversion routines based on rgb order
PIXEL2HLS=cv2.COLOR_BGR2HLS if RGB_R==2 else cv2.COLOR_RGB2HLS
HLS2PIXEL=cv2.COLOR_HLS2BGR if RGB_R==2 else cv2.COLOR_HLS2RGB
PIXEL2HSV=cv2.COLOR_BGR2HSV if RGB_R==2 else cv2.COLOR_RGB2HSV
HSV2PIXEL=cv2.COLOR_HSV2BGR if RGB_R==2 else cv2.COLOR_HSV2RGB

# Hershey fonts render at this size for fontScale=1.0
HERSHEY_FONTSIZE=22.0   # must be float

# open cv version differ in their constant definition
# if you have problems replace the definitions with the numbers following the hash
FONT_HERSHEY_SIMPLEX=cv2.FONT_HERSHEY_SIMPLEX   #0
FONT_HERSHEY_PLAIN=cv2.FONT_HERSHEY_PLAIN       #1
FONT_HERSHEY_DUPLEX=cv2.FONT_HERSHEY_DUPLEX     #2
FONT_HERSHEY_COMPLEX=cv2.FONT_HERSHEY_COMPLEX   #3
FONT_HERSHEY_TRIPLEX=cv2.FONT_HERSHEY_TRIPLEX   #4
FONT_HERSHEY_COMPLEX_SMALL =cv2.FONT_HERSHEY_COMPLEX_SMALL  #5
FONT_HERSHEY_SCRIPT_SIMPLEX=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX #6
FONT_HERSHEY_SCRIPT_COMPLEX=cv2.FONT_HERSHEY_SCRIPT_COMPLEX #7
FONT_ITALIC = cv2.FONT_ITALIC   #16
# opencv line types

LINE_AA=cv2.LINE_AA # 16
LINE_8=cv2.LINE_8   #8
LINE_4=cv2.LINE_4   #4
FILLED=cv2.FILLED   #-1

# parameters for imread
IMREAD_UNCHANGED=cv2.IMREAD_UNCHANGED   #-1
IMREAD_GRAYSCALE=cv2.IMREAD_GRAYSCALE   #0
IMREAD_COLOR=cv2.IMREAD_COLOR           #1



#BDF font folder location
#Fonts folder is outside the LEDAnimator folder

parent = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
BDF_FONTLOC=os.path.join(parent,"Fonts")

assert os.path.isdir(BDF_FONTLOC),"Constants.py: BDF fonts expected to be at "+BDF_FONTLOC

# BDF by name
BDF_GOHU14="gohufont-14.bdf"
BDF_HELVR12="helvR12.bdf"
BDF_TOMTHUMB="tom-thumb.bdf"

# BDF by size - allows code to select the nearest font
# point sizes are ASCENT sizes to be compatible with openCV

BDF_FONT={}
BDF_FONT[5]="4x6.bdf"       # ascent 5
BDF_FONT[6]="5x7.bdf"       # ascent 6
BDF_FONT[7]="6x9.bdf"       # ascent 7
BDF_FONT[8]="6x10.bdf"      # ascent 8
BDF_FONT[9]="cIR6x12.bdf"   # ascent 9
BDF_FONT[10]="6x12.bdf"     # ascent 10
BDF_FONT[11]="7x13.bdf"     # ascent 11
BDF_FONT[12]="7x14.bdf"     # ascent 12
BDF_FONT[13]="9x18.bdf"     # no 13
BDF_FONT[14]="9x18.bdf"     # ascent 14
BDF_FONT[15]="9x18.bdf"     # no 15
BDF_FONT[16]="10x20.bdf"    # ascent 16

BDF_BOLD={}
BDF_BOLD[11]="6x13B.bdf"
BDF_BOLD[12]="9x15B.bdf"
BDF_BOLD[14]="9x18B.bdf"

BDF_OBLIQUE={}
BDF_OBLIQUE[11]="9x13O.bdf"

# TODO find some bigger BDF fonts
# 16pt is the largest I found (without spending too long looking) consider using
# xmbdfed to create others

# quick check that fonts actually exist
if not os.path.isfile(os.path.join(BDF_FONTLOC,BDF_FONT[10])):
    print "Constants.py WARNING:",BDF_FONT[10],"not found at",BDF_FONTLOC
    print "This may be correct but is a simple check that the BDF fonts exist."
