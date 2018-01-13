'''
TextChainMaker.py

Takes a string, a BDF font and a starting point XY  (upper left corner)
produces a chain for a non-text animation which can be used to drive the animator like this:-

myChain=[(x,y).....(xn,yn)] <- copy and paste the python string which this program outputs

A.addAnimation(chain=Chain(myChain),seq=Seq1)

The point of this is that ordinary Text animations animate the entire text without
being able to control individual pixels. Using this code you can create a message chain
and animate it.

Caveat. This code cannot determine the writing direction of the Glyph strokes it can only
scan the character bit pattern from top to bottom. For scrolling animations the result will look weird
however, for Sparkle it should look ok. Also, the ON animation will turn all the LEDs on as will Pulse and the fade
animations. So they should look ok.


'''
from LEDAnimator.BDF.Font import *
import numpy as np

###############################################################
# setup these values first
###############################################################
textMsg="Happy"    # the messages
X,Y=5,5                     # coordinates of top left corner

FONTSIZE=14


###############################################################
#
# Not a good idea to mess with code beyond here
#
###############################################################
f= Font(FONTSIZE)

coordList=[]

startX=X



for ch in textMsg:
    print "Processing",ch

    glyph = f.getChar(ch)   # black and white numpy image
    h,w=glyph.shape[:2]


    # scan each row of the bitmap
    for row in range(h):   # pt size
        for col in range(w):
            # Glyph shape is white, bg is Black
            r,g,b,a=glyph[row, col]

            if (r,g,b,a)==(255,255,255,255):
                coordList.append((col+X,row+Y))
    X=X+w

print("String length=",X-startX,"pixels/leds long.")
print("CHAIN=",coordList)