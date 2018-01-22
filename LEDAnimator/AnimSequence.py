'''
AnimSequence.py

Simply maintains the animation list and a method to get the next
animation in the sequence

'''

class AnimSequence():

    debug=False     # can be passed in for debugging
    id='[no id]'    # can be passed in to label error messages

    def __init__(self,animList):
        # animList contains a list of function pointers
        self.animList=[]

        for entry in animList:
            self.animList.append(entry) # could use deepcopy?

        self.curAnim=0
        self.listLen=len(animList)

        assert self.listLen<>0, "Zero length animation list. Check syntax of your animation sequence."

    def getNextAnimation(self):
        p=self.curAnim
        self.curAnim=(self.curAnim+1) % self.listLen #' wraps to 0
        return self.animList[p]