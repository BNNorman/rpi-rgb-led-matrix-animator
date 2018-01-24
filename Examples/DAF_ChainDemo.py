
'''

DAF_ChainDemo.py - used to run a DAF Logo chain animation on a LED panel


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

import sys
import traceback
import PathSetter

from LEDAnimator import ChainAnimations, Palette, Animator, AnimSequence, ImageAnimations
from LEDAnimator.Chain import *
import LEDAnimator.Panel as Panel

FPS=100 # frames per sec for the animation
DEBUG=False
if DEBUG:
    sys.stdout=sys.stderr   # unbuffered error messages

# my panel is 64x64 made up of two panels stacked on top of each other
# each panel is a single piece but is made of two 32x32 panels side by side
PANEL_ROWS=32       # each sub panel is 32 LED x 32
PANEL_SERIES=2      # 2 in series = 64 leds horizontal
PANEL_PARALLEL=2    # 2 in parallel = 64 leds vertical


Panel.init(rows=PANEL_ROWS, chain_length=PANEL_SERIES, parallel=PANEL_PARALLEL,  fps=FPS, videoCapture=False,
           videoName="DAF_ChainDemo.avi",debug=DEBUG)

# chain definitions for the logo
from DAF_Chain_Data import *


print("Initialising animation sequences. Please wait....")


# declare the animator instance and add the chains


print("Creating the Animator and adding animations")


Speed=0.1

# the first two sequences shows how to enable debugging and add an ID to the messages
DAF_D_SEQ= AnimSequence.AnimSequence([
    ChainAnimations.Sparkle(duration=3, speed=Speed, palette=Palette.RGB, fps=FPS,id="D_FadeIn",debug=DEBUG),
    ChainAnimations.WipeRight(duration= 3, speed=Speed, palette=Palette.RGB, fps=FPS,id="D_WipeRight",debug=DEBUG),
])

DAF_A_SEQ= AnimSequence.AnimSequence([
    ChainAnimations.WipeRight(duration=3, speed=Speed, palette=Palette.RGB, fps=FPS,id="A_WipeRight",debug=DEBUG),
    ChainAnimations.Sparkle(duration=3, speed=Speed, palette=Palette.RGB, fps=FPS,id="A_Sparkle",debug=DEBUG),
])

DAF_F_SEQ= AnimSequence.AnimSequence([
    ChainAnimations.Sparkle(duration=3, speed=Speed, palette=Palette.RGB, fps=FPS),
    ChainAnimations.FadeIn(duration=5, speed=0.5, palette=Palette.RGB, fps=FPS),
    ChainAnimations.WipeRight(duration=3, speed=Speed, palette=Palette.RGB, fps=FPS),
])

DAF_CROSS_SEQ= AnimSequence.AnimSequence([
    ChainAnimations.Sparkle(duration=5, speed=Speed, palette=Palette.XMAS, fps=FPS)
])

DAF_OUTERCIRCLE_SEQ= AnimSequence.AnimSequence([
    ChainAnimations.CometsRight(duration=5, speed=Speed, palette=Palette.BLUE, fps=FPS)
])

DAF_INNERCIRCLE_SEQ= AnimSequence.AnimSequence([
    ChainAnimations.CometsLeft(duration=5, speed=Speed, palette=Palette.GREEN, fps=FPS)
])

DAF_LEFTWING_SEQ= AnimSequence.AnimSequence([
    ChainAnimations.Collider(duration=5, speed=Speed, palette=Palette.RGB, fps=FPS)
])

DAF_RIGHTWING_SEQ= AnimSequence.AnimSequence([
    ChainAnimations.Collider(duration=5, speed=Speed, palette=Palette.RGB, fps=FPS)
])

background= AnimSequence.AnimSequence([
    ImageAnimations.Place(duration=5, speed=0.1, palette=Palette.RGB, fps=FPS, imagePath="../images/DAF_640_640.png")
])

# contruct the Animator objecct

A= Animator.Animator(fps=FPS,debug=True)

# first three show how to turn on debug and tag messages with ids
A.addAnimation(chain=Chain(DAF_D),seq=DAF_D_SEQ, id="DAF_D_SEQ",debug=DEBUG)
A.addAnimation(chain=Chain(DAF_A),seq=DAF_A_SEQ,id="DAF_A_SEQ",debug=DEBUG)
A.addAnimation(chain=Chain(DAF_F),seq=DAF_F_SEQ,id="DAF_F_SEQ",debug=DEBUG)

A.addAnimation(chain=Chain(DAF_LEFTWING),seq=DAF_LEFTWING_SEQ)
A.addAnimation(chain=Chain(DAF_RIGHTWING),seq=DAF_RIGHTWING_SEQ)
A.addAnimation(chain=Chain(DAF_CROSS),seq=DAF_CROSS_SEQ)
A.addAnimation(chain=Chain(DAF_OUTERCIRCLE),seq=DAF_OUTERCIRCLE_SEQ)
A.addAnimation(chain=Chain(DAF_INNERCIRCLE),seq=DAF_INNERCIRCLE_SEQ)



print("Animations have been created")
# the run method only returns on error


try:
    print("Running")
    A.run()
    exit(0)

except Exception as e:

    print ("*** exception:")
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback,limit=15, file=sys.stdout)

