# LEDAnimator

## Introduction

The content of this document applies to ALL animations.

There are 3 main files which contain the animation code:-
1. ChainAnimations.py
2. TextAnimations.py
3. ImageAnimations.py 

These files can be edited to add your own extra animations. Each defines a similar base class which manages default parameters:-

1. duration - number of seconds the animation runs for (it is terminated when this expires)
2. fps - the frames per second rate of the animator
3. speed - relative speed of the animation 1.0 means the animation step routine is called on every fps tick
4. palette - a list of colours to use (Currently unused by image animations). Most of the provided animations cycle through the palette on each pass.

Other, user-defined, parameters may be added on a per-animation basis. See specific HOW-TO documents if you want to add extra animations.


## Duration

When an animation starts it runs until the duration is exceeded then it is frozen. If the animation is a cycle then it is possible that the cycle will terminate part way through. You need to adjust the duration to get the result you want. Bear in mind this will be affected by how many animations are running at any time and, probably, the hardware it is running on. A Raspberry Pi 3 was used for developing the code.

Your animation step() function can detect when the duration has been reached by using the following code:-

```
    if self.hasEnded():   
        do something here 
        return
```

## Speed
When the animator runs it cycles through the animation sequences calling the animation step() function once every 1/fps seconds. 

The speed of the animation can be controlled within the step() function with the code:- 

```
if self.isNotNextStep(): 
    return
```

Most animations run in discrete steps (ticks). At 200 fps there are 200 ticks per second. At a speed setting of 1.0 the tick count increases by one for every 1/200 seconds (tick=0,1,2,3,4,5,6...199). If the speed is set to 2.0 then the tick count increases by 2 every 1/200 seconds (0,2,4,6,8..198). Your animation code can use this to calculate where it is in it's cycle (if necessary).
If you set speed, say, to 0.5 then your step() function would be called at half speed.

Within the animation step() function the animation code can check the current 'clock' tick by calling self.calcTick() which returns an integer for the current tick. This will always cycle between 0 and fps-1.

### ChainAnimations

These are animations applied to a list of LEDs in an RGB matrix. A chain is simply a python list of X/Y coordinate pairs each of which represent an LED. Each has an associated colour. Changing the colours effects an animation.

The folders Chain Maker and Text Chain Maker contain some python programs for generating chains from a marked up SVG image.

### TextAnimations

Although text could be animated as a chain of LEDs it can also be drawn as simple mono-spaced text.

### ImageAnimations

These animations allow you to manipulate images and display the result. The original image is cached so that changes can be undone without the expense of a filesystem access. 

Use good quality images (better resolution than your LED matrix) but small enough to reduce memory usage.

Images are loaded and manipulated using the NumpyImage class in NumpyImage.py. Images are converted and resized to HSV using openCV. When output to the LED matrix using the hzeller drivers the images are converted to PIL format. With a small matrix this isn't a long process.

## Simulator

The library works with a real RGB LED panel or simulates the panel using TkInter. TkInter is problematic with refresh speed but, otherwise, is useful for intitial debugging of animations. And that's all it is for!

At the start of the library files you may see this code:-

```
 try:
    from rgbmatrix import graphics    
    simulating=False    
 except:
    from Simulator import graphics    
    simulating=True
```
On my windows machine PyCharm underlines rgbmatrix because it cannot be found. On my RasPi rgbmatrix IS imported and the except clause is ignored. Win-Win.

# Where Next

Read the Docs section