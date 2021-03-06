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
import threading

class Animator(object):

    chain=None      # updated by addAnimation
    seq=None        # animation sequence
    fps=None        # passed in

    #debugging
    debug=False
    id="[No id]"
    warned=False
    running=False
    runThread=None

    def __init__(self, **kwargs):

        for key,value in kwargs.iteritems():
            setattr(self,key,value)

        self.animations = []
        self.running=False
        self.runThread=None

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


    def start(self,reset=True):
        """
        execute the run() method in a separate thread

        The reset parameter if True causes animations to start at the beginning
        otherwise they resume from where they left off

        :param bool reset: enable the animations to start over.
        :return: Nothing
        """

        if reset: self.reset()

        if self.runThread is not None:
            print("Animator background thread is running. Ignored.")
        self.runThread=threading.Thread(target=self.run)
        self.runThread.start()

    def stop(self):
        """
        stops the run() method

        :return:
        """
        self.running=False
        #wait for the run() method to exit
        while self.runThread is not None:
            pass
        Panel.Clear()
        Panel.UpdateDisplay()

    def reset(self):
        for animInfo in self.animations:
            animInfo.reset()


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

        warned=False
        self.running=True;

        while self.running:

            # simulator window may have been closed
            # this exits if so
            self.checkPanelIsRunning()

            t0 = time.time()    # start time for this frame

            Panel.Clear()

            # run through all the animations.
            # the animation list contains info about each animation
            # We call nextFrame() for each one on each pass
            for animInfo in self.animations:
                if animInfo is None:
                    print "Animator.run() No animation info."
                    exit(1)

                if self.debug:
                    t2=time.time()
                    animInfo.nextFrame(self.debug)
                    t3=time.time()
                    if (t3-t2)>frameInterval:
                        print "Animator.run() anim.nextFrame() took","%.6f" % (t3-t2,) ,"for ",\
                            animInfo.animFunc.__class__.__name__,"frameInterval is",frameInterval
                else:
                    animInfo.nextFrame(self.debug)

            # copy panel frame buffer to actual or simulator matrix

            Panel.UpdateDisplay()

            # work out if we need to wait before the next loop
            loopTime=time.time() - t0

            # check if
            if (loopTime>frameInterval) and not self.warned:
                print "Animator.run() Animation frame interval exceeded - check animation durations. " \
                                     "Total loopTime=",loopTime,"frameInterval=",frameInterval
                self.warned=True

            # slow down animation cycle to match the required frameInterval
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
                loopTime = time.time() - t0

        self.runThread=None