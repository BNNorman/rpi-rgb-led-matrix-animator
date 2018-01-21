'''
Chain.py

A chain is a sequence of XY coordinates representing the position of LEDs in a string which can form any shape.
It is akin to a LED strip and animated in a similar fashion.

Each pixel is stored as a colour using the hsv colourspace (HSVA) plus an alpha component.

The utilities Chain Maker and Text Chain Maker provide a means to create chains to ustilise in this program.

Also, regular chain shapes can be created using the methods in Helpers/Chains

The pixels in chains may be anti-aliased using one of the methods in Helpers/AntiAlias.py.

The methods are selected by passing the parameter antiAliasMethod=<method> as a chain creation parameter in the main.py
script. Example:


    from LEDAnimator import ChainAnimations, Palette, Animator,
    from LEDAnimator.Chain import Chain

    chain=Chain(xyList,antiAliasMethod="wu")

    A= Animator.Animator(fps=FPS,debug=True)

    A.addAnimation(chain=Chain(DAF_D,antiAliasMethod="wu"),seq=DAF_D_SEQ)

if the antiAliasMethod is not specified anti-aliasing does not take place.

'''

import numpy as np
from LEDAnimator.Colors import *
import colorsys
from matplotlib.colors import *

import Helpers.AntiAlias as AA

##########################################################
#
# Chain class
#
##########################################################

class Chain():
    """
    A chain is a sequence of LEDs. The sequence can be hand generated (ugh) or
    you can use the built in functions to create geometric shapes or the utilities
    to create chains from SVG images or text strings

    XY coords are kept separate from the pixel data so that it is possible to shift the pixel colours
    without affecting the coordinates

    """
    x=None          # 1D numpy array
    y=None          # 1D numpy array
    alias=None      # 1D numpy array, brightness multiplier
    hsv=None        # 5D numpy array H,S,V,A,AA (anti-alias)
    curPos=0        # pointer to a given LED
    lenChain=0      # length of the chain
    brightness=1.0  # brightness multiplier for the whole chain
    alpha=1.0       # overall chain transparency - useful for fade out/in
    AAmethod=None   # which antiAlias method to use
    debug=False

    def __init__(self,xyList,antiAliasMethod=None):
        """
        creates a chain object from a python list
        
        :param xyList: a python xy pair list like [[x0,y0],[x1,y1],...[xn,yn]]
        """
        assert type(xyList) is list,"xyList needs to be a list of LED coordinates [(x0,y0),(x1,y1),...(xn,yn)]"

        self.AAmethod=antiAliasMethod

        if self.AAmethod is not None:
            a=AA.AntiAlias()
            x,y,v=a.antiAlias(self.AAmethod,xyList)
            self.x = np.array(x)
            self.y = np.array(y)
            self.alias=np.array(v)
            self.hsv = np.zeros((len(x), 5), dtype=np.float)
            self.hsv[...,ALIAS] = v  # whatever the AA routine chooses
        else:
            # split the xyList into two
            xList,yList=zip(*xyList)
            self.x=np.array(xList)
            self.y=np.array(yList)
            self.alias=np.array(xList)
            self.hsv = np.zeros((len(xList), 5), dtype=np.float)
            self.hsv[:,ALIAS] = 1.0  # brightness or alpha multiplier
            self.hsv[:,ALPHA]=0.0    # transparent

        self.lenChain=len(xyList)
        self.curPos=0


    def adjustPixel(self,pixelData):
        """
        correct the pixel brightness based on chain brightness and anti-alias factor
        :param tuple pixelData: (h,s,v,a,aa)
        :return:
        """
        h, s, v, a, aa=pixelData
        # anti alias (aa) affects V
        # brightness affects s and v
        v=v*aa*self.brightness
        s=s*self.brightness
        a=a*self.alpha
        return h,s,v,a


    def getCurPos(self):
        """
        returns the current LED pointer (list index)
        :return: int current insertion position
        """
        return self.curPos

    def setCurPos(self,pos):
        """
        sets the current LED insertion position
        :param int pos: LED index - wraps to length of chain
        :return Nothing:
        """
        self.curPos=pos % self.lenChain

    def getNextLED(self,wrap=False):
        """
        returns the X/Y coordinates and colour of the pixel at the current position (CurPos)

        :param boolean wrap: if True getNextLed will wrap back to the start
        :return int x, int y, tuple (r,g,b,a): (x,y,(r,g,b,a))
        """
        p=self.curPos
        self.curPos=self.curPos+1
        if wrap:
            if self.curPos>=self.lenChain: self.curPos=0
        else:
            if self.curPos>self.lenChain: return None

        h,s,v,a=self.adjustPixel(self.hsv[p])
        r,g,b=colorsys.hsv_to_rgb(h,s,v)
        return self.x[p],self.y[p],r*255,g*255,b*255,a*255

    def setChainBrightness(self,brightness=1.0):
        """
        Sets the overall chain brightness.
        Allows the chain to be dimmed/brightened without affecting the relative
        brightness of the LEDs or the hues of the colours.
        :param float brightness: 0->1.0 - multiplier to use when getting pixels to display
        :return None: nothing
        """
        assert brightness>=0 and brightness<=1,"brightness factor should be in the range 0.0->1.0."

        # this is applied when we convert to rgb/bgr on output
        # human eye response is approximately a square law
        self.brightness=brightness*brightness


    def setChainAlpha(self,alpha=1.0):
        """
        Sets the overall chain alpha
        :param float brightness: float 0->1.0 - multiplier
        :return None: nothing
        """
        assert alpha>=0 and alpha<=1,"alpha factor should be in the range 0.0->1.0."

        # this is applied when we convert to rgb/bgr on output
        self.alpha=alpha

    def setPixelBrightness(self,n,brightness=1.0):
        """
        set the brightness of a pixel at index n.
        :param int n: pixel to change
        :param float brightness: float 0->1.0 multiplier
        :return None: self.hsv is adjusted
        """
        assert brightness>=0 and brightness<=1,"Brightness factor should be in the range 0.0->1.0."
        self.hsv[n,:HSV_V]*=brightness

    def setPixelAlpha(self, n, alpha=1.0):
        """
        sets the transparency of a pixel
        :param n: pixel to affect
        :param alpha: transparency level
        :return: nothing the alpha component of the pixel is changed.
        """
        self.hsv[n,ALPHA] = alpha

    def setPixel(self,n,colour,alpha=1.0):
        """
        sets the rgba values of a pixel at index n
        Throws a value error if n is not in the range 0->length of the chain
        :param n: pixel position in the chain
        :param colour: tuple rgba in pixel order
        :return: nothing the pixel value is set in the chain
        """
        # ignore out of bounds LEDs
        if n<0 or n>=self.lenChain:
            raise ValueError("chain.setPixel(n,colour,alpha) n ("+str(n)+") is out of range 0 to "+ str(self.lenChain-1))

        h,s,v=colorsys.rgb_to_hsv(colour[RGB_R]/255.0,colour[RGB_G]/255.0,colour[RGB_B]/255.0)

        # only affect channels upto but not including AntiAlias factor
        self.hsv[n,:ALIAS]=[h,s,v,colour[ALPHA]/255.0]


    def getPixelXY(self,n):
        """
        returns the X/Y coordinates of the pixel
        :param n:
        :return: x,y
        """
        if n < 0 or n >= self.lenChain:
            raise ValueError("chain.getPixelXY(n) n (" + str(n) + ") is out of range 0 to " + str(self.lenChain - 1))
        return self.x[n],self.y[n]

    def getPixel(self,n):
        """
        returns the coordinates and colour of the pixel
        :param n:
        :return: x,y,r,g,b,a
        """
        if n < 0 or n >= self.lenChain:
            raise ValueError("chain.getPixel(n) n (" + str(n) + ") is out of range 0 to " + str(self.lenChain - 1))

        h,s,v,a=self.adjustPixel(self.hsv[n])
        colour=colorsys.hsv_to_rgb(h,s,v)
        return self.x[n],self.y[n],colour[RGB_R]*255,colour[RGB_G]*255,colour[RGB_B]*255,a*255

    def getAllPixels(self):
        """
        get all the pixels and their x,y coordinates as numpy arrays
        These can then be placed on an output image

        The pixelsd are adjusted for alpha, brightness and Alias

        :return numpy ndarray x,numpy ndarray y,numpy ndarray colours: x,y,rgba
        """
        # we are going to mod the brightness of the output only
        # we don't want to change the stored pixels

        tmp=self.hsv.copy()
        tmp[...,HSV_V]*=tmp[...,ALIAS]*self.brightness
        tmp[...,ALPHA]*=self.alpha
        # use matplotlib to convert to rgb
        tmp[:, :3] = hsv_to_rgb(tmp[:, :3])  # only the HSV channels are used

        # map all values (incl alpha) from 0->1.0 to  0->255
        tmp[:,:4]*= 255.0

        if RGB_R <> 0:
            # swap channels
            tmp[[RGB_R, RGB_B]] = tmp[[RGB_B, RGB_R]]

        return self.x,self.y,tmp[:,:4]  # don't need the alias info


    def getLength(self):
        """
        returns the length of the chain
        :return: int - number of LEDs in the chain
        """
        return self.lenChain

    def setAllPixels(self,colour):
        """
        sets all pixels to the same rgb colour
        :param colour: tuple rgba in pixel order
        :return: nothing the whole chain is set to the same colour
        """
        r,g,b,a=colour[RGB_R]/255.0,colour[RGB_G]/255.0,colour[RGB_B]/255.0,colour[ALPHA]/255.0,
        h,s,v,=colorsys.rgb_to_hsv(r,g,b)
        # must not touch the AntiAlias value
        self.hsv[...,:ALIAS]=[h,s,v,a]   # ignore ALIAS channel

        #self.hsv[:, ALPHA] = a
        #self.hsv[:, HSV_H] = h
        #self.hsv[:, HSV_S] = s
        #self.hsv[:, HSV_V] = v


    def setAllPixelsRandom(self):
        """
        sets all pixels in the chain to a random colour
        :return: nothing the whole chain is set to random colours
        """
        h=self.lenChain
        self.hsv[:,ALPHA]=np.random.random(size=self.lenChain)
        self.hsv[:,HSV_H]=np.random.random(size=self.lenChain)
        self.hsv[:,HSV_V]=np.random.random(size=self.lenChain)
        self.hsv[:,HSV_S]=np.random.random(size=self.lenChain)

    def roll(self, steps=1):
        """
        Rotates the pixels such that the pixel at the head moves to the tail
        or the other way around if steps is negative. It does not affect coordinates.
        This allows animation effects such as comets and the KnightRider
        to be achieved very simply
        :param steps: -/+ number of steps to roll
        :return: nothing the pixel array is rolled
        """
        self.hsv = np.roll(self.hsv, steps, axis=0)

    def shiftRight(self,steps=1,fill=Black.getPixelColor()):
        """
        shift pixels towards the end of the chain and fill
        :param steps: number of pixels to shift right
        :param fill: color to use for backfill default is Black
        :return: nothing, the chain is shifted right
        """
        self.hsv = np.roll(self.hsv, steps, axis=0)
        if fill is not None:
            r,g,b,a=fill
            h,s,v=colorsys.rgb_to_hsv(r/255.0,g/255.0,b/255.0)
            self.hsv[:steps,:ALIAS]=[h,s,v,a/255.0]

    def shiftLeft(self,steps=1,fill=(0,0,0,255)):
        """
        shift pixels left (towards start of chain) and fill if any
        :param steps: number of places to shift
        :return: nothing the pixel array is
        """
        self.hsv = np.roll(self.hsv, -steps, axis=0)
        if fill is not None:
            r, g, b, a = fill
            h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            self.hsv[-steps:,:ALIAS] = [h, s, v, a / 255.0]

    def shiftIn(self,steps=1,fill=(0,0,0,255)):
        """
        brings pixels in from right and left
        :param steps:
        :return:
        """
        midPoint = int(self.lenChain / 2)

        self.hsv[:midPoint] = np.roll(self.hsv[:midPoint], steps, axis=0)
        self.hsv[midPoint:] = np.roll(self.hsv[midPoint:], -steps, axis=0)

        if fill is not None:
            r, g, b, a = fill
            h, s,v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            a=a/255.0
            self.hsv[:steps,:ALIAS] = [h,s,v,a]
            self.hsv[-steps:,:ALIAS] = [h,s,v,a]

    def shiftOut(self, steps=1,fill=(0,0,0,255)):
        """
        moves pixels from  centre outwards
        :param steps:
        :return:
        """
        midPoint = int(self.lenChain / 2)

        self.hsv[:midPoint] = np.roll(self.hsv[:midPoint], -steps, axis=0)
        self.hsv[midPoint:] = np.roll(self.hsv[midPoint:], steps, axis=0)
        if fill is not None:
            r, g, b, a = fill

            h, s,v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            a = a / 255.0
            #    Dont mess with the AntiAliasing
            self.hsv[midPoint-steps:midPoint,:ALIAS] = [h,s,v,a]
            self.hsv[midPoint:midPoint+steps,:ALIAS] = [h,s,v,a]

