
##########################################################
#
# Methods for creating xyLists for chains programmatically
#
#
##########################################################

import math

def makeRect(posX,posY,w,h,fillMode=None):
    """
    creates xy coordinate list for a rectangular chain.
    The rectangle can be filled vertically or horizontally so that an
    animation would run left to right or top to bottom
    :param posX: top left origin
    :param posY: top left origin
    :param w: int width
    :param h: int height
    :param fillMode: "V","H", "B" or None (default)
    "V" causes the shape to be created using vertical chains left to right
    "H" causes the shape to be created using horizontal chains top to bottom
    "B" causes the shape to be created using concentric chains

    :return: python list of XY coordinates

    """

    xyList=[]

    fillMode=fillMode.upper()[:1]

    if fillMode=="V":
        # fill by vertical columns
        for x in range(w):
            for y in range(h):
                xyList.append((posX+x,posY+y))
    elif fillMode=="H":
        # fill by horizontal rows
        for y in range(h):
            for x in range(w):
                xyList.append((posX+x,posY+y))
    elif fillMode=="B":
        # fill with outlines - can give whizzy collapsing box animations
        while w>0 and h>0:
            for x in range(w):
                # left to right
                xyList.append((posX + x, posY))
            # right side down
            for y in range(h):
                # right hand top to bottom
                xyList.append((posX + w, posY + y))
            for x in range(w):
                # far right to left
                xyList.append((posX + w - x, posY + h))
            for y in range(h):
                # left bottom to top
                xyList.append((posX, posY + h - y))
            # reduce the rectangle shape

            posX=posX+1 # move top left corner down and right 1 pixel
            posY=posY+1
            w=w-2       # posX and posY change by 1 so width/height reduces by 2
            h=h-2
    else:
        # default - outline only
        # start at top left
        for x in range(w):
            # left to right
            xyList.append((posX + x, posY))
        # right side down
        for y in range(h):
            # right hand top to bottom
            xyList.append((posX + w, posY+y))
        for x in range(w):
            # far right to left
            xyList.append((posX + w - x, posY+h))
        for y in range(h):
            # left bottom to top
            xyList.append((posX, posY + h -y))

    return xyList

def makeCircle(cx,cy,r):
    """
    creates a hollow clockwise circular shape

    :param cx:  circle centre X
    :param cy: circle centre Y
    :param r: circle radius
    :return: a list of coordinates for the hollow circle
    """
    # just the clockwise circumference starting at (-r,0)
    # using r^2=x^2+y^2
    # create the presized list and fill it in from both ends

    xyList=[]

    r=int(round(r,0))

    # do -90 to +90
    for x in range(-r,+r):
        y=int(round(math.sqrt(r*r-x*x),0))
        xyList.append((cx+x,cy-y))
    # now do +90 to -90
    for x in range(+r,-r,-1):
        y=int(round(math.sqrt(r*r-x*x),0))
        xyList.append((cx+x,cy+y))
    return xyList

def makeDisc(cx,cy,r):
    """
    creates a disc comprising of concentric circles filled clockwise.
    calls on makeCircle to create the infill

    :param cx: disc centre X
    :param cy: disc centre Y
    :param r: disk outer radius
    :return: python list of coordinate pairs
    """
    # clockwise concentrically filled circle
    xyList = []
    for rad in range(int(round(r,0)),0,-1):
       xyList=xyList+makeCircle(cx,cy,rad)
    return xyList

def makeLine(x1,y1,x2,y2):
    """
    creates a line between two points (x1,y1) and (x2,y2)
    :param x1: start coordinate X
    :param y1:
    :param x2: end coordinate Y
    :param y2:
    :return:
    """
    xyList=[]
    slope=float(y2-y1)/float(x2-x1)
    for x in range(int(round(x2-x1,0)+1)): # range stops 1 short
        y=round(y1+slope*x,0)
        xyList.append((x1+x,y))
    return xyList
