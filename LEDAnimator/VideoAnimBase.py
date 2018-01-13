"""
VideoPlayer.py

Enables the user to include video in the LED matrix.

ADVICE: Prescale your video to the final size for the best performance. Scaling a video frame by frame
can be slow.


"""

#TODO - complete VideoPlayerBase
from LEDAnimator import AnimBase

class VideoPlayerBase(AnimBase):

    videoPath=""    # path to video file
    transMat=()     # 2x3 transform matrix

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
