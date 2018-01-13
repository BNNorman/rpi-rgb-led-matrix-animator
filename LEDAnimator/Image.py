"""
Image.py

An object to declare foreground or background images easily in one of two ways:-

ThisImage=Image(imagePath="..",scaleMode="F",alignMode=("C","C"),Xpos=10,Ypos=15)

or

ThisImage=Image()
ThisImage.imagePath=".."
ThisImage.scaleMode="F"
ThisImage.alignMode=("C","C")

Images can thenm be passed to the animations using

fgImage=ThisImage or bgImage=ThisImage


"""

import NumpyImage
from Constants import *

class Image():
    """
    The image class is used to pass image information into an animation. It
    is used for both foreground and background images.

    The image itself, when loaded, is a NumpyImage object. This class could be extended to hide the
    calls to the NumpyImage object methods if you wish.

    Parameters:-

    transMatrix=[a,b,c,d,e,f]
        the parameters to use in a 2x3 affine matrix [[a,b,c][d,e,f]]. Eventually assed to openCV warpAffine()

    Xpos,Ypos
        the position on the Panel at which this image is rendered. To scroll images just change Xpos and Ypos.
        Use floating point - the position is rounded to the nearest pixel when rendered

    imagePath
        operating system dependant path to the image on disk.

    alignMode(horiz,vert)
        for stationary images - how to align the image on the Panel Horizontal can be Left,Center/Middle,Right
        and vertical can be Top,Middle/Center,Bottom. Only the first character is used and it is changed to upper
        case so "t" and "T" would both mean "Top" as would "Tarantula" - LOL

        Aligning an image to the horizontal centre and vertical middle of the LED panel could be done in any of these
        ways:-

        alignMode=("C","C") or alignMode=("M","M") or alignMode=("C","M") or alignmode=("M","C")

    scaleMode="mode"
        "F" means fit the image to the panel both horizontally and vertically. This may result in stretching in one
        dimension
        "H" means fit the image to the width of the panel. A landscape image would have space above or below or both
        depending on the alignMode. I have not tried portrait images with this mode.
        "V" means fit vertically. I have not tried landscape images with this mode.

    loadVisible
        If False the image will be loaded invisible (alpha=0). This is useful for FadeIn animations to avoid the
        initial flash seen when the image is loaded before the animation starts.
    """
    image=None          # NumpyImage
    transMatrix=None    # [a,b,c,d,e,f] affine matrix parameters
    Xpos=0              # position for rendering on the panel
    Ypos=0
    imagePath=None
    scaleMode="F"       # fit to panel
    alignMode=("C","C") # center on the panel
    debug=False
    loadVisible=True

    def __init__(self,**kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)


    def loadImage(self):
        """
        Not loaded when the object is created so that it doesn't delay start up.
        Should be called during animation reset() when first needed
        :return:
        """
        if self.debug: print "Image.loadImage() called for imagePath=",self.imagePath

        # already loaded?
        if self.image is not None:
            if self.debug: print "Image.loadImage() imagePath=",self.imagePath,"is already loaded"
            return

        if self.imagePath is not None:
            if self.debug: print "Image.loadImage() loadVisible=",self.loadVisible
            alpha=255 if self.loadVisible else 0
            self.image=NumpyImage.NumpyImage(imagePath=self.imagePath,alpha=alpha)
            assert self.image is not None,"Image.loadImage() FAILED for imagePath="+self.imagePath

    def getScaleMode(self):
        return self.scaleMode

    def getImagePath(self):
        return self.imagePath

    def getAlignMode(self):
        return self.alignMode

    def getTransMatrix(self):
        return self.transMatrix

    def getPosition(self):
        return self.Xpos,self.Ypos

    def setPosition(self,pos):
        self.Xpos,self.Ypos=pos

    def getImageData(self):
        if self.image is None: return None
        return self.image.getImageData()

    def getSize(self):
        if self.image is None:
            print "Image not loaded ",self.imagePath
            return 0,0
        else:
            return self.image.width,self.image.height

    def getWidth(self):
        if self.image is None:
            print "Image not loaded ",self.imagePath
            return 0
        else:
            return self.image.width

    def getHeight(self):
        if self.image is None:
            print "Image not loaded ", self.imagePath
            return 0
        else:
            return self.image.height

    def countVisible(self):
        return self.image.countVisible()

    #####################################################
    #
    # convenience functions to hide mechanisms and
    # more importantly, reduce typing
    #
    #####################################################

    def resizeByFactor(self,factor):
        if self.image is None: return
        self.image.resizeByFactor(factor)

    def rollWindow(self,window,direction,speed):
        if self.image is None: return
        self.image.rollWindow(window,direction,speed)

    def adjustSat(self,satChange):
        if self.image is None: return
        self.image.adjustSat(satChange)

    def adjustHue(self,hueChange):
        if self.image is None: return
        self.image.adjustHue(hueChange)

    def copyWindow(self,window):
        if self.image is None: return
        self.image.copyWindow(window)

    def clearWindow(self,window):
        if self.image is None: return
        self.image.clearWindow(window)

    def fade(self,percent):
        if self.image is None: return
        self.image.fade(percent)

    def transform(self):
        if self.image is None: return
        self.image.transform(self.transMatrix)

    def blur(self,sigma):
        if self.image is None: return
        self.image.blur(sigma)

    def fillAlpha(self,alpha):
        """
        sets the alpha for the whole image
        :param int alpha: range 0-255
        :return None:
        """
        if self.image is None: return
        self.image.fillAlpha(alpha)

    def setPixelAlpha(self,x,y,alpha):
        if self.image is None: return
        self.image.setPixelAlpha(x,y,alpha)

    def setPixel(self,x,y,color):
        if self.image is None: return
        self.image.setPixel(x,y,color)

    def fill(self,color):
        if self.image is None: return
        self.image.fill(color)

    def clear(self):
        if self.image is None: return
        self.image.clear()

    def reset(self):
        if self.image is None: return
        self.image.resetImage()

    def fillWindowRandom(self, color):
        if self.image is None: return
        self.image.fillWindowRandom(color)

    def fillWindowAlpha(self, window, alpha=255):
        if self.image is None: return
        self.image.fillWindowAlpha(window,alpha)

    def drawPolyLine(self,pts, color, isClosed, thickness=1, lineType=LINE_8):
        if self.image is None: return
        self.image.cvPolyLines(pts, color, isClosed, thickness, lineType)

    def drawPolyLines(self, pts, palette, isClosed=False, thickness=1, lineType=cv2.LINE_AA):
        """
        draw a poly line list with each segment in a different color

        :param list pts: a python array [[x0,y0],[x1,y1], ..[xn,yn]]
        :param Palette palette: list of colours to use for separate segments
        :param bool isClosed: boolean default is False
        :param int thickness: int line tickness - default 1
        :param int lineType: line type (see opencv docs - defaults to LINE_AA - anti-aliased)
        :return: self.out has the shape drawn on it
        """

        if self.image is None: return

        # invisible - don't bother
        if thickness == 0: return

        startPos = None
        lastPos = None
        thisPos = None

        for thisPos in pts:
            if startPos is None:
                startPos = thisPos
                lastPos = startPos
            else:
                color = palette.getNextEntry().getPixelColor()
                self.drawLine(lastPos, thisPos, color, thickness, lineType)
                lastPos = thisPos

        if isClosed:
            color = palette.getNextEntry().getPixelColor()
            self.drawLine(lastPos, startPos, color, thickness, lineType)

    def drawLine(self,fromXY, toXY, color, thickness=1, lineType=LINE_8):
        if self.image is None: return
        self.image.cvLine(fromXY, toXY, color, thickness, lineType)

    def drawRectangle(self,pt1, pt2, color, thickness=1, lineType=LINE_8):
        if self.image is None: return
        self.image.cvRectangle(pt1, pt2, color, thickness, lineType)

    def drawEllipse(self,centre, axes, angle, startAngle, endAngle, color, thickness=1, lineType=LINE_AA):
        if self.image is None: return
        self.image.cvEllipse(centre, axes, angle, startAngle, endAngle, color, thickness, lineType)

    def drawCircle(self,pos,radius,color,thickness=1,lineType=LINE_AA):
        if self.image is None: return
        self.image.cvCircle(pos, radius, color, thickness,lineType)