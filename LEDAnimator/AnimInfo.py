"""
AnimInfo.py

Class to hold generic information about an animation

Used by Animator.

"""


class AnimInfo(object):
    classname = "AnimInfo"
    chain = None  # not used for non-chain based animations
    animSeq = None
    fps = None
    animFunc = None
    curPalEntry = 0
    palette = None

    # debugging
    debug = False
    id="[No id]"

    def __init__(self,**kwargs):
        """
        set any parameters passed in
        :param kwargs: key/value pairs
        """
        for key,value in kwargs.iteritems():
            setattr(self,key,value)


    def reset(self):
        """
        Added to enable resetting an animation to it's starting point

        :return:
        """
        if self.animFunc is not None:
            self.animFunc.reset()

    def nextFrame(self,debug=False):
        """
        called from Animator.run()
        iterates through the animation calling the reset() and step() functions
        :return: Nothing
        """

        self.debug=debug

        # initialise the next animation - setup animFunc

        if self.animFunc is None:
            self.animFunc = self.animSeq.getNextAnimation()

        # chain is ignored by non-chain based animations
        self.animFunc.chain=self.chain
        self.animFunc.id=self.id

        if self.animFunc.nextFrame(debug=self.debug,id=self.animFunc.id):
            self.animFunc = self.animSeq.getNextAnimation()

