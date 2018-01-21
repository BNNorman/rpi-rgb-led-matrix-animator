"""
ImageDemos.py - cycle through image animations

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
from Simulator.Exceptions import SimulatorWindowClosed

from LEDAnimator import ImageAnimations
from LEDAnimator.Animator import Animator
import LEDAnimator.Panel as Panel
from LEDAnimator.AnimSequence import *
from LEDAnimator.Image import *

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
Panel.init(rows=PANEL_ROWS, chain_len=PANEL_SERIES, parallel=PANEL_PARALLEL, fps=FPS,
           debug=DEBUG, videoCapture=True, videoName="./ImageDemo.avi")

# Images used - not loaded till required
tulip=Image(imagePath="../Images/tulips.jpg",scaleMode="H",alignMode=("C","C"))
theMatrix=Image(imagePath="../Images/TheMatrix.jpg",scaleMode="F",alignMode=("C","C"))
daf4=Image(imagePath="../Images/DAF4.jpg",scaleMode="F",alignMode=("C","C"))
daf640=Image(imagePath="../Images/DAF_640_640.png",scaleMode="F",alignMode=("C","C"),loadVisible=False)
scania=Image(imagePath="../Images/SCANIA_2a.jpg",scaleMode="F",alignMode=("C","C"))
volvo=Image(imagePath="../Images/VOLVO5.jpg",scaleMode="F",alignMode=("C","C"))
vw=Image(imagePath="../Images/VW2.jpg",scaleMode="F",alignMode=("C","C"))
merc=Image(imagePath="../Images/MERC_b.jpg",scaleMode="F",alignMode=("C","C"))
foden=Image(imagePath="../Images/Foden.jpg",scaleMode="F",alignMode=("C","C"))
ford=Image(imagePath="../Images/FORD_1a.png",scaleMode="F",alignMode=("C","C"))
man=Image(imagePath="../Images/MAN_b.jpg",scaleMode="F",alignMode=("C","C"))

# the animation sequence
# there can be more than one sequence running in parallel


SEQ1= AnimSequence([
    #ImageAnimations.Place(duration=3, speed=0.5, fps=FPS, fgImage=theMatrix, bgImage=tulip),
    ImageAnimations.TheMatrix(duration=10, startPause=2, speed=0.5, fps=FPS, fgImage=theMatrix),
    ImageAnimations.TheMatrix(duration=15, speed=0.5, fps=FPS, fgImage=daf4),
    ImageAnimations.SatCycle(duration=05, satChange=-5, speed=1.0, fps=FPS, fgImage=tulip),
    ImageAnimations.HueCycle(duration=3, hueChange=2, speed=2, fps=FPS, fgImage=scania),
    ImageAnimations.BlurOut(duration=10, startPause=1, maxBlur=2, blurStep=0.05, fps=FPS, speed=0.5, fgImage=volvo),
    ImageAnimations.ExpandIn(duration=8, speed=0.1, fps=FPS, fgImage=daf4, bgImage=vw),
    ImageAnimations.ExpandOut(duration=8, speed=0.1, fps=FPS, fgImage=merc, bgImage=foden),
    ImageAnimations.CollapseIn(duration=8, speed=0.1, fps=FPS, fgImage=man, bgImage=vw),
    ImageAnimations.CollapseOut(duration=8, speed=0.1, fps=FPS, fgImage=scania, bgImage=foden),
    ImageAnimations.RevealIn (duration=5, speed=1.0, fps=FPS, fgImage=daf4, revealFrom="bottom"),
    ImageAnimations.RevealIn (duration=5, speed=1.0, fps=FPS, fgImage=man, revealFrom="Left"),
    ImageAnimations.RevealIn (duration=5, speed=1.0, fps=FPS, fgImage=merc, revealFrom="Right"),
    ImageAnimations.RevealIn (duration=5, speed=1.0, fps=FPS, fgImage=vw, revealFrom="Top"),
    ImageAnimations.Roll (duration=10, speed=1.0, fps=FPS, fgImage=vw, rollWindow=(10,10,44,34), rollSteps=20,
                          rollDirection="Up"),
    ImageAnimations.DissolveIn (duration=10, speed=5.0, fps=FPS, fgImage=daf4,bgImage=tulip, startPause=1,
     endPause=1),
    ImageAnimations.DissolveOut(duration=10, speed=2.0, fps=FPS, fgImage=tulip, bgImage=daf4, startPause=2,
                                endPause=2),
    ImageAnimations.BlurIn(duration=10, startPause=1, endPause=1,blurStep=0.05, speed=1.0, fps=FPS, fgImage=scania),
    ImageAnimations.FadeIn(duration=10, startPause=1, animLoops=True, speed=0.5, fps=FPS, fgImage=daf640,
     endPause=2,bgImage=scania),
    ImageAnimations.SlideAndZoom(duration=15, animLoops=False, startPos=(64, 64), endPos=(0, 0), zoom=(0.05,.25),
                                 fadeRate=2, speed=0.5, fps=FPS, fgImage=daf4),

])


# create the animator object
A= Animator(debug=DEBUG,fps=FPS)
# add the sequences the order is bottom layer to top layer
A.addAnimation(seq=SEQ1)  # bg images must be laid down first

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


