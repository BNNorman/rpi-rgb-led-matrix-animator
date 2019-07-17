"""
Panel.py

This is a virtual RGB Matrix Panel library which routes image data either to the real RGB matrix
or through a simulator (which uses opencv to display the output).

Panel maintains a frameBuffer (video frame) which is written to by the animations and which is
sent off to the simulated or real matrix when swap is called (to signify the caller has finished)

The frameBuffer is a NumpyImage which allows the Panel to support, for example, Alpha channels
which the Hzeller drivers don't.

NOTE: sys.stdout.flush is used to prevent startuop messages being delayed


"""

import LEDAnimator.NumpyImage as ni
from LEDAnimator.ExceptionErrors import *
from LEDAnimator.UtilLib import pasteWithAlphaAt
from LEDAnimator.Colors import *
import sys

##############################################################
# are we simulating or running on the Raspberry Pi?
# try the actual hzeller imports first
#
# PyCharm underlines rgbmatrix below if developing the code
# on a Windows machine. It can be ignored.
##############################################################

import platform

if platform.system()=="Windows":
    print "Running on Windows simulator"
    sys.stdout.flush()

    from Simulator.RGBMatrix import RGBMatrix
    from Simulator.RGBMatrixOptions import RGBMatrixOptions
    simulating=True
else:
    from rgbmatrix import RGBMatrix,RGBMatrixOptions
    simulating=False


###############################################################
#
# hzeller driver SetImage wants a PIL RGB image, so we need these
#
###############################################################
try:
    # works on windows (Anaconda) and maybe others
    # might work ok using Anaconda on Linux (Pi Raspbian)
    from PIL import ImageTk,Image
except:
    try:
        # PILcompat is underlined in PyCharm when developing
        # on Windows because it was moved and renamed on Rasbian Lite
        from PILcompat import ImageTk,Image
    except:
        raise MissingImageTk

##########################################################################################
# define the default options for a 64x64 matrix comprising of two 64x32 panels in parallel
# each panel has two 32x32 sub-panels chained together
# these are passed in via init(rows=x, ...)
##########################################################################################
Options = RGBMatrixOptions()

# these are the default values in RGBMatrixOPtions so don't need specfying here
#Options.rows = 32           # 32 rows in each panel
#Options.cols = 32
#Options.parallel = 2        # two panels in parallel
#Options.chain_length = 2       # sub-panels per panel
#Options.gpio_slowdown = 2   # gets rid of flickering leds on my Pi3

# on Linux not doing this prevents access to images (files)
# after the RGBMatrix is created
Options.drop_privileges = False


###########################################################################
#
# The panel
#
# We write to the frameBuffer and send it to the Simulator or actual Matrix
#
# we are NOT using the HZeller canvas object
#
###########################################################################

matrix = None                           # the RGB matrix
canvas = None                           # not used by the simulator
frameBuffer=None                        # NumpyImage used to represent the current display
panelBgColor=Black.getPixelColor()     # panel background color opaque Black
width=0                                 # panel width in pixels
height=0                                # panel height in pixels

###################################################################
# some classes to help PyCharm know what parameters exist
#
# used for parameter collection and passing
###################################################################

class imageOptions(object):
    """
    used to gather image options from kwargs
    """
    Xpos=0
    Ypos=0
    image=None

####################################################################
#
# Main Panel library
#
####################################################################

def init(**kwargs):
    """
    init() must be called at the start of the program to create a Panel (matrix and canvas)
    :param kwargs: options for the matrix configuration
    :return: Nothing
    """
    global matrix,simulating,width,height,frameBuffer,canvas

    print "Panel.init() starting.."
    sys.stdout.flush()

    for key, value in kwargs.iteritems():
        # only accept valid RGBMatrix options
        if getattr(Options,key,None) is not None: setattr(Options,key,value)

    #create the matrix object
    matrix=RGBMatrix(options=Options)

    height=Options.rows*Options.parallel
    width=Options.rows*Options.chain_length

    print "Panel.init() creating frameBuffer width %d,height %d\n"% (width,height)
    sys.stdout.flush()

    frameBuffer=ni.NumpyImage(width=width,height=height)
    if not simulating:
        canvas=matrix.CreateFrameCanvas()

def CheckInit():
    """
    Checks if init has been called and if not aborts the program
    :return: Nothing
    """
    if matrix is None:
        raise PanelInitNotCalled

def UpdateDisplay():
    """
    copies the frameBuffer to the RGBMatrix and refreshes the visible display
    :return: nothing
    """
    global matrix,simulating,canvas

    CheckInit()

    # simulator and physical matrices behave differently here
    img=frameBuffer.getImageData()

    if simulating:
        # no matrix refresh needed here
        matrix.SetImage(img)
    else:
        img[RGB_R] = (img[RGB_R] * redAdjust)
        img[RGB_G] = (img[RGB_G] * greenAdjust)
        img[RGB_B] = (img[RGB_B] * blueAdjust)

        # note Constants.RGB_R & RGB_B will need to be set RGB_R=0 and RGB_B=2
        # to ensure RGB colours are in the correct order
        canvas.SetImage(Image.fromarray(img).convert("RGB"))
        canvas=matrix.SwapOnVSync(canvas)

def DrawImage(x,y,image):
    """
    Overwrites whatever is on the matrix in the region of the image.

    Respects alpha transparency.

    :param float x:   top left coord of image
    :param float y:   top left coord of image
    :param image: numpy image (ndarray) to draw
    :return None: frameBuffer is updated
    """

    global framebuffer

    CheckInit()

    # paste with Alpha converts X/y to nearest pixel
    pasteWithAlphaAt(frameBuffer.out,x,y,image)


def DrawPixel(x,y,color):
    """
    Set the pixels at X,Y . Intended for individual pixel drawing.
    If called after DrawImage - writes over the frameBuffer image.

    x/y will be rounded to nearest pixel.

    :param color: the color with channels in pixel order
    :param float x: the x-coordinate
    :param float y: the y-coordinate
    :return None: frameBuffer pixel is written
    """

    global frameBuffer,simulating

    CheckInit()

    frameBuffer.setPixel(x, y, color)

def DrawPixelsRandom(x,y):
    """
    Set the pixel at X,Y using random RGB values. Intended for individual pixel drawing.
    If called after DrawImage - writes over the frameBuffer image.
    :param x: pixel co-ord int or float (rounded to nearest int)
    :param y: pixel co-ord int or float (rounded to nearest int)
    :return: the pixels are drawn on the panel frame buffer
    """
    global frameBuffer,simulating

    CheckInit()

    # frameBuffer.setPixelRandom validates the parameters
    #print "Panel.DrawPixelsRandom(x,y) type x", type(x), "y", type(y)
    frameBuffer.setPixelRandom(x, y)

def GetPixel(x,y):
    """
    Get the pixel r,g,b values at X,Y from the frameBuffer.

    :param x: pixel co-ord int or float
    :param y: pixel co-ord int or float
    :return: color value of the pixel
    """

    global frameBuffer,simulating

    CheckInit()

    # Pixel X, Y values are rounded by the frameBuffer
    # and returned as numpy arrays so need to convert to tuple
    (a,b,c,d)=frameBuffer.getPixel(x, y)
    return (a,b,c,d)

def Clear():
    """
    Fill the frameBuffer with the current background color.
    :return: Nothing
    """
    global  panelBgColor
    frameBuffer.fill(panelBgColor)

def Fill(color):
    """
    fills the Panel with a spcified color without changing the current background color
    :param color: (r,g,b)
    :return: nothing
    """
    global frameBuffer
    CheckInit()
    frameBuffer.fill(color)

def SetBgColor(bg=Black.getPixelColor()):
    """
    set the default background color for the panel
    :param bg: tuple in pixel order
    :return: nothing
    """
    global panelBgColor

    panelBgColor=bg

def isRunning():
    """
    The simulated RGBMatrix uses a background thread to display the frameBuffer.
    The animator can use this to decide if the thread is still running and take
    appropriate action
    :return: True if the matrix is running otherwise False
    """
    global simulating,matrix

    # if the TSimulator window has closed we should stop
    if simulating: return matrix.IsRunning()

    # actual matrix will always be running
    return True

def nearestInt(x):
    if type(x) is int: return x
    return int(round(x,0))



