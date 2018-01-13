#!/usr/bin/env python
"""
Animator.py

Class to add animation sequences to a list and cycle through them at a pace detemined by
the fps of the animation.

This code also detects if we are running the simulator or real deal. It passes that info to each animation

"""
import time
from AnimInfo import AnimInfo
import Panel

class Animator(object):

    seq=None        # animation sequence
    fps=None        # passed in
    debug=False
    classname="Animator"

    def __init__(self, **kwargs):

        for key,value in kwargs.iteritems():
            setattr(self,key,value)

        self.animations = []

    def addAnimation(self, **kwargs):

        self.chain=None # text animations don't specify a chain

        for key,value in kwargs.iteritems():
            setattr(self,key,value)

        self.animations.append(AnimInfo(chain=self.chain,animSeq=self.seq,fps=self.fps))

    def setFPS(self,fps):
        """
        dynamically change the frames per second of the animation. On the Pi3
        I had trouble achieving 100 fps with some image animations

        :param fps: integer 1-200
        :return: Nothing
        """

        assert type(fps) is int,self.classname+".setFPS(): fps must be an int."
        assert fps>=1 and fps<=200,self.classname+".setFPS() fps must be between 1 and 200."

        if fps==self.fps: return    # nothing to do

        # scan the animations list and set the FPS

        self.fps=fps

        for a in self.animations:
            a.setFPS(fps)


    def run(self):
        """
        the animation run loop
        :return: Nothing
        """
        assert self.fps is not None,self.classname+".run() - fps not set."

        # if fps is integer 1/fps would be integer zero!
        frameInterval=1.0/self.fps

        if self.debug: print self.classname+".run() Frame interval=",frameInterval

        avg_frametime=0
        warned=False

        while True:

            # simulator window may have been closed
            if not Panel.isRunning():
                # possibly the Panel is taking time to initialise
                t0=time.time()
                while not Panel.isRunning():
                    if (time.time()-t0)>=5:
                        print self.classname+".run() panel is not running (5s timeout whilst waiting)."
                        exit(0)

            t0 = time.clock()    # start time for this frame

            # flush any artifacts
            Panel.Clear()


            # run through all the animations.
            # the animation list contains info about each animation
            # We call nextFrame() for each one on each pass
            for animInfo in self.animations:
                if animInfo is None:
                    print self.classname+".run() No animation info."
                    exit(1)

                if self.debug:
                    t2=time.clock()
                    animInfo.nextFrame()
                    t3=time.clock()
                    if (t3-t2)>frameInterval:
                        print self.classname+".run() anim.nextFrame() exceeded frameInterval; took","%.6f" % (t3-t2,) ,"for ",animInfo.animFunc.__class__.__name__,"frameInterval is",frameInterval
                else:
                    animInfo.nextFrame()

            # copy panel frame buffer to actual or simulator matrix

            Panel.UpdateDisplay()

            # work out if we need to wait before the next loop
            loopTime=time.clock() - t0

            # check if
            verbose=False
            if (loopTime>frameInterval) and not self.debug and verbose:
                print self.classname+".run() Animation frame interval exceeded - check animation durations. Total loopTime=",loopTime,"frameInterval=",frameInterval
                self.debug=True
                print "Animator debugging turned on to aid diagnosis."

            # slow down animation cycleto match the required frameInterval
            # this gives a repeatable time interval for the animations
            # 200fps may not be achievable.

            if self.debug:
                if avg_frametime==0:
                    avg_frametime=loopTime
                else:
                    avg_frametime=(avg_frametime+loopTime)/2

                if avg_frametime>frameInterval and not warned:
                    print self.classname+".run() Frame animations exceeded frameInterval %.3f took average of %.3f seconds" % (frameInterval,avg_frametime)
                    warned=True
            # wait till the next frame interval
            while loopTime < frameInterval:
                loopTime = time.clock() - t0
