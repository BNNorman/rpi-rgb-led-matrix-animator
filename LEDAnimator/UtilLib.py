"""
UtilLib.py

Library with a variety of general purpose routines

"""

import numpy as np
import time

# alphaBlend sometimes throws a "RuntimeWarning: invalid value encountered in divide"
# but still carries on without throwing an exception, the next line keeps it quiet
np.seterr(divide='ignore', invalid='ignore')

import BDF
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

    # only include for debugging
    #assert fg.shape[-1] >= 4, "Foreground image must have an alpha channel"
    #assert bg.shape[-1] >= 4, "background image must have an alpha channel"

    # cannot blend images if shapes are not the same
    # normally this happens when moving one image over another so should be ok
    if fg.shape<>bg.shape:
        print "UtilLib.alphaBlend() images not the same shape. Ignored. fg", fg.shape, "bg", bg.shape
        return None

    # are we blending a single pixel? shape=4L, (len==1) otherwise like 10L,10L,4L (len==3)
    # if so don't check height or width
    if len(fg.shape)==3:
        # cannot blend images which have a zero width or height
        w,h=fg.shape[:2]
        if w==0 or h==0:
            print "UtilLib.alphaBlend() fg image has a zero dimension. Ignored"
            return None

        w,h=bg.shape[:2]
        if w==0 or h==0:
            print "UtilLib.alphaBlend() bg image has a zero dimension. Ignored"
            return None


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

    return out

def alphaBlendPixels(fg, bg):
    """
    Used internally by pasteWithAlphaAt() and alphaBlendPixel() but could be used externally
    blend two images based on the alpha channel. src (fg) and dst (bg) MUST be the same size.

    :param tuple fg: foreground rgba
    :param tuple bg: background rgba
    :return tuple: rgba blended pixel
    """
    fg=[i/255.0 for i in fg]
    bg=[i/255.0 for i in bg]

    out_a = fg[ALPHA] + bg[ALPHA] * (1.0 - fg[ALPHA])

    # sometimes throws a "RuntimeWarning: invalid value encountered in divide"
    # but still carries on without throwing an exception
    out_rgb=[0,0,0]
    out_rgb[0] = (fg[0] * fg[ALPHA]+ bg[0] * bg[ALPHA] * (1.0 - fg[ALPHA])) / out_a
    out_rgb[1] = (fg[1] * fg[ALPHA]+ bg[1] * bg[ALPHA] * (1.0 - fg[ALPHA])) / out_a
    out_rgb[2] = (fg[2] * fg[ALPHA]+ bg[2] * bg[ALPHA] * (1.0 - fg[ALPHA])) / out_a

    return (out_rgb[0]*255,out_rgb[1]*255,out_rgb[2]*255,out_a*255)

def alphaBlendPixel(fg, bg):
    """
    blends two colors based on alpha.

    fg and bg can be numpy ndarrays or single color tuples.

    This function routes the args to the required routine

    :param tuple or ndarray fg: [(rgba)...] in Pixel colour order
    :param tuple or ndarray bg: [(rgbsa)...] in pixel colour order
    :return tuple or ndarray: alpha blended output
    """
    # convert colors to single colour arrays if not already arrays
    # this change reduced the drawChainLayerOnLayerBuffer code time by .0003 secs
    if type(fg) is tuple:
        return alphaBlendPixels(fg, bg)
    else:
        return alphaBlend(fg,bg)

def pasteWithAlphaAt(bg, bx, by, fg):
    """
    Pastes fg into bg using alpha channel.

    If fg does not overlap does nothing just returns the next X position (bx)

    If fg is pasted into bg, returns the next Z position - useful
    for butting images together like when drawing text glyphs

    :param numpy ndarray bg: background image
    :param float bx: coordinate of top left corner for fg on bg
    :param float by: coordinate of top left corner for fg on bg
    :param numpy ndarray fg: image to paste into bg
    :return int : next x position (used for character strings)
    """

    # ignore if there's no foreground image
    if fg is None:
        #print "UtilLib.pasteWithAlpha() fg is None"
        return bx

    bx0,by0=nearest(bx),nearest(by)

    h,w=fg.shape[:2]

    # get the slice of the fg image that fits within the bg image at bx,by
    fgROI,bgROI=getOverlapSlices(bg,bx0,by0,fg)

    # if None don't bother doing anything
    if fgROI is None or bgROI is None:
        #print "UtilLib.pasteWithAlpha() ROI is None,bx,by=",bx,by,"fg shape=",fg.shape
        return bx

    blend=alphaBlend(fgROI,bgROI)

    if blend is None:
        #print "UtilLib.pasteWithAlpha() Blend is None"
        return bx

    # copy blend output to background
    bgROI[:,:,:]=blend[:,:,:]

    #cv2.imshow("blend",blend)

    h,w=fg.shape[:2]

    # value used fior font rendering, ignored at other times
    return bx+w


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

def getOverlapSlices(bg,fx0,fy0,fg):
    """
    returns the slices of bg and fg which overlap

    Since the background image is allways at 0,0 the coordinates will be within the background image

    :param numpy ndarray bg: background image
    :param float or int x: x cordinate of fg within bg
    :param float or int y: y coordinate of fg within bg
    :param numpy ndarray fg: foreground image
    :return: foregroundimage slice,background image slice
    """

    # get rectangle coords for the foreground image
    fh,fw=fg.shape[:2]
    fx1=fx0+fw
    fy1=fy0+fh

    trap=True if fw>200 else False

    # background image is always at 0,0
    bh,bw=bg.shape[:2]
    bx0,by0=0,0
    bx1=bw
    by1=bh

    # make sure fg & bg actually overlap, if not there are no slices
    if (fx0>bx1) or (fy0>by1) or (fx1<0) or (fy1<0):
        return None,None

    # get intersect coords for background slice
    bsx0=max(fx0,bx0)
    bsx1=min(fx1,bx1)
    bsy0=max(fy0,by0)
    bsy1=min(fy1,by1)

    # check we have a valid slice by calculating its area
    if (bsx1-bsx0)*(bsy1-bsy0)==0:
        return None,None

    # set the background slice
    bgSlice=bg[bsy0:bsy1,bsx0:bsx1]

    # deal with fg images which hang over the left or top edges of bg
    if fx0<0:
        # foreground slice is offset into the foreground image
        fsx0=abs(fx0)
        fsx1=fsx0+bsx1-bsx0
    else:
        fsx0=0
        fsx1=bsx1-bsx0

    if fy0<0:
        # foreground slice protrudes above the background
        fsy0=abs(fy0)
        fsy1=fsy0+bsy1-bsy0
    else:
        fsy0=0
        fsy1=bsy1-bsy0

    # ignore if the foreground slice has zero area
    if (fsx1-fsx0)*(fsy1-fsy0)==0:
        return None,None

    fgSlice=fg[fsy0:fsy1,fsx0:fsx1]


    return fgSlice,bgSlice

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

def channelSwap(color):
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
