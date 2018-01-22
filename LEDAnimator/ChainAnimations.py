"""
ChainAnimations.py

a collection of possible LED chain animations.

These are just examples you may use. You can add your own here and remove any that are never used.

To use them you do something like this in your main.py:-

DAF_D_SEQ= AnimSequence.AnimSequence([
    ChainAnimations.Collider(duration=5, speed=0.1, palette=Palette.RGB, fps=FPS),
    ChainAnimations.FadeIn(duration=5, speed=1, palette=Palette.RGB, fps=FPS),
    ChainAnimations.Wait(duration=6, speed=0.5, palette=Palette.RED, fps=FPS),
    ChainAnimations.WipeRight(duration= 10, speed=1, palette=Palette.RGB, fps=FPS)
])


"""
import time
import random
from LEDAnimator.Colors import *

from ChainAnimBase import ChainAnimBase

# SPARKLE

class Sparkle(ChainAnimBase):
    """
    randomly selects a color from the supplied palette and uses it to color a random pixel at a random brightness
    """

    def step(self):
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        if self.init:
            assert self.palette is not None,"No palette for Sparkle animation"
            self.init=False

        for p in range(self.chain.getLength()):
            color=self.palette.getRandomEntry().getPixelColor()
            self.chain.setPixel(p,color)
            factor=random.randint(0,10)/10.0
            self.chain.setPixelBrightness(p,factor)

        self.refreshCanvas()

# SPARKLE-RANDOM
class SparkleRandom(ChainAnimBase):
    """
    Same as SPARKLE but selects a random color - palette is ignored
    """
    def step(self):
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        self.chain.setAllPixelsRandom()
        self.refreshCanvas()

# COMET - a single comet heading left or right
# used by CometRight and CometLeft
class Comet(ChainAnimBase):
    """
    comet is a sequence of pixel which tail off in brightness

    By default the comet is monochrome and uses the first color in the palette for the first session then
    selects the next color for the next session and so on.

    If multiColored is selected it selects the colors from the palette to fill the comet. The palette is reused cyclically

    """
    tailLen=None         # none means use the palette size for the tail length
    direction=1          # low to high (left to right)
    multiColored=False  # if true uses the entire palette otherwise picks one color


    def setTailLength(self,length):
        self.tailLen=length

    def step(self):
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        if self.init:
            if self.tailLen is None: self.tailLen=self.palette.getLength()

            # draw the initial pattern - just one comet
            self.chain.setAllPixels(Black.getPixelColor(alpha=0)) # transparent
            c = self.getNextPaletteEntry()  # color to use if not multicolored

            for p in xrange(self.tailLen):
                if self.multiColored: c = self.getNextPaletteEntry()
                brightness = float(p) / self.tailLen

                if self.direction<0: brightness = 1.0-brightness
                self.chain.setPixel(p,c.getPixelColor(brightness=brightness,alpha=brightness))
            self.init = False


        self.refreshCanvas()
        self.chain.roll(self.direction)

# COMET-RIGHT
class CometRight(Comet):
    direction=1

# COMET-LEFT
class CometLeft(Comet):
    direction=-1


# COMETS - repeating pattern of commets head to tail
# length of tail is determined by number of entries in the palette
class Comets(ChainAnimBase):
    """
    Comets is the same as comet but the chain is filled nose to tail
    """
    direction=1
    multiColored=False  # use first entry then next etc
    tailLen=None        # use the palette length if None

    def step(self):
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        chainLen=self.chain.getLength()

        if self.init:
            if self.tailLen is None: self.tailLen = self.palette.getLength()

            # draw the initial patterns
            self.chain.setChainBrightness(1.0)
            c = self.getNextPaletteEntry()
            for p in xrange(chainLen):
                if self.multiColored: c = self.getNextPaletteEntry()
                # head of the comet is brightest
                brightness = float(p % self.tailLen) / self.tailLen

                # comets going left should get dimmer left to right
                if self.direction<0: brightness=1.0-brightness
                # comets become transparent as they fade
                # human eye response is square law
                brightness=brightness*brightness
                self.chain.setPixel(p, c.getPixelColor(brightness=brightness,alpha=brightness))

            self.init=False

        self.chain.roll(self.direction)
        self.refreshCanvas()

class CometsRight(Comets):
    direction=1

class CometsLeft(Comets):
    direction=-1


# PULSE - similar to fade in/out but no fading
# uses a 25% duty cycle
# each pulse uses the next color from the palette
# cycling through
class Pulse(ChainAnimBase):
    """
    Pulse the leds on and off with duty cycle

    duty is a %

    """
    # use a square wave duty cycle
    # to turn LEDS on or Off

    # passed in
    duty=25

    #calculated
    switchOverPoint=0

    def step(self):
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        if self.init:
            self.chain.setAllPixels(self.getNextPaletteEntry().getPixelColor())
            self.switchOverPoint=(self.duty/100.0)*self.speed*self.fps
            self.init=False

        # number of ticks per second = speed*fps
        # ON cycle at 25% duty would be upto duty*speed*fps

        brightness=1.0 if self.tick>0 and self.tick<self.switchOverPoint else 0

        # this does not take effect till the chain is rendered
        # so it doesn't take a long time
        self.chain.setChainBrightness(brightness)
        self.refreshCanvas()

# ALT-ON-OFF
# if palette contains only one color then Alt color is black
# otherwise first two colors are used
class AltOnOff(ChainAnimBase):

    def step(self):
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        # get first color
        color1=self.palette.getEntry(0).getPixelColor()

        # use black as the alternate color if only one palette entry
        if self.palette.getLength()<2:
            color2=Black.getPixelColor()
        else:
            color2=self.palette.getEntry(1).getPixelColor()

        chainLen=self.chain.getLength()

        if self.init:
            self.init=False
            # populate the chain
            for p in range(0,chainLen):
                x,y=self.chain.getPixelXY(p)
                if p%2:
                    self.chain.setPixel(p,color1)
                else:
                    self.chain.setPixel(p,color2)

        self.refreshCanvas()
        self.chain.roll(1)

# ON - uses the palette to color LEDS
# if the color is black the LEDs will be off
class On(ChainAnimBase):

    def step(self):
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        if self.init:
            self.chain.setAllPixels(self.getNextPaletteEntry().getPixelColor())
            self.init=False

        # the animation does nothing else
        # it leaves the LEDs on as initialised
        self.refreshCanvas()

#############################################################
#
# fade animations
#
#############################################################

class Fade(ChainAnimBase):
    """
    Fade is the base class for FadeIn,FadeOut and FadeInOut

    Fade takes place over duration time
    """

    direction=1     # fade in by default
    alpha=0         # current transparency
    c=None

    def step(self):
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        if self.init:
            self.c=self.getNextPaletteEntry().getPixelColor()
            self.chain.setAllPixels(self.c)
            self.alpha=0.0 if self.direction > 0 else 1.0
            self.rate=0.1
            self.totalTicks=self.fps*self.duration
            self.init=False
        else:
            # we want the brightness to go from zero to 1.0 in duration seconds
            self.alpha= (time.time() - self.startTime) / self.duration
            if self.direction>0:
                if self.alpha>=1.0:
                    self.animationHasFinished()
                    self.alpha=1.0
            elif self.direction<0:
                self.alpha= 1.0 - self.alpha
                if self.alpha<=0:
                    self.animationHasFinished()
                    self.alpha=0

        self.chain.setChainBrightness(self.alpha)
        self.refreshCanvas()

class FadeIn(Fade):
    direction=1

class FadeOut(Fade):
    direction = -1

# FADE-IN-OUT
class FadeInOut(Fade):
    """
    Fade in-out does what it says on the tin by reversing the fade from in to out
    """
    direction=1 # initial is to fade in

    def __init__(self,**kwargs):
        super(FadeInOut, self).__init__(**kwargs)
        self.reset()

    def reset(self,**kwargs):
        super(FadeInOut,self).reset(**kwargs)
        self.alpha = 0
        self.direction=True # True=fade in, False=Fadeout
        self.init=True

    def step(self):
        super(FadeInOut,self).step()

        # we change the direction of fading here
        if self.alpha==0 and self.direction<0:
            self.direction=1
            self.init=True
        if self.alpha>=1.0 and self.direction>0:
            self.direction=-1
            self.init=True


# WAIT - does nothing but wait
class Wait(ChainAnimBase):
    def step(self):
        self.refreshCanvas()

# Larson scanner - same as Knight Rider car (ish)
class Larson(ChainAnimBase):
    """
    Larson scanner (as seen on Kinght Rider and Battlestar Galactica

    The default size is half the chain.

    Beware, lasronSize must divide wholly into the chain length so try to use
    even length chains
    """
    # user parameters
    larsonSize=2                # default half the chain length
    larsonBackground=None

    # internal
    larsonLen=0                 # calculated
    maxPosition=larsonLen    # calculated


    def step(self):
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        if self.init:
            # setup the Larson
            c = self.getNextPaletteEntry()
            self.chainLen=self.chain.getLength()
            self.larsonLen=int(self.chainLen/self.larsonSize)
            self.maxPosition=self.chainLen-self.larsonLen
            self.chain.setChainBrightness(1)
            if self.larsonBackground is not None:
                self.chain.setAllPixels(self.larsonBackground)
            else:
                self.chain.setAllPixels(Black.getPixelColor(alpha=0)) # transparent background

            # construct the shape on the left
            for p in range(self.larsonLen/2+1):
                #
                brightness=2*float(p)/self.larsonLen
                # human eye is nearly a square law
                # we set alpha as well so that the shape fades right out
                brightness=brightness*brightness
                color=c.getPixelColor(brightness=brightness,alpha=brightness)
                self.chain.setPixel(p,color)
                self.chain.setPixel(self.larsonLen-p, color)
            self.refreshCanvas()
            self.position=0
            self.direction=True # move right initially
            self.init=False
            return

        else:
            if self.direction:
                # moving right
                if self.position<self.maxPosition:
                    self.chain.roll(1)
                    self.position=self.position + 1
                else: #self.position>=self.maxPosition:
                    self.chain.roll(-1) # reverse
                    self.position = self.position - 1
                    self.direction=False
            else:
                # moving left
                if self.position==0:
                    self.chain.roll(1)  # reverse
                    self.position = self.position + 1
                    self.direction=True
                else:# self.position>0:
                    self.chain.roll(-1)
                    self.position = self.position - 1

        self.refreshCanvas()


class KnightRider(Larson):
    def __init__(self,**kwargs):
        super(KnightRider,self).__init__(**kwargs)

# COLLIDER - comets come in from both ends
# and smash in the middle
class Collider(ChainAnimBase):
    fading=False    # when the collision happens change to True
    chainPos=0
    collided=False  # set when the collision has happened
    tailLen=5

    def step(self):

        if self.isNotNextStep():
            self.refreshCanvas()
            #return

        if self.init:
            self.chainPos = 0
            self.collided=False
            self.brightness=1.0
            self.fading=False
            self.chain.setAllPixels(Black.getPixelColor(alpha=0))  # all transparent
            self.chain.setChainBrightness(1.0)
            self.chain.setChainAlpha(1.0)       # must start visible for colliding comets
            c = self.getNextPaletteEntry()      # color switch on restart

            # draw the left comet
            for p in xrange(self.tailLen):
                # head of the comet is brightest
                brightness = float(p) / self.tailLen
                self.chain.setPixel(p, c.getPixelColor(brightness=brightness,alpha=brightness))

            # right hand comet
            chainLen=self.chain.getLength()
            self.chainMiddle = int(chainLen / 2)

            for p in xrange(self.tailLen):
                # head of the comet is brightest
                brightness = float(p) / self.tailLen
                self.chain.setPixel(chainLen-p-1, c.getPixelColor(brightness=brightness,alpha=brightness))

            self.chainPos=self.tailLen  # remember comet has a tail
            self.init = False
            return

        if self.debug: print self.id, "ChainAnimations.Collider() step() running"

        if self.collided:
            if self.fading:
                if self.brightness<=0:
                    self.reset()
                    return
                self.chain.setChainBrightness(self.brightness)
                self.chain.setChainAlpha(self.brightness)
                self.brightness-=0.1
            else:
                # collided - create white flash
                self.brightness = 1.0
                self.chain.setChainAlpha(1.0)
                self.chain.setAllPixels(White.getPixelColor(brightness=self.brightness, alpha=1))  # white flash
                self.chain.setChainBrightness(self.brightness)
                self.fading = True
        else:
            # shift the pixels in from both ends until collided
            if self.chainPos>=(self.chain.getLength()/2):
                # white flash
                self.collided=True
            else:
                if self.collided:
                    return
                self.chain.shiftIn(fill=None)
                self.chainPos += 1

        self.refreshCanvas()



####################################################
#
# WIPE animations
#
####################################################
#WIPE-IN - color fills for both ends to middle
class WipeIn(ChainAnimBase):
    """
    color fills from both ends to middle
    """
    c=None          # current color being used


    def step(self):
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        self.chainLen = self.chain.getLength()
        self.chainMiddle = int(self.chainLen / 2)

        if self.init:
            if self.c:
                self.chain.setAllPixels(self.c.getPixelColor())
            else:
                self.chain.setAllPixels(Black.getPixelColor())

            self.chain.setChainBrightness(1.0)
            self.c = self.getNextPaletteEntry()
            self.chainPos = 0
            self.init = False

        self.chain.shiftIn(1,self.c.getPixelColor())

        self.chainPos = self.chainPos + 1
        if self.chainPos==self.chainMiddle:
            self.init=True

        self.refreshCanvas()


class WipeOut(ChainAnimBase):
    """
    color fills middle to ends
    """
    c=None # current color being used for fill

    def step(self, chain=None):
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        self.chainLen = self.chain.getLength()
        self.chainMiddle = int(self.chainLen / 2)

        if self.init:
            if self.c:
                self.chain.setAllPixels( self.c.getPixelColor())
            else:
                self.chain.setAllPixels(Black.getPixelColor())

            self.chain.setChainBrightness(1.0)
            self.c = self.getNextPaletteEntry()
            self.chainPos = self.chainMiddle
            self.init = False

        self.chain.shiftOut(1,self.c.getPixelColor())

        self.chainPos=self.chainPos-1
        if self.chainPos == 0:
            self.init=True

        self.refreshCanvas()


class Wipe(ChainAnimBase):
    """
    Wipe is the base class for WipeLeft and WipeRight

    if direction==True the wipe is to the right and if False it is to the left

    """
    c=None          # current color
    direction=True  # default is wipe right
    chainLen=0
    multiColored=False


    def step(self):
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        self.chainLen = self.chain.getLength()

        if self.init:
            # initially clear everything
            if self.c is None: self.chain.setAllPixels(Black.getPixelColor())
            self.chain.setChainBrightness(1.0)
            self.c = self.getNextPaletteEntry()
            self.chainPos=0 if self.direction else self.chainLen-1
            self.init = False

        # the main shifting is done here

        if self.multiColored:
            self.c = self.getNextPaletteEntry()

        if self.direction:
            self.chain.shiftRight(1, self.c.getPixelColor())
            self.chainPos+=1
            if self.chainPos == self.chainLen-1:
                self.init = True
        else:
            self.chain.shiftLeft(1, self.c.getPixelColor())
            self.chainPos-=1
            if self.chainPos == 0:
                self.init = True

        self.refreshCanvas()

class WipeRight(Wipe):
    direction = True

class WipeLeft(Wipe):
    direction = False

