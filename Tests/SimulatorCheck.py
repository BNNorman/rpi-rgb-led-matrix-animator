"""

SimulatorCheck.py

Requested by user.

Uses Panel.py to display an image to ensure the simulator is working.

Should also run on the Pi and output to the real panel - don't forget to
set RGB_R and RGB_B in Constants.py when running on a Pi if color
matters. (You will probably have done that anyway.

"""

import PathSetter
import LEDAnimator.Panel as Panel
from LEDAnimator.NumpyImage import *


# my panel is 64x64 made up of two panels stacked on top of each other
# each panel is a single piece but is made of two 32x32 panels side by side
FPS=50
PANEL_ROWS=32       # each sub panel is 32 LED x 32
PANEL_SERIES=2      # 2 in series = 64 leds horizontal
PANEL_PARALLEL=2    # 2 in parallel = 64 leds vertical

# must initialise the Panel first since some animations need the width and height
Panel.init(rows=PANEL_ROWS, chain_length=PANEL_SERIES, parallel=PANEL_PARALLEL, fps=FPS, videoCapture=True,
           videoName="./PanelDemo.avi")


# first fill the display with an image
img=NumpyImage(imagePath="../Images/DAF4.jpg")
if img.width<>64 or img.height<>64:
    img.resizeFitToTarget(64,64)    # remember this panel is 64x64

# send the image to the display
Panel.DrawImage(1,1,img.getImageData())
Panel.UpdateDisplay()


# some simple pixel drawing
# this is NOT quick. The actual animations write to a numpy
# image first and use Panel.DrawImage() to update the display
# to display moving objects you need to clear the panel before
# redrawing. If using nested loops call Panel.UpdateDisplay() in
# the outer loop for improved speed

# swap image pixels around
for x in range(32):
    for y in range(32):
        # swap pixels
        a=Panel.GetPixel(x,y)
        b=Panel.GetPixel(x+32,y+32)
        Panel.DrawPixel(x,y,b)
        Panel.DrawPixel(x+32,y+32,a)
    Panel.UpdateDisplay()   # done in outer loop to imporve speed

import random
import time
for x in range(64):
    for y in range(64):
        t0=time.time()

        #we use rgba (or bgra) colors
        color=(random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255))
        Panel.DrawPixel(x,y,color)

    # must update the display each time
    # done in the outer loop to imporve speed
    Panel.UpdateDisplay()

    # wait a short time if you want to slow it down
    #while time.time()-t0<1:
    #    pass

