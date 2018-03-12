'''

TextAmimBase.py

Base class for text animations.

See AnimBase.py for general parameters

Fonts supported are BDF and HERSHEY

Parameters:-

fontFace            either "BDF" or FONT_HERSHEY_??
                    default is FONT_HERSHEY_SIMPLEX
multiColored        only BDY fonts - uses palette to color each letter
fontSize            pixel size wanted
fgColor             foreground color
bgColor             background color or None (default)
text                the message
origin              (x,y) where to draw the text
bottomLeftOrigin    Origin is either top/left (False) or bottom/Left (True)

'''

import numpy as np
import Panel
from LEDAnimator.AnimBase import AnimBase
from LEDAnimator.NumpyImage import NumpyImage
from LEDAnimator.BDF import Font as bdf
from Constants import *
import Font
from Palette import *
from Colors import *
from ExceptionErrors import *
from Text import *
from Image import *


class TextAnimBase(AnimBase):

    Xpos=0                          # used when moving text
    Ypos=0
    origin=(0,0)                    # x,y for drawing
    bottomLeftOrigin = False        # top left corner is used for placement on the LED Panel
    text=Text()                     # text message to render

    font=None                       # font object
    palette=None                    # ignored if fgColor is not None
    fgColor=None                    # text character rendering colour
    bgColor=None                    # transparent background, for now
    textAlpha=1.0                   # for fading effects
    zoom=None                       # Future: would be (startSize,endSize)
    textBuffer=None                 # for rendering text before sending to panel
    lineType=None                   # possibly passed in for Hershey fonts
    startPos=None                   # used by Move routines
    endPos=None                     # ditto

    def __init__(self, **kwargs):
        super(TextAnimBase, self).__init__(**kwargs)

        # override defaults
        # gather any passed in values
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

        assert isinstance(self.text,Text),"text parameter must be an instance of Text."

        self.font=Font.Font(self.text.getFontFace(),self.text.getFontSize())

        # This needs changing to use self.text.Xpos etc at some point
        self.origin=(self.Xpos,self.Ypos)
        self.Xpos1,self.Ypos1=self.origin

        if self.text.lineType:
            self.lineType=self.text.lineType

        # buffer size needs to be adjusted if HERSHEY because openCV seems to
        #lose the first two horizontal pixels (left and right) and 2 vertical (top and bottom)


        # set the textBuffer to transparent black to start with
        w, h = self.font.getTextBbox(self.text.getText())
        if self.font.getFontType()==BDF_FONTTYPE:
            # BDF font width does not leave a gap between letters
            self.textBuffer = np.zeros((h+2, w, 4), dtype=np.uint8)
        else:
            # openCV fonts need a bigger margin
            self.textBuffer=np.zeros((h+4,w+4,4),dtype=np.uint8)

        self.setBgColor()

    def reset(self,**kwargs):

        super(TextAnimBase,self).reset(**kwargs)

        # fills the textBuffer
        self.setBgColor()

        if self.startPos is not None:
            self.origin=self.startPos

    def getFgColor(self):
        """
        Deals with returning a single colour or next color from   a palette
        :return:
        """
        color=self.text.getFgColor()
        if color is None:
            return None
        elif isinstance(color,Palette):
            if self.text.getMultiColored():
                return color
            return color.getNextEntry().getPixelColor()
        elif isinstance(color,Color):
            return color.getPixelColor()
        return color

    def getBgColor(self):
        """
        Deals with returning a single colour or next color from a palette
        :return:
        """
        color=self.text.getBgColor()
        if  color is None:
            return None
        elif isinstance(color,Palette):
            c=color.getNextEntry().getPixelColor()
            return c
        elif isinstance(color,Color):
            return color.getPixelColor()
        return color

    def setBgColor(self):
        """
        Sets the BgColor and fills text buffer with it. Useful for changing
        the background.

        Should be called before drawText()

        NOTE: When using BDF fonts the foreground and background colors can be set for the characters - ie. a string
        will be one foreground color and one background color

        :param tuple color: rgba tuple, in Pixel order
        :return Nothing: the text buffer is filled
        """

        color=self.getBgColor()
        if color is None:
            return

        # fill the buffer
        self.textBuffer[:,:]=[color]

    def drawText(self): #,brightness=1.0,alpha=1.0):
        """
        renders current text onto the text buffer which can be later copied to the Panel
        at the required point using refreshCanvas()

        uses self.fgColor and text.bgColor

        BDF fonts don't support anti-aliasing but openCV (HERSHET) fonts do.

        When rendering multicolored text brightness and alpha are required.

        NOTE: BDF and openCV (Hershey) fonts render differently. OpenCV renders on the baseline whereas BDF is above
        the baseline.


        :param float brightness: 0->1.0
        :param float alpha: 0->1.0
        :return Nothing: The text is drawn using either BDF fonts (if bdfFontID is not None) or openCV fonts
        """

        if self.text.getText() is None: return    # nothing to do

        ascent,descent= self.font.getFontMetrics()

        fontType=self.font.getFontType()

        if fontType==BDF_FONTTYPE:
            # BDF fontsize=ASCENDER+DESCENDER
            # baseline is the gap measured from the bottom of the bounding box
            # since BDF renders at the top left we need to push it down
            # also, openCV needs a margin of 2 pixels at left and top so we do the same here
            # so they appear similar
            origin=(1,0)
        elif fontType == TRUETYPE_FONTTYPE or fontType==OPENTYPE_FONTTYPE or fontType==PIL_FONTTYPE:
            origin=(0,0)
        elif fontType==HERSHEY_FONTTYPE:
            # openCV fonts take Y to be the baseline which make text render above 0 so
            # we must move it down
            origin=(2,ascent+2)
        else:
            raise UnknownFontType

        self.font.drawText(self.textBuffer,origin,self.text.getText(),self.text.getFgColor(),self.lineType)


    def refreshCanvas(self):
        """
        create the canvas for this text layer on top of image layers.

        calls the base class refreshCanvas() method first

        :return Nothing: the text buffer is written to the Panel

        """

        # lay down background color/images etc first
        super(TextAnimBase,self).refreshCanvas()

        # text is drawn on the top of previous layers
        h,w=self.font.getFontBbox()

        x,y=self.origin if self.origin is not None else (0,0)

        if self.bottomLeftOrigin:
            h,w=self.textBuffer.shape[:2]
            y=y-h

        # set alpha textAlpha is in range 0->1.0
        # no point bothering if alpha is zero
        if self.textAlpha>0:
            # multiply all alphas by textAlpha to retain relative transparency
            self.textBuffer[..., ALPHA].astype(np.uint8)*self.textAlpha
            Panel.DrawImage(x, y, self.textBuffer)



