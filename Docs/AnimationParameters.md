# Animation Parameters

There are some standard parameters and then there are parameters specific to a given animation.

If you write your own animations you can add whatever you like BUT be careful not to re-use parameters which you will
 already find in the files AnimBase.py, TextAnimBase.py , PanelAnimBase.py, ImageAnimBase.py, ChainAnimBase.py.
 
## standard parameters

### duration

Defines how long the animation is allowed to run for before it is terminated so that the next animation in your 
sequence can take over.

### fps

Frames per second. Determines the animation loop time - sort of. And passed in so you can use it.

The animator loop cycles through your animation sequences and then, possibly, waits till the fps period is reached. 
If the period has passed it doesn't wait but tries to play catchup.

If the animation loop takes longer than 1/fps seconds a warning message is issued and debugging is turned on for the 
Animator.

### debug

If you want to debug your animation then use **debug=True** as a parameter. Then you can add comments to your 
animation code like:-

    if self.debug: print "some status message"
    
### startPause

The number of seconds you want the animation to wait before it actually runs. This might be to allow the viewer to 
see something before it changes.

### endPause

Similar to **startPause** but occurs at the end of your animation but only if your code calls **self.animationHasFinished()**
 first
 
### background

A plain color to use as the background. If it is a Palette then the background color is chosen cyclically from the 
palette.

Color must be specified like: Pink.getPixelColor() because this adjusts the rgb values to color match to your panel 
(See [ColorBalancing](ColorBalancing.md))

### fgImage

A foreground image object. see [Image Handling](ImageHandling.md)

Your code can manipulate this image (see [Image Animations](../LEDAnimator/ImageAnimations.py))

### bgImage

Similar to fgImage but rendered behind the fgImage and infront of background.

You code can manipulate this image if you wish. None of my example do (yet).

### speed

A speed factor. A factor of 1.0 is normal speed, 0.5 is half speed and so on.

Your animation **step()** function always receives calls at the fps rate. However, the animator provide a tick value 
(self.tick) to your animation. At normal speed the tick value increases by one on each tick. At double speed the tick
 value changes this way 0,2,4,6,8,10... and at half speed it changes like this 00112233445566. So, if your animation 
 is time based it can use the tick value like a clock to work out what it should be doing.
 
 As an example, a sine wave value math.sin(angle) can be implemented where angle = 2*Pi * (self.tick/fps).
 
 ### text
 
 A text object which consist of a message, a foreground color (or palette) and a background color or palette.
 
 Two font types are supported at the moment BDF and Hershey (from openCV).
 
 BDF fonts have a maximum size of 16 pixels
 
 ## multiColored
 
 If multiColored is specified, for text, each letter will be rendered from the fgColor cyclically. Otherwise the text
  message color will change on each reset.
 
 # Animation Specific Variables
 
 Generally, you should read the animation code to see what variables they use but:-
 
 ## Xpos,Ypos
 
 Used for general manipulation in some animations. For images fgImage and bgImage have their own Xpos and Ypos 
 variables.
 
## startPos(x,y) .. endPos(x,y) 

These are used by Image - SlideAndZoom, also by Line animations.

## zoom(start,end)

Used by SlideAndZoom. The image starts scaled by **start** and ends at **end**. A zoom factor of 1.0 means full size 
and so on. You need to know the sizes of your images. If you want it to fit a 64x64 panel then it needs to fit in the
 64x64 space.
 
 
