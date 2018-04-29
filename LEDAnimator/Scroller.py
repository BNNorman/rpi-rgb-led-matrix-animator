"""
Scroller.py

Scrolling images/text can result in juddering because the general animation code cannot
achieve the scroll rates required to deliver smooth scrolling

This class backgrounds the scrolling to provide a tight update loop.
This should not be used with other animations

"""

import platform,sys
from LEDAnimator.ExceptionErrors import *
import time
import threading
import Panel

if platform.system()=="Windows":
    print "Running on Windows simulator"
    sys.stdout.flush()

    from Simulator.RGBMatrix import RGBMatrix
    from Simulator.RGBMatrixOptions import RGBMatrixOptions
    simulating=True
else:
    from rgbmatrix import RGBMatrix,RGBMatrixOptions
    simulating=False

###############################################################
#
# hzeller driver SetImage wants a PIL RGB image, so we need these
#
###############################################################
try:
    # works on windows (Anaconda) and maybe others
    # might work ok using Anaconda on Linux (Pi Raspbian)
    from PIL import ImageTk,Image
except:
    try:
        # PILcompat is underlined in PyCharm when developing
        # on Windows because it was moved and renamed on Rasbian Lite
        from PILcompat import ImageTk,Image
    except:
        raise MissingImageTk


class Scroller():

    Xpos=0
    Ypos=0
    xStep=0
    yStep=0
    duration=0
    loopDelay=0.005
    busy=False
    img=None

    def __init__(self,img,startPos,endPos,duration,matrixOptions):

        self.duration=duration
        self.img=img
        startX,startY=startPos
        endX,endY=endPos

        self.xStep=self.loopDelay*(endX-startX)/self.duration  # results in negative value moving left from startX
        self.yStep=self.loopDelay*(endY-startY)/self.duration

        # converting now reduces loop time
        #self.image=Image.fromarray(img).convert("RGB")
        self.start()


    def start(self):
        if self.busy: return

        t=threading.Thread(target=self._run)
        t.start()

    def _run(self):
        self.busy=True

        self.startTime=time.time()

        while self.busy:
            if time.time()-self.startTime>=self.duration:
                break

            self.Xpos=self.Xpos+self.xStep
            self.Ypos=self.Ypos+self.yStep

            Panel.DrawImage(self.Xpos,self.Ypos,self.img)

            # has no effect on speed
            time.sleep(self.loopDelay)

        self.busy=False



