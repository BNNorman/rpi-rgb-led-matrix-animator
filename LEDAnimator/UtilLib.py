"""
UtilLib.py

Library with a variety of general purpose routines

"""

import numpy as np

# alphaBlend sometimes throws a "RuntimeWarning: invalid value encountered in divide"
# but still carries on without throwing an exception, the next line keeps it quiet
np.seterr(divide='ignore', invalid='ignore')

import BDF
#from BDF import Font as bdf
from Constants import *
import cv2
import colorsys

def alphaBlend(fg, bg):
    """
    Used internally by pasteWithAlphaAt() and alphaBlendPixel() but could be used externally
    blend two images based on the alpha channel. src (fg) and dst (bg) MUST be the same size.

    :param numpy ndarray fg: foreground numpy image
    :param numpy ndarray bg: background numpy image
    :return: numpy ndarray blended images
    """
    assert fg.shape[-1] >= 4, "Foreground image must have an alpha channel"
    assert bg.shape[-1] >= 4, "background image must have an alpha channel"

    # cannot blend images if shapes are not the same
    # normally this happens when moving one image over another so should be ok
    if fg.shape<>bg.shape:
        #print "UtilLib.alphaBlend() images not the same shape. Ignored. fg", fg.shape, "bg", bg.shape
        return

    # are we blending a single pixel? shape=4L, (len==1) otherwise like 10L,10L,4L (len==3)
    # if so don't check height or width
    if len(fg.shape)==3:
        # cannot blend images which have a zero width or height
        w,h=fg.shape[:2]
        if w==0 or h==0:
            #print "UtilLib.alphaBlend() fg image has a zero dimension. Ignored"
            return

        w,h=bg.shape[:2]
        if w==0 or h==0:
            #print "UtilLib.alphaBlend() bg image has a zero dimension. Ignored"
            return


    src_rgb = fg[..., :3].astype(np.float32) / 255.0
    src_a = fg[..., 3].astype(np.float32) / 255.0
    dst_rgb = bg[..., :3].astype(np.float32) / 255.0
    dst_a = bg[..., 3].astype(np.float32) / 255.0

    out_a = src_a + dst_a * (1.0 - src_a)

    # sometimes throws a "RuntimeWarning: invalid value encountered in divide"
    # but still carries on without throwing an exception
    out_rgb = (src_rgb * src_a[..., None]
               + dst_rgb * dst_a[..., None] * (1.0 - src_a[..., None])) / out_a[..., None]

    out = np.zeros_like(bg)
    out[..., :3] = out_rgb * 255
    out[..., 3] = out_a * 255

    #print "UtilLib.alphaBlend() done."

    return out

def alphaBlendPixel(fg,bg):
    """
    blends two pixels based on alpha.

    :param tuple fg: (rgba) in Pixel colour order
    :param tuple bg: (rgbsa) in pixel colour order
    :return:
    """
    # convert colors to single colour arrays
    fg_arr=np.array(fg)
    bg_arr=np.array(bg)

    return alphaBlend(fg_arr,bg_arr)

def pasteWithAlphaAt(bg, bx, by, fg):
    """
    Pastes fg into bg using alpha channel.

    If fg does not overlap does nothing returns the next X position (bx)

    If fg is pasted into bg, returns the next Z position - useful
    for butting images together like when drawing text glyphs

    :param numpy ndarray bg: background image
    :param float bx: coordinate of top left corner for fg on bg
    :param float by: coordinate of top left corner for fg on bg
    :param numpy ndarray fg: image to paste into bg
    :return int or float: next x position (used for character strings)
    """
    assert fg is not None, "fg (foreground) image cannot be None."
    assert bg is not None, "bg (background) image cannot be None."
    assert type(fg) is np.ndarray, "Image must be a numpy.ndarray (image)"
    assert type(bg) is np.ndarray, "Image must be a numpy.ndarray (image)"

    bx,by=nearest(bx),nearest(by)

    #print "fg",fg.shape,"bg",bg.shape,"x,y",bx,by

    # get the slice of the fg image that fits within the bg image at bx,by
    fgROI=getOverlapCoords(bg,bx,by,fg)

    # if none don't bother doing anything
    if fgROI is None:
        #print "UtilLib.pasteWithAlphaAt()) ROI is None - ignored"
        return bx

    x0,y0,x1,y1=fgROI

    #print "utilLib.pasteWithAlphaAt() ROI=",x0,y0,x1,y1

    # the ROI is always within the bg image
    if bx<0: bx=0
    if by<0: by=0

    rw=x1-x0
    rh=y1-y0

    # if the ROI has no width or height don't bother
    if rw==0 or rh==0:
        #print "UtilLib.pasteWithAlphaAt()) zero size rw=",rw,"rh=",rh,"ignored"
        return bx

    # blend the background and foreground and put it back
    # into bg
    # both images must be the same size for alphaBlend

    # set the ROI
    F=fg[y0:y1, x0:x1]
    B=bg[by:by+rh, bx:bx + rw]

    blend=alphaBlend(F,B)
    if blend is None:
        #print "UtilLib,pasteWithAlphaAt() Blend is None"
        return bx

    # copy blend output to background
    #print "Shape bg",B.shape,"blend",blend.shape
    B[:,:,:]=blend[:,:,:]

    #print "UtilLib.pasteWithAlphaAt() finished"

    return bx+rw


def getActualBrightness(wanted):
    """
    Human preceived brightness follows, roughly, a square law. So, to get 50% brightness
    the LEDs need to be set at .5*.5 -> 25%

    Useful for smoothing Fade transitions.

    :param float wanted: wanted preceived brightness 0-100 %
    :return float: actual % level to use (0->100)
    """
    assert wanted>=0 and wanted<=100,"Wanted brightness should be in range 0 to 100%"

    return (wanted*wanted)/(10000.0)

def getOverlapCoords(bg,bx,by,fg):
    """
    returns the coords of the top left and bottom right of the area
    of fg placed at bx,by on bg or None if no overlap

    :param numpy ndarray bg: background image always at 0,0
    :param float or int bx: horizontal position of fg relative to bg
    :param float or int by: vertical position of fg relative to bg
    :param numpy ndarray fg: foreground image to place at bx,by
    :return None or tuple: None or (x0,y0,x1,y1) for fg
    """
    bh,bw=bg.shape[:2]
    fh,fw=fg.shape[:2]

    #print "UtilLib.getOverlapCoords() bg",bw,bh,"xy",bx,by,"fg",fw,fh

    # initialise slice coord values to fg

    sx0,sy0=0,0
    sx1,sy1=fw-1,fh-1

    # calc slice start coordinates
    if bx<0:
        sx0=abs(bx)
        bx=0

    if by<0:
        sy0=abs(by)
        by=0

    # calc slice end coords
    if bx+fw>bw:
        sx1=sx0+bw-bx-1    # zero based
    else:
        sx1=sx0+fw-1

    if by+fh>bh:
        sy1=sy0+bh-by-1
    else:
        sy1=sy0+fh-1

    if (sx1-sx0)==0 or (sy1-sy0)==0:
        #print "UtilLib.getOverlapCoords() Zero width or height overlap."
        return None

    #print "UtilLib.getOverlapCoords() returns sx0,sy0,sx1,sy1", sx0,sy0,sx1,sy1

    return sx0,sy0,sx1,sy1

#TODO rename as getSlice???
def getFgSlice(bg, x, y, fg):
    """
    Get the slice of fg which can be overlaid on to bg at x,y

    If fg fits wholly in bg returns fg otherwise the slice

    If fg does not lie within bg returns None

    :param numpy ndarray bg: background image
    :param float x: coordinates elative to bg
    :param float y:
    :param numpy ndarray fg: the image to overlay
    :return numpy ndarray: the sliced fg or None
    """
    coords=getOverlapCoords(bg,x,y,fg)

    if coords is None: return None

    x0,y0,x1,y1=coords
    # resolve for nearest pixel
    # slices MUST be integers
    x0 = nearest(x0)
    x1 = nearest(x1)
    y0 = nearest(y0)
    y1 = nearest(y1)

    return fg[y0:y1, x0:x1]

def nearest(n):
    """
    round up or down to nearest int returning an int

    Used for selecting the nearest pixel position.

    WARNING, this method is vectorised to handle a numpy array by NumpyImage

    :param a number or array of numbers: virtual pixel position (x or y)
    :return int: nearest integer (round up/down)
    """
    if type(n) is None: return
    n=float(n) # make sure n is a float
    return int(round(n,0))

def pasteOpaqueAt( bg, x, y, im):
    """
    paste im into bg overwriting whatever was there
    :param bg: numpy image
    :param x:  top left corner to paste at
    :param y:
    :param im: image to paste in
    :return:
    """
    h, w = im.shape[:2]
    if h * w == 0: return  # zero sized image - ignore it
    x, y = nearest(x), nearest(y)

    bg[y:y + h, x:x + w, :3] = im[:, :, :3]
    return bg

def insideRect(x,y,x0,y0,x1,y1):
    """
    Return True if x,y lies within the rectangle bounded by two points (x0,y0) and (x1,y1).
    Used to detect if movement lies within a start and end position
    :param x: The point coordinates
    :param y:
    :param x0: 1st corner coordinates
    :param y0:
    :param x1: opposite corner coordinates
    :param y1:
    :return: True if (x,y) is inside the rectanglar shape
    """
    if x >= min(x0, x1) and x <= max(x0, x1) and y >= min(y0, y1) and y <= max(y0, y1):
        return True
    return False

def insideWindow(x,y,window):
    """
    Retuirns True if point (x,y) lies within the window (x,y,w,h)
    :param x: The point of interest
    :param y:
    :param window: (x,y,w,h)
    :return: True if point is within the window or False
    """
    x0,y0,w,h=window
    return insideRect(x,y,x0,y0,x0+w,y0+h)


def addParentToSysPath(atStart=True):
    """
    add the parent folder to the sys.path. If the folder is already included does nothing.

    :param bool atStart: True means add to the start of path otherwise append
    :return None: sys.path is updated
    """
    import sys
    parent = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

    if not parent in sys.path:

        if atStart:
            sys.path.insert(0, parent)
        else:
            sys.path.append(parent)


def addFolderToParentPath(folder):
    """
    add the folder to the parent folder path.

    :param str folder: name of folder to add
    :return str: the full path to the folder
    """

    parent = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

    return os.path.join(parent,folder)

def uint8(n):
    """
    convert a float from range 0->1.0 to 0->255 (int)
    :param float n:
    :return int: n m,apped to 0->255 range
    """
    return int(round(n*255, 0))

def float8(n):
    """
    map n from 0->255 to 0->1.0 range
    :param in n: range 0 to 255
    :return float: n mapped to 0->1.0
    """
    # colorsys uses float values ranging 0.0->1.0
    # this scales a LED value and returns a float
    return n / 255.0

def adjustTupleBrightnessAndAlpha(color=None,brightness=1.0,alpha=1.0):
    """
    Given a colour expressed as a tuple e.g (r,g,b,a) adjust the brightness and alpha

    Mainly used where a colour is taken from a palette

    :param tuple color: e.g. (r,g,b,a) in Pixel color order
    :param float brightness: 0->1.0
    :param float alpha: 0->1.0
    :return:
    """
    assert color is not None,"Color cannot be None"
    assert brightness >= 0 and brightness <= 1, "brightness must be in range 0->1.0"
    assert alpha >= 0 and alpha <= 1, "alpha must be in range 0->1.0"

    if brightness==1:
        a, b, c, d = color
        return (a,b,c,int(alpha*255))    # order doesn't matter if just adjusting alpha

    # ok, brightness complicates matters
    h,s,v=colorsys.rgb_to_hsv(color[RGB_R]/255.0,color[RGB_G]/255.0,color[RGB_B]/255.0)
    v=v*brightness
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    color = (uint8(r), uint8(g), uint8(b), uint8(alpha))

    return (color[RGB_R], color[RGB_G], color[RGB_B], color[ALPHA])