"""
Palette.py

defines color scheme palettes as lists of Color objects.

The animations may cycles through the color entries when setting pixels in chains or text colors.

Some examples are included.

"""



import copy  # to allow copying of palettes

import Colors
import random

class Palette():
    """
    Palette class

    Just a list of color objects making up a color scheme

    """

    pal=None    # array of colours
    lenPal=0    # palette length
    curEntry=0  # used by getNextEntry

    def __init__(self,colors):
        """
        set up the colour palette from a list of Colors. Basically copies the supplied list in case
        it gets changed.

        :param Color colors: a python list of colors e.g. [Colors.RED,Colors.BLUE..]
        """
        self.pal=[]
        self.lenPal=len(colors)
        for c in colors:
            #TODO - does it resally need to be a deepcopy - the palettes are never altered!
            # a deep copy allows the palette entries to be changed without
            # affecting the original colours
            self.pal.append(copy.deepcopy(c))

    def getRandomEntry(self):
        """
        get a random entry from the palette
        :return Color object: randomly selected
        """
        entry=random.randint(0,self.lenPal-1)
        return self.pal[entry]

    def getEntry(self,n):
        """
        get the specified Color object from the palette at position n
        :param n:
        :return Color or None: if n is in
        """
        assert type(n) is int,"Palette entry index must be an int."
        if abs(n)>len(self.pal): return None
        self.curEntry=n # getNextEntry will retrieve the correct next entry
        return self.pal[n]

    def getNextEntry(self):
        """
        get the specified Color object from the palette at position self.curEntry
        :return Color
        """
        c=self.pal[self.curEntry]
        self.curEntry=(self.curEntry+1) % len(self.pal)
        return c

    def getLength(self):
        """
        return the number of entries in the palette
        :return int: number of entries
        """
        return len(self.pal)

    def getFirstEntry(self):
        """
        return the first entry in the palette
        :return Color: the first entry
        """
        self.curEntry=0 # ensure getNextEntry works as expected
        return self.pal[0]


# some predefined colors
# these colors are used a lot in the palettes below and are here for lazyness
R= Colors.Red
G= Colors.Green
B= Colors.Blue
M= Colors.Magenta
C= Colors.Cyan
Y= Colors.Yellow
K= Colors.Black
W= Colors.White

# predefined palettes
# a palette is just a list of colors defined in Colors.py
RGB=Palette([R,G,B])
RGBW=Palette([R,G,B,W])
CMY=Palette([C,M,Y])
CMYK=Palette([C,M,Y,K])
CMYW=Palette([C,M,Y,W])
BLACKWHITE=Palette([K,W])

# example single color palettes
RED=Palette([R])
GREEN=Palette([G])
BLUE=Palette([B])
CYAN=Palette([C])
MAGENTA=Palette([M])
YELLOW=Palette([Y])
WHITE=Palette([W])
LIGHTBLUE=Palette([Colors.LightBlue])

###################################
XMAS=Palette([R,G,B,W,M,C,Y])

# light shades
DELICATE=Palette([Colors.LightBlue, Colors.LightSalmon, Colors.LightSteelBlue, Colors.LavenderBlush, Colors.Lavender])



# lots of colors - just a proof of concept

LOTS=Palette([
    Colors.AliceBlue,
    Colors.AntiqueWhite,
    Colors.Aqua,
    Colors.Aquamarine,
    Colors.Azure,
    Colors.Beige,
    Colors.Bisque,
    Colors.Black,
    Colors.BlanchedAlmond,
    Colors.Blue,
    Colors.BlueViolet,
    Colors.Brown,
    Colors.BurlyWood,
    Colors.CadetBlue,
    Colors.Chartreuse,
    Colors.Chocolate,
    Colors.Coral,
    Colors.CornflowerBlue,
    Colors.Cornsilk,
    Colors.Crimson,
    Colors.Cyan,
    Colors.DarkBlue,
    Colors.DarkCyan,
    Colors.DarkGoldenRod,
    Colors.DarkGray,
    Colors.DarkGreen,
    Colors.DarkKhaki,
    Colors.DarkMagenta,
    Colors.DarkOliveGreen
])