"""
AudioPlayerBase.py

Enables the user to drive the matrix from and AudioFile

"""

#TODO - complete VideoPlayerBase
from LEDAnimator import AnimBase

class AudioPlayerBase(AnimBase):

    audioPath=""    # path to video file

    def __init__(self,**kwargs):
        super(VideoPlayerBase,self).__init__(**kwargs)

    def pause(self):
        pass

    def play(self):
        pass

    def rewind(self):
        pass

    def seek(self):
        pass

    def getFrame(self):
        pass
