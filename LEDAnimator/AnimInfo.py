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
    beginDone = False  # has begin been called?
    #canvas = None
    #matrix = None  # in case the animation needs a private canvas
    curPalEntry = 0
    palette = None
    simulating = False  # default
    debug = False

    def __init__(self,**kwargs):
        """
        set any parameters passed in
        :param kwargs: key/value pairs
        """
        for key,value in kwargs.iteritems():
            setattr(self,key,value)

    def begin(self):
        """
        begin() is called once for each animation in a sequence to allow it to do any pre-run setup.
        It selects the next animation in a sequence, cycling back to the first then calls the animation's reset() function.
        :return: nothing, simply sets self.animFunc and calls reset()
        """

        self.animFunc=self.animSeq.getNextAnimation()

        # initialise the animation for first run
        self.animFunc.durationExpired=False
        self.animFunc.reset()

        # flag to ensure that the animation has been initialised for first run
        self.beginDone=True



    def nextFrame(self,debug=False):
        """
        called from Animator.run()
        iterates through the animation calling the reset() and step() functions
        :return: Nothing
        """

        self.debug=debug

        # initialise the next animation - setup animFunc
        #if not self.beginDone: self.begin()

        #time to move to next animation in the sequence?
        #if self.animFunc.durationExpired:
        #    if self.debug:
        #        print "AnimInfo.nextFrame() calling begin() for next animation in seq"
        #    self.begin()

        if self.animFunc is None:
            self.animFunc = self.animSeq.getNextAnimation()


        # chain is ignored by non-chain based animations
        if self.debug: print "AnimInfo.nextFrame() Calling nextFrame() for",self.animFunc
        self.animFunc.chain=self.chain
        if self.animFunc.nextFrame(self.debug):
            self.animFunc = self.animSeq.getNextAnimation()

