"""

Font.py

An attempt to provide a unified interfec to the fonts supported which are currently
openCV HERSHEY and BDF

"""
from Palette import *
from Constants import *
import BDF.Font as bdf
import OPENCV.Font as OpenCV
import cv2
from UtilLib import *


class Font():

    fontSize=10
    font=bdf.Font(fontSize) # temporary
    lineType=LINE_8   # Hershey fonts only

    xFudge = 2      # rendering offsets to avoid edge corruption with openCV Hershey
    yFudge=1

    def __init__(self,fontFace,fontSize):
        """

        :param int or str fontFace: For BDF fonts this should be "BDF" for Hershey it should be FONT_HERSHEY_??
        :param float fontSize: will be rounded to nearest integer
        """
        self.fontFace=fontFace          # only used by openCV
        self.fontSize=nearest(fontSize) # integer - no such thing as half a LED

        if type(fontFace) is str:
            assert fontFace.upper()=="BDF","Expected 'BDF' for font face"
            self.font = bdf.Font(fontSize)
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

