"""

ChainAnimBAse.py

Base class for all LED chain animations.

Sub-class of AnimBase

"""
from AnimBase import AnimBase

class ChainAnimBase(AnimBase):

    brightness=1
    alpha=1

    chain=None              # the chain for this animation
    chainBuffer=None        # used to for rendering chains on transparent backgrounds

    def __init__(self, **kwargs):
        super(ChainAnimBase,self).__init__(**kwargs)

        self.targetSpeed = self.speed
        self.setSpeed(self.targetSpeed)

    def reset(self,**kwargs):
        super(ChainAnimBase,self).reset(**kwargs)




