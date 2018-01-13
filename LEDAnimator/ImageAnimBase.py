"""
ImageAnimBase.py

All image animations sub-class this

It is here in case we need to do any pre or post processing

"""

from AnimBase import AnimBase

class ImageAnimBase(AnimBase):

    classname="ImageAnimBase"

    def __init__(self,**kwargs):

        super(ImageAnimBase,self).__init__(**kwargs)
