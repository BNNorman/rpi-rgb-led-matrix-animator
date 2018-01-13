"""
Colors.py

Defines the Color object and provides a collection of www.w3schools.com colors.

Colors are stored as HSV values - this makes it a lot easier to change the brightness
without messing up the hue.

See also, Palette.py
"""

import colorsys
from Constants import *
import re
import random



###########################################################
#
# range mapping routines
#
###########################################################

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

class Color():
    """
    Color object

    Converts hex RRGGBB values to HSV

    Doing this makes it possible to change the brightness of a color by multiplying the V component
    by a factor in range 0->1.0

    Color objects do not have transparency - that is added in, for example, the Chain object

    """

    H=0.0   # range 0->1.0
    V=0.0
    S=0.0

    def __init__(self,col):
        """
        convert a color to HSV and store it

        :param str col: color format RRGGBB
        """
        assert type(col) is str,"Color must be a hex string format RRGGBB e.g. 'FF00FF'"

        lenCol=len(col)

        if lenCol<2 or lenCol>6:
            raise InvalidHexColor("Expected 2,4 or 6 characters")

        # prepend the required number of zeros
        if lenCol<6:
            prefix="0"*(6-lenCol)
            col=prefix+col

        p=re.compile(r"^[0-9A-Fa-f]{6}$")
        if p.match(col) is None:
            raise InvalidHexColor("Hex color string should only contains the characters a-fA-F0-9. Got",col)

        # assume RRGGBB order
        R=float8(int(col[0:2], 16))
        G=float8(int(col[2:4], 16))
        B=float8(int(col[4:6], 16))

        self.H, self.S, self.V = colorsys.rgb_to_hsv(R, G, B)

    def hsva2PixelColor(self,hsv):
        """
        internal only - converts HSV colour to RGB with 100% alpha added. Values are mapped to the 0->255 range.

        The order of the channels is governed by the values of RGB_R,RGB_G and RGB_B defined in Constants.py

        For simulating the BGR format is used by openCV's imshow()

        :param tuple hsv: (h,s,v,a)
        :return tuple : (r,g,b,a) in Pixel order
        """
        h,s,v,a=hsv
        r,g,b=colorsys.hsv_to_rgb(h,s,v)
        color = (uint8(r), uint8(g), uint8(b),uint8(a))
        return self.rgba2PixelColor((color[RGB_R],color[RGB_G],color[RGB_B],color[ALPHA]))

    def rgba2PixelColor(self,color):
        """
        Helper - ensures rgba is in the order required for pixels
        :param color: tuple rgba in Pixel order
        :return: tuple rgba in Pixel color order
        """
        assert len(color)==4,"color tuple should have 4 parts. Got "+str(color)
        return (color[RGB_R], color[RGB_G], color[RGB_B], color[ALPHA])


    def getPixelColor(self,brightness=1.0,alpha=1.0):
        """
        returns the pixel color adjusted for required brightness. Using a multiplier means
        we don't destroy the original color's hue
        :param float brightness: brightness multiplier in range 0.0->1.0
        :param float alpha: transparency 0->1.0 default 1.0
        :return tuple: (r,g,b,a) in pixel order
        """
        assert brightness>=0.0 and brightness<=1.0,"brightness value should be in range 0->1.0"
        assert alpha >= 0.0 and alpha <= 1.0,"alpha value should be in range 0->1.0"

        if brightness<=0:
            # it's black - no calcs needed
            # return solid black - all channels are zero
            return Black.getPixelColor(alpha=alpha)

        (r,g,b)=colorsys.hsv_to_rgb(self.H,self.S,self.V*brightness)

        color=(uint8(r),uint8(g),uint8(b),uint8(alpha))
        return self.rgba2PixelColor(color)

    def getRandomPixelColor(self,brightness=1.0,alpha=1.0):
        """
        returns a random color with the requested brightness and alpha

        :param float brightness: multiplier range 0->1.0 default 1.0
        :param float alpha: value range 0->1.0 default 1.0
        :return tuple: (r,g,b,a) mapped to 0->255 with channels ordered
        """
        assert brightness >= 0.0 and brightness <= 1.0, "brightness value should be in range 0->1.0"
        assert alpha >= 0.0 and alpha <= 1.0, "alpha value should be in range 0->1.0"

        H,S,V=random.randint(0,255)/255.0,random.randint(0,255)/255.0,random.randint(0,255)/255.0
        (r,g,b)=colorsys.hsv_to_rgb(H,S,V*brightness)
        color=(uint8(r),uint8(g),uint8(b),uint8(alpha))
        return self.rgba2PixelColor(color)

'''
www.w3schools.com standard web colors

If you aren't using all of these then it's best to comment out
those not needed to save some space and reduce startup time

These colors are in RRGGBB order and are converted to
HSV to make it easier to change the brightness but keep the hue constant
'''


AliceBlue=Color("F0F8FF")
AntiqueWhite=Color("FAEBD7")
Aqua=Color("00FFFF")
Aquamarine=Color("7FFFD4")
Azure=Color("F0FFFF")
Beige=Color("F5F5DC")
Bisque=Color("FFE4C4")
Black=Color("000000")
BlanchedAlmond=Color("FFEBCD")
Blue=Color("0000FF")
BlueViolet=Color("8A2BE2")
Brown=Color("A52A2A")
BurlyWood=Color("DEB887")
CadetBlue=Color("5F9EA0")
Chartreuse=Color("7FFF00")
Chocolate=Color("D2691E")
Coral=Color("FF7F50")
CornflowerBlue=Color("6495ED")
Cornsilk=Color("FFF8DC")
Crimson=Color("DC143C")
Cyan=Color("00FFFF")
DarkBlue=Color("00008B")
DarkCyan=Color("008B8B")
DarkGoldenRod=Color("B8860B")
DarkGray=Color("A9A9A9")
DarkGreen=Color("006400")
DarkKhaki=Color("BDB76B")
DarkMagenta=Color("8B008B")
DarkOliveGreen=Color("556B2F")
DarkOrange=Color("FF8C00")
DarkOrchid=Color("9932CC")
DarkRed=Color("8B0000")
DarkSalmon=Color("E9967A")
DarkSeaGreen=Color("8FBC8F")
DarkSlateBlue=Color("483D8B")
DarkSlateGray=Color("2F4F4F")
DarkTurquoise=Color("00CED1")
DarkViolet=Color("9400D3")
DeepPink=Color("FF1493")
DeepSkyBlue=Color("00BFFF")
DimGray=Color("696969")
DodgerBlue=Color("1E90FF")
FireBrick=Color("B22222")
FloralWhite=Color("FFFAF0")
ForestGreen=Color("228B22")
Fuchsia=Color("FF00FF")
Gainsboro=Color("DCDCDC")
GhostWhite=Color("F8F8FF")
Gold=Color("FFD700")
GoldenRod=Color("DAA520")
Gray=Color("808080")
Green=Color("00FF00")
GreenYellow=Color("ADFF2F")
HoneyDew=Color("F0FFF0")
HotPink=Color("FF69B4")
IndianRed=Color("CD5C5C")
Indigo=Color("4B0082")
Ivory=Color("FFFFF0")
Khaki=Color("F0E68C")
Lavender=Color("E6E6FA")
LavenderBlush=Color("FFF0F5")
LawnGreen=Color("7CFC00")
LemonChiffon=Color("FFFACD")
LightBlue=Color("ADD8E6")
LightCoral=Color("F08080")
LightCyan=Color("E0FFFF")
LightGoldenRodYellow=Color("FAFAD2")
LightGray=Color("D3D3D3")
LightGreen=Color("90EE90")
LightPink=Color("FFB6C1")
LightSalmon=Color("FFA07A")
LightSeaGreen=Color("20B2AA")
LightSkyBlue=Color("87CEFA")
LightSlateGray=Color("778899")
LightSteelBlue=Color("B0C4DE")
LightYellow=Color("FFFFE0")
Lime=Color("00FF00")
LimeGreen=Color("32CD32")
Linen=Color("FAF0E6")
Magenta=Color("FF00FF")
Maroon=Color("800000")
MediumAquaMarine=Color("66CDAA")
MediumBlue=Color("0000CD")
MediumOrchid=Color("BA55D3")
MediumPurple=Color("9370DB")
MediumSeaGreen=Color("3CB371")
MediumSlateBlue=Color("7B68EE")
MediumSpringGreen=Color("00FA9A")
MediumTurquoise=Color("48D1CC")
MediumVioletRed=Color("C71585")
MidnightBlue=Color("191970")
MintCream=Color("F5FFFA")
MistyRose=Color("FFE4E1")
Moccasin=Color("FFE4B5")
NavajoWhite=Color("FFDEAD")
Navy=Color("0000FF")
OldLace=Color("FDF5E6")
Olive=Color("808000")
OliveDrab=Color("6B8E23")
Orange=Color("FFA500")
OrangeRed=Color("FF4500")
Orchid=Color("DA70D6")
PaleGoldenRod=Color("EEE8AA")
PaleGreen=Color("98FB98")
PaleTurquoise=Color("AFEEEE")
PaleVioletRed=Color("DB7093")
PapayaWhip=Color("FFEFD5")
PeachPuff=Color("FFDAB9")
Peru=Color("CD853F")
Pink=Color("FFC0CB")
Plum=Color("DDA0DD")
PowderBlue=Color("B0E0E6")
Purple=Color("800080")
Red=Color("FF0000")
RosyBrown=Color("BC8F8F")
RoyalBlue=Color("41690")
SaddleBrown=Color("8B4513")
Salmon=Color("FA8072")
SandyBrown=Color("F4A460")
SeaGreen=Color("2E8B57")
SeaShell=Color("FFF5EE")
Sienna=Color("A0522D")
Silver=Color("C0C0C0")
SkyBlue=Color("87CEEB")
SlateBlue=Color("6A5ACD")
SlateGray=Color("708090")
Snow=Color("FFFAFA")
SpringGreen=Color("00FF7F")
SteelBlue=Color("4682B4")
Tan=Color("D2B48C")
Teal=Color("8080")
Thistle=Color("D8BFD8")
Tomato=Color("FF6347")
Turquoise=Color("40E0D0")
Violet=Color("EE82EE")
Wheat=Color("F5DEB3")
White=Color("FFFFFF")
WhiteSmoke=Color("F5F5F5")
Yellow=Color("FFFF00")
YellowGreen=Color("9ACD32")