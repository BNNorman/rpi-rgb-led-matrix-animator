# Palettes and Colors

Chain and text animations may use color palettes which are just python lists of colour objects.

## RGB or BGR?

OpenCV imread() returns images in BGR order so the code manages color in that way to minimise channel swapping.

The order is defined in Constants.py by setting the variables RGB_R=2, RGB_G=1, RGB_B=0. If you replace the imread() 
method in ImageCache.py you may need to redefine these - usually it's just R and B that are swapped.


Panel.py changes the byte order for output to the LED RGB Panel, if it needs to.

## Colors

See Colors.py

The Color object stores color using the HSV colorspace. This makes it easier to change the brightness of a colour 
just by multiplying the V component by a brightness factor e.g.:-

    color=Color.getPixelColor(brightness) 

Colors.py also includes a full list of the www.w3schools.org colour table. 

## Palettes

See Palette.py

Most animations cycle through the palette when the animation restarts however, this depends on how the animations are
 coded so you must look at the animation code to see how it uses the palette, if at all.
 
The www.w3schools.org colors are available to create your own palettes.

Some example palettes are already defined:-

    RGB         red, green, blue
    RGBW        as RGB but with white
    CMY         cyan, magenta, yelloe
    CMYK        as above plus black
    CMYW        as CMY plus white
    XMAS        R,G,B,W,M,C,Y  
    DELICATE    a list of delicate pastel colours  
    LOTS        a lot of colours from the www.w3school.org colors  




