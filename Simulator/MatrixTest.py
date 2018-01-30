"""
MatrixTest.py (simulator)

The RGBMatrix only displays images
Pixel animations are done by the Panel writing to an image which is
then sent to display.

On my Dell Inspiron quad core Q8200 2.33Ghz using a 64x64 image took 0.021850 seconds
to write the image into the frame buffer - that (sadly) equates to a potential maximum 50 frames per second
"""
from Simulator.RGBMatrix import *
from LEDAnimator.NumpyImage import *
import time

# the small red box is 64x64 - that matches my test panel
# so this will indicate how quickly I can send output to the
# simulator matrix Panel
img=NumpyImage(imagePath="../Images/SmallRedBox.png")

mat=RGBMatrix(rows=32, chain_len=2, parallel=2)


def imageTest(im):
    t0=time.clock()
    mat.SetImage(im.out) # always drawn top left
    t1=time.clock()

    print "Image display took %.6f" % (t1-t0)


while not mat.IsRunning():
    print "Waiting for RGBMatrix"

imageTest(img)

while mat.running:
    pass