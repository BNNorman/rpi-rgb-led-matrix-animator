"""
ImageAnimations.py

defines the Animation classes.

You would add your own animations here.

The AnimBase class loads and scales any images during reset() if not already loaded
"""



from ImageAnimBase import ImageAnimBase
import random
import Panel
import time
import cv2
from LEDAnimator.UtilLib import *
import math

######################################################
#
# The animations
#
######################################################

# PLACE just puts an image on the canvas at a given position (xpos,ypos)

class Place(ImageAnimBase):
    """
    Place an image on the Panel. If there's a background image it is placed
    first.

    If the foreground image has transparent parts the background image/color will show through

    """

    def step(self):
        # output the fg & bg image(s) to the panel
        self.refreshCanvas()

class Wait(Place):
    """
    Alternative name for Place
    """
    pass


###################################################
#
#  FADE
#
###################################################
class Fade(ImageAnimBase):
    """
    Fade a foreground image in/out by changing it's brightness and transparency

    By changing transparency at the same time as brightness the image will disappear rather than leaving a black hole.

    The animation must specify a foreground image and a fadeRate value. Positive values denote fade in, negative values
    cause a fade out.

    A foreground image is required.

    If no background image is specified the background will be whatever animation is playing on a lower layer.

    """

    fadePercent=0
    fadeIn=True
    fadeRate=1

    def step(self, chain=None):
        # speed control
        if self.isNotNextStep():
            # refreshCanvas can cause an image to appear before
            # it has been initialised - not good for fade in
            if not self.init: self.refreshCanvas()
            return

        # need to load the image initially but not every time
        if self.init:
            assert self.fgImage is not None,"You must supply a foreground image."
            self.fadePercent=0 if self.fadeIn else 100
            self.fgImage.fade(self.fadePercent)
            # finally
            self.init=False
            return

        # fade the image in or out
        self.fadePercent += self.fadeRate

        # clamp brightness at 0 or 100%
        if self.fadeRate>0 and self.fadePercent>100:
            # max reached
            self.fadePercent=100
            self.animationHasFinished()
        elif self.fadeRate<0 and self.fadePercent<0:
            # min reached
            self.fadePercent=0
            self.animationHasFinished()

        self.fgImage.fade(self.fadePercent)
        self.refreshCanvas()

class FadeOut(Fade):
    def __init__(self,**kwargs):
        super(FadeOut,self).__init__(**kwargs)
        if self.fadeRate>0: self.fadeRate=-self.fadeRate

class FadeIn(Fade):
    def __init__(self,**kwargs):
        super(Fade,self).__init__(**kwargs)
        if self.fadeRate<0: self.fadeRate=-self.fadeRate
        if self.fgImage is not None:
            self.fgImage.fade(0)    # start hidden

class HueCycle(ImageAnimBase):
    """
    Hue cycle adds an offset to the hue of a color and so changes it.

    You cannot just set an image's Hue to one value since that turns it into a solid
    colored rectangle

    Since Hue is a 360 degree value it is normally modulo 180 to keep it
    in the range of a uint8 integer. This means that with a step size of 1
    and an fps of 100 a full cycle will take just 2 seconds. Hence it has to
    be slowed right down within the animation. Setting speed to something
    like 0.01 at fps of 100 means the hue will change by 1 in 1 second hence a
    duration of 5 seconds would produce just 5 hue changes. If you get my meaning.

    To give a better result we use change values based on the duration such that
    the hue change is 180 over the period of the duration

    """
    # user supplied parameters
    hueChange=0
    hueAdjust=0
    hueGain=0

    def step(self, chain=None):
        # not used - speed is controlled by hueGain which is calculated
        #if self.isNotNextStep(): # speed control
        #    self.refreshCanvas()
        #    return

        if self.init:
            assert type(self.hueChange) is int or type(self.hueChange) is float,"hueChange must be a number."
            self.hueGain=self.speed*self.hueChange*((self.duration*self.fps)/180)
            self.init=False

        # change hue adjustment but keep within 0-180 degrees
        self.hueAdjust=(self.hueAdjust+self.hueGain)%180

        self.fgImage.adjustHue(int(self.hueAdjust))
        self.refreshCanvas()

class SatCycle(ImageAnimBase):
    """
    cycles through image color saturation
    """

    # user supplied parameter
    satChange=0

    def step(self, chain=None):
        # speed control
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        if self.init:
            assert type(self.satChange) is int or type(self.satChange) is float,"satChange parameter must be a number."
            self.init=False

        self.fgImage.adjustSat(self.satChange)
        self.refreshCanvas()

class SlideAndZoom(ImageAnimBase):
    """
    SlideAndZoom

    Moves the image from startPos(x,y) to endPos(x,y) meanwhile enlarging or shrinking
    according to zoom(start,end)

    If zoom=(1.0,1.0) the image just slides
    If the startPos and endPos are the same the image just enlarges or shrinks

    Zoom factors are floating point numbers 1.0=no zoom. You must know the size of your
    images and use an appropriate zoom factor

    Calculations are done using floating point. Actual image positions are rounded
    to nearest pixel when the canvas is refreshed.

    user supplied parameters :-

    startPos=(0.0,0.0)  # image starts at this position
    endPos=(0.0,0.0)    # image stops at this position
    zoom=(1.0,1.0)      # (start zoom,end zoom) default is no zoom

    """

    # user supplied parameters
    startPos=(0.0,0.0)  # image start position
    endPos=(0.0,0.0)    # image end position
    zoom=(1.0,1.0)      # no zoom

    # internal variables
    curZoom=1.0
    zoomRate=0.0
    xRate=0         # amount to adjust x position
    yRate=0         # ditto for y position

    def calcRates(self):
        # sliding
        x0,y0 = self.startPos
        x1,y1 = self.endPos

        xChange = x1-x0
        yChange = y1-y0
        # calc rate of change if speed=1.0 the animation receives
        # ticks at the FPS rate at speed=0.5 it's half that
        # make sure it's a float
        self.xRate = (float(self.speed) * xChange) / self.fps
        self.yRate = (float(self.speed) * yChange) / self.fps

        # zooming
        startZoom,endZoom=self.zoom
        zoomChange = endZoom-startZoom
        self.zoomRate = self.speed*float(zoomChange)/self.fps

        self.curZoom = startZoom

    def hasReachedEndPos(self):
        """
        Check to see if the top left coords are within the rectangle
        formed by startPos and endPos if so return False

        :return Bool: True if  current position is outside the rectangle
        """
        x0,y0 = self.startPos
        x1,y1 = self.endPos

        #check if Xpos,Xpos lies within the area startPos/endPos
        X,Y=self.fgImage.getPosition()
        return not insideRect(X,Y,x0,y0,x1,y1)

    def step(self, chain=None):
        # speed control
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        if self.init:

            x0, y0 = self.startPos

            assert type(x0) is int or type(x0) is float, "startPos X must be int or float."
            assert type(y0) is int or type(y0) is float, "startPos Y must be int or float."

            self.fgImage.setPosition((x0,y0))

            x1, y1 = self.endPos
            assert type(x1) is int or type(x1) is float, "endPos X must be int or float."
            assert type(y1) is int or type(y1) is float, "endPos Y must be int or float."

            self.calcRates()  # rate of zoom and movement
            self.fgImage.resizeByFactor(self.curZoom)

            self.refreshCanvas() # at Xpos,Ypos
            self.init=False
            return

        # check that we are within startPos and endPos
        if self.hasReachedEndPos():
            self.animationHasFinished()
            self.refreshCanvas()
            return

        # move to next position

        newX,newY=self.fgImage.getPosition()
        newX+=self.xRate
        newY+=self.yRate
        self.fgImage.setPosition((newX,newY))

        # zoom can take time so only do it if
        # necessary

        if self.zoomRate<>0:
            self.curZoom+=self.zoomRate
            self.fgImage.resizeByFactor(self.curZoom)

        self.refreshCanvas()

class Dissolve(ImageAnimBase):
    """
    Base class for dissolve in and dissolve out animations

    user supplied parameters:

    startPause  secs: time to wait before animation begins. Default 0.5s
    fgImage dict:   foreground i9mage to dissolve
    bgImage dict:   background image - overrides any background colour
    background colour:  Background colour to use if any, overruled by bgImage
    """

    dissolveIn=None
    pixelCount=0
    pixelsDone=0
    startPause=0.5  # how long to wait before the animation starts
    endPause=0.5

    LEDlist=[]
    lenList=0

    def reset(self,**kwargs):
        """
        Sets self.init and start transparency of the foreground image
        calls the base class reset() method.

        :param kwargs: animation parameters
        :return: nothing,
        """
        super(Dissolve, self).reset(**kwargs)

        # must be done here, before the screen is refreshed
        # otherwise you see the fgImage briefly before it is hidden
        alpha=0 if self.dissolveIn else 255
        self.fgImage.fillAlpha(alpha)

    def makeLEDlist(self):
        # only do this once
        if self.lenList>0:
            return

        w,h=self.fgImage.getSize()

        mx,my=0,0

        self.LEDlist=[]

        for x in range(w):
            for y in range(h):
                mx=max(mx,x)
                my=max(my,y)
                self.LEDlist.append((x, y))

        self.lenList=w*h

        random.shuffle(self.LEDlist)

    def step(self):
        # speed control
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        if self.init:
            # determine how many pixel swap loops are required per 'tick'
            # to dissolve the foreground image
            # this depends on speed and fps
            self.makeLEDlist()
            self.nextLED=0
            # we are not going to do all leds in one go
            self.loopCount=int(self.speed*self.lenList/self.fps)
            self.alpha=255 if self.dissolveIn else 0
            self.init = False
            return

        # loop through making foreground image pixels transparent or opaque
        for i in range(self.loopCount):

            if self.nextLED>=self.lenList:
                self.animationHasFinished()
                break

            x,y=self.LEDlist[self.nextLED]

            self.fgImage.setPixelAlpha(x,y,self.alpha)

            self.nextLED += 1

        self.refreshCanvas()

class DissolveIn(Dissolve):
    """
    DissolveIn - sub class of Dissolve

    Starts with foreground image invisible and gradually reveals.

    Animation duration must be long enough to allow it to complete.
    """
    dissolveIn=True

class DissolveOut(Dissolve):
    """
    DissolveOut - sub class of Dissolve

    Starts with foreground image visible and gradually hides it.

    Animation duration must be long enough to allow it to complete.
    """

    dissolveIn=False

class Roll(ImageAnimBase):
    """
    roll all or part (window) of the foreground image
    rolling can be left/right/up or down

    user supplied params:

    rollWindow      tuple (x,y,w,h) if None the whole image is rolled
    rollSteps       int - number of pixels to shift the image or window
    rollDirection   'up', 'down', 'left', or 'right'
    """

    rollWindow=None
    rollSteps=0
    rollDirection=None

    # used internally
    curRollPos=0
    rollRate=1

    def step(self, chain=None):
        # speed control
        if self.isNotNextStep() or self.rollDirection is None:
            self.refreshCanvas()
            return

        if self.init:
            self.curRollPos=0
            self.rollRate=1         #self.rollSteps/self.speed
            self.refreshCanvas()    #at current Xpos,Ypos
            self.init=False
            if self.rollWindow is None: # roll the whole image
                self.rollWindow=(0,0,self.fgImage.getWidth(),self.fgImage.getHeight())
            return

        # check if we have reached the end (does not loop)
        if self.curRollPos==self.rollSteps:
            self.refreshCanvas()
            return

        # roll the window
        self.fgImage.rollWindow(self.rollWindow,self.rollDirection, self.rollRate)
        self.refreshCanvas()

class Reveal(ImageAnimBase):
    """
    base class for reveal In and reveal Out

    reveals the foreground image from left/top/right/bottom

    background=None     possible background color
    bgImage             possible background image
    fgImage             required foreground image
    revealIn=True       True to revealIn (expose image) False to revealOut (hide image)
    revealFrom="Left"   or "Right", "Top","Bottom"
    """
    # user supplied params
    background=None # possible background colour
    revealIn=True
    revealFrom="Left"
    revealStep=0
    alpha=255

    def __init__(self,**kwargs):
        super(Reveal,self).__init__(**kwargs)

        # in case user gets flamboyant with capitalisation
        self.revealFrom=self.revealFrom.lower()

    def reset(self,**kwargs):
        super(Reveal, self).reset(**kwargs)

        self.alpha=255 if self.revealIn else 0
        self.fgImage.fillAlpha(255-self.alpha)

    def setWindow(self):
        #
        w,h=self.fgImage.getSize()

        if self.revealStep==w:
            if self.debug: print "horizontal limit reached"
            return

        self.revealStep=(self.revealStep+1)%w

        if self.revealFrom=="left":
            # TODO - could be quicker if the output is cumulative
            # also the panel may well crop if we just slide the image
            if self.revealStep == w:
                self.animationHasFinished()
                if self.debug: print "Reveal horizontal limit reached"
                return
            
            if self.revealStep>=0 and self.animStep<w:
                self.fgImage.fillWindowAlpha((0,0,self.revealStep,h-1),self.alpha)

        elif self.revealFrom=="right":
            if self.revealStep == w:
                self.animationHasFinished()
                if self.debug: print "Reveal horizontal limit reached"
                return
            
            if self.revealStep >=0 and self.revealStep < w:
                self.fgImage.fillWindowAlpha((w-1-self.revealStep, 0, self.revealStep, h - 1),self.alpha)

        elif self.revealFrom == "top":
            if self.revealStep == h:
                self.animationHasFinished()
                if self.debug: print "Reveal vertical limit reached"
                return
            
            if self.revealStep >= 0 and self.revealStep < h:
                self.fgImage.fillWindowAlpha((0,0, w - 1, self.revealStep),self.alpha)

        elif self.revealFrom == "bottom":
            if self.revealStep == h:
                self.animationHasFinished()
                if self.debug: print "Reveal vertical limit reached"
                return
            
            if self.revealStep >= 0 and self.revealStep < h:
                self.fgImage.fillWindowAlpha((0, h-1-self.revealStep, w - 1, self.revealStep),self.alpha)

        else:
            raise ValueError(self.classname+".setWindow() unexpected revealFrom param ("+self.revealFrom+") for "+self.animationClass())


    def step(self, chain=None):
        # speed control
        if self.isNotNextStep(): 
            if not self.init: self.refreshCanvas()
            return

        if self.init:
            self.animStep=0
            self.init=False

        self.setWindow()
        self.refreshCanvas()

class RevealOut(Reveal):
    # user supplied params
    # see Reveal base class

    revealIn = False

class RevealIn(Reveal):

    # user supplied params
    # see Reveal base class

    revealIn=True

class Expand(ImageAnimBase):
    """
    Expand - image grows from the middle of the panel outwards either exposing the foreground image
    (ExpandIn) or hiding it (ExpandOut).

    With background images, ExpandIn and ExpandOut can look identicsl. ExpandIn makes the foreground image
    appear over the background where as expandOut makes it look like the background is being expanded in
    in front of the foreground.

    This is achieved by changing the foreground image alpha

    See Collapse - which works for the outside in

    Parameters:-

    expandStep=nn


    """

    # user paramters
    expandStep = 1

    # defaults
    expandYgrowth=1
    expandXgrowth=1
    expandIn = True

    expandCentreX=0    # arbitrary values will be calculated
    expandCentreY=0
    expandMaxStep=0
    alpha=0


    def reset(self,**kwargs):
        super(Expand,self).reset(**kwargs)

        self.alpha=255 if self.expandIn else 0
        self.fgImage.fillAlpha(255-self.alpha)

    def setWindow(self):
        """
        setWindow recalculates the x,y,w,h values based on the expandStep
        :return: copies the image region
        """
        # nothing to do?
        if self.expandStep==0: return

        iw,ih=self.fgImage.getSize()

         # windows grows from the middle to the outside
        x=self.expandCentreX-self.expandStep*self.expandXgrowth
        y=self.expandCentreY-self.expandStep*self.expandXgrowth
        w=2*self.expandStep*self.expandXgrowth
        h=2*self.expandStep*self.expandYgrowth

        # make sure limits are not exceeded - which can happen
        if x<0: x=0
        if y<0: y=0
        if w > iw: w =iw
        if h > ih: h =ih

        if w==iw and h==ih:
            self.animationHasFinished()

        self.fgImage.fillWindowAlpha((x,y,w,h),self.alpha)


    def step(self, chain=None):
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        if self.init:
            # must be floating point
            imWidth,imHeight=float(self.fgImage.getWidth()),float(self.fgImage.getHeight())

            self.expandCentreX=imWidth/2
            self.expandCentreY=imHeight/2

            if self.expandIn:
                # set the output image to black
                # transparency is not affected
                #if self.background is not None and self.bgImage is None:
                #    self.fgImage.fill(self.background)
                pass

            self.expandStep=0
            if imWidth>imHeight:
                self.expandXgrowth=imWidth/imHeight
                self.expandYgrowth=1.0
                self.expandMaxStep=imHeight/2
            else:
                self.expandXgrowth=imHeight/imWidth
                self.expandYgrowth=1.0
                self.expandMaxStep = imWidth / 2

            self.setWindow()
            self.refreshCanvas()
            self.init=False
            return

        #TODO check if reveal has finished

        if self.expandStep < self.expandMaxStep:
            self.expandStep += 1
            self.setWindow()

        else:
            self.expandStep=self.expandMaxStep
            if self.animLoops:
                self.init=True

        self.refreshCanvas()

class ExpandIn(Expand):
    expandIn=True

class ExpandOut(Expand):
    expandIn=False

class Blur(ImageAnimBase):
    """
    Blur - well, blurs the image. It is subclessed by BlurIn and BlurOut

    parameters:-

    blurStep=0.05   amount to blur on each step

    """
    blurIn=True
    maxBlur=1
    minBlur=0
    blurStep=0.05
    sigma=0     # current blur factor

    def reset(self,**kwargs):
        super(Blur,self).reset(**kwargs)

        # must be done before first step()
        self.sigma = self.maxBlur if self.blurIn else self.minBlur
        self.fgImage.blur(self.sigma)

    def step(self):
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        if self.init:
            # nothing to do
            self.init=False

        self.fgImage.blur(self.sigma)
        self.refreshCanvas()

        if self.blurIn:
            self.sigma-=self.blurStep
            if self.sigma<self.minBlur:
                self.animationHasFinished()
                self.sigma=self.minBlur
        else:
            self.sigma+=self.blurStep
            if self.sigma>self.maxBlur:
                self.animationHasFinished()
                self.sigma=self.maxBlur


class BlurIn(Blur):
    """
    sub class of Blur
    """
    blurIn=True

class BlurOut(Blur):
    """
    sub class of Blur
    """
    blurIn=False

class TheMatrix(ImageAnimBase):
    """
    Rolls the foreground image supplied in the fashion of The Matrix.
    There isn't meant to be any background image or colour.
    Image columns are rolled at random speeds between 1 and 3 pixels at a time.

    Parameters

    fgImage See Image class

    """

    # calculated
    columnSpeeds=[]



    def reset(self,**kwargs):
        super(TheMatrix,self).reset(**kwargs)

        # make sure we start with a clean image
        self.fgImage.reset()

    def step(self):
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        imWidth,imHeight=self.fgImage.getSize()

        if self.init:
            for s in range(imWidth):
                self.columnSpeeds.append(random.randint(1,3))
            self.refreshCanvas()
            self.init=False
            return

        # roll each column by the given amount

        for col in range(imWidth):
            window=col,0,1,imHeight-1
            self.fgImage.rollWindow(window,"down",self.columnSpeeds[col])

        self.refreshCanvas()

class Collapse(ImageAnimBase):
    """
    Collapse - image grows from the outer edges towards the centre either exposing (CollapseIn) the foreground image
    or hiding it (CollapseOut)

    With background images, they can look identicsl. CollapseIn makes the foreground image
    appear over the background where as CollapseOut makes it look like the background is being collapsed
    in front of the foreground.

    This is effect achieved by changing the foreground image alpha using two overlapping windows. Hopefully this is
    fast enough to go unseen

    Parameters:-

    collapseStep=nn


    """


    # user paramters
    collapseStep = 1

    # in or out?
    collapseIn = True


    # defaults
    collapseYgrowth=1
    collapseXgrowth=1
    collapseCentreX=0    # arbitrary values will be calculated
    collapseCentreY=0
    collapseMaxStep=0
    alpha=0


    def reset(self,**kwargs):
        super(Collapse,self).reset(**kwargs)

        self.alpha=255 if self.collapseIn else 0
        self.fgImage.fillAlpha(255-self.alpha)

    def setWindow(self):
        """
        setWindow recalculates the x,y,w,h values based on the collapseStep
        :return: copies the image region
        """
        # nothing to do?
        if self.collapseStep==0: return

        iw,ih=self.fgImage.getSize()

         # windows grows from the middle to the outside
        x=self.collapseStep*self.collapseXgrowth
        y=self.collapseStep*self.collapseXgrowth
        w=iw-2*self.collapseStep*self.collapseXgrowth
        h=ih-2*self.collapseStep*self.collapseYgrowth

        # make sure limits are not exceeded - which can happen
        if x<0: x=0
        if y<0: y=0
        if w <= 0: w =0
        if h <= 0: h =0

        if w==0 and h==0:
            self.animationHasFinished()

        # outer part
        self.fgImage.fillWindowAlpha((x,y,w,h),self.alpha)
        self.fgImage.fillWindowAlpha((x+1, y+1, w-2, h-2), 255-self.alpha)

    def step(self, chain=None):
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        if self.init:
            # must be floating point
            imWidth,imHeight=float(self.fgImage.getWidth()),float(self.fgImage.getHeight())

            self.collapseStep=0
            if imWidth>imHeight:
                self.collapseXgrowth=imWidth/imHeight
                self.collapseYgrowth=1.0
                self.collapseMaxStep=imHeight/2
            else:
                self.collapseXgrowth=imHeight/imWidth
                self.collapseYgrowth=1.0
                self.collapseMaxStep = imWidth / 2

            self.setWindow()
            self.refreshCanvas()
            self.init=False
            return

        if self.collapseStep < self.collapseMaxStep:
            self.collapseStep += 1
            self.setWindow()

        self.refreshCanvas()

class CollapseIn(Collapse):

    collapseIn=True

class CollapseOut(Collapse):

    collapseIn=False
