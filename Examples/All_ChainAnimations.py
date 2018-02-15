
'''

All_ChainAnimations.py

Dis-plays the chain animations available. For clarity the chains are straight lines


Copyright (C) 2017 Brian Norman, brian.n.norman@gmail.com

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

print ("Doing imports, please wait...")

# make sure that the HUB75 folder is on the sys.path
import PathSetter

import sys
import traceback

from LEDAnimator import ChainAnimations, Palette, Animator, AnimSequence
import LEDAnimator.Panel as Panel
import PathSetter


FPS=100 # frames per sec for the animation
DEBUG=False

if DEBUG:
    sys.stdout=sys.stderr

# my panel is 64x64 made up of two panels stacked on top of each other
# each panel is a single piece but is made of two 32x32 panels side by side
PANEL_ROWS=32       # each sub panel is 32 LED x 32
PANEL_COLS=32
PANEL_SERIES=2      # 2 in series = 64 leds horizontal
PANEL_PARALLEL=2    # 2 in parallel = 64 leds vertical

# must initialise the Panel first since some animations need the width and height
Panel.init(rows=PANEL_ROWS, cols=PANEL_COLS, chain_length=PANEL_SERIES, parallel=PANEL_PARALLEL, fps=FPS, \
                                                                                                 videoCapture=False,
           videoName="./All_ChainAnimations.avi",debug=DEBUG)


# animation sequences can be run on different chains

Speed=1


COLLIDER= AnimSequence.AnimSequence([
    ChainAnimations.Collider(duration=10, speed=0.1, palette=Palette.XMAS, fps=FPS),
])

FADE_IN= AnimSequence.AnimSequence([
    ChainAnimations.FadeIn(duration=5, speed=Speed, palette=Palette.RGB, fps=FPS),
])


WIPE_RIGHT= AnimSequence.AnimSequence([
    ChainAnimations.WipeRight(duration=5, speed=Speed, palette=Palette.RGB, fps=FPS),
])

WIPE_LEFT= AnimSequence.AnimSequence([
    ChainAnimations.WipeLeft(duration=5, speed=Speed, palette=Palette.LOTS, fps=FPS),
])

WIPE_IN= AnimSequence.AnimSequence([
    ChainAnimations.WipeIn(duration=5, speed=Speed, palette=Palette.RGB, fps=FPS),
])

WIPE_OUT= AnimSequence.AnimSequence([
    ChainAnimations.WipeOut(duration=5, speed=Speed, palette=Palette.XMAS, fps=FPS),
])

COMET_RIGHT= AnimSequence.AnimSequence([
    ChainAnimations.CometRight(duration=5, speed=Speed, palette=Palette.RGB, fps=FPS),
])

COMETS_LEFT= AnimSequence.AnimSequence([
    ChainAnimations.CometsLeft(duration=5, speed=Speed, palette=Palette.XMAS, fps=FPS),
])

SPARKLE= AnimSequence.AnimSequence([
    ChainAnimations.Sparkle(duration=5, speed=Speed, palette=Palette.RGB, fps=FPS),
])

LARSON= AnimSequence.AnimSequence([
    ChainAnimations.Larson(duration=5, speed=0.5, palette=Palette.XMAS, fps=FPS),
])

SPARKLE_RANDOM= AnimSequence.AnimSequence([
    ChainAnimations.SparkleRandom(duration=5, speed=Speed, palette=Palette.RGB, fps=FPS),
])

PULSE= AnimSequence.AnimSequence([
    ChainAnimations.Pulse(duration=5, speed=Speed, palette=Palette.RGB, fps=FPS),
])

ALTONOFF= AnimSequence.AnimSequence([
    ChainAnimations.AltOnOff(duration=5, speed=Speed, palette=Palette.XMAS, fps=FPS),
])

RED=AnimSequence.AnimSequence([
    ChainAnimations.Pulse(duration=5,speed=Speed, duty=75,palette=Palette.RED,fps=FPS),
])

GREEN=AnimSequence.AnimSequence([
    ChainAnimations.Pulse(duration=5,speed=Speed, duty=75,palette=Palette.GREEN,fps=FPS),
])

BLUE=AnimSequence.AnimSequence([
    ChainAnimations.Pulse(duration=5,speed=Speed, duty=75,palette=Palette.BLUE,fps=FPS),
])


# create the animator object
A= Animator.Animator(fps=FPS,debug=DEBUG)

# add the chains - horizonatl lines

from LEDAnimator.Helpers.Chains import *
from LEDAnimator.Chain import *

# add all the animations running at the same time

A.addAnimation(chain=Chain(makeLine(0,2,63,2)),seq=COLLIDER)
A.addAnimation(chain=Chain(makeLine(0,4,63,4)),seq=FADE_IN)
A.addAnimation(chain=Chain(makeLine(0,6,63,6)),seq=WIPE_RIGHT)
A.addAnimation(chain=Chain(makeLine(0,8,63,8)),seq=WIPE_LEFT)
A.addAnimation(chain=Chain(makeLine(0,10,63,10)),seq=WIPE_IN)
A.addAnimation(chain=Chain(makeLine(0,12,63,12)),seq=WIPE_OUT)
A.addAnimation(chain=Chain(makeLine(0,14,63,14)),seq=COMET_RIGHT)
A.addAnimation(chain=Chain(makeLine(0,16,63,16)),seq=COMETS_LEFT)
A.addAnimation(chain=Chain(makeLine(0,18,63,18)),seq=LARSON)
A.addAnimation(chain=Chain(makeLine(0,20,63,20)),seq=SPARKLE)
A.addAnimation(chain=Chain(makeLine(0,22,63,22)),seq=SPARKLE_RANDOM)
A.addAnimation(chain=Chain(makeLine(0,24,63,24)),seq=PULSE)
A.addAnimation(chain=Chain(makeLine(0,26,63,26)),seq=ALTONOFF)
A.addAnimation(chain=Chain(makeLine(0,48,63,48)),seq=RED)
A.addAnimation(chain=Chain(makeLine(0,49,63,49)),seq=GREEN)
A.addAnimation(chain=Chain(makeLine(0,50,63,50)),seq=BLUE)


print("Animations have been created")
# the run method only returns on error


try:
    print("Running")
    A.run()
    exit(0)

except Exception as e:

    print ("*** exception:")
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback,limit=10, file=sys.stdout)

