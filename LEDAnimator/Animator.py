#!/usr/bin/env python
"""
Animator.py

Class to add animation sequences to a list and cycle through them at a pace determined by
the fps of the animation.

If the Panel exits this code will halt

"""
import time
from AnimInfo import AnimInfo
import Panel

class Animator(object):

    chain=None      # updated by addAnimation
    seq=None        # animation sequence
    fps=None        # passed in

    #debugging
    debug=False
    id="[No id]"

    def __init__(self, **kwargs):

        for key,value in kwargs.iteritems():
            setattr(self,key,value)

        self.animations = []

    def addAnimation(self, **kwargs):

        self.chain=None # text animations don't specify a chain
        self.seq=None

        for key,value in kwargs.iteritems():
            setattr(self,key,value)

        self.animations.append(AnimInfo(chain=self.chain,animSeq=self.seq,fps=self.fps,id=self.id))

    def checkPanelIsRunning(self):
        # simulator window may have been closed
        if Panel.isRunning(): return

        # possibly the Panel is taking time to initialise
        # terminate if timeout reached

        t0 = time.time()
        while not Panel.isRunning():
            if (time.time() - t0) >= 5:
                if self.debug: print "Animator: panel is not running (5s timeout whilst waiting)."
                exit(0)

    def run(self):
        """
        the animation run loop
        :return: Nothing
        """
        assert self.fps is not None,"Animator.run() - fps not set."

        # if fps is integer 1/fps would be integer zero!
        frameInterval=1.0/self.fps

        if self.debug: print "Animator.run() Frame interval=",frameInterval

        avg_frametime=0

        while True:

            # simulator window may have been closed
            # this exits if so
            self.checkPanelIsRunning()

            t0 = time.clock()    # start time for this frame

            Panel.Clear()

            # run through all the animations.
            # the animation list contains info about each animation
            # We call nextFrame() for each one on each pass
            for animInfo in self.animations:
                if animInfo is None:
                    print "Animator.run() No animation info."
                    exit(1)

                if self.debug:
                    t2=time.clock()
                    animInfo.nextFrame(self.debug)
                    t3=time.clock()
                    if (t3-t2)>frameInterval:
                        print "Animator.run() anim.nextFrame() took","%.6f" % (t3-t2,) ,"for ",\
                            animInfo.animFunc.__class__.__name__,"frameInterval is",frameInterval
                else:
                    animInfo.nextFrame(self.debug)

            # copy panel frame buffer to actual or simulator matrix

            Panel.UpdateDisplay()

            # work out if we need to wait before the next loop
            loopTime=time.clock() - t0

            # check if
            if (loopTime>frameInterval) and not self.debug:
                print "Animator.run() Animation frame interval exceeded - check animation durations. " \
                                     "Total loopTime=",loopTime,"frameInterval=",frameInterval

            # slow down animation cycleto match the required frameInterval
            # this gives a repeatable time interval for the animations
            # 200fps may not be achievable.

            if self.debug:
                if avg_frametime==0:
                    avg_frametime=loopTime
                else:
                    avg_frametime=(avg_frametime+loopTime)/2

                print "Animator.run() Frame animations took average of %.6f seconds" % (avg_frametime)

            # wait till the next frame interval
            while loopTime < frameInterval:
                loopTime = time.clock() - t0
