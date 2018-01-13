'''
AnimSequence.py

Simply maintains the animation list and a method to get the next
animation in the sequence

'''

class AnimSequence():

    def __init__(self,animList=[]):
        # animList contains a list of function pointers
        self.animList=[]

        for entry in animList:
            self.animList.append(entry)

        self.curAnim=0
        self.listLen=len(animList)

        assert self.listLen<>0, "Zero length animation list. Check syntax of your animation sequence."

    def getNextAnimation(self,debug=False):
        p=self.curAnim
        self.curAnim=(self.curAnim+1) % self.listLen #' wraps to 0
        if debug : print "AnimSequence.getNextAnimation() returns item",p
        return self.animList[p]