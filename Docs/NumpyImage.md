#NumpyImage

All images are handled as numpy ndarrays (images). The NumpyImage class adds operations which can be applied to an 
image.

First of all, within a NumpyImage there are actually three images:-

-rgba_orig - this is the image loaded from disc. It is never changed but is used as the starting point for 
transformations.  

-rgba_cached - this is the transformed version of rgba_orig. Colour changes are applied to this to produce the final 
image. This allows colour changes (and alpha) to be applied and, later, undone.  

-out - this is the final image that is sent to the LED panel layer for output.

When you create an image from a disc based file NumpyImage calls ImageCache to load and cache the image.

    img=NumpyImage(imagePath="../Images/Tulips.jpg")

NumpyImage can also be used to create a blank image of a given size:-

    img==NumpyImage(width=128,height=16,alpha=255)
    
The above will create a solid black image. This technique is used by the text rendering to create an image that 
matches the size of the proposed text message which is then merged into the Panel frameBuffer.

if you want the image color changed specify fillColor=(r,g,b,a).

##NumpyImage Methods

There are many image manipulation methods - each has (should have) a doc string.



