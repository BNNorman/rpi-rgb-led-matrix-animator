"""
Font.py

Handles the TrueType fonts via PIL

The fonts will be rendered into a textBuffer just big enough to hold the message
then drawn on the Panel so we don't care about originBottomLeft - that will
be taken care of when the textBuffer is copied to the panel

"""
import LEDAnimator.UtilLib
import numpy as np

from LEDAnimator.Colors import *
from LEDAnimator.Constants import *
from LEDAnimator.Palette import *

import cv2

# PIL(low) is used to read and render TrueType fonts
try:
    # works on windows (Anaconda) and maybe others
    # might work ok using Anaconda on Linux (Pi Raspbian)
    from PIL import ImageFont,ImageDraw,Image
except:
    try:
        # PILcompat is underlined in PyCharm when developing
        # on Windows because it was moved and renamed on Raspbian Lite
        from PILcompat import Image,ImageFont,ImageDraw
    except:
        raise MissingImageTk

import os


WHITE=White.getPixelColor() # foreground RGBA 100% alpha

class Font():

    fontFace=None       # use default font
    thickness=1.0
    italic=False
    size=10
    font=None           # PIL font object
    lineType=LINE_AA

    def __init__(self,size=10,fontFace=None,thickness=1,lineType=LINE_AA,italic=False):
        """
        simply initialises the values required by PIL

        :param int size: default is 10
        :param str fontFace: default is None
        :param int thickness: Not used; left in for compatability - may switch to kwargs
        :param int lineType: Not used
        :param bool italic: Not used
        """
        assert type(size) is int,"Size parameter must be an int got "+str(size)

        self.size=size              # point size
        self.fontFace=fontFace      # font filename
        self.lineType=lineType      # used to turn on/off anit-aliasing (default is LINE_AA)
        self.thickness=thickness    # not used
        self.italic=italic          # not used

        self.loadFont(fontFace,size)


    def loadFont(self,fontFace,size):
        if fontFace.lower().endswith(".ttf"):
            self.font = ImageFont.truetype(fontFace,size=size)
        elif fontFace.lower().endswith(".otf"):
            self.font = ImageFont.truetype(fontFace,size=size)
        elif fontFace.lower().endswith(".pil"):
            self.font = ImageFont.load(fontFace)
        else:
            # catchall
            self.font= ImageFont.load_default()

    def getFontType(self):
        if self.fontFace.lower().endswith(".ttf"): return TRUETYPE_FONTTYPE
        if self.fontFace.lower().endswith(".otf"): return OPENTYPE_FONTTYPE
        if self.fontFace.lower().endswith(".pil"): return PIL_FONTTYPE
        return UNKNOWN_FONTTYPE

    def setFontFace(self,fontFace):
        self.fontFace=fontFace
        self.loadFont(fontFace,self.size)

    def setFontSize(self,fontSize):
        self.fontSize=fontSize

    def getFontMetrics(self):
        """
        Only returns the font ascent and descent
        :return int,int:ascent,descent
        """
        return self.font.getmetrics()

    def getFontBbox(self):
        """
        Get the bounding box.

        Returns the width, height and baseline for the font as a whole/, which is ok for
        monospaced fonts, so use with care

        Individual characters can have different widths so we fake it using the letter W

        It is better to use getText(msg) to find the actual width of the whole message

        :return int,int: width,height
        """

        return self.getTextBbox("W")


    def getTextBbox(self,text):
        """
        returns the calculated width and height of a text string rendered in this fontFace.

        :param str text: a string of characters
        :return int,int: width,height of the bounding box
        """

        #(x, y, w, h) = self.font.getmask(text).getbbox()

        #img=self.font.getmask(text)
        #w=img.width()
        #h=img.height()

        size=self.font.getsize(text)
        w,h=size[0],size[1]

        # for multi-colored text kerning is ignored which makes the text too long
        wid=0
        for ch in text:
            size=self.font.getsize(ch)
            wid=wid+size[0]

        return wid,h #self.font.getmask(text).getbbox()

    def channelSwap(self,color):
        """
        swaps the red and blue channels for simulator use
        since openCV uses BGR images and PIL uses RGB

        See Constants.py for RGB_R and RGB_B values

        :param tuple color: (R,G,B)
        :return: (r,g,b) r&b swapped if required
        """

        if RGB_R==0: return color

        # R & B are swapped
        R, G, B,A = color[RGB_R], color[RGB_G], color[RGB_B], color[ALPHA]
        return (R, G, B,A)


    def drawText(self,img,x,y,message,fgColor,lineType=LINE_AA):
        """
        draws message onto img. If fgColor is a palette each letter is drawn in
        using colors from the palette cyclically

        :param numpy ndarray img: image on which to draw the text
        :param float x: x position to draw the text at
        :param float y: y position to draw text at
        :param str message: text message
        :param tuple or Palette fgColor: (r,g,b,a) in Pixel colour order or a list or Color objects
            If this is a tuple then all the text is rendered in that color.
            If this is a Palette then letters are colored using colors drawn cyclically from
            the palette.
        :param int lineType: Specifying LINE_AA renders the font using anti-aliasing otherwise not

        :return None: text is drawn on the img
        """

        # if fgColor is a Palette then we use the colors cyclically
        # which allows us to color each letter differently
        # otherwise all the letters are colored with fgColor
        # Background colors are handled by textAnimBase

        pil_im=Image.fromarray(img,'RGBA')
        w,h=pil_im.size[0],pil_im.size[1]

        render=ImageDraw.Draw(pil_im)

        # turn of anit-aliasing?
        if lineType!=LINE_AA:
            render.fontmode="1"

        if isinstance(fgColor,Palette):
            # render each character using the next color in the palette
            Xpos=x
            for ch in message:
                (w, h)= self.getTextBbox(ch)
                color=fgColor.getNextEntry().getPixelColor()
                color=self.channelSwap(color)
                render.text((Xpos,y),ch,font=self.font,fill=color)
                Xpos+=w
        else:
            # single color text
            fgColor=self.channelSwap(fgColor)
            render.text((x, y), message, font=self.font,fill=fgColor)

        #convert the PIL image back to a numpy array
        img[...]=np.array(pil_im)
