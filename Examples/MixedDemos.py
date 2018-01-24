"""
MixedDemos.py - a combination of Chain, Image and Text animations running at the same time

Many of the animations can be created by changing the foreground image alpha values
to reveal or hide the background image

"""

# used to ensure LEDAnimator folder is included when this
# program is not in the LEDAnimator folder

# information only
import os
cwd=os.getcwd()
print "cwd=",cwd

print ("Starting, please wait...")

import sys
import traceback
import PathSetter

from Simulator.Exceptions import SimulatorWindowClosed

from LEDAnimator import ImageAnimations,TextAnimations,ChainAnimations,Palette,Font,Text,Chain
from LEDAnimator.Animator import Animator
import LEDAnimator.Panel as Panel
from LEDAnimator.AnimSequence import *
from LEDAnimator.Image import *
from LEDAnimator.Helpers.Chains import *

FPS=100 # frames per sec for the animation
DEBUG=False

if DEBUG:
    sys.stdout=sys.stderr   # unbuffered debugging

# my panel is 64x64 made up of two panels stacked on top of each otherizontal
PANEL_PARALLEL=2    # 2 in parallel = 64 leds v
# each panel is a single piece but is made of two 32x32 panels side by side
PANEL_ROWS=32       # each sub panel is 32 LED x 32
PANEL_SERIES=2      # 2 in series = 64 leds horizontal


# The panel must be initialised first as it provides width and height info for the animations
# LEDSpacing and LEDSize determine the on-screen size of the simulator window (if used)
Panel.init(rows=PANEL_ROWS, chain_length=PANEL_SERIES, parallel=PANEL_PARALLEL, fps=FPS,
           debug=DEBUG, videoCapture=False, videoName="./MixedDemo.avi")

####################
# Image animations

theMatrix=Image(imagePath="../Images/TheMatrix.jpg",scaleMode="F",alignMode=("C","C"))

IMAGE_SEQ= AnimSequence([
    ImageAnimations.TheMatrix(duration=10, startPause=2, speed=0.5, fps=FPS, fgImage=theMatrix),
])

####################
# TextAnimations

bdfText="Hello sweetie BDF 12pt text here!"
bdf=Font.Font("BDF",12)
tLenBDF,h=bdf.getTextBbox(bdfText)

bdfmsg=Text.Text(text=bdfText, fontSize=12, fontFace="BDF", fgColor=Palette.XMAS,
            bgColor=Palette.LOTS)

TEXT_SEQ= AnimSequence([
    TextAnimations.Move (duration=20, speed=0.3, fps=FPS, startPos=(64,20), endPos=(-tLenBDF,20), text=bdfmsg,
                         multiColored=True, Xpos=32,Ypos=32,debug=DEBUG,id="BDFSEQ"),
])

####################
# ChainAnimations
COLLIDER= AnimSequence([
    ChainAnimations.Collider(duration=10, speed=0.1, palette=Palette.XMAS, fps=FPS),
])



# create the animator object
A= Animator(debug=DEBUG,fps=FPS)
# add the sequences the order is bottom layer to top layer
A.addAnimation(seq=IMAGE_SEQ)
A.addAnimation(seq=TEXT_SEQ)
A.addAnimation(chain=Chain.Chain(makeLine(0,2,63,2)),seq=COLLIDER)

# run the animation
try:
    print("Running")
    A.run() # no return from here

except SimulatorWindowClosed:
    print "Simulator window closed."

except Exception as e:

    print ("*** exception:")
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback,limit=10, file=sys.stdout)

exit(0)


