
'''
TextDemo.py - cycle through DAF truck logos

'''

# information only
import os
cwd=os.getcwd()
print "cwd=",cwd

print ("Starting, please wait...")
import PathSetter
import sys
import traceback

from LEDAnimator import TextAnimations
from LEDAnimator.Animator import Animator
import LEDAnimator.Panel as Panel
from LEDAnimator.AnimSequence import AnimSequence
from LEDAnimator.UtilLib import *
from LEDAnimator.Font import *
import LEDAnimator.Palette as Palette
from LEDAnimator.Image import *
from LEDAnimator.Text import *


FPS=30 # frames per sec for the animation

# my panel is 64x64 made up of two panels stacked on top of each otherizontal
PANEL_PARALLEL=2    # 2 in parallel = 64 leds v
# each panel is a single piece but is made of two 32x32 panels side by side
PANEL_ROWS=32       # each sub panel is 32 LED x 32
PANEL_SERIES=2      # 2 in series = 64 leds horertical

# The panel must be initialised first
# params LEDspacing and LEDsize control the simulator window size
Panel.init(rows=PANEL_ROWS, chain_len=PANEL_SERIES, parallel=PANEL_PARALLEL, fps=FPS,
           debug=True,videoCapture=True,videoName="./TextDemo {width}x{height}.avi")


# the animation sequence
# there can be more than one sequence running in parallel

# get the bounding box so we can scroll right off the panel
cv2Text="Hello sweetie CV2 12pt text here!"
hershey=Font(FONT_HERSHEY_SIMPLEX,12)
tLenCV2,h=hershey.getTextBbox(cv2Text)

bdfText="Hello sweetie BDF 12pt text here!"
bdf=Font("BDF",12)
tLenBDF,h=bdf.getTextBbox(bdfText)

cv2msg=Text(text=cv2Text,fontSize=12,fontFace=FONT_HERSHEY_SIMPLEX,
                 fgColor=Palette.XMAS,bgColor=(125,0,125,255))

bdfmsg=Text(text=bdfText, fontSize=12, fontFace="BDF", fgColor=Palette.XMAS,
            bgColor=Palette.LOTS)


bdfSeq= AnimSequence([
    TextAnimations.Move (duration=20, speed=0.3, fps=FPS, startPos=(64,20), endPos=(-tLenBDF,20), text=bdfmsg,
                         multiColored=True, Xpos=32,Ypos=32),
])

cv2Seq= AnimSequence([
    TextAnimations.Move (duration=20, speed=0.3, fps=FPS, startPos=(64,40), endPos=(-tLenCV2,40),  multiColored=True,
                         text=cv2msg),
])

# create the animator object
A= Animator(debug=True,fps=FPS)
# add the sequences the order is bottom layer to top layer
A.addAnimation(seq=bdfSeq)  # bg images must be laid down first
A.addAnimation(seq=cv2Seq)

# run the animation
try:
    print("Running")
    A.run()
    exit(0)

except Exception as e:

    print ("*** exception:")
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback,limit=10, file=sys.stdout)

