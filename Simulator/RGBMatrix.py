"""
Matrix

provides an opencv imshow window to display a NumpyImage

useage:-

mat=RGBMatrix(videoCapture=True,videoName="./HUB75 %dx%d.avi",)


"""
import numpy as np
import scipy.ndimage

import threading
#import cv2
from Simulator.Exceptions import *
from LEDAnimator.NumpyImage import *
import time
from LEDAnimator.Constants import *
from Simulator.RGBMatrixOptions import RGBMatrixOptions


class RGBMatrix(object):

    # defaults
    options=RGBMatrixOptions()

    # internal variables

    video=None              # video stream, set if creating a video
    classname="RGBMatrix"
    swapping=False
    readyForSwap=False
    running=False
    initDone=False

    pixelWidth=0            # width of panel in LEDs (Resolution)
    pixelHeight=0           # same for height
    screenWidth=0           # width & height of on-screen simulator window in pixels
    screenHeight=0          # same for height, calculated using scale

    windowTitle = "RGB Matrix Simulator"

    def __init__(self,**kwargs):

        # expectiong options=options_object
        for key,value in kwargs.iteritems():
            setattr(self,key,value)

        # make sure parameters are of the required data type
        self.options.validate()

        # calculate the window size in pixels
        pixelWidth = self.options.rows * self.options.parallel
        pixelHeight = self.options.rows * self.options.chain_len


        # on-screen window dimensions
        self.screenHeight = pixelHeight*self.options.scale
        self.screenWidth = pixelWidth*self.options.scale

        # create a blank screen so that we can open the simulator
        # window immediately.
        tmp=np.zeros((self.screenHeight,self.screenWidth,3),dtype=np.uint8)
        self.frameBuffer=tmp

        if self.options.videoCapture:
            fname = self.options.videoName.format(screenWidth=self.screenWidth, screenHeight=self.screenHeight,
                                           width=pixelWidth, height=pixelHeight)
            print "RGBMatrix: Recording video to ",fname
            self.startVideo(fname)
        else:
            print "RGBMatrix: Not recording video"

        # display updates done in another thread
        self.thread = threading.Thread(None, self.run)
        self.thread.start()
        self.initDone=True


    def _waitForInit(self):
        print "RGBMatrix.getShape() init not done - waiting"
        while not self.initDone:
            pass

    def getShape(self):
        """
        returns the unscaled size of the matrix (i.e num leds in x and y)
        :return: (vertical pixels,horiz pixels)
        """
        if self.initDone:
            return self.pixelHeight,self.pixelWidth

        self._waitForInit()


        return self.pixelHeight,self.pixelWidth

    def SetImage(self,img):
        """
        copies img to the frameBuffer for display
        does not need the simulator running to do this

        :param img: numpy image (NOT NumpyImage)
        :return: nothing
        """

        # opencv reads images in BGR order
        # If we are in RGB order change it now
        # see Constants.py for RGB_R
        if RGB_R==0:
            im=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        else:
            im=img

        # the on screen display will be a different size
        if self.options.scale==1:
            self.frameBuffer=im
        else:
            #extract just the RGB axes - alpha does not matter here
            # just scale up the x,y dimensions using linear interpolation
            # this gives a blocky appearance akin to a LED matrix
            # and is SIGNIFICANTLY faster than using cv2.resize()
            self.frameBuffer = scipy.ndimage.zoom(im[:,:,:3], (self.options.scale, self.options.scale, 1), order=0)

        if self.video:
            self.video.write(self.frameBuffer)

    def startVideo(self,fname):
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        self.video = cv2.VideoWriter(fname, fourcc, 10, (self.screenWidth, self.screenHeight))
        if self.video is None:
            print "VideoWriter failed to start."
        else:
            print "VideoWriter started ok"


    def run(self):
        """
        background task to refresh the display using the frameBuffer image.
        Terminates when any key is pressed.
        :return: Nothing
        """
        print self.classname+".run() starting the simulator window."
        self.running = True

        cv2.namedWindow(self.windowTitle)
        cv2.imshow(self.windowTitle, self.frameBuffer)

        r=cv2.waitKey(25)

        # frameDuration controls the refresh rate
        # so far I have not found any advantage in slowing it down
        #frameDuration=int(1000.0/self.options.fps)  # millisec
        frameDuration=1
        print self.classname + ".run() entering the run loop"

        while self.running:
            cv2.imshow(self.windowTitle, self.frameBuffer)
            #TODO: see if this works better running at max rate 1 millisec
            r=cv2.waitKey(frameDuration)

            if r<>255:
                self.running = False # window keepalive

        print self.classname + ".run() closed the simulator window."
        if self.video: self.video.release()
        cv2.destroyAllWindows()
        raise SimulatorWindowClosed


    def IsRunning(self):
        """
        used to check status of the imshow window display thread
        :return: True or False
        """
        return self.running