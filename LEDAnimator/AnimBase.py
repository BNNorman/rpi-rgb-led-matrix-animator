"""

AnimBase.py

Base class for all animation types.

"""

from LEDAnimator.ExceptionErrors import *
import time
import LEDAnimator.Panel as Panel
from LEDAnimator.NumpyImage import *
from matplotlib.colors import *
from LEDAnimator.Image import *
import random

class AnimBase(object):
    """
    AnimBase - base class of all animations

    The base class
        handles foreground and background images
        calculates the tick value based on animation speed and fps
        selection of next color from a palette
    """

    classname = "AnimBase"

    # default variables
    startTime=time.time()   # reset by reset()
    curPalEntry=0

    background=None         # (r,g,b,a) tuple in Pixel order default None
                            # if set then the Panel is filled before images are laid down.

    fps = 100               # default animation rate (passed in)
    speed = 1.0             # normal speed
    targetSpeed=1.0         # calculated

    duration = 2            # something to work with if omitted
    durationStart=None      # used to determine if duration has expired, set by reset(), cleared by nextFrame()
    palette = None          # list of colours. Currently only used for chain and text animations

    animLoops=False         # play once and stop - animation must check it, true enables repetition before duration expires
    debug = False

    # calculated
    tick=0                  # current tick number (see docs
    lastTick=0              # used to check if we have moved forward
    animationFinished=False # flag set by animation. used to decide if the animation should loop
    animationFinishedTime=None  # the time the animation said it finished

    Xpos,Ypos=0,0           # general positioning


    init=True               # used to indicate that an animation should initialise back to it's start point

    layerBuffer=None        # all animations are render to this first then merged with the Panel frameBuffer

    chain=None              # any animated chain
    chainBuffer=None
    startPause=0            # parameters which may be used to delay the start after a reset()
    endPause=0              # or the restart() after the animation has ended

    ###############################################################################################
    # images
    #
    # images are passed in as instances of Image (see Image.py)
    # ALL animations can have a background image and foreground image
    #
    fgImage=None
    bgImage=None


    def __init__(self, **kwargs):
        """
        intialises the animation base class setting any variables passed in.
        animations can use their own named parameters but they should not clash with the
        default variable names
        :param kwargs: key/value pairs used for passing in animation parameters
        """

        # gather any passed in values
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

        self.setSpeed(self.speed)

        # ALL outputs for this layer are sent to this buffer before sending to Panel
        self.layerBuffer=NumpyImage.NumpyImage(width=Panel.width, height=Panel.height, alpha=0)

    def animationClass(self):
        """
        convenience function to save typing
        :return: the animation sub-class name
        """
        return self.__class__.__name__

    def loadImage(self,which):
        # anything to do?
        if which is None: return

        # already loaded?
        if isinstance(which.image,NumpyImage.NumpyImage):
            if self.debug: print "AnimBase.loadImage() already loaded"
            which.reset()   # image may have been fiddled with (TheMatrix and Roll, Dissolve)
            return

        which.loadImage()
        assert which.image is not None, "Image failed to load"

        # perform any image transform etc
        which.image.transform(which.transMatrix)
        self.scaleImage(which.image,which.scaleMode)
        which.Xpos,which.Ypos=which.image.alignImage(which.alignMode,(Panel.width,Panel.height))

    def endPaused(self):
        """
        User animations can call this is they want to delay looping so viewers can see the end state

        Calls refreshCanvas() to keep the display live

        For this to work the animation code must call self.animationHasEnded() first.

        If True is returned the caller should exit their animation step() method.

        :return bool: True or False
        """
        if self.debug: print "AnimBase.endPaused() checking for",self.animationClass()

        if not self.animationFinished:
            if self.debug: print "AnimBase.endPaused() animation not finished for", self.animationClass()
            return False

        if self.animationFinished and self.animLoops:
            if self.debug: print "AnimBase.animationHasFinished() animLoops is True for",self.animationClass()
            self.reset()

        if self.animationFinishedTime is None:
            if self.debug: print "AnimBase.endPaused() finishedTime is not set for",self.animationClass()
            return False

        if (time.time()-self.animationFinishedTime)<self.endPause:
            if self.debug: print "AnimBase.endPaused() is True for",self.animationClass()
            self.refreshCanvas()
            return True

        if self.debug: print "AnimBase.endPaused() has ended for",self.animationClass()
        return False

    def startPaused(self):
        """
        user animations may call this to see if the animation start is paused
        to let the viewer see the initial state.

        Calls refreshCanvas() to keep the display live

        If True is returned the caller should exit their animation step() method

        :return bool: True or False
        """
        if (time.time()-self.startTime)<self.startPause:
            self.refreshCanvas()
            if self.debug: print "AnimBase.startPaused() is True for",self.animationClass()
            return True

        if self.debug: print "AnimBase.startPaused() is False for",self.animationClass()
        return False

    def animationHasFinished(self):
        """
        called by the animation code to signify the animation has finished

        If the animation has set animLoops to True (default) then the animation will be reset
        and started again ad-infinitum till the duration has passed

        :return:
        """
        #TODO - think about this - it has to work for all animations
        if self.debug: print "AnimBase.animationHasFinished() for",self.animationClass()
        self.animationFinished=True
        self.animationFinishedTime=time.time()

        if self.endPause is not None:
            if self.debug: print "AnimBase.animationHasFinished() endPause is active for",self.animationClass()
            return

        if self.debug: print "AnimBase.animationHasFinished() animLoops is",self.animLoops,"for",self.animationClass()

        if self.animLoops:  self.reset()

    def reset(self,**kwargs):
        """
        used to reset an animation to it's starting state. This is called by the animator
        before the animation begins for the first time. It may be called by animations
        to cause them to loop whilst duration has not expired
        :param kwargs: any parameters required
        :return: nothing
        """

        if self.debug: print "AnimBase.reset() called for",self.animationClass()
        # gather any passed in values
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

        # do any images need loading?
        # it is delayed till the animation begins
        # otherwise it would further delay startup
        self.loadImage(self.bgImage)
        self.loadImage(self.fgImage)

        # reset the animation back to it's starting state
        self.startTime = time.time()
        self.tick = 0
        self.lastTick = 0
        self.animationFinished=False
        self.animationFinishedTime=None

        if self.durationStart is None: self.durationStart=time.time()

        self.init=True  # tells the animation to initialise itself

    def nextFrame(self):
        """
        calculates the current value of self.tick based on the speed of the animation then calls the animation's step()
        function to move the animation on
        :param chain: only used by chain animations (default None)
        :return: True if the duration has expired otherwise false
        """

        # time is up, we move on to the next animation in the sequence
        if (time.time()-self.durationStart)>=self.duration:
            self.durationStart=None
            if self.debug: print "AnimBase.nextFrame() duration has expired for",self.animationClass()
            return True

        # animationFinished is set by the animation to halt/freeze it till the duration has expired
        # however, setting animLoops to True resets the animation so it can loop
        #if self.animationFinished:
            #print "AnimBase.nextFrame() animation has finished for "+self.animationClass()
            #if self.animLoops: self.reset()

        if self.startPaused():  return False
        if self.endPaused():  return False

        # update the current tick value
        t=time.time()-self.startTime    # interval since start
        ticks=t*self.fps                #
        # we report the ticks that have passed based on speed
        # at speed=2.0 this counts from 0,2,4,8...(fps/2)
        # sat speed=1.0 we get 0,1,2,3,..(fps-1)
        # at speed=0.5 it counds 0,0,1,1,2,2,3,3,4,4 ...
        # animations should use the value of self.tick to control their speed
        self.tick=int(self.speed*ticks) % self.fps

        # call the animation step() function to move it on
        self.step()

        # false indicates the animation duration has not expired
        return False

    def step(self):
        """
        Dummy class to warn of missing implementation.
        MUST be overridden in the subclass  (i.e. no super())
        :return None: nada,nothing
        """
        raise MethodNotImplemented("The step() method is missing in "+self.animationClass())

    def setSpeed(self, wanted):
        """
        used to ensure speed is set to a sensible value. Empirical eveidence has shown that if
        speed<=1/fps the animations will stall. If that's the case speed is changed to 1.1/fps.
        :param wanted:
        :return:nothing speed is set
        """
        assert wanted is not None, self.classname + " ERROR: wanted speed not set by " + self.animationClass()
        assert type(wanted) is float or type(wanted) is int,self.classname+"ERROR wanted should be a float or int"
        assert self.fps is not None, self.classname + " ERROR: fps not set by " + self.animationClass()

        # if speed is less than FPS the animations will stall
        if float(wanted) <= (1.0 / self.fps):
            self.speed = 1.1 / self.fps  # fudge to stop animations stalling
            print self.classname + " Animation speed", wanted, "increased to", self.speed,"to prevent animation stalling for", self.animationClass()
        else:
            self.speed = wanted

    #TODO remove this? I have not used it
    def setInfo(self,**kwargs):
        """
        setInfo allows the program to dynamically change parameters at runtime.
        parameter names are not checked so caller must take responsibility
        for spelling etc.
        :param kwargs: key/value pairs
        :return: Nothing
        """
        for key,value in kwargs.iteritems():
            if self.debug: print "AnimBAse.setInfo got key=",key,"value=",value
            setattr(self,key,value)

        self.setSpeed(self.speed)   # may have changed, needs checking

    # TODO - is this needed if it's done in nextFrame before step() is called

    def calcTick(self):
        """
        depracted
        :return:
        """
        return self.tick

    def splitCoordList(self,coordList):
        """
        utility routine to split a list of coordinates into two sepearte lists
        of x and y which can be used to select pixels in an image using numpy
        like arr[x,y]=somevalue to avoid iterating in Python
        This is meant to be used once for lists like LEDs chains when the animation
        first runs
        :param coordList: [[x0,y0],[x1,y1],..[xn,yn]]
        :return: x=[x0,x1..xn],y=[y0,y1,...yn]
        """
        x,y=zip(*coordList)
        return x,y

    def drawChainOnLayerBuffer(self):
        """
        Chain colours are held as HSV they need to be converted to Pixel colours
        before being sent to the Panel.
        ALPHA is ignored because the pixel is written direct to the Panel


        :return:

        """
        x,y,data=self.chain.getAllPixels()
        self.layerBuffer.setPixel(x, y, data)

    def isNotNextStep(self):
        """
        controls the speed of the animation
        :return:  returns True if the animation should not step
        """
        if self.lastTick==self.tick:
            return True
        self.lastTick=self.tick
        return False

    def getNextPaletteEntry(self):
        """
        selects the next colour from the list of colours in a palette. Cycles back to start.
        It is up to the animation to use the ino
        :return: next colour from the palette
        """
        # palette entries are colours
        # return the next in the list
        # cannot be done in the Palette object because
        # pointers are passed and palettes are shared
        # animations COULD combine the palette with the image pixels, maybe...
        assert self.palette is not None,"You need to include a Palette for getNextPaletteEntry(). Use an animation parameter like palette=Palette.XMAS."
        if self.palette is None: return None
        c = self.palette.getEntry(self.curPalEntry)
        self.curPalEntry = (self.curPalEntry + 1) % self.palette.getLength()
        return c

    def getRandomPaletteEntry(self):
        """
        selects a random color from the list of colors in a palette. Cycles back to start.
        It is up to the animation to use the ino
        :return: next colour from the palette
        """
        assert self.palette is not None,"You need to include a Palette for getRandomPaletteEntry(). Use an animation " \
                                        "parameter like palette=Palette.XMAS."

        e=random.randint(0,self.palette.getLength())
        c = self.palette.getEntry(e)
        return c

    def scaleImage(self,img,scaleMode):
        """
        scales the image according to the current scaleMode setting.

        "H"=scale to fit horizontally
        "V"=scale to fit vertically
        "F"=scale to fill the Panel

        :param NumpyImage img: The image to be scaled
        :param str scaleMode: How to scale the image. "H","V" or "F"
        :return: Nothing
        :raises InvalidMode if scaleMode is not "H","V", or "F"
        """
        assert type(scaleMode) is str, self.classname + ".scaleImage() scaleMode character should be a string."
        if scaleMode is None: return

        mode=scaleMode[:1].upper()

        if mode=="V" or mode=="H":
            img.resizeKeepAspect(Panel.width,Panel.height)
        elif mode=="F":
            img.resizeFitToTarget(Panel.width,Panel.height)
        else:
            raise InvalidMode("Image scale mode should be V(ertical),H(orizontal) or F(it)")

    def refreshCanvas(self):
        """
        Builds the output image for this layer of animation. Transparency is used.

        The output image is built in the following order:-
        1. If a background colour is defined wet the Panel colour first
        2. If a background image is defined write that to the Panel.
        3. If a foreground image is defined write that to the Panel.
        4. If a chain is defined write that to the Panel

        :return: Nothing
        """

        # clear the layer buffer amd make sure it's transparent
        self.layerBuffer.clear()

        # has itr got a simple background color?
        if self.background is not None:
            self.layerBuffer.fill(self.background)

        # or has it got a background image?
        if self.bgImage is not None and self.bgImage.image is not None:
            X,Y=self.bgImage.getPosition()
            pasteWithAlphaAt(self.layerBuffer.getImageData(),X, Y, self.bgImage.getImageData())

        if self.fgImage is not None and self.fgImage.image is not None:
            X,Y=self.fgImage.getPosition()
            pasteWithAlphaAt(self.layerBuffer.getImageData(),X, Y, self.fgImage.getImageData())

        if self.chain is not None:
            self.drawChainOnLayerBuffer()

        Panel.DrawImage(0,0,self.layerBuffer.getImageData())


    # TODO is this needed/used
    def drawPixel(self, x, y, colour):
        """
        Draw a pixel, currently ignoring trnasparency on the panel.
        Overwrites anything already at x,y

        :param float x: coord of pixel
        :param float y: coord of pixel
        :param tuple colour: (r,g,b,a) in Pixel colour order
        :return: Nothing
        """
        Panel.DrawPixel(x, y, colour)
