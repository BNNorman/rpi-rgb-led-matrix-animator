"""
TextAnimations.py


"""


from TextAnimBase import TextAnimBase
import time
import Panel
import cv2
from Palette import *
from Colors import Color
from ExceptionErrors import *
from UtilLib import *

# ON
class On(TextAnimBase):
    """
    On simply displays the given text message until the duration expires
    """
    def step(self):
        self.drawText()
        self.refreshCanvas()

# FADE
class Fade(TextAnimBase):
    """
    fade text in or out

    If multiColored is True then each character uses the colors from the palette

    """
    direction=1         # fade in, -1=fade out
    visibility=1.0      # current transparency
    multiColored=False  # not supported with fade in ( well, not yet anyway)
    curFgColor=None       # temp

    def reset(self,**kwargs):
        super(Fade,self).reset()

        # necessary to prevent invisible textBuffer showing up before step() is called
        self.textAlpha = 0.0 if self.direction == 1 else 1.0

    def step(self):

        if self.isNotNextStep():
            self.refreshCanvas()
            return

        if self.init:
            self.FgColor=self.getFgColor()
            self.textAlpha=0.0 if self.direction == 1 else 1.0
            self.origin=(self.Xpos,self.Ypos)
            self.drawText()
            self.refreshCanvas()
            self.init=False

        # work out visibility - time based. We want to fade in starting from the end of a startPause
        # upto the start of the endPause
        # So, goes from zero to hero in duration-startPause-endPause seconds
        self.textAlpha = (time.time()-self.startTime)/(self.duration-self.startPause-self.endPause)

        # make the transparency decrease
        if self.direction==1:
            if self.textAlpha > 1.0:
                self.textAlpha=1.0   # can't increase beyond full on
                self.animationHasFinished()
        # or make the transparency increase
        else:
            self.textAlpha = 1.0 - self.textAlpha
            if self.textAlpha < 0.0:
                self.animationHasFinished()
                self.textAlpha=0.0  # can't decrease below full off

        self.origin=(self.Xpos,self.Ypos)
        self.refreshCanvas()

#FADE-IN
class FadeIn(Fade):
    """
    sub class of Fade
    """
    direction=1

# FADE-0UT
class FadeOut(Fade):
    """
    sub class of Fade
    """
    direction=-1

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
    yLimit=Panel.height # recalculated based on the text size
    xLimit=Panel.width
    multiColored=False  # now in the text object


    def step(self):
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        if self.init:
            self.fgColor=self.getFgColor()
            self.origin = self.startPos
            self.multiColored=self.text.getMultiColored()
            self.drawText()

            # initial drawing position
            self.Xpos,self.Ypos=self.startPos

            xStart, yStart = self.startPos
            xEnd,yEnd=self.endPos

            # calculate the ammount to move
            # and remember these
            self.xScroll=(xEnd-xStart)*self.speed/self.fps
            self.yScroll=(yEnd-yStart)*self.speed/self.fps

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
        #self.drawText()
        print "TextAnimations.Move origin=",self.origin
        self.refreshCanvas()

class Wait(TextAnimBase):
    """
    wait does nothing except refresh the canvas for the duration
    """
    def step(self):
        self.refreshCanvas()