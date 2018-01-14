# Image Handling

All animations **may** use a background image **and** a foreground image. Image specific animations also use foreground 
images. For example the ImageAnimations.DissolveIn dissolves between the foreground and background images by changing the transparency of the
 foreground image to effect either a dissolve in or dissolve out.
  
When you specify an image in an animation sequence it is loaded and cached by [ImageCache.py](../../LEDAnimator/ImageCache.py), in case it may
 be reused. [AnimBase.py](../../LEDAnimator/AnimBase.py) is responsible for doing the following, in the order given.

- 1 transform (affine), if any  
- 2 scaling, if any
- 3 alignment, if any    

Scaling and transform are different because scaling uses the most appropriate anti-aliasing method depending on 
wether you are scaling the image up or down. You cannot mix both since scaling operates using the original image as 
the starting point.

Specifying an image is done in the animation sequence definition in this way :-
    
    bgnd=Image{imagePath="../Images/DAF_640_640.png", scaleMode="F", alignMode=("C","C")) 
    fgnd=Image(imagePath="../Images/tulips.jpg",scaleMode"F",alignMode=("C","C"))  
    
    background= AnimSequence.AnimSequence([  
        ImageAnimations.DissolveIn(duration=10, speed=0.1, fps=100, bgImage=bgnd, fgImage=fgnd)  
    ])  

The above will dissolve in  **../Images/tulips.jpg** covering **../Images/DAF_640_640.png**. It will stop dissolving and 
wait for the duration to expire before repeating

## loadInvisible

The load invisible option is useful when you want to fade in - i.e. start invisible

However, you may also need to prevent the canvas refreshing till the animation has finished handling the reset (ie 
wait till self.init has been set to False.

    def step():
        # speed control
        if self.isNotNextStep():
            # refreshCanvas can cause an image to appear before
            # it has been initialised - not good for fade in
            if not self.init: self.refreshCanvas()
            return

## scaleMode and alignMode

These determine the scaling and placement of the image as follows.

### scaleMode

The available modes are:-

-F(it) - the image is scaled to fit the panel - it will result in distorion if the image is not of the same aspect 
ratio as the panel
-H(orizontal) - the image is scaled so that width fits the panel. This may result in gaps above/below the image.
-V(ertical) -  the image is scaled so that heuight fits the panel. This may result in gaps to the left/right of the 
image.

Only the first letter is checked so Fart==Fit. LOL

Images are always scaled from the original to maintain the best quality.

### alignMode

This is a tuple and determines where the image is placed horizontally and vertically.

Horizontally:-
- L(eft) - align left
- R(ight) - align right
- M(iddle) - same as "C"
- C(entre) - align centre (or center)

Vertically:-
- T(op) - top
- B(ottom) - bottom
- M(iddle) - centre
- C(entre) - same as "M"

### debug

Setting the parameter **debug=True** will cause the image loading to produce debug messages. If you want them.

# Image Transforms

Transforms and scaling are applied to the original image in order to maintain the best quality. The original image is
 never altered. Consequently you must
 be careful of the order are made. For wexample if you change the colour then apply scaling the colour change will be
  lost.

The transforms are done using the openCV warpAffine method.

To apply a transform to an image use the **transMatrix=(a,b,c,d,e,f)** syntax. Where a to f are the 6 parts of an 
affine matrix :-  

    [a,b,c]  
    [d,e,f]  
        
Reading this https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_geometric_transformations
/py_geometric_transformations.html will help.

Some rotation transforms are pre-programmed to make life easier.

    1 rotateAboutCentre(degrees)  
    2 rotateAboutCentreRadians(radians)
    3 rotate(x,y,degrees) which rotates the image about x,y  
    4 rotateRadians(x,y,radians)  which rotates the image about x,y  
    5 shear(angle)

Read the NumpyImage doc for more details.

Suppose you specify a foreground image. You will be able to access this image, and its methods, in your animations 
using something like this:-

    self.fgImage.rotateAboutCentre(degrees)
    self.fgImage.getWidth()
    self.fgImage.setPixel(x,y,color)
    



