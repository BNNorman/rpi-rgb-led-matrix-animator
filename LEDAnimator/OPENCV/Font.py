"""
Font.py

Handles the openCv fonts

The fonts will be rendered into a textBuffer just big enough to hold the message
then drawn on the Panel so we don't care about originBottomLeft - that will
be taken care of when the textBuffer is copied to the panel

"""
import LEDAnimator.UtilLib
import numpy as np

from LEDAnimator.Colors import *
from LEDAnimator.Constants import *
from LEDAnimator.Palette import *


import os


WHITE=White.getPixelColor() # foreground RGBA 100% alpha

class Font():

    fontScale=1.0
    fontFace=FONT_HERSHEY_SIMPLEX
    thickness=1.0
    italic=False
    size=10
    lineType=LINE_8

    def __init__(self,size,fontFace=FONT_HERSHEY_SIMPLEX,thickness=1,lineType=LINE_8,italic=False):
        """
        simply initialises the values required by openCV putText

        :param int size:
        :param int fontFace: default is FONT_HERSHEYT_SIMPLEX
        :param int thickness: default 1
        :param int lineType: LINE_8,LINE_4 or LINE_AA (Anti-aliased)
        :param bool italic: True for italic fonts
        """
        assert type(size) is int,"Size parameter must be an int got "+str(size)

        # hershey font at scale=-10 renders at 22pt
        self.size=size
        self.fontScale=size/HERSHEY_FONTSIZE
        self.fontFace=fontFace
        self.lineType=lineType
        self.thickness=thickness
        self.italic=italic

    def getFontType(self):
        return HERSHEY_FONTTYPE

    def setFontFace(self,fontFace):
        self.fontFace=fontFace

    def setFontSize(self,fontSize):
        self.fontSize=fontSize
        self.fontScale=fontSize/HERSHEY_FONTSIZE

    # TODO test line thickness
    def setLineThickness(self,thickness):
        """
        stes the line thickness for drawing. Default=1
        :param int or float thickness:
        :return:
        """
        self.tickness=thickness

    def setLineType(self,type):
        """
        sets the line type to use.
        :param int type: LINE_AA,LINE_4, LINE_8
        :return None: The line type flag is set
        """
        self.lineType=type

    # TODO test italic
    def setItalic(self):
        """
        sets the itelic flag - text should be rendered italic
        :return None:
        """
        self.italic=True

    def setNoneItalic(self):
        """
        unsets the italic flag - text should be rendered normally
        :return None:
        """
        self.italic=False

    def getFontMetrics(self):
        """
        Only returns the font ascent and descent
        :return int,int:ascent,descent
        """
        (w,h),b=cv2.getTextSize("W",self.fontFace,self.fontScale,self.thickness)
        return h,b

    def getFontBbox(self):
        """
        Get the bounding box.

        Returns the width, height and baseline for the font as a whole.

        Individual characters can have different widths so we fake it using the letter W

        It is better to use getText(msg) to find the actual width of the whole message

        :return int,int,int: width,height,baseline (measured from top)
        """
        # for openCV fonts h is the ascent
        (w,h),b=cv2.getTextSize("W",self.fontFace,self.fontScale,self.thickness)
        return w,h+b


    def getTextBbox(self,text):
        """
        returns the calculated width and height of a text string rendered in this fontFace.

        For openCV the font point size is the Acsent only so we add the baseline (descent)

        :param str text: a string of characters
        :return int,int: width,height of the bounding box
        """

        # opencv routine seems to get this wrong (too short)
        #(w,h),b=cv2.getTextSize(text,self.fontFace,self.fontScale,self.thickness)

        len=0
        h=0
        b=0
        for ch in text:
            (w, h), b = cv2.getTextSize(ch, self.fontFace, self.fontScale, self.thickness)
            len+=w
        return len,h+b

    def channelSwap(self, color):
        """
        swaps the red and blue channels for simulator use
        since openCV uses BGR images and PIL uses RGB

        See Constants.py for RGB_R and RGB_B values

        :param tuple color: (R,G,B)
        :return: (r,g,b) r&b swapped if required
        """

        if RGB_R == 0: return color

        # R & B are swapped
        R, G, B ,A= color[RGB_R], color[RGB_G], color[RGB_B], color[ALPHA]
        return (R, G, B,A)

    def drawText(self,img,x,y,message,fgColor,lineType=LINE_8):
        """
        openCV font draw clips the text to the img it is being drawn on. The BDF fonts are written to a buffer
        then clipped.

        :param numpy ndarray img: image on which to draw the text
        :param float x: x position to draw the text at
        :param float y: y position to draw text at
        :param str message: text message
        :param tuple or Palette fgColor: (r,g,b,a) in Pixel colour order or a list or Color objects
            If this is a tuple then all the text is rendered in that color.
            If this is a Palette then letters are colored using colors drawn cyclically from
            the palette.
        :return None: text is drawn on the img
        """

        lineType=LINE_8 if lineType is None else lineType
        font = self.fontFace | FONT_ITALIC if self.italic else self.fontFace

        # if fgColor is a Palette then we use the colors cyclically
        # which allows us to color each letter differently
        # otherwise all the letters are colored with fgColor
        # Background colors are handled by textAnimBase

        if isinstance(fgColor,Palette):
            Xpos=x
            for ch in message:
                (w, h), b = cv2.getTextSize(ch, self.fontFace, self.fontScale, self.thickness)
                color=fgColor.getNextEntry().getPixelColor(alpha=1.0)
                color=self.channelSwap(color)
                cv2.putText(img, ch,(Xpos,y), font, self.fontScale, color,self.thickness,lineType,False)
                Xpos+=w
        else:
            # text is all one colour
            color = self.channelSwap(fgColor)
            cv2.putText(img, message,(x,y), font, self.fontScale, color, self.thickness, self.lineType,False)

