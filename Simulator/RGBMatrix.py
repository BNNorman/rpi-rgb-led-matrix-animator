"""
Matrix

provides an opencv imshow window to display a NumpyImage

useage:-

mat=RGBMatrix(videoCapture=True,videoName="./HUB75 %dx%d.avi",)


"""
import threading

from Simulator.Exceptions import *
from LEDAnimator.NumpyImage import *
from LEDAnimator.Constants import *
from Simulator.RGBMatrixOptions import RGBMatrixOptions
import cv2

class RGBMatrix(object):

    # defaults
    options=RGBMatrixOptions()

    # internal variables

    video=None              # video stream, set if creating a video
    swapping=False
    readyForSync=False      # ties the display to the panel refresh rate
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
        pixelHeight = self.options.rows * self.options.chain_length


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


    def numpyEnlarge(self,img,scale):
        """
        6x faster than scipy zoom

        Simple Enlargement by duplicating pixels. Since LEDs are integer sizes
        this gives a more realistuic effect and doesn;t require anti-aliasing

        :param numpy ndarray img: the image to enlarge
        :param int scale:
        :return None: frameBuffer is resized
        """
        if scale==1:
            # don't need alpha on output
            self.frameBuffer=img[:ALPHA]
            return
        if scale<1:
            raise InvalidScale("numpyEnlarge can only be used to enlarge. Got scale factor "+str(scale))

        h,w=img.shape[:2]
        for x in xrange(w):
            for y in xrange(h):
                pixel = img[y, x]
                y1=y*scale
                y2=y1+scale
                x1=x*scale
                x2=x1+scale
                self.frameBuffer[y1:y2, x1:x2] = pixel[:ALPHA]



    def SetImage(self,img):
        """
        copies img to the frameBuffer for display
        does not need the simulator running to do this

        simulator picks up this image in it's run loop

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
        # it is expected to be bigger than the actual panel
        self.numpyEnlarge(img,self.options.scale)

        if self.video:
            self.video.write(self.frameBuffer)

    def startVideo(self,fname):
        """
        attempt to create a video stream.
        :param string fname: the output filename like video.avi
        :return None: self.video is set up as a stream (or not)
        """


        try:
            fourcc = cv2.cv.CV_FOURCC(*'DIVX')

        except Exception as e:
            #print "Exception ",e.args
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
        print "RGBMatrix.run() starting the simulator window."
        self.running = True

        # open a window and size if as required
        cv2.namedWindow(self.windowTitle)
        cv2.imshow(self.windowTitle, self.frameBuffer)

        r=0xFF & cv2.waitKey(1)
        if r<>255:
            print "RGBMatrix.run() setting up window failed (keyboard key stuck?)."
            return

        # frameDuration controls the refresh rate
        # so far I have not found any advantage in slowing it down
        #
        frameDuration=int(1000.0/self.options.fps)  # millisec
        #frameDuration=1
        print "RGBMatrix.run() entering the run loop frameDuration=%.2fms"%(frameDuration)

        while self.running:
            # refresh the displayed image
            cv2.imshow(self.windowTitle, self.frameBuffer)
            r=0xFF & cv2.waitKey(frameDuration)
            if r<>255:
                print "RGBMatrix.run() key pressed."
                self.running = False # window closes

        print "RGBMatrix.run() closed the simulator window."
        if self.video: self.video.release()
        cv2.destroyAllWindows()
        raise SimulatorWindowClosed


    def IsRunning(self):
        """
        used to check status of the imshow window display thread
        :return: True or False
        """
        return self.running