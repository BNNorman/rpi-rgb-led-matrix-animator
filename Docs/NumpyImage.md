# NumpyImage

This class manages numpy images.

The class is actually 3 images.

1 The original image (rgba_orig) which is cached by ImageCache to save space and time when an image is reused.
2 rgba_cached, which is the rgba_orig with scaling/transforms applied. This is retained so changes can be undone
3 out - the image which you see on screen

Image manipulations consist of applying changes to **rgba_cached** and writing them to **out**. When transforms are 
done they are done to rgba_orig and copied to rgba_cache. This way maximum quality is maintained.


## Methods

### getImageData()

Returns the **out** image so you can do your own numpy fin stuff to it.

### resetImage()

Resets out by copying rgba_cached over it.

### alignImage(h,v)

Aligns the image in the horizontal/vertical direction in a given area and returns the top left coords for placing the 
image.

### countVisible()

Returns a count of pixels which have non-zero alpha values

### fill

Fills the image with a given color value

### fillAlpha

Sets the image transparency.

### clear and clearWindow()

Sets the transparency to 100%

### fillWindow

Fills a region with a color.

### fillWindowAlpha

Sets the transparency of the image or window with a given value

### fillWindowRandomPalette()

Sets all the pixels in the window with colors selected at random from the palette

### fillWindowRandom()

Fills a window with random colors

### clear()

Clears the image - sets transparency to 100%

### resizeByFactor

Scales rgba_orig to create rgba_cached and out. Any previous image edits are lost.

### resizeFitToTarget

Scales rgba_orig to create rgba_cached and fits it to the given window

### resizeKeepAspect

Scales the image but maintains the aspect ratio.

### getPixel

Returns the color of the chosen pixel

### setPixel

Sets the rgba color of a pixel OR if x&y are lists, sets all the pixels in the list.

### setPixelAlpha

Stes the transparency of a pixel or pixels

### setPixelRandom

Sets the color of a pixel or pixels to a random color

### adjustHue, adjustSat, adjustLuminance

Adds an offset to the HSV values of the image. Fun stuff indeed.

### setHue,setSat,setbrightness

Sets the HSV channels to specific values. More fun effects to be had.

### Fade

Adjusts the luminance and transparency of the image. Used for fade in and fade out animations.

### Blur

Blurs the image

### Blend

Blends the out image with the supplied image.

### rotateAboutCentre and rotateAboutCenterRadians

Rotates the image about its center. This is a transform so it blows away any prior edits.

### rotate and rotateRadians

Rotates the image about the given xy coords. 0,0 is top left so a +/-90 degree rotate will make the image vanish

### Shear
Transforms the original image using the openCV warp affine method but setup to shear at a specified angle

### transform

Transforms the original image using the openCV warp affine method.

### roll and rollWindow

Rolls the whole image or a window. Rolling can be donw in 4 directions, up,down,left,right. It is the method used by 
the Matrix animation.

### copyWindow

Copies a window from the **rgba_cached** image onto the **out** image. Effectively this resets the output image 
appearance as per the window selected. 

### getViewPort

Returns a numpy slice of the image data (**out**)

### openCV drawing functions

NumpyImage supports the following openCV drawing functions

- cvCircle
- cvLine
- cvRectangle
- cvPolyLines
- cvFilledPoly
- cvEllipse

They support attributes such as lineType and thickness. The allowed values for lineType are LINE_AA (anti-aliased), 
LINE_8 and LINE_4 as defined in Constants.py.
