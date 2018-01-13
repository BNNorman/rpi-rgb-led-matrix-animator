"""
Text.py

a text object class used to tidy up

Useage:-

msg1=Text(text="some message",fontFace="BDF",fontSize=12,fgColor=Palette.XMAS,bgColour=Aqua.getPixelColor())

or

msg1=Text()
msg1.text="some message"
msg1.fontFace="BDF"
msg1.fgColour=Palette.XMAS
msg1.bgColour=Aqua.getPixelColor()

Then use in an AnimationSequence with:- text=msg1


"""

class Text():

    # available parameters
    text=None           # string
    fgColor=None        # Color or Palette or None
    bgColor=None        # Color or Palette or None
    fontFace=None       # "BDF" or FONT_HERSHEY_??
    fontSize=None       # integer, pixels
    multiColored=False  # if True each character is rendered cyclically using the Palette colours

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def getText(self):
        return self.text

    def getFgColor(self):
        return self.fgColor

    def getBgColor(self):
        return self.bgColor

    def getFontFace(self):
        return self.fontFace

    def getFontSize(self):
        return self.fontSize

    def getMultiColored(self):
        return self.multiColored