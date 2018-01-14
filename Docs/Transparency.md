# Brightness and Transparency

Transparency and brightness values are supported in one of two ranges.

Some routines use the floating point range 0.0 to 1.0 and some use the integer range 0 to 255. Both mean 0% to 100%.

In particular, Chains and Colours are stored in HSV floating point format which means their values range from 0.0 to 
1.0 and so alpha values are also in the range 0.0 to 1.0

Images are stored in RGB format using the ranges 0 to 255 and so their brightness and alpha values are also in the 0 
to 255 range

If you use a development environment like PyCharm the system will tell you what is expected when you type the 
parameter lists.

I guess I could add extra code to convert for you and so give one scheme only but that could slow things down, so I 
haven't done that.


## Images and Transparency

When an image, with transparency, is loaded from disk the transparency is kept. However it is possible to change the 
transparency of an image if you want to. NumpyImage has a setAlpha() method for this.

If the image doesn't have an alpha channel the code adds one set to 100%.

You can create a blank image with transparency using NumpyImage(width=www, height=hhh, alpha=aaa). Values are 
integers. aa is in the range 0 to 255. If you don't specify an transparency value it is set to 255 by default.

## Brightness

Brightness is applied to all pixels as a multiplier in the range 0 to 1.0. Images need to be converted to HSV to do 
this then the V component is multiplied by the required brightness factor and then converted back to RGB. This means 
that the. 


## Animation tricks

The Image dissolve animation works by randomly changing the transparency of the foreground image pixels from 0% to 100% 
for dissolve in and 100% to 0% for dissolve out.

The fade animations alter both the brightness and transparency of the image. Transparency is changed to make the 
image disappear.


