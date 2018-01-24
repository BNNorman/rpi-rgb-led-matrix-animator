'''
ImageCache.py

Library used by all instances of NumpyImage

The cache must be shareable between instances of NumpyImage

Different animations may use the same image so the cache prevents excessive
memory usage and speeds

ImageCache does the following:-

1 checks the image loaded ok - aborts the program if not
2 if not simulating adjusts the RGB channels for the LED panel (not individual leds)
'''

import cv2
import os
import numpy as np
from LEDAnimator.ExceptionErrors import *
from LEDAnimator.Constants import *

# simple test to see if we are using the simulator or not
# if rgbmartrix imports we are running for real

try:
    import rgbmatrix
    simulating=False
except:
    simulating=True

#dictionary for the images
# usage: cache[imagePath]=numpy image
cache={}



def loadImage(imagePath):
    # if previously loaded get it from cache
    if imagePath in cache:
        # print "ImageCache.loadImage(): returning cached image."+imagePath
        return cache[imagePath]
    #else:
    #   print "cache contains ",cache.keys()

    # try to load the image and colour correct it
    try:
        f=open(imagePath)
        f.close()

    except Exception as e:
        print "ImageCache.loadImage(): Unable to locate image file - check path [%s] cwd=%s " % ( imagePath,os.getcwd())
        raise e

    # must include any Alpha channel so read unchanged
    # openCV reads in BGR order. See Constants.py
    srcBGR=cv2.imread(imagePath,cv2.IMREAD_UNCHANGED)

    if srcBGR is None:
        raise ImageLoadFailed

    if not srcBGR.data:
        raise NoImageData

    # change image color channel order to match output
    if RGB_R==0:
        cache[imagePath]=cv2.cvtColor(srcBGR,cv2.COLOR_BGR2RGB)
    else:
        cache[imagePath]=srcBGR

    # add an alpha channel if needed
    # always used for Fadein/out effects
    h, w, c = cache[imagePath].shape
    if c < 4:
        alpha = np.full([h, w, 1], 255, dtype=np.uint8)  # opaquee
        cache[imagePath] = np.concatenate((cache[imagePath], alpha), axis=2)

    return cache[imagePath]



