
'''

ChainDemo.py - used to run a DAF Logo chain animation on a LED panel


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

from LEDAnimator import ChainAnimations, Palette, Animator, AnimSequence, ImageAnimations
from LEDAnimator.Chain import *
import LEDAnimator.Panel as Panel
from LEDAnimator.Image import *

FPS=50 # frames per sec for the animation

# my panel is 64x64 made up of two panels stacked on top of each other
# each panel is a single piece but is made of two 32x32 panels side by side
PANEL_ROWS=32       # each sub panel is 32 LED x 32
PANEL_SERIES=2      # 2 in series = 64 leds horizontal
PANEL_PARALLEL=2    # 2 in parallel = 64 leds vertical

# must initialise the Panel first since some animations need the width and height
Panel.init(rows=PANEL_ROWS, chain_len=PANEL_SERIES, parallel=PANEL_PARALLEL, LEDspacing=5, LEDsize=3, fps=FPS, videoCapture=False)





# animation sequences can be run on different chains

Speed=0.1


DAF_D_SEQ= AnimSequence.AnimSequence([
    ChainAnimations.Collider(duration=5, speed=Speed, palette=Palette.RGB, fps=FPS),
    ChainAnimations.FadeIn(duration=5, speed=1, palette=Palette.RGB, fps=FPS),
    ChainAnimations.Wait(duration=6, speed=Speed, palette=Palette.RED, fps=FPS),
    ChainAnimations.WipeRight(duration= 10, speed=Speed, palette=Palette.RGB, fps=FPS)
])

DAF_A_SEQ= AnimSequence.AnimSequence([
    ChainAnimations.Wait(duration=3, speed=Speed, palette=Palette.RED, fps=FPS),
    ChainAnimations.FadeIn(duration=5, speed=Speed, palette=Palette.RGB, fps=FPS),
    ChainAnimations.Wait(duration=6, speed=Speed, palette=Palette.RED, fps=FPS),
    ChainAnimations.WipeRight(duration=10, speed=Speed, palette=Palette.RGB, fps=FPS)
])

DAF_F_SEQ= AnimSequence.AnimSequence([
    ChainAnimations.Wait(duration=6, speed=Speed, palette=Palette.RED, fps=FPS),
    ChainAnimations.FadeIn(duration=3, speed=Speed, palette=Palette.RGB, fps=FPS),
    ChainAnimations.Wait(duration=3, speed=Speed, palette=Palette.RED, fps=FPS),
    ChainAnimations.WipeRight(duration=10, speed=Speed, palette=Palette.RGB, fps=FPS)
])

DAF_CROSS_SEQ= AnimSequence.AnimSequence([
    ChainAnimations.Sparkle(duration=5, speed=Speed, palette=Palette.XMAS, fps=FPS)
])

DAF_OUTERRING_SEQ= AnimSequence.AnimSequence([
    ChainAnimations.CometsRight(duration=5, speed=Speed, palette=Palette.BLUE, fps=FPS)
])

DAF_INNERRING_SEQ= AnimSequence.AnimSequence([
    ChainAnimations.CometsLeft(duration=5, speed=Speed, palette=Palette.GREEN, fps=FPS)
])

DAF_LEFTWING_SEQ= AnimSequence.AnimSequence([
    ChainAnimations.Collider(duration=5, speed=Speed, palette=Palette.RGB, fps=FPS)
])

DAF_RIGHTWING_SEQ= AnimSequence.AnimSequence([
    ChainAnimations.Collider(duration=5, speed=Speed, palette=Palette.RGB, fps=FPS)
])

backdrop=Image(imagePath="../images/DAF_640_640.png",scaleMode="F",alignMode=("C","C"))

background= AnimSequence.AnimSequence([
    ImageAnimations.Wait(duration=10, speed=0.1, fps=FPS, bgImage=backdrop)
])

# chains for the logo

from DAF_Chain_Data import *

# create the animator and add the sequences

A= Animator.Animator(fps=FPS,debug=True)


A.addAnimation(seq=background)  # bg images must be laid down first
A.addAnimation(chain=Chain(DAF_D),seq=DAF_D_SEQ)
A.addAnimation(chain=Chain(DAF_A),seq=DAF_A_SEQ)
A.addAnimation(chain=Chain(DAF_F),seq=DAF_F_SEQ)
A.addAnimation(chain=Chain(DAF_LEFTWING),seq=DAF_LEFTWING_SEQ)
A.addAnimation(chain=Chain(DAF_RIGHTWING),seq=DAF_RIGHTWING_SEQ)
A.addAnimation(chain=Chain(DAF_CROSS),seq=DAF_CROSS_SEQ)
A.addAnimation(chain=Chain(DAF_OUTERCIRCLE),seq=DAF_OUTERRING_SEQ)
A.addAnimation(chain=Chain(DAF_INNERCIRCLE),seq=DAF_INNERRING_SEQ)



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

