"""
PanelAnimations.py

Animations which don't fall into any other category and normally involve drawing over
the entire panel.

Animations may use foreground and background images and may draw on both.
If no foreground image is provided a black transparent image is created to draw on.

General Parameters

bgImage         Image       optional
fgImage         Image       optional, if omitted a blank is created
palette         Palette     colors to use
window          tuple       (x,y,w,h) some animations work in windows. If none the whole panel is used.
thickness       int         line thickness, ignored if filled
filled          bool        if the shape should be filled
alpha           int         0-255, transparency
lineType        int         LINE_AA (anti-aliased) or LINE_4 or LINE_8
multicolored    bool        If False, color changes when the sequence starts, True means that
                            colour changes happen on each tick
background      tuple       Color to use for the background
"""

from PanelAnimBase import PanelAnimBase
import Panel
from Palette import *
from Constants import *
from Helpers.PoissonLib import *

######################################################
#
# The animations
#
######################################################


class RandomRectangles(PanelAnimBase):
    """
    Draw randomly sized and colored rectangles on the panel or in the specified window

    Parameters

    filled      bool,   Rectangles are filled if True
    thickness   int,    line thickness, not relevant if filled
    palette     list,   color palette to use
    alpha       int,    0-255, transparency


    """

    filled=True
    thickness=1
    alpha=255
    palette=None
    multiColored=False

    # internal variables
    color=None   # current drawing color

    def step(self,chain=None):
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        # change color on every reset
        if self.init:
            self.fgImage.clear()
            assert self.palette is not None,"palette is required"
            self.color=self.getNextPaletteEntry().getPixelColor()
            self.init=False

        if self.multiColored:
            self.color = self.getNextPaletteEntry().getPixelColor()

        x=random.randint(0,Panel.width-2)   # rectangles min of 2x2
        y=random.randint(0,Panel.height-2)
        w=int((Panel.width-x)/2)
        h=int((Panel.height-y)/2)

        if w>2:
            w=random.randint(2,w)
        if h>2:
            h=random.randint(2,h)

        self.fgImage.drawRectangle((x,y),(x+w,y+h), self.color, self.filled)
        self.refreshCanvas()

class RandomCircles(PanelAnimBase):
    """
    draw random sized cricles which may or may not be filled.

    color changes every tick.

    Additional Parameters

    filled          bool    True means fill the circle
    thickness       int     line thickness, irrelevant if filled
    palette         Palette list of colors to use
    multicolored    Bool    True means colours changes every tick otherwise
                            changes every reset
    lineType        int     default LINE_AA (Anti-aliased)
    """

    filled=False
    thickness=1
    palette=None
    color=None
    multicolored=True
    lineType=LINE_AA    # anti-aliased

    def step(self,chain=None):
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        if self.init:
            assert self.palette is not None,"palette is required."
            self.fgImage.clear()
            self.color = self.getNextPaletteEntry().getPixelColor()
            self.init=False

        posX=random.randint(10,50)
        posY=random.randint(10,50)
        radius=random.randint(5,10)

        if self.multicolored:
            self.color=self.getNextPaletteEntry().getPixelColor()

        thickness=FILLED if self.filled else self.thickness
        self.fgImage.drawCircle((posX,posY),radius,self.color,thickness,self.lineType)
        self.refreshCanvas()

class RandomEllipses(PanelAnimBase):
    """
    draw random sized elipses which may or may not be filled

    color changes every tick.

    Additional Parameters

    filled      bool    True means fill the circle
    thickness   int     line thickness, irrelevant if filled
    palette     Palette list of colors to use
    lineType    int     default LINE_AA (anti-aliased)
    """

    filled = False
    thickness = 1
    lineType=LINE_AA
    palette = None

    def step(self, chain=None):
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        if self.init:
            assert self.palette is not None,"palette is required."
            self.fgImage.clear()
            self.init = False

        posX = random.randint(10, 50)
        posY = random.randint(10, 50)
        rad1 = random.randint(5, 10)
        rad2 = random.randint(5, 10)
        color = self.getNextPaletteEntry().getPixelColor()

        thickness = FILLED if self.filled else self.thickness

        self.fgImage.drawEllipse((posX, posY),(rad1,rad2), 360,0,360,color, thickness,self.lineType)
        self.refreshCanvas()

class RandomSparkle(PanelAnimBase):
    """
    fills the window/panel with random colors on every tick

    Additional Parameters

    window  tuple   (x,y,w,h) if None the whole panel is used
    """

    window=None

    def step(self,chain=None):
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        if self.init:
            # since the window is filled there's no need to clear it
            if self.window is None:
                self.window=(0,0,self.fgImage.getWidth(),self.fgImage.getHeight())
            self.init=False

        self.fgImage.fillWindowRandom(self.window)
        self.refreshCanvas()

class Line(PanelAnimBase):
    """
    draws a line between two coordinate pair tuples fromXY() and toXY()

    line color changes on every reset using the supplied palette

    Additional Parameters

    fromXY      tuple (x,y) start point
    toXY        tuple (x,y) end point

    """
    fromXY=(0,0)        # start coordinate of the line
    toXY=(0,0)          # end coordinate of the line
    thickness=1         # thickness of the line
    palette=None        # colors to use - includes alpha
    multiColored=False  # if True colours change every tick
    lineType=LINE_8     # default LINE_8

    # internal use only
    color=None          # selected from the palette

    def step(self,chain=None):
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        if self.init:
            assert self.palette is not None, "palette is required"

            self.color = self.getNextPaletteEntry().getPixelColor()
            self.init=False

        if self.multiColored:
            self.color = self.getNextPaletteEntry().getPixelColor()

        # draw a line on the output image
        self.fgImage.fgImage.drawLine(self.fromXY,self.toXY, self.color,self.thickness,self.lineType)
        # send it to the panel
        self.refreshCanvas()

class PolyLines(PanelAnimBase):
    """

    Given a list of points draws lines joining the points

    Additional Parameters

    thickness       int         line thickness
    lineType        int         default LINE_AA (anti-aliased) or LINE_4 or LINE_8
    points          tuple list  xy coords [(x0,y0)...(xn,yn)]
    multiColored    bool        if True, each line segment is a different colour
    palette         Palette     colours to use
    """

    thickness=1
    lineType=LINE_AA
    color=None
    points=[]
    multiColored=False
    palette=None
    isClosed=False

    def step(self,chain=None):
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        if self.init:
            assert len(self.points)<>0,"No points specified for the animation. Should be like 'pts=[(x0,y0)...(xn,yn)]'"
            assert type(self.points[0]) is tuple,"Points must be a list of tuples"

            self.color = self.getNextPaletteEntry().getPixelColor()
            self.init=False

        if self.multiColored:
            self.color=self.fgImage.drawPolyLines(self.points,self.palette,self.isClosed,self.thickness,self.lineType)
        else:
            self.fgImage.drawPolyLine(self.points,self.color,self.isClosed,self.thickness,self.lineType)

        self.refreshCanvas()

class Rainbow(PanelAnimBase):
    """

    Rainbow uses the supplied palette to fill the panel with vertical bands
    of colors drawn, cyclically, from the palette (compulsory).


    Additional Parameters

    bandWidth   int     number of pixels wide for each band
                        Should be wholly divisible into panel width

    palette     Palette list of Color objects to use
    """

    bandWidth=1     # width of each band
    palette=None    # palette to use

    def step(self,chain=None):

        # speed control
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        assert self.palette is not None,"palette is required."
        assert type(self.bandWidth) is int,"bandWidth must be an int"
        assert self.bandWidth>0,"bandWidth must be greater than zero."

        for X in range(0,Panel.width,self.bandWidth):
            self.color=self.getNextPaletteEntry().getPixelColor()
            # draw a solid rectangle on the output image
            # this defaults to an anti-aliased line but they are vertical
            self.fgImage.drawRectangle((X,0),(X+self.bandWidth,Panel.height),self.color,FILLED)

        # send it to the panel
        self.refreshCanvas()

class Twinkle(PanelAnimBase):
    """
    Twinkle creates a static list of random points (LEDs) then changes their color/brightness using a palette to
    select the colors to use.

    The random points are obtained from a Poisson Disc algorithm to ensure the points don't clump together.

    The parameter 'radius' controls the seperation and number of the points - bigger radius means less points.

    Additional Parameters

    radius  int     poisson disc radius
    palette Palette list of Color object to select colors from
    """


    radius=5
    checkPts=30 # number of points, on radius, to check for candidates
    palette=None

    p=None      # internal Poisson object
    stars=None  # those that twinkle
    busy=False  # Poisson takes a lot of time to generate, this blocks re-entry till done

    def step(self,chain=None):
        # speed control
        if self.isNotNextStep():
            self.refreshCanvas()
            return

        if self.init:
            self.fgImage.clear()
            if self.stars is None:
                p=PoissonLib()
                self.stars=p.getSamples(30,self.radius,Panel.width,Panel.height)
            self.init=False

        # main loop - iterate through the list of stars and
        # make them Twinkle by flickeing their colors

        for (x,y) in self.stars:

            color=self.getNextPaletteEntry().getPixelColor(brightness=random.uniform(0,1),alpha=random.uniform(0,1))


            # using int cords prevents setPixel rounding 63.8 to 64 which causes
            # an error as the arrays are zero based
            self.fgImage.setPixel(int(x),int(y),color)

        self.refreshCanvas()


# WAIT
class Wait(PanelAnimBase):
    """
    wait does nothing. It just allows you to add delays to sequences

    If you have included an fgImage or bgImage they will be displayed.

    """

    def step(self):
        self.refreshCanvas()
        pass

