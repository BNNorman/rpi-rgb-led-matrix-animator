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


    def nextFrame(self,debug=False):
        """
        called from Animator.run()
        iterates through the animation calling the reset() and step() functions
        :return: Nothing
        """

        self.debug=debug

        # initialise the next animation - setup animFunc
        #if not self.beginDone: self.begin()

        if self.animFunc is None:
            self.animFunc = self.animSeq.getNextAnimation()

        # chain is ignored by non-chain based animations
        if self.debug: print "AnimInfo.nextFrame() Calling nextFrame() for",self.animFunc
        self.animFunc.chain=self.chain
        if self.animFunc.nextFrame(self.debug):
            self.animFunc = self.animSeq.getNextAnimation()

