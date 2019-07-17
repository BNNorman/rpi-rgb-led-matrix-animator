"""
AntiAlias.py

Intended to be used when creating chains. AntiAlias information is added at that time.

This script contains the methods which can be used.

Anti-Alising works on the principle that virtual pixels may have fractional parts e.g. x=1.5,y=1.7 whereas
real pixels lie on integer boundaries. Hence, a virtual pixel with an X value of 1.5 lies half in the pixel at x=1 and
half in the real pixel at x=2. The brightness of each of the real pixels is adjusted to 0.5.
A pixel at x=1.6 lies 40% at x=1 and 60% at x=2 so the brightnesses are 0.4 and 0.6.

The Quad method, herein, recognises that such virtual pixels overlap 4 real pixels and so using the Quad method
quadruples the number of pixels in a chain. Thus the processing time for such a chain is 4xlonger than one without
anti-alising. Also, the method employed below does not, currently, allow for overlapping virtual pixels.

The Wu method is a simplified version of Wu's algorithm. Essentially, when drawing a line from pixel A to pixel B
the line will either be vertically inclined (slope>1) or horizontally inclined (slope <1). When drawing vertically
an anti-alias pixel is placed in the horiziontal plane. If the slope is +ve the extra pixel is placed above and if
the slope is negative it is placed below. A similar logic is applied to the drawing horizontally scenario.

"""

import numpy as np
from LEDAnimator.ExceptionErrors import *

class AntiAlias():
    """
    AntiAlias a class which encloses various methods for anti-aliasing LED chains.

    """
    def __init__(self):
        """
        initialise the arrays used to hold x,y and brightness factors
        """
        self.newV=[]    # brightness factor (V as in hsv)
        self.newX=[]    # pixel real x coordinate
        self.newY=[]    # pixel real y coordinates
        self.lastX=None # used to calculate the slope between adjacent pixels
        self.lastY=None # ditto

    def antiAlias(self,method=None,coordList=None):
        """
        converts coordList into an anti-aliased list using the method indicated.

        Real pixels lie on integer boundaries but virtual pixels do not.

        Anti-aliasing is done on a proportional basis for example; if X is 0.5 then half
         of the pixel is at 0 and half at 1 so 50% of the brightness will be at 0 and 50% at 1

        methods are:-
        "quad" or "q": each virtual pixel is treated as overlapping a group of 4 real pixels

        "wu" or "w": pairs of pixels are modified based on the current direction of drawing

        :param method: "wu", "quad"
        :param float or int tuple coordList: [(x0,y0),...(xn,yn)]
        """
        m=method.lower()[:1]

        if m=="q":  return self.quadAntiAlias(coordList)
        if m=="w":  return self.wuAntiAlias(coordList)

        raise NoSuchMethod("Unrecognised anti-alias method %s".format(method))


    def _addPixel(self, x, y,v):

        self.newV.append(v)
        self.newX.append(x)
        self.newY.append(y)

        self.lastX=x    # used by WU method
        self.lastY=y

    #########################################################################
    #
    # quadAntiAlias
    #
    # real pixels are of unit size (area=1)
    #
    # virtual pixels may overlap upto 4 real pixels
    # calculate the area of overlap and use that to control
    # real pixel brightness
    #
    # NOTE: may not work well since adjacent virtual pixels can share real pixels
    # also requires the ability to combine with previous real pixels - easier to
    # explain in a diagram.
    #
    ##########################################################################
    def _QuadOverlapArea(self, x1, y1, x2, y2):
        """
        calculates the area of overlap of a virtual pixel with it's real 3 neighbours
        the area corresponds to the required pixel brightness/luminosity/value.

        Each real pixel has a unit dimension hence the overlap area is 0->1.0 which can be directly
        used as the v component for HSV colours

        Used by the quad method

        :param x1:  float, pixel x coord
        :param y1:  float, pixel y coord
        :param x2:  int(x1) neighbor coords
        :param y2:  int(y1)
        :return area: area of overlap
        """
        w=min(x1+1,x2+1)-max(x1,x2)
        h=min(y1+1,y2+1)-max(y1,y2)

        self._addPixel(x2, y2, w * h)

    def quadAntiAlias(self, coordlist):
        """
        Run through the virtual pixel list calculating the overlaps and aportion the brightness accordingly.

        technique may have been invented by others I don't know.

        :param float [] coordlist: [(x0,y0,...(xn,yn)] virtual coordinates of pixels
        :return int [x],int [y], float [v]:
        """

        for (x1,y1) in coordlist:
            # each virtual pixel overlaps upto 4 real pixels
            self._QuadOverlapArea(x1, y1, int(x1), int(y1))
            self._QuadOverlapArea(x1, y1, int(x1 + 1), int(y1))
            self._QuadOverlapArea(x1, y1, int(x1), int(y1 + 1))
            self._QuadOverlapArea(x1, y1, int(x1 + 1), int(y1 + 1))

        return self.newX,self.newY,self.newV

    ######################################################################
    #
    # wu method
    #
    # adjacent horizontal real pixels are affected when virtual pixel moves
    # vertically and vice versa
    #
    #######################################################################

    def _wu_horizontal(self,x,y,slope=0):
        """
        Deal with situation where real pixel is moving horizontally
        :param float x: virtual pixel x
        :param float y: virtual pixel y
        :param float slope: >0 if moving left to right and <0 if moving right to left
        :return Nothing: adds the pixels to the output list
        """
        intX = int(x)
        fracY1 = y - int(y)
        fracY2 = 1 - fracY1

        # only add antialias pixels if they have some brightness

        if fracY1>0: self._addPixel(int(x), int(y), fracY1)

        if slope<0:
            # moving up
            if fracY2>0: self._addPixel(int(x), int(y + 1), fracY2)
        else:
            # moving down (default)
            if fracY2 > 0: self._addPixel(int(x), int(y - 1), fracY2)


    def _wu_vertical(self,x,y,slope):
        """
        deal with the situation where the real pixel is moving vertically
        :param float x: virtual pixel x
        :param float y: virtual pixel y
        :param float slope: >0 if moving up and <0 if moving down
        :return Nothing: adds the pixels to the output list
        """
        intY = int(y)
        fracX1 = x - int(x)
        fracX2 = 1 - fracX1

        # only add antialias pixels if they have some brightness
        if fracX1>0: self._addPixel(int(x), int(y), fracX1)
        if slope<0:
            # moving right
            if fracX2>0: self._addPixel(int(x+1), int(y), fracX2)
        else:
            # moving left (default)
            if fracX2 > 0: self._addPixel(int(x - 1), int(y), fracX2)


    def wuAntiAlias(self,coordlist):
        """
        The wu method depends on the direction of drawing between adjacent pixels.
        When moving horizontally anti-aliasing is done vertically and when moving
        vertically it is done horizontally.

        This algorithm creates two real pixels for each virtual pixel.

        The output is a list of integer x/y coordinates and a value list to use with the V component
        of HSV.

        :param float [x]: virtual pixel x
        :param float [y]: virtual pixel y
        :return int [x],int [y],float [V]: two pixels for the proce of one
        """

        for (x1,y1) in coordlist:

            if self.lastX is None and self.lastY is None:
                # assume drawing horizontally
                self._wu_horizontal(x1,y1,1)
            else:
                # moving vertically or horizontally?
                dx=float(x1) - self.lastX   # positive if moving left to right
                dy=float(y1) - self.lastY   # positive if moving down
                if abs(dy)>=abs(dx):
                    self._wu_vertical(x1,y1,dy)
                else:
                    self._wu_horizontal(x1,y1,dx)

        # wu done - return the lists
        return self.newX,self.newY,self.newV
