"""

Font.py - a wrapper for other font handlers

An attempt to provide a unified interface to the fonts supported which are currently
openCV HERSHEY and BDF

Updated to use PIL for TrueType and OpenType fonts

useage:

myFont=Font(fontFace,fontSize)

Where fontFace is either an openCV HERSHEY font ID (e.g. FONT_HERSHEY_SIMPLEX)
or a path to a font file. The path should end in .bdf (Bitmap distribution Format) or .ttf (trueType) or .otf (openType)

"""
from Palette import *
from Constants import *
import BDF.Font as BdfFont
import OPENCV.Font as OpenCV
import PILFONT.Font as PilFont

import os
from ExceptionErrors import *
import cv2
from UtilLib import *


class Font():

    fontSize=10
    font=None
    lineType=LINE_8   # Hershey fonts only

    xFudge = 2      # rendering offsets to avoid edge corruption with openCV Hershey
    yFudge=1

    def __init__(self,fontFace,fontSize):
        """

        :param int or str fontFace: For BDF fonts this should be "BDF" for Hershey it should be FONT_HERSHEY_??
        :param float fontSize: will be rounded to nearest integer
        """
        self.fontFace=fontFace          # HERSHEY ID or path to font file
        self.fontSize=nearest(fontSize) # integer - no such thing as half an LED

        if type(fontFace) is str:

            if fontFace=="BDF":
                self.font = BdfFont.Font(fontSize)
            else:
                fname,ext=os.path.splitext(fontFace)
                ext=ext.lower()

                # PIL supports truetype, opentype and native PIL fonts
                if ext==".ttf" or ext==".otf" or ext==".pil":
                    self.font=PilFont.Font(self.fontSize, fontFace)
                elif ext==".bdf":
                    self.font=BdfFont.Font(self.fontSize)
                else:
                    raise UnsupportedFont(fontFace)
        else:
            self.font = OpenCV.Font(self.fontSize,fontFace)

    def getFontType(self):
        return self.font.getFontType()

    def getTextBbox(self,text):
        """
        calculates and returns the length of the text in pixels using the stated font and size.

        :param str message: text message
        :param int thickness: line thickness, only used for HERSHEY fonts
        :return tuple : width, height, baseline calculated width & height of the message in pixels
        """
        return self.font.getTextBbox(text)

    def getFontBbox(self):
        return self.font.getFontBbox()

    def getFontMetrics(self):
        return self.font.getFontMetrics()

    def drawText(self,img,origin,message,fgColor,lineType=None):
        """
        openCV font draw clips the text to the img it is being drawn on. The BDF fonts are written to a buffer
        then clipped.

        :param numpy ndarray img: image on which to draw the text
        :param tuple origin: (x,y) position to draw the text at top left
        :param str message: text message

        :param Color fgColor: if this is a Palette then letters are drawn in colors drawn cyclically from the palette
        :param Color bgColor: defaults to None for transparent background
        :param int thickness: line thickness for Hershey fonts
        :param int lineType: defaults to LINE_AA for hershey fonts - makes no difference to BDF fonts
        :param bool bottomLeftOrigin: default is False=origin at top left
        :return None: text is drawn on the img
        """
        x, y = origin # would it technically be faster to pass a tuple?

        self.font.drawText(img,x,y,message,fgColor,lineType)
