"""
Font.py

load and cache BDF font characters as numpy arrays.

The character glyphs are rendered as white on black and cached on demand.

The alpha channel is set to 100% for the character shapes and 0% for the black background.

The caller must do the colorising of the font.

The BDF font IDs are defined in Constants.py in a form like BDF_<size> where <size> is 6..20 and represents the font size.
font IDs are simply the filename of the font file within the Fonts folder.
The definitions in Constants.py enable the programmer to define which fonts are used for whatever size is needed.
The physical location of the font folder is also declared in Constants.py as BDF_FONTLOC

"""
import LEDAnimator.UtilLib
import numpy as np

from LEDAnimator.Colors import *
from LEDAnimator.Constants import *
from LEDAnimator.Palette import *

# in the same location as Font.py
import Cache as bdfCache
from UtilLib import *

import os

# font characters are stored in HLS format to be compatible with
# NumpyImage

WHITE=White.getPixelColor() # foreground RGBA 100% alpha

class Font():

    bdf_font=None
    charGlyphInfo={}    # BDF info
    charGlyphImage={}   # nump arrays

    def __init__(self,size):
        """
        load the BDF font file and cache it
        :param int: the font ID
        """
        assert type(size) is int,"Size parameter must be an int got "+str(size)
        assert size in BDF_FONT,"Unsupported font size. See Constants.py"

        fontPath=os.path.join(BDF_FONTLOC,BDF_FONT[size])

        # loads the font via the cache
        self.bdf_font = bdfCache.loadFont(fontPath)

    def getFontType(self):
        return BDF_FONTTYPE

    def getFontMetrics(self):
        """
        returns the ascent and descent for the font

        :return int,int: ascent,descent
        """
        return self.bdf_font.getFontMetrics()


    def getChar(self,char):
        """
        On first access a character bitmap is turned into a numpy array (RGBA) and
        ]stored in the charCache
        :param str char: Like "A"
        :return numpy ndarray: nunmpy image for the character (black and white)
        """
        if char not in self.charGlyphInfo:
            self._RenderChar(char)

        return self.charGlyphImage[char].copy()

    def getCharShape(self,char):
        """
        Returns the height and width of the given character for the current font & size

        :param str char: like "A"
        :return int,int: height,width
        """
        if char not in self.charGlyphInfo:
            self._RenderChar(char)

        # charCache contains numpy images
        return self.charGlyphImage[char].shape[:2]

    def getFontBbox(self):
        """
        get the bounding box for the font.

        Returns the width, height for the font characters as a whole.

        Individual characters may have different dimensions (unlikely).

        :return int,int: width,height
        """
        return self.bdf_font.getFontBbox()

    def getTextBbox(self,text):
        """
        returns the full height and width of a text box
        which will contain the text

        Since BDF is a monospaced font we can calculate the length
        by multiplying the width of the font bounding box by the number of characters

        :param str text: the text to measure
        :return int,int width,height: dimensions of the text
        """
        w,h=self.getFontBbox()
        return len(text)*w,h

    def _RenderChar(self, ch):
        """
        renders text as white on black and stores it in the character cache
        so it can be reused.

        Not meant for external consumption. Used by getChar()

        Characters are rendered as numpy arrays ONLY when they are called for
        to try to improve responsiveness.

        :param ch: character to render
        :return: Nothing - adds character as numpy array to the cache
        """
        assert self.bdf_font is not None, "No font loaded"

        bitmap = self.bdf_font.getBitmap(ch)    # Python list

        w, h = self.bdf_font.getTextBbox(ch)

        w = int(w)
        h = int(h)

        # create the image of the character using black transparent background
        # and add an Alpha channel
        im=np.zeros((h,w,4),np.uint8)

        #print "FONT _RenderChar w=",w

        # characters are left aligned in fields of 1,2,3,4 bytes etc
        # how many bytes will the character width be in?
        bytes = int(w / 8)+1  # number of bytes for this width
        align = bytes*8-w #w % 8  # extra bits to shift wordmask


        bitmask = 1 << (w - 1)  # left most bit
        wordmask = 0
        for b in range(w):
            wordmask = wordmask | (1 << b)


        #print "FONT _RenderChar bytes=",bytes,"align",align

        wordmask = wordmask << align
        bitmask = bitmask << align

        #print "FONT _RenderChar bytes=",bytes,"align",align,"wordmask=",bin(wordmask),"bitmask=",bin(bitmask)

        # scan each row of the bitmap
        for row in range(h):  # pt size
            x = bitmap[row]
            for col in range(w):
                if x & bitmask:
                    im[row, col]= WHITE # white has 100% alpha
                x = (x << 1) & wordmask

        self.charGlyphImage[ch]=im


    def drawText(self,image,x,y,text,fgColor,lineType=None):
        """
        Render the text on the image indicated at x,y using the specified foreground and
        background colors.

        if the foreground color is a Palette cycle through the palette with each character.

        If the Palette contains R,G,B in that order the first character will be rendered in red, the second green
        third blue, fourth red ... etc

        :param numpy ndarray image: image on which to render (textBuffer)
        :param int x: x pos
        :param int y: y pos
        :param str text: text string
        :param tuple or Palette fgColor: colors to use for the foreground
        :return int: next character x position
        """
        if not isinstance(fgColor, Palette):
            fgColor = channelSwap(fgColor)

        for ch in text:

            char=self.getChar(ch)

            if isinstance(fgColor,Palette):
                charColor=fgColor.getNextEntry().getPixelColor()
                charColor=channelSwap(charColor)
                char = self._ColorGlyph(char, charColor)
            else:
                char = self._ColorGlyph(char, fgColor)

            x=LEDAnimator.UtilLib.pasteWithAlphaAt(image, x+1, y, char)

        return x

    def _ColorGlyph(self, glyph, fgColor=None):
        """

        The glyph must be a numpy array with the glyph in white and the background in black (transparent)

        The colors include alpha which sets the character transparency. However, if the foreground is None it is made
        fully transparent. Similarly, if the background is None it is left fully tansparent.

        Background color is added to the textBuffer first.


        :param numpy ndarray instance glyph: the black and white character
        :param fgColor: (r,g,b,a) in Pixel order
        :return numpy ndarray: colored glyph
        """

        assert fgColor is not None,"fgColor cannot be None - transparency is done with Alpha"

        # define color order for masks
        alpha=glyph[:,:,ALPHA]
        foreground_mask = (alpha == 255)

        if fgColor is not None:
            glyph[:, :][foreground_mask] = fgColor

        return glyph
