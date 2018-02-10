"""
Text.py

a text object class used to tidy up

Useage:-

msg1=Text(text="some message",fontFace="BDF",fontSize=12,fgColor=Palette.XMAS,bgColor=Aqua.getPixelColor())

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
    Xpos,Ypos=0,0
    lineType=None       # only used by hershey fonts

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def setPos(self,pos):
        """
        Set the current position of the text relative to the Panel.

        :param tuple pos: X,Y values
        :return None:
        """
        self.Xpos,self.Ypos=pos

    def getPos(self):
        """
        Get the current position of the text relative to the Panel.

        :return tuple: (x,y)
        """
        return self.Xpos,self.Ypos

    def getText(self):
        """
        get the text of the message.

        This is a user supplied value which defaults to None

        :return string: the text of the message
        """
        return self.text

    def getFgColor(self):
        """
        gets the foreground colour of the text.

        The color could be either a tuple or a Palette object

        :return color or Palette:
        """
        return self.fgColor

    def getBgColor(self):
        """
        gets the background colour of the text.

        The color could be either a tuple or a Palette object

        :return color or Palette:
        """
        return self.bgColor

    def getFontFace(self):
        """
        gets the FontFace of the text.

        Currently this could be 'BDF' or a cv2 FONT_HERSHEY_?? values

        This is a uer parameter.

        :return string or int: The font face
        """
        return self.fontFace

    def getFontSize(self):
        """
        get the current font size

        This is a user parameter

        :return int: text height in pixels (hopefully)
        """
        return self.fontSize

    def getMultiColored(self):
        """
        Return the multiColored flag.

        This is a user parameter (defaults to False)

        :return Bool: True or False
        """
        return self.multiColored