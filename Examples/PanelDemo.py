
'''

PanelDemo.py - used to showcase panel animations

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

from LEDAnimator import PanelAnimations, Palette, Animator, AnimSequence, ImageAnimations
from LEDAnimator.Chain import *
import LEDAnimator.Panel as Panel

FPS=100 # frames per sec for the animation

# my panel is 64x64 made up of two panels stacked on top of each other
# each panel is a single piece but is made of two 32x32 panels side by side
PANEL_ROWS=32       # each sub panel is 32 LED x 32
PANEL_SERIES=2      # 2 in series = 64 leds horizontal
PANEL_PARALLEL=2    # 2 in parallel = 64 leds vertical

# must initialise the Panel first since some animations need the width and height
Panel.init(rows=PANEL_ROWS, chain_len=PANEL_SERIES, parallel=PANEL_PARALLEL, fps=FPS, videoCapture=True,
           videoName="./PanelDemo {width}x{height}.avi")

print("Creating the Animator and adding animations")

Speed=0.1

SEQ= AnimSequence.AnimSequence([
    PanelAnimations.RandomRectangles(duration=5, speed=Speed, multiColored=True,palette=Palette.XMAS, fps=FPS ),
    PanelAnimations.RandomCircles(duration=5, speed=Speed, multiColored=True,palette=Palette.XMAS, fps=FPS ),
    PanelAnimations.RandomEllipses(duration=5, speed=Speed, multiColored=True,palette=Palette.XMAS, fps=FPS ),
    PanelAnimations.RandomSparkle(duration=5, speed=Speed, multiColored=True,palette=Palette.XMAS, fps=FPS ),
    PanelAnimations.PolyLines(duration=5, speed=Speed, multiColored=True,palette=Palette.XMAS, fps=FPS, points=[(0,0),(10,10),(20,10),(25,15),(32,32)]),
    PanelAnimations.Twinkle(duration=5, speed=Speed, multiColored=True, palette=Palette.XMAS, fps=FPS),
    PanelAnimations.Rainbow(duration=5, speed=Speed, multiColored=True, palette=Palette.XMAS, fps=FPS),
])


A= Animator.Animator(fps=FPS,debug=True)
A.addAnimation(seq=SEQ)


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

