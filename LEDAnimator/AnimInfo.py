"""
AnimInfo.py

Class to hold generic information about an animation

Used by the Animator object. nextFrame() is called once per frame to allow the
animation to step through its sequence.

"""


class AnimInfo(object):
    classname = "AnimInfo"

    chain = None        # passed in if needed
    animSeq = None      # current animation sequence
    animFunc = None     # current animation function
    beginDone = False   # has begin been called to initialise the animation on first pass?


    debug = False

    def __init__(self,**kwargs):
        """
        set any parameters passed in
        :param kwargs: key/value pairs
        """
        for key,value in kwargs.iteritems():
            setattr(self,key,value)

    def nextFrame(self):
        """
        called from Animator.run()
        iterates through the animation calling the reset() and step() functions
        :return: Nothing
        """

        # initialise the next animation - setup animFunc
        # this call should only happen on first run
        if not self.beginDone:
            self.animFunc = self.animSeq.getNextAnimation(debug=self.debug)
            # initialise the animation for first run
            self.animFunc.reset()
            self.beginDone=True

        # chain is ignored by non-chain based animations
        # animFunc.nextFrame returns False until the duration has expired
        if self.chain and self.animFunc.chain is None:
            self.animFunc.chain=self.chain

        if self.animFunc.nextFrame():
            if self.debug:
                print self.classname+".nextFrame() animation duration HAS expired for",self.animFunc

            # move on to next animation in the sequence
            self.animFunc = self.animSeq.getNextAnimation(debug=self.debug)
            self.animFunc.reset()


