'''
Parser.py

e.g.

f=Parser.bdfFont(ID)

or
f=BdfParser.bdfFont()
f.LoadFont(ID)

Performance: Not good. Takes 0.384secs on a 960 Kb font file. using readlines() and specifying a 1mb buffer is actually worse.
Still, the font is chached on first access and measurements suggest a second access is 10,000 faster

So, if you are going to use a font during animations it's a good idea to pre-load the fonts before the text animations
get going. You can do that in the Main.py script just be creating font instances e.g.

f12=BDF.Font(12)
f14=BDF.Font(14)

but this won't help with text scaling


accessing properties can be done like so:-

SIZE=f.SIZE

see http://www.adobe.com/content/dam/acom/en/devnet/font/pdfs/5005.BDF_Spec.pdf

---------------------------------------------------------
Copyright (C) 2017 Brian Norman, brian.n.norman@gmail.com

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

from LEDAnimator.ExceptionErrors import *

class Glyph():

    # attributes of each character which can be accessed
    NAME = None     # string description like 'comma'
    BITMAP = []     # python str list of hex numbers
    BBX = None
    SWIDTH = None
    DWIDTH = None
    ENCODING = None # ascii code

    def __init__(self,char):
        self.NAME=char


    def getBitmap(self):
        return self.BITMAP

    def getBBX(self):
        return self.BBX


class Parser():

    Glyphs={}   # dictionary of Glyphs keyed on ENCODING

    # basic attributes, any not listed will be created autonmatically (see processProperties)
    SIZE=None           # tuple (ptsize , xres, yres)
    version=None
    FONTBOUNDINGBOX=None
    DWIDTH=None
    SWIDTH=None
    CHARS=None
    FONT_ASCENT=None    # above baseline
    FONT_DESCENT=0      # below baseline

    def __init__(self,path=None):
        if path is not None: self.loadFont(path)

    def getFontMetrics(self):
        # keep it simple
        return self.FONT_ASCENT,self.FONT_DESCENT


    def getBaseline(self):
        """
        try to get the baseline of a font.

        Generally for BDF pointsize=font_ascent+font_descent

        So baseline=FONT_DESCENT

        :return:
        """
        height,xres,yres=self.SIZE

        if self.FONT_DESCENT is None: return 0
        # return distance from bottom
        return self.FONT_DESCENT

    def loadFont(self, path):
        """
        Reads the specified font file and parses the contents into self.Glyphs
        which is keyed by character Encoding (decimal value e.g. ord(char)

        :param path: os path to the font file
        :return Nothing: self.Glyphs is populated
        """

        self.Glyphs={}  # dictionary such that Glyph<-self.Glyphs[encoding]

        try:
            self.fp=open(path,"r")

        except Exception as e:
            print("BDF/Parser.py: LoadFont() Cannot open font file ("+path+"). ",e.args)
            return False

        self.processFont()


    def processFont(self):
        """
        reads through all the lines in the text file
        :return Nothing: self.Glyphs is populated with characters
        """
        # scan through all lines in the font file
        while True:
            line=self.fp.readline().split()

            cmd=line[0]
            if cmd=="STARTFONT":
                self.version=line[1]
            elif cmd=="COMMENT":
                pass
            elif cmd=="SIZE":
                self.SIZE=(int(line[1]),int(line[2]),int(line[3]))
            elif cmd=="FONTBOUNDINGBOX":
                self.FONTBOUNDINGBOX=(int(line[1]),int(line[2]),int(line[3]),int(line[4]))
            elif cmd=="STARTPROPERTIES":
                self.processProperties(int(line[1]))
            elif cmd=="CHARS":
                self.CHARS=int(line[1])
            elif cmd=="STARTCHAR":
                self.processChar(line[1])
            elif cmd=="ENDFONT":
                self.fp.close()
                return
            else:
                setattr(self,cmd," ".join(line[1:]))

    def processProperties(self,count):
        """
        processes the initial properties of the font file and aets the attributes
        of the Parser.

        Caller can access properties thus:-

        p=Parser(<font file>)
        numChars=p.CHARS

        :param int count: number of properties specified on STARTPROPERTIES line
        :return Nothing: properties are added to the Parser object

        """
        for prop in range(count):
            line = self.fp.readline().split()
            cmd=line[0]

            if cmd=="ENDPROPERTIES":
                return
            elif cmd=="COMMENT":
                pass
            elif cmd=="FONT_ASCENT":
                self.FONT_ASCENT=int(line[1])
            elif cmd=="FONT_DESCENT":
                self.FONT_DESCENT=int(line[1])
            else:
                if len(line)==2:
                    setattr(self,line[0],line[1])
                else:
                    setattr(self,line[0]," ".join(line[1:]))

    def processChar(self,char):
        """
        char is a textual representation like 'double-quote'
        The actual character is determined by the ENCODING
        :param str char:
        :return Nothing: The character glyph is added to the Glyphs dictionary
        """

        charGlyph=Glyph(char)

        Done=False
        doingBitmap=False

        while not Done:
            line=self.fp.readline().split()

            prop=line[0]

            if prop=="COMMENT":
                pass
            elif prop=="BBX":
                charGlyph.BBX=(line[1],line[2],line[3],line[4])
            elif prop=="BITMAP":
                charGlyph.BITMAP=[]
                doingBitmap=True
            elif prop=="ENDCHAR":
                #self.Glyphs.append(charGlyph)
                self.Glyphs[charGlyph.ENCODING]=charGlyph
                doingBitmap=False
                Done=True
            elif prop=="SWIDTH":
                charGlyph.SWIDTH=(line[1])
            elif prop=="DWIDTH":
                charGlyph.DWIDTH=int(line[1])
            elif prop=="ENCODING":
                charGlyph.ENCODING = (int(line[1]))
            else:
                if doingBitmap: charGlyph.BITMAP.append(int(line[0],16))


    def getChar(self,char):
        """
        retrieve the character object from the Glyphs dictionary

        :param str char: like "A"
        :return Glyph: the character object
        """

        # Glyph table is keyed on encoding
        ordChar=ord(char)
        return self.Glyphs[ordChar]

    def getBitmap(self,char):
        if ord(char) in self.Glyphs:
            return self.Glyphs[ord(char)].BITMAP
        else:
            raise NoSuchGlyph("Character (" + char + ") not found in this font")

    def getFontBbox(self):
        w,h,x,y=self.FONTBOUNDINGBOX
        # using w on it's own causes letters to butt up to each other
        return w+1,h

    def getTextBbox(self,text):
        w, h, x, y = self.FONTBOUNDINGBOX
        return w*len(text),h