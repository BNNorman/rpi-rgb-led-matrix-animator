# NumpyImage.py
#
# images are handled as Numpy RGBA arrays so that they can be
# manipulated before being output to either the simulator or actual RGB matrix
#
#
# note: matplotlib hsv_to_rgb etc function expect an array of values in the range 0-1.0 not 0-255
# hence some scaling has to take place on output
#
# Images are loaded via the ImageCache module so re-using an image is faster as it doesn't need to be reloaded.
# The original image is called rgba_orig.
# If the image is scale is changed it is always done from the rgba_orig to keep the highest quality.
# the scaled image is called rgba_cached and is copied to the output image called 'out'
# this way we can undo changes to out by copying rgba_cached back and since rgba_cached is likely to be
# smaller than rgba_orig the operation is faster.
# Also, when adjusting the brightness etc of the image rgba_cached is used as the source. This means we can always
# get back to the original image (Undo brightness or alpha changes)
#
#
import math
from scipy import ndimage
from ExceptionErrors import *
import ImageCache
from LEDAnimator.UtilLib import *
import cv2

# required to support PIL image formats for hzeller drivers
# TODO - find out how to do this with numpy alone
try:
    from PIL import ImageTk,Image
except:
    try:
        # on my Raspian lite they are here
        from PILcompat import ImageTk,Image
    except:
        raise MissingImageTk



# numpy images allow for fast(ish) image manipulation

class NumpyImage():
    """
    Class to encapsulate image handling.

    Images are loaded via the image cache to reduce the memory footprint when images are re-used.

    The original mimage is stored as rgba_orig - all shape transform operations such as scaling, rotation etc
    use this as the starting point and generate a resulting rgba_cached image.

    rgba_cached is used as the base for simpler manipulations such as colour changes which are then
    copied to the final output image (out). In this was brightness changes can be made more quickly than
    messing with a HD image every time and allows such changes to be undone quickly (brightness is a destructive
    change - consider setting it to zero - the resulting rgb is 0,0,0 - you can never get back without caching.

    NumpyImage, as it's name implies, uses numpy images as the core format.

    The colour channel order is determined by the RGB_R setting in Constants.py. This allows the code to use either RGB or BGR images.
    The LED RGB Matrix simulator uses openCV imshow to display the simulated matrix.imshow uses BGR pixel ordering but the real matrix uses RGB.

    For testing on a PC RGB_R is set to 2 - meaning it is the third colour in the Pixel tuple (b,g,r)


    """

    classname = "NumpyImage"    # for debug messages

    rgba_orig=None      # original image, original size - all shape transforms start from here
    rgba_cached=None    # original image after any shape transforms
    out=None            # output image initially copied from rgba_cached
                        # transforms reset this back to the start
    height=0            # current out image width
    width=0             # current out image width
    imagePath=None
    image=None          # used to create NumpyImage from a numpy image
    debug=False
    alpha=255           # used when NumbyImage is created from dimensions
    fillColor=None      # (r,g,b,a)


    def getImageData(self):
        return self.out

    def resetImage(self):
        """
        used to undo ALL image editing changes to the final (out) image.

        Called after any shape transforms - so be careful as any colour changes will be lost

        :return: self.out <- rgba_cached
        """
        self.out = self.rgba_cached.copy()
        self.height, self.width = self.out.shape[:2]

    def __init__(self,**kwargs):
        """
        loads or creates an image. If the imagePath is specified it loads an image
        and caches it via the ImageCache.py module to save time if the image is reused.

        Otherwise if height and width are specified it creates an empty image which is not cached.

        :param kwargs: imagePath=<path to image> or height=<int>, width=<int> alpha=<value 0-255>
        """
        for key,value in kwargs.iteritems():
            setattr(self,key,value)

        # load the RGBA image - we keep this unchanged so we can work
        # forward from it if necessary (e.g. when changing hue/brightness/saturation)
        # ImageCache validates the loading of the image

        if self.imagePath is not None:
            # ImageCache adds an Alpha channel if needed
            self.rgba_orig = ImageCache.loadImage(self.imagePath)
        elif self.image is not None:
            #TODO - untested
            #print "create a NumpyImage from a numpy image shaped like",self.image.shape
            assert type(self.image) is np.ndarray,"NumpyImage.__initi__() image parameter should be a numpy image (" \
                                                  "ndarray)."
            self.rgba_orig=self.image.copy()
            self.rgba_orig[...,ALPHA]=self.alpha    # set by caller

        else:
            assert self.height>0 and self.width>0,"NumpyImage.__init__() no imagePath and width/height is zero."

            self.rgba_orig=np.zeros([nearest(self.height),nearest(self.width),4],dtype=np.uint8)
            self.rgba_orig[...,ALPHA]=self.alpha    # set by caller
            if self.fillColor is not None: self.fill(self.fillColor)


        # if the rgba image is transformed rgba_cached and out are re-created
        # this ensures we don't degrade the image with transforms
        # add an alpha channel if there isn't one
        h,w,c=self.rgba_orig.shape
        if c < 4:
            alpha = np.full([h, w, 1], 255, dtype=np.uint8)  # opaquee
            self.rgba_orig = np.concatenate((self.rgba_orig, alpha), axis=2)

        self.rgba_cached=self.rgba_orig.copy()
        self.resetImage()

    def alignImage(self, alignMode,area):
        """
        Returns positioning coords for this image within a given area according to the alignMode setting.


        :param tuple alignMode: ( horizontal align mode,vertical align mode)
            horizontal align mode can be L(eft),R(ight),C(enter), M(iddle)
            vertical align mode can be T(op),B(ottom),C(enter) or M(iddle)
        :param tuple area: (float width,float height)
        :return tuple : float x,float y : coords to place the image at within the given area
        :raises InvalidMode: if vertical mode is not T,C,M or B and if horizontal mode is not L,C,M or R
        """
        if alignMode is None: return 0, 0

        ih, iw = self.height, self.width

        aw, ah =area
        v, h = alignMode

        assert type(v) is str, "NumpyImage.alignImage() Vertical alignMode character should be a string."
        assert type(h) is str, "NumpyImage.alignImage() Horizontal alingMode character should be a string."

        v = v.upper()
        h = h.upper()

        v = v[:1]
        h = h[:1]

        # calc vertical position
        if v == "T":
            Ypos = 0
        elif v == "C" or v == "M":
            Ypos = round((ah - ih) / 2.0, 0)
        elif v == "B":
            Ypos = ah - ih
        else:
            raise InvalidMode("NumpyImage.alignImage() Invalid vertical alignment mode", alignMode,
                              "should be T,C,M or B")

        if h == "L":
            Xpos = 0
        elif h == "C" or h == "M":  # center or middle treated the same
            Xpos = round((aw - iw) / 2.0, 0)
        elif h == "R":
            Xpos = aw - iw
        else:
            raise InvalidMode("NumpyImage.alignImage() Invalid horizontal alignment mode", alignMode,
                              "should be L,C,M or R")

        return Xpos, Ypos

    def countVisible(self):
        tmp=self.out[ALPHA]
        return np.count_nonzero(tmp) # alpha channel)


    # TODO decide if this is needed/used
    def copy(self):
        """
        takes a copy of the rgba_orig image
        :return: rgba_orig
        """
        return self.rgba_orig.copy()

    def fill(self,color=None):
        """
        Fill the entire final image with a given pixel color.
        If the color is None just makes the image transparent

        :param tuple color: the rgba values in pixel order
        :return: nothing, self.out is filled or made transparent
        """

        if color is None:
            # just make it transparent
            self.out[...,ALPHA]=0
        else:
            assert len(color) == 4, "Fill colour must have 4 channels got " + str(color)
            self.out[:,:]=[color]

    def fillAlpha(self,alpha=255):
        """
        Fill the alpha channel for the entire image with a given value- defaults to opaque
        :param alpha : 0-255 alpha value, default 255
        :return: nothing, self.out is moddified
        """
        self.out[...,ALPHA]=alpha

    def clearWindow(self,window):
        """
        Fill the window with the default color see filLWindow()

        :param tuple window: (x,y,w,h)
        :return: the final image is made transparent
        """
        self.fillWindow(window)

    def fillWindow(self,window,color=None):
        """
        fills a window of this image with the given color

        if the fill color is None the window is just made transparent.

        :param tuple window: (x,y,w,h)
        :param tuple color: rgba in Pixel order
        :return the image window is filled:
        """

        X0, Y0, X1, Y1 = self.getViewport(window)
        if color is None:
            # just make the window transparent
            self.out[Y0:Y1,X0:X1,ALPHA]=0
        else:
            print "NumpyImage.filLWindow color=",color
            assert len(color) == 4, "Fill colour must have 4 channels got " + str(color)
            self.out[Y0:Y1, X0:X1] = [color]

    def fillWindowAlpha(self,window,alpha=255):
        """
        Fill a region with the given alpha value.
        Possible use is to blow a hole into an image

        :param tuple window: (x,y,w,h)
        :param int alpha:  0-255 default 255
        :return: nothing self.out region has alpha set accordingly
        """
        X0, Y0, X1, Y1 = self.getViewport(window)
        self.out[Y0:Y1, X0:X1,ALPHA ] = alpha

    # TODO needs testing
    def fillWindowRandomPalette(self,window,palette):
        """
        fills the specified window with colors chosen at random from
        the supplied palette.

        :param tuple window: (x,y,w,h)
        :param list palette: python list of color objects
        :return: nothing, the specified area is colored
        """

        X0, Y0, X1, Y1 = self.getViewport(window)
        palLen=len(palette)

        for x in range(X1-X0):
            for y in range (Y1-Y0):
                pixel=palette[random.randint[0,palLen]].getPixelColor()
                self.out[y,x]=[pixel]

    def fillWindowRandom(self,window,alpha=255):
        """
        fills a window with one random color

        :param tuple window: (x,y,w,h)
        :param int alpha: 0 (transp[arent) to 255 (opaque)
        :return: the window area is filled.
        """
        x,y,w,h=window
        tmp=np.random.randint(0,256,(h,w,3))
        self.out[y:y + h, x:x + w, :3 ] = tmp # np.random.randint(0, 256, (h, w, 3))
        self.out[y:y + h, x:x + w, ALPHA]=alpha

    def clear(self):
        """
        alternate for fill() with no color specified which should result
        in the image being made transparent.
        """
        self.fill((0,0,0,0))

    def interpolation(self,enlarging):
        """
        Determine which openCV interpolation method is best when enlarging or not.

        :param boolean enlarging: True if enlarging
        :return: cv2 parameter for cv2.resize
        """
        # choose a suitable interpolation alogrithm
        # LANCROS4 gives better results when enlarging but is SIGNIFICANTLY SLOWER then INTER_CUBIC
        return cv2.INTER_CUBIC if enlarging else cv2.INTER_AREA

    #############################################################
    #
    # resizing
    #
    #############################################################

    def resizeByFactor(self,factor):
        """
        Scales the rgba_orig image to rgba_cached and copies rgba_cached to the output image.
        WARNING: Color or window edits to self.out will be lost!

        If the scale factor would proudce an image less than 1x1 then the scale factor is increased

        :param float factor: resize factor >0.0
        :return: The images self.rgba_cached and self.out are recreated
        """
        if factor<0:
            print "resizeByFactor factor cannot be <=0.0. Got "+str(factor)
            return

        # anything to do?
        if factor==1.0:
            self.resetImage()
            return

        # choose best interpolation method
        enlarging=True if factor>1.0 else False

        # resize from the original to get best quality
        if self.rgba_orig is not None:
            h, w = self.rgba_orig.shape[:2]
            h,w=float(h),float(w)
            hSize=h*factor
            wSize=w*factor
            if hSize<2 or wSize<2:
                factor=2/h if hSize<wSize else 2/w
            self.rgba_cached = cv2.resize(self.rgba_orig, (0,0), fx=factor,fy=factor,interpolation=self.interpolation(enlarging))
        else:
            print "NumpyImage.resizeByFactor() WARNING: attempt to resize code-created image. Did you mean to?"

        self.resetImage()

    def resizeKeepAspect(self,boundaryWidth,boundaryHeight):
        """
        Resizes an image so that it fits within a given boundary.

        WARNING: Color or window edits to self.out will be lost!

        :param int boundaryWidth: pixels, maxWidth
        :param int boundaryHeight: pixels, maxHeight
        :return: Nothing self.rgba_cached and self.out are modified
        """

        # aspectRatio MUST be a float
        curImHeight,curImWidth=self.rgba_orig.shape[:2]
        aspectRatio=float(curImWidth)/curImHeight

        if aspectRatio>1:
            # landscape
            scale=float(boundaryWidth)/curImWidth
        elif aspectRatio<1.0:
            #portrait
            scale=float(boundaryHeight)/curImHeight

        else:
            # no change required
            return

        # are we enlarging?
        enlarging=True if scale>1 else False

        # TODO - think about this. What is the image is created by dimension
        # resize from the original if it exists
        if self.rgba_orig is not None:
            self.rgba_cached = cv2.resize(self.rgba_orig, (0,0), fx=scale,fy=scale, interpolation=self.interpolation(enlarging))
        else:
            print "NumpyImage.resizeKeepAspect() WARNING: attempt to resize code-created image. Did you mean to?"

        self.resetImage()

    def resizeFitToTarget(self,targetWidth,targetHeight):
        """
        image is stretched to fit the targetWidth snd targetHeight area

        :param float targetWidth: converted to int
        :param float targetHeight: converted to int
        :return:
        """

        enlarging=True if targetWidth*targetHeight> self.width*self.height else False

        # start from the original
        if self.rgba_orig is not None:
            self.rgba_cached = cv2.resize(self.rgba_orig, (int(targetWidth), int(targetHeight)), interpolation=self.interpolation(enlarging))
        else:
            print "NumpyImage.resizeFitToTarget() WARNING: attempt to resize code-created image. Did you mean to?"

        self.resetImage()

    def setWindow(self,window):
        """
        copies the specified window from rgba_cached to out
        :param tuple window: (x,y,w,h)
        :return: self.out is a window of rgba_cached
        """
        x,y,w,h=window

        ch,cw=self.rgba_cached.shape[:2]

        # can't request MORE than the available window
        w=min(cw,w)
        h=min(ch,h)

        x0=nearest(x)
        y0=nearest(y)
        x1=nearest(x+w)
        y1=nearest(y+h)

        out=self.rgba_cached[y0:y1,x0:x1].copy()


    #######################################################
    #
    # get/set pixel functions
    #
    #  individual pixel setter/getter for drawing over an image
    #
    #######################################################
    def getPixel(self,x,y):
        """
        returns the color of the Pixel at x,y

        :param int x:
        :param int y:
        :return tuple: color (rgba) in Pixel order
        """
        return self.out[y,x]

    def setPixelAlpha(self,x,y,alpha=255):
        """

        :param int x: x-coord of pixel to set
        :param int y: y-coord of pixel to set
        :param int alpha: alpha value 0->255
        :return:
        """
        assert alpha>=0 and alpha<=255,"Alpha value should be int in range 0 to 255"
        assert type(alpha) is int,"Alpha value should be int"

        # trap attempts to write beyond image bounds
        if x<0 or x>=self.width: return
        if y<0 or y>=self.height: return

        self.out[y,x,ALPHA]=alpha

    def setPixel(self, x, y, color):
        """
        sets the image pixel(s) using the color(s) provided.

        Due to the flexibility of numpy arrays this code will work for a single pixel or a list.
        To set a list of pixels then x,y and color must all be lists.
        Values of x and y must be integers.
        :param tuple or numpy ndarray color: [[r,g,b,a],....[r,g,b,a]] or (r,g,b,a) values are uint8 in range 0 to 255
        :param int or nunmp ndarray x: int [ x0,x1,...xn] or x
        :param int or numpy ndarray y: int [y0,y1,..yn] or y
        :return: the specified pixels are set to the corresponding color
        """
        if type(color) is np.ndarray:
            assert type(x) is np.ndarray and type(y) is np.ndarray, "If color is a numpy ndarray then x and y must also be ndarrays."
            assert x.shape[:1] == y.shape[:1] == color.shape[:1], "Arrays must be of the same length."

        elif type(color) is list:
            assert type(x) is list and type(y) is list, "If color is a list then x and y must also be lists. Got x="+str(type(x))+" y="+str(type(y))
            assert len(x) == len(y) == len(color), "Lists must be of the same length."

        f=np.vectorize(nearest)
        x=f(x)
        y=f(y)

        self.out[y, x] =alphaBlendPixel(color,self.out[y,x])

    def setPixelRandom(self, x, y):
        """
        sets the pixel(s) using randomised color channels and alpha.

        Is able to set a single pixel or a list of pixels.

        :param int or numpy ndarray x:   int [ x0,x1,...xn] or x
        :param int or numpy ndarray y:   int [y0,y1,..yn] or y
        :return Nothing: pixel at x,y is/are set to random color(s)
        """
        if type(x) is list:
            assert type(y) is list, " x is a list therefore y parameter must also be a list."
            assert len(x) == len(y), "Lists must be of the same length."
        if type(x) is np.ndarray:
            assert type(y) is np.ndarray, "If x is a numpy ndarray then y must also be an ndarray."
            assert x.shape[:1] == y.shape[:1], "Arrays must be of the same length."

        f=np.vectorize(nearest)
        x=f(x)
        y=f(y)
        self.out[y, x] = [np.random.random_integers(0, 255), np.random.random_integers(0, 255),
                          np.random.random_integers(0, 255), np.random.random_integers(0, 255)]

    ######################################################################
    #
    # Adjuster functions

    def adjustHue(self,amount=0):
        """
        adds amount to rgba_cached image

        :param int amount: any value positive or negative
        :return Nothing: self.out is modified
        """
        assert type(amount) is int, self.classname+".adjustHue() Amount should be an int."
        if amount==0: return
        tmp=cv2.cvtColor(self.rgba_cached,PIXEL2HSV)   # CONVERT2HLS - see Constants.py to HLS
        tmp[:,:,HSV_H]=(tmp[:,:,HSV_H] + amount ) % 180
        tmp2=cv2.cvtColor(tmp,HLS2PIXEL)      # back to RGB (or BGR - see Constants.py
        self.out[:,:,:3]=tmp2

    def adjustSat(self,amount=0):
        """
        adjust saturation
        :param int amount: -255 to +255 added to current value and limited to 0-255 range
        :return Nothing: self.out is modified
        """
        assert type(amount) is int, self.classname+".adjustSat() amount should be an int."
        assert amount >= -255 and amount <= 255,  self.classname+".adjustSat() amount should be between -255 and +255"
        if amount == 0: return

        tmp = cv2.cvtColor(self.out, PIXEL2HSV)  # see Constants.py
        if amount<0:
            tmp[:, :, HSV_S] = np.maximum(tmp[:, :, HSV_S] + amount, 0)
        elif amount>0:
            tmp[:, :, HSV_S] = np.minimum(tmp[:, :, HSV_S] + amount,255)

        tmp = cv2.cvtColor(tmp, HSV2PIXEL)  # see Constants.py
        self.out[:, :, :3] = tmp[:, :, :3]

    def adjustLum(self,amount=0):
        """
        adjust luminance adds amount to current luminance and caps the min/max values at 0 and 255 respectively
        :param int mount: -255 to +255 , added to current value and capped at 0 or 255
        :return Nothing: adjusted image
        """
        assert type(amount) is int, self.classname+".adjustValue() amount should be an int."
        assert amount>=-255 and amount<=255, self.classname+".adjustValue() amount should be between  -255 and +255"

        if amount==0: return

        tmp = cv2.cvtColor(self.out, PIXEL2HSV)  # see Constants.py
        if amount<0:
            tmp[:, :, HSV_V] = np.maximum(tmp[:, :, HSV_V] + amount, 0)
        elif amount>0:
            tmp[:, :, HSV_V] = np.minimum(tmp[:, :, HSV_V] + amount, 255)
        tmp = cv2.cvtColor(tmp, HSV2PIXEL)  # see Constants.py
        self.out[:, :, :3] = tmp[:, :, :3]
    ##########################################################################
    #
    # setter functions - simply set H,S or L to a value

    #TODO test setHue
    def setHue(self,amount):
        """
        sets the Hue of the out image to a given amount.
        rgba_cached is not changed so it can be undone

        :param int amount: range any (modulo 180  is taken)
        :return Nothing: output image is modified
        """
        assert type(amount) is int,  self.classname+".setHue() amount should be an int."
        assert amount >=0 and amount <= 180,  self.classname+".setHue() amount should be between 0 and 360"

        tmp = cv2.cvtColor(self.out, PIXEL2HSV)  # see Constants.py
        tmp[:, :, HSV_H] = np.minimum(amount, 180)
        tmp = cv2.cvtColor(tmp, HSV2PIXEL)  # see Constants.py
        self.out[:, :, :3] = tmp[:, :, :3]

    def setSat(self, amount):
        """
        changes the saturation of the self.out image

        rgba_cached is not changed so it can be undone

        :param amount: 0 to 255
        :return Nothing: self.out is modified
        """
        assert type(amount) is int,  self.classname+".setSat() amount should be an int."
        assert amount >=0 and amount <= 255,  self.classname+".setSat() amount should be between 0 and 255"

        tmp = cv2.cvtColor(self.out, PIXEL2HSV)  # see Constants.py
        tmp[:, :, HSV_S] = amount
        tmp = cv2.cvtColor(tmp, HSV2PIXEL)  # see Constants.py
        self.out[:, :, :3] = tmp[:, :, :3]

    def setValue(self,amount):
        """
        set V component of self.out when converted to HSV.
        self.out is converted to HSV first then converted back

        rgba_cached is not changed so it can be undone

        :param int amount: range 0->255
        :return Nothing: self.out is modified
        """
        assert type(amount) is int,  self.classname+".setValue() amount should be an int."
        assert amount >=0 and amount <= 255,  self.classname+".setValue() amount should be between 0 and 255"

        # openCV uses numer ranges 0-255
        # see Constants.py for PIXEL2HSV and HSV2PIXEL
        tmp = cv2.cvtColor(self.out, PIXEL2HSV)
        tmp[:, :, HSV_V] = np.minimum(amount, 255)
        tmp = cv2.cvtColor(tmp, HSV2PIXEL)
        self.out[:, :, :3] = tmp[:, :, :3]

    def OFF_setBrightness(self,wanted):
        """
        Changes the overall brightness of the image
        self.rgba_cached is converted to HLS then L&S are scaled
        It is then converted back to RGB and pasted into self.out

        rgba_cached is not changed so it can be undone

        :param float wanted: wanted brightness float 0->100 percent
        :return: Nothing. self.out is modified
        """
        print "NumpyImage.setBrightness - change to Fade?"
        return self.fade(wanted)


    def fade(self,percent):
        """
        Changes the overall alpha of the self.out image.

        rgba_cached is not changed so it can be undone

        :param float percent: 0->100 percentage visiblility
        :return None: self.out is modified
        """

        assert percent>=0 and percent<=100, "NumpyImage.fade() wanted range is 0.0 to 100.0%"

        # the eye has a square law response
        # this makes the transition appear correct
        factor=getActualBrightness(percent)

        # alter the alpha
        self.out[...,ALPHA]=int(factor*255)

    def OFFfade(self,percent):
        """
        Changes the overall brightness and alpha of the self.out image.

        Scaling alpha means we don't get a black box where the image was when
        fade percent=0

        rgba_cached is not changed so it can be undone

        :param float percent: float 0->100 percent
        :return None: self.out is modified
        """

        # scales both the V and alpha

        assert percent>=0 and percent<=100, self.classname+".fade() wanted range is 0.0 to 100.0%"

        # the eye has a square law response
        # this makes the transition appear correct
        factor=getActualBrightness(percent)

        # cvtColor ignores the alpha channel and returns
        # only the HSV channels as uint8 values
        tmp=cv2.cvtColor(self.rgba_cached,PIXEL2HSV) # see Constants.py
        tmp[..., HSV_V]=(tmp[...,HSV_V]*factor).astype(np.uint8)
        tmp=cv2.cvtColor(tmp,HSV2PIXEL)   # see Constants.py

        # copy the RGB values back
        self.out[...,:3]=tmp[...,:3]

        # alter the alpha
        self.out[...,ALPHA]=int(factor*255)
    ######################################################
    #
    # misc image manipulations
    #
    ######################################################

    def blur(self,sigma=0):
        """
        blurs the rgba cached image and copies to self.out
        uses a gaussian filter with the given sigma value

        rgba_cached is not changed so this can be undone

        :param sigma: float value, higher values give more blur (2 gives very blurred image)
        :return: self.out is blurred
        """
        if sigma==0:
            self.out=self.rgba_cached.copy()
        else:
            self.out=ndimage.gaussian_filter(self.rgba_cached,sigma=sigma)

    # TODO test blend
    def blend(self,blendWith,alpha=0):
        """
        blend mixes two images with a certain alpha

        rgba_cached is not changed so this can be undone

        :param numpy ndarray blendWith: image to blend with
        :param float alpha: 0->1.0 amount to blend by
        :return Nothing: self.out is changed
        """
        self.out=alpha*self.out+(1-alpha)*blendWith

    def rotateAboutCenter(self, angle):
        """
        performs an affine transform rotating the image about it's center
        through the given angle. The transform is always applied from the rgba_orig image
        to avoid degradation

        :param degrees angle: 0-360 in degrees
        :return Nothing: self.out is transformed
        """
        # just call the base routine
        self.rotateAboutCenterRadians(math.radians(angle))

    def rotateAboutCenterRadians(self, angle):
        """
        Performs an affine transform rotating the self.out image about it's center
        through the given angle (radians). The transform is always applied from the rgba_orig image
        to avoid degradation and to keep the size correct

        :param radians angle: amount to rotate by
        :return: nothing self.out is transformed
        """

        x=self.width/2
        y=self.height/2
        sina=math.sin(angle)
        cosa=math.cos(angle)

        Y=y-x*sina-y*cosa
        X=x-x*cosa+y*sina
        self.transform((cosa, -sina, X, sina, cosa, Y))

    def rotate(self,x,y,angle):
        """
        rotate the shape about the x,y coordinates.
        rotate is always based on the rgba_orig image to preserve quality
        unless the image is not loaded from a file
        :param x:
        :param y:
        :param angle: degrees
        :return: nothing self.out is transformed
        """
        x,y=nearest(x),nearest(y)

        rad=math.radians(angle) #*math.pi/180
        sina=math.sin(rad)
        cosa=math.cos(rad)
        Y=y-x*sina-y*cosa   ## added
        X=x-x*cosa+y*sina
        self.transform((cosa, -sina, X,sina,cosa, Y))

    def rotateRadians(self,x,y,angle):
        """
        rotate the shape about the x,y coordinates.
        rotate is always based on the rgba_cached image to preserve quality.
        unless the image is not loaded from a file
        :param x:
        :param y:
        :param angle: radians
        :return: nothing self.out is transformed
        """
        x,y=nearest(x),nearest(y)

        sina=math.sin(angle)
        cosa=math.cos(angle)
        Y=y-x*sina-y*cosa   ## added
        X=x-x*cosa+y*sina
        self.transform((cosa, -sina, X,sina,cosa, Y))

    def shear(self,angle):
        """
        shear the image with the given angle

        :param angle: degrees -90 to +90 is sensible
        :return: the self.out image is sheared
        """
        #[1,-tan(ang),0][0,1,0]
        a=math.radians(angle)
        self.transform(1,-math.tan(a),0,0,1,0)

    def transform(self,matrix=None):
        """
        transform self.rgba to create new rgba_cached and out images
        however, if the image is created in memory, not from a file,
        transform self.out only
        transform matrix is [[a,b,c][d,e,f]]
        :param a:
        :param b:
        :param c:
        :param d:
        :param e:
        :param f:
        :return: transformed image
        """
        if matrix is None: return

        assert type(matrix) is tuple,"Transform matrix must be a tuple of 6 floats (a,b,c,d,e,f)."
        assert len(matrix)==6,"Transform matrix MUST contain 6 floats."

        # there has to be a more elegant way to ensure these are all floats
        a,b,c,d,e,f=float(matrix[0]),float(matrix[1]),float(matrix[2]),float(matrix[3]),float(matrix[4]),float(matrix[5])

        matrix=np.zeros((2,3))
        matrix[0]=[a,b,c]
        matrix[1]=[d,e,f]

        # check if working on a created image
        if self.imagePath is None:
            self.rgba_cached = cv2.warpAffine(self.out, matrix, (self.rgba_cached.shape[:2]))
        else:
            self.rgba_cached=cv2.warpAffine(self.rgba_orig,matrix,(self.rgba_cached.shape[:2]))
        self.resetImage()
    ######################################################
    #
    # Roll left/right/up/down
    #
    def roll(self,direction="right",distance=0):
        """
        shifts the output matrix in required direction
        :param direction: "up","down","left","right" [or first letter udlr]
        :param distance: float (rounded to nearest pixel)
        :return: self.out is rolled
        """
        if distance==0: return

        distance=nearest(distance)
        direction=direction.lower()

        if direction in ("down","d"):
            axis=0
        elif direction in ("up","u"):
            distance=-distance
            axis=0
        elif direction in ("left","l"):
            axis=1
            distance=-distance
        elif direction in ("right","r"):
            axis=1

        self.out=np.roll(self.out,distance,axis=axis)

    def copyWindow(self,window):
        """
        copies the windowed area from rgba_cached to out
        used by reveals. out must be blanked first using fillRGB
        :param window: (x,y,w,h)
        :return: Nothing, out is updated
        """

        X0, Y0, X1, Y1 = self.getViewport(window)

        self.out[Y0:Y1, X0:X1]=self.rgba_cached[Y0:Y1,X0:X1]

    def getViewport(self,window):
        """
        return viewport coordinates

        Check if the given window lies within this image if not raises WindowOutOfBound
        otherwise returns coords for a view of thiws image

        :param tuple window: (x,y,w,h)
        :return int: Coords of view x0,y0,x1,y1 to use
        :raises WindowOutOfBounds if window does not fit into this image
        """
        x,y,w,h=window

        X0=nearest(x)
        Y0=nearest(y)
        X1=nearest(x+w)
        Y1=nearest(y+h)

        if (X0<0) or (X1>self.width) or (Y1<0) or (Y1>self.height):
            raise WindowOutOfBounds("Window =%d,%d,%d,%d"%(window)+" image width=%d height=%d"%(self.width,self.height),"View was X0=%d X1=%d Y0=%d Y1=%d"%(X0,X1,Y0,Y1))

        return X0,Y0,X1,Y1

    def rollWindow(self,window,direction="right",distance=0):
        """
        Rolls a sub-section of this image defined by (x,y,w,h)

        If the sub-window isn't within the image it is ignored
        if distance is zero, it is ignored
        :param tuple window: (x,y,w,h)
        :param str direction: up,down,left,right - only first character is used.
        :param float distance: number of pixels to roll, converted to nearest int
        :return: specified window is scrolled
        :raises ValueError: is roll direction is not up,down,left or right
        """
        if distance == 0: return
        assert type(direction) is str,"rollWindow direction must be a string: up/down/left or right."

        # raises an exception if the window doesn't fit
        x0,y0,x1,y1=self.getViewport(window)

        distance = nearest(distance)
        direction = direction.lower()

        axis=0
        if direction in ("down", "d"):
            axis = 0
        elif direction in ("up", "u"):
            distance = -distance
            axis = 0
        elif direction in ("left", "l"):
            axis = 1
            distance = -distance
        elif direction in ("right", "r"):
            axis = 1
        else:
            raise ValueError("Window roll direction must be u(p), d(own),r(ight) or l(eft).")

        self.out[y0:y1, x0:x1] = np.roll(self.out[y0:y1,x0:x1], distance, axis=axis)

    def cvCircle(self,center,radius,color,thickness=cv2.FILLED,lineType=cv2.LINE_AA):
        """
        draws a circle (unfilled). Line is solid (no alpha)
        :param center: (x,y)
        :param radius:  r - int number of LEDs
        :param color: (r,g,b,a) in Pixel color order
        :param thickness: int, default cv2.FILLED
        :param lineType: see openCV docs for line type. default LINE_AA (anti-aliased)
        :return:
        """
        self.out = cv2.circle(self.out, center, radius, color, thickness, lineType)

    def cvLine(self,startPt,endPt,color,thickness=1,lineType=cv2.LINE_AA):
        """
        draws a line between two points using the specified color which must include the transparency.

        :param startPt: (x,y)
        :param endPt: (x,y)
        :param color: (r,g,b,a) in Pixel color order
        :param thickness: int default 1
        :param lineType: int default LINE_AA (anti-aliased) see openCV docs for line types
        :return: self.out has the required line added
        """
        self.out=cv2.line(self.out,startPt,endPt,color,thickness,lineType)

    def cvRectangle(self,pt1,pt2,color,thickness=cv2.FILLED,lineType=cv2.LINE_AA):
        """
        draw a rectangle using openCV rectangle method.
        :param pt1: (x,y) one corner
        :param pt2: (x,y) opposite corner
        :param color: (r,g,b,a) in Pixel color order
        :param thickness: int default FILLED
        :param lineType: int default LINE_AA (anti-aliased) see openCV docs for line types
        :return: self.out has the shape drawn on it
        """
        self.out=cv2.rectangle(self.out,pt1,pt2,color,thickness,lineType)

    def cvPolyLines(self, pts, color, isClosed=False,thickness=1, lineType=cv2.LINE_AA):
        """
        draw a sequence of connected lines
        seems to have problems on the edges of an image
        :param pts: a python array [[x0,y0],[x1,y1], ..[xn,yn]]
        :param color: (r,g,b,a) in Pixel color order
        :param isClosed: boolean default is False
        :param thickness: int line tickness - default 1
        :param lineType: line type (see opencv docs - defaults to LINE_AA - anti-aliased)
        :return: self.out has the shape drawn on it
        """
        pts=np.array(pts,np.int32)
        pts=pts.reshape((-1,1,2))
        self.out = cv2.polylines(self.out,[pts],isClosed, color, thickness, lineType)

    def cvFilledPoly(self,pts,color,lineType=cv2.LINE_AA):
        """
        creates a closed and filled shape from the list of pts given.
        :param pts: python array of vertex coords e.g. [ [x0,y0],[x1,y1],...[xn,yn]
        :param color: (r,g,b,a) in Pixel color order
        :param lineType: default is cv2.LINE_AA
        :return: the shape is drawn
        """
        pts=np.array(pts,dtype=np.int32)
        self.out=cv2.fillPoly(self.out,[pts],color,lineType)

    def cvEllipse(self,center,axes,angle=0,startAngle=0,endAngle=360,color=(255,255,255,255),thickness=cv2.FILLED,
                  lineType=cv2.LINE_AA):
        """
        draws an ellipse centered on the center coordinates, rotated by angle. The ellipse is closed or open depending
        on startAngle and endAngle.
        The default values give a closed ellipse
        :param center: (x,y) coords
        :param axes:  (horiz,vertical) - lengths of the axes
        :param angle: degrees angle of rotation of the ellipse (default 0)
        :param startAngle: start angle for drawing the ellipse (default 0)
        :param endAngle: end angle for drawing the ellipse (default 360)
        :param color: rgba in Pixel color order
        :param thickness: line thickness default is 1
        :param lineType: see openCV line types - default is LINE_AA (anti-aliased)
        :return: self.out has an ellipse drawn on it
        """
        self.out=cv2.ellipse(self.out,center,axes,angle,startAngle,endAngle,color,thickness,lineType)




