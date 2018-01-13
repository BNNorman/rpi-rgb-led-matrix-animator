'''
TextAnimations.py

a list of possible text animations


TODO convert to openCV fonts only
'''

from TextAnimBase import TextAnimBase
import time
import Panel
import cv2

# ON
class On(TextAnimBase):
    """
    On simply displays the text message until the duration expires
    """
    def __init__(self, **kwargs):
        super(On, self).__init__(**kwargs)
        self.reset()

    def reset(self,**kwargs):
        super(On,self).reset(**kwargs)

    def step(self):
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        if self.init:
            self.drawText()
            self.init=False

        self.refreshCanvas()

# FADE
class Fade(TextAnimBase):
    """
    fade text in or out

    If multiColored is True then each character uses the colors from the palette

    """
    direction=1    # fade in, -1=fade out
    alpha=1.0      # current transparency

    def __init__(self, **kwargs):
        super(Fade, self).__init__(**kwargs)
        self.reset()

    def reset(self,**kwargs):
        super(Fade, self).reset(**kwargs)

    def step(self, chain=None):

        if self.isNotNextStep():
            # don't bother if init hasn't been done
            if not self.init:
                self.drawText(alpha=self.alpha)
                self.refreshCanvas()
            return

        if self.init:
            self.fgColor=self.palette if self.multiColored else self.palette.getNextEntry().getPixelColor()
            self.c = self.getNextPaletteEntry()
            self.alpha=0.0 if self.direction==1 else 1.0
            self.init=False

        # fadeInOut needs to know brightness
        self.alpha = float(self.tick) / (self.fps)

        # make the brightness increase
        if self.direction==1:
            if self.alpha > 1.0: self.alpha=1.0   # can't increase beyond full on
        # or make the brightness decrease
        else:
            self.alpha = 1.0 - self.alpha
            if self.alpha < 0.0:  self.alpha=0.0  # can't decrease below full off

        # is the text plain or multi-colored?
        # color selection based on bdfFontID and multicolored flags

        self.drawText(alpha=self.alpha)
        self.refreshCanvas()

#FADE-IN
class FadeIn(Fade):
    """
    sub class of Fade
    """

    def __init__(self,**kwargs):
        super(FadeIn,self).__init__(**kwargs)
        self.direction=1
        self.reset()

    def reset(self,**kwargs):
        super(Fade,self).reset(**kwargs)

# FADE-0UT
class FadeOut(Fade):
    """
    sub class of Fade
    """
    def __init__(self,**kwargs):
        super(FadeOut, self).__init__(**kwargs)
        self.direction=-1
        self.reset()

    def reset(self):
        super(FadeOut,self).reset()

class Move(TextAnimBase):
    """
    general purpose text mover.

    Will slide text from startPos(x,y) to endPos(x,y)


    """

    startPos=(0,0)      # where we come back to when we cycle
    endPos=(0,0)        # where we end up
    origin=startPos     # used by drawText
    xScroll = 0         # not moving - number of steps to move (+/-)
    yScroll = 0         # not moving
    yLimit=Panel.height # recalculated base on the text size
    xLimit=Panel.width
    multiColored=False



    def reset(self,**kwargs):
        super(Move,self).reset(**kwargs)
        self.origin=self.startPos

    def step(self):
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        if self.init:
            self.drawText()

            # work out the limits
            self.yLimit=0 # keep the compiler happy
            self.xLimit=0

            # initial drawing position
            self.Xpos,self.Ypos=self.startPos

            xStart, yStart = self.startPos
            xEnd,yEnd=self.endPos

            # calculate the ammount to move
            # and remember these
            self.xScroll=(xEnd-xStart)*self.speed/self.fps
            self.yScroll=(yEnd-yStart)*self.speed/self.fps

            #self.drawText()
            #self.refreshCanvas()
            self.init = False

        # move the text drawing point
        self.Xpos+=self.xScroll
        self.Ypos+=self.yScroll

        # have we reached the end points?
        # the calculation is complicated by direction of movement.
        xEnd,yEnd=self.endPos

        # possible bug - could reach xEnd before yEnd
        # though should not need to check Y because it's a straight line
        if self.xScroll>0:  # moving right
            if self.Xpos>=xEnd: self.init=True
        else:
            if self.Xpos<=xEnd: self.init=True

        self.origin=(self.Xpos,self.Ypos)   # origin is used by drawText
        self.drawText()
        self.refreshCanvas()

class Wait(TextAnimBase):
    """
    wait does nothing except refresh the canvas for the duration
    """
    def _init__(self,**kwargs):
        super(Wait, self).__init__(**kwargs)

    def reset(self,**kwargs):
        super(Wait, self).reset(**kwargs)

    def step(self):
        self.refreshCanvas()