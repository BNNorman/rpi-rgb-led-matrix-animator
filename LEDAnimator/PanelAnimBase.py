"""
PanelAnimBase.py

Basis for animations which utilise the panel as a sort of drawing surface

"""

from AnimBase import AnimBase
import NumpyImage
import Panel
import Image

class PanelAnimBase(AnimBase):
    """
    Base class for panel animations

    Ensures there is,at least a foreground image to draw onto

    """

    def __init__(self,**kwargs):
        super(PanelAnimBase,self).__init__(**kwargs)

        # if not provided create an image to draw on
        if self.fgImage is None:
            self.fgImage = Image.Image(image=NumpyImage.NumpyImage(width=Panel.width, height=Panel.height,alpha=0))



